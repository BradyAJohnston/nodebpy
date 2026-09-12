# SugiyamaOptions

``` python
SugiyamaOptions(
    margin=(30.0, 30.0),
    direction='RIGHT_UP',
    socket_alignment='NONE',
    add_reroutes=False,
    keep_reroutes_outside_frames=False,
    stack_collapsed=True,
    stack_margin_y_fac=0.5,
    optimize_sizes=False,
    iterations=50,
)
```

Options for the Sugiyama (layered) arrangement.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| margin | tuple\[float, float\] | Horizontal and vertical space between nodes. | `(30.0, 30.0)` |
| direction | str | Which directions nodes may be moved in during layout. | `'RIGHT_UP'` |
| socket_alignment | str | How aggressively links are straightened by aligning the sockets they connect. | `'NONE'` |
| add_reroutes | bool | Insert reroute nodes to route long edges around nodes. Off by default: added reroutes are real nodes, which would change the authored structure of generated trees (node counts, round-trips, diagrams). | `False` |
| keep_reroutes_outside_frames | bool | Do not place added reroutes inside frames. | `False` |
| stack_collapsed | bool | Stack consecutive collapsed nodes tightly. | `True` |
| stack_margin_y_fac | float | Fraction of the vertical margin used between stacked collapsed nodes. | `0.5` |
| optimize_sizes | bool | Fit the widths of collapsed nodes to their display name. | `False` |
| iterations | int | Number of crossing-minimization iterations. | `50` |

## Attributes

| Name | Description |
|----|----|
| [`add_reroutes`](#nodebpy.SugiyamaOptions.add_reroutes) |  |
| [`direction`](#nodebpy.SugiyamaOptions.direction) |  |
| [`iterations`](#nodebpy.SugiyamaOptions.iterations) |  |
| [`keep_reroutes_outside_frames`](#nodebpy.SugiyamaOptions.keep_reroutes_outside_frames) |  |
| [`margin`](#nodebpy.SugiyamaOptions.margin) |  |
| [`optimize_sizes`](#nodebpy.SugiyamaOptions.optimize_sizes) |  |
| [`socket_alignment`](#nodebpy.SugiyamaOptions.socket_alignment) |  |
| [`stack_collapsed`](#nodebpy.SugiyamaOptions.stack_collapsed) |  |
| [`stack_margin_y_fac`](#nodebpy.SugiyamaOptions.stack_margin_y_fac) |  |
