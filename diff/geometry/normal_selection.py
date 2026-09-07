# Node-group asset 'Normal Selection' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class NormalSelection(CustomGeometryGroup):
    _name = "Normal Selection"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        direction = tree.inputs.vector(
            "Direction",
            (0.0, 0.0, 1.0),
            description="Target direction to compare the normal to",
            min_value=-340282000000000000000000000000000000000.0,
            max_value=340282000000000000000000000000000000000.0,
            subtype="XYZ",
        )
        threshold = tree.inputs.float(
            "Threshold",
            0.0872665,
            description="Maximum angle between normal and target to include in the selection",
            subtype="ANGLE",
        )
        selection = tree.outputs.boolean(
            "Selection",
            description="Selection of elements with normals matching a target direction. (The normal is evaluated on the same domain as this selection output.)",
        )

        (
            g.Compare(
                a=direction,
                b=g.Normal(),
                angle=threshold,
                operation="LESS_EQUAL",
                data_type="VECTOR",
                mode="DIRECTION",
            )
            >> selection
        )


ASSET = NormalSelection

ASSET_METADATA = {
    "description": "Create a selection by normal",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "5fa1e91c-e798-4051-8e4d-5d47f76f789b",
    "catalog_simple_name": "Geometry-Selection",
}
