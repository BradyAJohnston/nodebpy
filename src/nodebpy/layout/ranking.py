"""The rank phase: give every node a column (:func:`compute_ranks`).

Network simplex (Gansner et al., below) over the *nesting graph*: the
layout graph plus two border nodes per frame, linked so that a frame's
nodes stay between them. See ``DESIGN.md``."""

# http://dx.doi.org/10.1109/32.221135

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from itertools import chain
from math import sqrt
from typing import TYPE_CHECKING

from .common import group_by
from .digraph import (
    DiGraph,
    LayoutGraph,
    Link,
    strongly_connected_components,
    topological_generations,
    weakly_connected_components,
)
from .model import Cluster, LinkIdent, Node, clusters_around

if TYPE_CHECKING:
    from .model import ClusterGraph


def get_nesting_graph(CG: ClusterGraph) -> LayoutGraph[Node]:
    """A copy of the layout graph with each cluster's left and right border
    nodes, linked so that everything in a cluster is ranked between them.
    With ``frames_as_stages`` the frame-sequence links are added too."""
    H = CG.G.copy()
    for u, v in CG.T.edges():
        if isinstance(u, Cluster):
            if not isinstance(v, Cluster):
                H.add_link(u.left, v)
                H.add_link(v, u.right)
            else:
                H.add_link(u.left, v.left)
                H.add_link(v.right, u.right)

    if CG.state.options.frames_as_stages:
        add_frame_sequence_links(CG, H)

    return H


def _top_level_unit(v: Node, root: Cluster) -> Node | Cluster:
    """The outermost frame (a child of *root*) containing *v*, or *v* itself
    when it sits directly in the root."""
    unit: Node | Cluster = v
    for c in clusters_around(v):
        if c is root:
            break
        unit = c
    return unit


def add_frame_sequence_links(CG: ClusterGraph, H: LayoutGraph[Node]) -> None:
    """Add links to *H* that put every node of a frame in a later column
    than every node of the frame that feeds it.

    A unit is an outermost frame or a node outside every frame. For each
    link between two units, a link is added from the source unit's right
    border (or the node itself) to the target unit's left border (or the
    node itself), and the constraint is recorded in
    ``state.frame_sequence``.

    Exempt: links between two nodes outside every frame, a source node
    outside every frame that has no predecessors, a target node outside
    every frame that has no successors, and units that feed each other in a
    cycle."""
    G = CG.G
    root = next(c for c in CG.S if not CG.T.predecessors(c))
    unit_of = {v: _top_level_unit(v, root) for v in G}

    unit_graph: DiGraph[Node | Cluster] = DiGraph()
    unit_graph.add_nodes(dict.fromkeys(unit_of.values()))
    for link in G.all_links():
        a, b = unit_of[link.fromnode], unit_of[link.tonode]
        if a is not b:
            unit_graph.add_edge(a, b)

    scc_of = {
        n: i
        for i, comp in enumerate(strongly_connected_components(unit_graph))
        for n in comp
    }
    for a, b in unit_graph.edges():
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
def get_adj_links_H(H: LayoutGraph[Node], v: Node) -> tuple[LinkIdent, ...]:
    """The links of *H* at *v*, incoming then outgoing, as ``Link.ident``.
    Cached. :func:`network_simplex_ranks` clears the cache."""
    return tuple(
        link.ident for links in (H.in_links(v), H.out_links(v)) for link in links
    )


def get_slack(e: LinkIdent) -> int:
    """How many columns longer the link *e* is than the minimum of one."""
    u, v, _ = e
    return v.rank - u.rank - 1


def tight_tree(H: LayoutGraph[Node], T: LayoutGraph[Node], root: Node) -> int:
    """Grow *T* from *root* over the links without slack, depth first, and
    return its size. An explicit stack is used because the tree can be as
    deep as the graph is long."""
    visited: set[LinkIdent] = set()
    T.add_node(root)
    stack = [(root, iter(get_adj_links_H(H, root)))]
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

            stack.append((other, iter(get_adj_links_H(H, other))))
            break
        else:
            stack.pop()

    return len(T)


@dataclass
class _TreeIndex:
    """What the exchanges read off the spanning tree: each node's parent
    and the link to it, the nodes by post-order number, and each link's
    place in the graph's own order."""

    parents: dict[Node, tuple[Node, Link[Node]]] = field(default_factory=dict)
    by_number: list[Node] = field(default_factory=list)
    link_order: dict[Link[Node], int] = field(default_factory=dict)

    def subtree(self, v: Node) -> list[Node]:
        """*v* and every node below it in the spanning tree."""
        return self.by_number[v.lowest_po_num : v.po_num + 1]


