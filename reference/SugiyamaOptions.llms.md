# SugiyamaOptions

``` python
SugiyamaOptions(
    margin=(30.0, 30.0),
    direction='BALANCED',
    socket_alignment='NONE',
    add_reroutes=False,
    keep_reroutes_outside_frames=False,
    stack_collapsed=True,
    stack_margin_y_fac=0.5,
    optimize_sizes=False,
    iterations=50,
    sequential_frames=True,
    balance_heights=True,
    balance_aspect=1.6,
    reroute_margin_y_fac=0.35,
)
```

Options for the Sugiyama (layered) arrangement.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| margin | tuple\[float, float\] | Horizontal and vertical space between nodes. | `(30.0, 30.0)` |
| direction | str | Which directions nodes may be moved in during layout. | `'BALANCED'` |
| socket_alignment | str | How aggressively links are straightened by aligning the sockets they connect. | `'NONE'` |
| add_reroutes | bool | Insert reroute nodes to route long edges around nodes. Off by default: added reroutes are real nodes, which would change the authored structure of generated trees (node counts, round-trips, diagrams). | `False` |
| keep_reroutes_outside_frames | bool | Do not place added reroutes inside frames. | `False` |
| stack_collapsed | bool | Stack consecutive collapsed nodes tightly. | `True` |
| stack_margin_y_fac | float | Fraction of the vertical margin used between stacked collapsed nodes. | `0.5` |
| optimize_sizes | bool | Fit the widths of collapsed nodes to their display name. | `False` |
| iterations | int | Number of crossing-minimization iterations. | `50` |
| sequential_frames | bool | Rank frames as stages of the flow: every node of a frame comes after every node of the frame (or intermediate node) feeding it, so successive frames line up left to right instead of stacking into a staircase. Frames with no links between them (parallel branches) still share columns and stack vertically. | `True` |
| balance_heights | bool | Shorten the tallest column by moving nodes whose feeders serve only them (a private upstream chain) one column left, while that makes the drawing smaller overall. Counters the tall sliver a node with many inputs otherwise produces, at the price of slightly longer links routed through reroutes / dummy nodes. | `True` |
| balance_aspect | float | Width-to-height ratio the balancing aims for: it keeps promoting feeders left while the drawing’s bounding box (height, or width divided by this ratio, whichever is larger) shrinks. | `1.6` |
| reroute_margin_y_fac | float | Fraction of the vertical margin kept between consecutive reroutes (and the dummy nodes long links are routed through) in a column; bundles of long links pack tighter than nodes. | `0.35` |

## Attributes

| Name | Description |
|----|----|
| [`add_reroutes`](#nodebpy.SugiyamaOptions.add_reroutes) |  |
| [`balance_aspect`](#nodebpy.SugiyamaOptions.balance_aspect) |  |
| [`balance_heights`](#nodebpy.SugiyamaOptions.balance_heights) |  |
| [`direction`](#nodebpy.SugiyamaOptions.direction) |  |
| [`iterations`](#nodebpy.SugiyamaOptions.iterations) |  |
| [`keep_reroutes_outside_frames`](#nodebpy.SugiyamaOptions.keep_reroutes_outside_frames) |  |
| [`margin`](#nodebpy.SugiyamaOptions.margin) |  |
| [`optimize_sizes`](#nodebpy.SugiyamaOptions.optimize_sizes) |  |
| [`reroute_margin_y_fac`](#nodebpy.SugiyamaOptions.reroute_margin_y_fac) |  |
| [`sequential_frames`](#nodebpy.SugiyamaOptions.sequential_frames) |  |
| [`socket_alignment`](#nodebpy.SugiyamaOptions.socket_alignment) |  |
| [`stack_collapsed`](#nodebpy.SugiyamaOptions.stack_collapsed) |  |
| [`stack_margin_y_fac`](#nodebpy.SugiyamaOptions.stack_margin_y_fac) |  |
