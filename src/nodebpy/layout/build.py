"""Build the layout graph from the tree: index the links, leave out those
that close a cycle, make a :class:`~.model.Node` for every node, and list
the columns once the nodes are ranked."""

from __future__ import annotations

from itertools import chain

from .common import group_by
from .config import LayoutState
from .digraph import LayoutGraph, bfs_edges
from .dna import bNode, bNodeLink, bNodeTree
from .model import (
    Cluster,
    Node,
    Socket,
    is_real,
    keep_frames_together,
    node_name,
)


def cycle_links(tree: bNodeTree) -> set[bNodeLink]:
    """The links of *tree* to leave out so that the rest has no cycle.

    First, among the links Blender calls valid: those that lead back to a
    node still being visited in a depth-first walk over the nodes and links
    in the tree's order. A tree from Blender has none, because Blender marks
    a link of every cycle invalid. Then each invalid link is kept unless it
    would close a cycle with the links kept so far."""
    out_links: dict[bNode, list[bNodeLink]] = {n: [] for n in tree.nodes}
    for link in tree.links:
        if link.is_valid and link.fromnode in out_links:
            out_links[link.fromnode].append(link)

    back = set()
    done: set[bNode] = set()
    for root in tree.nodes:
        if root in done:
            continue

        active = {root}
        stack = [(root, iter(out_links[root]))]
        while stack:
            node, links = stack[-1]
            for link in links:
                target = link.tonode
                if target in active:
                    back.add(link)
                elif target not in done and target in out_links:
                    active.add(target)
                    stack.append((target, iter(out_links[target])))
                    break
            else:
                stack.pop()
                active.discard(node)
                done.add(node)

    for links in out_links.values():
        links[:] = [link for link in links if link not in back]

    def reaches(start: bNode, goal: bNode) -> bool:
        seen = {start}
        pending = [start]
        while pending:
            node = pending.pop()
            if node is goal:
                return True
            for link in out_links.get(node, ()):
                if link.tonode not in seen:
                    seen.add(link.tonode)
                    pending.append(link.tonode)
        return False

    for link in tree.links:
        if link.is_valid or link.fromnode not in out_links:
            continue
        if reaches(link.tonode, link.fromnode):
            back.add(link)
        else:
            out_links[link.fromnode].append(link)

    return back


def precompute_links(state: LayoutState) -> None:
    """Index the links the layout uses: all of them except those that
    close a cycle. That includes the links Blender calls invalid because
    their sockets do not fit, which are still drawn. Raises ValueError for
    a linked socket without a location."""
    # Links into a collapsed panel's sockets are included. Blender calls
    # them hidden and draws them to the panel header, but they carry data.
    ignored = cycle_links(state.tree)
    for link in state.tree.links:
        if link in ignored:
            continue

        for socket in (link.fromsock, link.tosock):
            if socket.location is None and not socket.node.is_reroute():
                raise ValueError(
                    f"{socket.node!r}: linked "
                    f"{'output' if socket.is_output else 'input'} {socket.index} "
                    "has no location"
                )

        state.linked_sockets[link.tosock][link.fromsock] = None
        state.linked_sockets[link.fromsock][link.tosock] = None


def get_tree(state: LayoutState) -> LayoutGraph[Node]:
    """The layout graph of the tree in *state*: a :class:`~.model.Node` for
    every node that is neither a frame nor fixed, a
    :class:`~.model.Cluster` for every frame and one for the tree itself,
    and a link for every indexed link between two of those nodes."""
    parents = {
        n.parent: Cluster(n.parent, None)  # type: ignore
        for n in state.tree.nodes
    }
    for c in parents.values():
        if c.node:
            c.cluster = parents[c.node.parent]

    G: LayoutGraph[Node] = LayoutGraph()
    G.add_nodes(
        [
            Node(n, parents[n.parent])
            for n in state.tree.nodes
            if n not in state.fixed and not n.is_frame()
        ]
    )
    # Links to fixed nodes are left out.
    by_node = {v.node: v for v in G}
    for u in G:
        assert is_real(u)
        for i, from_output in enumerate(u.node.outputs):
            for to_input in state.linked_sockets[from_output]:
                v = by_node.get(to_input.node)
                if v is None:
                    continue

                G.add_link(u, v, Socket(u, i, True), Socket(v, to_input.index, False))

    return G


def save_multi_input_orders(G: LayoutGraph[Node], state: LayoutState) -> None:
    """Record in *state*, for every link into a multi-input socket, the
    output socket it comes from and its sort id. A link that arrives
    through reroutes is recorded under the output its chain starts at."""
    links = {(link.fromsock, link.tosock): link for link in state.tree.links}
    for edge in G.all_links():
        v, w = edge.fromnode, edge.tonode
        to_socket = edge.tosock

        if not to_socket.dna.is_multi_input:
            continue

        if v.is_reroute:
            for z, u in chain([(w, v)], bfs_edges(G, v, reverse=True)):
                if not u.is_reroute:
                    break
            base_from_socket = G.link(u, z, 0).fromsock
        else:
            base_from_socket = edge.fromsock

        link = links[(edge.fromsock.dna, to_socket.dna)]
        state.multi_input_sort_ids[to_socket].append(
            (base_from_socket, link.multi_input_sort_id)
        )


def add_columns(G: LayoutGraph[Node]) -> None:
    """Set ``G.columns``, the nodes of each rank, and every node's ``col``.
    Each column starts sorted by name, with unlinked nodes moved by their y
    in the tree, and with each frame's nodes together."""
    columns = [list(c) for c in group_by(G, key=lambda v: v.rank, sort=True)]
    G.columns = columns

    def y_loc(v):
        return v.node.location[1] if is_real(v) and G.degree(v) == 0 else 0

    for col in columns:
        col.sort(key=node_name)
        col.sort(key=y_loc, reverse=True)
        # The ordering may leave a column unchanged, because it stops as
        # soon as nothing crosses. So every frame's nodes start together.
        keep_frames_together(col)
        for v in col:
            v.col = col
