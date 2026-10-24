"""Hand-written mixins attached to auto-generated node classes.

These hold reusable behaviour that the code generator cannot derive on its own
(ergonomic flag accessors, items helpers, …). The ``gen`` package wires them
onto the generated classes via :class:`~gen.NodeCustomization`, so the bulky
boilerplate (sockets, docstrings, property accessors) stays generated while the
bespoke behaviour lives here.
"""

from __future__ import annotations

import warnings
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Literal, cast

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
    StringSocketList,
    VectorSocketList,
)
from ..builder._infer import infer_node_type
from ..builder.items import (
    _ALL_ITEM_TYPES,
    _DEFAULT_NAMES,
    Item,
    ItemCollection,
    _deprecated,
    _FieldItems,
    _socket_for_item,
    _SocketItems,
    _SocketValueItems,
    _ValueItems,
)
from ..builder.socket import BaseSocket
from ..types import (
    InputAny,
    InputBoolean,
    InputBundle,
    InputClosure,
    InputCollection,
    InputColor,
    InputFloat,
    InputFont,
    InputGeometry,
    InputImage,
    InputInteger,
    InputLinkable,
    InputMaterial,
    InputMatrix,
    InputMenu,
    InputObject,
    InputRotation,
    InputSound,
    InputString,
    InputVector,
    _BakedDataTypeValues,
)

if TYPE_CHECKING:
    from ..builder import (
        BooleanSocket,
        BundleSocket,
        ClosureSocket,
        CollectionSocket,
        ColorSocket,
        FloatSocket,
        FontSocket,
        GeometrySocket,
        ImageSocket,
        IntegerSocket,
        MaterialSocket,
        MatrixSocket,
        MenuSocket,
        ObjectSocket,
        RotationSocket,
        SoundSocket,
        StringSocket,
        VectorSocket,
    )


class _BakeItems(_FieldItems):
    """Bake items: the field types plus the geometry-ish types bake items
    additionally support."""

    def string(
        self, value: InputString = None, name: str | None = None
    ) -> Item[StringSocket]:
        return self._typed(value, name, "STRING")

    def geometry(
        self, value: InputGeometry = None, name: str | None = None
    ) -> Item[GeometrySocket]:
        return self._typed(value, name, "GEOMETRY")

    def bundle(
        self, value: InputBundle = None, name: str | None = None
    ) -> Item[BundleSocket]:
        return self._typed(value, name, "BUNDLE")


class _BakeMixin(ItemsMixin):
    """Variadic items constructor for the Bake node. Items may be passed
    positionally (``*args``, named after their sources), as a ``name ->
    value`` mapping, or as keyword arguments."""

    _items_collection = "bake_items"
    # sources are matched by socket type (VALUE), items are made by item type (FLOAT)
    _socket_data_types = tuple(
        "VALUE" if t == "FLOAT" else t for t in _BakedDataTypeValues
    )
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    def __init__(
        self,
        *args: InputLinkable | str,
        items: Mapping[str, InputAny] | Iterable[InputAny] | None = None,
        **kwargs: InputAny,
    ):
        """
        Parameters
        ----------
        *args : InputLinkable | str
            Values to bake, each as an item named after the socket it comes
            from; a socket-type string declares an unlinked item.
        items : dict[str, InputLinkable | str] | None
            Items by name: a value to bake, or a socket-type string.
        **kwargs : InputLinkable | str
            More items by name.
        """
        super().__init__()
        self.items._add_all(args)
        self.items._add_all(items)
        self.items._add_all(kwargs)
        self._establish_links()

    @property
    def items(self) -> _BakeItems:
        """The bake items."""
        return _BakeItems(self)


class _CombineBundleItems(_SocketValueItems):
    """Combine Bundle items: each has an input socket to feed."""

    _has_output = False


