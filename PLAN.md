# Codegen Project Plan

Goal: convert any Blender node tree back into idiomatic nodebpy Python — single
branches of nodes become single lines of math operators, `>>` chains, and
socket methods (`.curl()`, `.map_range()`, `.point.mean()`, …), matching the
style of `tests/test_usecases.py` and `nodes/geometry/groups.py`.

## Done

### Stage 1–3 (initial implementation)
- [x] Flat emission: every node as `var = g.ClassName(kwargs)` with linked
  inputs as kwargs, non-default literals, and non-default properties.
- [x] Chain stitching: linear first-socket runs rendered with `>>`.
- [x] Operator lifting: Math/VectorMath with binary Python operators.
- [x] Interface emission (`tree.inputs.*()` / `tree.outputs.*()`).
- [x] Snapshot + assertion test baseline (`tests/test_codegen.py`).

### Stage 4 (rewrite around expression IR — June 2026)
- [x] **Expression IR** (`Ref`, `Lit`, `Call`, `Attr`, `BinOp`, `UnaryOp`,
  `TupleExpr`): strings only produced in `render()`; parenthesisation derived
  from Python operator precedence. No more redundant parens or string surgery.
- [x] **Unified inlining**: a node consumed exactly once is substituted into
  its consumer (kwarg or `>>`). Chains emerge from recursion; the separate
  chain-finding pass is gone. `min_chain_length` gates only `>>` syntax.
- [x] **`register_emitter("bl_idname")`** registry for custom per-node
  generators; `EmitContext` provides `input_expr` / `upstream_expr` /
  `constructor` helpers. Built-in `Compare` emitter is the reference example.
- [x] **Lifting extended and corrected**: IntegerMath (`+ - * / ** % // -x
  abs()`), BooleanMath (`& | ^ ~`), float/vector `abs()`. Tables mirror
  `OperatorMixin` exactly (float `%` → FLOORED_MODULO, int `//` →
  DIVIDE_FLOOR). Lift refuses when extra links would be dropped.
- [x] **Bug fixes**:
  - inline chain tails no longer drop downstream links (orphaned-statement bug)
  - multi-input sockets emit tuples ordered by `multi_input_sort_id`
    descending (reproduces creation order)
  - missing upstream references raise `CodegenError` instead of silently
    skipping kwargs; `strict=True` raises on unsupported nodes
  - imports include only the aliases actually used (`g`/`s`/`c`)
  - group in/out matched by `bl_idname`, not node name
  - socket defaults probed on a scratch tree, never the user's tree
  - reroute fan-out collapsed before consumer counting (no duplicate emission)
  - positional-or-keyword node props (e.g. `Compare(operation=...)`) captured
    via `bl_rna.properties`; `NodeFrame` skipped; registry stores classes
- [x] **Structural round-trip tests**: generated code is exec'd and the
  rebuilt tree compared on node multisets (bl_idname, operation, data_type,
  domain, mode) + reroute-collapsed links. Covers hello-world surface,
  city-builder, boolean decoder, vector compare, multi-input join.

### Stage 5 (factory reverse-mapping — June 2026)
- [x] **Classmethod reverse table**: emits `g.Math.square_root(x)`,
  `g.Compare.float.less_than(a, b)`, `g.StoreNamedAttribute.point.integer(...)`
  instead of plain constructors with `operation=`/`data_type=` kwargs.
  Implemented by **AST-parsing the factory bodies at runtime** (no
  generate.py change needed — single source of truth, works for manual
  classes, parameterised factory instances resolve `self._domain`).
  Safety: a factory is used only when it covers *all* non-default props,
  every socket kwarg maps to a factory parameter, and factory parameter
  defaults that differ from the node's socket values get explicit kwargs.
  Unanalysable bodies (positional args, `**kwargs`, helper indirection like
  `Compare._VectorFactory._make`) fall back to the constructor. Leading
  consecutive parameters render positionally (`g.Math.sine(x)`).

