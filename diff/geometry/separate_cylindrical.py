# Node-group asset 'Separate Cylindrical' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy.builder import CustomGeometryGroup


class SeparateCylindrical(CustomGeometryGroup):
    _name = "Separate Cylindrical"
    _color_tag = "CONVERTER"

    def _build_group(self, tree):
        vector = tree.inputs.vector(
            "Vector", (0.0, 0.0, 0.0), min_value=0.0, max_value=1.0, hide_value=True
        )
        r = tree.outputs.float(
            "R",
            description="Radius - Length of the vector",
            min_value=-10000.0,
            max_value=10000.0,
        )
        phi = tree.outputs.float(
            "Phi",
            description="Azimuth - Angle around the up axis",
            min_value=0.0,
            max_value=6.2831855,
            subtype="ANGLE",
        )
        z = tree.outputs.float("Z", description="Offset from the ground plane")

        vector.y.atan2(vector.x) >> phi
        (vector * (1.0, 1.0, 0.0)).length() >> r

        vector.z >> z


ASSET = SeparateCylindrical

ASSET_METADATA = {
    "description": "Decompose a vector into its cylindrical components.",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
