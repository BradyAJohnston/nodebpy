from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class Cursor3D(NodeBuilder):
    """The scene's 3D cursor location and rotation"""

    _bl_idname = "GeometryNodeTool3DCursor"
    node: bpy.types.GeometryNodeTool3DCursor

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_location(self) -> SocketLinker:
        """Output socket: Location"""
        return self._output("Location")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class ActiveCamera(NodeBuilder):
    """Retrieve the scene's active camera"""

    _bl_idname = "GeometryNodeInputActiveCamera"
    node: bpy.types.GeometryNodeInputActiveCamera

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_active_camera(self) -> SocketLinker:
        """Output socket: Active Camera"""
        return self._output("Active Camera")


class ActiveElement(NodeBuilder):
    """Active element indices of the edited geometry, for tool execution"""

    _bl_idname = "GeometryNodeToolActiveElement"
    node: bpy.types.GeometryNodeToolActiveElement

    def __init__(self, domain: Literal["POINT", "EDGE", "FACE", "LAYER"] = "POINT"):
        super().__init__()
        key_args = {}
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def point(cls) -> "ActiveElement":
        """Create Active Element with operation 'Point'."""
        return cls(domain="POINT")

    @classmethod
    def edge(cls) -> "ActiveElement":
        """Create Active Element with operation 'Edge'."""
        return cls(domain="EDGE")

    @classmethod
    def face(cls) -> "ActiveElement":
        """Create Active Element with operation 'Face'."""
        return cls(domain="FACE")

    @classmethod
    def layer(cls) -> "ActiveElement":
        """Create Active Element with operation 'Layer'."""
        return cls(domain="LAYER")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "LAYER"]):
        self.node.domain = value


class Boolean(NodeBuilder):
    """Provide a True/False value that can be connected to other nodes in the tree"""

    _bl_idname = "FunctionNodeInputBool"
    node: bpy.types.FunctionNodeInputBool

    def __init__(self, boolean: bool = False):
        super().__init__()
        key_args = {}
        self.boolean = boolean
        self._establish_links(**key_args)

    @property
    def o_boolean(self) -> SocketLinker:
        """Output socket: Boolean"""
        return self._output("Boolean")

    @property
    def boolean(self) -> bool:
        return self.node.boolean

    @boolean.setter
    def boolean(self, value: bool):
        self.node.boolean = value


class CameraInfo(NodeBuilder):
    """Retrieve information from a camera object"""

    _bl_idname = "GeometryNodeCameraInfo"
    node: bpy.types.GeometryNodeCameraInfo

    def __init__(self, camera: TYPE_INPUT_OBJECT = None):
        super().__init__()
        key_args = {"Camera": camera}

        self._establish_links(**key_args)

    @property
    def i_camera(self) -> SocketLinker:
        """Input socket: Camera"""
        return self._input("Camera")

    @property
    def o_projection_matrix(self) -> SocketLinker:
        """Output socket: Projection Matrix"""
        return self._output("Projection Matrix")

    @property
    def o_focal_length(self) -> SocketLinker:
        """Output socket: Focal Length"""
        return self._output("Focal Length")

    @property
    def o_sensor(self) -> SocketLinker:
        """Output socket: Sensor"""
        return self._output("Sensor")

    @property
    def o_shift(self) -> SocketLinker:
        """Output socket: Shift"""
        return self._output("Shift")

    @property
    def o_clip_start(self) -> SocketLinker:
        """Output socket: Clip Start"""
        return self._output("Clip Start")

    @property
    def o_clip_end(self) -> SocketLinker:
        """Output socket: Clip End"""
        return self._output("Clip End")

    @property
    def o_focus_distance(self) -> SocketLinker:
        """Output socket: Focus Distance"""
        return self._output("Focus Distance")

    @property
    def o_is_orthographic(self) -> SocketLinker:
        """Output socket: Is Orthographic"""
        return self._output("Is Orthographic")

    @property
    def o_orthographic_scale(self) -> SocketLinker:
        """Output socket: Orthographic Scale"""
        return self._output("Orthographic Scale")


class Collection(NodeBuilder):
    """Output a single collection"""

    _bl_idname = "GeometryNodeInputCollection"
    node: bpy.types.GeometryNodeInputCollection

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_collection(self) -> SocketLinker:
        """Output socket: Collection"""
        return self._output("Collection")


class CollectionInfo(NodeBuilder):
    """Retrieve geometry instances from a collection"""

    _bl_idname = "GeometryNodeCollectionInfo"
    node: bpy.types.GeometryNodeCollectionInfo

    def __init__(
        self,
        collection: TYPE_INPUT_COLLECTION = None,
        separate_children: TYPE_INPUT_BOOLEAN = False,
        reset_children: TYPE_INPUT_BOOLEAN = False,
        *,
        transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL",
    ):
        super().__init__()
        key_args = {
            "Collection": collection,
            "Separate Children": separate_children,
            "Reset Children": reset_children,
        }
        self.transform_space = transform_space
        self._establish_links(**key_args)

    @property
    def i_collection(self) -> SocketLinker:
        """Input socket: Collection"""
        return self._input("Collection")

    @property
    def i_separate_children(self) -> SocketLinker:
        """Input socket: Separate Children"""
        return self._input("Separate Children")

    @property
    def i_reset_children(self) -> SocketLinker:
        """Input socket: Reset Children"""
        return self._input("Reset Children")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")

    @property
    def transform_space(self) -> Literal["ORIGINAL", "RELATIVE"]:
        return self.node.transform_space

    @transform_space.setter
    def transform_space(self, value: Literal["ORIGINAL", "RELATIVE"]):
        self.node.transform_space = value


