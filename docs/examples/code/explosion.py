from nodebpy import geometry as g

with g.tree("Explosion", is_modifier=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    speed = tree.inputs.float("Speed", 4.0, min_value=0.0)
    gravity = tree.inputs.float("Gravity", 9.81)
    seed = tree.inputs.integer("Seed")

    with g.Frame("Fragments"):
        # split every face off and give it its own launch velocity
        launch = g.Normal() * speed * g.RandomValue.float(0.4, 1.6, seed=seed)
        fragments = (
            geometry
            >> g.SplitEdges()
            >> g.ScaleElements.face(scale=0.9)
            >> g.StoreNamedAttribute.face.vector(name="velocity", value=launch)
        )

    with g.Frame("Ballistics"):
        sim = g.SimulationZone()
        pieces = sim.items.geometry(fragments, "Pieces")
        velocity = g.NamedAttribute.vector("velocity")
        dt = sim.delta_time

        # Set Position reads `velocity` after it has been stored,
        # so the offset already includes this step's gravity
        (
            pieces.current
            >> g.StoreNamedAttribute.point.vector(
                name="velocity", value=velocity - g.CombineXYZ(z=gravity * dt)
            )
            >> g.SetPosition(offset=velocity * dt)
            >> pieces.next
        )

    pieces.result >> tree.outputs.geometry("Geometry")
