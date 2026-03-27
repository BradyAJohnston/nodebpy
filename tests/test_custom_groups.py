from functools import reduce

from nodebpy import TreeBuilder
from nodebpy.nodes.geometry import IntegerMath
from nodebpy.nodes.geometry.groups import OffsetVector, OtherVertex


def test_custom_group():
    with TreeBuilder() as tb:
        last_group = reduce(
            lambda x, y: x >> y, [OtherVertex(edge_number=x) for x in range(5)]
        )

    assert last_group.node.node_tree.name == "Other Vertex"
    assert len(tb) == 5
    assert len(tb.tree.links) == 4


def test_custom_group_with_offset():
    with TreeBuilder() as tb:
        last_node = reduce(
            lambda x, y: x >> y, [OffsetVector(offset=x) for x in range(5)]
        )
        offset = OffsetVector()

    assert last_node.node.node_tree.name == "Offset Vector"
    assert len(tb) == 6
    assert len(tb.tree.links) == 4
    math = offset.node.node_tree.nodes["Group Input"].outputs[0].links[0].to_node
    assert math.bl_idname == IntegerMath._bl_idname
    assert math.operation == "ADD"
