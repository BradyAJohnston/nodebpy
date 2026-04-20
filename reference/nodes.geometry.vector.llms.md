# nodes.geometry.vector

`vector`

## Classes

| Name | Description |
|----|----|
| [RadialTiling](#nodebpy.nodes.geometry.vector.RadialTiling) | Transform Coordinate System for Radial Tiling |
| [VectorCurves](#nodebpy.nodes.geometry.vector.VectorCurves) | Map input vector components with curves |
| [VectorMath](#nodebpy.nodes.geometry.vector.VectorMath) | Perform vector math operation |
| [VectorRotate](#nodebpy.nodes.geometry.vector.VectorRotate) | Rotate a vector around a pivot point (center) |

### RadialTiling

``` python
RadialTiling(vector=None, sides=5.0, roundness=0.0, *, normalize=False)
```

Transform Coordinate System for Radial Tiling

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| vector    | InputVector | Vector      | `None`  |
| sides     | InputFloat  | Sides       | `5.0`   |
| roundness | InputFloat  | Roundness   | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.vector.RadialTiling.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.vector.RadialTiling.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.vector.RadialTiling.name) |  |
| [`node`](#nodebpy.nodes.geometry.vector.RadialTiling.node) |  |
| [`normalize`](#nodebpy.nodes.geometry.vector.RadialTiling.normalize) |  |
| [`o`](#nodebpy.nodes.geometry.vector.RadialTiling.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.vector.RadialTiling.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.vector.RadialTiling.tree) |  |
| [`type`](#nodebpy.nodes.geometry.vector.RadialTiling.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.vector`    | `VectorSocket` | Vector      |
| `i.sides`     | `FloatSocket`  | Sides       |
| `i.roundness` | `FloatSocket`  | Roundness   |

**Outputs**

| Attribute               | Type           | Description         |
|-------------------------|----------------|---------------------|
| `o.segment_coordinates` | `VectorSocket` | Segment Coordinates |
| `o.segment_id`          | `FloatSocket`  | Segment ID          |
| `o.segment_width`       | `FloatSocket`  | Segment Width       |
| `o.segment_rotation`    | `FloatSocket`  | Segment Rotation    |

### VectorCurves

``` python
VectorCurves(fac=1.0, vector=None)
```

Map input vector components with curves

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| fac    | InputFloat  | Factor      | `1.0`   |
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.vector.VectorCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.vector.VectorCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.vector.VectorCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.vector.VectorCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.vector.VectorCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.vector.VectorCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.vector.VectorCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.vector.VectorCurves.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.fac`    | `FloatSocket`  | Factor      |
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### VectorMath

``` python
VectorMath(
    vector=None,
    vector_001=None,
    vector_002=None,
    scale=1.0,
    *,
    operation='ADD',
)
```

Perform vector math operation

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| vector     | InputVector | Vector      | `None`  |
| vector_001 | InputVector | Vector      | `None`  |
| vector_002 | InputVector | Vector      | `None`  |
| scale      | InputFloat  | Scale       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.vector.VectorMath.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.vector.VectorMath.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.vector.VectorMath.name) |  |
| [`node`](#nodebpy.nodes.geometry.vector.VectorMath.node) |  |
| [`o`](#nodebpy.nodes.geometry.vector.VectorMath.o) |  |
| [`operation`](#nodebpy.nodes.geometry.vector.VectorMath.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.vector.VectorMath.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.vector.VectorMath.tree) |  |
| [`type`](#nodebpy.nodes.geometry.vector.VectorMath.type) |  |

#### Methods

| Name | Description |
|----|----|
| [absolute](#nodebpy.nodes.geometry.vector.VectorMath.absolute) | Create Vector Math with operation ‘Absolute’. Entry-wise absolute |
| [add](#nodebpy.nodes.geometry.vector.VectorMath.add) | Create Vector Math with operation ‘Add’. A + B |
| [ceil](#nodebpy.nodes.geometry.vector.VectorMath.ceil) | Create Vector Math with operation ‘Ceil’. Entry-wise ceil |
| [cosine](#nodebpy.nodes.geometry.vector.VectorMath.cosine) | Create Vector Math with operation ‘Cosine’. Entry-wise cos(A) |
| [cross_product](#nodebpy.nodes.geometry.vector.VectorMath.cross_product) | Create Vector Math with operation ‘Cross Product’. A cross B |
| [distance](#nodebpy.nodes.geometry.vector.VectorMath.distance) | Create Vector Math with operation ‘Distance’. Distance between A and B |
| [divide](#nodebpy.nodes.geometry.vector.VectorMath.divide) | Create Vector Math with operation ‘Divide’. Entry-wise divide |
| [dot_product](#nodebpy.nodes.geometry.vector.VectorMath.dot_product) | Create Vector Math with operation ‘Dot Product’. A dot B |
| [faceforward](#nodebpy.nodes.geometry.vector.VectorMath.faceforward) | Create Vector Math with operation ‘Faceforward’. Orients a vector A to point away from a surface B as defined by its normal C. Returns (dot(B, C) \< 0) ? A : -A |
| [floor](#nodebpy.nodes.geometry.vector.VectorMath.floor) | Create Vector Math with operation ‘Floor’. Entry-wise floor |
| [fraction](#nodebpy.nodes.geometry.vector.VectorMath.fraction) | Create Vector Math with operation ‘Fraction’. The fraction part of A entry-wise |
| [length](#nodebpy.nodes.geometry.vector.VectorMath.length) | Create Vector Math with operation ‘Length’. Length of A |
| [maximum](#nodebpy.nodes.geometry.vector.VectorMath.maximum) | Create Vector Math with operation ‘Maximum’. Entry-wise maximum |
| [minimum](#nodebpy.nodes.geometry.vector.VectorMath.minimum) | Create Vector Math with operation ‘Minimum’. Entry-wise minimum |
| [modulo](#nodebpy.nodes.geometry.vector.VectorMath.modulo) | Create Vector Math with operation ‘Modulo’. Entry-wise modulo using fmod(A,B) |
| [multiply](#nodebpy.nodes.geometry.vector.VectorMath.multiply) | Create Vector Math with operation ‘Multiply’. Entry-wise multiply |
| [multiply_add](#nodebpy.nodes.geometry.vector.VectorMath.multiply_add) | Create Vector Math with operation ‘Multiply Add’. A \* B + C |
| [normalize](#nodebpy.nodes.geometry.vector.VectorMath.normalize) | Create Vector Math with operation ‘Normalize’. Normalize A |
| [power](#nodebpy.nodes.geometry.vector.VectorMath.power) | Create Vector Math with operation ‘Power’. Entry-wise power |
| [project](#nodebpy.nodes.geometry.vector.VectorMath.project) | Create Vector Math with operation ‘Project’. Project A onto B |
| [reflect](#nodebpy.nodes.geometry.vector.VectorMath.reflect) | Create Vector Math with operation ‘Reflect’. Reflect A around the normal B. B does not need to be normalized. |
| [refract](#nodebpy.nodes.geometry.vector.VectorMath.refract) | Create Vector Math with operation ‘Refract’. For a given incident vector A, surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R |
| [scale](#nodebpy.nodes.geometry.vector.VectorMath.scale) | Create Vector Math with operation ‘Scale’. A multiplied by Scale |
| [sign](#nodebpy.nodes.geometry.vector.VectorMath.sign) | Create Vector Math with operation ‘Sign’. Entry-wise sign |
| [sine](#nodebpy.nodes.geometry.vector.VectorMath.sine) | Create Vector Math with operation ‘Sine’. Entry-wise sin(A) |
| [snap](#nodebpy.nodes.geometry.vector.VectorMath.snap) | Create Vector Math with operation ‘Snap’. Round A to the largest integer multiple of B less than or equal A |
| [subtract](#nodebpy.nodes.geometry.vector.VectorMath.subtract) | Create Vector Math with operation ‘Subtract’. A - B |
| [tangent](#nodebpy.nodes.geometry.vector.VectorMath.tangent) | Create Vector Math with operation ‘Tangent’. Entry-wise tan(A) |
| [wrap](#nodebpy.nodes.geometry.vector.VectorMath.wrap) | Create Vector Math with operation ‘Wrap’. Entry-wise wrap(A,B) |

##### absolute

``` python
absolute(vector=None)
```

Create Vector Math with operation ‘Absolute’. Entry-wise absolute

##### add

``` python
add(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Add’. A + B

##### ceil

``` python
ceil(vector=None)
```

Create Vector Math with operation ‘Ceil’. Entry-wise ceil

##### cosine

``` python
cosine(vector=None)
```

Create Vector Math with operation ‘Cosine’. Entry-wise cos(A)

##### cross_product

``` python
cross_product(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Cross Product’. A cross B

##### distance

``` python
distance(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Distance’. Distance between A and B

##### divide

``` python
divide(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Divide’. Entry-wise divide

##### dot_product

``` python
dot_product(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Dot Product’. A dot B

##### faceforward

``` python
faceforward(vector=None, vector_001=None, vector_002=None)
```

Create Vector Math with operation ‘Faceforward’. Orients a vector A to point away from a surface B as defined by its normal C. Returns (dot(B, C) \< 0) ? A : -A

##### floor

``` python
floor(vector=None)
```

Create Vector Math with operation ‘Floor’. Entry-wise floor

##### fraction

``` python
fraction(vector=None)
```

Create Vector Math with operation ‘Fraction’. The fraction part of A entry-wise

##### length

``` python
length(vector=None)
```

Create Vector Math with operation ‘Length’. Length of A

##### maximum

``` python
maximum(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Maximum’. Entry-wise maximum

##### minimum

``` python
minimum(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Minimum’. Entry-wise minimum

##### modulo

``` python
modulo(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Modulo’. Entry-wise modulo using fmod(A,B)

##### multiply

``` python
multiply(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Multiply’. Entry-wise multiply

##### multiply_add

``` python
multiply_add(vector=None, vector_001=None, vector_002=None)
```

Create Vector Math with operation ‘Multiply Add’. A \* B + C

##### normalize

``` python
normalize(vector=None)
```

Create Vector Math with operation ‘Normalize’. Normalize A

##### power

``` python
power(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Power’. Entry-wise power

##### project

``` python
project(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Project’. Project A onto B

##### reflect

``` python
reflect(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Reflect’. Reflect A around the normal B. B does not need to be normalized.

##### refract

``` python
refract(vector=None, vector_001=None, scale=1.0)
```

Create Vector Math with operation ‘Refract’. For a given incident vector A, surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R

##### scale

``` python
scale(vector=None, scale=1.0)
```

Create Vector Math with operation ‘Scale’. A multiplied by Scale

##### sign

``` python
sign(vector=None)
```

Create Vector Math with operation ‘Sign’. Entry-wise sign

##### sine

``` python
sine(vector=None)
```

Create Vector Math with operation ‘Sine’. Entry-wise sin(A)

##### snap

``` python
snap(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Snap’. Round A to the largest integer multiple of B less than or equal A

##### subtract

``` python
subtract(vector=None, vector_001=None)
```

Create Vector Math with operation ‘Subtract’. A - B

##### tangent

``` python
tangent(vector=None)
```

Create Vector Math with operation ‘Tangent’. Entry-wise tan(A)

##### wrap

``` python
wrap(vector=None, vector_001=None, vector_002=None)
```

Create Vector Math with operation ‘Wrap’. Entry-wise wrap(A,B)

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.vector`     | `VectorSocket` | Vector      |
| `i.vector_001` | `VectorSocket` | Vector      |
| `i.vector_002` | `VectorSocket` | Vector      |
| `i.scale`      | `FloatSocket`  | Scale       |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |
| `o.value`  | `FloatSocket`  | Value       |

### VectorRotate

``` python
VectorRotate(
    vector=None,
    center=None,
    axis=None,
    angle=0.0,
    rotation=None,
    *,
    rotation_type='AXIS_ANGLE',
    invert=False,
)
```

Rotate a vector around a pivot point (center)

#### Parameters

| Name     | Type        | Description | Default |
|----------|-------------|-------------|---------|
| vector   | InputVector | Vector      | `None`  |
| center   | InputVector | Center      | `None`  |
| axis     | InputVector | Axis        | `None`  |
| angle    | InputFloat  | Angle       | `0.0`   |
| rotation | InputVector | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.vector.VectorRotate.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.vector.VectorRotate.inputs) |  |
| [`invert`](#nodebpy.nodes.geometry.vector.VectorRotate.invert) |  |
| [`name`](#nodebpy.nodes.geometry.vector.VectorRotate.name) |  |
| [`node`](#nodebpy.nodes.geometry.vector.VectorRotate.node) |  |
| [`o`](#nodebpy.nodes.geometry.vector.VectorRotate.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.vector.VectorRotate.outputs) |  |
| [`rotation_type`](#nodebpy.nodes.geometry.vector.VectorRotate.rotation_type) |  |
| [`tree`](#nodebpy.nodes.geometry.vector.VectorRotate.tree) |  |
| [`type`](#nodebpy.nodes.geometry.vector.VectorRotate.type) |  |

#### Methods

| Name | Description |
|----|----|
| [axis_angle](#nodebpy.nodes.geometry.vector.VectorRotate.axis_angle) | Create Vector Rotate with operation ‘Axis Angle’. Rotate a point using axis angle |
| [euler](#nodebpy.nodes.geometry.vector.VectorRotate.euler) | Create Vector Rotate with operation ‘Euler’. Rotate a point using XYZ order |
| [x_axis](#nodebpy.nodes.geometry.vector.VectorRotate.x_axis) | Create Vector Rotate with operation ‘X Axis’. Rotate a point using X axis |
| [y_axis](#nodebpy.nodes.geometry.vector.VectorRotate.y_axis) | Create Vector Rotate with operation ‘Y Axis’. Rotate a point using Y axis |
| [z_axis](#nodebpy.nodes.geometry.vector.VectorRotate.z_axis) | Create Vector Rotate with operation ‘Z Axis’. Rotate a point using Z axis |

##### axis_angle

``` python
axis_angle(vector=None, center=None, axis=None, angle=0.0)
```

Create Vector Rotate with operation ‘Axis Angle’. Rotate a point using axis angle

##### euler

``` python
euler(vector=None, center=None, rotation=None)
```

Create Vector Rotate with operation ‘Euler’. Rotate a point using XYZ order

##### x_axis

``` python
x_axis(vector=None, center=None, angle=0.0)
```

Create Vector Rotate with operation ‘X Axis’. Rotate a point using X axis

##### y_axis

``` python
y_axis(vector=None, center=None, angle=0.0)
```

Create Vector Rotate with operation ‘Y Axis’. Rotate a point using Y axis

##### z_axis

``` python
z_axis(vector=None, center=None, angle=0.0)
```

Create Vector Rotate with operation ‘Z Axis’. Rotate a point using Z axis

**Inputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.vector`   | `VectorSocket` | Vector      |
| `i.center`   | `VectorSocket` | Center      |
| `i.axis`     | `VectorSocket` | Axis        |
| `i.angle`    | `FloatSocket`  | Angle       |
| `i.rotation` | `VectorSocket` | Rotation    |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |
