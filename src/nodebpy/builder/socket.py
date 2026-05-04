from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Iterator,
    Mapping,
    cast,
    overload,
)

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
from ._registry import _SOCKET_LINKER_REGISTRY
from ._utils import _NodeLike, _SocketLike
from .mixins import LinkingMixin, OperatorMixin

if TYPE_CHECKING:
    from ..nodes import compositor, geometry, shader
    from ..nodes.geometry import (
        IntegerMath,
        MatchString,
        Math,
        MultiplyMatrices,
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
        self._interface_socket: bpy.types.NodeTreeInterfaceSocket | None = None
        self._builder_node: BaseNode | None = None

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
    def name(self) -> str:
        return str(self.socket.name)

    @property
    def _is_geometry_tree(self) -> bool:
        return self.tree.tree.bl_idname == "GeometryNodeTree"

    @property
    def _is_shader_tree(self) -> bool:
        return self.tree.tree.bl_idname == "ShaderNodeTree"

    @property
    def _is_compositor_tree(self) -> bool:
        return self.tree.tree.bl_idname == "CompositorNodeTree"

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

    @property
    def builder_node(self) -> "BaseNode | None":
        """The builder node that owns this socket, if accessed via .o/.i."""
        return self._builder_node

    # -- Dispatch methods: per-type math logic. --
    # Called by OperatorMixin operators via _get_socket_linker().
    # Subclasses (and type-specific mixins) override to provide type-specific behaviour.

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "FloatSocket":
        """Scalar math dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        math_operation = "floored_modulo" if operation == "modulo" else operation
        return getattr(Math, math_operation)(*values).o.value

    def _dispatch_unary(self, operation: str) -> "FloatSocket":
        """Scalar unary dispatch (float). Uses the Math node."""
        from ..nodes.geometry.converter import Math

        if operation == "negate":
            return Math.multiply(self.socket, -1).o.value
        elif operation == "absolute":
            return Math.absolute(self.socket).o.value
        raise ValueError(f"Unknown unary operation: {operation}")

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "FloatSocket":
        """Scalar floor division: divide then floor."""
        from ..nodes.geometry.converter import Math

        values = (self.socket, other) if not reverse else (other, self.socket)
        divided = Math.divide(*values)
        return Math.floor(divided).o.value

    def _dispatch_compare(
        self, other: Any, operation: str
    ) -> "FloatSocket | BooleanSocket":
        """Scalar comparison dispatch."""
        if isinstance(self.tree.tree, GeometryNodeTree):
            from ..nodes.geometry.manual import Compare

            return cast(
                Compare, getattr(Compare.float, operation)(self.socket, other)
            ).o.result
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
            result = getattr(Math, math_op)(self.socket, other).o.value
            if operation == "equal":
                result.builder_node.i.value_002.default_value = 0.00001
            if negate:
                result = Math.subtract(1.0, result._default_output_socket).o.value
            return result

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "FloatSocket": ...
        def __radd__(self, other: Any) -> "FloatSocket": ...
        def __sub__(self, other: Any) -> "FloatSocket": ...
        def __rsub__(self, other: Any) -> "FloatSocket": ...
        def __mul__(self, other: Any) -> "FloatSocket": ...
        def __rmul__(self, other: Any) -> "FloatSocket": ...
        def __div__(self, other: Any) -> "FloatSocket": ...
        def __rdiv__(self, other: Any) -> "FloatSocket": ...
        def __truediv__(self, other: Any) -> "FloatSocket": ...
        def __rtruediv__(self, other: Any) -> "FloatSocket": ...
        def __floordiv__(self, other: Any) -> "FloatSocket": ...
        def __rfloordiv__(self, other: Any) -> "FloatSocket": ...
        def __neg__(self) -> "FloatSocket": ...
        def __abs__(self) -> "FloatSocket": ...
        def __lt__(self, other: Any) -> "BooleanSocket": ...
        def __gt__(self, other: Any) -> "BooleanSocket": ...
        def __le__(self, other: Any) -> "BooleanSocket": ...
        def __ge__(self, other: Any) -> "BooleanSocket": ...
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
    def _vmath(self) -> "type[VectorMath]":
        from ..nodes.geometry import VectorMath

        return VectorMath

    @property
    def _separate(self) -> "geometry.SeparateXYZ":
        from ..nodes.geometry import SeparateXYZ

        return SeparateXYZ._find_or_create_linked(self.socket)

    @property
    def x(self) -> FloatSocket:
        return self._separate.o.x

    @property
    def y(self) -> FloatSocket:
        return self._separate.o.y

    @property
    def z(self) -> FloatSocket:
        return self._separate.o.z

    def dot(self, vector: InputVector) -> "FloatSocket":
        """Dot product with another vector. The other vector can be a Socket, a NodeSocket, or a 3-tuple of floats.

        A different VectorMath node is created each time.
        """
        return self._vmath.dot_product(self.socket, vector).o.value

    def scale(self, scale: InputFloat) -> "VectorSocket":
        """Scale this vector by a scalar value and return VectorSocket"""
        return self._vmath.scale(self.socket, scale).o.vector

    def length(self) -> "FloatSocket":
        return self._vmath.length(self.socket).o.value

    def normalize(self) -> "VectorSocket":
        """Normalize this vector. Only valid for output sockets, as it creates a Normalize node linked from this socket.

        The same normalize node is re-used each time unless `new_node=True` where a new `VectorMath` node is created each time.
        """
        return self._vmath.normalize(self.socket).o.vector

    @property
    def default_value(self) -> list[float]:
        return list(self.socket.default_value)

    @default_value.setter
    def default_value(self, value: list[float] | tuple[float, float, float]) -> None:
        self.socket.default_value = value

    @overload
    def __getitem__(self, key: slice) -> "list[FloatSocket]": ...
    @overload
    def __getitem__(self, key: int) -> "FloatSocket": ...
    def __getitem__(self, key: int | slice) -> "FloatSocket | list[FloatSocket]":
        from ..nodes.geometry import CombineXYZ, SeparateXYZ

        if self.socket.is_output:
            node = SeparateXYZ._find_or_create_linked(self.socket)
            return [node.o.x, node.o.y, node.o.z][key]

        else:
            node = CombineXYZ._find_or_create_linked(self.socket)
            return [node.i.x, node.i.y, node.i.z][key]

    def __iter__(self) -> Iterator["FloatSocket"]:
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

    def _dispatch_unary(self, operation: str) -> "VectorSocket":
        from ..nodes.geometry import VectorMath

        if operation == "negate":
            return VectorMath.scale(self.socket, -1).o.vector
        elif operation == "absolute":
            return VectorMath.absolute(self.socket).o.vector
        raise ValueError(f"Unknown unary operation: {operation}")

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "VectorSocket":
        from ..nodes.geometry import VectorMath

        values = (self.socket, other) if not reverse else (other, self.socket)

        if operation == "multiply":
            if isinstance(other, (int, float)):
                return VectorMath.scale(self.socket, other).o.vector
            elif isinstance(other, NodeSocket) and other.type in (
                "VALUE",
                "FLOAT",
                "INT",
            ):
                return VectorMath.scale(self.socket, other).o.vector
            elif isinstance(other, (_SocketLike, _NodeLike)) and getattr(
                other, "type", None
            ) in (
                "VALUE",
                "FLOAT",
                "INT",
            ):
                return VectorMath.scale(
                    self.socket, other._default_output_socket
                ).o.vector
            elif isinstance(other, (list, tuple)) and len(other) == 3:
                return VectorMath.multiply(*values).o.vector
            elif isinstance(other, (_SocketLike, _NodeLike, NodeSocket)):
                return VectorMath.multiply(*values).o.vector
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
                ).o.vector
            elif (isinstance(other, (list, tuple)) and len(other) == 3) or isinstance(
                other, (_SocketLike, _NodeLike, NodeSocket)
            ):
                return vector_method(*values).o.vector
            else:
                raise TypeError(
                    f"Unsupported type for {operation} with VECTOR operand: {type(other)}"
                )

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "VectorSocket":
        from ..nodes.geometry import VectorMath

        divided = self._dispatch_math(other, "divide", reverse=reverse)
        return VectorMath.floor(divided).o.vector

    def _dispatch_compare(
        self, other: Any, operation: str
    ) -> "BooleanSocket | FloatSocket":
        if self._is_geometry_tree:
            from ..nodes.geometry import Compare

            return getattr(Compare.vector, operation)(self.socket, other).o.result
        else:
            return Socket._dispatch_compare(cast("Socket", self), other, operation)

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "VectorSocket": ...
        def __radd__(self, other: Any) -> "VectorSocket": ...
        def __sub__(self, other: Any) -> "VectorSocket": ...
        def __rsub__(self, other: Any) -> "VectorSocket": ...
        def __mul__(self, other: Any) -> "VectorSocket": ...
        def __rmul__(self, other: Any) -> "VectorSocket": ...
        def __truediv__(self, other: Any) -> "VectorSocket": ...
        def __rtruediv__(self, other: Any) -> "VectorSocket": ...
        def __floordiv__(self, other: Any) -> "VectorSocket": ...
        def __rfloordiv__(self, other: Any) -> "VectorSocket": ...
        def __neg__(self) -> "VectorSocket": ...
        def __abs__(self) -> "VectorSocket": ...
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

    def _separated_channel(
        self,
    ) -> "geometry.SeparateColor | shader.SeparateColor | compositor.SeparateColor":
        assert self.socket.links is not None
        tree_type = self.tree.tree.bl_idname

        if tree_type == "ShaderNodeTree":
            from ..nodes.shader import SeparateColor

            sep = SeparateColor._find_or_create_linked(self.socket)
        elif tree_type == "CompositorNodeTree":
            from ..nodes.compositor import SeparateColor

            sep = SeparateColor._find_or_create_linked(self.socket)
        else:
            from ..nodes.geometry import SeparateColor

            sep = SeparateColor._find_or_create_linked(self.socket)

        return sep

    def _combine_color(
        self,
    ) -> "shader.CombineColor | compositor.CombineColor | geometry.CombineColor":
        if self.tree.tree.bl_idname == "CompositorNodeTree":
            from ..nodes.compositor import CombineColor

            combine = CombineColor._find_or_create_linked(self.socket)
        elif self.tree.tree.bl_idname == "ShaderNodeTree":
            from ..nodes.shader import CombineColor

            combine = CombineColor._find_or_create_linked(self.socket)
        else:
            from ..nodes.geometry import CombineColor

            combine = CombineColor._find_or_create_linked(self.socket)
        self.tree.link(combine.node.outputs[0], self.socket)
        return combine

    @property
    def r(self) -> FloatSocket:
        if self.socket.is_output:
            return self._separated_channel().o.red
        else:
            return self._combine_color().i.red

    @property
    def g(self) -> FloatSocket:
        if self.socket.is_output:
            return self._separated_channel().o.green
        else:
            return self._combine_color().i.green

    @property
    def b(self) -> FloatSocket:
        if self.socket.is_output:
            return self._separated_channel().o.blue
        else:
            return self._combine_color().i.blue

    @property
    def a(self) -> FloatSocket:
        from ..nodes import shader

        if self.socket.is_output:
            node = self._separated_channel()
            if isinstance(node, shader.SeparateColor):
                raise TypeError(
                    "Shader SeparateColor node doesn't have an alpha output"
                )

            return node.o.alpha
        else:
            node = self._combine_color()
            if isinstance(node, shader.CombineColor):
                raise TypeError("Shader CombineColor node doesn't have an alpha input")
            return node.i.alpha

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

    @overload
    def __getitem__(self, key: slice) -> "list[FloatSocket]": ...
    @overload
    def __getitem__(self, key: int) -> "FloatSocket": ...
    def __getitem__(self, key: int | slice) -> "FloatSocket | list[FloatSocket]":
        if self._is_shader_tree:
            return [self.r, self.g, self.b][key]
        else:
            return [self.r, self.g, self.b, self.a][key]

    def __iter__(self) -> Iterator["FloatSocket"]:
        yield self.r
        yield self.g
        yield self.b
        if not self._is_shader_tree:
            yield self.a

    def __len__(self) -> int:
        if self._is_shader_tree:
            return 3
        else:
            return 4

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "VectorSocket":
        from ..nodes.geometry import VectorMath

        values = (self.socket, other) if not reverse else (other, self.socket)

        if operation == "multiply":
            if isinstance(other, (int, float)):
                return VectorMath.scale(self.socket, other).o.vector
            elif isinstance(other, NodeSocket) and other.type in (
                "VALUE",
                "FLOAT",
                "INT",
            ):
                return VectorMath.scale(self.socket, other).o.vector
            elif isinstance(other, (_SocketLike, _NodeLike)) and getattr(
                other, "type", None
            ) in ("VALUE", "FLOAT", "INT"):
                return VectorMath.scale(
                    self.socket, other._default_output_socket
                ).o.vector
            else:
                return VectorMath.multiply(*values).o.vector
        else:
            vector_method = getattr(VectorMath, operation, None)
            assert vector_method is not None
            if isinstance(other, (int, float)):
                scalar_vector = (other, other, other)
                return (
                    vector_method(self.socket, scalar_vector)
                    if not reverse
                    else vector_method(scalar_vector, self.socket)
                ).o.vector
            return vector_method(*values).o.vector


class _BooleanSwitchSocketFactory:
    def __init__(self, socket: NodeSocketBool):
        self._socket = socket
        from ..nodes.geometry import Switch

        self._switch = Switch

    def float(self, false: InputFloat = None, true: InputFloat = None) -> "FloatSocket":
        return self._switch.float(self._socket, false, true).o.output

    def integer(
        self, false: InputInteger = None, true: InputInteger = None
    ) -> "IntegerSocket":
        return self._switch.integer(self._socket, false, true).o.output

    def boolean(
        self, false: InputBoolean = None, true: InputBoolean = None
    ) -> "BooleanSocket":
        return self._switch.boolean(self._socket, false, true).o.output

    def vector(
        self, false: InputVector = None, true: InputVector = None
    ) -> "VectorSocket":
        return self._switch.vector(self._socket, false, true).o.output

    def color(self, false: InputColor = None, true: InputColor = None) -> "ColorSocket":
        return self._switch.color(self._socket, false, true).o.output

    def rotation(
        self, false: InputRotation = None, true: InputRotation = None
    ) -> "RotationSocket":
        return self._switch.rotation(self._socket, false, true).o.output

    def matrix(
        self, false: InputMatrix = None, true: InputMatrix = None
    ) -> "MatrixSocket":
        return self._switch.matrix(self._socket, false, true).o.output

    def string(
        self, false: InputString = None, true: InputString = None
    ) -> "StringSocket":
        return self._switch.string(self._socket, false, true).o.output

    def menu(self, false: InputMenu = None, true: InputMenu = None) -> "MenuSocket":
        return self._switch.menu(self._socket, false, true).o.output

    def object(
        self, false: InputObject = None, true: InputObject = None
    ) -> "ObjectSocket":
        return self._switch.object(self._socket, false, true).o.output

    def image(self, false: InputImage = None, true: InputImage = None) -> "ImageSocket":
        return self._switch.image(self._socket, false, true).o.output

    def geometry(
        self, false: InputGeometry = None, true: InputGeometry = None
    ) -> "GeometrySocket":
        return self._switch.geometry(self._socket, false, true).o.output

    def collection(
        self, false: InputCollection = None, true: InputCollection = None
    ) -> "CollectionSocket":
        return self._switch.collection(self._socket, false, true).o.output

    def material(
        self, false: InputMaterial = None, true: InputMaterial = None
    ) -> "MaterialSocket":
        return self._switch.material(self._socket, false, true).o.output

    def bundle(
        self, false: InputBundle = None, true: InputBundle = None
    ) -> "BundleSocket":
        return self._switch.bundle(self._socket, false, true).o.output

    def closure(
        self, false: InputClosure = None, true: InputClosure = None
    ) -> "ClosureSocket":
        return self._switch.closure(self._socket, false, true).o.output

    def font(self, false: InputFont = None, true: InputFont = None) -> "FontSocket":
        return self._switch.font(self._socket, false, true).o.output


class _BooleanMixin(BaseSocket):
    """Boolean-specific operator overrides — routes directly through BooleanMath."""

    socket: NodeSocketBool

    @property
    def default_value(self) -> bool:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: bool) -> None:
        self.socket.default_value = value

    def __or__(self, other: Any) -> "BooleanSocket":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(self.socket, other).o.boolean

    def __and__(self, other: Any) -> "BooleanSocket":
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(self.socket, other).o.boolean

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
    def _quaternion(self) -> "geometry.RotationToQuaternion":
        from ..nodes.geometry import RotationToQuaternion

        return RotationToQuaternion._find_or_create_linked(self.socket)

    @property
    def w(self) -> FloatSocket:
        "Separate the rotation into a quaternion and return the `w` component"
        return self._quaternion.o.w

    @property
    def x(self) -> FloatSocket:
        "Separate the rotation into a quaternion and return the `x` component"
        return self._quaternion.o.x

    @property
    def y(self) -> FloatSocket:
        "Separate the rotation into a quaternion and return the `y` component"
        return self._quaternion.o.y

    @property
    def z(self) -> FloatSocket:
        "Separate the rotation into a quaternion and return the `z` component"
        return self._quaternion.o.z

    def euler(self) -> "VectorSocket":
        "Convert the rotation to an XYZ euler rotation and return `VectorSocket`."
        from ..nodes.geometry.converter import RotationToEuler

        return RotationToEuler._find_or_create_linked(self.socket).o.euler

    def invert(self) -> "RotationSocket":
        "Invert the rotation of the socket."
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

    @property
    def _math(self) -> "type[Math]":
        from ..nodes.geometry import Math

        return Math

    def sign(self) -> "FloatSocket":
        "Return the sign of the FloatSocket, eithe `-1`, `0` or `1`."
        return self._math.sign(self.socket).o.value

    def negate(self) -> "FloatSocket":
        "Negate the `FloatSocket` by multiplying the value by `-1`."
        return self._math.multiply(self.socket, -1).o.value

    def to_string(self, decimals: InputInteger = 0) -> "StringSocket":
        "Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places"
        from ..nodes.geometry import ValueToString

        return ValueToString.float(self.socket, decimals).o.string


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

    @property
    def _imath(self) -> "type[IntegerMath]":
        from ..nodes.geometry import IntegerMath

        return IntegerMath

    def to_string(self) -> "StringSocket":
        "Convert the `IntegerSocket` to a `StringSocket`."
        from ..nodes.geometry import ValueToString

        return ValueToString.integer(self.socket).o.string

    def sign(self) -> "IntegerSocket":
        "Return the sign of the IntegerSocket, either `-1`, `0`, or `1`."
        return self._imath.sign(self.socket).o.value

    def negate(self) -> "IntegerSocket":
        return self._imath.negate(self.socket).o.value

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
    ) -> "IntegerSocket | FloatSocket":
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return getattr(IntegerMath, operation)(*values).o.value
        return Socket._dispatch_math(cast("Socket", self), other, operation, reverse)

    def _dispatch_unary(self, operation: str) -> "IntegerSocket | FloatSocket":
        if self._is_geometry_tree:
            from ..nodes.geometry.converter import IntegerMath

            if operation == "negate":
                return IntegerMath.negate(self.socket).o.value
            elif operation == "absolute":
                return IntegerMath.absolute(self.socket).o.value
        return Socket._dispatch_unary(cast("Socket", self), operation)

    def _dispatch_floordiv(
        self, other: Any, reverse: bool = False
    ) -> "IntegerSocket | FloatSocket":
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return IntegerMath.divide_floor(*values).o.value
        return Socket._dispatch_floordiv(cast("Socket", self), other, reverse)

    def _dispatch_compare(
        self, other: Any, operation: str
    ) -> "BooleanSocket | FloatSocket":
        if self._is_geometry_tree:
            from ..nodes.geometry.manual import Compare

            return getattr(Compare.integer, operation)(self.socket, other).o.result
        return Socket._dispatch_compare(cast("Socket", self), other, operation)

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> "IntegerSocket": ...
        def __radd__(self, other: Any) -> "IntegerSocket": ...
        def __sub__(self, other: Any) -> "IntegerSocket": ...
        def __rsub__(self, other: Any) -> "IntegerSocket": ...
        def __mul__(self, other: Any) -> "IntegerSocket": ...
        def __rmul__(self, other: Any) -> "IntegerSocket": ...
        def __truediv__(self, other: Any) -> "IntegerSocket": ...
        def __rtruediv__(self, other: Any) -> "IntegerSocket": ...
        def __floordiv__(self, other: Any) -> "IntegerSocket": ...
        def __rfloordiv__(self, other: Any) -> "IntegerSocket": ...
        def __neg__(self) -> "IntegerSocket": ...
        def __abs__(self) -> "IntegerSocket": ...
        def __lt__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __gt__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __le__(self, other: Any) -> "Compare[NodeSocketInt]": ...
        def __ge__(self, other: Any) -> "Compare[NodeSocketInt]": ...


class _StringMixin(BaseSocket):
    """Float-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocketString

    @property
    def default_value(self) -> str:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self.socket.default_value = value

    @property
    def _match(self) -> "type[MatchString]":
        from ..nodes.geometry import MatchString

        return MatchString

    def starts_with(self, search: InputString) -> "BooleanSocket":
        "Create a MatchString[Starts With], return the result as a `BooleanSocket`."
        return self._match(self.socket, "Starts With", search).o.result

    def ends_with(self, search: InputString) -> "BooleanSocket":
        "Create a MatchString[Ends With], return the result as a `BooleanSocket`."
        return self._match(self.socket, "Ends With", search).o.result

    def contains(self, search: InputString) -> "BooleanSocket":
        "Create a MatchString[Contains], return the result as a `BooleanSocket`."
        return self._match(self.socket, "Contains", search).o.result

    def slice(
        self, position: InputInteger = 0, length: InputInteger = 0
    ) -> StringSocket:
        "Slice a given string from a starting position for a given length."
        from ..nodes.geometry import SliceString

        return SliceString(self.socket, position, length).o.string

    def format(
        self, items: Mapping[str, InputString | InputInteger | InputFloat]
    ) -> "StringSocket":
        "Format a given string with the key-value items."
        from ..nodes.geometry import FormatString

        return FormatString(self.socket, items).o.string

    def replace(self, find: InputString, replace: InputString) -> "StringSocket":
        "Replace every match of the string with teh replacement string"
        from ..nodes.geometry import ReplaceString

        return ReplaceString(self.socket, find, replace).o.string

    def length(self) -> "IntegerSocket":
        "Compute the length of a string and return as `IntegerSocket`."
        from ..nodes.geometry import StringLength

        return StringLength(self.socket).o.length

    def find(self, search: InputString) -> tuple["IntegerSocket", "IntegerSocket"]:
        """Find where in a string a pattern occurs.

        Returns a tuple(IntegerSocket, IntegerSocket), corresponding to (index_of_first_match, count_of_matches)."""
        from ..nodes.geometry import FindInString

        node = FindInString(self.socket, search)

        return (node.o.first_found, node.o.count)

    def join(
        self, strings: Iterable[str | "StringSocket" | NodeSocketString | BaseNode]
    ) -> "StringSocket":
        """Join the input strings with this as the separator."""
        from ..nodes.geometry import JoinStrings

        return JoinStrings(strings, self.socket).o.string

    def __add__(self, other: "StringSocket" | str) -> StringSocket:
        from ..nodes.geometry import JoinStrings, String

        if isinstance(other, str):
            other = String(other).o.string

        return JoinStrings((self.socket, other)).o.string

    def __radd__(self, other: str | "StringSocket") -> StringSocket:
        from ..nodes.geometry import JoinStrings, String

        if isinstance(other, str):
            other = String(other).o.string

        return JoinStrings((other, self.socket)).o.string


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

    def determinant(self) -> "FloatSocket":
        "Compute the determinant of a matrix input and return as a `FloatSocket`"
        from ..nodes.geometry import MatrixDeterminant

        return MatrixDeterminant._find_or_create_linked(self.socket).o.determinant

    def invert(self) -> "MatrixSocket":
        "Invert the `MatrixSocet` and return a `MatrixSocket`"
        from ..nodes.geometry import InvertMatrix

        return InvertMatrix._find_or_create_linked(self.socket).o.matrix

    def transpose(self) -> "MatrixSocket":
        "Transpose the `MatrixSocket` and return a `MatrixSocket`"
        from ..nodes.geometry import TransposeMatrix

        return TransposeMatrix._find_or_create_linked(self.socket).o.matrix

    def svd(self) -> tuple[MatrixSocket, VectorSocket, MatrixSocket]:
        "Compute the 'Single Value Decomposition' and return output sockets of the MatrixSVD node, `tuple[u, s, v]`"
        from ..nodes.geometry import MatrixSVD

        return tuple(MatrixSVD(self.socket).o)

    @overload
    def __getitem__(self, key: slice) -> "list[FloatSocket]": ...
    @overload
    def __getitem__(self, key: int) -> "FloatSocket": ...
    def __getitem__(self, key: int | slice) -> "FloatSocket | list[FloatSocket]":
        from ..nodes.geometry import CombineMatrix, SeparateMatrix

        if self.socket.is_output:
            node = SeparateMatrix._find_or_create_linked(self.socket)
            if isinstance(key, slice):
                return [
                    cast(FloatSocket, node.o[i])
                    for i in range(*key.indices(len(node.o)))
                ]
            return cast(FloatSocket, node.o[key])
        else:
            node = CombineMatrix._find_or_create_linked(self.socket)
            if isinstance(key, slice):
                return [
                    cast(FloatSocket, node.i[i])
                    for i in range(*key.indices(len(node.i)))
                ]

        return cast(FloatSocket, node.i[key])

    def __iter__(self) -> Iterator["FloatSocket"]:
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
        ) -> "VectorSocket": ...
        @overload
        def __matmul__(self, other: Any) -> "MatrixSocket": ...

        def __rmatmul__(self, other: Any) -> "MatrixSocket": ...


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


class StringSocket(_StringMixin, Socket):
    """Runtime string socket wrapper."""


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
