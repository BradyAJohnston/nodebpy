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


# ---------------------------------------------------------------------------
# Frames
# ---------------------------------------------------------------------------


def _framed_tree(name: str) -> TreeBuilder:
    with TreeBuilder(name, arrange=None) as tree:
        x = tree.inputs.float("X")
        with g.Frame("Outer") as outer:
            a = x + 1.0
            with g.Frame("Inner", shrink=False, label_size=32).props(
                color="#336699", width=333, height=222
            ):
                a * 2.0 >> tree.outputs.float("Out")
            g.Frame("Empty in outer").props(width=300, height=150)
        g.Frame("Top empty").props(color="#FF0000")
        with g.Frame("Holder"):
            g.Frame("Held")
    assert outer.node.label == "Outer"
    return tree


def _frames(tree) -> dict:
    return {n.label: n for n in tree.nodes if n.bl_idname == "NodeFrame"}


def test_frame_settings_and_empty_frames_round_trip():
    tree = _framed_tree("FramesRoundTrip")
    text = bpy.data.texts.new("FramesRoundTripNote")
    _frames(tree.tree)["Inner"].text = text

    code = to_python(tree, snapshot_positions=True, format=False)
    assert (
        'with g.Frame("Inner", shrink=False, text=bpy.data.texts.get('
        '"FramesRoundTripNote"), label_size=32).props(color="#336699", '
        "width=333.0, height=222.0):" in code
    )
    assert 'g.Frame("Empty in outer").props(width=300.0, height=150.0)' in code

    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    frames = _frames(ns["tree"].tree)
    assert sorted(frames) == [
        "Empty in outer",
        "Held",
        "Holder",
        "Inner",
        "Outer",
        "Top empty",
    ]
    inner = frames["Inner"]
    assert not inner.shrink
    assert inner.label_size == 32
    assert inner.text == text
    assert tuple(inner.color) == pytest.approx((0.2, 0.4, 0.6))
    assert (inner.width, inner.height) == (333, 222)
    assert (frames["Empty in outer"].width, frames["Empty in outer"].height) == (
        300,
        150,
    )
    assert frames["Top empty"].use_custom_color
    parents = {
        label: frame.parent.label if frame.parent else None
        for label, frame in frames.items()
    }
    assert parents == {
        "Outer": None,
        "Inner": "Outer",
        "Empty in outer": "Outer",
        "Top empty": None,
        "Holder": None,
        "Held": "Holder",
    }


def test_shrinking_frame_size_is_not_written():
    """A frame fitting itself around its nodes gets its size from them."""
    with TreeBuilder("FramesShrink", arrange=None) as tree:
        x = tree.inputs.float("X")
        with g.Frame("Fit") as frame:
            x + 1.0 >> tree.outputs.float("Out")
    frame.node.width = 400
    assert 'with g.Frame("Fit"):' in to_python(tree, format=False)


# ---------------------------------------------------------------------------
# Gizmo pins
# ---------------------------------------------------------------------------


def test_pin_gizmo_pins_the_socket_blender_reads():
    """A value node's pin is on its output; a gizmo node's on its first
    input."""
    with TreeBuilder("PropsPin", arrange=None) as tree:
        value = g.Value(1.0).props(pin_gizmo=True)
        gizmo = g.LinearGizmo(value).props(pin_gizmo=True)
        g.SetPosition(offset=g.CombineXYZ(z=value)) >> tree.outputs.geometry("Out")
    assert value.node.outputs[0].pin_gizmo
    assert gizmo.node.inputs[0].pin_gizmo


def test_pin_gizmo_round_trips():
    from nodebpy.builder import CustomGeometryGroup

    class Lift(CustomGeometryGroup):
        _name = "PropsPinLift"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            amount = tree.inputs.float("Amount")
            tilt = tree.inputs.float("Tilt")
            g.LinearGizmo(amount)
            g.LinearGizmo(tilt)
            (
                geo
                >> g.SetPosition(offset=g.CombineXYZ(z=amount))
                >> tree.outputs.geometry("Geometry")
            )

    with TreeBuilder("PropsPinRoundTrip", arrange=None) as tree:
        value = g.Value(2.0).props(pin_gizmo=True)
        g.LinearGizmo(value).props(pin_gizmo=True)
        lift = Lift(Amount=value).props(pin_gizmo_inputs=["Tilt"])
        lift >> tree.outputs.geometry("Out")
    assert lift.node.inputs["Tilt"].pin_gizmo

    code = to_python(tree, format=False)
    assert code.count(".props(pin_gizmo=True)") == 2
    assert '.props(pin_gizmo_inputs=["Tilt"])' in code

    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    rebuilt = ns["tree"].tree
    nodes = {n.bl_idname: n for n in rebuilt.nodes}
    assert nodes["ShaderNodeValue"].outputs[0].pin_gizmo
    assert nodes["GeometryNodeGizmoLinear"].inputs[0].pin_gizmo
    group = nodes["GeometryNodeGroup"]
    assert group.inputs["Tilt"].pin_gizmo
    assert not group.inputs["Amount"].pin_gizmo
