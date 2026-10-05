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

Only seven modules import `bpy`, and a test holds the rest to that:

| Module | What it is |
| --- | --- |
| `api.py` | `arrange()`, `SugiyamaOptions`, and `arrange_node_tree()`, which runs the three stages |
| `extract.py`, `apply.py`, `utils.py` | Stages 1 and 3 |
| `rows.py` | A node's height and socket positions, estimated from the rows it draws |
| `simple.py` | The other arrangement: plain columns by dependency |
| `__init__.py` | The package's exports |

`SugiyamaOptions` has the fields of `config.Settings` plus the margin.

## The layout is a layered drawing

The method is Sugiyama's: put the nodes in columns so every link runs left
to right, order each column to keep links from crossing, then decide the
heights. `sugiyama.py` holds the list of steps
(`default_pipeline()`); `pipeline.py` runs it. Four of the steps are
the *phases* that decide the picture; the rest prepare for one or clean up.

| Step | What it does | Where |
| --- | --- | --- |
| `prioritize_links` | Mark the trunk and the zone spines | `priority.py` |
| `save_multi_input_orders` | Remember the order of links into multi-input sockets | `sugiyama.py` |
| `remove_reroutes` | Take out the tree's own reroutes (`reroutes="all"`) | `realize.py` |
| `contract_stacks` | Make each stack of collapsed nodes one node | `stacking.py` |
| **`rank`** | Give every node a column | `ranking.py` |
| `balance_heights` | Move feeder chains left out of the tallest columns | `balancing.py` |
| `constrain_layers` | Group Output to the last column, Group Input to the first | `sugiyama.py` |
| `merge_edges`, `insert_dummy_nodes` | Split long links with a dummy node per column | `graph.py` |
| `add_columns` | List the nodes of each column | `sugiyama.py` |
| **`order`** | Order each column to reduce crossings | `ordering.py` |
| `add_frame_borders` | Border nodes above and below each frame, per column | `graph.py` |
| **`place`** | Give every node its height | `y_coords.py` |
| `dissolve_dummy_nodes` | Drop the dummy nodes (`reroutes="none"`) | `sugiyama.py` |
| `align_reroutes` | Line reroutes up with the sockets they join | `sugiyama.py` |
| `remove_frame_borders` | Drop the border nodes | `sugiyama.py` |
| `space_columns` | Give every column its x | `x_coords.py` |
| `dissolve_clear_dummy_nodes` | Drop dummy nodes of links that cross no node (`reroutes="blocked"`) | `sugiyama.py` |
| **`route`** | Bend points where a link would cut across a node | `x_coords.py` |
| `expand_stacks` | Put the stacked nodes back | `stacking.py` |
| `realize` | Write the result out as edits | `realize.py` |

Around the pipeline, `sugiyama_layout()` splits the tree into its
unconnected parts, runs the pipeline on each, packs the results
(`packing.py`), and, when only the selection is arranged, moves the result
off the nodes that stay put.

### The four phases

- **Rank** (`ranking.py`). Network simplex: columns chosen so the links are
  as short as possible in total. Frames add constraints: a frame's nodes
  stay between its two border nodes, and with `sequential_frames` a frame
  comes wholly after the frame that feeds it.
- **Order** (`ordering.py`). Graphviz dot's recipe, with nothing random in
  it. From a few fixed starting orders, sweep back and forth over the
  columns, putting each node at the average position of its neighbours in
  the column before; after each sweep swap neighbouring nodes wherever
  that lowers the cost of crossings; keep the cheapest order found. A
  crossing between a flow link and another link costs four times any other
  (`CROSSING_WEIGHTS`). A frame's nodes stay together in every column.
- **Place** (`y_coords.py`). Brandes and Köpf: each node is aligned with
  one neighbour into *blocks* that share a height, and the blocks are
  packed. This is done four times (aligning to the left or right
  neighbour, packing up or down); `direction` picks one or `BALANCED`
  takes the middle. With `straighten_trunk` a node aligns across its
  heaviest link first, which is what makes the trunk a straight row.
- **Route** (`x_coords.py`). With reroutes on, a link that would cut across
  the node above or below its end gets a bend point beside that node.

## Glossary

- **Cluster** (`graph.Cluster`): a frame, as the layout sees it. Clusters
  nest as frames do; the outermost stands for the whole tree.
- **Column, rank**: the same thing. `v.rank` is the index of the column
  node `v` is in; `G.columns` lists the nodes of each.
