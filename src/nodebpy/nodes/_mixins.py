"""Hand-written mixins attached to auto-generated node classes.

These hold reusable behaviour that the code generator cannot derive on its own
(ergonomic flag accessors, items helpers, …). ``generate.py`` wires them onto
the generated classes via :class:`~generate.NodeCustomization`, so the bulky
boilerplate (sockets, docstrings, property accessors) stays generated while the
bespoke behaviour lives here.
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

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
from ..types import (
    InputBoolean,
    InputColor,
    InputFloat,
    InputInteger,
    InputLinkable,
    InputMatrix,
    InputRotation,
    InputString,
    InputVector,
    _BakedDataTypeValues,
)


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
        key_args.update(self._add_inputs(**(items or {})))  # type: ignore
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
