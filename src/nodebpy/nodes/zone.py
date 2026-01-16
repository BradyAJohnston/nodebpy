from nodebpy.builder import NodeBuilder, SocketLinker


import bpy

from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
)


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
