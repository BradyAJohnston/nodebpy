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
  description, author, tags, …) and a ``TREE_PROPERTIES`` dict (non-default
  tree flags such as ``is_modifier``/``is_tool``);
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
import re
import shutil
import sys
import uuid
from pathlib import Path

import bpy

from ..builder import NodeGroupBuilder
from ..builder._utils import normalize_name
from ..export.codegen import _class_name, _format_with_ruff, to_python

# Tree-type bl_idname → subdirectory the dumped modules are written into.
# Asset names repeat across editors (a geometry and a compositor "Combine
# Spherical" both exist), so splitting keeps filenames collision-free.
_TREE_DIRS: dict[str, str] = {
    "GeometryNodeTree": "geometry",
    "ShaderNodeTree": "shader",
    "CompositorNodeTree": "compositor",
}

# Asset-metadata fields that round-trip through ASSET_METADATA (plus tags,
# handled separately as a collection).
_METADATA_FIELDS = (
    "description",
    "author",
    "copyright",
    "license",
    "catalog_id",
    "catalog_simple_name",
)

# An unassigned catalog — not worth dumping.
_NIL_CATALOG = "00000000-0000-0000-0000-000000000000"

# Tree-level properties that affect how an asset behaves (modifier/tool flags,
# tool modes and object types) but aren't part of the node graph, so codegen
# doesn't capture them. Only values differing from a fresh tree's defaults are
# dumped; properties a Blender version doesn't have are skipped.
_TREE_PROP_CANDIDATES = (
    "description",
    "is_modifier",
    "is_tool",
    "is_mode_object",
    "is_mode_edit",
    "is_mode_sculpt",
    "use_wait_for_click",
    "is_type_mesh",
    "is_type_curve",
    "is_type_pointcloud",
    "is_type_grease_pencil",
)

#: Catalog definition file that Blender keeps next to an asset library.
CATALOG_FILENAME = "blender_assets.cats.txt"


def _asset_metadata(group) -> dict[str, object]:
    """The dumpable asset metadata of ``group``, non-empty fields only."""
    asset_data = group.asset_data
    if asset_data is None:
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


def _tree_properties(group) -> dict[str, object]:
    """Tree-level properties of ``group`` that differ from a fresh tree's
    defaults, probed against a throwaway tree of the same type."""
    probe = bpy.data.node_groups.new("_nodebpy_dump_probe", group.bl_idname)
    assert probe is not None
    try:
        props: dict[str, object] = {}
        for name in _TREE_PROP_CANDIDATES:
            if not hasattr(probe, name):
                continue
            value = getattr(group, name)
            if value != getattr(probe, name):
                props[name] = value
        return props
    finally:
        bpy.data.node_groups.remove(probe)


def _dict_lines(name: str, data: dict[str, object]) -> list[str]:
    lines = [f"{name} = {{"]
    lines += [f"    {key!r}: {value!r}," for key, value in data.items()]
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


def _assign_class_names(group_names: list[str]) -> dict[str, str]:
    """A globally unique PascalCase class name per group, assigned in sorted
    order so the result is deterministic across dumps. Global uniqueness
    matters because the classes span modules that import each other — two
    same-named classes would collide in the importing module's namespace."""
    class_names: dict[str, str] = {}
    used: set[str] = set()
    for group_name in sorted(group_names):
        base = _class_name(group_name)
        name, n = base, 1
        while name in used:
            n += 1
            name = f"{base}{n}"
        used.add(name)
        class_names[group_name] = name
    return class_names


def _assign_stems(group_names: list[str]) -> dict[str, str]:
    """A unique module filename stem per group within one directory, assigned
    in sorted order so the result is deterministic across dumps."""
    stems: dict[str, str] = {}
    used: set[str] = set()
    for group_name in sorted(group_names):
        base = normalize_name(group_name)
        stem, n = base, 1
        while stem in used:
            n += 1
            stem = f"{base}_{n}"
        used.add(stem)
        stems[group_name] = stem
    return stems


