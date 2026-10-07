---
name: nodebpy
description: Build, edit and verify Blender node trees (Geometry Nodes, shader materials, compositor) as Python code with the nodebpy library. Use whenever the task involves writing or changing a Blender node tree, node group or material from Python, porting a hand-made node setup to code, turning an existing .blend node tree into code (to_python), writing reusable node-group classes (CustomGeometryGroup), or running/rebuilding trees in a live Blender session or headless with the bpy module, even if the user just says "geometry nodes", "make a node group", or "a material with nodes" without naming nodebpy.
---

# Writing Blender node trees with nodebpy

nodebpy turns node trees into ordinary Python: every Blender node is a typed class,
instantiating it inside a `with ... tree(...)` block adds it to that tree, `>>` links
nodes, and Python operators build Math / Compare / Boolean nodes. Treat the Python as
the source of truth and the Blender tree as its build product.

Read [references/api.md](references/api.md) for the full idiom catalogue (sockets,
operators, interface options, zones, item nodes, switches, shader and compositor).
Read [references/groups-and-codegen.md](references/groups-and-codegen.md) for reusable
group classes, turning existing trees into code, live re-runs, and asset libraries.

## 1. Running code

nodebpy needs a real Blender runtime: either the `bpy` pip module (headless) or
Blender's own Python.

**Headless (preferred for writing and checking a tree).** The `bpy` wheel must match
the Blender version nodebpy targets: nodebpy versions are `BLENDER.MINOR.PATCH`, so
`520.x` wants Blender/bpy 5.2+. Python 3.13.

```bash
uv add nodebpy "bpy==5.2.*" matplotlib   # matplotlib only for tree.to_plot()
BLENDER_USER_EXTENSIONS=/nonexistent uv run python build_tree.py
```

- `BLENDER_USER_EXTENSIONS=/nonexistent` stops an installed Blender extension (e.g.
  Molecular Nodes) bundling an older nodebpy wheel from shadowing the one in the venv.
  Also `import nodebpy` before `import bpy`.
- Layout needs no extra package: trees are arranged when the `with` block exits.
- A headless session starts from the factory scene (a `Cube` object exists). Nothing is
  saved unless you call `bpy.ops.wm.save_as_mainfile(filepath=...)`.
- Don't name your scripts after stdlib modules (`inspect.py`, `types.py`, ...): the
  script's directory is first on `sys.path`, and `import bpy` crashes with an obscure
  glog "InitGoogleLogging() twice" error.

**Inside a running Blender** (text editor, Blender MCP `execute_blender_code`, an
add-on): the same code works. Rebuild in place with `clear=True` so objects keep their
modifiers (section 5).

## 2. The core idioms

```python
from nodebpy import geometry as g   # shader as s, compositor as c

with g.tree("Scatter Cubes", clear=True) as tree:
    count = tree.inputs.integer("Count", 50, min_value=0)
    scale = tree.inputs.float("Scale", 0.1, min_value=0.0)

    (
        g.Points(count, position=g.RandomValue.vector(min=-1))
        >> g.InstanceOnPoints(instance=g.Cube(), rotation=g.RandomRotation(seed=2), scale=scale)
        >> g.RealizeInstances()
        >> tree.outputs.geometry("Geometry")
    )
```

- **Nodes are classes named after the UI label**: "Random Value" becomes `g.RandomValue`.
  Variants (data type, domain, operation) are class methods, ordered
  mode > domain > data type > operation: `g.Math.sine(x)`, `g.Compare.float.less_than(a, b)`,
  `g.StoreNamedAttribute.point.vector(name="vel", value=v)`, `g.Switch.geometry(cond, false, true)`.
- **Socket inputs are constructor arguments** (positional or keyword, snake_case of the
  socket name). A value can be a node (its best output is used), a socket, a plain
  Python value (sets the default), a list (links every item into a multi-input socket
  such as Join Geometry), `None` (leave alone) or `...` (fill this socket from the next
  `>>`).
