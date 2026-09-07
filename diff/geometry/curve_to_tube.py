# Node-group asset 'Curve to Tube' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class Curve_UV_factor_propagate(CustomGeometryGroup):
    _name = ".curve_UV_factor_propagate"

    def _build_group(self, tree):
        input = tree.inputs.float("Input", 0.0)
        output = tree.outputs.float("Output")

        boolean_math = (input.corner.at(g.OffsetCornerInFace(offset=-1)) > 0.5) | (
            input.corner.at(g.OffsetCornerInFace(offset=1)) > 0.5
        )
        (
            (
                g.Compare.float.equal(input, 0.0, 0.0).o.result & boolean_math
            ).switch.float(input, 1.0)
            >> output
        )


class Curve_UV(CustomGeometryGroup):
    _name = ".curve_UV"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        menu = tree.inputs.menu("Menu", optional_label=True)
        factor = tree.outputs.float(
            "Factor",
            description="For points, the portion of the spline's total length at the control point. For Splines, the factor of that spline within the entire curve",
        )
        length = tree.outputs.boolean("Length")

        spline_parameter = g.SplineParameter()
        math = g.Math.divide(
            spline_parameter.o.index,
            g.SplineLength().o.point_count - ~g.IsSplineCyclic().o.cyclic,
        )
        menu_switch = g.MenuSwitch.float(
            menu,
            {
                "Factor": (
                    spline_parameter,
                    "Use the portion of the curve's total length",
                ),
                "Length": (
                    spline_parameter,
                    "Use the curve length at each point as the UV map coordinate directly",
                ),
                "Index": (
                    math,
                    "Use the portion of the total evaluated points along the curve as the UV coordinate",
                ),
            },
        )

        menu_switch >> factor
        menu_switch.o.length >> length

        menu.default_value = "Factor"


class UV_sphere_corrected(CustomGeometryGroup):
    _name = ".UV_sphere_corrected"

    def _build_group(self, tree):
        segments = tree.inputs.integer(
            "Segments",
            32,
            description="Horizontal resolution of the sphere",
            min_value=3,
            max_value=1024,
        )
        rings = tree.inputs.integer(
            "Rings",
            16,
            description="The number of horizontal rings",
            min_value=2,
            max_value=1024,
        )
        mesh = tree.outputs.geometry("Mesh")
        uv_map = tree.outputs.vector("UV Map", dimensions=2)
        equator = tree.outputs.boolean("Equator")

        uv_sphere = g.UVSphere(segments=segments, rings=rings)
        math = 1.0 / segments
        capture = g.CaptureAttribute.point(geometry=uv_sphere)
        result = capture.items.boolean(
            "Result",
            g.Compare.float.equal(abs(g.Position().o.position.z), 0.0, 0.00001),
        )
        switch = (
            ((g.Index().o.index + 1).modulo(segments) <= 0)
            .face.evaluate()
            .switch.float(math, -1.0 + math)
        )
        combine_xyz = g.CombineXYZ(
            x=uv_sphere.o.uv_map.x + switch, y=uv_sphere.o.uv_map.y
        )

        capture.o.geometry >> mesh
        combine_xyz >> uv_map
        result.output >> equator


class Half_spheres(CustomGeometryGroup):
    _name = ".half_spheres"

    def _build_group(self, tree):
        resolution = tree.inputs.integer("Resolution", 8, min_value=3, max_value=10000)
        shade_smooth = tree.inputs.boolean("Shade Smooth", False)
        uv_map = tree.inputs.boolean("UV Map", False)
        uv_name = tree.inputs.string("UV Name", "")
        align_normals = tree.inputs.boolean("Align Normals", False)
        top = tree.outputs.geometry("Top")
        bottom = tree.outputs.geometry("Bottom")
        boolean = tree.outputs.boolean("Boolean")

        boolean_math = ~shade_smooth
        group = UV_sphere_corrected(
            **{
                "Segments": resolution,
                "Rings": g.IntegerMath.divide_round(resolution, 2).o.value * 2,
            }
        )
        capture = g.CaptureAttribute.face(geometry=group >> g.TransformGeometry())
        top_1 = capture.items.boolean("Top", g.Position().o.position.z > 0.0)
        capture_1 = g.CaptureAttribute.point(geometry=capture.o.geometry)
        normal = capture_1.items.vector("Normal", g.Normal().o.normal)
        set_mesh_normal = capture_1.o.geometry >> g.SetMeshNormal(
            edge_sharpness=boolean_math, face_sharpness=boolean_math
        )
        rotate_vector = (
            group.o.uv_map
            + top_1.output.switch.vector((-1.0, -0.5, 0.0), (-1.0, -1.5, 0.0))
        ).rotate((0.0, 3.1415927, 1.5707964))
        switch = align_normals.switch.geometry(
            set_mesh_normal, g.SetMeshNormal.free(set_mesh_normal, normal.output)
        )
        separate_geometry = uv_map.switch.geometry(
            switch,
            g.StoreNamedAttribute.corner.vector_2d(
                switch, name=uv_name, value=rotate_vector
            ),
        ) >> g.SeparateGeometry.face(selection=top_1.output)

        separate_geometry >> top
        separate_geometry.o.inverted >> bottom
        group.o.equator >> boolean


