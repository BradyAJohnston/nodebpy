from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Literal,
    Mapping,
    Protocol,
    Self,
    TypeVar,
    cast,
    dataclass_transform,
)

import bpy
from bpy.types import (
    CompositorNodeGroup,
    CompositorNodeTree,
    GeometryNodeGroup,
    GeometryNodeTree,
    Node,
    NodeSocket,
    NodeTree,
    ShaderNodeGroup,
    ShaderNodeTree,
)

from ..types import SOCKET_COMPATIBILITY, SOCKET_TYPES, InputAny
from ._utils import SocketError, _NodeLike, _SocketLike
from .accessor import SocketAccessor
from .group_fields import _INPUT_FIELDS, InputField, OutputField
from .mixins import LinkingMixin, OperatorMixin
from .tree import TreeBuilder

_T = TypeVar("_T", bound=bpy.types.NodeTree)

if TYPE_CHECKING:

    class _DynamicTarget(Protocol):
        """Structural type for a node that supports dynamic socket addition."""

        def _add_inputs(self, *args: Any, **kwargs: Any) -> dict[str, NodeSocket]: ...

        @property
        def i(self) -> SocketAccessor: ...


def _find_socket_from_name(
    collection: bpy.types.NodeInputs | bpy.types.NodeOutputs | list[NodeSocket],
    name: str,
) -> NodeSocket:
    ids = [socket.identifier for socket in collection]
    names = [socket.name for socket in collection]
    for format in [name, name.title(), name.replace("_", " ").title()]:
        try:
            return collection[names.index(format)]
        except ValueError:
            try:
                return collection[ids.index(format)]
            except ValueError:
                continue
    raise ValueError(
        f"Socket '{name}' not found in collection names or ids, available names: {names}, available ids: {ids}"
    )


class BaseNode(_NodeLike, OperatorMixin, LinkingMixin):
    """Base class for all node wrappers."""

    _bl_idname: str
    _tree: TreeBuilder
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _placeholder_inputs: list[str]

    def __init__(self, node: Node | None = None):
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
            return self.node.inputs[self.i._index(self._default_input_id)]
        return self.node.inputs[0]

    @property
    def _default_output_socket(self) -> NodeSocket:
        if self._default_output_id is not None:
            return self.node.outputs[self.o._index(self._default_output_id)]

        counter = 0
        socket = self.node.outputs[counter]
        while not socket.is_icon_visible:
            counter += 1
            socket = self.node.outputs[counter]
        return socket

    @classmethod
    def _from_node(cls, node: Node) -> Self:
        builder = cls.__new__(cls)
        builder._tree = TreeBuilder(cast(NodeTree, node.id_data))
        builder._placeholder_inputs = []
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
            node.tree.link(socket, node.i._best_match(socket.type))
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

    def _set_input_default_value(self, input: NodeSocket, value: Any) -> None:
        """Set the default value for an input socket, handling type conversions."""
        assert hasattr(input, "default_value")
        if (
            hasattr(input, "type")
            and input.type == "VECTOR"
            and isinstance(value, (int, float))
        ):
            input.default_value = [value] * len(input.default_value)  # type: ignore
        else:
            input.default_value = value  # type: ignore

    def _establish_links(self, **kwargs: InputAny):
        for name, value in kwargs.items():
            # TODO: don't like these manual overrides for particular nodes, but best I can do for now
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
                self._link_from(value.o._best_match(self.i._get(name).type), name)  # type: ignore
            else:
                # TODO: explicitly skipping the sockets for BooleanMath as they are default false,
                # but this needs to be a more generic solution for sockets which aren't available
                # https://github.com/BradyAJohnston/nodebpy/issues/90
                if "BooleanMath" in self._bl_idname and value is False:
                    continue
                socket = _find_socket_from_name(self.node.inputs, name)
                self._set_input_default_value(socket, value)

    @property
    def o(self) -> SocketAccessor:
        """Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING."""
        return SocketAccessor(self.node.outputs, "output", builder=self)

    @property
    def i(self) -> SocketAccessor:
        """Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING."""
        return SocketAccessor(self.node.inputs, "input", builder=self)


class DynamicInputsMixin(ABC):
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
            return (source_socket, dyn.i[target_name].socket)

    @abstractmethod
    def _add_socket(self, name: str, *args: Any, **kwargs: Any) -> NodeSocket: ...

    def _add_inputs(self, *args, **kwargs) -> dict[str, NodeSocket]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        items = {}
        for arg in args:
            items[arg._default_output_socket.name] = arg
        items.update(kwargs)
        for key, source in items.items():
            socket_source, type = self._match_compatible_data(
                source.o._available if hasattr(source, "o") else [source]
            )
            if type in self._type_map:
                type = self._type_map[type]
            socket = self._add_socket(name=key, type=type)
            new_sockets[socket.name] = socket_source

        return new_sockets


class _GroupSocketAccessor(SocketAccessor):
    """A ``SocketAccessor`` that resolves attribute access via the group's
    declared fields, so a python field name maps to its (possibly overridden)
    Blender socket name — e.g. ``self.i.group_id`` -> ``"Group ID"``.
    """

    def __init__(
        self,
        collection: Any,
        direction: Any,
        *,
        builder: BaseNode,
        fields: Mapping[str, InputField | OutputField],
    ) -> None:
        super().__init__(collection, direction, builder=builder)
        self._fields = fields

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        field = self._fields.get(name)
        try:
            return self._get(field.display_name if field is not None else name)
        except RuntimeError:
            raise AttributeError(
                f"Socket '{name}' not found on {self._direction} accessor"
            )


@dataclass_transform(field_specifiers=_INPUT_FIELDS)
class NodeGroupBuilder(BaseNode, ABC, Generic[_T]):
    """Base class for custom node groups.

    Subclasses declare inputs as class-level :class:`~nodebpy.builder.group_fields.InputField`
    descriptors (``vertex_index: IntegerIn = IntegerIn(...)``) and outputs in a
    nested ``_Outputs`` class. The input declarations drive a fully typed
    constructor (via ``@dataclass_transform``), typed ``self.i.x`` access, the
    ``py-name -> display-name`` mapping, and the node-group interface built on
    first use. Graph logic goes in :meth:`_build_group`, reading inputs from
    ``self.i`` and linking results into ``self.o`` with ``>>``.

    Subclass one of the editor-specific variants: :class:`CustomGeometryGroup`,
    :class:`CustomShaderGroup`, or :class:`CustomCompositorGroup`.
    """

    _name: str
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

    # Populated by __init_subclass__ from the class body / nested _Outputs.
    _group_inputs: dict[str, InputField] = {}
    _group_outputs: dict[str, OutputField] = {}
    # Set to the inner TreeBuilder only while _build_group runs, so that
    # ``self.i`` / ``self.o`` resolve to the group's interface sockets.
    _build_tree: TreeBuilder | None = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._group_inputs = {
            name: field
            for name, field in vars(cls).items()
            if isinstance(field, InputField)
        }
        outputs_cls = vars(cls).get("_Outputs")
        cls._group_outputs = (
            {
                name: field
                for name, field in vars(outputs_cls).items()
                if isinstance(field, OutputField)
            }
            if outputs_cls is not None
            else {}
        )

    def __init__(self, **kwargs: Any):
        # Translate python field names to Blender socket names. Unknown keys are
        # passed through unchanged to support groups still using the explicit
        # ``super().__init__(**{"Display Name": value})`` style.
        link_kwargs: dict[str, Any] = {}
        for key, value in kwargs.items():
            field = type(self)._group_inputs.get(key)
            link_kwargs[field.display_name if field is not None else key] = value
        super().__init__()
        self._setup_node_group()
        self.node.show_options = False
        self._establish_links(**link_kwargs)

    if TYPE_CHECKING:
        # Inputs are exposed via ``self.i`` as the node itself, so the typed
        # InputField descriptors resolve (``self.i.vertex_index -> IntegerSocket``).
        # Subclasses narrow ``o`` to their nested ``_Outputs`` type.
        @property
        def i(self) -> Self: ...
    else:

        @property
        def i(self) -> SocketAccessor:
            collection = (
                self._build_tree._input_node().outputs
                if self._build_tree is not None
                else self.node.inputs
            )
            return _GroupSocketAccessor(
                collection, "input", builder=self, fields=type(self)._group_inputs
            )

    @property
    def o(self) -> SocketAccessor:
        """Output socket accessor (build-aware). Subclasses narrow the type."""
        collection = (
            self._build_tree._output_node().inputs
            if self._build_tree is not None
            else self.node.outputs
        )
        return _GroupSocketAccessor(
            collection, "output", builder=self, fields=type(self)._group_outputs
        )

    def _build_interface(self, tree: TreeBuilder) -> None:
        """Create the group's interface sockets from the declared fields."""
        self._build_sockets(tree.inputs, type(self)._group_inputs.values())
        self._build_sockets(tree.outputs, type(self)._group_outputs.values())

    @staticmethod
    def _build_sockets(
        context: Any, fields: Iterable[InputField | OutputField]
    ) -> None:
        """Create sockets in declaration order, grouping consecutive ``panel=`` runs."""
        open_panel = None
        current_panel: str | None = None
        try:
            for field in fields:
                if field._panel != current_panel:
                    if open_panel is not None:
                        open_panel.__exit__()
                    current_panel = field._panel
                    open_panel = (
                        context.panel(
                            current_panel, default_closed=field._panel_closed
                        ).__enter__()
                        if current_panel is not None
                        else None
                    )
                args, props = field._build_kwargs()
                getattr(context, field._method)(*args, **props)
        finally:
            if open_panel is not None:
                open_panel.__exit__()

    def _populate_group(self, tree: TreeBuilder) -> None:
        """Build the interface, then run the user's graph logic against it."""
        self._build_interface(tree)
        self._build_tree = tree
        try:
            self._build_group(tree)
        finally:
            self._build_tree = None

    @property
    @abstractmethod
    def node_tree(self) -> _T:
        """The internal node tree for this group node."""
        ...

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

    def _get_or_create_tree(self) -> _T:
        existing = bpy.data.node_groups[self._name]
        if existing.bl_idname == self.tree.tree.bl_idname:
            return cast(_T, existing)
        raise TypeError(
            f"Node group '{self._name}' already exists as "
            f"{type(existing).__name__}, not {self._bl_idname}. "
            f"Use a unique _name for this group."
        )


