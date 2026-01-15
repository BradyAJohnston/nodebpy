from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal

import arrangebpy
import bpy
from bpy.types import (
    GeometryNodeTree,
    Node,
    Nodes,
    NodeSocket,
)

from .nodes.types import (
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


# POSSIBLE_NODE_NAMES = "GeometryNode"
LINKABLE = "Node | NodeSocket | NodeBuilder"
TYPE_INPUT_VECTOR = "NodeSocketVector | Vector | NodeBuilder | list[float] | tuple[float, float, float] | None"
TYPE_INPUT_ROTATION = "NodeSocketRotation | Quaternion | NodeBuilder | list[float] | tuple[float, float, float, float] | None"
TYPE_INPUT_BOOLEAN = "NodeSocketBool | bool | NodeBuilder | None"


def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to 'geometry' or 'my_socket'."""
    return name.lower().replace(" ", "_")


def denormalize_name(attr_name: str) -> str:
    """Convert 'geometry' or 'my_socket' to 'Geometry' or 'My Socket'."""
    return attr_name.replace("_", " ").title()


def source_socket(node: LINKABLE) -> NodeSocket:
    if isinstance(node, NodeSocket):
        return node
    elif isinstance(node, Node):
        return node.outputs[0]
    elif hasattr(node, "_default_output_socket"):
        # NodeBuilder or SocketNodeBuilder
        return node._default_output_socket
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


def target_socket(node: LINKABLE) -> NodeSocket:
    if isinstance(node, NodeSocket):
        return node
    elif isinstance(node, Node):
        return node.inputs[0]
    elif hasattr(node, "_default_input_socket"):
        # NodeBuilder or SocketNodeBuilder
        return node._default_input_socket
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


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


class InputInterfaceContext(SocketContext):
    _direction = "INPUT"
    _active_context = None


class OutputInterfaceContext(SocketContext):
    _direction = "OUTPUT"
    _active_context = None


class NodeBuilder:
    """Base class for all geometry node wrappers."""

    node: Node
    name: str
    _tree: "TreeBuilder"
    _link_target: str | None = None  # Track which input should receive links
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

        self.inputs = InputInterfaceContext(tree)
        self.outputs = OutputInterfaceContext(tree)

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
    def _default_input_socket(self) -> NodeSocket:
        if self._default_input_id is not None:
            return self.node.inputs[self._input_idx(self._default_input_id)]
        return self.node.inputs[0]

    @property
    def _default_output_socket(self) -> NodeSocket:
        if self._default_output_id is not None:
            return self.node.outputs[self._output_idx(self._default_output_id)]
        return self.node.outputs[0]

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
        return input_ids.index(identifier)

    def _output_idx(self, identifier: str) -> int:
        output_ids = [output.identifier for output in self.node.outputs]
        return output_ids.index(identifier)

    def _input(self, identifier: str) -> SocketLinker:
        """Input socket: Vector"""
        return SocketLinker(self.node.inputs[self._input_idx(identifier)])

    def _output(self, identifier: str) -> SocketLinker:
        """Output socket: Vector"""
        return SocketLinker(self.node.outputs[self._output_idx(identifier)])

    def link(self, source: LINKABLE, target: LINKABLE):
        self.tree.link(source_socket(source), target_socket(target))

    def link_to(self, target: LINKABLE):
        self.tree.link(self._default_output_socket, target_socket(target))

    def link_from(self, source: LINKABLE, input: "LINKABLE | str"):
        if isinstance(input, str):
            try:
                self.link(source, self.node.inputs[input])
            except KeyError:
                self.link(source, self.node.inputs[self._input_idx(input)])
        else:
            self.link(source, input)

    def _establish_links(self, **kwargs):
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
            elif isinstance(value, (NodeBuilder, SocketNodeBuilder, NodeSocket, Node)):
                # print("Linking from", value, "to", name)
                self.link_from(value, name)
            else:
                if name in input_ids:
                    input = self.node.inputs[input_ids.index(name)]
                    input.default_value = value
                else:
                    input = self.node.inputs[name.replace("_", "").capitalize()]
                    input.default_value = value

    def __rshift__(self, other: "NodeBuilder") -> "NodeBuilder":
        """Chain nodes using >> operator. Links output to input.

        Usage:
            node1 >> node2 >> node3
            tree.inputs.value >> Math.add(..., 0.1) >> tree.outputs.result

        If the target node has an ellipsis placeholder (...), links to that specific input.
        Otherwise, tries to find Geometry sockets first, then falls back to default.

        Returns the right-hand node to enable continued chaining.
        """
        # Get source socket - prefer Geometry, fall back to default
        socket_out = self.node.outputs.get("Geometry") or self._default_output_socket
        other._from_socket = socket_out

        # Get target socket
        if other._link_target is not None:
            # Use specific target if set by ellipsis
            socket_in = self._get_input_socket_by_name(other, other._link_target)
        else:
            # Default behavior - prefer Geometry, fall back to default
            socket_in = other.node.inputs.get("Geometry") or other._default_input_socket

        # If target socket already has a link and isn't multi-input, try next available socket
        if socket_in.links and not socket_in.is_multi_input:
            socket_in = (
                self._get_next_available_socket(socket_in, socket_out) or socket_in
            )

        self.tree.link(socket_out, socket_in)
        return other

    def _get_input_socket_by_name(self, node: "NodeBuilder", name: str) -> NodeSocket:
        """Get input socket by name, trying direct access first, then title case."""
        try:
            return node.node.inputs[name]
        except KeyError:
            # Try with title case if direct access fails
            title_name = name.replace("_", " ").title()
            return node.node.inputs[title_name]

    def _get_next_available_socket(
        self, socket: NodeSocket, socket_out: NodeSocket
    ) -> NodeSocket | None:
        """Get the next available socket after the given one."""
        try:
            inputs = socket.node.inputs
            current_idx = inputs.find(socket.identifier)
            if current_idx >= 0 and current_idx + 1 < len(inputs):
                if socket_out.type == "GEOMETRY":
                    # Prefer Geometry sockets
                    for idx in range(current_idx + 1, len(inputs)):
                        if inputs[idx].type == "GEOMETRY" and not inputs[idx].links:
                            return inputs[idx]
                    raise RuntimeError("No available Geometry input sockets found.")
                return inputs[current_idx + 1]
        except (KeyError, IndexError, AttributeError):
            pass
        return None

    def __mul__(self, other: Any) -> "VectorMath | Math":
        from .nodes import Math, VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                if isinstance(other, (int, float)):
                    return VectorMath.scale(self._default_output_socket, other)
                elif isinstance(other, (list, tuple)) and len(other) == 3:
                    return VectorMath.multiply(self._default_output_socket, other)
                else:
                    raise TypeError(
                        f"Unsupported type for multiplication with VECTOR socket: {type(other)}"
                    )
            case "VALUE":
                return Math.multiply(self._default_output_socket, other)
            case _:
                raise TypeError(
                    f"Unsupported socket type for multiplication: {self._default_output_socket.type}"
                )

    def __rmul__(self, other: Any) -> "VectorMath | Math":
        from .nodes import Math, VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                if isinstance(other, (int, float)):
                    return VectorMath.scale(self._default_output_socket, other)
                elif isinstance(other, (list, tuple)) and len(other) == 3:
                    return VectorMath.multiply(other, self._default_output_socket)
                else:
                    raise TypeError(
                        f"Unsupported type for multiplication with VECTOR socket: {type(other)}"
                    )
            case "VALUE":
                return Math.multiply(other, self._default_output_socket)
            case _:
                raise TypeError(
                    f"Unsupported socket type for multiplication: {self._default_output_socket.type}"
                )

    def __truediv__(self, other: Any) -> "VectorMath":
        from .nodes import VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                return VectorMath.divide(self._default_output_socket, other)
            case _:
                raise TypeError(
                    f"Unsupported socket type for division: {self._default_output_socket.type}"
                )

    def __rtruediv__(self, other: Any) -> "VectorMath":
        from .nodes import VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                return VectorMath.divide(other, self._default_output_socket)
            case _:
                raise TypeError(
                    f"Unsupported socket type for division: {self._default_output_socket.type}"
                )

    def __add__(self, other: Any) -> "VectorMath | Math":
        from .nodes import Math, VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                return VectorMath.add(self._default_output_socket, other)
            case "VALUE":
                return Math.add(self._default_output_socket, other)
            case _:
                raise TypeError(
                    f"Unsupported socket type for addition: {self._default_output_socket.type}"
                )

    def __radd__(self, other: Any) -> "VectorMath | Math":
        from .nodes import Math, VectorMath

        match self._default_output_socket.type:
            case "VECTOR":
                return VectorMath.add(other, self._default_output_socket)
            case "VALUE":
                return Math.add(other, self._default_output_socket)
            case _:
                raise TypeError(
                    f"Unsupported socket type for addition: {self._default_output_socket.type}"
                )


class SocketLinker(NodeBuilder):
    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self.socket = socket
        self.node = socket.node
        self._default_output_id = socket.identifier
        self._tree = TreeBuilder(socket.node.id_data)  # type: ignore

    @property
    def type(self) -> str:
        return self.socket.type


class SocketNodeBuilder(NodeBuilder):
    """Special NodeBuilder for accessing specific sockets on input/output nodes."""

    def __init__(self, node: Node, socket_name: str, direction: str):
        # Don't call super().__init__ - we already have a node
        self.node = node
        self._tree = TreeBuilder(node.id_data)  # type: ignore
        self._socket_name = socket_name
        self._direction = direction

    @property
    def _default_output_socket(self) -> NodeSocket:
        """Return the specific named output socket."""
        if self._direction == "INPUT":
            return self.node.outputs[self._socket_name]
        else:
            raise ValueError("Output nodes don't have outputs")

    @property
    def _default_input_socket(self) -> NodeSocket:
        """Return the specific named input socket."""
        if self._direction == "OUTPUT":
            return self.node.inputs[self._socket_name]
        else:
            raise ValueError("Input nodes don't have inputs")


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
        super().__init__(name, description)
        assert len(default_value) == dimensions, (
            "Default value length must match dimensions"
        )
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
        super().__init__(name, description)
        assert len(default_value) == 4, "Default color must be RGBA tuple"
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
        assert len(default_value) == 4, "Default rotation must be quaternion tuple"
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
