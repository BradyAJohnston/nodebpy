# nodes.geometry.color

`color`

## Classes

| Name | Description |
|----|----|
| [Gamma](#nodebpy.nodes.geometry.color.Gamma) | Apply a gamma correction |
| [RGBCurves](#nodebpy.nodes.geometry.color.RGBCurves) | Apply color corrections for each color channel |

### Gamma

``` python
Gamma(color=None, gamma=1.0)
```

Apply a gamma correction

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| color | InputColor | Color       | `None`  |
| gamma | InputFloat | Gamma       | `1.0`   |

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.color.Gamma.i)             |             |
| [`name`](#nodebpy.nodes.geometry.color.Gamma.name)       |             |
| [`node`](#nodebpy.nodes.geometry.color.Gamma.node)       |             |
| [`o`](#nodebpy.nodes.geometry.color.Gamma.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.color.Gamma.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.color.Gamma.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.color.Gamma.type)       |             |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.color` | `ColorSocket` | Color       |
| `i.gamma` | `FloatSocket` | Gamma       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### RGBCurves

``` python
RGBCurves(fac=1.0, color=None)
```

Apply color corrections for each color channel

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| fac   | InputFloat | Factor      | `1.0`   |
| color | InputColor | Color       | `None`  |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.color.RGBCurves.i)             |             |
| [`name`](#nodebpy.nodes.geometry.color.RGBCurves.name)       |             |
| [`node`](#nodebpy.nodes.geometry.color.RGBCurves.node)       |             |
| [`o`](#nodebpy.nodes.geometry.color.RGBCurves.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.color.RGBCurves.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.color.RGBCurves.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.color.RGBCurves.type)       |             |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.fac`   | `FloatSocket` | Factor      |
| `i.color` | `ColorSocket` | Color       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
