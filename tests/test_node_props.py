"""``.props(...)``: setting the properties every node has while writing a
tree, and ``to_python`` writing them back."""

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.export import to_python


def test_props_sets_node_properties_and_returns_the_node():
    with TreeBuilder("PropsSet", arrange=None) as tree:
        geo = tree.inputs.geometry("G")
        node = g.SetPosition(geometry=geo)
        node >> tree.outputs.geometry("Out")
        returned = node.props(
            label="Lift",
            color="#FFAA00",
            width=200,
            hide=True,
            show_options=False,
            hide_inputs=["Selection"],
            mute=True,
            warning_propagation="ERRORS",
        )

    assert returned is node
    bl = node.node
    assert bl.label == "Lift"
    assert bl.use_custom_color
    assert tuple(round(c, 3) for c in bl.color) == (1.0, 0.667, 0.0)
    assert bl.width == 200
    assert bl.hide
    assert not bl.show_options
    assert bl.inputs["Selection"].hide
    assert bl.mute
    assert bl.warning_propagation == "ERRORS"


def test_props_on_a_socket_sets_its_node_and_returns_the_socket():
    with TreeBuilder("PropsSocket", arrange=None) as tree:
        x = tree.inputs.float("X")
        value = x + 1.0
        returned = value.props(label="Offset", color=(0.0, 0.5, 1.0))
        returned >> tree.outputs.float("Out")

    assert returned is value
    assert value.node.label == "Offset"
    assert tuple(value.node.color) == pytest.approx((0.0, 0.5, 1.0))


def test_props_hide_inputs_counts_visible_repeats():
    """``"Value#1"`` is the second *visible* Value input."""
    with TreeBuilder("PropsRepeat", arrange=None) as tree:
        x = tree.inputs.float("X")
        math = g.Math.add(x, 1.0).props(hide_inputs=["Value#1"])
        math >> tree.outputs.float("Out")
    hidden = [s.hide for s in math.node.inputs if s.enabled]
    assert hidden == [False, True]


def test_props_hide_outputs():
    """Blender won't hide a linked socket, so only unlinked outputs hide."""
    with TreeBuilder("PropsOutputs", arrange=None) as tree:
        x = tree.inputs.vector("V")
        separate = g.SeparateXYZ(x).props(hide_outputs=["Y", "Z"])
        separate.o.x >> tree.outputs.float("Out")
    assert [s.hide for s in separate.node.outputs] == [False, True, True]


def test_props_rejects_unknown_sockets_and_colors():
    with TreeBuilder("PropsBad", arrange=None):
        node = g.SetPosition()
        with pytest.raises(ValueError, match="no input socket 'Nope'"):
            node.props(hide_inputs=["Nope"])
        with pytest.raises(ValueError, match="hex colour"):
            node.props(color="orange")


def test_to_python_writes_props_and_rebuilds_them():
    with TreeBuilder("PropsRoundTrip", arrange=None) as tree:
        x = tree.inputs.float("X")
        geo = tree.inputs.geometry("G")
        offset = (x * 2.0).props(label="Double", hide=True)
        node = g.SetPosition(geometry=geo, offset=g.CombineXYZ(z=offset))
        node >> tree.outputs.geometry("Out")
    bl = node.node
    bl.use_custom_color = True
    bl.color = (0.2, 0.4, 0.6)
    bl.width = 220
    bl.inputs["Selection"].hide = True
    bl.mute = True

    code = to_python(tree, format=False)
    assert '.props(label="Double", hide=True)' in code
    assert (
        '.props(color="#336699", width=220.0, hide_inputs=["Selection"], mute=True)'
        in code
    )

    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    rebuilt = ns["tree"].tree
    math = next(n for n in rebuilt.nodes if n.bl_idname == "ShaderNodeMath")
    assert math.label == "Double" and math.hide
    set_pos = next(n for n in rebuilt.nodes if n.bl_idname == "GeometryNodeSetPosition")
    assert tuple(set_pos.color) == pytest.approx((0.2, 0.4, 0.6))
    assert set_pos.width == 220
    assert set_pos.inputs["Selection"].hide
    assert set_pos.mute


def test_to_python_writes_nothing_for_default_props():
    with TreeBuilder("PropsNone", arrange=None) as tree:
        x = tree.inputs.float("X")
        g.Math.add(x, 1.0) >> tree.outputs.float("Out")
    assert ".props(" not in to_python(tree, format=False)


def _collapsed_tree(name: str, expand_one: bool = False) -> TreeBuilder:
    with TreeBuilder(name, arrange=None) as tree:
        x = tree.inputs.float("X")
        a = x + 1.0
        (a * 2.0) >> tree.outputs.float("Out")
    for node in tree.tree.nodes:
        if node.bl_idname not in ("NodeGroupInput", "NodeGroupOutput"):
            node.hide = True
    if expand_one:
        a.node.hide = False
    return tree


def test_to_python_collapses_the_tree_when_every_node_is_collapsed():
    """Group Input/Output stay expanded: the builder makes them itself, so
    ``collapse`` doesn't reach them."""
    tree = _collapsed_tree("PropsAllCollapsed")
    code = to_python(tree, format=False)
    assert 'TreeBuilder("PropsAllCollapsed", collapse=True)' in code
    assert "hide" not in code

    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    for node in ns["tree"].tree.nodes:
        assert node.hide == (
            node.bl_idname not in ("NodeGroupInput", "NodeGroupOutput")
        )


def test_to_python_collapses_nodes_one_by_one_when_any_is_expanded():
    tree = _collapsed_tree("PropsMostlyCollapsed", expand_one=True)
    code = to_python(tree, format=False)
    assert "collapse=True" not in code
    assert code.count(".props(hide=True)") == 1


def test_to_python_group_class_sets_collapse():
    tree = _collapsed_tree("PropsCollapsedClass")
    code = to_python(tree, format=False, top_level="class")
    assert "tree.collapse = True" in code
    assert ".props(hide=True)" not in code


def test_to_python_leaves_group_node_options_alone():
    """A group node added in the editor shows its options; nodebpy builds
    them hidden, and that isn't written as a difference."""
    from nodebpy.builder import CustomGeometryGroup

    class Passthrough(CustomGeometryGroup):
        _name = "PropsPassthrough"

        def _build_group(self, tree):
            tree.inputs.geometry("G") >> tree.outputs.geometry("G")

    with TreeBuilder("PropsGroupOptions", arrange=None) as tree:
        group = Passthrough()
    group.node.show_options = True
    assert ".props(" not in to_python(tree, format=False)