class Color(NodeBuilder):
    """Output a color value chosen with the color picker widget"""

    _bl_idname = "FunctionNodeInputColor"
    node: bpy.types.FunctionNodeInputColor

    def __init__(
        self, value: tuple[float, float, float, float] = (0.735, 0.735, 0.735, 1.0)
    ):
        super().__init__()
        key_args = {}
        self.value = value
        self._establish_links(**key_args)

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def value(self) -> tuple[float, float, float, float]:
        return self.node.value

    @value.setter
    def value(self, value: tuple[float, float, float, float]):
        self.node.value = value


class CornersOfEdge(NodeBuilder):
    """Retrieve face corners connected to edges"""

    _bl_idname = "GeometryNodeCornersOfEdge"
    node: bpy.types.GeometryNodeCornersOfEdge

    def __init__(
        self,
        edge_index: TYPE_INPUT_INT = 0,
        weights: TYPE_INPUT_VALUE = 0.0,
        sort_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Edge Index": edge_index,
            "Weights": weights,
            "Sort Index": sort_index,
        }

        self._establish_links(**key_args)

    @property
    def i_edge_index(self) -> SocketLinker:
        """Input socket: Edge Index"""
        return self._input("Edge Index")

    @property
    def i_weights(self) -> SocketLinker:
        """Input socket: Weights"""
        return self._input("Weights")

    @property
    def i_sort_index(self) -> SocketLinker:
        """Input socket: Sort Index"""
        return self._input("Sort Index")

    @property
    def o_corner_index(self) -> SocketLinker:
        """Output socket: Corner Index"""
        return self._output("Corner Index")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")


class CornersOfFace(NodeBuilder):
    """Retrieve corners that make up a face"""

    _bl_idname = "GeometryNodeCornersOfFace"
    node: bpy.types.GeometryNodeCornersOfFace

    def __init__(
        self,
        face_index: TYPE_INPUT_INT = 0,
        weights: TYPE_INPUT_VALUE = 0.0,
        sort_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Face Index": face_index,
            "Weights": weights,
            "Sort Index": sort_index,
        }

        self._establish_links(**key_args)

    @property
    def i_face_index(self) -> SocketLinker:
        """Input socket: Face Index"""
        return self._input("Face Index")

    @property
    def i_weights(self) -> SocketLinker:
        """Input socket: Weights"""
        return self._input("Weights")

    @property
    def i_sort_index(self) -> SocketLinker:
        """Input socket: Sort Index"""
        return self._input("Sort Index")

    @property
    def o_corner_index(self) -> SocketLinker:
        """Output socket: Corner Index"""
        return self._output("Corner Index")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")


class CornersOfVertex(NodeBuilder):
    """Retrieve face corners connected to vertices"""

    _bl_idname = "GeometryNodeCornersOfVertex"
    node: bpy.types.GeometryNodeCornersOfVertex

    def __init__(
        self,
        vertex_index: TYPE_INPUT_INT = 0,
        weights: TYPE_INPUT_VALUE = 0.0,
        sort_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Vertex Index": vertex_index,
            "Weights": weights,
            "Sort Index": sort_index,
        }

        self._establish_links(**key_args)

    @property
    def i_vertex_index(self) -> SocketLinker:
        """Input socket: Vertex Index"""
        return self._input("Vertex Index")

    @property
    def i_weights(self) -> SocketLinker:
        """Input socket: Weights"""
        return self._input("Weights")

    @property
    def i_sort_index(self) -> SocketLinker:
        """Input socket: Sort Index"""
        return self._input("Sort Index")

    @property
    def o_corner_index(self) -> SocketLinker:
        """Output socket: Corner Index"""
        return self._output("Corner Index")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")


class CurveHandlePositions(NodeBuilder):
    """Retrieve the position of each Bézier control point's handles"""

    _bl_idname = "GeometryNodeInputCurveHandlePositions"
    node: bpy.types.GeometryNodeInputCurveHandlePositions

    def __init__(self, relative: TYPE_INPUT_BOOLEAN = False):
        super().__init__()
        key_args = {"Relative": relative}

        self._establish_links(**key_args)

    @property
    def i_relative(self) -> SocketLinker:
        """Input socket: Relative"""
        return self._input("Relative")

    @property
    def o_left(self) -> SocketLinker:
        """Output socket: Left"""
        return self._output("Left")

    @property
    def o_right(self) -> SocketLinker:
        """Output socket: Right"""
        return self._output("Right")


class CurveTangent(NodeBuilder):
    """Retrieve the direction of curves at each control point"""

    _bl_idname = "GeometryNodeInputTangent"
    node: bpy.types.GeometryNodeInputTangent

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")


class CurveTilt(NodeBuilder):
    """Retrieve the angle at each control point used to twist the curve's normal around its tangent"""

    _bl_idname = "GeometryNodeInputCurveTilt"
    node: bpy.types.GeometryNodeInputCurveTilt

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_tilt(self) -> SocketLinker:
        """Output socket: Tilt"""
        return self._output("Tilt")


