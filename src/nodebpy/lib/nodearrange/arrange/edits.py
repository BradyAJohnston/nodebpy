# SPDX-License-Identifier: GPL-2.0-or-later
"""What a layout asks to be done to the node tree.

The layout never touches the tree itself. It returns a :class:`LayoutResult`:
the edits to make, in the order to make them. ``nodearrange.apply`` carries
them out on a Blender tree; a C++ port would do the same with
``bke::node_remove_node``, ``bke::node_add_link`` and friends.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..dna import bNode, bNodeSocket


@dataclass(frozen=True, slots=True)
class RemoveNode:
    """Delete a node (a reroute the layout replaces), with its links."""

    node: bNode


@dataclass(frozen=True, slots=True)
class AddReroute:
    """Create a reroute node in the frame ``node.parent``. Later edits refer
    to it, and to its sockets, through ``node``."""

    node: bNode


@dataclass(frozen=True, slots=True)
class AddLink:
    fromsock: bNodeSocket | None
    tosock: bNodeSocket | None


@dataclass(frozen=True, slots=True)
class RemoveLink:
    """Delete the link between two sockets (it is being rerouted)."""

    fromsock: bNodeSocket | None
    tosock: bNodeSocket | None


@dataclass(frozen=True, slots=True)
class RestoreMultiInputOrder:
    """Put the links into a multi-input socket back in their original order.

    ``outputs`` are the sockets now linked to ``socket`` (a link is created
    for any that is missing). ``order`` pairs each of them with the sort id
    its link had before the layout rerouted it.
    """

    socket: bNodeSocket | None
    outputs: tuple[bNodeSocket | None, ...]
    order: tuple[tuple[bNodeSocket | None, int], ...]


@dataclass(frozen=True, slots=True)
class MoveNode:
    """Place a node inside the frame ``parent`` so that the top-left corner
    of the box it is drawn in is at ``top_left`` (absolute).

    This is not always the node's ``location``: a collapsed node is drawn
    around its location, by an amount that depends on its links, which the
    layout may just have changed. Whoever applies the edit works that out
    from the node as it then is.
    """

    node: bNode
    top_left: tuple[float, float]
    parent: bNode | None


@dataclass(frozen=True, slots=True)
class ResizeFrame:
    """Refit a frame that does not shrink to its members by itself."""

    frame: bNode
    children: tuple[bNode, ...]


type Edit = (
    RemoveNode
    | AddReroute
    | AddLink
    | RemoveLink
    | RestoreMultiInputOrder
    | MoveNode
    | ResizeFrame
)


@dataclass(slots=True)
class LayoutResult:
    edits: list[Edit] = field(default_factory=list)
    """In the order they must be applied."""

    def positions(self) -> dict[bNode, tuple[float, float]]:
        """Where the top-left corner of each node's box ends up."""
        return {e.node: e.top_left for e in self.edits if isinstance(e, MoveNode)}
