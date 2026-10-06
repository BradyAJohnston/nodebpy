"""Regenerate the typed classes for Blender's bundled essentials asset
libraries into ``src/nodebpy/nodes/<tree>/assets.py``."""

from __future__ import annotations

import os
from pathlib import Path

from nodebpy.assets import BundledLibrary, generate_asset_api

# Bundled libraries shipped with Blender, by the tree type of their groups.
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
    """Write ``<nodes_dir>/<tree>/assets.py`` for each tree type and return
    the class names written per tree. Libraries this Blender install does
    not ship are skipped."""
    written: dict[str, list[str]] = {}
    for tree, filenames in _ESSENTIALS.items():
        libraries = [
            BundledLibrary(f)
            for f in filenames
            if os.path.exists(BundledLibrary(f).path())
        ]
        if not libraries:
            print(f"  {tree}: no bundled libraries present, skipping")
            continue
        names = generate_asset_api(
            libraries, Path(nodes_dir) / tree / "assets.py", nodebpy_pkg=nodebpy_pkg
        )
        written[tree] = names
        print(f"  nodes/{tree}/assets.py: {len(names)} asset classes")
    return written
