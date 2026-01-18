from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from . import types
from .types import (
    LINKABLE,
    SOCKET_TYPES,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_INT,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    _AccumulateFieldDataTypes,
    _AttributeDomains,
    _EvaluateAtIndexDataTypes,
    _MixColorBlendTypes,
    _MixDataTypes,
    _RandomValueDataTypes,
    _VectorMathOperations,
)


class AlignRotationToVector(NodeBuilder):
    """Orient a rotation along the given direction"""

    name = "FunctionNodeAlignRotationToVector"
    node: bpy.types.FunctionNodeAlignRotationToVector

    def __init__(
        self,
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        factor: TYPE_INPUT_VALUE = 1.0,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 1.0),
        axis: Literal["X", "Y", "Z"] = "Z",
        pivot_axis: Literal["AUTO", "X", "Y", "Z"] = "AUTO",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Rotation": rotation, "Factor": factor, "Vector": vector}
        key_args.update(kwargs)
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
        primary_axis_vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 1.0),
        secondary_axis_vector: TYPE_INPUT_VECTOR = (1.0, 0.0, 0.0),
        primary_axis: Literal["X", "Y", "Z"] = "Z",
        secondary_axis: Literal["X", "Y", "Z"] = "X",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Primary Axis": primary_axis_vector,
            "Secondary Axis": secondary_axis_vector,
        }
        key_args.update(kwargs)
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
    def primary_axis(self) -> Literal["X", "Y", "Z"]:
        return self.node.primary_axis

    @primary_axis.setter
    def primary_axis(self, value: Literal["X", "Y", "Z"]):
        self.node.primary_axis = value

    @property
    def secondary_axis(self) -> Literal["X", "Y", "Z"]:
        return self.node.secondary_axis

    @secondary_axis.setter
    def secondary_axis(self, value: Literal["X", "Y", "Z"]):
        self.node.secondary_axis = value


class AxisAngleToRotation(NodeBuilder):
    """Build a rotation from an axis and a rotation around that axis"""

    name = "FunctionNodeAxisAngleToRotation"
    node: bpy.types.FunctionNodeAxisAngleToRotation

    def __init__(
        self,
        axis: TYPE_INPUT_VECTOR = (0.0, 0.0, 1.0),
        angle: TYPE_INPUT_VALUE = 0.0,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Axis": axis, "Angle": angle}
        key_args.update(kwargs)

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
        operation: Literal["AND", "OR", "XOR", "NOT", "SHIFT", "ROTATE"] = "AND",
        **kwargs,
    ):
        super().__init__()
        key_args = {"A": a, "B": b}
        key_args.update(kwargs)
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def l_and(cls, a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'And'."""
        return cls(operation="AND", A=a, B=b)

    @classmethod
    def l_or(cls, a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Or'."""
        return cls(operation="OR", A=a, B=b)

    @classmethod
    def l_exclusive_or(cls, a: TYPE_INPUT_INT = 0, b: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'XOR'."""
        return cls(operation="XOR", A=a, B=b)

    @classmethod
    def l_not(cls, a: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Not'."""
        return cls(operation="NOT", A=a)

    @classmethod
    def shift(cls, a: TYPE_INPUT_INT = 0, shift: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Shift'."""
        return cls(operation="SHIFT", A=a, B=shift)

    @classmethod
    def rotate(cls, a: TYPE_INPUT_INT = 0, shift: TYPE_INPUT_INT = 0) -> "BitMath":
        """Create Bit Math with operation 'Rotate'."""
        return cls(operation="ROTATE", A=a, B=shift)

    @property
    def i_a(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("A")

    @property
    def i_b(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("B")

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
        mode: Literal["RGB", "HSV", "HSL"] = "RGB",
    ):
        super().__init__()
        key_args = {"Red": red, "Green": green, "Blue": blue, "Alpha": alpha}
        self.mode = mode
        self._establish_links(**key_args)

    @classmethod
    def rgb(
        cls,
        red: TYPE_INPUT_VALUE = 0.0,
        green: TYPE_INPUT_VALUE = 0.0,
        blue: TYPE_INPUT_VALUE = 0.0,
        alpha: TYPE_INPUT_VALUE = 1.0,
    ):
        return cls(red=red, green=green, blue=blue, alpha=alpha, mode="RGB")

    @classmethod
    def hsv(
        cls,
        hue: TYPE_INPUT_VALUE = 0.0,
        saturation: TYPE_INPUT_VALUE = 0.0,
        value: TYPE_INPUT_VALUE = 0.0,
        alpha: TYPE_INPUT_VALUE = 1.0,
    ):
        return cls(red=hue, green=saturation, blue=value, alpha=alpha, mode="HSV")

    @classmethod
    def hsl(
        cls,
        hue: TYPE_INPUT_VALUE = 0.0,
        saturation: TYPE_INPUT_VALUE = 0.0,
        lightness: TYPE_INPUT_VALUE = 0.0,
        alpha: TYPE_INPUT_VALUE = 1.0,
    ):
        return cls(red=hue, green=saturation, blue=lightness, alpha=alpha, mode="HSL")

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
        **kwargs,
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
        key_args.update(kwargs)

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
        translation: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        scale: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
        **kwargs,
    ):
        super().__init__()
        key_args = {"Translation": translation, "Rotation": rotation, "Scale": scale}
        key_args.update(kwargs)

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


_CompareOperations = Literal[
    "LESS_THAN",
    "LESS_EQUAL",
    "GREATER_THAN",
    "GREATER_EQUAL",
    "EQUAL",
    "NOT_EQUAL",
    "BRIGHTER",
    "DARKER",
]

_CompareDataTypes = Literal[
    "FLOAT",
    "INT",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "STRING",
]

_CompareVectorModes = Literal[
    "ELEMENT", "LENGTH", "AVERAGE", "DOT_PRODUCT", "DIRECTION"
]


class Compare(NodeBuilder):
    """Perform a comparison operation on the two given inputs"""

    name = "FunctionNodeCompare"
    node: bpy.types.FunctionNodeCompare

    def __init__(
        self,
        operation: _CompareOperations = "GREATER_THAN",
        data_type: _CompareDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        self.operation = operation
        self.data_type = data_type
        if self.data_type == "VECTOR":
            self.mode = kwargs["mode"]
        self._establish_links(**kwargs)

    @classmethod
    def float(
        cls,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        operation: _CompareOperations = "LESS_THAN",
        *,
        epsilon: TYPE_INPUT_VALUE = 0.0001,
    ):
        kwargs = {"operation": operation, "data_type": "FLOAT", "A": a, "B": b}
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon
        return cls(**kwargs)

    @classmethod
    def integer(
        cls,
        a: TYPE_INPUT_INT = 0,
        b: TYPE_INPUT_INT = 0,
        operation: _CompareOperations = "LESS_THAN",
    ) -> "Compare":
        return cls(operation=operation, data_type="INT", A_INT=a, B_INT=b)

    @classmethod
    def vector(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        operation: _CompareOperations = "LESS_THAN",
        *,
        mode: _CompareVectorModes = "ELEMENT",
        c: TYPE_INPUT_VALUE = None,
        angle: TYPE_INPUT_VALUE = None,
        epsilon: TYPE_INPUT_VALUE = None,
    ) -> "Compare":
        kwargs = {
            "operation": operation,
            "data_type": "VECTOR",
            "mode": mode,
            "A_VEC3": a,
            "B_VEC3": b,
        }
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon

        match mode:
            case "DIRECTION":
                kwargs["Angle"] = angle
            case "DOT_PRODUCT":
                kwargs["C"] = c
            case _:
                pass

        return cls(**kwargs)

    @classmethod
    def color(
        cls,
        a: TYPE_INPUT_COLOR = None,
        b: TYPE_INPUT_COLOR = None,
        operation: _CompareOperations = "EQUAL",
        *,
        epsilon: TYPE_INPUT_VALUE = None,
    ) -> "Compare":
        """Create Compare with operation 'Color'."""
        kwargs = {
            "operation": operation,
            "data_type": "RGBA",
            "A_COL": a,
            "B_COL": b,
        }
        if operation in ("EQUAL", "NOT_EQUAL"):
            kwargs["Epsilon"] = epsilon
        return cls(**kwargs)

    @classmethod
    def string(
        cls,
        a,
        b,
    ) -> "Compare":
        """Create Compare with operation 'String'."""
        return cls(mode="STRING", A_STR=a, B_STR=b)

    def _suffix(self) -> str:
        suffix_lookup = {
            "FLOAT": "",
            "INT": "_INT",
            "VECTOR": "_VEC",
            "RGBA": "_COL",
            "STRING": "_STR",
        }
        return suffix_lookup[self.data_type]

    @property
    def i_a(self) -> SocketLinker:
        """Input socket: A"""
        return self._input(f"A{self._suffix()}")

    @property
    def i_b(self) -> SocketLinker:
        """Input socket: B"""
        return self._input(f"B{self._suffix()}")

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return self._output("Result")

    @property
    def operation(
        self,
    ) -> _CompareOperations:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: _CompareOperations,
    ):
        self.node.operation = value

    @property
    def data_type(
        self,
    ) -> _CompareDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _CompareDataTypes,
    ):
        self.node.data_type = value

    @property
    def mode(
        self,
    ) -> _CompareVectorModes:
        return self.node.mode

    @mode.setter
    def mode(
        self,
        value: _CompareVectorModes,
    ):
        self.node.mode = value


class EulerToRotation(NodeBuilder):
    """Build a rotation from separate angles around each axis"""

    name = "FunctionNodeEulerToRotation"
    node: bpy.types.FunctionNodeEulerToRotation

    def __init__(self, euler: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0)):
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


class FloatToInteger(NodeBuilder):
    """Convert the given floating-point number to an integer, with a choice of methods"""

    name = "FunctionNodeFloatToInt"
    node: bpy.types.FunctionNodeFloatToInt

    def __init__(
        self,
        float: TYPE_INPUT_VALUE = 0.0,
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


class FormatString(NodeBuilder):
    """Insert values into a string using a Python and path template compatible formatting syntax"""

    name = "FunctionNodeFormatString"
    node: bpy.types.FunctionNodeFormatString
    _socket_data_types = ("VALUE", "INT", "STRING")

    def __init__(
        self,
        *args,
        format: TYPE_INPUT_STRING = "",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Format": format}
        key_args.update(self._add_inputs(*args, **kwargs))  # type: ignore
        self._establish_links(**key_args)

    def _add_socket(  # type: ignore
        self,
        name: str,
        type: Literal["FLOAT", "INT", "STRING"] = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.format_items.new(socket_type=type, name=name)
        if default_value is not None:
            try:
                self.node.inputs[item.name].default_value = default_value  # type: ignore
            except TypeError as e:
                raise ValueError(
                    f"Invalid default value for {type}: {default_value}"
                ) from e
        return self.node.inputs[item.name]

    @property
    def i_format(self) -> SocketLinker:
        """Input socket: Format"""
        return self._input("Format")

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def items(self) -> dict[str, SocketLinker]:
        """Input sockets:"""
        return {socket.name: self._input(socket.name) for socket in self.node.inputs}

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


_HashValueDataTypes = Literal[
    "FLOAT",
    "INT",
    "VECTOR",
    "RGBA",
    "ROTATION",
    "MATRIX",
    "STRING",
]


class HashValue(NodeBuilder):
    """Generate a randomized integer using the given input value as a seed"""

    name = "FunctionNodeHashValue"
    node: bpy.types.FunctionNodeHashValue

    def __init__(
        self,
        value: TYPE_INPUT_VALUE
        | TYPE_INPUT_INT
        | TYPE_INPUT_VECTOR
        | TYPE_INPUT_STRING
        | TYPE_INPUT_COLOR
        | TYPE_INPUT_ROTATION
        | TYPE_INPUT_MATRIX
        | TYPE_INPUT_STRING = None,
        seed: TYPE_INPUT_INT = 0,
        *,
        data_type: _HashValueDataTypes = "INT",
    ):
        super().__init__()
        key_args = {"Value": value, "Seed": seed}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, value: TYPE_INPUT_VALUE = None, seed: TYPE_INPUT_INT = 0):
        return cls(value, seed, "FLOAT")

    @classmethod
    def integer(cls, value: TYPE_INPUT_INT = None, seed: TYPE_INPUT_INT = 0):
        return cls(value, seed, "INT")

    @classmethod
    def vector(cls, value: TYPE_INPUT_VECTOR = None, seed: TYPE_INPUT_INT = 0):
        return cls(value, seed, "VECTOR")

    @classmethod
    def string(cls, value: TYPE_INPUT_STRING = None, seed: TYPE_INPUT_INT = 0):
        return cls(value, seed, "STRING")

    @classmethod
    def color(cls, value: TYPE_INPUT_COLOR = None, seed: TYPE_INPUT_INT = 0):
        return cls(value, seed, "RGBA")

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
    ) -> _HashValueDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _HashValueDataTypes,
    ):
        self.node.data_type = value


class Math(NodeBuilder):
    """Perform math operations"""

    name = "ShaderNodeMath"
    node: bpy.types.ShaderNodeMath  # type: ignore

    def __init__(
        self,
        operation: types.NodeMathItems = "ADD",
        use_clamp: bool = False,
        **kwargs,
    ):
        super().__init__()
        self.operation = operation
        self.use_clamp = use_clamp
        self._establish_links(**kwargs)

    @property
    def operation(self) -> types.NodeMathItems:
        return self.node.operation

    @operation.setter
    def operation(self, value: types.NodeMathItems):
        self.node.operation = value

    @property
    def use_clamp(self) -> bool:
        return self.node.use_clamp

    @use_clamp.setter
    def use_clamp(self, value: bool):
        self.node.use_clamp = value

    @property
    def o_value(self) -> SocketLinker:
        return self._output("Value")  # type: ignore

    @property
    def i_value(self) -> SocketLinker:
        return self._input("Value")

    @property
    def i_value_001(self) -> SocketLinker:
        return self._input("Value_001")

    @property
    def i_value_002(self) -> SocketLinker:
        return self._input("Value_002")

    @classmethod
    def add(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation of `a + b`."""
        return cls(operation="ADD", Value=a, Value_001=b)

    @classmethod
    def subtract(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation of `a - b`."""
        return cls(operation="SUBTRACT", Value=a, Value_001=b)

    @classmethod
    def multiply(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation of `a * b`."""
        return cls(operation="MULTIPLY", Value=a, Value_001=b)

    @classmethod
    def divide(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation of `a / b`."""
        return cls(operation="DIVIDE", Value=a, Value_001=b)

    @classmethod
    def multiply_add(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
        c: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `a * b + c`."""
        return cls(operation="MULTIPLY_ADD", Value=a, Value_001=b, value_002=c)

    @classmethod
    def power(
        cls,
        base: float | LINKABLE = 0.5,
        exponent: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `base ** exponent`."""
        return cls(operation="POWER", Value=base, Value_001=exponent)

    @classmethod
    def logarithm(
        cls,
        value: float | LINKABLE = 0.5,
        base: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `log(value, base)`."""
        return cls(operation="LOGARITHM", Value=value, Value_001=base)

    @classmethod
    def sqrt(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `sqrt(value)`."""
        return cls(operation="SQRT", Value=value)

    @classmethod
    def inverse_sqrt(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `inverse_sqrt(value)`."""
        return cls(operation="INVERSE_SQRT", Value=value)

    @classmethod
    def absolute(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `abs(value)`."""
        return cls(operation="ABSOLUTE", Value=value)

    @classmethod
    def exponent(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `exp(value)`."""
        return cls(operation="EXPONENT", Value=value)

    @classmethod
    def minimum(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `min(a, b)`."""
        return cls(operation="MINIMUM", Value=a, Value_001=b)

    @classmethod
    def maximum(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `max(a, b)`."""
        return cls(operation="MAXIMUM", Value=a, Value_001=b)

    @classmethod
    def less_than(
        cls,
        value: float | LINKABLE = 0.5,
        threshold: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `value < threshold` returning 1 or 0."""
        return cls(operation="LESS_THAN", Value=value, Value_001=threshold)

    @classmethod
    def greater_than(
        cls,
        value: float | LINKABLE = 0.5,
        threshold: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `value > threshold` returning 1 or 0."""
        return cls(operation="GREATER_THAN", Value=value, Value_001=threshold)

    @classmethod
    def sign(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `sign(value)` returning -1, 0, or 1."""
        return cls(operation="SIGN", Value=value)

    @classmethod
    def compare(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
        epsilon: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `compare(a, b, epsilon)` returning -1, 0, or 1."""
        return cls(operation="COMPARE", Value=a, Value_001=b, value_002=epsilon)

    @classmethod
    def smooth_min(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
        distance: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `smooth_min(a, b, distance)`."""
        return cls(operation="SMOOTH_MIN", Value=a, Value_001=b, value_002=distance)

    @classmethod
    def smooth_max_(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
        distance: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `smooth_max(a, b, distance)`."""
        return cls(operation="SMOOTH_MAX", Value=a, Value_001=b, value_002=distance)

    @classmethod
    def round(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Round A to the nearest integer. Round up if 0.5 or greater."""
        return cls(operation="ROUND", Value=value)

    @classmethod
    def floor(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """The largest integer smaller than or equal to `value`"""
        return cls(operation="FLOOR", Value=value)

    @classmethod
    def ceil(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """The smallest integer greater than or equal to `value`"""
        return cls(operation="CEIL", Value=value)

    @classmethod
    def truncate(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """The integer part of `value` removing the fractional part"""
        return cls(operation="TRUNC", Value=value)

    @classmethod
    def fraction(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """The fractional part of `value`"""
        return cls(operation="FRACT", Value=value)

    @classmethod
    def truncated_modulo(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """The remained of truncated division using fmod(a, b)"""
        return cls(operation="MODULO", Value=a, Value_001=b)

    @classmethod
    def floored_modulo(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """The remained of floored division"""
        return cls(operation="FLOORED_MODULO", Value=a, Value_001=b)

    @classmethod
    def wrap(
        cls,
        value: float | LINKABLE = 0.5,
        max: float | LINKABLE = 0.5,
        min: float | LINKABLE = 0.5,
    ) -> "Math":
        """Wrap value to range, wrap(value, max, min)"""
        return cls(operation="WRAP", Value=value, Value_001=max, value_002=min)

    @classmethod
    def snap(
        cls,
        value: float | LINKABLE = 0.5,
        increment: float | LINKABLE = 0.5,
    ) -> "Math":
        """Snap to increment of `snap(value, increment)`"""
        return cls(operation="SNAP", Value=value, Value_001=increment)

    @classmethod
    def ping_pong(
        cls,
        value: float | LINKABLE = 0.5,
        scale: float | LINKABLE = 0.5,
    ) -> "Math":
        """Wraps a value and reverses every other cycle"""
        return cls(operation="PINGPONG", Value=value, Value_001=scale)

    @classmethod
    def sine(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'sin(value)'."""
        return cls(operation="SINE", Value=value)

    @classmethod
    def cosine(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'cos(value)'."""
        return cls(operation="COSINE", Value=value)

    @classmethod
    def tangent(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'tan(value)'."""
        return cls(operation="TANGENT", Value=value)

    @classmethod
    def arcsine(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `arcsin(value)`."""
        return cls(operation="ARCSINE", Value=value)

    @classmethod
    def arccosine(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'arccos(value)'."""
        return cls(operation="ARCCOSINE", Value=value)

    @classmethod
    def arctangent(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'arctan(value)'."""
        return cls(operation="ARCTANGENT", Value=value)

    @classmethod
    def arctan2(
        cls,
        a: float | LINKABLE = 0.5,
        b: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'arctan(a / b)'."""
        return cls(operation="ARCTAN2", Value=a, Value_001=b)

    @classmethod
    def sinh(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `sinh(value)`."""
        return cls(operation="SINH", Value=value)

    @classmethod
    def cosh(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `cosh(value)`."""
        return cls(operation="COSH", Value=value)

    @classmethod
    def tanh(
        cls,
        value: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `tanh(value)`."""
        return cls(operation="TANH", Value=value)

    @classmethod
    def radians(
        cls,
        degrees: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation `radians(degrees)`."""
        return cls(operation="RADIANS", Value=degrees)

    @classmethod
    def degrees(
        cls,
        radians: float | LINKABLE = 0.5,
    ) -> "Math":
        """Create Math with operation 'To Degrees'."""
        return cls(operation="DEGREES", Value=radians)


class BooleanMath(NodeBuilder):
    """Boolean Math node"""

    name = "FunctionNodeBooleanMath"
    node: bpy.types.FunctionNodeBooleanMath

    def __init__(self, operation: types.NodeBooleanMathItems = "AND", **kwargs):
        super().__init__()
        self.operator = operation
        self._establish_links(**kwargs)

    @property
    def operation(self) -> types.NodeBooleanMathItems:
        return self.node.operation

    @operation.setter
    def operation(self, value: types.NodeBooleanMathItems):
        self.node.operation = value

    @property
    def i_boolean(self) -> SocketLinker:
        return self._input("Boolean")  # type: ignore

    @property
    def i_boolean_001(self) -> SocketLinker:
        return self._input("Boolean_001")  # type: ignore

    @property
    def o_boolean(self) -> SocketLinker:
        return self._output("Boolean")  # type: ignore

    @classmethod
    def l_and(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'AND'."""
        return cls(operation="AND", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_or(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'OR'."""
        return cls(operation="OR", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_not(cls, boolean: TYPE_INPUT_BOOLEAN = False) -> "BooleanMath":
        """Create Boolean Math with operation 'NOT'."""
        return cls(operation="NOT", Boolean=boolean)

    @classmethod
    def l_not_and(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'NAND'."""
        return cls(operation="NAND", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_nor(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'NOR'."""
        return cls(operation="NOR", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_equal(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'XNOR'."""
        return cls(operation="XNOR", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_not_equal(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'XOR'."""
        return cls(operation="XOR", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_imply(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'IMPLY'."""
        return cls(operation="IMPLY", Boolean=boolean, Boolean_001=boolean_001)

    @classmethod
    def l_subtract(
        cls,
        boolean: TYPE_INPUT_BOOLEAN = False,
        boolean_001: TYPE_INPUT_BOOLEAN = False,
    ) -> "BooleanMath":
        """Create Boolean Math with operation 'NIMPLY'."""
        return cls(operation="NIMPLY", Boolean=boolean, Boolean_001=boolean_001)


class VectorMath(NodeBuilder):
    """Perform vector math operation"""

    name = "ShaderNodeVectorMath"
    node: bpy.types.ShaderNodeVectorMath

    def __init__(
        self,
        operation: _VectorMathOperations = "ADD",
        **kwargs,
    ):
        super().__init__()
        self.operation = operation
        self._establish_links(**kwargs)

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_vector_001(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector_001")

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        if self.operation in {"DOT_PRODUCT", "DISTANCE", "LENGTH"}:
            raise RuntimeError(
                f"Output 'Vector' is not available for operation '{self.operation}'"
            )
        return self._output("Vector")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        assert self.operation in {"DOT_PRODUCT", "DISTANCE", "LENGTH"}
        return self._output("Value")

    @property
    def _default_output_socket(self) -> bpy.types.NodeSocket:
        match self.operation:
            case "DOT_PRODUCT" | "DISTANCE" | "LENGTH":
                return self.o_value.socket
            case _:
                return self.o_vector.socket

    @property
    def operation(
        self,
    ) -> _VectorMathOperations:
        return self.node.operation

    @operation.setter
    def operation(
        self,
        value: _VectorMathOperations,
    ):
        self.node.operation = value

    @classmethod
    def add(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation `a + b`."""
        return cls(operation="ADD", Vector=a, Vector_001=b)

    @classmethod
    def subtract(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation `a - b`."""
        return cls(operation="SUBTRACT", Vector=a, Vector_001=b)

    @classmethod
    def multiply(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation `a * b` element-wise."""
        return cls(operation="MULTIPLY", Vector=a, Vector_001=b)

    @classmethod
    def divide(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Divide'."""
        return cls(operation="DIVIDE", Vector=a, Vector_001=b)

    @classmethod
    def multiply_add(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        multiplier: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        addend: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Multiply Add'."""
        return cls(
            operation="MULTIPLY_ADD",
            Vector=vector,
            Vector_001=multiplier,
            Vector_002=addend,
        )

    @classmethod
    def cross_product(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Cross Product'."""
        return cls(operation="CROSS_PRODUCT", Vector=a, Vector_001=b)

    @classmethod
    def project(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Project A onto B."""
        return cls(operation="PROJECT", Vector=a, Vector_001=b)

    @classmethod
    def reflect(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Reflect A around the normal B. B does not need to be normalized."""
        return cls(operation="REFLECT", Vector=a, Vector_001=b)

    @classmethod
    def refract(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        ior: LINKABLE | float = 1.0,
    ) -> "VectorMath":
        """For a given incident vector and surface normal (b) with an index of refraction (ior), return the refraction vector"""
        return cls(operation="REFRACT", Vector=a, Vector_001=b, Scale=ior)

    @classmethod
    def face_forward(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        incidence: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        reference: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Orients a vector to face away from a surface (incidence) defined by it's normal (reference)"""
        return cls(
            operation="FACEFORWARD",
            Vector=vector,
            Vector_001=incidence,
            Vector_002=reference,
        )

    @classmethod
    def dot_product(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Dot Product'."""
        return cls(operation="DOT_PRODUCT", Vector=a, Vector_001=b)

    @classmethod
    def distance(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Distance'."""
        return cls(operation="DISTANCE", Vector=a, Vector_001=b)

    @classmethod
    def length(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Length'."""
        return cls(operation="LENGTH", Vector=vector)

    @classmethod
    def scale(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        scale: LINKABLE | float = 1.0,
    ) -> "VectorMath":
        """Create Vector Math with operation 'Scale'."""
        return cls(operation="SCALE", Vector=vector, Scale=scale)

    @classmethod
    def normalize(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Normalize'."""
        return cls(operation="NORMALIZE", Vector=vector)

    @classmethod
    def absolute(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Absolute'."""
        return cls(operation="ABSOLUTE", Vector=vector)

    @classmethod
    def power(
        cls,
        base: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        exponent: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Power'."""
        return cls(operation="POWER", Vector=base, Vector_001=exponent)

    @classmethod
    def sign(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Sign'."""
        return cls(operation="SIGN", Vector=vector)

    @classmethod
    def minimum(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Minimum'."""
        return cls(operation="MINIMUM", Vector=a, Vector_001=b)

    @classmethod
    def maximum(
        cls,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Maximum'."""
        return cls(operation="MAXIMUM", Vector=a, Vector_001=b)

    @classmethod
    def floor(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Floor'."""
        return cls(operation="FLOOR", Vector=vector)

    @classmethod
    def ceil(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Ceil'."""
        return cls(operation="CEIL", Vector=vector)

    @classmethod
    def fraction(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Fraction'."""
        return cls(operation="FRACTION", Vector=vector)

    @classmethod
    def modulo(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Modulo'."""
        return cls(operation="MODULO", Vector=vector)

    @classmethod
    def wrap(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        min: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        max: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Wrap'."""
        return cls(operation="WRAP", Vector=vector, Vector_001=min, Vector_002=max)

    @classmethod
    def snap(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        increment: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Snap'."""
        return cls(operation="SNAP", Vector=vector, Vector_001=increment)

    @classmethod
    def sine(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Sine'."""
        return cls(operation="SINE", Vector=vector)

    @classmethod
    def cosine(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Cosine'."""
        return cls(operation="COSINE", Vector=vector)

    @classmethod
    def tangent(
        cls,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
    ) -> "VectorMath":
        """Create Vector Math with operation 'Tangent'."""
        return cls(operation="TANGENT", Vector=vector)


class RandomValue(NodeBuilder):
    """Random Value node"""

    name = "FunctionNodeRandomValue"
    node: bpy.types.FunctionNodeRandomValue
    _default_input_id = "ID"

    def __init__(
        self,
        data_type: _RandomValueDataTypes,
        id: TYPE_INPUT_INT = None,
        seed: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        self.node.data_type = data_type
        key_args = {
            "ID": id,
            "Seed": seed,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def data_type(self) -> _RandomValueDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: _RandomValueDataTypes):
        self.node.data_type = value

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        match self.data_type:
            case "FLOAT":
                return self._output("Value_001")
            case "INT":
                return self._output("Value_002")
            case "BOOLEAN":
                return self._output("Value_003")
            case "FLOAT_VECTOR":
                return self._output("Value")

    def i_min(self) -> SocketLinker:
        """Input socket: Minimum"""
        match self.data_type:
            case "FLOAT":
                return self._input("Min_001")
            case "INT":
                return self._input("Min_002")
            case "BOOLEAN":
                raise ValueError(
                    "Boolean data type does not support minimum value, use 'Probability'"
                )
            case "FLOAT_VECTOR":
                return self._input("Min")

    def i_max(self) -> SocketLinker:
        """Input socket: Maximum"""
        match self.data_type:
            case "FLOAT":
                return self._input("Max_001")
            case "INT":
                return self._input("Max_002")
            case "BOOLEAN":
                raise ValueError(
                    "Boolean data type does not support maximum value, use 'Probability'"
                )
            case "FLOAT_VECTOR":
                return self._input("Max")

    def i_probability(self) -> SocketLinker:
        """Input socket: Probability"""
        if self.data_type != "BOOLEAN":
            raise ValueError(
                f"Probability socket is only supported for boolean data types, not for data type: {self.data_type}"
            )

        return self._input("Probability")

    @classmethod
    def float(
        cls,
        min: TYPE_INPUT_VALUE = 0.0,
        max: TYPE_INPUT_VALUE = 1.0,
        id: TYPE_INPUT_INT = None,
        seed: int | LINKABLE = 1,
    ) -> NodeBuilder:
        buidler = cls(Min_001=min, Max_001=max, id=id, seed=seed, data_type="FLOAT")
        buidler._default_output_id = "Value_001"
        return buidler

    @classmethod
    def integer(
        cls,
        min: TYPE_INPUT_INT = 0,
        max: TYPE_INPUT_INT = 1,
        id: TYPE_INPUT_INT = None,
        seed: TYPE_INPUT_INT = 1,
    ) -> NodeBuilder:
        buidler = cls(Min_002=min, Max_002=max, id=id, seed=seed, data_type="INT")
        buidler._default_output_id = "Value_002"
        return buidler

    @classmethod
    def boolean(
        cls,
        probability: TYPE_INPUT_VALUE = 0.5,
        id: TYPE_INPUT_INT = None,
        seed: TYPE_INPUT_INT = 1,
    ) -> NodeBuilder:
        builder = cls(Probability=probability, id=id, seed=seed, data_type="BOOLEAN")
        builder._default_output_id = "Value_003"
        return builder

    @classmethod
    def vector(
        cls,
        min: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        max: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
        id: TYPE_INPUT_INT = None,
        seed: TYPE_INPUT_INT = 1,
    ) -> NodeBuilder:
        builder = cls(Min=min, Max=max, id=id, seed=seed, data_type="FLOAT_VECTOR")
        builder._default_output_id = "Value"
        return builder


class SeparateXYZ(NodeBuilder):
    """Split a vector into its X, Y, and Z components"""

    name = "ShaderNodeSeparateXYZ"
    node: bpy.types.ShaderNodeSeparateXYZ  # type: ignore

    def __init__(self, vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0)):
        super().__init__()
        self._establish_links(**{"Vector": vector})

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


class CombineXYZ(NodeBuilder):
    """Create a vector from X, Y, and Z components"""

    name = "ShaderNodeCombineXYZ"
    node: bpy.types.ShaderNodeCombineXYZ  # type: ignore

    def __init__(
        self,
        x: TYPE_INPUT_VALUE = 0.0,
        y: TYPE_INPUT_VALUE = 0.0,
        z: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        self._establish_links(**{"X": x, "Y": y, "Z": z})

    @property
    def o_vector(self) -> SocketLinker:
        """Output socket: Vector"""
        return self._output("Vector")

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


class Mix(NodeBuilder):
    """Mix values by a factor"""

    name = "ShaderNodeMix"
    node: bpy.types.ShaderNodeMix  # type: ignore

    def __init__(
        self,
        data_type: _MixDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        self._default_input_id = f"A_{data_type.title()}"
        self._default_output_id = f"Result_{data_type.title()}"
        self.node.data_type = "RGBA" if data_type == "COLOR" else data_type
        key_args = {}
        key_args.update(kwargs)
        self._establish_links(**key_args)

    @property
    def data_type(self) -> str:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: _MixDataTypes):
        self.node.data_type = value  # type: ignore

    @property
    def factor_mode(self) -> Literal["UNIFORM", "NON_UNIFORM"]:
        return self.node.factor_mode

    @factor_mode.setter
    def factor_mode(self, value: Literal["NON_UNIFORM", "UNIFORM"]):
        self.node.factor_mode = value

    @property
    def o_result(self) -> SocketLinker:
        """Output socket: Result"""
        return SocketLinker(self._default_output_socket)

    @property
    def i_factor(self) -> SocketLinker:
        """Input socket: Factor"""
        match self.data_type:
            case "FLOAT":
                name = "Factor_Float"
            case "VECTOR":
                name = (
                    "Factor_Float" if self.factor_mode == "UNIFORM" else "Factor_Vector"
                )
            case "RGBA":
                name = "Factor_Color"
            case "ROTATION":
                name = "Factor_Rotation"
            case _:
                raise ValueError(f"Unsupported data type: {self.data_type}")

        idx = self._input_idx(name)
        return SocketLinker(self.node.inputs[idx])

    @property
    def i_value_a(self) -> SocketLinker:
        """Input socket: Value A"""
        type_name = "Color" if self.data_type == "RGBA" else self.data_type
        name = f"A_{type_name}"
        idx = self._input_idx(name)
        return SocketLinker(self.node.inputs[idx])

    @property
    def i_value_b(self) -> SocketLinker:
        """Input socket: Value B"""
        type_name = "Color" if self.data_type == "RGBA" else self.data_type
        name = f"B_{type_name}"
        idx = self._input_idx(name)
        return SocketLinker(self.node.inputs[idx])

    @classmethod
    def float(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a: TYPE_INPUT_VALUE = 0.0,
        b: TYPE_INPUT_VALUE = 0.0,
        clamp_factor: bool = True,
    ) -> "Mix":
        builder = cls(
            Factor_Float=factor,
            A_Float=a,
            B_Float=b,
            data_type="COLOR",
        )
        builder.node.clamp_factor = clamp_factor
        return builder

    @classmethod
    def vector(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
        clamp_factor: bool = True,
        factor_mode: Literal["UNIFORM", "NON_UNIFORM"] = "UNIFORM",
    ) -> "Mix":
        match factor_mode:
            case "UNIFORM":
                builder = cls(
                    Factor_Float=factor,
                    A_Vector=a,
                    B_Vector=b,
                    data_type="VECTOR",
                )
            case "NON_UNIFORM":
                builder = cls(
                    Factor_Vector=factor,
                    A_Vector=a,
                    B_Vector=b,
                    data_type="VECTOR",
                )

        builder.node.clamp_factor = clamp_factor
        return builder

    @classmethod
    def color(
        cls,
        factor: TYPE_INPUT_VALUE = 0.5,
        a: TYPE_INPUT_COLOR = (0.0, 0.0, 0.0, 0.0),
        b: TYPE_INPUT_COLOR = (1.0, 1.0, 1.0, 1.0),
        blend_type: _MixColorBlendTypes = "ADD",
        clamp_factor: bool = True,
        clamp_result: bool = True,
    ) -> "Mix":
        builder = cls(
            Factor_Float=factor,
            A_Color=a,
            B_Color=b,
            data_type="COLOR",
        )
        builder.node.blend_type = blend_type
        builder.node.clamp_factor = clamp_factor
        builder.node.clamp_result = clamp_result
        return builder

    @classmethod
    def rotation(
        cls,
        a: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        b: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        factor: TYPE_INPUT_VALUE = 0.5,
        clamp_factor: bool = True,
    ) -> "Mix":
        builder = cls(
            Factor_Float=factor,
            A_Rotation=a,
            B_Rotation=b,
            data_type="ROTATION",
        )
        builder.node.clamp_factor = clamp_factor
        return builder


class AccumulateField(NodeBuilder):
    """Add the values of an evaluated field together and output the running total for each element"""

    name = "GeometryNodeAccumulateField"
    node: bpy.types.GeometryNodeAccumulateField

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 1.0,
        group_index: TYPE_INPUT_INT = 0,
        data_type: _AccumulateFieldDataTypes = "FLOAT",
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        key_args.update(kwargs)
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
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
    def data_type(self) -> _AccumulateFieldDataTypes:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: _AccumulateFieldDataTypes):
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


class EvaluateAtIndex(NodeBuilder):
    """Retrieve data of other elements in the context's geometry"""

    name = "GeometryNodeFieldAtIndex"
    node: bpy.types.GeometryNodeFieldAtIndex

    def __init__(
        self,
        value: LINKABLE = None,
        index: TYPE_INPUT_INT = 0,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Index": index}
        key_args.update(kwargs)
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

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
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def data_type(
        self,
    ) -> _EvaluateAtIndexDataTypes:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: _EvaluateAtIndexDataTypes,
    ):
        self.node.data_type = value


class FieldAverage(NodeBuilder):
    """Calculate the mean and median of a given field"""

    name = "GeometryNodeFieldAverage"
    node: bpy.types.GeometryNodeFieldAverage

    def __init__(
        self,
        value: LINKABLE = None,
        group_index: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
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
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class FieldMinMax(NodeBuilder):
    """Calculate the minimum and maximum of a given field"""

    name = "GeometryNodeFieldMinAndMax"
    node: bpy.types.GeometryNodeFieldMinAndMax

    def __init__(
        self,
        value: LINKABLE = None,
        group_index: TYPE_INPUT_INT = None,
        *,
        data_type: Literal["FLOAT", "INT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
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
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class EvaluateOnDomain(NodeBuilder):
    """Retrieve values from a field on a different domain besides the domain from the context"""

    name = "GeometryNodeFieldOnDomain"
    node: bpy.types.GeometryNodeFieldOnDomain

    def __init__(
        self,
        value: LINKABLE = None,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Value": value}
        self.domain = domain
        self.data_type = data_type
        self._establish_links(**key_args)

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
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def data_type(
        self,
    ) -> _EvaluateAtIndexDataTypes:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: _EvaluateAtIndexDataTypes,
    ):
        self.node.data_type = value


class FieldVariance(NodeBuilder):
    """Calculate the standard deviation and variance of a given field"""

    name = "GeometryNodeFieldVariance"
    node: bpy.types.GeometryNodeFieldVariance

    def __init__(
        self,
        value: LINKABLE = None,
        group_index: TYPE_INPUT_INT = None,
        *,
        data_type: Literal["FLOAT", "FLOAT_VECTOR"] = "FLOAT",
        domain: _AttributeDomains = "POINT",
    ):
        super().__init__()
        key_args = {"Value": value, "Group Index": group_index}
        self.data_type = data_type
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
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
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value


class IndexOfNearest(NodeBuilder):
    """Find the nearest element in a group. Similar to the "Sample Nearest" node"""

    name = "GeometryNodeIndexOfNearest"
    node: bpy.types.GeometryNodeIndexOfNearest

    def __init__(
        self, position: TYPE_INPUT_VECTOR = None, group_id: TYPE_INPUT_INT = None
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


class JoinStrings(NodeBuilder):
    """Combine any number of input strings"""

    name = "GeometryNodeStringJoin"
    node: bpy.types.GeometryNodeStringJoin

    def __init__(self, *args: LINKABLE, delimiter: TYPE_INPUT_STRING = ""):
        super().__init__()

        self._establish_links(Delimiter=delimiter)
        for arg in args:
            self.link_from(arg, "Strings")

    @property
    def i_delimiter(self) -> SocketLinker:
        """Input socket: Delimiter"""
        return self._input("Delimiter")

    @property
    def i_strings(self) -> SocketLinker:
        """Input socket: Strings"""
        return self._input("Strings")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class Switch(NodeBuilder):
    """Switch between two inputs"""

    name = "GeometryNodeSwitch"
    node: bpy.types.GeometryNodeSwitch

    def __init__(
        self,
        switch: TYPE_INPUT_BOOLEAN = False,
        false: LINKABLE = None,
        true: LINKABLE = None,
        *,
        input_type: SOCKET_TYPES = "GEOMETRY",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Switch": switch, "False": false, "True": true}
        key_args.update(kwargs)
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
    ) -> SOCKET_TYPES:
        return self.node.input_type  # type: ignore

    @input_type.setter
    def input_type(
        self,
        value: SOCKET_TYPES,
    ):
        self.node.input_type = value


class PackUVIslands(NodeBuilder):
    """Scale islands of a UV map and move them so they fill the UV space as much as possible"""

    name = "GeometryNodeUVPackIslands"
    node: bpy.types.GeometryNodeUVPackIslands

    def __init__(
        self,
        uv: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        selection: TYPE_INPUT_BOOLEAN = True,
        margin: TYPE_INPUT_VALUE = 0.001,
        rotate: TYPE_INPUT_BOOLEAN = True,
        method: Literal["Bounding Box", "Convex Hull", "Exact Shape"] = "Bounding Box",
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
        method: Literal["Angle Based", "Conformal"] = "Angle Based",
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


class FloatCurve(NodeBuilder):
    """Map an input float to a curve and outputs a float value"""

    # TODO: add support for custom curves

    name = "ShaderNodeFloatCurve"
    node: bpy.types.ShaderNodeFloatCurve

    def __init__(self, factor: TYPE_INPUT_VALUE = 1.0, value: TYPE_INPUT_VALUE = 1.0):
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
