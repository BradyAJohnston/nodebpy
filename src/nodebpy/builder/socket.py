"""Typed Python wrappers around Blender node sockets.

These classes give each socket type (float, vector, color, …) a fluent,
type-aware API and the operator overloads used when wiring node trees.

Organization (top to bottom):
    * Type variables and result types
    * Base wrappers: ``BaseSocket`` and ``Socket``
    * Grid sockets and domain-bound field evaluation
    * Per-type behaviour mixins (``_VectorMixin``, ``_FloatMixin``, …)
    * Structural mixins (lists, default values, type conversions)
    * Concrete socket classes — the registry targets returned by ``_wrap_socket``
    * Registry registration (bl_idname -> socket class)
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    NamedTuple,
    Self,
    TypeVar,
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
    NodeSocketSound,
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
    InputFloatList,
    InputFont,
    InputGeometry,
    InputImage,
    InputInteger,
    InputIntegerList,
    InputMaterial,
    InputMatrix,
    InputMenu,
    InputObject,
    InputRotation,
    InputSound,
    InputString,
    InputVector,
)
from ._registry import _SOCKET_GRID_REGISTRY, _SOCKET_LIST_REGISTRY, _SOCKET_REGISTRY
from ._utils import _NodeLike, _output_socket_type, _SocketLike
from .mixins import LinkingMixin, OperatorMixin

if TYPE_CHECKING:
    from ..nodes import compositor, geometry, shader
    from ..nodes.geometry import (
        CombineMatrix,
        CombineTransform,
        Compare,
        FieldToGrid,
        GridInfo,
        GridToPoints,
        IntegerMath,
        MatchString,
        Math,
        MultiplyMatrices,
        ObjectInfo,
        Position,
        Vector,
        VectorMath,
    )
    from .node import BaseNode
    from .tree import TreeBuilder


# ---------------------------------------------------------------------------
# Type variables and result types
# ---------------------------------------------------------------------------

_T = TypeVar("_T")
_S = TypeVar("_S")
_BooleanResult = TypeVar(
    "_BooleanResult", "BooleanSocket", "BooleanSocketGrid", "BooleanSocketList"
)
_StringResult = TypeVar("_StringResult", "StringSocket", "StringSocketList")
_IntegerResult = TypeVar(
    "_IntegerResult", "IntegerSocket", "IntegerSocketGrid", "IntegerSocketList"
)
_FloatResult = TypeVar(
    "_FloatResult", "FloatSocket", "FloatSocketGrid", "FloatSocketList"
)
_VectorResult = TypeVar(
    "_VectorResult", "VectorSocket", "VectorSocketGrid", "VectorSocketList"
)
_RotationResult = TypeVar("_RotationResult", "RotationSocket", "RotationSocketList")
_MatrixResult = TypeVar("_MatrixResult", "MatrixSocket", "MatrixSocketList")


class ResultQuaternionComponents(NamedTuple, Generic[_FloatResult]):
    """Quaternion components returned by `RotationSocket.to_quaternion()`."""

    w: "_FloatResult"
    x: "_FloatResult"
    y: "_FloatResult"
    z: "_FloatResult"


class ResultAxisAngle(NamedTuple, Generic[_FloatResult, _VectorResult]):
    """Axis-angle components returned by `RotationSocket.to_axis_angle()`."""

    axis: "_VectorResult"
    angle: "_FloatResult"


class ResultStringFind(NamedTuple, Generic[_IntegerResult]):
    """Result of `StringSocket.find()`."""

    first_found: _IntegerResult
    count: _IntegerResult


class ResultMatrixSVD(NamedTuple, Generic[_MatrixResult, _VectorResult]):
    """SVD components returned by `MatrixSocket.svd()`."""

    u: "_MatrixResult"
    s: "_VectorResult"
    v: "_MatrixResult"


# ---------------------------------------------------------------------------
# Base socket wrappers
# ---------------------------------------------------------------------------


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
    def _socket_dtype(self) -> str:
        """Socket type normalised for node ``data_type`` / ``socket_type`` args.

        Blender names the float socket type ``VALUE``, but grid and list nodes
        expect ``FLOAT``; every other type passes through unchanged.
        """
        return self.socket.type.replace("VALUE", "FLOAT")

    @property
    def name(self) -> str:
        return str(self.socket.name)

    def _assert_output(self, method: str) -> None:
        if hasattr(self, "socket"):
            socket = self.socket
        else:
            socket = self._socket
        if not socket.is_output:
            raise RuntimeError(
                f"'{method}' is only available on output sockets, "
                f"not input socket '{socket.name}'."
            )

    def _assert_input(self, method: str) -> None:
        if hasattr(self, "socket"):
            socket = self.socket
        else:
            socket = self._socket
        if socket.is_output:
            raise RuntimeError(
                f"'{method}' is only available on output sockets, "
                f"not input socket '{socket.name}'."
            )

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
    def builder_node(self) -> "BaseNode":
        """The builder node that owns this socket, if accessed via .o/.i."""
        assert self._builder_node is not None
        return self._builder_node

    # -- Dispatch methods: per-type math logic. --
    # Called by OperatorMixin operators via _wrap_socket().
    # Subclasses (and type-specific mixins) override to provide type-specific behaviour.

    def enable_output(self, enable: InputBoolean = True) -> "Self":
        """Enable or disable the the output of this node group that is connected to this socket.

        If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

        Parameters
        ----------
        enable : InputBoolean, optional
            Whether to enable or disable the output, by default True.

        Returns
        -------
        Self
            The output socket or input socket, depending on the socket type.
        """
        from ..nodes.geometry import EnableOutput

        if self.socket.is_output:
            return EnableOutput(
                enable,
                self.socket,
                data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
            ).o.value  # ty: ignore[invalid-return-type]
        else:
            enable = EnableOutput(enable, None, data_type=self._socket_dtype)  # ty: ignore[invalid-argument-type]
            enable >> self.socket
            return enable.i.value  # ty: ignore[invalid-return-type]

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
                "not_equal": ("compare", True),
            }
            math_op, negate = _MATH_COMPARE_MAP[operation]
            result = getattr(Math, math_op)(self.socket, other).o.value
            if operation in ("equal", "not_equal"):
                result.builder_node.i.value_002.default_value = 0.00001
            if negate:
                result = Math.subtract(1.0, result._default_output_socket).o.value
            return result

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> Self: ...
        def __radd__(self, other: Any) -> Self: ...
        def __sub__(self, other: Any) -> Self: ...
        def __rsub__(self, other: Any) -> Self: ...
        def __mul__(self, other: Any) -> Self: ...
        def __rmul__(self, other: Any) -> Self: ...
        def __div__(self, other: Any) -> Self: ...
        def __rdiv__(self, other: Any) -> Self: ...
        def __truediv__(self, other: Any) -> Self: ...
        def __rtruediv__(self, other: Any) -> Self: ...
        def __floordiv__(self, other: Any) -> Self: ...
        def __rfloordiv__(self, other: Any) -> Self: ...
        def __neg__(self) -> Self: ...
        def __abs__(self) -> Self: ...
        def __lt__(self, other: Any) -> "BooleanSocket": ...
        def __gt__(self, other: Any) -> "BooleanSocket": ...
        def __le__(self, other: Any) -> "BooleanSocket": ...
        def __ge__(self, other: Any) -> "BooleanSocket": ...
        def __eq__(self, other: Any) -> "BooleanSocket": ...
        def __ne__(self, other: Any) -> "BooleanSocket": ...


class _GridMeanMixin(Socket):
    def mean(self, width: InputInteger = 1, iterations: InputInteger = 1) -> Self:
        """Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value."""
        from ..nodes.geometry import GridMean

        return GridMean(  # ty: ignore[invalid-return-type]
            self.socket,
            width=width,
            iterations=iterations,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid

    def median(self, width: InputInteger = 1, iterations: InputInteger = 1) -> Self:
        """Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value."""
        from ..nodes.geometry import GridMedian

        return GridMedian(  # ty: ignore[invalid-return-type]
            self.socket,
            width=width,
            iterations=iterations,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid


class _FloatGridOperatorMixin(Socket):
    def gradient(self) -> VectorSocketGrid:
        """Calculate the direction and magnitude of the change in values of a scalar grid."""
        from ..nodes.geometry import GridGradient

        return GridGradient(self.socket).o.gradient

    def laplacian(self) -> FloatSocketGrid:
        """Compute the divergence of the gradient of the input grid."""
        from ..nodes.geometry import GridLaplacian

        return GridLaplacian(self.socket).o.laplacian

    def sdf_fillet(self, iterations: InputInteger = 1) -> FloatSocketGrid:
        """Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces."""
        from ..nodes.geometry import SDFGridFillet

        return SDFGridFillet(self.socket, iterations=iterations).o.grid

    def sdf_laplacian(self, iterations: InputInteger = 1) -> FloatSocketGrid:
        """Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization."""
        from ..nodes.geometry import SDFGridLaplacian

        return SDFGridLaplacian(self.socket, iterations=iterations).o.grid

    def sdf_mean(
        self, width: InputInteger = 1, iterations: InputInteger = 1
    ) -> FloatSocketGrid:
        """Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field."""
        from ..nodes.geometry import SDFGridMean

        return SDFGridMean(self.socket, width=width, iterations=iterations).o.grid

    def sdf_mean_curvature(self, iterations: InputInteger = 1) -> FloatSocketGrid:
        """Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas."""
        from ..nodes.geometry import SDFGridMeanCurvature

        return SDFGridMeanCurvature(self.socket, iterations=iterations).o.grid

    def sdf_median(
        self, width: InputInteger = 1, iterations: InputInteger = 1
    ) -> FloatSocketGrid:
        """Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field."""
        from ..nodes.geometry import SDFGridMedian

        return SDFGridMedian(self.socket, width=width, iterations=iterations).o.grid

    def sdf_offset(self, distance: InputFloat = 0.1) -> FloatSocketGrid:
        """Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property."""
        from ..nodes.geometry import SDFGridOffset

        return SDFGridOffset(self.socket, distance=distance).o.grid

    def to_mesh(
        self, threshold: InputFloat = 0.1, adaptivity: InputFloat = 0.0
    ) -> GeometrySocket:
        """Generate a mesh on the "surface" of a volume grid."""
        from ..nodes.geometry import GridToMesh

        return GridToMesh(
            self.socket, threshold=threshold, adaptivity=adaptivity
        ).o.mesh


class _VectorGridOperatorMixin(Socket):
    def curl(self) -> VectorSocketGrid:
        """Calculate the magnitude and direction of circulation of a directional vector grid."""
        from ..nodes.geometry import GridCurl

        return GridCurl(self.socket).o.curl

    def divergence(self) -> FloatSocketGrid:
        """Calculate the flow into and out of each point of a directional vector grid."""
        from ..nodes.geometry import GridDivergence

        return GridDivergence(self.socket).o.divergence


# ---------------------------------------------------------------------------
# Grid sockets and domain-bound field evaluation
# ---------------------------------------------------------------------------


class _GridSocketMixin(Socket, Generic[_T]):
    def _info(self) -> "GridInfo[_T]":
        from ..nodes.geometry import GridInfo

        self._assert_output("transform / background_value")
        # Reuse one GridInfo per grid socket (cannot go through
        # _find_or_create_linked — data_type must match the grid type).
        for link in self.socket.links or ():
            assert link.to_node
            if link.to_node.bl_idname == GridInfo._bl_idname:
                return GridInfo._from_node(link.to_node)
        dtype = self.socket.type.replace("VALUE", "FLOAT")
        return GridInfo(self.socket, data_type=dtype)  # ty: ignore[invalid-argument-type, invalid-return-type]

    @property
    def transform(
        self,
    ) -> "MatrixSocket":
        return self._info().o.transform

    @property
    def background_value(
        self,
    ) -> "_T":
        return self._info().o.background_value

    def sample(
        self,
        position: InputVector = None,
        interpolation: Literal[
            "Nearest Neighbor", "Trilinear", "Triquadratic"
        ] = "Trilinear",
    ) -> _T:
        """Retrieve values from the specified volume grid."""
        from ..nodes.geometry import SampleGrid

        return SampleGrid(
            grid=self.socket,
            position=position,
            interpolation=interpolation,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.value  # ty: ignore[invalid-return-type]

    def sample_index(
        self,
        x: InputInteger = 0,
        y: InputInteger = 0,
        z: InputInteger = 0,
    ) -> _T:
        """Retrieve volume grid values at specific voxels."""
        from ..nodes.geometry import SampleGridIndex

        return SampleGridIndex(
            grid=self.socket,
            x=x,
            y=y,
            z=z,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.value  # ty: ignore[invalid-return-type]

    def field_to_grid(self) -> FieldToGrid:
        """Create new grids by evaluating new values on an existing volume grid topology."""
        from ..nodes.geometry import FieldToGrid

        return FieldToGrid(
            topology=self.socket,  # ty: ignore[invalid-argument-type]
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        )

    def clip(
        self,
        min_x: InputInteger = 0,
        min_y: InputInteger = 0,
        min_z: InputInteger = 0,
        max_x: InputInteger = 32,
        max_y: InputInteger = 32,
        max_z: InputInteger = 32,
    ) -> Self:
        """Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value."""
        from ..nodes.geometry import ClipGrid

        return ClipGrid(
            grid=self.socket,
            min_x=min_x,
            min_y=min_y,
            min_z=min_z,
            max_x=max_x,
            max_y=max_y,
            max_z=max_z,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid  # ty: ignore[invalid-return-type]

    def dilate_erode(
        self,
        steps: InputInteger = 1,
        connectivity: InputMenu | Literal["Face", "Edge", "Vertex"] = "Face",
        tiles: InputMenu | Literal["Ignore", "Expand", "Preserve"] = "Preserve",
    ) -> Self:
        """Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values."""
        from ..nodes.geometry import GridDilateErode

        return GridDilateErode(
            grid=self.socket,
            connectivity=connectivity,
            tiles=tiles,
            steps=steps,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid  # ty: ignore[invalid-return-type]

    def prune(
        self,
        threshold: InputFloat = 0.1,
        mode: InputMenu | Literal["Inactive", "Threshold", "SDF"] = None,
    ) -> Self:
        """Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes."""
        from ..nodes.geometry import PruneGrid

        return PruneGrid(
            grid=self.socket,
            threshold=threshold,
            mode=mode,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid  # ty: ignore[invalid-return-type]

    def voxelize(
        self,
    ) -> Self:
        """Remove sparseness from a volume grid by making the active tiles into voxels."""
        from ..nodes.geometry import VoxelizeGrid

        return VoxelizeGrid(
            grid=self.socket,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.grid  # ty: ignore[invalid-return-type]

    def to_points(self) -> GridToPoints[_T]:
        """Generate a point cloud from a volume grid's active voxels."""
        from ..nodes.geometry import GridToPoints

        return GridToPoints(
            grid=self.socket,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        )  # ty: ignore[invalid-return-type]


class _EvaluateField(Socket, Generic[_T]):
    """Domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`.

    Access via a domain property (e.g. ``socket.point``). Provides field
    evaluation methods; subclasses add statistics for numeric socket types.
    """

    def __init__(self, socket: NodeSocket, dtype: str, domain: str) -> None:
        self._socket = socket
        self._assert_output("Domain-specific evaluation")
        self._dtype = dtype
        self._domain = domain

    def evaluate(self) -> "_T":
        """Force evaluation of this field on the bound domain via ``EvaluateOnDomain``."""
        from ..nodes.geometry import EvaluateOnDomain

        return getattr(getattr(EvaluateOnDomain, self._domain), self._dtype)(
            self._socket
        ).o.value

    def at(self, index: InputInteger = 0) -> "_T":
        """Evaluate this field's value at *index* on the bound domain via ``EvaluateAtIndex``."""
        from ..nodes.geometry import EvaluateAtIndex

        return getattr(getattr(EvaluateAtIndex, self._domain), self._dtype)(
            self._socket, index
        ).o.value


class _AccumulateField(_EvaluateField[_T]):
    """Domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""

    def _accumulate(
        self, output: Literal["leading", "trailing", "total"], group_index: InputInteger
    ) -> "_T":

        from ..nodes.geometry import AccumulateField

        node = getattr(
            getattr(AccumulateField, self._domain),
            self._dtype.replace("matrix", "transform"),
        )(self._socket, group_index)
        return getattr(node.o, output)

    def leading(self, group_index: InputInteger = None) -> "_T":
        """The running total of values in the corresponding group, starting at the first value"""
        return self._accumulate("leading", group_index)

    def trailing(self, group_index: InputInteger = None) -> "_T":
        """The running total of values in the corresponding group, starting at 0"""
        return self._accumulate("trailing", group_index)

    def total(self, group_index: InputInteger = None) -> "_T":
        """The total sum of values in the corresponding group"""
        return self._accumulate("total", group_index)


class _MinMaxField(_AccumulateField[_T]):
    """Domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""

    def _minmax(self, output: str, group_index: InputInteger) -> "_T":
        from ..nodes.geometry import FieldMinAndMax

        node = getattr(getattr(FieldMinAndMax, self._domain), self._dtype)(
            self._socket, group_index
        )
        return getattr(node.o, output)

    def min(self, group_index: InputInteger = None) -> "_T":
        return self._minmax("min", group_index)

    def max(self, group_index: InputInteger = None) -> "_T":
        return self._minmax("max", group_index)