class CustomGeometryGroup(NodeGroupBuilder[GeometryNodeTree]):
    """Node group in a Geometry Nodes tree."""

    _bl_idname = "GeometryNodeGroup"

    if TYPE_CHECKING:
        # Narrows ``self.node`` without becoming a dataclass-transform field.
        @property
        def node(self) -> GeometryNodeGroup: ...  # type: ignore[override]

    @property
    def node_tree(self) -> GeometryNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()
        self.node.warning_propagation = self._warning_propagation

    def _get_or_create_group(self) -> GeometryNodeTree:
        try:
            return self._get_or_create_tree()
        except KeyError:
            with TreeBuilder.geometry(self._name) as tree:
                self._populate_group(tree)
            tree.tree.color_tag = self._color_tag
            return tree.tree


class CustomShaderGroup(NodeGroupBuilder[ShaderNodeTree]):
    """Node group in a Shader (Material) node tree."""

    _bl_idname = "ShaderNodeGroup"

    if TYPE_CHECKING:
        # Narrows ``self.node`` without becoming a dataclass-transform field.
        @property
        def node(self) -> ShaderNodeGroup: ...  # type: ignore[override]

    @property
    def node_tree(self) -> ShaderNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()

    def _get_or_create_group(self) -> ShaderNodeTree:
        try:
            return self._get_or_create_tree()
        except KeyError:
            with TreeBuilder.shader(self._name) as tree:
                self._populate_group(tree)
            tree.tree.color_tag = self._color_tag
            return tree.tree


class CustomCompositorGroup(NodeGroupBuilder[CompositorNodeTree]):
    """Node group in a Compositor node tree."""

    _bl_idname = "CompositorNodeGroup"

    if TYPE_CHECKING:
        # Narrows ``self.node`` without becoming a dataclass-transform field.
        @property
        def node(self) -> CompositorNodeGroup: ...  # type: ignore[override]

    @property
    def node_tree(self) -> CompositorNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self._get_or_create_group()

    def _get_or_create_group(self) -> CompositorNodeTree:
        try:
            return self._get_or_create_tree()
        except KeyError:
            with TreeBuilder.compositor(self._name) as tree:
                self._populate_group(tree)
            tree.tree.color_tag = self._color_tag
            return tree.tree
