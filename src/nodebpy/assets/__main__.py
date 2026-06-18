"""Regenerate the bundled-essentials asset APIs.

``python -m nodebpy.assets`` introspects Blender's bundled node-group asset
libraries and writes typed classes to ``nodebpy/nodes/{geometry,shader,
compositor}/assets.py``, where ``python -m gen`` re-exports them so they are
available alongside the built-in nodes (e.g. ``g.SmoothByAngle()``). Run *before*
``python -m gen`` and through the ruff/ty post-processing (see the Makefile).
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from ..builder import BundledLibrary, PackageLibrary
from ._codegen import generate_asset_api

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
    nodes_dir: Path, nodebpy_pkg: str = ".."
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
        )
        written[tree] = names
        print(f"  nodes/{tree}/assets.py: {len(names)} asset classes")
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
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
        help="Path of the assets.py module to write.",
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
    return parser.parse_args()


def main() -> None:  # pragma: no cover - CLI wrapper
    args = parse_args()
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
        relative = Path(os.path.relpath(blend, output.resolve().parent)).as_posix()
        generate_asset_api(
            [PackageLibrary(str(output), relative)],
            output,
            nodebpy_pkg=args.nodebpy_pkg,
        )
        return

    generate_essentials(Path(__file__).parent.parent / "nodes")


if __name__ == "__main__":  # pragma: no cover
    main()
