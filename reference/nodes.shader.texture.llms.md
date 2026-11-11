# nodes.shader.texture

`texture`

## Classes

| Name | Description |
|----|----|
| [EnvironmentTexture](#nodebpy.nodes.shader.texture.EnvironmentTexture) | Sample an image file as an environment texture. Typically used to light the scene with the background node |
| [IESTexture](#nodebpy.nodes.shader.texture.IESTexture) | Match real world lights with IES files, which store the directional intensity distribution of light sources |
| [ImageTexture](#nodebpy.nodes.shader.texture.ImageTexture) | Sample an image file as a texture |
| [SkyTexture](#nodebpy.nodes.shader.texture.SkyTexture) | Generate a procedural sky texture |

### EnvironmentTexture

``` python
EnvironmentTexture(
    vector=None,
    *,
    image=None,
    projection='EQUIRECTANGULAR',
    interpolation='Linear',
)
```

Sample an image file as an environment texture. Typically used to light the scene with the background node

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.texture.EnvironmentTexture.i) |  |
| [`image`](#nodebpy.nodes.shader.texture.EnvironmentTexture.image) |  |
| [`interpolation`](#nodebpy.nodes.shader.texture.EnvironmentTexture.interpolation) |  |
| [`name`](#nodebpy.nodes.shader.texture.EnvironmentTexture.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.texture.EnvironmentTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.EnvironmentTexture.o) |  |
| [`projection`](#nodebpy.nodes.shader.texture.EnvironmentTexture.projection) |  |
| [`tree`](#nodebpy.nodes.shader.texture.EnvironmentTexture.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.texture.EnvironmentTexture.props) | Set the properties every node has and return the node, so it can |

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

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### IESTexture

``` python
IESTexture(vector=None, strength=1.0, *, ies=None, filepath='', mode='INTERNAL')
```

Match real world lights with IES files, which store the directional intensity distribution of light sources

#### Parameters

| Name     | Type        | Description | Default |
|----------|-------------|-------------|---------|
| vector   | InputVector | Vector      | `None`  |
| strength | InputFloat  | Strength    | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`filepath`](#nodebpy.nodes.shader.texture.IESTexture.filepath) |  |
| [`i`](#nodebpy.nodes.shader.texture.IESTexture.i) |  |
| [`ies`](#nodebpy.nodes.shader.texture.IESTexture.ies) |  |
| [`mode`](#nodebpy.nodes.shader.texture.IESTexture.mode) |  |
| [`name`](#nodebpy.nodes.shader.texture.IESTexture.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.texture.IESTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.IESTexture.o) |  |
| [`tree`](#nodebpy.nodes.shader.texture.IESTexture.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [external](#nodebpy.nodes.shader.texture.IESTexture.external) | Create IES Texture with operation ‘External’. Use external .ies file |
| [internal](#nodebpy.nodes.shader.texture.IESTexture.internal) | Create IES Texture with operation ‘Internal’. Use internal text data-block |
| [props](#nodebpy.nodes.shader.texture.IESTexture.props) | Set the properties every node has and return the node, so it can |

##### external

``` python
external(vector=None, strength=1.0, *, filepath='')
```

Create IES Texture with operation ‘External’. Use external .ies file

##### internal

``` python
internal(vector=None, strength=1.0, *, ies=None)
```

Create IES Texture with operation ‘Internal’. Use internal text data-block

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

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.vector`   | `VectorSocket` | Vector      |
| `i.strength` | `FloatSocket`  | Strength    |

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `o.factor` | `FloatSocket` | Factor. Renamed from `Fac`; `o.fac` still resolves to it. |

### ImageTexture

``` python
ImageTexture(
    vector=None,
    *,
    image=None,
    projection='FLAT',
    interpolation='Linear',
    projection_blend=0.0,
    extension='REPEAT',
)
```

Sample an image file as a texture

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`extension`](#nodebpy.nodes.shader.texture.ImageTexture.extension) |  |
| [`i`](#nodebpy.nodes.shader.texture.ImageTexture.i) |  |
| [`image`](#nodebpy.nodes.shader.texture.ImageTexture.image) |  |
| [`interpolation`](#nodebpy.nodes.shader.texture.ImageTexture.interpolation) |  |
| [`name`](#nodebpy.nodes.shader.texture.ImageTexture.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.texture.ImageTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.ImageTexture.o) |  |
| [`projection`](#nodebpy.nodes.shader.texture.ImageTexture.projection) |  |
| [`projection_blend`](#nodebpy.nodes.shader.texture.ImageTexture.projection_blend) |  |
| [`tree`](#nodebpy.nodes.shader.texture.ImageTexture.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.texture.ImageTexture.props) | Set the properties every node has and return the node, so it can |

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

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.alpha` | `FloatSocket` | Alpha       |

### SkyTexture

``` python
SkyTexture(
    vector=None,
    *,
    sky_type='MULTIPLE_SCATTERING',
    sun_disc=True,
    sun_size=0.0095120445,
    sun_intensity=1.0,
    sun_elevation=math.pi / 12,
    sun_rotation=0.0,
    altitude=100.0,
    air_density=1.0,
    aerosol_density=1.0,
    ozone_density=1.0,
    sun_direction=(0.0, 0.0, 1.0),
    turbidity=2.2,
    ground_albedo=0.3,
)
```

Generate a procedural sky texture

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`aerosol_density`](#nodebpy.nodes.shader.texture.SkyTexture.aerosol_density) |  |
| [`air_density`](#nodebpy.nodes.shader.texture.SkyTexture.air_density) |  |
| [`altitude`](#nodebpy.nodes.shader.texture.SkyTexture.altitude) |  |
| [`ground_albedo`](#nodebpy.nodes.shader.texture.SkyTexture.ground_albedo) |  |
| [`i`](#nodebpy.nodes.shader.texture.SkyTexture.i) |  |
| [`name`](#nodebpy.nodes.shader.texture.SkyTexture.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.texture.SkyTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.SkyTexture.o) |  |
| [`ozone_density`](#nodebpy.nodes.shader.texture.SkyTexture.ozone_density) |  |
| [`sky_type`](#nodebpy.nodes.shader.texture.SkyTexture.sky_type) |  |
| [`sun_direction`](#nodebpy.nodes.shader.texture.SkyTexture.sun_direction) |  |
| [`sun_disc`](#nodebpy.nodes.shader.texture.SkyTexture.sun_disc) |  |
| [`sun_elevation`](#nodebpy.nodes.shader.texture.SkyTexture.sun_elevation) |  |
| [`sun_intensity`](#nodebpy.nodes.shader.texture.SkyTexture.sun_intensity) |  |
| [`sun_rotation`](#nodebpy.nodes.shader.texture.SkyTexture.sun_rotation) |  |
| [`sun_size`](#nodebpy.nodes.shader.texture.SkyTexture.sun_size) |  |
| [`tree`](#nodebpy.nodes.shader.texture.SkyTexture.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`turbidity`](#nodebpy.nodes.shader.texture.SkyTexture.turbidity) |  |

#### Methods

| Name | Description |
|----|----|
| [hosek_wilkie](#nodebpy.nodes.shader.texture.SkyTexture.hosek_wilkie) | Create Sky Texture with operation ‘Hosek / Wilkie’. Hosek / Wilkie 2012 (Legacy) |
| [multiple_scattering](#nodebpy.nodes.shader.texture.SkyTexture.multiple_scattering) | Create Sky Texture with operation ‘Multiple Scattering’. Multiple scattering sky model (more accurate) |
| [preetham](#nodebpy.nodes.shader.texture.SkyTexture.preetham) | Create Sky Texture with operation ‘Preetham’. Preetham 1999 (Legacy) |
| [props](#nodebpy.nodes.shader.texture.SkyTexture.props) | Set the properties every node has and return the node, so it can |
| [single_scattering](#nodebpy.nodes.shader.texture.SkyTexture.single_scattering) | Create Sky Texture with operation ‘Single Scattering’. Single scattering sky model |

##### hosek_wilkie

``` python
hosek_wilkie(
    vector=None,
    *,
    sun_direction=(0.0, 0.0, 1.0),
    turbidity=2.2,
    ground_albedo=0.3,
)
```

Create Sky Texture with operation ‘Hosek / Wilkie’. Hosek / Wilkie 2012 (Legacy)

##### multiple_scattering

``` python
multiple_scattering(
    sun_disc=True,
    sun_size=0.0095120445,
    sun_intensity=1.0,
    sun_elevation=math.pi / 12,
    sun_rotation=0.0,
    altitude=100.0,
    air_density=1.0,
    aerosol_density=1.0,
    ozone_density=1.0,
)
```

Create Sky Texture with operation ‘Multiple Scattering’. Multiple scattering sky model (more accurate)

##### preetham

``` python
preetham(vector=None, *, sun_direction=(0.0, 0.0, 1.0), turbidity=2.2)
```

Create Sky Texture with operation ‘Preetham’. Preetham 1999 (Legacy)

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

##### single_scattering

``` python
single_scattering(
    sun_disc=True,
    sun_size=0.0095120445,
    sun_intensity=1.0,
    sun_elevation=math.pi / 12,
    sun_rotation=0.0,
    altitude=100.0,
    air_density=1.0,
    aerosol_density=1.0,
    ozone_density=1.0,
)
```

Create Sky Texture with operation ‘Single Scattering’. Single scattering sky model

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