class _CombineBundleMixin(ItemsMixin):
    """Items constructor for the Combine Bundle node, whose inputs are all
    dynamic bundle items."""

    _items_collection = "bundle_items"
    _socket_data_types = _ALL_ITEM_TYPES
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    if TYPE_CHECKING:
        node: bpy.types.NodeCombineBundle

    def __init__(
        self,
        items: Mapping[str, InputAny] | Iterable[InputAny] | None = None,
        *,
        define_signature: bool = False,
    ):
        """
        Parameters
        ----------
        items : dict[str, InputAny] | None
            Bundle items by name: a value or a link, with the type inferred.
        define_signature : bool
            Whether the node defines the bundle's signature.
        """
        super().__init__()
        self.items._add_all(items)
        self.node.define_signature = define_signature

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(self.node, self._items, "Item_", item, output=output)

    @property
    def items(self) -> _CombineBundleItems:
        """The bundle items."""
        return _CombineBundleItems(self)


class _SeparateBundleItems(_SocketItems):
    """Separate Bundle items: each has an output socket to read."""

    _has_input = False


class _SeparateBundleMixin(ItemsMixin):
    """Items constructor for the Separate Bundle node, whose outputs are all
    dynamic bundle items declared by name and socket type."""

    _items_collection = "bundle_items"
    _socket_data_types = _ALL_ITEM_TYPES
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    if TYPE_CHECKING:
        node: bpy.types.NodeSeparateBundle

    def __init__(
        self,
        bundle: InputBundle = None,
        items: Mapping[str, str] | None = None,
        *,
        define_signature: bool = False,
    ):
        """
        Parameters
        ----------
        bundle : InputBundle
            The bundle to separate.
        items : dict[str, str] | None
            The items to pull out, by name, each with its socket type
            (``"FLOAT"``, ``"GEOMETRY"``, ...).
        define_signature : bool
            Whether the node defines the bundle's signature.
        """
        super().__init__()
        self.node.define_signature = define_signature
        self.items._add_all(items)
        self._establish_links(Bundle=bundle)

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(self.node, self._items, "Item_", item, output=output)

    @property
    def items(self) -> _SeparateBundleItems:
        """The bundle items."""
        return _SeparateBundleItems(self)


class _ClosureToListItems(_SocketItems):
    """Closure to List items: each has an output socket carrying a list of
    that type, one element per closure evaluation."""

    _has_input = False


class _ClosureToListMixin(ItemsMixin):
    """Items constructor for the Closure to List node, whose outputs are all
    dynamic list items filled by evaluating the closure ``count`` times.
    Items must be declared explicitly — Blender only syncs them from the
    linked closure's signature on an editor update, which never runs in a
    headless build."""

    _items_collection = "list_items"
    _socket_data_types = _ALL_ITEM_TYPES
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    if TYPE_CHECKING:
        node: bpy.types.GeometryNodeClosureToList

    def __init__(
        self,
        count: InputInteger = 1,
        closure: InputClosure = None,
        items: Mapping[str, str] | None = None,
    ):
        """
        Parameters
        ----------
        count : InputInteger
            How many times the closure is evaluated.
        closure : InputClosure
            The closure to evaluate.
        items : dict[str, str] | None
            The output lists by name, each with the socket type of its
            elements (``"FLOAT"``, ``"GEOMETRY"``, ...).
        """
        super().__init__()
        self.items._add_all(items)
        self._establish_links(Count=count, Closure=closure)

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(self.node, self._items, "List_", item, output=output)

    @property
    def items(self) -> _ClosureToListItems:
        """The list items."""
        return _ClosureToListItems(self)


class _FormatStringItems(_ValueItems[Item]):
    """Format String items: the values interpolated into the template, each
    with an input socket."""

    _has_output = False

    def float(
        self, value: InputFloat = None, name: str | None = None
    ) -> Item[FloatSocket]:
        return self._typed(value, name, "FLOAT")

    def integer(
        self, value: InputInteger = None, name: str | None = None
    ) -> Item[IntegerSocket]:
        return self._typed(value, name, "INT")

    def string(
        self, value: InputString = None, name: str | None = None
    ) -> Item[StringSocket]:
        return self._typed(value, name, "STRING")


