from typing import Literal

import bpy

from ...builder import NodeBuilder, SocketLinker
from ...types import (
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class Bump(NodeBuilder):
    """
    Generate a perturbed normal from a height texture for bump mapping. Typically used for faking highly detailed surfaces
    """

    _bl_idname = "ShaderNodeBump"
    node: bpy.types.ShaderNodeBump

    def __init__(
        self,
        strength: TYPE_INPUT_VALUE = 1.0,
        distance: TYPE_INPUT_VALUE = 0.001,
        filter_width: TYPE_INPUT_VALUE = 0.1,
        height: TYPE_INPUT_VALUE = 1.0,
        normal: TYPE_INPUT_VECTOR = None,
        *,
        invert: bool = False,
    ):
        super().__init__()
        key_args = {
            "Strength": strength,
            "Distance": distance,
            "Filter Width": filter_width,
            "Height": height,
            "Normal": normal,
        }
        self.invert = invert
        self._establish_links(**key_args)

    @property
    def i_strength(self) -> SocketLinker:
        """Input socket: Strength"""
        return self._input("Strength")

    @property
    def i_distance(self) -> SocketLinker:
        """Input socket: Distance"""
        return self._input("Distance")

    @property
    def i_filter_width(self) -> SocketLinker:
        """Input socket: Filter Width"""
        return self._input("Filter Width")

    @property
    def i_height(self) -> SocketLinker:
        """Input socket: Height"""
        return self._input("Height")

    @property
    def i_normal(self) -> SocketLinker:
        """Input socket: Normal"""
        return self._input("Normal")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def invert(self) -> bool:
        return self.node.invert

    @invert.setter
    def invert(self, value: bool):
        self.node.invert = value


class Displacement(NodeBuilder):
    """
    Displace the surface along the surface normal
    """

    _bl_idname = "ShaderNodeDisplacement"
    node: bpy.types.ShaderNodeDisplacement

    def __init__(
        self,
        height: TYPE_INPUT_VALUE = 0.0,
        midlevel: TYPE_INPUT_VALUE = 0.5,
        scale: TYPE_INPUT_VALUE = 0.01,
        normal: TYPE_INPUT_VECTOR = None,
        *,
        space: Literal["OBJECT", "WORLD"] = "OBJECT",
    ):
        super().__init__()
        key_args = {
            "Height": height,
            "Midlevel": midlevel,
            "Scale": scale,
            "Normal": normal,
        }
        self.space = space
        self._establish_links(**key_args)

    @property
    def i_height(self) -> SocketLinker:
        """Input socket: Height"""
        return self._input("Height")

    @property
    def i_midlevel(self) -> SocketLinker:
        """Input socket: Midlevel"""
        return self._input("Midlevel")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_normal(self) -> SocketLinker:
        """Input socket: Normal"""
        return self._input("Normal")

    @property
    def o_displacement(self) -> SocketLinker:
        """Output socket: Displacement"""
        return self._output("Displacement")

    @property
    def space(self) -> Literal["OBJECT", "WORLD"]:
        return self.node.space

    @space.setter
    def space(self, value: Literal["OBJECT", "WORLD"]):
        self.node.space = value


class Mapping(NodeBuilder):
    """
    Transform the input vector by applying translation, rotation, and scale
    """

    _bl_idname = "ShaderNodeMapping"
    node: bpy.types.ShaderNodeMapping

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        location: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VECTOR = None,
        *,
        vector_type: Literal["POINT", "TEXTURE", "VECTOR", "NORMAL"] = "POINT",
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Location": location,
            "Rotation": rotation,
            "Scale": scale,
        }
        self.vector_type = vector_type
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_location(self) -> SocketLinker:
        """Input socket: Location"""
        return self._input("Location")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def vector_type(self) -> Literal["POINT", "TEXTURE", "VECTOR", "NORMAL"]:
        return self.node.vector_type

    @vector_type.setter
    def vector_type(self, value: Literal["POINT", "TEXTURE", "VECTOR", "NORMAL"]):
        self.node.vector_type = value


