"""nodebpy.math: numpy-style functions that build nodes, and their export."""

import math
import re

import numpy as np
import pytest
from mathutils import Euler, Matrix, Vector

import nodebpy.math as m
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.export.codegen import to_python

from .evaluate import evaluate
from .test_codegen import _assert_roundtrip
from .test_usecases import ROUNDTRIP_BUILDERS

V = (1.3, -2.6, 0.4)
W = (0.5, 0.7, -1.2)


def test_plain_inputs_build_a_node():
    with g.tree("NodeMathPlain"):
        result = m.sqrt(2)
    assert result.node.bl_idname == "ShaderNodeMath"
    assert result.node.operation == "SQRT"
    assert result.node.inputs[0].default_value == 2


@pytest.mark.parametrize(
    "build, bl_idname, state",
    [
        (lambda: m.abs(-3), "FunctionNodeIntegerMath", "ABSOLUTE"),
        (lambda: m.abs(-3.0), "ShaderNodeMath", "ABSOLUTE"),
        (lambda: m.abs(g.Position()), "ShaderNodeVectorMath", "ABSOLUTE"),
        (lambda: m.abs(True), "FunctionNodeIntegerMath", "ABSOLUTE"),
        (lambda: m.sqrt(4), "ShaderNodeMath", "SQRT"),
        (lambda: m.power(2, 0.5), "ShaderNodeMath", "POWER"),
        (lambda: m.sin(V), "ShaderNodeVectorMath", "SINE"),
        (lambda: m.fmod(g.Position(), 2.0), "ShaderNodeVectorMath", "MODULO"),
        (lambda: m.where(True, 1, 2), "GeometryNodeSwitch", "INT"),
        (lambda: m.where(True, 1, 2.5), "GeometryNodeSwitch", "FLOAT"),
        (lambda: m.where(g.Boolean(), V, W), "GeometryNodeSwitch", "VECTOR"),
        (lambda: m.lerp((1, 0, 0, 1), (0, 0, 1, 1), 0.5), "ShaderNodeMix", "RGBA"),
        (lambda: m.inv(g.EulerToRotation()), "FunctionNodeInvertRotation", None),
    ],
)
def test_node_follows_input_types(build, bl_idname, state):
    with g.tree("NodeMathDispatch"):
        node = build().node
    assert node.bl_idname == bl_idname
    if state is not None:
        assert state in (
            getattr(node, "operation", None),
            getattr(node, "data_type", None),
            getattr(node, "input_type", None),
        )


def test_integer_math_is_geometry_only():
    with s.material("NodeMathShader"):
        assert m.abs(-3).node.bl_idname == "ShaderNodeMath"


@pytest.mark.parametrize(
    "build",
    [
        lambda: m.sqrt(g.Position()),
        lambda: m.gcd(1.5, 2),  # ty: ignore[no-matching-overload]
        lambda: m.cross(g.CombineTransform(), V),
        lambda: m.det(V),  # ty: ignore[no-matching-overload]
    ],
)
def test_no_node_for_the_inputs(build):
    with g.tree("NodeMathError"), pytest.raises(TypeError):
        build()


def test_float_results_match_numpy():
    x, y = 0.7, -2.3
    with g.tree("NodeMathFloat") as tree:
        result = evaluate(
            tree,
            sqrt=m.sqrt(2),
            log=m.log(x),
            log2=m.log(8.0, 2.0),
            mod=m.mod(y, 1.5),
            fmod=m.fmod(y, 1.5),
            arctan2=m.arctan2(y, x),
            wrap=m.wrap(y, 0.0, 1.0),
            clip=m.clip(y, -1.0, 1.0),
            lerp=m.lerp(2.0, 4.0, 0.25),
            where=m.where(g.Boolean(False), 1.0, y),
            isclose=m.isclose(1.0, 1.0 + 1e-6),
            radians=m.radians(180.0),
        )
    expected = {
        "sqrt": math.sqrt(2),
        "log": np.log(x),
        "log2": 3.0,
        "mod": np.mod(y, 1.5),
        "fmod": np.fmod(y, 1.5),
        "arctan2": np.arctan2(y, x),
        "wrap": y - np.floor(y),
        "clip": -1.0,
        "lerp": 2.5,
        "where": y,
        "isclose": True,
        "radians": math.pi,
    }
    for name, value in expected.items():
        assert result[name] == pytest.approx(value, rel=1e-5), name


