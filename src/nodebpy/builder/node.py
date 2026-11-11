from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import cache
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Literal,
    Protocol,
    Self,
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

from ..types import SOCKET_COMPATIBILITY, Default, InputAny
from ._combine import holds_sockets, link_combined
from ._muted import Muted, muting
from ._utils import (
    SocketError,
    WarningPropagation,
    _deprecated,
    _needs_newer_blender,
    _NodeLike,
    _older_blender,
    _SocketLike,
    apply_node_props,
    enum_value_error,
    normalize_name,
)
from .accessor import SocketAccessor
from .mixins import LinkingMixin, OperatorMixin
from .tree import TreeBuilder

if TYPE_CHECKING:
    from types import EllipsisType

    from .socket import Socket

    class _DynamicTarget(Protocol):
        """Structural type for a node that supports dynamic socket addition."""

        def _add_inputs(self, *args: Any, **kwargs: Any) -> dict[str, NodeSocket]: ...

        @property
        def i(self) -> SocketAccessor: ...


_NO_DEFAULT = object()


@cache
def _constructor_defaults(cls: type) -> dict[str, Any]:
    """Parameter → default of ``cls``'s constructor."""
    return {
        name: param.default
        for name, param in inspect.signature(cls.__init__).parameters.items()
        if param.default is not param.empty
    }


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
    if isinstance(value, Muted):
        value = value.source
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
    _tree: TreeBuilder[Any]
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _placeholder_inputs: list[str]
    # Constructor parameters named after their socket's display name rather
    # than its identifier (normalized identifier -> parameter), for export.
    _socket_params: ClassVar[dict[str, str]] = {}
    # Menu inputs that replaced an enum property: socket identifier ->
    # (removal version, old enum identifier -> menu item). An old value still
    # works, with a DeprecationWarning (see ``legacy_menu_customization``).
    _legacy_menu_values: ClassVar[dict[str, tuple[int, dict[str, str]]]] = {}

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
        self._wrapped_node = node if node else self._tree.add(self.__class__._bl_idname)

    # Read-only, so subclasses can narrow its type (``node: GeometryNodeGroup``).
    @property
    def node(self) -> Node:
        """The Blender node this instance wraps."""
        return self._wrapped_node

    @property
    def tree(self) -> TreeBuilder[Any]:
        """The `TreeBuilder` instance this node belongs to and is being built within."""
        return self._tree

    @property
    def name(self) -> str:
        """The name of the node being wrapped by this instance."""
        return str(self.node.name)

    def props(
        self,
        *,
        label: str | None = None,
        color: str | tuple[float, float, float] | None = None,
        width: float | None = None,
        height: float | None = None,
        hide: bool | None = None,
        show_options: bool | None = None,
        hide_inputs: Iterable[str] = (),
        hide_outputs: Iterable[str] = (),
        mute: bool | None = None,
        warning_propagation: WarningPropagation | None = None,
        pin_gizmo: bool | None = None,
        pin_gizmo_inputs: Iterable[str] = (),
    ) -> Self:
        """Set the properties every node has and return the node, so it can
        go at the end of a chain::

            g.SetPosition(geometry=geo, offset=offset).props(
                label="Lift", color="#FFAA00", width=200
            )

        Properties left as ``None`` are unchanged.

        Args:
            label: The node's header label.
            color: A custom header colour, as a hex string (``"#FFAA00"``) or an
                ``(r, g, b)`` tuple; turns on ``use_custom_color``.
            width: The node's width.
            height: The node's height; only frames use it.
            hide: Collapse the node.
            show_options: Show the node's options (dropdowns and toggles).
            hide_inputs: Input sockets to hide, by name; ``"Value#1"`` names
                the second visible ``Value``.
            hide_outputs: Output sockets to hide, by name.
            mute: Mute (bypass) the node.
            warning_propagation: Which of the node's warnings show on the
                group node it sits in.
            pin_gizmo: Keep the node's gizmo visible when it isn't selected:
                a gizmo node's, or a value node's (Value, Vector, ...).
            pin_gizmo_inputs: Inputs whose gizmos stay visible when the node
                isn't selected, by name; for group nodes passing a gizmo
                through.
        """
        apply_node_props(
            self.node,
            label=label,
            color=color,
            width=width,
            height=height,
            hide=hide,
            show_options=show_options,
            hide_inputs=hide_inputs,
            hide_outputs=hide_outputs,
            mute=mute,
            warning_propagation=warning_propagation,
            pin_gizmo=pin_gizmo,
            pin_gizmo_inputs=pin_gizmo_inputs,
        )
        return self

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
        builder._wrapped_node = node
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

    def _set_enum(self, prop: str, value: Any) -> None:
        """Set an enum property, suggesting the closest options for a typo."""
        try:
            setattr(self.node, prop, value)
        except TypeError as error:
            raise enum_value_error(error, f"{type(self).__name__}'s {prop}") from None

    def _set_input_default_value(self, input: NodeSocket, value: Any) -> None:
        """Set the default value for an input socket, handling type conversions."""
        assert hasattr(input, "default_value")
        stype = getattr(input, "type", None)
        if holds_sockets(value):
            # (1, 1, height): the sockets are combined into a node and linked
            link_combined(self.tree, input, value)
        elif stype == "VECTOR" and isinstance(value, (int, float)):
            input.default_value = [value] * len(input.default_value)  # type: ignore
        elif stype == "INT" and isinstance(value, float):
            input.default_value = int(value)  # type: ignore
        elif stype == "MENU":
            removed_in, legacy = self._legacy_menu_values.get(input.identifier, (0, {}))
            if value in legacy:
                param = normalize_name(input.identifier)
                _deprecated(
                    f"{type(self).__name__}({param}={value!r})",
                    f"{param}={legacy[value]!r}",
                    removed_in=removed_in,
                )
                value = legacy[value]
            try:
                input.default_value = value  # type: ignore
            except TypeError:
                # A menu socket's enum items arrive by link propagation from
                # the Menu Switch that defines them, which may not have run
                # yet (e.g. a Switch whose output links up only after its
                # inputs get defaults). Retry at tree-context exit, when
                # every link exists.
                from .tree import _MenuDefault

                self.tree._menu_defaults.append(
                    _MenuDefault(cast("bpy.types.NodeSocketMenu", input), value)
                )
        else:
            input.default_value = value  # type: ignore

    def _establish_links(self, **kwargs: InputAny):
        for name, value in kwargs.items():
            self._apply_input(name, value)

    def _apply_input(self, target: str | NodeSocket, value: InputAny):
        """Link or default-set ``value`` onto an input.

        ``target`` is a socket name/identifier (resolved against
        ``self.node.inputs``) or an already-resolved input socket — the latter
        lets callers address one of several same-named sockets unambiguously.
        """
        named = isinstance(target, str)
        # A ``Default`` member stands for the socket's own fallback (an implicit
        # field or context value Blender reads when nothing is linked): nothing to
        # set or link, the same as ``None``.
        if isinstance(value, Default):
            return
        if isinstance(value, Muted):
            with muting(value.value):
                self._apply_input(target, value.source)
            return
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
            node._wrapped_node = value
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
            self._link_from(value.o._best_match(target_type), target)
        elif getattr(value, "_as_rshift_target", None) is not None:
            # an item handle stands for its output socket (and says so when
            # it has none)
            self._link_from(cast(Any, value)._default_output_socket, target)
        else:
            # TODO: explicitly skipping the sockets for BooleanMath as they are default false,
            # but this needs to be a more generic solution for sockets which aren't available
            # https://github.com/BradyAJohnston/nodebpy/issues/90
            if "BooleanMath" in self._bl_idname and value is False:
                return
            if named:
                try:
                    socket = _find_socket_from_name(self.node.inputs, target)
                except ValueError:
                    # An input added in a newer Blender than the running one:
                    # left at its default it's skipped, any other value needs it.
                    if not _older_blender():
                        raise
                    if target in self._legacy_menu_values:
                        self._set_legacy_menu_property(target, value)
                        return
                    if self._is_constructor_default(target, value):
                        return
                    raise _needs_newer_blender(
                        f"{type(self).__name__}'s {target!r} input"
                    ) from None
            else:
                socket = target
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

    def _set_legacy_menu_property(self, identifier: str, value: Any) -> None:
        """On a Blender from before an enum property became the menu input
        ``identifier``, set the property: ``value`` is a menu item, or the
        property's own value."""
        to_item = self._legacy_menu_values[identifier][1]
        to_enum = {item: enum for enum, item in to_item.items()}
        try:
            setattr(self.node, normalize_name(identifier), to_enum.get(value, value))
        except TypeError as error:
            raise enum_value_error(error, f"{type(self).__name__}'s {identifier}")

    def _is_constructor_default(self, identifier: str, value: Any) -> bool:
        """Whether ``value`` is what the constructor passes for the input
        ``identifier`` when its parameter is left out."""
        param = normalize_name(identifier)
        param = self._socket_params.get(param, param)
        default = _constructor_defaults(type(self)).get(param, _NO_DEFAULT)
        return default is not _NO_DEFAULT and value == default

    def _establish_named_links(self, pairs: list[tuple[str, InputAny]]):
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
            if value_type is None and isinstance(value, (tuple, list)):
                # A plain sequence is ambiguous between VECTOR, RGBA, ROTATION
                # and MATRIX (a blanket "VECTOR" would steer a 4-tuple colour
                # default onto a same-named vector socket): pick the first
                # candidate whose array default it actually fits, falling back
                # to interface order.
                def fits(s) -> bool:
                    try:
                        return len(s.default_value) == len(value)  # noqa: B023
                    except (AttributeError, TypeError):  # pragma: no cover
                        return False

                socket = next((s for s in candidates if fits(s)), candidates[0])
                used.add(socket.identifier)
                self._apply_input(socket, value)
                continue
            if value_type is None:
                # A plain default carries no socket, but its Python type still
                # narrows the target: 0.0 must mean a float "Profile Rotation",
                # never the same-named rotation socket, whose default it would
                # not even fit.
                from .items import _infer_value_type

                inferred = _infer_value_type(value)
                value_type = "VALUE" if inferred == "FLOAT" else inferred
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


