"""Typed APIs for node-group assets.

``generate_asset_api`` builds typed :class:`~nodebpy.builder.AssetNodeGroup`
classes for the node groups in a ``.blend`` asset library into a single module;
``generate_asset_modules`` splits them into one module per tree type
(``geometry.py`` / ``shader.py`` / ``compositor.py``). The bundled-essentials
APIs generated for nodebpy itself live in ``nodebpy.nodes.{geometry,shader,
compositor}.assets`` and are re-exported alongside the built-in nodes.
"""

from ..builder import AssetLibrary, BundledLibrary, PackageLibrary
from ._codegen import generate_asset_api, generate_asset_modules

__all__ = [
    "generate_asset_api",
    "generate_asset_modules",
    "AssetLibrary",
    "BundledLibrary",
    "PackageLibrary",
]
