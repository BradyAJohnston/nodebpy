import itertools
from typing import cast

import bpy
import pytest
from numpy import random

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import (
    BooleanSocketGrid,
    BooleanSocketList,
    ColorSocketList,
    FloatSocket,
    FloatSocketGrid,
    FloatSocketList,
    GeometrySocket,
    IntegerSocket,
    IntegerSocketGrid,
    IntegerSocketList,
    MatrixSocket,
    MatrixSocketList,
    MenuSocketList,
    RotationSocketList,
    StringSocket,
    StringSocketList,
    VectorSocket,
    VectorSocketGrid,
    VectorSocketList,
)
from nodebpy.nodes.geometry import SplitString


def test_capture_attribute():
    with TreeBuilder("TestCaptureAttribute") as tree:
        cube = g.Cube()
        cap = g.CaptureAttribute.edge()

        _ = (
            cube
            >> cap
            >> g.SetPosition(offset=(0, 0, 10))
            >> g.SetPosition(position=cap.capture(g.Position()))
        )

    assert "Capture Attribute" in tree.nodes
    assert len(cap._items) == 1
    assert cap.node.outputs[-2].name == "Position"
    assert cap.node.outputs[-2].type == "VECTOR"
    assert cap.i.position.links
    assert len(cap.i.position.links) == 1
    assert cap.i.position.links[0].from_node.bl_idname == g.Position._bl_idname

    with TreeBuilder() as tree:
        cap = g.Points(
            count=10, position=g.RandomValue.vector(), radius=g.RandomValue.float()
        ) >> g.CaptureAttribute.point(
            items={
                "Position": g.Position(),
                "Radius": g.Radius(),
                "Normal": g.Normal(),
            }
        )
        assert len(cap.node.capture_items) == 3
        assert cap.i.normal.links[0].from_node.bl_idname == "GeometryNodeInputNormal"
        assert (
            cap.i.position.links[0].from_node.bl_idname == "GeometryNodeInputPosition"
        )


def test_join_geometry():
    with g.tree() as tree:
        items = [g.Cube(), g.UVSphere(), g.Cone(), g.Cylinder(), g.Grid()]
        join = g.JoinGeometry(items)

    assert "Join Geometry" in tree.nodes
    assert len(join.node.inputs["Geometry"].links) == 5
    # links to join geometry are created in reverse order but we internally reverse them back
    assert join._default_input_socket.links[0].from_node == items[0].node


def test_socket_selection():
    with g.tree("AnotherTree"):
        pos = g.SetPosition()
        vec = g.Vector()

        vec >> pos.i.offset
        g.Position() * 1.0 >> pos.i.position

    assert pos.i.offset.socket.name == "Offset"
    assert vec.o.vector.socket.links[0].to_socket.node == pos.node
    assert vec.o.vector.socket.links[0].to_socket == pos.i.offset.socket
    assert len(pos.i.offset.socket.links) == 1


class TestMathOperators:
    @pytest.mark.parametrize(
        "operator,input",
        list(
            itertools.product(
                ["+", "-", "*", "/"],
                [g.Vector, g.Value],
            )
        ),
    )
    def test_math_operators(self, operator, input):
        with TreeBuilder("TestMathOperators"):
            set_pos = g.SetPosition()
            pos = g.Position()  # noqa: F841

            eval(f"input() {operator} 1.0 {operator} pos >> set_pos")

        assert len(set_pos.i.offset.links) == 0
        assert len(set_pos.i.geometry.links) == 0
        assert len(set_pos.i.position.links) == 1


def test_format_string():
    str_to_format = "Hello {x} friends, it is {y} hours and this is a {String}"
    with TreeBuilder("TestFormatString"):
        x_int = g.Integer(5)
        y_value = g.Value(12.50)
        format = g.FormatString(
            str_to_format,
            items={
                "String": g.String("test"),
                "x": x_int,
                "y": y_value,
            },
        )

        assert len(format.node.format_items) == 3
        assert format.i[0].default_value == str_to_format  # type: ignore
        i_string: StringSocket = format.i[1]  # ty: ignore[invalid-assignment]
        assert i_string.name == "String"
        assert i_string.type == "STRING"
        assert i_string.default_value == ""
        assert format.i[2].name == "x"
        assert isinstance(format.i[2], IntegerSocket)
        assert format.i[2].default_value == 0
        assert format.i[3].name == "y"
        assert isinstance(format.i[3], FloatSocket)
        assert format.i[3].default_value == 0.0
        assert format.items["String"].socket == format.i[1].socket
        assert format.items["x"].socket == format.i[2].socket
        assert format.items["y"].socket == format.i[3].socket


def test_field_to_grid():
    with TreeBuilder() as tree:
        # the rotation value should add a vector item as the next available compatible data type
        inputs = [g.Vector(), g.Value(), g.Boolean(), g.Integer(), g.Rotation()]
        items = {i.name: i for i in inputs}
        items["test"] = g.Value()

        ftg = g.FieldToGrid(items=items)
        math = g.Math.add()
        _ = ftg.o["test"] >> math

        ftg2 = g.FieldToGrid(items={"test_value": 0.3})
        assert ftg2.i["test_value"].socket.default_value == pytest.approx(0.3)

    assert len(tree) == 9
    assert len(ftg.node.grid_items) == 6
    assert ftg.node.grid_items[5].name == "test"
    assert ftg.o["test"].socket.links[0].to_socket.node == math.node
    assert all(
        [i._default_output_socket.links[0].to_socket.node == ftg.node for i in inputs]
    )
    for item, type in zip(
        ftg.node.grid_items, ["VECTOR", "FLOAT", "BOOLEAN", "INT", "VECTOR", "FLOAT"]
    ):
        assert item.data_type == type

    with TreeBuilder() as tree:
        grid = g.VolumeCube(g.NoiseTexture()) >> g.GetNamedGrid(name="density")
        ftg = g.FieldToGrid.vector(grid, {"Color": g.NoiseTexture().o.color})

    assert ftg.data_type == "VECTOR"
    assert len(ftg.node.grid_items) == 1
    assert ftg.i.topology.socket.links[0].from_node == grid.node
    assert ftg.i.topology.socket.links[0].from_socket == grid.o.grid.socket
    assert ftg.i["Color"].socket.links[0].from_node.name == "Noise Texture.001"

    with TreeBuilder() as tree:
        nt = g.NoiseTexture()
        ftg = g.FieldToGrid(g.CubeGridTopology().o.topology)
        pos, vec, fac = (
            item.output
            for item in ftg.add_items(
                {"position": g.Position(), "vec": nt.o.color, "fac": nt.o.fac}
            ).values()
        )
        assert len(ftg.o) == 4
        assert isinstance(pos, VectorSocketGrid)
        assert pos.name == "position"
        assert isinstance(vec, VectorSocketGrid)
        assert vec.name == "vec"
        assert isinstance(nt.o.fac, FloatSocket)
        assert fac.name == "fac"
        assert isinstance(fac, FloatSocketGrid)
        assert fac.name == "fac"


def test_field_variance():
    with g.tree():
        var = g.FieldVariance.edge.float(
            g.SplineParameter().o.length, g.CurveOfPoint().o.curve_index
        )
        assert var.data_type == "FLOAT"
        assert var.domain == "EDGE"
        var.domain = "POINT"
        assert var.domain == "POINT"


def test_color_socket_domain_field_evaluation():
    """ColorSocket exposes the per-domain field-evaluation accessors, each
    building a colour EvaluateAtIndex node."""
    from nodebpy.builder import ColorSocket

    with g.tree():
        col = g.NamedAttribute.color("c").o.attribute
        assert isinstance(col, ColorSocket)
        for domain in (
            "point",
            "edge",
            "face",
            "corner",
            "spline",
            "instance",
            "layer",
        ):
            result = getattr(col, domain).at(0)
            assert isinstance(result, ColorSocket)
            assert result.builder_node.node.data_type == "FLOAT_COLOR"


def test_geometry_to_instance():
    with TreeBuilder() as tree:
        inputs = [g.Cube(), g.UVSphere(), g.IcoSphere(), g.Cone()]
        gti = g.GeometryToInstance(*inputs)

    assert len(tree) == 5
    assert len(gti.node.inputs[0].links) == 4
    assert gti._default_input_socket.links[2].from_node == inputs[2].node
    assert gti._default_input_socket.links[1].from_node == inputs[1].node


def test_get_named_grid(snapshot):
    with TreeBuilder() as tree:
        gng = g.GetNamedGrid(name="density")
        (
            g.VolumeCube()
            >> gng
            >> g.FieldToGrid.float(
                items={"Position": g.Position(), "value": g.Position() * 2 + 10}
            )
        )

        assert gng.data_type == "FLOAT"
        gng.data_type = "INT"
        assert gng.data_type == "INT"

    assert snapshot == tree._repr_markdown_()


