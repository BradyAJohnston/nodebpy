# SPDX-License-Identifier: GPL-2.0-or-later

# http://dx.doi.org/10.1007/3-540-45848-4_3
# http://dx.doi.org/10.1007/978-3-319-27261-0_12
# https://arxiv.org/abs/2008.01252

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Collection, Iterable, Iterator, Sequence
from itertools import pairwise
from math import ceil, floor, inf
from statistics import fmean
from typing import Any, cast

from ..config import LayoutState
from ..dna import bNodeSocket
from .digraph import DiGraph, LayoutGraph, descendants
from .graph import Cluster, Edge, Kind, Node, Socket, link_priority
from .pipeline import Layout, register
from .priority import SPINE_MIN_PRIORITY, TRUNK_MIN_PRIORITY


def marked_conflicts(
    G: LayoutGraph[Node],
    *,
    should_ensure_alignment: Callable[[Node], Any],
) -> set[frozenset[Node]]:
    columns = G.columns
    marked_edges = set()
    for i, col in enumerate(columns[1:], 1):
        k_0 = 0
        link = 0
        for link_1, u in enumerate(col):
            if should_ensure_alignment(u):
                upper_nbr = next(iter(G.predecessors(u)))
                k_1 = upper_nbr.col.index(upper_nbr)
            elif u == col[-1]:
                k_1 = len(columns[i - 1]) - 1
            else:
                continue

            while link <= link_1:
                v = col[link]
                link += 1

                if should_ensure_alignment(v):
                    continue

                for pred in G.predecessors(v):
                    k = pred.col.index(pred)
                    if k < k_0 or k > k_1:
                        marked_edges.add(frozenset((pred, v)))

            k_0 = k_1

    return marked_edges


def _medians[T](items: Sequence[T]) -> Sequence[T]:
    """The middle item, or the middle two of an even number."""
    m = (len(items) - 1) / 2
    return items[floor(m) : ceil(m) + 1]


type _Candidate = tuple[int, Node, int]
"""A predecessor a node could align with: its index in its column, the
predecessor, and the priority of the link from it."""


def _align_column(
    G: LayoutGraph[Node],
    col: Sequence[Node],
    marked_edges: Collection[frozenset[Node]],
    marked_nodes: Collection[Node],
    priorities: dict[bNodeSocket, int],
    min_level: int,
) -> None:
    # For each node, its predecessors top to bottom.
    candidates: list[list[_Candidate]] = []
    levels: set[int] = set()
    for v in col:
        preds = []
        for u in sorted(G.predecessors(v), key=lambda u: u.col.index(u)):
            priority = 0
            if priorities:
                priority = max(
                    link_priority(link, priorities) for link in G.links_between(u, v)
                )
                levels.add(priority)
            preds.append((u.col.index(u), u, priority))
        candidates.append(preds)

    # (index of predecessor, index of node) of the alignments made.
    aligned: list[tuple[int, int]] = []

    def align(
        j: int,
        v: Node,
        options: Sequence[_Candidate],
        winners: dict[int, Sequence[int]] | None = None,
    ) -> None:
        for i, u, _ in options:
            if v.aligned != v or {u, v} in marked_edges:
                continue

            if winners is not None and j not in winners[i]:
                continue

            # Alignments must not cross.
            if any((i - i_) * (j - j_) <= 0 for i_, j_ in aligned):
                continue

            if u.cluster != v.cluster and {u, v} & marked_nodes:  # type: ignore
                continue

            u.aligned = v
            v.root = u.root
            v.aligned = v.root
            aligned.append((i, j))

    # Links that carry the tree's main data first, heaviest first.
    for level in sorted((p for p in levels if p >= min_level), reverse=True):
        options = [
            _medians([c for c in preds if c[2] == level]) for preds in candidates
        ]
        # Several nodes may want the same predecessor (the branches leaving
        # a fork, seen from the far side). The middle one gets it, so a fork
        # sits level with its middle branch rather than its first; whoever
        # is left over takes what remains.
        claims: defaultdict[int, list[int]] = defaultdict(list)
        for j, v in enumerate(col):
            if v.aligned == v:
                for i, _, _ in options[j]:
                    claims[i].append(j)
        winners = {i: _medians(claimants) for i, claimants in claims.items()}
        for j, v in enumerate(col):
            align(j, v, options[j], winners)
        for j, v in enumerate(col):
            align(j, v, options[j])

    # Then every node still unaligned, with a median predecessor.
    for j, v in enumerate(col):
        align(j, v, _medians(candidates[j]))


