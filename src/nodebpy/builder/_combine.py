"""Feed a vector, rotation or color input from a tuple that holds sockets.

``g.Cube(size=(1, 1, height))`` can't store ``height`` in the socket's
default, since it is only known when the tree runs, so the tuple is built into
a Combine XYZ (or Combine Color) node whose output is linked in instead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.types import NodeSocket

from ._infer import _source_socket
from ._utils import SocketError

if TYPE_CHECKING:
    from .tree import TreeBuilder


def _show(values: list[Any]) -> str:
    """The tuple as written, with sockets named by their node."""
    parts = []
    for v in values:
        socket = _source_socket(v)
        node = getattr(socket, "node", None)
        parts.append(f"{node.name}'s {socket.name}" if socket and node else repr(v))
    return f"({', '.join(parts)})"


def holds_sockets(value: Any) -> bool:
    """Whether ``value`` is a tuple or list with a socket or node in it."""
    return isinstance(value, (tuple, list)) and any(
        _source_socket(v) is not None for v in value
    )


def link_combined(tree: TreeBuilder[Any], socket: NodeSocket, value: Any) -> None:
    """Link a Combine XYZ / Combine Color built from ``value`` into ``socket``."""
    from ..nodes import compositor, geometry, shader

    nodes: Any = {"ShaderNodeTree": shader, "CompositorNodeTree": compositor}.get(
        tree.tree.bl_idname, geometry
    )
    values = list(value)
    if socket.type in ("VECTOR", "ROTATION"):
        # a 2D vector socket takes (x, y); an Euler rotation is converted
        size = len(getattr(socket, "default_value", ())) or 3
        if socket.type == "ROTATION" or size not in (2, 3):
            size = 3
        if len(values) != size:
            raise SocketError(
                f"'{socket.name}' takes {size} components, not {len(values)}: "
                f"{_show(values)}."
            )
        combined = nodes.CombineXYZ(*values)
    elif socket.type == "RGBA":
        if len(values) not in (3, 4):
            raise SocketError(
                f"'{socket.name}' takes a color of 3 or 4 components, not "
                f"{len(values)}: {_show(values)}."
            )
        red, green, blue, *alpha = values
        kwargs: dict[str, Any] = {"red": red, "green": green, "blue": blue}
        if alpha and "alpha" in nodes.CombineColor.__init__.__code__.co_varnames:
            kwargs["alpha"] = alpha[0]
        elif alpha and not (isinstance(alpha[0], (int, float)) and alpha[0] == 1):
            # shader colors carry no alpha through links (and ``==`` on a
            # socket would build a Compare node rather than test it)
            raise SocketError(
                f"Shader colors have no alpha to set from {_show(alpha)[1:-1]}; "
                f"pass (red, green, blue) to '{socket.name}'."
            )
        combined = nodes.CombineColor(**kwargs)
    else:
        raise SocketError(
            f"'{socket.name}' is a {socket.type} input, which a tuple of sockets "
            "can't feed."
        )
    tree.link(combined._default_output_socket, socket)