- **Non-socket properties are keyword-only UPPER_CASE enums**: `data_type="FLOAT_VECTOR"`,
  `domain="FACE"`. Menu *sockets* (many former enums in Blender 5) take the item's
  display name: `g.ResampleCurve(mode="Count")`, `g.TransformGeometry(mode="Matrix")`.
- **`a >> b` links a's output into b's most compatible input and returns b**, so chains
  read left to right. Target a specific socket with `a >> b.i.offset`. The interface
  output goes on the right: `... >> tree.outputs.geometry("Geometry")`.
- **Sockets**: `node.i.<name>` / `node.o.<name>` (snake_case; duplicates become
  `value_001`), or `node.i["Name"]`, `node.o[0]`. Regular nodes have no `.inputs` /
  `.outputs`; the raw bpy node is `node.node`.
- **Operators on nodes and sockets create nodes**: `+ - * / ** % //` (Math, IntegerMath or
  VectorMath by type), `< <= > >= == !=` (Compare), `& | ^ ~` (Boolean Math), `@`
  (matrix multiply / transform point). `==` builds a Compare node, so never use it to test
  whether two nodes are the same object. A float socket with a 3-tuple uses Vector
  Math: `dt * (0, 0, -9.8)` is a Scale node.
- **Socket methods live on sockets, not nodes**: `g.Position().o.position.x`, not
  `g.Position().x`. They build the matching node for you and are usually the most
  readable form: `vec.length()`, `vec.normalize()`, `vec.rotate(rot)`, `vec.distance(p)`,
  `f.map_range(0, 1, -1, 1)`, `(pos.z > 0.5).switch.float(a, b)`, `rot.rotate(by)`,
  `rot.to_euler()`, `color.r`, `matrix.translation`, `string.split(",")`. List every
  method on a socket type with `nodebpy lookup socket Vector` (section 3).
- **Call methods on the value that flows on down the chain.** The socket you are
  transforming is the subject: `pos.transform(world)` (Transform Point), not
  `g.TransformPoint(pos, world).o.vector`; `world_pos.z`, not
  `g.SeparateXYZ(world_pos).o.z`; `g.SelfObject().o.self_object.matrix()` for the
  object's matrix, not `g.ObjectInfo(g.SelfObject()).o.transform`. Reach for the node
  class only when no socket method covers it or you need several of its outputs.
  `vec.transform(m)` applies translation (it is a point transform); for a *direction*
  such as gravity or a normal use `vec.transform_direction(m)` (Transform Direction) so
  the object's location does not leak into it. The two selector factories,
  `fac.mix.float(a, b)` and `(x > 0).switch.float(a, b)`, are the deliberate exceptions:
  they sit on the factor or condition and return the mixed or chosen value.
- **Per-domain field methods** replace most statistic/evaluate nodes. On any field
  socket, `.point`, `.face`, `.edge`, `.corner`, `.spline`, `.instance`, `.layer` give:
  `.min(group)`, `.max(group)`, `.mean(group)`, `.median(group)`, `.std_dev(group)`,
  `.variance(group)` (Field Min & Max / Average / Variance), `.total(group)`,
  `.leading(group)`, `.trailing(group)` (Accumulate Field), `.at(index)` (Evaluate at
  Index) and `.evaluate()` (Evaluate on Domain). `group` is an optional group index such
  as `g.MeshIsland().o.island_index`. When you need a single output, use the method:
  `first_in_island = idx == idx.point.min(island)`, not
  `idx == g.FieldMinAndMax.point.integer(idx, island).o.min`. Create the node itself
  only when you use several of its outputs (e.g. both `.o.min` and `.o.max`).
- **Interface sockets** come from `tree.inputs.<type>(name, default, description, ...)`
  and `tree.outputs.<type>(name)`; keep the returned socket in a variable to link it.
  Group them with `with tree.inputs.panel("Advanced", default_closed=True):`.
- **Expose the parameters a user would want to tweak**, beyond the ones the request
  names, but not ones another control already covers. For a generated arrow, the
  vertex count (resolution) is worth an input; its height and width are not, because the
  instance scale already covers them. Hard-coded magic numbers buried in the tree are
  the usual thing reviewers ask to have exposed.
