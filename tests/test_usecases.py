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


def test_import_microscopy_meshes():
    GROUP_NAME = "Import Microscopy Meshes"

    def _set_common_socket_defaults(socket):
        socket.attribute_domain = "POINT"
        if hasattr(socket, "default_input"):
            socket.default_input = "VALUE"
        if hasattr(socket, "structure_type"):
            socket.structure_type = "AUTO"

    def _new_input(interface, name, socket_type, default=None):
        socket = interface.new_socket(
            name=name, in_out="INPUT", socket_type=socket_type
        )
        _set_common_socket_defaults(socket)
        if default is not None:
            socket.default_value = default
        return socket

    def _new_output(interface, name, socket_type):
        socket = interface.new_socket(
            name=name, in_out="OUTPUT", socket_type=socket_type
        )
        _set_common_socket_defaults(socket)
        return socket

    def import_microscopy_meshes_node_group():
        node_group = bpy.data.node_groups.get(GROUP_NAME)
        if node_group:
            return node_group

        node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name=GROUP_NAME)
        node_group.color_tag = "NONE"
        node_group.description = ""
        node_group.default_group_node_width = 140
        node_group.is_modifier = True
        node_group.show_modifier_manage_panel = True

        links = node_group.links
        nodes = node_group.nodes
        interface = node_group.interface

        _new_output(interface, "Geometry", "NodeSocketGeometry")

        _new_input(interface, "Include", "NodeSocketBool", False)
        _new_input(interface, "template_str", "NodeSocketString", "")
        _new_input(interface, "cache_dir", "NodeSocketString", "")
        _new_input(interface, "dataset_hash", "NodeSocketString", "")
        _new_input(interface, "scale", "NodeSocketInt", 0)
        _new_input(interface, "resolution", "NodeSocketInt", 0)
        _new_input(interface, "channel_ix", "NodeSocketInt", 0)
        _new_input(interface, "Frame", "NodeSocketInt", 0)
        _new_input(interface, "original_path", "NodeSocketString", "")
        _new_input(interface, "Channel Affine Matrix", "NodeSocketMatrix")

        group_input = nodes.new("NodeGroupInput")
        group_input.name = "Group Input"
        group_input.location = (-760, 80)
        group_input.width = 150

        group_output = nodes.new("NodeGroupOutput")
        group_output.name = "Group Output"
        group_output.location = (2010, -150)
        group_output.is_active_output = True

        format_string = nodes.new("FunctionNodeFormatString")
        format_string.name = "Format String"
        format_string.location = (-575, -15)
        format_string.width = 410
        format_string.format_items.clear()
        for item_type, name in (
            ("STRING", "cache_dir"),
            ("STRING", "dataset_hash"),
            ("INT", "scale"),
            ("INT", "resolution"),
            ("INT", "channel_ix"),
            ("INT", "t"),
        ):
            format_string.format_items.new(item_type, name)

        links.new(group_input.outputs["template_str"], format_string.inputs["Format"])
        links.new(group_input.outputs["cache_dir"], format_string.inputs["cache_dir"])
        links.new(
            group_input.outputs["dataset_hash"], format_string.inputs["dataset_hash"]
        )
        links.new(group_input.outputs["scale"], format_string.inputs["scale"])
        links.new(group_input.outputs["resolution"], format_string.inputs["resolution"])
        links.new(group_input.outputs["channel_ix"], format_string.inputs["channel_ix"])
        links.new(group_input.outputs["Frame"], format_string.inputs["t"])

        obj_suffix = nodes.new("FunctionNodeInputString")
        obj_suffix.name = "OBJ Suffix"
        obj_suffix.location = (-130, -150)
        obj_suffix.string = ".obj"

        obj_path = nodes.new("GeometryNodeStringJoin")
        obj_path.name = "OBJ Path"
        obj_path.location = (60, -125)
        obj_path.inputs["Delimiter"].default_value = ""
        links.new(obj_suffix.outputs["String"], obj_path.inputs["Strings"])
        links.new(format_string.outputs["String"], obj_path.inputs["Strings"])

        import_obj = nodes.new("GeometryNodeImportOBJ")
        import_obj.name = "Import OBJ"
        import_obj.location = (275, -140)
        links.new(obj_path.outputs["String"], import_obj.inputs["Path"])

        csv_suffix = nodes.new("FunctionNodeInputString")
        csv_suffix.name = "CSV Suffix"
        csv_suffix.location = (-130, -240)
        csv_suffix.string = ".csv"

        csv_path = nodes.new("GeometryNodeStringJoin")
        csv_path.name = "CSV Path"
        csv_path.location = (60, -215)
        csv_path.inputs["Delimiter"].default_value = ""
        links.new(csv_suffix.outputs["String"], csv_path.inputs["Strings"])
        links.new(format_string.outputs["String"], csv_path.inputs["Strings"])

        import_csv = nodes.new("GeometryNodeImportCSV")
        import_csv.name = "Import CSV"
        import_csv.location = (275, -230)
        import_csv.inputs["Delimiter"].default_value = ","
        links.new(csv_path.outputs["String"], import_csv.inputs["Path"])

        foreach_in = nodes.new("GeometryNodeForeachGeometryElementInput")
        foreach_in.name = "For Each Mesh Island"
        foreach_in.location = (710, -110)
        foreach_in.inputs["Selection"].default_value = True
        links.new(import_obj.outputs["Instances"], foreach_in.inputs[0])

        foreach_out = nodes.new("GeometryNodeForeachGeometryElementOutput")
        foreach_out.name = "Store Object IDs"
        foreach_out.location = (1620, -105)
        foreach_out.domain = "INSTANCE"
        foreach_out.generation_items.clear()
        foreach_out.generation_items.new("GEOMETRY", "Geometry")
        foreach_out.generation_items[0].domain = "POINT"
        foreach_out.input_items.clear()
        foreach_out.main_items.clear()
        foreach_in.pair_with_output(foreach_out)

        named_oid = nodes.new("GeometryNodeInputNamedAttribute")
        named_oid.name = "CSV oid"
        named_oid.location = (960, -245)
        named_oid.data_type = "INT"
        named_oid.inputs["Name"].default_value = "oid"

        sample_oid = nodes.new("GeometryNodeSampleIndex")
        sample_oid.name = "Sample oid"
        sample_oid.location = (1175, -235)
        sample_oid.clamp = False
        sample_oid.data_type = "INT"
        sample_oid.domain = "POINT"
        links.new(import_csv.outputs["Point Cloud"], sample_oid.inputs[0])
        links.new(named_oid.outputs["Attribute"], sample_oid.inputs[1])
        links.new(foreach_in.outputs["Index"], sample_oid.inputs[2])

        store_oid = nodes.new("GeometryNodeStoreNamedAttribute")
        store_oid.name = "Store oid"
        store_oid.location = (1430, -110)
        store_oid.data_type = "INT"
        store_oid.domain = "POINT"
        store_oid.inputs["Selection"].default_value = True
        store_oid.inputs["Name"].default_value = "oid"
        links.new(foreach_in.outputs["Element"], store_oid.inputs[0])
        links.new(sample_oid.outputs["Value"], store_oid.inputs[3])
        links.new(store_oid.outputs["Geometry"], foreach_out.inputs[1])

        transform_geometry = nodes.new("GeometryNodeTransform")
        transform_geometry.name = "Apply Channel Affine"
        transform_geometry.location = (1810, -105)
        transform_geometry.inputs[1].default_value = "Matrix"
        links.new(foreach_out.outputs[2], transform_geometry.inputs["Geometry"])
        links.new(
            group_input.outputs["Channel Affine Matrix"],
            transform_geometry.inputs["Transform"],
        )

        include_switch = nodes.new("GeometryNodeSwitch")
        include_switch.name = "Include Switch"
        include_switch.location = (2030, -150)
        include_switch.input_type = "GEOMETRY"
        links.new(group_input.outputs["Include"], include_switch.inputs["Switch"])
        links.new(transform_geometry.outputs["Geometry"], include_switch.inputs["True"])
        links.new(include_switch.outputs["Output"], group_output.inputs["Geometry"])
        group_output.location = (2210, -150)

        return node_group


