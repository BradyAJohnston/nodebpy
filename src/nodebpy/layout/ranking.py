# SPDX-License-Identifier: GPL-2.0-or-later
"""The rank phase: give every node a column (:func:`compute_ranks`).

Network simplex (Gansner et al., below) over the *nesting graph*: the
layout graph plus two border nodes per frame, linked so that a frame's
nodes stay between them. See ``DESIGN.md``."""

# http://dx.doi.org/10.1109/32.221135

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from math import sqrt
from typing import TYPE_CHECKING, Any

from .common import group_by
from .digraph import (
    DiGraph,
    LayoutGraph,
    Link,
    strongly_connected_components,
    topological_generations,
    weakly_connected_components,
)
from .graph import Cluster, Kind, MultiEdge, Node

if TYPE_CHECKING:
    from .sugiyama import ClusterGraph


# https://api.semanticscholar.org/CorpusID:14932050
def get_nesting_graph(CG: ClusterGraph) -> LayoutGraph[Node]:
    H = CG.G.copy()
    for u, v in CG.T.edges():
        if isinstance(u, Cluster):
            if not isinstance(v, Cluster):
                H.add_link(u.left, v)
                H.add_link(v, u.right)
            else:
                H.add_link(u.left, v.left)
                H.add_link(v.right, u.right)

    if CG.state.settings.sequential_frames:
        add_frame_sequence_edges(CG, H)

    return H


def _top_level_unit(v: Node, root: Cluster) -> Node | Cluster:
    """The outermost frame (a child of *root*) containing *v*, or *v* itself
    when it sits directly in the root."""
    unit: Node | Cluster = v
    c = v.cluster
    while c is not None and c is not root:
        unit = c
        c = c.cluster
    return unit


def add_frame_sequence_edges(CG: ClusterGraph, H: LayoutGraph[Node]) -> None:
    """Rank frames as stages of the flow.

    With plain nesting constraints a frame only has to enclose its own
    members, so a downstream frame's first nodes are ranked right next to the
    upstream frame's last ones and the two frames share columns — which
    forces them to be stacked vertically, producing a staircase of frames
    instead of a left-to-right flow. This adds, for every link between two
    top-level units (a frame, or a node outside every frame), a constraint
    from the source unit's right border to the target unit's left border:
    every node of a frame comes after every node of the frame (or the
    intermediate node) feeding it. Nodes without predecessors (inputs and
    values serving one consumer) and without successors are exempt so they
    stay next to their consumer / producer; units on a cycle of the quotient
    graph are left to the plain nesting constraints.
    """
    G = CG.G
    root = next(c for c in CG.S if not CG.T.predecessors(c))
    unit_of = {v: _top_level_unit(v, root) for v in G}

    Q: DiGraph[Node | Cluster] = DiGraph()
    Q.add_nodes(dict.fromkeys(unit_of.values()))
    for link in G.all_links():
        a, b = unit_of[link.fromnode], unit_of[link.tonode]
        if a is not b:
            Q.add_edge(a, b)

    scc_of = {
        n: i for i, comp in enumerate(strongly_connected_components(Q)) for n in comp
    }
    for a, b in Q.edges():
        if scc_of[a] == scc_of[b]:
            continue
        a_is_frame = isinstance(a, Cluster)
        b_is_frame = isinstance(b, Cluster)
        if not a_is_frame and not b_is_frame:
            continue
        if not a_is_frame and not G.predecessors(a):
            continue
        if not b_is_frame and not G.successors(b):
            continue
        tail = a.right if isinstance(a, Cluster) else a
        head = b.left if isinstance(b, Cluster) else b
        H.add_link(tail, head)
        CG.state.frame_sequence.append(
            (
                frozenset(v for v in G if unit_of[v] is a),
                frozenset(v for v in G if unit_of[v] is b),
            )
        )


@cache
def get_adj_edges_H(H: LayoutGraph[Node], v: Node) -> tuple[MultiEdge, ...]:
    return tuple(
        link.ident for links in (H.in_links(v), H.out_links(v)) for link in links
    )


@cache
def get_adj_edges_T(T: LayoutGraph[Node], v: Node) -> tuple[MultiEdge, ...]:
    return tuple(
        link.ident for links in (T.in_links(v), T.out_links(v)) for link in links
    )


def get_slack(e: MultiEdge) -> int:
    u, v, _ = e
    min_length = 1
    return v.rank - u.rank - min_length


def tight_tree(H: LayoutGraph[Node], T: LayoutGraph[Node], root: Node) -> int:
    """Grow *T* from *root* over the links without slack, depth first, and
    return its size. (An explicit stack: the tree can be as deep as the
    graph is long.)"""
    visited: set[MultiEdge] = set()
    T.add_node(root)
    stack = [(root, iter(get_adj_edges_H(H, root)))]
    while stack:
        v, edges = stack[-1]
        for e in edges:
            if e in visited:
                continue

            visited.add(e)

            u, w, k = e
            other = u if v != u else w
            if not T.has_link(u, w, k):
                if other in T or get_slack(e) != 0:
                    continue
                T.add_link(u, w, key=k)

            stack.append((other, iter(get_adj_edges_H(H, other))))
            break
        else:
            stack.pop()

    return len(T)


