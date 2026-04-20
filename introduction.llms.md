# Writing Node Trees

``` python
from nodebpy import geometry as g
```

## Adding Nodes

Adding nodes must be done inside of a context. We enter a context using the `with` keyword. While inside of this context, whenever you call a node class (`g.SetPosition()`) a node of that type will be added to the current tree.

This first example creates a new tree and adds two new nodes, linking the `Set Position` node into the `Transform Geometry` node. The output and input sockets for each are inferred based on simple heuristics around socket type and order.

``` python
with g.tree("NewTree") as tree:
    g.SetPosition() >> g.TransformGeometry()

tree
```

``` mermaid
graph LR
    N0("Set Position"):::geometry-node
    N1("Transform Geometry"):::geometry-node
    N0 -->|"Geometry->Geometry"| N1

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

These nodes can be saved as variables for re-use later in the node tree as well. After instantiating a class you can specify the input and output sockets using the `i_*` and `o_*` properties on the class.

These two approaches are equivalent:

## Individual Socket Access

``` python
with g.tree("AnotherTree") as tree:
    pos = g.SetPosition()

    g.Position() * 0.5 >> pos.i.position
    g.Vector() >> pos.i.offset
```

## Using Arguments to Class

``` python
with g.tree("AnotherAnotherTree") as tree:
    g.SetPosition(
        offset = g.Vector(),
        position = g.Position() * 0.5
    )
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Vector Math<br/><small>(SCALE)</small><br/><small>×0.5</small>"):::vector-node
    N2("Vector"):::input-node
    N3("Set Position"):::geometry-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"Vector->Position"| N3
    N2 -->|"Vector->Offset"| N3

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

## Node Input Sockets

The socket interface nodes define what values / sockets are available as inputs for the node tree.

We define them in a similar way to the socekts themselves, using context with the `tree.inputs` and `tree.outputs` and adding sockets with the `s.SocketGeometry()`.

``` python
with g.tree("NewTree") as tree:
    geom_inputs = [tree.inputs.geometry(f"Geometry_{i}") for i in range(5)]
    g.JoinGeometry(*geom_inputs) >> tree.outputs.geometry("The Output Socket")

tree
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Join Geometry"):::geometry-node
    N2("Group Output"):::default-node
    N0 -->|"Geometry_4->Geometry"| N1
    N0 -->|"Geometry_3->Geometry"| N1
    N0 -->|"Geometry_2->Geometry"| N1
    N0 -->|"Geometry_1->Geometry"| N1
    N0 -->|"Geometry_0->Geometry"| N1
    N1 -->|"Geometry->The Output Socket"| N2

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

``` python
with g.tree() as tree:
    (
        tree.inputs.integer("Count", 10)
        >> g.Points(position=g.RandomValue.vector(min=(-0.1,-0.1,-0.2)))
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Random Value<br/><small>(-0.1,-0.1,-0.2)</small>"):::converter-node
    N2("Points"):::geometry-node
    N3("Group Output"):::default-node
    N1 -->|"Value->Position"| N2
    N0 -->|"Count->Count"| N2
    N2 -->|"Points->Geometry"| N3

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

``` python
with g.tree() as tree:
    count = tree.inputs.integer("Count", 10)
    output = tree.outputs.geometry()

    (
        count
        >> g.Points(position=g.RandomValue.vector() * 0.5 * g.Position())
        >> output
    )

tree
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Random Value"):::converter-node
    N2("Vector Math<br/><small>(SCALE)</small><br/><small>×0.5</small>"):::vector-node
    N3("Position"):::input-node
    N4("Vector Math<br/><small>(MULTIPLY)</small>"):::vector-node
    N5("Points"):::geometry-node
    N6("Group Output"):::default-node
    N1 -->|"Value->Vector"| N2
    N2 -->|"Vector->Vector"| N4
    N3 -->|"Position->Vector"| N4
    N4 -->|"Vector->Position"| N5
    N0 -->|"Count->Count"| N5
    N5 -->|"Points->Geometry"| N6

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

## Zones

Zones like the repeat and simulation zone are initialized with their `SimulationZone()` and `RepeatZone()` constructors. You can add individvual `RepeatInput()` node and output, but they require additional setup to be actually linked. The repeat zone can be initialized with a repeat count, which can also be linked to from elsewhere.

We can access the input and output nodes with `zone.input` and `zone.output`. The repeat zone as the `zone.i` which is the iteration number of the current zone. Simulation zone has the `zone.output.o_delta_time` which is the time between previous and current simulation loop.

Both input and output nodes can automatically detect and capture links when you attempt to link into them with `>>`. The `zone.input.capture()` method also allows you to explicitly capture a link or a value, returning the output socket for further linking.

``` python
with g.tree(arrange=None) as tree:
    zone = g.RepeatZone(10)
    join = g.JoinGeometry()
    # a geometry socket is added to the zone when we try to connect from the Join Geometry
    # to the zone output, which is then available for the zone.input >> join
    join >> zone.output >> g.SetPosition()
    zone.input >> join
    g.Points(zone.i, position=g.RandomValue.vector(seed=zone.i)) >> join


tree
```

``` mermaid
graph LR
    N0("Repeat Input"):::default-node
    N1("Repeat Output"):::default-node
    N2("Join Geometry"):::geometry-node
    N3("Set Position"):::geometry-node
    N4("Random Value"):::converter-node
    N5("Points"):::geometry-node
    N2 -->|"Geometry->Geometry"| N1
    N1 -->|"Geometry->Geometry"| N3
    N0 -->|"Geometry->Geometry"| N2
    N0 -->|"Iteration->Seed"| N4
    N0 -->|"Iteration->Count"| N5
    N4 -->|"Value->Position"| N5
    N5 -->|"Points->Geometry"| N2

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

``` python
with g.tree(arrange=None) as tree:
    # this initializes the zone with two socket inputs for each of the values
    zone = g.SimulationZone(g.Value(), g.Vector())

    # this explicitly grabs the "Value" socket (which got it's name from the g.Value() node)
    # and adds 10 then attempts to plug it into the zone output (it will choose the float
    # socket instead of the vector socket because that is the most compatible)
    zone.input.outputs["Value"] + 10 >> zone.output
    # this should automatically pick the vector input socket because we are
    # explicity about the VectorMath and it will be the most compatible
    zone.input >> g.VectorMath.add((1.2, 1.2, 1.2)) >> zone.output

tree
```

``` mermaid
graph LR
    N0("Value"):::input-node
    N1("Vector"):::input-node
    N2("Simulation Input"):::default-node
    N3("Simulation Output"):::default-node
    N4("Math<br/><small>(ADD)</small>"):::converter-node
    N5("Vector Math<br/><small>(ADD)</small>"):::vector-node
    N0 -->|"Value->Value"| N2
    N1 -->|"Vector->Vector"| N2
    N2 -->|"Value->Value"| N4
    N4 -->|"Value->Value"| N3
    N2 -->|"Vector->Vector"| N5
    N5 -->|"Vector->Vector"| N3

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```