class Normal(NodeBuilder):
    """
    Generate a normal vector and a dot product
    """

    _bl_idname = "ShaderNodeNormal"
    node: bpy.types.ShaderNodeNormal

    def __init__(self, normal: TYPE_INPUT_VECTOR = None):
        super().__init__()
        key_args = {"Normal": normal}

        self._establish_links(**key_args)

    @property
    def i_normal(self) -> SocketLinker:
        """Input socket: Normal"""
        return self._input("Normal")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def o_dot(self) -> SocketLinker:
        """Output socket: Dot"""
        return self._output("Dot")


class NormalMap(NodeBuilder):
    """
    Generate a perturbed normal from an RGB normal map image. Typically used for faking highly detailed surfaces
    """

    _bl_idname = "ShaderNodeNormalMap"
    node: bpy.types.ShaderNodeNormalMap

    def __init__(
        self,
        strength: TYPE_INPUT_VALUE = 1.0,
        color: TYPE_INPUT_COLOR = None,
        *,
        space: Literal[
            "TANGENT", "OBJECT", "WORLD", "BLENDER_OBJECT", "BLENDER_WORLD"
        ] = "TANGENT",
        uv_map: str = "",
    ):
        super().__init__()
        key_args = {"Strength": strength, "Color": color}
        self.space = space
        self.uv_map = uv_map
        self._establish_links(**key_args)

    @property
    def i_strength(self) -> SocketLinker:
        """Input socket: Strength"""
        return self._input("Strength")

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def o_normal(self) -> SocketLinker:
        """Output socket: Normal"""
        return self._output("Normal")

    @property
    def space(
        self,
    ) -> Literal["TANGENT", "OBJECT", "WORLD", "BLENDER_OBJECT", "BLENDER_WORLD"]:
        return self.node.space

    @space.setter
    def space(
        self,
        value: Literal["TANGENT", "OBJECT", "WORLD", "BLENDER_OBJECT", "BLENDER_WORLD"],
    ):
        self.node.space = value

    @property
    def uv_map(self) -> str:
        return self.node.uv_map

    @uv_map.setter
    def uv_map(self, value: str):
        self.node.uv_map = value


class RadialTiling(NodeBuilder):
    """
    Transform Coordinate System for Radial Tiling
    """

    _bl_idname = "ShaderNodeRadialTiling"
    node: bpy.types.ShaderNodeRadialTiling

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        sides: TYPE_INPUT_VALUE = 5.0,
        roundness: TYPE_INPUT_VALUE = 0.0,
        *,
        normalize: bool = False,
    ):
        super().__init__()
        key_args = {"Vector": vector, "Sides": sides, "Roundness": roundness}
        self.normalize = normalize
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_sides(self) -> SocketLinker:
        """Input socket: Sides"""
        return self._input("Sides")

    @property
    def i_roundness(self) -> SocketLinker:
        """Input socket: Roundness"""
        return self._input("Roundness")

    @property
    def o_segment_coordinates(self) -> SocketLinker:
        """Output socket: Segment Coordinates"""
        return self._output("Segment Coordinates")

    @property
    def o_segment_id(self) -> SocketLinker:
        """Output socket: Segment ID"""
        return self._output("Segment ID")

    @property
    def o_segment_width(self) -> SocketLinker:
        """Output socket: Segment Width"""
        return self._output("Segment Width")

    @property
    def o_segment_rotation(self) -> SocketLinker:
        """Output socket: Segment Rotation"""
        return self._output("Segment Rotation")

    @property
    def normalize(self) -> bool:
        return self.node.normalize

    @normalize.setter
    def normalize(self, value: bool):
        self.node.normalize = value


