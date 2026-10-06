# SPDX-License-Identifier: GPL-2.0-or-later
"""What the layout works on: :class:`Node` (a node of the tree, or one the
layout makes up: a dummy node on a long link, a frame's border),
:class:`Socket`, :class:`Cluster` (a frame), and :class:`ClusterGraph`, the
graph of nodes together with the nesting of frames. See ``DESIGN.md`` for
the terms."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property
from itertools import chain, count, pairwise, product
from math import inf
from typing import TYPE_CHECKING, Literal, TypeGuard

from .common import REROUTE_DIM, frame_label_room, group_by
from .digraph import (
    DiGraph,
    LayoutGraph,
    Link,
    descendants,
)
from .dna import bNode, bNodeSocket
from .edits import RemoveNode
from .priority import is_flow_socket

if TYPE_CHECKING:
    from .config import LayoutState

# Nodes and clusters hash by creation order rather than id(), so iterating a
# set of them does not depend on memory addresses and a layout is the same
# on every run. sugiyama_layout() resets the counter.
_serials = count()


def reset_serials() -> None:
    global _serials
    _serials = count()


class Kind(Enum):
    """What a :class:`Node` is: a node of the tree, a stack of them, a dummy
    node, or a border node of a frame. ``HORIZONTAL_BORDER`` nodes stand
    left and right of a frame during ranking. ``VERTICAL_BORDER`` nodes
    stand above and below it in a column. ``CLUSTER`` is the kind of every
    :class:`Cluster`."""

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
    """Scratch values of the ordering: the positions of a node's sockets and
    the barycenter of a node or cluster."""

    socket_ranks: dict[Socket, float] = field(default_factory=dict)
    barycenter: float | None = None

    def reset(self) -> None:
        self.socket_ranks.clear()
        self.barycenter = None


class Node:
    """A node of the layout graph: a node of the tree (``node`` is set), or
    one the layout made up. ``rank`` is the index of its column, ``x`` its
    left edge and ``y`` its top edge. See ``placement.py`` for
    ``col_index``, ``root``, ``aligned``, ``sink``, ``shift`` and
    ``inner_shift``."""

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
    is_flow: bool

    col: list[Node]
    col_index: int
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
        self.is_flow = False

        self.col = None  # type: ignore
        self.col_index = None  # type: ignore
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


@dataclass(slots=True)
class Cluster:
    """A frame, or the whole tree for the outermost cluster.

    ``node`` is the frame, None for the outermost cluster. ``cluster`` is
    the cluster this one is in. ``left`` and ``right`` are the cluster's
    border nodes during ranking. :func:`~.long_links.insert_dummy_nodes`
    rebinds them to the cluster's leftmost and rightmost member nodes."""

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
        return frame_label_room(frame.label, frame.label_size) if frame else 0.0


def get_nesting_relations(
    v: Node | Cluster,
) -> Iterator[tuple[Cluster, Node | Cluster]]:
    """``(cluster, member)`` for *v* and for every cluster around it."""
    if c := v.cluster:
        yield (c, v)
        yield from get_nesting_relations(c)


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


def link_is_flow(link: Link[Node]) -> bool:
    """Whether a link of the layout graph carries the tree's main data
    (see :data:`.priority.FLOW_SOCKETS`). A piece of a long link carries
    what the whole does."""
    u = link.fromnode
    if u.type == Kind.DUMMY:
        return u.is_flow
    socket = link.fromsock.dna if link.fromsock is not None else None
    return socket is not None and is_flow_socket(socket)


def add_dummy_edge(G: LayoutGraph[Node], u: Node, v: Node) -> None:
    """Link *u* to *v* through made-up sockets."""
    G.add_link(u, v, Socket(u, 0, True), Socket(v, 0, False))


# https://api.semanticscholar.org/CorpusID:14932050
class ClusterGraph:
    """The layout graph with the nesting of its frames.

    ``G`` is the layout graph. ``T`` is the nesting: an edge from each
    cluster to every node and cluster directly in it. ``S`` lists the
    clusters of ``T``, the outermost included."""

    G: LayoutGraph[Node]
    T: DiGraph[Node | Cluster]
    S: list[Cluster]
    state: LayoutState
    __slots__ = tuple(__annotations__)

    def __init__(self, G: LayoutGraph[Node], state: LayoutState) -> None:
        self.G = G
        self.state = state
        self.T = DiGraph(chain(*map(get_nesting_relations, G)))
        self.S = [v for v in self.T if isinstance(v, Cluster)]

    def remove_nodes_from(self, nodes: Iterable[Node]) -> None:
        """Remove *nodes* from the graph, the nesting and their columns. For
        a node of the tree, also forget its links and record a
        ``RemoveNode`` edit."""
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

    def add_vertical_border_nodes(self) -> None:
        """Add a border node above and below each frame's nodes in every
        column the frame has nodes in. The upper one is as tall as the
        frame's label. A frame's upper border nodes are chained across the
        columns, and so are its lower ones."""
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


@dataclass(frozen=True)
class Socket:
    """A socket of a :class:`Node`, by index. ``prescribed_offset_y``, when
    set, is its offset from the node's top. Otherwise the offset comes from
    the tree's socket, and is zero for reroutes and made-up nodes."""

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

    Every ordering of a column must end with this true, because the border
    nodes, the placement and the frame outlines rely on it. A step that
    sorts a column by a key of its own can call this afterwards."""
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


def socket_graph(G: LayoutGraph[Node]) -> DiGraph[Socket]:
    """Which socket feeds which: every link, plus each node's inputs to its
    outputs."""
    H: DiGraph[Socket] = DiGraph()
    H.add_edges([(link.fromsock, link.tosock) for link in G.all_links()])
    for sockets in group_by(H, key=lambda s: s.owner):
        outputs = [s for s in sockets if s.is_output]
        inputs = [s for s in sockets if not s.is_output]
        H.add_edges(product(inputs, outputs))

    return H
