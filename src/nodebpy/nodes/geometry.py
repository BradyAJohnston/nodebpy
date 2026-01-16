import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    _DeleteGeometryDomains,
    _DeleteGeoemtryModes,
)


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


class BoundingBox(NodeBuilder):
    """Calculate the limits of a geometry's positions and generate a box mesh with those dimensions"""

    name = "GeometryNodeBoundBox"
    node: bpy.types.GeometryNodeBoundBox

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        use_radius: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Use Radius": use_radius}
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_use_radius(self) -> SocketLinker:
        """Input socket: Use Radius"""
        return self._input("Use Radius")

    @property
    def o_bounding_box(self) -> SocketLinker:
        """Output socket: Bounding Box"""
        return self._output("Bounding Box")

    @property
    def o_min(self) -> SocketLinker:
        """Output socket: Min"""
        return self._output("Min")

    @property
    def o_max(self) -> SocketLinker:
        """Output socket: Max"""
        return self._output("Max")


class ConvexHull(NodeBuilder):
    """Create a mesh that encloses all points in the input geometry with the smallest number of points"""

    name = "GeometryNodeConvexHull"
    node: bpy.types.GeometryNodeConvexHull

    def __init__(self, geometry: LINKABLE = None):
        super().__init__()
        key_args = {"Geometry": geometry}
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_convex_hull(self) -> SocketLinker:
        """Output socket: Convex Hull"""
        return self._output("Convex Hull")


class DeleteGeometry(NodeBuilder):
    """Remove selected elements of a geometry"""

    name = "GeometryNodeDeleteGeometry"
    node: bpy.types.GeometryNodeDeleteGeometry

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: _DeleteGeoemtryModes = "ALL",
        domain: _DeleteGeometryDomains = "POINT",
    ):
        super().__init__()
        self.mode = mode
        self.domain = domain
        key_args = {"Geometry": geometry, "Selection": selection}
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
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def mode(self) -> _DeleteGeoemtryModes:
        return self.node.mode

    @mode.setter
    def mode(self, value: _DeleteGeoemtryModes):
        self.node.mode = value

    @property
    def domain(self) -> _DeleteGeometryDomains:
        return self.node.domain

    @domain.setter
    def domain(self, value: _DeleteGeometryDomains):
        self.node.domain = value
