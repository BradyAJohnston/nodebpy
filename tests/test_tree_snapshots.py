"""Example test showing how to use tree snapshots."""

from nodebpy import TreeBuilder, nodes, sockets
import nodebpy.nodes.geometry


def test_simple_tree_snapshot(snapshot_tree):
    """Test a simple geometry node tree snapshot."""
    with TreeBuilder("SimpleTest") as tree:
        with tree.inputs:
            input = sockets.SocketGeometry()
        with tree.outputs:
            output = sockets.SocketGeometry()

        # Create some nodes
        set_pos = nodes.SetPosition()
        transform = nodes.TransformGeometry()

        # Link them together
        input >> set_pos >> transform >> output

        # Set some properties
        transform.node.inputs["Translation"].default_value = (1.0, 2.0, 3.0)
        set_pos.node.inputs["Offset"].default_value = (0.5, 0.5, 0.5)

    # This will create/compare a snapshot of the tree structure
    assert snapshot_tree == tree


def test_complex_tree_snapshot(snapshot_tree):
    """Test a more complex geometry node tree snapshot."""
    with TreeBuilder("ComplexTest") as tree:
        # Set up interface
        with tree.inputs:
            input = sockets.SocketGeometry()
            scale = sockets.SocketFloat("Scale", 1.0, min_value=0.0, max_value=10.0)
        with tree.outputs:
            output = sockets.SocketGeometry()

        subdivide = nodes.SubdivisionSurface()
        transform1 = nodes.TransformGeometry(scale=scale)
        transform2 = nodes.TransformGeometry(scale=scale)

        _ = (
            nodebpy.nodes.geometry.JoinGeometry(
                input >> subdivide >> transform1,
                input >> transform2,
            )
            >> output
        )

        transform1.node.inputs["Translation"].default_value = (2.0, 0.0, 0.0)
        transform2.node.inputs["Translation"].default_value = (-2.0, 0.0, 0.0)
        subdivide.node.inputs["Level"].default_value = 2

    assert snapshot_tree == tree


def test_tree_with_math_nodes(snapshot_tree):
    """Test tree with math operations."""
    with TreeBuilder("MathTest") as tree:
        with tree.inputs:
            geo_in = sockets.SocketGeometry()
            value = sockets.SocketFloat("Value", 5.0)

        with tree.outputs:
            geo_out = sockets.SocketGeometry()
            result = sockets.SocketFloat("Result")

        # Create math operations using the overloaded operators
        math_result = value * 2.0 + 1.0

        # Use result in geometry
        set_pos = nodes.SetPosition(offset=math_result)
        geo_in >> set_pos >> geo_out
        math_result >> result

    assert snapshot_tree == tree
