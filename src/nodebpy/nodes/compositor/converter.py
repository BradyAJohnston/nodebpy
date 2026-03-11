from typing import Literal

import bpy

from ...builder import NodeBuilder, SocketLinker
from ...types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class AlphaConvert(NodeBuilder):
    """
    Convert to and from premultiplied (associated) alpha
    """

    _bl_idname = "CompositorNodePremulKey"
    node: bpy.types.CompositorNodePremulKey

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        type: TYPE_INPUT_MENU = "To Premultiplied",
    ):
        super().__init__()
        key_args = {"Image": image, "Type": type}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_type(self) -> SocketLinker:
        """Input socket: Type"""
        return self._input("Type")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class Blackbody(NodeBuilder):
    """
    Convert a blackbody temperature to an RGB value
    """

    _bl_idname = "ShaderNodeBlackbody"
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


class Clamp(NodeBuilder):
    """
    Clamp a value between a minimum and a maximum
    """

    _bl_idname = "ShaderNodeClamp"
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
    """
    Map values to colors with the use of a gradient
    """

    _bl_idname = "ShaderNodeValToRGB"
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


class CombineColor(NodeBuilder):
    """
    Combine an image from its composite color channels
    """

    _bl_idname = "CompositorNodeCombineColor"
    node: bpy.types.CompositorNodeCombineColor

    def __init__(
        self,
        red: TYPE_INPUT_VALUE = 0.0,
        green: TYPE_INPUT_VALUE = 0.0,
        blue: TYPE_INPUT_VALUE = 0.0,
        alpha: TYPE_INPUT_VALUE = 1.0,
        *,
        mode: Literal["RGB", "HSV", "HSL", "YCC", "YUV"] = "RGB",
        ycc_mode: Literal["ITUBT601", "ITUBT709", "JFIF"] = "ITUBT709",
    ):
        super().__init__()
        key_args = {"Red": red, "Green": green, "Blue": blue, "Alpha": alpha}
        self.mode = mode
        self.ycc_mode = ycc_mode
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
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def mode(self) -> Literal["RGB", "HSV", "HSL", "YCC", "YUV"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["RGB", "HSV", "HSL", "YCC", "YUV"]):
        self.node.mode = value

    @property
    def ycc_mode(self) -> Literal["ITUBT601", "ITUBT709", "JFIF"]:
        return self.node.ycc_mode

    @ycc_mode.setter
    def ycc_mode(self, value: Literal["ITUBT601", "ITUBT709", "JFIF"]):
        self.node.ycc_mode = value


class CombineXYZ(NodeBuilder):
    """
    Create a vector from X, Y, and Z components
    """

    _bl_idname = "ShaderNodeCombineXYZ"
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


