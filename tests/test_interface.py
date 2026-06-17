from typing import cast, get_args

import bpy
import pytest
from mathutils import Euler

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import (
    BooleanSocket,
    ColorSocket,
    FloatSocket,
    FloatSocketList,
    IntegerSocket,
    MatrixSocket,
    RotationSocket,
    Socket,
    StringSocket,
    VectorSocket,
    VectorSocketList,
)
from nodebpy.nodes.compositor import CombineXYZ
from nodebpy.nodes.geometry import GetListItem, ObjectInfo, SortList
from nodebpy.types import SOCKET_TYPES

# ---------------------------------------------------------------------------
# Geometry tree — existing test
# ---------------------------------------------------------------------------


def test_geometry_interface():
    with g.tree(arrange="simple") as tree:
        # sockets are ordered by the order they are created, so to have "Position"
        # at the top under geometry we need to call it first rather than later in the tree
        # like the inputs for the transform
        geo = tree.inputs.geometry()
        pos = tree.inputs.vector("Position", default_input="POSITION")

        set_pos = g.SetPosition(
            geo,
            position=g.CombineTransform(
                tree.inputs.vector("Translation") * tree.inputs.float("Scale", 1.0),
                tree.inputs.rotation("Rotation"),
                tree.inputs.vector("Scale"),
            )
            @ pos,
        )

        assert set_pos.node.inputs[0].links
        assert set_pos.node.inputs[0].links[0].from_node == geo.node


# ---------------------------------------------------------------------------
# Geometry tree — socket types
# ---------------------------------------------------------------------------


def test_geometry_scalar_sockets():
    """Float, Int, and Boolean sockets are created with correct names and defaults."""
    with g.tree(arrange=None) as tree:
        f = tree.inputs.float("Value", default_value=2.5)
        i = tree.inputs.integer("Count", default_value=4)
        b = tree.inputs.boolean("Enabled", default_value=True)

    assert isinstance(f, Socket)
    assert isinstance(i, Socket)
    assert isinstance(b, Socket)
    assert f._interface_socket.name == "Value"
    assert i._interface_socket.name == "Count"
    assert b._interface_socket.name == "Enabled"
    assert f._interface_socket.default_value == pytest.approx(2.5)
    assert i._interface_socket.default_value == 4
    assert b._interface_socket.default_value is True


def test_geometry_vector_sockets():
    """Vector, Rotation, and Matrix sockets are created correctly."""
    with g.tree(arrange=None) as tree:
        v = tree.inputs.vector("Direction", (1.0, 0.0, 0.0))
        r = tree.inputs.rotation("Rotation")
        m = tree.inputs.matrix("Transform")

    assert v._interface_socket.name == "Direction"
    assert r._interface_socket.name == "Rotation"
    assert m._interface_socket.name == "Transform"
    assert v._interface_socket.socket_type == "NodeSocketVector"
    assert r._interface_socket.socket_type == "NodeSocketRotation"
    assert m._interface_socket.socket_type == "NodeSocketMatrix"


def test_geometry_string_socket():
    with g.tree(arrange=None) as tree:
        ss = tree.inputs.string("Label", default_value="hello")

    assert ss._interface_socket.name == "Label"
    assert ss._interface_socket.default_value == "hello"


def test_geometry_menu_socket():
    with g.tree(arrange=None) as tree:
        menu = tree.inputs.menu("Mode")

    assert menu._interface_socket.name == "Mode"
    assert menu._interface_socket.socket_type == "NodeSocketMenu"


def test_geometry_datablock_sockets():
    """Object, Collection, Material, and Image sockets are created correctly."""
    with g.tree(arrange=None) as tree:
        obj = tree.inputs.object("Object")
        col = tree.inputs.collection("Collection")
        mat = tree.inputs.material("Material")
        img = tree.inputs.image("Image")

    assert obj._interface_socket.socket_type == "NodeSocketObject"
    assert col._interface_socket.socket_type == "NodeSocketCollection"
    assert mat._interface_socket.socket_type == "NodeSocketMaterial"
    assert img._interface_socket.socket_type == "NodeSocketImage"


def test_geometry_bundle_and_closure_sockets():
    with g.tree(arrange=None) as tree:
        bundle = tree.inputs.bundle("Bundle")
        closure = tree.inputs.closure("Closure")

    assert bundle._interface_socket.socket_type == "NodeSocketBundle"
    assert closure._interface_socket.socket_type == "NodeSocketClosure"


def test_geometry_color_socket():
    with g.tree(arrange=None) as tree:
        col = tree.inputs.color("Tint", (0.5, 0.1, 0.9, 1.0))

    assert col._interface_socket.name == "Tint"
    assert col._interface_socket.default_value[0] == pytest.approx(0.5)
    assert col._interface_socket.default_value[2] == pytest.approx(0.9)


# ---------------------------------------------------------------------------
# Socket options
# ---------------------------------------------------------------------------


def test_float_subtype_and_limits():
    with g.tree(arrange=None) as tree:
        f = tree.inputs.float(
            "Factor",
            default_value=0.5,
            min_value=0.0,
            max_value=1.0,
            subtype="FACTOR",
        )

    assert f._interface_socket.default_value == pytest.approx(0.5)
    assert f._interface_socket.min_value == pytest.approx(0.0)
    assert f._interface_socket.max_value == pytest.approx(1.0)
    assert f._interface_socket.subtype == "FACTOR"


def test_integer_limits():
    with g.tree(arrange=None) as tree:
        i = tree.inputs.integer("Count", default_value=10, min_value=1, max_value=100)

    assert i._interface_socket.default_value == 10
    assert i._interface_socket.min_value == 1
    assert i._interface_socket.max_value == 100


def test_socket_description():
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry", description="The input mesh")
        f = tree.inputs.float("Scale", description="Uniform scale factor")

    assert geo._interface_socket.description == "The input mesh"
    assert f._interface_socket.description == "Uniform scale factor"


def test_socket_vector_default_input():
    with g.tree(arrange=None) as tree:
        pos = tree.inputs.vector("Position", default_input="POSITION")
        normal = tree.inputs.vector("Normal", default_input="NORMAL")
        out = tree.outputs.vector()

    assert pos._interface_socket.default_input == "POSITION"
    assert normal._interface_socket.default_input == "NORMAL"
    assert out._default_input_socket == out.socket


def test_socket_hide_value():
    with g.tree(arrange=None) as tree:
        f = tree.inputs.float("Hidden", hide_value=True)
        i = tree.inputs.integer("Visible")

    assert f._interface_socket.hide_value is True
    assert i._interface_socket.hide_value is False


def test_socket_menu_expanded():
    with g.tree(arrange=None) as tree:
        menu = tree.inputs.menu("Mode", expanded=True)

    assert menu._interface_socket.menu_expanded is True


def test_integer_percentage_subtype():
    with g.tree(arrange=None) as tree:
        pct = tree.inputs.integer("Progress", default_value=50, subtype="PERCENTAGE")

    assert pct._interface_socket.subtype == "PERCENTAGE"


def test_socket_vector_subtype():
    with g.tree(arrange=None) as tree:
        vel = tree.inputs.vector("Velocity", subtype="VELOCITY")

    assert vel._interface_socket.subtype == "VELOCITY"


