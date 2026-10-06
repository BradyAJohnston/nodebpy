"""The layout itself: :func:`sugiyama_layout` and the list of steps it runs
(:func:`default_pipeline`), with the steps that are too small for a module
of their own. ``DESIGN.md`` in this package describes every step."""

from __future__ import annotations

from statistics import fmean

from . import packing
from .balancing import balance_column_heights
from .build import add_columns, get_tree, precompute_links, save_multi_input_orders
from .common import Vec2, f32
from .config import LayoutState, SugiyamaOptions
from .dna import bNodeTree
from .edits import Edit, LayoutResult, MoveNode
from .long_links import insert_dummy_nodes, merge_links
from .model import (
    ClusterGraph,
    Kind,
    is_real,
    reset_serials,
)
from .ordering import minimize_crossings
from .pipeline import (
    Fact,
    Layout,
    Observer,
    Pipeline,
    Step,
)
from .placement import bk_assign_y_coords, pull_feeders
from .priority import socket_priorities, zone_priorities
from .ranking import compute_ranks
from .realize import realize_layout, remove_reroutes
from .reroutes import (
    align_reroutes_with_sockets,
    dissolve_clear_dummy_nodes,
    dissolve_dummy_nodes,
)
from .routing import route_links
from .snapping import snap_rows, snap_to_grid
from .spacing import assign_x_coords
from .stacking import contracted_node_stacks, expand_node_stack


def _contract_stacks(layout: Layout) -> None:
    layout.node_stacks = contracted_node_stacks(layout.CG)


def _expand_stacks(layout: Layout) -> None:
    for node_stack in layout.node_stacks:
        expand_node_stack(layout.CG, node_stack)


def _add_frame_borders(layout: Layout) -> None:
    """Add the border nodes of every frame, then drop the fill dummy nodes
    that held a frame's place in the columns where it has no node."""
    CG = layout.CG
    CG.add_vertical_border_nodes()
    CG.remove_nodes([v for v in CG.G if v.is_fill_dummy])


def _remove_frame_borders(layout: Layout) -> None:
    CG = layout.CG
    CG.remove_nodes([v for v in CG.G if v.type == Kind.VERTICAL_BORDER])


def _prioritize_links(layout: Layout) -> None:
    tree = layout.state.tree
    priorities = socket_priorities(tree)
    priorities.update(zone_priorities(tree))
    layout.state.socket_priority = priorities


def pin_group_nodes(layout: Layout) -> None:
    """Move Group Output nodes to the last column and Group Input nodes to
    the first, where the options ask. Only a Group Output outside frames
    that feeds nothing and a Group Input outside frames that nothing feeds
    are moved, because moving those cannot break a constraint."""
    options = layout.options
    G = layout.G
    root = next(c for c in layout.CG.S if not layout.T.predecessors(c))
    ranks = [v.rank for v in G]
    first, last = min(ranks), max(ranks)
    for v in G:
        if not is_real(v) or v.cluster is not root:
            continue
        node = v.node
        if options.pin_group_output and node.is_group_output() and not G.successors(v):
            v.rank = last
        if options.pin_group_input and node.is_group_input() and not G.predecessors(v):
            v.rank = first


def default_pipeline() -> Pipeline:
    """The standard layout: the steps in order."""
    F = Fact

    def reroutes(s: SugiyamaOptions) -> bool:
        return s.reroutes != "none"

    def replacing_reroutes(s: SugiyamaOptions) -> bool:
        return s.reroutes == "all"

    def sparing_reroutes(s: SugiyamaOptions) -> bool:
        return s.reroutes == "blocked"

    def no_reroutes(s: SugiyamaOptions) -> bool:
        return s.reroutes == "none"

    def stacks(s: SugiyamaOptions) -> bool:
        return s.stack_collapsed

    return Pipeline(
        [
            # Prepare the graph.
            Step(
                "prioritize_links",
                _prioritize_links,
                lambda s: s.straighten_trunk,
            ),
            Step(
                "save_multi_input_orders",
                lambda L: save_multi_input_orders(L.G, L.state),
            ),
            Step(
                "remove_reroutes", lambda L: remove_reroutes(L.CG), replacing_reroutes
            ),
            Step("contract_stacks", _contract_stacks, stacks),
            # Columns.
            Step(
                "rank",
                lambda L: compute_ranks(L.CG),
                phase="rank",
                provides={F.RANKED},
            ),
            Step(
                "balance_heights",
                lambda L: balance_column_heights(L.G, L.CG.S, L.state),
                lambda s: s.balance_heights,
                requires={F.RANKED},
            ),
            # After the balancing, which would otherwise move a pinned node
            # along with the nodes it moves left.
            Step("pin_group_nodes", pin_group_nodes, requires={F.RANKED}),
            Step("merge_edges", lambda L: merge_links(L.CG), requires={F.RANKED}),
            Step(
                "insert_dummy_nodes",
                lambda L: insert_dummy_nodes(L.CG),
                requires={F.RANKED},
                provides={F.PROPER},
            ),
            Step(
                "add_columns",
                lambda L: add_columns(L.G),
                requires={F.RANKED},
                provides={F.COLUMNS},
            ),
            # Order within the columns.
            Step(
                "order",
                lambda L: minimize_crossings(L.G, L.T, L.state),
                phase="order",
                requires={F.PROPER, F.COLUMNS},
                provides={F.ORDERED},
            ),
            # Positions along the columns.
            Step(
                "add_frame_borders",
                _add_frame_borders,
                requires={F.ORDERED},
                provides={F.BORDERS},
            ),
            Step(
                "place",
                lambda L: bk_assign_y_coords(L.G, L.T, L.state),
                phase="place",
                requires={F.ORDERED, F.BORDERS},
                provides={F.Y},
            ),
            Step(
                "pull_feeders",
                lambda L: pull_feeders(L.G, L.state),
                requires={F.Y},
            ),
            Step(
                "snap_rows",
                snap_rows,
                lambda s: s.snap_to_grid,
                requires={F.Y},
            ),
            Step(
                "dissolve_dummy_nodes",
                lambda L: dissolve_dummy_nodes(L.CG),
                no_reroutes,
                requires={F.Y},
                removes={F.PROPER},
            ),
            Step(
                "align_reroutes",
                lambda L: align_reroutes_with_sockets(L.CG),
                requires={F.Y},
            ),
            Step(
                "remove_frame_borders",
                _remove_frame_borders,
                requires={F.BORDERS},
                removes={F.BORDERS},
            ),
            # Positions across the columns, and the links between them.
            Step(
                "space_columns",
                lambda L: assign_x_coords(L.G, L.T, L.state),
                requires={F.COLUMNS, F.Y},
                provides={F.X},
            ),
            Step(
                "dissolve_clear_dummy_nodes",
                lambda L: dissolve_clear_dummy_nodes(L.CG),
                sparing_reroutes,
                requires={F.PROPER, F.X},
                removes={F.PROPER},
            ),
            Step(
                "route",
                lambda L: route_links(L.G, L.T, L.state),
                reroutes,
                phase="route",
                requires={F.X},
                # Bend points are new nodes, outside the ranks and columns.
                removes={F.RANKED, F.PROPER, F.COLUMNS},
            ),
            # Write the result out.
            Step(
                "expand_stacks",
                _expand_stacks,
                stacks,
                requires={F.X},
                # The nodes of a stack come back without a rank or column.
                removes={F.RANKED, F.PROPER, F.COLUMNS},
            ),
            Step(
                "realize",
                lambda L: realize_layout(L.CG, L.old_center),
                requires={F.X},
                # Chains of dummy nodes become reroutes, fewer than columns.
                removes={F.PROPER},
            ),
        ]
    )


