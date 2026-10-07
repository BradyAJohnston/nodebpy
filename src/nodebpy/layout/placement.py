"""The place phase: give every node its height (:func:`bk_assign_y_coords`).

Brandes and Köpf's method (below): each node is aligned with one neighbour
in the column before, forming *blocks* that share a height. The blocks are
then packed as close as the nodes above them allow. This is done four
times, aligning to either side and packing either way.

On ``model.Node``: ``col_index`` is a node's index in its column, kept by
:func:`index_columns`. ``root`` is the first node of a node's block and
``aligned`` the next one round it. ``sink`` and ``shift`` say which group of
blocks moves together and by how much. ``inner_shift`` is a node's offset
within its block: zero when tops are aligned, a socket's offset when
sockets are. See ``DESIGN.md``."""

# http://dx.doi.org/10.1007/3-540-45848-4_3
# http://dx.doi.org/10.1007/978-3-319-27261-0_12
# https://arxiv.org/abs/2008.01252

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Collection, Iterable, Iterator, Sequence
from itertools import pairwise
from math import ceil, floor, inf
from statistics import fmean
from typing import cast

from .common import GRID_SIZE, REROUTE_MARGIN_Y_FAC
from .config import LayoutState
from .digraph import DiGraph, LayoutGraph, Link, descendants
from .dna import bNodeSocket
from .model import Cluster, Kind, Node, NodePair, Socket, is_real, link_priority
from .priority import SPINE_MIN_PRIORITY, TRUNK_MIN_PRIORITY


def index_columns(columns: Iterable[Sequence[Node]]) -> None:
    """Give every node its ``col_index``. To be called again whenever the
    order within a column changes."""
    for col in columns:
        for i, v in enumerate(col):
            v.col_index = i


def marked_conflicts(
    G: LayoutGraph[Node],
    *,
    should_ensure_alignment: Callable[[Node], bool],
) -> set[frozenset[Node]]:
    """The links that the alignment must not use, each as the set of its
    two nodes. They are the links that cross the link between a node for
    which *should_ensure_alignment* holds and its first predecessor, so
    that this link can be aligned."""
    columns = G.columns
    marked_links = set()
    for i, col in enumerate(columns[1:], 1):
        k_0 = 0
        done = 0
        for upto, u in enumerate(col):
            if should_ensure_alignment(u):
                upper_nbr = next(iter(G.predecessors(u)))
                k_1 = upper_nbr.col_index
            elif u == col[-1]:
                k_1 = len(columns[i - 1]) - 1
            else:
                continue

            while done <= upto:
                v = col[done]
                done += 1

                if should_ensure_alignment(v):
                    continue

                for pred in G.predecessors(v):
                    k = pred.col_index
                    if k < k_0 or k > k_1:
                        marked_links.add(frozenset((pred, v)))

            k_0 = k_1

    return marked_links


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
    marked_links: Collection[frozenset[Node]],
    marked_nodes: set[Node],
    priorities: dict[bNodeSocket, int],
    min_level: int,
) -> None:
    """Align each node of *col* with at most one predecessor. See
    :func:`horizontal_alignment`."""
    # For each node, its predecessors top to bottom.
    candidates: list[list[_Candidate]] = []
    levels: set[int] = set()
    for v in col:
        preds = []
        for u in sorted(G.predecessors(v), key=lambda u: u.col_index):
            priority = 0
            if priorities:
                priority = max(
                    link_priority(link, priorities) for link in G.links_between(u, v)
                )
                levels.add(priority)
            preds.append((u.col_index, u, priority))
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
            if v.aligned != v or {u, v} in marked_links:
                continue

            if winners is not None and j not in winners[i]:
                continue

            # Alignments must not cross.
            if any((i - i_) * (j - j_) <= 0 for i_, j_ in aligned):
                continue

            if u.cluster != v.cluster and {u, v} & marked_nodes:
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
        # Several nodes may want the same predecessor, as the branches
        # leaving a fork do when seen from the far side. The middle one gets
        # it, so a fork sits level with its middle branch. The others take
        # what remains.
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
    marked_links: Collection[frozenset[Node]],
    marked_nodes: set[Node],
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
        _align_column(G, col, marked_links, marked_nodes, priorities, min_level)


def iter_block(start: Node) -> Iterator[Node]:
    """The nodes of the block *start* is in, from *start* round."""
    yield start
    w = start
    while (w := w.aligned) != start:
        yield w


def aligns_by_tops(
    G: LayoutGraph[Node], v: Node, w: Node, is_right: bool, state: LayoutState
) -> bool:
    """Whether *v* and *w*, linked from *v* to *w* in *G*, line up by their
    tops rather than by the sockets of their link.

    Never when one is a reroute. Along the spine of a zone always,
    regardless of size. Otherwise by ``socket_alignment``: always for
    ``"NONE"``, never for ``"FULL"``, and for ``"MODERATE"`` within one
    frame, between two plain nodes, where the right-hand node is the taller
    or the two are much the same height."""
    if v.is_reroute or w.is_reroute:
        return False

    priorities = state.socket_priority
    if priorities and any(
        link_priority(link, priorities) >= SPINE_MIN_PRIORITY
        for link in G.links_between(v, w)
    ):
        return True

    alignment = state.options.socket_alignment
    if alignment == "NONE":
        return True
    if alignment == "FULL":
        return False
    if v.cluster != w.cluster or Kind.STACK in {v.type, w.type}:
        return False

    right, left = (v, w) if is_right else (w, v)
    if right.height > left.height and not (
        left.node is not None and left.node.is_collapsed
    ):
        return True
    return abs(v.height - w.height) <= fmean((v.height, w.height)) / 2


def inner_shift(
    G: LayoutGraph[Node], is_right: bool, is_up: bool, state: LayoutState
) -> None:
    """Set every node's ``inner_shift``, its offset within its block. A node
    takes the offset of the node before it in the block when the two line
    up by their tops. Otherwise its offset makes the sockets of the link
    between them level."""
    for root in dict.fromkeys(v.root for v in G):
        for v, w in pairwise(iter_block(root)):
            if aligns_by_tops(G, v, w, is_right, state):
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


def separation(tall: Node, u: Node, w: Node, state: LayoutState) -> float:
    """How far apart the vertical neighbours *u* and *w* sit in a column:
    *tall*'s height (the one of them the packing direction counts) plus
    the margin, a fraction of it between two reroutes or dummy nodes
    (``REROUTE_MARGIN_Y_FAC``). With ``snap_to_grid`` it is rounded up to
    whole grid steps, except between two reroutes or dummy nodes, so that
    snapping moves a column as one."""
    tight = u.is_reroute and w.is_reroute
    distance = tall.height + state.margin.y * (REROUTE_MARGIN_Y_FAC if tight else 1)
    if state.options.snap_to_grid and not (
        tight and Kind.VERTICAL_BORDER not in (u.type, w.type)
    ):
        distance = ceil(distance / GRID_SIZE - 1e-6) * GRID_SIZE
    return distance


def place_block(v: Node, is_up: bool, state: LayoutState) -> None:
    """Place the block rooted at *v*, after the blocks it rests on."""
    # Each block yields the blocks that must be placed before it. An
    # explicit stack is used because such a chain can be as long as a column.
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
        i = w.col_index

        if i == 0:
            continue

        n = w.col[i - 1]
        u = n.root
        yield u

        if v.sink == v:
            v.sink = u.sink

        if v.sink == u.sink:
            delta_l = separation(n if is_up else w, n, w, state)
            s_b = u.y + n.inner_shift - w.inner_shift + delta_l
            v.y = s_b if initial else max(v.y, s_b)
            initial = False

    for w in iter_block(v):
        w.y = v.y
        w.sink = v.sink


def vertical_compaction(G: LayoutGraph[Node], is_up: bool, state: LayoutState) -> None:
    """Give every node a ``y``. Each block is placed against the blocks it
    rests on. Then each group of blocks that share a sink is moved as close
    to the neighbouring group as the gaps allow, and every node's
    ``inner_shift`` is added."""
    for v in G:
        if v.root == v:
            place_block(v, is_up, state)

    columns = G.columns
    # Per column (by index), the neighbouring pairs across two sink groups
    # that the lower node's sink belongs to.
    col_index = {id(col): i for i, col in enumerate(columns)}
    pairs_by_column: defaultdict[int, set[NodePair]] = defaultdict(set)

    for col in columns:
        for v, u in pairwise(reversed(col)):
            if u.sink != v.sink:
                pairs_by_column[col_index[id(v.sink.col)]].add((u, v))

    for i, col in enumerate(columns):
        if col[0].sink.shift == inf:
            col[0].sink.shift = 0

        for u, v in pairs_by_column[i]:
            delta_l = separation(u if is_up else v, u, v, state)
            s_c = v.y + v.inner_shift - u.y - u.inner_shift - delta_l
            u.sink.shift = min(u.sink.shift, v.sink.shift + s_c)

    for v in G:
        v.y += v.sink.shift + v.inner_shift


def get_merged_lines(lines: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    """The intervals *lines*, sorted, with those that overlap merged."""
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
    """Whether the nodes and frames directly in *cluster* leave a vertical
    gap wider than the margin between them."""
    lines = []
    for v in T.successors(cluster):
        if isinstance(v, Node):
            if v.type == Kind.VERTICAL_BORDER:
                continue
            line = (v.y, v.y + v.height) if is_up else (v.y - v.height, v.y)
        else:
            vertical_border_roots = {
                w.root
                for w in T.successors(v)
                if isinstance(w, Node) and w.type == Kind.VERTICAL_BORDER
            }
            # Usually two: the frame's upper borders are aligned in one
            # block and its lower ones in another. Where a border could not
            # be aligned with the rest there are more, and the outermost
            # two give the frame's extent.
            by_height = sorted(vertical_border_roots, key=lambda w: w.y)
            w, z = by_height[0], by_height[-1]
            line = (w.y, z.y + z.height) if is_up else (w.y - w.height, z.y)

        lines.append(line)

    merged = get_merged_lines(lines)
    return any(l2[0] - l1[1] > state.margin.y for l1, l2 in pairwise(merged))


def get_marked_nodes(
    T: DiGraph[Node | Cluster],
    old_marked_nodes: set[Node],
    is_up: bool,
    state: LayoutState,
) -> set[Node]:
    """The nodes the next alignment must not align with a node in another
    cluster. They are nodes directly in a frame whose contents were placed
    with a gap wider than the margin. Empty when no frame adds any."""
    marked_nodes = set()
    for cluster in T:
        if not isinstance(cluster, Cluster) or cluster.nesting_level != 1:
            continue

        below = descendants(T, cluster)
        descendant_clusters = [
            c for c in T if isinstance(c, Cluster) and (c is cluster or c in below)
        ]
        for nested_cluster in sorted(
            descendant_clusters, key=lambda c: c.nesting_level, reverse=True
        ):
            children = {
                v for v in T.successors(nested_cluster) if not isinstance(v, Cluster)
            }

            if children <= old_marked_nodes:
                continue

            if not has_large_gaps_in_frame(nested_cluster, T, is_up, state):
                continue

            if children & old_marked_nodes:
                marked_nodes.update(children)
                continue

            for root in dict.fromkeys(
                v.root
                for v in T.successors(nested_cluster)
                if not isinstance(v, Cluster)
            ):
                b = tuple(iter_block(root))
                for u, v in pairwise(b):
                    if (
                        u.is_reroute
                        and v.is_reroute
                        and u in children
                        and v in children
                    ):
                        break
                else:
                    marked_nodes.update(children.intersection(b))

    return marked_nodes


def line_up_runs(G: LayoutGraph[Node], layouts: list[list[float]]) -> None:
    """Shift the four layouts so they can be averaged. The least tall one is
    moved so that its lowest edge is at 0. Each other one is lined up with
    it, by the lowest edge for the layouts packed down and by the highest
    for those packed up."""

    def min_y(layout: Sequence[float]) -> float:
        return min([y - v.height for v, y in zip(G, layout)])

    smallest_layout = min(layouts, key=lambda layout: max(layout) - min_y(layout))

    movement = min_y(smallest_layout)
    for i in range(len(smallest_layout)):
        smallest_layout[i] -= movement

    for i, layout in enumerate(layouts):
        if layout is smallest_layout:
            continue

        is_up = i % 2 == 1
        func = max if is_up else min_y
        movement = func(smallest_layout) - func(layout)
        for j in range(len(layout)):
            layout[j] += movement


_ITER_LIMIT = 20
_DIRECTIONS = {
    "RIGHT_DOWN": (False, False),
    "RIGHT_UP": (False, True),
    "LEFT_DOWN": (True, False),
    "LEFT_UP": (True, True),
}
"""Each direction as (aligned to the right, packed up)."""


def _align_and_pack(
    G: LayoutGraph[Node],
    T: DiGraph[Node | Cluster],
    marked_links: set[frozenset[Node]],
    is_right: bool,
    is_up: bool,
    state: LayoutState,
) -> list[float]:
    """One of the four runs: align, shift and pack, repeated, at most
    ``_ITER_LIMIT`` times, while :func:`get_marked_nodes` finds frames with
    gaps. Returns the ``y`` of every node of *G*, as if packed down."""
    priorities = state.socket_priority
    marked_nodes: set[Node] = set()
    for _ in range(_ITER_LIMIT):
        horizontal_alignment(
            G, marked_links, marked_nodes, priorities, TRUNK_MIN_PRIORITY
        )
        inner_shift(G, is_right, is_up, state)
        vertical_compaction(G, is_up, state)

        if new_marked_nodes := get_marked_nodes(T, marked_nodes, is_up, state):
            marked_nodes.update(new_marked_nodes)
            for v in G:
                v.bk_reset()
        else:
            break
    layout = [-v.y if is_up else v.y for v in G]
    for v in G:
        v.bk_reset()
    return layout


def bk_assign_y_coords(
    G: LayoutGraph[Node], T: DiGraph[Node | Cluster], state: LayoutState
) -> None:
    """Give every node its ``y``, the height of its top edge.

    Aligns and packs with the neighbours to the left or to the right,
    packing up or down (:func:`_align_and_pack`). The result is the run
    ``options.direction`` names, then the only one made, or for
    ``"BALANCED"`` the mean of the two middle values of the four runs for
    each node."""
    columns = G.columns
    for col in columns:
        col.reverse()
    index_columns(columns)

    def is_incident_to_inner_segment(v: Node) -> bool:
        return v.is_reroute and any(u.is_reroute for u in G.predecessors(v))

    def is_incident_to_vertical_border(v: Node) -> bool:
        return v.type == Kind.VERTICAL_BORDER and bool(G.predecessors(v))

    marked_links = marked_conflicts(
        G, should_ensure_alignment=is_incident_to_inner_segment
    )
    marked_links |= marked_conflicts(
        G, should_ensure_alignment=is_incident_to_vertical_border
    )

    direction = state.options.direction
    wanted = (
        set(_DIRECTIONS.values())
        if direction == "BALANCED"
        else {_DIRECTIONS[direction]}
    )
    layouts = []
    for is_right in (False, True):
        G = G.reversed()
        columns.reverse()
        for is_up in (False, True):
            if (is_right, is_up) in wanted:
                layouts.append(
                    _align_and_pack(G, T, marked_links, is_right, is_up, state)
                )
            for col in columns:
                col.reverse()
            index_columns(columns)

    for col in columns:
        col.reverse()
    index_columns(columns)

    if direction == "BALANCED":
        line_up_runs(G, layouts)
        for i, v in enumerate(G):
            values = sorted(layout[i] for layout in layouts)
            v.y = fmean(values[1:3])
    else:
        for v, y in zip(G, layouts[0]):
            v.y = y


_PULL_ROUNDS = 10


def pull_feeders(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Move each feeder level with the node it feeds, as far as its column
    allows.

    A feeder is a node of the tree whose links all go to one other node.
    The placement aligns nothing with it, so each of the four runs packs
    it to one edge of its column and the balanced height leaves it part of
    the way to that node. Here it is moved towards the height that makes
    its link straight, or its top level with the other node's where the
    two line up by tops, but not past the nodes above and below it in its
    column. Rounds are repeated while anything moves, as one feeder moving
    can make room for another."""
    index_columns(G.columns)
    feeders: list[tuple[Node, Node, list[Link[Node]]]] = []
    for v in G:
        if not is_real(v) or v.is_reroute:
            continue
        links = [*G.in_links(v), *G.out_links(v)]
        others = {k.fromnode if k.tonode is v else k.tonode for k in links}
        if len(others) == 1:
            feeders.append((v, others.pop(), links))

    def wanted(v: Node, other: Node, links: list[Link[Node]]) -> float:
        left, right = (v, other) if v.rank < other.rank else (other, v)
        if aligns_by_tops(G, left, right, False, state):
            return other.y
        heights = []
        for k in links:
            p, q = (k.fromsock, k.tosock) if k.fromnode is v else (k.tosock, k.fromsock)
            heights.append(other.y + q._offset_y - p._offset_y)
        return fmean(heights)

    for _ in range(_PULL_ROUNDS):
        moved = False
        for v, other, links in feeders:
            col, i = v.col, v.col_index
            # Never closer to a neighbour than the placement puts them, and
            # never further from the target than now.
            highest = (
                max(v.y, col[i - 1].y - separation(col[i - 1], col[i - 1], v, state))
                if i > 0
                else inf
            )
            lowest = (
                min(v.y, col[i + 1].y + separation(v, v, col[i + 1], state))
                if i + 1 < len(col)
                else -inf
            )
            y = min(max(wanted(v, other, links), lowest), highest)
            if abs(y - v.y) > 1e-6:
                v.y = y
                moved = True
        if not moved:
            break
