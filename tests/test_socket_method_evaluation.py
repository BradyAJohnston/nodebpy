"""Socket methods evaluate to what the same maths gives in Python / numpy."""

import math

import numpy as np
import pytest
from mathutils import Euler, Vector

from nodebpy import geometry as g

from .evaluate import evaluate

V = (1.3, -2.6, 0.4)
W = (0.5, 0.7, -1.2)


def _wrap(value, low, high):
    span = high - low
    return value - span * np.floor((value - low) / span)


@pytest.mark.parametrize(
    "method, args, expected",
    [
        ("min", (W,), np.minimum(V, W)),
        ("max", (W,), np.maximum(V, W)),
        ("floor", (), np.floor(V)),
        ("ceil", (), np.ceil(V)),
        ("round", (), np.round(V)),
        ("fraction", (), np.subtract(V, np.floor(V))),
        ("sign", (), np.sign(V)),
        ("snap", ((0.5, 0.5, 0.5),), np.floor(np.divide(V, 0.5)) * 0.5),
        ("wrap", ((-1, -1, -1), (1, 1, 1)), _wrap(np.array(V), -1, 1)),
        ("sin", (), np.sin(V)),
        ("cos", (), np.cos(V)),
        ("tan", (), np.tan(V)),
        ("mul_add", (W, (1, 2, 3)), np.multiply(V, W) + (1, 2, 3)),
    ],
)
def test_vector_methods(method, args, expected):
    with g.tree("VectorMethod") as tree:
        result = evaluate(tree, r=getattr(g.Vector(V).o.vector, method)(*args))
    assert np.allclose(result["r"], expected, atol=1e-5)


def test_vector_faceforward_and_refract():
    normal = np.array((0.0, 0.0, 1.0))
    incident = np.array((0.6, 0.0, -0.8))
    ior = 1.0 / 1.33
    cos_i = -np.dot(normal, incident)
    k = 1 - ior**2 * (1 - cos_i**2)
    refracted = ior * incident + (ior * cos_i - np.sqrt(k)) * normal

    with g.tree("VectorFaceRefract") as tree:
        n = g.Vector(tuple(normal)).o.vector
        result = evaluate(
            tree,
            along=n.faceforward(tuple(incident), tuple(normal)),
            against=n.faceforward(tuple(-incident), tuple(normal)),
            refracted=g.Vector(tuple(incident)).o.vector.refract(n, ior),
        )
    assert np.allclose(result["along"], normal)
    assert np.allclose(result["against"], -normal)
    assert np.allclose(result["refracted"], refracted, atol=1e-5)


def test_vector_conversions():
    euler = (0.3, -0.8, 1.1)
    with g.tree("VectorConversions") as tree:
        matrix = g.CombineTransform(translation=(1, 2, 3), scale=(2, 2, 2))
        v = g.Vector(V).o.vector
        spherical = v.to_spherical()
        cylindrical = v.to_cylindrical()
        result = evaluate(
            tree,
            sr=spherical.r,
            sphi=spherical.phi,
            cr=cylindrical.r,
            cz=cylindrical.z,
            projected=v.project_point(matrix),
            rotated=g.Vector(W).o.vector.rotate(
                g.Vector(euler).o.vector.euler_to_rotation()
            ),
        )
    x, y, z = V
    assert result["sr"] == pytest.approx(math.dist(V, (0, 0, 0)), rel=1e-5)
    assert result["sphi"] == pytest.approx(math.atan2(y, x), rel=1e-5)
    assert result["cr"] == pytest.approx(math.hypot(x, y), rel=1e-5)
    assert result["cz"] == pytest.approx(z, rel=1e-5)
    assert np.allclose(result["projected"], np.multiply(V, 2) + (1, 2, 3))
    assert np.allclose(
        result["rotated"], Euler(euler).to_matrix() @ Vector(W), atol=1e-5
    )


INT_PAIRS = [(7, 2), (-7, 2), (9, 4), (12, 18)]


@pytest.mark.parametrize(
    "method, expected",
    [
        # halves round away from zero
        ("divide_round", lambda a, b: int(math.copysign(abs(a / b) + 0.5, a / b))),
        ("divide_ceiling", lambda a, b: math.ceil(a / b)),
        ("gcd", math.gcd),
        ("lcm", math.lcm),
    ],
)
def test_integer_methods(method, expected):
    with g.tree("IntegerMethod") as tree:
        result = evaluate(
            tree,
            **{
                f"v{i}": getattr(g.Integer(a).o.integer, method)(b)
                for i, (a, b) in enumerate(INT_PAIRS)
            },
        )
    assert [result[f"v{i}"] for i in range(len(INT_PAIRS))] == [
        expected(a, b) for a, b in INT_PAIRS
    ]


