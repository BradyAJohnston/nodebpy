"""Static-typing smoke test for nodebpy as an installed, PEP 561 package.

Never executed — ``run.sh`` installs the built wheel into a clean venv and
checks this file with mypy, pyright, basedpyright, pyrefly and ty. Every
``assert_type`` must hold under all of them, so inference drift in any one
checker fails CI.
"""

from typing import assert_type, override

from bpy.types import GeometryNodeTree

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import (
    BooleanSocket,
    ColorSocket,
    CustomGeometryGroup,
    FloatSocket,
    FloatSocketGrid,
    GeometrySocket,
    IntegerSocket,
    ShaderSocket,
    Socket,
    TreeBuilder,
    VectorSocket,
)
from nodebpy.builder.items import Item


def readme_example() -> TreeBuilder[GeometryNodeTree]:
    with g.tree("AnotherTree", collapse=True) as tree:
        rotation = (
            g.RandomValue.vector(min=-1, seed=2)
            >> g.AlignRotationToVector()
            >> g.RotateRotation(rotate_by=g.AxisAngleToRotation(angle=0.3))
        )
        _ = (
            tree.inputs.integer("Count", 10)
            >> g.Points(position=g.RandomValue.vector(min=-1))
            >> g.InstanceOnPoints(instance=g.Cube(), rotation=rotation)
            >> g.SetPosition(
                position=g.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> g.RealizeInstances()
            >> g.InstanceOnPoints(g.Cube(), instance=...)
            >> tree.outputs.geometry("Instances")
        )
    assert_type(tree, TreeBuilder[GeometryNodeTree])
    return tree


def interface_sockets() -> None:
    with g.tree("Interface") as tree:
        assert_type(tree.inputs.integer("Count", 10), IntegerSocket)
        assert_type(tree.inputs.float("Scale"), FloatSocket)
        assert_type(tree.inputs.vector("Offset"), VectorSocket)
        assert_type(tree.inputs.geometry("Geometry"), GeometrySocket)
        assert_type(tree.inputs.boolean("Flag"), BooleanSocket)


def socket_operators() -> None:
    with g.tree("Operators"):
        pos = g.Position()
        assert_type(pos.o.position, VectorSocket)
        assert_type(pos.o.position.x, FloatSocket)
        assert_type(pos.o.position * 2.0, VectorSocket)
        assert_type(pos.o.position.x + 1, FloatSocket)
        assert_type(g.Index().o.index * 2, IntegerSocket)
        # Arithmetic directly on a node yields its default output socket.
        assert_type(g.Value(2.0) * 2, Socket)
        assert_type(pos + (1, 2, 3), Socket)


def manual_nodes() -> None:
    with g.tree("Manual"):
        cube = g.Cube()
        pos = g.Position()

        sna = g.StoreNamedAttribute.point.integer(cube, name="x", value=g.Index())
        assert_type(sna, g.StoreNamedAttribute[IntegerSocket])
        assert_type(sna.o.geometry, GeometrySocket)
        assert_type(sna.i.value, IntegerSocket)

        assert_type(
            g.Compare.float.less_than(pos.o.position.x, 1.0), g.Compare[FloatSocket]
        )

        sw = g.IndexSwitch.float(g.Index(), [1.0, 2.0])
        assert_type(sw, g.IndexSwitch[FloatSocket])
        assert_type(sw.o.output, FloatSocket)

        assert_type(
            g.MenuSwitch.integer(None, {"A": 1, "B": 2}), g.MenuSwitch[IntegerSocket]
        )

        cap = g.CaptureAttribute(cube)
        assert_type(cap.items.float("x", pos.o.position.x), Item[FloatSocket])

        stat = g.AttributeStatistic.point.float(cube, attribute=pos.o.position.x)
        assert_type(stat, g.AttributeStatistic[FloatSocket])
        assert_type(stat.o.mean, FloatSocket)

        si = g.SampleIndex.point.integer(geometry=cube, value=g.Index(), index=0)
        assert_type(si, g.SampleIndex[IntegerSocket])
        assert_type(si.o.value, IntegerSocket)

        ramp = g.ColorRamp(0.5)
        assert_type(ramp, g.ColorRamp)
        assert_type(ramp.o.color, ColorSocket)


def grids() -> None:
    with g.tree("Grids"):
        grid = g.FieldToGrid.float(None)
        assert_type(grid, g.FieldToGrid[FloatSocketGrid])
        assert_type(grid.i.topology, FloatSocketGrid)
        sdf = g.SDFGridBoolean.union([grid.i.topology])
        assert_type(sdf.o.grid, FloatSocketGrid)


def zones() -> None:
    with g.tree("Zones") as tree:
        zone = g.RepeatZone(10)
        assert_type(zone.iteration, IntegerSocket)
        input_node, output_node = zone
        _ = (input_node, output_node)
        zone.output.o.geometry >> tree.outputs.geometry()


class OffsetGroup(CustomGeometryGroup):
    _name: str = "Offset Group"

    @override
    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.inputs.float("Value") >> tree.outputs.float("Result")


def shader_and_compositor() -> None:
    with s.tree("Material"):
        bsdf = s.PrincipledBSDF(base_color=(1, 0, 0, 1))
        bsdf >> s.MaterialOutput()
        assert_type(bsdf.o.bsdf, ShaderSocket)

    with c.tree("Compositor"):
        assert_type(c.Blur(), c.Blur)
