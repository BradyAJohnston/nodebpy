# SPDX-License-Identifier: GPL-2.0-or-later

# https://link.springer.com/chapter/10.1007/3-540-36151-0_26
# https://doi.org/10.1016/j.jvlc.2013.11.005
# https://doi.org/10.1007/978-3-642-11805-0_14
# https://link.springer.com/chapter/10.1007/978-3-540-31843-9_22
# https://doi.org/10.7155/jgaa.00088

from __future__ import annotations

import random
from collections import defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Iterator, Sequence
from dataclasses import replace
from functools import cache
from itertools import chain, pairwise
from math import inf
from operator import itemgetter
from statistics import fmean
from typing import cast

from ..config import LayoutState
from .graph import Cluster, Kind, Node, Socket, socket_graph
from .pipeline import Layout, register
from .tree import (
    DiGraph,
    Tree,
    ancestors,
    bfs_edges,
    descendants,
    edge_dfs,
    topological_sort,
)

# -------------------------------------------------------------------

type _MixedGraph = DiGraph[Node | Cluster]


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


def expand_multi_inputs(G: Tree[Node], state: LayoutState) -> None:
    H = socket_graph(G)
    reroutes = {v for v in H if v.owner.is_reroute}
    for v in {s.owner for s in state.multi_input_sort_ids}:
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

            sort_ids = state.multi_input_sort_ids[socket]
            SH = H.subgraph({i[0] for i in sort_ids} | {socket} | reroutes)
            seen = set()
            for base_from_socket, _ in sorted(
                sort_ids, key=itemgetter(1), reverse=True
            ):
                from_socket = next(
                    s
                    for s, t in edge_dfs(SH, base_from_socket)
                    if t == socket and s not in seen
                )
                link = next(
                    link
                    for link in G.links_between(from_socket.owner, v)
                    if link.tosock == socket and link.fromsock == from_socket
                )
                link.tosock = replace(socket, idx=i)
                seen.add(from_socket)
                i += 1


@cache
def reflexive_transitive_closure(LT: _MixedGraph) -> _MixedGraph:
    TC = LT.copy()
    for v in LT:
        for u in descendants(LT, v) | {v}:
            if u not in TC.successors(v):
                TC.add_edge(v, u)

    return TC


@cache
def topologically_sorted_clusters(LT: _MixedGraph) -> list[Cluster]:
    return [h for h in topological_sort(LT) if isinstance(h, Cluster)]


def crossing_reduction_graph(
    h: Cluster,
    LT: _MixedGraph,
    G: Tree[Node],
) -> Tree[Node | Cluster]:
    """The links from the fixed column into the direct children of *h*,
    with links into a child cluster's members redirected to that cluster.
    Every link runs from its fixed-column socket to its free-column one,
    whichever way *G* is oriented."""
    G_h: Tree[Node | Cluster] = Tree()
    G_h.add_nodes(LT.successors(h))
    TC = reflexive_transitive_closure(LT)
    members = [v for v in TC.successors(h) if isinstance(v, Node)]
    for s, t, link in G.entering(members):
        c = next(c for c in TC.predecessors(t) if c in LT.successors(h))

        input_socket: Socket = link.tosock
        output_socket: Socket = link.fromsock
        is_reversed = output_socket.owner != s
        if is_reversed:
            input_socket, output_socket = output_socket, input_socket

        if G_h.has_link(s, c, link.key):
            merged = G_h.link(s, c, link.key)
            # NOTE: kept from upstream, which reads the merged link through
            # the orientation of `G`: on a reversed `G` this compares the
            # free-column socket, so parallel links only merge going forwards.
            known = merged.tosock if is_reversed else merged.fromsock
            if known == output_socket:
                merged.weight += 1
                continue

        to_socket = (
            input_socket
            if c.type != Kind.CLUSTER
            else replace(input_socket, owner=c, idx=0)
        )
        G_h.add_link(s, c, output_socket, to_socket, weight=1)

    return G_h


