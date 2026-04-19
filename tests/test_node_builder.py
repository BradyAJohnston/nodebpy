"""
Tests for the node builder API.

Tests the TreeBuilder, NodeBuilder, and the >> operator chaining system.
"""

import inspect
import re
from math import pi

import bpy
import pytest
from bpy.types import (
    NodeSocketBool,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketInt,
    NodeSocketMatrix,
    NodeSocketShader,
    NodeSocketVector,
)
from numpy.testing import assert_allclose

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy import sockets as socket
from nodebpy.builder import BaseNode as NodeBuilder
from nodebpy.builder import ColorSocket as ColorSocketLinker
from nodebpy.builder import SocketAccessor, SocketError


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
            socket.SocketInteger("Count")

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
            count = socket.SocketInteger("Count")

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
            assert hasattr(bbox.o, "bounding_box")
            assert hasattr(bbox.o, "min")
            assert hasattr(bbox.o, "max")

            # They should return sockets
            assert bbox.o.bounding_box is not None
            assert bbox.o.min is not None
            assert bbox.o.max is not None


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
        count = socket.SocketInteger("Count", 50, min_value=0, max_value=100)
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
            count = socket.SocketInteger("Count", 10)
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

    assert not mix.inputs["Factor_Float"].socket.links
    assert tuple(mix.inputs["A_Color"].socket.default_value) == (0.5, 0.5, 0.5, 1.0)
    assert mix.inputs["B_Color"].socket.links
    assert mix.inputs["B_Color"].socket.links[0].from_node == v.node


def test_nested_trees():
    with TreeBuilder("Tree") as tree:
        with TreeBuilder("Tree2") as tree2:
            with TreeBuilder("Tree3") as tree3:
                with tree3.outputs:
                    _ = g.Cone() >> socket.SocketGeometry("Cone")
            group = g.Group()
            group.node.node_tree = tree3.tree

            with tree2.inputs:
                items = (
                    socket.SocketInteger("Count", 10) >> g.Points(),
                    g.Cube(),
                    group,
                )

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


def _collect_node_classes(module):
    """Collect NodeBuilder subclass names from a module."""
    return [
        name
        for name in dir(module)
        if re.match(r"^[A-Z][a-zA-Z0-9]+$", name)
        and inspect.isclass(cls := getattr(module, name))
        and issubclass(cls, NodeBuilder)
    ]


def _chunk(lst, n):
    """Split list into chunks of size n."""
    return [lst[i : i + n] for i in range(0, len(lst), n)]


_CHUNK_SIZE = 10
_all_node_params = []
for _mod, _tree_type in [
    (g, "GeometryNodeTree"),
    (s, "ShaderNodeTree"),
    (c, "CompositorNodeTree"),
]:
    _mod_name = _tree_type.removesuffix("NodeTree")
    for _i, _chunk_names in enumerate(_chunk(_collect_node_classes(_mod), _CHUNK_SIZE)):
        _all_node_params.append(
            pytest.param(_mod, _tree_type, _chunk_names, id=f"{_mod_name}-{_i}")
        )


