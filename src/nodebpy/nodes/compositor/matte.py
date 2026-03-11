from typing import Literal

import bpy

from ...builder import NodeBuilder, SocketLinker
from ...types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class BoxMask(NodeBuilder):
    """
    Create rectangular mask suitable for use as a simple matte
    """

    _bl_idname = "CompositorNodeBoxMask"
    node: bpy.types.CompositorNodeBoxMask

    def __init__(
        self,
        operation: TYPE_INPUT_MENU = "Add",
        mask: TYPE_INPUT_VALUE = 0.0,
        value: TYPE_INPUT_VALUE = 1.0,
        position: TYPE_INPUT_VECTOR = None,
        size: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Operation": operation,
            "Mask": mask,
            "Value": value,
            "Position": position,
            "Size": size,
            "Rotation": rotation,
        }

        self._establish_links(**key_args)

    @property
    def i_operation(self) -> SocketLinker:
        """Input socket: Operation"""
        return self._input("Operation")

    @property
    def i_mask(self) -> SocketLinker:
        """Input socket: Mask"""
        return self._input("Mask")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_size(self) -> SocketLinker:
        """Input socket: Size"""
        return self._input("Size")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_mask(self) -> SocketLinker:
        """Output socket: Mask"""
        return self._output("Mask")


class ChannelKey(NodeBuilder):
    """
    Create matte based on differences in color channels
    """

    _bl_idname = "CompositorNodeChannelMatte"
    node: bpy.types.CompositorNodeChannelMatte

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        minimum: TYPE_INPUT_VALUE = 0.0,
        maximum: TYPE_INPUT_VALUE = 1.0,
        color_space: TYPE_INPUT_MENU = "RGB",
        rgb_key_channel: TYPE_INPUT_MENU = "G",
        hsv_key_channel: TYPE_INPUT_MENU = "H",
        yuv_key_channel: TYPE_INPUT_MENU = "V",
        ycbcr_key_channel: TYPE_INPUT_MENU = "Cr",
        limit_method: TYPE_INPUT_MENU = "Max",
        rgb_limit_channel: TYPE_INPUT_MENU = "R",
        hsv_limit_channel: TYPE_INPUT_MENU = "S",
        yuv_limit_channel: TYPE_INPUT_MENU = "U",
        ycbcr_limit_channel: TYPE_INPUT_MENU = "Cb",
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Minimum": minimum,
            "Maximum": maximum,
            "Color Space": color_space,
            "RGB Key Channel": rgb_key_channel,
            "HSV Key Channel": hsv_key_channel,
            "YUV Key Channel": yuv_key_channel,
            "YCbCr Key Channel": ycbcr_key_channel,
            "Limit Method": limit_method,
            "RGB Limit Channel": rgb_limit_channel,
            "HSV Limit Channel": hsv_limit_channel,
            "YUV Limit Channel": yuv_limit_channel,
            "YCbCr Limit Channel": ycbcr_limit_channel,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_minimum(self) -> SocketLinker:
        """Input socket: Minimum"""
        return self._input("Minimum")

    @property
    def i_maximum(self) -> SocketLinker:
        """Input socket: Maximum"""
        return self._input("Maximum")

    @property
    def i_color_space(self) -> SocketLinker:
        """Input socket: Color Space"""
        return self._input("Color Space")

    @property
    def i_rgb_key_channel(self) -> SocketLinker:
        """Input socket: RGB Key Channel"""
        return self._input("RGB Key Channel")

    @property
    def i_hsv_key_channel(self) -> SocketLinker:
        """Input socket: HSV Key Channel"""
        return self._input("HSV Key Channel")

    @property
    def i_yuv_key_channel(self) -> SocketLinker:
        """Input socket: YUV Key Channel"""
        return self._input("YUV Key Channel")

    @property
    def i_ycbcr_key_channel(self) -> SocketLinker:
        """Input socket: YCbCr Key Channel"""
        return self._input("YCbCr Key Channel")

    @property
    def i_limit_method(self) -> SocketLinker:
        """Input socket: Limit Method"""
        return self._input("Limit Method")

    @property
    def i_rgb_limit_channel(self) -> SocketLinker:
        """Input socket: RGB Limit Channel"""
        return self._input("RGB Limit Channel")

    @property
    def i_hsv_limit_channel(self) -> SocketLinker:
        """Input socket: HSV Limit Channel"""
        return self._input("HSV Limit Channel")

    @property
    def i_yuv_limit_channel(self) -> SocketLinker:
        """Input socket: YUV Limit Channel"""
        return self._input("YUV Limit Channel")

    @property
    def i_ycbcr_limit_channel(self) -> SocketLinker:
        """Input socket: YCbCr Limit Channel"""
        return self._input("YCbCr Limit Channel")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")


class ChromaKey(NodeBuilder):
    """
    Create matte based on chroma values
    """

    _bl_idname = "CompositorNodeChromaMatte"
    node: bpy.types.CompositorNodeChromaMatte

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        key_color: TYPE_INPUT_COLOR = None,
        minimum: TYPE_INPUT_VALUE = 0.1745,
        maximum: TYPE_INPUT_VALUE = 0.5236,
        falloff: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Key Color": key_color,
            "Minimum": minimum,
            "Maximum": maximum,
            "Falloff": falloff,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_key_color(self) -> SocketLinker:
        """Input socket: Key Color"""
        return self._input("Key Color")

    @property
    def i_minimum(self) -> SocketLinker:
        """Input socket: Minimum"""
        return self._input("Minimum")

    @property
    def i_maximum(self) -> SocketLinker:
        """Input socket: Maximum"""
        return self._input("Maximum")

    @property
    def i_falloff(self) -> SocketLinker:
        """Input socket: Falloff"""
        return self._input("Falloff")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")


class ColorKey(NodeBuilder):
    """
    Create matte using a given color, for green or blue screen footage
    """

    _bl_idname = "CompositorNodeColorMatte"
    node: bpy.types.CompositorNodeColorMatte

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        key_color: TYPE_INPUT_COLOR = None,
        hue: TYPE_INPUT_VALUE = 0.01,
        saturation: TYPE_INPUT_VALUE = 0.1,
        value: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Key Color": key_color,
            "Hue": hue,
            "Saturation": saturation,
            "Value": value,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_key_color(self) -> SocketLinker:
        """Input socket: Key Color"""
        return self._input("Key Color")

    @property
    def i_hue(self) -> SocketLinker:
        """Input socket: Hue"""
        return self._input("Hue")

    @property
    def i_saturation(self) -> SocketLinker:
        """Input socket: Saturation"""
        return self._input("Saturation")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")