class _FormatStringMixin(ItemsMixin):
    """Items constructor for the Format String node; ``items`` become the
    interpolated values inserted into the format template."""

    _items_collection = "format_items"
    _socket_data_types = ("VALUE", "INT", "STRING")
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    def __init__(
        self,
        format: InputString = "",
        items: Mapping[str, InputString | InputInteger | InputFloat]
        | Iterable[InputString | InputInteger | InputFloat]
        | None = None,
    ):
        """
        Parameters
        ----------
        format : InputString
            The template, with ``{name}`` fields.
        items : Mapping[str, InputString | InputInteger | InputFloat] | None
            The values inserted into the template, by field name.
        """
        super().__init__()
        self.items._add_all(items)
        self._establish_links(Format=format)

    @property
    def items(self) -> _FormatStringItems:
        """The interpolated items."""
        return _FormatStringItems(self)


class _FieldToListItems(_ValueItems[Item]):
    """Field to List items: ``input`` is the field gathered, ``output`` the
    resulting list socket."""

    def float(
        self, value: InputFloat = None, name: str | None = None
    ) -> Item[FloatSocket, FloatSocketList]:
        return self._typed(value, name, "FLOAT")

    def integer(
        self, value: InputInteger = None, name: str | None = None
    ) -> Item[IntegerSocket, IntegerSocketList]:
        return self._typed(value, name, "INT")

    def boolean(
        self, value: InputBoolean = None, name: str | None = None
    ) -> Item[BooleanSocket, BooleanSocketList]:
        return self._typed(value, name, "BOOLEAN")

    def vector(
        self, value: InputVector = None, name: str | None = None
    ) -> Item[VectorSocket, VectorSocketList]:
        return self._typed(value, name, "VECTOR")

    def color(
        self, value: InputColor = None, name: str | None = None
    ) -> Item[ColorSocket, ColorSocketList]:
        return self._typed(value, name, "RGBA")

    def rotation(
        self, value: InputRotation = None, name: str | None = None
    ) -> Item[RotationSocket, RotationSocketList]:
        return self._typed(value, name, "ROTATION")

    def matrix(
        self, value: InputMatrix = None, name: str | None = None
    ) -> Item[MatrixSocket, MatrixSocketList]:
        return self._typed(value, name, "MATRIX")

    def string(
        self, value: InputString = None, name: str | None = None
    ) -> Item[StringSocket, StringSocketList]:
        return self._typed(value, name, "STRING")

    def menu(
        self, value: InputMenu = None, name: str | None = None
    ) -> Item[MenuSocket, MenuSocketList]:
        return self._typed(value, name, "MENU")


class _UnnamedItems[T: BaseSocket](ItemCollection["Item[T]"]):
    """Unnamed items, all of the owner's data type, each with an input
    socket: Index Switch and Combine List."""

    _has_output = False

    def new(self, value: InputAny = None) -> Item[T]:
        """Add an item, linked from or defaulting to ``value``."""
        return self._declare(value, "", self._owner.data_type)

    def _add_all(self, items: Mapping[str, Any] | Iterable[Any] | None) -> None:
        for value in items or ():
            self.new(value)


class _UnnamedItemsMixin(ItemsMixin):
    """Items machinery for nodes whose items are unnamed and untyped, with
    the node's ``data_type`` fixing the type of every item and each item's
    input socket identified as ``Item_<identifier>``: Index Switch and
    Combine List. ``_items_collection`` and ``data_type`` come from the
    node class."""

    if TYPE_CHECKING:
        node: Any

        @property
        def data_type(self) -> str: ...

    @property
    def items(self) -> _UnnamedItems[Any]:
        """The node's items, one input socket each."""
        return _UnnamedItems(self)

    @property
    def _socket_data_types(self) -> tuple[str, ...]:
        # "FLOAT" is the data_type spelling of socket.type "VALUE".
        return ("VALUE" if self.data_type == "FLOAT" else self.data_type,)

    def _new_item(self, name: str, type: str) -> Any:
        return self._items.new()

    def _item_socket(self, item: Any, *, output: bool = False) -> bpy.types.NodeSocket:
        if output:
            raise ValueError("the items have no output sockets")
        identifier = f"Item_{item.identifier}"
        for socket in self.node.inputs:
            if socket.identifier == identifier:
                return socket
        raise KeyError(f"No input socket for item {item.identifier}")


