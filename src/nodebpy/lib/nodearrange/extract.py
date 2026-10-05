# SPDX-License-Identifier: GPL-2.0-or-later
"""Read a Blender node tree into the plain data the layout works on.

This is the only place node sizes and socket positions are measured. Blender
computes them when a node editor draws the tree; where it has not (always,
under the headless ``bpy`` module) they are estimated from the node's
sockets and properties.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree

from .dna import bNode, bNodeSocket, bNodeTree
from .utils import abs_loc, dimensions, get_bottom, get_top
from .zones import find_zones

# -------------------------------------------------------------------


def get_display_name_of(node: BlenderNode) -> str:
    if node.label:
        return node.label

    if node.bl_idname.endswith("NodeGroup") and (
        tree := getattr(node, "node_tree", None)
    ):
        return tree.name

    if node.bl_idname.endswith("Math") or node.bl_idname == "FunctionNodeCompare":
        return getattr(node, "operation", node.bl_label)

    relevant_node_types = {
        "ShaderNodeTexImage",
        "ShaderNodeTexEnvironment",
        "CompositorNodeImage",
    }
    if node.bl_idname in relevant_node_types and (
        image := getattr(node, "image", None)
    ):
        return image.name

    return node.bl_label


NODE_LABEL_SIZE = 11
LABEL_LEFT_OFFSET = 23
LABEL_RIGHT_OFFSET = LABEL_LEFT_OFFSET

# Rough advance width per character, as a fraction of the font size. Used when
# `blf` can't measure text (e.g. the headless `bpy` module without a UI font).
_FALLBACK_CHAR_WIDTH_FAC = 0.6


def _label_width(text: str) -> float:
    try:
        import blf

        blf.size(0, NODE_LABEL_SIZE)
        width: float = blf.dimensions(0, text)[0]
    except (ImportError, RuntimeError):
        return len(text) * NODE_LABEL_SIZE * _FALLBACK_CHAR_WIDTH_FAC
    # Headless builds can report a zero width instead of raising.
    return (
        width if width > 0 else len(text) * NODE_LABEL_SIZE * _FALLBACK_CHAR_WIDTH_FAC
    )


def optimize_sizes(nodes: Iterable[BlenderNode]) -> None:
    for node in nodes:
        if not node.hide:
            continue

        display_name = get_display_name_of(node)
        optimized_width = (
            _label_width(display_name) + LABEL_LEFT_OFFSET + LABEL_RIGHT_OFFSET
        )
        node.width = max(optimized_width, node.bl_width_min)


# -------------------------------------------------------------------


def get_socket_y(socket: NodeSocket) -> float:
    """The height at which links attach to *socket*: estimated from the
    rows the node draws, since Python is not told where Blender drew it."""
    node = socket.node
    assert node is not None

    from ...builder.layout import calculate_socket_offset_y

    return get_top(node) + calculate_socket_offset_y(socket)


@dataclass(eq=False, slots=True)
class Binding:
    """Which Blender node each node of an extracted tree stands for, so the
    layout's edits can be applied to the Blender tree."""

    nodes: dict[bNode, BlenderNode] = field(default_factory=dict)

    def socket(self, socket: bNodeSocket) -> NodeSocket:
        """The Blender socket *socket* stands for. Looked up afresh each
        time: Blender replaces a reroute's sockets when it is linked, so a
        socket reference does not stay valid."""
        node = self.nodes[socket.node]
        sockets = node.outputs if socket.is_output else node.inputs
        return sockets[socket.index]


def _extract_node(node: BlenderNode) -> bNode:
    x, y = abs_loc(node)
    data = bNode(
        name=node.name,
        idname=node.bl_idname,
        label=node.label,
        location=(x, y),
        is_collapsed=node.hide,
    )
    if data.is_frame():
        data.label_size = getattr(node, "label_size", data.label_size)
        data.shrink = getattr(node, "shrink", data.shrink)
    else:
        width = dimensions(node).x
        data.width = width
        data.draw_bounds = (x, get_bottom(node), x + width, get_top(node))

    for socket in node.inputs:
        data.add_socket(
            False, is_multi_input=socket.is_multi_input, idname=socket.bl_idname
        )
    for socket in node.outputs:
        data.add_socket(True, idname=socket.bl_idname)
    return data


def extract(ntree: NodeTree) -> tuple[bNodeTree, Binding]:
    """The plain-data copy of *ntree*, and the binding back to it."""
    tree = bNodeTree()
    binding = Binding()
    data_of: dict[BlenderNode, bNode] = {}
    for node in ntree.nodes:
        data = tree.add_node(_extract_node(node))
        data.select = node.select
        data_of[node] = data
        binding.nodes[data] = node

    for node, data in data_of.items():
        if node.parent is not None:
            data.parent = data_of[node.parent]

    socket_of = {
        bpy_socket: socket
        for node, data in data_of.items()
        for sockets, bpy_sockets in (
            (data.inputs, node.inputs),
            (data.outputs, node.outputs),
        )
        for socket, bpy_socket in zip(sockets, bpy_sockets)
    }
    for link in ntree.links:
        if link.from_socket is None or link.to_socket is None:
            continue

        fromsock = socket_of[link.from_socket]
        tosock = socket_of[link.to_socket]
        data_link = tree.add_link(fromsock, tosock, link.multi_input_sort_id)
        data_link.is_valid = link.is_valid

        # Only sockets with a link need a position.
        for socket, bpy_socket in (
            (fromsock, link.from_socket),
            (tosock, link.to_socket),
        ):
            node = socket.node
            if socket.location is None and not node.is_reroute():
                x = node.draw_bounds[2] if socket.is_output else node.draw_bounds[0]
                socket.location = (x, get_socket_y(bpy_socket))

    pairs = []
    for node, data in data_of.items():
        output = getattr(node, "paired_output", None)
        if output is not None:
            pairs.append((data, data_of[output]))
    tree.zones = find_zones(tree, pairs)

    return tree, binding
