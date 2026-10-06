"""Small helpers shared by the layout passes. Nothing here needs ``bpy``."""

from __future__ import annotations

import struct
from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable
from operator import itemgetter
from typing import NamedTuple

from .dna import REROUTE_SIZE


class Vec2(NamedTuple):
    x: float
    y: float


REROUTE_DIM = Vec2(REROUTE_SIZE, REROUTE_SIZE)

type Point = tuple[float, float]

REROUTE_MARGIN_Y_FAC = 0.35
"""Fraction of the vertical margin kept between two reroutes or dummy
nodes next to each other in a column. Long links routed past a column pack
tighter than nodes."""


GRID_SIZE = 20.0
"""The grid nodes snap to in the node editor (``NODE_GRID_STEP_SIZE``)."""

FRAME_PADDING = 30.0
"""Room between a frame's border and the nodes in it (``NODE_FRAME_MARGIN``)."""


def frame_label_room(label: str, label_size: float) -> float:
    """Extra room a frame's label takes above the nodes in it."""
    return label_size * 1.25 - FRAME_PADDING / 2 if label else 0.0


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


_FLOAT = struct.Struct("f")


def f32(value: float) -> float:
    """*value* rounded to single precision, which is what Blender stores
    locations in."""
    return _FLOAT.unpack(_FLOAT.pack(value))[0]


def _cross(a: Point, b: Point) -> float:
    return f32(f32(a[0] * b[1]) - f32(a[1] * b[0]))


def _dot(a: Point, b: Point) -> float:
    return f32(f32(a[0] * b[0]) + f32(a[1] * b[1]))


def _sub(a: Point, b: Point) -> Point:
    return (f32(a[0] - b[0]), f32(a[1] - b[1]))


def segments_intersect(v0: Point, v1: Point, v2: Point, v3: Point) -> bool:
    """Whether segment ``v0-v1`` meets segment ``v2-v3`` in a single point.

    Segments lying along each other over a stretch do not count. Follows
    Blender's ``isect_seg_seg_v2_point`` (single precision included), which
    is what ``mathutils.geometry.intersect_line_line_2d`` calls.
    """
    v0, v1, v2, v3 = (
        (f32(v0[0]), f32(v0[1])),
        (f32(v1[0]), f32(v1[1])),
        (f32(v2[0]), f32(v2[1])),
        (f32(v3[0]), f32(v3[1])),
    )
    s10 = _sub(v1, v0)
    s32 = _sub(v3, v2)
    s30 = _sub(v3, v0)

    d = _cross(s10, s32)
    if d != 0:
        u = f32(_cross(s30, s32) / d)
        v = f32(_cross(s10, s30) / d)
        if not (0.0 <= u <= 1.0 and 0.0 <= v <= 1.0):
            return False

        # When `d` approaches zero, precision lets non-overlapping collinear
        # segments pass. Recompute `v` from the intersection point.
        point = (f32(v0[0] + f32(s10[0] * u)), f32(v0[1] + f32(s10[1] * u)))
        v = f32(_dot(s32, _sub(point, v2)) / _dot(s32, s32))
        return 0.0 <= v <= 1.0

    if _cross(s10, s30) != 0.0 or _cross(s32, s30) != 0.0:
        return False  # parallel

    # On one line.
    if v0 == v1:
        if _dot(_sub(v3, v2), _sub(v3, v2)) > 1e-12:
            # Use the segment that is not a point as the basis.
            v0, v2 = v2, v0
            v1, v3 = v3, v1
            s10 = _sub(v1, v0)
            s30 = _sub(v3, v0)
        else:
            return v0 == v2  # two points

    s20 = _sub(v2, v0)
    length = _dot(s10, s10)
    u_a = f32(_dot(s20, s10) / length)
    u_b = f32(_dot(s30, s10) / length)
    if u_a > u_b:
        u_a, u_b = u_b, u_a

    if u_a > 1.0 or u_b < 0.0:
        return False

    return max(0.0, u_a) == min(1.0, u_b)
