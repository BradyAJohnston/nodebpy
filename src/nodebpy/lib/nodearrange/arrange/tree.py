# SPDX-License-Identifier: GPL-2.0-or-later
"""Layout graph containers.

These replace the ``networkx`` graphs the arranger used to be built on. They
are shaped after the structs Blender's node editor already has, so that the
layout can later be ported to C++ against ``bNodeTree`` directly (the
layout's input, ``nodearrange.dna``, mirrors the same structs as plain data):

==================  ===================================================
here                Blender (``DNA_node_types.h`` / ``BKE_node_runtime.hh``)
==================  ===================================================
:class:`Tree`       ``bNodeTree``: owns the nodes and the links, and
                    answers topology queries (``all_nodes()``,
                    ``all_links()``, ``toposort_left_to_right()``) the way
                    the tree's topology cache does.
:class:`Link`       ``bNodeLink``: ``fromnode`` / ``fromsock`` / ``tonode``
                    / ``tosock``.
``graph.Node``      a ``bNode`` being laid out (``node`` is the
                    ``dna.bNode``), or a node the layout made up.
``graph.Socket``    a ``bNodeSocket`` (``dna``), or a made-up one.
``graph.Cluster``   a frame ``bNode`` and its ``direct_children_in_frame``.
==================  ===================================================

:class:`Tree` is a directed multigraph: two nodes can be joined by several
links (one per socket pair), told apart by :attr:`Link.key`. :class:`DiGraph`
is the plain directed graph used for auxiliary relations (the frame
hierarchy, ordering constraints, socket reachability).

Everything iterates in insertion order — nodes in the order they were added,
a node's neighbours in the order they were first linked — so a layout never
depends on hash values or memory addresses.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Iterator, KeysView
from typing import Any, cast

# -------------------------------------------------------------------


class Link[N: Hashable]:
    """A link between two nodes of a :class:`Tree` (``bNodeLink``).

    ``fromsock`` / ``tosock`` are None for links that only constrain the
    layout (frame borders, ranking constraints). ``key`` tells parallel
    links between the same two nodes apart, and is kept when a tree is
    copied, so ``(fromnode, tonode, key)`` names the same link in a tree and
    in its copies. ``weight`` and ``cut_value`` are scratch values for the
    ranking and feedback-arc-set passes.
    """

    __slots__ = (
        "cut_value",
        "fromnode",
        "fromsock",
        "key",
        "tonode",
        "tosock",
        "weight",
    )

    fromnode: N
    tonode: N
    fromsock: Any
    tosock: Any
    key: int
    weight: Any
    cut_value: Any

    def __init__(
        self,
        fromnode: N,
        tonode: N,
        fromsock: Any = None,
        tosock: Any = None,
        key: int = 0,
        weight: Any = None,
    ) -> None:
        self.fromnode = fromnode
        self.tonode = tonode
        self.fromsock = fromsock
        self.tosock = tosock
        self.key = key
        self.weight = weight
        self.cut_value = None

    @property
    def ident(self) -> tuple[N, N, int]:
        """``(fromnode, tonode, key)``: names this link across tree copies."""
        return (self.fromnode, self.tonode, self.key)

    def __repr__(self) -> str:
        return f"Link({self.fromnode!r} -> {self.tonode!r}, key={self.key})"


def _contains(mapping: dict, item: object) -> bool:
    try:
        return item in mapping
    except TypeError:
        return False


class Tree[N: Hashable]:
    """Nodes and the links between them (``bNodeTree``)."""

    __slots__ = ("_nodes", "_pred", "_succ", "columns")

    _nodes: dict[N, None]
    # node -> neighbour -> key -> link; the innermost dict is shared between
    # `_succ[u][v]` and `_pred[v][u]`.
    _succ: dict[N, dict[N, dict[int, Link[N]]]]
    _pred: dict[N, dict[N, dict[int, Link[N]]]]
    # The nodes grouped by rank, each column ordered top to bottom. Shared
    # with copies and reversed views.
    columns: list[list[N]]

    def __init__(self) -> None:
        self._nodes = {}
        self._succ = {}
        self._pred = {}

    # -- nodes ------------------------------------------------------

    def __iter__(self) -> Iterator[N]:
        return iter(self._nodes)

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node: object) -> bool:
        return _contains(self._nodes, node)

    def all_nodes(self) -> KeysView[N]:
        return self._nodes.keys()

    def add_node(self, node: N) -> None:
        if node not in self._nodes:
            self._nodes[node] = None
            self._succ[node] = {}
            self._pred[node] = {}

    def add_nodes(self, nodes: Iterable[N]) -> None:
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node: N) -> None:
        """Remove *node* and every link attached to it."""
        succs = self._succ[node]
        del self._nodes[node]
        for v in succs:
            del self._pred[v][node]
        del self._succ[node]
        for u in self._pred[node]:
            del self._succ[u][node]
        del self._pred[node]

    def remove_nodes(self, nodes: Iterable[N]) -> None:
        """Remove *nodes*, skipping any that are not in the tree."""
        for node in nodes:
            if node in self._nodes:
                self.remove_node(node)

    # -- links ------------------------------------------------------

    def add_link(
        self,
        fromnode: N,
        tonode: N,
        fromsock: Any = None,
        tosock: Any = None,
        *,
        key: int | None = None,
        weight: Any = None,
    ) -> Link[N]:
        """Link *fromnode* to *tonode*, adding either node if needed.

        Without *key* the link is a new parallel link. With the *key* of an
        existing link between the two nodes, that link is updated instead.
        """
        self.add_node(fromnode)
        self.add_node(tonode)
        keydict = self._succ[fromnode].get(tonode)
        if keydict is None:
            keydict = {}
            self._succ[fromnode][tonode] = keydict
            self._pred[tonode][fromnode] = keydict
        if key is None:
            key = len(keydict)
            while key in keydict:
                key += 1
        link = keydict.get(key)
        if link is None:
            link = Link(fromnode, tonode, fromsock, tosock, key, weight)
            keydict[key] = link
        else:
            if fromsock is not None:
                link.fromsock = fromsock
            if tosock is not None:
                link.tosock = tosock
            if weight is not None:
                link.weight = weight
        return link

    def remove_link(self, link: Link[N]) -> None:
        self.remove_link_between(link.fromnode, link.tonode, link.key)

    def remove_link_between(self, u: N, v: N, key: int | None = None) -> None:
        """Remove the link from *u* to *v* with *key*, or the most recently
        added one when *key* is None. Raises KeyError if there is none."""
        keydict = self._succ[u][v]
        if key is None:
            keydict.popitem()
        else:
            del keydict[key]
        if not keydict:
            del self._succ[u][v]
            del self._pred[v][u]

    def discard_link_between(self, u: N, v: N, key: int | None = None) -> None:
        """Like :meth:`remove_link_between`, ignoring a missing link."""
        try:
            self.remove_link_between(u, v, key)
        except KeyError:
            pass

    def link(self, u: N, v: N, key: int) -> Link[N]:
        return self._succ[u][v][key]

    def has_link(self, u: N, v: N, key: int | None = None) -> bool:
        keydict = self._succ.get(u, {}).get(v)
        if keydict is None:
            return False
        return True if key is None else key in keydict

    def links_between(self, u: N, v: N) -> list[Link[N]]:
        """The parallel links from *u* to *v*. Raises KeyError if *v* is not
        a successor of *u*."""
        return list(self._succ[u][v].values())

    def all_links(self) -> Iterator[Link[N]]:
        for nbrs in self._succ.values():
            for keydict in nbrs.values():
                yield from keydict.values()

    def _bunch(self, nodes: N | Iterable[N]) -> list[N]:
        if _contains(self._nodes, nodes):
            return [cast(N, nodes)]
        return list(
            dict.fromkeys(n for n in cast(Iterable[N], nodes) if n in self._nodes)
        )

    def out_links(self, nodes: N | Iterable[N]) -> Iterator[Link[N]]:
        """Links leaving *nodes* (one node or several)."""
        for n in self._bunch(nodes):
            for keydict in self._succ[n].values():
                yield from keydict.values()

    def in_links(self, nodes: N | Iterable[N]) -> Iterator[Link[N]]:
        """Links entering *nodes* (one node or several)."""
        for n in self._bunch(nodes):
            for keydict in self._pred[n].values():
                yield from keydict.values()

    def entering(self, nodes: N | Iterable[N]) -> Iterator[tuple[N, N, Link[N]]]:
        """``(source, target, link)`` for the links entering *nodes*, as this
        tree sees them: on a :meth:`reversed` view the source is the link's
        ``tonode``."""
        for n in self._bunch(nodes):
            for nbr, keydict in self._pred[n].items():
                for link in keydict.values():
                    yield (nbr, n, link)

    # -- topology ---------------------------------------------------

    def successors(self, node: N) -> KeysView[N]:
        return self._succ[node].keys()

    def predecessors(self, node: N) -> KeysView[N]:
        return self._pred[node].keys()

    def out_degree(self, node: N) -> int:
        return sum(len(keydict) for keydict in self._succ[node].values())

    def in_degree(self, node: N) -> int:
        return sum(len(keydict) for keydict in self._pred[node].values())

    def degree(self, node: N) -> int:
        return self.out_degree(node) + self.in_degree(node)

    def toposort_left_to_right(self) -> list[N]:
        return topological_sort(self)

    # -- derived trees ----------------------------------------------

    def copy(self) -> Tree[N]:
        """A tree with the same nodes and a copy of every link."""
        tree = type(self)()
        if hasattr(self, "columns"):
            tree.columns = self.columns
        tree.add_nodes(self._nodes)
        for link in self.all_links():
            copied = tree.add_link(
                link.fromnode,
                link.tonode,
                link.fromsock,
                link.tosock,
                key=link.key,
                weight=link.weight,
            )
            copied.cut_value = link.cut_value
        return tree

    def reversed(self) -> Tree[N]:
        """A view of this tree with successors and predecessors swapped.

        The nodes and links are shared, so a link's ``fromnode`` is still
        the node it leaves in the original tree.
        """
        tree = type(self)()
        if hasattr(self, "columns"):
            tree.columns = self.columns
        tree._nodes = self._nodes
        tree._succ = self._pred
        tree._pred = self._succ
        return tree

    def subgraph(self, nodes: Iterable[N]) -> Tree[N]:
        """A copy restricted to *nodes* and the links among them."""
        keep = {n for n in nodes if n in self._nodes}
        tree = type(self)()
        tree.add_nodes(_filtered(self._nodes, keep))
        for u in _filtered(self._succ, keep):
            nbrs = self._succ[u]
            for v in _filtered(nbrs, keep):
                for link in nbrs[v].values():
                    tree.add_link(
                        u,
                        v,
                        link.fromsock,
                        link.tosock,
                        key=link.key,
                        weight=link.weight,
                    )
        return tree

    def _multiplicity(self, u: N, v: N) -> int:
        return len(self._succ[u][v])


def _filtered[K](mapping: dict[K, Any], keep: set[K]) -> list[K]:
    # Walk whichever of the two is clearly smaller.
    if 2 * len(keep) < len(mapping):
        return [n for n in keep if n in mapping]
    return [n for n in mapping if n in keep]


# -------------------------------------------------------------------


class DiGraph[N: Hashable]:
    """A directed graph without parallel edges, each with an optional
    weight. Used for relations between layout items: the frame hierarchy,
    ordering constraints, socket reachability."""

    __slots__ = ("_nodes", "_pred", "_succ")

    _nodes: dict[N, None]
    # node -> neighbour -> weight, mirrored in both directions.
    _succ: dict[N, dict[N, Any]]
    _pred: dict[N, dict[N, Any]]

    def __init__(self, edges: Iterable[tuple[N, N]] = ()) -> None:
        self._nodes = {}
        self._succ = {}
        self._pred = {}
        self.add_edges(edges)

    def __iter__(self) -> Iterator[N]:
        return iter(self._nodes)

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node: object) -> bool:
        return _contains(self._nodes, node)

    def all_nodes(self) -> KeysView[N]:
        return self._nodes.keys()

    def add_node(self, node: N) -> None:
        if node not in self._nodes:
            self._nodes[node] = None
            self._succ[node] = {}
            self._pred[node] = {}

    def add_nodes(self, nodes: Iterable[N]) -> None:
        for node in nodes:
            self.add_node(node)

    def remove_node(self, node: N) -> None:
        succs = self._succ[node]
        del self._nodes[node]
        for v in succs:
            del self._pred[v][node]
        del self._succ[node]
        for u in self._pred[node]:
            del self._succ[u][node]
        del self._pred[node]

    def remove_nodes(self, nodes: Iterable[N]) -> None:
        for node in nodes:
            if node in self._nodes:
                self.remove_node(node)

    def add_edge(self, u: N, v: N, weight: Any = None) -> None:
        self.add_node(u)
        self.add_node(v)
        if weight is not None or v not in self._succ[u]:
            self._succ[u][v] = weight
            self._pred[v][u] = weight

    def add_edges(self, edges: Iterable[tuple[N, N]]) -> None:
        for u, v in edges:
            self.add_edge(u, v)

    def remove_edge(self, u: N, v: N) -> None:
        del self._succ[u][v]
        del self._pred[v][u]

    def remove_edges(self, edges: Iterable[tuple[N, N]]) -> None:
        """Remove *edges*, skipping any that are not in the graph."""
        for u, v in edges:
            if u in self._succ and v in self._succ[u]:
                self.remove_edge(u, v)

    def has_edge(self, u: N, v: N) -> bool:
        return u in self._succ and v in self._succ[u]

    def weight(self, u: N, v: N) -> Any:
        return self._succ[u][v]

    def set_weight(self, u: N, v: N, weight: Any) -> None:
        self._succ[u][v] = weight
        self._pred[v][u] = weight

    def edges(self) -> Iterator[tuple[N, N]]:
        for u, nbrs in self._succ.items():
            for v in nbrs:
                yield (u, v)

    def out_edges(self, node: N) -> Iterator[tuple[N, N]]:
        for v in self._succ[node]:
            yield (node, v)

    def in_edges(self, node: N) -> Iterator[tuple[N, N]]:
        for u in self._pred[node]:
            yield (u, node)

    def successors(self, node: N) -> KeysView[N]:
        return self._succ[node].keys()

    def predecessors(self, node: N) -> KeysView[N]:
        return self._pred[node].keys()

    def out_degree(self, node: N) -> int:
        return len(self._succ[node])

    def in_degree(self, node: N) -> int:
        return len(self._pred[node])

    def degree(self, node: N) -> int:
        return len(self._succ[node]) + len(self._pred[node])

    def copy(self) -> DiGraph[N]:
        graph = type(self)()
        graph.add_nodes(self._nodes)
        for u, nbrs in self._succ.items():
            for v, weight in nbrs.items():
                graph.add_edge(u, v, weight)
        return graph

    def reversed(self) -> DiGraph[N]:
        """A view of this graph with every edge reversed."""
        graph = type(self)()
        graph._nodes = self._nodes
        graph._succ = self._pred
        graph._pred = self._succ
        return graph

    def subgraph(self, nodes: Iterable[N]) -> DiGraph[N]:
        """A copy restricted to *nodes* and the edges among them."""
        keep = {n for n in nodes if n in self._nodes}
        graph = type(self)()
        graph.add_nodes(_filtered(self._nodes, keep))
        for u in _filtered(self._succ, keep):
            for v, weight in self._succ[u].items():
                if v in keep:
                    graph.add_edge(u, v, weight)
        return graph

    def _multiplicity(self, u: N, v: N) -> int:
        return 1


type AnyGraph[N: Hashable] = Tree[N] | DiGraph[N]


def simple_digraph[N: Hashable](tree: Tree[N]) -> DiGraph[N]:
    """*tree* with parallel links merged into single edges."""
    graph: DiGraph[N] = DiGraph()
    graph.add_nodes(tree)
    for u, nbrs in tree._succ.items():
        for v in nbrs:
            graph.add_edge(u, v)
    return graph


# -------------------------------------------------------------------
# Traversals and orderings. Each walks neighbours in insertion order.


class CycleError(ValueError):
    """The graph has a cycle where an acyclic one is required."""


def bfs_edges[N: Hashable](
    G: AnyGraph[N], source: N, *, reverse: bool = False
) -> Iterator[tuple[N, N]]:
    """Tree edges ``(parent, child)`` of a breadth-first search from
    *source*, following predecessors instead when *reverse* is set."""
    adjacency = G._pred if reverse else G._succ
    seen = {source}
    n = len(G)
    next_level = [(source, iter(adjacency[source]))]
    while next_level:
        this_level = next_level
        next_level = []
        for parent, children in this_level:
            for child in children:
                if child not in seen:
                    seen.add(child)
                    next_level.append((child, iter(adjacency[child])))
                    yield (parent, child)
            if len(seen) == n:
                return


def descendants[N: Hashable](G: AnyGraph[N], source: N) -> set[N]:
    """Every node reachable from *source*, excluding *source*."""
    return {child for _, child in bfs_edges(G, source)}


def ancestors[N: Hashable](G: AnyGraph[N], source: N) -> set[N]:
    """Every node *source* is reachable from, excluding *source*."""
    return {child for _, child in bfs_edges(G, source, reverse=True)}


def topological_generations[N: Hashable](G: AnyGraph[N]) -> Iterator[list[N]]:
    """Layers of a topological order: each node comes in the first layer
    after all of its predecessors. Raises :class:`CycleError` on a cycle."""
    indegree = {}
    zero_indegree = []
    for v in G:
        d = G.in_degree(v)
        if d > 0:
            indegree[v] = d
        else:
            zero_indegree.append(v)

    while zero_indegree:
        this_generation = zero_indegree
        zero_indegree = []
        for node in this_generation:
            for child in G._succ[node]:
                indegree[child] -= G._multiplicity(node, child)
                if indegree[child] == 0:
                    zero_indegree.append(child)
                    del indegree[child]
        yield this_generation

    if indegree:
        raise CycleError("graph contains a cycle")


def topological_sort[N: Hashable](G: AnyGraph[N]) -> list[N]:
    return [v for generation in topological_generations(G) for v in generation]


def is_acyclic[N: Hashable](G: AnyGraph[N]) -> bool:
    try:
        for _ in topological_generations(G):
            pass
    except CycleError:
        return False
    return True


def weakly_connected_components[N: Hashable](G: AnyGraph[N]) -> Iterator[set[N]]:
    """The node sets of the graph's connected pieces, ignoring direction."""
    seen: set[N] = set()
    n = len(G)
    for v in G:
        if v not in seen:
            component = _undirected_reach(G, n - len(seen), v)
            seen.update(component)
            yield component


def _undirected_reach[N: Hashable](G: AnyGraph[N], n: int, source: N) -> set[N]:
    seen = {source}
    next_level = [source]
    while next_level:
        this_level = next_level
        next_level = []
        for v in this_level:
            for w in G._succ[v]:
                if w not in seen:
                    seen.add(w)
                    next_level.append(w)
            for w in G._pred[v]:
                if w not in seen:
                    seen.add(w)
                    next_level.append(w)
            if len(seen) == n:
                return seen
    return seen


def strongly_connected_components[N: Hashable](G: AnyGraph[N]) -> Iterator[set[N]]:
    """The node sets within which every node reaches every other (Tarjan's
    algorithm with Nuutila's modifications, non-recursive)."""
    preorder: dict[N, int] = {}
    lowlink: dict[N, int] = {}
    found: set[N] = set()
    pending: list[N] = []
    i = 0
    neighbors = {v: iter(G._succ[v]) for v in G}
    for source in G:
        if source in found:
            continue
        stack = [source]
        while stack:
            v = stack[-1]
            if v not in preorder:
                i += 1
                preorder[v] = i
            done = True
            for w in neighbors[v]:
                if w not in preorder:
                    stack.append(w)
                    done = False
                    break
            if not done:
                continue
            lowlink[v] = preorder[v]
            for w in G._succ[v]:
                if w not in found:
                    if preorder[w] > preorder[v]:
                        lowlink[v] = min(lowlink[v], lowlink[w])
                    else:
                        lowlink[v] = min(lowlink[v], preorder[w])
            stack.pop()
            if lowlink[v] == preorder[v]:
                component = {v}
                while pending and preorder[pending[-1]] > preorder[v]:
                    component.add(pending.pop())
                found.update(component)
                yield component
            else:
                pending.append(v)


