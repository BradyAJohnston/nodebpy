# Items API Unification Plan

Design notes for cleaning up zones, capture, and all variable-items nodes —
**do this before building codegen for zones** (see PLAN.md). The goal is one
canonical, code-generatable authoring form, one shared mixin for item
machinery, and handle objects that name socket *roles* instead of plumbing.

## Why now

Codegen (Stage 8) needs a canonical form to emit for zones. The graph state
is fully readable, but several things cannot be faithfully *re-authored*
through the current API (no explicit item names, no unlinked item
declaration). Fixing the API first means codegen targets the good form
instead of baking in today's quirks.

## Current state inventory

### Item-bearing nodes and their machinery

| Node | Mixin? | bpy collection | `_add_socket` style |
|---|---|---|---|
| `Bake` (manual.py ~1053) | DynamicInputsMixin | `bake_items` | `.new(socket_type, name)` |
| `FormatString` (~1347) | DynamicInputsMixin | `format_items` | `.new(socket_type, name)` |
| `CaptureAttribute` (~2114) | DynamicInputsMixin | `capture_items` | `.new(socket_type, name)` |
| `FieldToList` (~2222) | DynamicInputsMixin | `list_items` | **`_add_socket` is a `pass` stub**; real work in a parallel `_new_item` + per-dtype methods |
| `FieldToGrid` (~2355) | DynamicInputsMixin | grid items | `.new(...)` |
| `SimulationZone` in/out (zone.py) | via `BaseZone` | `state_items` (shared, 4 sockets/item) | `items.new(type, name)` via abstract `items` property |
| `RepeatZone` in/out | via `BaseZone` | `repeat_items` (shared) | same |
| `ForEachGeometryElementZone` | via `BaseZone` | **three** collections: `input_items`, `main_items`, `generation_items` | `capture_generated` temporarily monkeypatches `_socket_data_types` + `_add_socket` (zone.py:436–443) |
| `IndexSwitch` (~1747) | **no mixin** | `index_switch_items` | `.new()` (unnamed), own `_create_socket`/`_link_args` |
| `MenuSwitch` (~1982) | **no mixin** | `enum_items` | `.new(name)`, own `_create_socket`/`_link_args`, plus `is_selected` |
| `ClosureZone` / `EvaluateClosure` | no | `input_items`/`output_items` | bespoke `link()` + `sync_signature` |
| `JoinGeometry` / `StringJoin` | no | multi-input socket (not items) | n/a — already handled by codegen tuples |

### DynamicInputsMixin contract today (builder/node.py:208)

`_socket_data_types` tuple + `_type_map` dict + abstract `_add_socket(name,
type)` + `_add_inputs(*args, **kwargs)` (auto-names positional args after
their source socket) + a `_find_best_socket_pair` override that makes `>>`
*implicitly create a new item*.

### Verb/signature drift

- `CaptureAttribute.capture(value) -> SocketLinker`
- `BaseZone.capture(value, domain="POINT")` — **`domain` is dead, never used**
  (zone.py:59–65)
- `ForEachOutput.capture_generated(value)` — **lacks** `domain`, the one place
  it matters (generation items have per-item domain; the microscopy usecase
  pokes `generation_items[0].domain` via raw bpy)
- `FieldToList.capture(fields: dict) -> list[SocketLinker]` — different
  signature entirely
- Constructor kwarg names: `items=` (CaptureAttribute, FormatString),
  `fields=` (FieldToList), `*args/**kwargs` (Bake), positional dict
  (MenuSwitch), `items=iterable` (IndexSwitch)
- Three implementations of "return the just-added socket":
  `outputs[-2]` (BaseZone), index-of-`__extend__` (ForEachInput),
  `_latest(suffix)` (ForEachOutput)

### Zone wrapper inconsistencies

- `SimulationZone`/`ForEachGeometryElementZone` unpack via `__getitem__`
  (2-tuple); `RepeatZone` instead has `__iter__`/`__next__` yielding a
  3-tuple inside a faux one-pass `for` loop — `input, output = repeat_zone`
  does not work.
- All zone wrappers use mutable default args (`items: dict = {}`).
- Zone wrappers are plain objects (not BaseNode) — fine, keep that.

