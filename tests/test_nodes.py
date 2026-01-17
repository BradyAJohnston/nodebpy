import itertools

import pytest

import nodebpy.nodes.converter
import nodebpy.nodes.geometry
import nodebpy.nodes.grid
import nodebpy.nodes.input
from nodebpy import TreeBuilder
from nodebpy import nodes as n


def test_capture_attribute():
    with TreeBuilder("TestCaptureAttribute") as tree:
        cube = n.Cube()
        cap = n.CaptureAttribute(domain="POINT")

        _ = (
            cube
            >> cap
            >> n.SetPosition(offset=(0, 0, 10))
            >> n.SetPosition(position=cap.capture(nodebpy.nodes.input.Position()))
        )

    assert "Capture Attribute" in tree.nodes
    assert len(cap._items) == 1
    assert cap.node.outputs[1].name == "Position"
    assert cap.node.outputs[1].type == "VECTOR"


def test_join_geometry():
    with TreeBuilder("TestJoinGeometry") as tree:
        items = [n.Cube(), n.UVSphere(), n.Cone(), n.Cylinder(), n.Grid()]
        join = nodebpy.nodes.geometry.JoinGeometry(*items)

    assert "Join Geometry" in tree.nodes
    assert len(join.node.inputs["Geometry"].links) == 5
    # links to join geometry are created in reverse order but we internally reverse them back
    assert join._default_input_socket.links[0].from_node == items[0].node


def test_socket_selection():
    with TreeBuilder("AnotherTree"):
        pos = n.SetPosition()
        vec = nodebpy.nodes.input.Vector()

        vec >> pos.i_offset
        nodebpy.nodes.input.Position() * 1.0 >> pos.i_position

    assert pos.i_offset.socket_name == "Offset"
    assert vec.o_vector.socket.links[0].to_socket.node == pos.node
    assert vec.o_vector.socket.links[0].to_socket == pos.i_offset.socket
    assert len(pos.i_offset.socket.links) == 1


class TestMathOperators:
    @pytest.mark.parametrize(
        "operator,input",
        itertools.product(
            ["+", "-", "*", "/"],
            [nodebpy.nodes.input.Vector, nodebpy.nodes.input.Value],
        ),
    )
    def test_math_operators(self, operator, input):
        with TreeBuilder("TestMathOperators"):
            set_pos = n.SetPosition()
            pos = nodebpy.nodes.input.Position()  # noqa: F841

            eval(f"input() {operator} 1.0 {operator} pos >> set_pos")

        assert len(set_pos.i_offset.socket.links) == 0
        assert len(set_pos.i_geometry.socket.links) == 0
        assert len(set_pos.i_position.socket.links) == 1


def test_format_string():
    format_string = "Hello {x} friends, it is {y} hours and this is a {String}"
    with TreeBuilder("TestFormatString"):
        x_int = n.Integer(5)
        y_value = n.Value(12.50)
        format = nodebpy.nodes.converter.FormatString(
            n.String("test"),
            format=format_string,
            x=x_int,
            y=y_value,
        )

        assert len(format.node.format_items) == 3
        assert format.node.inputs[0].default_value == format_string  # type: ignore
        assert format.node.inputs[1].name == "String"
        assert format.node.inputs[1].type == "STRING"
        assert format.node.inputs[1].default_value == ""
        assert format.node.inputs[2].name == "x"
        assert format.node.inputs[2].type == "INT"
        assert format.node.inputs[2].default_value == 0  # type: ignore
        assert format.node.inputs[3].name == "y"
        assert format.node.inputs[3].type == "VALUE"
        assert format.node.inputs[3].default_value == 0.0
        assert format.items["String"].socket == format.node.inputs[1]
        assert format.items["x"].socket == format.node.inputs[2]
        assert format.items["y"].socket == format.node.inputs[3]


def test_field_to_grid():
    with TreeBuilder() as tree:
        # the rotation value should add a vector item as the next available compatible data type
        inputs = [n.Vector(), n.Value(), n.Boolean(), n.Integer(), n.Rotation()]
        math = n.Math.add()

        ftg = n.FieldToGrid(*inputs, test=n.Value())
        _ = ftg.output_sockets["test"] >> math

    assert len(tree.nodes) == 8
    assert len(ftg.node.grid_items) == 6
    assert ftg.node.grid_items[5].name == "test"
    assert ftg.output_sockets["test"].socket.links[0].to_socket.node == math.node
    assert all(
        [i._default_output_socket.links[0].to_socket.node == ftg.node for i in inputs]
    )
    for item, type in zip(
        ftg.node.grid_items, ["VECTOR", "FLOAT", "BOOLEAN", "INT", "VECTOR", "FLOAT"]
    ):
        assert item.data_type == type


def test_geometry_to_instance():
    with TreeBuilder() as tree:
        inputs = [n.Cube(), n.UVSphere(), n.IcoSphere(), n.Cone()]
        gti = nodebpy.nodes.geometry.GeometryToInstance(*inputs)

    assert len(tree.nodes) == 5
    assert len(gti.node.inputs[0].links) == 4
    assert gti._default_input_socket.links[2].from_node == inputs[2].node
    assert gti._default_input_socket.links[1].from_node == inputs[1].node


def test_get_named_grid(snapshot_tree):
    with TreeBuilder() as tree:
        ftg = (
            n.VolumeCube()
            >> n.GetNamedGrid(name="density")
            >> n.FieldToGrid(n.Position(), n.Position() * 2 + 10)
        )

    assert snapshot_tree == tree
