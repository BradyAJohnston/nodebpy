# Node-group asset 'Box Selection' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class BoxSelection(CustomGeometryGroup):
    _name = "Box Selection"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

        center = tree.inputs.vector(
            "Center",
            (0.0, 0.0, 0.0),
            description="Center position of box selection",
            min_value=-340282000000000000000000000000000000000.0,
            max_value=340282000000000000000000000000000000000.0,
            subtype="TRANSLATION",
        )
        size = tree.inputs.vector(
            "Size",
            (1.0, 1.0, 1.0),
            description="Edge length of box selection",
            min_value=0.0,
            subtype="TRANSLATION",
        )
        selection = tree.outputs.boolean(
            "Selection", description="Elements inside the box"
        )

        position = g.Position()
        vector_math = size * 0.5
        _transform_gizmo = g.TransformGizmo(
            value=(g.CombineTransform(translation=center),),
            position=center,
            use_translation_x=True,
            use_translation_y=True,
            use_translation_z=True,
        )
        (
            ((position >= center - vector_math) & (position <= center + vector_math))
            >> selection
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (340.0, 40.0),
            "Compare": (-20.0, 40.0),
            "Position": (-260.0, 120.0),
            "Vector Math": (-260.0, -100.0),
            "Group Input": (-520.0, 260.0),
            "Vector Math.001": (-520.0, 40.0),
            "Group Input.001": (-700.0, 40.0),
            "Boolean Math": (160.0, 40.0),
            "Compare.001": (-20.0, -100.0),
            "Vector Math.002": (-260.0, 40.0),
            "Transform Gizmo": (-20.0, 280.0),
            "Combine Transform": (-280.0, 340.0),
        }


ASSET = BoxSelection

ASSET_METADATA = {
    "description": "Create a box selection",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "5fa1e91c-e798-4051-8e4d-5d47f76f789b",
    "catalog_simple_name": "Geometry-Selection",
}