class _StatsField(_MinMaxField[_T]):
    """Domain-bound methods from `EvaluateAtIndex`, `EvaluateoOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""

    def mean(self, group_index: InputInteger = None) -> "_T":
        from ..nodes.geometry import FieldAverage

        node = getattr(getattr(FieldAverage, self._domain), self._dtype)(
            self._socket, group_index
        )
        return node.o.mean

    def median(self, group_index: InputInteger = None) -> "_T":
        from ..nodes.geometry import FieldAverage

        node = getattr(getattr(FieldAverage, self._domain), self._dtype)(
            self._socket, group_index
        )
        return node.o.median

    def std_dev(self, group_index: InputInteger = None) -> "_T":
        from ..nodes.geometry import FieldVariance

        node = getattr(getattr(FieldVariance, self._domain), self._dtype)(
            self._socket, group_index
        )
        return node.o.standard_deviation

    def variance(self, group_index: InputInteger = None) -> "_T":
        from ..nodes.geometry import FieldVariance

        node = getattr(getattr(FieldVariance, self._domain), self._dtype)(
            self._socket, group_index
        )
        return node.o.variance


# ---------------------------------------------------------------------------
# Per-type behaviour mixins
# ---------------------------------------------------------------------------


# Element-wise (Vector Math) dispatch shared by vector and colour sockets.
# Colours are treated as vectors for arithmetic, so both route through here.


def _dispatch_vector_math(
    socket: NodeSocket, other: Any, operation: str, reverse: bool = False
) -> "VectorSocket":
    from ..nodes.geometry import VectorMath

    values = (socket, other) if not reverse else (other, socket)

    if operation == "multiply":
        if isinstance(other, (int, float)):
            return VectorMath.scale(socket, other).o.vector
        if _output_socket_type(other) in ("VALUE", "FLOAT", "INT"):
            scale_by = (
                other if isinstance(other, NodeSocket) else other._default_output_socket
            )
            return VectorMath.scale(socket, scale_by).o.vector
        if isinstance(other, (list, tuple)) and len(other) == 3:
            return VectorMath.multiply(*values).o.vector
        if isinstance(other, (_SocketLike, _NodeLike, NodeSocket)):
            return VectorMath.multiply(*values).o.vector
        raise TypeError(
            f"Unsupported operand for multiply with a vector/colour socket: {type(other)}"
        )

    method = getattr(VectorMath, operation)
    if isinstance(other, (int, float)):
        scalar_vector = (other, other, other)
        node = (
            method(socket, scalar_vector)
            if not reverse
            else method(scalar_vector, socket)
        )
        return node.o.vector
    if (isinstance(other, (list, tuple)) and len(other) == 3) or isinstance(
        other, (_SocketLike, _NodeLike, NodeSocket)
    ):
        return method(*values).o.vector
    raise TypeError(
        f"Unsupported operand for {operation} with a vector/colour socket: {type(other)}"
    )


def _dispatch_vector_unary(socket: NodeSocket, operation: str) -> "VectorSocket":
    from ..nodes.geometry import VectorMath

    if operation == "negate":
        return VectorMath.scale(socket, -1).o.vector
    if operation == "absolute":
        return VectorMath.absolute(socket).o.vector
    raise ValueError(f"Unknown unary operation: {operation}")


def _dispatch_vector_floordiv(
    socket: NodeSocket, other: Any, reverse: bool = False
) -> "VectorSocket":
    from ..nodes.geometry import VectorMath

    divided = _dispatch_vector_math(socket, other, "divide", reverse)
    return VectorMath.floor(divided).o.vector


def _dispatch_vector_compare(
    self: BaseSocket, other: Any, operation: str
) -> "BooleanSocket | FloatSocket":
    if self._is_geometry_tree:
        from ..nodes.geometry import Compare

        return getattr(Compare.vector, operation)(self.socket, other).o.result
    return Socket._dispatch_compare(cast("Socket", self), other, operation)


class _VectorMixin(BaseSocket, Generic[_FloatResult, _VectorResult, _RotationResult]):
    """Vector-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocketVector
    _tree: TreeBuilder

    @property
    def _vmath(self) -> "type[VectorMath]":
        from ..nodes.geometry import VectorMath

        return VectorMath

    def _separate(self) -> "geometry.SeparateXYZ":
        from ..nodes.geometry import SeparateXYZ

        return SeparateXYZ._find_or_create_linked(self.socket)

    def _combine(self) -> "geometry.CombineXYZ":
        from ..nodes.geometry import CombineXYZ

        return CombineXYZ._find_or_create_linked(self.socket)

    @property
    def x(self) -> _FloatResult:
        if self.socket.is_output:
            return self._separate().o.x  # ty: ignore[invalid-return-type]
        else:
            return self._combine().i.x  # ty: ignore[invalid-return-type]

    @property
    def y(self) -> _FloatResult:
        if self.socket.is_output:
            return self._separate().o.y  # ty: ignore[invalid-return-type]
        else:
            return self._combine().i.y  # ty: ignore[invalid-return-type]

    @property
    def z(self) -> _FloatResult:
        if self.socket.is_output:
            return self._separate().o.z  # ty: ignore[invalid-return-type]
        else:
            return self._combine().i.z  # ty: ignore[invalid-return-type]

    def dot(self, vector: InputVector = (0.0, 0.0, 1.0)) -> _FloatResult:
        """Dot product with another vector and return the result as a `FloatSocket`."""
        self._assert_output("dot")
        return self._vmath.dot_product(self.socket, vector).o.value  # ty: ignore[invalid-return-type]

    def scale(self, scale: InputFloat) -> _VectorResult:
        """Scale this vector by a scalar value and return VectorSocket"""
        self._assert_output("scale")
        return self._vmath.scale(self.socket, scale).o.vector  # ty: ignore[invalid-return-type]

    def length(self) -> _FloatResult:
        """Get the length of this vector as a `FloatSocket`"""
        self._assert_output("length")
        return self._vmath.length(self.socket).o.value  # ty: ignore[invalid-return-type]

    def normalize(self) -> _VectorResult:
        """Normalize this vector, making its length 1.0."""
        self._assert_output("normalize")
        return self._vmath.normalize(self.socket).o.vector  # ty: ignore[invalid-return-type]

    def cross(self, other: InputVector = (0.0, 0.0, 1.0)) -> _VectorResult:
        """Cross product of this vector with *other*. Returns a vector perpendicular to both."""
        self._assert_output("cross")
        return self._vmath.cross_product(self.socket, other).o.vector  # ty: ignore[invalid-return-type]

    def distance(self, other: InputVector = (0.0, 0.0, 0.0)) -> _FloatResult:
        """Euclidean distance between this vector and *other*, as a `FloatSocket`."""
        self._assert_output("distance")
        return self._vmath.distance(self.socket, other).o.value  # ty: ignore[invalid-return-type]

    def project(self, other: InputVector = (0.0, 0.0, 0.0)) -> _VectorResult:
        """Project this vector onto *other*, as a `VectorSocket`."""
        self._assert_output("project")
        return self._vmath.project(self.socket, other).o.vector  # ty: ignore[invalid-return-type]

    def reflect(self, normal: InputVector = (0.0, 0.0, 1.0)) -> _VectorResult:
        """Reflect this vector around *normal*, as a `VectorSocket`."""
        self._assert_output("reflect")
        return self._vmath.reflect(self.socket, normal).o.vector  # ty: ignore[invalid-return-type]

    def map_range(
        self,
        from_min: InputVector = (0.0, 0.0, 0.0),
        from_max: InputVector = (1.0, 1.0, 1.0),
        to_min: InputVector = (0.0, 0.0, 0.0),
        to_max: InputVector = (1.0, 1.0, 1.0),
        *,
        clamp: bool = True,
        interpolation_type: Literal[
            "LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"
        ] = "LINEAR",
        steps: InputVector = (4.0, 4.0, 4.0),
    ) -> _VectorResult:
        """Convenience method to remap a vector socket using the `MapRange.vector()` node with this socket as input"""
        self._assert_output("map_range")
        from ..nodes.geometry import MapRange

        node = MapRange.vector(self.socket, from_min, from_max, to_min, to_max)
        node.clamp = clamp
        node.interpolation_type = interpolation_type
        if interpolation_type == "STEPPED":
            kwargs = {"Steps_FLOAT3": steps}
            node._establish_links(**kwargs)
        return node.o.vector  # ty: ignore[invalid-return-type]\

    def align_rotation(
        self,
        rotation: InputRotation = None,
        factor: InputFloat = 1.0,
        *,
        axis: Literal["X", "Y", "Z"] = "Z",
        pivot_axis: Literal["AUTO", "X", "Y", "Z"] = "AUTO",
    ) -> _RotationResult:
        """Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input."""
        from ..nodes.geometry import AlignRotationToVector

        return AlignRotationToVector(
            rotation=rotation,
            factor=factor,
            vector=self.socket,
            axis=axis,
            pivot_axis=pivot_axis,
        ).o.rotation  # ty: ignore[invalid-return-type]

    def rotate(
        self,
        rotation: InputRotation,
    ) -> _VectorResult:
        "Rotate this vector by the given rotation. Uses `RotateVector` with this socket as the vector input."
        self._assert_output("rotate")
        from ..nodes.geometry import RotateVector

        return RotateVector(self.socket, rotation).o.vector  # ty: ignore[invalid-return-type]

    def transform(self, matrix: InputMatrix) -> _VectorResult:
        "Transform this vector by the given matrix."
        self._assert_output("transform")
        from ..nodes.geometry import TransformPoint

        return TransformPoint(self.socket, matrix).o.vector  # ty: ignore[invalid-return-type]

    @overload
    def __rmatmul__(self, other: CombineTransform) -> _VectorResult: ...
    @overload
    def __rmatmul__(self, other: MultiplyMatrices) -> _VectorResult: ...
    @overload
    def __rmatmul__(self, other: CombineMatrix) -> _VectorResult: ...
    def __rmatmul__(
        self, other: CombineTransform | MultiplyMatrices | CombineMatrix | MatrixSocket
    ) -> _VectorResult:
        "Transform this vector by the given matrix."
        from ..nodes.geometry import TransformPoint

        return TransformPoint(self.socket, other).o.vector  # ty: ignore[invalid-return-type]

    @overload
    def __getitem__(self, key: slice) -> "list[_FloatResult]": ...
    @overload
    def __getitem__(self, key: int) -> "_FloatResult": ...
    def __getitem__(self, key: int | slice) -> "_FloatResult | list[_FloatResult]":
        if self.socket.is_output:
            node = self._separate()
            return [node.o.x, node.o.y, node.o.z][key]  # ty: ignore[invalid-return-type]

        else:
            node = self._combine()
            return [node.i.x, node.i.y, node.i.z][key]  # ty: ignore[invalid-return-type]

    def __iter__(self) -> Iterator[_FloatResult]:
        if self.socket.is_output:
            node = self._separate()
            yield node.o.x  # ty: ignore[invalid-yield]
            yield node.o.y  # ty: ignore[invalid-yield]
            yield node.o.z  # ty: ignore[invalid-yield]
        else:
            node = self._combine()
            yield node.i.x  # ty: ignore[invalid-yield]
            yield node.i.y  # ty: ignore[invalid-yield]
            yield node.i.z  # ty: ignore[invalid-yield]

    def __len__(self) -> int:
        return 3

    def _dispatch_unary(self, operation: str) -> _VectorResult:
        return _dispatch_vector_unary(self.socket, operation)  # ty: ignore[invalid-return-type]

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> _VectorResult:
        return _dispatch_vector_math(self.socket, other, operation, reverse)  # ty: ignore[invalid-return-type]

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> _VectorResult:
        return _dispatch_vector_floordiv(self.socket, other, reverse)  # ty: ignore[invalid-return-type]

    def _dispatch_compare(
        self, other: Any, operation: str
    ) -> _BooleanResult | _FloatResult:
        return _dispatch_vector_compare(self, other, operation)  # ty: ignore[invalid-return-type]

    if TYPE_CHECKING:

        def scale(self, scale: InputFloat) -> Self: ...
        def normalize(self) -> Self: ...
        def cross(self, other: InputVector) -> Self: ...
        def project(self, other: InputVector) -> Self: ...
        def reflect(self, normal: InputVector) -> Self: ...
        def map_range(self, *args: Any, **kwargs: Any) -> Self: ...
        def rotate(self, rotation: InputRotation) -> Self: ...
        def transform(self, matrix: InputMatrix) -> Self: ...
        def _dispatch_unary(self, operation: str) -> Self: ...
        def _dispatch_math(
            self, other: Any, operation: str, reverse: bool = ...
        ) -> Self: ...
        def _dispatch_floordiv(self, other: Any, reverse: bool = ...) -> Self: ...
        def __add__(self, other: Any) -> Self: ...
        def __radd__(self, other: Any) -> Self: ...
        def __sub__(self, other: Any) -> Self: ...
        def __rsub__(self, other: Any) -> Self: ...
        def __mul__(self, other: Any) -> Self: ...
        def __rmul__(self, other: Any) -> Self: ...
        def __truediv__(self, other: Any) -> Self: ...
        def __rtruediv__(self, other: Any) -> Self: ...
        def __floordiv__(self, other: Any) -> Self: ...
        def __rfloordiv__(self, other: Any) -> Self: ...
        def __neg__(self) -> Self: ...
        def __abs__(self) -> Self: ...
        def __lt__(self, other: Any) -> "Compare[_VectorResult]": ...
        def __gt__(self, other: Any) -> "Compare[_VectorResult]": ...
        def __le__(self, other: Any) -> "Compare[_VectorResult]": ...
        def __ge__(self, other: Any) -> "Compare[_VectorResult]": ...


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

    @property
    def point(self) -> "_EvaluateField[ColorSocket]":
        """BooleanSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""

        return _EvaluateField(self.socket, "color", "point")

    @property
    def edge(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "edge")

    @property
    def face(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "face")

    @property
    def corner(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "corner")

    @property
    def spline(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "spline")

    @property
    def instance(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "instance")

    @property
    def layer(self) -> "_EvaluateField[ColorSocket]":
        """ColorSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "color", "layer")

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

    # Colours behave like vectors for arithmetic — share the vector dispatch so
    # ``-col``, ``abs(col)`` and ``col // x`` use Vector Math (not scalar Math).

    def _dispatch_math(
        self, other: Any, operation: str, reverse: bool = False
    ) -> "VectorSocket":
        return _dispatch_vector_math(self.socket, other, operation, reverse)

    def _dispatch_unary(self, operation: str) -> "VectorSocket":
        return _dispatch_vector_unary(self.socket, operation)

    def _dispatch_floordiv(self, other: Any, reverse: bool = False) -> "VectorSocket":
        return _dispatch_vector_floordiv(self.socket, other, reverse)

    def _dispatch_compare(
        self, other: Any, operation: str
    ) -> "BooleanSocket | FloatSocket":
        return _dispatch_vector_compare(self, other, operation)


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

    def sound(self, false: InputSound = None, true: InputSound = None) -> "SoundSocket":
        return self._switch.sound(self._socket, false, true).o.output


