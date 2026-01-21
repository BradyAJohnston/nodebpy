from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_BUNDLE,
    TYPE_INPUT_CLOSURE,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_MATERIAL,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class Arc(NodeBuilder):
    """Generate a poly spline arc"""

    name = "GeometryNodeCurveArc"
    node: bpy.types.GeometryNodeCurveArc

    def __init__(
        self,
        resolution: TYPE_INPUT_INT = 16,
        start: TYPE_INPUT_VECTOR = None,
        middle: TYPE_INPUT_VECTOR = None,
        end: TYPE_INPUT_VECTOR = None,
        radius: TYPE_INPUT_VALUE = 1.0,
        start_angle: TYPE_INPUT_VALUE = 0.0,
        sweep_angle: TYPE_INPUT_VALUE = 5.4978,
        offset_angle: TYPE_INPUT_VALUE = 0.0,
        connect_center: TYPE_INPUT_BOOLEAN = False,
        invert_arc: TYPE_INPUT_BOOLEAN = False,
        *,
        mode: Literal["POINTS", "RADIUS"] = "RADIUS",
    ):
        super().__init__()
        key_args = {
            "Resolution": resolution,
            "Start": start,
            "Middle": middle,
            "End": end,
            "Radius": radius,
            "Start Angle": start_angle,
            "Sweep Angle": sweep_angle,
            "Offset Angle": offset_angle,
            "Connect Center": connect_center,
            "Invert Arc": invert_arc,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_start(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start")

    @property
    def i_middle(self) -> SocketLinker:
        """Input socket: Middle"""
        return self._input("Middle")

    @property
    def i_end(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_start_angle(self) -> SocketLinker:
        """Input socket: Start Angle"""
        return self._input("Start Angle")

    @property
    def i_sweep_angle(self) -> SocketLinker:
        """Input socket: Sweep Angle"""
        return self._input("Sweep Angle")

    @property
    def i_offset_angle(self) -> SocketLinker:
        """Input socket: Offset Angle"""
        return self._input("Offset Angle")

    @property
    def i_connect_center(self) -> SocketLinker:
        """Input socket: Connect Center"""
        return self._input("Connect Center")

    @property
    def i_invert_arc(self) -> SocketLinker:
        """Input socket: Invert Arc"""
        return self._input("Invert Arc")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def o_center(self) -> SocketLinker:
        """Output socket: Center"""
        return self._output("Center")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def o_radius(self) -> SocketLinker:
        """Output socket: Radius"""
        return self._output("Radius")

    @property
    def mode(self) -> Literal["POINTS", "RADIUS"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["POINTS", "RADIUS"]):
        self.node.mode = value


class Bake(NodeBuilder):
    """Cache the incoming data so that it can be used without recomputation"""

    name = "GeometryNodeBake"
    node: bpy.types.GeometryNodeBake

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)


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


class BezierSegment(NodeBuilder):
    """Generate a 2D Bézier spline from the given control points and handles"""

    name = "GeometryNodeCurvePrimitiveBezierSegment"
    node: bpy.types.GeometryNodeCurvePrimitiveBezierSegment

    def __init__(
        self,
        resolution: TYPE_INPUT_INT = 16,
        start: TYPE_INPUT_VECTOR = None,
        start_handle: TYPE_INPUT_VECTOR = None,
        end_handle: TYPE_INPUT_VECTOR = None,
        end: TYPE_INPUT_VECTOR = None,
        *,
        mode: Literal["POSITION", "OFFSET"] = "POSITION",
    ):
        super().__init__()
        key_args = {
            "Resolution": resolution,
            "Start": start,
            "Start Handle": start_handle,
            "End Handle": end_handle,
            "End": end,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_start(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start")

    @property
    def i_start_handle(self) -> SocketLinker:
        """Input socket: Start Handle"""
        return self._input("Start Handle")

    @property
    def i_end_handle(self) -> SocketLinker:
        """Input socket: End Handle"""
        return self._input("End Handle")

    @property
    def i_end(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(self) -> Literal["POSITION", "OFFSET"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["POSITION", "OFFSET"]):
        self.node.mode = value


class Cone(NodeBuilder):
    """Generate a cone mesh"""

    name = "GeometryNodeMeshCone"
    node: bpy.types.GeometryNodeMeshCone

    def __init__(
        self,
        vertices: TYPE_INPUT_INT = 32,
        side_segments: TYPE_INPUT_INT = 1,
        fill_segments: TYPE_INPUT_INT = 1,
        radius_top: TYPE_INPUT_VALUE = 0.0,
        radius_bottom: TYPE_INPUT_VALUE = 1.0,
        depth: TYPE_INPUT_VALUE = 2.0,
        *,
        fill_type: Literal["NONE", "NGON", "TRIANGLE_FAN"] = "NGON",
    ):
        super().__init__()
        key_args = {
            "Vertices": vertices,
            "Side Segments": side_segments,
            "Fill Segments": fill_segments,
            "Radius Top": radius_top,
            "Radius Bottom": radius_bottom,
            "Depth": depth,
        }
        self.fill_type = fill_type
        self._establish_links(**key_args)

    @property
    def i_vertices(self) -> SocketLinker:
        """Input socket: Vertices"""
        return self._input("Vertices")

    @property
    def i_side_segments(self) -> SocketLinker:
        """Input socket: Side Segments"""
        return self._input("Side Segments")

    @property
    def i_fill_segments(self) -> SocketLinker:
        """Input socket: Fill Segments"""
        return self._input("Fill Segments")

    @property
    def i_radius_top(self) -> SocketLinker:
        """Input socket: Radius Top"""
        return self._input("Radius Top")

    @property
    def i_radius_bottom(self) -> SocketLinker:
        """Input socket: Radius Bottom"""
        return self._input("Radius Bottom")

    @property
    def i_depth(self) -> SocketLinker:
        """Input socket: Depth"""
        return self._input("Depth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_top(self) -> SocketLinker:
        """Output socket: Top"""
        return self._output("Top")

    @property
    def o_bottom(self) -> SocketLinker:
        """Output socket: Bottom"""
        return self._output("Bottom")

    @property
    def o_side(self) -> SocketLinker:
        """Output socket: Side"""
        return self._output("Side")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")

    @property
    def fill_type(self) -> Literal["NONE", "NGON", "TRIANGLE_FAN"]:
        return self.node.fill_type

    @fill_type.setter
    def fill_type(self, value: Literal["NONE", "NGON", "TRIANGLE_FAN"]):
        self.node.fill_type = value


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


class Cube(NodeBuilder):
    """Generate a cuboid mesh with variable side lengths and subdivisions"""

    name = "GeometryNodeMeshCube"
    node: bpy.types.GeometryNodeMeshCube

    def __init__(
        self,
        size: TYPE_INPUT_VECTOR = None,
        vertices_x: TYPE_INPUT_INT = 2,
        vertices_y: TYPE_INPUT_INT = 2,
        vertices_z: TYPE_INPUT_INT = 2,
    ):
        super().__init__()
        key_args = {
            "Size": size,
            "Vertices X": vertices_x,
            "Vertices Y": vertices_y,
            "Vertices Z": vertices_z,
        }

        self._establish_links(**key_args)

    @property
    def i_size(self) -> SocketLinker:
        """Input socket: Size"""
        return self._input("Size")

    @property
    def i_vertices_x(self) -> SocketLinker:
        """Input socket: Vertices X"""
        return self._input("Vertices X")

    @property
    def i_vertices_y(self) -> SocketLinker:
        """Input socket: Vertices Y"""
        return self._input("Vertices Y")

    @property
    def i_vertices_z(self) -> SocketLinker:
        """Input socket: Vertices Z"""
        return self._input("Vertices Z")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")


class CurveCircle(NodeBuilder):
    """Generate a poly spline circle"""

    name = "GeometryNodeCurvePrimitiveCircle"
    node: bpy.types.GeometryNodeCurvePrimitiveCircle

    def __init__(
        self,
        resolution: TYPE_INPUT_INT = 32,
        point_1: TYPE_INPUT_VECTOR = None,
        point_2: TYPE_INPUT_VECTOR = None,
        point_3: TYPE_INPUT_VECTOR = None,
        radius: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["POINTS", "RADIUS"] = "RADIUS",
    ):
        super().__init__()
        key_args = {
            "Resolution": resolution,
            "Point 1": point_1,
            "Point 2": point_2,
            "Point 3": point_3,
            "Radius": radius,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_point_1(self) -> SocketLinker:
        """Input socket: Point 1"""
        return self._input("Point 1")

    @property
    def i_point_2(self) -> SocketLinker:
        """Input socket: Point 2"""
        return self._input("Point 2")

    @property
    def i_point_3(self) -> SocketLinker:
        """Input socket: Point 3"""
        return self._input("Point 3")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def o_center(self) -> SocketLinker:
        """Output socket: Center"""
        return self._output("Center")

    @property
    def mode(self) -> Literal["POINTS", "RADIUS"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["POINTS", "RADIUS"]):
        self.node.mode = value


class CurveLength(NodeBuilder):
    """Retrieve the length of all splines added together"""

    name = "GeometryNodeCurveLength"
    node: bpy.types.GeometryNodeCurveLength

    def __init__(self, curve: TYPE_INPUT_GEOMETRY = None):
        super().__init__()
        key_args = {"Curve": curve}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")


class CurveLine(NodeBuilder):
    """Generate a poly spline line with two points"""

    name = "GeometryNodeCurvePrimitiveLine"
    node: bpy.types.GeometryNodeCurvePrimitiveLine

    def __init__(
        self,
        start: TYPE_INPUT_VECTOR = None,
        end: TYPE_INPUT_VECTOR = None,
        direction: TYPE_INPUT_VECTOR = None,
        length: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["POINTS", "DIRECTION"] = "POINTS",
    ):
        super().__init__()
        key_args = {
            "Start": start,
            "End": end,
            "Direction": direction,
            "Length": length,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_start(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start")

    @property
    def i_end(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End")

    @property
    def i_direction(self) -> SocketLinker:
        """Input socket: Direction"""
        return self._input("Direction")

    @property
    def i_length(self) -> SocketLinker:
        """Input socket: Length"""
        return self._input("Length")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(self) -> Literal["POINTS", "DIRECTION"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["POINTS", "DIRECTION"]):
        self.node.mode = value


class CurveToMesh(NodeBuilder):
    """Convert curves into a mesh, optionally with a custom profile shape defined by curves"""

    name = "GeometryNodeCurveToMesh"
    node: bpy.types.GeometryNodeCurveToMesh

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        profile_curve: TYPE_INPUT_GEOMETRY = None,
        scale: TYPE_INPUT_VALUE = 1.0,
        fill_caps: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Profile Curve": profile_curve,
            "Scale": scale,
            "Fill Caps": fill_caps,
        }

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_profile_curve(self) -> SocketLinker:
        """Input socket: Profile Curve"""
        return self._input("Profile Curve")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_fill_caps(self) -> SocketLinker:
        """Input socket: Fill Caps"""
        return self._input("Fill Caps")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class CurveToPoints(NodeBuilder):
    """Generate a point cloud by sampling positions along curves"""

    name = "GeometryNodeCurveToPoints"
    node: bpy.types.GeometryNodeCurveToPoints

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        count: TYPE_INPUT_INT = 10,
        length: TYPE_INPUT_VALUE = 0.1,
        *,
        mode: Literal["EVALUATED", "COUNT", "LENGTH"] = "COUNT",
    ):
        super().__init__()
        key_args = {"Curve": curve, "Count": count, "Length": length}
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_length(self) -> SocketLinker:
        """Input socket: Length"""
        return self._input("Length")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def mode(self) -> Literal["EVALUATED", "COUNT", "LENGTH"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["EVALUATED", "COUNT", "LENGTH"]):
        self.node.mode = value


class CurvesToGreasePencil(NodeBuilder):
    """Convert the curves in each top-level instance into Grease Pencil layer"""

    name = "GeometryNodeCurvesToGreasePencil"
    node: bpy.types.GeometryNodeCurvesToGreasePencil

    def __init__(
        self,
        curves: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        instances_as_layers: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {
            "Curves": curves,
            "Selection": selection,
            "Instances as Layers": instances_as_layers,
        }

        self._establish_links(**key_args)

    @property
    def i_curves(self) -> SocketLinker:
        """Input socket: Curves"""
        return self._input("Curves")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_instances_as_layers(self) -> SocketLinker:
        """Input socket: Instances as Layers"""
        return self._input("Instances as Layers")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")


class Cylinder(NodeBuilder):
    """Generate a cylinder mesh"""

    name = "GeometryNodeMeshCylinder"
    node: bpy.types.GeometryNodeMeshCylinder

    def __init__(
        self,
        vertices: TYPE_INPUT_INT = 32,
        side_segments: TYPE_INPUT_INT = 1,
        fill_segments: TYPE_INPUT_INT = 1,
        radius: TYPE_INPUT_VALUE = 1.0,
        depth: TYPE_INPUT_VALUE = 2.0,
        *,
        fill_type: Literal["NONE", "NGON", "TRIANGLE_FAN"] = "NGON",
    ):
        super().__init__()
        key_args = {
            "Vertices": vertices,
            "Side Segments": side_segments,
            "Fill Segments": fill_segments,
            "Radius": radius,
            "Depth": depth,
        }
        self.fill_type = fill_type
        self._establish_links(**key_args)

    @property
    def i_vertices(self) -> SocketLinker:
        """Input socket: Vertices"""
        return self._input("Vertices")

    @property
    def i_side_segments(self) -> SocketLinker:
        """Input socket: Side Segments"""
        return self._input("Side Segments")

    @property
    def i_fill_segments(self) -> SocketLinker:
        """Input socket: Fill Segments"""
        return self._input("Fill Segments")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_depth(self) -> SocketLinker:
        """Input socket: Depth"""
        return self._input("Depth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_top(self) -> SocketLinker:
        """Output socket: Top"""
        return self._output("Top")

    @property
    def o_side(self) -> SocketLinker:
        """Output socket: Side"""
        return self._output("Side")

    @property
    def o_bottom(self) -> SocketLinker:
        """Output socket: Bottom"""
        return self._output("Bottom")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")

    @property
    def fill_type(self) -> Literal["NONE", "NGON", "TRIANGLE_FAN"]:
        return self.node.fill_type

    @fill_type.setter
    def fill_type(self, value: Literal["NONE", "NGON", "TRIANGLE_FAN"]):
        self.node.fill_type = value


class DeformCurvesOnSurface(NodeBuilder):
    """Translate and rotate curves based on changes between the object's original and evaluated surface mesh"""

    name = "GeometryNodeDeformCurvesOnSurface"
    node: bpy.types.GeometryNodeDeformCurvesOnSurface

    def __init__(self, curves: TYPE_INPUT_GEOMETRY = None):
        super().__init__()
        key_args = {"Curves": curves}

        self._establish_links(**key_args)

    @property
    def i_curves(self) -> SocketLinker:
        """Input socket: Curves"""
        return self._input("Curves")

    @property
    def o_curves(self) -> SocketLinker:
        """Output socket: Curves"""
        return self._output("Curves")


class DeleteGeometry(NodeBuilder):
    """Remove selected elements of a geometry"""

    name = "GeometryNodeDeleteGeometry"
    node: bpy.types.GeometryNodeDeleteGeometry

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        mode: Literal["ALL", "EDGE_FACE", "ONLY_FACE"] = "ALL",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self.mode = mode
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Point'."""
        return cls(domain="POINT", geometry=geometry, selection=selection)

    @classmethod
    def edge(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, selection=selection)

    @classmethod
    def face(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, selection=selection)

    @classmethod
    def spline(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Spline'."""
        return cls(domain="CURVE", geometry=geometry, selection=selection)

    @classmethod
    def instance(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Instance'."""
        return cls(domain="INSTANCE", geometry=geometry, selection=selection)

    @classmethod
    def layer(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "DeleteGeometry":
        """Create Delete Geometry with operation 'Layer'."""
        return cls(domain="LAYER", geometry=geometry, selection=selection)

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
    def mode(self) -> Literal["ALL", "EDGE_FACE", "ONLY_FACE"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["ALL", "EDGE_FACE", "ONLY_FACE"]):
        self.node.mode = value

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]
    ):
        self.node.domain = value


class DistributePointsOnFaces(NodeBuilder):
    """Generate points spread out on the surface of a mesh"""

    name = "GeometryNodeDistributePointsOnFaces"
    node: bpy.types.GeometryNodeDistributePointsOnFaces

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        distance_min: TYPE_INPUT_VALUE = 0.0,
        density_max: TYPE_INPUT_VALUE = 10.0,
        density: TYPE_INPUT_VALUE = 10.0,
        density_factor: TYPE_INPUT_VALUE = 1.0,
        seed: TYPE_INPUT_INT = 0,
        *,
        distribute_method: Literal["RANDOM", "POISSON"] = "RANDOM",
        use_legacy_normal: bool = False,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Distance Min": distance_min,
            "Density Max": density_max,
            "Density": density,
            "Density Factor": density_factor,
            "Seed": seed,
        }
        self.distribute_method = distribute_method
        self.use_legacy_normal = use_legacy_normal
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
    def i_distance_min(self) -> SocketLinker:
        """Input socket: Distance Min"""
        return self._input("Distance Min")

    @property
    def i_density_max(self) -> SocketLinker:
        """Input socket: Density Max"""
        return self._input("Density Max")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_density_factor(self) -> SocketLinker:
        """Input socket: Density Factor"""
        return self._input("Density Factor")

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


class DualMesh(NodeBuilder):
    """Convert Faces into vertices and vertices into faces"""

    name = "GeometryNodeDualMesh"
    node: bpy.types.GeometryNodeDualMesh

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        keep_boundaries: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Keep Boundaries": keep_boundaries}

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_keep_boundaries(self) -> SocketLinker:
        """Input socket: Keep Boundaries"""
        return self._input("Keep Boundaries")

    @property
    def o_dual_mesh(self) -> SocketLinker:
        """Output socket: Dual Mesh"""
        return self._output("Dual Mesh")


class DuplicateElements(NodeBuilder):
    """Generate an arbitrary number copies of each selected input element"""

    name = "GeometryNodeDuplicateElements"
    node: bpy.types.GeometryNodeDuplicateElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
        *,
        domain: Literal[
            "POINT", "EDGE", "FACE", "SPLINE", "LAYER", "INSTANCE"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Amount": amount}
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Point'."""
        return cls(
            domain="POINT", geometry=geometry, selection=selection, amount=amount
        )

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, selection=selection, amount=amount)

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, selection=selection, amount=amount)

    @classmethod
    def spline(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Spline'."""
        return cls(
            domain="SPLINE", geometry=geometry, selection=selection, amount=amount
        )

    @classmethod
    def layer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Layer'."""
        return cls(
            domain="LAYER", geometry=geometry, selection=selection, amount=amount
        )

    @classmethod
    def instance(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        amount: TYPE_INPUT_INT = 1,
    ) -> "DuplicateElements":
        """Create Duplicate Elements with operation 'Instance'."""
        return cls(
            domain="INSTANCE", geometry=geometry, selection=selection, amount=amount
        )

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
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "SPLINE", "LAYER", "INSTANCE"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "SPLINE", "LAYER", "INSTANCE"]
    ):
        self.node.domain = value


class EdgePathsToCurves(NodeBuilder):
    """Output curves following paths across mesh edges"""

    name = "GeometryNodeEdgePathsToCurves"
    node: bpy.types.GeometryNodeEdgePathsToCurves

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        start_vertices: TYPE_INPUT_BOOLEAN = True,
        next_vertex_index: TYPE_INPUT_INT = -1,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Start Vertices": start_vertices,
            "Next Vertex Index": next_vertex_index,
        }

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_start_vertices(self) -> SocketLinker:
        """Input socket: Start Vertices"""
        return self._input("Start Vertices")

    @property
    def i_next_vertex_index(self) -> SocketLinker:
        """Input socket: Next Vertex Index"""
        return self._input("Next Vertex Index")

    @property
    def o_curves(self) -> SocketLinker:
        """Output socket: Curves"""
        return self._output("Curves")


class ExtrudeMesh(NodeBuilder):
    """Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary"""

    name = "GeometryNodeExtrudeMesh"
    node: bpy.types.GeometryNodeExtrudeMesh

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        offset: TYPE_INPUT_VECTOR = None,
        offset_scale: TYPE_INPUT_VALUE = 1.0,
        individual: TYPE_INPUT_BOOLEAN = True,
        *,
        mode: Literal["VERTICES", "EDGES", "FACES"] = "FACES",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Offset": offset,
            "Offset Scale": offset_scale,
            "Individual": individual,
        }
        self.mode = mode
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
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def i_offset_scale(self) -> SocketLinker:
        """Input socket: Offset Scale"""
        return self._input("Offset Scale")

    @property
    def i_individual(self) -> SocketLinker:
        """Input socket: Individual"""
        return self._input("Individual")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_top(self) -> SocketLinker:
        """Output socket: Top"""
        return self._output("Top")

    @property
    def o_side(self) -> SocketLinker:
        """Output socket: Side"""
        return self._output("Side")

    @property
    def mode(self) -> Literal["VERTICES", "EDGES", "FACES"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["VERTICES", "EDGES", "FACES"]):
        self.node.mode = value


class FillCurve(NodeBuilder):
    """Generate a mesh on the XY plane with faces on the inside of input curves"""

    name = "GeometryNodeFillCurve"
    node: bpy.types.GeometryNodeFillCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        group_id: TYPE_INPUT_INT = 0,
        mode: TYPE_INPUT_MENU = "Triangles",
    ):
        super().__init__()
        key_args = {"Curve": curve, "Group ID": group_id, "Mode": mode}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class FilletCurve(NodeBuilder):
    """Round corners by generating circular arcs on each control point"""

    name = "GeometryNodeFilletCurve"
    node: bpy.types.GeometryNodeFilletCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        radius: TYPE_INPUT_VALUE = 0.25,
        limit_radius: TYPE_INPUT_BOOLEAN = False,
        mode: TYPE_INPUT_MENU = "Bézier",
        count: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Radius": radius,
            "Limit Radius": limit_radius,
            "Mode": mode,
            "Count": count,
        }

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_limit_radius(self) -> SocketLinker:
        """Input socket: Limit Radius"""
        return self._input("Limit Radius")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class FlipFaces(NodeBuilder):
    """Reverse the order of the vertices and edges of selected faces, flipping their normal direction"""

    name = "GeometryNodeFlipFaces"
    node: bpy.types.GeometryNodeFlipFaces

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
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


class GeometryProximity(NodeBuilder):
    """Compute the closest location on the target geometry"""

    name = "GeometryNodeProximity"
    node: bpy.types.GeometryNodeProximity

    def __init__(
        self,
        target: TYPE_INPUT_GEOMETRY = None,
        group_id: TYPE_INPUT_INT = 0,
        source_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
        *,
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
    def i_target(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Target")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_source_position(self) -> SocketLinker:
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


class GeometryToInstance(NodeBuilder):
    """Convert each input geometry into an instance, which can be much faster than the Join Geometry node when the inputs are large"""

    name = "GeometryNodeGeometryToInstance"
    node: bpy.types.GeometryNodeGeometryToInstance

    def __init__(self, geometry: TYPE_INPUT_GEOMETRY = None):
        super().__init__()
        key_args = {"Geometry": geometry}

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class GreasePencilToCurves(NodeBuilder):
    """Convert Grease Pencil layers into curve instances"""

    name = "GeometryNodeGreasePencilToCurves"
    node: bpy.types.GeometryNodeGreasePencilToCurves

    def __init__(
        self,
        grease_pencil: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        layers_as_instances: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Layers as Instances": layers_as_instances,
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
    def i_layers_as_instances(self) -> SocketLinker:
        """Input socket: Layers as Instances"""
        return self._input("Layers as Instances")

    @property
    def o_curves(self) -> SocketLinker:
        """Output socket: Curves"""
        return self._output("Curves")


class Grid(NodeBuilder):
    """Generate a planar mesh on the XY plane"""

    name = "GeometryNodeMeshGrid"
    node: bpy.types.GeometryNodeMeshGrid

    def __init__(
        self,
        size_x: TYPE_INPUT_VALUE = 1.0,
        size_y: TYPE_INPUT_VALUE = 1.0,
        vertices_x: TYPE_INPUT_INT = 3,
        vertices_y: TYPE_INPUT_INT = 3,
    ):
        super().__init__()
        key_args = {
            "Size X": size_x,
            "Size Y": size_y,
            "Vertices X": vertices_x,
            "Vertices Y": vertices_y,
        }

        self._establish_links(**key_args)

    @property
    def i_size_x(self) -> SocketLinker:
        """Input socket: Size X"""
        return self._input("Size X")

    @property
    def i_size_y(self) -> SocketLinker:
        """Input socket: Size Y"""
        return self._input("Size Y")

    @property
    def i_vertices_x(self) -> SocketLinker:
        """Input socket: Vertices X"""
        return self._input("Vertices X")

    @property
    def i_vertices_y(self) -> SocketLinker:
        """Input socket: Vertices Y"""
        return self._input("Vertices Y")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")


class IcoSphere(NodeBuilder):
    """Generate a spherical mesh that consists of equally sized triangles"""

    name = "GeometryNodeMeshIcoSphere"
    node: bpy.types.GeometryNodeMeshIcoSphere

    def __init__(
        self,
        radius: TYPE_INPUT_VALUE = 1.0,
        subdivisions: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Radius": radius, "Subdivisions": subdivisions}

        self._establish_links(**key_args)

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_subdivisions(self) -> SocketLinker:
        """Input socket: Subdivisions"""
        return self._input("Subdivisions")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")


class InstanceOnPoints(NodeBuilder):
    """Generate a reference to geometry at each of the input points, without duplicating its underlying data"""

    name = "GeometryNodeInstanceOnPoints"
    node: bpy.types.GeometryNodeInstanceOnPoints

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        instance: TYPE_INPUT_GEOMETRY = None,
        pick_instance: TYPE_INPUT_BOOLEAN = False,
        instance_index: TYPE_INPUT_INT = 0,
        rotation: TYPE_INPUT_ROTATION = None,
        scale: TYPE_INPUT_VECTOR = None,
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
        selection: TYPE_INPUT_BOOLEAN = True,
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


class InterpolateCurves(NodeBuilder):
    """Generate new curves on points by interpolating between existing curves"""

    name = "GeometryNodeInterpolateCurves"
    node: bpy.types.GeometryNodeInterpolateCurves

    def __init__(
        self,
        guide_curves: TYPE_INPUT_GEOMETRY = None,
        guide_up: TYPE_INPUT_VECTOR = None,
        guide_group_id: TYPE_INPUT_INT = 0,
        points: TYPE_INPUT_GEOMETRY = None,
        point_up: TYPE_INPUT_VECTOR = None,
        point_group_id: TYPE_INPUT_INT = 0,
        max_neighbors: TYPE_INPUT_INT = 4,
    ):
        super().__init__()
        key_args = {
            "Guide Curves": guide_curves,
            "Guide Up": guide_up,
            "Guide Group ID": guide_group_id,
            "Points": points,
            "Point Up": point_up,
            "Point Group ID": point_group_id,
            "Max Neighbors": max_neighbors,
        }

        self._establish_links(**key_args)

    @property
    def i_guide_curves(self) -> SocketLinker:
        """Input socket: Guide Curves"""
        return self._input("Guide Curves")

    @property
    def i_guide_up(self) -> SocketLinker:
        """Input socket: Guide Up"""
        return self._input("Guide Up")

    @property
    def i_guide_group_id(self) -> SocketLinker:
        """Input socket: Guide Group ID"""
        return self._input("Guide Group ID")

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_point_up(self) -> SocketLinker:
        """Input socket: Point Up"""
        return self._input("Point Up")

    @property
    def i_point_group_id(self) -> SocketLinker:
        """Input socket: Point Group ID"""
        return self._input("Point Group ID")

    @property
    def i_max_neighbors(self) -> SocketLinker:
        """Input socket: Max Neighbors"""
        return self._input("Max Neighbors")

    @property
    def o_curves(self) -> SocketLinker:
        """Output socket: Curves"""
        return self._output("Curves")

    @property
    def o_closest_index(self) -> SocketLinker:
        """Output socket: Closest Index"""
        return self._output("Closest Index")

    @property
    def o_closest_weight(self) -> SocketLinker:
        """Output socket: Closest Weight"""
        return self._output("Closest Weight")


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
        grease_pencil: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        *,
        mode: Literal["MERGE_BY_NAME", "MERGE_BY_ID"] = "MERGE_BY_NAME",
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Group ID": group_id,
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
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
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
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: TYPE_INPUT_MENU = "All",
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


class MeshBoolean(NodeBuilder):
    """Cut, subtract, or join multiple mesh inputs"""

    name = "GeometryNodeMeshBoolean"
    node: bpy.types.GeometryNodeMeshBoolean

    def __init__(
        self,
        mesh_1: TYPE_INPUT_GEOMETRY = None,
        mesh_2: TYPE_INPUT_GEOMETRY = None,
        self_intersection: TYPE_INPUT_BOOLEAN = False,
        hole_tolerant: TYPE_INPUT_BOOLEAN = False,
        *,
        operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE",
        solver: Literal["EXACT", "FLOAT", "MANIFOLD"] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Mesh 1": mesh_1,
            "Mesh 2": mesh_2,
            "Self Intersection": self_intersection,
            "Hole Tolerant": hole_tolerant,
        }
        self.operation = operation
        self.solver = solver
        self._establish_links(**key_args)

    @classmethod
    def intersect(cls, mesh_2: TYPE_INPUT_GEOMETRY = None) -> "MeshBoolean":
        """Create Mesh Boolean with operation 'Intersect'."""
        return cls(operation="INTERSECT", mesh_2=mesh_2)

    @classmethod
    def union(cls, mesh_2: TYPE_INPUT_GEOMETRY = None) -> "MeshBoolean":
        """Create Mesh Boolean with operation 'Union'."""
        return cls(operation="UNION", mesh_2=mesh_2)

    @classmethod
    def difference(
        cls, mesh_1: TYPE_INPUT_GEOMETRY = None, mesh_2: TYPE_INPUT_GEOMETRY = None
    ) -> "MeshBoolean":
        """Create Mesh Boolean with operation 'Difference'."""
        return cls(operation="DIFFERENCE", mesh_1=mesh_1, mesh_2=mesh_2)

    @property
    def i_mesh_1(self) -> SocketLinker:
        """Input socket: Mesh 1"""
        return self._input("Mesh 1")

    @property
    def i_mesh_2(self) -> SocketLinker:
        """Input socket: Mesh 2"""
        return self._input("Mesh 2")

    @property
    def i_self_intersection(self) -> SocketLinker:
        """Input socket: Self Intersection"""
        return self._input("Self Intersection")

    @property
    def i_hole_tolerant(self) -> SocketLinker:
        """Input socket: Hole Tolerant"""
        return self._input("Hole Tolerant")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_intersecting_edges(self) -> SocketLinker:
        """Output socket: Intersecting Edges"""
        return self._output("Intersecting Edges")

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value

    @property
    def solver(self) -> Literal["EXACT", "FLOAT", "MANIFOLD"]:
        return self.node.solver

    @solver.setter
    def solver(self, value: Literal["EXACT", "FLOAT", "MANIFOLD"]):
        self.node.solver = value


class MeshCircle(NodeBuilder):
    """Generate a circular ring of edges"""

    name = "GeometryNodeMeshCircle"
    node: bpy.types.GeometryNodeMeshCircle

    def __init__(
        self,
        vertices: TYPE_INPUT_INT = 32,
        radius: TYPE_INPUT_VALUE = 1.0,
        *,
        fill_type: Literal["NONE", "NGON", "TRIANGLE_FAN"] = "NONE",
    ):
        super().__init__()
        key_args = {"Vertices": vertices, "Radius": radius}
        self.fill_type = fill_type
        self._establish_links(**key_args)

    @property
    def i_vertices(self) -> SocketLinker:
        """Input socket: Vertices"""
        return self._input("Vertices")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def fill_type(self) -> Literal["NONE", "NGON", "TRIANGLE_FAN"]:
        return self.node.fill_type

    @fill_type.setter
    def fill_type(self, value: Literal["NONE", "NGON", "TRIANGLE_FAN"]):
        self.node.fill_type = value


class MeshLine(NodeBuilder):
    """Generate vertices in a line and connect them with edges"""

    name = "GeometryNodeMeshLine"
    node: bpy.types.GeometryNodeMeshLine

    def __init__(
        self,
        count: TYPE_INPUT_INT = 10,
        resolution: TYPE_INPUT_VALUE = 1.0,
        start_location: TYPE_INPUT_VECTOR = None,
        offset: TYPE_INPUT_VECTOR = None,
        *,
        mode: Literal["OFFSET", "END_POINTS"] = "OFFSET",
        count_mode: Literal["TOTAL", "RESOLUTION"] = "TOTAL",
    ):
        super().__init__()
        key_args = {
            "Count": count,
            "Resolution": resolution,
            "Start Location": start_location,
            "Offset": offset,
        }
        self.mode = mode
        self.count_mode = count_mode
        self._establish_links(**key_args)

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_start_location(self) -> SocketLinker:
        """Input socket: Start Location"""
        return self._input("Start Location")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def mode(self) -> Literal["OFFSET", "END_POINTS"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["OFFSET", "END_POINTS"]):
        self.node.mode = value

    @property
    def count_mode(self) -> Literal["TOTAL", "RESOLUTION"]:
        return self.node.count_mode

    @count_mode.setter
    def count_mode(self, value: Literal["TOTAL", "RESOLUTION"]):
        self.node.count_mode = value


class MeshToCurve(NodeBuilder):
    """Generate a curve from a mesh"""

    name = "GeometryNodeMeshToCurve"
    node: bpy.types.GeometryNodeMeshToCurve

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        mode: Literal["EDGES", "FACES"] = "EDGES",
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection}
        self.mode = mode
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
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(self) -> Literal["EDGES", "FACES"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["EDGES", "FACES"]):
        self.node.mode = value


class MeshToPoints(NodeBuilder):
    """Generate a point cloud from a mesh's vertices"""

    name = "GeometryNodeMeshToPoints"
    node: bpy.types.GeometryNodeMeshToPoints

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        position: TYPE_INPUT_VECTOR = None,
        radius: TYPE_INPUT_VALUE = 0.05,
        *,
        mode: Literal["VERTICES", "EDGES", "FACES", "CORNERS"] = "VERTICES",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Position": position,
            "Radius": radius,
        }
        self.mode = mode
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

    @property
    def mode(self) -> Literal["VERTICES", "EDGES", "FACES", "CORNERS"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["VERTICES", "EDGES", "FACES", "CORNERS"]):
        self.node.mode = value


class Points(NodeBuilder):
    """Generate a point cloud with positions and radii defined by fields"""

    name = "GeometryNodePoints"
    node: bpy.types.GeometryNodePoints

    def __init__(
        self,
        count: TYPE_INPUT_INT = 1,
        position: TYPE_INPUT_VECTOR = None,
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
    def o_geometry(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Geometry")


class PointsToCurves(NodeBuilder):
    """Split all points to curve by its group ID and reorder by weight"""

    name = "GeometryNodePointsToCurves"
    node: bpy.types.GeometryNodePointsToCurves

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        curve_group_id: TYPE_INPUT_INT = 0,
        weight: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Curve Group ID": curve_group_id,
            "Weight": weight,
        }

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_curve_group_id(self) -> SocketLinker:
        """Input socket: Curve Group ID"""
        return self._input("Curve Group ID")

    @property
    def i_weight(self) -> SocketLinker:
        """Input socket: Weight"""
        return self._input("Weight")

    @property
    def o_curves(self) -> SocketLinker:
        """Output socket: Curves"""
        return self._output("Curves")


class PointsToVertices(NodeBuilder):
    """Generate a mesh vertex for each point cloud point"""

    name = "GeometryNodePointsToVertices"
    node: bpy.types.GeometryNodePointsToVertices

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
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


class QuadraticBezier(NodeBuilder):
    """Generate a poly spline in a parabola shape with control points positions"""

    name = "GeometryNodeCurveQuadraticBezier"
    node: bpy.types.GeometryNodeCurveQuadraticBezier

    def __init__(
        self,
        resolution: TYPE_INPUT_INT = 16,
        start: TYPE_INPUT_VECTOR = None,
        middle: TYPE_INPUT_VECTOR = None,
        end: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {
            "Resolution": resolution,
            "Start": start,
            "Middle": middle,
            "End": end,
        }

        self._establish_links(**key_args)

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_start(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start")

    @property
    def i_middle(self) -> SocketLinker:
        """Input socket: Middle"""
        return self._input("Middle")

    @property
    def i_end(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class Quadrilateral(NodeBuilder):
    """Generate a polygon with four points"""

    name = "GeometryNodeCurvePrimitiveQuadrilateral"
    node: bpy.types.GeometryNodeCurvePrimitiveQuadrilateral

    def __init__(
        self,
        width: TYPE_INPUT_VALUE = 2.0,
        height: TYPE_INPUT_VALUE = 2.0,
        bottom_width: TYPE_INPUT_VALUE = 4.0,
        top_width: TYPE_INPUT_VALUE = 2.0,
        offset: TYPE_INPUT_VALUE = 1.0,
        bottom_height: TYPE_INPUT_VALUE = 3.0,
        top_height: TYPE_INPUT_VALUE = 1.0,
        point_1: TYPE_INPUT_VECTOR = None,
        point_2: TYPE_INPUT_VECTOR = None,
        point_3: TYPE_INPUT_VECTOR = None,
        point_4: TYPE_INPUT_VECTOR = None,
        *,
        mode: Literal[
            "RECTANGLE", "PARALLELOGRAM", "TRAPEZOID", "KITE", "POINTS"
        ] = "RECTANGLE",
    ):
        super().__init__()
        key_args = {
            "Width": width,
            "Height": height,
            "Bottom Width": bottom_width,
            "Top Width": top_width,
            "Offset": offset,
            "Bottom Height": bottom_height,
            "Top Height": top_height,
            "Point 1": point_1,
            "Point 2": point_2,
            "Point 3": point_3,
            "Point 4": point_4,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_width(self) -> SocketLinker:
        """Input socket: Width"""
        return self._input("Width")

    @property
    def i_height(self) -> SocketLinker:
        """Input socket: Height"""
        return self._input("Height")

    @property
    def i_bottom_width(self) -> SocketLinker:
        """Input socket: Bottom Width"""
        return self._input("Bottom Width")

    @property
    def i_top_width(self) -> SocketLinker:
        """Input socket: Top Width"""
        return self._input("Top Width")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def i_bottom_height(self) -> SocketLinker:
        """Input socket: Bottom Height"""
        return self._input("Bottom Height")

    @property
    def i_top_height(self) -> SocketLinker:
        """Input socket: Top Height"""
        return self._input("Top Height")

    @property
    def i_point_1(self) -> SocketLinker:
        """Input socket: Point 1"""
        return self._input("Point 1")

    @property
    def i_point_2(self) -> SocketLinker:
        """Input socket: Point 2"""
        return self._input("Point 2")

    @property
    def i_point_3(self) -> SocketLinker:
        """Input socket: Point 3"""
        return self._input("Point 3")

    @property
    def i_point_4(self) -> SocketLinker:
        """Input socket: Point 4"""
        return self._input("Point 4")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(
        self,
    ) -> Literal["RECTANGLE", "PARALLELOGRAM", "TRAPEZOID", "KITE", "POINTS"]:
        return self.node.mode

    @mode.setter
    def mode(
        self,
        value: Literal["RECTANGLE", "PARALLELOGRAM", "TRAPEZOID", "KITE", "POINTS"],
    ):
        self.node.mode = value


class Raycast(NodeBuilder):
    """Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point"""

    name = "GeometryNodeRaycast"
    node: bpy.types.GeometryNodeRaycast

    def __init__(
        self,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_VALUE = 0.0,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
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

    @classmethod
    def float(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_VALUE = 0.0,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

    @classmethod
    def integer(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_INT = 0,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Integer'."""
        return cls(
            data_type="INT",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

    @classmethod
    def boolean(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_BOOLEAN = False,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

    @classmethod
    def vector(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

    @classmethod
    def color(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_COLOR = None,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

    @classmethod
    def quaternion(
        cls,
        target_geometry: TYPE_INPUT_GEOMETRY = None,
        attribute: TYPE_INPUT_ROTATION = None,
        interpolation: TYPE_INPUT_MENU = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = None,
        ray_direction: TYPE_INPUT_VECTOR = None,
        ray_length: TYPE_INPUT_VALUE = 100.0,
    ) -> "Raycast":
        """Create Raycast with operation 'Quaternion'."""
        return cls(
            data_type="QUATERNION",
            target_geometry=target_geometry,
            attribute=attribute,
            interpolation=interpolation,
            source_position=source_position,
            ray_direction=ray_direction,
            ray_length=ray_length,
        )

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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ],
    ):
        self.node.data_type = value


class RealizeInstances(NodeBuilder):
    """Convert instances into real geometry data"""

    name = "GeometryNodeRealizeInstances"
    node: bpy.types.GeometryNodeRealizeInstances

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
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


class ResampleCurve(NodeBuilder):
    """Generate a poly spline for each input spline"""

    name = "GeometryNodeResampleCurve"
    node: bpy.types.GeometryNodeResampleCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: TYPE_INPUT_MENU = "Count",
        count: TYPE_INPUT_INT = 10,
        length: TYPE_INPUT_VALUE = 0.1,
        *,
        keep_last_segment: bool = False,
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Selection": selection,
            "Mode": mode,
            "Count": count,
            "Length": length,
        }
        self.keep_last_segment = keep_last_segment
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_length(self) -> SocketLinker:
        """Input socket: Length"""
        return self._input("Length")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def keep_last_segment(self) -> bool:
        return self.node.keep_last_segment

    @keep_last_segment.setter
    def keep_last_segment(self, value: bool):
        self.node.keep_last_segment = value


class ReverseCurve(NodeBuilder):
    """Change the direction of curves by swapping their start and end data"""

    name = "GeometryNodeReverseCurve"
    node: bpy.types.GeometryNodeReverseCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class RotateInstances(NodeBuilder):
    """Rotate geometry instances in local or global space"""

    name = "GeometryNodeRotateInstances"
    node: bpy.types.GeometryNodeRotateInstances

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        rotation: TYPE_INPUT_ROTATION = None,
        pivot_point: TYPE_INPUT_VECTOR = None,
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


class SampleCurve(NodeBuilder):
    """Retrieve data from a point on a curve at a certain distance from its start"""

    name = "GeometryNodeSampleCurve"
    node: bpy.types.GeometryNodeSampleCurve

    def __init__(
        self,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        factor: TYPE_INPUT_VALUE = 0.0,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
        *,
        mode: Literal["FACTOR", "LENGTH"] = "FACTOR",
        use_all_curves: bool = False,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Curves": curves,
            "Value": value,
            "Factor": factor,
            "Length": length,
            "Curve Index": curve_index,
        }
        self.mode = mode
        self.use_all_curves = use_all_curves
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @classmethod
    def integer(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_INT = 0,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Integer'."""
        return cls(
            data_type="INT",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @classmethod
    def boolean(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_BOOLEAN = False,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @classmethod
    def vector(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VECTOR = None,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @classmethod
    def color(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_COLOR = None,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @classmethod
    def quaternion(
        cls,
        curves: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_ROTATION = None,
        length: TYPE_INPUT_VALUE = 0.0,
        curve_index: TYPE_INPUT_INT = 0,
    ) -> "SampleCurve":
        """Create Sample Curve with operation 'Quaternion'."""
        return cls(
            data_type="QUATERNION",
            curves=curves,
            value=value,
            length=length,
            curve_index=curve_index,
        )

    @property
    def i_curves(self) -> SocketLinker:
        """Input socket: Curves"""
        return self._input("Curves")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_factor(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Factor")

    @property
    def i_length(self) -> SocketLinker:
        """Input socket: Length"""
        return self._input("Length")

    @property
    def i_curve_index(self) -> SocketLinker:
        """Input socket: Curve Index"""
        return self._input("Curve Index")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def mode(self) -> Literal["FACTOR", "LENGTH"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["FACTOR", "LENGTH"]):
        self.node.mode = value

    @property
    def use_all_curves(self) -> bool:
        return self.node.use_all_curves

    @use_all_curves.setter
    def use_all_curves(self, value: bool):
        self.node.use_all_curves = value

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ],
    ):
        self.node.data_type = value


class SampleIndex(NodeBuilder):
    """Retrieve values from specific geometry elements"""

    name = "GeometryNodeSampleIndex"
    node: bpy.types.GeometryNodeSampleIndex

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        clamp: bool = False,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Value": value, "Index": index}
        self.data_type = data_type
        self.domain = domain
        self.clamp = clamp
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Float'."""
        return cls(data_type="FLOAT", geometry=geometry, value=value, index=index)

    @classmethod
    def integer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_INT = 0,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Integer'."""
        return cls(data_type="INT", geometry=geometry, value=value, index=index)

    @classmethod
    def boolean(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_BOOLEAN = False,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", geometry=geometry, value=value, index=index)

    @classmethod
    def vector(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VECTOR = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR", geometry=geometry, value=value, index=index
        )

    @classmethod
    def color(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_COLOR = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Color'."""
        return cls(data_type="FLOAT_COLOR", geometry=geometry, value=value, index=index)

    @classmethod
    def quaternion(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_ROTATION = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Quaternion'."""
        return cls(data_type="QUATERNION", geometry=geometry, value=value, index=index)

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Point'."""
        return cls(domain="POINT", geometry=geometry, value=value, index=index)

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, value=value, index=index)

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, value=value, index=index)

    @classmethod
    def spline(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Spline'."""
        return cls(domain="CURVE", geometry=geometry, value=value, index=index)

    @classmethod
    def instance(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Instance'."""
        return cls(domain="INSTANCE", geometry=geometry, value=value, index=index)

    @classmethod
    def layer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_MATRIX = None,
        index: TYPE_INPUT_INT = 0,
    ) -> "SampleIndex":
        """Create Sample Index with operation 'Layer'."""
        return cls(domain="LAYER", geometry=geometry, value=value, index=index)

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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ],
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: Literal["POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"],
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
        *,
        domain: Literal["POINT", "EDGE", "FACE", "CORNER"] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Sample Position": sample_position}
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        sample_position: TYPE_INPUT_VECTOR = None,
    ) -> "SampleNearest":
        """Create Sample Nearest with operation 'Point'."""
        return cls(domain="POINT", geometry=geometry, sample_position=sample_position)

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        sample_position: TYPE_INPUT_VECTOR = None,
    ) -> "SampleNearest":
        """Create Sample Nearest with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, sample_position=sample_position)

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        sample_position: TYPE_INPUT_VECTOR = None,
    ) -> "SampleNearest":
        """Create Sample Nearest with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, sample_position=sample_position)

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
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Value": value,
            "Group ID": group_id,
            "Sample Position": sample_position,
            "Sample Group ID": sample_group_id,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

    @classmethod
    def integer(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_INT = 0,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Integer'."""
        return cls(
            data_type="INT",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

    @classmethod
    def boolean(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_BOOLEAN = False,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

    @classmethod
    def vector(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VECTOR = None,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

    @classmethod
    def color(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_COLOR = None,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

    @classmethod
    def quaternion(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_ROTATION = None,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = None,
        sample_group_id: TYPE_INPUT_INT = 0,
    ) -> "SampleNearestSurface":
        """Create Sample Nearest Surface with operation 'Quaternion'."""
        return cls(
            data_type="QUATERNION",
            mesh=mesh,
            value=value,
            group_id=group_id,
            sample_position=sample_position,
            sample_group_id=sample_group_id,
        )

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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ],
    ):
        self.node.data_type = value


class SampleUVSurface(NodeBuilder):
    """Calculate the interpolated values of a mesh attribute at a UV coordinate"""

    name = "GeometryNodeSampleUVSurface"
    node: bpy.types.GeometryNodeSampleUVSurface

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
        *,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ] = "FLOAT",
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

    @classmethod
    def float(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VALUE = 0.0,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @classmethod
    def integer(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_INT = 0,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Integer'."""
        return cls(
            data_type="INT",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @classmethod
    def boolean(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_BOOLEAN = False,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @classmethod
    def vector(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_VECTOR = None,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @classmethod
    def color(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_COLOR = None,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Color'."""
        return cls(
            data_type="FLOAT_COLOR",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @classmethod
    def quaternion(
        cls,
        mesh: TYPE_INPUT_GEOMETRY = None,
        value: TYPE_INPUT_ROTATION = None,
        source_uv_map: TYPE_INPUT_VECTOR = None,
        sample_uv: TYPE_INPUT_VECTOR = None,
    ) -> "SampleUVSurface":
        """Create Sample UV Surface with operation 'Quaternion'."""
        return cls(
            data_type="QUATERNION",
            mesh=mesh,
            value=value,
            source_uv_map=source_uv_map,
            sample_uv=sample_uv,
        )

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_source_uv_map(self) -> SocketLinker:
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
        ],
    ):
        self.node.data_type = value


class ScaleElements(NodeBuilder):
    """Scale groups of connected edges and faces"""

    name = "GeometryNodeScaleElements"
    node: bpy.types.GeometryNodeScaleElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VALUE = 1.0,
        center: TYPE_INPUT_VECTOR = None,
        scale_mode: TYPE_INPUT_MENU = "Uniform",
        axis: TYPE_INPUT_VECTOR = None,
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

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VALUE = 1.0,
        center: TYPE_INPUT_VECTOR = None,
        scale_mode: TYPE_INPUT_MENU = "Uniform",
    ) -> "ScaleElements":
        """Create Scale Elements with operation 'Face'."""
        return cls(
            domain="FACE",
            geometry=geometry,
            selection=selection,
            scale=scale,
            center=center,
            scale_mode=scale_mode,
        )

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VALUE = 1.0,
        center: TYPE_INPUT_VECTOR = None,
        scale_mode: TYPE_INPUT_MENU = "Uniform",
    ) -> "ScaleElements":
        """Create Scale Elements with operation 'Edge'."""
        return cls(
            domain="EDGE",
            geometry=geometry,
            selection=selection,
            scale=scale,
            center=center,
            scale_mode=scale_mode,
        )

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


class ScaleInstances(NodeBuilder):
    """Scale geometry instances in local or global space"""

    name = "GeometryNodeScaleInstances"
    node: bpy.types.GeometryNodeScaleInstances

    def __init__(
        self,
        instances: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VECTOR = None,
        center: TYPE_INPUT_VECTOR = None,
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
        *,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Point'."""
        return cls(domain="POINT", geometry=geometry, selection=selection)

    @classmethod
    def edge(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, selection=selection)

    @classmethod
    def face(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, selection=selection)

    @classmethod
    def spline(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Spline'."""
        return cls(domain="CURVE", geometry=geometry, selection=selection)

    @classmethod
    def instance(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Instance'."""
        return cls(domain="INSTANCE", geometry=geometry, selection=selection)

    @classmethod
    def layer(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SeparateGeometry":
        """Create Separate Geometry with operation 'Layer'."""
        return cls(domain="LAYER", geometry=geometry, selection=selection)

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
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]
    ):
        self.node.domain = value


class SetCurveNormal(NodeBuilder):
    """Set the evaluation mode for curve normals"""

    name = "GeometryNodeSetCurveNormal"
    node: bpy.types.GeometryNodeSetCurveNormal

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: TYPE_INPUT_MENU = "Minimum Twist",
        normal: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Selection": selection,
            "Mode": mode,
            "Normal": normal,
        }

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_normal(self) -> SocketLinker:
        """Input socket: Normal"""
        return self._input("Normal")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class SetCurveRadius(NodeBuilder):
    """Set the radius of the curve at each control point"""

    name = "GeometryNodeSetCurveRadius"
    node: bpy.types.GeometryNodeSetCurveRadius

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        radius: TYPE_INPUT_VALUE = 0.005,
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection, "Radius": radius}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class SetCurveTilt(NodeBuilder):
    """Set the tilt angle at each curve control point"""

    name = "GeometryNodeSetCurveTilt"
    node: bpy.types.GeometryNodeSetCurveTilt

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        tilt: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection, "Tilt": tilt}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_tilt(self) -> SocketLinker:
        """Input socket: Tilt"""
        return self._input("Tilt")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


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


class SetGeometryName(NodeBuilder):
    """Set the name of a geometry for easier debugging"""

    name = "GeometryNodeSetGeometryName"
    node: bpy.types.GeometryNodeSetGeometryName

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
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
        grease_pencil: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        color: TYPE_INPUT_COLOR = None,
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
        *,
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


class SetHandlePositions(NodeBuilder):
    """Set the positions for the handles of Bézier curves"""

    name = "GeometryNodeSetCurveHandlePositions"
    node: bpy.types.GeometryNodeSetCurveHandlePositions

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        position: TYPE_INPUT_VECTOR = None,
        offset: TYPE_INPUT_VECTOR = None,
        *,
        mode: Literal["LEFT", "RIGHT"] = "LEFT",
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Selection": selection,
            "Position": position,
            "Offset": offset,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

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
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(self) -> Literal["LEFT", "RIGHT"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["LEFT", "RIGHT"]):
        self.node.mode = value


class SetID(NodeBuilder):
    """Set the id attribute on the input geometry, mainly used internally for randomizing"""

    name = "GeometryNodeSetID"
    node: bpy.types.GeometryNodeSetID

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        id: TYPE_INPUT_INT = 0,
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


class SetMeshNormal(NodeBuilder):
    """Store a normal vector for each mesh element"""

    name = "GeometryNodeSetMeshNormal"
    node: bpy.types.GeometryNodeSetMeshNormal

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        remove_custom: TYPE_INPUT_BOOLEAN = True,
        edge_sharpness: TYPE_INPUT_BOOLEAN = False,
        face_sharpness: TYPE_INPUT_BOOLEAN = False,
        *,
        mode: Literal["SHARPNESS", "FREE", "TANGENT_SPACE"] = "SHARPNESS",
        domain: Literal["POINT", "FACE", "CORNER"] = "POINT",
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Remove Custom": remove_custom,
            "Edge Sharpness": edge_sharpness,
            "Face Sharpness": face_sharpness,
        }
        self.mode = mode
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls, mesh: TYPE_INPUT_GEOMETRY = None, custom_normal: TYPE_INPUT_VECTOR = None
    ) -> "SetMeshNormal":
        """Create Set Mesh Normal with operation 'Point'."""
        return cls(domain="POINT", mesh=mesh, custom_normal=custom_normal)

    @classmethod
    def face(
        cls, mesh: TYPE_INPUT_GEOMETRY = None, custom_normal: TYPE_INPUT_VECTOR = None
    ) -> "SetMeshNormal":
        """Create Set Mesh Normal with operation 'Face'."""
        return cls(domain="FACE", mesh=mesh, custom_normal=custom_normal)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_remove_custom(self) -> SocketLinker:
        """Input socket: Remove Custom"""
        return self._input("Remove Custom")

    @property
    def i_edge_sharpness(self) -> SocketLinker:
        """Input socket: Edge Sharpness"""
        return self._input("Edge Sharpness")

    @property
    def i_face_sharpness(self) -> SocketLinker:
        """Input socket: Face Sharpness"""
        return self._input("Face Sharpness")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def mode(self) -> Literal["SHARPNESS", "FREE", "TANGENT_SPACE"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["SHARPNESS", "FREE", "TANGENT_SPACE"]):
        self.node.mode = value

    @property
    def domain(self) -> Literal["POINT", "FACE", "CORNER"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "FACE", "CORNER"]):
        self.node.domain = value


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
        offset: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Position": position,
            "Offset": offset,
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

    @classmethod
    def point(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SetSelection":
        """Create Set Selection with operation 'Point'."""
        return cls(domain="POINT", geometry=geometry, selection=selection)

    @classmethod
    def edge(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SetSelection":
        """Create Set Selection with operation 'Edge'."""
        return cls(domain="EDGE", geometry=geometry, selection=selection)

    @classmethod
    def face(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SetSelection":
        """Create Set Selection with operation 'Face'."""
        return cls(domain="FACE", geometry=geometry, selection=selection)

    @classmethod
    def spline(
        cls, geometry: TYPE_INPUT_GEOMETRY = None, selection: TYPE_INPUT_BOOLEAN = True
    ) -> "SetSelection":
        """Create Set Selection with operation 'Spline'."""
        return cls(domain="CURVE", geometry=geometry, selection=selection)

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

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        shade_smooth: TYPE_INPUT_BOOLEAN = True,
    ) -> "SetShadeSmooth":
        """Create Set Shade Smooth with operation 'Edge'."""
        return cls(
            domain="EDGE",
            geometry=geometry,
            selection=selection,
            shade_smooth=shade_smooth,
        )

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        shade_smooth: TYPE_INPUT_BOOLEAN = True,
    ) -> "SetShadeSmooth":
        """Create Set Shade Smooth with operation 'Face'."""
        return cls(
            domain="FACE",
            geometry=geometry,
            selection=selection,
            shade_smooth=shade_smooth,
        )

    @property
    def i_geometry(self) -> SocketLinker:
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
    def o_geometry(self) -> SocketLinker:
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
    def i_geometry(self) -> SocketLinker:
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
    def o_geometry(self) -> SocketLinker:
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
    def i_geometry(self) -> SocketLinker:
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
    def o_geometry(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Geometry")


class SetSplineType(NodeBuilder):
    """Change the type of curves"""

    name = "GeometryNodeCurveSplineType"
    node: bpy.types.GeometryNodeCurveSplineType

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        spline_type: Literal["CATMULL_ROM", "POLY", "BEZIER", "NURBS"] = "POLY",
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection}
        self.spline_type = spline_type
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def spline_type(self) -> Literal["CATMULL_ROM", "POLY", "BEZIER", "NURBS"]:
        return self.node.spline_type

    @spline_type.setter
    def spline_type(self, value: Literal["CATMULL_ROM", "POLY", "BEZIER", "NURBS"]):
        self.node.spline_type = value


class SortElements(NodeBuilder):
    """Rearrange geometry elements, changing their indices"""

    name = "GeometryNodeSortElements"
    node: bpy.types.GeometryNodeSortElements

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
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

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
    ) -> "SortElements":
        """Create Sort Elements with operation 'Point'."""
        return cls(
            domain="POINT",
            geometry=geometry,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
        )

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
    ) -> "SortElements":
        """Create Sort Elements with operation 'Edge'."""
        return cls(
            domain="EDGE",
            geometry=geometry,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
        )

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
    ) -> "SortElements":
        """Create Sort Elements with operation 'Face'."""
        return cls(
            domain="FACE",
            geometry=geometry,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
        )

    @classmethod
    def spline(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
    ) -> "SortElements":
        """Create Sort Elements with operation 'Spline'."""
        return cls(
            domain="CURVE",
            geometry=geometry,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
        )

    @classmethod
    def instance(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
    ) -> "SortElements":
        """Create Sort Elements with operation 'Instance'."""
        return cls(
            domain="INSTANCE",
            geometry=geometry,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
        )

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


class Spiral(NodeBuilder):
    """Generate a poly spline in a spiral shape"""

    name = "GeometryNodeCurveSpiral"
    node: bpy.types.GeometryNodeCurveSpiral

    def __init__(
        self,
        resolution: TYPE_INPUT_INT = 32,
        rotations: TYPE_INPUT_VALUE = 2.0,
        start_radius: TYPE_INPUT_VALUE = 1.0,
        end_radius: TYPE_INPUT_VALUE = 2.0,
        height: TYPE_INPUT_VALUE = 2.0,
        reverse: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {
            "Resolution": resolution,
            "Rotations": rotations,
            "Start Radius": start_radius,
            "End Radius": end_radius,
            "Height": height,
            "Reverse": reverse,
        }

        self._establish_links(**key_args)

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def i_rotations(self) -> SocketLinker:
        """Input socket: Rotations"""
        return self._input("Rotations")

    @property
    def i_start_radius(self) -> SocketLinker:
        """Input socket: Start Radius"""
        return self._input("Start Radius")

    @property
    def i_end_radius(self) -> SocketLinker:
        """Input socket: End Radius"""
        return self._input("End Radius")

    @property
    def i_height(self) -> SocketLinker:
        """Input socket: Height"""
        return self._input("Height")

    @property
    def i_reverse(self) -> SocketLinker:
        """Input socket: Reverse"""
        return self._input("Reverse")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class SplitEdges(NodeBuilder):
    """Duplicate mesh edges and break connections with the surrounding faces"""

    name = "GeometryNodeSplitEdges"
    node: bpy.types.GeometryNodeSplitEdges

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
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
        group_id: TYPE_INPUT_INT = 0,
        *,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Group ID": group_id}
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Point'."""
        return cls(
            domain="POINT", geometry=geometry, selection=selection, group_id=group_id
        )

    @classmethod
    def edge(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Edge'."""
        return cls(
            domain="EDGE", geometry=geometry, selection=selection, group_id=group_id
        )

    @classmethod
    def face(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Face'."""
        return cls(
            domain="FACE", geometry=geometry, selection=selection, group_id=group_id
        )

    @classmethod
    def spline(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Spline'."""
        return cls(
            domain="CURVE", geometry=geometry, selection=selection, group_id=group_id
        )

    @classmethod
    def instance(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Instance'."""
        return cls(
            domain="INSTANCE", geometry=geometry, selection=selection, group_id=group_id
        )

    @classmethod
    def layer(
        cls,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
    ) -> "SplitToInstances":
        """Create Split to Instances with operation 'Layer'."""
        return cls(
            domain="LAYER", geometry=geometry, selection=selection, group_id=group_id
        )

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
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]
    ):
        self.node.domain = value


class Star(NodeBuilder):
    """Generate a poly spline in a star pattern by connecting alternating points of two circles"""

    name = "GeometryNodeCurveStar"
    node: bpy.types.GeometryNodeCurveStar

    def __init__(
        self,
        points: TYPE_INPUT_INT = 8,
        inner_radius: TYPE_INPUT_VALUE = 1.0,
        outer_radius: TYPE_INPUT_VALUE = 2.0,
        twist: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Inner Radius": inner_radius,
            "Outer Radius": outer_radius,
            "Twist": twist,
        }

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_inner_radius(self) -> SocketLinker:
        """Input socket: Inner Radius"""
        return self._input("Inner Radius")

    @property
    def i_outer_radius(self) -> SocketLinker:
        """Input socket: Outer Radius"""
        return self._input("Outer Radius")

    @property
    def i_twist(self) -> SocketLinker:
        """Input socket: Twist"""
        return self._input("Twist")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def o_outer_points(self) -> SocketLinker:
        """Output socket: Outer Points"""
        return self._output("Outer Points")


class StringToCurves(NodeBuilder):
    """Generate a paragraph of text with a specific font, using a curve instance to store each character"""

    name = "GeometryNodeStringToCurves"
    node: bpy.types.GeometryNodeStringToCurves

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        size: TYPE_INPUT_VALUE = 1.0,
        character_spacing: TYPE_INPUT_VALUE = 1.0,
        word_spacing: TYPE_INPUT_VALUE = 1.0,
        line_spacing: TYPE_INPUT_VALUE = 1.0,
        text_box_width: TYPE_INPUT_VALUE = 0.0,
        text_box_height: TYPE_INPUT_VALUE = 0.0,
        *,
        overflow: Literal["OVERFLOW", "SCALE_TO_FIT", "TRUNCATE"] = "OVERFLOW",
        align_x: Literal["LEFT", "CENTER", "RIGHT", "JUSTIFY", "FLUSH"] = "LEFT",
        align_y: Literal[
            "TOP", "TOP_BASELINE", "MIDDLE", "BOTTOM_BASELINE", "BOTTOM"
        ] = "TOP_BASELINE",
        pivot_mode: Literal[
            "MIDPOINT",
            "TOP_LEFT",
            "TOP_CENTER",
            "TOP_RIGHT",
            "BOTTOM_LEFT",
            "BOTTOM_CENTER",
            "BOTTOM_RIGHT",
        ] = "BOTTOM_LEFT",
    ):
        super().__init__()
        key_args = {
            "String": string,
            "Size": size,
            "Character Spacing": character_spacing,
            "Word Spacing": word_spacing,
            "Line Spacing": line_spacing,
            "Text Box Width": text_box_width,
            "Text Box Height": text_box_height,
        }
        self.overflow = overflow
        self.align_x = align_x
        self.align_y = align_y
        self.pivot_mode = pivot_mode
        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def i_size(self) -> SocketLinker:
        """Input socket: Size"""
        return self._input("Size")

    @property
    def i_character_spacing(self) -> SocketLinker:
        """Input socket: Character Spacing"""
        return self._input("Character Spacing")

    @property
    def i_word_spacing(self) -> SocketLinker:
        """Input socket: Word Spacing"""
        return self._input("Word Spacing")

    @property
    def i_line_spacing(self) -> SocketLinker:
        """Input socket: Line Spacing"""
        return self._input("Line Spacing")

    @property
    def i_text_box_width(self) -> SocketLinker:
        """Input socket: Text Box Width"""
        return self._input("Text Box Width")

    @property
    def i_text_box_height(self) -> SocketLinker:
        """Input socket: Text Box Height"""
        return self._input("Text Box Height")

    @property
    def o_curve_instances(self) -> SocketLinker:
        """Output socket: Curve Instances"""
        return self._output("Curve Instances")

    @property
    def o_remainder(self) -> SocketLinker:
        """Output socket: Remainder"""
        return self._output("Remainder")

    @property
    def o_line(self) -> SocketLinker:
        """Output socket: Line"""
        return self._output("Line")

    @property
    def o_pivot_point(self) -> SocketLinker:
        """Output socket: Pivot Point"""
        return self._output("Pivot Point")

    @property
    def overflow(self) -> Literal["OVERFLOW", "SCALE_TO_FIT", "TRUNCATE"]:
        return self.node.overflow

    @overflow.setter
    def overflow(self, value: Literal["OVERFLOW", "SCALE_TO_FIT", "TRUNCATE"]):
        self.node.overflow = value

    @property
    def align_x(self) -> Literal["LEFT", "CENTER", "RIGHT", "JUSTIFY", "FLUSH"]:
        return self.node.align_x

    @align_x.setter
    def align_x(self, value: Literal["LEFT", "CENTER", "RIGHT", "JUSTIFY", "FLUSH"]):
        self.node.align_x = value

    @property
    def align_y(
        self,
    ) -> Literal["TOP", "TOP_BASELINE", "MIDDLE", "BOTTOM_BASELINE", "BOTTOM"]:
        return self.node.align_y

    @align_y.setter
    def align_y(
        self,
        value: Literal["TOP", "TOP_BASELINE", "MIDDLE", "BOTTOM_BASELINE", "BOTTOM"],
    ):
        self.node.align_y = value

    @property
    def pivot_mode(
        self,
    ) -> Literal[
        "MIDPOINT",
        "TOP_LEFT",
        "TOP_CENTER",
        "TOP_RIGHT",
        "BOTTOM_LEFT",
        "BOTTOM_CENTER",
        "BOTTOM_RIGHT",
    ]:
        return self.node.pivot_mode

    @pivot_mode.setter
    def pivot_mode(
        self,
        value: Literal[
            "MIDPOINT",
            "TOP_LEFT",
            "TOP_CENTER",
            "TOP_RIGHT",
            "BOTTOM_LEFT",
            "BOTTOM_CENTER",
            "BOTTOM_RIGHT",
        ],
    ):
        self.node.pivot_mode = value


class SubdivideCurve(NodeBuilder):
    """Dividing each curve segment into a specified number of pieces"""

    name = "GeometryNodeSubdivideCurve"
    node: bpy.types.GeometryNodeSubdivideCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        cuts: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Curve": curve, "Cuts": cuts}

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_cuts(self) -> SocketLinker:
        """Input socket: Cuts"""
        return self._input("Cuts")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")


class SubdivideMesh(NodeBuilder):
    """Divide mesh faces into smaller ones without changing the shape or volume, using linear interpolation to place the new vertices"""

    name = "GeometryNodeSubdivideMesh"
    node: bpy.types.GeometryNodeSubdivideMesh

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        level: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Level": level}

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
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SubdivisionSurface(NodeBuilder):
    """Divide mesh faces to form a smooth surface, using the Catmull-Clark subdivision method"""

    name = "GeometryNodeSubdivisionSurface"
    node: bpy.types.GeometryNodeSubdivisionSurface

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        level: TYPE_INPUT_INT = 1,
        edge_crease: TYPE_INPUT_VALUE = 0.0,
        vertex_crease: TYPE_INPUT_VALUE = 0.0,
        limit_surface: TYPE_INPUT_BOOLEAN = True,
        uv_smooth: TYPE_INPUT_MENU = "Keep Boundaries",
        boundary_smooth: TYPE_INPUT_MENU = "All",
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


class TransformGeometry(NodeBuilder):
    """Translate, rotate or scale the geometry"""

    name = "GeometryNodeTransform"
    node: bpy.types.GeometryNodeTransform

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        mode: TYPE_INPUT_MENU = "Components",
        translation: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_ROTATION = None,
        scale: TYPE_INPUT_VECTOR = None,
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
        translation: TYPE_INPUT_VECTOR = None,
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
        mesh: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        quad_method: TYPE_INPUT_MENU = "Shortest Diagonal",
        n_gon_method: TYPE_INPUT_MENU = "Beauty",
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


class TrimCurve(NodeBuilder):
    """Shorten curves by removing portions at the start or end"""

    name = "GeometryNodeTrimCurve"
    node: bpy.types.GeometryNodeTrimCurve

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        start: TYPE_INPUT_VALUE = 0.0,
        end: TYPE_INPUT_VALUE = 1.0,
        start_001: TYPE_INPUT_VALUE = 0.0,
        end_001: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["FACTOR", "LENGTH"] = "FACTOR",
    ):
        super().__init__()
        key_args = {
            "Curve": curve,
            "Selection": selection,
            "Start": start,
            "End": end,
            "Start_001": start_001,
            "End_001": end_001,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_start(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start")

    @property
    def i_end(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End")

    @property
    def i_start_001(self) -> SocketLinker:
        """Input socket: Start"""
        return self._input("Start_001")

    @property
    def i_end_001(self) -> SocketLinker:
        """Input socket: End"""
        return self._input("End_001")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def mode(self) -> Literal["FACTOR", "LENGTH"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["FACTOR", "LENGTH"]):
        self.node.mode = value


class UVSphere(NodeBuilder):
    """Generate a spherical mesh with quads, except for triangles at the top and bottom"""

    name = "GeometryNodeMeshUVSphere"
    node: bpy.types.GeometryNodeMeshUVSphere

    def __init__(
        self,
        segments: TYPE_INPUT_INT = 32,
        rings: TYPE_INPUT_INT = 16,
        radius: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"Segments": segments, "Rings": rings, "Radius": radius}

        self._establish_links(**key_args)

    @property
    def i_segments(self) -> SocketLinker:
        """Input socket: Segments"""
        return self._input("Segments")

    @property
    def i_rings(self) -> SocketLinker:
        """Input socket: Rings"""
        return self._input("Rings")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_uv_map(self) -> SocketLinker:
        """Output socket: UV Map"""
        return self._output("UV Map")
