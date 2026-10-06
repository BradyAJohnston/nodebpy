"""Layout of Blender node trees.

:func:`arrange` is the entry. It works in three stages:

1. :func:`~.extract.extract` reads the Blender tree into plain data
   (:mod:`.dna`).
2. :func:`~.sugiyama.sugiyama_layout` computes the layout from that data
   alone, never touching Blender, and returns the edits to make
   (:mod:`.edits`).
3. :func:`~.apply.apply` carries the edits out on the Blender tree.

``DESIGN.md`` beside this file explains the layout end to end.
"""

from .api import ArrangeMethod, arrange, default_sugiyama_options
from .config import SIMPLE_OPTIONS, SugiyamaOptions
from .sugiyama import sugiyama_layout

__all__ = [
    "SIMPLE_OPTIONS",
    "ArrangeMethod",
    "SugiyamaOptions",
    "arrange",
    "default_sugiyama_options",
    "sugiyama_layout",
]