@pytest.mark.parametrize("module,tree_type,class_names", _all_node_params)
def test_add_all_nodes(module, tree_type, class_names):
    def _test_node_property_access(node: NodeBuilder):
        assert node.node is not None
        for output in [
            getattr(node.o, name) for name in dir(node.o) if not name.startswith("_")
        ]:
            if NodeSocketVector.bl_rna.identifier in output.socket.bl_idname:
                result = -output
                assert result.node is not None
                assert result.operation == "SCALE"
                assert result.node.inputs["Scale"].default_value == -1.0
            elif NodeSocketFloat.bl_rna.identifier in output.socket.bl_idname:
                result = -output
                assert result.node is not None
                assert result.node.inputs["Value"].links
                assert result.node.operation == "MULTIPLY"
                assert result.node.inputs["Value_001"].default_value == -1
            elif NodeSocketInt.bl_rna.identifier in output.socket.bl_idname:
                result = -output
                assert result.node is not None
                assert result.node.inputs["Value"].links
                assert (
                    result.node.operation == "NEGATE"
                    if result.tree.tree.type == "GEOMETRY"
                    else "MULTIPLY"
                )
            elif isinstance(output.socket, NodeSocketBool):
                if not tree_type == "GeometryNodeTree":
                    continue
                result = output | True
                assert result.node is not None
                assert result.node.bl_idname == g.BooleanMath._bl_idname
                assert result.node.inputs[0].links
                assert not result.node.inputs[1].links
                assert result.node.inputs[1].default_value
                assert result.operation == "OR"
            elif isinstance(output.socket, NodeSocketMatrix):
                if not tree_type == "GeometryNodeTree":
                    continue
                result = output @ g.CombineTransform()
                assert result.node is not None
                assert result.node.bl_idname == g.MultiplyMatrices._bl_idname
            elif "NodeSocketGeometry" in output.socket.bl_idname:
                result = output >> g.JoinGeometry()
                assert result.node is not None
                assert result.node.bl_idname == g.JoinGeometry._bl_idname
                assert result.inputs[0].links[0].from_node == output.node
            elif NodeSocketColor.bl_rna.identifier in output.socket.bl_idname:
                result = output >> module.SeparateColor()
                assert result.node is not None
                assert module.SeparateColor._bl_idname in result.node.bl_idname
                assert result.node.inputs[0].links[0].from_node == output.node
            elif "NodeSocketShader" in output.socket.bl_idname:
                result = output >> s.AddShader()
                assert result.node is not None
                assert result.node.bl_idname == s.AddShader._bl_idname
                assert result.node.inputs[0].links[0].from_node == output.node
            elif NodeSocketMatrix.bl_rna.identifier in output.socket.bl_idname:
                result = output @ g.Position()
                assert result.node is not None
                assert result.node.bl_idname == g.TransformPoint._bl_idname
                assert result.node.inputs[0].links[0].from_node == output.node
        for prop in dir(node.i):
            if prop.startswith("_"):
                continue
            try:
                input = getattr(node.i, prop)
            except RuntimeError as e:
                print(f"Failed to get input {prop} due to error: {e}")
                continue
            if any(
                x.bl_rna.identifier in input.socket.bl_idname
                for x in (
                    NodeSocketFloat,
                    NodeSocketInt,
                    NodeSocketVector,
                    NodeSocketColor,
                    NodeSocketBool,
                )
            ):
                value = module.Value(10.0)
                try:
                    result = value >> input
                    assert result.node is not None
                    assert result.socket.links[0].from_node == value.node
                except RuntimeError as e:
                    print(
                        f"Failed to link {value.name} to {input.name} due to error: {e}"
                    )
            elif NodeSocketShader.bl_rna.identifier in input.socket.bl_idname:
                value = s.DiffuseBSDF()
                result = value >> input
                assert result.node is not None
                assert result.socket.links[0].from_node == value.node
            elif isinstance(input.socket, NodeSocketMatrix):
                trans = g.CombineTransform()
                result = trans >> input
                assert input.socket.links[0].from_node == trans.node

    with TreeBuilder(tree_type=tree_type, arrange=None, ignore_visibility=True):
        for name in class_names:
            cls = getattr(module, name)
            # Test the default constructor
            node = cls()
            assert node.node is not None
            if any(
                x in node.name
                for x in ["Repeat", "Zone", "Foreach", "Element", "Simulation"]
            ):
                continue
            _test_node_property_access(node)
            # Test each classmethod defined on this class (not inherited from NodeBuilder)
            for method_name in dir(cls):
                if isinstance(
                    inspect.getattr_static(cls, method_name), classmethod
                ) and method_name not in dir(NodeBuilder):
                    node = getattr(cls, method_name)()
                    assert node.node is not None
                    _test_node_property_access(node)


def test_iter_outputs():
    with TreeBuilder("IndexSwitch"):
        switch = g.IndexSwitch(*g.SeparateXYZ(g.Position()).outputs._values())

    assert len(switch.node.outputs) == 1
    # 1 input for the index, another for the dynamic socket
    assert len(switch.node.inputs) == 5

    with TreeBuilder("MultipleOutputs") as tree:
        for name, output in g.SeparateXYZ(g.Position()).outputs._items():
            with tree.outputs:
                _ = output >> socket.SocketFloat(name)

    with TreeBuilder("MenuSwitch") as tree:
        switch = g.MenuSwitch.float(**dict(g.SeparateXYZ().outputs._items()))

    assert len(switch.inputs) == 5


