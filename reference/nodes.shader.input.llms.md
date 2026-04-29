# nodes.shader.input

`input`

## Classes

| Name | Description |
|----|----|
| [AmbientOcclusion](#nodebpy.nodes.shader.input.AmbientOcclusion) | Compute how much the hemisphere above the shading point is occluded, for example to add weathering effects to corners. |
| [Bevel](#nodebpy.nodes.shader.input.Bevel) | Generates normals with round corners. |
| [CameraData](#nodebpy.nodes.shader.input.CameraData) | Retrieve information about the camera and how it relates to the current shading point’s position |
| [Color](#nodebpy.nodes.shader.input.Color) | A color picker |
| [ColorAttribute](#nodebpy.nodes.shader.input.ColorAttribute) | Retrieve a color attribute, or the default fallback if none is specified |
| [CurvesInfo](#nodebpy.nodes.shader.input.CurvesInfo) | Retrieve hair curve information |
| [Fresnel](#nodebpy.nodes.shader.input.Fresnel) | Produce a blending factor depending on the angle between the surface normal and the view direction using Fresnel equations. |
| [Geometry](#nodebpy.nodes.shader.input.Geometry) | Retrieve geometric information about the current shading point |
| [LayerWeight](#nodebpy.nodes.shader.input.LayerWeight) | Produce a blending factor depending on the angle between the surface normal and the view direction. |
| [LightPath](#nodebpy.nodes.shader.input.LightPath) | Retrieve the type of incoming ray for which the shader is being executed. |
| [ObjectInfo](#nodebpy.nodes.shader.input.ObjectInfo) | Retrieve information about the object instance |
| [ParticleInfo](#nodebpy.nodes.shader.input.ParticleInfo) | Retrieve the data of the particle that spawned the object instance, for example to give variation to multiple instances of an object |
| [PointInfo](#nodebpy.nodes.shader.input.PointInfo) | Retrieve information about points in a point cloud |
| [Raycast](#nodebpy.nodes.shader.input.Raycast) | Cast rays and retrieve information from the hit point |
| [Tangent](#nodebpy.nodes.shader.input.Tangent) | Generate a tangent direction for the Anisotropic BSDF |
| [TextureCoordinate](#nodebpy.nodes.shader.input.TextureCoordinate) | Retrieve multiple types of texture coordinates. |
| [UVAlongStroke](#nodebpy.nodes.shader.input.UVAlongStroke) | UV coordinates that map a texture along the stroke length |
| [UVMap](#nodebpy.nodes.shader.input.UVMap) | Retrieve a UV map from the geometry, or the default fallback if none is specified |
| [Wireframe](#nodebpy.nodes.shader.input.Wireframe) | Retrieve the edges of an object as it appears to Cycles. |

### AmbientOcclusion

``` python
AmbientOcclusion(
    color=None,
    distance=1.0,
    normal=None,
    *,
    samples=0,
    inside=False,
    only_local=False,
)
```

    Compute how much the hemisphere above the shading point is occluded, for example to add weathering effects to corners.

Note: For Cycles, this may slow down renders significantly

#### Parameters

    color : InputColor
        Color
    distance : InputFloat
        Distance
    normal : InputVector
        Normal

#### Inputs

    i.color : ColorSocket
        Color
    i.distance : FloatSocket
        Distance
    i.normal : VectorSocket
        Normal

#### Outputs

    o.color : ColorSocket
        Color
    o.ao : FloatSocket
        AO

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.AmbientOcclusion.i) |  |
| [`inside`](#nodebpy.nodes.shader.input.AmbientOcclusion.inside) |  |
| [`name`](#nodebpy.nodes.shader.input.AmbientOcclusion.name) |  |
| [`node`](#nodebpy.nodes.shader.input.AmbientOcclusion.node) |  |
| [`o`](#nodebpy.nodes.shader.input.AmbientOcclusion.o) |  |
| [`only_local`](#nodebpy.nodes.shader.input.AmbientOcclusion.only_local) |  |
| [`outputs`](#nodebpy.nodes.shader.input.AmbientOcclusion.outputs) |  |
| [`samples`](#nodebpy.nodes.shader.input.AmbientOcclusion.samples) |  |
| [`tree`](#nodebpy.nodes.shader.input.AmbientOcclusion.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.AmbientOcclusion.type) |  |

### Bevel

``` python
Bevel(radius=0.05, normal=None, *, samples=0)
```

    Generates normals with round corners.

Note: only supported in Cycles, and may slow down renders

#### Parameters

    radius : InputFloat
        Radius
    normal : InputVector
        Normal

#### Inputs

    i.radius : FloatSocket
        Radius
    i.normal : VectorSocket
        Normal

#### Outputs

    o.normal : VectorSocket
        Normal

#### Attributes

| Name                                                   | Description |
|--------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.Bevel.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.Bevel.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.Bevel.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.Bevel.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.Bevel.outputs) |             |
| [`samples`](#nodebpy.nodes.shader.input.Bevel.samples) |             |
| [`tree`](#nodebpy.nodes.shader.input.Bevel.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.Bevel.type)       |             |

### CameraData

``` python
CameraData()
```

Retrieve information about the camera and how it relates to the current shading point’s position

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.CameraData.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.CameraData.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.CameraData.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.CameraData.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.CameraData.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.CameraData.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.CameraData.type)       |             |

**Outputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `o.view_vector`   | `VectorSocket` | View Vector   |
| `o.view_z_depth`  | `FloatSocket`  | View Z Depth  |
| `o.view_distance` | `FloatSocket`  | View Distance |

### Color

``` python
Color()
```

A color picker

#### Attributes

| Name                                                   | Description |
|--------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.Color.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.Color.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.Color.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.Color.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.Color.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.Color.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.Color.type)       |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### ColorAttribute

``` python
ColorAttribute(layer_name='')
```

Retrieve a color attribute, or the default fallback if none is specified

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.ColorAttribute.i) |  |
| [`layer_name`](#nodebpy.nodes.shader.input.ColorAttribute.layer_name) |  |
| [`name`](#nodebpy.nodes.shader.input.ColorAttribute.name) |  |
| [`node`](#nodebpy.nodes.shader.input.ColorAttribute.node) |  |
| [`o`](#nodebpy.nodes.shader.input.ColorAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.ColorAttribute.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.ColorAttribute.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.ColorAttribute.type) |  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |
| `o.alpha` | `FloatSocket` | Alpha       |

### CurvesInfo

``` python
CurvesInfo()
```

Retrieve hair curve information

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.CurvesInfo.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.CurvesInfo.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.CurvesInfo.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.CurvesInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.CurvesInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.CurvesInfo.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.CurvesInfo.type)       |             |

**Outputs**

| Attribute          | Type           | Description    |
|--------------------|----------------|----------------|
| `o.is_strand`      | `FloatSocket`  | Is Strand      |
| `o.intercept`      | `FloatSocket`  | Intercept      |
| `o.length`         | `FloatSocket`  | Length         |
| `o.thickness`      | `FloatSocket`  | Thickness      |
| `o.tangent_normal` | `VectorSocket` | Tangent Normal |
| `o.random`         | `FloatSocket`  | Random         |

### Fresnel

``` python
Fresnel(ior=1.5, normal=None)
```

    Produce a blending factor depending on the angle between the surface normal and the view direction using Fresnel equations.

Typically used for mixing reflections at grazing angles

#### Parameters

    ior : InputFloat
        IOR
    normal : InputVector
        Normal

#### Inputs

    i.ior : FloatSocket
        IOR
    i.normal : VectorSocket
        Normal

#### Outputs

    o.fac : FloatSocket
        Factor

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.Fresnel.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.Fresnel.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.Fresnel.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.Fresnel.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.Fresnel.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.Fresnel.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.Fresnel.type)       |             |

### Geometry

``` python
Geometry()
```

Retrieve geometric information about the current shading point

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.Geometry.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.Geometry.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.Geometry.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.Geometry.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.Geometry.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.Geometry.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.Geometry.type)       |             |

**Outputs**

| Attribute             | Type           | Description       |
|-----------------------|----------------|-------------------|
| `o.position`          | `VectorSocket` | Position          |
| `o.normal`            | `VectorSocket` | Normal            |
| `o.tangent`           | `VectorSocket` | Tangent           |
| `o.true_normal`       | `VectorSocket` | True Normal       |
| `o.incoming`          | `VectorSocket` | Incoming          |
| `o.parametric`        | `VectorSocket` | Parametric        |
| `o.backfacing`        | `FloatSocket`  | Backfacing        |
| `o.pointiness`        | `FloatSocket`  | Pointiness        |
| `o.random_per_island` | `FloatSocket`  | Random Per Island |

### LayerWeight

``` python
LayerWeight(blend=0.5, normal=None)
```

    Produce a blending factor depending on the angle between the surface normal and the view direction.

Typically used for layering shaders with the Mix Shader node

#### Parameters

    blend : InputFloat
        Blend
    normal : InputVector
        Normal

#### Inputs

    i.blend : FloatSocket
        Blend
    i.normal : VectorSocket
        Normal

#### Outputs

    o.fresnel : FloatSocket
        Fresnel
    o.facing : FloatSocket
        Facing

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.LayerWeight.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.LayerWeight.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.LayerWeight.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.LayerWeight.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.LayerWeight.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.LayerWeight.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.LayerWeight.type)       |             |

### LightPath

``` python
LightPath()
```

    Retrieve the type of incoming ray for which the shader is being executed.

Typically used for non-physically-based tricks

#### Outputs

    o.is_camera_ray : FloatSocket
        Is Camera Ray
    o.is_shadow_ray : FloatSocket
        Is Shadow Ray
    o.is_diffuse_ray : FloatSocket
        Is Diffuse Ray
    o.is_glossy_ray : FloatSocket
        Is Glossy Ray
    o.is_singular_ray : FloatSocket
        Is Singular Ray
    o.is_reflection_ray : FloatSocket
        Is Reflection Ray
    o.is_transmission_ray : FloatSocket
        Is Transmission Ray
    o.is_volume_scatter_ray : FloatSocket
        Is Volume Scatter Ray
    o.ray_length : FloatSocket
        Ray Length
    o.ray_depth : FloatSocket
        Ray Depth
    o.diffuse_depth : FloatSocket
        Diffuse Depth
    o.glossy_depth : FloatSocket
        Glossy Depth
    o.transparent_depth : FloatSocket
        Transparent Depth
    o.transmission_depth : FloatSocket
        Transmission Depth
    o.portal_depth : FloatSocket
        Portal Depth

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.LightPath.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.LightPath.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.LightPath.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.LightPath.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.LightPath.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.LightPath.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.LightPath.type)       |             |

### ObjectInfo

``` python
ObjectInfo()
```

Retrieve information about the object instance

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.ObjectInfo.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.ObjectInfo.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.ObjectInfo.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.ObjectInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.ObjectInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.ObjectInfo.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.ObjectInfo.type)       |             |

**Outputs**

| Attribute          | Type           | Description    |
|--------------------|----------------|----------------|
| `o.location`       | `VectorSocket` | Location       |
| `o.color`          | `ColorSocket`  | Color          |
| `o.alpha`          | `FloatSocket`  | Alpha          |
| `o.object_index`   | `FloatSocket`  | Object Index   |
| `o.material_index` | `FloatSocket`  | Material Index |
| `o.random`         | `FloatSocket`  | Random         |

### ParticleInfo

``` python
ParticleInfo()
```

Retrieve the data of the particle that spawned the object instance, for example to give variation to multiple instances of an object

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.ParticleInfo.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.ParticleInfo.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.ParticleInfo.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.ParticleInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.ParticleInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.ParticleInfo.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.ParticleInfo.type)       |             |

**Outputs**

| Attribute            | Type           | Description      |
|----------------------|----------------|------------------|
| `o.index`            | `FloatSocket`  | Index            |
| `o.random`           | `FloatSocket`  | Random           |
| `o.age`              | `FloatSocket`  | Age              |
| `o.lifetime`         | `FloatSocket`  | Lifetime         |
| `o.location`         | `VectorSocket` | Location         |
| `o.size`             | `FloatSocket`  | Size             |
| `o.velocity`         | `VectorSocket` | Velocity         |
| `o.angular_velocity` | `VectorSocket` | Angular Velocity |

### PointInfo

``` python
PointInfo()
```

Retrieve information about points in a point cloud

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.input.PointInfo.i)             |             |
| [`name`](#nodebpy.nodes.shader.input.PointInfo.name)       |             |
| [`node`](#nodebpy.nodes.shader.input.PointInfo.node)       |             |
| [`o`](#nodebpy.nodes.shader.input.PointInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.input.PointInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.input.PointInfo.tree)       |             |
| [`type`](#nodebpy.nodes.shader.input.PointInfo.type)       |             |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.position` | `VectorSocket` | Position    |
| `o.radius`   | `FloatSocket`  | Radius      |
| `o.random`   | `FloatSocket`  | Random      |

### Raycast

``` python
Raycast(position=None, direction=None, length=1.0, *, only_local=False)
```

Cast rays and retrieve information from the hit point

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| position  | InputVector | Position    | `None`  |
| direction | InputVector | Direction   | `None`  |
| length    | InputFloat  | Length      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Raycast.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Raycast.name) |  |
| [`node`](#nodebpy.nodes.shader.input.Raycast.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Raycast.o) |  |
| [`only_local`](#nodebpy.nodes.shader.input.Raycast.only_local) |  |
| [`outputs`](#nodebpy.nodes.shader.input.Raycast.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.Raycast.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.Raycast.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.position`  | `VectorSocket` | Position    |
| `i.direction` | `VectorSocket` | Direction   |
| `i.length`    | `FloatSocket`  | Length      |

**Outputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `o.is_hit`       | `FloatSocket`  | Is Hit       |
| `o.self_hit`     | `FloatSocket`  | Self Hit     |
| `o.hit_distance` | `FloatSocket`  | Hit Distance |
| `o.hit_position` | `VectorSocket` | Hit Position |
| `o.hit_normal`   | `VectorSocket` | Hit Normal   |

### Tangent

``` python
Tangent(direction_type='RADIAL', axis='Z', uv_map='')
```

Generate a tangent direction for the Anisotropic BSDF

#### Attributes

| Name | Description |
|----|----|
| [`axis`](#nodebpy.nodes.shader.input.Tangent.axis) |  |
| [`direction_type`](#nodebpy.nodes.shader.input.Tangent.direction_type) |  |
| [`i`](#nodebpy.nodes.shader.input.Tangent.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Tangent.name) |  |
| [`node`](#nodebpy.nodes.shader.input.Tangent.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Tangent.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.Tangent.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.Tangent.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.Tangent.type) |  |
| [`uv_map`](#nodebpy.nodes.shader.input.Tangent.uv_map) |  |

**Outputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `o.tangent` | `VectorSocket` | Tangent     |

### TextureCoordinate

``` python
TextureCoordinate(from_instancer=False)
```

    Retrieve multiple types of texture coordinates.

Typically used as inputs for texture nodes

#### Outputs

    o.generated : VectorSocket
        Generated
    o.normal : VectorSocket
        Normal
    o.uv : VectorSocket
        UV
    o.object : VectorSocket
        Object
    o.camera : VectorSocket
        Camera
    o.window : VectorSocket
        Window
    o.reflection : VectorSocket
        Reflection

#### Attributes

| Name | Description |
|----|----|
| [`from_instancer`](#nodebpy.nodes.shader.input.TextureCoordinate.from_instancer) |  |
| [`i`](#nodebpy.nodes.shader.input.TextureCoordinate.i) |  |
| [`name`](#nodebpy.nodes.shader.input.TextureCoordinate.name) |  |
| [`node`](#nodebpy.nodes.shader.input.TextureCoordinate.node) |  |
| [`o`](#nodebpy.nodes.shader.input.TextureCoordinate.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.TextureCoordinate.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.TextureCoordinate.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.TextureCoordinate.type) |  |

### UVAlongStroke

``` python
UVAlongStroke(use_tips=False)
```

UV coordinates that map a texture along the stroke length

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.UVAlongStroke.i) |  |
| [`name`](#nodebpy.nodes.shader.input.UVAlongStroke.name) |  |
| [`node`](#nodebpy.nodes.shader.input.UVAlongStroke.node) |  |
| [`o`](#nodebpy.nodes.shader.input.UVAlongStroke.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.UVAlongStroke.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.UVAlongStroke.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.UVAlongStroke.type) |  |
| [`use_tips`](#nodebpy.nodes.shader.input.UVAlongStroke.use_tips) |  |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### UVMap

``` python
UVMap(from_instancer=False, uv_map='')
```

Retrieve a UV map from the geometry, or the default fallback if none is specified

#### Attributes

| Name | Description |
|----|----|
| [`from_instancer`](#nodebpy.nodes.shader.input.UVMap.from_instancer) |  |
| [`i`](#nodebpy.nodes.shader.input.UVMap.i) |  |
| [`name`](#nodebpy.nodes.shader.input.UVMap.name) |  |
| [`node`](#nodebpy.nodes.shader.input.UVMap.node) |  |
| [`o`](#nodebpy.nodes.shader.input.UVMap.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.UVMap.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.UVMap.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.UVMap.type) |  |
| [`uv_map`](#nodebpy.nodes.shader.input.UVMap.uv_map) |  |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### Wireframe

``` python
Wireframe(size=0.01, *, use_pixel_size=False)
```

    Retrieve the edges of an object as it appears to Cycles.

Note: as meshes are triangulated before being processed by Cycles, topology will always appear triangulated

#### Parameters

    size : InputFloat
        Size

#### Inputs

    i.size : FloatSocket
        Size

#### Outputs

    o.fac : FloatSocket
        Factor

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Wireframe.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Wireframe.name) |  |
| [`node`](#nodebpy.nodes.shader.input.Wireframe.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Wireframe.o) |  |
| [`outputs`](#nodebpy.nodes.shader.input.Wireframe.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.input.Wireframe.tree) |  |
| [`type`](#nodebpy.nodes.shader.input.Wireframe.type) |  |
| [`use_pixel_size`](#nodebpy.nodes.shader.input.Wireframe.use_pixel_size) |  |
