import bpy
import pytest

import nodebpy as nb
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import (
    CustomCompositorGroup,
    CustomGeometryGroup,
    CustomShaderGroup,
)
from nodebpy.types import InputFloat, InputGeometry, InputInteger


@nb.geometry_tree("Decorated Scatter")
def scatter(geometry: InputGeometry, count: InputInteger = 64, radius: float = 0.05):
    """Scatter spheres on the input geometry."""
    points = geometry >> g.DistributePointsOnFaces(density=count)
    return points >> g.InstanceOnPoints(instance=g.IcoSphere(radius=radius))


def _interface(node, in_out):
    return {
        item.name: item
        for item in node.node.node_tree.interface.items_tree
        if getattr(item, "in_out", None) == in_out
    }


def test_signature_becomes_interface():
    with g.tree():
        node = scatter()

    assert isinstance(node, CustomGeometryGroup)
    assert node.node.node_tree.name == "Decorated Scatter"
    assert scatter.__doc__ == "Scatter spheres on the input geometry."

    inputs = _interface(node, "INPUT")
    assert list(inputs) == ["Geometry", "Count", "Radius"]
    assert inputs["Geometry"].socket_type == "NodeSocketGeometry"
    assert inputs["Count"].socket_type == "NodeSocketInt"
    assert inputs["Count"].default_value == 64
    assert inputs["Radius"].socket_type == "NodeSocketFloat"
    assert inputs["Radius"].default_value == pytest.approx(0.05)


def test_return_value_becomes_output():
    with g.tree():
        node = scatter()

    outputs = _interface(node, "OUTPUT")
    assert list(outputs) == ["Instances"]
    assert outputs["Instances"].socket_type == "NodeSocketGeometry"
    assert node.node.outputs["Instances"].type == "GEOMETRY"

    group_output = node.node.node_tree.nodes["Group Output"]
    assert group_output.inputs["Instances"].is_linked


def test_each_call_adds_a_node_and_reuses_the_group():
    with g.tree() as tree:
        first = scatter(count=10)
        second = g.Cube() >> scatter(radius=g.Value(0.2) >> g.Math.add(1.0))
        _ = second >> tree.outputs.geometry()

        assert first.node.node_tree == second.node.node_tree
        assert len([n for n in tree.nodes if n.bl_idname == "GeometryNodeGroup"]) == 2

        assert first.node.inputs["Count"].default_value == 10
        assert first.node.inputs["Radius"].default_value == pytest.approx(0.05)
        assert not first.node.inputs["Radius"].is_linked

        assert second.node.inputs["Geometry"].is_linked
        assert second.node.inputs["Count"].default_value == 64
        assert second.node.inputs["Radius"].is_linked
        assert second.node.outputs["Instances"].is_linked

    groups = [t for t in bpy.data.node_groups if t.name.startswith("Decorated Scatter")]
    assert len(groups) == 1


def test_positional_arguments():
    with g.tree():
        node = scatter(g.Cube(), 7, 0.5)

    assert node.node.inputs["Geometry"].is_linked
    assert node.node.inputs["Count"].default_value == 7
    assert node.node.inputs["Radius"].default_value == pytest.approx(0.5)


def test_tuple_return_gives_multiple_outputs():
    @nb.geometry_tree("Decorated Tuple")
    def split(value: float = 1.0):
        return value * 2.0, g.Points(3), g.Cube()

    with g.tree():
        node = split()

    outputs = _interface(node, "OUTPUT")
    assert list(outputs) == ["Value", "Points", "Mesh"]
    assert outputs["Value"].socket_type == "NodeSocketFloat"
    assert outputs["Points"].socket_type == "NodeSocketGeometry"
    assert outputs["Mesh"].socket_type == "NodeSocketGeometry"
    assert node.o.value.socket.type == "VALUE"


def test_dict_return_names_outputs():
    @nb.geometry_tree("Decorated Dict")
    def stats(value: float = 1.0):
        return {"Double": value * 2.0, "Triple": value * 3.0}

    with g.tree():
        node = stats()

    assert list(_interface(node, "OUTPUT")) == ["Double", "Triple"]
    assert node.o.double.socket.type == "VALUE"


def test_none_return_gives_no_outputs():
    @nb.geometry_tree("Decorated No Outputs")
    def nothing(value: float = 1.0):
        _ = g.Points(1)

    with g.tree():
        node = nothing()

    assert _interface(node, "OUTPUT") == {}


def test_duplicate_output_names_rejected():
    @nb.geometry_tree("Decorated Duplicates")
    def twice(value: float = 1.0):
        return value * 2.0, value * 3.0

    with g.tree(), pytest.raises(TypeError, match="two outputs named 'Value'"):
        twice()


def test_non_socket_return_rejected():
    @nb.geometry_tree("Decorated Bad Return")
    def number(value: float = 1.0):
        return 3.0

    with g.tree(), pytest.raises(TypeError, match="not a socket or node"):
        number()


def test_name_defaults_to_function_name():
    @nb.geometry_tree()
    def offset_points(offset: float = 1.0):
        return g.Points(1) >> g.SetPosition(offset=offset)

    with g.tree():
        node = offset_points(offset=2.0)

    assert node.node.node_tree.name == "Offset Points"
    assert node.node.inputs["Offset"].default_value == pytest.approx(2.0)


def test_string_annotations():
    @nb.geometry_tree("Decorated String Annotations")
    def stringy(count: "int" = 3, scale: "nb.types.InputFloat" = 2.0):
        return g.Points(count), scale

    with g.tree():
        node = stringy()

    assert node.node.inputs["Count"].default_value == 3
    assert node.node.inputs["Scale"].default_value == pytest.approx(2.0)
    assert list(_interface(node, "OUTPUT")) == ["Points", "Scale"]


def test_shader_tree():
    @nb.shader_tree("Decorated Shader")
    def glossy(roughness: InputFloat = 0.25):
        return s.PrincipledBSDF(roughness=roughness)

    with s.tree() as tree:
        node = glossy(roughness=0.75)
        _ = node >> tree.outputs.shader()

    assert isinstance(node, CustomShaderGroup)
    assert node.node.node_tree.name == "Decorated Shader"
    assert node.node.inputs["Roughness"].default_value == pytest.approx(0.75)
    assert list(_interface(node, "OUTPUT")) == ["BSDF"]
    assert node.node.outputs["BSDF"].is_linked


def test_compositor_tree():
    @nb.compositor_tree("Decorated Compositor")
    def blur(image: nb.types.InputColor, size: float = 4.0):
        return image >> c.Kuwahara(size=size)

    with c.tree() as tree:
        image = tree.inputs.color("Image")
        node = image >> blur(size=8.0)
        _ = node >> tree.outputs.color("Image")

    assert isinstance(node, CustomCompositorGroup)
    assert node.node.node_tree.name == "Decorated Compositor"
    assert node.node.inputs["Image"].is_linked
    assert node.node.inputs["Size"].default_value == pytest.approx(8.0)
    assert list(_interface(node, "OUTPUT")) == ["Image"]


def test_requires_tree_context():
    with pytest.raises(RuntimeError, match="within a TreeBuilder context"):
        scatter()


def test_rejects_unannotated_parameter():
    with pytest.raises(TypeError, match="needs a socket type annotation"):

        @nb.geometry_tree("Decorated Bad")
        def bad(count):
            pass


def test_rejects_var_args():
    with pytest.raises(TypeError, match=r"cannot use \*args"):

        @nb.geometry_tree("Decorated Bad")
        def bad(*values: float):
            pass
