# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from itertools import chain, pairwise
from statistics import fmean

from ..config import LayoutState, Settings
from ..dna import bNode, bNodeLink, bNodeTree
from . import packing
from .balancing import balance_column_heights
from .common import Vec2, f32, group_by, segments_intersect
from .digraph import LayoutGraph, bfs_edges
from .edits import Edit, LayoutResult, MoveNode, RemoveLink
from .graph import (
    Cluster,
    ClusterGraph,
    Kind,
    Node,
    Socket,
    get_reroute_paths,
    is_real,
    keep_frames_together,
    node_name,
    reset_serials,
)
from .ordering import minimize_crossings
from .pipeline import (
    Fact,
    Layout,
    Observer,
    Phase,
    Pipeline,
    Step,
    StepFunction,
)
from .priority import socket_priorities, zone_priorities
from .ranking import compute_ranks
from .realize import realize_layout, remove_reroutes
from .stacking import contracted_node_stacks, expand_node_stack
from .x_coords import assign_x_coords, route_edges
from .y_coords import bk_assign_y_coords

# -------------------------------------------------------------------


def cycle_links(tree: bNodeTree) -> set[bNodeLink]:
    """The links of *tree* to leave out so that the rest has no cycle.

    Among the links Blender calls valid, those found leading back to a node
    still being visited in a depth-first walk over the nodes and links in
    the tree's order (none, in a tree that comes from Blender, which marks
    a link of every cycle invalid). Then each invalid link is taken in
    unless it would close a cycle with what has been taken in so far."""
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
    """Index the links the layout goes by: all of them, less those that
    close a cycle. (Upstream goes by Blender's ``is_valid``, which is also
    cleared for links that are merely between sockets that do not fit;
    those are still drawn, and still say where a node belongs.)"""
    # Headless divergence: links into a collapsed panel's sockets report
    # ``is_hidden`` (Blender draws them to the panel header); they still
    # carry data, so they still order the nodes.
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
            if n.select and not n.is_frame()
        ]
    )
    # As in the addon, the working set is the selected nodes, and links to
    # other nodes are left out. (Everything is selected unless the caller
    # asked for the selection to be arranged.)
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
    columns = [list(c) for c in group_by(G, key=lambda v: v.rank, sort=True)]
    G.columns = columns

    def y_loc(v):
        return v.node.location[1] if is_real(v) and G.degree(v) == 0 else 0

    for col in columns:
        col.sort(key=node_name)
        col.sort(key=y_loc, reverse=True)
        # nodebpy divergence: the ordering may leave a column as it finds it
        # (it stops as soon as nothing crosses), so start with every frame's
        # nodes together.
        keep_frames_together(col)
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


_CURVE_PIECES = 12
_CLEARANCE = 4.0


def _link_curve(
    start: tuple[float, float], end: tuple[float, float]
) -> list[tuple[float, float]]:
    """Points along a link as Blender draws it: a Bézier leaving and
    entering its sockets horizontally."""
    (x0, y0), (x3, y3) = start, end
    handle = max(0.4 * abs(x3 - x0), 12.0)
    x1, x2 = x0 + handle, x3 - handle
    points = []
    for k in range(_CURVE_PIECES + 1):
        t = k / _CURVE_PIECES
        s = 1.0 - t
        a, b, c, d = s**3, 3 * s**2 * t, 3 * s * t**2, t**3
        points.append((a * x0 + b * x1 + c * x2 + d * x3, (a + b) * y0 + (c + d) * y3))
    return points


def link_is_clear(start: Socket, end: Socket, obstacles: Sequence[Node]) -> bool:
    """Whether a link drawn straight from *start* to *end* passes clear of
    every node in *obstacles* (other than the two it joins)."""
    curve = _link_curve((start.x, start.y), (end.x, end.y))
    left = min(x for x, _ in curve)
    right = max(x for x, _ in curve)
    low = min(y for _, y in curve)
    high = max(y for _, y in curve)
    for v in obstacles:
        if v is start.owner or v is end.owner:
            continue
        xmin, xmax = v.x - _CLEARANCE, v.x + v.width + _CLEARANCE
        ymin, ymax = v.y - v.height - _CLEARANCE, v.y + _CLEARANCE
        if xmax < left or xmin > right or ymax < low or ymin > high:
            continue
        corners = ((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax))
        for p, q in pairwise(curve):
            if xmin < p[0] < xmax and ymin < p[1] < ymax:
                return False
            for i in range(4):
                if segments_intersect(p, q, corners[i], corners[i - 3]):
                    return False
    return True