def test_advect_grid():
    with TreeBuilder():
        grid = g.GetNamedGrid(g.VolumeCube(), name="density")
        ftg = g.FieldToGrid(
            grid,
            {"Position": g.Position()},
        )

        ag = grid >> g.AdvectGrid(
            velocity=ftg, time_step=g.Value(0.1), integration_scheme="Midpoint"
        )

    assert ftg.i.topology.socket.links[0].from_socket == grid.o.grid.socket
    assert len(grid.o.volume.socket.links) == 0
    assert ag.i.integration_scheme.socket.default_value == "Midpoint"


def test_grid_node_data_type_setters():
    with TreeBuilder():
        grid = g.GetNamedGrid(g.VolumeCube(), name="density")

        adv = g.AdvectGrid(grid)
        assert adv.data_type == "FLOAT"
        adv.data_type = "VECTOR"
        assert adv.data_type == "VECTOR"

        clip = g.ClipGrid(grid)
        assert clip.data_type == "FLOAT"
        clip.data_type = "INT"
        assert clip.data_type == "INT"


def test_duplicate_elements_domain_setter():
    with TreeBuilder():
        geo = g.IcoSphere()
        node = g.DuplicateElements(geo)
        assert node.domain == "POINT"
        node.domain = "EDGE"
        assert node.domain == "EDGE"


def test_sdf_grid_boolean():
    with TreeBuilder() as tree:
        trio = [g.PointsToSDFGrid() for _ in range(3)]
        bool1 = g.SDFGridBoolean.difference(
            g.GetNamedGrid(g.VolumeCube(), name="density"),
            trio,
        )
        bool2 = g.SDFGridBoolean.intersect(trio)
        bool3 = g.SDFGridBoolean.union(trio)

    assert len(tree) == 8
    assert (
        bool1.i.grid_1.socket.links[0].from_node.bl_idname == "GeometryNodeGetNamedGrid"
    )
    assert len(bool1.i.grid_2.socket.links) == 3
    assert len(bool2.i.grid_2.socket.links) == 3
    assert len(bool3.i.grid_2.socket.links) == 3


@pytest.mark.parametrize(
    "domain,output",
    list(
        zip(
            ["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"],
            [
                "Point Count",
                "Point Count",
                "Point Count",
                "Instance Count",
                "Layer Count",
            ],
        )
    ),
)
def test_domain_size(domain, output):
    with TreeBuilder() as tree:
        domain_size = g.DomainSize(g.Points(10), component=domain)
        domain_size >> g.Points()

    assert len(tree) == 3
    assert len(domain_size.node.outputs[output].links) == 1


def test_curve_handle():
    with TreeBuilder():
        node = g.HandleTypeSelection(left=False, right=False)
        assert not node.left
        assert not node.right
        node.left = True
        assert node.left
        node.right = True
        assert node.right
        node = g.HandleTypeSelection(left=False, right=True)
        assert not node.left
        assert node.right
        node = g.HandleTypeSelection(left=True, right=True)
        assert node.left
        assert node.right
        node = g.HandleTypeSelection(left=True, right=False)
        assert node.left
        assert not node.right


def test_bake():
    with TreeBuilder() as tree:
        bake = g.Bake(
            g.Points(10),
            g.Position(),
            g.Value() * g.Radius() + 10,
        )
        set_pos = bake >> g.SetPosition()

    assert len(tree) == 8
    assert len(bake.node.bake_items) == 3
    assert set_pos.node.inputs[0].links[0].from_node == bake.node
    assert set_pos.node.inputs[0].links[0].from_socket == bake.node.outputs[0]


def test_simulation(snapshot):
    with TreeBuilder() as tree:
        cube = g.Cube()
        sim = g.SimulationZone({"cube": cube})
        pos = sim.item("Position", g.Position())
        (pos.current + 0.1) >> pos.next
        offset = sim.delta_time * g.Vector((0, 0, 0.1)) * pos.current
        sim.input >> g.SetPosition(offset=offset) >> sim.output
        sim.output >> g.SetPosition(position=sim.output.o["Position"])
    assert len(sim.output.node.inputs["Skip"].links) == 0
    assert len(tree) == 11
    assert snapshot == tree._repr_markdown_()


def test_repeat(snapshot):
    with TreeBuilder() as tree:
        cube = g.Cube()
        zone = g.RepeatZone(10, {"cube": cube})
        input, output = zone
        assert input.node == zone[0].node
        assert output.node == zone[1].node
        with pytest.raises(IndexError):
            zone[2]
        pos_math = input.capture(g.Position()) * g.Position()
        _ = pos_math >> output
        _ = (
            input
            >> g.SetPosition(offset=zone.iteration * g.Vector((0, 0, 0.1)) * pos_math)
            >> output
        )
        _ = output >> g.SetPosition(position=output.o["Position"])
    assert len(tree) == 13
    assert len(input.items) == 2
    assert snapshot == tree._repr_markdown_()

    with TreeBuilder() as tree:
        zone = g.RepeatZone(5)
        join = g.JoinGeometry()
        zone.output.capture(join)
        zone.input >> join
        _ = (
            g.Points(
                zone.iteration,
                position=g.RandomValue.vector(min=-1, seed=zone.iteration),
            )
            >> join
        )
    assert all(
        [link.from_socket.type == "GEOMETRY" for link in join.node.inputs[0].links]
    )
    assert len(tree) == 7
    assert snapshot == tree._repr_markdown_()


def test_index_switch():
    with TreeBuilder() as tree:
        items = (g.Cube(), g.UVSphere(), g.Cube(), g.Cube())
        index = g.IndexSwitch.geometry(5, items)

        index2 = g.IndexSwitch.float(items=range(10))

    assert len(index.node.index_switch_items) == 4
    assert len(tree) == 6
    assert index.i.index.socket.default_value == 5
    assert index2.i[1].default_value == pytest.approx(0.0)
    assert index2.i[2].default_value == pytest.approx(1.0)
    assert index2.i[3].default_value == pytest.approx(2.0)


def test_menu_switch():
    with TreeBuilder() as tree:
        menu = tree.inputs.menu()
        items = {
            "Mesh": g.Cube(),
            "UVSphere": g.UVSphere(),
            "Cube": g.Cube(),
        }
        switch = g.MenuSwitch.geometry(items=items)
        menu >> switch
        menu.socket.default_value = "Mesh"

    assert switch.i.menu.socket.links[0].from_socket == menu.socket
    assert len(switch.node.enum_items) == 3

    with TreeBuilder() as tree:
        switch = g.MenuSwitch.float(items={f"Input_{i}": i for i in range(10)})

    assert len(switch.node.enum_items) == 10
    print(
        [
            (
                name,
                x.socket.default_value if hasattr(x.socket, "default_value") else None,
            )
            for name, x in switch.i._items()
        ]
    )
    assert switch.i["Input_5"].socket.default_value == 5


def test_menu_switch_menu_connection():
    with TreeBuilder("AnotherMenuSwitch"):
        switch = g.MenuSwitch.geometry(
            g.Switch.menu(),
            items={
                "cube": g.Cube(),
                "UVSphere": g.UVSphere(),
                "Cone": g.Cone(),
            },
        )
    assert switch.i["Menu"].links
    assert switch.i["Menu"].links[0].from_node.bl_idname == g.Switch._bl_idname
    assert switch.i["Menu"].links[0].from_node.input_type == "MENU"
    assert switch.i["Menu"].socket.default_value == "cube"


def test_menu_switch_menu_items_empty_default_deferred():
    """A MENU-typed MenuSwitch with string item values defers them to
    ``_menu_defaults`` (they can't be set until items are known), and empty
    string defaults are skipped when the defaults are applied on context exit."""
    with TreeBuilder("MenuOfMenus", arrange=None) as tree:
        switch = g.MenuSwitch.menu(items={"a": "", "b": ""})
        # the item menu sockets defer their (empty) string defaults
        assert len(tree._menu_defaults) == 2
        assert all(md.default == "" for md in tree._menu_defaults)
    # exiting the context applies the defaults; the empty strings are skipped
    # without error, and the enum items still exist
    assert len(switch.node.enum_items) == 2


def test_multi_menu():
    with TreeBuilder() as tree:
        items = (g.Cube(), g.IcoSphere(), g.Grid())

        menu = g.MenuSwitch.integer(items={"test": 0, "another": 1, "again": 2})
        switch1 = g.IndexSwitch.geometry(menu, items)
        switch2 = g.IndexSwitch.geometry(menu, reversed(items))

        menu_input = tree.inputs.menu()
        menu_input >> menu
        menu_input.default_value = "test"

        g.JoinGeometry([switch1, switch2]) >> tree.outputs.geometry("Output")


