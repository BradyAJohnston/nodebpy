from nodebpy import geometry as g

with g.tree("Repeat Grid", is_modifier=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    columns = tree.inputs.integer("Columns", 4, min_value=1)
    rows = tree.inputs.integer("Rows", 3, min_value=1)
    gap = tree.inputs.vector("Gap", (0.2, 0.2, 0.0), subtype="TRANSLATION")

    # one cell is the geometry's footprint plus the gap between copies
    bounds = g.BoundingBox(geometry)
    cell = bounds.o.max - bounds.o.min + gap

    grid = g.Grid(
        size_x=(columns - 1) * cell.x,
        size_y=(rows - 1) * cell.y,
        vertices_x=columns,
        vertices_y=rows,
    )

    (
        grid
        >> g.MeshToPoints()
        >> g.InstanceOnPoints(instance=geometry)
        >> tree.outputs.geometry("Geometry")
    )
