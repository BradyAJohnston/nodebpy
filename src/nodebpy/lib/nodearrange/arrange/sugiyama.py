# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections.abc import Sequence
from itertools import chain
from statistics import fmean

from ..config import LayoutState, Settings
from ..dna import bNodeTree
from .balancing import balance_column_heights
from .common import Vec2, f32, group_by
from .edits import LayoutResult
from .graph import (
    Cluster,
    ClusterGraph,
    Kind,
    Node,
    Socket,
    get_reroute_paths,
    is_real,
    node_name,
    reset_serials,
)
from .pipeline import Layout, Observer, Pipeline, Step, strategy
from .realize import realize_layout, remove_reroutes
from .stacking import contracted_node_stacks, expand_node_stack
from .tree import Tree, bfs_edges
from .x_coords import assign_x_coords

# Importing these registers their strategies.
from . import ordering, ranking, y_coords  # noqa: F401  isort: skip

# -------------------------------------------------------------------


def precompute_links(state: LayoutState) -> None:
    # Precompute links to ignore invalid links, and avoid `O(len(tree.links))` time

    # Headless divergence: links into a collapsed panel's sockets report
    # ``is_hidden`` (Blender draws them to the panel header); they still
    # carry data, so they still order the nodes.
    for link in state.tree.links:
        if link.is_valid:
            state.linked_sockets[link.tosock][link.fromsock] = None
            state.linked_sockets[link.fromsock][link.tosock] = None


def get_tree(state: LayoutState) -> Tree[Node]:
    parents = {
        n.parent: Cluster(n.parent, None)  # type: ignore
        for n in state.tree.nodes
    }
    for c in parents.values():
        if c.node:
            c.cluster = parents[c.node.parent]

    G: Tree[Node] = Tree()
    G.add_nodes(
        [Node(n, parents[n.parent]) for n in state.tree.nodes if not n.is_frame()]
    )
    # Headless divergence: the addon arranges the user's selection and skips
    # links to unselected nodes; here the working set is the whole tree.
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


def save_multi_input_orders(G: Tree[Node], state: LayoutState) -> None:
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


def add_columns(G: Tree[Node]) -> None:
    columns = [list(c) for c in group_by(G, key=lambda v: v.rank, sort=True)]
    G.columns = columns

    def y_loc(v):
        return v.node.location[1] if is_real(v) and G.degree(v) == 0 else 0

    for col in columns:
        col.sort(key=node_name)
        col.sort(key=y_loc, reverse=True)
        for v in col:
            v.col = col


def dissolve_dummy_nodes(CG: ClusterGraph) -> None:
    paths = get_reroute_paths(
        CG,
        lambda v: v.is_reroute and not is_real(v),
        preserve_reroute_clusters=False,
    )
    G = CG.G
    for path in paths:
        if G.predecessors(path[0]):
            first = next(G.in_links(path[0]))
            u, o = first.fromnode, first.fromsock
            succ_inputs = [link.tosock for link in G.out_links(path[-1])]
            for i in succ_inputs:
                G.add_link(u, i.owner, o, i)

        CG.remove_nodes_from(path)


# -------------------------------------------------------------------


def get_foreign_sockets_of(path: Sequence[Node], G: Tree[Node]) -> list[Socket]:
    inputs = [link.fromsock for link in G.in_links(path[0])]
    outputs = [link.tosock for link in G.out_links(path[-1])]
    return inputs + outputs


def align_reroutes_with_sockets(CG: ClusterGraph) -> None:
    reroute_paths: dict[tuple[Node, ...], list[Socket]] = {}
    for p in get_reroute_paths(
        CG, preserve_reroute_clusters=False, aligned=True, linear=False
    ):
        reroute_paths[tuple(p)] = get_foreign_sockets_of(p, CG.G)

    reroute_path_of = {v: p for p in reroute_paths for v in p}

    while True:
        changed = False
        for p1, foreign_sockets in tuple(reroute_paths.items()):
            if p1 not in reroute_paths:
                continue

            y = p1[0].y
            foreign_sockets.sort(key=lambda s: abs(y - s.y))
            foreign_sockets.sort(key=lambda s: y == s.owner.y, reverse=True)
            foreign_sockets.sort(key=lambda s: s.owner.is_reroute, reverse=True)

            if not foreign_sockets or y == foreign_sockets[0].y:
                del reroute_paths[p1]
                continue

            movement = y - foreign_sockets[0].y
            y -= movement
            if movement < 0:
                above_y_vals = [
                    (n := v.col[v.col.index(v) - 1]).y - n.height
                    for v in p1
                    if v != v.col[0]
                ]
                if above_y_vals and y > min(above_y_vals) - CG.state.margin.y:
                    continue
            else:
                below_y_vals = [
                    v.col[v.col.index(v) + 1].y for v in p1 if v != v.col[-1]
                ]
                if (
                    below_y_vals
                    and max(below_y_vals) + CG.state.margin.y > y - p1[0].height
                ):
                    continue

            for v in p1:
                v.y -= movement

            w = foreign_sockets[0].owner
            if w.is_reroute:
                p2 = reroute_path_of[w]
                p3 = p1 + p2 if w.rank > p1[-1].rank else p2 + p1
                reroute_paths[p3] = get_foreign_sockets_of(p3, CG.G)
                del reroute_paths[p1]
                reroute_paths.pop(p2, None)
                for v in p3:
                    reroute_path_of[v] = p3

            changed = True

        if not changed:
            if reroute_paths:
                for foreign_sockets in reroute_paths.values():
                    del foreign_sockets[0]
            else:
                break


