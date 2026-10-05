# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from itertools import pairwise
from typing import TYPE_CHECKING, cast

from .common import group_by
from .digraph import (
    DiGraph,
    LayoutGraph,
    Link,
    descendants,
    simple_digraph,
    topological_sort,
    weakly_connected_components,
)
from .edits import RemoveLink
from .model import (
    Cluster,
    ClusterGraph,
    Edge,
    Kind,
    Node,
    Socket,
    add_dummy_edge,
    is_real,
    link_is_flow,
    link_priority,
)

if TYPE_CHECKING:
    from .config import LayoutState


def lowest_common_cluster(
    T: DiGraph[Node | Cluster],
    links: Iterable[Link[Node]],
) -> dict[Edge, Cluster]:
    """The innermost cluster containing both ends of each link whose ends
    are in different clusters, keyed by ``(fromnode, tonode)``."""
    lca: dict[Edge, Cluster] = {}
    for link in links:
        u, v = link.fromnode, link.tonode
        if u.cluster == v.cluster or (u, v) in lca:
            continue

        enclosing: set[Node | Cluster] = set()
        c: Node | Cluster = u
        while parents := T.predecessors(c):
            c = next(iter(parents))
            enclosing.add(c)

        c = v
        while c not in enclosing:
            c = next(iter(T.predecessors(c)))

        lca[u, v] = cast(Cluster, c)

    return lca


def add_dummy_nodes_to_edge(
    G: LayoutGraph[Node],
    link: Link[Node],
    dummy_nodes: Sequence[Node],
    state: LayoutState,
) -> None:
    if not dummy_nodes:
        return

    priority = link_priority(link, state.socket_priority)
    is_flow = link_is_flow(link)
    for w in dummy_nodes:
        w.priority = max(w.priority, priority)
        w.is_flow = is_flow

    for a, b in pairwise(dummy_nodes):
        if not G.has_link(a, b, 0):
            add_dummy_edge(G, a, b)

    u, v = link.fromnode, link.tonode

    w = dummy_nodes[0]
    if w not in G.successors(u):
        G.add_link(u, w, link.fromsock, Socket(w, 0, False))

    z = dummy_nodes[-1]
    G.add_link(z, v, Socket(z, 0, True), link.tosock)

    G.remove_link(link)

    if not is_real(u) or not is_real(v):
        return

    # The link is replaced by the chain through the dummy nodes. A plain
    # input drops its old link when the new one is made; a multi-input
    # would keep both. (Without reroutes the chain is only the layout's:
    # the tree keeps its link.)
    if state.options.reroutes != "none" and link.tosock.dna.is_multi_input:
        edit = RemoveLink(link.fromsock.dna, link.tosock.dna)
        if edit not in state.edits:
            state.edits.append(edit)


def assign_clusters(
    dummy_nodes: Iterable[Node],
    start: Cluster,
    stop: Cluster,
    is_within_cluster: Callable[[Node, Cluster], bool],
) -> None:
    c = start
    for w in dummy_nodes:
        while c != stop and not is_within_cluster(w, c):
            c = c.cluster

        if c == stop:
            break

        w.cluster = c


def improve_cluster_assignment(e: Edge, dummy_nodes: Sequence[Node]) -> None:
    u, v = e
    assert u.cluster and v.cluster
    c1 = u.cluster
    c2 = v.cluster

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if not (c1.node and c2.node) or c1.right.rank >= c2.left.rank:
        if c2.node and u.rank < c2.left.rank:
            c1 = None
            while c2.cluster.node and u.rank < c2.cluster.left.rank:
                c2 = c2.cluster
        elif c1.node and v.rank > c1.right.rank:
            c2 = None
            while c1.cluster.node and v.rank > c1.cluster.right.rank:
                c1 = c1.cluster
        else:
            return
    else:
        while True:
            parent1 = c1.cluster
            if parent1.node and parent1.right.rank < c2.left.rank:
                c1 = parent1
                continue

            parent2 = c2.cluster
            if parent2.node and c1.right.rank < parent2.left.rank:
                c2 = parent2
                continue

            break

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if c1:
        assign_clusters(
            dummy_nodes,
            u.cluster,
            c1.cluster,
            lambda w, c: w.rank <= c.right.rank,
        )

    if c2:
        assign_clusters(
            reversed(dummy_nodes),
            v.cluster,
            c2.cluster,
            lambda w, c: w.rank >= c.left.rank,
        )


