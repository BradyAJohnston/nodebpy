from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Literal, Protocol, Self, cast

import bpy
from bpy.types import (
    CompositorNodeTree,
    GeometryNodeTree,
    Node,
    NodeSocket,
    ShaderNodeTree,
)

from ..types import SOCKET_COMPATIBILITY, SOCKET_TYPES, InputAny
from ._utils import SocketError, _NodeLike, _SocketLike
from .accessor import SocketAccessor
from .mixins import LinkingMixin, OperatorMixin
from .tree import TreeBuilder

if TYPE_CHECKING:

    class _DynamicTarget(Protocol):
        """Structural type for a node that supports dynamic socket addition."""

        def _add_inputs(self, *args: Any, **kwargs: Any) -> dict[str, NodeSocket]: ...

        @property
        def inputs(self) -> SocketAccessor: ...


class BaseNode(_NodeLike, OperatorMixin, LinkingMixin):
    """Base class for all node wrappers."""

    _bl_idname: str
    _tree: TreeBuilder
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _placeholder_inputs: list[str]

    def __init__(self, node: bpy.types.Node | None = None):
        tree = (
            TreeBuilder._tree_contexts[-1] if len(TreeBuilder._tree_contexts) else None
        )
        if tree is None:
            raise RuntimeError(
                f"Node '{self.__class__.__name__}' must be created within a TreeBuilder context manager.\n"
                f"Usage:\n"
                f"  with tree:\n"
                f"      node = {self.__class__.__name__}()\n"
            )

        self._tree = tree
        self._placeholder_inputs = []
        self.node = node if node else self._tree.add(self.__class__._bl_idname)

    @property
    def tree(self) -> TreeBuilder:
        return self._tree

    @property
    def type(self) -> SOCKET_TYPES:
        return self._default_output_socket.type  # type: ignore

    @property
    def name(self) -> str:
        return str(self.node.name)

    @property
    def _default_input_socket(self) -> NodeSocket:
        if self._default_input_id is not None:
            return self.node.inputs[self.inputs._index(self._default_input_id)]
        return self.node.inputs[0]

    @property
    def _default_output_socket(self) -> NodeSocket:
        if self._default_output_id is not None:
            return self.node.outputs[self.outputs._index(self._default_output_id)]

        counter = 0
        socket = self.node.outputs[counter]
        while not socket.is_icon_visible:
            counter += 1
            socket = self.node.outputs[counter]
        return socket

    @classmethod
    def _from_node(cls, node: bpy.types.Node) -> Self:
        builder = cls()
        builder.tree.nodes.remove(builder.node)
        builder.node = node
        return builder

    @classmethod
    def _find_or_create_linked(cls, socket: NodeSocket) -> Self:
        if socket.is_output:
            if socket.links:
                for link in socket.links:
                    assert link.to_node
                    if link.to_node.bl_idname == cls._bl_idname:
                        return cls._from_node(link.to_node)
            node = cls()
            node.tree.link(socket, node.inputs._best_match(socket.type))
            return node
        else:
            if socket.links:
                for link in socket.links:
                    assert link.from_node
                    if link.from_node.bl_idname == cls._bl_idname:
                        return cls._from_node(link.from_node)

            node = cls()
            node >> socket
            return node

    def _set_input_default_value(self, input, value):
        """Set the default value for an input socket, handling type conversions."""
        if (
            hasattr(input, "type")
            and input.type == "VECTOR"
            and isinstance(value, (int, float))
        ):
            input.default_value = [value] * len(input.default_value)
        else:
            input.default_value = value

    def _establish_links(self, **kwargs: InputAny):
        input_ids = [input.identifier for input in self.node.inputs]
        for name, value in kwargs.items():
            if value is None or (
                "GridPrune" in self._bl_idname
                and name == "Threshold"
                and getattr(self.node, "data_type", None) == "BOOLEAN"
            ):
                continue
            if isinstance(value, Node):
                node = BaseNode.__new__(BaseNode)
                node.node = value
                value = node

            if value is ...:
                self._placeholder_inputs.append(name)
                continue

            elif isinstance(value, _SocketLike):
                self._link_from(value.socket, name)
            elif isinstance(value, NodeSocket):
                self._link_from(value, name)
            elif isinstance(value, _NodeLike):
                self._link_from(
                    value.outputs._best_match(self.inputs._get(name).type), name
                )
            else:
                if name in input_ids:
                    input = self.node.inputs[input_ids.index(name)]
                    self._set_input_default_value(input, value)
                else:
                    if name in self.node.inputs:
                        input = self.node.inputs[name]
                    else:
                        input = self.node.inputs[name.replace("_", " ").title()]
                    self._set_input_default_value(input, value)

    @property
    def outputs(self) -> SocketAccessor:
        return SocketAccessor(self.node.outputs, "output")

    @property
    def inputs(self) -> SocketAccessor:
        return SocketAccessor(self.node.inputs, "input")

    @property
    def o(self) -> SocketAccessor:
        """Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING."""
        return SocketAccessor(self.node.outputs, "output")

    @property
    def i(self) -> SocketAccessor:
        """Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING."""
        return SocketAccessor(self.node.inputs, "input")


