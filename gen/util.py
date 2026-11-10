"""Small string/value helpers shared across the generator."""

from __future__ import annotations

import unicodedata
from typing import TYPE_CHECKING, Any

from bpy.types import VectorFont

from .config import _load_standalone

# Shared with ``to_python`` export so generated defaults and exported literals
# spell a float32 the same way (``0.1``, ``3 * math.pi / 4``); loaded from the
# file so the generator never imports the package it generates.
_floats = _load_standalone("_nodebpy_floats", "src/nodebpy/export/_floats.py")


def fmt_float(value: float) -> str:
    """The literal that rebuilds exactly this float32 socket default."""
    return _floats.fmt_float(value, snap=False)


if TYPE_CHECKING:
    from .model import SocketInfo


# Sockets Blender declares available only in its GPU shader trees, read from
# the generated socket-order table the same way.
INTERNAL_SOCKETS = _load_standalone(
    "_nodebpy_socket_order", "src/nodebpy/builder/_socket_order.py"
).INTERNAL_SOCKETS


def former_name(identifier: str, name: str) -> str | None:
    """The name a socket was labelled before, or ``None``.

    Blender keeps a socket's identifier when it relabels it, so an identifier
    that differs from the label is the old label (Import PLY's ``Mesh``
    output is labelled "Geometry" since 5.3), unless it is numbered
    (``Value_001``), generated (``Socket_3``) or a per-type variant of the
    label (Mix's ``A_Color``).
    """
    old, new = normalize_name(identifier), normalize_name(name)
    if old == new or old.startswith(f"{new}_") or "__" in identifier:
        return None
    if old.rsplit("_", 1)[-1].isdigit() or old[-3:].isdigit():
        return None
    return identifier


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'.

    Handles numeric names by prefixing with 'input_' to make valid Python identifiers.
    """
    # Fold accented letters to their ASCII base ('Bézier' → 'bezier') so
    # generated method names stay plain-ASCII identifiers.
    normalized = "".join(
        c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c)
    )
    # Replace spaces, hyphens, and other non-alphanumeric characters with underscores
    normalized = normalized.lower()
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
    elif isinstance(value, (bool, int)):
        return str(value)
    elif isinstance(value, VectorFont):
        return "None"
    elif isinstance(value, float):
        return fmt_float(value)
    elif hasattr(value, "__iter__") and not isinstance(value, str):
        try:
            return "({})".format(", ".join(format_python_value(x) for x in value))
        except (TypeError, AttributeError):
            return "None"
    else:
        try:
            return f'"{value}"'
        except Exception:  # noqa: BLE001
            return "None"