def test_integer_results_match_numpy():
    with g.tree("NodeMathInt") as tree:
        result = evaluate(
            tree,
            mod=m.mod(-7, 3),
            fmod=m.fmod(-7, 3),
            gcd=m.gcd(12, 18),
            lcm=m.lcm(4, 6),
            power=m.power(2, 10),
        )
    assert result["mod"] == np.mod(-7, 3)
    assert result["fmod"] == np.fmod(-7, 3)
    assert result["gcd"] == np.gcd(12, 18)
    assert result["lcm"] == np.lcm(4, 6)
    assert result["power"] == 2**10


def test_vector_results_match_numpy():
    with g.tree("NodeMathVector") as tree:
        v = g.Vector(V).o.vector
        result = evaluate(
            tree,
            dot=m.dot(v, W),
            cross=m.cross(v, W),
            norm=m.norm(v),
            distance=m.distance(v, W),
            normalize=m.normalize(v),
            minimum=m.minimum(v, W),
            wrap=m.wrap(v, (-1, -1, -1), (1, 1, 1)),
            sin=m.sin(v),
            lerp=m.lerp(v, W, 0.5),
        )
    a, b = np.array(V), np.array(W)
    assert result["dot"] == pytest.approx(a @ b, rel=1e-5)
    assert np.allclose(result["cross"], np.cross(a, b), atol=1e-5)
    assert result["norm"] == pytest.approx(np.linalg.norm(a), rel=1e-5)
    assert result["distance"] == pytest.approx(np.linalg.norm(a - b), rel=1e-5)
    assert np.allclose(result["normalize"], a / np.linalg.norm(a), atol=1e-5)
    assert np.allclose(result["minimum"], np.minimum(a, b))
    assert np.allclose(result["wrap"], a - 2 * np.floor((a + 1) / 2), atol=1e-5)
    assert np.allclose(result["sin"], np.sin(a), atol=1e-5)
    assert np.allclose(result["lerp"], (a + b) / 2, atol=1e-5)


