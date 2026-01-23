from __future__ import annotations

from ast import Return
from typing import TYPE_CHECKING, Any, ClassVar, Literal

from arrangebpy.arrange.routing import Socket
from numpy import isin

if TYPE_CHECKING:
    from .nodes import Math, VectorMath

import arrangebpy
import bpy
from bpy.types import (
    GeometryNodeTree,
    Node,
    Nodes,
    NodeSocket,
)

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


class SocketError(Exception):
    """Raised when a socket operation fails."""


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
        self, socket_def: SocketBase, name: str
    ) -> bpy.types.NodeTreeInterfaceSocket:
        """Create a socket from a socket definition."""
        socket = self.interface.new_socket(
            name=name,
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
        self, tree: GeometryNodeTree | str = "Geometry Nodes", arrange: bool = True
    ):
        if isinstance(tree, str):
            self.tree = bpy.data.node_groups.new(tree, "GeometryNodeTree")
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

    def link(self, socket1: NodeSocket, socket2: NodeSocket) -> bpy.types.NodeLink:
        if isinstance(socket1, SocketLinker):
            socket1 = socket1.socket
        if isinstance(socket2, SocketLinker):
            socket2 = socket2.socket

        link = self.tree.links.new(socket1, socket2, handle_dynamic_sockets=True)

        if any(socket.is_inactive for socket in [socket1, socket2]):
            assert socket1.node
            assert socket2.node
            # the warning message should report which sockets from which nodes were linked and which were innactive
            for socket in [socket1, socket2]:
                # we want to be loud about it if we end up linking an inactive socket to a node that is not a switch
                if socket.is_inactive and socket.node.bl_idname not in (  # type: ignore
                    "GeometryNodeIndexSwitch",
                    "GeometryNodeMenuSwitch",
                ):
                    message = f"Socket {socket.name} from node {socket.node.name} is inactive."  # type: ignore
                    message += f" It is linked to socket {socket2.name} from node {socket2.node.name}."
                    message += " This link will be created by Blender but ignored when evaluated."
                    message += f"Socket type: {socket.bl_idname}"
                    raise RuntimeError(message)

        return link

    def add(self, name: str) -> Node:
        return self.tree.nodes.new(name)


class NodeBuilder:
    """Base class for all geometry node wrappers."""

    node: Any
    _bl_idname: str
    _tree: "TreeBuilder"
    _link_target: str | None = None
    _from_socket: NodeSocket | None = None
    _default_input_id: str | None = None
    _default_output_id: str | None = None

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
            print(f"skipping inactive socket {socket.name}")
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
            return sorted(possible, key=lambda x: compatible.index(x.type))[0]

        raise SocketError("No compatible output sockets found")

    @staticmethod
    def _find_best_socket_pair(
        source: "NodeBuilder | NodeSocket", target: "NodeBuilder | NodeSocket"
    ) -> tuple[NodeSocket, NodeSocket]:
        """Find the best possible compatible pair of sockets between two nodes, looking only at the
        the currently available outputs from the source and the inputs from the target"""
        possible_combos = []
        if isinstance(source, NodeBuilder):
            outputs = source._available_outputs
        else:
            outputs = [source]
        if isinstance(target, NodeBuilder):
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
            f"Cannot link any output from {source.node.name} to any input of {target.node.name}. "
            f"Available output types: {outputs}, "
            f"Available input types: {inputs}"
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

    def _link(
        self, source: LINKABLE | SocketLinker | NodeSocket, target: LINKABLE
    ) -> bpy.types.NodeLink:
        return self.tree.link(self._source_socket(source), self._target_socket(target))

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
            if value is None:
                continue
            if isinstance(value, Node):
                node = NodeBuilder()
                node.node = value
                value = node

            if value is ...:
                # Ellipsis indicates this input should receive links from >> operator
                # which can potentially target multiple inputs on the new node
                if self._from_socket is not None:
                    self._link_from(self._from_socket, name)

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
        else:
            source, target = self._find_best_socket_pair(self, other)

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
        from .nodes import VectorMath

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
            from .nodes.converter import IntegerMath, Math

            if isinstance(other, int) and self._default_output_socket.type == "INT":
                return getattr(IntegerMath, operation)(*values)
            else:
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


class DynamicInputsMixin:
    _socket_data_types: tuple[str]
    _type_map: dict[str, str] = {}

    def _match_compatible_source(self, source: NodeBuilder) -> str:
        possible = []
        for output in source._available_outputs:
            compatible = SOCKET_COMPATIBILITY.get(output.type, ())
            possible = [
                (type, compatible.index(type))
                for type in self._socket_data_types
                if type in compatible
            ]

        if possible:
            return sorted(possible, key=lambda x: x[1])[0][0]

        raise SocketError("No compatible socket found")

    def _find_best_socket_pair(
        self, source: NodeBuilder, target: NodeBuilder
    ) -> tuple[NodeSocket, NodeSocket] | None:
        try:
            return super()._find_best_socket_pair(source, target)
        except SocketError:
            new_sockets = self._add_inputs(source)
            return (source, list(new_sockets.values())[0])

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
            type = self._match_compatible_source(source)
            print(f"{key=}, {source=}, {type=}")
            if type in self._type_map:
                type = self._type_map[type]
            socket = self._add_socket(name=key, type=type)
            new_sockets[socket.name] = source

        return new_sockets


class SocketLinker(NodeBuilder):
    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self.socket = socket
        self.node = socket.node
        self._default_output_id = socket.identifier
        self._tree = TreeBuilder(socket.node.id_data)  # type: ignore

    @property
    def _available_outputs(self) -> list[NodeSocket]:
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

        self._socket_context: SocketContext = SocketContext._active_context
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
            setattr(self.interface_socket, key, value)

    @property
    def default_value(self):
        if not hasattr(self.interface_socket, "default_value"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'default_value'"
            )
        return self.interface_socket.default_value

    @default_value.setter
    def default_value(self, value):
        if not hasattr(self.interface_socket, "default_value"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'default_value'"
            )
        self.interface_socket.default_value = value


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
