# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property
from itertools import chain, count, pairwise, product
from math import inf
from typing import TYPE_CHECKING, Literal, TypeGuard, cast

from ..dna import bNode, bNodeSocket
from .common import REROUTE_DIM, frame_padding, group_by
from .edits import RemoveLink, RemoveNode
from .tree import (
    DiGraph,
    Link,
    Tree,
    descendants,
    simple_digraph,
    topological_sort,
    weakly_connected_components,
)

if TYPE_CHECKING:
    from ..config import LayoutState

# -------------------------------------------------------------------

# Nodes and clusters hash by creation order rather than id(), so iterating a
# set of them doesn't depend on memory addresses and
# a layout is reproducible between runs. Reset per run by sugiyama_layout().
_serials = count()


def reset_serials() -> None:
    global _serials
    _serials = count()


class Kind(Enum):
    NODE = auto()
    STACK = auto()
    DUMMY = auto()
    CLUSTER = auto()
    HORIZONTAL_BORDER = auto()
    VERTICAL_BORDER = auto()


_NonCluster = Literal[
    Kind.NODE,
    Kind.STACK,
    Kind.DUMMY,
    Kind.HORIZONTAL_BORDER,
    Kind.VERTICAL_BORDER,
]


@dataclass(slots=True)
class CrossingReduction:
    socket_ranks: dict[Socket, float] = field(default_factory=dict)
    barycenter: float | None = None

    def reset(self) -> None:
        self.socket_ranks.clear()
        self.barycenter = None


class Node:
    node: bNode | None
    cluster: Cluster | None
    type: _NonCluster

    is_reroute: bool
    width: float
    height: float

    rank: int
    po_num: int
    lowest_po_num: int
    is_fill_dummy: bool
    priority: int

    col: list[Node]
    cr: CrossingReduction

    x: float
    y: float

    root: Node
    aligned: Node
    inner_shift: float
    sink: Node
    shift: float

    _serial: int

    __slots__ = tuple(__annotations__)

    def __init__(
        self,
        node: bNode | None = None,
        cluster: Cluster | None = None,
        type: _NonCluster = Kind.NODE,
        rank: int | None = None,
    ) -> None:

        self.node = node
        self.cluster = cluster
        self.type = type
        self.rank = rank  # type: ignore

        if type == Kind.DUMMY or (node is not None and node.is_reroute()):
            self.is_reroute = True
            self.width = REROUTE_DIM.x
            self.height = REROUTE_DIM.y
        elif node is not None:
            self.is_reroute = False
            self.width = node.width
            self.height = node.top - node.bottom
        else:
            self.is_reroute = type == Kind.VERTICAL_BORDER
            self.width = 0
            self.height = 0

        self.po_num = None  # type: ignore
        self.lowest_po_num = None  # type: ignore
        self.is_fill_dummy = False
        self.priority = 0

        self.col = None  # type: ignore
        self.cr = CrossingReduction()

        self.x = None  # type: ignore
        self.bk_reset()
        self._serial = next(_serials)

    def __hash__(self) -> int:
        return self._serial

    def __repr__(self) -> str:
        name = repr(self.node.name) if self.node is not None else f"#{self._serial}"
        return f"Node({name}, {self.type.name})"

    def bk_reset(self) -> None:
        self.root = self
        self.aligned = self
        self.inner_shift = 0

        self.sink = self
        self.shift = inf

        self.y = None  # type: ignore


class _RealNode(Node):
    node: bNode


def is_real(v: Node | Cluster) -> TypeGuard[_RealNode]:
    """Whether *v* stands for a node of the tree (a frame, for a cluster),
    rather than one the layout made up."""
    return v.node is not None


def node_name(v: Node) -> str:
    return getattr(v.node, "name", "")


Edge = tuple[Node, Node]
MultiEdge = tuple[Node, Node, int]


def opposite(v: Node, e: Edge | MultiEdge) -> Node:
    return e[0] if v != e[0] else e[1]


