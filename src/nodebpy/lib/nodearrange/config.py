# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from .arrange.common import Vec2
from .arrange.edits import Edit
from .dna import bNodeSocket, bNodeTree

if TYPE_CHECKING:
    from .arrange.graph import Node, Socket


@dataclass(frozen=True, slots=True)
class CrossingWeights:
    """What a crossing of two links costs the ordering, by what the links
    carry: the tree's main data ("flow": geometry, shader, bundle, closure)
    or anything else ("value"). Branches of the trunk passing each other
    read easily; a value cutting across the trunk does not."""

    flow_flow: float = 1.0
    value_value: float = 1.0
    flow_value: float = 4.0


@dataclass
class Settings:
    spacing: float = 30.0
    arrange_mode = "NODES"
    iterations: int = 50
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "LEFT_UP"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "MODERATE"
    add_reroutes: bool = True
    # nodebpy divergence: which links get reroutes when `add_reroutes` is
    # on. "long": every link that passes a column, and the reroutes already
    # in the tree are replaced (upstream). "blocked": only links that would
    # otherwise be drawn across a node, and the tree's own reroutes stay.
    reroute_links: Literal["long", "blocked"] = "long"
    keep_reroutes_outside_frames: bool = False
    stack_collapsed: bool = True
    optimize_sizes: bool = False
    recenter_mode = "NODES"
    origin: Literal["CENTER", "ACTIVE_OUTPUT", "ACTIVE_NODE"] = "CENTER"
    stack_margin_y_fac: float = 0.5
    # nodebpy divergence: rank frames as sequential stages (see
    # ranking.add_frame_sequence_edges).
    sequential_frames: bool = True
    # nodebpy divergence: promote private feeder chains out of the tallest
    # column (see arrange.balancing).
    balance_heights: bool = True
    balance_aspect: float = 1.6
    # nodebpy divergence: fraction of the vertical margin kept between
    # consecutive reroutes / dummy nodes in a column (see
    # y_coords.vertical_gap).
    reroute_margin_y_fac: float = 0.35
    # nodebpy divergence: which strategy runs each phase of the layout (see
    # arrange.pipeline; `pipeline.strategies(phase)` lists the choices).
    ranking: str = "network_simplex"
    ordering: str = "layer_sweep"
    placement: str = "brandes_koepf"
    routing: str = "bend_points"
    # nodebpy divergence: favour the links that carry the tree's main data
    # (see arrange.priority): "flow" keeps them short and straight, "none"
    # treats every link alike.
    # "main" takes each node's main socket as Blender picks it, of whatever
    # type, so chains of values get a trunk too.
    link_priority: Literal["flow", "main", "none"] = "flow"
    # nodebpy divergence: what a crossing costs the "layer_sweep" ordering,
    # by what the two links carry. All equal: every crossing counts alike.
    crossing_weights: CrossingWeights = field(default_factory=CrossingWeights)
    # nodebpy divergence: never split a column of at most this many nodes
    # when balancing heights, so a few parallel branches stay side by side.
    balance_min_column: int = 4
    # nodebpy divergence: put Group Output nodes (outside frames) in the
    # last column, and Group Input nodes in the first. (Any node can be
    # held to the first or last column with `dna.bNode.layer`.)
    pin_group_output: bool = True
    pin_group_input: bool = False
    # nodebpy divergence: draw each zone as a row, from its input node
    # through the nodes its data passes to its output node (see
    # priority.zone_priorities).
    straighten_zones: bool = True
    # nodebpy divergence: lay out the parts of the tree that are not linked
    # to each other apart, the largest first and the others in rows beneath
    # it (see arrange.packing), instead of as one graph sharing columns.
    pack_components: bool = True


DEFAULT_MARGIN = (200.0, 20.0)


@dataclass
class LayoutState:
    """All state for a single layout run.

    Replaces the upstream addon's module globals (which acted as ambient
    operator state plus a manual ``reset()``): one instance is created per
    ``sugiyama_layout()`` call and threaded through the pipeline, so nothing
    persists between runs.
    """

    tree: bNodeTree
    settings: Settings = field(default_factory=Settings)
    margin: Vec2 = field(default_factory=lambda: Vec2(*DEFAULT_MARGIN))
    # Which sockets each socket is linked to, both ways. The values are
    # insertion-ordered sets (dict keys).
    linked_sockets: defaultdict[bNodeSocket, dict[bNodeSocket, None]] = field(
        default_factory=lambda: defaultdict(dict)
    )
    multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    # Frame-sequence constraints applied by ranking.add_frame_sequence_edges:
    # every node of the first set is ranked before every node of the second.
    frame_sequence: list[tuple[frozenset[Node], frozenset[Node]]] = field(
        default_factory=list
    )
    # Priority of the sockets that have one (see arrange.priority); empty
    # when links are not prioritised.
    socket_priority: dict[bNodeSocket, int] = field(default_factory=dict)
    # The changes to make to the tree, in order. The layout only records
    # them; `nodearrange.apply` carries them out.
    edits: list[Edit] = field(default_factory=list)
