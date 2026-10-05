# How the node layout works

This package lays out a Blender node tree. This file explains its design.

It grew out of the add-on
[node-arrange](https://github.com/Leonardo-Pike-Excell/node-arrange) by
Leonardo Pike-Excell, and the modules that descend from it keep its
`GPL-2.0-or-later` licence header. It is no longer kept in step with that
add-on.

## Three stages

```
Blender tree --extract.py--> plain data --sugiyama.py--> edits --apply.py--> Blender tree
```

1. **Extract** (`extract.py`) copies what the layout reads into plain data
   (`dna.py`): nodes with their sizes, sockets with the height links attach
   at, links, frames, zones. The structs are named after Blender's
   (`bNodeTree`, `bNode`, `bNodeSocket`, `bNodeLink`, `bNodeTreeZone`).
2. **Lay out** (`sugiyama.sugiyama_layout()` and the modules it uses)
   computes the layout from that data alone and returns a list of edits
   (`edits.py`): move a node, add or remove a reroute or a link. It never
   touches Blender.
3. **Apply** (`apply.py`) carries the edits out on the Blender tree.

`api.arrange()` runs the three stages. `arrange(tree, "simple")` is the same
layout with the preset `config.SIMPLE_OPTIONS`.

## Modules

Four modules import `bpy`: `api`, `extract`, `apply` and `node_size`.
`__init__.py` only re-exports. Every other module is pure Python over plain
data.

**Blender side**

| Module | What it holds |
| --- | --- |
| `api.py` | `arrange()`, the public entry |
| `extract.py` | Stage 1: the Blender tree as plain data |
| `apply.py` | Stage 3: the edits carried out on the Blender tree |
| `node_size.py` | A node's box and socket positions: measured when drawn, else estimated from the rows it draws |

**Data and options**

| Module | What it holds |
| --- | --- |
| `dna.py` | The plain-data tree: `bNodeTree`, `bNode`, `bNodeSocket`, `bNodeLink`, `bNodeTreeZone` |
| `zones.py` | Which nodes are in which zone |
| `edits.py` | The edits a layout returns, and `LayoutResult` |
| `config.py` | `SugiyamaOptions`, `SIMPLE_OPTIONS`, and `LayoutState`, the state of one run |

**Graph**

| Module | What it holds |
| --- | --- |
| `digraph.py` | `LayoutGraph`, `DiGraph` and the graph algorithms |
| `model.py` | `Node`, `Socket`, `Cluster`, `ClusterGraph` |
| `build.py` | Index the links, break cycles, build the layout graph, list the columns |

**Pipeline and phases**

| Module | What it holds |
| --- | --- |
| `pipeline.py` | `Step`, `Pipeline`, the facts and their checks |
| `sugiyama.py` | `default_pipeline()` and `sugiyama_layout()` |
| `priority.py` | Link priorities: the trunk and the zone spines |
| `ranking.py` | Rank: a column for every node |
| `balancing.py` | Shorten the tallest columns |
| `ordering.py` | Order: the order within each column |
| `placement.py` | Place: a height for every node (Brandes-Köpf) |
| `spacing.py` | An x for every column |
| `routing.py` | Route: bend points |
| `realize.py` | Write the result out as edits |

**Reroutes and stacks**

| Module | What it holds |
| --- | --- |
| `long_links.py` | Dummy nodes on long links |
| `reroutes.py` | Dissolving and aligning dummy nodes |
| `stacking.py` | Stacks of collapsed Math nodes |

**Other**

| Module | What it holds |
| --- | --- |
| `packing.py` | Splitting the tree into parts and packing the laid-out parts |
| `snapping.py` | Moving the finished layout onto the node editor's grid |
| `common.py` | `Vec2`, `f32`, segment intersection, shared constants |

## Sizes

Blender only knows a node's size once a node editor has drawn it. Then
`node.dimensions` is used; otherwise the size is estimated from the rows the
node draws (`node_size.py`). Socket heights are always estimated. A tree
arranged in the UI can therefore come out differently from the same tree
arranged headless.

## The layout is a layered drawing

The method is Sugiyama's: put the nodes in columns so every link runs left
to right, order each column to keep links from crossing, then decide the
heights. `sugiyama.default_pipeline()` holds the list of steps and
`pipeline.py` runs it. Four of the steps are the *phases* that decide the
picture. The rest prepare for one or clean up.

| Step | What it does | Runs when | Where |
| --- | --- | --- | --- |
| `prioritize_links` | Mark the trunk and the zone spines | `straighten_trunk` | `priority.py` |
| `save_multi_input_orders` | Remember the order of links into multi-input sockets | always | `build.py` |
| `remove_reroutes` | Take out the tree's own reroutes | `reroutes="all"` | `realize.py` |
| `contract_stacks` | Make each stack of collapsed nodes one node | `stack_collapsed` | `stacking.py` |
| **`rank`** | Give every node a column | always | `ranking.py` |
| `balance_heights` | Move feeder chains left out of the tallest columns | `balance_heights` | `balancing.py` |
| `constrain_layers` | Group Output to the last column (`pin_group_output`), Group Input to the first (`pin_group_input`) | always | `sugiyama.py` |
| `merge_edges` | Let the long links from one output share dummy nodes | always | `long_links.py` |
| `insert_dummy_nodes` | Split long links with a dummy node per column | always | `long_links.py` |
| `add_columns` | List the nodes of each column | always | `build.py` |
| **`order`** | Order each column to reduce crossings | always | `ordering.py` |
| `add_frame_borders` | Border nodes above and below each frame, per column | always | `sugiyama.py`, `model.py` |
| **`place`** | Give every node its height | always | `placement.py` |
| `dissolve_dummy_nodes` | Drop the dummy nodes | `reroutes="none"` | `reroutes.py` |
| `align_reroutes` | Line reroutes and dummy nodes up with the sockets they join | always | `reroutes.py` |
| `remove_frame_borders` | Drop the border nodes | always | `sugiyama.py` |
| `space_columns` | Give every column its x | always | `spacing.py` |
| `dissolve_clear_dummy_nodes` | Drop the dummy nodes of links that cross no node | `reroutes="blocked"` | `reroutes.py` |
| **`route`** | Bend points where a link would cut across a node | `reroutes` is not `"none"` | `routing.py` |
| `expand_stacks` | Put the stacked nodes back | `stack_collapsed` | `stacking.py` |
| `realize` | Write the result out as edits | always | `realize.py` |

Around the pipeline, `sugiyama_layout()` splits the tree into its parts
(with `pack_components`), runs the pipeline on each, and packs the results
(`packing.py`). When only the selection is arranged it also moves the result
off the nodes that stay put. Last, with `snap_to_grid`, every node is moved
to the nearest point of the node editor's grid (`snapping.py`); nodes keep
the gap they had, rounded down to the grid, and reroutes are left alone so
their links stay straight.

### The four phases

- **Rank** (`ranking.py`). Network simplex: columns chosen so the links are
  as short as possible in total. Every link has weight 1. Frames add
  constraints: a frame's nodes stay between its two border nodes, and with
  `frames_as_stages` a frame comes wholly after the frame that feeds it.
- **Order** (`ordering.py`). Graphviz dot's recipe, deterministic for a
  given `seed`. From a few fixed starting orders, and on small graphs a few
  shuffled ones, sweep back and forth over the columns, putting each node
  at the average position of its neighbours in the column before. After
  each sweep swap neighbouring nodes wherever that lowers the cost of
  crossings. Keep the cheapest order found. A crossing between a flow link
  and another link costs four times any other (`CROSSING_WEIGHTS`). A
  frame's nodes stay together in every column.
- **Place** (`placement.py`). Brandes and Köpf: each node is aligned with
  one neighbour into *blocks* that share a height, and the blocks are
  packed. This is done four times (aligning to the left or right
  neighbour, packing up or down). `direction` picks one, or `BALANCED`
  takes the middle. With `straighten_trunk` a node aligns across its
  heaviest link first, which is what makes the trunk a straight row.
  Priorities affect only this phase.
- **Route** (`routing.py`). With reroutes on, a link that would cut across
  the node above or below its end gets a bend point beside that node.

## Glossary

- **Cluster** (`model.Cluster`): a frame, as the layout sees it. Clusters
  nest as frames do. The outermost stands for the whole tree.
- **`CG`** (`model.ClusterGraph`): the layout graph `G` together with `T`,
  the nesting of nodes and clusters, and `S`, the list of clusters.
- **Column, rank**: the same thing. `v.rank` is the index of the column
  node `v` is in. `G.columns` lists the nodes of each.
- **Dummy node**: a node the layout makes up where a long link passes a
  column, so that every link joins neighbouring columns. Dummy nodes become
  reroutes or are dropped, depending on `reroutes`.
- **Border node**: a made-up node above and below a frame's nodes in a
  column, which keeps room for the frame's outline. During ranking a frame
  also has one border node to its left and one to its right.
- **Stack**: a chain of collapsed Math nodes, drawn as a tight vertical
  pile and laid out as one node.
- **Flow socket**: a socket of a type that carries a tree's main data:
  geometry, shader, bundle, closure (`priority.FLOW_SOCKETS`). A **flow
  link** is one that leaves a flow socket.
- **Trunk**: the line the main data runs along, a chain of flow links. The
  placement keeps it straight and hangs the chains of values that feed it
  off it.
- **Spine**: the trunk of a zone, from the zone's input node to its output
  node (`priority.zone_spine`). The nodes along it get their tops level.
- **Part**: a piece of the tree not linked to the rest. Nodes sharing a
  frame or a zone are one part. The function is `packing.components` and
  the option `pack_components`.
- **Sink**: in the placement, the root node shared by a group of blocks
  that rest on one another. The whole group moves by the sink's `shift`.
- **Marked nodes**: in the placement, the nodes of a frame whose contents
  were placed with a gap wider than the margin. On the next try they do not
  align with nodes in another cluster.
- **Fact** (`pipeline.Fact`): something true of the layout graph between
  two steps: *ranked*, *proper* (every link joins neighbouring columns),
  *columns*, *ordered*, *borders*, *y*, *x*.
- **`LayoutGraph`** (`digraph.py`): the graph being laid out, a directed
  multigraph of `model.Node`s joined by `Link`s. Not to be confused with
  the node tree (`dna.bNodeTree`) it was built from, or with `T`, which in
  `ranking.py` is a spanning tree and elsewhere the nesting of frames.

## Steps state what they need

Each `Step` names the facts it `requires`, `provides` and `removes`.
`Pipeline.check()` refuses a list of steps that do not fit together before
anything runs. `sugiyama_layout(..., verify=True)` checks every fact
against the graph after every step (`pipeline.CHECKS`) and names the step
that broke one.

## Changing the layout

- **Another algorithm for a phase:** take `default_pipeline()` and replace
  the step. The function gets the `pipeline.Layout` and must leave the
  graph as the step's `provides` says. For example, to rank by longest
  path:

  ```python
  pipeline = default_pipeline()
  pipeline.replace(
      "rank", lambda L: ranking.compute_ranks(L.CG, ranking.longest_path_ranks)
  )
  arrange(tree, pipeline=pipeline)
  ```

- **An extra pass:** `pipeline.insert_after(name, Step(...))`.
- **Watching it run:** pass `observer=` to `sugiyama_layout()` or
  `arrange()`. It is called after each step with the step, the layout and
  the time taken.
- **Another order:** `SugiyamaOptions(seed=...)` changes the shuffled
  starting orders the ordering tries on small graphs. The layout is
  deterministic for a given `seed`.
- **Tuning numbers** are constants beside the code that uses them:
  `ordering.CROSSING_WEIGHTS`, `balancing.BALANCE_ASPECT`,
  `balancing.BALANCE_MIN_COLUMN`, `common.REROUTE_MARGIN_Y_FAC`,
  `stacking.STACK_MARGIN_Y_FAC`.
- **Judging a change:** the tests are in `tests/layout/`.
  `make layout-corpus` (`python -m tests.layout.corpus --update`) lays the
  stored trees out again and prints what changed in each layout's counts
  (crossings, level links, size). `make layout-report`
  (`python -m tests.layout.report`) prints the full metrics and can draw
  the trees.
- **Accepting a corpus change:** a change must add no overlaps and no
  backward links. Judge crossings and level links from the printed counts.

## Notes for a port to C++

- **What ports:** the pure layout modules, except `dna.py` and `zones.py`.
  Those two exist because Python sees only part of Blender. A port reads
  the real `bNodeTree`, `bNodeTree::zones()` and the drawn sizes itself.
  The edit list becomes direct calls (`bke::node_add_link` and so on).
- **What does not:** `api.py`, `extract.py`, `apply.py`, `node_size.py`,
  the observer and the test tooling.
- **Coordinates:** `runtime->draw_bounds` and the socket locations are in
  view space, multiplied by the UI scale. `location` is not.
  `bNode.location` is absolute in current Blender, so `MoveNode` maps
  directly.
- **Multi-input order:** the sort ids can be written directly, without the
  swapping `apply.py` does.
- **After the edits** the tree needs an update and an undo push.
- **Snapping:** an operator would set `snap_to_grid` from the node
  editor's Snap setting (`tool_settings.use_snap_node`), and use
  `NODE_GRID_STEP_SIZE` for `snapping.GRID_SIZE`.
- **Order is by insertion everywhere.** No result depends on iterating a
  hash set, so plain arrays reproduce it. `model.Node` hashes by a creation
  serial for the same reason. A port would use indices.
- **The one random source** is `ordering.Lcg`, the generator of `drand48`
  and of Blender's `RandomNumberGenerator`, seeded with `options.seed`. It
  gives a few shuffled starting orders on small graphs.
- **Python conveniences to unpick:** the `@cache`s keyed on graphs in
  `ordering.py` and `ranking.py` (cleared by hand after use), the
  Brandes-Köpf scratch fields kept on `model.Node` (`root`, `aligned`,
  `sink`, `shift`, `inner_shift`), and `dataclasses.replace` on
  `model.Socket`.
- **Single precision is only partly emulated** (`common.f32`): positions
  are rounded as Blender stores them, but the placement itself runs in
  doubles.
- **Cost:** each network-simplex exchange scans every node and link.
