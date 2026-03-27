from functools import partial

from ...builder import InputSpec, NodeGroupBuilder, OutputSpec, SocketInt, SocketVector
from ...types import TYPE_INPUT_INT
from . import EdgesOfVertex, EdgeVertices, EvaluateAtIndex, Switch


class OtherVertex(NodeGroupBuilder):
    """
    Given a vertex and an edge number from that vertex, returns the other
    vertex of that edge.
    """

    _node_group_name = "Other Vertex"
    _color_tag = "INPUT"

    i_vertex_index = InputSpec(
        partial(SocketInt, "Vertex Index", default_input="INDEX")
    )
    i_edge_number = InputSpec(partial(SocketInt, "Edge Number"))
    o_other_vertex = OutputSpec(partial(SocketInt, "Other Vertex"))

    def __init__(
        self, vertex_index: TYPE_INPUT_INT = None, edge_number: TYPE_INPUT_INT = 0
    ):
        super().__init__(vertex_index=vertex_index, edge_number=edge_number)

    @classmethod
    def _build_group(cls, tree, vertex_index: SocketInt, edge_number: SocketInt):
        eov = EdgesOfVertex(vertex_index, sort_index=edge_number)
        ev = EdgeVertices()
        vert_1 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_1, eov)
        vert_2 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_2, eov)
        switch = (vert_1 != vertex_index) >> Switch.integer(..., vert_1, vert_2)
        return {"Other Vertex": switch}


class OffsetVector(NodeGroupBuilder):
    """
    Evaluate a given vector field at an offset to the current `Index`.
    """

    _node_group_name = "Offset Vector"
    _color_tag = "INPUT"

    i_index = InputSpec(partial(SocketInt, "Index", default_input="INDEX"))
    i_vector = InputSpec(partial(SocketVector, "Vector", default_input="POSITION"))
    i_offset = InputSpec(partial(SocketInt, "Offset"))
    o_vector = OutputSpec(partial(SocketVector, "Vector"))

    def __init__(
        self,
        index: TYPE_INPUT_INT = None,
        vector: TYPE_INPUT_INT = None,
        offset: TYPE_INPUT_INT = 0,
    ):
        super().__init__(index=index, vector=vector, offset=offset)

    @classmethod
    def _build_group(
        cls, tree, index: SocketInt, vector: SocketVector, offset: SocketVector
    ):
        return {"Vector": EvaluateAtIndex.point.vector(vector, index + offset)}
