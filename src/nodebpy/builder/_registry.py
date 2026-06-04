from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import NodeSocket

if TYPE_CHECKING:
    from .socket import Socket

_SOCKET_REGISTRY: dict[str, "type[Socket]"] = {}
_SOCKET_LIST_REGISTRY: dict[str, "type[Socket]"] = {}
_SOCKET_GRID_REGISTRY: dict[str, "type[Socket]"] = {}


def _wrap_socket(socket: NodeSocket) -> "Socket":
    for key, cls in _SOCKET_REGISTRY.items():
        if key in socket.bl_idname:
            structure = getattr(socket, "inferred_structure_type", "SINGLE")
            if structure == "LIST":
                return _SOCKET_LIST_REGISTRY.get(key, cls)(socket)
            elif structure == "GRID":
                return _SOCKET_GRID_REGISTRY.get(key, cls)(socket)
            return cls(socket)
    from .socket import Socket

    return Socket(socket)