# ---------------------------------------------------------------------------
# Output sockets
# ---------------------------------------------------------------------------


def test_geometry_output_sockets():
    with g.tree(arrange=None) as tree:
        geo_out = tree.outputs.geometry()
        f_out = tree.outputs.float("Score")
        b_out = tree.outputs.boolean("Valid")

    assert geo_out._interface_socket.in_out == "OUTPUT"
    assert f_out._interface_socket.in_out == "OUTPUT"
    assert b_out._interface_socket.in_out == "OUTPUT"
    assert f_out._interface_socket.name == "Score"


def test_input_and_output_same_name_independent():
    """An input and output socket with the same name are separate interface items."""
    with g.tree(arrange=None) as tree:
        geo_in = tree.inputs.geometry("Geometry")
        geo_out = tree.outputs.geometry("Geometry")

    assert geo_in._interface_socket.in_out == "INPUT"
    assert geo_out._interface_socket.in_out == "OUTPUT"
    assert geo_in._interface_socket is not geo_out._interface_socket


# ---------------------------------------------------------------------------
# Linkability
# ---------------------------------------------------------------------------


def test_geometry_socket_links_to_node():
    """Socket returned by factory method can be wired directly into a node."""
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()

        set_pos = g.SetPosition(geo)
        set_pos >> out

    assert set_pos.node.inputs[0].links
    assert set_pos.node.inputs[0].links[0].from_node
    assert set_pos.node.inputs[0].links[0].from_node.name == "Group Input"


def test_geometry_float_socket_in_expression():
    """Float socket participates in arithmetic expressions."""
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry()
        scale = tree.inputs.float("Scale", default_value=2.0)
        out = tree.outputs.geometry()

        (
            g.SetPosition(
                geo,
                position=g.Position() * scale,
            )
            >> out
        )

    assert scale._interface_socket.default_value == pytest.approx(2.0)


def test_multiple_sockets_link_independently():
    """Two separate input sockets wire to different node inputs."""
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry()
        offset = tree.inputs.vector("Offset")
        out = tree.outputs.geometry()

        g.SetPosition(geo, offset=offset) >> out

    assert geo._interface_socket.name == "Geometry"
    assert offset._interface_socket.name == "Offset"


# ---------------------------------------------------------------------------
# Panels with method API
# ---------------------------------------------------------------------------


def test_panel_with_socket_methods():
    """Sockets created inside a panel() context are parented to that panel."""
    with g.tree(arrange=None) as tree:
        tree.inputs.geometry()
        with tree.inputs.panel("Settings"):
            tree.inputs.float("Scale", 1.0)
            tree.inputs.integer("Count", 3)

    items = list(tree.tree.interface.items_tree)
    panels = [i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)]
    assert len(panels) == 1
    assert panels[0].name == "Settings"

    scale = next(i for i in items if getattr(i, "name", None) == "Scale")
    count = next(i for i in items if getattr(i, "name", None) == "Count")
    geo = next(i for i in items if getattr(i, "name", None) == "Geometry")
    assert scale.parent == panels[0]
    assert count.parent == panels[0]
    assert geo.parent != panels[0]


def test_panel_default_closed_with_method_api():
    with g.tree(arrange=None) as tree:
        with tree.inputs.panel("Advanced", default_closed=True):
            tree.inputs.float("Threshold", 0.1)

    items = list(tree.tree.interface.items_tree)
    panel = next(i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel))
    assert panel.default_closed is True


def test_multiple_panels_with_method_api():
    with g.tree(arrange=None) as tree:
        with tree.inputs.panel("Transform"):
            tree.inputs.vector("Translation")
            tree.inputs.rotation("Rotation")
        with tree.inputs.panel("Appearance"):
            tree.inputs.color("Color")
            tree.inputs.float("Roughness", 0.5)

    items = list(tree.tree.interface.items_tree)
    panels = [i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)]
    assert {p.name for p in panels} == {"Transform", "Appearance"}

    color = next(i for i in items if getattr(i, "name", None) == "Color")
    translation = next(i for i in items if getattr(i, "name", None) == "Translation")
    assert color.parent.name == "Appearance"
    assert translation.parent.name == "Transform"


# ---------------------------------------------------------------------------
# Shader tree
# ---------------------------------------------------------------------------


def test_shader_interface_basic():
    with s.tree(arrange=None) as tree:
        base_color = tree.inputs.color("Color", (0.8, 0.2, 0.2, 1.0))
        metallic = tree.inputs.float("Metallic", 0.0, min_value=0.0, max_value=1.0)
        roughness = tree.inputs.float("Roughness", 0.5, min_value=0.0, max_value=1.0)
        shader_out = tree.outputs.shader("Shader")

        prin = s.PrincipledBSDF(
            base_color=base_color,
            metallic=metallic,
            roughness=roughness,
        )
        prin >> shader_out

    assert shader_out._interface_socket.in_out == "OUTPUT"
    assert shader_out._interface_socket.socket_type == "NodeSocketShader"
    assert base_color._interface_socket.default_value[0] == pytest.approx(0.8)
    assert metallic._interface_socket.max_value == pytest.approx(1.0)


def test_shader_vector_input():
    """Vector sockets are valid in shader trees (default_input is geometry-tree-only)."""
    with s.tree(arrange=None) as tree:
        normal = tree.inputs.vector("Normal")
        shader_out = tree.outputs.shader()

        s.PrincipledBSDF(normal=normal) >> shader_out

    assert normal._interface_socket.socket_type == "NodeSocketVector"
    assert normal._interface_socket.name == "Normal"


def test_shader_int_and_boolean_inputs():
    with s.tree(arrange=None) as tree:
        samples = tree.inputs.integer("Samples", 128, min_value=1, max_value=4096)
        enabled = tree.inputs.boolean("Enabled", default_value=True)
        shader_out = tree.outputs.shader()

        s.PrincipledBSDF() >> shader_out

    assert samples._interface_socket.default_value == 128
    assert samples._interface_socket.min_value == 1
    assert enabled._interface_socket.default_value is True


def test_shader_float_output():
    with s.tree(arrange=None) as tree:
        shader_out = tree.outputs.shader()
        alpha_out = tree.outputs.float("Alpha")

        prin = s.PrincipledBSDF()
        prin >> shader_out

    assert alpha_out._interface_socket.in_out == "OUTPUT"
    assert alpha_out._interface_socket.socket_type == "NodeSocketFloat"


# ---------------------------------------------------------------------------
# Compositor tree
# ---------------------------------------------------------------------------


def test_compositor_color_and_float_sockets():
    with c.tree(arrange=None) as tree:
        image = tree.inputs.color("Image")
        fac = tree.inputs.float(
            "Factor", default_value=1.0, min_value=0.0, max_value=1.0
        )
        out = tree.outputs.color("Image")

        c.Mix.color(fac, image, c.Blur(image)) >> out

    assert image._interface_socket.socket_type == "NodeSocketColor"
    assert fac._interface_socket.default_value == pytest.approx(1.0)
    assert out._interface_socket.in_out == "OUTPUT"


def test_compositor_vector_socket():
    with c.tree(arrange=None) as tree:
        normal = tree.inputs.vector("Normal")
        out = tree.outputs.color("Image")

        c.Blur(normal) >> out

    assert normal._interface_socket.socket_type == "NodeSocketVector"


def test_compositor_menu_socket():
    with c.tree(arrange=None) as tree:
        mode = tree.inputs.menu("Mode", expanded=True)
        image = tree.inputs.color("Image")
        out = tree.outputs.color("Image")

        c.Blur(image) >> out

    assert mode._interface_socket.socket_type == "NodeSocketMenu"
    assert mode._interface_socket.menu_expanded is True


def test_compositor_multiple_outputs():
    with c.tree(arrange=None) as tree:
        image = tree.inputs.color("Image")
        image_out = tree.outputs.color("Image")
        mask_out = tree.outputs.float("Mask")

        c.Blur(image) >> image_out

    assert image_out._interface_socket.in_out == "OUTPUT"
    assert mask_out._interface_socket.in_out == "OUTPUT"
    assert image_out._interface_socket.socket_type == "NodeSocketColor"
    assert mask_out._interface_socket.socket_type == "NodeSocketFloat"


def test_compositor_int_and_boolean_sockets():
    with c.tree(arrange=None) as tree:
        size = tree.inputs.integer("Size", 3, min_value=1, max_value=32)
        enabled = tree.inputs.boolean("Enabled")
        out = tree.outputs.color("Image")

        image = tree.inputs.color("Image")
        c.Blur(image) >> out

    assert size._interface_socket.default_value == 3
    assert size._interface_socket.min_value == 1
    assert enabled._interface_socket.socket_type == "NodeSocketBool"


def test_compositor_panel_with_socket_methods():
    with c.tree(arrange=None) as tree:
        image = tree.inputs.color("Image")
        with tree.inputs.panel("Outline"):
            tree.inputs.float("Threshold", 0.5)
            tree.inputs.color("Color")
        out = tree.outputs.color("Image")

        c.Blur(image) >> out

    items = list(tree.tree.interface.items_tree)
    panels = [i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)]
    assert len(panels) == 1
    assert panels[0].name == "Outline"

    threshold = next(i for i in items if getattr(i, "name", None) == "Threshold")
    color = next(i for i in items if getattr(i, "name", None) == "Color")
    assert threshold.parent == panels[0]
    assert color.parent == panels[0]


def test_socket_accessor():
    with g.tree():
        pos = g.Position()

        with pytest.raises(AttributeError, match="_some_name"):
            pos.o._some_name

    assert pos.i._node == pos.node

    with g.tree() as tree:
        cube = g.Cube()
        sim = g.SimulationZone()
        (
            sim.input.capture(cube)
            >> g.TransformGeometry(translation=g.CombineXYZ(y=sim.delta_time))
            >> sim.output
            >> tree.outputs.geometry("MovedCube")
        )


def test_accessor_slice():
    with g.tree():
        sep = g.SeparateXYZ(g.Position())
        comb = g.CombineXYZ(*sep.o)
        comb2 = g.CombineXYZ()

        sep.o[1] >> comb2.i[2]

        with pytest.raises(IndexError):
            sep.o[3] >> comb2.i.x
        with pytest.raises(IndexError):
            sep.o[0] >> comb2.i[3]

    assert all(input.links for input in comb.i)
    assert all(input.links[0].from_node == sep.node for input in comb.i)
    assert comb2.i.z.links
    assert comb2.i.z.links[0].from_node == sep.node
    assert comb2.i.z.links[0].from_socket == sep.o.y.socket


def test_accessor_slice_matrix():
    with g.tree():
        mat = g.InstanceTransform()
        comb = g.CombineMatrix(*mat.o.transform)

        vec = g.Position()
        vec_comb = g.CombineXYZ(*vec.o.position)

        col = g.Color()
        col_comb = g.CombineColor(*col.o.color)

    assert all(input.links for input in comb.i)
    assert all(
        (input.links[0].from_node.bl_idname == g.SeparateMatrix._bl_idname)
        for input in comb.i
    )
    assert all(input.links for input in vec_comb.i)
    assert all(
        (input.links[0].from_node.bl_idname == g.SeparateXYZ._bl_idname)
        for input in vec_comb.i
    )
    assert all(input.links for input in col_comb.i)
    assert all(
        (input.links[0].from_node.bl_idname == g.SeparateColor._bl_idname)
        for input in col_comb.i
    )


def test_vector_socket_input_indexing():
    """Indexing an input VectorSocket auto-wires a CombineXYZ and returns its component input."""
    with g.tree():
        val = g.Value(5.0)
        set_pos = g.SetPosition()
        val >> set_pos.i.position[1]

    pos_input = set_pos.node.inputs["Position"]
    assert pos_input.links, "CombineXYZ output should be linked to Position"
    combine_node = pos_input.links[0].from_node
    assert combine_node
    assert combine_node.bl_idname == g.CombineXYZ._bl_idname
    y_input = combine_node.inputs[1]
    assert y_input.links, "Value should be linked to CombineXYZ Y input"
    assert y_input.links[0].from_node == val.node


def test_vector_socket_input_indexing_reuse():
    """Multiple index accesses on the same input socket reuse the same CombineXYZ."""
    with g.tree():
        a = g.Value(1.0)
        b = g.Value(2.0)
        set_pos = g.SetPosition()
        a >> set_pos.i.position[0]
        b >> set_pos.i.position[2]

        set_pos2 = g.SetPosition()
        for axis in set_pos2.i.position:
            a >> axis

    pos_input = set_pos.node.inputs["Position"]
    assert pos_input
    assert pos_input.links
    assert len(pos_input.links) == 1, "Only one CombineXYZ should be wired"
    combine_node = pos_input.links[0].from_node
    assert combine_node
    assert combine_node.inputs[0].links
    assert combine_node.inputs[0].links[0].from_node == a.node
    assert combine_node.inputs[2].links
    assert combine_node.inputs[2].links[0].from_node == b.node
    assert set_pos2.i.position.links[0].from_node.bl_idname == g.CombineXYZ._bl_idname  # ty: ignore[unresolved-attribute]


def test_vector_socket_output_iteration():
    """Iterating an output VectorSocket yields X, Y, Z via a single SeparateXYZ."""
    with g.tree():
        pos = g.Position().o.position
        components = list(pos)
        assert pos[2].name == "Z"
        assert all(isinstance(x, FloatSocket) for x in pos)
        assert all(isinstance(x, FloatSocket) for x in pos[:2])

    assert len(components) == 3
    sep_node = components[0].socket.node
    assert sep_node
    assert sep_node.bl_idname == g.SeparateXYZ._bl_idname
    assert all(c.socket.node == sep_node for c in components)
    assert not pos._is_compositor_tree
    assert not pos._is_shader_tree


def test_vector_socket_output_len():
    with g.tree():
        vec = g.Position()
        assert len(vec.o.position) == 3