class ColorSpill(NodeBuilder):
    """
    Remove colors from a blue or green screen, by reducing one RGB channel compared to the others
    """

    _bl_idname = "CompositorNodeColorSpill"
    node: bpy.types.CompositorNodeColorSpill

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        fac: TYPE_INPUT_VALUE = 1.0,
        spill_channel: TYPE_INPUT_MENU = "G",
        limit_method: TYPE_INPUT_MENU = "Single",
        limit_channel: TYPE_INPUT_MENU = "R",
        limit_strength: TYPE_INPUT_VALUE = 1.0,
        use_spill_strength: TYPE_INPUT_BOOLEAN = False,
        spill_strength: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Fac": fac,
            "Spill Channel": spill_channel,
            "Limit Method": limit_method,
            "Limit Channel": limit_channel,
            "Limit Strength": limit_strength,
            "Use Spill Strength": use_spill_strength,
            "Spill Strength": spill_strength,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_fac(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Fac")

    @property
    def i_spill_channel(self) -> SocketLinker:
        """Input socket: Spill Channel"""
        return self._input("Spill Channel")

    @property
    def i_limit_method(self) -> SocketLinker:
        """Input socket: Limit Method"""
        return self._input("Limit Method")

    @property
    def i_limit_channel(self) -> SocketLinker:
        """Input socket: Limit Channel"""
        return self._input("Limit Channel")

    @property
    def i_limit_strength(self) -> SocketLinker:
        """Input socket: Limit Strength"""
        return self._input("Limit Strength")

    @property
    def i_use_spill_strength(self) -> SocketLinker:
        """Input socket: Use Spill Strength"""
        return self._input("Use Spill Strength")

    @property
    def i_spill_strength(self) -> SocketLinker:
        """Input socket: Strength"""
        return self._input("Spill Strength")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")


class Cryptomatte(NodeBuilder):
    """
    Generate matte for individual objects and materials using Cryptomatte render passes
    """

    _bl_idname = "CompositorNodeCryptomatteV2"
    node: bpy.types.CompositorNodeCryptomatteV2

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        *,
        source: Literal["RENDER", "IMAGE"] = "RENDER",
        matte_id: str = "",
        add: tuple[float, float, float, float] = (0.735, 0.735, 0.735, 1.0),
        remove: tuple[float, float, float, float] = (0.735, 0.735, 0.735, 1.0),
        layer_name: str = "",
        frame_duration: int = 0,
        frame_start: int = 0,
        frame_offset: int = 0,
        use_cyclic: bool = False,
        use_auto_refresh: bool = False,
        layer: str = "",
        has_layers: bool = False,
        view: str = "",
        has_views: bool = False,
    ):
        super().__init__()
        key_args = {"Image": image}
        self.source = source
        self.matte_id = matte_id
        self.add = add
        self.remove = remove
        self.layer_name = layer_name
        self.frame_duration = frame_duration
        self.frame_start = frame_start
        self.frame_offset = frame_offset
        self.use_cyclic = use_cyclic
        self.use_auto_refresh = use_auto_refresh
        self.layer = layer
        self.has_layers = has_layers
        self.view = view
        self.has_views = has_views
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
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")

    @property
    def o_pick(self) -> SocketLinker:
        """Output socket: Pick"""
        return self._output("Pick")

    @property
    def source(self) -> Literal["RENDER", "IMAGE"]:
        return self.node.source

    @source.setter
    def source(self, value: Literal["RENDER", "IMAGE"]):
        self.node.source = value

    @property
    def matte_id(self) -> str:
        return self.node.matte_id

    @matte_id.setter
    def matte_id(self, value: str):
        self.node.matte_id = value

    @property
    def add(self) -> tuple[float, float, float, float]:
        return self.node.add

    @add.setter
    def add(self, value: tuple[float, float, float, float]):
        self.node.add = value

    @property
    def remove(self) -> tuple[float, float, float, float]:
        return self.node.remove

    @remove.setter
    def remove(self, value: tuple[float, float, float, float]):
        self.node.remove = value

    @property
    def layer_name(self) -> str:
        return self.node.layer_name

    @layer_name.setter
    def layer_name(self, value: str):
        self.node.layer_name = value

    @property
    def frame_duration(self) -> int:
        return self.node.frame_duration

    @frame_duration.setter
    def frame_duration(self, value: int):
        self.node.frame_duration = value

    @property
    def frame_start(self) -> int:
        return self.node.frame_start

    @frame_start.setter
    def frame_start(self, value: int):
        self.node.frame_start = value

    @property
    def frame_offset(self) -> int:
        return self.node.frame_offset

    @frame_offset.setter
    def frame_offset(self, value: int):
        self.node.frame_offset = value

    @property
    def use_cyclic(self) -> bool:
        return self.node.use_cyclic

    @use_cyclic.setter
    def use_cyclic(self, value: bool):
        self.node.use_cyclic = value

    @property
    def use_auto_refresh(self) -> bool:
        return self.node.use_auto_refresh

    @use_auto_refresh.setter
    def use_auto_refresh(self, value: bool):
        self.node.use_auto_refresh = value

    @property
    def layer(self) -> str:
        return self.node.layer

    @layer.setter
    def layer(self, value: str):
        self.node.layer = value

    @property
    def has_layers(self) -> bool:
        return self.node.has_layers

    @has_layers.setter
    def has_layers(self, value: bool):
        self.node.has_layers = value

    @property
    def view(self) -> str:
        return self.node.view

    @view.setter
    def view(self, value: str):
        self.node.view = value

    @property
    def has_views(self) -> bool:
        return self.node.has_views

    @has_views.setter
    def has_views(self, value: bool):
        self.node.has_views = value