def test_switch_repeatzone(snapshot):
    with TreeBuilder() as tree:
        input = tree.inputs.geometry()
        output = tree.outputs.geometry()

        items = (g.Cube(), g.IcoSphere(), g.Grid())
        zone = g.RepeatZone(5, {"Geometry": input})
        switch = g.IndexSwitch.geometry(zone.iteration, items)
        join = g.JoinGeometry([zone.input, switch])
        join >> zone.output >> output

    assert len(zone.output.items) == 1
    assert zone.output.i["Geometry"].socket.links[0].from_node == join.node
    assert snapshot == tree._repr_markdown_()


def test_generate_select_group():
    with TreeBuilder() as tree:
        switch = g.IndexSwitch.boolean(
            g.NamedAttribute.integer("chain_id"),
            [tree.inputs.boolean(str(i)) for i in range(20)],
        )
        switch >> tree.outputs.boolean("Selection")

    assert len(switch.node.index_switch_items) == 20
    assert len(tree) == 4


def test_accumulate_field():
    with TreeBuilder() as tree:
        cube = g.Cube()
        aatr = g.AxisAngleToRotation(angle=1.0)
        tran = g.AccumulateField.point.transform(
            g.EvaluateAtIndex.point.quaternion(aatr, g.Index() - int(1))
        )
        _ = cube >> g.SetPosition(
            position=g.TransformPoint(g.Position(), tran.o.trailing),
            offset=g.FieldAverage.edge.vector(g.Position()),
        )

        g.SetPosition(offset=g.FieldVariance.point.vector(g.Position()))

    assert tree.nodes.get("Integer Math")
    assert tree.nodes.get("Accumulate Field").outputs["Trailing"].links[
        0
    ].to_node == tree.nodes.get("Transform Point")
    assert tree.nodes.get("Field Average").data_type == "FLOAT_VECTOR"
    assert tree.nodes.get("Field Average").domain == "EDGE"


def test_edge_other_point():
    with TreeBuilder(arrange="simple") as tree:
        v_index = tree.inputs.integer("Vertex Index", default_input="INDEX")
        e_index = tree.inputs.integer("Edge Number")

        # with the index from the selected edge from the input, we get the two different vertices
        # of the edge. We compare them and return the one that isn't the current input vertex index
        eov = g.EdgesOfVertex(v_index, sort_index=e_index)
        ev = g.EdgeVertices()
        vert_1 = g.EvaluateAtIndex.edge.integer(ev.o.vertex_index_1, eov)
        vert_2 = g.EvaluateAtIndex.edge.integer(ev.o.vertex_index_2, eov)
        other_vertex = g.Switch.integer(v_index == vert_1, vert_1, vert_2)

        _ = other_vertex >> tree.outputs.integer("Other Vertex")

    assert other_vertex.i[0].links[0].from_node
    assert other_vertex.i[0].links[0].from_node.bl_idname == g.Compare._bl_idname
    assert other_vertex.i[1].links[0].from_node == vert_1.node
    assert other_vertex.i[2].links[0].from_node == vert_2.node


def test_align_rotation_to_vector():
    """Ensure that it appropiately selects a vector or rotation socket"""
    with TreeBuilder() as tree:
        # this should select the vector input socket
        artv = g.RandomValue.vector() >> g.AlignRotationToVector()
        # this should select the rotation input socket
        artv2 = g.AxesToRotation() >> g.AlignRotationToVector()

    assert artv.i.vector.links[0].from_socket == tree.nodes["Random Value"].outputs[0]
    assert (
        artv2.i.rotation.links[0].from_socket
        == tree.nodes["Axes to Rotation"].outputs[0]
    )


def test_foreachgeometryelement_zone():
    with TreeBuilder() as tree:
        out = tree.outputs.geometry("Geometry")
        cube = g.Cube()
        zone = g.ForEachGeometryElementZone(
            cube,
            selection=g.Normal()
            >> g.VectorMath.dot_product(..., (0, 0, 1))
            >> g.Compare.float.greater_than(..., -0.1),
            domain="FACE",
        )
        pos = zone.input.capture(g.Position())
        norm = zone.input.capture(g.Normal())
        transformed = g.Cone() >> g.TransformGeometry(
            translation=pos,
            rotation=g.AlignRotationToVector(
                vector=norm + g.RandomValue.vector(min=-1, id=zone.index)
            ),
            scale=0.4,
        )
        zone.output.capture(pos)
        zone.output.capture_generated(pos)
        zone.output.capture_generated(transformed)
        _ = transformed >> zone.output
        _ = g.JoinGeometry([zone.output.o._get("Generation_0"), cube]) >> out

    input, output = zone
    with pytest.raises(IndexError):
        zone[2]

    assert all([i.socket_type == "VECTOR" for i in zone.input.items])
    assert len(zone.input.items) == 2
    assert len(zone.output.items) == 1
    assert zone.output.items[0].socket_type == "VECTOR"
    assert zone.output.node.inputs["Geometry"].links[0].from_node == transformed.node
    assert zone.input.node == input.node
    assert zone.output.node == output.node
    assert input.output == output.node
    assert input.i.selection.socket.links[0].from_node == tree.nodes["Compare"]
    assert tree.nodes["Compare"].data_type == "FLOAT"
    assert tree.nodes["Compare"].operation == "GREATER_THAN"
    assert len(zone.output.items_generated) == 3
    assert zone.output.items_generated[1].socket_type == "VECTOR"
    assert zone.output.items_generated[2].socket_type == "GEOMETRY"


def test_zone_capture_names_and_domains():
    with TreeBuilder():
        zone = g.ForEachGeometryElementZone(g.Cube(), domain="FACE")
        pos = zone.input.capture(g.Position(), name="MyPos")
        gen = zone.output.capture_generated(pos, name="MyGen", domain="FACE")
        assert zone.input.items[0].name == "MyPos"
        assert pos.name == "MyPos"
        assert zone.output.items_generated[1].name == "MyGen"
        assert zone.output.items_generated[1].domain == "FACE"
        assert gen.name == "MyGen"

        rzone = g.RepeatZone(3)
        val = rzone.input.capture(g.Value(), name="Counter")
        assert rzone.input.items[0].name == "Counter"
        assert rzone.input.items[0].socket_type == "FLOAT"
        assert val.name == "Counter"
        input, output = rzone
        assert input is rzone.input
        assert output is rzone.output
        with pytest.raises(IndexError):
            rzone[2]


def test_zone_item_handles():
    with TreeBuilder():
        zone = g.RepeatZone(10)
        value = zone.item("value", initial=1.0)
        _ = (value.current + 1.0) >> value.next
        assert zone.output.items[0].name == "value"
        assert zone.output.items[0].socket_type == "FLOAT"
        assert value.initial.socket.default_value == pytest.approx(1.0)
        assert value.current.socket.links[0].to_node.bl_idname == "ShaderNodeMath"
        assert value.next.socket.links[0].from_node.bl_idname == "ShaderNodeMath"
        assert value.result.socket.name == "value"

        # adding more items must not invalidate existing handles
        geo = zone.item("geo", type="GEOMETRY")
        vec = zone.item("vec", (1.0, 2.0, 3.0))
        assert value.name == "value"
        assert geo.socket_type == "GEOMETRY"
        assert len(geo.initial.socket.links) == 0
        assert vec.socket_type == "VECTOR"
        assert tuple(vec.initial.socket.default_value) == (1.0, 2.0, 3.0)

        with pytest.raises(TypeError):
            zone.item("nope")


def test_zone_items_declaration():
    with TreeBuilder():
        zone = g.SimulationZone({"geo": "GEOMETRY", "fac": g.Value()})
        assert [i.socket_type for i in zone.output.items] == ["GEOMETRY", "FLOAT"]
        assert len(zone.input.node.inputs[0].links) == 0
        assert len(zone.input.node.inputs[1].links) == 1

    with TreeBuilder():
        cap = g.CaptureAttribute(
            g.Cube(), items={"Pos": g.Position(), "Mask": "BOOLEAN"}
        )
        assert [i.data_type for i in cap.node.capture_items] == [
            "FLOAT_VECTOR",
            "BOOLEAN",
        ]
        assert len(cap.node.inputs["Pos"].links) == 1
        assert len(cap.node.inputs["Mask"].links) == 0


def test_foreach_item_handles():
    with TreeBuilder():
        zone = g.ForEachGeometryElementZone(g.Cube())
        pos = zone.item("Pos", g.Position())
        assert (
            pos.input.socket.links[0].from_node.bl_idname == "GeometryNodeInputPosition"
        )
        out = zone.main_item("Out", pos.output)
        assert out.input.socket.links[0].from_socket == pos.output.socket
        gen = zone.generated_item("Gen", g.Cone(), domain="FACE")
        assert gen.socket_type == "GEOMETRY"
        assert zone.output.items_generated[1].name == "Gen"
        unlinked = zone.generated_item("Mask", type="BOOLEAN", domain="FACE")
        assert zone.output.items_generated[2].domain == "FACE"
        defaulted = zone.generated_item("Weight", 0.5)
        assert zone.output.items_generated[3].socket_type == "FLOAT"
        assert defaulted.input.socket.default_value == pytest.approx(0.5)
        with pytest.raises(TypeError):
            zone.generated_item("nope")
        assert zone.output.domain == "POINT"
        assert len(unlinked.input.socket.links) == 0
        assert gen.name == "Gen"


def test_boolean_math_methods():
    with TreeBuilder(arrange="simple", collapse=True) as tree:
        _ = (
            g.Boolean()
            >> g.BooleanMath.not_and(..., True)
            >> g.BooleanMath.l_not()
            >> g.BooleanMath.nor()
            >> g.BooleanMath.not_equal()
            >> g.BooleanMath.imply()
        )
    assert len(tree) == 6


def test_integer_math_methods():
    with TreeBuilder(arrange=None) as tree:
        _ = (
            g.Integer(2444222)
            >> g.IntegerMath.divide_round(2)
            >> g.IntegerMath.divide_floor(3)
            >> g.IntegerMath.divide_ceiling(10)
            >> g.IntegerMath.floored_modulo(5)
            >> g.IntegerMath.modulo(2)
            >> g.IntegerMath.greatest_common_divisor(10)
            >> g.IntegerMath.least_common_multiple(15)
            >> g.IntegerMath.absolute()
        )

    assert len(tree) == 9


def test_math_methods():
    with TreeBuilder(arrange=None) as tree:
        _ = (
            g.Value(2.5)
            >> g.Math.add(3.5)
            >> g.Math.subtract(1.5)
            >> g.Math.multiply(2.5)
            >> g.Math.divide(4.5)
            >> g.Math.power(2)
            >> g.Math.logarithm(10)
            >> g.Math.square_root()
            >> g.Math.absolute()
            >> g.Math.square_root()
            >> g.Math.inverse_square_root()
            >> g.Math.absolute()
            >> g.Math.less_than(..., 1.5)
            >> g.Math.greater_than(..., 1.5)
            >> g.Math.sign()
            >> g.Math.smooth_minimum()
            >> g.Math.smooth_maximum()
            >> g.Math.round()
            >> g.Math.floored_modulo()
            >> g.Math.truncated_modulo()
            >> g.Math.floored_modulo()
            >> g.Math.wrap()
            >> g.Math.ping_pong()
            >> g.Math.sine()
            >> g.Math.hyperbolic_cosine()
            >> g.Math.hyperbolic_tangent()
            >> g.Math.hyperbolic_tangent()
            >> g.Math.to_radians()
            >> g.Math.to_degrees()
        )

    assert len(tree) == 29


def test_inputs():
    with TreeBuilder() as tree:
        cube = bpy.data.objects["Cube"]
        material = bpy.data.materials["Material"]
        object = g.ObjectInfo(g.Object(cube))
        set_material = g.SetMaterial(object, material=g.Material(material))
        coll = g.CollectionInfo(g.Collection(bpy.data.collections["Collection"]))

    assert len(tree) == 6
    assert object.i.object.socket.links[0].from_node.object == bpy.data.objects["Cube"]
    assert (
        set_material.i.material.socket.links[0].from_node.material
        == bpy.data.materials["Material"]
    )
    assert (
        coll.i.collection.links[0].from_node.collection
        == bpy.data.collections["Collection"]
    )


def test_has_inputs_registered():
    with g.tree():
        sp = g.SetPosition()
        assert hasattr(sp.i, "geometry")
        assert hasattr(sp.i, "offset")
        assert hasattr(sp.i, "position")
        assert hasattr(sp.i, "selection")
        assert hasattr(sp.o, "geometry")


def test_join_string():
    with g.tree():
        string = "abcdefg"
        letters = [g.String(x) for x in string]
        join = g.JoinStrings(letters)

    assert len(letters) == len(join.i.strings.links)


def test_mesh_boolean():
    with g.tree():
        meshes = [g.Cube(), g.IcoSphere() >> g.TransformGeometry(translation=0.2)]

        boolean = g.MeshBoolean.intersect(meshes)
        assert boolean.solver == "FLOAT"
        assert boolean.operation == "INTERSECT"
        boolean.solver = "EXACT"
        assert boolean.solver == "EXACT"
        bool2 = g.MeshBoolean.difference(g.Cone(), meshes, solver="EXACT")
        assert bool2.operation == "DIFFERENCE"
        assert bool2.solver == "EXACT"
        bool2.operation = "INTERSECT"
        assert bool2.operation == "INTERSECT"
        bool3 = g.MeshBoolean.intersect(meshes, False, g.Boolean(), solver="EXACT")
        assert len(bool3.i.mesh_2.links) == 2
        assert bool3.solver == "EXACT"
        assert bool3.operation == "INTERSECT"
        assert (
            bool3.i.hole_tolerant.links[0].from_node.bl_idname == g.Boolean._bl_idname
        )
        bool4 = g.MeshBoolean.union(meshes, self_intersection=True, solver="EXACT")
        assert len(bool4.i.mesh_2.links) == 2
        assert bool4.solver == "EXACT"
        assert bool4.i.self_intersection.default_value is True

    assert len(boolean.i.mesh_2.links) == 2
    assert len(bool2.i.mesh_2.links) == 2
    assert len(bool2.i.mesh_1.links) == 1


def set_handle_type_and_selection():
    with g.tree():
        sel = g.HandleTypeSelection(handle_type="VECTOR", right=False)
        assert sel.handle_type == "VECTOR"
        sel.handle_type = "ALIGN"
        assert sel.handle_type == "ALIGN"
        assert not sel.right
        assert sel.left
        sel.left = False
        sel.right = True
        assert not sel.left and sel.right

        sht = g.SetHandleType(left=False, handle_type="VECTOR")
        assert sht.handle_type == "VECTOR"
        assert not sht.left and sht.right
        sht.handle_type = "ALIGN"
        assert sht.handle_type == "ALIGN"
        sht.left = True
        sht.right = False
        assert sht.left and not sht.right


def test_compare_node_data_types():
    with g.tree():
        # --- string ---
        comp = g.Compare.string.equal("A", "B")
        assert comp.data_type == "STRING"
        assert comp.operation == "EQUAL"
        assert comp.i.a.default_value == "A"
        assert comp.i.b.default_value == "B"

        comp = g.Compare.string.not_equal("X", "Y")
        assert comp.data_type == "STRING"
        assert comp.operation == "NOT_EQUAL"
        assert comp.i.a.default_value == "X"
        assert comp.i.b.default_value == "Y"

        # --- float ---
        comp = g.Compare.float.less_than(1.0, 2.0)
        assert comp.data_type == "FLOAT"
        assert comp.operation == "LESS_THAN"
        assert comp.i.a.default_value == pytest.approx(1.0)
        assert comp.i.b.default_value == pytest.approx(2.0)

        comp = g.Compare.float.less_equal()
        assert comp.data_type == "FLOAT"
        assert comp.operation == "LESS_EQUAL"

        comp = g.Compare.float.greater_than()
        assert comp.operation == "GREATER_THAN"

        comp = g.Compare.float.greater_equal()
        assert comp.operation == "GREATER_EQUAL"

        comp = g.Compare.float.equal(1.0, 0.0)
        assert comp.operation == "EQUAL"
        assert comp.i.a.default_value == pytest.approx(1.0)

        comp = g.Compare.float.not_equal(3.0, 4.0)
        assert comp.operation == "NOT_EQUAL"
        assert comp.i.a.default_value == pytest.approx(3.0)
        assert comp.i.b.default_value == pytest.approx(4.0)

        # output socket
        assert comp.o.result.socket.type == "BOOLEAN"

        # --- integer ---
        comp = g.Compare.integer.less_than(1, 2)
        assert comp.data_type == "INT"
        assert comp.operation == "LESS_THAN"
        assert comp.i.a.default_value == 1
        assert comp.i.b.default_value == 2

        comp = g.Compare.integer.less_equal()
        assert comp.operation == "LESS_EQUAL"

        comp = g.Compare.integer.greater_than()
        assert comp.operation == "GREATER_THAN"

        comp = g.Compare.integer.greater_equal()
        assert comp.operation == "GREATER_EQUAL"

        comp = g.Compare.integer.equal(5, 5)
        assert comp.operation == "EQUAL"
        assert comp.i.a.default_value == 5

        comp = g.Compare.integer.not_equal()
        assert comp.operation == "NOT_EQUAL"

        # mutating data_type re-routes i.a / i.b
        comp.data_type = "FLOAT"
        assert comp.i.a.default_value == pytest.approx(0.0)
        comp.i.a.default_value = 7
        assert comp.i.a.default_value == pytest.approx(7.0)

        # --- vector ---
        comp = g.Compare.vector.less_than((1, 0, 0), (0, 1, 0))
        assert comp.data_type == "VECTOR"
        assert comp.operation == "LESS_THAN"

        comp = g.Compare.vector.less_equal()
        assert comp.operation == "LESS_EQUAL"

        comp = g.Compare.vector.greater_than()
        assert comp.operation == "GREATER_THAN"

        comp = g.Compare.vector.greater_equal()
        assert comp.operation == "GREATER_EQUAL"

        comp = g.Compare.vector.equal(mode="AVERAGE")
        assert comp.operation == "EQUAL"
        assert comp.mode == "AVERAGE"

        comp = g.Compare.vector.equal(mode="DIRECTION", angle=0.5, epsilon=0.3)
        assert comp.i.epsilon.default_value == pytest.approx(0.3)
        assert comp.i.angle.default_value == pytest.approx(0.5)

        comp = g.Compare.vector.equal(mode="DOT_PRODUCT", c=0.5, epsilon=0.2)
        assert comp.i.c.default_value == pytest.approx(0.5)
        assert comp.i.epsilon.default_value == pytest.approx(0.2)

        comp = g.Compare.vector.not_equal()
        assert comp.operation == "NOT_EQUAL"

        # --- color ---
        comp = g.Compare.color.brighter()
        assert comp.data_type == "RGBA"
        assert comp.operation == "BRIGHTER"

        comp = g.Compare.color.darker()
        assert comp.operation == "DARKER"

        comp = g.Compare.color.equal()
        assert comp.operation == "EQUAL"

        comp = g.Compare.color.not_equal()
        assert comp.operation == "NOT_EQUAL"


