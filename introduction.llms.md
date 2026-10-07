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

These nodes can be saved as variables for re-use later in the node tree as well. After instantiating a class you can access the input and output sockets through the `.i` and `.o` accessors on the class.

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

## Interface Sockets

The tree’s interface defines what sockets are available as inputs and outputs of the node tree.

We declare them with `tree.inputs` and `tree.outputs` — for example `tree.inputs.geometry()` or `tree.outputs.float("Result")` — which add the interface socket and return it for linking with other nodes.

``` python
with g.tree("NewTree") as tree:
    geom_inputs = [tree.inputs.geometry(f"Geometry_{i}") for i in range(5)]
    g.JoinGeometry(geom_inputs) >> tree.outputs.geometry("The Output Socket")

tree
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

``` python
with g.tree() as tree:
    count = tree.inputs.integer("Count", 10)
    pos = g.RandomValue.vector() * 0.5 * g.Position()
    g.Points(count, pos) >> tree.outputs.geometry()

tree
```

## Zones

Zones like the repeat and simulation zone are initialized with their `SimulationZone()` and `RepeatZone()` constructors. You can add individual `RepeatInput()` and output nodes, but they require additional setup to be actually linked. The repeat zone can be initialized with a repeat count, which can also be linked to from elsewhere.

We can access the input and output nodes with `zone.input` and `zone.output`. The repeat zone has `zone.iteration`, which is the iteration number of the current zone. The simulation zone has `zone.delta_time`, which is the time between the previous and current simulation loop.

Because of the complexity of zones, we have the `ZoneItem` helper which gives access to the input & output sockets on the input and output nodes (4 sockets total). For the Simulation and Repeat zones, we have the:

| Code           | Socket                      |
|----------------|-----------------------------|
| `item.initial` | `zone.input.i["Geometry"]`  |
| `item.current` | `zone.input.o["Geometry"]`  |
| `item.next`    | `zone.output.i["Geometry"]` |
| `item.result`  | `zone.output.o["Geometry"]` |

State items are declared on `zone.items`, one method per data type (`zone.items.geometry()`, `zone.items.float()`, `zone.items.vector()`, …). Each returns a `ZoneItem` handle whose four role sockets are statically typed to the matching socket class, so editors can autocomplete and type-check the zone body. The value comes first: pass a linkable to link it as the item’s starting value (the item is named after the source socket unless you give a name), a plain value to set the socket default, or nothing to declare the item unlinked. Linking into `initial` with `>>` continues the chain from `current`, and linking into `next` continues from `result`, so a zone body can be written as one chain:

``` python
with g.tree() as tree:
    zone = g.RepeatZone(10)
    random_pos = g.RandomValue.vector(seed=zone.iteration)
    geo = zone.items.geometry()
    (
        g.Cube()
        >> geo.initial
        >> g.JoinGeometry([g.Points(10, random_pos)])
        >> geo.next
        >> tree.outputs.geometry()
    )

tree
```

`zone.items` is also a collection: `len(zone.items)`, iterating it and indexing by position or name (`zone.items["Geometry"]`) all give the same handles. `zone.items.new(value, name, type="FLOAT")` declares an item whose type is only known at runtime.

The repeat zone additionally offers datablock item types the simulation zone does not support (`zone.items.object()`, `zone.items.image()`, `zone.items.collection()`, `zone.items.material()`, `zone.items.font()`, `zone.items.sound()` and `zone.items.closure()`).

The for-each zone has the same style of collections for its three kinds of items — `zone.items` (per-element fields read inside the body), `zone.main_items` (per-element results written back onto the input geometry) and `zone.generated_items` (values stored on the generated geometry, with a `domain=` option). The closure zone declares its signature through `zone.inputs` and `zone.outputs`; an input item’s `output` is the socket read inside the body and an output item’s `input` is the target to feed.

``` python
with g.tree() as tree:
    # this initializes the zone with two socket inputs for each of the values
    # we manually specify the socket names
    zone = g.SimulationZone({"Value": g.Value(), "Vector": g.Vector()})
    zone.input.o["Value"] + 10 >> zone.output

    # this should automatically pick the vector input socket because we are
    # explicit about the VectorMath and it will be the most compatible
    zone.input >> g.VectorMath.add(..., (0.2, 0.4, 0.6)) >> zone.output

tree
```

## Item Nodes

Several regular nodes are also driven by dynamic item collections — Capture Attribute, Bake, Field to Grid, Field to List, Format String, Combine/Separate Bundle, Closure to List, Evaluate Closure, Index Switch and Menu Switch. They all expose the same `items` collection as the zones, alongside their `items=` constructor argument (a name-to-value mapping, or a list of values named after their sources):

- `CaptureAttribute(...).items.vector(g.Position())` returns an `Item` handle — `item.input` is the field being captured, `item.output` the captured result. The item is named “Position” after its source; pass a name as the second argument to choose one.
- `Bake().items.geometry(source, "Geo")` works the same way for bake items.
- `FieldToGrid.float(topology).items.float(field, "Density")` returns an `Item[FloatSocket, FloatSocketGrid]`: `item.input` is the field input socket and `item.output` the evaluated grid, each with its own socket class. `FieldToList` items pair a field with its list socket the same way.
- `CombineBundle().items.float(0.5, "a")` and `SeparateBundle(bundle).items.float("a")` declare bundle items; the socket is `item.input` (the value fed into the bundle) or `item.output` (the value read from it).
- `EvaluateClosure(closure).inputs.geometry(source, "Geo")` and `.outputs.vector("Force")` declare the closure-call signature; the result socket is `item.output`.
- `MenuSwitch.float().items.new(0.5, "Option", description="...")` and `IndexSwitch.float().items.new(0.5)` add switch items, typed by the switch’s data type.

A handle stands in for its sockets, so it can be used where a socket is expected: as a node argument or on the left of `>>` it is `item.output`, on the right of `>>` it is `item.input`, and the chain then continues from `item.output`. An item with only one side (a Separate Bundle item has only an output, a Combine Bundle item only an input) raises when the other side is asked for. Zone state items have two inputs and two outputs, so they keep asking for the role: `initial`, `current`, `next` or `result`.

``` python
with g.tree() as tree:
    cap = g.CaptureAttribute(g.Cube())
    pos = g.Position() >> cap.items.vector()
    cap.o.geometry >> g.SetPosition(position=pos * 2) >> tree.outputs.geometry()

tree
```

The bundle and closure factories also accept `structure_type=` for non-`"AUTO"` socket shapes.

``` python
with g.tree() as tree:
    cap = g.CaptureAttribute.face(g.Cube())
    pos = cap.items.vector(g.Position(), "Pos")
    (
        g.StoreNamedAttribute.face.vector(cap.o.geometry, name="pos", value=pos.output)
        >> tree.outputs.geometry()
    )

tree
```
