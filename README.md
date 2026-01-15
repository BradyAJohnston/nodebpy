

# nodebpy

[![Run
Tests](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml/badge.svg)](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml)
[![](https://codecov.io/gh/BradyAJohnston/nodebpy/graph/badge.svg?token=buThDQZUED)](https://codecov.io/gh/BradyAJohnston/nodebpy)

A package to help build node trees in blender more elegantly with python
code.

## The Design Idea

Other projects have attempted similar but none quite handled the API how
I felt it should be done. Notable existing projects are
[geometry-script](https://github.com/carson-katri/geometry-script),
[geonodes](https://github.com/al1brn/geonodes),
[NodeToPython](https://github.com/BrendanParmer/NodeToPython).

Other projects implement chaining of nodes mostly as dot methos of nodes
to chain them (`InstanceOnPoints().set_position()`). This has the
potential to crowd the API for individual nodes and easy chaining is
instead approached via overriding the `>>` operator.

### Chain Nodes with `>>`

By default the operator attempts to link the first output of the
previous node with the first input of the next. You can override this
behaviour by being explicit with the socket you are passing out
(`AccumulateField().o_total`) or using the `...` for the inputs into the
next node. The dots can appear at multiple locations and each input will
be linked to the previous node via the inferred or specified socket.

# Example Node Tree

``` python
from nodebpy import TreeBuilder, nodes as n, sockets as s

with TreeBuilder("AnotherTree") as tree:
    with tree.inputs:
        count = s.SocketInt("Count", 10)
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

tree
```

``` mermaid
graph LR
    N0("NodeGroupInput"):::default-node
    N1("RandomValue<br/><small>(-1,-1,-1) seed:2</small>"):::converter-node
    N2("RandomValue<br/><small>(-1,-1,-1) seed:1</small>"):::converter-node
    N3("AlignRotationToVector<br/><small>(0,0,1)</small>"):::converter-node
    N4("AxisAngleToRotation<br/><small>(0,0,1)</small>"):::converter-node
    N5("InputPosition"):::input-node
    N6("Points"):::geometry-node
    N7("MeshCube"):::geometry-node
    N8("RotateRotation"):::converter-node
    N9("VectorMath<br/><small>×2</small>"):::vector-node
    N10("InstanceOnPoints"):::geometry-node
    N11("VectorMath<br/><small>(0,0.2,0.3)</small>"):::vector-node
    N12("SetPosition<br/><small>+(0,0,0.1)</small>"):::geometry-node
    N13("MeshCube"):::geometry-node
    N14("RealizeInstances"):::geometry-node
    N15("InstanceOnPoints"):::geometry-node
    N16("NodeGroupOutput"):::default-node
    N1 -->|"Value>>Rotation"| N3
    N4 -->|"Rotation>>Rotate By"| N8
    N3 -->|"Rotation>>Rotation"| N8
    N2 -->|"Value>>Position"| N6
    N0 -->|"Count>>Count"| N6
    N7 -->|"Mesh>>Instance"| N10
    N8 -->|"Rotation>>Rotation"| N10
    N6 -->|"Points>>Points"| N10
    N5 -->|"Position>>Vector"| N9
    N9 -->|"Vector>>Vector"| N11
    N11 -->|"Vector>>Position"| N12
    N10 -->|"Instances>>Geometry"| N12
    N12 -->|"Geometry>>Geometry"| N14
    N13 -->|"Mesh>>Points"| N15
    N14 -->|"Geometry>>Instance"| N15
    N15 -->|"Instances>>Instances"| N16

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

![](docs/images/paste-2.png)

# Design Considerations

Whenever possible, support IDE auto-complete and have useful types. We
should know as much ahead of time as possible if our network will
actually build.

- Stick as closely to Geometry Nodes naming as possible
  - `RandomValue` creates a random value node
    - `RandomValue.vector()` creates it set to `"VECTOR"` data type and
      provides arguments for IDE auto-complete
- Inputs and outputs from a node are prefixed with `i_*` and `o_`:
  - `AccumulateField().o_total` returns the output `Total` socket
  - `AccumulateField().i_value` returns the input `Value` socket
- If inputs are subject to change depending on enums, provide separate
  constructor methods that provide related inputs as arguments. There
  should be no guessing involved and IDEs should provide documentation
  for what is required:
  - `TransformGeometry.matrix(CombineTrasnsform(translation=(0, 0, 1))`
  - `TransformGeoemtry.components(translation=(0, 0, 1))`
  - `TransformGeometry(translation=(0, 0, 1))`
