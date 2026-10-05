# SPDX-License-Identifier: GPL-2.0-or-later
"""Stacks: chains of collapsed Math nodes, which are drawn as a tight
vertical pile. A stack is contracted into one node before the layout and
expanded again after it."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Mapping
from dataclasses import dataclass, field
from math import inf
from typing import Any, cast

from .config import LayoutState
from .digraph import (
    LayoutGraph,
    Link,
    find_cycle,
    is_acyclic,
    topological_sort,
    weakly_connected_components,
)
from .model import (
    Cluster,
    ClusterGraph,
    Edge,
    Kind,
    MultiEdge,
    Node,
    Socket,
    is_real,
    node_name,
)


@dataclass(slots=True)
class NodeStack:
    """A stack. ``path`` lists its nodes top to bottom. ``rep_node`` stands
    for them in the layout graph. ``stack_sockets_to_originals`` maps each
    socket of ``rep_node`` to the socket of a stacked node it stands for."""

    rep_node: Node
    path: list[Node]
    stack_sockets_to_originals: dict[Socket, Socket] = field(default_factory=dict)


# Adapted from NetworkX, to make it deterministic:
# https://github.com/networkx/networkx/blob/36e8a1ee85ca0ab4195a486451ca7d72153e2e00/networkx/algorithms/bipartite/matching.py#L59
def deterministic_hopcroft_karp_matching[T: Hashable](
    G: Mapping[T, Iterable[T]], top_nodes: Iterable[T], bottom_nodes: Iterable[T]
) -> dict[T, T]:
    """A maximum matching of the bipartite graph whose *top_nodes* have the
    neighbours *G* gives them among the *bottom_nodes*."""

    def bfs() -> bool:
        for u, paired in pair_U.items():
            if paired is None:
                dist[u] = 0
                Q.append(u)
            else:
                dist[u] = inf

        dist[None] = inf
        while Q:
            u = Q.popleft()
            if dist[u] < dist[None]:
                for v in G[u]:
                    if dist[pair_V[v]] == inf:
                        dist[pair_V[v]] = dist[u] + 1
                        Q.append(pair_V[v])

        return dist[None] != inf

    def dfs(root: T) -> bool:
        # Search for an augmenting path from `root` along the layers `bfs`
        # found, and flip it. Each stack entry is a node, its remaining
        # neighbours, and the neighbour the search went down through.
        stack: list[list[Any]] = [[root, iter(G[root]), None]]
        found = False
        while stack:
            entry = stack[-1]
            u, neighbours, via = entry
            if found:
                pair_V[via] = u
                pair_U[u] = via
                stack.pop()
                continue

            for v in neighbours:
                paired = pair_V[v]
                if dist[paired] != dist[u] + 1:
                    continue

                entry[2] = v
                if paired is None:
                    found = True
                else:
                    stack.append([paired, iter(G[paired]), None])
                break
            else:
                dist[u] = inf
                stack.pop()

        return found

    pair_U: dict[T, T | None] = {v: None for v in top_nodes}
    pair_V: dict[T, T | None] = {v: None for v in bottom_nodes}
    dist = {}
    Q = deque()

    while bfs():
        for u, v in pair_U.items():
            if v is None:
                dfs(u)

    return {k: v for k, v in (pair_U | pair_V).items() if v is not None}


def max_linear_branching(G: LayoutGraph[Node]) -> LayoutGraph[Node]:
    """The largest set of links of *G* in which every node has at most one
    predecessor and one successor, i.e. that only forms chains."""
    # Sorted by name, so the result does not depend on the order of *G*.
    nodes = sorted(G, key=node_name)
    edges = sorted(
        [(link.fromnode, link.tonode) for link in G.all_links()],
        key=lambda e: node_name(e[0]) + node_name(e[1]),
    )

    out_nodes = [(v, "out") for v in nodes]
    in_nodes = [(v, "in") for v in nodes]

    B: dict[tuple[Node, str], dict[tuple[Node, str], None]] = {
        u_out: {} for u_out in out_nodes
    }
    for u, v in edges:
        B[u, "out"][v, "in"] = None

    matching = deterministic_hopcroft_karp_matching(B, out_nodes, in_nodes)
    H: LayoutGraph[Node] = LayoutGraph()
    H.add_nodes(nodes)
    for u_out in out_nodes:
        if u_out in matching:
            H.add_link(u_out[0], matching[u_out][0])

    return H


# http://dx.doi.org/10.1016/S0020-0190(02)00491-X
def minimum_feedback_arc_set(G: LayoutGraph[Node]) -> set[MultiEdge]:
    """Links of the weighted *G* (as ``Link.ident``) whose removal leaves it
    acyclic, favouring light links. Lowers the weights of *G* in place."""
    G_ = G.copy()
    while cycle := find_cycle(G_):
        pairs = zip(cycle, cycle[1:] + cycle[:1])
        C = [G_.links_between(u, v)[0].ident for u, v in pairs]
        min_weight = min([G.link(*e).weight for e in C])
        for e in C:
            link = G.link(*e)
            link.weight -= min_weight
            if link.weight == 0:
                G_.remove_link_between(*e)

    for u, v, k in [link.ident for link in G.all_links()]:
        if G_.has_link(u, v, k):
            continue

        G_.add_link(u, v, key=k)
        if not is_acyclic(G_):
            G_.remove_link_between(u, v, k)

    return {link.ident for link in G.all_links() if not G_.has_link(*link.ident)}


def edges_preventing_acyclic_contraction(
    G: LayoutGraph[Node],
    K: LayoutGraph[Node],
) -> list[Edge]:
    """The links of *K* that cannot be contracted in *G* without creating a
    cycle, as ``(fromnode, tonode)``."""
    G_ = G.copy()
    for link in tuple(G_.all_links()):
        u, v, k = link.ident
        if K.has_link(u, v, k):
            G_.remove_link(link)
            G_.add_link(v, u, link.fromsock, link.tosock, key=k, weight=1)
        else:
            link.weight = inf

    F = minimum_feedback_arc_set(G_)
    return [(v, u) for u, v, _ in F]


def relabel_sockets(
    links: Iterable[Link[Node]],
    v: Node,
    node_stack: NodeStack,
    y: float,
) -> None:
    """Move the sockets of *v* that *links* attach to (all of them entering
    *v*, or all leaving it) onto the stack's representative node."""
    assert is_real(v)
    external_links = [
        link
        for link in links
        if (link.fromnode if v != link.fromnode else link.tonode) not in node_stack.path
    ]

    if not external_links:
        return

    is_output = external_links[0].fromnode == v
    attr = "fromsock" if is_output else "tosock"
    external_links.sort(key=lambda link: getattr(link, attr).idx)

    for link in external_links:
        original = getattr(link, attr)
        sockets = node_stack.stack_sockets_to_originals
        i = max([s.idx for s in sockets], default=-1) + 1
        socket = Socket(
            node_stack.rep_node,
            i,
            is_output,
            original.dna.location[1] - v.node.top - y,
        )
        sockets[socket] = original
        setattr(link, attr, socket)


