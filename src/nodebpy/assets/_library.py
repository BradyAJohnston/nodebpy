"""Round-trip a ``.blend`` asset library through Python source.

:func:`dump_library` writes every node-group asset in a ``.blend`` to its own
``.py`` file (via :func:`nodebpy.export.to_python` in ``class`` mode), and
:func:`build_library` rebuilds the ``.blend`` from those files. The intent is
that only the ``.py`` files are checked into version control — the ``.blend``
is a build artifact (rebuilt for shipping, or for tweaking node trees by hand
in Blender before dumping them back out).

Each dumped file is self-contained: it holds one ``Custom*Group`` class per
node group the asset (transitively) uses, an ``ASSET`` name pointing at the
asset's own class, and — when present — an ``ASSET_METADATA`` dict (catalog id,
description, author, tags, …) and a ``TREE_PROPERTIES`` dict (non-default tree
flags such as ``is_modifier``/``is_tool``). Groups shared by several assets are
repeated in each file; rebuilding deduplicates them by name, since
:meth:`~nodebpy.builder.NodeGroupBuilder.create_group` reuses an existing tree.

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

import re
import shutil
from pathlib import Path

import bpy

from ..builder import NodeGroupBuilder
from ..builder._utils import normalize_name
from ..export.codegen import _format_with_ruff, to_python

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


def _render_asset_module(
    group,
    *,
    nodebpy_pkg: str,
    snapshot_positions: bool,
    keep_reroutes: bool,
    format: bool,
) -> str:
    """The full source for one asset's ``.py`` file: generated classes, the
    ``ASSET`` marker and the metadata footers."""
    code = to_python(
        group,
        top_level="class",
        nodebpy_pkg=nodebpy_pkg,
        snapshot_positions=snapshot_positions,
        keep_reroutes=keep_reroutes,
        format=False,
    )
    # In class mode the top-level tree's class is emitted last (nested groups
    # are registered depth-first), so the final class is the asset's own.
    class_name = re.findall(r"^class (\w+)\(", code, flags=re.MULTILINE)[-1]

    # Deliberately no source filename/timestamp in the header: a dump must be
    # byte-identical across a no-op round-trip so it leaves no VCS diff.
    header = [
        (
            f"# Node-group asset {group.name!r} ({group.bl_idname}),"
            " dumped by nodebpy.assets.dump_library."
        ),
        (
            "# Rebuild the library with nodebpy.assets.build_library"
            " (python -m nodebpy.assets build)."
        ),
        "",
    ]
    footer = ["", "", f"ASSET = {class_name}"]
    meta = _asset_metadata(group)
    if meta:
        footer += [""] + _dict_lines("ASSET_METADATA", meta)
    props = _tree_properties(group)
    if props:
        footer += [""] + _dict_lines("TREE_PROPERTIES", props)

    source = "\n".join(header) + code + "\n".join(footer) + "\n"
    return _format_with_ruff(source) if format else source


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

    Each asset becomes one self-contained ``.py`` file under
    ``<output_dir>/<tree>/`` (``geometry``/``shader``/``compositor``), holding
    ``Custom*Group`` classes for the asset and every group it nests, an
    ``ASSET`` marker naming the asset's class, and metadata footers.
    :func:`build_library` rebuilds the ``.blend`` from these files. A
    ``blender_assets.cats.txt`` next to the ``.blend`` is copied into
    ``output_dir`` so catalog assignments travel with the sources.

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

    written: dict[str, Path] = {}
    used_paths: set[Path] = set()
    for name in wanted:
        before = set(bpy.data.node_groups.keys())
        # Append one asset at a time so a same-named pair in different tree
        # types (which .get() can't distinguish) never collides mid-dump.
        with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
            str(blend_path), link=False, assets_only=True
        ) as (src, dst):
            dst.node_groups = [name]
        appended = [g for g in bpy.data.node_groups if g.name not in before]
        try:
            renamed = sorted(
                g.name
                for g in appended
                if (m := re.fullmatch(r"(.*)\.\d{3}", g.name)) and m[1] in before
            )
            if renamed:
                raise RuntimeError(
                    f"Appending {name!r} renamed dependency groups {renamed} "
                    "because same-named groups already exist in this session — "
                    "dump from a fresh session."
                )
            group = dst.node_groups[0]
            subdir = _TREE_DIRS.get(group.bl_idname)
            if subdir is None:
                print(f"  skipping {name!r}: unsupported tree type {group.bl_idname}")
                continue
            path = output_dir / subdir / f"{normalize_name(name)}.py"
            n = 1
            while path in used_paths:
                n += 1
                path = path.with_name(f"{normalize_name(name)}_{n}.py")
            used_paths.add(path)
            source = _render_asset_module(
                group,
                nodebpy_pkg=nodebpy_pkg,
                snapshot_positions=snapshot_positions,
                keep_reroutes=keep_reroutes,
                format=format,
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
            written[name] = path
        finally:
            for g in appended:
                bpy.data.node_groups.remove(g)

    _copy_catalog_file(blend_path.parent, output_dir)
    return written


def _source_files(source_dir: Path) -> list[Path]:
    """The dumped asset modules under ``source_dir``, in deterministic order."""
    return sorted(
        p
        for p in source_dir.rglob("*.py")
        if not p.name.startswith("_") and p.name != "__init__.py"
    )


def build_library(
    source_dir: str | Path,
    blend_path: str | Path,
    *,
    compress: bool = True,
    allow_existing: bool = False,
) -> list[str]:
    """Rebuild a ``.blend`` asset library from sources written by
    :func:`dump_library`.

    Executes every ``.py`` under ``source_dir`` (recursively, skipping
    ``_``-prefixed files), builds each file's ``ASSET`` class via
    ``create_group()``, re-marks the tree as an asset, applies the dumped
    ``ASSET_METADATA``/``TREE_PROPERTIES``, and writes exactly those trees
    (plus their dependencies) to ``blend_path`` with
    ``bpy.data.libraries.write``. A ``blender_assets.cats.txt`` in
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
    for file in files:
        namespace: dict[str, object] = {"__file__": str(file), "__name__": file.stem}
        # Executing the user's own checked-in asset sources is the point here.
        exec(  # noqa: S102
            compile(file.read_text(encoding="utf-8"), str(file), "exec"), namespace
        )
        asset_cls = namespace.get("ASSET")
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
        metadata = namespace.get("ASSET_METADATA", {})
        assert isinstance(metadata, dict)
        for field in _METADATA_FIELDS:
            if field in metadata:
                setattr(asset_data, field, metadata[field])
        existing_tags = {tag.name for tag in asset_data.tags}
        for tag in metadata.get("tags", ()):
            if tag not in existing_tags:
                asset_data.tags.new(tag)
        properties = namespace.get("TREE_PROPERTIES", {})
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
        "dump", help="Dump every asset in a .blend to per-asset .py files."
    )
    dump.add_argument("blend", type=Path, help="The .blend asset library to dump.")
    dump.add_argument("output", type=Path, help="Directory to write the .py files to.")
    dump.add_argument(
        "--names", nargs="+", help="Only dump these asset names (default: all)."
    )
    dump.add_argument("--nodebpy-pkg", default="nodebpy")
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
        "build", help="Rebuild the .blend asset library from dumped .py files."
    )
    build.add_argument("source", type=Path, help="Directory of dumped .py files.")
    build.add_argument("blend", type=Path, help="The .blend file to write.")
    build.add_argument(
        "--allow-existing",
        action="store_true",
        help="Build even if the session already holds node groups.",
    )
    build.add_argument("--no-compress", dest="compress", action="store_false")

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
