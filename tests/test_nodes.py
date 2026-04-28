import itertools

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import FloatSocket, MatrixSocket, VectorSocket
from nodebpy.types import _AttributeDomains


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
    assert cap.node.outputs[1].name == "Position"
    assert cap.node.outputs[1].type == "VECTOR"
    assert cap.i.position.links
    assert len(cap.i.position.links) == 1
    assert cap.i.position.links[0].from_node.bl_idname == g.Position._bl_idname

    with TreeBuilder() as tree:
        cap = g.Points(
            count=10, position=g.RandomValue.vector(), radius=g.RandomValue.float()
        ) >> g.CaptureAttribute.point(
            g.Position(),
            g.Radius(),
            normal=g.Normal(),
        )
        assert len(cap.node.capture_items) == 3
        assert cap.i.normal.links[0].from_node.bl_idname == "GeometryNodeInputNormal"
        assert (
            cap.i.position.links[0].from_node.bl_idname == "GeometryNodeInputPosition"
        )


def test_join_geometry():
    with g.tree() as tree:
        items = [g.Cube(), g.UVSphere(), g.Cone(), g.Cylinder(), g.Grid()]
        join = g.JoinGeometry(*items)

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

    assert pos.i.offset.socket_name == "Offset"
    assert vec.o.vector.socket.links[0].to_socket.node == pos.node
    assert vec.o.vector.socket.links[0].to_socket == pos.i.offset.socket
    assert len(pos.i.offset.socket.links) == 1


class TestMathOperators:
    @pytest.mark.parametrize(
        "operator,input",
        itertools.product(
            ["+", "-", "*", "/"],
            [g.Vector, g.Value],
        ),
    )
    def test_math_operators(self, operator, input):
        with TreeBuilder("TestMathOperators"):
            set_pos = g.SetPosition()
            pos = g.Position()  # noqa: F841

            eval(f"input() {operator} 1.0 {operator} pos >> set_pos")

        assert len(set_pos.i.offset.socket.links) == 0
        assert len(set_pos.i.geometry.socket.links) == 0
        assert len(set_pos.i.position.socket.links) == 1


