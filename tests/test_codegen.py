# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for nodebpy.codegen.to_python() — node tree → Python code generation."""

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.codegen import CodegenError, to_python


def _structure(node_tree):
    """A comparable structural signature: nodes (with key props) and links."""
    from nodebpy.codegen import _effective_links

    nodes = sorted(
        (
            n.bl_idname,
            str(getattr(n, "operation", "")),
            str(getattr(n, "data_type", "")),
            str(getattr(n, "domain", "")),
            str(getattr(n, "mode", "")),
        )
        for n in node_tree.nodes
        if n.bl_idname not in ("NodeReroute", "NodeFrame")
    )

    def _socket_key(node, socket):
        # Interface socket identifiers (Socket_N) depend on declaration order;
        # compare group in/out sockets by name instead.
        if node.bl_idname in ("NodeGroupInput", "NodeGroupOutput"):
            return socket.name
        return socket.identifier

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
    code = to_python(tree)
    ns: dict = {}
    exec(code, ns)  # noqa: S102
    rebuilt: TreeBuilder = ns["tree"]
    assert _structure(rebuilt.tree) == _structure(tree.tree), code
    return code


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
    """Non-liftable operation (SINE) stays a call — via the factory shortcut."""
    with TreeBuilder("MathSine") as tree:
        val = tree.inputs.float("Value", 1.0)
        g.Math(val, operation="SINE") >> tree.outputs.float("Result")
    code = to_python(tree)
    assert "g.Math.sine(value)" in code


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
            a=vec, b=(0.5, 0.5, 0.5), operation="LESS_THAN", data_type="VECTOR", mode="AVERAGE"
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
    from nodebpy.codegen import _get_node_registry

    with TreeBuilder("Unsupported") as tree:
        g.SetPosition()
    monkeypatch.delitem(_get_node_registry(), "GeometryNodeSetPosition")
    with pytest.raises(CodegenError, match="GeometryNodeSetPosition"):
        to_python(tree)


def test_unsupported_node_placeholder_when_not_strict(monkeypatch):
    from nodebpy.codegen import _get_node_registry

    with TreeBuilder("UnsupportedLoose") as tree:
        g.SetPosition()
    monkeypatch.delitem(_get_node_registry(), "GeometryNodeSetPosition")
    code = to_python(tree, strict=False)
    assert "TODO: unsupported node" in code


def test_register_emitter_overrides_default():
    from nodebpy.codegen import _EMITTERS, BinOp, Call, register_emitter

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
        (
            geo_in
            >> g.SetPosition(offset=pos)
            >> g.TransformGeometry()
            >> tree.outputs.geometry()
        )
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


# ---------------------------------------------------------------------------
# Zones — emitted as zone wrappers with item handles
# ---------------------------------------------------------------------------


def test_dict_expr_renders():
    from nodebpy.codegen import DictExpr, Lit, Ref

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