def _relative_import(target_module: str, from_module: str) -> str:
    """The relative module reference from one dumped module to another, both
    given as paths relative to the tree directory (``"scale_up"`` or
    ``"_shared.utils"``)."""
    if from_module.startswith("_shared."):
        if target_module.startswith("_shared."):
            return "." + target_module.removeprefix("_shared.")
        return ".." + target_module
    return "." + target_module


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
    asset: bool,
    import_lines: list[str],
    class_names: dict[str, str],
    external: set[str],
    nodebpy_pkg: str,
    snapshot_positions: bool,
    keep_reroutes: bool,
    format: bool,
) -> str:
    """The full source for one dumped ``.py`` module: the group's class (plus
    any embedded helper classes), imports for externally defined classes, and
    — for assets — the ``ASSET`` marker and metadata footers."""
    code = to_python(
        group,
        top_level="class",
        nodebpy_pkg=nodebpy_pkg,
        snapshot_positions=snapshot_positions,
        keep_reroutes=keep_reroutes,
        format=False,
        group_class_names=class_names,
        external_groups=external,
    )
    code = _insert_imports(code, import_lines)

    # Deliberately no source filename/timestamp in the header: a dump must be
    # byte-identical across a no-op round-trip so it leaves no VCS diff.
    kind = "Node-group asset" if asset else "Node group"
    header = [
        (
            f"# {kind} {group.name!r} ({group.bl_idname}),"
            " dumped by nodebpy.assets.dump_library."
        ),
        (
            "# Rebuild the library with nodebpy.assets.build_library"
            " (python -m nodebpy.assets build)."
        ),
    ]
    if not asset:
        header.append(
            "# Shared by several assets, which import it; not an asset itself."
        )
    header.append("")

    footer: list[str] = []
    if asset:
        footer = ["", "", f"ASSET = {class_names[group.name]}"]
        meta = _asset_metadata(group)
        if meta:
            footer += [""] + _dict_lines("ASSET_METADATA", meta)
        props = _tree_properties(group)
        if props:
            footer += [""] + _dict_lines("TREE_PROPERTIES", props)

    source = "\n".join(header) + code + "\n".join(footer) + "\n"
    return _format_with_ruff(source) if format else source


_INIT_CONTENT = "# Package marker for nodebpy-dumped asset sources.\n"


def _ensure_init(directory: Path) -> None:
    """Make ``directory`` a package so the dumped relative imports resolve
    when the sources are imported as part of a larger package; an existing
    ``__init__.py`` (e.g. hand-written) is left untouched."""
    init = directory / "__init__.py"
    if not init.exists():
        init.write_text(_INIT_CONTENT, encoding="utf-8")


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
    format: bool = True,
) -> dict[str, Path]:
    """Dump every node-group asset in ``blend_path`` to Python source files.

    Each asset becomes one ``.py`` module under ``<output_dir>/<tree>/``
    (``geometry``/``shader``/``compositor``) with an ``ASSET`` marker and
    metadata footers. Every group class is defined exactly once: helper groups
    used by a single asset are embedded in that asset's module, groups nested
    by several assets get their own module under ``<tree>/_shared/``, and an
    asset nested inside other assets keeps its class in its own module — all
    referenced via relative imports (``__init__.py`` package markers are
    written so the imports resolve). :func:`build_library` rebuilds the
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
    format:
        Run the generated sources through ``ruff format`` when available.

    Returns
    -------
    dict[str, Path]
        Mapping of asset name to the file it was written to.
    """
    blend_path = Path(blend_path)
    output_dir = Path(output_dir)
    if not blend_path.is_file():
        raise FileNotFoundError(f"Asset library not found: {blend_path}")

    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(blend_path), link=False, assets_only=True
    ) as (src, _):
        available = list(src.node_groups)
    wanted = [n for n in available if names is None or n in names]
    if names is not None and (missing := names - set(wanted)):
        raise KeyError(f"Assets not found in {blend_path}: {sorted(missing)}")

    clashes = sorted(n for n in wanted if n in bpy.data.node_groups)
    if clashes:
        raise RuntimeError(
            f"Node groups already exist in this session: {clashes}. Appending "
            "would rename them and corrupt the dumped sources — dump from a "
            "fresh session (e.g. python -m nodebpy.assets dump)."
        )

    # Append every wanted asset in one load, so groups shared between assets
    # (including assets nested in other assets) arrive as single trees and the
    # sharing structure can be read off the session directly.
    before = set(bpy.data.node_groups.keys())
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(blend_path), link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = list(wanted)
    appended = [g for g in bpy.data.node_groups if g.name not in before]
    try:
        renamed = sorted(
            g.name
            for g in appended
            if (m := re.fullmatch(r"(.*)\.\d{3}", g.name)) and m[1] in before
        )
        if renamed:
            raise RuntimeError(
                f"Appending renamed dependency groups {renamed} because "
                "same-named groups already exist in this session — dump from "
                "a fresh session."
            )
        written = _dump_appended(
            list(dst.node_groups),
            appended,
            output_dir,
            nodebpy_pkg=nodebpy_pkg,
            snapshot_positions=snapshot_positions,
            keep_reroutes=keep_reroutes,
            format=format,
        )
    finally:
        for g in appended:
            bpy.data.node_groups.remove(g)

    _copy_catalog_file(blend_path.parent, output_dir)
    return written


