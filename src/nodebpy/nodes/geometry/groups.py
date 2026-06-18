from typing import TYPE_CHECKING

from ...builder import (
    CustomGeometryGroup,
    IntegerSocket,
    IntegerSocketList,
    RotationSocket,
    SocketAccessor,
    TreeBuilder,
    VectorSocket,
)
from ...types import (
    InputBoolean,
    InputGeometry,
    InputInteger,
    InputObject,
    InputVector,
)
from . import (
    AxesToRotation,
    CaptureAttribute,
    CombineMatrix,
    CombineXYZ,
    EdgesOfVertex,
    EdgeVertices,
    FieldToList,
    Frame,
    Index,
    IntegerMath,
    Position,
    SampleIndex,
    Switch,
)


class SliceToIndices(CustomGeometryGroup):
    """
    Converts a python slice to a list of indices.
    """

    _name = "Slice to Indices"
    _color_tag = "CONVERTER"

    class _Inputs(SocketAccessor):
        start: IntegerSocket
        stop: IntegerSocket
        step: IntegerSocket

    class _Outputs(SocketAccessor):
        indices: IntegerSocketList

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...

        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self, start: InputInteger = 0, stop: InputInteger = 0, step: InputInteger = 1
    ):
        kwargs = {"Start": start, "Stop": stop, "Step": step}
        super().__init__(**kwargs)

    def _build_group(self, tree: TreeBuilder) -> None:
        start = tree.inputs.integer("Start")
        stop = tree.inputs.integer("Stop")
        step = tree.inputs.integer("Step")

        range = stop - start
        length = IntegerMath.divide_ceiling(range, step).o.value.abs()
        indices = FieldToList(length).integer((start + step) * Index())

        indices >> tree.outputs.integer("Indices", structure_type="LIST")


class OtherVertex(CustomGeometryGroup):
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

    def _build_group(self, tree: TreeBuilder):
        vertex_index = tree.inputs.integer("Vertex Index", default_input="INDEX")
        edge_number = tree.inputs.integer("Edge Number")

        edge_index = EdgesOfVertex(vertex_index, sort_index=edge_number).o.edge_index
        edge_vertices = EdgeVertices()
        v1 = edge_vertices.o.vertex_index_1.edge.at(edge_index)
        v2 = edge_vertices.o.vertex_index_2.edge.at(edge_index)
        index = Switch.integer(vertex_index == v1, v1, v2)

        index >> tree.outputs.integer("Other Vertex")


class OffsetVector(CustomGeometryGroup):
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

    def _build_group(self, tree: TreeBuilder):
        index = tree.inputs.integer("Index", default_input="INDEX")
        vector = tree.inputs.vector("Vector", default_input="POSITION")
        offset = tree.inputs.integer("Offset")

        value = vector.point.at(index + offset)

        _ = value >> tree.outputs.vector("Vector")


class PrincipalComponents(CustomGeometryGroup):
    """
    Compute PCA on a given vector field.
    """

    _name = "Principal Components"
    _color_tag = "CONVERTER"

    class _Inputs(SocketAccessor):
        position: VectorSocket
        group_id: IntegerSocket

    class _Outputs(SocketAccessor):
        group_center: VectorSocket
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
        out_centroid = tree.outputs.vector("Group Center")
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
            centroid = position.point.mean(group_id)
            centroid >> out_centroid

        with Frame("Covariance Matrix"):
            diff = position - centroid
            matrix = CombineMatrix()

            for i, axis1 in enumerate(diff):
                mean = (diff * axis1).point.mean(group_id)
                for j, axis2 in enumerate(mean):
                    axis2 >> matrix.i[int(i * 4 + j)]

        with Frame("SVD"):
            u, s, v = matrix.o.matrix.svd()
            s >> out_princ
            long, inter, short = [CombineXYZ(*u[i * 4 : (i * 4) + 3]) for i in range(3)]
            long >> out_long
            short >> out_short
            AxesToRotation(long, short) >> out_rotation
            inter * u.determinant().sign() >> out_inter


class GeometryPrincipalComponents(CustomGeometryGroup):
    _name = "Geometry Principal Components"
    _color_tag = "GEOMETRY"

    class _Inputs:
        geometry: InputGeometry

    class _Outputs(SocketAccessor):
        group_center: VectorSocket
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
        geometry: InputGeometry = None,
        position: InputVector = None,
    ):
        kwargs = {
            "Geometry": geometry,
            "Position": position,
        }
        super().__init__(**kwargs)

    def _build_group(self, tree: TreeBuilder):
        tree.collapse = True
        geo = tree.inputs.geometry("Geometry")
        position = tree.inputs.vector("Position", default_input="POSITION")
        center = tree.outputs.vector("Group Center")
        rotation = tree.outputs.rotation("Rotation")
        principal_components = tree.outputs.vector("Principal Components")
        with tree.outputs.panel("Principal Axes", default_closed=True):
            longest_axis = tree.outputs.vector("Longest Axis")
            intermediate_axis = tree.outputs.vector("Intermediate Axis")
            shortest_axis = tree.outputs.vector("Shortest Axis")

        geo = geo >> CaptureAttribute.point()
        pca = PrincipalComponents(position=geo.capture(position))

        SampleIndex.point.vector(geo, pca.o.group_center) >> center
        SampleIndex.point.quaternion(geo, pca.o.rotation) >> rotation
        (
            SampleIndex.point.vector(geo, pca.o.principal_components)
            >> principal_components
        )
        SampleIndex.point.vector(geo, pca.o.longest_axis) >> longest_axis
        SampleIndex.point.vector(geo, pca.o.intermediate_axis) >> intermediate_axis
        SampleIndex.point.vector(geo, pca.o.shortest_axis) >> shortest_axis


class ClipFieldToBox(CustomGeometryGroup):
    _name = "Clip Field to Box"

    def __init__(
        self,
        box_object: InputObject = None,
        invert: InputBoolean = False,
    ):
        super().__init__(
            **{
                "Box Object": box_object,
                "Invert": invert,
            }
        )

    def _build_group(self, tree: TreeBuilder):
        box = tree.inputs.object("Box Object", optional_label=True)
        invert = tree.inputs.boolean("Invert")
        masked = tree.outputs.boolean("Clipped Field")

        pos = Position().o.position
        local_pos = box.transform("RELATIVE").invert() @ pos * 0.5
        result = abs(local_pos) < 0.5
        (result != invert) >> masked
