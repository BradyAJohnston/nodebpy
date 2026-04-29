from __future__ import annotations

from typing import Any, ClassVar, Generic, Literal, Self, TypeVar, cast

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

from ..arrange import arrange_tree
from ..types import (
    SOCKET_COMPATIBILITY,
    FloatInterfaceSubtypes,
    IntegerInterfaceSubtypes,
    StringInterfaceSubtypes,
    VectorInterfaceSubtypes,
    _AttributeDomains,
    _SocketShapeStructureType,
)
from ._utils import SocketError, _allow_innactive_sockets
from .socket import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    CollectionSocket,
    ColorSocket,
    FloatSocket,
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
    StringSocket,
    VectorSocket,
)

_SocketT = TypeVar("_SocketT", bound=Socket)


class PanelContext:
    """Context manager for grouping sockets into a panel."""

    def __init__(
        self,
        socket_context: "SocketContext",
        name: str,
        *,
        default_closed: bool = False,
    ):
        self._socket_context = socket_context
        self._name = name
        self._default_closed = default_closed
        self._panel: bpy.types.NodeTreeInterfacePanel | None = None

    def __enter__(self):
        self._panel = self._socket_context.interface.new_panel(
            self._name, default_closed=self._default_closed
        )
        self._socket_context._active_panel = self._panel
        return self

    def __exit__(self, *args):
        self._socket_context._active_panel = None


