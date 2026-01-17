import bpy
from typing_extensions import Literal

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_STRING,
    TYPE_INPUT_INT,
    TYPE_INPUT_MATERIAL,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_MENU,
    _DeleteGeoemtryModes,
    _DeleteGeometryDomains,
    _DuplicateElementsDomains,
    _RaycaseDataTypes,
    _AttributeDomains,
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

    def __init__(self, geometry: TYPE_INPUT_GEOMETRY = None):
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


class FlipFaces(NodeBuilder):
    """Reverse the order of the vertices and edges of selected faces, flipping their normal direction"""

    name = "GeometryNodeFlipFaces"
    node: bpy.types.GeometryNodeFlipFaces

    def __init__(
        self, mesh: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = None
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection}
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class GeometryToInstance(NodeBuilder):
    """Convert each input geometry into an instance, which can be much faster than the Join Geometry node when the inputs are large"""

    name = "GeometryNodeGeometryToInstance"
    node: bpy.types.GeometryNodeGeometryToInstance

    def __init__(self, *args: TYPE_INPUT_GEOMETRY):
        super().__init__()
        for arg in reversed(args):
            self.link_from(arg, "Geometry")

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class InstanceOnPoints(NodeBuilder):
    """Generate a reference to geometry at each of the input points, without duplicating its underlying data"""

    name = "GeometryNodeInstanceOnPoints"
    node: bpy.types.GeometryNodeInstanceOnPoints

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        instance: LINKABLE = None,
        pick_instance: TYPE_INPUT_BOOLEAN = False,
        instance_index: TYPE_INPUT_INT = 0,
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        scale: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Selection": selection,
            "Instance": instance,
            "Pick Instance": pick_instance,
            "Instance Index": instance_index,
            "Rotation": rotation,
            "Scale": scale,
        }
        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_instance(self) -> SocketLinker:
        """Input socket: Instance"""
        return self._input("Instance")

    @property
    def i_pick_instance(self) -> SocketLinker:
        """Input socket: Pick Instance"""
        return self._input("Pick Instance")

    @property
    def i_instance_index(self) -> SocketLinker:
        """Input socket: Instance Index"""
        return self._input("Instance Index")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class InstancesToPoints(NodeBuilder):
    """Generate points at the origins of instances.
    Note: Nested instances are not affected by this node"""

    name = "GeometryNodeInstancesToPoints"
    node: bpy.types.GeometryNodeInstancesToPoints

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        position: TYPE_INPUT_VECTOR = None,
        radius: TYPE_INPUT_VALUE = 0.05,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Position": position,
            "Radius": radius,
        }
        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")


class MaterialSelection(NodeBuilder):
    """Provide a selection of faces that use the specified material"""

    name = "GeometryNodeMaterialSelection"
    node: bpy.types.GeometryNodeMaterialSelection

    def __init__(self, material: TYPE_INPUT_MATERIAL = None):
        super().__init__()
        key_args = {"Material": material}
        self._establish_links(**key_args)

    @property
    def i_material(self) -> SocketLinker:
        """Input socket: Material"""
        return self._input("Material")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")


class MergeLayers(NodeBuilder):
    """Join groups of Grease Pencil layers into one"""

    name = "GeometryNodeMergeLayers"
    node: bpy.types.GeometryNodeMergeLayers

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = None,
        *,
        mode: Literal["MERGE_BY_NAME", "MERGE_BY_ID"] = "MERGE_BY_NAME",
    ):
        super().__init__()
        key_args = {"Grease Pencil": grease_pencil, "Selection": selection}
        self.mode = mode
        if self.mode == "MERGE_BY_ID":
            key_args["Group ID"] = group_id
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_group_id(self) -> SocketLinker:
        return self._input("Group ID")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def mode(self) -> Literal["MERGE_BY_NAME", "MERGE_BY_ID"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["MERGE_BY_NAME", "MERGE_BY_ID"]):
        self.node.mode = value


