# Node-group asset 'Screen to 3D Space' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class ProjectWithDepth(CustomGeometryGroup):
    _name = "Project with Depth"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
        normalized = tree.inputs.vector(
            "Normalized", (0.5, 0.5), dimensions=2, min_value=0.0, max_value=1.0
        )
        depth = tree.inputs.float(
            "Depth", 1.0, min_value=-10000.0, max_value=10000.0, subtype="DISTANCE"
        )
        projection = tree.inputs.matrix("Projection")
        transform = tree.inputs.matrix("Transform")
        clip_start = tree.inputs.float(
            "Clip Start", 0.1, min_value=-10000.0, max_value=10000.0, subtype="DISTANCE"
        )
        clip_end = tree.inputs.float(
            "Clip End", 100.0, min_value=-10000.0, max_value=10000.0, subtype="DISTANCE"
        )
        vector = tree.outputs.vector("Vector", subtype="XYZ")

        with g.Frame("Project Depth"):
            with g.Frame("(f + n) / (f - n)"):
                math = (clip_start + clip_end) / (clip_end - clip_start)
            with g.Frame("2fn / Z*(f - n)"):
                math_1 = clip_start * clip_end * 2.0 / (depth * (clip_end - clip_start))
            math_2 = math - math_1
        with g.Frame():
            vector_1 = g.VectorMath.multiply_add(
                normalized, (2.0, 2.0, 2.0), (-1.0, -1.0, -1.0)
            ).o.vector
            project_point = g.ProjectPoint(
                vector=g.CombineXYZ(x=vector_1.x, y=vector_1.y, z=math_2),
                transform=projection,
            )
            project_point.o.vector.transform(transform) >> vector


class ScreenTo3DSpace(CustomGeometryGroup):
    _name = "Screen to 3D Space"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
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
                **{
                    "Normalized": normalized,
                    "Depth": depth,
                    "Projection": camera_info.o.projection_matrix.invert(),
                    "Transform": g.ObjectInfo(
                        object=camera, transform_space="RELATIVE"
                    ),
                    "Clip Start": camera_info.o.clip_start,
                    "Clip End": camera_info.o.clip_end,
                }
            )
            >> vector
        )


ASSET = ScreenTo3DSpace

ASSET_METADATA = {
    "description": "Convert coordinates from screen to 3D space",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