class SocketContext:
    _direction: Literal["INPUT", "OUTPUT"] | None

    def __init__(self, tree_builder: "TreeBuilder"):
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

    def panel(self, name: str, *, default_closed: bool = False) -> PanelContext:
        """Create a panel context for grouping sockets."""
        return PanelContext(self, name, default_closed=default_closed)

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
        interface_socket.description = description
        return interface_socket

    def _set_props(
        self, interface_socket: bpy.types.NodeTreeInterfaceSocket, **kwargs: Any
    ) -> None:
        for key, value in kwargs.items():
            if value is None:
                continue
            if (
                interface_socket.socket_type == "NodeSocketMenu"
                and key == "default_value"
            ):
                self.builder._menu_defaults[interface_socket.identifier] = value
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
        s.interface_socket = interface_socket
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
    ) -> "FloatSocket":
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
        default_input: Literal["INDEX", "VALUE", "ID_OR_INDEX"] = "VALUE",
        subtype: IntegerInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ) -> "IntegerSocket":
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
    ) -> "BooleanSocket":
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
        )
        return self._wrap(BooleanSocket, iface)

    def vector(
        self,
        name: str = "Vector",
        default_value: tuple[float, float, float] = (0.0, 0.0, 0.0),  # ty: ignore[invalid-type-form]
        description: str = "",
        *,
        dimensions: int = 3,
        min_value: float | None = None,  # ty: ignore[invalid-type-form]
        max_value: float | None = None,  # ty: ignore[invalid-type-form]
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
    ) -> "VectorSocket":
        assert len(default_value) == dimensions, (
            "Default value length must match dimensions"
        )
        iface = self._add_socket("NodeSocketVector", name, description)
        self._set_props(
            iface,
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
    ) -> "ColorSocket":
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
    ) -> "RotationSocket":
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
        default_input: Literal["VALUE", "INSTANCE_TRANSFORM"] = "VALUE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ) -> "MatrixSocket":
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
    ) -> "StringSocket":
        iface = self._add_socket("NodeSocketString", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            subtype=subtype,
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
    ) -> "MenuSocket":
        iface = self._add_socket("NodeSocketMenu", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            menu_expanded=expanded,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
            structure_type=structure_type,
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
    ) -> "ObjectSocket":
        iface = self._add_socket("NodeSocketObject", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "GeometrySocket":
        iface = self._add_socket("NodeSocketGeometry", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "CollectionSocket":
        iface = self._add_socket("NodeSocketCollection", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "ImageSocket":
        iface = self._add_socket("NodeSocketImage", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "MaterialSocket":
        iface = self._add_socket("NodeSocketMaterial", name, description)
        self._set_props(
            iface,
            default_value=default_value,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )
        return self._wrap(MaterialSocket, iface)

    def bundle(
        self,
        name: str = "Bundle",
        description: str = "",
        *,
        optional_label: bool = False,
        hide_value: bool = False,
        hide_in_modifier: bool = False,
    ) -> "BundleSocket":
        iface = self._add_socket("NodeSocketBundle", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "ClosureSocket":
        iface = self._add_socket("NodeSocketClosure", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
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
    ) -> "ShaderSocket":
        iface = self._add_socket("NodeSocketShader", name, description)
        self._set_props(
            iface,
            optional_label=optional_label,
            hide_value=hide_value,
            hide_in_modifier=hide_in_modifier,
        )
        return self._wrap(ShaderSocket, iface)

    def __len__(self) -> int:
        return len(
            list(
                item
                for item in self.tree.interface.items_tree
                if item.in_out == self._direction
            )
        )


class DirectionalContext(SocketContext):
    """Base class for directional socket contexts"""

    _direction = "INPUT"


class InputInterfaceContext(DirectionalContext):
    _direction = "INPUT"


class OutputInterfaceContext(DirectionalContext):
    _direction = "OUTPUT"


_TreeT = TypeVar("_TreeT", bound=NodeTree)


class TreeBuilder(Generic[_TreeT]):
    """Builder for creating Blender node trees with a clean Python API.

    Supports geometry, shader, and compositor node trees.
    """

    tree: _TreeT
    _tree_contexts: ClassVar["list[TreeBuilder]"] = []
    _frame_contexts: ClassVar["list[NodeFrame]"] = []

    def __init__(
        self,
        tree: NodeTree | str = "Geometry Nodes",
        *,
        tree_type: Literal[
            "GeometryNodeTree", "ShaderNodeTree", "CompositorNodeTree"
        ] = "GeometryNodeTree",
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
        ignore_visibility: bool = False,
    ):
        if isinstance(tree, str):
            self.tree = bpy.data.node_groups.new(tree, tree_type)  # type: ignore[assignment]
        else:
            self.tree = tree  # type: ignore[assignment]

        self._menu_defaults: dict[str, str] = {}
        self.inputs = InputInterfaceContext(self)
        self.outputs = OutputInterfaceContext(self)
        self._arrange = arrange
        self.collapse = collapse
        self.fake_user = fake_user
        self.ignore_visibility = ignore_visibility

    @classmethod
    def geometry(
        cls,
        name: GeometryNodeTree | str = "Geometry Nodes",
        *,
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
    ) -> "TreeBuilder[GeometryNodeTree]":
        """Create a geometry node tree."""
        return cast(
            "TreeBuilder[GeometryNodeTree]",
            cls(
                name,
                tree_type="GeometryNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
            ),
        )

    @classmethod
    def shader(
        cls,
        name: ShaderNodeTree | str = "Shader Nodes",
        *,
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
    ) -> "TreeBuilder[ShaderNodeTree]":
        """Create a shader node tree."""
        return cast(
            "TreeBuilder[ShaderNodeTree]",
            cls(
                name,
                tree_type="ShaderNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
            ),
        )

    @classmethod
    def compositor(
        cls,
        name: CompositorNodeTree | str = "Compositor Nodes",
        *,
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
    ) -> "TreeBuilder[CompositorNodeTree]":
        """Create a compositor node tree."""
        return cast(
            "TreeBuilder[CompositorNodeTree]",
            cls(
                name,
                tree_type="CompositorNodeTree",
                collapse=collapse,
                arrange=arrange,
                fake_user=fake_user,
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

    def activate_tree(self) -> None:
        """Make this tree the active tree for all new node creation."""
        TreeBuilder._tree_contexts.append(self)

    def deactivate_tree(self) -> None:
        """Whatever tree was previously active is set to be the active one (or None if no previously active tree)."""
        TreeBuilder._tree_contexts.pop()

    def __enter__(self) -> Self:
        self.activate_tree()
        return self

    def __exit__(self, *args):
        if self._arrange is not None:
            self.arrange()
        self._apply_input_defaults()
        self.deactivate_tree()

    def _apply_input_defaults(self) -> None:
        for key, value in self._menu_defaults.items():
            for item in self.tree.interface.items_tree:  # type: ignore
                if not hasattr(item, "identifier"):
                    continue
                if item.identifier == key:
                    if hasattr(item, "default_value"):
                        item.default_value = value

    def __len__(self) -> int:
        return len(self.nodes)

    def arrange(self):
        if self._arrange == "sugiyama":
            try:
                from ..lib.nodearrange import arrange as nodearrange

                nodearrange.sugiyama.sugiyama_layout(self.tree)
                nodearrange.sugiyama.config.reset()
            except ImportError as e:
                if "networkx" not in str(e):
                    raise
                import warnings

                warnings.warn(
                    "networkx is not installed, falling back to simple arrangement. "
                    "Install networkx for the Sugiyama layout: pip install nodebpy[networkx]",
                    stacklevel=2,
                )
                arrange_tree(self.tree)
        elif self._arrange == "simple":
            arrange_tree(self.tree)

    def _repr_markdown_(self) -> str | None:
        """
        Return Markdown representation for Jupyter notebook display.

        This special method is called by Jupyter to display the TreeBuilder as a Mermaid diagram
        when it's the return value of a cell.
        """
        try:
            from ..diagram import to_mermaid

            return to_mermaid(self)
        except Exception as e:
            print(f"Mermaid diagram generation failed: {e}")
            return None

    def _input_node(self) -> Node:
        """Get or create the Group Input node."""
        try:
            return self.tree.nodes["Group Input"]
        except KeyError:
            return self.tree.nodes.new("NodeGroupInput")

    def _output_node(self) -> Node:
        """Get or create the Group Output node."""
        try:
            return self.tree.nodes["Group Output"]
        except KeyError:
            return self.tree.nodes.new("NodeGroupOutput")

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

        if (
            any(socket.is_inactive for socket in [socket1, socket2])
            and not self.ignore_visibility
        ):
            assert socket1.node
            assert socket2.node
            for socket in [socket1, socket2]:
                if socket.is_inactive and not _allow_innactive_sockets(socket.node):
                    message = f"Socket {socket.name} from node {socket.node.name} is inactive."  # type: ignore
                    message += f" It is linked to socket {socket2.name} from node {socket2.node.name}."
                    message += " This link will be created by Blender but ignored when evaluated."
                    message += f"Socket type: {socket.bl_idname}"
                    raise RuntimeError(message)

        return link

    def add(self, name: str) -> Node:
        node = self.tree.nodes.new(name)
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
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
        ignore_visibility: bool = False,
    ):
        self.material = bpy.data.materials.new(name)
        self.material.use_fake_user = fake_user
        assert self.material.node_tree
        super().__init__(
            self.material.node_tree,
            collapse=collapse,
            arrange=arrange,
            fake_user=fake_user,
            ignore_visibility=ignore_visibility,
        )