def _match_compatible_data(
    sockets: Iterable[NodeSocket], types: tuple[str, ...]
) -> tuple[NodeSocket, str]:
    """The socket among ``sockets`` that best fits one of ``types``, with
    that type: the closest match in Blender's implicit-conversion order."""
    possible = []
    for socket in sockets:
        compatible = SOCKET_COMPATIBILITY.get(socket.type, ())
        for type in types:
            if type in compatible:
                possible.append((socket, type, compatible.index(type)))
    if not possible:
        raise SocketError("No compatible socket found")
    possible.sort(key=lambda x: x[2])
    socket, type, _ = possible[0]
    return socket, type


class DynamicInputsMixin(ABC):
    if TYPE_CHECKING:
        # a class attribute, or a property when it depends on the node
        @property
        def _socket_data_types(self) -> tuple[str, ...]: ...

    _type_map: ClassVar[dict[str, str]] = {}

    def _match_compatible_data(
        self, sockets: Iterable[NodeSocket], types: tuple[str, ...] | None = None
    ) -> tuple[NodeSocket, str]:
        return _match_compatible_data(
            sockets, self._socket_data_types if types is None else types
        )

    def _find_best_socket_pair(
        self,
        source: BaseNode | Socket | NodeSocket | EllipsisType | LinkingMixin,
        target: BaseNode | Socket | NodeSocket | EllipsisType | LinkingMixin,
    ) -> tuple[NodeSocket, NodeSocket]:
        try:
            return super()._find_best_socket_pair(source, target)  # type: ignore
        except SocketError:
            dyn = cast("_DynamicTarget", target)
            target_name, source_socket = next(iter(dyn._add_inputs(source).items()))
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


