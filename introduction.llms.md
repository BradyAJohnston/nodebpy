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
```

## Node Input Sockets

The socket interface nodes define what values / sockets are available as inputs for the node tree.

We define them in a similar way to the socekts themselves, using context with the `tree.inputs` and `tree.outputs` and adding sockets with the `s.SocketGeometry()`.

``` python
with g.tree("NewTree") as tree:
    geom_inputs = [tree.inputs.geometry(f"Geometry_{i}") for i in range(5)]
    g.JoinGeometry(geom_inputs) >> tree.outputs.geometry("The Output Socket")

tree
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Join Geometry"):::geometry-node
    N2("Group Output"):::default-node
    N0 -->|"Geometry_0->Geometry"| N1
    N0 -->|"Geometry_1->Geometry"| N1
    N0 -->|"Geometry_2->Geometry"| N1
    N0 -->|"Geometry_3->Geometry"| N1
    N0 -->|"Geometry_4->Geometry"| N1
    N1 -->|"Geometry->The Output Socket"| N2
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
    N0 -->|"Count->Count"| N2
    N1 -->|"Value->Position"| N2
    N2 -->|"Points->Geometry"| N3
```

``` python
with g.tree() as tree:
    count = tree.inputs.integer("Count", 10)
    pos = g.RandomValue.vector() * 0.5 * g.Position()
    g.Points(count, pos) >> tree.outputs.geometry()

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
    N0 -->|"Count->Count"| N5
    N4 -->|"Vector->Position"| N5
    N5 -->|"Points->Geometry"| N6
```

## Zones

Zones like the repeat and simulation zone are initialized with their `SimulationZone()` and `RepeatZone()` constructors. You can add individvual `RepeatInput()` node and output, but they require additional setup to be actually linked. The repeat zone can be initialized with a repeat count, which can also be linked to from elsewhere.

We can access the input and output nodes with `zone.input` and `zone.output`. The repeat zone has the `zone.iteration` which is the iteration number of the current zone. Simulation zone has the `zone.delta_time` which is the time between previous and current simulation loop.

Because of the complexity of zones, we have the `Item` helper which gives access to the input & output sockets on the input and output nodes (4 sockets total). For the Simulation and Repeat zones, we have the:

| Code           | Socket                      |
|----------------|-----------------------------|
| `item.initial` | `zone.input.i["Geometry"]`  |
| `item.current` | `zone.input.o["Geometry"]`  |
| `item.next`    | `zone.output.i["Geometry"]` |
| `item.result`  | `zone.output.o["Geometry"]` |

``` python
with g.tree(arrange=None) as tree:
    zone = g.RepeatZone(10)
    random_pos = g.RandomValue.vector(seed=zone.iteration)
    geo = zone.item("Geometry", type="GEOMETRY")
    g.JoinGeometry([geo.current, g.Points(10, random_pos)]) >> geo.next
    geo.result >> tree.outputs.geometry()

tree
```

``` mermaid
graph LR
    N0("Repeat Input"):::default-node
    N1("Repeat Output"):::default-node
    N2("Random Value"):::converter-node
    N3("Points"):::geometry-node
    N4("Join Geometry"):::geometry-node
    N5("Group Output"):::default-node
    N4 -->|"Geometry->Geometry"| N1
    N0 -->|"Iteration->Seed"| N2
    N2 -->|"Value->Position"| N3
    N0 -->|"Geometry->Geometry"| N4
    N3 -->|"Points->Geometry"| N4
    N1 -->|"Geometry->Geometry"| N5
```

``` python
with g.tree(arrange=None) as tree:
    # this initializes the zone with two socket inputs for each of the values
    # we manually specify the socket names
    zone = g.SimulationZone({"Value": g.Value(), "Vector": g.Vector()})
    zone.input.o["Value"] + 10 >> zone.output

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
    N4 -->|"Value->Value"| N3
    N5 -->|"Vector->Vector"| N3
    N2 -->|"Value->Value"| N4
    N2 -->|"Vector->Vector"| N5
```
