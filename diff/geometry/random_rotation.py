# Node-group asset 'Random Rotation' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class RandomRotation(CustomGeometryGroup):
    _name = "Random Rotation"
    _color_tag = "CONVERTER"

    def _build_group(self, tree):
        min_zenith = tree.inputs.float(
            "Min Zenith",
            0.0,
            description="Lower limit of the tilt away from the +Z direction",
            min_value=0.0,
            max_value=3.1415927,
            subtype="ANGLE",
        )
        max_zenith = tree.inputs.float(
            "Max Zenith",
            3.1415927,
            description="Upper limit of the tilt away from the +Z direction",
            min_value=0.0,
            max_value=3.1415927,
            subtype="ANGLE",
        )
        id = tree.inputs.integer(
            "ID",
            0,
            description="Identifier per element used for randomization",
            hide_value=True,
            default_input="ID_OR_INDEX",
        )
        seed = tree.inputs.integer(
            "Seed",
            0,
            description="Base value to control random variation in a reproducible way",
            min_value=-10000,
            max_value=10000,
        )
        rotation = tree.outputs.rotation(
            "Rotation",
            description="Random rotations resulting in uniformly distributed directions. Rotation around the Z axis is fully random.",
        )

        value = g.RandomValue.vector(
            (0.0, 0.0, 0.0), (1.0, 6.2831855, 6.2831855), id, seed
        ).o.value
        map_range = value.x.map_range(
            to_min=min_zenith / 3.1415927, to_max=max_zenith / 3.1415927
        )
        math = map_range.sqrt()
        math_1 = (1.0 - map_range).sqrt()
        quaternion_to_rotation = g.QuaternionToRotation(
            w=math_1 * value.z.cos(),
            x=math * value.y.sin(),
            y=math * value.y.cos(),
            z=math_1 * value.z.sin(),
        )

        quaternion_to_rotation >> rotation


ASSET = RandomRotation

ASSET_METADATA = {
    "description": "Returns a uniformly distributed random rotation",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b8945cf7-3045-4675-aae3-0b0eba853415",
    "catalog_simple_name": "Utilities",
}
