# nodes.compositor.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [AlphaConvert](#nodebpy.nodes.compositor.converter.AlphaConvert) | Convert to and from premultiplied (associated) alpha |
| [CombineColor](#nodebpy.nodes.compositor.converter.CombineColor) | Combine an image from its composite color channels |
| [ConvertToDisplay](#nodebpy.nodes.compositor.converter.ConvertToDisplay) | Convert from scene linear to display color space, with a view transform and look for tone mapping |
| [IDMask](#nodebpy.nodes.compositor.converter.IDMask) | Create a matte from an object or material index pass |
| [ImplicitConversion](#nodebpy.nodes.compositor.converter.ImplicitConversion) | Implicitly convert the input value to a fixed socket type |
| [Levels](#nodebpy.nodes.compositor.converter.Levels) | Compute average and standard deviation of pixel values |
| [RGBToBW](#nodebpy.nodes.compositor.converter.RGBToBW) | Convert RGB input into grayscale using luminance |
| [RelativeToPixel](#nodebpy.nodes.compositor.converter.RelativeToPixel) | Converts values that are relative to the image size to be in terms of pixels |
| [SeparateColor](#nodebpy.nodes.compositor.converter.SeparateColor) | Split an image into its composite color channels |
| [SetAlpha](#nodebpy.nodes.compositor.converter.SetAlpha) | Add an alpha channel to an image |
| [Split](#nodebpy.nodes.compositor.converter.Split) | Combine two images for side-by-side display. Typically used in combination with a Viewer node |
| [Switch](#nodebpy.nodes.compositor.converter.Switch) | Switch between two inputs |
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
| [`name`](#nodebpy.nodes.compositor.converter.AlphaConvert.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.AlphaConvert.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.AlphaConvert.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.AlphaConvert.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`mode`](#nodebpy.nodes.compositor.converter.CombineColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.CombineColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.CombineColor.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.CombineColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
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
hsl(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
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

### ConvertToDisplay

``` python
ConvertToDisplay(image=(1.0, 1.0, 1.0, 1.0), invert=False)
```

Convert from scene linear to display color space, with a view transform and look for tone mapping

#### Parameters

| Name   | Type         | Description | Default                |
|--------|--------------|-------------|------------------------|
| image  | InputColor   | Image       | `(1.0, 1.0, 1.0, 1.0)` |
| invert | InputBoolean | Invert      | `False`                |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`name`](#nodebpy.nodes.compositor.converter.IDMask.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.IDMask.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.IDMask.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.IDMask.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`data_type`](#nodebpy.nodes.compositor.converter.ImplicitConversion.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.ImplicitConversion.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ImplicitConversion.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ImplicitConversion.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ImplicitConversion.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ImplicitConversion.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.converter.ImplicitConversion.boolean) | Create Implicit Conversion with operation ‘Boolean’. |
| [color](#nodebpy.nodes.compositor.converter.ImplicitConversion.color) | Create Implicit Conversion with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.ImplicitConversion.float) | Create Implicit Conversion with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.ImplicitConversion.font) | Create Implicit Conversion with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.converter.ImplicitConversion.integer) | Create Implicit Conversion with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.ImplicitConversion.integer_vector) | Create Implicit Conversion with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.converter.ImplicitConversion.matrix) | Create Implicit Conversion with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.ImplicitConversion.menu) | Create Implicit Conversion with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.ImplicitConversion.object) | Create Implicit Conversion with operation ‘Object’. |
| [rotation](#nodebpy.nodes.compositor.converter.ImplicitConversion.rotation) | Create Implicit Conversion with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.converter.ImplicitConversion.string) | Create Implicit Conversion with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.ImplicitConversion.vector) | Create Implicit Conversion with operation ‘Vector’. |

##### boolean

``` python
boolean(value=False)
```

Create Implicit Conversion with operation ‘Boolean’.

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

##### font

``` python
font(value=None)
```

Create Implicit Conversion with operation ‘Font’.

##### integer

``` python
integer(value=0)
```

Create Implicit Conversion with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(value=(0, 0, 0))
```

Create Implicit Conversion with operation ‘Integer Vector’.

##### matrix

``` python
matrix(value=None)
```

Create Implicit Conversion with operation ‘Matrix’.

##### menu

``` python
menu(value=None)
```

Create Implicit Conversion with operation ‘Menu’.

##### object

``` python
object(value=None)
```

Create Implicit Conversion with operation ‘Object’.

##### rotation

``` python
rotation(value=(0.0, 0.0, 0.0))
```

Create Implicit Conversion with operation ‘Rotation’.

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

### Levels

``` python
Levels(image=(0.0, 0.0, 0.0, 1.0), channel='Combined')
```

Compute average and standard deviation of pixel values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `(0.0, 0.0, 0.0, 1.0)` |
| channel | InputMenu \| Literal\['Combined', 'Red', 'Green', 'Blue', 'Luminance'\] | Channel | `'Combined'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Levels.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Levels.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Levels.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Levels.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Levels.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| `o.minimum`            | `FloatSocket` | Minimum            |
| `o.maximum`            | `FloatSocket` | Maximum            |

### RGBToBW

``` python
RGBToBW(image=(0.8, 0.8, 0.8, 1.0))
```

Convert RGB input into grayscale using luminance

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| image | InputColor | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.RGBToBW.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RGBToBW.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RGBToBW.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RGBToBW.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RGBToBW.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
    vector_value=(0.0, 0.0),
    float_value=0.0,
    image=(0.8, 0.8, 0.8, 1.0),
    *,
    data_type='FLOAT',
    reference_dimension='X',
)
```

Converts values that are relative to the image size to be in terms of pixels

#### Parameters

| Name         | Type        | Description | Default                |
|--------------|-------------|-------------|------------------------|
| vector_value | InputVector | Value       | `(0.0, 0.0)`           |
| float_value  | InputFloat  | Value       | `0.0`                  |
| image        | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.RelativeToPixel.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.RelativeToPixel.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RelativeToPixel.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RelativeToPixel.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RelativeToPixel.o) |  |
| [`reference_dimension`](#nodebpy.nodes.compositor.converter.RelativeToPixel.reference_dimension) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RelativeToPixel.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.compositor.converter.RelativeToPixel.float) | Create Relative To Pixel with operation ‘Float’. Float value |
| [vector](#nodebpy.nodes.compositor.converter.RelativeToPixel.vector) | Create Relative To Pixel with operation ‘Vector’. Vector value |

##### float

``` python
float(float_value=0.0, image=(0.8, 0.8, 0.8, 1.0), *, reference_dimension='X')
```

Create Relative To Pixel with operation ‘Float’. Float value

##### vector

``` python
vector(
    vector_value=(0.0, 0.0),
    image=(0.8, 0.8, 0.8, 1.0),
    *,
    reference_dimension='X',
)
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
SeparateColor(image=(1.0, 1.0, 1.0, 1.0), *, mode='RGB', ycc_mode='ITUBT709')
```

Split an image into its composite color channels

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| image | InputColor | Image       | `(1.0, 1.0, 1.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SeparateColor.i) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SeparateColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SeparateColor.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SeparateColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
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
hsl(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
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
| [`name`](#nodebpy.nodes.compositor.converter.SetAlpha.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SetAlpha.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SetAlpha.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SetAlpha.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
Split(
    position=(0.5, 0.5),
    rotation=math.pi / 4,
    image=(0.8, 0.8, 0.8, 1.0),
    image_001=(0.8, 0.8, 0.8, 1.0),
)
```

Combine two images for side-by-side display. Typically used in combination with a Viewer node

#### Parameters

| Name      | Type        | Description | Default                |
|-----------|-------------|-------------|------------------------|
| position  | InputVector | Position    | `(0.5, 0.5)`           |
| rotation  | InputFloat  | Rotation    | `math.pi / 4`          |
| image     | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |
| image_001 | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Split.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Split.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Split.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Split.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Split.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
Switch(switch=False, false=0.0, true=0.0, *, input_type=None)
```

Switch between two inputs

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| switch | InputBoolean | Switch      | `False` |
| false  | InputFloat   | False       | `0.0`   |
| true   | InputFloat   | True        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Switch.i) |  |
| [`input_type`](#nodebpy.nodes.compositor.converter.Switch.input_type) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Switch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Switch.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Switch.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Switch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.converter.Switch.boolean) | Create Switch with operation ‘Boolean’. |
| [color](#nodebpy.nodes.compositor.converter.Switch.color) | Create Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.Switch.float) | Create Switch with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.Switch.font) | Create Switch with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.converter.Switch.integer) | Create Switch with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.Switch.integer_vector) | Create Switch with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.converter.Switch.matrix) | Create Switch with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.Switch.menu) | Create Switch with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.Switch.object) | Create Switch with operation ‘Object’. |
| [rotation](#nodebpy.nodes.compositor.converter.Switch.rotation) | Create Switch with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.converter.Switch.string) | Create Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.Switch.vector) | Create Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(switch=False, false=False, true=False)
```

Create Switch with operation ‘Boolean’.

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

##### font

``` python
font(switch=False, false=None, true=None)
```

Create Switch with operation ‘Font’.

##### integer

``` python
integer(switch=False, false=0, true=0)
```

Create Switch with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(switch=False, false=(0, 0, 0), true=(0, 0, 0))
```

Create Switch with operation ‘Integer Vector’.

##### matrix

``` python
matrix(switch=False, false=None, true=None)
```

Create Switch with operation ‘Matrix’.

##### menu

``` python
menu(switch=False, false=None, true=None)
```

Create Switch with operation ‘Menu’.

##### object

``` python
object(switch=False, false=None, true=None)
```

Create Switch with operation ‘Object’.

##### rotation

``` python
rotation(switch=False, false=(0.0, 0.0, 0.0), true=(0.0, 0.0, 0.0))
```

Create Switch with operation ‘Rotation’.

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
| `i.false`  | `FloatSocket`   | False       |
| `i.true`   | `FloatSocket`   | True        |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `FloatSocket` | Output      |

### SwitchView

``` python
SwitchView(left=(0.0, 0.0, 0.0, 1.0), right=(0.0, 0.0, 0.0, 1.0))
```

Combine the views (left and right) into a single stereo 3D output

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| left  | InputColor | left        | `(0.0, 0.0, 0.0, 1.0)` |
| right | InputColor | right       | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SwitchView.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SwitchView.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SwitchView.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SwitchView.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SwitchView.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.left`  | `ColorSocket` | left        |
| `i.right` | `ColorSocket` | right       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
