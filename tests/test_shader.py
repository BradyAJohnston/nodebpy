import bpy
import pytest

from nodebpy import shader as s
from nodebpy import sockets
from nodebpy.builder import SocketError


def test_simple_shader():
    with s.tree() as tree:
        prin = s.PrincipledBSDF()
        with tree.outputs:
            _ = prin >> sockets.SocketShader()


def test_shader_math():
    with s.tree() as tree:
        comp = s.Geometry().o_random_per_island >= 10.0
        prin = s.PrincipledBSDF(ior=comp)
        with tree.outputs:
            _ = prin >> sockets.SocketShader()

    assert comp.node.bl_idname == "ShaderNodeMath"
    assert comp.operation == "SUBTRACT"
    assert comp.node.inputs[1].links[0].from_node.bl_idname == "ShaderNodeMath"
    assert comp.node.inputs[1].links[0].from_node.inputs[1].default_value == 10.0
    assert (
        comp.node.inputs[1].links[0].from_node.inputs[0].links[0].from_node.bl_idname
        == "ShaderNodeNewGeometry"
    )


def test_shader_menu_switch():
    with s.tree() as tree:
        menu = s.MenuSwitch.shader(*[s.PrincipledBSDF() for _ in range(10)])
        with tree.outputs:
            _ = menu >> sockets.SocketShader()

    assert len(menu.node.enum_items) == 10
    assert menu.node.outputs[0].links

    with s.tree() as tree:
        menu = s.MenuSwitch.float(
            **{f"Input_{i}": float(value) for i, value in enumerate(range(10))}
        )
        with tree.outputs:
            _ = menu >> sockets.SocketFloat()

    assert len(menu.node.enum_items) == 10
    for i, input in enumerate([x for x in menu.inputs.values() if x.type == "VALUE"]):
        assert f"Input_{i}" == input.name
        assert float(i) == input.socket.default_value

    with s.tree() as tree:
        menu = s.MenuSwitch.float(
            **{f"Input_{i}": s.Value(value) for i, value in enumerate(range(10))}
        )
        with tree.outputs:
            _ = menu >> sockets.SocketFloat()

    assert len(menu.node.enum_items) == 10
    print(list(menu.inputs.items()))
    for i, input in enumerate([x for x in menu.inputs.values() if x.type == "VALUE"]):
        assert input.socket.links[0].from_node.bl_idname == s.Value._bl_idname
        # we have to check the output defeault value here because that is how the Value
        # node is defined which is truly cursed but hey it is what it is
        assert input.socket.links[0].from_node.outputs[0].default_value == float(i)


def test_color_shader():
    with s.tree():
        mix_shader = s.MixShader(1.0, s.Color())
        assert (
            mix_shader.node.inputs["Shader"].links[0].from_node.bl_idname
            == s.Color._bl_idname
        )
        with pytest.raises(SocketError):
            _ = s.Mix.color(0.5, mix_shader)


def test_material_node_cartoon():
    with s.material("Cartoon", fake_user=True) as mat:
        mat.nodes.clear()
        output = s.MaterialOutput(surface=s.Attribute.geometry("Color").o_color)
        attr = s.Attribute.geometry("sec_struct")
        aov = s.AovOutput(value=attr, aov_name="sec_struct")

    assert (
        output.node.inputs["Surface"].links[0].from_node.bl_idname
        == s.Attribute._bl_idname
    )
    assert (
        aov.node.inputs["Value"].links[0].from_node.bl_idname == s.Attribute._bl_idname
    )
    assert "Cartoon" in bpy.data.materials
    assert "Cartoon" not in bpy.data.node_groups
    assert attr.attribute_name == "sec_struct"
    assert attr.attribute_type == "GEOMETRY"
