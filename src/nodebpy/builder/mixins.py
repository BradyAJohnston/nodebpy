from __future__ import annotations

from types import EllipsisType
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast, overload

from bpy.types import NodeLink, NodeSocket

from ._registry import _wrap_socket
from ._utils import SocketError, _resolve_promotion, _SocketLike

_RShiftT = TypeVar("_RShiftT")

if TYPE_CHECKING:
    from ..nodes.geometry import CombineTransform
    from ..types import InputLinkable
    from .accessor import SocketAccessor
    from .node import BaseNode
    from .socket import (
        BooleanSocket,
        FloatSocket,
        IntegerSocket,
        MatrixSocket,
        Position,
        Socket,
        VectorSocket,
    )
    from .tree import TreeBuilder


class OperatorMixin:
    """All arithmetic, comparison, boolean, and matrix operator overloads.

    Requires ``_default_output_socket`` on the concrete class.
    Delegates all dispatch to type-specific ``_dispatch_*`` methods on Socket
    subclasses, looked up via ``_wrap_socket``.
    """

    __array_ufunc__ = None

    if TYPE_CHECKING:

        @property
        def _default_output_socket(self) -> "NodeSocket": ...

    def _apply_math_operation(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "FloatSocket | VectorSocket | IntegerSocket":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            reverse,
        )
        return _wrap_socket(socket)._dispatch_math(other, operation, reverse)

    def __mul__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "multiply")

    def __rmul__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "multiply", reverse=True)

    def __truediv__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "divide")

    def __rtruediv__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "divide", reverse=True)

    def __add__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "add")

    def __radd__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "add", reverse=True)

    def __sub__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "subtract")

    def __rsub__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "subtract", reverse=True)

    def __pow__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "power")

    def __rpow__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "power", reverse=True)

    def __mod__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "modulo")

    def __rmod__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        return self._apply_math_operation(other, "modulo", reverse=True)

    def __floordiv__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            False,
        )
        return _wrap_socket(socket)._dispatch_floordiv(other, reverse)

    def __rfloordiv__(self, other: Any) -> "FloatSocket | VectorSocket | IntegerSocket":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            True,
        )
        return _wrap_socket(socket)._dispatch_floordiv(other, reverse)

    @overload
    def __matmul__(self, other: "Position") -> "VectorSocket": ...
    @overload
    def __matmul__(self, other: "CombineTransform") -> "VectorSocket": ...
    def __matmul__(
        self, other: "Position | CombineTransform | VectorSocket | MatrixSocket"
    ) -> "VectorSocket | MatrixSocket":
        from ..builder.socket import VectorSocket
        from ..nodes.geometry import (
            MultiplyMatrices,
            Position,
            TransformPoint,
        )

        if isinstance(other, (Position, VectorSocket)):
            return TransformPoint(other, self).o.vector  # ty: ignore[invalid-argument-type]

        return MultiplyMatrices(self, other).o.matrix  # ty: ignore[invalid-argument-type]

    def __rmatmul__(self, other: Any) -> "MatrixSocket | VectorSocket":
        from ..builder.socket import VectorSocket
        from ..nodes.geometry import MultiplyMatrices, Position, TransformPoint

        if isinstance(
            self,
            (
                VectorSocket,
                Position,
            ),
        ):
            return TransformPoint(self, other).o.vector

        return MultiplyMatrices(other, self).o.matrix  # ty: ignore[invalid-argument-type]

    def __neg__(self) -> "FloatSocket | VectorSocket | IntegerSocket":
        return _wrap_socket(self._default_output_socket)._dispatch_unary("negate")

    def __abs__(self) -> "FloatSocket | VectorSocket | IntegerSocket":
        return _wrap_socket(self._default_output_socket)._dispatch_unary("absolute")

    if TYPE_CHECKING:

        def __mul__(self, other: Any) -> Self: ...
        def __rmul__(self, other: Any) -> Self: ...
        def __truediv__(self, other: Any) -> Self: ...
        def __rtruediv__(self, other: Any) -> Self: ...
        def __add__(self, other: Any) -> Self: ...
        def __radd__(self, other: Any) -> Self: ...
        def __sub__(self, other: Any) -> Self: ...
        def __rsub__(self, other: Any) -> Self: ...
        def __pow__(self, other: Any) -> Self: ...
        def __rpow__(self, other: Any) -> Self: ...
        def __mod__(self, other: Any) -> Self: ...
        def __rmod__(self, other: Any) -> Self: ...
        def __floordiv__(self, other: Any) -> Self: ...
        def __rfloordiv__(self, other: Any) -> Self: ...
        def __neg__(self) -> Self: ...
        def __abs__(self) -> Self: ...

    def _apply_compare_operation(
        self, other: Any, operation: str
    ) -> "FloatSocket | BooleanSocket":
        socket, other, _ = _resolve_promotion(
            self._default_output_socket,
            other,
            False,
        )
        return _wrap_socket(socket)._dispatch_compare(other, operation)

    def __lt__(self, other: Any) -> "FloatSocket | BooleanSocket":
        return self._apply_compare_operation(other, "less_than")

    def __gt__(self, other: Any) -> "FloatSocket | BooleanSocket":
        return self._apply_compare_operation(other, "greater_than")

    def __le__(self, other: Any) -> "FloatSocket | BooleanSocket":
        return self._apply_compare_operation(other, "less_equal")

    def __ge__(self, other: Any) -> "FloatSocket | BooleanSocket":
        return self._apply_compare_operation(other, "greater_equal")

    def __eq__(self, other: Any) -> "FloatSocket | BooleanSocket":  # type: ignore
        return self._apply_compare_operation(other, "equal")

    def __ne__(self, other: Any) -> "FloatSocket | BooleanSocket":  # type: ignore
        return self._apply_compare_operation(other, "not_equal")

    def _apply_boolean_operation(self, other: Any, operation: str):
        from ..nodes.geometry.converter import BooleanMath

        return getattr(BooleanMath, operation)(self, other)

    def __and__(self, other: Any):
        return self._apply_boolean_operation(other, "l_and")

    def __rand__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(other, cast(Any, self))

    def __or__(self, other: Any):
        return self._apply_boolean_operation(other, "l_or")

    def __ror__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(other, cast(Any, self))

    def __xor__(self, other: Any):
        return self._apply_boolean_operation(other, "not_equal")

    def __rxor__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.not_equal(other, cast(Any, self))

    def __invert__(self):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_not(cast(Any, self))