def test_format_string():
    str_to_format = "Hello {x} friends, it is {y} hours and this is a {String}"
    with TreeBuilder("TestFormatString"):
        x_int = g.Integer(5)
        y_value = g.Value(12.50)
        format = g.FormatString(
            g.String("test"),
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
        inputs = [g.Vector(), g.Value(), g.Boolean(), g.Integer(), g.Rotation()]
        math = g.Math.add()

        ftg = g.FieldToGrid(*inputs, test=g.Value())
        _ = ftg.outputs["test"] >> math

        ftg2 = g.FieldToGrid(test_value=0.3)
        assert ftg2.inputs["test_value"].socket.default_value == pytest.approx(0.3)

    assert len(tree) == 9
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
        grid = g.VolumeCube(g.NoiseTexture()) >> g.GetNamedGrid(name="density")
        ftg = g.FieldToGrid.vector(g.NoiseTexture().o.color, topology=grid)

    assert ftg.data_type == "VECTOR"
    assert len(ftg.node.grid_items) == 1
    assert ftg.i.topology.socket.links[0].from_node == grid.node
    assert ftg.i.topology.socket.links[0].from_socket == grid.o.grid.socket
    assert ftg.inputs["Color"].socket.links[0].from_node.name == "Noise Texture.001"


def test_field_variance():
    with g.tree():
        var = g.FieldVariance.edge.float(
            g.SplineParameter().o.length, g.CurveOfPoint().o.curve_index
        )
        assert var.data_type == "FLOAT"
        assert var.domain == "EDGE"
        var.domain = "POINT"
        assert var.domain == "POINT"


def test_geometry_to_instance():
    with TreeBuilder() as tree:
        inputs = [g.Cube(), g.UVSphere(), g.IcoSphere(), g.Cone()]
        gti = g.GeometryToInstance(*inputs)

    assert len(tree) == 5
    assert len(gti.node.inputs[0].links) == 4
    assert gti._default_input_socket.links[2].from_node == inputs[2].node
    assert gti._default_input_socket.links[1].from_node == inputs[1].node


def test_get_named_grid(snapshot_tree):
    with TreeBuilder() as tree:
        _ = (
            g.VolumeCube()
            >> g.GetNamedGrid(name="density")
            >> g.FieldToGrid(g.Position(), g.Position() * 2 + 10)
        )

    assert snapshot_tree == tree


def test_advect_grid(snapshot_tree):
    with TreeBuilder():
        grid = g.GetNamedGrid(g.VolumeCube(), name="density")
        ftg = g.FieldToGrid(
            g.Position(),
            topology=grid,
        )

        ag = grid >> g.AdvectGrid(
            velocity=ftg, time_step=g.Value(0.1), integration_scheme="Midpoint"
        )

    assert ftg.i.topology.socket.links[0].from_socket == grid.o.grid.socket
    assert len(grid.o.volume.socket.links) == 0
    assert ag.i.integration_scheme.socket.default_value == "Midpoint"


def test_sdf_grid_boolean():
    with TreeBuilder() as tree:
        trio = [g.PointsToSDFGrid() for _ in range(3)]
        bool1 = g.SDFGridBoolean.difference(
            *trio,
            grid_1=g.GetNamedGrid(g.VolumeCube(), name="density"),
        )
        bool2 = g.SDFGridBoolean.intersect(*trio)
        bool3 = g.SDFGridBoolean.union(*trio)

    assert len(tree) == 8
    assert (
        bool1.i.grid_1.socket.links[0].from_node.bl_idname == "GeometryNodeGetNamedGrid"
    )
    assert len(bool1.i.grid_2.socket.links) == 3
    assert len(bool2.i.grid_2.socket.links) == 3
    assert len(bool3.i.grid_2.socket.links) == 3


@pytest.mark.parametrize(
    "domain,output",
    zip(
        ["MESH", "POINTCLOUD", "CURVE", "INSTANCES", "GREASEPENCIL"],
        ["Point Count", "Point Count", "Point Count", "Instance Count", "Layer Count"],
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


def test_simulation(snapshot_tree):
    with TreeBuilder() as tree:
        cube = g.Cube()
        input, output = g.SimulationZone(cube)
        pos_math = input.capture(g.Position()) * g.Position()
        _ = pos_math >> output
        _ = (
            input
            >> g.SetPosition(
                offset=input.o.delta_time * g.Vector((0, 0, 0.1)) * pos_math
            )
            >> output
        )
        _ = output >> g.SetPosition(position=output.outputs["Position"])
    assert len(output.node.inputs["Skip"].links) == 0
    assert len(tree) == 13
    assert snapshot_tree == tree


def test_repeat(snapshot_tree):
    with TreeBuilder() as tree:
        cube = g.Cube()
        for i, input, output in g.RepeatZone(10, cube):
            pos_math = input.capture(g.Position()) * g.Position()
            _ = pos_math >> output
            _ = (
                input
                >> g.SetPosition(offset=i * g.Vector((0, 0, 0.1)) * pos_math)
                >> output
            )
            _ = output >> g.SetPosition(position=output.outputs["Position"])
    assert len(tree) == 13
    assert len(input.items) == 2
    assert snapshot_tree == tree

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
    assert snapshot_tree == tree


def test_index_switch(snapshot_tree):
    with TreeBuilder() as tree:
        items = (g.Cube(), g.UVSphere(), g.Cube(), g.Cube())
        index = g.IndexSwitch.geometry(*items, index=5)

        index2 = g.IndexSwitch.float(*range(10))

    assert len(index.node.index_switch_items) == 4
    assert len(tree) == 6
    assert index.i.index.socket.default_value == 5
    assert index2.i[1].default_value == pytest.approx(0.0)
    assert index2.i[2].default_value == pytest.approx(1.0)
    assert index2.i[3].default_value == pytest.approx(2.0)


def test_menu_switch():
    with TreeBuilder() as tree:
        menu = tree.inputs.menu()
        items = (
            g.Cube(),
            g.UVSphere(),
            g.Cube(),
            g.Cube(),
        )
        switch = g.MenuSwitch.geometry(*items, custom=g.Cone())
        menu >> switch
        menu.socket.default_value = "Mesh"

    assert switch.i.menu.socket.links[0].from_socket == menu.socket
    assert len(switch.node.enum_items) == 5

    with TreeBuilder() as tree:
        switch = g.MenuSwitch.float(*range(10))

    assert len(switch.node.enum_items) == 10
    print(
        [
            (
                name,
                x.socket.default_value if hasattr(x.socket, "default_value") else None,
            )
            for name, x in switch.inputs._items()
        ]
    )
    assert switch.inputs["Input_5"].socket.default_value == 5


def test_menu_switch_menu_connection():
    with TreeBuilder("AnotherMenuSwitch"):
        switch = g.MenuSwitch.geometry(
            cube=g.Cube(), sphere=g.UVSphere(), cone=g.Cone(), menu=g.Switch.menu()
        )
    assert switch.inputs["Menu"].links
    assert switch.inputs["Menu"].links[0].from_node.bl_idname == g.Switch._bl_idname
    assert switch.inputs["Menu"].links[0].from_node.input_type == "MENU"
    assert switch.inputs["Menu"].socket.default_value == "cube"


def test_multi_menu():
    with TreeBuilder() as tree:
        items = (g.Cube(), g.IcoSphere(), g.Grid())

        menu = g.MenuSwitch.integer(test=0, another=1, again=2)
        switch1 = g.IndexSwitch.geometry(*items, index=menu)
        switch2 = g.IndexSwitch.geometry(*reversed(items), index=menu)

        menu_input = tree.inputs.menu()
        menu_input >> menu
        menu_input.default_value = "test"

        g.JoinGeometry(switch1, switch2) >> tree.outputs.geometry("Output")


def test_switch_repeatzone(snapshot_tree):
    with TreeBuilder() as tree:
        input = tree.inputs.geometry()
        output = tree.outputs.geometry()

        items = (g.Cube(), g.IcoSphere(), g.Grid())
        zone = g.RepeatZone(5, input)
        switch = g.IndexSwitch.geometry(*items, index=zone.iteration)
        join = g.JoinGeometry(zone.input, switch)
        join >> zone.output >> output

    assert len(zone.output.items) == 1
    assert zone.output.inputs["Geometry"].socket.links[0].from_node == join.node
    assert snapshot_tree == tree


def test_generate_select_group():
    with TreeBuilder() as tree:
        switch = g.IndexSwitch.boolean(
            *[tree.inputs.boolean(str(i)) for i in range(20)],
            index=g.NamedAttribute.integer("chain_id"),
        )
        switch >> tree.outputs.boolean("Selection")

    assert len(switch.node.index_switch_items) == 20
    assert len(tree) == 4


def test_accumulate_field():
    with TreeBuilder() as tree:
        cube = g.Cube()
        aatr = g.AxisAngleToRotation(angle=1.0)
        tran = g.AccumulateField.point.transform(
            g.EvaluateAtIndex.point.rotation(aatr, g.Index() - int(1))
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
        _ = g.JoinGeometry(zone.output.outputs._get("Generation_0"), cube) >> out

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
        join = g.JoinStrings(*letters)

    assert len(letters) == len(join.i.strings.links)


def test_mesh_boolean():
    with g.tree():
        meshes = [g.Cube(), g.IcoSphere() >> g.TransformGeometry(translation=0.2)]

        boolean = g.MeshBoolean.intersect(*meshes)
        assert boolean.solver == "FLOAT"
        assert boolean.operation == "INTERSECT"
        boolean.solver = "EXACT"
        assert boolean.solver == "EXACT"
        bool2 = g.MeshBoolean.difference(*meshes, mesh_1=g.Cone(), solver="EXACT")
        assert bool2.operation == "DIFFERENCE"
        assert bool2.solver == "EXACT"
        bool2.operation = "INTERSECT"
        assert bool2.operation == "INTERSECT"
        bool3 = g.MeshBoolean.intersect(
            *meshes, hole_tolerant=g.Boolean(), self_intersection=False, solver="EXACT"
        )
        assert len(bool3.i.mesh_2.links) == 2
        assert bool3.solver == "EXACT"
        assert bool3.operation == "INTERSECT"
        assert (
            bool3.i.hole_tolerant.links[0].from_node.bl_idname == g.Boolean._bl_idname
        )
        bool4 = g.MeshBoolean.union(*meshes, self_intersection=True, solver="EXACT")
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

        eai = g.EvaluateAtIndex.face.transform()
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

        eod = g.EvaluateOnDomain.edge.rotation()
        assert eod.domain == "EDGE"
        assert eod.data_type == "QUATERNION"

        eod = g.EvaluateOnDomain.edge.transform()
        assert eod.domain == "EDGE"
        assert eod.data_type == "FLOAT4X4"

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

        idx = g.IndexSwitch.bundle()
        assert idx.data_type == "BUNDLE"
        idx.data_type = "FLOAT"
        assert idx.data_type == "FLOAT"


def test_bundle_item():
    with g.tree():
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
    with g.tree():
        node = g.Reroute()
        assert node.socket_idname == "NodeSocketColor"
        node.socket_idname = "NodeSocketFloat"
        assert node.socket_idname == "NodeSocketFloat"

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
        _ = [input.link(x) for x in vec.i[:]]
        output.link(vec.o.vector)

        ec = g.EvaluateClosure()
        ec.sync_signature(output)
        output >> ec >> tree.outputs.vector()

        input, output = g.ClosureZone()

        output.sync_signature(ec)
        assert isinstance(output.i[0], VectorSocket)
        assert len(input.o[:]) == 4
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

        si = g.SampleIndex.instance.rotation()
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

        sc = g.SampleCurve.factor.rotation()
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

        sc = g.SampleCurve.length.rotation()
        assert sc.data_type == "QUATERNION"
        assert sc.mode == "LENGTH"
