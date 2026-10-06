"""Long links. A link that passes over one or more columns is split by a
dummy node in each of them (:func:`merge_edges`,
:func:`insert_dummy_nodes`). Also here: finding chains of reroutes and
dummy nodes (:func:`get_reroute_paths`)."""

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
    """Replace *link* by a chain through *dummy_nodes*, which take the
    link's priority and whether it is a flow link. Dummy nodes that are
    already chained, or already fed by the link's source, are reused."""
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

    # In the tree, a plain input drops its old link when the link from the
    # last reroute is made. A multi-input would keep both, so its old link
    # is removed. Without reroutes the tree keeps its link.
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
    """Give each of *dummy_nodes* in turn the innermost cluster that
    *is_within_cluster* accepts it in, going outwards from *start* and never
    back in. Stops at the first dummy node that only *stop* would hold."""
    c = start
    for w in dummy_nodes:
        while c != stop and not is_within_cluster(w, c):
            c = c.cluster

        if c == stop:
            break

        w.cluster = c


def improve_cluster_assignment(e: Edge, dummy_nodes: Sequence[Node]) -> None:
    """Move the dummy nodes of the long link *e* into the frames at its ends
    where they fit. A dummy node in a column that the frame of the source
    node, or a frame around it, still spans joins that frame. The same is
    done from the target's end. The other dummy nodes keep their cluster."""
    u, v = e
    assert u.cluster and v.cluster
    c1 = u.cluster
    c2 = v.cluster

    # c1: the outermost frame around u that ends before the other end's
    # frame begins. c2: likewise around v. None where that end has no such
    # frame.
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
    """The chains of reroutes and dummy nodes that *function* accepts, each
    from its source end to its target end.

    A chain ends at a reroute with more than one link out. With *linear*
    every link out counts. Without it only links to other reroutes of the
    selection count, so a reroute that also feeds nodes stays in its chain.
    With *preserve_reroute_clusters* a chain also breaks between two
    clusters when one of them is a frame that holds only reroutes. With
    *aligned* it also breaks between two reroutes at different heights.
    """
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
    """Let the long links that leave one output share dummy nodes.

    For an output with two or more long links, one dummy node is made in the
    column before each target, and the dummy nodes are chained. Each link
    then runs along the chain to the dummy node before its target, so the
    links are drawn as one line that branches."""
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
        # All from one output, so one source node; the farthest target last.
        u = long_edges[0].fromnode
        farthest = long_edges[-1].tonode
        dummy_nodes = []
        for link in long_edges:
            v = link.tonode
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

        improve_cluster_assignment((u, farthest), dummy_nodes)
        for w in dummy_nodes:
            assert w.cluster is not None
            T.add_edge(w.cluster, w)


def insert_dummy_nodes(CG: ClusterGraph) -> None:
    """Split every long link with a dummy node in each column it passes, so
    that every link joins neighbouring columns.

    Also rebinds each cluster's ``left`` and ``right`` to its leftmost and
    rightmost member nodes, and gives each frame a fill dummy node in every
    column between its nodes where it has none."""
    G = CG.G
    T = CG.T

    for c in CG.S:
        members = [v for v in descendants(T, c) if v.type != Kind.CLUSTER]
        c.left = min(members, key=lambda v: v.rank)
        c.right = max(members, key=lambda v: v.rank)

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

    # Fill dummy nodes, so that a frame has a node in every column it spans.
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
