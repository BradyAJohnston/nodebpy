import bpy
import pytest

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder.interface import InterfaceSocket

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

    assert isinstance(f, InterfaceSocket)
    assert isinstance(i, InterfaceSocket)
    assert isinstance(b, InterfaceSocket)
    assert f.interface_socket.name == "Value"
    assert i.interface_socket.name == "Count"
    assert b.interface_socket.name == "Enabled"
    assert f.interface_socket.default_value == pytest.approx(2.5)
    assert i.interface_socket.default_value == 4
    assert b.interface_socket.default_value is True


def test_geometry_vector_sockets():
    """Vector, Rotation, and Matrix sockets are created correctly."""
    with g.tree(arrange=None) as tree:
        v = tree.inputs.vector("Direction", (1.0, 0.0, 0.0))
        r = tree.inputs.rotation("Rotation")
        m = tree.inputs.matrix("Transform")

    assert v.interface_socket.name == "Direction"
    assert r.interface_socket.name == "Rotation"
    assert m.interface_socket.name == "Transform"
    assert v.interface_socket.socket_type == "NodeSocketVector"
    assert r.interface_socket.socket_type == "NodeSocketRotation"
    assert m.interface_socket.socket_type == "NodeSocketMatrix"


def test_geometry_string_socket():
    with g.tree(arrange=None) as tree:
        ss = tree.inputs.string("Label", default_value="hello")

    assert ss.interface_socket.name == "Label"
    assert ss.interface_socket.default_value == "hello"


def test_geometry_menu_socket():
    with g.tree(arrange=None) as tree:
        menu = tree.inputs.menu("Mode")

    assert menu.interface_socket.name == "Mode"
    assert menu.interface_socket.socket_type == "NodeSocketMenu"


def test_geometry_datablock_sockets():
    """Object, Collection, Material, and Image sockets are created correctly."""
    with g.tree(arrange=None) as tree:
        obj = tree.inputs.object("Object")
        col = tree.inputs.collection("Collection")
        mat = tree.inputs.material("Material")
        img = tree.inputs.image("Image")

    assert obj.interface_socket.socket_type == "NodeSocketObject"
    assert col.interface_socket.socket_type == "NodeSocketCollection"
    assert mat.interface_socket.socket_type == "NodeSocketMaterial"
    assert img.interface_socket.socket_type == "NodeSocketImage"


def test_geometry_bundle_and_closure_sockets():
    with g.tree(arrange=None) as tree:
        bundle = tree.inputs.bundle("Bundle")
        closure = tree.inputs.closure("Closure")

    assert bundle.interface_socket.socket_type == "NodeSocketBundle"
    assert closure.interface_socket.socket_type == "NodeSocketClosure"


def test_geometry_color_socket():
    with g.tree(arrange=None) as tree:
        col = tree.inputs.color("Tint", (0.5, 0.1, 0.9, 1.0))

    assert col.interface_socket.name == "Tint"
    assert col.interface_socket.default_value[0] == pytest.approx(0.5)
    assert col.interface_socket.default_value[2] == pytest.approx(0.9)


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

    assert f.interface_socket.default_value == pytest.approx(0.5)
    assert f.interface_socket.min_value == pytest.approx(0.0)
    assert f.interface_socket.max_value == pytest.approx(1.0)
    assert f.interface_socket.subtype == "FACTOR"


def test_integer_limits():
    with g.tree(arrange=None) as tree:
        i = tree.inputs.integer("Count", default_value=10, min_value=1, max_value=100)

    assert i.interface_socket.default_value == 10
    assert i.interface_socket.min_value == 1
    assert i.interface_socket.max_value == 100


def test_socket_description():
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry("Geometry", description="The input mesh")
        f = tree.inputs.float("Scale", description="Uniform scale factor")

    assert geo.interface_socket.description == "The input mesh"
    assert f.interface_socket.description == "Uniform scale factor"


def test_socket_vector_default_input():
    with g.tree(arrange=None) as tree:
        pos = tree.inputs.vector("Position", default_input="POSITION")
        normal = tree.inputs.vector("Normal", default_input="NORMAL")

    assert pos.interface_socket.default_input == "POSITION"
    assert normal.interface_socket.default_input == "NORMAL"


def test_socket_hide_value():
    with g.tree(arrange=None) as tree:
        f = tree.inputs.float("Hidden", hide_value=True)
        i = tree.inputs.integer("Visible")

    assert f.interface_socket.hide_value is True
    assert i.interface_socket.hide_value is False


def test_socket_menu_expanded():
    with g.tree(arrange=None) as tree:
        menu = tree.inputs.menu("Mode", expanded=True)

    assert menu.interface_socket.menu_expanded is True


def test_integer_percentage_subtype():
    with g.tree(arrange=None) as tree:
        pct = tree.inputs.integer("Progress", default_value=50, subtype="PERCENTAGE")

    assert pct.interface_socket.subtype == "PERCENTAGE"


def test_socket_vector_subtype():
    with g.tree(arrange=None) as tree:
        vel = tree.inputs.vector("Velocity", subtype="VELOCITY")

    assert vel.interface_socket.subtype == "VELOCITY"


# ---------------------------------------------------------------------------
# Output sockets
# ---------------------------------------------------------------------------


def test_geometry_output_sockets():
    with g.tree(arrange=None) as tree:
        geo_out = tree.outputs.geometry()
        f_out = tree.outputs.float("Score")
        b_out = tree.outputs.boolean("Valid")

    assert geo_out.interface_socket.in_out == "OUTPUT"
    assert f_out.interface_socket.in_out == "OUTPUT"
    assert b_out.interface_socket.in_out == "OUTPUT"
    assert f_out.interface_socket.name == "Score"


def test_input_and_output_same_name_independent():
    """An input and output socket with the same name are separate interface items."""
    with g.tree(arrange=None) as tree:
        geo_in = tree.inputs.geometry("Geometry")
        geo_out = tree.outputs.geometry("Geometry")

    assert geo_in.interface_socket.in_out == "INPUT"
    assert geo_out.interface_socket.in_out == "OUTPUT"
    assert geo_in.interface_socket is not geo_out.interface_socket


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

    assert scale.interface_socket.default_value == pytest.approx(2.0)


def test_multiple_sockets_link_independently():
    """Two separate input sockets wire to different node inputs."""
    with g.tree(arrange=None) as tree:
        geo = tree.inputs.geometry()
        offset = tree.inputs.vector("Offset")
        out = tree.outputs.geometry()

        g.SetPosition(geo, offset=offset) >> out

    assert geo.interface_socket.name == "Geometry"
    assert offset.interface_socket.name == "Offset"


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

    assert shader_out.interface_socket.in_out == "OUTPUT"
    assert shader_out.interface_socket.socket_type == "NodeSocketShader"
    assert base_color.interface_socket.default_value[0] == pytest.approx(0.8)
    assert metallic.interface_socket.max_value == pytest.approx(1.0)


def test_shader_vector_input():
    """Vector sockets are valid in shader trees (default_input is geometry-tree-only)."""
    with s.tree(arrange=None) as tree:
        normal = tree.inputs.vector("Normal")
        shader_out = tree.outputs.shader()

        s.PrincipledBSDF(normal=normal) >> shader_out

    assert normal.interface_socket.socket_type == "NodeSocketVector"
    assert normal.interface_socket.name == "Normal"


def test_shader_int_and_boolean_inputs():
    with s.tree(arrange=None) as tree:
        samples = tree.inputs.integer("Samples", 128, min_value=1, max_value=4096)
        enabled = tree.inputs.boolean("Enabled", default_value=True)
        shader_out = tree.outputs.shader()

        s.PrincipledBSDF() >> shader_out

    assert samples.interface_socket.default_value == 128
    assert samples.interface_socket.min_value == 1
    assert enabled.interface_socket.default_value is True


def test_shader_float_output():
    with s.tree(arrange=None) as tree:
        shader_out = tree.outputs.shader()
        alpha_out = tree.outputs.float("Alpha")

        prin = s.PrincipledBSDF()
        prin >> shader_out

    assert alpha_out.interface_socket.in_out == "OUTPUT"
    assert alpha_out.interface_socket.socket_type == "NodeSocketFloat"


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

    assert image.interface_socket.socket_type == "NodeSocketColor"
    assert fac.interface_socket.default_value == pytest.approx(1.0)
    assert out.interface_socket.in_out == "OUTPUT"


def test_compositor_vector_socket():
    with c.tree(arrange=None) as tree:
        normal = tree.inputs.vector("Normal")
        out = tree.outputs.color("Image")

        c.Blur(normal) >> out

    assert normal.interface_socket.socket_type == "NodeSocketVector"


def test_compositor_menu_socket():
    with c.tree(arrange=None) as tree:
        mode = tree.inputs.menu("Mode", expanded=True)
        image = tree.inputs.color("Image")
        out = tree.outputs.color("Image")

        c.Blur(image) >> out

    assert mode.interface_socket.socket_type == "NodeSocketMenu"
    assert mode.interface_socket.menu_expanded is True


def test_compositor_multiple_outputs():
    with c.tree(arrange=None) as tree:
        image = tree.inputs.color("Image")
        image_out = tree.outputs.color("Image")
        mask_out = tree.outputs.float("Mask")

        c.Blur(image) >> image_out

    assert image_out.interface_socket.in_out == "OUTPUT"
    assert mask_out.interface_socket.in_out == "OUTPUT"
    assert image_out.interface_socket.socket_type == "NodeSocketColor"
    assert mask_out.interface_socket.socket_type == "NodeSocketFloat"


def test_compositor_int_and_boolean_sockets():
    with c.tree(arrange=None) as tree:
        size = tree.inputs.integer("Size", 3, min_value=1, max_value=32)
        enabled = tree.inputs.boolean("Enabled")
        out = tree.outputs.color("Image")

        image = tree.inputs.color("Image")
        c.Blur(image) >> out

    assert size.interface_socket.default_value == 3
    assert size.interface_socket.min_value == 1
    assert enabled.interface_socket.socket_type == "NodeSocketBool"


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