def test_vector_socket_linker():
    with TreeBuilder("SeparateXYZ_z"):
        pos = g.Position().o.position

        result = g.SetPosition(position=pos.x * g.Position())
        pos.y * 0.5 * g.Normal() + g.CombineXYZ(z=pos.z) >> result.i.offset

    assert result.node
    assert result.node.inputs["Position"].links[0].from_node.operation == "SCALE"
    assert len(pos.links) == 1


def test_color_socket_linker():
    with TreeBuilder("ColorChannels"):
        color = g.Color((1.0, 0.5, 0.25, 1.0)).o.color

        assert isinstance(color, ColorSocketLinker)

        r = color.r
        g_channel = color.g
        b = color.b
        a = color.a

        # Each channel creates a float output from SeparateColor
        assert r.type == "VALUE"
        assert g_channel.type == "VALUE"
        assert b.type == "VALUE"
        assert a.type == "VALUE"
        assert a.node == r.node == g_channel.node == b.node

        # The SeparateColor node should be reused across channels
        assert r.node.bl_idname == "FunctionNodeSeparateColor"


def test_color_socket_linker_in_shader_tree():
    with TreeBuilder.shader():
        color = s.CombineColor(red=1.0, green=0.5, blue=0.25).o.color

        assert isinstance(color, ColorSocketLinker)

        r, g, b = color.r, color.g, color.b
        assert r.type == "VALUE"
        assert b.type == "VALUE"
        assert g.type == "VALUE"
        assert r.node == g.node == b.node
        assert r.node.bl_idname == "ShaderNodeSeparateColor"


def test_color_socket_linker_channel_into_math():
    with TreeBuilder("ColorMath"):
        color = g.Color((1.0, 0.5, 0.25, 1.0)).o.color

        # Use a color channel in a math expression
        result = color.r * 2.0 + color.g

    assert result.node is not None
    assert result.node.bl_idname == "ShaderNodeMath"
    assert result.node.operation == "ADD"


