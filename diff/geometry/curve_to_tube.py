# Node-group asset 'Curve to Tube' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class Curve_UV_factor_propagate(CustomGeometryGroup):
    _name = ".curve_UV_factor_propagate"

    def _build_group(self, tree):
        tree.disable_arrange()

        input = tree.inputs.float("Input", 0.0)
        output = tree.outputs.float("Output")

        reroute = g.Reroute(input=input)
        boolean_math = (
            reroute.o.output.corner.at(g.OffsetCornerInFace(offset=-1)) > 0.5
        ) | (reroute.o.output.corner.at(g.OffsetCornerInFace(offset=1)) > 0.5)
        (
            (
                g.Compare.float.equal(reroute, 0.0, 0.0).o.result & boolean_math
            ).switch.float(reroute, 1.0)
            >> output
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (720.0, 80.0),
            "Group Input": (-751.1, 108.2),
            "Offset Corner in Face.006": (-565.8, -102.6),
            "Offset Corner in Face.007": (-565.8, -222.6),
            "Compare.010": (90.6, 1.6),
            "Switch.008": (520.0, 100.0),
            "Boolean Math.012": (297.1, -8.4),
            "Evaluate at Index.006": (-384.1, -53.8),
            "Boolean Math.013": (96.3, -137.6),
            "Evaluate at Index.007": (-378.3, -224.8),
            "Compare.011": (-167.2, -50.4),
            "Compare.012": (-170.8, -218.4),
            "Reroute.014": (-471.4, 33.7),
        }


