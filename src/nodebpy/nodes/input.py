import bpy
from mathutils import Euler
from typing_extensions import Literal

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_INT,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    _SampleIndexDataTypes,
)


class Boolean(NodeBuilder):
    """Provide a True/False value that can be connected to other nodes in the tree"""

    name = "FunctionNodeInputBool"
    node: bpy.types.FunctionNodeInputBool

    def __init__(self, boolean: bool = False):
        super().__init__()
        self.boolean = boolean

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


class Color(NodeBuilder):
    """Output a color value chosen with the color picker widget"""

    name = "FunctionNodeInputColor"
    node: bpy.types.FunctionNodeInputColor

    def __init__(
        self, value: tuple[float, float, float, float] = (1.0, 0.0, 1.0, 1.0), **kwargs
    ):
        super().__init__()
        self.value = value

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def value(self) -> tuple[float, float, float, float]:
        return self.node.value  # type: ignore

    @value.setter
    def value(self, value: tuple[float, float, float, float]):
        self.node.value = value


class Integer(NodeBuilder):
    """Provide an integer value that can be connected to other nodes in the tree"""

    name = "FunctionNodeInputInt"
    node: bpy.types.FunctionNodeInputInt

    def __init__(self, integer: int = 1):
        super().__init__()
        self.integer = integer

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


class Rotation(NodeBuilder):
    """Provide a rotation value that can be connected to other nodes in the tree"""

    name = "FunctionNodeInputRotation"
    node: bpy.types.FunctionNodeInputRotation

    def __init__(
        self,
        rotation_euler: tuple[float, float, float] | Euler = (
            0,
            0,
            0,
        ),
    ):
        super().__init__()
        self.rotation_euler = rotation_euler

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def rotation_euler(
        self,
    ) -> tuple[float, float, float] | Euler:
        return self.node.rotation_euler

    @rotation_euler.setter
    def rotation_euler(self, value: tuple[float, float, float] | Euler):
        self.node.rotation_euler = value


class SpecialCharacters(NodeBuilder):
    """Output string characters that cannot be typed directly with the keyboard"""

    name = "FunctionNodeInputSpecialCharacters"
    node: bpy.types.FunctionNodeInputSpecialCharacters

    @property
    def o_line_break(self) -> SocketLinker:
        """Output socket: Line Break"""
        return self._output("Line Break")

    @property
    def o_tab(self) -> SocketLinker:
        """Output socket: Tab"""
        return self._output("Tab")


class String(NodeBuilder):
    """Provide a string value that can be connected to other nodes in the tree"""

    name = "FunctionNodeInputString"
    node: bpy.types.FunctionNodeInputString

    def __init__(self, string: str = ""):
        super().__init__()
        self.string = string

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


class ActiveCamera(NodeBuilder):
    """Retrieve the scene's active camera"""

    name = "GeometryNodeInputActiveCamera"
    node: bpy.types.GeometryNodeInputActiveCamera

    @property
    def o_active_camera(self) -> SocketLinker:
        """Output socket: Active Camera"""
        return self._output("Active Camera")


class Collection(NodeBuilder):
    """Output a single collection"""

    name = "GeometryNodeInputCollection"
    node: bpy.types.GeometryNodeInputCollection

    def __init__(self, collection: bpy.types.Collection | None = None):
        super().__init__()
        self.collection = collection

    @property
    def collection(self) -> bpy.types.Collection | None:
        return self.node.collection

    @collection.setter
    def collection(self, value: bpy.types.Collection | None):
        self.node.collection = value

    @property
    def o_collection(self) -> SocketLinker:
        """Output socket: Collection"""
        return self._output("Collection")


class IsEdgeSmooth(NodeBuilder):
    """Retrieve whether each edge is marked for smooth or split normals"""

    name = "GeometryNodeInputEdgeSmooth"
    node: bpy.types.GeometryNodeInputEdgeSmooth

    @property
    def o_smooth(self) -> SocketLinker:
        """Output socket: Smooth"""
        return self._output("Smooth")


class ID(NodeBuilder):
    """Retrieve a stable random identifier value from the "id" attribute on the point domain, or the index if the attribute does not exist"""

    name = "GeometryNodeInputID"
    node: bpy.types.GeometryNodeInputID

    @property
    def o_id(self) -> SocketLinker:
        """Output socket: ID"""
        return self._output("ID")


