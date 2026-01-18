from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal

if TYPE_CHECKING:
    from .nodes.converter import Math, VectorMath

import arrangebpy
import bpy
from bpy.types import (
    GeometryNodeTree,
    Node,
    Nodes,
    NodeSocket,
)

from .nodes.types import (
    LINKABLE,
    SOCKET_COMPATIBILITY,
    SOCKET_TYPES,
    TYPE_INPUT_ALL,
    FloatInterfaceSubtypes,
    IntegerInterfaceSubtypes,
    StringInterfaceSubtypes,
    VectorInterfaceSubtypes,
    _AttributeDomains,
)

# from .arrange import arrange_tree

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


def source_socket(node: LINKABLE | SocketLinker | NodeSocket) -> NodeSocket:
    assert node
    if isinstance(node, NodeSocket):
        return node
    elif isinstance(node, Node):
        return node.outputs[0]
    elif hasattr(node, "_default_output_socket"):
        return node._default_output_socket
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


def target_socket(node: LINKABLE | SocketLinker | NodeSocket) -> NodeSocket:
    assert node
    if isinstance(node, NodeSocket):
        return node
    elif isinstance(node, Node):
        return node.inputs[0]
    elif hasattr(node, "_default_input_socket"):
        return node._default_input_socket
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


class SocketContext:
    _direction: Literal["INPUT", "OUTPUT"] | None
    _active_context: SocketContext | None = None

    def __init__(self, tree_builder: TreeBuilder):
        self.builder = tree_builder

    @property
    def tree(self) -> GeometryNodeTree:
        tree = self.builder.tree
        assert tree is not None and isinstance(tree, GeometryNodeTree)
        return tree

    @property
    def interface(self) -> bpy.types.NodeTreeInterface:
        interface = self.tree.interface
        assert interface is not None
        return interface

    def _create_socket(
        self, socket_def: SocketBase
    ) -> bpy.types.NodeTreeInterfaceSocket:
        """Create a socket from a socket definition."""
        socket = self.interface.new_socket(
            name=socket_def.name,
            in_out=self._direction,
            socket_type=socket_def._bl_socket_type,
        )
        socket.description = socket_def.description
        return socket

    def __enter__(self):
        SocketContext._direction = self._direction
        SocketContext._active_context = self
        return self

    def __exit__(self, *args):
        SocketContext._direction = None
        SocketContext._active_context = None
        pass


class DirectionalContext(SocketContext):
    """Base class for directional socket contexts"""

    _direction: Literal["INPUT", "OUTPUT"] = "INPUT"
    _active_context = None


class InputInterfaceContext(DirectionalContext):
    _direction = "INPUT"


class OutputInterfaceContext(DirectionalContext):
    _direction = "OUTPUT"


class TreeBuilder:
    """Builder for creating Blender geometry node trees with a clean Python API."""

    _active_tree: ClassVar["TreeBuilder | None"] = None
    _previous_tree: ClassVar["TreeBuilder | None"] = None
    just_added: "Node | None" = None

    def __init__(
        self, tree: "GeometryNodeTree | str | None" = None, arrange: bool = True
    ):
        if isinstance(tree, str):
            self.tree = bpy.data.node_groups.new(tree, "GeometryNodeTree")
        elif tree is None:
            self.tree = bpy.data.node_groups.new("GeometryNodeTree", "GeometryNodeTree")
        else:
            assert isinstance(tree, GeometryNodeTree)
            self.tree = tree

        # Create socket accessors for named access
        self.inputs = InputInterfaceContext(self)
        self.outputs = OutputInterfaceContext(self)
        self._arrange = arrange

    def __enter__(self):
        TreeBuilder._previous_tree = TreeBuilder._active_tree
        TreeBuilder._active_tree = self
        return self

    def __exit__(self, *args):
        if self._arrange:
            self.arrange()
        TreeBuilder._active_tree = TreeBuilder._previous_tree
        TreeBuilder._previous_tree = None

    @property
    def nodes(self) -> Nodes:
        return self.tree.nodes

    def __len__(self) -> int:
        return len(self.nodes)

    def arrange(self):
        settings = arrangebpy.LayoutSettings(
            horizontal_spacing=200, vertical_spacing=200, align_top_layer=True
        )
        arrangebpy.sugiyama_layout(self.tree, settings)

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

    def link(self, socket1: NodeSocket, socket2: NodeSocket):
        if isinstance(socket1, SocketLinker):
            socket1 = socket1.socket
        if isinstance(socket2, SocketLinker):
            socket2 = socket2.socket

        self.tree.links.new(socket1, socket2)

        if any(socket.is_inactive for socket in [socket1, socket2]):
            # the warning message should report which sockets from which nodes were linked and which were innactive
            for socket in [socket1, socket2]:
                if socket.is_inactive:
                    message = f"Socket {socket.name} from node {socket.node.name} is inactive."
                    message += f" It is linked to socket {socket2.name} from node {socket2.node.name}."
                    message += " This link will be created by Blender but ignored when evaluated."
                    message += f"Socket type: {socket.bl_idname}"
                    raise RuntimeError(message)

    def add(self, name: str) -> Node:
        self.just_added = self.tree.nodes.new(name)  # type: ignore
        assert self.just_added is not None
        return self.just_added