### Stage 6 (socket-method table — June 2026)
- [x] **Socket-method table**: declarative `SocketMethodSpec` table renders
  nodes as methods on the socket feeding their primary input:
  `value.map_range(...)`, `cond.switch.float(a, b)`, `field.point.at(i)`,
  `.point.mean/median/min/max/std_dev/variance/leading/trailing/total()`,
  `.point.evaluate()`. Method paths template on node props
  (`{domain}` → point/spline/…, `{input_type}` → switch dtype); multi-output
  nodes (AccumulateField etc.) match the spec for the single output in use.
  Faithfulness guards: receiver socket type must match (so the method
  re-derives the same data_type on round-trip), all linked inputs covered by
  params, no uncovered non-default props.
- [x] **SeparateXYZ dissolves to `vec.x` / `vec.y` / `vec.z`** via per-output
  expressions; the source is auto-promoted to a variable
  (`position = g.Position().o.position`) when referenced more than once, so
  repeated accessors reuse one node through `_find_or_create_linked`.
- [x] **Expression kind tracking** (`_Val`): node- vs socket-valued
  expressions, output pinning, and per-output maps — the foundation for
  receiver-based emission (`ctx.socket_expr()` forces `.o.<name>` on
  node-valued upstreams).

### Stage 7 (broadened spec table — June 2026)
- [x] **Vector methods**: `.dot()`, `.length()`, `.normalize()`, `.cross()`,
  `.distance()`, `.project()`, `.reflect()` (VectorMath ops without operator
  equivalents), `.rotate(rotation)` (RotateVector), `.transform(matrix)`
  (TransformPoint).
- [x] **String methods**: `.slice()`, `.replace()`, `.reverse()`,
  `.length()`, `.uppercase()`/`.lowercase()` (SetStringCase), and
  `.starts_with()`/`.ends_with()`/`.contains()` (MatchString) — menu-socket
  constants handled via the new `require_sockets` spec field.
- [x] **Matrix/rotation methods**: `.invert()`, `.transpose()`,
  `.determinant()`, `.transform_direction()`, rotation `.invert()`,
  `.rotate()`, `.to_euler()`.
- [x] **`Clamp` → `.clamp(min, max)`** (MINMAX only).
- [x] **Generalised dissolution table** (`DissolveSpec`): SeparateTransform →
  `mat.translation/.rotation/.scale`, SeparateColor (RGB mode) →
  `col.r/.g/.b/.a`, alongside SeparateXYZ.
- [x] Fixed `_non_default_props` collision with base-Node rna properties
  (socket param `color` shadowed the node UI ``color`` property).

### Stage 8 (items API + zone emitters — June 2026)
- [x] **Items API unification** (full design + completion notes in
  [ITEMS_API_PLAN.md](ITEMS_API_PLAN.md)): single `ItemsMixin` for all
  variable-items nodes, `Item`/`ZoneItem` handles (`item.current` /
  `item.next` / `item.result`), `capture(value, name=...)`, unified
  `items=` kwarg with type-string declarations, zone wrapper unpacking,
  dead-param/monkeypatch fixes.
- [x] **Zone emitters**: Repeat/Simulation/ForEach paired nodes emit the
  canonical handle form — `zone = g.RepeatZone(n)` +
  `h = zone.item("name", initial)` lines at the input node's position
  (in creation-counter order so socket identifiers round-trip), deferred
  `expr >> h.next` statements at the output node's position, and both bpy
  nodes dissolved into per-output handle expressions. `_topo_sort` gains
  a synthetic input→paired-output edge; emitters may return `_Val` to
  dissolve nodes; `DictExpr` IR added for items dicts. ForEach's default
  generation item maps to the new `zone.generation` handle. Fixed
  `RepeatZone` linking `Iterations` before pairing (inactive sockets).
  Known gaps: non-default *unlinked* `Skip` values, hand-built zones
  whose first generation item isn't the default, item reordering.

- [x] **String emitters + Compare lifting + float32 literals**:
  `FormatString` → `fmt.format({...})` / `g.FormatString("...", items={...})`
  and `StringJoin` → `delim.join((...))` / `g.JoinStrings((...))` custom
  emitters; Compare lifts to `a < b` (always-parenthesised `CompareOp` IR)
  when state matches the operator overloads (ELEMENT mode, lhs-type
  dispatch, default epsilon on `==`/`!=`); float literals emit the shortest
  decimal that round-trips through float32. Items with plain default values
  (`items={"label": "hello"}`) now supported via `_add_unlinked_input`.

