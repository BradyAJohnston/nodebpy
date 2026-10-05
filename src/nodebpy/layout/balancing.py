# SPDX-License-Identifier: GPL-2.0-or-later
"""Height-balanced ranking.

Network-simplex ranking minimises total edge length, so every feeder sits in
the column right before its consumer. A node with many inputs — a big group
node taking a dozen values, switches and math results — therefore gets all
of its feeders stacked in one column, which grows far taller than any other
column while the columns further left stay nearly empty: the tree becomes a
tall sliver with dead space everywhere else.

:func:`balance_column_heights` post-processes the ranks: while the tallest
column can be made shorter without making the drawing larger overall, it
moves a node of that column one column to the left together with
everything upstream of it, which is always feasible (the moved set has no
predecessor outside itself). Links from the moved set to the nodes left
behind become one column longer and are routed through dummy nodes /
reroutes, which the height estimate charges for.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable

from .common import REROUTE_DIM, REROUTE_MARGIN_Y_FAC
from .config import LayoutState
from .digraph import LayoutGraph, ancestors
from .model import Cluster, Kind, Node, Socket

_MAX_MOVES = 500


def _upstream(G: LayoutGraph[Node], v: Node) -> set[Node]:
    """Every node *v* depends on. Moving *v* together with its upstream one
    column to the left is always feasible: the set has no predecessor
    outside itself, and links from it to nodes left behind only get
    longer."""
    return set(ancestors(G, v))


def _column_heights(
    G: LayoutGraph[Node], ranks: dict[Node, int], state: LayoutState
) -> dict[int, float]:
    """Estimated drawn height per rank: real nodes plus the dummy nodes of
    the long edges passing through, each separated by the vertical margin.
    Long edges leaving the same socket merge into one dummy chain."""
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
        # Dummy chains pack at the reduced reroute gap (see y_coords).
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
    """Whether every recorded frame-sequence constraint (all of unit *a*
    before all of unit *b*) still holds under *ranks*."""
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
    """Greedily move nodes (with their upstream) left until no column is
    taller than *target*; None when the greedy gets stuck first."""
    ranks = dict(ranks)
    sequence = state.frame_sequence
    for _ in range(_MAX_MOVES):
        heights = _column_heights(G, ranks, state)
        current = _overshoot(heights, target)
        if current <= 0:
            return ranks
        best: tuple[float, dict[Node, int]] | None = None
        sizes = Counter(ranks.values())
        for v, upstream in upstream_of.items():
            if not upstream or heights.get(ranks[v], 0.0) <= target:
                continue
            # A few parallel branches read best side by side.
            if sizes[ranks[v]] <= BALANCE_MIN_COLUMN:
                continue
            trial = dict(ranks)
            for w in upstream | {v}:
                trial[w] -= 1
            if not _frame_sequence_ok(trial, sequence):
                continue
            shoot = _overshoot(_column_heights(G, trial, state), target)
            if shoot < current and (best is None or shoot < best[0]):
                best = (shoot, trial)
        if best is None:
            return None
        ranks = best[1]
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
    """Shorten the tallest columns by promoting feeder chains left.

    Lowers a target height step by step from the current tallest column and
    for each target greedily moves nodes of over-tall columns — together
    with their upstream — one column to the left until every column
    fits (or gives up). Of the layouts found, the one needing the smallest
    screen-shaped box (``balance_aspect`` wide for every unit of height) is
    kept, so height is traded for width only while the drawing gets closer
    to that shape; the descent stops once fitting fails or the box starts
    growing again. Frame-sequence constraints are kept throughout.
    """
    nodes = [v for v in G if v.type != Kind.HORIZONTAL_BORDER]
    if not nodes:
        return
    ranks = {v: v.rank for v in nodes}
    margin_x = state.margin.x
    upstream_of = {v: _upstream(G, v) for v in nodes}

    aspect = BALANCE_ASPECT

    def area(r: dict[Node, int]) -> float:
        """Size of the drawing as the side of the screen-shaped box (of the
        target aspect ratio) it needs: the taller of its height and its
        width scaled down by the aspect ratio."""
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
    # Frame borders follow their members (recomputed by insert_dummy_nodes);
    # keep them consistent for anything reading them before that.
    for c in clusters:
        members = [v for v in nodes if _is_in(v, c)]
        if members:
            c.left.rank = min(v.rank for v in members) - 1
            c.right.rank = max(v.rank for v in members) + 1
