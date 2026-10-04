# SPDX-License-Identifier: GPL-2.0-or-later
"""Carry out a layout's edits on a Blender node tree."""

from __future__ import annotations

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree

from .arrange.edits import (
    AddLink,
    AddReroute,
    LayoutResult,
    MoveNode,
    RemoveLink,
    RemoveNode,
    ResizeFrame,
    RestoreMultiInputOrder,
)
from .dna import bNodeSocket
from .extract import Binding
from .utils import abs_loc, get_top, move


def _restore_multi_input_order(
    ntree: NodeTree,
    multi_input: NodeSocket,
    outputs: list[NodeSocket | None],
    order: list[tuple[NodeSocket | None, int]],
) -> None:
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


def apply(ntree: NodeTree, binding: Binding, result: LayoutResult) -> None:
    """Make the edits of *result* to *ntree*, in order. *binding* comes from
    the :func:`~.extract.extract` call that produced the layout's input."""
    nodes: list[BlenderNode] = list(ntree.nodes)

    def bpy_socket(socket: bNodeSocket | None) -> NodeSocket | None:
        return None if socket is None else binding.socket(socket)

    for edit in result.edits:
        match edit:
            case RemoveNode(node=data):
                node = binding.nodes.pop(data)
                nodes.remove(node)
                ntree.nodes.remove(node)

            case AddReroute(node=data):
                reroute = ntree.nodes.new(type="NodeReroute")
                assert reroute is not None
                if data.parent is not None:
                    reroute.parent = binding.nodes[data.parent]
                nodes.append(reroute)
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
                # Optimization: avoid using bpy.ops for as many nodes as
                # possible (see `utils.move()`)
                node.parent = None
                x, y = node.location
                # A collapsed node's box is not anchored at its location.
                target_y = top + (abs_loc(node).y - get_top(node))
                move(node, nodes, x=left - x, y=target_y - y)
                node.parent = None if parent is None else binding.nodes[parent]

            case ResizeFrame(frame=frame_data, children=children):
                frame = binding.nodes[frame_data]
                members = [binding.nodes[child] for child in children]
                for node in members:
                    node.parent = None

                frame.shrink = False  # ty: ignore[unresolved-attribute]
                frame.shrink = True  # ty: ignore[unresolved-attribute]

                for node in members:
                    node.parent = frame
