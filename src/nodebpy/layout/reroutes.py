# SPDX-License-Identifier: GPL-2.0-or-later
"""Dummy nodes after the placement: dropping the ones that are not wanted
(:func:`dissolve_dummy_nodes`, :func:`dissolve_clear_dummy_nodes`) and
lining the rest up with the sockets they join
(:func:`align_reroutes_with_sockets`)."""

from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise

from .common import segments_intersect
from .digraph import LayoutGraph
from .edits import RemoveLink
from .long_links import get_reroute_paths
from .model import (
    ClusterGraph,
    Kind,
    Node,
    Socket,
    is_real,
)


def dissolve_dummy_nodes(CG: ClusterGraph) -> None:
    """Remove every dummy node, linking the source of each chain straight
    to what the chain feeds."""
    paths = get_reroute_paths(
        CG,
        lambda v: v.is_reroute and not is_real(v),
        preserve_reroute_clusters=False,
    )
    G = CG.G
    for path in paths:
        if G.predecessors(path[0]):
            first = next(G.in_links(path[0]))
            u, o = first.fromnode, first.fromsock
            succ_inputs = [link.tosock for link in G.out_links(path[-1])]
            for i in succ_inputs:
                G.add_link(u, i.owner, o, i)

        CG.remove_nodes_from(path)


_CURVE_PIECES = 12


_CLEARANCE = 4.0


def _link_curve(
    start: tuple[float, float], end: tuple[float, float]
) -> list[tuple[float, float]]:
    """Points along a link as Blender draws it: a Bézier leaving and
    entering its sockets horizontally."""
    (x0, y0), (x3, y3) = start, end
    handle = max(0.4 * abs(x3 - x0), 12.0)
    x1, x2 = x0 + handle, x3 - handle
    points = []
    for k in range(_CURVE_PIECES + 1):
        t = k / _CURVE_PIECES
        s = 1.0 - t
        a, b, c, d = s**3, 3 * s**2 * t, 3 * s * t**2, t**3
        points.append((a * x0 + b * x1 + c * x2 + d * x3, (a + b) * y0 + (c + d) * y3))
    return points


def link_is_clear(start: Socket, end: Socket, obstacles: Sequence[Node]) -> bool:
    """Whether a link drawn straight from *start* to *end* passes clear of
    every node in *obstacles* (other than the two it joins)."""
    curve = _link_curve((start.x, start.y), (end.x, end.y))
    left = min(x for x, _ in curve)
    right = max(x for x, _ in curve)
    low = min(y for _, y in curve)
    high = max(y for _, y in curve)
    for v in obstacles:
        if v is start.owner or v is end.owner:
            continue
        xmin, xmax = v.x - _CLEARANCE, v.x + v.width + _CLEARANCE
        ymin, ymax = v.y - v.height - _CLEARANCE, v.y + _CLEARANCE
        if xmax < left or xmin > right or ymax < low or ymin > high:
            continue
        corners = ((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax))
        for p, q in pairwise(curve):
            if xmin < p[0] < xmax and ymin < p[1] < ymax:
                return False
            for i in range(4):
                if segments_intersect(p, q, corners[i], corners[i - 3]):
                    return False
    return True


def dissolve_clear_dummy_nodes(CG: ClusterGraph) -> None:
    """Take long links off their dummy nodes again wherever the link drawn
    straight would pass clear of every node, so that only the links that
    need routing around something end up with reroutes."""
    G = CG.G
    obstacles = [v for v in G if not v.is_reroute]
    paths = get_reroute_paths(
        CG,
        lambda v: v.is_reroute and not is_real(v),
        preserve_reroute_clusters=False,
    )
    for path in paths:
        # A chain of dummy nodes always has a link into it.
        output = next(G.in_links(path[0])).fromsock
        inputs = [link.tosock for link in G.out_links(path[-1])]
        if not all(link_is_clear(output, i, obstacles) for i in inputs):
            continue
        for i in inputs:
            G.add_link(output.owner, i.owner, output, i)
            # The tree keeps its own link, so drop the edit that removes it.
            edit = RemoveLink(output.dna, i.dna)
            if edit in CG.state.edits:
                CG.state.edits.remove(edit)
        CG.remove_nodes_from(path)


def get_foreign_sockets_of(path: Sequence[Node], G: LayoutGraph[Node]) -> list[Socket]:
    """The sockets outside the chain *path* that it is linked to: the
    outputs that feed its first node, then the inputs its last node feeds."""
    inputs = [link.fromsock for link in G.in_links(path[0])]
    outputs = [link.tosock for link in G.out_links(path[-1])]
    return inputs + outputs


def align_reroutes_with_sockets(CG: ClusterGraph) -> None:
    """Move each level chain of reroutes and dummy nodes up or down to the
    height of a socket it joins, where the nodes above and below it leave
    room. The sockets are tried in turn: those of other reroutes first,
    then the nearest. A chain moved level with another chain's socket is
    joined to that chain, and the two then move as one."""
    reroute_paths: dict[tuple[Node, ...], list[Socket]] = {}
    # Border nodes of frames have ``is_reroute`` set, but have nothing to
    # align to.
    for p in get_reroute_paths(
        CG,
        lambda v: v.type != Kind.VERTICAL_BORDER,
        preserve_reroute_clusters=False,
        aligned=True,
        linear=False,
    ):
        reroute_paths[tuple(p)] = get_foreign_sockets_of(p, CG.G)

    reroute_path_of = {v: p for p in reroute_paths for v in p}

    while True:
        changed = False
        for p1, foreign_sockets in tuple(reroute_paths.items()):
            if p1 not in reroute_paths:
                continue

            y = p1[0].y
            foreign_sockets.sort(key=lambda s: abs(y - s.y))
            foreign_sockets.sort(key=lambda s: y == s.owner.y, reverse=True)
            foreign_sockets.sort(key=lambda s: s.owner.is_reroute, reverse=True)

            if not foreign_sockets or y == foreign_sockets[0].y:
                del reroute_paths[p1]
                continue

            movement = y - foreign_sockets[0].y
            y -= movement
            if movement < 0:
                above_y_vals = [
                    (n := v.col[v.col.index(v) - 1]).y - n.height
                    for v in p1
                    if v != v.col[0]
                ]
                if above_y_vals and y > min(above_y_vals) - CG.state.margin.y:
                    continue
            else:
                below_y_vals = [
                    v.col[v.col.index(v) + 1].y for v in p1 if v != v.col[-1]
                ]
                if (
                    below_y_vals
                    and max(below_y_vals) + CG.state.margin.y > y - p1[0].height
                ):
                    continue

            for v in p1:
                v.y -= movement

            w = foreign_sockets[0].owner
            if w.is_reroute:
                p2 = reroute_path_of[w]
                p3 = p1 + p2 if w.rank > p1[-1].rank else p2 + p1
                reroute_paths[p3] = get_foreign_sockets_of(p3, CG.G)
                del reroute_paths[p1]
                reroute_paths.pop(p2, None)
                for v in p3:
                    reroute_path_of[v] = p3

            changed = True

        if not changed:
            if reroute_paths:
                for foreign_sockets in reroute_paths.values():
                    del foreign_sockets[0]
            else:
                break
