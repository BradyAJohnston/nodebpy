# Node-group asset '3D to Screen Space' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup

from .transform_and_project import TransformAndProject


class Group3DToScreenSpace(CustomGeometryGroup):
    _name = "3D to Screen Space"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
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


ASSET = Group3DToScreenSpace

ASSET_METADATA = {
    "description": "Convert input coordinates to normalized camera space",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