class NodeBuilder:
    """Base class for all geometry node wrappers."""

    node: Any
    name: str
    _tree: "TreeBuilder"
    _link_target: str | None = None
    _from_socket: NodeSocket | None = None
    _default_input_id: str | None = None
    _default_output_id: str | None = None
    _socket_data_types = tuple(SOCKET_COMPATIBILITY.keys())

    def __init__(self):
        # Get active tree from context manager
        tree = TreeBuilder._active_tree
        if tree is None:
            raise RuntimeError(
                f"Node '{self.__class__.__name__}' must be created within a TreeBuilder context manager.\n"
                f"Usage:\n"
                f"  with tree:\n"
                f"      node = {self.__class__.__name__}()\n"
            )

        self._tree = tree
        self._link_target = None
        if self.__class__.name is not None:
            self.node = self._tree.add(self.__class__.name)
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
    def _default_input_socket(self) -> NodeSocket:
        if self._default_input_id is not None:
            return self.node.inputs[self._input_idx(self._default_input_id)]
        return self.node.inputs[0]

    @property
    def _default_output_socket(self) -> NodeSocket:
        if self._default_output_id is not None:
            return self.node.outputs[self._output_idx(self._default_output_id)]
        return self.node.outputs[0]

    def _find_compatible_output_socket(self, linkable: "NodeBuilder") -> NodeSocket:
        """Find a compatible output socket from the linkable node that matches our accepted socket types."""
        # First try the default output socket
        default_output = linkable._default_output_socket
        for comp in SOCKET_COMPATIBILITY[default_output.type]:
            if comp in self._socket_data_types:
                return default_output

        # If default doesn't work, try all other output sockets
        for output_socket in linkable.node.outputs:
            for comp in SOCKET_COMPATIBILITY[output_socket.type]:
                if comp in self._socket_data_types:
                    return output_socket

        # No compatible socket found
        raise ValueError(
            f"No compatible output socket found on {linkable.node.name} for {self.__class__.__name__}. "
            f"Available output types: {[s.type for s in linkable.node.outputs]}, "
            f"Accepted input types: {self._socket_data_types}"
        )

    def _find_compatible_source_socket(
        self, source_node: "NodeBuilder", target_socket: NodeSocket
    ) -> NodeSocket:
        """Find a compatible output socket from source node that can link to the target input socket."""
        target_type = target_socket.type
        compatible_types = SOCKET_COMPATIBILITY.get(target_type, ())

        # Collect all compatible sockets with their compatibility priority
        compatible_sockets = []
        for output_socket in source_node.node.outputs:
            if output_socket.type in compatible_types:
                # Priority is the index in the compatibility list (0 = highest priority)
                priority = compatible_types.index(output_socket.type)
                compatible_sockets.append((priority, output_socket))

        if not compatible_sockets:
            # No compatible socket found
            raise ValueError(
                f"No compatible output socket found on {source_node.node.name} for target socket {target_socket.name} of type {target_type}. "
                f"Available output types: {[s.type for s in source_node.node.outputs]}, "
                f"Compatible types: {compatible_types}"
            )

        # Sort by priority (lowest number = highest priority) and return the best match
        compatible_sockets.sort(key=lambda x: x[0])
        return compatible_sockets[0][1]

    def _find_best_socket_pair(
        self, target_node: "NodeBuilder"
    ) -> tuple[NodeSocket, NodeSocket]:
        """Find the best compatible socket pair between this node (source) and target node."""
        # First try to connect default output to default input
        default_output = self._default_output_socket
        default_input = target_node._default_input_socket

        # Handle zone outputs that don't have inputs yet
        if default_input is None and hasattr(target_node, "_add_socket"):
            # Target is a zone without inputs - create compatible socket
            source_type = default_output.type
            compatible_types = SOCKET_COMPATIBILITY.get(source_type, [source_type])
            best_type = compatible_types[0] if compatible_types else source_type

            # Create socket on target zone
            default_input = target_node._add_socket(
                name=best_type.title(), type=best_type
            )
            return default_output, default_input




        # Check if default sockets are compatible
        if default_input is not None:
            output_compatibles = SOCKET_COMPATIBILITY.get(default_output.type, ())
            if default_input.type in output_compatibles and (
                not default_input.links or default_input.is_multi_input
            ):
                return default_output, default_input

        # If defaults don't work, try all combinations with priority-based matching
        best_match = None
        best_priority = float("inf")

        for output_socket in self.node.outputs:
            output_compatibles = SOCKET_COMPATIBILITY.get(output_socket.type, ())
            for input_socket in target_node.node.inputs:
                # Skip if socket already has a link and isn't multi-input
                if input_socket.links and not input_socket.is_multi_input:
                    continue

                if input_socket.type in output_compatibles:
                    # Calculate priority as the index in the compatibility list
                    priority = output_compatibles.index(input_socket.type)
                    if priority < best_priority:
                        best_priority = priority
                        best_match = (output_socket, input_socket)

        if best_match:
            return best_match

        # No compatible pair found
        available_outputs = [s.type for s in self.node.outputs]
        available_inputs = [
            s.type for s in target_node.node.inputs if not s.links or s.is_multi_input
        ]
        raise RuntimeError(
            f"Cannot link any output from {self.node.name} to any input of {target_node.node.name}. "
            f"Available output types: {available_outputs}, "
            f"Available input types: {available_inputs}"
        )

    def _socket_type_from_linkable(self, linkable: LINKABLE):
        if linkable is None:
            raise ValueError("Linkable cannot be None")

        # If it's a NodeBuilder, try to find a compatible output socket
        if hasattr(linkable, "node") and hasattr(linkable, "_default_output_socket"):
            compatible_socket = self._find_compatible_output_socket(linkable)
            socket_type = compatible_socket.type
            for comp in SOCKET_COMPATIBILITY[socket_type]:
                if comp in self._socket_data_types:
                    return comp if comp != "VALUE" else "FLOAT"

        # Fallback to original logic for other types
        for comp in SOCKET_COMPATIBILITY[linkable.type]:
            if comp in self._socket_data_types:
                return comp if comp != "VALUE" else "FLOAT"
        raise ValueError(
            f"Unsupported socket type for linking: {linkable}, type: {linkable.type=}"
        )

    def _add_inputs(self, *args, **kwargs) -> dict[str, LINKABLE]:
        """Dictionary with {new_socket.name: from_linkable} for link creation"""
        new_sockets = {}
        items = {}
        for arg in args:
            if isinstance(arg, bpy.types.NodeSocket):
                items[arg.name] = arg
            else:
                items[arg._default_output_socket.name] = arg
        items.update(kwargs)
        for key, value in items.items():
            # For NodeBuilder objects, find the best compatible output socket
            if hasattr(value, "node") and hasattr(value, "_default_output_socket"):
                compatible_socket = self._find_compatible_output_socket(value)
                # Create a SocketLinker to represent the specific socket we want to link from
                # from . import SocketLinker
                socket_linker = SocketLinker(compatible_socket)
                type = self._socket_type_from_linkable(value)
                socket = self._add_socket(name=key, type=type)
                new_sockets[socket.name] = socket_linker
            else:
                type = self._socket_type_from_linkable(value)
                socket = self._add_socket(name=key, type=type)
                new_sockets[socket.name] = value

        return new_sockets

    def _add_socket(
        self, name: str, type: str, default_value: Any | None = None
    ) -> NodeSocket:
        raise NotImplementedError

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

        raise RuntimeError()

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

    def link(self, source: LINKABLE | SocketLinker | NodeSocket, target: LINKABLE):
        self.tree.link(source_socket(source), target_socket(target))

    def link_to(self, target: LINKABLE):
        self.tree.link(self._default_output_socket, target_socket(target))

    def link_from(
        self,
        source: LINKABLE,
        input: LINKABLE | str,
    ):
        # Special handling for zone inputs that need auto-socket creation
        if (hasattr(source, 'items_collection') and 
            hasattr(source, '__rshift__') and 
            not isinstance(input, str)):
            # Use zone input's custom linking logic
            return source >> input
            
        if isinstance(input, str):
            try:
                self.link(source, self.node.inputs[input])
            except KeyError:
                self.link(source, self.node.inputs[self._input_idx(input)])
        else:
            self.link(source, input)

    def _smart_link_from(
        self,
        source: LINKABLE,
        input_name: str,
    ):
        """Smart linking that finds compatible sockets when default fails."""
        # Get the target input socket
        try:
            target_socket = self.node.inputs[input_name]
        except KeyError:
            target_socket = self.node.inputs[self._input_idx(input_name)]

        # If source is a NodeBuilder, find the best compatible output socket
        if isinstance(source, NodeBuilder):
            # Search for compatible output sockets - don't try default first as it might be wrong type
            try:
                compatible_output = self._find_compatible_source_socket(
                    source, target_socket
                )
                self.link(compatible_output, target_socket)
                return
            except ValueError:
                # No compatible socket found - this is an error, don't fall back
                raise ValueError(
                    f"Cannot link {source.node.name} to {self.node.name}.{input_name}: "
                    f"No compatible sockets. Available output types: {[s.type for s in source.node.outputs]}, "
                    f"Target socket type: {target_socket.type}, "
                    f"Compatible types: {SOCKET_COMPATIBILITY.get(target_socket.type, ())}"
                )
        else:
            # For other types, use original link_from behavior
            self.link_from(source, input_name)

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

    def _find_best_compatible_socket(
        self, target_node: "NodeBuilder", output_socket: NodeSocket
    ) -> NodeSocket:
        """Find the best compatible input socket on target node for the given output socket."""
        output_type = output_socket.type
        compatible_types = SOCKET_COMPATIBILITY.get(output_type, ())

        # Collect all compatible input sockets with their priority
        compatible_inputs = []
        for input_socket in target_node.node.inputs:
            # Skip if socket already has a link and isn't multi-input
            if input_socket.links and not input_socket.is_multi_input:
                continue

            if input_socket.type in compatible_types:
                # Priority is the index in the compatibility list (0 = highest priority)
                priority = compatible_types.index(input_socket.type)
                compatible_inputs.append((priority, input_socket))

        if not compatible_inputs:
            # No compatible socket found
            available_types = [
                socket.type
                for socket in target_node.node.inputs
                if not socket.links or socket.is_multi_input
            ]
            raise RuntimeError(
                f"Cannot link {output_type} output to {target_node.node.name}. "
                f"Compatible types: {compatible_types}, "
                f"Available input types: {available_types}"
            )

        # Sort by priority (lowest number = highest priority) and return the best match
        compatible_inputs.sort(key=lambda x: x[0])
        return compatible_inputs[0][1]

    def _establish_links(self, **kwargs: TYPE_INPUT_ALL):
        input_ids = [input.identifier for input in self.node.inputs]
        for name, value in kwargs.items():
            if value is None:
                continue

            if value is ...:
                # Ellipsis indicates this input should receive links from >> operator
                # which can potentially target multiple inputs on the new node
                if self._from_socket is not None:
                    self.link(
                        self._from_socket, self.node.inputs[self._input_idx(name)]
                    )

            # we can also provide just a default value for the socket to take if we aren't
            # providing a socket to link with
            elif isinstance(value, (NodeBuilder, NodeSocket, Node)):
                self._smart_link_from(value, name)
            else:
                if name in input_ids:
                    input = self.node.inputs[input_ids.index(name)]
                    self._set_input_default_value(input, value)
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
            # Direct socket linking - use default output
            socket_out = self._default_output_socket
            socket_in = other.socket
            other._from_socket = socket_out
        else:
            # NodeBuilder linking - need to find compatible sockets
            if other._link_target is not None:
                # Target socket is specified
                socket_in = self._get_input_socket_by_name(other, other._link_target)
                socket_out = self._default_output_socket

                # Try to find a better source socket if default doesn't work
                try:
                    socket_out = self._find_compatible_source_socket(self, socket_in)
                except ValueError:
                    # If no compatible socket found, use default and let the link fail with a clear error
                    pass

                other._from_socket = socket_out
            else:
                # No target specified - find best compatible socket pair
                socket_out, socket_in = self._find_best_socket_pair(other)
                other._from_socket = socket_out

        self.tree.link(socket_out, socket_in)
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
        from .nodes.converter import VectorMath

        values = (
            (self._default_output_socket, other)
            if not reverse
            else (other, self._default_output_socket)
        )

        # Determine if either operand is a vector type
        self_is_vector = self._default_output_socket.type == "VECTOR"
        other_is_vector = False
        if isinstance(other, NodeBuilder):
            other_is_vector = other._default_output_socket.type == "VECTOR"

        # Use VectorMath if either operand is a vector
        if self_is_vector or other_is_vector:
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
                        f"Unsupported type for {operation} with VECTOR socket: {type(other)}"
                    )
            else:
                vector_method = getattr(VectorMath, operation)
                if isinstance(other, (int, float)):
                    scalar_vector = (other, other, other)
                    return (
                        vector_method(scalar_vector, self._default_output_socket)
                        if not reverse
                        else vector_method(self._default_output_socket, scalar_vector)
                    )
                elif (
                    isinstance(other, (list, tuple)) and len(other) == 3
                ) or isinstance(other, NodeBuilder):
                    return vector_method(*values)

                else:
                    raise TypeError(
                        f"Unsupported type for {operation} with VECTOR operand: {type(other)}"
                    )
        else:
            # Both operands are scalar types, use regular Math
            from .nodes.converter import Math

            return getattr(Math, operation)(*values)

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


