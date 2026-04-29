# nodes.shader.color

`color`

## Classes

| Name | Description |
|----|----|
| [Brightnesscontrast](#nodebpy.nodes.shader.color.Brightnesscontrast) | Control the brightness and contrast of the input color |
| [Huesaturationvalue](#nodebpy.nodes.shader.color.Huesaturationvalue) | Apply a color transformation in the HSV color model |
| [InvertColor](#nodebpy.nodes.shader.color.InvertColor) | Invert a color, producing a negative |
| [LightFalloff](#nodebpy.nodes.shader.color.LightFalloff) | Manipulate how light intensity decreases over distance. Typically used for non-physically-based effects; in reality light always falls off quadratically |

### Brightnesscontrast

``` python
Brightnesscontrast(color=None, bright=0.0, contrast=0.0)
```

Control the brightness and contrast of the input color

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| color    | InputColor | Color       | `None`  |
| bright   | InputFloat | Brightness  | `0.0`   |
| contrast | InputFloat | Contrast    | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.Brightnesscontrast.i) |  |
| [`name`](#nodebpy.nodes.shader.color.Brightnesscontrast.name) |  |
| [`node`](#nodebpy.nodes.shader.color.Brightnesscontrast.node) |  |
| [`o`](#nodebpy.nodes.shader.color.Brightnesscontrast.o) |  |
| [`outputs`](#nodebpy.nodes.shader.color.Brightnesscontrast.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.color.Brightnesscontrast.tree) |  |
| [`type`](#nodebpy.nodes.shader.color.Brightnesscontrast.type) |  |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.color`    | `ColorSocket` | Color       |
| `i.bright`   | `FloatSocket` | Brightness  |
| `i.contrast` | `FloatSocket` | Contrast    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### Huesaturationvalue

``` python
Huesaturationvalue(hue=0.5, saturation=1.0, value=1.0, fac=1.0, color=None)
```

Apply a color transformation in the HSV color model

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| hue        | InputFloat | Hue         | `0.5`   |
| saturation | InputFloat | Saturation  | `1.0`   |
| value      | InputFloat | Value       | `1.0`   |
| fac        | InputFloat | Factor      | `1.0`   |
| color      | InputColor | Color       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.color.Huesaturationvalue.i) |  |
| [`name`](#nodebpy.nodes.shader.color.Huesaturationvalue.name) |  |
| [`node`](#nodebpy.nodes.shader.color.Huesaturationvalue.node) |  |
| [`o`](#nodebpy.nodes.shader.color.Huesaturationvalue.o) |  |
| [`outputs`](#nodebpy.nodes.shader.color.Huesaturationvalue.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.color.Huesaturationvalue.tree) |  |
| [`type`](#nodebpy.nodes.shader.color.Huesaturationvalue.type) |  |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.hue`        | `FloatSocket` | Hue         |
| `i.saturation` | `FloatSocket` | Saturation  |
| `i.value`      | `FloatSocket` | Value       |
| `i.fac`        | `FloatSocket` | Factor      |
| `i.color`      | `ColorSocket` | Color       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### InvertColor

``` python
InvertColor(fac=1.0, color=None)
```

Invert a color, producing a negative

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| fac   | InputFloat | Factor      | `1.0`   |
| color | InputColor | Color       | `None`  |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.color.InvertColor.i)             |             |
| [`name`](#nodebpy.nodes.shader.color.InvertColor.name)       |             |
| [`node`](#nodebpy.nodes.shader.color.InvertColor.node)       |             |
| [`o`](#nodebpy.nodes.shader.color.InvertColor.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.color.InvertColor.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.color.InvertColor.tree)       |             |
| [`type`](#nodebpy.nodes.shader.color.InvertColor.type)       |             |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.fac`   | `FloatSocket` | Factor      |
| `i.color` | `ColorSocket` | Color       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### LightFalloff

``` python
LightFalloff(strength=100.0, smooth=0.0)
```

Manipulate how light intensity decreases over distance. Typically used for non-physically-based effects; in reality light always falls off quadratically

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| strength | InputFloat | Strength    | `100.0` |
| smooth   | InputFloat | Smooth      | `0.0`   |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.color.LightFalloff.i)             |             |
| [`name`](#nodebpy.nodes.shader.color.LightFalloff.name)       |             |
| [`node`](#nodebpy.nodes.shader.color.LightFalloff.node)       |             |
| [`o`](#nodebpy.nodes.shader.color.LightFalloff.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.color.LightFalloff.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.color.LightFalloff.tree)       |             |
| [`type`](#nodebpy.nodes.shader.color.LightFalloff.type)       |             |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.strength` | `FloatSocket` | Strength    |
| `i.smooth`   | `FloatSocket` | Smooth      |

**Outputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `o.quadratic` | `FloatSocket` | Quadratic   |
| `o.linear`    | `FloatSocket` | Linear      |
| `o.constant`  | `FloatSocket` | Constant    |
