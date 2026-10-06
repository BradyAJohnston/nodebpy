"""Lay out the unconnected parts of a tree apart.

A tree is often several drawings: the main graph, a second group of nodes
linked to nothing in the first, a frame holding only a note. Laid out as
one graph they share columns. Here the tree is split into its parts
(:func:`components`), and the boxes of the laid-out parts are put together
(:func:`pack`): the largest first, the others in rows beneath it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from .common import FRAME_PADDING, Vec2, f32, frame_label_room
from .dna import bNode, bNodeTree
from .edits import Edit, MoveNode

type Rect = tuple[float, float, float, float]
"""``(xmin, ymin, xmax, ymax)``"""


def _outermost_frame(node: bNode) -> bNode | None:
    frame = node.parent
    while frame is not None and frame.parent is not None:
        frame = frame.parent
    return frame


def components(
    tree: bNodeTree, fixed: frozenset[bNode] = frozenset()
) -> list[list[bNode]]:
    """The parts of *tree* that are laid out by themselves: its nodes
    (frames and the *fixed* ones aside), grouped so that nodes joined by a
    link, in the same outermost frame or in the same zone are in one part.
    Parts and their nodes are in the tree's order."""
    nodes = [n for n in tree.nodes if n not in fixed and not n.is_frame()]
    leader = {n: n for n in nodes}

    def find(node: bNode) -> bNode:
        root = node
        while leader[root] is not root:
            root = leader[root]
        while leader[node] is not root:
            leader[node], node = root, leader[node]
        return root

    def join(group: Sequence[bNode]) -> None:
        group = [n for n in group if n in leader]
        for other in group[1:]:
            leader[find(other)] = find(group[0])

    for link in tree.links:
        join((link.fromnode, link.tonode))
    by_frame: dict[bNode, list[bNode]] = {}
    for node in nodes:
        frame = _outermost_frame(node)
        if frame is not None:
            by_frame.setdefault(frame, []).append(node)
    for members in by_frame.values():
        join(members)
    for zone in tree.zones:
        join(zone.nodes())

    parts: dict[bNode, list[bNode]] = {}
    for node in nodes:
        parts.setdefault(find(node), []).append(node)
    return list(parts.values())


def subtree(tree: bNodeTree, nodes: Sequence[bNode]) -> bNodeTree:
    """The part of *tree* made of *nodes*: they, the frames around them and
    the links among them. The nodes are the tree's own, not copies."""
    inside = set(nodes)
    frames: dict[bNode, None] = {}
    for node in nodes:
        frame = node.parent
        while frame is not None and frame not in frames:
            frames[frame] = None
            frame = frame.parent
    return bNodeTree(
        nodes=[n for n in tree.nodes if n in inside or n in frames],
        links=[k for k in tree.links if k.fromnode in inside and k.tonode in inside],
        zones=[z for z in tree.zones if z.input_node in inside],
    )


def bounds(edits: Sequence[Edit]) -> Rect | None:
    """The box around the nodes *edits* place, with the frames around
    them. None when they place nothing."""
    rects = []
    for edit in edits:
        if not isinstance(edit, MoveNode):
            continue
        node = edit.node
        left, top = edit.top_left
        right, bottom = left, top
        if not node.is_reroute():
            right, bottom = left + node.width, top - (node.top - node.bottom)
        pad = label_room = 0.0
        frame = edit.parent
        while frame is not None:
            pad += FRAME_PADDING
            label_room += frame_label_room(frame.label, frame.label_size)
            frame = frame.parent
        rects.append((left - pad, bottom - pad, right + pad, top + pad + label_room))
    if not rects:
        return None
    return (
        min(r[0] for r in rects),
        min(r[1] for r in rects),
        max(r[2] for r in rects),
        max(r[3] for r in rects),
    )


def pack(boxes: Sequence[Rect], gap: Vec2) -> list[tuple[float, float]]:
    """Where to move each of *boxes* so that none overlap: the offset to
    add to everything in it. The first box stays where it is. The others
    go in rows beneath it, left to right in the order given. A row is as
    wide as the widest box."""
    if not boxes:
        return []
    first = boxes[0]
    left = first[0]
    limit = max(b[2] - b[0] for b in boxes)
    offsets = [(0.0, 0.0)]
    x = left
    row_top = first[1] - gap.y
    row_bottom = row_top
    for box in boxes[1:]:
        width, height = box[2] - box[0], box[3] - box[1]
        if x > left and x + width > left + limit:
            x = left
            row_top = row_bottom - gap.y
        offsets.append((f32(x - box[0]), f32(row_top - box[3])))
        x += width + gap.x
        row_bottom = min(row_bottom, row_top - height)
    return offsets


def moved(edits: Sequence[Edit], offset: tuple[float, float]) -> list[Edit]:
    """*edits* with every node they place shifted by *offset*."""
    dx, dy = offset
    if dx == 0 and dy == 0:
        return list(edits)
    return [
        replace(e, top_left=(f32(e.top_left[0] + dx), f32(e.top_left[1] + dy)))
        if isinstance(e, MoveNode)
        else e
        for e in edits
    ]


def node_rects(edits: Sequence[Edit]) -> list[Rect]:
    """The box of each node (reroutes aside) *edits* place."""
    rects = []
    for edit in edits:
        if isinstance(edit, MoveNode) and not edit.node.is_reroute():
            node = edit.node
            left, top = edit.top_left
            rects.append((left, top - (node.top - node.bottom), left + node.width, top))
    return rects


def _first_clear(blocked: list[tuple[float, float]]) -> float:
    """The smallest distance, zero or more, in none of the open intervals
    *blocked*."""
    distance = 0.0
    for start, end in sorted(blocked):
        if start >= distance:
            break
        distance = max(distance, end)
    return distance


def clear_of(
    rects: Sequence[Rect], obstacles: Sequence[Rect], gap: Vec2
) -> tuple[float, float]:
    """The shortest move left, right, up or down that takes *rects*, moved
    together, clear of every one of *obstacles* by *gap*. ``(0, 0)`` when
    they are clear already."""
    best = (0.0, 0.0)
    shortest = None
    # (axis, direction): slide along x or y, forwards or backwards.
    for axis, sign in ((1, -1), (1, 1), (0, 1), (0, -1)):
        other = 1 - axis
        margin, side = gap[axis], gap[other]
        blocked = []
        for a in rects:
            for b in obstacles:
                # Only a pair that overlaps across the slide can collide.
                if a[other] >= b[other + 2] + side or b[other] >= a[other + 2] + side:
                    continue
                if sign > 0:
                    blocked.append(
                        (b[axis] - a[axis + 2] - margin, b[axis + 2] - a[axis] + margin)
                    )
                else:
                    blocked.append(
                        (a[axis] - b[axis + 2] - margin, a[axis + 2] - b[axis] + margin)
                    )
        distance = _first_clear(blocked)
        if shortest is None or distance < shortest:
            shortest = distance
            best = (sign * distance, 0.0) if axis == 0 else (0.0, sign * distance)
    return best
