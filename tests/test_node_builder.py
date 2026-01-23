"""
Tests for the node builder API.

Tests the TreeBuilder, NodeBuilder, and the >> operator chaining system.
"""

import re
from math import pi

import bpy
import pytest
from numpy.testing import assert_allclose

from nodebpy import TreeBuilder
from nodebpy import nodes as n
from nodebpy import sockets as s


class TestTreeBuilder:
    """Tests for TreeBuilder basic functionality."""

    def test_tree_creation(self):
        """Test creating a basic node tree."""
        tree = TreeBuilder("TestTree")
        assert tree.tree is not None
        assert tree.tree.name == "TestTree"
        assert isinstance(tree.tree, bpy.types.GeometryNodeTree)

    def test_interface_definition(self):
        """Test defining tree interface with socket types."""
        tree = TreeBuilder("InterfaceTest")
        with tree.inputs:
            s.SocketGeometry()
            s.SocketBoolean("Selection", True)
            s.SocketVector("Offset", (1.0, 2.0, 3.0))

        with tree.outputs:
            s.SocketGeometry()
            s.SocketInt("Count")

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
            s.SocketBoolean("Selection", True)
            s.SocketVector("Offset", (1.0, 2.0, 3.0))
            s.SocketFloat("Scale", 2.5, min_value=0.0, max_value=10.0)
        with tree.outputs:
            s.SocketGeometry("Geometry")

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
            pos = n.Position()
            assert pos.node is not None
            assert pos.tree == tree

    def test_context_manager_node_creation(self):
        """Test that nodes created in context use the active tree."""

        with TreeBuilder("NodeCreationTest") as tree:
            node1 = n.Position()
            node2 = n.SetPosition()

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
            pos = n.Position()
            set_pos = n.SetPosition()

            # Chain with >> operator
            result = pos >> set_pos

            # Should return the right-hand node
            assert result == set_pos

            # Should create a link between the nodes
            links = tree.tree.links
            assert len(links) > 0

    def test_multi_node_chaining(self):
        """Test chaining multiple nodes together."""
        tree = TreeBuilder("MultiChainTest")
        with tree.inputs:
            i_geo = s.SocketGeometry()
        with tree.outputs:
            o_geo = s.SocketGeometry()

        with tree:
            # Chain multiple nodes
            _ = (
                i_geo
                >> n.SetPosition()
                >> n.TransformGeometry(translation=(0, 0, 1))
                >> o_geo
            )

        # Check that links were created
        assert len(tree.tree.links) >= 3


