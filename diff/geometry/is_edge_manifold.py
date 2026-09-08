# Node-group asset 'Is Edge Manifold' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class IsEdgeManifold(CustomGeometryGroup):
    _name = "Is Edge Manifold"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

        is_edge_manifold = tree.outputs.boolean(
            "Is Edge Manifold",
            description="Selection of edges that connect two faces of a mesh surface",
        )

        (
            g.Compare.integer.equal(
                g.CornersOfEdge().o.total, 2
            ).o.result.edge.evaluate()
            >> is_edge_manifold
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (440.0, 0.0),
            "Corners of Edge": (-100.0, 0.0),
            "Compare": (80.0, 0.0),
            "Evaluate on Domain": (260.0, 0.0),
        }


ASSET = IsEdgeManifold

ASSET_METADATA = {
    "description": "Returns a selection of manifold edges",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
