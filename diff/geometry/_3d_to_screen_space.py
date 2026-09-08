# Node-group asset '3D to Screen Space' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .transform_and_project import TransformAndProject


class Group3DToScreenSpace(CustomGeometryGroup):
    _name = "3D to Screen Space"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
        tree.disable_arrange()

        vector = tree.inputs.vector(
            "Vector",
            (0.0, 0.0, 0.0),
            description="Input 3D coordinates in world space",
            subtype="XYZ",
        )
        camera = tree.inputs.object(
            "Camera",
            description="The camera used for rendering the scene",
            optional_label=True,
        )
        clamp_depth = tree.inputs.boolean(
            "Clamp Depth", True, description="Clamps depth to camera clipping range"
        )
        normalized = tree.outputs.vector(
            "Normalized",
            description="2D coordinates in the [0, 1] range in screen space",
            dimensions=2,
            subtype="XYZ",
        )
        depth = tree.outputs.float(
            "Depth", description="Depth in scene units. Same as depth pass"
        )

        camera_info = g.CameraInfo(camera=camera)
        group = TransformAndProject(
            Vector=vector,
            Transform=g.ObjectInfo(object=camera).o.transform.invert(),
            Projection=camera_info,
        )
        (
            clamp_depth.switch.float(
                group.o.depth,
                group.o.depth.clamp(camera_info.o.clip_start, camera_info.o.clip_end),
            )
            >> depth
        )

        group >> normalized

        # Restore authored node positions.
        tree.node_positions = {
            "Camera Info": (-101.3, -375.5),
            "Object Info.001": (-281.3, -295.5),
            "Invert Matrix": (-101.3, -295.5),
            "Group Input.001": (-624.1, -240.1),
            "Clamp": (364.0, -342.9),
            "Group Output.001": (782.2, -186.9),
            "Switch": (594.0, -247.2),
            "Group Input.002": (420.0, -240.0),
            "Group": (100.0, -200.0),
        }


ASSET = Group3DToScreenSpace

ASSET_METADATA = {
    "description": "Convert input coordinates to normalized camera space",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
