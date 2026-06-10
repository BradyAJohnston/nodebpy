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

## To Do

### High value
- [ ] **Classmethod reverse table**: emit `g.Math.square_root(x)` instead of
  `g.Math(value=x, operation="SQRT")`. `generate.py` already generates the
  classmethod shortcuts — have it emit the reverse mapping
  (bl_idname + props → constructor path) at the same time, single source of
  truth. Same for nested factories (`g.Compare.float.less_than`,
  `g.StoreNamedAttribute.point.integer`, `g.SetShadeSmooth.face`).
- [ ] **Zone emitters**: Repeat/Simulation/ForEach paired nodes currently
  produce broken constructor pairs. Needs `register_emitter` implementations
  emitting `g.RepeatZone(...)`, `zone.input.o.x`, `zone.output.i.x` patterns.
- [ ] **Socket-method table**: `MapRange` → `.map_range()`, `EvaluateAtIndex`
  → `.point.at()`, `AccumulateField` → `.point.trailing()`, `FormatString` →
  `.format()`, `Switch` → `.switch.float()`, SeparateXYZ → `vec.x`, plus
  future `.curl()` / `.divergence()` / `.laplacian()` when those exist.
- [ ] **Compare lifting**: `a < b` instead of `g.Compare(...)` when props
  match what the operator overload produces (mode ELEMENT, default epsilon).

### Polish
- [ ] Line-length handling: deep graphs now collapse into long single
  statements. Either a max-inline-width budget that falls back to a variable,
  or document running output through ruff/black.
- [ ] Interface fidelity: `subtype`, `min_value`/`max_value`, `description`,
  `hide_value`, `default_input`, `structure_type`, panels.
- [ ] Float32 noise in literals (`0.10000000149011612` → `0.1`): shortest
  repr that round-trips through float32.
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
