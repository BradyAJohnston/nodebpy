from typing import TYPE_CHECKING

from nodebpy import TreeBuilder
from nodebpy.nodes.compositor import CombineXYZ
from nodebpy.types import InputInteger, InputVector

from ...builder import (
    IntegerSocket,
    NodeGroupBuilder,
    RotationSocket,
    SocketAccessor,
    VectorSocket,
)
from . import (
    AxesToRotation,
    CombineMatrix,
    EdgesOfVertex,
    EdgeVertices,
    EvaluateAtIndex,
    FieldAverage,
    Frame,
    Math,
    MatrixSVD,
    Switch,
)


class OtherVertex(NodeGroupBuilder):
    """
    Given a vertex and an edge number from that vertex, returns the other
    vertex of that edge.
    """

    _name = "Other Vertex"
    _color_tag = "INPUT"

    class _Inputs(SocketAccessor):
        vertex_index: IntegerSocket
        """The vertex to start from."""
        edge_number: IntegerSocket
        """Which edge of that vertex to traverse."""

    class _Outputs(SocketAccessor):
        other_vertex: IntegerSocket
        """The vertex at the other end of the selected edge."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self, vertex_index: InputInteger = None, edge_number: InputInteger = 0
    ):
        kwargs = {"Vertex Index": vertex_index, "Edge Number": edge_number}
        super().__init__(**kwargs)

    @classmethod
    def _build_group(cls, tree):
        vertex_index = tree.inputs.integer("Vertex Index", default_input="INDEX")
        edge_number = tree.inputs.integer("Edge Number")

        eov = EdgesOfVertex(vertex_index, sort_index=edge_number)
        ev = EdgeVertices()
        vert_1 = EvaluateAtIndex.edge.integer(ev.o.vertex_index_1, eov)
        vert_2 = EvaluateAtIndex.edge.integer(ev.o.vertex_index_2, eov)
        switch = (vert_1 != vertex_index) >> Switch.integer(..., vert_1, vert_2)

        _ = switch >> tree.outputs.integer("Other Vertex")


class OffsetVector(NodeGroupBuilder):
    """
    Evaluate a given vector field at an offset to the current ``Index``.
    """

    _name = "Offset Vector"
    _color_tag = "INPUT"

    class _Inputs(SocketAccessor):
        index: IntegerSocket
        """The base index to evaluate at."""
        vector: VectorSocket
        """The vector field to sample."""
        offset: IntegerSocket
        """Integer offset added to the index before sampling."""

    class _Outputs(SocketAccessor):
        vector: VectorSocket
        """The vector value at ``index + offset``."""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        index: InputInteger = None,
        vector: InputVector = None,
        offset: InputInteger = 0,
    ):
        super().__init__(index=index, vector=vector, offset=offset)

    @classmethod
    def _build_group(cls, tree):
        index = tree.inputs.integer("Index", default_input="INDEX")
        vector = tree.inputs.vector("Vector", default_input="POSITION")
        offset = tree.inputs.integer("Offset")

        value = EvaluateAtIndex.point.vector(vector, index + offset)

        _ = value >> tree.outputs.vector("Vector")


class PrincipalComponents(NodeGroupBuilder):
    """
    Compute PCA on a given vector field.
    """

    _name = "Principal Components"
    _color_tag = "INPUT"

    class _Inputs(SocketAccessor):
        position: VectorSocket
        group_id: IntegerSocket

    class _Outputs(SocketAccessor):
        center: VectorSocket
        rotation: RotationSocket
        principal_components: VectorSocket
        longest_axis: VectorSocket
        intermediate_axis: VectorSocket
        shortest_axis: VectorSocket

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        position: InputVector = None,
        group_id: InputInteger = None,
    ):
        kwargs = {
            "Position": position,
            "Group ID": group_id,
        }
        super().__init__(**kwargs)

    def _build_group(self, tree: TreeBuilder):
        tree.collapse = True
        position = tree.inputs.vector("Position", default_input="POSITION")
        group_id = tree.inputs.integer(
            "Group ID",
            description="An index used to group values together for multiple separate operations",
            hide_value=True,
        )
        out_centroid = tree.outputs.vector("Centroid")
        out_princ = tree.outputs.vector(
            "Principal Components",
            description="Variance of the data along each principal axis",
        )
        out_rotation = tree.outputs.rotation(
            "Rotation",
            description="Rotation that defines the principal component basis",
        )
        with tree.outputs.panel("Principal Axes", default_closed=True):
            out_long = tree.outputs.vector("Longest Axis")
            out_inter = tree.outputs.vector("Intermediate Axis")
            out_short = tree.outputs.vector("Shortest Axis")

        with Frame("Centroid"):
            centroid = FieldAverage.point.vector(position, group_id)
            centroid >> out_centroid

        with Frame("Covariance Matrix"):
            diff = position - centroid
            matrix = CombineMatrix()

            for i, axis1 in enumerate(diff.o.vector):
                mean = FieldAverage.point.vector(diff * axis1, group_id)
                for j, axis2 in enumerate(mean.o.mean):
                    axis2 >> matrix.i[int(i * 4 + j)]

        with Frame("SVD"):
            svd = MatrixSVD(matrix)
            svd.o.s >> out_princ
            long, inter, short = [
                CombineXYZ(*svd.o.u[i * 4 : (i * 4) + 3]) for i in range(3)
            ]
            long >> out_long
            short >> out_short
            AxesToRotation(long, short) >> out_rotation
            (inter * Math.sign(svd.o.u.determinant)) >> out_inter
