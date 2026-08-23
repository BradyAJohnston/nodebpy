"""Hand-written mixins attached to auto-generated node classes.

These hold reusable behaviour that the code generator cannot derive on its own
(ergonomic flag accessors, items helpers, …). The ``gen`` package wires them
onto the generated classes via :class:`~gen.NodeCustomization`, so the bulky
boilerplate (sockets, docstrings, property accessors) stays generated while the
bespoke behaviour lives here.
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, cast

import bpy
from mathutils import Euler

from ..builder import (
    BooleanSocketList,
    ColorSocketList,
    FloatSocketList,
    IntegerSocketList,
    ItemsMixin,
    MatrixSocketList,
    MenuSocketList,
    RotationSocketList,
    SocketAccessor,
    StringSocketList,
    VectorSocketList,
)
from ..builder import BaseNode
from ..builder import Socket as SocketLinker
from ..builder._registry import _wrap_socket
from ..builder.items import (
    Item,
    _apply_item_value,
    _FieldItemFactory,
    _infer_value_type,
    _socket_for_item,
    _SocketItemFactory,
    _SocketValueItemFactory,
)
from ..types import (
    InputAny,
    InputBoolean,
    InputBundle,
    InputColor,
    InputFloat,
    InputGeometry,
    InputInteger,
    InputLinkable,
    InputMatrix,
    InputRotation,
    InputString,
    InputVector,
    _BakedDataTypeValues,
    _SocketShapeStructureType,
)

if TYPE_CHECKING:
    from ..builder import BundleSocket, GeometrySocket, StringSocket
    from ..builder.tree import TreeBuilder


class _BakeItems(_FieldItemFactory):
    """Typed item factories for the Bake node — the field types plus the
    geometry-ish types bake items additionally support."""

    _owner: "_BakeMixin"

    def string(
        self, name: str = "String", value: InputString = None
    ) -> Item[StringSocket]:
        return cast("Item[StringSocket]", self._declare(name, value, "STRING"))

    def geometry(
        self, name: str = "Geometry", value: InputGeometry = None
    ) -> Item[GeometrySocket]:
        return cast("Item[GeometrySocket]", self._declare(name, value, "GEOMETRY"))

    def bundle(
        self, name: str = "Bundle", value: InputBundle = None
    ) -> Item[BundleSocket]:
        return cast("Item[BundleSocket]", self._declare(name, value, "BUNDLE"))


class _BakeMixin(ItemsMixin):
    """Variadic items constructor for the Bake node. Items may be passed
    positionally (``*args``), as a ``name -> value`` mapping, or as keyword
    arguments; all are funnelled through :meth:`ItemsMixin._add_inputs`."""

    _items_collection = "bake_items"
    _socket_data_types = _BakedDataTypeValues

    def __init__(
        self, *args, items: dict[str, InputLinkable | str] | None = None, **kwargs
    ):
        super().__init__()
        key_args = dict(items or {})
        key_args.update(kwargs)
        self._establish_links(**self._add_inputs(*args, **key_args))

    @property
    def items(self) -> _BakeItems:
        """Typed item factories — declare bake items with static types."""
        return _BakeItems(self)


class _CombineBundleItems(_SocketValueItemFactory):
    """Typed factories for Combine Bundle items; each declares one bundle
    item and returns its typed input socket, linked from ``value`` when one
    is given."""

    _owner: "_CombineBundleMixin"

    def _declare(
        self,
        name: str,
        value: InputAny,
        type: str,
        structure_type: _SocketShapeStructureType,
    ) -> SocketLinker:
        node = self._owner.node
        item = node.bundle_items.new(type, name)  # ty: ignore[invalid-argument-type]
        if structure_type != "AUTO":
            item.structure_type = structure_type
        socket = _socket_for_item(node, node.bundle_items, "Item_", item)
        _apply_item_value(self._owner, socket, value)
        return _wrap_socket(socket)


class _CombineBundleMixin:
    """Items constructor + typed item factories for the Combine Bundle
    node, whose inputs are all dynamic bundle items."""

    if TYPE_CHECKING:
        node: bpy.types.NodeCombineBundle
        tree: TreeBuilder

        def _source_socket(self, node) -> bpy.types.NodeSocket: ...

    def __init__(
        self,
        items: dict[str, InputAny] | None = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        for name, value in (items or {}).items():
            self._add_bundle_item(name, value)
        self.node.define_signature = define_signature

    @property
    def items(self) -> _CombineBundleItems:
        """Typed item factories — declare bundle items with static types."""
        return _CombineBundleItems(self)

    def _add_bundle_item(self, name: str, value: InputAny) -> None:
        """Add a named bundle item from a value of any supported kind.

        - a socket-type string (``"GEOMETRY"``) declares an empty item;
        - a socket / node source is linked in via the ``__extend__`` virtual
          socket (Blender makes an item of the source's own type, then renamed);
        - any other value declares an item of the inferred type and sets its
          default.
        """
        if isinstance(value, str):
            self.node.bundle_items.new(value, name)  # ty: ignore[invalid-argument-type]
        elif isinstance(value, (BaseNode, SocketLinker, bpy.types.NodeSocket)):
            extend = self.node.inputs[len(self.node.inputs) - 1]
            self.tree.link(self._source_socket(value), extend)
            # Re-fetch by index: the collection just grew, so any earlier item
            # reference is stale (see bpy collection invalidation).
            self.node.bundle_items[len(self.node.bundle_items) - 1].name = name
        else:
            socket_type = _infer_value_type(value)
            if socket_type is None:
                raise TypeError(f"Unsupported bundle item {name!r}: {value!r}")
            self.node.bundle_items.new(socket_type, name)  # ty: ignore[invalid-argument-type]
            self.node.inputs[name].default_value = value


class _SeparateBundleItems(_SocketItemFactory):
    """Typed factories for Separate Bundle items; each declares one bundle
    item and returns its typed output socket."""

    _owner: "_SeparateBundleMixin"

    def _declare(
        self, name: str, type: str, structure_type: _SocketShapeStructureType
    ) -> SocketLinker:
        node = self._owner.node
        item = node.bundle_items.new(type, name)  # ty: ignore[invalid-argument-type]
        if structure_type != "AUTO":
            item.structure_type = structure_type
        return _wrap_socket(
            _socket_for_item(node, node.bundle_items, "Item_", item, output=True)
        )


class _SeparateBundleMixin:
    """Items constructor + typed item factories for the Separate Bundle
    node, whose outputs are all dynamic bundle items."""

    if TYPE_CHECKING:
        node: bpy.types.NodeSeparateBundle

        def _establish_links(self, **kwargs: Any) -> None: ...

    def __init__(
        self,
        bundle: InputBundle = None,
        items: dict[str, str] | None = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        self.node.define_signature = define_signature
        # Items are output sockets pulled from the bundle; each is declared by
        # name and socket-type string (the inverse of CombineBundle, where the
        # type is inferred from a linked source).
        for name, socket_type in (items or {}).items():
            self.node.bundle_items.new(socket_type, name)  # ty: ignore[invalid-argument-type]
        self._establish_links(Bundle=bundle)

    @property
    def items(self) -> _SeparateBundleItems:
        """Typed item factories — declare bundle items with static types."""
        return _SeparateBundleItems(self)


class _FormatStringMixin(ItemsMixin):
    """Items constructor for the Format String node; ``items`` become the
    interpolated values inserted into the format template."""

    _items_collection = "format_items"
    _socket_data_types = ("VALUE", "INT", "STRING")
    _type_map = {"VALUE": "FLOAT"}

    if TYPE_CHECKING:

        @property
        def i(self) -> SocketAccessor: ...

    def __init__(
        self,
        format: InputString = "",
        items: Mapping[str, InputString | InputInteger | InputFloat] | None = None,
    ):
        super().__init__()
        key_args = {"Format": format}
        key_args.update(self._add_inputs(**(items or {})))
        self._establish_links(**key_args)

    @property
    def items(self) -> dict[str, SocketLinker]:
        """Input sockets:"""
        return {socket.name: self.i._get(socket.name) for socket in self.node.inputs}


class _FieldToListMixin(ItemsMixin):
    """Items constructor + per-type ``float``/``integer``/… helpers for the
    Field to List node, which gathers field values into typed socket lists."""

    _items_collection = "list_items"
    _socket_data_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
    )
    _type_map = {"VALUE": "FLOAT"}

    if TYPE_CHECKING:
        # i/o are declared on the generated subclass; restate them here so the
        # item helpers below type-check against the mixin in isolation.
        @property
        def i(self) -> SocketAccessor: ...
        @property
        def o(self) -> SocketAccessor: ...

    def __init__(
        self,
        count: InputInteger = 1,
        items: dict[str, InputLinkable | str] | None = None,
        *,
        fields: dict[str, InputLinkable | str] | None = None,
    ):
        super().__init__()
        if fields is not None:
            warnings.warn(
                "'fields' is deprecated, use 'items'", DeprecationWarning, stacklevel=2
            )
            items = fields
        key_args = {"Count": count}
        key_args.update(self._add_inputs(**(items or {})))
        self._establish_links(**key_args)

    def _declare_item(
        self,
        type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
        ],
        name: str | None = None,
        default: Any | None = None,
    ) -> bpy.types.NodeSocket:
        item = self._new_item(name if name else type, type)

        input_socket = self.i[item.name]
        if isinstance(default, (BaseNode, SocketLinker)):
            self._establish_links(**{item.name: default})
        else:
            input_socket.default_value = default

        return self.o[item.name].socket

    def float(
        self, input: InputFloat = 0.0, name: str | None = None
    ) -> FloatSocketList:
        return FloatSocketList(self._declare_item("FLOAT", name, input))

    def integer(
        self, input: InputInteger = 0, name: str | None = None
    ) -> IntegerSocketList:
        return IntegerSocketList(self._declare_item("INT", name, input))

    def boolean(
        self, input: InputBoolean = False, name: str | None = None
    ) -> BooleanSocketList:
        return BooleanSocketList(self._declare_item("BOOLEAN", name, input))

    def vector(
        self, input: InputVector = (0, 0, 0), name: str | None = None
    ) -> VectorSocketList:
        return VectorSocketList(self._declare_item("VECTOR", name, input))

    def color(
        self, input: InputColor = (0, 0, 0, 1), name: str | None = None
    ) -> ColorSocketList:
        return ColorSocketList(self._declare_item("RGBA", name, input))

    def rotation(
        self, input: InputRotation = Euler((0, 0, 0)), name: str | None = None
    ) -> RotationSocketList:
        return RotationSocketList(self._declare_item("ROTATION", name, input))

    def matrix(
        self, input: InputMatrix = None, name: str | None = None
    ) -> MatrixSocketList:
        return MatrixSocketList(self._declare_item("MATRIX", name, input))

    def string(
        self, input: InputString = "", name: str | None = None
    ) -> StringSocketList:
        return StringSocketList(self._declare_item("STRING", name, input))

    def menu(
        self, input: InputString = None, name: str | None = None
    ) -> MenuSocketList:
        return MenuSocketList(self._declare_item("MENU", name, input))


class _HandleModeMixin:
    """Shared ``left``/``right``/``mode`` flags for the Bézier handle nodes
    (``SetHandleType`` / ``HandleTypeSelection``), whose ``mode`` is an
    ENUM_FLAG set drawn from ``{"LEFT", "RIGHT"}``. ``left``/``right`` are
    ergonomic per-side toggles; ``mode`` exposes the raw set."""

    if TYPE_CHECKING:
        node: (
            bpy.types.GeometryNodeCurveSetHandles
            | bpy.types.GeometryNodeCurveHandleTypeSelection
        )

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        self.node.mode = (
            (self.node.mode | {"LEFT"}) if value else (self.node.mode - {"LEFT"})
        )

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        self.node.mode = (
            (self.node.mode | {"RIGHT"}) if value else (self.node.mode - {"RIGHT"})
        )

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]):
        self.node.mode = value