class Image(NodeBuilder):
    """Input an image data-block"""

    name = "GeometryNodeInputImage"
    node: bpy.types.GeometryNodeInputImage

    def __init__(self, image: bpy.types.Image | None = None):
        super().__init__()
        self.image = image

    @property
    def image(self) -> bpy.types.Image | None:
        """Input socket: Image"""
        return self.node.image

    @image.setter
    def image(self, value: bpy.types.Image | None):
        self.node.image = value

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class Index(NodeBuilder):
    """Retrieve an integer value indicating the position of each element in the list, starting at zero"""

    name = "GeometryNodeInputIndex"
    node: bpy.types.GeometryNodeInputIndex

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")


class InstanceBounds(NodeBuilder):
    """Calculate position bounds of each instance's geometry set"""

    name = "GeometryNodeInputInstanceBounds"
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

    name = "GeometryNodeInputInstanceRotation"
    node: bpy.types.GeometryNodeInputInstanceRotation

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class InstanceScale(NodeBuilder):
    """Retrieve the scale of each instance in the geometry"""

    name = "GeometryNodeInputInstanceScale"
    node: bpy.types.GeometryNodeInputInstanceScale

    @property
    def o_scale(self) -> SocketLinker:
        """Output socket: Scale"""
        return self._output("Scale")


class Material(NodeBuilder):
    """Output a single material"""

    name = "GeometryNodeInputMaterial"
    node: bpy.types.GeometryNodeInputMaterial

    def __init__(self, material: bpy.types.Material | None = None):
        super().__init__()
        self.material = material

    @property
    def material(self) -> bpy.types.Material | None:
        """Input socket: Material"""
        return self.node.material

    @material.setter
    def material(self, value: bpy.types.Material | None):
        self.node.material

    @property
    def o_material(self) -> SocketLinker:
        """Output socket: Material"""
        return self._output("Material")


class MaterialIndex(NodeBuilder):
    """Retrieve the index of the material used for each element in the geometry's list of materials"""

    name = "GeometryNodeInputMaterialIndex"
    node: bpy.types.GeometryNodeInputMaterialIndex

    @property
    def o_material_index(self) -> SocketLinker:
        """Output socket: Material Index"""
        return self._output("Material Index")


class NamedLayerSelection(NodeBuilder):
    """Output a selection of a Grease Pencil layer"""

    name = "GeometryNodeInputNamedLayerSelection"
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

    name = "GeometryNodeInputNormal"
    node: bpy.types.GeometryNodeInputNormal

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

    name = "GeometryNodeInputObject"
    node: bpy.types.GeometryNodeInputObject

    def __init__(self, object: bpy.types.Object | None = None):
        super().__init__()
        self.node.object = object

    @property
    def object(self) -> bpy.types.Object | None:
        return self.node.object

    @object.setter
    def object(self, value: bpy.types.Object | None):
        self.node.object = value

    @property
    def o_object(self) -> SocketLinker:
        """Output socket: Object"""
        return self._output("Object")


class Position(NodeBuilder):
    """Retrieve a vector indicating the location of each element"""

    name = "GeometryNodeInputPosition"
    node: bpy.types.GeometryNodeInputPosition

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")


class Radius(NodeBuilder):
    """Retrieve the radius at each point on curve or point cloud geometry"""

    name = "GeometryNodeInputRadius"
    node: bpy.types.GeometryNodeInputRadius

    @property
    def o_radius(self) -> SocketLinker:
        """Output socket: Radius"""
        return self._output("Radius")


class SceneTime(NodeBuilder):
    """Retrieve the current time in the scene's animation in units of seconds or frames"""

    name = "GeometryNodeInputSceneTime"
    node: bpy.types.GeometryNodeInputSceneTime

    @property
    def o_seconds(self) -> SocketLinker:
        """Output socket: Seconds"""
        return self._output("Seconds")

    @property
    def o_frame(self) -> SocketLinker:
        """Output socket: Frame"""
        return self._output("Frame")


class IsFaceSmooth(NodeBuilder):
    """Retrieve whether each face is marked for smooth or sharp normals"""

    name = "GeometryNodeInputShadeSmooth"
    node: bpy.types.GeometryNodeInputShadeSmooth

    @property
    def o_smooth(self) -> SocketLinker:
        """Output socket: Smooth"""
        return self._output("Smooth")


