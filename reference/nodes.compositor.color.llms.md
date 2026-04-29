# nodes.compositor.color

`color`

## Classes

| Name | Description |
|----|----|
| [AlphaOver](#nodebpy.nodes.compositor.color.AlphaOver) | Overlay a foreground image onto a background image |
| [Brightnesscontrast](#nodebpy.nodes.compositor.color.Brightnesscontrast) | Adjust brightness and contrast |
| [ColorBalance](#nodebpy.nodes.compositor.color.ColorBalance) | Adjust color and values |
| [ColorCorrection](#nodebpy.nodes.compositor.color.ColorCorrection) | Adjust the color of an image, separately in several tonal ranges (highlights, midtones and shadows) |
| [DepthCombine](#nodebpy.nodes.compositor.color.DepthCombine) | Combine two images using depth maps |
| [Exposure](#nodebpy.nodes.compositor.color.Exposure) | Adjust brightness using a camera exposure parameter |
| [HueCorrect](#nodebpy.nodes.compositor.color.HueCorrect) | Adjust hue, saturation, and value with a curve |
| [Huesaturationvalue](#nodebpy.nodes.compositor.color.Huesaturationvalue) | Apply a color transformation in the HSV color model |
| [InvertColor](#nodebpy.nodes.compositor.color.InvertColor) | Invert colors, producing a negative |
| [Posterize](#nodebpy.nodes.compositor.color.Posterize) | Reduce number of colors in an image, converting smooth gradients into sharp transitions |
| [RGBCurves](#nodebpy.nodes.compositor.color.RGBCurves) | Perform level adjustments on each color channel of an image |
| [Tonemap](#nodebpy.nodes.compositor.color.Tonemap) | Map one set of colors to another in order to approximate the appearance of high dynamic range |

### AlphaOver

``` python
AlphaOver(
    background=None,
    foreground=None,
    fac=1.0,
    type='Over',
    straight_alpha=False,
)
```

Overlay a foreground image onto a background image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| background | InputColor | Background | `None` |
| foreground | InputColor | Foreground | `None` |
| fac | InputFloat | Factor | `1.0` |
| type | InputMenu \| Literal\['Over', 'Disjoint Over', 'Conjoint Over'\] | Type | `'Over'` |
| straight_alpha | InputBoolean | Straight Alpha | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.AlphaOver.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.AlphaOver.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.AlphaOver.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.AlphaOver.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.AlphaOver.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.AlphaOver.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.AlphaOver.type) |  |

#### Methods

| Name | Description |
|----|----|
| [conjoint_over](#nodebpy.nodes.compositor.color.AlphaOver.conjoint_over) | Create Alpha Over node with type ‘Conjoint Over’. |
| [disjoint_over](#nodebpy.nodes.compositor.color.AlphaOver.disjoint_over) | Create Alpha Over node with type ‘Disjoint Over’. |
| [over](#nodebpy.nodes.compositor.color.AlphaOver.over) | Create Alpha Over node with type ‘Over’. |

##### conjoint_over

``` python
conjoint_over(background=None, foreground=None, fac=1.0, straight_alpha=False)
```

Create Alpha Over node with type ‘Conjoint Over’.

##### disjoint_over

``` python
disjoint_over(background=None, foreground=None, fac=1.0, straight_alpha=False)
```

Create Alpha Over node with type ‘Disjoint Over’.

##### over

``` python
over(background=None, foreground=None, fac=1.0, straight_alpha=False)
```

Create Alpha Over node with type ‘Over’.

**Inputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `i.background`     | `ColorSocket`   | Background     |
| `i.foreground`     | `ColorSocket`   | Foreground     |
| `i.fac`            | `FloatSocket`   | Factor         |
| `i.type`           | `MenuSocket`    | Type           |
| `i.straight_alpha` | `BooleanSocket` | Straight Alpha |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Brightnesscontrast

``` python
Brightnesscontrast(image=None, bright=0.0, contrast=0.0)
```

Adjust brightness and contrast

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| image    | InputColor | Image       | `None`  |
| bright   | InputFloat | Brightness  | `0.0`   |
| contrast | InputFloat | Contrast    | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.Brightnesscontrast.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.Brightnesscontrast.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.Brightnesscontrast.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.Brightnesscontrast.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.Brightnesscontrast.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.Brightnesscontrast.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.Brightnesscontrast.type) |  |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.image`    | `ColorSocket` | Image       |
| `i.bright`   | `FloatSocket` | Brightness  |
| `i.contrast` | `FloatSocket` | Contrast    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### ColorBalance

``` python
ColorBalance(
    image=None,
    fac=1.0,
    type='Lift/Gamma/Gain',
    base_lift=0.0,
    color_lift=None,
    base_gamma=1.0,
    color_gamma=None,
    base_gain=1.0,
    color_gain=None,
    base_offset=0.0,
    color_offset=None,
    base_power=1.0,
    color_power=None,
    base_slope=1.0,
    color_slope=None,
    input_temperature=6500.0,
    input_tint=10.0,
    output_temperature=6500.0,
    output_tint=10.0,
    *,
    input_whitepoint=(0.735, 0.735, 0.735),
    output_whitepoint=(0.735, 0.735, 0.735),
)
```

Adjust color and values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| fac | InputFloat | Factor | `1.0` |
| type | InputMenu \| Literal\['Lift/Gamma/Gain', 'Offset/Power/Slope (ASC-CDL)', 'White Point'\] | Type | `'Lift/Gamma/Gain'` |
| base_lift | InputFloat | Lift | `0.0` |
| color_lift | InputColor | Lift | `None` |
| base_gamma | InputFloat | Gamma | `1.0` |
| color_gamma | InputColor | Gamma | `None` |
| base_gain | InputFloat | Gain | `1.0` |
| color_gain | InputColor | Gain | `None` |
| base_offset | InputFloat | Offset | `0.0` |
| color_offset | InputColor | Offset | `None` |
| base_power | InputFloat | Power | `1.0` |
| color_power | InputColor | Power | `None` |
| base_slope | InputFloat | Slope | `1.0` |
| color_slope | InputColor | Slope | `None` |
| input_temperature | InputFloat | Temperature | `6500.0` |
| input_tint | InputFloat | Tint | `10.0` |
| output_temperature | InputFloat | Temperature | `6500.0` |
| output_tint | InputFloat | Tint | `10.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.ColorBalance.i) |  |
| [`input_whitepoint`](#nodebpy.nodes.compositor.color.ColorBalance.input_whitepoint) |  |
| [`name`](#nodebpy.nodes.compositor.color.ColorBalance.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.ColorBalance.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.ColorBalance.o) |  |
| [`output_whitepoint`](#nodebpy.nodes.compositor.color.ColorBalance.output_whitepoint) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.ColorBalance.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.ColorBalance.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.ColorBalance.type) |  |

#### Methods

| Name | Description |
|----|----|
| [lift_gamma_gain](#nodebpy.nodes.compositor.color.ColorBalance.lift_gamma_gain) | Create Color Balance node with type ‘Lift/Gamma/Gain’. |
| [offset_power_slope_asc_cdl](#nodebpy.nodes.compositor.color.ColorBalance.offset_power_slope_asc_cdl) | Create Color Balance node with type ‘Offset/Power/Slope (ASC-CDL)’. |
| [white_point](#nodebpy.nodes.compositor.color.ColorBalance.white_point) | Create Color Balance node with type ‘White Point’. |

##### lift_gamma_gain

``` python
lift_gamma_gain(
    image=None,
    fac=1.0,
    base_lift=0.0,
    color_lift=None,
    base_gamma=1.0,
    color_gamma=None,
    base_gain=1.0,
    color_gain=None,
)
```

Create Color Balance node with type ‘Lift/Gamma/Gain’.

##### offset_power_slope_asc_cdl

``` python
offset_power_slope_asc_cdl(
    image=None,
    fac=1.0,
    base_offset=0.0,
    color_offset=None,
    base_power=1.0,
    color_power=None,
    base_slope=1.0,
    color_slope=None,
)
```

Create Color Balance node with type ‘Offset/Power/Slope (ASC-CDL)’.

##### white_point

``` python
white_point(
    image=None,
    fac=1.0,
    input_temperature=6500.0,
    input_tint=10.0,
    output_temperature=6500.0,
    output_tint=10.0,
)
```

Create Color Balance node with type ‘White Point’.

**Inputs**

| Attribute              | Type          | Description |
|------------------------|---------------|-------------|
| `i.image`              | `ColorSocket` | Image       |
| `i.fac`                | `FloatSocket` | Factor      |
| `i.type`               | `MenuSocket`  | Type        |
| `i.base_lift`          | `FloatSocket` | Lift        |
| `i.color_lift`         | `ColorSocket` | Lift        |
| `i.base_gamma`         | `FloatSocket` | Gamma       |
| `i.color_gamma`        | `ColorSocket` | Gamma       |
| `i.base_gain`          | `FloatSocket` | Gain        |
| `i.color_gain`         | `ColorSocket` | Gain        |
| `i.base_offset`        | `FloatSocket` | Offset      |
| `i.color_offset`       | `ColorSocket` | Offset      |
| `i.base_power`         | `FloatSocket` | Power       |
| `i.color_power`        | `ColorSocket` | Power       |
| `i.base_slope`         | `FloatSocket` | Slope       |
| `i.color_slope`        | `ColorSocket` | Slope       |
| `i.input_temperature`  | `FloatSocket` | Temperature |
| `i.input_tint`         | `FloatSocket` | Tint        |
| `i.output_temperature` | `FloatSocket` | Temperature |
| `i.output_tint`        | `FloatSocket` | Tint        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### ColorCorrection

``` python
ColorCorrection(
    image=None,
    mask=1.0,
    master_saturation=1.0,
    master_contrast=1.0,
    master_gamma=1.0,
    master_gain=1.0,
    master_offset=0.0,
    highlights_saturation=1.0,
    highlights_contrast=1.0,
    highlights_gamma=1.0,
    highlights_gain=1.0,
    highlights_offset=0.0,
    midtones_saturation=1.0,
    midtones_contrast=1.0,
    midtones_gamma=1.0,
    midtones_gain=1.0,
    midtones_offset=0.0,
    shadows_saturation=1.0,
    shadows_contrast=1.0,
    shadows_gamma=1.0,
    shadows_gain=1.0,
    shadows_offset=0.0,
    midtones_start=0.2,
    midtones_end=0.7,
    apply_on_red=True,
    apply_on_green=True,
    apply_on_blue=True,
)
```

Adjust the color of an image, separately in several tonal ranges (highlights, midtones and shadows)

#### Parameters

| Name                  | Type         | Description    | Default |
|-----------------------|--------------|----------------|---------|
| image                 | InputColor   | Image          | `None`  |
| mask                  | InputFloat   | Mask           | `1.0`   |
| master_saturation     | InputFloat   | Saturation     | `1.0`   |
| master_contrast       | InputFloat   | Contrast       | `1.0`   |
| master_gamma          | InputFloat   | Gamma          | `1.0`   |
| master_gain           | InputFloat   | Gain           | `1.0`   |
| master_offset         | InputFloat   | Offset         | `0.0`   |
| highlights_saturation | InputFloat   | Saturation     | `1.0`   |
| highlights_contrast   | InputFloat   | Contrast       | `1.0`   |
| highlights_gamma      | InputFloat   | Gamma          | `1.0`   |
| highlights_gain       | InputFloat   | Gain           | `1.0`   |
| highlights_offset     | InputFloat   | Offset         | `0.0`   |
| midtones_saturation   | InputFloat   | Saturation     | `1.0`   |
| midtones_contrast     | InputFloat   | Contrast       | `1.0`   |
| midtones_gamma        | InputFloat   | Gamma          | `1.0`   |
| midtones_gain         | InputFloat   | Gain           | `1.0`   |
| midtones_offset       | InputFloat   | Offset         | `0.0`   |
| shadows_saturation    | InputFloat   | Saturation     | `1.0`   |
| shadows_contrast      | InputFloat   | Contrast       | `1.0`   |
| shadows_gamma         | InputFloat   | Gamma          | `1.0`   |
| shadows_gain          | InputFloat   | Gain           | `1.0`   |
| shadows_offset        | InputFloat   | Offset         | `0.0`   |
| midtones_start        | InputFloat   | Midtones Start | `0.2`   |
| midtones_end          | InputFloat   | Midtones End   | `0.7`   |
| apply_on_red          | InputBoolean | Red            | `True`  |
| apply_on_green        | InputBoolean | Green          | `True`  |
| apply_on_blue         | InputBoolean | Blue           | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.ColorCorrection.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.ColorCorrection.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.ColorCorrection.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.ColorCorrection.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.ColorCorrection.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.ColorCorrection.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.ColorCorrection.type) |  |

**Inputs**

| Attribute                 | Type            | Description    |
|---------------------------|-----------------|----------------|
| `i.image`                 | `ColorSocket`   | Image          |
| `i.mask`                  | `FloatSocket`   | Mask           |
| `i.master_saturation`     | `FloatSocket`   | Saturation     |
| `i.master_contrast`       | `FloatSocket`   | Contrast       |
| `i.master_gamma`          | `FloatSocket`   | Gamma          |
| `i.master_gain`           | `FloatSocket`   | Gain           |
| `i.master_offset`         | `FloatSocket`   | Offset         |
| `i.highlights_saturation` | `FloatSocket`   | Saturation     |
| `i.highlights_contrast`   | `FloatSocket`   | Contrast       |
| `i.highlights_gamma`      | `FloatSocket`   | Gamma          |
| `i.highlights_gain`       | `FloatSocket`   | Gain           |
| `i.highlights_offset`     | `FloatSocket`   | Offset         |
| `i.midtones_saturation`   | `FloatSocket`   | Saturation     |
| `i.midtones_contrast`     | `FloatSocket`   | Contrast       |
| `i.midtones_gamma`        | `FloatSocket`   | Gamma          |
| `i.midtones_gain`         | `FloatSocket`   | Gain           |
| `i.midtones_offset`       | `FloatSocket`   | Offset         |
| `i.shadows_saturation`    | `FloatSocket`   | Saturation     |
| `i.shadows_contrast`      | `FloatSocket`   | Contrast       |
| `i.shadows_gamma`         | `FloatSocket`   | Gamma          |
| `i.shadows_gain`          | `FloatSocket`   | Gain           |
| `i.shadows_offset`        | `FloatSocket`   | Offset         |
| `i.midtones_start`        | `FloatSocket`   | Midtones Start |
| `i.midtones_end`          | `FloatSocket`   | Midtones End   |
| `i.apply_on_red`          | `BooleanSocket` | Red            |
| `i.apply_on_green`        | `BooleanSocket` | Green          |
| `i.apply_on_blue`         | `BooleanSocket` | Blue           |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### DepthCombine

``` python
DepthCombine(
    a=None,
    depth_a=1.0,
    b=None,
    depth_b=1.0,
    use_alpha=False,
    anti_alias=True,
)
```

Combine two images using depth maps

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| a          | InputColor   | A           | `None`  |
| depth_a    | InputFloat   | Depth A     | `1.0`   |
| b          | InputColor   | B           | `None`  |
| depth_b    | InputFloat   | Depth B     | `1.0`   |
| use_alpha  | InputBoolean | Use Alpha   | `False` |
| anti_alias | InputBoolean | Anti-Alias  | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.DepthCombine.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.DepthCombine.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.DepthCombine.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.DepthCombine.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.DepthCombine.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.DepthCombine.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.DepthCombine.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.a`          | `ColorSocket`   | A           |
| `i.depth_a`    | `FloatSocket`   | Depth A     |
| `i.b`          | `ColorSocket`   | B           |
| `i.depth_b`    | `FloatSocket`   | Depth B     |
| `i.use_alpha`  | `BooleanSocket` | Use Alpha   |
| `i.anti_alias` | `BooleanSocket` | Anti-Alias  |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.result` | `ColorSocket` | Result      |
| `o.depth`  | `FloatSocket` | Depth       |

### Exposure

``` python
Exposure(image=None, exposure=0.0)
```

Adjust brightness using a camera exposure parameter

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| image    | InputColor | Image       | `None`  |
| exposure | InputFloat | Exposure    | `0.0`   |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.color.Exposure.i)             |             |
| [`name`](#nodebpy.nodes.compositor.color.Exposure.name)       |             |
| [`node`](#nodebpy.nodes.compositor.color.Exposure.node)       |             |
| [`o`](#nodebpy.nodes.compositor.color.Exposure.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.color.Exposure.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.color.Exposure.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.color.Exposure.type)       |             |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.image`    | `ColorSocket` | Image       |
| `i.exposure` | `FloatSocket` | Exposure    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### HueCorrect

``` python
HueCorrect(image=None, fac=1.0)
```

Adjust hue, saturation, and value with a curve

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |
| fac   | InputFloat | Factor      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.HueCorrect.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.HueCorrect.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.HueCorrect.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.HueCorrect.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.HueCorrect.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.HueCorrect.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.HueCorrect.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.fac`   | `FloatSocket` | Factor      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Huesaturationvalue

``` python
Huesaturationvalue(image=None, hue=0.5, saturation=1.0, value=1.0, fac=1.0)
```

Apply a color transformation in the HSV color model

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| image      | InputColor | Image       | `None`  |
| hue        | InputFloat | Hue         | `0.5`   |
| saturation | InputFloat | Saturation  | `1.0`   |
| value      | InputFloat | Value       | `1.0`   |
| fac        | InputFloat | Factor      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.Huesaturationvalue.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.Huesaturationvalue.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.Huesaturationvalue.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.Huesaturationvalue.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.Huesaturationvalue.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.Huesaturationvalue.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.Huesaturationvalue.type) |  |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.image`      | `ColorSocket` | Image       |
| `i.hue`        | `FloatSocket` | Hue         |
| `i.saturation` | `FloatSocket` | Saturation  |
| `i.value`      | `FloatSocket` | Value       |
| `i.fac`        | `FloatSocket` | Factor      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### InvertColor

``` python
InvertColor(color=None, fac=1.0, invert_color=True, invert_alpha=False)
```

Invert colors, producing a negative

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| color        | InputColor   | Color        | `None`  |
| fac          | InputFloat   | Factor       | `1.0`   |
| invert_color | InputBoolean | Invert Color | `True`  |
| invert_alpha | InputBoolean | Invert Alpha | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.InvertColor.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.InvertColor.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.InvertColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.InvertColor.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.InvertColor.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.InvertColor.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.InvertColor.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.color`        | `ColorSocket`   | Color        |
| `i.fac`          | `FloatSocket`   | Factor       |
| `i.invert_color` | `BooleanSocket` | Invert Color |
| `i.invert_alpha` | `BooleanSocket` | Invert Alpha |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### Posterize

``` python
Posterize(image=None, steps=8.0)
```

Reduce number of colors in an image, converting smooth gradients into sharp transitions

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |
| steps | InputFloat | Steps       | `8.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.Posterize.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.Posterize.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.Posterize.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.Posterize.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.Posterize.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.Posterize.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.Posterize.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.steps` | `FloatSocket` | Steps       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### RGBCurves

``` python
RGBCurves(image=None, fac=1.0, black_level=None, white_level=None)
```

Perform level adjustments on each color channel of an image

#### Parameters

| Name        | Type       | Description | Default |
|-------------|------------|-------------|---------|
| image       | InputColor | Image       | `None`  |
| fac         | InputFloat | Factor      | `1.0`   |
| black_level | InputColor | Black Level | `None`  |
| white_level | InputColor | White Level | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.color.RGBCurves.i) |  |
| [`name`](#nodebpy.nodes.compositor.color.RGBCurves.name) |  |
| [`node`](#nodebpy.nodes.compositor.color.RGBCurves.node) |  |
| [`o`](#nodebpy.nodes.compositor.color.RGBCurves.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.color.RGBCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.color.RGBCurves.tree) |  |
| [`type`](#nodebpy.nodes.compositor.color.RGBCurves.type) |  |

**Inputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `i.image`       | `ColorSocket` | Image       |
| `i.fac`         | `FloatSocket` | Factor      |
| `i.black_level` | `ColorSocket` | Black Level |
| `i.white_level` | `ColorSocket` | White Level |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Tonemap

``` python
Tonemap(
    image=None,
    type='R/D Photoreceptor',
    key=0.18,
    balance=1.0,
    gamma=1.0,
    intensity=0.0,
    contrast=0.0,
    light_adaptation=0.0,
    chromatic_adaptation=0.0,
)
```

Map one set of colors to another in order to approximate the appearance of high dynamic range

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['R/D Photoreceptor', 'Rh Simple'\] | Type | `'R/D Photoreceptor'` |
| key | InputFloat | Key | `0.18` |
| balance | InputFloat | Balance | `1.0` |
| gamma | InputFloat | Gamma | `1.0` |
| intensity | InputFloat | Intensity | `0.0` |
| contrast | InputFloat | Contrast | `0.0` |
| light_adaptation | InputFloat | Light Adaptation | `0.0` |
| chromatic_adaptation | InputFloat | Chromatic Adaptation | `0.0` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.color.Tonemap.i)             |             |
| [`name`](#nodebpy.nodes.compositor.color.Tonemap.name)       |             |
| [`node`](#nodebpy.nodes.compositor.color.Tonemap.node)       |             |
| [`o`](#nodebpy.nodes.compositor.color.Tonemap.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.color.Tonemap.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.color.Tonemap.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.color.Tonemap.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [r_d_photoreceptor](#nodebpy.nodes.compositor.color.Tonemap.r_d_photoreceptor) | Create Tonemap node with type ‘R/D Photoreceptor’. |
| [rh_simple](#nodebpy.nodes.compositor.color.Tonemap.rh_simple) | Create Tonemap node with type ‘Rh Simple’. |

##### r_d_photoreceptor

``` python
r_d_photoreceptor(
    image=None,
    intensity=0.0,
    contrast=0.0,
    light_adaptation=0.0,
    chromatic_adaptation=0.0,
)
```

Create Tonemap node with type ‘R/D Photoreceptor’.

##### rh_simple

``` python
rh_simple(image=None, key=0.18, balance=1.0, gamma=1.0)
```

Create Tonemap node with type ‘Rh Simple’.

**Inputs**

| Attribute                | Type          | Description          |
|--------------------------|---------------|----------------------|
| `i.image`                | `ColorSocket` | Image                |
| `i.type`                 | `MenuSocket`  | Type                 |
| `i.key`                  | `FloatSocket` | Key                  |
| `i.balance`              | `FloatSocket` | Balance              |
| `i.gamma`                | `FloatSocket` | Gamma                |
| `i.intensity`            | `FloatSocket` | Intensity            |
| `i.contrast`             | `FloatSocket` | Contrast             |
| `i.light_adaptation`     | `FloatSocket` | Light Adaptation     |
| `i.chromatic_adaptation` | `FloatSocket` | Chromatic Adaptation |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
