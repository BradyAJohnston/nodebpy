# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for nodebpy.export.codegen.to_python() — node tree → Python code generation."""

import re
from pathlib import Path

import pytest

from nodebpy import TreeBuilder
from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.export.codegen import CodegenError, to_python

from .test_usecases import ROUNDTRIP_BUILDERS


def _structure(node_tree):
    """A comparable structural signature: nodes (with key props) and links."""
    from nodebpy.export.codegen import _effective_links

    # NodeGroupInput/Output are excluded like reroutes/frames: a tree may hold
    # several Group Input nodes (editor convenience to shorten wires) that are
    # all functionally one interface. nodebpy authors a single logical
    # interface, so codegen collapses them to one node. Links still reference
    # group sockets by name, so a genuinely missing interface socket is caught.
    nodes = sorted(
        (
            n.bl_idname,
            str(getattr(n, "operation", "")),
            str(getattr(n, "data_type", "")),
            str(getattr(n, "domain", "")),
            str(getattr(n, "mode", "")),
        )
        for n in node_tree.nodes
        if n.bl_idname
        not in ("NodeReroute", "NodeFrame", "NodeGroupInput", "NodeGroupOutput")
    )

    def _socket_key(node, socket):
        # Interface socket identifiers (Socket_N) depend on declaration order;
        # compare group in/out sockets by name instead.
        if node.bl_idname in ("NodeGroupInput", "NodeGroupOutput"):
            return socket.name
        # Variable-items sockets carry a creation-order counter in their
        # identifier (Generation_1, Item_0, Field_2, …). The counter need not
        # round-trip — a hand-built node whose collection was cleared and
        # rebuilt keeps a higher counter than a fresh one, and the *first* item
        # often has no counter at all (CaptureAttribute "Attribute" vs
        # "Attribute_001"). What matters is that a corresponding socket exists,
        # so always key on the role prefix + name. (Multi-input regular sockets
        # like Math "Value"/"Value_001" still disambiguate via the link's
        # source side in the multiset, and codegen never reorders them.)
        prefix = re.sub(r"_\d+$", "", socket.identifier)
        return prefix + ":" + socket.name

    links = sorted(
        (
            link.from_node.bl_idname,
            _socket_key(link.from_node, link.from_socket),
            link.to_node.bl_idname,
            _socket_key(link.to_node, link.to_socket),
        )
        for link in _effective_links(node_tree)
    )
    return nodes, links


def _assert_roundtrip(tree):
    """Exec the generated code and assert the rebuilt tree is structurally equal."""
    # format=False keeps this testing the generator's own output (and avoids a
    # ruff subprocess per round-trip); ruff formatting is covered separately.
    code = to_python(tree, format=False)
    ns: dict = {}
    # exec(code, ns)  # noqa: S102
    try:
        exec(code, ns)  # noqa: S102
    except Exception as e:
        print("Generated code:\n", code)
        pytest.fail(f"Failed to execute generated code: {e}")
    rebuilt: TreeBuilder = ns["tree"]
    assert _structure(rebuilt.tree) == _structure(tree.tree), code
    return code


# ---------------------------------------------------------------------------
# Assertion tests (TDD baseline — each verifies one specific behaviour)
# ---------------------------------------------------------------------------


def test_with_probe_tree_returns_default_on_failure():
    """A probe whose body raises (here: an invalid tree idname) yields the
    supplied default instead of propagating, and a successful probe returns its
    result."""
    from nodebpy.export.codegen import _with_probe_tree

    sentinel = object()
    assert (
        _with_probe_tree("NotARealTreeType", lambda tree: "unused", sentinel)
        is sentinel
    )
    assert (
        _with_probe_tree("GeometryNodeTree", lambda tree: tree.bl_idname, None)
        == "GeometryNodeTree"
    )


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
    """A non-default property with no factory equivalent is emitted as a kwarg."""
    with TreeBuilder("WithProp") as tree:
        g.Math(operation="MULTIPLY", use_clamp=True)
    code = to_python(tree)
    # use_clamp has no factory shortcut, so the plain constructor is used
    # and both non-default properties appear explicitly.
    assert 'operation="MULTIPLY"' in code
    assert "use_clamp=True" in code


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


def test_node_positions_property_get_and_set():
    """TreeBuilder.node_positions reads every node's location and, on assign,
    applies a mapping by name (skipping names not in the tree)."""
    with TreeBuilder("Positions", arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry")
        g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")
    snapshot = tree.node_positions  # getter
    assert isinstance(snapshot, dict)
    assert "Set Position" in snapshot

    tree.node_positions = {"Set Position": (123.0, 45.0), "Does Not Exist": (9, 9)}
    assert tuple(tree.tree.nodes["Set Position"].location) == (123.0, 45.0)


def test_snapshot_positions_round_trip():
    """``snapshot_positions=True`` disables auto-layout and restores each
    node's authored location by name on rebuild."""
    with TreeBuilder("Snapshot", arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry")
        out = tree.outputs.geometry("Geometry")
        pos = g.Position()
        noise = g.NoiseTexture(scale=3.0)
        g.SetPosition(geometry=geo, offset=pos.o.position + noise.o.color) >> out
    want = {}
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 137.0, i * 53.0)
        want[node.name] = (i * 137.0, i * 53.0)

    code = to_python(tree, snapshot_positions=True)
    assert "arrange=None" in code  # auto-layout disabled
    assert "tree.node_positions = {" in code

    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt: TreeBuilder = ns["tree"]
    for node in rebuilt.tree.nodes:
        got = tuple(round(v, 1) for v in node.location)
        assert got == want[node.name], (node.name, got, want[node.name])


def test_default_does_not_snapshot_positions():
    """Without the flag, no positions block and no arrange override appear."""
    with TreeBuilder("NoSnapshot") as tree:
        g.Position()
    code = to_python(tree, format=False)
    assert "arrange=None" not in code
    assert "_node_positions" not in code


def test_format_with_ruff_tidies_output():
    """format=True (the default) runs the output through ruff when installed,
    tidying long lines the generator left unwrapped; format=False returns the
    raw generator output. The formatted result is still valid, runnable code."""
    import ast

    pytest.importorskip("ruff")
    with TreeBuilder("Formatted") as tree:
        geo = tree.inputs.geometry("Geometry")
        amp = tree.inputs.float("Amplitude", 0.5)
        out = tree.outputs.geometry("Geometry")
        height = g.Math.sine(g.Position().o.position.x) * amp
        (
            geo
            >> g.SetPosition(offset=g.CombineXYZ(z=height))
            >> g.SetShadeSmooth()
            >> g.TransformGeometry()
            >> out
        )

    raw = tree.to_python(format=False)
    formatted = tree.to_python(format=True)
    assert tree.to_python() == formatted  # format=True is the default

    assert formatted != raw  # ruff reformatted something
    # the generator left at least one over-long line; ruff wrapped it.
    assert max(len(line) for line in raw.splitlines()) > 88
    assert max(len(line) for line in formatted.splitlines()) < max(
        len(line) for line in raw.splitlines()
    )

    ast.parse(formatted)  # still valid Python
    ns: dict = {}
    exec(formatted, ns)  # noqa: S102 — still runnable
    assert ns["tree"] is not None


def test_nodebpy_pkg_rewrites_import_anchor():
    """nodebpy_pkg rewrites every nodebpy import anchor so vendored copies are
    reachable with a relative path; the same anchor is used for both the
    top-level and ``.builder`` imports."""
    with TreeBuilder("Vendored") as tree:
        geo = tree.inputs.geometry("Geometry")
        g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")

    code = to_python(tree, top_level="class", nodebpy_pkg="..vendor.nodebpy")
    assert "from ..vendor.nodebpy import" in code
    assert "from ..vendor.nodebpy.builder import" in code
    assert "from nodebpy" not in code


def test_top_level_class_emits_class_not_with_block():
    """top_level='class' renders the working tree as a Custom*Group subclass
    (no ``with`` block / TreeBuilder import); the default stays the ``with``
    form."""
    with TreeBuilder("ArchiveMe") as tree:
        geo = tree.inputs.geometry("Geometry")
        g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")

    assert "with TreeBuilder(" in to_python(tree)  # default unchanged

    code = to_python(tree, top_level="class")
    assert "class ArchiveMe(CustomGeometryGroup):" in code
    assert "def _build_group(self, tree):" in code
    assert "with TreeBuilder(" not in code
    assert "TreeBuilder" not in code  # not imported when unused


def test_top_level_class_round_trips_via_create_group():
    """The emitted top-level class rebuilds the tree (and any nested group)
    through create_group()."""
    import bpy

    from nodebpy.builder import CustomGeometryGroup
    from nodebpy.export.codegen import _class_name

    class _ArchiveInner(CustomGeometryGroup):
        _name = "ArchiveInner"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")

    with TreeBuilder("ArchiveOuter") as tree:
        geo = tree.inputs.geometry("Geometry")
        _ArchiveInner(**{"Geometry": geo}) >> tree.outputs.geometry("Geometry")
    orig_top = _structure(tree.tree)
    orig_inner = _structure(
        next(n.node_tree for n in tree.tree.nodes if n.bl_idname == "GeometryNodeGroup")
    )

    code = to_python(tree, top_level="class")
    for t in list(bpy.data.node_groups):  # force fresh builds
        t.name = "_orig_" + t.name
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt = ns[_class_name("ArchiveOuter")].create_group()

    assert _structure(rebuilt) == orig_top, code
    rebuilt_inner = next(
        n.node_tree for n in rebuilt.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    assert _structure(rebuilt_inner) == orig_inner, code


def test_snapshot_top_level_class(snapshot):
    """The class-per-group archive form for a tree with a nested group."""
    from nodebpy.builder import CustomGeometryGroup

    class _SnapClassInner(CustomGeometryGroup):
        _name = "SnapClassInner"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")

    with TreeBuilder("SnapClassOuter") as tree:
        geo = tree.inputs.geometry("Geometry")
        _SnapClassInner(**{"Geometry": geo}) >> tree.outputs.geometry("Geometry")
    assert snapshot == to_python(tree, top_level="class", format=False)


def _tree_with_reroute(name):
    """A tree whose Set Position output reaches the group output through a
    reroute node."""
    with TreeBuilder(name, arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry")
        out = tree.outputs.geometry("Geometry")
        sp = g.SetPosition(geometry=geo, offset=g.Position())
        reroute = tree.tree.nodes.new("NodeReroute")
        tree.tree.links.new(sp.node.outputs[0], reroute.inputs[0])
        tree.tree.links.new(reroute.outputs[0], out.socket)
    return tree


def test_keep_reroutes_emits_reroute_call():
    """keep_reroutes emits ``g.Reroute(...)`` (with auto-layout disabled, which
    would otherwise dissolve the reroute); the default collapses it instead."""
    tree = _tree_with_reroute("RerouteKeep")
    assert any(n.bl_idname == "NodeReroute" for n in tree.tree.nodes)

    assert "g.Reroute" not in to_python(tree)  # collapsed by default

    code = to_python(tree, keep_reroutes=True)
    assert "g.Reroute(" in code
    assert "arrange=None" in code  # layout off, so the reroute survives a rebuild


def test_keep_reroutes_with_snapshot_positions():
    """keep_reroutes + snapshot_positions emits the reroute node and includes
    its own location in the positions block.

    (Asserts on the generated source rather than exec-rebuilding: linking a
    fresh ``g.Reroute`` mutates the node's adaptive sockets, which intermittently
    segfaults the in-process Blender under full-suite memory pressure. The
    exact rebuilt output is locked by ``test_snapshot_keep_reroutes_block``.)"""
    tree = _tree_with_reroute("ReroutePos")
    reroute = next(n for n in tree.tree.nodes if n.bl_idname == "NodeReroute")
    reroute.location = (360.0, 120.0)

    code = to_python(tree, keep_reroutes=True, snapshot_positions=True)
    assert "g.Reroute(" in code
    assert "arrange=None" in code
    assert "tree.node_positions = {" in code
    assert f'"{reroute.name}": (360.0, 120.0)' in code  # reroute position kept


def test_snapshot_positions_nested_group_round_trip():
    """snapshot_positions restores locations inside nested group classes too:
    the generated ``_build_group`` disables its own auto-layout and applies a
    positions block, so both the outer tree and the group round-trip."""
    import bpy

    from nodebpy.builder import CustomGeometryGroup

    class _PosInner(CustomGeometryGroup):
        _name = "PosInner"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            out = tree.outputs.geometry("Geometry")
            g.SetPosition(geometry=geo, offset=g.Position()) >> out

    with TreeBuilder("PosOuter", arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry")
        out = tree.outputs.geometry("Geometry")
        _PosInner(**{"Geometry": geo}) >> out

    want_outer, want_inner = {}, {}
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 111.0, i * 40.0)
        want_outer[node.name] = (i * 111.0, i * 40.0)
    for i, node in enumerate(bpy.data.node_groups["PosInner"].nodes):
        node.location = (i * 222.0, i * 70.0)
        want_inner[node.name] = (i * 222.0, i * 70.0)

    code = to_python(tree, snapshot_positions=True)
    assert "tree.disable_arrange()" in code  # group's own layout disabled

    _force_fresh_group_build()
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt: TreeBuilder = ns["tree"]
    for node in rebuilt.tree.nodes:
        got = tuple(round(v, 1) for v in node.location)
        assert got == want_outer[node.name], (node.name, got)
    rebuilt_inner = next(
        n.node_tree for n in rebuilt.tree.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    for node in rebuilt_inner.nodes:
        got = tuple(round(v, 1) for v in node.location)
        assert got == want_inner[node.name], (node.name, got)


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
        (
            geo_in
            >> g.SetPosition(offset=pos)
            >> g.TransformGeometry()
            >> tree.outputs.geometry()
        )
    code = to_python(tree)
    assert "offset=" in code
    assert ">>" in code
    # The chain input kwarg (geometry=) is omitted — carried by >>
    assert "geometry=geometry" not in code


def test_long_chain_wraps_one_segment_per_line():
    """A chain past 88 columns wraps in parens with one >> segment per line."""
    with TreeBuilder("LongChain") as tree:
        geo_in = tree.inputs.geometry("Geometry")
        (
            geo_in
            >> g.DistributePointsOnFaces()
            >> g.InstanceOnPoints(instance=g.IcoSphere())
            >> g.RealizeInstances()
            >> tree.outputs.geometry("Geometry")
        )
    code = _assert_roundtrip(tree)
    assert "    (\n        geometry\n" in code
    assert "\n        >> g.RealizeInstances()\n" in code
    assert "\n    )" in code
    assert all(len(line) <= 88 for line in code.splitlines()), code


def test_short_chain_stays_one_line():
    """A chain that fits in 88 columns is not wrapped."""
    with TreeBuilder("ShortChain") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> tree.outputs.geometry()
    code = to_python(tree)
    assert ">> g.SetPosition() >> g.TransformGeometry() >>" in code


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
    """Math with no linked inputs stays a call — via the factory shortcut."""
    with TreeBuilder("MathUnlinked") as tree:
        g.Math(operation="MULTIPLY")
    code = to_python(tree)
    assert "g.Math.multiply()" in code


def test_math_non_liftable_stays_as_call():
    """Non-liftable operation (INVERSE_SQUARE_ROOT) stays a call — via the factory shortcut."""
    with TreeBuilder("MathInverseSquareRoot") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math.inverse_square_root(val) >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "g.Math.inverse_square_root(value)" in code


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
# Inlining and round-trip fidelity
# ---------------------------------------------------------------------------


def test_single_use_node_inlines_as_kwarg():
    """A node consumed exactly once is embedded in its consumer's call."""
    with TreeBuilder("KwargInline") as tree:
        geo_in = tree.inputs.geometry()
        noise = g.NoiseTexture(scale=3.0)
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry()
    code = to_python(tree)
    assert "offset=g.NoiseTexture(scale=3.0)" in code
    assert "noise_texture =" not in code


def test_regression_chain_tail_into_kwarg_keeps_link():
    """A lifted chain whose tail feeds a non-first input must not drop the link.

    Regression: the divide expression below was emitted as an orphaned
    statement and CombineXYZ lost its z= input entirely.
    """
    with TreeBuilder("HelloWorld") as tree:
        height = tree.inputs.float("Height", 3.0)
        omega = tree.inputs.float("Omega", 2.0)
        pos = g.Position().o.position
        distance = g.Math.square_root(pos.x**2 + pos.y**2)
        z = height * g.Math.sine(distance * omega) / distance
        (
            g.Grid(20, 20, 200, 200)
            >> g.SetPosition(offset=g.CombineXYZ(z=z))
            >> g.SetShadeSmooth.face()
            >> tree.outputs.geometry("Mesh")
        )
    code = _assert_roundtrip(tree)
    assert "g.CombineXYZ(z=" in code


def test_roundtrip_structural_chain():
    with TreeBuilder("RoundTripChain") as tree:
        geo_in = tree.inputs.geometry()
        pos = g.Position()
        (
            geo_in
            >> g.SetPosition(offset=pos)
            >> g.TransformGeometry()
            >> tree.outputs.geometry()
        )
    _assert_roundtrip(tree)


def test_multi_input_socket_becomes_tuple():
    """Several links into one multi-input socket emit a tuple kwarg.

    Regression: JoinGeometry's second branch was silently dropped because the
    chain logic skipped every link sharing the multi-input identifier.
    """
    with TreeBuilder("MultiInput") as tree:
        a = g.Cube()
        b = g.UVSphere()
        g.JoinGeometry((a, b)) >> tree.outputs.geometry()
    code = _assert_roundtrip(tree)
    assert "g.JoinGeometry(geometry=(g.Cube(), g.UVSphere()))" in code


def test_geometry_to_instance_emits_positional_args():
    """GeometryToInstance takes its multi-input geometry as *args, so links
    render as positional arguments — a geometry= kwarg would be rejected by
    the varargs constructor."""
    with TreeBuilder("GTI") as tree:
        (
            g.GeometryToInstance(g.Cube(), g.UVSphere(), g.Cone())
            >> tree.outputs.geometry()
        )
    code = _assert_roundtrip(tree)
    assert "g.GeometryToInstance(g.Cube(), g.UVSphere(), g.Cone())" in code
    assert "geometry=" not in code


def test_roundtrip_structural_city_builder():
    with TreeBuilder("Voxelise") as tree:
        geo = tree.inputs.geometry("Geometry")
        seed = tree.inputs.integer("Seed")
        road_width = tree.inputs.float("Road Width", 0.25)
        density = tree.inputs.float("Density", 10.0)

        curve_mesh = geo >> g.CurveToMesh(
            profile_curve=g.CurveLine(
                start=g.CombineXYZ(x=road_width * -0.5),
                end=g.CombineXYZ(x=road_width * 0.5),
            ),
        )
        building_points = g.Grid(5.0, 5.0) >> g.DistributePointsOnFaces(
            density=density, seed=seed
        )
        road_points = geo >> g.CurveToPoints(mode="EVALUATED")
        building_points = g.DeleteGeometry.point(
            building_points,
            selection=g.GeometryProximity(
                road_points, target_element="POINTS"
            ).o.distance
            < road_width,
        )
        buildings = building_points >> g.InstanceOnPoints(
            instance=g.Cube() >> g.TransformGeometry(translation=(0, 0, 0.5)),
        )
        g.JoinGeometry((curve_mesh, buildings)) >> tree.outputs.geometry("Result")
    _assert_roundtrip(tree)


def test_roundtrip_structural_boolean_decoder():
    from functools import reduce
    from itertools import product
    from operator import and_

    with TreeBuilder("Decoder") as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(2)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]
        for i, combo in enumerate(product((False, True), repeat=2)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")
    _assert_roundtrip(tree)


# ---------------------------------------------------------------------------
# Operator lifting: boolean, integer, abs(), modulo
# ---------------------------------------------------------------------------


def test_boolean_math_lifts_to_operators():
    with TreeBuilder("BoolOps") as tree:
        a = tree.inputs.boolean("A")
        b = tree.inputs.boolean("B")
        ((a & b) | ~a) >> tree.outputs.boolean("Out")
    code = _assert_roundtrip(tree)
    assert "a & b | ~a" in code
    assert "BooleanMath" not in code


def test_integer_math_lifts_to_operators():
    with TreeBuilder("IntOps") as tree:
        i = tree.inputs.integer("I")
        (i // 2 + abs(i)) >> tree.outputs.integer("Out")
    code = _assert_roundtrip(tree)
    assert "i // 2 + abs(i)" in code
    assert "IntegerMath" not in code


def test_compare_emits_factory_path():
    """A Compare whose state no operator produces (custom epsilon) falls
    back to the nested factory spelling and round-trips its props."""
    with TreeBuilder("CompareProps") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Compare.float.equal(val, 0.5, epsilon=0.5) >> tree.outputs.boolean("Out")
    code = _assert_roundtrip(tree)
    assert "g.Compare.float.equal(value, 0.5" in code
    assert "==" not in code


def test_vector_compare_emits_mode():
    """Non-ELEMENT VECTOR Compare requires mode= (popped from **kwargs)."""
    with TreeBuilder("VecCompare") as tree:
        vec = tree.inputs.vector("V")
        g.Compare(
            a=vec,
            b=(0.5, 0.5, 0.5),
            operation="LESS_THAN",
            data_type="VECTOR",
            mode="AVERAGE",
        ) >> tree.outputs.boolean("Out")
    code = _assert_roundtrip(tree)
    assert 'data_type="VECTOR"' in code
    assert 'mode="AVERAGE"' in code


def test_compare_lifts_to_operators():
    """ELEMENT-mode comparisons matching the operator overloads lift."""
    with TreeBuilder("CompareLift") as tree:
        val = tree.inputs.float("Value", 1.0)
        vec = tree.inputs.vector("V")
        (val < 0.5) >> tree.outputs.boolean("Less")
        (vec >= (0.5, 0.5, 0.5)) >> tree.outputs.boolean("GreaterEq")
        (val == 0.25) >> tree.outputs.boolean("Equal")
    code = _assert_roundtrip(tree)
    assert "val < 0.5" in code or "value < 0.5" in code
    assert ">= (0.5, 0.5, 0.5)" in code
    assert "== 0.25" in code


def test_compare_lift_parenthesises_nested_comparisons():
    """Comparisons feeding boolean operators and other comparisons get
    parens — Python would otherwise chain ``a < b < c``."""
    with TreeBuilder("CompareNest") as tree:
        val = tree.inputs.float("Value", 1.0)
        ((val < 0.5) & (val > 0.1)) >> tree.outputs.boolean("Band")
    code = _assert_roundtrip(tree)
    assert "(value < 0.5) & (value > 0.1)" in code


def test_float_modulo_round_trips_to_floored_modulo():
    """Python % on floats creates FLOORED_MODULO; lifting must mirror that."""
    with TreeBuilder("Modulo") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val % 3.0) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value % 3.0" in code


# ---------------------------------------------------------------------------
# Socket-method reverse-mapping
# ---------------------------------------------------------------------------


def test_switch_emits_socket_method():
    with TreeBuilder("SwitchMethod") as tree:
        include = tree.inputs.boolean("Include")
        vol = tree.inputs.geometry("Volume")
        include.switch.geometry(None, vol) >> tree.outputs.geometry("Out")
    code = _assert_roundtrip(tree)
    assert "include.switch.geometry(true=volume)" in code
    assert "g.Switch" not in code


def test_switch_unlinked_condition_falls_back():
    """Switch with no linked condition can't be a method — constructor/factory.

    FLOAT is the default input_type, so the plain constructor suffices; a
    non-default type (geometry) uses the factory spelling.
    """
    with TreeBuilder("SwitchFactory") as tree:
        a = tree.inputs.float("A", 1.0)
        b = tree.inputs.float("B", 2.0)
        g.Switch.float(None, a, b) >> tree.outputs.float("Out")
        geo = tree.inputs.geometry("Geo")
        g.Switch.geometry(None, None, geo) >> tree.outputs.geometry("GeoOut")
    code = _assert_roundtrip(tree)
    assert "g.Switch(false=a, true=b)" in code
    assert "g.Switch.geometry(true=geo)" in code


def test_map_range_emits_socket_method():
    with TreeBuilder("MapRangeMethod") as tree:
        val = tree.inputs.float("Value", 0.5)
        lo = tree.inputs.float("Lo")
        hi = tree.inputs.float("Hi", 1.0)
        val.map_range(lo, hi, 0.0, 2.0) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value.map_range(lo, hi, to_max=2.0)" in code


def test_map_range_emits_non_default_props_as_kwargs():
    with TreeBuilder("MapRangeProps") as tree:
        val = tree.inputs.float("Value", 0.5)
        val.map_range(clamp=False) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value.map_range(clamp=False)" in code


def test_field_at_index_emits_domain_method():
    with TreeBuilder("FieldAt") as tree:
        val = tree.inputs.float("Value", 0.5)
        ix = tree.inputs.integer("Ix")
        val.point.at(ix) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value.point.at(ix)" in code


def test_accumulate_field_picks_output_method():
    with TreeBuilder("Accumulate") as tree:
        val = tree.inputs.float("Value", 0.5)
        gid = tree.inputs.integer("Group")
        val.point.trailing(gid) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value.point.trailing(group)" in code


def test_field_mean_on_vector():
    with TreeBuilder("Mean") as tree:
        vec = tree.inputs.vector("Vec")
        vec.point.mean() >> tree.outputs.vector("Out")
    code = _assert_roundtrip(tree)
    assert "vec.point.mean()" in code


def test_separate_xyz_dissolves_to_attrs():
    """SeparateXYZ becomes vec.x / vec.y, promoting the source to a variable."""
    with TreeBuilder("SepXYZ") as tree:
        pos = g.Position().o.position
        (pos.x**2 + pos.y**2) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "position = g.Position().o.position" in code
    assert "position.x ** 2.0 + position.y ** 2.0" in code
    assert "SeparateXYZ" not in code


def test_separate_xyz_single_output_stays_inline():
    """One used output needs no promotion — the accessor renders once."""
    with TreeBuilder("SepX") as tree:
        (g.Position().o.position.x * 2.0) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "g.Position().o.position.x * 2.0" in code
    assert "SeparateXYZ" not in code


def test_vector_math_methods():
    with TreeBuilder("VecMethods") as tree:
        a = tree.inputs.vector("A")
        b = tree.inputs.vector("B")
        a.dot(b) >> tree.outputs.float("Dot")
        a.cross(b) >> tree.outputs.vector("Cross")
        a.length() >> tree.outputs.float("Len")
        a.normalize() >> tree.outputs.vector("Norm")
        a.distance(b) >> tree.outputs.float("Dist")
    code = _assert_roundtrip(tree)
    for expected in (
        "a.dot(b)",
        "a.cross(b)",
        "a.length()",
        "a.normalize()",
        "a.distance(b)",
    ):
        assert expected in code, expected
    assert "VectorMath" not in code


def test_vector_rotate_and_transform_methods():
    with TreeBuilder("VecTransform") as tree:
        vec = tree.inputs.vector("Vec")
        rot = tree.inputs.rotation("Rot")
        mat = tree.inputs.matrix("Mat")
        vec.rotate(rot) >> tree.outputs.vector("Rotated")
        vec.transform(mat) >> tree.outputs.vector("Transformed")
    code = _assert_roundtrip(tree)
    assert "vec.rotate(rot)" in code
    assert "vec.transform(mat)" in code


def test_clamp_method():
    with TreeBuilder("ClampMethod") as tree:
        val = tree.inputs.float("Value", 0.5)
        val.clamp(0.2, 0.8) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert "value.clamp(0.2" in code


def test_string_methods():
    with TreeBuilder("StringMethods") as tree:
        path = tree.inputs.string("Path")
        prefix = tree.inputs.string("Prefix")
        path.starts_with(prefix) >> tree.outputs.boolean("Starts")
        path.slice(1, 3) >> tree.outputs.string("Sliced")
        path.length() >> tree.outputs.integer("Len")
        path.uppercase() >> tree.outputs.string("Upper")
        path.replace("a", "b") >> tree.outputs.string("Replaced")
    code = _assert_roundtrip(tree)
    for expected in (
        "path.starts_with(prefix)",
        "path.slice(1, 3)",
        "path.length()",
        "path.uppercase()",
        'path.replace("a", "b")',
    ):
        assert expected in code, expected


def test_matrix_methods():
    with TreeBuilder("MatrixMethods") as tree:
        mat = tree.inputs.matrix("Mat")
        vec = tree.inputs.vector("Vec")
        mat.invert() >> tree.outputs.matrix("Inverted")
        mat.transpose() >> tree.outputs.matrix("Transposed")
        mat.determinant() >> tree.outputs.float("Det")
        mat.transform_direction(vec) >> tree.outputs.vector("Dir")
    code = _assert_roundtrip(tree)
    for expected in (
        "mat.invert()",
        "mat.transpose()",
        "mat.determinant()",
        "mat.transform_direction(vec)",
    ):
        assert expected in code, expected


def test_rotation_methods():
    with TreeBuilder("RotationMethods") as tree:
        rot = tree.inputs.rotation("Rot")
        rot.invert() >> tree.outputs.rotation("Inverted")
        rot.to_euler() >> tree.outputs.vector("Euler")
    code = _assert_roundtrip(tree)
    assert "rot.invert()" in code
    assert "rot.to_euler()" in code


def test_separate_transform_dissolves():
    with TreeBuilder("SepTransform") as tree:
        mat = tree.inputs.matrix("Mat")
        mat.translation >> tree.outputs.vector("T")
        mat.scale >> tree.outputs.vector("S")
    code = _assert_roundtrip(tree)
    assert "mat.translation" in code
    assert "mat.scale" in code
    assert "SeparateTransform" not in code


def test_separate_color_dissolves():
    with TreeBuilder("SepColor") as tree:
        col = tree.inputs.color("Col")
        (col.r + col.g) >> tree.outputs.float("Sum")
    code = _assert_roundtrip(tree)
    assert "col.r + col.g" in code
    assert "SeparateColor" not in code


# ---------------------------------------------------------------------------
# Factory reverse-mapping
# ---------------------------------------------------------------------------


def test_factory_nested_instance_path():
    """Parameterised factory instances reverse-map (domain via self._domain)."""
    with TreeBuilder("StoreAttr") as tree:
        geo_in = tree.inputs.geometry()
        (
            g.StoreNamedAttribute.point.integer(geo_in, name="id", value=7)
            >> tree.outputs.geometry()
        )
    code = _assert_roundtrip(tree)
    assert "g.StoreNamedAttribute.point.integer(" in code
    assert 'data_type="INT"' not in code


def test_factory_fallback_when_props_not_covered():
    """A non-default prop outside the factory signature forces the constructor."""
    with TreeBuilder("MathClamp") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, operation="SINE", use_clamp=True) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    assert 'g.Math(value=value, operation="SINE", use_clamp=True)' in code


def test_factory_keeps_default_prop_constructor():
    """No non-default state to cover → plain constructor, no factory."""
    with TreeBuilder("PlainMath") as tree:
        g.Math()  # ADD is the default operation
    code = to_python(tree)
    assert "math = g.Math()" in code


# ---------------------------------------------------------------------------
# Unsupported nodes and custom emitters
# ---------------------------------------------------------------------------


def test_unsupported_node_raises_by_default(monkeypatch):
    from nodebpy.export.codegen import _get_node_registry

    with TreeBuilder("Unsupported") as tree:
        g.SetPosition()
    monkeypatch.delitem(_get_node_registry(), "GeometryNodeSetPosition")
    with pytest.raises(CodegenError, match="GeometryNodeSetPosition"):
        to_python(tree)


def test_unsupported_node_placeholder_when_not_strict(monkeypatch):
    from nodebpy.export.codegen import _get_node_registry

    with TreeBuilder("UnsupportedLoose") as tree:
        g.SetPosition()
    monkeypatch.delitem(_get_node_registry(), "GeometryNodeSetPosition")
    code = to_python(tree, strict=False)
    assert "TODO: unsupported node" in code


def test_register_emitter_overrides_default():
    from nodebpy.export.codegen import _EMITTERS, BinOp, Call, register_emitter

    @register_emitter("GeometryNodeSetShadeSmooth")
    def _emit_shade_smooth(node, ctx):
        if node.domain != "FACE":
            return None
        ctx.used_aliases.add("g")
        call = Call("g.SetShadeSmooth.face")
        link = ctx.input_link(node, node.inputs[0].identifier)
        if link is not None:
            return BinOp(">>", ctx.upstream_expr(link), call)
        return call

    try:
        with TreeBuilder("Emitter") as tree:
            g.Cube() >> g.SetShadeSmooth.face() >> tree.outputs.geometry()
        code = to_python(tree)
        assert "g.SetShadeSmooth.face()" in code
        assert 'domain="FACE"' not in code
    finally:
        _EMITTERS.pop("GeometryNodeSetShadeSmooth", None)


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


def test_imports_only_used_aliases():
    with TreeBuilder("GeoOnly") as tree:
        g.Position()
    code = to_python(tree)
    assert code.splitlines()[0] == "from nodebpy import geometry as g, TreeBuilder"


def test_imports_no_alias_for_empty_tree():
    with TreeBuilder("Empty") as tree:
        tree.inputs.float("Value", 1.0)
    code = to_python(tree)
    assert code.splitlines()[0] == "from nodebpy import TreeBuilder"


# ---------------------------------------------------------------------------
# Snapshot tests — stabilise the full string output
# ---------------------------------------------------------------------------


def test_snapshot_single_node(snapshot):
    with TreeBuilder("SnapshotSingle") as tree:
        g.Position()
    assert snapshot == to_python(tree, format=False)


def test_snapshot_simple(snapshot):
    with TreeBuilder("SnapshotSimple") as tree:
        geo_in = tree.inputs.geometry()
        g.SetPosition(geo_in) >> tree.outputs.geometry()
    assert snapshot == to_python(tree, format=False)


def test_snapshot_with_properties(snapshot):
    with TreeBuilder("SnapshotProps") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, 2.0, operation="MULTIPLY") >> tree.outputs.float("Result")
    assert snapshot == to_python(tree, format=False)


def test_snapshot_fanout(snapshot):
    """Fan-out: one noise node feeding two set-position nodes."""
    with TreeBuilder("SnapshotFanOut") as tree:
        geo_in = tree.inputs.geometry()
        noise = g.NoiseTexture()
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry("Out1")
        g.SetPosition(geo_in, offset=noise) >> tree.outputs.geometry("Out2")
    assert snapshot == to_python(tree, format=False)


def test_snapshot_positions_block(snapshot):
    """snapshot_positions=True: arrange=None + a trailing positions block.
    Locations are assigned deterministically so the snapshot is stable."""
    with TreeBuilder("SnapPositions", arrange=None) as tree:
        geo_in = tree.inputs.geometry("Geometry")
        g.SetPosition(geo_in, offset=g.Position()) >> tree.outputs.geometry("Geometry")
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 100.0, i * 40.0)
    assert snapshot == to_python(tree, snapshot_positions=True, format=False)


def test_snapshot_positions_nested_group_block(snapshot):
    """snapshot_positions=True with a nested group: the group's _build_group
    disables auto-layout and restores its own node positions."""
    import bpy

    from nodebpy.builder import CustomGeometryGroup

    class _SnapInner(CustomGeometryGroup):
        _name = "SnapInner"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            g.SetPosition(geometry=geo) >> tree.outputs.geometry("Geometry")

    with TreeBuilder("SnapNested", arrange=None) as tree:
        geo_in = tree.inputs.geometry("Geometry")
        _SnapInner(**{"Geometry": geo_in}) >> tree.outputs.geometry("Geometry")
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 120.0, i * 50.0)
    for i, node in enumerate(bpy.data.node_groups["SnapInner"].nodes):
        node.location = (i * 200.0, i * 60.0)
    assert snapshot == to_python(tree, snapshot_positions=True, format=False)