def set_post_order_numbers(
    top: Node, T: LayoutGraph[Node], index: _TreeIndex | None = None
) -> _TreeIndex:
    """Number the nodes of the spanning tree *T* in post-order, and give
    each the lowest number in its subtree. Returns the tree's index.

    Without *index* the whole tree is numbered, with *top* as its root.
    With the index of an earlier numbering only the subtree below *top*
    is numbered again, within the numbers it had: enough after an exchange
    of two links that are both in that subtree."""
    if index is None:
        index = _TreeIndex(by_number=[top] * len(T))
        num = 0
        above = None
    else:
        num = top.lowest_po_num
        above = index.parents[top][1] if top in index.parents else None
    parents = index.parents
    by_number = index.by_number

    def children(v: Node, above: Link[Node] | None) -> list[tuple[Node, Link[Node]]]:
        """The nodes below *v*, each with its link, *above* being the link
        to the node above *v*."""
        return [
            (link.fromnode if link.tonode is v else link.tonode, link)
            for link in chain(T.in_links(v), T.out_links(v))
            if link is not above
        ]

    # The numbers of a subtree are those handed out while it is open, so
    # the lowest is the count at entry.
    top.lowest_po_num = num
    stack = [(top, iter(children(top, above)))]
    while stack:
        w, below = stack[-1]
        for child, link in below:
            parents[child] = (w, link)
            child.lowest_po_num = num
            stack.append((child, iter(children(child, link))))
            break
        else:
            stack.pop()
            w.po_num = num
            by_number[num] = w
            num += 1

    return index


def _is_above(v: Node, w: Node) -> bool:
    """Whether *w* is *v* or below it in the numbered spanning tree."""
    return v.lowest_po_num <= w.po_num <= v.po_num


