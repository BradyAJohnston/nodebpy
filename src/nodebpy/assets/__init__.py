"""Typed APIs for node-group assets.

``generate_asset_api`` builds typed :class:`~nodebpy.builder.AssetNodeGroup`
classes for the node groups in a ``.blend`` asset library. The bundled-essentials
APIs generated for nodebpy itself live alongside this module as
``nodebpy.assets.geometry`` / ``.shader`` / ``.compositor``.
"""

from ..builder import AssetLibrary, BundledLibrary, PackageLibrary
from ._codegen import generate_asset_api

__all__ = [
    "generate_asset_api",
    "AssetLibrary",
    "BundledLibrary",
    "PackageLibrary",
]
