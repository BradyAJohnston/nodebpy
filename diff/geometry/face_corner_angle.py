# Node-group asset 'Face Corner Angle' (GeometryNodeTree), dumped by nodebpy.assets.dump_library.
# Rebuild the library with nodebpy.assets.build_library (python -m nodebpy.assets build).
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup


class FaceCornerAngle(CustomGeometryGroup):
    _name = "Face Corner Angle"
    _color_tag = "INPUT"

    def _build_group(self, tree):
        corner_angle = tree.outputs.float(
            "Corner Angle",
            description="Angle between the next and previous edge of a face corner within the face",
        )
        bisector = tree.outputs.vector(
            "Bisector",
            description="Directional vector pointing central between next and previous edge of a face corner",
        )

        position = g.Position()
        evaluate_on_domain = g.Normal().o.true_normal.face.evaluate()
        vector_math = (
            position.o.position.corner.at(g.OffsetCornerInFace(offset=-1)) - position
        ).normalize()
        vector_math_1 = (
            position.o.position.corner.at(g.OffsetCornerInFace(offset=1)) - position
        ).normalize()
        math = vector_math.dot(vector_math_1).acos()
        math_1 = vector_math.cross(vector_math_1).dot(evaluate_on_domain).sign()
        with g.Frame("angle"):
            switch = (math_1 > 0.0).switch.float(math, 6.2831855 - math)
        switch.corner.evaluate() >> corner_angle
        (
            g.VectorRotate(
                vector=vector_math_1, axis=evaluate_on_domain, angle=switch * 0.5
            ).o.vector.corner.evaluate()
            >> bisector
        )


ASSET = FaceCornerAngle

ASSET_METADATA = {
    "description": "Returns the angle between the two flanking edges of a face corner inside the face",
    "copyright": "Blender Foundation",
    "license": "CC0 - Public Domain",
    "catalog_id": "b6bb38bb-bfe1-4a12-b2bc-fc87d060864f",
    "catalog_simple_name": "Mesh-Read",
}
