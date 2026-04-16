from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Literal

import bpy
from bpy.types import Node, NodeSocket

from ..types import SOCKET_COMPATIBILITY, SOCKET_TYPES, InputAny, InputLinkable
from ._utils import SocketError, _NodeLike, _SocketLike
from .accessor import SocketAccessor
from .mixins import LinkingMixin, OperatorMixin
from .tree import TreeBuilder

if TYPE_CHECKING:
    pass


class BaseNode(_NodeLike, OperatorMixin, LinkingMixin):
    """Base class for all node wrappers."""

    node: bpy.types.Node
    _bl_idname: str
    _tree: TreeBuilder
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _placeholder_inputs: list[str]

    def __init__(self):
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
        self.node = self._tree.add(self.__class__._bl_idname)

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
                and self.node.data_type == "BOOLEAN"
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
                self._link_from(value, name)
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
        """Output socket accessor. Typed subclasses override this on generated nodes."""
        return self.outputs

    @property
    def i(self) -> SocketAccessor:
        """Input socket accessor. Typed subclasses override this on generated nodes."""
        return self.inputs


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
            target_name, source_socket = list(target._add_inputs(source).items())[0]
            return (source_socket, target.inputs[target_name].socket)

    def _add_inputs(self, *args, **kwargs) -> dict[str, InputLinkable]:
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
    """

    _name: str
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

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "Inputs" in cls.__dict__:
            cls.i = property(lambda self, c=cls: c.Inputs(self.node.inputs, "input"))
        if "Outputs" in cls.__dict__:
            cls.o = property(lambda self, c=cls: c.Outputs(self.node.outputs, "output"))

    def __init__(self, **kwargs):
        super().__init__()
        self.node.node_tree = self._get_or_create_group()
        self.node.show_options = False
        self.node.warning_propagation = self._warning_propagation
        self._establish_links(**kwargs)

    def _get_or_create_group(self) -> bpy.types.GeometryNodeTree:
        name = self._name
        if name in bpy.data.node_groups:
            return bpy.data.node_groups[name]

        with TreeBuilder(name) as tree:
            self._build_group(tree)
            tree.tree.color_tag = self._color_tag

        return tree.tree

    @classmethod
    @abstractmethod
    def _build_group(cls, tree: TreeBuilder) -> None:
        """Code that builds the node group internals and interface"""
