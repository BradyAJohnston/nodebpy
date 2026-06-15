from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Literal,
    Protocol,
    Self,
    TypeVar,
    cast,
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

from ..types import SOCKET_COMPATIBILITY, InputAny
from ._utils import SocketError, _NodeLike, _SocketLike
from .accessor import SocketAccessor
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
    # An exact identifier match wins (aligning with SocketAccessor's
    # identifier-first strategy). Item sockets may share a name with another
    # socket — e.g. a CaptureAttribute item named "Value" alongside the item
    # whose identifier is "Value" — so the unambiguous identifier must take
    # precedence over a name match before the name-normalising passes below.
    if name in ids:
        return collection[ids.index(name)]
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


def _value_socket_type(value: Any) -> str | None:
    """The Blender socket ``type`` an input value carries, when knowable —
    used to disambiguate same-named target sockets. ``None`` for plain
    defaults and multi-output nodes (resolution then falls back to order)."""
    if isinstance(value, _SocketLike):
        return value.socket.type
    if isinstance(value, NodeSocket):
        return value.type
    if isinstance(value, Node):
        return value.outputs[0].type if value.outputs else None
    if isinstance(value, _NodeLike):
        default = getattr(value, "_default_output_socket", None)
        return default.type if default is not None else None
    return None


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
        """The `TreeBuilder` instance this node belongs to and is being built within."""
        return self._tree

    @property
    def name(self) -> str:
        """The name of the node being wrapped by this instance."""
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
        stype = getattr(input, "type", None)
        if stype == "VECTOR" and isinstance(value, (int, float)):
            input.default_value = [value] * len(input.default_value)  # type: ignore
        elif stype == "INT" and isinstance(value, float):
            input.default_value = int(value)  # type: ignore
        else:
            input.default_value = value  # type: ignore

    def _establish_links(self, **kwargs: InputAny):
        for name, value in kwargs.items():
            self._apply_input(name, value)

    def _apply_input(self, target: "str | NodeSocket", value: InputAny):
        """Link or default-set ``value`` onto an input.

        ``target`` is a socket name/identifier (resolved against
        ``self.node.inputs``) or an already-resolved input socket — the latter
        lets callers address one of several same-named sockets unambiguously.
        """
        named = isinstance(target, str)
        # TODO: don't like these manual overrides for particular nodes, but best I can do for now
        if value is None or (
            named
            and "GridPrune" in self._bl_idname
            and target == "Threshold"
            and getattr(self.node, "data_type", None) == "BOOLEAN"
        ):
            return
        if isinstance(value, Node):
            node = BaseNode.__new__(BaseNode)
            node.node = value
            value = node

        if value is ...:
            if named:
                self._placeholder_inputs.append(target)
            return

        elif isinstance(value, _SocketLike):
            self._link_from(value.socket, target)
        elif isinstance(value, NodeSocket):
            self._link_from(value, target)
        elif isinstance(value, _NodeLike):
            target_type = target.type if not named else self.i._get(target).type
            self._link_from(value.o._best_match(target_type), target)  # type: ignore
        else:
            # TODO: explicitly skipping the sockets for BooleanMath as they are default false,
            # but this needs to be a more generic solution for sockets which aren't available
            # https://github.com/BradyAJohnston/nodebpy/issues/90
            if "BooleanMath" in self._bl_idname and value is False:
                return
            socket = (
                _find_socket_from_name(self.node.inputs, target) if named else target
            )
            # A multi-input socket (JoinGeometry, JoinBundle, …) fed an iterable
            # links each source; reversed so the tuple order reproduces creation
            # order, as JoinGeometry's own constructor does. A vector/colour
            # default tuple is not multi-input, so it falls through unchanged.
            if isinstance(value, (list, tuple)) and getattr(
                socket, "is_multi_input", False
            ):
                for source in reversed(list(value)):
                    self._apply_input(socket, cast("InputAny", source))
                return
            self._set_input_default_value(socket, value)

    def _establish_named_links(self, pairs: "list[tuple[str, InputAny]]"):
        """Link inputs that share a socket name (so the name alone is
        ambiguous), resolving each to a distinct socket by name plus a type
        match, falling back to interface order. Used for group nodes whose
        interface declares several inputs with the same name."""
        used: set[str] = set()
        for name, value in pairs:
            candidates = [
                s
                for s in self.node.inputs
                if s.name == name
                and s.identifier not in used
                and not s.identifier.startswith("__extend__")
            ]
            if not candidates:
                raise ValueError(
                    f"no remaining input socket named {name!r} on {self._bl_idname}"
                )
            value_type = _value_socket_type(value)
            socket = next(
                (s for s in candidates if s.type == value_type), candidates[0]
            )
            used.add(socket.identifier)
            self._apply_input(socket, value)

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
        self, sockets: Iterable[NodeSocket], types: tuple[str, ...] | None = None
    ) -> tuple[NodeSocket, str]:
        if types is None:
            types = self._socket_data_types
        possible = []
        for socket in sockets:
            compatible = SOCKET_COMPATIBILITY.get(socket.type, ())
            for type in types:
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

    def _declared_item_type(self, value: Any) -> str | None:
        """Subclasses may interpret ``value`` as an explicit socket-type
        declaration (an unlinked item); ``None`` means treat it as a link
        source."""
        return None

    def _add_unlinked_input(self, name: str, value: Any) -> bool:
        """Create the socket for a non-linkable value (a socket-type
        declaration; subclasses extend this for plain default values).
        Returns True when the value was handled."""
        declared = self._declared_item_type(value)
        if declared is not None:
            self._add_socket(name=name, type=declared)
            return True
        return False

    def _add_inputs(self, *args, **kwargs) -> dict[str, NodeSocket]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        items = {}
        for arg in args:
            items[arg._default_output_socket.name] = arg
        items.update(kwargs)
        for key, source in items.items():
            if self._add_unlinked_input(key, source):
                continue
            socket_source, type = self._match_compatible_data(
                source.o._available if hasattr(source, "o") else [source]
            )
            if type in self._type_map:
                type = self._type_map[type]
            socket = self._add_socket(name=key, type=type)
            # Key by identifier, not name: an item may share a name with a
            # built-in socket (e.g. a CaptureAttribute item named "Selection"),
            # and _establish_links resolves identifiers unambiguously.
            new_sockets[socket.identifier] = socket_source

        return new_sockets


class NodeGroupBuilder(BaseNode, ABC, Generic[_T]):
    """Base class for custom node groups.

    Subclasses implement :meth:`_build_group` with the node-graph logic.
    Subclass one of the editor-specific variants: :class:`GeometryNodeGroup`,
    :class:`ShaderNodeGroup`, or :class:`CompositorNodeGroup`.
    """

    _name: str
    # The inner node-tree bl_idname, set by each editor-specific subclass.
    _tree_idname: Literal["GeometryNodeTree", "ShaderNodeTree", "CompositorNodeTree"]
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

    def __init__(self, **kwargs):
        super().__init__()
        self._setup_node_group()
        self.node.show_options = False
        # Inputs whose interface name is shared by several sockets can't be
        # keyed in the kwargs dict; they arrive as ``(name, value)`` pairs.
        named_links = kwargs.pop("_named_links", None)
        self._establish_links(**kwargs)
        if named_links:
            self._establish_named_links(named_links)

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

    @classmethod
    def create_group(cls) -> _T:
        """Build this group's node tree and return it, reusing an existing tree
        of the same name.

        Unlike instantiating the class, this needs no active ``TreeBuilder``
        context — it opens its own — so a group can be pre-built and reused
        directly (e.g. assigned to a node's ``node_tree``) instead of being
        created by constructing the class inside a tree.
        """
        existing = bpy.data.node_groups.get(cls._name)
        if existing is not None:
            if existing.bl_idname != cls._tree_idname:
                raise TypeError(
                    f"Node group '{cls._name}' already exists as "
                    f"{existing.bl_idname}, not {cls._tree_idname}. "
                    f"Use a unique _name for this group."
                )
            return cast(_T, existing)
        # Only the inner tree is needed (no group *node*), so skip __init__,
        # which would require an active context to create a node.
        builder = cls.__new__(cls)
        with TreeBuilder(cls._name, tree_type=cls._tree_idname) as tree:
            builder._build_group(tree)
        tree.tree.color_tag = cls._color_tag
        return cast(_T, tree.tree)


class CustomGeometryGroup(NodeGroupBuilder[GeometryNodeTree]):
    """Node group in a Geometry Nodes tree."""

    _bl_idname = "GeometryNodeGroup"
    _tree_idname = "GeometryNodeTree"
    node: GeometryNodeGroup

    @property
    def node_tree(self) -> GeometryNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self.create_group()
        self.node.warning_propagation = self._warning_propagation


class CustomShaderGroup(NodeGroupBuilder[ShaderNodeTree]):
    """Node group in a Shader (Material) node tree."""

    _bl_idname = "ShaderNodeGroup"
    _tree_idname = "ShaderNodeTree"
    node: ShaderNodeGroup

    @property
    def node_tree(self) -> ShaderNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self.create_group()


class CustomCompositorGroup(NodeGroupBuilder[CompositorNodeTree]):
    """Node group in a Compositor node tree."""

    _bl_idname = "CompositorNodeGroup"
    _tree_idname = "CompositorNodeTree"
    node: CompositorNodeGroup

    @property
    def node_tree(self) -> CompositorNodeTree:
        assert self.node.node_tree is not None
        return self.node.node_tree

    def _setup_node_group(self) -> None:
        self.node.node_tree = self.create_group()