_CombineListDataType = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "MENU",
    "OBJECT",
    "IMAGE",
    "GEOMETRY",
    "COLLECTION",
    "MATERIAL",
    "BUNDLE",
    "CLOSURE",
    "FONT",
    "SOUND",
]


class _CombineListMixin(_UnnamedItemsMixin):
    """Items constructor for the Combine List node: one input per item,
    all of the node's ``data_type``, combined into a list."""

    _items_collection = "combine_list_items"

    def __init__(
        self,
        items: Iterable[InputAny] = (),
        *,
        data_type: _CombineListDataType = "FLOAT",
    ):
        """
        Parameters
        ----------
        items : Iterable[InputAny]
            One input per item: a default value, something to link from, or
            None for an input left open.
        data_type : str
            The type of every item and of the list.
        """
        super().__init__()
        self.node.data_type = data_type
        self._items.clear()
        self.items._add_all(items)


class _FieldToListMixin(ItemsMixin):
    """Items constructor for the Field to List node, which gathers field
    values into typed socket lists."""

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
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    def __init__(
        self,
        count: InputInteger = 1,
        items: Mapping[str, InputAny] | Iterable[InputAny] | None = None,
        *,
        fields: dict[str, InputLinkable | str] | None = None,
    ):
        """
        Parameters
        ----------
        count : InputInteger
            The length of the lists.
        items : dict[str, InputLinkable | str] | None
            The fields to gather, by name: a value or a link, or a
            socket-type string for an input left open.
        fields : dict[str, InputLinkable | str] | None
            Deprecated name of ``items``.
        """
        super().__init__()
        if fields is not None:
            _deprecated("FieldToList(fields=)", "FieldToList(items=)")
            items = fields
        self.items._add_all(items)
        self._establish_links(Count=count)

    @property
    def items(self) -> _FieldToListItems:
        """The list items."""
        return _FieldToListItems(self)

    # -- deprecated per-type methods, removed in 530 --

    def _list_item(self, type: str, value: Any, name: str | None) -> Any:
        _deprecated(
            f"FieldToList.{_DEFAULT_NAMES[type].lower()}(value, name)",
            "items.<type>(value, name).output",
        )
        return self.items._declare(value, name, type).output

    def float(
        self, input: InputFloat = 0.0, name: str | None = None
    ) -> FloatSocketList:
        return self._list_item("FLOAT", input, name)

    def integer(
        self, input: InputInteger = 0, name: str | None = None
    ) -> IntegerSocketList:
        return self._list_item("INT", input, name)

    def boolean(
        self, input: InputBoolean = False, name: str | None = None
    ) -> BooleanSocketList:
        return self._list_item("BOOLEAN", input, name)

    def vector(
        self, input: InputVector = (0, 0, 0), name: str | None = None
    ) -> VectorSocketList:
        return self._list_item("VECTOR", input, name)

    def color(
        self, input: InputColor = (0, 0, 0, 1), name: str | None = None
    ) -> ColorSocketList:
        return self._list_item("RGBA", input, name)

    def rotation(
        self, input: InputRotation = None, name: str | None = None
    ) -> RotationSocketList:
        return self._list_item(
            "ROTATION", Euler((0, 0, 0)) if input is None else input, name
        )

    def matrix(
        self, input: InputMatrix = None, name: str | None = None
    ) -> MatrixSocketList:
        return self._list_item("MATRIX", input, name)

    def string(
        self, input: InputString = "", name: str | None = None
    ) -> StringSocketList:
        return self._list_item("STRING", input, name)

    def menu(
        self, input: InputString = None, name: str | None = None
    ) -> MenuSocketList:
        return self._list_item("MENU", input, name)


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
    def left(self, value: bool) -> None:
        self.node.mode = (
            (self.node.mode | {"LEFT"}) if value else (self.node.mode - {"LEFT"})
        )

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool) -> None:
        self.node.mode = (
            (self.node.mode | {"RIGHT"}) if value else (self.node.mode - {"RIGHT"})
        )

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]) -> None:
        self.node.mode = value


