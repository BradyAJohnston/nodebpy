from pathlib import Path

import bpy
import pytest

from nodebpy import TreeBuilder, sockets as s, nodes as n

from .snapshots import TreeBuilderSnapshotExtension

BLEND_DIR = Path(__file__).parent / "blend_files"
JSON_DIR = Path(__file__).parent / "clippings"


@pytest.fixture(autouse=True, scope="function")
def clean_and_save(request):
    """Cleans the Blender file before each test and saves it after."""
    # Before each test: load a clean home file
    bpy.ops.wm.read_homefile()

    yield

    # After each test: save the current file to a location for potential inspection
    # we have to make sure the node trees are used somewhere or they will be purged on save
    tree_names = [
        tree.name
        for tree in bpy.data.node_groups
        if tree.bl_idname == "GeometryNodeTree"
    ]

    bpy.data.objects["Cube"].modifiers.clear()
    bpy.data.objects["Cube"].modifiers.new("StoreTrees", "NODES")
    mod: bpy.types.NodesModifier = bpy.data.objects["Cube"].modifiers["StoreTrees"]  # type: ignore
    with TreeBuilder("StoredTrees") as tree:
        with tree.inputs:
            ing = s.SocketGeometry()
        with tree.outputs:
            ong = s.SocketGeometry()

        _ = ing >> ong

        for i, name in enumerate(tree_names):
            node = n.Group(name)
            node.node.location = (0, 200 * i)

    mod.node_group = tree.tree

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
