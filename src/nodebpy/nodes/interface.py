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
        *,
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
        *,
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


class GroupInput(NodeBuilder):
    """Expose connected data from inside a node group as inputs to its interface"""

    name = "NodeGroupInput"
    node: bpy.types.Node

    def __init__(self):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)


class GroupOutput(NodeBuilder):
    """Output data from inside of a node group"""

    name = "NodeGroupOutput"
    node: bpy.types.Node

    def __init__(self, is_active_output: bool = False):
        super().__init__()
        key_args = kwargs
        self.is_active_output = is_active_output
        self._establish_links(**key_args)

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
        *,
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
        *,
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
        *,
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
