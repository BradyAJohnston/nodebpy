"""Socket type definitions for node group interfaces.

These dataclasses define the properties for node group input/output sockets.
Each socket type provides full IDE autocomplete and type checking.

Socket classes are prefixed with 'Socket' to distinguish them from node classes.
For example: SocketVector (interface socket) vs Vector (input node).
"""

from .builder import (
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
    SocketString,
    SocketVector,
)

__all__ = [
    "SocketGeometry",
    "SocketBoolean",
    "SocketFloat",
    "SocketVector",
    "SocketInt",
    "SocketColor",
    "SocketRotation",
    "SocketMatrix",
    "SocketString",
    "SocketMenu",
    "SocketObject",
    "SocketCollection",
    "SocketImage",
    "SocketMaterial",
    "SocketBundle",
    "SocketClosure",
]