def test_color_socket_input_indexing():
    """Indexing an input ColorSocket auto-wires a CombineColor and returns its component input."""
    with g.tree():
        val = g.Value(0.5)
        sgpc = g.SetGreasePencilColor()
        val >> sgpc.i.color[2]
        val >> sgpc.i.color[1]

    a_input = sgpc.node.inputs["Color"]
    assert a_input.links
    combine_node = a_input.links[0].from_node
    assert combine_node
    assert combine_node.bl_idname == g.CombineColor._bl_idname
    assert combine_node.inputs[1].links
    assert combine_node.inputs[1].links[0].from_node == val.node
    assert combine_node.inputs[2].links
    assert combine_node.inputs[2].links[0].from_node == val.node
    assert (
        combine_node.inputs[1].links[0].from_node
        == combine_node.inputs[2].links[0].from_node
    )


def test_color_socket_input_shader():
    with s.tree():
        sep = s.SeparateColor()

        for i, axis in enumerate(sep.i.color):
            s.Value(i) >> axis

        with pytest.raises(TypeError):
            sep.i.color.a

        comb = s.CombineColor()
        with pytest.raises(TypeError):
            comb.o.color.a

        assert len(comb.o.color) == 3
        assert sep.i.color[2].name == "Blue"
        assert sep.i.color[0].name == "Red"

    assert sep.i.color.links[0].from_node
    assert sep.i.color.links[0].from_node.bl_idname == s.CombineColor._bl_idname
    assert len(sep.i.color) == 3


def test_color_socket_input_compositor():
    with c.tree():
        image = c.SeparateColor().i.image

        for i, axis in enumerate(image):
            c.Value(i) >> axis

    assert image.links[0].from_node
    assert image.links[0].from_node.bl_idname == c.CombineColor._bl_idname
    assert image._is_compositor_tree


def test_color_socket_output_iteration():
    """Iterating an output ColorSocket yields R, G, B, A via a single SeparateColor."""
    with g.tree():
        col = g.Color()
        components = list(col.o.color)

    assert len(components) == 4
    sep_node = components[0].socket.node
    assert sep_node
    assert sep_node.bl_idname == g.SeparateColor._bl_idname
    assert all(c.socket.node == sep_node for c in components)


def test_color_socket_output_len():
    with g.tree():
        col = g.Color()
        assert len(col.o.color) == 4


def test_matrix_socket_input_indexing():
    """Indexing an input MatrixSocket auto-wires a CombineMatrix and returns its component input."""
    with g.tree():
        val = g.Value(1.0)
        transform = g.SetInstanceTransform()
        val >> transform.i.transform[0]
        val >> transform.i.transform[1]

        for i, input in enumerate(transform.i.transform):
            if i < 2:
                assert input.links
                assert input.links[0].from_node == val.node
            else:
                assert not input.links
            input.socket.default_value = i
            assert input.socket.default_value == i

    transform_input = transform.node.inputs["Transform"]
    assert transform_input.links
    combine_node = transform_input.links[0].from_node
    assert combine_node
    assert combine_node.bl_idname == g.CombineMatrix._bl_idname
    assert combine_node.inputs[0].links
    assert combine_node.inputs[0].links[0].from_node == val.node
    assert combine_node.inputs[1].links
    assert (
        combine_node.inputs[1].links[0].from_node
        == combine_node.inputs[0].links[0].from_node
    )


def test_matrix_socket_input_slice():
    """Slicing an input MatrixSocket returns component inputs for that range."""
    with g.tree():
        transform = g.SetInstanceTransform()
        components = transform.i.transform[0:3]

    assert len(components) == 3
    combine_node = transform.node.inputs["Transform"].links[0].from_node
    assert combine_node
    assert combine_node.bl_idname == g.CombineMatrix._bl_idname


def test_matrix_socket_output_iteration():
    """Iterating an output MatrixSocket yields all 16 elements via a single SeparateMatrix."""
    with g.tree():
        mat = g.InstanceTransform()
        components = list(mat.o.transform)
        comb = g.CombineMatrix(*components)
        math = mat.o.transform[3] + 3

    assert len(components) == 16
    sep_node = components[0].socket.node
    assert all(
        input.links[0].from_node.bl_idname == g.SeparateMatrix._bl_idname
        for input in comb.i
    )
    assert sep_node
    assert sep_node.bl_idname == g.SeparateMatrix._bl_idname
    assert all(c.socket.node == sep_node for c in components)
    assert math.builder_node.i[0].links[0].from_node == comb.i[0].links[0].from_node


def test_accessor_rotation():
    with g.tree():
        rot = g.AlignRotationToVector()
        quat = g.RotationToQuaternion(rot.o.rotation)
        assert quat.i[0].links
        rot_to_quat = quat.i[0].links[0].from_node
        assert all(
            axis.node.inputs[0].links[0].from_node == rot_to_quat for axis in quat.o
        )

        eul = rot.o.rotation.to_euler()
        assert isinstance(eul, VectorSocket)
        assert eul.node == rot.o.rotation.to_euler().node


def test_matrix_socket_output_len():
    with g.tree():
        mat = g.InstanceTransform()
        assert len(mat.o.transform) == 16

        assert mat.o.transform.invert().node.bl_idname == g.InvertMatrix._bl_idname
        assert (
            mat.o.transform.transpose().node.bl_idname == g.TransposeMatrix._bl_idname
        )

        assert len(mat.o.transform.links) == 2

        rot = g.Rotation()
        rot.o.rotation.invert().node.bl_idname == g.InvertRotation._bl_idname


def test_socket_default_values():
    with g.tree():
        sep = g.SeparateXYZ()
        assert sep.i.vector.links == []
        g.Vector() >> sep
        assert sep.i.vector.links != []
        assert len(sep.i.vector.links) == 1

        rot = g.RotationToEuler()
        assert rot.i.rotation.default_value == Euler([0.0, 0.0, 0.0])
        rot.i.rotation.default_value = Euler([1.0, 1.0, 1.0])
        assert rot.i.rotation.default_value == Euler([1.0, 1.0, 1.0])

        sep = g.SeparateColor()
        assert sep.i.color.default_value == [1.0, 1.0, 1.0, 1.0]
        sep.i.color.default_value = [0.0, 0.0, 0.0, 1.0]
        assert sep.i.color.default_value == [0.0, 0.0, 0.0, 1.0]

        n = g.BooleanMath.l_not()
        assert n.i.boolean.default_value is False
        n.i.boolean.default_value = True
        assert n.i.boolean.default_value is True

        string = g.StringLength()
        assert string.i.string.default_value == ""
        string.i.string.default_value = "Some string"
        assert string.i.string.default_value == "Some string"

        mat = g.SetMaterial().i.material
        assert mat.default_value is None
        mat.default_value = bpy.data.materials.new("New Material")
        assert mat.default_value.name == "New Material"

        image = g.ImageInfo().i.image
        assert image.default_value is None
        image.default_value = bpy.data.images.new("New Image", width=1024, height=1024)
        assert image.default_value == bpy.data.images["New Image"]

        collection = g.CollectionInfo()
        assert collection.i.collection.default_value is None
        collection.i.collection.default_value = bpy.data.collections.new(
            "New Collection"
        )
        assert (
            collection.i.collection.default_value
            == bpy.data.collections["New Collection"]
        )

        obj = g.ObjectInfo()
        assert obj.i.object.default_value is None
        obj.i.object.default_value = bpy.data.objects["Cube"]
        assert obj.i.object.default_value == bpy.data.objects["Cube"]


