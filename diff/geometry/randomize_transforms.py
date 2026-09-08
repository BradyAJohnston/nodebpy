# Node-group asset 'Randomize Transforms' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class RandomizeTransforms(CustomGeometryGroup):
    _name = "Randomize Transforms"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        instances = tree.inputs.geometry(
            "Instances", description="Instances to rotate individually"
        )
        selection = tree.inputs.boolean(
            "Selection",
            True,
            description="Selection of instances to randomize",
            hide_value=True,
            hide_in_modifier=True,
        )
        local_space = tree.inputs.boolean(
            "Local Space",
            True,
            description="Randomize instance transforms in their individual local space",
        )
        offset = tree.inputs.vector(
            "Offset",
            (0.0, 0.0, 0.0),
            description="Offset the instances randomly",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
            subtype="XYZ",
        )
        rotation = tree.inputs.vector(
            "Rotation",
            (0.0, 0.0, 0.0),
            description="Rotate the instances randomly",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
            subtype="EULER",
        )
        scale_axes = tree.inputs.menu(
            "Scale Axes",
            description="Whether to apply random scale uniformly or per axis",
            expanded=True,
            optional_label=True,
            structure_type="SINGLE",
        )
        scale = tree.inputs.vector(
            "Scale",
            (0.0, 0.0, 0.0),
            description="Scale the instances randomly per axis",
            min_value=0.0,
            max_value=1.0,
            structure_type="FIELD",
        )
        scale_1 = tree.inputs.float(
            "Scale",
            0.0,
            description="Scale the instances randomly",
            min_value=0.0,
            max_value=1.0,
            structure_type="FIELD",
            subtype="FACTOR",
        )
        flipping = tree.inputs.vector(
            "Flipping",
            (0.0, 0.0, 0.0),
            description="Flip a fraction of instances along individual axes",
            min_value=0.0,
            max_value=1.0,
            structure_type="FIELD",
            subtype="FACTOR",
        )
        seed = tree.inputs.integer(
            "Seed",
            0,
            description="Base value to control random variation in a reproducible way",
            structure_type="SINGLE",
        )
        instances_1 = tree.outputs.geometry("Instances")

        reroute = g.Reroute(input=selection)
        hash_value = g.HashValue(value=seed, seed=465656096)
        reroute_1 = g.Reroute(input=local_space)
        reroute_2 = g.Reroute(input=reroute.o.output)
        hash_value_1 = g.HashValue(value=hash_value, seed=76836728)
        reroute_3 = g.Reroute(input=reroute_1.o.output)
        reroute_4 = g.Reroute(input=hash_value_1.o.hash)
        reroute_5 = g.Reroute(
            input=reroute_1.o.output.switch.vector(g.Position(), (0.0, 0.0, 0.0))
        )
        random_value = g.RandomValue.vector(
            (1.0, 1.0, 1.0) - flipping,
            (0.0, 0.0, 0.0) - flipping,
            seed=g.HashValue(value=hash_value_1, seed=76881592),
        )
        index_switch = g.IndexSwitch.vector(
            g.MenuSwitch.integer(scale_axes, {"Uniform": 0, "Axes": 1}),
            (
                g.RandomValue(max=scale_1, seed=reroute_4),
                g.RandomValue.vector((0.0, 0.0, 0.0), scale, seed=reroute_4),
            ),
        )
        random_value_1 = g.RandomValue.vector(
            (-1.0, -1.0, -1.0),
            (1.0, 1.0, 1.0),
            seed=g.HashValue(
                value=g.Reroute(input=hash_value_1.o.hash), seed=587641147
            ),
        )
        (
            instances
            >> g.RotateInstances(
                selection=reroute,
                rotation=g.RandomValue.vector(
                    rotation * -0.5, rotation * 0.5, seed=hash_value
                ),
                pivot_point=reroute_5,
                local_space=reroute_1,
            )
            >> g.TranslateInstances(
                selection=reroute_2,
                translation=random_value_1.o.value * offset,
                local_space=reroute_3,
            )
            >> g.ScaleInstances(
                selection=reroute_2,
                scale=((1.0, 1.0, 1.0) - index_switch)
                * g.VectorMath.sign(random_value),
                center=reroute_5,
                local_space=reroute_3,
            )
            >> instances_1
        )

        scale_axes.default_value = "Uniform"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (1484.6, 64.5),
            "Group Input": (-340.0, 200.0),
            "Rotate Instances": (636.4, 180.1),
            "Random Value": (-140.9, -18.1),
            "Scale Instances": (1283.7, 86.4),
            "Group Input.021": (-540.0, -60.0),
            "Vector Math.010": (-340.9, 21.9),
            "Vector Math.011": (-340.9, -98.1),
            "Group Input.024": (-733.6, -304.7),
            "Reroute": (525.5, 103.6),
            "Random Value.005": (690.5, -35.7),
            "Vector Math.004": (886.3, -78.5),
            "Random Value.008": (501.5, -612.4),
            "Vector Math.001": (273.2, -568.8),
            "Vector Math.002": (273.2, -742.6),
            "Vector Math.003": (700.1, -628.0),
            "Translate Instances": (1068.0, 125.9),
            "Group Input.001": (688.6, -327.4),
            "Hash Value.004": (-360.5, -300.5),
            "Hash Value.007": (-552.3, -299.7),
            "Menu Switch.007": (-102.3, -238.6),
            "Group Input.002": (-347.7, -479.0),
            "Random Value.004": (-100.1, -392.4),
            "Index Switch.013": (95.6, -483.1),
            "Random Value.006": (-101.0, -626.1),
            "Vector Math.007": (391.0, -336.8),
            "Hash Value.005": (279.9, -927.6),
            "Vector Math": (908.0, -383.7),
            "Group Input.003": (94.2, -777.1),
            "Group Input.004": (-125.7, 76.9),
            "Position": (96.4, -39.8),
            "Switch": (289.2, 5.1),
            "Reroute.002": (562.8, -44.4),
            "Reroute.003": (229.7, 49.1),
            "Reroute.001": (1014.9, -7.6),
            "Reroute.004": (986.0, 40.6),
            "Reroute.005": (-166.6, -660.4),
            "Hash Value.006": (503.4, -160.3),
            "Reroute.006": (-125.0, -221.1),
        }


ASSET = RandomizeTransforms

ASSET_METADATA = {
    "description": "Randomize the transformation of instances",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "a01301f0-5ae0-4627-91a4-b7fde91e5c5a",
    "catalog_simple_name": "Instances",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