@dataclass(slots=True)
class Cluster:
    node: bNode | None
    cluster: Cluster
    nesting_level: int | None = None
    cr: CrossingReduction = field(default_factory=CrossingReduction)
    left: Node = field(init=False)
    right: Node = field(init=False)
    _serial: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._serial = next(_serials)
        self.left = Node(None, self, Kind.HORIZONTAL_BORDER)
        self.right = Node(None, self, Kind.HORIZONTAL_BORDER)

    def __hash__(self) -> int:
        return self._serial

    @property
    def type(self) -> Literal[Kind.CLUSTER]:
        return Kind.CLUSTER

    def label_height(self) -> float:
        frame = self.node
        if frame and frame.label:
            return -(frame_padding() / 2 - frame.label_size * 1.25)
        else:
            return 0


# -------------------------------------------------------------------


def get_nesting_relations(
    v: Node | Cluster,
) -> Iterator[tuple[Cluster, Node | Cluster]]:
    if c := v.cluster:
        yield (c, v)
        yield from get_nesting_relations(c)


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


def link_priority(link: Link[Node], priorities: dict[bNodeSocket, int]) -> int:
    """The priority of a link of the layout graph. A piece of a long link
    (one that passes through dummy nodes) has the priority of the whole."""
    through = [v.priority for v in (link.fromnode, link.tonode) if v.type == Kind.DUMMY]
    if through:
        return max(through)

    total = 0
    for socket in (link.fromsock, link.tosock):
        if socket is not None and socket.dna is not None:
            total += priorities.get(socket.dna, 0)
    return total


def add_dummy_edge(G: Tree[Node], u: Node, v: Node) -> None:
    G.add_link(u, v, Socket(u, 0, True), Socket(v, 0, False))


def add_dummy_nodes_to_edge(
    G: Tree[Node],
    link: Link[Node],
    dummy_nodes: Sequence[Node],
    state: LayoutState,
) -> None:
    if not dummy_nodes:
        return

    priority = link_priority(link, state.socket_priority)
    for w in dummy_nodes:
        w.priority = max(w.priority, priority)

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
    if state.settings.add_reroutes and link.tosock.dna.is_multi_input:
        state.edits.append(RemoveLink(link.fromsock.dna, link.tosock.dna))


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


def improve_cluster_assignment(
    e: Edge, dummy_nodes: Sequence[Node], state: LayoutState
) -> None:
    if state.settings.keep_reroutes_outside_frames:
        return

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


# https://api.semanticscholar.org/CorpusID:14932050
class ClusterGraph:
    G: Tree[Node]
    T: DiGraph[Node | Cluster]
    S: list[Cluster]
    state: LayoutState
    __slots__ = tuple(__annotations__)

    def __init__(self, G: Tree[Node], state: LayoutState) -> None:
        self.G = G
        self.state = state
        self.T = DiGraph(chain(*map(get_nesting_relations, G)))
        self.S = [v for v in self.T if isinstance(v, Cluster)]

    def remove_nodes_from(self, nodes: Iterable[Node]) -> None:
        state = self.state
        for v in nodes:
            self.G.remove_node(v)
            self.T.remove_node(v)
            if v.col:
                v.col.remove(v)

            if not is_real(v):
                continue

            sockets = [*v.node.inputs, *v.node.outputs]

            for socket in sockets:
                state.linked_sockets.pop(socket, None)

            for val in state.linked_sockets.values():
                for socket in sockets:
                    val.pop(socket, None)

            state.edits.append(RemoveNode(v.node))

    def merge_edges(self) -> None:
        G = self.G
        T = self.T
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

                add_dummy_nodes_to_edge(G, link, [w], self.state)
                G.remove_link_between(u, w)

            for pair in pairwise(dummy_nodes):
                add_dummy_edge(G, *pair)

            w = dummy_nodes[0]
            G.add_link(u, w, from_socket, Socket(w, 0, False))

            improve_cluster_assignment((u, v), dummy_nodes, self.state)
            for w in dummy_nodes:
                assert w.cluster is not None
                T.add_edge(w.cluster, w)

    def insert_dummy_nodes(self) -> None:
        G = self.G
        T = self.T

        # -------------------------------------------------------------------

        for c in self.S:
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

            improve_cluster_assignment((u, v), dummy_nodes, self.state)
            add_dummy_nodes_to_edge(G, link, dummy_nodes, self.state)

        for w in [w for w in G if w not in T]:
            assert w.cluster
            T.add_edge(w.cluster, w)

        # -------------------------------------------------------------------

        for c in self.S:
            if not c.node:
                continue

            ranks = sorted(
                {v.rank for v in descendants(T, c) if v.type != Kind.CLUSTER}
            )
            for i, j in pairwise(ranks):
                for k in range(i + 1, j):
                    v = Node(None, c, Kind.DUMMY, k)
                    v.is_fill_dummy = True
                    G.add_node(v)
                    T.add_edge(c, v)

    def add_vertical_border_nodes(self) -> None:
        T = self.T
        G = self.G
        columns = G.columns
        for c in self.S:
            if not c.node:
                continue

            members = [v for v in descendants(T, c) if v.type != Kind.CLUSTER]
            lower_border_nodes = []
            upper_border_nodes = []
            for subcol in group_by(
                members, key=lambda v: columns.index(v.col), sort=True
            ):
                col = subcol[0].col
                indices = [col.index(v) for v in subcol]

                lower_v = Node(None, c, Kind.VERTICAL_BORDER)
                col.insert(max(indices) + 1, lower_v)
                lower_v.col = col
                T.add_edge(c, lower_v)
                lower_border_nodes.append(lower_v)

                upper_v = Node(None, c, Kind.VERTICAL_BORDER)
                upper_v.height += c.label_height()
                col.insert(min(indices), upper_v)
                upper_v.col = col
                T.add_edge(c, upper_v)
                upper_border_nodes.append(upper_v)

            G.add_nodes(lower_border_nodes + upper_border_nodes)
            for p in *pairwise(lower_border_nodes), *pairwise(upper_border_nodes):
                add_dummy_edge(G, *p)


