# Node-group asset 'Randomize Transforms' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class RandomizeTransforms(CustomGeometryGroup):
    _name = "Randomize Transforms"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
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

        hash_value = g.HashValue(value=seed, seed=465656096)
        switch = local_space.switch.vector(g.Position(), (0.0, 0.0, 0.0))
        hash_value_1 = g.HashValue(value=hash_value, seed=76836728)
        index_switch = g.IndexSwitch.vector(
            g.MenuSwitch.integer(scale_axes, {"Uniform": 0, "Axes": 1}),
            (
                g.RandomValue(max=scale_1, seed=hash_value_1),
                g.RandomValue.vector((0.0, 0.0, 0.0), scale, seed=hash_value_1),
            ),
        )
        random_value = g.RandomValue.vector(
            (1.0, 1.0, 1.0) - flipping,
            (0.0, 0.0, 0.0) - flipping,
            seed=g.HashValue(value=hash_value_1, seed=76881592),
        )
        random_value_1 = g.RandomValue.vector(
            (-1.0, -1.0, -1.0),
            (1.0, 1.0, 1.0),
            seed=g.HashValue(value=hash_value_1, seed=587641147),
        )
        (
            instances
            >> g.RotateInstances(
                selection=selection,
                rotation=g.RandomValue.vector(
                    rotation * -0.5, rotation * 0.5, seed=hash_value
                ),
                pivot_point=switch,
                local_space=local_space,
            )
            >> g.TranslateInstances(
                selection=selection,
                translation=random_value_1.o.value * offset,
                local_space=local_space,
            )
            >> g.ScaleInstances(
                selection=selection,
                scale=((1.0, 1.0, 1.0) - index_switch)
                * g.VectorMath.sign(random_value),
                center=switch,
                local_space=local_space,
            )
            >> instances_1
        )

        scale_axes.default_value = "Uniform"


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
