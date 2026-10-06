"""Turn the finished layout into edits: reroutes for the dummy nodes that
remain, links through them, and a position for every node. Also the removal
of the tree's own reroutes before the layout, when it replaces them."""

from __future__ import annotations

from math import isclose
from statistics import fmean

from .common import Vec2, f32
from .config import LayoutState
from .digraph import LayoutGraph, descendants
from .dna import new_reroute
from .edits import AddLink, AddReroute, MoveNode, ResizeFrame, RestoreMultiInputOrder
from .long_links import get_reroute_paths
from .model import (
    Cluster,
    ClusterGraph,
    Kind,
    Node,
    Socket,
    add_dummy_link,
    is_real,
    socket_graph,
    trace_multi_input_sources,
)
from .reroutes import chain_ends


def is_safe_to_remove(v: Node, state: LayoutState) -> bool:
    """Whether the layout may remove *v*: a made-up node, or a reroute that
    has no label, is not the source a saved multi-input order names, and is
    not linked to a fixed node."""
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


def dissolve_reroute_links(
    G: LayoutGraph[Node], path: list[Node], state: LayoutState
) -> None:
    """Link the source of the reroute chain *path* straight to every input
    the chain feeds, and record the links as edits. When the source already
    feeds one of those inputs directly, *path* is emptied instead, which
    keeps the chain."""
    output, inputs = chain_ends(G, path)

    # A reroute can link an output to a multi-input it already feeds.
    for link in G.out_links(output.owner):
        if link.fromsock == output and link.tosock in inputs:
            path.clear()
            return

    for i in inputs:
        G.add_link(output.owner, i.owner, output, i)
        state.edits.append(AddLink(output.dna, i.dna))


def remove_reroutes(CG: ClusterGraph) -> None:
    """Take the tree's own reroutes out where :func:`is_safe_to_remove`
    allows, linking each chain's source straight to what it feeds. In a
    frame that holds only reroutes, a chain keeps its two ends. Chains that
    lead nowhere or come from nowhere stay."""
    reroute_clusters = {
        c
        for c in CG.S
        if all(not isinstance(v, Cluster) and v.is_reroute for v in CG.T.successors(c))
    }
    for path in get_reroute_paths(CG, lambda v: is_safe_to_remove(v, CG.state)):
        if path[0].cluster in reroute_clusters:
            if len(path) > 2:
                u, *between, v = path
                add_dummy_link(CG.G, u, v)
                CG.remove_nodes(between)
        elif CG.G.predecessors(path[0]) and CG.G.successors(path[-1]):
            # A chain that comes from nowhere or leads nowhere is someone's
            # work in progress, and stays.
            dissolve_reroute_links(CG.G, path, CG.state)
            CG.remove_nodes(path)


_Y_TOL = 5


def simplify_path(CG: ClusterGraph, path: list[Node]) -> None:
    """Remove the nodes of the level chain *path* that a straight link
    replaces, from the graph and from *path*: all but its two ends, and an
    end too when it is level, within ``_Y_TOL``, with the socket it joins.
    A chain of one dummy node goes when the sockets either side of it are
    level."""
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
        if isclose(p.y, q.y, abs_tol=_Y_TOL):
            G.add_link(p.owner, q.owner, p, q)
            CG.remove_nodes(path)
            path.clear()

        return

    u, *between, v = path

    # Each end goes too when it is level with the socket beyond it.
    p = pred_output(u) if G.predecessors(u) else None
    if p is not None and isclose(p.y, u.y, abs_tol=_Y_TOL):
        between.append(u)
    else:
        p = Socket(u, 0, True)

    q = succ_input(v) if G.out_degree(v) == 1 else None
    if q is not None and isclose(v.y, q.y, abs_tol=_Y_TOL):
        between.append(v)
    else:
        q = Socket(v, 0, False)

    if p.owner != u or q.owner != v or between:
        G.add_link(p.owner, q.owner, p, q)

    CG.remove_nodes(between)
    for v in between:
        path.remove(v)


def add_reroute(v: Node, state: LayoutState) -> None:
    """Make the dummy node *v* stand for a new reroute, and record the
    ``AddReroute`` edit."""
    assert v.cluster
    reroute = new_reroute(parent=v.cluster.node)
    state.edits.append(AddReroute(reroute))
    v.node = reroute
    v.type = Kind.NODE


def realize_links(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Record an ``AddLink`` edit for every link that starts or ends at a
    reroute."""
    for link in G.all_links():
        if link.fromnode.is_reroute or link.tonode.is_reroute:
            state.edits.append(AddLink(link.fromsock.dna, link.tosock.dna))


def realize_dummy_nodes(CG: ClusterGraph) -> None:
    """Simplify each chain of reroutes and dummy nodes, turn the dummy nodes
    that remain into reroutes, and record the links through them."""
    for path in get_reroute_paths(
        CG, lambda v: is_safe_to_remove(v, CG.state), aligned=True
    ):
        simplify_path(CG, path)

        for v in path:
            if not is_real(v):
                add_reroute(v, CG.state)

    realize_links(CG.G, CG.state)


def restore_multi_input_orders(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Record, for every multi-input socket, which sockets now feed it and
    the order their links must be put back in."""
    H = socket_graph(G)
    for socket, sort_ids in state.multi_input_sort_ids.items():
        outputs = tuple(dict.fromkeys(s.dna for s in H.predecessors(socket)))
        order = tuple(
            (from_socket.dna, sort_id)
            for from_socket, sort_id in trace_multi_input_sources(H, socket, sort_ids)
        )
        state.edits.append(RestoreMultiInputOrder(socket.dna, outputs, order))


def realize_locations(
    G: LayoutGraph[Node], old_center: Vec2, state: LayoutState
) -> None:
    """Record a ``MoveNode`` edit for every node, with the layout centred
    on *old_center*."""
    # Centre in single precision, like the node locations themselves.
    offset_x = f32(old_center.x - f32(fmean([v.x for v in G])))
    offset_y = f32(old_center.y - f32(fmean([v.y for v in G])))

    for v in G:
        assert v.node is not None
        assert v.cluster

        v.x += offset_x
        v.y += offset_y
        state.edits.append(MoveNode(v.node, (v.x, v.y), v.cluster.node))


def resize_unshrunken_frame(CG: ClusterGraph, cluster: Cluster) -> None:
    """Record a ``ResizeFrame`` edit for a frame with Shrink off."""
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
    """Record the edits for the finished layout: with reroutes on, the
    reroutes, their links and the multi-input orders, then every node's
    position and the frames to refit."""
    if CG.state.options.reroutes != "none":
        realize_dummy_nodes(CG)

        # Only rerouting touches links, and so their order.
        restore_multi_input_orders(CG.G, CG.state)
    realize_locations(CG.G, old_center, CG.state)
    for c in CG.S:
        resize_unshrunken_frame(CG, c)
