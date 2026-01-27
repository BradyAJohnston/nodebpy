import itertools

import pytest

from nodebpy import TreeBuilder
from nodebpy import nodes as n
from nodebpy import sockets as s


def test_capture_attribute():
    with TreeBuilder("TestCaptureAttribute") as tree:
        cube = n.Cube()
        cap = n.CaptureAttribute.edge()

        _ = (
            cube
            >> cap
            >> n.SetPosition(offset=(0, 0, 10))
            >> n.SetPosition(position=cap.capture(n.Position()))
        )

    assert "Capture Attribute" in tree.nodes
    assert len(cap._items) == 1
    assert cap.node.outputs[1].name == "Position"
    assert cap.node.outputs[1].type == "VECTOR"

    with TreeBuilder() as tree:
        cap = n.Points(
            count=10, position=n.RandomValue.vector(), radius=n.RandomValue.float()
        ) >> n.CaptureAttribute.point(
            n.Position(),
            n.Radius(),
            normal=n.Normal(),
        )
        assert len(cap.node.capture_items) == 3
        assert (
            cap.inputs["normal"].socket.links[0].from_node.bl_idname
            == "GeometryNodeInputNormal"
        )
        assert (
            cap.inputs["Position"].socket.links[0].from_node.bl_idname
            == "GeometryNodeInputPosition"
        )


def test_join_geometry():
    with TreeBuilder("TestJoinGeometry") as tree:
        items = [n.Cube(), n.UVSphere(), n.Cone(), n.Cylinder(), n.Grid()]
        join = n.JoinGeometry(*items)

    assert "Join Geometry" in tree.nodes
    assert len(join.node.inputs["Geometry"].links) == 5
    # links to join geometry are created in reverse order but we internally reverse them back
    assert join._default_input_socket.links[0].from_node == items[0].node


def test_socket_selection():
    with TreeBuilder("AnotherTree"):
        pos = n.SetPosition()
        vec = n.Vector()

        vec >> pos.i_offset
        n.Position() * 1.0 >> pos.i_position

    assert pos.i_offset.socket_name == "Offset"
    assert vec.o_vector.socket.links[0].to_socket.node == pos.node
    assert vec.o_vector.socket.links[0].to_socket == pos.i_offset.socket
    assert len(pos.i_offset.socket.links) == 1


class TestMathOperators:
    @pytest.mark.parametrize(
        "operator,input",
        itertools.product(
            ["+", "-", "*", "/"],
            [n.Vector, n.Value],
        ),
    )
    def test_math_operators(self, operator, input):
        with TreeBuilder("TestMathOperators"):
            set_pos = n.SetPosition()
            pos = n.Position()  # noqa: F841

            eval(f"input() {operator} 1.0 {operator} pos >> set_pos")

        assert len(set_pos.i_offset.socket.links) == 0
        assert len(set_pos.i_geometry.socket.links) == 0
        assert len(set_pos.i_position.socket.links) == 1


def test_format_string():
    str_to_format = "Hello {x} friends, it is {y} hours and this is a {String}"
    with TreeBuilder("TestFormatString"):
        x_int = n.Integer(5)
        y_value = n.Value(12.50)
        format = n.FormatString(
            n.String("test"),
            format=str_to_format,
            x=x_int,
            y=y_value,
        )

        assert len(format.node.format_items) == 3
        assert format.node.inputs[0].default_value == str_to_format  # type: ignore
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
        _ = ftg.outputs["test"] >> math

    assert len(tree) == 8
    assert len(ftg.node.grid_items) == 6
    assert ftg.node.grid_items[5].name == "test"
    assert ftg.outputs["test"].socket.links[0].to_socket.node == math.node
    assert all(
        [i._default_output_socket.links[0].to_socket.node == ftg.node for i in inputs]
    )
    for item, type in zip(
        ftg.node.grid_items, ["VECTOR", "FLOAT", "BOOLEAN", "INT", "VECTOR", "FLOAT"]
    ):
        assert item.data_type == type

    with TreeBuilder() as tree:
        grid = n.VolumeCube(n.NoiseTexture()) >> n.GetNamedGrid(name="density")
        ftg = n.FieldToGrid.vector(n.NoiseTexture().o_color, topology=grid)

    assert ftg.data_type == "VECTOR"
    assert len(ftg.node.grid_items) == 1
    assert ftg.i_topology.socket.links[0].from_node == grid.node
    assert ftg.i_topology.socket.links[0].from_socket == grid.o_grid.socket
    assert ftg.inputs["Color"].socket.links[0].from_node.name == "Noise Texture.001"


