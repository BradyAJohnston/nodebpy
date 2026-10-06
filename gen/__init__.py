"""Build-time code generator for nodebpy's node classes.

Run with ``python -m gen`` (see the Makefile). This package is intentionally
kept outside ``src/`` so it is never shipped in the installed wheel.
"""

# The project's own nodebpy, before anything imports bpy: Blender puts its
# extensions' site-packages first on sys.path when bpy loads, and a nodebpy
# installed there (as a dependency of another extension) would shadow the
# sources being generated.
import nodebpy  # noqa: F401  # isort: skip

from .customizations import NodeCustomization, register_customization

__all__ = ["NodeCustomization", "register_customization"]
