from math import tau

from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputInteger


def mottled(scale, a, b, spread=0.2):
    """Blend two colors through a noise texture of the given scale."""
    noise = s.NoiseTexture(scale=scale).o.fac
    return noise.map_range(0.5 - spread, 0.5 + spread).mix.color(a, b)


with s.material("Bark") as bark:
    (
        s.PrincipledBSDF(base_color=(0.097, 0.036, 0.008, 1.0), roughness=0.9)
        >> s.MaterialOutput()
    )

with s.material("Foliage") as foliage:
    greens = mottled(37.0, (0.002, 0.035, 0.015, 1.0), (0.001, 0.427, 0.015, 1.0))
    browns = mottled(20.0, (0.209, 0.168, 0.004, 1.0), (0.264, 0.033, 0.013, 1.0))
    color = mottled(5.0, greens, browns, spread=0.1)
    s.PrincipledBSDF(base_color=color, roughness=0.9) >> s.MaterialOutput()

with s.material("Ground") as ground:
    color = mottled(2.0, (0.05, 0.06, 0.02, 1.0), (0.12, 0.09, 0.04, 1.0))
    s.PrincipledBSDF(base_color=color, roughness=1.0) >> s.MaterialOutput()


class Tree(CustomGeometryGroup):
    """A conifer: a tapered trunk inside a squashed, randomly lumpy sphere."""

    _name = "A Tree"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        height: InputFloat = 7.0,
        width: InputFloat = 0.5,
        trunk: InputFloat = 0.2,
        conic: InputFloat = 0.4,
        seed: InputInteger = 0,
    ):
        super().__init__(
            height=height, width=width, trunk=trunk, conic=conic, seed=seed
        )

    def _build_group(self, tree):
        height = tree.inputs.float("Height", 7.0, min_value=0.0, subtype="DISTANCE")
        width = tree.inputs.float("Width", 0.5, min_value=0.0, subtype="FACTOR")
        trunk = tree.inputs.float(
            "Trunk", 0.2, min_value=0.0, max_value=0.9, subtype="FACTOR"
        )
        conic = tree.inputs.float(
            "Conic", 0.4, min_value=-1.0, max_value=1.0, subtype="FACTOR"
        )
        seed = tree.inputs.integer("Seed")

        with g.Frame("Trunk"):
            base = height * 0.04
            stem = g.Cone(
                radius_bottom=base, radius_top=base / 3, depth=height * 0.9
            ) >> g.SetMaterial(material=bark.material)

        with g.Frame("Foliage"):
            # stretch a unit sphere into the crown, wider at the bottom when conic
            crown = height * (1 - trunk)
            radius = width * height
            position = g.Position().o.position
            spread = position.z.map_range(
                -0.5, 0.5, radius * (1 + conic), radius * (1 - conic)
            )
            shape = g.CombineXYZ(spread, spread, crown) * g.RandomValue.vector(
                0.8, 1.2, seed=seed
            )
            leaves = (
                g.IcoSphere(radius=0.5, subdivisions=3)
                >> g.SetPosition(
                    position=position * shape + g.CombineXYZ(z=height - crown / 2)
                )
                >> g.SetMaterial(material=foliage.material)
            )

        (
            g.JoinGeometry([stem, leaves])
            >> g.SetShadeSmooth()
            >> tree.outputs.geometry("Tree")
        )


# height and width of each tree variant
SHAPES = [(6, 0.3), (7, 0.25), (8, 0.3), (9, 0.2), (10, 0.22)]

with g.tree("Forest", is_modifier=True) as tree:
    size = tree.inputs.float("Size", 40.0, min_value=0.0, subtype="DISTANCE")
    spacing = tree.inputs.float("Spacing", 2.0, min_value=0.1, subtype="DISTANCE")
    hills = tree.inputs.float("Hills", 4.0, subtype="DISTANCE")
    seed = tree.inputs.integer("Seed")

    with g.Frame("Terrain"):
        bumps = g.NoiseTexture(scale=0.05).o.fac - 0.5
        terrain = (
            g.Grid(size, size, 80, 80)
            >> g.SetPosition(offset=g.CombineXYZ(z=bumps * hills))
            >> g.SetShadeSmooth()
            >> g.SetMaterial(material=ground.material)
        )

    with g.Frame("Tree Variants"):
        # a handful of trees, each with its own seed and proportions
        variants = g.GeometryToInstance(
            *[Tree(height, width, seed=i) for i, (height, width) in enumerate(SHAPES)]
        )

    with g.Frame("Planting"):
        trees = (
            terrain
            >> g.DistributePointsOnFaces(
                distance_min=spacing,
                density_max=1.0,
                seed=seed,
                distribute_method="POISSON",
            )
            >> g.InstanceOnPoints(
                instance=variants,
                pick_instance=True,
                instance_index=g.RandomValue.integer(0, len(SHAPES) - 1, seed=seed + 1),
                rotation=g.CombineXYZ(z=g.RandomValue.float(0, tau, seed=seed + 2)),
                scale=g.RandomValue.float(0.6, 1.3, seed=seed + 3),
            )
        )

    g.JoinGeometry([terrain, trees]) >> tree.outputs.geometry("Geometry")
