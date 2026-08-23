from abc import ABC
from typing import TYPE_CHECKING, TypeVar, Union, cast

import bpy
from bpy.types import (
    NodeClosureInput,
    NodeClosureInputItems,
    NodeClosureOutput,
    NodeClosureOutputItems,
    NodeEvaluateClosureInputItems,
    NodeEvaluateClosureOutputItems,
)

if TYPE_CHECKING:
    from .manual import EvaluateClosure

from ...builder import BaseNode as BaseNode
from ...builder import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    FloatSocket,
    GeometrySocket,
    ImageSocket,
    IntegerSocket,
    Item,
    ItemsMixin,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    StringSocket,
    VectorSocket,
)
from ...builder import Socket as SocketLinker
from ...builder._registry import _wrap_socket
from ...builder._utils import _SocketLike
from ...builder.accessor import SocketAccessor
from ...builder.items import _infer_value_type, _socket_for_item, _SocketItemFactory
from ...types import (
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
    _AttributeDomains,
    _is_default_value,
    _SocketShapeStructureType,
)

_SocketT = TypeVar("_SocketT", bound=SocketLinker, default=SocketLinker)


class BaseZone(ItemsMixin, BaseNode, ABC):
    # zone sockets can share names across fixed sockets and item collections,
    # so item sockets are found by identifier prefix instead of by name
    _item_identifier_prefix = "Item_"

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(
            self.node, self._items, self._item_identifier_prefix, item, output=output
        )


class BaseZoneInput(BaseZone, ABC):
    """Base class for zone input nodes"""

    node: bpy.types.GeometryNodeSimulationInput | bpy.types.GeometryNodeRepeatInput

    @property
    def _items_node(self):
        return self.node.paired_output

    @property
    def output(
        self,
    ) -> (
        bpy.types.GeometryNodeSimulationOutput
        | bpy.types.GeometryNodeRepeatOutput
        | bpy.types.GeometryNodeForeachGeometryElementOutput
    ):
        return self.node.paired_output  # type: ignore


class BaseZoneOutput(BaseZone, ABC):
    """Base class for zone output nodes"""

    node: bpy.types.GeometryNodeSimulationOutput | bpy.types.GeometryNodeRepeatOutput


class ZoneItem(Item[_SocketT]):
    """Handle for a simulation/repeat state item (four sockets per item).

    The type parameter is the socket class every role returns; the typed
    factories on ``zone.items`` (:class:`_StateZoneItems`) produce
    parameterised handles such as ``ZoneItem[GeometrySocket]``.
    """

    def __init__(self, input_node: BaseZoneInput, output_node: BaseZoneOutput, item):
        super().__init__(output_node, item)
        self._input_node = input_node

    @property
    def initial(self) -> _SocketT:
        """Input-node input socket — set the item's starting value."""
        return cast("_SocketT", _wrap_socket(self._input_node._item_socket(self._item)))

    @property
    def current(self) -> _SocketT:
        """Input-node output socket — read the item inside the zone body."""
        return cast(
            "_SocketT",
            _wrap_socket(self._input_node._item_socket(self._item, output=True)),
        )

    @property
    def next(self) -> _SocketT:
        """Output-node input socket — write the item's per-iteration result."""
        return self.input

    @property
    def result(self) -> _SocketT:
        """Output-node output socket — read the item after the zone."""
        return self.output


class _ZonePair:
    """Zone wrapper holding the paired input and output builder nodes.

    Supports ``input, output = zone`` unpacking and indexing with
    ``zone[0]`` / ``zone[1]``.
    """

    input: BaseNode
    output: BaseNode

    def _pair(self) -> None:
        """Pair the two nodes. Must run before any linking — sockets on an
        unpaired zone node are inactive."""
        self.input.node.pair_with_output(self.output.node)  # ty: ignore[unresolved-attribute]

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.input
            case 1:
                return self.output
            case _:
                raise IndexError(f"{type(self).__name__} has only two items")

    def __iter__(self):
        return iter((self.input, self.output))