def _dump_appended(
    asset_trees: list,
    appended: list,
    output_dir: Path,
    *,
    nodebpy_pkg: str,
    snapshot_positions: bool,
    keep_reroutes: bool,
    format: bool,
) -> dict[str, Path]:
    """Partition the appended groups into modules and write them.

    ``asset_trees`` are the trees dumped as assets; ``appended`` is every
    group the load brought in (the assets plus all their dependencies).
    """
    # Unsupported tree types (e.g. texture trees) can't be code-generated;
    # skip those assets — their private dependencies drop out with them.
    unsupported = [t for t in asset_trees if t.bl_idname not in _TREE_DIRS]
    for tree in unsupported:
        print(f"  skipping {tree.name!r}: unsupported tree type {tree.bl_idname}")
    asset_trees = [t for t in asset_trees if t.bl_idname in _TREE_DIRS]
    asset_names = {t.name for t in asset_trees}
    trees = {g.name: g for g in appended}

    # Sharing structure: which groups each asset (transitively) reaches.
    refs = {g.name: _direct_refs(g) for g in appended}
    closures: dict[str, set[str]] = {}
    for tree in asset_trees:
        seen: set[str] = set()
        stack = list(refs[tree.name])
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(refs.get(name, ()))
        closures[tree.name] = seen

    usage: dict[str, int] = {}
    for closure in closures.values():
        for name in closure - asset_names:
            usage[name] = usage.get(name, 0) + 1
    shared = {name for name, count in usage.items() if count >= 2}

    # Every class that lives in its own module (assets and shared helpers) is
    # imported by name across files, so names are assigned globally; helper
    # groups used by one asset stay embedded in that asset's module.
    class_names = _assign_class_names(list(trees))
    external = asset_names | shared

    # Module paths (relative to the tree directory) for every non-embedded
    # group, per tree type so filenames never collide across editors.
    modules: dict[str, str] = {}
    for tree_idname in _TREE_DIRS:
        dir_assets = [t.name for t in asset_trees if t.bl_idname == tree_idname]
        dir_shared = [n for n in shared if trees[n].bl_idname == tree_idname]
        modules.update(_assign_stems(dir_assets))
        modules.update(
            {n: f"_shared.{stem}" for n, stem in _assign_stems(dir_shared).items()}
        )

    def write_module(group, module: str, *, asset: bool) -> Path:
        # Emitted here: the group itself plus, for assets, its private helpers.
        emitted = {group.name}
        if asset:
            emitted |= closures[group.name] - external
        needed = set().union(*(refs[n] for n in emitted)) & (external - {group.name})
        import_lines = sorted(
            f"from {_relative_import(modules[n], module)} import {class_names[n]}"
            for n in needed
        )
        source = _render_group_module(
            group,
            asset=asset,
            import_lines=import_lines,
            class_names=class_names,
            external=external - {group.name},
            nodebpy_pkg=nodebpy_pkg,
            snapshot_positions=snapshot_positions,
            keep_reroutes=keep_reroutes,
            format=format,
        )
        subdir = output_dir / _TREE_DIRS[group.bl_idname]
        path = subdir / (module.replace(".", "/") + ".py")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
        _ensure_init(output_dir)
        _ensure_init(subdir)
        if path.parent != subdir:
            _ensure_init(path.parent)
        return path

    written: dict[str, Path] = {}
    for tree in asset_trees:
        written[tree.name] = write_module(tree, modules[tree.name], asset=True)
    for name in sorted(shared):
        write_module(trees[name], modules[name], asset=False)
    return written