def get_reroute_paths(
    CG: ClusterGraph,
    function: Callable | None = None,
    *,
    preserve_reroute_clusters: bool = True,
    aligned: bool = False,
    linear: bool = True,
) -> list[list[Node]]:
    G = CG.G
    reroutes = {v for v in G if v.is_reroute and (not function or function(v))}
    H = simple_digraph(G.subgraph(reroutes))

    K = G if linear else H
    for v in H:
        if K.out_degree(v) > 1:
            H.remove_edges(tuple(H.out_edges(v)))

    if preserve_reroute_clusters:
        reroute_clusters = {
            c
            for c in CG.S
            if all(v.is_reroute for v in CG.T.successors(c) if v.type != Kind.CLUSTER)
        }
        H.remove_edges(
            [
                (u, v)
                for u, v in H.edges()
                if u.cluster != v.cluster and {u.cluster, v.cluster} & reroute_clusters
            ]
        )

    if aligned:
        H.remove_edges([(u, v) for u, v in H.edges() if u.y != v.y])

    indicies = {v: i for i, v in enumerate(topological_sort(G)) if v in reroutes}
    paths = [
        sorted(c, key=lambda v: indicies[v]) for c in weakly_connected_components(H)
    ]
    paths.sort(key=lambda p: sum([indicies[v] for v in p]))
    return paths


def merge_edges(CG: ClusterGraph) -> None:
    G = CG.G
    T = CG.T
    groups = group_by(G.all_links(), key=lambda link: link.fromsock)
    links: tuple[Link[Node], ...]
    for links, from_socket in groups.items():
        long_edges = [
            link for link in links if link.tonode.rank - link.fromnode.rank > 1
        ]

        if len(long_edges) < 2:
            continue

        long_edges.sort(key=lambda link: link.tonode.rank)
        lca = lowest_common_cluster(T, long_edges)
        dummy_nodes = []
        for link in long_edges:
            u, v = link.fromnode, link.tonode
            if dummy_nodes and dummy_nodes[-1].rank == v.rank - 1:
                w = dummy_nodes[-1]
            else:
                assert u.cluster
                c = lca.get((u, v), u.cluster)
                w = Node(None, c, Kind.DUMMY, v.rank - 1)
                dummy_nodes.append(w)

            add_dummy_nodes_to_edge(G, link, [w], CG.state)
            G.remove_link_between(u, w)

        for pair in pairwise(dummy_nodes):
            add_dummy_edge(G, *pair)

        w = dummy_nodes[0]
        G.add_link(u, w, from_socket, Socket(w, 0, False))

        improve_cluster_assignment((u, v), dummy_nodes)
        for w in dummy_nodes:
            assert w.cluster is not None
            T.add_edge(w.cluster, w)


def insert_dummy_nodes(CG: ClusterGraph) -> None:
    G = CG.G
    T = CG.T

    # -------------------------------------------------------------------

    for c in CG.S:
        members = [v for v in descendants(T, c) if v.type != Kind.CLUSTER]
        c.left = min(members, key=lambda v: v.rank)
        c.right = max(members, key=lambda v: v.rank)

    # -------------------------------------------------------------------

    long_edges = [
        link for link in G.all_links() if link.tonode.rank - link.fromnode.rank > 1
    ]
    lca = lowest_common_cluster(T, long_edges)
    for link in long_edges:
        u, v = link.fromnode, link.tonode
        assert u.cluster
        c = lca.get((u, v), u.cluster)
        dummy_nodes = []
        for i in range(u.rank + 1, v.rank):
            w = Node(None, c, Kind.DUMMY, i)
            dummy_nodes.append(w)

        improve_cluster_assignment((u, v), dummy_nodes)
        add_dummy_nodes_to_edge(G, link, dummy_nodes, CG.state)

    for w in [w for w in G if w not in T]:
        assert w.cluster
        T.add_edge(w.cluster, w)

    # -------------------------------------------------------------------

    for c in CG.S:
        if not c.node:
            continue

        ranks = sorted({v.rank for v in descendants(T, c) if v.type != Kind.CLUSTER})
        for i, j in pairwise(ranks):
            for k in range(i + 1, j):
                v = Node(None, c, Kind.DUMMY, k)
                v.is_fill_dummy = True
                G.add_node(v)
                T.add_edge(c, v)