def test_import_microscopy_meshes_node_group(snapshot):
    with g.tree("Import Microscopy Meshes") as tree:
        include = tree.inputs.boolean("Include")
        template_str = tree.inputs.string("template_str")
        to_format = {
            "cache_dir": tree.inputs.string("cache_dir"),
            "dataset_hash": tree.inputs.string("dataset_hash"),
            **{
                x: tree.inputs.integer(x) for x in ["scale", "resolution", "channel_ix"]
            },
            "Frame": tree.inputs.integer("t"),
        }
        _ = tree.inputs.string("original_path")
        affine_mat = tree.inputs.matrix("Channel Affine Matrix")

        string = g.FormatString(template_str, to_format)

        csv = g.ImportCSV(
            g.JoinStrings(strings=(string, g.String(".csv"))), delimiter=","
        )
        obj = g.ImportOBJ(g.JoinStrings(strings=(string, g.String(".obj"))))

        zone = g.ForEachGeometryElementZone()
        zone.output.node.domain = "INSTANCE"
        obj >> zone.input.i.geometry
        sna = g.StoreNamedAttribute.point.integer(
            zone.input.o.element,
            name="old",
            value=g.SampleIndex.point.integer(
                geometry=csv,
                value=g.NamedAttribute.integer("old"),
                index=zone.index,
            ),
        )

        sna.o.geometry >> zone.output.i.generation_0
        (
            zone.output.o.geometry
            >> g.TransformGeometry(mode="Matrix", transform=affine_mat)
            >> g.Switch.geometry(include, None, ...)
            >> tree.outputs.geometry()
        )
    assert snapshot == tree._repr_markdown_()