- [x] **Remaining socket-method specs**: `Mix` → `factor.mix.*` (new
  `always_args` spec field — required params render even at default values);
  `TupleMethodSpec` for NamedTuple-returning methods (`.find()`, `.svd()`,
  `.to_quaternion()`, `.to_axis_angle()`) — outputs map to tuple attributes,
  bound to a variable when consumed more than once; GridInfo dissolves into
  `.transform`/`.background_value` (builder `_info()` now reuses one GridInfo
  per grid socket); `_output_expr` falls back to identifiers for duplicated
  output names (Mix's four "Result" sockets). Future: `.curl()` /
  `.divergence()` / `.laplacian()` when those exist.

### Stage 9 (polish — June 2026)
- [x] **Line-length handling**: `max_inline_width` budget (default 88) binds
  long expressions to a variable instead of inlining; top-level `>>` chains
  that still exceed the width wrap in parentheses with one segment per line.
- [x] **Interface fidelity**: every keyword-only parameter of the
  `SocketContext` builder methods (`subtype`, `min_value`/`max_value`,
  `hide_value`, `structure_type`, …) is compared against a probed fresh
  interface socket and emitted when non-default; `description` and panels
  (as `with` blocks; nested panels are inexpressible and skipped) included.
- [x] **Frames**: `with g.Frame("..."):` blocks re-emitted from node
  parenting via a cluster-level topological sort; interleaved frames fall
  back to flat emission.
- [x] **Tree type detection**: shader/compositor trees emit
  `TreeBuilder.shader(...)` / `TreeBuilder.compositor(...)`.
- [x] **TreeBuilder UX**: codegen/diagram moved behind `export/`;
  `tree.to_python()` method and `_repr_markdown_` integration.
- [x] **Parametrised usecase round-trip**: every tree built in
  `tests/test_usecases.py` is exposed as a `build_*() -> TreeBuilder`
  function (collected in `ROUNDTRIP_BUILDERS`) and round-tripped by
  `test_roundtrip_usecases` in test_codegen.py. Found and fixed:
  `_make_var` produced invalid identifiers (Python keywords like `with`,
  punctuation as in "Extent (unit)", leading digits). Two strict xfails
  document the open gaps below.
- [x] **MenuSwitch/IndexSwitch emitters**: MenuSwitch emits the factory
  dict form (`g.MenuSwitch.geometry(menu, {"Name": value, ...})`) so enum
  item names round-trip; IndexSwitch emits the factory tuple form
  (`g.IndexSwitch.float(index, (a, b, ...))`). Along the way: `items=`
  values of `None` declare an unlinked item (type comes from the node
  `data_type`), an explicit string `menu=` selection is no longer clobbered
  by the first-item default, and the ambiguous `*NodeGroup` bl_idnames were
  dropped from the codegen registry (group nodes now report unsupported
  instead of emitting an arbitrary `CustomGeometryGroup` subclass).
- [x] **Recursive node groups**: a group node round-trips as a
  `Custom{Geometry,Shader,Compositor}Group` subclass whose `_build_group`
  recreates the inner tree, instantiated as
  `GeneratedClass(**{"Socket Name": value, ...})`. `to_python` body was
  split into a per-tree `_emit_tree` (returning `_TreeEmission`) plus
  module assembly; a `_GroupCollector` threads through `EmitContext`,
  deduplicates inner trees by name, renders each class once, and orders
  them innermost-first (a group is appended only after the groups it
  nests). Only linked inputs and unlinked inputs that differ from the
  group's own interface default are passed; the `GroupCall` IR renders the
  `**{...}` form because socket names need not be valid identifiers. Tests
  force a fresh `_build_group` rebuild (renaming existing groups) so the
  inner structure — not just reuse-by-name — is verified.
- [x] **Variable-items node emitter** (`CaptureAttribute`, `FieldToGrid`,
  `Bake`, `FieldToList`): round-trip as `items={name: field}` instead of
  emitting each item input as an invalid `field_0=` kwarg. A small
  `_ItemsNodeSpec` table names the fixed inputs and, where the node has one,
  the factory method chosen by its `data_type`/`domain`
  (`g.CaptureAttribute.point(geometry=…, items={…})`,
  `g.FieldToGrid.boolean(topology=…, items={…})`); nodes without a
  type/domain property use the plain constructor
  (`g.Bake(items={…})`, `g.FieldToList(count=…, items={…})`). Item sockets
  are identified generically as the trailing N input/output sockets
  (N = collection length); a fixed input is emitted only when linked or
  differing from a fresh node's socket default (so `FieldToList count=5`
  survives). Bails to the generic path when a fixed input it can't author
  (e.g. a linked CaptureAttribute `Selection`) is in use.

- [x] **Variable-items socket identifiers in round-trip comparison**: a
  hand-built node whose item collection was `clear()`ed and rebuilt keeps a
  higher creation-order counter (`Generation_1`) than a fresh one
  (`Generation_0`). The counter is an implementation detail — what matters
  is that codegen creates a corresponding socket — so the round-trip
  comparison (`_structure`) keys variable-items sockets on their role prefix
  + name instead of the raw identifier. This cleared the last xfail
  (`build_import_microscopy_meshes_api`); every usecase now round-trips.

- [x] **Bundled-asset round-trip coverage**: `test_roundtrip_bundled_asset`
  parametrises over every geometry node-group asset Blender ships with bpy
  (the "essentials"/dynamics/hair/principal-components libraries). The set
  that round-trips cleanly (`_ASSET_ROUNDTRIP_OK`, 54 groups after the
  backlog work below) is asserted hard for regression protection; the
  remaining ~11 that hit codegen gaps are non-strict `xfail` so
  a future fix surfaces as XPASS. This is the broadest available coverage —
  real trees not authored through nodebpy. Backlog of the gaps they exercise
  is below.

## To Do

### Polish
- [ ] Mode-dependent socket defaults: probe node currently created with
  default properties, so irrelevant kwargs (e.g. `length=` on EVALUATED
  CurveToPoints) are emitted. Probe could copy enum props first.
- [x] **Inactive group-input sockets** (`RuntimeError: Socket … is
  inactive`): a group input only used behind an internal switch polls as
  inactive until the group is evaluated — including the input being linked,
  so `tree.link`'s guard blocked the very link needed to round-trip. Group
  nodes joined `_allow_innactive_sockets`. Also fixed the guard message,
  which always named the source socket even when the *target* was inactive.
  Flipped 7 hair assets.

### Bundled-asset backlog
Failure categories blocking the xfailed `test_roundtrip_bundled_asset`
cases (counts approximate), by node/feature gap:
- [x] **Menu/enum socket defaults** (`enum "X" not found in ()`): a menu
  interface input's valid values come from the MenuSwitch linked to it, so
  its default can only be set once the body has created that node. Codegen
  now emits the menu input *without* its default and appends a deferred
  `<var>.default_value = "X"` statement after the body (new
  `EmitContext.iface_deferred` → `_TreeEmission.deferred_lines`). Removes the
  enum error from ~9 assets (Array, Curve to Tube, Scatter on Surface, hair
  generators); those now hit the vector/scalar-default gap below.
- [x] **Bundle nodes** (`CombineBundle`/`SeparateBundle`): both gained an
  `items=` builder API and a codegen emitter. `CombineBundle(items={name:
  source})` links each source into the bundle via the `__extend__` virtual
  socket (Blender infers the item type from the source) then renames the
  item; `SeparateBundle(bundle, items={name: "TYPE"})` declares each output
  by name + socket-type string and reads them via `.o[name]`. The bundle
  parts of the dynamics/hair assets now round-trip (verified by link diffs);
  those assets remain xfailed on other gaps below.
- [x] **EvaluateClosure**: gained `input_items=`/`output_items=` constructor
  args and a codegen emitter — `g.EvaluateClosure(closure, input_items={name:
  source}, output_items={name: "TYPE"})`. Input items link sources via the
  input `__extend__` socket (like CombineBundle); output items declare type
  strings (like SeparateBundle), read via `.o[name]`. The closure source is
  whatever feeds the `Closure` input (a group input, etc.). All three
  EvaluateClosure assets now round-trip the closure correctly; Displace
  Geometry is left blocked only on the multiple-Group-Input gap.
