# nodebpy API reference for agents

Idioms beyond the core ones in SKILL.md. Every snippet runs inside a
`with g.tree(...) as tree:` block with `from nodebpy import geometry as g`.

## Contents
1. Tree constructors
2. Node arguments in detail
3. Socket access and socket methods
4. Operators
5. Group interface
6. Zones (repeat, simulation, for-each, closure)
7. Item nodes (capture attribute, bake, field to grid)
8. Switches (Switch, IndexSwitch, MenuSwitch)
9. Layout options
10. Shader and compositor specifics

## 1. Tree constructors

| Call | Builds | Notes |
|---|---|---|
| `g.tree(name, *, collapse=False, arrange="sugiyama", clear=False)` | Geometry node group | No `fake_user`; use `TreeBuilder.geometry(name, fake_user=True)` if needed. |
| `s.tree(name, *, fake_user=False, clear=False, ...)` | Shader node group | |
| `s.material(name, *, fake_user=False, ...)` | Material; `.material` is the `bpy.types.Material` | No `clear`; see SKILL.md section 6. |
| `c.tree(name, *, fake_user=False, clear=False, ...)` | Compositor node group | |
| `TreeBuilder(bpy_tree_or_name, tree_type="GeometryNodeTree", clear=False, ...)` | Wrap an existing tree or make one | Also `TreeBuilder.geometry/.shader/.compositor(...)`. |

Useful attributes on the builder: `tree.tree` (bpy NodeTree), `len(tree)` (node count),
`tree.inputs`, `tree.outputs`, `tree.link(out_socket, in_socket)`, `tree.arrange()`,
`tree.to_python()`, `tree.to_mermaid()`, `tree.to_plot(path)`.

Group node usage of an existing bpy group inside a tree: `TreeBuilder(node.node_tree)`
wraps it for inspection.

## 2. Node arguments in detail

- Keyword names match the socket identifier, then the name, then title-cased forms:
  `value=` hits "Value", `a_vector=` hits Mix's "A" vector socket.
- Scalars broadcast to vectors: `g.SetPosition(offset=0.1)` sets (0.1, 0.1, 0.1).
- Enum properties can also be set after creation: `node.data_type = "FLOAT_VECTOR"`.
- `g.Compare(operation, data_type, **sockets)` takes its two enums positionally, unlike
  other nodes; prefer `g.Compare.float.less_than(a, b)` or the `<` operator.
- `...` placeholders: `g.InstanceOnPoints(g.Cube(), instance=...)` makes the next `>>`
  fill `instance` rather than the first compatible socket.
- `x >> None` returns `x` unchanged, handy for optional pipeline steps.
- Nodes that take a datablock (Object Info, Image Texture, Collection Info):
  `g.ObjectInfo(object=bpy.data.objects["Cube"])`, or set
  `node.i.object.default_value = obj`. Non-socket datablock properties go on the raw
  node: `img.node.image = bpy.data.images["x.png"]`.

## 3. Socket access and socket methods

```python
sep = g.SeparateXYZ(g.Position())
sep.o.x                       # attribute access, snake_case
sep.o["X"], sep.o[0]          # by name / index
g.CombineXYZ(*sep.o)          # accessors iterate
sep.o.y >> g.Math.sine()      # link a specific output
```

`socket.socket` is the bpy socket, `socket.node` the bpy node, `socket.links` its links,
`socket.default_value` the value on an unlinked input.

Methods by socket type (all return new sockets/nodes). This is a highlight list; the
complete, current list for any type comes from `python scripts/lookup.py socket <Type>`.

- **Vector**: `.x .y .z` (shared Separate XYZ), `.length()`, `.dot(v)`, `.cross(v)`,
  `.distance(p)`, `.normalize()`, `.project(v)`, `.reflect(n)`, `.scale(s)`,
  `.map_range(...)`, `.rotate(rotation)` (Rotate Vector; `rotation` may be an Euler
  tuple), `.transform(matrix)`, `.align_rotation(...)`.
- **Float / Integer**: `.sin()`, `.clamp(min, max)`, `.map_range(from_min, from_max, to_min, to_max)`,
  `.to_string()`, `.mix.color(a, b)`.
