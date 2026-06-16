"""Regenerate the bundled-essentials asset APIs.

``python -m nodebpy.assets`` introspects Blender's bundled node-group asset
libraries and writes typed classes to ``nodebpy/nodes/{geometry,shader,
compositor}/assets.py``, where ``python -m gen`` re-exports them so they are
available alongside the built-in nodes (e.g. ``g.SmoothByAngle()``). Run *before*
``python -m gen`` and through the ruff/ty post-processing (see the Makefile).
"""

from __future__ import annotations

import os
from pathlib import Path

from ..builder import BundledLibrary
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


def generate_essentials(nodes_dir: Path) -> dict[str, list[str]]:
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
        names = generate_asset_api(libraries, Path(nodes_dir) / tree / "assets.py")
        written[tree] = names
        print(f"  nodes/{tree}/assets.py: {len(names)} asset classes")
    return written


def main() -> None:  # pragma: no cover - CLI wrapper over generate_essentials
    generate_essentials(Path(__file__).parent.parent / "nodes")


if __name__ == "__main__":  # pragma: no cover
    main()
