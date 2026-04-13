from __future__ import annotations

from typing import TYPE_CHECKING, Any

import bpy
from bpy.types import GeometryNodeTree, NodeSocket

from ..types import SOCKET_TYPES
from ._registry import _SOCKET_LINKER_REGISTRY
from ._utils import _NodeLike, _SocketLike
from .accessor import SocketAccessor
from .mixins import LinkingMixin, OperatorMixin
from .tree import TreeBuilder

if TYPE_CHECKING:
    from .node import BaseNode


class Socket(_SocketLike, OperatorMixin, LinkingMixin):
    """Wraps a single Blender NodeSocket, providing operator overloads and linking.

    Returned by ``SocketAccessor.get()`` / ``node.inputs[...]`` / ``node.outputs[...]``.
    Type-specific subclasses (``VectorSocket``, ``ColorSocket``, ``IntegerSocket``)
    are selected automatically via the registry.
    """

    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self.socket = socket
        self.node = socket.node
        self._default_output_id = socket.identifier
        self._tree = TreeBuilder(socket.node.id_data)  # type: ignore

    @property
    def tree(self) -> TreeBuilder:
        return self._tree

    @property
    def links(self) -> bpy.types.NodeLinks:
        links = self.socket.links
        assert links
        return links

    @property
    def _default_output_socket(self) -> NodeSocket:
        return self.socket

    @property
    def _default_input_socket(self) -> NodeSocket:
        return self.socket

    @property
    def outputs(self) -> SocketAccessor:
        return SocketAccessor([self.socket], "output", self.node)

    @property
    def inputs(self) -> SocketAccessor:
        return SocketAccessor([self.socket], "input", self.node)

    @property
    def type(self) -> SOCKET_TYPES:
        return self.socket.type  # type: ignore

    @property
    def socket_name(self) -> str:
        return self.socket.name

    @property
    def name(self) -> str:
        return str(self.socket.name)

    # -- Dispatch methods: per-type math logic. --
    # Called by OperatorMixin operators via _get_socket_linker().
    # Subclasses (and type-specific mixins) override to provide type-specific behaviour.

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "BaseNode":
        """Scalar math dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        math_operation = "floored_modulo" if operation == "modulo" else operation
        return getattr(Math, math_operation)(*values)

    def _dispatch_unary(self, operation: str) -> "BaseNode":
        """Scalar unary dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        if operation == "negate":
            return Math.multiply(self.socket, -1)
        elif operation == "absolute":
            return Math.absolute(self.socket)
        raise ValueError(f"Unknown unary operation: {operation}")

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "BaseNode":
        """Scalar floor division: divide then floor."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        divided = Math.divide(*values)
        return Math.floor(divided)

    def _dispatch_compare(self, other: Any, operation: str) -> "BaseNode":
        """Scalar comparison dispatch."""
        if isinstance(self._tree.tree, GeometryNodeTree):
            from ..nodes.geometry.manual import Compare

            return getattr(Compare, operation).float(self.socket, other)
        else:
            from ..nodes.geometry.converter import Math

            _MATH_COMPARE_MAP = {
                "less_than": ("less_than", False),
                "greater_than": ("greater_than", False),
                "less_equal": ("greater_than", True),
                "greater_equal": ("less_than", True),
            }
            math_op, negate = _MATH_COMPARE_MAP[operation]
            result = getattr(Math, math_op)(self.socket, other)
            if negate:
                result = Math.subtract(1.0, result._default_output_socket)
            return result


# ---------------------------------------------------------------------------
# Type-specific behaviour mixins
# ---------------------------------------------------------------------------


class _VectorMixin:
    """Vector-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocket
    _tree: TreeBuilder

    def _separated_value(self, value: str) -> Socket:
        from ..nodes.geometry import SeparateXYZ

        for link in self.socket.links:
            if link.to_node.bl_idname == "ShaderNodeSeparateXYZ":
                return Socket(link.to_node.outputs[value])

        return getattr(SeparateXYZ(self), f"o_{value.lower()}")

    @property
    def x(self) -> Socket:
        return self._separated_value("X")

    @property
    def y(self) -> Socket:
        return self._separated_value("Y")

    @property
    def z(self) -> Socket:
        return self._separated_value("Z")

    def _dispatch_unary(self, operation: str) -> "BaseNode":
        from ..nodes.geometry import VectorMath

        if operation == "negate":
            return VectorMath.scale(self.socket, -1)
        elif operation == "absolute":
            return VectorMath.absolute(self.socket)
        raise ValueError(f"Unknown unary operation: {operation}")

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "BaseNode":
        from ..nodes.geometry import VectorMath

        values = (self.socket, other) if not reverse else (other, self.socket)

        if operation == "multiply":
            if isinstance(other, (int, float)):
                return VectorMath.scale(self.socket, other)
            elif isinstance(other, NodeSocket) and other.type in (
                "VALUE",
                "FLOAT",
                "INT",
            ):
                return VectorMath.scale(self.socket, other)
            elif isinstance(other, (_SocketLike, _NodeLike)) and getattr(other, "type", None) in (
                "VALUE",
                "FLOAT",
                "INT",
            ):
                return VectorMath.scale(self.socket, other._default_output_socket)
            elif isinstance(other, (list, tuple)) and len(other) == 3:
                return VectorMath.multiply(*values)
            elif isinstance(other, (_SocketLike, _NodeLike, NodeSocket)):
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
                    vector_method(self.socket, scalar_vector)
                    if not reverse
                    else vector_method(scalar_vector, self.socket)
                )
            elif (isinstance(other, (list, tuple)) and len(other) == 3) or isinstance(
                other, (_SocketLike, _NodeLike, NodeSocket)
            ):
                return vector_method(*values)
            else:
                raise TypeError(
                    f"Unsupported type for {operation} with VECTOR operand: {type(other)}"
                )

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "BaseNode":
        from ..nodes.geometry import VectorMath

        divided = self._dispatch_math(other, "divide", reverse=reverse)
        return VectorMath.floor(divided)

    def _dispatch_compare(self, other: Any, operation: str) -> "BaseNode":
        if isinstance(self._tree.tree, GeometryNodeTree):
            from ..nodes.geometry.manual import Compare

            return getattr(Compare, operation).vector(self.socket, other)
        else:
            return Socket._dispatch_compare(self, other, operation)  # type: ignore[arg-type]