def test_snapshot_keep_reroutes_block(snapshot):
    """keep_reroutes emits the reroute as ``g.Reroute(input=...)`` instead of
    collapsing it; shown alongside snapshot_positions."""
    with TreeBuilder("KeepReroute", arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry")
        out = tree.outputs.geometry("Geometry")
        sp = g.SetPosition(geometry=geo, offset=g.Position())
        reroute = tree.tree.nodes.new("NodeReroute")
        tree.tree.links.new(sp.node.outputs[0], reroute.inputs[0])
        tree.tree.links.new(reroute.outputs[0], out.socket)
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 90.0, i * 30.0)
    assert snapshot == to_python(
        tree, keep_reroutes=True, snapshot_positions=True, format=False
    )


def test_snapshot_chain_simple(snapshot):
    """Simple 4-item chain: iface_in >> N1 >> N2 >> iface_out."""
    with TreeBuilder("ChainSnap") as tree:
        geo_in = tree.inputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> tree.outputs.geometry()
    assert snapshot == to_python(tree, format=False)


def test_snapshot_chain_with_extra_kwargs(snapshot):
    """Chain where one node has a non-chain input wired from outside."""
    with TreeBuilder("ChainKwargs") as tree:
        geo_in = tree.inputs.geometry()
        pos = g.Position()
        (
            geo_in
            >> g.SetPosition(offset=pos)
            >> g.TransformGeometry()
            >> tree.outputs.geometry()
        )
    assert snapshot == to_python(tree, format=False)


