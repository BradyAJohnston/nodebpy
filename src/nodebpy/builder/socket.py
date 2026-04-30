from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator, cast, overload

import bpy
from bpy.types import (
    GeometryNodeTree,
    Node,
    NodeLink,
    NodeSocket,
    NodeSocketBool,
    NodeSocketBundle,
    NodeSocketClosure,
    NodeSocketCollection,
    NodeSocketColor,
    NodeSocketFloat,
    NodeSocketFont,
    NodeSocketGeometry,
    NodeSocketImage,
    NodeSocketInt,
    NodeSocketMaterial,
    NodeSocketMatrix,
    NodeSocketMenu,
    NodeSocketObject,
    NodeSocketRotation,
    NodeSocketShader,
    NodeSocketString,
    NodeSocketVector,
    NodeTree,
)
from mathutils import Euler

from ..types import (
    SOCKET_TYPES,
    InputBoolean,
    InputBundle,
    InputClosure,
    InputCollection,
    InputColor,
    InputFloat,
    InputFont,
    InputGeometry,
    InputImage,
    InputInteger,
    InputMaterial,
    InputMatrix,
    InputMenu,
    InputObject,
    InputRotation,
    InputString,
    InputVector,
)
from ._registry import _SOCKET_LINKER_REGISTRY, _get_socket_linker
from ._utils import _NodeLike, _SocketLike
from .mixins import LinkingMixin, OperatorMixin

if TYPE_CHECKING:
    from ..nodes.geometry import (
        IntegerMath,
        Math,
        MultiplyMatrices,
        Switch,
        TransformPoint,
    )
    from ..nodes.geometry.manual import Compare
    from ..nodes.geometry.vector import VectorMath
    from .node import BaseNode
    from .tree import TreeBuilder


class BaseSocket:
    def __init__(self, socket: NodeSocket):
        assert socket.node is not None
        self._tree = None
        self.socket = socket
        self.interface_socket: bpy.types.NodeTreeInterfaceSocket | None = None

    @property
    def node(self) -> Node:
        assert self.socket.node is not None
        return self.socket.node

    @property
    def links(self) -> list[NodeLink]:
        assert self.socket.links is not None
        return [link for link in self.socket.links]

    @property
    def _default_output_socket(self) -> NodeSocket:
        return self.socket

    @property
    def _default_input_socket(self) -> NodeSocket:
        return self.socket

    @property
    def type(self) -> SOCKET_TYPES:
        return self.socket.type  # type: ignore

    @property
    def socket_name(self) -> str:
        return self.socket.name

    @property
    def name(self) -> str:
        return str(self.socket.name)

    @property
    def _is_geometry_tree(self) -> bool:
        return self.tree.tree.bl_idname == "GeometryNodeTree"

    @property
    def tree(self) -> TreeBuilder:
        if self._tree is None:
            from .tree import TreeBuilder

            self._tree = TreeBuilder(cast(NodeTree, self.node.id_data))

        return self._tree


