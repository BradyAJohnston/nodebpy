# Node-group asset 'Is Edge Boundary' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class IsEdgeBoundary(CustomGeometryGroup):
    _name = "Is Edge Boundary"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        is_edge_boundary = tree.outputs.boolean(
            "Is Edge Boundary",
            description="Selection of edges that are part of the boundary of a mesh surface",
        )

        (
            g.Compare.integer.equal(g.EdgeNeighbors(), 1).o.result.edge.evaluate()
            >> is_edge_boundary
        )


ASSET = IsEdgeBoundary

ASSET_METADATA = {
    "description": "Returns a selection of boundary edges",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
