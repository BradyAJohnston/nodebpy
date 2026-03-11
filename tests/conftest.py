from pathlib import Path

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import sockets as s

from .snapshots import TreeBuilderSnapshotExtension

CURRENT = Path(__file__).parent
BLEND_DIR = CURRENT / "blend_files"
JSON_DIR = CURRENT / "clippings"


@pytest.fixture(autouse=True, scope="function")
def clean_and_save(request):
    """Cleans the Blender file before each test and saves it after."""
    # Before each test: load a clean home file
    bpy.ops.wm.read_homefile(filepath=str(CURRENT / "test_startup.blend"))

    yield

    # After each test: save the current file to a location for potential inspection
    # we have to make sure the node trees are used somewhere or they will be purged on save

    # --- Geometry node trees: store via a modifier on the Cube ---
    geo_tree_names = [
        tree.name
        for tree in bpy.data.node_groups
        if tree.bl_idname == "GeometryNodeTree"
    ]

    if geo_tree_names:
        bpy.data.objects["Cube"].modifiers.clear()
        bpy.data.objects["Cube"].modifiers.new("StoreTrees", "NODES")
        mod: bpy.types.NodesModifier = bpy.data.objects["Cube"].modifiers["StoreTrees"]  # type: ignore
        with TreeBuilder("StoredTrees") as tree:
            with tree.inputs:
                ing = s.SocketGeometry()
            with tree.outputs:
                ong = s.SocketGeometry()

            for i, name in enumerate(geo_tree_names):
                node = g.Group()
                node.node.node_tree = bpy.data.node_groups[name]
                node.node.location = (0, 200 * i)

            if node.node.outputs and node.node.outputs[0].type == "GEOMETRY":  # type: ignore
                _ = node >> ong  # type: ignore
            else:
                _ = ing >> ong

        mod.node_group = tree.tree

    # --- Shader node trees: store via a material on the Cube ---
    shader_tree_names = [
        tree.name for tree in bpy.data.node_groups if tree.bl_idname == "ShaderNodeTree"
    ]

    if shader_tree_names:
        cube = bpy.data.objects["Cube"]
        mat = bpy.data.materials.new("StoreShaderTrees")
        mat.use_nodes = True
        cube.data.materials.append(mat)
        node_tree = mat.node_tree
        for i, name in enumerate(shader_tree_names):
            group_node = node_tree.nodes.new("ShaderNodeGroup")

            group_node.node_tree = bpy.data.node_groups[name]
            group_node.location = (0, 200 * i)

    # --- Compositor node trees: store via the scene compositor ---
    compositor_tree_names = [
        tree.name
        for tree in bpy.data.node_groups
        if tree.bl_idname == "CompositorNodeTree"
    ]

    if compositor_tree_names:
        with TreeBuilder.compositor("CompHoldingTree") as tree:
            for i, name in enumerate(compositor_tree_names):
                group = c.Group()
                group.node.node_tree = bpy.data.node_groups[name]
        bpy.context.scene.compositing_node_group = tree.tree

    # save a .blendfile for inspection with the current tests' nodes and also
    # named after the current test function
    name = request.node.name
    for key, value in (
        ("/", "divide"),
        ("+", "plus"),
        ("*", "multiply"),
        ("-", "subtract"),
    ):
        name = name.replace(key, value)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_DIR / f"{name}.blend"))


@pytest.fixture
def snapshot_tree(snapshot):
    """Fixture that provides tree snapshot functionality."""
    return snapshot.with_defaults(extension_class=TreeBuilderSnapshotExtension)
