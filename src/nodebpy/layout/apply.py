# SPDX-License-Identifier: GPL-2.0-or-later
"""Carry out a layout's edits on a Blender node tree."""

from __future__ import annotations

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree

from .common import FRAME_PADDING, frame_label_room
from .dna import bNodeSocket
from .edits import (
    AddLink,
    AddReroute,
    LayoutResult,
    MoveNode,
    RemoveLink,
    RemoveNode,
    ResizeFrame,
    RestoreMultiInputOrder,
)
from .extract import Binding
from .node_size import dimensions, get_bottom, get_top


def _restore_multi_input_order(
    ntree: NodeTree,
    multi_input: NodeSocket,
    outputs: list[NodeSocket | None],
    order: list[tuple[NodeSocket | None, int]],
) -> None:
    """Link every one of *outputs* to *multi_input* and give each link the
    sort id *order* pairs its output with.

    Removing and re-adding a link leaves duplicate sort ids. When there are
    duplicates, all the links into the socket are rebuilt so that the ids
    are distinct before they are swapped into place."""
    links = ntree.links
    as_links = {
        link.from_socket: link
        for link in links
        if link.to_socket == multi_input and link.from_socket is not None
    }

    # The creation order of these links sets their sort ids.
    for output in outputs:
        if output in as_links:
            continue
        assert output
        new_link = links.new(output, multi_input)
        assert new_link is not None
        as_links[output] = new_link

    if len(as_links) != len({link.multi_input_sort_id for link in as_links.values()}):
        for link in as_links.values():
            links.remove(link)

        for output in as_links:
            new_link = links.new(output, multi_input)
            assert new_link is not None
            as_links[output] = new_link

    for output, sort_id in order:
        other = min(
            as_links.values(),
            key=lambda link: abs(link.multi_input_sort_id - sort_id),
        )
        assert output is not None
        as_links[output].swap_multi_input_sort_id(other)


def _fit_frame(frame: BlenderNode, members: list[BlenderNode]) -> None:
    """Size and place *frame* around *members* (the nodes in it), leaving its
    Shrink setting as the user had it. Blender only refits a frame itself
    when Shrink is on and a node editor draws it."""
    boxes = []
    for node in members:
        x = node.location_absolute.x
        boxes.append((x, get_bottom(node), x + dimensions(node)[0], get_top(node)))
    label = frame_label_room(frame.label, getattr(frame, "label_size", 20))
    left = min(b[0] for b in boxes) - FRAME_PADDING
    bottom = min(b[1] for b in boxes) - FRAME_PADDING
    right = max(b[2] for b in boxes) + FRAME_PADDING
    top = max(b[3] for b in boxes) + FRAME_PADDING + label

    # Moving a frame by its absolute location leaves its nodes in place.
    frame.location_absolute = (left, top)
    frame.width = right - left
    frame.height = top - bottom


def apply(ntree: NodeTree, binding: Binding, result: LayoutResult) -> None:
    """Make the edits of *result* to *ntree*, in order. *binding* comes from
    the :func:`~.extract.extract` call that produced the layout's input."""

    def bpy_socket(socket: bNodeSocket | None) -> NodeSocket | None:
        return None if socket is None else binding.socket(socket)

    for edit in result.edits:
        match edit:
            case RemoveNode(node=data):
                node = binding.nodes.pop(data)
                ntree.nodes.remove(node)

            case AddReroute(node=data):
                reroute = ntree.nodes.new(type="NodeReroute")
                assert reroute is not None
                if data.parent is not None:
                    reroute.parent = binding.nodes[data.parent]
                binding.nodes[data] = reroute

            case AddLink(fromsock=fromsock, tosock=tosock):
                ntree.links.new(bpy_socket(fromsock), bpy_socket(tosock))  # ty: ignore[invalid-argument-type]

            case RemoveLink(fromsock=fromsock, tosock=tosock):
                target = (bpy_socket(fromsock), bpy_socket(tosock))
                ntree.links.remove(
                    next(
                        link
                        for link in ntree.links
                        if (link.from_socket, link.to_socket) == target
                    )
                )

            case RestoreMultiInputOrder(socket=socket, outputs=outputs, order=order):
                multi_input = bpy_socket(socket)
                assert multi_input
                _restore_multi_input_order(
                    ntree,
                    multi_input,
                    [bpy_socket(s) for s in outputs],
                    [(bpy_socket(s), sort_id) for s, sort_id in order],
                )

            case MoveNode(node=data, top_left=(left, top), parent=parent):
                node = binding.nodes[data]
                # A collapsed node's box is not anchored at its location.
                offset = node.location_absolute.y - get_top(node)
                node.parent = None if parent is None else binding.nodes[parent]
                node.location_absolute = (left, top + offset)

            case ResizeFrame(frame=frame_data, children=children):
                frame = binding.nodes[frame_data]
                members = [binding.nodes[child] for child in children]
                _fit_frame(frame, members)
