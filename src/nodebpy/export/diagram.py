# SPDX-License-Identifier: GPL-3.0-or-later
"""Mermaid diagram generation for node trees."""

from __future__ import annotations

import bpy
from bpy.types import Node, NodeTree

_COLOR_CLASS_MAP = {
    "GEOMETRY": "geometry-node",
    "CONVERTER": "converter-node",
    "VECTOR": "vector-node",
    "TEXTURE": "texture-node",
    "SHADER": "shader-node",
    "INPUT": "input-node",
    "OUTPUT": "output-node",
}


def _node_css_class(node: Node) -> str:
    color_tag = getattr(node, "color_tag", "GEOMETRY")
    return _COLOR_CLASS_MAP.get(color_tag, "default-node")


def _node_label(node: Node) -> str:
    node_tree = getattr(node, "node_tree", None)
    if isinstance(node_tree, bpy.types.NodeTree):
        label = node_tree.name.replace('"', "'")
    else:
        label = node.bl_label.replace('"', "'")

    if hasattr(node, "operation"):
        label += f"<br/><small>({node.operation})</small>"

    key_params = []
    for socket in node.inputs:
        if socket.is_linked or not hasattr(socket, "default_value"):
            continue
        name = socket.name.lower()
        try:
            value = socket.default_value
            if name == "seed":
                if isinstance(value, (int, float)) and value != 0:
                    key_params.append(f"seed:{int(value)}")
            elif name == "scale" and isinstance(value, (int, float)):
                if value != 1:
                    key_params.append(f"×{value:.1g}")
            elif name == "offset" and hasattr(value, "__len__"):
                if not all(v == 0 for v in value):
                    key_params.append(f"+({','.join(f'{v:.1g}' for v in value)})")
            elif hasattr(value, "__len__") and len(value) == 3:
                if not all(v == 0 for v in value) and not all(v == 1 for v in value):
                    key_params.append(f"({','.join(f'{v:.1g}' for v in value)})")
        except Exception:
            pass

    if key_params:
        label += f"<br/><small>{' '.join(key_params[:2])}</small>"

    return label.replace('"', "'")


def _sorted_nodes(node_tree: NodeTree, reroute_names: set) -> list[Node]:
    input_nodes = [n for n in node_tree.nodes if "GroupInput" in n.bl_idname]
    output_nodes = [n for n in node_tree.nodes if "GroupOutput" in n.bl_idname]
    regular_nodes = [
        n
        for n in node_tree.nodes
        if n not in input_nodes + output_nodes and n.name not in reroute_names
    ]
    sorted_regular = sorted(
        regular_nodes, key=lambda n: (n.location[0], -n.location[1])
    )
    return input_nodes + sorted_regular + output_nodes


def to_mermaid(tree, fenced=True) -> str:
    """Generate a Mermaid diagram string from a node tree.

    Arguments
    ---------
        tree:
            TreeBuilder or Blender node tree
        fenced:
            Whether to wrap the output in a fenced code block

    Returns
    -------
        A string containing the Mermaid diagram as a possibly fenced markdown code block
    """
    node_tree = tree.tree if hasattr(tree, "tree") else tree

    reroute_names = {n.name for n in node_tree.nodes if n.bl_idname == "NodeReroute"}
    sorted_nodes = _sorted_nodes(node_tree, reroute_names)

    lines = ["graph LR"]

    node_map: dict[str, str] = {}

    # Assign a stable id to every non-frame node up front so edges resolve
    # regardless of how nodes are nested inside frames.
    for i, node in enumerate(n for n in sorted_nodes if n.bl_idname != "NodeFrame"):
        node_map[node.name] = f"N{i}"

    # A NodeFrame is itself a node; its members point back at it via
    # `node.parent`. Group children by their parent frame and collect the
    # top-level (unparented) nodes to start rendering from.
    frame_ids: dict[str, str] = {
        node.name: f"F{i}"
        for i, node in enumerate(n for n in sorted_nodes if n.bl_idname == "NodeFrame")
    }

    children: dict[str, list[Node]] = {}
    roots: list[Node] = []
    for node in sorted_nodes:
        if node.parent is not None:
            children.setdefault(node.parent.name, []).append(node)
        else:
            roots.append(node)

    def _emit(node: Node, indent: str) -> None:
        if node.bl_idname == "NodeFrame":
            title = (node.label or node.name).replace('"', "'")
            lines.append(f'{indent}subgraph {frame_ids[node.name]}["{title}"]')
            for child in children.get(node.name, []):
                _emit(child, indent + "    ")
            lines.append(f"{indent}end")
        else:
            label = _node_label(node)
            css_class = _node_css_class(node)
            lines.append(f'{indent}{node_map[node.name]}("{label}"):::{css_class}')

    for node in roots:
        _emit(node, "    ")

    # Effective links collapse reroute chains and come in canonical
    # (structural) order, so the diagram never depends on link insertion
    # order.
    from .codegen import _effective_links

    seen_edges = set()
    for link in _effective_links(node_tree):
        if link.from_node.name not in node_map or link.to_node.name not in node_map:
            continue

        from_id = node_map[link.from_node.name]
        to_id = node_map[link.to_node.name]

        edge_key = (from_id, to_id, link.from_socket.name, link.to_socket.name)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        lines.append(
            f'    {from_id} -->|"{link.from_socket.name}->{link.to_socket.name}"| {to_id}'
        )

    pre = ["```{mermaid}"] if fenced else []
    post = ["```"] if fenced else []

    return "\n".join(pre + lines + post)
