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
