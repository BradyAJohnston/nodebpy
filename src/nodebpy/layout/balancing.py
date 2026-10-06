# SPDX-License-Identifier: GPL-2.0-or-later
"""Shorten the tallest columns after ranking.

The ranking puts the nodes that feed a node in the column right before it,
so a node with many inputs gets one very tall column. While the tallest
column can be made shorter without making the drawing larger overall,
:func:`balance_column_heights` moves a node of that column one column to the
left, together with every node it depends on. That move is always feasible,
because nothing outside the moved set feeds it.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable

from .common import REROUTE_DIM, REROUTE_MARGIN_Y_FAC
from .config import LayoutState
from .digraph import LayoutGraph, Link, topological_sort
from .model import Cluster, Node, Socket

_MAX_MOVES = 500
_EPSILON = 1e-9


def _upstream_sets(G: LayoutGraph[Node]) -> dict[Node, set[Node]]:
    """For every node, every node it depends on."""
    upstream_of: dict[Node, set[Node]] = {}
    for v in topological_sort(G):
        upstream = set()
        for u in G.predecessors(v):
            upstream.add(u)
            upstream |= upstream_of[u]
        upstream_of[v] = upstream
    return {v: upstream_of[v] for v in G}


def _column_heights(
    G: LayoutGraph[Node], ranks: dict[Node, int], state: LayoutState
) -> dict[int, float]:
    """Estimated height of each column: its nodes with the vertical margin
    between them, plus a dummy node for every long link passing through.
    Long links leaving the same socket count once."""
    margin = state.margin.y
    heights: defaultdict[int, float] = defaultdict(float)
    counts: defaultdict[int, int] = defaultdict(int)
    for v, r in ranks.items():
        heights[r] += v.height
        counts[r] += 1
    crossings: defaultdict[int, set[Socket]] = defaultdict(set)
    for link in G.all_links():
        for r in range(ranks[link.fromnode] + 1, ranks[link.tonode]):
            crossings[r].add(link.fromsock)
    dummy_gap = margin * REROUTE_MARGIN_Y_FAC
    for r, sources in crossings.items():
        # Dummy nodes are spaced by the reroute gap (placement.vertical_gap).
        heights[r] += len(sources) * (REROUTE_DIM.y + dummy_gap)
    return {r: heights[r] + margin * max(counts[r] - 1, 0) for r in heights}


def _column_widths(ranks: dict[Node, int]) -> dict[int, float]:
    widths: defaultdict[int, float] = defaultdict(float)
    for v, r in ranks.items():
        widths[r] = max(widths[r], v.width)
    return widths


def _frame_sequence_ok(
    ranks: dict[Node, int],
    sequence: Iterable[tuple[frozenset[Node], frozenset[Node]]],
) -> bool:
    """Whether every constraint of *sequence* holds under *ranks*: every
    node of the first set is before every node of the second."""
    for before, after in sequence:
        if max(ranks[v] for v in before) >= min(ranks[v] for v in after):
            return False
    return True


def _overshoot(heights: dict[int, float], target: float) -> float:
    return sum(max(0.0, h - target) for h in heights.values())


def _fit_to_height(
    G: LayoutGraph[Node],
    ranks: dict[Node, int],
    target: float,
    state: LayoutState,
    upstream_of: dict[Node, set[Node]],
) -> dict[Node, int] | None:
    """Move nodes one column left, each with every node it depends on,
    until no column is taller than *target*. Each move is the one that
    leaves the least height above the target. Returns the new ranks, or
    None when no move helps or ``_MAX_MOVES`` is reached.

    A move is scored by the change it makes to the columns it touches,
    rather than by measuring every column again."""
    ranks = dict(ranks)
    sequence = state.frame_sequence
    margin = state.margin.y
    dummy = REROUTE_DIM.y + margin * REROUTE_MARGIN_Y_FAC
    links = list(G.all_links())
    links_of: defaultdict[Node, list[Link[Node]]] = defaultdict(list)
    for k in links:
        links_of[k.fromnode].append(k)
        links_of[k.tonode].append(k)

    for _ in range(_MAX_MOVES):
        node_height: defaultdict[int, float] = defaultdict(float)
        counts: defaultdict[int, int] = defaultdict(int)
        for v, r in ranks.items():
            node_height[r] += v.height
            counts[r] += 1
        # Per column, the sockets of the long links passing through, with
        # how many links each socket sends through. See _column_heights.
        passing: defaultdict[int, Counter[Socket]] = defaultdict(Counter)
        for k in links:
            for r in range(ranks[k.fromnode] + 1, ranks[k.tonode]):
                passing[r][k.fromsock] += 1

        def height(nodes: float, count: int, sources: int) -> float:
            return nodes + sources * dummy + margin * max(count - 1, 0)

        heights = {
            r: height(node_height[r], counts[r], len(passing[r]))
            for r in node_height.keys() | passing.keys()
        }
        current = _overshoot(heights, target)
        if current <= 0:
            return ranks

        best: tuple[float, set[Node]] | None = None
        for v, upstream in upstream_of.items():
            if not upstream or heights.get(ranks[v], 0.0) <= target:
                continue
            # A few parallel branches read best side by side.
            if counts[ranks[v]] <= BALANCE_MIN_COLUMN:
                continue
            moved = upstream | {v}
            if sequence:
                trial = {w: ranks[w] - (w in moved) for w in ranks}
                if not _frame_sequence_ok(trial, sequence):
                    continue

            # What the move changes, per column.
            d_height: defaultdict[int, float] = defaultdict(float)
            d_count: defaultdict[int, int] = defaultdict(int)
            d_passing: defaultdict[int, Counter[Socket]] = defaultdict(Counter)
            for w in moved:
                r = ranks[w]
                d_height[r] -= w.height
                d_height[r - 1] += w.height
                d_count[r] -= 1
                d_count[r - 1] += 1
            for k in {k for w in moved for k in links_of[w]}:
                a, b = ranks[k.fromnode], ranks[k.tonode]
                for r in range(a + 1, b):
                    d_passing[r][k.fromsock] -= 1
                a -= k.fromnode in moved
                b -= k.tonode in moved
                for r in range(a + 1, b):
                    d_passing[r][k.fromsock] += 1

            shoot = current
            for r in d_height.keys() | d_passing.keys():
                sources = len(passing[r])
                for socket, d in d_passing[r].items():
                    before = passing[r][socket]
                    sources += (before + d > 0) - (before > 0)
                new = height(
                    node_height[r] + d_height[r], counts[r] + d_count[r], sources
                )
                old = heights.get(r, 0.0)
                shoot += max(0.0, new - target) - max(0.0, old - target)
            # Summing changes leaves rounding noise that must not decide.
            if shoot < current - _EPSILON and (
                best is None or shoot < best[0] - _EPSILON
            ):
                best = (shoot, moved)

        if best is None:
            return None
        for w in best[1]:
            ranks[w] -= 1
    return None


_TARGET_STEP = 0.9


def _is_in(v: Node, cluster: Cluster) -> bool:
    """Whether *v* is in *cluster* or in a cluster within it."""
    c = v.cluster
    while c is not None:
        if c is cluster:
            return True
        c = c.cluster
    return False


BALANCE_ASPECT = 1.6
"""The shape balancing aims for: this wide for every unit of height."""

BALANCE_MIN_COLUMN = 4
"""A column of at most this many nodes is never split, so a few parallel
branches stay side by side."""


def balance_column_heights(
    G: LayoutGraph[Node],
    clusters: Iterable[Cluster],
    state: LayoutState,
) -> None:
    """Shorten the tallest columns by moving the chains that feed them left.

    Lowers a target height step by step from the tallest column. For each
    target, :func:`_fit_to_height` moves nodes out of the columns taller
    than it. Of the rankings found, the one that fits the smallest box of
    aspect ``BALANCE_ASPECT`` is kept. The search stops when a target cannot
    be met or the box grows. Frame-sequence constraints are kept throughout.
    """
    nodes = list(G)
    if not nodes:
        return
    ranks = {v: v.rank for v in nodes}
    margin_x = state.margin.x
    upstream_of = _upstream_sets(G)

    aspect = BALANCE_ASPECT

    def area(r: dict[Node, int]) -> float:
        """Height of the smallest box of the target aspect ratio that the
        drawing fits in: the larger of its height and its width divided by
        the aspect ratio."""
        heights = _column_heights(G, r, state)
        widths = _column_widths(r)
        width = sum(widths.values()) + margin_x * max(len(widths) - 1, 0)
        return max(max(heights.values()), width / aspect)

    best_ranks = ranks
    best_area = area(ranks)
    target = max(_column_heights(G, ranks, state).values()) * _TARGET_STEP
    floor = max(v.height for v in nodes)
    while target >= floor:
        fitted = _fit_to_height(G, best_ranks, target, state, upstream_of)
        if fitted is None:
            break
        fitted_area = area(fitted)
        if fitted_area > best_area:
            break
        best_ranks, best_area = fitted, fitted_area
        target = max(_column_heights(G, fitted, state).values()) * _TARGET_STEP

    offset = min(best_ranks.values())
    for v in nodes:
        v.rank = best_ranks[v] - offset
    # Keep each frame's border nodes just outside its nodes until
    # insert_dummy_nodes rebinds them.
    for c in clusters:
        members = [v for v in nodes if _is_in(v, c)]
        if members:
            c.left.rank = min(v.rank for v in members) - 1
            c.right.rank = max(v.rank for v in members) + 1
