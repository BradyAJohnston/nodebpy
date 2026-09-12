"""Regenerate the bundled-essentials asset APIs.

``python -m nodebpy.assets`` introspects Blender's bundled node-group asset
libraries and writes typed classes to ``nodebpy/nodes/{geometry,shader,
compositor}/assets.py``, where ``python -m gen`` re-exports them so they are
available alongside the built-in nodes (e.g. ``g.SmoothByAngle()``). Run *before*
``python -m gen`` and through the ruff/ty post-processing (see the Makefile).

``python -m nodebpy.assets dump <blend> <dir>`` and ``… build <dir> <blend>``
instead round-trip a ``.blend`` asset library through per-asset Python sources;
``… ensure`` rebuilds only when the ``.blend`` is missing or stale, and
``… check`` verifies that build → dump reproduces the sources byte-for-byte
(see :mod:`nodebpy.assets._library` and :mod:`nodebpy.assets._pipeline` — the
latter also documents the ``[tool.nodebpy.assets]`` pyproject table these
subcommands read their arguments from).

Under a full Blender (no ``bpy`` module) any invocation runs this file as a
script, with the arguments after Blender's ``--`` separator::

    blender -b --factory-startup -P <.../nodebpy/assets/__main__.py> -- ensure
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# ``blender ... -P .../nodebpy/assets/__main__.py`` runs this file as a plain
# script (no package context): put the package root on sys.path so the
# absolute imports resolve — a no-op under ``python -m nodebpy.assets``.
if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from nodebpy.assets._codegen import generate_asset_api, generate_asset_modules
from nodebpy.builder import BundledLibrary, PackageLibrary

# Bundled libraries shipped with Blender, grouped by output module. Each library
# holds node groups of a single tree type.
_ESSENTIALS: dict[str, tuple[str, ...]] = {
    "geometry": (
        "geometry_nodes_essentials.blend",
        "geometry_nodes_dynamics_assets.blend",
        "procedural_hair_node_assets.blend",
        "principal_components.blend",
    ),
    "shader": ("shading_nodes_essentials.blend",),
    "compositor": ("compositing_nodes_essentials.blend",),
}


def generate_essentials(
    nodes_dir: Path, nodebpy_pkg: str = "..", docstrings: bool = True
) -> dict[str, list[str]]:
    """Generate the bundled-essentials asset modules into
    ``<nodes_dir>/<tree>/assets.py``; returns the class names written per tree
    (libraries not present in this Blender install are skipped)."""
    written: dict[str, list[str]] = {}
    for tree, filenames in _ESSENTIALS.items():
        libraries = [
            BundledLibrary(f)
            for f in filenames
            if os.path.exists(BundledLibrary(f).path())
        ]
        if not libraries:  # pragma: no cover - depends on the Blender install
            print(f"  {tree}: no bundled libraries present, skipping")
            continue
        names = generate_asset_api(
            libraries,
            Path(nodes_dir) / tree / "assets.py",
            nodebpy_pkg=nodebpy_pkg,
            docstrings=docstrings,
        )
        written[tree] = names
        print(f"  nodes/{tree}/assets.py: {len(names)} asset classes")
    return written


def parse_args(
    argv: list[str] | None = None,
) -> argparse.Namespace:  # pragma: no cover - CLI wrapper
    parser = argparse.ArgumentParser(
        prog="python -m nodebpy.assets",
        description=(
            "Generate typed nodebpy API classes for node-group assets. "
            "Without a subcommand this regenerates the bundled-essentials "
            "asset APIs (or, with --blend-file, generates an API module for "
            "a custom asset library)."
        ),
        epilog=(
            "subcommands:\n"
            "  dump <blend> <output-dir>    dump every node-group asset in a "
            ".blend to per-asset .py source files\n"
            "  build <source-dir> <blend>   rebuild the .blend asset library "
            "from dumped .py source files\n"
            "  ensure <source-dir> <blend>  rebuild only when the .blend or "
            "its fingerprint stamp is missing or stale\n"
            "  check <source-dir> <blend>   verify that build -> dump "
            "reproduces the sources byte-for-byte\n"
            "  plot <blend> <output-dir> [names ...]\n"
            "                               render node groups (wildcards "
            "supported) to PNG images\n"
            "\n"
            "These subcommands can read their positionals and flags from a "
            "[tool.nodebpy.assets] table\n"
            "in the nearest pyproject.toml. Inside a full Blender (no bpy "
            "module), run any of them as\n"
            "  blender -b --factory-startup -P <.../nodebpy/assets/"
            "__main__.py> -- <subcommand ...>\n"
            "\n"
            "See 'python -m nodebpy.assets dump --help', '… build --help' "
            "and '… plot --help' for their options."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--blend-file",
        "-b",
        type=Path,
        help="Optional custom .blend asset library to generate from.",
    )
    parser.add_argument(
        "--output",
        "--output-dir",
        "-o",
        dest="output",
        type=Path,
        help=(
            "Where to write the generated module(s). A .py path writes a single "
            "module; a directory writes one module per tree type "
            "(geometry.py / shader.py / compositor.py)."
        ),
    )
    parser.add_argument(
        "--nodebpy-pkg",
        default="nodebpy",
        help=(
            "Import anchor for nodebpy in the generated module. Defaults to the "
            "absolute 'nodebpy'. When nodebpy is vendored inside another package, "
            "pass the path that reaches it relative to the generated module's "
            "package — e.g. '..lib.nodebpy'."
        ),
    )
    parser.add_argument(
        "--no-docstrings",
        dest="docstrings",
        action="store_false",
        help=(
            "Skip the numpy-style class docstrings (description, Parameters, "
            "Inputs, Outputs) and emit a terser module."
        ),
    )
    return parser.parse_args(argv)


def main() -> None:  # pragma: no cover - CLI wrapper
    # Blender passes script arguments after a ``--`` separator (``blender -b
    # --factory-startup -P .../__main__.py -- build``): strip everything up
    # to and including it, so the same subcommands work there too.
    argv = sys.argv[1:]
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]

    # The dump/build/ensure/check/plot subcommands (blend ↔ .py round-trip,
    # staleness stamping, roundtrip verification, PNG renders) have their own
    # parser; everything else keeps the original flag-based interface.
    if argv and argv[0] in ("dump", "build", "ensure", "check", "plot"):
        from nodebpy.assets._library import main as library_main

        library_main(argv)
        return

    args = parse_args(argv)
    output = (
        args.output
        if args.output
        else Path(__file__).parent.parent / "nodes" / "custom" / "assets.py"
    )

    if args.blend_file is not None:
        # PackageLibrary resolves ``relative`` against the generated module's
        # directory (``__file__``), so express the .blend relative to the output
        # module — not the CWD the command happened to run from.
        blend = args.blend_file.resolve()
        if output.suffix != ".py":
            # Directory output: one module per tree type.
            out_dir = output.resolve()
            relative = Path(os.path.relpath(blend, out_dir)).as_posix()
            generate_asset_modules(
                [PackageLibrary(str(out_dir / "_anchor.py"), relative)],
                output,
                nodebpy_pkg=args.nodebpy_pkg,
            )
            return
        relative = Path(os.path.relpath(blend, output.resolve().parent)).as_posix()
        generate_asset_api(
            [PackageLibrary(str(output), relative)],
            output,
            nodebpy_pkg=args.nodebpy_pkg,
            docstrings=args.docstrings,
        )
        return

    generate_essentials(
        Path(__file__).parent.parent / "nodes", docstrings=args.docstrings
    )


if __name__ == "__main__":  # pragma: no cover
    main()
