# SPDX-License-Identifier: GPL-2.0-or-later
"""Snap a finished layout to the node editor's grid."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from math import floor

from .common import f32
from .edits import Edit, MoveNode

GRID_SIZE = 20.0
"""The grid nodes snap to in the node editor (``NODE_GRID_STEP_SIZE``)."""


def snap_to_grid(edits: Sequence[Edit], grid: float = GRID_SIZE) -> list[Edit]:
    """*edits* with every node moved so that its location is on the grid.

    Each node goes to the nearest grid point. A node that would then be
    closer to one above it than the grid allows moves down a step at a
    time: two nodes keep the gap they had, rounded down to the grid.
    Reroutes stay where they are, level with the sockets they join.
    """
    moves = [
        (index, edit)
        for index, edit in enumerate(edits)
        if isinstance(edit, MoveNode) and not edit.node.is_reroute()
    ]
    # From the top down, so a node is only ever pushed by nodes already set.
    moves.sort(key=lambda move: (-move[1].top_left[1], move[1].top_left[0]))

    result = list(edits)
    # (left, right, bottom before, bottom after) of the nodes set so far.
    above: list[tuple[float, float, float, float]] = []
    for index, edit in moves:
        node = edit.node
        left, top = edit.top_left
        height = node.top - node.bottom
        # A node's location is not always the corner of its box.
        offset_x = node.location[0] - node.draw_bounds[0]
        offset_y = node.location[1] - node.draw_bounds[3]

        new_left = round((left + offset_x) / grid) * grid - offset_x
        new_top = round((top + offset_y) / grid) * grid - offset_y
        for other_left, other_right, bottom, new_bottom in above:
            if new_left >= other_right or other_left >= new_left + node.width:
                continue
            gap = floor(max(bottom - top, 0.0) / grid) * grid
            limit = new_bottom - gap
            if new_top > limit:
                new_top = floor((limit + offset_y) / grid) * grid - offset_y

        above.append((new_left, new_left + node.width, top - height, new_top - height))
        result[index] = replace(edit, top_left=(f32(new_left), f32(new_top)))
    return result