class _StateZone(_ZonePair):
    """Zone wrapper for zones with shared state items (simulation/repeat)."""

    input: BaseZoneInput
    output: BaseZoneOutput

    def _init_items(self, items: dict[str, InputAny] | None) -> None:
        self.output._items.clear()
        for name, value in (items or {}).items():
            self.item(name, value)

    def item(
        self,
        name: str,
        initial: InputAny = None,
        *,
        type: str | None = None,
    ) -> ZoneItem:
        """Declare a state item and return its handle.

        ``initial`` may be a linkable (linked as the item's starting
        value), a plain default value, or a socket-type string such as
        ``"FLOAT"`` (declares the item without linking).
        """
        output = self.output
        if type is None:
            declared = output._declared_item_type(initial)
            if declared is not None:
                type, initial = declared, None
        if initial is not None and not _is_default_value(initial):
            source, inferred, _ = output._resolve_capture(
                cast("InputLinkable", initial), name=name
            )
            item = output._new_item(name, type or inferred)
            handle = ZoneItem(self.input, output, item)
            output.tree.link(source, handle.initial.socket)
        else:
            if type is None:
                type = _infer_value_type(initial)
            if type is None:
                raise TypeError(
                    f"cannot infer a socket type for item {name!r}; pass type="
                )
            item = output._new_item(name, type)
            handle = ZoneItem(self.input, output, item)
            if initial is not None:
                handle.initial.socket.default_value = initial  # ty: ignore[unresolved-attribute]
        return handle


class _StateZoneItems:
    """Typed per-datatype item factories for simulation/repeat zones.

    Each method declares one state item and returns its
    :class:`ZoneItem` handle parameterised with the matching socket
    class, so ``initial``/``current``/``next``/``result`` are statically
    typed. ``initial`` may be a linkable (linked as the starting value)
    or a plain default value; omit it to declare the item unlinked.
    """

    def __init__(self, zone: _StateZone):
        self._zone = zone

    def _declare(self, name: str, initial: InputAny, type: str) -> ZoneItem:
        if isinstance(initial, bpy.types.ID):
            # datablocks (Object, Image, …) are socket defaults, not linkables
            handle = self._zone.item(name, type=type)
            handle.initial.socket.default_value = initial  # ty: ignore[unresolved-attribute]
            return handle
        return self._zone.item(name, initial, type=type)

    def float(
        self, name: str = "Value", initial: InputFloat = None
    ) -> "ZoneItem[FloatSocket]":
        return cast("ZoneItem[FloatSocket]", self._declare(name, initial, "FLOAT"))

    def integer(
        self, name: str = "Integer", initial: InputInteger = None
    ) -> "ZoneItem[IntegerSocket]":
        return cast("ZoneItem[IntegerSocket]", self._declare(name, initial, "INT"))

    def boolean(
        self, name: str = "Boolean", initial: InputBoolean = None
    ) -> "ZoneItem[BooleanSocket]":
        return cast("ZoneItem[BooleanSocket]", self._declare(name, initial, "BOOLEAN"))

    def vector(
        self, name: str = "Vector", initial: InputVector = None
    ) -> "ZoneItem[VectorSocket]":
        return cast("ZoneItem[VectorSocket]", self._declare(name, initial, "VECTOR"))

    def color(
        self, name: str = "Color", initial: InputColor = None
    ) -> "ZoneItem[ColorSocket]":
        return cast("ZoneItem[ColorSocket]", self._declare(name, initial, "RGBA"))

    def rotation(
        self, name: str = "Rotation", initial: InputRotation = None
    ) -> "ZoneItem[RotationSocket]":
        return cast(
            "ZoneItem[RotationSocket]", self._declare(name, initial, "ROTATION")
        )

    def matrix(
        self, name: str = "Matrix", initial: InputMatrix = None
    ) -> "ZoneItem[MatrixSocket]":
        return cast("ZoneItem[MatrixSocket]", self._declare(name, initial, "MATRIX"))

    def string(
        self, name: str = "String", initial: InputString = None
    ) -> "ZoneItem[StringSocket]":
        return cast("ZoneItem[StringSocket]", self._declare(name, initial, "STRING"))

    def geometry(
        self, name: str = "Geometry", initial: InputGeometry = None
    ) -> "ZoneItem[GeometrySocket]":
        return cast(
            "ZoneItem[GeometrySocket]", self._declare(name, initial, "GEOMETRY")
        )

    def bundle(
        self, name: str = "Bundle", initial: InputBundle = None
    ) -> "ZoneItem[BundleSocket]":
        return cast("ZoneItem[BundleSocket]", self._declare(name, initial, "BUNDLE"))


class _SimulationZoneItems(_StateZoneItems):
    """Typed item factories for the simulation zone's state items."""


class _RepeatZoneItems(_StateZoneItems):
    """Typed item factories for the repeat zone's state items, including
    the datablock and closure types only the repeat zone supports."""

    def object(
        self, name: str = "Object", initial: InputObject = None
    ) -> "ZoneItem[ObjectSocket]":
        return cast("ZoneItem[ObjectSocket]", self._declare(name, initial, "OBJECT"))

    def image(
        self, name: str = "Image", initial: InputImage = None
    ) -> "ZoneItem[ImageSocket]":
        return cast("ZoneItem[ImageSocket]", self._declare(name, initial, "IMAGE"))

    def collection(
        self, name: str = "Collection", initial: InputCollection = None
    ) -> "ZoneItem[CollectionSocket]":
        return cast(
            "ZoneItem[CollectionSocket]", self._declare(name, initial, "COLLECTION")
        )

    def material(
        self, name: str = "Material", initial: InputMaterial = None
    ) -> "ZoneItem[MaterialSocket]":
        return cast(
            "ZoneItem[MaterialSocket]", self._declare(name, initial, "MATERIAL")
        )

    def closure(
        self, name: str = "Closure", initial: InputClosure = None
    ) -> "ZoneItem[ClosureSocket]":
        return cast("ZoneItem[ClosureSocket]", self._declare(name, initial, "CLOSURE"))


class BaseSimulationZone(BaseZone):
    _items_collection = "state_items"
    _socket_data_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "GEOMETRY",
        "BUNDLE",
    )
    _type_map = {"VALUE": "FLOAT"}


class SimulationInput(BaseSimulationZone, BaseZoneInput):
    """Simulation Input node"""

    _bl_idname = "GeometryNodeSimulationInput"
    node: bpy.types.GeometryNodeSimulationInput

    class _Outputs(SocketAccessor):
        delta_time: FloatSocket
        """Time elapsed since the previous simulation frame."""

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...