class Socket(BaseSocket, _SocketLike, OperatorMixin, LinkingMixin):
    """Wraps a single Blender NodeSocket, providing operator overloads and linking.

    Returned by ``SocketAccessor.get()`` / ``node.inputs[...]`` / ``node.outputs[...]``.
    Type-specific subclasses (``VectorSocket``, ``ColorSocket``, ``IntegerSocket``)
    are selected automatically via the registry.

    Properties:
    ----------
    tree : TreeBuilder
        The tree this socket belongs to.
    socket : NodeSocket
        The underlying Blender NodeSocket.

    """

    # -- Dispatch methods: per-type math logic. --
    # Called by OperatorMixin operators via _get_socket_linker().
    # Subclasses (and type-specific mixins) override to provide type-specific behaviour.

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "Math":
        """Scalar math dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        math_operation = "floored_modulo" if operation == "modulo" else operation
        return getattr(Math, math_operation)(*values)

    def _dispatch_unary(self, operation: str) -> "Math":
        """Scalar unary dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        if operation == "negate":
            return Math.multiply(self.socket, -1)
        elif operation == "absolute":
            return Math.absolute(self.socket)
        raise ValueError(f"Unknown unary operation: {operation}")

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "Math":
        """Scalar floor division: divide then floor."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        divided = Math.divide(*values)
        return Math.floor(divided)

    def _dispatch_compare(self, other: Any, operation: str) -> "Compare | Math":
        """Scalar comparison dispatch."""
        if isinstance(self.tree.tree, GeometryNodeTree):
            from ..nodes.geometry.manual import Compare

            return getattr(Compare.float, operation)(self.socket, other)
        else:
            from ..nodes.geometry.converter import Math

            _MATH_COMPARE_MAP = {
                "less_than": ("less_than", False),
                "greater_than": ("greater_than", False),
                "less_equal": ("greater_than", True),
                "greater_equal": ("less_than", True),
                "equal": ("compare", False),
            }
            math_op, negate = _MATH_COMPARE_MAP[operation]
            result = getattr(Math, math_op)(self.socket, other)
            if operation == "equal":
                result.i.value_002.default_value = 0.00001
            if negate:
                result = Math.subtract(1.0, result._default_output_socket)
            return result

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "Math": ...
        def __radd__(self, other: Any) -> "Math": ...
        def __sub__(self, other: Any) -> "Math": ...
        def __rsub__(self, other: Any) -> "Math": ...
        def __mul__(self, other: Any) -> "Math": ...
        def __rmul__(self, other: Any) -> "Math": ...
        def __div__(self, other: Any) -> "Math": ...
        def __rdiv__(self, other: Any) -> "Math": ...
        def __truediv__(self, other: Any) -> "Math": ...
        def __rtruediv__(self, other: Any) -> "Math": ...
        def __floordiv__(self, other: Any) -> "Math": ...
        def __rfloordiv__(self, other: Any) -> "Math": ...
        def __neg__(self) -> "Math": ...
        def __abs__(self) -> "Math": ...
        def __lt__(self, other: Any) -> "Compare": ...
        def __gt__(self, other: Any) -> "Compare": ...
        def __le__(self, other: Any) -> "Compare": ...
        def __ge__(self, other: Any) -> "Compare": ...
        def __eq__(self, other: Any) -> "Compare": ...
        def __ne__(self, other: Any) -> "Compare": ...


# ---------------------------------------------------------------------------
# Type-specific behaviour mixins
# ---------------------------------------------------------------------------


class _VectorMixin(BaseSocket):
    """Vector-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocketVector
    _tree: TreeBuilder

    @property
    def x(self) -> Socket:
        from ..nodes.geometry import SeparateXYZ

        return SeparateXYZ._find_or_create_linked(self.socket).o.x

    @property
    def y(self) -> Socket:
        from ..nodes.geometry import SeparateXYZ

        return SeparateXYZ._find_or_create_linked(self.socket).o.y

    @property
    def z(self) -> Socket:
        from ..nodes.geometry import SeparateXYZ

        return SeparateXYZ._find_or_create_linked(self.socket).o.z

    @property
    def default_value(self) -> list[float]:
        return list(self.socket.default_value)

    @default_value.setter
    def default_value(self, value: list[float] | tuple[float, float, float]) -> None:
        self.socket.default_value = value

    @overload
    def __getitem__(self, key: slice) -> "list[Socket]": ...
    @overload
    def __getitem__(self, key: int) -> "Socket": ...
    def __getitem__(self, key: int | slice) -> "Socket | list[Socket]":
        from ..nodes.geometry import CombineXYZ, SeparateXYZ

        if self.socket.is_output:
            return SeparateXYZ._find_or_create_linked(self.socket).o[key]
        else:
            return CombineXYZ._find_or_create_linked(self.socket).i[key]

    def __iter__(self) -> Iterator["Socket"]:
        from ..nodes.geometry import CombineXYZ, SeparateXYZ

        if self.socket.is_output:
            node = SeparateXYZ._find_or_create_linked(self.socket)
            yield node.o.x
            yield node.o.y
            yield node.o.z
        else:
            node = CombineXYZ._find_or_create_linked(self.socket)
            yield node.i.x
            yield node.i.y
            yield node.i.z

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
        if self._is_geometry_tree:
            from ..nodes.geometry.manual import Compare

            return getattr(Compare.vector, operation)(self.socket, other)
        else:
            return Socket._dispatch_compare(cast("Socket", self), other, operation)

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "VectorMath": ...
        def __radd__(self, other: Any) -> "VectorMath": ...
        def __sub__(self, other: Any) -> "VectorMath": ...
        def __rsub__(self, other: Any) -> "VectorMath": ...
        def __mul__(self, other: Any) -> "VectorMath": ...
        def __rmul__(self, other: Any) -> "VectorMath": ...
        def __truediv__(self, other: Any) -> "VectorMath": ...
        def __rtruediv__(self, other: Any) -> "VectorMath": ...
        def __floordiv__(self, other: Any) -> "VectorMath": ...
        def __rfloordiv__(self, other: Any) -> "VectorMath": ...
        def __neg__(self) -> "VectorMath": ...
        def __abs__(self) -> "VectorMath": ...
        def __lt__(self, other: Any) -> "Compare[NodeSocketVector]": ...
        def __gt__(self, other: Any) -> "Compare[NodeSocketVector]": ...
        def __le__(self, other: Any) -> "Compare[NodeSocketVector]": ...
        def __ge__(self, other: Any) -> "Compare[NodeSocketVector]": ...


