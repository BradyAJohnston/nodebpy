# SPDX-License-Identifier: GPL-2.0-or-later
"""Measure how readable a node tree's layout is.

:func:`measure` looks at a tree as it is currently laid out — node locations,
node sizes, socket positions, frames — and counts the things that make a
layout hard or easy to read: link crossings, links running backwards or
through unrelated nodes, overlapping nodes and frames, how many links are
straight, how much room the drawing takes.

It measures plain data (a :class:`~.dna.bNodeTree`), so a layout can be
judged without Blender: ``result.apply_to(tree); measure(tree)``. Given a
Blender tree it reads it with :func:`~.extract.extract` first, which is the
geometry the arranger and :func:`nodebpy.export.to_plot` use (drawn sizes
when Blender has drawn the tree, estimates otherwise), so the numbers
describe the picture ``to_plot`` draws.

The metrics are the yardstick for changing the layout algorithm: arrange a
corpus of trees before and after a change and compare. :meth:`LayoutMetrics.cost`
folds them into one number to minimise when tuning.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from itertools import combinations
from statistics import fmean
from typing import TYPE_CHECKING, Any

import numpy as np

from .arrange.common import frame_padding
from .arrange.priority import FLOW_SOCKETS, zone_spine
from .dna import bNode, bNodeLink, bNodeSocket, bNodeTree

if TYPE_CHECKING:
    from numpy.typing import NDArray

type Rect = tuple[float, float, float, float]
"""``(xmin, ymin, xmax, ymax)``"""

# A link counts as straight when its two sockets are this close in height.
_STRAIGHT_TOL = 1.0
# Rectangles must overlap by more than this, in both axes, to count.
_OVERLAP_TOL = 1.0
# Straight pieces a link's curve is approximated by.
_CURVE_SEGMENTS = 12
# Room a frame's label takes above its contents (see `to_plot`).
_FRAME_LABEL_PADDING = 10.0
# Room Blender leaves between a zone's nodes and its outline.
_ZONE_PADDING = 10.0


@dataclass(frozen=True, slots=True)
class CostWeights:
    """What each defect costs in :meth:`LayoutMetrics.cost`. Lengths are in
    Blender UI units, so the per-unit weights are small."""

    crossing: float = 10.0
    mixed_crossing: float = 10.0
    """On top of ``crossing``, for a link of values crossing one that
    carries the tree's main data."""
    backward_link: float = 20.0
    node_overlap: float = 50.0
    link_through_node: float = 15.0
    frame_overlap: float = 30.0
    foreign_node_in_frame: float = 30.0
    bent_zone: float = 10.0
    """For a zone whose spine is not one straight line."""
    bent_link: float = 1.0
    bent_flow_link: float = 4.0
    """On top of ``bent_link``, for a link carrying the tree's main data."""
    fork_imbalance: float = 0.02
    link_length: float = 0.002
    link_span_y: float = 0.01
    area: float = 1e-6


