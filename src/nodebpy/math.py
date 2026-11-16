"""Node math: numpy-style functions that build nodes.

```python
import nodebpy.math as m

m.sqrt(2)              # Math (Square Root) with 2 as its input
m.sin(position)        # Vector Math (Sine): the node follows the input type
m.cross(a, b)
m.where(cond, a, b)    # Switch
```

Every function builds a node and returns its output socket, plain Python
inputs included. The node is picked from the input types the way numpy picks
a dtype: vector over float over integer over boolean, with integer nodes only
in geometry trees. A function with no node for the inputs raises
``TypeError`` (``m.sqrt(vector)``, ``m.gcd(1.5, 2)``).

``to_python(tree, node_math=True)`` writes these calls back out.
"""

from __future__ import annotations

import inspect
from collections.abc import Sequence
from math import e, pi, tau
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from .builder.node import BaseNode
    from .builder.socket import (
        BooleanSocket,
        FloatSocket,
        ResultMatrixSVD,
        Socket,
        VectorSocket,
    )

__all__ = [
    "abs",
    "arccos",
    "arcsin",
    "arctan",
    "arctan2",
    "ceil",
    "clip",
    "cos",
    "cosh",
    "cross",
    "degrees",
    "det",
    "distance",
    "dot",
    "e",
    "exp",
    "faceforward",
    "floor",
    "fmod",
    "fract",
    "gcd",
    "inv",
    "isclose",
    "lcm",
    "lerp",
    "log",
    "matmul",
    "maximum",
    "minimum",
    "mod",
    "norm",
    "normalize",
    "pi",
    "pingpong",
    "power",
    "project",
    "radians",
    "reflect",
    "refract",
    "round",
    "sign",
    "sin",
    "sinh",
    "snap",
    "sqrt",
    "svd",
    "tan",
    "tanh",
    "tau",
    "transpose",
    "trunc",
    "where",
    "wrap",
]


class _Impl(NamedTuple):
    """One node a function can build."""

    cls: str  # class name in nodebpy.nodes.geometry
    factory: str | None  # dotted factory path on the class; None: the constructor
    output: str  # output accessor name (``node.o.<output>``)
    # factory parameters in the function's argument order; None: signature order
    params: tuple[str, ...] | None = None


class _Spec(NamedTuple):
    impls: dict[str, _Impl]  # input kind → node
    dispatch: tuple[int, ...] | None = None  # arguments that pick the kind


def _math(factory: str, **more: _Impl) -> dict[str, _Impl]:
    return {"FLOAT": _Impl("Math", factory, "value"), **more}


def _int(factory: str) -> _Impl:
    return _Impl("IntegerMath", factory, "value")


def _vec(factory: str, output: str = "vector", **kw: Any) -> _Impl:
    return _Impl("VectorMath", factory, output, **kw)


