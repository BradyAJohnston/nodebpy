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
| [props](#nodebpy.nodes.compositor.output.FileOutput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

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

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.output.Viewer.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