class SimulationOutput(BaseSimulationZone, BaseZoneOutput):
    """Simulation Output node"""

    _bl_idname = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    class _Inputs(SocketAccessor):
        skip: BooleanSocket
        """Skip the simulation for this frame."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...


class SimulationZone(_StateZone):
    input: SimulationInput
    output: SimulationOutput

    def __init__(self, items: dict[str, InputAny] | None = None):
        self.input = SimulationInput()
        self.output = SimulationOutput()
        self._pair()
        self._init_items(items)

    @property
    def items(self) -> _SimulationZoneItems:
        """Typed item factories — declare state items with static types."""
        return _SimulationZoneItems(self)

    @property
    def delta_time(self) -> FloatSocket:
        return self.input.o.delta_time


class BaseRepeatZone(BaseZone):
    _items_collection = "repeat_items"
    _socket_data_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    )

    _type_map = {"VALUE": "FLOAT"}


class RepeatInput(BaseRepeatZone, BaseZoneInput):
    """Repeat Input node"""

    _bl_idname = "GeometryNodeRepeatInput"
    node: bpy.types.GeometryNodeRepeatInput

    class _Outputs(SocketAccessor):
        iteration: IntegerSocket
        """The current iteration index."""

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, iterations: InputInteger = 1):
        super().__init__()
        key_args = {"Iterations": iterations}
        self._establish_links(**key_args)


class RepeatOutput(BaseRepeatZone, BaseZoneOutput):
    """Repeat Output node"""

    _bl_idname = "GeometryNodeRepeatOutput"
    node: bpy.types.GeometryNodeRepeatOutput


class RepeatZone(_StateZone):
    input: RepeatInput
    output: RepeatOutput

    def __init__(
        self,
        iterations: InputInteger = 1,
        items: dict[str, InputAny] | None = None,
    ):
        self.input = RepeatInput()
        self.output = RepeatOutput()
        self._pair()
        self.input._establish_links(Iterations=iterations)
        self._init_items(items)

    @property
    def items(self) -> _RepeatZoneItems:
        """Typed item factories — declare state items with static types."""
        return _RepeatZoneItems(self)

    @property
    def iteration(self) -> IntegerSocket:
        """The current iteration index."""
        return self.input.o.iteration


class _ForEachInputItems:
    """Typed factories for the for-each zone's input items — per-element
    fields made available inside the zone body. Each returns an
    :class:`Item` handle: ``input`` feeds the field, ``output`` reads the
    per-element value in the body."""

    def __init__(self, zone: "ForEachGeometryElementZone"):
        self._zone = zone

    def _declare(self, name: str, value: InputAny, type: str) -> Item:
        return self._zone.input.add_item(name, value, type=type)

    def float(
        self, name: str = "Value", value: InputFloat = None
    ) -> "Item[FloatSocket]":
        return cast("Item[FloatSocket]", self._declare(name, value, "FLOAT"))

    def integer(
        self, name: str = "Integer", value: InputInteger = None
    ) -> "Item[IntegerSocket]":
        return cast("Item[IntegerSocket]", self._declare(name, value, "INT"))

    def boolean(
        self, name: str = "Boolean", value: InputBoolean = None
    ) -> "Item[BooleanSocket]":
        return cast("Item[BooleanSocket]", self._declare(name, value, "BOOLEAN"))

    def vector(
        self, name: str = "Vector", value: InputVector = None
    ) -> "Item[VectorSocket]":
        return cast("Item[VectorSocket]", self._declare(name, value, "VECTOR"))

    def color(
        self, name: str = "Color", value: InputColor = None
    ) -> "Item[ColorSocket]":
        return cast("Item[ColorSocket]", self._declare(name, value, "RGBA"))

    def rotation(
        self, name: str = "Rotation", value: InputRotation = None
    ) -> "Item[RotationSocket]":
        return cast("Item[RotationSocket]", self._declare(name, value, "ROTATION"))

    def matrix(
        self, name: str = "Matrix", value: InputMatrix = None
    ) -> "Item[MatrixSocket]":
        return cast("Item[MatrixSocket]", self._declare(name, value, "MATRIX"))

    def menu(self, name: str = "Menu", value: InputMenu = None) -> "Item[MenuSocket]":
        return cast("Item[MenuSocket]", self._declare(name, value, "MENU"))


class _ForEachMainItems:
    """Typed factories for the for-each zone's main items — per-element
    results written back onto the input geometry. ``input`` is the
    ``>>`` target inside the body, ``output`` the combined result."""

    def __init__(self, zone: "ForEachGeometryElementZone"):
        self._zone = zone

    def _declare(self, name: str, value: InputAny, type: str) -> Item:
        return self._zone.output.add_item(name, value, type=type)

    def float(
        self, name: str = "Value", value: InputFloat = None
    ) -> "Item[FloatSocket]":
        return cast("Item[FloatSocket]", self._declare(name, value, "FLOAT"))

    def integer(
        self, name: str = "Integer", value: InputInteger = None
    ) -> "Item[IntegerSocket]":
        return cast("Item[IntegerSocket]", self._declare(name, value, "INT"))

    def boolean(
        self, name: str = "Boolean", value: InputBoolean = None
    ) -> "Item[BooleanSocket]":
        return cast("Item[BooleanSocket]", self._declare(name, value, "BOOLEAN"))

    def vector(
        self, name: str = "Vector", value: InputVector = None
    ) -> "Item[VectorSocket]":
        return cast("Item[VectorSocket]", self._declare(name, value, "VECTOR"))

    def color(
        self, name: str = "Color", value: InputColor = None
    ) -> "Item[ColorSocket]":
        return cast("Item[ColorSocket]", self._declare(name, value, "RGBA"))

    def rotation(
        self, name: str = "Rotation", value: InputRotation = None
    ) -> "Item[RotationSocket]":
        return cast("Item[RotationSocket]", self._declare(name, value, "ROTATION"))

    def matrix(
        self, name: str = "Matrix", value: InputMatrix = None
    ) -> "Item[MatrixSocket]":
        return cast("Item[MatrixSocket]", self._declare(name, value, "MATRIX"))


class _ForEachGeneratedItems:
    """Typed factories for the for-each zone's generation items — values
    stored on the generated geometry, evaluated on ``domain``. ``input``
    is the ``>>`` target inside the body, ``output`` the stored result."""

    def __init__(self, zone: "ForEachGeometryElementZone"):
        self._zone = zone

    def _declare(
        self, name: str, value: InputAny, type: str, domain: _AttributeDomains
    ) -> Item:
        return self._zone.output.add_generated_item(
            name, value, type=type, domain=domain
        )

    def float(
        self,
        name: str = "Value",
        value: InputFloat = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[FloatSocket]":
        return cast("Item[FloatSocket]", self._declare(name, value, "FLOAT", domain))

    def integer(
        self,
        name: str = "Integer",
        value: InputInteger = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[IntegerSocket]":
        return cast("Item[IntegerSocket]", self._declare(name, value, "INT", domain))

    def boolean(
        self,
        name: str = "Boolean",
        value: InputBoolean = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[BooleanSocket]":
        return cast(
            "Item[BooleanSocket]", self._declare(name, value, "BOOLEAN", domain)
        )

    def vector(
        self,
        name: str = "Vector",
        value: InputVector = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[VectorSocket]":
        return cast("Item[VectorSocket]", self._declare(name, value, "VECTOR", domain))

    def color(
        self,
        name: str = "Color",
        value: InputColor = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[ColorSocket]":
        return cast("Item[ColorSocket]", self._declare(name, value, "RGBA", domain))

    def rotation(
        self,
        name: str = "Rotation",
        value: InputRotation = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[RotationSocket]":
        return cast(
            "Item[RotationSocket]", self._declare(name, value, "ROTATION", domain)
        )

    def matrix(
        self,
        name: str = "Matrix",
        value: InputMatrix = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[MatrixSocket]":
        return cast("Item[MatrixSocket]", self._declare(name, value, "MATRIX", domain))

    def geometry(
        self,
        name: str = "Geometry",
        value: InputGeometry = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[GeometrySocket]":
        return cast(
            "Item[GeometrySocket]", self._declare(name, value, "GEOMETRY", domain)
        )


class ForEachGeometryElementZone(_ZonePair):
    input: "ForEachGeometryElementInput"
    output: "ForEachGeometryElementOutput"

    def __init__(
        self,
        geometry: InputGeometry = None,
        selection: InputBoolean = True,
        *,
        domain: _AttributeDomains = "POINT",
    ):
        self.input = ForEachGeometryElementInput()
        self.output = ForEachGeometryElementOutput()
        self._pair()
        self.output.domain = domain
        self.input._establish_links(Geometry=geometry, Selection=selection)

    @property
    def inputs(self) -> _ForEachInputItems:
        """Typed factories for per-element input items."""
        return _ForEachInputItems(self)

    @property
    def main(self) -> _ForEachMainItems:
        """Typed factories for main (per-element result) items."""
        return _ForEachMainItems(self)

    @property
    def generated(self) -> _ForEachGeneratedItems:
        """Typed factories for generation items."""
        return _ForEachGeneratedItems(self)

    @property
    def index(self) -> IntegerSocket:
        return self.input.o.index

    @property
    def element(self) -> GeometrySocket:
        """The current element as geometry, read inside the zone body."""
        return self.input.o.element

    @property
    def generation(self) -> "Item[GeometrySocket]":
        """Handle for the default generation item (the generated geometry)."""
        return cast(
            "Item[GeometrySocket]",
            _GenerationItem(self.output, self.output.items_generated[0]),
        )

    def item(
        self, name: str, value: InputLinkable = None, *, type: str | None = None
    ) -> Item:
        """Declare an input item — a per-element field made available
        inside the zone."""
        return self.input.add_item(name, value, type=type)

    def main_item(
        self, name: str, value: InputLinkable = None, *, type: str | None = None
    ) -> Item:
        """Declare a main item — a per-element result written back onto
        the input geometry."""
        return self.output.add_item(name, value, type=type)

    def generated_item(
        self,
        name: str,
        value: InputLinkable = None,
        *,
        type: str | None = None,
        domain: _AttributeDomains = "POINT",
    ) -> Item:
        """Declare a generation item — a value stored on the generated
        geometry with the given ``domain``."""
        return self.output.add_generated_item(name, value, type=type, domain=domain)


class ForEachGeometryElementInput(BaseZoneInput):
    """For Each Geometry Element Input node"""

    _items_collection = "input_items"
    _item_identifier_prefix = "Input_"
    _socket_data_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "MENU",
    )
    _type_map = {"VALUE": "FLOAT"}

    _bl_idname = "GeometryNodeForeachGeometryElementInput"
    node: bpy.types.GeometryNodeForeachGeometryElementInput

    class _Inputs(SocketAccessor):
        geometry: GeometrySocket
        """The geometry to iterate over."""
        selection: BooleanSocket
        """Limits which elements are iterated over."""

    class _Outputs(SocketAccessor):
        index: IntegerSocket
        """The index of the current element."""
        element: GeometrySocket

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(self, geometry: InputGeometry = None, selection: InputBoolean = True):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self._establish_links(**key_args)


class ForEachGeometryElementOutput(BaseZoneOutput):
    """For Each Geometry Element Output node"""

    _items_collection = "main_items"
    _item_identifier_prefix = "Main_"
    _socket_data_types: tuple[str, ...] = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
    )
    _generation_data_types = _socket_data_types + ("GEOMETRY",)
    _type_map = {"VALUE": "FLOAT"}

    _bl_idname = "GeometryNodeForeachGeometryElementOutput"
    node: bpy.types.GeometryNodeForeachGeometryElementOutput

    class _Inputs(SocketAccessor):
        generation_0: GeometrySocket
        """The geometry to generate elements from."""

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
        """The output geometry after processing all elements."""
        generation_0: GeometrySocket
        """The generated geometry output."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {}
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def items_generated(
        self,
    ) -> bpy.types.NodeGeometryForeachGeometryElementGenerationItems:
        return self.node.generation_items

    def add_generated_item(
        self,
        name: str,
        value: InputAny = None,
        *,
        type: str | None = None,
        domain: _AttributeDomains = "POINT",
    ) -> Item:
        """Add a generation item and return its handle.

        ``value`` may be a linkable (linked to the item's input) or a plain
        default value; otherwise ``type`` declares the item unlinked.
        """
        source = None
        if value is not None and not _is_default_value(value):
            source, inferred, _ = self._resolve_capture(
                cast("InputLinkable", value),
                name=name,
                types=self._generation_data_types,
            )
            type = type or inferred
        elif type is None:
            type = _infer_value_type(value)
            if type is None:
                raise TypeError(f"item {name!r} requires a value or an explicit type=")
        item = self.items_generated.new(type, name)  # ty: ignore[invalid-argument-type]
        item.domain = domain
        handle = _GenerationItem(self, item)
        if source is not None:
            self.tree.link(source, handle.input.socket)
        elif value is not None:
            handle.input.socket.default_value = value  # ty: ignore[unresolved-attribute]
        return handle

    def capture_generated(
        self,
        value: InputLinkable,
        *,
        name: str | None = None,
        domain: _AttributeDomains = "POINT",
    ) -> SocketLinker:
        """Capture ``value`` as a generated-geometry item evaluated on the
        given ``domain``, and return its output socket."""
        if name is None:
            _, _, name = self._resolve_capture(
                value, name=None, types=self._generation_data_types
            )
        return self.add_generated_item(name, value, domain=domain).output

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class _GenerationItem(Item[_SocketT]):
    """Handle for a ForEach generation item; its sockets carry the
    ``Generation_`` identifier prefix rather than the owner's default."""

    _owner: "ForEachGeometryElementOutput"

    @property
    def _collection(self):
        return self._owner.items_generated

    @property
    def input(self) -> _SocketT:
        return cast(
            "_SocketT",
            _wrap_socket(
                _socket_for_item(
                    self._owner.node,
                    self._owner.items_generated,
                    "Generation_",
                    self._item,
                )
            ),
        )

    @property
    def output(self) -> _SocketT:
        return cast(
            "_SocketT",
            _wrap_socket(
                _socket_for_item(
                    self._owner.node,
                    self._owner.items_generated,
                    "Generation_",
                    self._item,
                    output=True,
                )
            ),
        )


