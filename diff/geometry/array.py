# Node-group asset 'Array' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .randomize_transforms import RandomizeTransforms


class Array(CustomGeometryGroup):
    _name = "Array"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        geometry = tree.inputs.geometry(
            "Geometry", description="Geometry that is duplicated"
        )
        shape = tree.inputs.menu(
            "Shape",
            description="Method used for arranging the duplicates",
            optional_label=True,
        )
        count_method = tree.inputs.menu(
            "Count Method",
            description="Method to choose the number of duplicates",
            expanded=True,
            optional_label=True,
        )
        count = tree.inputs.integer(
            "Count",
            3,
            description="The number of copies to generate",
            min_value=1,
            max_value=10000,
        )
        distance = tree.inputs.float(
            "Distance",
            1.0,
            description="The distance along the curve between copies",
            min_value=0.01,
            subtype="DISTANCE",
        )
        angular_distance = tree.inputs.float(
            "Angular Distance",
            0.7853982,
            description="The angle along the circle arc between copies",
            min_value=0.017453292,
            max_value=6.2831855,
            subtype="ANGLE",
        )
        per_curve = tree.inputs.boolean(
            "Per Curve",
            True,
            description="Specify the number of copies for each curve separately",
        )
        offset_method = tree.inputs.menu(
            "Offset Method",
            description="Method to interpret the offset parameters",
            expanded=True,
            optional_label=True,
        )
        transform_reference = tree.inputs.menu(
            "Transform Reference",
            description="Define the transform locally or with an object's transform",
            expanded=True,
            optional_label=True,
        )
        translation = tree.inputs.vector(
            "Translation",
            (1.0, 0.0, 0.0),
            description="Translation accumulated for each copy",
            subtype="TRANSLATION",
        )
        offset = tree.inputs.vector(
            "Offset",
            (1.0, 0.0, 0.0),
            description="Amount to move each copy relative to its bounding box size",
            subtype="XYZ",
        )
        rotation = tree.inputs.rotation(
            "Rotation",
            (0.0, 0.0, 0.0),
            description="Rotation accumulated for each copy",
        )
        scale = tree.inputs.vector(
            "Scale",
            (1.0, 1.0, 1.0),
            description="Scale accumulated for each copy",
            subtype="XYZ",
        )
        central_axis = tree.inputs.menu(
            "Central Axis",
            description="The up direction for the circle shape",
            expanded=True,
            optional_label=True,
        )
        circle_segment = tree.inputs.menu(
            "Circle Segment",
            description="Whether the copies should fan out in a full circle or an arc",
            expanded=True,
            optional_label=True,
        )
        sweep_angle = tree.inputs.float(
            "Sweep Angle",
            3.1415927,
            description="Total angle used to fan out the copies in a circular arc",
            min_value=0.0,
            max_value=6.2831855,
            subtype="ANGLE",
        )
        radius = tree.inputs.float(
            "Radius",
            0.0,
            description="Distance of the instances from the origin",
            min_value=0.0,
            subtype="DISTANCE",
        )
        transform_object = tree.inputs.object(
            "Transform Object",
            description="Reference object to define the accumulated transform",
        )
        curve_object = tree.inputs.object(
            "Curve Object", description="Reference curve object for array"
        )
        relative_space = tree.inputs.boolean(
            "Relative Space",
            True,
            description="Use relative space for the input geometry so the transforms of both inputs in relation are considered",
        )
        realize_instances = tree.inputs.boolean(
            "Realize Instances",
            True,
            description="Turn the output into a single geometry rather than instances (required by many other modifiers)",
        )
        with tree.inputs.panel("Align Rotation", default_closed=True):
            align_rotation = tree.inputs.boolean(
                "Align Rotation",
                True,
                description="Rotate copies based on the array shape",
                structure_type="SINGLE",
                is_panel_toggle=True,
            )
            local_rotation = tree.inputs.rotation(
                "Local Rotation",
                (0.0, 0.0, 0.0),
                description="Local rotation of the instances to tune the rotation alignment",
                optional_label=True,
                structure_type="SINGLE",
            )
        with tree.inputs.panel("Randomize", default_closed=True):
            randomize = tree.inputs.boolean(
                "Randomize",
                False,
                description="Randomize transforms between all copies",
                structure_type="SINGLE",
                is_panel_toggle=True,
            )
            randomize_offset = tree.inputs.vector(
                "Randomize Offset",
                (0.0, 0.0, 0.0),
                description="Offset the copies randomly",
                min_value=-10000.0,
                max_value=10000.0,
                structure_type="SINGLE",
                subtype="XYZ",
            )
            randomize_rotation = tree.inputs.vector(
                "Randomize Rotation",
                (0.0, 0.0, 0.0),
                description="Rotate the copies randomly",
                structure_type="SINGLE",
                subtype="EULER",
            )
            randomize_scale_axes = tree.inputs.menu(
                "Randomize Scale Axes",
                description="Whether to apply random scale uniformly or per axis",
                expanded=True,
                optional_label=True,
                structure_type="SINGLE",
            )
            randomize_scale = tree.inputs.vector(
                "Randomize Scale",
                (0.0, 0.0, 0.0),
                description="Scale the copies randomly per axis",
                min_value=0.0,
                max_value=1.0,
                structure_type="SINGLE",
                subtype="XYZ",
            )
            randomize_scale_1 = tree.inputs.float(
                "Randomize Scale",
                0.0,
                description="Scale the copies randomly",
                min_value=0.0,
                max_value=1.0,
                structure_type="SINGLE",
                subtype="FACTOR",
            )
            randomize_flipping = tree.inputs.vector(
                "Randomize Flipping",
                (0.0, 0.0, 0.0),
                description="Flip a fraction of copies along individual axes",
                min_value=0.0,
                max_value=1.0,
                structure_type="SINGLE",
                subtype="FACTOR",
            )
            exclude_first = tree.inputs.boolean(
                "Exclude First",
                True,
                description="Exclude the first (original) copy from randomization",
                structure_type="SINGLE",
            )
            exclude_last = tree.inputs.boolean(
                "Exclude Last",
                False,
                description="Exclude the last copy from randomization",
                structure_type="SINGLE",
            )
            seed = tree.inputs.integer(
                "Seed",
                0,
                description="Base value to control random variation in a reproducible way",
                min_value=-10000,
                max_value=10000,
                structure_type="SINGLE",
            )
        with tree.inputs.panel("Merge", default_closed=True):
            merge = tree.inputs.boolean(
                "Merge",
                False,
                description="Merge overlapping points by their distance. (Realize Instances must be enabled).",
                is_panel_toggle=True,
            )
            merge_distance = tree.inputs.float(
                "Merge Distance",
                0.001,
                description="Distance below which points will be merged",
                min_value=0.0,
                subtype="DISTANCE",
            )
        geometry_1 = tree.outputs.geometry("Geometry", description="Resulting Geometry")

        with g.Frame("Transform Instances"):
            combine_transform = g.CombineTransform(
                translation=translation, rotation=rotation, scale=scale
            )
            transform_gizmo = g.TransformGizmo(
                value=(combine_transform,),
                position=translation,
                rotation=rotation,
                use_translation_x=True,
                use_translation_y=True,
                use_translation_z=True,
                use_rotation_x=True,
                use_rotation_y=True,
                use_rotation_z=True,
                use_scale_x=True,
                use_scale_y=True,
                use_scale_z=True,
            )
            switch = relative_space.switch.matrix(
                g.ObjectInfo(object=transform_object),
                g.ObjectInfo(object=transform_object, transform_space="RELATIVE"),
            )
            reroute = g.Reroute(
                input=g.MenuSwitch.integer(
                    transform_reference, {"Inputs": 0, "Object": 1}
                ).o.output
            )
            index_switch = g.IndexSwitch.matrix(reroute, (combine_transform, switch))
            set_instance_transform = (
                g.Points(count=count, radius=0.1)
                >> g.InstanceOnPoints(instance=geometry)
                >> g.SetInstanceTransform(
                    transform=index_switch.o.output.instance.trailing()
                )
            )
            sample_index = g.SampleIndex(
                geometry=set_instance_transform,
                value=g.InstanceTransform(),
                index=count - 1,
                data_type="FLOAT4X4",
                domain="INSTANCE",
            )
            combine_transform_1 = g.CombineTransform(
                rotation=sample_index.o.value.rotation, scale=sample_index.o.value.scale
            )
            reroute_1 = g.Reroute(input=sample_index.o.value.translation)
            linear_gizmo = g.LinearGizmo(
                value=(
                    count
                    * index_switch.o.output.translation.transform(
                        combine_transform_1
                    ).length(),
                ),
                position=reroute_1,
                direction=reroute_1,
                draw_style="CROSS",
            )
            join_geometry = g.JoinGeometry(
                geometry=(
                    g.IndexSwitch.geometry(reroute, (transform_gizmo, None)),
                    linear_gizmo,
                )
            )
        menu_switch = g.MenuSwitch.integer(circle_segment, {"Full": 0, "Arc": 1})
        hash_value = g.HashValue(value=seed, seed=1000)
        reroute_2 = g.Reroute(
            input=g.MenuSwitch.integer(
                offset_method, {"Relative": 0, "Offset": 1, "Endpoint": 2}
            ).o.output
        )
        bounding_box = (
            geometry
            >> g.RealizeInstances(realize_to_point_domain=True)
            >> g.BoundingBox()
        )
        reroute_3 = g.Reroute(
            input=g.MenuSwitch.integer(
                count_method, {"Count": 0, "Distance": 1}
            ).o.output
        )
        with g.Frame("Circle Gizmos"):
            linear_gizmo_1 = g.LinearGizmo(
                value=(radius,),
                position=g.VectorMath.scale((0.0, 1.0, 0.0), radius),
                direction=(0.0, 1.0, 0.0),
                draw_style="BOX",
            )
            switch_1 = g.Compare.integer.equal(menu_switch, 1).o.result.switch.geometry(
                true=g.DialGizmo(value=(sweep_angle,), color_id="SECONDARY")
            )
            switch_2 = g.Switch.geometry(
                reroute_3,
                g.LinearGizmo(
                    value=(count,), direction=(0.0, 1.0, 0.0), draw_style="CROSS"
                ),
                g.DialGizmo(value=(angular_distance,), radius=0.8),
            )
            join_geometry_1 = g.JoinGeometry(
                geometry=(switch_1, linear_gizmo_1, switch_2)
            )
        reroute_4 = g.Reroute(input=reroute_3.o.output)
        with g.Frame("Circle Instances"):
            reroute_5 = g.Reroute(input=g.Index().o.index)
            menu_switch_1 = g.MenuSwitch.integer(central_axis, {"X": 0, "Y": 1, "Z": 2})
            index_switch_1 = g.IndexSwitch.rotation(
                menu_switch_1,
                ((1.5707964, 0.0, 1.5707964), (1.5707964, 0.0, 0.0), (0.0, 0.0, 0.0)),
            )
            warning = g.Warning(
                show=g.Compare.float.equal(angular_distance, 0.0, 0.0),
                message="Invalid Distance",
            )
            reroute_6 = g.Reroute(input=menu_switch.o.output)
            reroute_7 = g.Reroute(input=index_switch_1.o.output)
            reroute_8 = g.Reroute(input=reroute_6.o.output)
            math = abs(
                g.IndexSwitch.float(reroute_6, (6.2831855, sweep_angle)).o.output
                / angular_distance
            )
            transform_geometry = g.Reroute(
                input=g.Reroute(input=join_geometry_1.o.geometry).o.output
            ) >> g.TransformGeometry(
                transform=g.Reroute(input=reroute_7.o.output), mode="Matrix"
            )
            switch_3 = warning.o.show.switch.integer(
                g.FloatToInteger(float=math.max(1.0), rounding_mode="FLOOR").o.integer
                + reroute_8,
                1,
            )
            switch_4 = g.Switch.integer(
                g.Reroute(input=g.Reroute(input=reroute_4.o.output).o.output),
                count,
                switch_3,
            )
            reroute_9 = g.Reroute(input=switch_4.o.output)
            index_switch_2 = g.IndexSwitch.float(
                g.Reroute(input=reroute_8.o.output),
                (
                    g.Math.divide(reroute_5, reroute_9).o.value * 6.2831855,
                    g.Math.divide(reroute_5, reroute_9.o.output - 1).o.value
                    * sweep_angle,
                ),
            )
            reroute_10 = g.Reroute(input=index_switch_2.o.output)
            reroute_11 = g.Reroute(input=reroute_10.o.output)
            index_switch_3 = g.IndexSwitch.vector(
                menu_switch_1,
                (
                    g.CombineXYZ(x=reroute_11),
                    g.CombineXYZ(y=reroute_11.o.output * -1.0),
                    g.CombineXYZ(z=reroute_11),
                ),
            )
            rotate_rotation = g.RotateRotation(
                rotation=index_switch_3,
                rotate_by=local_rotation,
                rotation_space="LOCAL",
            )
            switch_5 = align_rotation.switch.rotation(
                (0.0, 0.0, 0.0),
                g.IndexSwitch.rotation(items=(rotate_rotation, (1.5707964, 0.0, 0.0))),
            )
            instance_on_points = (
                g.Points(count=switch_4, radius=0.1)
                >> g.SetPosition(
                    position=g.CombineXYZ(y=radius).o.vector.rotate(
                        g.CombineXYZ(z=reroute_10)
                    )
                )
                >> g.TransformGeometry(transform=reroute_7, mode="Matrix")
                >> g.InstanceOnPoints(instance=geometry, rotation=switch_5)
            )
        vector_math = offset * (bounding_box.o.max - bounding_box.o.min)
        with g.Frame("Line Gismoz"):
            reroute_12 = g.Reroute(input=count)
            reroute_13 = g.Reroute(input=rotation)
            integer_math = reroute_12.o.output - 1
            reroute_14 = g.Reroute(input=reroute_13.o.output)
            math_1 = 1.0 / integer_math
            reroute_15 = g.Reroute(input=reroute_2.o.output)
            compare = g.Compare.integer.not_equal(reroute_2, 0)
            reroute_16 = g.Reroute(input=vector_math)
            reroute_17 = g.Reroute(
                input=compare.o.result.switch.vector(reroute_16, translation)
            )
            reroute_18 = g.Reroute(input=reroute_17.o.output)
            reroute_19 = g.Reroute(input=reroute_17.o.output)
            reroute_20 = g.Reroute(input=reroute_18.o.output)
            reroute_21 = g.Reroute(input=reroute_18.o.output)
            transform_gizmo_1 = g.TransformGizmo(
                value=(
                    g.CombineTransform(
                        translation=translation, rotation=reroute_13, scale=scale
                    ),
                ),
                position=reroute_19,
                rotation=reroute_14,
                use_translation_x=True,
                use_translation_y=True,
                use_translation_z=True,
                use_rotation_x=True,
                use_rotation_y=True,
                use_rotation_z=True,
                use_scale_x=True,
                use_scale_y=True,
                use_scale_z=True,
            )
            transform_gizmo_2 = g.TransformGizmo(
                value=(
                    g.CombineTransform(
                        translation=reroute_16, rotation=reroute_13, scale=scale
                    ),
                ),
                position=reroute_19,
                rotation=reroute_14,
                use_translation_x=True,
                use_translation_y=True,
                use_translation_z=True,
                use_rotation_x=True,
                use_rotation_y=True,
                use_rotation_z=True,
                use_scale_x=True,
                use_scale_y=True,
                use_scale_z=True,
            )
            reroute_22 = g.Reroute(input=reroute_18.o.output * integer_math)
            switch_6 = compare.o.result.switch.geometry(
                transform_gizmo_2, transform_gizmo_1
            )
            vector_math_1 = g.IndexSwitch.vector(
                reroute_15, (reroute_20, reroute_20, reroute_18.o.output * math_1)
            ).o.output.length()
            linear_gizmo_2 = g.LinearGizmo(
                value=(reroute_12.o.output * vector_math_1,),
                position=g.IndexSwitch.vector(
                    reroute_15, (reroute_22, reroute_22, reroute_18)
                ),
                direction=reroute_21,
                draw_style="CROSS",
            )
        reroute_23 = g.Reroute(input=reroute_4.o.output)
        reroute_24 = g.Reroute(input=reroute_23.o.output)
        with g.Frame("Curve Instances"):
            switch_7 = relative_space.switch.geometry(
                g.ObjectInfo(object=curve_object).o.geometry,
                g.ObjectInfo(
                    object=curve_object, transform_space="RELATIVE"
                ).o.geometry,
            )
            with g.Frame("Single Curve Fallback"):
                compare_1 = g.Compare.integer.equal(
                    g.DomainSize(geometry=switch_7, component="CURVE").o.spline_count, 1
                )
                switch_8 = compare_1.o.result.switch.boolean(per_curve, True)
            compare_2 = g.Compare.integer.equal(
                g.DomainSize(geometry=switch_7, component="CURVE").o.spline_count, 0
            )
            reroute_25 = g.Reroute(
                input=g.Warning(
                    show=compare_2, message="No Curve Selected"
                ).o.show.switch.geometry(switch_7)
            )
            reroute_26 = g.Reroute(input=g.Reroute(input=switch_8).o.output)
            with g.Frame("Distance Method"):
                index = g.Index()
                reroute_27 = g.Reroute(input=distance)
                boolean_math = ~g.IsSplineCyclic().o.cyclic
                integer_math_1 = (
                    g.FloatToInteger(
                        float=g.SplineLength().o.length / reroute_27,
                        rounding_mode="FLOOR",
                    ).o.integer
                    + 1
                )
                reroute_28 = g.Reroute(input=reroute_25.o.output)
                curve_length = g.CurveLength(curve=reroute_25)
                reroute_29 = g.Reroute(input=reroute_26.o.output)
                capture = g.CaptureAttribute.curve(geometry=reroute_28)
                value = capture.items.integer("Value", integer_math_1)
                index_1 = capture.items.integer("Index", g.Index())
                reroute_30 = g.Reroute(input=reroute_28.o.output)
                reroute_31 = g.Reroute(input=reroute_29.o.output)
                resample_curve = g.ResampleCurve(
                    curve=capture.o.geometry,
                    count=value.output,
                    length=3.6699998,
                    keep_last_segment=True,
                )
                sample_index_1 = g.SampleIndex(
                    geometry=capture.o.geometry,
                    value=value.output.spline.total(),
                    data_type="INT",
                    domain="CURVE",
                )
                reroute_32 = g.Reroute(input=resample_curve.o.curve)
                integer_math_2 = (
                    g.FloatToInteger(
                        float=curve_length.o.length / reroute_27, rounding_mode="FLOOR"
                    ).o.integer
                    + 1
                )
                points = g.Points(count=sample_index_1, radius=0.1)
                sample_index_2 = g.SampleIndex(
                    geometry=reroute_32,
                    value=g.SplineParameter().o.index,
                    index=index,
                    data_type="INT",
                )
                capture_1 = g.CaptureAttribute.point(geometry=points)
                curve_index = capture_1.items.integer(
                    "Curve Index",
                    g.SampleIndex(
                        geometry=reroute_32,
                        value=index_1.output,
                        index=index,
                        data_type="INT",
                    ),
                )
                index_in_curve = capture_1.items.integer(
                    "Index in Curve", sample_index_2
                )
                sample_curve = g.SampleCurve(
                    curves=reroute_30,
                    length=g.Math.divide(g.Index(), integer_math_2).o.value
                    * curve_length,
                    mode="LENGTH",
                    use_all_curves=True,
                )
                sample_curve_1 = g.SampleCurve(
                    curves=reroute_30,
                    length=index_in_curve.output * reroute_27,
                    curve_index=curve_index.output,
                    mode="LENGTH",
                )
                hash_value_1 = g.HashValue(
                    value=g.HashValue(
                        value=curve_index.output, seed=index_in_curve.output
                    ),
                    seed=seed,
                )
                switch_9 = reroute_29.o.output.switch.integer(
                    g.HashValue(value=g.Index(), seed=seed), hash_value_1
                )
                capture_2 = g.CaptureAttribute.point(
                    geometry=reroute_29.o.output.switch.geometry(
                        points, capture_1.o.geometry
                    )
                )
                position = capture_2.items.vector(
                    "Position",
                    reroute_31.o.output.switch.vector(
                        sample_curve.o.position, sample_curve_1.o.position
                    ),
                )
                tangent = capture_2.items.vector(
                    "Tangent",
                    reroute_31.o.output.switch.vector(
                        sample_curve.o.tangent, sample_curve_1.o.tangent
                    ),
                )
                normal = capture_2.items.vector(
                    "Normal",
                    reroute_31.o.output.switch.vector(
                        sample_curve.o.normal, sample_curve_1.o.normal
                    ),
                )
                axes_to_rotation = g.AxesToRotation(
                    primary_axis=tangent.output,
                    secondary_axis=normal.output,
                    primary="X",
                    secondary="Z",
                )
                switch_10 = align_rotation.switch.rotation(
                    (0.0, 0.0, 0.0),
                    axes_to_rotation.o.rotation.rotate(
                        local_rotation, rotation_space="LOCAL"
                    ),
                )
                instance_on_points_1 = g.Warning(
                    show=g.Compare.float.equal(distance, 0.0, 0.0),
                    message="Invalid Distance",
                ).o.show.switch.geometry(
                    capture_2.o.geometry
                    >> g.SetID(id=switch_9)
                    >> g.SetPosition(position=position.output),
                    g.Points(radius=0.1),
                ) >> g.InstanceOnPoints(instance=geometry, rotation=switch_10)
            with g.Frame("Count Method"):
                reroute_33 = g.Reroute(input=count)
                reroute_34 = g.Reroute(input=g.Index().o.index)
                reroute_35 = g.Reroute(input=reroute_34.o.output)
                reroute_36 = g.Reroute(input=reroute_34.o.output / count)
                reroute_37 = g.Reroute(input=reroute_36.o.output)
                reroute_38 = g.Reroute(input=reroute_37.o.output)
                integer_math_3 = reroute_35.o.output - reroute_37.o.output * reroute_33
                reroute_39 = g.Reroute(input=reroute_25.o.output)
                reroute_40 = g.Reroute(input=reroute_26.o.output)
                reroute_41 = g.Reroute(input=reroute_39.o.output)
                sample_index_3 = g.SampleIndex(
                    geometry=reroute_39,
                    value=boolean_math,
                    index=reroute_36,
                    data_type="INT",
                    domain="CURVE",
                )
                switch_11 = reroute_40.o.output.switch.integer(
                    g.HashValue(value=g.Index(), seed=seed),
                    g.HashValue(
                        value=g.HashValue(value=reroute_38, seed=integer_math_3),
                        seed=seed,
                    ),
                )
                sample_curve_2 = g.SampleCurve(
                    curves=reroute_41,
                    factor=g.Math.divide(reroute_35, reroute_33.o.output - 1),
                    use_all_curves=True,
                )
                switch_12 = g.Reroute(input=switch_8).o.output.switch.integer(
                    count,
                    count
                    * g.DomainSize(
                        geometry=reroute_39, component="CURVE"
                    ).o.spline_count,
                )
                sample_curve_3 = g.SampleCurve(
                    curves=reroute_41,
                    factor=g.Math.divide(
                        integer_math_3, reroute_33.o.output - sample_index_3
                    ),
                    curve_index=reroute_38,
                )
                capture_3 = g.CaptureAttribute.point(
                    geometry=g.Points(count=switch_12, radius=0.1)
                )
                position_1 = capture_3.items.vector(
                    "Position",
                    reroute_40.o.output.switch.vector(
                        sample_curve_2.o.position, sample_curve_3.o.position
                    ),
                )
                tangent_1 = capture_3.items.vector(
                    "Tangent",
                    reroute_40.o.output.switch.vector(
                        sample_curve_2.o.tangent, sample_curve_3.o.tangent
                    ),
                )
                normal_1 = capture_3.items.vector(
                    "Normal",
                    reroute_40.o.output.switch.vector(
                        sample_curve_2.o.normal, sample_curve_3.o.normal
                    ),
                )
                axes_to_rotation_1 = g.AxesToRotation(
                    primary_axis=tangent_1.output,
                    secondary_axis=normal_1.output,
                    primary="X",
                    secondary="Z",
                )
                switch_13 = align_rotation.switch.rotation(
                    (0.0, 0.0, 0.0),
                    axes_to_rotation_1.o.rotation.rotate(
                        local_rotation, rotation_space="LOCAL"
                    ),
                )
                instance_on_points_2 = (
                    capture_3.o.geometry
                    >> g.SetID(id=switch_11)
                    >> g.SetPosition(position=position_1.output)
                    >> g.InstanceOnPoints(instance=geometry, rotation=switch_13)
                )
            switch_14 = g.Switch.geometry(
                reroute_24, instance_on_points_2, instance_on_points_1
            )
        with g.Frame("Curve Gizmos"):
            reroute_42 = g.Reroute(input=switch_7)
            sample_curve_4 = g.SampleCurve(curves=reroute_42)
            sample_curve_5 = g.SampleCurve(
                curves=reroute_42, length=distance, mode="LENGTH"
            )
            linear_gizmo_3 = g.LinearGizmo(
                value=(count,),
                position=sample_curve_4.o.position,
                direction=sample_curve_4.o.tangent,
                draw_style="CROSS",
            )
            linear_gizmo_4 = g.LinearGizmo(
                value=(distance,),
                position=sample_curve_5.o.position,
                direction=sample_curve_5.o.tangent,
                draw_style="CROSS",
            )
        reroute_43 = g.Reroute(
            input=g.Switch.geometry(
                g.Reroute(input=reroute_23.o.output), linear_gizmo_3, linear_gizmo_4
            ).o.output
        )
        join_geometry_2 = g.JoinGeometry(geometry=(linear_gizmo_2, switch_6))
        with g.Frame("Line Instances"):
            reroute_44 = g.Reroute(input=math_1)
            reroute_45 = g.Reroute(input=reroute_15.o.output)
            with g.Frame("Position"):
                reroute_46 = g.Reroute(input=reroute_21.o.output)
                reroute_47 = g.Reroute(input=reroute_46.o.output)
                index_switch_4 = g.IndexSwitch.vector(
                    g.Reroute(input=reroute_45.o.output),
                    (reroute_47, reroute_47, reroute_46.o.output * reroute_44),
                )
                set_position = g.Points(count=count, radius=0.1) >> g.SetPosition(
                    position=index_switch_4.o.output * g.Index()
                )
            reroute_48 = g.Reroute(input=g.Reroute(input=reroute_45.o.output).o.output)
            with g.Frame("Rotation"):
                reroute_49 = g.Reroute(input=rotation)
                reroute_50 = g.Reroute(input=reroute_49.o.output)
                index_switch_5 = g.IndexSwitch.rotation(
                    reroute_48,
                    (
                        reroute_50,
                        reroute_50,
                        reroute_44.o.output.mix.rotation((0.0, 0.0, 0.0), reroute_49),
                    ),
                )
                mix = g.Mix.rotation(g.Index(), b_rotation=index_switch_5)
            with g.Frame("Scale"):
                integer_math_4 = count - 1
                reroute_51 = g.Reroute(input=scale)
                reroute_52 = g.Reroute(
                    input=g.Mix.vector(
                        integer_math_4, (1.0, 1.0, 1.0), reroute_51
                    ).o.result_vector
                )
                mix_1 = g.Math.divide(g.Index(), integer_math_4).o.value.mix.vector(
                    (1.0, 1.0, 1.0),
                    g.IndexSwitch.vector(
                        reroute_48, (reroute_52, reroute_52, reroute_51)
                    ),
                )
            instance_on_points_3 = set_position >> g.InstanceOnPoints(
                instance=geometry, rotation=mix.o.result_rotation, scale=mix_1
            )
            reroute_53 = g.Reroute(
                input=g.Reroute(input=join_geometry_2.o.geometry).o.output
            )
        index_switch_6 = g.IndexSwitch.geometry(
            g.MenuSwitch.integer(
                shape, {"Line": 0, "Circle": 1, "Curve": 2, "Transform": 3}
            ),
            (
                g.JoinGeometry(geometry=(instance_on_points_3, reroute_53)),
                g.JoinGeometry(geometry=(instance_on_points, transform_geometry)),
                g.JoinGeometry(geometry=(switch_14, reroute_43)),
                g.JoinGeometry(geometry=(set_instance_transform, join_geometry)),
            ),
        )
        with g.Frame("Store Info"):
            capture_4 = g.CaptureAttribute.instance(geometry=index_switch_6)
            random = capture_4.items.vector(
                "random",
                g.RandomValue.vector((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), seed=hash_value),
            )
            instance_index = capture_4.items.integer("instance_index", g.Index())
            store_named_attribute = (
                capture_4.o.geometry
                >> g.StoreNamedAttribute.instance.vector(
                    name="instance_random", value=random.output
                )
                >> g.StoreNamedAttribute.instance.integer(
                    name="instance_index", value=instance_index.output
                )
            )
        reroute_54 = g.Reroute(input=store_named_attribute.o.geometry)
        with g.Frame("Randomization"):
            index_2 = g.Index()
            switch_15 = exclude_first.switch.boolean(
                True, g.Compare.integer.not_equal(index_2, 0)
            )
            reroute_55 = g.Reroute(input=reroute_54.o.output)
            compare_3 = g.Compare.integer.not_equal(
                index_2,
                g.DomainSize(
                    geometry=reroute_54, component="INSTANCES"
                ).o.instance_count
                - 1,
            )
            group = RandomizeTransforms(
                Instances=reroute_55,
                Selection=exclude_last.switch.boolean(switch_15, switch_15 & compare_3),
                Offset=randomize_offset,
                Rotation=randomize_rotation,
                **{"Scale Axes": randomize_scale_axes},
                Flipping=randomize_flipping,
                Seed=seed,
                _named_links=[("Scale", randomize_scale), ("Scale", randomize_scale_1)],
            )
            switch_16 = randomize.switch.geometry(reroute_55, group)
        with g.Frame("Merge Instances"):
            reroute_56 = g.Reroute(input=switch_16)
            reroute_57 = g.Reroute(
                input=g.RealizeInstances(
                    geometry=reroute_56, realize_to_point_domain=True
                ).o.geometry
            )
            switch_17 = merge.switch.geometry(
                reroute_57,
                g.MergeByDistance(geometry=reroute_57, distance=merge_distance),
            )
            realize_instances.switch.geometry(reroute_56, switch_17) >> geometry_1

        shape.default_value = "Line"
        count_method.default_value = "Count"
        offset_method.default_value = "Relative"
        transform_reference.default_value = "Inputs"
        central_axis.default_value = "Z"
        circle_segment.default_value = "Full"
        randomize_scale_axes.default_value = "Uniform"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (4305.5, -102.9),
            "Group Input": (-1992.8, 1426.2),
            "Instance on Points": (1327.9, -331.8),
            "Menu Switch": (-1812.8, 1446.2),
            "Linear Gizmo": (1949.5, -200.7),
            "Group Input.003": (189.5, -240.7),
            "Group Input.004": (2086.4, -108.9),
            "Join Geometry": (-1541.0, 582.3),
            "Group Input.005": (1135.6, -374.9),
            "Vector Math.001": (1189.5, -520.7),
            "Integer Math": (509.5, -380.7),
            "Join Geometry.001": (-5021.7, 556.4),
            "Vector Math.002": (1569.5, -120.7),
            "Math": (1749.5, -140.7),
            "Group Input.006": (29.5, -980.7),
            "Reroute.001": (1069.5, -460.7),
            "Index": (1265.4, -388.9),
            "Math.001": (1595.7, -385.7),
            "Math.002": (1775.7, -505.7),
            "Menu Switch.001": (2599.2, -338.7),
            "Group Input.009": (2419.2, -318.7),
            "Switch.001": (3899.2, -238.7),
            "Group Input.010": (3719.2, -258.7),
            "Index Switch.005": (2779.2, -338.7),
            "Join Geometry.002": (1054.5, -180.0),
            "Dial Gizmo": (229.3, -196.1),
            "Transform Geometry.001": (4079.9, -748.9),
            "Points": (495.4, -65.2),
            "Set Position": (714.2, -76.0),
            "Group Input.014": (29.1, -96.0),
            "Set Position.001": (2929.0, -88.9),
            "Combine XYZ.003": (2266.4, -108.9),
            "Rotate Vector": (2746.4, -128.9),
            "Combine XYZ.004": (2566.4, -188.9),
            "Linear Gizmo.001": (789.3, -236.1),
            "Group Input.015": (429.3, -296.1),
            "Vector Math": (609.3, -356.1),
            "Switch.002": (1569.5, -820.7),
            "Transform Gizmo.001": (1309.5, -960.7),
            "Combine Transform.003": (929.5, -980.7),
            "Reroute.010": (2979.2, -338.7),
            "Menu Switch.002": (-8170.7, 1089.8),
            "Index Switch.006": (294.2, -156.0),
            "Index Switch.007": (509.4, -175.8),
            "Reroute.008": (789.5, -960.7),
            "Math.003": (889.5, -320.7),
            "Vector Math.008": (94.2, -196.0),
            "Reroute.011": (-7828.6, 980.0),
            "Group Input.016": (-8370.7, 1069.8),
            "Index Switch.008": (1429.5, -400.7),
            "Reroute.009": (1189.5, -40.7),
            "Index Switch.010": (1369.5, -100.7),
            "Vector Math.003": (1169.5, -220.7),
            "Index Switch.009": (-260.0, -180.0),
            "Instance on Points.001": (4124.8, -86.3),
            "Group Input.017": (3879.2, -158.7),
            "Join Geometry.003": (-570.9, -282.5),
            "Points.002": (2747.6, -76.2),
            "Index.001": (529.4, -35.8),
            "Frame.006": (-5099.2, 98.7),
            "Frame.007": (-3146.9, 1184.1),
            "Reroute.002": (34.2, -193.2),
            "Index Switch.011": (709.1, -196.0),
            "Reroute.003": (34.2, -594.2),
            "Reroute.007": (409.5, -300.7),
            "Index.002": (549.1, -36.0),
            "Math.004": (729.1, -36.0),
            "Integer Math.001": (269.1, -56.0),
            "Mix": (909.1, -36.0),
            "Reroute.005": (34.2, -156.0),
            "Reroute.012": (174.2, -634.2),
            "Group Input.021": (909.1, -336.1),
            "Switch.003": (1449.1, -36.1),
            "Mix.001": (489.1, -116.0),
            "Group Input.022": (1209.1, -36.1),
            "Vector Math.006": (-7452.8, 189.8),
            "Group Input.025": (-8292.8, 109.8),
            "Bounding Box": (-7932.8, 109.8),
            "Vector Math.009": (-7752.8, 109.8),
            "Reroute.014": (1169.5, -920.7),
            "Reroute.015": (34.2, -196.0),
            "Reroute": (629.5, -740.7),
            "Reroute.016": (1329.5, -220.7),
            "Reroute.017": (1409.5, -500.7),
            "Reroute.018": (254.2, -176.0),
            "Group Input.027": (-7632.8, 209.8),
            "Transform Gizmo.002": (1289.5, -740.7),
            "Combine Transform.004": (929.5, -780.7),
            "Switch": (369.5, -680.7),
            "Compare": (89.5, -560.7),
            "Switch.004": (409.1, -136.1),
            "Index.003": (29.1, -336.1),
            "Compare.001": (209.1, -256.1),
            "Reroute.021": (669.1, -196.0),
            "Join Geometry.004": (-1417.4, -3029.7),
            "Instance on Points.002": (869.2, -56.0),
            "Set Instance Transform": (1049.2, -136.0),
            "Points.003": (669.2, -36.0),
            "Group Input.026": (489.2, -36.0),
            "Group Input.028": (669.2, -136.0),
            "Accumulate Field": (849.2, -236.0),
            "Group Input.029": (229.8, -420.1),
            "Combine Transform": (449.2, -376.0),
            "Transform Gizmo.003": (669.2, -516.0),
            "Object Info": (249.2, -796.0),
            "Group Input.002": (29.2, -796.0),
            "Switch.005": (449.2, -616.0),
            "Object Info.001": (249.2, -676.0),
            "Frame.010": (-4342.6, -2650.1),
            "Reroute.022": (54.2, -994.2),
            "Reroute.023": (1414.2, -994.2),
            "Reroute.024": (359.5, -845.7),
            "Reroute.025": (3801.7, -843.9),
            "Menu Switch.003": (449.8, -220.1),
            "Index Switch": (669.2, -296.0),
            "Index Switch.001": (849.2, -476.0),
            "Group Input.032": (249.2, -216.0),
            "Group Input.033": (249.2, -616.0),
            "Reroute.026": (629.2, -296.0),
            "Join Geometry.005": (2649.2, -516.0),
            "Group Input.034": (989.2, -696.0),
            "Linear Gizmo.002": (2489.2, -616.0),
            "Instance Transform": (1189.2, -776.0),
            "Sample Index": (1369.2, -736.0),
            "Integer Math.002": (1189.2, -836.0),
            "Separate Transform.001": (1549.2, -736.0),
            "Math.005": (2280.1, -634.8),
            "Vector Math.005": (2109.1, -772.3),
            "Separate Transform.002": (849.8, -360.1),
            "Transform Point": (1929.2, -776.0),
            "Combine Transform.001": (1749.2, -776.0),
            "Reroute.027": (2449.2, -756.0),
            "Object Info.003": (229.2, -436.1),
            "Object Info.004": (229.2, -316.1),
            "Group Input.036": (229.2, -256.1),
            "Group Input.035": (29.2, -436.1),
            "Switch.006": (429.2, -296.1),
            "Group Input.039": (1594.7, -625.7),
            "Group Input.040": (29.3, -236.1),
            "Group Input.041": (429.3, -576.1),
            "Realize Instances": (-8112.8, 109.8),
            "Math.006": (1595.7, -505.7),
            "Integer Math.003": (1415.7, -505.7),
            "Reroute.028": (1514.7, -445.7),
            "Reroute.029": (1375.7, -485.7),
            "Group Input.042": (29.5, -68.9),
            "Reroute.030": (2173.5, -446.9),
            "Math.007": (1775.7, -385.7),
            "Group Input.043": (-7859.4, -413.6),
            "Menu Switch.006": (-7679.4, -393.6),
            "Index Switch.002": (1995.7, -405.7),
            "Reroute.031": (50.3, -345.7),
            "Reroute.032": (1914.7, -345.7),
            "Switch.007": (469.3, -36.1),
            "Compare.002": (229.3, -36.1),
            "Linear Gizmo.003": (612.9, -576.7),
            "Frame.001": (-7494.7, -450.4),
            "Switch.008": (670.8, -135.6),
            "Reroute.033": (34.2, -116.8),
            "Merge by Distance": (470.8, -315.6),
            "Vector Math.015": (494.2, -136.0),
            "Index.004": (294.2, -216.0),
            "Group Input.045": (190.8, -195.6),
            "Spline Length": (60.0, -294.4),
            "Math.008": (280.0, -294.4),
            "Reroute.034": (220.0, -434.4),
            "Capture Attribute.001": (900.0, -214.4),
            "Group Input.037": (59.9, -74.8),
            "Instance on Points.004": (3284.6, -166.8),
            "Group Input.047": (3083.2, -276.4),
            "Switch.011": (3082.6, -344.0),
            "Sample Curve.002": (2107.0, -331.7),
            "Points.004": (1567.0, -151.7),
            "Accumulate Field.002": (1160.0, -134.4),
            "Sample Index.001": (1380.0, -134.4),
            "Resample Curve.003": (1160.0, -294.4),
            "Sample Index.002": (1427.0, -451.7),
            "Capture Attribute.003": (1747.0, -131.7),
            "Index.006": (1220.0, -554.4),
            "Sample Index.003": (1427.0, -511.7),
            "Spline Parameter": (1220.0, -494.4),
            "Math.014": (1927.0, -291.7),
            "Set Position.003": (2907.0, -171.7),
            "Capture Attribute.004": (2501.1, -154.4),
            "Index.007": (640.0, -454.4),
            "Switch.009": (4509.5, -287.3),
            "Instance on Points.005": (2610.1, -110.9),
            "Switch.012": (2379.9, -234.8),
            "Menu Switch.005": (-7352.8, -230.2),
            "Group Input.038": (-7552.8, -270.2),
            "Group Input.046": (40.0, -434.4),
            "Float to Integer": (460.0, -294.4),
            "Integer Math.004": (640.0, -294.4),
            "Frame.002": (-5908.9, -1069.3),
            "Frame.005": (1508.9, -35.9),
            "Reroute.035": (760.0, -214.4),
            "Frame.012": (989.1, -669.2),
            "Frame.013": (1078.2, -94.1),
            "Reroute.036": (249.5, -880.7),
            "Sample Curve.003": (1319.9, -294.8),
            "Points.005": (1514.3, -96.0),
            "Integer Math.005": (554.3, -136.0),
            "Domain Size": (354.3, -216.0),
            "Switch.010": (734.3, -36.0),
            "Group Input.051": (29.2, -36.1),
            "Reroute.037": (314.3, -316.0),
            "Integer Math.006": (779.9, -454.8),
            "Switch.013": (1520.6, -214.9),
            "Switch.014": (1520.6, -274.9),
            "Index.005": (29.5, -375.6),
            "Integer Math.008": (699.9, -374.8),
            "Integer Math.009": (859.9, -354.8),
            "Math.009": (1059.9, -414.8),
            "Integer Math.007": (229.5, -475.6),
            "Reroute.040": (435.5, -503.2),
            "Switch.015": (1520.6, -154.9),
            "Capture Attribute.002": (1719.2, -108.2),
            "Set Position.002": (2146.5, -36.7),
            "Reroute.039": (209.5, -435.6),
            "Reroute.041": (534.3, -316.0),
            "Sample Curve.004": (1319.9, -234.8),
            "Math.010": (985.0, -201.3),
            "Reroute.042": (1219.9, -274.8),
            "Is Spline Cyclic": (29.3, -142.4),
            "Boolean Math": (214.1, -115.8),
            "Sample Index.004": (559.9, -454.8),
            "Integer Math.010": (748.1, -200.3),
            "Reroute.044": (1319.9, -354.8),
            "Set ID": (1939.2, -52.9),
            "Hash Value.001": (1319.9, -494.8),
            "Switch.016": (1717.3, -342.4),
            "Hash Value.002": (1519.9, -394.8),
            "Index.008": (1319.9, -374.8),
            "Hash Value.003": (1519.9, -494.8),
            "Group Input.052": (1319.9, -434.8),
            "Reroute.046": (-5651.0, -962.8),
            "Reroute.047": (-1620.0, -960.0),
            "Reroute.048": (-6012.8, -270.2),
            "Reroute.049": (64.5, -58.3),
            "Switch.017": (1123.1, -36.2),
            "Float to Integer.001": (564.0, -172.5),
            "Switch.018": (812.9, -596.7),
            "Group Input.055": (425.7, -935.3),
            "Reroute.050": (-6832.8, -270.2),
            "Math.011": (396.8, -208.9),
            "Index Switch.003": (236.8, -168.9),
            "Math.012": (396.8, -248.9),
            "Math.013": (396.8, -288.9),
            "Sample Curve.005": (2107.0, -391.7),
            "Switch.019": (2319.7, -253.0),
            "Switch.020": (2318.2, -298.6),
            "Switch.021": (2317.9, -354.0),
            "Switch.022": (2107.0, -91.7),
            "Reroute.051": (2087.0, -131.7),
            "Index.009": (1567.0, -371.7),
            "Math.015": (1927.0, -431.7),
            "Math.016": (1747.0, -411.7),
            "Math.017": (590.2, -545.9),
            "Float to Integer.002": (770.2, -545.9),
            "Integer Math.011": (950.2, -545.9),
            "Curve Length": (420.4, -559.4),
            "Reroute.052": (2266.1, -186.8),
            "Set ID.001": (2721.1, -141.2),
            "Reroute.053": (2047.0, -371.7),
            "Reroute.054": (1387.0, -491.7),
            "Switch.023": (2510.9, -499.8),
            "Hash Value.004": (2287.0, -511.7),
            "Index.010": (2087.0, -491.7),
            "Group Input.058": (2087.0, -531.7),
            "Hash Value.005": (2287.0, -571.7),
            "Hash Value.006": (2087.0, -591.7),
            "Mix.003": (289.4, -175.8),
            "Mix.004": (729.4, -35.8),
            "Reroute.019": (469.4, -175.8),
            "Warning": (409.5, -68.9),
            "Compare.003": (243.8, -121.4),
            "Warning.001": (2904.4, -35.9),
            "Compare.004": (2718.5, -65.6),
            "Switch.025": (3087.3, -112.6),
            "Points.007": (2906.3, -265.8),
            "Group Input.059": (2537.5, -35.6),
            "Switch.024": (921.9, -89.3),
            "Realize Instances.002": (190.8, -275.6),
            "Switch.026": (870.8, -35.6),
            "Group Input.018": (630.8, -35.6),
            "Group Input.011": (2899.8, -341.5),
            "Group Input.062": (2179.9, -174.8),
            "Transform Geometry": (3237.1, -93.2),
            "Reroute.004": (1339.0, -344.4),
            "Switch.027": (1145.4, -222.1),
            "Domain Size.001": (626.3, -210.7),
            "Compare.005": (792.5, -182.9),
            "Warning.002": (961.4, -181.8),
            "Randomize Instance Transforms": (1109.1, -216.1),
            "Reroute.056": (1009.1, -116.1),
            "Compare.006": (409.1, -356.1),
            "Switch.028": (789.1, -176.1),
            "Boolean Math.001": (609.1, -256.1),
            "Group Input.070": (189.1, -156.1),
            "Domain Size.002": (49.1, -456.1),
            "Integer Math.012": (229.1, -436.1),
            "Reroute.013": (967.2, -210.2),
            "Random Value": (29.4, -175.8),
            "Store Named Attribute": (449.4, -55.8),
            "Group Input.071": (-492.8, -570.2),
            "Hash Value": (-292.8, -550.2),
            "Capture Attribute": (257.5, -76.2),
            "Index.011": (29.0, -482.2),
            "Store Named Attribute.001": (649.4, -55.8),
            "Integer Math.013": (736.8, -148.9),
            "Reroute.020": (629.5, -348.9),
            "Dial Gizmo.001": (620.0, -895.3),
            "Join Geometry.006": (-1130.2, -1395.0),
            "Group Input.072": (249.5, -35.6),
            "Linear Gizmo.004": (429.5, -35.6),
            "Reroute.043": (-1438.2, -2505.4),
            "Sample Curve": (249.5, -135.6),
            "Group Input.073": (29.5, -395.6),
            "Switch.029": (-4085.5, -2468.0),
            "Reroute.055": (-5106.2, -2493.9),
            "Linear Gizmo.005": (429.5, -235.6),
            "Sample Curve.001": (269.5, -375.6),
            "Reroute.059": (51.3, -189.0),
            "Frame.003": (-5010.7, -2538.4),
            "Reroute.060": (1066.4, -59.7),
            "Reroute.057": (1169.5, -960.7),
            "Reroute.061": (369.1, -196.0),
            "Group Input.019": (294.2, -36.0),
            "Reroute.063": (614.2, -634.2),
            "Reroute.064": (229.4, -135.8),
            "Frame": (-7244.5, 1023.6),
            "Frame.004": (2956.4, -74.6),
            "Frame.008": (-57.4, -71.1),
            "Reroute.065": (410.8, -315.6),
            "Group Input.020": (29.4, -95.8),
            "Frame.009": (116.2, -643.0),
            "Frame.011": (202.4, -35.9),
            "Frame.014": (193.7, -377.6),
            "Reroute.066": (1779.5, -451.1),
            "Reroute.038": (959.9, -434.8),
            "Reroute.045": (579.9, -434.8),
            "Reroute.067": (759.9, -334.8),
            "Combine XYZ": (3156.3, -375.7),
            "Index Switch.012": (3356.3, -475.7),
            "Combine XYZ.001": (3156.3, -475.7),
            "Combine XYZ.005": (3156.3, -575.7),
            "Index Switch.013": (3719.2, -338.7),
            "Math.018": (2956.3, -475.7),
            "Reroute.006": (3176.4, -829.7),
            "Reroute.062": (2895.5, -430.8),
            "Rotate Rotation.001": (3536.3, -435.7),
            "Group Input.007": (3356.3, -535.7),
            "Axes to Rotation.005": (1999.9, -274.8),
            "Rotate Rotation.002": (2179.9, -314.8),
            "Group Input.008": (1999.9, -454.8),
            "Axes to Rotation.006": (2719.8, -381.5),
            "Rotate Rotation.003": (2899.8, -441.5),
            "Group Input.012": (2719.8, -561.5),
            "Domain Size.003": (29.2, -116.1),
            "Compare.007": (189.2, -96.1),
            "Switch.030": (369.2, -76.1),
            "Reroute.068": (2706.2, -652.3),
            "Reroute.069": (1508.9, -650.7),
            "Reroute.070": (59.9, -54.8),
            "Frame.015": (759.7, -394.6),
        }


ASSET = Array

ASSET_METADATA = {
    "description": "Create copies of the geometry with different methods of cumulative offset",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "007a2c8d-f113-421b-a39c-8fbc76c4f7fe",
    "catalog_simple_name": "Generate",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