def test_stub_is_current():
    """``python -m gen.math_stub`` regenerates src/nodebpy/math.pyi."""
    import importlib.util
    from pathlib import Path

    # load the file alone: importing the gen package runs its customizations,
    # which raise on a Blender that dropped a deprecated property
    path = Path(__file__).parents[1] / "gen" / "math_stub.py"
    spec = importlib.util.spec_from_file_location("_math_stub", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.STUB_PATH.read_text() == module.render()


def test_matrix_functions():
    with g.tree("NodeMathMatrix") as tree:
        matrix = g.CombineTransform(translation=(1, 2, 3), scale=(2, 2, 2))
        u, s_, v = m.svd(matrix)
        result = evaluate(
            tree,
            det=m.det(matrix),
            inverted=m.matmul(m.inv(matrix), V),
            transposed=m.det(m.transpose(matrix)),
            singular=s_,
        )
    assert result["det"] == pytest.approx(8.0, rel=1e-5)
    assert np.allclose(result["inverted"], (np.array(V) - (1, 2, 3)) / 2, atol=1e-5)
    assert result["transposed"] == pytest.approx(8.0, rel=1e-5)
    assert np.allclose(result["singular"], (2, 2, 2), atol=1e-5)


_STORE_TYPES = {
    "VALUE": "FLOAT",
    "INT": "INT",
    "BOOLEAN": "BOOLEAN",
    "VECTOR": "FLOAT_VECTOR",
    "RGBA": "FLOAT_COLOR",
    "ROTATION": "QUATERNION",
    "MATRIX": "FLOAT4X4",
}


def _every_function_tree():
    """A tree with one node per table entry, each fed by a linked input."""
    with g.tree("NodeMathEvery") as tree:
        f = tree.inputs.float("F")
        i = tree.inputs.integer("I")
        b = tree.inputs.boolean("B")
        v = tree.inputs.vector("V")
        mat = g.CombineTransform(translation=v).o.transform
        rot = g.EulerToRotation(v).o.rotation
        out = [
            m.abs(f), m.abs(i), m.abs(v), m.sign(f), m.sign(i), m.sign(v),
            m.floor(f), m.floor(v), m.ceil(f), m.ceil(v), m.round(f), m.round(v),
            m.trunc(f), m.fract(f), m.fract(v), m.sqrt(f), m.exp(f), m.log(f),
            m.log(f, 2.0), m.power(f, 3.0), m.power(i, 3), m.power(v, V),
            m.minimum(f, 1.0), m.minimum(i, 1), m.minimum(v, W),
            m.maximum(f, 1.0), m.maximum(i, 1), m.maximum(v, W),
            m.mod(f, 2.0), m.mod(i, 2), m.fmod(f, 2.0), m.fmod(i, 2),
            m.fmod(v, W), m.gcd(i, 6), m.lcm(i, 6), m.clip(f, 0.0, 1.0),
            m.wrap(f, 0.0, 2.0), m.wrap(v, V, W), m.snap(f, 0.5), m.snap(v, W),
            m.pingpong(f, 2.0), m.sin(f), m.sin(v), m.cos(f), m.cos(v), m.tan(f),
            m.tan(v), m.arcsin(f), m.arccos(f), m.arctan(f), m.arctan2(f, 1.0),
            m.sinh(f), m.cosh(f), m.tanh(f), m.radians(f), m.degrees(f),
            m.where(b, f, 1.0), m.where(b, i, 1), m.where(b, b, False),
            m.where(b, v, V), m.where(b, rot, rot), m.where(b, mat, mat),
            m.lerp(f, 1.0, 0.5), m.lerp(v, V, f), m.lerp(rot, rot, f),
            m.isclose(f, 1.0, 0.1), m.dot(v, W), m.cross(v, W), m.norm(v),
            m.normalize(v), m.distance(v, W), m.reflect(v, W),
            m.refract(v, W, 1.33), m.faceforward(v, V, W), m.project(v, W),
            m.inv(mat), m.inv(rot), m.det(mat), m.transpose(mat),
        ]  # fmt: skip
        geometry = g.Points(count=1).o.points
        for index, value in enumerate(out):
            geometry = g.StoreNamedAttribute(
                geometry,
                name=f"a{index}",
                value=value,
                data_type=_STORE_TYPES[value.socket.type],
            ).o.geometry
        geometry >> tree.outputs.geometry("Geometry")
    return tree


def test_export_writes_every_function():
    tree = _every_function_tree()
    code = _assert_roundtrip(tree, node_math=True)
    assert "from nodebpy import geometry as g, math as m" in code
    from nodebpy.math import _SPECS

    # abs and mod have operator forms, which win: abs(f), f % 2.0
    missing = [name for name in _SPECS if f"m.{name}(" not in code]
    assert missing == ["abs", "mod"], code
    assert "abs(f)" in code and "f % 2.0" in code


def test_export_is_opt_in_and_keeps_operators():
    with g.tree("NodeMathOperators") as tree:
        f = tree.inputs.float("F")
        (m.sqrt(f) + f) * 2.0 >> tree.outputs.float("Out")
    assert "m." not in to_python(tree)
    code = _assert_roundtrip(tree, node_math=True)
    assert "m.sqrt(" in code and " + " in code


def test_export_leaves_out_default_arguments():
    with g.tree("NodeMathDefaults") as tree:
        f = tree.inputs.float("F")
        m.log(f) >> tree.outputs.float("Out")
    code = _assert_roundtrip(tree, node_math=True)
    assert re.search(r"m\.log\(\w+\)", code), code


@pytest.mark.parametrize("build", ROUNDTRIP_BUILDERS, ids=lambda b: b.__name__)
def test_roundtrip_usecases_with_node_math(build):
    _assert_roundtrip(build(), node_math=True)


@pytest.mark.parametrize(
    "value, kind",
    [
        (Euler((0, 0, 1)), "ROTATION"),
        (Matrix.Identity(4), "MATRIX"),
        (Vector((1, 2, 3)), "VECTOR"),
        (np.zeros(3), "VECTOR"),
        ((1, 0, 0, 1), "COLOR"),
        ("text", None),
        (object(), None),
    ],
)
def test_value_kinds(value, kind):
    assert m._value_kind(value) == kind


def test_color_reads_as_vector_without_a_color_node():
    with g.tree("NodeMathColor") as tree:
        color = tree.inputs.color("C")
        assert m.sin(color).node.bl_idname == "ShaderNodeVectorMath"


@pytest.mark.parametrize(
    "build, bl_idname",
    [
        (lambda: m.matmul(g.CombineTransform(), g.CombineTransform()), "FunctionNodeMatrixMultiply"),
        (lambda: m.matmul(g.EulerToRotation(), g.EulerToRotation()), "FunctionNodeRotateRotation"),
        (lambda: m.matmul(g.EulerToRotation(), V), "FunctionNodeRotateVector"),
        (lambda: m.matmul(g.Position(), W), "ShaderNodeVectorMath"),
    ],
)  # fmt: skip
def test_matmul_follows_input_kinds(build, bl_idname):
    with g.tree("NodeMathMatmul"):
        assert build().node.bl_idname == bl_idname


def test_matmul_and_svd_reject_other_kinds():
    with g.tree("NodeMathMatmulError"):
        with pytest.raises(TypeError):
            m.matmul(1.0, g.Position())
        with pytest.raises(TypeError):
            m.svd(g.Position())


def test_every_table_factory_is_analysable():
    """Codegen reads each factory's operation and sockets from its source."""
    from nodebpy.export.codegen import _class_factories

    for spec in m._SPECS.values():
        for impl in spec.impls.values():
            if impl.factory is not None:
                paths = {f.path for f in _class_factories(m._impl_class(impl))}
                assert impl.factory in paths, impl


def test_export_falls_back_when_a_call_cannot_rebuild_the_node():
    with g.tree("NodeMathFallback") as tree:
        f = tree.inputs.float("F")
        i = tree.inputs.integer("I")
        out = [
            g.Math.square_root(f, use_clamp=True),  # a flag the call can't carry
            g.IntegerMath.greatest_common_divisor(f, i),  # a float m.gcd refuses
        ]
        for index, node in enumerate(out):
            node >> tree.outputs.float(f"Out{index}")
        g.InvertMatrix()  # a matrix input with no value to write
    code = _assert_roundtrip(tree, node_math=True)
    assert "m." not in code, code


@pytest.fixture
def partial_entries(monkeypatch):
    """Table entries that leave an input or output of their node unused."""
    from nodebpy.export.codegen import _node_math_index

    specs = {
        # ahead of the real entries, so they are tried first
        "first": m._Spec({"FLOAT": m._Impl("Math", "minimum", "value", ("value",))}),
        "xof": m._Spec({"VECTOR": m._Impl("SeparateXYZ", None, "x")}),
        **m._SPECS,
    }
    monkeypatch.setattr(m, "_SPECS", specs)
    monkeypatch.setattr(m, "first", lambda x: m._call("first", x), raising=False)
    monkeypatch.setattr(m, "xof", lambda v: m._call("xof", v), raising=False)
    _node_math_index.cache_clear()
    yield
    _node_math_index.cache_clear()


def test_export_checks_inputs_and_outputs_the_call_leaves_out(partial_entries):
    with g.tree("NodeMathPartial") as tree:
        f = tree.inputs.float("F")
        v = tree.inputs.vector("V")
        g.Math.minimum(f, 0.5) >> tree.outputs.float("Default")  # left out at default
        g.Math.minimum(f, 2.0) >> tree.outputs.float("Set")  # left out, off default
        g.Math.minimum(f, f) >> tree.outputs.float("Linked")  # left out, linked
        g.SeparateXYZ(v).o.x >> tree.outputs.float("X")
        g.SeparateXYZ(v).o.y >> tree.outputs.float("Y")  # another output
    code = to_python(tree, node_math=True)
    assert code.count("m.first(") == 1, code
    assert code.count("m.xof(") == 1, code