- [ ] **ClosureZone** (inline closure *definition* via `ClosureInput`/
  `ClosureOutput`): a paired zone that defines a closure's signature + body,
  needs a zone emitter like Repeat/Simulation. Only one asset uses it
  (Custom Force), which is also blocked on the menu/enum gap, so it unblocks
  nothing on its own.
- [x] **Multiple Group Input/Output nodes**: a tree may hold several Group
  Input nodes (editor convenience to shorten wires) that are functionally one
  interface; nodebpy authors a single interface so codegen collapses them to
  one node — the correct, idiomatic behaviour, like reroute collapsing. The
  round-trip comparison (`_structure`) now excludes `NodeGroupInput`/
  `NodeGroupOutput` from the node multiset (links still reference group
  sockets by name, so a genuinely missing socket is still caught). This plus
  the bundle/closure work moved **16 assets** to passing (14 → 30),
  resolving most of the old "structural mismatch" category (Box/Normal/Sphere
  Selection, Randomize Transforms, Smooth by Angle, …) and unblocking
  Collider/Displace Geometry.
- [x] **String escaping**: `_fmt` now uses `json.dumps(…, ensure_ascii=False)`
  so string defaults with newlines/tabs/control chars emit a valid literal
  (was a naive quote/backslash replace → `unterminated string literal`).
  Cleared the SyntaxError for Cloth Dynamics and Hair Dynamics (they now hit
  the menu/enum gap); Braid Hair Curves has an unrelated `FloatCurve.items`
  property bug, not a string issue.
- [x] **Vector interface `dimensions` (2D/4D)** (`should contain 3 items`/
  `length must match dimensions`): the interface vector socket's
  `default_value` RNA is a fixed 3-float array regardless of `dimensions`, so
  a 2-element default (read from a `dimensions=2` socket) couldn't be set and
  the `(0,0,0)` param default failed the length assert for `dimensions != 3`.
  `tree.inputs/outputs.vector` now defaults `default_value=None` →
  `(0.0,)*dimensions` and pads/truncates to 3 floats when assigning. Flipped
  5 assets: 3D to Screen Space, Screen to 3D Space, Project with Depth,
  Set Attachment Surface, Transform and Project.
- [x] **Operator lifting of `vector_const * scalar`** (`NodeSocketFloat
  .default_value expected a float, not tuple`): codegen lifted a VectorMath
  multiply to `(1.0, 0.0, 0.0) * r`, but `tuple * float_socket` re-creates a
  *scalar* Math node whose float input rejects the tuple. A VectorMath lift
  is now refused unless at least one operand is a linked vector socket (so
  the operator dispatches to VectorMath), falling back to the
  `g.VectorMath.*` constructor — `_lift_plan` gained the incoming source
  types (`_linked_src_types`). Flipped Combine Cylindrical and Combine
  Spherical.
- [x] **GeometryToInstance multi-input** (`__init__() got an unexpected
  keyword argument 'geometry'`): unlike JoinGeometry (whose `geometry=`
  iterable param absorbs the multi-input tuple), GeometryToInstance takes
  `*args`, so the generic `geometry=(...)` kwarg was rejected. A custom
  emitter now renders its multi-input geometry links as positional args
  (`g.GeometryToInstance(a, b, c)`, creation order). Removes the error from
  Scatter on Surface / Curve to Tube / Instance on Elements, which now reach
  the socket-method/output-accessor gap below.
- [x] **`.mix` on a non-float receiver** (`'IntegerSocket' has no attribute
  'mix'`): a symptom of the Math-lift bug above — a ShaderNodeMath with two
  integer inputs lifted to `Index / integer_math` produced an *IntegerMath*
  receiver, which lacks `.mix`. Fixed by the `_operator_dispatch_ok` Math
  guard, not by adding `.mix` to IntegerSocket (which would have masked the
  wrong-node-type lift).
- [x] **`.o.<name>` output accessor for multi-word names** (`Socket
  'flip_and_cyclic' not found on output accessor`): the accessor normalised
  identifiers but not names, and `denormalize_name("flip_and_cyclic")`
  title-cases the connector → "Flip **And** Cyclic" ≠ the real name "Flip
  **and** Cyclic". `SocketAccessor._index` now also matches the key against
  *normalised socket names*, so `.o.flip_and_cyclic` resolves "Flip and
  Cyclic". Flipped 5 hair assets (Attachment Info, Curl/Duplicate/Roll/
  Rotate Hair Curves).
- [x] **Lifted operator returns a node** (`'BooleanMath' has no attribute
  'switch'`): a Python operator dispatches on its left operand, and nodebpy's
  operators only return a socket when the left operand is already one — so
  `g.Compare…() & g.Compare…()` (two nodes) returned a node. `_lift_expr` now
  forces only the leading operand to a socket (socket_expr; a no-op when
  already a socket), keeping the lifted result a socket. Flipped Shrinkwrap.
- [x] **Boolean `~`/`^` returned nodes**: the boolean socket mixin overrode
  `&`/`|` to return sockets but missed `__invert__`/`__xor__`; added them so
  all boolean ops return a `BooleanSocket`.
- [x] **CaptureAttribute matrix/color/rotation item types**: `_type_map`
  used data_type spellings (`FLOAT4X4`…) where `capture_items.new()` wants
  socket-type spellings (`MATRIX`…); now `{'VALUE': 'FLOAT'}`.
- [x] **Bare reference resolves to the wrong output**: a bare node reference
  links its output by best type-match, so a `MenuSwitch` (int `Output` +
  per-item boolean `is_selected`) feeding a boolean `Switch` linked the wrong
  output. `_output_expr` now pins `.o.<name>` only when the linked output's
  type differs from the consumer's *and* a better-typed output exists (no
  churn on same-type cases). Flipped Generate / Interpolate Hair Curves.

- [x] **Duplicate group socket names** (Array): a group with two interface
  inputs both named "Randomize Scale" feeding a nested group with two "Scale"
  inputs — `GroupCall(**{name: value})` can't carry two same-name keys.
  `_emit_group_node` now keys by socket identifier when the name is not unique
  (`_establish_links` resolves identifiers too).
- [x] **Math vs VectorMath with a color operand** (Scatter on Surface):
  `color - x` dispatches to VectorMath, but the original is a scalar Math.
  `_operator_dispatch_ok` now refuses the Math lift when its dispatching (first
  linked) operand is an RGBA/VECTOR source.

- [x] **Float default on an INT socket** (Create Guide Index Map): not a
  codegen bug but a library one — `g.AccumulateField(data_type="INT")` applies
  its constructor's `value=1.0` float default to the now-integer Value socket,
  which bpy rejects. `_set_input_default_value` already broadcasts scalars into
  VECTOR sockets; it now also coerces a float to `int` for INT sockets (mirrors
  that special case). Flipped Create Guide Index Map (54 → 55 passing).

- [x] **CaptureAttribute built-in `Selection`** (Attach Hair Curves to
  Surface): Blender gave geometry CaptureAttribute a fixed `Selection`
  input/output (no item needed); the nodebpy class signature gained the
  matching `selection=` param. Codegen's `_ItemsNodeSpec` named only
  `Geometry` as a fixed input, so a *linked* Selection tripped the
  bail-to-generic guard and the constructor then emitted an item input as a
  bogus `value=` kwarg. Added `("Selection", "selection")` to the spec's
  `fixed` tuple — Selection is now authored (linked → upstream; unlinked True
  default dropped). Flipped Attach Hair Curves to Surface (55 → 56 passing).
- [x] **FloatCurve `items` mis-read as a property** (Braid): `_non_default_props`
  captured every keyword-only constructor param as a node setting via
  `getattr(node, name)`. FloatCurve's `items` is a nodebpy-only convenience
  param (curve points), not a bpy property, so `getattr` returned the unrelated
  `bpy_struct.items` dict method and codegen emitted `items=<built-in method…>`
  (SyntaxError). `_non_default_props` now requires keyword-only params to be
  real RNA properties, exactly as it already did for positional-or-keyword
  params. Flipped Braid Hair Curves (56 → 57 passing). Caveat: the FloatCurve's
  curve shape is not yet re-emitted (structural round-trip doesn't compare
  points); a dedicated `items=[(x, y, handle), …]` emitter is a future polish.
- [x] **VectorMath SCALE lifted to `*` with a non-scalar operand** (Trim Hair
  Curves): a SCALE node lifted to `vec * x`, but `vec * x` only re-creates a
  SCALE node when `x` is a scalar (VALUE/INT) or an unlinked float literal — a
  linked BOOLEAN/VECTOR `Scale` operand dispatches to MULTIPLY on rebuild (see
  `_dispatch_vector_math`), swapping both the op and the target socket.
  `_operator_dispatch_ok` now refuses the SCALE lift in that case, falling back
  to `g.VectorMath.scale()`. Flipped Trim Hair Curves (57 → 58 passing).
- [x] **Item name colliding with a built-in socket** (Curve to Tube): a
  CaptureAttribute item named "Selection" collides with the new built-in
  `Selection` socket, so `_item_socket` (and the link target in
  `_establish_links`) resolved by name to the wrong socket. `_item_socket` now
  falls back to positional resolution (item sockets are the trailing N) on a
  name clash, and `_add_inputs` keys returned sockets by *identifier* so links
  are established unambiguously. Flipped Curve to Tube (58 → 59 passing).
- [x] **Item identifier vs name collision** (Instance on Elements): a
  CaptureAttribute with items named "Normal" *and* "Value" — the "Normal"
  item's socket identifier is "Value" (capture_items number sockets from
  "Value"), colliding with the "Value" item's *name*. `_add_inputs` keys links
  by identifier, but `_find_socket_from_name` resolved name-first, so the key
  "Value" hijacked to the socket *named* "Value" and the "Normal" item lost its
  link — one of two duplicate Normal captures silently dropped (a multiplicity
  bug the round-trip's old `set()`-based debug masked). `_find_socket_from_name`
  now returns an exact identifier match before the name-normalising passes,
  aligning with SocketAccessor's identifier-first strategy. Flipped Instance on
  Elements (59 → 60 passing).

- [x] **ClosureZone** inline closure definition (Custom Force): a paired
  `ClosureInput`/`ClosureOutput` zone defining a closure's signature + body.
  Items live on the output node (`input_items` drive the input node's outputs,
  `output_items` drive the output node's inputs), so the plain-constructor path
  (`g.ClosureInput()` + `g.ClosureOutput(item_0=…)`) can't work. Added a
  builder API — `cz = g.ClosureZone()`, `cz.input_item(name, type)` (returns
  the socket read in the body), `cz.output_item(name, type)` (returns a `>>`
  target), and `cz.closure` (the resulting closure) — plus a zone emitter
  modelled on Repeat/Simulation: `_emit_closure_input` declares the zone and
  per-item lines and dissolves the input node into input-item reads; the output
  node reuses `_emit_zone_output` (links → `expr >> target`, dissolves into
  `cz.closure`). The synthetic input→paired-output ordering edge already covers
  closures (`paired_output` is generic). Flipped Custom Force (60 → 61
  passing).

- [x] **Hair Dynamics & Cloth Dynamics** (were filed as "segfaults" — actually
  a chain of three exceptions, not crashes, surfaced by tracing the exec in an
  isolated subprocess):
  1. *Duplicate-named group inputs keyed by identifier* — see the
     name-based fix above; removed the MENU/MATRIX mislink.
  2. *Multi-input socket fed an iterable* (`JoinBundle(bundle=(…))`):
     auto-generated multi-input nodes take a single socket param, so the tuple
     hit the default-value path (`assert hasattr(input, "default_value")`).
     `_apply_input` now links each source into an `is_multi_input` socket
     (reversed, as JoinGeometry does); a vector/colour default tuple is not
     multi-input so it falls through unchanged.
  3. *Output name that isn't a valid identifier* (`.o.physics_(experimental)`
     for a socket named "Physics (Experimental)"): added a `Subscript` IR;
     `_output_expr` emits `value.o["Physics (Experimental)"]` when the
     normalised name fails `str.isidentifier()`.
  All 63 bundled geometry assets now round-trip — **zero xfails**.

### To do
- [ ] Extend coverage to the shader and compositor essentials libraries
  (`shading_nodes_essentials.blend`, `compositing_nodes_essentials.blend`).
