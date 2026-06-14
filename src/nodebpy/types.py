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
    NodeSocketIntVector3D,
    NodeSocketMaterial,
    NodeSocketMatrix,
    NodeSocketMenu,
    NodeSocketObject,
    NodeSocketRotation,
    NodeSocketShader,
    NodeSocketSound,
    NodeSocketString,
    NodeSocketVector,
    Object,
    Sound,
    VectorFont,
)
from mathutils import Euler

if typing.TYPE_CHECKING:
    from nodebpy.builder import (
        BooleanSocket,
        BooleanSocketGrid,
        BooleanSocketList,
        BundleSocket,
        BundleSocketList,
        ClosureSocket,
        ClosureSocketList,
        CollectionSocket,
        CollectionSocketList,
        ColorSocket,
        ColorSocketList,
        FloatSocket,
        FloatSocketGrid,
        FloatSocketList,
        FontSocket,
        FontSocketList,
        GeometrySocket,
        GeometrySocketList,
        ImageSocket,
        ImageSocketList,
        IntegerSocket,
        IntegerSocketGrid,
        IntegerSocketList,
        IntegerVectorSocket,
        MaterialSocket,
        MaterialSocketList,
        MatrixSocket,
        MatrixSocketList,
        MenuSocket,
        MenuSocketList,
        ObjectSocket,
        ObjectSocketList,
        RotationSocket,
        RotationSocketList,
        ShaderSocket,
        ShaderSocketList,
        SoundSocket,
        SoundSocketList,
        StringSocket,
        StringSocketList,
        VectorSocket,
        VectorSocketGrid,
        VectorSocketList,
    )

    from .builder import BaseNode as BaseNode
    from .builder import Socket as SocketLinker
    from .nodes.geometry.converter import CombineMatrix, CombineTransform


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
InputIntegerVector = typing.Union[
    list[int], NodeSocketIntVector3D, InputLinkable, "IntegerVectorSocket"
]

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
InputString = typing.Union[None, str, NodeSocketString, EllipsisType, "StringSocket"]
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
    NodeSocketMatrix,
    NodeSocketRotation,
    InputLinkable,
    "MatrixSocket",
    "CombineTransform",
    "CombineMatrix",
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
InputSound = typing.Union[NodeSocketSound, InputLinkable, "SoundSocket", Sound]

InputFloatGrid = typing.Union[NodeSocketFloat, "FloatSocketGrid", None]
InputVectorGrid = typing.Union[NodeSocketVector, "VectorSocketGrid", None]
InputIntegerGrid = typing.Union[NodeSocketInt, "IntegerSocketGrid", None]
InputBooleanGrid = typing.Union[NodeSocketBool, "BooleanSocketGrid", None]

InputGrid = typing.Union[
    InputFloatGrid,
    InputVectorGrid,
    InputIntegerGrid,
    InputBooleanGrid,
]

InputFloatList = typing.Union[NodeSocketFloat, "FloatSocketList", None]
InputVectorList = typing.Union[NodeSocketVector, "VectorSocketList", None]
InputColorList = typing.Union[NodeSocketColor, "ColorSocketList", None]
InputIntegerList = typing.Union[NodeSocketInt, "IntegerSocketList", None]
InputBooleanList = typing.Union[NodeSocketBool, "BooleanSocketList", None]
InputRotationList = typing.Union[NodeSocketRotation, "RotationSocketList", None]
InputMatrixList = typing.Union[NodeSocketMatrix, "MatrixSocketList", None]
InputStringList = typing.Union[NodeSocketString, "StringSocketList", None]
InputMenuList = typing.Union[NodeSocketMenu, "MenuSocketList", None]
InputObjectList = typing.Union[NodeSocketObject, "ObjectSocketList", None]
InputGeometryList = typing.Union[NodeSocketGeometry, "GeometrySocketList", None]
InputCollectionList = typing.Union[NodeSocketCollection, "CollectionSocketList", None]
InputImageList = typing.Union[NodeSocketImage, "ImageSocketList", None]
InputMaterialList = typing.Union[NodeSocketMaterial, "MaterialSocketList", None]
InputBundleList = typing.Union[NodeSocketBundle, "BundleSocketList", None]
InputClosureList = typing.Union[NodeSocketClosure, "ClosureSocketList", None]
InputShaderList = typing.Union[NodeSocketShader, "ShaderSocketList", None]
InputFontList = typing.Union[NodeSocketFont, "FontSocketList", None]
InputSoundList = typing.Union[NodeSocketSound, "SoundSocketList", None]

InputList = typing.Union[
    InputFloatList,
    InputVectorList,
    InputColorList,
    InputIntegerList,
    InputBooleanList,
    InputRotationList,
    InputMatrixList,
    InputStringList,
    InputMenuList,
    InputObjectList,
    InputGeometryList,
    InputCollectionList,
    InputImageList,
    InputMaterialList,
    InputBundleList,
    InputClosureList,
    InputShaderList,
    InputFontList,
    InputSoundList,
]

InputAny = typing.Union[
    InputFloat,
    InputInteger,
    InputString,
    InputColor,
    InputIntegerVector,
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
    InputSound,
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

_SocketShapeStructureType = Literal[
    "AUTO", "DYNAMIC", "FIELD", "GRID", "SINGLE", "LIST"
]


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
    "SOUND",
    # "INT_VECTOR",
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
    "INT_VECTOR": (
        "INT_VECTOR",
        "VECTOR",
        "VALUE",
        "INT",
        "BOOLEAN",
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
        "INT_VECTOR",
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
    "SOUND": ("SOUND",),
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
    "PIXEL",
    "PERCENTAGE",
    "FACTOR",
    "MASS",
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
    "PIXEL",
    "PERCENTAGE",
    "FACTOR",
    "TRANSLATION",
    "DIRECTION",
    "VELOCITY",
    "ACCELERATION",
    "EULER",
    "XYZ",
]

IntegerInterfaceSubtypes = typing.Literal["NONE", "PIXEL", "PERCENTAGE", "FACTOR"]

StringInterfaceSubtypes = typing.Literal["NONE", "FILE_PATH"]