class DynamicInputsMixin:
    _socket_data_types: tuple[str, ...]
    _type_map: dict[str, str] = {}

    def _match_compatible_data(
        self, sockets: Iterable[NodeSocket]
    ) -> tuple[NodeSocket, str]:
        possible = []
        for socket in sockets:
            compatible = SOCKET_COMPATIBILITY.get(socket.type, ())
            for type in self._socket_data_types:
                if type in compatible:
                    possible.append((socket, type, compatible.index(type)))

        if len(possible) > 0:
            possible.sort(key=lambda x: x[2])
            best_value = possible[0]
            return best_value[:2]

        raise SocketError("No compatible socket found")

    def _find_best_socket_pair(
        self, source: BaseNode | NodeSocket, target: BaseNode | NodeSocket
    ) -> tuple[NodeSocket, NodeSocket]:
        try:
            return super()._find_best_socket_pair(source, target)  # type: ignore
        except SocketError:
            dyn = cast("_DynamicTarget", target)
            target_name, source_socket = list(dyn._add_inputs(source).items())[0]
            return (source_socket, dyn.inputs[target_name].socket)

    def _add_socket(self, name: str, *args: Any, **kwargs: Any) -> NodeSocket:
        raise NotImplementedError(f"{type(self).__name__} must implement _add_socket")

    def _add_inputs(self, *args, **kwargs) -> dict[str, NodeSocket]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        items = {}
        for arg in args:
            items[arg._default_output_socket.name] = arg
        items.update(kwargs)
        for key, source in items.items():
            socket_source, type = self._match_compatible_data(source.outputs._available)
            if type in self._type_map:
                type = self._type_map[type]
            socket = self._add_socket(name=key, type=type)
            new_sockets[socket.name] = socket_source

        return new_sockets


class NodeGroupBuilder(BaseNode, ABC):
    """Base class for custom node groups.

    Subclasses implement :meth:`_build_group` with the node-graph logic.
    Subclass one of the editor-specific variants: :class:`GeometryNodeGroup`,
    :class:`ShaderNodeGroup`, or :class:`CompositorNodeGroup`.
    """

    _name: str

    def __init__(self, **kwargs):
        super().__init__()
        self._setup_node_group()
        self.node.show_options = False
        self._establish_links(**kwargs)

    @abstractmethod
    def _setup_node_group(self) -> None:
        """Set ``self.node.node_tree`` and any node-type-specific properties.

        Called by ``__init__`` after the node is created but before links are
        established. Concrete subclasses have a narrowed ``self.node`` type,
        so the ``node_tree`` assignment is type-safe here rather than in the
        base class where ``self.node`` is only ``bpy.types.Node``.
        """
        ...

    @abstractmethod
    def _build_group(self, tree: TreeBuilder) -> None:
        """Build the node group internals and interface."""


class GeometryNodeGroup(NodeGroupBuilder):
    """Node group in a Geometry Nodes tree."""

    _bl_idname = "GeometryNodeGroup"
    _warning_propagation: Literal["ALL", "ERRORS_AND_WARNINGS", "ERRORS", "NONE"] = (
        "ALL"
    )
    _color_tag: Literal[
        "NONE",
        "ATTRIBUTE",
        "COLOR",
        "CONVERTER",
        "GEOMETRY",
        "INPUT",
        "OUTPUT",
        "TEXTURE",
        "VECTOR",
    ] = "NONE"
    node: bpy.types.GeometryNodeGroup

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()
        self.node.warning_propagation = self._warning_propagation

    def _get_or_create_group(self) -> GeometryNodeTree:
        if self._name in bpy.data.node_groups:
            existing = bpy.data.node_groups[self._name]
            if isinstance(existing, GeometryNodeTree):
                return existing
            raise TypeError(
                f"Node group '{self._name}' already exists as "
                f"{type(existing).__name__}, not GeometryNodeTree. "
                f"Use a unique _name for this group."
            )
        with TreeBuilder.geometry(self._name) as tree:
            self._build_group(tree)
        tree.tree.color_tag = self._color_tag
        return tree.tree


class ShaderNodeGroup(NodeGroupBuilder):
    """Node group in a Shader (Material) node tree."""

    _bl_idname = "ShaderNodeGroup"
    node: bpy.types.ShaderNodeGroup

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()

    def _get_or_create_group(self) -> ShaderNodeTree:
        if self._name in bpy.data.node_groups:
            existing = bpy.data.node_groups[self._name]
            if isinstance(existing, ShaderNodeTree):
                return existing
            raise TypeError(
                f"Node group '{self._name}' already exists as "
                f"{type(existing).__name__}, not ShaderNodeTree. "
                f"Use a unique _name for this group."
            )
        with TreeBuilder.shader(self._name) as tree:
            self._build_group(tree)
        return tree.tree


class CompositorNodeGroup(NodeGroupBuilder):
    """Node group in a Compositor node tree."""

    _bl_idname = "CompositorNodeGroup"
    node: bpy.types.CompositorNodeGroup

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()

    def _get_or_create_group(self) -> CompositorNodeTree:
        if self._name in bpy.data.node_groups:
            existing = bpy.data.node_groups[self._name]
            if isinstance(existing, CompositorNodeTree):
                return existing
            raise TypeError(
                f"Node group '{self._name}' already exists as "
                f"{type(existing).__name__}, not CompositorNodeTree. "
                f"Use a unique _name for this group."
            )
        with TreeBuilder.compositor(self._name) as tree:
            self._build_group(tree)
        return tree.tree
