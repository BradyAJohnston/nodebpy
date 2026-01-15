"""Socket type definitions for node group interfaces.

These dataclasses define the properties for node group input/output sockets.
Each socket type provides full IDE autocomplete and type checking.

Socket classes are prefixed with 'Socket' to distinguish them from node classes.
For example: SocketVector (interface socket) vs Vector (input node).
"""

from .builder import (
    SocketGeometry,
    SocketBoolean,
    SocketFloat,
    SocketVector,
    SocketInt,
    SocketColor,
    SocketRotation,
    SocketMatrix,
    SocketString,
    MenuSocket,
    SocketObject,
    SocketCollection,
    SocketImage,
    SocketMaterial,
    SocketBundle,
    SocketClosure,
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
    "MenuSocket",
    "SocketObject",
    "SocketCollection",
    "SocketImage",
    "SocketMaterial",
    "SocketBundle",
    "SocketClosure",
]