def test_import_microscopy_volume_nodebpy_node_group(snapshot):
    with g.tree() as tree:
        grid_name = tree.inputs.string("Grid Name")
        normalized = tree.inputs.boolean("Normalized", True)
        min = tree.inputs.float("VDB Minimum", 0.0)
        max = tree.inputs.float("VDB Maximum", 1.0)
        original_max = tree.inputs.float("Original Maximum", 1.0)
        include = tree.inputs.boolean("Include")
        string = tree.inputs.string("template_str")

        to_format = {
            "cache_dir": tree.inputs.string("cache_dir"),
            "dataset_has": tree.inputs.string("dataset_hash"),
            **{
                x: tree.inputs.integer(x)
                for x in ["scale", "x", "y", "z", "channel_ix"]
            },
            "t": tree.inputs.integer("Frame"),
        }

        _ = tree.inputs.string("original_path")
        affine_mat = tree.inputs.matrix("Channel Affine Matrix")

        vdb = g.ImportVDB(g.FormatString(string, to_format))
        with g.Frame("Normalize Grid"):
            grid = g.GetNamedGrid.float(vdb, grid_name).o.grid
            grid_normalised = g.MapRange.float(grid, min, max, 0.0, 1.0)
            grid = normalized.switch.float(
                grid_normalised * original_max,
                grid_normalised,
            )
            grid = g.SetGridTransform.float(grid, affine_mat)
        volume = g.StoreNamedGrid(vdb, grid_name, grid)
        volume = include.switch.geometry(None, volume)
        volume >> tree.outputs.geometry("Volume")
        (
            g.Switch.float(include, None, grid)
            >> tree.outputs.float("Grid", structure_type="GRID")
        )

    assert snapshot == tree._repr_markdown_()


