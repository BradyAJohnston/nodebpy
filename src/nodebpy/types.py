from __future__ import annotations

import enum
import typing
from dataclasses import dataclass
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
    from .builder import (
        BaseNode,
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
    from .builder import Socket as SocketLinker
    from .nodes.geometry.converter import CombineMatrix, CombineTransform


def _is_default_value(value: InputAny):
    return isinstance(value, (int, float, str, bool, tuple, list, Euler))


class Default(enum.Enum):
    """What an unconnected input reads instead of a stored value.

    Blender lets a group input (and a few built-in inputs, such as Set
    Position's *Position*) fall back to an implicit field or context value when
    nothing is linked to it: the socket shows no value in the UI and its stored
    ``default_value`` is ignored. The members mirror the ``default_input``
    identifiers of ``bpy.types.NodeTreeInterfaceSocket``.

    A generated asset class spells such a parameter as, for example,
    ``position: InputVector = Default.POSITION``, so the fallback shows in the
    signature and the docs. Passing a member to a node constructor leaves the
    socket untouched — it does not add a link — exactly like ``None``. The
    same members are accepted by the ``default_input=`` argument of the
    ``tree.inputs.*`` socket factories, and :meth:`attribute` names the
    attribute a group input reads when unconnected (``default_attribute=``).
    """

    INDEX = "INDEX"
    ID_OR_INDEX = "ID_OR_INDEX"
    NORMAL = "NORMAL"
    POSITION = "POSITION"
    INSTANCE_TRANSFORM = "INSTANCE_TRANSFORM"
    HANDLE_LEFT = "HANDLE_LEFT"
    HANDLE_RIGHT = "HANDLE_RIGHT"
    SCENE_FRAME = "SCENE_FRAME"
    UNIFORM_IMAGE_COORDINATES = "UNIFORM_IMAGE_COORDINATES"
    SELF_OBJECT = "SELF_OBJECT"

    @staticmethod
    def attribute(name: str) -> DefaultAttribute:
        """The fallback that reads the named attribute of the geometry."""
        return DefaultAttribute(name)

    @property
    def description(self) -> str:
        """A phrase for docstrings: what the input reads when unconnected."""
        return _DEFAULT_DESCRIPTIONS[self]

    def __repr__(self) -> str:
        return f"Default.{self.name}"

    __str__ = __repr__


_DEFAULT_DESCRIPTIONS: dict[Default, str] = {
    Default.INDEX: "the index field",
    Default.ID_OR_INDEX: "the ID field, or the index when there is no ID",
    Default.NORMAL: "the normal field",
    Default.POSITION: "the position field",
    Default.INSTANCE_TRANSFORM: "the instance transform field",
    Default.HANDLE_LEFT: "the left handle position field",
    Default.HANDLE_RIGHT: "the right handle position field",
    Default.SCENE_FRAME: "the current scene frame",
    Default.UNIFORM_IMAGE_COORDINATES: "uniform image coordinates",
    Default.SELF_OBJECT: "the object the modifier is on",
}


@dataclass(frozen=True, slots=True)
class DefaultAttribute:
    """The fallback of an input that reads a named attribute when unconnected.

    Create one with :meth:`Default.attribute`; it prints as
    ``Default.attribute("UVMap")`` so it reads the same in a generated
    signature as in source.
    """

    name: str

    @property
    def description(self) -> str:
        return f'the "{self.name}" attribute'

    def __repr__(self) -> str:
        return f"Default.attribute({self.name!r})"

    __str__ = __repr__


# Type aliases for node inputs using typing.Union for runtime compatibility
InputLinkable = typing.Union[
    "BaseNode",
    "SocketLinker",
    NodeSocket,
    None,
    EllipsisType,
    Default,
    DefaultAttribute,
]

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
    tuple[int, int],
    tuple[int, int, int],
    list[int],
    NodeSocketIntVector3D,
    InputLinkable,
    "IntegerVectorSocket",
]

InputBoolean = typing.Union[bool, NodeSocketBool, InputLinkable, "BooleanSocket"]
InputVector = typing.Union[
    tuple[float, float],
    tuple[float, float, float],
    tuple[float, float, float, float],
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

InputGrid = InputFloatGrid | InputVectorGrid | InputIntegerGrid | InputBooleanGrid

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

InputList = (
    InputFloatList
    | InputVectorList
    | InputColorList
    | InputIntegerList
    | InputBooleanList
    | InputRotationList
    | InputMatrixList
    | InputStringList
    | InputMenuList
    | InputObjectList
    | InputGeometryList
    | InputCollectionList
    | InputImageList
    | InputMaterialList
    | InputBundleList
    | InputClosureList
    | InputShaderList
    | InputFontList
    | InputSoundList
)

InputAny = (
    InputFloat
    | InputInteger
    | InputString
    | InputColor
    | InputIntegerVector
    | InputGeometry
    | InputObject
    | InputMaterial
    | InputImage
    | InputCollection
    | InputMatrix
    | InputVector
    | InputBoolean
    | InputMenu
    | InputRotation
    | InputFont
    | InputBundle
    | InputClosure
    | InputShader
    | InputSound
)

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
    "FONT": ("FONT",),
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
