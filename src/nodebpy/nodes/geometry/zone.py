from abc import ABC
from typing import TYPE_CHECKING, Union, cast

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
    ClosureSocket,
    FloatSocket,
    GeometrySocket,
    IntegerSocket,
    Item,
    ItemsMixin,
)
from ...builder import Socket as SocketLinker
from ...builder._registry import _wrap_socket
from ...builder._utils import _SocketLike
from ...builder.accessor import SocketAccessor
from ...builder.items import _infer_value_type
from ...types import (
    InputAny,
    InputBoolean,
    InputGeometry,
    InputInteger,
    InputLinkable,
    _AttributeDomains,
    _is_default_value,
)


def _socket_for_item(
    node: bpy.types.Node, items, prefix: str, item, *, output: bool = False
) -> bpy.types.NodeSocket:
    """Find the node socket belonging to ``item`` by identifier prefix and
    collection position; item names are not unique across a zone node's
    fixed sockets and item collections."""
    index = next(i for i, candidate in enumerate(items) if candidate == item)
    sockets = node.outputs if output else node.inputs
    return [s for s in sockets if s.identifier.startswith(prefix)][index]


class BaseZone(ItemsMixin, BaseNode, ABC):
    # zone sockets can share names across fixed sockets and item collections,
    # so item sockets are found by identifier prefix instead of by name
    _item_identifier_prefix = "Item_"

    @property
    def items(self):
        """The bpy item collection driving this zone's sockets."""
        return self._items

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


class ZoneItem(Item):
    """Handle for a simulation/repeat state item (four sockets per item)."""

    def __init__(self, input_node: BaseZoneInput, output_node: BaseZoneOutput, item):
        super().__init__(output_node, item)
        self._input_node = input_node

    @property
    def initial(self) -> SocketLinker:
        """Input-node input socket — set the item's starting value."""
        return _wrap_socket(self._input_node._item_socket(self._item))

    @property
    def current(self) -> SocketLinker:
        """Input-node output socket — read the item inside the zone body."""
        return _wrap_socket(self._input_node._item_socket(self._item, output=True))

    @property
    def next(self) -> SocketLinker:
        """Output-node input socket — write the item's per-iteration result."""
        return self.input

    @property
    def result(self) -> SocketLinker:
        """Output-node output socket — read the item after the zone."""
        return self.output


class _ZonePair:
    """Zone wrapper holding the paired input and output builder nodes.

    Supports ``input, output = zone`` unpacking and indexing with
    ``zone[0]`` / ``zone[1]``.
    """

    input: BaseNode
    output: BaseNode

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
        self.input.node.pair_with_output(self.output.node)

        self.output.node.state_items.clear()
        for name, value in (items or {}).items():
            self.item(name, value)

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
        iteration: SocketLinker
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
        self.input.node.pair_with_output(self.output.node)
        # linked after pairing — sockets on an unpaired zone node are inactive
        self.input._establish_links(Iterations=iterations)

        self.output.node.repeat_items.clear()
        for name, value in (items or {}).items():
            self.item(name, value)

    @property
    def iteration(self) -> SocketLinker:
        """The current iteration index."""
        return self.input.o.iteration


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
        self.input.node.pair_with_output(self.output.node)
        self.output.domain = domain
        self.input._establish_links(Geometry=geometry, Selection=selection)

    @property
    def index(self) -> SocketLinker:
        return self.input.o.index

    @property
    def generation(self) -> Item:
        """Handle for the default generation item (the generated geometry)."""
        return _GenerationItem(self.output, self.output.items_generated[0])

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
        value: InputLinkable = None,
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
                value, name=name, types=self._generation_data_types
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


class _GenerationItem(Item):
    """Handle for a ForEach generation item; its sockets carry the
    ``Generation_`` identifier prefix rather than the owner's default."""

    _owner: "ForEachGeometryElementOutput"

    @property
    def _collection(self):
        return self._owner.items_generated

    @property
    def input(self) -> SocketLinker:
        return _wrap_socket(
            _socket_for_item(
                self._owner.node,
                self._owner.items_generated,
                "Generation_",
                self._item,
            )
        )

    @property
    def output(self) -> SocketLinker:
        return _wrap_socket(
            _socket_for_item(
                self._owner.node,
                self._owner.items_generated,
                "Generation_",
                self._item,
                output=True,
            )
        )


class ClosureZone(_ZonePair):
    input: "ClosureInput"
    output: "ClosureOutput"

    def __init__(
        self,
    ):
        self.input = ClosureInput()
        self.output = ClosureOutput()
        self.input.node.pair_with_output(self.output.node)
        self.input._establish_links()

    def input_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Declare a closure input and return the socket to read in the body.

        ``type`` is a socket-type string (``"GEOMETRY"``, ``"MATRIX"``,
        ``"VECTOR"``, …); the item collection lives on the output node and
        drives the matching output socket on the input node.
        """
        self.output.node.input_items.new(type, name)
        return _wrap_socket(self.input.node.outputs[-2])

    def output_item(self, name: str, type: str = "GEOMETRY") -> SocketLinker:
        """Declare a closure output and return the target to feed with ``>>``."""
        self.output.node.output_items.new(type, name)
        return _wrap_socket(self.output.node.inputs[-2])

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
