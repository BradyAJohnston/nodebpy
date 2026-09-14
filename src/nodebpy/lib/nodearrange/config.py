# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree
from mathutils import Vector

if TYPE_CHECKING:
    from .arrange.graph import Node, Socket


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


DEFAULT_MARGIN = (200.0, 20.0)


@dataclass
class LayoutState:
    """All state for a single layout run.

    Replaces the upstream addon's module globals (which acted as ambient
    operator state plus a manual ``reset()``): one instance is created per
    ``sugiyama_layout()`` call and threaded through the pipeline, so nothing
    persists between runs.
    """

    ntree: NodeTree
    settings: Settings = field(default_factory=Settings)
    margin: Vector = field(default_factory=lambda: Vector(DEFAULT_MARGIN))
    selected: list[BlenderNode] = field(default_factory=list)
    linked_sockets: defaultdict[NodeSocket, set[NodeSocket]] = field(
        default_factory=lambda: defaultdict(set)
    )
    multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    # Frame-sequence constraints applied by ranking.add_frame_sequence_edges:
    # every node of the first set is ranked before every node of the second.
    frame_sequence: list[tuple[frozenset[Node], frozenset[Node]]] = field(
        default_factory=list
    )
