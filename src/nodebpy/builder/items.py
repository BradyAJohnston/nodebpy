from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, cast

from bpy.types import Node, NodeSocket
from mathutils import Euler

from ..types import _is_default_value
from ._registry import _wrap_socket
from ._utils import _SocketLike
from .node import DynamicInputsMixin
from .socket import Socket

if TYPE_CHECKING:
    from ..types import InputLinkable
    from .tree import TreeBuilder


def _infer_value_type(value: Any) -> str | None:
    """Item ``socket_type`` for a plain default value, or None."""
    match value:
        case bool():
            return "BOOLEAN"
        case int():
            return "INT"
        case float():
            return "FLOAT"
        case str():
            return "STRING"
        case tuple() | list():
            return "VECTOR"
        case Euler():
            return "ROTATION"
        case _:
            return None


class Item:
    """Handle for one item of an items-driven node.

    Names the item's socket *roles* rather than socket plumbing: ``input``
    is the node's input socket for the item, ``output`` the matching
    output socket.

    Holds the item's collection index rather than the bpy item itself —
    bpy collection item references are invalidated when the collection
    grows.
    """

    def __init__(self, owner: ItemsMixin, item: Any):
        self._owner = owner
        self._index = next(
            i for i, candidate in enumerate(self._collection) if candidate == item
        )

    @property
    def _collection(self):
        return self._owner._items

    @property
    def _item(self):
        return self._collection[self._index]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, {self.socket_type!r})"

    @property
    def name(self) -> str:
        return self._item.name

    @property
    def socket_type(self) -> str:
        # some collections (capture_items, grid_items) call this data_type
        item = self._item
        return getattr(item, "socket_type", None) or item.data_type

    @property
    def input(self) -> Socket:
        """The node's input socket for this item."""
        return _wrap_socket(self._owner._item_socket(self._item))

    @property
    def output(self) -> Socket:
        """The node's output socket for this item."""
        return _wrap_socket(self._owner._item_socket(self._item, output=True))


