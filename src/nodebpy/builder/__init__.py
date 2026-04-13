"""nodebpy.builder — node tree construction API.

Public names are re-exported here. Old names (NodeBuilder, SocketLinker,
SocketBase) are kept as aliases for backward compatibility.
"""

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
    ColorSocket,
    IntegerSocket,
    Socket,
    VectorSocket,
    _ColorMixin,
    _IntegerMixin,
    _VectorMixin,
)
from .tree import (
    InputInterfaceContext,
    OutputInterfaceContext,
    PanelContext,
    SocketContext,
    TreeBuilder,
)
from ._utils import SocketError, denormalize_name, normalize_name

# Backward-compatible aliases for hand-written code that uses the old names.
NodeBuilder = BaseNode
SocketLinker = Socket
SocketBase = InterfaceSocket

__all__ = [
    # Core
    "TreeBuilder",
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
    "VectorSocket",
    "ColorSocket",
    "IntegerSocket",
    # Type-specific behaviour mixins
    "_VectorMixin",
    "_ColorMixin",
    "_IntegerMixin",
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
