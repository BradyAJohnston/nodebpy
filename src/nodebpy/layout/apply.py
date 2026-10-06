# SPDX-License-Identifier: GPL-2.0-or-later
"""Carry out a layout's edits on a Blender node tree."""

from __future__ import annotations

from array import array

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree

from .common import FRAME_PADDING, f32, frame_label_room
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
from .node_size import dimensions, size_cache, top_offset


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


def _frame_box(
    frame: BlenderNode, boxes: list[tuple[float, float, float, float]]
) -> tuple[float, float, float, float]:
    """Left, top, width and height of *frame* fitted around *boxes*, the
    boxes of the nodes in it."""
    label = frame_label_room(frame.label, getattr(frame, "label_size", 20))
    left = min(b[0] for b in boxes) - FRAME_PADDING
    bottom = min(b[1] for b in boxes) - FRAME_PADDING
    right = max(b[2] for b in boxes) + FRAME_PADDING
    top = max(b[3] for b in boxes) + FRAME_PADDING + label
    return left, top, right - left, top - bottom


def _write_locations(
    ntree: NodeTree,
    binding: Binding,
    moves: list[MoveNode],
    frames: list[ResizeFrame],
) -> None:
    """Carry out the moves, and refit the frames around the moved nodes.

    Every location is written in one call. Setting a node's location one
    at a time updates the whole tree each time, which makes arranging a
    large tree quadratic. Frames with Shrink off are sized here as well,
    leaving that setting as the user had it: Blender only refits a frame
    itself when Shrink is on and a node editor draws it."""
    nodes = list(ntree.nodes)
    index = {node.as_pointer(): i for i, node in enumerate(nodes)}
    located = array("f", bytes(8 * len(nodes)))
    ntree.nodes.foreach_get("location_absolute", located)

    def box(node: BlenderNode) -> tuple[float, float, float, float]:
        i = index[node.as_pointer()]
        x, top = located[2 * i], located[2 * i + 1] - top_offset(node)
        width, height = dimensions(node)
        return (x, top - height, x + width, top)

    for move in moves:
        node = binding.nodes[move.node]
        node.parent = None if move.parent is None else binding.nodes[move.parent]
        i = index[node.as_pointer()]
        left, top = move.top_left
        # A collapsed node's box is not anchored at its location.
        located[2 * i], located[2 * i + 1] = left, top + top_offset(node)

    for edit in frames:
        frame = binding.nodes[edit.frame]
        left, top, width, height = _frame_box(
            frame, [box(binding.nodes[child]) for child in edit.children]
        )
        i = index[frame.as_pointer()]
        located[2 * i], located[2 * i + 1] = left, top
        frame.width = width
        frame.height = height

    # Positions are dumped to two decimals. Rounding them keeps an arranged
    # tree unchanged through a round trip.
    relative = array("f", located)
    for i, node in enumerate(nodes):
        parent = node.parent
        if parent is not None:
            j = index[parent.as_pointer()]
            relative[2 * i] = f32(located[2 * i] - located[2 * j])
            relative[2 * i + 1] = f32(located[2 * i + 1] - located[2 * j + 1])
    ntree.nodes.foreach_set("location", [round(v, 2) for v in relative])


def apply(ntree: NodeTree, binding: Binding, result: LayoutResult) -> None:
    """Make the edits of *result* to *ntree*. *binding* comes from the
    :func:`~.extract.extract` call that produced the layout's input.

    The link and reroute edits are made in order. The moves and frame
    refits are gathered and written together at the end."""

    def bpy_socket(socket: bNodeSocket | None) -> NodeSocket | None:
        return None if socket is None else binding.socket(socket)

    moves: list[MoveNode] = []
    frames: list[ResizeFrame] = []
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

            case MoveNode():
                moves.append(edit)

            case ResizeFrame():
                frames.append(edit)

    if moves or frames:
        with size_cache():
            _write_locations(ntree, binding, moves, frames)
