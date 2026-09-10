"""Round-trip a ``.blend`` asset library through Python source.

:func:`dump_library` writes every node-group asset in a ``.blend`` to its own
``.py`` file (via :func:`nodebpy.export.to_python` in ``class`` mode), and
:func:`build_library` rebuilds the ``.blend`` from those files. The intent is
that only the ``.py`` files are checked into version control — the ``.blend``
is a build artifact (rebuilt for shipping, or for tweaking node trees by hand
in Blender before dumping them back out).

Every node group's class is defined in exactly one file, so the sources stay
hand-editable without divergent copies:

- each **asset** gets its own module holding its class, an ``ASSET`` name
  pointing at it, and — when present — an ``ASSET_METADATA`` dict (catalog id,
  description, author, tags, …); non-default tree flags (``is_modifier``,
  description, …) ride on every generated class as ``_tree_properties``;
- a helper group used by **only that asset** is embedded in the same module;
- a group nested by **several** assets gets its own module under
  ``_shared/``, and an asset nested inside **another asset** keeps its class in
  its own asset module — dependents ``import`` these instead of re-defining
  them.

The import graph mirrors the group-nesting graph, which Blender guarantees is
acyclic (a group cannot contain itself), so arbitrarily deep asset-in-asset
nesting can never produce an import cycle. At build time
:meth:`~nodebpy.builder.NodeGroupBuilder.create_group` reuses an existing tree
by name, so each group is still built exactly once.

**Materials** referenced by the dumped trees (a Material socket or interface
default) are code-generated too: each becomes a module under ``materials/``
holding its shader tree as a class, a ``MATERIAL`` marker and a
``MATERIAL_PROPERTIES`` dict. Build recreates the material and runs the class
body into ``material.node_tree`` — a material is never a node group, so its
class is only a recipe, never ``create_group``-ed. A material's nested shader
groups take part in the normal shared/embedded classification.

**Datablocks that cannot be serialised** (images, objects, collections, …)
are recorded per module in a ``DATABLOCK_DEPENDENCIES`` footer. At build time
they resolve in order: already present in the session ("build in the
presence" of the data), appended by name from a ``resources`` ``.blend``, or
— with ``on_missing="drop"`` — replaced by temporary placeholders that are
deleted before the ``.blend`` is written, leaving those socket defaults
empty. The default is a hard error listing exactly what is missing.

Asset previews are not round-tripped (they are binary); regenerate them in
Blender after a rebuild if needed. An asset catalog definition file
(``blender_assets.cats.txt``) sitting next to the source is copied alongside
the output in both directions, so catalog assignments survive the trip.

Both directions assume a session without unrelated node groups: appending
renames on a name clash (which would corrupt the dumped ``_name``), and
rebuilding reuses same-named trees (which would bake a stale group into the
``.blend``). The CLI (``python -m nodebpy.assets dump/build``) runs in a fresh
``bpy`` session, which satisfies this by construction.
"""

from __future__ import annotations

import importlib
import importlib.machinery
import importlib.util
import os
import re
import shutil
import sys
import uuid
from pathlib import Path

import bpy

from ..builder import NodeGroupBuilder, TreeBuilder, build_from_source
from ..builder._utils import normalize_name
from ..export.codegen import (
    _ID_COLLECTIONS,
    GroupInterface,
    _class_name,
    _fmt,
    _format_with_ruff,
    to_python,
)
from ._codegen import _TREE_MODULES

# Tree-type bl_idname → subdirectory the dumped modules are written into.
# Asset names repeat across editors (a geometry and a compositor "Combine
# Spherical" both exist), so splitting keeps filenames collision-free. The
# same table drives the per-tree module split in the typed-API generator.
_TREE_DIRS: dict[str, str] = _TREE_MODULES

# Directory for code-generated materials referenced by the dumped trees.
_MATERIALS_DIR = "materials"

# The datablock-dependency scan and cleanup share codegen's ID.id_type →
# bpy.data collection table (imported above as _ID_COLLECTIONS).

# bpy.data collections the dump appends dependencies into and cleans back
# out: node groups plus every datablock kind the dependency scan can record.
_CLEANUP_COLLECTIONS = ("node_groups", *_ID_COLLECTIONS.values())

# Collections that can stand in a placeholder for on_missing="drop": the
# placeholder satisfies the bpy.data lookup during the build and is deleted
# before the .blend is written, which nulls the referencing socket defaults.
_PLACEHOLDER_FACTORIES = {
    "materials": lambda name: bpy.data.materials.new(name),
    "images": lambda name: bpy.data.images.new(name, 1, 1),
    "objects": lambda name: bpy.data.objects.new(name, None),
    "collections": lambda name: bpy.data.collections.new(name),
    "texts": lambda name: bpy.data.texts.new(name),
}

# Asset-metadata fields that round-trip through ASSET_METADATA (plus tags,
# handled separately as a collection). ``catalog_simple_name`` is deliberately
# absent: it is read-only on AssetMetaData (Blender derives it from
# ``catalog_id`` and the catalog definition file), so it is neither dumped nor
# applied — a stale key in an older dump's metadata is ignored at build time.
_METADATA_FIELDS = (
    "description",
    "author",
    "copyright",
    "license",
    "catalog_id",
)

# An unassigned catalog — not worth dumping.
_NIL_CATALOG = "00000000-0000-0000-0000-000000000000"

# Tree-level properties (description, modifier/tool flags, …) now ride on
# each generated class as ``_tree_properties`` (see nodebpy.export.codegen);
# build_library still applies a legacy TREE_PROPERTIES footer when an older
# dump carries one.

# Material-level properties (beyond the shader tree) worth round-tripping.
# Only values differing from a fresh material's defaults are dumped;
# properties a Blender version doesn't have are skipped.
_MATERIAL_PROP_CANDIDATES = (
    "diffuse_color",
    "metallic",
    "roughness",
    "surface_render_method",
    "displacement_method",
    "use_backface_culling",
    "use_transparency_overlap",
    "use_transparent_shadow",
    "blend_method",
    "pass_index",
)

#: Catalog definition file that Blender keeps next to an asset library.
CATALOG_FILENAME = "blender_assets.cats.txt"