class _BooleanMixin(BaseSocket):
    """Boolean-specific operator overrides — routes directly through BooleanMath."""

    socket: NodeSocketBool

    def __or__(self, other: Any) -> Self:
        self._assert_output("|")
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_or(self.socket, other).o.boolean  # ty: ignore[invalid-return-type]

    def __and__(self, other: Any) -> Self:
        self._assert_output("&")
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_and(self.socket, other).o.boolean  # ty: ignore[invalid-return-type]

    def __xor__(self, other: Any) -> Self:
        self._assert_output("^")
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.not_equal(self.socket, other).o.boolean  # ty: ignore[invalid-return-type]

    def __invert__(self) -> Self:
        self._assert_output("~")
        from ..nodes.geometry.converter import BooleanMath

        return BooleanMath.l_not(self.socket).o.boolean  # ty: ignore[invalid-return-type]

    @property
    def switch(self) -> "_BooleanSwitchSocketFactory":
        "Creat a Switch node with this boolean as the `switch` input."
        self._assert_output("switch")
        return _BooleanSwitchSocketFactory(self.socket)


class _RotationMixin(BaseSocket, Generic[_FloatResult, _VectorResult]):
    """Rotation-specific methods."""

    socket: NodeSocketRotation

    def invert(self) -> Self:
        "Invert the rotation of the socket."
        self._assert_output("invert")
        from ..nodes.geometry import InvertRotation

        return InvertRotation._find_or_create_linked(self.socket).o.rotation  # ty: ignore[invalid-return-type]

    def rotate(
        self,
        rotation: InputRotation,
        rotation_space: Literal["GLOBAL", "LOCAL"] = "GLOBAL",
    ) -> Self:
        "Rotate this rotation by the given rotation in the specified rotation space."
        self._assert_output("rotate")
        from ..nodes.geometry import RotateRotation

        return RotateRotation(
            self.socket, rotation, rotation_space=rotation_space
        ).o.rotation  # ty: ignore[invalid-return-type]

    def to_euler(self) -> _VectorResult:
        "Convert the rotation to an XYZ euler rotation and return `VectorSocket`."
        self._assert_output("to_euler")
        from ..nodes.geometry.converter import RotationToEuler

        return RotationToEuler._find_or_create_linked(self.socket).o.euler  # ty: ignore[invalid-return-type]

    def to_quaternion(self) -> ResultQuaternionComponents[_FloatResult]:
        "Decompose the rotation into quaternion components `(w, x, y, z)`."
        self._assert_output("to_quaternion")
        from ..nodes.geometry import RotationToQuaternion

        o = RotationToQuaternion._find_or_create_linked(self.socket).o
        return ResultQuaternionComponents(o.w, o.x, o.y, o.z)  # ty: ignore[invalid-return-type]

    def to_axis_angle(self) -> ResultAxisAngle[_FloatResult, _VectorResult]:
        "Decompose the rotation into axis-angle components `(axis, angle)`."
        self._assert_output("to_axis_angle")
        from ..nodes.geometry import RotationToAxisAngle

        o = RotationToAxisAngle(self.socket).o
        return ResultAxisAngle(o.axis, o.angle)  # ty: ignore[invalid-return-type]

    def align_to_vector(
        self,
        vector: InputVector = (0.0, 0.0, 1.0),
        factor: InputFloat = 1.0,
        *,
        axis: Literal["X", "Y", "Z"] = "Z",
        pivot_axis: Literal["AUTO", "X", "Y", "Z"] = "AUTO",
    ) -> Self:
        "Align the specified axis of this rotation to the given vector. Uses `AlignRotationToVector` with this socket as the rotation input."
        self._assert_output("align_to_vector")
        from ..nodes.geometry import AlignRotationToVector

        return AlignRotationToVector(
            rotation=self.socket,
            factor=factor,
            vector=vector,
            axis=axis,
            pivot_axis=pivot_axis,
        ).o.rotation  # ty: ignore[invalid-return-type]


class _FloatMixDataTypeFactory:
    """Factory for typed Mix nodes driven by a float factor socket.

    Access via ``FloatSocket.mix``. Each method creates a ``Mix`` node using
    this socket as the factor and returns the corresponding output socket.
    """

    def __init__(self, socket: NodeSocket):
        self._socket = socket
        from ..nodes.geometry import Mix

        self._mix = Mix

    def float(self, a: InputFloat, b: InputFloat) -> "FloatSocket":
        "Mix two float values, returning a ``FloatSocket``."
        return self._mix.float(self._socket, a, b).o.result_float

    def vector(self, a: InputVector, b: InputVector) -> "VectorSocket":
        "Mix two vectors, returning a ``VectorSocket``."
        return self._mix.vector(self._socket, a, b).o.result_vector

    def color(self, a: InputColor, b: InputColor) -> "ColorSocket":
        "Mix two colors, returning a ``ColorSocket``."
        return self._mix.color(self._socket, a, b).o.result_color

    def rotation(self, a: InputRotation, b: InputRotation) -> "RotationSocket":
        "Mix two rotations, returning a ``RotationSocket``."
        return self._mix.rotation(self._socket, a, b).o.result_rotation