class LinkingMixin:
    """Node/socket linking logic: ``>>``, ``_link``, best-socket matching.

    Requires ``tree``, ``i``, ``o``, ``_default_output_socket``,
    and ``_default_input_socket`` on the concrete class.
    """

    tree: "TreeBuilder"

    if TYPE_CHECKING:
        import bpy

        node: bpy.types.Node

        @property
        def i(self) -> "SocketAccessor": ...

        @property
        def o(self) -> "SocketAccessor": ...

        @property
        def _default_output_socket(self) -> "NodeSocket": ...

    def _source_socket(self, node: "InputLinkable | Socket | NodeSocket") -> NodeSocket:
        assert node is not None
        if isinstance(node, NodeSocket):
            return node
        elif hasattr(node, "_default_output_socket"):
            return node._default_output_socket  # type: ignore[union-attr]
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    def _target_socket(self, node: "InputLinkable | Socket | NodeSocket") -> NodeSocket:
        assert node is not None
        if isinstance(node, NodeSocket):
            return node
        elif hasattr(node, "_default_input_socket"):
            return node._default_input_socket  # type: ignore[union-attr]
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    def _find_best_socket_pair(
        self,
        source: "BaseNode | Socket | NodeSocket | EllipsisType | LinkingMixin",
        target: "BaseNode | Socket | NodeSocket | EllipsisType | LinkingMixin",
    ) -> tuple[NodeSocket, NodeSocket]:
        """Find the best compatible pair of sockets between two nodes/sockets."""
        from ..builder.node import BaseNode
        from ..builder.socket import Socket
        from ..types import PREFER_FIRST_SOCKET, SOCKET_COMPATIBILITY

        possible_combos = []
        if isinstance(source, BaseNode):
            outputs = source.o._available
        elif isinstance(source, NodeSocket):
            outputs = [source]
        elif isinstance(source, Socket):
            outputs = [source.socket]
        else:
            raise TypeError(f"Cannot get outputs from {type(source)}")

        if isinstance(target, BaseNode):
            inputs = target.i._available
        elif isinstance(target, Socket):
            inputs = [target.socket]
        elif isinstance(target, NodeSocket):
            inputs = [target]
        else:
            raise TypeError(f"Cannot get inputs from {type(target)}")

        # NodeReroute adapts its type to whatever is linked — skip type matching
        if getattr(getattr(target, "node", None), "bl_idname", None) == "NodeReroute":
            if outputs and inputs:
                return inputs[0], outputs[0]

        # Try first available input first — if the output type matches it exactly,
        # or is a "preferred" implicit conversion (e.g. float→color, vector→color),
        # use the first socket rather than searching for a better-typed later one.
        # This keeps float→Image working in the compositor instead of drifting to
        # a float Factor socket that scores higher on raw compatibility.
        # Pairs not in PREFER_FIRST_SOCKET (e.g. VALUE→BOOLEAN, VECTOR→ROTATION)
        # fall through to the ranked search below.
        if inputs:
            first_input = inputs[0]
            for output in outputs:
                if first_input.type == output.type:
                    return first_input, output
                if (output.type, first_input.type) in PREFER_FIRST_SOCKET:
                    return first_input, output

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
            return sorted(possible_combos, key=lambda x: x[0])[0][1]

        # A node with a virtual ``__extend__`` input (Viewer, …) accepts any
        # source: linking to it makes Blender create a typed socket. Fall back
        # to it when nothing else matched, pairing with the source's first
        # available output.
        extend = next(
            (i for i in inputs if i.identifier.startswith("__extend__")), None
        )
        if extend is not None and outputs:
            return extend, outputs[0]

        src_name = getattr(getattr(source, "node", None), "name", repr(source))
        tgt_name = getattr(getattr(target, "node", None), "name", repr(target))
        raise SocketError(
            f"Cannot link any output from {src_name} to any input of {tgt_name}. "
            f"Available output types: {[f'{o.name}:{o.type}' for o in outputs]}, "
            f"Available input types: {[f'{i.name}:{i.type}' for i in inputs]}"
        )

    def _link(
        self, source: "InputLinkable | Socket | NodeSocket", target: "InputLinkable"
    ) -> NodeLink:
        source_socket = self._source_socket(source)
        target_socket = self._target_socket(target)
        return self.tree.link(source_socket, target_socket)

    def _link_from(
        self,
        source: "InputLinkable",
        input: "InputLinkable | str",
    ):
        from .node import _find_socket_from_name

        if isinstance(input, str):
            self._link(source, _find_socket_from_name(self.node.inputs, input))
        else:
            self._link(source, input)

    @overload
    def __rshift__(self, other: None) -> Self: ...
    @overload
    def __rshift__(self, other: _RShiftT) -> _RShiftT: ...
    def __rshift__(self, other: _RShiftT | None) -> _RShiftT | Self:
        """Chain nodes using >> operator. Links output to input.

        Usage:
            node1 >> node2 >> node3
            tree.inputs.value >> Math.add(..., 0.1) >> tree.outputs.result

        If the target node has an ellipsis placeholder (...), links to that specific input.
        Otherwise, finds the best compatible socket pair based on type compatibility.

        Returns the right-hand node to enable continued chaining. A ``None``
        target is a no-op passthrough — nothing is linked and ``self`` is
        returned so an optional node can be conditionally skipped::

            src >> SetPosition() >> (Transform() if trans else None) >> out
        """
        if other is None:
            return self
        if isinstance(other, _SocketLike):
            source = self._default_output_socket
            target = other.socket
        elif getattr(other, "_placeholder_inputs", None):
            node_other = cast("BaseNode", other)
            name = node_other._placeholder_inputs.pop(0)
            try:
                target = node_other.node.inputs[name]
            except KeyError:
                target = node_other.node.inputs[node_other.i._index(name)]
            source = (
                self.o._best_match(target.type)
                if hasattr(self, "o")
                else self._default_output_socket
            )
        else:
            try:
                source, target = self._find_best_socket_pair(self, cast(Any, other))
            except SocketError:
                source, target = cast("LinkingMixin", other)._find_best_socket_pair(
                    self, cast(Any, other)
                )

        self.tree.link(source, target)
        return other