def dissolve_clear_dummy_nodes(CG: ClusterGraph) -> None:
    """Take long links off their dummy nodes again wherever the link drawn
    straight would pass clear of every node, so that only the links that
    need routing around something end up with reroutes."""
    G = CG.G
    obstacles = [v for v in G if not v.is_reroute]
    paths = get_reroute_paths(
        CG,
        lambda v: v.is_reroute and not is_real(v),
        preserve_reroute_clusters=False,
    )
    for path in paths:
        # (A chain of dummy nodes always has the link it came from behind it.)
        output = next(G.in_links(path[0])).fromsock
        inputs = [link.tosock for link in G.out_links(path[-1])]
        if not all(link_is_clear(output, i, obstacles) for i in inputs):
            continue
        for i in inputs:
            G.add_link(output.owner, i.owner, output, i)
            # The tree's own link stands after all.
            edit = RemoveLink(output.dna, i.dna)
            if edit in CG.state.edits:
                CG.state.edits.remove(edit)
        CG.remove_nodes_from(path)


# -------------------------------------------------------------------


def get_foreign_sockets_of(path: Sequence[Node], G: LayoutGraph[Node]) -> list[Socket]:
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


def _prioritize_links(layout: Layout) -> None:
    tree = layout.state.tree
    priorities = socket_priorities(tree)
    priorities.update(zone_priorities(tree))
    layout.state.socket_priority = priorities


def constrain_layers(layout: Layout) -> None:
    """Move Group Output nodes to the last column and Group Input nodes to
    the first, as the settings ask. Only nodes outside frames with nothing
    after (before) them: moving those cannot break a constraint."""
    settings = layout.settings
    G = layout.G
    root = next(c for c in layout.CG.S if not layout.T.predecessors(c))
    ranks = [v.rank for v in G]
    first, last = min(ranks), max(ranks)
    for v in G:
        if not is_real(v) or v.cluster is not root:
            continue
        node = v.node
        if settings.pin_group_output and node.is_group_output() and not G.successors(v):
            v.rank = last
        if settings.pin_group_input and node.is_group_input() and not G.predecessors(v):
            v.rank = first


def default_pipeline() -> Pipeline:
    """The standard layout: the steps in order."""
    F = Fact

    def step(
        name: str,
        run: StepFunction,
        enabled: Callable[[Settings], bool] | None = None,
        *,
        phase: Phase | None = None,
        requires: Iterable[Fact] = (),
        provides: Iterable[Fact] = (),
        removes: Iterable[Fact] = (),
    ) -> Step:
        return Step(
            name,
            run,
            enabled or (lambda settings: True),
            phase,
            frozenset(requires),
            frozenset(provides),
            frozenset(removes),
        )

    def reroutes(s: Settings) -> bool:
        return s.reroutes != "none"

    def replacing_reroutes(s: Settings) -> bool:
        return s.reroutes == "all"

    def sparing_reroutes(s: Settings) -> bool:
        return s.reroutes == "blocked"

    def no_reroutes(s: Settings) -> bool:
        return s.reroutes == "none"

    def stacks(s: Settings) -> bool:
        return s.stack_collapsed

    return Pipeline(
        [
            # Prepare the graph.
            step(
                "prioritize_links",
                _prioritize_links,
                lambda s: s.straighten_trunk,
            ),
            step(
                "save_multi_input_orders",
                lambda L: save_multi_input_orders(L.G, L.state),
            ),
            step(
                "remove_reroutes", lambda L: remove_reroutes(L.CG), replacing_reroutes
            ),
            step("contract_stacks", _contract_stacks, stacks),
            # Columns.
            step(
                "rank",
                lambda L: compute_ranks(L.CG),
                phase="rank",
                provides=[F.RANKED],
            ),
            step(
                "balance_heights",
                lambda L: balance_column_heights(L.G, L.CG.S, L.state),
                lambda s: s.balance_heights,
                requires=[F.RANKED],
            ),
            # After the balancing, which would move a held node along with
            # whatever it moves left.
            step("constrain_layers", constrain_layers, requires=[F.RANKED]),
            step("merge_edges", lambda L: L.CG.merge_edges(), requires=[F.RANKED]),
            step(
                "insert_dummy_nodes",
                lambda L: L.CG.insert_dummy_nodes(),
                requires=[F.RANKED],
                provides=[F.PROPER],
            ),
            step(
                "add_columns",
                lambda L: add_columns(L.G),
                requires=[F.RANKED],
                provides=[F.COLUMNS],
            ),
            # Order within the columns.
            step(
                "order",
                lambda L: minimize_crossings(L.G, L.T, L.state),
                phase="order",
                requires=[F.PROPER, F.COLUMNS],
                provides=[F.ORDERED],
            ),
            # Positions along the columns.
            step(
                "add_frame_borders",
                _add_frame_borders,
                requires=[F.ORDERED],
                provides=[F.BORDERS],
            ),
            step(
                "place",
                lambda L: bk_assign_y_coords(L.G, L.T, L.state),
                phase="place",
                requires=[F.ORDERED, F.BORDERS],
                provides=[F.Y],
            ),
            step(
                "dissolve_dummy_nodes",
                lambda L: dissolve_dummy_nodes(L.CG),
                no_reroutes,
                requires=[F.Y],
                removes=[F.PROPER],
            ),
            step(
                "align_reroutes",
                lambda L: align_reroutes_with_sockets(L.CG),
                requires=[F.Y],
            ),
            step(
                "remove_frame_borders",
                _remove_frame_borders,
                requires=[F.BORDERS],
                removes=[F.BORDERS],
            ),
            # Positions across the columns, and the links between them.
            step(
                "space_columns",
                lambda L: assign_x_coords(L.G, L.T, L.state),
                requires=[F.COLUMNS, F.Y],
                provides=[F.X],
            ),
            step(
                "dissolve_clear_dummy_nodes",
                lambda L: dissolve_clear_dummy_nodes(L.CG),
                sparing_reroutes,
                requires=[F.PROPER, F.X],
                removes=[F.PROPER],
            ),
            step(
                "route",
                lambda L: route_edges(L.G, L.T, L.state),
                reroutes,
                phase="route",
                requires=[F.X],
                # Bend points are new nodes, outside the ranks and columns.
                removes=[F.RANKED, F.PROPER, F.COLUMNS],
            ),
            # Write the result out.
            step(
                "expand_stacks",
                _expand_stacks,
                stacks,
                requires=[F.X],
                # The nodes of a stack come back without a rank or column.
                removes=[F.RANKED, F.PROPER, F.COLUMNS],
            ),
            step(
                "realize",
                lambda L: realize_layout(L.CG, L.old_center),
                requires=[F.X],
                # Chains of dummy nodes become reroutes, fewer than columns.
                removes=[F.PROPER],
            ),
        ]
    )