_BALANCING_FAC = 1


class _CrossingReductionGraph:
    graph: Tree[Node | Cluster]

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

    N: list[Socket]
    S: list[Socket]
    bipartite_edges: list[tuple[Socket, Socket, int]]

    __slots__ = tuple(__annotations__)

    def _insert_border_edges(self, is_forwards: bool) -> None:
        self.border_pairs = {}
        free_clusters = {v for v in self.reduced_free_col if v.type == Kind.CLUSTER}
        for c in {c for c in free_clusters if c in self.fixed_LT}:
            upper_v = Node(type=Kind.VERTICAL_BORDER)
            lower_v = Node(type=Kind.VERTICAL_BORDER)
            self.expanded_fixed_col.extend((upper_v, lower_v))

            fac = 1 + sum(v in self.fixed_LT for v in descendants(self.free_LT, c))
            for border_v in upper_v, lower_v:
                self.graph.add_link(
                    border_v,
                    c,
                    Socket(border_v, 0, is_forwards),
                    # border sockets use the cluster as an opaque owner
                    Socket(cast("Node", c), 0, not is_forwards),
                    weight=(0.5 * _BALANCING_FAC) * fac,
                )

            bordered_nodes = [
                v for v in descendants(self.fixed_LT, c) if v.type != Kind.CLUSTER
            ]
            self.border_pairs[upper_v, lower_v] = bordered_nodes

    def _add_bipartite_edges(self) -> None:
        # Links between the same two sockets count once, with the weight of
        # the last one.
        B: DiGraph[Socket] = DiGraph()
        for link in self.graph.all_links():
            B.add_edge(link.fromsock, link.tosock, link.weight)

        if not B:
            self.N = []
            self.S = []
            self.bipartite_edges = []
            return

        N, S = map(set, zip(*B.edges()))
        if len(S) > len(N):
            N, S = S, N
            B = B.reversed()

        self.N = sorted(N, key=lambda d: d.idx)
        self.S = sorted(S, key=lambda d: d.idx)
        self.bipartite_edges = [(u, v, B.weight(u, v)) for u, v in B.edges()]

    def __init__(
        self,
        G: Tree[Node],
        h: Cluster,
        fixed_LT: _MixedGraph,
        free_LT: _MixedGraph,
        is_forwards: bool,
    ) -> None:
        G_h = crossing_reduction_graph(h, free_LT, G)
        self.graph = G_h

        self.fixed_LT = fixed_LT
        self.free_LT = free_LT

        fixed_col = next(v.col for v in fixed_LT if v.type != Kind.CLUSTER)
        self.fixed_col = fixed_col
        self.free_col = next(v.col for v in free_LT if v.type != Kind.CLUSTER)

        G_h.add_nodes(fixed_col)

        self.expanded_fixed_col = fixed_col.copy()

        def pos(v):
            return v.col.index(v) if v.type != Kind.CLUSTER else inf

        self.reduced_free_col = sorted(free_LT.successors(h), key=pos)

        self._insert_border_edges(is_forwards)

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

        self._add_bipartite_edges()


def crossing_reduction_items(
    trees: Iterable[_MixedGraph],
    G: Tree[Node],
    is_forwards: bool,
) -> list[list[_CrossingReductionGraph]]:
    items = []
    for fixed_LT, free_LT in pairwise(trees):
        crossing_reduction_graphs = [
            _CrossingReductionGraph(G, h, fixed_LT, free_LT, is_forwards)
            for h in topologically_sorted_clusters(free_LT)
        ]
        items.append(crossing_reduction_graphs)

    return items


# -------------------------------------------------------------------


