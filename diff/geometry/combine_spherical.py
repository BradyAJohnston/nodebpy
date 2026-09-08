# Node-group asset 'Combine Spherical' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class CombineSpherical(CustomGeometryGroup):
    _name = "Combine Spherical"
    _color_tag = "CONVERTER"

    def _build_group(self, tree):
        tree.disable_arrange()

        r = tree.inputs.float(
            "R",
            0.0,
            description="Radius - Length of the vector",
            min_value=0.0,
            max_value=10000.0,
        )
        phi = tree.inputs.float(
            "Phi",
            0.0,
            description="Azimuth - Angle around the up axis",
            min_value=-3.1415927,
            max_value=3.1415927,
            subtype="ANGLE",
        )
        theta = tree.inputs.float(
            "Theta",
            0.0,
            description="Zenith - Angle from the ground plane",
            min_value=-1.5707964,
            max_value=1.5707964,
            subtype="ANGLE",
        )
        vector = tree.outputs.vector("Vector")

        vector_rotate = g.VectorRotate(
            vector=g.VectorMath.scale((1.0, 0.0, 0.0), r),
            angle=theta,
            rotation_type="Y_AXIS",
            invert=True,
        )
        vector_rotate_1 = g.VectorRotate.z_axis(vector_rotate, angle=phi)

        vector_rotate_1 >> vector

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (-120.0, 200.0),
            "Vector Math": (-680.0, 240.0),
            "Vector Rotate": (-500.0, 240.0),
            "Vector Rotate.001": (-320.0, 240.0),
            "Group Input": (-900.0, 240.0),
        }


ASSET = CombineSpherical

ASSET_METADATA = {
    "description": "Create a vector from its spherical components.",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