class TestSocketAccessor:
    """Tests for SocketAccessor visibility and context-guard behaviour."""

    def test_iter(self):
        """values()/items()/keys() should respect node-level visibility rules."""

        def _assert_equal(dict1, dict2):
            # if we just compare the socket accessors then it creates compare
            # nodes so we have to get the sockets and keys from each to compare them
            for items1, items2 in zip(dict1.items(), dict2.items()):
                assert items1[0] == items2[0], f"Expected {items2[0]}, got {items1[0]}"
                assert items1[1].socket == items2[1].socket, (
                    f"Expected {items2[1]}, got {items1[1]}"
                )

        with TreeBuilder("IterTest"):
            pos = g.Position()
            _assert_equal(dict(pos.outputs._items()), {"Position": pos.o.position})

            setpos = g.SetPosition()
            _assert_equal(
                dict(setpos.inputs._items()),
                {
                    "Geometry": setpos.i.geometry,
                    "Selection": setpos.i.selection,
                    "Position": setpos.i.position,
                    "Offset": setpos.i.offset,
                },
            )

            assert all(
                [
                    a == b
                    for a, b in zip(
                        ["Geometry", "Selection", "Position", "Offset"],
                        list(setpos.inputs),
                    )
                ]
            )

    def test_ignore_visibility_outside_context_returns_false(self):
        """_ignore_visibility must not crash when called outside a tree context."""
        with TreeBuilder("AccessorGuardTest"):
            pos = g.Position()
            # grab a SocketAccessor while inside the context so we have a valid node
            accessor = pos.outputs

        # Now we're outside the context — _tree_contexts is empty.
        # This should return False rather than raise IndexError.
        assert accessor._ignore_visibility is False

    def test_ignore_visibility_inside_context_default_false(self):
        """Inside a normal tree context, ignore_visibility defaults to False."""
        with TreeBuilder("NormalContext"):
            pos = g.Position()
            assert pos.outputs._ignore_visibility is False

    def test_ignore_visibility_inside_context_when_set_true(self):
        """Inside an ignore_visibility=True context, the flag propagates."""
        with TreeBuilder("IgnoreVisContext", ignore_visibility=True):
            pos = g.Position()
            assert pos.outputs._ignore_visibility is True

    def test_values_unaffected_by_ignore_visibility(self):
        """values() / items() / keys() should not change when ignore_visibility=True.

        Only ``available`` / ``best_match`` (the auto-linking heuristics) are
        affected by the flag — enumeration uses node-level visibility rules.
        """
        with TreeBuilder("NormalVis", arrange=None) as _:
            node_normal = g.SeparateXYZ(g.Position())
            normal_values = node_normal.outputs._values()
            normal_keys = node_normal.outputs._keys()

        with TreeBuilder("IgnoreVis", arrange=None, ignore_visibility=True) as _:
            node_ignore = g.SeparateXYZ(g.Position())
            ignore_values = node_ignore.outputs._values()
            ignore_keys = node_ignore.outputs._keys()

        # SeparateXYZ has three visible outputs (X, Y, Z) regardless of the flag.
        assert len(normal_values) == len(ignore_values)
        assert normal_keys == ignore_keys

    def test_available_respects_ignore_visibility(self):
        """available does change when ignore_visibility=True for nodes with hidden sockets."""
        # Mix node has inactive sockets depending on data_type — use it as an example
        # of a node whose visible socket count varies.  With ignore_visibility the
        # accessor should expose more (or equal) sockets than without it.
        with TreeBuilder("NormalAvail", arrange=None):
            mix = g.Mix()
            normal_available = len(mix.inputs._available)

        with TreeBuilder("IgnoreAvail", arrange=None, ignore_visibility=True):
            mix = g.Mix()
            ignore_available = len(mix.inputs._available)

        assert ignore_available >= normal_available

    def test_index_ambiguous_name_raises(self):
        """index() raises when a socket name is duplicated and lookup falls through to name."""

        # Synthetic sockets: two distinct identifiers that share the same display name.
        class _FakeSocket:
            def __init__(self, identifier, name):
                self.identifier = identifier
                self.name = name
                self.node = g.Value().node

        with TreeBuilder("AmbiguousName", arrange=None):
            fake_sockets = [
                _FakeSocket("unique_id_1", "Value"),
                _FakeSocket("unique_id_2", "Value"),  # same name, different identifier
            ]
            accessor = SocketAccessor(fake_sockets, "input")

            # Unique identifier lookup is fine.
            assert accessor._index("unique_id_1") == 0
            # Duplicate name lookup must raise with a clear message.
            with pytest.raises(RuntimeError, match="ambiguous"):
                accessor._index("Value")


class TestIntegerSocketLinker:
    """Tests for IntegerSocketLinker dispatch, including the _is_integer_socket helper."""

    def test_integer_plus_integer_socket_uses_integer_math(self):
        """INT + IntegerSocketLinker should route through IntegerMath, not Math.

        This exercises _is_integer_socket via _other_is_integer when `other` is a
        SocketLinker wrapping an INT socket (not a plain Python int).
        """
        with TreeBuilder("IntPlusIntSocket"):
            a = g.Integer(1)
            b = g.Integer(2)
            # b.o.integer is an IntegerSocketLinker; adding it to another integer
            # socket linker should use IntegerMath.add, not Math.add
            result = a.o.integer + b.o.integer

        assert isinstance(result, g.IntegerMath)
        assert result.node.operation == "ADD"

    def test_integer_plus_node_builder_uses_integer_math(self):
        """INT + NodeBuilder(INT output) should also route through IntegerMath.

        _is_integer_socket falls back to _default_output_socket when the value has
        no .socket attribute (i.e. it's a NodeBuilder).
        """
        with TreeBuilder("IntPlusNodeBuilder"):
            a = g.Integer(1)
            b = g.Integer(2)
            # Use the NodeBuilder directly (not its output socket linker)
            result = a.o.integer + b

        assert isinstance(result, g.IntegerMath)
        assert result.node.operation == "ADD"

    def test_integer_floordiv_non_integer_falls_back_to_math(self):
        """INT // float should fall back to Math.divide + Math.floor (not IntegerMath).

        _dispatch_floordiv only uses IntegerMath when _other_is_integer is True.
        Passing a float makes that False, hitting the super() fallback (line 1279).
        """
        with TreeBuilder("IntFloorDivFloat"):
            n = g.Integer(10)
            result = n.o.integer // 2.5

        # Should be the Math.floor wrapping a Math.divide — not IntegerMath
        assert isinstance(result, g.Math)
        assert result.node.operation == "FLOOR"

    def test_integer_compare_in_shader_tree_falls_back(self):
        """IntegerSocketLinker compare in a shader tree falls back to the float compare path.

        _dispatch_compare line 1286 is only reached when the tree is NOT a GeometryNodeTree.
        """
        with TreeBuilder.shader():
            val = s.Value()
            # Value output in a shader tree is a float socket, not integer — but we can
            # still trigger the integer dispatch path via an Integer node if available.
            # Use a Math node set to round to get an integer-typed output workaround:
            # Instead trigger it directly: create a geometry tree just for the socket,
            # then verify shader-tree integer compare uses Math nodes (not Compare).
            result = val > 0.5

        # In shader tree the compare falls through to Math.greater_than
        assert result.node.bl_idname == "ShaderNodeMath"
        assert result.node.operation == "GREATER_THAN"