class _ClosureInputItems(_SocketItemFactory):
    """Typed factories for closure inputs; each declares an input item and
    returns the socket read inside the closure body.

    Both item collections live on the output node. Sockets are found by
    identifier prefix and collection position, never by list position.
    """

    _owner: "ClosureZone"

    def _declare(
        self, name: str, type: str, structure_type: _SocketShapeStructureType
    ) -> SocketLinker:
        zone = self._owner
        items = zone.output.node.input_items
        item = items.new(type, name)  # ty: ignore[invalid-argument-type]
        if structure_type != "AUTO":
            item.structure_type = structure_type
        return _wrap_socket(
            _socket_for_item(zone.input.node, items, "Item_", item, output=True)
        )


class _ClosureOutputItems(_SocketItemFactory):
    """Typed factories for closure outputs; each declares an output item
    and returns the target to feed with ``>>``."""

    _owner: "ClosureZone"

    def _declare(
        self, name: str, type: str, structure_type: _SocketShapeStructureType
    ) -> SocketLinker:
        zone = self._owner
        items = zone.output.node.output_items
        item = items.new(type, name)  # ty: ignore[invalid-argument-type]
        if structure_type != "AUTO":
            item.structure_type = structure_type
        return _wrap_socket(_socket_for_item(zone.output.node, items, "Item_", item))


