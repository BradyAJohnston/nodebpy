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
    directory='',
    file_name='',
    save_as_render=True,
    use_file_extension=True,
)
```

Write image file to disk

#### Attributes

| Name | Description |
|----|----|
| [`directory`](#nodebpy.nodes.compositor.output.FileOutput.directory) |  |
| [`file_name`](#nodebpy.nodes.compositor.output.FileOutput.file_name) |  |
| [`i`](#nodebpy.nodes.compositor.output.FileOutput.i) |  |
| [`items`](#nodebpy.nodes.compositor.output.FileOutput.items) | The inputs to write, one per item. |
| [`name`](#nodebpy.nodes.compositor.output.FileOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.output.FileOutput.node) |  |
| [`o`](#nodebpy.nodes.compositor.output.FileOutput.o) |  |
| [`save_as_render`](#nodebpy.nodes.compositor.output.FileOutput.save_as_render) |  |
| [`tree`](#nodebpy.nodes.compositor.output.FileOutput.tree) |  |
| [`use_file_extension`](#nodebpy.nodes.compositor.output.FileOutput.use_file_extension) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.compositor.output.FileOutput.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.compositor.output.FileOutput.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [capture](#nodebpy.nodes.compositor.output.FileOutput.capture) | Deprecated: use `items.new(value, name).output`. |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

### Viewer

``` python
Viewer(image=(0.0, 0.0, 0.0, 1.0), *, ui_shortcut=0)
```

Visualize data from inside a node graph, in the image editor or as a backdrop

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| image | InputColor | Image       | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.output.Viewer.i) |  |
| [`name`](#nodebpy.nodes.compositor.output.Viewer.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.output.Viewer.node) |  |
| [`o`](#nodebpy.nodes.compositor.output.Viewer.o) |  |
| [`tree`](#nodebpy.nodes.compositor.output.Viewer.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`ui_shortcut`](#nodebpy.nodes.compositor.output.Viewer.ui_shortcut) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
