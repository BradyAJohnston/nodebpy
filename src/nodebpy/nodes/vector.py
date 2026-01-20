from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class RadialTiling(NodeBuilder):
    """Transform Coordinate System for Radial Tiling"""

    name = "ShaderNodeRadialTiling"
    node: bpy.types.ShaderNodeRadialTiling

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        sides: TYPE_INPUT_VALUE = 5.0,
        roundness: TYPE_INPUT_VALUE = 0.0,
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
    """Map input vector components with curves"""

    name = "ShaderNodeVectorCurve"
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
    def i_factor(self) -> SocketLinker:
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


class VectorRotate(NodeBuilder):
    """Rotate a vector around a pivot point (center)"""

    name = "ShaderNodeVectorRotate"
    node: bpy.types.ShaderNodeVectorRotate

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        center: TYPE_INPUT_VECTOR = None,
        axis: TYPE_INPUT_VECTOR = None,
        angle: TYPE_INPUT_VALUE = 0.0,
        rotation: TYPE_INPUT_VECTOR = None,
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