def _source_files(source_dir: Path) -> list[Path]:
    """The dumped *asset* modules under ``source_dir``, in deterministic order.

    ``_``-prefixed files and directories (the ``_shared`` group modules) and
    ``__init__.py`` package markers are not asset modules — shared groups are
    pulled in by the asset modules' own imports."""
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
    try:
        return [
            importlib.import_module(
                ".".join((package, *file.relative_to(source_dir).with_suffix("").parts))
            )
            for file in files
        ]
    finally:
        for key in [k for k in sys.modules if k.split(".")[0] == package]:
            del sys.modules[key]


def build_library(
    source_dir: str | Path,
    blend_path: str | Path,
    *,
    compress: bool = True,
    allow_existing: bool = False,
) -> list[str]:
    """Rebuild a ``.blend`` asset library from sources written by
    :func:`dump_library`.

    Imports every asset module under ``source_dir`` (recursively; ``_shared``
    group modules are pulled in by the asset modules' own imports), builds
    each module's ``ASSET`` class via ``create_group()``, re-marks the tree as
    an asset, applies the dumped ``ASSET_METADATA``/``TREE_PROPERTIES``, and
    writes exactly those trees (plus their dependencies) to ``blend_path``
    with ``bpy.data.libraries.write``. A ``blender_assets.cats.txt`` in
    ``source_dir`` is copied next to the ``.blend``.

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
        raise FileNotFoundError(f"No asset sources (*.py) found under {source_dir}")
    if bpy.data.node_groups and not allow_existing:
        existing = sorted(g.name for g in bpy.data.node_groups)
        raise RuntimeError(
            f"The session already holds node groups {existing}; a same-named "
            "stale group would be reused and written into the library. Build "
            "from a fresh session (e.g. python -m nodebpy.assets build), or "
            "pass allow_existing=True to override."
        )

    trees = []
    for file, module in zip(
        files, _import_source_modules(source_dir, files), strict=True
    ):
        asset_cls = getattr(module, "ASSET", None)
        if asset_cls is None:
            raise ValueError(f"{file} defines no ASSET — not a dumped asset module?")
        if not (
            isinstance(asset_cls, type) and issubclass(asset_cls, NodeGroupBuilder)
        ):
            raise TypeError(f"{file}: ASSET is not a node-group class: {asset_cls!r}")
        tree = asset_cls.create_group()
        if tree.asset_data is None:
            tree.asset_mark()
        asset_data = tree.asset_data
        assert asset_data is not None
        metadata = getattr(module, "ASSET_METADATA", {})
        assert isinstance(metadata, dict)
        for field in _METADATA_FIELDS:
            if field in metadata:
                setattr(asset_data, field, metadata[field])
        existing_tags = {tag.name for tag in asset_data.tags}
        for tag in metadata.get("tags", ()):
            if tag not in existing_tags:
                asset_data.tags.new(tag)
        properties = getattr(module, "TREE_PROPERTIES", {})
        assert isinstance(properties, dict)
        for key, value in properties.items():
            setattr(tree, key, value)
        trees.append(tree)

    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.data.libraries.write(
        str(blend_path), set(trees), fake_user=True, compress=compress
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

    args = parser.parse_args(argv)
    if args.command == "dump":
        written = dump_library(
            args.blend,
            args.output,
            names=set(args.names) if args.names else None,
            nodebpy_pkg=args.nodebpy_pkg,
            snapshot_positions=args.snapshot_positions,
            keep_reroutes=args.keep_reroutes,
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
        )
        print(f"Built {args.blend} with {len(names)} assets: {', '.join(names)}")


if __name__ == "__main__":  # pragma: no cover
    main()