class MergeByDistance(NodeBuilder):
    """Merge vertices or points within a given distance"""

    name = "GeometryNodeMergeByDistance"
    node: bpy.types.GeometryNodeMergeByDistance

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        mode: Literal["All", "Connected"] = "All",
        distance: TYPE_INPUT_VALUE = 0.001,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Mode": mode,
            "Distance": distance,
        }
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
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_distance(self) -> SocketLinker:
        """Input socket: Distance"""
        return self._input("Distance")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class Points(NodeBuilder):
    """Generate a point cloud with positions and radii defined by fields"""

    name = "GeometryNodePoints"
    node: bpy.types.GeometryNodePoints

    def __init__(
        self,
        count: TYPE_INPUT_INT = 1,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        radius: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {"Count": count, "Position": position, "Radius": radius}
        self._establish_links(**key_args)

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Geometry")


class PointsToSDFGrid(NodeBuilder):
    """Create a signed distance volume grid from points"""

    name = "GeometryNodePointsToSDFGrid"
    node: bpy.types.GeometryNodePointsToSDFGrid

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        radius: TYPE_INPUT_VALUE = 0.5,
        voxel_size: TYPE_INPUT_VALUE = 0.3,
    ):
        super().__init__()
        key_args = {"Points": points, "Radius": radius, "Voxel Size": voxel_size}
        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def o_sdf_grid(self) -> SocketLinker:
        """Output socket: SDF Grid"""
        return self._output("SDF Grid")


class PointsToVertices(NodeBuilder):
    """Generate a mesh vertex for each point cloud point"""

    name = "GeometryNodePointsToVertices"
    node: bpy.types.GeometryNodePointsToVertices

    def __init__(
        self, points: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = None
    ):
        super().__init__()
        key_args = {"Points": points, "Selection": selection}
        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class GeometryProximity(NodeBuilder):
    """Compute the closest location on the target geometry"""

    name = "GeometryNodeProximity"
    node: bpy.types.GeometryNodeProximity

    def __init__(
        self,
        target: TYPE_INPUT_GEOMETRY = None,
        group_id: TYPE_INPUT_INT = None,
        source_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = None,
        target_element: Literal["POINTS", "EDGES", "FACES"] = "FACES",
    ):
        super().__init__()
        key_args = {
            "Target": target,
            "Group ID": group_id,
            "Source Position": source_position,
            "Sample Group ID": sample_group_id,
        }
        self.target_element = target_element
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Target")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Source Position")

    @property
    def i_sample_group_id(self) -> SocketLinker:
        """Input socket: Sample Group ID"""
        return self._input("Sample Group ID")

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")

    @property
    def o_distance(self) -> SocketLinker:
        """Output socket: Distance"""
        return self._output("Distance")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def target_element(self) -> Literal["POINTS", "EDGES", "FACES"]:
        return self.node.target_element

    @target_element.setter
    def target_element(self, value: Literal["POINTS", "EDGES", "FACES"]):
        self.node.target_element = value