class _FloatMixin(BaseSocket, Generic[_IntegerResult]):
    """Float-specific properties (.x, .y, .z) and dispatch."""

    socket: NodeSocketFloat

    @property
    def _math(self) -> "type[Math]":
        from ..nodes.geometry import Math

        return Math

    @property
    def mix(self) -> _FloatMixDataTypeFactory:
        "Create a ``Mix`` node using this socket as the factor."
        self._assert_output("mix")
        return _FloatMixDataTypeFactory(self.socket)

    def map_range(
        self,
        from_min: InputFloat = 0.0,
        from_max: InputFloat = 1.0,
        to_min: InputFloat = 0.0,
        to_max: InputFloat = 1.0,
        *,
        clamp=True,
        interpolation_type: Literal[
            "LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"
        ] = "LINEAR",
        steps: InputFloat = 4.0,
    ) -> Self:
        """Remap the values on the float socket using the MapRange node."""
        self._assert_output("map_range")
        from ..nodes.geometry import MapRange

        node = MapRange.float(self.socket, from_min, from_max, to_min, to_max)
        node.clamp = clamp
        node.interpolation_type = interpolation_type
        if interpolation_type == "STEPPED":
            node._establish_links(steps=steps)
        return node.o.result  # ty: ignore[invalid-return-type]

    def clamp(self, min: InputFloat = 0.0, max: InputFloat = 1.0) -> Self:
        """Clamp the value to *[min, max]*. Defaults to the unit interval ``[0, 1]``."""
        self._assert_output("clamp")
        from ..nodes.geometry import Clamp

        return Clamp.min_max(self.socket, min, max).o.result  # ty: ignore[invalid-return-type]

    def min(self, value: InputFloat = 0.0) -> Self:
        """Create Math with operation 'Minimum'. The minimum from self and value"""
        self._assert_output("min")
        return self._math.minimum(self.socket, value).o.value  # ty: ignore[invalid-return-type]

    def max(self, value: InputFloat = 1.0) -> Self:
        """Create Math with operation 'Maximum'. The maximum from self and value"""
        self._assert_output("max")
        return self._math.maximum(self.socket, value).o.value  # ty: ignore[invalid-return-type]

    def sin(self) -> Self:
        "Create a Math node with operation 'Sine'. The sine of self"
        self._assert_output("sin")
        return self._math.sine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def cos(self) -> Self:
        "Create a Math node with operation 'Cosine'. The cosine of self"
        self._assert_output("cos")
        return self._math.cosine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def tan(self) -> Self:
        "Create a Math node with operation 'Tangent'. The tangent of self"
        self._assert_output("tan")
        return self._math.tangent(self.socket).o.value  # ty: ignore[invalid-return-type]

    def asin(self) -> Self:
        "Create a Math node with operation 'ArcSine'. The arcsine of self"
        self._assert_output("asin")
        return self._math.arcsine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def acos(self) -> Self:
        "Create a Math node with operation 'ArcCosine'. The arccosine of self"
        self._assert_output("acos")
        return self._math.arccosine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def atan(self) -> Self:
        "Create a Math node with operation 'ArcTangent'. The arctangent of self"
        self._assert_output("atan")
        return self._math.arctangent(self.socket).o.value  # ty: ignore[invalid-return-type]

    def sinh(self) -> Self:
        "Create a Math node with operation 'Hyperbolic Sine'. The hyperbolic sine of self"
        self._assert_output("sinh")
        return self._math.hyperbolic_sine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def cosh(self) -> Self:
        "Create a Math node with operation 'Hyperbolic Cosine'. The hyperbolic cosine of self"
        self._assert_output("cosh")
        return self._math.hyperbolic_cosine(self.socket).o.value  # ty: ignore[invalid-return-type]

    def tanh(self) -> Self:
        "Create a Math node with operation 'Hyperbolic Tangent'. The hyperbolic tangent of self"
        self._assert_output("tanh")
        return self._math.hyperbolic_tangent(self.socket).o.value  # ty: ignore[invalid-return-type]

    def exp(self) -> Self:
        "Create a Math node with operation 'Exponent'. The exponent of self"
        self._assert_output("exp")
        return self._math.exponent(self.socket).o.value  # ty: ignore[invalid-return-type]

    def snap(self, increment: InputFloat = 0.5) -> Self:
        "Create a Math node with operation 'Snap'. The snap of self"
        self._assert_output("snap")
        return self._math.snap(self.socket, increment).o.value  # ty: ignore[invalid-return-type]

    def atan2(self, value: InputFloat = 0.5) -> Self:
        "Create a Math node with operation 'ArcTan2'. The arctangent of self"
        self._assert_output("atan2")
        return self._math.arctan2(self.socket, value).o.value  # ty: ignore[invalid-return-type]

    def sqrt(self) -> Self:
        """Return the square root of this value."""
        self._assert_output("sqrt")
        return self._math.square_root(self.socket).o.value  # ty: ignore[invalid-return-type]

    def power(self, exponent: InputFloat = 2.0) -> Self:
        """Raise this value to *exponent*."""
        self._assert_output("power")
        return self._math.power(self.socket, exponent).o.value  # ty: ignore[invalid-return-type]

    def log(self, base: InputFloat = 2.0) -> Self:
        """Return the logarithm of this value to *base*."""
        self._assert_output("log")
        return self._math.logarithm(self.socket, base).o.value  # ty: ignore[invalid-return-type]

    def floor(self) -> Self:
        """Round down to the nearest integer."""
        self._assert_output("floor")
        return self._math.floor(self.socket).o.value  # ty: ignore[invalid-return-type]

    def ceil(self) -> Self:
        """Round up to the nearest integer."""
        self._assert_output("ceil")
        return self._math.ceil(self.socket).o.value  # ty: ignore[invalid-return-type]

    def truncate(self) -> Self:
        """The integer part of of the value, removing fractional digits"""
        self._assert_output("truncate")
        return self._math.truncate(self.socket).o.value  # ty: ignore[invalid-return-type]

    def fraction(self) -> Self:
        """The fractional part of the vlaue"""
        self._assert_output("fraction")
        return self._math.fraction(self.socket).o.value  # ty: ignore[invalid-return-type]

    def round(self) -> Self:
        """Round to the nearest integer."""
        self._assert_output("round")
        return self._math.round(self.socket).o.value  # ty: ignore[invalid-return-type]

    def ping_pong(self, value: InputFloat = 1.0) -> Self:
        """Input ping-pongs between 0 and *value*."""
        self._assert_output("ping_pong")
        return self._math.ping_pong(self.socket, value).o.value  # ty: ignore[invalid-return-type]

    def modulo(self, divisor: InputFloat) -> Self:
        """Floored modulo — remainder after dividing by *divisor*, always non-negative."""
        self._assert_output("modulo")
        return self._math.floored_modulo(self.socket, divisor).o.value  # ty: ignore[invalid-return-type]

    def abs(self) -> Self:
        """Absolute value of the input"""
        self._assert_output("abs")
        return self._math.absolute(self.socket).o.value  # ty: ignore[invalid-return-type]

    def wrap(self, min: InputFloat = 0.0, max: InputFloat = 1.0) -> Self:
        """Wrap the value into the *[min, max]* range, repeating cyclically."""
        self._assert_output("wrap")
        # the wrap method has different order of arguments with max being first
        # compared to other nodes that are defined.
        return self._math.wrap(self.socket, value_001=max, value_002=min).o.value  # ty: ignore[invalid-return-type]

    def mul_add(self, multiplier: InputFloat = 0.5, addend: InputFloat = 0.5) -> Self:
        """Multiply and then add a value. More efficient as it is a single CPU instruction."""
        self._assert_output("mul_add")
        return self._math.multiply_add(self.socket, multiplier, addend).o.value  # ty: ignore[invalid-return-type]

    def to_radians(self) -> Self:
        """Convert degrees to radians."""
        self._assert_output("to_radians")
        return self._math.to_radians(self.socket).o.value  # ty: ignore[invalid-return-type]

    def to_degrees(self) -> Self:
        """Convert radians to degrees."""
        self._assert_output("to_degrees")
        return self._math.to_degrees(self.socket).o.value  # ty: ignore[invalid-return-type]

    def sign(self) -> Self:
        "Return the sign of the FloatSocket, eithe `-1`, `0` or `1`."
        self._assert_output("sign")
        return self._math.sign(self.socket).o.value  # ty: ignore[invalid-return-type]

    def negate(self) -> Self:
        "Negate the `FloatSocket` by multiplying the value by `-1`."
        self._assert_output("negate")
        return self._math.multiply(self.socket, -1).o.value  # ty: ignore[invalid-return-type]


class _IntegerMixin(BaseSocket, Generic[_FloatResult]):
    """Integer-specific dispatch — uses IntegerMath in geometry trees."""

    socket: NodeSocketInt
    tree: TreeBuilder
    _tree: TreeBuilder

    @property
    def _imath(self) -> "type[IntegerMath]":
        from ..nodes.geometry import IntegerMath

        return IntegerMath

    def clamp(self, min: InputInteger = 0, max: InputInteger = 1) -> Self:
        """Clamp the value to *[min, max]*."""
        self._assert_output("clamp")
        return self._imath.minimum(
            self._imath.maximum(self.socket, min).o.value, max
        ).o.value  # ty: ignore[invalid-return-type]

    def modulo(self, divisor: InputInteger) -> Self:
        """Remainder after dividing by *divisor* (always non-negative)."""
        self._assert_output("modulo")
        return self._imath.modulo(self.socket, divisor).o.value  # ty: ignore[invalid-return-type]

    def abs(self) -> Self:
        """Return the absolute value of the IntegerSocket."""
        self._assert_output("abs")
        return self._imath.absolute(self.socket).o.value  # ty: ignore[invalid-return-type]

    def sign(self) -> Self:
        "Return the sign of the IntegerSocket, either `-1`, `0`, or `1`."
        self._assert_output("sign")
        return self._imath.sign(self.socket).o.value  # ty: ignore[invalid-return-type]

    def negate(self) -> Self:
        """Negate the IntegerSocket value. Positive becomes negative, negative becomes positive."""
        self._assert_output("negate")
        return self._imath.negate(self.socket).o.value  # ty: ignore[invalid-return-type]

    def mul_add(self, multiplier: InputInteger = 0, addend: InputInteger = 0) -> Self:
        "Multiply and then add a value. More efficient as it is a single CPU instruction."
        self._assert_output("mul_add")
        return self._imath.multiply_add(self.socket, multiplier, addend).o.value  # ty: ignore[invalid-return-type]

    def power(self, exponent: InputInteger = 2) -> Self:
        """Raise this value to *exponent*."""
        self._assert_output("power")
        return self._imath.power(self.socket, exponent).o.value  # ty: ignore[invalid-return-type]

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
    ) -> Self | _FloatResult:
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return getattr(IntegerMath, operation)(*values).o.value
        return Socket._dispatch_math(cast("Socket", self), other, operation, reverse)  # ty: ignore[invalid-return-type]

    def _dispatch_unary(self, operation: str) -> Self | _FloatResult:
        if self._is_geometry_tree:
            from ..nodes.geometry.converter import IntegerMath

            if operation == "negate":
                return IntegerMath.negate(self.socket).o.value  # ty: ignore[invalid-return-type]
            elif operation == "absolute":
                return IntegerMath.absolute(self.socket).o.value  # ty: ignore[invalid-return-type]
        return Socket._dispatch_unary(cast("Socket", self), operation)  # ty: ignore[invalid-return-type]

    def _dispatch_floordiv(
        self, other: Any, reverse: bool = False
    ) -> Self | _FloatResult:
        if self._is_geometry_tree and self._other_is_integer(other):
            from ..nodes.geometry.converter import IntegerMath

            values = (self.socket, other) if not reverse else (other, self.socket)
            return IntegerMath.divide_floor(*values).o.value  # ty: ignore[invalid-return-type]
        return Socket._dispatch_floordiv(cast("Socket", self), other, reverse)  # ty: ignore[invalid-return-type]

    def _dispatch_compare(self, other: Any, operation: str) -> Self | _FloatResult:
        if self._is_geometry_tree:
            from ..nodes.geometry.manual import Compare

            return getattr(Compare.integer, operation)(self.socket, other).o.result
        return Socket._dispatch_compare(cast("Socket", self), other, operation)  # ty: ignore[invalid-return-type]

    if TYPE_CHECKING:

        def __add__(self, other: Any) -> Self: ...
        def __radd__(self, other: Any) -> Self: ...
        def __sub__(self, other: Any) -> Self: ...
        def __rsub__(self, other: Any) -> Self: ...
        def __mul__(self, other: Any) -> Self: ...
        def __rmul__(self, other: Any) -> Self: ...
        def __truediv__(self, other: Any) -> Self: ...
        def __rtruediv__(self, other: Any) -> Self: ...
        def __floordiv__(self, other: Any) -> Self: ...
        def __rfloordiv__(self, other: Any) -> Self: ...
        def __neg__(self) -> Self: ...
        def __abs__(self) -> Self: ...
        def __lt__(self, other: Any) -> "Compare[IntegerSocket]": ...
        def __gt__(self, other: Any) -> "Compare[IntegerSocket]": ...
        def __le__(self, other: Any) -> "Compare[IntegerSocket]": ...
        def __ge__(self, other: Any) -> "Compare[IntegerSocket]": ...