def test_geometry_to_instance():
    with TreeBuilder() as tree:
        inputs = [n.Cube(), n.UVSphere(), n.IcoSphere(), n.Cone()]
        gti = n.GeometryToInstance(*inputs)

    assert len(tree) == 5
    assert len(gti.node.inputs[0].links) == 4
    assert gti._default_input_socket.links[2].from_node == inputs[2].node
    assert gti._default_input_socket.links[1].from_node == inputs[1].node


def test_get_named_grid(snapshot_tree):
    with TreeBuilder() as tree:
        (
            n.VolumeCube()
            >> n.GetNamedGrid(name="density")
            >> n.FieldToGrid(n.Position(), n.Position() * 2 + 10)
        )

    assert snapshot_tree == tree


def test_advect_grid(snapshot_tree):
    with TreeBuilder():
        grid = n.GetNamedGrid(n.VolumeCube(), name="density")
        ftg = n.FieldToGrid(
            n.Position(),
            topology=grid,
        )

        ag = grid >> n.AdvectGrid(
            velocity=ftg, time_step=n.Value(0.1), integration_scheme="Midpoint"
        )

    assert ftg.i_topology.socket.links[0].from_socket == grid.o_grid.socket
    assert len(grid.o_volume.socket.links) == 0
    assert ag.i_integration_scheme.socket.default_value == "Midpoint"


def test_sdf_grid_boolean():
    with TreeBuilder() as tree:
        trio = [n.PointsToSDFGrid() for _ in range(3)]
        bool1 = n.SDFGridBoolean.difference(
            *trio,
            grid_1=n.GetNamedGrid(n.VolumeCube(), name="density"),
        )
        bool2 = n.SDFGridBoolean.intersect(*trio)
        bool3 = n.SDFGridBoolean.union(*trio)

    assert len(tree) == 8
    assert (
        bool1.i_grid_1.socket.links[0].from_node.bl_idname == "GeometryNodeGetNamedGrid"
    )
    assert len(bool1.i_grid_2.socket.links) == 3
    assert len(bool2.i_grid_2.socket.links) == 3
    assert len(bool3.i_grid_2.socket.links) == 3


@pytest.mark.parametrize(
    "domain,output",
    zip(
        ["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"],
        ["Point Count", "Point Count", "Point Count", "Instance Count", "Layer Count"],
    ),
)
def test_domain_size(domain, output):
    with TreeBuilder() as tree:
        domain_size = n.DomainSize(n.Points(10), component=domain)
        domain_size >> n.Points()

    assert len(tree) == 3
    assert len(domain_size.node.outputs[output].links) == 1


def test_curve_handle():
    with TreeBuilder():
        node = n.HandleTypeSelection(left=False, right=False)
        assert not node.left
        assert not node.right
        node.left = True
        assert node.left
        node.right = True
        assert node.right
        node = n.HandleTypeSelection(left=False, right=True)
        assert not node.left
        assert node.right
        node = n.HandleTypeSelection(left=True, right=True)
        assert node.left
        assert node.right
        node = n.HandleTypeSelection(left=True, right=False)
        assert node.left
        assert not node.right


def test_bake():
    with TreeBuilder() as tree:
        bake = n.Bake(
            n.Points(10),
            n.Position(),
            n.Value() * n.Radius() + 10,
        )
        set_pos = bake >> n.SetPosition()

    assert len(tree) == 8
    assert len(bake.node.bake_items) == 3
    assert set_pos.node.inputs[0].links[0].from_node == bake.node
    assert set_pos.node.inputs[0].links[0].from_socket == bake.node.outputs[0]


def test_simulation(snapshot_tree):
    with TreeBuilder() as tree:
        cube = n.Cube()
        input, output = n.SimulationZone(cube)
        pos_math = input.capture(n.Position()) * n.Position()
        _ = pos_math >> output
        _ = (
            input
            >> n.SetPosition(
                offset=input.o_delta_time * n.Vector((0, 0, 0.1)) * pos_math
            )
            >> output
        )
        _ = output >> n.SetPosition(position=output.outputs["Position"])
    assert len(output.node.inputs["Skip"].links) == 0
    assert len(tree) == 13
    assert snapshot_tree == tree


