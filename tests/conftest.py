import pytest
from pathlib import Path
import bpy
from nodebpy import TreeBuilder, nodes, sockets

BLEND_DIR = Path(__file__).parent / "blend_files"

@pytest.fixture(autouse=True, scope="function")
def clean_and_save(request):
    """Cleans the Blender file before each test and saves it after."""
    # Before each test: load a clean home file
    bpy.ops.wm.read_homefile()
    
    yield
    
    # After each test: save the current file to a temporary location
    tree_names = [tree.name for tree in bpy.data.node_groups if tree.bl_idname == "GeometryNodeTree"]
    
    bpy.data.objects['Cube'].modifiers.clear()
    bpy.data.objects['Cube'].modifiers.new("StoreTrees", "NODES")
    mod: bpy.types.NodesModifier = bpy.data.objects['Cube'].modifiers['StoreTrees'] # type: ignore
    with TreeBuilder("StoredTrees") as tree:
        for i, name in enumerate(tree_names):
            n = nodes.Group()
            n.node.node_tree = bpy.data.node_groups[name] # type: ignore
            n.node.location = (0, 200 * i)
    
    mod.node_group = tree.tree

    # save a .blendfile for inspection with the current tests' nodes and also
    # named after the current test function

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_DIR / f"{request.node.name}.blend"))
    