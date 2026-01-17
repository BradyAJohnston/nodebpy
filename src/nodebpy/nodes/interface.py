from typing import Literal

import bpy
from typing_extensions import Literal

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_ROTATION,
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
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        up: TYPE_INPUT_VECTOR = (0.0, 0.0, 1.0),
        screen_space: TYPE_INPUT_BOOLEAN = True,
        radius: TYPE_INPUT_VALUE = 1.0,
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
        pin_gizmo: bool = False,
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
        self.pin_gizmo = pin_gizmo
        self._establish_links(**key_args)

    @property
    def pin_gizmo(self) -> bool:
        """Pin the gizmo to the viewport"""
        return self.node.inputs[0].pin_gizmo

    @pin_gizmo.setter
    def pin_gizmo(self, value: bool):
        self.node.inputs[0].pin_gizmo = value

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


class LinearGizmo(NodeBuilder):
    """Show a linear gizmo in the viewport for a value"""

    name = "GeometryNodeGizmoLinear"
    node: bpy.types.GeometryNodeGizmoLinear

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        direction: TYPE_INPUT_VECTOR = (0.0, 0.0, 1.0),
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
        draw_style: Literal["ARROW", "CROSS", "BOX"] = "ARROW",
        pin_gizmo: bool = False,
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Direction": direction}
        self.color_id = color_id
        self.draw_style = draw_style
        self.pin_gizmo = pin_gizmo
        self._establish_links(**key_args)

    @property
    def pin_gizmo(self) -> bool:
        """Input socket: Pin Gizmo"""
        return self.node.inputs[0].pin_gizmo

    @pin_gizmo.setter
    def pin_gizmo(self, value: bool):
        self.node.inputs[0].pin_gizmo = value

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
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        *,
        pin_gizmo: bool = False,
        use_translation_x: bool = True,
        use_translation_y: bool = True,
        use_translation_z: bool = True,
        use_rotation_x: bool = True,
        use_rotation_y: bool = True,
        use_rotation_z: bool = True,
        use_scale_x: bool = True,
        use_scale_y: bool = True,
        use_scale_z: bool = True,
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Rotation": rotation}
        self.pin_gizmo = pin_gizmo
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
    def pin_gizmo(self) -> bool:
        return self.node.inputs[0].pin_gizmo

    @pin_gizmo.setter
    def pin_gizmo(self, value: bool):
        self.node.inputs[0].pin_gizmo = value

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