_SwitchType = Literal[
    "FLOAT",
    "INT",
    "BOOLEAN",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
    "MENU",
    "OBJECT",
    "IMAGE",
    "GEOMETRY",
    "COLLECTION",
    "MATERIAL",
    "BUNDLE",
    "CLOSURE",
    "FONT",
    "SOUND",
    "INT_VECTOR",  # compositor only
    "SHADER",  # shader only
]


class _SwitchMixin:
    """Switch's constructor: without an ``input_type``, the type comes from
    the values switched between, so a node passed in links the output of
    that type (``g.Switch(cond, g.Cube(), g.UVSphere())`` switches meshes)."""

    if TYPE_CHECKING:
        node: bpy.types.GeometryNodeSwitch

        def _establish_links(self, **kwargs: InputAny) -> None: ...

    def __init__(
        self,
        switch: InputBoolean = False,
        false: InputAny = None,
        true: InputAny = None,
        *,
        input_type: _SwitchType | None = None,
    ):
        super().__init__()
        if input_type is None:
            # when the values don't decide, the type a new node has in this
            # tree (Color in shader and compositor trees)
            input_type = cast(
                "_SwitchType",
                infer_node_type(
                    self.node, "input_type", (false, true), default=self.node.input_type
                ),
            )
        self.input_type = input_type
        self._establish_links(**{"Switch": switch, "False": false, "True": true})


_PACKAGE_DIR = str(Path(__file__).resolve().parents[1])


