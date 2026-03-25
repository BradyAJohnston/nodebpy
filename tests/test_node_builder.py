"""
Tests for the node builder API.

Tests the TreeBuilder, NodeBuilder, and the >> operator chaining system.
"""

import inspect
import re
from math import pi

import bpy
import pytest
from bpy.types import NodeSocketInt
from numpy.testing import assert_allclose

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy import sockets as socket
from nodebpy.builder import NodeBuilder, VectorSocketLinker
from nodebpy.types import NodeSocketFloat


class TestTreeBuilder:
    """Tests for TreeBuilder basic functionality."""

    def test_tree_creation(self):
        """Test creating a basic node tree."""
        tree = TreeBuilder("TestTree")
        assert tree.tree is not None
        assert tree.tree.name == "TestTree"
        assert isinstance(tree.tree, bpy.types.GeometryNodeTree)

    def test_interface_definition(self):
        """Test defining tree interface with socket typesocket."""
        tree = TreeBuilder("InterfaceTest")
        with tree.inputs:
            socket.SocketGeometry()
            socket.SocketBoolean("Selection", True)
            socket.SocketVector("Offset", (1.0, 2.0, 3.0))

        with tree.outputs:
            socket.SocketGeometry()
            socket.SocketInt("Count")

        # Check inputs were created
        input_names = [
            socket.name
            for socket in tree.tree.interface.items_tree
            if socket.in_out == "INPUT"
        ]
        assert "Geometry" in input_names
        assert "Selection" in input_names
        assert "Offset" in input_names

        # Check outputs were created
        output_names = [
            socket.name
            for socket in tree.tree.interface.items_tree
            if socket.in_out == "OUTPUT"
        ]
        assert "Geometry" in output_names
        assert "Count" in output_names

    def test_socket_defaults(self):
        """Test that socket defaults are set correctly."""
        tree = TreeBuilder("DefaultsTest")
        with tree.inputs:
            socket.SocketBoolean("Selection", True)
            socket.SocketVector("Offset", (1.0, 2.0, 3.0))
            socket.SocketFloat("Scale", 2.5, min_value=0.0, max_value=10.0)
        with tree.outputs:
            socket.SocketGeometry("Geometry")

        # Find the selection input
        selection_socket = None
        for item in tree.tree.interface.items_tree:
            if item.name == "Selection" and item.in_out == "INPUT":
                selection_socket = item
                break

        assert selection_socket is not None
        assert selection_socket.default_value is True


class TestContextManager:
    """Tests for the context manager functionality."""

    def test_context_manager_basic(self):
        """Test using the tree as a context manager."""

        with TreeBuilder("ContextTest") as tree:
            # Should be able to create nodes without passing tree
            pos = g.Position()
            assert pos.node is not None
            assert pos.tree == tree

    def test_context_manager_node_creation(self):
        """Test that nodes created in context use the active tree."""

        with TreeBuilder("NodeCreationTest") as tree:
            node1 = g.Position()
            node2 = g.SetPosition()

            # Both nodes should be in the same tree
            assert node1.tree == tree
            assert node2.tree == tree
            assert node1.node.id_data == tree.tree
            assert node2.node.id_data == tree.tree


class TestOperatorChaining:
    """Tests for the >> operator chaining."""

    def test_basic_chaining(self):
        """Test basic node chaining with >> operator."""

        with TreeBuilder("ChainingTest") as tree:
            pos = g.Position()
            set_pos = g.SetPosition()

            # Chain with >> operator
            result = pos >> set_pos

            # Should return the right-hand node
            assert result.node == set_pos.node

            # Should create a link between the nodes
            links = tree.tree.links
            assert len(links) > 0

    def test_multi_node_chaining(self):
        """Test chaining multiple nodes together."""
        tree = TreeBuilder("MultiChainTest")
        with tree.inputs:
            i_geo = socket.SocketGeometry()
        with tree.outputs:
            o_geo = socket.SocketGeometry()

        with tree:
            # Chain multiple nodes
            _ = (
                i_geo
                >> g.SetPosition()
                >> g.TransformGeometry(translation=(0, 0, 1))
                >> o_geo
            )

        # Check that links were created
        assert len(tree.tree.links) >= 3