def _asset_metadata(group) -> dict[str, object]:
    """The dumpable asset metadata of ``group``, non-empty fields only."""
    asset_data = group.asset_data
    if asset_data is None:  # pragma: no cover - assets_only appends stay marked
        return {}
    meta: dict[str, object] = {}
    for field in _METADATA_FIELDS:
        value = getattr(asset_data, field, "")
        if value and value != _NIL_CATALOG:
            meta[field] = value
    tags = tuple(tag.name for tag in asset_data.tags)
    if tags:
        meta["tags"] = tags
    return meta


def _material_properties(material) -> dict[str, object]:
    """Material-level properties of ``material`` that differ from a fresh
    material's defaults, probed against a throwaway material."""
    probe = bpy.data.materials.new("_nodebpy_dump_probe")
    assert probe is not None
    try:
        props: dict[str, object] = {}
        for name in _MATERIAL_PROP_CANDIDATES:
            if not hasattr(probe, name):  # pragma: no cover - other Blender versions
                continue
            value = getattr(material, name)
            default = getattr(probe, name)
            if not isinstance(value, (str, int, float, bool)):
                try:  # bpy float arrays (diffuse_color) repr as data paths —
                    value, default = tuple(value), tuple(default)  # dump tuples
                except TypeError:  # pragma: no cover - unexpected prop shape
                    continue
            if value != default:
                props[name] = value
        return props
    finally:
        bpy.data.materials.remove(probe)


def _id_defaults(tree) -> dict[str, set[str]]:
    """``{bpy.data collection: {names}}`` of ID datablocks referenced by
    ``tree`` — socket and interface defaults plus node pointer properties
    (e.g. an Image Texture's image). Node trees are excluded: groups are
    dumped as classes rather than treated as data dependencies."""
    found: dict[str, set[str]] = {}

    def record(value) -> None:
        if not isinstance(value, bpy.types.ID) or isinstance(value, bpy.types.NodeTree):
            return
        collection = _ID_COLLECTIONS.get(value.id_type)
        if collection is not None:
            found.setdefault(collection, set()).add(value.name)

    for node in tree.nodes:
        for prop in node.bl_rna.properties:
            if prop.type == "POINTER":
                record(getattr(node, prop.identifier, None))
        for socket in node.inputs:
            record(getattr(socket, "default_value", None))
    for item in tree.interface.items_tree:
        if getattr(item, "item_type", "") == "SOCKET":
            record(getattr(item, "default_value", None))
    return found


def _dict_lines(name: str, data: dict[str, object]) -> list[str]:
    lines = [f"{name} = {{"]
    lines += [f"    {_fmt(key)}: {_fmt(value)}," for key, value in data.items()]
    lines.append("}")
    return lines


def _direct_refs(tree) -> set[str]:
    """Names of the node groups directly referenced by ``tree``'s group nodes."""
    refs: set[str] = set()
    for node in tree.nodes:
        inner = getattr(node, "node_tree", None)
        if inner is not None:
            refs.add(inner.name)
    return refs


def _assign_class_names(display_names: dict[str, str]) -> dict[str, str]:
    """A globally unique PascalCase class name per tree key, derived from the
    key's display name and assigned in sorted order so the result is
    deterministic across dumps. Global uniqueness matters because the classes
    span modules that import each other — two same-named classes would
    collide in the importing module's namespace."""
    class_names: dict[str, str] = {}
    used: set[str] = set()
    for key in sorted(display_names, key=lambda k: (display_names[k], k)):
        base = _class_name(display_names[key])
        name, n = base, 1
        while name in used:
            n += 1
            name = f"{base}{n}"
        used.add(name)
        class_names[key] = name
    return class_names


def _assign_stems(group_names: list[str]) -> dict[str, str]:
    """A unique module filename stem per group within one directory, assigned
    in sorted order so the result is deterministic across dumps."""
    stems: dict[str, str] = {}
    used: set[str] = set()
    for group_name in sorted(group_names):
        base = normalize_name(group_name)
        if base.startswith("_"):
            # A "_"-prefixed module would be skipped as non-root by the build
            # (the _shared convention); digit-led names ("2 Index Angle")
            # take an "n" prefix instead.
            base = "n" + base.lstrip("_")
        stem, n = base, 1
        while stem in used:
            n += 1
            stem = f"{base}_{n}"
        used.add(stem)
        stems[group_name] = stem
    return stems


def _relative_import(target_module: str, from_module: str) -> str:
    """The relative module reference from one dumped module to another, both
    given as ``/``-separated paths from the output root (``"geometry/scale_up"``,
    ``"geometry/_shared/utils"``, ``"materials/glass"``)."""
    target = target_module.split("/")
    source = from_module.split("/")
    common = 0
    while (
        common < min(len(target), len(source)) - 1 and target[common] == source[common]
    ):
        common += 1
    ups = len(source) - 1 - common  # levels above the source module's package
    return "." * (ups + 1) + ".".join(target[common:])


def _insert_imports(code: str, import_lines: list[str]) -> str:
    """Insert ``import_lines`` after the leading import block of ``code``."""
    if not import_lines:
        return code
    lines = code.split("\n")
    idx = 0
    for i, line in enumerate(lines):
        if line.startswith(("import ", "from ")):
            idx = i + 1
        elif line.strip():
            break
    return "\n".join(lines[:idx] + import_lines + lines[idx:])