class PointsToVolume(NodeBuilder):
    """Generate a fog volume sphere around every point"""

    name = "GeometryNodePointsToVolume"
    node: bpy.types.GeometryNodePointsToVolume

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        density: TYPE_INPUT_VALUE = 1.0,
        radius: TYPE_INPUT_VALUE = 0.5,
        *,
        resolution_mode: Literal["Amount", "Size"] = "Amount",
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        voxel_amount: TYPE_INPUT_VALUE = 64.0,
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Density": density,
            "Resolution Mode": resolution_mode,
            "Radius": radius,
        }
        match resolution_mode:
            case "Amount":
                key_args["Voxel Amount"] = voxel_amount
            case "Size":
                key_args["Voxel Size"] = voxel_size
        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_resolution_mode(self) -> SocketLinker:
        """Input socket: Resolution Mode"""
        return self._input("Resolution Mode")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_voxel_amount(self) -> SocketLinker:
        """Input socket: Voxel Amount"""
        return self._input("Voxel Amount")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class Raycast(NodeBuilder):
    """Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point"""

    name = "GeometryNodeRaycast"
    node: bpy.types.GeometryNodeRaycast

    def __init__(
        self,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_VALUE = None,
        interpolation: Literal["Interpolated", "Nearest"] = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        ray_direction: TYPE_INPUT_VECTOR = (0.0, 0.0, -1.0),
        ray_length: TYPE_INPUT_VALUE = 100.0,
        *,
        data_type: _RaycaseDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Target Geometry": target_geometry,
            "Attribute": attribute,
            "Interpolation": interpolation,
            "Source Position": source_position,
            "Ray Direction": ray_direction,
            "Ray Length": ray_length,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_target_geometry(self) -> SocketLinker:
        """Input socket: Target Geometry"""
        return self._input("Target Geometry")

    @property
    def i_attribute(self) -> SocketLinker:
        """Input socket: Attribute"""
        return self._input("Attribute")

    @property
    def i_interpolation(self) -> SocketLinker:
        """Input socket: Interpolation"""
        return self._input("Interpolation")

    @property
    def i_source_position(self) -> SocketLinker:
        """Input socket: Source Position"""
        return self._input("Source Position")

    @property
    def i_ray_direction(self) -> SocketLinker:
        """Input socket: Ray Direction"""
        return self._input("Ray Direction")

    @property
    def i_ray_length(self) -> SocketLinker:
        """Input socket: Ray Length"""
        return self._input("Ray Length")

    @property
    def o_is_hit(self) -> SocketLinker:
        """Output socket: Is Hit"""
        return self._output("Is Hit")

    @property
    def o_hit_position(self) -> SocketLinker:
        """Output socket: Hit Position"""
        return self._output("Hit Position")

    @property
    def o_hit_normal(self) -> SocketLinker:
        """Output socket: Hit Normal"""
        return self._output("Hit Normal")

    @property
    def o_hit_distance(self) -> SocketLinker:
        """Output socket: Hit Distance"""
        return self._output("Hit Distance")

    @property
    def o_attribute(self) -> SocketLinker:
        """Output socket: Attribute"""
        return self._output("Attribute")

    @property
    def data_type(
        self,
    ) -> _RaycaseDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _RaycaseDataTypes,
    ):
        self.node.data_type = value


class RealizeInstances(NodeBuilder):
    """Convert instances into real geometry data"""

    name = "GeometryNodeRealizeInstances"
    node: bpy.types.GeometryNodeRealizeInstances

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        realize_all: TYPE_INPUT_BOOLEAN = True,
        depth: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Realize All": realize_all,
            "Depth": depth,
        }
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
    def i_realize_all(self) -> SocketLinker:
        """Input socket: Realize All"""
        return self._input("Realize All")

    @property
    def i_depth(self) -> SocketLinker:
        """Input socket: Depth"""
        return self._input("Depth")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class ReplaceMaterial(NodeBuilder):
    """Swap one material with another"""

    name = "GeometryNodeReplaceMaterial"
    node: bpy.types.GeometryNodeReplaceMaterial

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        old: TYPE_INPUT_MATERIAL = None,
        new: TYPE_INPUT_MATERIAL = None,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Old": old, "New": new}
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_old(self) -> SocketLinker:
        """Input socket: Old"""
        return self._input("Old")

    @property
    def i_new(self) -> SocketLinker:
        """Input socket: New"""
        return self._input("New")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class RotateInstances(NodeBuilder):
    """Rotate geometry instances in local or global space"""

    name = "GeometryNodeRotateInstances"
    node: bpy.types.GeometryNodeRotateInstances

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        pivot_point: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Rotation": rotation,
            "Pivot Point": pivot_point,
            "Local Space": local_space,
        }
        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_pivot_point(self) -> SocketLinker:
        """Input socket: Pivot Point"""
        return self._input("Pivot Point")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SampleIndex(NodeBuilder):
    """Retrieve values from specific geometry elements"""

    name = "GeometryNodeSampleIndex"
    node: bpy.types.GeometryNodeSampleIndex

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: LINKABLE = None,
        index: TYPE_INPUT_INT = 0,
        *,
        data_type: _RaycaseDataTypes = "FLOAT",
        domain: _AttributeDomains = "POINT",
        clamp: bool = False,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Value": value, "Index": index}
        self.data_type = data_type
        self.domain = domain
        self.clamp = clamp
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(
        self,
    ) -> _RaycaseDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _RaycaseDataTypes,
    ):
        self.node.data_type = value

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
    def clamp(self) -> bool:
        return self.node.clamp

    @clamp.setter
    def clamp(self, value: bool):
        self.node.clamp = value


