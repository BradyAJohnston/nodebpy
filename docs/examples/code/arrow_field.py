from nodebpy import geometry as g
from nodebpy import shader as s


def arrow(vertices):
    """A unit-length arrow pointing up Z, built from a shaft and a head."""
    shaft = g.Cylinder(vertices, radius=0.05, depth=0.7)
    head = g.Cone(vertices, radius_bottom=0.12, depth=0.3)
    return g.JoinGeometry(
        [
            shaft >> g.TransformGeometry(translation=(0, 0, 0.35)),
            head >> g.TransformGeometry(translation=(0, 0, 0.7)),
        ]
    )


with s.material("Arrow") as material:
    strength = s.Attribute.instancer("strength").o.fac
    ramp = s.ColorRamp(
        strength,
        items=[
            (0.0, (0.05, 0.15, 0.6, 1.0)),
            (0.5, (0.1, 0.7, 0.6, 1.0)),
            (1.0, (1.0, 0.5, 0.05, 1.0)),
        ],
    )
    s.PrincipledBSDF(base_color=ramp, roughness=0.4) >> s.MaterialOutput()


with g.tree("Arrow Field", is_modifier=True) as tree:
    size = tree.inputs.float("Size", 6.0, min_value=0.0)
    count = tree.inputs.integer("Count", 15, min_value=2)
    scale = tree.inputs.float("Arrow Scale", 0.5, min_value=0.0)
    vertices = tree.inputs.integer("Arrow Vertices", 12, min_value=3)

    with g.Frame("Vortex"):
        # swirl around Z, strongest near the axis
        position = g.Position().o.position
        field = position.cross((0, 0, -1)) / (position.length() ** 2 + 0.5)
        strength = field.length() / field.length().point.max()

    points = (
        g.Grid(size, size, count, count)
        >> g.MeshToPoints()
        >> g.StoreNamedAttribute.point.float(name="strength", value=strength)
    )

    (
        points
        >> g.InstanceOnPoints(
            instance=arrow(vertices),
            rotation=g.AlignRotationToVector(vector=field),
            scale=strength.map_range(0.0, 1.0, 0.3, 1.0) * scale,
        )
        >> g.SetMaterial(material=material.material)
        >> tree.outputs.geometry("Geometry")
    )
