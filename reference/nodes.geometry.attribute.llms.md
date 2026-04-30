# nodes.geometry.attribute

`attribute`

## Classes

| Name | Description |
|----|----|
| [BlurAttribute](#nodebpy.nodes.geometry.attribute.BlurAttribute) | Mix attribute values of neighboring elements |
| [DomainSize](#nodebpy.nodes.geometry.attribute.DomainSize) | Retrieve the number of elements in a geometry for each attribute domain |
| [RemoveNamedAttribute](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute) | Delete an attribute with a specified name from a geometry. Typically used to optimize performance |

### BlurAttribute

``` python
BlurAttribute(value=0.0, iterations=1, weight=1.0, *, data_type='FLOAT')
```

Mix attribute values of neighboring elements

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| value      | InputFloat   | Value       | `0.0`   |
| iterations | InputInteger | Iterations  | `1`     |
| weight     | InputFloat   | Weight      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.attribute.BlurAttribute.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.attribute.BlurAttribute.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.BlurAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.attribute.BlurAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.BlurAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.attribute.BlurAttribute.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.BlurAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.attribute.BlurAttribute.type) |  |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.geometry.attribute.BlurAttribute.color) | Create Blur Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.attribute.BlurAttribute.float) | Create Blur Attribute with operation ‘Float’. Floating-point value |
| [integer](#nodebpy.nodes.geometry.attribute.BlurAttribute.integer) | Create Blur Attribute with operation ‘Integer’. 32-bit integer |
| [vector](#nodebpy.nodes.geometry.attribute.BlurAttribute.vector) | Create Blur Attribute with operation ‘Vector’. 3D vector with floating-point values |

##### color

``` python
color(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(value=0.0, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Float’. Floating-point value

##### integer

``` python
integer(value=0, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Integer’. 32-bit integer

##### vector

``` python
vector(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.value`      | `FloatSocket`   | Value       |
| `i.iterations` | `IntegerSocket` | Iterations  |
| `i.weight`     | `FloatSocket`   | Weight      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### DomainSize

``` python
DomainSize(geometry=None, *, component='MESH')
```

Retrieve the number of elements in a geometry for each attribute domain

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`component`](#nodebpy.nodes.geometry.attribute.DomainSize.component) |  |
| [`i`](#nodebpy.nodes.geometry.attribute.DomainSize.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.DomainSize.name) |  |
| [`node`](#nodebpy.nodes.geometry.attribute.DomainSize.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.DomainSize.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.attribute.DomainSize.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.DomainSize.tree) |  |
| [`type`](#nodebpy.nodes.geometry.attribute.DomainSize.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |

**Outputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `o.point_count`       | `IntegerSocket` | Point Count       |
| `o.edge_count`        | `IntegerSocket` | Edge Count        |
| `o.face_count`        | `IntegerSocket` | Face Count        |
| `o.face_corner_count` | `IntegerSocket` | Face Corner Count |
| `o.spline_count`      | `IntegerSocket` | Spline Count      |
| `o.instance_count`    | `IntegerSocket` | Instance Count    |
| `o.layer_count`       | `IntegerSocket` | Layer Count       |

### RemoveNamedAttribute

``` python
RemoveNamedAttribute(geometry=None, pattern_mode='Exact', name='')
```

Delete an attribute with a specified name from a geometry. Typically used to optimize performance

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| geometry | InputGeometry | Geometry | `None` |
| pattern_mode | InputMenu \| Literal\['Exact', 'Wildcard'\] | Pattern Mode | `'Exact'` |
| name | InputString | Name | `''` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.type) |  |

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.geometry`     | `GeometrySocket` | Geometry     |
| `i.pattern_mode` | `MenuSocket`     | Pattern Mode |
| `i.name`         | `StringSocket`   | Name         |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |
