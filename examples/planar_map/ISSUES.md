# Issues found while building the planar map example

Things to file once the example settles: bugs and rough edges in nodebpy, in its
agent skill, and Blender behaviour that cost time. Each entry says what happened,
how it was worked around here, and what a fix could look like. Limitations of the
method itself are under "Open items in the method" in the README.

## nodebpy: bugs

### `__exit__` hides the exception raised inside `with g.tree(...)`
- **Seen:** `TypeError: The 'Data' menu has no option 'None': it has no items yet.`
  The real error was a `RuntimeError` from a bad link several lines earlier.
- **Cause:** `TreeBuilder.__exit__` runs `_apply_input_defaults()` even when the
  block is unwinding from an exception. The tree is half built, the Menu Switch
  never got created, so the default can't apply, and this new error replaces the
  original.
- **Fix:** in `__exit__`, skip the finishing steps (input defaults, mutes, layout)
  when an exception is propagating, or chain the original as `__context__`.

### Linking into an output socket gives Blender's opaque error
- **Seen:** `RuntimeError: Error: Same input/output direction of sockets`.
- **Cause:** `loops >> g.SeparateGeometry.spline(...).o.selection`. Attribute
  access binds tighter than `>>`, so the right-hand side is the node's *output*
  socket and `>>` tries to link into it.
- **Fix:** `__rshift__` should check the target is an input and raise
  "can't link into output socket 'Selection' of Separate Geometry; did you mean
  `(a >> node).o.selection`?".

### Positional argument to `g.RemoveNamedAttribute("keep")` gives a bare `AssertionError`
- **Seen:** `assert hasattr(input, "default_value")` in `_set_input_default_value`.
- **Cause:** the first positional parameter is `geometry`; the string went to a
  geometry socket, which has no default value.
- **Fix:** raise a `TypeError` naming the socket and the value's type ("'Geometry'
  takes a geometry, not str 'keep'"). Worth checking every node whose first
  parameter is a geometry and whose obvious positional is something else.

## nodebpy: typing

### `InputVector` rejects tuples that mix sockets and numbers
- **Seen:** `ty` error on `g.SetPosition(position=(q.x / -q.z, q.y / -q.z, 0.0))`:
  `found tuple[FloatSocket, FloatSocket, float]`.
- **Runtime:** works, and the skill documents it ("a tuple that mixes values and
  sockets ... becomes a Combine XYZ").
- **Workaround:** `g.CombineXYZ(...)`.
- **Fix:** widen `InputVector` (and colour / rotation equivalents) to accept
  `tuple[float | FloatSocket, ...]`.

### Group classes made by a factory lose their `__init__` signature
- **Seen:** `too-many-positional-arguments` on `WriteSplit(geometry, ...)` where
  `WriteSplit = writer(...)` returns `type[CustomGeometryGroup]`.
- **Workaround:** keyword arguments.
- **Fix:** probably not nodebpy's to fix; document a typed pattern for generated
  group classes (a `Protocol`, or `**kwargs` on the base `__init__`).

## nodebpy: improvements

### Socket methods on single-output nodes
- `perp(v) = g.CombineXYZ(-v.y, v.x)` then `.normalize()` raised
  `AttributeError: 'CombineXYZ' object has no attribute 'normalize'`; needed
  `.o.vector`. Forwarding unknown attributes from a node with one output to that
  output would make helpers like this read naturally.

### Setting modifier inputs by name
- 5.2 removed `mod[identifier] = value` for these inputs; it is now
  `getattr(mod.properties.inputs, identifier).value = value`, after looking the
  identifier up from the interface. `docs/examples/render.py` and
  `run_suzanne.py` both carry their own helper. A `nodebpy` helper
  (`set_modifier_input(mod, "Max Depth", 18)`) would save every script this.

### Layout of zones inside frames
- `BSP Cells` with fields fanning across a repeat zone laid out as a 564-node
  tangle, and the zone's frame drew as a slanted polygon rather than a box. Deferred
  by request, but the slanted frame looks like a layout bug on its own.

### Evaluation context is easy to get wrong
Two mistakes here were fields evaluated on a different geometry than intended,
with no error, just wrong output:
- `Offset Point in Curve` used in a selection after Curve to Points (no curve any
  more: every point deleted).
- A switch on a halfedge attribute inside Sample Index's `value`, which is
  evaluated on the *sampled* geometry, where that attribute doesn't exist.

Neither is a nodebpy bug, but the skill could say it plainly: "Sample Index,
Sample Nearest and Raycast evaluate their value field on the target geometry;
anything from the current geometry must be captured or chosen outside."

## Blender behaviour worth knowing (skill notes, possible reports)

### Grease Pencil fills need a `fill_id`
- Curves converted with Curves to Grease Pencil draw strokes only, whatever the
  material says. In 5.2 a stroke is filled only if its integer `fill_id` (curve
  domain) is non-zero; strokes sharing an id form one fill (holes).
  `MaterialGPencilStyle.show_fill` is deprecated and does nothing since 5.1.
- Found by reading `fill_cache_from_fill_ids` in `grease_pencil_fills.cc`.
- **Report?** Curves to Grease Pencil could offer to set `fill_id`, or the node's
  docs could mention it. **Skill:** add to the Grease Pencil notes.

### Field switches evaluate both branches
- With Separating Lines off, a pass still computes every separating-line field;
  depth 18 took 0.16 s instead of 0.07 s. Expected Blender behaviour, but worth a
  skill note: gate expensive work with a geometry Switch (which is lazy), not a
  field switch.

### Sort Elements orders groups by id
- Groups come out in ascending id order, sorted by weight within each group. This
  makes `(group = segment, weight = fraction)` a lexicographic sort. Confirmed by
  experiment; worth a line in the skill.

### Evaluate at Index out of range returns the type's default
- `curve.point.at(index - 1)` at index 0 returns 0. Here curve ids start at 1, but
  code that compares ids at neighbours needs an explicit range check.

## Repository

### The `ty` override for tests and examples misses `missing-union-attribute`
- `bpy.context.scene.camera` fails `ty` in `examples/` (and would in `tests/`):
  `bpy.context.scene` is `Scene | None`. The override in `pyproject.toml` relaxes
  `missing-attribute` but not `missing-union-attribute`, the rule this hits.
- **Workaround:** `bpy.data.objects["Camera"]`, or an `assert`.
- **Fix:** add `missing-union-attribute = "ignore"` to the override, or keep
  narrowing by hand.

## Environment

### Stale nodebpy in Blender's extension site-packages
- Known: scripts need `BLENDER_USER_EXTENSIONS=/nonexistent` and `import nodebpy`
  before `bpy`. `ruff`'s import sorting moves `bpy` above `nodebpy`, so driver
  scripts need `# isort: off` around those imports.
