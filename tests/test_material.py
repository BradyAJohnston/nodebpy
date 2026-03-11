from nodebpy import TreeBuilder, sockets
from nodebpy import shader as s


def test_simple_material():
    with TreeBuilder.shader() as tree:
        prin = s.PrincipledBsdf()
        with tree.outputs:
            _ = prin >> sockets.SocketShader()
