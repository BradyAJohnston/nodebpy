# SPDX-License-Identifier: GPL-3.0-or-later
"""Mermaid diagram generation for node trees."""

from __future__ import annotations

_COLOR_CLASS_MAP = {
    "GEOMETRY": "geometry-node",
    "CONVERTER": "converter-node",
    "VECTOR": "vector-node",
    "TEXTURE": "texture-node",
    "SHADER": "shader-node",
    "INPUT": "input-node",
    "OUTPUT": "output-node",
}


def _node_css_class(node) -> str:
    color_tag = getattr(node, "color_tag", "GEOMETRY")
    return _COLOR_CLASS_MAP.get(color_tag, "default-node")


def _node_label(node) -> str:
    if (
        node.bl_idname == "GeometryNodeGroup"
        and hasattr(node, "node_tree")
        and node.node_tree
    ):
        label = node.node_tree.name.replace('"', "'")
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


def _sorted_nodes(node_tree, reroute_names: set) -> list:
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


def _trace_reroute(node_tree, node, socket):
    """Follow a reroute chain backward to the real source node and socket."""
    while node.bl_idname == "NodeReroute":
        input_links = [link for link in node_tree.links if link.to_node == node]
        if not input_links:
            return node, socket
        link = input_links[0]
        node = link.from_node
        socket = link.from_socket
    return node, socket


def to_mermaid(tree) -> str:
    """Generate a Mermaid diagram string from a node tree.

    Args:
        tree: TreeBuilder or Blender node tree

    Returns:
        Mermaid diagram as a fenced markdown code block
    """
    node_tree = tree.tree if hasattr(tree, "tree") else tree

    reroute_names = {n.name for n in node_tree.nodes if n.bl_idname == "NodeReroute"}
    sorted_nodes = _sorted_nodes(node_tree, reroute_names)

    lines = ["```{mermaid}", "graph LR"]

    node_map = {}
    for i, node in enumerate(sorted_nodes):
        node_id = f"N{i}"
        node_map[node.name] = node_id
        label = _node_label(node)
        css_class = _node_css_class(node)
        lines.append(f'    {node_id}("{label}"):::{css_class}')

    seen_edges = set()
    for link in node_tree.links:
        if link.to_node.name in reroute_names:
            continue

        from_node = link.from_node
        from_socket = link.from_socket

        if from_node.name in reroute_names:
            from_node, from_socket = _trace_reroute(node_tree, from_node, from_socket)

        if from_node.name not in node_map or link.to_node.name not in node_map:
            continue

        from_id = node_map[from_node.name]
        to_id = node_map[link.to_node.name]

        edge_key = (from_id, to_id, from_socket.name, link.to_socket.name)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        from_name = from_socket.name if hasattr(from_socket, "name") else ""
        to_name = link.to_socket.name if hasattr(link.to_socket, "name") else ""

        if from_name and to_name:
            lines.append(f'    {from_id} -->|"{from_name}->{to_name}"| {to_id}')
        else:
            lines.append(f"    {from_id} --> {to_id}")

    lines.append("```")

    return "\n".join(lines)


def save_diagram(filepath: str, tree) -> None:
    """Save a Mermaid diagram of the node tree to a markdown file.

    Args:
        filepath: Path to save the diagram
        tree: TreeBuilder or Blender node tree
    """
    node_tree = tree.tree if hasattr(tree, "tree") else tree

    with open(filepath, "w") as f:
        f.write(f"# Node Tree: {node_tree.name}\n\n")
        f.write(
            f"**{len(node_tree.nodes)} nodes, {len(node_tree.links)} connections**\n\n"
        )
        f.write(to_mermaid(tree))
