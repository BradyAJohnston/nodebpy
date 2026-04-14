"""nodebpy.builder — node tree construction API.

Public names are re-exported here. Old names (NodeBuilder, SocketLinker,
SocketBase) are kept as aliases for backward compatibility.
"""

from ._utils import SocketError, denormalize_name, normalize_name
from .accessor import SocketAccessor
from .interface import (
    InterfaceSocket,
    SocketBoolean,
    SocketBundle,
    SocketClosure,
    SocketCollection,
    SocketColor,
    SocketFloat,
    SocketGeometry,
    SocketImage,
    SocketInt,
    SocketMaterial,
    SocketMatrix,
    SocketMenu,
    SocketObject,
    SocketRotation,
    SocketShader,
    SocketString,
    SocketVector,
)
from .mixins import LinkingMixin, OperatorMixin
from .node import BaseNode, DynamicInputsMixin, NodeGroupBuilder
from .socket import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    FloatSocket,
    GeometrySocket,
    ImageSocket,
    IntegerSocket,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    ShaderSocket,
    Socket,
    StringSocket,
    VectorSocket,
    _BooleanMixin,
    _ColorMixin,
    _IntegerMixin,
    _MatrixMixin,
    _RotationMixin,
    _VectorMixin,
)
from .tree import (
    InputInterfaceContext,
    MaterialBuilder,
    OutputInterfaceContext,
    PanelContext,
    SocketContext,
    TreeBuilder,
)

# Backward-compatible aliases for hand-written code that uses the old names.
NodeBuilder = BaseNode
SocketLinker = Socket
SocketBase = InterfaceSocket

__all__ = [
    # Core
    "TreeBuilder",
    "MaterialBuilder",
    "BaseNode",
    "Socket",
    "SocketAccessor",
    # Mixins
    "OperatorMixin",
    "LinkingMixin",
    "DynamicInputsMixin",
    # Node groups
    "NodeGroupBuilder",
    # Type-specific socket classes (runtime)
    "FloatSocket",
    "VectorSocket",
    "ColorSocket",
    "IntegerSocket",
    "BooleanSocket",
    "RotationSocket",
    "MatrixSocket",
    "StringSocket",
    "MenuSocket",
    "GeometrySocket",
    "ObjectSocket",
    "MaterialSocket",
    "ImageSocket",
    "CollectionSocket",
    "BundleSocket",
    "ClosureSocket",
    "ShaderSocket",
    # Type-specific behaviour mixins
    "_VectorMixin",
    "_ColorMixin",
    "_IntegerMixin",
    "_BooleanMixin",
    "_RotationMixin",
    "_MatrixMixin",
    # Interface socket base
    "InterfaceSocket",
    # Interface socket types
    "SocketFloat",
    "SocketInt",
    "SocketBoolean",
    "SocketVector",
    "SocketColor",
    "SocketRotation",
    "SocketMatrix",
    "SocketString",
    "SocketMenu",
    "SocketObject",
    "SocketGeometry",
    "SocketCollection",
    "SocketImage",
    "SocketMaterial",
    "SocketBundle",
    "SocketClosure",
    "SocketShader",
    # Tree context helpers
    "SocketContext",
    "PanelContext",
    "InputInterfaceContext",
    "OutputInterfaceContext",
    # Utilities
    "SocketError",
    "normalize_name",
    "denormalize_name",
    # Backward-compatible aliases
    "NodeBuilder",
    "SocketLinker",
    "SocketBase",
]
