"""The route phase: give a link a bend point beside a node it would
otherwise cut across (:func:`route_edges`)."""

from __future__ import annotations

from collections import defaultdict
from itertools import chain

from .common import FRAME_PADDING, group_by, segments_intersect
from .config import LayoutState
from .digraph import DiGraph, LayoutGraph, Link
from .long_links import add_dummy_nodes_to_edge, lowest_common_cluster
from .model import Cluster, Kind, Node, Socket

_MIN_X_DIFF = 30
_MIN_Y_DIFF = 8


def is_unnecessary_bend_point(
    socket: Socket, other_socket: Socket, state: LayoutState
) -> bool:
    """Whether the link from *socket* to *other_socket*, drawn straight,
    does not cross the near edge of the node next to *socket*'s node in its
    column, on the side the link heads to. That edge is padded by half the
    margin, and by the frame padding when the neighbour is in another
    frame. True when there is no such neighbour or it is a reroute. False
    for a reroute's own socket."""
    v = socket.owner

    if v.is_reroute:
        return False

    i = v.col.index(v)
    is_above = other_socket.y > socket.y

    j = i - 1 if is_above else i + 1
    if not 0 <= j < len(v.col):
        return True
    nbr = v.col[j]

    if nbr.is_reroute:
        return True

    nbr_x_offset, nbr_y_offset = state.margin.x / 2, state.margin.y / 2
    nbr_y = nbr.y - nbr.height - nbr_y_offset if is_above else nbr.y + nbr_y_offset

    assert nbr.cluster
    if nbr.cluster.node and nbr.cluster != v.cluster:
        nbr_x_offset += FRAME_PADDING
        if is_above:
            nbr_y -= FRAME_PADDING
        else:
            nbr_y += FRAME_PADDING + nbr.cluster.label_height()

    line_a = ((nbr.x - nbr_x_offset, nbr_y), (nbr.x + nbr.width + nbr_x_offset, nbr_y))
    line_b = ((socket.x, socket.y), (other_socket.x, other_socket.y))
    return not segments_intersect(*line_a, *line_b)


def add_bend_points(
    G: LayoutGraph[Node],
    v: Node,
    bend_points: defaultdict[Link[Node], list[Node]],
    state: LayoutState,
) -> None:
    """Add to *bend_points* a bend point for each link of *v* that needs
    one. It goes at the height of the link's socket on *v*, at the edge of
    the widest node of the column. A link needs none when its socket is
    within ``_MIN_X_DIFF`` of that edge, when its other end is within
    ``_MIN_Y_DIFF`` of the same height, or when
    :func:`is_unnecessary_bend_point` holds."""
    largest = max(v.col, key=lambda w: w.width)
    for link in (*G.out_links(v), *G.in_links(v)):
        socket: Socket = link.fromsock if v == link.fromnode else link.tosock
        bend_point = Node(type=Kind.DUMMY)
        bend_point.x = largest.x + largest.width if socket.is_output else largest.x

        if abs(socket.x - bend_point.x) <= _MIN_X_DIFF:
            continue

        bend_point.y = socket.y
        other_socket = next(s for s in (link.fromsock, link.tosock) if s != socket)

        if abs(other_socket.y - bend_point.y) <= _MIN_Y_DIFF:
            continue

        if is_unnecessary_bend_point(socket, other_socket, state):
            continue

        bend_points[link].append(bend_point)


def node_overlaps_edge(
    v: Node,
    edge_line: tuple[tuple[float, float], tuple[float, float]],
) -> bool:
    """Whether the segment *edge_line* crosses the top or bottom edge of
    *v*. Never for a reroute."""
    if v.is_reroute:
        return False

    top_line = ((v.x, v.y), (v.x + v.width, v.y))
    if segments_intersect(*edge_line, *top_line):
        return True

    bottom_line = (
        (v.x, v.y - v.height),
        (v.x + v.width, v.y - v.height),
    )
    return segments_intersect(*edge_line, *bottom_line)


def route_edges(
    G: LayoutGraph[Node], T: DiGraph[Node | Cluster], state: LayoutState
) -> None:
    """Give every link that would cut across a node next to one of its ends
    a bend point beside that node. The bend points become dummy nodes on
    the link, in the innermost cluster that holds both its ends."""
    bend_points: defaultdict[Link[Node], list[Node]] = defaultdict(list)
    for v in chain(*G.columns):
        add_bend_points(G, v, bend_points, state)

    # Links from one output with a bend point at the same place share it.
    edge_of = {b: e for e, d in bend_points.items() for b in d}

    def key(b):
        return (edge_of[b].fromsock, b.x, b.y)

    for (target, *redundant), (from_socket, *_) in group_by(edge_of, key=key).items():
        for b in redundant:
            dummy_nodes = bend_points[edge_of[b]]
            dummy_nodes[dummy_nodes.index(b)] = target

        u = from_socket.owner
        if not u.is_reroute or G.out_degree(u) < 2:
            continue

        for e in G.out_links(u):
            if target not in bend_points[e] and e.tosock.y == target.y:
                bend_points[e].append(target)

    # Another link from the same output follows these bend points too, when
    # it can go straight on from the last one without crossing a node.
    for e, dummy_nodes in tuple(bend_points.items()):
        dummy_nodes.sort(key=lambda b: b.x)
        from_socket = e.fromsock
        for e_ in G.out_links(e.fromnode):
            if e_.fromsock != from_socket or e_ in bend_points:
                continue

            if e_.tosock.x <= dummy_nodes[-1].x:
                continue

            b = dummy_nodes[-1]
            line = ((b.x, b.y), (e_.tosock.x, e_.tosock.y))
            if any(node_overlaps_edge(v, line) for v in e.tonode.col):
                continue

            bend_points[e_] = dummy_nodes

    lca = lowest_common_cluster(T, bend_points)
    for link, dummy_nodes in bend_points.items():
        add_dummy_nodes_to_edge(G, link, dummy_nodes, state)

        u, v = link.fromnode, link.tonode
        c = lca.get((u, v), u.cluster)
        assert c is not None
        for w in dummy_nodes:
            w.cluster = c
            T.add_edge(c, w)
