from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import bpy
from bpy.types import NodeSocket

from ._registry import _get_socket_linker
from ._utils import SocketError, _allow_innactive_sockets, denormalize_name

if TYPE_CHECKING:
    from .socket import Socket


class SocketAccessor:
    """Unified accessor for a node's input or output socket collection.

    Supports identifier/name lookup, dict-style ``[]`` access, availability
    filtering, and type-compatible matching — replacing the former pairs of
    ``_input_idx``/``_output_idx``, ``_input``/``_output``,
    ``_available_inputs``/``_available_outputs``, and ``_best_output_socket``.
    """

    def __init__(
        self,
        collection: bpy.types.NodeInputs | bpy.types.NodeOutputs,
        direction: Literal["input", "output"],
    ):
        self._direction = direction
        self._collection = collection

    def _index(self, key: str | int) -> int:
        """Find socket index by identifier, falling back to name.

        Tries identifier match first. If no identifier matches, falls back to
        name lookup — but raises if the name is duplicated (ambiguous).
        Integer keys are returned directly.
        """
        if isinstance(key, int):
            return key
        ids = [s.identifier for s in self._collection]
        if key in ids:
            return ids.index(key)
        names = [s.name for s in self._collection]
        for key in (key, denormalize_name(key)):
            if key in names:
                if names.count(key) > 1:
                    raise RuntimeError(
                        f"{self._direction.title()} name '{key}' is ambiguous on "
                        f"{self._node.bl_idname} (appears {names.count(key)} times). "
                        f"Use the socket identifier instead."
                    )
                return names.index(key)
        raise RuntimeError(
            f"{self._direction.title()} '{key}' not found on "
            f"{self._node.bl_idname}. Available sockets (id: name): {list(zip(ids, names))}"
        )

    def _get(self, key: str | int) -> "Socket":
        """Get a Socket for a socket by identifier, name, or index."""
        return _get_socket_linker(self._collection[self._index(key)])

    def __getitem__(self, key: str | int) -> "Socket":
        """Access by identifier, name, or integer index."""
        return self._get(key)

    @property
    def _node(self) -> bpy.types.Node:
        """The node this accessor is associated with."""
        if isinstance(self._collection, list):
            return self._collection[0].node
        # bpy NodeInputs/NodeOutputs.id_data returns the NodeTree (top-level ID),
        # not the Node. Retrieve the node via the first socket instead.
        for s in self._collection:
            return s.node
        return self._collection.id_data  # empty collection fallback

    @property
    def _ignore_visibility(self) -> bool:
        """Whether to ignore socket visibility when selecting available sockets.

        Only affects ``available`` / ``best_match`` (the auto-linking heuristics).
        ``values()`` / ``items()`` always respect node-level visibility so that
        iteration over a node's sockets stays predictable regardless of context.
        Returns False when called outside a tree context (e.g. from a bare
        Socket that was created outside a ``with tree:`` block).
        """
        from .tree import TreeBuilder

        if not TreeBuilder._tree_contexts:
            return False
        return TreeBuilder._tree_contexts[-1].ignore_visibility

    def _visible_sockets(self) -> list[NodeSocket]:
        """Sockets that should appear in iteration (values/items/keys).

        Uses the per-node allowlist (``_allow_innactive_sockets``) rather than
        the tree-level ``ignore_visibility`` flag — enumeration should always
        reflect what is meaningfully present on the node, not the linking context.
        """
        if self._direction == "input":
            return [
                s
                for s in self._collection
                if _allow_innactive_sockets(self._node)
                or (not s.is_inactive and s.is_icon_visible)
            ]
        return [s for s in self._collection if s.is_icon_visible]

    @property
    def _available(self) -> list[NodeSocket]:
        """Sockets eligible for automatic linking.

        Respects ``ignore_visibility`` on the active ``TreeBuilder`` context, so
        nodes with normally-hidden sockets can still be auto-linked when that flag
        is set (e.g. during ``test_add_all_nodes``).
        """
        if self._direction == "input":
            return [
                s
                for s in self._collection
                if (
                    self._ignore_visibility or (not s.is_inactive and s.is_icon_visible)
                )
                and (not s.links or s.is_multi_input)
            ]
        return [
            s for s in self._collection if self._ignore_visibility or s.is_icon_visible
        ]

    def _best_match(self, socket_type: str) -> NodeSocket:
        """Find the best compatible socket for the given type."""
        from ..types import SOCKET_COMPATIBILITY

        compatible = SOCKET_COMPATIBILITY.get(socket_type, ())
        possible = [s for s in self._available if s.type in compatible]
        if possible:
            possible.sort(key=lambda x: compatible.index(x.type))
            return possible[0]
        raise SocketError(
            f"No compatible {self._direction} socket found for type "
            f"{socket_type} on {self._node.name}"
        )

    def _values(self) -> "list[Socket]":
        """All visible sockets as Sockets.

        Uses node-level visibility rules regardless of ``ignore_visibility`` —
        see ``_visible_sockets`` for rationale.
        """
        return [_get_socket_linker(s) for s in self._visible_sockets()]

    def _items(self) -> "list[tuple[str, Socket]]":
        """All visible sockets as (name, Socket) pairs.

        Uses node-level visibility rules regardless of ``ignore_visibility`` —
        see ``_visible_sockets`` for rationale.
        """
        return [(s.name, _get_socket_linker(s)) for s in self._visible_sockets()]

    def _keys(self) -> list[str]:
        """All visible socket names."""
        return [name for name, _ in self._items()]

    def __len__(self) -> int:
        return len(self._items())

    def __iter__(self):
        """Iterate over socket names (enables ``**node.outputs`` unpacking)."""
        return iter(self._keys())