# -------------------------------------------------------------------


def _contract_stacks(layout: Layout) -> None:
    layout.node_stacks = contracted_node_stacks(layout.CG)


def _expand_stacks(layout: Layout) -> None:
    for node_stack in layout.node_stacks:
        expand_node_stack(layout.CG, node_stack)


def _add_frame_borders(layout: Layout) -> None:
    CG = layout.CG
    CG.add_vertical_border_nodes()
    CG.remove_nodes_from([v for v in CG.G if v.is_fill_dummy])


def _remove_frame_borders(layout: Layout) -> None:
    CG = layout.CG
    CG.remove_nodes_from([v for v in CG.G if v.type == Kind.VERTICAL_BORDER])


def default_pipeline(settings: Settings | None = None) -> Pipeline:
    """The standard layout: the steps in order, with the strategy *settings*
    selects for each phase."""
    settings = settings or Settings()

    def reroutes(s: Settings) -> bool:
        return s.add_reroutes

    def no_reroutes(s: Settings) -> bool:
        return not s.add_reroutes

    def stacks(s: Settings) -> bool:
        return s.stack_collapsed

    return Pipeline(
        [
            # Prepare the graph.
            Step(
                "save_multi_input_orders",
                lambda L: save_multi_input_orders(L.G, L.state),
            ),
            Step("remove_reroutes", lambda L: remove_reroutes(L.CG), reroutes),
            Step("contract_stacks", _contract_stacks, stacks),
            # Columns.
            Step("rank", strategy("rank", settings.ranking), phase="rank"),
            Step(
                "balance_heights",
                lambda L: balance_column_heights(L.G, L.CG.S, L.state),
                lambda s: s.balance_heights,
            ),
            Step("merge_edges", lambda L: L.CG.merge_edges()),
            Step("insert_dummy_nodes", lambda L: L.CG.insert_dummy_nodes()),
            Step("add_columns", lambda L: add_columns(L.G)),
            # Order within the columns.
            Step("order", strategy("order", settings.ordering), phase="order"),
            # Positions along the columns.
            Step("add_frame_borders", _add_frame_borders),
            Step("place", strategy("place", settings.placement), phase="place"),
            Step(
                "dissolve_dummy_nodes",
                lambda L: dissolve_dummy_nodes(L.CG),
                no_reroutes,
            ),
            Step("align_reroutes", lambda L: align_reroutes_with_sockets(L.CG)),
            Step("remove_frame_borders", _remove_frame_borders),
            # Positions across the columns, and the links between them.
            Step("space_columns", lambda L: assign_x_coords(L.G, L.T, L.state)),
            Step("route", strategy("route", settings.routing), reroutes, phase="route"),
            # Write the result out.
            Step("expand_stacks", _expand_stacks, stacks),
            Step("realize", lambda L: realize_layout(L.CG, L.old_center)),
        ]
    )


def sugiyama_layout(
    tree: bNodeTree,
    settings: Settings | None = None,
    margin: tuple[float, float] | None = None,
    *,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
) -> LayoutResult:
    """Lay out *tree* and return the edits that realise the layout.

    *tree* is only read. *margin* is the horizontal and vertical room to
    leave between nodes. *pipeline* replaces the steps of
    :func:`default_pipeline`; *observer* is called after each step (see
    :class:`~.pipeline.Pipeline`).
    """
    reset_serials()
    state = LayoutState(tree=tree, settings=settings or Settings())
    if margin is not None:
        state.margin = Vec2(f32(margin[0]), f32(margin[1]))
    locs = [n.location for n in tree.nodes if not n.is_frame()]

    if not locs:
        return LayoutResult()

    xs, ys = zip(*locs)
    old_center = Vec2(f32(fmean(xs)), f32(fmean(ys)))

    precompute_links(state)
    layout = Layout(ClusterGraph(get_tree(state), state), old_center)
    (pipeline or default_pipeline(state.settings)).run(layout, observer)
    return LayoutResult(state.edits)