@dataclass(frozen=True, slots=True)
class LayoutMetrics:
    """Counts and sizes describing one layout. Lower is better for every
    field except :attr:`straight_links`."""

    nodes: int
    """Nodes other than frames (reroutes included)."""
    reroutes: int
    links: int
    width: float
    """Width of the box around all nodes and frames."""
    height: float
    crossings: int
    """Pairs of links whose curves cross."""
    backward_links: int
    """Links whose target socket is left of their source socket."""
    straight_links: int
    """Links whose two sockets are at the same height."""
    level_links: int
    """Links that are straight, or whose two nodes have their tops at the
    same height: the nodes read as one row."""
    link_length: float
    """Summed straight-line distance between linked sockets."""
    link_span_y: float
    """Summed height difference between linked sockets."""
    node_overlaps: int
    """Pairs of nodes drawn on top of each other."""
    links_through_nodes: int
    """Link / node pairs where the link's curve passes over a node it is
    not attached to."""
    frame_overlaps: int
    """Pairs of frames that overlap without one being inside the other."""
    foreign_nodes_in_frames: int
    """Node / frame pairs where a node sits on a frame it is not in."""
    imbalance: float
    """How far, on average, a node with several inputs (or several outputs)
    is from the vertical middle of the nodes feeding it (fed by it)."""
    flow_links: int = 0
    """Links between two sockets carrying the tree's main data (geometry,
    shader, …): the trunk and its branches."""
    level_flow_links: int = 0
    """Those of them that are level. All of them, when the trunk is a row."""
    fork_imbalance: float = 0.0
    """Summed over the nodes where the main data forks (or merges): how far
    the socket the links fan out of (or into) is from the middle height of
    their other ends. Zero when every fork is symmetric."""
    flow_crossings: int = 0
    """Crossings between two links that both carry the main data. The
    easiest kind to read: branches of the trunk passing each other."""
    mixed_crossings: int = 0
    """Crossings between a link carrying the main data and one that does
    not: a value cutting across the trunk. The hardest kind to read."""

    zones: int = 0
    """Zones whose input node leads to their output node."""
    straight_zones: int = 0
    """Those of them drawn as a row: every link of the spine (the line of
    the main data from the zone's input node to its output node) straight."""
    foreign_nodes_in_zones: int = 0
    """Node / zone pairs where a node that is not in a zone sits in the
    box around the zone's nodes, and so on or inside its outline. (Not part
    of :meth:`cost`: keeping such nodes out costs more crossings than it
    is worth.)"""

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def aspect(self) -> float:
        """Width over height (0 for an empty tree)."""
        return self.width / self.height if self.height else 0.0

    @property
    def straightness(self) -> float:
        """Fraction of links that are straight (1 for a tree without links)."""
        return self.straight_links / self.links if self.links else 1.0

    def cost(self, weights: CostWeights | None = None) -> float:
        """One number for the layout's defects, weighted by *weights*."""
        w = weights or CostWeights()
        return (
            w.crossing * self.crossings
            + w.mixed_crossing * self.mixed_crossings
            + w.backward_link * self.backward_links
            + w.node_overlap * self.node_overlaps
            + w.link_through_node * self.links_through_nodes
            + w.frame_overlap * self.frame_overlaps
            + w.foreign_node_in_frame * self.foreign_nodes_in_frames
            + w.bent_zone * (self.zones - self.straight_zones)
            + w.bent_link * (self.links - self.level_links)
            + w.bent_flow_link * (self.flow_links - self.level_flow_links)
            + w.fork_imbalance * self.fork_imbalance
            + w.link_length * self.link_length
            + w.link_span_y * self.link_span_y
            + w.area * self.area
        )

    def as_dict(self, ndigits: int | None = 0) -> dict[str, float]:
        """The fields as a dict, floats rounded to *ndigits* (None: as is)."""
        values = asdict(self)
        if ndigits is None:
            return values
        return {
            k: round(v, ndigits) if isinstance(v, float) else v
            for k, v in values.items()
        }

    def summary(self) -> str:
        """A one-line digest, e.g. for a plot title."""
        return (
            f"{self.crossings} crossings · "
            f"{self.level_links}/{self.links} level · "
            f"{self.width:.0f}×{self.height:.0f}"
            + (f" · {self.node_overlaps} overlaps" if self.node_overlaps else "")
            + (
                f" · {self.links_through_nodes} through nodes"
                if self.links_through_nodes
                else ""
            )
            + (f" · {self.backward_links} backward" if self.backward_links else "")
        )

    @classmethod
    def field_names(cls) -> list[str]:
        return [f.name for f in fields(cls)]


# -------------------------------------------------------------------
# Geometry of a tree as laid out


def node_rect(node: bNode) -> Rect:
    """The box a node is drawn in. A reroute is a point."""
    if node.is_reroute():
        x, y = node.location
        return (x, y, x, y)
    return node.draw_bounds


def socket_anchor(socket: bNodeSocket) -> tuple[float, float]:
    """Where a link attaches to *socket*."""
    if socket.node.is_reroute():
        return socket.node.location
    assert socket.location is not None
    return socket.location


def frame_rects(tree: bNodeTree) -> dict[bNode, Rect]:
    """The box each frame is drawn in: around its members, padded, with room
    for its label. Empty frames have no box."""
    children: dict[bNode, list[bNode]] = {}
    for node in tree.nodes:
        if node.parent is not None:
            children.setdefault(node.parent, []).append(node)

    rects: dict[bNode, Rect] = {}

    def rect_of(frame: bNode) -> Rect | None:
        if frame in rects:
            return rects[frame]
        boxes = []
        for child in children.get(frame, ()):
            box = rect_of(child) if child.is_frame() else node_rect(child)
            if box is not None:
                boxes.append(box)
        if not boxes:
            return None
        padding = frame_padding()
        label_room = 0.0
        if frame.label:
            label_room = float(frame.label_size) + _FRAME_LABEL_PADDING
        rects[frame] = (
            min(b[0] for b in boxes) - padding,
            min(b[1] for b in boxes) - padding,
            max(b[2] for b in boxes) + padding,
            max(b[3] for b in boxes) + padding + label_room,
        )
        return rects[frame]

    for node in tree.nodes:
        if node.is_frame():
            rect_of(node)
    return rects


