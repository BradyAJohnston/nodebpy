"""Snap a layout to the node editor's grid.

Two passes. :func:`snap_rows` runs inside the pipeline, once nodes have
their heights: it puts each node on a grid row, so that the reroutes and
bend points placed afterwards line up with the snapped nodes.
:func:`snap_to_grid` runs on the finished layout and puts whatever is still
off the grid on it: the columns, and the nodes of stacks.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from itertools import pairwise
from math import floor

from .common import FRAME_PADDING, GRID_SIZE, f32
from .dna import bNode
from .edits import Edit, MoveNode
from .model import Cluster, Kind, Node, is_real
from .pipeline import Layout

# Two neighbours in a column may come this close (in grid steps) before the
# lower one is moved down. Rounding moves each by at most half a step, so
# with a margin of a step and a half or more nothing is ever moved down,
# and nodes that were level stay level.
_MIN_GAP = 0.5
_LEVELLING_ROUNDS = 3


def _location_offset(node: bNode) -> tuple[float, float]:
    """From the top-left corner of the box *node* is drawn in to its
    location, which is what lands on the grid. They differ for a collapsed
    node."""
    return (
        node.location[0] - node.draw_bounds[0],
        node.location[1] - node.draw_bounds[3],
    )


def _nearest(value: float, grid: float) -> float:
    """The grid line nearest *value*, the higher one from half way. Values
    that differ only by rounding error go the same way, and so do values a
    whole number of steps apart, which keeps level nodes level and evenly
    spaced ones evenly spaced. (``round`` sends halves to the even line.)"""
    return floor(round(value, 3) / grid + 0.5) * grid


def _is_snapped(v: Node) -> bool:
    return v.type == Kind.NODE and is_real(v) and not v.is_reroute


def snap_rows(layout: Layout, grid: float = GRID_SIZE) -> None:
    """Move every node of the tree to the nearest grid row.

    A frame's border nodes move with the frame's nodes, so the frame keeps
    its room, and its lower border is kept level across its columns. A
    node left less than half a grid step under the one above it in its
    column moves down a row; with a margin of a step and a half or more
    that never happens, and nodes that were level stay level."""
    columns = layout.G.columns
    before = {v: v.y for col in columns for v in col}
    offsets = {
        v: _location_offset(v.node)[1]
        for v in before
        if _is_snapped(v) and v.node is not None
    }
    for v, offset in offsets.items():
        v.y = _nearest(v.y + offset, grid) - offset

    # Each frame's border nodes, and for each the side its frame is on: the
    # first one met in a column is the upper border, with the frame below.
    inside_below: dict[Node, bool] = {}
    lower_borders: dict[Cluster, list[Node]] = {}
    for col in columns:
        seen: set[Cluster] = set()
        for v in col:
            if v.type != Kind.VERTICAL_BORDER or v.cluster is None:
                continue
            inside_below[v] = v.cluster not in seen
            if v.cluster in seen:
                lower_borders.setdefault(v.cluster, []).append(v)
            seen.add(v.cluster)

    # A border moves as the nearest node on its frame's side did.
    for col in columns:
        for i, v in enumerate(col):
            if v not in inside_below:
                continue
            side = col[i + 1 :] if inside_below[v] else reversed(col[:i])
            member = next((w for w in side if w in offsets), None)
            if member is not None:
                v.y += member.y - before[member]

    # Room a frame's outline needs beyond the margin under its border.
    outside_gap = max(FRAME_PADDING - layout.state.margin.y, 0.0)

    def room(upper: Node, v: Node) -> float:
        """The least gap to leave between two neighbours in a column."""
        gap = before[upper] - upper.height - before[v]
        if inside_below.get(upper) is True or inside_below.get(v) is False:
            return gap  # a border and what is in its frame
        if upper in inside_below or v in inside_below:
            return max(min(gap, outside_gap), 0.0)
        return max(min(gap, grid * _MIN_GAP), 0.0)

    def settle(col: Sequence[Node]) -> bool:
        """Move the nodes of *col* down until each has its room under the
        node above. Returns whether any moved."""
        moved = False
        for upper, v in pairwise(col):
            limit = upper.y - upper.height - room(upper, v)
            if v.y > limit:
                offset = offsets.get(v)
                if offset is not None:
                    limit = floor((limit + offset) / grid) * grid - offset
                v.y = limit
                moved = True
        return moved

    for col in columns:
        settle(col)
    # Levelling a border can push nodes down, which can lower another
    # frame's border in turn. Two frames side by side in one column and the
    # other way up in another would chase each other, so stop after a few
    # rounds.
    for _ in range(_LEVELLING_ROUNDS):
        changed = False
        for borders in lower_borders.values():
            lowest = min(v.y for v in borders)
            for v in borders:
                if v.y > lowest:
                    v.y = lowest
                    changed = True
        if not changed:
            break
        for col in columns:
            settle(col)


def snap_to_grid(edits: Sequence[Edit], grid: float = GRID_SIZE) -> list[Edit]:
    """*edits* with every node moved so that its location is on the grid.

    Each node goes to the nearest grid point. A node left less than half a
    grid step under one above it moves down a step. A reroute moves as the
    node nearest to it does, which keeps it level with the socket it was
    aligned to."""
    moves = [(i, e) for i, e in enumerate(edits) if isinstance(e, MoveNode)]
    nodes = [(i, e) for i, e in moves if not e.node.is_reroute()]
    # From the top down, so a node is only ever pushed by nodes already set.
    nodes.sort(key=lambda move: (-move[1].top_left[1], move[1].top_left[0]))

    result = list(edits)
    # (left, right, bottom before, bottom after) of the nodes set so far.
    above: list[tuple[float, float, float, float]] = []
    # (centre before, how far it moved) of each node.
    shifts: list[tuple[float, float, float, float]] = []
    for index, edit in nodes:
        node = edit.node
        left, top = edit.top_left
        height = node.top - node.bottom
        offset_x, offset_y = _location_offset(node)

        new_left = _nearest(left + offset_x, grid) - offset_x
        new_top = _nearest(top + offset_y, grid) - offset_y
        for other_left, other_right, bottom, new_bottom in above:
            if new_left >= other_right or other_left >= new_left + node.width:
                continue
            gap = max(min(bottom - top, grid * _MIN_GAP), 0.0)
            limit = new_bottom - gap
            if new_top > limit:
                new_top = floor((limit + offset_y) / grid) * grid - offset_y

        above.append((new_left, new_left + node.width, top - height, new_top - height))
        shifts.append(
            (left + node.width / 2, top - height / 2, new_left - left, new_top - top)
        )
        result[index] = replace(edit, top_left=(f32(new_left), f32(new_top)))

    if not shifts:
        return result
    for index, edit in moves:
        if not edit.node.is_reroute():
            continue
        x, y = edit.top_left
        _, _, dx, dy = min(shifts, key=lambda s: (s[0] - x) ** 2 + (s[1] - y) ** 2)
        result[index] = replace(edit, top_left=(f32(x + dx), f32(y + dy)))
    return result