class TestExamples:
    """Tests that replicate the original example functionsocket."""

    def test_example_basic(self):
        """Test the basic example from example.py."""
        tree = TreeBuilder("ExampleTree")

        with tree.inputs:
            i_geo = socket.SocketGeometry()
            selection = socket.SocketBoolean("Selection", True)
            offset = socket.SocketVector("Offset", (1.0, 2.0, 3.0))
        with tree.outputs:
            o_geo = socket.SocketGeometry()

        with tree:
            _ = (
                i_geo
                >> g.SetPosition(
                    selection=selection,
                    position=g.Position() * 2.0,
                    offset=offset,
                )
                >> g.TransformGeometry(translation=(0, 0, 1))
                >> o_geo
            )

        # Verify tree was created correctly
        assert tree.tree is not None
        assert len(tree.tree.nodes) == 6
        assert len(tree.tree.links) == 7

    def test_example_multi_socket(self):
        """Test the multi-socket example from example.py."""
        tree = TreeBuilder("MultiSocketExample")

        with tree.inputs:
            i_geo = socket.SocketGeometry("Geometry")
            selection = socket.SocketBoolean("Selection", True)

        with tree.outputs:
            o_geo = socket.SocketGeometry("Geometry")
            count = socket.SocketInt("Count")

        with tree:
            # Access multiple named sockets
            pos = i_geo >> g.SetPosition(selection=selection)
            _ = pos >> g.DomainSize() >> count
            _ = pos >> o_geo

        # Verify tree structure
        assert tree.tree is not None
        assert len(tree.tree.nodes) > 0

        # Check that both outputs were created
        output_names = [
            socket.name
            for socket in tree.tree.interface.items_tree
            if socket.in_out == "OUTPUT"
        ]
        assert "Geometry" in output_names
        assert "Count" in output_names


class TestGeneratedNodes:
    """Tests for generated node classesocket."""

    def test_position_node(self):
        """Test the Position input node."""
        tree = TreeBuilder("PositionTest")

        with tree:
            pos = g.Position()
            assert pos.node is not None
            assert pos.node.bl_idname == "GeometryNodeInputPosition"

    def test_set_position_node(self):
        """Test the SetPosition node with parametersocket."""
        tree = TreeBuilder("SetPositionTest")
        with tree.inputs:
            in_geo = socket.SocketGeometry()
        with tree.outputs:
            out_geo = socket.SocketGeometry()

        with tree:
            pos = g.Position()
            set_pos = g.SetPosition(position=pos)
            in_geo >> set_pos >> out_geo

            assert set_pos.node is not None
            assert set_pos.node.bl_idname == "GeometryNodeSetPosition"

            # Check that the position input was linked
            assert len(set_pos.node.inputs["Position"].links) > 0

    def test_transform_geometry_node(self):
        """Test the TransformGeometry node."""

        with TreeBuilder("TransformTest"):
            transform = g.TransformGeometry(translation=(1, 2, 3))

            assert transform.node is not None
            assert transform.node.bl_idname == "GeometryNodeTransform"

    def test_node_output_properties(self):
        """Test that output properties are accessible."""

        with TreeBuilder("OutputPropsTest"):
            bbox = g.BoundingBox()

            # Test output property accessors
            assert hasattr(bbox, "o_bounding_box")
            assert hasattr(bbox, "o_min")
            assert hasattr(bbox, "o_max")

            # They should return sockets
            assert bbox.o_bounding_box is not None
            assert bbox.o_min is not None
            assert bbox.o_max is not None