def test_repeat(snapshot_tree):
    with TreeBuilder() as tree:
        cube = n.Cube()
        for i, input, output in n.RepeatZone(10, cube):
            pos_math = input.capture(n.Position()) * n.Position()
            _ = pos_math >> output
            _ = (
                input
                >> n.SetPosition(offset=i * n.Vector((0, 0, 0.1)) * pos_math)
                >> output
            )
            _ = output >> n.SetPosition(position=output.outputs["Position"])
    assert len(tree) == 13
    assert len(input.items) == 2
    assert snapshot_tree == tree

    with TreeBuilder() as tree:
        zone = n.RepeatZone(5)
        join = n.JoinGeometry()
        zone.output.capture(join)
        zone.input >> join
        _ = n.Points(zone.i, position=n.RandomValue.vector(min=-1, seed=zone.i)) >> join
    assert all(
        [link.from_socket.type == "GEOMETRY" for link in join.node.inputs[0].links]
    )
    assert len(tree) == 7
    assert snapshot_tree == tree


def test_index_switch(snapshot_tree):
    with TreeBuilder() as tree:
        items = (n.Cube(), n.UVSphere(), n.Cube(), n.Cube())
        index = n.IndexSwitch.geometry(*items, index=5)

    assert len(index.node.index_switch_items) == 4
    assert len(tree) == 5
    assert index.i_index.socket.default_value == 5


def test_menu_switch():
    with TreeBuilder() as tree:
        items = (
            n.Cube(),
            n.UVSphere(),
            n.Cube(),
            n.Cube(),
        )
        switch = n.MenuSwitch.geometry(*items, custom=n.Cone())
        with tree.inputs:
            menu = s.SocketMenu()
        menu >> switch
        menu.socket.default_value = "Mesh"

    assert switch.i_menu.socket.links[0].from_socket == menu.socket
    assert len(switch.node.enum_items) == 5

    with TreeBuilder() as tree:
        switch = n.MenuSwitch.float(*range(10))

    assert len(switch.node.enum_items) == 10
    assert switch.inputs["Item_5"].socket.default_value == 5


def test_multi_menu():
    with TreeBuilder() as tree:
        items = (n.Cube(), n.IcoSphere(), n.Grid())

        menu = n.MenuSwitch.integer(test=0, another=1, again=2)
        switch1 = n.IndexSwitch.geometry(*items, index=menu)
        switch2 = n.IndexSwitch.geometry(*reversed(items), index=menu)

        with tree.inputs:
            menu_input = s.SocketMenu()
            menu_input >> menu
            menu_input.default_value = "test"

        with tree.outputs:
            n.JoinGeometry(switch1, switch2) >> s.SocketGeometry("Output")


def test_switch_repeatzone(snapshot_tree):
    with TreeBuilder() as tree:
        with tree.inputs:
            input = s.SocketGeometry()
        with tree.outputs:
            output = s.SocketGeometry()

        items = (n.Cube(), n.IcoSphere(), n.Grid())
        zone = n.RepeatZone(5, input)
        switch = n.IndexSwitch.geometry(*items, index=zone.i)
        join = n.JoinGeometry(zone.input, switch)
        join >> zone.output >> output

    assert len(zone.output.items) == 1
    assert zone.output.inputs["Geometry"].socket.links[0].from_node == join.node
    assert snapshot_tree == tree


def test_generate_select_group():
    with TreeBuilder() as tree:
        with tree.inputs:
            switch = n.IndexSwitch.boolean(
                *[s.SocketBoolean(str(i)) for i in range(20)],
                index=n.NamedAttribute.integer("chain_id"),
            )
        with tree.outputs:
            switch >> s.SocketBoolean("Selection")

    assert len(switch.node.index_switch_items) == 20
    assert len(tree) == 4


