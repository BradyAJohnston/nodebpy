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
    normal=(0.0, 0.0, 0.0),
    *,
    invert=False,
)
```

Generate a perturbed normal from a height texture for bump mapping. Typically used for faking highly detailed surfaces

#### Parameters

| Name         | Type        | Description  | Default           |
|--------------|-------------|--------------|-------------------|
| strength     | InputFloat  | Strength     | `1.0`             |
| distance     | InputFloat  | Distance     | `0.001`           |
| filter_width | InputFloat  | Filter Width | `0.1`             |
| height       | InputFloat  | Height       | `1.0`             |
| normal       | InputVector | Normal       | `(0.0, 0.0, 0.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Bump.i) |  |
| [`invert`](#nodebpy.nodes.shader.vector.Bump.invert) |  |
| [`name`](#nodebpy.nodes.shader.vector.Bump.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.Bump.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Bump.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Bump.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Bump.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
    normal=(0.0, 0.0, 0.0),
    *,
    space='OBJECT',
)
```

Displace the surface along the surface normal

#### Parameters

| Name     | Type        | Description | Default           |
|----------|-------------|-------------|-------------------|
| height   | InputFloat  | Height      | `0.0`             |
| midlevel | InputFloat  | Midlevel    | `0.5`             |
| scale    | InputFloat  | Scale       | `0.01`            |
| normal   | InputVector | Normal      | `(0.0, 0.0, 0.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Displacement.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.Displacement.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.Displacement.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Displacement.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Displacement.outputs) |  |
| [`space`](#nodebpy.nodes.shader.vector.Displacement.space) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Displacement.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
    vector=(0.0, 0.0, 0.0),
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, 0.0),
    scale=(1.0, 1.0, 1.0),
    *,
    vector_type='POINT',
)
```

Transform the input vector by applying translation, rotation, and scale

#### Parameters

| Name     | Type        | Description | Default           |
|----------|-------------|-------------|-------------------|
| vector   | InputVector | Vector      | `(0.0, 0.0, 0.0)` |
| location | InputVector | Location    | `(0.0, 0.0, 0.0)` |
| rotation | InputVector | Rotation    | `(0.0, 0.0, 0.0)` |
| scale    | InputVector | Scale       | `(1.0, 1.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Mapping.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.Mapping.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.Mapping.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Mapping.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Mapping.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Mapping.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
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
normal(vector=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
```

Create Mapping with operation ‘Normal’. Transform a unit normal vector (Location is ignored)

##### point

``` python
point(
    vector=(0.0, 0.0, 0.0),
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, 0.0),
    scale=(1.0, 1.0, 1.0),
)
```

Create Mapping with operation ‘Point’. Transform a point

##### texture

``` python
texture(
    vector=(0.0, 0.0, 0.0),
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, 0.0),
    scale=(1.0, 1.0, 1.0),
)
```

Create Mapping with operation ‘Texture’. Transform a texture by inverse mapping the texture coordinate

##### vector

``` python
vector(vector=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
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
Normal(normal=(0.0, 0.0, 1.0))
```

Generate a normal vector and a dot product

#### Parameters

| Name   | Type        | Description | Default           |
|--------|-------------|-------------|-------------------|
| normal | InputVector | Normal      | `(0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.Normal.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.Normal.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.Normal.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.Normal.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.Normal.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.Normal.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
NormalMap(
    strength=1.0,
    color=(0.5, 0.5, 1.0, 1.0),
    *,
    space='TANGENT',
    uv_map='',
    convention='OPENGL',
    base='DISPLACED',
)
```

Generate a perturbed normal from an RGB normal map image. Typically used for faking highly detailed surfaces

#### Parameters

| Name     | Type       | Description | Default                |
|----------|------------|-------------|------------------------|
| strength | InputFloat | Strength    | `1.0`                  |
| color    | InputColor | Color       | `(0.5, 0.5, 1.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`base`](#nodebpy.nodes.shader.vector.NormalMap.base) |  |
| [`convention`](#nodebpy.nodes.shader.vector.NormalMap.convention) |  |
| [`i`](#nodebpy.nodes.shader.vector.NormalMap.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.NormalMap.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.NormalMap.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.NormalMap.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.NormalMap.outputs) |  |
| [`space`](#nodebpy.nodes.shader.vector.NormalMap.space) |  |
| [`tree`](#nodebpy.nodes.shader.vector.NormalMap.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`uv_map`](#nodebpy.nodes.shader.vector.NormalMap.uv_map) |  |

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
VectorDisplacement(
    vector=(0.8, 0.8, 0.8, 1.0),
    midlevel=0.0,
    scale=0.01,
    *,
    space='TANGENT',
)
```

Displace the surface along an arbitrary direction

#### Parameters

| Name     | Type       | Description | Default                |
|----------|------------|-------------|------------------------|
| vector   | InputColor | Vector      | `(0.8, 0.8, 0.8, 1.0)` |
| midlevel | InputFloat | Midlevel    | `0.0`                  |
| scale    | InputFloat | Scale       | `0.01`                 |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.vector.VectorDisplacement.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.VectorDisplacement.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.VectorDisplacement.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.VectorDisplacement.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.VectorDisplacement.outputs) |  |
| [`space`](#nodebpy.nodes.shader.vector.VectorDisplacement.space) |  |
| [`tree`](#nodebpy.nodes.shader.vector.VectorDisplacement.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
    vector=(0.5, 0.5, 0.5),
    *,
    vector_type='VECTOR',
    convert_from='WORLD',
    convert_to='OBJECT',
)
```

Convert a vector, point, or normal between world, camera, and object coordinate space

#### Parameters

| Name   | Type        | Description | Default           |
|--------|-------------|-------------|-------------------|
| vector | InputVector | Vector      | `(0.5, 0.5, 0.5)` |

#### Attributes

| Name | Description |
|----|----|
| [`convert_from`](#nodebpy.nodes.shader.vector.VectorTransform.convert_from) |  |
| [`convert_to`](#nodebpy.nodes.shader.vector.VectorTransform.convert_to) |  |
| [`i`](#nodebpy.nodes.shader.vector.VectorTransform.i) |  |
| [`name`](#nodebpy.nodes.shader.vector.VectorTransform.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.vector.VectorTransform.node) |  |
| [`o`](#nodebpy.nodes.shader.vector.VectorTransform.o) |  |
| [`outputs`](#nodebpy.nodes.shader.vector.VectorTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.vector.VectorTransform.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`vector_type`](#nodebpy.nodes.shader.vector.VectorTransform.vector_type) |  |

#### Methods

| Name | Description |
|----|----|
| [normal](#nodebpy.nodes.shader.vector.VectorTransform.normal) | Create Vector Transform with operation ‘Normal’. Transform a normal vector with unit length |
| [point](#nodebpy.nodes.shader.vector.VectorTransform.point) | Create Vector Transform with operation ‘Point’. Transform a point |
| [vector](#nodebpy.nodes.shader.vector.VectorTransform.vector) | Create Vector Transform with operation ‘Vector’. Transform a direction vector |

##### normal

``` python
normal(vector=(0.5, 0.5, 0.5))
```

Create Vector Transform with operation ‘Normal’. Transform a normal vector with unit length

##### point

``` python
point(vector=(0.5, 0.5, 0.5))
```

Create Vector Transform with operation ‘Point’. Transform a point

##### vector

``` python
vector(vector=(0.5, 0.5, 0.5))
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
