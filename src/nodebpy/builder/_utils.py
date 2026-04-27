from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

import bpy
from bpy.types import NodeSocket


class SocketError(Exception):
    """Raised when a socket operation fails."""


# Type precedence for mixed-type operator dispatch (higher = dominant).
_TYPE_PRECEDENCE: dict[str, int] = {
    "INT": 0,
    "VALUE": 1,
    "FLOAT": 1,
    "VECTOR": 2,
}

GEO_NODE_NAMES = (
    f"GeometryNode{name}"
    for name in (
        "SetPosition",
        "TransformGeometry",
        "GroupInput",
        "GroupOutput",
        "MeshToPoints",
        "PointsToVertices",
    )
)


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'."""
    return name.lower().replace(" ", "_").replace("é", "e")


def denormalize_name(attr_name: str) -> str:
    """Convert 'geometry' or 'my_socket' to 'Geometry' or 'My Socket'."""
    return attr_name.replace("_", " ").title()


def _allow_innactive_sockets(node: bpy.types.Node) -> bool:
    """Returns True if we should allow inactive sockets to be linked for this node type"""
    return node.bl_idname in (
        "GeometryNodeIndexSwitch",
        "GeometryNodeMenuSwitch",
        "ShaderNodeMixShader",
        "GeometryNodeSwitch",
    )


def _resolve_promotion(
    self_socket: NodeSocket, other: Any, reverse: bool
) -> "tuple[NodeSocket, Any, bool]":
    """Determine the dominant socket for operator dispatch.

    When both operands have a socket type, the higher-precedence type wins.
    If `other` is dominant, the operands are swapped and `reverse` is flipped.

    Returns (dominant_socket, effective_other, effective_reverse).
    """
    other_type = getattr(other, "type", None)
    self_prec = _TYPE_PRECEDENCE.get(self_socket.type, 1)
    other_prec = _TYPE_PRECEDENCE.get(other_type, -1)  # type: ignore[arg-type]

    if other_prec > self_prec:
        # Other side is dominant — swap so the linker wraps the vector/higher socket
        if isinstance(other, NodeSocket):
            other_socket = other
        else:
            other_socket = other._default_output_socket
        return other_socket, self_socket, not reverse

    return self_socket, other, reverse


@runtime_checkable
class _NodeLike(Protocol):
    """Protocol for objects that wrap a Blender node and expose an ``outputs`` accessor."""

    outputs: Any  # SocketAccessor at runtime; typed as Any to avoid circular import


@runtime_checkable
class _SocketLike(Protocol):
    """Protocol for objects that wrap a single Blender NodeSocket and expose ``.socket``."""

    socket: NodeSocket
