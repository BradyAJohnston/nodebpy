from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, ClassVar, Iterable, Literal

if TYPE_CHECKING:
    from .nodes.geometry import IntegerMath, Math, VectorMath
    from .nodes.geometry.converter import BooleanMath, MultiplyMatrices, TransformPoint
    from .nodes.geometry.manual import Compare

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

from .arrange import arrange_tree
from .types import (
    LINKABLE,
    SOCKET_COMPATIBILITY,
    SOCKET_TYPES,
    TYPE_INPUT_ALL,
    FloatInterfaceSubtypes,
    IntegerInterfaceSubtypes,
    StringInterfaceSubtypes,
    VectorInterfaceSubtypes,
    _AttributeDomains,
    _SocketShapeStructureType,
)

GEO_NODE_NAMES = (
    f"GeometryNode{name}"
    for name in (
        "SetPosition",
        "TransformGeometry",
        "GroupInput",
        "GroupOutput",
        "MeshToPoints",
        "PointsToVertices",
    )
)


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'."""
    return name.lower().replace(" ", "_")


def denormalize_name(attr_name: str) -> str:
    """Convert 'geometry' or 'my_socket' to 'Geometry' or 'My Socket'."""
    return attr_name.replace("_", " ").title()


class SocketError(Exception):
    """Raised when a socket operation fails."""


class PanelContext:
    """Context manager for grouping sockets into a panel."""

    def __init__(
        self,
        socket_context: SocketContext,
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
    _active_context: SocketContext | None = None

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

    def panel(self, name: str, *, default_closed: bool = False) -> PanelContext:
        """Create a panel context for grouping sockets."""
        return PanelContext(self, name, default_closed=default_closed)

    def _create_socket(
        self, socket_def: SocketBase, name: str
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
        SocketContext._direction = self._direction
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
    just_added: "Node | None" = None
    collapse: bool = False

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
    ):
        if isinstance(tree, str):
            self.tree = bpy.data.node_groups.new(tree, tree_type)
        else:
            self.tree = tree

        self._menu_defaults: dict[str, str] = {}
        # Create socket accessors for named access
        self.inputs = InputInterfaceContext(self)
        self.outputs = OutputInterfaceContext(self)
        self._arrange = arrange
        self.collapse = collapse
        self.fake_user = fake_user

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
                from .lib.nodearrange import arrange as nodearrange

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
            from .screenshot import generate_mermaid_diagram

            return generate_mermaid_diagram(self)
        except Exception as e:
            # Diagram generation failed - return None to let Jupyter use text representation
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
        if isinstance(socket1, SocketLinker):
            socket1 = socket1.socket
        if isinstance(socket2, SocketLinker):
            socket2 = socket2.socket

        if (
            socket1.type not in SOCKET_COMPATIBILITY.get(socket2.type, ())
            and socket2.type != "CUSTOM"
        ):
            raise SocketError(
                f"Incompatible socket types, {socket1.type} and {socket2.type}"
            )

        link = self.tree.links.new(socket1, socket2, handle_dynamic_sockets=True)

        if any(socket.is_inactive for socket in [socket1, socket2]):
            assert socket1.node
            assert socket2.node
            # the warning message should report which sockets from which nodes were linked and which were innactive
            for socket in [socket1, socket2]:
                # we want to be loud about it if we end up linking an inactive socket to a node that is not a switch
                if socket.is_inactive and (
                    socket.node.bl_idname  # type: ignore
                    not in (  # type: ignore
                        "GeometryNodeIndexSwitch",
                        "GeometryNodeMenuSwitch",
                        "ShaderNodeMixShader",
                        "GeometryNodeSwitch",
                    )
                ):
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


class NodeBuilder:
    """Base class for all geometry node wrappers."""

    node: bpy.types.Node
    _bl_idname: str
    _tree: "TreeBuilder"
    _link_target: str | None = None
    _from_socket: NodeSocket | None = None
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _placeholder_inputs: list[str]
    __array_ufunc__ = None

    def __init__(self):
        # Get active tree from context manager
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
        self._link_target = None
        self._placeholder_inputs = []
        if self.__class__.name is not None:
            self.node = self._tree.add(self.__class__._bl_idname)
        else:
            raise ValueError(
                f"Class {self.__class__.__name__} must define a 'name' attribute"
            )

    @property
    def tree(self) -> "TreeBuilder":
        return self._tree

    @tree.setter
    def tree(self, value: "TreeBuilder"):
        self._tree = value

    @property
    def type(self) -> SOCKET_TYPES:
        return self._default_output_socket.type  # type: ignore

    @property
    def name(self) -> str:
        return str(self.node.name)

    @property
    def _default_input_socket(self) -> NodeSocket:
        if self._default_input_id is not None:
            return self.node.inputs[self._input_idx(self._default_input_id)]
        return self.node.inputs[0]

    @property
    def _default_output_socket(self) -> NodeSocket:
        if self._default_output_id is not None:
            return self.node.outputs[self._output_idx(self._default_output_id)]

        counter = 0
        socket = self.node.outputs[counter]
        while not socket.is_icon_visible:
            counter += 1
            socket = self.node.outputs[counter]
        return socket

    def _source_socket(self, node: LINKABLE | SocketLinker | NodeSocket) -> NodeSocket:
        assert node
        if isinstance(node, NodeSocket):
            return node
        elif isinstance(node, Node):
            return node.outputs[0]
        elif hasattr(node, "_default_output_socket"):
            return node._default_output_socket
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    def _target_socket(self, node: LINKABLE | SocketLinker | NodeSocket) -> NodeSocket:
        assert node
        if isinstance(node, NodeSocket):
            return node
        elif isinstance(node, Node):
            return node.inputs[0]
        elif hasattr(node, "_default_input_socket"):
            return node._default_input_socket
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    @property
    def _available_outputs(self) -> list[NodeSocket]:
        return [socket for socket in self.node.outputs if socket.is_icon_visible]

    @property
    def _available_inputs(self) -> list[NodeSocket]:
        return [
            socket
            for socket in self.node.inputs
            # only sockets that are available, don't have a link already (unless multi-input)
            if not socket.is_inactive
            and socket.is_icon_visible
            and (not socket.links or socket.is_multi_input)
        ]

    def _best_output_socket(self, type: str) -> NodeSocket:
        compatible = SOCKET_COMPATIBILITY.get(type, ())
        possible = [
            socket for socket in self._available_outputs if socket.type in compatible
        ]
        if possible:
            possible.sort(key=lambda x: compatible.index(x.type))
            return possible[0]

        raise SocketError("No compatible output sockets found")

    def _find_best_socket_pair(
        self,
        source: "NodeBuilder | SocketLinker | NodeSocket",
        target: "NodeBuilder | SocketLinker | NodeSocket",
    ) -> tuple[NodeSocket, NodeSocket]:
        """Find the best possible compatible pair of sockets between two nodes, looking only at the
        the currently available outputs from the source and the inputs from the target"""
        possible_combos = []
        if isinstance(source, (NodeBuilder, SocketLinker)):
            outputs = source._available_outputs
        elif isinstance(source, NodeSocket):
            outputs = [source]

        if isinstance(target, (NodeBuilder, SocketLinker)):
            inputs = target._available_inputs
        else:
            inputs = [target]
        for output in outputs:
            compat_sockets = SOCKET_COMPATIBILITY.get(output.type, ())
            for input in inputs:
                if input.type == output.type:
                    return input, output

                if input.type in compat_sockets:
                    possible_combos.append(
                        (compat_sockets.index(input.type), (input, output))
                    )

        if possible_combos:
            # sort by distance between compatible sockets and return the best match
            return sorted(possible_combos, key=lambda x: x[0])[0][1]

        raise SocketError(
            f"Cannot link any output from {source.node.name} to any input of {target.node.name}. "  # type: ignore
            f"Available output types: {[f'{o.name}:{o.type}' for o in outputs]}, "
            f"Available input types: {[f'{i.name}:{i.type}' for i in inputs]}"
        )

    def _input_idx(self, identifier: str) -> int:
        # currently there is a Blender bug that is preventing the lookup of sockets from identifiers on some
        # nodes but not others
        # This currently fails:
        #
        # node = bpy.data.node_groups["Geometry Nodes"].nodes['Mix']
        # node.inputs[node.inputs[0].identifier]
        #
        # This should succeed because it should be able to lookup the socket by identifier
        # so instead we have to convert the identifier to an index and then lookup the socket
        # from the index instead
        input_ids = [input.identifier for input in self.node.inputs]
        if identifier in input_ids:
            idx = input_ids.index(identifier)
            return idx
        input_names = [input.name for input in self.node.inputs]
        if identifier in input_names:
            return input_names.index(identifier)

        raise RuntimeError(
            f"Input '{identifier}' not found on {self.node.bl_idname}. "
            f"Available inputs: {input_names}"
        )

    def _output_idx(self, identifier: str) -> int:
        output_ids = [output.identifier for output in self.node.outputs]
        return output_ids.index(identifier)

    def _input(self, identifier: str) -> SocketLinker:
        """Input socket: Vector"""
        input = self.node.inputs[self._input_idx(identifier)]
        return SocketLinker(input)

    def _output(self, identifier: str) -> SocketLinker:
        """Output socket: Vector"""
        return SocketLinker(self.node.outputs[self._output_idx(identifier)])

    def _link(
        self, source: LINKABLE | SocketLinker | NodeSocket, target: LINKABLE
    ) -> bpy.types.NodeLink:
        source_socket = self._source_socket(source)
        target_socket = self._target_socket(target)
        return self.tree.link(source_socket, target_socket)

    def _link_from(
        self,
        source: LINKABLE,
        input: LINKABLE | str,
    ):
        if isinstance(input, str):
            try:
                self._link(source, self.node.inputs[input])
            except KeyError:
                self._link(source, self.node.inputs[self._input_idx(input)])
        else:
            self._link(source, input)

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

    def _establish_links(self, **kwargs: TYPE_INPUT_ALL):
        input_ids = [input.identifier for input in self.node.inputs]
        for name, value in kwargs.items():
            if value is None or (
                # TODO: this is an ugly single-node exception for this particular case. I'd
                # like to fine a cleaner way to handle this automatically instead.
                "GridPrune" in self._bl_idname
                and name == "Threshold"
                and self.node.data_type == "BOOLEAN"
            ):
                continue
            if isinstance(value, Node):
                node = NodeBuilder()
                node.node = value
                value = node

            if value is ...:
                # Ellipsis marks this input as a placeholder for the >> operator
                self._placeholder_inputs.append(name)
                if self._from_socket is not None:
                    self._link_from(self._from_socket, name)
                continue

            elif isinstance(value, SocketLinker):
                self._link_from(value, name)
            elif isinstance(value, NodeSocket):
                self._link_from(value, name)
            elif isinstance(value, NodeBuilder):
                self._link_from(value._best_output_socket(self._input(name).type), name)
            else:
                if name in input_ids:
                    input = self.node.inputs[input_ids.index(name)]
                    self._set_input_default_value(input, value)
                else:
                    if name in self.node.inputs:
                        input = self.node.inputs[name]
                    else:
                        input = self.node.inputs[name.replace("_", "").capitalize()]
                    self._set_input_default_value(input, value)

    def __rshift__(self, other: "NodeBuilder | SocketLinker") -> "NodeBuilder":
        """Chain nodes using >> operator. Links output to input.

        Usage:
            node1 >> node2 >> node3
            tree.inputs.value >> Math.add(..., 0.1) >> tree.outputs.result

        If the target node has an ellipsis placeholder (...), links to that specific input.
        Otherwise, finds the best compatible socket pair based on type compatibility.

        Returns the right-hand node to enable continued chaining.
        """
        if isinstance(other, SocketLinker):
            source = self._default_output_socket
            target = other.socket
            other._from_socket = source
        elif getattr(other, "_placeholder_inputs", None):
            # Link to the first placeholder input marked with ...
            name = other._placeholder_inputs.pop(0)
            try:
                target = other.node.inputs[name]
            except KeyError:
                target = other.node.inputs[other._input_idx(name)]
            source = self._best_output_socket(target.type)
        else:
            try:
                source, target = self._find_best_socket_pair(self, other)
            except SocketError:
                source, target = other._find_best_socket_pair(self, other)

        self.tree.link(source, target)
        return other

    def _get_input_socket_by_name(self, node: "NodeBuilder", name: str) -> NodeSocket:
        """Get input socket by name, trying direct access first, then title case."""
        try:
            return node.node.inputs[name]
        except KeyError:
            title_name = name.replace("_", " ").title()
            return node.node.inputs[title_name]

    def _apply_math_operation(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "VectorMath | Math":
        """Apply a math operation with appropriate Math/VectorMath node."""
        from .nodes.geometry import VectorMath

        values = (
            (self._default_output_socket, other)
            if not reverse
            else (other, self._default_output_socket)
        )

        component_is_vector = False
        for value in values:
            if getattr(value, "type", None) == "VECTOR":
                component_is_vector = True
                break

        # Use VectorMath if either operand is a vector
        if component_is_vector:
            if operation == "multiply":
                # Handle special cases for vector multiplication where we might scale instead
                # of using the multiply method
                if isinstance(other, (int, float)):
                    return VectorMath.scale(self._default_output_socket, other)
                elif isinstance(other, (list, tuple)) and len(other) == 3:
                    return VectorMath.multiply(*values)
                elif isinstance(other, NodeBuilder):
                    return VectorMath.multiply(*values)
                else:
                    raise TypeError(
                        f"Unsupported type for {operation} with VECTOR socket: {type(other)}, {other=}"
                    )
            else:
                vector_method = getattr(VectorMath, operation)
                if isinstance(other, (int, float)):
                    scalar_vector = (other, other, other)
                    return (
                        vector_method(self._default_output_socket, scalar_vector)
                        if not reverse
                        else vector_method(scalar_vector, self._default_output_socket)
                    )
                elif (
                    isinstance(other, (list, tuple)) and len(other) == 3
                ) or isinstance(other, NodeBuilder):
                    return vector_method(*values)

                else:
                    raise TypeError(
                        f"Unsupported type for {operation} with VECTOR operand: {type(other)}"
                    )
        else:  # Both operands are scalar types, use regular Math
            from .nodes.geometry.converter import IntegerMath, Math

            # only the Geometry Node Tree supports integer math currently, potential
            # to support other trees when Blender supports it
            is_geometry_tree = self._tree.tree.bl_idname == "GeometryNodeTree"
            if (
                is_geometry_tree
                and isinstance(other, int)
                and self._default_output_socket.type == "INT"
            ):
                return getattr(IntegerMath, operation)(*values)
            else:
                # Math node uses 'floored_modulo' instead of 'modulo'
                math_operation = (
                    "floored_modulo" if operation == "modulo" else operation
                )
                return getattr(Math, math_operation)(*values)

    def __mul__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "multiply")

    def __rmul__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "multiply", reverse=True)

    def __truediv__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "divide")

    def __rtruediv__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "divide", reverse=True)

    def __add__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "add")

    def __radd__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "add", reverse=True)

    def __sub__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "subtract")

    def __rsub__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "subtract", reverse=True)

    def __pow__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "power")

    def __rpow__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "power", reverse=True)

    def __mod__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "modulo")

    def __rmod__(self, other: Any) -> "VectorMath | Math":
        return self._apply_math_operation(other, "modulo", reverse=True)

    def __floordiv__(self, other: Any) -> "VectorMath | Math | IntegerMath":
        return self._apply_floordiv_operation(other)

    def __rfloordiv__(self, other: Any) -> "VectorMath | Math | IntegerMath":
        return self._apply_floordiv_operation(other, reverse=True)

    def __neg__(self) -> "VectorMath | Math | IntegerMath":
        from .nodes.geometry import VectorMath
        from .nodes.geometry.converter import IntegerMath, Math

        socket = self._default_output_socket
        if socket.type == "VECTOR":
            return VectorMath.scale(socket, -1)
        elif socket.type == "INT":
            return IntegerMath.negate(socket)
        else:
            return Math.multiply(socket, -1)

    def __abs__(self) -> "VectorMath | Math | IntegerMath":
        from .nodes.geometry import VectorMath
        from .nodes.geometry.converter import IntegerMath, Math

        socket = self._default_output_socket
        if socket.type == "VECTOR":
            return VectorMath.absolute(socket)
        elif socket.type == "INT":
            return IntegerMath.absolute(socket)
        else:
            return Math.absolute(socket)

    def _apply_floordiv_operation(
        self, other: Any, reverse: bool = False
    ) -> "VectorMath | Math | IntegerMath":
        """Apply floor division: divide then floor."""
        from .nodes.geometry import VectorMath
        from .nodes.geometry.converter import IntegerMath, Math

        socket = self._default_output_socket
        component_is_vector = (
            socket.type == "VECTOR" or getattr(other, "type", None) == "VECTOR"
        )

        if not component_is_vector and isinstance(other, int) and socket.type == "INT":
            values = (socket, other) if not reverse else (other, socket)
            return IntegerMath.divide_floor(*values)

        divided = self._apply_math_operation(other, "divide", reverse=reverse)
        if component_is_vector:
            return VectorMath.floor(divided)
        else:
            return Math.floor(divided)

    def _apply_compare_operation(self, other: Any, operation: str) -> "Compare | Math":
        """Apply a comparison operation.

        Uses the Compare node in geometry trees (supports float, int, vector and
        outputs a boolean). Falls back to Math.less_than / Math.greater_than in
        compositor and shader trees which lack a Compare node. For <= and >= in
        non-geometry trees, we swap the operands (a <= b == b >= a == !(a > b)
        is equivalent to less_than(b, a) when treating the output as boolean).
        """
        if isinstance(self._tree.tree, GeometryNodeTree):
            from .nodes.geometry.manual import Compare

            socket = self._default_output_socket
            values = (socket, other)

            if socket.type == "VECTOR":
                return getattr(Compare, operation).vector(*values)
            elif socket.type == "INT":
                return getattr(Compare, operation).integer(*values)
            else:
                return getattr(Compare, operation).float(*values)
        else:
            # Compositor / Shader trees only have Math.less_than and
            # Math.greater_than (float output, no boolean). Map <= and >= by
            # swapping operands: a <= b ≡ less_than(b, a) is wrong —
            # but greater_than(b, a) gives 1 when b>a i.e. a<b.
            # So: a <= b → 1 - greater_than(a, b)  — needs two nodes.
            # Simpler: a >= b ≡ !(a < b) ≡ 1 - less_than(a, b)
            from .nodes.geometry.converter import Math

            socket = self._default_output_socket
            _MATH_COMPARE_MAP = {
                "less_than": ("less_than", False),
                "greater_than": ("greater_than", False),
                "less_equal": ("greater_than", True),  # a<=b → !(a>b) → 1-gt(a,b)
                "greater_equal": ("less_than", True),  # a>=b → !(a<b) → 1-lt(a,b)
            }
            math_op, negate = _MATH_COMPARE_MAP[operation]
            result = getattr(Math, math_op)(socket, other)
            if negate:
                result = Math.subtract(1.0, result._default_output_socket)
            return result

    def __lt__(self, other: Any) -> "Compare | Math":
        return self._apply_compare_operation(other, "less_than")

    def __gt__(self, other: Any) -> "Compare | Math":
        return self._apply_compare_operation(other, "greater_than")

    def __le__(self, other: Any) -> "Compare | Math":
        return self._apply_compare_operation(other, "less_equal")

    def __ge__(self, other: Any) -> "Compare | Math":
        return self._apply_compare_operation(other, "greater_equal")

    def __eq__(self, other: Any) -> "Compare | Math":  # type: ignore
        return self._apply_compare_operation(other, "equal")

    def __ne__(self, other: Any) -> "Compare | Math":  # type: ignore
        return self._apply_compare_operation(other, "not_equal")

    def _apply_boolean_operation(self, other: Any, operation: str) -> "BooleanMath":
        """Apply a boolean operation using the BooleanMath node."""
        from .nodes.geometry.converter import BooleanMath

        return getattr(BooleanMath, operation)(self, other)

    def __and__(self, other: Any) -> "BooleanMath":
        return self._apply_boolean_operation(other, "l_and")

    def __rand__(self, other: Any) -> "BooleanMath":
        from .nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(other, self)

    def __or__(self, other: Any) -> "BooleanMath":
        return self._apply_boolean_operation(other, "l_or")

    def __ror__(self, other: Any) -> "BooleanMath":
        from .nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(other, self)

    def __xor__(self, other: Any) -> "BooleanMath":
        return self._apply_boolean_operation(other, "not_equal")

    def __rxor__(self, other: Any) -> "BooleanMath":
        from .nodes.geometry.converter import BooleanMath

        return BooleanMath.not_equal(other, self)

    def __invert__(self) -> "BooleanMath":
        from .nodes.geometry.converter import BooleanMath

        return BooleanMath.l_not(self)

    @staticmethod
    def _cast_to_matrix(value):
        from .nodes.geometry.converter import CombineMatrix

        if hasattr(value, "shape") and value.shape == (4, 4):
            return CombineMatrix(*value.ravel())
        else:
            return value

    def __matmul__(self, other: Any) -> "MultiplyMatrices | TransformPoint":
        from .nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket
        other_type = getattr(other, "type", None)

        # matrix @ vector → TransformPoint (standard M @ v)
        if socket.type == "MATRIX" and other_type == "VECTOR":
            return TransformPoint(other, socket)

        return MultiplyMatrices(self, other)

    def __rmatmul__(self, other: Any) -> "MultiplyMatrices | TransformPoint":
        from .nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket
        other_type = getattr(other, "type", None)

        # matrix @ vector: other is matrix (non-NodeBuilder cast), self is vector
        if socket.type == "VECTOR" and other_type == "MATRIX":
            return TransformPoint(socket, other)

        return MultiplyMatrices(other, self)


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
        self, source: NodeBuilder | NodeSocket, target: NodeBuilder | NodeSocket
    ) -> tuple[NodeSocket, NodeSocket]:
        try:
            return super()._find_best_socket_pair(source, target)  # type: ignore
        except SocketError:
            if target == self:
                target_name, source_socket = list(target._add_inputs(source).items())[0]
                return (source_socket, target.inputs[target_name].socket)
            else:
                target_name, source_socket = list(
                    source._add_inputs(*target.node.inputs).items()
                )[0]
                return (
                    source.outputs[target_name].socket,
                    target.inputs[target_name].socket,
                )

            # for target_name, source_socket in new_sockets.items():
            #     target_socket = target.inputs[target_name].socket
            #     return (source_socket, target_socket)

    # def _best_output_socket(self, type: str) -> NodeSocket:
    #     # compatible = SOCKET_COMPATIBILITY.get(type, ())
    #     # possible = [
    #     #     socket for socket in self._available_outputs if socket.type in compatible
    #     # ]
    #     # if possible:
    #     #     return sorted(possible, key=lambda x: compatible.index(x.type))[0]

    #     raise SocketError("No compatible output sockets found")

    def _add_inputs(self, *args, **kwargs) -> dict[str, LINKABLE]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        items = {}
        for arg in args:
            if isinstance(arg, bpy.types.NodeSocket):
                name = arg.name
                items[name] = arg
            else:
                items[arg._default_output_socket.name] = arg
        items.update(kwargs)
        for key, source in items.items():
            socket_source, type = self._match_compatible_data(source._available_outputs)
            if type in self._type_map:
                type = self._type_map[type]
            socket = self._add_socket(name=key, type=type)
            new_sockets[socket.name] = socket_source

        return new_sockets