def test_snapshot_math_single(snapshot):
    """Single Math MULTIPLY with one linked input lifts to operator."""
    with TreeBuilder("MathSingle") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, 2.0, operation="MULTIPLY") >> tree.outputs.float("Result")
    assert snapshot == to_python(tree, format=False)


def test_snapshot_math_chain(snapshot):
    """Nested Math: val * 2 + 1 collapses to a single expression."""
    with TreeBuilder("MathChain") as tree:
        val = tree.inputs.float("Value", 1.0)
        (val * 2.0 + 1.0) >> tree.outputs.float("Result")
    assert snapshot == to_python(tree, format=False)


def test_snapshot_math_offset(snapshot):
    """Math expression fed into a geometry node kwarg."""
    with TreeBuilder("MathOffset") as tree:
        geo_in = tree.inputs.geometry()
        val = tree.inputs.float("Scale", 1.0)
        geo_in >> g.SetPosition(offset=val * 2.0) >> tree.outputs.geometry()
    assert snapshot == to_python(tree, format=False)


# ---------------------------------------------------------------------------
# Zones — emitted as zone wrappers with item handles
# ---------------------------------------------------------------------------


def test_dict_expr_renders():
    from nodebpy.export.codegen import DictExpr, Lit, Ref

    expr = DictExpr({"a": Lit(1.0), "b": Ref("value")})
    assert expr.render() == '{"a": 1.0, "b": value}'


def test_repeat_zone_emits_handle_form():
    with TreeBuilder("RepeatHandles") as tree:
        out = tree.outputs.geometry("Geometry")
        zone = g.RepeatZone(10)
        value = zone.item("value", initial=1.0)
        (value.current + 1.0) >> value.next
        cube = zone.item("cube", g.Cube())
        cube.current >> g.SetPosition(offset=(0, 0, 0.1)) >> cube.next
        cube.result >> out
    code = to_python(tree)
    assert "g.RepeatZone(10)" in code
    assert 'value = repeat_zone.item("value", 1.0)' in code
    assert ">> value.next" in code
    assert "cube.result >> geometry" in code


def test_roundtrip_structural_repeat_zone():
    with TreeBuilder("RepeatRoundtrip") as tree:
        iterations = tree.inputs.integer("Iterations", 5)
        out = tree.outputs.geometry("Geometry")
        zone = g.RepeatZone(iterations)
        cube = zone.item("cube", g.Cube())
        fac = zone.item("fac", initial=0.5)
        (fac.current * 2.0) >> fac.next
        cube.current >> g.SetPosition(offset=(0, 0, 0.1)) >> cube.next
        cube.result >> g.SetShadeSmooth(shade_smooth=fac.result > 1.0) >> out
    _assert_roundtrip(tree)


def test_roundtrip_structural_simulation_zone():
    with TreeBuilder("SimRoundtrip") as tree:
        out = tree.outputs.geometry("Geometry")
        zone = g.SimulationZone({"cube": g.Cube()})
        input, output = zone
        pos = input.capture(g.Position())
        pos >> output
        g.Boolean(False) >> output.i.skip
        input >> g.SetPosition(offset=zone.delta_time * g.Vector((0, 0, 0.1))) >> output
        output >> g.SetPosition(position=output.o["Position"]) >> out
    code = _assert_roundtrip(tree)
    assert "g.SimulationZone()" in code
    assert ".delta_time" in code
    assert ">> simulation_zone.output.i.skip" in code


def test_roundtrip_structural_foreach_zone():
    with TreeBuilder("ForEachRoundtrip") as tree:
        out = tree.outputs.geometry("Geometry")
        cube = g.Cube()
        zone = g.ForEachGeometryElementZone(cube, domain="FACE")
        pos = zone.item("Pos", g.Position())
        transformed = g.Cone() >> g.TransformGeometry(translation=pos.output)
        main = zone.main_item("Out", type="VECTOR")
        pos.output >> main.input
        zone.generated_item("Gen", transformed, domain="FACE")
        transformed >> zone.output
        g.JoinGeometry([zone.generation.output, cube]) >> out
    code = _assert_roundtrip(tree)
    assert 'domain="FACE"' in code
    assert ">> for_each.generation.input" in code
    assert "for_each.generation.output" in code


def test_zone_unreferenced_item_declared_without_variable():
    with TreeBuilder("RepeatUnused") as tree:
        zone = g.RepeatZone(3)
        zone.item("spare", type="VECTOR")
    code = _assert_roundtrip(tree)
    assert 'repeat_zone.item("spare", type="VECTOR")' in code
    assert "= repeat_zone.item(" not in code


def test_unpaired_zone_input_raises():
    with TreeBuilder("Unpaired") as tree:
        tree.tree.nodes.new("GeometryNodeSimulationInput")
    with pytest.raises(CodegenError, match="paired"):
        to_python(tree)


# ---------------------------------------------------------------------------
# FormatString / JoinStrings
# ---------------------------------------------------------------------------


def test_format_string_constructor_with_items_dict():
    with TreeBuilder("Format") as tree:
        val = g.Value()
        fmt = g.FormatString("x={x} n={n}", items={"x": val, "n": "hello"})
        fmt >> tree.outputs.string("Out")
    code = _assert_roundtrip(tree)
    assert 'g.FormatString("x={x} n={n}", items={"x": g.Value(), "n": "hello"})' in code


def test_format_string_linked_format_uses_method():
    with TreeBuilder("FormatMethod") as tree:
        s = g.String("v={v}")
        s.o.string.format({"v": g.Value()}) >> tree.outputs.string("Out")
    code = _assert_roundtrip(tree)
    assert '.format({"v": g.Value()})' in code


def test_join_strings_constructor_and_method():
    with TreeBuilder("Join") as tree:
        a = g.JoinStrings([g.String("a"), g.String("b")], delimiter="-")
        d = g.String("+")
        d.o.string.join([a, g.String("c")]) >> tree.outputs.string("Out")
    code = _assert_roundtrip(tree)
    assert 'delimiter="-"' in code
    assert ".join((" in code


def test_string_with_control_characters_round_trips():
    """A string default with newlines/tabs/quotes/backslashes emits a valid,
    exec'able literal that preserves the exact value (json escaping)."""
    import ast

    tricky = 'line1\nline2\t"quoted"\\end\r'
    with TreeBuilder("TrickyStr") as tree:
        g.String(tricky) >> tree.outputs.string("Out")
    code = to_python(tree)
    ast.parse(code)  # would raise SyntaxError on an unterminated literal
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    node = next(
        n for n in ns["tree"].tree.nodes if n.bl_idname == "FunctionNodeInputString"
    )
    assert node.string == tricky


# ---------------------------------------------------------------------------
# MenuSwitch / IndexSwitch emitters
# ---------------------------------------------------------------------------


def test_menu_switch_emits_factory_dict():
    """MenuSwitch round-trips its enum item names through the items dict;
    is_selected outputs resolve as named output accessors."""
    with TreeBuilder("MenuRT") as tree:
        menu = tree.inputs.menu("Mode", "Object")
        switch = g.MenuSwitch.geometry(menu, {"Object": g.Cube(), "Mesh": g.Grid()})
        switch >> tree.outputs.geometry("Out")
        switch.is_selected("Mesh") >> tree.outputs.boolean("IsMesh")
    code = _assert_roundtrip(tree)
    assert "g.MenuSwitch.geometry(" in code
    assert '"Object":' in code and '"Mesh":' in code
    assert "_MenuSwitchBase" not in code


def test_menu_switch_defaults_and_unlinked_items():
    """Unlinked items keep their default value (or None for linkable types);
    a non-first menu selection survives as an explicit argument."""
    with TreeBuilder("MenuDefaults") as tree:
        switch = g.MenuSwitch.float("B", {"A": 1.0, "B": tree.inputs.float("In")})
        geo = g.MenuSwitch.geometry(items={"Linked": g.Cube(), "Empty": None})
        switch >> tree.outputs.float("Out")
        geo >> tree.outputs.geometry("Geo")
    code = _assert_roundtrip(tree)
    assert 'g.MenuSwitch.float("B", {"A": 1.0,' in code
    assert '"Empty": None' in code
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt = ns["tree"].tree
    menu_node = next(
        n
        for n in rebuilt.nodes
        if n.bl_idname == "GeometryNodeMenuSwitch" and n.data_type == "FLOAT"
    )
    assert menu_node.inputs["Menu"].default_value == "B"


def test_menu_interface_default_deferred_after_body():
    """A menu interface input's default is set after the body, not inline: its
    valid values only exist once the consuming MenuSwitch has been linked, so
    setting it at creation would raise ``enum "X" not found in ()``."""
    with TreeBuilder("MenuIface") as tree:
        shape = tree.inputs.menu("Shape", "Circle")
        out = tree.outputs.integer("Out")
        g.MenuSwitch.integer(shape, {"Line": 0, "Circle": 1, "Curve": 2}) >> out
    code = _assert_roundtrip(tree)  # exec would raise if the default were inline
    lines = code.splitlines()
    create = next(i for i, ln in enumerate(lines) if "tree.inputs.menu(" in ln)
    deferred = next(
        i for i, ln in enumerate(lines) if 'shape.default_value = "Circle"' in ln
    )
    assert '"Circle"' not in lines[create]  # not passed at creation
    assert deferred > create  # set later, after the MenuSwitch in the body


def test_index_switch_emits_factory_tuple():
    """IndexSwitch round-trips item count and order as a tuple; literal
    defaults and the index input are preserved."""
    with TreeBuilder("IndexRT") as tree:
        idx = tree.inputs.integer("Choice")
        linked = tree.inputs.float("Linked")
        g.IndexSwitch.float(idx, (1.5, linked, 3.0)) >> tree.outputs.float("Out")
        g.IndexSwitch.integer(1, (10, 20)) >> tree.outputs.integer("Fixed")
    code = _assert_roundtrip(tree)
    assert "g.IndexSwitch.float(" in code
    assert "g.IndexSwitch.integer(1, (10, 20))" in code


# ---------------------------------------------------------------------------
# Variable-items nodes (CaptureAttribute / FieldToGrid)
# ---------------------------------------------------------------------------


def test_capture_attribute_emits_items_dict():
    """CaptureAttribute round-trips as the domain factory with an items dict;
    the captured output is read by item name."""
    with TreeBuilder("CaptureRT") as tree:
        geo = tree.inputs.geometry("Geo")
        cap = g.CaptureAttribute.point(geo, items={"Pos": g.Position()})
        cap.o.geometry >> tree.outputs.geometry("Out")
        g.StoreNamedAttribute.point.vector(
            cap.o.geometry, name="captured", value=cap.o["Pos"]
        ) >> tree.outputs.geometry("Stored")
    code = _assert_roundtrip(tree)
    assert 'g.CaptureAttribute.point(geometry=geo, items={"Pos":' in code
    assert "capture_attribute.o.pos" in code


def test_multi_word_output_accessor_round_trips():
    """An output read by a multi-word name emits ``.o.flip_and_cyclic``; the
    accessor must resolve that back to the socket named "Flip and Cyclic"
    (denormalize can't recover the lowercase connector "and")."""
    with TreeBuilder("MultiWord") as tree:
        geo = tree.inputs.geometry("Geo")
        cap = g.CaptureAttribute.point(geo, items={"Flip and Cyclic": g.Position()})
        cap.o["Flip and Cyclic"] >> tree.outputs.vector("V")
    code = _assert_roundtrip(tree)
    assert ".o.flip_and_cyclic" in code


def test_field_to_grid_emits_items_dict():
    """FieldToGrid round-trips as the data-type factory with an items dict."""
    with TreeBuilder("FieldGridRT") as tree:
        grid = tree.inputs.float("Grid", structure_type="GRID")
        mask = g.FieldToGrid.boolean(
            topology=grid, items={"Mask": g.Position().o.position.x > 0.0}
        )
        mask.o["Mask"] >> tree.outputs.boolean("Out", structure_type="GRID")
    code = _assert_roundtrip(tree)
    assert "g.FieldToGrid.boolean(" in code
    assert '"Mask":' in code
    assert "field_0" not in code


def test_bake_emits_items_dict():
    """Bake has no fixed inputs or type property: every socket is an item, so
    it round-trips as g.Bake(items={...}) read back by item name."""
    with TreeBuilder("BakeRT") as tree:
        geo = tree.inputs.geometry("Geo")
        bake = g.Bake(items={"Geometry": geo, "Factor": 1.5})
        bake.o["Geometry"] >> tree.outputs.geometry("Out")
        g.StoreNamedAttribute.point.float(
            bake.o["Geometry"], name="f", value=bake.o["Factor"]
        ) >> tree.outputs.geometry("Stored")
    code = _assert_roundtrip(tree)
    assert 'g.Bake(items={"Geometry": geo, "Factor": 1.5})' in code
    assert "item_0" not in code  # not the raw Item_N socket kwargs


def test_field_to_list_emits_constructor_items_dict():
    """FieldToList round-trips as g.FieldToList(count, items={...}); an unlinked
    non-default count is preserved."""
    with TreeBuilder("FieldListRT") as tree:
        pos = g.Position().o.position
        g.FieldToList(5, items={"x": pos.x, "flag": pos.y > 0.0})
    code = _assert_roundtrip(tree)
    assert "g.FieldToList(count=5, items={" in code
    assert '"x":' in code and '"flag":' in code
    assert "field_0" not in code


def test_combine_and_separate_bundle_round_trip():
    """CombineBundle bundles named sources; SeparateBundle pulls them back out
    by name and socket type. Both emit the items-dict form."""
    with TreeBuilder("BundleRT") as tree:
        geo = tree.inputs.geometry("Geo")
        val = tree.inputs.float("Val")
        bundle = g.CombineBundle(items={"Geometry": geo, "Factor": val})
        parts = g.SeparateBundle(
            bundle.o.bundle, items={"Geometry": "GEOMETRY", "Factor": "FLOAT"}
        )
        parts.o["Geometry"] >> tree.outputs.geometry("Out")
        parts.o["Factor"] >> tree.outputs.float("F")
    code = _assert_roundtrip(tree)
    assert 'g.CombineBundle(items={"Geometry": geo, "Factor": val})' in code
    assert "g.SeparateBundle(" in code
    assert '"Geometry": "GEOMETRY"' in code
    assert "item_0" not in code  # not the raw Item_N socket kwargs


def test_evaluate_closure_round_trip():
    """EvaluateClosure feeds linked values into a closure (input_items) and
    declares its results by type (output_items), read back via .o[name]."""
    with TreeBuilder("ClosureRT") as tree:
        fn = tree.inputs.closure("Fn")
        geo = tree.inputs.geometry("Geo")
        strength = tree.inputs.float("Strength")
        ev = g.EvaluateClosure(
            fn,
            input_items={"Geometry": geo, "Strength": strength},
            output_items={"Geometry": "GEOMETRY"},
        )
        ev.o["Geometry"] >> tree.outputs.geometry("Out")
    code = _assert_roundtrip(tree)
    assert "g.EvaluateClosure(fn, input_items={" in code
    assert 'output_items={"Geometry": "GEOMETRY"}' in code
    assert "item_0" not in code


def test_closure_zone_round_trip():
    """A ClosureZone defines a closure body: input_item reads feed the body,
    output_item targets collect results, and .closure produces the closure."""
    with TreeBuilder("ClosureZoneRT") as tree:
        cz = g.ClosureZone()
        geo = cz.input_item("Geometry", "GEOMETRY")
        g.SetPosition(geometry=geo).o.geometry >> cz.output_item("Geometry", "GEOMETRY")
        g.CombineXYZ(x=1.0).o.vector >> cz.output_item("Force", "VECTOR")
        ev = g.EvaluateClosure(
            cz.closure,
            input_items={"Geometry": tree.inputs.geometry("Geo")},
            output_items={"Force": "VECTOR"},
        )
        ev.o["Force"] >> tree.outputs.vector("Out")
    code = _assert_roundtrip(tree)
    assert "g.ClosureZone()" in code
    assert '.input_item("Geometry", "GEOMETRY")' in code
    assert '.output_item("Force", "VECTOR")' in code
    assert ".closure" in code
    assert "item_0" not in code  # no raw Item_N socket kwargs


