import bpy
from mathutils import Euler

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
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
