from __future__ import annotations

from typing import Literal

import bpy

from ..types import (
    FloatInterfaceSubtypes,
    IntegerInterfaceSubtypes,
    StringInterfaceSubtypes,
    VectorInterfaceSubtypes,
    _AttributeDomains,
    _SocketShapeStructureType,
)
from .socket import (
    Socket,
    _BooleanMixin,
    _ColorMixin,
    _IntegerMixin,
    _MatrixMixin,
    _RotationMixin,
    _VectorMixin,
)
from .tree import SocketContext


class InterfaceSocket(Socket):
    """Base class for all node group interface socket definitions.

    Extends ``Socket`` so that interface sockets behave like runtime sockets:
    they can be used directly in operator expressions, linked with ``>>``, etc.
    """

    _bl_socket_type: str = ""

    def __init__(self, name: str, description: str = ""):
        self.description = description

        self._socket_context = SocketContext._active_context
        self.interface_socket = self._socket_context._create_socket(self, name)
        self._tree = self._socket_context.builder
        if self._socket_context._direction == "INPUT":
            socket = self.tree._input_node().outputs[self.interface_socket.identifier]
        else:
            socket = self.tree._output_node().inputs[self.interface_socket.identifier]
        super().__init__(socket)

    def _set_values(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            if (
                self.interface_socket.socket_type == "NodeSocketMenu"
                and key == "default_value"
            ):
                self.tree._menu_defaults[self.interface_socket.identifier] = value
            else:
                setattr(self.interface_socket, key, value)

    @property
    def default_value(self):
        if not hasattr(self.interface_socket, "default_value"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'default_value'"
            )
        return getattr(self.interface_socket, "default_value")

    @default_value.setter
    def default_value(self, value):
        if not hasattr(self.interface_socket, "default_value"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'default_value'"
            )
        setattr(self.interface_socket, "default_value", value)


class SocketFloat(InterfaceSocket):
    """Float socket"""

    _bl_socket_type: str = "NodeSocketFloat"
    socket: bpy.types.NodeTreeInterfaceSocketFloat

    def __init__(
        self,
        name: str = "Value",
        default_value: float = 0.0,
        description: str = "",
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        subtype: FloatInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            subtype=subtype,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketInt(_IntegerMixin, InterfaceSocket):
    """Integer socket"""

    _bl_socket_type: str = "NodeSocketInt"
    socket: bpy.types.NodeTreeInterfaceSocketInt

    def __init__(
        self,
        name: str = "Integer",
        default_value: int = 0,
        description: str = "",
        *,
        min_value: int = -2147483648,
        max_value: int = 2147483647,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        default_input: Literal["INDEX", "VALUE", "ID_OR_INDEX"] = "VALUE",
        subtype: IntegerInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            default_input=default_input,
            subtype=subtype,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketBoolean(_BooleanMixin, InterfaceSocket):
    """Boolean socket - true/false value."""

    _bl_socket_type: str = "NodeSocketBool"
    socket: bpy.types.NodeTreeInterfaceSocketBool

    def __init__(
        self,
        name: str = "Boolean",
        default_value: bool = False,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        layer_selection_field: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        is_panel_toggle: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            layer_selection_field=layer_selection_field,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
            is_panel_toggle=is_panel_toggle,
        )


class SocketVector(_VectorMixin, InterfaceSocket):
    """Vector socket — also provides .x, .y, .z and vector math dispatch."""

    _bl_socket_type: str = "NodeSocketVector"
    socket: bpy.types.NodeTreeInterfaceSocketVector

    def __init__(
        self,
        name: str = "Vector",
        default_value: tuple[float, float, float] = (0.0, 0.0, 0.0),
        description: str = "",
        *,
        dimensions: int = 3,
        min_value: float | None = None,
        max_value: float | None = None,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        subtype: VectorInterfaceSubtypes = "NONE",
        default_attribute: str | None = None,
        default_input: Literal[
            "VALUE", "NORMAL", "POSITION", "HANDLE_LEFT", "HANDLE_RIGHT"
        ] = "VALUE",
        attribute_domain: _AttributeDomains = "POINT",
    ):
        assert len(default_value) == dimensions, (
            "Default value length must match dimensions"
        )
        super().__init__(name, description)
        self._set_values(
            dimensions=dimensions,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            subtype=subtype,
            default_input=default_input,
            default_attribute=default_attribute,
            attribute_domain=attribute_domain,
        )


class SocketColor(_ColorMixin, InterfaceSocket):
    """Color socket — also provides .r, .g, .b, .a."""

    _bl_socket_type: str = "NodeSocketColor"
    socket: bpy.types.NodeTreeInterfaceSocketColor

    def __init__(
        self,
        name: str = "Color",
        default_value: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        assert len(default_value) == 4, "Default color must be RGBA tuple"
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketRotation(_RotationMixin, InterfaceSocket):
    """Rotation socket - rotation value (Euler or Quaternion)."""

    _bl_socket_type: str = "NodeSocketRotation"
    socket: bpy.types.NodeTreeInterfaceSocketRotation

    def __init__(
        self,
        name: str = "Rotation",
        default_value: tuple[float, float, float] = (1.0, 0.0, 0.0),
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketMatrix(_MatrixMixin, InterfaceSocket):
    """Matrix socket - 4x4 transformation matrix."""

    _bl_socket_type: str = "NodeSocketMatrix"
    socket: bpy.types.NodeTreeInterfaceSocketMatrix

    def __init__(
        self,
        name: str = "Matrix",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        default_input: Literal["VALUE", "INSTANCE_TRANSFORM"] = "VALUE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            default_input=default_input,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketString(InterfaceSocket):
    _bl_socket_type: str = "NodeSocketString"
    socket: bpy.types.NodeTreeInterfaceSocketString

    def __init__(
        self,
        name: str = "String",
        default_value: str = "",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        subtype: StringInterfaceSubtypes = "NONE",
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            subtype=subtype,
        )


class SocketMenu(InterfaceSocket):
    """Menu socket - holds a selection from predefined items."""

    _bl_socket_type: str = "NodeSocketMenu"
    socket: bpy.types.NodeTreeInterfaceSocketMenu

    def __init__(
        self,
        name: str = "Menu",
        default_value: str | None = None,
        description: str = "",
        *,
        expanded: bool = False,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            menu_expanded=expanded,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
        )


class SocketObject(InterfaceSocket):
    """Object socket - Blender object reference."""

    _bl_socket_type: str = "NodeSocketObject"
    socket: bpy.types.NodeTreeInterfaceSocketObject

    def __init__(
        self,
        name: str = "Object",
        default_value: bpy.types.Object | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketGeometry(InterfaceSocket):
    """Geometry socket - holds mesh, curve, point cloud, or volume data."""

    _bl_socket_type: str = "NodeSocketGeometry"
    socket: bpy.types.NodeTreeInterfaceSocketGeometry

    def __init__(
        self,
        name: str = "Geometry",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketCollection(InterfaceSocket):
    """Collection socket - Blender collection reference."""

    _bl_socket_type: str = "NodeSocketCollection"
    socket: bpy.types.NodeTreeInterfaceSocketCollection

    def __init__(
        self,
        name: str = "Collection",
        default_value: bpy.types.Collection | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketImage(InterfaceSocket):
    """Image socket - Blender image datablock reference."""

    _bl_socket_type: str = "NodeSocketImage"
    socket: bpy.types.NodeTreeInterfaceSocketImage

    def __init__(
        self,
        name: str = "Image",
        default_value: bpy.types.Image | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketMaterial(InterfaceSocket):
    """Material socket - Blender material reference."""

    _bl_socket_type: str = "NodeSocketMaterial"
    socket: bpy.types.NodeTreeInterfaceSocketMaterial

    def __init__(
        self,
        name: str = "Material",
        default_value: bpy.types.Material | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketBundle(InterfaceSocket):
    """Bundle socket - holds multiple data types in one socket."""

    _bl_socket_type: str = "NodeSocketBundle"
    socket: bpy.types.NodeTreeInterfaceSocketBundle

    def __init__(
        self,
        name: str = "Bundle",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketClosure(InterfaceSocket):
    """Closure socket - holds shader closure data."""

    _bl_socket_type: str = "NodeSocketClosure"
    socket: bpy.types.NodeTreeInterfaceSocketClosure

    def __init__(
        self,
        name: str = "Closure",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )


class SocketShader(InterfaceSocket):
    """Shader that is the final output for a material"""

    _bl_socket_type: str = "NodeSocketShader"
    socket: bpy.types.NodeTreeInterfaceSocketShader

    def __init__(
        self,
        name: str = "Shader",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )
