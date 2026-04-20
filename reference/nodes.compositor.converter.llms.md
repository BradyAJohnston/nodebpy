# nodes.compositor.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [AlphaConvert](#nodebpy.nodes.compositor.converter.AlphaConvert) | Convert to and from premultiplied (associated) alpha |
| [CombineColor](#nodebpy.nodes.compositor.converter.CombineColor) | Combine an image from its composite color channels |
| [ConvertColorspace](#nodebpy.nodes.compositor.converter.ConvertColorspace) | Convert between color spaces |
| [ConvertToDisplay](#nodebpy.nodes.compositor.converter.ConvertToDisplay) | Convert from scene linear to display color space, with a view transform and look for tone mapping |
| [IDMask](#nodebpy.nodes.compositor.converter.IDMask) | Create a matte from an object or material index pass |
| [Levels](#nodebpy.nodes.compositor.converter.Levels) | Compute average and standard deviation of pixel values |
| [Mix](#nodebpy.nodes.compositor.converter.Mix) | Mix values by a factor |
| [RGBToBw](#nodebpy.nodes.compositor.converter.RGBToBw) | Convert RGB input into grayscale using luminance |
| [RelativeToPixel](#nodebpy.nodes.compositor.converter.RelativeToPixel) | Converts values that are relative to the image size to be in terms of pixels |
| [SeparateColor](#nodebpy.nodes.compositor.converter.SeparateColor) | Split an image into its composite color channels |
| [SetAlpha](#nodebpy.nodes.compositor.converter.SetAlpha) | Add an alpha channel to an image |
| [Split](#nodebpy.nodes.compositor.converter.Split) | Combine two images for side-by-side display. Typically used in combination with a Viewer node |
| [Switch](#nodebpy.nodes.compositor.converter.Switch) | Switch between two images using a checkbox |
| [SwitchView](#nodebpy.nodes.compositor.converter.SwitchView) | Combine the views (left and right) into a single stereo 3D output |

### AlphaConvert

``` python
AlphaConvert(image=None, type='To Premultiplied')
```

Convert to and from premultiplied (associated) alpha

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['To Premultiplied', 'To Straight'\] | Type | `'To Premultiplied'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.AlphaConvert.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.AlphaConvert.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.AlphaConvert.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.AlphaConvert.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.AlphaConvert.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.AlphaConvert.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.AlphaConvert.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.AlphaConvert.type) |  |

#### Methods

| Name | Description |
|----|----|
| [to_premultiplied](#nodebpy.nodes.compositor.converter.AlphaConvert.to_premultiplied) | Create Alpha Convert node with type ‘To Premultiplied’. |
| [to_straight](#nodebpy.nodes.compositor.converter.AlphaConvert.to_straight) | Create Alpha Convert node with type ‘To Straight’. |

##### to_premultiplied

``` python
to_premultiplied(image=None)
```

Create Alpha Convert node with type ‘To Premultiplied’.

##### to_straight

``` python
to_straight(image=None)
```

Create Alpha Convert node with type ‘To Straight’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### CombineColor

``` python
CombineColor(
    red=0.0,
    green=0.0,
    blue=0.0,
    alpha=1.0,
    *,
    mode='RGB',
    ycc_mode='ITUBT709',
)
```

Combine an image from its composite color channels

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| red   | InputFloat | Red         | `0.0`   |
| green | InputFloat | Green       | `0.0`   |
| blue  | InputFloat | Blue        | `0.0`   |
| alpha | InputFloat | Alpha       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.CombineColor.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.CombineColor.inputs) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.CombineColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.CombineColor.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.CombineColor.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.CombineColor.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.CombineColor.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.CombineColor.type) |  |
| [`ycc_mode`](#nodebpy.nodes.compositor.converter.CombineColor.ycc_mode) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.compositor.converter.CombineColor.hsl) | Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.compositor.converter.CombineColor.hsv) | Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [rgb](#nodebpy.nodes.compositor.converter.CombineColor.rgb) | Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |
| [ycbcr](#nodebpy.nodes.compositor.converter.CombineColor.ycbcr) | Create Combine Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing |
| [yuv](#nodebpy.nodes.compositor.converter.CombineColor.yuv) | Create Combine Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing |

##### hsl

``` python
hsl(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.red`   | `FloatSocket` | Red         |
| `i.green` | `FloatSocket` | Green       |
| `i.blue`  | `FloatSocket` | Blue        |
| `i.alpha` | `FloatSocket` | Alpha       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### ConvertColorspace

``` python
ConvertColorspace(
    image=None,
    *,
    from_color_space='scene_linear',
    to_color_space='scene_linear',
)
```

Convert between color spaces

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`from_color_space`](#nodebpy.nodes.compositor.converter.ConvertColorspace.from_color_space) |  |
| [`i`](#nodebpy.nodes.compositor.converter.ConvertColorspace.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.ConvertColorspace.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ConvertColorspace.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.ConvertColorspace.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ConvertColorspace.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.ConvertColorspace.outputs) |  |
| [`to_color_space`](#nodebpy.nodes.compositor.converter.ConvertColorspace.to_color_space) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ConvertColorspace.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.ConvertColorspace.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### ConvertToDisplay

``` python
ConvertToDisplay(image=None, invert=False)
```

Convert from scene linear to display color space, with a view transform and look for tone mapping

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| image  | InputColor   | Image       | `None`  |
| invert | InputBoolean | Invert      | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.type) |  |

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.image`  | `ColorSocket`   | Image       |
| `i.invert` | `BooleanSocket` | Invert      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### IDMask

``` python
IDMask(id_value=1.0, index=0, anti_alias=False)
```

Create a matte from an object or material index pass

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| id_value   | InputFloat   | ID value    | `1.0`   |
| index      | InputInteger | Index       | `0`     |
| anti_alias | InputBoolean | Anti-Alias  | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.IDMask.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.IDMask.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.IDMask.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.IDMask.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.IDMask.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.IDMask.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.IDMask.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.IDMask.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.id_value`   | `FloatSocket`   | ID value    |
| `i.index`      | `IntegerSocket` | Index       |
| `i.anti_alias` | `BooleanSocket` | Anti-Alias  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.alpha` | `FloatSocket` | Alpha       |

### Levels

``` python
Levels(image=None, channel='Combined')
```

Compute average and standard deviation of pixel values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| channel | InputMenu \| Literal\['Combined', 'Red', 'Green', 'Blue', 'Luminance'\] | Channel | `'Combined'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Levels.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.Levels.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Levels.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.Levels.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Levels.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Levels.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Levels.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.Levels.type) |  |

**Inputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.image`   | `ColorSocket` | Image       |
| `i.channel` | `MenuSocket`  | Channel     |

**Outputs**

| Attribute              | Type          | Description        |
|------------------------|---------------|--------------------|
| `o.mean`               | `FloatSocket` | Mean               |
| `o.standard_deviation` | `FloatSocket` | Standard Deviation |

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
| [`blend_type`](#nodebpy.nodes.compositor.converter.Mix.blend_type) |  |
| [`clamp_factor`](#nodebpy.nodes.compositor.converter.Mix.clamp_factor) |  |
| [`clamp_result`](#nodebpy.nodes.compositor.converter.Mix.clamp_result) |  |
| [`data_type`](#nodebpy.nodes.compositor.converter.Mix.data_type) |  |
| [`factor_mode`](#nodebpy.nodes.compositor.converter.Mix.factor_mode) |  |
| [`i`](#nodebpy.nodes.compositor.converter.Mix.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.Mix.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Mix.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.Mix.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Mix.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Mix.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Mix.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.Mix.type) |  |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.compositor.converter.Mix.color) | Create Mix with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.Mix.float) | Create Mix with operation ‘Float’. |
| [vector](#nodebpy.nodes.compositor.converter.Mix.vector) | Create Mix with operation ‘Vector’. |

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

### RGBToBw

``` python
RGBToBw(image=None)
```

Convert RGB input into grayscale using luminance

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.RGBToBw.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.RGBToBw.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RGBToBw.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.RGBToBw.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RGBToBw.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.RGBToBw.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RGBToBw.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.RGBToBw.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.val`   | `FloatSocket` | Val         |

### RelativeToPixel

``` python
RelativeToPixel(
    vector_value=None,
    float_value=0.0,
    image=None,
    *,
    data_type='FLOAT',
    reference_dimension='X',
)
```

Converts values that are relative to the image size to be in terms of pixels

#### Parameters

| Name         | Type        | Description | Default |
|--------------|-------------|-------------|---------|
| vector_value | InputVector | Value       | `None`  |
| float_value  | InputFloat  | Value       | `0.0`   |
| image        | InputColor  | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.RelativeToPixel.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.RelativeToPixel.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.RelativeToPixel.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RelativeToPixel.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.RelativeToPixel.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RelativeToPixel.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.RelativeToPixel.outputs) |  |
| [`reference_dimension`](#nodebpy.nodes.compositor.converter.RelativeToPixel.reference_dimension) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RelativeToPixel.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.RelativeToPixel.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.compositor.converter.RelativeToPixel.float) | Create Relative To Pixel with operation ‘Float’. Float value |
| [vector](#nodebpy.nodes.compositor.converter.RelativeToPixel.vector) | Create Relative To Pixel with operation ‘Vector’. Vector value |

##### float

``` python
float(float_value=0.0, image=None)
```

Create Relative To Pixel with operation ‘Float’. Float value

##### vector

``` python
vector(vector_value=None, image=None)
```

Create Relative To Pixel with operation ‘Vector’. Vector value

**Inputs**

| Attribute        | Type           | Description |
|------------------|----------------|-------------|
| `i.vector_value` | `VectorSocket` | Value       |
| `i.float_value`  | `FloatSocket`  | Value       |
| `i.image`        | `ColorSocket`  | Image       |

**Outputs**

| Attribute        | Type           | Description |
|------------------|----------------|-------------|
| `o.float_value`  | `FloatSocket`  | Value       |
| `o.vector_value` | `VectorSocket` | Value       |

### SeparateColor

``` python
SeparateColor(image=None, *, mode='RGB', ycc_mode='ITUBT709')
```

Split an image into its composite color channels

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SeparateColor.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.SeparateColor.inputs) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SeparateColor.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SeparateColor.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SeparateColor.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SeparateColor.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.SeparateColor.type) |  |
| [`ycc_mode`](#nodebpy.nodes.compositor.converter.SeparateColor.ycc_mode) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.compositor.converter.SeparateColor.hsl) | Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.compositor.converter.SeparateColor.hsv) | Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [rgb](#nodebpy.nodes.compositor.converter.SeparateColor.rgb) | Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |
| [ycbcr](#nodebpy.nodes.compositor.converter.SeparateColor.ycbcr) | Create Separate Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing |
| [yuv](#nodebpy.nodes.compositor.converter.SeparateColor.yuv) | Create Separate Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing |

##### hsl

``` python
hsl(image=None)
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(image=None)
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(image=None)
```

Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(image=None)
```

Create Separate Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(image=None)
```

Create Separate Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.red`   | `FloatSocket` | Red         |
| `o.green` | `FloatSocket` | Green       |
| `o.blue`  | `FloatSocket` | Blue        |
| `o.alpha` | `FloatSocket` | Alpha       |

### SetAlpha

``` python
SetAlpha(image=None, alpha=1.0, type='Apply Mask')
```

Add an alpha channel to an image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| alpha | InputFloat | Alpha | `1.0` |
| type | InputMenu \| Literal\['Apply Mask', 'Replace Alpha'\] | Type | `'Apply Mask'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SetAlpha.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.SetAlpha.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SetAlpha.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.SetAlpha.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SetAlpha.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SetAlpha.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SetAlpha.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.SetAlpha.type) |  |

#### Methods

| Name | Description |
|----|----|
| [apply_mask](#nodebpy.nodes.compositor.converter.SetAlpha.apply_mask) | Create Set Alpha node with type ‘Apply Mask’. |
| [replace_alpha](#nodebpy.nodes.compositor.converter.SetAlpha.replace_alpha) | Create Set Alpha node with type ‘Replace Alpha’. |

##### apply_mask

``` python
apply_mask(image=None, alpha=1.0)
```

Create Set Alpha node with type ‘Apply Mask’.

##### replace_alpha

``` python
replace_alpha(image=None, alpha=1.0)
```

Create Set Alpha node with type ‘Replace Alpha’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.alpha` | `FloatSocket` | Alpha       |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Split

``` python
Split(position=None, rotation=0.7854, image=None, image_001=None)
```

Combine two images for side-by-side display. Typically used in combination with a Viewer node

#### Parameters

| Name      | Type        | Description | Default  |
|-----------|-------------|-------------|----------|
| position  | InputVector | Position    | `None`   |
| rotation  | InputFloat  | Rotation    | `0.7854` |
| image     | InputColor  | Image       | `None`   |
| image_001 | InputColor  | Image       | `None`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Split.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.Split.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Split.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.Split.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Split.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Split.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Split.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.Split.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.position`  | `VectorSocket` | Position    |
| `i.rotation`  | `FloatSocket`  | Rotation    |
| `i.image`     | `ColorSocket`  | Image       |
| `i.image_001` | `ColorSocket`  | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Switch

``` python
Switch(switch=False, off=None, on=None)
```

Switch between two images using a checkbox

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| switch | InputBoolean | Switch      | `False` |
| off    | InputColor   | Off         | `None`  |
| on     | InputColor   | On          | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Switch.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.Switch.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Switch.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.Switch.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Switch.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Switch.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Switch.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.Switch.type) |  |

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.switch` | `BooleanSocket` | Switch      |
| `i.off`    | `ColorSocket`   | Off         |
| `i.on`     | `ColorSocket`   | On          |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### SwitchView

``` python
SwitchView(left=None, right=None)
```

Combine the views (left and right) into a single stereo 3D output

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| left  | InputColor | left        | `None`  |
| right | InputColor | right       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SwitchView.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.converter.SwitchView.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SwitchView.name) |  |
| [`node`](#nodebpy.nodes.compositor.converter.SwitchView.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SwitchView.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SwitchView.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SwitchView.tree) |  |
| [`type`](#nodebpy.nodes.compositor.converter.SwitchView.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.left`  | `ColorSocket` | left        |
| `i.right` | `ColorSocket` | right       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