def _render_group_module(
    group,
    *,
    kind: str,  # "asset" | "shared" | "material"
    class_name: str,
    import_lines: list[str],
    class_names: dict[str, str],
    external: set[str],
    dependencies: dict[str, tuple[str, ...]],
    material_name: str | None = None,
    nodebpy_pkg: str,
    snapshot_positions: bool,
    keep_reroutes: bool,
    format: bool,
    typed_groups: set[str] | None = None,
    root_interface: GroupInterface | None = None,
) -> str:
    """The full source for one dumped ``.py`` module: the tree's class (plus
    any embedded helper classes), imports for externally defined classes, and
    the marker/metadata footers for its kind."""
    code = to_python(
        group,
        top_level="class",
        nodebpy_pkg=nodebpy_pkg,
        snapshot_positions=snapshot_positions,
        keep_reroutes=keep_reroutes,
        format=False,
        group_class_names=class_names,
        external_groups=external,
        typed_groups=typed_groups,
        root_interface=root_interface,
    )
    code = _insert_imports(code, import_lines)

    # Deliberately no source filename/timestamp in the header: a dump must be
    # byte-identical across a no-op round-trip so it leaves no VCS diff.
    label = {
        "asset": f'Node-group asset "{group.name}" ({group.bl_idname})',
        "shared": f'Node group "{group.name}" ({group.bl_idname})',
        "material": f'Material "{material_name}"',
    }[kind]
    header = [
        f"# {label}, dumped by nodebpy.assets.dump_library.",
        (
            "# Rebuild the library with nodebpy.assets.build_library"
            " (python -m nodebpy.assets build)."
        ),
    ]
    if kind == "shared":
        header.append(
            "# Shared by several assets, which import it; not an asset itself."
        )
    if root_interface is not None:
        header.append(
            "# _build_group() is the source of truth: the docstring, __init__ "
            "and accessors are regenerated from it on the next dump."
        )
    if kind == "material":
        header.append(
            "# The class is a recipe for the material's shader tree — build "
            "recreates the material and runs it into material.node_tree."
        )
    header.append("")

    footer: list[str] = []
    if kind == "asset":
        footer = ["", "", f"ASSET = {class_name}"]
        meta = _asset_metadata(group)
        if meta:
            footer += [""] + _dict_lines("ASSET_METADATA", meta)
    elif kind == "material":
        assert material_name is not None
        footer = [
            "",
            "",
            f"MATERIAL = {class_name}",
            f"MATERIAL_NAME = {_fmt(material_name)}",
        ]
        material = bpy.data.materials[material_name]
        props = _material_properties(material)
        if props:
            footer += [""] + _dict_lines("MATERIAL_PROPERTIES", props)
    if dependencies:
        footer = footer or ["", ""]
        footer += [""] + _dict_lines(
            "DATABLOCK_DEPENDENCIES", dict(sorted(dependencies.items()))
        )

    source = "\n".join(header) + code + "\n".join(footer) + "\n"
    return _format_with_ruff(source) if format else source


_INIT_CONTENT = "# Package marker for nodebpy-dumped asset sources.\n"

_GENERATED_INIT_HEADER = (
    "# Auto-generated by nodebpy.assets.dump_library — do not edit manually."
)


def _write_dir_exports(directory: Path, exports: list[tuple[str, str]]) -> None:
    """Write ``directory``'s ``__init__.py`` re-exporting its asset classes
    (``exports`` is ``[(module stem, class name), ...]``). A hand-written
    ``__init__.py`` (anything not starting with a nodebpy marker) is left
    untouched."""
    init = directory / "__init__.py"
    if init.exists():
        first_line = init.read_text(encoding="utf-8").split("\n", 1)[0]
        if first_line not in (_GENERATED_INIT_HEADER, _INIT_CONTENT.rstrip("\n")):
            return
    lines = [_GENERATED_INIT_HEADER]
    lines += [f"from .{stem} import {cls}" for stem, cls in exports]
    names = ",\n    ".join(f'"{cls}"' for cls in sorted(cls for _, cls in exports))
    lines += ["", f"__all__ = (\n    {names},\n)"]
    init.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _ensure_init(directory: Path) -> None:
    """Make ``directory`` a package so the dumped relative imports resolve
    when the sources are imported as part of a larger package; an existing
    ``__init__.py`` (e.g. hand-written) is left untouched."""
    init = directory / "__init__.py"
    if not init.exists():
        init.write_text(_INIT_CONTENT, encoding="utf-8", newline="\n")


def _copy_catalog_file(src_dir: Path, dst_dir: Path) -> None:
    """Carry the asset catalog definitions alongside, if the source has one."""
    catalog = src_dir / CATALOG_FILENAME
    if catalog.is_file():
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(catalog, dst_dir / CATALOG_FILENAME)


