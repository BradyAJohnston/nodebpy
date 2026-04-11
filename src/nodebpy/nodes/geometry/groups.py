from ...builder import (
    IntegerSocketLinker,
    NodeGroupBuilder,
    SocketInt,
    SocketVector,
    VectorSocketLinker,
)
from ...types import InputInteger, InputVector
from . import EdgesOfVertex, EdgeVertices, EvaluateAtIndex, Switch


class OtherVertex(NodeGroupBuilder):
    """
    Given a vertex and an edge number from that vertex, returns the other
    vertex of that edge.
    """

    _name = "Other Vertex"
    _color_tag = "INPUT"

    i_vertex_index: IntegerSocketLinker
    i_edge_number: IntegerSocketLinker
    o_other_vertex: IntegerSocketLinker

    def __init__(
        self, vertex_index: InputInteger = None, edge_number: InputInteger = 0
    ):
        kwargs = {"Vertex Index": vertex_index, "Edge Number": edge_number}
        super().__init__(**kwargs)

    @classmethod
    def _build_group(cls, tree):
        with tree.inputs:
            vertex_index = SocketInt("Vertex Index", default_input="INDEX")
            edge_number = SocketInt("Edge Number")

        eov = EdgesOfVertex(vertex_index, sort_index=edge_number)
        ev = EdgeVertices()
        vert_1 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_1, eov)
        vert_2 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_2, eov)
        switch = (vert_1 != vertex_index) >> Switch.integer(..., vert_1, vert_2)

        with tree.outputs:
            _ = switch >> SocketInt("Other Vertex")


class OffsetVector(NodeGroupBuilder):
    """
    Evaluate a given vector field at an offset to the current `Index`.
    """

    _name = "Offset Vector"
    _color_tag = "INPUT"

    i_index: IntegerSocketLinker
    i_vector: VectorSocketLinker
    i_offset: IntegerSocketLinker
    o_vector: VectorSocketLinker

    def __init__(
        self,
        index: InputInteger = None,
        vector: InputVector = None,
        offset: InputInteger = 0,
    ):
        super().__init__(index=index, vector=vector, offset=offset)

    @classmethod
    def _build_group(cls, tree):
        with tree.inputs:
            index = SocketInt("Index", default_input="INDEX")
            vector = SocketVector("Vector", default_input="POSITION")
            offset = SocketInt("Offset")

        value = EvaluateAtIndex.point.vector(vector, index + offset)

        with tree.outputs:
            _ = value >> SocketVector("Vector")
