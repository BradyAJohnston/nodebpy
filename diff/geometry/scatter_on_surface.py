# Node-group asset 'Scatter on Surface' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .randomize_transforms import RandomizeTransforms


class ScatterOnSurface(CustomGeometryGroup):
    _name = "Scatter on Surface"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

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
                reroute = g.Reroute(input=amount)
                repeat_zone = g.RepeatZone(g.Integer(integer=5))
                geometry = repeat_zone.items.geometry("Geometry")
                density_1 = repeat_zone.items.float("Density", math_1)
                output = repeat_zone.items.rotation("Output")
                normal = repeat_zone.items.vector("Normal")
                result = repeat_zone.items.boolean("Result")
                reroute_1 = g.Reroute(input=g.Reroute(input=math_2).o.output)
                distribute_points_on_faces = g.DistributePointsOnFaces(
                    mesh=mesh,
                    selection=selection,
                    density=density_1.current * distribution_mask,
                    seed=seed,
                )
                with g.Frame("Make new density estimate"):
                    reroute_2 = g.Reroute(input=reroute.o.output)
                    domain_size = g.DomainSize(
                        geometry=distribute_points_on_faces, component="POINTCLOUD"
                    )
                    compare = domain_size >= reroute_2
                    with g.Frame("new estimate"):
                        reroute_3 = g.Reroute(input=domain_size.o.point_count)
                        switch = g.Switch(
                            switch=reroute_3,
                            true=(
                                g.Math.divide(reroute_2, reroute_3).o.value * 1.1
                            ).clamp(1.1, 10.0),
                            false=2.0,
                        )
                reroute_4 = g.Reroute(input=g.Reroute(input=result.current).o.output)
                reroute_5 = g.Reroute(input=g.Reroute(input=density_1.current).o.output)
                reroute_6 = g.Reroute(input=reroute_4.o.output)
                reroute_7 = g.Reroute(input=reroute_6.o.output)
                switch_1 = reroute_7.o.output.switch.vector(
                    g.Reroute(input=distribute_points_on_faces.o.normal), normal.current
                )
                reroute_8 = g.Reroute(input=reroute_7.o.output)
                switch_2 = reroute_8.o.output.switch.rotation(
                    g.Reroute(input=distribute_points_on_faces.o.rotation),
                    output.current,
                )
                switch_3 = g.Reroute(input=reroute_8.o.output).o.output.switch.geometry(
                    distribute_points_on_faces, geometry.current
                )
                switch_3 >> geometry.next
                switch_2 >> output.next
                switch_1 >> normal.next
                (
                    reroute_6.o.output.switch.float(
                        switch.o.output * reroute_5, reroute_5
                    )
                    >> density_1.next
                )
                reroute_4.o.output.switch.boolean(compare, reroute_4) >> result.next
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
                reroute_9 = g.Reroute(input=density)
                reroute_10 = g.Reroute(input=g.Reroute(input=selection).o.output)
                reroute_11 = g.Reroute(
                    input=g.Reroute(input=distribution_mask).o.output
                )
                reroute_12 = g.Reroute(input=g.Reroute(input=seed).o.output)
                reroute_13 = g.Reroute(
                    input=scatter_on_instances.switch.geometry(
                        g.SeparateComponents(geometry=mesh), mesh
                    )
                )
                attribute_statistic_3 = g.AttributeStatistic(
                    geometry=reroute_13, attribute=reroute_9, domain="CORNER"
                )
                reroute_14 = g.Reroute(input=reroute_13.o.output)
                reroute_15 = g.Reroute(
                    input=g.Reroute(
                        input=g.Reroute(input=menu_switch.o.poisson_disk).o.output
                    ).o.output
                )
                reroute_16 = g.Reroute(input=attribute_statistic_3.o.max)
                distribute_points_on_faces_1 = g.DistributePointsOnFaces(
                    mesh=reroute_14,
                    selection=reroute_10,
                    density=reroute_11.o.output * density,
                    seed=reroute_12,
                )
                reroute_17 = g.Reroute(input=reroute_15.o.output)
                reroute_18 = g.Reroute(input=reroute_16.o.output)
                distribute_points_on_faces_2 = g.DistributePointsOnFaces(
                    mesh=reroute_14,
                    selection=reroute_10,
                    distance_min=minimum_distance,
                    density_max=reroute_16,
                    density_factor=reroute_11.o.output
                    * (reroute_9.o.output / attribute_statistic_3.o.max),
                    seed=reroute_12,
                    distribute_method="POISSON",
                )
                switch_4 = reroute_15.o.output.switch.geometry(
                    distribute_points_on_faces_1, distribute_points_on_faces_2
                )
                switch_5 = reroute_17.o.output.switch.rotation(
                    distribute_points_on_faces_1.o.rotation,
                    distribute_points_on_faces_2.o.rotation,
                )
                switch_6 = g.Reroute(input=reroute_17.o.output).o.output.switch.vector(
                    distribute_points_on_faces_1.o.normal,
                    distribute_points_on_faces_2.o.normal,
                )
        reroute_19 = g.Reroute(input=pick_instance)
        separate_components = g.SeparateComponents(geometry=mesh)
        reroute_20 = g.Reroute(input=reroute_19.o.output)
        reroute_21 = g.Reroute(
            input=g.MenuSwitch.integer(
                density_method, {"Density": 0, "Amount": 1}
            ).o.amount
        )
        reroute_22 = g.Reroute(input=reroute_21.o.output)
        reroute_23 = g.Reroute(input=reroute_22.o.output)
        reroute_24 = g.Reroute(
            input=g.Reroute(input=reroute_23.o.output).o.output.switch.float(
                reroute_18, reroute_1
            )
        )
        with g.Frame("Instance Geometry"):
            menu_switch_1 = g.MenuSwitch.integer(
                instance_type, {"Object": 0, "Collection": 1}
            )
            reroute_25 = g.Reroute(input=scale)
            reroute_26 = g.Reroute(input=collection)
            reroute_27 = g.Reroute(input=instance)
            reroute_28 = g.Reroute(input=menu_switch_1.o.collection)
            reroute_29 = g.Reroute(
                input=g.MenuSwitch.integer(
                    input_type, {"Data-Block": 0, "Geometry": 1}
                ).o.geometry
            )
            reroute_30 = g.Reroute(
                input=reroute_19.o.output.switch.boolean(true=reset_transform)
            )
            switch_7 = reroute_30.o.output.switch.geometry(
                g.CollectionInfo(collection=reroute_26, separate_children=True),
                g.CollectionInfo(
                    collection=reroute_26, separate_children=True, reset_children=True
                ),
            )
            switch_8 = reroute_30.o.output.switch.geometry(
                reroute_27,
                g.SetInstanceTransform(
                    instances=reroute_27, transform=g.CombineTransform()
                ),
            )
            index_switch = g.IndexSwitch.geometry(
                menu_switch_1,
                (g.ObjectInfo(object=object, as_instance=True).o.geometry, switch_7),
            )
            index_switch_1 = g.IndexSwitch.geometry(
                reroute_29, (index_switch, switch_8)
            )
            integer_math = (
                g.DomainSize(geometry=index_switch_1).o.point_count
                + g.DomainSize(
                    geometry=index_switch_1, component="INSTANCES"
                ).o.instance_count
            )
            reroute_31 = g.Reroute(input=reroute_24.o.output)
            with g.Frame("Dummy Cube"):
                delete_geometry_1 = g.DeleteGeometry(
                    geometry=g.Cube(size=(0.31830987 / reroute_31) ** 0.5),
                    mode="ONLY_FACE",
                    domain="FACE",
                )
                geometry_to_instance = g.GeometryToInstance(delete_geometry_1)
            switch_9 = g.Compare.integer.equal(
                integer_math, 0
            ).o.result.switch.geometry(
                g.Reroute(input=g.Reroute(input=index_switch_1.o.output).o.output),
                geometry_to_instance,
            )
        switch_10 = g.Reroute(input=reroute_29.o.output).o.output.switch.boolean(
            g.Reroute(input=reroute_28.o.output).o.output.switch.boolean(
                true=reroute_20
            ),
            g.Reroute(input=reroute_20.o.output),
        )
        reroute_32 = g.Reroute(input=switch_10)
        with g.Frame("Instance Fallback"):
            reroute_33 = g.Reroute(input=reroute_32.o.output)
            reroute_34 = g.Reroute(input=switch_9)
            reroute_35 = g.Reroute(input=reroute_34.o.output)
            compare_1 = g.Compare.integer.equal(
                g.DomainSize(
                    geometry=reroute_34, component="INSTANCES"
                ).o.instance_count,
                0,
            )
            warning = g.Warning.info(
                reroute_33.o.output & compare_1,
                "Pick Instance is on, but there are no instances to pick from. Falling back to using input as instance.",
            )
            switch_11 = warning.o.show.switch.geometry(
                reroute_35, g.GeometryToInstance(reroute_35)
            )
        switch_12 = reroute_22.o.output.switch.rotation(switch_5, output.result)
        with g.Frame("Alignment"):
            reroute_36 = g.Reroute(input=switch_12)
            transform_direction = g.TransformDirection(
                transform=reroute_36, direction=(0.0, 0.0, 1.0)
            )
            reroute_37 = g.Reroute(input=reroute_36.o.output)
            index_switch_2 = g.IndexSwitch.rotation(
                g.MenuSwitch.integer(alignment_axis, {"X": 0, "Y": 1, "Z": 2}),
                (
                    g.AlignRotationToVector(
                        rotation=reroute_37, vector=transform_direction, axis="X"
                    ),
                    g.AlignRotationToVector(
                        rotation=reroute_37, vector=transform_direction, axis="Y"
                    ),
                    g.Reroute(input=reroute_37.o.output),
                ),
            )
            switch_13 = align_rotation.switch.rotation((0.0, 0.0, 0.0), index_switch_2)
        reroute_38 = g.Reroute(
            input=g.Reroute(
                input=reroute_23.o.output.switch.vector(switch_6, normal.result)
            ).o.output
        )
        switch_14 = reroute_21.o.output.switch.geometry(
            switch_4, g.Reroute(input=delete_geometry.o.geometry)
        )
        with g.Frame("Viewport Visibility"):
            reroute_39 = g.Reroute(input=switch_14)
            delete_geometry_2 = g.DeleteGeometry(
                geometry=reroute_39,
                selection=g.RandomValue(seed=g.HashValue(value=seed, seed=32351))
                > viewport_visibility,
            )
            switch_15 = ((viewport_visibility < 1.0) & g.IsViewport()).switch.geometry(
                reroute_39, delete_geometry_2
            )
        with g.Frame("Masking"):
            random_value = g.RandomValue.boolean(
                g.Math.subtract(
                    1.0, g.ImageTexture(image=image_mask, vector=uv_map).o.color
                ),
                seed=g.HashValue(value=seed, seed=-75381),
            )
            reroute_40 = g.Reroute(input=switch_15)
            switch_16 = (g.ImageInfo(image=image_mask) > 0).switch.geometry(
                reroute_40,
                g.DeleteGeometry(geometry=reroute_40, selection=random_value),
            )
            switch_17 = masking.switch.geometry(reroute_40, switch_16)
        with g.Frame("Normal Offset"):
            set_position = switch_17 >> g.SetPosition(
                offset=reroute_38.o.output * surface_offset
            )
        instance_on_points = g.Reroute(
            input=set_position.o.geometry
        ) >> g.InstanceOnPoints(
            instance=switch_11,
            pick_instance=reroute_33,
            instance_index=reroute_32.o.output.switch.integer(
                true=g.HashValue(value=g.ID(), seed=instance_seed)
            ),
            rotation=g.Reroute(input=switch_13),
            scale=g.Reroute(input=reroute_25.o.output),
        )
        with g.Frame("Randomization"):
            reroute_41 = g.Reroute(input=instance_on_points.o.instances)
            group = RandomizeTransforms(
                Instances=reroute_41,
                Offset=randomize_offset,
                Rotation=randomize_rotation,
                **{"Scale Axes": randomize_scale_axes},
                Flipping=randomize_flipping,
                Seed=g.HashValue(value=seed, seed=randomize_seed),
                _named_links=[("Scale", randomize_scale), ("Scale", randomize_scale_1)],
            )
            switch_18 = randomize.switch.geometry(reroute_41, group)
        reroute_42 = g.Reroute(input=switch_18)
        switch_19 = realize_instances.switch.geometry(
            reroute_42,
            g.RealizeInstances(geometry=reroute_42, realize_to_point_domain=True),
        )
        reroute_43 = g.Reroute(input=switch_19)
        join_geometry = g.JoinGeometry(
            geometry=(
                separate_components.o.curve,
                separate_components.o.grease_pencil,
                separate_components.o.point_cloud,
                separate_components.o.volume,
                separate_components.o.instances,
                reroute_43,
            )
        )
        (
            keep_surface.switch.geometry(
                scatter_on_instances.switch.geometry(join_geometry, reroute_43),
                g.JoinGeometry(geometry=(mesh, reroute_43)),
            )
            >> instances
        )

        density_method.default_value = "Density"
        distribution_method.default_value = "Random"
        input_type.default_value = "Data-Block"
        instance_type.default_value = "Object"
        alignment_axis.default_value = "Z"
        randomize_scale_axes.default_value = "Uniform"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (4600.0, 440.0),
            "Group Input": (30.4, -396.1),
            "Distribute Points on Faces": (1231.6, -84.2),
            "Instance on Points": (1813.0, 234.2),
            "Collection Info": (390.4, -516.1),
            "Distribute Points on Faces.001": (1230.5, -323.5),
            "Menu Switch": (230.4, -176.1),
            "Index Switch": (1010.4, -316.1),
            "Image Texture": (225.8, -265.8),
            "Reroute": (630.5, -323.5),
            "Reroute.001": (630.5, -343.5),
            "Reroute.002": (630.5, -363.5),
            "Group Input.001": (30.5, -363.5),
            "Switch": (1610.5, -83.5),
            "Switch.001": (1610.5, -243.5),
            "Reroute.003": (430.4, -1016.1),
            "Menu Switch.001": (-7575.8, 500.0),
            "Reroute.004": (1570.5, -143.5),
            "Random Value": (692.6, -260.0),
            "Reroute.006": (630.5, -383.5),
            "Group Input.002": (-7775.8, 480.0),
            "Delete Geometry": (892.6, -260.0),
            "Hash Value": (1147.4, -318.9),
            "Group Input.004": (960.2, -404.8),
            "Switch.002": (1321.6, -217.6),
            "Reroute.007": (652.5, 151.4),
            "Cube": (390.6, -55.9),
            "Geometry to Instance": (750.6, -35.9),
            "Switch.003": (2110.4, -236.1),
            "Domain Size": (1430.4, -236.1),
            "Domain Size.001": (1430.4, -356.1),
            "Integer Math": (1630.4, -256.1),
            "Compare.001": (1830.4, -256.1),
            "Delete Geometry.001": (570.6, -35.9),
            "Group Input.005": (-1880.0, 180.0),
            "Switch.004": (100.0, 100.0),
            "Switch.005": (735.5, -116.3),
            "Group Input.006": (561.0, -88.1),
            "Index Switch.001": (1210.4, -256.1),
            "Menu Switch.002": (230.4, -36.1),
            "Switch.007": (362.3, 167.9),
            "Group Input.010": (30.3, -321.4),
            "Group Input.011": (48.4, -508.9),
            "Hash Value.003": (255.7, -487.1),
            "Join Geometry": (3863.8, 225.1),
            "Group Input.012": (3520.0, 360.0),
            "Switch.006": (4400.0, 440.0),
            "Group Input.013": (4180.0, 520.0),
            "Realize Instances": (3302.8, 194.8),
            "Reroute.008": (3757.9, 240.9),
            "Switch.008": (3522.8, 294.8),
            "Group Input.014": (3274.9, 274.8),
            "Group Input.015": (370.5, -483.5),
            "Math.001": (1034.5, -350.6),
            "Switch.009": (1415.4, -36.3),
            "Group Input.016": (1175.4, -56.3),
            "Reroute.005": (812.6, -160.0),
            "Frame": (-2092.6, 820.0),
            "Frame.001": (-8183.7, 619.5),
            "Frame.003": (1053.1, -36.1),
            "Distribute Points on Faces.002": (1935.3, -484.5),
            "Group Input.017": (1437.5, -573.4),
            "Math.002": (1697.7, -558.8),
            "Frame.005": (30.4, -742.2),
            "Switch.012": (-3520.0, 460.0),
            "Switch.013": (-3520.0, 300.0),
            "Menu Switch.005": (-4154.3, 849.6),
            "Group Input.018": (-4339.7, 833.6),
            "Repeat Input.001": (1439.3, -190.7),
            "Repeat Output.001": (3641.4, -238.8),
            "Domain Size.002": (30.5, -116.3),
            "Compare": (270.5, -36.3),
            "Attribute Statistic": (690.5, -443.5),
            "Math": (870.5, -563.5),
            "Reroute.017": (590.5, -543.5),
            "Math.004": (3007.3, -457.4),
            "Switch.014": (3313.9, -36.0),
            "Switch.015": (3313.9, -176.0),
            "Reroute.019": (3267.3, -97.4),
            "Group Input.021": (420.2, -157.3),
            "Group Input.022": (30.3, -317.3),
            "Attribute Statistic.001": (463.6, -232.4),
            "Face Area": (43.6, -492.4),
            "Math.006": (677.5, -156.3),
            "Reroute.020": (-3560.0, 400.0),
            "Math.007": (30.5, -36.2),
            "Frame.006": (1087.6, -36.1),
            "Delete Geometry.002": (4111.2, -286.0),
            "Index.001": (3607.1, -540.0),
            "Compare.004": (3767.1, -500.0),
            "Group Input.023": (3607.1, -620.0),
            "Math.003": (673.3, -332.2),
            "Attribute Statistic.002": (458.8, -408.9),
            "Random Value.002": (3606.3, -696.8),
            "Sort Elements": (3926.2, -265.5),
            "Math.008": (55.5, -116.0),
            "Switch.016": (235.5, -36.0),
            "Math.009": (55.5, -136.0),
            "Math.012": (900.2, -198.3),
            "Math.011": (263.6, -492.4),
            "Clamp": (55.5, -196.0),
            "Frame.007": (30.4, -246.3),
            "Switch.017": (-3520.0, -20.0),
            "Switch.018": (3313.9, -456.0),
            "Math.005": (30.6, -95.9),
            "Math.010": (210.6, -95.9),
            "Reroute.021": (150.5, -56.3),
            "Reroute.022": (673.2, -137.4),
            "Group Input.003": (3219.9, -869.3),
            "Hash Value.001": (3415.0, -809.4),
            "Math.017": (1050.5, -543.5),
            "Reroute.009": (2927.3, -597.4),
            "Math.014": (1127.8, -453.0),
            "Attribute Statistic.003": (612.2, -529.3),
            "Integer": (1173.0, -159.4),
            "Reroute.014": (123.3, -41.2),
            "Reroute.015": (1330.5, -43.5),
            "Group Input.020": (394.6, -201.6),
            "Switch.019": (1116.6, -224.5),
            "Random Value.003": (398.5, -36.2),
            "Group Input.024": (30.3, -111.8),
            "Hash Value.002": (208.8, -113.2),
            "Compare.005": (576.8, -54.7),
            "Compare.006": (576.6, -182.3),
            "Delete Geometry.003": (931.8, -356.5),
            "Reroute.016": (888.8, -322.5),
            "Frame.002": (-3808.9, 1136.4),
            "Align Rotation to Vector": (295.5, -156.3),
            "Transform Direction": (95.5, -316.3),
            "Index Switch.003": (555.5, -156.3),
            "Align Rotation to Vector.001": (295.5, -316.3),
            "Reroute.011": (155.5, -136.3),
            "Reroute.012": (475.5, -136.3),
            "Reroute.013": (35.5, -236.3),
            "Menu Switch.004": (315.5, -56.3),
            "Group Input.019": (115.5, -36.3),
            "Math.013": (512.6, -260.0),
            "Image Info": (233.3, -204.7),
            "Compare.007": (519.0, -203.9),
            "Switch.010": (1098.1, -186.2),
            "Frame.004": (-3095.5, 336.3),
            "Boolean Math": (882.1, -186.9),
            "Is Viewport": (574.2, -294.3),
            "Switch.011": (778.0, -36.2),
            "Frame.013": (2054.5, 268.8),
            "Reroute.024": (3181.7, 184.1),
            "Group Input.008": (30.4, -263.3),
            "Group Input.026": (545.2, -74.7),
            "Reroute.023": (710.4, -136.1),
            "Switch.020": (830.4, -456.1),
            "Collection Info.001": (390.4, -676.1),
            "Group Input.007": (390.4, -456.1),
            "Reroute.025": (350.4, -676.1),
            "Object Info.001": (230.4, -316.1),
            "Switch.021": (830.4, -596.1),
            "Set Instance Transform": (630.4, -836.1),
            "Combine Transform": (450.4, -896.1),
            "Reroute.026": (410.4, -856.1),
            "Switch.022": (3313.9, -316.0),
            "Switch.023": (-3520.0, 140.0),
            "Set Position": (400.2, -36.0),
            "Vector Math.005": (229.0, -104.6),
            "Frame.011": (-364.1, 702.8),
            "Reroute.027": (-2227.0, -207.0),
            "Reroute.028": (-3148.3, -203.4),
            "Switch.024": (1610.5, -383.5),
            "Frame.012": (2176.7, -81.1),
            "Reroute.029": (35.5, -96.0),
            "Frame.014": (255.0, -160.2),
            "Switch.026": (3307.7, -590.6),
            "ID": (962.0, -313.3),
            "Group Input.031": (30.6, -216.3),
            "Group.006": (459.8, -173.0),
            "Reroute.031": (186.6, -123.6),
            "Hash Value.005": (249.9, -438.3),
            "Switch.025": (450.5, -203.5),
            "Group Input.027": (270.5, -163.5),
            "Separate Components": (270.5, -243.5),
            "Separate Components.001": (3740.0, 360.0),
            "Group Input.035": (3974.0, 495.8),
            "Switch.028": (4180.0, 440.0),
            "Join Geometry.001": (3980.0, 400.0),
            "Warning": (662.2, -51.5),
            "Reroute.018": (35.5, -222.9),
            "Domain Size.003": (107.2, -87.5),
            "Compare.002": (286.3, -65.8),
            "Boolean Math.001": (475.5, -42.9),
            "Switch.027": (837.2, -71.4),
            "Geometry to Instance.001": (586.9, -203.3),
            "Reroute.032": (533.9, -216.4),
            "Frame.008": (730.6, 188.9),
            "Reroute.037": (384.5, -41.2),
            "Reroute.033": (1163.7, -1120.0),
            "Reroute.035": (1676.6, 213.4),
            "Reroute.036": (1698.0, 268.1),
            "Reroute.038": (3267.3, -637.4),
            "Reroute.039": (3267.3, -237.4),
            "Reroute.040": (3267.3, -517.4),
            "Reroute.041": (3267.3, -377.4),
            "Reroute.030": (2287.3, -637.4),
            "Reroute.042": (2287.3, -597.4),
            "Reroute.044": (2867.3, -557.4),
            "Reroute.045": (3187.3, -537.4),
            "Reroute.043": (1447.8, -940.9),
            "Reroute.046": (4226.4, -943.8),
            "Reroute.047": (-3560.0, 240.0),
            "Reroute.048": (-3560.0, 80.0),
            "Reroute.049": (-3560.0, -80.0),
            "Reroute.050": (-3580.0, 360.0),
            "Reroute.051": (1570.5, -303.5),
            "Reroute.052": (1570.5, -443.5),
            "Reroute.053": (950.5, -363.5),
            "Reroute.054": (950.5, -343.5),
            "Reroute.055": (950.5, -323.5),
            "Reroute.056": (950.5, -383.5),
            "Reroute.057": (1108.6, -597.9),
            "Reroute.058": (1714.8, -599.5),
            "Reroute.059": (-360.0, 120.0),
            "Reroute.060": (710.4, -276.1),
            "Reroute.061": (-360.0, 40.0),
            "Reroute.062": (240.0, 160.0),
            "Reroute.010": (1950.4, -216.1),
            "Reroute.063": (1410.4, -216.1),
            "Frame.009": (-1970.4, -103.9),
            "Frame.010": (1099.8, -520.2),
            "Reroute.034": (862.3, -978.7),
            "Reroute.064": (-2811.8, -1076.8),
            "Reroute.065": (20.0, 160.0),
            "Reroute.066": (770.4, -496.1),
            "Switch.029": (590.4, -376.1),
            "Reroute.067": (-1640.0, 140.0),
        }


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