def test_manual_field_factories():
    with g.tree("FieldFactories"):
        eai = g.EvaluateAtIndex.corner.boolean()
        assert eai.domain == "CORNER"
        assert eai.data_type == "BOOLEAN"

        eai = g.EvaluateAtIndex.face.float()
        assert eai.domain == "FACE"
        assert eai.data_type == "FLOAT"

        eai = g.EvaluateAtIndex.face.matrix()
        assert eai.domain == "FACE"
        assert eai.data_type == "FLOAT4X4"

        with g.Frame("Test") as f:
            af = g.AccumulateField.edge.float()
            assert af.domain == "EDGE"
            assert af.data_type == "FLOAT"

        assert af.node.parent == f.node

        assert f.shrink
        f.shrink = False
        assert not f.shrink
        assert f.label == "Test"
        assert f.text is None
        f.text = bpy.data.texts.new("NewTex")
        assert f.text is not None
        assert isinstance(f.text, bpy.types.Text)

        af = g.AccumulateField.edge.float(g.SplineParameter().o.length)
        assert af.node
        assert af.node.parent is None

        af = g.AccumulateField.edge.integer()
        assert af.data_type == "INT"
        assert af.domain == "EDGE"

        af = g.AccumulateField.edge.vector()
        assert af.data_type == "FLOAT_VECTOR"
        assert af.domain == "EDGE"

        fa = g.FieldAverage.edge.float()
        assert fa.domain == "EDGE"
        assert fa.data_type == "FLOAT"

        fmm = g.FieldMinAndMax.edge.float()
        assert fmm.domain == "EDGE"
        assert fmm.data_type == "FLOAT"

        fmm = g.FieldMinAndMax.edge.integer()
        assert fmm.domain == "EDGE"
        assert fmm.data_type == "INT"

        fmm = g.FieldMinAndMax.edge.vector()
        assert fmm.domain == "EDGE"
        assert fmm.data_type == "FLOAT_VECTOR"

        eod = g.EvaluateOnDomain.edge.float()
        assert eod.domain == "EDGE"
        assert eod.data_type == "FLOAT"

        eod = g.EvaluateOnDomain.edge.integer()
        assert eod.domain == "EDGE"
        assert eod.data_type == "INT"

        eod = g.EvaluateOnDomain.edge.boolean()
        assert eod.domain == "EDGE"
        assert eod.data_type == "BOOLEAN"

        eod = g.EvaluateOnDomain.edge.vector()
        assert eod.domain == "EDGE"
        assert eod.data_type == "FLOAT_VECTOR"

        eod = g.EvaluateOnDomain.edge.quaternion()
        assert eod.domain == "EDGE"
        assert eod.data_type == "QUATERNION"

        eod = g.EvaluateOnDomain.edge.matrix()
        assert eod.domain == "EDGE"
        assert eod.data_type == "FLOAT4X4"

        eod = g.EvaluateOnDomain.face.color()
        assert eod.domain == "FACE"
        assert eod.data_type == "FLOAT_COLOR"

        stat = g.AttributeStatistic.point.float()
        assert stat.domain == "POINT"
        assert stat.data_type == "FLOAT"

        stat = g.AttributeStatistic.point.vector()
        assert stat.domain == "POINT"
        assert stat.data_type == "FLOAT_VECTOR"

        stat = g.AttributeStatistic.edge.float()
        assert stat.domain == "EDGE"

        stat = g.AttributeStatistic.face.vector()
        assert stat.domain == "FACE"
        stat = g.AttributeStatistic.corner.float()
        assert stat.domain == "CORNER"

        stat = g.AttributeStatistic.spline.float()
        assert stat.domain == "CURVE"

        stat = g.AttributeStatistic.instance.float()
        assert stat.domain == "INSTANCE"

        stat = g.AttributeStatistic.layer.float()
        assert stat.domain == "LAYER"


def test_bone_info():
    with g.tree():
        bi = g.BoneInfo()
        assert bi.transform_space == "ORIGINAL"
        bi.transform_space = "RELATIVE"
        assert bi.transform_space == "RELATIVE"


def test_grid():
    with g.tree():
        info = g.GridInfo.boolean()
        assert info.data_type == "BOOLEAN"
        info.data_type = "FLOAT"
        assert info.data_type == "FLOAT"

        mean = g.GridMean.vector()
        assert mean.data_type == "VECTOR"
        mean.data_type = "FLOAT"
        assert mean.data_type == "FLOAT"

        median = g.GridMedian.vector()
        assert median.data_type == "VECTOR"
        median.data_type = "FLOAT"
        assert median.data_type == "FLOAT"

        gtp = g.GridToPoints.vector()
        assert gtp.data_type == "VECTOR"
        gtp.data_type = "FLOAT"
        assert gtp.data_type == "FLOAT"

        gc = g.ClipGrid.integer()
        assert gc.data_type == "INT"
        gc.data_type = "FLOAT"
        assert gc.data_type == "FLOAT"

        gde = g.GridDilateErode.vector()
        assert gde.data_type == "VECTOR"
        gde.data_type = "FLOAT"
        assert gde.data_type == "FLOAT"

        prune = g.PruneGrid.vector()
        assert prune.data_type == "VECTOR"
        prune.data_type = "FLOAT"
        assert prune.data_type == "FLOAT"

        sample = g.SampleGrid.float()
        assert sample.data_type == "FLOAT"
        sample.data_type = "INT"
        assert sample.data_type == "INT"

        sgi = g.SampleGridIndex.integer()
        assert sgi.data_type == "INT"
        sgi.data_type = "FLOAT"
        assert sgi.data_type == "FLOAT"

        sng = g.StoreNamedGrid.boolean()
        assert sng.data_type == "BOOLEAN"
        sng.data_type = "FLOAT"
        assert sng.data_type == "FLOAT"

        vox = g.VoxelizeGrid.float()
        assert vox.data_type == "FLOAT"
        vox.data_type = "INT"
        assert vox.data_type == "INT"

        idx = g.IndexSwitch.bundle()
        assert idx.data_type == "BUNDLE"
        idx.data_type = "FLOAT"
        assert idx.data_type == "FLOAT"


def test_bundle_item():
    with g.tree():
        bundle = g.CombineBundle({"pos": g.Position().o.position, "val": 0.5})

        gbi = g.GetBundleItem.float()
        assert gbi.structure_type == "AUTO"
        gbi.structure_type = "LIST"
        assert gbi.structure_type == "LIST"
        assert gbi.socket_type == "FLOAT"
        gbi.socket_type = "INT"
        assert gbi.socket_type == "INT"

        sbi = g.StoreBundleItem.float()
        assert sbi.structure_type == "AUTO"
        sbi.structure_type = "LIST"
        assert sbi.structure_type == "LIST"
        assert sbi.socket_type == "FLOAT"
        sbi.socket_type = "INT"
        assert sbi.socket_type == "INT"

        switch = g.Switch.bundle()
        assert switch.input_type == "BUNDLE"
        switch.input_type = "FLOAT"
        assert switch.input_type == "FLOAT"

        assert not bundle.define_signature
        bundle.define_signature = True
        assert bundle.define_signature
        assert isinstance(bundle.i["val"], FloatSocket)
        sep = g.SeparateBundle()
        assert not sep.define_signature
        sep.define_signature = True
        assert sep.define_signature

        with pytest.raises(TypeError):
            g.CombineBundle({"pos": float})