type _Parents = dict[Node, tuple[Node, Link[Node]]]
"""For each node of the spanning tree but its root: the node above it, and
the tree link between the two."""


def set_post_order_numbers(
    top: Node, T: LayoutGraph[Node], parents: _Parents | None = None
) -> _Parents:
    """Number the nodes of the spanning tree *T* in post-order, and give
    each the lowest number in its subtree. Returns each node's parent.

    Without *parents* the whole tree is numbered, with *top* as its root.
    With the parents of an earlier numbering only the subtree below *top*
    is numbered again, within the numbers it had: enough after an exchange
    of two links that are both in that subtree."""
    if parents is None:
        parents = {}
        num = 0
        visited: set[Link[Node]] = set()
    else:
        num = top.lowest_po_num
        visited = {parents[top][1]} if top in parents else set()

    def tree_links(v: Node) -> list[Link[Node]]:
        return [*T.in_links(v), *T.out_links(v)]

    # Each entry: a node, its remaining tree links, the lowest number below.
    stack: list[list[Any]] = [[top, iter(tree_links(top)), None]]
    while stack:
        w, links, lowest = stack[-1]
        for link in links:
            if link in visited:
                continue

            visited.add(link)
            child = link.fromnode if link.tonode is w else link.tonode
            parents[child] = (w, link)
            stack.append([child, iter(tree_links(child)), None])
            break
        else:
            stack.pop()
            w.po_num = num
            w.lowest_po_num = num if lowest is None else min(lowest, num)
            num += 1
            if stack:
                parent = stack[-1]
                if parent[2] is None or w.lowest_po_num < parent[2]:
                    parent[2] = w.lowest_po_num

    return parents


def _is_above(v: Node, w: Node) -> bool:
    """Whether *w* is *v* or below it in the numbered spanning tree."""
    return v.lowest_po_num <= w.po_num <= v.po_num


def tree_path(
    start: Node, end: Node, parents: _Parents
) -> tuple[Node, list[tuple[Link[Node], bool]]]:
    """The way through the spanning tree from *start* to *end*: the highest
    node on it, and its links, each with whether the path runs along it
    from its ``fromnode`` to its ``tonode``."""
    path = []
    v = start
    while not _is_above(v, end):
        v, link = parents[v]
        path.append((link, link.tonode is v))
    top = v
    v = end
    while v is not top:
        v, link = parents[v]
        path.append((link, link.fromnode is v))
    return top, path


def compute_cut_values(H: LayoutGraph[Node], T: LayoutGraph[Node]) -> None:
    unknown_cut_values = {}
    leaves = []
    for v in H:
        adj_edges = get_adj_edges_T(T, v)
        unknown_cut_values[v] = list(adj_edges)
        if len(adj_edges) == 1:
            leaves.append(v)

    for v in leaves:
        while len(unknown_cut_values[v]) == 1:
            to_determine = unknown_cut_values[v][0]
            d = T.link(*to_determine)
            d.cut_value = H.link(*to_determine).weight
            u, w, _ = to_determine
            for e in get_adj_edges_H(H, v):
                if e == to_determine:
                    continue

                weight = H.link(*e).weight
                if T.has_link(*e):
                    if u == e[0] or w == e[1]:
                        d.cut_value -= T.link(*e).cut_value - weight
                    else:
                        d.cut_value += T.link(*e).cut_value - weight
                else:
                    if (v == u and e[0] != v) or (v != u and e[0] == v):
                        weight = -weight
                    d.cut_value += weight

            unknown_cut_values[u].remove(to_determine)
            unknown_cut_values[w].remove(to_determine)
            v = w if u == v else u


def longest_path_ranks(H: LayoutGraph[Node]) -> None:
    """Rank every node as late as its successors allow: one column before
    the earliest of them, the nodes without successors in the last column."""
    generations = topological_generations(H.reversed())
    for i, col in enumerate(reversed(tuple(generations))):
        for v in col:
            v.rank = i


def feasible_tree(H: LayoutGraph[Node]) -> tuple[LayoutGraph[Node], _Parents]:
    longest_path_ranks(H)

    T: LayoutGraph[Node] = LayoutGraph()
    v_root = next(iter(H))

    while tight_tree(H, T, v_root) < len(H):
        incident_edges = [
            link.ident
            for link in H.all_links()
            if (link.fromnode in T) ^ (link.tonode in T)
        ]
        e = min(incident_edges, key=get_slack)
        slack = -get_slack(e) if e[1] in T else get_slack(e)
        for v in T:
            v.rank += slack

    parents = set_post_order_numbers(v_root, T)
    compute_cut_values(H, T)

    return T, parents


