from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bpy.types import NodeLink, NodeSocket

from ._registry import _get_socket_linker
from ._utils import SocketError, _resolve_promotion, _SocketLike

if TYPE_CHECKING:
    from ..types import InputLinkable
    from .node import BaseNode
    from .socket import Socket


class OperatorMixin:
    """All arithmetic, comparison, boolean, and matrix operator overloads.

    Requires ``_default_output_socket`` on the concrete class.
    Delegates all dispatch to type-specific ``_dispatch_*`` methods on Socket
    subclasses, looked up via ``_get_socket_linker``.
    """

    __array_ufunc__ = None

    def _apply_math_operation(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "BaseNode":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            reverse,  # type: ignore[attr-defined]
        )
        return _get_socket_linker(socket)._dispatch_math(other, operation, reverse)

    def __mul__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "multiply")

    def __rmul__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "multiply", reverse=True)

    def __truediv__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "divide")

    def __rtruediv__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "divide", reverse=True)

    def __add__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "add")

    def __radd__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "add", reverse=True)

    def __sub__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "subtract")

    def __rsub__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "subtract", reverse=True)

    def __pow__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "power")

    def __rpow__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "power", reverse=True)

    def __mod__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "modulo")

    def __rmod__(self, other: Any) -> "BaseNode":
        return self._apply_math_operation(other, "modulo", reverse=True)

    def __floordiv__(self, other: Any) -> "BaseNode":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            False,  # type: ignore[attr-defined]
        )
        return _get_socket_linker(socket)._dispatch_floordiv(other, reverse)

    def __rfloordiv__(self, other: Any) -> "BaseNode":
        socket, other, reverse = _resolve_promotion(
            self._default_output_socket,
            other,
            True,  # type: ignore[attr-defined]
        )
        return _get_socket_linker(socket)._dispatch_floordiv(other, reverse)

    def __neg__(self) -> "BaseNode":
        return _get_socket_linker(self._default_output_socket)._dispatch_unary(  # type: ignore[attr-defined]
            "negate"
        )

    def __abs__(self) -> "BaseNode":
        return _get_socket_linker(self._default_output_socket)._dispatch_unary(  # type: ignore[attr-defined]
            "absolute"
        )

    def _apply_compare_operation(self, other: Any, operation: str) -> "BaseNode":
        return _get_socket_linker(self._default_output_socket)._dispatch_compare(  # type: ignore[attr-defined]
            other, operation
        )

    def __lt__(self, other: Any) -> "BaseNode":
        return self._apply_compare_operation(other, "less_than")

    def __gt__(self, other: Any) -> "BaseNode":
        return self._apply_compare_operation(other, "greater_than")

    def __le__(self, other: Any) -> "BaseNode":
        return self._apply_compare_operation(other, "less_equal")

    def __ge__(self, other: Any) -> "BaseNode":
        return self._apply_compare_operation(other, "greater_equal")

    def __eq__(self, other: Any) -> "BaseNode":  # type: ignore[override]
        return self._apply_compare_operation(other, "equal")

    def __ne__(self, other: Any) -> "BaseNode":  # type: ignore[override]
        return self._apply_compare_operation(other, "not_equal")

    def _apply_boolean_operation(self, other: Any, operation: str):
        from ..nodes.geometry.converter import BooleanMath

        return getattr(BooleanMath, operation)(self, other)

    def __and__(self, other: Any):
        return self._apply_boolean_operation(other, "l_and")

    def __rand__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(other, self)

    def __or__(self, other: Any):
        return self._apply_boolean_operation(other, "l_or")

    def __ror__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(other, self)

    def __xor__(self, other: Any):
        return self._apply_boolean_operation(other, "not_equal")

    def __rxor__(self, other: Any):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.not_equal(other, self)

    def __invert__(self):
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_not(self)

    @staticmethod
    def _cast_to_matrix(value):
        from ..nodes.geometry.converter import CombineMatrix

        if hasattr(value, "shape") and value.shape == (4, 4):
            return CombineMatrix(*value.ravel())
        else:
            return value

    def __matmul__(self, other: Any):
        from ..nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket  # type: ignore[attr-defined]
        other_type = getattr(other, "type", None)

        if socket.type == "MATRIX" and other_type == "VECTOR":
            return TransformPoint(other, socket)

        return MultiplyMatrices(self, other)

    def __rmatmul__(self, other: Any):
        from ..nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket  # type: ignore[attr-defined]
        other_type = getattr(other, "type", None)

        if socket.type == "VECTOR" and other_type == "MATRIX":
            return TransformPoint(socket, other)

        return MultiplyMatrices(other, self)