class ConvertColorspace(NodeBuilder):
    """
    Convert between color spaces
    """

    _bl_idname = "CompositorNodeConvertColorSpace"
    node: bpy.types.CompositorNodeConvertColorSpace

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        *,
        from_color_space: Literal[
            "ACES 1.3 sRGB",
            "ACES 2.0 sRGB",
            "ACES2065-1",
            "ACEScc",
            "ACEScct",
            "ACEScg",
            "AgX Base sRGB",
            "AgX Log",
            "Display P3",
            "Filmic Log",
            "Filmic sRGB",
            "Khronos PBR Neutral sRGB",
            "Linear CIE-XYZ D65",
            "Linear CIE-XYZ E",
            "Linear DCI-P3 D65",
            "Linear FilmLight E-Gamut",
            "Linear Rec.2020",
            "Linear Rec.709",
            "Non-Color",
            "Rec.1886",
            "Rec.2020",
            "Rec.2100-HLG",
            "Rec.2100-PQ",
            "sRGB",
            "scene_linear",
        ] = "scene_linear",
        to_color_space: Literal[
            "ACES 1.3 sRGB",
            "ACES 2.0 sRGB",
            "ACES2065-1",
            "ACEScc",
            "ACEScct",
            "ACEScg",
            "AgX Base sRGB",
            "AgX Log",
            "Display P3",
            "Filmic Log",
            "Filmic sRGB",
            "Khronos PBR Neutral sRGB",
            "Linear CIE-XYZ D65",
            "Linear CIE-XYZ E",
            "Linear DCI-P3 D65",
            "Linear FilmLight E-Gamut",
            "Linear Rec.2020",
            "Linear Rec.709",
            "Non-Color",
            "Rec.1886",
            "Rec.2020",
            "Rec.2100-HLG",
            "Rec.2100-PQ",
            "sRGB",
            "scene_linear",
        ] = "scene_linear",
    ):
        super().__init__()
        key_args = {"Image": image}
        self.from_color_space = from_color_space
        self.to_color_space = to_color_space
        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def from_color_space(
        self,
    ) -> Literal[
        "ACES 1.3 sRGB",
        "ACES 2.0 sRGB",
        "ACES2065-1",
        "ACEScc",
        "ACEScct",
        "ACEScg",
        "AgX Base sRGB",
        "AgX Log",
        "Display P3",
        "Filmic Log",
        "Filmic sRGB",
        "Khronos PBR Neutral sRGB",
        "Linear CIE-XYZ D65",
        "Linear CIE-XYZ E",
        "Linear DCI-P3 D65",
        "Linear FilmLight E-Gamut",
        "Linear Rec.2020",
        "Linear Rec.709",
        "Non-Color",
        "Rec.1886",
        "Rec.2020",
        "Rec.2100-HLG",
        "Rec.2100-PQ",
        "sRGB",
        "scene_linear",
    ]:
        return self.node.from_color_space

    @from_color_space.setter
    def from_color_space(
        self,
        value: Literal[
            "ACES 1.3 sRGB",
            "ACES 2.0 sRGB",
            "ACES2065-1",
            "ACEScc",
            "ACEScct",
            "ACEScg",
            "AgX Base sRGB",
            "AgX Log",
            "Display P3",
            "Filmic Log",
            "Filmic sRGB",
            "Khronos PBR Neutral sRGB",
            "Linear CIE-XYZ D65",
            "Linear CIE-XYZ E",
            "Linear DCI-P3 D65",
            "Linear FilmLight E-Gamut",
            "Linear Rec.2020",
            "Linear Rec.709",
            "Non-Color",
            "Rec.1886",
            "Rec.2020",
            "Rec.2100-HLG",
            "Rec.2100-PQ",
            "sRGB",
            "scene_linear",
        ],
    ):
        self.node.from_color_space = value

    @property
    def to_color_space(
        self,
    ) -> Literal[
        "ACES 1.3 sRGB",
        "ACES 2.0 sRGB",
        "ACES2065-1",
        "ACEScc",
        "ACEScct",
        "ACEScg",
        "AgX Base sRGB",
        "AgX Log",
        "Display P3",
        "Filmic Log",
        "Filmic sRGB",
        "Khronos PBR Neutral sRGB",
        "Linear CIE-XYZ D65",
        "Linear CIE-XYZ E",
        "Linear DCI-P3 D65",
        "Linear FilmLight E-Gamut",
        "Linear Rec.2020",
        "Linear Rec.709",
        "Non-Color",
        "Rec.1886",
        "Rec.2020",
        "Rec.2100-HLG",
        "Rec.2100-PQ",
        "sRGB",
        "scene_linear",
    ]:
        return self.node.to_color_space

    @to_color_space.setter
    def to_color_space(
        self,
        value: Literal[
            "ACES 1.3 sRGB",
            "ACES 2.0 sRGB",
            "ACES2065-1",
            "ACEScc",
            "ACEScct",
            "ACEScg",
            "AgX Base sRGB",
            "AgX Log",
            "Display P3",
            "Filmic Log",
            "Filmic sRGB",
            "Khronos PBR Neutral sRGB",
            "Linear CIE-XYZ D65",
            "Linear CIE-XYZ E",
            "Linear DCI-P3 D65",
            "Linear FilmLight E-Gamut",
            "Linear Rec.2020",
            "Linear Rec.709",
            "Non-Color",
            "Rec.1886",
            "Rec.2020",
            "Rec.2100-HLG",
            "Rec.2100-PQ",
            "sRGB",
            "scene_linear",
        ],
    ):
        self.node.to_color_space = value


class ConvertToDisplay(NodeBuilder):
    """
    Convert from scene linear to display color space, with a view transform and look for tone mapping
    """

    _bl_idname = "CompositorNodeConvertToDisplay"
    node: bpy.types.CompositorNodeConvertToDisplay

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        invert: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {"Image": image, "Invert": invert}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_invert(self) -> SocketLinker:
        """Input socket: Invert"""
        return self._input("Invert")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class FloatCurve(NodeBuilder):
    """
    Map an input float to a curve and outputs a float value
    """

    _bl_idname = "ShaderNodeFloatCurve"
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


