from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal, Self, TypeVar, cast

import bpy
from bpy.types import (
    CompositorNodeTree,
    GeometryNodeTree,
    Node,
    NodeFrame,
    Nodes,
    NodeSocket,
    NodeTree,
    ShaderNodeTree,
)

from ..types import (
    SOCKET_COMPATIBILITY,
    FloatInterfaceSubtypes,
    IntegerInterfaceSubtypes,
    StringInterfaceSubtypes,
    VectorInterfaceSubtypes,
    _AttributeDomains,
    _SocketShapeStructureType,
)
from ._utils import (
    SocketError,
    _allow_innactive_sockets,
    resolve_socket_key,
    socket_key,
)
from .layout import ArrangeMethod
from .layout import arrange as _arrange_nodes
from .socket import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    FloatSocket,
    FontSocket,
    GeometrySocket,
    ImageSocket,
    IntegerSocket,
    MaterialSocket,
    MatrixSocket,
    MenuSocket,
    ObjectSocket,
    RotationSocket,
    ShaderSocket,
    Socket,
    SoundSocket,
    StringSocket,
    VectorSocket,
)

_SocketT = TypeVar("_SocketT", bound=Socket)

# The interface ``default_input`` values Blender actually accepts at runtime,
# per socket type (the RNA enum lists every option on every type, but
# assignment validates a per-type subset — union across tree types here).
# Socket types not listed accept only "VALUE", so their factories don't take
# the parameter at all.
_FloatDefaultInputs = Literal["VALUE", "SCENE_FRAME"]
_IntegerDefaultInputs = Literal["VALUE", "INDEX", "ID_OR_INDEX", "SCENE_FRAME"]
_VectorDefaultInputs = Literal[
    "VALUE",
    "NORMAL",
    "POSITION",
    "HANDLE_LEFT",
    "HANDLE_RIGHT",
    "UNIFORM_IMAGE_COORDINATES",
]
_MatrixDefaultInputs = Literal["VALUE", "INSTANCE_TRANSFORM"]
_ObjectDefaultInputs = Literal["VALUE", "SELF_OBJECT"]


class PanelContext:
    """Context manager for grouping sockets into a panel."""

    def __init__(
        self,
        socket_context: SocketContext,
        name: str,
        *,
        description: str = "",
        default_closed: bool = False,
    ):
        self._socket_context = socket_context
        self._name = name
        self._description = description
        self._default_closed = default_closed
        self._panel: bpy.types.NodeTreeInterfacePanel | None = None

    def __enter__(self):
        interface = self._socket_context.interface
        self._panel = interface.new_panel(
            self._name,
            description=self._description,
            default_closed=self._default_closed,
        )
        # Entered inside another panel context → nest under it.
        self._previous = self._socket_context._active_panel
        if self._previous is not None:
            assert self._panel is not None
            interface.move_to_parent(
                self._panel, self._previous, len(self._previous.interface_items)
            )
        self._socket_context._active_panel = self._panel
        return self

    def __exit__(self, *args):
        self._socket_context._active_panel = self._previous


class TreePanelContext:
    """Context manager for a panel holding both input *and* output sockets.

    Activates the panel on the builder's ``inputs`` and ``outputs`` contexts
    at once, and reuses an existing top-level panel of the same name — so a
    mixed panel can be filled in two passes (inputs, then outputs) without
    duplicating it."""

    def __init__(
        self,
        builder: TreeBuilder,
        name: str | bpy.types.NodeTreeInterfacePanel,
        *,
        description: str = "",
        default_closed: bool = False,
        reuse: bool = True,
    ):
        self._builder = builder
        self._name = name
        self._description = description
        self._default_closed = default_closed
        self._reuse = reuse
        self.panel: bpy.types.NodeTreeInterfacePanel | None = None

    def __enter__(self):
        interface = self._builder.tree.interface
        assert interface is not None
        # Entered inside another panel context → nest under it. A mixed panel
        # lives in one place, so an enclosing panel open on only one side
        # (e.g. inside ``tree.outputs.panel(...)``) parents it too; two
        # different panels open at once leave no sensible parent.
        self._previous_inputs = self._builder.inputs._active_panel
        self._previous_outputs = self._builder.outputs._active_panel
        parent = self._previous_inputs or self._previous_outputs
        if (
            self._previous_inputs is not None
            and self._previous_outputs is not None
            and self._previous_inputs != self._previous_outputs
        ):
            raise ValueError(
                f"Cannot nest mixed panel {self._name!r}: different panels "
                f"are active for inputs ({self._previous_inputs.name!r}) and "
                f"outputs ({self._previous_outputs.name!r})."
            )

        def parent_matches(item) -> bool:
            if parent is None:
                return item.parent is None or item.parent.index == -1
            return item.parent == parent

        if not isinstance(self._name, str):
            # Reopening an exact panel by handle (e.g. the second direction
            # pass of generated round-trip code, where a name lookup could
            # land on a same-named sibling): activate it as it stands.
            self.panel = self._name
        else:
            self.panel = None
            if self._reuse:
                self.panel = next(
                    (
                        item
                        for item in interface.items_tree
                        if getattr(item, "item_type", "") == "PANEL"
                        and item.name == self._name
                        and parent_matches(item)
                    ),
                    None,
                )
            if self.panel is None:
                self.panel = interface.new_panel(
                    self._name,
                    description=self._description,
                    default_closed=self._default_closed,
                )
                if parent is not None:
                    interface.move_to_parent(
                        self.panel, parent, len(parent.interface_items)
                    )
        self._builder.inputs._active_panel = self.panel
        self._builder.outputs._active_panel = self.panel
        return self

    def __exit__(self, *args):
        self._builder.inputs._active_panel = self._previous_inputs
        self._builder.outputs._active_panel = self._previous_outputs


