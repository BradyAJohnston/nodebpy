import math
from functools import reduce
from itertools import combinations, product
from operator import and_, or_

import bpy

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.builder import FloatSocket
from nodebpy.nodes.geometry.groups import PrincipalComponents


def import_channel() -> bpy.types.GeometryNodeTree:
    string_to_format = "{base_path}/{scale}/x0y0z0/x0y0z0c0t{time:04}.vdb"

    with g.tree("Channel Import", arrange="simple") as tree:
        base_path = tree.inputs.string("base_path", subtype="FILE_PATH")
        time = tree.inputs.integer("Time")
        channel_number = tree.inputs.integer("Channel Number")
        channel_name = tree.inputs.string("Channel Name")
        min_value = tree.inputs.float("Minimum Value")
        max_value = tree.inputs.float("Maximum Value")

        volume = g.ImportVDB(
            g.FormatString(
                string_to_format,
                {
                    "time": time,
                    "channel_number": channel_number,
                    "base_path": base_path,
                    "scale": g.Integer(0),
                },
            )
        )
        gng = g.GetNamedGrid.float(volume, "data")
        sng = g.StoreNamedGrid.float(
            gng,
            name=channel_name,
            grid=(gng.o.grid - min_value) / (max_value - min_value),
        )
        _ = sng >> tree.outputs.geometry("Volume")

    return tree.tree


