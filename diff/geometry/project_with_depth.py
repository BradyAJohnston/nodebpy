# Node-group asset 'Project with Depth' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
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


ASSET = ProjectWithDepth

ASSET_METADATA = {
    "description": "Transforms 2D coordinates with their corresponding depth into a 3D vector ",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