_SEPARATE_COLOR_IDNAMES = (
    "FunctionNodeSeparateColor",
    "ShaderNodeSeparateColor",
    "CompositorNodeSeparateColor",
)


class _ColorMixin:
    """Color-specific properties (.r, .g, .b, .a)."""

    socket: NodeSocket
    _tree: TreeBuilder

    def _get_separate_color_cls(self):
        tree_type = self._tree.tree.bl_idname
        if tree_type == "ShaderNodeTree":
            from ..nodes.shader.converter import SeparateColor
        elif tree_type == "CompositorNodeTree":
            from ..nodes.compositor.converter import SeparateColor
        else:
            from ..nodes.geometry.converter import SeparateColor
        return SeparateColor

    def _separated_channel(self, channel: str) -> Socket:
        for link in self.socket.links:
            if link.to_node.bl_idname in _SEPARATE_COLOR_IDNAMES:
                return Socket(link.to_node.outputs[channel])

        SeparateColor = self._get_separate_color_cls()
        return getattr(SeparateColor(self), f"o_{channel.lower()}")

    @property
    def r(self) -> Socket:
        return self._separated_channel("Red")

    @property
    def g(self) -> Socket:
        return self._separated_channel("Green")

    @property
    def b(self) -> Socket:
        return self._separated_channel("Blue")

    @property
    def a(self) -> Socket:
        return self._separated_channel("Alpha")


class _IntegerMixin:
    """Integer-specific dispatch — uses IntegerMath in geometry trees."""

    socket: NodeSocket
    _tree: TreeBuilder

    @property
    def _is_geometry_tree(self) -> bool:
        return self._tree.tree.bl_idname == "GeometryNodeTree"

    @staticmethod
    def _is_integer_socket(value: Any) -> bool:
        socket = getattr(
            value, "socket", getattr(value, "_default_output_socket", None)
        )
        return isinstance(socket, NodeSocket) and socket.type == "INT"

    def _other_is_integer(self, other: Any) -> bool:
        return isinstance(other, int) or self._is_integer_socket(other)

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "BaseNode":
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return getattr(IntegerMath, operation)(*values)
        return Socket._dispatch_math(self, other, operation, reverse)  # type: ignore[arg-type]

    def _dispatch_unary(self, operation: str) -> "BaseNode":
        if self._is_geometry_tree:
            from ..nodes.geometry.converter import IntegerMath

            if operation == "negate":
                return IntegerMath.negate(self.socket)
            elif operation == "absolute":
                return IntegerMath.absolute(self.socket)
        return Socket._dispatch_unary(self, operation)  # type: ignore[arg-type]

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "BaseNode":
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return IntegerMath.divide_floor(*values)
        return Socket._dispatch_floordiv(self, other, reverse)  # type: ignore[arg-type]

    def _dispatch_compare(self, other: Any, operation: str) -> "BaseNode":
        if isinstance(self._tree.tree, GeometryNodeTree):
            from ..nodes.geometry.manual import Compare

            return getattr(Compare, operation).integer(self.socket, other)
        return Socket._dispatch_compare(self, other, operation)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Registry-target socket classes
# Used by _get_socket_linker() for runtime socket wrapping.
# The corresponding SocketVector / SocketColor / SocketInt in interface.py
# inherit the same mixins and gain identical behaviour for interface sockets.
# ---------------------------------------------------------------------------


class VectorSocket(_VectorMixin, Socket):
    """Runtime vector socket wrapper."""


class ColorSocket(_ColorMixin, Socket):
    """Runtime color socket wrapper."""


class IntegerSocket(_IntegerMixin, Socket):
    """Runtime integer socket wrapper."""


_SOCKET_LINKER_REGISTRY["NodeSocketVector"] = VectorSocket
_SOCKET_LINKER_REGISTRY["NodeSocketColor"] = ColorSocket
_SOCKET_LINKER_REGISTRY["NodeSocketInt"] = IntegerSocket
