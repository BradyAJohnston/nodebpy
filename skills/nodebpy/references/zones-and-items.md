# Zones, item nodes and switches

Every snippet runs inside `with g.tree(...) as tree:` with
`from nodebpy import geometry as g`.

## Contents
1. The items API
2. Repeat zones
3. Simulation zones
4. For Each Element zones
5. Closure zones
6. Item nodes
7. Switches

## 1. The items API

Zones and items-driven nodes expose their items as one collection, `x.items`. The
typed methods take **the value first, then an optional name**, and name the item after
its source socket when no name is given (`zone.items.geometry(g.Cube())` is "Mesh").
`items.new(value, name, type="FLOAT")` chooses the type at runtime; `len(items)`,
iteration, `items[0]` and `items["Name"]` work. Omit the value to declare an unlinked
item: `zone.items.float(name="Count")`.

Each method returns an `Item` handle: `.input` is the socket it is fed through,
`.output` the socket it is read from. A handle stands in for its sockets: as an
argument or on the left of `>>` it is `.output`, on the right of `>>` it is `.input`
(and the chain continues from `.output`). One-sided items raise for the side they lack.

## 2. Repeat zones

```python
zone = g.RepeatZone(10)                               # iterations (can be linked)
geo = zone.items.geometry(g.Cube(), "Geometry")       # the value is the initial state
offset = g.RandomValue.vector(seed=zone.iteration)
geo.current >> g.SetPosition(offset=offset * 0.1) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

A zone item has four sockets: `.initial` (fed before the zone), `.current` (read
inside), `.next` (written inside), `.result` (after the zone). `>> geo.initial`
continues from `geo.current` and `>> geo.next` from `geo.result`, so a body can be one
chain: `g.Cube() >> geo.initial >> g.SetShadeSmooth() >> geo.next >> out`.

## 3. Simulation zones

```python
sim = g.SimulationZone()
geo = sim.items.geometry(g.Points(100), "Geometry")
vel = sim.items.vector((0, 0, 0), "Velocity")
new_vel = vel.current + sim.delta_time * (0, 0, -9.8)
new_vel >> vel.next
geo.current >> g.SetPosition(offset=new_vel * sim.delta_time) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

A simulation only advances when frames are stepped in order in a real scene; at frame
1 it shows the initial state ([verifying.md](verifying.md)). Storing state as a named
attribute instead of a zone item works too, and the order of Store Named Attribute and
Set Position then decides whether the offset sees this step's value.

## 4. For Each Element zones

```python
zone = g.ForEachGeometryElementZone.face(geometry, selection=True)
pos = zone.items.vector(g.Position(), "Pos")              # a field in, a value inside
zone.main_items.float(pos.output.x, "Out")               # written back per element
gen = zone.generated_items.geometry(g.Cube(size=0.1), "Gen")  # geometry made per element
# zone.index and zone.element inside; results on zone.output.o.<name>; the zone starts
# with no generated items, read each one's result on its handle (gen.output). A
# non-geometry generated item is stored on the geometry item declared before it.
```

## 5. Closure zones

```python
cz = g.ClosureZone()                      # s.ClosureZone in shader trees
x = cz.inputs.float("x")
x.output * 2 >> cz.outputs.float("y").input
call = g.EvaluateClosure(cz.closure)
call.inputs.float(3.0, "x")
result = call.outputs.float("y").output
```

## 6. Item nodes

```python
cap = g.CaptureAttribute.face(g.Cube())
normal = cap.items.vector(g.Normal())               # named "Normal" after its source
cap >> g.SetPosition(offset=normal.output * 0.1)    # .output is the captured field
```

- Constructor form: `g.CaptureAttribute(geo, items={"Pos": g.Position(), "Mask": "BOOLEAN"})`
  (a type name declares an unlinked item) or `items=[g.Position(), g.Normal()]`.
- `g.Bake().items.geometry(g.Cube(), "Geo")`; `g.FieldToGrid.float().items.float(0.5, "Density")`
  and `g.FieldToList(10).items.vector(pos)` give a field `.input` and a grid / list `.output`.
- Bundles: `g.CombineBundle().items.float(0.5, "a")` (`.input`),
  `g.SeparateBundle(bundle).items.float("a")` (`.output`); or the socket methods
  `bundle.store(...)` / `bundle.get.float(...)` ([writing-trees.md](writing-trees.md)).
- `g.FormatString("{x}", items={"x": 1.0})`.
- `g.Viewer(domain="POINT").items.float(height, "Height")` views a value (any type).
  The Viewer, the compositor's File Output and the shader Raycast have `.items` but no
  `items=` constructor argument ([shader-compositor.md](shader-compositor.md)).

## 7. Switches

```python
g.Switch(condition, g.Cube(), g.Cone())               # a Geometry switch, from its values
(value > 0.5).switch.float(0.0, 1.0)
g.IndexSwitch(index, [g.Cube(), g.IcoSphere(), g.Cone()])
g.IndexSwitch.float(items=range(10))
mode = tree.inputs.menu("Shape", "Cube")
g.MenuSwitch(mode, {"Cube": g.Cube(), "Sphere": (g.UVSphere(), "A tooltip")})
```

Without `input_type` / `data_type`, a switch takes its type from its values: a linked
value's socket type decides, plain values only when nothing is linked
(`g.Switch(cond, 1, 2)` is an Integer switch), and values of different types raise a
`SocketError` naming each. Use a typed variant (`g.Switch.float(...)`,
`g.IndexSwitch.vector(...)`) when the values don't say, such as an empty switch filled
later with `switch.items.new(value)`. Menu Switch items may be `(value, "description")`
pairs; `switch.items.new(value, "Name", description=...)` returns an item with
`.is_selected`. The first item declared is the default selection.
