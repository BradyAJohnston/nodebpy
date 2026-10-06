"""Read a Blender node tree into the plain data the layout works on.

Node sizes and socket positions enter the layout only here;
:mod:`.node_size` says where they come from.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket, NodeTree

from .dna import bNode, bNodeSocket, bNodeTree
from .node_size import (
    calculate_socket_offset_y,
    dimensions,
    get_bottom,
    get_top,
    size_cache,
)
from .zones import find_zones

_IMAGE_NODES = {"ShaderNodeTexImage", "ShaderNodeTexEnvironment", "CompositorNodeImage"}


def _display_name(node: BlenderNode) -> str:
    """The text a collapsed node's width is fitted to: its label, else the
    name of its group, operation or image, else the label of its type."""
    if node.label:
        return node.label

    if node.bl_idname.endswith("NodeGroup") and (
        tree := getattr(node, "node_tree", None)
    ):
        return tree.name

    if node.bl_idname.endswith("Math") or node.bl_idname == "FunctionNodeCompare":
        return getattr(node, "operation", node.bl_label)

    if node.bl_idname in _IMAGE_NODES and (image := getattr(node, "image", None)):
        return image.name

    return node.bl_label


_NODE_LABEL_SIZE = 11  # font size of a collapsed node's label
_LABEL_PADDING = 23  # either side of the label
# Rough advance width per character, as a fraction of the font size, for
# when blf cannot measure text (the headless bpy module has no UI font).
_FALLBACK_CHAR_WIDTH_FAC = 0.6


def _label_width(text: str) -> float:
    try:
        import blf

        blf.size(0, _NODE_LABEL_SIZE)
        width: float = blf.dimensions(0, text)[0]
    except (ImportError, RuntimeError):
        width = 0.0
    # Headless builds raise, or report no width.
    return width or len(text) * _NODE_LABEL_SIZE * _FALLBACK_CHAR_WIDTH_FAC


def fit_collapsed_widths(nodes: Iterable[BlenderNode]) -> None:
    """Set the width of every collapsed node to fit its display name."""
    for node in nodes:
        if not node.hide:
            continue

        width = _label_width(_display_name(node)) + 2 * _LABEL_PADDING
        node.width = max(width, node.bl_width_min)


@dataclass(eq=False, slots=True)
class Binding:
    """Which Blender node each node of an extracted tree stands for, so the
    layout's edits can be applied to the Blender tree."""

    nodes: dict[bNode, BlenderNode] = field(default_factory=dict)

    def socket(self, socket: bNodeSocket) -> NodeSocket:
        """The Blender socket *socket* stands for, looked up afresh each
        time: Blender may rebuild a node's sockets when its links change (a
        reroute takes the type of what it is linked to), so a socket
        reference is not kept."""
        node = self.nodes[socket.node]
        sockets = node.outputs if socket.is_output else node.inputs
        return sockets[socket.index]


def _extract_node(node: BlenderNode) -> bNode:
    x, y = node.location_absolute
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
        width = dimensions(node)[0]
        data.width = width
        data.draw_bounds = (x, get_bottom(node), x + width, get_top(node))

    for socket in node.inputs:
        data.add_socket(
            False, is_multi_input=socket.is_multi_input, idname=socket.bl_idname
        )
    for socket in node.outputs:
        data.add_socket(True, idname=socket.bl_idname)
    return data


@size_cache()
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
                socket.location = (
                    x,
                    node.draw_bounds[3] + calculate_socket_offset_y(bpy_socket),
                )

    pairs = []
    for node, data in data_of.items():
        output = getattr(node, "paired_output", None)
        if output is not None:
            pairs.append((data, data_of[output]))
    tree.zones = find_zones(tree, pairs)

    return tree, binding
