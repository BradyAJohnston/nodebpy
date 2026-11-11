import re
import sys
from pathlib import Path

import bpy
import pytest

# Importing bpy puts Blender's extensions site-packages ahead of the repo on
# sys.path; if nodebpy is installed there (e.g. as a MolecularNodes wheel) it
# would shadow the code under test. Force the repo's src back to the front.
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nodebpy import TreeBuilder, shader
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy.builder._utils import NodeUnavailableError, _older_blender
from nodebpy.nodes._blender import GENERATED_FOR

# The node classes are generated from one Blender; the suite also runs on the
# one before it. There a test using a node that Blender lacks is skipped, and
# one marked ``generated_blender`` (it tests that Blender's behaviour) too.
OLDER_BLENDER = _older_blender()
_GENERATED = ".".join(map(str, GENERATED_FOR))


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "generated_blender: tests behaviour of the Blender the node classes are "
        "generated from; skipped on an older one",
    )


def pytest_collection_modifyitems(config, items):
    if not OLDER_BLENDER:
        return
    skip = pytest.mark.skip(reason=f"tests Blender {_GENERATED} behaviour")
    for item in items:
        if item.get_closest_marker("generated_blender"):
            item.add_marker(skip)


def _unavailable(error: BaseException | None) -> NodeUnavailableError | None:
    while error is not None:
        if isinstance(error, NodeUnavailableError):
            return error
        error = error.__cause__ or error.__context__
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if OLDER_BLENDER and call.excinfo is not None and report.failed:
        error = _unavailable(call.excinfo.value)
        if error is not None:
            report.outcome = "skipped"
            report.longrepr = (str(item.path), item.location[1] or 0, str(error))


CURRENT = Path(__file__).parent
BLEND_DIR = CURRENT / "blend_files"
JSON_DIR = CURRENT / "clippings"


@pytest.fixture(autouse=True, scope="function")
def clean_and_save(request):
    """Cleans the Blender file before each test and saves it after."""
    # Before each test: load a clean home file
    bpy.ops.wm.read_homefile(filepath=str(CURRENT / "data/test_startup.blend"))

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
        mod: bpy.types.NodesModifier = bpy.data.objects["Cube"].modifiers["StoreTrees"]
        with TreeBuilder("StoredTrees") as tree:
            ing = tree.inputs.geometry()
            ong = tree.outputs.geometry()

            for i, name in enumerate(geo_tree_names):
                node = g.Group()
                node.node.node_tree = bpy.data.node_groups[name]
                node.node.location = (0, 200 * i)

            if node.node.outputs and node.node.outputs[0].type == "GEOMETRY":
                _ = node >> ong
            else:
                _ = ing >> ong

        mod.node_group = tree.tree

    # --- Shader node trees: store via a material on the Cube ---
    shader_tree_names = [
        tree.name for tree in bpy.data.node_groups if tree.bl_idname == "ShaderNodeTree"
    ]

    if shader_tree_names:
        assert bpy.data.objects.get("Cube")
        node_tree = bpy.data.materials["Material"].node_tree
        assert node_tree
        with TreeBuilder.shader(node_tree) as tree:
            for i, name in enumerate(shader_tree_names):
                group_node = shader.Group()
                group_node.node.node_tree = bpy.data.node_groups[name]
                group_node.node.location = (0, 200 * i)

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
    # named after the current test function. Prefix the module so same-named
    # tests in different files (e.g. test_nodes) don't race on one file
    # under pytest-xdist.
    name = f"{request.module.__name__}.{request.node.name}"
    for key, value in (
        ("/", "divide"),
        ("+", "plus"),
        ("*", "multiply"),
        ("-", "subtract"),
    ):
        name = name.replace(key, value)
    # characters Windows forbids in file names, e.g. "<lambda>" in a test id
    name = re.sub(r'[<>:"|?\\]', "_", name)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_DIR / f"{name}.blend"))
