# SPDX-License-Identifier: GPL-3.0-or-later
"""Programmatic node tree screenshot capture.

This module provides functions to capture screenshots of Blender node trees
without UI interaction. Screenshots can be returned as PIL Images or numpy arrays
for use in Jupyter notebooks or other contexts.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING

import bpy
import numpy as np
from mathutils import Vector

if TYPE_CHECKING:
    from PIL import Image as PILImage

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


def compute_node_bounds(context, margin: float) -> tuple[Vector, Vector]:
    """
    Compute the extent (in View2D space) of all nodes in a node tree.

    Args:
        context: Blender context
        margin: Margin to add around nodes

    Returns:
        Tuple of (min, max) vectors of the node bounds
    """
    ui_scale = context.preferences.system.ui_scale
    space = context.space_data
    node_tree = space.edit_tree
    if not node_tree:
        return Vector((0.0, 0.0)), Vector((0.0, 0.0))

    bmin = Vector((1.0e8, 1.0e8))
    bmax = Vector((-1.0e8, -1.0e8))
    for node in node_tree.nodes:
        node_view_min = (
            Vector(
                (
                    node.location_absolute[0],
                    node.location_absolute[1] - node.height - NODE_EXTRA_HEIGHT,
                )
            )
            * ui_scale
        )
        node_view_max = (
            Vector((node.location_absolute[0] + node.width, node.location_absolute[1]))
            * ui_scale
        )

        bmin = Vector((min(bmin.x, node_view_min.x), min(bmin.y, node_view_min.y)))
        bmax = Vector((max(bmax.x, node_view_max.x), max(bmax.y, node_view_max.y)))

    return bmin - Vector((margin, margin)), bmax + Vector((margin, margin))


@contextmanager
def clean_node_window_region(context):
    """
    Creates a safe context for executing screenshots
    and ensures the region properties are reset afterwards.
    """
    try:
        # Remember image format settings
        img_settings = context.scene.render.image_settings
        file_format = img_settings.file_format
        color_mode = img_settings.color_mode
        color_depth = img_settings.color_depth
        tiff_codec = img_settings.tiff_codec

        # Set image format for screenshots
        img_settings.file_format = IMAGE_FILE_FORMAT
        img_settings.color_mode = IMAGE_COLOR_MODE
        img_settings.color_depth = IMAGE_COLOR_DEPTH
        img_settings.tiff_codec = IMAGE_TIFF_CODEC

        space = context.space_data
        show_region_header = space.show_region_header
        show_context_path = space.overlay.show_context_path

        space.show_region_header = False
        space.overlay.show_context_path = False

        yield context

    finally:
        img_settings.file_format = file_format
        img_settings.color_mode = color_mode
        img_settings.color_depth = color_depth
        img_settings.tiff_codec = tiff_codec

        space.show_region_header = show_region_header
        space.overlay.show_context_path = show_context_path


class TileInfo:
    """Information about tiling strategy for large node trees."""

    def __init__(self, context, region):
        v2d = region.view2d

        self.nodes_min, self.nodes_max = compute_node_bounds(context, NODE_MARGIN)

        # Min/Max points of the region considered usable for screenshots.
        # The margin excludes some bits that can't be hidden (dividers, scrollbars, sidebar buttons).
        usable_region_min = Vector((REGION_MARGIN, REGION_MARGIN))
        usable_region_max = Vector(
            (region.width - REGION_MARGIN, region.height - REGION_MARGIN)
        )
        self.tile_margin = REGION_MARGIN
        self.tile_size = (
            int(usable_region_max.x - usable_region_min.x),
            int(usable_region_max.y - usable_region_min.y),
        )

        self.orig_view_min = Vector(
            v2d.region_to_view(usable_region_min.x, usable_region_min.y)
        )
        self.orig_view_max = Vector(
            v2d.region_to_view(usable_region_max.x, usable_region_max.y)
        )
        self.image_num = (
            int(self.nodes_size.x / self.view_size.x) + 1,
            int(self.nodes_size.y / self.view_size.y) + 1,
        )

    @property
    def view_size(self) -> Vector:
        return self.orig_view_max - self.orig_view_min

    @property
    def nodes_size(self) -> Vector:
        return self.nodes_max - self.nodes_min

    @property
    def full_size(self) -> tuple[int, int]:
        return (int(self.nodes_size[0]), int(self.nodes_size[1]))

    @property
    def tile_num(self) -> int:
        return self.image_num[0] * self.image_num[1]

    def tile_boxes(
        self, tile_index: tuple[int, int]
    ) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
        """Calculate input and output boxes for a tile."""
        in_start = (self.tile_margin, self.tile_margin)
        out_start = (
            tile_index[0] * self.tile_size[0],
            tile_index[1] * self.tile_size[1],
        )
        tile_size_clamped = (
            min(out_start[0] + self.tile_size[0], self.full_size[0]) - out_start[0],
            min(out_start[1] + self.tile_size[1], self.full_size[1]) - out_start[1],
        )
        in_end = (
            in_start[0] + tile_size_clamped[0],
            in_start[1] + tile_size_clamped[1],
        )
        out_end = (
            out_start[0] + tile_size_clamped[0],
            out_start[1] + tile_size_clamped[1],
        )
        return (*in_start, *in_end), (*out_start, *out_end)


def find_node_editor_window_region(context):
    """Find the window region in a node editor area."""
    for region in context.area.regions:
        if region.type == "WINDOW":
            return region
    return None


def capture_tiles(
    context, region, tile_info: TileInfo, area=None, window=None, screen=None
) -> dict[tuple[int, int], str]:
    """
    Capture individual screenshot tiles of the node tree.

    Args:
        context: Blender context
        region: Node editor window region
        tile_info: Tiling information
        area: Node editor area (optional, extracted from context if None)
        window: Window context (optional, extracted from context if None)
        screen: Screen context (optional, extracted from context if None)

    Returns:
        Dictionary mapping tile indices to temporary file paths
    """
    context_override = context.copy()
    context_override["region"] = region
    if area is not None:
        context_override["area"] = area
    if window is not None:
        context_override["window"] = window
    if screen is not None:
        context_override["screen"] = screen
    render_settings = context.scene.render

    # View2D only supports relative panning, this provides a "goto" function.
    current_view_min = tile_info.orig_view_min

    def pan_to_view(view_min):
        nonlocal current_view_min
        delta = view_min - current_view_min
        with context.temp_override(**context_override):
            bpy.ops.view2d.pan(deltax=int(delta.x), deltay=int(delta.y))
        current_view_min = view_min

    image_files = {}
    for i in range(tile_info.image_num[0]):
        for j in range(tile_info.image_num[1]):
            pan_to_view(tile_info.nodes_min + Vector((i, j)) * tile_info.view_size)

            tmp_filepath = os.path.join(
                bpy.app.tempdir,
                f"node_tree_screenshot_tile_{i}_{j}{render_settings.file_extension}",
            )
            with context.temp_override(**context_override):
                bpy.ops.screen.screenshot_area(filepath=tmp_filepath)
            image_files[(i, j)] = tmp_filepath

    # Reset view.
    pan_to_view(tile_info.orig_view_min)

    return image_files


def stitch_tiles_numpy(
    context, tile_info: TileInfo, image_files: dict[tuple[int, int], str]
) -> np.ndarray:
    """
    Stitch tiles into a single numpy array.

    Args:
        context: Blender context
        tile_info: Tiling information
        image_files: Dictionary of tile files

    Returns:
        Numpy array with shape (height, width, 4) containing RGBA data
    """
    if not image_files:
        raise ValueError("No image files to stitch")

    # NOTE: NumPy pixel arrays are declared with shape (HEIGHT, WIDTH, CHANNELS)
    pixels_out = np.zeros(
        (tile_info.full_size[1], tile_info.full_size[0], 4), dtype=float
    )

    for tile_index, tile_filepath in image_files.items():
        tile_image = context.blend_data.images.load(tile_filepath)
        assert tile_image.channels == 4, "Tile images should have 4 channels"

        in_box, out_box = tile_info.tile_boxes(tile_index)

        pixels_flat = np.fromiter(
            tile_image.pixels,
            dtype=float,
            count=tile_image.size[0] * tile_image.size[1] * 4,
        )
        pixels_in = np.reshape(pixels_flat, (tile_image.size[1], tile_image.size[0], 4))
        pixels_out[out_box[1] : out_box[3], out_box[0] : out_box[2], :] = pixels_in[
            in_box[1] : in_box[3], in_box[0] : in_box[2], :
        ]

        context.blend_data.images.remove(tile_image)

    return pixels_out


def stitch_tiles_pil(
    context, tile_info: TileInfo, image_files: dict[tuple[int, int], str]
) -> PILImage.Image:
    """
    Stitch tiles into a single PIL Image.

    Args:
        context: Blender context
        tile_info: Tiling information
        image_files: Dictionary of tile files

    Returns:
        PIL Image object
    """
    from PIL import Image

    if not image_files:
        raise ValueError("No image files to stitch")

    full_image = Image.new("RGB", tile_info.full_size)

    for tile_index, tile_filepath in image_files.items():
        with Image.open(tile_filepath) as tile_image:
            in_box, out_box = tile_info.tile_boxes(tile_index)

            # Note: Pillow library uses upper-left corner as (0, 0), subtract Y coordinate from height!
            pil_in_box = (
                in_box[0],
                tile_image.height - in_box[3],
                in_box[2],
                tile_image.height - in_box[1],
            )
            pil_out_box = (
                out_box[0],
                full_image.height - out_box[3],
                out_box[2],
                full_image.height - out_box[1],
            )
            tile_cropped = tile_image.crop(pil_in_box)
            full_image.paste(tile_cropped, pil_out_box)

    return full_image


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
            # Always show from >> to format with full socket names
            label = f"{from_socket}>>{to_socket}"

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