def tree_path(
    start: Node, end: Node, parents: dict[Node, tuple[Node, Link[Node]]]
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
    """Set the cut value of every link of the spanning tree *T*.

    Removing a tree link splits the tree in two. Its cut value is the
    weight of the links of *H* that run between the two halves the way it
    does, less the weight of those that run the other way. The values are
    worked out from the leaves inwards, each from the ones already known
    around one of its ends."""
    unknown_cut_values = {}
    leaves = []
    for v in H:
        adj_links = [k.ident for k in (*T.in_links(v), *T.out_links(v))]
        unknown_cut_values[v] = adj_links
        if len(adj_links) == 1:
            leaves.append(v)

    for v in leaves:
        while len(unknown_cut_values[v]) == 1:
            to_determine = unknown_cut_values[v][0]
            d = T.link(*to_determine)
            d.cut_value = H.link(*to_determine).weight
            u, w, _ = to_determine
            for e in get_adj_links_H(H, v):
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


def feasible_tree(H: LayoutGraph[Node]) -> tuple[LayoutGraph[Node], _TreeIndex]:
    """A first ranking and a spanning tree of links without slack to go
    with it. Starts from :func:`longest_path_ranks` and grows the tree. While
    the tree does not span *H*, its nodes are shifted to close the shortest
    gap to a node outside it. Returns the tree, numbered and with its cut
    values, and its index."""
    longest_path_ranks(H)

    T: LayoutGraph[Node] = LayoutGraph()
    v_root = next(iter(H))

    while tight_tree(H, T, v_root) < len(H):
        incident_links = [
            link.ident
            for link in H.all_links()
            if (link.fromnode in T) ^ (link.tonode in T)
        ]
        e = min(incident_links, key=get_slack)
        slack = -get_slack(e) if e[1] in T else get_slack(e)
        for v in T:
            v.rank += slack

    index = set_post_order_numbers(v_root, T)
    index.link_order = {link: i for i, link in enumerate(H.all_links())}
    compute_cut_values(H, T)

    return T, index


def leave_link(T: LayoutGraph[Node]) -> LinkIdent | None:
    """A tree link with a negative cut value, which an exchange can improve
    on. None when there is none."""
    return next((link.ident for link in T.all_links() if link.cut_value < 0), None)


def is_in_head(v: Node, e: LinkIdent) -> bool:
    """Whether *v* is in the half of the spanning tree that the tree link
    *e* points into, the two halves being what is left when *e* is removed.
    Read off the post-order numbers."""
    u, w, _ = e
    if _is_above(u, v) and _is_above(w, v):
        return u.po_num >= w.po_num
    return u.po_num < w.po_num


def enter_link(H: LayoutGraph[Node], e: LinkIdent, index: _TreeIndex) -> LinkIdent:
    """The link to put in the spanning tree in place of the tree link *e*:
    of the links of *H* that run from the half *e* points into to the other
    half, the one with the least slack, and of those the first in *H*.

    One half is the subtree below the lower end of *e*. Every link between
    the halves has an end in it, so only the links there are looked at."""
    u, w, _ = e
    lower = w if u.po_num > w.po_num else u
    low, high = lower.lowest_po_num, lower.po_num
    # With the lower end at the head, the links leave the subtree.
    # Otherwise they enter it.
    leaving = lower is w
    best: tuple[tuple[int, int], Link[Node]] | None = None
    for v in index.subtree(lower):
        for link in H.out_links(v) if leaving else H.in_links(v):
            other = link.tonode if leaving else link.fromnode
            if low <= other.po_num <= high:
                continue
            key = (get_slack(link.ident), index.link_order[link])
            if best is None or key < best[0]:
                best = (key, link)
    assert best is not None
    return best[1].ident


def exchange(
    T: LayoutGraph[Node],
    index: _TreeIndex,
    leave: LinkIdent,
    enter: LinkIdent,
) -> _TreeIndex:
    """Swap the tree link *leave* for the link *enter*, and bring the ranks,
    the cut values and the numbering up to date. Returns the index.

    Only the cut values around the cycle *enter* closes in the tree change,
    by the cut value of *leave*: up for the links that run around the cycle
    the way *enter* does, down for the others."""
    tail, head, key = enter
    cut_value = T.link(*leave).cut_value
    top, cycle = tree_path(head, tail, index.parents)
    for link, forwards in cycle:
        link.cut_value += -cut_value if forwards else cut_value

    T.remove_link_between(*leave)
    T.add_link(tail, head, key=key)
    T.link(tail, head, key).cut_value = -cut_value

    # The half of the tree *enter* points into closes up to the other by
    # the slack of *enter*. Only the subtree below the lower end of *leave*
    # is moved, the way that brings the halves together: the ranks matter
    # only relative to each other.
    slack = get_slack(enter)
    if not is_in_head(enter[1], leave):
        slack = -slack
    u, w, _ = leave
    if u.po_num > w.po_num:
        for v in index.subtree(w):
            v.rank -= slack
    else:
        for v in index.subtree(u):
            v.rank += slack

    # Both links are below the top of the cycle, so the tree is as it was
    # everywhere else.
    return set_post_order_numbers(top, T, index)


def tidy_ranks(CG: ClusterGraph, H: LayoutGraph[Node]) -> None:
    """Tidy the ranks after solving.

    A connected piece of the layout graph that lies wholly in one cluster
    is moved as a block, without gaps between its columns. In a frame it
    starts at the first column of the frame's own nodes. Outside frames it
    ends no later than the outermost cluster's left border. Then the ranks
    of *H* are renumbered from 0 without gaps. Last, a node with as many
    links in as out moves to the column with the fewest nodes among those
    its links allow."""
    for cc in weakly_connected_components(CG.G):
        c = cc[0].cluster
        assert c

        if any(v.cluster != c for v in cc):
            continue

        ranked = group_by(cc, key=lambda v: v.rank, sort=True)

        if c.node:
            start = min(
                v.rank for v in CG.T.successors(c) if not isinstance(v, Cluster)
            )
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

        # The columns its links allow: after its nearest predecessor, before
        # its nearest successor. A node without either stays put.
        before = min([v.rank - u.rank for u in H.predecessors(v)], default=-1)
        after = min([w.rank - v.rank for w in H.successors(v)], default=-1)
        allowed = range(v.rank - before + 1, v.rank + after)
        new_rank = min(allowed, key=lambda i: col_sizes[i], default=v.rank)

        if col_sizes[new_rank] < col_sizes[v.rank]:
            col_sizes[v.rank] -= 1
            col_sizes[new_rank] += 1
            v.rank = new_rank


_BASE_ITER_LIMIT = 50


def network_simplex_ranks(H: LayoutGraph[Node]) -> None:
    """Rank the nodes so that the total weighted length of the links is as
    small as possible, by network simplex.

    Stops after ``_BASE_ITER_LIMIT * sqrt(n)`` exchanges for *n* nodes, to
    bound the time taken. The ranking it then has is valid but may not be
    the shortest."""
    T, index = feasible_tree(H)
    i = 0
    iter_limit = _BASE_ITER_LIMIT * sqrt(len(H))
    while (e := leave_link(T)) and i < iter_limit:
        index = exchange(T, index, e, enter_link(H, e, index))
        i += 1

    # The adjacency cache is keyed by this run's graph. Clear it so the
    # graph and its nodes can be freed.
    get_adj_links_H.cache_clear()


def compute_ranks(
    CG: ClusterGraph, solve: Callable[[LayoutGraph[Node]], None] = network_simplex_ranks
) -> None:
    """Assign every node its column (``rank``): *solve* ranks the nesting
    graph (:func:`get_nesting_graph`), then the ranks are tidied
    (:func:`tidy_ranks`)."""
    # Every link weighs the same.
    H = get_nesting_graph(CG)
    for link in H.all_links():
        link.weight = 1

    solve(H)

    root = next(c for c in CG.S if not CG.T.predecessors(c))
    H.remove_nodes((root.left, root.right))
    tidy_ranks(CG, H)