def test_boolean_socket_switches():
    with g.tree() as tree:
        i = tree.inputs.boolean("Enabled", default_value=True)

        for name in get_args(SOCKET_TYPES):
            method = name.lower().replace("int", "integer").replace("rgba", "color")
            if method == "shader":
                continue
            sock = getattr(i.switch, method)()
            assert sock.node.input_type == name


def _assert_integer_method(result, operation):
    node = cast(g.IntegerMath, result.builder_node)
    assert isinstance(node, g.IntegerMath)
    assert node.operation == operation


def test_integer_socket_methods():
    with g.tree():
        val = g.Integer().o.integer

        result = val.sign()
        node = cast(g.IntegerMath, result.builder_node)
        assert isinstance(node, g.IntegerMath)
        assert node.operation == "SIGN"
        assert node.i.value.links[0].from_socket == val.socket

        result = val.negate()
        node = cast(g.IntegerMath, result.builder_node)
        assert isinstance(node, g.IntegerMath)
        assert node.operation == "NEGATE"
        assert node.i.value.links[0].from_socket == val.socket
        assert len(val.links) == 2

        string = val.to_string()
        node = cast(g.ValueToString, string.builder_node)
        assert isinstance(node, g.ValueToString)
        assert node.data_type == "INT"

        for method, operation in [
            ("sign", "SIGN"),
            ("negate", "NEGATE"),
            ("abs", "ABSOLUTE"),
            ("mul_add", "MULTIPLY_ADD"),
            ("power", "POWER"),
        ]:
            result = getattr(val, method)()
            _assert_integer_method(result, operation)


def _assert_method(result, expected_operation):
    assert result.node.bl_idname == g.Math._bl_idname
    assert result.node.operation == expected_operation


def test_float_socket_methods(snapshot):
    with g.tree() as tree:
        val = g.Float().o.value
        b = g.Float().o.value

        result = val.negate()
        _assert_method(result, "MULTIPLY")
        assert result.node.inputs[1].default_value == pytest.approx(-1.0)
        assert result.node.inputs[0].links[0].from_node == val.node
        assert len(val.links) == 1

        string = val.to_string(3)
        assert string.builder_node.i.decimals.default_value == 3
        assert isinstance(string.builder_node, g.ValueToString)

        for method, operation in [
            ("sign", "SIGN"),
            ("min", "MINIMUM"),
            ("max", "MAXIMUM"),
            ("sin", "SINE"),
            ("cos", "COSINE"),
            ("tan", "TANGENT"),
            ("asin", "ARCSINE"),
            ("acos", "ARCCOSINE"),
            ("atan", "ARCTANGENT"),
            ("sinh", "SINH"),
            ("cosh", "COSH"),
            ("tanh", "TANH"),
            ("atan2", "ARCTAN2"),
            # ("asinh", "ARCSINH"),
            # ("acosh", "ARCCOSH"),
            # ("atanh", "ARCTANH"),
            ("sqrt", "SQRT"),
            ("power", "POWER"),
            ("log", "LOGARITHM"),
            ("exp", "EXPONENT"),
            ("to_degrees", "DEGREES"),
            ("to_radians", "RADIANS"),
            ("mul_add", "MULTIPLY_ADD"),
            ("ping_pong", "PINGPONG"),
            ("snap", "SNAP"),
            ("truncate", "TRUNC"),
            ("fraction", "FRACT"),
            ("abs", "ABSOLUTE"),
        ]:
            _assert_method(getattr(val, method)(), operation)

    assert snapshot == tree.to_mermaid()


def test_vector_socket_methods(snapshot):
    with g.tree() as tree:
        vec = tree.inputs.vector()
        norm = vec.normalize()
        assert isinstance(norm, VectorSocket)
        assert norm.node.bl_idname == g.VectorMath._bl_idname
        assert norm.node.operation == "NORMALIZE"
        assert norm.socket != vec.normalize().socket

        dot = vec.dot(g.Vector())
        assert isinstance(dot, FloatSocket)
        assert dot.node.bl_idname == g.VectorMath._bl_idname
        assert dot.node.operation == "DOT_PRODUCT"
        assert dot.socket != vec.dot(g.Vector()).socket

        ln = vec.length()
        assert isinstance(ln, FloatSocket)
        assert ln.node.bl_idname == g.VectorMath._bl_idname
        assert ln.node.operation == "LENGTH"
        assert ln.socket != vec.length().socket

        sc = vec.scale(2.0)
        assert isinstance(sc, VectorSocket)
        assert sc.node.bl_idname == g.VectorMath._bl_idname
        assert sc.node.operation == "SCALE"
        assert sc.builder_node.i.scale.default_value == pytest.approx(2.0)
        assert snapshot == tree._repr_markdown_()

        rot = vec.align_rotation()
        assert isinstance(rot, RotationSocket)
        assert rot.node.bl_idname == g.AlignRotationToVector._bl_idname

        rot2 = rot.align_to_vector((1, 0, 0))
        node = cast(g.AlignRotationToVector, rot2.builder_node)
        assert isinstance(node, g.AlignRotationToVector)
        assert node.i.rotation.links[0].from_node == rot.node
        assert node.i.vector.default_value == [1.0, 0.0, 0.0]


def test_vector_socket_input_methods(snapshot):
    with g.tree() as tree:
        setpos = g.SetPosition()
        offset = setpos.i.offset
        assert isinstance(offset, VectorSocket)

        x = offset.x
        assert isinstance(x, FloatSocket)
        assert isinstance(x.builder_node, CombineXYZ)
        y = offset.y
        assert isinstance(y, FloatSocket)
        assert isinstance(y.builder_node, CombineXYZ)
        z = offset.z
        assert isinstance(z, FloatSocket)
        assert isinstance(z.builder_node, CombineXYZ)

        assert x.node == y.node == z.node

    assert snapshot == tree._repr_markdown_()


def test_socket_builder_reference(snapshot):
    with g.tree() as tree:
        position = g.Position()
        pos = position.o.position
        assert pos.builder_node
        assert pos.builder_node.node == position.node

        _node = pos.builder_node.node
        del position
        del pos

        position = g.Position._from_node(_node)
        assert position.node == _node

        par = g.SplineParameter()

        socks = list(par.o[:2])
        assert all(s.builder_node.node == par.node for s in socks)
        assert snapshot == tree._repr_markdown_()