# -------------------------------------------------------------------


@dataclass(frozen=True)
class Socket:
    owner: Node
    idx: int
    is_output: bool
    prescribed_offset_y: float | None = field(default=None, hash=False, compare=False)

    @property
    def dna(self) -> bNodeSocket | None:
        """The socket of the tree this stands for, if any."""
        v = self.owner

        if not is_real(v):
            return None

        sockets = v.node.outputs if self.is_output else v.node.inputs
        if self.idx >= len(sockets):
            return None
        return sockets[self.idx]

    @property
    def x(self) -> float:
        v = self.owner
        return v.x + v.width if self.is_output else v.x

    @cached_property
    def _offset_y(self) -> float:
        if self.prescribed_offset_y is not None:
            return self.prescribed_offset_y

        v = self.owner

        if v.is_reroute or not is_real(v):
            return 0

        socket = self.dna
        assert socket is not None and socket.location is not None
        return socket.location[1] - v.node.top

    @property
    def y(self) -> float:
        return self.owner.y + self._offset_y


def keep_frames_together(col: list[Node]) -> None:
    """Reorder *col* in place, as little as possible, so that the nodes of
    each frame are next to each other: every frame's nodes gather where the
    first of them is, in the order they were in.

    An ordering of a column has to end with this true of it (the border
    nodes, the placement and the frame outlines all rely on it); a strategy
    that sorts a column by some key of its own can call this afterwards."""
    first: dict[Cluster, int] = {}
    chains: dict[Node, list[Cluster]] = {}
    for i, v in enumerate(col):
        chain = []
        c = v.cluster
        while c is not None:
            chain.append(c)
            first.setdefault(c, i)
            c = c.cluster
        chain.reverse()
        chains[v] = chain

    position = {v: i for i, v in enumerate(col)}
    col.sort(key=lambda v: (*[first[c] for c in chains[v]], position[v]))


def socket_graph(G: Tree[Node]) -> DiGraph[Socket]:
    """Which socket feeds which: every link, plus each node's inputs to its
    outputs."""
    H: DiGraph[Socket] = DiGraph()
    H.add_edges([(link.fromsock, link.tosock) for link in G.all_links()])
    for sockets in group_by(H, key=lambda s: s.owner):
        outputs = [s for s in sockets if s.is_output]
        inputs = [s for s in sockets if not s.is_output]
        H.add_edges(product(inputs, outputs))

    return H


# -------------------------------------------------------------------


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