class LinkingMixin:
    """Node/socket linking logic: ``>>``, ``_link``, best-socket matching.

    Requires ``tree``, ``inputs``, ``outputs``, ``_default_output_socket``,
    and ``_default_input_socket`` on the concrete class.
    """

    def _source_socket(self, node: "InputLinkable | Socket | NodeSocket") -> NodeSocket:
        assert node
        if isinstance(node, NodeSocket):
            return node
        elif hasattr(node, "_default_output_socket"):
            return node._default_output_socket  # type: ignore[union-attr]
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    def _target_socket(self, node: "InputLinkable | Socket | NodeSocket") -> NodeSocket:
        assert node
        if isinstance(node, NodeSocket):
            return node
        elif hasattr(node, "_default_input_socket"):
            return node._default_input_socket  # type: ignore[union-attr]
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    def _find_best_socket_pair(
        self,
        source: "BaseNode | Socket | NodeSocket",
        target: "BaseNode | Socket | NodeSocket",
    ) -> tuple[NodeSocket, NodeSocket]:
        """Find the best compatible pair of sockets between two nodes/sockets."""
        from ..types import SOCKET_COMPATIBILITY

        possible_combos = []
        if hasattr(source, "outputs"):
            outputs = source.outputs._available  # type: ignore[union-attr]
        elif isinstance(source, NodeSocket):
            outputs = [source]
        else:
            raise TypeError(f"Cannot get outputs from {type(source)}")

        if hasattr(target, "inputs"):
            inputs = target.inputs._available  # type: ignore[union-attr]
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
            return sorted(possible_combos, key=lambda x: x[0])[0][1]

        raise SocketError(
            f"Cannot link any output from {source.node.name} to any input of {target.node.name}. "  # type: ignore[union-attr]
            f"Available output types: {[f'{o.name}:{o.type}' for o in outputs]}, "
            f"Available input types: {[f'{i.name}:{i.type}' for i in inputs]}"
        )

    def _link(
        self, source: "InputLinkable | Socket | NodeSocket", target: "InputLinkable"
    ) -> NodeLink:
        source_socket = self._source_socket(source)
        target_socket = self._target_socket(target)
        return self.tree.link(source_socket, target_socket)  # type: ignore[attr-defined]

    def _link_from(
        self,
        source: "InputLinkable",
        input: "InputLinkable | str",
    ):
        if isinstance(input, str):
            try:
                self._link(source, self.node.inputs[input])  # type: ignore[attr-defined]
            except KeyError:
                self._link(source, self.node.inputs[self.inputs._index(input)])  # type: ignore[attr-defined]
        else:
            self._link(source, input)

    def __rshift__(self, other: "BaseNode | Socket") -> "BaseNode | Socket":
        """Chain nodes using >> operator. Links output to input.

        Usage:
            node1 >> node2 >> node3
            tree.inputs.value >> Math.add(..., 0.1) >> tree.outputs.result

        If the target node has an ellipsis placeholder (...), links to that specific input.
        Otherwise, finds the best compatible socket pair based on type compatibility.

        Returns the right-hand node to enable continued chaining.
        """
        if isinstance(other, _SocketLike):
            source = self._default_output_socket  # type: ignore[attr-defined]
            target = other.socket  # type: ignore[attr-defined]
        elif getattr(other, "_placeholder_inputs", None):
            name = other._placeholder_inputs.pop(0)
            try:
                target = other.node.inputs[name]  # type: ignore[union-attr]
            except KeyError:
                target = other.node.inputs[other.inputs._index(name)]  # type: ignore[union-attr]
            source = self.outputs._best_match(target.type)  # type: ignore[attr-defined]
        else:
            try:
                source, target = self._find_best_socket_pair(self, other)  # type: ignore[arg-type]
            except SocketError:
                source, target = other._find_best_socket_pair(self, other)  # type: ignore[union-attr]

        self.tree.link(source, target)  # type: ignore[attr-defined]
        return other
