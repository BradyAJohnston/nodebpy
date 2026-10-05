# SPDX-License-Identifier: GPL-2.0-or-later
"""Sugiyama-style layout of Blender node trees.

Three stages:

1. :func:`~.extract.extract` reads the Blender tree into plain data
   (:mod:`.dna`), measuring node sizes and socket positions.
2. :func:`.arrange.sugiyama.sugiyama_layout` computes the layout from that
   data alone and returns the edits to make (:mod:`.arrange.edits`). It
   never touches Blender. The layout is a list of named steps
   (:mod:`.arrange.pipeline`).
3. :func:`~.apply.apply` carries the edits out on the Blender tree.

``DESIGN.md`` beside this file explains the layout end to end.
"""

from __future__ import annotations

from bpy.types import NodeTree

from .apply import apply
from .arrange import sugiyama
from .arrange.pipeline import Observer, Pipeline
from .config import Settings
from .extract import extract, optimize_sizes

__all__ = [
    "arrange_node_tree",
    "sugiyama",
]


def arrange_node_tree(
    ntree: NodeTree,
    settings: Settings | None = None,
    margin: tuple[float, float] | None = None,
    *,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
    verify: bool = False,
    selected_only: bool = False,
) -> None:
    """Arrange the nodes of *ntree*.

    The whole tree is laid out unless *selected_only* is set. (The
    node-arrange addon always arranges the user's selection; but a
    library-loaded tree has no selection at all, which would silently
    arrange nothing.) With *selected_only* the selected nodes are arranged
    among themselves around where they were; other nodes do not move, and
    links to them are left out of account.

    *pipeline*, *observer* and *verify* are passed on to the layout (see
    :func:`.arrange.sugiyama.sugiyama_layout`).
    """
    settings = settings or Settings()
    if settings.optimize_sizes:
        optimize_sizes(ntree.nodes)

    tree, binding = extract(ntree)
    result = sugiyama.sugiyama_layout(
        tree,
        settings,
        margin,
        pipeline=pipeline,
        observer=observer,
        verify=verify,
        selected_only=selected_only,
    )
    apply(ntree, binding, result)