- **Boolean**: `.switch.float(false, true)`, `.switch.geometry(...)`, `.switch.vector(...)`.
- **Color**: `.r .g .b .a`.
- **Matrix**: `.translation`, `.rotation`, `.scale`, `.invert()`, `.determinant()`, `.svd()`.
- **String**: `.format({...})`, `.find(s)` -> `(first, count)`, `.slice(...)`,
  `.starts_with(...)`, `.split(...)`, `.to_float()`.
- **Rotation**: `.rotate(by, rotation_space="LOCAL")` (Rotate Rotation), `.invert()`,
  `.to_euler()`, `.to_axis_angle()`, `.to_quaternion()`, `.align_to_vector(v, axis=...)`.
- **Domain methods on any field** (`.point`, `.face`, `.edge`, `.corner`, `.spline`,
  `.instance`, `.layer`): `.min/.max/.mean/.median/.std_dev/.variance(group_index)`,
  `.total/.leading/.trailing(group_index)` (Accumulate Field), `.at(index)`,
  `.evaluate()`. E.g. `pos.map_range(pos.point.min(), pos.point.max())`,
  `idx == idx.point.min(g.MeshIsland().o.island_index)` (first vertex per island).
  Prefer these over creating the statistic node unless you use several of its outputs.

When unsure whether a method exists, `dir(sock)` on the socket you have.

## 4. Operators

| Python | Node created |
|---|---|
| `a + b`, `- * / ** %` | Math (float), IntegerMath (both ints), VectorMath (any vector); reversed operands work (`2.0 ** x`) |
| `a // b` | IntegerMath DIVIDE_FLOOR for ints, Divide + Floor for floats |
| `-a`, `abs(a)` | Multiply by -1 / Negate / Scale -1; Absolute |
| `a < b` etc., `a == b`, `a != b` | Compare (data type from the operands) |
| `a & b`, `a \| b`, `a ^ b`, `~a` | Boolean Math AND / OR / NOT_EQUAL / NOT |
| `m @ n`, `m @ v` | Multiply Matrices; Transform Point when the right side is a vector |

Integer x float mixes pick the float node from the dominant type. A scalar socket
with a 3-tuple promotes to Vector Math (`dt * (0, 0, -9.8)` is Scale, `x + (1, 2, 3)`
is Add). When you want an
explicit node, call it: `g.Math.multiply(g.Index(), x)`, `g.VectorMath.cross_product(a, b)`.
Compare nodes for Python `==` means `if node_a == node_b:` is always truthy; use `is`.

## 5. Group interface

```python
geo    = tree.inputs.geometry("Geometry")                        # no default for geometry
count  = tree.inputs.integer("Count", 10, min_value=1, max_value=1000)
factor = tree.inputs.float("Factor", 0.5, min_value=0.0, max_value=1.0, subtype="FACTOR")
dist   = tree.inputs.float("Distance", 0.1, subtype="DISTANCE", description="Tooltip")
pos    = tree.inputs.vector("Position", default_input="POSITION", hide_value=True)
axis   = tree.inputs.vector("Axis", (0, 0, 1))
mode   = tree.inputs.menu("Mode", "Mesh")   # must be linked to a MenuSwitch with a "Mesh" item
with tree.inputs.panel("Advanced", default_closed=True):
    seed = tree.inputs.integer("Seed", 0)
out    = tree.outputs.geometry("Geometry")
mask   = tree.outputs.boolean("Selection")
grid   = tree.outputs.float("Density", structure_type="GRID")
```

Types: `float integer boolean vector color rotation matrix string menu object geometry
collection image material font sound bundle closure shader`. Common keywords:
`min_value`, `max_value`, `subtype`, `hide_value` (field inputs), `hide_in_modifier`,
`default_input` ("POSITION", "INDEX", ...), `attribute_domain`, `structure_type`
("AUTO"/"FIELD"/"SINGLE"/"GRID"), `dimensions` (vector), `expanded` (menu),
`is_panel_toggle` (boolean).

A menu input's default is applied when the tree closes and must name an item of the
MenuSwitch it is linked to; an unlinked menu input with a default raises
`TypeError: enum "Mesh" not found`.

Every call adds one socket. Call each once and keep the variable; `tree.outputs` is not
subscriptable. `with tree.panel("Name"):` makes a panel holding inputs and outputs.

## 6. Zones

**Repeat**

```python
zone = g.RepeatZone(10)                       # iteration count (can be linked)
geo = zone.items.geometry("Geometry", g.Cube())   # second arg links the initial value
offset = g.RandomValue.vector(seed=zone.iteration)
geo.current >> g.SetPosition(offset=offset * 0.1) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

A `ZoneItem` has four sockets: `.initial` (input node input), `.current` (read inside
the zone), `.next` (write inside the zone), `.result` (after the zone). Factories:
`zone.items.float/integer/boolean/vector/color/rotation/matrix/string/geometry/bundle`,
plus datablock types on repeat zones only. `zone.item(name, initial, type="GEOMETRY")`
is the string-typed form.

**Simulation**: same item API; `sim.delta_time` gives the step.

```python
sim = g.SimulationZone()
geo = sim.items.geometry("Geometry", g.Points(100))
vel = sim.items.vector("Velocity", (0, 0, 0))
new_vel = vel.current + sim.delta_time * (0, 0, -9.8)
new_vel >> vel.next
geo.current >> g.SetPosition(offset=new_vel * sim.delta_time) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

Simulation zones only step when the frame changes in a real scene; headless evaluation
at frame 1 shows the initial state.

**For each element**

```python
zone = g.ForEachGeometryElementZone(geometry, selection=True, domain="POINT")
pos = zone.inputs.vector("Pos", g.Position())       # .input (field in) / .output (value in body)
zone.main.float("Out", pos.output.x)                 # per-element result written back
zone.generated.geometry("Gen", g.Cube(size=0.1))     # geometry generated per element
# zone.index, zone.element; results on zone.output.o.<name>, default generated at zone.output.o.generation_0
```

**Closure**: `cz = g.ClosureZone(); a = cz.inputs.geometry("Geo"); out = cz.outputs.geometry("Out")`;
evaluate with `g.EvaluateClosure(cz.closure).inputs.geometry("Geometry", g.Cube())`.

## 7. Item nodes

```python
cap = g.CaptureAttribute.face(g.Cube())
normal = cap.items.vector("Normal", g.Normal())
cap >> g.SetPosition(offset=normal.output * 0.1)   # .output is the captured field
```

Dict form: `g.CaptureAttribute(geo, items={"Pos": g.Position(), "Mask": "BOOLEAN"})` (a type
name string declares an unlinked item). `g.Bake().items.geometry("Geo", g.Cube())`.
`g.FieldToGrid.float().items.float("Density", 0.5)` returns `.field` / `.grid`.

## 8. Switches

```python
g.Switch.geometry(condition, false_geo, true_geo)
(value > 0.5).switch.float(0.0, 1.0)
g.IndexSwitch.geometry(index, [g.Cube(), g.IcoSphere(), g.Cone()])
g.IndexSwitch.float(items=range(10))
mode = tree.inputs.menu("Shape", "Cube")
g.MenuSwitch.geometry(mode, {"Cube": g.Cube(), "Sphere": g.UVSphere()})
```

MenuSwitch items may be `(value, "description")` tuples; `switch.item("Name", value)` returns
a `MenuItem` with `.is_selected` (a boolean socket).

## 9. Layout options

- `arrange="sugiyama"` (default, needs networkx), `"simple"`, or `None` to keep positions.
- `SugiyamaOptions(direction="BALANCED", add_reroutes=False, margin=(30, 30), ...)` and
  `SimpleOptions(spacing=(50, 25))` from `nodebpy` for fine control.
- `nodebpy.arrange(bpy_tree, method)` re-arranges any tree, including hand-made ones.
- `collapse=True` collapses nodes (compact trees).

## 10. Shader and compositor specifics

- Import `from nodebpy import shader as s` / `compositor as c`. Class names follow the UI:
  `s.PrincipledBSDF`, `s.NoiseTexture`, `s.ColorRamp`, `s.TextureCoordinate`,
  `c.Blur`, `c.Glare`, `c.Kuwahara`.
- Shader operators build Math / VectorMath nodes; comparisons become Math
  GREATER_THAN / LESS_THAN (there is no Compare node in shader trees).
- `s.MenuSwitch.shader(items={...})` and `c.MenuSwitch.color(menu, {...})` exist.
- Compositor groups take `t.inputs.color("Image")` and output `t.outputs.color("Image")`.
  Frames work as in geometry trees (`with c.Frame("Label"):`).
- Materials read geometry-node attributes via `s.Attribute(attribute_name="name")`
  (`attribute_type="INSTANCER"` for attributes stored on instances).
