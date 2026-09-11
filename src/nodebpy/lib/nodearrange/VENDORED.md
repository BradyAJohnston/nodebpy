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

- `utils.get_ntree()` resolves the tree from `config.ntree` (set by
  `sugiyama_layout()`) instead of `bpy.context` (no UI context exists under
  the `bpy` module). Settings are applied per-call by
  `nodebpy.builder.layout.arrange()` swapping `config.SETTINGS` /
  `config.MARGIN`.
- Headless adaptations — under the headless `bpy` module Blender never draws
  the tree, so UI-derived geometry (`node.dimensions`, socket runtime
  locations) stays zeroed:
  - `utils.dimensions()` and `graph.get_socket_y()` use the drawn values
    when present and otherwise fall back to estimates from
    `nodebpy.builder.layout` (`calculate_node_dimensions()` /
    `calculate_socket_offset_y()`).
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

Run `make vendor-check` from the repo root to list upstream commits not yet
ported, or manually:

```sh
git clone https://github.com/Leonardo-Pike-Excell/node-arrange /tmp/node-arrange
cd /tmp/node-arrange
git log --stat <last-synced-commit>..HEAD -- source/arrange source/config.py source/utils.py
```

Port each relevant commit as a patch onto the vendored files (paths map
`source/` → this directory), respecting the divergences above. Then update
the "Last sync" line and the list of ported commits, and run
`make format && make test`.
