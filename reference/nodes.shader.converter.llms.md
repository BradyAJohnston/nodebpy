# nodes.shader.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [CombineColor](#nodebpy.nodes.shader.converter.CombineColor) | Create a color from individual components using multiple models |
| [ImplicitConversion](#nodebpy.nodes.shader.converter.ImplicitConversion) | Implicitly convert the input value to a fixed socket type |
| [IndexSwitch](#nodebpy.nodes.shader.converter.IndexSwitch) | Choose between an arbitrary number of values with an index |
| [Mix](#nodebpy.nodes.shader.converter.Mix) | Mix values by a factor |
| [RGBToBW](#nodebpy.nodes.shader.converter.RGBToBW) | Convert a color’s luminance to a grayscale value |
| [SeparateColor](#nodebpy.nodes.shader.converter.SeparateColor) | Split a color into its individual components using multiple models |
| [ShaderToRGB](#nodebpy.nodes.shader.converter.ShaderToRGB) | Convert rendering effect (such as light and shadow) to color. Typically used for non-photorealistic rendering, to apply additional effects on the output of BSDFs. |
| [Switch](#nodebpy.nodes.shader.converter.Switch) | Switch between two inputs |
| [Wavelength](#nodebpy.nodes.shader.converter.Wavelength) | Convert a wavelength value to an RGB value |

### CombineColor

``` python
CombineColor(red=0.0, green=0.0, blue=0.0, *, mode='RGB')
```

Create a color from individual components using multiple models

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| red   | InputFloat | Red         | `0.0`   |
| green | InputFloat | Green       | `0.0`   |
| blue  | InputFloat | Blue        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.CombineColor.i) |  |
| [`mode`](#nodebpy.nodes.shader.converter.CombineColor.mode) |  |
| [`name`](#nodebpy.nodes.shader.converter.CombineColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.CombineColor.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.CombineColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.shader.converter.CombineColor.hsl) | Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.shader.converter.CombineColor.hsv) | Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [props](#nodebpy.nodes.shader.converter.CombineColor.props) | Set the properties every node has and return the node, so it can |
| [rgb](#nodebpy.nodes.shader.converter.CombineColor.rgb) | Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |

##### hsl

``` python
hsl(red=0.0, green=0.0, blue=0.0)
```

Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(red=0.0, green=0.0, blue=0.0)
```

Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

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

##### rgb

``` python
rgb(red=0.0, green=0.0, blue=0.0)
```

Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.red`   | `FloatSocket` | Red         |
| `i.green` | `FloatSocket` | Green       |
| `i.blue`  | `FloatSocket` | Blue        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### ImplicitConversion

``` python
ImplicitConversion(value=(0.0, 0.0, 0.0, 1.0), *, data_type='RGBA')
```

Implicitly convert the input value to a fixed socket type

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| value | InputColor | Value       | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.shader.converter.ImplicitConversion.data_type) |  |
| [`i`](#nodebpy.nodes.shader.converter.ImplicitConversion.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.ImplicitConversion.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.ImplicitConversion.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.ImplicitConversion.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.ImplicitConversion.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.shader.converter.ImplicitConversion.boolean) | Create Implicit Conversion with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.shader.converter.ImplicitConversion.bundle) | Create Implicit Conversion with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.shader.converter.ImplicitConversion.closure) | Create Implicit Conversion with operation ‘Closure’. |
| [color](#nodebpy.nodes.shader.converter.ImplicitConversion.color) | Create Implicit Conversion with operation ‘Color’. |
| [float](#nodebpy.nodes.shader.converter.ImplicitConversion.float) | Create Implicit Conversion with operation ‘Float’. |
| [integer](#nodebpy.nodes.shader.converter.ImplicitConversion.integer) | Create Implicit Conversion with operation ‘Integer’. |
| [menu](#nodebpy.nodes.shader.converter.ImplicitConversion.menu) | Create Implicit Conversion with operation ‘Menu’. |
| [props](#nodebpy.nodes.shader.converter.ImplicitConversion.props) | Set the properties every node has and return the node, so it can |
| [shader](#nodebpy.nodes.shader.converter.ImplicitConversion.shader) | Create Implicit Conversion with operation ‘Shader’. |
| [string](#nodebpy.nodes.shader.converter.ImplicitConversion.string) | Create Implicit Conversion with operation ‘String’. |
| [vector](#nodebpy.nodes.shader.converter.ImplicitConversion.vector) | Create Implicit Conversion with operation ‘Vector’. |

##### boolean

``` python
boolean(value=False)
```

Create Implicit Conversion with operation ‘Boolean’.

##### bundle

``` python
bundle(value=None)
```

Create Implicit Conversion with operation ‘Bundle’.

##### closure

``` python
closure(value=None)
```

Create Implicit Conversion with operation ‘Closure’.

##### color

``` python
color(value=(0.0, 0.0, 0.0, 1.0))
```

Create Implicit Conversion with operation ‘Color’.

##### float

``` python
float(value=0.0)
```

Create Implicit Conversion with operation ‘Float’.

##### integer

``` python
integer(value=0)
```

Create Implicit Conversion with operation ‘Integer’.

##### menu

``` python
menu(value=None)
```

Create Implicit Conversion with operation ‘Menu’.

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

##### shader

``` python
shader(value=None)
```

Create Implicit Conversion with operation ‘Shader’.

##### string

``` python
string(value='')
```

Create Implicit Conversion with operation ‘String’.

##### vector

``` python
vector(value=(0.0, 0.0, 0.0))
```

Create Implicit Conversion with operation ‘Vector’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.value` | `ColorSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `ColorSocket` | Value       |

### IndexSwitch

``` python
IndexSwitch(
    index=0,
    input_0=(0.8, 0.8, 0.8, 1.0),
    input_1=(0.8, 0.8, 0.8, 1.0),
    input_socket=None,
    *,
    data_type='RGBA',
)
```

Choose between an arbitrary number of values with an index

#### Parameters

| Name         | Type          | Description | Default                |
|--------------|---------------|-------------|------------------------|
| index        | InputInteger  | Index       | `0`                    |
| input_0      | InputColor    | 0           | `(0.8, 0.8, 0.8, 1.0)` |
| input_1      | InputColor    | 1           | `(0.8, 0.8, 0.8, 1.0)` |
| input_socket | InputLinkable |             | `None`                 |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.shader.converter.IndexSwitch.data_type) |  |
| [`i`](#nodebpy.nodes.shader.converter.IndexSwitch.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.IndexSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.IndexSwitch.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.IndexSwitch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.shader.converter.IndexSwitch.boolean) | Create Index Switch with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.shader.converter.IndexSwitch.bundle) | Create Index Switch with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.shader.converter.IndexSwitch.closure) | Create Index Switch with operation ‘Closure’. |
| [color](#nodebpy.nodes.shader.converter.IndexSwitch.color) | Create Index Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.shader.converter.IndexSwitch.float) | Create Index Switch with operation ‘Float’. |
| [integer](#nodebpy.nodes.shader.converter.IndexSwitch.integer) | Create Index Switch with operation ‘Integer’. |
| [menu](#nodebpy.nodes.shader.converter.IndexSwitch.menu) | Create Index Switch with operation ‘Menu’. |
| [props](#nodebpy.nodes.shader.converter.IndexSwitch.props) | Set the properties every node has and return the node, so it can |
| [shader](#nodebpy.nodes.shader.converter.IndexSwitch.shader) | Create Index Switch with operation ‘Shader’. |
| [string](#nodebpy.nodes.shader.converter.IndexSwitch.string) | Create Index Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.shader.converter.IndexSwitch.vector) | Create Index Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(index=0, input_0=False, input_1=False, input_socket=None)
```

Create Index Switch with operation ‘Boolean’.

##### bundle

``` python
bundle(index=0, input_0=None, input_1=None, input_socket=None)
```

Create Index Switch with operation ‘Bundle’.

##### closure

``` python
closure(index=0, input_0=None, input_1=None, input_socket=None)
```

Create Index Switch with operation ‘Closure’.

##### color

``` python
color(
    index=0,
    input_0=(0.8, 0.8, 0.8, 1.0),
    input_1=(0.8, 0.8, 0.8, 1.0),
    input_socket=None,
)
```

Create Index Switch with operation ‘Color’.

##### float

``` python
float(index=0, input_0=0.0, input_1=0.0, input_socket=None)
```

Create Index Switch with operation ‘Float’.

##### integer

``` python
integer(index=0, input_0=0, input_1=0, input_socket=None)
```

Create Index Switch with operation ‘Integer’.

##### menu

``` python
menu(index=0, input_0=None, input_1=None, input_socket=None)
```

Create Index Switch with operation ‘Menu’.

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

##### shader

``` python
shader(index=0, input_0=None, input_1=None, input_socket=None)
```

Create Index Switch with operation ‘Shader’.

##### string

``` python
string(index=0, input_0='', input_1='', input_socket=None)
```

Create Index Switch with operation ‘String’.

##### vector

``` python
vector(
    index=0,
    input_0=(0.0, 0.0, 0.0),
    input_1=(0.0, 0.0, 0.0),
    input_socket=None,
)
```

Create Index Switch with operation ‘Vector’.

**Inputs**

| Attribute        | Type            | Description |
|------------------|-----------------|-------------|
| `i.index`        | `IntegerSocket` | Index       |
| `i.input_0`      | `ColorSocket`   | 0           |
| `i.input_1`      | `ColorSocket`   | 1           |
| `i.input_socket` | `Socket`        |             |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `ColorSocket` | Output      |

### Mix

``` python
Mix(
    factor_float=1.0,
    factor_vector=(0.5, 0.5, 0.5),
    a_float=0.0,
    b_float=0.0,
    a_vector=(0.0, 0.0, 0.0),
    b_vector=(0.0, 0.0, 0.0),
    a_color=(0.5, 0.5, 0.5, 1.0),
    b_color=(0.5, 0.5, 0.5, 1.0),
    a_rotation=(0.0, 0.0, 0.0),
    b_rotation=(0.0, 0.0, 0.0),
    *,
    data_type='FLOAT',
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=True,
    clamp_result=False,
)
```

Mix values by a factor

#### Parameters

| Name          | Type          | Description | Default                |
|---------------|---------------|-------------|------------------------|
| factor_float  | InputFloat    | Factor      | `1.0`                  |
| factor_vector | InputVector   | Factor      | `(0.5, 0.5, 0.5)`      |
| a_float       | InputFloat    | A           | `0.0`                  |
| b_float       | InputFloat    | B           | `0.0`                  |
| a_vector      | InputVector   | A           | `(0.0, 0.0, 0.0)`      |
| b_vector      | InputVector   | B           | `(0.0, 0.0, 0.0)`      |
| a_color       | InputColor    | A           | `(0.5, 0.5, 0.5, 1.0)` |
| b_color       | InputColor    | B           | `(0.5, 0.5, 0.5, 1.0)` |
| a_rotation    | InputRotation | A           | `(0.0, 0.0, 0.0)`      |
| b_rotation    | InputRotation | B           | `(0.0, 0.0, 0.0)`      |

#### Attributes

| Name | Description |
|----|----|
| [`blend_type`](#nodebpy.nodes.shader.converter.Mix.blend_type) |  |
| [`clamp_factor`](#nodebpy.nodes.shader.converter.Mix.clamp_factor) |  |
| [`clamp_result`](#nodebpy.nodes.shader.converter.Mix.clamp_result) |  |
| [`data_type`](#nodebpy.nodes.shader.converter.Mix.data_type) |  |
| [`factor_mode`](#nodebpy.nodes.shader.converter.Mix.factor_mode) |  |
| [`i`](#nodebpy.nodes.shader.converter.Mix.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.Mix.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.Mix.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.Mix.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.Mix.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.shader.converter.Mix.color) | Create Mix with operation ‘Color’. |
| [float](#nodebpy.nodes.shader.converter.Mix.float) | Create Mix with operation ‘Float’. |
| [props](#nodebpy.nodes.shader.converter.Mix.props) | Set the properties every node has and return the node, so it can |
| [vector](#nodebpy.nodes.shader.converter.Mix.vector) | Create Mix with operation ‘Vector’. |

##### color

``` python
color(
    factor=1.0,
    a=(0.5, 0.5, 0.5, 1.0),
    b=(0.5, 0.5, 0.5, 1.0),
    *,
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=True,
    clamp_result=False,
)
```

Create Mix with operation ‘Color’.

##### float

``` python
float(
    factor=1.0,
    a=0.0,
    b=0.0,
    *,
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=True,
    clamp_result=False,
)
```

Create Mix with operation ‘Float’.

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

##### vector

``` python
vector(
    factor=1.0,
    a=(0.0, 0.0, 0.0),
    b=(0.0, 0.0, 0.0),
    *,
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=True,
    clamp_result=False,
)
```

Create Mix with operation ‘Vector’.

**Inputs**

| Attribute         | Type             | Description |
|-------------------|------------------|-------------|
| `i.factor_float`  | `FloatSocket`    | Factor      |
| `i.factor_vector` | `VectorSocket`   | Factor      |
| `i.a_float`       | `FloatSocket`    | A           |
| `i.b_float`       | `FloatSocket`    | B           |
| `i.a_vector`      | `VectorSocket`   | A           |
| `i.b_vector`      | `VectorSocket`   | B           |
| `i.a_color`       | `ColorSocket`    | A           |
| `i.b_color`       | `ColorSocket`    | B           |
| `i.a_rotation`    | `RotationSocket` | A           |
| `i.b_rotation`    | `RotationSocket` | B           |

**Outputs**

| Attribute           | Type             | Description |
|---------------------|------------------|-------------|
| `o.result_float`    | `FloatSocket`    | Result      |
| `o.result_vector`   | `VectorSocket`   | Result      |
| `o.result_color`    | `ColorSocket`    | Result      |
| `o.result_rotation` | `RotationSocket` | Result      |

### RGBToBW

``` python
RGBToBW(color=(0.5, 0.5, 0.5, 1.0))
```

Convert a color’s luminance to a grayscale value

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| color | InputColor | Color       | `(0.5, 0.5, 0.5, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.RGBToBW.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.RGBToBW.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.RGBToBW.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.RGBToBW.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.RGBToBW.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.converter.RGBToBW.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.val`   | `FloatSocket` | Val         |

### SeparateColor

``` python
SeparateColor(color=(0.8, 0.8, 0.8, 1.0), *, mode='RGB')
```

Split a color into its individual components using multiple models

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| color | InputColor | Color       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.SeparateColor.i) |  |
| [`mode`](#nodebpy.nodes.shader.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.shader.converter.SeparateColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.SeparateColor.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.SeparateColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.shader.converter.SeparateColor.hsl) | Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.shader.converter.SeparateColor.hsv) | Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [props](#nodebpy.nodes.shader.converter.SeparateColor.props) | Set the properties every node has and return the node, so it can |
| [rgb](#nodebpy.nodes.shader.converter.SeparateColor.rgb) | Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |

##### hsl

``` python
hsl(color=(0.8, 0.8, 0.8, 1.0))
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(color=(0.8, 0.8, 0.8, 1.0))
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

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

##### rgb

``` python
rgb(color=(0.8, 0.8, 0.8, 1.0))
```

Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.color` | `ColorSocket` | Color       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.red`   | `FloatSocket` | Red         |
| `o.green` | `FloatSocket` | Green       |
| `o.blue`  | `FloatSocket` | Blue        |

### ShaderToRGB

``` python
ShaderToRGB(shader=None)
```

    Convert rendering effect (such as light and shadow) to color. Typically used for non-photorealistic rendering, to apply additional effects on the output of BSDFs.

Note: only supported in EEVEE

#### Parameters

    shader : InputShader
        Shader

#### Inputs

    i.shader : ShaderSocket
        Shader

#### Outputs

    o.color : ColorSocket
        Color
    o.alpha : FloatSocket
        Alpha

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.ShaderToRGB.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.ShaderToRGB.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.ShaderToRGB.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.ShaderToRGB.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.ShaderToRGB.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.converter.ShaderToRGB.props) | Set the properties every node has and return the node, so it can |

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

### Switch

``` python
Switch(switch=False, false=None, true=None, *, input_type=None)
```

Switch between two inputs

#### Parameters

| Name       | Type                 | Description | Default |
|------------|----------------------|-------------|---------|
| switch     | InputBoolean         | switch      | `False` |
| false      | InputAny             | false       | `None`  |
| true       | InputAny             | true        | `None`  |
| input_type | \_SwitchType \| None | input_type  | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.Switch.i) |  |
| [`input_type`](#nodebpy.nodes.shader.converter.Switch.input_type) |  |
| [`name`](#nodebpy.nodes.shader.converter.Switch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.Switch.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.Switch.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.Switch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.shader.converter.Switch.boolean) | Create Switch with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.shader.converter.Switch.bundle) | Create Switch with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.shader.converter.Switch.closure) | Create Switch with operation ‘Closure’. |
| [color](#nodebpy.nodes.shader.converter.Switch.color) | Create Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.shader.converter.Switch.float) | Create Switch with operation ‘Float’. |
| [integer](#nodebpy.nodes.shader.converter.Switch.integer) | Create Switch with operation ‘Integer’. |
| [menu](#nodebpy.nodes.shader.converter.Switch.menu) | Create Switch with operation ‘Menu’. |
| [props](#nodebpy.nodes.shader.converter.Switch.props) | Set the properties every node has and return the node, so it can |
| [shader](#nodebpy.nodes.shader.converter.Switch.shader) | Create Switch with operation ‘Shader’. |
| [string](#nodebpy.nodes.shader.converter.Switch.string) | Create Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.shader.converter.Switch.vector) | Create Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(switch=False, false=False, true=False)
```

Create Switch with operation ‘Boolean’.

##### bundle

``` python
bundle(switch=False, false=None, true=None)
```

Create Switch with operation ‘Bundle’.

##### closure

``` python
closure(switch=False, false=None, true=None)
```

Create Switch with operation ‘Closure’.

##### color

``` python
color(switch=False, false=(0.8, 0.8, 0.8, 1.0), true=(0.8, 0.8, 0.8, 1.0))
```

Create Switch with operation ‘Color’.

##### float

``` python
float(switch=False, false=0.0, true=0.0)
```

Create Switch with operation ‘Float’.

##### integer

``` python
integer(switch=False, false=0, true=0)
```

Create Switch with operation ‘Integer’.

##### menu

``` python
menu(switch=False, false=None, true=None)
```

Create Switch with operation ‘Menu’.

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

##### shader

``` python
shader(switch=False, false=None, true=None)
```

Create Switch with operation ‘Shader’.

##### string

``` python
string(switch=False, false='', true='')
```

Create Switch with operation ‘String’.

##### vector

``` python
vector(switch=False, false=(0.0, 0.0, 0.0), true=(0.0, 0.0, 0.0))
```

Create Switch with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.switch` | `BooleanSocket` | Switch      |
| `i.false`  | `ColorSocket`   | False       |
| `i.true`   | `ColorSocket`   | True        |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `ColorSocket` | Output      |

### Wavelength

``` python
Wavelength(wavelength=500.0)
```

Convert a wavelength value to an RGB value

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| wavelength | InputFloat | Wavelength  | `500.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.Wavelength.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.Wavelength.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.converter.Wavelength.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.Wavelength.o) |  |
| [`tree`](#nodebpy.nodes.shader.converter.Wavelength.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.converter.Wavelength.props) | Set the properties every node has and return the node, so it can |

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

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.wavelength` | `FloatSocket` | Wavelength  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
