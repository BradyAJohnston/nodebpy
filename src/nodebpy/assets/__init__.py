"""Typed APIs for node-group assets.

``generate_asset_api`` builds typed :class:`~nodebpy.builder.AssetNodeGroup`
classes for the node groups in a ``.blend`` asset library into a single module;
``generate_asset_modules`` splits them into one module per tree type
(``geometry.py`` / ``shader.py`` / ``compositor.py``). The bundled-essentials
APIs generated for nodebpy itself live in ``nodebpy.nodes.{geometry,shader,
compositor}.assets`` and are re-exported alongside the built-in nodes.

``dump_library`` and ``build_library`` round-trip a ``.blend`` asset library
through Python source: every asset is dumped to its own ``.py`` file (the
version-controlled source of truth) and the ``.blend`` is rebuilt from them
(``python -m nodebpy.assets dump/build``). The CLI adds ``ensure`` (rebuild
only when the ``.blend`` or its fingerprint stamp is stale) and ``check``
(verify that build → dump reproduces the sources byte-for-byte), and reads
its arguments from a ``[tool.nodebpy.assets]`` pyproject table — see
:mod:`nodebpy.assets._pipeline`. ``plot_library`` renders node groups from a
``.blend`` to PNG images by name or wildcard
(``python -m nodebpy.assets plot``), for review outside Blender.
"""

from ..builder import AssetLibrary, BundledLibrary, PackageLibrary
from ._codegen import generate_asset_api, generate_asset_modules
from ._library import build_library, dump_library, plot_library

__all__ = [
    "AssetLibrary",
    "BundledLibrary",
    "PackageLibrary",
    "build_library",
    "dump_library",
    "generate_asset_api",
    "generate_asset_modules",
    "plot_library",
]
