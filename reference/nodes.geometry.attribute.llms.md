# nodes.geometry.attribute

`attribute`

## Classes

| Name | Description |
|----|----|
| [BlurAttribute](#nodebpy.nodes.geometry.attribute.BlurAttribute) | Mix attribute values of neighboring elements |
| [DomainSize](#nodebpy.nodes.geometry.attribute.DomainSize) | Retrieve the number of elements in a geometry for each attribute domain |
| [RemoveNamedAttribute](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute) | Delete an attribute with a specified name from a geometry. Typically used to optimize performance |
| [StoreNamedAttribute](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute) | Store the result of a field on a geometry as an attribute with the specified name |

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
| [`inputs`](#nodebpy.nodes.geometry.attribute.BlurAttribute.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.attribute.DomainSize.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.inputs) |  |
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

### StoreNamedAttribute

``` python
StoreNamedAttribute(
    geometry=None,
    selection=True,
    name='',
    value=0.0,
    *,
    data_type='FLOAT',
    domain='POINT',
)
```

Store the result of a field on a geometry as an attribute with the specified name

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| name      | InputString   | Name        | `''`    |
| value     | InputFloat    | Value       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.domain) |  |
| [`i`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.boolean) | Create Store Named Attribute with operation ‘Boolean’. True or false |
| [byte_color](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.byte_color) | Create Store Named Attribute with operation ‘Byte Color’. RGBA color with 8-bit positive integer values |
| [color](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.color) | Create Store Named Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [edge](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.edge) | Create Store Named Attribute with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.face) | Create Store Named Attribute with operation ‘Face’. Attribute on mesh faces |
| [face_corner](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.face_corner) | Create Store Named Attribute with operation ‘Face Corner’. Attribute on mesh face corner |
| [float](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.float) | Create Store Named Attribute with operation ‘Float’. Floating-point value |
| [input_2d_vector](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.input_2d_vector) | Create Store Named Attribute with operation ‘2D Vector’. 2D vector with floating-point values |
| [input_4x4_matrix](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.input_4x4_matrix) | Create Store Named Attribute with operation ‘4x4 Matrix’. Floating point matrix |
| [input_8_bit_integer](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.input_8_bit_integer) | Create Store Named Attribute with operation ‘8-Bit Integer’. Smaller integer with a range from -128 to 127 |
| [instance](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.instance) | Create Store Named Attribute with operation ‘Instance’. Attribute on instance |
| [integer](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.integer) | Create Store Named Attribute with operation ‘Integer’. 32-bit integer |
| [layer](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.layer) | Create Store Named Attribute with operation ‘Layer’. Attribute on Grease Pencil layer |
| [point](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.point) | Create Store Named Attribute with operation ‘Point’. Attribute on point |
| [quaternion](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.quaternion) | Create Store Named Attribute with operation ‘Quaternion’. Floating point quaternion rotation |
| [spline](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.spline) | Create Store Named Attribute with operation ‘Spline’. Attribute on spline |
| [vector](#nodebpy.nodes.geometry.attribute.StoreNamedAttribute.vector) | Create Store Named Attribute with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(geometry=None, selection=True, name='', value=False)
```

Create Store Named Attribute with operation ‘Boolean’. True or false

##### byte_color

``` python
byte_color(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘Byte Color’. RGBA color with 8-bit positive integer values

##### color

``` python
color(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values

##### edge

``` python
edge(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Face’. Attribute on mesh faces

##### face_corner

``` python
face_corner(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Face Corner’. Attribute on mesh face corner

##### float

``` python
float(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Float’. Floating-point value

##### input_2d_vector

``` python
input_2d_vector(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘2D Vector’. 2D vector with floating-point values

##### input_4x4_matrix

``` python
input_4x4_matrix(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘4x4 Matrix’. Floating point matrix

##### input_8_bit_integer

``` python
input_8_bit_integer(geometry=None, selection=True, name='', value=0)
```

Create Store Named Attribute with operation ‘8-Bit Integer’. Smaller integer with a range from -128 to 127

##### instance

``` python
instance(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Instance’. Attribute on instance

##### integer

``` python
integer(geometry=None, selection=True, name='', value=0)
```

Create Store Named Attribute with operation ‘Integer’. 32-bit integer

##### layer

``` python
layer(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Layer’. Attribute on Grease Pencil layer

##### point

``` python
point(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Point’. Attribute on point

##### quaternion

``` python
quaternion(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘Quaternion’. Floating point quaternion rotation

##### spline

``` python
spline(geometry=None, selection=True, name='', value=0.0)
```

Create Store Named Attribute with operation ‘Spline’. Attribute on spline

##### vector

``` python
vector(geometry=None, selection=True, name='', value=None)
```

Create Store Named Attribute with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.name`      | `StringSocket`   | Name        |
| `i.value`     | `FloatSocket`    | Value       |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |
