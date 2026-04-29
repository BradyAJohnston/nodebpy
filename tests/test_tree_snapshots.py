"""Example test showing how to use tree snapshots."""

from nodebpy import TreeBuilder
from nodebpy import geometry as g


def test_simple_tree_snapshot(snapshot_tree):
    """Test a simple geometry node tree snapshot."""
    with TreeBuilder("SimpleTest") as tree:
        input = tree.inputs.geometry()
        output = tree.outputs.geometry()

        # Create some nodes
        set_pos = g.SetPosition()
        transform = g.TransformGeometry()

        # Link them together
        input >> set_pos >> transform >> output

        # Set some properties
        transform.i.translation.default_value = (1.0, 2.0, 3.0)
        set_pos.i.offset.default_value = (0.5, 0.5, 0.5)

    # This will create/compare a snapshot of the tree structure
    assert snapshot_tree == tree


def test_complex_tree_snapshot(snapshot_tree):
    """Test a more complex geometry node tree snapshot."""
    with TreeBuilder("ComplexTest") as tree:
        input = tree.inputs.geometry()
        scale = tree.inputs.float("Scale", 1.0, min_value=0.0, max_value=10.0)
        output = tree.outputs.geometry()

        subdivide = g.SubdivisionSurface()
        transform1 = g.TransformGeometry(scale=scale)
        transform2 = g.TransformGeometry(scale=scale)

        _ = (
            g.JoinGeometry(
                input >> subdivide >> transform1,
                input >> transform2,
            )
            >> output
        )

        transform1.i.translation.default_value = (2.0, 0.0, 0.0)
        transform2.i.translation.default_value = (-2.0, 0.0, 0.0)
        subdivide.i.level.default_value = 2

    assert snapshot_tree == tree


def test_tree_with_math_nodes(snapshot_tree):
    """Test tree with math operations."""
    with TreeBuilder("MathTest") as tree:
        geo_in = tree.inputs.geometry()
        value = tree.inputs.float("Value", 5.0)
        geo_out = tree.outputs.geometry()
        result = tree.outputs.float("Result")

        # Create math operations using the overloaded operators
        math_result = value * 2.0 + 1.0

        # Use result in geometry
        set_pos = g.SetPosition(offset=math_result)
        geo_in >> set_pos >> geo_out
        math_result >> result

    assert snapshot_tree == tree