class SocketLinker(NodeBuilder):
    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self.socket = socket
        self.node = socket.node
        self._default_output_id = socket.identifier
        self._tree = TreeBuilder(socket.node.id_data)  # type: ignore

    @property
    def type(self) -> SOCKET_TYPES:
        return self.socket.type  # type: ignore

    @property
    def socket_name(self) -> str:
        return self.socket.name


class SocketBase(SocketLinker):
    """Base class for all socket definitions."""

    _bl_socket_type: str = ""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

        self._socket_context: SocketContext = SocketContext._active_context
        self.interface_socket = self._socket_context._create_socket(self)
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
            setattr(self.interface_socket, key, value)


class SocketGeometry(SocketBase):
    """Geometry socket - holds mesh, curve, point cloud, or volume data."""

    _bl_socket_type: str = "NodeSocketGeometry"
    socket: bpy.types.NodeTreeInterfaceSocketGeometry

    def __init__(self, name: str = "Geometry", description: str = ""):
        super().__init__(name, description)


class SocketBoolean(SocketBase):
    """Boolean socket - true/false value."""

    _bl_socket_type: str = "NodeSocketBool"
    socket: bpy.types.NodeTreeInterfaceSocketBool

    def __init__(
        self,
        name: str = "Boolean",
        default_value: bool = False,
        *,
        description: str = "",
        hide_value: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketFloat(SocketBase):
    """Float socket"""

    _bl_socket_type: str = "NodeSocketFloat"
    socket: bpy.types.NodeTreeInterfaceSocketFloat

    def __init__(
        self,
        name: str = "Value",
        default_value: float = 0.0,
        *,
        description: str = "",
        min_value: float | None = None,
        max_value: float | None = None,
        subtype: FloatInterfaceSubtypes = "NONE",
        hide_value: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            subtype=subtype,
            hide_value=hide_value,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketVector(SocketBase):
    _bl_socket_type: str = "NodeSocketVector"
    socket: bpy.types.NodeTreeInterfaceSocketVector

    def __init__(
        self,
        name: str = "Vector",
        default_value: tuple[float, float, float] = (0.0, 0.0, 0.0),
        *,
        description: str = "",
        dimensions: int = 3,
        min_value: float | None = None,
        max_value: float | None = None,
        hide_value: bool = False,
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
            hide_value=hide_value,
            subtype=subtype,
            default_attribute=default_attribute,
            attribute_domain=attribute_domain,
        )


class SocketInt(SocketBase):
    _bl_socket_type: str = "NodeSocketInt"
    socket: bpy.types.NodeTreeInterfaceSocketInt

    def __init__(
        self,
        name: str = "Integer",
        default_value: int = 0,
        *,
        description: str = "",
        min_value: int = -2147483648,
        max_value: int = 2147483647,
        hide_value: bool = False,
        subtype: IntegerInterfaceSubtypes = "NONE",
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            hide_value=hide_value,
            subtype=subtype,
            attribute_domain=attribute_domain,
            default_attribute=default_attribute,
        )


class SocketColor(SocketBase):
    """Color socket - RGB color value."""

    _bl_socket_type: str = "NodeSocketColor"
    socket: bpy.types.NodeTreeInterfaceSocketColor

    def __init__(
        self,
        name: str = "Color",
        default_value: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        *,
        description: str = "",
        hide_value: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        assert len(default_value) == 4, "Default color must be RGBA tuple"
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
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
        *,
        description: str = "",
        hide_value: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
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
        *,
        description: str = "",
        hide_value: bool = False,
        attribute_domain: _AttributeDomains = "POINT",
        default_attribute: str | None = None,
    ):
        super().__init__(name, description)
        self._set_values(
            hide_value=hide_value,
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
        *,
        description: str = "",
        hide_value: bool = False,
        subtype: StringInterfaceSubtypes = "NONE",
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
            subtype=subtype,
        )


class MenuSocket(SocketBase):
    """Menu socket - holds a selection from predefined items."""

    _bl_socket_type: str = "NodeSocketMenu"
    socket: bpy.types.NodeTreeInterfaceSocketMenu

    def __init__(
        self,
        name: str = "Menu",
        default_value: str | None = None,
        *,
        description: str = "",
        expanded: bool = False,
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            menu_expanded=expanded,
            hide_value=hide_value,
        )


class SocketObject(SocketBase):
    """Object socket - Blender object reference."""

    _bl_socket_type: str = "NodeSocketObject"
    socket: bpy.types.NodeTreeInterfaceSocketObject

    def __init__(
        self,
        name: str = "Object",
        default_value: bpy.types.Object | None = None,
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
        )


class SocketCollection(SocketBase):
    """Collection socket - Blender collection reference."""

    _bl_socket_type: str = "NodeSocketCollection"
    socket: bpy.types.NodeTreeInterfaceSocketCollection

    def __init__(
        self,
        name: str = "Collection",
        default_value: bpy.types.Collection | None = None,
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
        )


class SocketImage(SocketBase):
    """Image socket - Blender image datablock reference."""

    _bl_socket_type: str = "NodeSocketImage"
    socket: bpy.types.NodeTreeInterfaceSocketImage

    def __init__(
        self,
        name: str = "Image",
        default_value: bpy.types.Image | None = None,
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
        )


class SocketMaterial(SocketBase):
    """Material socket - Blender material reference."""

    _bl_socket_type: str = "NodeSocketMaterial"
    socket: bpy.types.NodeTreeInterfaceSocketMaterial

    def __init__(
        self,
        name: str = "Material",
        default_value: bpy.types.Material | None = None,
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            default_value=default_value,
            hide_value=hide_value,
        )


class SocketBundle(SocketBase):
    """Bundle socket - holds multiple data types in one socket."""

    _bl_socket_type: str = "NodeSocketBundle"
    socket: bpy.types.NodeTreeInterfaceSocketBundle

    def __init__(
        self,
        name: str = "Bundle",
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            hide_value=hide_value,
        )


class SocketClosure(SocketBase):
    """Closure socket - holds shader closure data."""

    _bl_socket_type: str = "NodeSocketClosure"
    socket: bpy.types.NodeTreeInterfaceSocketClosure

    def __init__(
        self,
        name: str = "Closure",
        *,
        description: str = "",
        hide_value: bool = False,
    ):
        super().__init__(name, description)
        self._set_values(
            hide_value=hide_value,
        )
