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

## To Do

### High value

### Polish
- [ ] Line-length handling: deep graphs now collapse into long single
  statements. Either a max-inline-width budget that falls back to a variable,
  or document running output through ruff/black.
- [ ] Interface fidelity: `subtype`, `min_value`/`max_value`, `description`,
  `hide_value`, `default_input`, `structure_type`, panels.
- [ ] Mode-dependent socket defaults: probe node currently created with
  default properties, so irrelevant kwargs (e.g. `length=` on EVALUATED
  CurveToPoints) are emitted. Probe could copy enum props first.
- [ ] Frames: re-emit `with g.Frame("..."):` blocks from node parenting.
- [ ] Tree type detection: shader/compositor trees should emit
  `TreeBuilder.shader(...)` / matching constructor, not the geometry default.
- [ ] Wire codegen into `TreeBuilder` UX (e.g. `tree.to_python()` method,
  `_repr_` integration, clipboard/CLI entry point).

### Stretch
- [ ] Run `to_python` round-trip across every tree built in
  `tests/test_usecases.py` as a parametrised test.
- [ ] Round-trip node groups recursively (emit `CustomGeometryGroup`
  subclasses for nested groups).
