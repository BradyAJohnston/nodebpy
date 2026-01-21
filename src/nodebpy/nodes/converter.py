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


class AccumulateField(NodeBuilder):
    """Add the values of an evaluated field together and output the running total for each element"""

    name = "GeometryNodeAccumulateField"
    node: bpy.types.GeometryNodeAccumulateField

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 1.0,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 1.0, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, group_index=group_index)

    @classmethod
    def integer(
        cls, value: TYPE_INPUT_INT = 1, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Integer'."""
        return cls(data_type="INT", value=value, group_index=group_index)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value, group_index=group_index)

    @classmethod
    def transform(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Transform'."""
        return cls(data_type="TRANSFORM", value=value, group_index=group_index)

    @classmethod
    def point(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Point'."""
        return cls(domain="POINT", value=value, group_index=group_index)

    @classmethod
    def edge(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Edge'."""
        return cls(domain="EDGE", value=value, group_index=group_index)

    @classmethod
    def face(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Face'."""
        return cls(domain="FACE", value=value, group_index=group_index)

    @classmethod
    def spline(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Spline'."""
        return cls(domain="CURVE", value=value, group_index=group_index)

    @classmethod
    def instance(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value, group_index=group_index)

    @classmethod
    def layer(
        cls, value: TYPE_INPUT_MATRIX = None, group_index: TYPE_INPUT_INT = 0
    ) -> "AccumulateField":
        """Create Accumulate Field with operation 'Layer'."""
        return cls(domain="LAYER", value=value, group_index=group_index)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_index(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_leading(self) -> SocketLinker:
        """Output socket: Leading"""
        return self._output("Leading")

    @property
    def o_trailing(self) -> SocketLinker:
        """Output socket: Trailing"""
        return self._output("Trailing")

    @property
    def o_total(self) -> SocketLinker:
        """Output socket: Total"""
        return self._output("Total")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "FLOAT_VECTOR", "TRANSFORM"]):
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


class AlignRotationToVector(NodeBuilder):
    """Orient a rotation along the given direction"""

    name = "FunctionNodeAlignRotationToVector"
    node: bpy.types.FunctionNodeAlignRotationToVector

    def __init__(
        self,
        rotation: TYPE_INPUT_ROTATION = None,
        factor: TYPE_INPUT_VALUE = 1.0,
        vector: TYPE_INPUT_VECTOR = None,
        *,
        axis: Literal["X", "Y", "Z"] = "Z",
        pivot_axis: Literal["AUTO", "X", "Y", "Z"] = "AUTO",
    ):
        super().__init__()
        key_args = {"Rotation": rotation, "Factor": factor, "Vector": vector}
        self.axis = axis
        self.pivot_axis = pivot_axis
        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_factor(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Factor")

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def axis(self) -> Literal["X", "Y", "Z"]:
        return self.node.axis

    @axis.setter
    def axis(self, value: Literal["X", "Y", "Z"]):
        self.node.axis = value

    @property
    def pivot_axis(self) -> Literal["AUTO", "X", "Y", "Z"]:
        return self.node.pivot_axis

    @pivot_axis.setter
    def pivot_axis(self, value: Literal["AUTO", "X", "Y", "Z"]):
        self.node.pivot_axis = value


class AxesToRotation(NodeBuilder):
    """Create a rotation from a primary and (ideally orthogonal) secondary axis"""

    name = "FunctionNodeAxesToRotation"
    node: bpy.types.FunctionNodeAxesToRotation

    def __init__(
        self,
        primary_axis: TYPE_INPUT_VECTOR = None,
        secondary_axis: TYPE_INPUT_VECTOR = None,
        *,
        primary: Literal["X", "Y", "Z"] = "Z",
        secondary: Literal["X", "Y", "Z"] = "X",
    ):
        super().__init__()
        key_args = {"Primary Axis": primary_axis, "Secondary Axis": secondary_axis}
        self.primary_axis = primary_axis
        self.secondary_axis = secondary_axis
        self._establish_links(**key_args)

    @property
    def i_primary_axis(self) -> SocketLinker:
        """Input socket: Primary Axis"""
        return self._input("Primary Axis")

    @property
    def i_secondary_axis(self) -> SocketLinker:
        """Input socket: Secondary Axis"""
        return self._input("Secondary Axis")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def primary(self) -> Literal["X", "Y", "Z"]:
        return self.node.primary_axis

    @primary.setter
    def primary(self, value: Literal["X", "Y", "Z"]):
        self.node.primary_axis = value

    @property
    def secondary(self) -> Literal["X", "Y", "Z"]:
        return self.node.secondary_axis

    @secondary.setter
    def secondary(self, value: Literal["X", "Y", "Z"]):
        self.node.secondary_axis = value


class AxisAngleToRotation(NodeBuilder):
    """Build a rotation from an axis and a rotation around that axis"""

    name = "FunctionNodeAxisAngleToRotation"
    node: bpy.types.FunctionNodeAxisAngleToRotation

    def __init__(
        self,
        axis: TYPE_INPUT_VECTOR = None,
        angle: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {"Axis": axis, "Angle": angle}

        self._establish_links(**key_args)

    @property
    def i_axis(self) -> SocketLinker:
        """Input socket: Axis"""
        return self._input("Axis")

    @property
    def i_angle(self) -> SocketLinker:
        """Input socket: Angle"""
        return self._input("Angle")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class BitMath(NodeBuilder):
    """Perform bitwise operations on 32-bit integers"""

    name = "FunctionNodeBitMath"
    node: bpy.types.FunctionNodeBitMath

    def __init__(
        self,
        a: TYPE_INPUT_INT = 0,
        b: TYPE_INPUT_INT = 0,
        shift: TYPE_INPUT_INT = 0,
        *,
        operation: Literal["AND", "OR", "XOR", "NOT", "SHIFT", "ROTATE"] = "AND",
    ):
        super().__init__()
        key_args = {"A": a, "B": b, "Shift": shift}
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def l_and(cls, a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'And'."""
        return cls(operation="AND", a=a, b=b)

    @classmethod
    def l_or(cls, a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Or'."""
        return cls(operation="OR", a=a, b=b)

    @classmethod
    def l_not(cls, a: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Not'."""
        return cls(operation="NOT", a=a)

    @classmethod
    def shift(cls, a: TYPE_INPUT_INT = 0, shift: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Shift'."""
        return cls(operation="SHIFT", a=a, shift=shift)

    @classmethod
    def rotate(cls, a: TYPE_INPUT_INT = 0, shift: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Rotate'."""
        return cls(operation="ROTATE", a=a, shift=shift)

    @property
    def i_a(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A")

    @property
    def i_b(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B")

    @property
    def i_shift(self) -> SocketLinker:
        """Input socket: Shift"""
        return self._input("Shift")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def operation(self) -> Literal["AND", "OR", "XOR", "NOT", "SHIFT", "ROTATE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["AND", "OR", "XOR", "NOT", "SHIFT", "ROTATE"]):
        self.node.operation = value


class Blackbody(NodeBuilder):
    """Convert a blackbody temperature to an RGB value"""

    name = "ShaderNodeBlackbody"
    node: bpy.types.ShaderNodeBlackbody

    def __init__(self, temperature: TYPE_INPUT_VALUE = 6500.0):
        super().__init__()
        key_args = {"Temperature": temperature}

        self._establish_links(**key_args)

    @property
    def i_temperature(self) -> SocketLinker:
        """Input socket: Temperature"""
        return self._input("Temperature")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")


class BooleanMath(NodeBuilder):
    """Perform a logical operation on the given boolean inputs"""

    name = "FunctionNodeBooleanMath"
    node: bpy.types.FunctionNodeBooleanMath

    def __init__(
        self,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
        *,
        operation: Literal[
            "AND", "OR", "NOT", "NAND", "NOR", "XNOR", "XOR", "IMPLY", "NIMPLY"
        ] = "AND",
    ):
        super().__init__()
        key_args = {"Boolean": boolean, "Boolean_001": boolean_001}
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def l_and(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'And'."""
        return cls(operation="AND", boolean=boolean, boolean_001=boolean_001)

    @classmethod
    def l_or(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'Or'."""
        return cls(operation="OR", boolean=boolean, boolean_001=boolean_001)

    @classmethod
    def l_not(cls, boolean: TYPE_INPUT_BOOLEAN = False) -> "BooleanMath":
        """Create Boolean Math with operation 'Not'."""
        return cls(operation="NOT", boolean=boolean)

    @classmethod
    def nor(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'Nor'."""
        return cls(operation="NOR", boolean=boolean, boolean_001=boolean_001)

    @classmethod
    def equal(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'Equal'."""
        return cls(operation="XNOR", boolean=boolean, boolean_001=boolean_001)

    @classmethod
    def imply(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'Imply'."""
        return cls(operation="IMPLY", boolean=boolean, boolean_001=boolean_001)

    @classmethod
    def subtract(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'Subtract'."""
        return cls(operation="NIMPLY", boolean=boolean, boolean_001=boolean_001)

    @property
    def i_boolean(self) -> SocketLinker:
        """Input socket: Boolean"""
        return self._input("Boolean")

    @property
    def i_boolean_001(self) -> SocketLinker:
        """Input socket: Boolean"""
        return self._input("Boolean_001")

    @property
    def o_boolean(self) -> SocketLinker:
        """Output socket: Boolean"""
        return self._output("Boolean")

    @property
    def operation(
        self,
    ) -> Literal["AND", "OR", "NOT", "NAND", "NOR", "XNOR", "XOR", "IMPLY", "NIMPLY"]:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: Literal[
            "AND", "OR", "NOT", "NAND", "NOR", "XNOR", "XOR", "IMPLY", "NIMPLY"
        ],
    ):
        self.node.operation = value


class Clamp(NodeBuilder):
    """Clamp a value between a minimum and a maximum"""

    name = "ShaderNodeClamp"
    node: bpy.types.ShaderNodeClamp

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 1.0,
        min: TYPE_INPUT_VALUE = 0.0,
        max: TYPE_INPUT_VALUE = 1.0,
        *,
        clamp_type: Literal["MINMAX", "RANGE"] = "MINMAX",
    ):
        super().__init__()
        key_args = {"Value": value, "Min": min, "Max": max}
        self.clamp_type = clamp_type
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_min(self) -> SocketLinker:
        """Input socket: Min"""
        return self._input("Min")

    @property
    def i_max(self) -> SocketLinker:
        """Input socket: Max"""
        return self._input("Max")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")

    @property
    def clamp_type(self) -> Literal["MINMAX", "RANGE"]:
        return self.node.clamp_type

    @clamp_type.setter
    def clamp_type(self, value: Literal["MINMAX", "RANGE"]):
        self.node.clamp_type = value


class ColorRamp(NodeBuilder):
    """Map values to colors with the use of a gradient"""

    name = "ShaderNodeValToRGB"
    node: bpy.types.ShaderNodeValToRGB

    def __init__(self, fac: TYPE_INPUT_VALUE = 0.5):
        super().__init__()
        key_args = {"Fac": fac}

        self._establish_links(**key_args)

    @property
    def i_fac(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Fac")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")


class CombineBundle(NodeBuilder):
    """Combine multiple socket values into one."""

    name = "NodeCombineBundle"
    node: bpy.types.Node

    def __init__(self, define_signature: bool = False):
        super().__init__()
        key_args = {}
        self.define_signature = define_signature
        self._establish_links(**key_args)

    @property
    def o_bundle(self) -> SocketLinker:
        """Output socket: Bundle"""
        return self._output("Bundle")

    @property
    def define_signature(self) -> bool:
        return self.node.define_signature

    @define_signature.setter
    def define_signature(self, value: bool):
        self.node.define_signature = value


class CombineColor(NodeBuilder):
    """Combine four channels into a single color, based on a particular color model"""

    name = "FunctionNodeCombineColor"
    node: bpy.types.FunctionNodeCombineColor

    def __init__(
        self,
        red: TYPE_INPUT_VALUE = 0.0,
        green: TYPE_INPUT_VALUE = 0.0,
        blue: TYPE_INPUT_VALUE = 0.0,
        alpha: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["RGB", "HSV", "HSL"] = "RGB",
    ):
        super().__init__()
        key_args = {"Red": red, "Green": green, "Blue": blue, "Alpha": alpha}
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_red(self) -> SocketLinker:
        """Input socket: Red"""
        return self._input("Red")

    @property
    def i_green(self) -> SocketLinker:
        """Input socket: Green"""
        return self._input("Green")

    @property
    def i_blue(self) -> SocketLinker:
        """Input socket: Blue"""
        return self._input("Blue")

    @property
    def i_alpha(self) -> SocketLinker:
        """Input socket: Alpha"""
        return self._input("Alpha")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def mode(self) -> Literal["RGB", "HSV", "HSL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["RGB", "HSV", "HSL"]):
        self.node.mode = value


class CombineMatrix(NodeBuilder):
    """Construct a 4x4 matrix from its individual values"""

    name = "FunctionNodeCombineMatrix"
    node: bpy.types.FunctionNodeCombineMatrix

    def __init__(
        self,
        column_1_row_1: TYPE_INPUT_VALUE = 1.0,
        column_1_row_2: TYPE_INPUT_VALUE = 0.0,
        column_1_row_3: TYPE_INPUT_VALUE = 0.0,
        column_1_row_4: TYPE_INPUT_VALUE = 0.0,
        column_2_row_1: TYPE_INPUT_VALUE = 0.0,
        column_2_row_2: TYPE_INPUT_VALUE = 1.0,
        column_2_row_3: TYPE_INPUT_VALUE = 0.0,
        column_2_row_4: TYPE_INPUT_VALUE = 0.0,
        column_3_row_1: TYPE_INPUT_VALUE = 0.0,
        column_3_row_2: TYPE_INPUT_VALUE = 0.0,
        column_3_row_3: TYPE_INPUT_VALUE = 1.0,
        column_3_row_4: TYPE_INPUT_VALUE = 0.0,
        column_4_row_1: TYPE_INPUT_VALUE = 0.0,
        column_4_row_2: TYPE_INPUT_VALUE = 0.0,
        column_4_row_3: TYPE_INPUT_VALUE = 0.0,
        column_4_row_4: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {
            "Column 1 Row 1": column_1_row_1,
            "Column 1 Row 2": column_1_row_2,
            "Column 1 Row 3": column_1_row_3,
            "Column 1 Row 4": column_1_row_4,
            "Column 2 Row 1": column_2_row_1,
            "Column 2 Row 2": column_2_row_2,
            "Column 2 Row 3": column_2_row_3,
            "Column 2 Row 4": column_2_row_4,
            "Column 3 Row 1": column_3_row_1,
            "Column 3 Row 2": column_3_row_2,
            "Column 3 Row 3": column_3_row_3,
            "Column 3 Row 4": column_3_row_4,
            "Column 4 Row 1": column_4_row_1,
            "Column 4 Row 2": column_4_row_2,
            "Column 4 Row 3": column_4_row_3,
            "Column 4 Row 4": column_4_row_4,
        }

        self._establish_links(**key_args)

    @property
    def i_column_1_row_1(self) -> SocketLinker:
        """Input socket: Column 1 Row 1"""
        return self._input("Column 1 Row 1")

    @property
    def i_column_1_row_2(self) -> SocketLinker:
        """Input socket: Column 1 Row 2"""
        return self._input("Column 1 Row 2")

    @property
    def i_column_1_row_3(self) -> SocketLinker:
        """Input socket: Column 1 Row 3"""
        return self._input("Column 1 Row 3")

    @property
    def i_column_1_row_4(self) -> SocketLinker:
        """Input socket: Column 1 Row 4"""
        return self._input("Column 1 Row 4")

    @property
    def i_column_2_row_1(self) -> SocketLinker:
        """Input socket: Column 2 Row 1"""
        return self._input("Column 2 Row 1")

    @property
    def i_column_2_row_2(self) -> SocketLinker:
        """Input socket: Column 2 Row 2"""
        return self._input("Column 2 Row 2")

    @property
    def i_column_2_row_3(self) -> SocketLinker:
        """Input socket: Column 2 Row 3"""
        return self._input("Column 2 Row 3")

    @property
    def i_column_2_row_4(self) -> SocketLinker:
        """Input socket: Column 2 Row 4"""
        return self._input("Column 2 Row 4")

    @property
    def i_column_3_row_1(self) -> SocketLinker:
        """Input socket: Column 3 Row 1"""
        return self._input("Column 3 Row 1")

    @property
    def i_column_3_row_2(self) -> SocketLinker:
        """Input socket: Column 3 Row 2"""
        return self._input("Column 3 Row 2")

    @property
    def i_column_3_row_3(self) -> SocketLinker:
        """Input socket: Column 3 Row 3"""
        return self._input("Column 3 Row 3")

    @property
    def i_column_3_row_4(self) -> SocketLinker:
        """Input socket: Column 3 Row 4"""
        return self._input("Column 3 Row 4")

    @property
    def i_column_4_row_1(self) -> SocketLinker:
        """Input socket: Column 4 Row 1"""
        return self._input("Column 4 Row 1")

    @property
    def i_column_4_row_2(self) -> SocketLinker:
        """Input socket: Column 4 Row 2"""
        return self._input("Column 4 Row 2")

    @property
    def i_column_4_row_3(self) -> SocketLinker:
        """Input socket: Column 4 Row 3"""
        return self._input("Column 4 Row 3")

    @property
    def i_column_4_row_4(self) -> SocketLinker:
        """Input socket: Column 4 Row 4"""
        return self._input("Column 4 Row 4")

    @property
    def o_matrix(self) -> SocketLinker:
        """Output socket: Matrix"""
        return self._output("Matrix")


class CombineTransform(NodeBuilder):
    """Combine a translation vector, a rotation, and a scale vector into a transformation matrix"""

    name = "FunctionNodeCombineTransform"
    node: bpy.types.FunctionNodeCombineTransform

    def __init__(
        self,
        translation: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_ROTATION = None,
        scale: TYPE_INPUT_VECTOR = None,
    ):
        super().__init__()
        key_args = {"Translation": translation, "Rotation": rotation, "Scale": scale}

        self._establish_links(**key_args)

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
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")


class CombineXYZ(NodeBuilder):
    """Create a vector from X, Y, and Z components"""

    name = "ShaderNodeCombineXYZ"
    node: bpy.types.ShaderNodeCombineXYZ

    def __init__(
        self,
        x: TYPE_INPUT_VALUE = 0.0,
        y: TYPE_INPUT_VALUE = 0.0,
        z: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {"X": x, "Y": y, "Z": z}

        self._establish_links(**key_args)

    @property
    def i_x(self) -> SocketLinker:
        """Input socket: X"""
        return self._input("X")

    @property
    def i_y(self) -> SocketLinker:
        """Input socket: Y"""
        return self._input("Y")

    @property
    def i_z(self) -> SocketLinker:
        """Input socket: Z"""
        return self._input("Z")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")


class Compare(NodeBuilder):
    """Perform a comparison operation on the two given inputs"""

    name = "FunctionNodeCompare"
    node: bpy.types.FunctionNodeCompare

    def __init__(
        self,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        a_int: TYPE_INPUT_INT = 0,
        b_int: TYPE_INPUT_INT = 0,
        a_vec3: TYPE_INPUT_VECTOR = None,
        b_vec3: TYPE_INPUT_VECTOR = None,
        a_col: TYPE_INPUT_COLOR = None,
        b_col: TYPE_INPUT_COLOR = None,
        a_str: TYPE_INPUT_STRING = "",
        b_str: TYPE_INPUT_STRING = "",
        c: TYPE_INPUT_VALUE = 0.9,
        angle: TYPE_INPUT_VALUE = 0.0873,
        epsilon: TYPE_INPUT_VALUE = 0.001,
        *,
        operation: Literal[
            "LESS_THAN",
            "LESS_EQUAL",
            "GREATER_THAN",
            "GREATER_EQUAL",
            "EQUAL",
            "NOT_EQUAL",
        ] = "GREATER_THAN",
        data_type: Literal["FLOAT", "INT", "VECTOR", "RGBA", "STRING"] = "FLOAT",
        mode: Literal[
            "ELEMENT", "LENGTH", "AVERAGE", "DOT_PRODUCT", "DIRECTION"
        ] = "ELEMENT",
    ):
        super().__init__()
        key_args = {
            "A": a,
            "B": b,
            "A_INT": a_int,
            "B_INT": b_int,
            "A_VEC3": a_vec3,
            "B_VEC3": b_vec3,
            "A_COL": a_col,
            "B_COL": b_col,
            "A_STR": a_str,
            "B_STR": b_str,
            "C": c,
            "Angle": angle,
            "Epsilon": epsilon,
        }
        self.operation = operation
        self.data_type = data_type
        self.mode = mode
        self._establish_links(**key_args)

    @classmethod
    def equal(
        cls,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        epsilon: TYPE_INPUT_VALUE = 0.001,
    ) -> "Compare":
        """Create Compare with operation 'Equal'."""
        return cls(operation="EQUAL", a=a, b=b, epsilon=epsilon)

    @classmethod
    def float(
        cls,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        epsilon: TYPE_INPUT_VALUE = 0.001,
    ) -> "Compare":
        """Create Compare with operation 'Float'."""
        return cls(data_type="FLOAT", a=a, b=b, epsilon=epsilon)

    @classmethod
    def integer(cls, a_int: TYPE_INPUT_INT = 0, b_int: TYPE_INPUT_INT = 0) -> "Compare":
        """Create Compare with operation 'Integer'."""
        return cls(data_type="INT", a_int=a_int, b_int=b_int)

    @classmethod
    def vector(
        cls,
        a_vec3: TYPE_INPUT_VECTOR = None,
        b_vec3: TYPE_INPUT_VECTOR = None,
        epsilon: TYPE_INPUT_VALUE = 0.001,
    ) -> "Compare":
        """Create Compare with operation 'Vector'."""
        return cls(data_type="VECTOR", a_vec3=a_vec3, b_vec3=b_vec3, epsilon=epsilon)

    @classmethod
    def color(
        cls,
        a_col: TYPE_INPUT_COLOR = None,
        b_col: TYPE_INPUT_COLOR = None,
        epsilon: TYPE_INPUT_VALUE = 0.001,
    ) -> "Compare":
        """Create Compare with operation 'Color'."""
        return cls(data_type="RGBA", a_col=a_col, b_col=b_col, epsilon=epsilon)

    @classmethod
    def string(
        cls, a_str: TYPE_INPUT_STRING = "", b_str: TYPE_INPUT_STRING = ""
    ) -> "Compare":
        """Create Compare with operation 'String'."""
        return cls(data_type="STRING", a_str=a_str, b_str=b_str)

    @property
    def i_a(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A")

    @property
    def i_b(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B")

    @property
    def i_a_int(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_INT")

    @property
    def i_b_int(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_INT")

    @property
    def i_a_vec3(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_VEC3")

    @property
    def i_b_vec3(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_VEC3")

    @property
    def i_a_col(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_COL")

    @property
    def i_b_col(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_COL")

    @property
    def i_a_str(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_STR")

    @property
    def i_b_str(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_STR")

    @property
    def i_c(self) -> SocketLinker:
        """Input socket: C"""
        return self._input("C")

    @property
    def i_angle(self) -> SocketLinker:
        """Input socket: Angle"""
        return self._input("Angle")

    @property
    def i_epsilon(self) -> SocketLinker:
        """Input socket: Epsilon"""
        return self._input("Epsilon")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")

    @property
    def operation(
        self,
    ) -> Literal[
        "LESS_THAN", "LESS_EQUAL", "GREATER_THAN", "GREATER_EQUAL", "EQUAL", "NOT_EQUAL"
    ]:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: Literal[
            "LESS_THAN",
            "LESS_EQUAL",
            "GREATER_THAN",
            "GREATER_EQUAL",
            "EQUAL",
            "NOT_EQUAL",
        ],
    ):
        self.node.operation = value

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "VECTOR", "RGBA", "STRING"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "VECTOR", "RGBA", "STRING"]):
        self.node.data_type = value

    @property
    def mode(
        self,
    ) -> Literal["ELEMENT", "LENGTH", "AVERAGE", "DOT_PRODUCT", "DIRECTION"]:
        return self.node.mode

    @mode.setter
    def mode(
        self, value: Literal["ELEMENT", "LENGTH", "AVERAGE", "DOT_PRODUCT", "DIRECTION"]
    ):
        self.node.mode = value


class EulerToRotation(NodeBuilder):
    """Build a rotation from separate angles around each axis"""

    name = "FunctionNodeEulerToRotation"
    node: bpy.types.FunctionNodeEulerToRotation

    def __init__(self, euler: TYPE_INPUT_VECTOR = None):
        super().__init__()
        key_args = {"Euler": euler}

        self._establish_links(**key_args)

    @property
    def i_euler(self) -> SocketLinker:
        """Input socket: Euler"""
        return self._input("Euler")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class EvaluateAtIndex(NodeBuilder):
    """Retrieve data of other elements in the context's geometry"""

    name = "GeometryNodeFieldAtIndex"
    node: bpy.types.GeometryNodeFieldAtIndex

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
        *,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
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
        key_args = {"Value": value, "Index": index}
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def point(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Point'."""
        return cls(domain="POINT", value=value, index=index)

    @classmethod
    def edge(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Edge'."""
        return cls(domain="EDGE", value=value, index=index)

    @classmethod
    def face(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Face'."""
        return cls(domain="FACE", value=value, index=index)

    @classmethod
    def spline(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Spline'."""
        return cls(domain="CURVE", value=value, index=index)

    @classmethod
    def instance(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value, index=index)

    @classmethod
    def layer(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Layer'."""
        return cls(domain="LAYER", value=value, index=index)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, index=index)

    @classmethod
    def integer(
        cls, value: TYPE_INPUT_INT = 0, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Integer'."""
        return cls(data_type="INT", value=value, index=index)

    @classmethod
    def boolean(
        cls, value: TYPE_INPUT_BOOLEAN = False, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", value=value, index=index)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value, index=index)

    @classmethod
    def color(
        cls, value: TYPE_INPUT_COLOR = None, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Color'."""
        return cls(data_type="FLOAT_COLOR", value=value, index=index)

    @classmethod
    def quaternion(
        cls, value: TYPE_INPUT_ROTATION = None, index: TYPE_INPUT_INT = 0
    ) -> "EvaluateAtIndex":
        """Create Evaluate at Index with operation 'Quaternion'."""
        return cls(data_type="QUATERNION", value=value, index=index)

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


class EvaluateOnDomain(NodeBuilder):
    """Retrieve values from a field on a different domain besides the domain from the context"""

    name = "GeometryNodeFieldOnDomain"
    node: bpy.types.GeometryNodeFieldOnDomain

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        *,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
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
        key_args = {"Value": value}
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def point(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Point'."""
        return cls(domain="POINT", value=value)

    @classmethod
    def edge(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Edge'."""
        return cls(domain="EDGE", value=value)

    @classmethod
    def face(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Face'."""
        return cls(domain="FACE", value=value)

    @classmethod
    def spline(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Spline'."""
        return cls(domain="CURVE", value=value)

    @classmethod
    def instance(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value)

    @classmethod
    def layer(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Layer'."""
        return cls(domain="LAYER", value=value)

    @classmethod
    def float(cls, value: TYPE_INPUT_VALUE = 0.0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Float'."""
        return cls(data_type="FLOAT", value=value)

    @classmethod
    def integer(cls, value: TYPE_INPUT_INT = 0) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Integer'."""
        return cls(data_type="INT", value=value)

    @classmethod
    def boolean(cls, value: TYPE_INPUT_BOOLEAN = False) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", value=value)

    @classmethod
    def vector(cls, value: TYPE_INPUT_VECTOR = None) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value)

    @classmethod
    def color(cls, value: TYPE_INPUT_COLOR = None) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Color'."""
        return cls(data_type="FLOAT_COLOR", value=value)

    @classmethod
    def quaternion(cls, value: TYPE_INPUT_ROTATION = None) -> "EvaluateOnDomain":
        """Create Evaluate on Domain with operation 'Quaternion'."""
        return cls(data_type="QUATERNION", value=value)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

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


class FieldAverage(NodeBuilder):
    """Calculate the mean and median of a given field"""

    name = "GeometryNodeFieldAverage"
    node: bpy.types.GeometryNodeFieldAverage

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, group_index=group_index)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value, group_index=group_index)

    @classmethod
    def point(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Point'."""
        return cls(domain="POINT", value=value, group_index=group_index)

    @classmethod
    def edge(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Edge'."""
        return cls(domain="EDGE", value=value, group_index=group_index)

    @classmethod
    def face(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Face'."""
        return cls(domain="FACE", value=value, group_index=group_index)

    @classmethod
    def spline(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Spline'."""
        return cls(domain="CURVE", value=value, group_index=group_index)

    @classmethod
    def instance(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value, group_index=group_index)

    @classmethod
    def layer(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldAverage":
        """Create Field Average with operation 'Layer'."""
        return cls(domain="LAYER", value=value, group_index=group_index)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_index(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_mean(self) -> SocketLinker:
        """Output socket: Mean"""
        return self._output("Mean")

    @property
    def o_median(self) -> SocketLinker:
        """Output socket: Median"""
        return self._output("Median")

    @property
    def data_type(self) -> Literal["FLOAT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "FLOAT_VECTOR"]):
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


class FieldMinMax(NodeBuilder):
    """Calculate the minimum and maximum of a given field"""

    name = "GeometryNodeFieldMinAndMax"
    node: bpy.types.GeometryNodeFieldMinAndMax

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR"] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, group_index=group_index)

    @classmethod
    def integer(
        cls, value: TYPE_INPUT_INT = 0, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Integer'."""
        return cls(data_type="INT", value=value, group_index=group_index)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value, group_index=group_index)

    @classmethod
    def point(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Point'."""
        return cls(domain="POINT", value=value, group_index=group_index)

    @classmethod
    def edge(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Edge'."""
        return cls(domain="EDGE", value=value, group_index=group_index)

    @classmethod
    def face(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Face'."""
        return cls(domain="FACE", value=value, group_index=group_index)

    @classmethod
    def spline(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Spline'."""
        return cls(domain="CURVE", value=value, group_index=group_index)

    @classmethod
    def instance(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value, group_index=group_index)

    @classmethod
    def layer(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldMinMax":
        """Create Field Min & Max with operation 'Layer'."""
        return cls(domain="LAYER", value=value, group_index=group_index)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_index(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_min(self) -> SocketLinker:
        """Output socket: Min"""
        return self._output("Min")

    @property
    def o_max(self) -> SocketLinker:
        """Output socket: Max"""
        return self._output("Max")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "FLOAT_VECTOR"]):
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


class FieldVariance(NodeBuilder):
    """Calculate the standard deviation and variance of a given field"""

    name = "GeometryNodeFieldVariance"
    node: bpy.types.GeometryNodeFieldVariance

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, group_index=group_index)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", value=value, group_index=group_index)

    @classmethod
    def point(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Point'."""
        return cls(domain="POINT", value=value, group_index=group_index)

    @classmethod
    def edge(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Edge'."""
        return cls(domain="EDGE", value=value, group_index=group_index)

    @classmethod
    def face(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Face'."""
        return cls(domain="FACE", value=value, group_index=group_index)

    @classmethod
    def spline(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Spline'."""
        return cls(domain="CURVE", value=value, group_index=group_index)

    @classmethod
    def instance(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Instance'."""
        return cls(domain="INSTANCE", value=value, group_index=group_index)

    @classmethod
    def layer(
        cls, value: TYPE_INPUT_VECTOR = None, group_index: TYPE_INPUT_INT = 0
    ) -> "FieldVariance":
        """Create Field Variance with operation 'Layer'."""
        return cls(domain="LAYER", value=value, group_index=group_index)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_index(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group Index")

    @property
    def o_standard_deviation(self) -> SocketLinker:
        """Output socket: Standard Deviation"""
        return self._output("Standard Deviation")

    @property
    def o_variance(self) -> SocketLinker:
        """Output socket: Variance"""
        return self._output("Variance")

    @property
    def data_type(self) -> Literal["FLOAT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "FLOAT_VECTOR"]):
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


class FindInString(NodeBuilder):
    """Find the number of times a given string occurs in another string and the position of the first match"""

    name = "FunctionNodeFindInString"
    node: bpy.types.FunctionNodeFindInString

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        search: TYPE_INPUT_STRING = "",
    ):
        super().__init__()
        key_args = {"String": string, "Search": search}

        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def i_search(self) -> SocketLinker:
        """Input socket: Search"""
        return self._input("Search")

    @property
    def o_first_found(self) -> SocketLinker:
        """Output socket: First Found"""
        return self._output("First Found")

    @property
    def o_count(self) -> SocketLinker:
        """Output socket: Count"""
        return self._output("Count")


class FloatCurve(NodeBuilder):
    """Map an input float to a curve and outputs a float value"""

    name = "ShaderNodeFloatCurve"
    node: bpy.types.ShaderNodeFloatCurve

    def __init__(
        self,
        factor: TYPE_INPUT_VALUE = 1.0,
        value: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"Factor": factor, "Value": value}

        self._establish_links(**key_args)

    @property
    def i_factor(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Factor")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")


class FloatToInteger(NodeBuilder):
    """Convert the given floating-point number to an integer, with a choice of methods"""

    name = "FunctionNodeFloatToInt"
    node: bpy.types.FunctionNodeFloatToInt

    def __init__(
        self,
        float: TYPE_INPUT_VALUE = 0.0,
        *,
        rounding_mode: Literal["ROUND", "FLOOR", "CEILING", "TRUNCATE"] = "ROUND",
    ):
        super().__init__()
        key_args = {"Float": float}
        self.rounding_mode = rounding_mode
        self._establish_links(**key_args)

    @property
    def i_float(self) -> SocketLinker:
        """Input socket: Float"""
        return self._input("Float")

    @property
    def o_integer(self) -> SocketLinker:
        """Output socket: Integer"""
        return self._output("Integer")

    @property
    def rounding_mode(self) -> Literal["ROUND", "FLOOR", "CEILING", "TRUNCATE"]:
        return self.node.rounding_mode

    @rounding_mode.setter
    def rounding_mode(self, value: Literal["ROUND", "FLOOR", "CEILING", "TRUNCATE"]):
        self.node.rounding_mode = value


class Gamma(NodeBuilder):
    """Apply a gamma correction"""

    name = "ShaderNodeGamma"
    node: bpy.types.ShaderNodeGamma

    def __init__(
        self,
        color: TYPE_INPUT_COLOR = None,
        gamma: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"Color": color, "Gamma": gamma}

        self._establish_links(**key_args)

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def i_gamma(self) -> SocketLinker:
        """Input socket: Gamma"""
        return self._input("Gamma")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")


class HashValue(NodeBuilder):
    """Generate a randomized integer using the given input value as a seed"""

    name = "FunctionNodeHashValue"
    node: bpy.types.FunctionNodeHashValue

    def __init__(
        self,
        value: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal[
            "FLOAT", "INT", "VECTOR", "RGBA", "ROTATION", "MATRIX", "STRING"
        ] = "INT",
    ):
        super().__init__()
        key_args = {"Value": value, "Seed": seed}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, seed=seed)

    @classmethod
    def integer(
        cls, value: TYPE_INPUT_INT = 0, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Integer'."""
        return cls(data_type="INT", value=value, seed=seed)

    @classmethod
    def vector(
        cls, value: TYPE_INPUT_VECTOR = None, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Vector'."""
        return cls(data_type="VECTOR", value=value, seed=seed)

    @classmethod
    def color(
        cls, value: TYPE_INPUT_COLOR = None, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Color'."""
        return cls(data_type="RGBA", value=value, seed=seed)

    @classmethod
    def rotation(
        cls, value: TYPE_INPUT_ROTATION = None, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Rotation'."""
        return cls(data_type="ROTATION", value=value, seed=seed)

    @classmethod
    def matrix(
        cls, value: TYPE_INPUT_MATRIX = None, seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'Matrix'."""
        return cls(data_type="MATRIX", value=value, seed=seed)

    @classmethod
    def string(
        cls, value: TYPE_INPUT_STRING = "", seed: TYPE_INPUT_INT = 0
    ) -> "HashValue":
        """Create Hash Value with operation 'String'."""
        return cls(data_type="STRING", value=value, seed=seed)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_seed(self) -> SocketLinker:
        """Input socket: Seed"""
        return self._input("Seed")

    @property
    def o_hash(self) -> SocketLinker:
        """Output socket: Hash"""
        return self._output("Hash")

    @property
    def data_type(
        self,
    ) -> Literal["FLOAT", "INT", "VECTOR", "RGBA", "ROTATION", "MATRIX", "STRING"]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT", "INT", "VECTOR", "RGBA", "ROTATION", "MATRIX", "STRING"
        ],
    ):
        self.node.data_type = value


class IndexOfNearest(NodeBuilder):
    """Find the nearest element in a group. Similar to the "Sample Nearest" node"""

    name = "GeometryNodeIndexOfNearest"
    node: bpy.types.GeometryNodeIndexOfNearest

    def __init__(
        self,
        position: TYPE_INPUT_VECTOR = None,
        group_id: TYPE_INPUT_INT = 0,
    ):
        super().__init__()
        key_args = {"Position": position, "Group ID": group_id}

        self._establish_links(**key_args)

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_has_neighbor(self) -> SocketLinker:
        """Output socket: Has Neighbor"""
        return self._output("Has Neighbor")


class IntegerMath(NodeBuilder):
    """Perform various math operations on the given integer inputs"""

    name = "FunctionNodeIntegerMath"
    node: bpy.types.FunctionNodeIntegerMath

    def __init__(
        self,
        value: TYPE_INPUT_INT = 0,
        value_001: TYPE_INPUT_INT = 0,
        value_002: TYPE_INPUT_INT = 0,
        *,
        operation: Literal[
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVIDE",
            "MULTIPLY_ADD",
            "ABSOLUTE",
            "NEGATE",
            "POWER",
            "MINIMUM",
            "MAXIMUM",
            "SIGN",
            "DIVIDE_ROUND",
            "DIVIDE_FLOOR",
            "DIVIDE_CEIL",
            "FLOORED_MODULO",
            "MODULO",
            "GCD",
            "LCM",
        ] = "ADD",
    ):
        super().__init__()
        key_args = {"Value": value, "Value_001": value_001, "Value_002": value_002}
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def add(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Add'."""
        return cls(operation="ADD", value=value, value_001=value_001)

    @classmethod
    def subtract(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Subtract'."""
        return cls(operation="SUBTRACT", value=value, value_001=value_001)

    @classmethod
    def multiply(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Multiply'."""
        return cls(operation="MULTIPLY", value=value, value_001=value_001)

    @classmethod
    def divide(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Divide'."""
        return cls(operation="DIVIDE", value=value, value_001=value_001)

    @classmethod
    def absolute(cls, value: TYPE_INPUT_INT = 0) -> "IntegerMath":
        """Create Integer Math with operation 'Absolute'."""
        return cls(operation="ABSOLUTE", value=value)

    @classmethod
    def negate(cls, value: TYPE_INPUT_INT = 0) -> "IntegerMath":
        """Create Integer Math with operation 'Negate'."""
        return cls(operation="NEGATE", value=value)

    @classmethod
    def power(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Power'."""
        return cls(operation="POWER", value=value, value_001=value_001)

    @classmethod
    def minimum(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Minimum'."""
        return cls(operation="MINIMUM", value=value, value_001=value_001)

    @classmethod
    def maximum(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Maximum'."""
        return cls(operation="MAXIMUM", value=value, value_001=value_001)

    @classmethod
    def sign(cls, value: TYPE_INPUT_INT = 0) -> "IntegerMath":
        """Create Integer Math with operation 'Sign'."""
        return cls(operation="SIGN", value=value)

    @classmethod
    def modulo(
        cls, value: TYPE_INPUT_INT = 0, value_001: TYPE_INPUT_INT = 0
    ) -> "IntegerMath":
        """Create Integer Math with operation 'Modulo'."""
        return cls(operation="MODULO", value=value, value_001=value_001)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_value_001(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value_001")

    @property
    def i_value_002(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value_002")

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
        "ABSOLUTE",
        "NEGATE",
        "POWER",
        "MINIMUM",
        "MAXIMUM",
        "SIGN",
        "DIVIDE_ROUND",
        "DIVIDE_FLOOR",
        "DIVIDE_CEIL",
        "FLOORED_MODULO",
        "MODULO",
        "GCD",
        "LCM",
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
            "ABSOLUTE",
            "NEGATE",
            "POWER",
            "MINIMUM",
            "MAXIMUM",
            "SIGN",
            "DIVIDE_ROUND",
            "DIVIDE_FLOOR",
            "DIVIDE_CEIL",
            "FLOORED_MODULO",
            "MODULO",
            "GCD",
            "LCM",
        ],
    ):
        self.node.operation = value


class InvertMatrix(NodeBuilder):
    """Compute the inverse of the given matrix, if one exists"""

    name = "FunctionNodeInvertMatrix"
    node: bpy.types.FunctionNodeInvertMatrix

    def __init__(self, matrix: TYPE_INPUT_MATRIX = None):
        super().__init__()
        key_args = {"Matrix": matrix}

        self._establish_links(**key_args)

    @property
    def i_matrix(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix")

    @property
    def o_matrix(self) -> SocketLinker:
        """Output socket: Matrix"""
        return self._output("Matrix")

    @property
    def o_invertible(self) -> SocketLinker:
        """Output socket: Invertible"""
        return self._output("Invertible")


class InvertRotation(NodeBuilder):
    """Compute the inverse of the given rotation"""

    name = "FunctionNodeInvertRotation"
    node: bpy.types.FunctionNodeInvertRotation

    def __init__(self, rotation: TYPE_INPUT_ROTATION = None):
        super().__init__()
        key_args = {"Rotation": rotation}

        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class JoinBundle(NodeBuilder):
    """Join multiple bundles together"""

    name = "NodeJoinBundle"
    node: bpy.types.Node

    def __init__(self, bundle: TYPE_INPUT_BUNDLE = None):
        super().__init__()
        key_args = {"Bundle": bundle}

        self._establish_links(**key_args)

    @property
    def i_bundle(self) -> SocketLinker:
        """Input socket: Bundle"""
        return self._input("Bundle")

    @property
    def o_bundle(self) -> SocketLinker:
        """Output socket: Bundle"""
        return self._output("Bundle")


class MapRange(NodeBuilder):
    """Remap a value from a range to a target range"""

    name = "ShaderNodeMapRange"
    node: bpy.types.ShaderNodeMapRange

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 1.0,
        from_min: TYPE_INPUT_VALUE = 0.0,
        from_max: TYPE_INPUT_VALUE = 1.0,
        to_min: TYPE_INPUT_VALUE = 0.0,
        to_max: TYPE_INPUT_VALUE = 1.0,
        steps: TYPE_INPUT_VALUE = 4.0,
        vector: TYPE_INPUT_VECTOR = None,
        from_min_float3: TYPE_INPUT_VECTOR = None,
        from_max_float3: TYPE_INPUT_VECTOR = None,
        to_min_float3: TYPE_INPUT_VECTOR = None,
        to_max_float3: TYPE_INPUT_VECTOR = None,
        steps_float3: TYPE_INPUT_VECTOR = None,
        *,
        clamp: bool = False,
        interpolation_type: Literal[
            "LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"
        ] = "LINEAR",
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Value": value,
            "From Min": from_min,
            "From Max": from_max,
            "To Min": to_min,
            "To Max": to_max,
            "Steps": steps,
            "Vector": vector,
            "From_Min_FLOAT3": from_min_float3,
            "From_Max_FLOAT3": from_max_float3,
            "To_Min_FLOAT3": to_min_float3,
            "To_Max_FLOAT3": to_max_float3,
            "Steps_FLOAT3": steps_float3,
        }
        self.clamp = clamp
        self.interpolation_type = interpolation_type
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        value: TYPE_INPUT_VALUE = 1.0,
        from_min: TYPE_INPUT_VALUE = 0.0,
        from_max: TYPE_INPUT_VALUE = 1.0,
        to_min: TYPE_INPUT_VALUE = 0.0,
        to_max: TYPE_INPUT_VALUE = 1.0,
    ) -> "MapRange":
        """Create Map Range with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            value=value,
            from_min=from_min,
            from_max=from_max,
            to_min=to_min,
            to_max=to_max,
        )

    @classmethod
    def vector(
        cls,
        vector: TYPE_INPUT_VECTOR = None,
        from_min3: TYPE_INPUT_VECTOR = None,
        from_max3: TYPE_INPUT_VECTOR = None,
        to_min3: TYPE_INPUT_VECTOR = None,
        to_max3: TYPE_INPUT_VECTOR = None,
    ) -> "MapRange":
        """Create Map Range with operation 'Vector'."""
        return cls(
            data_type="FLOAT_VECTOR",
            vector=vector,
            from_min_float3=from_min3,
            from_max_float3=from_max3,
            to_min_float3=to_min3,
            to_max_float3=to_max3,
        )

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_from_min(self) -> SocketLinker:
        """Input socket: From Min"""
        return self._input("From Min")

    @property
    def i_from_max(self) -> SocketLinker:
        """Input socket: From Max"""
        return self._input("From Max")

    @property
    def i_to_min(self) -> SocketLinker:
        """Input socket: To Min"""
        return self._input("To Min")

    @property
    def i_to_max(self) -> SocketLinker:
        """Input socket: To Max"""
        return self._input("To Max")

    @property
    def i_steps(self) -> SocketLinker:
        """Input socket: Steps"""
        return self._input("Steps")

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_from_min_float3(self) -> SocketLinker:
        """Input socket: From Min"""
        return self._input("From_Min_FLOAT3")

    @property
    def i_from_max_float3(self) -> SocketLinker:
        """Input socket: From Max"""
        return self._input("From_Max_FLOAT3")

    @property
    def i_to_min_float3(self) -> SocketLinker:
        """Input socket: To Min"""
        return self._input("To_Min_FLOAT3")

    @property
    def i_to_max_float3(self) -> SocketLinker:
        """Input socket: To Max"""
        return self._input("To_Max_FLOAT3")

    @property
    def i_steps_float3(self) -> SocketLinker:
        """Input socket: Steps"""
        return self._input("Steps_FLOAT3")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

    @property
    def clamp(self) -> bool:
        return self.node.clamp

    @clamp.setter
    def clamp(self, value: bool):
        self.node.clamp = value

    @property
    def interpolation_type(
        self,
    ) -> Literal["LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"]:
        return self.node.interpolation_type

    @interpolation_type.setter
    def interpolation_type(
        self, value: Literal["LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"]
    ):
        self.node.interpolation_type = value

    @property
    def data_type(self) -> Literal["FLOAT", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "FLOAT_VECTOR"]):
        self.node.data_type = value


class MatchString(NodeBuilder):
    """Check if a given string exists within another string"""

    name = "FunctionNodeMatchString"
    node: bpy.types.FunctionNodeMatchString

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        operation: TYPE_INPUT_MENU = "Starts With",
        key: TYPE_INPUT_STRING = "",
    ):
        super().__init__()
        key_args = {"String": string, "Operation": operation, "Key": key}

        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def i_operation(self) -> SocketLinker:
        """Input socket: Operation"""
        return self._input("Operation")

    @property
    def i_key(self) -> SocketLinker:
        """Input socket: Key"""
        return self._input("Key")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")


class Math(NodeBuilder):
    """Perform math operations"""

    name = "ShaderNodeMath"
    node: bpy.types.ShaderNodeMath

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
        *,
        operation: Literal[
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVIDE",
            "MULTIPLY_ADD",
            "POWER",
            "LOGARITHM",
            "SQRT",
            "INVERSE_SQRT",
            "ABSOLUTE",
            "EXPONENT",
            "MINIMUM",
            "MAXIMUM",
            "LESS_THAN",
            "GREATER_THAN",
            "SIGN",
            "COMPARE",
            "SMOOTH_MIN",
            "SMOOTH_MAX",
            "ROUND",
            "FLOOR",
            "CEIL",
            "TRUNC",
            "FRACT",
            "MODULO",
            "FLOORED_MODULO",
            "WRAP",
            "SNAP",
            "PINGPONG",
            "SINE",
            "COSINE",
            "TANGENT",
            "ARCSINE",
            "ARCCOSINE",
            "ARCTANGENT",
            "ARCTAN2",
            "SINH",
            "COSH",
            "TANH",
            "RADIANS",
            "DEGREES",
        ] = "ADD",
        use_clamp: bool = False,
    ):
        super().__init__()
        key_args = {"Value": value, "Value_001": value_001, "Value_002": value_002}
        self.operation = operation
        self.use_clamp = use_clamp
        self._establish_links(**key_args)

    @classmethod
    def add(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Add'."""
        return cls(operation="ADD", value=value, value_001=value_001)

    @classmethod
    def subtract(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Subtract'."""
        return cls(operation="SUBTRACT", value=value, value_001=value_001)

    @classmethod
    def multiply(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Multiply'."""
        return cls(operation="MULTIPLY", value=value, value_001=value_001)

    @classmethod
    def divide(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Divide'."""
        return cls(operation="DIVIDE", value=value, value_001=value_001)

    @classmethod
    def power(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Power'."""
        return cls(operation="POWER", value=value, value_001=value_001)

    @classmethod
    def logarithm(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Logarithm'."""
        return cls(operation="LOGARITHM", value=value, value_001=value_001)

    @classmethod
    def absolute(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Absolute'."""
        return cls(operation="ABSOLUTE", value=value)

    @classmethod
    def exponent(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Exponent'."""
        return cls(operation="EXPONENT", value=value)

    @classmethod
    def minimum(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Minimum'."""
        return cls(operation="MINIMUM", value=value, value_001=value_001)

    @classmethod
    def maximum(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Maximum'."""
        return cls(operation="MAXIMUM", value=value, value_001=value_001)

    @classmethod
    def sign(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Sign'."""
        return cls(operation="SIGN", value=value)

    @classmethod
    def compare(
        cls,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
    ) -> "Math":
        """Create Math with operation 'Compare'."""
        return cls(
            operation="COMPARE", value=value, value_001=value_001, value_002=value_002
        )

    @classmethod
    def round(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Round'."""
        return cls(operation="ROUND", value=value)

    @classmethod
    def floor(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Floor'."""
        return cls(operation="FLOOR", value=value)

    @classmethod
    def ceil(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Ceil'."""
        return cls(operation="CEIL", value=value)

    @classmethod
    def truncate(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Truncate'."""
        return cls(operation="TRUNC", value=value)

    @classmethod
    def fraction(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Fraction'."""
        return cls(operation="FRACT", value=value)

    @classmethod
    def wrap(
        cls,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
    ) -> "Math":
        """Create Math with operation 'Wrap'."""
        return cls(
            operation="WRAP", value=value, value_001=value_001, value_002=value_002
        )

    @classmethod
    def snap(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Snap'."""
        return cls(operation="SNAP", value=value, value_001=value_001)

    @classmethod
    def sine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Sine'."""
        return cls(operation="SINE", value=value)

    @classmethod
    def cosine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Cosine'."""
        return cls(operation="COSINE", value=value)

    @classmethod
    def tangent(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Tangent'."""
        return cls(operation="TANGENT", value=value)

    @classmethod
    def arcsine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Arcsine'."""
        return cls(operation="ARCSINE", value=value)

    @classmethod
    def arccosine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Arccosine'."""
        return cls(operation="ARCCOSINE", value=value)

    @classmethod
    def arctangent(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Arctangent'."""
        return cls(operation="ARCTANGENT", value=value)

    @classmethod
    def arctan2(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Arctan2'."""
        return cls(operation="ARCTAN2", value=value, value_001=value_001)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_value_001(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value_001")

    @property
    def i_value_002(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value_002")

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
        "POWER",
        "LOGARITHM",
        "SQRT",
        "INVERSE_SQRT",
        "ABSOLUTE",
        "EXPONENT",
        "MINIMUM",
        "MAXIMUM",
        "LESS_THAN",
        "GREATER_THAN",
        "SIGN",
        "COMPARE",
        "SMOOTH_MIN",
        "SMOOTH_MAX",
        "ROUND",
        "FLOOR",
        "CEIL",
        "TRUNC",
        "FRACT",
        "MODULO",
        "FLOORED_MODULO",
        "WRAP",
        "SNAP",
        "PINGPONG",
        "SINE",
        "COSINE",
        "TANGENT",
        "ARCSINE",
        "ARCCOSINE",
        "ARCTANGENT",
        "ARCTAN2",
        "SINH",
        "COSH",
        "TANH",
        "RADIANS",
        "DEGREES",
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
            "POWER",
            "LOGARITHM",
            "SQRT",
            "INVERSE_SQRT",
            "ABSOLUTE",
            "EXPONENT",
            "MINIMUM",
            "MAXIMUM",
            "LESS_THAN",
            "GREATER_THAN",
            "SIGN",
            "COMPARE",
            "SMOOTH_MIN",
            "SMOOTH_MAX",
            "ROUND",
            "FLOOR",
            "CEIL",
            "TRUNC",
            "FRACT",
            "MODULO",
            "FLOORED_MODULO",
            "WRAP",
            "SNAP",
            "PINGPONG",
            "SINE",
            "COSINE",
            "TANGENT",
            "ARCSINE",
            "ARCCOSINE",
            "ARCTANGENT",
            "ARCTAN2",
            "SINH",
            "COSH",
            "TANH",
            "RADIANS",
            "DEGREES",
        ],
    ):
        self.node.operation = value

    @property
    def use_clamp(self) -> bool:
        return self.node.use_clamp

    @use_clamp.setter
    def use_clamp(self, value: bool):
        self.node.use_clamp = value


class MatrixDeterminant(NodeBuilder):
    """Compute the determinant of the given matrix"""

    name = "FunctionNodeMatrixDeterminant"
    node: bpy.types.FunctionNodeMatrixDeterminant

    def __init__(self, matrix: TYPE_INPUT_MATRIX = None):
        super().__init__()
        key_args = {"Matrix": matrix}

        self._establish_links(**key_args)

    @property
    def i_matrix(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix")

    @property
    def o_determinant(self) -> SocketLinker:
        """Output socket: Determinant"""
        return self._output("Determinant")


class Mix(NodeBuilder):
    """Mix values by a factor"""

    name = "ShaderNodeMix"
    node: bpy.types.ShaderNodeMix

    def __init__(
        self,
        factor_float: TYPE_INPUT_VALUE = 0.5,
        factor_vector: TYPE_INPUT_VECTOR = None,
        a_float: TYPE_INPUT_VALUE = 0.0,
        b_float: TYPE_INPUT_VALUE = 0.0,
        a_vector: TYPE_INPUT_VECTOR = None,
        b_vector: TYPE_INPUT_VECTOR = None,
        a_color: TYPE_INPUT_COLOR = None,
        b_color: TYPE_INPUT_COLOR = None,
        a_rotation: TYPE_INPUT_ROTATION = None,
        b_rotation: TYPE_INPUT_ROTATION = None,
        *,
        data_type: Literal["FLOAT", "VECTOR", "RGBA", "ROTATION"] = "FLOAT",
        factor_mode: Literal["UNIFORM", "NON_UNIFORM"] = "UNIFORM",
        blend_type: Literal[
            "MIX",
            "DARKEN",
            "MULTIPLY",
            "BURN",
            "LIGHTEN",
            "SCREEN",
            "DODGE",
            "ADD",
            "OVERLAY",
            "SOFT_LIGHT",
            "LINEAR_LIGHT",
            "DIFFERENCE",
            "EXCLUSION",
            "SUBTRACT",
            "DIVIDE",
            "HUE",
            "SATURATION",
            "COLOR",
            "VALUE",
        ] = "MIX",
        clamp_factor: bool = False,
        clamp_result: bool = False,
    ):
        super().__init__()
        key_args = {
            "Factor_Float": factor_float,
            "Factor_Vector": factor_vector,
            "A_Float": a_float,
            "B_Float": b_float,
            "A_Vector": a_vector,
            "B_Vector": b_vector,
            "A_Color": a_color,
            "B_Color": b_color,
            "A_Rotation": a_rotation,
            "B_Rotation": b_rotation,
        }
        self.data_type = data_type
        self.factor_mode = factor_mode
        self.blend_type = blend_type
        self.clamp_factor = clamp_factor
        self.clamp_result = clamp_result
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
    ) -> "Mix":
        """Create Mix with operation 'Float'."""
        return cls(data_type="FLOAT", factor_float=factor, a_float=a, b_float=b)

    @classmethod
    def vector(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a: TYPE_INPUT_VECTOR = None,
        b: TYPE_INPUT_VECTOR = None,
    ) -> "Mix":
        """Create Mix with operation 'Vector'."""
        return cls(data_type="VECTOR", factor_float=factor, a_vector=a, b_vector=b)

    @classmethod
    def color(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a_color: TYPE_INPUT_COLOR = None,
        b_color: TYPE_INPUT_COLOR = None,
    ) -> "Mix":
        """Create Mix with operation 'Color'."""
        return cls(
            data_type="RGBA", factor_float=factor, a_color=a_color, b_color=b_color
        )

    @classmethod
    def rotation(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a_rotation: TYPE_INPUT_ROTATION = None,
        b_rotation: TYPE_INPUT_ROTATION = None,
    ) -> "Mix":
        """Create Mix with operation 'Rotation'."""
        return cls(
            data_type="ROTATION",
            factor_float=factor,
            a_rotation=a_rotation,
            b_rotation=b_rotation,
        )

    @property
    def i_factor_float(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Factor_Float")

    @property
    def i_factor_vector(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Factor_Vector")

    @property
    def i_a_float(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_Float")

    @property
    def i_b_float(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_Float")

    @property
    def i_a_vector(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_Vector")

    @property
    def i_b_vector(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_Vector")

    @property
    def i_a_color(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_Color")

    @property
    def i_b_color(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_Color")

    @property
    def i_a_rotation(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A_Rotation")

    @property
    def i_b_rotation(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B_Rotation")

    @property
    def o_result_float(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result_Float")

    @property
    def o_result_vector(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result_Vector")

    @property
    def o_result_color(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result_Color")

    @property
    def o_result_rotation(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result_Rotation")

    @property
    def data_type(self) -> Literal["FLOAT", "VECTOR", "RGBA", "ROTATION"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "VECTOR", "RGBA", "ROTATION"]):
        self.node.data_type = value

    @property
    def factor_mode(self) -> Literal["UNIFORM", "NON_UNIFORM"]:
        return self.node.factor_mode

    @factor_mode.setter
    def factor_mode(self, value: Literal["UNIFORM", "NON_UNIFORM"]):
        self.node.factor_mode = value

    @property
    def blend_type(
        self,
    ) -> Literal[
        "MIX",
        "DARKEN",
        "MULTIPLY",
        "BURN",
        "LIGHTEN",
        "SCREEN",
        "DODGE",
        "ADD",
        "OVERLAY",
        "SOFT_LIGHT",
        "LINEAR_LIGHT",
        "DIFFERENCE",
        "EXCLUSION",
        "SUBTRACT",
        "DIVIDE",
        "HUE",
        "SATURATION",
        "COLOR",
        "VALUE",
    ]:
        return self.node.blend_type

    @blend_type.setter
    def blend_type(
        self,
        value: Literal[
            "MIX",
            "DARKEN",
            "MULTIPLY",
            "BURN",
            "LIGHTEN",
            "SCREEN",
            "DODGE",
            "ADD",
            "OVERLAY",
            "SOFT_LIGHT",
            "LINEAR_LIGHT",
            "DIFFERENCE",
            "EXCLUSION",
            "SUBTRACT",
            "DIVIDE",
            "HUE",
            "SATURATION",
            "COLOR",
            "VALUE",
        ],
    ):
        self.node.blend_type = value

    @property
    def clamp_factor(self) -> bool:
        return self.node.clamp_factor

    @clamp_factor.setter
    def clamp_factor(self, value: bool):
        self.node.clamp_factor = value

    @property
    def clamp_result(self) -> bool:
        return self.node.clamp_result

    @clamp_result.setter
    def clamp_result(self, value: bool):
        self.node.clamp_result = value


class MultiplyMatrices(NodeBuilder):
    """Perform a matrix multiplication on two input matrices"""

    name = "FunctionNodeMatrixMultiply"
    node: bpy.types.FunctionNodeMatrixMultiply

    def __init__(
        self,
        matrix: TYPE_INPUT_MATRIX = None,
        matrix_001: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {"Matrix": matrix, "Matrix_001": matrix_001}

        self._establish_links(**key_args)

    @property
    def i_matrix(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix")

    @property
    def i_matrix_001(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix_001")

    @property
    def o_matrix(self) -> SocketLinker:
        """Output socket: Matrix"""
        return self._output("Matrix")


class PackUVIslands(NodeBuilder):
    """Scale islands of a UV map and move them so they fill the UV space as much as possible"""

    name = "GeometryNodeUVPackIslands"
    node: bpy.types.GeometryNodeUVPackIslands

    def __init__(
        self,
        uv: TYPE_INPUT_VECTOR = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        margin: TYPE_INPUT_VALUE = 0.001,
        rotate: TYPE_INPUT_BOOLEAN = True,
        method: TYPE_INPUT_MENU = "Bounding Box",
    ):
        super().__init__()
        key_args = {
            "UV": uv,
            "Selection": selection,
            "Margin": margin,
            "Rotate": rotate,
            "Method": method,
        }

        self._establish_links(**key_args)

    @property
    def i_uv(self) -> SocketLinker:
        """Input socket: UV"""
        return self._input("UV")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_margin(self) -> SocketLinker:
        """Input socket: Margin"""
        return self._input("Margin")

    @property
    def i_rotate(self) -> SocketLinker:
        """Input socket: Rotate"""
        return self._input("Rotate")

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def o_uv(self) -> SocketLinker:
        """Output socket: UV"""
        return self._output("UV")


class ProjectPoint(NodeBuilder):
    """Project a point using a matrix, using location, rotation, scale, and perspective divide"""

    name = "FunctionNodeProjectPoint"
    node: bpy.types.FunctionNodeProjectPoint

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        transform: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {"Vector": vector, "Transform": transform}

        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")


class QuaternionToRotation(NodeBuilder):
    """Build a rotation from quaternion components"""

    name = "FunctionNodeQuaternionToRotation"
    node: bpy.types.FunctionNodeQuaternionToRotation

    def __init__(
        self,
        w: TYPE_INPUT_VALUE = 1.0,
        x: TYPE_INPUT_VALUE = 0.0,
        y: TYPE_INPUT_VALUE = 0.0,
        z: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {"W": w, "X": x, "Y": y, "Z": z}

        self._establish_links(**key_args)

    @property
    def i_w(self) -> SocketLinker:
        """Input socket: W"""
        return self._input("W")

    @property
    def i_x(self) -> SocketLinker:
        """Input socket: X"""
        return self._input("X")

    @property
    def i_y(self) -> SocketLinker:
        """Input socket: Y"""
        return self._input("Y")

    @property
    def i_z(self) -> SocketLinker:
        """Input socket: Z"""
        return self._input("Z")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class RgbCurves(NodeBuilder):
    """Apply color corrections for each color channel"""

    name = "ShaderNodeRGBCurve"
    node: bpy.types.ShaderNodeRGBCurve

    def __init__(
        self,
        fac: TYPE_INPUT_VALUE = 1.0,
        color: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {"Fac": fac, "Color": color}

        self._establish_links(**key_args)

    @property
    def i_fac(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Fac")

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")


class RandomValue(NodeBuilder):
    """Output a randomized value"""

    name = "FunctionNodeRandomValue"
    node: bpy.types.FunctionNodeRandomValue

    def __init__(
        self,
        min: TYPE_INPUT_VECTOR = None,
        max: TYPE_INPUT_VECTOR = None,
        min_001: TYPE_INPUT_VALUE = 0.0,
        max_001: TYPE_INPUT_VALUE = 1.0,
        min_002: TYPE_INPUT_INT = 0,
        max_002: TYPE_INPUT_INT = 100,
        probability: TYPE_INPUT_VALUE = 0.5,
        id: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Min": min,
            "Max": max,
            "Min_001": min_001,
            "Max_001": max_001,
            "Min_002": min_002,
            "Max_002": max_002,
            "Probability": probability,
            "ID": id,
            "Seed": seed,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        min: TYPE_INPUT_VALUE = 0.0,
        max: TYPE_INPUT_VALUE = 1.0,
        id: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
    ) -> "RandomValue":
        """Create Random Value with operation 'Float'."""
        return cls(data_type="FLOAT", min_001=min, max_001=max, id=id, seed=seed)

    @classmethod
    def integer(
        cls,
        min: TYPE_INPUT_INT = 0,
        max: TYPE_INPUT_INT = 100,
        id: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
    ) -> "RandomValue":
        """Create Random Value with operation 'Integer'."""
        return cls(data_type="INT", min_002=min, max_002=max, id=id, seed=seed)

    @classmethod
    def boolean(
        cls,
        probability: TYPE_INPUT_VALUE = 0.5,
        id: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
    ) -> "RandomValue":
        """Create Random Value with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", probability=probability, id=id, seed=seed)

    @classmethod
    def vector(
        cls,
        min: TYPE_INPUT_VECTOR = None,
        max: TYPE_INPUT_VECTOR = None,
        id: TYPE_INPUT_INT = 0,
        seed: TYPE_INPUT_INT = 0,
    ) -> "RandomValue":
        """Create Random Value with operation 'Vector'."""
        return cls(data_type="FLOAT_VECTOR", min=min, max=max, id=id, seed=seed)

    @property
    def i_min(self) -> SocketLinker:
        """Input socket: Min"""
        return self._input("Min")

    @property
    def i_max(self) -> SocketLinker:
        """Input socket: Max"""
        return self._input("Max")

    @property
    def i_min_001(self) -> SocketLinker:
        """Input socket: Min"""
        return self._input("Min_001")

    @property
    def i_max_001(self) -> SocketLinker:
        """Input socket: Max"""
        return self._input("Max_001")

    @property
    def i_min_002(self) -> SocketLinker:
        """Input socket: Min"""
        return self._input("Min_002")

    @property
    def i_max_002(self) -> SocketLinker:
        """Input socket: Max"""
        return self._input("Max_002")

    @property
    def i_probability(self) -> SocketLinker:
        """Input socket: Probability"""
        return self._input("Probability")

    @property
    def i_id(self) -> SocketLinker:
        """Input socket: ID"""
        return self._input("ID")

    @property
    def i_seed(self) -> SocketLinker:
        """Input socket: Seed"""
        return self._input("Seed")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_value_001(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value_001")

    @property
    def o_value_002(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value_002")

    @property
    def o_value_003(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value_003")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "FLOAT_VECTOR"]):
        self.node.data_type = value


class ReplaceString(NodeBuilder):
    """Replace a given string segment with another"""

    name = "FunctionNodeReplaceString"
    node: bpy.types.FunctionNodeReplaceString

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        find: TYPE_INPUT_STRING = "",
        replace: TYPE_INPUT_STRING = "",
    ):
        super().__init__()
        key_args = {"String": string, "Find": find, "Replace": replace}

        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def i_find(self) -> SocketLinker:
        """Input socket: Find"""
        return self._input("Find")

    @property
    def i_replace(self) -> SocketLinker:
        """Input socket: Replace"""
        return self._input("Replace")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class RotateEuler(NodeBuilder):
    """Apply a secondary Euler rotation to a given Euler rotation"""

    name = "FunctionNodeRotateEuler"
    node: bpy.types.FunctionNodeRotateEuler

    def __init__(
        self,
        rotation: TYPE_INPUT_VECTOR = None,
        rotate_by: TYPE_INPUT_VECTOR = None,
        axis: TYPE_INPUT_VECTOR = None,
        angle: TYPE_INPUT_VALUE = 0.0,
        *,
        rotation_type: Literal["AXIS_ANGLE", "EULER"] = "EULER",
        space: Literal["OBJECT", "LOCAL"] = "OBJECT",
    ):
        super().__init__()
        key_args = {
            "Rotation": rotation,
            "Rotate By": rotate_by,
            "Axis": axis,
            "Angle": angle,
        }
        self.rotation_type = rotation_type
        self.space = space
        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_rotate_by(self) -> SocketLinker:
        """Input socket: Rotate By"""
        return self._input("Rotate By")

    @property
    def i_axis(self) -> SocketLinker:
        """Input socket: Axis"""
        return self._input("Axis")

    @property
    def i_angle(self) -> SocketLinker:
        """Input socket: Angle"""
        return self._input("Angle")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def rotation_type(self) -> Literal["AXIS_ANGLE", "EULER"]:
        return self.node.rotation_type

    @rotation_type.setter
    def rotation_type(self, value: Literal["AXIS_ANGLE", "EULER"]):
        self.node.rotation_type = value

    @property
    def space(self) -> Literal["OBJECT", "LOCAL"]:
        return self.node.space

    @space.setter
    def space(self, value: Literal["OBJECT", "LOCAL"]):
        self.node.space = value


class RotateRotation(NodeBuilder):
    """Apply a secondary rotation to a given rotation value"""

    name = "FunctionNodeRotateRotation"
    node: bpy.types.FunctionNodeRotateRotation

    def __init__(
        self,
        rotation: TYPE_INPUT_ROTATION = None,
        rotate_by: TYPE_INPUT_ROTATION = None,
        *,
        rotation_space: Literal["GLOBAL", "LOCAL"] = "GLOBAL",
    ):
        super().__init__()
        key_args = {"Rotation": rotation, "Rotate By": rotate_by}
        self.rotation_space = rotation_space
        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_rotate_by(self) -> SocketLinker:
        """Input socket: Rotate By"""
        return self._input("Rotate By")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def rotation_space(self) -> Literal["GLOBAL", "LOCAL"]:
        return self.node.rotation_space

    @rotation_space.setter
    def rotation_space(self, value: Literal["GLOBAL", "LOCAL"]):
        self.node.rotation_space = value


class RotateVector(NodeBuilder):
    """Apply a rotation to a given vector"""

    name = "FunctionNodeRotateVector"
    node: bpy.types.FunctionNodeRotateVector

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_ROTATION = None,
    ):
        super().__init__()
        key_args = {"Vector": vector, "Rotation": rotation}

        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")


class RotationToAxisAngle(NodeBuilder):
    """Convert a rotation to axis angle components"""

    name = "FunctionNodeRotationToAxisAngle"
    node: bpy.types.FunctionNodeRotationToAxisAngle

    def __init__(self, rotation: TYPE_INPUT_ROTATION = None):
        super().__init__()
        key_args = {"Rotation": rotation}

        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_axis(self) -> SocketLinker:
        """Output socket: Axis"""
        return self._output("Axis")

    @property
    def o_angle(self) -> SocketLinker:
        """Output socket: Angle"""
        return self._output("Angle")


class RotationToEuler(NodeBuilder):
    """Convert a standard rotation value to an Euler rotation"""

    name = "FunctionNodeRotationToEuler"
    node: bpy.types.FunctionNodeRotationToEuler

    def __init__(self, rotation: TYPE_INPUT_ROTATION = None):
        super().__init__()
        key_args = {"Rotation": rotation}

        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_euler(self) -> SocketLinker:
        """Output socket: Euler"""
        return self._output("Euler")


class RotationToQuaternion(NodeBuilder):
    """Retrieve the quaternion components representing a rotation"""

    name = "FunctionNodeRotationToQuaternion"
    node: bpy.types.FunctionNodeRotationToQuaternion

    def __init__(self, rotation: TYPE_INPUT_ROTATION = None):
        super().__init__()
        key_args = {"Rotation": rotation}

        self._establish_links(**key_args)

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_w(self) -> SocketLinker:
        """Output socket: W"""
        return self._output("W")

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


class SeparateBundle(NodeBuilder):
    """Split a bundle into multiple sockets."""

    name = "NodeSeparateBundle"
    node: bpy.types.Node

    def __init__(
        self,
        bundle: TYPE_INPUT_BUNDLE = None,
        *,
        define_signature: bool = False,
    ):
        super().__init__()
        key_args = {"Bundle": bundle}
        self.define_signature = define_signature
        self._establish_links(**key_args)

    @property
    def i_bundle(self) -> SocketLinker:
        """Input socket: Bundle"""
        return self._input("Bundle")

    @property
    def define_signature(self) -> bool:
        return self.node.define_signature

    @define_signature.setter
    def define_signature(self, value: bool):
        self.node.define_signature = value


class SeparateColor(NodeBuilder):
    """Split a color into separate channels, based on a particular color model"""

    name = "FunctionNodeSeparateColor"
    node: bpy.types.FunctionNodeSeparateColor

    def __init__(
        self,
        color: TYPE_INPUT_COLOR = None,
        *,
        mode: Literal["RGB", "HSV", "HSL"] = "RGB",
    ):
        super().__init__()
        key_args = {"Color": color}
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def o_red(self) -> SocketLinker:
        """Output socket: Red"""
        return self._output("Red")

    @property
    def o_green(self) -> SocketLinker:
        """Output socket: Green"""
        return self._output("Green")

    @property
    def o_blue(self) -> SocketLinker:
        """Output socket: Blue"""
        return self._output("Blue")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")

    @property
    def mode(self) -> Literal["RGB", "HSV", "HSL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["RGB", "HSV", "HSL"]):
        self.node.mode = value


class SeparateMatrix(NodeBuilder):
    """Split a 4x4 matrix into its individual values"""

    name = "FunctionNodeSeparateMatrix"
    node: bpy.types.FunctionNodeSeparateMatrix

    def __init__(self, matrix: TYPE_INPUT_MATRIX = None):
        super().__init__()
        key_args = {"Matrix": matrix}

        self._establish_links(**key_args)

    @property
    def i_matrix(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix")

    @property
    def o_column_1_row_1(self) -> SocketLinker:
        """Output socket: Column 1 Row 1"""
        return self._output("Column 1 Row 1")

    @property
    def o_column_1_row_2(self) -> SocketLinker:
        """Output socket: Column 1 Row 2"""
        return self._output("Column 1 Row 2")

    @property
    def o_column_1_row_3(self) -> SocketLinker:
        """Output socket: Column 1 Row 3"""
        return self._output("Column 1 Row 3")

    @property
    def o_column_1_row_4(self) -> SocketLinker:
        """Output socket: Column 1 Row 4"""
        return self._output("Column 1 Row 4")

    @property
    def o_column_2_row_1(self) -> SocketLinker:
        """Output socket: Column 2 Row 1"""
        return self._output("Column 2 Row 1")

    @property
    def o_column_2_row_2(self) -> SocketLinker:
        """Output socket: Column 2 Row 2"""
        return self._output("Column 2 Row 2")

    @property
    def o_column_2_row_3(self) -> SocketLinker:
        """Output socket: Column 2 Row 3"""
        return self._output("Column 2 Row 3")

    @property
    def o_column_2_row_4(self) -> SocketLinker:
        """Output socket: Column 2 Row 4"""
        return self._output("Column 2 Row 4")

    @property
    def o_column_3_row_1(self) -> SocketLinker:
        """Output socket: Column 3 Row 1"""
        return self._output("Column 3 Row 1")

    @property
    def o_column_3_row_2(self) -> SocketLinker:
        """Output socket: Column 3 Row 2"""
        return self._output("Column 3 Row 2")

    @property
    def o_column_3_row_3(self) -> SocketLinker:
        """Output socket: Column 3 Row 3"""
        return self._output("Column 3 Row 3")

    @property
    def o_column_3_row_4(self) -> SocketLinker:
        """Output socket: Column 3 Row 4"""
        return self._output("Column 3 Row 4")

    @property
    def o_column_4_row_1(self) -> SocketLinker:
        """Output socket: Column 4 Row 1"""
        return self._output("Column 4 Row 1")

    @property
    def o_column_4_row_2(self) -> SocketLinker:
        """Output socket: Column 4 Row 2"""
        return self._output("Column 4 Row 2")

    @property
    def o_column_4_row_3(self) -> SocketLinker:
        """Output socket: Column 4 Row 3"""
        return self._output("Column 4 Row 3")

    @property
    def o_column_4_row_4(self) -> SocketLinker:
        """Output socket: Column 4 Row 4"""
        return self._output("Column 4 Row 4")


class SeparateTransform(NodeBuilder):
    """Split a transformation matrix into a translation vector, a rotation, and a scale vector"""

    name = "FunctionNodeSeparateTransform"
    node: bpy.types.FunctionNodeSeparateTransform

    def __init__(self, transform: TYPE_INPUT_MATRIX = None):
        super().__init__()
        key_args = {"Transform": transform}

        self._establish_links(**key_args)

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_translation(self) -> SocketLinker:
        """Output socket: Translation"""
        return self._output("Translation")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def o_scale(self) -> SocketLinker:
        """Output socket: Scale"""
        return self._output("Scale")


class SeparateXYZ(NodeBuilder):
    """Split a vector into its X, Y, and Z components"""

    name = "ShaderNodeSeparateXYZ"
    node: bpy.types.ShaderNodeSeparateXYZ

    def __init__(self, vector: TYPE_INPUT_VECTOR = None):
        super().__init__()
        key_args = {"Vector": vector}

        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

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


class SliceString(NodeBuilder):
    """Extract a string segment from a larger string"""

    name = "FunctionNodeSliceString"
    node: bpy.types.FunctionNodeSliceString

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        position: TYPE_INPUT_INT = 0,
        length: TYPE_INPUT_INT = 10,
    ):
        super().__init__()
        key_args = {"String": string, "Position": position, "Length": length}

        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_length(self) -> SocketLinker:
        """Input socket: Length"""
        return self._input("Length")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class StringLength(NodeBuilder):
    """Output the number of characters in the given string"""

    name = "FunctionNodeStringLength"
    node: bpy.types.FunctionNodeStringLength

    def __init__(self, string: TYPE_INPUT_STRING = ""):
        super().__init__()
        key_args = {"String": string}

        self._establish_links(**key_args)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")


class StringToValue(NodeBuilder):
    """Derive a numeric value from a given string representation"""

    name = "FunctionNodeStringToValue"
    node: bpy.types.FunctionNodeStringToValue

    def __init__(
        self,
        string: TYPE_INPUT_STRING = "",
        *,
        data_type: Literal["FLOAT", "INT"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"String": string}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, string: TYPE_INPUT_STRING = "") -> "StringToValue":
        """Create String to Value with operation 'Float'."""
        return cls(data_type="FLOAT", string=string)

    @classmethod
    def integer(cls, string: TYPE_INPUT_STRING = "") -> "StringToValue":
        """Create String to Value with operation 'Integer'."""
        return cls(data_type="INT", string=string)

    @property
    def i_string(self) -> SocketLinker:
        """Input socket: String"""
        return self._input("String")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def data_type(self) -> Literal["FLOAT", "INT"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT"]):
        self.node.data_type = value


class Switch(NodeBuilder):
    """Switch between two inputs"""

    name = "GeometryNodeSwitch"
    node: bpy.types.GeometryNodeSwitch

    def __init__(
        self,
        switch: TYPE_INPUT_BOOLEAN = False,
        false: TYPE_INPUT_GEOMETRY = None,
        true: TYPE_INPUT_GEOMETRY = None,
        *,
        input_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "GEOMETRY",
    ):
        super().__init__()
        key_args = {"Switch": switch, "False": false, "True": true}
        self.input_type = input_type
        self._establish_links(**key_args)

    @property
    def i_switch(self) -> SocketLinker:
        """Input socket: Switch"""
        return self._input("Switch")

    @property
    def i_false(self) -> SocketLinker:
        """Input socket: False"""
        return self._input("False")

    @property
    def i_true(self) -> SocketLinker:
        """Input socket: True"""
        return self._input("True")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def input_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.input_type

    @input_type.setter
    def input_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.input_type = value


class TransformDirection(NodeBuilder):
    """Apply a transformation matrix (excluding translation) to the given vector"""

    name = "FunctionNodeTransformDirection"
    node: bpy.types.FunctionNodeTransformDirection

    def __init__(
        self,
        direction: TYPE_INPUT_VECTOR = None,
        transform: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {"Direction": direction, "Transform": transform}

        self._establish_links(**key_args)

    @property
    def i_direction(self) -> SocketLinker:
        """Input socket: Direction"""
        return self._input("Direction")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_direction(self) -> SocketLinker:
        """Output socket: Direction"""
        return self._output("Direction")


class TransformPoint(NodeBuilder):
    """Apply a transformation matrix to the given vector"""

    name = "FunctionNodeTransformPoint"
    node: bpy.types.FunctionNodeTransformPoint

    def __init__(
        self,
        vector: TYPE_INPUT_VECTOR = None,
        transform: TYPE_INPUT_MATRIX = None,
    ):
        super().__init__()
        key_args = {"Vector": vector, "Transform": transform}

        self._establish_links(**key_args)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")


class TransposeMatrix(NodeBuilder):
    """Flip a matrix over its diagonal, turning columns into rows and vice-versa"""

    name = "FunctionNodeTransposeMatrix"
    node: bpy.types.FunctionNodeTransposeMatrix

    def __init__(self, matrix: TYPE_INPUT_MATRIX = None):
        super().__init__()
        key_args = {"Matrix": matrix}

        self._establish_links(**key_args)

    @property
    def i_matrix(self) -> SocketLinker:
        """Input socket: Matrix"""
        return self._input("Matrix")

    @property
    def o_matrix(self) -> SocketLinker:
        """Output socket: Matrix"""
        return self._output("Matrix")


class UVUnwrap(NodeBuilder):
    """Generate a UV map based on seam edges"""

    name = "GeometryNodeUVUnwrap"
    node: bpy.types.GeometryNodeUVUnwrap

    def __init__(
        self,
        selection: TYPE_INPUT_BOOLEAN = True,
        seam: TYPE_INPUT_BOOLEAN = False,
        margin: TYPE_INPUT_VALUE = 0.001,
        fill_holes: TYPE_INPUT_BOOLEAN = True,
        method: TYPE_INPUT_MENU = "Angle Based",
    ):
        super().__init__()
        key_args = {
            "Selection": selection,
            "Seam": seam,
            "Margin": margin,
            "Fill Holes": fill_holes,
            "Method": method,
        }

        self._establish_links(**key_args)

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_seam(self) -> SocketLinker:
        """Input socket: Seam"""
        return self._input("Seam")

    @property
    def i_margin(self) -> SocketLinker:
        """Input socket: Margin"""
        return self._input("Margin")

    @property
    def i_fill_holes(self) -> SocketLinker:
        """Input socket: Fill Holes"""
        return self._input("Fill Holes")

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def o_uv(self) -> SocketLinker:
        """Output socket: UV"""
        return self._output("UV")


class ValueToString(NodeBuilder):
    """Generate a string representation of the given input value"""

    name = "FunctionNodeValueToString"
    node: bpy.types.FunctionNodeValueToString

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        decimals: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value, "Decimals": decimals}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, value: TYPE_INPUT_VALUE = 0.0, decimals: TYPE_INPUT_INT = 0
    ) -> "ValueToString":
        """Create Value to String with operation 'Float'."""
        return cls(data_type="FLOAT", value=value, decimals=decimals)

    @classmethod
    def integer(cls, value: TYPE_INPUT_INT = 0) -> "ValueToString":
        """Create Value to String with operation 'Integer'."""
        return cls(data_type="INT", value=value)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_decimals(self) -> SocketLinker:
        """Input socket: Decimals"""
        return self._input("Decimals")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")

    @property
    def data_type(self) -> Literal["FLOAT", "INT"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT"]):
        self.node.data_type = value
