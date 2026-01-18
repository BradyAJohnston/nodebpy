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


def simulation_zone(*args: LINKABLE, **kwargs: LINKABLE):
    input = SimulationInput()
    output = SimulationOutput()
    input.node.pair_with_output(output.node)

    output.node.state_items.clear()
    socket_lookup = output._add_inputs(*args, **kwargs)
    for name, source in socket_lookup.items():
        input.link_from(source, name)

    return input, output


class SimulationInput(NodeBuilder):
    """Simulation Input node"""

    name = "GeometryNodeSimulationInput"
    node: bpy.types.GeometryNodeSimulationInput

    def _add_socket(self, name: str, type: _BakeDataTypes):
        item = self.output_node.state_items.new(type, name)
        return self.output_node.inputs[item.name]

    def capture(self, value: LINKABLE) -> SocketLinker:
        """Capture something as an input to the simulation"""
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
        self._establish_links(**self._add_inputs(value))
        return SocketLinker(self.node.outputs[-2])

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
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.output_node.state_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.output_node.state_items
        }


class SimulationOutput(NodeBuilder):
    """Simulation Output node"""

    name = "GeometryNodeSimulationOutput"
    node: bpy.types.GeometryNodeSimulationOutput

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an output to the simulation, optionally specifying the domain"""
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
        input_dict = self._add_inputs(value)
        name = next(iter(input_dict))
        self.node.state_items[name].attribute_domain = domain
        return SocketLinker(self.node.inputs[name])

    def _add_socket(self, name: str, type: _BakeDataTypes):
        item = self.node.state_items.new(type, name)
        return self.node.inputs[item.name]

    @property
    def _default_input_socket(self) -> NodeSocket:
        # we want the default input socket to not be the "skip" socket which is the first one
        # and would otherwise potentially be picked
        return next(iter(self.inputs.values())).socket

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.state_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.state_items
        }

    @property
    def i_skip(self) -> SocketLinker:
        """Input socket: Skip simluation frame"""
        return self._input("Skip")


def repeat_zone(iterations: TYPE_INPUT_INT = 1, *args: LINKABLE, **kwargs: LINKABLE):
    input = RepeatInput(iterations)
    output = RepeatOutput()
    input.node.pair_with_output(output.node)

    output.node.repeat_items.clear()
    socket_lookup = output._add_inputs(*args, **kwargs)
    for name, source in socket_lookup.items():
        input.link_from(source, name)

    return input, output


class RepeatInput(NodeBuilder):
    """Repeat Input node"""

    name = "GeometryNodeRepeatInput"
    node: bpy.types.GeometryNodeRepeatInput

    def __init__(self, iterations: TYPE_INPUT_INT = 1):
        super().__init__()
        key_args = {"Iterations": iterations}
        self._establish_links(**key_args)

    def _add_socket(self, name: str, type: _BakeDataTypes):
        item = self.output_node.repeat_items.new(type, name)
        return self.output_node.inputs[item.name]

    def capture(self, value: LINKABLE) -> SocketLinker:
        """Capture something as an input to the simulation"""
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
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
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.output_node.repeat_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.output_node.repeat_items
        }


class RepeatOutput(NodeBuilder):
    """Repeat Output node"""

    name = "GeometryNodeRepeatOutput"
    node: bpy.types.GeometryNodeRepeatOutput

    def capture(
        self, value: LINKABLE, domain: _AttributeDomains = "POINT"
    ) -> SocketLinker:
        """Capture something as an output to the simulation, optionally specifying the domain"""
        # the _add_inputs returns a dictionary but we only want the first key
        # because we are adding a single input
        input_dict = self._add_inputs(value)
        name = next(iter(input_dict))
        return SocketLinker(self.node.inputs[name])

    def _add_socket(self, name: str, type: _BakeDataTypes):
        item = self.node.repeat_items.new(type, name)
        return self.node.inputs[item.name]

    @property
    def _default_input_socket(self) -> NodeSocket:
        # we want the default input socket to not be the "skip" socket which is the first one
        # and would otherwise potentially be picked
        return next(iter(self.inputs.values())).socket

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.repeat_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.repeat_items
        }


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
