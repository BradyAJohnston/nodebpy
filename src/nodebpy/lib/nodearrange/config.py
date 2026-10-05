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


@dataclass
class Settings:
    """What the layout can be asked to do differently. (The numbers it is
    tuned with are constants next to the code that uses them.)"""

    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "BALANCED"
    )
    """Which way nodes lean when they could sit in several places along a
    column; ``BALANCED`` takes the middle of the four."""
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "NONE"
    """Whether aligned nodes line up by their tops (``NONE``), by the
    sockets of the link between them (``FULL``), or by sockets only where
    the nodes differ much in height (``MODERATE``)."""
    reroutes: Literal["none", "blocked", "all"] = "none"
    """Which links get reroutes. ``none``: the layout only moves nodes.
    ``blocked``: links that would otherwise be drawn across a node, and the
    tree's own reroutes stay. ``all``: every link that passes a column, and
    the tree's own reroutes are replaced."""
    stack_collapsed: bool = True
    """Stack chains of collapsed Math nodes vertically."""
    optimize_sizes: bool = False
    """Fit the widths of collapsed nodes to their names first."""
    straighten_trunk: bool = True
    """Align the links that carry the tree's main data before any other
    (see :mod:`.arrange.priority`), and draw each zone as a level row."""
    pin_group_output: bool = True
    """Put Group Output nodes (outside frames) in the last column."""
    pin_group_input: bool = False
    """Put Group Input nodes (outside frames) in the first column."""
    sequential_frames: bool = True
    """Rank frames as stages, each after the one that feeds it (see
    :func:`.arrange.ranking.add_frame_sequence_edges`)."""
    balance_heights: bool = True
    """Shorten the tallest columns by moving feeder chains left (see
    :mod:`.arrange.balancing`)."""
    pack_components: bool = True
    """Lay out the unconnected parts of the tree apart (see
    :mod:`.arrange.packing`)."""


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
