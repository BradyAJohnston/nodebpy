"""Build-time code generator for nodebpy's node classes.

Run with ``python -m gen`` (see the Makefile). This package is intentionally
kept outside ``src/`` so it is never shipped in the installed wheel.
"""

from .customizations import NodeCustomization, register_customization

__all__ = ["NodeCustomization", "register_customization"]