class SampleNearest(NodeBuilder):
    """Find the element of a geometry closest to a position. Similar to the "Index of Nearest" node"""

    name = "GeometryNodeSampleNearest"
    node: bpy.types.GeometryNodeSampleNearest

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        sample_position: TYPE_INPUT_VECTOR = None,
        domain: Literal["POINT", "EDGE", "FACE", "CORNER"] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Sample Position": sample_position}
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Sample Position")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CORNER"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CORNER"]):
        self.node.domain = value


class SampleNearestSurface(NodeBuilder):
    """Calculate the interpolated value of a mesh attribute on the closest point of its surface"""

    name = "GeometryNodeSampleNearestSurface"
    node: bpy.types.GeometryNodeSampleNearestSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        value: TYPE_INPUT_VALUE = None,
        group_id: TYPE_INPUT_INT = None,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = None,
        *,
        data_type: _RaycaseDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Value": value,
            "Group ID": group_id,
            "Sample Position": sample_position,
            "Sample Group ID": sample_group_id,
        }
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Sample Position")

    @property
    def i_sample_group_id(self) -> SocketLinker:
        """Input socket: Sample Group ID"""
        return self._input("Sample Group ID")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def data_type(
        self,
    ) -> _RaycaseDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _RaycaseDataTypes,
    ):
        self.node.data_type = value


class ScaleElements(NodeBuilder):
    """Scale groups of connected edges and faces"""

    name = "GeometryNodeScaleElements"
    node: bpy.types.GeometryNodeScaleElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = None,
        scale: TYPE_INPUT_VALUE = 1.0,
        center: TYPE_INPUT_VECTOR = None,
        scale_mode: Literal["Uniform", "Single Axis"] | TYPE_INPUT_MENU = "Uniform",
        axis: TYPE_INPUT_VECTOR = (1.0, 0.0, 0.0),
        *,
        domain: Literal["FACE", "EDGE"] = "FACE",
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Scale": scale,
            "Center": center,
            "Scale Mode": scale_mode,
            "Axis": axis,
        }
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
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_center(self) -> SocketLinker:
        """Input socket: Center"""
        return self._input("Center")

    @property
    def i_scale_mode(self) -> SocketLinker:
        """Input socket: Scale Mode"""
        return self._input("Scale Mode")

    @property
    def i_axis(self) -> SocketLinker:
        """Input socket: Axis"""
        return self._input("Axis")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["FACE", "EDGE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["FACE", "EDGE"]):
        self.node.domain = value


class SampleUVSurface(NodeBuilder):
    """Calculate the interpolated values of a mesh attribute at a UV coordinate"""

    name = "GeometryNodeSampleUVSurface"
    node: bpy.types.GeometryNodeSampleUVSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        value: LINKABLE = None,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        *,
        data_type: _RaycaseDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Value": value,
            "Source UV Map": source_uv_map,
            "Sample UV": sample_uv,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_uv_map(self) -> SocketLinker:
        """Input socket: UV Map"""
        return self._input("Source UV Map")

    @property
    def i_sample_uv(self) -> SocketLinker:
        """Input socket: Sample UV"""
        return self._input("Sample UV")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def data_type(
        self,
    ) -> _RaycaseDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _RaycaseDataTypes,
    ):
        self.node.data_type = value


class ScaleInstances(NodeBuilder):
    """Scale geometry instances in local or global space"""

    name = "GeometryNodeScaleInstances"
    node: bpy.types.GeometryNodeScaleInstances

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
        center: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Scale": scale,
            "Center": center,
            "Local Space": local_space,
        }
        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_center(self) -> SocketLinker:
        """Input socket: Center"""
        return self._input("Center")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SeparateComponents(NodeBuilder):
    """Split a geometry into a separate output for each type of data in the geometry"""

    name = "GeometryNodeSeparateComponents"
    node: bpy.types.GeometryNodeSeparateComponents

    def __init__(self, geometry: TYPE_INPUT_GEOMETRY = None):
        super().__init__()
        key_args = {"Geometry": geometry}
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def o_point_cloud(self) -> SocketLinker:
        """Output socket: Point Cloud"""
        return self._output("Point Cloud")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SeparateGeometry(NodeBuilder):
    """Split a geometry into two geometry outputs based on a selection"""

    name = "GeometryNodeSeparateGeometry"
    node: bpy.types.GeometryNodeSeparateGeometry

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        domain: _DeleteGeometryDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
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
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")

    @property
    def o_inverted(self) -> SocketLinker:
        """Output socket: Inverted"""
        return self._output("Inverted")

    @property
    def domain(self) -> _DeleteGeometryDomains:
        return self.node.domain

    @domain.setter
    def domain(self, value: _DeleteGeometryDomains):
        self.node.domain = value


