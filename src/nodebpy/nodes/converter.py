import bpy
from typing_extensions import Literal

from nodebpy.builder import NodeBuilder, SocketLinker
from nodebpy.nodes.types import SOCKET_COMPATIBILITY

from .types import (
    LINKABLE,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_INT,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
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

    def __init__(
        self,
        *args,
        format: TYPE_INPUT_STRING = "",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Format": format}
        # key_args.update(kwargs)
        key_args.update(self.add_inputs(*args, **kwargs))
        self._establish_links(**key_args)

    def _socket_type_from_linkable(self, linkable: LINKABLE):
        if linkable is None:
            raise ValueError("Linkable cannot be None")
        for comp in SOCKET_COMPATIBILITY[linkable.type]:
            if comp in ("VALUE", "INT", "STRING"):
                return comp if comp != "VALUE" else "FLOAT"
        raise ValueError(
            f"Unsupported socket type for linking to the FormatString: {linkable}, type: {linkable.type=}"
        )

    def add_inputs(
        self, *args, **kwargs
    ) -> dict[str, tuple[LINKABLE, bpy.types.NodeSocket]]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        # kwargs.update({arg.name: arg for arg in args})
        for arg in args:
            if isinstance(arg, bpy.types.NodeSocket):
                kwargs[arg.name] = arg
            else:
                kwargs[arg._default_output_socket.name] = arg

        for key, value in kwargs.items():
            type = self._socket_type_from_linkable(value)
            socket = self.add_socket(name=key, type=type)
            new_sockets[socket.name] = value

        return new_sockets

    def add_socket(
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

    @property
    def active_index(self) -> int:
        return self.node.active_index

    @active_index.setter
    def active_index(self, value: int):
        self.node.active_index = value


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