class SocketContext:
    _direction: Literal["INPUT", "OUTPUT"] | None

    def __init__(self, tree_builder: TreeBuilder):
        self.builder = tree_builder
        self._active_panel: bpy.types.NodeTreeInterfacePanel | None = None

    @property
    def tree(self) -> NodeTree:
        tree = self.builder.tree
        assert tree is not None
        return tree

    @property
    def interface(self) -> bpy.types.NodeTreeInterface:
        interface = self.tree.interface
        assert interface is not None
        return interface

    def panel(
        self, name: str, *, description: str = "", default_closed: bool = False
    ) -> PanelContext:
        """Create a panel context for grouping sockets."""
        return PanelContext(
            self, name, description=description, default_closed=default_closed
        )

    # ------------------------------------------------------------------
    # Socket factory methods
    # ------------------------------------------------------------------

    def _add_socket(
        self, socket_type: str, name: str, description: str
    ) -> bpy.types.NodeTreeInterfaceSocket:
        kwargs: dict[str, Any] = {
            "name": name,
            "in_out": self._direction,
            "socket_type": socket_type,
        }
        if self._active_panel is not None:
            kwargs["parent"] = self._active_panel
        interface_socket = self.interface.new_socket(**kwargs)
        assert interface_socket is not None
        interface_socket.description = description
        return interface_socket

    def _set_props(
        self, interface_socket: bpy.types.NodeTreeInterfaceSocket, **kwargs: Any
    ) -> None:
        # ``force_non_field``'s RNA update callback recomputes the structure
        # type, clobbering an already-assigned ``structure_type`` — apply it
        # first, and skip the pointless (but still update-firing) False write.
        if kwargs.get("force_non_field") is False:
            kwargs.pop("force_non_field")
        elif "force_non_field" in kwargs:
            kwargs = {"force_non_field": kwargs.pop("force_non_field"), **kwargs}
        for key, value in kwargs.items():
            if value is None:
                continue
            if (
                interface_socket.socket_type == "NodeSocketMenu"
                and key == "default_value"
            ):
                self.builder._menu_defaults.append(
                    _MenuDefault(interface_socket, value)
                )
            elif key == "default_attribute":
                # the bpy property is named default_attribute_name
                interface_socket.default_attribute_name = value
            else:
                setattr(interface_socket, key, value)

    def _wrap(
        self,
        socket_cls: type[_SocketT],
        interface_socket: bpy.types.NodeTreeInterfaceSocket,
    ) -> _SocketT:
        if self._direction == "INPUT":
            bpy_socket = self.builder._input_node().outputs[interface_socket.identifier]
        else:
            bpy_socket = self.builder._output_node().inputs[interface_socket.identifier]
        s = socket_cls(bpy_socket)
        s._tree = self.builder
        s._interface_socket = interface_socket
        # Captured while the reference is certainly fresh: interface items
        # reallocate as the interface grows, so a later read through
        # _interface_socket can hit a different item.
        s._interface_identifier = interface_socket.identifier
        return s

    def float(
        self,
        name: str = "Value",
        default_value: float = 0.0,  # ty: ignore[invalid-type-form]
        description: str = "",
        *,
        min_value: float | None = None,  # ty: ignore[invalid-type-form]
        max_value: float | None = None,  # ty: ignore[invalid-type-form]
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        subtype: FloatInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        force_non_field: bool = False,
        default_input: _FloatDefaultInputs = "VALUE",
    ) -> FloatSocket:
        iface = self._add_socket("NodeSocketFloat", name, description)
        self._set_props(
            iface,
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
            force_non_field=force_non_field,
            default_input=default_input,
        )
        return self._wrap(FloatSocket, iface)

    def integer(
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
        default_input: _IntegerDefaultInputs = "VALUE",
        subtype: IntegerInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        force_non_field: bool = False,
    ) -> IntegerSocket:
        iface = self._add_socket("NodeSocketInt", name, description)
        self._set_props(
            iface,
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
            force_non_field=force_non_field,
        )
        return self._wrap(IntegerSocket, iface)

    def boolean(
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
        force_non_field: bool = False,
    ) -> BooleanSocket:
        iface = self._add_socket("NodeSocketBool", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            layer_selection_field=layer_selection_field,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
            is_panel_toggle=is_panel_toggle,
            force_non_field=force_non_field,
        )
        return self._wrap(BooleanSocket, iface)

    def vector(
        self,
        name: str = "Vector",
        default_value: tuple[float, float]  # ty: ignore[invalid-type-form]
        | tuple[float, float, float]  # ty: ignore[invalid-type-form]
        | tuple[float, float, float, float]  # ty: ignore[invalid-type-form]
        | None = None,
        description: str = "",
        *,
        dimensions: Literal[2, 3, 4] = 3,
        min_value: float | None = None,  # ty: ignore[invalid-type-form]
        max_value: float | None = None,  # ty: ignore[invalid-type-form]
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        subtype: VectorInterfaceSubtypes = "NONE",
        default_attribute: str | None = None,
        default_input: _VectorDefaultInputs = "VALUE",
        attribute_domain: _AttributeDomains = "POINT",
        force_non_field: bool = False,
    ) -> VectorSocket:
        values: tuple[float, ...] = (
            (0.0,) * dimensions if default_value is None else tuple(default_value)
        )
        assert len(values) == dimensions, "Default value length must match dimensions"
        iface = self._add_socket("NodeSocketVector", name, description)
        # The interface socket's default_value RNA is a fixed 3-float array
        # regardless of `dimensions`; pad (or truncate) to length 3 to assign.
        rna_default = (values + (0.0, 0.0, 0.0))[:3]
        self._set_props(
            iface,
            dimensions=dimensions,
            default_value=rna_default,
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
            force_non_field=force_non_field,
        )
        return self._wrap(VectorSocket, iface)

    def color(
        self,
        name: str = "Color",
        default_value: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),  # ty: ignore[invalid-type-form]
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        force_non_field: bool = False,
    ) -> ColorSocket:
        assert len(default_value) == 4, "Default color must be RGBA tuple"
        iface = self._add_socket("NodeSocketColor", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
            force_non_field=force_non_field,
        )
        return self._wrap(ColorSocket, iface)

    def rotation(
        self,
        name: str = "Rotation",
        default_value: tuple[float, float, float] = (0.0, 0.0, 0.0),  # ty: ignore[invalid-type-form]
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        force_non_field: bool = False,
    ) -> RotationSocket:
        iface = self._add_socket("NodeSocketRotation", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
            force_non_field=force_non_field,
        )
        return self._wrap(RotationSocket, iface)

    def matrix(
        self,
        name: str = "Matrix",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        default_input: _MatrixDefaultInputs = "VALUE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
        force_non_field: bool = False,
    ) -> MatrixSocket:
        iface = self._add_socket("NodeSocketMatrix", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            default_input=default_input,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
            force_non_field=force_non_field,
        )
        return self._wrap(MatrixSocket, iface)

    def string(
        self,
        name: str = "String",
        default_value: str = "",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        subtype: StringInterfaceSubtypes = "NONE",
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> StringSocket:
        iface = self._add_socket("NodeSocketString", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            subtype=subtype,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(StringSocket, iface)

    def menu(
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
        force_non_field: bool = False,
    ) -> MenuSocket:
        iface = self._add_socket("NodeSocketMenu", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            menu_expanded=expanded,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(MenuSocket, iface)

    def object(
        self,
        name: str = "Object",
        default_value: bpy.types.Object | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
        default_input: _ObjectDefaultInputs = "VALUE",
    ) -> ObjectSocket:
        iface = self._add_socket("NodeSocketObject", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
            default_input=default_input,
        )
        return self._wrap(ObjectSocket, iface)

    def geometry(
        self,
        name: str = "Geometry",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> GeometrySocket:
        iface = self._add_socket("NodeSocketGeometry", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(GeometrySocket, iface)

    def collection(
        self,
        name: str = "Collection",
        default_value: bpy.types.Collection | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> CollectionSocket:
        iface = self._add_socket("NodeSocketCollection", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(CollectionSocket, iface)

    def image(
        self,
        name: str = "Image",
        default_value: bpy.types.Image | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> ImageSocket:
        iface = self._add_socket("NodeSocketImage", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(ImageSocket, iface)

    def material(
        self,
        name: str = "Material",
        default_value: bpy.types.Material | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> MaterialSocket:
        iface = self._add_socket("NodeSocketMaterial", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(MaterialSocket, iface)

    def font(
        self,
        name: str = "Font",
        default_value: bpy.types.VectorFont | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ) -> FontSocket:
        iface = self._add_socket("NodeSocketFont", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )
        return self._wrap(FontSocket, iface)

    def sound(
        self,
        name: str = "Sound",
        default_value: bpy.types.Sound | None = None,
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ) -> SoundSocket:
        iface = self._add_socket("NodeSocketSound", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )
        return self._wrap(SoundSocket, iface)

    def bundle(
        self,
        name: str = "Bundle",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> BundleSocket:
        iface = self._add_socket("NodeSocketBundle", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(BundleSocket, iface)

    def closure(
        self,
        name: str = "Closure",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> ClosureSocket:
        iface = self._add_socket("NodeSocketClosure", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(ClosureSocket, iface)

    def shader(
        self,
        name: str = "Shader",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
        structure_type: _SocketShapeStructureType = "AUTO",
        force_non_field: bool = False,
    ) -> ShaderSocket:
        iface = self._add_socket("NodeSocketShader", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
            force_non_field=force_non_field,
        )
        return self._wrap(ShaderSocket, iface)

    def __len__(self) -> int:
        assert self.tree.interface is not None
        return len(
            [
                item
                for item in self.tree.interface.items_tree
                if isinstance(item, bpy.types.NodeTreeInterfaceSocket)
                and item.in_out == self._direction
            ]
        )


class DirectionalContext(SocketContext):
    """Base class for directional socket contexts"""

    _direction = "INPUT"


class InputInterfaceContext(DirectionalContext):
    _direction = "INPUT"


class OutputInterfaceContext(DirectionalContext):
    _direction = "OUTPUT"


@dataclass
class _MenuDefault:
    """A menu default deferred to context exit, with enough breadcrumbs to
    re-resolve its target — the reference captured at queue time is
    invalidated by the interface update that populates the menu enums."""

    item: bpy.types.NodeSocketMenu | bpy.types.NodeTreeInterfaceSocketMenu
    default: str
    # Interface references go stale as the interface grows, so a caller that
    # captured the identifier while the reference was fresh passes it in;
    # otherwise it is read here, at queue time.
    identifier: str = ""
    node_name: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if not self.identifier:
            self.identifier = self.item.identifier
            node = getattr(self.item, "node", None)  # sockets only
            self.node_name = node.name if node is not None else None

    def resolve(self, tree: NodeTree):
        """The live menu socket/interface item this default targets.

        Interface items are re-resolved by identifier — the interface update
        that populates the enums reallocates them, leaving the queued
        reference stale. A node socket keeps its direct reference (its node
        may have been *renamed* since queueing, so the name breadcrumb could
        hit a different same-named node); the breadcrumbs are only its
        fallback if the socket itself was removed."""
        if self.node_name is None:
            interface = tree.interface
            assert interface is not None
            return next(
                (
                    item
                    for item in interface.items_tree
                    if getattr(item, "identifier", None) == self.identifier
                ),
                None,
            )
        try:
            if self.item.identifier == self.identifier:
                return self.item
        except ReferenceError:  # pragma: no cover - the socket was removed
            pass
        return self._resolve_by_breadcrumbs(tree)  # pragma: no cover

    def _resolve_by_breadcrumbs(self, tree: NodeTree):  # pragma: no cover
        """Fallback for a removed/stale socket reference: re-find the socket
        via its node name and identifier."""
        assert self.node_name is not None
        node = tree.nodes.get(self.node_name)
        if node is None:
            return None
        return next((s for s in node.inputs if s.identifier == self.identifier), None)


# One node's layout-snapshot record: (bl_idname, (x, y), parent frame name,
# incoming links as (own input socket key, source node name, source socket
# key)) — socket keys per :func:`socket_key`, stable across a rebuild where
# identifiers are not.
type _LayoutEntry = tuple[
    str,
    tuple[float, float],
    str | None,
    tuple[tuple[str, str, str], ...],
]

# One piece of matching evidence: a link as (own socket id, is_output, peer's
# authored name, peer socket id), or ("parent", frame's authored name) /
# ("child", child's authored name) for frame membership.
type _Evidence = tuple[str, bool, str, str] | tuple[str, str]


_IO_BL_IDNAMES = frozenset({"NodeGroupInput", "NodeGroupOutput"})


def _sub_multiset(smaller: Counter, larger: Counter) -> bool:
    return all(count <= larger[key] for key, count in smaller.items())


def _match_layout_snapshot(
    tree: NodeTree, entries: dict[str, _LayoutEntry]
) -> list[tuple[Node, str]]:
    """Match the tree's nodes to layout-snapshot entries, returning
    ``(node, entry name)`` pairs.

    Structure decides, names only break ties: a rebuild reuses authored
    names for *different* nodes whenever duplicate-type creation order
    differs, so a name match is a hint, never ground truth. A node is
    compatible with an entry of its type when its evidence — links to
    already-matched neighbours (Group Input/Output instances counting as
    anonymous peers), plus frame parent/child relations — equals the
    entry's. Each round binds every node compatible with exactly one entry
    that no other node uniquely demands; when a round stalls, the first
    same-name pair whose node evidence is a sub-multiset of its entry's (a
    rebuild recreates the authored links but may drop one it refuses)
    binds, and propagation resumes. Leftovers pair up by sorted name within
    each type — after the fixpoint they are structural twins
    (interchangeable by definition) or pairs the evidence could not
    separate, where a best-effort spot beats no position at all."""
    nodes = {node.name: node for node in tree.nodes}
    node_parent = {
        name: node.parent.name if node.parent is not None else None
        for name, node in nodes.items()
    }
    entry_parent = {name: entry[2] for name, entry in entries.items()}

    node_adj: dict[str, list[tuple[str, bool, str, str]]] = {name: [] for name in nodes}
    for link in tree.links:
        assert link.to_node and link.to_socket and link.from_node
        assert link.from_socket is not None
        to_key, from_key = socket_key(link.to_socket), socket_key(link.from_socket)
        node_adj[link.to_node.name].append(
            (to_key, False, link.from_node.name, from_key)
        )
        node_adj[link.from_node.name].append(
            (from_key, True, link.to_node.name, to_key)
        )
    entry_adj: dict[str, list[tuple[str, bool, str, str]]] = {
        name: [] for name in entries
    }
    for name, (_type, _pos, _parent, incoming) in entries.items():
        for own_sock, peer, peer_sock in incoming:
            entry_adj[name].append((own_sock, False, peer, peer_sock))
            if peer in entry_adj:
                entry_adj[peer].append((peer_sock, True, name, own_sock))

    n2e: dict[str, str] = {}  # rebuilt node name -> entry (authored) name
    e2n: dict[str, str] = {}

    # Group Input/Output instances are matched by name alone and count as
    # anonymous link peers: authored links may be spread over several split
    # instances while the rebuilt tree still has them all on the primary
    # (splits apply *after* the snapshot, once consumers carry their
    # authored names), so instance identity would contradict, not confirm.
    def node_sig(name: str) -> Counter[_Evidence]:
        sig: Counter[_Evidence] = Counter()
        if nodes[name].bl_idname not in _IO_BL_IDNAMES:
            for own_sock, is_out, peer, peer_sock in node_adj[name]:
                peer_type = nodes[peer].bl_idname
                if peer_type in _IO_BL_IDNAMES:
                    sig[(own_sock, is_out, peer_type, peer_sock)] += 1
                elif peer in n2e:
                    sig[(own_sock, is_out, n2e[peer], peer_sock)] += 1
        parent = node_parent[name]
        if parent is not None and parent in n2e:
            sig[("parent", n2e[parent])] += 1
        for child, child_parent in node_parent.items():
            if child_parent == name and child in n2e:
                sig[("child", n2e[child])] += 1
        return sig

    def entry_sig(name: str) -> Counter[_Evidence]:
        sig: Counter[_Evidence] = Counter()
        if entries[name][0] not in _IO_BL_IDNAMES:
            for own_sock, is_out, peer, peer_sock in entry_adj[name]:
                # A peer with no entry is a split Group Input instance — the
                # snapshot deliberately omits them (they don't exist until
                # the splits block runs, after this match).
                peer_type = entries[peer][0] if peer in entries else "NodeGroupInput"
                if peer_type in _IO_BL_IDNAMES:
                    sig[(own_sock, is_out, peer_type, peer_sock)] += 1
                elif peer in e2n:
                    sig[(own_sock, is_out, peer, peer_sock)] += 1
        parent = entry_parent[name]
        if parent is not None and parent in e2n:
            sig[("parent", parent)] += 1
        for child, child_parent in entry_parent.items():
            if child_parent == name and child in e2n:
                sig[("child", child)] += 1
        return sig

    def bind(name: str, entry_name: str) -> None:
        n2e[name] = entry_name
        e2n[entry_name] = name

    while True:
        by_type_entries: dict[str, list[str]] = {}
        for entry_name in entries:
            if entry_name not in e2n:
                by_type_entries.setdefault(entries[entry_name][0], []).append(
                    entry_name
                )
        by_type_nodes: dict[str, list[str]] = {}
        for name, node in nodes.items():
            if name not in n2e and node.bl_idname in by_type_entries:
                by_type_nodes.setdefault(node.bl_idname, []).append(name)

        binds: list[tuple[str, str]] = []
        for bl_idname, group_nodes in by_type_nodes.items():
            node_sigs = {name: node_sig(name) for name in group_nodes}
            entry_sigs = {name: entry_sig(name) for name in by_type_entries[bl_idname]}
            # Both sides restrict evidence to already-matched neighbours, so
            # a true pair's signatures are *equal* whenever the rebuild
            # recreated every authored link (it does, short of a link the
            # builder refused — those resolve via the name tie-break below).
            # A node equal to exactly one entry must be that entry — unless
            # another node demands the same entry just as uniquely, which
            # means the evidence cannot separate them yet.
            demands: dict[str, list[str]] = {}
            for name, sig in node_sigs.items():
                compatible = [
                    entry_name for entry_name, esig in entry_sigs.items() if sig == esig
                ]
                if len(compatible) == 1:
                    demands.setdefault(compatible[0], []).append(name)
            for entry_name, claimants in demands.items():
                if len(claimants) == 1:
                    binds.append((claimants[0], entry_name))
        if binds:
            for name, entry_name in binds:
                bind(name, entry_name)
            continue

        # Stalled: use a name match as a tie-break — one pair per stall, so
        # the evidence it adds can veto later same-name pairs that would
        # have bound wrongly.
        tie = next(
            (
                name
                for name in sorted(nodes)
                if name not in n2e
                and name in entries
                and name not in e2n
                and nodes[name].bl_idname == entries[name][0]
                and _sub_multiset(node_sig(name), entry_sig(name))
            ),
            None,
        )
        if tie is None:
            break
        bind(tie, tie)

    # Leftovers: pair remaining same-type nodes and entries by sorted name.
    # After the fixpoint these are either structural twins (any assignment
    # reproduces the authored look) or pairs blocked by a missing link — for
    # which a best-effort spot still beats no position at all.
    remaining_entries: dict[str, list[str]] = {}
    for entry_name in sorted(entries):
        if entry_name not in e2n:
            remaining_entries.setdefault(entries[entry_name][0], []).append(entry_name)
    for name in sorted(nodes):
        if name in n2e:
            continue
        pool = remaining_entries.get(nodes[name].bl_idname)
        if pool:
            n2e[name] = pool.pop(0)

    return [(nodes[name], entry_name) for name, entry_name in n2e.items()]


class TreeBuilder[TreeT: NodeTree]:
    """Builder for creating Blender node trees with a clean Python API.

    Supports geometry, shader, and compositor node trees.
    """

    tree: TreeT
    _tree_contexts: ClassVar[list[TreeBuilder]] = []
    _frame_contexts: ClassVar[list[NodeFrame]] = []

    def __init__(
        self,
        tree: NodeTree | str = "Geometry Nodes",
        *,
        tree_type: Literal[
            "GeometryNodeTree", "ShaderNodeTree", "CompositorNodeTree"
        ] = "GeometryNodeTree",
        collapse: bool = False,
        arrange: ArrangeMethod = "sugiyama",
        fake_user: bool = False,
        ignore_visibility: bool = False,
        split_inputs: bool = False,
    ):
        if isinstance(tree, str):
            self.tree = bpy.data.node_groups.new(tree, tree_type)  # ty: ignore[invalid-assignment]
        else:
            self.tree = tree  # type: ignore

        self._menu_defaults: list[_MenuDefault] = []
        self._exited = False
        self.inputs = InputInterfaceContext(self)
        self.outputs = OutputInterfaceContext(self)
        self._arrange = arrange
        self.collapse = collapse
        self.fake_user = fake_user
        self.ignore_visibility = ignore_visibility
        self._split_inputs = split_inputs

    @classmethod
    def geometry(
        cls,
        name: GeometryNodeTree | str = "Geometry Nodes",
        *,
        collapse: bool = False,
        arrange: ArrangeMethod = "sugiyama",
        fake_user: bool = False,
        split_inputs: bool = False,
    ) -> TreeBuilder[GeometryNodeTree]:
        """Create a geometry node tree."""
        return cast(
            "TreeBuilder[GeometryNodeTree]",
            cls(
                name,
                tree_type="GeometryNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
                split_inputs=split_inputs,
            ),
        )

    @classmethod
    def shader(
        cls,
        name: ShaderNodeTree | str = "Shader Nodes",
        *,
        collapse: bool = False,
        arrange: ArrangeMethod = "sugiyama",
        fake_user: bool = False,
        split_inputs: bool = False,
    ) -> TreeBuilder[ShaderNodeTree]:
        """Create a shader node tree."""
        return cast(
            "TreeBuilder[ShaderNodeTree]",
            cls(
                name,
                tree_type="ShaderNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
                split_inputs=split_inputs,
            ),
        )

    @classmethod
    def compositor(
        cls,
        name: CompositorNodeTree | str = "Compositor Nodes",
        *,
        collapse: bool = False,
        arrange: ArrangeMethod = "sugiyama",
        fake_user: bool = False,
        split_inputs: bool = False,
    ) -> TreeBuilder[CompositorNodeTree]:
        """Create a compositor node tree."""
        return cast(
            "TreeBuilder[CompositorNodeTree]",
            cls(
                name,
                tree_type="CompositorNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
                split_inputs=split_inputs,
            ),
        )

    @property
    def nodes(self) -> Nodes:
        return self.tree.nodes

    @property
    def fake_user(self) -> bool:
        return self.tree.use_fake_user

    @fake_user.setter
    def fake_user(self, value: bool) -> None:
        self.tree.use_fake_user = value

    def to_python(
        self,
        min_chain_length: int = 3,
        strict: bool = True,
        max_inline_width: int | None = 88,
        snapshot_positions: bool = False,
        keep_reroutes: bool = False,
        top_level: Literal["with", "class"] = "with",
        format: bool = True,
        nodebpy_pkg: str = "nodebpy",
    ) -> str:
        """Generate Python source that recreates this tree using nodebpy.

        See :func:`nodebpy.codegen.to_python` for parameter details.
        """
        from ..export import to_python

        return to_python(
            self,
            min_chain_length=min_chain_length,
            strict=strict,
            max_inline_width=max_inline_width,
            snapshot_positions=snapshot_positions,
            keep_reroutes=keep_reroutes,
            top_level=top_level,
            format=format,
            nodebpy_pkg=nodebpy_pkg,
        )

    def to_mermaid(self, fenced: bool = True) -> str:
        """Generate a Mermaid diagram that represents this tree.

        This can be used for documentation or visualization purposes.
        The Mermaid syntax is supported by many tools, including GitHub and Jupyter notebooks.

        Arguments
        ---------
            fenced:
                Whether to wrap the output in a fenced code block with mermaid syntax highlighting.

        Returns
        -------
            A string containing the Mermaid diagram syntax representing this node tree.
        """
        from ..export import to_mermaid

        return to_mermaid(self, fenced=fenced)

    def activate_tree(self) -> None:
        """Make this tree the active tree for all new node creation."""
        TreeBuilder._tree_contexts.append(self)

    def deactivate_tree(self) -> None:
        """Whatever tree was previously active is set to be the active one (or None if no previously active tree)."""
        TreeBuilder._tree_contexts.pop()

    def __enter__(self) -> Self:
        self.activate_tree()
        self._exited = False
        return self

    def __exit__(self, *args):
        # Split before auto-layout, so the created instances get arranged
        # next to their consumers.
        if self._split_inputs:
            self.split_group_inputs()
        if self._arrange is not None:
            self.arrange()
        self._apply_input_defaults()
        # Interface-menu defaults assigned from here on can't wait for a
        # context exit that already happened — apply them immediately
        # (see MenuSocket.default_value).
        self._exited = True
        self.deactivate_tree()

    def _apply_input_defaults(self) -> None:
        if not self._menu_defaults:
            return
        # Menu enums populate by propagation from the Menu Switch that
        # defines them; a headless session never runs the editor update that
        # triggers it, so without this nudge the assignments below silently
        # store an empty default. The update can reallocate the targets, so
        # each is re-resolved from its breadcrumbs before assignment.
        self.tree.interface_update(bpy.context)
        for value in self._menu_defaults:
            if value.default == "":
                continue
            item = value.resolve(self.tree)
            if item is not None:
                item.default_value = value.default

    def __len__(self) -> int:
        return len(self.nodes)

    def disable_arrange(self) -> None:
        """Disable the auto-layout that otherwise runs when this tree's context
        exits, so explicitly assigned node locations are preserved."""
        self._arrange = None

    def panel(
        self,
        name: str | bpy.types.NodeTreeInterfacePanel | TreePanelContext,
        *,
        description: str = "",
        default_closed: bool = False,
        reuse: bool = True,
    ) -> TreePanelContext:
        """A panel that can group input *and* output sockets together
        (``tree.inputs.panel`` / ``tree.outputs.panel`` group one direction).
        Reuses an existing same-named panel under the same parent, so a mixed
        panel can be declared in separate input and output passes; pass
        ``reuse=False`` to always create a fresh panel — Blender allows
        several same-named sibling panels, and rebuilding such an interface
        must not fold them into one. Passing an existing panel (or a previous
        ``tree.panel(...)`` context) instead of a name reopens exactly that
        panel — the unambiguous spelling generated code uses for the second
        direction pass over a same-named sibling."""
        if isinstance(name, TreePanelContext):
            assert name.panel is not None
            name = name.panel
        return TreePanelContext(
            self,
            name,
            description=description,
            default_closed=default_closed,
            reuse=reuse,
        )

    @property
    def node_positions(self) -> dict[str, tuple[float, float]]:
        """A ``{node name: (x, y)}`` snapshot of every node's location."""
        return {
            node.name: (node.location.x, node.location.y) for node in self.tree.nodes
        }

    @node_positions.setter
    def node_positions(self, positions: dict[str, tuple[float, float]]) -> None:
        """Apply ``{node name: (x, y)}`` locations. Names absent from the tree
        (e.g. a reroute a rebuild dropped) are skipped."""
        for name, location in positions.items():
            node = self.tree.nodes.get(name)
            if node is not None:
                node.location = location

    @property
    def layout_snapshot(self) -> dict[str, _LayoutEntry]:
        """A structural layout snapshot: for every node its type, ``(x, y)``
        location, frame parent and incoming links, keyed by node name —
        the block ``to_python(snapshot_positions=True)`` emits. See the
        setter for how it is applied."""
        incoming: dict[str, list[tuple[str, str, str]]] = {}
        for link in self.tree.links:
            assert link.to_node and link.to_socket and link.from_node
            assert link.from_socket is not None
            incoming.setdefault(link.to_node.name, []).append(
                (
                    socket_key(link.to_socket),
                    link.from_node.name,
                    socket_key(link.from_socket),
                )
            )
        return {
            node.name: (
                node.bl_idname,
                (node.location.x, node.location.y),
                node.parent.name if node.parent is not None else None,
                tuple(sorted(incoming.get(node.name, ()))),
            )
            for node in self.tree.nodes
        }

    @layout_snapshot.setter
    def layout_snapshot(self, snapshot: dict[str, _LayoutEntry]) -> None:
        """Restore authored node names and locations from a snapshot.

        A rebuild names duplicate-type nodes by creation order (``Math``,
        ``Math.001``, ...), which rarely matches the authored order, so
        applying locations by bare name would put nodes on each other's
        authored spots. Nodes are instead matched to snapshot entries
        structurally: exact name+type matches seed the correspondence, then
        it grows through link/frame evidence against already-matched
        neighbours; matched nodes are renamed to their authored names and
        moved to their authored locations. Entries a rebuild has no
        counterpart for (e.g. dropped reroutes) are skipped, so applying a
        snapshot to an edited tree degrades gracefully."""
        entries = {
            name: (entry[0], tuple(entry[1]), entry[2], tuple(entry[3]))
            for name, entry in snapshot.items()
        }
        matches = _match_layout_snapshot(self.tree, entries)

        # Rename via unique temporaries: authored names can swap between
        # nodes (assigning directly would make Blender suffix the second),
        # and an unmatched node squatting on a target name must yield it.
        targets = {entry_name for _node, entry_name in matches}
        matched_nodes = {node.name for node, _entry_name in matches}
        squatters = [
            node
            for node in self.tree.nodes
            if node.name in targets and node.name not in matched_nodes
        ]
        displaced = [(node, node.name) for node in squatters]
        for index, node in enumerate([node for node, _ in matches] + squatters):
            node.name = f"__nodebpy_tmp_{index}"
        matched_by_entry = {entry_name: node for node, entry_name in matches}
        for node, entry_name in matches:
            node.name = entry_name
            _bl_idname, location, parent, _links = entries[entry_name]
            # Restore frame membership before the location: locations are
            # parent-relative, and a rebuild leaves some nodes unparented
            # (split Group Input instances are created outside any frame).
            parent_node = matched_by_entry.get(parent) if parent is not None else None
            if parent_node is not None or parent is None:
                node.parent = cast("NodeFrame | None", parent_node)
            node.location = location
        for node, old_name in displaced:
            node.name = old_name  # re-suffixed by Blender on collision

    @property
    def group_input_splits(self) -> list[dict]:
        """The extra Group Input instances beyond the primary one, each as
        ``{"name": ..., "links": [(interface input name, consumer node name,
        consumer socket key), ...], "location": ..., "parent": ...}`` — the
        editor convention of several input nodes near their consumers
        instead of one node trailing long noodles. See the setter."""
        splits: list[dict] = []
        for node in self.tree.nodes:
            if node.bl_idname != "NodeGroupInput" or node.name == "Group Input":
                continue
            links: list[tuple[str, str, str]] = []
            for socket in node.outputs:
                for link in socket.links or ():
                    to_node, to_socket = link.to_node, link.to_socket
                    assert to_node is not None and to_socket is not None
                    links.append((socket.name, to_node.name, socket_key(to_socket)))
            splits.append(
                {
                    "name": node.name,
                    "links": links,
                    "location": (node.location.x, node.location.y),
                    "parent": node.parent.name if node.parent is not None else None,
                }
            )
        return splits

    @group_input_splits.setter
    def group_input_splits(self, splits: list[dict]) -> None:
        """Split the Group Input node into several instances: each entry
        creates one instance carrying the listed links (moved off whichever
        input node holds them — exactly one per entry, so parallel links from
        several instances into one multi-input socket are never swept away
        together). An entry naming a consumer or socket the tree doesn't have
        is skipped — that noodle simply stays on the primary node — so
        applying a snapshot to an edited tree degrades gracefully, like
        :attr:`node_positions`."""
        # Deferred menu defaults must land before any link moves: their enums
        # propagate through the pre-split wiring, and re-sourcing a menu link
        # leaves the enum unpopulated until an editor update this headless
        # session never runs.
        self._apply_input_defaults()
        self._menu_defaults.clear()
        for split in splits:
            instance = self.tree.nodes.new("NodeGroupInput")
            assert instance is not None
            instance.name = split["name"]
            # Authored placement (parent before location — locations are
            # parent-relative); older snapshots without these keys leave the
            # instance where auto-layout or the caller puts it.
            parent = self.tree.nodes.get(split.get("parent") or "")
            if isinstance(parent, NodeFrame):
                instance.parent = parent
            if (location := split.get("location")) is not None:
                instance.location = location
            for from_name, to_node_name, to_socket_key in split["links"]:
                to_node = self.tree.nodes.get(to_node_name)
                if to_node is None:
                    continue
                to_socket = resolve_socket_key(to_node.inputs, to_socket_key)
                if to_socket is None:
                    continue
                # Only re-source an existing identical link: the consumer
                # must already take this same interface input from some
                # Group Input instance. A rebuild that assigned this name to
                # a *different* node fails the check and the noodle stays on
                # the primary — names alone must never create connectivity,
                # or two same-typed consumers could end up cross-wired.
                existing = [
                    link
                    for link in to_socket.links or ()
                    if link.from_node is not None
                    and link.from_socket is not None
                    and link.from_node.bl_idname == "NodeGroupInput"
                    and link.from_socket.name == from_name
                ]
                if not existing:
                    continue
                # Move exactly one link per recorded entry: a multi-input
                # socket legally takes the same interface input several
                # times, and the getter records one entry per link — moving
                # them all here would collapse the duplicates into one.
                # Prefer a link still on another instance so repeated entries
                # walk through the remaining duplicates.
                link = next(
                    (ln for ln in existing if ln.from_node != instance), existing[0]
                )
                # Re-source the very interface socket the link already uses
                # (by identifier): interface names can repeat across types,
                # so a name lookup on the instance could pick a same-named
                # socket of the wrong type and forge an invalid link.
                assert link.from_socket is not None
                identifier = link.from_socket.identifier
                from_socket = next(
                    (s for s in instance.outputs if s.identifier == identifier), None
                )
                if from_socket is None:
                    continue  # pragma: no cover - instance lacks the socket
                self.tree.links.remove(link)
                # Removing the link can retype a reroute consumer, freeing
                # and recreating its sockets — re-resolve before relinking.
                to_socket = resolve_socket_key(to_node.inputs, to_socket_key)
                if to_socket is None:
                    continue  # pragma: no cover - socket vanished on retype
                self.tree.links.new(from_socket, to_socket)
        if splits:
            self._hide_unused_input_sockets()

    def split_group_inputs(self) -> None:
        """Split the Group Input node into one instance per consumer node,
        with unused sockets hidden — regenerating the editor style that
        avoids a single input node trailing long noodles. Runs automatically
        on context exit (before auto-layout, so the instances are arranged
        next to their consumers) when the builder was created with
        ``split_inputs=True``."""
        primary = self.tree.nodes.get("Group Input")
        if primary is None:
            return
        by_consumer: dict[str, list[tuple[str, str, str]]] = {}
        for socket in primary.outputs:
            for link in socket.links:
                by_consumer.setdefault(link.to_node.name, []).append(
                    (socket.name, link.to_node.name, socket_key(link.to_socket))
                )
        # The first consumer keeps the primary node; each further consumer
        # gets its own instance (named like Blender would on duplication).
        self.group_input_splits = [
            {"name": f"Group Input.{index:03d}", "links": by_consumer[consumer]}
            for index, consumer in enumerate(list(by_consumer)[1:], start=1)
        ]
        self._hide_unused_input_sockets()

    def _hide_unused_input_sockets(self) -> None:
        """Hide every unlinked output on every Group Input instance (the
        virtual extension socket excluded), as the editor's Hide Unused
        Sockets does."""
        for node in self.tree.nodes:
            if node.bl_idname != "NodeGroupInput":
                continue
            for socket in node.outputs:
                if not socket.identifier.startswith("__extend__"):
                    socket.hide = not socket.is_linked

    def arrange(self):
        _arrange_nodes(self.tree, self._arrange)

    def _repr_markdown_(self) -> str | None:
        """
        Return Markdown representation for Jupyter notebook display.

        This special method is called by Jupyter to display the TreeBuilder as a Mermaid diagram
        when it's the return value of a cell.
        """
        try:
            from ..export import to_mermaid

            return to_mermaid(self)
        except Exception as e:  # noqa: BLE001
            print(f"Mermaid diagram generation failed: {e}")
            return None

    def _repr_html_(self) -> str | None:
        """
        Return an interactive geonodes-web-render graph for Jupyter/Quarto.

        This is called when the TreeBuilder is the return value of a cell. The
        tree is exported to the Tree Clipper format and embedded as a Blender-
        styled, pan/zoomable graph. Returning ``None`` on failure lets the
        Mermaid ``_repr_markdown_`` fallback take over.
        """
        try:
            from ..export import to_web_render_html

            return to_web_render_html(self)
        except Exception as e:  # noqa: BLE001
            print(f"Web render generation failed: {e}")
            return None

    def _input_node(self) -> Node:
        """Get or create the Group Input node."""
        try:
            return self.tree.nodes["Group Input"]
        except KeyError:
            node = self.tree.nodes.new("NodeGroupInput")
            assert node is not None
            return node

    def _output_node(self) -> Node:
        """Get or create the Group Output node."""
        try:
            return self.tree.nodes["Group Output"]
        except KeyError:
            node = self.tree.nodes.new("NodeGroupOutput")
            assert node is not None
            return node

    def link(self, socket1: NodeSocket, socket2: NodeSocket) -> bpy.types.NodeLink:
        # Unwrap Socket wrappers to raw NodeSocket
        if not isinstance(socket1, NodeSocket):
            socket1 = socket1.socket  # type: ignore[attr-defined]
        if not isinstance(socket2, NodeSocket):
            socket2 = socket2.socket  # type: ignore[attr-defined]

        is_reroute = (
            getattr(socket1.node, "bl_idname", None) == "NodeReroute"
            or getattr(socket2.node, "bl_idname", None) == "NodeReroute"
        )
        if (
            not is_reroute
            and socket1.type not in SOCKET_COMPATIBILITY.get(socket2.type, ())
            and socket1.type != "CUSTOM"
            and socket2.type != "CUSTOM"
        ):
            raise SocketError(
                f"Incompatible socket types, {socket1.type} and {socket2.type}"
            )

        link = self.tree.links.new(socket1, socket2, handle_dynamic_sockets=True)
        assert link is not None

        # handle_dynamic_sockets=True can free and recreate an endpoint (a
        # reroute retypes its sockets to match the link), leaving socket1 /
        # socket2 dangling — read the endpoints back off the link instead.
        from_socket, to_socket = link.from_socket, link.to_socket
        assert from_socket is not None and to_socket is not None

        if (
            any(socket.is_inactive for socket in [from_socket, to_socket])
            and not self.ignore_visibility
        ):
            for socket in [from_socket, to_socket]:
                assert socket.node is not None
                if socket.is_inactive and (
                    # allow innactive sockets on some node types but we can't just blanket allow the sockets
                    # for the Mix node as it has sockets for each data type so we have to check if they are
                    # active and if they match the currently selected data type. If they are the same data type
                    # then we allow it because they poll as innative when factor is 0.0 or 1.0.
                    not _allow_innactive_sockets(socket.node)
                    and (getattr(socket.node, "data_type", None) != socket.type)
                ):
                    other = to_socket if socket is from_socket else from_socket
                    assert other.node is not None
                    direction = "input" if socket.is_output is False else "output"
                    message = (
                        f"Socket '{socket.name}' ({direction}) on node "
                        f"'{socket.node.name}' ({socket.node.bl_idname}) is inactive, "
                        f"so the link from '{other.name}' on '{other.node.name}' will "
                        "be created by Blender but ignored when evaluated. "
                        f"Socket type: {socket.bl_idname}."
                    )
                    raise RuntimeError(message)

        return link

    def add(self, name: str) -> Node:
        node = self.tree.nodes.new(name)
        assert node is not None
        node.hide = self.collapse
        if self._frame_contexts:
            node.parent = self._frame_contexts[-1]
        return node


class MaterialBuilder(TreeBuilder):
    def __init__(
        self,
        name: str = "New Material",
        *,
        collapse: bool = False,
        arrange: ArrangeMethod = "sugiyama",
        fake_user: bool = False,
        ignore_visibility: bool = False,
    ):
        material = bpy.data.materials.new(name)
        assert material is not None
        self.material = material
        self.material.use_fake_user = fake_user
        assert self.material.node_tree
        super().__init__(
            self.material.node_tree,
            collapse=collapse,
            arrange=arrange,
            fake_user=fake_user,
            ignore_visibility=ignore_visibility,
        )
