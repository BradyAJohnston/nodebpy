# builder.BaseNode

``` python
BaseNode(node=None)
```

Base class for all node wrappers.

## Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.BaseNode.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.BaseNode.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.BaseNode.node) |  |
| [`o`](#nodebpy.builder.BaseNode.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.BaseNode.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

## Methods

| Name | Description |
|----|----|
| [props](#nodebpy.builder.BaseNode.props) | Set the properties every node has and return the node, so it can |

### props

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