_SPECS: dict[str, _Spec] = {
    # element-wise
    "abs": _Spec(_math("absolute", INT=_int("absolute"), VECTOR=_vec("absolute"))),
    "sign": _Spec(_math("sign", INT=_int("sign"), VECTOR=_vec("sign"))),
    "floor": _Spec(_math("floor", VECTOR=_vec("floor"))),
    "ceil": _Spec(_math("ceil", VECTOR=_vec("ceil"))),
    "round": _Spec(_math("round", VECTOR=_vec("round"))),
    "trunc": _Spec(_math("truncate")),
    "fract": _Spec(_math("fraction", VECTOR=_vec("fraction"))),
    "sqrt": _Spec(_math("square_root")),
    "exp": _Spec(_math("exponent")),
    "log": _Spec(_math("logarithm")),
    "power": _Spec(_math("power", INT=_int("power"), VECTOR=_vec("power"))),
    "minimum": _Spec(_math("minimum", INT=_int("minimum"), VECTOR=_vec("minimum"))),
    "maximum": _Spec(_math("maximum", INT=_int("maximum"), VECTOR=_vec("maximum"))),
    "mod": _Spec(_math("floored_modulo", INT=_int("floored_modulo"))),
    "fmod": _Spec(_math("truncated_modulo", INT=_int("modulo"), VECTOR=_vec("modulo"))),
    "gcd": _Spec({"INT": _int("greatest_common_divisor")}),
    "lcm": _Spec({"INT": _int("least_common_multiple")}),
    "clip": _Spec({"FLOAT": _Impl("Clamp", "min_max", "result")}),
    # Blender's wrap inputs are (value, max, min)
    "wrap": _Spec(
        {
            "FLOAT": _Impl(
                "Math", "wrap", "value", ("value", "value_002", "value_001")
            ),
            "VECTOR": _vec("wrap", params=("vector", "vector_002", "vector_001")),
        }
    ),
    "snap": _Spec(_math("snap", VECTOR=_vec("snap"))),
    "pingpong": _Spec(_math("ping_pong")),
    "sin": _Spec(_math("sine", VECTOR=_vec("sine"))),
    "cos": _Spec(_math("cosine", VECTOR=_vec("cosine"))),
    "tan": _Spec(_math("tangent", VECTOR=_vec("tangent"))),
    "arcsin": _Spec(_math("arcsine")),
    "arccos": _Spec(_math("arccosine")),
    "arctan": _Spec(_math("arctangent")),
    "arctan2": _Spec(_math("arctan2")),
    "sinh": _Spec(_math("hyperbolic_sine")),
    "cosh": _Spec(_math("hyperbolic_cosine")),
    "tanh": _Spec(_math("hyperbolic_tangent")),
    "radians": _Spec(_math("to_radians")),
    "degrees": _Spec(_math("to_degrees")),
    # selection and blending
    "where": _Spec(
        {
            kind: _Impl("Switch", factory, "output", ("switch", "true", "false"))
            for kind, factory in (
                ("BOOLEAN", "boolean"),
                ("INT", "integer"),
                ("FLOAT", "float"),
                ("VECTOR", "vector"),
                ("COLOR", "color"),
                ("ROTATION", "rotation"),
                ("MATRIX", "matrix"),
            )
        },
        dispatch=(1, 2),
    ),
    "lerp": _Spec(
        {
            kind: _Impl("Mix", factory, f"result_{factory}", ("a", "b", "factor"))
            for kind, factory in (
                ("FLOAT", "float"),
                ("VECTOR", "vector"),
                ("COLOR", "color"),
                ("ROTATION", "rotation"),
            )
        },
        dispatch=(0, 1),
    ),
    "isclose": _Spec({"FLOAT": _Impl("Compare", "float.equal", "result")}),
    # linear algebra
    "dot": _Spec({"VECTOR": _vec("dot_product", "value")}),
    "cross": _Spec({"VECTOR": _vec("cross_product")}),
    "norm": _Spec({"VECTOR": _vec("length", "value")}),
    "normalize": _Spec({"VECTOR": _vec("normalize")}),
    "distance": _Spec({"VECTOR": _vec("distance", "value")}),
    "reflect": _Spec({"VECTOR": _vec("reflect")}),
    "refract": _Spec({"VECTOR": _vec("refract")}, dispatch=(0, 1)),
    "faceforward": _Spec({"VECTOR": _vec("faceforward")}),
    "project": _Spec({"VECTOR": _vec("project")}),
    "inv": _Spec(
        {
            "MATRIX": _Impl("InvertMatrix", None, "matrix"),
            "ROTATION": _Impl("InvertRotation", None, "rotation"),
        }
    ),
    "det": _Spec({"MATRIX": _Impl("MatrixDeterminant", None, "determinant")}),
    "transpose": _Spec({"MATRIX": _Impl("TransposeMatrix", None, "matrix")}),
}


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_SOCKET_KINDS = {
    "VALUE": "FLOAT",
    "INT": "INT",
    "BOOLEAN": "BOOLEAN",
    "VECTOR": "VECTOR",
    "RGBA": "COLOR",
    "ROTATION": "ROTATION",
    "MATRIX": "MATRIX",
}
# scalars and vectors promote upwards; rotations and matrices never convert
_LADDER = ("BOOLEAN", "INT", "FLOAT", "VECTOR")


def _value_kind(value: Any) -> str | None:
    """The input kind of an argument: a socket's type, or a plain value's."""
    from bpy.types import NodeSocket
    from mathutils import Euler, Matrix, Quaternion, Vector

    from .builder._utils import _NodeLike, _SocketLike

    if isinstance(value, (NodeSocket, _SocketLike, _NodeLike)):
        from .builder._utils import _output_socket_type

        return _SOCKET_KINDS.get(_output_socket_type(value) or "")
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    if isinstance(value, (Euler, Quaternion)):
        return "ROTATION"
    if isinstance(value, Matrix) or getattr(value, "shape", None) == (4, 4):
        return "MATRIX"
    if (
        isinstance(value, (Sequence, Vector)) and not isinstance(value, str)
    ) or getattr(value, "ndim", None) == 1:
        return {3: "VECTOR", 4: "COLOR"}.get(len(value))
    return None


def _resolve(name: str, kinds: Sequence[str | None], geometry: bool) -> str:
    """The kind of node ``m.<name>`` builds for arguments of these kinds.

    Shared with ``to_python``, which writes ``m.<name>(...)`` only when this
    picks the node being exported."""
    spec = _SPECS[name]
    available = set(spec.impls)
    if not geometry:
        available.discard("INT")  # Integer Math is geometry-only
    present = {kind for kind in kinds if kind is not None}
    for kind in ("MATRIX", "ROTATION"):
        if kind in present:
            if kind in available:
                return kind
            raise TypeError(f"m.{name} does not take {kind.lower()} inputs")
    if "COLOR" in present:
        if "COLOR" in available:
            return "COLOR"
        present = (present - {"COLOR"}) | {"VECTOR"}  # read as a vector
    start = max((_LADDER.index(k) for k in present), default=_LADDER.index("FLOAT"))
    for kind in _LADDER[start:]:
        if kind in available:
            return kind
    raise TypeError(f"m.{name} does not take {_LADDER[start].lower()} inputs")


def _dispatch_kinds(name: str, args: Sequence[Any]) -> list[Any]:
    """The arguments that pick the node, in order."""
    indices = _SPECS[name].dispatch
    return list(args) if indices is None else [args[i] for i in indices]


def _impl_params(impl: _Impl) -> tuple[str, ...]:
    """The factory (or constructor) parameters the arguments fill, in order."""
    if impl.params is not None:
        return impl.params
    return tuple(
        name
        for name, param in inspect.signature(_impl_callable(impl)).parameters.items()
        if name != "self"
        and param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    )


def _impl_class(impl: _Impl) -> type[BaseNode]:
    from .nodes import geometry

    return getattr(geometry, impl.cls)


def _impl_callable(impl: _Impl) -> Any:
    target: Any = _impl_class(impl)
    if impl.factory is None:
        return target
    for part in impl.factory.split("."):
        target = getattr(target, part)
    return target


def _current_tree_is_geometry() -> bool:
    from .builder.tree import TreeBuilder

    contexts = TreeBuilder._tree_contexts
    return not contexts or contexts[-1].tree.bl_idname == "GeometryNodeTree"


def _call(name: str, *args: Any) -> Any:
    kinds = [_value_kind(a) for a in _dispatch_kinds(name, args)]
    impl = _SPECS[name].impls[_resolve(name, kinds, _current_tree_is_geometry())]
    kwargs = dict(zip(_impl_params(impl), args, strict=True))
    node = _impl_callable(impl)(**kwargs)
    return getattr(node.o, impl.output)


# ---------------------------------------------------------------------------
# Element-wise
# ---------------------------------------------------------------------------


def abs(x: Any) -> Socket:
    """Absolute value (Math, Integer Math or Vector Math)."""
    return _call("abs", x)


def sign(x: Any) -> Socket:
    """-1, 0 or 1 by the sign of ``x`` (Math, Integer Math or Vector Math)."""
    return _call("sign", x)


def floor(x: Any) -> Socket:
    """Round down (Math or Vector Math). Returns a float, as numpy does."""
    return _call("floor", x)


def ceil(x: Any) -> Socket:
    """Round up (Math or Vector Math). Returns a float, as numpy does."""
    return _call("ceil", x)


def round(x: Any) -> Socket:
    """Round to the nearest whole number (Math or Vector Math); halves round
    away from zero, where numpy rounds them to even."""
    return _call("round", x)


def trunc(x: Any) -> FloatSocket:
    """Round towards zero (Math)."""
    return _call("trunc", x)


def fract(x: Any) -> Socket:
    """``x - floor(x)`` (Math or Vector Math)."""
    return _call("fract", x)


def sqrt(x: Any) -> FloatSocket:
    """Square root (Math)."""
    return _call("sqrt", x)


def exp(x: Any) -> FloatSocket:
    """``e ** x`` (Math)."""
    return _call("exp", x)


def log(x: Any, base: Any = e) -> FloatSocket:
    """Logarithm of ``x``, natural unless ``base`` is given (Math)."""
    return _call("log", x, base)


def power(x: Any, y: Any) -> Socket:
    """``x ** y`` (Math, Integer Math or Vector Math)."""
    return _call("power", x, y)


def minimum(x: Any, y: Any) -> Socket:
    """Element-wise minimum (Math, Integer Math or Vector Math)."""
    return _call("minimum", x, y)


def maximum(x: Any, y: Any) -> Socket:
    """Element-wise maximum (Math, Integer Math or Vector Math)."""
    return _call("maximum", x, y)


def mod(x: Any, y: Any) -> Socket:
    """Floored modulo, with the sign of ``y`` (Math or Integer Math), as
    numpy's ``mod`` and Python's ``%``."""
    return _call("mod", x, y)


def fmod(x: Any, y: Any) -> Socket:
    """Truncated modulo, with the sign of ``x`` (Math, Integer Math or Vector
    Math), as numpy's ``fmod``."""
    return _call("fmod", x, y)


def gcd(x: Any, y: Any) -> Socket:
    """Greatest common divisor (Integer Math)."""
    return _call("gcd", x, y)


def lcm(x: Any, y: Any) -> Socket:
    """Least common multiple (Integer Math)."""
    return _call("lcm", x, y)


def clip(x: Any, a_min: Any, a_max: Any) -> FloatSocket:
    """Clamp ``x`` between ``a_min`` and ``a_max`` (Clamp)."""
    return _call("clip", x, a_min, a_max)


def wrap(x: Any, min: Any, max: Any) -> Socket:
    """Wrap ``x`` into the range ``[min, max)`` (Math or Vector Math)."""
    return _call("wrap", x, min, max)


def snap(x: Any, step: Any) -> Socket:
    """Round ``x`` down to a multiple of ``step`` (Math or Vector Math)."""
    return _call("snap", x, step)


def pingpong(x: Any, scale: Any) -> FloatSocket:
    """Bounce ``x`` between 0 and ``scale`` (Math)."""
    return _call("pingpong", x, scale)


def sin(x: Any) -> Socket:
    """Sine (Math or Vector Math)."""
    return _call("sin", x)


def cos(x: Any) -> Socket:
    """Cosine (Math or Vector Math)."""
    return _call("cos", x)


def tan(x: Any) -> Socket:
    """Tangent (Math or Vector Math)."""
    return _call("tan", x)


def arcsin(x: Any) -> FloatSocket:
    """Inverse sine (Math)."""
    return _call("arcsin", x)


def arccos(x: Any) -> FloatSocket:
    """Inverse cosine (Math)."""
    return _call("arccos", x)


def arctan(x: Any) -> FloatSocket:
    """Inverse tangent (Math)."""
    return _call("arctan", x)


def arctan2(y: Any, x: Any) -> FloatSocket:
    """Angle of the point ``(x, y)`` (Math)."""
    return _call("arctan2", y, x)


def sinh(x: Any) -> FloatSocket:
    """Hyperbolic sine (Math)."""
    return _call("sinh", x)


def cosh(x: Any) -> FloatSocket:
    """Hyperbolic cosine (Math)."""
    return _call("cosh", x)


def tanh(x: Any) -> FloatSocket:
    """Hyperbolic tangent (Math)."""
    return _call("tanh", x)


def radians(x: Any) -> FloatSocket:
    """Degrees to radians (Math)."""
    return _call("radians", x)


def degrees(x: Any) -> FloatSocket:
    """Radians to degrees (Math)."""
    return _call("degrees", x)