def test_decoder_8bit():
    # this should actually be 8 bits but it takes a bit longer to run through
    # (~20 seconds) so for testing we can keep it much smaller. It's a nice
    # clean implementation and good example of the code in action.
    N_BITS = 4
    with g.tree("8-Bit Decoder", arrange="simple") as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(N_BITS)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]

        for i, combo in enumerate(product((False, True), repeat=N_BITS)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")

    assert len(tree) == 54
    assert len(tree.inputs) == 4
    assert len(tree.outputs) == 16
    assert all(
        i.links[0].from_node.operation == "AND"
        for i in tree.nodes["Group Output"].inputs
        if i.identifier != "__extend__"
    )


def test_import_channel():
    tree = import_channel()
    assert len(tree.nodes) == 10


def test_PCA_asset():
    with g.tree():
        pca = PrincipalComponents()

    assert len(pca.node_tree.nodes) == 35


def test_surface_hello_world():
    with g.tree("Hello World") as tree:
        height = tree.inputs.float("Height", 3.0)
        omega = tree.inputs.float("Omega", 0.5)

        with g.Frame("Computing the wave"):
            with g.Frame("Distance"):
                pos = g.Position().o.position
                distance = g.Math.square_root(pos.x**2 + pos.y**2)
            z = height * g.Math.sine(distance / omega) / distance

        with g.Frame("Point offset & smooth"):
            mesh = (
                g.Grid(20, 20, 200, 200)
                >> g.SetPosition(offset=g.CombineXYZ(z=z))
                >> g.SetShadeSmooth.face()
            )

        mesh >> tree.outputs.geometry("Mesh")

    assert len(tree) == 22


def test_eulers_number():
    with g.tree("Euler's Number") as tree:
        tau = g.Float(math.tau)
        e = g.Float(math.e)
        value = g.Float(1.0)

        zone = g.RepeatZone(100, {"value": value})

        with g.Frame("Factorial"):
            value = g.Math.square_root(zone.iteration * tau) * (
                (zone.iteration / e) ** zone.iteration
            )

        (zone.input.o.value + 1 / value) >> zone.output.i.value

        (
            zone.output.o.value
            >> g.ValueToString(decimals=10)
            >> g.StringToCurves()
            >> g.FillCurve()
            >> g.ExtrudeMesh(offset_scale=0.1)
            >> tree.outputs.geometry()
        )

    assert isinstance(zone.input.i.value, FloatSocket)


class CompareGenerationMethods:
    def test_compare_methods(self, snapshot):
        trees = [
            getattr(self, method)()
            for method in [x for x in dir(self) if x.startswith("method_")]
        ]
        for tree in trees:
            with tree as tree:
                tree.arrange()

        assert len(trees[0]) == len(trees[1])
        assert len(trees[0].tree.links) == len(trees[1].tree.links)


class TestCompareMiNCleanGridVerts(CompareGenerationMethods):
    def method_nodebpy_gridverts(self) -> TreeBuilder:
        with g.tree() as tree:
            extent = tree.inputs.vector(
                "Extent (unit)",
                (7.0, 5.0, 4.0),
                min_value=0.0,
                max_value=1_000_000,
            )
            world = tree.inputs.vector(
                "World per Unit",
                (1e-6, 1e-6, 1e-6),
                min_value=0.0,
            )

            pos = g.Position().o.position
            mul = extent * world

            equals = []
            for x in [-0.5, 0.5]:
                comp = g.VectorMath.multiply(mul, x).o.vector
                equals.append(
                    (g.Compare.float.equal(a, b, 0.001) for a, b in zip(comp, pos))
                )

            ors = [a | b for a, b in zip(*equals)]
            ands = [a & b for a, b in combinations(ors, 2)]
            final = reduce(or_, ands)
            final >> tree.outputs.boolean()
        return tree

    def method_api_gridverts(self) -> TreeBuilder:
        node_group = bpy.data.node_groups.get("_grid_verts")
        if node_group:
            return node_group

        node_group = bpy.data.node_groups.new(
            type="GeometryNodeTree", name="_grid_verts"
        )
        links = node_group.links
        interface = node_group.interface

        interface.new_socket(
            "Extent (unit)", in_out="INPUT", socket_type="NodeSocketVector"
        )
        interface.items_tree[-1].default_value = (7.0, 5.0, 4.0)
        interface.items_tree[-1].min_value = 0.0
        interface.items_tree[-1].max_value = 10000000.0
        interface.items_tree[-1].attribute_domain = "POINT"

        interface.new_socket(
            "World per Unit", in_out="INPUT", socket_type="NodeSocketVector"
        )
        interface.items_tree[-1].default_value = (1e-6, 1e-6, 1e-6)
        interface.items_tree[-1].min_value = 0.0
        interface.items_tree[-1].max_value = 3.4028234663852886e38
        interface.items_tree[-1].attribute_domain = "POINT"

        interface.new_socket("Boolean", in_out="OUTPUT", socket_type="NodeSocketBool")
        interface.items_tree[-1].attribute_domain = "POINT"

        group_input = node_group.nodes.new("NodeGroupInput")
        group_input.location = (-1000, 0)

        group_output = node_group.nodes.new("NodeGroupOutput")
        group_output.location = (850, 100)

        extent_world = node_group.nodes.new("ShaderNodeVectorMath")
        extent_world.operation = "MULTIPLY"
        extent_world.location = (-620, -220)
        links.new(group_input.outputs["Extent (unit)"], extent_world.inputs[0])
        links.new(group_input.outputs["World per Unit"], extent_world.inputs[1])

        pos = node_group.nodes.new("GeometryNodeInputPosition")
        pos.location = (-620, 140)

        pos_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
        pos_xyz.location = (-420, 140)
        links.new(pos.outputs[0], pos_xyz.inputs[0])

        boundary_compares = [[], [], []]

        for ix, side in enumerate(["min", "max"]):
            loc = node_group.nodes.new("ShaderNodeVectorMath")
            loc.operation = "MULTIPLY"
            loc.location = (-620, -80 - 170 * ix)
            links.new(extent_world.outputs[0], loc.inputs[0])
            loc.inputs[1].default_value = (
                (-0.5, -0.5, -0.5) if side == "min" else (0.5, 0.5, 0.5)
            )

            loc_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
            loc_xyz.location = (-420, -80 - 170 * ix)
            links.new(loc.outputs[0], loc_xyz.inputs[0])

            for axix in range(3):
                compare = node_group.nodes.new("FunctionNodeCompare")
                compare.data_type = "FLOAT"
                compare.operation = "EQUAL"
                compare.mode = "ELEMENT"
                compare.location = (-210, 320 - (ix * 3 + axix) * 140)
                links.new(pos_xyz.outputs[axix], compare.inputs[1])
                links.new(loc_xyz.outputs[axix], compare.inputs[0])
                boundary_compares[axix].append(compare)

        on_boundary = []
        for axix in range(3):
            ornode = node_group.nodes.new("FunctionNodeBooleanMath")
            ornode.operation = "OR"
            ornode.location = (10, 100 - axix * 140)
            links.new(boundary_compares[axix][0].outputs[0], ornode.inputs[0])
            links.new(boundary_compares[axix][1].outputs[0], ornode.inputs[1])
            on_boundary.append(ornode)

        edge_xy = node_group.nodes.new("FunctionNodeBooleanMath")
        edge_xy.operation = "AND"
        edge_xy.location = (220, 120)
        links.new(on_boundary[0].outputs[0], edge_xy.inputs[0])
        links.new(on_boundary[1].outputs[0], edge_xy.inputs[1])

        edge_yz = node_group.nodes.new("FunctionNodeBooleanMath")
        edge_yz.operation = "AND"
        edge_yz.location = (220, -20)
        links.new(on_boundary[1].outputs[0], edge_yz.inputs[0])
        links.new(on_boundary[2].outputs[0], edge_yz.inputs[1])

        edge_zx = node_group.nodes.new("FunctionNodeBooleanMath")
        edge_zx.operation = "AND"
        edge_zx.location = (220, -160)
        links.new(on_boundary[2].outputs[0], edge_zx.inputs[1])
        links.new(on_boundary[0].outputs[0], edge_zx.inputs[0])

        edge_or_1 = node_group.nodes.new("FunctionNodeBooleanMath")
        edge_or_1.operation = "OR"
        edge_or_1.location = (420, 80)
        links.new(edge_xy.outputs[0], edge_or_1.inputs[0])
        links.new(edge_yz.outputs[0], edge_or_1.inputs[1])

        edge_or_2 = node_group.nodes.new("FunctionNodeBooleanMath")
        edge_or_2.operation = "OR"
        edge_or_2.location = (620, 80)
        links.new(edge_or_1.outputs[0], edge_or_2.inputs[0])
        links.new(edge_zx.outputs[0], edge_or_2.inputs[1])

        links.new(edge_or_2.outputs[0], group_output.inputs["Boolean"])

        return TreeBuilder.geometry(node_group)
