# SPDX-License-Identifier: GPL-2.0-or-later
"""An x for every column (:func:`assign_x_coords`)."""

from __future__ import annotations

from collections.abc import Collection, Sequence
from itertools import chain
from typing import cast

from .common import FRAME_PADDING
from .config import LayoutState
from .digraph import DiGraph, LayoutGraph, ancestors, dag_longest_path_length
from .model import Cluster, Node


def frame_padding_of_col(
    columns: Sequence[Collection[Node]],
    i: int,
    T: DiGraph[Node | Cluster],
) -> float:
    """Extra room between column *i* and the next for the outlines of the
    frames that end or begin between them: ``FRAME_PADDING`` for each level
    of nesting that ends, and for each that begins."""
    col = columns[i]

    if col == columns[-1]:
        return 0

    clusters1 = {cast(Cluster, v.cluster) for v in col}
    clusters2 = {cast(Cluster, v.cluster) for v in columns[i + 1]}

    if not clusters1 ^ clusters2:
        return 0

    ST1 = T.subgraph(chain(clusters1, *[ancestors(T, c) for c in clusters1]))
    ST2 = T.subgraph(chain(clusters2, *[ancestors(T, c) for c in clusters2]))

    for u, v in tuple(ST1.edges()):
        ST1.set_weight(u, v, int(not ST2.has_edge(u, v)))

    for u, v in tuple(ST2.edges()):
        ST2.set_weight(u, v, int(not ST1.has_edge(u, v)))

    dist = dag_longest_path_length(ST1) + dag_longest_path_length(ST2)
    return FRAME_PADDING * dist


def assign_x_coords(
    G: LayoutGraph[Node], T: DiGraph[Node | Cluster], state: LayoutState
) -> None:
    """Give every node its ``x``, column by column from the left. A node is
    centred in its column, and a reroute sits at the column's left edge.
    The gap to the next column is the horizontal margin, widened up to
    three times when many links leaving the column are steep, plus the
    room frame outlines need."""
    columns: list[list[Node]] = G.columns
    x = 0
    for i, col in enumerate(columns):
        if not col:
            # A column that held only dummy nodes, since dissolved, takes
            # no space.
            continue
        max_width = max([v.width for v in col])

        for v in col:
            v.x = x if v.is_reroute else x - (v.width - max_width) / 2

        # https://doi.org/10.7155/jgaa.00220 (p. 139)
        delta_i = sum(
            [
                1
                for link in G.out_links(col)
                if abs(link.tosock.y - link.fromsock.y) >= state.margin.x * 3
            ]
        )
        spacing = (1 + min(delta_i / 4, 2)) * state.margin.x
        x += max_width + spacing + frame_padding_of_col(columns, i, T)