class SocketLinker(NodeBuilder):
    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self.socket = socket
        self.node = socket.node
        self._default_output_id = socket.identifier
        self._tree = TreeBuilder(socket.node.id_data)  # type: ignore

    @property
    def links(self) -> bpy.types.NodeLinks:
        links = self.socket.links
        assert links
        return links

    @property
    def _available_outputs(self) -> list[NodeSocket]:
        return [self.socket]

    @property
    def _available_inputs(self) -> list[NodeSocket]:
        return [self.socket]

    @property
    def type(self) -> SOCKET_TYPES:
        return self.socket.type  # type: ignore

    @property
    def socket_name(self) -> str:
        return self.socket.name

    @property
    def name(self) -> str:
        return str(self.socket.name)


class SocketBase(SocketLinker):
    """Base class for all socket definitions."""

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
                # we delay the setting of the default value until the menu is created
                # because it doesn't have potential enum values yet until the menu socket is
                # connected and the node tree is complete
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


class SocketFloat(SocketBase):
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


class SocketInt(SocketBase):
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


class SocketBoolean(SocketBase):
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


class SocketVector(SocketBase):
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
            default_attribute=default_attribute,
            attribute_domain=attribute_domain,
        )


class SocketColor(SocketBase):
    """Color socket - RGB color value."""

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


class SocketRotation(SocketBase):
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


class SocketMatrix(SocketBase):
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


class SocketString(SocketBase):
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


class SocketMenu(SocketBase):
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


class SocketObject(SocketBase):
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


class SocketGeometry(SocketBase):
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


class SocketCollection(SocketBase):
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


class SocketImage(SocketBase):
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


class SocketMaterial(SocketBase):
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


class SocketBundle(SocketBase):
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


class SocketClosure(SocketBase):
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


class SocketShader(SocketBase):
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


class NodeGroupBase(NodeBuilder):
    """
    Base NodeGroup for interacting with custom node groups
    """

    _node_group_name: str
    _bl_idname = "GeometryNodeGroup"
    node: bpy.types.GeometryNodeGroup

    def __init__(self):
        super().__init__()

    def _generate_node_group(self, name: str) -> bpy.types.GeometryNodeGroup: ...