- **Dummy node**: a node the layout makes up where a long link passes a
  column, so that every link joins neighbouring columns. Dummy nodes become
  reroutes or are dropped, depending on `reroutes`.
- **Border node**: a made-up node above and below a frame's nodes in a
  column, which keeps room for the frame's outline.
- **Stack**: a chain of collapsed Math nodes, drawn as a tight vertical
  pile and laid out as one node.
- **Flow socket**: a socket of a type that carries a tree's main data:
  geometry, shader, bundle, closure (`priority.FLOW_SOCKETS`). A **flow
  link** is one that leaves a flow socket.
- **Trunk**: the line the main data runs along, a chain of flow links. The
  layout keeps it short and straight and hangs the chains of values that
  feed it off it.
- **Spine**: the trunk of a zone, from the zone's input node to its output
  node (`priority.zone_spine`). The nodes along it get their tops level.
- **Part**: a piece of the tree not linked to the rest (`packing.components`).
  Nodes sharing a frame or a zone are one part.
- **Fact** (`pipeline.Fact`): something true of the layout graph between
  two steps: *ranked*, *proper* (every link joins neighbouring columns),
  *columns*, *ordered*, *borders*, *y*, *x*.
- **`LayoutGraph`** (`digraph.py`): the graph being laid out, a directed
  multigraph of `graph.Node`s joined by `Link`s. Not to be confused with
  the node tree (`dna.bNodeTree`) it was built from, or with `T`, which in
  `ranking.py` is a spanning tree and elsewhere the nesting of frames.

## Steps state what they need

Each `Step` names the facts it `requires`, `provides` and `removes`.
`Pipeline.check()` refuses a list of steps that do not fit together before
anything runs. `sugiyama_layout(..., verify=True)` checks every fact
against the graph after every step (`pipeline.CHECKS`) and names the step
that broke one. The random-tree test runs with it on.

## Changing the layout

- **Another algorithm for a phase:** take `default_pipeline()` and
  `pipeline.replace("rank", function)`. The function gets the
  `pipeline.Layout` and must leave the graph as the step's `provides`
  says. `ranking.longest_path_ranks` is a second ranking to try this with.
- **An extra pass:** `pipeline.insert_after(name, Step(...))`.
- **Watching it run:** pass `observer=` to `sugiyama_layout()`; it is
  called after each step with the step, the layout and the time taken.
- **Tuning numbers** are constants beside the code that uses them:
  `ordering.CROSSING_WEIGHTS`, `balancing.BALANCE_ASPECT`,
  `balancing.BALANCE_MIN_COLUMN`, `common.REROUTE_MARGIN_Y_FAC`,
  `stacking.STACK_MARGIN_Y_FAC`.
- **Judging a change:** `make arrange-corpus` re-lays the stored trees of
  `tests/arrange_corpus/` and prints what changed in each layout's counts
  (crossings, level links, size). `make arrange-report` prints the full
  metrics and can draw the trees. Both use `tests/arrange_metrics.py`.

## Notes for a port to C++

- **What ports:** the modules that do not import `bpy`. Their input is the real `bNodeTree`; its
  output, the edit list, becomes direct calls (`bke::node_add_link` and so
  on).
- **What does not:** `dna.py`, `extract.py`, `apply.py` and `zones.py`
  exist because Python sees only part of Blender. A port reads the structs,
  `bNodeTree::zones()` and the drawn sizes itself. The observer and the
  test tooling stay in Python.
- **Order is by insertion everywhere.** No result depends on iterating a
  hash set, so plain arrays reproduce it. `graph.Node` hashes by a creation
  serial for the same reason; a port would use indices.
- **The one random source** is `ordering._Lcg`, the generator of `drand48`
  and of Blender's `RandomNumberGenerator`, seeded with 0, used for a few
  shuffled starting orders on small graphs.
- **Python conveniences to unpick:** the `@cache`s keyed on graphs in
  `ordering.py` and `ranking.py` (cleared by hand after use), the
  Brandes-Köpf scratch fields kept on `graph.Node` (`root`, `aligned`,
  `sink`, `shift`, `inner_shift`), and `dataclasses.replace` on
  `graph.Socket`.
- **Single precision is only partly emulated** (`common.f32`): positions
  are rounded as Blender stores them, but the placement itself runs in
  doubles.
- **Node sizes are only known to Blender once a node editor has drawn the
  tree.** Headless, they are estimated (`rows.py`).
- **Not a conformance suite:** `tests/arrange_corpus/` stores positions
  that depend on those estimated sizes, which the files do not hold.
- **Still linear per step:** each exchange of the network simplex scans
  every node and link.
