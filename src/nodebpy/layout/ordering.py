"""The order phase: order the nodes within each column so that few links
cross (:func:`minimize_crossings`).

Sweeps over the columns, ordering each by where its nodes' neighbours are
in the column before (the barycenter heuristic, per socket, with a frame's
nodes kept together), then swaps neighbours where that helps, and counts
crossings exactly to keep the best order. See ``DESIGN.md``. The papers the
sweep follows:"""

# https://link.springer.com/chapter/10.1007/3-540-36151-0_26
# https://doi.org/10.1016/j.jvlc.2013.11.005
# https://doi.org/10.1007/978-3-642-11805-0_14
# https://link.springer.com/chapter/10.1007/978-3-540-31843-9_22
# https://doi.org/10.7155/jgaa.00088

from __future__ import annotations

from bisect import bisect_right, insort
from collections import defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Iterator, Sequence
from dataclasses import dataclass, replace
from functools import cache
from itertools import chain, pairwise
from math import inf
from operator import itemgetter
from statistics import fmean
from typing import cast

from .config import LayoutState
from .digraph import (
    DiGraph,
    LayoutGraph,
    ancestors,
    bfs_edges,
    descendants,
    topological_sort,
)
from .model import (
    Cluster,
    Kind,
    Node,
    Socket,
    keep_frames_together,
    link_is_flow,
    socket_graph,
    trace_multi_input_sources,
)

type _MixedGraph = DiGraph[Node | Cluster]
# The graphs of one column, in the names the papers use: LT is the part of
# the nesting tree above the column's nodes, TC its reflexive transitive
# closure, GC the order constraints between the column's clusters.


def get_col_nesting_trees(
    columns: Sequence[Collection[Node]],
    T: _MixedGraph,
) -> list[_MixedGraph]:
    """For each column, the part of the cluster tree above its nodes."""
    trees = []
    for col in columns:
        LT: _MixedGraph = DiGraph()
        nodes = [v for v in col if v in T]
        visited: set[Node | Cluster] = set(nodes)
        queue: deque[Node | Cluster] = deque(nodes)
        while queue:
            child = queue.popleft()
            for parent in T.predecessors(child):
                if parent not in visited:
                    visited.add(parent)
                    queue.append(parent)

                LT.add_edge(parent, child)

        trees.append(LT)

    return trees


def expand_multi_inputs(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Give every link into a multi-input socket an input index of its own,
    highest sort id first, and renumber the node's later inputs to follow.
    The ordering then sees those links as entering separate sockets."""
    H = socket_graph(G)
    for v in dict.fromkeys(s.owner for s in state.multi_input_sort_ids):
        if v not in G:
            continue
        inputs = sorted({link.tosock for link in G.in_links(v)}, key=lambda s: s.idx)
        i = inputs[0].idx
        for socket in inputs:
            if socket not in state.multi_input_sort_ids:
                if i != socket.idx:
                    link = next(link for link in G.in_links(v) if link.tosock == socket)
                    link.tosock = replace(socket, idx=i)
                i += 1
                continue

            sort_ids = sorted(
                state.multi_input_sort_ids[socket], key=itemgetter(1), reverse=True
            )
            for from_socket, _ in trace_multi_input_sources(H, socket, sort_ids):
                link = next(
                    link
                    for link in G.links_between(from_socket.owner, v)
                    if link.tosock == socket and link.fromsock == from_socket
                )
                link.tosock = replace(socket, idx=i)
                i += 1


@cache
def reflexive_transitive_closure(LT: _MixedGraph) -> _MixedGraph:
    """*LT* with an edge from every node to each of its descendants and to
    itself."""
    TC = LT.copy()
    for v in LT:
        for u in (*descendants(LT, v), v):
            if u not in TC.successors(v):
                TC.add_edge(v, u)

    return TC


@cache
def topologically_sorted_clusters(LT: _MixedGraph) -> list[Cluster]:
    """The clusters of *LT*, outer ones first."""
    return [h for h in topological_sort(LT) if isinstance(h, Cluster)]


def crossing_reduction_graph(
    h: Cluster,
    LT: _MixedGraph,
    G: LayoutGraph[Node],
) -> LayoutGraph[Node | Cluster]:
    """The links from the fixed column into the direct children of *h*,
    with links into a child cluster's members redirected to that cluster.
    Every link runs from its fixed-column socket to its free-column one,
    whichever way *G* is oriented."""
    G_h: LayoutGraph[Node | Cluster] = LayoutGraph()
    G_h.add_nodes(LT.successors(h))
    TC = reflexive_transitive_closure(LT)
    members = [v for v in TC.successors(h) if isinstance(v, Node)]
    for t in members:
        if t not in G:
            continue
        for s, link in G.entering(t):
            c = next(c for c in TC.predecessors(t) if c in LT.successors(h))

            input_socket: Socket = link.tosock
            output_socket: Socket = link.fromsock
            is_reversed = output_socket.owner != s
            if is_reversed:
                input_socket, output_socket = output_socket, input_socket

            if G_h.has_link(s, c, link.key):
                merged = G_h.link(s, c, link.key)
                # The merged link is read through the orientation of `G`: on a
                # reversed `G` this compares the free-column socket, so parallel
                # links only merge going forwards.
                known = merged.tosock if is_reversed else merged.fromsock
                if known == output_socket:
                    continue

            to_socket = (
                input_socket
                if not isinstance(c, Cluster)
                else replace(input_socket, owner=c, idx=0)
            )
            G_h.add_link(s, c, output_socket, to_socket)

    return G_h


class _CrossingReductionGraph:
    """What a sweep needs to order the children of one cluster in a free
    column by the fixed column before it.

    ``graph`` is :func:`crossing_reduction_graph` for the cluster.
    ``reduced_free_col`` lists the cluster's direct children in the free
    column, nodes and clusters. ``expanded_fixed_col`` is the fixed column
    plus an upper and a lower border node for each of those clusters that
    also has nodes in the fixed column. ``constrained_clusters`` are those
    same clusters, whose order the free column must keep."""

    graph: LayoutGraph[Node | Cluster]

    fixed_LT: _MixedGraph
    free_LT: _MixedGraph

    fixed_col: list[Node]
    free_col: list[Node]

    expanded_fixed_col: list[Node]
    reduced_free_col: list[Node | Cluster]

    fixed_sockets: dict[Node, list[Socket]]
    free_sockets: dict[Node | Cluster, list[Socket]]

    border_pairs: dict[tuple[Node, Node], list[Node]]
    constrained_clusters: list[Cluster]

    __slots__ = tuple(__annotations__)

    def __init__(
        self,
        G: LayoutGraph[Node],
        h: Cluster,
        fixed_LT: _MixedGraph,
        free_LT: _MixedGraph,
        is_forwards: bool,
    ) -> None:
        G_h = crossing_reduction_graph(h, free_LT, G)
        self.graph = G_h

        self.fixed_LT = fixed_LT
        self.free_LT = free_LT

        fixed_col = next(v.col for v in fixed_LT if not isinstance(v, Cluster))
        self.fixed_col = fixed_col
        self.free_col = next(v.col for v in free_LT if not isinstance(v, Cluster))

        G_h.add_nodes(fixed_col)

        self.expanded_fixed_col = fixed_col.copy()

        def pos(v):
            return inf if isinstance(v, Cluster) else v.col.index(v)

        self.reduced_free_col = sorted(free_LT.successors(h), key=pos)

        self._insert_border_links(is_forwards)

        self.fixed_sockets = {}
        for u in self.expanded_fixed_col:
            if sockets := {link.fromsock for link in G_h.out_links(u)}:
                self.fixed_sockets[u] = sorted(
                    sockets, key=lambda d: d.idx, reverse=is_forwards
                )

        self.free_sockets = {}
        for v in self.reduced_free_col:
            self.free_sockets[v] = [link.fromsock for link in G_h.in_links(v)]

        self.constrained_clusters = [
            cast(Cluster, v) for v in self.reduced_free_col if v in fixed_LT
        ]

    def _insert_border_links(self, is_forwards: bool) -> None:
        self.border_pairs = {}
        free_clusters = [v for v in self.reduced_free_col if isinstance(v, Cluster)]
        for c in [c for c in free_clusters if c in self.fixed_LT]:
            upper_v = Node(type=Kind.VERTICAL_BORDER)
            lower_v = Node(type=Kind.VERTICAL_BORDER)
            self.expanded_fixed_col.extend((upper_v, lower_v))

            for border_v in upper_v, lower_v:
                self.graph.add_link(
                    border_v,
                    c,
                    Socket(border_v, 0, is_forwards),
                    # border sockets use the cluster as an opaque owner
                    Socket(cast("Node", c), 0, not is_forwards),
                )

            bordered_nodes = [
                v for v in descendants(self.fixed_LT, c) if not isinstance(v, Cluster)
            ]
            self.border_pairs[upper_v, lower_v] = bordered_nodes


def crossing_reduction_items(
    trees: Iterable[_MixedGraph],
    G: LayoutGraph[Node],
    is_forwards: bool,
) -> list[list[_CrossingReductionGraph]]:
    """For each pair of neighbouring columns, a
    :class:`_CrossingReductionGraph` per cluster of the free column, outer
    clusters first."""
    items = []
    for fixed_LT, free_LT in pairwise(trees):
        crossing_reduction_graphs = [
            _CrossingReductionGraph(G, h, fixed_LT, free_LT, is_forwards)
            for h in topologically_sorted_clusters(free_LT)
        ]
        items.append(crossing_reduction_graphs)

    return items


def sort_expanded_fixed_col(H: _CrossingReductionGraph) -> None:
    """Sort the expanded fixed column by the fixed column's current order,
    with each pair of border nodes just above and below the nodes they
    stand for."""
    pos: dict[Node, float] = {v: i for i, v in enumerate(H.fixed_col)}

    for (upper_v, lower_v), bordered_nodes in H.border_pairs.items():
        positions = [pos[v] for v in bordered_nodes]
        pos[upper_v] = min(positions) - 0.1
        pos[lower_v] = max(positions) + 0.1

    H.expanded_fixed_col.sort(key=pos.__getitem__)


def calc_socket_ranks(H: _CrossingReductionGraph, is_forwards: bool) -> None:
    """Give every linked socket of the fixed column a position: its node's
    place in the column plus a fraction for its place among the node's
    sockets."""
    for v, sockets in H.fixed_sockets.items():
        incr = 1 / (len(sockets) + 1)
        rank = H.expanded_fixed_col.index(v) + 1
        if is_forwards:
            incr = -incr

        for socket in sockets:
            rank += incr
            v.cr.socket_ranks[socket] = rank


def calc_barycenters(H: _CrossingReductionGraph) -> None:
    """Set the barycenter of each item of the free column to the mean
    position of the fixed-column sockets it is linked to. An item without
    such links keeps None."""
    for w in H.reduced_free_col:
        if sockets := H.free_sockets[w]:
            w.cr.barycenter = fmean([s.owner.cr.socket_ranks[s] for s in sockets])


def get_barycenter(v: Node | Cluster) -> float:
    barycenter = v.cr.barycenter
    assert barycenter is not None
    return barycenter


def fill_in_unknown_barycenters(col: list[Node | Cluster]) -> None:
    """A node with no neighbour in the fixed column stays between the nodes
    it is between now."""
    for i, v in enumerate(col):
        if v.cr.barycenter is not None:
            continue

        prev_b = get_barycenter(col[i - 1]) if i != 0 else 0
        next_b = next(
            (b for w in col[i + 1 :] if (b := w.cr.barycenter) is not None), prev_b + 1
        )
        v.cr.barycenter = (prev_b + next_b) / 2


def find_violated_constraint(
    GC: _MixedGraph,
) -> tuple[Node | Cluster, Node | Cluster] | None:
    """A constraint ``(s, t)`` of *GC* that the barycenters break, with *s*
    not before *t*, or None when all hold."""
    active = [v for v in GC if GC.successors(v) and not GC.predecessors(v)]
    incoming_constraints = defaultdict(list)
    while active:
        v = active.pop(0)

        for c in incoming_constraints[v]:
            if c[0].cr.barycenter >= v.cr.barycenter:
                return c

        for t in GC.successors(v):
            incoming_constraints[t].insert(0, (v, t))
            if len(incoming_constraints[t]) == GC.in_degree(t):
                active.append(t)

    return None


def merge_constrained(
    GC: _MixedGraph, s: Node | Cluster, t: Node | Cluster, merged: Node
) -> None:
    """Replace *s* and *t* by *merged*, which takes over their constraints
    (the one between them becomes a self-loop)."""
    for old in [v for v in GC if v in (s, t)]:
        GC.add_node(merged)
        edges: list[tuple[Node | Cluster, Node | Cluster]] = [
            (merged, merged if w == old else w) for w in GC.successors(old)
        ]
        edges += [(merged if u == old else u, merged) for u in GC.predecessors(old)]
        GC.remove_node(old)
        GC.add_edges(edges)


def handle_constraints(H: _CrossingReductionGraph) -> None:
    """Turn the barycenters of the free column into an order (each node's
    ``barycenter`` becomes its position) that keeps the constrained
    clusters in their order."""
    GC: _MixedGraph = DiGraph(pairwise(H.constrained_clusters))

    unconstrained = [v for v in H.reduced_free_col if v not in GC]
    # The free-column items each merged node stands for.
    L = {v: [v] for v in H.reduced_free_col}

    deg = {v: H.graph.degree(v) for v in GC}
    while c := find_violated_constraint(GC):
        v_c = Node(type=Kind.DUMMY)
        s, t = c

        deg[v_c] = deg[s] + deg[t]
        assert s.cr.barycenter is not None and t.cr.barycenter is not None
        if deg[v_c] > 0:
            v_c.cr.barycenter = (
                s.cr.barycenter * deg[s] + t.cr.barycenter * deg[t]
            ) / deg[v_c]
        else:
            v_c.cr.barycenter = (s.cr.barycenter + t.cr.barycenter) / 2

        L[v_c] = L[s] + L[t]

        merge_constrained(GC, s, t, v_c)
        if GC.has_edge(v_c, v_c):
            GC.remove_edge(v_c, v_c)

        if v_c not in GC:
            unconstrained.append(v_c)

    groups = sorted(dict.fromkeys(chain(GC, unconstrained)), key=get_barycenter)
    for i, v in enumerate(chain(*[L[v] for v in groups])):
        v.cr.barycenter = i


def get_new_col_order(v: Node | Cluster, LT: _MixedGraph) -> Iterator[Node | Cluster]:
    """The nodes below *v* in the column's nesting tree, each cluster's
    children by barycenter."""
    if isinstance(v, Cluster):
        for w in sorted(LT.successors(v), key=get_barycenter):
            yield from get_new_col_order(w, LT)
    else:
        yield v


@cache
def non_cluster_descendant(T: _MixedGraph, c: Cluster) -> Node:
    """The first node found below the cluster *c*."""
    return next(v for _, v in bfs_edges(T, c) if not isinstance(v, Cluster))


def sort_reduced_free_columns(
    items: Iterable[Sequence[_CrossingReductionGraph]],
) -> None:
    """Bring every ``reduced_free_col`` back in line with the current order
    of its column. A cluster is placed by one of its nodes."""
    for crossing_reduction_graphs in items:
        for H in crossing_reduction_graphs:

            def pos(v: Node | Cluster, H=H) -> int:
                w = (
                    non_cluster_descendant(H.free_LT, v)
                    if isinstance(v, Cluster)
                    else v
                )
                return H.free_col.index(w)

            H.reduced_free_col.sort(key=pos)


_MAX_SWEEPS = 24
_PATIENCE = 2
# Besides the three fixed starting orders, shuffled ones are tried while
# the graph is small enough for them to be cheap: about this many nodes'
# worth of extra starts in all, and never more than `_MAX_SHUFFLES`.
_SHUFFLE_BUDGET = 500
_MAX_SHUFFLES = 8
_MAX_TRANSPOSE_PASSES = 10


class Lcg:
    """A minimal random generator, the same in any language: the 48-bit
    linear congruential generator of ``drand48`` (and of Blender's
    ``RandomNumberGenerator``)."""

    __slots__ = ("state",)

    state: int

    def __init__(self, seed: int) -> None:
        self.state = (seed << 16) | 0x330E

    def below(self, n: int) -> int:
        """An integer in ``range(n)``."""
        self.state = (self.state * 0x5DEECE66D + 0xB) & 0xFFFFFFFFFFFF
        return (self.state >> 17) % n

    def shuffle[T](self, items: list[T]) -> None:
        for i in range(len(items) - 1, 0, -1):
            j = self.below(i + 1)
            items[i], items[j] = items[j], items[i]


def _set_order(
    columns: Sequence[list[Node]],
    order: Sequence[Sequence[Node]],
    items: list[list[_CrossingReductionGraph]],
) -> None:
    """Put *columns* in the given *order*, in place."""
    for col, wanted in zip(columns, order):
        col.sort(key=wanted.index)
    sort_reduced_free_columns(items)


def _sweep(
    items: list[list[_CrossingReductionGraph]],
    T: _MixedGraph,
    is_forwards: bool,
) -> None:
    """One pass over the columns in one direction, reordering each by the
    barycenters of its nodes."""
    for v in T:
        v.cr.reset()

    for i, crossing_reduction_graphs in enumerate(items):
        if i == 0:
            # The first fixed column has no barycenters yet: its clusters
            # keep the column's own order.
            clusters = {
                c: j
                for j, v in enumerate(crossing_reduction_graphs[0].fixed_col)
                for c in ancestors(T, v)
            }
            key = cast(Callable[[Cluster], int], clusters.get)
        else:
            key = get_barycenter

        for H in crossing_reduction_graphs:
            H.constrained_clusters.sort(key=key)
            sort_expanded_fixed_col(H)

            calc_socket_ranks(H, is_forwards)
            calc_barycenters(H)
            fill_in_unknown_barycenters(H.reduced_free_col)
            handle_constraints(H)

        # The graphs of a column share its nesting tree and its column.
        free_LT = crossing_reduction_graphs[0].free_LT
        free_col = crossing_reduction_graphs[0].free_col
        root = topologically_sorted_clusters(free_LT)[0]
        free_col.sort(key=tuple(get_new_col_order(root, free_LT)).index)


def _depth_first_order(
    G: LayoutGraph[Node], columns: Sequence[list[Node]], forwards: bool
) -> list[list[Node]]:
    """The columns reordered by when a depth-first walk reaches each node,
    starting from the first column (the last, going backwards) and taking
    nodes and links in their current order. Nodes that are linked end up
    near each other, which is a good order to start sweeping from."""
    reached: dict[Node, int] = {}
    starts = columns if forwards else list(reversed(columns))
    for col in starts:
        for root in col:
            if root in reached:
                continue
            reached[root] = len(reached)
            stack = [iter(G.out_links(root) if forwards else G.in_links(root))]
            while stack:
                for link in stack[-1]:
                    v = link.tonode if forwards else link.fromnode
                    if v not in reached:
                        reached[v] = len(reached)
                        stack.append(
                            iter(G.out_links(v) if forwards else G.in_links(v))
                        )
                        break
                else:
                    stack.pop()

    order = []
    for col in columns:
        new = sorted(col, key=reached.__getitem__)
        keep_frames_together(new)
        order.append(new)
    return order


@dataclass(frozen=True, slots=True)
class CrossingWeights:
    """What a crossing of two links costs the ordering, by what the links
    carry: the tree's main data ("flow", see ``priority.FLOW_SOCKETS``) or
    anything else ("value"). Branches of the trunk passing each other read
    easily. A value cutting across the trunk does not."""

    flow_flow: float = 1.0
    value_value: float = 1.0
    flow_value: float = 4.0


CROSSING_WEIGHTS = CrossingWeights()
"""The weights the ordering uses."""


type _Endpoint = tuple[int, int]
"""Where a link ends in a column: the position of the node, and of the
socket on it."""


def _transpose(
    G: LayoutGraph[Node], columns: Sequence[list[Node]], weights: CrossingWeights
) -> bool:
    """Swap neighbours in a column wherever that lowers the cost of the
    crossings among their links, until no swap helps. Only nodes directly
    in the same frame are swapped, so frames stay together. Returns whether
    anything moved.

    The sweeps order a column by where its nodes' neighbours are on
    average. This looks at the actual links of two nodes, and so finds the
    swaps an average hides."""
    position = {v: i for col in columns for i, v in enumerate(col)}
    # cost[a_flow][b_flow]: what a crossing of two links costs.
    cost = (
        (weights.value_value, weights.flow_value),
        (weights.flow_value, weights.flow_flow),
    )
    flow = {k: link_is_flow(k) for k in G.all_links()}

    def ends(v: Node) -> tuple[list[tuple[_Endpoint, bool]], ...]:
        left = [
            ((position[k.fromnode], k.fromsock.idx), flow[k]) for k in G.in_links(v)
        ]
        right = [((position[k.tonode], k.tosock.idx), flow[k]) for k in G.out_links(v)]
        return left, right

    def gain(
        upper: tuple[list[tuple[_Endpoint, bool]], ...],
        lower: tuple[list[tuple[_Endpoint, bool]], ...],
    ) -> float:
        """Cost of the crossings between the links of two neighbours now,
        less what it would be with the two swapped."""
        total = 0.0
        for above, below in zip(upper, lower):
            for a, a_flow in above:
                costs = cost[a_flow]
                for b, b_flow in below:
                    if a > b:
                        total += costs[b_flow]
                    elif a < b:
                        total -= costs[b_flow]
        return total

    moved = False
    last = len(columns) - 1
    # A column is looked at again only while its own order, or a
    # neighbour's, has changed since it was last looked at.
    changed_before = [True] * len(columns)
    for _ in range(_MAX_TRANSPOSE_PASSES):
        improved = False
        changed = [False] * len(columns)
        for c, col in enumerate(columns):
            if not (
                changed_before[c]
                or (c > 0 and changed[c - 1])
                or (c < last and changed_before[c + 1])
            ):
                continue
            # The neighbouring columns stay put while this one is swept.
            ends_of = {v: ends(v) for v in col}
            for i in range(len(col) - 1):
                upper, lower = col[i], col[i + 1]
                if upper.cluster is not lower.cluster:
                    continue
                if gain(ends_of[upper], ends_of[lower]) > 0:
                    col[i], col[i + 1] = lower, upper
                    position[lower], position[upper] = i, i + 1
                    improved = moved = changed[c] = True
        if not improved:
            break
        changed_before = changed
    return moved


def _inversions(links: list[tuple[_Endpoint, _Endpoint]]) -> int:
    """Pairs of *links* (sorted) that cross. Links from one socket are
    taken together so they do not count against each other."""
    total = 0
    seen: list[tuple[int, int]] = []
    i = 0
    while i < len(links):
        j = i
        while j < len(links) and links[j][0] == links[i][0]:
            j += 1
        for _, right in links[i:j]:
            total += len(seen) - bisect_right(seen, right)
        for _, right in links[i:j]:
            insort(seen, right)
        i = j
    return total


def count_crossings(
    G: LayoutGraph[Node],
    columns: Sequence[list[Node]],
    weights: CrossingWeights | None = None,
) -> float:
    """Pairs of links between neighbouring columns that cross, by the
    order of the nodes and of the sockets on each node. Links that share a
    socket do not cross.

    With *weights* each pair counts for what a crossing of its kind costs
    (see :class:`CrossingWeights`)."""
    position = {v: i for col in columns for i, v in enumerate(col)}
    total = 0.0
    for col in columns:
        links: list[tuple[_Endpoint, _Endpoint]] = []
        flow: list[tuple[_Endpoint, _Endpoint]] = []
        values: list[tuple[_Endpoint, _Endpoint]] = []
        for k in (k for v in col for k in G.in_links(v)):
            ends = (
                (position[k.fromnode], k.fromsock.idx),
                (position[k.tonode], k.tosock.idx),
            )
            links.append(ends)
            if weights is not None:
                (flow if link_is_flow(k) else values).append(ends)
        links.sort()
        crossings = _inversions(links)
        if weights is None:
            total += crossings
            continue
        flow.sort()
        values.sort()
        of_flow = _inversions(flow)
        of_values = _inversions(values)
        total += (
            weights.flow_flow * of_flow
            + weights.value_value * of_values
            + weights.flow_value * (crossings - of_flow - of_values)
        )
    return total


def minimize_crossings(
    G: LayoutGraph[Node], T: _MixedGraph, state: LayoutState
) -> None:
    """Order the columns so that the crossings of links cost as little as
    the search finds.

    Sweeps from several starting orders, each in both directions, and keeps
    the cheapest order. The starts are the order the columns come in and
    two depth-first orders. On small graphs a few shuffled orders from
    ``Lcg(options.seed)`` are added. From each start, sweeps alternate
    direction, each followed by swaps of neighbours (:func:`_transpose`),
    until ``_PATIENCE`` sweeps in a row bring no improvement. The result is
    deterministic for a given seed."""
    columns = G.columns
    weights = CROSSING_WEIGHTS
    trees = get_col_nesting_trees(columns, T)
    G_ = G.copy()

    expand_multi_inputs(G_, state)

    forward_items = crossing_reduction_items(trees, G_, True)
    backward_items = crossing_reduction_items(reversed(trees), G_.reversed(), False)
    items = forward_items + backward_items

    starts = [
        [col.copy() for col in columns],
        _depth_first_order(G, columns, True),
        _depth_first_order(G, columns, False),
    ]

    shuffles = min(_MAX_SHUFFLES, _SHUFFLE_BUDGET // max(len(G), 1))
    rng = Lcg(state.options.seed)
    for _ in range(shuffles):
        shuffled = [col.copy() for col in columns]
        for col in shuffled:
            rng.shuffle(col)
            keep_frames_together(col)
        starts.append(shuffled)

    best_cross_count = inf
    best_columns = [col.copy() for col in columns]

    for start in starts:
        for first_forwards in (True, False):
            if best_cross_count == 0:
                break
            _set_order(columns, start, items)
            is_forwards = first_forwards
            # The start itself may be as good as it gets.
            fewest = count_crossings(G_, columns, weights)
            if fewest < best_cross_count:
                best_cross_count = fewest
                best_columns = [col.copy() for col in columns]
            stale = 0
            for _ in range(_MAX_SWEEPS):
                _sweep(forward_items if is_forwards else backward_items, T, is_forwards)
                is_forwards = not is_forwards
                _transpose(G_, columns, weights)
                sort_reduced_free_columns(items)
                cross_count = count_crossings(G_, columns, weights)
                if cross_count < best_cross_count:
                    best_cross_count = cross_count
                    best_columns = [col.copy() for col in columns]
                if cross_count < fewest:
                    fewest = cross_count
                    stale = 0
                else:
                    stale += 1
                if stale >= _PATIENCE or fewest == 0:
                    break

    _set_order(columns, best_columns, items)

    reflexive_transitive_closure.cache_clear()
    topologically_sorted_clusters.cache_clear()
    non_cluster_descendant.cache_clear()
