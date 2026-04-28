from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Union

import bpy
from bpy.types import (
    NodeClosureInput,
    NodeClosureInputItems,
    NodeClosureOutput,
    NodeClosureOutputItems,
    NodeEvaluateClosureInputItems,
    NodeEvaluateClosureOutputItems,
    NodeSocket,
)

from nodebpy.builder._utils import _SocketLike

if TYPE_CHECKING:
    from .manual import EvaluateClosure

from nodebpy.builder import BaseNode as NodeBuilder
from nodebpy.builder import ClosureSocket, DynamicInputsMixin
from nodebpy.builder import Socket as SocketLinker
from nodebpy.builder.accessor import SocketAccessor

from ...types import (
    InputBoolean,
    InputGeometry,
    InputInteger,
    InputLinkable,
    _AttributeDomains,
    _BakeDataTypes,
)


class BaseZone(DynamicInputsMixin, NodeBuilder, ABC):
    @property
    @abstractmethod
    def _items_node(
        self,
    ) -> bpy.types.GeometryNodeRepeatOutput | bpy.types.GeometryNodeSimulationOutput:
        """Return the items node (state_node, repeat_node, etc.)"""
        pass

    @property
    @abstractmethod
    def items(
        self,
    ) -> (
        bpy.types.NodeGeometryRepeatOutputItems
        | bpy.types.NodeGeometrySimulationOutputItems
    ):
        """Return the items collection"""
        pass

    def capture(
        self, value: InputLinkable, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        return SocketLinker(self.node.outputs[-2])


class BaseZoneInput(BaseZone, NodeBuilder, ABC):
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

    def _add_socket(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items.new(type, name)
        return self.inputs[item.name]


class BaseZoneOutput(BaseZone, NodeBuilder, ABC):
    """Base class for zone output nodes"""

    node: bpy.types.GeometryNodeSimulationOutput | bpy.types.GeometryNodeRepeatOutput

    @property
    def _items_node(
        self,
    ) -> bpy.types.GeometryNodeRepeatOutput | bpy.types.GeometryNodeSimulationOutput:
        return self.node

    def _add_socket(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items.new(type, name)
        return self.node.inputs[item.name]


class BaseSimulationZone(BaseZone):
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

    @property
    def items(self) -> bpy.types.NodeGeometrySimulationOutputItems:
        return self._items_node.state_items  # type: ignore


class SimulationInput(BaseSimulationZone, BaseZoneInput):
    """Simulation Input node"""

    _bl_idname = "GeometryNodeSimulationInput"
    node: bpy.types.GeometryNodeSimulationInput

    class _Outputs(SocketAccessor):
        delta_time: SocketLinker
        """Time elapsed since the previous simulation frame."""

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...


class SimulationOutput(BaseSimulationZone, BaseZoneOutput):
    """Simulation Output node"""

    _bl_idname = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    class _Inputs(SocketAccessor):
        skip: SocketLinker
        """Skip the simulation for this frame."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...


class SimulationZone:
    def __init__(self, *args: InputLinkable, **kwargs: InputLinkable):
        self.input = SimulationInput()
        self.output = SimulationOutput()
        self.input.node.pair_with_output(self.output.node)

        self.output.node.state_items.clear()
        socket_lookup = self.output._add_inputs(*args, **kwargs)
        for name, source in socket_lookup.items():
            self.input._link_from(source, name)

    @property
    def delta_time(self) -> SocketLinker:
        return self.input.o.delta_time

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.input
            case 1:
                return self.output
            case _:
                raise IndexError("SimulationZone has only two items")


class BaseRepeatZone(BaseZone):
    _socket_data_types = (
        "FLOAT",
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

    @property
    def items(self) -> bpy.types.NodeGeometryRepeatOutputItems:
        return self._items_node.repeat_items  # type: ignore


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


class RepeatZone:
    """Wrapper that supports both direct unpacking and iteration"""

    def __init__(
        self,
        iterations: InputInteger = 1,
        *args: InputLinkable,
        **kwargs: InputLinkable,
    ):
        self.input = RepeatInput(iterations)
        self.output = RepeatOutput()
        self.input.node.pair_with_output(self.output.node)

        self.output.node.repeat_items.clear()
        self.input._establish_links(**self.input._add_inputs(*args, **kwargs))

    @property
    def i(self) -> SocketLinker:
        """The current iteration index."""
        return self.input.o.iteration

    def __iter__(self):
        """Support for loop: for i, input, output in RepeatZone(...)"""
        self._index = 0
        return self

    def __next__(self):
        """Support for iteration: next(RepeatZone)"""
        if self._index > 0:
            raise StopIteration
        self._index += 1
        return self.i, self.input, self.output


class ForEachGeometryElementZone:
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

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.input
            case 1:
                return self.output
            case _:
                raise IndexError("ForEachZone has only two items")


class ForEachGeometryElementInput(BaseZoneInput):
    """For Each Geometry Element Input node"""

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

    def __init__(self, geometry: InputGeometry = None, selection: InputBoolean = True):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self._establish_links(**key_args)

    def capture(
        self, value: InputLinkable, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        new_output_idx = [o.identifier for o in self.node.outputs].index(
            "__extend__"
        ) - 1
        output = self.node.outputs[new_output_idx]

        return SocketLinker(output)

    @property
    def items(self) -> bpy.types.NodeGeometryForeachGeometryElementInputItems:
        return self.output.input_items

    class _Inputs(SocketAccessor):
        geometry: SocketLinker
        """The geometry to iterate over."""
        selection: SocketLinker
        """Limits which elements are iterated over."""

    class _Outputs(SocketAccessor):
        index: SocketLinker
        """The index of the current element."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...


class ForEachGeometryElementOutput(BaseZoneOutput):
    """For Each Geometry Element Output node"""

    _socket_data_types = [
        "VALUE",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
    ]
    _type_map = {"VALUE": "FLOAT"}

    _bl_idname = "GeometryNodeForeachGeometryElementOutput"
    node: bpy.types.GeometryNodeForeachGeometryElementOutput

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
    def items(self) -> bpy.types.NodeGeometryForeachGeometryElementMainItems:
        return self.node.main_items

    @property
    def items_generated(
        self,
    ) -> bpy.types.NodeGeometryForeachGeometryElementGenerationItems:
        return self.node.generation_items

    def _latest(
        self, suffix: str, sockets: Iterable[bpy.types.NodeSocket]
    ) -> bpy.types.NodeSocket:
        idx = [o.identifier for o in sockets].index(f"__extend__{suffix}") - 1
        return sockets[idx]

    def capture(
        self, value: InputLinkable, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        return SocketLinker(self._latest("main", self.node.outputs))

    def capture_generated(self, value: InputLinkable) -> SocketLinker:
        self._socket_data_types = tuple(list(self._socket_data_types) + ["GEOMETRY"])
        self._add_socket = self._add_socket_generated
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        self._socket_data_types = tuple(
            [x for x in self._socket_data_types if x != "GEOMETRY"]
        )
        self._add_socket = self._add_socket_main
        return SocketLinker(self._latest("generation", self.node.outputs))

    def _add_socket_main(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        _ = self.items.new(type, name)
        return self._latest("main", self.node.inputs)

    def _add_socket_generated(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        _ = self.items_generated.new(type, name)
        return self._latest("generation", self.node.inputs)

    class _Inputs(SocketAccessor):
        generation_0: SocketLinker
        """The geometry to generate elements from."""

    class _Outputs(SocketAccessor):
        geometry: SocketLinker
        """The output geometry after processing all elements."""
        generation_0: SocketLinker
        """The generated geometry output."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

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


class ClosureZone:
    def __init__(
        self,
    ):
        self.input = ClosureInput()
        self.output = ClosureOutput()
        self.input.node.pair_with_output(self.output.node)
        self.input._establish_links()

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.input
            case 1:
                return self.output
            case _:
                raise IndexError("ClosureZone has only two items")


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


class ClosureInput(NodeBuilder):
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

    def link(self, target: _SocketLike) -> NodeSocket:
        self.tree.link(self.node.outputs[-1], target.socket)
        return self.node.outputs[-2]


class ClosureOutput(NodeBuilder):
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

    def link(self, source: _SocketLike) -> NodeSocket:
        self.tree.link(source.socket, self.node.inputs[-1])
        return self.node.inputs[-2]

    def sync_signature(self, node: "EvaluateClosure") -> None:
        for name in ["input_items", "output_items"]:
            _sync_closure_items(getattr(node, name), getattr(self.node, name))