class Curve_UV(CustomGeometryGroup):
    _name = ".curve_UV"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

        menu = tree.inputs.menu("Menu", optional_label=True)
        factor = tree.outputs.float(
            "Factor",
            description="For points, the portion of the spline's total length at the control point. For Splines, the factor of that spline within the entire curve",
        )
        length = tree.outputs.boolean("Length")

        spline_parameter = g.SplineParameter()
        reroute = g.Reroute(input=spline_parameter.o.factor)
        math = g.Math.divide(
            spline_parameter.o.index,
            g.SplineLength().o.point_count - ~g.IsSplineCyclic().o.cyclic,
        )
        menu_switch = g.MenuSwitch.float(
            menu,
            {
                "Factor": (reroute, "Use the portion of the curve's total length"),
                "Length": (
                    reroute,
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

        # Restore authored node positions.
        tree.node_positions = {
            "Group Input": (-395.9, 72.6),
            "Group Output": (356.7, 48.7),
            "Spline Parameter.001": (-500.0, -40.0),
            "Menu Switch": (-108.7, 39.6),
            "Math": (-307.4, -109.5),
            "Spline Length": (-860.0, -200.0),
            "Integer Math": (-500.0, -180.0),
            "Is Spline Cyclic": (-860.0, -280.0),
            "Boolean Math": (-680.0, -280.0),
            "Reroute": (-165.3, -53.7),
        }


class UV_sphere_corrected(CustomGeometryGroup):
    _name = ".UV_sphere_corrected"

    def _build_group(self, tree):
        tree.disable_arrange()

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
        reroute = g.Reroute(input=segments)
        math = 1.0 / reroute
        capture = g.CaptureAttribute.point(geometry=uv_sphere)
        result = capture.items.boolean(
            "Result",
            g.Compare.float.equal(abs(g.Position().o.position.z), 0.0, 0.00001),
        )
        switch = (
            ((g.Index().o.index + 1).modulo(reroute) <= 0)
            .face.evaluate()
            .switch.float(math, -1.0 + math)
        )
        combine_xyz = g.CombineXYZ(
            x=uv_sphere.o.uv_map.x + switch, y=uv_sphere.o.uv_map.y
        )

        capture.o.geometry >> mesh
        combine_xyz >> uv_map
        result.output >> equator

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (706.4, 35.9),
            "Group Input": (-1120.3, 9.0),
            "UV Sphere": (-688.5, 103.1),
            "Combine XYZ": (497.2, -93.1),
            "Math": (-531.3, -254.3),
            "Evaluate on Domain": (-137.1, -134.6),
            "Index.001": (-920.3, -158.3),
            "Integer Math.002": (-508.2, -140.2),
            "Reroute": (-708.0, -290.3),
            "Compare.001": (-328.5, -152.8),
            "Switch": (63.7, -193.3),
            "Integer Math.003": (-714.4, -114.8),
            "Math.002": (-181.0, -327.5),
            "Separate XYZ.001": (-455.0, 26.5),
            "Math.001": (282.2, -26.0),
            "Compare": (-711.3, 311.8),
            "Separate XYZ": (-1098.6, 284.1),
            "Position": (-1296.4, 283.5),
            "Math.003": (-925.7, 298.0),
            "Capture Attribute": (-271.0, 119.5),
        }


class Half_spheres(CustomGeometryGroup):
    _name = ".half_spheres"

    def _build_group(self, tree):
        tree.disable_arrange()

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
            Segments=resolution,
            Rings=g.IntegerMath.divide_round(resolution, 2).o.value * 2,
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
        reroute = g.Reroute(input=switch)
        separate_geometry = uv_map.switch.geometry(
            reroute,
            g.StoreNamedAttribute.corner.vector_2d(
                reroute, name=uv_name, value=rotate_vector
            ),
        ) >> g.SeparateGeometry.face(selection=top_1.output)

        separate_geometry >> top
        separate_geometry.o.inverted >> bottom
        group.o.equator >> boolean

        # Restore authored node positions.
        tree.node_positions = {
            "Set Mesh Normal.001": (409.8, 957.5),
            "Boolean Math.001": (157.9, 837.5),
            "Set Mesh Normal.002": (776.4, 807.4),
            "Capture Attribute": (133.9, 1014.0),
            "Normal.001": (-678.8, 818.6),
            "Switch.003": (1219.2, 940.3),
            "Store Named Attribute.001": (1987.4, 1208.5),
            "Integer Math": (-1357.9, 1019.6),
            "Integer Math.001": (-1094.2, 987.6),
            "Group Input": (-1615.1, 1094.7),
            "Group Output": (2962.5, 926.4),
            "Group Input.001": (-109.6, 785.2),
            "Group Input.003": (1693.7, 1028.7),
            "Group": (-740.6, 1121.0),
            "Group Input.004": (760.3, 1074.4),
            "Separate Geometry": (2776.5, 934.3),
            "Compare.001": (-389.0, 1346.1),
            "Separate XYZ.001": (-557.7, 1256.0),
            "Position.001": (-762.9, 1287.7),
            "Capture Attribute.001": (-112.0, 1151.9),
            "Rotate Vector": (1220.9, 1511.9),
            "Vector Math": (1030.9, 1506.3),
            "Switch.001": (819.6, 1391.3),
            "Transform Geometry": (-409.6, 1149.6),
            "Switch": (2237.0, 1294.8),
            "Reroute": (1789.2, 1213.2),
            "Group Input.005": (1985.6, 1333.7),
        }


class CurveToTube(CustomGeometryGroup):
    _name = "Curve to Tube"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

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
        _miter_scale = tree.inputs.boolean(
            "Miter Scale",
            True,
            description="Scale the profile along the axis of the corner's turn to maintain a constant visual width",
            is_panel_toggle=True,
        )
        _miter_scale_limit = tree.inputs.float(
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
            switch = offset_point_in_curve.o.is_valid_offset.switch.integer(
                g.Index(), offset_point_in_curve.o.point_index
            )
            reroute = g.Reroute(input=g.Position().o.position)
            vector_math_1 = (
                (reroute.o.output - reroute.o.output.point.at(switch))
                .point.evaluate()
                .length()
            )
        with g.Frame("Segment Length"):
            offset_point_in_curve_1 = g.OffsetPointInCurve(offset=-1)
            switch_1 = offset_point_in_curve_1.o.is_valid_offset.switch.integer(
                g.Index(), offset_point_in_curve_1.o.point_index
            )
            reroute_1 = g.Reroute(input=g.Position().o.position)
            vector_math_2 = (
                (reroute_1.o.output - reroute_1.o.output.point.at(switch_1))
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
        reroute_2 = g.Reroute(input=menu_switch.o.flat)
        reroute_3 = g.Reroute(input=menu_switch_1.o.output)
        resample_curve = g.MenuSwitch.geometry(
            profile_input,
            {
                "Object": g.ObjectInfo(object=profile_object).o.geometry,
                "Geometry": profile_geometry,
            },
        ) >> g.ResampleCurve(mode="Evaluated", length=0.1, keep_last_segment=True)
        reroute_4 = g.Reroute(input=g.Reroute(input=menu_switch.o.output).o.output)
        reroute_5 = g.Reroute(input=reroute_3.o.output)
        reroute_6 = g.Reroute(input=caps.switch.boolean(true=reroute_2))
        reroute_7 = g.Reroute(input=g.Reroute(input=reroute_2.o.output).o.output)
        reroute_8 = g.Reroute(
            input=g.Reroute(
                input=caps.switch.boolean(true=g.Reroute(input=menu_switch.o.round))
            ).o.output
        )
        reroute_9 = g.Reroute(
            input=g.Reroute(
                input=caps.switch.boolean(true=g.Reroute(input=menu_switch.o.custom))
            ).o.output
        )
        reroute_10 = g.Reroute(input=reroute_8.o.output)
        reroute_11 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(
                    input=g.Reroute(input=reroute_4.o.output).o.output
                ).o.output
            ).o.output
        )
        reroute_12 = g.Reroute(input=g.Reroute(input=reroute_9.o.output).o.output)
        capture = g.CaptureAttribute.curve(geometry=resample_curve)
        flip = capture.items.boolean("Flip", compare)
        flip_and_cyclic = capture.items.boolean(
            "Flip and Cyclic", compare & g.IsSplineCyclic()
        )
        reroute_13 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(
                    input=g.Reroute(input=reroute_7.o.output).o.output
                ).o.output
            ).o.output
        )
        reverse_curve = capture.o.geometry >> g.ReverseCurve(selection=flip.output)
        reroute_14 = g.Reroute(input=flip_and_cyclic.output)
        with g.Frame("Pre-Processing"):
            spline_parameter = g.SplineParameter()
            switch_2 = reroute_14.o.output.switch.float(
                spline_parameter,
                spline_parameter.o.factor.point.at(
                    g.OffsetPointInCurve(offset=1).o.point_index
                ),
            )
            capture_1 = g.CaptureAttribute.point(
                geometry=g.Reroute(input=reverse_curve.o.curve)
                >> g.SetCurveNormal(mode="Free")
            )
            factor = capture_1.items.float("Factor", switch_2)
            capture_2 = g.CaptureAttribute.curve(geometry=capture_1.o.geometry)
            spline_position = capture_2.items.vector("Spline Position", g.Position())
            spline_length = capture_2.items.float(
                "Spline Length", g.SplineLength().o.length
            )
            reroute_15 = g.Reroute(input=factor.output)
        reroute_16 = g.Reroute(input=reroute_14.o.output)
        reroute_17 = g.Reroute(input=g.Reroute(input=reroute_13.o.output).o.output)
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
        with g.Frame("Custom Segment Length"):
            attribute_statistic = g.AttributeStatistic(
                geometry=menu_switch_2, attribute=vector_math_2 * field_average
            )
        reroute_18 = g.Reroute(input=capture_2.o.geometry)
        reroute_19 = g.Reroute(input=spline_length.output)
        reroute_20 = g.Reroute(input=menu_switch_2.o.custom)
        reroute_21 = g.Reroute(input=menu_switch_2.o.output)
        reroute_22 = g.Reroute(input=reroute_18.o.output)
        reroute_23 = g.Reroute(input=g.Reroute(input=spline_position.output).o.output)
        reroute_24 = g.Reroute(input=reroute_20.o.output)
        reroute_25 = g.Reroute(input=reroute_23.o.output)
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
            reroute_26 = g.Reroute(input=g.Reroute(input=factor_1.output).o.output)
            reroute_27 = g.Reroute(input=math_1)
            reroute_28 = g.Reroute(input=reroute_26.o.output)
            with g.Frame("circular profile"):
                math_2 = (1.0 - reroute_27.o.output**2.0).sqrt()
            reroute_29 = g.Reroute(input=reroute_28.o.output)
            reroute_30 = g.Reroute(input=1.0 - reroute_27)
            reroute_31 = g.Reroute(input=reroute_15.o.output)
            math_3 = reroute_19.o.output / 6.2831855
            curve_to_mesh = g.CurveToMesh(
                curve=reroute_22,
                profile_curve=g.ReverseCurve(curve=capture_3.o.geometry),
                scale=math_3,
            )
            reroute_32 = g.Reroute(input=math_3)
            vector_math_3 = g.Position().o.position - reroute_23
            reroute_33 = g.Reroute(input=reroute_27.o.output * reroute_32)
            reroute_34 = g.Reroute(input=factor_1.output * reroute_32)
            vector_math_4 = (
                vector_math_3 * g.CombineXYZ(x=math_2, y=math_2) + reroute_25
            )
            reroute_35 = g.Reroute(input=vector_math_3.z)
            combine_xyz = g.CombineXYZ(
                z=reroute_33.o.output
                + (reroute_35.o.output * -1.0 - reroute_34) * reroute_30
            )
            vector_math_5 = vector_math_4 + g.CombineXYZ(
                z=reroute_33.o.output + (reroute_35.o.output - reroute_34) * reroute_30
            )
            set_position = (
                g.Reroute(input=reroute_18.o.output)
                >> g.CurveToMesh(
                    profile_curve=g.TransformGeometry(
                        geometry=capture_3.o.geometry, rotation=(0.0, 0.0, 3.1415927)
                    ),
                    scale=reroute_32,
                )
                >> g.SetPosition(position=vector_math_4 - combine_xyz)
            )
            capture_4 = g.CaptureAttribute.face(
                geometry=g.Reroute(input=curve_to_mesh.o.mesh)
                >> g.SetPosition(position=vector_math_5)
            )
            boolean = capture_4.items.boolean("Boolean", True)
            with g.Frame("UV"):
                vector_math_6 = g.CombineXYZ(
                    x=reroute_26, y=1.0 - Curve_UV_factor_propagate(Input=reroute_31)
                ).o.vector * (0.5, 1.0, 1.0)
                reroute_36 = g.Reroute(input=vector_math_6)
                switch_3 = boolean.output.switch.vector(
                    reroute_36.o.output * (-1.0, 1.0, 1.0),
                    reroute_36.o.output + (1.0, 0.0, 0.0),
                )
            capture_5 = g.CaptureAttribute.face(geometry=set_position)
            boolean_1 = capture_5.items.boolean("Boolean", True)
            reroute_37 = g.Reroute(input=g.Reroute(input=boolean.output).o.output)
            set_mesh_normal = g.GeometryToInstance(
                capture_4.o.geometry, capture_5.o.geometry
            ) >> g.SetMeshNormal(
                edge_sharpness=boolean_math, face_sharpness=boolean_math
            )
            reroute_38 = g.Reroute(input=g.Reroute(input=boolean_1.output).o.output)
            store_named_attribute = g.StoreNamedAttribute.corner.vector_2d(
                set_mesh_normal, name=uv_map_name, value=switch_3
            )
            merge_by_distance = uv_map.switch.geometry(
                set_mesh_normal, store_named_attribute
            ) >> g.MergeByDistance(
                selection=g.Compare.float.equal(reroute_28, 1.0, 0.001), distance=0.001
            )
        reroute_39 = g.Reroute(input=g.Reroute(input=reroute_27.o.output).o.output)
        with g.Frame("Select Cap Endpoints"):
            boolean_math_1 = g.Compare.float.equal(reroute_29, 0.0, 0.001).o.result & (
                reroute_37.o.output | reroute_38
            )
        reroute_40 = g.Reroute(input=reroute_24.o.output)
        reroute_41 = g.Reroute(input=reroute_40.o.output)
        math_4 = (
            abs(reroute_20.o.output.switch.float(math, attribute_statistic))
            * resample_scale
        )
        with g.Frame("Estimate Count"):
            float_to_integer = g.FloatToInteger(
                float=g.SplineLength().o.length / resample_length,
                rounding_mode="CEILING",
            )
            float_to_integer_1 = g.FloatToInteger(
                float=g.SplineLength().o.length / g.Reroute(input=math_4),
                rounding_mode="CEILING",
            )
        reroute_42 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(
                    input=g.Reroute(input=reroute_19.o.output).o.output
                ).o.output
            ).o.output
        )
        reroute_43 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(
                    input=g.Reroute(input=reroute_22.o.output).o.output
                ).o.output
            ).o.output
        )
        reroute_44 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(
                    input=g.Reroute(input=reroute_25.o.output).o.output
                ).o.output
            ).o.output
        )
        reroute_45 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(input=reroute_41.o.output).o.output
            ).o.output
        )
        reroute_46 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(input=reroute_42.o.output).o.output
            ).o.output
        )
        reroute_47 = g.Reroute(input=reroute_44.o.output)
        index_switch = g.IndexSwitch.integer(
            reroute_3, (0, float_to_integer_1, resample_count, float_to_integer)
        )
        with g.Frame("Resample"):
            reroute_48 = g.Reroute(input=g.SeparateComponents(geometry=curve).o.curve)
            with g.Frame("Pre-Sample Resolution"):
                reroute_49 = g.Reroute(input=reroute_48.o.output)
                integer_math = g.Reroute(
                    input=g.Reroute(input=index_switch.o.output).o.output
                ).o.output / (g.SplineLength().o.point_count - 1)
                reroute_50 = g.Reroute(input=integer_math)
                reroute_51 = g.Reroute(input=reroute_50.o.output)
                reroute_52 = g.Reroute(input=reroute_50 > g.SplineResolution())
            reroute_53 = g.Reroute(input=g.SplineLength().o.point_count > 1)
            reroute_54 = g.Reroute(input=reroute_53.o.output)
            resample_curve_2 = g.ResampleCurve(
                curve=g.SetSplineResolution(
                    geometry=reroute_49, selection=reroute_52, resolution=reroute_51
                ),
                selection=reroute_54,
                length=resample_length,
                mode="Length",
                keep_last_segment=True,
            )
            resample_curve_3 = g.ResampleCurve(
                curve=g.SetSplineResolution(
                    geometry=reroute_49, selection=reroute_52, resolution=reroute_51
                ),
                selection=reroute_54,
                count=resample_count,
                length=0.1,
                keep_last_segment=True,
            )
            resample_curve_4 = g.ResampleCurve(
                curve=g.SetSplineResolution(
                    geometry=reroute_49, selection=reroute_52, resolution=reroute_51
                ),
                selection=reroute_53,
                length=math_4,
                mode="Length",
                keep_last_segment=True,
            )
            index_switch_1 = g.IndexSwitch.geometry(
                reroute_5,
                (
                    g.ResampleCurve(
                        curve=reroute_48,
                        mode="Evaluated",
                        length=0.1,
                        keep_last_segment=True,
                    ),
                    resample_curve_4,
                    resample_curve_3,
                    resample_curve_2,
                ),
            )
            switch_4 = resample.switch.geometry(
                g.Reroute(input=g.Reroute(input=reroute_48.o.output).o.output),
                index_switch_1,
            )
        with g.Frame("Calculate Radius Derivatives"):
            value = g.Value(0.001)
            evaluate_on_domain = g.Index().o.index.spline.evaluate()
            reroute_55 = g.Reroute(input=value.o.value)
            reroute_56 = g.Reroute(
                input=g.NamedAttribute(name="radius").o.exists.switch.float(
                    1.0, g.Radius()
                )
                * scale
            )
            reroute_57 = g.Reroute(input=reroute_56.o.output)
            reroute_58 = g.Reroute(input=reroute_56.o.output)
            reroute_59 = g.Reroute(input=switch_4)
            reroute_60 = g.Reroute(input=reroute_59.o.output)
            reroute_61 = g.Reroute(input=reroute_59.o.output)
            sample_curve = g.SampleCurve(
                curves=reroute_60,
                value=reroute_57,
                length=reroute_55,
                curve_index=evaluate_on_domain,
                mode="LENGTH",
            )
            sample_index = g.SampleIndex(
                geometry=reroute_60,
                value=reroute_57,
                index=g.PointsOfCurve().o.point_index.spline.evaluate(),
            )
            sample_index_1 = g.SampleIndex(
                geometry=reroute_61,
                value=reroute_58,
                index=g.PointsOfCurve(sort_index=-1).o.point_index.spline.evaluate(),
            )
            sample_curve_1 = g.SampleCurve(
                curves=reroute_61,
                value=reroute_58,
                length=g.SplineLength().o.length - value,
                curve_index=evaluate_on_domain,
                mode="LENGTH",
            )
            capture_6 = g.CaptureAttribute.curve(geometry=reroute_59)
            radius_start = capture_6.items.float("Radius Start", sample_index)
            radius_end = capture_6.items.float("Radius End", sample_index_1)
            radius_derivative_start = capture_6.items.float(
                "Radius Derivative Start",
                (sample_index.o.value - sample_curve) / reroute_55,
            )
            radius_derivative_end = capture_6.items.float(
                "Radius Derivative End",
                (sample_index_1.o.value - sample_curve_1) / value,
            )
            reroute_62 = g.Reroute(input=radius_start.output)
            reroute_63 = g.Reroute(input=radius_end.output)
            reroute_64 = g.Reroute(input=radius_derivative_start.output)
            reroute_65 = g.Reroute(input=radius_derivative_end.output)
        reroute_66 = g.Reroute(input=g.Reroute(input=reroute_45.o.output).o.output)
        with g.Frame("Estimate merge distance"):
            with g.Frame("round"):
                math_5 = (
                    g.NamedAttribute(name="radius").o.exists.switch.float(
                        1.0, g.Radius()
                    )
                    * scale
                )
                attribute_statistic_1 = g.AttributeStatistic(
                    geometry=curve,
                    selection=g.EndpointSelection().o.selection
                    & g.Compare.float.not_equal(math_5, 0.0, 0.0),
                    attribute=math_5,
                )
                math_6 = (
                    attribute_statistic_1.o.min * 6.2831855 / (profile_resolution - 1)
                )
            reroute_67 = g.Reroute(input=vector_math_1)
            compare_1 = reroute_67 > 0.0
            with g.Frame("custom"):
                math_7 = (
                    reroute_43
                    >> g.AttributeStatistic(selection=compare_1, attribute=reroute_67)
                ).o.min * attribute_statistic_1.o.min
            math_8 = reroute_66.o.output.switch.float(math_6, math_7) * 0.5
            switch_5 = (math_8 > 0.0).switch.float(0.00001, math_8)
        reroute_68 = g.Reroute(input=reroute_66.o.output)
        capture_7 = g.CaptureAttribute.point(geometry=capture_6.o.geometry)
        radius = capture_7.items.float(
            "Radius",
            abs(
                g.NamedAttribute(name="radius").o.exists.switch.float(1.0, g.Radius())
                * scale
            ),
        )
        reroute_69 = g.Reroute(input=capture_7.o.geometry)
        reroute_70 = g.Reroute(input=radius.output)
        with g.Frame("Tube Mesh & UVs"):
            group = Curve_UV(Menu=uv_map_parameter_u)
            group_1 = Curve_UV(Menu=uv_map_parameter_v)
            reroute_71 = g.Reroute(input=g.Reroute(input=group.o.length).o.output)
            reroute_72 = g.Reroute(input=g.Reroute(input=group_1.o.length).o.output)
            switch_6 = g.Reroute(input=reroute_16.o.output).o.output.switch.float(
                group_1,
                group_1.o.factor.point.at(g.OffsetPointInCurve(offset=1).o.point_index),
            )
            capture_8 = g.CaptureAttribute.point(
                geometry=g.Reroute(input=reroute_21.o.output)
            )
            factor_2 = capture_8.items.float(
                "Factor",
                g.Reroute(input=reroute_24.o.output).o.output.switch.float(
                    group_1, switch_6
                ),
            )
            capture_9 = g.CaptureAttribute.curve(geometry=reroute_69)
            use_length = capture_9.items.boolean("Use Length", group.o.length)
            length = capture_9.items.float("Length", g.SplineLength().o.length)
            reroute_73 = g.Reroute(input=reroute_70.o.output)
            capture_10 = g.CaptureAttribute.point(geometry=capture_9.o.geometry)
            factor_3 = capture_10.items.float("Factor", group.o.factor)
            start_point = capture_10.items.boolean(
                "Start Point", g.EndpointSelection(end_size=0)
            )
            end_point = capture_10.items.boolean(
                "End Point", g.EndpointSelection(start_size=0)
            )
            reroute_74 = g.Reroute(input=length.output)
            curve_to_mesh_1 = capture_10.o.geometry >> g.CurveToMesh(
                profile_curve=capture_8.o.geometry,
                scale=reroute_73,
                fill_caps=reroute_6,
            )
            group_2 = Curve_UV_factor_propagate(Input=factor_3.output)
            reroute_75 = g.Reroute(input=end_point.output)
            reroute_76 = g.Reroute(input=start_point.output)
            reroute_77 = g.Reroute(input=reroute_74.o.output)
            reroute_78 = g.Reroute(input=curve_to_mesh_1.o.mesh)
            switch_7 = g.Reroute(input=use_length.output).o.output.switch.float(
                group_2, group_2.o.output * reroute_74
            )
            store_named_attribute_1 = g.StoreNamedAttribute.corner.vector_2d(
                reroute_78,
                name=uv_map_name,
                value=g.CombineXYZ(
                    x=switch_7, y=1.0 - Curve_UV_factor_propagate(Input=factor_2.output)
                ),
            )
            switch_8 = uv_map.switch.geometry(reroute_78, store_named_attribute_1)
        with g.Frame("Shade Smooth and Flat Caps Smooth"):
            boolean_math_2 = ~g.IsEdgeSmooth().o.smooth & ~g.Reroute(
                input=reroute_7.o.output
            ).o.output.switch.boolean(true=caps_smooth)
            set_mesh_normal_1 = switch_8 >> g.SetMeshNormal(
                edge_sharpness=caps.switch.boolean(true=boolean_math_2),
                face_sharpness=~shade_smooth,
            )
        switch_9 = uv_map.switch.boolean(true=g.Reroute(input=reroute_71.o.output))
        reroute_79 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(input=reroute_72.o.output).o.output
            ).o.output
        )
        reroute_80 = g.Reroute(input=reroute_62.o.output)
        reroute_81 = g.Reroute(input=reroute_63.o.output)
        reroute_82 = g.Reroute(input=reroute_64.o.output)
        reroute_83 = g.Reroute(input=reroute_65.o.output)
        reroute_84 = g.Reroute(input=reroute_70.o.output)
        capture_11 = g.CaptureAttribute.point(geometry=capture_9.o.geometry)
        radius_1 = capture_11.items.float("Radius", reroute_84)
        selection = capture_11.items.boolean("Selection", g.EndpointSelection())
        reroute_85 = g.Reroute(input=capture_11.o.geometry)
        with g.Frame("Round / Object Caps"):
            endpoint_selection = g.EndpointSelection(start_size=0)
            with g.Frame("Double for single point curves"):
                switch_10 = g.Compare.integer.equal(
                    g.SplineLength().o.point_count, 1
                ).o.result.switch.integer(1, 2)
            geometry_to_instance = g.GeometryToInstance(
                g.ObjectInfo(object=caps_start).o.geometry,
                g.ObjectInfo(object=caps_end).o.geometry,
            )
            menu_switch_3 = g.MenuSwitch.geometry(
                caps_input,
                {
                    "Object": geometry_to_instance,
                    "Geometry": g.GeometryToInstance(caps_start_1, caps_end_1),
                },
            )
            group_3 = Half_spheres(
                Resolution=profile_resolution,
                **{
                    "Shade Smooth": shade_smooth,
                    "UV Map": uv_map,
                    "UV Name": uv_map_name,
                    "Align Normals": shade_smooth.switch.boolean(
                        true=caps_merge.switch.boolean(caps_align_normals)
                    ),
                },
            )
            switch_11 = reroute_8.o.output.switch.integer(
                endpoint_selection, endpoint_selection.o.selection.switch.integer(1)
            )
            switch_12 = reroute_41.o.output.switch.geometry(
                g.GeometryToInstance(group_3, group_3.o.bottom),
                g.Reroute(input=merge_by_distance.o.geometry),
            )
            capture_12 = g.CaptureAttribute.curve(geometry=reroute_85)
            index = capture_12.items.integer("Index", g.Index())
            sample_curve_2 = g.SampleCurve(
                curves=capture_12.o.geometry,
                factor=endpoint_selection.o.selection.switch.float(true=1.0),
                curve_index=index.output,
            )
            axes_to_rotation = g.AxesToRotation(
                primary_axis=sample_curve_2.o.tangent,
                secondary_axis=sample_curve_2.o.normal,
            )
            capture_13 = g.CaptureAttribute.point(
                geometry=g.Reroute(
                    input=g.Reroute(input=capture_12.o.geometry).o.output
                )
            )
            start_point_1 = capture_13.items.boolean(
                "Start Point", g.EndpointSelection(end_size=0)
            )
            end_point_1 = capture_13.items.boolean(
                "End Point", g.EndpointSelection(start_size=0)
            )
            duplicate_elements = capture_13.o.geometry >> g.DuplicateElements.spline(
                amount=switch_10
            )
            integer_math_1 = (
                g.Reroute(input=g.Reroute(input=switch_11).o.output).o.output
                + duplicate_elements.o.duplicate_index
            )
            reroute_86 = g.Reroute(input=g.Reroute(input=end_point_1.output).o.output)
            instance_on_points = duplicate_elements >> g.InstanceOnPoints(
                selection=(start_point_1.output | end_point_1.output)
                & ~g.IsSplineCyclic().o.cyclic,
                instance=g.IndexSwitch.geometry(
                    reroute_4, (None, None, switch_12, menu_switch_3)
                ),
                instance_index=integer_math_1,
                rotation=axes_to_rotation,
                scale=g.Reroute(input=g.Reroute(input=reroute_73.o.output).o.output),
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
            switch_13 = caps.switch.boolean(true=caps_merge).switch.geometry(
                reroute_10.o.output.switch.geometry(
                    capture_14.o.geometry, realize_instances
                ),
                realize_instances,
            )
        switch_14 = g.Reroute(
            input=g.Reroute(input=reroute_40.o.output).o.output
        ).o.output.switch.boolean(group_3.o.boolean, boolean_math_1)
        reroute_87 = g.Reroute(input=radius_1.output)
        reroute_88 = g.Reroute(input=g.Reroute(input=reroute_84.o.output).o.output)
        reroute_89 = g.Reroute(input=g.Reroute(input=reroute_75.o.output).o.output)
        reroute_90 = g.Reroute(input=g.Reroute(input=reroute_76.o.output).o.output)
        with g.Frame("Custom Cap Merging"):
            separate_geometry = g.SeparateGeometry.instance(
                menu_switch_3, g.Compare.integer.equal(g.Index(), 0)
            )
            compare_2 = (
                g.Reroute(input=separate_geometry.o.selection)
                >> g.RealizeInstances()
                >> g.DomainSize()
            ).o.face_count > 0
            compare_3 = (
                g.Reroute(input=separate_geometry.o.inverted)
                >> g.RealizeInstances()
                >> g.DomainSize()
            ).o.face_count > 0
            reroute_91 = g.Reroute(input=reroute_89.o.output)
            reroute_92 = g.Reroute(input=reroute_90.o.output)
            switch_15 = reroute_12.o.output.switch.boolean(
                reroute_92.o.output | reroute_91,
                reroute_92.o.output & compare_2 | reroute_91.o.output & compare_3,
            )
            boolean_math_3 = switch_14 | switch_15
        reroute_93 = g.Reroute(input=g.Reroute(input=reroute_77.o.output).o.output)
        reroute_94 = g.Reroute(input=g.Reroute(input=reroute_85.o.output).o.output)
        reroute_95 = g.Reroute(
            input=g.Reroute(input=g.Reroute(input=selection.output).o.output).o.output
        )
        reroute_96 = g.Reroute(input=reroute_95.o.output)
        reroute_97 = g.Reroute(input=reroute_86.o.output)
        reroute_98 = g.Reroute(input=reroute_97.o.output)
        with g.Frame("Adjust UVs - U"):
            math_9 = (
                reroute_87.o.output
                * 4.0
                * reroute_45.o.output.switch.float(1.0, reroute_42.o.output / 6.2831855)
            )
            vector_math_7 = g.NamedAttribute.vector(
                uv_map_name
            ).o.attribute - reroute_97.o.output.switch.vector(
                (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)
            )
            vector_math_8 = vector_math_7 * g.CombineXYZ(x=math_9, y=1.0)
            switch_16 = reroute_98.o.output.switch.vector(
                vector_math_8,
                vector_math_8 + g.CombineXYZ(x=g.Reroute(input=reroute_93.o.output)),
            )
            reroute_99 = g.Reroute(input=switch_13)
            switch_17 = switch_9.switch.geometry(
                reroute_99,
                g.StoreNamedAttribute.corner.vector_2d(
                    reroute_99, reroute_95, uv_map_name, switch_16
                ),
            )
        reroute_100 = g.Reroute(
            input=g.Reroute(
                input=g.Reroute(input=set_mesh_normal_1.o.mesh).o.output
            ).o.output
        )
        reroute_101 = g.Reroute(input=reroute_98.o.output)
        reroute_102 = g.Reroute(input=g.Reroute(input=index_1.output).o.output)
        reroute_103 = g.Reroute(input=g.Reroute(input=transform.output).o.output)
        reroute_104 = g.Reroute(input=switch_17)
        merge_by_distance_1 = g.MergeByDistance(
            geometry=reroute_104,
            selection=g.Reroute(
                input=g.Reroute(input=boolean_math_3).o.output | capture_14.o.selection
            ),
            distance=switch_5,
        )
        reroute_105 = g.Reroute(
            input=caps.switch.boolean(true=caps_merge).switch.geometry(
                reroute_104, merge_by_distance_1
            )
        )
        with g.Frame("Material Transfer"):
            reroute_106 = g.Reroute(input=reroute_94.o.output)
            compare_4 = g.Compare.integer.equal(
                g.AttributeStatistic(
                    geometry=reroute_106, attribute=g.MaterialIndex(), domain="CURVE"
                ).o.max,
                0,
            )
            sample_index_2 = g.SampleIndex(
                geometry=reroute_106,
                value=g.MaterialIndex(),
                index=reroute_102.o.output / 2,
                data_type="INT",
                domain="CURVE",
            )
            reroute_107 = g.Reroute(input=reroute_105.o.output)
            switch_18 = compare_4.o.result.switch.geometry(
                reroute_107,
                g.SetMaterialIndex(geometry=reroute_107, material_index=sample_index_2),
            )
        with g.Frame("Extrapolate Radius"):
            reroute_108 = g.Reroute(input=reroute_68.o.output)
            reroute_109 = g.Reroute(input=reroute_108.o.output)
            reroute_110 = g.Reroute(input=reroute_96.o.output)
            switch_19 = caps.switch.boolean(true=caps_merge).switch.boolean(
                reroute_110,
                g.Compare.float.equal(g.BlurAttribute(value=reroute_110), 1.0, 0.001),
            )
            reroute_111 = g.Reroute(input=switch_19)
            switch_20 = g.Reroute(input=reroute_101.o.output).o.output.switch.float(
                g.Reroute(input=reroute_82.o.output).o.output
                / g.Reroute(input=reroute_80.o.output),
                g.Reroute(input=reroute_83.o.output).o.output
                / g.Reroute(input=reroute_81.o.output),
            )
            reroute_112 = g.Reroute(input=reroute_103.o.output)
            combine_transform = g.CombineTransform(
                translation=reroute_112.o.output.translation,
                rotation=reroute_112.o.output.rotation,
            )
            reroute_113 = g.Reroute(input=combine_transform.o.transform)
            invert_matrix = reroute_113.o.output.invert()
            transform_point = g.Position().o.position.transform(invert_matrix)
            transform_point_1 = reroute_47.o.output.transform(reroute_112).transform(
                invert_matrix
            )
            reroute_114 = g.Reroute(input=transform_point)
            switch_21 = reroute_108.o.output.switch.float(
                abs(transform_point.z),
                g.Reroute(input=reroute_39.o.output).o.output
                * reroute_112.o.output.scale.z,
            )
            math_10 = switch_21 * switch_20 + 1.0
            reroute_115 = g.Reroute(input=switch_18)
            reroute_116 = g.Reroute(input=math_10)
            combine_xyz_1 = g.CombineXYZ(
                x=reroute_116,
                y=reroute_116,
                z=g.Mix(
                    a_float=math_10, factor_float=0.5, b_float=1.0, clamp_factor=True
                ),
            )
            vector_math_9 = reroute_114.o.output * combine_xyz_1
            mix = g.Mix(
                a_vector=vector_math_9,
                b_vector=(reroute_114.o.output - transform_point_1) * combine_xyz_1
                + transform_point_1,
                factor_float=0.5,
                data_type="VECTOR",
                clamp_factor=True,
            )
            transform_point_2 = reroute_109.o.output.switch.vector(
                vector_math_9, mix.o.result_vector
            ).transform(reroute_113)
            switch_22 = caps_extrapolate_radius.switch.geometry(
                reroute_115,
                g.SetPosition(
                    geometry=reroute_115,
                    selection=reroute_111,
                    position=transform_point_2,
                ),
            )
        reroute_117 = g.Reroute(input=reroute_109.o.output)
        switch_23 = caps.switch.geometry(
            reroute_100,
            g.IndexSwitch.geometry(
                reroute_11, (None, reroute_100, switch_22, reroute_105)
            ),
        )
        with g.Frame("Adjust UVs - V"):
            reroute_118 = g.Reroute(
                input=1.0 * reroute_117.o.output.switch.float(6.2831855, reroute_46)
            )
            math_11 = reroute_118.o.output * reroute_88
            reroute_119 = g.Reroute(input=math_11)
            switch_24 = g.Switch(
                switch=g.EvaluateOnDomain(value=reroute_111),
                true=g.Reroute(input=math_10),
                false=1.0,
            )
            switch_25 = (
                (~reroute_17.o.output)
                .switch.boolean(true=caps_extrapolate_radius)
                .switch.float(reroute_119, math_11 * switch_24)
            )
            switch_26 = consider_curve_radius.switch.float(
                reroute_118, caps.switch.float(reroute_119, switch_25)
            )
            vector_math_10 = g.NamedAttribute.vector(
                uv_map_name
            ).o.attribute * g.CombineXYZ(y=switch_26, x=1.0, z=1.0)
            reroute_120 = g.Reroute(input=g.Reroute(input=switch_23).o.output)
            store_named_attribute_2 = g.StoreNamedAttribute.corner.vector_2d(
                reroute_120, name=uv_map_name, value=vector_math_10
            )
            switch_27 = uv_map.switch.boolean(true=reroute_79).switch.geometry(
                reroute_120, store_named_attribute_2
            )
        with g.Frame("Pass-Through"):
            with g.Frame("Scale is 0"):
                compare_5 = g.Compare.float.equal(
                    g.AttributeStatistic(geometry=curve, attribute=scale).o.max,
                    0.0,
                    0.0,
                )
                switch_28 = g.Warning.warning(
                    compare_5, "Scale is 0"
                ).o.show.switch.geometry(switch_27, g.Reroute(input=curve))
            with g.Frame("No Curves"):
                compare_6 = g.Compare.integer.equal(
                    g.DomainSize(geometry=curve, component="CURVE").o.spline_count, 0
                )
                (
                    g.Warning.warning(
                        compare_6, "No curve data in input"
                    ).o.show.switch.geometry(switch_28, g.Reroute(input=curve))
                    >> mesh
                )

        profile_mode.default_value = "Round"
        profile_input.default_value = "Object"
        resample_mode.default_value = "Evaluated"
        caps_type.default_value = "Flat"
        caps_input.default_value = "Object"
        uv_map_parameter_u.default_value = "Length"
        uv_map_parameter_v.default_value = "Factor"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Input": (-6900.0, -440.0),
            "Group Output": (21499.7, -80.0),
            "Curve to Mesh": (1796.7, -336.3),
            "Object Info": (-6660.0, -420.0),
            "Menu Switch": (-3980.0, -360.0),
            "Menu Switch.001": (2800.0, -520.0),
            "Group Input.001": (2620.0, -560.0),
            "Instance on Points": (2812.6, -173.5),
            "Axes to Rotation": (2325.8, -493.7),
            "Join Geometry": (99.1, -259.7),
            "Group Input.004": (570.0, -272.0),
            "Set Mesh Normal": (988.3, -55.6),
            "Boolean Math": (770.0, -252.0),
            "Reroute": (1459.7, -782.9),
            "Reroute.002": (3000.0, -620.0),
            "Group Input.005": (377.2, -90.0),
            "Switch.001": (1123.9, -165.1),
            "Realize Instances": (565.5, -300.4),
            "Curve Circle": (-4220.0, -400.0),
            "Group Input.010": (30.0, -272.0),
            "Is Edge Smooth": (202.4, -82.7),
            "Boolean Math.003": (382.4, -82.7),
            "Boolean Math.004": (567.5, -121.7),
            "Boolean Math.005": (390.0, -192.0),
            "Switch.004": (210.0, -192.0),
            "Frame.003": (4610.0, -635.0),
            "Reroute.007": (50.0, -252.0),
            "Capture Attribute.001": (1208.2, -216.3),
            "Reroute.008": (46.4, -454.9),
            "Capture Attribute.005": (1028.2, -436.3),
            "Combine XYZ.001": (2191.0, -588.9),
            "Store Named Attribute": (2392.0, -462.9),
            "Group Input.011": (2088.2, -356.3),
            "Half Sphere": (610.0, -105.0),
            "Geometry to Instance": (850.0, -125.0),
            "Switch.003": (1890.0, -405.0),
            "Endpoint Selection.002": (1651.2, -472.9),
            "Group": (1528.5, -636.3),
            "Group.001": (1536.7, -493.3),
            "Spline Parameter.005": (320.0, -205.0),
            "Spline Parameter.006": (210.1, -597.3),
            "Group Input.003": (107.8, -232.8),
            "Group Input.007": (30.1, -597.3),
            "Index Switch": (1530.0, -245.0),
            "Geometry to Instance.001": (850.0, -605.0),
            "Object Info.001": (650.0, -565.0),
            "Group Input.009": (430.0, -645.0),
            "Object Info.002": (650.0, -685.0),
            "Reroute.012": (3000.0, -560.0),
            "Reroute.013": (452.5, -974.2),
            "Frame": (7896.0, -263.0),
            "Index Switch.001": (16708.5, -180.0),
            "Reroute.001": (12817.5, -282.3),
            "Reroute.003": (13180.0, -196.2),
            "Frame.001": (6350.0, 432.0),
            "Reroute.005": (5443.8, -566.6),
            "Frame.002": (2380.0, 765.0),
            "Sample Index": (540.1, -188.9),
            "Material Index": (270.1, -188.9),
            "Set Material Index": (742.7, -155.6),
            "Index": (30.3, -344.5),
            "Integer Math": (380.1, -288.9),
            "Capture Attribute": (313.8, -253.5),
            "Compare": (458.6, -408.9),
            "Attribute Statistic": (238.6, -448.9),
            "Material Index.001": (30.1, -508.9),
            "Switch": (942.7, -35.6),
            "Reroute.006": (662.7, -115.6),
            "Switch.002": (754.0, -170.1),
            "Boolean Math.001": (1930.0, -36.0),
            "Switch.005": (236.8, -106.8),
            "Geometry to Instance.002": (850.0, -805.0),
            "Group Input.015": (650.0, -825.0),
            "Reroute.004": (2488.9, -972.9),
            "Menu Switch.002": (1090.0, -605.0),
            "Group Input.016": (850.0, -525.0),
            "Capture Attribute.002": (648.2, -56.3),
            "Switch.006": (1976.7, -456.3),
            "Math.002": (1796.7, -556.3),
            "Spline Length": (320.0, -145.0),
            "Resample Curve": (1261.6, -576.1),
            "Reroute.010": (178.6, -448.9),
            "Reroute.015": (2660.0, 940.0),
            "Reroute.016": (5587.6, 612.1),
            "Reverse Curve.001": (-5720.0, -520.0),
            "Accumulate Field": (830.0, -76.0),
            "Separate XYZ": (650.0, -76.0),
            "Vector Math": (450.0, -56.0),
            "Evaluate on Domain": (650.0, -176.0),
            "Index.001": (450.0, -176.0),
            "Curve Tangent.001": (30.0, -176.0),
            "Compare.001": (1030.0, -76.0),
            "Frame.006": (-7670.0, -684.0),
            "Capture Attribute.004": (1885.9, -56.2),
            "Endpoint Selection.003": (1677.7, -82.9),
            "Endpoint Selection.004": (1675.1, -129.4),
            "Boolean Math.002": (2086.3, -118.8),
            "Named Attribute": (583.1, -277.0),
            "Reroute.014": (12551.5, -355.7),
            "Store Named Attribute.001": (1654.5, -194.0),
            "Group Input.002": (383.1, -217.0),
            "Vector Math.001": (1178.1, -450.7),
            "Combine XYZ": (899.8, -549.6),
            "Group Input.012": (737.1, -35.9),
            "Attribute Statistic.001": (927.0, -64.7),
            "Radius.001": (30.1, -259.8),
            "Endpoint Selection": (477.1, -75.9),
            "Math.005": (1106.6, -55.9),
            "Math.006": (1294.5, -97.0),
            "Group Input.018": (922.8, -215.7),
            "Integer Math.001": (1108.3, -188.4),
            "Frame.011": (9222.0, -1399.0),
            "Math.007": (1718.0, -101.0),
            "Math.004": (397.1, -195.9),
            "Group Input.019": (210.9, -329.3),
            "Capture Attribute.006": (5385.7, 670.2),
            "Switch.008": (1376.6, -332.2),
            "Reroute.020": (9350.5, -1254.0),
            "Switch.009": (1858.9, -36.1),
            "Reroute.021": (1551.5, -137.0),
            "Endpoint Selection.005": (5182.4, 596.9),
            "Reroute.022": (9588.5, 80.0),
            "Reroute.023": (35.0, -626.4),
            "Combine XYZ.002": (814.7, -423.4),
            "Switch.010": (591.5, -377.0),
            "Vector Math.002": (813.6, -294.0),
            "Vector Math.003": (1002.7, -374.8),
            "Math.003": (411.9, -462.9),
            "Resample Curve.001": (-6180.0, -480.0),
            "Menu Switch.003": (-6360.0, -440.0),
            "Switch.011": (1538.0, -101.0),
            "Reroute.025": (390.0, -90.0),
            "Field at Index.001": (439.4, -35.8),
            "Vector Math.008": (620.2, -35.8),
            "Interpolate Domain.002": (801.0, -35.8),
            "Vector Math.007": (980.8, -40.4),
            "Index.002": (30.0, -150.0),
            "Switch.015": (212.9, -163.1),
            "Offset Point in Curve.001": (30.0, -210.0),
            "Position.002": (210.0, -50.0),
            "Frame.010": (8810.0, -2110.0),
            "Attribute Statistic.002": (30.1, -55.9),
            "Math.009": (230.1, -35.9),
            "Frame.012": (1057.0, -456.0),
            "Frame.013": (30.0, -36.0),
            "Switch.012": (1290.0, -325.0),
            "Reroute.026": (35.0, -76.2),
            "Curve to Mesh.001": (2299.0, -36.0),
            "Curve Line": (209.7, -593.7),
            "Capture Attribute.007": (632.2, -698.5),
            "Spline Parameter": (429.7, -813.7),
            "Set Curve Normal": (115.0, -56.2),
            "Resample Curve.002": (429.7, -673.7),
            "Capture Attribute.008": (955.0, -56.2),
            "Position.001": (755.0, -136.2),
            "Set Position": (3299.0, -176.0),
            "Math.010": (390.0, -36.0),
            "Position.003": (1479.0, -176.0),
            "Vector Math.004": (2295.7, -233.1),
            "Combine XYZ.004": (2099.0, -276.0),
            "Math.011": (210.0, -36.0),
            "Math.012": (30.0, -36.0),
            "Vector Math.005": (1659.0, -156.0),
            "Vector Math.006": (2779.0, -256.0),
            "Vector Math.009": (3099.0, -316.0),
            "Combine XYZ.005": (2919.0, -436.0),
            "Reroute.027": (1279.0, -576.0),
            "Math.013": (210.0, -36.0),
            "Math.014": (30.0, -36.0),
            "Frame.014": (869.0, -500.0),
            "Frame.015": (1509.0, -280.0),
            "Separate XYZ.001": (1959.0, -496.0),
            "Geometry to Instance.003": (3739.4, -193.8),
            "Set Position.001": (3272.1, -512.1),
            "Reroute.030": (3139.6, -113.6),
            "Curve to Mesh.002": (2366.5, -778.6),
            "Vector Math.010": (3103.7, -579.4),
            "Math.015": (2239.0, -656.0),
            "Combine XYZ.006": (2919.0, -636.0),
            "Spline Length.001": (749.8, -205.0),
            "Math.016": (1219.0, -56.0),
            "Reroute.028": (2179.0, -576.0),
            "Reroute.031": (2639.0, -576.0),
            "Math.017": (1679.0, -656.0),
            "Switch.013": (6060.0, -1840.0),
            "Compare.002": (250.0, -56.0),
            "Merge by Distance.001": (4846.2, -401.4),
            "Compare.003": (4558.0, -1009.9),
            "Frame.016": (-599.0, -1304.0),
            "Group Input.017": (29.7, -873.7),
            "Transform Geometry": (2029.4, -861.3),
            "Reroute.036": (1399.0, -1196.0),
            "Reroute.037": (5019.0, -1196.0),
            "Math.018": (1968.2, -636.3),
            "Reverse Curve": (2059.0, -76.0),
            "Set Mesh Normal.001": (4043.7, -273.3),
            "Boolean Math.006": (3842.1, -354.9),
            "Reroute.039": (772.3, -390.0),
            "Group Input.021": (3659.6, -354.4),
            "Store Named Attribute.002": (4443.7, -352.9),
            "Group Input.022": (4234.0, -417.1),
            "Group.002": (30.1, -240.0),
            "Combine XYZ.007": (446.3, -172.6),
            "Capture Attribute.009": (589.8, -65.0),
            "Spline Parameter.001": (49.8, -285.0),
            "Math.019": (270.1, -235.5),
            "Reroute.041": (4398.1, -1196.0),
            "Capture Attribute.010": (3493.5, -163.9),
            "Switch.014": (1036.1, -43.1),
            "Vector Math.011": (835.8, -220.0),
            "Reroute.042": (791.9, -200.1),
            "Frame.017": (3266.0, -645.0),
            "Math.020": (599.1, -487.0),
            "Switch.016": (403.1, -597.0),
            "Reroute.043": (9227.8, -1371.6),
            "Vector Math.012": (839.4, -35.8),
            "Vector Math.013": (626.4, -154.7),
            "Capture Attribute.011": (-5940.0, -500.0),
            "Evaluate at Index": (418.6, -719.0),
            "Offset Point in Curve": (215.1, -799.3),
            "Switch.017": (605.0, -636.6),
            "Evaluate at Index.001": (229.8, -345.0),
            "Offset Point in Curve.002": (49.8, -365.0),
            "Switch.018": (415.0, -236.2),
            "Reroute.045": (-5240.0, -620.0),
            "Boolean Math.007": (-6240.0, -800.0),
            "Is Spline Cyclic": (-6440.0, -880.0),
            "Switch.019": (814.3, -530.6),
            "Reroute.046": (1414.5, -463.5),
            "Reroute.047": (-3640.0, -460.0),
            "Reroute.048": (5491.6, -490.8),
            "Store Named Attribute.003": (1980.5, -266.0),
            "Switch.020": (2170.5, -159.7),
            "Reroute.044": (897.5, -944.3),
            "Reroute.050": (10494.4, 130.0),
            "Named Attribute.001": (1546.7, -422.0),
            "Group Input.023": (1346.7, -342.0),
            "Reroute.051": (1826.8, -220.1),
            "Frame.019": (9376.9, -223.0),
            "Frame.020": (17064.5, 22.0),
            "Reroute.052": (11402.4, 580.5),
            "Reroute.053": (8764.1, -2538.6),
            "Reroute.054": (11946.6, -2537.8),
            "Reroute.055": (6371.3, 695.1),
            "Reroute.056": (11440.0, 668.8),
            "Vector Math.014": (1764.2, -425.6),
            "Combine XYZ.008": (1580.6, -539.1),
            "Switch.021": (86.7, -765.1),
            "Math.001": (286.8, -636.1),
            "Switch.007": (1379.7, -547.4),
            "Math.021": (546.8, -831.3),
            "Capture Attribute.012": (2460.0, 1000.0),
            "Radius.003": (1401.0, 618.0),
            "Reroute.057": (2660.0, 900.0),
            "Reroute.060": (11308.5, 918.2),
            "Group Input.025": (1175.5, -562.0),
            "Math.022": (2747.2, -472.5),
            "Math.023": (2392.9, -485.7),
            "Math.024": (2573.8, -502.2),
            "Math.025": (1959.0, -576.0),
            "Math.026": (2739.0, -696.0),
            "Math.027": (2399.0, -696.0),
            "Math.028": (2579.0, -716.0),
            "Integer Math.002": (209.7, -873.7),
            "Math.029": (163.1, -677.0),
            "Boolean Math.008": (2612.4, -144.9),
            "Is Spline Cyclic.001": (2248.5, -189.2),
            "Boolean Math.009": (2409.6, -189.7),
            "Reroute.059": (2499.0, -576.0),
            "Reroute.061": (2339.0, -576.0),
            "Math.030": (1679.0, -516.0),
            "Instance Transform": (29.6, -409.4),
            "Frame.009": (12066.0, -454.0),
            "Sample Curve": (838.6, -55.9),
            "Capture Attribute.013": (1469.5, -425.0),
            "Sample Index.001": (840.7, -266.2),
            "Interpolate Domain": (521.7, -615.5),
            "Points of Curve": (340.9, -655.7),
            "Sample Index.002": (843.4, -590.2),
            "Interpolate Domain.001": (521.7, -739.3),
            "Points of Curve.001": (340.9, -779.5),
            "Reroute.062": (407.2, -522.9),
            "Index.003": (147.6, -372.6),
            "Interpolate Domain.003": (328.7, -355.3),
            "Sample Curve.001": (842.8, -753.5),
            "Spline Length.002": (344.2, -892.9),
            "Math.031": (560.1, -857.9),
            "Value": (247.9, -73.0),
            "Math.032": (1026.2, -61.9),
            "Math.033": (1064.5, -625.1),
            "Math.034": (1216.4, -133.0),
            "Math.035": (1267.5, -642.3),
            "Reroute.063": (1736.4, -533.0),
            "Reroute.064": (1736.4, -553.0),
            "Reroute.065": (1736.4, -593.0),
            "Reroute.066": (1736.4, -613.0),
            "Reroute.068": (159.2, -41.0),
            "Reroute.069": (140.5, -51.9),
            "Reroute.070": (117.4, -82.8),
            "Reroute.071": (109.8, -100.7),
            "Reroute.067": (11408.5, 1180.0),
            "Reroute.072": (11408.5, 1100.0),
            "Reroute.073": (11408.5, 1120.0),
            "Reroute.074": (11408.5, 1160.0),
            "Set Position.002": (3035.0, -219.4),
            "Transform Point": (665.0, -527.2),
            "Reroute.075": (8717.1, -2578.9),
            "Position.004": (490.1, -498.5),
            "Invert Matrix": (507.8, -629.3),
            "Transform Point.001": (2795.0, -519.4),
            "Reroute.077": (445.6, -740.1),
            "Reroute.078": (1154.0, -201.8),
            "Vector Math.015": (2075.0, -479.4),
            "Combine XYZ.009": (1843.1, -638.4),
            "Separate XYZ.002": (822.1, -582.0),
            "Math.036": (1335.0, -699.4),
            "Math.037": (1495.0, -679.4),
            "Switch.022": (1141.9, -812.3),
            "Switch.023": (1648.4, -114.7),
            "Blur Attribute": (1271.4, -242.3),
            "Compare.004": (1448.2, -244.7),
            "Switch.024": (3235.0, -79.4),
            "Reroute.079": (2915.0, -179.4),
            "Group Input.027": (2946.5, -79.4),
            "Separate Transform": (79.9, -774.8),
            "Combine Transform": (259.6, -717.5),
            "Math.040": (875.0, -879.4),
            "Math.041": (875.0, -919.4),
            "Frame.021": (13233.5, -380.6),
            "Reroute.076": (12705.8, -2583.8),
            "Reroute.084": (697.5, -752.2),
            "Reroute.086": (12780.8, -2658.7),
            "Math.038": (975.0, -739.4),
            "Separate XYZ.003": (790.7, -753.5),
            "Switch.025": (1154.7, -571.3),
            "Reroute.087": (246.5, -1339.4),
            "Merge by Distance.002": (11825.2, -400.0),
            "Switch.026": (12018.9, -272.7),
            "Group Input.028": (11628.7, -236.9),
            "Reroute.081": (35.0, -1104.4),
            "Math.039": (755.4, -911.0),
            "Mix": (1660.6, -744.3),
            "Switch.027": (976.8, -830.7),
            "Group Input.029": (541.3, -761.2),
            "Switch.028": (543.8, -965.8),
            "Reroute.091": (143.8, -210.1),
            "Evaluate on Domain.001": (351.3, -939.2),
            "Switch.029": (1884.4, -35.5),
            "Group Input.030": (1665.7, -52.0),
            "Switch.030": (10920.0, -20.0),
            "Group Input.031": (10720.0, -20.0),
            "Switch.032": (2596.7, -416.3),
            "Group Input.033": (4433.0, -279.8),
            "Switch.033": (4641.6, -332.4),
            "Group Input.034": (30.0, -85.0),
            "Boolean Math.010": (450.0, -36.0),
            "Frame.004": (485.0, 1774.0),
            "Reroute.098": (35.0, -1159.4),
            "Transform Point.003": (974.9, -1101.0),
            "Transform Point.004": (1154.0, -1127.4),
            "Vector Math.017": (1895.0, -459.4),
            "Vector Math.018": (2235.0, -459.4),
            "Mix.001": (2435.0, -479.4),
            "Vector Math.019": (2066.5, -626.7),
            "Reroute.093": (1795.0, -519.4),
            "Switch.031": (2615.0, -499.4),
            "Math.045": (398.5, -35.8),
            "Group Input.038": (30.0, -168.0),
            "Math.046": (581.3, -62.4),
            "Math.047": (222.0, -173.2),
            "Math.048": (401.0, -171.2),
            "Attribute Statistic.003": (208.8, -35.8),
            "Reroute.095": (389.9, -78.2),
            "Field at Index.002": (431.9, -52.6),
            "Vector Math.021": (612.7, -52.6),
            "Interpolate Domain.004": (796.2, -48.9),
            "Vector Math.022": (972.6, -36.4),
            "Index.004": (29.9, -118.2),
            "Switch.037": (209.9, -98.2),
            "Offset Point in Curve.003": (29.9, -178.2),
            "Position.005": (209.9, -38.2),
            "Frame.005": (-4662.0, 280.0),
            "Switch.034": (-2820.0, 340.0),
            "Group Input.035": (-2440.0, 1340.0),
            "Menu Switch.004": (-2260.0, 1360.0),
            "Index Switch.002": (1463.5, -179.9),
            "Set Spline Resolution.001": (1027.5, -537.9),
            "Resample Curve.003": (1016.9, -59.0),
            "Resample Curve.004": (1261.6, -419.6),
            "Set Spline Resolution.002": (1027.5, -417.9),
            "Switch.035": (1689.4, -82.5),
            "Group Input.040": (1466.1, -56.6),
            "Resample Curve.005": (1260.3, -275.7),
            "Set Spline Resolution.003": (1027.5, -297.9),
            "Math.043": (-2416.5, 340.0),
            "Group Input.042": (-2620.0, 200.0),
            "Reroute.094": (16600.0, -180.0),
            "Switch.036": (16888.5, -120.0),
            "Group Input.043": (16713.7, -95.1),
            "Switch.038": (3300.0, -540.0),
            "Group Input.044": (3100.0, -620.0),
            "Switch.039": (773.4, -77.4),
            "Group Input.045": (568.7, -50.9),
            "Switch.040": (3460.0, -620.0),
            "Reroute.090": (3000.0, -640.0),
            "Switch.041": (11825.7, -198.8),
            "Group Input.047": (11627.4, -171.8),
            "Group Input.048": (720.7, -41.3),
            "Switch.042": (918.3, -35.7),
            "Group Input.050": (1222.6, -77.4),
            "Switch.043": (1420.3, -71.8),
            "Group Input.052": (981.6, -660.0),
            "Switch.044": (1184.1, -655.3),
            "Reroute.097": (877.4, -855.2),
            "Spline Resolution": (405.0, -174.0),
            "Compare.005": (646.5, -161.0),
            "Frame.007": (-1424.0, 1297.9),
            "Frame.008": (-3770.0, 608.0),
            "Frame.018": (-3250.0, 208.0),
            "Spline Length.004": (31.5, -81.2),
            "Integer Math.004": (208.0, -81.7),
            "Integer Math.005": (410.6, -56.6),
            "Frame.022": (30.0, -325.1),
            "Reroute.100": (592.1, -108.9),
            "Reroute.101": (363.5, -41.0),
            "Switch.045": (778.5, -156.0),
            "Compare.006": (410.0, -56.0),
            "Warning": (590.0, -56.0),
            "Group Input.026": (30.0, -96.0),
            "Frame.023": (30.0, -36.0),
            "Index Switch.003": (-1600.1, 977.7),
            "Group Input.053": (30.0, -116.0),
            "Group Input.054": (1024.0, -657.9),
            "Spline Length.003": (30.0, -216.0),
            "Math.044": (210.0, -156.0),
            "Float to Integer": (370.0, -156.0),
            "Reroute.102": (-1960.0, 1320.0),
            "Reroute.103": (-233.6, 1337.1),
            "Frame.024": (-5469.8, -715.0),
            "Frame.025": (-2218.0, 996.0),
            "Spline Length.005": (30.0, -36.0),
            "Math.050": (213.5, -36.0),
            "Float to Integer.001": (373.5, -36.0),
            "Switch.046": (725.4, -670.0),
            "Boolean Math.011": (537.2, -670.4),
            "Evaluate at Index.002": (250.0, -56.0),
            "Offset Point in Curve.004": (30.0, -36.0),
            "Reroute.104": (1019.3, -41.0),
            "Reroute.105": (1436.0, -47.1),
            "Math.051": (975.0, -639.4),
            "Capture Attribute.014": (3491.1, -402.0),
            "Boolean Math.012": (30.0, -36.0),
            "Frame.026": (4610.0, -2064.0),
            "Reroute.106": (804.0, -117.9),
            "Domain Size": (222.2, -56.0),
            "Compare.007": (402.2, -56.0),
            "Separate Components": (557.2, -70.0),
            "Group Input.055": (30.4, -77.2),
            "Switch.047": (830.7, -116.0),
            "Frame.027": (989.0, -36.0),
            "Frame.028": (19420.0, 92.0),
            "Warning.001": (602.2, -56.0),
            "Reroute.107": (884.3, -133.0),
            "Spline Length.006": (842.9, -187.0),
            "Compare.008": (1015.3, -170.2),
            "Reroute.108": (35.0, -41.3),
            "Reroute.109": (885.0, -170.5),
            "Reroute.110": (882.5, -107.7),
            "Reroute.111": (1191.6, -263.1),
            "Duplicate Elements": (2351.3, -305.8),
            "Spline Length.008": (30.3, -88.3),
            "Compare.010": (208.8, -61.9),
            "Integer Math.003": (2622.6, -302.7),
            "Switch.048": (385.6, -36.2),
            "Frame.029": (1577.0, -740.0),
            "Switch.049": (1581.8, 732.9),
            "Named Attribute.002": (1401.0, 738.0),
            "Reroute.112": (3339.0, -1196.0),
            "Reroute.040": (10503.3, 80.0),
            "Reroute.114": (10253.3, -1250.5),
            "Reroute.113": (1814.8, -708.0),
            "Reroute.115": (302.2, -216.0),
            "Reroute.116": (481.2, -256.0),
            "Reroute.117": (35.9, -101.3),
            "Reroute.096": (62.4, -389.9),
            "Reroute.118": (5179.6, 918.2),
            "Reroute.119": (300.0, -840.0),
            "Reroute.120": (300.0, -880.0),
            "Reroute.121": (300.0, -860.0),
            "Reroute.122": (840.0, -840.0),
            "Reroute.123": (840.0, -860.0),
            "Reroute.124": (1841.7, -845.4),
            "Reroute.125": (1827.4, -871.9),
            "Reroute.126": (4220.0, -880.0),
            "Reroute.127": (4200.0, -900.0),
            "Reroute.128": (144.3, -1110.8),
            "Reroute.029": (9100.0, -962.8),
            "Reroute.131": (4180.0, -920.0),
            "Reroute.049": (9234.6, -1304.8),
            "Reroute.132": (10440.0, -1315.6),
            "Reroute.133": (11864.4, -1315.6),
            "Reroute.134": (1886.5, -1339.4),
            "Reroute.135": (1597.0, -634.9),
            "Reroute.033": (1700.7, -836.0),
            "Reroute.038": (1248.8, -2608.6),
            "Reroute.034": (892.2, -916.3),
            "Reroute.035": (8964.8, 521.2),
            "Reroute.136": (9020.2, 587.6),
            "Reroute.137": (8953.8, 508.0),
            "Reroute.138": (10028.6, -132.1),
            "Reroute.139": (10028.6, -157.8),
            "Reroute.017": (2316.7, -456.3),
            "Reroute.140": (807.9, -213.0),
            "Reroute.141": (756.3, -259.2),
            "Reroute.142": (761.7, -698.5),
            "Reroute.143": (748.3, -164.3),
            "Reroute.144": (771.4, -673.0),
            "Reroute.145": (1224.0, -517.9),
            "Reroute.011": (3860.0, -620.0),
            "Reroute.148": (3540.0, -580.0),
            "Reroute.149": (6440.0, -600.0),
            "Reroute.129": (7580.0, -600.0),
            "Reroute.152": (7580.0, -520.0),
            "Reroute.153": (7580.0, -560.0),
            "Reroute.009": (8160.0, -1340.0),
            "Reroute.151": (9229.7, -1335.6),
            "Reroute.154": (11849.1, -1333.4),
            "Reroute.155": (13310.5, -1857.0),
            "Reroute.156": (16552.0, -1846.2),
            "Reroute.157": (16298.8, 918.2),
            "Reroute.082": (42.9, -558.6),
            "Reroute.158": (8140.0, -962.8),
            "Reroute.160": (9040.0, -1170.0),
            "Reroute.161": (11168.5, -1164.7),
            "Reroute.083": (11765.2, -360.0),
            "Reroute.164": (1747.4, -176.3),
            "Reroute.165": (2676.7, -216.3),
            "Reroute.166": (13334.5, -1902.3),
            "Reroute.167": (13168.5, -1239.4),
            "Reroute.168": (11828.5, -1361.9),
            "Reroute.169": (16191.6, -1894.0),
            "Reroute.058": (18224.7, 140.0),
            "Reroute.085": (1300.0, -360.0),
            "Reroute.163": (301.7, -628.6),
            "Reroute.170": (4760.0, -1760.0),
            "Reroute.171": (4740.0, -1780.0),
            "Reroute.172": (8860.0, -1780.0),
            "Reroute.173": (6120.0, -2720.0),
            "Reroute.174": (4780.0, -1740.0),
            "Reroute.175": (8860.0, -1740.0),
            "Reroute.176": (5520.0, -1760.0),
            "Reroute.177": (12879.1, -2716.9),
            "Reroute.178": (2103.0, -80.2),
            "Reroute.179": (2935.5, -93.7),
            "Reroute.180": (2713.3, -943.1),
            "Reroute.181": (8138.0, -829.7),
            "Reroute.182": (7592.9, -481.2),
            "Reroute.183": (2915.0, -319.4),
            "Reroute.184": (16528.5, -260.0),
            "Reroute.185": (11774.4, 297.5),
            "Reroute.186": (13871.1, 78.9),
            "Reroute.080": (3898.9, -555.0),
            "Reroute.088": (3897.6, -571.8),
            "Reroute.089": (5009.3, -557.2),
            "Reroute.187": (5010.6, -574.1),
            "Reroute.188": (16540.0, -1720.0),
            "Reroute.189": (3360.0, -520.0),
            "Reroute.150": (5800.3, -526.0),
            "Reroute.099": (2707.1, -914.4),
            "Reroute.190": (1525.0, -191.5),
            "Reroute.146": (1003.7, -847.6),
            "Reroute.147": (1030.5, -447.5),
            "Switch.050": (430.0, -45.0),
            "Named Attribute.003": (30.1, -179.8),
            "Switch.051": (210.1, -179.8),
            "Attribute Statistic.004": (230.0, -56.0),
            "Reroute.191": (584.8, -247.8),
            "Radius.002": (29.8, -224.2),
            "Group Input.032": (189.8, -284.2),
            "Named Attribute.004": (29.8, -144.2),
            "Switch.052": (209.8, -144.2),
            "Math.042": (389.8, -224.2),
            "Reroute.197": (461.4, -684.3),
            "Math.008": (1784.4, 659.5),
            "Group Input.036": (1587.6, 581.7),
            "Math.053": (30.4, -126.8),
            "Field Average": (576.0, -175.0),
            "Index.006": (210.4, -296.4),
            "Evaluate on Domain.004": (390.4, -276.4),
            "Radius.004": (30.4, -116.4),
            "Math.049": (390.4, -116.4),
            "Group Input.020": (210.4, -196.4),
            "Named Attribute.005": (30.4, -36.4),
            "Switch.053": (210.4, -36.4),
            "Group Input.006": (-4440.0, -320.0),
            "Frame.030": (-4556.0, 715.0),
            "Compare.009": (577.1, -195.9),
            "Boolean Math.013": (737.1, -95.9),
            "Compare.011": (1898.0, -101.0),
            "Switch.054": (2075.7, -122.8),
            "Compare.012": (871.3, -505.5),
            "Reroute.018": (818.4, -614.8),
            "Math": (-2620.0, 340.0),
            "Math.052": (1958.9, 634.9),
            "Capture Attribute.003": (1407.2, -60.8),
            "Index.005": (1221.0, -101.8),
            "Sample Curve.002": (2125.8, -513.7),
            "Switch.055": (1890.0, -545.0),
            "Reroute.019": (2270.0, -285.0),
            "Reroute.024": (2530.0, -285.0),
            "Reroute.159": (1650.0, -50.5),
            "Reroute.192": (1830.0, -50.5),
            "Custom Cap Merging": (6350.0, -1804.0),
            "Reroute.032": (590.0, -356.0),
            "Reroute.193": (590.0, -396.0),
            "Index.007": (30.0, -456.0),
            "Compare.013": (210.0, -436.0),
            "Separate Geometry": (410.0, -336.0),
            "Realize Instances.001": (670.0, -296.0),
            "Domain Size.001": (850.0, -296.0),
            "Compare.014": (1030.0, -296.0),
            "Boolean Math.014": (1290.0, -256.0),
            "Boolean Math.015": (1510.0, -276.0),
            "Switch.056": (1710.0, -116.0),
            "Realize Instances.002": (670.0, -416.0),
            "Domain Size.002": (850.0, -416.0),
            "Compare.016": (1030.0, -416.0),
            "Boolean Math.016": (1290.0, -356.0),
            "Endpoint Selection.006": (1028.2, -336.3),
            "Endpoint Selection.007": (1028.2, -376.3),
            "Boolean Math.017": (1290.0, -156.0),
            "Reroute.194": (1150.0, -216.0),
            "Reroute.198": (1150.0, -256.0),
            "Reroute.092": (1440.0, -365.0),
            "Reroute.162": (1460.0, -345.0),
            "Reroute.199": (4900.0, -1660.0),
            "Reroute.200": (4880.0, -1680.0),
            "Reroute.201": (6860.0, -1680.0),
            "Reroute.202": (6860.0, -1660.0),
            "Switch.057": (3620.0, -700.0),
            "Reroute.203": (3000.0, -660.0),
            "Reroute.204": (3801.4, -731.0),
            "Reroute.205": (4800.0, -1720.0),
            "Reroute.206": (4240.0, -860.0),
            "Reroute.207": (7400.0, -1720.0),
            "Reroute.195": (4056.2, -482.5),
            "Reroute.130": (4860.0, -1700.0),
            "Reroute.196": (5880.0, -1700.0),
            "Boolean Math.018": (9212.7, -1111.1),
            "Switch.058": (2070.1, -320.1),
            "Group Input.008": (1609.6, -313.1),
        }


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