def dump_library(
    blend_path: str | Path,
    output_dir: str | Path,
    *,
    names: set[str] | None = None,
    nodebpy_pkg: str = "nodebpy",
    snapshot_positions: bool = False,
    keep_reroutes: bool = False,
    materials: bool = True,
    format: bool = True,
    typed_api: bool = False,
) -> dict[str, Path]:
    """Dump every node-group asset in ``blend_path`` to Python source files.

    Each asset becomes one ``.py`` module under ``<output_dir>/<tree>/``
    (``geometry``/``shader``/``compositor``) with an ``ASSET`` marker and
    metadata footers. Every group class is defined exactly once: helper groups
    used by a single asset are embedded in that asset's module, groups nested
    by several assets get their own module under ``<tree>/_shared/``, and an
    asset nested inside other assets keeps its class in its own module — all
    referenced via relative imports (``__init__.py`` package markers are
    written so the imports resolve). Materials referenced by the trees are
    code-generated into ``materials/`` modules, and other non-serialisable
    datablocks each module needs are recorded in its
    ``DATABLOCK_DEPENDENCIES`` footer. :func:`build_library` rebuilds the
    ``.blend`` from these files. A ``blender_assets.cats.txt`` next to the
    ``.blend`` is copied into ``output_dir`` so catalog assignments travel
    with the sources.

    Each asset is appended into the current session for introspection and the
    appended groups are removed again afterwards. Run this in a session that
    doesn't already hold node groups with the same names — appending renames on
    a clash, which would corrupt the dumped ``_name`` attributes; a clash
    raises instead. The CLI (``python -m nodebpy.assets dump``) runs in a fresh
    session by construction.

    Parameters
    ----------
    blend_path:
        The ``.blend`` asset library to dump.
    output_dir:
        Directory to write the per-asset modules into (created if needed).
    names:
        Restrict the dump to these asset (node-group) names; defaults to all.
        A full dump first clears the managed subdirectories
        (``geometry``/``shader``/``compositor``/``materials``) so files from
        renamed or deleted assets don't linger; a filtered dump leaves the
        other assets' files in place.
    nodebpy_pkg:
        Import anchor for nodebpy in the generated sources, as for
        :func:`nodebpy.export.to_python`.
    snapshot_positions:
        Preserve each node's authored editor position so a rebuilt ``.blend``
        opens with the same layout, instead of auto-arranging. Positions churn
        on every edit, so leave this off when minimal VCS diffs matter more
        than layout fidelity.
    keep_reroutes:
        Preserve reroute nodes instead of collapsing them into direct links.
    materials:
        Code-generate materials referenced by the dumped trees into
        ``materials/`` modules (the default). With ``False`` they are only
        recorded as ``DATABLOCK_DEPENDENCIES``, to be resolved at build time
        like any other non-serialisable datablock.
    format:
        Run the generated sources through ``ruff format`` when available.
    typed_api:
        Merge the typed asset API into the dumped classes: each asset class
        gains a numpydoc docstring, ``_Inputs``/``_Outputs`` accessors and a
        typed ``__init__``, subclasses ``Asset*Group`` and carries
        ``_library = PackageLibrary(__file__, <relative path to blend_path>)``
        — so at runtime it *appends* the shipped ``.blend`` while its
        ``_build_group`` remains the source of truth that regenerates it
        (``build_library`` builds from source via
        :func:`nodebpy.builder.build_from_source`). Shared helper modules get
        the typed API too (but stay ``Custom*Group`` — they are not assets),
        group calls in generated bodies use the typed parameter names, and
        each tree directory's ``__init__.py`` re-exports its asset classes.
        Everything outside ``_build_group`` is regenerated on the next dump.

    Returns
    -------
    dict[str, Path]
        Mapping of asset name to the file it was written to.
    """
    blend_path = Path(blend_path)
    output_dir = Path(output_dir)
    if not blend_path.is_file():
        raise FileNotFoundError(f"Asset library not found: {blend_path.resolve()}")

    # Append every wanted asset in one load, so groups shared between assets
    # (including assets nested in other assets) arrive as single trees and the
    # sharing structure can be read off the session directly. Dependencies of
    # other kinds (materials, images, …) come along too; everything appended
    # is cleaned back out afterwards. The pre-append checks run inside the
    # load context (the load itself happens on exit, with nothing selected
    # when a check raises), so the .blend is opened only once.
    before = {
        coll: set(getattr(bpy.data, coll).keys()) for coll in _CLEANUP_COLLECTIONS
    }
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(blend_path), link=False, assets_only=True
    ) as (src, dst):
        available = list(src.node_groups)
        wanted = [n for n in available if names is None or n in names]
        if names is not None and (missing := names - set(wanted)):
            raise KeyError(f"Assets not found in {blend_path}: {sorted(missing)}")
        clashes = sorted(n for n in wanted if n in bpy.data.node_groups)
        if clashes:
            raise RuntimeError(
                f"Node groups already exist in this session: {clashes}. "
                "Appending would rename them and corrupt the dumped sources — "
                "dump from a fresh session (e.g. python -m nodebpy.assets dump)."
            )
        dst.node_groups = list(wanted)
    added = {
        coll: [db for db in getattr(bpy.data, coll) if db.name not in before[coll]]
        for coll in _CLEANUP_COLLECTIONS
    }
    try:
        # Any appended datablock (not just a group) arriving renamed means a
        # same-named datablock already sat in the session; the '.001' name
        # would be baked into DATABLOCK_DEPENDENCIES and the generated
        # bpy.data lookups, silently corrupting the dump.
        renamed = sorted(
            f"{coll}[{db.name!r}]"
            for coll, dbs in added.items()
            for db in dbs
            if (m := re.fullmatch(r"(.*)\.\d{3}", db.name)) and m[1] in before[coll]
        )
        if renamed:
            raise RuntimeError(
                f"Appending renamed dependency datablocks {renamed} because "
                "same-named datablocks already exist in this session — dump "
                "from a fresh session."
            )
        written = _dump_appended(
            list(dst.node_groups),
            added["node_groups"],
            output_dir,
            nodebpy_pkg=nodebpy_pkg,
            snapshot_positions=snapshot_positions,
            keep_reroutes=keep_reroutes,
            materials=materials,
            format=format,
            library_blend=blend_path.resolve() if typed_api else None,
            # A full dump owns the managed subdirectories: clear stale modules
            # from assets since renamed or deleted, so the next build_library
            # doesn't silently resurrect them. A filtered dump (names=...)
            # leaves the other assets' files alone.
            clean_stale=names is None,
        )
    finally:
        for coll in _CLEANUP_COLLECTIONS:
            data = getattr(bpy.data, coll)
            for db in added[coll]:
                data.remove(db)

    _copy_catalog_file(blend_path.parent, output_dir)
    return written


def _is_generated_init(path: Path) -> bool:
    """Whether ``path`` is an ``__init__.py`` nodebpy wrote (marker or plain
    package marker) rather than a hand-written one."""
    first_line = path.read_text(encoding="utf-8").split("\n", 1)[0]
    return first_line in (_GENERATED_INIT_HEADER, _INIT_CONTENT.rstrip("\n"))


def _remove_stale_modules(output_dir: Path, written: set[Path]) -> None:
    """Remove modules under the managed subdirectories that this dump did not
    write — leftovers from assets since renamed or deleted. Hand-written
    ``__init__.py`` files survive; directories left holding nothing but a
    generated ``__init__.py`` are pruned entirely."""
    keep = {path.resolve() for path in written}
    for dirname in (*_TREE_DIRS.values(), _MATERIALS_DIR):
        base = output_dir / dirname
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            if path.name != "__init__.py" and path.resolve() not in keep:
                path.unlink()
        subdirs = sorted((p for p in base.rglob("*") if p.is_dir()), reverse=True) + [
            base
        ]
        for sub in subdirs:
            entries = list(sub.iterdir())
            if (
                len(entries) == 1
                and (init := entries[0]).name == "__init__.py"
                and _is_generated_init(init)
            ):
                init.unlink()
                entries = []
            if not entries:
                sub.rmdir()