class DifferenceKey(NodeBuilder):
    """
    Produce a matte that isolates foreground content by comparing it with a reference background image
    """

    _bl_idname = "CompositorNodeDiffMatte"
    node: bpy.types.CompositorNodeDiffMatte

    def __init__(
        self,
        image_1: TYPE_INPUT_COLOR = None,
        image_2: TYPE_INPUT_COLOR = None,
        tolerance: TYPE_INPUT_VALUE = 0.1,
        falloff: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {
            "Image 1": image_1,
            "Image 2": image_2,
            "Tolerance": tolerance,
            "Falloff": falloff,
        }

        self._establish_links(**key_args)

    @property
    def i_image_1(self) -> SocketLinker:
        """Input socket: Image 1"""
        return self._input("Image 1")

    @property
    def i_image_2(self) -> SocketLinker:
        """Input socket: Image 2"""
        return self._input("Image 2")

    @property
    def i_tolerance(self) -> SocketLinker:
        """Input socket: Tolerance"""
        return self._input("Tolerance")

    @property
    def i_falloff(self) -> SocketLinker:
        """Input socket: Falloff"""
        return self._input("Falloff")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")


class DistanceKey(NodeBuilder):
    """
    Create matte based on 3D distance between colors
    """

    _bl_idname = "CompositorNodeDistanceMatte"
    node: bpy.types.CompositorNodeDistanceMatte

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        key_color: TYPE_INPUT_COLOR = None,
        color_space: TYPE_INPUT_MENU = "RGB",
        tolerance: TYPE_INPUT_VALUE = 0.1,
        falloff: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Key Color": key_color,
            "Color Space": color_space,
            "Tolerance": tolerance,
            "Falloff": falloff,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_key_color(self) -> SocketLinker:
        """Input socket: Key Color"""
        return self._input("Key Color")

    @property
    def i_color_space(self) -> SocketLinker:
        """Input socket: Color Space"""
        return self._input("Color Space")

    @property
    def i_tolerance(self) -> SocketLinker:
        """Input socket: Tolerance"""
        return self._input("Tolerance")

    @property
    def i_falloff(self) -> SocketLinker:
        """Input socket: Falloff"""
        return self._input("Falloff")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")


class DoubleEdgeMask(NodeBuilder):
    """
    Create a gradient between two masks
    """

    _bl_idname = "CompositorNodeDoubleEdgeMask"
    node: bpy.types.CompositorNodeDoubleEdgeMask

    def __init__(
        self,
        outer_mask: TYPE_INPUT_VALUE = 0.8,
        inner_mask: TYPE_INPUT_VALUE = 0.8,
        image_edges: TYPE_INPUT_BOOLEAN = False,
        only_inside_outer: TYPE_INPUT_BOOLEAN = False,
    ):
        super().__init__()
        key_args = {
            "Outer Mask": outer_mask,
            "Inner Mask": inner_mask,
            "Image Edges": image_edges,
            "Only Inside Outer": only_inside_outer,
        }

        self._establish_links(**key_args)

    @property
    def i_outer_mask(self) -> SocketLinker:
        """Input socket: Outer Mask"""
        return self._input("Outer Mask")

    @property
    def i_inner_mask(self) -> SocketLinker:
        """Input socket: Inner Mask"""
        return self._input("Inner Mask")

    @property
    def i_image_edges(self) -> SocketLinker:
        """Input socket: Image Edges"""
        return self._input("Image Edges")

    @property
    def i_only_inside_outer(self) -> SocketLinker:
        """Input socket: Only Inside Outer"""
        return self._input("Only Inside Outer")

    @property
    def o_mask(self) -> SocketLinker:
        """Output socket: Mask"""
        return self._output("Mask")


class EllipseMask(NodeBuilder):
    """
    Create elliptical mask suitable for use as a simple matte or vignette mask
    """

    _bl_idname = "CompositorNodeEllipseMask"
    node: bpy.types.CompositorNodeEllipseMask

    def __init__(
        self,
        operation: TYPE_INPUT_MENU = "Add",
        mask: TYPE_INPUT_VALUE = 0.0,
        value: TYPE_INPUT_VALUE = 1.0,
        position: TYPE_INPUT_VECTOR = None,
        size: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Operation": operation,
            "Mask": mask,
            "Value": value,
            "Position": position,
            "Size": size,
            "Rotation": rotation,
        }

        self._establish_links(**key_args)

    @property
    def i_operation(self) -> SocketLinker:
        """Input socket: Operation"""
        return self._input("Operation")

    @property
    def i_mask(self) -> SocketLinker:
        """Input socket: Mask"""
        return self._input("Mask")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_size(self) -> SocketLinker:
        """Input socket: Size"""
        return self._input("Size")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_mask(self) -> SocketLinker:
        """Output socket: Mask"""
        return self._output("Mask")


class Keying(NodeBuilder):
    """
    Perform both chroma keying (to remove the backdrop) and despill (to correct color cast from the backdrop)
    """

    _bl_idname = "CompositorNodeKeying"
    node: bpy.types.CompositorNodeKeying

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        key_color: TYPE_INPUT_COLOR = None,
        preprocess_blur_size: TYPE_INPUT_INT = 0,
        key_balance: TYPE_INPUT_VALUE = 0.5,
        black_level: TYPE_INPUT_VALUE = 0.0,
        white_level: TYPE_INPUT_VALUE = 1.0,
        edge_search_size: TYPE_INPUT_INT = 3,
        edge_tolerance: TYPE_INPUT_VALUE = 0.1,
        garbage_matte: TYPE_INPUT_VALUE = 0.0,
        core_matte: TYPE_INPUT_VALUE = 0.0,
        postprocess_blur_size: TYPE_INPUT_INT = 0,
        postprocess_dilate_size: TYPE_INPUT_INT = 0,
        postprocess_feather_size: TYPE_INPUT_INT = 0,
        feather_falloff: TYPE_INPUT_MENU = "Smooth",
        despill_strength: TYPE_INPUT_VALUE = 1.0,
        despill_balance: TYPE_INPUT_VALUE = 0.5,
    ):
        super().__init__()
        key_args = {
            "Image": image,
            "Key Color": key_color,
            "Preprocess Blur Size": preprocess_blur_size,
            "Key Balance": key_balance,
            "Black Level": black_level,
            "White Level": white_level,
            "Edge Search Size": edge_search_size,
            "Edge Tolerance": edge_tolerance,
            "Garbage Matte": garbage_matte,
            "Core Matte": core_matte,
            "Postprocess Blur Size": postprocess_blur_size,
            "Postprocess Dilate Size": postprocess_dilate_size,
            "Postprocess Feather Size": postprocess_feather_size,
            "Feather Falloff": feather_falloff,
            "Despill Strength": despill_strength,
            "Despill Balance": despill_balance,
        }

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_key_color(self) -> SocketLinker:
        """Input socket: Key Color"""
        return self._input("Key Color")

    @property
    def i_preprocess_blur_size(self) -> SocketLinker:
        """Input socket: Blur Size"""
        return self._input("Preprocess Blur Size")

    @property
    def i_key_balance(self) -> SocketLinker:
        """Input socket: Balance"""
        return self._input("Key Balance")

    @property
    def i_black_level(self) -> SocketLinker:
        """Input socket: Black Level"""
        return self._input("Black Level")

    @property
    def i_white_level(self) -> SocketLinker:
        """Input socket: White Level"""
        return self._input("White Level")

    @property
    def i_edge_search_size(self) -> SocketLinker:
        """Input socket: Size"""
        return self._input("Edge Search Size")

    @property
    def i_edge_tolerance(self) -> SocketLinker:
        """Input socket: Tolerance"""
        return self._input("Edge Tolerance")

    @property
    def i_garbage_matte(self) -> SocketLinker:
        """Input socket: Garbage Matte"""
        return self._input("Garbage Matte")

    @property
    def i_core_matte(self) -> SocketLinker:
        """Input socket: Core Matte"""
        return self._input("Core Matte")

    @property
    def i_postprocess_blur_size(self) -> SocketLinker:
        """Input socket: Blur Size"""
        return self._input("Postprocess Blur Size")

    @property
    def i_postprocess_dilate_size(self) -> SocketLinker:
        """Input socket: Dilate Size"""
        return self._input("Postprocess Dilate Size")

    @property
    def i_postprocess_feather_size(self) -> SocketLinker:
        """Input socket: Feather Size"""
        return self._input("Postprocess Feather Size")

    @property
    def i_feather_falloff(self) -> SocketLinker:
        """Input socket: Feather Falloff"""
        return self._input("Feather Falloff")

    @property
    def i_despill_strength(self) -> SocketLinker:
        """Input socket: Strength"""
        return self._input("Despill Strength")

    @property
    def i_despill_balance(self) -> SocketLinker:
        """Input socket: Balance"""
        return self._input("Despill Balance")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")

    @property
    def o_edges(self) -> SocketLinker:
        """Output socket: Edges"""
        return self._output("Edges")


