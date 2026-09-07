# Node-group asset 'Is UV Split' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup

from .is_edge_boundary import IsEdgeBoundary


class Average_face_corners_for_edge(CustomGeometryGroup):
    _name = ".average_face_corners_for_edge"

    def _build_group(self, tree):
        edge_index = tree.inputs.integer("Edge Index", 0)
        vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
        vector_1 = tree.outputs.vector("Vector")

        hash_value = g.HashValue(
            value=g.HashValue(value=edge_index, seed=137),
            seed=g.HashValue(value=g.VertexOfCorner(), seed=231),
        )
        (
            (g.EdgeNeighbors().o.face_count.edge.at(edge_index) > 2).switch.vector(
                vector, vector.corner.mean(hash_value)
            )
            >> vector_1
        )


class IsUVSplit(CustomGeometryGroup):
    _name = "Is UV Split"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        uv_map = tree.inputs.vector(
            "UV Map",
            (0.0, 0.0, 0.0),
            description="Vectors to compare between connected face corners of an edge for differences. (Supports 3D vectors.)",
            hide_value=True,
        )
        is_uv_split = tree.outputs.boolean(
            "Is UV Split",
            description="Selection of edges that signify a discontinuity of the input vectors",
            attribute_domain="EDGE",
        )

        vertex_of_corner = g.VertexOfCorner()
        with g.Frame("Compare averages for face count > 2"):
            edges_of_corner = g.EdgesOfCorner()
            group = Average_face_corners_for_edge(
                **{"Edge Index": edges_of_corner.o.previous_edge_index}, Vector=uv_map
            )
            group_1 = Average_face_corners_for_edge(
                **{"Edge Index": edges_of_corner}, Vector=uv_map
            )
        value = g.Value(0.00001)
        corners_of_edge = g.CornersOfEdge(weights=vertex_of_corner)
        corners_of_edge_1 = g.CornersOfEdge(weights=vertex_of_corner, sort_index=-1)
        with g.Frame("Flipped Normals"):
            compare = g.Compare.integer.equal(
                g.VertexOfCorner(corner_index=corners_of_edge),
                g.VertexOfCorner(corner_index=corners_of_edge_1),
            )
        offset_corner_in_face = g.OffsetCornerInFace(
            corner_index=corners_of_edge_1, offset=1
        )
        evaluate_at_index = group.o.vector.corner.at(
            compare.o.result.switch.integer(offset_corner_in_face, corners_of_edge_1)
        )
        evaluate_at_index_1 = group_1.o.vector.corner.at(
            compare.o.result.switch.integer(corners_of_edge_1, offset_corner_in_face)
        )
        compare_1 = g.Compare(
            a=group_1.o.vector.corner.at(corners_of_edge),
            b=evaluate_at_index,
            epsilon=value,
            operation="NOT_EQUAL",
            data_type="VECTOR",
            mode="ELEMENT",
        )
        compare_2 = g.Compare(
            a=group.o.vector.corner.at(
                g.OffsetCornerInFace(corner_index=corners_of_edge, offset=1)
            ),
            b=evaluate_at_index_1,
            epsilon=value,
            operation="NOT_EQUAL",
            data_type="VECTOR",
            mode="ELEMENT",
        )
        boolean_math = compare_1.o.result | compare_2
        with g.Frame("Edge Boundary"):
            switch = IsEdgeBoundary().o.is_edge_boundary.switch.boolean(boolean_math)
        switch.edge.evaluate() >> is_uv_split


ASSET = IsUVSplit

ASSET_METADATA = {
    "description": "Returns a selection of edges that make up a seam in the provided UV data. A seam is defined as a discontinuity of the data between connected face corners.",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