## Target design

### 1. One `ItemsMixin` replacing all the bespoke machinery

A single mixin parameterised by declarative class attributes instead of
per-class method overrides:

```python
class ItemsMixin:
    _items_collection: str          # "capture_items", "bake_items", "repeat_items", …
    _socket_data_types: tuple[str, ...]
    _type_map: dict[str, str] = {}

    @property
    def _items_node(self) -> bpy.types.Node:  # override for zone inputs → paired_output
        return self.node

    def _items(self):  # the bpy collection
        return getattr(self._items_node, self._items_collection)

    def _new_item(self, name, type) -> Item: ...      # normalises .new() signatures
    def _item_socket(self, item, *, output: bool): ...  # one "find the socket" impl
    def add_items(self, items: Mapping[str, InputLinkable | None]) -> dict[str, Item]
    def capture(self, value, *, name: str | None = None) -> Item | Socket
```

- `.new()` signature differences (`(type, name)` vs `()` vs `(name)`) are
  normalised inside `_new_item` via a small adapter, not subclass overrides.
- ForEach's dual collections become **two mixin instances' worth of state on
  one class** (e.g. a second descriptor `_generation = ItemCollection(
  "generation_items", ...)`) — kills the monkeypatch.
- The one "socket for item" implementation replaces `outputs[-2]` /
  `__extend__`-index / `_latest`.