class SetGeometryName(NodeBuilder):
    """Set the name of a geometry for easier debugging"""

    name = "GeometryNodeSetGeometryName"
    node: bpy.types.GeometryNodeSetGeometryName

    def __init__(
        self, geometry: TYPE_INPUT_GEOMETRY = None, name: TYPE_INPUT_STRING = ""
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Name": name}
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetGreasePencilColor(NodeBuilder):
    """Set color and opacity attributes on Grease Pencil geometry"""

    name = "GeometryNodeSetGreasePencilColor"
    node: bpy.types.GeometryNodeSetGreasePencilColor

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        color: TYPE_INPUT_COLOR = (1.0, 1.0, 1.0, 1.0),
        opacity: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["STROKE", "FILL"] = "STROKE",
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Color": color,
            "Opacity": opacity,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def i_opacity(self) -> SocketLinker:
        """Input socket: Opacity"""
        return self._input("Opacity")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def mode(self) -> Literal["STROKE", "FILL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["STROKE", "FILL"]):
        self.node.mode = value


class SetGreasePencilDepth(NodeBuilder):
    """Set the Grease Pencil depth order to use"""

    name = "GeometryNodeSetGreasePencilDepth"
    node: bpy.types.GeometryNodeSetGreasePencilDepth

    def __init__(
        self,
        grease_pencil: TYPE_INPUT_GEOMETRY = None,
        depth_order: Literal["2D", "3D"] = "2D",
    ):
        super().__init__()
        key_args = {"Grease Pencil": grease_pencil}
        self.depth_order = depth_order
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def depth_order(self) -> Literal["2D", "3D"]:
        return self.node.depth_order

    @depth_order.setter
    def depth_order(self, value: Literal["2D", "3D"]):
        self.node.depth_order = value


class SetGreasePencilSoftness(NodeBuilder):
    """Set softness attribute on Grease Pencil geometry"""

    name = "GeometryNodeSetGreasePencilSoftness"
    node: bpy.types.GeometryNodeSetGreasePencilSoftness

    def __init__(
        self,
        grease_pencil: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        softness: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Softness": softness,
        }
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_softness(self) -> SocketLinker:
        """Input socket: Softness"""
        return self._input("Softness")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")


class SetID(NodeBuilder):
    """Set the id attribute on the input geometry, mainly used internally for randomizing"""

    name = "GeometryNodeSetID"
    node: bpy.types.GeometryNodeSetID

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        id: TYPE_INPUT_INT = None,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "ID": id}
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
    def i_id(self) -> SocketLinker:
        """Input socket: ID"""
        return self._input("ID")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetInstanceTransform(NodeBuilder):
    """Set the transformation matrix of every instance"""

    name = "GeometryNodeSetInstanceTransform"
    node: bpy.types.GeometryNodeSetInstanceTransform

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        transform: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Transform": transform,
        }
        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SetMaterial(NodeBuilder):
    """Assign a material to geometry elements"""

    name = "GeometryNodeSetMaterial"
    node: bpy.types.GeometryNodeSetMaterial

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        material: TYPE_INPUT_MATERIAL = None,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Material": material}
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
    def i_material(self) -> SocketLinker:
        """Input socket: Material"""
        return self._input("Material")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetMaterialIndex(NodeBuilder):
    """Set the material index for each selected geometry element"""

    name = "GeometryNodeSetMaterialIndex"
    node: bpy.types.GeometryNodeSetMaterialIndex

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        material_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Material Index": material_index,
        }
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
    def i_material_index(self) -> SocketLinker:
        """Input socket: Material Index"""
        return self._input("Material Index")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetPointRadius(NodeBuilder):
    """Set the display size of point cloud points"""

    name = "GeometryNodeSetPointRadius"
    node: bpy.types.GeometryNodeSetPointRadius

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        radius: TYPE_INPUT_VALUE = 0.05,
    ):
        super().__init__()
        key_args = {"Points": points, "Selection": selection, "Radius": radius}
        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")


