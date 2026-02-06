# SPDX-License-Identifier: GPL-2.0-or-later

from collections import Counter, defaultdict
from collections.abc import Callable, Hashable, Iterable
from functools import cache
from operator import itemgetter
from typing import TypeVar

import bpy
from bpy.types import Node
from mathutils import Vector

from . import config


def get_ntree() -> bpy.types.NodeTree:
    from ...builder import TreeBuilder

    return TreeBuilder._tree_contexts[-1].tree


_T1 = TypeVar("_T1", bound=Hashable)
_T2 = TypeVar("_T2", bound=Hashable)


def group_by(
    iterable: Iterable[_T1],
    key: Callable[[_T1], _T2],
    sort: bool = False,
) -> dict[tuple[_T1, ...], _T2]:
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
    if node.bl_idname != "NodeReroute":
        return node.dimensions
    else:
        return REROUTE_DIM


_HIDE_OFFSET = 10


def get_top(node: Node, y_loc: float | None = None) -> float:
    if y_loc is None:
        y_loc = abs_loc(node).y

    return (y_loc + dimensions(node).y / 2) - _HIDE_OFFSET if node.hide else y_loc


def get_bottom(node: Node, y_loc: float | None = None) -> float:
    from ...arrange import calculate_node_dimensions

    if y_loc is None:
        y_loc = abs_loc(node).y
    dim_y = calculate_node_dimensions(
        node, Counter({i: len(i.links) for i in node.inputs}), 1.0
    )[1]
    bottom = y_loc - dim_y
    return bottom + dim_y / 2 - _HIDE_OFFSET if node.hide else bottom


@cache
def frame_padding() -> float:
    return 1.5 * 20.0


_MAX_LOC = 100_000


def move(node: Node, *, x: float = 0, y: float = 0) -> None:
    if x == 0 and y == 0:
        return

    # If the (absolute) value of a node's X/Y axis exceeds 100k,
    # `node.location` can't be affected directly. (This often happens with
    # frames since their locations are relative.)

    loc = node.location
    if abs(loc.x + x) <= _MAX_LOC and abs(loc.y + y) <= _MAX_LOC:
        loc += Vector((x, y))
        return

    for n in config.selected:
        n.select = n == node

    ui_scale = 1.0
    bpy.ops.transform.translate(value=[v * ui_scale for v in (x, y, 0)])

    for n in config.selected:
        n.select = True
