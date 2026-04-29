# nodes.shader.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [CombineColor](#nodebpy.nodes.shader.converter.CombineColor) | Create a color from individual components using multiple models |
| [Mix](#nodebpy.nodes.shader.converter.Mix) | Mix values by a factor |
| [RGBToBW](#nodebpy.nodes.shader.converter.RGBToBW) | Convert a color’s luminance to a grayscale value |
| [SeparateColor](#nodebpy.nodes.shader.converter.SeparateColor) | Split a color into its individual components using multiple models |
| [ShaderToRGB](#nodebpy.nodes.shader.converter.ShaderToRGB) | Convert rendering effect (such as light and shadow) to color. Typically used for non-photorealistic rendering, to apply additional effects on the output of BSDFs. |
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
| [`name`](#nodebpy.nodes.shader.converter.CombineColor.name) |  |
| [`node`](#nodebpy.nodes.shader.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.CombineColor.o) |  |
| [`outputs`](#nodebpy.nodes.shader.converter.CombineColor.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.converter.CombineColor.tree) |  |
| [`type`](#nodebpy.nodes.shader.converter.CombineColor.type) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.shader.converter.CombineColor.hsl) | Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.shader.converter.CombineColor.hsv) | Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
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

### Mix

``` python
Mix(
    factor_float=0.5,
    factor_vector=None,
    a_float=0.0,
    b_float=0.0,
    a_vector=None,
    b_vector=None,
    a_color=None,
    b_color=None,
    a_rotation=None,
    b_rotation=None,
    *,
    data_type='FLOAT',
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=False,
    clamp_result=False,
)
```

Mix values by a factor

#### Parameters

| Name          | Type          | Description | Default |
|---------------|---------------|-------------|---------|
| factor_float  | InputFloat    | Factor      | `0.5`   |
| factor_vector | InputVector   | Factor      | `None`  |
| a_float       | InputFloat    | A           | `0.0`   |
| b_float       | InputFloat    | B           | `0.0`   |
| a_vector      | InputVector   | A           | `None`  |
| b_vector      | InputVector   | B           | `None`  |
| a_color       | InputColor    | A           | `None`  |
| b_color       | InputColor    | B           | `None`  |
| a_rotation    | InputRotation | A           | `None`  |
| b_rotation    | InputRotation | B           | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`blend_type`](#nodebpy.nodes.shader.converter.Mix.blend_type) |  |
| [`clamp_factor`](#nodebpy.nodes.shader.converter.Mix.clamp_factor) |  |
| [`clamp_result`](#nodebpy.nodes.shader.converter.Mix.clamp_result) |  |
| [`data_type`](#nodebpy.nodes.shader.converter.Mix.data_type) |  |
| [`factor_mode`](#nodebpy.nodes.shader.converter.Mix.factor_mode) |  |
| [`i`](#nodebpy.nodes.shader.converter.Mix.i) |  |
| [`name`](#nodebpy.nodes.shader.converter.Mix.name) |  |
| [`node`](#nodebpy.nodes.shader.converter.Mix.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.Mix.o) |  |
| [`outputs`](#nodebpy.nodes.shader.converter.Mix.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.converter.Mix.tree) |  |
| [`type`](#nodebpy.nodes.shader.converter.Mix.type) |  |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.shader.converter.Mix.color) | Create Mix with operation ‘Color’. |
| [float](#nodebpy.nodes.shader.converter.Mix.float) | Create Mix with operation ‘Float’. |
| [vector](#nodebpy.nodes.shader.converter.Mix.vector) | Create Mix with operation ‘Vector’. |

##### color

``` python
color(factor=0.5, a_color=None, b_color=None)
```

Create Mix with operation ‘Color’.

##### float

``` python
float(factor=0.5, a=0.0, b=0.0)
```

Create Mix with operation ‘Float’.

##### vector

``` python
vector(factor=0.5, a=None, b=None)
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
RGBToBW(color=None)
```

Convert a color’s luminance to a grayscale value

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| color | InputColor | Color       | `None`  |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.converter.RGBToBW.i)             |             |
| [`name`](#nodebpy.nodes.shader.converter.RGBToBW.name)       |             |
| [`node`](#nodebpy.nodes.shader.converter.RGBToBW.node)       |             |
| [`o`](#nodebpy.nodes.shader.converter.RGBToBW.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.converter.RGBToBW.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.converter.RGBToBW.tree)       |             |
| [`type`](#nodebpy.nodes.shader.converter.RGBToBW.type)       |             |

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
SeparateColor(color=None, *, mode='RGB')
```

Split a color into its individual components using multiple models

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| color | InputColor | Color       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.converter.SeparateColor.i) |  |
| [`mode`](#nodebpy.nodes.shader.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.shader.converter.SeparateColor.name) |  |
| [`node`](#nodebpy.nodes.shader.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.SeparateColor.o) |  |
| [`outputs`](#nodebpy.nodes.shader.converter.SeparateColor.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.converter.SeparateColor.tree) |  |
| [`type`](#nodebpy.nodes.shader.converter.SeparateColor.type) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.shader.converter.SeparateColor.hsl) | Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.shader.converter.SeparateColor.hsv) | Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [rgb](#nodebpy.nodes.shader.converter.SeparateColor.rgb) | Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |

##### hsl

``` python
hsl(color=None)
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(color=None)
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(color=None)
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
| [`name`](#nodebpy.nodes.shader.converter.ShaderToRGB.name) |  |
| [`node`](#nodebpy.nodes.shader.converter.ShaderToRGB.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.ShaderToRGB.o) |  |
| [`outputs`](#nodebpy.nodes.shader.converter.ShaderToRGB.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.converter.ShaderToRGB.tree) |  |
| [`type`](#nodebpy.nodes.shader.converter.ShaderToRGB.type) |  |

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
| [`name`](#nodebpy.nodes.shader.converter.Wavelength.name) |  |
| [`node`](#nodebpy.nodes.shader.converter.Wavelength.node) |  |
| [`o`](#nodebpy.nodes.shader.converter.Wavelength.o) |  |
| [`outputs`](#nodebpy.nodes.shader.converter.Wavelength.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.converter.Wavelength.tree) |  |
| [`type`](#nodebpy.nodes.shader.converter.Wavelength.type) |  |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.wavelength` | `FloatSocket` | Wavelength  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