class IDMask(NodeBuilder):
    """
    Create a matte from an object or material index pass
    """

    _bl_idname = "CompositorNodeIDMask"
    node: bpy.types.CompositorNodeIDMask

    def __init__(
        self,
        id_value: TYPE_INPUT_VALUE = 1.0,
        index: TYPE_INPUT_INT = 0,
        anti_alias: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {"ID value": id_value, "Index": index, "Anti-Alias": anti_alias}

        self._establish_links(**key_args)

    @property
    def i_id_value(self) -> SocketLinker:
        """Input socket: ID value"""
        return self._input("ID value")

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def i_anti_alias(self) -> SocketLinker:
        """Input socket: Anti-Alias"""
        return self._input("Anti-Alias")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")


class Levels(NodeBuilder):
    """
    Compute average and standard deviation of pixel values
    """

    _bl_idname = "CompositorNodeLevels"
    node: bpy.types.CompositorNodeLevels

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        channel: TYPE_INPUT_MENU = "Combined",
    ):
        super().__init__()
        key_args = {"Image": image, "Channel": channel}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_channel(self) -> SocketLinker:
        """Input socket: Channel"""
        return self._input("Channel")

    @property
    def o_mean(self) -> SocketLinker:
        """Output socket: Mean"""
        return self._output("Mean")

    @property
    def o_standard_deviation(self) -> SocketLinker:
        """Output socket: Standard Deviation"""
        return self._output("Standard Deviation")


class MapRange(NodeBuilder):
    """
    Remap a value from a range to a target range
    """

    _bl_idname = "ShaderNodeMapRange"
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


class Math(NodeBuilder):
    """
    Perform math operations
    """

    _bl_idname = "ShaderNodeMath"
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
    def multiply_add(
        cls,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
    ) -> "Math":
        """Create Math with operation 'Multiply Add'."""
        return cls(
            operation="MULTIPLY_ADD",
            value=value,
            value_001=value_001,
            value_002=value_002,
        )

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
    def square_root(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Square Root'."""
        return cls(operation="SQRT", value=value)

    @classmethod
    def inverse_square_root(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Inverse Square Root'."""
        return cls(operation="INVERSE_SQRT", value=value)

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
    def less_than(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Less Than'."""
        return cls(operation="LESS_THAN", value=value, value_001=value_001)

    @classmethod
    def greater_than(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Greater Than'."""
        return cls(operation="GREATER_THAN", value=value, value_001=value_001)

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
    def smooth_minimum(
        cls,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
    ) -> "Math":
        """Create Math with operation 'Smooth Minimum'."""
        return cls(
            operation="SMOOTH_MIN",
            value=value,
            value_001=value_001,
            value_002=value_002,
        )

    @classmethod
    def smooth_maximum(
        cls,
        value: TYPE_INPUT_VALUE = 0.5,
        value_001: TYPE_INPUT_VALUE = 0.5,
        value_002: TYPE_INPUT_VALUE = 0.5,
    ) -> "Math":
        """Create Math with operation 'Smooth Maximum'."""
        return cls(
            operation="SMOOTH_MAX",
            value=value,
            value_001=value_001,
            value_002=value_002,
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
    def truncated_modulo(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Truncated Modulo'."""
        return cls(operation="MODULO", value=value, value_001=value_001)

    @classmethod
    def floored_modulo(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Floored Modulo'."""
        return cls(operation="FLOORED_MODULO", value=value, value_001=value_001)

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
    def ping_pong(
        cls, value: TYPE_INPUT_VALUE = 0.5, value_001: TYPE_INPUT_VALUE = 0.5
    ) -> "Math":
        """Create Math with operation 'Ping-Pong'."""
        return cls(operation="PINGPONG", value=value, value_001=value_001)

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

    @classmethod
    def hyperbolic_sine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Hyperbolic Sine'."""
        return cls(operation="SINH", value=value)

    @classmethod
    def hyperbolic_cosine(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Hyperbolic Cosine'."""
        return cls(operation="COSH", value=value)

    @classmethod
    def hyperbolic_tangent(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'Hyperbolic Tangent'."""
        return cls(operation="TANH", value=value)

    @classmethod
    def to_radians(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'To Radians'."""
        return cls(operation="RADIANS", value=value)

    @classmethod
    def to_degrees(cls, value: TYPE_INPUT_VALUE = 0.5) -> "Math":
        """Create Math with operation 'To Degrees'."""
        return cls(operation="DEGREES", value=value)

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


class MenuSwitch(NodeBuilder):
    """
    Select from multiple inputs by name
    """

    _bl_idname = "GeometryNodeMenuSwitch"
    node: bpy.types.GeometryNodeMenuSwitch

    def __init__(
        self,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_COLOR = None,
        item_1: TYPE_INPUT_COLOR = None,
        extend: LINKABLE = None,
        *,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"
        ] = "RGBA",
    ):
        super().__init__()
        key_args = {
            "Menu": menu,
            "Item_0": item_0,
            "Item_1": item_1,
            "__extend__": extend,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_VALUE = 0.0,
        item_1: TYPE_INPUT_VALUE = 0.0,
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Float'."""
        return cls(
            data_type="FLOAT", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def integer(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_INT = 0,
        item_1: TYPE_INPUT_INT = 0,
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Integer'."""
        return cls(
            data_type="INT", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def boolean(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_BOOLEAN = False,
        item_1: TYPE_INPUT_BOOLEAN = False,
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def vector(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_VECTOR = None,
        item_1: TYPE_INPUT_VECTOR = None,
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Vector'."""
        return cls(
            data_type="VECTOR", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def color(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_COLOR = None,
        item_1: TYPE_INPUT_COLOR = None,
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Color'."""
        return cls(
            data_type="RGBA", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def string(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_STRING = "",
        item_1: TYPE_INPUT_STRING = "",
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'String'."""
        return cls(
            data_type="STRING", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @classmethod
    def menu(
        cls,
        menu: TYPE_INPUT_MENU = "A",
        item_0: TYPE_INPUT_MENU = "",
        item_1: TYPE_INPUT_MENU = "",
        extend: LINKABLE = None,
    ) -> "MenuSwitch":
        """Create Menu Switch with operation 'Menu'."""
        return cls(
            data_type="MENU", menu=menu, item_0=item_0, item_1=item_1, extend=extend
        )

    @property
    def i_menu(self) -> SocketLinker:
        """Input socket: Menu"""
        return self._input("Menu")

    @property
    def i_item_0(self) -> SocketLinker:
        """Input socket: A"""
        return self._input("Item_0")

    @property
    def i_item_1(self) -> SocketLinker:
        """Input socket: B"""
        return self._input("Item_1")

    @property
    def i_extend(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def o_item_0(self) -> SocketLinker:
        """Output socket: A"""
        return self._output("Item_0")

    @property
    def o_item_1(self) -> SocketLinker:
        """Output socket: B"""
        return self._output("Item_1")

    @property
    def data_type(
        self,
    ) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"],
    ):
        self.node.data_type = value


class Mix(NodeBuilder):
    """
    Mix values by a factor
    """

    _bl_idname = "ShaderNodeMix"
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
        data_type: Literal["FLOAT", "VECTOR", "RGBA"] = "FLOAT",
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
    def data_type(self) -> Literal["FLOAT", "VECTOR", "RGBA"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "VECTOR", "RGBA"]):
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


class RgbToBw(NodeBuilder):
    """
    Convert RGB input into grayscale using luminance
    """

    _bl_idname = "CompositorNodeRGBToBW"
    node: bpy.types.CompositorNodeRGBToBW

    def __init__(self, image: TYPE_INPUT_COLOR = None):
        super().__init__()
        key_args = {"Image": image}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def o_val(self) -> SocketLinker:
        """Output socket: Val"""
        return self._output("Val")


class RelativeToPixel(NodeBuilder):
    """
    Converts values that are relative to the image size to be in terms of pixels
    """

    _bl_idname = "CompositorNodeRelativeToPixel"
    node: bpy.types.CompositorNodeRelativeToPixel

    def __init__(
        self,
        vector_value: TYPE_INPUT_VECTOR = None,
        float_value: TYPE_INPUT_VALUE = 0.0,
        image: TYPE_INPUT_COLOR = None,
        *,
        data_type: Literal["FLOAT", "VECTOR"] = "FLOAT",
        reference_dimension: Literal[
            "PER_DIMENSION", "X", "Y", "Greater", "Smaller", "Diagonal"
        ] = "X",
    ):
        super().__init__()
        key_args = {
            "Vector Value": vector_value,
            "Float Value": float_value,
            "Image": image,
        }
        self.data_type = data_type
        self.reference_dimension = reference_dimension
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, float_value: TYPE_INPUT_VALUE = 0.0, image: TYPE_INPUT_COLOR = None
    ) -> "RelativeToPixel":
        """Create Relative To Pixel with operation 'Float'."""
        return cls(data_type="FLOAT", float_value=float_value, image=image)

    @classmethod
    def vector(
        cls, vector_value: TYPE_INPUT_VECTOR = None, image: TYPE_INPUT_COLOR = None
    ) -> "RelativeToPixel":
        """Create Relative To Pixel with operation 'Vector'."""
        return cls(data_type="VECTOR", vector_value=vector_value, image=image)

    @property
    def i_vector_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Vector Value")

    @property
    def i_float_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Float Value")

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def o_float_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Float Value")

    @property
    def o_vector_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Vector Value")

    @property
    def data_type(self) -> Literal["FLOAT", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "VECTOR"]):
        self.node.data_type = value

    @property
    def reference_dimension(
        self,
    ) -> Literal["PER_DIMENSION", "X", "Y", "Greater", "Smaller", "Diagonal"]:
        return self.node.reference_dimension

    @reference_dimension.setter
    def reference_dimension(
        self,
        value: Literal["PER_DIMENSION", "X", "Y", "Greater", "Smaller", "Diagonal"],
    ):
        self.node.reference_dimension = value


class SeparateColor(NodeBuilder):
    """
    Split an image into its composite color channels
    """

    _bl_idname = "CompositorNodeSeparateColor"
    node: bpy.types.CompositorNodeSeparateColor

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        *,
        mode: Literal["RGB", "HSV", "HSL", "YCC", "YUV"] = "RGB",
        ycc_mode: Literal["ITUBT601", "ITUBT709", "JFIF"] = "ITUBT709",
    ):
        super().__init__()
        key_args = {"Image": image}
        self.mode = mode
        self.ycc_mode = ycc_mode
        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

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
    def mode(self) -> Literal["RGB", "HSV", "HSL", "YCC", "YUV"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["RGB", "HSV", "HSL", "YCC", "YUV"]):
        self.node.mode = value

    @property
    def ycc_mode(self) -> Literal["ITUBT601", "ITUBT709", "JFIF"]:
        return self.node.ycc_mode

    @ycc_mode.setter
    def ycc_mode(self, value: Literal["ITUBT601", "ITUBT709", "JFIF"]):
        self.node.ycc_mode = value


class SeparateXYZ(NodeBuilder):
    """
    Split a vector into its X, Y, and Z components
    """

    _bl_idname = "ShaderNodeSeparateXYZ"
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


class SetAlpha(NodeBuilder):
    """
    Add an alpha channel to an image
    """

    _bl_idname = "CompositorNodeSetAlpha"
    node: bpy.types.CompositorNodeSetAlpha

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        alpha: TYPE_INPUT_VALUE = 1.0,
        type: TYPE_INPUT_MENU = "Apply Mask",
    ):
        super().__init__()
        key_args = {"Image": image, "Alpha": alpha, "Type": type}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_alpha(self) -> SocketLinker:
        """Input socket: Alpha"""
        return self._input("Alpha")

    @property
    def i_type(self) -> SocketLinker:
        """Input socket: Type"""
        return self._input("Type")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class Split(NodeBuilder):
    """
    Combine two images for side-by-side display. Typically used in combination with a Viewer node
    """

    _bl_idname = "CompositorNodeSplit"
    node: bpy.types.CompositorNodeSplit

    def __init__(
        self,
        position: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_VALUE = 0.7854,
        image: TYPE_INPUT_COLOR = None,
        image_001: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {
            "Position": position,
            "Rotation": rotation,
            "Image": image,
            "Image_001": image_001,
        }

        self._establish_links(**key_args)

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_image_001(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image_001")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class Switch(NodeBuilder):
    """
    Switch between two images using a checkbox
    """

    _bl_idname = "CompositorNodeSwitch"
    node: bpy.types.CompositorNodeSwitch

    def __init__(
        self,
        switch: TYPE_INPUT_BOOLEAN = False,
        off: TYPE_INPUT_COLOR = None,
        on: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {"Switch": switch, "Off": off, "On": on}

        self._establish_links(**key_args)

    @property
    def i_switch(self) -> SocketLinker:
        """Input socket: Switch"""
        return self._input("Switch")

    @property
    def i_off(self) -> SocketLinker:
        """Input socket: Off"""
        return self._input("Off")

    @property
    def i_on(self) -> SocketLinker:
        """Input socket: On"""
        return self._input("On")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class SwitchView(NodeBuilder):
    """
    Combine the views (left and right) into a single stereo 3D output
    """

    _bl_idname = "CompositorNodeSwitchView"
    node: bpy.types.CompositorNodeSwitchView

    def __init__(
        self,
        left: TYPE_INPUT_COLOR = None,
        right: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {"left": left, "right": right}

        self._establish_links(**key_args)

    @property
    def i_left(self) -> SocketLinker:
        """Input socket: left"""
        return self._input("left")

    @property
    def i_right(self) -> SocketLinker:
        """Input socket: right"""
        return self._input("right")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")
