# SPDX-License-Identifier: GPL-3.0-or-later
"""Programmatic node tree screenshot capture.

This module provides functions to capture screenshots of Blender node trees
without UI interaction. Screenshots can be returned as PIL Images or numpy arrays
for use in Jupyter notebooks or other contexts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass

# Mermaid diagram generation (no subprocess needed)

# Margin for node bounds to ensure sockets and links are included.
NODE_MARGIN = 30
# Node height isn't very accurate and needs more margin
NODE_EXTRA_HEIGHT = 30
# Margin for regions to hide unwanted UI parts (scrollbars, dividers, sidebar buttons).
REGION_MARGIN = 20
# Image output settings
IMAGE_FILE_FORMAT = "TIFF"
IMAGE_COLOR_MODE = "RGB"
IMAGE_COLOR_DEPTH = "8"
IMAGE_TIFF_CODEC = "DEFLATE"
IMAGE_EXTENSION = ".tif"


def generate_mermaid_diagram(tree) -> str:
    """
    Generate a Mermaid diagram from a node tree with color coding based on node types.

    Args:
        tree: TreeBuilder or GeometryNodeTree to create diagram for

    Returns:
        Mermaid diagram as markdown string with CSS styling

    Example:
        >>> from nodebpy import TreeBuilder
        >>> from nodebpy.screenshot import generate_mermaid_diagram
        >>> with TreeBuilder("MyTree") as tree:
        ...     # build your tree
        ...     pass
        >>> mermaid = generate_mermaid_diagram(tree)
        >>> print(mermaid)
    """
    # Get the actual node tree object
    if hasattr(tree, "tree"):
        node_tree = tree.tree
    else:
        node_tree = tree

    mermaid_lines = ["```{mermaid}", "graph LR"]

    # Define color mappings for different node types
    color_class_map = {
        "GEOMETRY": "geometry-node",
        "CONVERTER": "converter-node",
        "VECTOR": "vector-node",
        "TEXTURE": "texture-node",
        "SHADER": "shader-node",
        "INPUT": "input-node",
        "OUTPUT": "output-node",
    }

    # Enhanced sorting to better match visual flow in Blender
    # First, try to identify input/output nodes for special handling
    input_nodes = [n for n in node_tree.nodes if "GroupInput" in n.bl_idname]
    output_nodes = [n for n in node_tree.nodes if "GroupOutput" in n.bl_idname]
    regular_nodes = [n for n in node_tree.nodes if n not in input_nodes + output_nodes]

    # Sort regular nodes primarily by X position (left to right flow), then by Y position
    sorted_regular = sorted(
        regular_nodes, key=lambda n: (n.location[0], -n.location[1])
    )

    # Combine: inputs first, then regular nodes, then outputs
    sorted_nodes = input_nodes + sorted_regular + output_nodes

    # Create node definitions in vertical order
    node_map = {}
    for i, node in enumerate(sorted_nodes):
        node_id = f"N{i}"
        node_map[node.name] = node_id

        # Clean up the node type name for display - use just the type, not the full name
        node_type = (
            node.bl_idname.replace("GeometryNode", "")
            .replace("ShaderNode", "")
            .replace("FunctionNode", "")
        )
        node_type_clean = node_type.replace('"', "'")

        # Only show the most critical non-default values
        key_params = []

        # Get only the most important input parameters that differ from defaults
        for input_socket in node.inputs:
            if input_socket.is_linked:
                continue

            socket_name = input_socket.name

            if hasattr(input_socket, "default_value"):
                try:
                    value = input_socket.default_value

                    # Only show very specific important parameters
                    if socket_name.lower() in ["seed"]:
                        if isinstance(value, (int, float)) and value != 0:
                            key_params.append(f"seed:{int(value)}")
                    elif socket_name.lower() in ["scale"] and isinstance(
                        value, (int, float)
                    ):
                        if value != 1:
                            key_params.append(f"×{value:.1g}")
                    elif socket_name.lower() in ["offset"] and hasattr(
                        value, "__len__"
                    ):
                        if not all(v == 0 for v in value):
                            formatted = ",".join(f"{v:.1g}" for v in value)
                            key_params.append(f"+({formatted})")
                    elif hasattr(value, "__len__") and len(value) == 3:
                        # Show non-zero vectors compactly
                        if not all(v == 0 for v in value) and not all(
                            v == 1 for v in value
                        ):
                            formatted = ",".join(f"{v:.1g}" for v in value)
                            key_params.append(f"({formatted})")
                except Exception as e:
                    print(f"Error processing node: {e}")
                    pass

        # Build minimal node label
        node_label = node_type_clean
        if hasattr(node, "operation"):
            node_label += f"<br/><small>({node.operation})</small>"

        # Only add parameters if there are any significant ones
        if key_params:
            params_str = " ".join(key_params[:2])  # Max 2 parameters
            node_label += f"<br/><small>{params_str}</small>"

        # Escape quotes for Mermaid
        node_label = node_label.replace('"', "'")

        # Apply color class based on node color_tag
        color_tag = getattr(node, "color_tag", "GEOMETRY")
        css_class = color_class_map.get(color_tag, "default-node")

        mermaid_lines.append(f'    {node_id}("{node_label}"):::{css_class}')

    # Create connections with socket labels
    for link in node_tree.links:
        from_node_id = node_map[link.from_node.name]
        to_node_id = node_map[link.to_node.name]

        # Get socket names
        from_socket = link.from_socket.name if hasattr(link.from_socket, "name") else ""
        to_socket = link.to_socket.name if hasattr(link.to_socket, "name") else ""

        # Create socket label with full names
        if from_socket and to_socket:
            # Always show from -> to format with full socket names
            label = f"{from_socket}->{to_socket}"

            mermaid_lines.append(f'    {from_node_id} -->|"{label}"| {to_node_id}')
        else:
            mermaid_lines.append(f"    {from_node_id} --> {to_node_id}")

    # Add CSS styling for node colors (lighter tints for subtlety)
    # Mermaid doesn't support gradients, so using light tints as a compromise
    mermaid_lines.extend(
        [
            "",
            "    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px",
            "    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px",
            "    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px",
            "    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px",
            "    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px",
            "    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px",
            "    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px",
            "    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px",
        ]
    )

    # Close the mermaid block
    mermaid_lines.append("```")

    # Join into a single diagram
    return "\n".join(mermaid_lines)


def save_mermaid_diagram(filepath: str, tree, format: str = "md") -> None:
    """
    Save a Mermaid diagram of the node tree to a file.

    Args:
        filepath: Path to save the diagram
        tree: TreeBuilder or GeometryNodeTree to create diagram for
        format: Output format ('md' for markdown, 'mmd' for raw mermaid)

    Example:
        >>> from nodebpy.screenshot import save_mermaid_diagram
        >>> save_mermaid_diagram('/tmp/my_node_tree.md', tree=my_tree)
    """
    mermaid_diagram = generate_mermaid_diagram(tree)

    with open(filepath, "w") as f:
        if format.lower() == "md":
            # Write as full markdown
            tree_name = tree.tree.name if hasattr(tree, "tree") else "NodeTree"
            node_count = len(tree.tree.nodes) if hasattr(tree, "tree") else 0
            link_count = len(tree.tree.links) if hasattr(tree, "tree") else 0

            f.write(f"# Node Tree: {tree_name}\n\n")
            f.write(f"**{node_count} nodes, {link_count} connections**\n\n")
            f.write(mermaid_diagram)
        else:
            # Write raw mermaid (remove markdown wrapper)
            lines = mermaid_diagram.split("\n")
            mermaid_content = "\n".join(lines[1:-1])  # Remove ```mermaid and ``` lines
            f.write(mermaid_content)
