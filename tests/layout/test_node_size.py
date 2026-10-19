"""The size of a node and the heights of its sockets, estimated from the
rows it draws (``nodebpy.layout.node_size``)."""

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.layout.node_size import (
    HEADER,
    PROPERTY_ROW,
    SOCKET_ROW,
    VECTOR_EXPANDED,
    calculate_node_dimensions,
    calculate_socket_offset_y,
    get_bottom,
    get_top,
    node_property_rows,
    node_rows,
)


def _node(idname: str) -> bpy.types.Node:
    tree = bpy.data.node_groups.new("NodeSize", "GeometryNodeTree")
    return tree.nodes.new(idname)


def _enabled(sockets) -> list:
    return [socket for socket in sockets if socket.enabled]


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------


def test_node_with_more_sockets_is_taller():
    _, value_height = calculate_node_dimensions(_node("ShaderNodeValue"))
    _, set_position_height = calculate_node_dimensions(_node("GeometryNodeSetPosition"))
    assert 0 < value_height < set_position_height


def test_hidden_sockets_take_a_row_only_when_linked():
    with TreeBuilder("HiddenSockets", arrange=None) as tree:
        geo = tree.inputs.geometry()
        geo >> g.SetPosition() >> tree.outputs.geometry()
    node = tree.tree.nodes["Set Position"]

    full = calculate_node_dimensions(node)[1]
    for socket in node.inputs:
        if not socket.is_linked:
            socket.hide = True
    reduced = calculate_node_dimensions(node)[1]
    assert reduced == pytest.approx(HEADER + SOCKET_ROW)
    assert reduced < full

    for socket in node.inputs:
        socket.hide = True
    assert calculate_node_dimensions(node)[1] == reduced


# ---------------------------------------------------------------------------
# Socket offsets
# ---------------------------------------------------------------------------


def test_outputs_are_above_inputs():
    node = _node("ShaderNodeMath")
    outputs = [calculate_socket_offset_y(s) for s in _enabled(node.outputs)]
    inputs = [calculate_socket_offset_y(s) for s in _enabled(node.inputs)]

    assert all(offset < 0 for offset in outputs + inputs)
    assert max(inputs) < min(outputs)


def test_aligned_output_shares_the_row_of_its_input():
    """Set Position draws its Geometry output on the row of its Geometry
    input, above the other inputs."""
    node = _node("GeometryNodeSetPosition")
    geometry_out = calculate_socket_offset_y(node.outputs["Geometry"])
    inputs = [calculate_socket_offset_y(s) for s in _enabled(node.inputs)]

    assert geometry_out == inputs[0]
    assert all(offset < geometry_out for offset in inputs[1:])


def test_inputs_are_ordered_top_to_bottom_within_the_node():
    node = _node("GeometryNodeSetPosition")
    height = calculate_node_dimensions(node)[1]
    offsets = [calculate_socket_offset_y(s) for s in _enabled(node.inputs)]

    assert offsets == sorted(offsets, reverse=True)
    assert len(set(offsets)) == len(offsets)
    assert all(-height < offset < -HEADER for offset in offsets)


def _collapsed_math(linked_inputs: int) -> bpy.types.Node:
    """A collapsed Math node (Add: two inputs, one output), with that many
    of its inputs linked."""
    tree = bpy.data.node_groups.new("Collapsed", "GeometryNodeTree")
    math = tree.nodes.new("ShaderNodeMath")
    for socket in _enabled(math.inputs)[:linked_inputs]:
        tree.links.new(tree.nodes.new("ShaderNodeValue").outputs[0], socket)
    math.hide = True
    return math


def test_collapsed_node_has_a_row_of_10_per_visible_socket_plus_8():
    """Its sockets are 10 apart around its middle."""
    math = _collapsed_math(linked_inputs=1)
    first, second = _enabled(math.inputs)

    assert calculate_node_dimensions(math) == (140.0, 10 * 2 + 8)
    assert calculate_socket_offset_y(first) == -9
    assert calculate_socket_offset_y(second) == -19
    assert calculate_socket_offset_y(math.outputs[0]) == -14

    wide = _node("ShaderNodeMix")
    wide.hide = True
    visible = len(_enabled(wide.inputs))
    assert visible > 2
    assert calculate_node_dimensions(wide)[1] == 10 * visible + 8


def test_collapsed_node_counts_hidden_sockets_only_when_linked():
    math = _collapsed_math(linked_inputs=1)
    first, second = _enabled(math.inputs)
    first.hide = second.hide = True

    # One visible input and one output: the minimum of two rows.
    assert calculate_node_dimensions(math) == (140.0, 10 * 2 + 8)
    assert calculate_socket_offset_y(first) == -14


def test_collapsed_node_is_drawn_around_a_point_10_below_its_location():
    math = _collapsed_math(linked_inputs=0)
    math.location = (0.0, 100.0)
    assert (get_top(math), get_bottom(math)) == (100.0 - 10 + 14, 100.0 - 10 - 14)


# ---------------------------------------------------------------------------
# The rows a node draws
# ---------------------------------------------------------------------------


def test_set_position_draws_four_input_rows():
    """The Geometry output shares the Geometry input's row, and the
    unlinked Offset vector adds its three value rows."""
    node = _node("GeometryNodeSetPosition")
    rows = node_rows(node)

    assert [r.kind for r in rows] == ["input"] * 4
    assert rows[0].socket.name == "Geometry" and rows[0].partner.name == "Geometry"
    assert calculate_socket_offset_y(node.outputs["Geometry"]) == rows[0].anchor
    assert calculate_node_dimensions(node)[1] == pytest.approx(
        HEADER + 4 * SOCKET_ROW + VECTOR_EXPANDED
    )


def test_property_rows_leave_out_what_blender_does_not_draw():
    with TreeBuilder("RowModel", arrange=None) as tree:
        sim = g.SimulationZone({"cube": g.Cube()})
        vec = g.Vector((1.0, 2.0, 3.0))
        sim.output >> tree.outputs.geometry()

    assert node_property_rows(sim.input.node) == []
    assert node_property_rows(sim.output.node) == []
    assert node_property_rows(tree.tree.nodes["Group Output"]) == []
    ((vector, rows),) = node_property_rows(vec.node)
    assert vector.identifier == "vector" and rows == 3


def test_menu_switch_rows_follow_its_declaration():
    """Output, the data-type dropdown, Menu, then one row per item holding
    both its value input and its output."""
    with TreeBuilder("Declared", arrange=None):
        switch = g.MenuSwitch(data_type="BOOLEAN")
        switch.items.new(True, "A")
        switch.items.new(False, "B")
        node = switch.node

    rows = node_rows(node)
    summary = [
        (r.kind, r.socket.name if r.socket else r.prop.identifier, bool(r.partner))
        for r in rows
    ]
    assert summary == [
        ("output", "Output", False),
        ("property", "data_type", False),
        ("input", "Menu", False),
        ("input", "A", True),
        ("input", "B", True),
        ("input", "", False),  # the extend socket
    ]
    assert rows[3].partner.name == "A" and rows[3].partner.is_output
    assert calculate_socket_offset_y(node.outputs["A"]) == rows[3].anchor
    assert calculate_node_dimensions(node)[1] == pytest.approx(
        HEADER + 5 * SOCKET_ROW + PROPERTY_ROW
    )


def test_zone_output_node_pairs_each_item_input_with_its_output():
    with TreeBuilder("ZoneRows", arrange=None):
        rep = g.RepeatZone()
        rep.input >> g.SetPosition() >> rep.output

    geometry = [
        r
        for r in node_rows(rep.output.node)
        if r.socket is not None and r.socket.name == "Geometry"
    ]
    assert len(geometry) == 1 and geometry[0].partner is not None


def test_closed_panel_is_one_row_hiding_its_sockets():
    with TreeBuilder.shader("DeclaredShader") as shader_tree:
        bsdf = s.PrincipledBSDF()
        bsdf >> shader_tree.outputs.shader("Shader")

    def subsurface_weight():
        return [
            r
            for r in node_rows(bsdf.node)
            if r.socket is not None and r.socket.name == "Subsurface Weight"
        ]

    kinds = [
        (r.kind, r.panel if r.kind == "panel" else None, r.open)
        for r in node_rows(bsdf.node)
    ]
    assert kinds[0] == ("output", None, True)
    assert ("panel", "Subsurface", False) in kinds
    assert subsurface_weight() == []

    for state in bsdf.node.panel_states:
        state.is_collapsed = False
    (row,) = subsurface_weight()
    assert row.depth == 1


def test_group_node_draws_its_interface_panels():
    """A closed panel is one header row, and a linked socket in it attaches
    at that header; an open panel is a header row above its sockets."""
    with TreeBuilder("Panelled", arrange=None) as inner:
        geo = inner.inputs.geometry()
        with inner.inputs.panel("Shape", default_closed=True):
            inner.inputs.float("Radius", 1.0)
            inner.inputs.float("Depth", 2.0)
        with inner.inputs.panel("Colour"):
            inner.inputs.boolean("Flat", False)
        geo >> inner.outputs.geometry()

    with TreeBuilder("Outer", arrange=None) as outer:
        group = g.Group()
        group.node.node_tree = inner.tree
        outer.inputs.float("Value", 0.5) >> group.node.inputs["Depth"]
        node = group.node

    kinds = [(r.kind, getattr(r.panel, "name", None), r.open) for r in node_rows(node)]
    assert kinds == [
        ("output", None, True),
        ("property", None, True),
        ("input", None, True),  # Geometry
        ("panel", "Shape", False),
        ("panel", "Colour", True),
        ("input", None, True),  # Flat
    ]
    _, height = calculate_node_dimensions(node)
    assert height == pytest.approx(HEADER + 5 * SOCKET_ROW + PROPERTY_ROW)
    shape_row = node_rows(node)[3]
    assert [s.name for s in shape_row.collapsed_sockets] == ["Depth"]
    assert calculate_socket_offset_y(node.inputs["Depth"]) == shape_row.anchor
    # Radius is not drawn: it counts as at the node's header.
    assert calculate_socket_offset_y(node.inputs["Radius"]) == pytest.approx(
        -HEADER / 2
    )

    for state in node.panel_states:
        state.is_collapsed = False
    assert [r.kind for r in node_rows(node)].count("input") == 4
