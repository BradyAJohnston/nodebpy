# nodes.compositor.output

`output`

## Classes

| Name | Description |
|----|----|
| [FileOutput](#nodebpy.nodes.compositor.output.FileOutput) | Write image file to disk |
| [Viewer](#nodebpy.nodes.compositor.output.Viewer) | Visualize data from inside a node graph, in the image editor or as a backdrop |

### FileOutput

``` python
FileOutput(
    active_item_index=0,
    directory='',
    file_name='',
    save_as_render=False,
)
```

Write image file to disk

#### Attributes

| Name | Description |
|----|----|
| [`active_item_index`](#nodebpy.nodes.compositor.output.FileOutput.active_item_index) |  |
| [`directory`](#nodebpy.nodes.compositor.output.FileOutput.directory) |  |
| [`file_name`](#nodebpy.nodes.compositor.output.FileOutput.file_name) |  |
| [`i`](#nodebpy.nodes.compositor.output.FileOutput.i) |  |
| [`name`](#nodebpy.nodes.compositor.output.FileOutput.name) |  |
| [`node`](#nodebpy.nodes.compositor.output.FileOutput.node) |  |
| [`o`](#nodebpy.nodes.compositor.output.FileOutput.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.output.FileOutput.outputs) |  |
| [`save_as_render`](#nodebpy.nodes.compositor.output.FileOutput.save_as_render) |  |
| [`tree`](#nodebpy.nodes.compositor.output.FileOutput.tree) |  |
| [`type`](#nodebpy.nodes.compositor.output.FileOutput.type) |  |

### Viewer

``` python
Viewer(image=None, *, ui_shortcut=0)
```

Visualize data from inside a node graph, in the image editor or as a backdrop

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.output.Viewer.i) |  |
| [`name`](#nodebpy.nodes.compositor.output.Viewer.name) |  |
| [`node`](#nodebpy.nodes.compositor.output.Viewer.node) |  |
| [`o`](#nodebpy.nodes.compositor.output.Viewer.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.output.Viewer.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.output.Viewer.tree) |  |
| [`type`](#nodebpy.nodes.compositor.output.Viewer.type) |  |
| [`ui_shortcut`](#nodebpy.nodes.compositor.output.Viewer.ui_shortcut) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
