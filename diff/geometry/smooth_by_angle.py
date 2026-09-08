# Node-group asset 'Smooth by Angle' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class SmoothByAngle(CustomGeometryGroup):
    _name = "Smooth by Angle"
    _color_tag = "GEOMETRY"

    def _build_group(self, tree):
        tree.disable_arrange()

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

        # Restore authored node positions.
        tree.node_positions = {
            "Set Shade Smooth": (120.0, -80.0),
            "Set Shade Smooth.001": (300.0, -80.0),
            "Group Output": (480.0, -80.0),
            "Edge Angle": (-440.0, -240.0),
            "Group Input": (-80.0, -80.0),
            "Is Edge Smooth": (-260.0, -120.0),
            "Is Shade Smooth": (-439.5, -396.6),
            "Compare": (-260.0, -260.0),
            "Boolean Math.001": (-80.0, -260.0),
            "Group Input.001": (-439.5, -329.1),
            "Group Input.002": (-259.0, -188.7),
            "Boolean Math": (-80.0, -149.1),
            "Boolean Math.002": (-260.0, -380.0),
            "Group Input.003": (-440.0, -460.0),
        }


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