class ClosureZone(_ZonePair):
    input: "ClosureInput"
    output: "ClosureOutput"

    def __init__(
        self,
    ):
        self.input = ClosureInput()
        self.output = ClosureOutput()
        self._pair()
        self.input._establish_links()

    @property
    def inputs(self) -> _ClosureInputItems:
        """Typed factories for the closure's input items."""
        return _ClosureInputItems(self)

    @property
    def outputs(self) -> _ClosureOutputItems:
        """Typed factories for the closure's output items."""
        return _ClosureOutputItems(self)

    def input_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Declare a closure input and return the socket to read in the body.

        ``type`` is a socket-type string (``"GEOMETRY"``, ``"MATRIX"``,
        ``"VECTOR"``, …); the typed factories on :attr:`inputs` are the
        static-typed equivalent.
        """
        return _ClosureInputItems(self)._declare(name, type, "AUTO")

    def output_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Declare a closure output and return the target to feed with ``>>``.

        The typed factories on :attr:`outputs` are the static-typed
        equivalent.
        """
        return _ClosureOutputItems(self)._declare(name, type, "AUTO")

    @property
    def closure(self) -> ClosureSocket:
        """The closure produced by the zone."""
        return self.output.o.closure


_ClosureItemCollections = Union[
    NodeClosureInputItems,
    NodeClosureOutputItems,
    NodeEvaluateClosureInputItems,
    NodeEvaluateClosureOutputItems,
    NodeEvaluateClosureOutputItems,
]


