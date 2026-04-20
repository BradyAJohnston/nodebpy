# nodebpy

[![Run Tests](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml/badge.svg)](https://github.com/BradyAJohnston/nodebpy/actions/workflows/tests.yml) [![](https://codecov.io/gh/BradyAJohnston/nodebpy/graph/badge.svg?token=buThDQZUED)](https://codecov.io/gh/BradyAJohnston/nodebpy)

A package to help build node trees in blender more elegantly with python code.

## The Design Idea

Other projects have attempted similar but none quite handled the API how I felt it should be done. Notable existing projects are [geometry-script](https://github.com/carson-katri/geometry-script), [geonodes](https://github.com/al1brn/geonodes), [NodeToPython](https://github.com/BrendanParmer/NodeToPython).

Other projects implement chaining of nodes mostly as dot methos of nodes to chain them (`InstanceOnPoints().set_position()`). This has the potential to crowd the API for individual nodes and easy chaining is instead approached via overriding the `>>` operator.

### Chain Nodes with `>>`

By default the operator attempts to link the first output of the previous node with the first input of the next. You can override this behaviour by being explicit with the socket you are passing out (`AccumulateField().o_total`) or using the `...` for the inputs into the next node. The dots can appear at multiple locations and each input will be linked to the previous node via the inferred or specified socket.

# Example Node Tree

``` python
from nodebpy import geometry as g

with g.tree("AnotherTree") as tree:
    count = tree.inputs.integer("Count", 10)
    instances = tree.outputs.geometry("Instances")

    rotation = (
        g.RandomValue.vector(min=(-1, -1, -1), seed=2)
        >> g.AlignRotationToVector()
        >> g.RotateRotation(
            rotate_by=g.AxisAngleToRotation(angle=0.3), rotation_space="LOCAL"
        )
    )

    _ = (
        count
        >> g.Points(position=g.RandomValue.vector(min=(-1, -1, -1)))
        >> g.InstanceOnPoints(instance=g.Cube(), rotation=rotation)
        >> g.SetPosition(
            position=g.Position() * 2.0 + (0, 0.2, 0.3),
            offset=(0, 0, 0.1),
        )
        >> g.RealizeInstances()
        >> g.InstanceOnPoints(g.Cube(), instance=...)
        >> instances
    )

tree
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Random Value<br/><small>(-1,-1,-1) seed:2</small>"):::converter-node
    N2("Random Value<br/><small>(-1,-1,-1)</small>"):::converter-node
    N3("Align Rotation to Vector"):::converter-node
    N4("Axis Angle to Rotation<br/><small>(0,0,1)</small>"):::converter-node
    N5("Position"):::input-node
    N6("Points"):::geometry-node
    N7("Cube"):::geometry-node
    N8("Rotate Rotation"):::converter-node
    N9("Vector Math<br/><small>(SCALE)</small><br/><small>×2</small>"):::vector-node
    N10("Instance on Points"):::geometry-node
    N11("Vector Math<br/><small>(ADD)</small><br/><small>(0,0.2,0.3)</small>"):::vector-node
    N12("Set Position<br/><small>+(0,0,0.1)</small>"):::geometry-node
    N13("Cube"):::geometry-node
    N14("Realize Instances"):::geometry-node
    N15("Instance on Points"):::geometry-node
    N16("Group Output"):::default-node
    N1 -->|"Value->Vector"| N3
    N4 -->|"Rotation->Rotate By"| N8
    N3 -->|"Rotation->Rotation"| N8
    N2 -->|"Value->Position"| N6
    N0 -->|"Count->Count"| N6
    N7 -->|"Mesh->Instance"| N10
    N8 -->|"Rotation->Rotation"| N10
    N6 -->|"Points->Points"| N10
    N5 -->|"Position->Vector"| N9
    N9 -->|"Vector->Vector"| N11
    N11 -->|"Vector->Position"| N12
    N10 -->|"Instances->Geometry"| N12
    N12 -->|"Geometry->Geometry"| N14
    N13 -->|"Mesh->Points"| N15
    N14 -->|"Geometry->Instance"| N15
    N15 -->|"Instances->Instances"| N16

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

![](images/paste-1.png)

# Design Considerations

Whenever possible, support IDE auto-complete and have useful types. We should know as much ahead of time as possible if our network will actually build.

- Stick as closely to Geometry Nodes naming as possible
  - `RandomValue` creates a random value node
    - `RandomValue.vector()` creates it set to `"VECTOR"` data type and provides arguments for IDE auto-complete
- Inputs and outputs from a node are prefixed with `i_*` and `o_`:
  - `AccumulateField().o_total` returns the output `Total` socket
  - `AccumulateField().i_value` returns the input `Value` socket
- If inputs are subject to change depending on enums, provide separate constructor methods that provide related inputs as arguments. There should be no guessing involved and IDEs should provide documentation for what is required:
  - `TransformGeometry.matrix(CombineTrasnsform(translation=(0, 0, 1))`
  - `TransformGeoemtry.components(translation=(0, 0, 1))`
  - `TransformGeometry(translation=(0, 0, 1))`