class VectorCurves(NodeBuilder):
    """
    Map input vector components with curves
    """

    _bl_idname = "ShaderNodeVectorCurve"
    node: bpy.types.ShaderNodeVectorCurve

    def __init__(
        self,
        fac: TYPE_INPUT_VALUE = 1.0,
        vector: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {"Fac": fac, "Vector": vector}

        self._establish_links(**key_args)

    @property
    def i_fac(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Fac")

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")


class VectorDisplacement(NodeBuilder):
    """
    Displace the surface along an arbitrary direction
    """

    _bl_idname = "ShaderNodeVectorDisplacement"
    node: bpy.types.ShaderNodeVectorDisplacement

    def __init__(
        self,
        vector: TYPE_INPUT_COLOR = None,
        midlevel: TYPE_INPUT_VALUE = 0.0,
        scale: TYPE_INPUT_VALUE = 0.01,
        *,
        space: Literal["TANGENT", "OBJECT", "WORLD"] = "TANGENT",
    ):
        super().__init__()
        key_args = {"Vector": vector, "Midlevel": midlevel, "Scale": scale}
        self.space = space
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_midlevel(self) -> SocketLinker:
        """Input socket: Midlevel"""
        return self._input("Midlevel")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_displacement(self) -> SocketLinker:
        """Output socket: Displacement"""
        return self._output("Displacement")

    @property
    def space(self) -> Literal["TANGENT", "OBJECT", "WORLD"]:
        return self.node.space

    @space.setter
    def space(self, value: Literal["TANGENT", "OBJECT", "WORLD"]):
        self.node.space = value


class VectorMath(NodeBuilder):
    """
    Perform vector math operation
    """

    _bl_idname = "ShaderNodeVectorMath"
    node: bpy.types.ShaderNodeVectorMath

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        vector_001: TYPE_INPUT_VECTOR = None,
        vector_002: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VALUE = 1.0,
        *,
        operation: Literal[
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVIDE",
            "MULTIPLY_ADD",
            "CROSS_PRODUCT",
            "PROJECT",
            "REFLECT",
            "REFRACT",
            "FACEFORWARD",
            "DOT_PRODUCT",
            "DISTANCE",
            "LENGTH",
            "SCALE",
            "NORMALIZE",
            "ABSOLUTE",
            "POWER",
            "SIGN",
            "MINIMUM",
            "MAXIMUM",
            "FLOOR",
            "CEIL",
            "FRACTION",
            "MODULO",
            "WRAP",
            "SNAP",
            "SINE",
            "COSINE",
            "TANGENT",
        ] = "ADD",
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Vector_001": vector_001,
            "Vector_002": vector_002,
            "Scale": scale,
        }
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def add(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Add'."""
        return cls(operation="ADD", vector=vector, vector_001=vector_001)

    @classmethod
    def subtract(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Subtract'."""
        return cls(operation="SUBTRACT", vector=vector, vector_001=vector_001)

    @classmethod
    def multiply(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Multiply'."""
        return cls(operation="MULTIPLY", vector=vector, vector_001=vector_001)

    @classmethod
    def divide(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Divide'."""
        return cls(operation="DIVIDE", vector=vector, vector_001=vector_001)

    @classmethod
    def multiply_add(
        cls,
        vector: TYPE_INPUT_VECTOR = None,
        vector_001: TYPE_INPUT_VECTOR = None,
        vector_002: TYPE_INPUT_VECTOR = None,
    ) -> "VectorMath":
        """Create Vector Math with operation 'Multiply Add'."""
        return cls(
            operation="MULTIPLY_ADD",
            vector=vector,
            vector_001=vector_001,
            vector_002=vector_002,
        )

    @classmethod
    def cross_product(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Cross Product'."""
        return cls(operation="CROSS_PRODUCT", vector=vector, vector_001=vector_001)

    @classmethod
    def project(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Project'."""
        return cls(operation="PROJECT", vector=vector, vector_001=vector_001)

    @classmethod
    def reflect(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Reflect'."""
        return cls(operation="REFLECT", vector=vector, vector_001=vector_001)

    @classmethod
    def refract(
        cls,
        vector: TYPE_INPUT_VECTOR = None,
        vector_001: TYPE_INPUT_VECTOR = None,
        scale: TYPE_INPUT_VALUE = 1.0,
    ) -> "VectorMath":
        """Create Vector Math with operation 'Refract'."""
        return cls(
            operation="REFRACT", vector=vector, vector_001=vector_001, scale=scale
        )

    @classmethod
    def faceforward(
        cls,
        vector: TYPE_INPUT_VECTOR = None,
        vector_001: TYPE_INPUT_VECTOR = None,
        vector_002: TYPE_INPUT_VECTOR = None,
    ) -> "VectorMath":
        """Create Vector Math with operation 'Faceforward'."""
        return cls(
            operation="FACEFORWARD",
            vector=vector,
            vector_001=vector_001,
            vector_002=vector_002,
        )

    @classmethod
    def dot_product(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Dot Product'."""
        return cls(operation="DOT_PRODUCT", vector=vector, vector_001=vector_001)

    @classmethod
    def distance(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Distance'."""
        return cls(operation="DISTANCE", vector=vector, vector_001=vector_001)

    @classmethod
    def length(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Length'."""
        return cls(operation="LENGTH", vector=vector)

    @classmethod
    def scale(
        cls, vector: TYPE_INPUT_VECTOR = None, scale: TYPE_INPUT_VALUE = 1.0
    ) -> "VectorMath":
        """Create Vector Math with operation 'Scale'."""
        return cls(operation="SCALE", vector=vector, scale=scale)

    @classmethod
    def normalize(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Normalize'."""
        return cls(operation="NORMALIZE", vector=vector)

    @classmethod
    def absolute(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Absolute'."""
        return cls(operation="ABSOLUTE", vector=vector)

    @classmethod
    def power(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Power'."""
        return cls(operation="POWER", vector=vector, vector_001=vector_001)

    @classmethod
    def sign(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Sign'."""
        return cls(operation="SIGN", vector=vector)

    @classmethod
    def minimum(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Minimum'."""
        return cls(operation="MINIMUM", vector=vector, vector_001=vector_001)

    @classmethod
    def maximum(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Maximum'."""
        return cls(operation="MAXIMUM", vector=vector, vector_001=vector_001)

    @classmethod
    def floor(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Floor'."""
        return cls(operation="FLOOR", vector=vector)

    @classmethod
    def ceil(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Ceil'."""
        return cls(operation="CEIL", vector=vector)

    @classmethod
    def fraction(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Fraction'."""
        return cls(operation="FRACTION", vector=vector)

    @classmethod
    def modulo(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Modulo'."""
        return cls(operation="MODULO", vector=vector, vector_001=vector_001)

    @classmethod
    def wrap(
        cls,
        vector: TYPE_INPUT_VECTOR = None,
        vector_001: TYPE_INPUT_VECTOR = None,
        vector_002: TYPE_INPUT_VECTOR = None,
    ) -> "VectorMath":
        """Create Vector Math with operation 'Wrap'."""
        return cls(
            operation="WRAP",
            vector=vector,
            vector_001=vector_001,
            vector_002=vector_002,
        )

    @classmethod
    def snap(
        cls, vector: TYPE_INPUT_VECTOR = None, vector_001: TYPE_INPUT_VECTOR = None
    ) -> "VectorMath":
        """Create Vector Math with operation 'Snap'."""
        return cls(operation="SNAP", vector=vector, vector_001=vector_001)

    @classmethod
    def sine(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Sine'."""
        return cls(operation="SINE", vector=vector)

    @classmethod
    def cosine(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Cosine'."""
        return cls(operation="COSINE", vector=vector)

    @classmethod
    def tangent(cls, vector: TYPE_INPUT_VECTOR = None) -> "VectorMath":
        """Create Vector Math with operation 'Tangent'."""
        return cls(operation="TANGENT", vector=vector)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_vector_001(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector_001")

    @property
    def i_vector_002(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector_002")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def operation(
        self,
    ) -> Literal[
        "ADD",
        "SUBTRACT",
        "MULTIPLY",
        "DIVIDE",
        "MULTIPLY_ADD",
        "CROSS_PRODUCT",
        "PROJECT",
        "REFLECT",
        "REFRACT",
        "FACEFORWARD",
        "DOT_PRODUCT",
        "DISTANCE",
        "LENGTH",
        "SCALE",
        "NORMALIZE",
        "ABSOLUTE",
        "POWER",
        "SIGN",
        "MINIMUM",
        "MAXIMUM",
        "FLOOR",
        "CEIL",
        "FRACTION",
        "MODULO",
        "WRAP",
        "SNAP",
        "SINE",
        "COSINE",
        "TANGENT",
    ]:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: Literal[
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVIDE",
            "MULTIPLY_ADD",
            "CROSS_PRODUCT",
            "PROJECT",
            "REFLECT",
            "REFRACT",
            "FACEFORWARD",
            "DOT_PRODUCT",
            "DISTANCE",
            "LENGTH",
            "SCALE",
            "NORMALIZE",
            "ABSOLUTE",
            "POWER",
            "SIGN",
            "MINIMUM",
            "MAXIMUM",
            "FLOOR",
            "CEIL",
            "FRACTION",
            "MODULO",
            "WRAP",
            "SNAP",
            "SINE",
            "COSINE",
            "TANGENT",
        ],
    ):
        self.node.operation = value


class VectorRotate(NodeBuilder):
    """
    Rotate a vector around a pivot point (center)
    """

    _bl_idname = "ShaderNodeVectorRotate"
    node: bpy.types.ShaderNodeVectorRotate

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        center: TYPE_INPUT_VECTOR = None,
        axis: TYPE_INPUT_VECTOR = None,
        angle: TYPE_INPUT_VALUE = 0.0,
        rotation: TYPE_INPUT_VECTOR = None,
        *,
        rotation_type: Literal[
            "AXIS_ANGLE", "X_AXIS", "Y_AXIS", "Z_AXIS", "EULER_XYZ"
        ] = "AXIS_ANGLE",
        invert: bool = False,
    ):
        super().__init__()
        key_args = {
            "Vector": vector,
            "Center": center,
            "Axis": axis,
            "Angle": angle,
            "Rotation": rotation,
        }
        self.rotation_type = rotation_type
        self.invert = invert
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_center(self) -> SocketLinker:
        """Input socket: Center"""
        return self._input("Center")

    @property
    def i_axis(self) -> SocketLinker:
        """Input socket: Axis"""
        return self._input("Axis")

    @property
    def i_angle(self) -> SocketLinker:
        """Input socket: Angle"""
        return self._input("Angle")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def rotation_type(
        self,
    ) -> Literal["AXIS_ANGLE", "X_AXIS", "Y_AXIS", "Z_AXIS", "EULER_XYZ"]:
        return self.node.rotation_type

    @rotation_type.setter
    def rotation_type(
        self, value: Literal["AXIS_ANGLE", "X_AXIS", "Y_AXIS", "Z_AXIS", "EULER_XYZ"]
    ):
        self.node.rotation_type = value

    @property
    def invert(self) -> bool:
        return self.node.invert

    @invert.setter
    def invert(self, value: bool):
        self.node.invert = value


class VectorTransform(NodeBuilder):
    """
    Convert a vector, point, or normal between world, camera, and object coordinate space
    """

    _bl_idname = "ShaderNodeVectorTransform"
    node: bpy.types.ShaderNodeVectorTransform

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        vector_type: Literal["POINT", "VECTOR", "NORMAL"] = "VECTOR",
        convert_from: Literal["WORLD", "OBJECT", "CAMERA"] = "WORLD",
        convert_to: Literal["WORLD", "OBJECT", "CAMERA"] = "OBJECT",
    ):
        super().__init__()
        key_args = {"Vector": vector}
        self.vector_type = vector_type
        self.convert_from = convert_from
        self.convert_to = convert_to
        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def vector_type(self) -> Literal["POINT", "VECTOR", "NORMAL"]:
        return self.node.vector_type

    @vector_type.setter
    def vector_type(self, value: Literal["POINT", "VECTOR", "NORMAL"]):
        self.node.vector_type = value

    @property
    def convert_from(self) -> Literal["WORLD", "OBJECT", "CAMERA"]:
        return self.node.convert_from

    @convert_from.setter
    def convert_from(self, value: Literal["WORLD", "OBJECT", "CAMERA"]):
        self.node.convert_from = value

    @property
    def convert_to(self) -> Literal["WORLD", "OBJECT", "CAMERA"]:
        return self.node.convert_to

    @convert_to.setter
    def convert_to(self, value: Literal["WORLD", "OBJECT", "CAMERA"]):
        self.node.convert_to = value
