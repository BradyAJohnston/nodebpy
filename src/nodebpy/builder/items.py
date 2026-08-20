from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, cast

from bpy.types import ID, Node, NodeSocket
from mathutils import Euler

from ..types import _is_default_value
from ._registry import _wrap_socket
from ._utils import _SocketLike
from .node import DynamicInputsMixin
from .socket import Socket

if TYPE_CHECKING:
    from ..types import (
        InputAny,
        InputBoolean,
        InputBundle,
        InputClosure,
        InputCollection,
        InputColor,
        InputFloat,
        InputGeometry,
        InputImage,
        InputInteger,
        InputLinkable,
        InputMaterial,
        InputMatrix,
        InputMenu,
        InputObject,
        InputRotation,
        InputString,
        InputVector,
        _SocketShapeStructureType,
    )
    from .socket import (
        BooleanSocket,
        BundleSocket,
        ClosureSocket,
        CollectionSocket,
        ColorSocket,
        FloatSocket,
        GeometrySocket,
        ImageSocket,
        IntegerSocket,
        MaterialSocket,
        MatrixSocket,
        MenuSocket,
        ObjectSocket,
        RotationSocket,
        StringSocket,
        VectorSocket,
    )
    from .tree import TreeBuilder


def _socket_for_item(
    node: Node, items, prefix: str, item, *, output: bool = False
) -> NodeSocket:
    """Find the node socket belonging to ``item`` by identifier prefix and
    collection position; item names are not unique across a node's fixed
    sockets and item collections."""
    index = next(i for i, candidate in enumerate(items) if candidate == item)
    sockets = node.outputs if output else node.inputs
    return [s for s in sockets if s.identifier.startswith(prefix)][index]


def _apply_item_value(owner, socket: NodeSocket, value: Any) -> None:
    """Link ``value`` into ``socket`` (linkables) or set it as the socket
    default (plain values and datablocks); ``None`` leaves it untouched."""
    if value is None:
        return
    if _is_default_value(value) or isinstance(value, ID):
        socket.default_value = value  # ty: ignore[unresolved-attribute]
    else:
        owner.tree.link(owner._source_socket(value), socket)


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


_SocketT = TypeVar("_SocketT", bound=Socket, default=Socket)


class Item(Generic[_SocketT]):
    """Handle for one item of an items-driven node.

    Names the item's socket *roles* rather than socket plumbing: ``input``
    is the node's input socket for the item, ``output`` the matching
    output socket. The type parameter is the socket class both roles
    return; the untyped default is plain :class:`Socket`.

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
    def input(self) -> _SocketT:
        """The node's input socket for this item."""
        return cast("_SocketT", _wrap_socket(self._owner._item_socket(self._item)))

    @property
    def output(self) -> _SocketT:
        """The node's output socket for this item."""
        return cast(
            "_SocketT", _wrap_socket(self._owner._item_socket(self._item, output=True))
        )


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


_FieldT = TypeVar("_FieldT", bound=Socket, default=Socket)
_GridT = TypeVar("_GridT", bound=Socket, default=Socket)


class GridItem(Item[Socket], Generic[_FieldT, _GridT]):
    """Handle for a field→grid item whose two roles carry different socket
    classes: ``field`` is the node's field input socket, ``grid`` the
    matching grid output socket."""

    @property
    def field(self) -> _FieldT:
        """The node's field input socket for this item."""
        return cast("_FieldT", self.input)

    @property
    def grid(self) -> _GridT:
        """The node's grid output socket for this item."""
        return cast("_GridT", self.output)


class _TypedItemFactory:
    """Base for per-datatype typed item factories.

    Holds the owning builder object; subclasses implement ``_declare`` and
    expose one factory method per socket type so declarations carry static
    socket types.
    """

    def __init__(self, owner: Any):
        self._owner = owner


class _FieldItemFactory(_TypedItemFactory):
    """Typed factories for the seven field data types, returning two-role
    :class:`Item` handles. The default ``_declare`` targets an
    :class:`ItemsMixin` owner's :meth:`~ItemsMixin.add_item`."""

    _owner: ItemsMixin

    def _declare(self, name: str, value: InputAny, type: str) -> Item:
        return self._owner.add_item(name, value, type=type)

    def float(self, name: str = "Value", value: InputFloat = None) -> Item[FloatSocket]:
        return cast("Item[FloatSocket]", self._declare(name, value, "FLOAT"))

    def integer(
        self, name: str = "Integer", value: InputInteger = None
    ) -> Item[IntegerSocket]:
        return cast("Item[IntegerSocket]", self._declare(name, value, "INT"))

    def boolean(
        self, name: str = "Boolean", value: InputBoolean = None
    ) -> Item[BooleanSocket]:
        return cast("Item[BooleanSocket]", self._declare(name, value, "BOOLEAN"))

    def vector(
        self, name: str = "Vector", value: InputVector = None
    ) -> Item[VectorSocket]:
        return cast("Item[VectorSocket]", self._declare(name, value, "VECTOR"))

    def color(self, name: str = "Color", value: InputColor = None) -> Item[ColorSocket]:
        return cast("Item[ColorSocket]", self._declare(name, value, "RGBA"))

    def rotation(
        self, name: str = "Rotation", value: InputRotation = None
    ) -> Item[RotationSocket]:
        return cast("Item[RotationSocket]", self._declare(name, value, "ROTATION"))

    def matrix(
        self, name: str = "Matrix", value: InputMatrix = None
    ) -> Item[MatrixSocket]:
        return cast("Item[MatrixSocket]", self._declare(name, value, "MATRIX"))