def test_accumulate_field():
    with TreeBuilder() as tree:
        cube = n.Cube()
        aatr = n.AxisAngleToRotation(angle=1.0)
        tran = n.AccumulateField.point.transform(
            n.EvaluateAtIndex.point.rotation(aatr, n.Index() - int(1))
        )
        _ = cube >> n.SetPosition(
            position=n.TransformPoint(n.Position(), tran.o_trailing),
            offset=n.FieldAverage.edge.vector(n.Position()),
        )

        n.SetPosition(offset=n.FieldVariance.point.vector(n.Position()))

    assert tree.nodes.get("Integer Math")
    assert tree.nodes.get("Accumulate Field").outputs["Trailing"].links[
        0
    ].to_node == tree.nodes.get("Transform Point")
    assert tree.nodes.get("Field Average").data_type == "FLOAT_VECTOR"
    assert tree.nodes.get("Field Average").domain == "EDGE"


def test_edge_other_point():
    with TreeBuilder() as tree:
        with tree.inputs:
            v_index = s.SocketInt("Vertex Index", default_input="INDEX")
            e_index = s.SocketInt("Edge Number")

        # with the index from the selected edge from the input, we get the two different vertices
        # of the edge. We compare them and return the one that isn't the current input vertex index
        eov = n.EdgesOfVertex(v_index, sort_index=e_index)
        ev = n.EdgeVertices()
        vert_1 = n.EvaluateAtIndex.edge.integer(ev.o_vertex_index_1, eov)
        vert_2 = n.EvaluateAtIndex.edge.integer(ev.o_vertex_index_2, eov)
        compare = n.Compare.equal.integer(v_index, vert_1)
        other_vertex = n.Switch.integer(compare, vert_1, vert_2)

        with tree.outputs:
            _ = other_vertex >> s.SocketInt("Other Vertex")

    other_vertex.node.inputs[0].links[0].from_node == vert_1.node
    other_vertex.node.inputs[1].links[0].from_node == vert_2.node
    other_vertex.node.inputs[2].links[0].from_node.name == "Compare"
    compare.o_result.socket.links[0].to_node.name == "Switch"


def test_align_rotation_to_vector():
    """Ensure that it appropiately selects a vector or rotation socket"""
    with TreeBuilder() as tree:
        # this should select the vector input socket
        artv = n.RandomValue.vector() >> n.AlignRotationToVector()
        # this should select the rotation input socket
        artv2 = n.AxesToRotation() >> n.AlignRotationToVector()

    assert (
        artv.i_vector.socket.links[0].from_socket
        == tree.nodes["Random Value"].outputs[0]
    )
    assert (
        artv2.i_rotation.socket.links[0].from_socket
        == tree.nodes["Axes to Rotation"].outputs[0]
    )


def test_foreachgeometryelement_zone():
    with TreeBuilder() as tree:
        with tree.outputs:
            out = s.SocketGeometry("Geometry")
        cube = n.Cube()
        zone = n.ForEachGeometryElementZone(
            cube,
            selection=n.Normal()
            >> n.VectorMath.dot_product(..., (0, 0, 1))
            >> n.Compare.greater_than.float(..., -0.1),
            domain="FACE",
        )
        pos = zone.input.capture(n.Position())
        norm = zone.input.capture(n.Normal())
        transformed = n.Cone() >> n.TransformGeometry(
            translation=pos,
            rotation=n.AlignRotationToVector(
                vector=norm + n.RandomValue.vector(min=-1, id=zone.index)
            ),
            scale=0.4,
        )
        zone.output.capture(pos)
        zone.output.capture_generated(pos)
        zone.output.capture_generated(transformed)
        _ = transformed >> zone.output
        _ = n.JoinGeometry(zone.output.o_generation, cube) >> out

    input, output = zone
    with pytest.raises(IndexError):
        zone[2]

    assert all([i.socket_type == "VECTOR" for i in zone.input.items])
    assert len(zone.input.items) == 2
    assert len(zone.output.items) == 1
    assert zone.output.items[0].socket_type == "VECTOR"
    assert zone.output.node.inputs["Geometry"].links[0].from_node == transformed.node
    assert zone.input == input
    assert zone.output == output
    assert input.output == output.node
    assert input.i_selection.socket.links[0].from_node == tree.nodes["Compare"]
    assert tree.nodes["Compare"].data_type == "FLOAT"
    assert tree.nodes["Compare"].operation == "GREATER_THAN"
    assert len(zone.output.items_generated) == 3
    assert zone.output.items_generated[1].socket_type == "VECTOR"
    assert zone.output.items_generated[2].socket_type == "GEOMETRY"
