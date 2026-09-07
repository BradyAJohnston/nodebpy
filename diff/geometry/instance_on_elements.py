# Node-group asset 'Instance on Elements' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup

from .face_corner_angle import FaceCornerAngle


class InstanceOnElements(CustomGeometryGroup):
    _name = "Instance on Elements"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
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
            switch_1 = menu_switch.o.corner_center.switch.vector(
                mix.o.result_vector, vector_math_1
            )
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
            capture = g.CaptureAttribute.face(geometry=geometry)
            face_area = capture.items.float("Face Area", g.FaceArea())
            tangent = capture.items.vector("Tangent", vector_math)
            capture_1 = g.CaptureAttribute.corner(geometry=capture.o.geometry)
            tangent_1 = capture_1.items.vector("Tangent", vector_math_2)
            normal_1 = capture_1.items.vector("Normal", normal.o.normal)
            capture_2 = g.CaptureAttribute.edge(geometry=capture.o.geometry)
            normal_2 = capture_2.items.vector("Normal", normal.o.normal)
            tangent_2 = capture_2.items.vector(
                "Tangent",
                (
                    edge_vertices_1.o.position_2 - edge_vertices_1.o.position_1
                ).normalize(),
            )
            capture_3 = g.CaptureAttribute.face(geometry=capture.o.geometry)
            normal_3 = capture_3.items.vector("Normal", normal.o.normal)
            capture_3.items.vector("Tangent", tangent.output)
            capture_4 = g.CaptureAttribute.point(geometry=capture.o.geometry)
            normal_4 = capture_4.items.vector("Normal", normal.o.normal)
            value = capture_4.items.vector("Value", evaluate_at_index)
            index_switch = g.IndexSwitch.vector(
                menu_switch_1,
                (normal_4.output, normal_2.output, normal_3.output, normal_1.output),
            )
            index_switch_1 = g.IndexSwitch.vector(
                menu_switch_1,
                (value.output, tangent_2.output, tangent.output, tangent_1.output),
            )
            index_switch_2 = g.IndexSwitch.geometry(
                menu_switch_1,
                (
                    capture_4.o.geometry,
                    capture_2.o.geometry >> g.MeshToPoints.edges(radius=0.05),
                    capture_3.o.geometry >> g.MeshToPoints.faces(radius=0.05),
                    capture_1.o.geometry
                    >> g.MeshToPoints.corners(position=switch_1, radius=0.05),
                ),
            )
        with g.Frame("Selection"):
            random_value = g.RandomValue.boolean(
                mask, seed=g.HashValue(value=seed, seed=548754876)
            )
        menu_switch_2 = g.MenuSwitch.integer(
            instance_type, {"Object": 0, "Collection": 1}
        )
        menu_switch_3 = g.MenuSwitch.integer(
            input_type, {"Data-Block": 0, "Geometry": 1}
        )
        with g.Frame("Input Geometry"):
            switch_2 = pick_instance.switch.boolean(true=reset_transform)
            switch_3 = switch_2.switch.geometry(
                g.CollectionInfo(collection=collection, separate_children=True),
                g.CollectionInfo(
                    collection=collection, separate_children=True, reset_children=True
                ),
            )
            switch_4 = switch_2.switch.geometry(
                instance,
                g.SetInstanceTransform(
                    instances=instance, transform=g.CombineTransform()
                ),
            )
            index_switch_3 = g.IndexSwitch.geometry(
                menu_switch_2,
                (g.ObjectInfo(object=object, as_instance=True).o.geometry, switch_3),
            )
            switch_5 = menu_switch_3.o.geometry.switch.geometry(
                index_switch_3, switch_4
            )
        switch_6 = menu_switch_3.o.geometry.switch.boolean(
            menu_switch_2.o.collection.switch.boolean(true=pick_instance), pick_instance
        )
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
            switch_7 = switch_6.switch.integer(index, menu_switch_4)
        with g.Frame("Scale"):
            with g.Frame("Scale by Face Area"):
                switch_8 = scale_by_face_area.switch.vector(
                    scale,
                    scale * (face_area.output.sqrt() * scale_by_face_area_multiplier),
                )
                with g.Frame("Only use when instancing on faces"):
                    switch_9 = menu_switch_1.o.faces.switch.vector(scale, switch_8)
        with g.Frame("Instance Fallback"):
            compare = g.Compare.integer.equal(
                g.DomainSize(geometry=switch_5, component="INSTANCES").o.instance_count,
                0,
            )
            warning = g.Warning.info(
                switch_6 & compare,
                "Pick Instance is on, but there are no instances to pick from. Falling back to using input as instance.",
            )
            switch_10 = warning.o.show.switch.geometry(
                switch_5, g.GeometryToInstance(switch_5)
            )
        with g.Frame("Align Rotation to Normal"):
            align_rotation_to_vector = g.AlignRotationToVector(
                rotation=g.AlignRotationToVector(vector=index_switch),
                vector=index_switch_1,
                axis="X",
                pivot_axis="Z",
            )
            switch_11 = align_rotation.switch.rotation(
                (0.0, 0.0, 0.0), align_rotation_to_vector
            )
        instance_on_points = index_switch_2 >> g.InstanceOnPoints(
            selection=random_value,
            instance=switch_10,
            pick_instance=switch_6,
            instance_index=switch_7,
            rotation=switch_11,
            scale=switch_9,
        )
        with g.Frame("Offset"):
            translate_instances = instance_on_points >> g.TranslateInstances(
                translation=g.CombineXYZ(z=surface_offset)
            )
        switch_12 = realize_instances.switch.geometry(
            translate_instances,
            g.RealizeInstances(
                geometry=translate_instances, realize_to_point_domain=True
            ),
        )
        (
            keep_surface.switch.geometry(
                switch_12, g.JoinGeometry(geometry=(geometry, switch_12))
            )
            >> geometry_1
        )

        instance_on.default_value = "Points"
        input_type.default_value = "Data-Block"
        instance_type.default_value = "Object"
        instance_index.default_value = "Random"
        corner_offset_method.default_value = "Face Center"


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
