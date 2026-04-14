from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import NodeSocket

if TYPE_CHECKING:
    from .socket import Socket

_SOCKET_LINKER_REGISTRY: dict[str, "type[Socket]"] = {}


def _get_socket_linker(socket: NodeSocket) -> "Socket":
    for key, cls in _SOCKET_LINKER_REGISTRY.items():
        if key in socket.bl_idname:
            return cls(socket)
    from .socket import Socket

    return Socket(socket)
