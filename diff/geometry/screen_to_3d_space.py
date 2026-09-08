# Node-group asset 'Screen to 3D Space' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from .project_with_depth import ProjectWithDepth


class ScreenTo3DSpace(CustomGeometryGroup):
    _name = "Screen to 3D Space"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
        tree.disable_arrange()

        normalized = tree.inputs.vector(
            "Normalized",
            (0.5, 0.5),
            description="2D screen space coordinates in the [0, 1] range",
            dimensions=2,
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )
        depth = tree.inputs.float(
            "Depth",
            0.5,
            description="Depth from camera in scene units. Same as depth pass",
            min_value=-10000.0,
            max_value=10000.0,
            subtype="DISTANCE",
        )
        camera = tree.inputs.object(
            "Camera",
            description="The camera used for rendering the scene",
            optional_label=True,
        )
        vector = tree.outputs.vector(
            "Vector", description="Projected 3D vector in 3D space", subtype="XYZ"
        )

        camera_info = g.CameraInfo(camera=camera)
        (
            ProjectWithDepth(
                Normalized=normalized,
                Depth=depth,
                Projection=camera_info.o.projection_matrix.invert(),
                Transform=g.ObjectInfo(object=camera, transform_space="RELATIVE"),
                **{
                    "Clip Start": camera_info.o.clip_start,
                    "Clip End": camera_info.o.clip_end,
                },
            )
            >> vector
        )

        # Restore authored node positions.
        tree.node_positions = {
            "Group Input": (-434.9, 11.4),
            "Group Output": (20.0, -40.0),
            "Group": (-200.0, -40.0),
            "Camera Info": (-640.0, -160.0),
            "Invert Matrix": (-480.0, -100.0),
            "Object Info.001": (-640.0, -300.0),
            "Group Input.001": (-860.0, -340.0),
        }


ASSET = ScreenTo3DSpace

ASSET_METADATA = {
    "description": "Convert coordinates from screen to 3D space",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