class _StringMixin(BaseSocket, Generic[_StringResult, _BooleanResult, _IntegerResult]):
    """String-specific methods (match, slice, join, etc.)."""

    socket: NodeSocketString

    @property
    def _match(self) -> "type[MatchString]":
        from ..nodes.geometry import MatchString

        return MatchString

    def starts_with(self, search: InputString) -> _BooleanResult:
        "Create a MatchString[Starts With], return the result as a `BooleanSocket`."
        self._assert_output("starts_with")
        return self._match(self.socket, "Starts With", search).o.result  # ty: ignore[invalid-return-type]

    def ends_with(self, search: InputString) -> _BooleanResult:
        "Create a MatchString[Ends With], return the result as a `BooleanSocket`."
        self._assert_output("ends_with")
        return self._match(self.socket, "Ends With", search).o.result  # ty: ignore[invalid-return-type]

    def contains(self, search: InputString) -> _BooleanResult:
        "Create a MatchString[Contains], return the result as a `BooleanSocket`."
        self._assert_output("contains")
        return self._match(self.socket, "Contains", search).o.result  # ty: ignore[invalid-return-type]

    def slice(
        self, position: InputInteger = 0, length: InputInteger = 0
    ) -> _StringResult:
        "Slice a given string from a starting position for a given length."
        self._assert_output("slice")
        from ..nodes.geometry import SliceString

        return SliceString(self.socket, position, length).o.string  # ty: ignore[invalid-return-type]

    def format(
        self, items: Mapping[str, InputString | InputInteger | InputFloat]
    ) -> _StringResult:
        "Format a given string with the key-value items."
        self._assert_output("format")
        from ..nodes.geometry import FormatString

        return FormatString(self.socket, items).o.string  # ty: ignore[invalid-return-type]

    def replace(self, find: InputString, replace: InputString) -> _StringResult:
        "Replace every match of the string with the replacement string"
        self._assert_output("replace")
        from ..nodes.geometry import ReplaceString

        return ReplaceString(self.socket, find, replace).o.string  # ty: ignore[invalid-return-type]

    def reverse(self) -> _StringResult:
        "Reverse the string."
        self._assert_output("reverse")
        from ..nodes.geometry import ReverseString

        return ReverseString(self.socket).o.string  # ty: ignore[invalid-return-type]

    def length(self) -> _IntegerResult:
        "Compute the length of a string and return as `IntegerSocket`."
        self._assert_output("length")
        from ..nodes.geometry import StringLength

        return StringLength(self.socket).o.length  # ty: ignore[invalid-return-type]

    def find(self, search: InputString) -> ResultStringFind[_IntegerResult]:
        "Find where in a string a pattern occurs. Returns `(first_found, count)`."
        self._assert_output("find")
        from ..nodes.geometry import FindInString

        o = FindInString(self.socket, search).o
        return ResultStringFind(o.first_found, o.count)  # ty: ignore[invalid-return-type]

    def uppercase(self) -> _StringResult:
        "Convert the string to uppercase and return as `StringSocket`."
        self._assert_output("uppercase")
        from ..nodes.geometry import SetStringCase

        return SetStringCase(self.socket, case="Uppercase").o.string  # ty: ignore[invalid-return-type]

    def lowercase(self) -> _StringResult:
        "Convert the string to lowercase and return as `StringSocket`."
        self._assert_output("lowercase")
        from ..nodes.geometry import SetStringCase

        return SetStringCase(self.socket, case="Lowercase").o.string  # ty: ignore[invalid-return-type]


class _MatrixMixin(
    BaseSocket, Generic[_VectorResult, _RotationResult, _FloatResult, _MatrixResult]
):
    """Matrix-specific properties (.translation, .rotation, .scale) via SeparateTransform."""

    socket: NodeSocketMatrix

    @property
    def translation(self) -> _VectorResult:
        """Get the translation component of the matrix, via [`~nodebpy.nodes.geometry.converter.SeparateTransform`]."""
        self._assert_output("translation")
        from ..nodes.geometry.converter import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.translation  # ty: ignore[invalid-return-type]

    @property
    def rotation(self) -> _RotationResult:
        """Get the rotation component of the matrix, via [`~nodebpy.nodes.geometry.converter.SeparateTransform`]."""
        self._assert_output("rotation")
        from ..nodes.geometry.converter import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.rotation  # ty: ignore[invalid-return-type]

    @property
    def scale(self) -> _VectorResult:
        """Get the scale component of the matrix, via [`~nodebpy.nodes.geometry.converter.SeparateTransform`]."""
        self._assert_output("scale")
        from ..nodes.geometry.converter import SeparateTransform

        return SeparateTransform._find_or_create_linked(self.socket).o.scale  # ty: ignore[invalid-return-type]

    def determinant(self) -> _FloatResult:
        """Compute the determinant of a matrix input and return as a `FloatSocket`."""
        self._assert_output("determinant")
        from ..nodes.geometry import MatrixDeterminant

        return MatrixDeterminant._find_or_create_linked(self.socket).o.determinant  # ty: ignore[invalid-return-type]

    def invert(self) -> Self:
        """Invert the `MatrixSocet` and return a `MatrixSocket`."""
        self._assert_output("invert")
        from ..nodes.geometry import InvertMatrix

        return InvertMatrix._find_or_create_linked(self.socket).o.matrix  # ty: ignore[invalid-return-type]

    def transpose(self) -> Self:
        """Transpose the `MatrixSocket` and return a `MatrixSocket`."""
        self._assert_output("transpose")
        from ..nodes.geometry import TransposeMatrix

        return TransposeMatrix._find_or_create_linked(self.socket).o.matrix  # ty: ignore[invalid-return-type]

    def svd(self) -> ResultMatrixSVD[_MatrixResult, _VectorResult]:
        """Decompose the matrix via SVD. Returns `(u, s, v)`."""
        self._assert_output("svd")
        from ..nodes.geometry import MatrixSVD

        o = MatrixSVD(self.socket).o
        return ResultMatrixSVD(o.u, o.s, o.v)  # ty: ignore[invalid-return-type]

    def transform_direction(self, direction: InputVector) -> _VectorResult:
        """Apply this matrix to *direction*, ignoring translation.

        Use this instead of ``transform()`` when transforming a direction vector
        (e.g. a normal) where translation must not affect the result.
        """
        self._assert_output("transform_direction")
        from ..nodes.geometry import TransformDirection

        return TransformDirection(direction, self.socket).o.direction  # ty: ignore[invalid-return-type]

    @staticmethod
    def _cast_to_matrix(value) -> MatrixSocket:
        from ..nodes.geometry.converter import CombineMatrix

        if hasattr(value, "shape") and value.shape == (4, 4):
            return CombineMatrix(*value.ravel()).o.matrix
        else:
            return value

    @overload
    def __matmul__(self, other: MatrixSocket) -> _MatrixResult: ...
    @overload
    def __matmul__(self, other: RotationSocket) -> _RotationResult: ...
    @overload
    def __matmul__(self, other: Position) -> _VectorResult: ...
    @overload
    def __matmul__(self, other: VectorSocket) -> _VectorResult: ...
    @overload
    def __matmul__(self, other: Vector) -> _VectorResult: ...
    def __matmul__(self, other: Any) -> Self | _VectorResult:
        from ..nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket

        if socket.type == "MATRIX" and _output_socket_type(other) == "VECTOR":
            return TransformPoint(other, socket).o.vector  # ty: ignore[invalid-return-type]

        return MultiplyMatrices(socket, other).o.matrix  # ty: ignore[invalid-return-type]

    def __rmatmul__(self, other: MatrixSocket | MatrixSocketList) -> Self:
        from ..nodes.geometry.converter import MultiplyMatrices, TransformPoint

        other = self._cast_to_matrix(other)
        socket = self._default_output_socket

        if socket.type == "VECTOR" and _output_socket_type(other) == "MATRIX":
            return TransformPoint(socket, other).o.vector  # ty: ignore[invalid-return-type]

        return MultiplyMatrices(other, socket).o.matrix  # ty: ignore[invalid-return-type]


# ---------------------------------------------------------------------------
# Structural mixins (lists, default values, type conversions)
# ---------------------------------------------------------------------------