class TestComplexWorkflow:
    """Test more complex node tree workflowsocket."""

    def test_branching_workflow(self):
        """Test a workflow with branching node connectionsocket."""

        with TreeBuilder("BranchingTest"):
            pos = g.Position()

            # Use the same position node in multiple places
            _set_pos1 = g.SetPosition(position=pos, offset=(1, 0, 0))
            _set_pos2 = g.SetPosition(position=pos, offset=(0, 1, 0))

            # Both should reference the same position node
            assert len(pos.node.outputs[0].links) == 2

    def test_multiple_inputs_workflow(self):
        """Test using multiple tree inputs in a workflow."""
        tree = TreeBuilder("MultiInputTest")
        with tree.inputs:
            geo = socket.SocketGeometry(name="Geometry")
            selection = socket.SocketBoolean(name="Selection")
            translation = socket.SocketVector(name="Translation")
        with tree.outputs:
            geo_out = socket.SocketGeometry(name="Geometry")

        with tree:
            _ = (
                geo
                >> g.SetPosition(selection=selection)
                >> g.TransformGeometry(translation=translation)
                >> geo_out
            )

        # Verify all inputs are used
        group_input_node = tree.tree.nodes.get("Group Input")
        assert group_input_node is not None

        # Check that inputs have outgoing links
        assert len(group_input_node.outputs["Geometry"].links) == 1
        assert len(group_input_node.outputs["Selection"].links) == 1
        assert len(group_input_node.outputs["Translation"].links) == 1


def create_tree_chain():
    tree = TreeBuilder("MathTest")
    with tree.inputs:
        value = socket.SocketFloat()
    with tree.outputs:
        result = socket.SocketFloat("Result")

    with tree:
        _ = (
            value
            >> g.Math.add(..., 0.1)
            >> g.VectorMath.multiply(..., (2.0, 2.0, 2.0))
            >> result
        )

    return tree


def create_tree():
    tree = TreeBuilder("MathTest")
    with tree.inputs:
        value = socket.SocketFloat()

    with tree.outputs:
        result = socket.SocketFloat("Result")
    with tree:
        final = g.VectorMath.multiply(g.Math.add(value, 0.1), (2.0, 2.0, 2.0))

        final >> result

    return tree


@pytest.mark.parametrize("maker", [create_tree_chain, create_tree])
def test_math_nodes(maker):
    """Test math nodesocket."""
    tree: TreeBuilder = maker()
    # Verify all inputs are used
    node_input = tree.tree.nodes.get("Group Input")
    assert node_input is not None

    # check the default values have been property set
    assert_allclose(tree.tree.nodes["Math"].inputs[0].default_value, 0.5)
    assert_allclose(tree.tree.nodes["Math"].inputs[1].default_value, 0.1)
    assert_allclose(tree.nodes["Vector Math"].inputs[0].default_value, (0.0, 0.0, 0.0))
    assert_allclose(tree.nodes["Vector Math"].inputs[1].default_value, (2.0, 2.0, 2.0))

    # Check that inputs have outgoing links
    assert len(node_input.outputs["Value"].links) == 1
    assert len(tree.tree.nodes.get("Group Output").inputs["Result"].links) == 1

    assert tree.tree.nodes["Math"].inputs[0].links[0].from_node == tree._input_node()


def test_nodes():
    tree = TreeBuilder()
    with tree.outputs:
        output = socket.SocketGeometry()

    with tree:
        _ = (
            g.Points(1_000, position=g.RandomValue.vector())
            >> g.PointsToCurves(curve_group_id=g.RandomValue.integer(min=0, max=10))
            >> g.CurveToMesh(profile_curve=g.CurveCircle(12, radius=0.1))
            >> output
        )


