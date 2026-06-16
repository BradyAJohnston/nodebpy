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


def main() -> None:
    nodes_dir = Path(__file__).parent.parent / "nodes"
    for tree, filenames in _ESSENTIALS.items():
        libraries = [
            BundledLibrary(f)
            for f in filenames
            if os.path.exists(BundledLibrary(f).path())
        ]
        if not libraries:
            print(f"  {tree}: no bundled libraries present, skipping")
            continue
        names = generate_asset_api(libraries, nodes_dir / tree / "assets.py")
        print(f"  nodes/{tree}/assets.py: {len(names)} asset classes")


if __name__ == "__main__":
    main()
