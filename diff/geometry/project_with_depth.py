# Node-group asset 'Project with Depth' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class ProjectWithDepth(CustomGeometryGroup):
    _name = "Project with Depth"
    _color_tag = "VECTOR"

    def _build_group(self, tree):
        tree.disable_arrange()

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

        # Restore authored node positions.
        tree.node_positions = {
            "Math": (29.7, -36.3),
            "Math.001": (249.7, -76.3),
            "Math.002": (29.7, -216.3),
            "Math.003": (719.7, -272.3),
            "Frame.001": (30.0, -36.0),
            "Math.004": (29.7, -36.3),
            "Math.005": (189.7, -56.3),
            "Math.006": (449.7, -196.3),
            "Math.007": (229.7, -256.3),
            "Math.008": (49.7, -256.3),
            "Frame.002": (30.0, -476.0),
            "Group Output": (897.5, -568.1),
            "Group Input.001": (-1025.3, 456.7),
            "Group Input.002": (-1024.6, -3.3),
            "Project Point": (731.5, -122.2),
            "Transform Point": (931.9, -219.9),
            "Vector Math": (29.7, -31.9),
            "Combine XYZ.001": (533.6, -30.5),
            "Separate XYZ.001": (269.7, -31.9),
            "Group Input": (-519.4, -426.6),
            "Group Input.003": (449.8, -226.6),
            "Frame": (-302.0, -349.0),
            "Frame.003": (-865.0, 669.0),
        }


ASSET = ProjectWithDepth

ASSET_METADATA = {
    "description": "Transforms 2D coordinates with their corresponding depth into a 3D vector ",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "8c0273f0-3645-449f-9d95-c4f17fb910db",
    "catalog_simple_name": "Utilities-Vector",
}
