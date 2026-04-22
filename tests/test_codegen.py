# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for nodebpy.codegen.to_python() — node tree → Python code generation."""

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.codegen import to_python


# ---------------------------------------------------------------------------
# Assertion tests (TDD baseline — each verifies one specific behaviour)
# ---------------------------------------------------------------------------


def test_single_node():
    """Minimal: one node, no links. Validates registry lookup and var naming."""
    with TreeBuilder("SingleNode") as tree:
        g.Position()
    code = to_python(tree)
    assert "g.Position()" in code
    assert "position" in code
    assert 'TreeBuilder("SingleNode")' in code


def test_boilerplate_imports():
    """Generated code contains the standard import line."""
    with TreeBuilder("Imports") as tree:
        g.Position()
    code = to_python(tree)
    assert "from nodebpy import geometry as g, TreeBuilder" in code


def test_with_interface_inputs():
    """Interface inputs are emitted as tree.inputs.*() calls."""
    with TreeBuilder("WithInputs") as tree:
        tree.inputs.geometry()
        tree.inputs.float("Scale", 1.0)
    code = to_python(tree)
    assert "tree.inputs.geometry(" in code
    assert "tree.inputs.float(" in code


def test_with_interface_outputs():
    """Interface outputs are emitted as tree.outputs.*() calls."""
    with TreeBuilder("WithOutputs") as tree:
        tree.outputs.geometry()
    code = to_python(tree)
    assert "tree.outputs.geometry(" in code


def test_interface_default_value():
    """Interface float input with non-zero default value includes that value."""
    with TreeBuilder("InterfaceDefault") as tree:
        tree.inputs.float("Scale", 2.5)
        tree.outputs.geometry()
    code = to_python(tree)
    assert "2.5" in code
    assert '"Scale"' in code


def test_non_default_property():
    """Keyword-only node property is emitted when it differs from the default."""
    with TreeBuilder("WithProp") as tree:
        g.Math(operation="MULTIPLY")
    code = to_python(tree)
    assert 'operation="MULTIPLY"' in code


def test_default_property_omitted():
    """Keyword-only property is omitted when it matches the constructor default."""
    with TreeBuilder("DefaultProp") as tree:
        g.Math(operation="ADD")  # ADD is the default
    code = to_python(tree)
    assert "operation=" not in code


def test_unlinked_non_default_input():
    """An unlinked socket with a non-default value emits a literal kwarg."""
    with TreeBuilder("NonDefaultInput") as tree:
        g.Math(value=3.14)
    code = to_python(tree)
    assert "3.14" in code


def test_fanout_assigns_variable():
    """Every node gets a named variable (Phase 1 rule)."""
    with TreeBuilder("FanOut") as tree:
        noise = g.NoiseTexture()
        g.SetPosition(offset=noise)
        g.SetPosition(offset=noise)
    code = to_python(tree)
    assert "noise_texture = g.NoiseTexture()" in code


def test_linked_input_uses_upstream_var():
    """A linked input is expressed using the upstream node's variable name."""
    with TreeBuilder("LinkedInput") as tree:
        pos = g.Position()
        g.SetPosition(offset=pos)
    code = to_python(tree)
    assert "set_position = g.SetPosition(" in code
    assert "position" in code


def test_interface_geo_links_to_output():
    """Interface input geo linked through node to output emits >> connection."""
    with TreeBuilder("GeoPassThrough") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        g.SetPosition(geo_in) >> geo_out
    code = to_python(tree)
    assert ">>" in code


def test_dedup_variable_names():
    """Two nodes with the same label get distinct variable names."""
    with TreeBuilder("DedupVars") as tree:
        g.SetPosition()
        g.SetPosition()
    code = to_python(tree)
    # The second should have a suffix
    assert "set_position_1" in code


