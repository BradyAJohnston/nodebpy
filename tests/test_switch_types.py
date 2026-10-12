"""Switch nodes take their type from the values they switch between, and a link
from or to a socket the node's settings hide raises instead of doing nothing."""

import pytest

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy.builder._utils import SocketError
from nodebpy.export import to_python


def _sources(tree, node):
    """(node, output) linked into each item input of ``node``."""
    return [
        (link.from_node.bl_idname, link.from_socket.name)
        for link in tree.tree.links
        if link.to_node == node.node
        and link.to_socket.name not in ("Switch", "Index", "Menu")
    ]


MESHES = [("GeometryNodeMeshCube", "Mesh"), ("GeometryNodeMeshUVSphere", "Mesh")]


def test_switch_takes_the_type_of_its_values():
    with TreeBuilder() as tree:
        switch = g.Switch(tree.inputs.boolean("Use"), g.Cube(), g.UVSphere())
    # left at Float, the UV Map outputs would have been linked instead
    assert switch.input_type == "GEOMETRY"
    assert _sources(tree, switch) == MESHES


def test_index_switch_takes_the_type_of_its_items():
    with TreeBuilder() as tree:
        switch = g.IndexSwitch(items=(node for node in [g.Cube(), g.UVSphere()]))
    assert switch.data_type == "GEOMETRY"
    assert _sources(tree, switch) == MESHES


def test_menu_switch_takes_the_type_of_its_items():
    with TreeBuilder() as tree:
        menu = tree.inputs.menu("Shape", "Cube")
        switch = g.MenuSwitch(
            menu, {"Cube": (g.Cube(), "A box"), "Sphere": g.UVSphere()}
        )
    assert switch.data_type == "GEOMETRY"
    assert _sources(tree, switch) == MESHES


@pytest.mark.parametrize(
    ("false", "true", "expected"),
    [
        (1, 2, "INT"),
        (1, 2.5, "FLOAT"),
        (True, False, "BOOLEAN"),
        ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), "VECTOR"),
        ("a", "b", "STRING"),
        (0.0, 0.0, "FLOAT"),
    ],
)
def test_plain_values_pick_the_type(false, true, expected):
    with TreeBuilder():
        assert g.Switch(False, false, true).input_type == expected


def test_a_linked_value_decides_over_a_plain_one():
    with TreeBuilder():
        assert g.Switch(False, g.Position(), (0, 0, 1)).input_type == "VECTOR"


def test_an_explicit_type_is_kept():
    with TreeBuilder():
        assert g.Switch(False, g.Value(), g.Value(), input_type="INT").input_type == (
            "INT"
        )
        assert g.IndexSwitch.vector(items=[g.Value()]).data_type == "VECTOR"


def test_values_of_different_types_raise():
    with TreeBuilder():
        with pytest.raises(SocketError, match="GEOMETRY from .*VECTOR from"):
            g.Switch(False, g.Cube(), g.Position())
        with pytest.raises(SocketError, match=r"IndexSwitch\.float"):
            g.IndexSwitch(items=[g.Value(), g.Cube()])


def test_linking_a_hidden_output_raises():
    with TreeBuilder():
        dot = g.VectorMath.dot_product((1, 0, 0), (0, 1, 0))
        with pytest.raises(RuntimeError, match=r"no 'Vector' output.*\['Value'\]"):
            dot.o.vector >> g.SetPosition(offset=...)


def test_compositor_index_switch_takes_the_type_of_its_items():
    """The compositor's Index Switch is the same node, with fewer types."""
    with c.tree() as tree:
        floats = c.IndexSwitch(items=[c.Value(), c.Value()])
        vectors = c.IndexSwitch(items=[c.CombineXYZ(), c.CombineXYZ()])
        ints = c.IndexSwitch(items=[1, 2])
    assert (floats.data_type, vectors.data_type, ints.data_type) == (
        "FLOAT",
        "VECTOR",
        "INT",
    )
    # left at Color, the values would have been converted to colours
    assert {link.to_socket.type for link in tree.tree.links} == {"VALUE", "VECTOR"}


def test_compositor_index_switch_defaults_to_color():
    with c.tree():
        assert c.IndexSwitch().data_type == "RGBA"
        assert c.IndexSwitch.integer_vector(items=[(1, 2, 3)]).data_type == (
            "INT_VECTOR"
        )
        assert not hasattr(c.IndexSwitch, "geometry")


def test_a_type_the_tree_does_not_switch_raises():
    with g.tree():
        mesh = g.Cube().o.mesh.socket
    with c.tree():
        with pytest.raises(SocketError, match="can't switch GEOMETRY.*INT_VECTOR"):
            c.IndexSwitch(items=[mesh])


def test_compositor_index_switch_exports_with_its_alias():
    with c.tree() as tree:
        c.IndexSwitch.integer_vector(items=[(1, 2, 3)])
        c.IndexSwitch(items=[c.Value()])
    code = to_python(tree)
    assert "c.IndexSwitch.integer_vector(" in code
    assert "c.IndexSwitch.float(" in code
