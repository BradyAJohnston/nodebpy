from functools import reduce

from nodebpy import TreeBuilder
from nodebpy.nodes.geometry.groups import OtherVertex


def test_custom_group():
    with TreeBuilder() as tb:
        last_group = reduce(
            lambda x, y: x >> y, [OtherVertex(edge_number=x) for x in range(5)]
        )

    assert last_group.node.node_tree.name == "Other Vertex"
    assert len(tb) == 5
    assert len(tb.tree.links) == 4
