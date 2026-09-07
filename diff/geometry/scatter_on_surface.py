# Node-group asset 'Scatter on Surface' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup

from .randomize_transforms import RandomizeTransforms


class ScatterOnSurface(CustomGeometryGroup):
    _name = "Scatter on Surface"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        mesh = tree.inputs.geometry(
            "Mesh", description="Mesh on whose faces to scatter on"
        )
        selection = tree.inputs.boolean(
            "Selection",
            True,
            description="Which faces to scatter on",
            hide_value=True,
            hide_in_modifier=True,
        )
        density_method = tree.inputs.menu(
            "Density Method",
            description="Method to define the number of scattered instances",
            expanded=True,
            optional_label=True,
        )
        distribution_method = tree.inputs.menu(
            "Distribution Method",
            description="Method to use for scattering points",
            expanded=True,
            optional_label=True,
        )
        amount = tree.inputs.integer(
            "Amount",
            1000,
            description="Exact number of scattered instances before masking",
            min_value=0,
        )
        density = tree.inputs.float(
            "Density",
            1.0,
            description="Amount of scattered instances per unit squared",
            min_value=0.0,
        )
        distribution_mask = tree.inputs.float(
            "Distribution Mask",
            1.0,
            description="Mask to multiply the density by",
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )
        minimum_distance = tree.inputs.float(
            "Minimum Distance",
            0.0,
            description="Minimum allowed distance between the centers of two scattered instances. Increase value for a more locally even distribution.",
            min_value=0.0,
            subtype="DISTANCE",
        )
        keep_surface = tree.inputs.boolean(
            "Keep Surface",
            True,
            description="Keep the original input geometry and join it with the scattered geometry",
        )
        scatter_on_instances = tree.inputs.boolean(
            "Scatter on Instances",
            False,
            description="Use instances contained in the input geometry as base for scattering",
        )
        seed = tree.inputs.integer(
            "Seed",
            0,
            description="Base value to control random variation in a reproducible way",
            structure_type="SINGLE",
        )
        with tree.inputs.panel("Instancing"):
            input_type = tree.inputs.menu(
                "Input Type",
                description="How the instance geometry input should be exposed",
                expanded=True,
                optional_label=True,
                hide_in_modifier=True,
            )
            instance_type = tree.inputs.menu(
                "Instance Type",
                description="How the instance geometry data-block should be exposed",
                expanded=True,
                optional_label=True,
            )
            object = tree.inputs.object(
                "Object",
                description="Object providing the instance geometry used for scattering",
            )
            collection = tree.inputs.collection(
                "Collection",
                description="Collection providing the instance geometry used for scattering",
            )
            instance = tree.inputs.geometry(
                "Instance",
                description="Geometry that is instanced on the scattered points",
            )
            viewport_visibility = tree.inputs.float(
                "Viewport Visibility",
                1.0,
                description="Amount of scattered instances shown in the viewport",
                min_value=0.0,
                max_value=1.0,
                subtype="FACTOR",
            )
            realize_instances = tree.inputs.boolean(
                "Realize Instances",
                False,
                description="Turn the output into a single geometry rather than instances (required by many other modifiers)",
            )
        pick_instance = tree.inputs.boolean(
            "Pick Instance",
            False,
            description="Choose child instances for each element instead of instancing the entire geometry",
            is_panel_toggle=True,
        )
        reset_transform = tree.inputs.boolean(
            "Reset Transform",
            True,
            description="Reset the transforms of each individual child instance",
        )
        instance_seed = tree.inputs.integer(
            "Instance Seed",
            0,
            description="Base value to control random instance variation in a reproducible way",
            structure_type="SINGLE",
        )
        surface_offset = tree.inputs.float(
            "Surface Offset",
            0.0,
            description="Distance to offset each instance along the normal of the surface geometry",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
            subtype="DISTANCE",
        )
        align_rotation = tree.inputs.boolean(
            "Align Rotation",
            True,
            description="Rotate instances based on the shape of the surface geometry",
            structure_type="FIELD",
        )
        alignment_axis = tree.inputs.menu(
            "Alignment Axis",
            description="Which axis to align with the normal of the surface geometry",
            expanded=True,
            optional_label=True,
            structure_type="SINGLE",
        )
        scale = tree.inputs.vector(
            "Scale",
            (1.0, 1.0, 1.0),
            description="Scale of the instances on each local axis",
            structure_type="FIELD",
            subtype="XYZ",
        )
        randomize = tree.inputs.boolean(
            "Randomize",
            False,
            description="Randomize transforms between all scattered instances",
            is_panel_toggle=True,
        )
        randomize_offset = tree.inputs.vector(
            "Randomize Offset",
            (0.0, 0.0, 0.0),
            description="Offset the instances randomly",
            min_value=-10000.0,
            max_value=10000.0,
            subtype="XYZ",
        )
        randomize_rotation = tree.inputs.vector(
            "Randomize Rotation",
            (0.0, 0.0, 0.0),
            description="Rotate the instances randomly",
            min_value=-6.28319,
            max_value=6.2831855,
            subtype="EULER",
        )
        randomize_scale_axes = tree.inputs.menu(
            "Randomize Scale Axes",
            description="Whether to apply random scale uniformly or per axis",
            expanded=True,
            optional_label=True,
        )
        randomize_scale = tree.inputs.vector(
            "Randomize Scale",
            (0.0, 0.0, 0.0),
            description="Scale the instances down randomly per axis",
            min_value=0.0,
            max_value=1.0,
            subtype="XYZ",
        )
        randomize_scale_1 = tree.inputs.float(
            "Randomize Scale",
            0.0,
            description="Scale the instances down randomly",
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )
        randomize_flipping = tree.inputs.vector(
            "Randomize Flipping",
            (0.0, 0.0, 0.0),
            description="Flip a fraction of instances along individual axes",
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )
        randomize_seed = tree.inputs.integer(
            "Randomize Seed",
            0,
            description="Base value to control random variation in a reproducible way",
        )
        with tree.inputs.panel("Masking", default_closed=True):
            masking = tree.inputs.boolean(
                "Masking",
                False,
                description="Additional masking applied after the initial scattering of instances",
                is_panel_toggle=True,
            )
            image_mask = tree.inputs.image(
                "Image Mask",
                description="Grayscale image texture used to remove scattered instances",
            )
            uv_map = tree.inputs.vector(
                "UV Map",
                (0.0, 0.0, 0.0),
                description="Texture coordinates used to map the image on the surface",
                hide_value=True,
                structure_type="FIELD",
                default_attribute="UVMap",
                default_input="POSITION",
            )
        instances = tree.outputs.geometry("Instances")

        menu_switch = g.MenuSwitch.integer(
            distribution_method, {"Random": 0, "Poisson Disk": 1}
        )
        with g.Frame("Distribution"):
            with g.Frame("Amount"):
                with g.Frame("Initial Density Estimate"):
                    face_area = g.FaceArea()
                    attribute_statistic = g.AttributeStatistic(
                        geometry=mesh,
                        selection=selection,
                        attribute=distribution_mask,
                        domain="FACE",
                    )
                    attribute_statistic_1 = g.AttributeStatistic(
                        geometry=mesh,
                        selection=selection,
                        attribute=face_area,
                        domain="FACE",
                    )
                    attribute_statistic_2 = g.AttributeStatistic(
                        geometry=mesh,
                        selection=selection,
                        attribute=distribution_mask * face_area,
                        domain="FACE",
                    )
                    math = (
                        amount
                        / attribute_statistic_1.o.sum
                        * (attribute_statistic_1.o.sum / attribute_statistic_2.o.sum)
                    )
                    with g.Frame("10% supersample"):
                        math_1 = math * 1.1
                    math_2 = math * attribute_statistic.o.max
                repeat_zone = g.RepeatZone(g.Integer(integer=5))
                geometry = repeat_zone.items.geometry("Geometry")
                density_1 = repeat_zone.items.float("Density", math_1)
                output = repeat_zone.items.rotation("Output")
                normal = repeat_zone.items.vector("Normal")
                result = repeat_zone.items.boolean("Result")
                distribute_points_on_faces = g.DistributePointsOnFaces(
                    mesh=mesh,
                    selection=selection,
                    density=density_1.current * distribution_mask,
                    seed=seed,
                )
                with g.Frame("Make new density estimate"):
                    domain_size = g.DomainSize(
                        geometry=distribute_points_on_faces, component="POINTCLOUD"
                    )
                    compare = domain_size >= amount
                    with g.Frame("new estimate"):
                        switch = g.Switch(
                            switch=domain_size,
                            true=(
                                g.Math.divide(amount, domain_size).o.value * 1.1
                            ).clamp(1.1, 10.0),
                            false=2.0,
                        )
                (
                    result.current.switch.geometry(
                        distribute_points_on_faces, geometry.current
                    )
                    >> geometry.next
                )
                (
                    result.current.switch.rotation(
                        distribute_points_on_faces.o.rotation, output.current
                    )
                    >> output.next
                )
                (
                    result.current.switch.vector(
                        distribute_points_on_faces.o.normal, normal.current
                    )
                    >> normal.next
                )
                (
                    result.current.switch.float(
                        switch.o.output * density_1.current, density_1.current
                    )
                    >> density_1.next
                )
                result.current.switch.boolean(compare, result.current) >> result.next
                delete_geometry = (
                    geometry.result
                    >> g.SortElements(
                        sort_weight=g.RandomValue(
                            seed=g.HashValue(value=seed, seed=32351)
                        )
                    )
                    >> g.DeleteGeometry(selection=g.Index() >= amount)
                )
            with g.Frame("Density"):
                switch_1 = scatter_on_instances.switch.geometry(
                    g.SeparateComponents(geometry=mesh), mesh
                )
                distribute_points_on_faces_1 = g.DistributePointsOnFaces(
                    mesh=switch_1,
                    selection=selection,
                    density=distribution_mask * density,
                    seed=seed,
                )
                attribute_statistic_3 = g.AttributeStatistic(
                    geometry=switch_1, attribute=density, domain="CORNER"
                )
                distribute_points_on_faces_2 = g.DistributePointsOnFaces(
                    mesh=switch_1,
                    selection=selection,
                    distance_min=minimum_distance,
                    density_max=attribute_statistic_3.o.max,
                    density_factor=distribution_mask
                    * (density / attribute_statistic_3.o.max),
                    seed=seed,
                    distribute_method="POISSON",
                )
                switch_2 = menu_switch.o.poisson_disk.switch.geometry(
                    distribute_points_on_faces_1, distribute_points_on_faces_2
                )
                switch_3 = menu_switch.o.poisson_disk.switch.rotation(
                    distribute_points_on_faces_1.o.rotation,
                    distribute_points_on_faces_2.o.rotation,
                )
                switch_4 = menu_switch.o.poisson_disk.switch.vector(
                    distribute_points_on_faces_1.o.normal,
                    distribute_points_on_faces_2.o.normal,
                )
        separate_components = g.SeparateComponents(geometry=mesh)
        menu_switch_1 = g.MenuSwitch.integer(
            density_method, {"Density": 0, "Amount": 1}
        )
        switch_5 = menu_switch_1.o.amount.switch.float(
            attribute_statistic_3.o.max, math_2
        )
        with g.Frame("Instance Geometry"):
            menu_switch_2 = g.MenuSwitch.integer(
                instance_type, {"Object": 0, "Collection": 1}
            )
            menu_switch_3 = g.MenuSwitch.integer(
                input_type, {"Data-Block": 0, "Geometry": 1}
            )
            switch_6 = pick_instance.switch.boolean(true=reset_transform)
            switch_7 = switch_6.switch.geometry(
                g.CollectionInfo(collection=collection, separate_children=True),
                g.CollectionInfo(
                    collection=collection, separate_children=True, reset_children=True
                ),
            )
            switch_8 = switch_6.switch.geometry(
                instance,
                g.SetInstanceTransform(
                    instances=instance, transform=g.CombineTransform()
                ),
            )
            index_switch = g.IndexSwitch.geometry(
                menu_switch_2,
                (g.ObjectInfo(object=object, as_instance=True).o.geometry, switch_7),
            )
            index_switch_1 = g.IndexSwitch.geometry(
                menu_switch_3.o.geometry, (index_switch, switch_8)
            )
            integer_math = (
                g.DomainSize(geometry=index_switch_1).o.point_count
                + g.DomainSize(
                    geometry=index_switch_1, component="INSTANCES"
                ).o.instance_count
            )
            with g.Frame("Dummy Cube"):
                delete_geometry_1 = g.DeleteGeometry(
                    geometry=g.Cube(size=(0.31830987 / switch_5) ** 0.5),
                    mode="ONLY_FACE",
                    domain="FACE",
                )
                geometry_to_instance = g.GeometryToInstance(delete_geometry_1)
            switch_9 = g.Compare.integer.equal(
                integer_math, 0
            ).o.result.switch.geometry(index_switch_1, geometry_to_instance)
        switch_10 = menu_switch_3.o.geometry.switch.boolean(
            menu_switch_2.o.collection.switch.boolean(true=pick_instance), pick_instance
        )
        with g.Frame("Instance Fallback"):
            compare_1 = g.Compare.integer.equal(
                g.DomainSize(geometry=switch_9, component="INSTANCES").o.instance_count,
                0,
            )
            warning = g.Warning.info(
                switch_10 & compare_1,
                "Pick Instance is on, but there are no instances to pick from. Falling back to using input as instance.",
            )
            switch_11 = warning.o.show.switch.geometry(
                switch_9, g.GeometryToInstance(switch_9)
            )
        switch_12 = menu_switch_1.o.amount.switch.rotation(switch_3, output.result)
        with g.Frame("Alignment"):
            transform_direction = g.TransformDirection(
                transform=switch_12, direction=(0.0, 0.0, 1.0)
            )
            index_switch_2 = g.IndexSwitch.rotation(
                g.MenuSwitch.integer(alignment_axis, {"X": 0, "Y": 1, "Z": 2}),
                (
                    g.AlignRotationToVector(
                        rotation=switch_12, vector=transform_direction, axis="X"
                    ),
                    g.AlignRotationToVector(
                        rotation=switch_12, vector=transform_direction, axis="Y"
                    ),
                    switch_12,
                ),
            )
            switch_13 = align_rotation.switch.rotation((0.0, 0.0, 0.0), index_switch_2)
        switch_14 = menu_switch_1.o.amount.switch.vector(switch_4, normal.result)
        switch_15 = menu_switch_1.o.amount.switch.geometry(switch_2, delete_geometry)
        with g.Frame("Viewport Visibility"):
            delete_geometry_2 = g.DeleteGeometry(
                geometry=switch_15,
                selection=g.RandomValue(seed=g.HashValue(value=seed, seed=32351))
                > viewport_visibility,
            )
            switch_16 = ((viewport_visibility < 1.0) & g.IsViewport()).switch.geometry(
                switch_15, delete_geometry_2
            )
        with g.Frame("Masking"):
            random_value = g.RandomValue.boolean(
                g.Math.subtract(
                    1.0, g.ImageTexture(image=image_mask, vector=uv_map).o.color
                ),
                seed=g.HashValue(value=seed, seed=-75381),
            )
            switch_17 = (g.ImageInfo(image=image_mask) > 0).switch.geometry(
                switch_16, g.DeleteGeometry(geometry=switch_16, selection=random_value)
            )
            switch_18 = masking.switch.geometry(switch_16, switch_17)
        with g.Frame("Normal Offset"):
            set_position = switch_18 >> g.SetPosition(offset=switch_14 * surface_offset)
        instance_on_points = set_position >> g.InstanceOnPoints(
            instance=switch_11,
            pick_instance=switch_10,
            instance_index=switch_10.switch.integer(
                true=g.HashValue(value=g.ID(), seed=instance_seed)
            ),
            rotation=switch_13,
            scale=scale,
        )
        with g.Frame("Randomization"):
            group = RandomizeTransforms(
                Instances=instance_on_points,
                Offset=randomize_offset,
                Rotation=randomize_rotation,
                **{"Scale Axes": randomize_scale_axes},
                Flipping=randomize_flipping,
                Seed=g.HashValue(value=seed, seed=randomize_seed),
                _named_links=[("Scale", randomize_scale), ("Scale", randomize_scale_1)],
            )
            switch_19 = randomize.switch.geometry(instance_on_points, group)
        switch_20 = realize_instances.switch.geometry(
            switch_19,
            g.RealizeInstances(geometry=switch_19, realize_to_point_domain=True),
        )
        join_geometry = g.JoinGeometry(
            geometry=(
                separate_components.o.curve,
                separate_components.o.grease_pencil,
                separate_components.o.point_cloud,
                separate_components.o.volume,
                separate_components.o.instances,
                switch_20,
            )
        )
        (
            keep_surface.switch.geometry(
                scatter_on_instances.switch.geometry(join_geometry, switch_20),
                g.JoinGeometry(geometry=(mesh, switch_20)),
            )
            >> instances
        )

        density_method.default_value = "Density"
        distribution_method.default_value = "Random"
        input_type.default_value = "Data-Block"
        instance_type.default_value = "Object"
        alignment_axis.default_value = "Z"
        randomize_scale_axes.default_value = "Uniform"


ASSET = ScatterOnSurface

ASSET_METADATA = {
    "description": "Scatter referenced geometry on a surface mesh",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "007a2c8d-f113-421b-a39c-8fbc76c4f7fe",
    "catalog_simple_name": "Generate",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
