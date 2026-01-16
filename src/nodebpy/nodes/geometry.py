from ..builder import NodeBuilder, SocketLinker
from .types import LINKABLE


import bpy


class JoinGeometry(NodeBuilder):
    """Merge separately generated geometries into a single one"""

    name = "GeometryNodeJoinGeometry"
    node: bpy.types.GeometryNodeJoinGeometry

    def __init__(self, *args: LINKABLE):
        super().__init__()
        for source in reversed(args):
            self.link_from(source, self)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")