class ItemsMixin(DynamicInputsMixin):
    """Socket machinery for nodes whose sockets are driven by a bpy item
    collection (``capture_items``, ``bake_items``, ``format_items``, ...).

    Subclasses declare class attributes instead of overriding methods:

    - ``_items_collection``: name of the collection on ``_items_node``
    - ``_socket_data_types``: socket types considered when inferring an
      item's type from a source socket
    - ``_type_map``: socket type -> item ``socket_type`` renames
      (e.g. ``VALUE`` -> ``FLOAT``)

    Must come *before* ``BaseNode`` in the bases so that
    ``_find_best_socket_pair`` (the ``>>``-implicit-add behaviour) takes
    precedence over ``LinkingMixin``'s.
    """

    _items_collection: str

    if TYPE_CHECKING:
        node: Node
        tree: TreeBuilder

        def _establish_links(self, **kwargs: Any) -> None: ...

    @property
    def _items_node(self) -> Node:
        """Node owning the items collection.

        Zone input nodes override this to return ``paired_output``, where
        the shared collection lives.
        """
        return self.node

    @property
    def _items(self):
        return getattr(self._items_node, self._items_collection)

    def _new_item(self, name: str, type: str):
        """Create a new collection item.

        Override to adapt collections whose ``.new()`` signature differs
        from ``(socket_type, name)``.
        """
        return self._items.new(socket_type=type, name=name)

    def _item_socket(self, item, *, output: bool = False) -> NodeSocket:
        """The node socket belonging to ``item``."""
        sockets = self.node.outputs if output else self.node.inputs
        matches = [s for s in sockets if s.name == item.name]
        if len(matches) == 1:
            return matches[0]
        # Name collides — e.g. a capture item named "Selection" alongside the
        # built-in CaptureAttribute "Selection" socket. Item sockets are the
        # trailing N sockets (one per collection item), so resolve by the
        # item's position in the collection instead.
        items = list(self._items)
        idx = next(i for i, it in enumerate(items) if it == item)
        real = [s for s in sockets if not s.identifier.startswith("__extend__")]
        return real[len(real) - len(items) + idx]

    def _add_socket(self, name: str, type: str) -> NodeSocket:
        return self._item_socket(self._new_item(name, type))

    def _resolve_capture(
        self,
        value: InputLinkable,
        *,
        name: str | None,
        types: tuple[str, ...] | None = None,
    ) -> tuple[NodeSocket, str, str]:
        """Resolve the source socket, item type and item name for a capture."""
        accessor = getattr(value, "o", None)
        sources = (
            [cast("NodeSocket", value)] if accessor is None else accessor._available
        )
        socket_source, type = self._match_compatible_data(sources, types)
        if type in self._type_map:
            type = self._type_map[type]
        if name is None:
            default_socket = getattr(value, "_default_output_socket", None)
            name = socket_source.name if default_socket is None else default_socket.name
        if isinstance(socket_source, _SocketLike):
            socket_source = socket_source.socket
        return socket_source, type, name

    def _declared_item_type(self, value: Any) -> str | None:
        """The item ``socket_type`` if ``value`` is a socket-type string
        (e.g. ``"FLOAT"``) valid for this node, else ``None``."""
        if not isinstance(value, str):
            return None
        if value in self._socket_data_types:
            return self._type_map.get(value, value)
        if value in {self._type_map.get(t, t) for t in self._socket_data_types}:
            return value
        return None

    def _add_unlinked_input(self, name: str, value: Any) -> bool:
        """Items may also be declared with a plain default value
        (``items={"label": "hello"}``) — the item type is inferred from
        the Python type and the value becomes the socket default."""
        if super()._add_unlinked_input(name, value):
            return True
        type = _infer_value_type(value)
        if type is None:
            return False
        socket = self._add_socket(
            name=name, type=self._declared_item_type(type) or type
        )
        socket.default_value = value  # ty: ignore[unresolved-attribute]
        return True

    def capture(self, value: InputLinkable, *, name: str | None = None) -> Socket:
        """Add an item linked from ``value`` and return its output socket.

        The item is auto-named after the source socket unless ``name`` is
        given.
        """
        source, type, name = self._resolve_capture(value, name=name)
        item = self._new_item(name, type)
        self.tree.link(source, self._item_socket(item))
        return _wrap_socket(self._item_socket(item, output=True))

    def add_item(
        self, name: str, value: Any = None, *, type: str | None = None
    ) -> Item:
        """Add a single item and return its handle.

        ``value`` may be a linkable (linked to the item's input) or a plain
        default value; otherwise ``type`` (a socket-type string such as
        ``"FLOAT"``) declares the item unlinked.
        """
        if value is not None and not _is_default_value(value):
            source, inferred, _ = self._resolve_capture(value, name=name)
            item = self._new_item(name, type or inferred)
            self.tree.link(source, self._item_socket(item))
            return Item(self, item)
        if type is None:
            type = _infer_value_type(value)
        if type is None:
            raise TypeError(f"item {name!r} requires a value or an explicit type=")
        item = self._new_item(name, self._declared_item_type(type) or type)
        if value is not None:
            self._item_socket(item).default_value = value  # ty: ignore[unresolved-attribute]
        return Item(self, item)

    def add_items(self, items: Mapping[str, InputLinkable | str]) -> dict[str, Item]:
        """Add an item per mapping entry and return their handles by name.

        Values may be linkables (linked to the new item's input) or
        socket-type strings such as ``"FLOAT"`` (declare an unlinked item).
        """
        handles = {}
        for key, value in items.items():
            type = self._declared_item_type(value)
            if type is not None:
                handles[key] = self.add_item(key, type=type)
            else:
                handles[key] = self.add_item(key, cast("InputLinkable", value))
        return handles
