from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal

import bpy
from bpy.types import (
    CompositorNodeTree,
    GeometryNodeTree,
    Node,
    Nodes,
    NodeSocket,
    NodeTree,
    ShaderNodeTree,
)

from ..arrange import arrange_tree
from ..types import SOCKET_COMPATIBILITY
from ._utils import SocketError, _allow_innactive_sockets

if TYPE_CHECKING:
    from .interface import InterfaceSocket


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
    _active_context: "SocketContext | None" = None

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

    def _create_socket(
        self, socket_def: "InterfaceSocket", name: str
    ) -> bpy.types.NodeTreeInterfaceSocket:
        """Create a socket from a socket definition."""
        kwargs: dict[str, Any] = {
            "name": name,
            "in_out": self._direction,
            "socket_type": socket_def._bl_socket_type,
        }
        if self._active_panel is not None:
            kwargs["parent"] = self._active_panel
        socket = self.interface.new_socket(**kwargs)
        socket.description = socket_def.description
        return socket

    def __enter__(self):
        SocketContext._active_context = self
        return self

    def __exit__(self, *args):
        SocketContext._direction = None
        SocketContext._active_context = None


class DirectionalContext(SocketContext):
    """Base class for directional socket contexts"""

    _direction = "INPUT"
    _active_context = None


class InputInterfaceContext(DirectionalContext):
    _direction = "INPUT"


class OutputInterfaceContext(DirectionalContext):
    _direction = "OUTPUT"


class TreeBuilder:
    """Builder for creating Blender node trees with a clean Python API.

    Supports geometry, shader, and compositor node trees.
    """

    _tree_contexts: ClassVar["list[TreeBuilder]"] = []

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
            self.tree = bpy.data.node_groups.new(tree, tree_type)
        else:
            self.tree = tree

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
    ) -> "TreeBuilder":
        """Create a geometry node tree."""
        return cls(
            name,
            tree_type="GeometryNodeTree",
            collapse=collapse,
            arrange=arrange,
            fake_user=fake_user,
        )

    @classmethod
    def shader(
        cls,
        name: ShaderNodeTree | str = "Shader Nodes",
        *,
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
    ) -> "TreeBuilder":
        """Create a shader node tree."""
        return cls(
            name,
            tree_type="ShaderNodeTree",
            collapse=collapse,
            arrange=arrange,
            fake_user=fake_user,
        )

    @classmethod
    def compositor(
        cls,
        name: CompositorNodeTree | str = "Compositor Nodes",
        *,
        collapse: bool = False,
        arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
        fake_user: bool = False,
    ) -> "TreeBuilder":
        """Create a compositor node tree."""
        return cls(
            name,
            tree_type="CompositorNodeTree",
            collapse=collapse,
            arrange=arrange,
            fake_user=fake_user,
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

    def __enter__(self):
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
                if item.identifier == key:  # type: ignore
                    item.default_value = value  # type: ignore
                    break

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
            from ..screenshot import generate_mermaid_diagram

            return generate_mermaid_diagram(self)
        except Exception as e:
            print(f"Mermaid diagram generation failed: {e}")
            return None

    def _input_node(self) -> Node:
        """Get or create the Group Input node."""
        try:
            return self.tree.nodes["Group Input"]  # type: ignore
        except KeyError:
            return self.tree.nodes.new("NodeGroupInput")  # type: ignore

    def _output_node(self) -> Node:
        """Get or create the Group Output node."""
        try:
            return self.tree.nodes["Group Output"]  # type: ignore
        except KeyError:
            return self.tree.nodes.new("NodeGroupOutput")  # type: ignore

    def link(self, socket1: NodeSocket, socket2: NodeSocket) -> bpy.types.NodeLink:
        # Unwrap Socket wrappers to raw NodeSocket
        if not isinstance(socket1, NodeSocket):
            socket1 = socket1.socket  # type: ignore[attr-defined]
        if not isinstance(socket2, NodeSocket):
            socket2 = socket2.socket  # type: ignore[attr-defined]

        if (
            socket1.type not in SOCKET_COMPATIBILITY.get(socket2.type, ())
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
        return node
