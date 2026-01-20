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


class DialGizmo(NodeBuilder):
    """Show a dial gizmo in the viewport for a value"""

    name = "GeometryNodeGizmoDial"
    node: bpy.types.GeometryNodeGizmoDial

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = None,
        up: TYPE_INPUT_VECTOR = None,
        screen_space: TYPE_INPUT_BOOLEAN = True,
        radius: TYPE_INPUT_VALUE = 1.0,
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
    ):
        super().__init__()
        key_args = {
            "Value": value,
            "Position": position,
            "Up": up,
            "Screen Space": screen_space,
            "Radius": radius,
        }
        self.color_id = color_id
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_up(self) -> SocketLinker:
        """Input socket: Up"""
        return self._input("Up")

    @property
    def i_screen_space(self) -> SocketLinker:
        """Input socket: Screen Space"""
        return self._input("Screen Space")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def color_id(self) -> Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]:
        return self.node.color_id

    @color_id.setter
    def color_id(self, value: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]):
        self.node.color_id = value


class EnableOutput(NodeBuilder):
    """Either pass through the input value or output the fallback value"""

    name = "NodeEnableOutput"
    node: bpy.types.Node

    def __init__(
        self,
        enable: TYPE_INPUT_BOOLEAN = False,
        value: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
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
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Enable": enable, "Value": value}
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_enable(self) -> SocketLinker:
        """Input socket: Enable"""
        return self._input("Enable")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(
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
        return self.node.data_type

    @data_type.setter
    def data_type(
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
        self.node.data_type = value


class ForEachGeometryElementInput(NodeBuilder):
    """For Each Geometry Element Input node"""

    name = "GeometryNodeForeachGeometryElementInput"
    node: bpy.types.GeometryNodeForeachGeometryElementInput

    def __init__(
        self,
        geometry: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        extend: None = None,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "__extend__": extend}

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_element(self) -> SocketLinker:
        """Output socket: Element"""
        return self._output("Element")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__")


class ForEachGeometryElementOutput(NodeBuilder):
    """For Each Geometry Element Output node"""

    name = "GeometryNodeForeachGeometryElementOutput"
    node: bpy.types.GeometryNodeForeachGeometryElementOutput

    def __init__(
        self,
        extend_main: None = None,
        generation_0: TYPE_INPUT_GEOMETRY = None,
        extend_generation: None = None,
        active_input_index: int = 0,
        active_generation_index: int = 0,
        active_main_index: int = 0,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        inspection_index: int = 0,
    ):
        super().__init__()
        key_args = {
            "__extend__main": extend_main,
            "Generation_0": generation_0,
            "__extend__generation": extend_generation,
        }
        self.active_input_index = active_input_index
        self.active_generation_index = active_generation_index
        self.active_main_index = active_main_index
        self.domain = domain
        self.inspection_index = inspection_index
        self._establish_links(**key_args)

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__main")

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Generation_0")

    @property
    def i_extend_generation(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__generation")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__main")

    @property
    def o_generation_0(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Generation_0")

    @property
    def o_extend_generation(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__generation")

    @property
    def active_input_index(self) -> int:
        return self.node.active_input_index

    @active_input_index.setter
    def active_input_index(self, value: int):
        self.node.active_input_index = value

    @property
    def active_generation_index(self) -> int:
        return self.node.active_generation_index

    @active_generation_index.setter
    def active_generation_index(self, value: int):
        self.node.active_generation_index = value

    @property
    def active_main_index(self) -> int:
        return self.node.active_main_index

    @active_main_index.setter
    def active_main_index(self, value: int):
        self.node.active_main_index = value

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
    def inspection_index(self) -> int:
        return self.node.inspection_index

    @inspection_index.setter
    def inspection_index(self, value: int):
        self.node.inspection_index = value


class GroupInput(NodeBuilder):
    """Expose connected data from inside a node group as inputs to its interface"""

    name = "NodeGroupInput"
    node: bpy.types.Node

    def __init__(self):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__")


class GroupOutput(NodeBuilder):
    """Output data from inside of a node group"""

    name = "NodeGroupOutput"
    node: bpy.types.Node

    def __init__(
        self,
        extend: None = None,
        is_active_output: bool = False,
    ):
        super().__init__()
        key_args = {"__extend__": extend}
        self.is_active_output = is_active_output
        self._establish_links(**key_args)

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def is_active_output(self) -> bool:
        return self.node.is_active_output

    @is_active_output.setter
    def is_active_output(self, value: bool):
        self.node.is_active_output = value


class LinearGizmo(NodeBuilder):
    """Show a linear gizmo in the viewport for a value"""

    name = "GeometryNodeGizmoLinear"
    node: bpy.types.GeometryNodeGizmoLinear

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = None,
        direction: TYPE_INPUT_VECTOR = None,
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
        draw_style: Literal["ARROW", "CROSS", "BOX"] = "ARROW",
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Direction": direction}
        self.color_id = color_id
        self.draw_style = draw_style
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_direction(self) -> SocketLinker:
        """Input socket: Direction"""
        return self._input("Direction")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def color_id(self) -> Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]:
        return self.node.color_id

    @color_id.setter
    def color_id(self, value: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]):
        self.node.color_id = value

    @property
    def draw_style(self) -> Literal["ARROW", "CROSS", "BOX"]:
        return self.node.draw_style

    @draw_style.setter
    def draw_style(self, value: Literal["ARROW", "CROSS", "BOX"]):
        self.node.draw_style = value


class TransformGizmo(NodeBuilder):
    """Show a transform gizmo in the viewport"""

    name = "GeometryNodeGizmoTransform"
    node: bpy.types.GeometryNodeGizmoTransform

    def __init__(
        self,
        value: TYPE_INPUT_MATRIX = None,
        position: TYPE_INPUT_VECTOR = None,
        rotation: TYPE_INPUT_ROTATION = None,
        use_translation_x: bool = False,
        use_translation_y: bool = False,
        use_translation_z: bool = False,
        use_rotation_x: bool = False,
        use_rotation_y: bool = False,
        use_rotation_z: bool = False,
        use_scale_x: bool = False,
        use_scale_y: bool = False,
        use_scale_z: bool = False,
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Rotation": rotation}
        self.use_translation_x = use_translation_x
        self.use_translation_y = use_translation_y
        self.use_translation_z = use_translation_z
        self.use_rotation_x = use_rotation_x
        self.use_rotation_y = use_rotation_y
        self.use_rotation_z = use_rotation_z
        self.use_scale_x = use_scale_x
        self.use_scale_y = use_scale_y
        self.use_scale_z = use_scale_z
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def use_translation_x(self) -> bool:
        return self.node.use_translation_x

    @use_translation_x.setter
    def use_translation_x(self, value: bool):
        self.node.use_translation_x = value

    @property
    def use_translation_y(self) -> bool:
        return self.node.use_translation_y

    @use_translation_y.setter
    def use_translation_y(self, value: bool):
        self.node.use_translation_y = value

    @property
    def use_translation_z(self) -> bool:
        return self.node.use_translation_z

    @use_translation_z.setter
    def use_translation_z(self, value: bool):
        self.node.use_translation_z = value

    @property
    def use_rotation_x(self) -> bool:
        return self.node.use_rotation_x

    @use_rotation_x.setter
    def use_rotation_x(self, value: bool):
        self.node.use_rotation_x = value

    @property
    def use_rotation_y(self) -> bool:
        return self.node.use_rotation_y

    @use_rotation_y.setter
    def use_rotation_y(self, value: bool):
        self.node.use_rotation_y = value

    @property
    def use_rotation_z(self) -> bool:
        return self.node.use_rotation_z

    @use_rotation_z.setter
    def use_rotation_z(self, value: bool):
        self.node.use_rotation_z = value

    @property
    def use_scale_x(self) -> bool:
        return self.node.use_scale_x

    @use_scale_x.setter
    def use_scale_x(self, value: bool):
        self.node.use_scale_x = value

    @property
    def use_scale_y(self) -> bool:
        return self.node.use_scale_y

    @use_scale_y.setter
    def use_scale_y(self, value: bool):
        self.node.use_scale_y = value

    @property
    def use_scale_z(self) -> bool:
        return self.node.use_scale_z

    @use_scale_z.setter
    def use_scale_z(self, value: bool):
        self.node.use_scale_z = value


class Warning(NodeBuilder):
    """Create custom warnings in node groups"""

    name = "GeometryNodeWarning"
    node: bpy.types.GeometryNodeWarning

    def __init__(
        self,
        show: TYPE_INPUT_BOOLEAN = True,
        message: TYPE_INPUT_STRING = "",
        warning_type: Literal["ERROR", "WARNING", "INFO"] = "ERROR",
    ):
        super().__init__()
        key_args = {"Show": show, "Message": message}
        self.warning_type = warning_type
        self._establish_links(**key_args)

    @property
    def i_show(self) -> SocketLinker:
        """Input socket: Show"""
        return self._input("Show")

    @property
    def i_message(self) -> SocketLinker:
        """Input socket: Message"""
        return self._input("Message")

    @property
    def o_show(self) -> SocketLinker:
        """Output socket: Show"""
        return self._output("Show")

    @property
    def warning_type(self) -> Literal["ERROR", "WARNING", "INFO"]:
        return self.node.warning_type

    @warning_type.setter
    def warning_type(self, value: Literal["ERROR", "WARNING", "INFO"]):
        self.node.warning_type = value
