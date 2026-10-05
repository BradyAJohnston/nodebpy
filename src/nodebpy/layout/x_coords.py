# SPDX-License-Identifier: GPL-2.0-or-later
"""Across the columns: an x for every column (:func:`assign_x_coords`), and
the route phase, which gives a link a bend point beside a node it would
otherwise cut across (:func:`route_edges`)."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection, Sequence
from itertools import chain
from typing import cast

from .common import frame_padding, group_by, segments_intersect
from .config import LayoutState
from .digraph import DiGraph, LayoutGraph, Link, ancestors, dag_longest_path_length
from .graph import (
    Cluster,
    Kind,
    Node,
    Socket,
    add_dummy_nodes_to_edge,
    lowest_common_cluster,
)


def frame_padding_of_col(
    columns: Sequence[Collection[Node]],
    i: int,
    T: DiGraph[Node | Cluster],
) -> float:
    col = columns[i]

    if col == columns[-1]:
        return 0

    clusters1 = {cast(Cluster, v.cluster) for v in col}
    clusters2 = {cast(Cluster, v.cluster) for v in columns[i + 1]}

    if not clusters1 ^ clusters2:
        return 0

    ST1 = T.subgraph(chain(clusters1, *[ancestors(T, c) for c in clusters1]))
    ST2 = T.subgraph(chain(clusters2, *[ancestors(T, c) for c in clusters2]))

    for u, v in tuple(ST1.edges()):
        ST1.set_weight(u, v, int(not ST2.has_edge(u, v)))

    for u, v in tuple(ST2.edges()):
        ST2.set_weight(u, v, int(not ST1.has_edge(u, v)))

    dist = dag_longest_path_length(ST1) + dag_longest_path_length(ST2)
    return frame_padding() * dist


def assign_x_coords(
    G: LayoutGraph[Node], T: DiGraph[Node | Cluster], state: LayoutState
) -> None:
    columns: list[list[Node]] = G.columns
    x = 0
    for i, col in enumerate(columns):
        if not col:
            # A rank whose only occupants were dummy nodes (dissolved when
            # reroutes are not added) takes no space.
            continue
        max_width = max([v.width for v in col])

        for v in col:
            v.x = x if v.is_reroute else x - (v.width - max_width) / 2

        # https://doi.org/10.7155/jgaa.00220 (p. 139)
        delta_i = sum(
            [
                1
                for link in G.out_links(col)
                if abs(link.tosock.y - link.fromsock.y) >= state.margin.x * 3
            ]
        )
        spacing = (1 + min(delta_i / 4, 2)) * state.margin.x
        x += max_width + spacing + frame_padding_of_col(columns, i, T)


_MIN_X_DIFF = 30
_MIN_Y_DIFF = 8


def is_unnecessary_bend_point(
    socket: Socket, other_socket: Socket, state: LayoutState
) -> bool:
    v = socket.owner

    if v.is_reroute:
        return False

    i = v.col.index(v)
    is_above = other_socket.y > socket.y

    try:
        nbr = v.col[i - 1] if is_above else v.col[i + 1]
    except IndexError:
        return True

    if nbr.is_reroute:
        return True

    nbr_x_offset, nbr_y_offset = state.margin.x / 2, state.margin.y / 2
    nbr_y = nbr.y - nbr.height - nbr_y_offset if is_above else nbr.y + nbr_y_offset

    assert nbr.cluster
    if nbr.cluster.node and nbr.cluster != v.cluster:
        nbr_x_offset += frame_padding()
        if is_above:
            nbr_y -= frame_padding()
        else:
            nbr_y += frame_padding() + nbr.cluster.label_height()

    line_a = ((nbr.x - nbr_x_offset, nbr_y), (nbr.x + nbr.width + nbr_x_offset, nbr_y))
    line_b = ((socket.x, socket.y), (other_socket.x, other_socket.y))
    return not segments_intersect(*line_a, *line_b)


def add_bend_points(
    G: LayoutGraph[Node],
    v: Node,
    bend_points: defaultdict[Link[Node], list[Node]],
    state: LayoutState,
) -> None:
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
    bend_points: defaultdict[Link[Node], list[Node]] = defaultdict(list)
    for v in chain(*G.columns):
        add_bend_points(G, v, bend_points, state)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    lca = lowest_common_cluster(T, bend_points)
    for link, dummy_nodes in bend_points.items():
        add_dummy_nodes_to_edge(G, link, dummy_nodes, state)

        u, v = link.fromnode, link.tonode
        c = lca.get((u, v), u.cluster)
        assert c is not None
        for w in dummy_nodes:
            w.cluster = c
            T.add_edge(c, w)