def leave_edge(T: LayoutGraph[Node]) -> MultiEdge | None:
    return next((link.ident for link in T.all_links() if link.cut_value < 0), None)


def is_in_head(v: Node, e: MultiEdge) -> bool:
    u, w, _ = e

    if (
        u.lowest_po_num <= v.po_num
        and v.po_num <= u.po_num
        and w.lowest_po_num <= v.po_num
        and v.po_num <= w.po_num
    ):
        return u.po_num >= w.po_num

    return u.po_num < w.po_num


def enter_edge(H: LayoutGraph[Node], e: MultiEdge) -> MultiEdge:
    edges = [
        link.ident
        for link in H.all_links()
        if is_in_head(link.fromnode, e) and not is_in_head(link.tonode, e)
    ]
    return min(edges, key=get_slack)


def exchange(
    H: LayoutGraph[Node],
    T: LayoutGraph[Node],
    parents: _Parents,
    leave: MultiEdge,
    enter: MultiEdge,
) -> _Parents:
    """Swap the tree link *leave* for the link *enter*, and bring the ranks,
    the cut values and the numbering up to date. Returns the parents.

    Only the cut values around the cycle *enter* closes in the tree change,
    by the cut value of *leave*: up for the links that run around the cycle
    the way *enter* does, down for the others."""
    tail, head, key = enter
    cut_value = T.link(*leave).cut_value
    top, cycle = tree_path(head, tail, parents)
    for link, forwards in cycle:
        link.cut_value += -cut_value if forwards else cut_value

    T.remove_link_between(*leave)
    T.add_link(tail, head, key=key)
    T.link(tail, head, key).cut_value = -cut_value

    slack = get_slack(enter)
    if not is_in_head(enter[1], leave):
        slack = -slack

    for v in H:
        if not is_in_head(v, leave):
            v.rank += slack

    # Both links are below the top of the cycle, so the tree is as it was
    # everywhere else.
    return set_post_order_numbers(top, T, parents)


def normalize_and_balance(CG: ClusterGraph, H: LayoutGraph[Node]) -> None:
    for cc in weakly_connected_components(CG.G):
        c = cc[0].cluster
        assert c

        if any(v.cluster != c for v in cc):
            continue

        ranked = group_by(cc, key=lambda v: v.rank, sort=True)

        if c.node:
            start = min(v.rank for v in CG.T.successors(c) if v.type != Kind.CLUSTER)
        else:
            start = c.left.rank - (max(ranked.values()) - min(ranked.values()))

        for i, col in enumerate(ranked, start):
            for v in col:
                v.rank = i

    col_sizes = []
    for i, col in enumerate(group_by(H, key=lambda v: v.rank, sort=True)):
        col_sizes.append(len(col))
        for v in col:
            v.rank = i

    for v in H:
        if H.in_degree(v) != H.out_degree(v):
            continue

        start = (
            v.rank - min([v.rank - u.rank for u in H.predecessors(v)], default=-1) + 1
        )
        stop = v.rank + min([w.rank - v.rank for w in H.successors(v)], default=-1)
        new_rank = max(range(start, stop), key=lambda i: col_sizes[i], default=v.rank)

        if col_sizes[new_rank] < col_sizes[v.rank]:
            col_sizes[v.rank] -= 1
            col_sizes[new_rank] += 1
            v.rank = new_rank


_BASE_ITER_LIMIT = 50


def network_simplex_ranks(H: LayoutGraph[Node]) -> None:
    """Rank the nodes so that the total (weighted) length of the links is
    minimal, by network simplex."""
    T, parents = feasible_tree(H)
    i = 0
    iter_limit = _BASE_ITER_LIMIT * sqrt(len(H))
    while (e := leave_edge(T)) and i < iter_limit:
        parents = exchange(H, T, parents, e, enter_edge(H, e))
        i += 1

    # The adjacency caches are keyed by the graphs of this run; drop them so
    # the graphs (and the nodes they reference) can be freed.
    get_adj_edges_H.cache_clear()
    get_adj_edges_T.cache_clear()


def compute_ranks(
    CG: ClusterGraph, solve: Callable[[LayoutGraph[Node]], None] = network_simplex_ranks
) -> None:
    """Assign every node its column (``rank``).

    *solve* ranks the nodes of the nesting graph — the layout graph plus
    border nodes and links that keep each frame's members between the
    frame's borders — so that every link spans at least one column.
    """
    for i, layer in enumerate(topological_generations(CG.T)):
        for c in layer:
            if isinstance(c, Cluster):
                c.nesting_level = i

    # Every link weighs the same.
    H = get_nesting_graph(CG)
    for link in H.all_links():
        link.weight = 1

    solve(H)

    root = next(c for c in CG.S if not CG.T.predecessors(c))
    H.remove_nodes((root.left, root.right))
    normalize_and_balance(CG, H)