def _frames_around(node: bNode) -> set[bNode]:
    frames = set()
    parent = node.parent
    while parent is not None:
        frames.add(parent)
        parent = parent.parent
    return frames


def _rects_overlap(a: Rect, b: Rect, tol: float = _OVERLAP_TOL) -> bool:
    return (
        min(a[2], b[2]) - max(a[0], b[0]) > tol
        and min(a[3], b[3]) - max(a[1], b[1]) > tol
    )


def _link_curves(
    starts: NDArray[np.float64], ends: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Points along each link's curve, shape ``(links, points, 2)``. Blender
    draws a link as a Bézier leaving and entering its sockets horizontally."""
    dx = np.maximum(0.4 * np.abs(ends[:, 0] - starts[:, 0]), 12.0)
    handle = np.stack([dx, np.zeros_like(dx)], axis=1)
    p0, p3 = starts[:, None, :], ends[:, None, :]
    p1, p2 = p0 + handle[:, None, :], p3 - handle[:, None, :]
    t = np.linspace(0.0, 1.0, _CURVE_SEGMENTS + 1)[None, :, None]
    mt = 1.0 - t
    return mt**3 * p0 + 3 * mt**2 * t * p1 + 3 * mt * t**2 * p2 + t**3 * p3


def _cross(
    o: NDArray[np.float64], a: NDArray[np.float64], b: NDArray[np.float64]
) -> NDArray[np.float64]:
    return (a[..., 0] - o[..., 0]) * (b[..., 1] - o[..., 1]) - (
        a[..., 1] - o[..., 1]
    ) * (b[..., 0] - o[..., 0])


def _curves_cross(a: NDArray[np.float64], b: NDArray[np.float64]) -> bool:
    """Whether two curves (point arrays) cross somewhere. Meeting at a
    sample point counts (two mirrored links cross exactly there); lying
    along each other does not."""
    a0, a1 = a[:-1, None, :], a[1:, None, :]
    b0, b1 = b[None, :-1, :], b[None, 1:, :]
    d1 = _cross(a0, a1, b0)
    d2 = _cross(a0, a1, b1)
    d3 = _cross(b0, b1, a0)
    d4 = _cross(b0, b1, a1)
    collinear = (d1 == 0) & (d2 == 0) & (d3 == 0) & (d4 == 0)
    return bool(np.any((d1 * d2 <= 0) & (d3 * d4 <= 0) & ~collinear))


def _crossing_pairs(
    curves: NDArray[np.float64], sockets: list[tuple[bNodeSocket, bNodeSocket]]
) -> list[tuple[int, int]]:
    """The pairs of links (by index) whose curves cross."""
    n = len(curves)
    if n < 2:
        return []

    lo = curves.min(axis=1)
    hi = curves.max(axis=1)
    # Pairs of links whose bounding boxes overlap.
    apart = (
        (lo[:, None, 0] >= hi[None, :, 0])
        | (lo[None, :, 0] >= hi[:, None, 0])
        | (lo[:, None, 1] >= hi[None, :, 1])
        | (lo[None, :, 1] >= hi[:, None, 1])
    )
    candidates = np.argwhere(np.triu(~apart, k=1))

    pairs = []
    for i, j in candidates:
        from_i, to_i = sockets[i]
        from_j, to_j = sockets[j]
        # Links fanning out of (or into) one socket meet there, not cross;
        # so do the two links either side of a reroute.
        if from_i is from_j or to_i is to_j:
            continue
        ends_i, ends_j = curves[i][[0, -1]], curves[j][[0, -1]]
        if np.any(np.all(ends_i[:, None, :] == ends_j[None, :, :], axis=2)):
            continue
        if _curves_cross(curves[i], curves[j]):
            pairs.append((int(i), int(j)))
    return pairs


def _curve_hits_rects(
    curve: NDArray[np.float64], rects: NDArray[np.float64]
) -> NDArray[np.bool_]:
    """For each rect ``(xmin, ymin, xmax, ymax)``, whether any piece of the
    curve passes through its interior."""
    p = curve[:-1, None, :]
    d = curve[1:, None, :] - p
    lo = rects[None, :, 0:2]
    hi = rects[None, :, 2:4]

    with np.errstate(divide="ignore", invalid="ignore"):
        t0 = (lo - p) / d
        t1 = (hi - p) / d
    t_near = np.minimum(t0, t1)
    t_far = np.maximum(t0, t1)
    # A piece parallel to an axis either lies within that slab or misses it.
    parallel = d == 0
    inside = (p > lo) & (p < hi)
    t_near = np.where(parallel, np.where(inside, -np.inf, np.inf), t_near)
    t_far = np.where(parallel, np.where(inside, np.inf, -np.inf), t_far)

    enter = np.maximum(t_near.max(axis=2), 0.0)
    leave = np.minimum(t_far.min(axis=2), 1.0)
    return np.any(enter < leave, axis=0)


# -------------------------------------------------------------------


def measure(tree: bNodeTree | Any) -> LayoutMetrics:
    """Measure the layout *tree* currently has: plain data, or a Blender
    ``NodeTree`` (which is read into plain data first)."""
    if not isinstance(tree, bNodeTree):
        from .extract import extract

        tree = extract(tree)[0]

    nodes = [n for n in tree.nodes if not n.is_frame()]
    boxes = [n for n in nodes if not n.is_reroute()]
    rect_of = {n: node_rect(n) for n in nodes}
    frames = frame_rects(tree)

    # (from socket, to socket, from node, to node) of every valid link.
    links = [
        (link.fromsock, link.tosock, link.fromnode, link.tonode)
        for link in tree.links
        if link.is_valid
    ]
    sockets = [(from_socket, to_socket) for from_socket, to_socket, *_ in links]
    starts = np.array([socket_anchor(s) for s, _ in sockets], dtype=np.float64).reshape(
        -1, 2
    )
    ends = np.array([socket_anchor(t) for _, t in sockets], dtype=np.float64).reshape(
        -1, 2
    )
    delta = ends - starts
    straight = np.abs(delta[:, 1]) <= _STRAIGHT_TOL
    level_tops = np.array(
        [
            abs(rect_of[from_node][3] - rect_of[to_node][3]) <= _STRAIGHT_TOL
            for *_, from_node, to_node in links
        ],
        dtype=bool,
    )

    # -- extent -----------------------------------------------------
    extents = [*rect_of.values(), *frames.values()]
    if extents:
        width = max(r[2] for r in extents) - min(r[0] for r in extents)
        height = max(r[3] for r in extents) - min(r[1] for r in extents)
    else:
        width = height = 0.0

    # -- links ------------------------------------------------------
    curves = _link_curves(starts, ends)
    crossing_pairs = _crossing_pairs(curves, sockets)

    links_through_nodes = 0
    if boxes and links:
        # Shrink the boxes a little so a link skimming an edge doesn't count.
        shrink = np.array([1.0, 1.0, -1.0, -1.0]) * _OVERLAP_TOL
        box_rects = np.array([rect_of[n] for n in boxes], dtype=np.float64) + shrink
        index_of = {n: i for i, n in enumerate(boxes)}
        for (*_, from_node, to_node), curve in zip(links, curves):
            hits = _curve_hits_rects(curve, box_rects)
            for end in (from_node, to_node):
                if end in index_of:
                    hits[index_of[end]] = False
            links_through_nodes += int(hits.sum())

    # -- nodes and frames -------------------------------------------
    node_overlaps = sum(
        _rects_overlap(rect_of[a], rect_of[b]) for a, b in combinations(boxes, 2)
    )

    around = {n: _frames_around(n) for n in tree.nodes}
    frame_overlaps = sum(
        a not in around[b]
        and b not in around[a]
        and _rects_overlap(frames[a], frames[b])
        for a, b in combinations(frames, 2)
    )
    foreign_nodes_in_frames = sum(
        frame not in around[n] and _rects_overlap(rect_of[n], rect)
        for frame, rect in frames.items()
        for n in boxes
    )

    foreign_nodes_in_zones = 0
    for zone in tree.zones:
        members = set(zone.nodes())
        inside = [rect_of[n] for n in members if n in rect_of]
        if not inside:
            continue
        rect = (
            min(r[0] for r in inside) - _ZONE_PADDING,
            min(r[1] for r in inside) - _ZONE_PADDING,
            max(r[2] for r in inside) + _ZONE_PADDING,
            max(r[3] for r in inside) + _ZONE_PADDING,
        )
        foreign_nodes_in_zones += sum(
            n not in members and _rects_overlap(rect_of[n], rect) for n in boxes
        )

    zones = straight_zones = 0
    index_of_link = {(a, b): i for i, (a, b) in enumerate(sockets)}
    taken: set[bNodeLink] = set()
    for zone in reversed(tree.zones):
        spine = zone_spine(zone, tree, taken)
        taken.update(spine)
        if spine:
            zones += 1
            straight_zones += all(
                straight[index_of_link[link.fromsock, link.tosock]] for link in spine
            )

    # -- balance ----------------------------------------------------
    def middle(node: bNode) -> float:
        rect = rect_of[node]
        return (rect[1] + rect[3]) / 2

    def offsets_from_neighbours(
        linked: list[tuple[bNodeSocket, bNodeSocket, bNode, bNode]],
    ) -> list[float]:
        feeders: dict[bNode, dict[bNode, None]] = {}
        consumers: dict[bNode, dict[bNode, None]] = {}
        for *_, from_node, to_node in linked:
            feeders.setdefault(to_node, {})[from_node] = None
            consumers.setdefault(from_node, {})[to_node] = None
        return [
            abs(middle(node) - fmean(middle(n) for n in neighbours))
            for neighbourhood in (feeders, consumers)
            for node, neighbours in neighbourhood.items()
            if len(neighbours) > 1
        ]

    offsets = offsets_from_neighbours(links)

    # -- the main data ------------------------------------------------
    level = straight | level_tops
    # A reroute passes on whatever feeds it.
    feeds = {to_node: from_socket for from_socket, _, _, to_node in links}

    def carries_flow(socket: bNodeSocket) -> bool:
        seen = set()
        while socket.node.is_reroute() and socket.node not in seen:
            seen.add(socket.node)
            if socket.node not in feeds:
                return False
            socket = feeds[socket.node]
        return socket.idname in FLOW_SOCKETS

    is_flow = np.array(
        [
            carries_flow(from_socket)
            and (to_socket.node.is_reroute() or to_socket.idname in FLOW_SOCKETS)
            for from_socket, to_socket in sockets
        ],
        dtype=bool,
    )
    # A fork is symmetric when its links fan out evenly above and below the
    # socket they share: compare the heights of the two ends of the fan.
    fans_out: dict[bNode, list[int]] = {}
    fans_in: dict[bNode, list[int]] = {}
    for i, (*_, from_node, to_node) in enumerate(links):
        if is_flow[i]:
            fans_out.setdefault(from_node, []).append(i)
            fans_in.setdefault(to_node, []).append(i)
    flow_offsets = [
        abs(float(starts[fan, 1].mean() - ends[fan, 1].mean()))
        for fans, far_end in ((fans_out, 3), (fans_in, 2))
        for fan in fans.values()
        if len({links[i][far_end] for i in fan}) > 1
    ]

    return LayoutMetrics(
        nodes=len(nodes),
        reroutes=len(nodes) - len(boxes),
        links=len(links),
        width=float(width),
        height=float(height),
        crossings=len(crossing_pairs),
        backward_links=int(np.count_nonzero(delta[:, 0] < 0)),
        straight_links=int(np.count_nonzero(straight)),
        level_links=int(np.count_nonzero(level)),
        link_length=float(np.hypot(delta[:, 0], delta[:, 1]).sum()),
        link_span_y=float(np.abs(delta[:, 1]).sum()),
        node_overlaps=int(node_overlaps),
        links_through_nodes=links_through_nodes,
        frame_overlaps=int(frame_overlaps),
        foreign_nodes_in_frames=int(foreign_nodes_in_frames),
        imbalance=fmean(offsets) if offsets else 0.0,
        flow_links=int(np.count_nonzero(is_flow)),
        level_flow_links=int(np.count_nonzero(is_flow & level)),
        fork_imbalance=float(sum(flow_offsets)),
        flow_crossings=sum(bool(is_flow[i] and is_flow[j]) for i, j in crossing_pairs),
        mixed_crossings=sum(bool(is_flow[i] != is_flow[j]) for i, j in crossing_pairs),
        zones=zones,
        straight_zones=straight_zones,
        foreign_nodes_in_zones=int(foreign_nodes_in_zones),
    )
