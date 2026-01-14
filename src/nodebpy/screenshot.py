# SPDX-License-Identifier: GPL-3.0-or-later
"""Programmatic node tree screenshot capture.

This module provides functions to capture screenshots of Blender node trees
without UI interaction. Screenshots can be returned as PIL Images or numpy arrays
for use in Jupyter notebooks or other contexts.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Literal

import bpy
import numpy as np
from mathutils import Vector

if TYPE_CHECKING:
    from PIL import Image as PILImage

# Import subprocess-based screenshot for headless environments
from .screenshot_subprocess import screenshot_node_tree_subprocess

# Margin for node bounds to ensure sockets and links are included.
NODE_MARGIN = 30
# Node height isn't very accurate and needs more margin
NODE_EXTRA_HEIGHT = 30
# Margin for regions to hide unwanted UI parts (scrollbars, dividers, sidebar buttons).
REGION_MARGIN = 20
# Image output settings
IMAGE_FILE_FORMAT = 'TIFF'
IMAGE_COLOR_MODE = 'RGB'
IMAGE_COLOR_DEPTH = '8'
IMAGE_TIFF_CODEC = 'DEFLATE'
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
        node_view_min = Vector((
            node.location_absolute[0],
            node.location_absolute[1] - node.height - NODE_EXTRA_HEIGHT
        )) * ui_scale
        node_view_max = Vector((
            node.location_absolute[0] + node.width,
            node.location_absolute[1]
        )) * ui_scale

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
        usable_region_max = Vector((region.width - REGION_MARGIN, region.height - REGION_MARGIN))
        self.tile_margin = REGION_MARGIN
        self.tile_size = (
            int(usable_region_max.x - usable_region_min.x),
            int(usable_region_max.y - usable_region_min.y)
        )

        self.orig_view_min = Vector(v2d.region_to_view(usable_region_min.x, usable_region_min.y))
        self.orig_view_max = Vector(v2d.region_to_view(usable_region_max.x, usable_region_max.y))
        self.image_num = (
            int(self.nodes_size.x / self.view_size.x) + 1,
            int(self.nodes_size.y / self.view_size.y) + 1
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

    def tile_boxes(self, tile_index: tuple[int, int]) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
        """Calculate input and output boxes for a tile."""
        in_start = (self.tile_margin, self.tile_margin)
        out_start = (tile_index[0] * self.tile_size[0], tile_index[1] * self.tile_size[1])
        tile_size_clamped = (
            min(out_start[0] + self.tile_size[0], self.full_size[0]) - out_start[0],
            min(out_start[1] + self.tile_size[1], self.full_size[1]) - out_start[1]
        )
        in_end = (in_start[0] + tile_size_clamped[0], in_start[1] + tile_size_clamped[1])
        out_end = (out_start[0] + tile_size_clamped[0], out_start[1] + tile_size_clamped[1])
        return (*in_start, *in_end), (*out_start, *out_end)


def find_node_editor_window_region(context):
    """Find the window region in a node editor area."""
    for region in context.area.regions:
        if region.type == 'WINDOW':
            return region
    return None


def capture_tiles(context, region, tile_info: TileInfo, area=None, window=None, screen=None) -> dict[tuple[int, int], str]:
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
                f"node_tree_screenshot_tile_{i}_{j}{render_settings.file_extension}"
            )
            with context.temp_override(**context_override):
                bpy.ops.screen.screenshot_area(filepath=tmp_filepath)
            image_files[(i, j)] = tmp_filepath

    # Reset view.
    pan_to_view(tile_info.orig_view_min)

    return image_files


def stitch_tiles_numpy(context, tile_info: TileInfo, image_files: dict[tuple[int, int], str]) -> np.ndarray:
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
    pixels_out = np.zeros((tile_info.full_size[1], tile_info.full_size[0], 4), dtype=float)

    for tile_index, tile_filepath in image_files.items():
        tile_image = context.blend_data.images.load(tile_filepath)
        assert tile_image.channels == 4, "Tile images should have 4 channels"

        in_box, out_box = tile_info.tile_boxes(tile_index)

        pixels_flat = np.fromiter(
            tile_image.pixels,
            dtype=float,
            count=tile_image.size[0] * tile_image.size[1] * 4
        )
        pixels_in = np.reshape(pixels_flat, (tile_image.size[1], tile_image.size[0], 4))
        pixels_out[out_box[1]:out_box[3], out_box[0]:out_box[2], :] = \
            pixels_in[in_box[1]:in_box[3], in_box[0]:in_box[2], :]

        context.blend_data.images.remove(tile_image)

    return pixels_out


def stitch_tiles_pil(context, tile_info: TileInfo, image_files: dict[tuple[int, int], str]) -> PILImage.Image:
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
            pil_in_box = (in_box[0], tile_image.height - in_box[3], in_box[2], tile_image.height - in_box[1])
            pil_out_box = (out_box[0], full_image.height - out_box[3], out_box[2], full_image.height - out_box[1])
            tile_cropped = tile_image.crop(pil_in_box)
            full_image.paste(tile_cropped, pil_out_box)

    return full_image


def screenshot_node_tree(
    tree=None,
    context=None,
    return_format: Literal['pil', 'numpy'] = 'pil',
    cleanup: bool = True,
    use_subprocess: bool | None = None,
    blender_executable: str | None = None,
    timeout: float = 30.0
) -> PILImage.Image | np.ndarray:
    """
    Create a screenshot of the active node tree.

    This function automatically detects whether a GUI is available and uses
    the appropriate method:
    - If GUI is available: Direct screenshot capture (fast)
    - If no GUI (headless/Jupyter): Launch Blender subprocess (slower but works everywhere)

    Args:
        tree: TreeBuilder or GeometryNodeTree to screenshot (uses active tree if None)
        context: Blender context (uses bpy.context if None)
        return_format: 'pil' for PIL Image, 'numpy' for numpy array
        cleanup: Whether to delete temporary tile files after stitching
        use_subprocess: Force subprocess mode (auto-detect if None)
        blender_executable: Path to Blender for subprocess mode (auto-detect if None)
        timeout: Subprocess timeout in seconds (default 30)

    Returns:
        PIL Image or numpy array of the node tree screenshot

    Raises:
        RuntimeError: If screenshot capture fails
        ValueError: If return_format is invalid

    Example:
        >>> import bpy
        >>> from nodebpy.screenshot import screenshot_node_tree
        >>>
        >>> # In a Jupyter notebook (will use subprocess automatically):
        >>> from IPython.display import display
        >>> img = screenshot_node_tree(tree=my_tree, return_format='pil')
        >>> display(img)
    """
    if context is None:
        context = bpy.context

    if return_format not in ('pil', 'numpy'):
        raise ValueError(f"return_format must be 'pil' or 'numpy', got {return_format!r}")

    # Auto-detect if we should use subprocess
    if use_subprocess is None:
        # Use subprocess if no GUI windows available
        use_subprocess = not context.window_manager.windows

    # Use subprocess approach if needed
    if use_subprocess:
        if tree is None:
            raise ValueError("tree parameter is required when using subprocess mode")
        return screenshot_node_tree_subprocess(
            tree=tree,
            return_format=return_format,
            blender_executable=blender_executable,
            timeout=timeout
        )

    # Get the actual node tree object
    if tree is not None:
        # Handle TreeBuilder wrapper
        if hasattr(tree, 'tree'):
            node_tree = tree.tree
        else:
            node_tree = tree
    else:
        node_tree = None

    # Find or create a node editor area
    area = None
    original_area_type = None
    context_dict = None
    window = None

    # First, try to find an existing node editor
    for win in context.window_manager.windows:
        for a in win.screen.areas:
            if a.type == 'NODE_EDITOR':
                area = a
                window = win
                context_dict = context.copy()
                context_dict['window'] = window
                context_dict['screen'] = window.screen
                context_dict['area'] = area
                break
        if area and area.type == 'NODE_EDITOR':
            break

    # If no node editor found, temporarily convert an area
    if not area or area.type != 'NODE_EDITOR':
        # Use the first available window and area
        if context.window_manager.windows:
            window = context.window_manager.windows[0]
            if window.screen.areas:
                area = window.screen.areas[0]
                original_area_type = area.type
                area.type = 'NODE_EDITOR'
                context_dict = context.copy()
                context_dict['window'] = window
                context_dict['screen'] = window.screen
                context_dict['area'] = area
            else:
                raise RuntimeError("No areas available in window")
        else:
            raise RuntimeError("No windows available to create node editor")

    try:
        # Set the tree in the node editor if provided
        if node_tree is not None:
            space = area.spaces.active
            space.tree_type = 'GeometryNodeTree'
            space.node_tree = node_tree

        # Find the window region using the area directly
        region = None
        for r in area.regions:
            if r.type == 'WINDOW':
                region = r
                break
        if not region:
            raise RuntimeError("No node editor window region found")

        # Build proper context override with all necessary fields
        context_override = context.copy()
        context_override["region"] = region
        context_override["area"] = area
        context_override["window"] = window
        context_override["screen"] = window.screen if window else None

        # Use a properly structured context for operations
        # Create a namespace object that mimics context behavior
        class ContextNamespace:
            def __init__(self, ctx_dict, base_context):
                # Set attributes from dict
                for key, value in ctx_dict.items():
                    setattr(self, key, value)
                # Add essential context properties from base context
                self.scene = base_context.scene
                self.preferences = base_context.preferences
                self.blend_data = base_context.blend_data
                self.window_manager = base_context.window_manager
                # Get space_data from the area
                self.space_data = area.spaces.active

        ctx_ns = ContextNamespace(context_override, context)

        with clean_node_window_region(ctx_ns):
            # Reset view to ensure consistent captures
            with context.temp_override(**context_override):
                bpy.ops.view2d.reset()

            tile_info = TileInfo(ctx_ns, region)
            # Pass the original context to capture_tiles so it can use temp_override
            screen = window.screen if window else None
            image_files = capture_tiles(context, region, tile_info, area=area, window=window, screen=screen)

        try:
            if return_format == 'pil':
                result = stitch_tiles_pil(context, tile_info, image_files)
            else:  # numpy
                result = stitch_tiles_numpy(context, tile_info, image_files)

            return result
        finally:
            if cleanup:
                for filepath in image_files.values():
                    if os.path.exists(filepath):
                        os.remove(filepath)
    finally:
        # Restore original area type if we changed it
        if original_area_type is not None and area is not None:
            area.type = original_area_type


def save_node_tree_screenshot(
    filepath: str,
    tree=None,
    context=None,
    format: str = 'PNG',
    use_subprocess: bool | None = None,
    blender_executable: str | None = None,
    timeout: float = 30.0
) -> None:
    """
    Save a screenshot of the active node tree to a file.

    Args:
        filepath: Path to save the screenshot
        tree: TreeBuilder or GeometryNodeTree to screenshot (uses active tree if None)
        context: Blender context (uses bpy.context if None)
        format: Image format ('TIFF', 'PNG', 'JPEG', etc.)
        use_subprocess: Force subprocess mode (auto-detect if None)
        blender_executable: Path to Blender for subprocess mode
        timeout: Subprocess timeout in seconds

    Example:
        >>> from nodebpy.screenshot import save_node_tree_screenshot
        >>> save_node_tree_screenshot('/tmp/my_node_tree.png', tree=my_tree, format='PNG')
    """
    # If using subprocess and format matches, we can save directly
    if context is None:
        context = bpy.context

    if use_subprocess is None:
        use_subprocess = not context.window_manager.windows

    if use_subprocess and filepath.lower().endswith('.png'):
        # Use subprocess directly to save to the target file
        screenshot_node_tree_subprocess(
            tree=tree,
            output_path=filepath,
            return_format='path',
            blender_executable=blender_executable,
            timeout=timeout
        )
    else:
        # Get image and save
        img = screenshot_node_tree(
            tree=tree,
            context=context,
            return_format='pil',
            use_subprocess=use_subprocess,
            blender_executable=blender_executable,
            timeout=timeout
        )
        img.save(filepath, format)


class NodeTreeDisplay:
    """
    Wrapper to enable automatic display of node trees in Jupyter notebooks.

    This class wraps a TreeBuilder and automatically displays a screenshot
    when the object is displayed in a Jupyter notebook.

    Example:
        >>> from nodebpy import TreeBuilder
        >>> from nodebpy.screenshot import NodeTreeDisplay
        >>>
        >>> tree = TreeBuilder("MyTree")
        >>> display_tree = NodeTreeDisplay(tree)
        >>> display_tree  # In Jupyter, this will show the screenshot automatically
    """

    def __init__(self, tree_builder, blender_executable=None, timeout=30.0):
        """
        Initialize with a TreeBuilder instance.

        Args:
            tree_builder: A TreeBuilder instance
            blender_executable: Optional path to Blender executable (auto-detected if None)
            timeout: Subprocess timeout in seconds (default 30)
        """
        self.tree_builder = tree_builder
        self.blender_executable = blender_executable
        self.timeout = timeout

    def _repr_png_(self) -> bytes | None:
        """
        Return PNG representation for Jupyter notebook display.

        This special method is called by Jupyter to display the object as an image.

        Uses subprocess mode by default since Jupyter notebooks typically don't
        have proper GUI context for direct screenshots.
        """
        import io
        try:
            # Force subprocess mode in Jupyter since direct screenshots usually don't work
            img = screenshot_node_tree(
                tree=self.tree_builder,
                return_format='pil',
                use_subprocess=True,  # Force subprocess mode for Jupyter
                blender_executable=self.blender_executable,
                timeout=self.timeout
            )
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return buf.getvalue()
        except Exception as e:
            # Screenshot failed - return None to let Jupyter use text representation
            print(f"Screenshot failed: {e}")
            print("Check that Blender is installed and accessible.")
            return None

    def __repr__(self) -> str:
        """Text representation showing tree info."""
        tree_name = self.tree_builder.tree.name if hasattr(self.tree_builder, 'tree') else 'Unknown'
        node_count = len(self.tree_builder.nodes) if hasattr(self.tree_builder, 'nodes') else 0
        return f"<NodeTreeDisplay: '{tree_name}' with {node_count} nodes>"

    def __enter__(self):
        """Support context manager protocol."""
        return self.tree_builder.__enter__()

    def __exit__(self, *args):
        """Support context manager protocol."""
        return self.tree_builder.__exit__(*args)

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped TreeBuilder."""
        return getattr(self.tree_builder, name)
