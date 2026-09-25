# export.to_plot

``` python
to_plot(
    tree,
    filepath,
    *,
    title=None,
    dpi=150,
    node=False,
    open_panels=False,
    width=None,
    axes=False,
    grid=True,
)
```

Draw a node tree to an image file, Blender-style.

By default the tree’s *internals* are drawn: nodes at their real locations with the same estimated dimensions the arranger uses, so what you see is what the layout algorithm saw. Each node shows its header colour, title, socket markers, value widgets for unlinked inputs, and property dropdowns; links are coloured by socket type (dashed for fields), and frames and zones are drawn behind their members.

With `node=True` the tree is drawn instead as the single group node a user sees when adding it to another tree: a scratch tree holding one group node that references *tree* is drawn and discarded, showing the group’s interface — inputs with their default values, outputs, and interface panels in their default open / closed state.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| tree | bpy.types.NodeTree | The node tree to draw. | *required* |
| filepath | str \| Path | Image path; the format follows the extension (`.png`, `.svg`, `.pdf`, …). | *required* |
| title | str \| None | Text drawn in the top-left corner, like the editor’s breadcrumb. Defaults to no title; pass `tree.name` to label the render. | `None` |
| dpi | int | Output resolution. One Blender UI unit is drawn as one point, so a default 140-wide node is about 290 px across at 150 dpi. Very large trees lower the dpi automatically to stay within a sane image size. | `150` |
| node | bool | Draw the tree as one group node rather than its internals. | `False` |
| open_panels | bool | With `node=True`, expand every interface panel instead of honouring each panel’s default closed state, so all sockets are visible for review. | `False` |
| width | float \| None | With `node=True`, the group node’s width in UI units; defaults to Blender’s default group-node width (140), which is also what a user gets when adding the group. | `None` |
| axes | bool | Frame the drawing with axes ticked in Blender UI units (node locations), handy for reading off distances when tuning a layout. | `False` |
| grid | bool | Draw the editor’s dotted background grid. | `True` |
