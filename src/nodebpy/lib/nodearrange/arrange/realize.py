# SPDX-License-Identifier: GPL-2.0-or-later
"""Turn the finished layout into edits: reroutes for the dummy nodes that
remain, links through them, and a position for every node. Also the removal
of the tree's own reroutes before the layout, when it replaces them."""

from __future__ import annotations

from math import isclose
from statistics import fmean

from ..config import LayoutState
from ..dna import new_reroute
from .common import Vec2, f32
from .digraph import LayoutGraph, descendants, edge_dfs
from .edits import AddLink, AddReroute, MoveNode, ResizeFrame, RestoreMultiInputOrder
from .graph import (
    Cluster,
    ClusterGraph,
    Kind,
    Node,
    Socket,
    add_dummy_edge,
    get_reroute_paths,
    is_real,
    socket_graph,
)


def is_safe_to_remove(v: Node, state: LayoutState) -> bool:
    if not is_real(v):
        return True

    if v.node.label:
        return False

    for val in state.multi_input_sort_ids.values():
        if any(v == i[0].owner for i in val):
            return False

    # A reroute that also links to a node outside the selection stays: the
    # layout does not know that link, and would lose it with the reroute.
    return all(
        peer.node not in state.fixed
        for socket in (*v.node.inputs, *v.node.outputs)
        for peer in state.linked_sockets.get(socket, ())
    )


def is_dangling(G: LayoutGraph[Node], path: list[Node]) -> bool:
    """Whether a chain of reroutes leads nowhere, or comes from nowhere."""
    return not G.successors(path[-1]) or not G.predecessors(path[0])


def dissolve_reroute_edges(
    G: LayoutGraph[Node], path: list[Node], state: LayoutState
) -> None:
    first = next(G.in_links(path[0]))

    u, o = first.fromnode, first.fromsock
    succ_inputs = [link.tosock for link in G.out_links(path[-1])]

    # Check if a reroute has been used to link the same output to the same multi-input multiple
    # times
    for link in G.out_links(u):
        if link.fromsock == o and link.tosock in succ_inputs:
            path.clear()
            return

    for i in succ_inputs:
        G.add_link(u, i.owner, o, i)
        state.edits.append(AddLink(o.dna, i.dna))


def remove_reroutes(CG: ClusterGraph) -> None:
    reroute_clusters = {
        c
        for c in CG.S
        if all(v.type != Kind.CLUSTER and v.is_reroute for v in CG.T.successors(c))
    }
    for path in get_reroute_paths(CG, lambda v: is_safe_to_remove(v, CG.state)):
        if path[0].cluster in reroute_clusters:
            if len(path) > 2:
                u, *between, v = path
                add_dummy_edge(CG.G, u, v)
                CG.remove_nodes_from(between)
        elif not is_dangling(CG.G, path):
            # nodebpy divergence: reroutes left dangling are someone's work
            # in progress; upstream deletes them with their links.
            dissolve_reroute_edges(CG.G, path, CG.state)
            CG.remove_nodes_from(path)


_Y_TOL = 5


def simplify_path(CG: ClusterGraph, path: list[Node]) -> None:
    G = CG.G

    def pred_output(w: Node) -> Socket:
        return next(G.in_links(w)).fromsock

    def succ_input(w: Node) -> Socket:
        return next(G.out_links(w)).tosock

    if len(path) == 1:
        v = path[0]

        if not G.predecessors(v) or G.out_degree(v) != 1 or v.col is None or is_real(v):
            return

        p = pred_output(v)
        q = succ_input(v)
        if isclose(p.y, q.y, rel_tol=0, abs_tol=_Y_TOL):
            G.add_link(p.owner, q.owner, p, q)
            CG.remove_nodes_from(path)
            path.clear()

        return

    u, *between, v = path

    if G.predecessors(u) and isclose(
        (p := pred_output(u)).y, u.y, rel_tol=0, abs_tol=_Y_TOL
    ):
        between.append(u)
    else:
        p = Socket(u, 0, True)

    if G.out_degree(v) == 1 and isclose(
        v.y, (q := succ_input(v)).y, rel_tol=0, abs_tol=_Y_TOL
    ):
        between.append(v)
    else:
        q = Socket(v, 0, False)

    if p.owner != u or q.owner != v or between:
        G.add_link(p.owner, q.owner, p, q)

    CG.remove_nodes_from(between)
    for v in between:
        path.remove(v)


def add_reroute(v: Node, state: LayoutState) -> None:
    assert v.cluster
    reroute = new_reroute(parent=v.cluster.node)
    state.edits.append(AddReroute(reroute))
    v.node = reroute
    v.type = Kind.NODE


def realize_edges(G: LayoutGraph[Node], state: LayoutState) -> None:
    for link in G.all_links():
        if link.fromnode.is_reroute or link.tonode.is_reroute:
            state.edits.append(AddLink(link.fromsock.dna, link.tosock.dna))


def realize_dummy_nodes(CG: ClusterGraph) -> None:
    for path in get_reroute_paths(
        CG, lambda v: is_safe_to_remove(v, CG.state), aligned=True
    ):
        simplify_path(CG, path)

        for v in path:
            if not is_real(v):
                add_reroute(v, CG.state)

    realize_edges(CG.G, CG.state)


def restore_multi_input_orders(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Record, for every multi-input socket, which sockets now feed it and
    the order their links must be put back in."""
    H = socket_graph(G)
    for socket, sort_ids in state.multi_input_sort_ids.items():
        outputs = tuple(dict.fromkeys(s.dna for s in H.predecessors(socket)))

        SH = H.subgraph(
            {i[0] for i in sort_ids} | {socket} | {v for v in H if v.owner.is_reroute}
        )
        seen = set()
        order = []
        for base_from_socket, sort_id in sort_ids:
            from_socket = next(
                s
                for s, t in edge_dfs(SH, base_from_socket)
                if t == socket and s not in seen
            )
            order.append((from_socket.dna, sort_id))
            seen.add(from_socket)

        state.edits.append(RestoreMultiInputOrder(socket.dna, outputs, tuple(order)))


def realize_locations(
    G: LayoutGraph[Node], old_center: Vec2, state: LayoutState
) -> None:
    # Keep the layout centred where the nodes were (in single precision,
    # like the node locations themselves).
    offset_x = f32(old_center.x - f32(fmean([v.x for v in G])))
    offset_y = f32(old_center.y - f32(fmean([v.y for v in G])))

    for v in G:
        assert v.node is not None
        assert v.cluster

        v.x += offset_x
        v.y += offset_y
        state.edits.append(MoveNode(v.node, (v.x, v.y), v.cluster.node))


def resize_unshrunken_frame(CG: ClusterGraph, cluster: Cluster) -> None:
    frame = cluster.node

    if not frame or frame.shrink:
        return

    # Every node in the frame, those of the frames inside it included.
    children = tuple(
        v.node
        for v in descendants(CG.T, cluster)
        if not isinstance(v, Cluster) and is_real(v)
    )
    CG.state.edits.append(ResizeFrame(frame, children))


def realize_layout(CG: ClusterGraph, old_center: Vec2) -> None:
    if CG.state.settings.reroutes != "none":
        realize_dummy_nodes(CG)

        # Only rerouting touches links, and so their order.
        restore_multi_input_orders(CG.G, CG.state)
    realize_locations(CG.G, old_center, CG.state)
    for c in CG.S:
        resize_unshrunken_frame(CG, c)
