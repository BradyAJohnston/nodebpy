# Node-group asset 'Capture Rest Geometry' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class CaptureRestGeometry(CustomGeometryGroup):
    _name = "Capture Rest Geometry"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

        geometry = tree.inputs.geometry(
            "Geometry", description="Points to modify the positions of"
        )
        rest_position = tree.inputs.boolean(
            "Rest Position", True, structure_type="SINGLE"
        )
        geometry_1 = tree.outputs.geometry("Geometry")

        named_attribute = g.NamedAttribute.vector("rest_position")
        get_geometry_bundle = g.GetGeometryBundle(geometry=geometry, remove=True)
        set_position = g.SetPosition(
            geometry=geometry,
            position=named_attribute.o.exists.switch.vector(
                g.Position(), named_attribute
            ),
        )
        store_bundle_item = g.StoreBundleItem.geometry(
            get_geometry_bundle.o.bundle,
            "rest_geometry",
            rest_position.switch.geometry(geometry, set_position),
        )
        (
            get_geometry_bundle
            >> g.SetGeometryBundle(bundle=store_bundle_item)
            >> geometry_1
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Set Geometry Bundle": (420.0, 60.0),
            "Set Position": (-120.0, -220.0),
            "Named Attribute": (-480.0, -300.0),
            "Group Output": (600.0, 60.0),
            "Group Input": (-140.0, 60.0),
            "Get Geometry Bundle": (40.0, 60.0),
            "Store Bundle Item": (240.0, 0.0),
            "Switch": (-300.0, -240.0),
            "Position": (-480.0, -240.0),
            "Switch.001": (60.0, -60.0),
            "Group Input.002": (-120.0, -100.0),
            "Group Input.003": (-300.0, -160.0),
        }


ASSET = CaptureRestGeometry

ASSET_METADATA = {
    "catalog_id": "1599ecb4-d5ef-4dac-bde9-357d938c1bee",
    "catalog_simple_name": "Geometry Nodes-Geometry-Write",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