def test_mix_node():
    tree = TreeBuilder()
    with tree.inputs:
        count = socket.SocketInt("Count", 50, min_value=0, max_value=100)
    with tree.outputs:
        output = socket.SocketGeometry("Instances")

    with tree:
        rotation = g.Mix.rotation(
            g.RandomValue.float(seed=g.Index()),
            g.RandomValue.vector((-pi, -pi, -pi), (pi, pi, pi)),
            (0, 0, 1),
        )

        selection = (
            g.RandomValue.boolean(0.3)
            >> g.BooleanMath.l_not()
            >> g.BooleanMath.l_and(g.RandomValue.boolean(0.8))
            >> g.BooleanMath.l_or(g.RandomValue.boolean(0.5))
            >> g.BooleanMath.equal(g.RandomValue.boolean(0.4))
            >> g.BooleanMath.l_not()
        )

        _ = (
            g.Points(count, position=g.RandomValue.vector())
            >> g.InstanceOnPoints(
                selection=selection,
                instance=g.Cube(),
                rotation=rotation,
            )
            >> g.TranslateInstances(translation=(0.0, 0.1, 0.0))
            >> output
        )

    # some nodes with different data types have a different output for each data type
    # so for rotation the socket is the 4th output - this will change in the future
    # with raibow sockets eventually
    assert len(rotation.node.outputs[3].links) == 1
    assert len(tree.nodes) == 20


def test_warning_innactive_socket():
    "Raises an error because we want to not let a user silently link sockets that won't do anything"
    with TreeBuilder():
        pos = g.Position()
        # this works because by default we link to the currently active vector sockets
        g.Mix(a_vector=pos, data_type="VECTOR")
        # this now fails because we try to link to the innactive float sockets
        with pytest.raises(RuntimeError):
            g.Mix(a_vector=pos, data_type="FLOAT")


