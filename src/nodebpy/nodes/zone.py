from abc import ABC, abstractmethod

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


class BaseZoneInput(NodeBuilder, ABC):
    """Base class for zone input nodes"""

    @property
    @abstractmethod
    def output_node(self):
        """Return the paired output node"""
        pass

    @property
    @abstractmethod
    def items_collection(self):
        """Return the items collection (state_items, repeat_items, etc.)"""
        pass

    def _add_socket(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items_collection.new(type, name)
        return self.output_node.inputs[item.name]

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
        elif hasattr(other, "_default_input_socket") and other._default_input_socket:
            # Check if we need to create a compatible output socket
            from ..builder import SOCKET_COMPATIBILITY
            
            source_socket = self._default_output_socket
            target_socket = other._default_input_socket
            source_type = source_socket.type
            target_type = target_socket.type
            
            # Check if source is compatible with target
            compatible_types = SOCKET_COMPATIBILITY.get(source_type, [])
            if target_type not in compatible_types:
                # Check if we already have a compatible output socket
                existing_socket = None
                for name, socket_linker in self.outputs.items():
                    socket_compatibles = SOCKET_COMPATIBILITY.get(socket_linker.socket.type, [])
                    if target_type in socket_compatibles:
                        existing_socket = socket_linker.socket
                        break
                
                if existing_socket:
                    # Use existing compatible socket
                    self.tree.link(existing_socket, target_socket)
                    return other
                else:
                    # Create new compatible output socket
                    self._add_socket(name=target_type.title(), type=target_type)
                    # Find the newly created output socket
                    for name, socket_linker in self.outputs.items():
                        if socket_linker.socket.type == target_type:
                            self.tree.link(socket_linker.socket, target_socket)
                            return other
                        
            # Normal linking - compatible sockets exist
            return super().__rshift__(other)
        else:
            # Normal linking
            return super().__rshift__(other)

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        """Get all output sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.items_collection
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        """Get all input sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.items_collection
        }



class BaseZoneOutput(NodeBuilder, ABC):
    """Base class for zone output nodes"""

    @property
    @abstractmethod
    def items_collection(self):
        """Return the items collection (state_items, repeat_items, etc.)"""
        pass

    def _add_socket(self, name: str, type: _BakeDataTypes):
        """Add a socket to the zone"""
        item = self.items_collection.new(type, name)
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

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        """Get all output sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.items_collection
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        """Get all input sockets based on items collection"""
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.items_collection
        }


def simulation_zone(*args: LINKABLE, **kwargs: LINKABLE):
    """Create a simulation zone for iterative geometry processing over time

    Simulation zones allow geometry to evolve over multiple frames, with state
    persisting between Blender frames.

    Args:
        *args: Initial geometry or data to pass into the simulation
        **kwargs: Named inputs to the simulation zone

    Returns:
        tuple[SimulationInput, SimulationOutput]: Input and output nodes for the simulation

    Usage:
        ```python
        with TreeBuilder() as tree:
            cube = n.Cube()
            input, output = n.simulation_zone(cube)

            # Capture position for feedback
            pos_math = input.capture(n.Position()) * n.Position()
            pos_math >> output

            # Move geometry based on delta time
            input >> n.SetPosition(
                offset=input.o_delta_time * n.Vector((0, 0, 0.1)) * pos_math
            ) >> output

            # Output final position
            output >> n.SetPosition(position=output.outputs["Position"])
        ```

    The simulation input provides:
        - o_delta_time: Time elapsed since last iteration
        - capture(): Method to capture values for state persistence

    The simulation output provides:
        - i_skip: Boolean input to skip simulation frames
        - outputs: Dictionary of captured state outputs
    """
    input = SimulationInput()
    output = SimulationOutput()
    input.node.pair_with_output(output.node)

    output.node.state_items.clear()
    socket_lookup = output._add_inputs(*args, **kwargs)
    for name, source in socket_lookup.items():
        input.link_from(source, name)

    return input, output


class SimulationInput(BaseZoneInput):
    """Simulation Input node"""

    name = "GeometryNodeSimulationInput"
    node: bpy.types.GeometryNodeSimulationInput

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an output to the simulation, optionally specifying the domain"""
        input_dict = self._add_inputs(value)
        self._establish_links(**input_dict)
        name = next(iter(input_dict))
        self.output_node.state_items[name].attribute_domain = domain
        return SocketLinker(self.node.inputs[name])

    @property
    def o_delta_time(self) -> SocketLinker:
        """Output socket: Delta Time"""
        return self._output("Delta Time")

    @property
    def output_node(self) -> bpy.types.GeometryNodeSimulationOutput:
        zone_output = self.node.paired_output  # type: ignore
        assert zone_output is not None
        return zone_output  # type: ignore

    @property
    def items_collection(self):
        """Return the state items collection"""
        return self.output_node.state_items


