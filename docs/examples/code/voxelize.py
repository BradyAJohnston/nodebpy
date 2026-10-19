from nodebpy import geometry as g

with g.tree("Voxelize", is_modifier=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    size = tree.inputs.float("Voxel Size", 0.2, min_value=0.01, subtype="DISTANCE")
    material = tree.inputs.material("Material")

    voxel = g.Cube(size=size) >> g.SetMaterial(material=material)

    (
        geometry
        >> g.MeshToVolume(interior_band_width=size)
        >> g.DistributePointsInVolume(mode="Grid", spacing=size)
        >> g.InstanceOnPoints(instance=voxel)
        >> tree.outputs.geometry("Geometry")
    )
