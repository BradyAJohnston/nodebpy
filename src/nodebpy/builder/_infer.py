"""Pick a multi-type node's data type from the values it is given.

Switch, Index Switch and Menu Switch need their type set before anything is
linked. Left at the default (Float), a node passed in links whichever of its
outputs converts to a float, so ``g.Switch(cond, g.Cube(), g.UVSphere())``
silently switches between the two UV Maps instead of the meshes.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, cast

from bpy.types import Node, NodeSocket

from ._utils import SocketError

# the data_type / input_type spelling of a socket type, where they differ
_DATA_TYPE = {"VALUE": "FLOAT"}


def _source_socket(value: Any) -> NodeSocket | None:
    """The socket ``value`` would link from, or ``None`` for a plain value."""
    if value is None or value is ...:
        return None
    if isinstance(value, NodeSocket):
        return value
    if isinstance(value, Node):
        return next((s for s in value.outputs if s.enabled), None)
    socket = getattr(value, "socket", None)
    if isinstance(socket, NodeSocket):
        return socket
    try:
        # nodes and item handles link from their default output
        default = getattr(value, "_default_output_socket", None)
    except (IndexError, ValueError, AttributeError):
        return None
    return default if isinstance(default, NodeSocket) else None


def _literal_type(value: Any) -> str | None:
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    if isinstance(value, str):
        return "STRING"
    if isinstance(value, (tuple, list)) and all(
        isinstance(v, (int, float)) for v in value
    ):
        return {3: "VECTOR", 4: "RGBA"}.get(len(value))
    return None


def _describe(socket: NodeSocket) -> str:
    return f"{getattr(socket.node, 'name', '?')}'s {socket.name}"


def infer_node_type(node: Node, prop: str, values: Iterable[Any]) -> str:
    """``prop``'s value for ``node`` switching between ``values``."""
    rna = cast(Any, node.bl_rna)
    allowed = [item.identifier for item in rna.properties[prop].enum_items]
    return infer_data_type(rna.name, values, allowed, keyword=prop)


def infer_data_type(
    node_name: str,
    values: Iterable[Any],
    allowed: Iterable[str],
    *,
    keyword: str,
    default: str = "FLOAT",
) -> str:
    """The data type for a node switching between ``values``.

    Sockets and nodes decide it: each links from one socket, and they must all
    agree. Plain Python values only decide when nothing is linked (``1`` and
    ``2.5`` together make a float). Raises :class:`SocketError` when the linked
    values disagree or have a type the node can't switch.
    """
    values = list(values)
    allowed = list(allowed)
    sources = [s for s in (_source_socket(v) for v in values) if s is not None]

    if sources:
        found: dict[str, list[str]] = {}
        for socket in sources:
            data_type = _DATA_TYPE.get(socket.type, socket.type)
            found.setdefault(data_type, []).append(_describe(socket))
        if len(found) > 1:
            listing = "; ".join(
                f"{data_type} from {', '.join(names)}"
                for data_type, names in found.items()
            )
            raise SocketError(
                f"Can't tell which type of {node_name} to build: the values are "
                f"{listing}. Use a typed variant (e.g. "
                f"{node_name.replace(' ', '')}.{_variant(next(iter(found)))}(...)) "
                f"or pass {keyword}=."
            )
        (data_type,) = found
    else:
        literals = {t for t in map(_literal_type, values) if t is not None}
        if literals <= {"INT", "FLOAT"} and len(literals) == 2:
            literals = {"FLOAT"}
        data_type = literals.pop() if len(literals) == 1 else default

    if data_type not in allowed:
        raise SocketError(
            f"{node_name} can't switch {data_type} values; it takes "
            f"{', '.join(allowed)}."
        )
    return data_type


def _variant(data_type: str) -> str:
    """The class-method name for a data type (``RGBA`` is ``color``)."""
    return {"RGBA": "color", "INT": "integer"}.get(data_type, data_type.lower())