def horizontal_alignment(
    G: LayoutGraph[Node],
    marked_edges: Collection[frozenset[Node]],
    marked_nodes: Collection[Node],
    priorities: dict[bNodeSocket, int],
    min_level: int = 1,
) -> None:
    """Align each node with one of its predecessors, forming the blocks
    that are placed as straight lines.

    A node aligns with a median predecessor. With *priorities* (see
    :mod:`.priority`), predecessors linked by a link of priority *min_level*
    or more are tried first, heaviest first, so a trunk stays straight
    where a side chain would otherwise claim the alignment.
    """
    for col in G.columns:
        _align_column(G, col, marked_edges, marked_nodes, priorities, min_level)


def iter_block(start: Node) -> Iterator[Node]:
    yield start
    w = start
    while (w := w.aligned) != start:
        yield w


def should_use_inner_shift(
    v: Node, w: Node, is_right: bool, state: LayoutState
) -> bool:
    if v.is_reroute or w.is_reroute:
        return True

    if state.settings.socket_alignment == "NONE":
        return False

    if state.settings.socket_alignment == "FULL":
        return True

    if v.cluster != w.cluster or Kind.STACK in {v.type, w.type}:
        return True

    if not is_right:
        v, w = w, v

    if v.height > w.height and not (w.node is not None and w.node.is_collapsed):
        return False

    return abs(v.height - w.height) > fmean((v.height, w.height)) / 2


def inner_shift(
    G: LayoutGraph[Node], is_right: bool, is_up: bool, state: LayoutState
) -> None:
    priorities = state.socket_priority
    for root in dict.fromkeys(v.root for v in G):
        for v, w in pairwise(iter_block(root)):
            # The nodes along the spine of a zone have their tops level
            # whatever their sizes (nodebpy addition).
            on_spine = (
                bool(priorities)
                and not (v.is_reroute or w.is_reroute)
                and any(
                    link_priority(link, priorities) >= SPINE_MIN_PRIORITY
                    for link in G.links_between(v, w)
                )
            )
            if on_spine or not should_use_inner_shift(v, w, is_right, state):
                w.inner_shift = v.inner_shift
                continue

            inner_shifts = []
            for link in G.links_between(v, w):
                p: Socket = link.fromsock
                q: Socket = link.tosock
                if p.owner != v:
                    p, q = q, p

                if is_up:
                    inner_shifts.append(v.inner_shift - p._offset_y + q._offset_y)
                else:
                    inner_shifts.append(v.inner_shift + p._offset_y - q._offset_y)

            w.inner_shift = fmean(inner_shifts)


def vertical_gap(u: Node, w: Node, state: LayoutState) -> float:
    """Margin between two vertically adjacent nodes of a column (nodebpy
    divergence): consecutive reroutes / dummy nodes — the bundles of long
    links routed past a column — pack much tighter than nodes, as reroute
    dots do in hand-made trees, so a fan-in of many long links no longer
    costs a node's height per link."""
    if u.is_reroute and w.is_reroute:
        return state.margin.y * state.settings.reroute_margin_y_fac
    return state.margin.y


def place_block(v: Node, is_up: bool, state: LayoutState) -> None:
    """Place the block rooted at *v*, after the blocks it rests on."""
    # Each block yields the blocks that must be placed before it goes on;
    # an explicit stack, since such a chain can be as long as a column.
    stack = [_place_block(v, is_up, state)]
    while stack:
        below = next(stack[-1], None)
        if below is None:
            stack.pop()
        else:
            stack.append(_place_block(below, is_up, state))