class CurveOfPoint(NodeBuilder):
    """Retrieve the curve a control point is part of"""

    _bl_idname = "GeometryNodeCurveOfPoint"
    node: bpy.types.GeometryNodeCurveOfPoint

    def __init__(self, point_index: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Point Index": point_index}

        self._establish_links(**key_args)

    @property
    def i_point_index(self) -> SocketLinker:
        """Input socket: Point Index"""
        return self._input("Point Index")

    @property
    def o_curve_index(self) -> SocketLinker:
        """Output socket: Curve Index"""
        return self._output("Curve Index")

    @property
    def o_index_in_curve(self) -> SocketLinker:
        """Output socket: Index in Curve"""
        return self._output("Index in Curve")


class EdgeAngle(NodeBuilder):
    """The angle between the normals of connected manifold faces"""

    _bl_idname = "GeometryNodeInputMeshEdgeAngle"
    node: bpy.types.GeometryNodeInputMeshEdgeAngle

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_unsigned_angle(self) -> SocketLinker:
        """Output socket: Unsigned Angle"""
        return self._output("Unsigned Angle")

    @property
    def o_signed_angle(self) -> SocketLinker:
        """Output socket: Signed Angle"""
        return self._output("Signed Angle")


class EdgeNeighbors(NodeBuilder):
    """Retrieve the number of faces that use each edge as one of their sides"""

    _bl_idname = "GeometryNodeInputMeshEdgeNeighbors"
    node: bpy.types.GeometryNodeInputMeshEdgeNeighbors

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class EdgePathsToSelection(NodeBuilder):
    """Output a selection of edges by following paths across mesh edges"""

    _bl_idname = "GeometryNodeEdgePathsToSelection"
    node: bpy.types.GeometryNodeEdgePathsToSelection

    def __init__(
        self,
        start_vertices: TYPE_INPUT_BOOLEAN = True,
        next_vertex_index: TYPE_INPUT_INT = -1,
    ):
        super().__init__()
        key_args = {
            "Start Vertices": start_vertices,
            "Next Vertex Index": next_vertex_index,
        }

        self._establish_links(**key_args)

    @property
    def i_start_vertices(self) -> SocketLinker:
        """Input socket: Start Vertices"""
        return self._input("Start Vertices")

    @property
    def i_next_vertex_index(self) -> SocketLinker:
        """Input socket: Next Vertex Index"""
        return self._input("Next Vertex Index")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")


class EdgeVertices(NodeBuilder):
    """Retrieve topology information relating to each edge of a mesh"""

    _bl_idname = "GeometryNodeInputMeshEdgeVertices"
    node: bpy.types.GeometryNodeInputMeshEdgeVertices

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_vertex_index_1(self) -> SocketLinker:
        """Output socket: Vertex Index 1"""
        return self._output("Vertex Index 1")

    @property
    def o_vertex_index_2(self) -> SocketLinker:
        """Output socket: Vertex Index 2"""
        return self._output("Vertex Index 2")

    @property
    def o_position_1(self) -> SocketLinker:
        """Output socket: Position 1"""
        return self._output("Position 1")

    @property
    def o_position_2(self) -> SocketLinker:
        """Output socket: Position 2"""
        return self._output("Position 2")


class EdgesOfCorner(NodeBuilder):
    """Retrieve the edges on both sides of a face corner"""

    _bl_idname = "GeometryNodeEdgesOfCorner"
    node: bpy.types.GeometryNodeEdgesOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Corner Index": corner_index}

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def o_next_edge_index(self) -> SocketLinker:
        """Output socket: Next Edge Index"""
        return self._output("Next Edge Index")

    @property
    def o_previous_edge_index(self) -> SocketLinker:
        """Output socket: Previous Edge Index"""
        return self._output("Previous Edge Index")


class EdgesOfVertex(NodeBuilder):
    """Retrieve the edges connected to each vertex"""

    _bl_idname = "GeometryNodeEdgesOfVertex"
    node: bpy.types.GeometryNodeEdgesOfVertex

    def __init__(
        self,
        vertex_index: TYPE_INPUT_INT = 0,
        weights: TYPE_INPUT_VALUE = 0.0,
        sort_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Vertex Index": vertex_index,
            "Weights": weights,
            "Sort Index": sort_index,
        }

        self._establish_links(**key_args)

    @property
    def i_vertex_index(self) -> SocketLinker:
        """Input socket: Vertex Index"""
        return self._input("Vertex Index")

    @property
    def i_weights(self) -> SocketLinker:
        """Input socket: Weights"""
        return self._input("Weights")

    @property
    def i_sort_index(self) -> SocketLinker:
        """Input socket: Sort Index"""
        return self._input("Sort Index")

    @property
    def o_edge_index(self) -> SocketLinker:
        """Output socket: Edge Index"""
        return self._output("Edge Index")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")


class EdgesToFaceGroups(NodeBuilder):
    """Group faces into regions surrounded by the selected boundary edges"""

    _bl_idname = "GeometryNodeEdgesToFaceGroups"
    node: bpy.types.GeometryNodeEdgesToFaceGroups

    def __init__(self, boundary_edges: TYPE_INPUT_BOOLEAN = True):
        super().__init__()
        key_args = {"Boundary Edges": boundary_edges}

        self._establish_links(**key_args)

    @property
    def i_boundary_edges(self) -> SocketLinker:
        """Input socket: Boundary Edges"""
        return self._input("Boundary Edges")

    @property
    def o_face_group_id(self) -> SocketLinker:
        """Output socket: Face Group ID"""
        return self._output("Face Group ID")


class EndpointSelection(NodeBuilder):
    """Provide a selection for an arbitrary number of endpoints in each spline"""

    _bl_idname = "GeometryNodeCurveEndpointSelection"
    node: bpy.types.GeometryNodeCurveEndpointSelection

    def __init__(
        self,
        start_size: TYPE_INPUT_INT = 1,
        end_size: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Start Size": start_size, "End Size": end_size}

        self._establish_links(**key_args)

    @property
    def i_start_size(self) -> SocketLinker:
        """Input socket: Start Size"""
        return self._input("Start Size")

    @property
    def i_end_size(self) -> SocketLinker:
        """Input socket: End Size"""
        return self._input("End Size")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")


class FaceArea(NodeBuilder):
    """Calculate the surface area of a mesh's faces"""

    _bl_idname = "GeometryNodeInputMeshFaceArea"
    node: bpy.types.GeometryNodeInputMeshFaceArea

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_area(self) -> SocketLinker:
        """Output socket: Area"""
        return self._output("Area")


class FaceGroupBoundaries(NodeBuilder):
    """Find edges on the boundaries between groups of faces with the same ID value"""

    _bl_idname = "GeometryNodeMeshFaceSetBoundaries"
    node: bpy.types.GeometryNodeMeshFaceSetBoundaries

    def __init__(self, face_set: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Face Set": face_set}

        self._establish_links(**key_args)

    @property
    def i_face_set(self) -> SocketLinker:
        """Input socket: Face Group ID"""
        return self._input("Face Set")

    @property
    def o_boundary_edges(self) -> SocketLinker:
        """Output socket: Boundary Edges"""
        return self._output("Boundary Edges")


class FaceNeighbors(NodeBuilder):
    """Retrieve topology information relating to each face of a mesh"""

    _bl_idname = "GeometryNodeInputMeshFaceNeighbors"
    node: bpy.types.GeometryNodeInputMeshFaceNeighbors

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_vertex_count(self) -> SocketLinker:
        """Output socket: Vertex Count"""
        return self._output("Vertex Count")

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class FaceSet(NodeBuilder):
    """Each face's sculpt face set value"""

    _bl_idname = "GeometryNodeToolFaceSet"
    node: bpy.types.GeometryNodeToolFaceSet

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_face_set(self) -> SocketLinker:
        """Output socket: Face Set"""
        return self._output("Face Set")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")


class FaceOfCorner(NodeBuilder):
    """Retrieve the face each face corner is part of"""

    _bl_idname = "GeometryNodeFaceOfCorner"
    node: bpy.types.GeometryNodeFaceOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Corner Index": corner_index}

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def o_face_index(self) -> SocketLinker:
        """Output socket: Face Index"""
        return self._output("Face Index")

    @property
    def o_index_in_face(self) -> SocketLinker:
        """Output socket: Index in Face"""
        return self._output("Index in Face")


class ID(NodeBuilder):
    """Retrieve a stable random identifier value from the "id" attribute on the point domain, or the index if the attribute does not exist"""

    _bl_idname = "GeometryNodeInputID"
    node: bpy.types.GeometryNodeInputID

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_id(self) -> SocketLinker:
        """Output socket: ID"""
        return self._output("ID")


class Image(NodeBuilder):
    """Input an image data-block"""

    _bl_idname = "GeometryNodeInputImage"
    node: bpy.types.GeometryNodeInputImage

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class ImageInfo(NodeBuilder):
    """Retrieve information about an image"""

    _bl_idname = "GeometryNodeImageInfo"
    node: bpy.types.GeometryNodeImageInfo

    def __init__(
        self,
        image: TYPE_INPUT_IMAGE = None,
        frame: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {"Image": image, "Frame": frame}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_frame(self) -> SocketLinker:
        """Input socket: Frame"""
        return self._input("Frame")

    @property
    def o_width(self) -> SocketLinker:
        """Output socket: Width"""
        return self._output("Width")

    @property
    def o_height(self) -> SocketLinker:
        """Output socket: Height"""
        return self._output("Height")

    @property
    def o_has_alpha(self) -> SocketLinker:
        """Output socket: Has Alpha"""
        return self._output("Has Alpha")

    @property
    def o_frame_count(self) -> SocketLinker:
        """Output socket: Frame Count"""
        return self._output("Frame Count")

    @property
    def o_fps(self) -> SocketLinker:
        """Output socket: FPS"""
        return self._output("FPS")


class ImportCSV(NodeBuilder):
    """Import geometry from an CSV file"""

    _bl_idname = "GeometryNodeImportCSV"
    node: bpy.types.GeometryNodeImportCSV

    def __init__(
        self,
        path: TYPE_INPUT_STRING = "",
        delimiter: TYPE_INPUT_STRING = ",",
    ):
        super().__init__()
        key_args = {"Path": path, "Delimiter": delimiter}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def i_delimiter(self) -> SocketLinker:
        """Input socket: Delimiter"""
        return self._input("Delimiter")

    @property
    def o_point_cloud(self) -> SocketLinker:
        """Output socket: Point Cloud"""
        return self._output("Point Cloud")


class ImportOBJ(NodeBuilder):
    """Import geometry from an OBJ file"""

    _bl_idname = "GeometryNodeImportOBJ"
    node: bpy.types.GeometryNodeImportOBJ

    def __init__(self, path: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Path": path}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class ImportPLY(NodeBuilder):
    """Import a point cloud from a PLY file"""

    _bl_idname = "GeometryNodeImportPLY"
    node: bpy.types.GeometryNodeImportPLY

    def __init__(self, path: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Path": path}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class ImportSTL(NodeBuilder):
    """Import a mesh from an STL file"""

    _bl_idname = "GeometryNodeImportSTL"
    node: bpy.types.GeometryNodeImportSTL

    def __init__(self, path: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Path": path}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class ImportText(NodeBuilder):
    """Import a string from a text file"""

    _bl_idname = "GeometryNodeImportText"
    node: bpy.types.GeometryNodeImportText

    def __init__(self, path: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Path": path}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class ImportVDB(NodeBuilder):
    """Import volume data from a .vdb file"""

    _bl_idname = "GeometryNodeImportVDB"
    node: bpy.types.GeometryNodeImportVDB

    def __init__(self, path: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Path": path}

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class Index(NodeBuilder):
    """Retrieve an integer value indicating the position of each element in the list, starting at zero"""

    _bl_idname = "GeometryNodeInputIndex"
    node: bpy.types.GeometryNodeInputIndex

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")


class InstanceBounds(NodeBuilder):
    """Calculate position bounds of each instance's geometry set"""

    _bl_idname = "GeometryNodeInputInstanceBounds"
    node: bpy.types.GeometryNodeInputInstanceBounds

    def __init__(self, use_radius: TYPE_INPUT_BOOLEAN = True):
        super().__init__()
        key_args = {"Use Radius": use_radius}

        self._establish_links(**key_args)

    @property
    def i_use_radius(self) -> SocketLinker:
        """Input socket: Use Radius"""
        return self._input("Use Radius")

    @property
    def o_min(self) -> SocketLinker:
        """Output socket: Min"""
        return self._output("Min")

    @property
    def o_max(self) -> SocketLinker:
        """Output socket: Max"""
        return self._output("Max")


class InstanceRotation(NodeBuilder):
    """Retrieve the rotation of each instance in the geometry"""

    _bl_idname = "GeometryNodeInputInstanceRotation"
    node: bpy.types.GeometryNodeInputInstanceRotation

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class InstanceScale(NodeBuilder):
    """Retrieve the scale of each instance in the geometry"""

    _bl_idname = "GeometryNodeInputInstanceScale"
    node: bpy.types.GeometryNodeInputInstanceScale

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_scale(self) -> SocketLinker:
        """Output socket: Scale"""
        return self._output("Scale")


class InstanceTransform(NodeBuilder):
    """Retrieve the full transformation of each instance in the geometry"""

    _bl_idname = "GeometryNodeInstanceTransform"
    node: bpy.types.GeometryNodeInstanceTransform

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")


class Integer(NodeBuilder):
    """Provide an integer value that can be connected to other nodes in the tree"""

    _bl_idname = "FunctionNodeInputInt"
    node: bpy.types.FunctionNodeInputInt

    def __init__(self, integer: int = 1):
        super().__init__()
        key_args = {}
        self.integer = integer
        self._establish_links(**key_args)

    @property
    def o_integer(self) -> SocketLinker:
        """Output socket: Integer"""
        return self._output("Integer")

    @property
    def integer(self) -> int:
        return self.node.integer

    @integer.setter
    def integer(self, value: int):
        self.node.integer = value


class IsEdgeSmooth(NodeBuilder):
    """Retrieve whether each edge is marked for smooth or split normals"""

    _bl_idname = "GeometryNodeInputEdgeSmooth"
    node: bpy.types.GeometryNodeInputEdgeSmooth

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_smooth(self) -> SocketLinker:
        """Output socket: Smooth"""
        return self._output("Smooth")


class IsFacePlanar(NodeBuilder):
    """Retrieve whether all triangles in a face are on the same plane, i.e. whether they have the same normal"""

    _bl_idname = "GeometryNodeInputMeshFaceIsPlanar"
    node: bpy.types.GeometryNodeInputMeshFaceIsPlanar

    def __init__(self, threshold: TYPE_INPUT_VALUE = 0.01):
        super().__init__()
        key_args = {"Threshold": threshold}

        self._establish_links(**key_args)

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def o_planar(self) -> SocketLinker:
        """Output socket: Planar"""
        return self._output("Planar")


class IsFaceSmooth(NodeBuilder):
    """Retrieve whether each face is marked for smooth or sharp normals"""

    _bl_idname = "GeometryNodeInputShadeSmooth"
    node: bpy.types.GeometryNodeInputShadeSmooth

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_smooth(self) -> SocketLinker:
        """Output socket: Smooth"""
        return self._output("Smooth")


class IsSplineCyclic(NodeBuilder):
    """Retrieve whether each spline endpoint connects to the beginning"""

    _bl_idname = "GeometryNodeInputSplineCyclic"
    node: bpy.types.GeometryNodeInputSplineCyclic

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_cyclic(self) -> SocketLinker:
        """Output socket: Cyclic"""
        return self._output("Cyclic")


class IsViewport(NodeBuilder):
    """Retrieve whether the nodes are being evaluated for the viewport rather than the final render"""

    _bl_idname = "GeometryNodeIsViewport"
    node: bpy.types.GeometryNodeIsViewport

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_is_viewport(self) -> SocketLinker:
        """Output socket: Is Viewport"""
        return self._output("Is Viewport")


class Material(NodeBuilder):
    """Output a single material"""

    _bl_idname = "GeometryNodeInputMaterial"
    node: bpy.types.GeometryNodeInputMaterial

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_material(self) -> SocketLinker:
        """Output socket: Material"""
        return self._output("Material")


class MaterialIndex(NodeBuilder):
    """Retrieve the index of the material used for each element in the geometry's list of materials"""

    _bl_idname = "GeometryNodeInputMaterialIndex"
    node: bpy.types.GeometryNodeInputMaterialIndex

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_material_index(self) -> SocketLinker:
        """Output socket: Material Index"""
        return self._output("Material Index")


class MeshIsland(NodeBuilder):
    """Retrieve information about separate connected regions in a mesh"""

    _bl_idname = "GeometryNodeInputMeshIsland"
    node: bpy.types.GeometryNodeInputMeshIsland

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_island_index(self) -> SocketLinker:
        """Output socket: Island Index"""
        return self._output("Island Index")

    @property
    def o_island_count(self) -> SocketLinker:
        """Output socket: Island Count"""
        return self._output("Island Count")


class MousePosition(NodeBuilder):
    """Retrieve the position of the mouse cursor"""

    _bl_idname = "GeometryNodeToolMousePosition"
    node: bpy.types.GeometryNodeToolMousePosition

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_mouse_x(self) -> SocketLinker:
        """Output socket: Mouse X"""
        return self._output("Mouse X")

    @property
    def o_mouse_y(self) -> SocketLinker:
        """Output socket: Mouse Y"""
        return self._output("Mouse Y")

    @property
    def o_region_width(self) -> SocketLinker:
        """Output socket: Region Width"""
        return self._output("Region Width")

    @property
    def o_region_height(self) -> SocketLinker:
        """Output socket: Region Height"""
        return self._output("Region Height")


class NamedAttribute(NodeBuilder):
    """Retrieve the data of a specified attribute"""

    _bl_idname = "GeometryNodeInputNamedAttribute"
    node: bpy.types.GeometryNodeInputNamedAttribute

    def __init__(
        self,
        name: TYPE_INPUT_STRING = "",
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
        key_args = {"Name": name}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Float'."""
        return cls(data_type="FLOAT", name=name)

    @classmethod
    def integer(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Integer'."""
        return cls(data_type="INT", name=name)

    @classmethod
    def boolean(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", name=name)

    @classmethod
    def vector(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", name=name)

    @classmethod
    def color(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Color'."""
        return cls(data_type="FLOAT_COLOR", name=name)

    @classmethod
    def quaternion(cls, name: TYPE_INPUT_STRING = "") -> "NamedAttribute":
        """Create Named Attribute with operation 'Quaternion'."""
        return cls(data_type="QUATERNION", name=name)

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def o_attribute(self) -> SocketLinker:
        """Output socket: Attribute"""
        return self._output("Attribute")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")

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


class NamedLayerSelection(NodeBuilder):
    """Output a selection of a Grease Pencil layer"""

    _bl_idname = "GeometryNodeInputNamedLayerSelection"
    node: bpy.types.GeometryNodeInputNamedLayerSelection

    def __init__(self, name: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"Name": name}

        self._establish_links(**key_args)

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")


class Normal(NodeBuilder):
    """Retrieve a unit length vector indicating the direction pointing away from the geometry at each element"""

    _bl_idname = "GeometryNodeInputNormal"
    node: bpy.types.GeometryNodeInputNormal

    def __init__(self, legacy_corner_normals: bool = False):
        super().__init__()
        key_args = {}
        self.legacy_corner_normals = legacy_corner_normals
        self._establish_links(**key_args)

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def o_true_normal(self) -> SocketLinker:
        """Output socket: True Normal"""
        return self._output("True Normal")

    @property
    def legacy_corner_normals(self) -> bool:
        return self.node.legacy_corner_normals

    @legacy_corner_normals.setter
    def legacy_corner_normals(self, value: bool):
        self.node.legacy_corner_normals = value


class Object(NodeBuilder):
    """Output a single object"""

    _bl_idname = "GeometryNodeInputObject"
    node: bpy.types.GeometryNodeInputObject

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_object(self) -> SocketLinker:
        """Output socket: Object"""
        return self._output("Object")


class ObjectInfo(NodeBuilder):
    """Retrieve information from an object"""

    _bl_idname = "GeometryNodeObjectInfo"
    node: bpy.types.GeometryNodeObjectInfo

    def __init__(
        self,
        object: TYPE_INPUT_OBJECT = None,
        as_instance: TYPE_INPUT_BOOLEAN = False,
        *,
        transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL",
    ):
        super().__init__()
        key_args = {"Object": object, "As Instance": as_instance}
        self.transform_space = transform_space
        self._establish_links(**key_args)

    @property
    def i_object(self) -> SocketLinker:
        """Input socket: Object"""
        return self._input("Object")

    @property
    def i_as_instance(self) -> SocketLinker:
        """Input socket: As Instance"""
        return self._input("As Instance")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def o_location(self) -> SocketLinker:
        """Output socket: Location"""
        return self._output("Location")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def o_scale(self) -> SocketLinker:
        """Output socket: Scale"""
        return self._output("Scale")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def transform_space(self) -> Literal["ORIGINAL", "RELATIVE"]:
        return self.node.transform_space

    @transform_space.setter
    def transform_space(self, value: Literal["ORIGINAL", "RELATIVE"]):
        self.node.transform_space = value


class OffsetCornerInFace(NodeBuilder):
    """Retrieve corners in the same face as another"""

    _bl_idname = "GeometryNodeOffsetCornerInFace"
    node: bpy.types.GeometryNodeOffsetCornerInFace

    def __init__(
        self,
        corner_index: TYPE_INPUT_INT = 0,
        offset: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {"Corner Index": corner_index, "Offset": offset}

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_corner_index(self) -> SocketLinker:
        """Output socket: Corner Index"""
        return self._output("Corner Index")


class OffsetPointInCurve(NodeBuilder):
    """Offset a control point index within its curve"""

    _bl_idname = "GeometryNodeOffsetPointInCurve"
    node: bpy.types.GeometryNodeOffsetPointInCurve

    def __init__(
        self,
        point_index: TYPE_INPUT_INT = 0,
        offset: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {"Point Index": point_index, "Offset": offset}

        self._establish_links(**key_args)

    @property
    def i_point_index(self) -> SocketLinker:
        """Input socket: Point Index"""
        return self._input("Point Index")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_is_valid_offset(self) -> SocketLinker:
        """Output socket: Is Valid Offset"""
        return self._output("Is Valid Offset")

    @property
    def o_point_index(self) -> SocketLinker:
        """Output socket: Point Index"""
        return self._output("Point Index")


class PointsOfCurve(NodeBuilder):
    """Retrieve a point index within a curve"""

    _bl_idname = "GeometryNodePointsOfCurve"
    node: bpy.types.GeometryNodePointsOfCurve

    def __init__(
        self,
        curve_index: TYPE_INPUT_INT = 0,
        weights: TYPE_INPUT_VALUE = 0.0,
        sort_index: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {
            "Curve Index": curve_index,
            "Weights": weights,
            "Sort Index": sort_index,
        }

        self._establish_links(**key_args)

    @property
    def i_curve_index(self) -> SocketLinker:
        """Input socket: Curve Index"""
        return self._input("Curve Index")

    @property
    def i_weights(self) -> SocketLinker:
        """Input socket: Weights"""
        return self._input("Weights")

    @property
    def i_sort_index(self) -> SocketLinker:
        """Input socket: Sort Index"""
        return self._input("Sort Index")

    @property
    def o_point_index(self) -> SocketLinker:
        """Output socket: Point Index"""
        return self._output("Point Index")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")


class Position(NodeBuilder):
    """Retrieve a vector indicating the location of each element"""

    _bl_idname = "GeometryNodeInputPosition"
    node: bpy.types.GeometryNodeInputPosition

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")


class Radius(NodeBuilder):
    """Retrieve the radius at each point on curve or point cloud geometry"""

    _bl_idname = "GeometryNodeInputRadius"
    node: bpy.types.GeometryNodeInputRadius

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_radius(self) -> SocketLinker:
        """Output socket: Radius"""
        return self._output("Radius")


class Rotation(NodeBuilder):
    """Provide a rotation value that can be connected to other nodes in the tree"""

    _bl_idname = "FunctionNodeInputRotation"
    node: bpy.types.FunctionNodeInputRotation

    def __init__(self, rotation_euler: tuple[float, float, float] = (0.0, 0.0, 0.0)):
        super().__init__()
        key_args = {}
        self.rotation_euler = rotation_euler
        self._establish_links(**key_args)

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def rotation_euler(self) -> tuple[float, float, float]:
        return self.node.rotation_euler

    @rotation_euler.setter
    def rotation_euler(self, value: tuple[float, float, float]):
        self.node.rotation_euler = value


class SceneTime(NodeBuilder):
    """Retrieve the current time in the scene's animation in units of seconds or frames"""

    _bl_idname = "GeometryNodeInputSceneTime"
    node: bpy.types.GeometryNodeInputSceneTime

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_seconds(self) -> SocketLinker:
        """Output socket: Seconds"""
        return self._output("Seconds")

    @property
    def o_frame(self) -> SocketLinker:
        """Output socket: Frame"""
        return self._output("Frame")


class Selection(NodeBuilder):
    """User selection of the edited geometry, for tool execution"""

    _bl_idname = "GeometryNodeToolSelection"
    node: bpy.types.GeometryNodeToolSelection

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Boolean"""
        return self._output("Selection")

    @property
    def o_float(self) -> SocketLinker:
        """Output socket: Float"""
        return self._output("Float")


class SelfObject(NodeBuilder):
    """Retrieve the object that contains the geometry nodes modifier currently being executed"""

    _bl_idname = "GeometryNodeSelfObject"
    node: bpy.types.GeometryNodeSelfObject

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_self_object(self) -> SocketLinker:
        """Output socket: Self Object"""
        return self._output("Self Object")


class ShortestEdgePaths(NodeBuilder):
    """Find the shortest paths along mesh edges to selected end vertices, with customizable cost per edge"""

    _bl_idname = "GeometryNodeInputShortestEdgePaths"
    node: bpy.types.GeometryNodeInputShortestEdgePaths

    def __init__(
        self,
        end_vertex: TYPE_INPUT_BOOLEAN = False,
        edge_cost: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"End Vertex": end_vertex, "Edge Cost": edge_cost}

        self._establish_links(**key_args)

    @property
    def i_end_vertex(self) -> SocketLinker:
        """Input socket: End Vertex"""
        return self._input("End Vertex")

    @property
    def i_edge_cost(self) -> SocketLinker:
        """Input socket: Edge Cost"""
        return self._input("Edge Cost")

    @property
    def o_next_vertex_index(self) -> SocketLinker:
        """Output socket: Next Vertex Index"""
        return self._output("Next Vertex Index")

    @property
    def o_total_cost(self) -> SocketLinker:
        """Output socket: Total Cost"""
        return self._output("Total Cost")


class SpecialCharacters(NodeBuilder):
    """Output string characters that cannot be typed directly with the keyboard"""

    _bl_idname = "FunctionNodeInputSpecialCharacters"
    node: bpy.types.FunctionNodeInputSpecialCharacters

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_line_break(self) -> SocketLinker:
        """Output socket: Line Break"""
        return self._output("Line Break")

    @property
    def o_tab(self) -> SocketLinker:
        """Output socket: Tab"""
        return self._output("Tab")


class SplineLength(NodeBuilder):
    """Retrieve the total length of each spline, as a distance or as a number of points"""

    _bl_idname = "GeometryNodeSplineLength"
    node: bpy.types.GeometryNodeSplineLength

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def o_point_count(self) -> SocketLinker:
        """Output socket: Point Count"""
        return self._output("Point Count")


class SplineParameter(NodeBuilder):
    """Retrieve how far along each spline a control point is"""

    _bl_idname = "GeometryNodeSplineParameter"
    node: bpy.types.GeometryNodeSplineParameter

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_factor(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Factor")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")


class SplineResolution(NodeBuilder):
    """Retrieve the number of evaluated points that will be generated for every control point on curves"""

    _bl_idname = "GeometryNodeInputSplineResolution"
    node: bpy.types.GeometryNodeInputSplineResolution

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_resolution(self) -> SocketLinker:
        """Output socket: Resolution"""
        return self._output("Resolution")


class String(NodeBuilder):
    """Provide a string value that can be connected to other nodes in the tree"""

    _bl_idname = "FunctionNodeInputString"
    node: bpy.types.FunctionNodeInputString

    def __init__(self, string: str = ""):
        super().__init__()
        key_args = {}
        self.string = string
        self._establish_links(**key_args)

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")

    @property
    def string(self) -> str:
        return self.node.string

    @string.setter
    def string(self, value: str):
        self.node.string = value


class UVTangent(NodeBuilder):
    """Generate tangent directions based on a UV map"""

    _bl_idname = "GeometryNodeUVTangent"
    node: bpy.types.GeometryNodeUVTangent

    def __init__(
        self,
        method: TYPE_INPUT_MENU = "Exact",
        uv: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {"Method": method, "UV": uv}

        self._establish_links(**key_args)

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def i_uv(self) -> SocketLinker:
        """Input socket: UV"""
        return self._input("UV")

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")


class Vector(NodeBuilder):
    """Provide a vector value that can be connected to other nodes in the tree"""

    _bl_idname = "FunctionNodeInputVector"
    node: bpy.types.FunctionNodeInputVector

    def __init__(self, vector: tuple[float, float, float] = (0.0, 0.0, 0.0)):
        super().__init__()
        key_args = {}
        self.vector = vector
        self._establish_links(**key_args)

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def vector(self) -> tuple[float, float, float]:
        return self.node.vector

    @vector.setter
    def vector(self, value: tuple[float, float, float]):
        self.node.vector = value


class VertexNeighbors(NodeBuilder):
    """Retrieve topology information relating to each vertex of a mesh"""

    _bl_idname = "GeometryNodeInputMeshVertexNeighbors"
    node: bpy.types.GeometryNodeInputMeshVertexNeighbors

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_vertex_count(self) -> SocketLinker:
        """Output socket: Vertex Count"""
        return self._output("Vertex Count")

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class VertexOfCorner(NodeBuilder):
    """Retrieve the vertex each face corner is attached to"""

    _bl_idname = "GeometryNodeVertexOfCorner"
    node: bpy.types.GeometryNodeVertexOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Corner Index": corner_index}

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def o_vertex_index(self) -> SocketLinker:
        """Output socket: Vertex Index"""
        return self._output("Vertex Index")


class ViewportTransform(NodeBuilder):
    """Retrieve the view direction and location of the 3D viewport"""

    _bl_idname = "GeometryNodeViewportTransform"
    node: bpy.types.GeometryNodeViewportTransform

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_projection(self) -> SocketLinker:
        """Output socket: Projection"""
        return self._output("Projection")

    @property
    def o_view(self) -> SocketLinker:
        """Output socket: View"""
        return self._output("View")

    @property
    def o_is_orthographic(self) -> SocketLinker:
        """Output socket: Is Orthographic"""
        return self._output("Is Orthographic")


class VoxelIndex(NodeBuilder):
    """Retrieve the integer coordinates of the voxel that the field is evaluated on"""

    _bl_idname = "GeometryNodeInputVoxelIndex"
    node: bpy.types.GeometryNodeInputVoxelIndex

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)

    @property
    def o_x(self) -> SocketLinker:
        """Output socket: X"""
        return self._output("X")

    @property
    def o_y(self) -> SocketLinker:
        """Output socket: Y"""
        return self._output("Y")

    @property
    def o_z(self) -> SocketLinker:
        """Output socket: Z"""
        return self._output("Z")

    @property
    def o_is_tile(self) -> SocketLinker:
        """Output socket: Is Tile"""
        return self._output("Is Tile")

    @property
    def o_extent_x(self) -> SocketLinker:
        """Output socket: Extent X"""
        return self._output("Extent X")

    @property
    def o_extent_y(self) -> SocketLinker:
        """Output socket: Extent Y"""
        return self._output("Extent Y")

    @property
    def o_extent_z(self) -> SocketLinker:
        """Output socket: Extent Z"""
        return self._output("Extent Z")
