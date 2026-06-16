"""Small string/value helpers shared across the generator."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.types import VectorFont

if TYPE_CHECKING:
    from .model import SocketInfo


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'.

    Handles numeric names by prefixing with 'input_' to make valid Python identifiers.
    """
    # Replace spaces, hyphens, and other non-alphanumeric characters with underscores
    normalized = name.lower()
    normalized = "".join(c if c.isalnum() else "_" for c in normalized)

    # Remove consecutive underscores and leading/trailing underscores
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")

    # If the name starts with a digit or is purely numeric, prefix it
    if normalized and (normalized[0].isdigit() or normalized.isdigit()):
        normalized = f"input_{normalized}"

    # If the name is empty or only underscores, provide a fallback
    if not normalized or normalized == "_":
        normalized = "input_socket"

    return normalized


def get_socket_param_name(socket: SocketInfo, use_identifier: bool = False) -> str:
    """Get the best parameter name for a socket, preferring label over name."""
    # Use label if available and non-empty, otherwise fallback to name
    # if sockets all use the same label name, we need to drop back to using the iden
    return normalize_name(socket.identifier)
    if use_identifier:
        return normalize_name(socket.identifier)
    else:
        display_name = socket.label if socket.label else socket.name
        return normalize_name(display_name)


def format_python_value(value: Any) -> str:
    """Format a Python value as a string for code generation."""
    if value is None:
        return "None"
    elif isinstance(value, str):
        return f'"{value}"' if value != "" else '""'
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, VectorFont):
        return "None"
    elif isinstance(value, float):
        return str(round(value, 4))
    elif hasattr(value, "__iter__") and not isinstance(value, str):
        try:
            return "({})".format(", ".join([round(x, 3) for x in value]))
        except (TypeError, AttributeError):
            return "None"
    else:
        try:
            return f'"{value}"'
        except Exception:
            return "None"