def test_integer_to_float():
    with g.tree("IntegerToFloat") as tree:
        result = evaluate(tree, f=g.Integer(-7).o.integer.to_float() / 2)
    assert result["f"] == pytest.approx(-3.5)


def test_float_methods():
    with g.tree("FloatMethods") as tree:
        f = g.Value(4.0).o.value
        result = evaluate(
            tree,
            smooth_min=f.smooth_min(6.0, 0.0),
            smooth_max=f.smooth_max(6.0, 0.0),
            blended=f.smooth_min(4.5, 1.0),
            inverse_sqrt=f.inverse_sqrt(),
            close=f.is_close(4.05, 0.1),
            far=f.is_close(4.05, 0.01),
        )
    assert result["smooth_min"] == pytest.approx(4.0)
    assert result["smooth_max"] == pytest.approx(6.0)
    assert result["blended"] < 4.0
    assert result["inverse_sqrt"] == pytest.approx(0.5)
    assert result["close"] and not result["far"]


@pytest.mark.parametrize("op", [round, math.floor, math.ceil, math.trunc])
def test_float_rounding_builtins(op):
    values = [2.3, -2.3, 2.7, -2.7, -0.4]
    with g.tree("FloatRounding") as tree:
        sockets = {f"v{i}": op(g.Value(v).o.value) for i, v in enumerate(values)}
        result = evaluate(tree, **sockets)
    assert [result[f"v{i}"] for i in range(len(values))] == [op(v) for v in values]


def test_round_rejects_ndigits():
    with g.tree("RoundDigits"), pytest.raises(TypeError):
        round(g.Value(1.25).o.value, 1)  # ty: ignore[no-matching-overload]


A = (0.2, 0.4, 0.6, 0.5)
B = (0.1, 0.3, 0.2, 0.8)


@pytest.mark.parametrize(
    "op, expected",
    [
        (lambda a, b: a + b, np.add(A[:3], B[:3])),
        (lambda a, b: a - b, np.subtract(A[:3], B[:3])),
        (lambda a, b: a * b, np.multiply(A[:3], B[:3])),
        (lambda a, b: a / b, np.divide(A[:3], B[:3])),
    ],
    ids=["add", "sub", "mul", "div"],
)
def test_color_arithmetic_keeps_left_alpha(op, expected):
    with g.tree("ColorArithmetic") as tree:
        a = g.Color(A).o.color
        result = evaluate(tree, sockets=op(a, g.Color(B).o.color), literal=op(a, B))
    for value in result.values():
        assert np.allclose(value[:3], expected, atol=1e-5)
        assert value[3] == pytest.approx(A[3])


def test_color_scalar_arithmetic_stays_vector():
    with g.tree("ColorScalar") as tree:
        result = evaluate(tree, r=g.Color(A).o.color * 0.5)
    assert np.allclose(result["r"], np.multiply(A[:3], 0.5))


def test_color_gamma():
    with g.tree("ColorGamma") as tree:
        result = evaluate(tree, r=g.Color(A).o.color.gamma(2.2))
    assert np.allclose(result["r"][:3], np.power(A[:3], 2.2), atol=1e-5)
    assert result["r"][3] == pytest.approx(A[3])


def test_bundle_methods():
    with g.tree("BundleMethods") as tree:
        a = g.CombineBundle().o.bundle.store("x", 1.0).store("n", 3)
        b = g.CombineBundle().o.bundle.store("x", 2.0).store("v", g.Vector(V))
        on_geometry = g.Points(1).o.points.set_bundle(a).bundle()
        result = evaluate(
            tree,
            x=a.get.float("x"),
            n=a.get.integer("n"),
            joined=a.join(b).get.float("x"),
            merged=(a | b).get.float("x"),
            v=(a | b).get.vector("v"),
            has=a.has("n"),
            missing=a.has("v"),
            from_geometry=on_geometry.get.integer("n"),
        )
    assert result["x"] == pytest.approx(1.0)
    assert result["n"] == 3
    # the later bundle wins on a duplicate path, like dict |
    assert result["joined"] == pytest.approx(2.0)
    assert result["merged"] == pytest.approx(2.0)
    assert np.allclose(result["v"], V)
    assert result["has"] and not result["missing"]
    assert result["from_geometry"] == 3
