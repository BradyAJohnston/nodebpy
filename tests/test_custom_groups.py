from functools import reduce

import bpy
import pytest
from bpy.types import CompositorNodeTree, GeometryNodeTree, ShaderNodeTree

from nodebpy.builder import (
    CustomCompositorGroup,
    CustomGeometryGroup,
    CustomShaderGroup,
    SocketLinker,
    TreeBuilder,
)
from nodebpy.nodes import compositor as c
from nodebpy.nodes import geometry as g
from nodebpy.nodes import shader as s
from nodebpy.nodes.geometry import IntegerMath
from nodebpy.nodes.geometry.groups import OffsetVector, OtherVertex
from nodebpy.types import InputColor

# ---------------------------------------------------------------------------
# Concrete subclasses used in the new tests below
# ---------------------------------------------------------------------------


class _SimpleGeomGroup(CustomGeometryGroup):
    _name = "Test Simple Geometry Group"
    _color_tag = "GEOMETRY"
    _warning_propagation = "ERRORS"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]):
        x = tree.inputs.float("Value")
        x >> tree.outputs.float("Result")


class _SimpleShaderGroup(CustomShaderGroup):
    _name = "Test Simple Shader Group"

    def _build_group(self, tree):
        x = tree.inputs.float("Value")
        x >> tree.outputs.float("Result")


class _SimpleCompositorGroup(CustomCompositorGroup):
    _name = "Test Simple Compositor Group"

    def _build_group(self, tree):
        x = tree.inputs.float("Value")
        x >> tree.outputs.float("Result")


def test_custom_group():
    with TreeBuilder() as tb:
        last_group = reduce(
            lambda x, y: x >> y, [OtherVertex(edge_number=x) for x in range(5)]
        )

    assert last_group.node.node_tree.name == "Other Vertex"
    assert len(tb) == 5
    assert len(tb.tree.links) == 4
    # we should be re-using the same node group for multiple instances
    assert len(bpy.data.node_groups) == 2


def test_custom_group_with_offset():
    with TreeBuilder() as tb:
        last_node = reduce(
            lambda x, y: x >> y, [OffsetVector(offset=x) for x in range(5)]
        )
        offset = OffsetVector()

    assert last_node.node.node_tree.name == "Offset Vector"
    assert len(tb) == 6
    assert len(tb.tree.links) == 4
    math = offset.node.node_tree.nodes["Group Input"].outputs[0].links[0].to_node
    assert math.bl_idname == IntegerMath._bl_idname
    assert math.operation == "ADD"


# --- Instance access returns SocketLinker (Blender) ---


def test_i_prefix_returns_socket_linker():
    """Accessing i_* on an instance returns a SocketLinker for that input socket."""
    with TreeBuilder():
        node = OtherVertex()
        linker = node.i.vertex_index

    assert isinstance(linker, SocketLinker)
    assert linker.socket_name == "Vertex Index"


def test_o_prefix_returns_socket_linker():
    """Accessing o_* on an instance returns a SocketLinker for that output socket."""
    with TreeBuilder():
        node = OtherVertex()
        out = node.o.other_vertex

    assert isinstance(out, SocketLinker)


def test_wrong_attribute_access():
    """Accessing a non-existent attribute raises an AttributeError."""
    with TreeBuilder():
        node = OtherVertex()

        with pytest.raises(AttributeError):
            node.wrong_attribute_name
        with pytest.raises(AttributeError):
            node.o.wrong_attribute_name


# --- Group caching ---


def test_group_reuses_existing_node_group():
    """Second instantiation reuses the cached node group, not a new one."""
    with TreeBuilder():
        a = OtherVertex()
        b = OtherVertex()

    assert a.node.node_tree is b.node.node_tree
    assert a.node is not b.node


# ---------------------------------------------------------------------------
# ShaderNodeGroup
# ---------------------------------------------------------------------------


def test_shader_node_group_creates_shader_tree():
    """ShaderNodeGroup.node_tree is a ShaderNodeTree."""
    with TreeBuilder.shader():
        node = _SimpleShaderGroup()
    assert isinstance(node.node.node_tree, ShaderNodeTree)


def test_shader_node_group_reuses_tree():
    """Multiple instances share the same underlying ShaderNodeTree."""
    with TreeBuilder.shader():
        a = _SimpleShaderGroup()
        b = _SimpleShaderGroup()
    assert a.node.node_tree is b.node.node_tree
    assert a.node is not b.node


# ---------------------------------------------------------------------------
# CompositorNodeGroup
# ---------------------------------------------------------------------------


def test_compositor_node_group_creates_compositor_tree():
    """CompositorNodeGroup.node_tree is a CompositorNodeTree."""
    with TreeBuilder.compositor():
        node = _SimpleCompositorGroup()
    assert isinstance(node.node.node_tree, CompositorNodeTree)


def test_compositor_node_group_reuses_tree():
    """Multiple instances share the same underlying CompositorNodeTree."""
    with TreeBuilder.compositor():
        a = _SimpleCompositorGroup()
        b = _SimpleCompositorGroup()
    assert a.node.node_tree is b.node.node_tree
    assert a.node is not b.node


# ---------------------------------------------------------------------------
# GeometryNodeGroup — class-level properties
# ---------------------------------------------------------------------------


def test_geometry_node_group_creates_geometry_tree():
    """GeometryNodeGroup.node_tree is a GeometryNodeTree."""
    with TreeBuilder():
        node = _SimpleGeomGroup()
    assert isinstance(node.node.node_tree, GeometryNodeTree)


def test_geometry_node_group_color_tag():
    """_color_tag is applied to the node tree on first creation."""
    with TreeBuilder():
        node = _SimpleGeomGroup()
    assert node.node.node_tree.color_tag == "GEOMETRY"


def test_geometry_node_group_warning_propagation():
    """_warning_propagation is applied to the node instance."""
    with TreeBuilder():
        node = _SimpleGeomGroup()
    assert node.node.warning_propagation == "ERRORS"


# ---------------------------------------------------------------------------
# Type-mismatch detection
# ---------------------------------------------------------------------------


def test_type_mismatch_geometry_vs_shader_raises():
    """Reusing a geometry group name for a ShaderNodeGroup raises TypeError."""

    class _ConflictGeom(CustomGeometryGroup):
        _name = "Test Conflict Geom vs Shader"

        def _build_group(self, tree):
            pass

    class _ConflictShader(CustomShaderGroup):
        _name = "Test Conflict Geom vs Shader"

        def _build_group(self, tree):
            pass

    with TreeBuilder():
        _ConflictGeom()

    with TreeBuilder.shader():
        with pytest.raises(TypeError, match="already exists"):
            _ConflictShader()


def test_type_mismatch_shader_vs_compositor_raises():
    """Reusing a shader group name for a CompositorNodeGroup raises TypeError."""

    class _ConflictShader(CustomShaderGroup):
        _name = "Test Conflict Shader vs Compositor"

        def _build_group(self, tree):
            pass

    class _ConflictCompositor(CustomCompositorGroup):
        _name = "Test Conflict Shader vs Compositor"

        def _build_group(self, tree):
            pass

    with TreeBuilder.shader():
        _ConflictShader()

    with TreeBuilder.compositor():
        with pytest.raises(TypeError, match="already exists"):
            _ConflictCompositor()


def test_same_name_same_type_does_not_raise():
    """Reusing a name for the same tree type is fine — it returns the cached tree."""

    class _CacheA(CustomGeometryGroup):
        _name = "Test Same Type Cache"

        def _build_group(self, tree):
            pass

    class _CacheB(CustomGeometryGroup):
        _name = "Test Same Type Cache"

        def _build_group(self, tree):
            pass

    with TreeBuilder():
        a = _CacheA()
        b = _CacheB()  # different Python class, same _name → reuses

    assert a.node.node_tree is b.node.node_tree


# ---------------------------------------------------------------------------
# _build_group is a regular instance method (not classmethod)
# ---------------------------------------------------------------------------


def test_build_group_receives_instance_not_class():
    """_build_group receives self as a class instance, not the class itself."""
    captured = []

    class _SelfCheck(CustomGeometryGroup):
        _name = "Test Build Group Self Check"

        def _build_group(self, tree):
            captured.append(self)

    with TreeBuilder():
        _SelfCheck()

    assert len(captured) == 1
    assert isinstance(captured[0], _SelfCheck)
    assert not isinstance(captured[0], type)


def test_build_group_called_once_across_instances():
    """_build_group is only called when the group is first created, not on reuse."""
    call_count = [0]

    class _CountCalls(CustomGeometryGroup):
        _name = "Test Build Group Call Count"

        def _build_group(self, tree):
            call_count[0] += 1

    with TreeBuilder():
        _CountCalls()
        _CountCalls()
        _CountCalls()

    assert call_count[0] == 1


def test_group_already_exists_wrong_type():
    class _GeomGroup(CustomGeometryGroup):
        _name = "TestGroup"

        def _build_group(self, tree):
            pass

    class _CompGroup(CustomCompositorGroup):
        _name = "TestGroup"

        def _build_group(self, tree):
            pass

    with g.tree():
        _GeomGroup()

    with c.tree():
        with pytest.raises(TypeError):
            _CompGroup()


class TestCustomShaderGroup:
    class _SimpleEmissionGroup(CustomShaderGroup):
        _name = "SimpleEmission"

        def _build_group(self, tree: TreeBuilder):
            s.Attribute.geometry("Color") >> tree.outputs.shader("Shader")

    def test_simple_emission_group(self):
        with s.tree():
            node = self._SimpleEmissionGroup()
            assert isinstance(node.node_tree, ShaderNodeTree)
            assert len(node.node_tree.nodes) == 2


class TestCustomCompositorGroup:
    class _SimpleCompositorGroup(CustomCompositorGroup):
        _name = ""

        def __init__(self, image: InputColor):
            kwargs = {
                "Image": image,
            }
            super().__init__(**kwargs)

        def _build_group(self, tree: TreeBuilder):
            (
                tree.inputs.color("Image")
                >> c.AlphaOver()
                >> c.Blur()
                >> tree.outputs.color("Image")
            )

    def test_simple_compositor_group(self):
        with c.tree() as tree:
            node = self._SimpleCompositorGroup(c.RenderLayers().o.image)
            assert isinstance(node.node_tree, CompositorNodeTree)
            assert len(node.node_tree.nodes) == 4
            node >> tree.outputs.color("Image")


class TestMenuDefaultValue:
    class SimpleMenuGroup(CustomGeometryGroup):
        _name = "SimpleMenuGroup"

        def __init__(self, letter: str = "B"):
            kwargs = {
                "Letter": letter,
            }
            super().__init__(**kwargs)

        def _build_group(self, tree: TreeBuilder):
            (
                tree.inputs.menu("Letter", "B")
                >> g.MenuSwitch.string(
                    **{letter: letter for letter in "ABCDEFG"}, menu=...
                )
                >> tree.outputs.string()
            )

    def test_simple_menu_group(self):
        with g.tree():
            node = self.SimpleMenuGroup()
            assert node.i.letter.default_value == "B"
            node = self.SimpleMenuGroup("C")
            assert node.i.letter.default_value == "C"

            ms = g.MenuSwitch.string(
                **{letter: letter for letter in "ABCDEFG"}, menu=...
            )
            assert ms.i.menu.default_value == "A"