class SetPosition(NodeBuilder):
    """Set the location of each point"""

    name = "GeometryNodeSetPosition"
    node: bpy.types.GeometryNodeSetPosition

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        position: TYPE_INPUT_VECTOR = None,
        offset: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Position": position,
            "Offset": offset,
        }
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
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetShadeSmooth(NodeBuilder):
    """Control the smoothness of mesh normals around each face by changing the "shade smooth" attribute"""

    name = "GeometryNodeSetShadeSmooth"
    node: bpy.types.GeometryNodeSetShadeSmooth

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        shade_smooth: TYPE_INPUT_BOOLEAN = True,
        *,
        domain: Literal["EDGE", "FACE"] = "FACE",
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Shade Smooth": shade_smooth,
        }
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_shade_smooth(self) -> SocketLinker:
        """Input socket: Shade Smooth"""
        return self._input("Shade Smooth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["EDGE", "FACE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["EDGE", "FACE"]):
        self.node.domain = value


class SetSplineCyclic(NodeBuilder):
    """Control whether each spline loops back on itself by changing the "cyclic" attribute"""

    name = "GeometryNodeSetSplineCyclic"
    node: bpy.types.GeometryNodeSetSplineCyclic

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        cyclic: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Cyclic": cyclic}
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_cyclic(self) -> SocketLinker:
        """Input socket: Cyclic"""
        return self._input("Cyclic")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Geometry")


class SetSplineResolution(NodeBuilder):
    """Control how many evaluated points should be generated on every curve segment"""

    name = "GeometryNodeSetSplineResolution"
    node: bpy.types.GeometryNodeSetSplineResolution

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        resolution: TYPE_INPUT_INT = 12,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Resolution": resolution,
        }
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Geometry")


class SortElements(NodeBuilder):
    """Rearrange geometry elements, changing their indices"""

    name = "GeometryNodeSortElements"
    node: bpy.types.GeometryNodeSortElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = None,
        sort_weight: TYPE_INPUT_VALUE = None,
        *,
        domain: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"] = "POINT",
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Group ID": group_id,
            "Sort Weight": sort_weight,
        }
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
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sort_weight(self) -> SocketLinker:
        """Input socket: Sort Weight"""
        return self._input("Sort Weight")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"]):
        self.node.domain = value


class SplitEdges(NodeBuilder):
    """Duplicate mesh edges and break connections with the surrounding faces"""

    name = "GeometryNodeSplitEdges"
    node: bpy.types.GeometryNodeSplitEdges

    def __init__(
        self, mesh: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection}
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SplitToInstances(NodeBuilder):
    """Create separate geometries containing the elements from the same group"""

    name = "GeometryNodeSplitToInstances"
    node: bpy.types.GeometryNodeSplitToInstances

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = None,
        *,
        domain: _DeleteGeometryDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Group ID": group_id}
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
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")

    @property
    def o_group_id(self) -> SocketLinker:
        """Output socket: Group ID"""
        return self._output("Group ID")

    @property
    def domain(self) -> _DeleteGeometryDomains:
        return self.node.domain

    @domain.setter
    def domain(self, value: _DeleteGeometryDomains):
        self.node.domain = value


class SubdivisionSurface(NodeBuilder):
    """Divide mesh faces to form a smooth surface, using the Catmull-Clark subdivision method"""

    name = "GeometryNodeSubdivisionSurface"
    node: bpy.types.GeometryNodeSubdivisionSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        level: TYPE_INPUT_INT = 1,
        edge_crease: TYPE_INPUT_VALUE = 0.0,
        vertex_crease: TYPE_INPUT_VALUE = 0.0,
        limit_surface: TYPE_INPUT_BOOLEAN = True,
        uv_smooth: Literal[
            "None",
            "Keep Corners",
            "Keep Corners, Junctions",
            "Keep Corners, Junctions, Concave",
            "Keep Boundaries",
            "All",
        ] = "Keep Boundaries",
        boundary_smooth: Literal["Keep Corners", "All"] | TYPE_INPUT_MENU = "All",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Level": level,
            "Edge Crease": edge_crease,
            "Vertex Crease": vertex_crease,
            "Limit Surface": limit_surface,
            "UV Smooth": uv_smooth,
            "Boundary Smooth": boundary_smooth,
        }
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_level(self) -> SocketLinker:
        """Input socket: Level"""
        return self._input("Level")

    @property
    def i_edge_crease(self) -> SocketLinker:
        """Input socket: Edge Crease"""
        return self._input("Edge Crease")

    @property
    def i_vertex_crease(self) -> SocketLinker:
        """Input socket: Vertex Crease"""
        return self._input("Vertex Crease")

    @property
    def i_limit_surface(self) -> SocketLinker:
        """Input socket: Limit Surface"""
        return self._input("Limit Surface")

    @property
    def i_uv_smooth(self) -> SocketLinker:
        """Input socket: UV Smooth"""
        return self._input("UV Smooth")

    @property
    def i_boundary_smooth(self) -> SocketLinker:
        """Input socket: Boundary Smooth"""
        return self._input("Boundary Smooth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SetFaceSet(NodeBuilder):
    """Set sculpt face set values for faces"""

    name = "GeometryNodeToolSetFaceSet"
    node: bpy.types.GeometryNodeToolSetFaceSet

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        face_set: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection, "Face Set": face_set}
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_face_set(self) -> SocketLinker:
        """Input socket: Face Set"""
        return self._input("Face Set")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SetSelection(NodeBuilder):
    """Set selection of the edited geometry, for tool execution"""

    name = "GeometryNodeToolSetSelection"
    node: bpy.types.GeometryNodeToolSetSelection

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        domain: Literal["POINT", "EDGE", "FACE", "CURVE"] = "POINT",
        selection_type: Literal["BOOLEAN", "FLOAT"] = "BOOLEAN",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self.domain = domain
        self.selection_type = selection_type
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
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CURVE"]):
        self.node.domain = value

    @property
    def selection_type(self) -> Literal["BOOLEAN", "FLOAT"]:
        return self.node.selection_type

    @selection_type.setter
    def selection_type(self, value: Literal["BOOLEAN", "FLOAT"]):
        self.node.selection_type = value


class TransformGeometry(NodeBuilder):
    """Translate, rotate or scale the geometry"""

    name = "GeometryNodeTransform"
    node: bpy.types.GeometryNodeTransform

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        mode: Literal["Components", "Matrix"] = "Components",
        *,
        translation: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        scale: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
        transform: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Mode": mode,
            "Translation": translation,
            "Rotation": rotation,
            "Scale": scale,
            "Transform": transform,
        }
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_translation(self) -> SocketLinker:
        """Input socket: Translation"""
        return self._input("Translation")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class TranslateInstances(NodeBuilder):
    """Move top-level geometry instances in local or global space"""

    name = "GeometryNodeTranslateInstances"
    node: bpy.types.GeometryNodeTranslateInstances

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        translation: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Translation": translation,
            "Local Space": local_space,
        }
        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_translation(self) -> SocketLinker:
        """Input socket: Translation"""
        return self._input("Translation")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class Triangulate(NodeBuilder):
    """Convert all faces in a mesh to triangular faces"""

    name = "GeometryNodeTriangulate"
    node: bpy.types.GeometryNodeTriangulate

    def __init__(
        self,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        quad_method: Literal[
            "Beauty",
            "Fixed",
            "Fixed Alternate",
            "Shortest Diagonal",
            "Longest Diagonal",
        ]
        | TYPE_INPUT_MENU = "Shortest Diagonal",
        n_gon_method: Literal["Beauty", "Clip"] | TYPE_INPUT_MENU = "Beauty",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Quad Method": quad_method,
            "N-gon Method": n_gon_method,
        }
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_quad_method(self) -> SocketLinker:
        """Input socket: Quad Method"""
        return self._input("Quad Method")

    @property
    def i_n_gon_method(self) -> SocketLinker:
        """Input socket: N-gon Method"""
        return self._input("N-gon Method")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")