def sugiyama_layout(
    tree: bNodeTree,
    options: SugiyamaOptions | None = None,
    *,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
    verify: bool = False,
    selected_only: bool = False,
) -> LayoutResult:
    """Lay out *tree* and return the edits that realise the layout.

    *tree* is only read. *pipeline* replaces the steps of
    :func:`default_pipeline`. *observer* is called after each step with the
    step, the layout and the seconds taken. With *verify* the graph is
    checked after every step, and a step that breaks an invariant raises
    :class:`~.pipeline.InvariantError`. That is slower, and meant for tests
    and for developing steps. With *selected_only* the selected nodes are
    arranged among themselves around where they were, and the others do not
    move.

    With ``pack_components`` each part of the tree is laid out by itself
    and the results are packed (:mod:`.packing`).
    """
    reset_serials()
    fixed = frozenset(n for n in tree.nodes if selected_only and not n.select)
    state = LayoutState(tree=tree, options=options or SugiyamaOptions())
    # The top-left corners, which is what the result is centred by.
    locs = [
        (n.draw_bounds[0], n.draw_bounds[3])
        for n in tree.nodes
        if n not in fixed and not n.is_frame()
    ]

    if not locs:
        return LayoutResult()

    xs, ys = zip(*locs)
    old_center = Vec2(f32(fmean(xs)), f32(fmean(ys)))

    def lay_out(part: bNodeTree) -> list[Edit]:
        part_state = LayoutState(part, state.options, fixed)
        precompute_links(part_state)
        layout = Layout(ClusterGraph(get_tree(part_state), part_state), old_center)
        (pipeline or default_pipeline()).run(layout, observer, verify=verify)
        return part_state.edits

    def clear_of_the_rest(edits: list[Edit]) -> list[Edit]:
        """Move the laid-out nodes clear of the fixed ones. They stay where
        they are when that would take them further than twice the longer
        side of the box around them."""
        obstacles = [
            n.draw_bounds
            for n in tree.nodes
            if n in fixed and not n.is_frame() and not n.is_reroute()
        ]
        if not obstacles:
            return edits
        rects = packing.node_rects(edits)
        if not rects:
            return edits
        # The vertical margin is used in both directions.
        dx, dy = packing.clear_of(
            rects, obstacles, Vec2(state.margin.y, state.margin.y)
        )
        width = max(r[2] for r in rects) - min(r[0] for r in rects)
        height = max(r[3] for r in rects) - min(r[1] for r in rects)
        if max(abs(dx), abs(dy)) > 2 * max(width, height):
            return edits
        return packing.moved(edits, (f32(dx), f32(dy)))

    def finish(edits: list[Edit]) -> LayoutResult:
        edits = clear_of_the_rest(edits)
        if state.options.snap_to_grid:
            edits = snap_to_grid(edits)
        return LayoutResult(edits)

    parts = packing.components(tree, fixed) if state.options.pack_components else []
    if len(parts) < 2:
        return finish(lay_out(tree))

    # The part with the most nodes comes first. The others, largest first,
    # are packed beneath it.
    parts.sort(key=len, reverse=True)
    laid_out = [lay_out(packing.subtree(tree, part)) for part in parts]
    boxes = [packing.bounds(edits) for edits in laid_out]
    gap = Vec2(state.margin.x, f32(3 * state.margin.y))
    offsets = iter(packing.pack([box for box in boxes if box is not None], gap))
    edits: list[Edit] = []
    for part_edits, box in zip(laid_out, boxes):
        offset = next(offsets) if box is not None else (0.0, 0.0)
        edits += packing.moved(part_edits, offset)

    # Keep the whole centred where the nodes were, as a single part is.
    corners = [e.top_left for e in edits if isinstance(e, MoveNode)]
    shift = (
        f32(old_center.x - f32(fmean(x for x, _ in corners))),
        f32(old_center.y - f32(fmean(y for _, y in corners))),
    )
    return finish(packing.moved(edits, shift))