def _place_block(v: Node, is_up: bool, state: LayoutState) -> Iterator[Node]:
    if cast(float | None, v.y) is not None:
        return

    v.y = 0
    initial = True
    for w in iter_block(v):
        i = w.col.index(w)

        if i == 0:
            continue

        n = w.col[i - 1]
        u = n.root
        yield u

        if v.sink == v:
            v.sink = u.sink

        if v.sink == u.sink:
            gap = vertical_gap(n, w, state)
            delta_l = n.height + gap if is_up else w.height + gap
            s_b = u.y + n.inner_shift - w.inner_shift + delta_l
            v.y = s_b if initial else max(v.y, s_b)
            initial = False

    for w in iter_block(v):
        w.y = v.y
        w.sink = v.sink


def vertical_compaction(G: LayoutGraph[Node], is_up: bool, state: LayoutState) -> None:
    for v in G:
        if v.root == v:
            place_block(v, is_up, state)

    columns = G.columns
    neighborings: defaultdict[tuple[Node, ...], set[Edge]] = defaultdict(set)

    for col in columns:
        for v, u in pairwise(reversed(col)):
            if u.sink != v.sink:
                neighborings[tuple(v.sink.col)].add((u, v))

    for col in columns:
        if col[0].sink.shift == inf:
            col[0].sink.shift = 0

        for u, v in neighborings[tuple(col)]:
            gap = vertical_gap(u, v, state)
            delta_l = u.height + gap if is_up else v.height + gap
            s_c = v.y + v.inner_shift - u.y - u.inner_shift - delta_l
            u.sink.shift = min(u.sink.shift, v.sink.shift + s_c)

    for v in G:
        v.y += v.sink.shift + v.inner_shift