_SEPARATE_COLOR_IDNAMES = (
    "FunctionNodeSeparateColor",
    "ShaderNodeSeparateColor",
    "CompositorNodeSeparateColor",
)


class _ColorMixin(BaseSocket):
    """Color-specific properties (.r, .g, .b, .a)."""

    socket: NodeSocketColor

    def _separated_channel(self, channel: str) -> Socket:
        assert self.socket.links is not None
        tree_type = self.tree.tree.bl_idname

        for link in self.socket.links:
            assert link.to_node is not None
            if link.to_node.bl_idname in _SEPARATE_COLOR_IDNAMES:
                return Socket(link.to_node.outputs[channel])

        if tree_type == "ShaderNodeTree":
            from ..nodes.shader.converter import SeparateColor

            sep = SeparateColor(self.socket)
        elif tree_type == "CompositorNodeTree":
            from ..nodes.compositor.converter import SeparateColor

            sep = SeparateColor(self.socket)
        else:
            from ..nodes.geometry.converter import SeparateColor

            sep = SeparateColor(self.socket)

        return sep.o[channel.lower()]

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

    @property
    def default_value(self) -> list[float]:
        return list(self.socket.default_value)

    @default_value.setter
    def default_value(self, value: list[float]) -> None:
        self.socket.default_value = value

    _COMBINE_COLOR_IDNAMES = (
        "FunctionNodeCombineColor",
        "ShaderNodeCombineColor",
        "CompositorNodeCombineColor",
    )

    def _get_or_create_combine_color(self) -> "Node":
        if self.socket.links:
            for link in self.socket.links:
                assert link.from_node
                if link.from_node.bl_idname in self._COMBINE_COLOR_IDNAMES:
                    return link.from_node

        if self.tree.tree.bl_idname == "CompositorNodeTree":
            from ..nodes.compositor import CombineColor

            combine = CombineColor()
        elif self.tree.tree.bl_idname == "ShaderNodeTree":
            from ..nodes.shader import CombineColor

            combine = CombineColor()
        else:
            from ..nodes.geometry import CombineColor

            combine = CombineColor()
        self.tree.link(combine.node.outputs[0], self.socket)
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
            ) in ("VALUE", "FLOAT", "INT"):
                return VectorMath.scale(self.socket, other._default_output_socket)
            else:
                return VectorMath.multiply(*values)
        else:
            vector_method = getattr(VectorMath, operation, None)
            assert vector_method is not None
            if isinstance(other, (int, float)):
                scalar_vector = (other, other, other)
                return (
                    vector_method(self.socket, scalar_vector)
                    if not reverse
                    else vector_method(scalar_vector, self.socket)
                )
            return vector_method(*values)


