# Node-group asset 'Geometry Input' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class GeometryInput(CustomGeometryGroup):
    _name = "Geometry Input"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        input_type = tree.inputs.menu(
            "Input Type",
            description="How the geometry input should be exposed",
            expanded=True,
            optional_label=True,
        )
        object = tree.inputs.object(
            "Object", description="Object to use as the input geometry"
        )
        collection = tree.inputs.collection(
            "Collection", description="Collection to use as the input geometry"
        )
        relative_space = tree.inputs.boolean(
            "Relative Space",
            False,
            description="Transform the input relative to the main geometry",
        )
        as_instance = tree.inputs.boolean(
            "As Instance",
            True,
            description="Input the geometry as an instance. (Further processing might require non-instance geometry).",
        )
        replace_original = tree.inputs.boolean(
            "Replace Original",
            False,
            description="Replace the original input geometry with the selected input geometry",
        )
        geometry_1 = tree.outputs.geometry("Geometry")

        reroute = g.Reroute(input=relative_space)
        reroute_1 = g.Reroute(input=collection)
        switch = reroute.o.output.switch.geometry(
            g.ObjectInfo(object=object, as_instance=as_instance).o.geometry,
            g.ObjectInfo(
                object=object, as_instance=as_instance, transform_space="RELATIVE"
            ).o.geometry,
        )
        switch_1 = reroute.o.output.switch.geometry(
            g.CollectionInfo(collection=reroute_1),
            g.CollectionInfo(collection=reroute_1, transform_space="RELATIVE"),
        )
        menu_switch = g.MenuSwitch.geometry(
            input_type, {"Object": switch, "Collection": switch_1}
        )
        switch_2 = as_instance.switch.geometry(
            g.RealizeInstances(geometry=menu_switch, realize_to_point_domain=True),
            menu_switch,
        )
        (
            replace_original.switch.geometry(
                g.JoinGeometry(geometry=(geometry, switch_2)), switch_2
            )
            >> geometry_1
        )

        input_type.default_value = "Object"

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (700.0, 20.0),
            "Collection Info": (-800.0, -220.0),
            "Realize Instances": (-120.0, -80.0),
            "Switch": (520.0, 20.0),
            "Group Input.001": (320.0, 80.0),
            "Menu Switch": (-325.9, 0.1),
            "Object Info": (-980.0, 140.0),
            "Collection Info.001": (-800.0, -380.0),
            "Object Info.001": (-800.0, 40.0),
            "Switch.001": (-530.4, 31.1),
            "Switch.002": (-528.0, -139.0),
            "Group Input.002": (-800.0, 120.0),
            "Reroute": (-581.2, 8.1),
            "Switch.003": (80.3, -29.8),
            "Group Input.003": (-120.0, 0.0),
            "Group Input.004": (-1320.0, -140.0),
            "Group Input.005": (-520.0, 100.0),
            "Reroute.001": (-860.0, -400.0),
            "Group Input.006": (80.0, 40.0),
            "Join Geometry": (320.0, 0.0),
        }


ASSET = GeometryInput

ASSET_METADATA = {
    "description": "Take reference geometry as input",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "a7b80fd1-5de6-4c15-9049-52f25f4376de",
    "catalog_simple_name": "Geometry",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