class _DeprecatedNodeMixin:
    """A node Blender deprecates: building one warns and names the replacement."""

    _replacement: ClassVar[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        warnings.warn(
            f"Blender deprecates the {type(self).__name__} node; use "
            f"{self._replacement} instead.",
            DeprecationWarning,
            # point at the caller's code, past the class methods that build it
            skip_file_prefixes=(_PACKAGE_DIR,),
        )
        super().__init__(*args, **kwargs)


class _ViewerItems(_FieldItems):
    """Viewer items: each is an input showing a value in the spreadsheet and
    viewport; every socket type can be viewed."""

    _has_output = False

    def string(
        self, value: InputString = None, name: str | None = None
    ) -> Item[StringSocket]:
        return self._typed(value, name, "STRING")

    def menu(
        self, value: InputMenu = None, name: str | None = None
    ) -> Item[MenuSocket]:
        return self._typed(value, name, "MENU")

    def object(
        self, value: InputObject = None, name: str | None = None
    ) -> Item[ObjectSocket]:
        return self._typed(value, name, "OBJECT")

    def image(
        self, value: InputImage = None, name: str | None = None
    ) -> Item[ImageSocket]:
        return self._typed(value, name, "IMAGE")

    def geometry(
        self, value: InputGeometry = None, name: str | None = None
    ) -> Item[GeometrySocket]:
        return self._typed(value, name, "GEOMETRY")

    def collection(
        self, value: InputCollection = None, name: str | None = None
    ) -> Item[CollectionSocket]:
        return self._typed(value, name, "COLLECTION")

    def material(
        self, value: InputMaterial = None, name: str | None = None
    ) -> Item[MaterialSocket]:
        return self._typed(value, name, "MATERIAL")

    def bundle(
        self, value: InputBundle = None, name: str | None = None
    ) -> Item[BundleSocket]:
        return self._typed(value, name, "BUNDLE")

    def closure(
        self, value: InputClosure = None, name: str | None = None
    ) -> Item[ClosureSocket]:
        return self._typed(value, name, "CLOSURE")

    def font(
        self, value: InputFont = None, name: str | None = None
    ) -> Item[FontSocket]:
        return self._typed(value, name, "FONT")

    def sound(
        self, value: InputSound = None, name: str | None = None
    ) -> Item[SoundSocket]:
        return self._typed(value, name, "SOUND")


class _ViewerMixin(ItemsMixin):
    """Items for the Viewer node, whose inputs are all viewer items."""

    _items_collection = "viewer_items"
    _socket_data_types = _ALL_ITEM_TYPES
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    @property
    def items(self) -> _ViewerItems:
        """The values to view, one input socket each."""
        return _ViewerItems(self)


class _FileOutputItems(_ValueItems[Item]):
    """File Output items: each is an image, value or vector to write out."""

    _has_output = False

    def float(
        self, value: InputFloat = None, name: str | None = None
    ) -> Item[FloatSocket]:
        return self._typed(value, name, "FLOAT")

    def vector(
        self, value: InputVector = None, name: str | None = None
    ) -> Item[VectorSocket]:
        return self._typed(value, name, "VECTOR")

    def color(
        self, value: InputColor = None, name: str | None = None
    ) -> Item[ColorSocket]:
        return self._typed(value, name, "RGBA")


class _FileOutputMixin(ItemsMixin):
    """Items for the compositor's File Output node, one input per file or
    layer written."""

    _items_collection = "file_output_items"
    _socket_data_types = ("VALUE", "VECTOR", "RGBA")
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    @property
    def items(self) -> _FileOutputItems:
        """The inputs to write, one per item."""
        return _FileOutputItems(self)


class _RaycastItems(_ValueItems[Item]):
    """Raycast's sample attributes: each item's input is the name of the
    attribute to read where the ray hits, and its output the value read.
    A color item also has an "<name> Alpha" output on the node."""

    _value_types = ("STRING",)

    def float(
        self, attribute: InputString, name: str | None = None
    ) -> Item[FloatSocket]:
        """Sample the float attribute named ``attribute`` at the hit point."""
        return self._attribute(attribute, name, "FLOAT")

    def vector(
        self, attribute: InputString, name: str | None = None
    ) -> Item[VectorSocket]:
        """Sample the vector attribute named ``attribute`` at the hit point."""
        return self._attribute(attribute, name, "VECTOR")

    def color(
        self, attribute: InputString, name: str | None = None
    ) -> Item[ColorSocket]:
        """Sample the color attribute named ``attribute`` at the hit point."""
        return self._attribute(attribute, name, "RGBA")

    def new(  # ty: ignore[invalid-method-override]
        self, attribute: InputString = None, name: str | None = None, *, type: str
    ) -> Item:
        """Sample ``attribute`` as a runtime-chosen ``type`` (``"FLOAT"``,
        ``"VECTOR"`` or ``"RGBA"``)."""
        return self._attribute(attribute, name, type)

    def _attribute(self, attribute: Any, name: str | None, type: str) -> Any:
        # the value is the attribute's name, so it also names the item, and
        # it isn't the old name-first order ``_typed`` watches for
        if name is None and isinstance(attribute, str):
            name = attribute
        return self._declare(attribute, name, type)


class _RaycastMixin(ItemsMixin):
    """Sample attributes for the shader Raycast node."""

    _items_collection = "sample_attribute_items"
    _socket_data_types = ("VALUE", "VECTOR", "RGBA")
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        # the item sockets are Value_<n> in, Attribute_<n> out; a color item's
        # extra Attribute_<n>_Alpha output is not one of them
        prefix = "Attribute_" if output else "Value_"
        sockets = self.node.outputs if output else self.node.inputs
        own = [
            s
            for s in sockets
            if s.identifier.startswith(prefix) and s.identifier[len(prefix) :].isdigit()
        ]
        index = next(i for i, candidate in enumerate(self._items) if candidate == item)
        return own[index]

    @property
    def items(self) -> _RaycastItems:
        """The attributes to sample at the hit point."""
        return _RaycastItems(self)
