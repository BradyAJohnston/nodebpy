# Vendored: node-arrange

Sugiyama-based node layout, vendored from
[Leonardo-Pike-Excell/node-arrange](https://github.com/Leonardo-Pike-Excell/node-arrange)
(GPL-2.0-or-later).

- **Base:** upstream commit `05d7aef` (2026-02-19, "refactor: remove dead code")
- **Last sync:** upstream commit `8ca5e29` (2026-07-01, "refactor: cleanup") — synced 2026-09-11

## What is not vendored

The Blender-addon shell: `__init__.py` (registration), `operators.py`,
`properties.py`, `ui.py`, `keymaps.py`. Their tunables are mirrored by the
`Settings` dataclass in `config.py` instead of a `PropertyGroup`.

## Local divergences from upstream

Keep these in mind when porting upstream commits; a straight file copy will
break headless operation.

- `utils.get_ntree()` resolves the tree from `TreeBuilder._tree_contexts`
  instead of `bpy.context` (no UI context exists under the `bpy` module).
- Headless adaptations — Blender never draws the tree, so UI-derived data is
  unavailable:
  - `graph.get_socket_y()` is stubbed (socket runtime locations are only
    written during drawing). Socket-precise Y alignment is effectively
    disabled; `utils.get_bottom()` estimates node heights via
    `nodebpy.builder.arrange.calculate_node_dimensions()`.
  - `sugiyama.optimize_sizes()` skips `bpy.ops.wm.redraw_timer` and falls
    back to a per-character width estimate when `blf` can't measure text.
- `structs.py` uses explicit `_fields_` lists (upstream builds them from
  annotations, formerly via `eval`) and additionally binds `bNode` /
  `bNodeRuntime` / `rctf`, which upstream does not have.
- Typing/lint fixes throughout to satisfy `ty` and `ruff` under this repo's
  config.

## Upstream commits ported since base

- `ec36f75` / `3fc80aa` / `5f9e8a7` — bNodeSocket(Runtime) bindings updated
  for Blender 5.0/5.1/5.2 field changes; class renamed to `bNodeSocketRuntime`.
- `0c8586b` — remove `eval` (already covered by the local explicit-fields
  rewrite).
- `5ac05cb` — `optimize_sizes` option: fit collapsed-node widths to their
  display name (adapted for headless; default off, see `Settings`).
- `34ce6c4` / `8ca5e29` — `minimum_feedback_arc_set`: reconstruct cycle edges
  explicitly instead of `G.subgraph(cycle).edges`, which also picked up chord
  and parallel edges.

## How to sync with upstream

```sh
git clone https://github.com/Leonardo-Pike-Excell/node-arrange /tmp/node-arrange
cd /tmp/node-arrange
git log --stat <last-synced-commit>..HEAD -- source/arrange source/config.py source/utils.py
```

Port each relevant commit as a patch onto the vendored files (paths map
`source/` → this directory), respecting the divergences above. Then update
the "Last sync" line and the list of ported commits, and run
`make format && make test`.