class _IntegerMixin(BaseSocket):
    """Integer-specific dispatch — uses IntegerMath in geometry trees."""

    socket: NodeSocketInt
    tree: TreeBuilder
    _tree: TreeBuilder

    @property
    def default_value(self) -> int:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: int) -> None:
        self.socket.default_value = value

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
        return Socket._dispatch_math(cast("Socket", self), other, operation, reverse)

    def _dispatch_unary(self, operation: str) -> "BaseNode":
        if self._is_geometry_tree:
            from ..nodes.geometry.converter import IntegerMath

            if operation == "negate":
                return IntegerMath.negate(self.socket)
            elif operation == "absolute":
                return IntegerMath.absolute(self.socket)
        return Socket._dispatch_unary(cast("Socket", self), operation)

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "BaseNode":
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return IntegerMath.divide_floor(*values)
        return Socket._dispatch_floordiv(cast("Socket", self), other, reverse)

    def _dispatch_compare(self, other: Any, operation: str) -> "Compare | Math":
        if self._is_geometry_tree:
            from ..nodes.geometry.manual import Compare

            return getattr(Compare.integer, operation)(self.socket, other)
        return Socket._dispatch_compare(cast("Socket", self), other, operation)

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "IntegerMath": ...
        def __radd__(self, other: Any) -> "IntegerMath": ...
        def __sub__(self, other: Any) -> "IntegerMath": ...
        def __rsub__(self, other: Any) -> "IntegerMath": ...
        def __mul__(self, other: Any) -> "IntegerMath": ...
        def __rmul__(self, other: Any) -> "IntegerMath": ...
        def __truediv__(self, other: Any) -> "IntegerMath": ...
        def __rtruediv__(self, other: Any) -> "IntegerMath": ...
        def __floordiv__(self, other: Any) -> "IntegerMath": ...
        def __rfloordiv__(self, other: Any) -> "IntegerMath": ...
        def __neg__(self) -> "IntegerMath": ...
        def __abs__(self) -> "IntegerMath": ...
        def __lt__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __gt__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __le__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __ge__(self, other: Any) -> "Compare[NodeSocketInt]": ...


# ---------------------------------------------------------------------------
# Type-specific behaviour mixins (continued)
# ---------------------------------------------------------------------------


class _BooleanSwitchSocketFactory:
    def __init__(self, socket: NodeSocketBool):
        self._socket = socket
        from ..nodes.geometry import Switch

        self._switch = Switch

    def float(
        self, false: InputFloat = None, true: InputFloat = None
    ) -> "Switch[FloatSocket]":
        return self._switch.float(self._socket, false, true)

    def integer(
        self, false: InputInteger = None, true: InputInteger = None
    ) -> "Switch[IntegerSocket]":
        return self._switch.integer(self._socket, false, true)

    def boolean(
        self, false: InputBoolean = None, true: InputBoolean = None
    ) -> "Switch[BooleanSocket]":
        return self._switch.boolean(self._socket, false, true)

    def vector(
        self, false: InputVector = None, true: InputVector = None
    ) -> "Switch[VectorSocket]":
        return self._switch.vector(self._socket, false, true)

    def color(
        self, false: InputColor = None, true: InputColor = None
    ) -> "Switch[ColorSocket]":
        return self._switch.color(self._socket, false, true)

    def rotation(
        self, false: InputRotation = None, true: InputRotation = None
    ) -> "Switch[RotationSocket]":
        return self._switch.rotation(self._socket, false, true)

    def matrix(
        self, false: InputMatrix = None, true: InputMatrix = None
    ) -> "Switch[MatrixSocket]":
        return self._switch.matrix(self._socket, false, true)

    def string(
        self, false: InputString = None, true: InputString = None
    ) -> "Switch[StringSocket]":
        return self._switch.string(self._socket, false, true)

    def menu(
        self, false: InputMenu = None, true: InputMenu = None
    ) -> "Switch[MenuSocket]":
        return self._switch.menu(self._socket, false, true)

    def object(
        self, false: InputObject = None, true: InputObject = None
    ) -> "Switch[ObjectSocket]":
        return self._switch.object(self._socket, false, true)

    def image(
        self, false: InputImage = None, true: InputImage = None
    ) -> "Switch[ImageSocket]":
        return self._switch.image(self._socket, false, true)

    def geometry(
        self, false: InputGeometry = None, true: InputGeometry = None
    ) -> "Switch[GeometrySocket]":
        return self._switch.geometry(self._socket, false, true)

    def collection(
        self, false: InputCollection = None, true: InputCollection = None
    ) -> "Switch[CollectionSocket]":
        return self._switch.collection(self._socket, false, true)

    def material(
        self, false: InputMaterial = None, true: InputMaterial = None
    ) -> "Switch[MaterialSocket]":
        return self._switch.material(self._socket, false, true)

    def bundle(
        self, false: InputBundle = None, true: InputBundle = None
    ) -> "Switch[BundleSocket]":
        return self._switch.bundle(self._socket, false, true)

    def closure(
        self, false: InputClosure = None, true: InputClosure = None
    ) -> "Switch[ClosureSocket]":
        return self._switch.closure(self._socket, false, true)

    def font(
        self, false: InputFont = None, true: InputFont = None
    ) -> "Switch[FontSocket]":
        return self._switch.font(self._socket, false, true)


class _BooleanMixin(BaseSocket):
    """Boolean-specific operator overrides — routes directly through BooleanMath."""

    socket: NodeSocketBool

    @property
    def default_value(self) -> bool:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bool) -> None:
        self.socket.default_value = value

    def __or__(self, other: Any) -> "BaseNode":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(self.socket, other)

    def __and__(self, other: Any) -> "BaseNode":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(self.socket, other)

    @property
    def switch(self) -> "_BooleanSwitchSocketFactory":
        "Creat a Switch node with this boolean as the `switch` input."

        return _BooleanSwitchSocketFactory(self.socket)


class _RotationMixin(BaseSocket):
    """Rotation-specific properties (.w, .x, .y, .z) via RotationToQuaternion."""

    socket: NodeSocketRotation

    @property
    def default_value(self) -> Euler:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: Euler) -> None:
        self.socket.default_value = value

    @property
    def w(self) -> FloatSocket:
        from ..nodes.geometry import RotationToQuaternion

        return RotationToQuaternion._find_or_create_linked(self.socket).o.w

    @property
    def x(self) -> FloatSocket:
        from ..nodes.geometry import RotationToQuaternion

        return RotationToQuaternion._find_or_create_linked(self.socket).o.x

    @property
    def y(self) -> FloatSocket:
        from ..nodes.geometry import RotationToQuaternion

        return RotationToQuaternion._find_or_create_linked(self.socket).o.y

    @property
    def z(self) -> FloatSocket:
        from ..nodes.geometry import RotationToQuaternion

        return RotationToQuaternion._find_or_create_linked(self.socket).o.z

    @property
    def euler(self) -> "VectorSocket":
        from ..nodes.geometry.converter import RotationToEuler

        return RotationToEuler._find_or_create_linked(self.socket).o.euler

    @property
    def invert(self) -> "RotationSocket":
        from ..nodes.geometry import InvertRotation

        return InvertRotation._find_or_create_linked(self.socket).o.rotation