def test_string_socket_methods(snapshot):
    with g.tree() as tree:
        string = tree.inputs.string()

        ew = string.ends_with("test")
        assert isinstance(ew.builder_node, g.MatchString)
        assert ew.builder_node.i.operation.default_value == "Ends With"
        assert ew.builder_node.i.key.default_value == "test"
        assert ew.builder_node.i.string.links[0].from_node == string.node

        con = string.contains("abc")
        assert isinstance(con.builder_node, g.MatchString)
        assert con.builder_node.i.operation.default_value == "Contains"
        assert con.builder_node.i.key.default_value == "abc"
        assert con.builder_node.i.string.links[0].from_node == string.node

        sw = string.starts_with("hello")
        assert isinstance(sw.builder_node, g.MatchString)
        assert sw.builder_node.i.operation.default_value == "Starts With"
        assert sw.builder_node.i.key.default_value == "hello"
        assert sw.builder_node.i.string.links[0].from_node == string.node

        slice = string.slice(1, 4)
        assert isinstance(slice.builder_node, g.SliceString)
        assert slice.builder_node.i.position.default_value == 1
        assert slice.builder_node.i.length.default_value == 4
        assert slice.builder_node.i.string.links[0].from_node == string.node

        rep = string.replace("a", "b")
        assert isinstance(rep.builder_node, g.ReplaceString)
        assert rep.builder_node.i.find.default_value == "a"
        assert rep.builder_node.i.replace.default_value == "b"
        assert rep.builder_node.i.string.links[0].from_node == string.node

        length = string.length()
        assert isinstance(length.builder_node, g.StringLength)
        assert length.builder_node.i.string.links[0].from_node == string.node
        assert isinstance(length, IntegerSocket)

        joined = string + "test"
        node = cast(g.JoinStrings, joined.builder_node)
        assert isinstance(node, g.JoinStrings)
        assert len(node.i.strings.links) == 2
        assert node.i.strings.links[0].from_node == string.node
        assert node.i.strings.links[1].from_node.bl_idname == g.String._bl_idname

        joined = "test" + string
        node = cast(g.JoinStrings, joined.builder_node)
        assert isinstance(node, g.JoinStrings)
        assert len(node.i.strings.links) == 2
        assert node.i.strings.links[0].from_node.bl_idname == g.String._bl_idname
        assert node.i.strings.links[1].from_node == string.node

        join = g.String(",").o.string.join([slice, rep, joined])
        node = cast(g.JoinStrings, join.builder_node)
        assert isinstance(node, g.JoinStrings)
        assert len(node.i.strings.links) == 3

        string.replace("A", "B").slice(1, 2).join(["test"]).slice(2, 3).join(
            ["A", "test"]
        ).length()

        assert len(tree) == 22
        assert snapshot == tree._repr_markdown_()

        reversed = string.reverse()
        assert isinstance(reversed, StringSocket)
        assert reversed.node.bl_idname == g.ReverseString._bl_idname
        assert reversed.builder_node.i.string.links[0].from_node == string.node

        upper = string.uppercase()
        assert isinstance(upper, StringSocket)
        assert upper.node.bl_idname == g.SetStringCase._bl_idname
        assert upper.builder_node.i.case.default_value == "Uppercase"
        assert upper.builder_node.i.string.links[0].from_node == string.node

        lower = string.lowercase()
        assert isinstance(lower, StringSocket)
        assert lower.node.bl_idname == g.SetStringCase._bl_idname
        assert lower.builder_node.i.case.default_value == "Lowercase"
        assert lower.builder_node.i.string.links[0].from_node == string.node


def test_vector_socket_rotate():
    with g.tree():
        vec = g.Position().o.position
        rot = g.AlignRotationToVector().o.rotation

        result = vec.rotate(rot)

    assert isinstance(result, VectorSocket)
    assert result.node.bl_idname == g.RotateVector._bl_idname
    assert result.builder_node.i.vector.links[0].from_node == vec.node
    assert result.builder_node.i.rotation.links[0].from_node == rot.node


def test_vector_socket_transform():
    with g.tree():
        vec = g.Position().o.position
        mat = g.CombineTransform().o.transform

        result = vec.transform(mat)

    assert isinstance(result, VectorSocket)
    assert result.node.bl_idname == g.TransformPoint._bl_idname
    assert result.builder_node.i.vector.links[0].from_node == vec.node
    assert result.builder_node.i.transform.links[0].from_node == mat.node


def test_rotation_socket_rotate():
    with g.tree():
        rot = g.AlignRotationToVector().o.rotation
        result_global = rot.rotate(rot)
        result_local = rot.rotate(rot, rotation_space="LOCAL")

    assert isinstance(result_global, RotationSocket)
    assert result_global.node.bl_idname == g.RotateRotation._bl_idname
    assert result_global.node.rotation_space == "GLOBAL"
    assert result_local.node.rotation_space == "LOCAL"


def test_rotation_socket_to_quaternion():
    with g.tree():
        rot = g.AlignRotationToVector().o.rotation
        w, x, y, z = rot.to_quaternion()

    assert all(isinstance(s, FloatSocket) for s in (w, x, y, z))
    assert w.node == x.node == y.node == z.node
    assert w.node.bl_idname == g.RotationToQuaternion._bl_idname

    with g.tree():
        rot = g.AlignRotationToVector().o.rotation
        quat = rot.to_quaternion()
        assert isinstance(quat.w, FloatSocket)
        assert isinstance(quat.x, FloatSocket)


def test_rotation_socket_to_axis_angle():
    with g.tree():
        rot = g.AlignRotationToVector().o.rotation
        axis, angle = rot.to_axis_angle()

    assert isinstance(axis, VectorSocket)
    assert isinstance(angle, FloatSocket)
    assert axis.node == angle.node
    assert axis.node.bl_idname == g.RotationToAxisAngle._bl_idname

    with g.tree():
        rot = g.AlignRotationToVector().o.rotation
        aa = rot.to_axis_angle()
        assert isinstance(aa.axis, VectorSocket)
        assert isinstance(aa.angle, FloatSocket)


def test_float_socket_mix():
    with g.tree():
        fac = g.Value(0.5).o.value
        a = g.Value(1.0).o.value
        b = g.Value(2.0).o.value
        result = fac.mix.float(a, b)

        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.Mix._bl_idname
        assert result.builder_node.i.factor_float.links[0].from_node == fac.node

        fac = g.Value(0.5).o.value
        result_v = fac.mix.vector((0, 0, 0), (1, 1, 1))
        result_r = fac.mix.rotation(
            g.AlignRotationToVector().o.rotation,
            g.AlignRotationToVector().o.rotation,
        )

        assert isinstance(result_v, VectorSocket)
        assert isinstance(result_r, RotationSocket)

        result = fac.mix.color(g.Color(), g.Mix.color())
        assert isinstance(result, ColorSocket)
        assert result.node.bl_idname == g.Mix._bl_idname
        assert result.builder_node.i.factor_float.links[0].from_node == fac.node


def test_float_socket_to_integer():
    with g.tree():
        val = g.Value(3.7).o.value
        result = val.to_integer()
        result_floor = val.to_integer(rounding_mode="FLOOR")

    assert isinstance(result, IntegerSocket)
    assert result.node.bl_idname == g.FloatToInteger._bl_idname
    assert result.node.rounding_mode == "ROUND"
    assert result_floor.node.rounding_mode == "FLOOR"


def test_float_socket_math_methods():
    with g.tree():
        val = g.Value(4.0).o.value

        result = val.clamp()
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.Clamp._bl_idname
        assert result.node.clamp_type == "MINMAX"
        assert result.builder_node.i.min.default_value == pytest.approx(0.0)
        assert result.builder_node.i.max.default_value == pytest.approx(1.0)
        assert result.builder_node.i.value.links[0].from_node == val.node

        result = val.clamp(-1.0, 1.0)
        assert result.builder_node.i.min.default_value == pytest.approx(-1.0)
        assert result.builder_node.i.max.default_value == pytest.approx(1.0)

        result = val.sqrt()
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.Math._bl_idname
        assert result.node.operation == "SQRT"
        assert result.builder_node.i.value.links[0].from_node == val.node

        result = val.power(2.0)
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.Math._bl_idname
        assert result.node.operation == "POWER"
        assert result.builder_node.i.value_001.default_value == pytest.approx(2.0)

        result = val.floor()
        assert result.node.operation == "FLOOR"

        result = val.ceil()
        assert result.node.operation == "CEIL"

        result = val.round()
        assert result.node.operation == "ROUND"

        result = val.modulo(3.0)
        assert result.node.operation == "FLOORED_MODULO"
        assert result.builder_node.i.value_001.default_value == pytest.approx(3.0)

        result = val.wrap(0.0, 1.0)
        assert result.node.operation == "WRAP"
        assert result.builder_node.i.value_001.default_value == pytest.approx(1.0)
        assert result.builder_node.i.value_002.default_value == pytest.approx(0.0)

        result = val.to_radians()
        assert result.node.operation == "RADIANS"

        result = val.to_degrees()
        assert result.node.operation == "DEGREES"


def test_float_socket_map_range():
    with g.tree():
        val = g.Value(0.5).o.value

        result = val.map_range(0.0, 100.0, 0.0, 1.0)
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.MapRange._bl_idname
        assert result.builder_node.i.value.links[0].from_node == val.node
        assert result.builder_node.i.from_min.default_value == pytest.approx(0.0)
        assert result.builder_node.i.from_max.default_value == pytest.approx(100.0)
        assert result.builder_node.i.to_min.default_value == pytest.approx(0.0)
        assert result.builder_node.i.to_max.default_value == pytest.approx(1.0)

        result_stepped = val.map_range(interpolation_type="STEPPED", steps=8.0)
        assert result_stepped.node.interpolation_type == "STEPPED"
        assert result_stepped.builder_node.i.steps.default_value == pytest.approx(8.0)


def test_float_socket_domain_aggregation():
    with g.tree():
        val = g.Position().o.position.length()

        lo = val.point.min()
        assert isinstance(lo, FloatSocket)
        assert lo.node.bl_idname == g.FieldMinAndMax._bl_idname
        assert lo.builder_node.i.value.links[0].from_node == val.node

        hi = val.edge.max()
        assert isinstance(hi, FloatSocket)
        assert hi.node.bl_idname == g.FieldMinAndMax._bl_idname

        mean = val.point.mean()
        assert isinstance(mean, FloatSocket)
        assert mean.node.bl_idname == g.FieldAverage._bl_idname

        median = val.face.median()
        assert isinstance(median, FloatSocket)
        assert median.node.bl_idname == g.FieldAverage._bl_idname

        std_dev = val.point.std_dev()
        assert isinstance(std_dev, FloatSocket)
        assert std_dev.node.bl_idname == g.FieldVariance._bl_idname

        variance = val.spline.variance()
        assert isinstance(variance, FloatSocket)
        assert variance.node.bl_idname == g.FieldVariance._bl_idname


def test_vector_socket_new_methods():
    with g.tree():
        vec = g.Position().o.position
        other = g.Vector().o.vector

        result = vec.cross(other)
        assert isinstance(result, VectorSocket)
        assert result.node.bl_idname == g.VectorMath._bl_idname
        assert result.node.operation == "CROSS_PRODUCT"
        assert result.builder_node.i.vector.links[0].from_node == vec.node
        assert result.builder_node.i.vector_001.links[0].from_node == other.node

        result = vec.distance(other)
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.VectorMath._bl_idname
        assert result.node.operation == "DISTANCE"

        result = vec.project(other)
        assert isinstance(result, VectorSocket)
        assert result.node.operation == "PROJECT"

        result = vec.reflect(other)
        assert isinstance(result, VectorSocket)
        assert result.node.operation == "REFLECT"

        ftl = g.FieldToList(10)
        veclist = ftl.vector(vec)
        assert ftl.i["VECTOR"].links
        assert ftl.i["VECTOR"].links[0].from_node == vec.node
        sorted = veclist.sort(veclist.length())
        assert isinstance(sorted, VectorSocketList)
        node = sorted.builder_node
        assert isinstance(node, SortList)
        assert node.socket_type == "VECTOR"
        assert node.i.list.links[0].from_node == ftl.node
        assert not node.i.group_id.links
        assert not node.i.selection.links
        assert (
            node.i.sort_weight.links[0].from_node.bl_idname == g.VectorMath._bl_idname
        )

        list = ftl.float(1.0)
        assert isinstance(list, FloatSocketList)
        assert list.node.bl_idname == g.FieldToList._bl_idname


def test_vector_socket_map_range():
    with g.tree():
        vec = g.Position().o.position

        result = vec.map_range((0, 0, 0), (1, 1, 1), (-1, -1, -1), (1, 1, 1))
        assert isinstance(result, VectorSocket)
        assert result.node.bl_idname == g.MapRange._bl_idname
        assert result.builder_node.i.vector.links[0].from_node == vec.node

        result_stepped = vec.map_range(interpolation_type="STEPPED")
        assert result_stepped.node.interpolation_type == "STEPPED"


def test_vector_socket_domain_aggregation():
    with g.tree():
        vec = g.Position().o.position

        lo = vec.point.min()
        assert isinstance(lo, VectorSocket)
        assert lo.node.bl_idname == g.FieldMinAndMax._bl_idname

        hi = vec.edge.max()
        assert isinstance(hi, VectorSocket)
        assert hi.node.bl_idname == g.FieldMinAndMax._bl_idname

        mean = vec.point.mean()
        assert isinstance(mean, VectorSocket)
        assert mean.node.bl_idname == g.FieldAverage._bl_idname

        median = vec.corner.median()
        assert isinstance(median, VectorSocket)
        assert median.node.bl_idname == g.FieldAverage._bl_idname

        std_dev = vec.point.std_dev()
        assert isinstance(std_dev, VectorSocket)
        assert std_dev.node.bl_idname == g.FieldVariance._bl_idname

        variance = vec.instance.variance()
        assert isinstance(variance, VectorSocket)
        assert variance.node.bl_idname == g.FieldVariance._bl_idname


def test_integer_socket_new_methods():
    with g.tree():
        val = g.Integer().o.integer

        result = val.clamp(0, 10)
        assert isinstance(result, IntegerSocket)
        assert result.builder_node.operation == "MINIMUM"
        inner = result.builder_node.i.value.links[0].from_node
        assert inner.bl_idname == g.IntegerMath._bl_idname
        assert inner.operation == "MAXIMUM"
        assert inner.inputs[1].default_value == 0
        assert result.builder_node.i.value_001.default_value == 10

        result = val.modulo(7)
        assert isinstance(result, IntegerSocket)
        assert result.node.bl_idname == g.IntegerMath._bl_idname
        assert result.node.operation == "MODULO"
        assert result.builder_node.i.value.links[0].from_node == val.node
        assert result.builder_node.i.value_001.default_value == 7


def test_integer_socket_domain_aggregation():
    with g.tree():
        val = g.Integer().o.integer

        lo = val.point.min()
        assert isinstance(lo, IntegerSocket)
        assert lo.node.bl_idname == g.FieldMinAndMax._bl_idname

        hi = val.face.max()
        assert isinstance(hi, IntegerSocket)
        assert hi.node.bl_idname == g.FieldMinAndMax._bl_idname


def test_domain_factory_evaluate_and_at_index():
    with g.tree():
        # Float
        val = g.Position().o.position.length()
        result = val.point.evaluate()
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname
        assert result.builder_node.i.value.links[0].from_node == val.node

        result = val.edge.at(2)
        assert isinstance(result, FloatSocket)
        assert result.node.bl_idname == g.EvaluateAtIndex._bl_idname
        assert result.builder_node.i.index.default_value == 2

        # Vector
        vec = g.Position().o.position
        result = vec.face.evaluate()
        assert isinstance(result, VectorSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname

        result = vec.corner.at(0)
        assert isinstance(result, VectorSocket)
        assert result.node.bl_idname == g.EvaluateAtIndex._bl_idname

        # Integer
        idx = g.Integer().o.integer
        result = idx.spline.evaluate()
        assert isinstance(result, IntegerSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname

        # Boolean
        flag = g.Boolean().o.boolean
        result = flag.point.evaluate()
        assert isinstance(result, BooleanSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname

        result = flag.edge.at(1)
        assert isinstance(result, BooleanSocket)
        assert result.node.bl_idname == g.EvaluateAtIndex._bl_idname

        # Rotation
        rot = g.AlignRotationToVector().o.rotation
        result = rot.point.evaluate()
        assert isinstance(result, RotationSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname

        result = rot.face.at(0)
        assert isinstance(result, RotationSocket)
        assert result.node.bl_idname == g.EvaluateAtIndex._bl_idname

        # Matrix
        mat = g.CombineTransform().o.transform
        result = mat.point.evaluate()
        assert isinstance(result, MatrixSocket)
        assert result.node.bl_idname == g.EvaluateOnDomain._bl_idname

        result = mat.edge.at(3)
        assert isinstance(result, MatrixSocket)
        assert result.node.bl_idname == g.EvaluateAtIndex._bl_idname


def test_all_domain_properties_reachable():
    """Every domain property on every socket type constructs its factory and evaluates."""
    domains = ("point", "edge", "face", "corner", "spline", "instance", "layer")
    with g.tree():
        vec = g.Position().o.position
        val = vec.length()
        idx = g.Integer().o.integer
        flag = g.Boolean(True).o.boolean
        rot = g.AlignRotationToVector().o.rotation
        mat = g.CombineTransform().o.transform

        for d in domains:
            assert isinstance(getattr(vec, d).evaluate(), VectorSocket)
            assert isinstance(getattr(val, d).evaluate(), FloatSocket)
            assert isinstance(getattr(idx, d).evaluate(), IntegerSocket)
            assert isinstance(getattr(flag, d).evaluate(), BooleanSocket)
            assert isinstance(getattr(rot, d).evaluate(), RotationSocket)
            assert isinstance(getattr(mat, d).evaluate(), MatrixSocket)

        input_pos = g.SetPosition().i.position
        with pytest.raises(RuntimeError):
            input_pos.point.evaluate()


def test_matrix_socket_transform_direction():
    with g.tree():
        mat = g.CombineTransform().o.transform
        direction = g.Vector().o.vector

        result = mat.transform_direction(direction)

    assert isinstance(result, VectorSocket)
    assert result.node.bl_idname == g.TransformDirection._bl_idname
    assert result.builder_node.i.direction.links[0].from_node == direction.node
    assert result.builder_node.i.transform.links[0].from_node == mat.node


def test_accumulate_field_socket_methods():
    with g.tree():
        vec = g.Position().o.position
        val = g.Value().o.value
        int = g.Integer().o.integer
        mat = g.CombineTransform().o.transform

        acc = vec.point.leading()
        node = acc.builder_node
        assert isinstance(acc, VectorSocket)
        assert acc.name == "Leading"
        assert isinstance(node, g.AccumulateField)
        assert node.data_type == "FLOAT_VECTOR"
        assert node.domain == "POINT"

        acc = val.edge.trailing()
        node = acc.builder_node
        assert isinstance(acc, FloatSocket)
        assert acc.name == "Trailing"
        assert isinstance(node, g.AccumulateField)
        assert node.data_type == "FLOAT"
        assert node.domain == "EDGE"

        acc = int.face.total()
        node = acc.builder_node
        assert isinstance(acc, IntegerSocket)
        assert acc.name == "Total"
        assert isinstance(node, g.AccumulateField)
        assert node.data_type == "INT"
        assert node.domain == "FACE"

        acc = mat.spline.trailing()
        node = acc.builder_node
        assert isinstance(acc, MatrixSocket)
        assert acc.name == "Trailing"
        assert isinstance(node, g.AccumulateField)
        assert node.data_type == "TRANSFORM"
        assert node.domain == "CURVE"


def test_object_methods():
    with g.tree() as tree:
        o = tree.inputs.object()

        loc = o.location()
        assert isinstance(loc, VectorSocket)
        assert isinstance(loc.builder_node, ObjectInfo)

        rot = o.rotation()
        assert isinstance(rot, RotationSocket)
        assert isinstance(rot.builder_node, ObjectInfo)

        scale = o.scale()
        assert isinstance(scale, VectorSocket)
        assert isinstance(scale.builder_node, ObjectInfo)

        assert loc.builder_node.transform_space == "ORIGINAL"
        assert rot.builder_node.transform_space == "ORIGINAL"
        assert scale.builder_node.transform_space == "ORIGINAL"
        rot.builder_node.transform_space = "RELATIVE"
        assert rot.builder_node.transform_space == "RELATIVE"
        scale.builder_node.transform_space = "RELATIVE"
        assert scale.builder_node.transform_space == "RELATIVE"
        loc.builder_node.transform_space = "RELATIVE"
        assert loc.builder_node.transform_space == "RELATIVE"


def test_list_slicing(snapshot):
    with g.tree() as tree:
        sliced = g.Index().o.index.to_list(10)[::2]
        assert sliced.node.bl_idname == GetListItem._bl_idname

    assert snapshot == tree._repr_markdown_()


def test_list_operations():
    with g.tree():
        lst = g.Index().o.index.to_list(10)

        # reverse uses a SortList node with a negated Index weight
        rev = lst.reverse()
        assert rev.node.bl_idname == SortList._bl_idname

        # negative start/stop are resolved relative to the list length
        neg = lst[-3:-1]
        assert neg.node.bl_idname == GetListItem._bl_idname

        # explicit None step falls back to a step of 1
        none_step = lst.list_slice(0, 5, None)
        assert none_step.node.bl_idname == GetListItem._bl_idname

        # integer indexing returns a single value via GetListItem
        item = lst[2]
        assert isinstance(item, IntegerSocket)
        assert item.node.bl_idname == GetListItem._bl_idname

        # __len__ returns an IntegerSocket backed by ListLength
        length = lst.__len__()
        assert isinstance(length, IntegerSocket)
        assert length.node.bl_idname == g.ListLength._bl_idname


def test_enable_output(snapshot):
    with g.tree() as tree:
        sel = tree.inputs.boolean()
        g.Cube().o.mesh.enable_output(sel) >> tree.outputs.geometry("Cube")
        g.IcoSphere() >> tree.outputs.geometry("IcoSphere").enable_output(sel)

    assert snapshot == tree.to_mermaid()
