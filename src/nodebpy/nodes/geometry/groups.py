from ...builder import (
    IntegerSocket,
    NodeGroupBuilder,
    SocketInteger,
    SocketVector,
    VectorSocket,
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

    i_vertex_index: IntegerSocket
    i_edge_number: IntegerSocket
    o_other_vertex: IntegerSocket

    def __init__(
        self, vertex_index: InputInteger = None, edge_number: InputInteger = 0
    ):
        kwargs = {"Vertex Index": vertex_index, "Edge Number": edge_number}
        super().__init__(**kwargs)

    @classmethod
    def _build_group(cls, tree):
        with tree.inputs:
            vertex_index = SocketInteger("Vertex Index", default_input="INDEX")
            edge_number = SocketInteger("Edge Number")

        eov = EdgesOfVertex(vertex_index, sort_index=edge_number)
        ev = EdgeVertices()
        vert_1 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_1, eov)
        vert_2 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_2, eov)
        switch = (vert_1 != vertex_index) >> Switch.integer(..., vert_1, vert_2)

        with tree.outputs:
            _ = switch >> SocketInteger("Other Vertex")


class OffsetVector(NodeGroupBuilder):
    """
    Evaluate a given vector field at an offset to the current `Index`.
    """

    _name = "Offset Vector"
    _color_tag = "INPUT"

    i_index: IntegerSocket
    i_vector: VectorSocket
    i_offset: IntegerSocket
    o_vector: VectorSocket

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
            index = SocketInteger("Index", default_input="INDEX")
            vector = SocketVector("Vector", default_input="POSITION")
            offset = SocketInteger("Offset")

        value = EvaluateAtIndex.point.vector(vector, index + offset)

        with tree.outputs:
            _ = value >> SocketVector("Vector")