class _SocketItemFactory(_TypedItemFactory):
    """Typed factories that declare one item per call and return the single
    node socket the item drives; subclasses implement ``_declare``."""

    def _declare(
        self, name: str, type: str, structure_type: _SocketShapeStructureType
    ) -> Socket:
        raise NotImplementedError

    def float(
        self,
        name: str = "Value",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> FloatSocket:
        return cast("FloatSocket", self._declare(name, "FLOAT", structure_type))

    def integer(
        self,
        name: str = "Integer",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> IntegerSocket:
        return cast("IntegerSocket", self._declare(name, "INT", structure_type))

    def boolean(
        self,
        name: str = "Boolean",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> BooleanSocket:
        return cast("BooleanSocket", self._declare(name, "BOOLEAN", structure_type))

    def vector(
        self,
        name: str = "Vector",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> VectorSocket:
        return cast("VectorSocket", self._declare(name, "VECTOR", structure_type))

    def color(
        self,
        name: str = "Color",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ColorSocket:
        return cast("ColorSocket", self._declare(name, "RGBA", structure_type))

    def rotation(
        self,
        name: str = "Rotation",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> RotationSocket:
        return cast("RotationSocket", self._declare(name, "ROTATION", structure_type))

    def matrix(
        self,
        name: str = "Matrix",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MatrixSocket:
        return cast("MatrixSocket", self._declare(name, "MATRIX", structure_type))

    def string(
        self,
        name: str = "String",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> StringSocket:
        return cast("StringSocket", self._declare(name, "STRING", structure_type))

    def menu(
        self,
        name: str = "Menu",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MenuSocket:
        return cast("MenuSocket", self._declare(name, "MENU", structure_type))

    def geometry(
        self,
        name: str = "Geometry",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> GeometrySocket:
        return cast("GeometrySocket", self._declare(name, "GEOMETRY", structure_type))

    def object(
        self,
        name: str = "Object",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ObjectSocket:
        return cast("ObjectSocket", self._declare(name, "OBJECT", structure_type))

    def image(
        self,
        name: str = "Image",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ImageSocket:
        return cast("ImageSocket", self._declare(name, "IMAGE", structure_type))

    def collection(
        self,
        name: str = "Collection",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> CollectionSocket:
        return cast(
            "CollectionSocket", self._declare(name, "COLLECTION", structure_type)
        )

    def material(
        self,
        name: str = "Material",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MaterialSocket:
        return cast("MaterialSocket", self._declare(name, "MATERIAL", structure_type))

    def bundle(
        self,
        name: str = "Bundle",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> BundleSocket:
        return cast("BundleSocket", self._declare(name, "BUNDLE", structure_type))

    def closure(
        self,
        name: str = "Closure",
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ClosureSocket:
        return cast("ClosureSocket", self._declare(name, "CLOSURE", structure_type))


class _SocketValueItemFactory(_TypedItemFactory):
    """Like :class:`_SocketItemFactory` but each declaration may take a
    ``value`` — a linkable linked into the new socket, or a plain default;
    subclasses implement ``_declare``."""

    def _declare(
        self,
        name: str,
        value: InputAny,
        type: str,
        structure_type: _SocketShapeStructureType,
    ) -> Socket:
        raise NotImplementedError

    def float(
        self,
        name: str = "Value",
        value: InputFloat = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> FloatSocket:
        return cast("FloatSocket", self._declare(name, value, "FLOAT", structure_type))

    def integer(
        self,
        name: str = "Integer",
        value: InputInteger = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> IntegerSocket:
        return cast("IntegerSocket", self._declare(name, value, "INT", structure_type))

    def boolean(
        self,
        name: str = "Boolean",
        value: InputBoolean = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> BooleanSocket:
        return cast(
            "BooleanSocket", self._declare(name, value, "BOOLEAN", structure_type)
        )

    def vector(
        self,
        name: str = "Vector",
        value: InputVector = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> VectorSocket:
        return cast(
            "VectorSocket", self._declare(name, value, "VECTOR", structure_type)
        )

    def color(
        self,
        name: str = "Color",
        value: InputColor = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ColorSocket:
        return cast("ColorSocket", self._declare(name, value, "RGBA", structure_type))

    def rotation(
        self,
        name: str = "Rotation",
        value: InputRotation = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> RotationSocket:
        return cast(
            "RotationSocket", self._declare(name, value, "ROTATION", structure_type)
        )

    def matrix(
        self,
        name: str = "Matrix",
        value: InputMatrix = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MatrixSocket:
        return cast(
            "MatrixSocket", self._declare(name, value, "MATRIX", structure_type)
        )

    def string(
        self,
        name: str = "String",
        value: InputString = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> StringSocket:
        return cast(
            "StringSocket", self._declare(name, value, "STRING", structure_type)
        )

    def menu(
        self,
        name: str = "Menu",
        value: InputMenu = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MenuSocket:
        return cast("MenuSocket", self._declare(name, value, "MENU", structure_type))

    def geometry(
        self,
        name: str = "Geometry",
        value: InputGeometry = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> GeometrySocket:
        return cast(
            "GeometrySocket", self._declare(name, value, "GEOMETRY", structure_type)
        )

    def object(
        self,
        name: str = "Object",
        value: InputObject = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ObjectSocket:
        return cast(
            "ObjectSocket", self._declare(name, value, "OBJECT", structure_type)
        )

    def image(
        self,
        name: str = "Image",
        value: InputImage = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ImageSocket:
        return cast("ImageSocket", self._declare(name, value, "IMAGE", structure_type))

    def collection(
        self,
        name: str = "Collection",
        value: InputCollection = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> CollectionSocket:
        return cast(
            "CollectionSocket", self._declare(name, value, "COLLECTION", structure_type)
        )

    def material(
        self,
        name: str = "Material",
        value: InputMaterial = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> MaterialSocket:
        return cast(
            "MaterialSocket", self._declare(name, value, "MATERIAL", structure_type)
        )

    def bundle(
        self,
        name: str = "Bundle",
        value: InputBundle = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> BundleSocket:
        return cast(
            "BundleSocket", self._declare(name, value, "BUNDLE", structure_type)
        )

    def closure(
        self,
        name: str = "Closure",
        value: InputClosure = None,
        *,
        structure_type: _SocketShapeStructureType = "AUTO",
    ) -> ClosureSocket:
        return cast(
            "ClosureSocket", self._declare(name, value, "CLOSURE", structure_type)
        )