- **Frames**: `with g.Frame("Label"):` parents every node created in the block.
- **Fields are evaluated where they are consumed**, not where you wrote them. A field
  built from `g.Position()` and used after a Set Position sees the *moved* points. To
  store or reuse a value computed from the original geometry, store it (or
  `g.CaptureAttribute`) before the node that changes the geometry. The same applies to
  context: after Mesh to Points, Instance on Points or Realize Instances, fields such as
  Mesh Island or a per-island Field Min & Max no longer mean what they did on the mesh,
  so capture those values first.
- **Primitive origins differ**: `g.Cone()` has its origin at the base (spans z 0 to depth),
  while `g.Cylinder()` and `g.Cube()` are centred. Offset accordingly when stacking them.
- Layout runs automatically when the `with` block exits (`arrange="sugiyama"`); you do
  not position nodes by hand.

### Prefer rotation and matrix sockets over Euler/vector workarounds

Blender now has dedicated rotation (quaternion) and matrix socket types, and trees
built on them are more correct and read better than the older Euler-vector idioms.
Reach for these first:

| Goal | Use | Instead of |
|---|---|---|
| Random rotation per point/instance | `g.RandomRotation(seed=...)` (an Essentials group: uniformly distributed) | `g.RandomValue.vector(max=2*pi)` into Euler to Rotation (biased distribution) |
| Rotate a vector | `pos.rotate((0, 0, pi))` (socket method) or `g.RotateVector(vector=pos, rotation=(0, 0, pi))`; a varying angle about an axis: `rotation=g.AxisAngleToRotation(axis=(0, 0, 1), angle=a)` | Vector Rotate node |
| Rotate/transform about another pivot | Build matrices and use `@`: `(g.CombineTransform(translation=p) @ g.CombineTransform(rotation=rot) @ g.CombineTransform(translation=-p)) @ pos` gives a Transform Point | Offsetting and re-offsetting vectors by hand |
| Combine rotations | `g.RandomRotation().o.rotation.rotate((0, 0, pi))`, `rot.rotate(by, rotation_space="LOCAL")`, or `g.RotateRotation(rotation, rotate_by=...)` | Adding Euler angles |

Euler tuples and vector sockets convert implicitly into rotation sockets, so
`rotation=(0, 0, pi)` works and an explicit Euler to Rotation node is optional. More
generally: check the bundled Essentials groups (`nodebpy lookup search` lists them with
bl_idname `GeometryNodeGroup`) before building a common operation from primitives. They
are what Blender users expect to see.

Plain Python functions that take and return sockets are the way to factor repeated
sub-graphs; for a sub-graph that should appear as one group node, write a
`CustomGeometryGroup` (see references/groups-and-codegen.md).

## 3. Finding the right node and its sockets

Guessing class names, socket names and enum strings is the main source of errors.
Look them up instead; it is fast:

```bash
nodebpy lookup search "named attribute"      # class, bl_idname, summary
nodebpy lookup show StoreNamedAttribute      # args, enum options, variants, outputs
nodebpy lookup show Mix --tree shader
nodebpy lookup socket Rotation               # methods on a socket type
nodebpy lookup socket                        # list socket types
```

`nodebpy` is the console script of the installed package (`uv run nodebpy ...` in a
uv project, or `python -m nodebpy ...`), so it always describes the version you have.
`print(g.SomeNode.__doc__)` gives the same information in numpydoc form. When you know
the bl_idname from an existing tree (`node.bl_idname == "GeometryNodeSetPosition"`),
search for it directly.

Other sources, in order of usefulness:
- the nodebpy tests, which are runnable examples of every idiom: `tests/test_usecases.py`,
  `test_operators.py`, `test_nodes.py`, `test_custom_groups.py` (in a checkout, or at
  https://github.com/BradyAJohnston/nodebpy/tree/main/tests);
- the docs at https://bradyajohnston.github.io/nodebpy;
- the installed source (`python -c "import nodebpy; print(nodebpy.__path__)"`):
  `builder/` for the machinery, `nodes/` for the generated node classes, `live.py` for
  in-session rebuild helpers.

## 4. Verify what you built

Building without errors is not the same as building the right tree: `>>` picks sockets
by heuristic, and an unlinked input silently uses its default. Check the result before
reporting success. Pick whichever of these fit the task:

1. **Look at it.** `tree.to_plot("tree.png")` draws the tree the way Blender's editor
   does (needs matplotlib). Open the image and check that every link goes where you
   meant, and that no input you meant to drive is showing a default value widget.
   `tree.to_plot("group.png", node=True)` draws the group as the single node users see,
   which shows the interface. `print(tree.to_mermaid())` gives a text version of the links.
2. **Check structure.** `len(tree)` (node count), `len(tree.tree.links)`,
   `node.node.inputs["Offset"].is_linked`, `tree.tree.interface.items_tree`.
3. **Evaluate the geometry.** Attach the tree to an object and read the result:

   ```python
   import bpy
   obj = bpy.data.objects["Cube"]
   mod = obj.modifiers.new("GN", "NODES")
   mod.node_group = tree.tree                 # tree.tree is the bpy NodeTree, not `tree`
   ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
   mesh = ev.to_mesh()
   print(len(mesh.vertices), [a.name for a in mesh.attributes])
   ```

   `to_mesh()` only shows mesh data. For point clouds, curves and instances use
   `geo = ev.evaluated_geometry()` (a GeometrySet): `print(geo)` summarises counts, and
   `geo.pointcloud.attributes`, `geo.mesh`, `geo.curves` hold the components.
   Unrealized instances: `pc = geo.instances_pointcloud()` has one point per instance
   and an `instance_transform` FLOAT4X4 attribute (`pc.attributes["instance_transform"].data[i].value`
   rows; column 2 is the instance's local Z axis, column 3 its translation).
   Evaluated data (`to_mesh()`, `evaluated_geometry()` and its components,
   `instance_references()`) is owned by the depsgraph and freed on the next update,
   giving `ReferenceError: StructRNA of type ... has been removed`. Copy the values you
   need into plain Python lists straight away, keep the returned objects in variables
   while you read them, and evaluate again after each `frame_set` or input change.
   Simulation zones only advance when frames are stepped in order:
   `for f in range(scene.frame_start, n + 1): scene.frame_set(f)`, then evaluate.

   A plot shows wiring, not field semantics. When the tree computes something
   numeric (a displacement formula, a stored attribute), compare the evaluated values
   against the same formula in plain Python; that catches evaluation-order mistakes a
   correct-looking graph hides.

## 5. Changing a tree that already exists

- **Rebuild in place with `clear=True`**: `with g.tree("Name", clear=True) as tree:`
  reuses the datablock called "Name" (creating it if missing) and empties it, so
  modifiers and group nodes that point at it stay attached. Without `clear=True`, the
  same name makes a second tree `Name.001` and the modifier still shows the old one.
  `s.tree(...)`, `s.material(...)` and `c.tree(...)` take `clear=` too. For a tree you
  already hold: `TreeBuilder(existing_bpy_tree, clear=True)`.
- A group meant to be added as a modifier needs `is_modifier=True`
  (`g.tree("Name", is_modifier=True)`), and a node tool `is_tool=True`; both are also
  properties on the builder. Rebuilding with `clear=True` keeps the flags.
- `clear=True` keeps Geometry Nodes modifier input values: they are carried over by
  socket name, so keep existing input names unchanged when editing a tree a user has
  already tuned.
- **Start from the existing tree's code** instead of reverse-engineering it:
  `from nodebpy.export import to_python; print(to_python(bpy.data.node_groups["Name"], in_place=True))`.
  This works on hand-made trees too. Edit that code and run it; `in_place=True` makes the
  emitted header use `clear=True`.
- **Re-running a script that defines group classes** in a live session: use
  `nodebpy.live.run_source(code)`. A `CustomGeometryGroup` builds its tree once per
  session per `_name`, so re-running changed class code otherwise reuses the stale group.
  `run_source` rebuilds them, remaps users and keeps modifier input values.
- Rebuilding clears keyframes on node default values and resets simulation caches.
  Check `tree.tree.animation_data` first when editing a user's tree.
- Wire nodes with nodebpy, not `tree.links.new(...)`. Tweaking a property on an existing
  node through bpy is fine.

**Setting modifier inputs (Blender 5):** `mod["Socket_0"] = 1.0` raises
`TypeError: id properties not supported`. Set the input through attribute access on
the socket identifier (subscripting `inputs[...]` returns a raw IDPropertyGroup with no
`.value` attribute):

```python
ident = {i.name: i.identifier for i in tree.tree.interface.items_tree
         if i.item_type == "SOCKET" and i.in_out == "INPUT"}
getattr(mod.properties.inputs, ident["Count"]).value = 100
obj.update_tag()   # headless: otherwise the next evaluated_get() can return stale geometry
```

## 6. Shader and compositor trees

```python
from nodebpy import shader as s

with s.material("Rust", clear=True) as mat:     # starts empty; re-runs rebuild in place
    noise = s.NoiseTexture(scale=8.0)
    rust = s.Mix.color(noise.o.fac, (0.3, 0.1, 0.05, 1.0), (0.6, 0.25, 0.1, 1.0))
    bsdf = s.PrincipledBSDF(base_color=rust, roughness=noise.o.fac.map_range(0, 1, 0.4, 0.9))
    bsdf >> s.MaterialOutput()
obj.data.materials.append(mat.material)   # mat.material is the bpy.types.Material
```

- `s.material(name)` builds a material. `s.tree(name)` builds a shader node group with
  `tree.outputs.shader(...)`. `c.tree(name)` builds a compositor group.
- `s.material(name, clear=True)` reuses and rebuilds an existing material, so objects
  keep it assigned; without `clear=` a second run makes `Rust.001`.
- `Mix` variants take `(factor, a, b)`: `s.Mix.color(fac, a, b)`. Pass `a` explicitly:
  `x >> g.Mix.color(...)` links into Factor (the first compatible input), not A.
- Shader trees have no Compare node: `a > b` on shader sockets builds Math nodes.
- A shader output cannot feed a color input (raises `SocketError`).
- Read attributes stored by geometry nodes with
  `s.Attribute(attribute_type="INSTANCER", attribute_name="col")` when the attribute was
  stored on instances before `InstanceOnPoints`, and `attribute_type="GEOMETRY"` otherwise.

## 7. Errors and what they mean

| Error | Cause and fix |
|---|---|
| `RuntimeError: Node 'X' must be created within a TreeBuilder context manager` | Node class called outside `with g.tree(...)`. |
| `SocketError: No compatible output socket found for type ...` / `Cannot link any output ...` | `>>` found no socket pair of compatible types. Name the socket: `a.o.vector >> b.i.offset`, or pick the typed variant (`g.Switch.geometry`). |
| `RuntimeError: Socket 'A' ... is inactive` | Linking to a socket hidden by the node's current `data_type`/mode. Use the variant class method (`g.Mix.vector(...)`) so the right sockets are active. |
| `RuntimeError: ... is ambiguous` | Two sockets share that name; use `.i.value_001`, an index, or the identifier. |
| `AttributeError: 'Position' object has no attribute 'x'` | Socket method on a node; go through `.o.<socket>` first. |
| `TypeError: expected a NodeTree type, not TreeBuilder` | Assign `tree.tree`, not `tree`, to `mod.node_group`. |
| `TypeError: ... already exists as GeometryNodeTree ... Use a unique _name` | Two group classes share `_name` across tree types. |
| `CodegenError` from `to_python` | A node with no nodebpy class (usually legacy). Pass `strict=False` or register an emitter. |
| `RuntimeError` setting `.default_value` on a Group Input socket | Set interface defaults via the factory argument: `tree.inputs.float("X", 0.5)`. |

## 8. Checklist before you finish

1. Every node the task needs is present, looked up rather than guessed.
2. You ran the script and it exits cleanly.
3. You checked the result (plot, structure or evaluated geometry) and it matches the intent.
4. Interface sockets have sensible names, defaults, and `min_value`/`max_value` where
   a user could enter nonsense.
5. Existing trees were rebuilt with `clear=True` (or via `to_python(..., in_place=True)`),
   so nothing is left as a `.001` duplicate.
