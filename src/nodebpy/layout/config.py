# SPDX-License-Identifier: GPL-2.0-or-later
"""What the layout can be asked to do (:class:`SugiyamaOptions`), and the
state of one run of it (:class:`LayoutState`)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from .common import Vec2, f32
from .dna import bNode, bNodeSocket, bNodeTree
from .edits import Edit

if TYPE_CHECKING:
    from .model import Node, Socket


@dataclass(frozen=True)
class SugiyamaOptions:
    """Options for the Sugiyama (layered) arrangement.

    Parameters
    ----------
    margin : tuple[float, float]
        Horizontal and vertical space between nodes.
    direction : str
        Which way nodes lean where they could sit in several places along
        a column: ``"LEFT_UP"``, ``"LEFT_DOWN"``, ``"RIGHT_UP"``,
        ``"RIGHT_DOWN"``, or ``"BALANCED"`` for the middle of the four.
    socket_alignment : str
        Whether aligned nodes line up by their tops (``"NONE"``), by the
        sockets of the link between them so the link is straight
        (``"FULL"``), or by sockets only where the nodes differ much in
        height (``"MODERATE"``).
    reroutes : str
        Which links get reroute nodes. ``"none"``: the layout only moves
        nodes. ``"blocked"``: links that would otherwise be drawn across a
        node get reroutes, and the reroutes already in the tree are kept.
        ``"all"``: every link that passes over a column gets reroutes, and
        the tree's own reroutes are replaced.
    stack_collapsed : bool
        Stack chains of collapsed Math nodes vertically.
    fit_collapsed_widths : bool
        Fit the widths of collapsed nodes to their display name.
    straighten_trunk : bool
        Align the trunk first, so that the flow links (geometry, shader,
        bundle, closure) form a straight row and each zone is a row with
        its node tops level. Off, a node aligns with its median neighbour.
    pin_group_output : bool
        Put Group Output nodes (outside frames) in the last column.
    pin_group_input : bool
        Put Group Input nodes (outside frames) in the first column. Off,
        they sit next to the nodes they feed.
    frames_as_stages : bool
        Put every node of a frame in a later column than every node of
        the frame, or node outside frames, that feeds it. Frames then line
        up left to right.
    balance_heights : bool
        Shorten the tallest columns by moving the chains that feed them one
        column left, while that brings the drawing closer to a screen's
        shape.
    seed : int
        Seed of the shuffled starting orders the ordering tries besides its
        fixed ones. The same seed always gives the same layout.
    snap_to_grid : bool
        Put every node on the node editor's grid, as Blender's Snap does
        when nodes are moved by hand, and space the nodes of a column in
        whole grid steps. Reroutes are not snapped; they follow the sockets
        they join. With this on, ``socket_alignment`` can only line sockets
        up to within half a grid step.
    """

    margin: tuple[float, float] = (30.0, 30.0)
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "BALANCED"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "NONE"
    reroutes: Literal["none", "blocked", "all"] = "none"
    stack_collapsed: bool = True
    fit_collapsed_widths: bool = False
    straighten_trunk: bool = True
    pin_group_output: bool = True
    pin_group_input: bool = False
    frames_as_stages: bool = True
    balance_heights: bool = True
    pack_components: bool = True
    seed: int = 0
    snap_to_grid: bool = True


SIMPLE_OPTIONS = SugiyamaOptions(
    margin=(50.0, 25.0),
    stack_collapsed=False,
    straighten_trunk=False,
    pin_group_output=False,
    frames_as_stages=False,
    balance_heights=False,
    pack_components=False,
)
"""What ``arrange(tree, "simple")`` uses: nodes in columns by dependency,
with none of the refinements."""


@dataclass
class LayoutState:
    """All the state of one layout run: what it was asked for, what it
    indexes on the way, and the edits it produces. One is created per part
    of the tree laid out and passed through the pipeline, so nothing
    persists between runs."""

    tree: bNodeTree
    options: SugiyamaOptions = field(default_factory=SugiyamaOptions)
    # The nodes the layout leaves where they are: the unselected ones, when
    # only the selection is arranged.
    fixed: frozenset[bNode] = frozenset()
    # Which sockets each socket is linked to, both ways. The values are
    # insertion-ordered sets (dict keys).
    linked_sockets: defaultdict[bNodeSocket, dict[bNodeSocket, None]] = field(
        default_factory=lambda: defaultdict(dict)
    )
    # For each multi-input socket, the (source socket, sort id) of every
    # link into it before the layout.
    multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    # Frame-sequence constraints applied by ranking.add_frame_sequence_edges:
    # every node of the first set is ranked before every node of the second.
    frame_sequence: list[tuple[frozenset[Node], frozenset[Node]]] = field(
        default_factory=list
    )
    # Priority of the sockets that have one (see :mod:`.priority`). Empty
    # when links are not prioritised.
    socket_priority: dict[bNodeSocket, int] = field(default_factory=dict)
    # The changes to make to the tree, in order. The layout only records
    # them. `apply.apply` carries them out.
    edits: list[Edit] = field(default_factory=list)

    @property
    def margin(self) -> Vec2:
        """Room to leave between nodes, across and down."""
        x, y = self.options.margin
        return Vec2(f32(x), f32(y))
