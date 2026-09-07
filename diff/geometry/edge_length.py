# Node-group asset 'Edge Length' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class EdgeLength(CustomGeometryGroup):
    _name = "Edge Length"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        length = tree.outputs.float("Length")

        edge_vertices = g.EdgeVertices()
        (
            edge_vertices.o.position_1.distance(
                edge_vertices.o.position_2
            ).edge.evaluate()
            >> length
        )


ASSET = EdgeLength

ASSET_METADATA = {
    "description": "Returns the length of an edge",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
