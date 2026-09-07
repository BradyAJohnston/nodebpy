# Node-group asset 'Geometry Input' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class GeometryInput(CustomGeometryGroup):
    _name = "Geometry Input"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
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

        switch = relative_space.switch.geometry(
            g.CollectionInfo(collection=collection),
            g.CollectionInfo(collection=collection, transform_space="RELATIVE"),
        )
        switch_1 = relative_space.switch.geometry(
            g.ObjectInfo(object=object, as_instance=as_instance).o.geometry,
            g.ObjectInfo(
                object=object, as_instance=as_instance, transform_space="RELATIVE"
            ).o.geometry,
        )
        menu_switch = g.MenuSwitch.geometry(
            input_type, {"Object": switch_1, "Collection": switch}
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
