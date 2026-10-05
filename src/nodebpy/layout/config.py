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
        nodes (the default: reroutes are real nodes, which would change
        the authored structure of generated trees). ``"blocked"``: links
        that would otherwise be drawn across a node, and the reroutes
        already in the tree are kept. ``"all"``: every link that passes
        over a column, and the tree's own reroutes are replaced.
    stack_collapsed : bool
        Stack chains of collapsed Math nodes vertically.
    optimize_sizes : bool
        Fit the widths of collapsed nodes to their display name.
    straighten_trunk : bool
        Keep the trunk straight. The trunk is the line the tree's main
        data runs along: the links between flow sockets (geometry, shader,
        bundle, closure). They are aligned before any other, so a chain of
        geometry nodes is one flat row with the side chains feeding it
        hung below, a fork that merges again is symmetric around its
        middle branch, and each zone (simulation, repeat, for-each,
        closure) is a row with its node tops level. Off, every link is
        treated alike and a node aligns with its median neighbour.
    pin_group_output : bool
        Put Group Output nodes (outside frames) in the last column.
    pin_group_input : bool
        Put Group Input nodes (outside frames) in the first column, rather
        than next to the nodes they feed.
    sequential_frames : bool
        Rank frames as stages: every node of a frame comes after every
        node of the frame (or intermediate node) feeding it, so frames
        line up left to right instead of stacking.
    balance_heights : bool
        Shorten the tallest columns by moving the chains that feed them one
        column left, while that brings the drawing closer to a screen's
        shape.
    seed : int
        Seed of the shuffled starting orders the ordering tries besides its
        fixed ones. The same seed always gives the same layout.
    pack_components : bool
        Lay out the parts of the tree that are not linked to each other
        apart: the largest first, the others (a second group of nodes, a
        frame holding a note) in rows beneath it. Off, the whole tree is
        laid out as one graph and unrelated parts share its columns.
    """

    margin: tuple[float, float] = (30.0, 30.0)
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "BALANCED"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "NONE"
    reroutes: Literal["none", "blocked", "all"] = "none"
    stack_collapsed: bool = True
    optimize_sizes: bool = False
    straighten_trunk: bool = True
    pin_group_output: bool = True
    pin_group_input: bool = False
    sequential_frames: bool = True
    balance_heights: bool = True
    pack_components: bool = True
    seed: int = 0


SIMPLE_OPTIONS = SugiyamaOptions(
    margin=(50.0, 25.0),
    stack_collapsed=False,
    straighten_trunk=False,
    pin_group_output=False,
    sequential_frames=False,
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
    multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    # Frame-sequence constraints applied by ranking.add_frame_sequence_edges:
    # every node of the first set is ranked before every node of the second.
    frame_sequence: list[tuple[frozenset[Node], frozenset[Node]]] = field(
        default_factory=list
    )
    # Priority of the sockets that have one (see :mod:`.priority`); empty
    # when links are not prioritised.
    socket_priority: dict[bNodeSocket, int] = field(default_factory=dict)
    # The changes to make to the tree, in order. The layout only records
    # them; `apply.apply` carries them out.
    edits: list[Edit] = field(default_factory=list)

    @property
    def margin(self) -> Vec2:
        """Room to leave between nodes, across and down."""
        x, y = self.options.margin
        return Vec2(f32(x), f32(y))
