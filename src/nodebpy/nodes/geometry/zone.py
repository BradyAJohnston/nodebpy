from abc import ABC
from collections.abc import Iterable, Iterator, Mapping
from typing import TYPE_CHECKING, ClassVar, TypeVar, cast

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

from ...builder import (
    BaseNode,
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
    Item,
    ItemsMixin,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    SoundSocket,
    StringSocket,
    VectorSocket,
)
from ...builder import Socket as SocketLinker
from ...builder._registry import _wrap_socket
from ...builder._utils import _SocketLike
from ...builder.accessor import SocketAccessor
from ...builder.items import (
    _chained,
    _deprecated,
    _FieldItems,
    _socket_for_item,
    _SocketItems,
    _ValueItems,
)
from ...types import (
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
    _AttributeDomains,
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

    ``initial`` and ``next`` are the link targets; ``>> item.initial``
    continues the chain from ``current`` and ``>> item.next`` from
    ``result``, so a zone body can be written as one chain::

        g.Cube() >> geo.initial >> g.SetShadeSmooth() >> geo.next >> out

    The type parameter is the socket class every role returns; the typed
    methods on ``zone.items`` produce parameterised handles such as
    ``ZoneItem[GeometrySocket]``.
    """

    _items: "_StateZoneItems"

    @property
    def initial(self) -> _SocketT:
        """Input-node input socket — set the item's starting value."""
        socket = self._items._zone.input._item_socket(self._item)
        return cast("_SocketT", _chained(socket, True, lambda: self.current))

    @property
    def current(self) -> _SocketT:
        """Input-node output socket — read the item inside the zone body."""
        socket = self._items._zone.input._item_socket(self._item, output=True)
        return cast("_SocketT", _wrap_socket(socket))

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

    def __getitem__(self, index: int) -> BaseNode:
        match index:
            case 0:
                return self.input
            case 1:
                return self.output
            case _:
                raise IndexError(f"{type(self).__name__} has only two items")

    def __iter__(self) -> Iterator[BaseNode]:
        return iter((self.input, self.output))


class _StateZone(_ZonePair):
    """Zone wrapper for zones with shared state items (simulation/repeat)."""

    input: BaseZoneInput
    output: BaseZoneOutput

    if TYPE_CHECKING:

        @property
        def items(self) -> "_StateZoneItems": ...

    def _init_items(
        self, items: Mapping[str, InputAny] | Iterable[InputAny] | None
    ) -> None:
        self.output._items.clear()
        self.items._add_all(items)

    def item(
        self,
        name: str,
        initial: InputAny = None,
        *,
        type: str | None = None,
    ) -> ZoneItem:
        """Deprecated: use ``zone.items.new(initial, name, type=)``."""
        _deprecated("zone.item(name, initial)", "zone.items.new(initial, name)")
        if type is None:
            declared = self.output._declared_item_type(initial)
            if declared is not None:
                type, initial = declared, None
        return self.items.new(initial, name, type=type)


class _StateZoneItems(_ValueItems[ZoneItem]):
    """The state items of a simulation/repeat zone.

    Each typed method declares one state item and returns its
    :class:`ZoneItem` handle parameterised with the matching socket
    class, so ``initial``/``current``/``next``/``result`` are statically
    typed. ``initial`` may be a linkable (linked as the starting value,
    and naming the item) or a plain default value; omit it to declare the
    item unlinked.
    """

    _handle_type = ZoneItem

    def __init__(self, zone: _StateZone):
        super().__init__(zone.output)
        self._zone = zone

    def _entry_socket(self, handle: Item) -> bpy.types.NodeSocket:
        return cast("ZoneItem", handle).initial.socket

    def float(
        self, initial: InputFloat = None, name: str | None = None
    ) -> "ZoneItem[FloatSocket]":
        return self._typed(initial, name, "FLOAT")

    def integer(
        self, initial: InputInteger = None, name: str | None = None
    ) -> "ZoneItem[IntegerSocket]":
        return self._typed(initial, name, "INT")

    def boolean(
        self, initial: InputBoolean = None, name: str | None = None
    ) -> "ZoneItem[BooleanSocket]":
        return self._typed(initial, name, "BOOLEAN")

    def vector(
        self, initial: InputVector = None, name: str | None = None
    ) -> "ZoneItem[VectorSocket]":
        return self._typed(initial, name, "VECTOR")

    def color(
        self, initial: InputColor = None, name: str | None = None
    ) -> "ZoneItem[ColorSocket]":
        return self._typed(initial, name, "RGBA")

    def rotation(
        self, initial: InputRotation = None, name: str | None = None
    ) -> "ZoneItem[RotationSocket]":
        return self._typed(initial, name, "ROTATION")

    def matrix(
        self, initial: InputMatrix = None, name: str | None = None
    ) -> "ZoneItem[MatrixSocket]":
        return self._typed(initial, name, "MATRIX")

    def string(
        self, initial: InputString = None, name: str | None = None
    ) -> "ZoneItem[StringSocket]":
        return self._typed(initial, name, "STRING")

    def geometry(
        self, initial: InputGeometry = None, name: str | None = None
    ) -> "ZoneItem[GeometrySocket]":
        return self._typed(initial, name, "GEOMETRY")

    def bundle(
        self, initial: InputBundle = None, name: str | None = None
    ) -> "ZoneItem[BundleSocket]":
        return self._typed(initial, name, "BUNDLE")


class _SimulationZoneItems(_StateZoneItems):
    """The simulation zone's state items."""


class _RepeatZoneItems(_StateZoneItems):
    """The repeat zone's state items, including the datablock and closure
    types only the repeat zone supports."""

    def object(
        self, initial: InputObject = None, name: str | None = None
    ) -> "ZoneItem[ObjectSocket]":
        return self._typed(initial, name, "OBJECT")

    def image(
        self, initial: InputImage = None, name: str | None = None
    ) -> "ZoneItem[ImageSocket]":
        return self._typed(initial, name, "IMAGE")

    def collection(
        self, initial: InputCollection = None, name: str | None = None
    ) -> "ZoneItem[CollectionSocket]":
        return self._typed(initial, name, "COLLECTION")

    def material(
        self, initial: InputMaterial = None, name: str | None = None
    ) -> "ZoneItem[MaterialSocket]":
        return self._typed(initial, name, "MATERIAL")

    def closure(
        self, initial: InputClosure = None, name: str | None = None
    ) -> "ZoneItem[ClosureSocket]":
        return self._typed(initial, name, "CLOSURE")

    def font(
        self, initial: InputFont = None, name: str | None = None
    ) -> "ZoneItem[FontSocket]":
        return self._typed(initial, name, "FONT")

    def sound(
        self, initial: InputSound = None, name: str | None = None
    ) -> "ZoneItem[SoundSocket]":
        return self._typed(initial, name, "SOUND")


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
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}


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

    def __init__(
        self, items: Mapping[str, InputAny] | Iterable[InputAny] | None = None
    ):
        self.input = SimulationInput()
        self.output = SimulationOutput()
        self._pair()
        self._init_items(items)

    @property
    def items(self) -> _SimulationZoneItems:
        """The zone's state items."""
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
        "FONT",
        "SOUND",
    )

    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}


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
        items: Mapping[str, InputAny] | Iterable[InputAny] | None = None,
    ):
        self.input = RepeatInput()
        self.output = RepeatOutput()
        self._pair()
        self.input._establish_links(Iterations=iterations)
        self._init_items(items)

    @property
    def items(self) -> _RepeatZoneItems:
        """The zone's state items."""
        return _RepeatZoneItems(self)

    @property
    def iteration(self) -> IntegerSocket:
        """The current iteration index."""
        return self.input.o.iteration


