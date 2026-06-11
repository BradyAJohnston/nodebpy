from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.types import Node, NodeSocket

from .node import DynamicInputsMixin
from .socket import Socket

if TYPE_CHECKING:
    from ..types import InputLinkable


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
        return sockets[item.name]

    def _add_socket(self, name: str, type: str) -> NodeSocket:
        return self._item_socket(self._new_item(name, type))

    def capture(self, value: InputLinkable, *, name: str | None = None) -> Socket:
        """Add an item linked from ``value`` and return its output socket.

        The item is auto-named after the source socket unless ``name`` is
        given.
        """
        if name is None:
            new_sockets = self._add_inputs(value)
        else:
            new_sockets = self._add_inputs(**{name: value})
        self._establish_links(**new_sockets)
        return Socket(self.node.outputs[next(iter(new_sockets))])
