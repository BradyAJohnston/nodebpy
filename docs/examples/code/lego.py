from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputInteger


class LegoBrick(CustomGeometryGroup):
    """A brick of studded cells, with a matching hole underneath each stud."""

    _name = "LEGO Brick"
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        size: InputFloat = 1.0,
        count_x: InputInteger = 1,
        count_y: InputInteger = 1,
    ):
        super().__init__(**{"Size": size, "Count X": count_x, "Count Y": count_y})

    def _build_group(self, tree):
        size = tree.inputs.float("Size", 1.0, min_value=0.0)
        count_x = tree.inputs.integer("Count X", 1, min_value=1)
        count_y = tree.inputs.integer("Count Y", 1, min_value=1)

        with g.Frame("Cell"):
            depth = size / 8
            stud = g.Cylinder(vertices=16, radius=size / 3, depth=depth)
            # the same stud sits on top of the cube and is cut out of its base
            top = stud >> g.TransformGeometry(
                translation=g.CombineXYZ(z=(size + depth) / 2)
            )
            hole = stud >> g.TransformGeometry(
                translation=g.CombineXYZ(z=(depth - size) / 2)
            )
            cell = g.MeshBoolean.difference(
                g.MeshBoolean.union([g.Cube(size=size), top]), [hole]
            )

        with g.Frame("Rows and Columns"):
            row = g.MeshLine(count_x, offset=g.CombineXYZ(x=size))
            row = row >> g.InstanceOnPoints(instance=cell)
            (
                g.MeshLine(count_y, offset=g.CombineXYZ(y=size))
                >> g.InstanceOnPoints(instance=row)
                >> g.RealizeInstances()
                >> g.MergeByDistance()
                >> tree.outputs.geometry("Brick")
            )


with g.tree("Mesh to LEGO", is_modifier=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    size = tree.inputs.float("Brick Size", 0.2, min_value=0.01, subtype="DISTANCE")
    material = tree.inputs.material("Material")

    (
        geometry
        >> g.MeshToVolume(interior_band_width=size)
        >> g.DistributePointsInVolume(mode="Grid", spacing=size)
        >> g.InstanceOnPoints(instance=LegoBrick(size))
        >> g.RealizeInstances()
        >> g.MergeByDistance()
        >> g.SetMaterial(material=material)
        >> tree.outputs.geometry("Geometry")
    )