class _ListMixin(Socket, Generic[_T]):
    """Generic list mixin for socket lists."""

    def list_length(self) -> "IntegerSocket":
        """Get the length of the list."""
        from ..nodes.geometry import ListLength

        return ListLength(self.socket, data_type=self._socket_dtype).o.length  # ty: ignore[invalid-argument-type]

    @overload
    def get(self, index: InputIntegerList) -> Self: ...

    @overload
    def get(self, index: InputInteger) -> _T: ...

    def get(self, index: InputInteger | InputIntegerList) -> _T | Self:
        """Get the item at the given index from the list."""
        from ..nodes.geometry import GetListItem

        return GetListItem(  # ty: ignore[invalid-return-type]
            list=self.socket,
            index=index,
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.value

    def filter(self, selection: InputBoolean | BooleanSocketList = True) -> Self:
        """Filter the list based on the selection."""
        from ..nodes.geometry import FilterList

        return FilterList(
            self.socket,
            selection=selection,
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.selection  # ty: ignore[invalid-return-type]

    def sort(
        self,
        sort_weight: InputFloat | InputFloatList,
        group_id: InputInteger | IntegerSocket = None,
        selection: InputBoolean | BooleanSocketList = None,
    ) -> Self:
        """Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

        Parameters
        ----------
        sort_weight : InputFloat | InputFloatList
            The weight to sort by.
        group_id : InputInteger | IntegerSocket, optional
            The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID.
        selection : InputBoolean | BooleanSocketList, optional
            The selection to sort by. If False then an element is not included in the sort and remains in its original position.

        Returns
        -------
        Self
            The sorted list.
        """
        from ..nodes.geometry import SortList

        return SortList(
            self.socket,
            selection=selection,
            group_id=group_id,
            sort_weight=sort_weight,
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.list  # ty: ignore[invalid-return-type]

    def reverse(self) -> Self:
        """Reverse the list. Currently uses a SortList node with negative Index to reverse the list."""
        from ..nodes.geometry import Index, SortList

        return SortList(
            list=self.socket,
            sort_weight=Index().o.index.negate(),
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.list  # ty: ignore[invalid-return-type]

    def list_slice(
        self, start: InputInteger = 0, stop: InputInteger = None, step: InputInteger = 1
    ) -> Self:
        """Slice the list using start, stop, and step indices. Behaves like Python's slice notation."""
        from ..nodes.geometry.converter import GetListItem
        from ..nodes.geometry.groups import SliceToIndices

        if stop is None:
            stop = self.list_length()
        elif isinstance(stop, int):
            if stop < 0:
                stop = self.list_length() + stop

        if start is None:
            start = 0
        elif isinstance(start, int):
            if start < 0:
                start = self.list_length() + start

        if step is None:
            step = 1

        indices = SliceToIndices(start=start, stop=stop, step=step).o.indices
        return GetListItem(  # ty: ignore[invalid-return-type]
            self.socket,
            indices,
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.value

    @overload
    def __getitem__(self, key: int) -> _T: ...
    @overload
    def __getitem__(self, key: IntegerSocketList) -> Self: ...
    @overload
    def __getitem__(self, key: slice) -> Self: ...
    def __getitem__(self, key: int | IntegerSocketList | slice) -> _T:
        from ..nodes.geometry.converter import GetListItem

        if isinstance(key, slice):
            return self.list_slice(key.start, key.stop, key.step)  # ty: ignore[invalid-return-type]

        return GetListItem(
            self.socket,
            index=key,
            socket_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.value  # ty: ignore[invalid-return-type]

    def __len__(self) -> IntegerSocket:
        from ..nodes.geometry.converter import ListLength

        return ListLength(
            self.socket,
            data_type=self._socket_dtype,  # ty: ignore[invalid-argument-type]
        ).o.length


class _DefaultValueMixin(BaseSocket, Generic[_T]):
    @property
    def default_value(self) -> _T:
        """Get or set the default value of the socket. Only relevant for input sockets."""
        self._assert_input("default_value")
        return self.socket.default_value  # ty: ignore[unresolved-attribute]

    @default_value.setter
    def default_value(self, value: _T) -> None:
        """Get or set the default value of the socket. Only relevant for input sockets."""
        self._assert_input("default_value")
        self.socket.default_value = value  # ty: ignore[unresolved-attribute]


class _ToListMixin(BaseSocket, Generic[_T]):
    def to_list(self, count: InputInteger = 10) -> _T:
        """Create a list of elements, evaluating this field `count` times based on the `Index` node."""
        from ..nodes.geometry import FieldToList

        return FieldToList(count, {self.name: self}).o[0]  # ty: ignore[invalid-return-type, invalid-argument-type]


class _FloatConvertDatatypeMixin(BaseSocket, Generic[_IntegerResult, _StringResult]):
    def to_string(self, decimals: InputInteger = 0) -> "_StringResult":
        "Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places"
        self._assert_output("to_string")
        from ..nodes.geometry import ValueToString

        return ValueToString.float(self.socket, decimals).o.string  # ty: ignore[invalid-return-type]

    def to_integer(
        self, rounding_mode: Literal["ROUND", "FLOOR", "CEILING", "TRUNCATE"] = "ROUND"
    ) -> "_IntegerResult":
        "Convert the `FloatSocket` to an `IntegerSocket` by truncating the decimal part."
        self._assert_output("to_integer")
        from ..nodes.geometry import FloatToInteger

        return FloatToInteger(self.socket, rounding_mode=rounding_mode).o.integer  # ty: ignore[invalid-return-type]


class _IntegerConvertDatatypeMixin(Socket, Generic[_StringResult]):
    def to_string(self) -> _StringResult:
        "Convert the `IntegerSocket` to a `StringSocket`."
        self._assert_output("to_string")
        from ..nodes.geometry import ValueToString

        return ValueToString.integer(self.socket).o.string  # ty: ignore[invalid-return-type]


# ---------------------------------------------------------------------------
# Concrete socket classes (registry targets)
#
# Selected at runtime by ``_wrap_socket()``. The matching Socket* classes in
# interface.py inherit the same mixins, so interface sockets behave identically.
# ---------------------------------------------------------------------------


# -- Float --
class FloatSocket(
    _FloatMixin["IntegerSocket"],
    _ToListMixin["FloatSocketList"],
    _FloatConvertDatatypeMixin["IntegerSocket", "StringSocket"],
    _DefaultValueMixin[float],
    Socket,
):
    """Runtime float socket wrapper."""

    @property
    def point(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "point")

    @property
    def edge(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "edge")

    @property
    def face(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "face")

    @property
    def corner(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "corner")

    @property
    def spline(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "spline")

    @property
    def instance(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "instance")

    @property
    def layer(self) -> "_StatsField[FloatSocket]":
        """FloatSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "float", "layer")


class FloatSocketList(
    _FloatMixin["IntegerSocketList"],
    _FloatConvertDatatypeMixin["IntegerSocketList", "StringSocketList"],
    _ListMixin[FloatSocket],
):
    """"""


class FloatSocketGrid(
    _FloatMixin["IntegerSocketGrid"],
    _GridSocketMixin[FloatSocket],
    _FloatGridOperatorMixin,
    _GridMeanMixin,
):
    """Runtime float grid socket wrapper."""


# -- Vector --
class VectorSocket(
    _VectorMixin[
        "FloatSocket",
        "VectorSocket",
        "RotationSocket",
    ],
    _ToListMixin["VectorSocketList"],
    Socket,
):
    """Runtime vector socket wrapper."""

    @property
    def default_value(self) -> list[float]:
        return list(self.socket.default_value)

    @default_value.setter
    def default_value(self, value: list[float] | tuple[float, float, float]) -> None:
        self.socket.default_value = value

    @property
    def point(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "point")

    @property
    def edge(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "edge")

    @property
    def face(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "face")

    @property
    def corner(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "corner")

    @property
    def spline(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "spline")

    @property
    def instance(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "instance")

    @property
    def layer(self) -> "_StatsField[VectorSocket]":
        """VectorSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`."""
        return _StatsField(self.socket, "vector", "layer")


class VectorSocketList(
    _VectorMixin["FloatSocketList", "VectorSocketList", "RotationSocketList"],
    _ListMixin[VectorSocket],
):
    """"""


class VectorSocketGrid(
    _VectorMixin,
    _GridSocketMixin[VectorSocket],
    _VectorGridOperatorMixin,
    _GridMeanMixin,
):
    """Runtime vector grid socket wrapper."""


# -- Color --
class ColorSocket(_ColorMixin, _ToListMixin["ColorSocketList"], Socket):
    """Runtime color socket wrapper."""


class ColorSocketList(ColorSocket, _ListMixin[ColorSocket]):
    """List of color sockets."""


# -- Integer --
class IntegerSocket(
    _IntegerMixin[FloatSocket],
    _ToListMixin["IntegerSocketList"],
    _IntegerConvertDatatypeMixin["StringSocket"],
    _DefaultValueMixin[int],
    Socket,
):
    """Runtime integer socket wrapper."""

    @property
    def point(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "point")

    @property
    def edge(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "edge")

    @property
    def face(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "face")

    @property
    def corner(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "corner")

    @property
    def spline(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "spline")

    @property
    def instance(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "instance")

    @property
    def layer(self) -> "_MinMaxField[IntegerSocket]":
        """IntegerSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`."""
        return _MinMaxField(self.socket, "integer", "layer")


class IntegerSocketList(
    _IntegerMixin["FloatSocket"],
    _IntegerConvertDatatypeMixin["StringSocket"],
    _ListMixin[IntegerSocket],
):
    """List of integer sockets."""


class IntegerVectorSocket(
    _IntegerMixin["FloatSocket"],
    _DefaultValueMixin[list[int]],
    Socket,
):
    """Runtime integer vector socket wrapper."""


class IntegerSocketGrid(_IntegerMixin, _GridSocketMixin[IntegerSocket], _GridMeanMixin):
    """Runtime integer grid socket wrapper."""


# -- Boolean --
class BooleanSocket(
    _BooleanMixin, _ToListMixin["BooleanSocketList"], _DefaultValueMixin[bool], Socket
):
    """Runtime boolean socket wrapper."""

    @property
    def point(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""

        return _EvaluateField(self.socket, "boolean", "point")

    @property
    def edge(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "edge")

    @property
    def face(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "face")

    @property
    def corner(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "corner")

    @property
    def spline(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "spline")

    @property
    def instance(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "instance")

    @property
    def layer(self) -> "_EvaluateField[BooleanSocket]":
        """BooleanSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "boolean", "layer")


class BooleanSocketList(_BooleanMixin, _ListMixin[BooleanSocket]):
    """List of boolean sockets."""


class BooleanSocketGrid(_BooleanMixin, _GridSocketMixin[BooleanSocket]):
    """Runtime boolean grid socket wrapper."""


# -- Rotation --
class RotationSocket(
    _RotationMixin["FloatSocket", "VectorSocket"],
    _ToListMixin["RotationSocketList"],
    _DefaultValueMixin[Euler],
    Socket,
):
    """Runtime rotation socket wrapper."""

    @property
    def point(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "point")

    @property
    def edge(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "edge")

    @property
    def face(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "face")

    @property
    def corner(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "corner")

    @property
    def spline(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "spline")

    @property
    def instance(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "instance")

    @property
    def layer(self) -> "_EvaluateField[RotationSocket]":
        """RotationSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`."""
        return _EvaluateField(self.socket, "quaternion", "layer")


class RotationSocketList(
    _RotationMixin["FloatSocketList", "VectorSocketList"], _ListMixin[RotationSocket]
):
    """List of rotation sockets."""


# -- Matrix --
class MatrixSocket(
    _MatrixMixin[VectorSocket, RotationSocket, FloatSocket, "MatrixSocket"],
    _ToListMixin["MatrixSocketList"],
    Socket,
):
    """Runtime matrix socket wrapper."""

    @property
    def point(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "point")

    @property
    def edge(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "edge")

    @property
    def face(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "face")

    @property
    def corner(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "corner")

    @property
    def spline(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "spline")

    @property
    def instance(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "instance")

    @property
    def layer(self) -> "_AccumulateField[MatrixSocket]":
        """MatrixSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`."""
        return _AccumulateField(self.socket, "matrix", "layer")

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
            for i in node.o:
                yield cast(FloatSocket, i)
        else:
            node = CombineMatrix._find_or_create_linked(self.socket)
            for i in node.i:
                yield cast(FloatSocket, i)

    def __len__(self) -> int:
        return 16


class MatrixSocketList(
    _MatrixMixin[
        VectorSocketList, RotationSocketList, FloatSocketList, "MatrixSocketList"
    ],
    _ListMixin[MatrixSocket],
):
    """List of matrix sockets."""


# -- String --
class StringSocket(
    _StringMixin["StringSocket", "BooleanSocket", IntegerSocket],
    _ToListMixin["StringSocketList"],
    _DefaultValueMixin[str],
    Socket,
):
    """Runtime string socket wrapper."""

    def split(self, separator: InputString = "") -> "StringSocketList":
        from ..nodes.geometry import SplitString

        return SplitString(self.socket, separator=separator).o.list

    def join(
        self, strings: Iterable[str | "StringSocket" | NodeSocketString | BaseNode]
    ) -> "StringSocket":
        """Join the input strings with this as the separator."""
        self._assert_output("join")
        from ..nodes.geometry import JoinStrings

        return JoinStrings(strings, self.socket).o.string

    def __add__(self, other: "StringSocket" | str) -> "StringSocket":
        self._assert_output("+")
        from ..nodes.geometry import JoinStrings, String

        if isinstance(other, str):
            other = String(other).o.string

        return JoinStrings((self.socket, other)).o.string

    def __radd__(self, other: str | "StringSocket") -> "StringSocket":
        self._assert_output("+")
        from ..nodes.geometry import JoinStrings, String

        if isinstance(other, str):
            other = String(other).o.string

        return JoinStrings((other, self.socket)).o.string


class StringSocketList(
    _StringMixin["StringSocketList", "BooleanSocketList", "IntegerSocketList"],
    _ListMixin[StringSocket],
):
    """List of string sockets."""


# -- Menu --
class _MenuSocketMixin(Socket):
    socket: NodeSocketMenu


class MenuSocket(_MenuSocketMixin, _ToListMixin["MenuSocketList"]):
    """Runtime menu socket wrapper."""

    @property
    def default_value(self) -> str:
        return self.socket.default_value

    @default_value.setter
    def default_value(self, value: str) -> None:
        self.socket.default_value = value


class MenuSocketList(_MenuSocketMixin, _ListMixin[MenuSocket]):
    """List of menu sockets."""


# -- Geometry --
class GeometrySocket(Socket):
    """Runtime geometry socket wrapper."""

    socket: NodeSocketGeometry

    def realize_instances(
        self,
        selection: InputBoolean = True,
        realize_all: InputBoolean = False,
        depth: InputInteger = 0,
    ) -> "GeometrySocket":
        from ..nodes.geometry import RealizeInstances

        return RealizeInstances(
            self.socket,
            selection=selection,
            realize_all=realize_all,
            depth=depth,
        ).o.geometry


class GeometrySocketList(GeometrySocket, _ListMixin[GeometrySocket]):
    """List of geometry sockets."""


# -- Data-block and opaque sockets (object, material, image, …) --
class _ObjectMixin(Socket):
    socket: NodeSocketObject


class ObjectSocket(_ObjectMixin, _DefaultValueMixin[bpy.types.Object]):
    """Runtime object socket wrapper."""

    @property
    def _info(self) -> "type[ObjectInfo]":
        from ..nodes.geometry import ObjectInfo

        return ObjectInfo

    def transform(
        self, transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL"
    ) -> "MatrixSocket":
        """The Object's transform matrix, optionally in relative space.

        Adds [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo) to the node tree and returns.

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The space in which to return the transform matrix.

        Returns
        -------
        MatrixSocket
            The output 'Transform' `MatrixSocket`.
        """
        return self._info(self.socket, transform_space=transform_space).o.transform

    def location(
        self, transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL"
    ) -> "VectorSocket":
        """
        The object's location, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The space in which to return the location.

        Returns
        -------
        VectorSocket
            The output 'Location' `VectorSocket`.

        """
        return self._info(self.socket, transform_space=transform_space).o.location

    def rotation(
        self, transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL"
    ) -> "RotationSocket":
        """
        The object's rotation, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The space in which to return the rotation.

        Returns
        -------
        RotationSocket
            The output 'Rotation' `RotationSocket`.
        """
        return self._info(self.socket, transform_space=transform_space).o.rotation

    def scale(
        self, transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL"
    ) -> "VectorSocket":
        """
        The object's scale, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The space in which to return the scale.

        Returns
        -------
        VectorSocket
            The output 'Scale' `VectorSocket`.
        """
        return self._info(self.socket, transform_space=transform_space).o.scale

    def geometry(
        self,
        transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL",
        as_instance: InputBoolean = False,
    ) -> "GeometrySocket":
        """
        The object's geometry, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The space in which to return the geometry.
        as_instance : InputBoolean
            Whether to return the geometry as an instance.

        Returns
        -------
        GeometrySocket
            The output 'Geometry' `GeometrySocket`.
        """
        return self._info(
            self.socket, as_instance=as_instance, transform_space=transform_space
        ).o.geometry


class ObjectSocketList(_ObjectMixin, _ListMixin[ObjectSocket]):
    """List of object sockets."""


class _MaterialSocketMixin(Socket):
    socket: NodeSocketMaterial


class MaterialSocket(_MaterialSocketMixin, _DefaultValueMixin[bpy.types.Material]):
    """Runtime material socket wrapper."""


class MaterialSocketList(_MaterialSocketMixin, _ListMixin[MaterialSocket]):
    """List of material sockets."""


class _ImageSocketMixin(Socket):
    socket: NodeSocketImage


class ImageSocket(_ImageSocketMixin, _DefaultValueMixin[bpy.types.Image]):
    """Runtime image socket wrapper."""


class ImageSocketList(_ImageSocketMixin, _ListMixin[ImageSocket]):
    """List of image sockets."""


class _CollectionSocketMixin(Socket):
    socket: NodeSocketCollection


class CollectionSocket(
    _CollectionSocketMixin, _DefaultValueMixin[bpy.types.Collection]
):
    """Runtime collection socket wrapper."""

    def instances(
        self,
        transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL",
        separate_children: InputBoolean = False,
        reset_children: InputBoolean = False,
    ) -> "GeometrySocket":
        """Import objects from the collection as instances.

        Parameters
        ----------
        transform_space : Literal["ORIGINAL", "RELATIVE"]
            The transform space to use for the instances.
        separate_children : bool
            Whether to separate objects as their own instances.
        reset_children : bool
            Whether to reset children of the collection to world origin.

        Returns
        -------
        GeometrySocket
            The output 'Instances' `GeometrySocket`. Will be a single instance or multiple instances if `separate_children` is `True`.

        """
        from ..nodes.geometry import CollectionInfo

        return CollectionInfo(
            self.socket,
            separate_children,
            reset_children,
            transform_space=transform_space,
        ).o.instances


class CollectionSocketList(_CollectionSocketMixin, _ListMixin[CollectionSocket]):
    """List of collection sockets."""


class _BundleSocketMixin(Socket):
    socket: NodeSocketBundle


class BundleSocket(_BundleSocketMixin):
    """Runtime bundle socket wrapper."""


class BundleSocketList(_BundleSocketMixin, _ListMixin[BundleSocket]):
    """List of bundle sockets."""


class _ClosureSocketMixin(Socket):
    socket: NodeSocketClosure


class ClosureSocket(_ClosureSocketMixin):
    """Runtime closure socket wrapper."""


class ClosureSocketList(_ClosureSocketMixin, _ListMixin[ClosureSocket]):
    """List of closure sockets."""


class _ShaderSocketMixin(Socket):
    socket: NodeSocketShader


class ShaderSocket(_ShaderSocketMixin):
    """Runtime shader socket wrapper."""


class ShaderSocketList(_ShaderSocketMixin, _ListMixin[ShaderSocket]):
    """List of shader sockets."""


class _FontSocketMixin(Socket):
    socket: NodeSocketFont


class FontSocket(_FontSocketMixin):
    """Runtime font socket wrapper."""


class FontSocketList(_FontSocketMixin, _ListMixin[FontSocket]):
    """List of font sockets."""


class _SoundSocketMixin(Socket):
    socket: NodeSocketSound


class SoundSocket(_SoundSocketMixin):
    """Runtime sound socket wrapper."""


class SoundSocketList(_SoundSocketMixin, _ListMixin[SoundSocket]):
    """List of sound sockets."""


# ---------------------------------------------------------------------------
# Registry registration (bl_idname -> socket class)
# ---------------------------------------------------------------------------

_SOCKET_REGISTRY["NodeSocketFloat"] = FloatSocket
_SOCKET_REGISTRY["NodeSocketVector"] = VectorSocket
_SOCKET_REGISTRY["NodeSocketColor"] = ColorSocket
_SOCKET_REGISTRY["NodeSocketInt"] = IntegerSocket
_SOCKET_REGISTRY["NodeSocketIntVector3D"] = IntegerVectorSocket
_SOCKET_REGISTRY["NodeSocketBool"] = BooleanSocket
_SOCKET_REGISTRY["NodeSocketRotation"] = RotationSocket
_SOCKET_REGISTRY["NodeSocketMatrix"] = MatrixSocket
_SOCKET_REGISTRY["NodeSocketString"] = StringSocket
_SOCKET_REGISTRY["NodeSocketMenu"] = MenuSocket
_SOCKET_REGISTRY["NodeSocketGeometry"] = GeometrySocket
_SOCKET_REGISTRY["NodeSocketObject"] = ObjectSocket
_SOCKET_REGISTRY["NodeSocketMaterial"] = MaterialSocket
_SOCKET_REGISTRY["NodeSocketImage"] = ImageSocket
_SOCKET_REGISTRY["NodeSocketSound"] = SoundSocket
_SOCKET_REGISTRY["NodeSocketFont"] = FontSocket
_SOCKET_REGISTRY["NodeSocketCollection"] = CollectionSocket
_SOCKET_REGISTRY["NodeSocketBundle"] = BundleSocket
_SOCKET_REGISTRY["NodeSocketClosure"] = ClosureSocket
_SOCKET_REGISTRY["NodeSocketShader"] = ShaderSocket

_SOCKET_LIST_REGISTRY["NodeSocketFloat"] = FloatSocketList
_SOCKET_LIST_REGISTRY["NodeSocketVector"] = VectorSocketList
_SOCKET_LIST_REGISTRY["NodeSocketColor"] = ColorSocketList
_SOCKET_LIST_REGISTRY["NodeSocketInt"] = IntegerSocketList
_SOCKET_LIST_REGISTRY["NodeSocketBool"] = BooleanSocketList
_SOCKET_LIST_REGISTRY["NodeSocketRotation"] = RotationSocketList
_SOCKET_LIST_REGISTRY["NodeSocketMatrix"] = MatrixSocketList
_SOCKET_LIST_REGISTRY["NodeSocketString"] = StringSocketList
_SOCKET_LIST_REGISTRY["NodeSocketMenu"] = MenuSocketList
_SOCKET_LIST_REGISTRY["NodeSocketGeometry"] = GeometrySocketList
_SOCKET_LIST_REGISTRY["NodeSocketObject"] = ObjectSocketList
_SOCKET_LIST_REGISTRY["NodeSocketImage"] = ImageSocketList
_SOCKET_LIST_REGISTRY["NodeSocketCollection"] = CollectionSocketList
_SOCKET_LIST_REGISTRY["NodeSocketBundle"] = BundleSocketList
_SOCKET_LIST_REGISTRY["NodeSocketShader"] = ShaderSocketList
_SOCKET_LIST_REGISTRY["NodeSocketFont"] = FontSocketList
_SOCKET_LIST_REGISTRY["NodeSocketSound"] = SoundSocketList

_SOCKET_GRID_REGISTRY["NodeSocketFloat"] = FloatSocketGrid
_SOCKET_GRID_REGISTRY["NodeSocketVector"] = VectorSocketGrid
_SOCKET_GRID_REGISTRY["NodeSocketInt"] = IntegerSocketGrid
_SOCKET_GRID_REGISTRY["NodeSocketBool"] = BooleanSocketGrid