# ---------------------------------------------------------------------------
# Recursive node groups
# ---------------------------------------------------------------------------


def _force_fresh_group_build():
    """Rename every existing node group so generated ``_build_group`` methods
    rebuild from scratch instead of reusing the originals by name."""
    import bpy

    for t in list(bpy.data.node_groups):
        t.name = "_orig_" + t.name


def test_custom_group_emits_recursive_class():
    """A node group round-trips as a CustomGeometryGroup subclass whose
    _build_group rebuilds the inner tree (verified by a forced fresh build)."""
    from nodebpy.nodes.geometry.groups import ClipFieldToBox

    with TreeBuilder("UsesGroup") as tree:
        obj = tree.inputs.object("Object")
        ClipFieldToBox(box_object=obj) >> tree.outputs.boolean("Out")

    code = to_python(tree)
    assert "from nodebpy.builder import CustomGeometryGroup" in code
    assert "class ClipFieldToBox(CustomGeometryGroup):" in code
    assert "def _build_group(self, tree):" in code
    assert 'ClipFieldToBox(**{"Box Object": object})' in code

    orig_top = _structure(tree.tree)
    inner = next(
        n.node_tree for n in tree.tree.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    orig_inner = _structure(inner)

    _force_fresh_group_build()
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt = ns["tree"].tree
    assert _structure(rebuilt) == orig_top, code
    rebuilt_inner = next(
        n.node_tree for n in rebuilt.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    assert _structure(rebuilt_inner) == orig_inner, code


def test_nested_groups_emit_in_dependency_order():
    """A group nested inside another emits both classes, the inner before the
    outer (so the outer's _build_group can reference it), and rebuilds fresh."""
    from nodebpy.builder import CustomGeometryGroup

    class Inner(CustomGeometryGroup):
        _name = "Nested Inner"

        def _build_group(self, tree):
            x = tree.inputs.float("X")
            (x + 1.0) >> tree.outputs.float("Y")

    class Outer(CustomGeometryGroup):
        _name = "Nested Outer"

        def _build_group(self, tree):
            x = tree.inputs.float("X")
            Inner(x=x) >> tree.outputs.float("Y")

    with TreeBuilder("UsesNested") as tree:
        v = tree.inputs.float("In")
        Outer(x=v) >> tree.outputs.float("Out")

    code = to_python(tree)
    lines = code.splitlines()
    inner_at = next(
        i for i, ln in enumerate(lines) if ln.startswith("class NestedInner")
    )
    outer_at = next(
        i for i, ln in enumerate(lines) if ln.startswith("class NestedOuter")
    )
    with_at = next(i for i, ln in enumerate(lines) if ln.startswith("with "))
    assert inner_at < outer_at < with_at  # dependency order, all before the tree

    orig_top = _structure(tree.tree)
    outer_tree = next(
        n.node_tree for n in tree.tree.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    orig_outer = _structure(outer_tree)

    _force_fresh_group_build()
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt = ns["tree"].tree
    assert _structure(rebuilt) == orig_top, code
    rebuilt_outer = next(
        n.node_tree for n in rebuilt.nodes if n.bl_idname == "GeometryNodeGroup"
    )
    assert _structure(rebuilt_outer) == orig_outer, code


# ---------------------------------------------------------------------------
# Mix / tuple-result methods / grid info accessors
# ---------------------------------------------------------------------------


def test_mix_lifts_to_factor_mix_method():
    """Mix emits ``factor.mix.<type>(a, b)``; a and b are required params so
    they render even at their default values."""
    with TreeBuilder("MixLift") as tree:
        fac = tree.inputs.float("Fac", 0.5)
        vec = tree.inputs.vector("V")
        fac.mix.float(0.0, 1.0) >> tree.outputs.float("F")
        fac.mix.vector(vec, (1.0, 1.0, 1.0)) >> tree.outputs.vector("Vec")
        fac.mix.color((1, 0, 0, 1), (0, 0, 1, 1)) >> tree.outputs.color("C")
    code = _assert_roundtrip(tree)
    assert "fac.mix.float(0.0, 1.0)" in code
    assert "fac.mix.vector(v, (1.0, 1.0, 1.0))" in code
    assert "fac.mix.color(" in code


def test_mix_nondefault_props_fall_back_to_constructor():
    """A blend_type the mix methods cannot express falls back to the
    constructor spelling."""
    with TreeBuilder("MixFallback") as tree:
        fac = tree.inputs.float("Fac", 0.5)
        node = g.Mix.color(fac, (1, 0, 0, 1), (0, 0, 1, 1))
        node.blend_type = "MULTIPLY"
        node.o.result_color >> tree.outputs.color("C")
    code = _assert_roundtrip(tree)
    assert ".mix.color(" not in code
    assert 'blend_type="MULTIPLY"' in code


def test_string_find_promotes_tuple_result_to_variable():
    """Both find() outputs consumed — the NamedTuple binds to a variable so
    the node is created exactly once."""
    with TreeBuilder("Find") as tree:
        string = tree.inputs.string()
        found = string.find("na")
        found.first_found >> tree.outputs.integer("First")
        found.count >> tree.outputs.integer("Count")
    code = _assert_roundtrip(tree)
    assert '= string.find("na")' in code
    assert ".first_found" in code
    assert ".count" in code


def test_string_find_single_output_inlines():
    with TreeBuilder("FindOne") as tree:
        string = tree.inputs.string()
        string.find("a").count >> tree.outputs.integer("Count")
    code = _assert_roundtrip(tree)
    assert 'string.find("a").count' in code


def test_matrix_svd_and_rotation_decompose():
    with TreeBuilder("Decompose") as tree:
        mat = tree.inputs.matrix("M")
        rot = tree.inputs.rotation("R")
        u, sing, _v = mat.svd()
        u.determinant() >> tree.outputs.float("DetU")
        sing >> tree.outputs.vector("S")
        quat = rot.to_quaternion()
        quat.w >> tree.outputs.float("W")
        quat.x >> tree.outputs.float("X")
        axis, angle = rot.to_axis_angle()
        axis >> tree.outputs.vector("Axis")
        angle >> tree.outputs.float("Angle")
    code = _assert_roundtrip(tree)
    assert "= m.svd()" in code
    assert ".u.determinant()" in code
    assert "= r.to_quaternion()" in code
    assert "= r.to_axis_angle()" in code


def test_disabled_socket_values_not_emitted():
    """Sockets disabled by the active mode (Length on an EVALUATED
    CurveToPoints) hold stale values that must not become kwargs."""
    with TreeBuilder("DisabledSockets") as tree:
        pts = g.CurveToPoints.evaluated(g.CurveCircle())
        # bpy string lookup skips disabled sockets — index to Length directly
        pts.node.inputs[2].default_value = 0.5
        pts >> tree.outputs.geometry("Points")
    code = _assert_roundtrip(tree)
    assert "length" not in code


def test_shader_tree_emits_shader_constructor():
    with TreeBuilder.shader("ShaderRT") as tree:
        s.PrincipledBSDF(roughness=0.25) >> tree.outputs.shader("Surface")
    code = _assert_roundtrip(tree)
    assert 'with TreeBuilder.shader("ShaderRT") as tree:' in code
    assert "from nodebpy import shader as s" in code


def test_compositor_tree_emits_compositor_constructor():
    with TreeBuilder.compositor("CompRT") as tree:
        img = tree.inputs.color("Image")
        img >> c.Kuwahara(size=4.0) >> tree.outputs.color("Out")
    code = _assert_roundtrip(tree)
    assert 'with TreeBuilder.compositor("CompRT") as tree:' in code
    assert "from nodebpy import compositor as c" in code


def _iface_structure(node_tree):
    """Interface signature: sockets with their expressible properties."""
    items = []
    for item in node_tree.interface.items_tree:
        if item.item_type != "SOCKET":
            continue
        parent = item.parent
        items.append(
            (
                item.name,
                item.socket_type,
                item.in_out,
                item.description,
                parent.name if parent is not None and parent.index != -1 else "",
                tuple(
                    (attr, str(getattr(item, attr)))
                    for attr in (
                        "subtype",
                        "min_value",
                        "max_value",
                        "hide_value",
                        "hide_in_modifier",
                        "default_input",
                        "structure_type",
                        "default_attribute_name",
                        "attribute_domain",
                    )
                    if hasattr(item, attr)
                ),
            )
        )
    return items


def test_interface_props_round_trip():
    with TreeBuilder("IfaceProps") as tree:
        val = tree.inputs.float(
            "Value",
            0.5,
            "How much",
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
            default_attribute="my_attr",
        )
        idx = tree.inputs.integer("Index", 0, default_input="INDEX")
        off = tree.inputs.vector("Offset", hide_value=True)
        (val + idx) >> tree.outputs.float("Out")
        off >> tree.outputs.vector("Off Out")
    code = _assert_roundtrip(tree)
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    assert _iface_structure(ns["tree"].tree) == _iface_structure(tree.tree), code
    assert 'description="How much"' in code
    assert "min_value=0.0" in code and "max_value=1.0" in code
    assert 'subtype="FACTOR"' in code
    assert 'default_attribute="my_attr"' in code
    assert 'default_input="INDEX"' in code
    assert "hide_value=True" in code


def test_interface_panels_round_trip():
    with TreeBuilder("IfacePanels") as tree:
        geo = tree.inputs.geometry("Geometry")
        with tree.inputs.panel("Settings", default_closed=True):
            size = tree.inputs.float("Size", 1.0)
            count = tree.inputs.integer("Count", 4)
        geo >> tree.outputs.geometry("Out")
        (size * count) >> tree.outputs.float("Sized")
    code = _assert_roundtrip(tree)
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    assert _iface_structure(ns["tree"].tree) == _iface_structure(tree.tree), code
    assert 'with tree.inputs.panel("Settings", default_closed=True):' in code
    assert '        size = tree.inputs.float("Size", 1.0)' in code


def _frame_structure(node_tree):
    """(node, parent frame label) pairs for frame fidelity comparison."""
    return sorted(
        (n.bl_idname, n.parent.label if n.parent is not None else None)
        for n in node_tree.nodes
        if n.bl_idname
        not in ("NodeFrame", "NodeReroute", "NodeGroupInput", "NodeGroupOutput")
    )


def test_frames_round_trip():
    with TreeBuilder("Frames") as tree:
        geo = tree.inputs.geometry("Geometry")
        with g.Frame("Deform"):
            warped = geo >> g.SetPosition(offset=(0.0, 0.0, 1.0))
        with g.Frame("Shade"):
            smooth = warped >> g.SetShadeSmooth()
        smooth >> tree.outputs.geometry("Out")
    code = _assert_roundtrip(tree)
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    assert _frame_structure(ns["tree"].tree) == _frame_structure(tree.tree), code
    assert 'with g.Frame("Deform"):' in code
    assert 'with g.Frame("Shade"):' in code


def test_nested_frames_round_trip():
    """Frames nested inside other frames (and a pure-container frame holding
    only sub-frames) re-emit as nested ``with g.Frame():`` blocks."""
    with TreeBuilder("NestedFrames") as tree:
        geo = tree.inputs.geometry("Geometry")
        with g.Frame("Outer"):
            with g.Frame("Inner A"):
                a = geo >> g.SetPosition(offset=(0.0, 0.0, 1.0))
            with g.Frame("Inner B"):
                b = a >> g.SetShadeSmooth()
        b >> tree.outputs.geometry("Out")

    def _frame_parents(node_tree):
        return sorted(
            (n.label, n.parent.label if n.parent else None)
            for n in node_tree.nodes
            if n.bl_idname == "NodeFrame"
        )

    orig_parents = _frame_parents(tree.tree)
    code = _assert_roundtrip(tree)
    assert 'with g.Frame("Outer"):' in code
    assert 'with g.Frame("Inner A"):' in code
    assert 'with g.Frame("Inner B"):' in code

    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt = ns["tree"].tree
    assert _frame_structure(rebuilt) == _frame_structure(tree.tree), code
    # "Inner A"/"Inner B" must be re-parented under "Outer", not top-level.
    assert _frame_parents(rebuilt) == orig_parents, code
    assert ("Inner A", "Outer") in orig_parents


def test_frame_interleaved_falls_back_flat():
    """A frame whose members must interleave with outside nodes cannot be
    one with-block — its nodes emit flat instead."""
    with TreeBuilder("FrameCycle") as tree:
        v = tree.inputs.float("V")
        a = v + 1.0
        b = a * 2.0
        c = b + 3.0
        c >> tree.outputs.float("Out")
        frame = g.Frame("F")
        a.node.parent = frame.node
        c.node.parent = frame.node
    code = _assert_roundtrip(tree)
    assert "Frame(" not in code


def test_long_expressions_split_into_variables():
    """Deep operator graphs split at the inline-width budget instead of
    collapsing into one statement; disabling the budget restores it."""
    with TreeBuilder("LongExpr") as tree:
        expr = tree.inputs.float("Value")
        for i in range(12):
            expr = expr * 1.5 + float(i)
        expr >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree)
    body = [line for line in code.splitlines() if line.strip()]
    assert all(len(line) <= 110 for line in body), code
    assert any(line.strip().startswith("math = ") for line in body), code

    # format=False so ruff doesn't re-wrap the long line we're asserting on.
    unbudgeted = to_python(tree, max_inline_width=None, format=False)
    assert any(len(line) > 110 for line in unbudgeted.splitlines())


def test_grid_info_accessors_dissolve():
    """GridInfo dissolves into .transform / .background_value on the grid
    socket; rebuilt code reuses one GridInfo node per grid."""
    with TreeBuilder("GridAccessors") as tree:
        vol = tree.inputs.geometry("Volume")
        grid = g.GetNamedGrid(vol, "density").o.grid
        grid.transform >> tree.outputs.matrix("T")
        grid.background_value >> tree.outputs.float("BG")
    code = _assert_roundtrip(tree)
    assert ".transform" in code
    assert ".background_value" in code
    assert "GridInfo" not in code


def _named_grid(tree, dtype="density"):
    vol = tree.inputs.geometry("Volume")
    return g.GetNamedGrid(vol, dtype).o.grid


def test_grid_numeric_methods_lift():
    """Mean / median lift to grid socket methods; data_type re-derived."""
    with TreeBuilder("GridNumeric") as tree:
        grid = _named_grid(tree)
        grid.mean(width=2, iterations=3) >> tree.outputs.float(
            "M", structure_type="GRID"
        )
        grid.median() >> tree.outputs.float("Md", structure_type="GRID")
    code = _assert_roundtrip(tree)
    assert ".mean(" in code
    assert ".median()" in code
    assert "g.GridMean(" not in code


def test_grid_float_operator_methods_lift():
    """Float-grid operators (gradient / sdf_* / to_mesh) lift to socket methods."""
    with TreeBuilder("GridFloatOps") as tree:
        grid = _named_grid(tree)
        grid.gradient() >> tree.outputs.vector("G", structure_type="GRID")
        grid.laplacian() >> tree.outputs.float("L", structure_type="GRID")
        grid.sdf_offset(distance=0.5) >> tree.outputs.float("O", structure_type="GRID")
        grid.sdf_mean(width=2) >> tree.outputs.float("SM", structure_type="GRID")
        grid.to_mesh(threshold=0.2) >> tree.outputs.geometry("Mesh")
    code = _assert_roundtrip(tree)
    assert ".gradient()" in code
    assert ".laplacian()" in code
    assert ".sdf_offset(" in code
    assert ".to_mesh(" in code


def test_grid_vector_operator_methods_lift():
    """Vector-grid operators (curl / divergence) lift to socket methods."""
    with TreeBuilder("GridVecOps") as tree:
        grid = g.GetNamedGrid.vector(tree.inputs.geometry("Volume"), "vel").o.grid
        grid.curl() >> tree.outputs.vector("C", structure_type="GRID")
        grid.divergence() >> tree.outputs.float("D", structure_type="GRID")
    code = _assert_roundtrip(tree)
    assert ".curl()" in code
    assert ".divergence()" in code


def test_grid_common_methods_lift():
    """Methods shared by every grid type (sample / clip / prune / …) lift."""
    with TreeBuilder("GridCommon") as tree:
        grid = _named_grid(tree)
        grid.sample(interpolation="Nearest Neighbor") >> tree.outputs.float("S")
        grid.sample_index(x=1, y=2, z=3) >> tree.outputs.float("SI")
        grid.clip(max_x=10) >> tree.outputs.float("Cl", structure_type="GRID")
        grid.dilate_erode(steps=2) >> tree.outputs.float("DE", structure_type="GRID")
        grid.prune(threshold=0.05, mode="SDF") >> tree.outputs.float(
            "P", structure_type="GRID"
        )
        grid.voxelize() >> tree.outputs.float("V", structure_type="GRID")
    code = _assert_roundtrip(tree)
    for snippet in (
        ".sample(",
        ".sample_index(",
        ".clip(",
        ".dilate_erode(",
        ".prune(",
        ".voxelize()",
    ):
        assert snippet in code, snippet


def test_grid_method_defers_when_rebuild_loses_structure():
    """A grid whose GRID structure is only *propagated* (an EvaluateClosure
    output) is lost on rebuild — the rebuilt output item carries no GRID
    structure — so codegen must fall back to the constructor rather than emit a
    method the rebuilt (non-grid) wrapper would lack. The closure output's
    structure is set directly on the node, mirroring an authored-in-Blender
    grid that nodebpy's closure API does not yet round-trip."""
    with TreeBuilder("GridDeferred") as tree:
        closure = tree.inputs.closure("Make Grid")
        evaluated = g.EvaluateClosure(closure, output_items={"Grid": "FLOAT"})
        evaluated.node.output_items[0].structure_type = "GRID"
        g.GridToMesh(grid=evaluated.o.grid) >> tree.outputs.geometry("Mesh")
    assert evaluated.o.grid.socket.inferred_structure_type == "GRID"
    code = _assert_roundtrip(tree)
    assert "g.GridToMesh(" in code
    assert ".to_mesh(" not in code


# ---------------------------------------------------------------------------
# Parametrised round-trip over every tree built in test_usecases.py
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("build", ROUNDTRIP_BUILDERS, ids=lambda b: b.__name__)
def test_roundtrip_usecases(build):
    _assert_roundtrip(build())


# ---------------------------------------------------------------------------
# Round-trip over Blender's bundled node-group assets (the "essentials"
# libraries shipped with bpy). These are real-world trees not authored through
# nodebpy, so they are the broadest available codegen coverage. Many use nodes
# or features codegen does not yet round-trip; those are marked xfail (see the
# asset backlog in PLAN.md). The set known to round-trip is asserted hard, so a
# regression in any of them fails the build.
# ---------------------------------------------------------------------------

# Each essentials/asset library holds node groups of a single tree type, so the
# per-type OK sets below are keyed by bare group name (unique within a type).
# Names DO collide across types (a geometry, shader and compositor "Combine
# Spherical" all exist), which is why membership is checked per tree type.
_GEOMETRY_ASSET_FILES = (
    "geometry_nodes_essentials.blend",
    "geometry_nodes_dynamics_assets.blend",
    "procedural_hair_node_assets.blend",
    "principal_components.blend",
)
_SHADER_ASSET_FILES = ("shading_nodes_essentials.blend",)
_COMPOSITOR_ASSET_FILES = ("compositing_nodes_essentials.blend",)

# Bundled geometry assets that currently round-trip cleanly. Everything else is
# xfailed; when a codegen gap is closed, re-measure and move names in here.
_ASSET_ROUNDTRIP_OK = frozenset(
    {
        "3D to Screen Space",
        "Array",
        "Attach Hair Curves to Surface",
        "Attachment Info",
        "Blend Hair Curves",
        "Box Selection",
        "Braid Hair Curves",
        "Capture Rest Geometry",
        "Cloth Dynamics (Experimental)",
        "Clump Hair Curves",
        "Collider",
        "Combine Cylindrical",
        "Combine Spherical",
        "Curl Hair Curves",
        "Create Guide Index Map",
        "Curve to Tube",
        "Curve Info",
        "Custom Force",
        "Curve Root",
        "Curve Segment",
        "Curve Tip",
        "Custom Effector",
        "Displace Geometry",
        "Displace Hair Curves",
        "Duplicate Hair Curves",
        "Edge Length",
        "Frizz Hair Curves",
        "Face Corner Angle",
        "Generate Hair Curves",
        "Geometry Input",
        "Geometry Principal Components",
        "Hair Curves Noise",
        "Hair Dynamics",
        "Instance on Elements",
        "Interpolate Hair Curves",
        "Is Edge Boundary",
        "Is Edge Loose",
        "Is Edge Manifold",
        "Is UV Split",
        "Normal Selection",
        "Principal Components",
        "Project with Depth",
        "Random Rotation",
        "Randomize Transforms",
        "Redistribute Curve Points",
        "Restore Curve Segment Length",
        "Roll Hair Curves",
        "Rotate Hair Curves",
        "Scatter on Surface",
        "Screen to 3D Space",
        "Separate Cylindrical",
        "Separate Spherical",
        "Set Hair Curve Profile",
        "Set Attachment Surface",
        "Shrinkwrap Hair Curves",
        "Set Effector",
        "Smooth by Angle",
        "Smooth Geometry",
        "Smooth Hair Curves",
        "Sphere Selection",
        "Straighten Hair Curves",
        "Transform and Project",
        "Trim Hair Curves",
    }
)

# Bundled shader assets that currently round-trip cleanly (keyed by name within
# shading_nodes_essentials.blend). Everything else is xfailed.
_SHADER_ASSET_OK = frozenset(
    {
        "Combine Cylindrical",
        "Combine Spherical",
        "Separate Cylindrical",
        "Separate Spherical",
    }
)

# Bundled compositor assets that currently round-trip cleanly.
_COMPOSITOR_ASSET_OK = frozenset(
    {
        "3D to Screen Space",
        "Chromatic Aberration",
        "Combine Cylindrical",
        "Combine Spherical",
        "Project with Depth",
        "Retime",
        "Screen to 3D Space",
        "Sensor Noise",
        "Separate Cylindrical",
        "Separate Spherical",
        "Sepia",
        "Split Toning",
        "Transform and Project",
        "Tune Image",
        "Unsharp Mask",
        "Vignette",
        "Film Grain",
    }
)

# (files, expected bl_idname, OK set) for each tree type's bundled libraries.
_ASSET_LIBRARIES = (
    (_GEOMETRY_ASSET_FILES, "GeometryNodeTree", _ASSET_ROUNDTRIP_OK),
    (_SHADER_ASSET_FILES, "ShaderNodeTree", _SHADER_ASSET_OK),
    (_COMPOSITOR_ASSET_FILES, "CompositorNodeTree", _COMPOSITOR_ASSET_OK),
)

_TREE_BUILDER_FOR = {
    "GeometryNodeTree": TreeBuilder.geometry,
    "ShaderNodeTree": TreeBuilder.shader,
    "CompositorNodeTree": TreeBuilder.compositor,
}


def _bundled_assets():
    """``[(path, name)]`` for every bundled node-group asset across the
    geometry, shader and compositor essentials libraries."""
    import os

    import bpy

    nodes_dir = os.path.join(bpy.utils.system_resource("DATAFILES"), "assets", "nodes")
    params = []
    for filenames, _bl_idname, ok in _ASSET_LIBRARIES:
        for filename in filenames:
            path = os.path.join(nodes_dir, filename)
            if not os.path.exists(path):
                continue
            with bpy.data.libraries.load(path, link=False, assets_only=True) as (
                src,
                _,
            ):
                names = list(src.node_groups)
            for name in names:
                marks = (
                    ()
                    if name in ok
                    else pytest.mark.xfail(
                        reason="codegen gap — see asset backlog in PLAN.md",
                        strict=False,
                    )
                )
                params.append(
                    pytest.param(
                        path, name, id=f"{filename.split('.')[0]}-{name}", marks=marks
                    )
                )
    return params


@pytest.mark.parametrize("path,name", _bundled_assets())
def test_roundtrip_bundled_asset(path, name):
    import bpy

    with bpy.data.libraries.load(path, link=False, assets_only=True) as (src, dst):
        if name not in src.node_groups:
            pytest.skip(f"{name!r} not in {path}")
        dst.node_groups = [name]
    group = dst.node_groups[0]
    builder = _TREE_BUILDER_FOR.get(group.bl_idname)
    if builder is None:
        pytest.skip(f"unsupported tree type {group.bl_idname}")
    _assert_roundtrip(builder(group))


# ---------------------------------------------------------------------------
# Regression tests for round-trip bugs first surfaced by MolecularNodes assets,
# reproduced here with hand-built trees so they run without the MN library.
# ---------------------------------------------------------------------------


def test_keyword_named_output_uses_suffixed_attribute():
    """An output socket whose name would normalize to a Python keyword (``From``
    → ``from``) is read via the suffixed attribute ``.o.from_`` — ``normalize_name``
    appends the underscore so the accessor resolves it and ``.o.from`` (a
    SyntaxError) is never emitted. (MN asset: "Sample Mixed Color".)"""
    from nodebpy.builder import CustomGeometryGroup

    class _KeywordOut(CustomGeometryGroup):
        _name = "KeywordOutGrp"

        def _build_group(self, tree):
            v = tree.inputs.float("Value")
            v >> tree.outputs.float("Value")
            v >> tree.outputs.integer("From")

    with TreeBuilder("KeywordOutTree") as tree:
        v = tree.inputs.float("Value")
        grp = _KeywordOut(**{"Value": v})
        grp.o["From"] >> tree.outputs.integer("Result")

    code = _assert_roundtrip(tree)
    assert ".o.from_" in code
    assert ".o.from " not in code


def test_links_into_inactive_sockets_are_dropped():
    """Links Blender keeps but ignores at evaluation (into sockets hidden by a
    ``data_type`` switch — here a Mix node set to RGBA still carries float A/B
    links) are not effective: they're excluded from emission and structural
    comparison so the tree round-trips. (MN asset: "Index Mix Color".)"""
    from nodebpy.export.codegen import _effective_links

    with TreeBuilder("InactiveMix", ignore_visibility=True) as tree:
        col = tree.inputs.color("Color")
        fac = tree.inputs.float("Fac")
        mix = g.Mix(
            data_type="RGBA",
            factor_float=fac,
            a_color=col,
            b_color=col,
            a_float=fac,
            b_float=fac,
        )
        mix.o.result_color >> tree.outputs.color("Result")

    mix_links = [
        link for link in tree.tree.links if link.to_node.bl_idname == "ShaderNodeMix"
    ]
    # The raw tree carries the inactive float A/B links...
    assert any(not link.to_socket.enabled for link in mix_links)
    # ...but they are not "effective" and so are filtered out.
    effective = [
        link
        for link in _effective_links(tree.tree)
        if link.to_node.bl_idname == "ShaderNodeMix"
    ]
    assert effective and all(link.to_socket.enabled for link in effective)

    code = _assert_roundtrip(tree)
    assert "a_float" not in code and "b_float" not in code


def test_axes_to_rotation_socket_property_collision():
    """A constructor param that names an input socket (AxesToRotation's
    ``primary_axis`` Vector socket) must not be mistaken for the same-named bpy
    enum property; the enum rides on the renamed ``primary`` param instead.
    (MN asset: "Plexus".)"""
    from nodebpy.export.codegen import _non_default_props

    with TreeBuilder("AxesRot") as tree:
        vec = tree.inputs.vector("V")
        node = g.AxesToRotation(primary_axis=vec)
        node.o.rotation >> tree.outputs.rotation("R")
        # Defaults: nothing emitted, and never the socket-named ``*_axis``.
        assert _non_default_props(node.node, g.AxesToRotation) == {}

    code = _assert_roundtrip(tree)
    assert "secondary_axis=" not in code
    assert "g.AxesToRotation(primary_axis=v)" in code

    # A non-default enum is applied by the constructor (the renamed ``primary``
    # param writes the bpy ``primary_axis`` property), emitted under that param,
    # and round-trips back onto the rebuilt node.
    with TreeBuilder("AxesRotProp") as tree:
        vec = tree.inputs.vector("V")
        node = g.AxesToRotation(primary_axis=vec, primary="X", secondary="Y")
        # the constructor must actually write the enum to the node
        assert node.node.primary_axis == "X"
        assert node.node.secondary_axis == "Y"
        node.o.rotation >> tree.outputs.rotation("R")
        assert _non_default_props(node.node, g.AxesToRotation) == {
            "primary": "X",
            "secondary": "Y",
        }

    code = _assert_roundtrip(tree)
    assert 'g.AxesToRotation(primary_axis=v, primary="X", secondary="Y")' in code
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt_axes = next(
        n for n in ns["tree"].tree.nodes if n.bl_idname == "FunctionNodeAxesToRotation"
    )
    assert rebuilt_axes.primary_axis == "X"
    assert rebuilt_axes.secondary_axis == "Y"


def test_property_rna_name_unreadable_getter_returns_none():
    """A proxy ``@property`` whose getter source can't be retrieved (here
    compiled from a string, so it has no source file) falls through to ``None``
    instead of raising — covers the defensive ``getsource`` guard."""
    from nodebpy.export.codegen import _property_rna_name

    ns: dict = {}
    exec(  # noqa: S102 — getter has no source file, so getsource() raises OSError
        "class C:\n"
        "    @property\n"
        "    def primary(self):\n"
        "        return self.node.primary_axis\n",
        ns,
    )
    # ``primary`` isn't itself a bpy prop, so resolution falls to the getter,
    # whose source is unavailable → the except branch returns None.
    assert _property_rna_name(ns["C"], "primary", {"primary_axis"}) is None


def test_duplicate_separators_on_one_source_stay_explicit():
    """Several separator nodes sharing a source socket must not all dissolve to
    the component accessor — ``_find_or_create_linked`` would collapse them into
    one node. They stay as explicit constructor calls so the count round-trips.
    (MN asset: "Color Mix Intermediate".)"""
    with TreeBuilder("DupSeparate") as tree:
        col = tree.inputs.color("Color")
        s1 = g.SeparateColor(color=col)
        s2 = g.SeparateColor(color=col)
        g.CombineColor(red=s1.o.red, green=s2.o.green) >> tree.outputs.color("Result")

    code = _assert_roundtrip(tree)
    assert code.count("g.SeparateColor(color=color)") == 2
    # not dissolved to the accessor sugar
    assert "color.r" not in code and "color.g" not in code


MN_FILE_PATH = (
    Path.cwd().parent / "MolecularNodes/molecularnodes/assets/node_data_file.blend"
)


def get_mn_asset_names():
    """Return the names of all node groups in the MolecularNodes asset library."""
    import bpy

    if not MN_FILE_PATH.exists():
        return []

    with bpy.data.libraries.load(
        str(MN_FILE_PATH),
        link=False,
        assets_only=True,
    ) as (src, _):
        return list(src.node_groups)


@pytest.mark.skipif(
    not MN_FILE_PATH.exists(),
    reason="MolecularNodes asset library not found",
)
@pytest.mark.parametrize("name", get_mn_asset_names())
def test_roundtrip_mn_assets(name):
    import bpy

    with bpy.data.libraries.load(
        str(MN_FILE_PATH),
        link=False,
        assets_only=True,
    ) as (src, dst):
        dst.node_groups = [name]
    group = dst.node_groups[0]
    builder = _TREE_BUILDER_FOR.get(group.bl_idname)
    if builder is None:
        pytest.skip(f"unsupported tree type {group.bl_idname}")
    _assert_roundtrip(builder(group))


def test_codegen_list_methods(snapshot):
    with g.tree() as tree:
        lst = g.FieldToList(10).vector()
        lst.filter(g.RandomValue.boolean()) >> tree.outputs.vector("Filtered")

    string = tree.to_python()
    assert ".filter(" in string
    assert snapshot == string