def _sync_closure_items(
    source: _ClosureItemCollections, target: _ClosureItemCollections
) -> None:
    target.clear()
    for source_item in source:
        item = target.new(source_item.socket_type, source_item.name)
        item.structure_type = source_item.structure_type


class ClosureInput(BaseNode):
    """
    Closure Input node
    """

    _bl_idname = "NodeClosureInput"
    node: NodeClosureInput

    class _Inputs(SocketAccessor):
        pass

    class _Outputs(SocketAccessor):
        pass

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    def link(self, target: _SocketLike) -> SocketLinker:
        self.tree.link(self.node.outputs[-1], target.socket)
        return _wrap_socket(self.node.outputs[-2])


class ClosureOutput(BaseNode):
    """
    Closure Output node

    Outputs
    -------
    o.closure : ClosureSocket
        Closure
    """

    _bl_idname = "NodeClosureOutput"
    node: NodeClosureOutput

    class _Inputs(SocketAccessor):
        pass

    class _Outputs(SocketAccessor):
        closure: ClosureSocket
        """Closure"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        define_signature: bool = False,
    ):
        super().__init__()
        key_args = {}
        self.define_signature = define_signature
        self._establish_links(**key_args)

    def link(self, source: _SocketLike) -> SocketLinker:
        self.tree.link(source.socket, self.node.inputs[-1])

        return _wrap_socket(self.node.inputs[-2])

    def sync_signature(self, node: "EvaluateClosure") -> None:
        for name in ["input_items", "output_items"]:
            _sync_closure_items(getattr(node.node, name), getattr(self.node, name))
