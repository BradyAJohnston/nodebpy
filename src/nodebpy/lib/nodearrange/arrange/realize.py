# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from itertools import chain
from math import isclose
from statistics import fmean

from bpy.types import Node as BlenderNode
from mathutils import Vector

from ..config import LayoutState
from ..utils import move
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
from .tree import Tree, edge_dfs


def is_safe_to_remove(v: Node, state: LayoutState) -> bool:
    if not is_real(v):
        return True

    if v.node.label:
        return False

    for val in state.multi_input_sort_ids.values():
        if any(v == i[0].owner for i in val):
            return False

    # Headless divergence: the addon requires the reroute's peers to be in
    # the selection; here the working set is the whole tree.
    return all(
        s.node is not None
        for s in chain(
            state.linked_sockets[v.node.inputs[0]],
            state.linked_sockets[v.node.outputs[0]],
        )
    )


def dissolve_reroute_edges(G: Tree[Node], path: list[Node], state: LayoutState) -> None:
    if not G.successors(path[-1]):
        return

    first = next(G.in_links(path[0]), None)
    if first is None:
        return

    u, o = first.fromnode, first.fromsock
    succ_inputs = [link.tosock for link in G.out_links(path[-1])]

    # Check if a reroute has been used to link the same output to the same multi-input multiple
    # times
    for link in G.out_links(u):
        if link.fromsock == o and link.tosock in succ_inputs:
            path.clear()
            return

    links = state.ntree.links
    for i in succ_inputs:
        G.add_link(u, i.owner, o, i)
        links.new(o.bpy, i.bpy)


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
        else:
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
    reroute = state.ntree.nodes.new(type="NodeReroute")
    assert reroute is not None
    assert v.cluster
    reroute.parent = v.cluster.node
    state.selected.append(reroute)
    v.node = reroute
    v.type = Kind.NODE


def realize_edges(G: Tree[Node], state: LayoutState) -> None:
    links = state.ntree.links
    for link in G.all_links():
        if link.fromnode.is_reroute or link.tonode.is_reroute:
            links.new(link.fromsock.bpy, link.tosock.bpy)


def realize_dummy_nodes(CG: ClusterGraph) -> None:
    for path in get_reroute_paths(
        CG, lambda v: is_safe_to_remove(v, CG.state), aligned=True
    ):
        simplify_path(CG, path)

        for v in path:
            if not is_real(v):
                add_reroute(v, CG.state)

    realize_edges(CG.G, CG.state)


def restore_multi_input_orders(G: Tree[Node], state: LayoutState) -> None:
    links = state.ntree.links
    H = socket_graph(G)
    for socket, sort_ids in state.multi_input_sort_ids.items():
        multi_input = socket.bpy
        assert multi_input

        as_links = {
            link.from_socket: link
            for link in links
            if link.to_socket == multi_input and link.from_socket is not None
        }

        # In graph order, not a set: bpy sockets hash by pointer, and the
        # creation order of these links sets their sort ids.
        for output in dict.fromkeys(s.bpy for s in H.predecessors(socket)):
            if output in as_links:
                continue
            assert output
            new_link = links.new(output, multi_input)
            assert new_link is not None
            as_links[output] = new_link

        if len(as_links) != len(
            {link.multi_input_sort_id for link in as_links.values()}
        ):
            for link in as_links.values():
                links.remove(link)

            for output in as_links:
                new_link = links.new(output, multi_input)
                assert new_link is not None
                as_links[output] = new_link

        SH = H.subgraph(
            {i[0] for i in sort_ids} | {socket} | {v for v in H if v.owner.is_reroute}
        )
        seen = set()
        for base_from_socket, sort_id in sort_ids:
            other = min(
                as_links.values(),
                key=lambda link: abs(link.multi_input_sort_id - sort_id),
            )
            from_socket = next(
                s
                for s, t in edge_dfs(SH, base_from_socket)
                if t == socket and s not in seen
            )
            output = from_socket.bpy
            assert output is not None
            as_links[output].swap_multi_input_sort_id(other)
            seen.add(from_socket)


def realize_locations(G: Tree[Node], old_center: Vector, state: LayoutState) -> None:
    new_center = (fmean([v.x for v in G]), fmean([v.y for v in G]))
    offset_x, offset_y = -Vector(new_center) + old_center

    for v in G:
        assert isinstance(v.node, BlenderNode)
        assert v.cluster

        # Optimization: avoid using bpy.ops for as many nodes as possible (see `utils.move()`)
        v.node.parent = None

        x, y = v.node.location
        v.x += offset_x
        v.y += offset_y
        move(v.node, state.selected, x=v.x - x, y=v.corrected_y() - y)

        v.node.parent = v.cluster.node


def resize_unshrunken_frame(CG: ClusterGraph, cluster: Cluster) -> None:
    frame = cluster.node

    if not frame or frame.shrink:
        return

    real_children = [v for v in CG.T.successors(cluster) if is_real(v)]

    for v in real_children:
        v.node.parent = None

    frame.shrink = False
    frame.shrink = True

    for v in real_children:
        v.node.parent = frame


def realize_layout(CG: ClusterGraph, old_center: Vector) -> None:
    if CG.state.settings.add_reroutes:
        realize_dummy_nodes(CG)

    restore_multi_input_orders(CG.G, CG.state)
    realize_locations(CG.G, old_center, CG.state)
    for c in CG.S:
        resize_unshrunken_frame(CG, c)
