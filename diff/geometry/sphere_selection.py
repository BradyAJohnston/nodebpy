# Node-group asset 'Sphere Selection' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class SphereSelection(CustomGeometryGroup):
    _name = "Sphere Selection"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        center = tree.inputs.vector(
            "Center",
            (0.0, 0.0, 0.0),
            description="Center position of the sphere selection",
            min_value=-340282000000000000000000000000000000000.0,
            max_value=340282000000000000000000000000000000000.0,
            subtype="TRANSLATION",
        )
        radius = tree.inputs.float(
            "Radius",
            1.0,
            description="Maximum distance of the element from the selection center",
            subtype="DISTANCE",
        )
        selection = tree.outputs.boolean(
            "Selection", description="Selection of elements within a sphere"
        )

        transform_gizmo = g.TransformGizmo(
            value=(g.CombineTransform(translation=center),),
            position=center,
            use_translation_x=True,
            use_translation_y=True,
            use_translation_z=True,
        )
        (g.Position().o.position.distance(center) <= radius) >> selection


ASSET = SphereSelection

ASSET_METADATA = {
    "description": "Create a spherical selection",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "5fa1e91c-e798-4051-8e4d-5d47f76f789b",
    "catalog_simple_name": "Geometry-Selection",
}
