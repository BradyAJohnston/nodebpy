# Node-group asset 'Random Rotation' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class RandomRotation(CustomGeometryGroup):
    _name = "Random Rotation"
    _color_tag = "CONVERTER"

    def _build_group(self, tree):
        tree.disable_arrange()

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
        reroute = g.Reroute(input=value.y)
        reroute_1 = g.Reroute(input=value.z)
        reroute_2 = g.Reroute(
            input=value.x.map_range(
                to_min=min_zenith / 3.1415927, to_max=max_zenith / 3.1415927
            )
        )
        reroute_3 = g.Reroute(input=reroute_2.o.output.sqrt())
        reroute_4 = g.Reroute(input=(1.0 - reroute_2).sqrt())
        quaternion_to_rotation = g.QuaternionToRotation(
            w=reroute_4.o.output * reroute_1.o.output.cos(),
            x=reroute_3.o.output * reroute.o.output.sin(),
            y=reroute_3.o.output * reroute.o.output.cos(),
            z=reroute_4.o.output * reroute_1.o.output.sin(),
        )

        quaternion_to_rotation >> rotation

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (780.0, 100.0),
            "Group Input": (-1200.0, -20.0),
            "Random Value": (-1000.0, 180.0),
            "Separate XYZ": (-800.0, 180.0),
            "Math": (-260.0, 160.0),
            "Math.001": (-60.0, 240.0),
            "Quaternion to Rotation": (580.0, 100.0),
            "Math.002": (360.0, 200.0),
            "Math.003": (-60.0, 140.0),
            "Reroute": (-180.0, 20.0),
            "Math.004": (-60.0, 40.0),
            "Math.005": (-60.0, -60.0),
            "Math.006": (-60.0, -160.0),
            "Math.007": (-60.0, -260.0),
            "Reroute.001": (-180.0, -40.0),
            "Math.008": (360.0, 80.0),
            "Math.009": (360.0, -40.0),
            "Math.010": (360.0, -160.0),
            "Reroute.002": (200.0, 180.0),
            "Reroute.003": (200.0, 120.0),
            "Reroute.004": (-300.0, 140.0),
            "Map Range": (-520.0, 180.0),
            "Math.011": (-800.0, -120.0),
            "Math.012": (-800.0, -240.0),
            "Group Input.001": (-1000.0, -200.0),
        }


ASSET = RandomRotation

ASSET_METADATA = {
    "description": "Returns a uniformly distributed random rotation",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b8945cf7-3045-4675-aae3-0b0eba853415",
    "catalog_simple_name": "Utilities",
}