class ShortestEdgePaths(NodeBuilder):
    """Find the shortest paths along mesh edges to selected end vertices, with customizable cost per edge"""

    name = "GeometryNodeInputShortestEdgePaths"
    node: bpy.types.GeometryNodeInputShortestEdgePaths

    def __init__(
        self,
        end_vertex: TYPE_INPUT_BOOLEAN = None,
        edge_cost: TYPE_INPUT_VALUE = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {"End Vertex": end_vertex, "Edge Cost": edge_cost}
        key_args.update(kwargs)

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


class IsSplineCyclic(NodeBuilder):
    """Retrieve whether each spline endpoint connects to the beginning"""

    name = "GeometryNodeInputSplineCyclic"
    node: bpy.types.GeometryNodeInputSplineCyclic

    @property
    def o_cyclic(self) -> SocketLinker:
        """Output socket: Cyclic"""
        return self._output("Cyclic")


class SplineResolution(NodeBuilder):
    """Retrieve the number of evaluated points that will be generated for every control point on curves"""

    name = "GeometryNodeInputSplineResolution"
    node: bpy.types.GeometryNodeInputSplineResolution

    @property
    def o_resolution(self) -> SocketLinker:
        """Output socket: Resolution"""
        return self._output("Resolution")


class CurveTangent(NodeBuilder):
    """Retrieve the direction of curves at each control point"""

    name = "GeometryNodeInputTangent"
    node: bpy.types.GeometryNodeInputTangent

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")


class VoxelIndex(NodeBuilder):
    """Retrieve the integer coordinates of the voxel that the field is evaluated on"""

    name = "GeometryNodeInputVoxelIndex"
    node: bpy.types.GeometryNodeInputVoxelIndex

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


class Value(NodeBuilder):
    """Input numerical values to other nodes in the tree"""

    name = "ShaderNodeValue"
    node: bpy.types.ShaderNodeValue

    def __init__(self, value: float = 0.0):
        super().__init__()
        self.value = value

    @property
    def value(self) -> float:
        """Input socket: Value"""
        # this node is a strange one because it doesn't have a value property,
        # instead we directly access and change the sockets default output
        return self.node.outputs[0].default_value  # type: ignore

    @value.setter
    def value(self, value: float):
        self.node.outputs[0].default_value = value  # type: ignore

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")


class Vector(NodeBuilder):
    """Provide a vector value that can be connected to other nodes in the tree"""

    name = "FunctionNodeInputVector"
    node: bpy.types.FunctionNodeInputVector

    def __init__(self, vector: tuple[float, float, float] = (0, 0, 0)):
        super().__init__()
        self.vector = vector

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def vector(self) -> tuple[float, float, float]:
        return tuple(list(self.node.vector))  # type: ignore

    @vector.setter
    def vector(self, value: tuple[float, float, float]):
        self.node.vector = value


class CameraInfo(NodeBuilder):
    """Retrieve information from a camera object"""

    name = "GeometryNodeCameraInfo"
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


class CollectionInfo(NodeBuilder):
    """Retrieve geometry instances from a collection"""

    name = "GeometryNodeCollectionInfo"
    node: bpy.types.GeometryNodeCollectionInfo

    def __init__(
        self,
        collection: TYPE_INPUT_COLLECTION = None,
        separate_children: TYPE_INPUT_BOOLEAN = False,
        reset_children: TYPE_INPUT_BOOLEAN = False,
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


class CornersOfEdge(NodeBuilder):
    """Retrieve face corners connected to edges"""

    name = "GeometryNodeCornersOfEdge"
    node: bpy.types.GeometryNodeCornersOfEdge

    def __init__(
        self,
        edge_index: TYPE_INPUT_INT = None,
        weights: TYPE_INPUT_VALUE = None,
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


class CornersOfVertex(NodeBuilder):
    """Retrieve face corners connected to vertices"""

    name = "GeometryNodeCornersOfVertex"
    node: bpy.types.GeometryNodeCornersOfVertex

    def __init__(
        self,
        vertex_index: TYPE_INPUT_INT = None,
        weights: TYPE_INPUT_VALUE = None,
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


class CornersOfFace(NodeBuilder):
    """Retrieve corners that make up a face"""

    name = "GeometryNodeCornersOfFace"
    node: bpy.types.GeometryNodeCornersOfFace

    def __init__(
        self,
        face_index: TYPE_INPUT_INT = None,
        weights: TYPE_INPUT_VALUE = None,
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


class EdgePathsToSelection(NodeBuilder):
    """Output a selection of edges by following paths across mesh edges"""

    name = "GeometryNodeEdgePathsToSelection"
    node: bpy.types.GeometryNodeEdgePathsToSelection

    def __init__(
        self,
        start_vertices: TYPE_INPUT_BOOLEAN = None,
        next_vertex_index: TYPE_INPUT_INT = None,
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


class EdgesOfCorner(NodeBuilder):
    """Retrieve the edges on both sides of a face corner"""

    name = "GeometryNodeEdgesOfCorner"
    node: bpy.types.GeometryNodeEdgesOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = None):
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

    name = "GeometryNodeEdgesOfVertex"
    node: bpy.types.GeometryNodeEdgesOfVertex

    def __init__(
        self,
        vertex_index: TYPE_INPUT_INT = None,
        weights: TYPE_INPUT_VALUE = None,
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

    name = "GeometryNodeEdgesToFaceGroups"
    node: bpy.types.GeometryNodeEdgesToFaceGroups

    def __init__(self, boundary_edges: TYPE_INPUT_BOOLEAN = None):
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


class FaceOfCorner(NodeBuilder):
    """Retrieve the face each face corner is part of"""

    name = "GeometryNodeFaceOfCorner"
    node: bpy.types.GeometryNodeFaceOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = None):
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


class ImageInfo(NodeBuilder):
    """Retrieve information about an image"""

    name = "GeometryNodeImageInfo"
    node: bpy.types.GeometryNodeImageInfo

    def __init__(self, image: TYPE_INPUT_IMAGE = None, frame: TYPE_INPUT_INT = 0):
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


class VertexOfCorner(NodeBuilder):
    """Retrieve the vertex each face corner is attached to"""

    name = "GeometryNodeVertexOfCorner"
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


class ImportCSV(NodeBuilder):
    """Import geometry from an CSV file"""

    name = "GeometryNodeImportCSV"
    node: bpy.types.GeometryNodeImportCSV

    def __init__(
        self, path: TYPE_INPUT_STRING = "", delimiter: TYPE_INPUT_STRING = ","
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

    name = "GeometryNodeImportOBJ"
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

    name = "GeometryNodeImportPLY"
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

    name = "GeometryNodeImportSTL"
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

    name = "GeometryNodeImportText"
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

    name = "GeometryNodeImportVDB"
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


class InstanceTransform(NodeBuilder):
    """Retrieve the full transformation of each instance in the geometry"""

    name = "GeometryNodeInstanceTransform"
    node: bpy.types.GeometryNodeInstanceTransform

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")


class IsViewport(NodeBuilder):
    """Retrieve whether the nodes are being evaluated for the viewport rather than the final render"""

    name = "GeometryNodeIsViewport"
    node: bpy.types.GeometryNodeIsViewport

    @property
    def o_is_viewport(self) -> SocketLinker:
        """Output socket: Is Viewport"""
        return self._output("Is Viewport")


class OffsetCornerInFace(NodeBuilder):
    """Retrieve corners in the same face as another"""

    name = "GeometryNodeOffsetCornerInFace"
    node: bpy.types.GeometryNodeOffsetCornerInFace

    def __init__(self, corner_index: TYPE_INPUT_INT = None, offset: TYPE_INPUT_INT = 0):
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


class ObjectInfo(NodeBuilder):
    """Retrieve information from an object"""

    name = "GeometryNodeObjectInfo"
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


class SelfObject(NodeBuilder):
    """Retrieve the object that contains the geometry nodes modifier currently being executed"""

    name = "GeometryNodeSelfObject"
    node: bpy.types.GeometryNodeSelfObject

    @property
    def o_self_object(self) -> SocketLinker:
        """Output socket: Self Object"""
        return self._output("Self Object")


class SplineLength(NodeBuilder):
    """Retrieve the total length of each spline, as a distance or as a number of points"""

    name = "GeometryNodeSplineLength"
    node: bpy.types.GeometryNodeSplineLength

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

    name = "GeometryNodeSplineParameter"
    node: bpy.types.GeometryNodeSplineParameter

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


class Cursor3D(NodeBuilder):
    """The scene's 3D cursor location and rotation"""

    name = "GeometryNodeTool3DCursor"
    node: bpy.types.GeometryNodeTool3DCursor

    @property
    def o_location(self) -> SocketLinker:
        """Output socket: Location"""
        return self._output("Location")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class ActiveElement(NodeBuilder):
    """Active element indices of the edited geometry, for tool execution"""

    name = "GeometryNodeToolActiveElement"
    node: bpy.types.GeometryNodeToolActiveElement

    def __init__(self, domain: Literal["POINT", "EDGE", "FACE", "LAYER"] = "POINT"):
        super().__init__()
        self.domain = domain

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


class FaceSet(NodeBuilder):
    """Each face's sculpt face set value"""

    name = "GeometryNodeToolFaceSet"
    node: bpy.types.GeometryNodeToolFaceSet

    @property
    def o_face_set(self) -> SocketLinker:
        """Output socket: Face Set"""
        return self._output("Face Set")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")


class MousePosition(NodeBuilder):
    """Retrieve the position of the mouse cursor"""

    name = "GeometryNodeToolMousePosition"
    node: bpy.types.GeometryNodeToolMousePosition

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


class Selection(NodeBuilder):
    """User selection of the edited geometry, for tool execution"""

    name = "GeometryNodeToolSelection"
    node: bpy.types.GeometryNodeToolSelection

    @property
    def o_boolean(self) -> SocketLinker:
        """Output socket: Boolean"""
        return self._output("Selection")

    @property
    def o_float(self) -> SocketLinker:
        """Output socket: Float"""
        return self._output("Float")


class UVTangent(NodeBuilder):
    """Generate tangent directions based on a UV map"""

    name = "GeometryNodeUVTangent"
    node: bpy.types.GeometryNodeUVTangent

    def __init__(
        self,
        method: Literal["Exact", "Fast"] = "Exact",
        uv: TYPE_INPUT_VECTOR = (0.0, 0.0),  # type: ignore
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


class ViewportTransform(NodeBuilder):
    """Retrieve the view direction and location of the 3D viewport"""

    name = "GeometryNodeViewportTransform"
    node: bpy.types.GeometryNodeViewportTransform

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


def _typed_named_attribute(data_type: str):
    @classmethod
    def method(cls, name: TYPE_INPUT_STRING) -> "NamedAttribute":
        """Create a NamedAttribute with a non-default_data_type"""
        return cls(name=name, data_type=data_type)

    return method


class NamedAttribute(NodeBuilder):
    """Retrieve the data of a specified attribute"""

    name = "GeometryNodeInputNamedAttribute"
    node: bpy.types.GeometryNodeInputNamedAttribute
    float = _typed_named_attribute("FLOAT")
    integer = _typed_named_attribute("INT")
    boolean = _typed_named_attribute("BOOLEAN")
    vector = _typed_named_attribute("FLOAT_VECTOR")
    color = _typed_named_attribute("FLOAT_COLOR")
    quaternion = _typed_named_attribute("QUATNERNION")
    matrix = _typed_named_attribute("FLOAT4X4")

    def __init__(
        self,
        name: TYPE_INPUT_STRING = "",
        *,
        data_type: _SampleIndexDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Name": name}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    ) -> _SampleIndexDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _SampleIndexDataTypes,
    ):
        self.node.data_type = value


class EndpointSelection(NodeBuilder):
    """Provide a selection for an arbitrary number of endpoints in each spline"""

    name = "GeometryNodeCurveEndpointSelection"
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


class HandleTypeSelection(NodeBuilder):
    """Provide a selection based on the handle types of Bézier control points"""

    name = "GeometryNodeCurveHandleTypeSelection"
    node: bpy.types.GeometryNodeCurveHandleTypeSelection

    def __init__(
        self,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
        left: bool = True,
        right: bool = True,
    ):
        super().__init__()
        self.handle_type = handle_type
        self.left = left
        self.right = right

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")

    @property
    def handle_type(self) -> Literal["FREE", "AUTO", "VECTOR", "ALIGN"]:
        return self.node.handle_type

    @handle_type.setter
    def handle_type(self, value: Literal["FREE", "AUTO", "VECTOR", "ALIGN"]):
        self.node.handle_type = value

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        match value, self.right:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        match self.left, value:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]):
        self.node.mode = value


class CurveOfPoint(NodeBuilder):
    """Retrieve the curve a control point is part of"""

    name = "GeometryNodeCurveOfPoint"
    node: bpy.types.GeometryNodeCurveOfPoint

    def __init__(self, point_index: TYPE_INPUT_INT = None):
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


class CurveHandlePositions(NodeBuilder):
    """Retrieve the position of each Bézier control point's handles"""

    name = "GeometryNodeInputCurveHandlePositions"
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


class CurveTilt(NodeBuilder):
    """Retrieve the angle at each control point used to twist the curve's normal around its tangent"""

    name = "GeometryNodeInputCurveTilt"
    node: bpy.types.GeometryNodeInputCurveTilt

    @property
    def o_tilt(self) -> SocketLinker:
        """Output socket: Tilt"""
        return self._output("Tilt")


class OffsetPointInCurve(NodeBuilder):
    """Offset a control point index within its curve"""

    name = "GeometryNodeOffsetPointInCurve"
    node: bpy.types.GeometryNodeOffsetPointInCurve

    def __init__(self, point_index: TYPE_INPUT_INT = None, offset: TYPE_INPUT_INT = 0):
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

    name = "GeometryNodePointsOfCurve"
    node: bpy.types.GeometryNodePointsOfCurve

    def __init__(
        self,
        curve_index: TYPE_INPUT_INT = None,
        weights: TYPE_INPUT_VALUE = None,
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


class EdgeAngle(NodeBuilder):
    """The angle between the normals of connected manifold faces"""

    name = "GeometryNodeInputMeshEdgeAngle"
    node: bpy.types.GeometryNodeInputMeshEdgeAngle

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

    name = "GeometryNodeInputMeshEdgeNeighbors"
    node: bpy.types.GeometryNodeInputMeshEdgeNeighbors

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class EdgeVertices(NodeBuilder):
    """Retrieve topology information relating to each edge of a mesh"""

    name = "GeometryNodeInputMeshEdgeVertices"
    node: bpy.types.GeometryNodeInputMeshEdgeVertices

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


class FaceArea(NodeBuilder):
    """Calculate the surface area of a mesh's faces"""

    name = "GeometryNodeInputMeshFaceArea"
    node: bpy.types.GeometryNodeInputMeshFaceArea

    @property
    def o_area(self) -> SocketLinker:
        """Output socket: Area"""
        return self._output("Area")


class IsFacePlanar(NodeBuilder):
    """Retrieve whether all triangles in a face are on the same plane, i.e. whether they have the same normal"""

    name = "GeometryNodeInputMeshFaceIsPlanar"
    node: bpy.types.GeometryNodeInputMeshFaceIsPlanar

    def __init__(self, threshold: TYPE_INPUT_VALUE = 0.001):
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


class FaceNeighbors(NodeBuilder):
    """Retrieve topology information relating to each face of a mesh"""

    name = "GeometryNodeInputMeshFaceNeighbors"
    node: bpy.types.GeometryNodeInputMeshFaceNeighbors

    @property
    def o_vertex_count(self) -> SocketLinker:
        """Output socket: Vertex Count"""
        return self._output("Vertex Count")

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class MeshIsland(NodeBuilder):
    """Retrieve information about separate connected regions in a mesh"""

    name = "GeometryNodeInputMeshIsland"
    node: bpy.types.GeometryNodeInputMeshIsland

    @property
    def o_island_index(self) -> SocketLinker:
        """Output socket: Island Index"""
        return self._output("Island Index")

    @property
    def o_island_count(self) -> SocketLinker:
        """Output socket: Island Count"""
        return self._output("Island Count")


class VertexNeighbors(NodeBuilder):
    """Retrieve topology information relating to each vertex of a mesh"""

    name = "GeometryNodeInputMeshVertexNeighbors"
    node: bpy.types.GeometryNodeInputMeshVertexNeighbors

    @property
    def o_vertex_count(self) -> SocketLinker:
        """Output socket: Vertex Count"""
        return self._output("Vertex Count")

    @property
    def o_face_count(self) -> SocketLinker:
        """Output socket: Face Count"""
        return self._output("Face Count")


class FaceGroupBoundaries(NodeBuilder):
    """Find edges on the boundaries between groups of faces with the same ID value"""

    name = "GeometryNodeMeshFaceSetBoundaries"
    node: bpy.types.GeometryNodeMeshFaceSetBoundaries

    def __init__(self, face_set: TYPE_INPUT_INT = 0):
        super().__init__()
        key_args = {"Face Set": face_set}
        self._establish_links(**key_args)

    @property
    def i_face_group_id(self) -> SocketLinker:
        """Input socket: Face Group ID"""
        return self._input("Face Set")

    @property
    def o_boundary_edges(self) -> SocketLinker:
        """Output socket: Boundary Edges"""
        return self._output("Boundary Edges")
