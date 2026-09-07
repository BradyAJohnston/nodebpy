# Node-group asset 'Smooth Geometry' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class SmoothGeometry(CustomGeometryGroup):
    _name = "Smooth Geometry"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        geometry = tree.inputs.geometry(
            "Geometry", description="Points to smooth based on their neighbors"
        )
        selection = tree.inputs.boolean("Selection", True, hide_value=True)
        iterations = tree.inputs.integer(
            "Iterations",
            5,
            description="How many times to repeat the smoothing step",
            min_value=0,
        )
        weight = tree.inputs.float(
            "Weight",
            0.5,
            description="Relative mix weight of neighboring elements",
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )
        geometry_1 = tree.outputs.geometry("Geometry")

        (
            geometry
            >> g.SetPosition(
                selection=selection,
                position=g.BlurAttribute.vector(g.Position(), iterations, weight),
            )
            >> geometry_1
        )


ASSET = SmoothGeometry

ASSET_METADATA = {
    "description": "Smooth connected parts of a geometry",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "463e71f0-6db1-41af-bc96-6f875196aac7",
    "catalog_simple_name": "Geometry-Operations",
}