class CurveToTube(CustomGeometryGroup):
    _name = "Curve to Tube"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        curve = tree.inputs.geometry(
            "Curve", description="Curve geometry defining the curve path"
        )
        scale = tree.inputs.float(
            "Scale",
            0.1,
            description="Distance factor multiplied with the curve's radius attribute to define the resulting tube radius",
            min_value=0.0,
            subtype="DISTANCE",
        )
        with tree.inputs.panel("Profile"):
            profile_mode = tree.inputs.menu(
                "Profile Mode",
                description="Method used to define the profile shape",
                expanded=True,
                optional_label=True,
                structure_type="SINGLE",
            )
            profile_input = tree.inputs.menu(
                "Profile Input",
                description="How the profile geometry input should be exposed",
                expanded=True,
                optional_label=True,
                hide_in_modifier=True,
            )
            profile_object = tree.inputs.object(
                "Profile Object",
                description="Shape defining a section of the tube, using the XY plane",
            )
            profile_geometry = tree.inputs.geometry(
                "Profile Geometry",
                description="Shape defining a section of the tube, using the XY plane",
            )
            profile_resolution = tree.inputs.integer(
                "Profile Resolution",
                8,
                description="Number of points on the profile circle. Also defines the round cap resolution.",
                min_value=3,
                max_value=512,
            )
            shade_smooth = tree.inputs.boolean(
                "Shade Smooth",
                True,
                description="Use smooth vertex normals instead of face normals for the result mesh",
            )
        miter_scale = tree.inputs.boolean(
            "Miter Scale",
            True,
            description="Scale the profile along the axis of the corner's turn to maintain a constant visual width",
            is_panel_toggle=True,
        )
        miter_scale_limit = tree.inputs.float(
            "Miter Scale Limit",
            2.3561945,
            description="Angle at which the miter scale stops increasing",
            min_value=0.0,
            max_value=3.1415927,
            subtype="ANGLE",
        )
        with tree.inputs.panel("Resample", default_closed=True):
            resample = tree.inputs.boolean(
                "Resample",
                True,
                description="Resample the input curve before meshing",
                is_panel_toggle=True,
            )
            resample_mode = tree.inputs.menu(
                "Resample Mode",
                description="How to specify the number of samples",
                optional_label=True,
            )
            resample_count = tree.inputs.integer(
                "Resample Count",
                10,
                description="Number of sample points on the curve",
                min_value=2,
                max_value=100000,
            )
            resample_length = tree.inputs.float(
                "Resample Length",
                0.1,
                description="Distance between two sample points along the curve",
                min_value=0.01,
                subtype="DISTANCE",
            )
            resample_scale = tree.inputs.float(
                "Resample Scale",
                1.0,
                description="Scale factor applied on the automatically derived resample length",
                min_value=0.1,
                max_value=10000.0,
                structure_type="FIELD",
            )
        with tree.inputs.panel("Caps", default_closed=True):
            caps = tree.inputs.boolean(
                "Caps",
                True,
                description="Fill the holes at the tube ends with cap geometry",
                is_panel_toggle=True,
            )
            caps_type = tree.inputs.menu(
                "Caps Type",
                description="Method used to build the start and end geometry",
                optional_label=True,
            )
            caps_input = tree.inputs.menu(
                "Caps Input",
                description="How the cap geometry input should be exposed",
                expanded=True,
                optional_label=True,
                hide_in_modifier=True,
            )
            caps_start = tree.inputs.object(
                "Caps Start", description="Geometry to add to the start of each curve"
            )
            caps_end = tree.inputs.object(
                "Caps End", description="Geometry to add to the end of each curve"
            )
            caps_start_1 = tree.inputs.geometry(
                "Caps Start", description="Geometry to add to the start of each curve"
            )
            caps_end_1 = tree.inputs.geometry(
                "Caps End", description="Geometry to add to the end of each curve"
            )
            caps_resolution = tree.inputs.integer(
                "Caps Resolution",
                12,
                description="Amount of edge loops the round caps are generated with",
                min_value=1,
                max_value=256,
            )
            caps_smooth = tree.inputs.boolean(
                "Caps Smooth",
                False,
                description="Make border edges between the caps and the tube shape smooth instead of sharp",
                structure_type="SINGLE",
            )
            caps_merge = tree.inputs.boolean(
                "Caps Merge",
                True,
                description="Combine the cap geometry with the base mesh (realizing instances and merging vertices)",
                structure_type="SINGLE",
            )
            caps_align_normals = tree.inputs.boolean(
                "Caps Align Normals",
                False,
                description="Build custom normals on the caps for more continuous shading borders with the tube shape",
                structure_type="SINGLE",
            )
            caps_extrapolate_radius = tree.inputs.boolean(
                "Caps Extrapolate Radius",
                True,
                description="Adjust the shape of the cap to follow the change in radius towards the curve ends",
                structure_type="SINGLE",
            )
        with tree.inputs.panel("UV Map", default_closed=True):
            uv_map = tree.inputs.boolean(
                "UV Map",
                True,
                description="Generate UV attribute data on the curve geometry",
                is_panel_toggle=True,
            )
            uv_map_name = tree.inputs.string(
                "UV Map Name",
                "UVMap",
                description="Name of the UV map attribute to generate",
            )
            uv_map_parameter_u = tree.inputs.menu(
                "UV Map Parameter U",
                description="Method to generate the map's X coordinate along the main curve",
            )
            uv_map_parameter_v = tree.inputs.menu(
                "UV Map Parameter V",
                description="Method to generate the map's Y coordinate along the profile curve",
            )
            consider_curve_radius = tree.inputs.boolean(
                "Consider Curve Radius",
                True,
                description="Consider the main curve's radius attribute as a factor when mapping the V component by the profile curve's length parameter",
                structure_type="SINGLE",
            )
        mesh = tree.outputs.geometry("Mesh", description="Tube mesh")

        with g.Frame("Flip curve based on winding direction"):
            curve_tangent = g.CurveTangent()
            vector_math = curve_tangent.o.tangent.point.at(
                g.OffsetPointInCurve(offset=-1).o.point_index
            ).cross(curve_tangent)
            compare = (
                vector_math.z.point.total(g.Index().o.index.spline.evaluate()) <= 0.0
            )
        with g.Frame("segment length"):
            offset_point_in_curve = g.OffsetPointInCurve(offset=-1)
            position = g.Position()
            switch = offset_point_in_curve.o.is_valid_offset.switch.integer(
                g.Index(), offset_point_in_curve.o.point_index
            )
            vector_math_1 = (
                (position.o.position - position.o.position.point.at(switch))
                .point.evaluate()
                .length()
            )
        with g.Frame("Segment Length"):
            offset_point_in_curve_1 = g.OffsetPointInCurve(offset=-1)
            position_1 = g.Position()
            switch_1 = offset_point_in_curve_1.o.is_valid_offset.switch.integer(
                g.Index(), offset_point_in_curve_1.o.point_index
            )
            vector_math_2 = (
                (position_1.o.position - position_1.o.position.point.at(switch_1))
                .point.evaluate()
                .length()
            )
        with g.Frame("Averaged radius estimation"):
            field_average = (
                g.NamedAttribute(name="radius").o.exists.switch.float(1.0, g.Radius())
                * scale
            ).point.mean(g.Index().o.index.spline.evaluate())
        menu_switch = g.MenuSwitch.integer(
            caps_type,
            {
                "Flat": (1, "Use a single Ngon for the caps"),
                "Round": (2, "Use a half-circle for each cap"),
                "Custom": (3, "Use custom objects to define the cap shapes"),
            },
        )
        with g.Frame("Estimate round segment length"):
            math = field_average * 2.0 * (3.1415927 / profile_resolution).sin()
        menu_switch_1 = g.MenuSwitch.integer(
            resample_mode, {"Evaluated": 0, "Auto": 1, "Count": 2, "Length": 3}
        )
        switch_2 = caps.switch.boolean(true=menu_switch.o.flat)
        switch_3 = caps.switch.boolean(true=menu_switch.o.round)
        switch_4 = caps.switch.boolean(true=menu_switch.o.custom)
        resample_curve = g.MenuSwitch.geometry(
            profile_input,
            {
                "Object": g.ObjectInfo(object=profile_object).o.geometry,
                "Geometry": profile_geometry,
            },
        ) >> g.ResampleCurve(mode="Evaluated", length=0.1, keep_last_segment=True)
        capture = g.CaptureAttribute.curve(geometry=resample_curve)
        flip = capture.items.boolean("Flip", compare)
        flip_and_cyclic = capture.items.boolean(
            "Flip and Cyclic", compare & g.IsSplineCyclic()
        )
        reverse_curve = capture.o.geometry >> g.ReverseCurve(selection=flip.output)
        with g.Frame("Pre-Processing"):
            spline_parameter = g.SplineParameter()
            switch_5 = flip_and_cyclic.output.switch.float(
                spline_parameter,
                spline_parameter.o.factor.point.at(
                    g.OffsetPointInCurve(offset=1).o.point_index
                ),
            )
            capture_1 = g.CaptureAttribute.point(
                geometry=reverse_curve >> g.SetCurveNormal(mode="Free")
            )
            factor = capture_1.items.float("Factor", switch_5)
            capture_2 = g.CaptureAttribute.curve(geometry=capture_1.o.geometry)
            spline_position = capture_2.items.vector("Spline Position", g.Position())
            spline_length = capture_2.items.float(
                "Spline Length", g.SplineLength().o.length
            )
        with g.Frame("Round Caps Custom Profile"):
            boolean_math = ~shade_smooth
            resample_curve_1 = g.ResampleCurve(
                curve=g.CurveLine(end=(1.0, 0.0, 0.0)),
                count=caps_resolution + 1,
                length=0.1,
                keep_last_segment=True,
            )
            capture_3 = g.CaptureAttribute.point(geometry=resample_curve_1)
            factor_1 = capture_3.items.float("Factor", g.SplineParameter().o.factor)
            with g.Frame("redistribute circular"):
                math_1 = (factor_1.output * 1.5707964).sin()
            with g.Frame("circular profile"):
                math_2 = (1.0 - math_1**2.0).sqrt()
            math_3 = 1.0 - math_1
            vector_math_3 = g.Position().o.position - spline_position.output
            math_4 = spline_length.output / 6.2831855
            curve_to_mesh = g.CurveToMesh(
                curve=capture_2.o.geometry,
                profile_curve=g.ReverseCurve(curve=capture_3.o.geometry),
                scale=math_4,
            )
            curve_to_mesh_1 = g.CurveToMesh(
                curve=capture_2.o.geometry,
                profile_curve=g.TransformGeometry(
                    geometry=capture_3.o.geometry, rotation=(0.0, 0.0, 3.1415927)
                ),
                scale=math_4,
            )
            math_5 = math_1 * math_4
            math_6 = factor_1.output * math_4
            vector_math_4 = (
                vector_math_3 * g.CombineXYZ(x=math_2, y=math_2)
                + spline_position.output
            )
            set_position = g.SetPosition(
                geometry=curve_to_mesh,
                position=vector_math_4
                + g.CombineXYZ(z=math_5 + (vector_math_3.z - math_6) * math_3),
            )
            set_position_1 = g.SetPosition(
                geometry=curve_to_mesh_1,
                position=vector_math_4
                - g.CombineXYZ(z=math_5 + (vector_math_3.z * -1.0 - math_6) * math_3),
            )
            capture_4 = g.CaptureAttribute.face(geometry=set_position)
            boolean = capture_4.items.boolean("Boolean", True)
            with g.Frame("UV"):
                combine_xyz = g.CombineXYZ(
                    x=factor_1.output,
                    y=1.0 - Curve_UV_factor_propagate(**{"Input": factor.output}),
                )
                vector_math_5 = combine_xyz.o.vector * (0.5, 1.0, 1.0)
                switch_6 = boolean.output.switch.vector(
                    vector_math_5 * (-1.0, 1.0, 1.0), vector_math_5 + (1.0, 0.0, 0.0)
                )
            capture_5 = g.CaptureAttribute.face(geometry=set_position_1)
            boolean_1 = capture_5.items.boolean("Boolean", True)
            set_mesh_normal = g.GeometryToInstance(
                capture_4.o.geometry, capture_5.o.geometry
            ) >> g.SetMeshNormal(
                edge_sharpness=boolean_math, face_sharpness=boolean_math
            )
            store_named_attribute = g.StoreNamedAttribute.corner.vector_2d(
                set_mesh_normal, name=uv_map_name, value=switch_6
            )
            merge_by_distance = uv_map.switch.geometry(
                set_mesh_normal, store_named_attribute
            ) >> g.MergeByDistance(
                selection=g.Compare.float.equal(factor_1.output, 1.0, 0.001),
                distance=0.001,
            )
        with g.Frame("Select Cap Endpoints"):
            boolean_math_1 = g.Compare.float.equal(
                factor_1.output, 0.0, 0.001
            ).o.result & (boolean.output | boolean_1.output)
        menu_switch_2 = g.MenuSwitch.geometry(
            profile_mode,
            {
                "Round": (
                    g.CurveCircle(resolution=profile_resolution),
                    "Use a circle to define the profile",
                ),
                "Custom": (
                    capture_2.o.geometry,
                    "Use a custom object to define the profile",
                ),
            },
        )
        with g.Frame("Estimate merge distance"):
            with g.Frame("round"):
                math_7 = (
                    g.NamedAttribute(name="radius").o.exists.switch.float(
                        1.0, g.Radius()
                    )
                    * scale
                )
                attribute_statistic = g.AttributeStatistic(
                    geometry=curve,
                    selection=g.EndpointSelection().o.selection
                    & g.Compare.float.not_equal(math_7, 0.0, 0.0),
                    attribute=math_7,
                )
                math_8 = (
                    attribute_statistic.o.min * 6.2831855 / (profile_resolution - 1)
                )
            compare_1 = vector_math_1 > 0.0
            with g.Frame("custom"):
                attribute_statistic_1 = g.AttributeStatistic(
                    geometry=capture_2.o.geometry,
                    selection=compare_1,
                    attribute=vector_math_1,
                )
                math_9 = attribute_statistic_1.o.min * attribute_statistic.o.min
            math_10 = menu_switch_2.o.custom.switch.float(math_8, math_9) * 0.5
            switch_7 = (math_10 > 0.0).switch.float(0.00001, math_10)
        with g.Frame("Custom Segment Length"):
            attribute_statistic_2 = g.AttributeStatistic(
                geometry=menu_switch_2, attribute=vector_math_2 * field_average
            )
        math_11 = (
            abs(menu_switch_2.o.custom.switch.float(math, attribute_statistic_2))
            * resample_scale
        )
        with g.Frame("Estimate Count"):
            float_to_integer = g.FloatToInteger(
                float=g.SplineLength().o.length / resample_length,
                rounding_mode="CEILING",
            )
            float_to_integer_1 = g.FloatToInteger(
                float=g.SplineLength().o.length / math_11, rounding_mode="CEILING"
            )
        index_switch = g.IndexSwitch.integer(
            menu_switch_1, (0, float_to_integer_1, resample_count, float_to_integer)
        )
        with g.Frame("Resample"):
            with g.Frame("Pre-Sample Resolution"):
                integer_math = index_switch.o.output / (
                    g.SplineLength().o.point_count - 1
                )
                compare_2 = integer_math > g.SplineResolution()
            separate_components = g.SeparateComponents(geometry=curve)
            compare_3 = g.SplineLength().o.point_count > 1
            resample_curve_2 = g.ResampleCurve(
                curve=separate_components.o.curve,
                mode="Evaluated",
                length=0.1,
                keep_last_segment=True,
            )
            set_spline_resolution = g.SetSplineResolution(
                geometry=separate_components.o.curve,
                selection=compare_2,
                resolution=integer_math,
            )
            set_spline_resolution_1 = g.SetSplineResolution(
                geometry=separate_components.o.curve,
                selection=compare_2,
                resolution=integer_math,
            )
            set_spline_resolution_2 = g.SetSplineResolution(
                geometry=separate_components.o.curve,
                selection=compare_2,
                resolution=integer_math,
            )
            resample_curve_3 = g.ResampleCurve(
                curve=set_spline_resolution,
                selection=compare_3,
                length=resample_length,
                mode="Length",
                keep_last_segment=True,
            )
            resample_curve_4 = g.ResampleCurve(
                curve=set_spline_resolution_1,
                selection=compare_3,
                count=resample_count,
                length=0.1,
                keep_last_segment=True,
            )
            resample_curve_5 = g.ResampleCurve(
                curve=set_spline_resolution_2,
                selection=compare_3,
                length=math_11,
                mode="Length",
                keep_last_segment=True,
            )
            index_switch_1 = g.IndexSwitch.geometry(
                menu_switch_1,
                (
                    resample_curve_2,
                    resample_curve_5,
                    resample_curve_4,
                    resample_curve_3,
                ),
            )
            switch_8 = resample.switch.geometry(
                separate_components.o.curve, index_switch_1
            )
        with g.Frame("Calculate Radius Derivatives"):
            value = g.Value(0.001)
            evaluate_on_domain = g.Index().o.index.spline.evaluate()
            math_12 = (
                g.NamedAttribute(name="radius").o.exists.switch.float(1.0, g.Radius())
                * scale
            )
            sample_curve = g.SampleCurve(
                curves=switch_8,
                value=math_12,
                length=value,
                curve_index=evaluate_on_domain,
                mode="LENGTH",
            )
            sample_index = g.SampleIndex(
                geometry=switch_8,
                value=math_12,
                index=g.PointsOfCurve().o.point_index.spline.evaluate(),
            )
            sample_index_1 = g.SampleIndex(
                geometry=switch_8,
                value=math_12,
                index=g.PointsOfCurve(sort_index=-1).o.point_index.spline.evaluate(),
            )
            sample_curve_1 = g.SampleCurve(
                curves=switch_8,
                value=math_12,
                length=g.SplineLength().o.length - value,
                curve_index=evaluate_on_domain,
                mode="LENGTH",
            )
            capture_6 = g.CaptureAttribute.curve(geometry=switch_8)
            radius_start = capture_6.items.float("Radius Start", sample_index)
            radius_end = capture_6.items.float("Radius End", sample_index_1)
            radius_derivative_start = capture_6.items.float(
                "Radius Derivative Start", (sample_index.o.value - sample_curve) / value
            )
            radius_derivative_end = capture_6.items.float(
                "Radius Derivative End",
                (sample_index_1.o.value - sample_curve_1) / value,
            )
        capture_7 = g.CaptureAttribute.point(geometry=capture_6.o.geometry)
        radius = capture_7.items.float(
            "Radius",
            abs(
                g.NamedAttribute(name="radius").o.exists.switch.float(1.0, g.Radius())
                * scale
            ),
        )
        with g.Frame("Tube Mesh & UVs"):
            group = Curve_UV(**{"Menu": uv_map_parameter_u})
            group_1 = Curve_UV(**{"Menu": uv_map_parameter_v})
            switch_9 = flip_and_cyclic.output.switch.float(
                group_1,
                group_1.o.factor.point.at(g.OffsetPointInCurve(offset=1).o.point_index),
            )
            capture_8 = g.CaptureAttribute.point(geometry=menu_switch_2)
            factor_2 = capture_8.items.float(
                "Factor", menu_switch_2.o.custom.switch.float(group_1, switch_9)
            )
            capture_9 = g.CaptureAttribute.curve(geometry=capture_7.o.geometry)
            use_length = capture_9.items.boolean("Use Length", group.o.length)
            length = capture_9.items.float("Length", g.SplineLength().o.length)
            capture_10 = g.CaptureAttribute.point(geometry=capture_9.o.geometry)
            factor_3 = capture_10.items.float("Factor", group.o.factor)
            start_point = capture_10.items.boolean(
                "Start Point", g.EndpointSelection(end_size=0)
            )
            end_point = capture_10.items.boolean(
                "End Point", g.EndpointSelection(start_size=0)
            )
            curve_to_mesh_2 = capture_10.o.geometry >> g.CurveToMesh(
                profile_curve=capture_8.o.geometry,
                scale=radius.output,
                fill_caps=switch_2,
            )
            group_2 = Curve_UV_factor_propagate(**{"Input": factor_3.output})
            combine_xyz_1 = g.CombineXYZ(
                x=use_length.output.switch.float(
                    group_2, group_2.o.output * length.output
                ),
                y=1.0 - Curve_UV_factor_propagate(**{"Input": factor_2.output}),
            )
            store_named_attribute_1 = g.StoreNamedAttribute.corner.vector_2d(
                curve_to_mesh_2, name=uv_map_name, value=combine_xyz_1
            )
            switch_10 = uv_map.switch.geometry(curve_to_mesh_2, store_named_attribute_1)
        with g.Frame("Shade Smooth and Flat Caps Smooth"):
            switch_11 = caps.switch.boolean(
                true=~g.IsEdgeSmooth().o.smooth
                & ~menu_switch.o.flat.switch.boolean(true=caps_smooth)
            )
            set_mesh_normal_1 = switch_10 >> g.SetMeshNormal(
                edge_sharpness=switch_11, face_sharpness=~shade_smooth
            )
        switch_12 = uv_map.switch.boolean(true=group.o.length)
        capture_11 = g.CaptureAttribute.point(geometry=capture_9.o.geometry)
        radius_1 = capture_11.items.float("Radius", radius.output)
        selection = capture_11.items.boolean("Selection", g.EndpointSelection())
        with g.Frame("Round / Object Caps"):
            endpoint_selection = g.EndpointSelection(start_size=0)
            with g.Frame("Double for single point curves"):
                switch_13 = g.Compare.integer.equal(
                    g.SplineLength().o.point_count, 1
                ).o.result.switch.integer(1, 2)
            geometry_to_instance = g.GeometryToInstance(
                g.ObjectInfo(object=caps_start).o.geometry,
                g.ObjectInfo(object=caps_end).o.geometry,
            )
            switch_14 = switch_3.switch.integer(
                endpoint_selection, endpoint_selection.o.selection.switch.integer(1)
            )
            menu_switch_3 = g.MenuSwitch.geometry(
                caps_input,
                {
                    "Object": geometry_to_instance,
                    "Geometry": g.GeometryToInstance(caps_start_1, caps_end_1),
                },
            )
            group_3 = Half_spheres(
                **{
                    "Resolution": profile_resolution,
                    "Shade Smooth": shade_smooth,
                    "UV Map": uv_map,
                    "UV Name": uv_map_name,
                    "Align Normals": shade_smooth.switch.boolean(
                        true=caps_merge.switch.boolean(caps_align_normals)
                    ),
                }
            )
            switch_15 = menu_switch_2.o.custom.switch.geometry(
                g.GeometryToInstance(group_3, group_3.o.bottom), merge_by_distance
            )
            capture_12 = g.CaptureAttribute.curve(geometry=capture_11.o.geometry)
            index = capture_12.items.integer("Index", g.Index())
            capture_13 = g.CaptureAttribute.point(geometry=capture_12.o.geometry)
            start_point_1 = capture_13.items.boolean(
                "Start Point", g.EndpointSelection(end_size=0)
            )
            end_point_1 = capture_13.items.boolean(
                "End Point", g.EndpointSelection(start_size=0)
            )
            sample_curve_2 = g.SampleCurve(
                curves=capture_12.o.geometry,
                factor=endpoint_selection.o.selection.switch.float(true=1.0),
                curve_index=index.output,
            )
            duplicate_elements = capture_13.o.geometry >> g.DuplicateElements.spline(
                amount=switch_13
            )
            axes_to_rotation = g.AxesToRotation(
                primary_axis=sample_curve_2.o.tangent,
                secondary_axis=sample_curve_2.o.normal,
            )
            instance_on_points = duplicate_elements >> g.InstanceOnPoints(
                selection=(start_point_1.output | end_point_1.output)
                & ~g.IsSplineCyclic().o.cyclic,
                instance=g.IndexSwitch.geometry(
                    menu_switch, (None, None, switch_15, menu_switch_3)
                ),
                instance_index=switch_14 + duplicate_elements.o.duplicate_index,
                rotation=axes_to_rotation,
                scale=radius.output,
                pick_instance=True,
            )
        with g.Frame("Realize"):
            capture_14 = g.CaptureAttribute.instance(
                geometry=g.JoinGeometry(
                    geometry=(set_mesh_normal_1, instance_on_points)
                )
            )
            index_1 = capture_14.items.integer("Index", g.Index())
            transform = capture_14.items.matrix("Transform", g.InstanceTransform())
            realize_instances = g.RealizeInstances(
                geometry=capture_14.o.geometry, realize_to_point_domain=True
            )
            switch_16 = caps.switch.boolean(true=caps_merge).switch.geometry(
                switch_3.switch.geometry(capture_14.o.geometry, realize_instances),
                realize_instances,
            )
        with g.Frame("Adjust UVs - U"):
            math_13 = (
                radius_1.output
                * 4.0
                * menu_switch_2.o.custom.switch.float(
                    1.0, spline_length.output / 6.2831855
                )
            )
            vector_math_6 = g.NamedAttribute.vector(
                uv_map_name
            ).o.attribute - end_point_1.output.switch.vector(
                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)
            )
            vector_math_7 = vector_math_6 * g.CombineXYZ(x=math_13, y=1.0)
            switch_17 = end_point_1.output.switch.vector(
                vector_math_7, vector_math_7 + g.CombineXYZ(x=length.output)
            )
            store_named_attribute_2 = g.StoreNamedAttribute.corner.vector_2d(
                switch_16, selection.output, uv_map_name, switch_17
            )
            switch_18 = switch_12.switch.geometry(switch_16, store_named_attribute_2)
        switch_19 = menu_switch_2.o.custom.switch.boolean(
            group_3.o.boolean, boolean_math_1
        )
        with g.Frame("Custom Cap Merging"):
            separate_geometry = g.SeparateGeometry.instance(
                menu_switch_3, g.Compare.integer.equal(g.Index(), 0)
            )
            compare_4 = (
                g.DomainSize(
                    geometry=g.RealizeInstances(geometry=separate_geometry.o.inverted)
                ).o.face_count
                > 0
            )
            boolean_math_2 = start_point.output & (
                (
                    separate_geometry >> g.RealizeInstances() >> g.DomainSize()
                ).o.face_count
                > 0
            )
            switch_20 = switch_4.switch.boolean(
                start_point.output | end_point.output,
                boolean_math_2 | end_point.output & compare_4,
            )
            boolean_math_3 = switch_19 | switch_20
        merge_by_distance_1 = g.MergeByDistance(
            geometry=switch_18,
            selection=boolean_math_3 | capture_14.o.selection,
            distance=switch_7,
        )
        switch_21 = caps.switch.boolean(true=caps_merge).switch.geometry(
            switch_18, merge_by_distance_1
        )
        with g.Frame("Material Transfer"):
            attribute_statistic_3 = g.AttributeStatistic(
                geometry=capture_11.o.geometry,
                attribute=g.MaterialIndex(),
                domain="CURVE",
            )
            sample_index_2 = g.SampleIndex(
                geometry=capture_11.o.geometry,
                value=g.MaterialIndex(),
                index=index_1.output / 2,
                data_type="INT",
                domain="CURVE",
            )
            switch_22 = g.Compare.integer.equal(
                attribute_statistic_3.o.max, 0
            ).o.result.switch.geometry(
                switch_21,
                g.SetMaterialIndex(geometry=switch_21, material_index=sample_index_2),
            )
        with g.Frame("Extrapolate Radius"):
            switch_23 = caps.switch.boolean(true=caps_merge).switch.boolean(
                selection.output,
                g.Compare.float.equal(
                    g.BlurAttribute(value=selection.output), 1.0, 0.001
                ),
            )
            switch_24 = end_point_1.output.switch.float(
                radius_derivative_start.output / radius_start.output,
                radius_derivative_end.output / radius_end.output,
            )
            combine_transform = g.CombineTransform(
                translation=transform.output.translation,
                rotation=transform.output.rotation,
            )
            invert_matrix = combine_transform.o.transform.invert()
            transform_point = g.Position().o.position.transform(invert_matrix)
            transform_point_1 = spline_position.output.transform(
                transform.output
            ).transform(invert_matrix)
            switch_25 = menu_switch_2.o.custom.switch.float(
                abs(transform_point.z), math_1 * transform.output.scale.z
            )
            math_14 = switch_25 * switch_24 + 1.0
            combine_xyz_2 = g.CombineXYZ(
                x=math_14,
                y=math_14,
                z=g.Mix(
                    a_float=math_14, factor_float=0.5, b_float=1.0, clamp_factor=True
                ),
            )
            vector_math_8 = transform_point * combine_xyz_2
            mix = g.Mix(
                a_vector=vector_math_8,
                b_vector=(transform_point - transform_point_1) * combine_xyz_2
                + transform_point_1,
                factor_float=0.5,
                data_type="VECTOR",
                clamp_factor=True,
            )
            transform_point_2 = menu_switch_2.o.custom.switch.vector(
                vector_math_8, mix.o.result_vector
            ).transform(combine_transform)
            switch_26 = caps_extrapolate_radius.switch.geometry(
                switch_22,
                g.SetPosition(
                    geometry=switch_22, selection=switch_23, position=transform_point_2
                ),
            )
        switch_27 = caps.switch.geometry(
            set_mesh_normal_1,
            g.IndexSwitch.geometry(
                menu_switch, (None, set_mesh_normal_1, switch_26, switch_21)
            ),
        )
        with g.Frame("Adjust UVs - V"):
            math_15 = 1.0 * menu_switch_2.o.custom.switch.float(
                6.2831855, spline_length.output
            )
            math_16 = math_15 * radius.output
            switch_28 = (
                (~menu_switch.o.flat)
                .switch.boolean(true=caps_extrapolate_radius)
                .switch.float(
                    math_16,
                    math_16
                    * g.Switch(
                        switch=g.EvaluateOnDomain(value=switch_23),
                        true=math_14,
                        false=1.0,
                    ),
                )
            )
            combine_xyz_3 = g.CombineXYZ(
                y=consider_curve_radius.switch.float(
                    math_15, caps.switch.float(math_16, switch_28)
                ),
                x=1.0,
                z=1.0,
            )
            store_named_attribute_3 = g.StoreNamedAttribute.corner.vector_2d(
                switch_27,
                name=uv_map_name,
                value=g.NamedAttribute.vector(uv_map_name).o.attribute * combine_xyz_3,
            )
            switch_29 = uv_map.switch.boolean(true=group_1.o.length).switch.geometry(
                switch_27, store_named_attribute_3
            )
        with g.Frame("Pass-Through"):
            with g.Frame("Scale is 0"):
                compare_5 = g.Compare.float.equal(
                    g.AttributeStatistic(geometry=curve, attribute=scale).o.max,
                    0.0,
                    0.0,
                )
                switch_30 = g.Warning.warning(
                    compare_5, "Scale is 0"
                ).o.show.switch.geometry(switch_29, curve)
            with g.Frame("No Curves"):
                compare_6 = g.Compare.integer.equal(
                    g.DomainSize(geometry=curve, component="CURVE").o.spline_count, 0
                )
                (
                    g.Warning.warning(
                        compare_6, "No curve data in input"
                    ).o.show.switch.geometry(switch_30, curve)
                    >> mesh
                )

        profile_mode.default_value = "Round"
        profile_input.default_value = "Object"
        resample_mode.default_value = "Evaluated"
        caps_type.default_value = "Flat"
        caps_input.default_value = "Object"
        uv_map_parameter_u.default_value = "Length"
        uv_map_parameter_v.default_value = "Factor"


ASSET = CurveToTube

ASSET_METADATA = {
    "description": "Convert curve geometry into tube meshes",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "6ecdfe44-a0d7-40b9-8518-b92c97a1b4f2",
    "catalog_simple_name": "Generate",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