def test_import_microscopy_volume_node_group():
    GROUP_NAME = "Import Microscopy Volume"

    def _set_common_socket_defaults(socket):
        socket.attribute_domain = "POINT"
        if hasattr(socket, "default_input"):
            socket.default_input = "VALUE"
        if hasattr(socket, "structure_type"):
            socket.structure_type = "AUTO"

    def _new_input(interface, name, socket_type, default=None):
        socket = interface.new_socket(
            name=name, in_out="INPUT", socket_type=socket_type
        )
        _set_common_socket_defaults(socket)
        if default is not None:
            socket.default_value = default
        return socket

    def _new_output(interface, name, socket_type, default=None):
        socket = interface.new_socket(
            name=name, in_out="OUTPUT", socket_type=socket_type
        )
        _set_common_socket_defaults(socket)
        if default is not None:
            socket.default_value = default
        return socket

    node_group = bpy.data.node_groups.get(GROUP_NAME)
    if node_group:
        return node_group

    node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name=GROUP_NAME)
    node_group.color_tag = "NONE"
    node_group.description = ""
    node_group.default_group_node_width = 140
    node_group.is_modifier = True
    node_group.show_modifier_manage_panel = True

    links = node_group.links
    nodes = node_group.nodes
    interface = node_group.interface

    _new_output(interface, "Volume", "NodeSocketGeometry")
    _new_output(interface, "Grid", "NodeSocketFloat", 0.0)

    _new_input(interface, "Grid Name", "NodeSocketString", "data")
    _new_input(interface, "Normalized", "NodeSocketBool", True)

    vdb_minimum_socket = _new_input(interface, "VDB Minimum", "NodeSocketFloat", 0.0)
    vdb_minimum_socket.min_value = -10000.0
    vdb_minimum_socket.max_value = 10000.0

    vdb_maximum_socket = _new_input(interface, "VDB Maximum", "NodeSocketFloat", 1.0)
    vdb_maximum_socket.min_value = -10000.0
    vdb_maximum_socket.max_value = 10000.0

    _new_input(interface, "Original Maximum", "NodeSocketFloat", 1.0)
    _new_input(interface, "Include", "NodeSocketBool", False)

    _new_input(interface, "template_str", "NodeSocketString", "")
    _new_input(interface, "cache_dir", "NodeSocketString", "")
    _new_input(interface, "dataset_hash", "NodeSocketString", "")
    _new_input(interface, "scale", "NodeSocketInt", 0)
    _new_input(interface, "x", "NodeSocketInt", 0)
    _new_input(interface, "y", "NodeSocketInt", 0)
    _new_input(interface, "z", "NodeSocketInt", 0)
    _new_input(interface, "channel_ix", "NodeSocketInt", 0)
    _new_input(interface, "Frame", "NodeSocketInt", 0)
    _new_input(interface, "original_path", "NodeSocketString", "")
    _new_input(interface, "Channel Affine Matrix", "NodeSocketMatrix")

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.location = (-760, 80)
    group_input.width = 150

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.location = (1560, 20)
    group_output.is_active_output = True

    format_string = nodes.new("FunctionNodeFormatString")
    format_string.name = "Format String"
    format_string.location = (-580, -40)
    format_string.width = 410
    format_string.format_items.clear()
    for item_type, name in (
        ("STRING", "cache_dir"),
        ("STRING", "dataset_hash"),
        ("INT", "scale"),
        ("INT", "x"),
        ("INT", "y"),
        ("INT", "z"),
        ("INT", "channel_ix"),
        ("INT", "t"),
    ):
        format_string.format_items.new(item_type, name)

    links.new(group_input.outputs["template_str"], format_string.inputs["Format"])
    links.new(group_input.outputs["cache_dir"], format_string.inputs["cache_dir"])
    links.new(group_input.outputs["dataset_hash"], format_string.inputs["dataset_hash"])
    links.new(group_input.outputs["scale"], format_string.inputs["scale"])
    links.new(group_input.outputs["x"], format_string.inputs["x"])
    links.new(group_input.outputs["y"], format_string.inputs["y"])
    links.new(group_input.outputs["z"], format_string.inputs["z"])
    links.new(group_input.outputs["channel_ix"], format_string.inputs["channel_ix"])
    links.new(group_input.outputs["Frame"], format_string.inputs["t"])

    import_vdb = nodes.new("GeometryNodeImportVDB")
    import_vdb.name = "Import VDB"
    import_vdb.location = (-100, 160)
    links.new(format_string.outputs["String"], import_vdb.inputs["Path"])

    get_grid = nodes.new("GeometryNodeGetNamedGrid")
    get_grid.name = "Get Named Grid"
    get_grid.location = (90, 250)
    get_grid.data_type = "FLOAT"
    get_grid.inputs["Name"].default_value = "data"
    get_grid.inputs["Remove"].default_value = True
    links.new(import_vdb.outputs["Volume"], get_grid.inputs["Volume"])
    links.new(group_input.outputs["Grid Name"], get_grid.inputs["Name"])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.location = (280, 290)
    map_range.clamp = True
    map_range.data_type = "FLOAT"
    map_range.interpolation_type = "LINEAR"
    map_range.inputs["To Min"].default_value = 0.0
    map_range.inputs["To Max"].default_value = 1.0
    links.new(get_grid.outputs["Grid"], map_range.inputs["Value"])
    links.new(group_input.outputs["VDB Minimum"], map_range.inputs["From Min"])
    links.new(group_input.outputs["VDB Maximum"], map_range.inputs["From Max"])

    store_normalized = nodes.new("GeometryNodeStoreNamedGrid")
    store_normalized.name = "Store Normalized Grid"
    store_normalized.location = (750, -40)
    store_normalized.data_type = "FLOAT"
    links.new(import_vdb.outputs["Volume"], store_normalized.inputs["Volume"])
    links.new(group_input.outputs["Grid Name"], store_normalized.inputs["Name"])
    links.new(map_range.outputs["Result"], store_normalized.inputs["Grid"])

    restore_original_range = nodes.new("ShaderNodeMath")
    restore_original_range.name = "Restore Original Range"
    restore_original_range.location = (560, 265)
    restore_original_range.operation = "MULTIPLY"
    restore_original_range.use_clamp = False
    links.new(map_range.outputs["Result"], restore_original_range.inputs["Value"])
    links.new(group_input.outputs["Original Maximum"], restore_original_range.inputs[1])

    store_original = nodes.new("GeometryNodeStoreNamedGrid")
    store_original.name = "Store Original Grid"
    store_original.location = (760, 105)
    store_original.data_type = "FLOAT"
    links.new(import_vdb.outputs["Volume"], store_original.inputs["Volume"])
    links.new(group_input.outputs["Grid Name"], store_original.inputs["Name"])
    links.new(restore_original_range.outputs["Value"], store_original.inputs["Grid"])

    normalized_switch = nodes.new("GeometryNodeSwitch")
    normalized_switch.name = "Normalized Switch"
    normalized_switch.location = (960, 25)
    normalized_switch.input_type = "GEOMETRY"
    links.new(group_input.outputs["Normalized"], normalized_switch.inputs["Switch"])
    links.new(store_original.outputs["Volume"], normalized_switch.inputs["False"])
    links.new(store_normalized.outputs["Volume"], normalized_switch.inputs["True"])

    include_switch = nodes.new("GeometryNodeSwitch")
    include_switch.name = "Include Switch"
    include_switch.location = (1170, 20)
    include_switch.input_type = "GEOMETRY"
    links.new(group_input.outputs["Include"], include_switch.inputs["Switch"])
    links.new(normalized_switch.outputs["Output"], include_switch.inputs["True"])

    output_grid = nodes.new("GeometryNodeGetNamedGrid")
    output_grid.name = "Output Grid"
    output_grid.location = (1380, 30)
    output_grid.data_type = "FLOAT"
    output_grid.inputs["Remove"].default_value = False
    links.new(include_switch.outputs["Output"], output_grid.inputs["Volume"])
    links.new(group_input.outputs["Grid Name"], output_grid.inputs["Name"])

    set_grid_transform = nodes.new("GeometryNodeSetGridTransform")
    set_grid_transform.name = "Set Channel Affine Transform"
    set_grid_transform.location = (1560, 250)
    set_grid_transform.data_type = "FLOAT"
    links.new(output_grid.outputs["Grid"], set_grid_transform.inputs["Grid"])
    links.new(
        group_input.outputs["Channel Affine Matrix"],
        set_grid_transform.inputs["Transform"],
    )

    store_transformed_grid = nodes.new("GeometryNodeStoreNamedGrid")
    store_transformed_grid.name = "Store Transformed Grid"
    store_transformed_grid.location = (1770, 80)
    store_transformed_grid.data_type = "FLOAT"
    links.new(output_grid.outputs["Volume"], store_transformed_grid.inputs["Volume"])
    links.new(group_input.outputs["Grid Name"], store_transformed_grid.inputs["Name"])
    links.new(set_grid_transform.outputs["Grid"], store_transformed_grid.inputs["Grid"])

    group_output.location = (2020, 20)
    links.new(store_transformed_grid.outputs["Volume"], group_output.inputs["Volume"])
    links.new(set_grid_transform.outputs["Grid"], group_output.inputs["Grid"])

    return node_group
