# nodes.shader.color

`color`

## Classes

| Name | Description |
|----|----|
| [BrightnessContrast](#nodebpy.nodes.shader.color.BrightnessContrast) | Control the brightness and contrast of the input color |
| [HueSaturationValue](#nodebpy.nodes.shader.color.HueSaturationValue) | Apply a color transformation in the HSV color model |
| [InvertColor](#nodebpy.nodes.shader.color.InvertColor) | Invert a color, producing a negative |
| [LightFalloff](#nodebpy.nodes.shader.color.LightFalloff) | Manipulate how light intensity decreases over distance. Typically used for non-physically-based effects; in reality light always falls off quadratically |

### BrightnessContrast

``` python
BrightnessContrast(color=(1.0, 1.0, 1.0, 1.0), brightness=0.0, contrast=0.0)
```

Control the brightness and contrast of the input color

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| color | InputColor | Color | `(1.0, 1.0, 1.0, 1.0)` |
| brightness | InputFloat | Brightness. Renamed from `Bright`; `i.bright` still resolves to it. | `0.0` |
| contrast | InputFloat | Contrast | `0.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.BrightnessContrast.i) |  |
| [`name`](#nodebpy.nodes.shader.color.BrightnessContrast.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.color.BrightnessContrast.node) |  |
| [`o`](#nodebpy.nodes.shader.color.BrightnessContrast.o) |  |
| [`tree`](#nodebpy.nodes.shader.color.BrightnessContrast.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.color.BrightnessContrast.props) | Set the properties every node has and return the node, so it can |

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
| `i.color` | `ColorSocket` | Color |
| `i.brightness` | `FloatSocket` | Brightness. Renamed from `Bright`; `i.bright` still resolves to it. |
| `i.contrast` | `FloatSocket` | Contrast |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### HueSaturationValue

``` python
HueSaturationValue(
    hue=0.5,
    saturation=1.0,
    value=1.0,
    factor=1.0,
    color=(0.8, 0.8, 0.8, 1.0),
)
```

Apply a color transformation in the HSV color model

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| hue | InputFloat | Hue | `0.5` |
| saturation | InputFloat | Saturation | `1.0` |
| value | InputFloat | Value | `1.0` |
| factor | InputFloat | Factor. Renamed from `Fac`; `i.fac` still resolves to it. | `1.0` |
| color | InputColor | Color | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.HueSaturationValue.i) |  |
| [`name`](#nodebpy.nodes.shader.color.HueSaturationValue.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.color.HueSaturationValue.node) |  |
| [`o`](#nodebpy.nodes.shader.color.HueSaturationValue.o) |  |
| [`tree`](#nodebpy.nodes.shader.color.HueSaturationValue.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.color.HueSaturationValue.props) | Set the properties every node has and return the node, so it can |

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
| `i.hue` | `FloatSocket` | Hue |
| `i.saturation` | `FloatSocket` | Saturation |
| `i.value` | `FloatSocket` | Value |
| `i.factor` | `FloatSocket` | Factor. Renamed from `Fac`; `i.fac` still resolves to it. |
| `i.color` | `ColorSocket` | Color |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### InvertColor

``` python
InvertColor(factor=1.0, color=(0.0, 0.0, 0.0, 1.0))
```

Invert a color, producing a negative

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| factor | InputFloat | Factor. Renamed from `Fac`; `i.fac` still resolves to it. | `1.0` |
| color | InputColor | Color | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.InvertColor.i) |  |
| [`name`](#nodebpy.nodes.shader.color.InvertColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.color.InvertColor.node) |  |
| [`o`](#nodebpy.nodes.shader.color.InvertColor.o) |  |
| [`tree`](#nodebpy.nodes.shader.color.InvertColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.color.InvertColor.props) | Set the properties every node has and return the node, so it can |

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

### LightFalloff

``` python
LightFalloff(strength=100.0, smooth=0.0)
```

Manipulate how light intensity decreases over distance. Typically used for non-physically-based effects; in reality light always falls off quadratically

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| strength | InputFloat | Strength    | `100.0` |
| smooth   | InputFloat | Smooth      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.LightFalloff.i) |  |
| [`name`](#nodebpy.nodes.shader.color.LightFalloff.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.color.LightFalloff.node) |  |
| [`o`](#nodebpy.nodes.shader.color.LightFalloff.o) |  |
| [`tree`](#nodebpy.nodes.shader.color.LightFalloff.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.color.LightFalloff.props) | Set the properties every node has and return the node, so it can |

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

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.strength` | `FloatSocket` | Strength    |
| `i.smooth`   | `FloatSocket` | Smooth      |

**Outputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `o.quadratic` | `FloatSocket` | Quadratic   |
| `o.linear`    | `FloatSocket` | Linear      |
| `o.constant`  | `FloatSocket` | Constant    |
