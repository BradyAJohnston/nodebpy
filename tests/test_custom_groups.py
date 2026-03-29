from functools import partial, reduce

import pytest

from nodebpy import TreeBuilder
from nodebpy.builder import (
    InputSpec,
    NodeGroupBuilder,
    OutputSpec,
    SocketFloat,
    SocketInt,
    SocketLinker,
)
from nodebpy.nodes.geometry import IntegerMath
from nodebpy.nodes.geometry.groups import OffsetVector, OtherVertex


def test_custom_group_simple():
    class GroupWithoutMethod(NodeGroupBuilder):
        _node_group_name = "This Should Error"

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


# --- Descriptor mechanics (pure Python) ---


def test_input_spec_set_name():
    """__set_name__ derives param_name by stripping i_ prefix."""
    spec = InputSpec(lambda: None)
    spec.__set_name__(None, "i_vertex_index")
    assert spec.attr_name == "i_vertex_index"
    assert spec.param_name == "vertex_index"


def test_output_spec_set_name():
    spec = OutputSpec(lambda: None)
    spec.__set_name__(None, "o_result")
    assert spec.attr_name == "o_result"


def test_input_spec_class_access_returns_descriptor():
    """Accessing on the class (not instance) returns the InputSpec itself."""

    class Fake(NodeGroupBuilder):
        _node_group_name = "Test Descriptor Access"
        i_foo = InputSpec(partial(SocketInt, "Foo"))

        @classmethod
        def _build_group(cls, tree, **kw):
            return {}

    assert isinstance(Fake.i_foo, InputSpec)


# --- Subclass registration ---


def test_init_subclass_collects_specs():
    """__init_subclass__ populates _group_inputs and _group_outputs."""

    class MyGroup(NodeGroupBuilder):
        _node_group_name = "Test Registration"
        i_a = InputSpec(partial(SocketInt, "A"))
        i_b = InputSpec(partial(SocketFloat, "B"))
        o_c = OutputSpec(partial(SocketInt, "C"))

        @classmethod
        def _build_group(cls, tree, **kw):
            return {}

    assert set(MyGroup._group_inputs.keys()) == {"i_a", "i_b"}
    assert set(MyGroup._group_outputs.keys()) == {"o_c"}


# --- Kwarg-to-socket mapping (Blender) ---


def test_kwarg_mapping():
    """InputSpec.param_name maps __init__ kwargs to socket names."""
    with TreeBuilder():
        OtherVertex(edge_number=3)

    spec = OtherVertex._group_inputs["i_edge_number"]
    assert spec.param_name == "edge_number"
    assert spec.socket_name == "Edge Number"


# --- Instance access returns SocketLinker (Blender) ---


def test_descriptor_get_returns_socket_linker():
    """Accessing i_* on an instance returns a SocketLinker for that socket."""
    with TreeBuilder():
        node = OtherVertex()
        linker = node.i_vertex_index

    assert isinstance(linker, SocketLinker)
    assert linker.socket_name == "Vertex Index"


def test_output_descriptor_returns_socket_linker():
    """o_* descriptors return a SocketLinker that can be chained."""
    with TreeBuilder():
        node = OtherVertex()
        out = node.o_other_vertex

    assert isinstance(out, SocketLinker)


# --- Group caching ---


def test_group_reuses_existing_node_group():
    """Second instantiation reuses the cached node group, not a new one."""
    with TreeBuilder():
        a = OtherVertex()
        b = OtherVertex()

    assert a.node.node_tree is b.node.node_tree