class KeyingScreen(NodeBuilder):
    """
    Create plates for use as a color reference for keying nodes
    """

    _bl_idname = "CompositorNodeKeyingScreen"
    node: bpy.types.CompositorNodeKeyingScreen

    def __init__(
        self,
        smoothness: TYPE_INPUT_VALUE = 0.0,
        *,
        tracking_object: str = "",
    ):
        super().__init__()
        key_args = {"Smoothness": smoothness}
        self.tracking_object = tracking_object
        self._establish_links(**key_args)

    @property
    def i_smoothness(self) -> SocketLinker:
        """Input socket: Smoothness"""
        return self._input("Smoothness")

    @property
    def o_screen(self) -> SocketLinker:
        """Output socket: Screen"""
        return self._output("Screen")

    @property
    def tracking_object(self) -> str:
        return self.node.tracking_object

    @tracking_object.setter
    def tracking_object(self, value: str):
        self.node.tracking_object = value


class LuminanceKey(NodeBuilder):
    """
    Create a matte based on luminance (brightness) difference
    """

    _bl_idname = "CompositorNodeLumaMatte"
    node: bpy.types.CompositorNodeLumaMatte

    def __init__(
        self,
        image: TYPE_INPUT_COLOR = None,
        minimum: TYPE_INPUT_VALUE = 0.0,
        maximum: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"Image": image, "Minimum": minimum, "Maximum": maximum}

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_minimum(self) -> SocketLinker:
        """Input socket: Minimum"""
        return self._input("Minimum")

    @property
    def i_maximum(self) -> SocketLinker:
        """Input socket: Maximum"""
        return self._input("Maximum")

    @property
    def o_image(self) -> SocketLinker:
        """Output socket: Image"""
        return self._output("Image")

    @property
    def o_matte(self) -> SocketLinker:
        """Output socket: Matte"""
        return self._output("Matte")
