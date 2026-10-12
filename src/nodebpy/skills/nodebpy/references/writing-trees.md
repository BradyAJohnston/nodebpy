# Writing trees: arguments, sockets, operators, interface

Every snippet runs inside `with g.tree(...) as tree:` with
`from nodebpy import geometry as g`.

## Contents
1. Tree constructors
2. Node arguments
3. Sockets and socket methods
4. Operators
5. The group interface
6. Rotations and matrices
7. Layout

## 1. Tree constructors

| Call | Builds |
|---|---|
| `g.tree(name, *, clear=False, is_modifier=None, is_tool=None, collapse=False, arrange="sugiyama", fake_user=False)` | Geometry node group (`g.tree` is `TreeBuilder.geometry`) |
| `s.tree(name, ...)`, `s.material(name, ...)` | Shader node group; material (`.material` is the `bpy.types.Material`) |
| `s.world(name, clear=False, scene=False)` | World node tree (`.world` is the World) |
| `c.tree(name, ..., scene=False)` | Compositor node group (`scene=True`: the scene's compositor) |
| `TreeBuilder(bpy_tree_or_name, tree_type="GeometryNodeTree", clear=False, ...)` | Wraps an existing tree (a group from a file) or makes one |

On the builder: `tree.tree` (the bpy NodeTree), `len(tree)` (nodes), `tree.inputs`,
`tree.outputs`, `tree.link(out_socket, in_socket)`, `tree.arrange()`,
`tree.to_python()`, `tree.to_mermaid()`, `tree.to_plot(path)`.

## 2. Node arguments

- Keywords match the socket identifier, then its name: `value=` is "Value",
  `a_vector=` is Mix's vector "A".
- A scalar broadcasts to a vector input: `g.SetPosition(offset=0.1)`.
- A tuple holding sockets is built into a Combine XYZ (vector inputs, Euler rotations)
  or the tree's Combine Color (color inputs; shader colors take 3 components):
  `g.Cube(size=(1, 1, height))`, `pos + (0, 0, height)`. A wrong length raises a
  `SocketError` naming the parts.
- Enum properties can be set after creation (`node.data_type = "FLOAT_VECTOR"`); an
  unknown value raises a `TypeError` suggesting the closest options.
- `...` placeholders: `g.InstanceOnPoints(g.Cube(), instance=...)` makes the next `>>`
  fill `instance`. `x >> None` returns `x`, for optional pipeline steps.
- Datablocks: `g.ObjectInfo(object=bpy.data.objects["Cube"])`, or
  `node.i.object.default_value = obj`; datablock *properties* go on the raw node
  (`img.node.image = bpy.data.images["x.png"]`).
- `g.Compare(operation, data_type, **sockets)` takes its enums positionally; prefer
  `g.Compare.float.less_than(a, b)` or `<`.

## 3. Sockets and socket methods

```python
sep = g.SeparateXYZ(g.Position())
sep.o.x, sep.o["X"], sep.o[0]   # attribute, name, index
g.CombineXYZ(*sep.o)            # accessors iterate
sep.o.y >> g.Math.sine()        # link one output
```

`socket.socket` is the bpy socket, `socket.node` its bpy node,
`socket.default_value` an unlinked input's value. Methods return new sockets (they add
nodes); `nodebpy lookup socket <Type>` is the full, current list. Highlights:

- **Vector**: `.x .y .z`, `.length()`, `.normalize()`, `.dot(v)`, `.cross(v)`,
  `.distance(p)`, `.project(v)`, `.reflect(n)`, `.scale(s)`, `.map_range(...)`,
  `.rotate(rotation)`, `.transform(m)` (point), `.transform_direction(m)` (direction),
  `.mul_add(m, a)`, `.min(v)` / `.max(v)` / `.floor()` / `.snap(step)` / `.wrap(...)`,
  `.to_spherical()` / `.to_cylindrical()`, `.euler_to_rotation()`, `.align_rotation(...)`.
- **Float**: `.sin()`, `.clamp(lo, hi)`, `.map_range(from_min, from_max, to_min, to_max)`,
  `.min(x)` / `.max(x)` (argument required), `.smooth_min(x, d)`, `.is_close(x, eps)`,
  `.to_string()`, `.mix.color(a, b)`.
- **Integer**: `.min(x)` / `.max(x)`, `.divide_round(x)`, `.gcd(x)`, `.to_float()`,
  `.shift(n)` / `.rotate(n)` (Bit Math).
- **Boolean**: `.switch.float(false, true)`, `.switch.geometry(...)`, ...
- **Color**: `.r .g .b .a`, `.gamma(g)`. **Matrix**: `.translation`, `.rotation`,
  `.scale`, `.invert()`, `.determinant()`, `.svd()`.
- **Rotation**: `.rotate(by, rotation_space="LOCAL")`, `.invert()`, `.to_euler()`,
  `.to_axis_angle()`, `.align_to_vector(v, axis=...)`.
- **String**: `.format({...})`, `.find(s)`, `.slice(...)`, `.split(...)`, `.to_float()`.
- **Object**: `.matrix(space)`, `.location(space)`, `.geometry(space, as_instance)`,
  `.camera_info()`, `.bone_info(name)`; **Collection**: `.instances(...)`, `.children()`.
- **Bundle**: `b.store("path", value)`, `b.get.float("path")`, `b.has("path")`,
  `b.paths()`, `a | b` (later wins); geometry: `geo.bundle()`, `geo.set_bundle(b)`.
- **Any field, any of seven types**: `.hash(seed)`; float/int/vector/color fields:
  `.blur(iterations, weight)`.
- **Per-domain** (`.point`, `.face`, `.edge`, `.corner`, `.spline`, `.instance`,
  `.layer`): `.min/.max/.mean/.median/.std_dev/.variance(group)`,
  `.total/.leading/.trailing(group)`, `.at(index)`, `.evaluate()`. Make the statistic
  node itself only when you use several of its outputs.

## 4. Operators

| Python | Node |
|---|---|
| `a + b`, `-`, `*`, `**`, `%` | Math (floats), Integer Math (both integers), Vector Math (a vector), Mix (two colors, keeping the left alpha) |
| `a / b` | Math divide; two integers give a float (true division) |
| `a // b` | Integer Math floor division for integers; Divide + Floor for floats |
| `a % b` on integers | floored modulo, as in Python (`g.IntegerMath.modulo()` is the truncated one) |
| `-a`, `abs(a)`, `round(a)`, `math.floor(a)` | negate; Absolute; Float to Integer (an integer socket) |
| `<`, `<=`, `>`, `>=`, `==`, `!=` | Compare, data type from both sides |
| `&`, `|`, `^`, `~` | Boolean Math on booleans; Bit Math on integers |
| `m @ n`, `m @ v` | Multiply Matrices; Transform Point when the right side is a vector |

A scalar socket with a 3-tuple uses Vector Math (`dt * (0, 0, -9.8)` is Scale).
Call the node for anything else: `g.Math.multiply(g.Index(), x)`,
`g.VectorMath.cross_product(a, b)`. Sockets have no truth value: `if`, `and`, `or`,
`max()` and `min()` raise, so use `.max()` / `.min()` or a Switch.

## 5. The group interface

```python
geo    = tree.inputs.geometry("Geometry")
count  = tree.inputs.integer("Count", 10, min_value=1, max_value=1000)
factor = tree.inputs.float("Factor", 0.5, min_value=0.0, max_value=1.0, subtype="FACTOR")
dist   = tree.inputs.float("Distance", 0.1, subtype="DISTANCE", description="Tooltip")
pos    = tree.inputs.vector("Position", default_input="POSITION", hide_value=True)
mode   = tree.inputs.menu("Mode", "Mesh")   # its default must be an item of the switch it feeds
shape  = g.MenuSwitch(mode, {"Mesh": g.Cube(), "Points": g.Points()})
with tree.inputs.panel("Advanced", default_closed=True):
    seed = tree.inputs.integer("Seed", 0)
tree.outputs.geometry("Geometry")
tree.outputs.float("Density", structure_type="GRID")
```

Types: `float integer boolean vector color rotation matrix string menu object geometry
collection image material font sound bundle closure shader`. Keywords include
`min_value`, `max_value`, `subtype`, `hide_value`, `hide_in_modifier`,
`default_input`, `attribute_domain`, `structure_type`, `dimensions`, `expanded`,
`is_panel_toggle`. Each call adds one socket; keep the variable. A menu input's
default is applied when the tree closes and must name an item of the Menu Switch it
feeds.

## 6. Rotations and matrices

| Goal | Use | Instead of |
|---|---|---|
| Random rotation | `g.RandomRotation(seed=...)` (Essentials, uniform) | Random Value vector into Euler to Rotation (biased) |
| Rotate a vector | `pos.rotate((0, 0, pi))`; about an axis: `pos.rotate(g.AxisAngleToRotation(axis=(0, 0, 1), angle=a))` | Vector Rotate |
| Transform about a pivot | `(g.CombineTransform(translation=p) @ g.CombineTransform(rotation=r) @ g.CombineTransform(translation=-p)) @ pos` | offsetting by hand |
| Combine rotations | `rot.rotate(by)`, `rot.rotate(by, rotation_space="LOCAL")` | adding Euler angles, or the deprecated Rotate Euler |

Euler tuples and vectors convert to rotation inputs, so `rotation=(0, 0, pi)` works.
Check the bundled Essentials groups (`nodebpy lookup search` lists them as
`GeometryNodeGroup`) before building a common operation from primitives.

## 7. Layout

- `arrange="sugiyama"` (default), `"simple"`, or `None` to keep positions.
- `SugiyamaOptions(...)` from `nodebpy` for fine control, passed as `arrange=`.
- `nodebpy.arrange(bpy_tree, method)` re-arranges any tree, including hand-made ones.
- `collapse=True` collapses the nodes.