def test_output_is_valid_python():
    """Generated code is syntactically valid Python."""
    import ast

    with TreeBuilder("ValidPython") as tree:
        geo_in = tree.inputs.geometry()
        noise = g.NoiseTexture(scale=3.0)
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry()
    code = to_python(tree)
    ast.parse(code)  # raises SyntaxError if invalid


def test_round_trip_executes():
    """Generated code can be exec'd without raising."""
    import ast

    with TreeBuilder("RoundTrip") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        g.SetPosition(geo_in) >> geo_out

    original_node_count = len(tree.tree.nodes)
    code = to_python(tree)

    # Must be valid syntax first
    ast.parse(code)

    ns: dict = {}
    exec(code, ns)  # noqa: S102

    new_tree: TreeBuilder = ns.get("tree")  # type: ignore[assignment]
    assert new_tree is not None
    assert len(new_tree.tree.nodes) == original_node_count


# ---------------------------------------------------------------------------
# Phase 2: chain stitching tests
# ---------------------------------------------------------------------------


def test_chain_three_items_uses_rshift():
    """A chain of 3+ items collapses to >> syntax."""
    with TreeBuilder("Chain3") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> tree.outputs.geometry()
    code = to_python(tree)
    assert "g.SetPosition() >> g.TransformGeometry()" in code
    # No standalone assignment for the interior nodes
    assert "set_position = g.SetPosition(" not in code


def test_chain_below_threshold_stays_flat():
    """A chain below min_chain_length stays as flat Phase 1 code."""
    with TreeBuilder("Chain2") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> tree.outputs.geometry()
    # Raise threshold so the 3-item chain doesn't qualify
    code = to_python(tree, min_chain_length=4)
    assert "set_position = g.SetPosition(" in code


def test_chain_with_extra_kwargs():
    """Chain node with non-chain inputs still emits those as constructor kwargs."""
    with TreeBuilder("ChainExtra") as tree:
        geo_in = tree.inputs.geometry()
        pos = g.Position()
        geo_in >> g.SetPosition(offset=pos) >> g.TransformGeometry() >> tree.outputs.geometry()
    code = to_python(tree)
    assert "offset=" in code
    assert ">>" in code
    # The chain input kwarg (geometry=) is omitted — carried by >>
    assert "geometry=geometry" not in code


def test_chain_fanout_breaks_chain():
    """Fan-out on the chain port prevents that node from being chain-interior."""
    with TreeBuilder("FanOutBreak") as tree:
        geo_in = tree.inputs.geometry()
        set_pos = g.SetPosition(geo_in)
        g.TransformGeometry(set_pos) >> tree.outputs.geometry("Out1")
        g.TransformGeometry(set_pos) >> tree.outputs.geometry("Out2")
    code = to_python(tree)
    # set_pos fans out to two TransformGeometry nodes → must get a variable
    assert "set_position = g.SetPosition(" in code


def test_chain_output_is_valid_python():
    """Chain-stitched code is syntactically valid Python."""
    import ast

    with TreeBuilder("ChainValid") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> tree.outputs.geometry()
    code = to_python(tree)
    ast.parse(code)


# ---------------------------------------------------------------------------
# Phase 3: operator lifting tests
# ---------------------------------------------------------------------------


def test_math_add_lifts_to_operator():
    """Math ADD with a linked input is emitted as + instead of g.Math()."""
    with TreeBuilder("MathAdd") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val + 2.0) >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "+ 2.0" in code
    assert "g.Math(" not in code


def test_math_multiply_lifts_to_operator():
    """Math MULTIPLY with a linked input is emitted as *."""
    with TreeBuilder("MathMul") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val * 2.0) >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "* 2.0" in code
    assert "g.Math(" not in code


def test_math_no_lift_when_unlinked():
    """Math with no linked inputs stays as a function call."""
    with TreeBuilder("MathUnlinked") as tree:
        g.Math(operation="MULTIPLY")
    code = to_python(tree)
    assert "g.Math(" in code
    assert 'operation="MULTIPLY"' in code