- Keep the `>>`-implicit-add behaviour (it's used and liked), implemented
  once in the mixin.
- `IndexSwitch` (unnamed positional items) and `MenuSwitch` join the mixin
  with `_new_item` adapters; their positional/iterable constructor sugar
  stays.

### 2. Item handles (the core new concept)

`add_items`/`capture`/`zone.item()` return handle objects that name roles,
not plumbing:

```python
class Item:            # single-node items (CaptureAttribute, Bake, FormatString, …)
    name, socket_type
    input: Socket      # the node's input socket for this item
    output: Socket     # the node's output socket for this item

class ZoneItem(Item):  # repeat/simulation state items (4 sockets per item)
    initial: Socket    # input-node input  — set the starting value
    current: Socket    # input-node output — read inside the body
    next: Socket       # output-node input — write the per-iteration result
    result: Socket     # output-node output — read after the zone
```

Canonical zone authoring becomes:

```python
zone = g.RepeatZone(100)
value = zone.item("value", initial=1.0)
(value.current + 1 / factorial) >> value.next
value.result >> g.ValueToString.float(decimals=10) >> ...
```

Existing spellings (`zone.input.o.value`, constructor `items=` dict,
`capture`) remain as sugar over handles. ForEach gets
`zone.item(...)` (input items), `zone.main_item(...)`, and
`zone.generated_item(name, value, domain=...)`.

### 3. Unified verbs and signatures

- `capture(value, *, name: str | None = None)` everywhere; auto-name from the
  source socket only when `name` is omitted. **Explicit names are the single
  most important change for codegen round-trip.**
- `capture_generated(value, *, name=None, domain="POINT")` — gains the
  `domain` it needs; `BaseZone.capture` loses the dead one.
- Constructor kwarg is `items=` on every items node (keep `fields=`
  etc. as deprecated aliases initially).
- `items=` dict values may be `None` → declare the item *unlinked* (needed
  to round-trip items whose initial value is the socket default). Type then
  comes from… an explicit type when value is None: allow
  `items={"value": Float}` socket-class or `"FLOAT"` string. (Pick one;
  string matches `_socket_data_types`.)
- All zone wrappers: `__getitem__` 0/1 + 2-tuple `__iter__`; keep
  `.input`/`.output`/`.iteration`/`.delta_time`/`.index` properties.
  Deprecate (or document as sugar) the 3-tuple `for i, input, output in
  RepeatZone(...)` faux-loop.
- Replace mutable default args (`items={}` → `items=None`).

### 4. Codegen follow-up unlocked by this (Stage 8)

- Canonical zone form to emit: `zone = g.RepeatZone(n, items={...})` /
  handle form; body refs `zone.input.o.x` or `item.current`; result links as
  `expr >> item.next` statements at the output node's topological position.
- Emission needs: paired-node recognition (`node.paired_output`); zone
  declaration emitted at input-node position; output-node incoming links as
  deferred `>>` statements; `var_map` entries for both bpy nodes →
  `Attr(zone_ref, "input"/"output")`; a `DictExpr` IR node (also unlocks
  `FormatString.format({...})`, `MenuSwitch`, `IndexSwitch`, Bake,
  CaptureAttribute items).
- `CaptureAttribute` needs no API change for codegen — `g.CaptureAttribute
  .point(geo, items={"Position": g.Position()})` is already canonical.

## Suggested implementation order

1. **`ItemsMixin`** in builder/ — port `CaptureAttribute`, `Bake`,
   `FormatString` first (simple, one collection each). Verify: existing
   tests pass unchanged (the public constructors don't change). ✅ DONE
2. Port `FieldToList`/`FieldToGrid` (removes the `_add_socket` stub) and
   `IndexSwitch`/`MenuSwitch` (adapters for their `.new()` signatures).
   ✅ DONE
3. Port zones onto the mixin; fix `capture` signatures (`name=`, domain
   move); replace the ForEach monkeypatch with a second collection
   descriptor; unify wrapper unpacking; mutable-default cleanup. ✅ DONE
   Implementation notes (deviations from the sketch above):
   - Zone item sockets are found by **identifier prefix + collection
     index** (`Item_`/`Input_`/`Main_`/`Generation_` via
     `_socket_for_item` in zone.py) — names are not unique across a zone
     node's fixed sockets and item collections (e.g. a main item and a
     generation item can both be called "Position").
   - The ForEach second collection is handled by an explicit
     `capture_generated` built on `ItemsMixin._resolve_capture` rather
     than an `ItemCollection` descriptor — only one node needed it.
   - `ItemsMixin.add_items(items) -> dict[str, Socket]` is the dict-based
     verb (replaces the `FieldToList`/`FieldToGrid` dict `capture`); step
     4 upgrades its return value to `Item` handles.
   - Constructor kwarg is now `items=` everywhere (incl. `Bake`);
     `FieldToList(fields=...)` kept as a `DeprecationWarning` alias.
4. **Item / ZoneItem handles** + `zone.item()` and `items={name: None/type}`
   declaration support. ✅ DONE
   Implementation notes:
   - `Item` (builder/items.py) stores the item's **collection index**, not
     the bpy item — bpy collection item references are invalidated when
     the collection grows (segfault). `Item.socket_type` falls back to
     `data_type` (capture_items, grid_items spelling).
   - `ItemsMixin.add_item(name, value=None, *, type=)` is the single-item
     verb; `add_items` now returns `dict[str, Item]`.
   - Unlinked declaration uses **socket-type strings as dict values**
     (`items={"geo": "GEOMETRY"}`), validated against
     `_socket_data_types`/`_type_map` via `_declared_item_type` — a hook
     on `DynamicInputsMixin._add_inputs`, so every `items=` constructor
     supports it. Bare `None` values are rejected (no type to infer).
   - `zone.item(name, initial=...)` lives on `_StateZone`
     (Simulation/Repeat wrappers) and returns `ZoneItem`
     (initial/current/next/result). `initial` accepts linkables, plain
     defaults (python-type inference), or type strings; the constructor
     `items=` dict is now sugar over `zone.item()`.
   - ForEach wrapper: `zone.item()` / `zone.main_item()` /
     `zone.generated_item(name, value, type=, domain=)`; generation
     handles resolve sockets with the `Generation_` prefix
     (`_GenerationItem`); `capture_generated` delegates to
     `add_generated_item`.
5. Then Stage 8 codegen: zone emitters targeting the handle/canonical form,
   plus `DictExpr`. ✅ DONE — see PLAN.md Stage 8 for the emitter design
   and known gaps. Along the way: `ItemsMixin.add_item` /
   `add_generated_item` accept plain default values,
   `ForEachGeometryElementZone.generation` exposes the default generation
   item handle, and `RepeatZone` pairs before linking `Iterations`
   (sockets on unpaired zone nodes are inactive).

Each step: `uv run pytest` green before moving on; the structural round-trip
harness in tests/test_codegen.py is the safety net for codegen stages.
