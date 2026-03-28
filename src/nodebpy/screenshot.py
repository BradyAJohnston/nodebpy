# SPDX-License-Identifier: GPL-3.0-or-later
"""Node tree diagrams and viewport rendering.

This module provides functions to generate Mermaid diagrams of node trees
and render viewport previews of geometry node output for documentation.
"""

from __future__ import annotations

import math
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import bpy

if TYPE_CHECKING:
    from .builder import TreeBuilder

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

    # Skip reroute nodes — trace through them when building links
    reroute_names = {n.name for n in node_tree.nodes if n.bl_idname == "NodeReroute"}

    # Enhanced sorting to better match visual flow in Blender
    # First, try to identify input/output nodes for special handling
    input_nodes = [n for n in node_tree.nodes if "GroupInput" in n.bl_idname]
    output_nodes = [n for n in node_tree.nodes if "GroupOutput" in n.bl_idname]
    regular_nodes = [
        n
        for n in node_tree.nodes
        if n not in input_nodes + output_nodes and n.name not in reroute_names
    ]

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

        # Use bl_label for the display name — it's the human-readable name Blender shows.
        # For node groups, show the group tree name instead of generic "Group".
        if (
            node.bl_idname == "GeometryNodeGroup"
            and hasattr(node, "node_tree")
            and node.node_tree
        ):
            node_type_clean = node.node_tree.name.replace('"', "'")
        else:
            node_type_clean = node.bl_label.replace('"', "'")

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

    # Trace through reroute chains to find the real source node/socket
    def trace_source(node, socket):
        """Follow reroute chains backward to find the real source."""
        while node.bl_idname == "NodeReroute":
            input_links = [l for l in node_tree.links if l.to_node == node]
            if not input_links:
                return node, socket
            link = input_links[0]
            node = link.from_node
            socket = link.from_socket
        return node, socket

    # Create connections with socket labels, skipping reroute intermediaries
    seen_edges = set()
    for link in node_tree.links:
        # Skip links that feed into reroutes — we trace from the output side
        if link.to_node.name in reroute_names:
            continue

        from_node = link.from_node
        from_socket = link.from_socket

        # If source is a reroute, trace back to the real source
        if from_node.name in reroute_names:
            from_node, from_socket = trace_source(from_node, from_socket)

        if from_node.name not in node_map or link.to_node.name not in node_map:
            continue

        from_node_id = node_map[from_node.name]
        to_node_id = node_map[link.to_node.name]

        # Deduplicate edges (multiple reroute paths can resolve to the same pair)
        edge_key = (from_node_id, to_node_id, from_socket.name, link.to_socket.name)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        from_socket_name = from_socket.name if hasattr(from_socket, "name") else ""
        to_socket_name = link.to_socket.name if hasattr(link.to_socket, "name") else ""

        if from_socket_name and to_socket_name:
            label = f"{from_socket_name}->{to_socket_name}"
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


def _ensure_camera() -> bpy.types.Object:
    """Get or create a camera and set it as the active scene camera."""
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.get("nodebpy_cam")
    if cam_data is None:
        cam_data = bpy.data.cameras.new("nodebpy_cam")
    cam_obj = bpy.data.objects.get("nodebpy_cam")
    if cam_obj is None:
        cam_obj = bpy.data.objects.new("nodebpy_cam", cam_data)
        scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    return cam_obj


