from functools import reduce

from nodebpy import TreeBuilder
from nodebpy.nodes.geometry.groups import OtherVertex


def test_custom_group():
    with TreeBuilder() as tb:
        reduce(lambda x, y: x >> y, [OtherVertex(edge_number=x) for x in range(5)])

    assert other_vertex.node.node_tree.name == "Other Vertex"
