"""Switch nodes take their type from the values they switch between, and a link
from or to a socket the node's settings hide raises instead of doing nothing."""

import bpy
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


def test_compositor_switch_is_the_typed_switch():
    """Blender 5.2 deprecates the compositor's Color-only Switch."""
    with c.tree() as tree:
        image = tree.inputs.color("Image")
        switch = c.Switch(True, image, c.Blur(image))
        values = c.Switch(False, c.Value(), 2.0)
    assert c.Switch._bl_idname == "GeometryNodeSwitch"
    assert (switch.input_type, values.input_type) == ("RGBA", "FLOAT")
    assert hasattr(c.Switch, "integer_vector") and not hasattr(c.Switch, "geometry")


def test_deprecated_node_warns_at_the_callers_line():
    with g.tree():
        with pytest.warns(DeprecationWarning, match="RotateRotation") as caught:
            g.RotateEuler.axis_angle()
    assert caught[0].filename == __file__


def test_legacy_compositor_switch_exports_as_the_typed_switch():
    tree = bpy.data.node_groups.new("Legacy Switch", "CompositorNodeTree")
    tree.interface.new_socket("Image", in_out="INPUT", socket_type="NodeSocketColor")
    tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    group_in = tree.nodes.new("NodeGroupInput")
    group_out = tree.nodes.new("NodeGroupOutput")
    legacy = tree.nodes.new("CompositorNodeSwitch")
    tree.links.new(group_in.outputs[0], legacy.inputs["On"])
    tree.links.new(legacy.outputs[0], group_out.inputs[0])

    code = to_python(tree)
    assert "c.Switch.color(" in code
    namespace: dict = {}
    exec(code, namespace)  # noqa: S102
    rebuilt = namespace["tree"].tree
    switch = next(n for n in rebuilt.nodes if n.bl_idname == "GeometryNodeSwitch")
    assert switch.input_type == "RGBA"
    assert switch.inputs["True"].links[0].from_node.bl_idname == "NodeGroupInput"
    assert switch.outputs[0].links[0].to_node.bl_idname == "NodeGroupOutput"


def test_inference_skips_values_that_cannot_decide():
    """None, a node with no outputs and other objects leave the type to the
    rest of the values; a raw bpy node counts as its first output."""
    from nodebpy.builder._infer import _source_socket, infer_data_type

    with g.tree():
        viewer = g.Viewer()  # no outputs to link from
        assert _source_socket(viewer) is None
        assert _source_socket(None) is None
        cube = g.Cube().node  # a raw bpy node
        assert _source_socket(cube).name == "Mesh"
        assert g.Switch(False, cube, g.Cone()).input_type == "GEOMETRY"
        assert g.IndexSwitch(items=[g.Value(), None]).data_type == "FLOAT"
    assert infer_data_type("Switch", [object(), (1, 2)], keyword="input_type") == (
        "FLOAT"
    )
