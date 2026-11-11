# nodes.compositor.vector

`vector`

## Classes

| Name | Description |
|----|----|
| [Normalize](#nodebpy.nodes.compositor.vector.Normalize) | Map values to 0 to 1 range, based on the minimum and maximum pixel values |

### Normalize

``` python
Normalize(value=1.0)
```

Map values to 0 to 1 range, based on the minimum and maximum pixel values

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| value | InputFloat | Value       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.vector.Normalize.i) |  |
| [`name`](#nodebpy.nodes.compositor.vector.Normalize.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.vector.Normalize.node) |  |
| [`o`](#nodebpy.nodes.compositor.vector.Normalize.o) |  |
| [`tree`](#nodebpy.nodes.compositor.vector.Normalize.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.vector.Normalize.props) | Set the properties every node has and return the node, so it can |

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
| `i.value` | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |
