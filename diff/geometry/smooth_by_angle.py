# Node-group asset 'Smooth by Angle' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class SmoothByAngle(CustomGeometryGroup):
    _name = "Smooth by Angle"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        mesh = tree.inputs.geometry("Mesh")
        angle = tree.inputs.float(
            "Angle",
            0.5235988,
            description="Maximum face angle for smooth edges",
            min_value=0.0,
            max_value=3.1415927,
            structure_type="FIELD",
            subtype="ANGLE",
        )
        ignore_sharpness = tree.inputs.boolean(
            "Ignore Sharpness", False, structure_type="SINGLE"
        )
        mesh_1 = tree.outputs.geometry("Mesh")

        (
            mesh
            >> g.SetShadeSmooth.edge(
                selection=g.IsEdgeSmooth().o.smooth | ignore_sharpness,
                shade_smooth=(g.EdgeAngle() <= angle)
                & (g.IsFaceSmooth().o.smooth | ignore_sharpness),
            )
            >> g.SetShadeSmooth()
            >> mesh_1
        )


ASSET = SmoothByAngle

ASSET_METADATA = {
    "description": "Set the sharpness of mesh edges based on the angle between the neighboring faces",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "9e98eca8-e987-44d3-88a1-6633d0a8ad82",
    "catalog_simple_name": "Normals",
}

TREE_PROPERTIES = {
    "is_modifier": True,
}