def sort_expanded_fixed_col(H: _CrossingReductionGraph) -> None:
    pos: dict[Node, float] = {v: i for i, v in enumerate(H.fixed_col)}

    for (upper_v, lower_v), bordered_nodes in H.border_pairs.items():
        positions = [pos[v] for v in bordered_nodes]
        pos[upper_v] = min(positions) - 0.1
        pos[lower_v] = max(positions) + 0.1

    H.expanded_fixed_col.sort(key=pos.get)  # type: ignore


def calc_socket_ranks(H: _CrossingReductionGraph, is_forwards: bool) -> None:
    for v, sockets in H.fixed_sockets.items():
        incr = 1 / (len(sockets) + 1)
        rank = H.expanded_fixed_col.index(v) + 1
        if is_forwards:
            incr = -incr

        for socket in sockets:
            rank += incr
            v.cr.socket_ranks[socket] = rank


def random_perturbation() -> float:
    random_amount = random.uniform(-1, 1)
    return random.uniform(0, 1) * random_amount - random_amount / 2


def calc_barycenters(H: _CrossingReductionGraph) -> None:
    for w in H.reduced_free_col:
        if sockets := H.free_sockets[w]:
            w.cr.barycenter = (
                fmean([s.owner.cr.socket_ranks[s] for s in sockets])
                + random_perturbation()
            )


def get_barycenter(v: Node | Cluster) -> float:
    barycenter = v.cr.barycenter
    assert barycenter is not None
    return barycenter


def fill_in_unknown_barycenters(
    col: list[Node | Cluster], is_first_sweep: bool
) -> None:
    if is_first_sweep:
        max_b = (
            max([b for v in col if (b := v.cr.barycenter) is not None], default=0) + 2
        )
        for v in col:
            if v.cr.barycenter is None:
                v.cr.barycenter = (
                    random.uniform(0, 1) * max_b - 1 + random_perturbation()
                )
        return

    for i, v in enumerate(col):
        if v.cr.barycenter is not None:
            continue

        prev_b = get_barycenter(col[i - 1]) if i != 0 else 0
        next_b = next(
            (b for w in col[i + 1 :] if (b := w.cr.barycenter) is not None), prev_b + 1
        )
        v.cr.barycenter = (prev_b + next_b) / 2 + random_perturbation()


def find_violated_constraint(
    GC: _MixedGraph,
) -> tuple[Node | Cluster, Node | Cluster] | None:
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
    GC: _MixedGraph = DiGraph(pairwise(H.constrained_clusters))

    unconstrained = {v for v in set(H.reduced_free_col) if v not in GC}
    L = {v: [v] for v in H.reduced_free_col}

    deg = {v: H.graph.degree(v) for v in GC}
    while c := find_violated_constraint(GC):
        v_c = Node(type=Kind.DUMMY)
        s, t = c

        deg[v_c] = deg[s] + deg[t]
        assert s.cr.barycenter and t.cr.barycenter
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
            unconstrained.add(v_c)

    groups = sorted(set(chain(GC, unconstrained)), key=get_barycenter)
    for i, v in enumerate(chain(*[L[v] for v in groups])):
        v.cr.barycenter = i


def get_cross_count(H: _CrossingReductionGraph) -> int:
    edges = H.bipartite_edges

    if not edges:
        return 0

    reduced_free_col = set(H.reduced_free_col)

    def pos(s: Socket) -> float:
        v = s.owner
        if v in reduced_free_col:
            return v.cr.barycenter  # type: ignore
        else:
            return H.expanded_fixed_col.index(v)

    H.N.sort(key=pos)
    H.S.sort(key=pos)

    south_indicies = {k: i for i, k in enumerate(H.S)}
    north_indicies = {k: i for i, k in enumerate(H.N)}

    edges.sort(key=lambda e: south_indicies[e[1]])
    edges.sort(key=lambda e: north_indicies[e[0]])

    first_idx = 1
    while first_idx < len(H.S):
        first_idx *= 2

    tree = [0] * (2 * first_idx - 1)
    first_idx -= 1

    cross_weight = 0
    for _, v, weight in edges:
        idx = south_indicies[v] + first_idx
        tree[idx] += weight
        weight_sum = 0
        while idx > 0:
            if idx % 2 == 1:
                weight_sum += tree[idx + 1]

            idx = (idx - 1) // 2
            tree[idx] += weight

        cross_weight += weight * weight_sum

    return cross_weight


