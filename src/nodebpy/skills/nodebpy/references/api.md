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
| `g.tree(name, *, collapse=False, arrange="sugiyama", fake_user=False, clear=False, is_modifier=None, is_tool=None)` | Geometry node group | `g.tree` is `TreeBuilder.geometry`; `is_modifier=True` for a modifier group. |
| `s.tree(name, *, fake_user=False, clear=False, ...)` | Shader node group | |
| `s.material(name, *, fake_user=False, clear=False, ...)` | Material; `.material` is the `bpy.types.Material` | See SKILL.md section 6. |
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
complete, current list for any type comes from `nodebpy lookup socket <Type>`.

- **Vector**: `.x .y .z` (shared Separate XYZ), `.length()`, `.dot(v)`, `.cross(v)`,
  `.distance(p)`, `.normalize()`, `.project(v)`, `.reflect(n)`, `.scale(s)`,
  `.map_range(...)`, `.rotate(rotation)` (Rotate Vector; `rotation` may be an Euler
  tuple), `.transform(matrix)` (as a point: translation applies),
  `.transform_direction(matrix)` (as a direction: it does not), `.align_rotation(...)`.
- **Float / Integer**: `.sin()`, `.clamp(min, max)`, `.map_range(from_min, from_max, to_min, to_max)`,
  `.to_string()`, `.mix.color(a, b)`.
- **Boolean**: `.switch.float(false, true)`, `.switch.geometry(...)`, `.switch.vector(...)`.
- **Color**: `.r .g .b .a`.
- **Matrix**: `.translation`, `.rotation`, `.scale`, `.invert()`, `.determinant()`, `.svd()`.
- **Object**: `.matrix(space)`, `.location(space)`, `.rotation(space)`, `.scale(space)`,
  `.geometry(space, as_instance)` read the object through Object Info
  (`space` is `"ORIGINAL"` or `"RELATIVE"`); **Collection**: `.instances(...)`.
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

Every items-driven node and zone exposes its items as one collection: the typed
methods take **the value first, then an optional name**, and name the item after the
linked source socket when no name is given (`zone.items.geometry(g.Cube())` is named
"Mesh"). `items.new(value, name, type="FLOAT")` is the runtime-typed form, and the
collection supports `len(items)`, iteration and `items[0]` / `items["Name"]`. Each
method returns an `Item` handle whose `.input` is the socket the item is fed through and
`.output` the socket it is read from; `>> item.input` continues the chain from `.output`.

**Repeat**

```python
zone = g.RepeatZone(10)                       # iteration count (can be linked)
geo = zone.items.geometry(g.Cube(), "Geometry")   # the value links the initial state
offset = g.RandomValue.vector(seed=zone.iteration)
geo.current >> g.SetPosition(offset=offset * 0.1) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

A `ZoneItem` has four sockets: `.initial` (input node input), `.current` (read inside
the zone), `.next` (write inside the zone), `.result` (after the zone). `>> geo.initial`
continues from `geo.current` and `>> geo.next` from `geo.result`, so a zone body can
be one chain: `g.Cube() >> geo.initial >> g.SetShadeSmooth() >> geo.next >> out`.
Methods: `zone.items.float/integer/boolean/vector/color/rotation/matrix/string/geometry/bundle`,
plus datablock types on repeat zones only; omit the value to declare an unlinked item
(`zone.items.float(name="Count")`).

**Simulation**: same item API; `sim.delta_time` gives the step.

```python
sim = g.SimulationZone()
geo = sim.items.geometry(g.Points(100), "Geometry")
vel = sim.items.vector((0, 0, 0), "Velocity")
new_vel = vel.current + sim.delta_time * (0, 0, -9.8)
new_vel >> vel.next
geo.current >> g.SetPosition(offset=new_vel * sim.delta_time) >> geo.next
geo.result >> tree.outputs.geometry("Geometry")
```

Simulation zones only step when the frame changes in a real scene; headless evaluation
at frame 1 shows the initial state.

**For each element**

```python
zone = g.ForEachGeometryElementZone.face(geometry, selection=True)   # or domain="FACE"
pos = zone.items.vector(g.Position(), "Pos")         # .input (field in) / .output (value in body)
zone.main_items.float(pos.output.x, "Out")           # per-element result written back
zone.generated_items.geometry(g.Cube(size=0.1), "Gen")   # geometry generated per element
# zone.index, zone.element; results on zone.output.o.<name>; the default generated
# geometry is zone.generation (.input to feed, .output to read)
```

**Closure**: `cz = g.ClosureZone(); a = cz.inputs.geometry("Geo"); out = cz.outputs.geometry("Out")`;
read `a.output` in the body and feed `>> out.input`. Evaluate with
`g.EvaluateClosure(cz.closure).inputs.geometry(g.Cube(), "Geometry")` and read the
results from `.outputs.<type>("Name").output`.

## 7. Item nodes

```python
cap = g.CaptureAttribute.face(g.Cube())
normal = cap.items.vector(g.Normal())                # named "Normal" after its source
cap >> g.SetPosition(offset=normal.output * 0.1)     # .output is the captured field
```

Constructor form: `g.CaptureAttribute(geo, items={"Pos": g.Position(), "Mask": "BOOLEAN"})`
(a type name string declares an unlinked item) or `items=[g.Position(), g.Normal()]`
(named after the sources). `g.Bake().items.geometry(g.Cube(), "Geo")`.
`g.FieldToGrid.float().items.float(0.5, "Density")` and `g.FieldToList(10).items.vector(pos)`
return handles whose `.input` is the field and `.output` the grid or list.
`g.CombineBundle().items.float(0.5, "a")` (socket on `.input`) and
`g.SeparateBundle(bundle).items.float("a")` (socket on `.output`) declare bundle items;
`g.FormatString("{x}", items={"x": 1.0})` likewise.

## 8. Switches

```python
g.Switch.geometry(condition, false_geo, true_geo)
(value > 0.5).switch.float(0.0, 1.0)
g.IndexSwitch.geometry(index, [g.Cube(), g.IcoSphere(), g.Cone()])
g.IndexSwitch.float(items=range(10))            # or switch.items.new(value) afterwards
mode = tree.inputs.menu("Shape", "Cube")
g.MenuSwitch.geometry(mode, {"Cube": g.Cube(), "Sphere": g.UVSphere()})
```

MenuSwitch items may be `(value, "description")` tuples;
`switch.items.new(value, "Name", description="...")` returns a `MenuItem` with
`.is_selected` (a boolean socket). The first item declared becomes the default selection.

## 9. Layout options

- `arrange="sugiyama"` (default), `"simple"`, or `None` to keep positions. No extra
  package is needed.
- `SugiyamaOptions(margin=..., direction=..., socket_alignment=..., reroutes="none"|"blocked"|"all",
  straighten_trunk=True, pin_group_output=True, snap_to_grid=True, seed=0, ...)` from
  `nodebpy` for fine control; pass it as `arrange=`.
- `nodebpy.arrange(bpy_tree, method, selected_only=False)` re-arranges any tree,
  including hand-made ones.
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
