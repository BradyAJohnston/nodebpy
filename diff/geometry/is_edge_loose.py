# Node-group asset 'Is Edge Loose' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class IsEdgeLoose(CustomGeometryGroup):
    _name = "Is Edge Loose"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

        is_edge_loose = tree.outputs.boolean(
            "Is Edge Loose",
            description="Selection of edges that are not connected to a face",
        )

        (
            g.Compare.integer.equal(
                g.CornersOfEdge().o.total, 0
            ).o.result.edge.evaluate()
            >> is_edge_loose
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (240.0, 0.0),
            "Corners of Edge": (-360.0, 0.0),
            "Compare": (-160.0, 0.0),
            "Evaluate on Domain": (40.0, 0.0),
        }


ASSET = IsEdgeLoose

ASSET_METADATA = {
    "description": "Returns a selection of loose edges",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
