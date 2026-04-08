from functools import reduce

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy.builder import (
    NodeGroupBuilder,
    SocketLinker,
)
from nodebpy.nodes.geometry import IntegerMath
from nodebpy.nodes.geometry.groups import OffsetVector, OtherVertex


def test_custom_group_simple():
    class GroupWithoutMethod(NodeGroupBuilder):
        _name = "This Should Error"

    with TreeBuilder():
        with pytest.raises(NotImplementedError):
            GroupWithoutMethod()


def test_custom_group():
    with TreeBuilder() as tb:
        last_group = reduce(
            lambda x, y: x >> y, [OtherVertex(edge_number=x) for x in range(5)]
        )

    assert last_group.node.node_tree.name == "Other Vertex"
    assert len(tb) == 5
    assert len(tb.tree.links) == 4
    # we should be re-using the same node group for multiple instances
    assert len(bpy.data.node_groups) == 2


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


# --- Instance access returns SocketLinker (Blender) ---


def test_descriptor_get_returns_socket_linker():
    """Accessing i_* on an instance returns a SocketLinker for that socket."""
    with TreeBuilder():
        node = OtherVertex()
        linker = node.inputs["vertex_index"]

    assert isinstance(linker, SocketLinker)
    assert linker.socket_name == "Vertex Index"


def test_output_descriptor_returns_socket_linker():
    """o_* descriptors return a SocketLinker that can be chained."""
    with TreeBuilder():
        node = OtherVertex()
        out = node.outputs["other_vertex"]

    assert isinstance(out, SocketLinker)


# --- Group caching ---


def test_group_reuses_existing_node_group():
    """Second instantiation reuses the cached node group, not a new one."""
    with TreeBuilder():
        a = OtherVertex()
        b = OtherVertex()

    assert a.node.node_tree is b.node.node_tree