def get_new_col_order(v: Node | Cluster, LT: _MixedGraph) -> Iterator[Node | Cluster]:
    if v.type == Kind.CLUSTER:
        for w in sorted(LT.successors(v), key=get_barycenter):
            yield from get_new_col_order(w, LT)
    else:
        yield v


@cache
def non_cluster_descendant(T: _MixedGraph, c: Cluster) -> Node:
    return next(v for _, v in bfs_edges(T, c) if v.type != Kind.CLUSTER)


def sort_reduced_free_columns(
    items: Iterable[Sequence[_CrossingReductionGraph]],
) -> None:
    for crossing_reduction_graphs in items:
        for H in crossing_reduction_graphs:

            def pos(v: Node | Cluster, H=H) -> int:
                w = (
                    non_cluster_descendant(H.free_LT, v)
                    if v.type == Kind.CLUSTER
                    else v
                )
                return H.free_col.index(w)

            H.reduced_free_col.sort(key=pos)


# -------------------------------------------------------------------


def minimized_cross_count(
    columns: Sequence[list[Node]],
    forward_items: list[list[_CrossingReductionGraph]],
    backward_items: list[list[_CrossingReductionGraph]],
    T: _MixedGraph,
) -> float:
    cross_count = inf
    is_forwards = random.choice((True, False))
    is_first_sweep = True
    while True:
        for v in T:
            v.cr.reset()

        if cross_count == 0:
            return 0

        is_forwards = not is_forwards
        old_cross_count = cross_count
        cross_count = 0

        items = forward_items if is_forwards else backward_items
        for i, crossing_reduction_graphs in enumerate(items):
            if i == 0:
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
                fill_in_unknown_barycenters(H.reduced_free_col, is_first_sweep)
                handle_constraints(H)

                cross_count += get_cross_count(H)

            root = topologically_sorted_clusters(H.free_LT)[0]
            new_order = tuple(get_new_col_order(root, H.free_LT))
            H.free_col.sort(key=new_order.index)

        if old_cross_count > cross_count:
            sort_reduced_free_columns(forward_items + backward_items)
            best_columns = [c.copy() for c in columns]
            is_first_sweep = False
        else:
            for col, best_col in zip(columns, best_columns):
                col.sort(key=best_col.index)
            break

    return old_cross_count


def minimize_crossings(G: Tree[Node], T: _MixedGraph, state: LayoutState) -> None:
    columns = G.columns
    trees = get_col_nesting_trees(columns, T)
    G_ = G.copy()

    expand_multi_inputs(G_, state)

    forward_items = crossing_reduction_items(trees, G_, True)

    G__ = G_.reversed()
    backward_items = crossing_reduction_items(reversed(trees), G__, False)

    # -------------------------------------------------------------------

    random.seed(0)
    best_cross_count = inf
    best_columns = [c.copy() for c in columns]
    for _ in range(state.settings.iterations):
        cross_count = minimized_cross_count(columns, forward_items, backward_items, T)
        if cross_count < best_cross_count:
            best_cross_count = cross_count
            best_columns = [c.copy() for c in columns]
            if best_cross_count == 0:
                break
        else:
            for col, best_col in zip(columns, best_columns):
                col.sort(key=best_col.index)
            sort_reduced_free_columns(forward_items + backward_items)


@register("order", "layer_sweep")
def order_layer_sweep(layout: Layout) -> None:
    """Sweep back and forth over the columns, ordering each by the average
    position of its nodes' neighbours in the column before."""
    minimize_crossings(layout.G, layout.T, layout.state)
