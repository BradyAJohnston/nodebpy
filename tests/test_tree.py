from nodebpy import TreeBuilder
from nodebpy import nodes as n
from nodebpy import sockets as s


def test_create_tree_and_save():
    with TreeBuilder("AnotherTree") as tree:
        with tree.inputs:
            count = s.SocketInt("Count")
        with tree.outputs:
            instances = s.SocketGeometry("Instances")

        rotation = (
            n.RandomValue.vector(min=(-1, -1, -1), seed=2)
            >> n.AlignRotationToVector()
            >> n.RotateRotation(
                rotate_by=n.AxisAngleToRotation(angle=0.3), rotation_space="LOCAL"
            )
        )

        _ = (
            count
            >> n.Points(position=n.RandomValue.vector(min=(-1, -1, -1)))
            >> n.InstanceOnPoints(instance=n.Cube(), rotation=rotation)
            >> n.SetPosition(
                position=n.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> n.RealizeInstances()
            >> n.InstanceOnPoints(n.Cube(), instance=...)
            >> instances
        )
