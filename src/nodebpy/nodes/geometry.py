from typing_extensions import Literal
import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_VALUE,
    _DeleteGeometryDomains,
    _DeleteGeoemtryModes,
    _DuplicateElementsDomains,
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


class DistributePointsOnFaces(NodeBuilder):
    """Generate points spread out on the surface of a mesh"""

    name = "GeometryNodeDistributePointsOnFaces"
    node: bpy.types.GeometryNodeDistributePointsOnFaces

    def __init__(
        self,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        density: TYPE_INPUT_VALUE = 10.0,
        distance_min: TYPE_INPUT_VALUE = 10.0,
        density_max: TYPE_INPUT_VALUE = 10.0,
        density_factor: TYPE_INPUT_VALUE = 10.0,
        distribute_method: Literal["RANDOM", "POISSON"] = "RANDOM",
        seed: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Seed": seed,
        }
        if distribute_method == "RANDOM":
            key_args["Density"] = density
        elif distribute_method == "POISSON":
            key_args["Distance Min"] = distance_min
            key_args["Density Max"] = density_max
            key_args["Density Factor"] = density_factor
        key_args.update(kwargs)
        self.distribute_method = distribute_method
        self._establish_links(**key_args)

    @classmethod
    def random(
        cls,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        density: TYPE_INPUT_VALUE = 10.0,
        seed: TYPE_INPUT_INT = 0,
    ):
        return cls(
            mesh=mesh,
            selection=selection,
            density=density,
            seed=seed,
            distribute_method="RANDOM",
        )

    @classmethod
    def poisson(
        cls,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        distance_min: TYPE_INPUT_VALUE = 10.0,
        density_max: TYPE_INPUT_VALUE = 10.0,
        density_factor: TYPE_INPUT_VALUE = 10.0,
        seed: TYPE_INPUT_INT = 0,
    ):
        return cls(
            mesh=mesh,
            selection=selection,
            seed=seed,
            distribute_method="POISSON",
            distance_min=distance_min,
            density_max=density_max,
            density_factor=density_factor,
        )

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_seed(self) -> SocketLinker:
        """Input socket: Seed"""
        return self._input("Seed")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def distribute_method(self) -> Literal["RANDOM", "POISSON"]:
        return self.node.distribute_method

    @distribute_method.setter
    def distribute_method(self, value: Literal["RANDOM", "POISSON"]):
        self.node.distribute_method = value

    @property
    def use_legacy_normal(self) -> bool:
        return self.node.use_legacy_normal

    @use_legacy_normal.setter
    def use_legacy_normal(self, value: bool):
        self.node.use_legacy_normal = value


class DuplicateElements(NodeBuilder):
    """Generate an arbitrary number copies of each selected input element"""

    name = "GeometryNodeDuplicateElements"
    node: bpy.types.GeometryNodeDuplicateElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
        domain: _DuplicateElementsDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Amount": amount}
        self.domain = domain
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
    def i_amount(self) -> SocketLinker:
        """Input socket: Amount"""
        return self._input("Amount")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def o_duplicate_index(self) -> SocketLinker:
        """Output socket: Duplicate Index"""
        return self._output("Duplicate Index")

    @property
    def domain(self) -> _DuplicateElementsDomains:
        return self.node.domain

    @domain.setter
    def domain(self, value: _DuplicateElementsDomains):
        self.node.domain = value
