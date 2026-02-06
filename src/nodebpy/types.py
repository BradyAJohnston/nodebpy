from __future__ import annotations

import typing
from typing import Literal

from bpy.types import (
    Collection,
    Material,
    NodeSocket,
    NodeSocketBool,
    NodeSocketBundle,
    NodeSocketClosure,
    NodeSocketCollection,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketGeometry,
    NodeSocketImage,
    NodeSocketInt,
    NodeSocketMaterial,
    NodeSocketMatrix,
    NodeSocketMenu,
    NodeSocketObject,
    NodeSocketString,
    NodeSocketVector,
    Object,
)
from mathutils import Euler

if typing.TYPE_CHECKING:
    from .builder import NodeBuilder, SocketLinker


def _is_default_value(value: TYPE_INPUT_ALL):
    return isinstance(value, (int, float, str, bool, tuple, list, Euler))


# Type aliases for node inputs using typing.Union for runtime compatibility
LINKABLE = typing.Union["NodeBuilder", "SocketLinker", NodeSocket, None]
TYPE_INPUT_ROTATION = typing.Union[
    tuple[float, float, float], float, int, Euler, LINKABLE
]
TYPE_INPUT_BOOLEAN = typing.Union[
    bool, LINKABLE, NodeSocketBool, NodeSocketInt, NodeSocketFloat, NodeSocketVector
]
TYPE_INPUT_VALUE = typing.Union[float, int, LINKABLE, NodeSocketInt, NodeSocketFloat]
TYPE_INPUT_INT = typing.Union[
    int, LINKABLE, NodeSocketInt, NodeSocketInt, NodeSocketInt
]
TYPE_INPUT_VECTOR = typing.Union[
    typing.Tuple[float, float, float],
    LINKABLE,
    TYPE_INPUT_INT,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_BOOLEAN,
    NodeSocketVector,
    NodeSocketColor,
    TYPE_INPUT_ROTATION,
]


TYPE_INPUT_COLOR = typing.Union[
    LINKABLE, tuple[float, float, float, float], NodeSocketColor
]
TYPE_INPUT_STRING = typing.Union[str, LINKABLE, NodeSocketString]
TYPE_INPUT_GEOMETRY = typing.Union[LINKABLE, NodeSocketGeometry]
TYPE_INPUT_OBJECT = typing.Union[LINKABLE, NodeSocketObject, Object]
TYPE_INPUT_MATERIAL = typing.Union[LINKABLE, NodeSocketMaterial, Material]
TYPE_INPUT_IMAGE = typing.Union[LINKABLE, NodeSocketImage]
TYPE_INPUT_COLLECTION = typing.Union[LINKABLE, NodeSocketCollection, Collection]
TYPE_INPUT_MATRIX = typing.Union[LINKABLE, NodeSocketMatrix]
TYPE_INPUT_GRID = typing.Union[
    TYPE_INPUT_VALUE, TYPE_INPUT_VECTOR, TYPE_INPUT_BOOLEAN, TYPE_INPUT_INT
]
TYPE_INPUT_MENU = typing.Union[LINKABLE, NodeSocketMenu]
TYPE_INPUT_BUNDLE = typing.Union[LINKABLE, NodeSocketBundle]
TYPE_INPUT_CLOSURE = typing.Union[LINKABLE, NodeSocketClosure]

TYPE_INPUT_DATA = typing.Union[
    TYPE_INPUT_VALUE,
    TYPE_INPUT_INT,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_VECTOR,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_MATRIX,
]

TYPE_INPUT_ALL = typing.Union[
    TYPE_INPUT_VALUE,
    TYPE_INPUT_INT,
    TYPE_INPUT_STRING,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_MATERIAL,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_VECTOR,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_MENU,
    TYPE_INPUT_ROTATION,
]

_AccumulateFieldDataTypes = Literal["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"]

_AttributeDomains = typing.Literal[
    "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
]
_DeleteGeometryDomains = typing.Literal[
    "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
]
_BakedDataTypeValues = (
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "GEOMETRY",
    "BUNDLE",
)
_IntegerMathOperations = Literal[
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "MULTIPLY_ADD",
    "ABSOLUTE",
    "NEGATE",
    "POWER",
    "MINIMUM",
    "MAXIMUM",
    "SIGN",
    "DIVIDE_ROUND",
    "DIVIDE_FLOOR",
    "DIVIDE_CEIL",
    "FLOORED_MODULO",
    "MODULO",
    "GCD",
    "LCM",
]
_BakeDataTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "GEOMETRY",
    "BUNDLE",
]

_GridDataTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
]
_AdvectGridIntegration = Literal[
    "Semi-Lagrangian",
    "Midpoint",
    "Runge-Kutta 3",
    "Runge-Kutta 4",
    "MacCormack",
    "BFECC",
]

_DeleteGeoemtryModes = Literal["ALL", "EDGE_FACE", "ONLY_FACE"]
_RandomValueDataTypes = Literal["FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR"]
_EvaluateAtIndexDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR", "FLOAT_COLOR", "QUATERNION", "FLOAT4X4"
]
_DuplicateElementsDomains = Literal[
    "POINT", "EDGE", "FACE", "SPLINE", "LAYER", "INSTANCE"
]

_AttributeDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX"
]
_MixDataTypes = Literal["FLOAT", "VECTOR", "COLOR", "ROTATION"]


_MixColorBlendTypes = Literal[
    "MIX",
    "DARKEN",
    "MULTIPLY",
    "BURN",
    "LIGHTEN",
    "SCREEN",
    "DODGE",
    "ADD",
    "OVERLAY",
    "SOFT_LIGHT",
    "LINEAR_LIGHT",
    "DIFFERENCE",
    "EXCLUSION",
    "SUBTRACT",
    "DIVIDE",
    "HUE",
    "SATURATION",
    "COLOR",
    "VALUE",
]

_RaycaseDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR", "FLOAT_COLOR", "QUATERNION", "FLOAT4X4"
]
_SampleIndexDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR", "FLOAT_COLOR", "QUATERNION", "FLOAT4X4"
]

_EvaluateCurveModes = Literal["EVALUATED", "COUNT", "LENGTH"]

_StoreNamedAttributeTypes = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "FLOAT_VECTOR",
    "FLOAT_COLOR",
    "QUATERNION",
    "FLOAT4X4",
    "STRING",
    "INT8",
    "FLOAT2",
    "BYTE_COLOR",
]

_SocketShapeStructureType = Literal["AUTO", "DYNAMIC", "FIELD", "GRID", "SINGLE"]

_VectorMathOperations = Literal[
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "MULTIPLY_ADD",
    "CROSS_PRODUCT",
    "PROJECT",
    "REFLECT",
    "REFRACT",
    "FACEFORWARD",
    "DOT_PRODUCT",
    "DISTANCE",
    "LENGTH",
    "SCALE",
    "NORMALIZE",
    "ABSOLUTE",
    "POWER",
    "SIGN",
    "MINIMUM",
    "MAXIMUM",
    "FLOOR",
    "CEIL",
    "FRACTION",
    "MODULO",
    "WRAP",
    "SNAP",
    "SINE",
    "COSINE",
    "TANGENT",
]


SOCKET_TYPES = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "MENU",
    "OBJECT",
    "GEOMETRY",
    "COLLECTION",
    "IMAGE",
    "MATERIAL",
    "BUNDLE",
    "CLOSURE",
]

SOCKET_COMPATIBILITY: dict[str, tuple[str]] = {
    "VALUE": (
        "VALUE",
        "VECTOR",
        "INT",
        "BOOLEAN",
        "RGBA",
        "ROTATION",
    ),
    "INT": (
        "INT",
        "VALUE",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
    ),
    "BOOLEAN": (
        "BOOLEAN",
        "INT",
        "VALUE",
        "VECTOR",
        "RGBA",
    ),
    "VECTOR": (
        "VECTOR",
        "RGBA",
        "ROTATION",
        "VALUE",
        "INT",
        "BOOLEAN",
    ),
    "RGBA": (
        "RGBA",
        "VECTOR",
        "VALUE",
        "INT",
        "BOOLEAN",
    ),
    "ROTATION": (
        "ROTATION",
        "MATRIX",
        "VECTOR",
    ),
    "MATRIX": (
        "MATRIX",
        "ROTATION",
    ),
    "STRING": ("STRING",),
    "MENU": ("MENU",),
    "OBJECT": ("OBJECT",),
    "GEOMETRY": ("GEOMETRY",),
    "COLLECTION": ("COLLECTION",),
    "IMAGE": ("IMAGE",),
    "MATERIAL": ("MATERIAL",),
    "BUNDLE": ("BUNDLE",),
    "CLOSURE": ("CLOSURE",),
}


class DataTypes:
    FLOAT = "FLOAT"
    INT = "INT"
    BOOL = "BOOL"
    VECTOR = "VECTOR"
    ROTATION = "ROTATION"
    COLOR = "COLOR"
    RGBA = "RGBA"


class AttributeTypes:
    FLOAT = "FLOAT_VECTOR"
    INT = "INT"
    BOOL = "BOOL"
    VECTOR = "VECTOR"
    ROTATION = "ROTATION"
    COLOR = "RGBA"
    RGBA = "RGBA"


FloatInterfaceSubtypes = typing.Literal[
    "NONE",
    "PERCENTAGE",
    "FACTOR",
    "ANGLE",
    "TIME",
    "TIME_ABSOLUTE",
    "DISTANCE",
    "WAVELENGTH",
    "COLOR_TEMPERATURE",
    "FREQUENCY",
]
VectorInterfaceSubtypes = typing.Literal[
    "NONE",
    "PERCENTAGE",
    "FACTOR",
    "ANGLE",
    "TIME",
    "TIME_ABSOLUTE",
    "DISTANCE",
    "WAVELENGTH",
    "COLOR_TEMPERATURE",
    "FREQUENCY",
]

IntegerInterfaceSubtypes = typing.Literal["NONE", "PERCENTAGE", "FACTOR"]

StringInterfaceSubtypes = typing.Literal["NONE", "FILE_PATH"]


NodeMathItems = typing.Literal[
    "ADD",  # Add.A + B.
    "SUBTRACT",  # Subtract.A - B.
    "MULTIPLY",  # Multiply.A * B.
    "DIVIDE",  # Divide.A / B.
    "MULTIPLY_ADD",  # Multiply Add.A * B + C.
    "POWER",  # Power.A power B.
    "LOGARITHM",  # Logarithm.Logarithm A base B.
    "SQRT",  # Square Root.Square root of A.
    "INVERSE_SQRT",  # Inverse Square Root.1 / Square root of A.
    "ABSOLUTE",  # Absolute.Magnitude of A.
    "EXPONENT",  # Exponent.exp(A).
    "MINIMUM",  # Minimum.The minimum from A and B.
    "MAXIMUM",  # Maximum.The maximum from A and B.
    "LESS_THAN",  # Less Than.1 if A < B else 0.
    "GREATER_THAN",  # Greater Than.1 if A > B else 0.
    "SIGN",  # Sign.Returns the sign of A.
    "COMPARE",  # Compare.1 if (A == B) within tolerance C else 0.
    "SMOOTH_MIN",  # Smooth Minimum.The minimum from A and B with smoothing C.
    "SMOOTH_MAX",  # Smooth Maximum.The maximum from A and B with smoothing C.
    "ROUND",  # Round.Round A to the nearest integer. Round upward if the fraction part is 0.5.
    "FLOOR",  # Floor.The largest integer smaller than or equal A.
    "CEIL",  # Ceil.The smallest integer greater than or equal A.
    "TRUNC",  # Truncate.The integer part of A, removing fractional digits.
    "FRACT",  # Fraction.The fraction part of A.
    "MODULO",  # Truncated Modulo.The remainder of truncated division using fmod(A,B).
    "FLOORED_MODULO",  # Floored Modulo.The remainder of floored division.
    "WRAP",  # Wrap.Wrap value to range, wrap(A,B).
    "SNAP",  # Snap.Snap to increment, snap(A,B).
    "PINGPONG",  # Ping-Pong.Wraps a value and reverses every other cycle (A,B).
    "SINE",  # Sine.sin(A).
    "COSINE",  # Cosine.cos(A).
    "TANGENT",  # Tangent.tan(A).
    "ARCSINE",  # Arcsine.arcsin(A).
    "ARCCOSINE",  # Arccosine.arccos(A).
    "ARCTANGENT",  # Arctangent.arctan(A).
    "ARCTAN2",  # Arctan2.The signed angle arctan(A / B).
    "SINH",  # Hyperbolic Sine.sinh(A).
    "COSH",  # Hyperbolic Cosine.cosh(A).
    "TANH",  # Hyperbolic Tangent.tanh(A).
    "RADIANS",  # To Radians.Convert from degrees to radians.
    "DEGREES",  # To Degrees.Convert from radians to degrees.
]
NodeBooleanMathItems = typing.Literal[
    "AND",  # And.True when both inputs are true.
    "OR",  # Or.True when at least one input is true.
    "NOT",  # Not.Opposite of the input.
    "NAND",  # Not And.True when at least one input is false.
    "NOR",  # Nor.True when both inputs are false.
    "XNOR",  # Equal.True when both inputs are equal (exclusive nor).
    "XOR",  # Not Equal.True when both inputs are different (exclusive or).
    "IMPLY",  # Imply.True unless the first input is true and the second is false.
    "NIMPLY",  # Subtract.True when the first input is true and the second is false (not imply).
]