class _FloatMixin(BaseSocket):
    """Float-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocketFloat

    @property
    def default_value(self) -> float:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: float) -> None:
        self.socket.default_value = value


class _MatrixMixin(BaseSocket):
    """Matrix-specific properties (.translation, .rotation, .scale) via SeparateTransform."""

    socket: NodeSocketMatrix

    @property
    def translation(self) -> "VectorSocket":
        from ..nodes.geometry import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.translation

    @property
    def rotation(self) -> "RotationSocket":
        from ..nodes.geometry import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.rotation

    @property
    def scale(self) -> "VectorSocket":
        from ..nodes.geometry import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.scale

    @property
    def determinant(self) -> "FloatSocket":
        from ..nodes.geometry import MatrixDeterminant

        return MatrixDeterminant._find_or_create_linked(self.socket).o.determinant

    @property
    def invert(self) -> "MatrixSocket":
        from ..nodes.geometry import InvertMatrix

        return InvertMatrix._find_or_create_linked(self.socket).o.matrix

    @property
    def transpose(self) -> "MatrixSocket":
        from ..nodes.geometry import TransposeMatrix

        return TransposeMatrix._find_or_create_linked(self.socket).o.matrix

    @overload
    def __getitem__(self, key: slice) -> "list[Socket]": ...
    @overload
    def __getitem__(self, key: int) -> "Socket": ...
    def __getitem__(self, key: int | slice) -> "Socket | list[Socket]":
        from ..nodes.geometry import CombineMatrix, SeparateMatrix

        if self.socket.is_output:
            node = SeparateMatrix._find_or_create_linked(self.socket)
            if isinstance(key, slice):
                return [node.o[i] for i in range(*key.indices(len(node.o)))]
            return node.o[key]
        node = CombineMatrix._find_or_create_linked(self.socket)
        if isinstance(key, slice):
            return [node.i[i] for i in range(*key.indices(len(node.i)))]
        return node.i[key]

    def __iter__(self) -> Iterator["Socket"]:
        from ..nodes.geometry import CombineMatrix, SeparateMatrix

        if self.socket.is_output:
            node = SeparateMatrix._find_or_create_linked(self.socket)
            return iter(node.o)
        else:
            node = CombineMatrix._find_or_create_linked(self.socket)
            return iter(node.i)

    def __len__(self) -> int:
        return 16

    if TYPE_CHECKING:

        @overload
        def __matmul__(
            self, other: "VectorSocket | NodeSocketVector"
        ) -> "TransformPoint": ...
        @overload
        def __matmul__(self, other: Any) -> "MultiplyMatrices": ...

        def __rmatmul__(self, other: Any) -> "MultiplyMatrices": ...


# ---------------------------------------------------------------------------
# Registry-target socket classes
# Used by _get_socket_linker() for runtime socket wrapping.
# The corresponding SocketVector / SocketColor / etc. in interface.py
# inherit the same mixins and gain identical behaviour for interface sockets.
# ---------------------------------------------------------------------------


class FloatSocket(_FloatMixin, Socket):
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

    socket: NodeSocketString

    @property
    def default_value(self) -> str:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self.socket.default_value = value


class MenuSocket(Socket):
    """Runtime menu socket wrapper."""

    socket: NodeSocketMenu

    @property
    def default_value(self) -> str:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self.socket.default_value = value


class GeometrySocket(Socket):
    """Runtime geometry socket wrapper."""

    socket: NodeSocketGeometry


class ObjectSocket(Socket):
    """Runtime object socket wrapper."""

    socket: NodeSocketObject

    @property
    def default_value(self) -> bpy.types.Object | None:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bpy.types.Object) -> None:
        self.socket.default_value = value


class MaterialSocket(Socket):
    """Runtime material socket wrapper."""

    socket: NodeSocketMaterial

    @property
    def default_value(self) -> bpy.types.Material | None:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bpy.types.Material) -> None:
        self.socket.default_value = value


class ImageSocket(Socket):
    """Runtime image socket wrapper."""

    socket: NodeSocketImage

    @property
    def default_value(self) -> bpy.types.Image | None:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bpy.types.Image) -> None:
        self.socket.default_value = value


class CollectionSocket(Socket):
    """Runtime collection socket wrapper."""

    socket: NodeSocketCollection

    @property
    def default_value(self) -> bpy.types.Collection | None:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bpy.types.Collection) -> None:
        self.socket.default_value = value


class BundleSocket(Socket):
    """Runtime bundle socket wrapper."""

    socket: NodeSocketBundle


class ClosureSocket(Socket):
    """Runtime closure socket wrapper."""

    socket: NodeSocketClosure


class ShaderSocket(Socket):
    """Runtime shader socket wrapper."""

    socket: NodeSocketShader


class FontSocket(Socket):
    """Runtime font socket wrapper."""

    socket: NodeSocketFont


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
_SOCKET_LINKER_REGISTRY["NodeSocketFont"] = FontSocket
_SOCKET_LINKER_REGISTRY["NodeSocketCollection"] = CollectionSocket
_SOCKET_LINKER_REGISTRY["NodeSocketBundle"] = BundleSocket
_SOCKET_LINKER_REGISTRY["NodeSocketClosure"] = ClosureSocket
_SOCKET_LINKER_REGISTRY["NodeSocketShader"] = ShaderSocket
