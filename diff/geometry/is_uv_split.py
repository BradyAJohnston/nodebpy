# Node-group asset 'Is UV Split' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .is_edge_boundary import IsEdgeBoundary


class Average_face_corners_for_edge(CustomGeometryGroup):
    _name = ".average_face_corners_for_edge"

    def _build_group(self, tree):
        tree.disable_arrange()

        edge_index = tree.inputs.integer("Edge Index", 0)
        vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0))
        vector_1 = tree.outputs.vector("Vector")

        reroute = g.Reroute(input=vector)
        hash_value = g.HashValue(
            value=g.HashValue(value=edge_index, seed=137),
            seed=g.HashValue(value=g.VertexOfCorner(), seed=231),
        )
        (
            (g.EdgeNeighbors().o.face_count.edge.at(edge_index) > 2).switch.vector(
                reroute, reroute.o.output.corner.mean(hash_value)
            )
            >> vector_1
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (540.0, 100.0),
            "Group Input": (-360.0, 40.0),
            "Field Average.002": (180.0, -20.0),
            "Vertex of Corner.005": (-360.0, -200.0),
            "Hash Value.004": (-180.0, -60.0),
            "Hash Value.005": (-180.0, -200.0),
            "Switch.005": (360.0, 100.0),
            "Evaluate at Index.002": (0.0, 180.0),
            "Edge Neighbors.006": (-180.0, 180.0),
            "Compare.006": (180.0, 180.0),
            "Reroute.003": (141.6, -11.0),
            "Hash Value": (2.8, -95.9),
        }


class IsUVSplit(CustomGeometryGroup):
    _name = "Is UV Split"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

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
            reroute = g.Reroute(input=uv_map)
            group = Average_face_corners_for_edge(
                **{"Edge Index": edges_of_corner.o.previous_edge_index}, Vector=reroute
            )
            group_1 = Average_face_corners_for_edge(
                **{"Edge Index": edges_of_corner}, Vector=reroute
            )
        corners_of_edge = g.CornersOfEdge(weights=vertex_of_corner)
        corners_of_edge_1 = g.CornersOfEdge(weights=vertex_of_corner, sort_index=-1)
        reroute_1 = g.Reroute(input=g.Value(0.00001).o.value)
        with g.Frame("Flipped Normals"):
            compare = g.Compare.integer.equal(
                g.VertexOfCorner(corner_index=corners_of_edge),
                g.VertexOfCorner(corner_index=corners_of_edge_1),
            )
        offset_corner_in_face = g.OffsetCornerInFace(
            corner_index=corners_of_edge_1, offset=1
        )
        reroute_2 = g.Reroute(input=group.o.vector)
        reroute_3 = g.Reroute(input=group_1.o.vector)
        evaluate_at_index = reroute_2.o.output.corner.at(
            g.OffsetCornerInFace(corner_index=corners_of_edge, offset=1)
        )
        evaluate_at_index_1 = reroute_2.o.output.corner.at(
            compare.o.result.switch.integer(offset_corner_in_face, corners_of_edge_1)
        )
        evaluate_at_index_2 = reroute_3.o.output.corner.at(
            compare.o.result.switch.integer(corners_of_edge_1, offset_corner_in_face)
        )
        compare_1 = g.Compare(
            a=reroute_3.o.output.corner.at(corners_of_edge),
            b=evaluate_at_index_1,
            epsilon=reroute_1,
            operation="NOT_EQUAL",
            data_type="VECTOR",
            mode="ELEMENT",
        )
        compare_2 = g.Compare(
            a=evaluate_at_index,
            b=evaluate_at_index_2,
            epsilon=reroute_1,
            operation="NOT_EQUAL",
            data_type="VECTOR",
            mode="ELEMENT",
        )
        boolean_math = compare_1.o.result | compare_2
        with g.Frame("Edge Boundary"):
            switch = IsEdgeBoundary().o.is_edge_boundary.switch.boolean(boolean_math)
        switch.edge.evaluate() >> is_uv_split

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (900.0, -140.0),
            "Corners of Edge.004": (-1080.0, -160.0),
            "Corners of Edge.005": (-1080.0, -420.0),
            "Evaluate at Index.006": (-240.0, 0.0),
            "Evaluate at Index.007": (-240.0, -140.0),
            "Offset Corner in Face.002": (-880.0, -500.0),
            "Compare.001": (-40.0, -80.0),
            "Offset Corner in Face.003": (-880.0, -240.0),
            "Evaluate at Index.008": (-240.0, -280.0),
            "Evaluate at Index.009": (-240.0, -420.0),
            "Compare.003": (-40.0, -360.0),
            "Boolean Math.001": (120.0, -180.0),
            "Vertex of Corner.002": (29.6, -35.9),
            "Vertex of Corner.003": (29.6, -135.9),
            "Compare.004": (209.6, -35.9),
            "Switch": (-460.0, -240.0),
            "Switch.001": (-460.0, -520.0),
            "Reroute": (-300.0, -200.0),
            "Reroute.001": (-300.0, -80.0),
            "Vertex of Corner.004": (-1303.7, -302.2),
            "Switch.002": (229.6, -76.0),
            "Frame.001": (290.4, -64.0),
            "Frame.002": (-909.6, 35.9),
            "Evaluate on Domain.004": (720.0, -140.0),
            "Group Input.004": (-1260.0, 180.0),
            "Edges of Corner.004": (29.5, -156.0),
            "Group.001": (249.5, -196.0),
            "Frame": (-1009.5, 436.0),
            "Is Edge Boundary": (29.6, -36.0),
            "Reroute.002": (149.5, -296.0),
            "Group.002": (249.5, -36.0),
            "Value": (-240.0, 80.0),
            "Reroute.003": (-60.0, -260.0),
        }


ASSET = IsUVSplit

ASSET_METADATA = {
    "description": "Returns a selection of edges that make up a seam in the provided UV data. A seam is defined as a discontinuity of the data between connected face corners.",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