def _frame_camera_to_object(
    cam_obj: bpy.types.Object,
    target: bpy.types.Object,
    padding: float = 1.4,
) -> None:
    """Position the camera to frame the target object's bounding box.

    Places the camera at a 30-degree elevation looking down at the object,
    pulled back far enough that the bounding box fits within the frame
    (with *padding* as a multiplier).
    """
    from mathutils import Matrix, Vector

    # Evaluate the object to get its final bounding box after modifiers
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = target.evaluated_get(depsgraph)

    bbox_corners = [target.matrix_world @ Vector(c) for c in eval_obj.bound_box]
    center = sum(bbox_corners, Vector()) / 8
    radius = max((c - center).length for c in bbox_corners)

    cam_data = cam_obj.data
    # Use a sensible default FOV if not set
    fov = cam_data.angle  # horizontal FOV in radians

    # Distance to fit the bounding sphere in the camera frustum
    aspect = (
        bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
    )
    if aspect < 1:
        fov_effective = 2 * math.atan(math.tan(fov / 2) * aspect)
    else:
        fov_effective = fov
    distance = (radius * padding) / math.tan(fov_effective / 2)

    # Camera at 30° elevation, 30° azimuth from front
    elevation = math.radians(30)
    azimuth = math.radians(30)

    offset = Vector(
        (
            distance * math.cos(elevation) * math.sin(azimuth),
            -distance * math.cos(elevation) * math.cos(azimuth),
            distance * math.sin(elevation),
        )
    )
    cam_obj.location = center + offset

    # Point at center
    direction = center - cam_obj.location
    rot_quat = direction.to_track_quat("-Z", "Y")
    cam_obj.rotation_euler = rot_quat.to_euler()


def _clear_scene(keep: bpy.types.Object | None = None) -> None:
    """Remove all objects and lights from the scene except *keep*."""
    for obj in list(bpy.data.objects):
        if obj is keep:
            continue
        bpy.data.objects.remove(obj, do_unlink=True)
    # Clean up orphaned meshes, lights, cameras left behind
    for block in list(bpy.data.meshes):
        if not block.users:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.lights):
        if not block.users:
            bpy.data.lights.remove(block)


def _setup_eevee(
    width: int = 720,
    height: int = 480,
    samples: int = 16,
) -> None:
    """Configure the scene for a fast EEVEE render."""
    scene = bpy.context.scene
    # "BLENDER_EEVEE_NEXT" in Blender 4.2+, "BLENDER_EEVEE" in older versions
    try:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = samples
    scene.render.film_transparent = True


def _get_ao_material() -> bpy.types.Material:
    """Get or create a simple Ambient Occlusion material.

    Uses an AO node piped into an Emission shader so the geometry is
    lit purely by occlusion with no dependency on scene lights.
    """
    mat = bpy.data.materials.get("nodebpy_ao")
    if mat is not None:
        return mat

    from .builder import TreeBuilder
    from .nodes.shader import AmbientOcclusion, Emission, MaterialOutput

    mat = bpy.data.materials.new("nodebpy_ao")
    mat.use_nodes = True
    # Clear the default Principled BSDF tree
    mat.node_tree.nodes.clear()

    with TreeBuilder(mat.node_tree):
        ao = AmbientOcclusion(distance=2)
        MaterialOutput(surface=Emission(color=ao.o_color ** 50))

    return mat


def _inject_ao_material(
    node_tree: bpy.types.NodeTree, material: bpy.types.Material
) -> None:
    """Insert a Set Material node before the Group Output in a geometry node tree.

    Finds geometry socket links going into the Group Output and splices a
    Set Material node in between. Skips if already injected.
    """
    output_node = None
    for node in node_tree.nodes:
        if "GroupOutput" in node.bl_idname:
            output_node = node
            break
    if output_node is None:
        return

    # Check if we already injected — look for our Set Material node
    for node in node_tree.nodes:
        if node.label == "_nodebpy_ao":
            return

    for input_socket in output_node.inputs:
        if input_socket.type != "GEOMETRY" or not input_socket.is_linked:
            continue

        link = input_socket.links[0]
        source_socket = link.from_socket

        # Create a Set Material node
        set_mat = node_tree.nodes.new("GeometryNodeSetMaterial")
        set_mat.label = "_nodebpy_ao"
        set_mat.inputs["Material"].default_value = material

        # Re-wire: source -> SetMaterial -> GroupOutput
        node_tree.links.remove(link)
        node_tree.links.new(source_socket, set_mat.inputs["Geometry"])
        node_tree.links.new(set_mat.outputs["Geometry"], input_socket)


