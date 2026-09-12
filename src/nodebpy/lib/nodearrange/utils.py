# SPDX-License-Identifier: GPL-2.0-or-later

from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable
from functools import cache
from operator import itemgetter

import bpy
from bpy.types import Node
from mathutils import Vector


def group_by[T1: Hashable, T2: Hashable](
    iterable: Iterable[T1],
    key: Callable[[T1], T2],
    sort: bool = False,
) -> dict[tuple[T1, ...], T2]:
    groups = defaultdict(list)
    for item in iterable:
        groups[key(item)].append(item)

    items = sorted(groups.items(), key=itemgetter(0)) if sort else groups.items()
    return {tuple(g): k for k, g in items}


def abs_loc(node: Node) -> Vector:
    loc = node.location.copy()

    parent = node
    while parent := parent.parent:
        loc += parent.location

    return loc


REROUTE_DIM = Vector((8, 8))


def dimensions(node: Node) -> Vector:
    if node.bl_idname == "NodeReroute":
        return REROUTE_DIM

    dim = node.dimensions
    if dim.x > 0 and dim.y > 0:  # pragma: no cover - only drawn in a UI
        return dim

    # `node.dimensions` is only computed when a node editor draws the tree;
    # under the headless `bpy` module it stays (0, 0), so estimate instead.
    from ...builder.layout import calculate_node_dimensions

    return Vector(calculate_node_dimensions(node))


_HIDE_OFFSET = 10


def get_top(node: Node, y_loc: float | None = None) -> float:
    if y_loc is None:
        y_loc = abs_loc(node).y

    return (y_loc + dimensions(node).y / 2) - _HIDE_OFFSET if node.hide else y_loc


def get_bottom(node: Node, y_loc: float | None = None) -> float:
    if y_loc is None:
        y_loc = abs_loc(node).y
    dim_y = dimensions(node).y
    bottom = y_loc - dim_y
    return bottom + dim_y / 2 - _HIDE_OFFSET if node.hide else bottom


@cache
def frame_padding() -> float:
    return 1.5 * 20.0


_MAX_LOC = 100_000


def move(node: Node, selected: list[Node], *, x: float = 0, y: float = 0) -> None:
    if x == 0 and y == 0:
        return

    # If the (absolute) value of a node's X/Y axis exceeds 100k,
    # `node.location` can't be affected directly. (This often happens with
    # frames since their locations are relative.)

    loc = node.location
    if abs(loc.x + x) <= _MAX_LOC and abs(loc.y + y) <= _MAX_LOC:
        loc += Vector((x, y))
        return

    _move_via_operator(node, selected, x, y)  # pragma: no cover - see below


def _move_via_operator(
    node: Node, selected: list[Node], x: float, y: float
) -> None:  # pragma: no cover - needs a windowed UI context
    for n in selected:
        n.select = n == node

    ui_scale = 1.0
    bpy.ops.transform.translate(value=[v * ui_scale for v in (x, y, 0)])

    for n in selected:
        n.select = True
