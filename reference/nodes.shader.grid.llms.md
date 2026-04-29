# nodes.shader.grid

`grid`

## Classes

| Name | Description |
|----|----|
| [PrincipledVolume](#nodebpy.nodes.shader.grid.PrincipledVolume) | Combine all volume shading components into a single easy to use node |
| [VolumeAbsorption](#nodebpy.nodes.shader.grid.VolumeAbsorption) | Absorb light as it passes through the volume |
| [VolumeCoefficients](#nodebpy.nodes.shader.grid.VolumeCoefficients) | Model all three physical processes in a volume, represented by their coefficients |
| [VolumeInfo](#nodebpy.nodes.shader.grid.VolumeInfo) | Read volume data attributes from volume grids |
| [VolumeScatter](#nodebpy.nodes.shader.grid.VolumeScatter) | Scatter light as it passes through the volume, often used to add fog to a scene |

### PrincipledVolume

``` python
PrincipledVolume(
    color=None,
    color_attribute='',
    density=1.0,
    density_attribute='density',
    anisotropy=0.0,
    absorption_color=None,
    emission_strength=0.0,
    emission_color=None,
    blackbody_intensity=0.0,
    blackbody_tint=None,
    temperature=1000.0,
    temperature_attribute='temperature',
    weight=0.0,
)
```

Combine all volume shading components into a single easy to use node

#### Parameters

| Name                  | Type        | Description           | Default         |
|-----------------------|-------------|-----------------------|-----------------|
| color                 | InputColor  | Color                 | `None`          |
| color_attribute       | InputString | Color Attribute       | `''`            |
| density               | InputFloat  | Density               | `1.0`           |
| density_attribute     | InputString | Density Attribute     | `'density'`     |
| anisotropy            | InputFloat  | Anisotropy            | `0.0`           |
| absorption_color      | InputColor  | Absorption Color      | `None`          |
| emission_strength     | InputFloat  | Emission Strength     | `0.0`           |
| emission_color        | InputColor  | Emission Color        | `None`          |
| blackbody_intensity   | InputFloat  | Blackbody Intensity   | `0.0`           |
| blackbody_tint        | InputColor  | Blackbody Tint        | `None`          |
| temperature           | InputFloat  | Temperature           | `1000.0`        |
| temperature_attribute | InputString | Temperature Attribute | `'temperature'` |
| weight                | InputFloat  | Weight                | `0.0`           |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.PrincipledVolume.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.PrincipledVolume.name) |  |
| [`node`](#nodebpy.nodes.shader.grid.PrincipledVolume.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.PrincipledVolume.o) |  |
| [`outputs`](#nodebpy.nodes.shader.grid.PrincipledVolume.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.grid.PrincipledVolume.tree) |  |
| [`type`](#nodebpy.nodes.shader.grid.PrincipledVolume.type) |  |

**Inputs**

| Attribute                 | Type           | Description           |
|---------------------------|----------------|-----------------------|
| `i.color`                 | `ColorSocket`  | Color                 |
| `i.color_attribute`       | `StringSocket` | Color Attribute       |
| `i.density`               | `FloatSocket`  | Density               |
| `i.density_attribute`     | `StringSocket` | Density Attribute     |
| `i.anisotropy`            | `FloatSocket`  | Anisotropy            |
| `i.absorption_color`      | `ColorSocket`  | Absorption Color      |
| `i.emission_strength`     | `FloatSocket`  | Emission Strength     |
| `i.emission_color`        | `ColorSocket`  | Emission Color        |
| `i.blackbody_intensity`   | `FloatSocket`  | Blackbody Intensity   |
| `i.blackbody_tint`        | `ColorSocket`  | Blackbody Tint        |
| `i.temperature`           | `FloatSocket`  | Temperature           |
| `i.temperature_attribute` | `StringSocket` | Temperature Attribute |
| `i.weight`                | `FloatSocket`  | Weight                |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeAbsorption

``` python
VolumeAbsorption(color=None, density=1.0, weight=0.0)
```

Absorb light as it passes through the volume

#### Parameters

| Name    | Type       | Description | Default |
|---------|------------|-------------|---------|
| color   | InputColor | Color       | `None`  |
| density | InputFloat | Density     | `1.0`   |
| weight  | InputFloat | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeAbsorption.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeAbsorption.name) |  |
| [`node`](#nodebpy.nodes.shader.grid.VolumeAbsorption.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeAbsorption.o) |  |
| [`outputs`](#nodebpy.nodes.shader.grid.VolumeAbsorption.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeAbsorption.tree) |  |
| [`type`](#nodebpy.nodes.shader.grid.VolumeAbsorption.type) |  |

**Inputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.color`   | `ColorSocket` | Color       |
| `i.density` | `FloatSocket` | Density     |
| `i.weight`  | `FloatSocket` | Weight      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeCoefficients

``` python
VolumeCoefficients(
    weight=0.0,
    absorption_coefficients=None,
    scatter_coefficients=None,
    anisotropy=0.0,
    ior=1.33,
    backscatter=0.1,
    alpha=0.5,
    diameter=20.0,
    emission_coefficients=None,
    *,
    phase='HENYEY_GREENSTEIN',
)
```

Model all three physical processes in a volume, represented by their coefficients

#### Parameters

| Name                    | Type        | Description             | Default |
|-------------------------|-------------|-------------------------|---------|
| weight                  | InputFloat  | Weight                  | `0.0`   |
| absorption_coefficients | InputVector | Absorption Coefficients | `None`  |
| scatter_coefficients    | InputVector | Scatter Coefficients    | `None`  |
| anisotropy              | InputFloat  | Anisotropy              | `0.0`   |
| ior                     | InputFloat  | IOR                     | `1.33`  |
| backscatter             | InputFloat  | Backscatter             | `0.1`   |
| alpha                   | InputFloat  | Alpha                   | `0.5`   |
| diameter                | InputFloat  | Diameter                | `20.0`  |
| emission_coefficients   | InputVector | Emission Coefficients   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.grid.VolumeCoefficients.i) |  |
| [`name`](#nodebpy.nodes.shader.grid.VolumeCoefficients.name) |  |
| [`node`](#nodebpy.nodes.shader.grid.VolumeCoefficients.node) |  |
| [`o`](#nodebpy.nodes.shader.grid.VolumeCoefficients.o) |  |
| [`outputs`](#nodebpy.nodes.shader.grid.VolumeCoefficients.outputs) |  |
| [`phase`](#nodebpy.nodes.shader.grid.VolumeCoefficients.phase) |  |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeCoefficients.tree) |  |
| [`type`](#nodebpy.nodes.shader.grid.VolumeCoefficients.type) |  |

**Inputs**

| Attribute                   | Type           | Description             |
|-----------------------------|----------------|-------------------------|
| `i.weight`                  | `FloatSocket`  | Weight                  |
| `i.absorption_coefficients` | `VectorSocket` | Absorption Coefficients |
| `i.scatter_coefficients`    | `VectorSocket` | Scatter Coefficients    |
| `i.anisotropy`              | `FloatSocket`  | Anisotropy              |
| `i.ior`                     | `FloatSocket`  | IOR                     |
| `i.backscatter`             | `FloatSocket`  | Backscatter             |
| `i.alpha`                   | `FloatSocket`  | Alpha                   |
| `i.diameter`                | `FloatSocket`  | Diameter                |
| `i.emission_coefficients`   | `VectorSocket` | Emission Coefficients   |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |

### VolumeInfo

``` python
VolumeInfo()
```

Read volume data attributes from volume grids

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.grid.VolumeInfo.i)             |             |
| [`name`](#nodebpy.nodes.shader.grid.VolumeInfo.name)       |             |
| [`node`](#nodebpy.nodes.shader.grid.VolumeInfo.node)       |             |
| [`o`](#nodebpy.nodes.shader.grid.VolumeInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.grid.VolumeInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeInfo.tree)       |             |
| [`type`](#nodebpy.nodes.shader.grid.VolumeInfo.type)       |             |

**Outputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `o.color`       | `ColorSocket` | Color       |
| `o.density`     | `FloatSocket` | Density     |
| `o.flame`       | `FloatSocket` | Flame       |
| `o.temperature` | `FloatSocket` | Temperature |

### VolumeScatter

``` python
VolumeScatter(
    color=None,
    density=1.0,
    anisotropy=0.0,
    ior=1.33,
    backscatter=0.1,
    alpha=0.5,
    diameter=20.0,
    weight=0.0,
    *,
    phase='HENYEY_GREENSTEIN',
)
```

Scatter light as it passes through the volume, often used to add fog to a scene

#### Parameters

| Name        | Type       | Description | Default |
|-------------|------------|-------------|---------|
| color       | InputColor | Color       | `None`  |
| density     | InputFloat | Density     | `1.0`   |
| anisotropy  | InputFloat | Anisotropy  | `0.0`   |
| ior         | InputFloat | IOR         | `1.33`  |
| backscatter | InputFloat | Backscatter | `0.1`   |
| alpha       | InputFloat | Alpha       | `0.5`   |
| diameter    | InputFloat | Diameter    | `20.0`  |
| weight      | InputFloat | Weight      | `0.0`   |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.grid.VolumeScatter.i)             |             |
| [`name`](#nodebpy.nodes.shader.grid.VolumeScatter.name)       |             |
| [`node`](#nodebpy.nodes.shader.grid.VolumeScatter.node)       |             |
| [`o`](#nodebpy.nodes.shader.grid.VolumeScatter.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.grid.VolumeScatter.outputs) |             |
| [`phase`](#nodebpy.nodes.shader.grid.VolumeScatter.phase)     |             |
| [`tree`](#nodebpy.nodes.shader.grid.VolumeScatter.tree)       |             |
| [`type`](#nodebpy.nodes.shader.grid.VolumeScatter.type)       |             |

**Inputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `i.color`       | `ColorSocket` | Color       |
| `i.density`     | `FloatSocket` | Density     |
| `i.anisotropy`  | `FloatSocket` | Anisotropy  |
| `i.ior`         | `FloatSocket` | IOR         |
| `i.backscatter` | `FloatSocket` | Backscatter |
| `i.alpha`       | `FloatSocket` | Alpha       |
| `i.diameter`    | `FloatSocket` | Diameter    |
| `i.weight`      | `FloatSocket` | Weight      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.volume` | `ShaderSocket` | Volume      |
