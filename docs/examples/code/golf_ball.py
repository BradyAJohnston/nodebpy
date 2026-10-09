from nodebpy import geometry as g
from nodebpy import shader as s

with s.material("Golf Ball") as material:
    coords = s.TextureCoordinate().o.object
    grain = s.NoiseTexture(coords, scale=180.0, detail=3.0, roughness=0.65).o.fac
    micro = s.NoiseTexture(coords, scale=650.0, detail=2.0).o.fac

    white = grain.map_range(0.25, 0.75, interpolation_type="SMOOTHSTEP")
    color = white.mix.color((0.69, 0.70, 0.67, 1.0), (0.91, 0.91, 0.87, 1.0))

    # darken the inside of each dimple so the pattern reads at a distance
    occlusion = s.AmbientOcclusion(distance=0.05).o.ao
    color = (occlusion**2).mix.color((0.3, 0.3, 0.29, 1.0), color)

    (
        s.PrincipledBSDF(
            base_color=color,
            roughness=grain.map_range(0.2, 0.8, 0.32, 0.46),
            normal=s.Bump(
                height=grain * 0.7 + micro * 0.3, strength=0.16, distance=0.0025
            ),
        )
        >> s.MaterialOutput()
    )


with g.tree("Golf Ball", is_modifier=True) as tree:
    radius = tree.inputs.float("Radius", 1.0, min_value=0.0, subtype="DISTANCE")
    with tree.inputs.panel("Dimples"):
        layout = tree.inputs.integer("Layout", 4, min_value=1, max_value=6)
        width = tree.inputs.float("Width", 0.075, min_value=0.0, subtype="DISTANCE")
        depth = tree.inputs.float("Depth", 0.012, min_value=0.0, subtype="DISTANCE")

    # one dimple centred on each vertex of a coarse icosphere
    centers = g.IcoSphere(radius, subdivisions=layout) >> g.MeshToPoints()
    distance = g.GeometryProximity(centers, target_element="POINTS").o.distance
    profile = distance.map_range(
        0.0, width, 1.0, 0.0, interpolation_type="SMOOTHERSTEP"
    )

    # push the dense surface inwards along its normal
    inwards = g.Position().o.position.normalize() * -(profile * depth)

    (
        g.IcoSphere(radius, subdivisions=7)
        >> g.SetPosition(offset=inwards)
        >> g.SetShadeSmooth()
        >> g.SetMaterial(material=material.material)
        >> tree.outputs.geometry("Geometry")
    )