def test_uv_normal_map():
    with s.tree():
        map = s.NormalMap()
        assert map.space == "TANGENT"
        map.space = "OBJECT"
        assert map.uv_map == ""
        map.uv_map = "UV Map"
        assert map.uv_map == "UV Map"
        assert map.base == "DISPLACED"
        map.base = "ORIGINAL"
        assert map.base == "ORIGINAL"

        vec = s.VectorDisplacement()
        assert vec.space == "TANGENT"
        vec.space = "OBJECT"

        vec = s.VectorTransform()
        assert vec.vector_type == "VECTOR"
        vec.vector_type = "POINT"
        assert vec.vector_type == "POINT"
        assert vec.convert_from == "WORLD"
        vec.convert_from = "OBJECT"
        assert vec.convert_from == "OBJECT"
        assert vec.convert_to == "OBJECT"
        vec.convert_to = "WORLD"
        assert vec.convert_to == "WORLD"


def test_geometry_nodes():
    with g.tree():
        cu = g.Arc.points()
        assert cu.mode == "POINTS"
        cu.mode = "RADIUS"
        assert cu.mode == "RADIUS"

        bez = g.BezierSegment.position()
        assert bez.mode == "POSITION"
        bez.mode = "OFFSET"
        assert bez.mode == "OFFSET"

        cone = g.Cone.n_gon()
        assert cone.fill_type == "NGON"
        cone.fill_type = "TRIANGLE_FAN"
        assert cone.fill_type == "TRIANGLE_FAN"

        circle = g.CurveCircle.points()
        assert circle.mode == "POINTS"
        circle.mode = "RADIUS"
        assert circle.mode == "RADIUS"

        line = g.CurveLine.direction()
        assert line.mode == "DIRECTION"
        line.mode = "POINTS"
        assert line.mode == "POINTS"

        ctp = g.CurveToPoints.evaluated()
        assert ctp.mode == "EVALUATED"
        ctp.mode = "COUNT"
        assert ctp.mode == "COUNT"

        cyl = g.Cylinder.triangles()
        assert cyl.fill_type == "TRIANGLE_FAN"
        cyl.fill_type = "NGON"
        assert cyl.fill_type == "NGON"

        dg = g.DeleteGeometry.edge()
        assert dg.domain == "EDGE"
        dg.domain = "FACE"
        assert dg.domain == "FACE"
        assert dg.mode == "ALL"
        dg.mode = "EDGE_FACE"
        assert dg.mode == "EDGE_FACE"

        dis = g.DistributePointsOnFaces()
        assert dis.distribute_method == "RANDOM"
        dis.distribute_method = "POISSON"
        assert dis.distribute_method == "POISSON"
        assert not dis.use_legacy_normal
        dis.use_legacy_normal = True
        assert dis.use_legacy_normal

        rz = g.RealizeInstances()
        assert not rz.realize_to_point_domain
        rz.realize_to_point_domain = True
        assert rz.realize_to_point_domain

        res = g.ResampleCurve()
        assert res.i.mode.default_value == "Count"
        res.i.mode.default_value = "Length"
        assert res.i.mode.default_value == "Length"
        assert not res.keep_last_segment
        res.keep_last_segment = True
        assert res.keep_last_segment

        ray = g.Raycast.boolean()
        assert ray.data_type == "BOOLEAN"
        ray.data_type = "FLOAT"
        assert ray.data_type == "FLOAT"

        sns = g.SampleNearestSurface.color()
        assert sns.data_type == "FLOAT_COLOR"
        sns.data_type = "FLOAT"
        assert sns.data_type == "FLOAT"

        suv = g.SampleUVSurface.float()
        assert suv.data_type == "FLOAT"
        suv.data_type = "FLOAT_COLOR"
        assert suv.data_type == "FLOAT_COLOR"

        att = g.NamedAttribute.vector()
        assert att.data_type == "FLOAT_VECTOR"
        att.data_type = "FLOAT"
        assert att.data_type == "FLOAT"

        rot = g.Rotation()
        assert list(rot.rotation_euler) == [0.0, 0.0, 0.0]  # ty: ignore[invalid-argument-type]
        rot.rotation_euler = (1.0, 2.0, 3.0)
        assert list(rot.rotation_euler) == [1.0, 2.0, 3.0]  # ty: ignore[invalid-argument-type]

        vec = g.Vector()
        assert list(vec.vector) == [0.0, 0.0, 0.0]  # ty: ignore[invalid-argument-type]
        vec.vector = (1.0, 2.0, 3.0)
        assert list(vec.vector) == [1.0, 2.0, 3.0]  # ty: ignore[invalid-argument-type]

        blur = g.BlurAttribute.integer()
        assert blur.data_type == "INT"
        blur.data_type = "FLOAT"
        assert blur.data_type == "FLOAT"

        hash = g.HashValue.matrix()
        assert hash.data_type == "MATRIX"
        hash.data_type = "INT"
        assert hash.data_type == "INT"

        rand = g.RandomValue.vector()
        assert rand.data_type == "FLOAT_VECTOR"
        rand.data_type = "INT"
        assert rand.data_type == "INT"

        sgb = g.SetGridBackground.integer()
        assert sgb.data_type == "INT"
        sgb.data_type = "FLOAT"
        assert sgb.data_type == "FLOAT"

        sgt = g.SetGridTransform.integer()
        assert sgt.data_type == "INT"
        sgt.data_type = "FLOAT"
        assert sgt.data_type == "FLOAT"

        eo = g.EnableOutput.closure()
        assert eo.data_type == "CLOSURE"
        eo.data_type = "FLOAT"
        assert eo.data_type == "FLOAT"


def test_node_float_input():
    with g.tree():
        node = g.Float(5.0)
        assert node.value == pytest.approx(5.0)
        assert node.node.bl_idname == g.Value._bl_idname

    with c.tree():
        node = c.Float(5.0)
        assert node.value == pytest.approx(5.0)
        assert node.node.bl_idname == g.Value._bl_idname

    with s.tree():
        node = s.Float(5.0)
        assert node.value == pytest.approx(5.0)
        assert node.node.bl_idname == g.Value._bl_idname


def test_compositor_node_image():
    with c.tree():
        im = bpy.data.images.new("test", width=100, height=100)
        node = c.Image(image=im)
        assert node.node.bl_idname == "CompositorNodeImage"
        assert node.frame_duration == 0
        node.frame_duration = 10
        assert node.frame_duration == 10
        assert node.frame_start == 0
        node.frame_start = 10
        assert node.frame_start == 10
        assert node.frame_offset == 0
        node.frame_offset = 10
        assert node.frame_offset == 10
        assert not node.use_cyclic
        node.use_cyclic = True
        assert node.use_cyclic
        assert not node.use_auto_refresh
        node.use_auto_refresh = True
        assert node.use_auto_refresh
        assert not node.has_layers
        assert node.image == im
        node.image = None
        assert node.image is None
        node.image = im
        assert node.layer == ""
        assert node.view == ""
        assert not node.has_views

        matt = c.Cryptomatte()
        assert matt.source == "RENDER"
        matt.source = "IMAGE"
        assert matt.source == "IMAGE"
        assert matt.matte_id == ""
        matt.matte_id = "test"
        assert matt.matte_id == "test"
        assert matt.layer_name == ""
        assert matt.layer == ""
        assert matt.view == ""
        assert not matt.has_views
        assert matt.frame_duration == 0
        matt.frame_duration = 10
        assert matt.frame_duration == 10
        assert matt.frame_start == 0
        matt.frame_start = 10
        assert matt.frame_start == 10
        assert matt.frame_offset == 0
        matt.frame_offset = 10
        assert matt.frame_offset == 10
        assert not matt.use_cyclic
        matt.use_cyclic = True
        assert matt.use_cyclic
        assert not matt.use_auto_refresh
        matt.use_auto_refresh = True
        assert matt.use_auto_refresh
        assert not matt.has_layers


def test_geometry_reroute():
    with g.tree("test", arrange=None) as tree:
        g.Cube().o.mesh >> g.Reroute() >> tree.outputs.geometry()

    assert len(tree) == 3
    assert len(tree.tree.links) == 2
    assert bpy.data.node_groups["test"].nodes["Reroute"].inputs[0].type == "GEOMETRY"
    assert bpy.data.node_groups["test"].nodes["Reroute"].outputs[0].type == "GEOMETRY"


