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
| [IndexSwitch](#nodebpy.nodes.compositor.converter.IndexSwitch) | Choose between an arbitrary number of values with an index |
| [Levels](#nodebpy.nodes.compositor.converter.Levels) | Compute average and standard deviation of pixel values |
| [RGBToBW](#nodebpy.nodes.compositor.converter.RGBToBW) | Convert RGB input into grayscale using luminance |
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
| [`name`](#nodebpy.nodes.compositor.converter.AlphaConvert.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.AlphaConvert.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.AlphaConvert.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.AlphaConvert.outputs) |  |
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
| [`outputs`](#nodebpy.nodes.compositor.converter.CombineColor.outputs) |  |
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
| [`name`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.outputs) |  |
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
| [`outputs`](#nodebpy.nodes.compositor.converter.IDMask.outputs) |  |
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
ImplicitConversion(value=None, *, data_type='RGBA')
```

Implicitly convert the input value to a fixed socket type

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| value | InputColor | Value       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.ImplicitConversion.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.ImplicitConversion.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ImplicitConversion.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ImplicitConversion.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ImplicitConversion.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.ImplicitConversion.outputs) |  |
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
color(value=None)
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
integer_vector(value=None)
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
rotation(value=None)
```

Create Implicit Conversion with operation ‘Rotation’.

##### string

``` python
string(value='')
```

Create Implicit Conversion with operation ‘String’.

##### vector

``` python
vector(value=None)
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
IndexSwitch(index=0, item_0=None, item_1=None, extend=None, *, data_type='RGBA')
```

Choose between an arbitrary number of values with an index

#### Parameters

| Name   | Type          | Description | Default |
|--------|---------------|-------------|---------|
| index  | InputInteger  | Index       | `0`     |
| item_0 | InputColor    | 0           | `None`  |
| item_1 | InputColor    | 1           | `None`  |
| extend | InputLinkable |             | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.IndexSwitch.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.IndexSwitch.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.IndexSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.IndexSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.IndexSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.IndexSwitch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.converter.IndexSwitch.boolean) | Create Index Switch with operation ‘Boolean’. |
| [color](#nodebpy.nodes.compositor.converter.IndexSwitch.color) | Create Index Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.IndexSwitch.float) | Create Index Switch with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.IndexSwitch.font) | Create Index Switch with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.converter.IndexSwitch.integer) | Create Index Switch with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.IndexSwitch.integer_vector) | Create Index Switch with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.converter.IndexSwitch.matrix) | Create Index Switch with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.IndexSwitch.menu) | Create Index Switch with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.IndexSwitch.object) | Create Index Switch with operation ‘Object’. |
| [rotation](#nodebpy.nodes.compositor.converter.IndexSwitch.rotation) | Create Index Switch with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.converter.IndexSwitch.string) | Create Index Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.IndexSwitch.vector) | Create Index Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(index=0, item_0=False, item_1=False, extend=None)
```

Create Index Switch with operation ‘Boolean’.

##### color

``` python
color(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Color’.

##### float

``` python
float(index=0, item_0=0.0, item_1=0.0, extend=None)
```

Create Index Switch with operation ‘Float’.

##### font

``` python
font(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Font’.

##### integer

``` python
integer(index=0, item_0=0, item_1=0, extend=None)
```

Create Index Switch with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Integer Vector’.

##### matrix

``` python
matrix(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Matrix’.

##### menu

``` python
menu(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Menu’.

##### object

``` python
object(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Object’.

##### rotation

``` python
rotation(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Rotation’.

##### string

``` python
string(index=0, item_0='', item_1='', extend=None)
```

Create Index Switch with operation ‘String’.

##### vector

``` python
vector(index=0, item_0=None, item_1=None, extend=None)
```

Create Index Switch with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.index`  | `IntegerSocket` | Index       |
| `i.item_0` | `ColorSocket`   | 0           |
| `i.item_1` | `ColorSocket`   | 1           |
| `i.extend` | `Socket`        |             |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `ColorSocket` | Output      |

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
| [`name`](#nodebpy.nodes.compositor.converter.Levels.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Levels.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Levels.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Levels.outputs) |  |
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
RGBToBW(image=None)
```

Convert RGB input into grayscale using luminance

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.RGBToBW.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RGBToBW.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RGBToBW.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RGBToBW.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.RGBToBW.outputs) |  |
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
| [`name`](#nodebpy.nodes.compositor.converter.RelativeToPixel.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RelativeToPixel.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RelativeToPixel.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.RelativeToPixel.outputs) |  |
| [`reference_dimension`](#nodebpy.nodes.compositor.converter.RelativeToPixel.reference_dimension) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RelativeToPixel.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`mode`](#nodebpy.nodes.compositor.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SeparateColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SeparateColor.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SeparateColor.outputs) |  |
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
| [`name`](#nodebpy.nodes.compositor.converter.SetAlpha.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SetAlpha.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SetAlpha.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SetAlpha.outputs) |  |
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
| [`name`](#nodebpy.nodes.compositor.converter.Split.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Split.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Split.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Split.outputs) |  |
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
| [`name`](#nodebpy.nodes.compositor.converter.Switch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Switch.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Switch.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.Switch.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Switch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`name`](#nodebpy.nodes.compositor.converter.SwitchView.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SwitchView.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SwitchView.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.converter.SwitchView.outputs) |  |
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