def _dump_appended(
    asset_trees: list,
    appended: list,
    output_dir: Path,
    *,
    nodebpy_pkg: str,
    snapshot_positions: bool,
    keep_reroutes: bool,
    materials: bool,
    format: bool,
    library_blend: Path | None = None,
    clean_stale: bool = False,
) -> dict[str, Path]:
    """Partition the appended groups (and referenced materials) into modules
    and write them.

    ``asset_trees`` are the trees dumped as assets; ``appended`` is every
    group the load brought in (the assets plus all their dependencies).
    ``library_blend`` (the resolved ``.blend`` path) turns on the merged
    typed API — see ``dump_library(typed_api=...)``. ``clean_stale`` removes
    modules under the managed subdirectories that this dump did not write
    (hand-written ``__init__.py`` files are kept, as ever).
    """
    # Unsupported tree types (e.g. texture trees) can't be code-generated;
    # skip those assets — their private dependencies drop out with them.
    unsupported = [t for t in asset_trees if t.bl_idname not in _TREE_DIRS]
    for tree in unsupported:
        print(f"  skipping {tree.name!r}: unsupported tree type {tree.bl_idname}")
    asset_trees = [t for t in asset_trees if t.bl_idname in _TREE_DIRS]
    asset_names = {t.name for t in asset_trees}
    trees = {g.name: g for g in appended}

    # Non-serialisable datablocks each group references, by tree name.
    id_deps = {g.name: _id_defaults(g) for g in appended}

    # Materials referenced anywhere in the dump are code-generated too: their
    # embedded shader tree joins the group universe as an extra root. Embedded
    # trees all ship named "Shader Nodetree" and the name is read-only, so
    # material trees are keyed synthetically ("material:<name>") and the class
    # name is overridden per emission instead.
    material_trees: dict[str, str] = {}  # tree key → material name
    if materials:
        referenced = sorted(
            {name for deps in id_deps.values() for name in deps.get("materials", ())}
        )
        for mat_name in referenced:
            material = bpy.data.materials.get(mat_name)
            if material is None or material.node_tree is None:  # pragma: no cover
                print(f"  material {mat_name!r}: no shader tree, left as a dependency")
                continue
            if material.node_tree.name in trees:
                # A node group named like the embedded tree would be clobbered
                # by the per-emission class-name override.
                raise RuntimeError(
                    f"A node group is named {material.node_tree.name!r}, which "
                    f"collides with material {mat_name!r}'s embedded tree — "
                    "rename that group to dump this library."
                )
            key = f"material:{mat_name}"
            trees[key] = material.node_tree
            id_deps[key] = _id_defaults(material.node_tree)
            material_trees[key] = mat_name

    # Sharing structure: which groups each root (asset or material tree)
    # transitively reaches.
    refs = {name: _direct_refs(tree) for name, tree in trees.items()}
    root_names = asset_names | set(material_trees)
    closures: dict[str, set[str]] = {}
    for root in root_names:
        seen: set[str] = set()
        stack = list(refs[root])
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(refs.get(name, ()))
        closures[root] = seen

    usage: dict[str, int] = {}
    for closure in closures.values():
        for name in closure - asset_names:
            usage[name] = usage.get(name, 0) + 1
    shared = {name for name, count in usage.items() if count >= 2}

    # Every class that lives in its own module (assets, materials and shared
    # helpers) is imported or referenced by name across files, so names are
    # assigned globally; helper groups used by one root stay embedded.
    # Material keys display as the material's name, not the embedded tree's.
    class_names = _assign_class_names({name: name for name in trees} | material_trees)
    external = asset_names | shared

    # Module paths from the output root for every non-embedded tree.
    modules: dict[str, str] = {}
    for tree_idname, dirname in _TREE_DIRS.items():
        dir_assets = [t.name for t in asset_trees if t.bl_idname == tree_idname]
        dir_shared = [n for n in shared if trees[n].bl_idname == tree_idname]
        modules.update(
            {n: f"{dirname}/{stem}" for n, stem in _assign_stems(dir_assets).items()}
        )
        modules.update(
            {
                n: f"{dirname}/_shared/{stem}"
                for n, stem in _assign_stems(dir_shared).items()
            }
        )
    material_stems = _assign_stems(list(material_trees.values()))
    for key, mat_name in material_trees.items():
        modules[key] = f"{_MATERIALS_DIR}/{material_stems[mat_name]}"

    def module_dependencies(root: str) -> dict[str, tuple[str, ...]]:
        """The datablocks the root's whole subtree references, sorted for a
        deterministic dump. Recorded on root modules only — shared groups'
        needs are repeated in every dependent root, and build unions them."""
        merged: dict[str, set[str]] = {}
        for name in {root} | closures[root]:
            for collection, ids in id_deps.get(name, {}).items():
                merged.setdefault(collection, set()).update(ids)
        return {coll: tuple(sorted(ids)) for coll, ids in merged.items()}

    # Merged typed API: every asset and shared class gets the typed interface,
    # and group calls to any of them use the typed parameter names.
    typed_groups = external if library_blend is not None else set()

    def write_module(key: str, module: str, *, kind: str) -> Path:
        group = trees[key]
        # Emitted here: the tree itself plus, for roots, its private helpers.
        # Sets mix tree keys and group names; for groups the two coincide.
        emitted = {key}
        if kind in ("asset", "material"):
            emitted |= closures[key] - external
        needed = set().union(*(refs[n] for n in emitted)) & (external - {key})
        import_lines = sorted(
            f"from {_relative_import(modules[n], module)} import {class_names[n]}"
            for n in needed
        )
        root_interface = None
        if library_blend is not None and kind in ("asset", "shared"):
            from ._codegen import interface_parts

            library_source = None
            if kind == "asset":
                module_dir = (output_dir / module).parent
                relpath = Path(os.path.relpath(library_blend, module_dir)).as_posix()
                library_source = f"PackageLibrary(__file__, {_fmt(relpath)})"
            root_interface, iface_imports = interface_parts(
                group, library_source=library_source, nodebpy_pkg=nodebpy_pkg
            )
            import_lines = iface_imports + import_lines
        # A material tree's key isn't its (read-only, non-unique) tree name,
        # so map the tree's actual name onto the key's class name for codegen.
        source = _render_group_module(
            group,
            kind=kind,
            class_name=class_names[key],
            import_lines=import_lines,
            class_names={**class_names, group.name: class_names[key]},
            external=external - {key},
            dependencies=(module_dependencies(key) if kind != "shared" else {}),
            material_name=material_trees.get(key),
            nodebpy_pkg=nodebpy_pkg,
            snapshot_positions=snapshot_positions,
            keep_reroutes=keep_reroutes,
            format=format,
            typed_groups=typed_groups,
            root_interface=root_interface,
        )
        path = output_dir / (module + ".py")
        path.parent.mkdir(parents=True, exist_ok=True)
        # LF regardless of platform: dumps are committed to git, and a
        # Windows dump must not diff against the same dump made elsewhere.
        path.write_text(source, encoding="utf-8", newline="\n")
        _ensure_init(output_dir)
        parent = path.parent
        while parent != output_dir:
            _ensure_init(parent)
            parent = parent.parent
        return path

    written: dict[str, Path] = {}
    for tree in asset_trees:
        written[tree.name] = write_module(tree.name, modules[tree.name], kind="asset")
    all_written = set(written.values())
    for name in sorted(shared):
        all_written.add(write_module(name, modules[name], kind="shared"))
    for key in sorted(material_trees):
        all_written.add(write_module(key, modules[key], kind="material"))
    if clean_stale:
        _remove_stale_modules(output_dir, all_written)

    if library_blend is not None:
        # Typed API: each tree directory re-exports its asset classes, so
        # ``from <pkg>.<tree_dir> import <Class>`` (or an aliased module
        # import) works like the old single-file API.
        for dirname in set(_TREE_DIRS.values()):
            exports = sorted(
                (modules[t.name].split("/")[1], class_names[t.name])
                for t in asset_trees
                if modules[t.name].startswith(f"{dirname}/")
            )
            if exports:
                _write_dir_exports(output_dir / dirname, exports)
    return written