class NodeGroupBuilder[T: bpy.types.NodeTree](BaseNode, ABC):
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
    # Tree-level properties applied after the build (description, modifier/
    # tool flags, default group-node width, …) — only values differing from a
    # fresh tree's defaults belong here; codegen fills it when exporting.
    _tree_properties: ClassVar[dict[str, Any]] = {}

    def __init__(self, **kwargs: Any):
        super().__init__()
        self._setup_node_group()
        self.node.show_options = False
        # Inputs whose interface name is shared by several sockets can't be
        # keyed in the kwargs dict; they arrive as ``(name, value)`` pairs.
        named_links = kwargs.pop("_named_links", None)
        self._establish_links(**kwargs)
        if named_links:
            self._establish_named_links(named_links)
        # Name the node after its tree (Blender deduplicates with a
        # ``.001``-style suffix), matching how group assets added from the
        # Add menu are named, instead of Blender's default ``Group``.
        self.node.name = self.node_tree.name

    @property
    @abstractmethod
    def node_tree(self) -> T:
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
    def _build_group(self, tree: TreeBuilder[T]) -> None:
        """Build the node group internals and interface."""

    @classmethod
    def create_group(cls) -> T:
        """Build this group's node tree and return it, reusing an existing tree
        of the same name.

        Unlike instantiating the class, this needs no active ``TreeBuilder``
        context — it opens its own — so a group can be pre-built and reused
        directly (e.g. assigned to a node's ``node_tree``) instead of being
        created by constructing the class inside a tree.
        """
        # Only the inner tree is needed (no group *node*), so skip __init__,
        # which would require an active context to create a node.
        return cls.__new__(cls)._create_group()

    def _group_name(self) -> str:
        """Name of the inner tree. Override when instance state set before
        ``super().__init__()`` (e.g. a data type) selects a variant, so each
        variant builds and reuses its own tree."""
        return self._name

    def _create_group(self) -> T:
        name = self._group_name()
        existing = bpy.data.node_groups.get(name)
        if existing is not None:
            if existing.bl_idname != self._tree_idname:
                raise TypeError(
                    f"Node group '{name}' already exists as "
                    f"{existing.bl_idname}, not {self._tree_idname}. "
                    f"Use a unique _name for this group."
                )
            return cast(T, existing)
        with TreeBuilder(name, tree_type=self._tree_idname) as tree:
            self._build_group(tree)
        tree.tree.color_tag = self._color_tag
        for key, value in self._tree_properties.items():
            try:
                setattr(tree.tree, key, value)
            except (AttributeError, TypeError):
                # A property this Blender version doesn't have (or types
                # differently) — skip rather than fail the whole build.
                print(f"  {name}: skipping tree property {key!r}")
        return cast(T, tree.tree)


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
        self.node.node_tree = self._create_group()
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
        self.node.node_tree = self._create_group()


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
        self.node.node_tree = self._create_group()