def test_closure_nodes():
    with g.tree() as tree:
        setpos = g.SetPosition()

        cl = g.ClosureZone()

        cl.input.link(setpos.i.geometry)
        cl.output.link(setpos.o.geometry)

        ec = g.EvaluateClosure()
        ec.sync_signature(cl)
        cl.output >> ec >> tree.outputs.geometry()

        input, output = g.ClosureZone()
        vec = g.CombineXYZ()
        _ = [input.link(x) for x in vec.i]
        output.link(vec.o.vector)

        ec = g.EvaluateClosure()
        ec.sync_signature(output)
        output >> ec >> tree.outputs.vector()

        input, output = g.ClosureZone()

        output.sync_signature(ec)
        assert isinstance(output.i[0], VectorSocket)
        assert len(input.o) == 4
        assert isinstance(input.o[0], FloatSocket)


def test_sample_index():
    with g.tree():
        points = g.Points(10, g.RandomValue.vector().o.value)
        node = g.SampleIndex.point.vector(points, g.Position(), g.Index())

        assert node.data_type == "FLOAT_VECTOR"
        assert node.domain == "POINT"
        assert node.i.value.links[0].from_node.bl_idname == g.Position._bl_idname

        si = g.SampleIndex.edge.float()
        assert si.data_type == "FLOAT"
        assert si.domain == "EDGE"
        assert not si.clamp
        si.clamp = True
        assert si.clamp

        si = g.SampleIndex.face.vector(clamp=True)
        assert si.data_type == "FLOAT_VECTOR"
        assert si.domain == "FACE"
        assert si.clamp

        si = g.SampleIndex.layer.integer()
        assert si.data_type == "INT"
        assert si.domain == "LAYER"

        si = g.SampleIndex.spline.boolean()
        assert si.data_type == "BOOLEAN"
        assert si.domain == "CURVE"

        si = g.SampleIndex.edge.color()
        assert si.data_type == "FLOAT_COLOR"
        assert si.domain == "EDGE"

        si = g.SampleIndex.instance.quaternion()
        assert si.data_type == "QUATERNION"
        assert si.domain == "INSTANCE"

        si = g.SampleIndex.instance.matrix()
        assert si.data_type == "FLOAT4X4"
        assert si.domain == "INSTANCE"
        assert isinstance(si.i.value, MatrixSocket)

        si.data_type = "FLOAT"
        assert si.data_type == "FLOAT"
        assert isinstance(si.i.value, FloatSocket)


def test_sample_curve():
    with g.tree():
        sc = g.SampleCurve.factor.boolean()
        assert sc.data_type == "BOOLEAN"
        assert sc.mode == "FACTOR"
        assert not sc.use_all_curves
        sc.use_all_curves = True
        assert sc.use_all_curves
        sc.data_type = "FLOAT"
        assert sc.data_type == "FLOAT"
        assert isinstance(sc.i.value, FloatSocket)

        sc = g.SampleCurve.factor.color()
        assert sc.data_type == "FLOAT_COLOR"
        assert sc.mode == "FACTOR"

        sc = g.SampleCurve.factor.vector()
        assert sc.data_type == "FLOAT_VECTOR"

        sc = g.SampleCurve.factor.float()
        assert sc.data_type == "FLOAT"

        sc = g.SampleCurve.factor.integer()
        assert sc.data_type == "INT"

        sc = g.SampleCurve.factor.matrix()
        assert sc.data_type == "FLOAT4X4"
        assert sc.mode == "FACTOR"

        sc = g.SampleCurve.factor.quaternion()
        assert sc.data_type == "QUATERNION"
        assert sc.mode == "FACTOR"

        sc = g.SampleCurve.length.float()
        assert sc.data_type == "FLOAT"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.integer()
        assert sc.data_type == "INT"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.boolean()
        assert sc.data_type == "BOOLEAN"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.vector()
        assert sc.data_type == "FLOAT_VECTOR"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.color()
        assert sc.data_type == "FLOAT_COLOR"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.matrix()
        assert sc.data_type == "FLOAT4X4"
        assert sc.mode == "LENGTH"

        sc = g.SampleCurve.length.quaternion()
        assert sc.data_type == "QUATERNION"
        assert sc.mode == "LENGTH"


def test_float_curve():
    with g.tree():
        rand = random.rand(12).reshape((6, 2))
        fc = g.FloatCurve(items=rand)
        assert len(fc.points) == 6

        values = (
            (0.0, 0.0, "AUTO_CLAMPED"),
            (0.0, 0.5, "VECTOR"),
            (0.0, 1.0, "AUTO"),
        )
        fc = g.FloatCurve(items=values)
        assert fc.points[1].handle_type == "VECTOR"


def test_color_ramp():
    with g.tree():
        rand = random.rand(16).reshape((4, 4))
        rand[:, 3] = 1.0

        cr = g.ColorRamp(
            items=((i / (rand.shape[0] - 1), x) for i, x in enumerate(rand))
        )
        assert len(cr.elements) == 4


def test_float_to_integer():
    with g.tree():
        fti = g.FloatToInteger()
        assert fti.rounding_mode == "ROUND"
        fti.rounding_mode = "FLOOR"
        assert fti.rounding_mode == "FLOOR"

        fti = g.Float().o.value.to_integer("TRUNCATE")
        node = fti.builder_node
        assert isinstance(node, g.FloatToInteger)
        assert node.rounding_mode == "TRUNCATE"


def test_store_named_attribute():
    with g.tree():
        points = g.Points()

        sna = g.StoreNamedAttribute.edge.float(points)
        assert sna.domain == "EDGE"
        assert sna.data_type == "FLOAT"
        sna.domain = "POINT"
        assert sna.domain == "POINT"
        sna.data_type = "BOOLEAN"
        assert sna.data_type == "BOOLEAN"

        sna = g.StoreNamedAttribute.corner.boolean()
        assert sna.domain == "CORNER"
        assert sna.data_type == "BOOLEAN"

        sna = g.StoreNamedAttribute.face.vector()
        assert sna.domain == "FACE"
        assert sna.data_type == "FLOAT_VECTOR"

        sna = g.StoreNamedAttribute.spline.quaternion()
        assert sna.domain == "CURVE"
        assert sna.data_type == "QUATERNION"

        sna = g.StoreNamedAttribute.layer.matrix()
        assert sna.domain == "LAYER"
        assert sna.data_type == "FLOAT4X4"

        sna = g.StoreNamedAttribute.point.integer_8bit()
        assert sna.domain == "POINT"
        assert sna.data_type == "INT8"

        sna = g.StoreNamedAttribute.point.vector_2d()
        assert sna.data_type == "FLOAT2"

        sna = g.StoreNamedAttribute.point.byte_color()
        assert sna.data_type == "BYTE_COLOR"

        sna = g.StoreNamedAttribute.point.color()
        assert sna.data_type == "FLOAT_COLOR"
        cr = g.ColorRamp(hue_interpolation="CCW", mode="HSL")
        assert cr.hue_interpolation == "CCW"
        assert cr.mode == "HSL"
        assert cr.color_interpolation == "EASE"


def test_string_split():
    with g.tree():
        string = g.String("Example String")
        split = g.SplitString(string.o.string, separator=" ")
        assert split.node.bl_idname == SplitString._bl_idname

        count = string.o.string.split(" ").list_length()
        assert count.node.bl_idname == g.ListLength._bl_idname

        ftl = g.FieldToList(
            10, {"pos": g.Position().o.position, "idx": g.Index(), "num": g.Float(0.0)}
        )
        assert len(ftl.node.list_items) == 3

        assert ftl.i.pos
        assert ftl.i.idx
        assert ftl.i.num

        assert isinstance(ftl.i.pos, VectorSocket)
        assert isinstance(ftl.o.pos, VectorSocketList)

        pos = ftl.o.pos
        norm = pos.normalize()
        assert isinstance(norm, VectorSocketList)
        assert norm.node.bl_idname == g.VectorMath._bl_idname


def test_input_menu():
    with g.tree():
        menu = g.Menu()
        switch = g.MenuSwitch.float(items={"a": 0.0, "b": 0.0, "c": 0.0})
        assert menu.value == ""
        menu >> switch
        assert menu.value == ""
        menu.value = "a"
        assert menu.value == "a"


def test_vector_dimensions():
    with g.tree():
        vec = g.Vector()
        assert vec.vector_dimensions == 3
        assert len(vec.o.vector) == 3
        vec.vector_dimensions = 2
        assert vec.vector_dimensions == 2
        # assert len(vec.o.vector) == 2


