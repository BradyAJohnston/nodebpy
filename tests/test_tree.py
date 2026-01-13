import bpy
from nodebpy import nodes, sockets, TreeBuilder

with TreeBuilder() as tree:
    tree.interface(
        inputs=[sockets.SocketInt("Count")],
        outputs=[sockets.SocketGeometry("Instances")],
    )

    rotation = (
        nodes.RandomValue.vector(min=(-1, -1, -1), seed=2)
        >> nodes.AlignRotationToVector()
        >> nodes.RotateRotation()
    )

    _ = (
        tree.inputs.count
        >> nodes.Points(position=nodes.RandomValue.vector(min=(-1, -1, -1)))
        >> nodes.InstanceOnPoints(instance=nodes.Cube(), rotation=rotation)
        >> nodes.SetPosition(
            position=nodes.Position()
            >> nodes.VectorMath.scale(..., 2.0)
            >> nodes.VectorMath.add((0, 0.2, 0.3)),
            offset=(0, 0, 0.1),
        )
        >> nodes.RealizeInstances()
        >> nodes.InstanceOnPoints(nodes.Cube(), instance=...)
        >> tree.outputs.instances
    )

# save as a .blendfile for inspection
mod = bpy.data.objects["Cube"].modifiers.new("TestModifier", "NODES")
mod.node_group = tree.tree
bpy.ops.wm.save_as_mainfile(filepath="example.blend")