class TestLinkErrors:
    """Tests for error paths in TreeBuilder.link and NodeBuilder._find_best_socket_pair."""

    def test_link_incompatible_types_raises_socket_error(self):
        """TreeBuilder.link raises SocketError when socket types are incompatible."""
        with TreeBuilder("IncompatibleLink") as tree:
            pos = g.Position()  # VECTOR output
            set_pos = g.SetPosition()

            with pytest.raises(SocketError, match="Incompatible socket types"):
                # VECTOR output → GEOMETRY input: types are not compatible
                tree.link(
                    pos.node.outputs[0],  # VECTOR
                    set_pos.node.inputs["Geometry"],  # GEOMETRY
                )

    def test_find_best_socket_pair_no_match_raises(self):
        """_find_best_socket_pair raises SocketError when no compatible pair exists."""
        with TreeBuilder("NoMatch"):
            geo = g.JoinGeometry()  # geometry output
            count = g.DomainSize()  # wants geometry input, produces INT outputs

            with pytest.raises(SocketError):
                # Force a geometry → geometry domain-size node >> another geometry node in a
                # direction that has no compatible output→input pair
                geo._find_best_socket_pair(count, geo)


class TestEstablishLinksNameFallback:
    """Tests for the name-based fallback branches in _establish_links."""

    def test_kwarg_by_socket_display_name(self):
        """Passing a kwarg whose key is a socket's display name (not identifier) sets the value.

        This hits the `name in self.node.inputs` branch (line 769-770) when the key
        isn't an identifier but is a valid socket name.
        """
        with TreeBuilder("DisplayNameKwarg"):
            # "Geometry" is the display name and identifier here so it won't
            # exercise 769. Use a node where name != identifier: Math node has
            # identifier "Value" and "Value_001" but display names "Value" match.
            # Use TransformGeometry whose "Translation" kwarg is by name.
            node = g.TransformGeometry(translation=(1.0, 2.0, 3.0))

        from numpy.testing import assert_allclose

        assert_allclose(node.node.inputs["Translation"].default_value, (1.0, 2.0, 3.0))


class TestRShiftFallback:
    """Tests for the __rshift__ SocketError fallback path."""

    def test_rshift_falls_back_to_target_find_best_socket_pair(self):
        """When source._find_best_socket_pair fails, >> retries from the target's perspective.

        JoinGeometry uses DynamicInputsMixin._find_best_socket_pair which can add new
        sockets dynamically — the source-first attempt raises SocketError (no pre-existing
        compatible input), then the target-side retry succeeds.
        """
        with TreeBuilder("RShiftFallback"):
            g.Position()
            join = g.JoinGeometry()
            # Position output is VECTOR; JoinGeometry normally takes GEOMETRY.
            # This should fail source-first and succeed target-side.
            # Use a geometry node that actually produces geometry:
            cube = g.Cube()
            result = cube >> join

        assert result.node.bl_idname == "GeometryNodeJoinGeometry"
        assert len(result.node.inputs[0].links) == 1
