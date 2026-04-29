# nodes.shader.shader

`shader`

## Classes

| Name | Description |
|----|----|
| [AddShader](#nodebpy.nodes.shader.shader.AddShader) | Add two Shaders together |
| [Background](#nodebpy.nodes.shader.shader.Background) | Add background light emission. |
| [DiffuseBSDF](#nodebpy.nodes.shader.shader.DiffuseBSDF) | Lambertian and Oren-Nayar diffuse reflection |
| [Emission](#nodebpy.nodes.shader.shader.Emission) | Lambertian emission shader |
| [GlassBSDF](#nodebpy.nodes.shader.shader.GlassBSDF) | Glass-like shader mixing refraction and reflection at grazing angles |
| [GlossyBSDF](#nodebpy.nodes.shader.shader.GlossyBSDF) | Reflection with microfacet distribution, used for materials such as metal or mirrors |
| [HairBSDF](#nodebpy.nodes.shader.shader.HairBSDF) | Reflection and transmission shaders optimized for hair rendering |
| [Holdout](#nodebpy.nodes.shader.shader.Holdout) | Create a “hole” in the image with zero alpha transparency, which is useful for compositing. |
| [MetallicBSDF](#nodebpy.nodes.shader.shader.MetallicBSDF) | Metallic reflection with microfacet distribution, and metallic fresnel |
| [MixShader](#nodebpy.nodes.shader.shader.MixShader) | Mix two shaders together. Typically used for material layering |
| [PrincipledBSDF](#nodebpy.nodes.shader.shader.PrincipledBSDF) | Physically-based, easy-to-use shader for rendering surface materials, based on the OpenPBR model |
| [PrincipledHairBSDF](#nodebpy.nodes.shader.shader.PrincipledHairBSDF) | Physically-based, easy-to-use shader for rendering hair and fur |
| [RayPortalBSDF](#nodebpy.nodes.shader.shader.RayPortalBSDF) | Continue tracing from an arbitrary new position and in a new direction |
| [RefractionBSDF](#nodebpy.nodes.shader.shader.RefractionBSDF) | Glossy refraction with sharp or microfacet distribution, typically used for materials that transmit light |
| [SheenBSDF](#nodebpy.nodes.shader.shader.SheenBSDF) | Reflection for materials such as cloth. |
| [SpecularBSDF](#nodebpy.nodes.shader.shader.SpecularBSDF) | Similar to the Principled BSDF node but uses the specular workflow instead of metallic, which functions by specifying the facing (along normal) reflection color. Energy is not conserved, so the result may not be physically accurate |
| [SubsurfaceScattering](#nodebpy.nodes.shader.shader.SubsurfaceScattering) | Subsurface multiple scattering shader to simulate light entering the surface and bouncing internally. |
| [ToonBSDF](#nodebpy.nodes.shader.shader.ToonBSDF) | Diffuse and Glossy shaders with cartoon light effects |
| [TranslucentBSDF](#nodebpy.nodes.shader.shader.TranslucentBSDF) | Lambertian diffuse transmission |
| [TransparentBSDF](#nodebpy.nodes.shader.shader.TransparentBSDF) | Transparency without refraction, passing straight through the surface as if there were no geometry |

### AddShader

``` python
AddShader(shader=None, shader_001=None)
```

Add two Shaders together

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| shader     | InputShader | Shader      | `None`  |
| shader_001 | InputShader | Shader      | `None`  |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.AddShader.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.AddShader.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.AddShader.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.AddShader.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.AddShader.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.AddShader.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.AddShader.type)       |             |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.shader`     | `ShaderSocket` | Shader      |
| `i.shader_001` | `ShaderSocket` | Shader      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.shader` | `ShaderSocket` | Shader      |

### Background

``` python
Background(color=None, strength=1.0, weight=0.0)
```

    Add background light emission.

Note: This node should only be used for the world surface output

#### Parameters

    color : InputColor
        Color
    strength : InputFloat
        Strength
    weight : InputFloat
        Weight

#### Inputs

    i.color : ColorSocket
        Color
    i.strength : FloatSocket
        Strength
    i.weight : FloatSocket
        Weight

#### Outputs

    o.background : ShaderSocket
        Background

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.Background.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.Background.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.Background.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.Background.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.Background.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.Background.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.Background.type)       |             |

### DiffuseBSDF

``` python
DiffuseBSDF(color=None, roughness=0.0, normal=None, weight=0.0)
```

Lambertian and Oren-Nayar diffuse reflection

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| color     | InputColor  | Color       | `None`  |
| roughness | InputFloat  | Roughness   | `0.0`   |
| normal    | InputVector | Normal      | `None`  |
| weight    | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.DiffuseBSDF.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.DiffuseBSDF.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.DiffuseBSDF.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.DiffuseBSDF.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.DiffuseBSDF.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.DiffuseBSDF.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.DiffuseBSDF.type)       |             |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.color`     | `ColorSocket`  | Color       |
| `i.roughness` | `FloatSocket`  | Roughness   |
| `i.normal`    | `VectorSocket` | Normal      |
| `i.weight`    | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### Emission

``` python
Emission(color=None, strength=1.0, weight=0.0)
```

Lambertian emission shader

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| color    | InputColor | Color       | `None`  |
| strength | InputFloat | Strength    | `1.0`   |
| weight   | InputFloat | Weight      | `0.0`   |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.Emission.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.Emission.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.Emission.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.Emission.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.Emission.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.Emission.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.Emission.type)       |             |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.color`    | `ColorSocket` | Color       |
| `i.strength` | `FloatSocket` | Strength    |
| `i.weight`   | `FloatSocket` | Weight      |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.emission` | `ShaderSocket` | Emission    |

### GlassBSDF

``` python
GlassBSDF(
    color=None,
    roughness=0.0,
    ior=1.5,
    normal=None,
    weight=0.0,
    thin_film_thickness=0.0,
    thin_film_ior=1.33,
    *,
    distribution='MULTI_GGX',
)
```

Glass-like shader mixing refraction and reflection at grazing angles

#### Parameters

| Name                | Type        | Description         | Default |
|---------------------|-------------|---------------------|---------|
| color               | InputColor  | Color               | `None`  |
| roughness           | InputFloat  | Roughness           | `0.0`   |
| ior                 | InputFloat  | IOR                 | `1.5`   |
| normal              | InputVector | Normal              | `None`  |
| weight              | InputFloat  | Weight              | `0.0`   |
| thin_film_thickness | InputFloat  | Thin Film Thickness | `0.0`   |
| thin_film_ior       | InputFloat  | Thin Film IOR       | `1.33`  |

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.GlassBSDF.distribution) |  |
| [`i`](#nodebpy.nodes.shader.shader.GlassBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.GlassBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.GlassBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.GlassBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.GlassBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.GlassBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.GlassBSDF.type) |  |

**Inputs**

| Attribute               | Type           | Description         |
|-------------------------|----------------|---------------------|
| `i.color`               | `ColorSocket`  | Color               |
| `i.roughness`           | `FloatSocket`  | Roughness           |
| `i.ior`                 | `FloatSocket`  | IOR                 |
| `i.normal`              | `VectorSocket` | Normal              |
| `i.weight`              | `FloatSocket`  | Weight              |
| `i.thin_film_thickness` | `FloatSocket`  | Thin Film Thickness |
| `i.thin_film_ior`       | `FloatSocket`  | Thin Film IOR       |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### GlossyBSDF

``` python
GlossyBSDF(
    color=None,
    roughness=0.5,
    anisotropy=0.0,
    rotation=0.0,
    normal=None,
    tangent=None,
    weight=0.0,
    *,
    distribution='MULTI_GGX',
)
```

Reflection with microfacet distribution, used for materials such as metal or mirrors

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| color      | InputColor  | Color       | `None`  |
| roughness  | InputFloat  | Roughness   | `0.5`   |
| anisotropy | InputFloat  | Anisotropy  | `0.0`   |
| rotation   | InputFloat  | Rotation    | `0.0`   |
| normal     | InputVector | Normal      | `None`  |
| tangent    | InputVector | Tangent     | `None`  |
| weight     | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.GlossyBSDF.distribution) |  |
| [`i`](#nodebpy.nodes.shader.shader.GlossyBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.GlossyBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.GlossyBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.GlossyBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.GlossyBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.GlossyBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.GlossyBSDF.type) |  |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.color`      | `ColorSocket`  | Color       |
| `i.roughness`  | `FloatSocket`  | Roughness   |
| `i.anisotropy` | `FloatSocket`  | Anisotropy  |
| `i.rotation`   | `FloatSocket`  | Rotation    |
| `i.normal`     | `VectorSocket` | Normal      |
| `i.tangent`    | `VectorSocket` | Tangent     |
| `i.weight`     | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### HairBSDF

``` python
HairBSDF(
    color=None,
    offset=0.0,
    roughnessu=0.1,
    roughnessv=1.0,
    tangent=None,
    weight=0.0,
    *,
    component='Reflection',
)
```

Reflection and transmission shaders optimized for hair rendering

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| color      | InputColor  | Color       | `None`  |
| offset     | InputFloat  | Offset      | `0.0`   |
| roughnessu | InputFloat  | RoughnessU  | `0.1`   |
| roughnessv | InputFloat  | RoughnessV  | `1.0`   |
| tangent    | InputVector | Tangent     | `None`  |
| weight     | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`component`](#nodebpy.nodes.shader.shader.HairBSDF.component) |  |
| [`i`](#nodebpy.nodes.shader.shader.HairBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.HairBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.HairBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.HairBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.HairBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.HairBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.HairBSDF.type) |  |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.color`      | `ColorSocket`  | Color       |
| `i.offset`     | `FloatSocket`  | Offset      |
| `i.roughnessu` | `FloatSocket`  | RoughnessU  |
| `i.roughnessv` | `FloatSocket`  | RoughnessV  |
| `i.tangent`    | `VectorSocket` | Tangent     |
| `i.weight`     | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### Holdout

``` python
Holdout(weight=0.0)
```

    Create a "hole" in the image with zero alpha transparency, which is useful for compositing.

Note: the holdout shader can only create alpha when transparency is enabled in the film settings

#### Parameters

    weight : InputFloat
        Weight

#### Inputs

    i.weight : FloatSocket
        Weight

#### Outputs

    o.holdout : ShaderSocket
        Holdout

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.Holdout.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.Holdout.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.Holdout.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.Holdout.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.Holdout.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.Holdout.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.Holdout.type)       |             |

### MetallicBSDF

``` python
MetallicBSDF(
    base_color=None,
    edge_tint=None,
    ior=None,
    extinction=None,
    roughness=0.5,
    anisotropy=0.0,
    rotation=0.0,
    normal=None,
    tangent=None,
    weight=0.0,
    thin_film_thickness=0.0,
    thin_film_ior=1.33,
    *,
    distribution='MULTI_GGX',
    fresnel_type='F82',
)
```

Metallic reflection with microfacet distribution, and metallic fresnel

#### Parameters

| Name                | Type        | Description         | Default |
|---------------------|-------------|---------------------|---------|
| base_color          | InputColor  | Base Color          | `None`  |
| edge_tint           | InputColor  | Edge Tint           | `None`  |
| ior                 | InputVector | IOR                 | `None`  |
| extinction          | InputVector | Extinction          | `None`  |
| roughness           | InputFloat  | Roughness           | `0.5`   |
| anisotropy          | InputFloat  | Anisotropy          | `0.0`   |
| rotation            | InputFloat  | Rotation            | `0.0`   |
| normal              | InputVector | Normal              | `None`  |
| tangent             | InputVector | Tangent             | `None`  |
| weight              | InputFloat  | Weight              | `0.0`   |
| thin_film_thickness | InputFloat  | Thin Film Thickness | `0.0`   |
| thin_film_ior       | InputFloat  | Thin Film IOR       | `1.33`  |

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.MetallicBSDF.distribution) |  |
| [`fresnel_type`](#nodebpy.nodes.shader.shader.MetallicBSDF.fresnel_type) |  |
| [`i`](#nodebpy.nodes.shader.shader.MetallicBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.MetallicBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.MetallicBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.MetallicBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.MetallicBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.MetallicBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.MetallicBSDF.type) |  |

#### Methods

| Name | Description |
|----|----|
| [f82_tint](#nodebpy.nodes.shader.shader.MetallicBSDF.f82_tint) | Create Metallic BSDF with operation ‘F82 Tint’. An approximation of the Fresnel conductor curve based on the colors at perpendicular and near-grazing (roughly 82°) angles |
| [physical_conductor](#nodebpy.nodes.shader.shader.MetallicBSDF.physical_conductor) | Create Metallic BSDF with operation ‘Physical Conductor’. Fresnel conductor based on the complex refractive index per color channel |

##### f82_tint

``` python
f82_tint(
    base_color=None,
    edge_tint=None,
    roughness=0.5,
    anisotropy=0.0,
    rotation=0.0,
    normal=None,
    tangent=None,
    thin_film_thickness=0.0,
    thin_film_ior=1.33,
)
```

Create Metallic BSDF with operation ‘F82 Tint’. An approximation of the Fresnel conductor curve based on the colors at perpendicular and near-grazing (roughly 82°) angles

##### physical_conductor

``` python
physical_conductor(
    ior=None,
    extinction=None,
    roughness=0.5,
    anisotropy=0.0,
    rotation=0.0,
    normal=None,
    tangent=None,
    thin_film_thickness=0.0,
    thin_film_ior=1.33,
)
```

Create Metallic BSDF with operation ‘Physical Conductor’. Fresnel conductor based on the complex refractive index per color channel

**Inputs**

| Attribute               | Type           | Description         |
|-------------------------|----------------|---------------------|
| `i.base_color`          | `ColorSocket`  | Base Color          |
| `i.edge_tint`           | `ColorSocket`  | Edge Tint           |
| `i.ior`                 | `VectorSocket` | IOR                 |
| `i.extinction`          | `VectorSocket` | Extinction          |
| `i.roughness`           | `FloatSocket`  | Roughness           |
| `i.anisotropy`          | `FloatSocket`  | Anisotropy          |
| `i.rotation`            | `FloatSocket`  | Rotation            |
| `i.normal`              | `VectorSocket` | Normal              |
| `i.tangent`             | `VectorSocket` | Tangent             |
| `i.weight`              | `FloatSocket`  | Weight              |
| `i.thin_film_thickness` | `FloatSocket`  | Thin Film Thickness |
| `i.thin_film_ior`       | `FloatSocket`  | Thin Film IOR       |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### MixShader

``` python
MixShader(fac=0.5, shader=None, shader_001=None)
```

Mix two shaders together. Typically used for material layering

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| fac        | InputFloat  | Factor      | `0.5`   |
| shader     | InputShader | Shader      | `None`  |
| shader_001 | InputShader | Shader      | `None`  |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.shader.MixShader.i)             |             |
| [`name`](#nodebpy.nodes.shader.shader.MixShader.name)       |             |
| [`node`](#nodebpy.nodes.shader.shader.MixShader.node)       |             |
| [`o`](#nodebpy.nodes.shader.shader.MixShader.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.shader.MixShader.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.shader.MixShader.tree)       |             |
| [`type`](#nodebpy.nodes.shader.shader.MixShader.type)       |             |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.fac`        | `FloatSocket`  | Factor      |
| `i.shader`     | `ShaderSocket` | Shader      |
| `i.shader_001` | `ShaderSocket` | Shader      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.shader` | `ShaderSocket` | Shader      |

### PrincipledBSDF

``` python
PrincipledBSDF(
    base_color=None,
    metallic=0.0,
    roughness=0.5,
    ior=1.5,
    alpha=1.0,
    normal=None,
    weight=0.0,
    diffuse_roughness=0.0,
    subsurface_weight=0.0,
    subsurface_radius=None,
    subsurface_scale=0.05,
    subsurface_ior=1.4,
    subsurface_anisotropy=0.0,
    specular_ior_level=0.5,
    specular_tint=None,
    anisotropic=0.0,
    anisotropic_rotation=0.0,
    tangent=None,
    transmission_weight=0.0,
    coat_weight=0.0,
    coat_roughness=0.03,
    coat_ior=1.5,
    coat_tint=None,
    coat_normal=None,
    sheen_weight=0.0,
    sheen_roughness=0.5,
    sheen_tint=None,
    emission_color=None,
    emission_strength=0.0,
    thin_film_thickness=0.0,
    thin_film_ior=1.33,
    *,
    distribution='MULTI_GGX',
    subsurface_method='RANDOM_WALK',
)
```

Physically-based, easy-to-use shader for rendering surface materials, based on the OpenPBR model

#### Parameters

| Name                  | Type        | Description           | Default |
|-----------------------|-------------|-----------------------|---------|
| base_color            | InputColor  | Base Color            | `None`  |
| metallic              | InputFloat  | Metallic              | `0.0`   |
| roughness             | InputFloat  | Roughness             | `0.5`   |
| ior                   | InputFloat  | IOR                   | `1.5`   |
| alpha                 | InputFloat  | Alpha                 | `1.0`   |
| normal                | InputVector | Normal                | `None`  |
| weight                | InputFloat  | Weight                | `0.0`   |
| diffuse_roughness     | InputFloat  | Diffuse Roughness     | `0.0`   |
| subsurface_weight     | InputFloat  | Subsurface Weight     | `0.0`   |
| subsurface_radius     | InputVector | Subsurface Radius     | `None`  |
| subsurface_scale      | InputFloat  | Subsurface Scale      | `0.05`  |
| subsurface_ior        | InputFloat  | Subsurface IOR        | `1.4`   |
| subsurface_anisotropy | InputFloat  | Subsurface Anisotropy | `0.0`   |
| specular_ior_level    | InputFloat  | Specular IOR Level    | `0.5`   |
| specular_tint         | InputColor  | Specular Tint         | `None`  |
| anisotropic           | InputFloat  | Anisotropic           | `0.0`   |
| anisotropic_rotation  | InputFloat  | Anisotropic Rotation  | `0.0`   |
| tangent               | InputVector | Tangent               | `None`  |
| transmission_weight   | InputFloat  | Transmission Weight   | `0.0`   |
| coat_weight           | InputFloat  | Coat Weight           | `0.0`   |
| coat_roughness        | InputFloat  | Coat Roughness        | `0.03`  |
| coat_ior              | InputFloat  | Coat IOR              | `1.5`   |
| coat_tint             | InputColor  | Coat Tint             | `None`  |
| coat_normal           | InputVector | Coat Normal           | `None`  |
| sheen_weight          | InputFloat  | Sheen Weight          | `0.0`   |
| sheen_roughness       | InputFloat  | Sheen Roughness       | `0.5`   |
| sheen_tint            | InputColor  | Sheen Tint            | `None`  |
| emission_color        | InputColor  | Emission Color        | `None`  |
| emission_strength     | InputFloat  | Emission Strength     | `0.0`   |
| thin_film_thickness   | InputFloat  | Thin Film Thickness   | `0.0`   |
| thin_film_ior         | InputFloat  | Thin Film IOR         | `1.33`  |

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.PrincipledBSDF.distribution) |  |
| [`i`](#nodebpy.nodes.shader.shader.PrincipledBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.PrincipledBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.PrincipledBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.PrincipledBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.PrincipledBSDF.outputs) |  |
| [`subsurface_method`](#nodebpy.nodes.shader.shader.PrincipledBSDF.subsurface_method) |  |
| [`tree`](#nodebpy.nodes.shader.shader.PrincipledBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.PrincipledBSDF.type) |  |

**Inputs**

| Attribute                 | Type           | Description           |
|---------------------------|----------------|-----------------------|
| `i.base_color`            | `ColorSocket`  | Base Color            |
| `i.metallic`              | `FloatSocket`  | Metallic              |
| `i.roughness`             | `FloatSocket`  | Roughness             |
| `i.ior`                   | `FloatSocket`  | IOR                   |
| `i.alpha`                 | `FloatSocket`  | Alpha                 |
| `i.normal`                | `VectorSocket` | Normal                |
| `i.weight`                | `FloatSocket`  | Weight                |
| `i.diffuse_roughness`     | `FloatSocket`  | Diffuse Roughness     |
| `i.subsurface_weight`     | `FloatSocket`  | Subsurface Weight     |
| `i.subsurface_radius`     | `VectorSocket` | Subsurface Radius     |
| `i.subsurface_scale`      | `FloatSocket`  | Subsurface Scale      |
| `i.subsurface_ior`        | `FloatSocket`  | Subsurface IOR        |
| `i.subsurface_anisotropy` | `FloatSocket`  | Subsurface Anisotropy |
| `i.specular_ior_level`    | `FloatSocket`  | Specular IOR Level    |
| `i.specular_tint`         | `ColorSocket`  | Specular Tint         |
| `i.anisotropic`           | `FloatSocket`  | Anisotropic           |
| `i.anisotropic_rotation`  | `FloatSocket`  | Anisotropic Rotation  |
| `i.tangent`               | `VectorSocket` | Tangent               |
| `i.transmission_weight`   | `FloatSocket`  | Transmission Weight   |
| `i.coat_weight`           | `FloatSocket`  | Coat Weight           |
| `i.coat_roughness`        | `FloatSocket`  | Coat Roughness        |
| `i.coat_ior`              | `FloatSocket`  | Coat IOR              |
| `i.coat_tint`             | `ColorSocket`  | Coat Tint             |
| `i.coat_normal`           | `VectorSocket` | Coat Normal           |
| `i.sheen_weight`          | `FloatSocket`  | Sheen Weight          |
| `i.sheen_roughness`       | `FloatSocket`  | Sheen Roughness       |
| `i.sheen_tint`            | `ColorSocket`  | Sheen Tint            |
| `i.emission_color`        | `ColorSocket`  | Emission Color        |
| `i.emission_strength`     | `FloatSocket`  | Emission Strength     |
| `i.thin_film_thickness`   | `FloatSocket`  | Thin Film Thickness   |
| `i.thin_film_ior`         | `FloatSocket`  | Thin Film IOR         |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### PrincipledHairBSDF

``` python
PrincipledHairBSDF(
    color=None,
    melanin=0.8,
    melanin_redness=1.0,
    tint=None,
    absorption_coefficient=None,
    aspect_ratio=0.85,
    roughness=0.3,
    radial_roughness=0.3,
    coat=0.0,
    ior=1.55,
    offset=0.0349,
    random_color=0.0,
    random_roughness=0.0,
    random=0.0,
    weight=0.0,
    r_lobe=1.0,
    tt_lobe=1.0,
    trt_lobe=1.0,
    *,
    model='CHIANG',
    parametrization='COLOR',
)
```

Physically-based, easy-to-use shader for rendering hair and fur

#### Parameters

| Name                   | Type        | Description            | Default  |
|------------------------|-------------|------------------------|----------|
| color                  | InputColor  | Color                  | `None`   |
| melanin                | InputFloat  | Melanin                | `0.8`    |
| melanin_redness        | InputFloat  | Melanin Redness        | `1.0`    |
| tint                   | InputColor  | Tint                   | `None`   |
| absorption_coefficient | InputVector | Absorption Coefficient | `None`   |
| aspect_ratio           | InputFloat  | Aspect Ratio           | `0.85`   |
| roughness              | InputFloat  | Roughness              | `0.3`    |
| radial_roughness       | InputFloat  | Radial Roughness       | `0.3`    |
| coat                   | InputFloat  | Coat                   | `0.0`    |
| ior                    | InputFloat  | IOR                    | `1.55`   |
| offset                 | InputFloat  | Offset                 | `0.0349` |
| random_color           | InputFloat  | Random Color           | `0.0`    |
| random_roughness       | InputFloat  | Random Roughness       | `0.0`    |
| random                 | InputFloat  | Random                 | `0.0`    |
| weight                 | InputFloat  | Weight                 | `0.0`    |
| r_lobe                 | InputFloat  | Reflection             | `1.0`    |
| tt_lobe                | InputFloat  | Transmission           | `1.0`    |
| trt_lobe               | InputFloat  | Secondary Reflection   | `1.0`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.i) |  |
| [`model`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.model) |  |
| [`name`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.outputs) |  |
| [`parametrization`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.parametrization) |  |
| [`tree`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.PrincipledHairBSDF.type) |  |

**Inputs**

| Attribute                  | Type           | Description            |
|----------------------------|----------------|------------------------|
| `i.color`                  | `ColorSocket`  | Color                  |
| `i.melanin`                | `FloatSocket`  | Melanin                |
| `i.melanin_redness`        | `FloatSocket`  | Melanin Redness        |
| `i.tint`                   | `ColorSocket`  | Tint                   |
| `i.absorption_coefficient` | `VectorSocket` | Absorption Coefficient |
| `i.aspect_ratio`           | `FloatSocket`  | Aspect Ratio           |
| `i.roughness`              | `FloatSocket`  | Roughness              |
| `i.radial_roughness`       | `FloatSocket`  | Radial Roughness       |
| `i.coat`                   | `FloatSocket`  | Coat                   |
| `i.ior`                    | `FloatSocket`  | IOR                    |
| `i.offset`                 | `FloatSocket`  | Offset                 |
| `i.random_color`           | `FloatSocket`  | Random Color           |
| `i.random_roughness`       | `FloatSocket`  | Random Roughness       |
| `i.random`                 | `FloatSocket`  | Random                 |
| `i.weight`                 | `FloatSocket`  | Weight                 |
| `i.r_lobe`                 | `FloatSocket`  | Reflection             |
| `i.tt_lobe`                | `FloatSocket`  | Transmission           |
| `i.trt_lobe`               | `FloatSocket`  | Secondary Reflection   |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### RayPortalBSDF

``` python
RayPortalBSDF(color=None, position=None, direction=None, weight=0.0)
```

Continue tracing from an arbitrary new position and in a new direction

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| color     | InputColor  | Color       | `None`  |
| position  | InputVector | Position    | `None`  |
| direction | InputVector | Direction   | `None`  |
| weight    | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.shader.RayPortalBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.RayPortalBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.RayPortalBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.RayPortalBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.RayPortalBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.RayPortalBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.RayPortalBSDF.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.color`     | `ColorSocket`  | Color       |
| `i.position`  | `VectorSocket` | Position    |
| `i.direction` | `VectorSocket` | Direction   |
| `i.weight`    | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### RefractionBSDF

``` python
RefractionBSDF(
    color=None,
    roughness=0.0,
    ior=1.45,
    normal=None,
    weight=0.0,
    *,
    distribution='BECKMANN',
)
```

Glossy refraction with sharp or microfacet distribution, typically used for materials that transmit light

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| color     | InputColor  | Color       | `None`  |
| roughness | InputFloat  | Roughness   | `0.0`   |
| ior       | InputFloat  | IOR         | `1.45`  |
| normal    | InputVector | Normal      | `None`  |
| weight    | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.RefractionBSDF.distribution) |  |
| [`i`](#nodebpy.nodes.shader.shader.RefractionBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.RefractionBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.RefractionBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.RefractionBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.RefractionBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.RefractionBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.RefractionBSDF.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.color`     | `ColorSocket`  | Color       |
| `i.roughness` | `FloatSocket`  | Roughness   |
| `i.ior`       | `FloatSocket`  | IOR         |
| `i.normal`    | `VectorSocket` | Normal      |
| `i.weight`    | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### SheenBSDF

``` python
SheenBSDF(
    color=None,
    roughness=0.5,
    normal=None,
    weight=0.0,
    *,
    distribution='MICROFIBER',
)
```

    Reflection for materials such as cloth.

Typically mixed with other shaders (such as a Diffuse Shader) and is not particularly useful on its own

#### Parameters

    color : InputColor
        Color
    roughness : InputFloat
        Roughness
    normal : InputVector
        Normal
    weight : InputFloat
        Weight

#### Inputs

    i.color : ColorSocket
        Color
    i.roughness : FloatSocket
        Roughness
    i.normal : VectorSocket
        Normal
    i.weight : FloatSocket
        Weight

#### Outputs

    o.bsdf : ShaderSocket
        BSDF

#### Attributes

| Name | Description |
|----|----|
| [`distribution`](#nodebpy.nodes.shader.shader.SheenBSDF.distribution) |  |
| [`i`](#nodebpy.nodes.shader.shader.SheenBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.SheenBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.SheenBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.SheenBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.SheenBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.SheenBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.SheenBSDF.type) |  |

### SpecularBSDF

``` python
SpecularBSDF(
    base_color=None,
    specular=None,
    roughness=0.2,
    emissive_color=None,
    transparency=0.0,
    normal=None,
    clear_coat=0.0,
    clear_coat_roughness=0.0,
    clear_coat_normal=None,
    weight=0.0,
)
```

Similar to the Principled BSDF node but uses the specular workflow instead of metallic, which functions by specifying the facing (along normal) reflection color. Energy is not conserved, so the result may not be physically accurate

#### Parameters

| Name                 | Type        | Description          | Default |
|----------------------|-------------|----------------------|---------|
| base_color           | InputColor  | Base Color           | `None`  |
| specular             | InputColor  | Specular             | `None`  |
| roughness            | InputFloat  | Roughness            | `0.2`   |
| emissive_color       | InputColor  | Emissive Color       | `None`  |
| transparency         | InputFloat  | Transparency         | `0.0`   |
| normal               | InputVector | Normal               | `None`  |
| clear_coat           | InputFloat  | Clear Coat           | `0.0`   |
| clear_coat_roughness | InputFloat  | Clear Coat Roughness | `0.0`   |
| clear_coat_normal    | InputVector | Clear Coat Normal    | `None`  |
| weight               | InputFloat  | Weight               | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.shader.SpecularBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.SpecularBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.SpecularBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.SpecularBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.SpecularBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.SpecularBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.SpecularBSDF.type) |  |

**Inputs**

| Attribute                | Type           | Description          |
|--------------------------|----------------|----------------------|
| `i.base_color`           | `ColorSocket`  | Base Color           |
| `i.specular`             | `ColorSocket`  | Specular             |
| `i.roughness`            | `FloatSocket`  | Roughness            |
| `i.emissive_color`       | `ColorSocket`  | Emissive Color       |
| `i.transparency`         | `FloatSocket`  | Transparency         |
| `i.normal`               | `VectorSocket` | Normal               |
| `i.clear_coat`           | `FloatSocket`  | Clear Coat           |
| `i.clear_coat_roughness` | `FloatSocket`  | Clear Coat Roughness |
| `i.clear_coat_normal`    | `VectorSocket` | Clear Coat Normal    |
| `i.weight`               | `FloatSocket`  | Weight               |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### SubsurfaceScattering

``` python
SubsurfaceScattering(
    color=None,
    scale=0.05,
    radius=None,
    ior=1.4,
    roughness=1.0,
    anisotropy=0.0,
    normal=None,
    weight=0.0,
    *,
    falloff='RANDOM_WALK',
)
```

    Subsurface multiple scattering shader to simulate light entering the surface and bouncing internally.

Typically used for materials such as skin, wax, marble or milk

#### Parameters

    color : InputColor
        Color
    scale : InputFloat
        Scale
    radius : InputVector
        Radius
    ior : InputFloat
        IOR
    roughness : InputFloat
        Roughness
    anisotropy : InputFloat
        Anisotropy
    normal : InputVector
        Normal
    weight : InputFloat
        Weight

#### Inputs

    i.color : ColorSocket
        Color
    i.scale : FloatSocket
        Scale
    i.radius : VectorSocket
        Radius
    i.ior : FloatSocket
        IOR
    i.roughness : FloatSocket
        Roughness
    i.anisotropy : FloatSocket
        Anisotropy
    i.normal : VectorSocket
        Normal
    i.weight : FloatSocket
        Weight

#### Outputs

    o.bssrdf : ShaderSocket
        BSSRDF

#### Attributes

| Name | Description |
|----|----|
| [`falloff`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.falloff) |  |
| [`i`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.SubsurfaceScattering.type) |  |

### ToonBSDF

``` python
ToonBSDF(
    color=None,
    size=0.5,
    smooth=0.0,
    normal=None,
    weight=0.0,
    *,
    component='DIFFUSE',
)
```

Diffuse and Glossy shaders with cartoon light effects

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| color  | InputColor  | Color       | `None`  |
| size   | InputFloat  | Size        | `0.5`   |
| smooth | InputFloat  | Smooth      | `0.0`   |
| normal | InputVector | Normal      | `None`  |
| weight | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`component`](#nodebpy.nodes.shader.shader.ToonBSDF.component) |  |
| [`i`](#nodebpy.nodes.shader.shader.ToonBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.ToonBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.ToonBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.ToonBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.ToonBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.ToonBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.ToonBSDF.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.color`  | `ColorSocket`  | Color       |
| `i.size`   | `FloatSocket`  | Size        |
| `i.smooth` | `FloatSocket`  | Smooth      |
| `i.normal` | `VectorSocket` | Normal      |
| `i.weight` | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### TranslucentBSDF

``` python
TranslucentBSDF(color=None, normal=None, weight=0.0)
```

Lambertian diffuse transmission

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| color  | InputColor  | Color       | `None`  |
| normal | InputVector | Normal      | `None`  |
| weight | InputFloat  | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.shader.TranslucentBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.TranslucentBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.TranslucentBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.TranslucentBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.TranslucentBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.TranslucentBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.TranslucentBSDF.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.color`  | `ColorSocket`  | Color       |
| `i.normal` | `VectorSocket` | Normal      |
| `i.weight` | `FloatSocket`  | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |

### TransparentBSDF

``` python
TransparentBSDF(color=None, weight=0.0)
```

Transparency without refraction, passing straight through the surface as if there were no geometry

#### Parameters

| Name   | Type       | Description | Default |
|--------|------------|-------------|---------|
| color  | InputColor | Color       | `None`  |
| weight | InputFloat | Weight      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.shader.TransparentBSDF.i) |  |
| [`name`](#nodebpy.nodes.shader.shader.TransparentBSDF.name) |  |
| [`node`](#nodebpy.nodes.shader.shader.TransparentBSDF.node) |  |
| [`o`](#nodebpy.nodes.shader.shader.TransparentBSDF.o) |  |
| [`outputs`](#nodebpy.nodes.shader.shader.TransparentBSDF.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.shader.TransparentBSDF.tree) |  |
| [`type`](#nodebpy.nodes.shader.shader.TransparentBSDF.type) |  |

**Inputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `i.color`  | `ColorSocket` | Color       |
| `i.weight` | `FloatSocket` | Weight      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.bsdf`  | `ShaderSocket` | BSDF        |
