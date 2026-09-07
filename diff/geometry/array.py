# Node-group asset 'Array' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup

from .randomize_transforms import RandomizeTransforms


class Array(CustomGeometryGroup):
    _name = "Array"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
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
            menu_switch = g.MenuSwitch.integer(
                transform_reference, {"Inputs": 0, "Object": 1}
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
            index_switch = g.IndexSwitch.matrix(
                menu_switch, (combine_transform, switch)
            )
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
            linear_gizmo = g.LinearGizmo(
                value=(
                    count
                    * index_switch.o.output.translation.transform(
                        combine_transform_1
                    ).length(),
                ),
                position=sample_index.o.value.translation,
                direction=sample_index.o.value.translation,
                draw_style="CROSS",
            )
            join_geometry = g.JoinGeometry(
                geometry=(
                    g.IndexSwitch.geometry(menu_switch, (transform_gizmo, None)),
                    linear_gizmo,
                )
            )
        menu_switch_1 = g.MenuSwitch.integer(
            offset_method, {"Relative": 0, "Offset": 1, "Endpoint": 2}
        )
        menu_switch_2 = g.MenuSwitch.integer(circle_segment, {"Full": 0, "Arc": 1})
        menu_switch_3 = g.MenuSwitch.integer(count_method, {"Count": 0, "Distance": 1})
        with g.Frame("Curve Instances"):
            switch_1 = relative_space.switch.geometry(
                g.ObjectInfo(object=curve_object).o.geometry,
                g.ObjectInfo(
                    object=curve_object, transform_space="RELATIVE"
                ).o.geometry,
            )
            with g.Frame("Single Curve Fallback"):
                compare = g.Compare.integer.equal(
                    g.DomainSize(geometry=switch_1, component="CURVE").o.spline_count, 1
                )
                switch_2 = compare.o.result.switch.boolean(per_curve, True)
            compare_1 = g.Compare.integer.equal(
                g.DomainSize(geometry=switch_1, component="CURVE").o.spline_count, 0
            )
            switch_3 = g.Warning(
                show=compare_1, message="No Curve Selected"
            ).o.show.switch.geometry(switch_1)
            with g.Frame("Distance Method"):
                index = g.Index()
                boolean_math = ~g.IsSplineCyclic().o.cyclic
                integer_math = (
                    g.FloatToInteger(
                        float=g.SplineLength().o.length / distance,
                        rounding_mode="FLOOR",
                    ).o.integer
                    + 1
                )
                capture = g.CaptureAttribute.curve(geometry=switch_3)
                value = capture.items.integer("Value", integer_math)
                index_1 = capture.items.integer("Index", g.Index())
                curve_length = g.CurveLength(curve=switch_3)
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
                sample_index_2 = g.SampleIndex(
                    geometry=resample_curve,
                    value=index_1.output,
                    index=index,
                    data_type="INT",
                )
                sample_index_3 = g.SampleIndex(
                    geometry=resample_curve,
                    value=g.SplineParameter().o.index,
                    index=index,
                    data_type="INT",
                )
                points = g.Points(count=sample_index_1, radius=0.1)
                integer_math_1 = (
                    g.FloatToInteger(
                        float=curve_length.o.length / distance, rounding_mode="FLOOR"
                    ).o.integer
                    + 1
                )
                capture_1 = g.CaptureAttribute.point(geometry=points)
                curve_index = capture_1.items.integer("Curve Index", sample_index_2)
                index_in_curve = capture_1.items.integer(
                    "Index in Curve", sample_index_3
                )
                sample_curve = g.SampleCurve(
                    curves=switch_3,
                    length=index_in_curve.output * distance,
                    curve_index=curve_index.output,
                    mode="LENGTH",
                )
                hash_value = g.HashValue(
                    value=g.HashValue(
                        value=curve_index.output, seed=index_in_curve.output
                    ),
                    seed=seed,
                )
                sample_curve_1 = g.SampleCurve(
                    curves=switch_3,
                    length=g.Math.divide(g.Index(), integer_math_1).o.value
                    * curve_length,
                    mode="LENGTH",
                    use_all_curves=True,
                )
                capture_2 = g.CaptureAttribute.point(
                    geometry=switch_2.switch.geometry(points, capture_1.o.geometry)
                )
                position = capture_2.items.vector(
                    "Position",
                    switch_2.switch.vector(
                        sample_curve_1.o.position, sample_curve.o.position
                    ),
                )
                tangent = capture_2.items.vector(
                    "Tangent",
                    switch_2.switch.vector(
                        sample_curve_1.o.tangent, sample_curve.o.tangent
                    ),
                )
                normal = capture_2.items.vector(
                    "Normal",
                    switch_2.switch.vector(
                        sample_curve_1.o.normal, sample_curve.o.normal
                    ),
                )
                axes_to_rotation = g.AxesToRotation(
                    primary_axis=tangent.output,
                    secondary_axis=normal.output,
                    primary="X",
                    secondary="Z",
                )
                set_position = (
                    capture_2.o.geometry
                    >> g.SetID(
                        id=switch_2.switch.integer(
                            g.HashValue(value=g.Index(), seed=seed), hash_value
                        )
                    )
                    >> g.SetPosition(position=position.output)
                )
                switch_4 = align_rotation.switch.rotation(
                    (0.0, 0.0, 0.0),
                    axes_to_rotation.o.rotation.rotate(
                        local_rotation, rotation_space="LOCAL"
                    ),
                )
                instance_on_points = g.Warning(
                    show=g.Compare.float.equal(distance, 0.0, 0.0),
                    message="Invalid Distance",
                ).o.show.switch.geometry(
                    set_position, g.Points(radius=0.1)
                ) >> g.InstanceOnPoints(instance=geometry, rotation=switch_4)
            with g.Frame("Count Method"):
                index_2 = g.Index()
                integer_math_2 = index_2.o.index / count
                integer_math_3 = index_2.o.index - integer_math_2 * count
                switch_5 = switch_2.switch.integer(
                    g.HashValue(value=g.Index(), seed=seed),
                    g.HashValue(
                        value=g.HashValue(value=integer_math_2, seed=integer_math_3),
                        seed=seed,
                    ),
                )
                sample_curve_2 = g.SampleCurve(
                    curves=switch_3,
                    factor=g.Math.divide(index_2, count - 1),
                    use_all_curves=True,
                )
                sample_index_4 = g.SampleIndex(
                    geometry=switch_3,
                    value=boolean_math,
                    index=integer_math_2,
                    data_type="INT",
                    domain="CURVE",
                )
                switch_6 = switch_2.switch.integer(
                    count,
                    count
                    * g.DomainSize(geometry=switch_3, component="CURVE").o.spline_count,
                )
                sample_curve_3 = g.SampleCurve(
                    curves=switch_3,
                    factor=g.Math.divide(integer_math_3, count - sample_index_4),
                    curve_index=integer_math_2,
                )
                capture_3 = g.CaptureAttribute.point(
                    geometry=g.Points(count=switch_6, radius=0.1)
                )
                position_1 = capture_3.items.vector(
                    "Position",
                    switch_2.switch.vector(
                        sample_curve_2.o.position, sample_curve_3.o.position
                    ),
                )
                tangent_1 = capture_3.items.vector(
                    "Tangent",
                    switch_2.switch.vector(
                        sample_curve_2.o.tangent, sample_curve_3.o.tangent
                    ),
                )
                normal_1 = capture_3.items.vector(
                    "Normal",
                    switch_2.switch.vector(
                        sample_curve_2.o.normal, sample_curve_3.o.normal
                    ),
                )
                axes_to_rotation_1 = g.AxesToRotation(
                    primary_axis=tangent_1.output,
                    secondary_axis=normal_1.output,
                    primary="X",
                    secondary="Z",
                )
                switch_7 = align_rotation.switch.rotation(
                    (0.0, 0.0, 0.0),
                    axes_to_rotation_1.o.rotation.rotate(
                        local_rotation, rotation_space="LOCAL"
                    ),
                )
                instance_on_points_1 = (
                    capture_3.o.geometry
                    >> g.SetID(id=switch_5)
                    >> g.SetPosition(position=position_1.output)
                    >> g.InstanceOnPoints(instance=geometry, rotation=switch_7)
                )
            switch_8 = g.Switch.geometry(
                menu_switch_3.o.output, instance_on_points_1, instance_on_points
            )
        with g.Frame("Circle Gizmos"):
            linear_gizmo_1 = g.LinearGizmo(
                value=(radius,),
                position=g.VectorMath.scale((0.0, 1.0, 0.0), radius),
                direction=(0.0, 1.0, 0.0),
                draw_style="BOX",
            )
            switch_9 = g.Switch.geometry(
                menu_switch_3.o.output,
                g.LinearGizmo(
                    value=(count,), direction=(0.0, 1.0, 0.0), draw_style="CROSS"
                ),
                g.DialGizmo(value=(angular_distance,), radius=0.8),
            )
            switch_10 = g.Compare.integer.equal(
                menu_switch_2, 1
            ).o.result.switch.geometry(
                true=g.DialGizmo(value=(sweep_angle,), color_id="SECONDARY")
            )
            join_geometry_1 = g.JoinGeometry(
                geometry=(switch_10, linear_gizmo_1, switch_9)
            )
        with g.Frame("Circle Instances"):
            index_3 = g.Index()
            menu_switch_4 = g.MenuSwitch.integer(central_axis, {"X": 0, "Y": 1, "Z": 2})
            index_switch_1 = g.IndexSwitch.rotation(
                menu_switch_4,
                ((1.5707964, 0.0, 1.5707964), (1.5707964, 0.0, 0.0), (0.0, 0.0, 0.0)),
            )
            warning = g.Warning(
                show=g.Compare.float.equal(angular_distance, 0.0, 0.0),
                message="Invalid Distance",
            )
            math = abs(
                g.IndexSwitch.float(menu_switch_2, (6.2831855, sweep_angle)).o.output
                / angular_distance
            )
            transform_geometry = g.TransformGeometry(
                geometry=join_geometry_1, transform=index_switch_1, mode="Matrix"
            )
            switch_11 = warning.o.show.switch.integer(
                g.FloatToInteger(float=math.max(1.0), rounding_mode="FLOOR").o.integer
                + menu_switch_2,
                1,
            )
            switch_12 = g.Switch.integer(menu_switch_3.o.output, count, switch_11)
            index_switch_2 = g.IndexSwitch.float(
                menu_switch_2,
                (
                    g.Math.divide(index_3, switch_12).o.value * 6.2831855,
                    g.Math.divide(index_3, switch_12.o.output - 1).o.value
                    * sweep_angle,
                ),
            )
            index_switch_3 = g.IndexSwitch.vector(
                menu_switch_4,
                (
                    g.CombineXYZ(x=index_switch_2),
                    g.CombineXYZ(y=index_switch_2.o.output * -1.0),
                    g.CombineXYZ(z=index_switch_2),
                ),
            )
            rotate_rotation = g.RotateRotation(
                rotation=index_switch_3,
                rotate_by=local_rotation,
                rotation_space="LOCAL",
            )
            switch_13 = align_rotation.switch.rotation(
                (0.0, 0.0, 0.0),
                g.IndexSwitch.rotation(items=(rotate_rotation, (1.5707964, 0.0, 0.0))),
            )
            instance_on_points_2 = (
                g.Points(count=switch_12, radius=0.1)
                >> g.SetPosition(
                    position=g.CombineXYZ(y=radius).o.vector.rotate(
                        g.CombineXYZ(z=index_switch_2)
                    )
                )
                >> g.TransformGeometry(transform=index_switch_1, mode="Matrix")
                >> g.InstanceOnPoints(instance=geometry, rotation=switch_13)
            )
        hash_value_1 = g.HashValue(value=seed, seed=1000)
        bounding_box = (
            geometry
            >> g.RealizeInstances(realize_to_point_domain=True)
            >> g.BoundingBox()
        )
        with g.Frame("Curve Gizmos"):
            sample_curve_4 = g.SampleCurve(curves=switch_1)
            sample_curve_5 = g.SampleCurve(
                curves=switch_1, length=distance, mode="LENGTH"
            )
            linear_gizmo_2 = g.LinearGizmo(
                value=(count,),
                position=sample_curve_4.o.position,
                direction=sample_curve_4.o.tangent,
                draw_style="CROSS",
            )
            linear_gizmo_3 = g.LinearGizmo(
                value=(distance,),
                position=sample_curve_5.o.position,
                direction=sample_curve_5.o.tangent,
                draw_style="CROSS",
            )
        vector_math = offset * (bounding_box.o.max - bounding_box.o.min)
        with g.Frame("Line Gismoz"):
            integer_math_4 = count - 1
            math_1 = 1.0 / integer_math_4
            compare_2 = g.Compare.integer.not_equal(menu_switch_1, 0)
            switch_14 = compare_2.o.result.switch.vector(vector_math, translation)
            vector_math_1 = switch_14 * integer_math_4
            transform_gizmo_1 = g.TransformGizmo(
                value=(
                    g.CombineTransform(
                        translation=translation, rotation=rotation, scale=scale
                    ),
                ),
                position=switch_14,
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
            transform_gizmo_2 = g.TransformGizmo(
                value=(
                    g.CombineTransform(
                        translation=vector_math, rotation=rotation, scale=scale
                    ),
                ),
                position=switch_14,
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
            switch_15 = compare_2.o.result.switch.geometry(
                transform_gizmo_2, transform_gizmo_1
            )
            vector_math_2 = g.IndexSwitch.vector(
                menu_switch_1, (switch_14, switch_14, switch_14 * math_1)
            ).o.output.length()
            linear_gizmo_4 = g.LinearGizmo(
                value=(count * vector_math_2,),
                position=g.IndexSwitch.vector(
                    menu_switch_1, (vector_math_1, vector_math_1, switch_14)
                ),
                direction=switch_14,
                draw_style="CROSS",
            )
        with g.Frame("Line Instances"):
            with g.Frame("Rotation"):
                index_switch_4 = g.IndexSwitch.rotation(
                    menu_switch_1,
                    (
                        rotation,
                        rotation,
                        math_1.mix.rotation((0.0, 0.0, 0.0), rotation),
                    ),
                )
                mix = g.Mix.rotation(g.Index(), b_rotation=index_switch_4)
            with g.Frame("Scale"):
                integer_math_5 = count - 1
                mix_1 = g.Mix.vector(integer_math_5, (1.0, 1.0, 1.0), scale)
                index_switch_5 = g.IndexSwitch.vector(
                    menu_switch_1, (mix_1.o.result_vector, mix_1.o.result_vector, scale)
                )
                mix_2 = g.Math.divide(g.Index(), integer_math_5).o.value.mix.vector(
                    (1.0, 1.0, 1.0), index_switch_5
                )
            with g.Frame("Position"):
                vector_math_3 = (
                    g.IndexSwitch.vector(
                        menu_switch_1, (switch_14, switch_14, switch_14 * math_1)
                    ).o.output
                    * g.Index()
                )
                set_position_1 = g.Points(count=count, radius=0.1) >> g.SetPosition(
                    position=vector_math_3
                )
            instance_on_points_3 = set_position_1 >> g.InstanceOnPoints(
                instance=geometry, rotation=mix.o.result_rotation, scale=mix_2
            )
        join_geometry_2 = g.JoinGeometry(
            geometry=(
                instance_on_points_3,
                g.JoinGeometry(geometry=(linear_gizmo_4, switch_15)),
            )
        )
        join_geometry_3 = g.JoinGeometry(
            geometry=(
                switch_8,
                g.Switch.geometry(
                    menu_switch_3.o.output, linear_gizmo_2, linear_gizmo_3
                ),
            )
        )
        index_switch_6 = g.IndexSwitch.geometry(
            g.MenuSwitch.integer(
                shape, {"Line": 0, "Circle": 1, "Curve": 2, "Transform": 3}
            ),
            (
                join_geometry_2,
                g.JoinGeometry(geometry=(instance_on_points_2, transform_geometry)),
                join_geometry_3,
                g.JoinGeometry(geometry=(set_instance_transform, join_geometry)),
            ),
        )
        with g.Frame("Store Info"):
            capture_4 = g.CaptureAttribute.instance(geometry=index_switch_6)
            random = capture_4.items.vector(
                "random",
                g.RandomValue.vector(
                    (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), seed=hash_value_1
                ),
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
        with g.Frame("Randomization"):
            index_4 = g.Index()
            switch_16 = exclude_first.switch.boolean(
                True, g.Compare.integer.not_equal(index_4, 0)
            )
            compare_3 = g.Compare.integer.not_equal(
                index_4,
                g.DomainSize(
                    geometry=store_named_attribute, component="INSTANCES"
                ).o.instance_count
                - 1,
            )
            group = RandomizeTransforms(
                Instances=store_named_attribute,
                Selection=exclude_last.switch.boolean(switch_16, switch_16 & compare_3),
                Offset=randomize_offset,
                Rotation=randomize_rotation,
                **{"Scale Axes": randomize_scale_axes},
                Flipping=randomize_flipping,
                Seed=seed,
                _named_links=[("Scale", randomize_scale), ("Scale", randomize_scale_1)],
            )
            switch_17 = randomize.switch.geometry(store_named_attribute, group)
        with g.Frame("Merge Instances"):
            realize_instances_1 = g.RealizeInstances(
                geometry=switch_17, realize_to_point_domain=True
            )
            switch_18 = merge.switch.geometry(
                realize_instances_1,
                g.MergeByDistance(
                    geometry=realize_instances_1, distance=merge_distance
                ),
            )
            realize_instances.switch.geometry(switch_17, switch_18) >> geometry_1

        shape.default_value = "Line"
        count_method.default_value = "Count"
        offset_method.default_value = "Relative"
        transform_reference.default_value = "Inputs"
        central_axis.default_value = "Z"
        circle_segment.default_value = "Full"
        randomize_scale_axes.default_value = "Uniform"


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
