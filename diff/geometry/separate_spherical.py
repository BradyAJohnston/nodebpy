# Node-group asset 'Separate Spherical' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy.builder import CustomGeometryGroup


class SeparateSpherical(CustomGeometryGroup):
    _name = "Separate Spherical"
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
        theta = tree.outputs.float(
            "Theta", description="Zenith - Angle from the ground plane", subtype="ANGLE"
        )

        vector_math = vector.length()
        vector.y.atan2(vector.x) >> phi
        (vector.z / vector_math).asin() >> theta

        vector_math >> r


ASSET = SeparateSpherical

ASSET_METADATA = {
    "description": "Decompose a vector into its spherical components.",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
