# SPDX-License-Identifier: GPL-2.0-or-later
"""What a layout asks to be done to the node tree.

The layout never touches the tree itself. It returns a :class:`LayoutResult`:
the edits to make, in the order to make them. ``apply.apply`` carries
them out on a Blender tree.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .dna import bNode, bNodeSocket, bNodeTree


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
    """Link two sockets."""

    fromsock: bNodeSocket | None
    tosock: bNodeSocket | None


@dataclass(frozen=True, slots=True)
class RemoveLink:
    """Delete the link between two sockets, because it is being rerouted."""

    fromsock: bNodeSocket | None
    tosock: bNodeSocket | None


@dataclass(frozen=True, slots=True)
class RestoreMultiInputOrder:
    """Put the links into a multi-input socket back in their original order.

    ``outputs`` are the sockets to be linked to ``socket``. A link is
    created for any that is missing. ``order`` pairs each of them with the
    sort id its link had before the layout rerouted it.
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
    layout may just have changed. ``apply`` computes the location from the
    node as it then is.
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
    """What a layout returns."""

    edits: list[Edit] = field(default_factory=list)
    """In the order they must be applied."""

    def positions(self) -> dict[bNode, tuple[float, float]]:
        """Where the top-left corner of each node's box ends up."""
        return {e.node: e.top_left for e in self.edits if isinstance(e, MoveNode)}

    def apply_to(self, tree: bNodeTree) -> None:
        """Make the edits to the plain-data *tree* in place, so that it
        describes the tree as laid out. This is what ``apply.apply`` does
        to a Blender tree. Every node keeps the size and the socket offsets
        it came with."""
        for edit in self.edits:
            match edit:
                case RemoveNode(node=node):
                    tree.nodes.remove(node)
                    tree.links[:] = [
                        link
                        for link in tree.links
                        if link.fromnode is not node and link.tonode is not node
                    ]

                case AddReroute(node=node):
                    tree.nodes.append(node)

                case AddLink(fromsock=fromsock, tosock=tosock):
                    assert fromsock is not None and tosock is not None
                    _link(tree, fromsock, tosock)

                case RemoveLink(fromsock=fromsock, tosock=tosock):
                    tree.links.remove(
                        next(
                            link
                            for link in tree.links
                            if link.fromsock is fromsock and link.tosock is tosock
                        )
                    )

                case RestoreMultiInputOrder(
                    socket=socket, outputs=outputs, order=order
                ):
                    assert socket is not None
                    for output in outputs:
                        assert output is not None
                        _link(tree, output, socket)
                    sort_id_of = dict(order)
                    for link in tree.links:
                        if link.tosock is socket and link.fromsock in sort_id_of:
                            link.multi_input_sort_id = sort_id_of[link.fromsock]

                case MoveNode(node=node, top_left=(left, top), parent=parent):
                    dx = left - node.draw_bounds[0]
                    dy = top - node.draw_bounds[3]
                    xmin, ymin, xmax, ymax = node.draw_bounds
                    node.draw_bounds = (xmin + dx, ymin + dy, xmax + dx, ymax + dy)
                    node.location = (node.location[0] + dx, node.location[1] + dy)
                    for socket in (*node.inputs, *node.outputs):
                        if socket.location is not None:
                            socket.location = (
                                socket.location[0] + dx,
                                socket.location[1] + dy,
                            )
                    node.parent = parent

                case ResizeFrame():
                    pass  # a frame's box is derived from its members


def _link(tree: bNodeTree, fromsock: bNodeSocket, tosock: bNodeSocket) -> None:
    """Link two sockets unless they already are, as ``links.new`` does: an
    input that takes one link loses the one it had."""
    into = [link for link in tree.links if link.tosock is tosock]
    if any(link.fromsock is fromsock for link in into):
        return
    if not tosock.is_multi_input:
        for link in into:
            tree.links.remove(link)
        into = []
    tree.add_link(fromsock, tosock, len(into))