def _remove_ao_material(node_tree: bpy.types.NodeTree) -> None:
    """Remove any injected AO Set Material nodes, restoring original links."""
    for node in list(node_tree.nodes):
        if node.label != "_nodebpy_ao":
            continue

        # Find the source feeding into this node's Geometry input
        geo_in = node.inputs["Geometry"]
        geo_out = node.outputs["Geometry"]

        source_socket = geo_in.links[0].from_socket if geo_in.is_linked else None
        target_sockets = (
            [l.to_socket for l in geo_out.links] if geo_out.is_linked else []
        )

        # Re-wire original connections
        if source_socket:
            for target in target_sockets:
                node_tree.links.new(source_socket, target)

        node_tree.nodes.remove(node)


def apply_tree(
    tree: TreeBuilder,
    obj: bpy.types.Object | None = None,
    modifier_name: str = "nodebpy",
) -> bpy.types.Object:
    """Apply a geometry node tree to an object as a modifier.

    If *obj* is ``None`` a new empty mesh object is created. Returns the object.
    """
    if obj is None:
        mesh = bpy.data.meshes.new("nodebpy_mesh")
        obj = bpy.data.objects.new("nodebpy_obj", mesh)
        bpy.context.scene.collection.objects.link(obj)

    bpy.context.view_layer.objects.active = obj

    node_tree = tree.tree if hasattr(tree, "tree") else tree
    mod = obj.modifiers.get(modifier_name)
    if mod is None:
        mod = obj.modifiers.new(name=modifier_name, type="NODES")
    mod.node_group = node_tree
    return obj


def render_preview(
    tree: TreeBuilder | None = None,
    obj: bpy.types.Object | None = None,
    filepath: str | Path | None = None,
    width: int = 720,
    height: int = 480,
    samples: int = 16,
    padding: float = 1.4,
) -> str:
    """Render a viewport preview of a geometry node tree.

    Either *tree* or *obj* must be provided. If *tree* is given it is applied
    to *obj* (or a new empty object) as a Geometry Nodes modifier. The camera
    is automatically framed to the object and a quick EEVEE render is saved.

    Args:
        tree: A :class:`TreeBuilder` to apply as a modifier.
        obj: An existing Blender object to render. If *tree* is also given
            the modifier is applied to this object.
        filepath: Where to save the PNG. Defaults to a temp file.
        width: Render width in pixels.
        height: Render height in pixels.
        samples: EEVEE render samples.
        padding: Camera framing padding multiplier.

    Returns:
        The absolute path to the rendered PNG image.
    """
    # Clear the scene before setting up the render
    _clear_scene(keep=obj)

    if tree is not None:
        # Inject a SetMaterial node with AO material before the Group Output
        ao_mat = _get_ao_material()
        node_tree = tree.tree if hasattr(tree, "tree") else tree
        _inject_ao_material(node_tree, ao_mat)

        obj = apply_tree(tree, obj)
    if obj is None:
        raise ValueError("Either tree or obj must be provided")

    _setup_eevee(width=width, height=height, samples=samples)
    cam = _ensure_camera()
    _frame_camera_to_object(cam, obj, padding=padding)

    if filepath is None:
        filepath = tempfile.mktemp(suffix=".png", prefix="nodebpy_render_")
    filepath = str(filepath)

    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

    # Clean up injected AO material node so the user's tree is unmodified
    if tree is not None:
        _remove_ao_material(node_tree)

    return filepath


def display_render(
    tree: TreeBuilder | None = None,
    obj: bpy.types.Object | None = None,
    filepath: str | Path | None = None,
    width: int = 720,
    height: int = 480,
    samples: int = 16,
    padding: float = 1.4,
) -> None:
    """Render a preview and display it inline in a Jupyter/Quarto notebook.

    Accepts the same arguments as :func:`render_preview`. The image is
    displayed using IPython's display machinery, which Quarto picks up
    automatically.
    """
    from IPython.display import Image, display

    path = render_preview(
        tree=tree,
        obj=obj,
        filepath=filepath,
        width=width,
        height=height,
        samples=samples,
        padding=padding,
    )
    display(Image(filename=path, width=width))
