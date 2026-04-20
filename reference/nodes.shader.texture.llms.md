# nodes.shader.texture

`texture`

## Classes

| Name | Description |
|----|----|
| [EnvironmentTexture](#nodebpy.nodes.shader.texture.EnvironmentTexture) | Sample an image file as an environment texture. Typically used to light the scene with the background node |
| [IesTexture](#nodebpy.nodes.shader.texture.IesTexture) | Match real world lights with IES files, which store the directional intensity distribution of light sources |
| [ImageTexture](#nodebpy.nodes.shader.texture.ImageTexture) | Sample an image file as a texture |
| [SkyTexture](#nodebpy.nodes.shader.texture.SkyTexture) | Generate a procedural sky texture |

### EnvironmentTexture

``` python
EnvironmentTexture(
    vector=None,
    *,
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
| [`inputs`](#nodebpy.nodes.shader.texture.EnvironmentTexture.inputs) |  |
| [`interpolation`](#nodebpy.nodes.shader.texture.EnvironmentTexture.interpolation) |  |
| [`name`](#nodebpy.nodes.shader.texture.EnvironmentTexture.name) |  |
| [`node`](#nodebpy.nodes.shader.texture.EnvironmentTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.EnvironmentTexture.o) |  |
| [`outputs`](#nodebpy.nodes.shader.texture.EnvironmentTexture.outputs) |  |
| [`projection`](#nodebpy.nodes.shader.texture.EnvironmentTexture.projection) |  |
| [`tree`](#nodebpy.nodes.shader.texture.EnvironmentTexture.tree) |  |
| [`type`](#nodebpy.nodes.shader.texture.EnvironmentTexture.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### IesTexture

``` python
IesTexture(vector=None, strength=1.0, *, filepath='', mode='INTERNAL')
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
| [`filepath`](#nodebpy.nodes.shader.texture.IesTexture.filepath) |  |
| [`i`](#nodebpy.nodes.shader.texture.IesTexture.i) |  |
| [`inputs`](#nodebpy.nodes.shader.texture.IesTexture.inputs) |  |
| [`mode`](#nodebpy.nodes.shader.texture.IesTexture.mode) |  |
| [`name`](#nodebpy.nodes.shader.texture.IesTexture.name) |  |
| [`node`](#nodebpy.nodes.shader.texture.IesTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.IesTexture.o) |  |
| [`outputs`](#nodebpy.nodes.shader.texture.IesTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.texture.IesTexture.tree) |  |
| [`type`](#nodebpy.nodes.shader.texture.IesTexture.type) |  |

#### Methods

| Name | Description |
|----|----|
| [external](#nodebpy.nodes.shader.texture.IesTexture.external) | Create IES Texture with operation ‘External’. Use external .ies file |
| [internal](#nodebpy.nodes.shader.texture.IesTexture.internal) | Create IES Texture with operation ‘Internal’. Use internal text data-block |

##### external

``` python
external(vector=None, strength=1.0)
```

Create IES Texture with operation ‘External’. Use external .ies file

##### internal

``` python
internal(vector=None, strength=1.0)
```

Create IES Texture with operation ‘Internal’. Use internal text data-block

**Inputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.vector`   | `VectorSocket` | Vector      |
| `i.strength` | `FloatSocket`  | Strength    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.fac`   | `FloatSocket` | Factor      |

### ImageTexture

``` python
ImageTexture(
    vector=None,
    *,
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
| [`inputs`](#nodebpy.nodes.shader.texture.ImageTexture.inputs) |  |
| [`interpolation`](#nodebpy.nodes.shader.texture.ImageTexture.interpolation) |  |
| [`name`](#nodebpy.nodes.shader.texture.ImageTexture.name) |  |
| [`node`](#nodebpy.nodes.shader.texture.ImageTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.ImageTexture.o) |  |
| [`outputs`](#nodebpy.nodes.shader.texture.ImageTexture.outputs) |  |
| [`projection`](#nodebpy.nodes.shader.texture.ImageTexture.projection) |  |
| [`projection_blend`](#nodebpy.nodes.shader.texture.ImageTexture.projection_blend) |  |
| [`tree`](#nodebpy.nodes.shader.texture.ImageTexture.tree) |  |
| [`type`](#nodebpy.nodes.shader.texture.ImageTexture.type) |  |

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
    sun_size=0.01,
    sun_intensity=1.0,
    sun_elevation=0.262,
    sun_rotation=0.0,
    altitude=100.0,
    air_density=1.0,
    aerosol_density=1.0,
    ozone_density=1.0,
    sun_direction=(0.0, 0.0, 1.0),
    turbidity=0.0,
    ground_albedo=0.0,
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
| [`inputs`](#nodebpy.nodes.shader.texture.SkyTexture.inputs) |  |
| [`name`](#nodebpy.nodes.shader.texture.SkyTexture.name) |  |
| [`node`](#nodebpy.nodes.shader.texture.SkyTexture.node) |  |
| [`o`](#nodebpy.nodes.shader.texture.SkyTexture.o) |  |
| [`outputs`](#nodebpy.nodes.shader.texture.SkyTexture.outputs) |  |
| [`ozone_density`](#nodebpy.nodes.shader.texture.SkyTexture.ozone_density) |  |
| [`sky_type`](#nodebpy.nodes.shader.texture.SkyTexture.sky_type) |  |
| [`sun_direction`](#nodebpy.nodes.shader.texture.SkyTexture.sun_direction) |  |
| [`sun_disc`](#nodebpy.nodes.shader.texture.SkyTexture.sun_disc) |  |
| [`sun_elevation`](#nodebpy.nodes.shader.texture.SkyTexture.sun_elevation) |  |
| [`sun_intensity`](#nodebpy.nodes.shader.texture.SkyTexture.sun_intensity) |  |
| [`sun_rotation`](#nodebpy.nodes.shader.texture.SkyTexture.sun_rotation) |  |
| [`sun_size`](#nodebpy.nodes.shader.texture.SkyTexture.sun_size) |  |
| [`tree`](#nodebpy.nodes.shader.texture.SkyTexture.tree) |  |
| [`turbidity`](#nodebpy.nodes.shader.texture.SkyTexture.turbidity) |  |
| [`type`](#nodebpy.nodes.shader.texture.SkyTexture.type) |  |

#### Methods

| Name | Description |
|----|----|
| [hosek_wilkie](#nodebpy.nodes.shader.texture.SkyTexture.hosek_wilkie) | Create Sky Texture with operation ‘Hosek / Wilkie’. Hosek / Wilkie 2012 (Legacy) |
| [multiple_scattering](#nodebpy.nodes.shader.texture.SkyTexture.multiple_scattering) | Create Sky Texture with operation ‘Multiple Scattering’. Multiple scattering sky model (more accurate) |
| [preetham](#nodebpy.nodes.shader.texture.SkyTexture.preetham) | Create Sky Texture with operation ‘Preetham’. Preetham 1999 (Legacy) |
| [single_scattering](#nodebpy.nodes.shader.texture.SkyTexture.single_scattering) | Create Sky Texture with operation ‘Single Scattering’. Single scattering sky model |

##### hosek_wilkie

``` python
hosek_wilkie(vector=None)
```

Create Sky Texture with operation ‘Hosek / Wilkie’. Hosek / Wilkie 2012 (Legacy)

##### multiple_scattering

``` python
multiple_scattering()
```

Create Sky Texture with operation ‘Multiple Scattering’. Multiple scattering sky model (more accurate)

##### preetham

``` python
preetham(vector=None)
```

Create Sky Texture with operation ‘Preetham’. Preetham 1999 (Legacy)

##### single_scattering

``` python
single_scattering()
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
