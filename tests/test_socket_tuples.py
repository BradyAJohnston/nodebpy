"""Tuples holding sockets feed vector, rotation and color inputs through a
Combine node."""

import pytest

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder._utils import SocketError


def _combined(socket):
    """(node type, component sources) of the Combine node linked into ``socket``."""
    node = socket.links[0].from_node
    components = [
        "linked" if i.links else round(i.default_value, 3)
        for i in node.inputs
        if i.enabled
    ]
    return node.bl_idname, components


def test_tuple_with_a_socket_builds_combine_xyz():
    with g.tree() as tree:
        height = tree.inputs.float("Height")
        cube = g.Cube(size=(1, 1, height))
    assert _combined(cube.node.inputs["Size"]) == (
        "ShaderNodeCombineXYZ",
        [1.0, 1.0, "linked"],
    )


def test_operators_and_items_take_socket_tuples():
    with g.tree() as tree:
        height = tree.inputs.float("Height")
        moved = g.Position().o.position + (0, 0, height)
        viewer = g.Viewer()
        item = viewer.items.vector((height, 0, 0))
    assert _combined(moved.node.inputs[1])[1] == [0.0, 0.0, "linked"]
    assert _combined(item.input.socket)[1] == ["linked", 0.0, 0.0]


def test_euler_tuple_feeds_a_rotation_input():
    with g.tree() as tree:
        angle = tree.inputs.float("Angle")
        node = g.InstanceOnPoints(rotation=(0, 0, angle))
    assert _combined(node.node.inputs["Rotation"])[0] == "ShaderNodeCombineXYZ"


def test_color_tuples_use_each_trees_combine_color():
    with s.material("Tinted"):
        bsdf = s.PrincipledBSDF(base_color=(s.Value(), 0.2, 0.1, 1.0))
    assert _combined(bsdf.node.inputs["Base Color"]) == (
        "ShaderNodeCombineColor",
        ["linked", 0.2, 0.1],
    )
    with c.tree():
        x = c.Value()
        blur = c.Blur(image=(x, x, x, x))
    assert _combined(blur.node.inputs["Image"])[0] == "CompositorNodeCombineColor"


def test_bad_socket_tuples_raise():
    with g.tree() as tree:
        height = tree.inputs.float("Height")
        with pytest.raises(SocketError, match=r"3 components, not 2: \(Group Input"):
            g.SetPosition(offset=(height, 0))
    with s.material("Alpha"):
        with pytest.raises(SocketError, match="no alpha"):
            s.PrincipledBSDF(base_color=(0.1, 0.2, 0.1, s.Value()))
