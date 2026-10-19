"""Operators on sockets evaluate to what Python gives for the same values."""

import operator

import numpy as np
import pytest

from nodebpy import geometry as g

from .evaluate import evaluate

INTS = [(7, 3), (-7, 3), (7, -3), (-7, -3), (0, 5), (12, 10)]
FLOATS = [(7.5, 2.0), (-7.5, 2.0), (7.5, -2.0), (-7.5, -2.0), (0.25, 4.0)]
MIXED = [(7, 2.5), (-7, 2.5), (7.5, -2)]

ARITHMETIC = [
    operator.add,
    operator.sub,
    operator.mul,
    operator.truediv,
    operator.floordiv,
    operator.mod,
]
COMPARISON = [
    operator.lt,
    operator.le,
    operator.gt,
    operator.ge,
    operator.eq,
    operator.ne,
]
BITWISE = [operator.and_, operator.or_, operator.xor]


def _socket(value):
    if isinstance(value, int):
        return g.Integer(value).o.integer
    return g.Value(value).o.value


def _assert_binary(op, pairs):
    """Evaluate ``op`` on every pair as socket∘socket, socket∘literal and
    literal∘socket, and compare each with Python's result."""
    forms = {
        "ss": lambda a, b: op(_socket(a), _socket(b)),
        "sl": lambda a, b: op(_socket(a), b),
        "ls": lambda a, b: op(a, _socket(b)),
    }
    with g.tree("OperatorEvaluation") as tree:
        values = {
            f"{form}_{index}": build(a, b)
            for index, (a, b) in enumerate(pairs)
            for form, build in forms.items()
        }
        result = evaluate(tree, **values)

    mismatches = []
    for index, (a, b) in enumerate(pairs):
        expected = op(a, b)
        for form in forms:
            actual = result[f"{form}_{index}"]
            if not np.isclose(actual, expected, rtol=1e-6):
                mismatches.append(
                    f"{form}: {a!r} {op.__name__} {b!r} = {actual}, Python {expected!r}"
                )
    assert not mismatches, "\n".join(mismatches)


@pytest.mark.parametrize("op", ARITHMETIC + COMPARISON, ids=lambda op: op.__name__)
def test_integer_operators_match_python(op):
    _assert_binary(op, INTS)


@pytest.mark.parametrize("op", ARITHMETIC + COMPARISON, ids=lambda op: op.__name__)
def test_float_operators_match_python(op):
    _assert_binary(op, FLOATS)


@pytest.mark.parametrize("op", ARITHMETIC + COMPARISON, ids=lambda op: op.__name__)
def test_mixed_operators_match_python(op):
    _assert_binary(op, MIXED)


@pytest.mark.parametrize("op", BITWISE, ids=lambda op: op.__name__)
def test_integer_bitwise_operators_match_python(op):
    _assert_binary(op, INTS)


def test_power_matches_python():
    _assert_binary(operator.pow, [(2, 3), (-2, 3), (3, 0), (2.5, 2.0), (2.0, 0.5)])


@pytest.mark.parametrize(
    "op", [operator.neg, abs, operator.invert], ids=lambda op: op.__name__
)
def test_integer_unary_operators_match_python(op):
    values = [7, -7, 0]
    with g.tree("UnaryEvaluation") as tree:
        result = evaluate(
            tree, **{f"v{i}": op(_socket(v)) for i, v in enumerate(values)}
        )
    assert [result[f"v{i}"] for i in range(len(values))] == [op(v) for v in values]


@pytest.mark.parametrize("op", [operator.neg, abs], ids=lambda op: op.__name__)
def test_float_unary_operators_match_python(op):
    values = [7.5, -7.5, 0.0]
    with g.tree("UnaryEvaluation") as tree:
        result = evaluate(
            tree, **{f"v{i}": op(_socket(v)) for i, v in enumerate(values)}
        )
    assert np.allclose(
        [result[f"v{i}"] for i in range(len(values))], [op(v) for v in values]
    )
