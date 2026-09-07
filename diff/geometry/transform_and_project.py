# Node-group asset 'Transform and Project' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class TransformAndProject(CustomGeometryGroup):
    _name = "Transform and Project"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
        vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), subtype="XYZ")
        transform = tree.inputs.matrix("Transform")
        projection = tree.inputs.matrix("Projection")
        normalized = tree.outputs.vector("Normalized", dimensions=2)
        depth = tree.outputs.float("Depth")

        transform_point = vector.transform(transform)
        with g.Frame("Depth in scene units"):
            abs(transform_point.z) >> depth
        vector_math = g.VectorMath.multiply_add(
            g.ProjectPoint(vector=transform_point, transform=projection),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
        )

        vector_math >> normalized


ASSET = TransformAndProject

ASSET_METADATA = {
    "description": "Computes a normalized 2D vector and its corresponding depths from a 3D vector and a given projection",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
