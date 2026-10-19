from nodebpy import geometry as g
from nodebpy import shader as s

with s.material("Asphalt") as asphalt:
    (
        s.PrincipledBSDF(base_color=(0.02, 0.02, 0.025, 1.0), roughness=0.8)
        >> s.MaterialOutput()
    )

with g.tree("City Builder", is_modifier=True) as tree:
    roads = tree.inputs.geometry("Roads")
    road_width = tree.inputs.float("Road Width", 0.25, min_value=0.0)
    with tree.inputs.panel("City"):
        size_x = tree.inputs.float("Size X", 5.0, min_value=0.0)
        size_y = tree.inputs.float("Size Y", 5.0, min_value=0.0)
        density = tree.inputs.float("Density", 10.0, min_value=0.0)
        seed = tree.inputs.integer("Seed")
    with tree.inputs.panel("Buildings"):
        smallest = tree.inputs.vector("Size Min", (0.1, 0.1, 0.2))
        largest = tree.inputs.vector("Size Max", (0.3, 0.3, 1.0))
        material = tree.inputs.material("Material")

    with g.Frame("Roads"):
        half = road_width / 2
        profile = g.CurveLine(start=g.CombineXYZ(x=-half), end=g.CombineXYZ(x=half))
        road_mesh = (
            roads
            >> g.CurveToMesh(profile_curve=profile)
            >> g.SetMaterial(material=asphalt.material)
        )

    with g.Frame("Building Lots"):
        # scatter lots everywhere, then clear the ones that land on a road
        road_points = g.CurveToPoints.evaluated(roads)
        distance = g.GeometryProximity(road_points, target_element="POINTS").o.distance
        lots = (
            g.Grid(size_x, size_y)
            >> g.DistributePointsOnFaces(density=density, seed=seed)
            >> g.DeleteGeometry.point(selection=distance < road_width)
        )

    with g.Frame("Buildings"):
        # move the cube up so it sits on the ground before it is scaled
        block = (
            g.Cube()
            >> g.TransformGeometry(translation=(0, 0, 0.5))
            >> g.SetMaterial(material=material)
        )
        size = g.RandomValue.vector(min=smallest, max=largest, seed=seed)
        buildings = lots >> g.InstanceOnPoints(instance=block, scale=size)

    g.JoinGeometry([road_mesh, buildings]) >> tree.outputs.geometry("City")
