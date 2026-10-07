# SugiyamaOptions

``` python
SugiyamaOptions(
    margin=(30.0, 30.0),
    direction='BALANCED',
    socket_alignment='NONE',
    reroutes='none',
    stack_collapsed=True,
    fit_collapsed_widths=False,
    straighten_trunk=True,
    pin_group_output=True,
    pin_group_input=False,
    frames_as_stages=True,
    balance_heights=True,
    pack_components=True,
    seed=0,
    snap_to_grid=True,
)
```

Options for the Sugiyama (layered) arrangement.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| margin | tuple\[float, float\] | Horizontal and vertical space between nodes. | `(30.0, 30.0)` |
| direction | str | Which way nodes lean where they could sit in several places along a column: `"LEFT_UP"`, `"LEFT_DOWN"`, `"RIGHT_UP"`, `"RIGHT_DOWN"`, or `"BALANCED"` for the middle of the four. | `'BALANCED'` |
| socket_alignment | str | Whether aligned nodes line up by their tops (`"NONE"`), by the sockets of the link between them so the link is straight (`"FULL"`), or by sockets only where the nodes differ much in height (`"MODERATE"`). | `'NONE'` |
| reroutes | str | Which links get reroute nodes. `"none"`: the layout only moves nodes. `"blocked"`: links that would otherwise be drawn across a node get reroutes, and the reroutes already in the tree are kept. `"all"`: every link that passes over a column gets reroutes, and the tree’s own reroutes are replaced. | `'none'` |
| stack_collapsed | bool | Stack chains of collapsed Math nodes vertically. | `True` |
| fit_collapsed_widths | bool | Fit the widths of collapsed nodes to their display name. | `False` |
| straighten_trunk | bool | Align the trunk first, so that the flow links (geometry, shader, bundle, closure) form a straight row and each zone is a row with its node tops level. Off, a node aligns with its median neighbour. | `True` |
| pin_group_output | bool | Put Group Output nodes (outside frames) in the last column. | `True` |
| pin_group_input | bool | Put Group Input nodes (outside frames) in the first column. Off, they sit next to the nodes they feed. | `False` |
| frames_as_stages | bool | Put every node of a frame in a later column than every node of the frame, or node outside frames, that feeds it. Frames then line up left to right. | `True` |
| balance_heights | bool | Shorten the tallest columns by moving the chains that feed them one column left, while that brings the drawing closer to a screen’s shape. | `True` |
| seed | int | Seed of the shuffled starting orders the ordering tries besides its fixed ones. The same seed always gives the same layout. | `0` |
| snap_to_grid | bool | Put every node on the node editor’s grid, as Blender’s Snap does when nodes are moved by hand, and space the nodes of a column in whole grid steps. Reroutes are not snapped; they follow the sockets they join. With this on, `socket_alignment` can only line sockets up to within half a grid step. | `True` |

## Attributes

| Name | Description |
|----|----|
| [`balance_heights`](#nodebpy.SugiyamaOptions.balance_heights) |  |
| [`direction`](#nodebpy.SugiyamaOptions.direction) |  |
| [`fit_collapsed_widths`](#nodebpy.SugiyamaOptions.fit_collapsed_widths) |  |
| [`frames_as_stages`](#nodebpy.SugiyamaOptions.frames_as_stages) |  |
| [`margin`](#nodebpy.SugiyamaOptions.margin) |  |
| [`pack_components`](#nodebpy.SugiyamaOptions.pack_components) |  |
| [`pin_group_input`](#nodebpy.SugiyamaOptions.pin_group_input) |  |
| [`pin_group_output`](#nodebpy.SugiyamaOptions.pin_group_output) |  |
| [`reroutes`](#nodebpy.SugiyamaOptions.reroutes) |  |
| [`seed`](#nodebpy.SugiyamaOptions.seed) |  |
| [`snap_to_grid`](#nodebpy.SugiyamaOptions.snap_to_grid) |  |
| [`socket_alignment`](#nodebpy.SugiyamaOptions.socket_alignment) |  |
| [`stack_collapsed`](#nodebpy.SugiyamaOptions.stack_collapsed) |  |
| [`straighten_trunk`](#nodebpy.SugiyamaOptions.straighten_trunk) |  |
