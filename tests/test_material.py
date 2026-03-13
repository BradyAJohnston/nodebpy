from nodebpy import TreeBuilder, sockets
from nodebpy import shader as s


def test_simple_material():
    with TreeBuilder.shader() as tree:
        prin = s.PrincipledBSDF()
        with tree.outputs:
            _ = prin >> sockets.SocketShader()


def test_material_math():
    with TreeBuilder.shader() as tree:
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


def test_material_menu_switch():
    with TreeBuilder.shader() as tree:
        menu = s.MenuSwitch.shader(*[s.PrincipledBSDF() for _ in range(10)])
        with tree.outputs:
            _ = menu >> sockets.SocketShader()

    assert len(menu.node.enum_items) == 10
    assert menu.node.outputs[0].links

    with TreeBuilder.shader() as tree:
        menu = s.MenuSwitch.float(
            **{f"Input_{i}": float(value) for i, value in enumerate(range(10))}
        )
        with tree.outputs:
            _ = menu >> sockets.SocketFloat()

    assert len(menu.node.enum_items) == 10
    for i, input in enumerate(menu.inputs.values()):
        assert f"Input_{i}" == input.name
        assert float(i) == input.socket.default_value
