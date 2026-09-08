# Node-group asset 'Face Corner Angle' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class FaceCornerAngle(CustomGeometryGroup):
    _name = "Face Corner Angle"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        tree.disable_arrange()

        corner_angle = tree.outputs.float(
            "Corner Angle",
            description="Angle between the next and previous edge of a face corner within the face",
        )
        bisector = tree.outputs.vector(
            "Bisector",
            description="Directional vector pointing central between next and previous edge of a face corner",
        )

        position = g.Position()
        reroute = g.Reroute(input=g.Normal().o.true_normal.face.evaluate())
        vector_math = (
            position.o.position.corner.at(g.OffsetCornerInFace(offset=-1)) - position
        ).normalize()
        vector_math_1 = (
            position.o.position.corner.at(g.OffsetCornerInFace(offset=1)) - position
        ).normalize()
        math = vector_math.dot(vector_math_1).acos()
        math_1 = vector_math.cross(vector_math_1).dot(reroute).sign()
        with g.Frame("angle"):
            reroute_1 = g.Reroute(input=math)
            switch = (math_1 > 0.0).switch.float(reroute_1, 6.2831855 - reroute_1)
        switch.corner.evaluate() >> corner_angle
        vector_rotate = g.VectorRotate(
            vector=g.Reroute(input=vector_math_1),
            axis=g.Reroute(input=reroute.o.output),
            angle=switch * 0.5,
        )
        vector_rotate.o.vector.corner.evaluate() >> bisector

        # Restore authored node positions.
        tree.node_positions = {
            "Group Output": (1320.0, 380.0),
            "Offset Corner in Face": (-1104.2, 329.0),
            "Offset Corner in Face.001": (-1102.7, 200.4),
            "Position.003": (-1104.2, 389.0),
            "Evaluate at Index.002": (-904.2, 389.0),
            "Evaluate at Index.003": (-904.2, 229.0),
            "Vector Math.002": (-544.2, 329.0),
            "Vector Math.003": (-544.2, 209.0),
            "Vector Math.008": (-724.2, 349.0),
            "Vector Math.009": (-724.2, 169.0),
            "Vector Math.010": (-340.0, 460.0),
            "Math.004": (660.0, 380.0),
            "Vector Math.012": (-160.0, 460.0),
            "Evaluate on Domain.001": (-540.0, 620.0),
            "Normal": (-740.0, 580.0),
            "Math.006": (0.0, 460.0),
            "Switch.011": (274.4, -75.9),
            "Vector Math.013": (-340.0, 320.0),
            "Reroute.022": (34.4, -215.9),
            "Vector Rotate": (860.0, 380.0),
            "Math.008": (-160.0, 320.0),
            "Frame.011": (185.6, 515.9),
            "Compare.001": (94.4, -35.9),
            "Math.007": (94.4, -155.9),
            "Evaluate on Domain": (1100.0, 360.0),
            "Evaluate on Domain.002": (1100.0, 480.0),
            "Reroute": (-338.3, 531.7),
            "Reroute.001": (660.1, 535.6),
            "Reroute.002": (780.0, 180.0),
        }


ASSET = FaceCornerAngle

ASSET_METADATA = {
    "description": "Returns the angle between the two flanking edges of a face corner inside the face",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
