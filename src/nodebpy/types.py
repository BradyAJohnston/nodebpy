from __future__ import annotations

import typing
from types import EllipsisType
from typing import Literal

from bpy.types import (
    Collection,
    Image,
    Material,
    NodeSocket,
    NodeSocketBool,
    NodeSocketBundle,
    NodeSocketClosure,
    NodeSocketCollection,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketFont,
    NodeSocketGeometry,
    NodeSocketImage,
    NodeSocketInt,
    NodeSocketMaterial,
    NodeSocketMatrix,
    NodeSocketMenu,
    NodeSocketObject,
    NodeSocketRotation,
    NodeSocketShader,
    NodeSocketString,
    NodeSocketVector,
    Object,
    VectorFont,
)
from mathutils import Euler

if typing.TYPE_CHECKING:
    from nodebpy.builder import (
        BooleanSocket,
        BundleSocket,
        ClosureSocket,
        CollectionSocket,
        ColorSocket,
        FloatSocket,
        FontSocket,
        GeometrySocket,
        ImageSocket,
        IntegerSocket,
        MaterialSocket,
        MatrixSocket,
        MenuSocket,
        ObjectSocket,
        RotationSocket,
        ShaderSocket,
        StringSocket,
        VectorSocket,
    )

    from .builder import BaseNode as BaseNode
    from .builder import Socket as SocketLinker


def _is_default_value(value: InputAny):
    return isinstance(value, (int, float, str, bool, tuple, list, Euler))


# Type aliases for node inputs using typing.Union for runtime compatibility
InputLinkable = typing.Union["BaseNode", "SocketLinker", NodeSocket, None, EllipsisType]

InputFloat = typing.Union[
    float,
    int,
    NodeSocketFloat,
    NodeSocketInt,
    NodeSocketVector,
    InputLinkable,
    "FloatSocket",
]
InputInteger = typing.Union[int, NodeSocketInt, InputLinkable, "IntegerSocket"]
InputBoolean = typing.Union[bool, NodeSocketBool, InputLinkable, "BooleanSocket"]
InputVector = typing.Union[
    tuple[float, float, float],
    float,
    int,
    bool,
    Euler,
    NodeSocketFloat,
    NodeSocketVector,
    NodeSocketInt,
    InputLinkable,
    "VectorSocket",
]
InputRotation = typing.Union[
    tuple[float, float, float], float, int, Euler, InputLinkable, "RotationSocket"
]
InputColor = typing.Union[
    tuple[float, float, float, float],
    NodeSocketColor,
    NodeSocketVector,
    float,
    int,
    InputLinkable,
    "ColorSocket",
]
InputString = typing.Union[str, NodeSocketString, InputLinkable, "StringSocket"]
InputGeometry = typing.Union[NodeSocketGeometry, InputLinkable, "GeometrySocket"]
InputObject = typing.Union[NodeSocketObject, Object, InputLinkable, "ObjectSocket"]
InputMaterial = typing.Union[
    NodeSocketMaterial, Material, InputLinkable, "MaterialSocket"
]
InputImage = typing.Union[NodeSocketImage, Image, InputLinkable, "ImageSocket"]
InputCollection = typing.Union[
    Collection, NodeSocketCollection, InputLinkable, "CollectionSocket"
]
InputMatrix = typing.Union[
    NodeSocketMatrix, NodeSocketRotation, InputLinkable, "MatrixSocket"
]
InputMenu = typing.Union[str, NodeSocketMenu, InputLinkable, "MenuSocket"]
InputBundle = typing.Union[NodeSocketBundle, InputLinkable, "BundleSocket"]
InputClosure = typing.Union[NodeSocketClosure, InputLinkable, "ClosureSocket"]
InputShader = typing.Union[
    NodeSocketShader,
    NodeSocketColor,
    NodeSocketVector,
    NodeSocketFloat,
    InputLinkable,
    "ShaderSocket",
]
InputFont = typing.Union[NodeSocketFont, InputLinkable, VectorFont, "FontSocket"]


InputGrid = typing.Union[
    NodeSocketFloat,
    NodeSocketInt,
    NodeSocketVector,
    NodeSocketBool,
    InputLinkable,
    "FloatSocket",
    "IntegerSocket",
    "VectorSocket",
    "BooleanSocket",
]

InputAny = typing.Union[
    InputFloat,
    InputInteger,
    InputString,
    InputColor,
    InputGeometry,
    InputObject,
    InputMaterial,
    InputImage,
    InputCollection,
    InputMatrix,
    InputVector,
    InputBoolean,
    InputMenu,
    InputRotation,
    InputFont,
    InputBundle,
    InputClosure,
    InputShader,
]

_AccumulateFieldDataTypes = Literal["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"]

_AttributeDomains = typing.Literal[
    "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
]

# Runtime tuple used for isinstance-style membership checks; _BakeDataTypes is the
# matching Literal for static type annotations.
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

_GridDataTypes = Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]

_EvaluateAtIndexDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR", "FLOAT_COLOR", "QUATERNION", "FLOAT4X4"
]

_AttributeDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX"
]

_SocketShapeStructureType = Literal["AUTO", "DYNAMIC", "FIELD", "GRID", "SINGLE"]


SOCKET_TYPES = Literal[
    # "VALUE",
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
    "SHADER",
    "FONT",
    # "CUSTOM",
]

SOCKET_COMPATIBILITY: dict[str, tuple[str, ...]] = {
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
    "RGBA": ("RGBA", "VECTOR", "VALUE", "INT", "BOOLEAN"),
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
    "SHADER": ("SHADER", "RGBA"),
}

# Type pairs (output, input) where the first available input socket should be
# preferred over a later socket with a closer type match. Covers the common
# float ↔ color ↔ vector implicit conversions in compositor / shader nodes.
# Intentionally excludes low-semantic-overlap pairs like VALUE→BOOLEAN or
# VECTOR→ROTATION, which should still fall through to best-match logic.
PREFER_FIRST_SOCKET: frozenset[tuple[str, str]] = frozenset(
    {
        ("VALUE", "RGBA"),
        ("RGBA", "VALUE"),
        ("VECTOR", "RGBA"),
        ("RGBA", "VECTOR"),
        ("VALUE", "SHADER"),
        ("VECTOR", "SHADER"),
        ("RGBA", "SHADER"),
    }
)


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
VectorInterfaceSubtypes = FloatInterfaceSubtypes

IntegerInterfaceSubtypes = typing.Literal["NONE", "PERCENTAGE", "FACTOR"]

StringInterfaceSubtypes = typing.Literal["NONE", "FILE_PATH"]