def test_field_to_list():
    with g.tree():
        ftl = g.FieldToList(10)
        pos, idx, num = (
            item.output
            for item in ftl.add_items(
                {"pos": g.Position().o.position, "idx": g.Index(), "num": g.Float(0.0)}
            ).values()
        )
        assert len(ftl.node.list_items) == 3
        assert isinstance(pos, VectorSocketList)
        assert isinstance(idx, IntegerSocketList)
        assert isinstance(num, FloatSocketList)
        filtered = pos.filter().get(0)
        assert isinstance(filtered, VectorSocket)
        filtered = idx.filter()
        assert isinstance(filtered, IntegerSocketList)
        filtered = num.filter()
        assert isinstance(filtered, FloatSocketList)
        # if we get using a list index, we should get a list of values, but Blender
        # won't infer that during node tree creation. For type checking it will propagate
        # but not during execution
        assert isinstance(pos.get(idx), VectorSocket)
        # if we get using a single index, we should get a single value
        assert isinstance(pos.get(1), VectorSocket)


def test_field_to_list_fields_deprecated():
    with g.tree():
        with pytest.warns(DeprecationWarning):
            ftl = g.FieldToList(5, fields={"x": g.Value()})
        assert len(ftl.node.list_items) == 1
        assert ftl.node.list_items[0].name == "x"


def test_grid_methods():
    with g.tree():
        grid = g.CubeGridTopology().o.topology
        trans = grid.transform
        assert isinstance(trans, MatrixSocket)
        assert trans.node.bl_idname == g.GridInfo._bl_idname

        grid = cast(FloatSocketGrid, g.FieldToGrid().capture(g.Float(), name="test"))
        value = grid.background_value

        list = g.FieldToList(10).capture(g.Vector(), name="test")
        assert isinstance(list, VectorSocketList)

        assert isinstance(value, FloatSocket)


def test_implicit_conversion():
    with g.tree():
        con = g.ImplicitConversion.boolean(g.Float())
        assert con.data_type == "BOOLEAN"
        con.data_type = "VECTOR"
        assert con.data_type == "VECTOR"

    with c.tree():
        con = c.ImplicitConversion.boolean(c.Float())
        assert con.data_type == "BOOLEAN"
        con.data_type = "VECTOR"
        assert con.data_type == "VECTOR"

    with s.tree():
        con = s.ImplicitConversion.boolean(s.Float())
        assert con.data_type == "BOOLEAN"
        con.data_type = "VECTOR"
        assert con.data_type == "VECTOR"


def test_integer_vector():
    with c.tree():
        vec = c.IntegerVector()
        assert len(vec.vector) == 3
        assert vec.vector == [0, 0, 0]
        assert vec.vector_dimensions == 3
        vec.vector_dimensions = 2
        assert vec.vector_dimensions == 2
        assert vec.vector == [0, 0]
        vec.vector = [1, 2]
        assert vec.vector == [1, 2]
        vec.vector_dimensions = 3
        vec.vector = [3, 2, 1]
        assert vec.vector == [3, 2, 1]


def test_matrix_socket():
    with g.tree():
        mat = g.CombineTransform().o.transform
        result = mat @ g.Position().o.position
        result = cast(MatrixSocketList, mat)

        r2 = mat @ result
        assert isinstance(r2, MatrixSocket)


def test_set_handle_type():
    with g.tree():
        sh = g.SetHandleType(handle_type="VECTOR", left=True, right=True)
        assert sh.handle_type == "VECTOR"
        assert sh.left
        assert sh.right

        sh.handle_type = "AUTO"
        assert sh.handle_type == "AUTO"

        sh.left = False
        sh.right = False
        assert not sh.left
        assert not sh.right

        # left setter while right is False: True -> {"LEFT"}, then False -> set()
        sh.left = True
        assert sh.left and not sh.right
        sh.left = False
        assert not sh.left and not sh.right

        sh.right = True
        assert sh.right
        sh.left = True
        assert sh.left

        sh2 = g.SetHandleType(left=False, right=True)
        assert not sh2.left
        assert sh2.right

        sh3 = g.SetHandleType(left=True, right=False)
        assert sh3.left
        assert not sh3.right


def test_handle_type_selection_mode():
    with g.tree():
        node = g.HandleTypeSelection(handle_type="VECTOR", left=True, right=True)
        assert node.handle_type == "VECTOR"
        assert node.mode == {"LEFT", "RIGHT"}

        # right setter while left is True: True -> {"LEFT", "RIGHT"}, False -> {"LEFT"}
        node.right = False
        assert node.left and not node.right
        # left setter while right is False -> set()
        node.left = False
        assert not node.left and not node.right

        node.mode = {"LEFT"}
        assert node.mode == {"LEFT"}


def test_input_node_value_getters():
    """The collection/material/object input nodes expose their stored value."""
    with g.tree():
        assert g.Collection().collection is None
        assert g.Material().material is None
        assert g.Object().object is None


def test_node_enum_property_getters():
    """Enum/bool properties added in 5.2 round-trip through their getters."""
    with g.tree():
        assert g.CaptureAttribute.point().domain == "POINT"
        assert g.MenuSwitch.float(items={"a": 0.0}).data_type == "FLOAT"
        assert g.SDFGridBoolean().operation == "DIFFERENCE"

        mix = g.Mix.float()
        assert mix.factor_mode == "UNIFORM"
        assert mix.blend_type == "MIX"
        assert mix.clamp_factor is False
        assert mix.clamp_result is False


def test_field_to_list_typed_items():
    """Each typed FieldToList helper adds an item of the matching list type."""
    with g.tree():
        ftl = g.FieldToList(5)
        assert isinstance(ftl.float(1.0), FloatSocketList)
        assert isinstance(ftl.integer(2), IntegerSocketList)
        assert isinstance(ftl.boolean(True), BooleanSocketList)
        assert isinstance(ftl.vector((1, 2, 3)), VectorSocketList)
        assert isinstance(ftl.color((1, 0, 0, 1)), ColorSocketList)
        assert isinstance(ftl.rotation(), RotationSocketList)
        assert isinstance(ftl.matrix(), MatrixSocketList)
        assert isinstance(ftl.string("name", name="Label"), StringSocketList)
        assert isinstance(ftl.menu(g.Menu().o.menu), MenuSocketList)


def test_field_to_grid_capture_typed(snapshot):
    """Each typed FieldToGrid capture helper adds a grid item of the matching type."""
    with g.tree(arrange="simple") as tree:
        ftg = g.CubeGridTopology() >> g.FieldToGrid.boolean()
        assert isinstance(ftg.capture_float(g.Float()), FloatSocketGrid)
        assert isinstance(ftg.capture_boolean(g.Boolean()), BooleanSocketGrid)
        assert isinstance(ftg.capture_vector(g.Vector()), VectorSocketGrid)
        named = ftg.capture_integer(g.Integer(), name="idx")
        assert isinstance(named, IntegerSocketGrid)
        assert named.name == "idx"

        back = named.dilate_erode(-2).voxelize().background_value

        f = ftg.capture_float(g.NoiseTexture().o.fac)
        end = f.dilate_erode(1).laplacian().gradient().divergence()

        end >> tree.outputs.float("Grid", structure_type="GRID")
        back >> tree.outputs.integer("Background", structure_type="SINGLE")

    assert snapshot == tree.to_mermaid()


def test_grid_socket_methods():
    """Every grid socket helper builds its node and returns the expected socket type."""
    with g.tree():
        ftg = g.CubeGridTopology() >> g.FieldToGrid.boolean()
        fgrid = ftg.capture_float(g.Float())
        vgrid = ftg.capture_vector(g.Vector())
        igrid = ftg.capture_integer(g.Integer())

        # _GridMeanMixin (float / vector / integer grids)
        assert isinstance(fgrid.mean(), FloatSocketGrid)
        assert isinstance(fgrid.median(), FloatSocketGrid)
        assert isinstance(vgrid.mean(), VectorSocketGrid)
        assert isinstance(igrid.median(), IntegerSocketGrid)

        # _FloatGridOperatorMixin (float grids only)
        assert isinstance(fgrid.gradient(), VectorSocketGrid)
        assert isinstance(fgrid.laplacian(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_fillet(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_laplacian(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_mean(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_mean_curvature(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_median(), FloatSocketGrid)
        assert isinstance(fgrid.sdf_offset(), FloatSocketGrid)
        assert isinstance(fgrid.to_mesh(), GeometrySocket)

        # _VectorGridOperatorMixin (vector grids only)
        assert isinstance(vgrid.curl(), VectorSocketGrid)
        assert isinstance(vgrid.divergence(), FloatSocketGrid)

        # _GridSocketMixin (all grid types)
        assert isinstance(fgrid.sample(), FloatSocket)
        assert isinstance(fgrid.sample_index(), FloatSocket)
        assert isinstance(fgrid.field_to_grid(), g.FieldToGrid)
        assert isinstance(fgrid.clip(), FloatSocketGrid)
        assert isinstance(fgrid.dilate_erode(), FloatSocketGrid)
        assert isinstance(fgrid.prune(), FloatSocketGrid)
        assert isinstance(fgrid.voxelize(), FloatSocketGrid)
        assert isinstance(fgrid.to_points(), g.GridToPoints)
