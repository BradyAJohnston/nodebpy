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

- **No networkx.** Upstream builds its graphs on `networkx`. Here they are
  the structs in `arrange/tree.py`, shaped after Blender's own so the layout
  can later be ported to C++: `Tree` (`bNodeTree`) owns the nodes and the
  `Link`s (`bNodeLink`: `fromnode` / `fromsock` / `tonode` / `tosock`) between
  them, and `DiGraph` holds auxiliary relations (the frame hierarchy,
  ordering constraints). The same file has the few graph algorithms the
  layout needs (topological order, components, reachability, cycle search).
  Everything iterates in insertion order exactly as the networkx graphs did,
  so the port produces identical layouts. Upstream patches need translating:

  | networkx                               | here                                   |
  | -------------------------------------- | -------------------------------------- |
  | `G.add_edge(u, v, from_socket=p, to_socket=q)` | `G.add_link(u, v, p, q)`       |
  | `(u, v, k)` edge tuples, `G.edges[e]`  | `Link` objects (`link.ident` is the tuple, `G.link(u, v, k)` looks one up) |
  | `d[FROM_SOCKET]` / `d[TO_SOCKET]`      | `link.fromsock` / `link.tosock`        |
  | `G.edges`, `G.in_edges(v)`, `G.out_edges(v)` | `G.all_links()`, `G.in_links(v)`, `G.out_links(v)` |
  | `G.pred[v]`, `G[v]` / `G.succ[v]`      | `G.predecessors(v)`, `G.successors(v)` |
  | `G[u][v]`                              | `G.links_between(u, v)`                |
  | `G.out_degree[v]`                      | `G.out_degree(v)`                      |
  | `G.reverse(copy=False)`                | `G.reversed()`                         |
  | `G.graph["columns"]`                   | `G.columns`                            |
  | `T[c]` (cluster tree)                  | `T.successors(c)`                      |
  | `nx.descendants`, `nx.topological_sort`, … | the functions of the same name in `tree.py` |

- **The layout is pure.** Upstream reads and edits the Blender tree
  throughout the pipeline. Here that is three stages (see `__init__.py`):
  `extract.py` copies the tree into plain data (`dna.py`: `bNodeTree`,
  `bNode`, `bNodeSocket`, `bNodeLink`, named after the Blender structs),
  measuring node sizes and socket positions; `arrange/` computes the layout
  from that data alone and returns an ordered list of edits
  (`arrange/edits.py`); `apply.py` carries them out. Nothing under
  `arrange/`, nor `dna.py` or `config.py`, may import `bpy` or `mathutils`
  (a test enforces it). Upstream patches need translating:

  | upstream                                  | here                                  |
  | ----------------------------------------- | ------------------------------------- |
  | `v.node` is a `bpy.types.Node`            | a `dna.bNode` (`idname`, `is_collapsed`, `is_reroute()`, `top`, …) |
  | `socket.bpy`                              | `socket.dna`, a `dna.bNodeSocket`     |
  | `ntree.nodes.remove(node)`                | `state.edits.append(RemoveNode(node))` |
  | `ntree.nodes.new("NodeReroute")`          | `dna.new_reroute(parent)` + `AddReroute` |
  | `links.new(a, b)` / `links.remove(link)`  | `AddLink(a, b)` / `RemoveLink(a, b)`  |
  | setting `node.location` / `node.parent`   | `MoveNode(node, top_left, parent)`    |
  | `abs_loc`, `dimensions`, `get_top`, `get_socket_y` | fields of the `dna` structs (those helpers now live in `utils.py` / `extract.py`, for the Blender side only) |
  | `mathutils.Vector`, `intersect_line_line_2d` | `common.Vec2`, `common.segments_intersect` |

  One consequence: node sizes and socket positions are all read once, before
  the layout. Upstream reads socket positions lazily, part-way through, after
  it has already removed reroutes and links from the tree — which matters
  for collapsed nodes, whose sockets are spread according to how many are
  linked. Layouts are identical to before except in that case (a collapsed
  node next to a reroute the layout replaces).
- **The layout is a pipeline.** Upstream's `sugiyama_layout` is one fixed
  function calling each pass in turn. Here `arrange/pipeline.py` makes it a
  list of named `Step`s (`sugiyama.default_pipeline()`), run by a
  `Pipeline` that can be edited (replace / insert / remove a step) and
  observed (a callback after each step). The four deciding passes are
  *phases* with registered strategies, selected in `Settings`: `rank`
  (`ranking`), `order` (`ordering`), `place` (`placement`), `route`
  (`routing`). An upstream change to the order of passes goes into
  `default_pipeline()`; a new upstream pass becomes a `Step` there.
  `ranking.compute_ranks()` takes the solver as an argument, and
  `"longest_path"` is a second ranking strategy (nodebpy-only).
  Steps state how they depend on each other: each `Step` names the
  `pipeline.Fact`s it `requires`, `provides` and `removes` (ranked, proper,
  columns, ordered, borders, y, x, …). `Pipeline.check()` refuses a list of
  steps that do not fit together before anything runs, and
  `sugiyama_layout(..., verify=True)` checks every fact against the graph
  after every step (`pipeline.CHECKS`), so a step or strategy that breaks an
  invariant is named at once. A phase looks up its strategy when it runs,
  from the settings of that run. In a C++ port the facts are the pre- and
  postconditions of the phase functions and the checks are debug asserts.
  `sugiyama.add_columns()` also starts every column with each frame's nodes
  together (`graph.keep_frames_together()`): upstream's ordering stops as
  soon as nothing crosses and could leave a column it never visited with a
  frame split in two.