def _source_files(source_dir: Path) -> list[Path]:
    """The dumped *root* modules (assets and materials) under ``source_dir``,
    in deterministic order.

    ``_``-prefixed files and directories (the ``_shared`` group modules) and
    ``__init__.py`` package markers are not root modules — shared groups are
    pulled in by the root modules' own imports."""
    return sorted(
        p
        for p in source_dir.rglob("*.py")
        if p.name != "__init__.py"
        and not any(part.startswith("_") for part in p.relative_to(source_dir).parts)
    )


def _import_source_modules(source_dir: Path, files: list[Path]) -> list:
    """Import the dumped modules under a throwaway package so their relative
    imports (shared groups, nested assets) resolve; returns the module per
    file, in order. The package is unique per call and unregistered afterwards
    so edited sources are never served from a stale module cache."""
    package = f"_nodebpy_asset_sources_{uuid.uuid4().hex[:8]}"
    spec = importlib.machinery.ModuleSpec(package, None, is_package=True)
    spec.submodule_search_locations = [str(source_dir)]
    sys.modules[package] = importlib.util.module_from_spec(spec)
    # No __pycache__ droppings in the (version-controlled) source tree.
    dont_write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        return [
            importlib.import_module(
                ".".join((package, *file.relative_to(source_dir).with_suffix("").parts))
            )
            for file in files
        ]
    finally:
        sys.dont_write_bytecode = dont_write_bytecode
        for key in [k for k in sys.modules if k.split(".")[0] == package]:
            del sys.modules[key]


def _resolve_dependencies(
    needed: dict[str, set[str]],
    resources: Path | None,
    on_missing: str,
) -> list:
    """Make the datablocks in ``needed`` available for the build.

    Resolution order per datablock: already present in the session, appended
    by name from the ``resources`` ``.blend``, or — with
    ``on_missing="drop"`` — a temporary placeholder the caller must delete
    before writing. Anything still missing raises with the full list.

    Returns the placeholder datablocks created (as ``(collection, id)``).
    """

    def missing_now() -> dict[str, set[str]]:
        return {
            coll: absent
            for coll, ids in needed.items()
            if (
                absent := {n for n in ids if getattr(bpy.data, coll, {}).get(n) is None}
            )
        }

    missing = missing_now()
    if missing and resources is not None:
        if not resources.is_file():
            raise FileNotFoundError(
                f"Resources library not found: {resources.resolve()}"
            )
        with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
            str(resources), link=False
        ) as (src, dst):
            for coll, ids in missing.items():
                available = set(getattr(src, coll, ()))
                setattr(dst, coll, sorted(ids & available))
        missing = missing_now()

    if not missing:
        return []
    if on_missing != "drop":
        listing = "; ".join(
            f"{coll}: {sorted(ids)}" for coll, ids in sorted(missing.items())
        )
        raise RuntimeError(
            f"Datablocks referenced by the sources are missing: {listing}. "
            "Either build in a session that already holds them, pass "
            "resources=<.blend> to append them by name, or pass "
            "on_missing='drop' to build with those defaults left empty."
        )

    placeholders = []
    for coll, ids in sorted(missing.items()):
        factory = _PLACEHOLDER_FACTORIES.get(coll)
        if factory is None:
            raise RuntimeError(
                f"Cannot placeholder missing {coll} {sorted(ids)} for "
                "on_missing='drop'; provide them via a resources .blend or "
                "the session instead."
            )
        for name in sorted(ids):
            placeholders.append((coll, factory(name)))
    return placeholders


def _build_material(material_cls, name: str):
    """Recreate the material ``name`` by running ``material_cls``'s
    ``_build_group`` recipe into its embedded shader tree; an existing
    same-named material is reused untouched ("in the presence" of the data)."""
    existing = bpy.data.materials.get(name)
    if existing is not None:
        return existing
    material = bpy.data.materials.new(name)
    assert material is not None
    if material.node_tree is None:  # pragma: no cover - pre-5.x Blender
        material.use_nodes = True
    tree = material.node_tree
    assert tree is not None
    tree.nodes.clear()
    builder = material_cls.__new__(material_cls)
    with TreeBuilder(tree) as wrapped:
        builder._build_group(wrapped)
    return material


