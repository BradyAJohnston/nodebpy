import bpy
from bpy.types import GeometryNodeGroup

from ...builder import NodeGroupBase, SocketInt, SocketLinker, TreeBuilder
from ...types import TYPE_INPUT_INT
from . import EdgesOfVertex, EdgeVertices, EvaluateAtIndex, Switch


class OtherVertex(NodeGroupBase):
    """
    OtherVertex node group
    """

    _node_group_name = "Other Vertex"

    def __init__(
        self, vertex_index: TYPE_INPUT_INT = None, edge_number: TYPE_INPUT_INT = 0
    ):
        super().__init__()
        self.node.node_tree = self._get_node_group(name=self._node_group_name)
        key_args = {
            "Vertex Index": vertex_index,
            "Edge Number": edge_number,
        }
        self._establish_links(**key_args)

    @property
    def i_vertex_index(self) -> SocketLinker:
        return self._input("Vertex Index")

    @property
    def i_edge_number(self) -> SocketLinker:
        return self._input("Edge Number")

    @property
    def o_other_vertex(self) -> SocketLinker:
        return self._output("Other Vertex")

    def _get_node_group(self, name: str) -> GeometryNodeGroup:
        if name in bpy.data.node_groups:
            return bpy.data.node_groups[name]

        with TreeBuilder(name) as tree:
            with tree.inputs:
                v_index = SocketInt("Vertex Index", default_input="INDEX")
                e_index = SocketInt("Edge Number")

            # with the index from the selected edge from the input, we get the two different vertices
            # of the edge. We compare them and return the one that isn't the current input vertex index
            eov = EdgesOfVertex(v_index, sort_index=e_index)
            ev = EdgeVertices()
            vert_1 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_1, eov)
            vert_2 = EvaluateAtIndex.edge.integer(ev.o_vertex_index_2, eov)
            switch = (vert_1 != v_index).switch(vert_1, vert_2)
            with tree.outputs:
                _ = switch >> SocketInt("Other Vertex")
            return tree.tree
