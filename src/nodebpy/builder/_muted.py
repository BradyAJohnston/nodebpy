"""Muted links: ``muted(source)`` feeds an input through a link that passes
nothing, so the input uses its own value, as a link muted in the editor
(Ctrl + click-drag across it) does."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from bpy.types import NodeSocket

from ._infer import _source_socket

if TYPE_CHECKING:
    from bpy.types import NodeLink


class Muted:
    """A link source whose link is muted; made by :func:`muted`."""

    def __init__(self, source: Any, value: Any = None):
        if isinstance(source, Muted):
            raise TypeError("muted() of a muted source")
        if _source_socket(source) is None:
            raise TypeError(
                f"muted() takes a node or socket to link from, not {source!r}"
            )
        self.source = source
        self.value = value

    @property
    def _default_output_socket(self) -> NodeSocket:
        socket = _source_socket(self.source)
        assert socket is not None
        return socket

    def __rshift__(self, other: Any) -> Any:
        with muting(self.value):
            return self.source >> other

    def __repr__(self) -> str:
        value = "" if self.value is None else f", value={self.value!r}"
        return f"muted({self.source!r}{value})"


def muted(source: Any, value: Any = None) -> Any:
    """Link ``source`` into an input through a muted link.

    A muted link stays in the tree but passes nothing, so the input uses its
    own value: ``value``, or the socket's default when ``value`` is ``None``.
    It works wherever a node or socket is passed as an input::

        g.JoinGeometry([muted(set_position), geo])
        g.SetPosition(geometry=geo, offset=muted(offset, value=(0, 0, 1)))
        muted(geo) >> g.SetPosition() >> tree.outputs.geometry("Geometry")

    ``source`` must be a node or socket: the muted link is the one from it.
    """
    return Muted(source, value)


# The links made while a muted source is being linked, innermost scope last.
# Class-level rather than per TreeBuilder: a node wraps its tree in a fresh
# TreeBuilder at times (``_from_node``), and the link must be caught anyway.
_scopes: list[list[NodeLink]] = []


def record(link: NodeLink) -> None:
    """Called by :meth:`TreeBuilder.link` for every link it makes."""
    if _scopes:
        _scopes[-1].append(link)


# Links to mute when their tree's builder exits, by tree. Muting at once
# would change the tree under the rest of the build: Blender reads a muted
# link's input as its own value, which can leave other inputs unused (a Mix
# factor at 0 makes B inactive, which TreeBuilder.link refuses to link into),
# and menu items don't propagate through a muted link.
_pending: dict[int, list[NodeLink]] = {}


@contextmanager
def muting(value: Any = None) -> Generator[None]:
    """Mute the links made inside the block (when their tree's builder
    exits), and give their inputs ``value``."""
    links: list[NodeLink] = []
    _scopes.append(links)
    try:
        yield
    finally:
        _scopes.pop()
    for link in links:
        tree = link.id_data
        assert tree is not None
        _pending.setdefault(tree.as_pointer(), []).append(link)
        if value is not None:
            _set_value(link, value)


def has_pending(tree: Any) -> bool:
    return tree.as_pointer() in _pending


def apply(tree: Any) -> None:
    """Mute the links :func:`muting` recorded for ``tree``."""
    for link in _pending.pop(tree.as_pointer(), ()):
        link.is_muted = True


def _set_value(link: NodeLink, value: Any) -> None:
    from .node import BaseNode

    to_node, to_socket = link.to_node, link.to_socket
    assert to_node is not None and to_socket is not None
    if not hasattr(to_socket, "default_value"):
        raise TypeError(f"'{to_socket.name}' has no value for muted(value=...)")
    BaseNode._from_node(to_node)._set_input_default_value(to_socket, value)
