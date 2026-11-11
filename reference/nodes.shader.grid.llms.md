# nodes.shader.grid

`grid`

## Classes

| Name | Description |
|----|----|
| [PrincipledVolume](#nodebpy.nodes.shader.grid.PrincipledVolume) | Combine all volume shading components into a single easy to use node |
| [VolumeAbsorption](#nodebpy.nodes.shader.grid.VolumeAbsorption) | Absorb light as it passes through the volume |
| [VolumeCoefficients](#nodebpy.nodes.shader.grid.VolumeCoefficients) | Model all three physical processes in a volume, represented by their coefficients |
| [VolumeInfo](#nodebpy.nodes.shader.grid.VolumeInfo) | Read volume data attributes from volume grids |
| [VolumeScatter](#nodebpy.nodes.shader.grid.VolumeScatter) | Scatter light as it passes through the volume, often used to add fog to a scene |

### PrincipledVolume

``` python
PrincipledVolume(
    color=(0.5, 0.5, 0.5, 1.0),
    color_attribute='',
    density=1.0,
    density_attribute='density',
    anisotropy=0.0,
    absorption_color=(0.0, 0.0, 0.0, 1.0),
    emission_strength=0.0,
    emission_color=(1.0, 1.0, 1.0, 1.0),
    blackbody_intensity=0.0,
    blackbody_tint=(1.0, 1.0, 1.0, 1.0),
    temperature=1000.0,
    temperature_attribute='temperature',
)
```

Combine all volume shading components into a single easy to use node

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| color | InputColor | Color | `(0.5, 0.5, 0.5, 1.0)` |
| color_attribute | InputString | Color Attribute | `''` |
| density | InputFloat | Density | `1.0` |
| density_attribute | InputString | Density Attribute | `'density'` |
| anisotropy | InputFloat | Anisotropy | `0.0` |
| absorption_color | InputColor | Absorption Color | `(0.0, 0.0, 0.0, 1.0)` |
| emission_strength | InputFloat | Emission Strength | `0.0` |
| emission_color | InputColor | Emission Color | `(1.0, 1.0, 1.0, 1.0)` |
| blackbody_intensity | InputFloat | Blackbody Intensity | `0.0` |
| blackbody_tint | InputColor | Blackbody Tint | `(1.0, 1.0, 1.0, 1.0)` |
| temperature | InputFloat | Temperature | `1000.0` |
| temperature_attribute | InputString | Temperature Attribute | `'temperature'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.PrincipledVolume.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.PrincipledVolume.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.grid.PrincipledVolume.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.PrincipledVolume.o) |  |
| [`tree`](#nodebpy.nodes.shader.grid.PrincipledVolume.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.grid.PrincipledVolume.props) | Set the properties every node has and return the node, so it can |

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

| Attribute                 | Type           | Description           |
|---------------------------|----------------|-----------------------|
| `i.color`                 | `ColorSocket`  | Color                 |
| `i.color_attribute`       | `StringSocket` | Color Attribute       |
| `i.density`               | `FloatSocket`  | Density               |
| `i.density_attribute`     | `StringSocket` | Density Attribute     |
| `i.anisotropy`            | `FloatSocket`  | Anisotropy            |
| `i.absorption_color`      | `ColorSocket`  | Absorption Color      |
| `i.emission_strength`     | `FloatSocket`  | Emission Strength     |
| `i.emission_color`        | `ColorSocket`  | Emission Color        |
| `i.blackbody_intensity`   | `FloatSocket`  | Blackbody Intensity   |
| `i.blackbody_tint`        | `ColorSocket`  | Blackbody Tint        |
| `i.temperature`           | `FloatSocket`  | Temperature           |
| `i.temperature_attribute` | `StringSocket` | Temperature Attribute |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeAbsorption

``` python
VolumeAbsorption(color=(0.8, 0.8, 0.8, 1.0), density=1.0)
```

Absorb light as it passes through the volume

#### Parameters

| Name    | Type       | Description | Default                |
|---------|------------|-------------|------------------------|
| color   | InputColor | Color       | `(0.8, 0.8, 0.8, 1.0)` |
| density | InputFloat | Density     | `1.0`                  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeAbsorption.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeAbsorption.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.grid.VolumeAbsorption.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeAbsorption.o) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeAbsorption.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.grid.VolumeAbsorption.props) | Set the properties every node has and return the node, so it can |

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

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.color`   | `ColorSocket` | Color       |
| `i.density` | `FloatSocket` | Density     |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeCoefficients

``` python
VolumeCoefficients(
    absorption_coefficients=(1.0, 1.0, 1.0),
    scatter_coefficients=(1.0, 1.0, 1.0),
    anisotropy=0.0,
    ior=1.33,
    backscatter=0.1,
    alpha=0.5,
    diameter=20.0,
    emission_coefficients=(0.0, 0.0, 0.0),
    *,
    phase='HENYEY_GREENSTEIN',
)
```

Model all three physical processes in a volume, represented by their coefficients

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| absorption_coefficients | InputVector | Absorption Coefficients | `(1.0, 1.0, 1.0)` |
| scatter_coefficients | InputVector | Scatter Coefficients | `(1.0, 1.0, 1.0)` |
| anisotropy | InputFloat | Anisotropy | `0.0` |
| ior | InputFloat | IOR | `1.33` |
| backscatter | InputFloat | Backscatter | `0.1` |
| alpha | InputFloat | Alpha | `0.5` |
| diameter | InputFloat | Diameter | `20.0` |
| emission_coefficients | InputVector | Emission Coefficients | `(0.0, 0.0, 0.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeCoefficients.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeCoefficients.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.grid.VolumeCoefficients.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeCoefficients.o) |  |
| [`phase`](#nodebpy.nodes.shader.grid.VolumeCoefficients.phase) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeCoefficients.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.grid.VolumeCoefficients.props) | Set the properties every node has and return the node, so it can |

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

| Attribute                   | Type           | Description             |
|-----------------------------|----------------|-------------------------|
| `i.absorption_coefficients` | `VectorSocket` | Absorption Coefficients |
| `i.scatter_coefficients`    | `VectorSocket` | Scatter Coefficients    |
| `i.anisotropy`              | `FloatSocket`  | Anisotropy              |
| `i.ior`                     | `FloatSocket`  | IOR                     |
| `i.backscatter`             | `FloatSocket`  | Backscatter             |
| `i.alpha`                   | `FloatSocket`  | Alpha                   |
| `i.diameter`                | `FloatSocket`  | Diameter                |
| `i.emission_coefficients`   | `VectorSocket` | Emission Coefficients   |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeInfo

``` python
VolumeInfo()
```

Read volume data attributes from volume grids

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.grid.VolumeInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.grid.VolumeInfo.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `o.color`       | `ColorSocket` | Color       |
| `o.density`     | `FloatSocket` | Density     |
| `o.flame`       | `FloatSocket` | Flame       |
| `o.temperature` | `FloatSocket` | Temperature |

### VolumeScatter

``` python
VolumeScatter(
    color=(0.8, 0.8, 0.8, 1.0),
    density=1.0,
    anisotropy=0.0,
    ior=1.33,
    backscatter=0.1,
    alpha=0.5,
    diameter=20.0,
    *,
    phase='HENYEY_GREENSTEIN',
)
```

Scatter light as it passes through the volume, often used to add fog to a scene

#### Parameters

| Name        | Type       | Description | Default                |
|-------------|------------|-------------|------------------------|
| color       | InputColor | Color       | `(0.8, 0.8, 0.8, 1.0)` |
| density     | InputFloat | Density     | `1.0`                  |
| anisotropy  | InputFloat | Anisotropy  | `0.0`                  |
| ior         | InputFloat | IOR         | `1.33`                 |
| backscatter | InputFloat | Backscatter | `0.1`                  |
| alpha       | InputFloat | Alpha       | `0.5`                  |
| diameter    | InputFloat | Diameter    | `20.0`                 |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeScatter.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeScatter.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.grid.VolumeScatter.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeScatter.o) |  |
| [`phase`](#nodebpy.nodes.shader.grid.VolumeScatter.phase) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeScatter.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.grid.VolumeScatter.props) | Set the properties every node has and return the node, so it can |

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

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `i.color`       | `ColorSocket` | Color       |
| `i.density`     | `FloatSocket` | Density     |
| `i.anisotropy`  | `FloatSocket` | Anisotropy  |
| `i.ior`         | `FloatSocket` | IOR         |
| `i.backscatter` | `FloatSocket` | Backscatter |
| `i.alpha`       | `FloatSocket` | Alpha       |
| `i.diameter`    | `FloatSocket` | Diameter    |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |
