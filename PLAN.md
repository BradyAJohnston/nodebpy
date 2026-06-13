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
  that round-trips cleanly (`_ASSET_ROUNDTRIP_OK`, 30 groups after the
  bundle/closure/group-input work) is asserted hard for regression
  protection; the rest (~33) that hit codegen gaps are non-strict `xfail` so
  a future fix surfaces as XPASS. This is the broadest available coverage —
  real trees not authored through nodebpy. Backlog of the gaps they exercise
  is below.

## To Do

### Polish
- [ ] Mode-dependent socket defaults: probe node currently created with
  default properties, so irrelevant kwargs (e.g. `length=` on EVALUATED
  CurveToPoints) are emitted. Probe could copy enum props first. Also the
  cause of several bundled-asset `RuntimeError: Socket … is inactive`
  failures (a link targets a socket inactive under the rebuilt node's mode).

### Bundled-asset backlog
Failure categories blocking the xfailed `test_roundtrip_bundled_asset`
cases (counts approximate), by node/feature gap:
- [ ] **Menu/enum socket defaults** (`enum "X" not found in ()`, ~9): a menu
  input socket default is set before the node's enum items exist, so the
  value isn't a valid choice yet. Needs ordering or deferral of menu default
  assignment (e.g. Array, Curve to Tube, Scatter on Surface, hair generators).
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
- [ ] **Vector vs scalar defaults** (`expected a float`/`should contain 3`/
  `length must match dimensions`): a vector socket default emitted as a
  scalar (or vice versa) — `CombineXYZ`-style sockets, `3D to Screen Space`.
- [ ] **Socket-method / output-accessor faithfulness**
  (`'BooleanMath' object has no attribute 'switch'`, `Socket 'X' not found
  on output accessor`): a socket method or `.o.<name>` is emitted that the
  rebuilt socket doesn't expose.
- [x] **Structural mismatches**: the original ~13 were almost all the
  multiple-Group-Input case above and are now resolved; re-diff any new ones
  per-case.
- [ ] Extend coverage to the shader and compositor essentials libraries
  (`shading_nodes_essentials.blend`, `compositing_nodes_essentials.blend`).