def sugiyama_layout(
    tree: bNodeTree,
    settings: Settings | None = None,
    margin: tuple[float, float] | None = None,
    *,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
    verify: bool = False,
) -> LayoutResult:
    """Lay out *tree* and return the edits that realise the layout.

    *tree* is only read. *margin* is the horizontal and vertical room to
    leave between nodes. *pipeline* replaces the steps of
    :func:`default_pipeline`; *observer* is called after each step (see
    :class:`~.pipeline.Pipeline`). With *verify* the graph is checked after
    every step, and a step that breaks an invariant raises
    :class:`~.pipeline.InvariantError` (slower; for tests and for developing
    steps and strategies).
    """
    reset_serials()
    state = LayoutState(tree=tree, settings=settings or Settings())
    if margin is not None:
        state.margin = Vec2(f32(margin[0]), f32(margin[1]))
    locs = [n.location for n in tree.nodes if n.select and not n.is_frame()]

    if not locs:
        return LayoutResult()

    xs, ys = zip(*locs)
    old_center = Vec2(f32(fmean(xs)), f32(fmean(ys)))

    def lay_out(part: bNodeTree) -> list[Edit]:
        part_state = LayoutState(part, state.settings, state.margin)
        precompute_links(part_state)
        layout = Layout(ClusterGraph(get_tree(part_state), part_state), old_center)
        (pipeline or default_pipeline()).run(layout, observer, verify=verify)
        return part_state.edits

    def clear_of_the_rest(edits: list[Edit]) -> LayoutResult:
        """Move what was laid out off the nodes that were not (when only
        the selection is arranged), unless that would take it further than
        twice its own size (the longer side) from where it was."""
        obstacles = [
            n.draw_bounds
            for n in tree.nodes
            if not n.select and not n.is_frame() and not n.is_reroute()
        ]
        if not obstacles:
            return LayoutResult(edits)
        rects = packing.node_rects(edits)
        if not rects:
            return LayoutResult(edits)
        dx, dy = packing.clear_of(
            rects, obstacles, Vec2(state.margin.y, state.margin.y)
        )
        width = max(r[2] for r in rects) - min(r[0] for r in rects)
        height = max(r[3] for r in rects) - min(r[1] for r in rects)
        if max(abs(dx), abs(dy)) > 2 * max(width, height):
            return LayoutResult(edits)
        return LayoutResult(packing.moved(edits, (f32(dx), f32(dy))))

    parts = packing.components(tree) if state.settings.pack_components else []
    if len(parts) < 2:
        return clear_of_the_rest(lay_out(tree))

    # The part with the most nodes first; the others, largest first, are
    # packed beneath it.
    parts.sort(key=len, reverse=True)
    laid_out = [lay_out(packing.subtree(tree, part)) for part in parts]
    boxes = [packing.bounds(edits) for edits in laid_out]
    placed = [(edits, box) for edits, box in zip(laid_out, boxes) if box is not None]
    gap = Vec2(state.margin.x, f32(3 * state.margin.y))
    offsets = packing.pack([box for _, box in placed], gap)
    offset_of = {id(edits): offset for (edits, _), offset in zip(placed, offsets)}
    edits: list[Edit] = []
    for part_edits in laid_out:
        edits += packing.moved(part_edits, offset_of.get(id(part_edits), (0.0, 0.0)))

    # Keep the whole centred where the nodes were, as a single part is.
    corners = [e.top_left for e in edits if isinstance(e, MoveNode)]
    shift = (
        f32(old_center.x - f32(fmean(x for x, _ in corners))),
        f32(old_center.y - f32(fmean(y for _, y in corners))),
    )
    return clear_of_the_rest(packing.moved(edits, shift))
