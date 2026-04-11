from ...builder import (
    IntegerSocketLinker,
    NodeGroupBuilder,
    SocketInt,
    SocketVector,
    TypedInputs,
    TypedOutputs,
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

    class Inputs(TypedInputs):
        @property
        def vertex_index(self) -> IntegerSocketLinker:
            """Input socket: Vertex Index"""
            return self.get("Vertex Index")  # type: ignore[return-value]

        @property
        def edge_number(self) -> IntegerSocketLinker:
            """Input socket: Edge Number"""
            return self.get("Edge Number")  # type: ignore[return-value]

    @property
    def i(self) -> "Inputs":
        return OtherVertex.Inputs(self)

    class Outputs(TypedOutputs):
        @property
        def other_vertex(self) -> IntegerSocketLinker:
            """Output socket: Other Vertex"""
            return self.get("Other Vertex")  # type: ignore[return-value]

    @property
    def o(self) -> "Outputs":
        return OtherVertex.Outputs(self)

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
        vert_1 = EvaluateAtIndex.edge.integer(ev.o.vertex_index_1, eov)
        vert_2 = EvaluateAtIndex.edge.integer(ev.o.vertex_index_2, eov)
        switch = (vert_1 != vertex_index) >> Switch.integer(..., vert_1, vert_2)

        with tree.outputs:
            _ = switch >> SocketInt("Other Vertex")


class OffsetVector(NodeGroupBuilder):
    """
    Evaluate a given vector field at an offset to the current `Index`.
    """

    _name = "Offset Vector"
    _color_tag = "INPUT"

    class Inputs(TypedInputs):
        @property
        def index(self) -> IntegerSocketLinker:
            """Input socket: Index"""
            return self.get("Index")  # type: ignore[return-value]

        @property
        def vector(self) -> VectorSocketLinker:
            """Input socket: Vector"""
            return self.get("Vector")  # type: ignore[return-value]

        @property
        def offset(self) -> IntegerSocketLinker:
            """Input socket: Offset"""
            return self.get("Offset")  # type: ignore[return-value]

    @property
    def i(self) -> "Inputs":
        return OffsetVector.Inputs(self)

    class Outputs(TypedOutputs):
        @property
        def vector(self) -> VectorSocketLinker:
            """Output socket: Vector"""
            return self.get("Vector")  # type: ignore[return-value]

    @property
    def o(self) -> "Outputs":
        return OffsetVector.Outputs(self)

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
