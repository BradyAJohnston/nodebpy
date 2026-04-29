# nodes.geometry.texture

`texture`

## Classes

| Name | Description |
|----|----|
| [BrickTexture](#nodebpy.nodes.geometry.texture.BrickTexture) | Generate a procedural texture producing bricks |
| [CheckerTexture](#nodebpy.nodes.geometry.texture.CheckerTexture) | Generate a checkerboard texture |
| [GaborTexture](#nodebpy.nodes.geometry.texture.GaborTexture) | Generate Gabor noise |
| [GradientTexture](#nodebpy.nodes.geometry.texture.GradientTexture) | Generate interpolated color and intensity values based on the input vector |
| [ImageTexture](#nodebpy.nodes.geometry.texture.ImageTexture) | Sample values from an image texture |
| [MagicTexture](#nodebpy.nodes.geometry.texture.MagicTexture) | Generate a psychedelic color texture |
| [NoiseTexture](#nodebpy.nodes.geometry.texture.NoiseTexture) | Generate fractal Perlin noise |
| [VoronoiTexture](#nodebpy.nodes.geometry.texture.VoronoiTexture) | Generate Worley noise based on the distance to random points. Typically used to generate textures such as stones, water, or biological cells |
| [WaveTexture](#nodebpy.nodes.geometry.texture.WaveTexture) | Generate procedural bands or rings with noise |
| [WhiteNoiseTexture](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture) | Calculate a random value or color based on an input seed |

### BrickTexture

``` python
BrickTexture(
    vector=None,
    color1=None,
    color2=None,
    mortar=None,
    scale=5.0,
    mortar_size=0.02,
    mortar_smooth=0.1,
    bias=0.0,
    brick_width=0.5,
    row_height=0.25,
    *,
    offset_frequency=2,
    squash_frequency=2,
    offset=0.5,
    squash=1.0,
)
```

Generate a procedural texture producing bricks

#### Parameters

| Name          | Type        | Description   | Default |
|---------------|-------------|---------------|---------|
| vector        | InputVector | Vector        | `None`  |
| color1        | InputColor  | Color1        | `None`  |
| color2        | InputColor  | Color2        | `None`  |
| mortar        | InputColor  | Mortar        | `None`  |
| scale         | InputFloat  | Scale         | `5.0`   |
| mortar_size   | InputFloat  | Mortar Size   | `0.02`  |
| mortar_smooth | InputFloat  | Mortar Smooth | `0.1`   |
| bias          | InputFloat  | Bias          | `0.0`   |
| brick_width   | InputFloat  | Brick Width   | `0.5`   |
| row_height    | InputFloat  | Row Height    | `0.25`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.texture.BrickTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.BrickTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.BrickTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.BrickTexture.o) |  |
| [`offset`](#nodebpy.nodes.geometry.texture.BrickTexture.offset) |  |
| [`offset_frequency`](#nodebpy.nodes.geometry.texture.BrickTexture.offset_frequency) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.BrickTexture.outputs) |  |
| [`squash`](#nodebpy.nodes.geometry.texture.BrickTexture.squash) |  |
| [`squash_frequency`](#nodebpy.nodes.geometry.texture.BrickTexture.squash_frequency) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.BrickTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.BrickTexture.type) |  |

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.vector`        | `VectorSocket` | Vector        |
| `i.color1`        | `ColorSocket`  | Color1        |
| `i.color2`        | `ColorSocket`  | Color2        |
| `i.mortar`        | `ColorSocket`  | Mortar        |
| `i.scale`         | `FloatSocket`  | Scale         |
| `i.mortar_size`   | `FloatSocket`  | Mortar Size   |
| `i.mortar_smooth` | `FloatSocket`  | Mortar Smooth |
| `i.bias`          | `FloatSocket`  | Bias          |
| `i.brick_width`   | `FloatSocket`  | Brick Width   |
| `i.row_height`    | `FloatSocket`  | Row Height    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.fac`   | `FloatSocket` | Factor      |

### CheckerTexture

``` python
CheckerTexture(vector=None, color1=None, color2=None, scale=5.0)
```

Generate a checkerboard texture

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |
| color1 | InputColor  | Color1      | `None`  |
| color2 | InputColor  | Color2      | `None`  |
| scale  | InputFloat  | Scale       | `5.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.texture.CheckerTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.CheckerTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.CheckerTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.CheckerTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.CheckerTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.CheckerTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.CheckerTexture.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |
| `i.color1` | `ColorSocket`  | Color1      |
| `i.color2` | `ColorSocket`  | Color2      |
| `i.scale`  | `FloatSocket`  | Scale       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.fac`   | `FloatSocket` | Factor      |

### GaborTexture

``` python
GaborTexture(
    vector=None,
    scale=5.0,
    frequency=2.0,
    anisotropy=1.0,
    orientation_2d=0.7854,
    orientation_3d=None,
    *,
    gabor_type='2D',
)
```

Generate Gabor noise

#### Parameters

| Name           | Type        | Description | Default  |
|----------------|-------------|-------------|----------|
| vector         | InputVector | Vector      | `None`   |
| scale          | InputFloat  | Scale       | `5.0`    |
| frequency      | InputFloat  | Frequency   | `2.0`    |
| anisotropy     | InputFloat  | Anisotropy  | `1.0`    |
| orientation_2d | InputFloat  | Orientation | `0.7854` |
| orientation_3d | InputVector | Orientation | `None`   |

#### Attributes

| Name | Description |
|----|----|
| [`gabor_type`](#nodebpy.nodes.geometry.texture.GaborTexture.gabor_type) |  |
| [`i`](#nodebpy.nodes.geometry.texture.GaborTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.GaborTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.GaborTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.GaborTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.GaborTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.GaborTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.GaborTexture.type) |  |

#### Methods

| Name | Description |
|----|----|
| [input_2d](#nodebpy.nodes.geometry.texture.GaborTexture.input_2d) | Create Gabor Texture with operation ‘2D’. Use the 2D vector (X, Y) as input. The Z component is ignored. |
| [input_3d](#nodebpy.nodes.geometry.texture.GaborTexture.input_3d) | Create Gabor Texture with operation ‘3D’. Use the 3D vector (X, Y, Z) as input |

##### input_2d

``` python
input_2d(
    vector=None,
    scale=5.0,
    frequency=2.0,
    anisotropy=1.0,
    orientation_2d=0.7854,
)
```

Create Gabor Texture with operation ‘2D’. Use the 2D vector (X, Y) as input. The Z component is ignored.

##### input_3d

``` python
input_3d(
    vector=None,
    scale=5.0,
    frequency=2.0,
    anisotropy=1.0,
    orientation_3d=None,
)
```

Create Gabor Texture with operation ‘3D’. Use the 3D vector (X, Y, Z) as input

**Inputs**

| Attribute          | Type           | Description |
|--------------------|----------------|-------------|
| `i.vector`         | `VectorSocket` | Vector      |
| `i.scale`          | `FloatSocket`  | Scale       |
| `i.frequency`      | `FloatSocket`  | Frequency   |
| `i.anisotropy`     | `FloatSocket`  | Anisotropy  |
| `i.orientation_2d` | `FloatSocket`  | Orientation |
| `i.orientation_3d` | `VectorSocket` | Orientation |

**Outputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `o.value`     | `FloatSocket` | Value       |
| `o.phase`     | `FloatSocket` | Phase       |
| `o.intensity` | `FloatSocket` | Intensity   |

### GradientTexture

``` python
GradientTexture(vector=None, *, gradient_type='LINEAR')
```

Generate interpolated color and intensity values based on the input vector

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`gradient_type`](#nodebpy.nodes.geometry.texture.GradientTexture.gradient_type) |  |
| [`i`](#nodebpy.nodes.geometry.texture.GradientTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.GradientTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.GradientTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.GradientTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.GradientTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.GradientTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.GradientTexture.type) |  |

#### Methods

| Name | Description |
|----|----|
| [diagonal](#nodebpy.nodes.geometry.texture.GradientTexture.diagonal) | Create Gradient Texture with operation ‘Diagonal’. Create a diagonal progression |
| [easing](#nodebpy.nodes.geometry.texture.GradientTexture.easing) | Create Gradient Texture with operation ‘Easing’. Create a progression easing from one step to the next |
| [linear](#nodebpy.nodes.geometry.texture.GradientTexture.linear) | Create Gradient Texture with operation ‘Linear’. Create a linear progression |
| [quadratic](#nodebpy.nodes.geometry.texture.GradientTexture.quadratic) | Create Gradient Texture with operation ‘Quadratic’. Create a quadratic progression |
| [quadratic_sphere](#nodebpy.nodes.geometry.texture.GradientTexture.quadratic_sphere) | Create Gradient Texture with operation ‘Quadratic Sphere’. Create a quadratic progression in the shape of a sphere |
| [radial](#nodebpy.nodes.geometry.texture.GradientTexture.radial) | Create Gradient Texture with operation ‘Radial’. Create a radial progression |
| [spherical](#nodebpy.nodes.geometry.texture.GradientTexture.spherical) | Create Gradient Texture with operation ‘Spherical’. Create a spherical progression |

##### diagonal

``` python
diagonal(vector=None)
```

Create Gradient Texture with operation ‘Diagonal’. Create a diagonal progression

##### easing

``` python
easing(vector=None)
```

Create Gradient Texture with operation ‘Easing’. Create a progression easing from one step to the next

##### linear

``` python
linear(vector=None)
```

Create Gradient Texture with operation ‘Linear’. Create a linear progression

##### quadratic

``` python
quadratic(vector=None)
```

Create Gradient Texture with operation ‘Quadratic’. Create a quadratic progression

##### quadratic_sphere

``` python
quadratic_sphere(vector=None)
```

Create Gradient Texture with operation ‘Quadratic Sphere’. Create a quadratic progression in the shape of a sphere

##### radial

``` python
radial(vector=None)
```

Create Gradient Texture with operation ‘Radial’. Create a radial progression

##### spherical

``` python
spherical(vector=None)
```

Create Gradient Texture with operation ‘Spherical’. Create a spherical progression

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.fac`   | `FloatSocket` | Factor      |

### ImageTexture

``` python
ImageTexture(
    image=None,
    vector=None,
    frame=0,
    *,
    interpolation='Linear',
    extension='REPEAT',
)
```

Sample values from an image texture

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| image  | InputImage   | Image       | `None`  |
| vector | InputVector  | Vector      | `None`  |
| frame  | InputInteger | Frame       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`extension`](#nodebpy.nodes.geometry.texture.ImageTexture.extension) |  |
| [`i`](#nodebpy.nodes.geometry.texture.ImageTexture.i) |  |
| [`interpolation`](#nodebpy.nodes.geometry.texture.ImageTexture.interpolation) |  |
| [`name`](#nodebpy.nodes.geometry.texture.ImageTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.ImageTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.ImageTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.ImageTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.ImageTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.ImageTexture.type) |  |

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.image`  | `ImageSocket`   | Image       |
| `i.vector` | `VectorSocket`  | Vector      |
| `i.frame`  | `IntegerSocket` | Frame       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.alpha` | `FloatSocket` | Alpha       |

### MagicTexture

``` python
MagicTexture(vector=None, scale=5.0, distortion=1.0, *, turbulence_depth=0)
```

Generate a psychedelic color texture

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| vector     | InputVector | Vector      | `None`  |
| scale      | InputFloat  | Scale       | `5.0`   |
| distortion | InputFloat  | Distortion  | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.texture.MagicTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.MagicTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.MagicTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.MagicTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.MagicTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.MagicTexture.tree) |  |
| [`turbulence_depth`](#nodebpy.nodes.geometry.texture.MagicTexture.turbulence_depth) |  |
| [`type`](#nodebpy.nodes.geometry.texture.MagicTexture.type) |  |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.vector`     | `VectorSocket` | Vector      |
| `i.scale`      | `FloatSocket`  | Scale       |
| `i.distortion` | `FloatSocket`  | Distortion  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.fac`   | `FloatSocket` | Factor      |

### NoiseTexture

``` python
NoiseTexture(
    vector=None,
    w=0.0,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    offset=0.0,
    gain=1.0,
    distortion=0.0,
    *,
    noise_dimensions='3D',
    noise_type='FBM',
    normalize=False,
)
```

Generate fractal Perlin noise

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| vector     | InputVector | Vector      | `None`  |
| w          | InputFloat  | W           | `0.0`   |
| scale      | InputFloat  | Scale       | `5.0`   |
| detail     | InputFloat  | Detail      | `2.0`   |
| roughness  | InputFloat  | Roughness   | `0.5`   |
| lacunarity | InputFloat  | Lacunarity  | `2.0`   |
| offset     | InputFloat  | Offset      | `0.0`   |
| gain       | InputFloat  | Gain        | `1.0`   |
| distortion | InputFloat  | Distortion  | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.texture.NoiseTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.NoiseTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.NoiseTexture.node) |  |
| [`noise_dimensions`](#nodebpy.nodes.geometry.texture.NoiseTexture.noise_dimensions) |  |
| [`noise_type`](#nodebpy.nodes.geometry.texture.NoiseTexture.noise_type) |  |
| [`normalize`](#nodebpy.nodes.geometry.texture.NoiseTexture.normalize) |  |
| [`o`](#nodebpy.nodes.geometry.texture.NoiseTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.NoiseTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.NoiseTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.NoiseTexture.type) |  |

#### Methods

| Name | Description |
|----|----|
| [fbm](#nodebpy.nodes.geometry.texture.NoiseTexture.fbm) | Create Noise Texture with operation ‘fBM’. The standard fractal Perlin noise |
| [hetero_terrain](#nodebpy.nodes.geometry.texture.NoiseTexture.hetero_terrain) | Create Noise Texture with operation ‘Hetero Terrain’. Similar to Hybrid Multifractal creates a heterogeneous terrain, but with the likeness of river channels |
| [hybrid_multifractal](#nodebpy.nodes.geometry.texture.NoiseTexture.hybrid_multifractal) | Create Noise Texture with operation ‘Hybrid Multifractal’. Create peaks and valleys with different roughness values |
| [multifractal](#nodebpy.nodes.geometry.texture.NoiseTexture.multifractal) | Create Noise Texture with operation ‘Multifractal’. More uneven result (varies with location), more similar to a real terrain |
| [ridged_multifractal](#nodebpy.nodes.geometry.texture.NoiseTexture.ridged_multifractal) | Create Noise Texture with operation ‘Ridged Multifractal’. Create sharp peaks |

##### fbm

``` python
fbm(
    vector=None,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    distortion=0.0,
)
```

Create Noise Texture with operation ‘fBM’. The standard fractal Perlin noise

##### hetero_terrain

``` python
hetero_terrain(
    vector=None,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    offset=0.0,
    distortion=0.0,
)
```

Create Noise Texture with operation ‘Hetero Terrain’. Similar to Hybrid Multifractal creates a heterogeneous terrain, but with the likeness of river channels

##### hybrid_multifractal

``` python
hybrid_multifractal(
    vector=None,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    offset=0.0,
    gain=1.0,
    distortion=0.0,
)
```

Create Noise Texture with operation ‘Hybrid Multifractal’. Create peaks and valleys with different roughness values

##### multifractal

``` python
multifractal(
    vector=None,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    distortion=0.0,
)
```

Create Noise Texture with operation ‘Multifractal’. More uneven result (varies with location), more similar to a real terrain

##### ridged_multifractal

``` python
ridged_multifractal(
    vector=None,
    scale=5.0,
    detail=2.0,
    roughness=0.5,
    lacunarity=2.0,
    offset=0.0,
    gain=1.0,
    distortion=0.0,
)
```

Create Noise Texture with operation ‘Ridged Multifractal’. Create sharp peaks

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.vector`     | `VectorSocket` | Vector      |
| `i.w`          | `FloatSocket`  | W           |
| `i.scale`      | `FloatSocket`  | Scale       |
| `i.detail`     | `FloatSocket`  | Detail      |
| `i.roughness`  | `FloatSocket`  | Roughness   |
| `i.lacunarity` | `FloatSocket`  | Lacunarity  |
| `i.offset`     | `FloatSocket`  | Offset      |
| `i.gain`       | `FloatSocket`  | Gain        |
| `i.distortion` | `FloatSocket`  | Distortion  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.fac`   | `FloatSocket` | Factor      |
| `o.color` | `ColorSocket` | Color       |

### VoronoiTexture

``` python
VoronoiTexture(
    vector=None,
    w=0.0,
    scale=5.0,
    detail=0.0,
    roughness=0.5,
    lacunarity=2.0,
    smoothness=1.0,
    exponent=0.5,
    randomness=1.0,
    *,
    voronoi_dimensions='3D',
    distance='EUCLIDEAN',
    feature='F1',
    normalize=False,
)
```

Generate Worley noise based on the distance to random points. Typically used to generate textures such as stones, water, or biological cells

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| vector     | InputVector | Vector      | `None`  |
| w          | InputFloat  | W           | `0.0`   |
| scale      | InputFloat  | Scale       | `5.0`   |
| detail     | InputFloat  | Detail      | `0.0`   |
| roughness  | InputFloat  | Roughness   | `0.5`   |
| lacunarity | InputFloat  | Lacunarity  | `2.0`   |
| smoothness | InputFloat  | Smoothness  | `1.0`   |
| exponent   | InputFloat  | Exponent    | `0.5`   |
| randomness | InputFloat  | Randomness  | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`distance`](#nodebpy.nodes.geometry.texture.VoronoiTexture.distance) |  |
| [`feature`](#nodebpy.nodes.geometry.texture.VoronoiTexture.feature) |  |
| [`i`](#nodebpy.nodes.geometry.texture.VoronoiTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.VoronoiTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.VoronoiTexture.node) |  |
| [`normalize`](#nodebpy.nodes.geometry.texture.VoronoiTexture.normalize) |  |
| [`o`](#nodebpy.nodes.geometry.texture.VoronoiTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.VoronoiTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.VoronoiTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.VoronoiTexture.type) |  |
| [`voronoi_dimensions`](#nodebpy.nodes.geometry.texture.VoronoiTexture.voronoi_dimensions) |  |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.vector`     | `VectorSocket` | Vector      |
| `i.w`          | `FloatSocket`  | W           |
| `i.scale`      | `FloatSocket`  | Scale       |
| `i.detail`     | `FloatSocket`  | Detail      |
| `i.roughness`  | `FloatSocket`  | Roughness   |
| `i.lacunarity` | `FloatSocket`  | Lacunarity  |
| `i.smoothness` | `FloatSocket`  | Smoothness  |
| `i.exponent`   | `FloatSocket`  | Exponent    |
| `i.randomness` | `FloatSocket`  | Randomness  |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.distance` | `FloatSocket`  | Distance    |
| `o.color`    | `ColorSocket`  | Color       |
| `o.position` | `VectorSocket` | Position    |
| `o.w`        | `FloatSocket`  | W           |
| `o.radius`   | `FloatSocket`  | Radius      |

### WaveTexture

``` python
WaveTexture(
    vector=None,
    scale=5.0,
    distortion=0.0,
    detail=2.0,
    detail_scale=1.0,
    detail_roughness=0.5,
    phase_offset=0.0,
    *,
    wave_type='BANDS',
    bands_direction='X',
    rings_direction='X',
    wave_profile='SIN',
)
```

Generate procedural bands or rings with noise

#### Parameters

| Name             | Type        | Description      | Default |
|------------------|-------------|------------------|---------|
| vector           | InputVector | Vector           | `None`  |
| scale            | InputFloat  | Scale            | `5.0`   |
| distortion       | InputFloat  | Distortion       | `0.0`   |
| detail           | InputFloat  | Detail           | `2.0`   |
| detail_scale     | InputFloat  | Detail Scale     | `1.0`   |
| detail_roughness | InputFloat  | Detail Roughness | `0.5`   |
| phase_offset     | InputFloat  | Phase Offset     | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`bands_direction`](#nodebpy.nodes.geometry.texture.WaveTexture.bands_direction) |  |
| [`i`](#nodebpy.nodes.geometry.texture.WaveTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.WaveTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.WaveTexture.node) |  |
| [`o`](#nodebpy.nodes.geometry.texture.WaveTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.WaveTexture.outputs) |  |
| [`rings_direction`](#nodebpy.nodes.geometry.texture.WaveTexture.rings_direction) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.WaveTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.WaveTexture.type) |  |
| [`wave_profile`](#nodebpy.nodes.geometry.texture.WaveTexture.wave_profile) |  |
| [`wave_type`](#nodebpy.nodes.geometry.texture.WaveTexture.wave_type) |  |

#### Methods

| Name | Description |
|----|----|
| [bands](#nodebpy.nodes.geometry.texture.WaveTexture.bands) | Create Wave Texture with operation ‘Bands’. Use standard wave texture in bands |
| [rings](#nodebpy.nodes.geometry.texture.WaveTexture.rings) | Create Wave Texture with operation ‘Rings’. Use wave texture in rings |

##### bands

``` python
bands(
    vector=None,
    scale=5.0,
    distortion=0.0,
    detail=2.0,
    detail_scale=1.0,
    detail_roughness=0.5,
    phase_offset=0.0,
)
```

Create Wave Texture with operation ‘Bands’. Use standard wave texture in bands

##### rings

``` python
rings(
    vector=None,
    scale=5.0,
    distortion=0.0,
    detail=2.0,
    detail_scale=1.0,
    detail_roughness=0.5,
    phase_offset=0.0,
)
```

Create Wave Texture with operation ‘Rings’. Use wave texture in rings

**Inputs**

| Attribute            | Type           | Description      |
|----------------------|----------------|------------------|
| `i.vector`           | `VectorSocket` | Vector           |
| `i.scale`            | `FloatSocket`  | Scale            |
| `i.distortion`       | `FloatSocket`  | Distortion       |
| `i.detail`           | `FloatSocket`  | Detail           |
| `i.detail_scale`     | `FloatSocket`  | Detail Scale     |
| `i.detail_roughness` | `FloatSocket`  | Detail Roughness |
| `i.phase_offset`     | `FloatSocket`  | Phase Offset     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.fac`   | `FloatSocket` | Factor      |

### WhiteNoiseTexture

``` python
WhiteNoiseTexture(vector=None, w=0.0, *, noise_dimensions='3D')
```

Calculate a random value or color based on an input seed

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |
| w      | InputFloat  | W           | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.i) |  |
| [`name`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.name) |  |
| [`node`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.node) |  |
| [`noise_dimensions`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.noise_dimensions) |  |
| [`o`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.tree) |  |
| [`type`](#nodebpy.nodes.geometry.texture.WhiteNoiseTexture.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |
| `i.w`      | `FloatSocket`  | W           |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |
| `o.color` | `ColorSocket` | Color       |
