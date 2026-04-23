from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator, overload

import bpy
from bpy.types import (
    FunctionNodeAlignRotationToVector,
    FunctionNodeCombineMatrix,
    FunctionNodeRotationToEuler,
    FunctionNodeRotationToQuaternion,
    FunctionNodeSeparateMatrix,
    GeometryNodeTree,
    NodeLinks,
    NodeSocket,
)

from ..types import SOCKET_TYPES
from ._registry import _SOCKET_LINKER_REGISTRY, _get_socket_linker
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
    def links(self) -> NodeLinks | None:
        return self.socket.links

    @property
    def _default_output_socket(self) -> NodeSocket:
        return self.socket

    @property
    def _default_input_socket(self) -> NodeSocket:
        return self.socket

    @property
    def outputs(self) -> SocketAccessor:
        return SocketAccessor([self.socket], "output")

    @property
    def inputs(self) -> SocketAccessor:
        return SocketAccessor([self.socket], "input")

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

            return getattr(Compare.float, operation)(self.socket, other)
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

        return SeparateXYZ(self).o._get(value.lower())

    @property
    def x(self) -> Socket:
        return self._separated_value("X")

    @property
    def y(self) -> Socket:
        return self._separated_value("Y")

    @property
    def z(self) -> Socket:
        return self._separated_value("Z")

    def _get_or_create_combine_xyz(self) -> "bpy.types.Node":
        from ..nodes.geometry.converter import CombineXYZ

        for link in self.socket.links:
            if link.from_node.bl_idname == "ShaderNodeCombineXYZ":
                return link.from_node
        combine = CombineXYZ()
        self._tree.link(combine.node.outputs[0], self.socket)
        return combine.node

    @overload
    def __getitem__(self, key: slice) -> "list[Socket]": ...
    @overload
    def __getitem__(self, key: int) -> "Socket": ...
    def __getitem__(self, key: int | slice) -> "Socket | list[Socket]":
        if self.socket.is_output:
            return [self.x, self.y, self.z][key]
        node = self._get_or_create_combine_xyz()
        return [_get_socket_linker(node.inputs[i]) for i in range(3)][key]

    def __iter__(self) -> Iterator["Socket"]:
        if self.socket.is_output:
            yield self.x
            yield self.y
            yield self.z
        else:
            node = self._get_or_create_combine_xyz()
            for i in node.inputs:
                yield _get_socket_linker(i)

    def __len__(self) -> int:
        return 3

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
            elif isinstance(other, (_SocketLike, _NodeLike)) and getattr(
                other, "type", None
            ) in (
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

            return getattr(Compare.vector, operation)(self.socket, other)
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
        return SeparateColor(self).o._get(channel.lower())

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

    _COMBINE_COLOR_IDNAMES = (
        "FunctionNodeCombineColor",
        "ShaderNodeCombineColor",
        "CompositorNodeCombineColor",
    )

    def _get_combine_color_cls(self):
        tree_type = self._tree.tree.bl_idname
        if tree_type == "ShaderNodeTree":
            from ..nodes.shader.converter import CombineColor
        elif tree_type == "CompositorNodeTree":
            from ..nodes.compositor.converter import CombineColor
        else:
            from ..nodes.geometry.converter import CombineColor
        return CombineColor

    def _get_or_create_combine_color(self) -> "bpy.types.Node":
        if self.socket.links:
            for link in self.socket.links:
                assert link.from_node
                if link.from_node.bl_idname in self._COMBINE_COLOR_IDNAMES:
                    return link.from_node
        CombineColor = self._get_combine_color_cls()
        combine = CombineColor()
        self._tree.link(combine.node.outputs[0], self.socket)
        return combine.node

    @overload
    def __getitem__(self, key: slice) -> "list[Socket]": ...
    @overload
    def __getitem__(self, key: int) -> "Socket": ...
    def __getitem__(self, key: int | slice) -> "Socket | list[Socket]":
        if self.socket.is_output:
            return [self.r, self.g, self.b, self.a][key]
        node = self._get_or_create_combine_color()
        return [_get_socket_linker(node.inputs[i]) for i in range(4)][key]

    def __iter__(self) -> Iterator["Socket"]:
        if self.socket.is_output:
            yield self.r
            yield self.g
            yield self.b
            yield self.a
        else:
            node = self._get_or_create_combine_color()
            for input in node.inputs:
                yield _get_socket_linker(input)

    def __len__(self) -> int:
        return 4


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

            return getattr(Compare.integer, operation)(self.socket, other)
        return Socket._dispatch_compare(self, other, operation)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Type-specific behaviour mixins (continued)
# ---------------------------------------------------------------------------


class _BooleanMixin:
    """Boolean-specific operator overrides — routes directly through BooleanMath."""

    socket: NodeSocket

    def __or__(self, other: Any) -> "BaseNode":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(self.socket, other)

    def __and__(self, other: Any) -> "BaseNode":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(self.socket, other)


class _RotationMixin:
    """Rotation-specific properties (.w, .x, .y, .z) via RotationToQuaternion."""

    socket: NodeSocket
    _tree: TreeBuilder

    def _quaternion_component(self, component: str) -> FloatSocket:
        from ..nodes.geometry.converter import RotationToQuaternion

        if self.socket.links:
            for link in self.socket.links:
                if isinstance(link.to_node, FunctionNodeRotationToQuaternion):
                    return _get_socket_linker(link.to_node.outputs[component])
        return RotationToQuaternion(self.socket).o[component]

    @property
    def w(self) -> FloatSocket:
        return self._quaternion_component("W")

    @property
    def x(self) -> FloatSocket:
        return self._quaternion_component("X")

    @property
    def y(self) -> FloatSocket:
        return self._quaternion_component("Y")

    @property
    def z(self) -> FloatSocket:
        return self._quaternion_component("Z")

    @property
    def euler(self) -> "VectorSocket":
        from ..nodes.geometry.converter import RotationToEuler

        if self.socket.links:
            for link in self.socket.links:
                if isinstance(link.to_node, FunctionNodeRotationToEuler):
                    return _get_socket_linker(link.to_node.outputs["Euler"])
        return RotationToEuler(self.socket).o.euler


class _MatrixMixin:
    """Matrix-specific properties (.translation, .rotation, .scale) via SeparateTransform."""

    socket: NodeSocket
    _tree: TreeBuilder

    def _separate_transform(self, output: str) -> Socket:
        from ..nodes.geometry.converter import SeparateTransform

        for link in self.socket.links:
            if link.to_node.bl_idname == "FunctionNodeSeparateTransform":
                return _get_socket_linker(link.to_node.outputs[output])
        return SeparateTransform(self).outputs._get(output)

    @property
    def translation(self) -> "VectorSocket":
        return self._separate_transform("Translation")  # type: ignore[return-value]

    @property
    def rotation(self) -> "RotationSocket":
        return self._separate_transform("Rotation")  # type: ignore[return-value]

    @property
    def scale(self) -> "VectorSocket":
        return self._separate_transform("Scale")  # type: ignore[return-value]

    def _get_or_create_separate_matrix(self) -> FunctionNodeSeparateMatrix:
        from ..nodes.geometry.converter import SeparateMatrix

        if self.socket.links:
            for link in self.socket.links:
                if isinstance(link.to_node, FunctionNodeSeparateMatrix):
                    return link.to_node
        return SeparateMatrix(self).node

    def _get_or_create_combine_matrix(self) -> FunctionNodeCombineMatrix:
        from ..nodes.geometry.converter import CombineMatrix

        if self.socket.links:
            for link in self.socket.links:
                if isinstance(link.from_node, FunctionNodeCombineMatrix):
                    return link.from_node

        combine = CombineMatrix()
        self._tree.link(combine.node.outputs[0], self.socket)
        return combine.node

    @overload
    def __getitem__(self, key: slice) -> "list[Socket]": ...
    @overload
    def __getitem__(self, key: int) -> "Socket": ...
    def __getitem__(self, key: int | slice) -> "Socket | list[Socket]":
        if self.socket.is_output:
            node = self._get_or_create_separate_matrix()
            outputs = node.outputs
            if isinstance(key, slice):
                return [
                    _get_socket_linker(outputs[i])
                    for i in range(*key.indices(len(outputs)))
                ]
            return _get_socket_linker(outputs[key])
        node = self._get_or_create_combine_matrix()
        inputs = node.inputs
        if isinstance(key, slice):
            return [
                _get_socket_linker(inputs[i]) for i in range(*key.indices(len(inputs)))
            ]
        return _get_socket_linker(inputs[key])

    def __iter__(self) -> Iterator["Socket"]:
        if self.socket.is_output:
            node = self._get_or_create_separate_matrix()
            return iter(_get_socket_linker(o) for o in node.outputs)
        node = self._get_or_create_combine_matrix()
        return iter(_get_socket_linker(i) for i in node.inputs)

    def __len__(self) -> int:
        return 16


# ---------------------------------------------------------------------------
# Registry-target socket classes
# Used by _get_socket_linker() for runtime socket wrapping.
# The corresponding SocketVector / SocketColor / etc. in interface.py
# inherit the same mixins and gain identical behaviour for interface sockets.
# ---------------------------------------------------------------------------


class FloatSocket(Socket):
    """Runtime float socket wrapper."""


class VectorSocket(_VectorMixin, Socket):
    """Runtime vector socket wrapper."""


class ColorSocket(_ColorMixin, Socket):
    """Runtime color socket wrapper."""


class IntegerSocket(_IntegerMixin, Socket):
    """Runtime integer socket wrapper."""


class BooleanSocket(_BooleanMixin, Socket):
    """Runtime boolean socket wrapper."""


class RotationSocket(_RotationMixin, Socket):
    """Runtime rotation socket wrapper."""


class MatrixSocket(_MatrixMixin, Socket):
    """Runtime matrix socket wrapper."""


class StringSocket(Socket):
    """Runtime string socket wrapper."""


class MenuSocket(Socket):
    """Runtime menu socket wrapper."""


class GeometrySocket(Socket):
    """Runtime geometry socket wrapper."""


class ObjectSocket(Socket):
    """Runtime object socket wrapper."""


class MaterialSocket(Socket):
    """Runtime material socket wrapper."""


class ImageSocket(Socket):
    """Runtime image socket wrapper."""


class CollectionSocket(Socket):
    """Runtime collection socket wrapper."""


class BundleSocket(Socket):
    """Runtime bundle socket wrapper."""


class ClosureSocket(Socket):
    """Runtime closure socket wrapper."""


class ShaderSocket(Socket):
    """Runtime shader socket wrapper."""


_SOCKET_LINKER_REGISTRY["NodeSocketFloat"] = FloatSocket
_SOCKET_LINKER_REGISTRY["NodeSocketVector"] = VectorSocket
_SOCKET_LINKER_REGISTRY["NodeSocketColor"] = ColorSocket
_SOCKET_LINKER_REGISTRY["NodeSocketInt"] = IntegerSocket
_SOCKET_LINKER_REGISTRY["NodeSocketBool"] = BooleanSocket
_SOCKET_LINKER_REGISTRY["NodeSocketRotation"] = RotationSocket
_SOCKET_LINKER_REGISTRY["NodeSocketMatrix"] = MatrixSocket
_SOCKET_LINKER_REGISTRY["NodeSocketString"] = StringSocket
_SOCKET_LINKER_REGISTRY["NodeSocketMenu"] = MenuSocket
_SOCKET_LINKER_REGISTRY["NodeSocketGeometry"] = GeometrySocket
_SOCKET_LINKER_REGISTRY["NodeSocketObject"] = ObjectSocket
_SOCKET_LINKER_REGISTRY["NodeSocketMaterial"] = MaterialSocket
_SOCKET_LINKER_REGISTRY["NodeSocketImage"] = ImageSocket
_SOCKET_LINKER_REGISTRY["NodeSocketCollection"] = CollectionSocket
_SOCKET_LINKER_REGISTRY["NodeSocketBundle"] = BundleSocket
_SOCKET_LINKER_REGISTRY["NodeSocketClosure"] = ClosureSocket
_SOCKET_LINKER_REGISTRY["NodeSocketShader"] = ShaderSocket
