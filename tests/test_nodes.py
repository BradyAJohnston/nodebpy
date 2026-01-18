import itertools
from turtle import pos, position

import pytest
from bpy.types import OUTLINER_HT_header

from nodebpy import TreeBuilder
from nodebpy import nodes as n


def test_capture_attribute():
    with TreeBuilder("TestCaptureAttribute") as tree:
        cube = n.Cube()
        cap = n.CaptureAttribute(domain="POINT")

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
        ) >> n.CaptureAttribute(
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
    format_string = "Hello {x} friends, it is {y} hours and this is a {String}"
    with TreeBuilder("TestFormatString"):
        x_int = n.Integer(5)
        y_value = n.Value(12.50)
        format = n.FormatString(
            n.String("test"),
            format=format_string,
            x=x_int,
            y=y_value,
        )

        assert len(format.node.format_items) == 3
        assert format.node.inputs[0].default_value == format_string  # type: ignore
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
        assert node.left == False
        assert node.right == False
        node.left = True
        assert node.left == True
        node.right = True
        assert node.right == True
        node = n.HandleTypeSelection(left=False, right=True)
        assert node.left == False
        assert node.right == True
        node = n.HandleTypeSelection(left=True, right=True)
        assert node.left == True
        assert node.right == True
        node = n.HandleTypeSelection(left=True, right=False)
        assert node.left == True
        assert node.right == False


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
        input, output = n.simulation_zone(cube)
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