- **No module globals.** Upstream keeps its working state (`selected`,
  `linked_sockets`, `multi_input_sort_ids`, `SETTINGS`, `MARGIN`) as module
  globals in `config.py`, reset manually per operator invocation. Here that
  is a per-run `config.LayoutState` dataclass, created by
  `sugiyama_layout(tree, settings, margin)` and threaded explicitly:
  `ClusterGraph` carries it as `.state` for the pipeline, and pure-graph
  helpers take it as a parameter. It also collects the edits.
- Headless adaptations — under the headless `bpy` module Blender never draws
  the tree, so UI-derived geometry (`node.dimensions`, socket runtime
  locations) stays zeroed:
  - `utils.dimensions()` and `extract.get_socket_y()` use the drawn values
    when present and otherwise fall back to estimates from
    `nodebpy.builder.layout` (`calculate_node_dimensions()` /
    `calculate_socket_offset_y()`).
  - `extract.optimize_sizes()` skips `bpy.ops.wm.redraw_timer` and falls
    back to a per-character width estimate when `blf` can't measure text.
- **Selection is ignored.** Upstream arranges the user's selection
  (`config.selected`, and per-link `node.select` gates in
  `get_multidigraph()`, here `get_tree()`, and `realize.is_safe_to_remove()`). Here
  `arrange_node_tree` always lays out the whole tree — a library-loaded tree
  has no selection at all, which would silently arrange nothing — so the
  working set is every node of the tree and the select gates are membership /
  always-true checks. Upstream patches touching `.select` need the same
  translation.
- **Layout readability additions** (nodebpy-only, each behind a `Settings`
  flag mirrored on `SugiyamaOptions`):
  - `ranking.add_frame_sequence_edges()` (`sequential_frames`): ranks
    frames as stages of the flow by constraining every node of a frame to
    come after every node of the frame (or intermediate node) feeding it, so
    successive frames line up left to right instead of stacking into a
    staircase.
  - `balancing.balance_column_heights()` (`balance_heights`,
    `balance_aspect`): after ranking, promotes nodes of the tallest columns
    together with their upstream into emptier columns while the drawing
    gets closer to a screen-shaped box.
  - `priority.socket_priorities()` / `graph.link_priority()`
    (`link_priority`, `trunk_min_priority`): links carrying the tree's main
    data (geometry, shader, bundle, closure) get a priority, and
    `y_coords.horizontal_alignment()` aligns a node with a neighbour across
    such a link before falling back to upstream's median neighbour — so the
    trunk is a straight row. When several nodes want the same neighbour
    across such links the middle one gets it, which makes a fork that
    merges again symmetric. `weighted_ranking` also feeds the priorities to
    the network simplex as link weights. With `link_priority="none"` the
    alignment is upstream's.
  - `balancing` skips columns of at most `balance_min_column` nodes, so a
    few parallel branches are not staggered over two columns.
  - `sugiyama.pin_interface_nodes()` (`pin_group_output`,
    `pin_group_input`): a pipeline step after ranking that moves Group
    Output / Group Input nodes outside frames to the last / first column.
  - `y_coords.vertical_gap()` (`reroute_margin_y_fac`): consecutive
    reroutes / dummy nodes in a column pack at a fraction of the margin.
  - `sugiyama.precompute_links()` keeps `is_hidden` links (links into a
    collapsed panel's sockets), which still order the nodes; and
    `x_coords.assign_x_coords()` skips a column left empty by dissolved
    dummies.
- **Deterministic iteration order.** Upstream hashes `graph.Node` and
  `graph.Cluster` by `id()` and keeps `linked_sockets` values as sets of bpy
  sockets (which hash by pointer), so set iteration followed memory addresses
  and the same tree could lay out differently between runs. Here they hash by
  a creation serial (`graph._serials`, reset per run in `sugiyama_layout`),
  `linked_sockets` values are insertion-ordered dicts, and
  `realize.restore_multi_input_orders` creates missing links in graph order
  rather than from a set of bpy sockets.
  Nothing that decides the result iterates a `set` any more: the cluster
  list `ClusterGraph.S` is a list, `descendants` / `ancestors` and the
  component functions of `tree.py` return their nodes in traversal order,
  and `subgraph` keeps the graph's order. (Upstream's sets are still there
  where only membership is asked.) A C++ port can therefore reproduce the
  order with plain arrays.
- **Robustness** (nodebpy-only):
  - `sugiyama.cycle_links()`: the layout drops the links that close a cycle
    itself rather than rely on Blender having marked one invalid, and
    reports a linked socket without a location as a `ValueError`.
  - `ranking.tight_tree`, `ranking.set_post_order_numbers`,
    `y_coords.place_block` and the matching in `stacking.py` use explicit
    stacks where upstream recurses, so a chain or column of thousands of
    nodes does not hit the recursion limit.
  - `ordering.minimize_crossings` draws from its own `random.Random(0)`
    (upstream reseeds the global generator) and clears the `@cache`s of
    `ordering.py` when done.
  - `stacking._point_multi_input_orders_at_stack()`: the saved multi-input
    orders follow the sockets a stack takes over.
  - `utils.dimensions()` divides drawn sizes by the UI scale, as
    `extract.get_socket_y()` does for socket positions.
- **A harness** (nodebpy-only): `LayoutResult.apply_to()` makes a layout's
  edits to the plain data, and `metrics.py` measures plain data, so a layout
  can be judged without Blender. `tests/arrange_corpus/` stores node trees
  as `tree_clipper` JSON with the location every node must end up at — the
  suite to hold a C++ port against, since the same files load into any
  Blender through Tree Clipper.
- `structs.py` (moved up from `arrange/`, since only `extract.py` uses it)
  uses explicit `_fields_` lists (upstream builds them from annotations, formerly via `eval`) and additionally binds `bNode` /
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
