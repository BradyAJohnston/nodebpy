from abc import ABC, abstractmethod

import bpy

from nodebpy.builder import DynamicInputsMixin, NodeBuilder, SocketLinker

from ..types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
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

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        """Get all output sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.outputs[item.name]) for item in self.items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        """Get all input sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.inputs[item.name]) for item in self.items
        }

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        return SocketLinker(self.node.outputs[-2])


class BaseZoneInput(BaseZone, NodeBuilder, ABC):
    """Base class for zone input nodes"""

    node: bpy.types.GeometryNodeSimulationInput | bpy.types.GeometryNodeRepeatInput

    @property
    def _items_node(self):  # type: ignore
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

    @property
    def o_delta_time(self) -> SocketLinker:
        """Output socket: Delta Time"""
        return self._output("Delta Time")


class SimulationOutput(BaseSimulationZone, BaseZoneOutput):
    """Simulation Output node"""

    _bl_idname = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    @property
    def i_skip(self) -> SocketLinker:
        """Input socket: Skip simluation frame"""
        return self._input("Skip")


class SimulationZone:
    def __init__(self, *args: LINKABLE, **kwargs: LINKABLE):
        self.input = SimulationInput()
        self.output = SimulationOutput()
        self.input.node.pair_with_output(self.output.node)

        self.output.node.state_items.clear()
        socket_lookup = self.output._add_inputs(*args, **kwargs)
        for name, source in socket_lookup.items():
            self.input._link_from(source, name)

    def delta_time(self) -> SocketLinker:
        return self.input.o_delta_time

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

    def __init__(self, iterations: TYPE_INPUT_INT = 1):
        super().__init__()
        key_args = {"Iterations": iterations}
        self._establish_links(**key_args)

    @property
    def o_iteration(self) -> SocketLinker:
        """Output socket: Iteration"""
        return self._output("Iteration")


class RepeatOutput(BaseRepeatZone, BaseZoneOutput):
    """Repeat Output node"""

    _bl_idname = "GeometryNodeRepeatOutput"
    node: bpy.types.GeometryNodeRepeatOutput


class RepeatZone:
    """Wrapper that supports both direct unpacking and iteration"""

    def __init__(
        self, iterations: TYPE_INPUT_INT = 1, *args: LINKABLE, **kwargs: LINKABLE
    ):
        self.input = RepeatInput(iterations)
        self.output = RepeatOutput()
        self.input.node.pair_with_output(self.output.node)

        self.output.node.repeat_items.clear()
        self.input._establish_links(**self.input._add_inputs(*args, **kwargs))

    @property
    def i(self) -> SocketLinker:
        """Input socket: Skip simluation frame"""
        return self.input.o_iteration

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
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        domain: _AttributeDomains = "POINT",
    ):
        self.input = ForEachGeometryElementInput()
        self.output = ForEachGeometryElementOutput()
        self.input.node.pair_with_output(self.output.node)
        self.output.domain = domain
        self.input._establish_links(Geometry=geometry, Selection=selection)

    def index(self) -> SocketLinker:
        return self.input.o_index

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

    def __init__(
        self, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self._establish_links(**key_args)

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        return SocketLinker(self.node.outputs[-2])

    @property
    def output(self) -> bpy.types.GeometryNodeForeachGeometryElementOutput:
        return self.node.paired_output  # type: ignore

    @property
    def items(self) -> bpy.types.NodeGeometryForeachGeometryElementInputItems:
        return self.output.input_items

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")


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

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an input to the simulation"""
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        # we have to do a convoluted lookup to get the most recently added socket
        new_output_idx = [o.identifier for o in self.node.outputs].index(
            "__extend__main"
        ) - 1
        return SocketLinker(self.node.outputs[new_output_idx])

    def capture_generated(self, value: LINKABLE) -> SocketLinker:
        self._socket_data_types = self._socket_data_types + ["GEOMETRY"]
        self._add_socket = self._add_socket_generated
        item_dict = self._add_inputs(value)
        self._establish_links(**item_dict)
        self._socket_data_types = list(
            [x for x in self._socket_data_types if x != "GEOMETRY"]
        )
        self._add_socket = self._add_socket_main
        return SocketLinker(self.node.outputs[-2])

    def _add_socket_main(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items.new(type, name)
        return self.inputs[item.name]

    def _add_socket_generated(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items.new(type, name)
        return self.inputs[item.name]

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Generation_0")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def o_generation(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Generation_0")

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
