from nodebpy.builder import NodeBuilder, SocketLinker


import bpy

from .types import LINKABLE, TYPE_INPUT_BOOLEAN, _AttributeDomains


class ForEachGeometryElementInput(NodeBuilder):
    """For Each Geometry Element Input node"""

    name = "GeometryNodeForeachGeometryElementInput"
    node: bpy.types.GeometryNodeForeachGeometryElementInput

    def __init__(
        self,
        geometry: LINKABLE = None,
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