# ---------------------------------------------------------------------------
# Selection and blending
# ---------------------------------------------------------------------------


def where(condition: Any, x: Any, y: Any) -> Socket:
    """``x`` where ``condition`` is true, else ``y`` (Switch)."""
    return _call("where", condition, x, y)


def lerp(a: Any, b: Any, t: Any) -> Socket:
    """Blend from ``a`` to ``b`` by ``t`` (Mix)."""
    return _call("lerp", a, b, t)


def isclose(a: Any, b: Any, atol: Any = 0.0001) -> BooleanSocket:
    """Whether ``a`` and ``b`` differ by at most ``atol`` (Compare)."""
    return _call("isclose", a, b, atol)


# ---------------------------------------------------------------------------
# Linear algebra
# ---------------------------------------------------------------------------


def dot(a: Any, b: Any) -> FloatSocket:
    """Dot product (Vector Math)."""
    return _call("dot", a, b)


def cross(a: Any, b: Any) -> VectorSocket:
    """Cross product (Vector Math)."""
    return _call("cross", a, b)


def norm(x: Any) -> FloatSocket:
    """Length of a vector (Vector Math)."""
    return _call("norm", x)


def normalize(x: Any) -> VectorSocket:
    """Unit vector in the direction of ``x`` (Vector Math)."""
    return _call("normalize", x)


def distance(a: Any, b: Any) -> FloatSocket:
    """Distance between two points (Vector Math)."""
    return _call("distance", a, b)


def reflect(x: Any, normal: Any) -> VectorSocket:
    """Reflect ``x`` about ``normal`` (Vector Math)."""
    return _call("reflect", x, normal)


def refract(x: Any, normal: Any, eta: Any) -> VectorSocket:
    """Refract ``x`` through a surface with ``normal`` and index ratio ``eta``
    (Vector Math)."""
    return _call("refract", x, normal, eta)


def faceforward(x: Any, incident: Any, reference: Any) -> VectorSocket:
    """``x``, flipped to point away from a surface (Vector Math)."""
    return _call("faceforward", x, incident, reference)


def project(a: Any, b: Any) -> VectorSocket:
    """Projection of ``a`` onto ``b`` (Vector Math)."""
    return _call("project", a, b)


def inv(x: Any) -> Socket:
    """Inverse of a matrix (Invert Matrix) or rotation (Invert Rotation)."""
    return _call("inv", x)


def det(x: Any) -> FloatSocket:
    """Determinant of a matrix (Matrix Determinant)."""
    return _call("det", x)


def transpose(x: Any) -> Socket:
    """Transpose of a matrix (Transpose Matrix)."""
    return _call("transpose", x)


def svd(x: Any) -> ResultMatrixSVD:
    """Singular value decomposition ``(u, s, v)`` of a matrix (Matrix SVD)."""
    from .builder.socket import ResultMatrixSVD
    from .nodes.geometry import MatrixSVD

    if _value_kind(x) != "MATRIX":
        raise TypeError("m.svd takes a matrix")
    o = MatrixSVD(x).o
    return ResultMatrixSVD(o.u, o.s, o.v)


def matmul(a: Any, b: Any) -> Socket:
    """``a @ b`` by the input kinds: matrix product (Multiply Matrices), matrix
    times point (Transform Point), rotation composition (Rotate Rotation, ``b``
    first), rotated vector (Rotate Vector) or dot product (Vector Math)."""
    from .nodes import geometry as g

    kinds = (_value_kind(a), _value_kind(b))
    if kinds == ("MATRIX", "MATRIX"):
        return g.MultiplyMatrices(a, b).o.matrix
    if kinds == ("MATRIX", "VECTOR"):
        return g.TransformPoint(b, a).o.vector
    if kinds == ("ROTATION", "ROTATION"):
        return g.RotateRotation(a, b, rotation_space="LOCAL").o.rotation
    if kinds == ("ROTATION", "VECTOR"):
        return g.RotateVector(b, a).o.vector
    if kinds == ("VECTOR", "VECTOR"):
        return dot(a, b)
    raise TypeError(f"m.matmul does not take {kinds[0]} @ {kinds[1]}".lower())