class SimulationOutput(BaseZoneOutput):
    """Simulation Output node"""

    name = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an output to the simulation, optionally specifying the domain"""
        input_dict = self._add_inputs(value)
        self._establish_links(**input_dict)
        name = next(iter(input_dict))
        self.node.state_items[name].attribute_domain = domain
        return SocketLinker(self.node.inputs[name])

    @property
    def items_collection(self):
        """Return the state items collection"""
        return self.node.state_items

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
        socket_lookup = self.output._add_inputs(*args, **kwargs)
        for name, source in socket_lookup.items():
            self.input.link_from(source, name)

    def __iter__(self):
        """Support for loop: for i, input, output in repeat_zone(...)"""
        yield self.input.o_iteration, self.input, self.output

    def __getitem__(self, index):
        """Support direct unpacking: i, input, output = repeat_zone(...)"""
        if index == 0:
            return self.input.o_iteration
        elif index == 1:
            return self.input
        elif index == 2:
            return self.output
        else:
            raise IndexError("repeat_zone returns (iteration, input, output)")

    def __len__(self):
        """Support unpacking"""
        return 3


def repeat_zone(iterations: TYPE_INPUT_INT = 1, *args: LINKABLE, **kwargs: LINKABLE):
    """Create a repeat zone for iterative geometry operations

    Repeat zones execute their contents a specified number of times, useful for
    procedural generation, iterations, and repetitive operations. The zone provides
    access to the current iteration index. Zones iterate linearly unless the zone can
    detect that it isn't dependent on the inputs from previous iterations in which
    case they can run in parallel.

    Args:
        iterations: Number of times to repeat (can be int or node outputting int)
        *args: Initial geometry or data to pass into the repeat zone
        **kwargs: Named inputs to the repeat zone

    Returns:
        RepeatZone: Object supporting both direct unpacking and iteration

    Usage:
        ```python
        # Direct unpacking - gets iteration socket, input node, output node
        i, input, output = repeat_zone(10, cube)
        pos_math = input.capture(n.Position()) * n.Position()
        pos_math >> output
        input >> n.SetPosition(offset=i * n.Vector((0, 0, 0.1)) * pos_math) >> output
        output >> n.SetPosition(position=output.outputs["Position"])

        # For loop syntax - same functionality, more explicit
        for i, input, output in repeat_zone(5):
            join = n.JoinGeometry()
            # i is the iteration socket, can be used in math operations
            n.Points(i, position=n.RandomValue.vector(min=-1, seed=i)) >> join >> output
            input >> join
        ```

    The repeat input provides:
        - o_iteration: Current iteration index (0-based)
        - capture(): Method to capture values between iterations

    The repeat output automatically creates sockets as needed when connected to.
    Sockets are created based on the type compatibility of the connecting node.
    """
    return RepeatZone(iterations, *args, **kwargs)


class RepeatInput(BaseZoneInput):
    """Repeat Input node"""

    name = "GeometryNodeRepeatInput"
    node: bpy.types.GeometryNodeRepeatInput

    def __init__(self, iterations: TYPE_INPUT_INT = 1):
        super().__init__()
        key_args = {"Iterations": iterations}
        self._establish_links(**key_args)

    def capture(self, value: LINKABLE) -> SocketLinker:
        """Capture something as an input to the simulation"""
        self._establish_links(**self._add_inputs(value))
        return SocketLinker(self.node.outputs[-2])

    @property
    def o_iteration(self) -> SocketLinker:
        """Output socket: Iteration"""
        return self._output("Iteration")

    @property
    def output_node(self) -> bpy.types.GeometryNodeRepeatOutput:
        zone_output = self.node.paired_output  # type: ignore
        assert zone_output is not None
        return zone_output  # type: ignore

    @property
    def items_collection(self):
        """Return the repeat items collection"""
        return self.output_node.repeat_items


class RepeatOutput(BaseZoneOutput):
    """Repeat Output node"""

    name = "GeometryNodeRepeatOutput"
    node: bpy.types.GeometryNodeRepeatOutput

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an output to the simulation"""
        input_dict = self._add_inputs(value)
        name = next(iter(input_dict))
        return SocketLinker(self.node.inputs[name])

    @property
    def items_collection(self):
        """Return the repeat items collection"""
        return self.node.repeat_items


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