class TestExamples:
    """Tests that replicate the original example functions."""

    def test_example_basic(self):
        """Test the basic example from example.py."""
        tree = TreeBuilder("ExampleTree")

        with tree.inputs:
            i_geo = s.SocketGeometry()
            selection = s.SocketBoolean("Selection", True)
            offset = s.SocketVector("Offset", (1.0, 2.0, 3.0))
        with tree.outputs:
            o_geo = s.SocketGeometry()

        with tree:
            _ = (
                i_geo
                >> n.SetPosition(
                    selection=selection,
                    position=n.Position() * 2.0,
                    offset=offset,
                )
                >> n.TransformGeometry(translation=(0, 0, 1))
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
            i_geo = s.SocketGeometry("Geometry")
            selection = s.SocketBoolean("Selection", True)

        with tree.outputs:
            o_geo = s.SocketGeometry("Geometry")
            count = s.SocketInt("Count")

        with tree:
            # Access multiple named sockets
            pos = i_geo >> n.SetPosition(selection=selection)
            _ = pos >> n.DomainSize() >> count
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
    """Tests for generated node classes."""

    def test_position_node(self):
        """Test the Position input node."""
        tree = TreeBuilder("PositionTest")

        with tree:
            pos = n.Position()
            assert pos.node is not None
            assert pos.node.bl_idname == "GeometryNodeInputPosition"

    def test_set_position_node(self):
        """Test the SetPosition node with parameters."""
        tree = TreeBuilder("SetPositionTest")
        with tree.inputs:
            in_geo = s.SocketGeometry()
        with tree.outputs:
            out_geo = s.SocketGeometry()

        with tree:
            pos = n.Position()
            set_pos = n.SetPosition(position=pos)
            in_geo >> set_pos >> out_geo

            assert set_pos.node is not None
            assert set_pos.node.bl_idname == "GeometryNodeSetPosition"

            # Check that the position input was linked
            assert len(set_pos.node.inputs["Position"].links) > 0

    def test_transform_geometry_node(self):
        """Test the TransformGeometry node."""

        with TreeBuilder("TransformTest"):
            transform = n.TransformGeometry(translation=(1, 2, 3))

            assert transform.node is not None
            assert transform.node.bl_idname == "GeometryNodeTransform"

    def test_node_output_properties(self):
        """Test that output properties are accessible."""

        with TreeBuilder("OutputPropsTest"):
            bbox = n.BoundingBox()

            # Test output property accessors
            assert hasattr(bbox, "o_bounding_box")
            assert hasattr(bbox, "o_min")
            assert hasattr(bbox, "o_max")

            # They should return sockets
            assert bbox.o_bounding_box is not None
            assert bbox.o_min is not None
            assert bbox.o_max is not None


class TestComplexWorkflow:
    """Test more complex node tree workflows."""

    def test_branching_workflow(self):
        """Test a workflow with branching node connections."""

        with TreeBuilder("BranchingTest"):
            pos = n.Position()

            # Use the same position node in multiple places
            _set_pos1 = n.SetPosition(position=pos, offset=(1, 0, 0))
            _set_pos2 = n.SetPosition(position=pos, offset=(0, 1, 0))

            # Both should reference the same position node
            assert len(pos.node.outputs[0].links) == 2

    def test_multiple_inputs_workflow(self):
        """Test using multiple tree inputs in a workflow."""
        tree = TreeBuilder("MultiInputTest")
        with tree.inputs:
            geo = s.SocketGeometry(name="Geometry")
            selection = s.SocketBoolean(name="Selection")
            translation = s.SocketVector(name="Translation")
        with tree.outputs:
            geo_out = s.SocketGeometry(name="Geometry")

        with tree:
            _ = (
                geo
                >> n.SetPosition(selection=selection)
                >> n.TransformGeometry(translation=translation)
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
        value = s.SocketFloat()
    with tree.outputs:
        result = s.SocketFloat("Result")

    with tree:
        _ = (
            value
            >> n.Math.add(..., 0.1)
            >> n.VectorMath.multiply(..., (2.0, 2.0, 2.0))
            >> result
        )

    return tree


def create_tree():
    tree = TreeBuilder("MathTest")
    with tree.inputs:
        value = s.SocketFloat()

    with tree.outputs:
        result = s.SocketFloat("Result")
    with tree:
        final = n.VectorMath.multiply(n.Math.add(value, 0.1), (2.0, 2.0, 2.0))

        final >> result

    return tree


@pytest.mark.parametrize("maker", [create_tree_chain, create_tree])
def test_math_nodes(maker):
    """Test math nodes."""
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
        output = s.SocketGeometry()

    with tree:
        _ = (
            n.Points(1_000, position=n.RandomValue.vector())
            >> n.PointsToCurves(curve_group_id=n.RandomValue.integer(min=0, max=10))
            >> n.CurveToMesh(profile_curve=n.CurveCircle(12, radius=0.1))
            >> output
        )


def test_mix_node():
    tree = TreeBuilder()
    with tree.inputs:
        count = s.SocketInt("Count", 50, min_value=0, max_value=100)
    with tree.outputs:
        output = s.SocketGeometry("Instances")

    with tree:
        rotation = n.Mix.rotation(
            n.RandomValue.float(seed=n.Index()),
            n.RandomValue.vector((-pi, -pi, -pi), (pi, pi, pi)),
            (0, 0, 1),
        )

        selection = (
            n.RandomValue.boolean(probability=0.3)
            >> n.BooleanMath.l_not()
            >> n.BooleanMath.l_and(n.RandomValue.boolean(probability=0.8))
            >> n.BooleanMath.l_or(n.RandomValue.boolean(probability=0.5))
            >> n.BooleanMath.equal(n.RandomValue.boolean(probability=0.4))
            >> n.BooleanMath.l_not()
        )

        _ = (
            n.Points(count, position=n.RandomValue.vector())
            >> n.InstanceOnPoints(
                selection=selection,
                instance=n.Cube(),
                rotation=rotation,
            )
            >> n.TranslateInstances(translation=(0.0, 0.1, 0.0))
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
        pos = n.Position()
        mix = n.Mix.vector()
        # this works because by default we link to the currently active vector sockets
        n.Mix(a_vector=pos, data_type="VECTOR")
        # this now fails because we try to link to the innactive float sockets
        with pytest.raises(RuntimeError):
            n.Mix(a_vector=pos, data_type="FLOAT")


def test_readme_tree():
    with TreeBuilder("AnotherTree") as tree:
        with tree.inputs:
            count = s.SocketInt("Count")
        with tree.outputs:
            instances = s.SocketGeometry("Instances")

        rotation = (
            n.RandomValue.vector(min=(-1, -1, -1), seed=2)
            >> n.AlignRotationToVector()
            >> n.RotateRotation(
                rotate_by=n.AxisAngleToRotation(angle=0.3),
                rotation_space="LOCAL",
            )
        )

        _ = (
            count
            >> n.Points(position=n.RandomValue.vector(min=(-1, -1, -1)))
            >> n.InstanceOnPoints(instance=n.Cube(), rotation=rotation)
            >> n.SetPosition(
                position=n.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> n.RealizeInstances()
            >> n.InstanceOnPoints(n.Cube(), instance=...)
            >> instances
        )


def test_auto_selection():
    with TreeBuilder(arrange=False) as tree:
        # this initializes the zone with two socket inputs for each of the values
        zone = n.SimulationZone(n.Value(), n.Vector())

        # this explicitly grabs the "Value" socket (which got it's name from the n.Value() node)
        # and adds 10 then attempts to plug it into the zone output (it will choose the float
        # socket instead of the vector socket because that is the most compatible)
        zone.input.outputs["Value"] + 10 >> zone.output
        # this should automatically pick the vector input socket because we are
        # explicity about the VectorMath and it will be the most compatible
        zone.input >> n.VectorMath.add(..., (1.2, 1.2, 1.2)) >> zone.output

    assert (
        tree.nodes["Math"].inputs[0].links[0].from_socket
        == zone.input.outputs["Value"].socket
    )
    assert (
        tree.nodes["Vector Math"].inputs[1].links[0].from_socket
        == zone.input.outputs["Vector"].socket
    )


def test_add_all_nodes():
    with TreeBuilder():
        for name in dir(n):
            if re.match(r"^[A-Z]", name):
                getattr(n, name)()
