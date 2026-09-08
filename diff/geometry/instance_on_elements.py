# Node-group asset 'Instance on Elements' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .face_corner_angle import FaceCornerAngle


class InstanceOnElements(CustomGeometryGroup):
    _name = "Instance on Elements"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        instance_on = tree.inputs.menu(
            "Instance On",
            description="Geometry element type to instance on",
            optional_label=True,
        )
        mask = tree.inputs.float(
            "Mask",
            1.0,
            description="Specify which elements to use for instancing. (Floating point values result in a random selection.)",
            min_value=0.0,
            max_value=1.0,
            structure_type="FIELD",
            subtype="FACTOR",
        )
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
        collection = tree.inputs.collection(
            "Collection", description="Instance geometry collection"
        )
        object = tree.inputs.object("Object", description="Instance geometry object")
        instance = tree.inputs.geometry(
            "Instance", description="Instance geometry input"
        )
        realize_instances = tree.inputs.boolean(
            "Realize Instances",
            False,
            description="Turn the output into a single geometry rather than instances (required by many other modifiers)",
        )
        keep_surface = tree.inputs.boolean(
            "Keep Surface",
            True,
            description="Keep the original input geometry and join it with the instance geometry",
        )
        seed = tree.inputs.integer(
            "Seed",
            0,
            description="Base value to control random variation in a reproducible way",
            structure_type="SINGLE",
        )
        with tree.inputs.panel("Pick Instance", default_closed=True):
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
            instance_index = tree.inputs.menu(
                "Instance Index",
                description="Method how the child instance is chosen per element",
                optional_label=True,
                structure_type="SINGLE",
            )
            instance_index_1 = tree.inputs.integer(
                "Instance Index",
                0,
                description="Which child instance to pick per element by index",
                structure_type="FIELD",
            )
        with tree.inputs.panel("Transform", default_closed=True):
            surface_offset = tree.inputs.float(
                "Surface Offset",
                0.0,
                description="Distance to offset each instance along the normal of the input geometry",
                min_value=-10000.0,
                max_value=10000.0,
                subtype="DISTANCE",
            )
            align_rotation = tree.inputs.boolean(
                "Align Rotation",
                True,
                description="Rotate instances based on the shape of the input geometry",
                structure_type="FIELD",
            )
            scale = tree.inputs.vector(
                "Scale",
                (1.0, 1.0, 1.0),
                description="Scale the instances on each local axis",
                structure_type="FIELD",
                subtype="XYZ",
            )
        scale_by_face_area = tree.inputs.boolean(
            "Scale by Face Area",
            False,
            description="Scale the instances based on the face area of the input geometry",
            structure_type="SINGLE",
            is_panel_toggle=True,
        )
        scale_by_face_area_multiplier = tree.inputs.float(
            "Scale by Face Area Multiplier",
            1.0,
            description="Multiply the instance scale with a factor to calibrate the considered face area",
            min_value=-10000.0,
            max_value=10000.0,
            structure_type="FIELD",
        )
        corner_offset_method = tree.inputs.menu(
            "Corner Offset Method",
            description="Method to define the direction of the offset along the corner",
            expanded=True,
            optional_label=True,
        )
        corner_offset_factor = tree.inputs.float(
            "Corner Offset Factor",
            0.1,
            description="Move the instances towards the face center",
            min_value=0.0,
            max_value=1.0,
            structure_type="FIELD",
            subtype="FACTOR",
        )
        corner_offset_distance = tree.inputs.float(
            "Corner Offset Distance",
            0.1,
            description="Distance to offset the instances from the face corner",
            min_value=0.0,
            max_value=10000.0,
            structure_type="FIELD",
            subtype="DISTANCE",
        )
        even_edge_distance = tree.inputs.boolean(
            "Even Edge Distance",
            True,
            description="Adjust the offset distance to keep an even perpendicular distance to edges",
            structure_type="FIELD",
        )
        geometry_1 = tree.outputs.geometry("Geometry")

        with g.Frame("Face Tangent Vector"):
            position = g.Position()
            vector_math = position.o.position.corner.at(
                g.CornersOfFace(sort_index=1)
            ) - position.o.position.corner.at(g.CornersOfFace())
        with g.Frame("Face Corner Offset"):
            with g.Frame("Face Center Offset"):
                position_1 = g.Position()
                mix = g.Mix(
                    factor_float=corner_offset_factor,
                    a_vector=position_1,
                    b_vector=position_1.o.position.face.evaluate(),
                    data_type="VECTOR",
                    clamp_factor=True,
                )
            with g.Frame("Corner Bisector Offset"):
                group = FaceCornerAngle()
                switch = even_edge_distance.switch.float(
                    corner_offset_distance,
                    corner_offset_distance / (group.o.corner_angle * 0.5).sin(),
                )
                vector_math_1 = g.Position().o.position + group.o.bisector * switch
            menu_switch = g.MenuSwitch.geometry(
                corner_offset_method, {"Face Center": None, "Corner Center": None}
            )
            switch_1 = g.Reroute(
                input=g.Reroute(input=menu_switch.o.corner_center).o.output
            ).o.output.switch.vector(mix.o.result_vector, vector_math_1)
        with g.Frame("Corner Flank Direction"):
            position_2 = g.Position()
            vector_math_2 = (
                position_2.o.position.corner.at(g.OffsetCornerInFace(offset=-1))
                - position_2
            )
        with g.Frame("Face Tangent Vector"):
            edge_vertices = g.EdgeVertices()
            evaluate_at_index = (
                (edge_vertices.o.position_2 - edge_vertices.o.position_1)
                .normalize()
                .edge.at(g.EdgesOfVertex())
            )
        with g.Frame("Elements to Points"):
            normal = g.Normal()
            edge_vertices_1 = g.EdgeVertices()
            menu_switch_1 = g.MenuSwitch.integer(
                instance_on, {"Points": 0, "Edges": 1, "Faces": 2, "Corners": 3}
            )
            reroute = g.Reroute(input=menu_switch_1.o.faces)
            reroute_1 = g.Reroute(input=menu_switch_1.o.output)
            capture = g.CaptureAttribute.face(geometry=geometry)
            face_area = capture.items.float("Face Area", g.FaceArea())
            tangent = capture.items.vector("Tangent", vector_math)
            reroute_2 = g.Reroute(input=capture.o.geometry)
            capture_1 = g.CaptureAttribute.edge(geometry=reroute_2)
            normal_1 = capture_1.items.vector("Normal", normal.o.normal)
            tangent_1 = capture_1.items.vector(
                "Tangent",
                (
                    edge_vertices_1.o.position_2 - edge_vertices_1.o.position_1
                ).normalize(),
            )
            capture_2 = g.CaptureAttribute.face(geometry=reroute_2)
            normal_2 = capture_2.items.vector("Normal", normal.o.normal)
            capture_2.items.vector("Tangent", tangent.output)
            capture_3 = g.CaptureAttribute.corner(geometry=reroute_2)
            tangent_2 = capture_3.items.vector(
                "Tangent", g.Reroute(input=g.Reroute(input=vector_math_2).o.output)
            )
            normal_3 = capture_3.items.vector("Normal", normal.o.normal)
            capture_4 = g.CaptureAttribute.point(
                geometry=g.Reroute(input=reroute_2.o.output)
            )
            normal_4 = capture_4.items.vector("Normal", normal.o.normal)
            value = capture_4.items.vector("Value", evaluate_at_index)
            index_switch = g.IndexSwitch.vector(
                reroute_1,
                (normal_4.output, normal_1.output, normal_2.output, normal_3.output),
            )
            index_switch_1 = g.IndexSwitch.vector(
                reroute_1,
                (
                    value.output,
                    tangent_1.output,
                    g.Reroute(input=g.Reroute(input=tangent.output).o.output),
                    tangent_2.output,
                ),
            )
            mesh_to_points = capture_3.o.geometry >> g.MeshToPoints.corners(
                position=g.Reroute(input=g.Reroute(input=switch_1).o.output),
                radius=0.05,
            )
            index_switch_2 = g.IndexSwitch.geometry(
                reroute_1,
                (
                    g.Reroute(input=capture_4.o.geometry),
                    capture_1.o.geometry >> g.MeshToPoints.edges(radius=0.05),
                    capture_2.o.geometry >> g.MeshToPoints.faces(radius=0.05),
                    mesh_to_points,
                ),
            )
        with g.Frame("Selection"):
            random_value = g.RandomValue.boolean(
                mask, seed=g.HashValue(value=seed, seed=548754876)
            )
        reroute_3 = g.Reroute(input=pick_instance)
        menu_switch_2 = g.MenuSwitch.integer(
            instance_type, {"Object": 0, "Collection": 1}
        )
        menu_switch_3 = g.MenuSwitch.integer(
            input_type, {"Data-Block": 0, "Geometry": 1}
        )
        with g.Frame("Input Geometry"):
            reroute_4 = g.Reroute(input=instance)
            reroute_5 = g.Reroute(input=menu_switch_2.o.collection)
            reroute_6 = g.Reroute(input=menu_switch_3.o.geometry)
            reroute_7 = g.Reroute(
                input=pick_instance.switch.boolean(true=reset_transform)
            )
            reroute_8 = g.Reroute(input=reroute_6.o.output)
            switch_2 = reroute_7.o.output.switch.geometry(
                reroute_4,
                g.SetInstanceTransform(
                    instances=reroute_4, transform=g.CombineTransform()
                ),
            )
            switch_3 = reroute_7.o.output.switch.geometry(
                g.CollectionInfo(collection=collection, separate_children=True),
                g.CollectionInfo(
                    collection=collection, separate_children=True, reset_children=True
                ),
            )
            index_switch_3 = g.IndexSwitch.geometry(
                g.Reroute(input=menu_switch_2.o.output),
                (g.ObjectInfo(object=object, as_instance=True).o.geometry, switch_3),
            )
            switch_4 = reroute_6.o.output.switch.geometry(index_switch_3, switch_2)
        reroute_9 = g.Reroute(input=g.Reroute(input=reroute.o.output).o.output)
        with g.Frame("Scale"):
            with g.Frame("Scale by Face Area"):
                reroute_10 = g.Reroute(input=scale)
                reroute_11 = g.Reroute(input=g.Reroute(input=scale).o.output)
                switch_5 = g.Reroute(input=scale_by_face_area).o.output.switch.vector(
                    reroute_10,
                    reroute_10.o.output
                    * (face_area.output.sqrt() * scale_by_face_area_multiplier),
                )
                with g.Frame("Only use when instancing on faces"):
                    switch_6 = reroute_9.o.output.switch.vector(reroute_11, switch_5)
        switch_7 = g.Reroute(
            input=g.Reroute(input=reroute_5.o.output).o.output
        ).o.output.switch.boolean(true=reroute_3)
        switch_8 = g.Reroute(
            input=g.Reroute(input=reroute_8.o.output).o.output
        ).o.output.switch.boolean(switch_7, g.Reroute(input=reroute_3.o.output))
        reroute_12 = g.Reroute(input=switch_8)
        with g.Frame("Instance Index (if target type is collection)"):
            index = g.Index()
            menu_switch_4 = g.MenuSwitch.integer(
                instance_index,
                {
                    "Random": g.HashValue(value=g.ID(), seed=seed),
                    "Sequence": index,
                    "Input": instance_index_1,
                },
            )
            switch_9 = reroute_12.o.output.switch.integer(
                g.Reroute(input=index.o.index), menu_switch_4
            )
        reroute_13 = g.Reroute(input=g.Reroute(input=switch_4).o.output)
        with g.Frame("Align Rotation to Normal"):
            align_rotation_to_vector = g.AlignRotationToVector(
                rotation=g.AlignRotationToVector(
                    vector=g.Reroute(input=index_switch.o.output)
                ),
                vector=g.Reroute(input=index_switch_1.o.output),
                axis="X",
                pivot_axis="Z",
            )
            switch_10 = align_rotation.switch.rotation(
                (0.0, 0.0, 0.0), align_rotation_to_vector
            )
        reroute_14 = g.Reroute(input=reroute_12.o.output)
        with g.Frame("Instance Fallback"):
            reroute_15 = g.Reroute(input=reroute_13.o.output)
            reroute_16 = g.Reroute(input=reroute_14.o.output)
            reroute_17 = g.Reroute(input=reroute_15.o.output)
            compare = g.Compare.integer.equal(
                g.DomainSize(
                    geometry=reroute_15, component="INSTANCES"
                ).o.instance_count,
                0,
            )
            warning = g.Warning.info(
                reroute_16.o.output & compare,
                "Pick Instance is on, but there are no instances to pick from. Falling back to using input as instance.",
            )
            switch_11 = warning.o.show.switch.geometry(
                reroute_17, g.GeometryToInstance(reroute_17)
            )
        instance_on_points = g.Reroute(
            input=g.Reroute(input=index_switch_2.o.output).o.output
        ) >> g.InstanceOnPoints(
            selection=g.Reroute(input=random_value.o.value),
            instance=switch_11,
            pick_instance=g.Reroute(input=reroute_16.o.output),
            instance_index=switch_9,
            rotation=switch_10,
            scale=g.Reroute(input=switch_6),
        )
        with g.Frame("Offset"):
            translate_instances = instance_on_points >> g.TranslateInstances(
                translation=g.CombineXYZ(z=surface_offset)
            )
        reroute_18 = g.Reroute(input=translate_instances.o.instances)
        switch_12 = realize_instances.switch.geometry(
            reroute_18,
            g.RealizeInstances(geometry=reroute_18, realize_to_point_domain=True),
        )
        (
            keep_surface.switch.geometry(
                switch_12,
                g.JoinGeometry(geometry=(g.Reroute(input=geometry), switch_12)),
            )
            >> geometry_1
        )

        instance_on.default_value = "Points"
        input_type.default_value = "Data-Block"
        instance_type.default_value = "Object"
        instance_index.default_value = "Random"
        corner_offset_method.default_value = "Face Center"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (4480.0, 280.0),
            "Object Info": (329.4, -240.7),
            "Instance on Points": (2644.6, 160.0),
            "Join Geometry": (4044.6, 200.0),
            "Group Input.001": (29.0, -98.2),
            "Frame": (-2749.4, 200.7),
            "Mesh to Points": (989.2, -201.4),
            "Menu Switch.001": (229.2, -161.4),
            "Mesh to Points.001": (989.2, -81.4),
            "Frame.001": (-369.2, 501.4),
            "Reroute.003": (1160.0, -460.0),
            "Index Switch": (1209.2, -101.4),
            "Translate Instances": (434.1, -35.8),
            "Combine XYZ": (209.5, -135.8),
            "Group Input.005": (29.5, -195.8),
            "Frame.003": (2877.6, 205.5),
            "Align Rotation to Vector.001": (94.2, -75.9),
            "Capture Attribute": (229.2, -241.4),
            "Frame.002": (1805.8, -144.1),
            "Group Input.003": (294.2, -35.9),
            "Switch": (494.2, -35.9),
            "Reroute.002": (34.2, -215.9),
            "Collection Info": (329.4, -380.7),
            "Menu Switch.002": (-2940.0, 120.0),
            "Index Switch.001": (889.4, -180.7),
            "Frame.004": (820.7, -652.7),
            "Vector Math": (535.8, -151.4),
            "Face Area.001": (29.2, -281.4),
            "Math": (310.0, -211.4),
            "Switch.002": (710.0, -51.4),
            "Frame.006": (29.3, -35.9),
            "Frame.007": (810.9, 1185.4),
            "Group Input.008": (29.1, -165.4),
            "Index": (215.9, -155.6),
            "Menu Switch.003": (455.9, -135.6),
            "Group Input.009": (209.6, -45.8),
            "Frame.008": (1370.4, 525.8),
            "Reroute.009": (2288.9, 541.8),
            "Realize Instances": (3624.6, 100.0),
            "Switch.003": (3824.6, 240.0),
            "Group Input.010": (3600.0, 340.0),
            "Frame.009": (926.2, -35.9),
            "Switch.004": (29.5, -35.6),
            "Reroute.011": (257.7, -334.0),
            "Reroute.012": (2360.0, -780.0),
            "Reroute.015": (813.8, -331.4),
            "Switch.005": (4264.6, 320.0),
            "Switch.001": (675.9, -35.6),
            "Reroute.005": (435.9, -115.6),
            "Reroute.006": (1129.2, -61.4),
            "Group Input.002": (29.2, -35.6),
            "Menu Switch.004": (-2940.0, 180.0),
            "Switch.006": (1086.9, -180.0),
            "Reroute.008": (1005.7, -640.0),
            "Reroute.010": (1685.7, -640.0),
            "Reroute.004": (3564.6, 140.0),
            "Corners of Face": (29.2, -115.9),
            "Corners of Face.001": (29.2, -275.9),
            "Evaluate at Index": (229.2, -75.9),
            "Evaluate at Index.001": (229.2, -215.9),
            "Position": (29.2, -35.9),
            "Vector Math.001": (409.2, -135.9),
            "Reroute.014": (34.2, -255.9),
            "Align Rotation to Vector.002": (294.2, -115.9),
            "Random Value.001": (418.5, -35.6),
            "Group Input.013": (29.6, -145.8),
            "Hash Value": (209.6, -125.8),
            "Frame.010": (-1089.2, 315.9),
            "Mesh to Points.002": (989.2, -341.4),
            "Position.002": (29.2, -95.6),
            "Mix": (409.2, -35.6),
            "Evaluate on Domain": (229.2, -155.6),
            "Group Input.014": (160.0, 700.0),
            "Reroute.017": (1460.0, 540.0),
            "Switch.008": (500.0, 880.0),
            "Switch.009": (700.0, 820.0),
            "Reroute.019": (380.0, 820.0),
            "Warning": (660.9, -49.7),
            "Reroute.013": (34.2, -221.2),
            "Domain Size": (105.9, -85.7),
            "Compare": (285.0, -64.1),
            "Boolean Math": (474.2, -41.2),
            "Switch.007": (828.4, -99.5),
            "Geometry to Instance": (585.6, -201.5),
            "Reroute.016": (532.5, -214.6),
            "Frame.005": (1471.4, 190.3),
            "Menu Switch": (698.6, -35.7),
            "Switch.010": (1618.6, -215.7),
            "Group Input.015": (518.6, -35.7),
            "Vector Math.006": (1309.4, -35.7),
            "Vector Math.007": (1109.4, -95.7),
            "Math.002": (509.4, -335.7),
            "Capture Attribute.001": (769.2, -421.4),
            "Group Input.016": (509.4, -235.7),
            "Math.003": (709.4, -295.7),
            "Switch.013": (889.4, -195.7),
            "Offset Corner in Face.002": (29.2, -95.7),
            "Position.004": (29.2, -35.7),
            "Evaluate at Index.004": (229.2, -35.7),
            "Vector Math.011": (409.2, -75.7),
            "Position.005": (1109.4, -35.7),
            "Math.009": (329.4, -335.7),
            "Group": (29.4, -75.7),
            "Group Input.017": (689.4, -155.7),
            "Frame.011": (-1089.2, -164.3),
            "Frame.012": (949.4, -100.1),
            "Frame.013": (29.3, -360.0),
            "Frame.014": (-2498.6, 1355.7),
            "Reroute.021": (1538.6, -55.7),
            "Reroute.023": (918.6, -55.7),
            "Reroute.024": (49.2, -501.4),
            "Reroute.025": (809.2, -501.4),
            "Reroute.027": (609.2, -301.4),
            "Reroute.029": (669.2, -61.4),
            "Reroute": (469.2, -541.4),
            "Reroute.030": (49.2, -521.4),
            "Reroute.031": (629.2, -521.4),
            "Reroute.033": (409.2, -181.4),
            "Reroute.034": (1129.2, -541.4),
            "Reroute.032": (430.0, -131.4),
            "Reroute.035": (2329.5, 453.6),
            "Index Switch.002": (1209.2, -401.4),
            "Normal.002": (450.3, -36.0),
            "Capture Attribute.003": (769.2, -161.4),
            "Capture Attribute.004": (769.2, -61.4),
            "Index Switch.003": (1209.2, -501.4),
            "Reroute.026": (1151.5, -278.9),
            "Edge Vertices": (29.2, -81.4),
            "Vector Math.002": (229.2, -81.4),
            "Vector Math.003": (445.0, -109.6),
            "Capture Attribute.002": (769.2, -281.4),
            "Group Input.018": (29.2, -161.4),
            "Reroute.028": (994.0, 788.2),
            "Reroute.036": (1333.4, 147.8),
            "Reroute.037": (429.9, -40.7),
            "Evaluate at Index.002": (595.7, -36.0),
            "Frame.015": (-1163.6, -530.4),
            "Edges of Vertex": (409.3, -116.8),
            "Edge Vertices.001": (29.3, -76.8),
            "Vector Math.004": (229.3, -76.8),
            "Vector Math.005": (409.3, -76.8),
            "Group Input.019": (-3140.0, 200.0),
            "Group Input.021": (29.4, -320.7),
            "Reroute.038": (2498.2, 152.9),
            "Math.001": (35.2, -220.2),
            "Hash Value.001": (269.8, -285.6),
            "ID": (81.0, -305.7),
            "Reroute.001": (3960.0, 300.0),
            "Reroute.020": (289.4, -640.7),
            "Reroute.022": (-1040.8, -472.9),
            "Reroute.040": (1212.0, -107.4),
            "Reroute.041": (1207.6, -43.7),
            "Reroute.042": (-348.1, 717.5),
            "Reroute.018": (546.4, 719.8),
            "Reroute.043": (-352.6, 684.1),
            "Reroute.045": (290.0, -111.4),
            "Reroute.007": (400.0, 660.0),
            "Reroute.046": (540.0, 660.0),
            "Switch.011": (329.4, -100.7),
            "Group Input": (129.4, -180.7),
            "Switch.012": (749.4, -560.7),
            "Switch.014": (649.4, -300.7),
            "Collection Info.001": (329.4, -540.7),
            "Reroute.048": (969.4, -40.7),
            "Reroute.049": (794.4, -80.7),
            "Group Input.020": (129.4, -120.7),
            "Reroute.039": (569.4, -360.7),
            "Set Instance Transform": (489.4, -700.7),
            "Combine Transform": (269.4, -740.7),
        }


ASSET = InstanceOnElements

ASSET_METADATA = {
    "description": "Create copies of referenced geometry on geometry elements",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "a01301f0-5ae0-4627-91a4-b7fde91e5c5a",
    "catalog_simple_name": "Instances",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