def build_library(
    source_dir: str | Path,
    blend_path: str | Path,
    *,
    compress: bool = True,
    allow_existing: bool = False,
    resources: str | Path | None = None,
    on_missing: str = "error",
) -> list[str]:
    """Rebuild a ``.blend`` asset library from sources written by
    :func:`dump_library`.

    Imports every root module under ``source_dir`` (recursively; ``_shared``
    group modules are pulled in by the root modules' own imports), rebuilds
    each ``MATERIAL`` module's material, builds each ``ASSET`` class via
    ``create_group()``, re-marks the tree as an asset, applies the dumped
    ``ASSET_METADATA``/``TREE_PROPERTIES``/``MATERIAL_PROPERTIES``, and
    writes those trees and materials (plus their dependencies) to
    ``blend_path`` with ``bpy.data.libraries.write``. A
    ``blender_assets.cats.txt`` in ``source_dir`` is copied next to the
    ``.blend``.

    Datablocks the sources reference but cannot serialise (images, objects,
    …, recorded in each module's ``DATABLOCK_DEPENDENCIES``) resolve in
    order: already present in the session (build "in the presence" of the
    data — e.g. after opening a working file), appended by name from the
    ``resources`` ``.blend``, or — with ``on_missing="drop"`` — replaced by
    temporary placeholders deleted again before the write, leaving those
    socket defaults empty. The default ``on_missing="error"`` raises upfront,
    listing everything missing.

    The built trees stay in the current session afterwards. Because
    ``create_group()`` reuses an existing tree of the same name (that is what
    deduplicates groups shared between asset files), the session must not
    already hold node groups when the build starts — a stale same-named group
    would silently end up in the ``.blend``. This raises if any exist, unless
    ``allow_existing`` is passed. The CLI (``python -m nodebpy.assets build``)
    runs in a fresh session by construction.

    Returns
    -------
    list[str]
        The names of the asset node groups written to the ``.blend``.
    """
    source_dir = Path(source_dir)
    blend_path = Path(blend_path)
    files = _source_files(source_dir)
    if not files:
        raise FileNotFoundError(
            f"No asset sources (*.py) found under {source_dir.resolve()}"
        )
    if bpy.data.node_groups and not allow_existing:
        existing = sorted(g.name for g in bpy.data.node_groups)
        raise RuntimeError(
            f"The session already holds node groups {existing}; a same-named "
            "stale group would be reused and written into the library. Build "
            "from a fresh session (e.g. python -m nodebpy.assets build), or "
            "pass allow_existing=True to override."
        )

    asset_modules: list[tuple[Path, object]] = []
    material_modules: list[tuple[Path, object]] = []
    for file, module in zip(
        files, _import_source_modules(source_dir, files), strict=True
    ):
        if getattr(module, "MATERIAL", None) is not None:
            material_modules.append((file, module))
        elif getattr(module, "ASSET", None) is not None:
            asset_modules.append((file, module))
        else:
            raise ValueError(
                f"{file} defines neither ASSET nor MATERIAL — not a dumped module?"
            )

    # A .blend keys node groups by name across every tree type, so two dumped
    # assets sharing a display name (e.g. a geometry and a compositor "Combine
    # Spherical", dumped from separate libraries into one source dir) cannot
    # coexist in one rebuilt library — the second create_group would abort the
    # build mid-way on the name/type clash. Fail upfront with the way out.
    by_name: dict[str, list[Path]] = {}
    for file, module in asset_modules:
        name = getattr(module.ASSET, "_name", None)  # ty: ignore[unresolved-attribute]
        if isinstance(name, str):
            by_name.setdefault(name, []).append(file)
    if duplicates := {n: fs for n, fs in by_name.items() if len(fs) > 1}:
        listing = "; ".join(
            f"{name!r} in {[str(f.relative_to(source_dir)) for f in files]}"
            for name, files in sorted(duplicates.items())
        )
        raise ValueError(
            f"Duplicate asset names across sources: {listing}. A .blend holds "
            "one node group per name regardless of tree type — build each "
            "tree directory into its own .blend (e.g. "
            "build_library(source_dir / 'geometry', ...))."
        )

    # Resolve non-serialisable datablocks before anything builds. Materials
    # the dump code-generated are provided by their own modules, not looked
    # up, so they never count as missing.
    provided_materials = {
        getattr(module, "MATERIAL_NAME", None) or module.MATERIAL._name  # ty: ignore[unresolved-attribute]
        for _, module in material_modules
    }
    needed: dict[str, set[str]] = {}
    for _, module in asset_modules + material_modules:
        dependencies = getattr(module, "DATABLOCK_DEPENDENCIES", {})
        assert isinstance(dependencies, dict)
        for coll, ids in dependencies.items():
            needed.setdefault(coll, set()).update(ids)
    if "materials" in needed:
        needed["materials"] -= provided_materials
    placeholders = _resolve_dependencies(
        {c: ids for c, ids in needed.items() if ids},
        Path(resources) if resources is not None else None,
        on_missing,
    )

    # Materials first: asset trees look them up by name while building.
    built_materials = []
    for file, module in material_modules:
        material_cls = module.MATERIAL  # ty: ignore[unresolved-attribute]
        if not (
            isinstance(material_cls, type)
            and issubclass(material_cls, NodeGroupBuilder)
        ):
            raise TypeError(f"{file}: MATERIAL is not a node-group class")
        name = getattr(module, "MATERIAL_NAME", None) or material_cls._name
        # The material recipe may instantiate typed-API asset classes, which
        # must build from their _build_group source, not append.
        with build_from_source():
            material = _build_material(material_cls, name)
        for key, value in getattr(module, "MATERIAL_PROPERTIES", {}).items():
            try:
                setattr(material, key, value)
            except AttributeError:
                print(f"  {name}: skipping read-only material property {key!r}")
        built_materials.append(material)

    trees = []
    for file, module in asset_modules:
        asset_cls = module.ASSET  # ty: ignore[unresolved-attribute]
        if not (
            isinstance(asset_cls, type) and issubclass(asset_cls, NodeGroupBuilder)
        ):
            raise TypeError(f"{file}: ASSET is not a node-group class: {asset_cls!r}")
        # Merged typed-API classes are Asset*Groups that would *append* their
        # own .blend; building from source is the whole point here.
        with build_from_source():
            tree = asset_cls.create_group()
        if tree.asset_data is None:
            tree.asset_mark()
        asset_data = tree.asset_data
        assert asset_data is not None
        metadata = getattr(module, "ASSET_METADATA", {})
        assert isinstance(metadata, dict)
        for field in _METADATA_FIELDS:
            if field in metadata:
                try:
                    setattr(asset_data, field, metadata[field])
                except AttributeError:  # pragma: no cover - other Blender versions
                    # Read-only in this Blender version (as catalog_simple_name
                    # was) — the value is derived, not lost; keep building.
                    print(f"  {tree.name}: skipping read-only asset field {field!r}")
        existing_tags = {tag.name for tag in asset_data.tags}
        for tag in metadata.get("tags", ()):
            if tag not in existing_tags:
                asset_data.tags.new(tag)
        properties = getattr(module, "TREE_PROPERTIES", {})
        assert isinstance(properties, dict)
        for key, value in properties.items():
            setattr(tree, key, value)
        trees.append(tree)

    # Placeholders satisfied the lookups during the build; deleting them nulls
    # the referencing socket defaults, which is exactly what "drop" means.
    for coll, datablock in placeholders:
        getattr(bpy.data, coll).remove(datablock)

    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(
        str(blend_path),
        set(trees) | set(built_materials),
        fake_user=True,
        compress=compress,
    )
    _copy_catalog_file(source_dir, blend_path.parent)
    return [tree.name for tree in trees]