STACK_MARGIN_Y_FAC = 0.5
"""Fraction of the vertical margin kept between the nodes of a stack."""


def contracted_node_stacks(CG: ClusterGraph) -> list[NodeStack]:
    """Find the stacks and replace each in the graph by one node.

    A stack is a chain of two or more collapsed Math or Vector Math nodes
    in the same frame, each joined to the next by a single link. Where the
    nodes branch, the chains are chosen to use as many links as possible
    (:func:`max_linear_branching`). A link is left out of a chain when
    contracting it would create a cycle. The node that replaces a stack is
    as tall as the pile and takes over the stack's links to other nodes.
    Returns the stacks, for :func:`expand_node_stack`."""
    G = CG.G
    T = CG.T

    collapsed_math_nodes = [
        v
        for v in G
        if is_real(v)
        and v.node.is_collapsed
        and v.node.idname in {"ShaderNodeMath", "ShaderNodeVectorMath"}
    ]
    H = G.subgraph(collapsed_math_nodes)

    # Not across frames, and not where two nodes are joined by several links.
    for link in tuple(H.all_links()):
        if link.fromnode.cluster != link.tonode.cluster:
            H.remove_link(link)

    for u in H:
        for v in tuple(H.successors(u)):
            parallel = H.links_between(u, v)
            if len(parallel) > 1:
                for link in parallel:
                    H.remove_link(link)

    # Keep only chains, and only links that contract without a cycle.
    for c in weakly_connected_components(H):
        H_c = H.subgraph(c)
        B = max_linear_branching(H_c)
        for link in H_c.all_links():
            if not B.has_link(*link.ident):
                H.discard_link_between(*link.ident)

    for c in weakly_connected_components(H):
        for u, v in edges_preventing_acyclic_contraction(G, H.subgraph(c)):
            H.discard_link_between(u, v)

    for u, v in edges_preventing_acyclic_contraction(G, H):
        H.discard_link_between(u, v)

    # Replace each chain by one node.
    order = {v: i for i, v in enumerate(topological_sort(H))}
    node_stacks = []
    for c in weakly_connected_components(H):
        if len(c) == 1:
            continue

        rep_node = Node(type=Kind.STACK)
        path: list[Node] = sorted(c, key=order.get)  # type: ignore
        node_stack = NodeStack(rep_node, path)

        y = 0
        for v in path:
            relabel_sockets(G.in_links(v), v, node_stack, y)
            relabel_sockets(G.out_links(v), v, node_stack, y)
            y += v.height + CG.state.margin.y * STACK_MARGIN_Y_FAC

        rep_node.height = y
        rep_node.width = max([v.width for v in path])

        cluster = cast(Cluster, path[0].cluster)
        rep_node.cluster = cluster
        T.add_edge(cluster, rep_node)

        # A stack nothing else links to would otherwise never enter the
        # graph, and so never get a rank or a column.
        G.add_node(rep_node)
        entering = [k for v in path for k in G.in_links(v)]
        leaving = [k for v in path for k in G.out_links(v)]
        for link in (*entering, *leaving):
            u, v = link.fromnode, link.tonode
            if u in path and v in path:
                continue

            G.remove_link(link)
            e_ = (rep_node, v) if u in path else (u, rep_node)
            G.add_link(*e_, link.fromsock, link.tosock, weight=link.weight)

        G.remove_nodes(path)
        T.remove_nodes(path)

        node_stacks.append(node_stack)

    assert is_acyclic(G)

    for node_stack in node_stacks:
        _point_multi_input_orders_at_stack(G, CG.state, node_stack)

    return node_stacks


def _feeds(G: LayoutGraph[Node], source: Socket, target: Socket) -> bool:
    """Whether a link from *source* reaches *target*, directly or through
    reroutes."""
    links = [link for link in G.out_links(source.owner) if link.fromsock == source]
    while links:
        link = links.pop()
        if link.tosock == target:
            return True
        if link.tonode.is_reroute:
            links.extend(G.out_links(link.tonode))
    return False


def _point_multi_input_orders_at_stack(
    G: LayoutGraph[Node], state: LayoutState, node_stack: NodeStack
) -> None:
    """The saved multi-input orders name the socket each link comes from.
    Where that is a socket the stack took over, name the stack's socket
    instead. A socket with several outside links gets a stack socket per
    link, so the one that feeds the multi-input is picked."""
    stand_ins: dict[Socket, list[Socket]] = {}
    for stack_socket, original in node_stack.stack_sockets_to_originals.items():
        stand_ins.setdefault(original, []).append(stack_socket)

    for target, sort_ids in state.multi_input_sort_ids.items():
        for k, (source, sort_id) in enumerate(sort_ids):
            candidates = stand_ins.get(source)
            if not candidates:
                continue
            stand_in = next(
                (s for s in candidates if _feeds(G, s, target)), candidates[0]
            )
            sort_ids[k] = (stand_in, sort_id)


def _relabel_multi_input_sources(
    state: LayoutState, renamed: Mapping[Socket, Socket]
) -> None:
    """Rename the source sockets of the saved multi-input orders by
    *renamed*."""
    for sort_ids in state.multi_input_sort_ids.values():
        sort_ids[:] = [(renamed.get(s, s), i) for s, i in sort_ids]


def expand_node_stack(CG: ClusterGraph, node_stack: NodeStack) -> None:
    """Put the nodes of *node_stack* back in place of the node that stood
    for them. Its links go back to the sockets they came from. The nodes are
    piled downwards from its top, centred on it, with
    ``STACK_MARGIN_Y_FAC`` of the vertical margin between them."""
    G = CG.G
    rep_node = node_stack.rep_node
    path = node_stack.path

    for stack_socket, original_socket in node_stack.stack_sockets_to_originals.items():
        if stack_socket.is_output:
            for link in tuple(G.out_links(rep_node)):
                if link.fromsock != stack_socket:
                    continue

                G.remove_link(link)
                G.add_link(
                    original_socket.owner, link.tonode, original_socket, link.tosock
                )
        else:
            # The link into this socket of the stack; the last link into
            # the stack if none is.
            entering = list(G.in_links(rep_node))
            link = next((k for k in entering if k.tosock == stack_socket), entering[-1])
            u = link.fromnode
            G.remove_link_between(u, rep_node, link.key)
            G.add_link(u, original_socket.owner, link.fromsock, original_socket)

    G.add_nodes(path)

    i = rep_node.col.index(rep_node)
    rep_node.col[i:i] = path

    y = rep_node.y
    for v in path:
        CG.T.add_edge(cast(Cluster, rep_node.cluster), v)
        v.x = rep_node.x - (v.width - rep_node.width) / 2
        v.y = y
        y -= v.height + CG.state.margin.y * STACK_MARGIN_Y_FAC

    _relabel_multi_input_sources(CG.state, node_stack.stack_sockets_to_originals)
    CG.remove_nodes_from([rep_node])
