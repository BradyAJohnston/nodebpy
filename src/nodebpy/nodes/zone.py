from abc import ABC, abstractmethod
from typing import Literal

import bpy
from bpy.types import NodeSocket

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    _AttributeDomains,
    _BakeDataTypes,
)


class BaseZone(NodeBuilder, ABC):
    _items_attribute: Literal["state_items", "repeat_items"]

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
    ) -> bpy.types.GeometryNodeSimulationOutput | bpy.types.GeometryNodeRepeatOutput:
        return self.node.paired_output  # type: ignore

    def _add_socket(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items.new(type, name)
        return self.inputs[item.name]

    def __rshift__(self, other):
        """Custom zone input linking that creates sockets as needed"""
        # Check if target is a zone output without inputs
        if (
            hasattr(other, "_default_input_socket")
            and other._default_input_socket is None
        ):
            # Target zone needs a socket - create one based on our output
            from ..builder import SOCKET_COMPATIBILITY

            source_socket = self._default_output_socket
            source_type = source_socket.type

            compatible_types = SOCKET_COMPATIBILITY.get(source_type, [source_type])
            best_type = compatible_types[0] if compatible_types else source_type

            # Create socket on target zone
            target_socket = other._add_socket(name=best_type.title(), type=best_type)
            self.tree.link(source_socket, target_socket)
            return other
        else:
            # Use the general smart linking approach
            return self._smart_link_to(other)


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

    def __rshift__(self, other):
        """Custom zone output linking that creates sockets as needed"""
        from ..builder import SOCKET_COMPATIBILITY

        # Get the source socket type
        source_socket = self._default_output_socket
        source_type = source_socket.type

        # Check if target has compatible inputs
        if hasattr(other, "_default_input_socket") and other._default_input_socket:
            # Normal linking
            return super().__rshift__(other)
        elif hasattr(other, "_add_socket"):
            # Target is also a zone - create compatible socket
            compatible_types = SOCKET_COMPATIBILITY.get(source_type, [source_type])
            best_type = compatible_types[0] if compatible_types else source_type

            # Create socket on target zone
            target_socket = other._add_socket(name=best_type.title(), type=best_type)
            self.tree.link(source_socket, target_socket)
            return other
        else:
            # Normal NodeBuilder
            return super().__rshift__(other)

    @property
    def _default_input_socket(self) -> NodeSocket:
        """Get default input socket, avoiding skip-type sockets"""
        inputs = list(self.inputs.values())
        if inputs:
            return inputs[0].socket
        else:
            # No socket exists - this should be handled by zone-specific __rshift__ logic
            # Return None to signal that a socket needs to be created
            return None


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


class BaseSimulationZone(BaseZone):
    _items_attribute = "state_items"

    @property
    def items(self) -> bpy.types.NodeGeometrySimulationOutputItems:
        return self._items_node.state_items  # type: ignore


class SimulationInput(BaseSimulationZone, BaseZoneInput):
    """Simulation Input node"""

    name = "GeometryNodeSimulationInput"
    node: bpy.types.GeometryNodeSimulationInput

    @property
    def o_delta_time(self) -> SocketLinker:
        """Output socket: Delta Time"""
        return self._output("Delta Time")


class SimulationOutput(BaseSimulationZone, BaseZoneOutput):
    """Simulation Output node"""

    name = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    @property
    def i_skip(self) -> SocketLinker:
        """Input socket: Skip simluation frame"""
        return self._input("Skip")


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


class BaseRepeatZone(BaseZone):
    _items_attribute = "repeat_items"

    @property
    def items(self) -> bpy.types.NodeGeometryRepeatOutputItems:
        return self._items_node.repeat_items  # type: ignore


class RepeatInput(BaseRepeatZone, BaseZoneInput):
    """Repeat Input node"""

    name = "GeometryNodeRepeatInput"
    node: bpy.types.GeometryNodeRepeatInput

    def __init__(self, iterations: TYPE_INPUT_INT = 1):
        super().__init__()
        key_args = {"Iterations": iterations}
        self._establish_links(**key_args)

    @property
    def o_iteration(self) -> SocketLinker:
        """Output socket: Iteration"""
        return self._output("Iteration")

    @property
    def output_node(self) -> bpy.types.GeometryNodeRepeatOutput:
        zone_output = self.node.paired_output  # type: ignore
        assert zone_output is not None
        return zone_output  # type: ignore


class RepeatOutput(BaseRepeatZone, BaseZoneOutput):
    """Repeat Output node"""

    name = "GeometryNodeRepeatOutput"
    node: bpy.types.GeometryNodeRepeatOutput


class ForEachGeometryElementInput(NodeBuilder):
    """For Each Geometry Element Input node"""

    name = "GeometryNodeForeachGeometryElementInput"
    node: bpy.types.GeometryNodeForeachGeometryElementInput

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        extend: LINKABLE | None = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "__extend__": extend}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__")


class ForEachGeometryElementOutput(NodeBuilder):
    """For Each Geometry Element Output node"""

    name = "GeometryNodeForeachGeometryElementOutput"
    node: bpy.types.GeometryNodeForeachGeometryElementOutput

    def __init__(
        self,
        extend_main: LINKABLE | None = None,
        generation_0: LINKABLE = None,
        extend_generation: LINKABLE | None = None,
        active_input_index: int = 0,
        active_generation_index: int = 0,
        active_main_index: int = 0,
        domain: _AttributeDomains = "POINT",
        inspection_index: int = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "__extend__main": extend_main,
            "Generation_0": generation_0,
            "__extend__generation": extend_generation,
        }
        key_args.update(kwargs)
        self.active_input_index = active_input_index
        self.active_generation_index = active_generation_index
        self.active_main_index = active_main_index
        self.domain = domain
        self.inspection_index = inspection_index
        self._establish_links(**key_args)

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__main")

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Generation_0")

    @property
    def i_extend_generation(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__generation")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__main")

    @property
    def o_generation_0(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Generation_0")

    @property
    def o_extend_generation(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__generation")

    @property
    def active_input_index(self) -> int:
        return self.node.active_input_index

    @active_input_index.setter
    def active_input_index(self, value: int):
        self.node.active_input_index = value

    @property
    def active_generation_index(self) -> int:
        return self.node.active_generation_index

    @active_generation_index.setter
    def active_generation_index(self, value: int):
        self.node.active_generation_index = value

    @property
    def active_main_index(self) -> int:
        return self.node.active_main_index

    @active_main_index.setter
    def active_main_index(self, value: int):
        self.node.active_main_index = value

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

    @property
    def inspection_index(self) -> int:
        return self.node.inspection_index

    @inspection_index.setter
    def inspection_index(self, value: int):
        self.node.inspection_index = value
