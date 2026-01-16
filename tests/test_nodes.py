import itertools

import pytest

from nodebpy import TreeBuilder
from nodebpy import nodes as n
import nodebpy.nodes.input


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
        join = n.JoinGeometry(geometry=items)

    assert "Join Geometry" in tree.nodes
    assert len(join.node.inputs["Geometry"].links) == 5
    # links to join geometry are created in reverse order but we internally reverse them back
    assert join._default_input_socket.links[0].from_node == items[0].node


def test_socket_selection():
    with TreeBuilder("AnotherTree"):
        pos = n.SetPosition()
        vec = n.Vector()

        vec >> pos.i_offset
        nodebpy.nodes.input.Position() * 1.0 >> pos.i_position

    assert pos.i_offset.socket_name == "Offset"
    assert vec.o_vector.socket.links[0].to_socket.node == pos.node
    assert vec.o_vector.socket.links[0].to_socket == pos.i_offset.socket
    assert len(pos.i_offset.socket.links) == 1


class TestMathOperators:
    @pytest.mark.parametrize(
        "operator,input",
        itertools.product(["+", "-", "*", "/"], [n.Vector, nodebpy.nodes.input.Value]),
    )
    def test_math_operators(self, operator, input):
        with TreeBuilder("TestMathOperators"):
            set_pos = n.SetPosition()
            pos = nodebpy.nodes.input.Position()  # noqa: F841

            eval(f"input() {operator} 1.0 {operator} pos >> set_pos")

        assert len(set_pos.i_offset.socket.links) == 0
        assert len(set_pos.i_geometry.socket.links) == 0
        assert len(set_pos.i_position.socket.links) == 1