def get_merged_lines(lines: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    merged = []
    for line in sorted(lines, key=lambda line: line[0]):
        if merged and merged[-1][1] >= line[0]:
            a, b = merged[-1]
            merged[-1] = (a, max(b, line[1]))
        else:
            merged.append(line)

    return merged


def has_large_gaps_in_frame(
    cluster: Cluster, T: DiGraph[Cluster | Node], is_up: bool, state: LayoutState
) -> bool:
    lines = []
    for v in T.successors(cluster):
        if v.type == Kind.VERTICAL_BORDER:
            continue

        if v.type != Kind.CLUSTER:
            line = (v.y, v.y + v.height) if is_up else (v.y - v.height, v.y)
        else:
            vertical_border_roots = {
                w.root for w in T.successors(v) if w.type == Kind.VERTICAL_BORDER
            }
            # Usually two: the frame's upper borders are aligned in one
            # block and its lower ones in another. Where a border could not
            # be aligned with the rest there are more, and the outermost
            # two give the frame's extent. (nodebpy divergence: upstream
            # assumes exactly two.)
            by_height = sorted(vertical_border_roots, key=lambda w: w.y)
            w, z = by_height[0], by_height[-1]
            line = (w.y, z.y + z.height) if is_up else (w.y - w.height, z.y)

        lines.append(line)

    merged = get_merged_lines(lines)
    return any(l2[0] - l1[1] > state.margin.y for l1, l2 in pairwise(merged))


def get_marked_nodes(
    G: LayoutGraph[Node],
    T: DiGraph[Node | Cluster],
    old_marked_nodes: set[Node],
    is_up: bool,
    state: LayoutState,
) -> set[Node]:
    marked_nodes = set()
    for cluster in T:
        if not isinstance(cluster, Cluster) or cluster.nesting_level != 1:
            continue

        below = descendants(T, cluster)
        descendant_clusters = [
            c for c in T if isinstance(c, Cluster) and (c is cluster or c in below)
        ]
        for nested_cluster in sorted(
            descendant_clusters,
            key=lambda c: cast(int, c.nesting_level),
            reverse=True,
        ):
            children = {
                v for v in T.successors(nested_cluster) if v.type != Kind.CLUSTER
            }

            if children <= old_marked_nodes:
                continue

            if not has_large_gaps_in_frame(nested_cluster, T, is_up, state):
                continue

            if children & old_marked_nodes:
                marked_nodes.update(children)
                continue

            for root in dict.fromkeys(
                v.root for v in T.successors(nested_cluster) if v.type != Kind.CLUSTER
            ):
                b = tuple(iter_block(root))
                for u, v in pairwise(b):
                    if (
                        u.is_reroute
                        and v.is_reroute
                        and (u in children != v in children)
                    ):
                        break
                else:
                    marked_nodes.update(children.intersection(b))

    return marked_nodes


def balance(G: LayoutGraph[Node], layouts: list[list[float]]) -> None:
    def min_y(layout: Sequence[float]) -> float:
        return min([y - v.height for v, y in zip(G, layout)])

    smallest_layout = min(layouts, key=lambda layout: max(layout) - min_y(layout))

    movement = min_y(smallest_layout)
    for i in range(len(smallest_layout)):
        smallest_layout[i] -= movement

    for i, layout in enumerate(layouts):
        if layout == smallest_layout:
            continue

        func = min_y if i % 2 != 1 else max
        movement = func(smallest_layout) - func(layout)
        for j in range(len(layout)):
            layout[j] += movement


_ITER_LIMIT = 20
_DIRECTION_TO_IDX = {"RIGHT_DOWN": 0, "RIGHT_UP": 1, "LEFT_DOWN": 2, "LEFT_UP": 3}


def bk_assign_y_coords(
    G: LayoutGraph[Node], T: DiGraph[Node | Cluster], state: LayoutState
) -> None:
    columns = G.columns
    for col in columns:
        col.reverse()

    def is_incident_to_inner_segment(v):
        return v.is_reroute and any(u.is_reroute for u in G.predecessors(v))

    def is_incident_to_vertical_border(v):
        return v.type == Kind.VERTICAL_BORDER and G.predecessors(v)

    marked_edges = marked_conflicts(
        G, should_ensure_alignment=is_incident_to_inner_segment
    )
    marked_edges |= marked_conflicts(
        G, should_ensure_alignment=is_incident_to_vertical_border
    )

    priorities = state.socket_priority
    layouts = []
    for dir_x in (-1, 1):
        G = G.reversed()
        columns.reverse()
        for dir_y in (-1, 1):
            i = 0
            marked_nodes = set()
            is_up = dir_y == 1
            while i < _ITER_LIMIT:
                i += 1
                horizontal_alignment(
                    G,
                    marked_edges,
                    marked_nodes,
                    priorities,
                    TRUNK_MIN_PRIORITY,
                )
                inner_shift(G, dir_x == 1, is_up, state)
                vertical_compaction(G, is_up, state)

                if new_marked_nodes := get_marked_nodes(
                    G, T, marked_nodes, is_up, state
                ):
                    marked_nodes.update(new_marked_nodes)
                    for v in G:
                        v.bk_reset()
                else:
                    break
            layouts.append([v.y * -dir_y for v in G])

            for v in G:
                v.bk_reset()

            for col in columns:
                col.reverse()

    for col in columns:
        col.reverse()

    if state.settings.direction == "BALANCED":
        balance(G, layouts)
        for i, v in enumerate(G):
            values = [layout[i] for layout in layouts]
            values.sort()
            v.y = fmean(values[1:3])
    else:
        i = _DIRECTION_TO_IDX[state.settings.direction]
        for v, y in zip(G, layouts[i]):
            v.y = y


@register("place", "brandes_koepf")
def place_brandes_koepf(layout: Layout) -> None:
    """Align each node with a median neighbour into straight blocks, then
    pack the blocks (Brandes & Köpf)."""
    bk_assign_y_coords(layout.G, layout.T, layout.state)
