import bpy
import pytest
from bpy.types import (
    CompositorNodeTree,
    FunctionNodeInputInt,
    GeometryNodeTree,
    ShaderNodeTree,
)

import nodebpy as nb
from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.nodes.geometry.groups import PrincipalComponents


def test_create_tree_and_save():
    with TreeBuilder("AnotherTree") as tree:
        count = tree.inputs.integer("Count")
        instances = tree.outputs.geometry("Instances")

        rotation = (
            g.RandomValue.vector(min=(-1, -1, -1), seed=2)
            >> g.AlignRotationToVector()
            >> g.RotateRotation(
                rotate_by=g.AxisAngleToRotation(angle=0.3),
                rotation_space="LOCAL",
            )
        )

        _ = (
            count
            >> g.Points(position=g.RandomValue.vector(min=(-1, -1, -1)))
            >> g.InstanceOnPoints(instance=g.Cube(), rotation=rotation)
            >> g.SetPosition(
                position=g.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> g.RealizeInstances()
            >> g.InstanceOnPoints(g.Cube(), instance=...)
            >> instances
        )


def test_panel_groups_input_sockets():
    """Test that sockets created inside a panel context are children of that panel."""
    with TreeBuilder("PanelInputTest") as tree:
        tree.inputs.geometry("Geometry")
        with tree.inputs.panel("Settings"):
            tree.inputs.integer("Count")
            tree.inputs.float("Scale")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 1
        assert panel_items[0].name == "Settings"

        count_item = next(i for i in items if getattr(i, "name", None) == "Count")
        scale_item = next(i for i in items if getattr(i, "name", None) == "Scale")
        assert count_item.parent == panel_items[0]
        assert scale_item.parent == panel_items[0]

        geo_item = next(i for i in items if getattr(i, "name", None) == "Geometry")
        assert geo_item.parent != panel_items[0]


def test_panel_groups_output_sockets():
    """Test that panels work on outputs too."""
    with TreeBuilder("PanelOutputTest") as tree:
        with tree.outputs.panel("Results"):
            tree.outputs.geometry("Geometry")
        tree.outputs.float("Extra")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 1
        assert panel_items[0].name == "Results"

        geo_item = next(i for i in items if getattr(i, "name", None) == "Geometry")
        extra_item = next(i for i in items if getattr(i, "name", None) == "Extra")
        assert geo_item.parent == panel_items[0]
        assert extra_item.parent != panel_items[0]


def test_multiple_panels():
    """Test creating multiple panels in the same inputs context."""
    with TreeBuilder("MultiPanelTest") as tree:
        with tree.inputs.panel("Transform"):
            tree.inputs.vector("Position")
        with tree.inputs.panel("Appearance"):
            tree.inputs.color("Color")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 2
        panel_names = {p.name for p in panel_items}
        assert panel_names == {"Transform", "Appearance"}

        pos_item = next(i for i in items if getattr(i, "name", None) == "Position")
        color_item = next(i for i in items if getattr(i, "name", None) == "Color")
        assert pos_item.parent.name == "Transform"
        assert color_item.parent.name == "Appearance"


def test_panel_default_closed():
    """Test that the default_closed option is applied to the panel."""
    with TreeBuilder("PanelClosedTest") as tree:
        with tree.inputs.panel("Advanced", default_closed=True):
            tree.inputs.float("Threshold")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        assert panel.default_closed is True


def test_panel_context_clears_after_exit():
    """Test that sockets after the panel block are not in the panel."""
    with TreeBuilder("PanelClearTest") as tree:
        with tree.inputs.panel("Group"):
            tree.inputs.integer("Inside")
        tree.inputs.integer("Outside")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        inside = next(i for i in items if getattr(i, "name", None) == "Inside")
        outside = next(i for i in items if getattr(i, "name", None) == "Outside")
        assert inside.parent == panel
        assert outside.parent != panel


def test_string_generators(snapshot):
    with g.tree():
        tree = TreeBuilder(PrincipalComponents().node_tree)

    assert snapshot == tree.to_python(format=False)
    assert snapshot == tree.to_mermaid()
    assert snapshot == tree.to_mermaid(fenced=False)


def test_tree_decorator():
    """Test that the tree decorator works correctly."""

    @nb.geometry_tree("Simple Points Group")
    def new_group(tree: nb.TreeBuilder[GeometryNodeTree], count: int):
        g.Integer(count) >> g.Points() >> tree.outputs.geometry()

    tree = new_group(100)
    assert isinstance(tree, GeometryNodeTree)
    assert tree.name == "Simple Points Group"
    assert new_group.__name__ == "new_group"
    node: FunctionNodeInputInt = tree.nodes["Integer"]  # ty: ignore
    assert node.integer == 100
    assert len(tree.nodes) == 3

    # calling again reuses the existing data-block instead of rebuilding,
    # so the arguments of the second call are ignored
    other = new_group(count=42)
    assert other == tree
    node = other.nodes["Integer"]  # ty: ignore
    assert node.integer == 100


def test_tree_decorator_name_clash():
    from nodebpy import shader as s

    @nb.shader_tree("Clashing Group Name")
    def new_shader(tree: nb.TreeBuilder[ShaderNodeTree]):
        _ = s.PrincipledBSDF() >> tree.outputs.shader()

    new_shader()

    @nb.geometry_tree("Clashing Group Name")
    def new_group(tree: nb.TreeBuilder[GeometryNodeTree]):
        pass

    with pytest.raises(TypeError, match="already exists as ShaderNodeTree"):
        new_group()


def test_shader_tree_decorator():
    from nodebpy import shader as s

    @nb.shader_tree("Decorated Shader")
    def new_shader(tree: nb.TreeBuilder[ShaderNodeTree], roughness: float):
        _ = s.PrincipledBSDF(roughness=roughness) >> tree.outputs.shader()

    tree = new_shader(0.25)
    assert isinstance(tree, ShaderNodeTree)
    assert tree.name == "Decorated Shader"
    node = tree.nodes["Principled BSDF"]
    assert node.inputs["Roughness"].default_value == 0.25  # ty: ignore
    assert len(tree.nodes) == 2


def test_compositor_tree_decorator():
    from nodebpy import compositor as c

    @nb.compositor_tree("Decorated Compositor")
    def new_compositor(tree: nb.TreeBuilder[CompositorNodeTree], size: float):
        image = tree.inputs.color("Image")
        _ = image >> c.Kuwahara(size=size) >> tree.outputs.color("Image")

    tree = new_compositor(4.0)
    assert isinstance(tree, CompositorNodeTree)
    assert tree.name == "Decorated Compositor"
    node = tree.nodes["Kuwahara"]
    assert node.inputs["Size"].default_value == 4.0  # ty: ignore
    assert len(tree.nodes) == 3
