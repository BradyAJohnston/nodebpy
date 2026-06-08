from typing import TYPE_CHECKING

from nodebpy import TreeBuilder

from ...builder import (
    BooleanIn,
    BooleanOut,
    CustomGeometryGroup,
    IntegerIn,
    IntegerListOut,
    IntegerOut,
    ObjectIn,
    RotationOut,
    VectorIn,
    VectorOut,
)
from . import (
    AxesToRotation,
    CombineMatrix,
    CombineXYZ,
    EdgesOfVertex,
    EdgeVertices,
    Frame,
    Position,
    Switch,
    IntegerMath,
    FieldToList,
    Index,
)


class SliceToIndices(CustomGeometryGroup):
    """
    Converts a python slice to a list of indices.
    """

    _name = "Slice to Indices"
    _color_tag = "CONVERTER"

    start: IntegerIn = IntegerIn()
    stop: IntegerIn = IntegerIn()
    step: IntegerIn = IntegerIn(1)

    class _Outputs:
        indices: IntegerListOut = IntegerListOut(structure_type="LIST")

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def _build_group(self, tree: TreeBuilder) -> None:
        range = self.i.stop - self.i.start
        length = IntegerMath.divide_ceiling(range, self.i.step).o.value.abs()
        indices = FieldToList(length).integer((self.i.start + self.i.step) * Index())

        indices >> self.o.indices


class OtherVertex(CustomGeometryGroup):
    """
    Given a vertex and an edge number from that vertex, returns the other
    vertex of that edge.
    """

    _name = "Other Vertex"
    _color_tag = "INPUT"

    vertex_index: IntegerIn = IntegerIn(
        default_input="INDEX", doc="The vertex to start from."
    )
    edge_number: IntegerIn = IntegerIn(0, doc="Which edge of that vertex to traverse.")

    class _Outputs:
        other_vertex: IntegerOut = IntegerOut(
            doc="The vertex at the other end of the selected edge."
        )

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def _build_group(self, tree: TreeBuilder):
        edge_index = EdgesOfVertex(
            self.i.vertex_index, sort_index=self.i.edge_number
        ).o.edge_index
        edge_vertices = EdgeVertices()
        v1 = edge_vertices.o.vertex_index_1.edge.at(edge_index)
        v2 = edge_vertices.o.vertex_index_2.edge.at(edge_index)

        Switch.integer(self.i.vertex_index == v1, v1, v2) >> self.o.other_vertex


class OffsetVector(CustomGeometryGroup):
    """
    Evaluate a given vector field at an offset to the current ``Index``.
    """

    _name = "Offset Vector"
    _color_tag = "INPUT"

    index: IntegerIn = IntegerIn(
        default_input="INDEX", doc="The base index to evaluate at."
    )
    vector: VectorIn = VectorIn(
        default_input="POSITION", doc="The vector field to sample."
    )
    offset: IntegerIn = IntegerIn(
        0, doc="Integer offset added to the index before sampling."
    )

    class _Outputs:
        vector: VectorOut = VectorOut(doc="The vector value at ``index + offset``.")

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def _build_group(self, tree: TreeBuilder):
        value = self.i.vector.point.at(self.i.index + self.i.offset)

        value >> self.o.vector


class PrincipalComponents(CustomGeometryGroup):
    """
    Compute PCA on a given vector field.
    """

    _name = "Principal Components"
    _color_tag = "INPUT"

    position: VectorIn = VectorIn(default_input="POSITION")
    group_id: IntegerIn = IntegerIn(
        name="Group ID",
        doc="An index used to group values together for multiple separate operations",
        hide_value=True,
    )

    class _Outputs:
        centroid: VectorOut = VectorOut()
        principal_components: VectorOut = VectorOut(
            doc="Variance of the data along each principal axis"
        )
        rotation: RotationOut = RotationOut(
            doc="Rotation that defines the principal component basis"
        )
        longest_axis: VectorOut = VectorOut(panel="Principal Axes", panel_closed=True)
        intermediate_axis: VectorOut = VectorOut(panel="Principal Axes")
        shortest_axis: VectorOut = VectorOut(panel="Principal Axes")

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def _build_group(self, tree: TreeBuilder):
        tree.collapse = True
        position = self.i.position
        group_id = self.i.group_id

        with Frame("Centroid"):
            centroid = position.point.mean(group_id)
            centroid >> self.o.centroid

        with Frame("Covariance Matrix"):
            diff = position - centroid
            matrix = CombineMatrix()

            for i, axis1 in enumerate(diff):
                mean = (diff * axis1).point.mean(group_id)
                for j, axis2 in enumerate(mean):
                    axis2 >> matrix.i[int(i * 4 + j)]

        with Frame("SVD"):
            u, s, v = matrix.o.matrix.svd()
            s >> self.o.principal_components
            long, inter, short = [CombineXYZ(*u[i * 4 : (i * 4) + 3]) for i in range(3)]
            long >> self.o.longest_axis
            short >> self.o.shortest_axis
            AxesToRotation(long, short) >> self.o.rotation
            inter * u.determinant().sign() >> self.o.intermediate_axis


class ClipFieldToBox(CustomGeometryGroup):
    _name = "Clip Field to Box"

    box_object: ObjectIn = ObjectIn(optional_label=True)
    invert: BooleanIn = BooleanIn(False)

    class _Outputs:
        clipped_field: BooleanOut = BooleanOut()

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

    def _build_group(self, tree: TreeBuilder):
        pos = Position().o.position
        local_pos = self.i.box_object.transform("RELATIVE").invert() @ pos * 0.5
        result = abs(local_pos) < 0.5
        (result != self.i.invert) >> self.o.clipped_field
