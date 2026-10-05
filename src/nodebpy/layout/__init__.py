# SPDX-License-Identifier: GPL-2.0-or-later
"""Layout of Blender node trees.

:func:`arrange` is the entry: the layered (Sugiyama) layout by default, or
the simple column arrangement. The layered layout is three stages:

1. :func:`~.extract.extract` reads the Blender tree into plain data
   (:mod:`.dna`), with node sizes and socket positions.
2. :func:`~.sugiyama.sugiyama_layout` computes the layout from that data
   alone and returns the edits to make (:mod:`.edits`). It never touches
   Blender. It runs a list of named steps (:mod:`.pipeline`).
3. :func:`~.apply.apply` carries the edits out on the Blender tree.

``DESIGN.md`` beside this file explains the layout end to end.
"""

from .api import (
    ArrangeMethod,
    SimpleOptions,
    SugiyamaOptions,
    arrange,
    arrange_node_tree,
    default_split_inputs,
    default_sugiyama_options,
)
from .config import Settings
from .simple import arrange_tree
from .sugiyama import sugiyama_layout

__all__ = [
    "ArrangeMethod",
    "Settings",
    "SimpleOptions",
    "SugiyamaOptions",
    "arrange",
    "arrange_node_tree",
    "arrange_tree",
    "default_split_inputs",
    "default_sugiyama_options",
    "sugiyama_layout",
]