def test_readme_tree():
    with TreeBuilder("AnotherTree", collapse=True, arrange="simple") as tree:
        with tree.inputs:
            count = socket.SocketInt("Count", 10)
        with tree.outputs:
            instances = socket.SocketGeometry("Instances")

        rotation = (
            g.RandomValue.vector(min=-1, seed=2)
            >> g.AlignRotationToVector()
            >> g.RotateRotation(rotate_by=g.AxisAngleToRotation(angle=0.3))
        )

        _ = (
            count
            >> g.Points(position=g.RandomValue.vector(min=-1))
            >> g.InstanceOnPoints(instance=g.Cube(), rotation=rotation)
            >> g.SetPosition(
                position=g.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> g.RealizeInstances()
            >> g.InstanceOnPoints(g.Cube(), instance=...)
            >> instances
        )


def test_auto_selection():
    with TreeBuilder(arrange=None) as tree:
        # this initializes the zone with two socket inputs for each of the values
        zone = g.SimulationZone(g.Value(), g.Vector())

        # this explicitly grabs the "Value" socket (which got it's name from the n.Value() node)
        # and adds 10 then attempts to plug it into the zone output (it will choose the float
        # socket instead of the vector socket because that is the most compatible)
        zone.input.outputs["Value"] + 10 >> zone.output
        # this should automatically pick the vector input socket because we are
        # explicity about the VectorMath and it will be the most compatible
        zone.input >> g.VectorMath.add(..., (1.2, 1.2, 1.2)) >> zone.output

    assert (
        tree.nodes["Math"].inputs[0].links[0].from_socket
        == zone.input.outputs["Value"].socket
    )
    assert (
        tree.nodes["Vector Math"].inputs[0].links[0].from_socket
        == zone.input.outputs["Vector"].socket
    )


def test_placeholder():
    # use ... to force a link into the second socket,
    # setting the value for the first instead
    with TreeBuilder.geometry():
        v = g.Value()
        add = v >> g.Math.add(1.0, ...)

    assert not add.node.inputs[0].links
    assert add.node.inputs[0].default_value == 1.0
    assert add.node.inputs[1].links
    assert add.node.inputs[1].links[0].from_node == v.node

    # use ... to force a link into the first socket,
    # setting the value for the second instead
    with TreeBuilder.geometry():
        v = g.Value()
        add = v >> g.Math.add(..., 1.0)

    assert not add.node.inputs[1].links
    assert add.node.inputs[1].default_value == 1.0
    assert add.node.inputs[0].links
    assert add.node.inputs[0].links[0].from_node == v.node

    with TreeBuilder.geometry():
        v = g.Color()
        mix = v >> g.Mix.color(0.3, (0.5, 0.5, 0.5, 1.0), ...)

    assert not mix._input("Factor_Float").socket.links
    assert tuple(mix._input("A_Color").socket.default_value) == (0.5, 0.5, 0.5, 1.0)
    assert mix._input("B_Color").socket.links
    assert mix._input("B_Color").socket.links[0].from_node == v.node


def test_nested_trees():
    with TreeBuilder("Tree") as tree:
        with TreeBuilder("Tree2") as tree2:
            with TreeBuilder("Tree3") as tree3:
                with tree3.outputs:
                    _ = g.Cone() >> socket.SocketGeometry("Cone")
            group = g.Group()
            group.node.node_tree = tree3.tree

            with tree2.inputs:
                items = (socket.SocketInt("Count", 10) >> g.Points(), g.Cube(), group)

            with tree2.outputs:
                _ = g.JoinGeometry(*items) >> socket.SocketGeometry("Output")

        group = g.Group()
        group.node.node_tree = tree2.tree

        with tree.outputs:
            _ = (
                group
                >> g.InstanceOnPoints(g.Grid(), instance=...)
                >> socket.SocketGeometry("Test")
            )

    assert len(tree3) == 2
    assert len(tree2) == 6
    assert len(tree2.tree.links) == 5
    assert len(tree) == 4


@pytest.mark.parametrize(
    "module,tree_type",
    [(g, "GeometryNodeTree"), (s, "ShaderNodeTree"), (c, "CompositorNodeTree")],
)
def test_add_all_nodes(module, tree_type):
    def _test_node_outputs(node: NodeBuilder):
        assert node.node is not None
        for output in node.outputs.values():
            if isinstance(output, VectorSocketLinker):
                result = -output
                assert result.node is not None
                assert result.operation == "SCALE"
                assert result.node.inputs["Scale"].default_value == -1.0
            elif isinstance(output.socket, NodeSocketFloat):
                result = -output
                assert result.node is not None
                assert result.node.inputs["Value"].links
                assert result.node.operation == "MULTIPLY"
                assert result.node.inputs["Value_001"].default_value == -1
            elif isinstance(output.socket, NodeSocketInt):
                result = -output
                assert result.node is not None
                assert result.node.inputs["Value"].links
                assert (
                    result.node.operation == "NEGATE"
                    if result.tree.tree.type == "GEOMETRY"
                    else "MULTIPLY"
                )

    with TreeBuilder(tree_type=tree_type):
        for name in dir(module):
            if not re.match(r"^([A-Z][a-z]+)+$", name):
                continue
            cls = getattr(module, name)
            if not (inspect.isclass(cls) and issubclass(cls, NodeBuilder)):
                continue
            # Test the default constructor
            node = cls()
            assert node.node is not None
            if any(
                x in node.name
                for x in ["Repeat", "Zone", "Foreach", "Element", "Simulation"]
            ):
                continue
            _test_node_outputs(node)
            # Test each classmethod defined on this class (not inherited from NodeBuilder)
            for method_name in dir(cls):
                if isinstance(
                    inspect.getattr_static(cls, method_name), classmethod
                ) and method_name not in dir(NodeBuilder):
                    node = getattr(cls, method_name)()
                    assert node.node is not None
                    _test_node_outputs(node)


def test_iter_outputs():
    with TreeBuilder("IndexSwitch"):
        switch = g.IndexSwitch(*g.SeparateXYZ(g.Position()).outputs.values())

    assert len(switch.node.outputs) == 1
    # 1 input for the index, another for the dynamic socket
    assert len(switch.node.inputs) == 5

    with TreeBuilder("MultipleOutputs") as tree:
        for name, output in g.SeparateXYZ(g.Position()).outputs.items():
            with tree.outputs:
                _ = output >> socket.SocketFloat(name)

    with TreeBuilder("MenuSwitch") as tree:
        switch = g.MenuSwitch.float(**g.SeparateXYZ(g.Position()).outputs)

    assert len(switch.inputs) == 5