def main(argv: list[str] | None = None) -> None:  # pragma: no cover - CLI wrapper
    """CLI entry point for the ``dump`` and ``build`` subcommands."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m nodebpy.assets",
        description="Round-trip a .blend asset library through Python source.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    dump = sub.add_parser(
        "dump",
        help="Dump every asset in a .blend to per-asset .py files.",
        description=(
            "Dump every node-group asset in a .blend to Python source files: "
            "one .py per asset under <output>/geometry, <output>/shader and "
            "<output>/compositor, holding the asset's class, an ASSET marker "
            "and its metadata. Each group class is defined exactly once — "
            "helpers used by a single asset are embedded in its module, "
            "groups nested by several assets get their own module under "
            "_shared/, and nested assets are imported from their own modules. "
            "Check these files into version control as the source of truth "
            "and rebuild the .blend from them with the 'build' subcommand. A "
            "blender_assets.cats.txt next to the .blend is copied along, so "
            "catalog assignments survive the round trip."
        ),
    )
    dump.add_argument("blend", type=Path, help="The .blend asset library to dump.")
    dump.add_argument("output", type=Path, help="Directory to write the .py files to.")
    dump.add_argument(
        "--names", nargs="+", help="Only dump these asset names (default: all)."
    )
    dump.add_argument(
        "--nodebpy-pkg",
        default="nodebpy",
        help=(
            "Import anchor for nodebpy in the dumped sources. Defaults to the "
            "absolute 'nodebpy'; when nodebpy is vendored inside another "
            "package, pass the path that reaches it relative to the dumped "
            "modules — e.g. '..lib.nodebpy'."
        ),
    )
    dump.add_argument(
        "--snapshot-positions",
        action="store_true",
        help="Preserve authored node positions in the dumped sources.",
    )
    dump.add_argument(
        "--keep-reroutes",
        action="store_true",
        help="Preserve reroute nodes instead of collapsing them.",
    )
    dump.add_argument(
        "--typed-api",
        action="store_true",
        help=(
            "Merge the typed asset API into the dumped classes: numpydoc "
            "docstrings, _Inputs/_Outputs accessors and a typed __init__, "
            "with each asset class appending the .blend at runtime "
            "(PackageLibrary) while its _build_group stays the source of "
            "truth for rebuilding it. Tree directories get __init__.py "
            "re-exports of their asset classes."
        ),
    )
    dump.add_argument(
        "--no-materials",
        dest="materials",
        action="store_false",
        help=(
            "Skip code-generating referenced materials into materials/ "
            "modules; record them only as DATABLOCK_DEPENDENCIES, to be "
            "resolved at build time (session / --resources / --drop-missing)."
        ),
    )

    build = sub.add_parser(
        "build",
        help="Rebuild the .blend asset library from dumped .py files.",
        description=(
            "Rebuild a .blend asset library from sources written by the "
            "'dump' subcommand: every .py under <source> is executed, its "
            "ASSET class is built, re-marked as an asset with its dumped "
            "metadata, and exactly those node groups (plus dependencies) are "
            "written to the .blend. Asset previews are not round-tripped; "
            "regenerate them in Blender if needed. A blender_assets.cats.txt "
            "in <source> is copied next to the built .blend."
        ),
    )
    build.add_argument("source", type=Path, help="Directory of dumped .py files.")
    build.add_argument("blend", type=Path, help="The .blend file to write.")
    build.add_argument(
        "--allow-existing",
        action="store_true",
        help=(
            "Build even if the session already holds node groups. Same-named "
            "existing groups are reused rather than rebuilt from source, so "
            "only pass this when you know they are not stale."
        ),
    )
    build.add_argument(
        "--no-compress",
        dest="compress",
        action="store_false",
        help="Write the .blend uncompressed (compressed by default).",
    )
    build.add_argument(
        "--resources",
        type=Path,
        help=(
            "A .blend to append missing datablock dependencies (images, "
            "objects, …) from, by name, before building."
        ),
    )
    build.add_argument(
        "--drop-missing",
        dest="on_missing",
        action="store_const",
        const="drop",
        default="error",
        help=(
            "Build even when datablock dependencies are missing: temporary "
            "placeholders satisfy the lookups and are deleted before the "
            ".blend is written, leaving those socket defaults empty. The "
            "default is to error upfront, listing everything missing."
        ),
    )

    args = parser.parse_args(argv)
    if args.command == "dump":
        written = dump_library(
            args.blend,
            args.output,
            names=set(args.names) if args.names else None,
            nodebpy_pkg=args.nodebpy_pkg,
            snapshot_positions=args.snapshot_positions,
            keep_reroutes=args.keep_reroutes,
            materials=args.materials,
            typed_api=args.typed_api,
        )
        for name, path in written.items():
            print(f"  {name}: {path}")
        print(f"Dumped {len(written)} assets to {args.output}")
    else:
        names = build_library(
            args.source,
            args.blend,
            compress=args.compress,
            allow_existing=args.allow_existing,
            resources=args.resources,
            on_missing=args.on_missing,
        )
        print(f"Built {args.blend} with {len(names)} assets: {', '.join(names)}")


if __name__ == "__main__":  # pragma: no cover
    main()