class _ForEachItems(_FieldItems):
    """The for-each zone's input items — per-element fields made available
    inside the zone body. ``input`` feeds the field, ``output`` reads the
    per-element value in the body."""

    def menu(
        self, value: InputMenu = None, name: str | None = None
    ) -> "Item[MenuSocket]":
        return self._typed(value, name, "MENU")


class _ForEachMainItems(_FieldItems):
    """The for-each zone's main items — per-element results written back
    onto the input geometry. ``input`` is the ``>>`` target inside the
    body, ``output`` the combined result."""


class _ForEachGeneratedItems(_ValueItems[Item]):
    """The for-each zone's generation items — values stored on the
    generated geometry, evaluated on ``domain``. ``input`` is the ``>>``
    target inside the body, ``output`` the stored result."""

    _collection = "generation_items"
    _prefix = "Generation_"
    _value_types = (
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "GEOMETRY",
    )

    def float(
        self,
        value: InputFloat = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[FloatSocket]":
        return self._typed(value, name, "FLOAT", domain=domain)

    def integer(
        self,
        value: InputInteger = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[IntegerSocket]":
        return self._typed(value, name, "INT", domain=domain)

    def boolean(
        self,
        value: InputBoolean = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[BooleanSocket]":
        return self._typed(value, name, "BOOLEAN", domain=domain)

    def vector(
        self,
        value: InputVector = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[VectorSocket]":
        return self._typed(value, name, "VECTOR", domain=domain)

    def color(
        self,
        value: InputColor = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[ColorSocket]":
        return self._typed(value, name, "RGBA", domain=domain)

    def rotation(
        self,
        value: InputRotation = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[RotationSocket]":
        return self._typed(value, name, "ROTATION", domain=domain)

    def matrix(
        self,
        value: InputMatrix = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[MatrixSocket]":
        return self._typed(value, name, "MATRIX", domain=domain)

    def geometry(
        self,
        value: InputGeometry = None,
        name: str | None = None,
        *,
        domain: _AttributeDomains = "POINT",
    ) -> "Item[GeometrySocket]":
        return self._typed(value, name, "GEOMETRY", domain=domain)


class ForEachGeometryElementZone(_ZonePair):
    input: "ForEachGeometryElementInput"
    output: "ForEachGeometryElementOutput"

    class _DomainFactory:
        def __init__(self, domain: _AttributeDomains):
            self._domain = domain

        def __call__(
            self, geometry: InputGeometry = None, selection: InputBoolean = True
        ) -> "ForEachGeometryElementZone":
            """Create a for-each zone iterating over a pre-set domain."""
            return ForEachGeometryElementZone(geometry, selection, domain=self._domain)

    point: _DomainFactory = _DomainFactory("POINT")
    edge: _DomainFactory = _DomainFactory("EDGE")
    face: _DomainFactory = _DomainFactory("FACE")
    corner: _DomainFactory = _DomainFactory("CORNER")
    curve: _DomainFactory = _DomainFactory("CURVE")
    instance: _DomainFactory = _DomainFactory("INSTANCE")
    layer: _DomainFactory = _DomainFactory("LAYER")

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
    def items(self) -> _ForEachItems:
        """Per-element input items, read inside the body."""
        return _ForEachItems(self.input)

    @property
    def main_items(self) -> _ForEachMainItems:
        """Main items: per-element results written back onto the geometry."""
        return _ForEachMainItems(self.output)

    @property
    def generated_items(self) -> _ForEachGeneratedItems:
        """Generation items: values stored on the generated geometry."""
        return _ForEachGeneratedItems(self.output)

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
        return cast("Item[GeometrySocket]", self.generated_items[0])

    # -- deprecated entry points, removed in 530 --

    @property
    def inputs(self) -> _ForEachItems:
        _deprecated("zone.inputs", "zone.items")
        return self.items

    @property
    def main(self) -> _ForEachMainItems:
        _deprecated("zone.main", "zone.main_items")
        return self.main_items

    @property
    def generated(self) -> _ForEachGeneratedItems:
        _deprecated("zone.generated", "zone.generated_items")
        return self.generated_items

    def item(
        self, name: str, value: InputLinkable = None, *, type: str | None = None
    ) -> Item:
        _deprecated("zone.item(name, value)", "zone.items.new(value, name)")
        return self.items.new(value, name, type=type)

    def main_item(
        self, name: str, value: InputLinkable = None, *, type: str | None = None
    ) -> Item:
        _deprecated("zone.main_item(name, value)", "zone.main_items.new(value, name)")
        return self.main_items.new(value, name, type=type)

    def generated_item(
        self,
        name: str,
        value: InputLinkable = None,
        *,
        type: str | None = None,
        domain: _AttributeDomains = "POINT",
    ) -> Item:
        _deprecated(
            "zone.generated_item(name, value)",
            "zone.generated_items.<type>(value, name)",
        )
        return self.generated_items._declare(value, name, type, domain=domain)


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
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

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
    _type_map: ClassVar[dict[str, str]] = {"VALUE": "FLOAT"}

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
        **kwargs: InputAny,
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
        """Deprecated: use ``zone.generated_items.<type>(value, name)``."""
        _deprecated(
            "add_generated_item(name, value)",
            "zone.generated_items.<type>(value, name)",
        )
        return _ForEachGeneratedItems(self)._declare(value, name, type, domain=domain)

    def capture_generated(
        self,
        value: InputLinkable,
        *,
        name: str | None = None,
        domain: _AttributeDomains = "POINT",
    ) -> SocketLinker:
        """Deprecated: use ``zone.generated_items.<type>(value, name).output``."""
        _deprecated(
            "capture_generated(value)",
            "zone.generated_items.<type>(value, name).output",
        )
        return (
            _ForEachGeneratedItems(self)
            ._declare(value, name, None, domain=domain)
            .output
        )

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ) -> None:
        self.node.domain = value


class _ClosureInputItems(_SocketItems):
    """The closure's input items; ``output`` is the socket read inside the
    body (the item has no input socket).

    Both item collections live on the output node. Sockets are found by
    identifier prefix and collection position, never by list position.
    """

    _collection = "input_items"
    _has_input = False

    def __init__(self, zone: "ClosureZone"):
        super().__init__(zone.output)
        self._zone = zone

    @property
    def _bpy(self):
        return self._zone.output.node.input_items

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(
            self._zone.input.node, self._bpy, "Item_", item, output=True
        )


class _ClosureOutputItems(_SocketItems):
    """The closure's output items; ``input`` is the target to feed with
    ``>>`` (the item has no output socket)."""

    _collection = "output_items"
    _has_output = False

    def __init__(self, zone: "ClosureZone"):
        super().__init__(zone.output)
        self._zone = zone

    @property
    def _bpy(self):
        return self._zone.output.node.output_items

    def _item_socket(self, item, *, output: bool = False) -> bpy.types.NodeSocket:
        return _socket_for_item(self._zone.output.node, self._bpy, "Item_", item)


class ClosureZone(_ZonePair):
    input: "ClosureInput"
    output: "ClosureOutput"

    def __init__(self) -> None:
        self.input = ClosureInput()
        self.output = ClosureOutput()
        self._pair()
        self.input._establish_links()

    @property
    def inputs(self) -> _ClosureInputItems:
        """The closure's input items."""
        return _ClosureInputItems(self)

    @property
    def outputs(self) -> _ClosureOutputItems:
        """The closure's output items."""
        return _ClosureOutputItems(self)

    def input_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Deprecated: use ``zone.inputs.new(name, type=type).output``."""
        _deprecated("input_item(name, type)", "inputs.new(name, type=type).output")
        return self.inputs.new(name, type=type).output

    def output_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Deprecated: use ``zone.outputs.new(name, type=type).input``."""
        _deprecated("output_item(name, type)", "outputs.new(name, type=type).input")
        return self.outputs.new(name, type=type).input

    @property
    def closure(self) -> ClosureSocket:
        """The closure produced by the zone."""
        return self.output.o.closure


_ClosureItemCollections = (
    NodeClosureInputItems
    | NodeClosureOutputItems
    | NodeEvaluateClosureInputItems
    | NodeEvaluateClosureOutputItems
)


def _sync_closure_items(
    source: _ClosureItemCollections, target: _ClosureItemCollections
) -> None:
    target.clear()
    for source_item in source:
        item = target.new(source_item.socket_type, source_item.name)
        assert item is not None
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

    def __init__(self) -> None:
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
