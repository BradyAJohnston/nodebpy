"""Command-line entry point for nodebpy (``nodebpy ...``).

Two subcommands bridge between Blender node trees and nodebpy Python code:

* ``nodebpy export BLEND`` opens a ``.blend`` and converts its node groups to a
  single Python module of ``Custom*Group`` builder classes (the inverse of
  ``build``). Flags map onto :func:`nodebpy.export.to_python`.
* ``nodebpy build PY ...`` imports those modules, builds each
  :class:`~nodebpy.builder.NodeGroupBuilder` subclass into a fresh ``.blend``,
  marks the groups as assets, and saves the file.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import sys
from pathlib import Path

from .builder import NodeGroupBuilder
from .export import to_python


def _load_blend(path: Path) -> None:
    """Open ``path`` as the active Blender file (replaces the current session)."""
    import bpy

    if not path.exists():
        raise FileNotFoundError(f"Blend file not found: {path}")
    bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))


def _merge_modules(codes: list[str]) -> str:
    """Merge several single-class ``to_python`` modules into one.

    Each input is an unformatted module: contiguous ``from``/``import`` lines,
    then the class block. Imports are unioned per module path; class blocks are
    concatenated. Formatting is left to the caller.
    """
    imports: dict[str, list[str]] = {}
    plain: list[str] = []
    bodies: list[str] = []
    for code in codes:
        body_lines: list[str] = []
        for line in code.splitlines():
            if line.startswith("from "):
                module, _, names = line[len("from ") :].partition(" import ")
                seen = imports.setdefault(module, [])
                for name in names.split(", "):
                    if name not in seen:
                        seen.append(name)
            elif line.startswith("import "):
                if line not in plain:
                    plain.append(line)
            else:
                body_lines.append(line)
        bodies.append("\n".join(body_lines).strip())

    header = plain + [
        f"from {module} import " + ", ".join(names) for module, names in imports.items()
    ]
    return "\n".join(header) + "\n\n\n" + "\n\n\n".join(bodies) + "\n"


def _export(args: argparse.Namespace) -> None:
    import bpy

    _load_blend(args.blend)
    groups = list(bpy.data.node_groups)
    if args.name:
        wanted = set(args.name)
        groups = [g for g in groups if g.name in wanted]
        missing = wanted - {g.name for g in groups}
        if missing:
            raise SystemExit(
                f"Node group(s) not found in {args.blend}: {sorted(missing)}"
            )
    if not groups:
        raise SystemExit(f"No node groups to export in {args.blend}")

    codes = [
        to_python(
            group,
            snapshot_positions=args.snapshot_positions,
            keep_reroutes=args.keep_reroutes,
            min_chain_length=args.min_chain_length,
            strict=not args.no_strict,
            top_level="class",
            format=False,
            nodebpy_pkg=args.nodebpy_pkg,
        )
        for group in groups
    ]
    module = _merge_modules(codes)
    if not args.no_format:
        module = _format(module)

    if args.output is None:
        sys.stdout.write(module)
    else:
        args.output.write_text(module)
        print(f"Wrote {len(groups)} group(s) to {args.output}")


def _format(code: str) -> str:
    """Run ruff format over generated source, returning it unchanged on failure."""
    import subprocess

    result = subprocess.run(
        ["ruff", "format", "-"],
        input=code,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else code


def _import_module(path: Path):
    """Import a ``.py`` file by path under a unique module name."""
    spec = importlib.util.spec_from_file_location(f"_nodebpy_build_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _builders(module) -> list[type[NodeGroupBuilder]]:
    """Concrete ``NodeGroupBuilder`` subclasses defined in ``module``."""
    return [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, NodeGroupBuilder)
        and obj.__module__ == module.__name__
        and getattr(obj, "_name", None)
    ]


def _build(args: argparse.Namespace) -> None:
    import bpy

    bpy.ops.wm.read_factory_settings(use_empty=True)

    built: list[str] = []
    for py in args.modules:
        module = _import_module(py)
        builders = _builders(module)
        if not builders:
            print(f"  {py}: no NodeGroupBuilder subclasses found, skipping")
            continue
        for builder in builders:
            if args.no_asset:
                tree = builder.create_group()
                tree.use_fake_user = True
            else:
                tree = builder.create_asset()
            built.append(tree.name)

    if not built:
        raise SystemExit("No node groups were built.")

    bpy.ops.wm.save_as_mainfile(filepath=str(args.output.resolve()))
    print(f"Saved {len(built)} group(s) to {args.output}: {', '.join(built)}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nodebpy", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    export = sub.add_parser(
        "export", help="Convert a .blend's node groups to nodebpy Python code."
    )
    export.add_argument("blend", type=Path, help="Source .blend file.")
    export.add_argument(
        "-o", "--output", type=Path, help="Output .py path (default: stdout)."
    )
    export.add_argument(
        "-n",
        "--name",
        action="append",
        help="Node group to export (repeatable; default: all groups).",
    )
    export.add_argument(
        "--snapshot-positions",
        action="store_true",
        help="Preserve each node's x/y location in the generated code.",
    )
    export.add_argument(
        "--keep-reroutes",
        action="store_true",
        help="Keep reroute nodes instead of collapsing them.",
    )
    export.add_argument(
        "--min-chain-length",
        type=int,
        default=3,
        help="Minimum pipeline length expressed with >> (default: 3).",
    )
    export.add_argument(
        "--no-strict",
        action="store_true",
        help="Emit `var = None  # TODO` for unmapped nodes instead of erroring.",
    )
    export.add_argument(
        "--no-format", action="store_true", help="Skip ruff formatting of output."
    )
    export.add_argument(
        "--nodebpy-pkg",
        default="nodebpy",
        help="Import anchor for nodebpy in the generated module.",
    )
    export.set_defaults(func=_export)

    build = sub.add_parser(
        "build", help="Build a .blend asset library from nodebpy .py modules."
    )
    build.add_argument("modules", type=Path, nargs="+", help="Source .py module(s).")
    build.add_argument(
        "-o", "--output", type=Path, required=True, help="Output .blend path."
    )
    build.add_argument(
        "--no-asset",
        action="store_true",
        help="Save the node groups without marking them as assets.",
    )
    build.set_defaults(func=_build)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
