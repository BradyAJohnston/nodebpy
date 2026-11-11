# nodes.geometry.color

`color`

## Classes

| Name | Description |
|----|----|
| [Gamma](#nodebpy.nodes.geometry.color.Gamma) | Apply a gamma correction |
| [RGBCurves](#nodebpy.nodes.geometry.color.RGBCurves) | Apply color corrections for each color channel |

### Gamma

``` python
Gamma(color=None, gamma=1.0)
```

Apply a gamma correction

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| color | InputColor | Color       | `None`  |
| gamma | InputFloat | Gamma       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.color.Gamma.i) |  |
| [`name`](#nodebpy.nodes.geometry.color.Gamma.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.color.Gamma.node) |  |
| [`o`](#nodebpy.nodes.geometry.color.Gamma.o) |  |
| [`tree`](#nodebpy.nodes.geometry.color.Gamma.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.color.Gamma.props) | Set the properties every node has and return the node, so it can |

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
| `i.color` | `ColorSocket` | Color       |
| `i.gamma` | `FloatSocket` | Gamma       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### RGBCurves

``` python
RGBCurves(factor=1.0, color=(1.0, 1.0, 1.0, 1.0))
```

Apply color corrections for each color channel

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| factor | InputFloat | Factor. Renamed from `Fac`; `i.fac` still resolves to it. | `1.0` |
| color | InputColor | Color | `(1.0, 1.0, 1.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.color.RGBCurves.i) |  |
| [`name`](#nodebpy.nodes.geometry.color.RGBCurves.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.color.RGBCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.color.RGBCurves.o) |  |
| [`tree`](#nodebpy.nodes.geometry.color.RGBCurves.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.color.RGBCurves.props) | Set the properties every node has and return the node, so it can |

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

| Attribute | Type | Description |
|----|----|----|
| `i.factor` | `FloatSocket` | Factor. Renamed from `Fac`; `i.fac` still resolves to it. |
| `i.color` | `ColorSocket` | Color |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