def find_cycle[N: Hashable](G: AnyGraph[N]) -> list[N] | None:
    """The nodes of one cycle of *G* in order, or None if it is acyclic."""
    for v, nbrs in G._succ.items():
        if v in nbrs:
            return [v]

    simple: DiGraph[N] = DiGraph(
        (u, v) for u, nbrs in G._succ.items() for v in nbrs if v != u
    )
    components = [c for c in strongly_connected_components(simple) if len(c) >= 2]
    if not components:
        return None

    component = components.pop()
    sub = simple.subgraph(component)
    start = next(iter(component))

    # First cycle of Johnson's search from `start` within its component.
    neighbors = {v: set(sub._succ[v]) for v in sub}
    path = [start]
    blocked = {start}
    stack = [iter(neighbors[start])]
    while stack:
        for w in stack[-1]:
            if w == start:
                return path
            if w not in blocked:
                path.append(w)
                stack.append(iter(neighbors[w]))
                blocked.add(w)
                break
        else:
            stack.pop()
            path.pop()

    # A component of two or more nodes always has a cycle through `start`.
    raise AssertionError("unreachable")  # pragma: no cover


def edge_dfs[N: Hashable](G: DiGraph[N], source: N) -> Iterator[tuple[N, N]]:
    """Every edge reachable from *source*, in depth-first order."""
    if source not in G:
        return

    visited_edges: set[tuple[N, N]] = set()
    visited_nodes: set[N] = set()
    edges: dict[N, Iterator[tuple[N, N]]] = {}
    stack = [source]
    while stack:
        current = stack[-1]
        if current not in visited_nodes:
            edges[current] = G.out_edges(current)
            visited_nodes.add(current)

        edge = next(edges[current], None)
        if edge is None:
            stack.pop()
        elif edge not in visited_edges:
            visited_edges.add(edge)
            stack.append(edge[1])
            yield edge


def dag_longest_path_length[N: Hashable](G: DiGraph[N]) -> Any:
    """The largest total edge weight along any path of the acyclic *G*
    (an edge without a weight counts 1)."""
    if not G:
        return 0

    dist: dict[N, Any] = {}
    for v in topological_sort(G):
        best = 0
        for u in G._pred[v]:
            weight = G._succ[u][v]
            best = max(best, dist[u] + (1 if weight is None else weight))
        dist[v] = best

    return max(dist.values())
