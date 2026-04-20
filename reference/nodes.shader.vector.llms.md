# nodes.shader.vector

`vector`

## Classes

| Name | Description |
|----|----|
| [Bump](#nodebpy.nodes.shader.vector.Bump) | Generate a perturbed normal from a height texture for bump mapping. Typically used for faking highly detailed surfaces |
| [Displacement](#nodebpy.nodes.shader.vector.Displacement) | Displace the surface along the surface normal |
| [Mapping](#nodebpy.nodes.shader.vector.Mapping) | Transform the input vector by applying translation, rotation, and scale |
| [Normal](#nodebpy.nodes.shader.vector.Normal) | Generate a normal vector and a dot product |
| [NormalMap](#nodebpy.nodes.shader.vector.NormalMap) | Generate a perturbed normal from an RGB normal map image. Typically used for faking highly detailed surfaces |
| [VectorDisplacement](#nodebpy.nodes.shader.vector.VectorDisplacement) | Displace the surface along an arbitrary direction |
| [VectorTransform](#nodebpy.nodes.shader.vector.VectorTransform) | Convert a vector, point, or normal between world, camera, and object coordinate space |

### Bump

``` python
Bump(
    strength=1.0,
    distance=0.001,
    filter_width=0.1,
    height=1.0,
    normal=None,
    *,
    invert=False,
)
```

Generate a perturbed normal from a height texture for bump mapping. Typically used for faking highly detailed surfaces

#### Parameters

| Name         | Type        | Description  | Default |
|--------------|-------------|--------------|---------|
| strength     | InputFloat  | Strength     | `1.0`   |
| distance     | InputFloat  | Distance     | `0.001` |
| filter_width | InputFloat  | Filter Width | `0.1`   |
| height       | InputFloat  | Height       | `1.0`   |
| normal       | InputVector | Normal       | `None`  |

#### Attributes

| Name                                                   | Description |
|--------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.vector.Bump.i)             |             |
| [`inputs`](#nodebpy.nodes.shader.vector.Bump.inputs)   |             |
| [`invert`](#nodebpy.nodes.shader.vector.Bump.invert)   |             |
| [`name`](#nodebpy.nodes.shader.vector.Bump.name)       |             |
| [`node`](#nodebpy.nodes.shader.vector.Bump.node)       |             |
| [`o`](#nodebpy.nodes.shader.vector.Bump.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.vector.Bump.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.vector.Bump.tree)       |             |
| [`type`](#nodebpy.nodes.shader.vector.Bump.type)       |             |

**Inputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `i.strength`     | `FloatSocket`  | Strength     |
| `i.distance`     | `FloatSocket`  | Distance     |
| `i.filter_width` | `FloatSocket`  | Filter Width |
| `i.height`       | `FloatSocket`  | Height       |
| `i.normal`       | `VectorSocket` | Normal       |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.normal` | `VectorSocket` | Normal      |

### Displacement

``` python
Displacement(
    height=0.0,
    midlevel=0.5,
    scale=0.01,
    normal=None,
    *,
    space='OBJECT',
)
```

Displace the surface along the surface normal

#### Parameters

| Name     | Type        | Description | Default |
|----------|-------------|-------------|---------|
| height   | InputFloat  | Height      | `0.0`   |
| midlevel | InputFloat  | Midlevel    | `0.5`   |
| scale    | InputFloat  | Scale       | `0.01`  |
| normal   | InputVector | Normal      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Displacement.i) |  |
| [`inputs`](#nodebpy.nodes.shader.vector.Displacement.inputs) |  |
| [`name`](#nodebpy.nodes.shader.vector.Displacement.name) |  |
| [`node`](#nodebpy.nodes.shader.vector.Displacement.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Displacement.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Displacement.outputs) |  |
| [`space`](#nodebpy.nodes.shader.vector.Displacement.space) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Displacement.tree) |  |
| [`type`](#nodebpy.nodes.shader.vector.Displacement.type) |  |

**Inputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.height`   | `FloatSocket`  | Height      |
| `i.midlevel` | `FloatSocket`  | Midlevel    |
| `i.scale`    | `FloatSocket`  | Scale       |
| `i.normal`   | `VectorSocket` | Normal      |

**Outputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `o.displacement` | `VectorSocket` | Displacement |

### Mapping

``` python
Mapping(
    vector=None,
    location=None,
    rotation=None,
    scale=None,
    *,
    vector_type='POINT',
)
```

Transform the input vector by applying translation, rotation, and scale

#### Parameters

| Name     | Type        | Description | Default |
|----------|-------------|-------------|---------|
| vector   | InputVector | Vector      | `None`  |
| location | InputVector | Location    | `None`  |
| rotation | InputVector | Rotation    | `None`  |
| scale    | InputVector | Scale       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Mapping.i) |  |
| [`inputs`](#nodebpy.nodes.shader.vector.Mapping.inputs) |  |
| [`name`](#nodebpy.nodes.shader.vector.Mapping.name) |  |
| [`node`](#nodebpy.nodes.shader.vector.Mapping.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Mapping.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Mapping.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Mapping.tree) |  |
| [`type`](#nodebpy.nodes.shader.vector.Mapping.type) |  |
| [`vector_type`](#nodebpy.nodes.shader.vector.Mapping.vector_type) |  |

#### Methods

| Name | Description |
|----|----|
| [normal](#nodebpy.nodes.shader.vector.Mapping.normal) | Create Mapping with operation ‘Normal’. Transform a unit normal vector (Location is ignored) |
| [point](#nodebpy.nodes.shader.vector.Mapping.point) | Create Mapping with operation ‘Point’. Transform a point |
| [texture](#nodebpy.nodes.shader.vector.Mapping.texture) | Create Mapping with operation ‘Texture’. Transform a texture by inverse mapping the texture coordinate |
| [vector](#nodebpy.nodes.shader.vector.Mapping.vector) | Create Mapping with operation ‘Vector’. Transform a direction vector (Location is ignored) |

##### normal

``` python
normal(vector=None, rotation=None, scale=None)
```

Create Mapping with operation ‘Normal’. Transform a unit normal vector (Location is ignored)

##### point

``` python
point(vector=None, location=None, rotation=None, scale=None)
```

Create Mapping with operation ‘Point’. Transform a point

##### texture

``` python
texture(vector=None, location=None, rotation=None, scale=None)
```

Create Mapping with operation ‘Texture’. Transform a texture by inverse mapping the texture coordinate

##### vector

``` python
vector(vector=None, rotation=None, scale=None)
```

Create Mapping with operation ‘Vector’. Transform a direction vector (Location is ignored)

**Inputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.vector`   | `VectorSocket` | Vector      |
| `i.location` | `VectorSocket` | Location    |
| `i.rotation` | `VectorSocket` | Rotation    |
| `i.scale`    | `VectorSocket` | Scale       |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### Normal

``` python
Normal(normal=None)
```

Generate a normal vector and a dot product

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| normal | InputVector | Normal      | `None`  |

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.vector.Normal.i)             |             |
| [`inputs`](#nodebpy.nodes.shader.vector.Normal.inputs)   |             |
| [`name`](#nodebpy.nodes.shader.vector.Normal.name)       |             |
| [`node`](#nodebpy.nodes.shader.vector.Normal.node)       |             |
| [`o`](#nodebpy.nodes.shader.vector.Normal.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.vector.Normal.outputs) |             |
| [`tree`](#nodebpy.nodes.shader.vector.Normal.tree)       |             |
| [`type`](#nodebpy.nodes.shader.vector.Normal.type)       |             |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.normal` | `VectorSocket` | Normal      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.normal` | `VectorSocket` | Normal      |
| `o.dot`    | `FloatSocket`  | Dot         |

### NormalMap

``` python
NormalMap(strength=1.0, color=None, *, space='TANGENT', uv_map='')
```

Generate a perturbed normal from an RGB normal map image. Typically used for faking highly detailed surfaces

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| strength | InputFloat | Strength    | `1.0`   |
| color    | InputColor | Color       | `None`  |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.shader.vector.NormalMap.i)             |             |
| [`inputs`](#nodebpy.nodes.shader.vector.NormalMap.inputs)   |             |
| [`name`](#nodebpy.nodes.shader.vector.NormalMap.name)       |             |
| [`node`](#nodebpy.nodes.shader.vector.NormalMap.node)       |             |
| [`o`](#nodebpy.nodes.shader.vector.NormalMap.o)             |             |
| [`outputs`](#nodebpy.nodes.shader.vector.NormalMap.outputs) |             |
| [`space`](#nodebpy.nodes.shader.vector.NormalMap.space)     |             |
| [`tree`](#nodebpy.nodes.shader.vector.NormalMap.tree)       |             |
| [`type`](#nodebpy.nodes.shader.vector.NormalMap.type)       |             |
| [`uv_map`](#nodebpy.nodes.shader.vector.NormalMap.uv_map)   |             |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.strength` | `FloatSocket` | Strength    |
| `i.color`    | `ColorSocket` | Color       |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.normal` | `VectorSocket` | Normal      |

### VectorDisplacement

``` python
VectorDisplacement(vector=None, midlevel=0.0, scale=0.01, *, space='TANGENT')
```

Displace the surface along an arbitrary direction

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| vector   | InputColor | Vector      | `None`  |
| midlevel | InputFloat | Midlevel    | `0.0`   |
| scale    | InputFloat | Scale       | `0.01`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.VectorDisplacement.i) |  |
| [`inputs`](#nodebpy.nodes.shader.vector.VectorDisplacement.inputs) |  |
| [`name`](#nodebpy.nodes.shader.vector.VectorDisplacement.name) |  |
| [`node`](#nodebpy.nodes.shader.vector.VectorDisplacement.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.VectorDisplacement.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.VectorDisplacement.outputs) |  |
| [`space`](#nodebpy.nodes.shader.vector.VectorDisplacement.space) |  |
| [`tree`](#nodebpy.nodes.shader.vector.VectorDisplacement.tree) |  |
| [`type`](#nodebpy.nodes.shader.vector.VectorDisplacement.type) |  |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.vector`   | `ColorSocket` | Vector      |
| `i.midlevel` | `FloatSocket` | Midlevel    |
| `i.scale`    | `FloatSocket` | Scale       |

**Outputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `o.displacement` | `VectorSocket` | Displacement |

### VectorTransform

``` python
VectorTransform(
    vector=None,
    *,
    vector_type='VECTOR',
    convert_from='WORLD',
    convert_to='OBJECT',
)
```

Convert a vector, point, or normal between world, camera, and object coordinate space

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`convert_from`](#nodebpy.nodes.shader.vector.VectorTransform.convert_from) |  |
| [`convert_to`](#nodebpy.nodes.shader.vector.VectorTransform.convert_to) |  |
| [`i`](#nodebpy.nodes.shader.vector.VectorTransform.i) |  |
| [`inputs`](#nodebpy.nodes.shader.vector.VectorTransform.inputs) |  |
| [`name`](#nodebpy.nodes.shader.vector.VectorTransform.name) |  |
| [`node`](#nodebpy.nodes.shader.vector.VectorTransform.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.VectorTransform.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.VectorTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.VectorTransform.tree) |  |
| [`type`](#nodebpy.nodes.shader.vector.VectorTransform.type) |  |
| [`vector_type`](#nodebpy.nodes.shader.vector.VectorTransform.vector_type) |  |

#### Methods

| Name | Description |
|----|----|
| [normal](#nodebpy.nodes.shader.vector.VectorTransform.normal) | Create Vector Transform with operation ‘Normal’. Transform a normal vector with unit length |
| [point](#nodebpy.nodes.shader.vector.VectorTransform.point) | Create Vector Transform with operation ‘Point’. Transform a point |
| [vector](#nodebpy.nodes.shader.vector.VectorTransform.vector) | Create Vector Transform with operation ‘Vector’. Transform a direction vector |

##### normal

``` python
normal(vector=None)
```

Create Vector Transform with operation ‘Normal’. Transform a normal vector with unit length

##### point

``` python
point(vector=None)
```

Create Vector Transform with operation ‘Point’. Transform a point

##### vector

``` python
vector(vector=None)
```

Create Vector Transform with operation ‘Vector’. Transform a direction vector

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |
