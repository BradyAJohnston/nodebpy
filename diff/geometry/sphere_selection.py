# Node-group asset 'Sphere Selection' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class SphereSelection(CustomGeometryGroup):
    _name = "Sphere Selection"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

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

        _transform_gizmo = g.TransformGizmo(
            value=(g.CombineTransform(translation=center),),
            position=center,
            use_translation_x=True,
            use_translation_y=True,
            use_translation_z=True,
        )
        (g.Position().o.position.distance(center) <= radius) >> selection

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (320.0, 40.0),
            "Position": (-260.0, 40.0),
            "Group Input": (-260.0, -180.0),
            "Group Input.001": (-260.0, -60.0),
            "Transform Gizmo": (140.0, -140.0),
            "Combine Transform": (-40.0, -120.0),
            "Vector Math": (-40.0, 40.0),
            "Compare": (140.0, 40.0),
        }


ASSET = SphereSelection

ASSET_METADATA = {
    "description": "Create a spherical selection",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "5fa1e91c-e798-4051-8e4d-5d47f76f789b",
    "catalog_simple_name": "Geometry-Selection",
}