def test_math_non_liftable_stays_as_call():
    """Non-liftable operation (SINE) stays as g.Math()."""
    with TreeBuilder("MathSine") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, operation="SINE") >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "g.Math(" in code


def test_math_fanout_assigns_variable():
    """A Math node whose output feeds multiple consumers gets a variable."""
    with TreeBuilder("MathFanOut") as tree:
        val = tree.inputs.float("Value", 1.0)
        m = val * 2.0
        m >> tree.outputs.float("Out1")
        m >> tree.outputs.float("Out2")
    code = to_python(tree)
    assert "= value * 2.0" in code


def test_nested_math_lifts():
    """Chained Math nodes collapse to a single operator expression."""
    with TreeBuilder("NestedMath") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val * 2.0 + 1.0) >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "value * 2.0" in code
    assert "+ 1.0" in code
    assert "g.Math(" not in code


def test_operator_output_is_valid_python():
    """Lifted operator expressions produce syntactically valid Python."""
    import ast

    with TreeBuilder("OpValid") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val * 2.0 + 1.0) >> tree.outputs.float("Result")
    ast.parse(to_python(tree))


# ---------------------------------------------------------------------------
# Snapshot tests — stabilise the full string output
# ---------------------------------------------------------------------------


def test_snapshot_single_node(snapshot):
    with TreeBuilder("SnapshotSingle") as tree:
        g.Position()
    assert snapshot == to_python(tree)


def test_snapshot_simple(snapshot):
    with TreeBuilder("SnapshotSimple") as tree:
        geo_in = tree.inputs.geometry()
        g.SetPosition(geo_in) >> tree.outputs.geometry()
    assert snapshot == to_python(tree)


def test_snapshot_with_properties(snapshot):
    with TreeBuilder("SnapshotProps") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, 2.0, operation="MULTIPLY") >> tree.outputs.float("Result")
    assert snapshot == to_python(tree)


def test_snapshot_fanout(snapshot):
    """Fan-out: one noise node feeding two set-position nodes."""
    with TreeBuilder("SnapshotFanOut") as tree:
        geo_in = tree.inputs.geometry()
        noise = g.NoiseTexture()
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry("Out1")
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry("Out2")
    assert snapshot == to_python(tree)


def test_snapshot_chain_simple(snapshot):
    """Simple 4-item chain: iface_in >> N1 >> N2 >> iface_out."""
    with TreeBuilder("ChainSnap") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> tree.outputs.geometry()
    assert snapshot == to_python(tree)


def test_snapshot_chain_with_extra_kwargs(snapshot):
    """Chain where one node has a non-chain input wired from outside."""
    with TreeBuilder("ChainKwargs") as tree:
        geo_in = tree.inputs.geometry()
        pos = g.Position()
        geo_in >> g.SetPosition(offset=pos) >> g.TransformGeometry() >> tree.outputs.geometry()
    assert snapshot == to_python(tree)


def test_snapshot_math_single(snapshot):
    """Single Math MULTIPLY with one linked input lifts to operator."""
    with TreeBuilder("MathSingle") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, 2.0, operation="MULTIPLY") >> tree.outputs.float("Result")
    assert snapshot == to_python(tree)


def test_snapshot_math_chain(snapshot):
    """Nested Math: val * 2 + 1 collapses to a single expression."""
    with TreeBuilder("MathChain") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val * 2.0 + 1.0) >> tree.outputs.float("Result")
    assert snapshot == to_python(tree)


def test_snapshot_math_offset(snapshot):
    """Math expression fed into a geometry node kwarg."""
    with TreeBuilder("MathOffset") as tree:
        geo_in = tree.inputs.geometry()
        val = tree.inputs.float("Scale", 1.0)
        geo_in >> g.SetPosition(offset=val * 2.0) >> tree.outputs.geometry()
    assert snapshot == to_python(tree)
