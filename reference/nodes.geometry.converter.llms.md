# nodes.geometry.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [AlignRotationToVector](#nodebpy.nodes.geometry.converter.AlignRotationToVector) | Orient a rotation along the given direction |
| [AxesToRotation](#nodebpy.nodes.geometry.converter.AxesToRotation) | Create a rotation from a primary and (ideally orthogonal) secondary axis |
| [AxisAngleToRotation](#nodebpy.nodes.geometry.converter.AxisAngleToRotation) | Build a rotation from an axis and a rotation around that axis |
| [BitMath](#nodebpy.nodes.geometry.converter.BitMath) | Perform bitwise operations on 32-bit integers |
| [Blackbody](#nodebpy.nodes.geometry.converter.Blackbody) | Convert a blackbody temperature to an RGB value |
| [BooleanMath](#nodebpy.nodes.geometry.converter.BooleanMath) | Perform a logical operation on the given boolean inputs |
| [Clamp](#nodebpy.nodes.geometry.converter.Clamp) | Clamp a value between a minimum and a maximum |
| [CombineBundle](#nodebpy.nodes.geometry.converter.CombineBundle) | Combine multiple socket values into one. |
| [CombineColor](#nodebpy.nodes.geometry.converter.CombineColor) | Combine four channels into a single color, based on a particular color model |
| [CombineMatrix](#nodebpy.nodes.geometry.converter.CombineMatrix) | Construct a 4x4 matrix from its individual values |
| [CombineTransform](#nodebpy.nodes.geometry.converter.CombineTransform) | Combine a translation vector, a rotation, and a scale vector into a transformation matrix |
| [CombineXYZ](#nodebpy.nodes.geometry.converter.CombineXYZ) | Create a vector from X, Y, and Z components |
| [EulerToRotation](#nodebpy.nodes.geometry.converter.EulerToRotation) | Build a rotation from separate angles around each axis |
| [FindInString](#nodebpy.nodes.geometry.converter.FindInString) | Find the number of times a given string occurs in another string and the position of the first match |
| [FloatToInteger](#nodebpy.nodes.geometry.converter.FloatToInteger) | Convert the given floating-point number to an integer, with a choice of methods |
| [GetBundleItem](#nodebpy.nodes.geometry.converter.GetBundleItem) | Retrieve a bundle item by path. |
| [HashValue](#nodebpy.nodes.geometry.converter.HashValue) | Generate a randomized integer using the given input value as a seed |
| [IndexOfNearest](#nodebpy.nodes.geometry.converter.IndexOfNearest) | Find the nearest element in a group. Similar to the “Sample Nearest” node |
| [IntegerMath](#nodebpy.nodes.geometry.converter.IntegerMath) | Perform various math operations on the given integer inputs |
| [InvertMatrix](#nodebpy.nodes.geometry.converter.InvertMatrix) | Compute the inverse of the given matrix, if one exists |
| [InvertRotation](#nodebpy.nodes.geometry.converter.InvertRotation) | Compute the inverse of the given rotation |
| [JoinBundle](#nodebpy.nodes.geometry.converter.JoinBundle) | Join multiple bundles together |
| [MapRange](#nodebpy.nodes.geometry.converter.MapRange) | Remap a value from a range to a target range |
| [MatchString](#nodebpy.nodes.geometry.converter.MatchString) | Check if a given string exists within another string |
| [Math](#nodebpy.nodes.geometry.converter.Math) | Perform math operations |
| [MatrixDeterminant](#nodebpy.nodes.geometry.converter.MatrixDeterminant) | Compute the determinant of the given matrix |
| [MatrixSVD](#nodebpy.nodes.geometry.converter.MatrixSVD) | Compute the singular value decomposition of the 3x3 part of a matrix |
| [Mix](#nodebpy.nodes.geometry.converter.Mix) | Mix values by a factor |
| [MultiplyMatrices](#nodebpy.nodes.geometry.converter.MultiplyMatrices) | Perform a matrix multiplication on two input matrices |
| [PackUVIslands](#nodebpy.nodes.geometry.converter.PackUVIslands) | Scale islands of a UV map and move them so they fill the UV space as much as possible |
| [ProjectPoint](#nodebpy.nodes.geometry.converter.ProjectPoint) | Project a point using a matrix, using location, rotation, scale, and perspective divide |
| [QuaternionToRotation](#nodebpy.nodes.geometry.converter.QuaternionToRotation) | Build a rotation from quaternion components |
| [RandomValue](#nodebpy.nodes.geometry.converter.RandomValue) | Output a randomized value |
| [ReplaceString](#nodebpy.nodes.geometry.converter.ReplaceString) | Replace a given string segment with another |
| [RotateEuler](#nodebpy.nodes.geometry.converter.RotateEuler) | Apply a secondary Euler rotation to a given Euler rotation |
| [RotateRotation](#nodebpy.nodes.geometry.converter.RotateRotation) | Apply a secondary rotation to a given rotation value |
| [RotateVector](#nodebpy.nodes.geometry.converter.RotateVector) | Apply a rotation to a given vector |
| [RotationToAxisAngle](#nodebpy.nodes.geometry.converter.RotationToAxisAngle) | Convert a rotation to axis angle components |
| [RotationToEuler](#nodebpy.nodes.geometry.converter.RotationToEuler) | Convert a standard rotation value to an Euler rotation |
| [RotationToQuaternion](#nodebpy.nodes.geometry.converter.RotationToQuaternion) | Retrieve the quaternion components representing a rotation |
| [SeparateBundle](#nodebpy.nodes.geometry.converter.SeparateBundle) | Split a bundle into multiple sockets. |
| [SeparateColor](#nodebpy.nodes.geometry.converter.SeparateColor) | Split a color into separate channels, based on a particular color model |
| [SeparateMatrix](#nodebpy.nodes.geometry.converter.SeparateMatrix) | Split a 4x4 matrix into its individual values |
| [SeparateTransform](#nodebpy.nodes.geometry.converter.SeparateTransform) | Split a transformation matrix into a translation vector, a rotation, and a scale vector |
| [SeparateXYZ](#nodebpy.nodes.geometry.converter.SeparateXYZ) | Split a vector into its X, Y, and Z components |
| [SliceString](#nodebpy.nodes.geometry.converter.SliceString) | Extract a string segment from a larger string |
| [StoreBundleItem](#nodebpy.nodes.geometry.converter.StoreBundleItem) | Store a bundle item by path and data type. |
| [StringLength](#nodebpy.nodes.geometry.converter.StringLength) | Output the number of characters in the given string |
| [StringToValue](#nodebpy.nodes.geometry.converter.StringToValue) | Derive a numeric value from a given string representation |
| [TransformDirection](#nodebpy.nodes.geometry.converter.TransformDirection) | Apply a transformation matrix (excluding translation) to the given vector |
| [TransformPoint](#nodebpy.nodes.geometry.converter.TransformPoint) | Apply a transformation matrix to the given vector |
| [TransposeMatrix](#nodebpy.nodes.geometry.converter.TransposeMatrix) | Flip a matrix over its diagonal, turning columns into rows and vice-versa |
| [UVUnwrap](#nodebpy.nodes.geometry.converter.UVUnwrap) | Generate a UV map based on seam edges |
| [ValueToString](#nodebpy.nodes.geometry.converter.ValueToString) | Generate a string representation of the given input value |

### AlignRotationToVector

``` python
AlignRotationToVector(
    rotation=None,
    factor=1.0,
    vector=None,
    *,
    axis='Z',
    pivot_axis='AUTO',
)
```

Orient a rotation along the given direction

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| rotation | InputRotation | Rotation    | `None`  |
| factor   | InputFloat    | Factor      | `1.0`   |
| vector   | InputVector   | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`axis`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.axis) |  |
| [`i`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.outputs) |  |
| [`pivot_axis`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.pivot_axis) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.AlignRotationToVector.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.rotation` | `RotationSocket` | Rotation    |
| `i.factor`   | `FloatSocket`    | Factor      |
| `i.vector`   | `VectorSocket`   | Vector      |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### AxesToRotation

``` python
AxesToRotation(
    primary_axis=None,
    secondary_axis=None,
    *,
    primary='Z',
    secondary='X',
)
```

Create a rotation from a primary and (ideally orthogonal) secondary axis

#### Parameters

| Name           | Type        | Description    | Default |
|----------------|-------------|----------------|---------|
| primary_axis   | InputVector | Primary Axis   | `None`  |
| secondary_axis | InputVector | Secondary Axis | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.AxesToRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.AxesToRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.AxesToRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.AxesToRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.AxesToRotation.outputs) |  |
| [`primary`](#nodebpy.nodes.geometry.converter.AxesToRotation.primary) |  |
| [`primary_axis`](#nodebpy.nodes.geometry.converter.AxesToRotation.primary_axis) |  |
| [`secondary`](#nodebpy.nodes.geometry.converter.AxesToRotation.secondary) |  |
| [`secondary_axis`](#nodebpy.nodes.geometry.converter.AxesToRotation.secondary_axis) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.AxesToRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.AxesToRotation.type) |  |

**Inputs**

| Attribute          | Type           | Description    |
|--------------------|----------------|----------------|
| `i.primary_axis`   | `VectorSocket` | Primary Axis   |
| `i.secondary_axis` | `VectorSocket` | Secondary Axis |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### AxisAngleToRotation

``` python
AxisAngleToRotation(axis=None, angle=0.0)
```

Build a rotation from an axis and a rotation around that axis

#### Parameters

| Name  | Type        | Description | Default |
|-------|-------------|-------------|---------|
| axis  | InputVector | Axis        | `None`  |
| angle | InputFloat  | Angle       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.AxisAngleToRotation.type) |  |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.axis`  | `VectorSocket` | Axis        |
| `i.angle` | `FloatSocket`  | Angle       |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### BitMath

``` python
BitMath(a=0, b=0, shift=0, *, operation='AND')
```

Perform bitwise operations on 32-bit integers

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| a     | InputInteger | A           | `0`     |
| b     | InputInteger | B           | `0`     |
| shift | InputInteger | Shift       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.BitMath.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.BitMath.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.BitMath.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.BitMath.o) |  |
| [`operation`](#nodebpy.nodes.geometry.converter.BitMath.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.BitMath.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.BitMath.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.BitMath.type) |  |

#### Methods

| Name | Description |
|----|----|
| [exclusive_or](#nodebpy.nodes.geometry.converter.BitMath.exclusive_or) | Create Bit Math with operation ‘Exclusive Or’. Returns a value where only one bit from A and B is set |
| [l_and](#nodebpy.nodes.geometry.converter.BitMath.l_and) | Create Bit Math with operation ‘And’. Returns a value where the bits of A and B are both set |
| [l_not](#nodebpy.nodes.geometry.converter.BitMath.l_not) | Create Bit Math with operation ‘Not’. Returns the opposite bit value of A, in decimal it is equivalent of A = -A - 1 |
| [l_or](#nodebpy.nodes.geometry.converter.BitMath.l_or) | Create Bit Math with operation ‘Or’. Returns a value where the bits of either A or B are set |
| [rotate](#nodebpy.nodes.geometry.converter.BitMath.rotate) | Create Bit Math with operation ‘Rotate’. Rotates the bit values of A by the specified Shift amount. Positive values rotate left, negative values rotate right. |
| [shift](#nodebpy.nodes.geometry.converter.BitMath.shift) | Create Bit Math with operation ‘Shift’. Shifts the bit values of A by the specified Shift amount. Positive values shift left, negative values shift right. |

##### exclusive_or

``` python
exclusive_or(a=0, b=0)
```

Create Bit Math with operation ‘Exclusive Or’. Returns a value where only one bit from A and B is set

##### l_and

``` python
l_and(a=0, b=0)
```

Create Bit Math with operation ‘And’. Returns a value where the bits of A and B are both set

##### l_not

``` python
l_not(a=0)
```

Create Bit Math with operation ‘Not’. Returns the opposite bit value of A, in decimal it is equivalent of A = -A - 1

##### l_or

``` python
l_or(a=0, b=0)
```

Create Bit Math with operation ‘Or’. Returns a value where the bits of either A or B are set

##### rotate

``` python
rotate(a=0, shift=0)
```

Create Bit Math with operation ‘Rotate’. Rotates the bit values of A by the specified Shift amount. Positive values rotate left, negative values rotate right.

##### shift

``` python
shift(a=0, shift=0)
```

Create Bit Math with operation ‘Shift’. Shifts the bit values of A by the specified Shift amount. Positive values shift left, negative values shift right.

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.a`     | `IntegerSocket` | A           |
| `i.b`     | `IntegerSocket` | B           |
| `i.shift` | `IntegerSocket` | Shift       |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.value` | `IntegerSocket` | Value       |

### Blackbody

``` python
Blackbody(temperature=6500.0)
```

Convert a blackbody temperature to an RGB value

#### Parameters

| Name        | Type       | Description | Default  |
|-------------|------------|-------------|----------|
| temperature | InputFloat | Temperature | `6500.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.Blackbody.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.Blackbody.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.Blackbody.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.Blackbody.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.Blackbody.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.Blackbody.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.Blackbody.type) |  |

**Inputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `i.temperature` | `FloatSocket` | Temperature |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### BooleanMath

``` python
BooleanMath(boolean=False, boolean_001=False, *, operation='AND')
```

Perform a logical operation on the given boolean inputs

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| boolean     | InputBoolean | Boolean     | `False` |
| boolean_001 | InputBoolean | Boolean     | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.BooleanMath.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.BooleanMath.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.BooleanMath.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.BooleanMath.o) |  |
| [`operation`](#nodebpy.nodes.geometry.converter.BooleanMath.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.BooleanMath.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.BooleanMath.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.BooleanMath.type) |  |

#### Methods

| Name | Description |
|----|----|
| [equal](#nodebpy.nodes.geometry.converter.BooleanMath.equal) | Create Boolean Math with operation ‘Equal’. True when both inputs are equal (exclusive nor) |
| [imply](#nodebpy.nodes.geometry.converter.BooleanMath.imply) | Create Boolean Math with operation ‘Imply’. True unless the first input is true and the second is false |
| [l_and](#nodebpy.nodes.geometry.converter.BooleanMath.l_and) | Create Boolean Math with operation ‘And’. True when both inputs are true |
| [l_not](#nodebpy.nodes.geometry.converter.BooleanMath.l_not) | Create Boolean Math with operation ‘Not’. Opposite of the input |
| [l_or](#nodebpy.nodes.geometry.converter.BooleanMath.l_or) | Create Boolean Math with operation ‘Or’. True when at least one input is true |
| [nor](#nodebpy.nodes.geometry.converter.BooleanMath.nor) | Create Boolean Math with operation ‘Nor’. True when both inputs are false |
| [not_and](#nodebpy.nodes.geometry.converter.BooleanMath.not_and) | Create Boolean Math with operation ‘Not And’. True when at least one input is false |
| [not_equal](#nodebpy.nodes.geometry.converter.BooleanMath.not_equal) | Create Boolean Math with operation ‘Not Equal’. True when both inputs are different (exclusive or) |
| [subtract](#nodebpy.nodes.geometry.converter.BooleanMath.subtract) | Create Boolean Math with operation ‘Subtract’. True when the first input is true and the second is false (not imply) |

##### equal

``` python
equal(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Equal’. True when both inputs are equal (exclusive nor)

##### imply

``` python
imply(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Imply’. True unless the first input is true and the second is false

##### l_and

``` python
l_and(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘And’. True when both inputs are true

##### l_not

``` python
l_not(boolean=False)
```

Create Boolean Math with operation ‘Not’. Opposite of the input

##### l_or

``` python
l_or(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Or’. True when at least one input is true

##### nor

``` python
nor(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Nor’. True when both inputs are false

##### not_and

``` python
not_and(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Not And’. True when at least one input is false

##### not_equal

``` python
not_equal(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Not Equal’. True when both inputs are different (exclusive or)

##### subtract

``` python
subtract(boolean=False, boolean_001=False)
```

Create Boolean Math with operation ‘Subtract’. True when the first input is true and the second is false (not imply)

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.boolean`     | `BooleanSocket` | Boolean     |
| `i.boolean_001` | `BooleanSocket` | Boolean     |

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.boolean` | `BooleanSocket` | Boolean     |

### Clamp

``` python
Clamp(value=1.0, min=0.0, max=1.0, *, clamp_type='MINMAX')
```

Clamp a value between a minimum and a maximum

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| value | InputFloat | Value       | `1.0`   |
| min   | InputFloat | Min         | `0.0`   |
| max   | InputFloat | Max         | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`clamp_type`](#nodebpy.nodes.geometry.converter.Clamp.clamp_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.Clamp.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.Clamp.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.Clamp.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.Clamp.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.Clamp.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.Clamp.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.Clamp.type) |  |

#### Methods

| Name | Description |
|----|----|
| [min_max](#nodebpy.nodes.geometry.converter.Clamp.min_max) | Create Clamp with operation ‘Min Max’. Constrain value between min and max |
| [range](#nodebpy.nodes.geometry.converter.Clamp.range) | Create Clamp with operation ‘Range’. Constrain value between min and max, swapping arguments when min \> max |

##### min_max

``` python
min_max(value=1.0, min=0.0, max=1.0)
```

Create Clamp with operation ‘Min Max’. Constrain value between min and max

##### range

``` python
range(value=1.0, min=0.0, max=1.0)
```

Create Clamp with operation ‘Range’. Constrain value between min and max, swapping arguments when min \> max

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.value` | `FloatSocket` | Value       |
| `i.min`   | `FloatSocket` | Min         |
| `i.max`   | `FloatSocket` | Max         |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.result` | `FloatSocket` | Result      |

### CombineBundle

``` python
CombineBundle(define_signature=False)
```

Combine multiple socket values into one.

#### Attributes

| Name | Description |
|----|----|
| [`define_signature`](#nodebpy.nodes.geometry.converter.CombineBundle.define_signature) |  |
| [`i`](#nodebpy.nodes.geometry.converter.CombineBundle.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.CombineBundle.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.CombineBundle.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.CombineBundle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.CombineBundle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.CombineBundle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.CombineBundle.type) |  |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.bundle` | `BundleSocket` | Bundle      |

### CombineColor

``` python
CombineColor(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, mode='RGB')
```

Combine four channels into a single color, based on a particular color model

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| red   | InputFloat | Red         | `0.0`   |
| green | InputFloat | Green       | `0.0`   |
| blue  | InputFloat | Blue        | `0.0`   |
| alpha | InputFloat | Alpha       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.CombineColor.i) |  |
| [`mode`](#nodebpy.nodes.geometry.converter.CombineColor.mode) |  |
| [`name`](#nodebpy.nodes.geometry.converter.CombineColor.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.CombineColor.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.CombineColor.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.CombineColor.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.CombineColor.type) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.geometry.converter.CombineColor.hsl) | Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.geometry.converter.CombineColor.hsv) | Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [rgb](#nodebpy.nodes.geometry.converter.CombineColor.rgb) | Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |

##### hsl

``` python
hsl(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(red=0.0, green=0.0, blue=0.0, alpha=1.0)
```

Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.red`   | `FloatSocket` | Red         |
| `i.green` | `FloatSocket` | Green       |
| `i.blue`  | `FloatSocket` | Blue        |
| `i.alpha` | `FloatSocket` | Alpha       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### CombineMatrix

``` python
CombineMatrix(
    column_1_row_1=1.0,
    column_1_row_2=0.0,
    column_1_row_3=0.0,
    column_1_row_4=0.0,
    column_2_row_1=0.0,
    column_2_row_2=1.0,
    column_2_row_3=0.0,
    column_2_row_4=0.0,
    column_3_row_1=0.0,
    column_3_row_2=0.0,
    column_3_row_3=1.0,
    column_3_row_4=0.0,
    column_4_row_1=0.0,
    column_4_row_2=0.0,
    column_4_row_3=0.0,
    column_4_row_4=1.0,
)
```

Construct a 4x4 matrix from its individual values

#### Parameters

| Name           | Type       | Description    | Default |
|----------------|------------|----------------|---------|
| column_1_row_1 | InputFloat | Column 1 Row 1 | `1.0`   |
| column_1_row_2 | InputFloat | Column 1 Row 2 | `0.0`   |
| column_1_row_3 | InputFloat | Column 1 Row 3 | `0.0`   |
| column_1_row_4 | InputFloat | Column 1 Row 4 | `0.0`   |
| column_2_row_1 | InputFloat | Column 2 Row 1 | `0.0`   |
| column_2_row_2 | InputFloat | Column 2 Row 2 | `1.0`   |
| column_2_row_3 | InputFloat | Column 2 Row 3 | `0.0`   |
| column_2_row_4 | InputFloat | Column 2 Row 4 | `0.0`   |
| column_3_row_1 | InputFloat | Column 3 Row 1 | `0.0`   |
| column_3_row_2 | InputFloat | Column 3 Row 2 | `0.0`   |
| column_3_row_3 | InputFloat | Column 3 Row 3 | `1.0`   |
| column_3_row_4 | InputFloat | Column 3 Row 4 | `0.0`   |
| column_4_row_1 | InputFloat | Column 4 Row 1 | `0.0`   |
| column_4_row_2 | InputFloat | Column 4 Row 2 | `0.0`   |
| column_4_row_3 | InputFloat | Column 4 Row 3 | `0.0`   |
| column_4_row_4 | InputFloat | Column 4 Row 4 | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.CombineMatrix.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.CombineMatrix.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.CombineMatrix.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.CombineMatrix.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.CombineMatrix.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.CombineMatrix.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.CombineMatrix.type) |  |

**Inputs**

| Attribute          | Type          | Description    |
|--------------------|---------------|----------------|
| `i.column_1_row_1` | `FloatSocket` | Column 1 Row 1 |
| `i.column_1_row_2` | `FloatSocket` | Column 1 Row 2 |
| `i.column_1_row_3` | `FloatSocket` | Column 1 Row 3 |
| `i.column_1_row_4` | `FloatSocket` | Column 1 Row 4 |
| `i.column_2_row_1` | `FloatSocket` | Column 2 Row 1 |
| `i.column_2_row_2` | `FloatSocket` | Column 2 Row 2 |
| `i.column_2_row_3` | `FloatSocket` | Column 2 Row 3 |
| `i.column_2_row_4` | `FloatSocket` | Column 2 Row 4 |
| `i.column_3_row_1` | `FloatSocket` | Column 3 Row 1 |
| `i.column_3_row_2` | `FloatSocket` | Column 3 Row 2 |
| `i.column_3_row_3` | `FloatSocket` | Column 3 Row 3 |
| `i.column_3_row_4` | `FloatSocket` | Column 3 Row 4 |
| `i.column_4_row_1` | `FloatSocket` | Column 4 Row 1 |
| `i.column_4_row_2` | `FloatSocket` | Column 4 Row 2 |
| `i.column_4_row_3` | `FloatSocket` | Column 4 Row 3 |
| `i.column_4_row_4` | `FloatSocket` | Column 4 Row 4 |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.matrix` | `MatrixSocket` | Matrix      |

### CombineTransform

``` python
CombineTransform(translation=None, rotation=None, scale=None)
```

Combine a translation vector, a rotation, and a scale vector into a transformation matrix

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| translation | InputVector   | Translation | `None`  |
| rotation    | InputRotation | Rotation    | `None`  |
| scale       | InputVector   | Scale       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.CombineTransform.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.CombineTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.CombineTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.CombineTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.CombineTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.CombineTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.CombineTransform.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.translation` | `VectorSocket`   | Translation |
| `i.rotation`    | `RotationSocket` | Rotation    |
| `i.scale`       | `VectorSocket`   | Scale       |

**Outputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `o.transform` | `MatrixSocket` | Transform   |

### CombineXYZ

``` python
CombineXYZ(x=0.0, y=0.0, z=0.0)
```

Create a vector from X, Y, and Z components

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| x    | InputFloat | X           | `0.0`   |
| y    | InputFloat | Y           | `0.0`   |
| z    | InputFloat | Z           | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.CombineXYZ.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.CombineXYZ.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.CombineXYZ.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.CombineXYZ.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.CombineXYZ.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.CombineXYZ.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.CombineXYZ.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.x`     | `FloatSocket` | X           |
| `i.y`     | `FloatSocket` | Y           |
| `i.z`     | `FloatSocket` | Z           |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### EulerToRotation

``` python
EulerToRotation(euler=None)
```

Build a rotation from separate angles around each axis

#### Parameters

| Name  | Type        | Description | Default |
|-------|-------------|-------------|---------|
| euler | InputVector | Euler       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.EulerToRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.EulerToRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.EulerToRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.EulerToRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.EulerToRotation.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.EulerToRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.EulerToRotation.type) |  |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.euler` | `VectorSocket` | Euler       |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### FindInString

``` python
FindInString(string='', search='')
```

Find the number of times a given string occurs in another string and the position of the first match

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| string | InputString | String      | `''`    |
| search | InputString | Search      | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.FindInString.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.FindInString.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.FindInString.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.FindInString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.FindInString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.FindInString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.FindInString.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.string` | `StringSocket` | String      |
| `i.search` | `StringSocket` | Search      |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.first_found` | `IntegerSocket` | First Found |
| `o.count`       | `IntegerSocket` | Count       |

### FloatToInteger

``` python
FloatToInteger(float=0.0, *, rounding_mode='ROUND')
```

Convert the given floating-point number to an integer, with a choice of methods

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| float | InputFloat | Float       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.FloatToInteger.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.FloatToInteger.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.FloatToInteger.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.FloatToInteger.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.FloatToInteger.outputs) |  |
| [`rounding_mode`](#nodebpy.nodes.geometry.converter.FloatToInteger.rounding_mode) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.FloatToInteger.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.FloatToInteger.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.float` | `FloatSocket` | Float       |

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.integer` | `IntegerSocket` | Integer     |

### GetBundleItem

``` python
GetBundleItem(
    bundle=None,
    path='',
    remove=False,
    *,
    socket_type='FLOAT',
    structure_type='AUTO',
)
```

Retrieve a bundle item by path.

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| bundle | InputBundle  | Bundle      | `None`  |
| path   | InputString  | Path        | `''`    |
| remove | InputBoolean | Remove      | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.GetBundleItem.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.GetBundleItem.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.GetBundleItem.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.GetBundleItem.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.GetBundleItem.outputs) |  |
| [`socket_type`](#nodebpy.nodes.geometry.converter.GetBundleItem.socket_type) |  |
| [`structure_type`](#nodebpy.nodes.geometry.converter.GetBundleItem.structure_type) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.GetBundleItem.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.GetBundleItem.type) |  |

#### Methods

| Name | Description |
|----|----|
| [auto](#nodebpy.nodes.geometry.converter.GetBundleItem.auto) | Create Get Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used |
| [boolean](#nodebpy.nodes.geometry.converter.GetBundleItem.boolean) | Create Get Bundle Item with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.geometry.converter.GetBundleItem.bundle) | Create Get Bundle Item with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.geometry.converter.GetBundleItem.closure) | Create Get Bundle Item with operation ‘Closure’. |
| [collection](#nodebpy.nodes.geometry.converter.GetBundleItem.collection) | Create Get Bundle Item with operation ‘Collection’. |
| [color](#nodebpy.nodes.geometry.converter.GetBundleItem.color) | Create Get Bundle Item with operation ‘Color’. |
| [dynamic](#nodebpy.nodes.geometry.converter.GetBundleItem.dynamic) | Create Get Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures |
| [field](#nodebpy.nodes.geometry.converter.GetBundleItem.field) | Create Get Bundle Item with operation ‘Field’. Socket expects a field |
| [float](#nodebpy.nodes.geometry.converter.GetBundleItem.float) | Create Get Bundle Item with operation ‘Float’. |
| [font](#nodebpy.nodes.geometry.converter.GetBundleItem.font) | Create Get Bundle Item with operation ‘Font’. |
| [geometry](#nodebpy.nodes.geometry.converter.GetBundleItem.geometry) | Create Get Bundle Item with operation ‘Geometry’. |
| [grid](#nodebpy.nodes.geometry.converter.GetBundleItem.grid) | Create Get Bundle Item with operation ‘Grid’. Socket expects a grid |
| [image](#nodebpy.nodes.geometry.converter.GetBundleItem.image) | Create Get Bundle Item with operation ‘Image’. |
| [integer](#nodebpy.nodes.geometry.converter.GetBundleItem.integer) | Create Get Bundle Item with operation ‘Integer’. |
| [list](#nodebpy.nodes.geometry.converter.GetBundleItem.list) | Create Get Bundle Item with operation ‘List’. Socket expects a list |
| [material](#nodebpy.nodes.geometry.converter.GetBundleItem.material) | Create Get Bundle Item with operation ‘Material’. |
| [matrix](#nodebpy.nodes.geometry.converter.GetBundleItem.matrix) | Create Get Bundle Item with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.geometry.converter.GetBundleItem.menu) | Create Get Bundle Item with operation ‘Menu’. |
| [object](#nodebpy.nodes.geometry.converter.GetBundleItem.object) | Create Get Bundle Item with operation ‘Object’. |
| [rotation](#nodebpy.nodes.geometry.converter.GetBundleItem.rotation) | Create Get Bundle Item with operation ‘Rotation’. |
| [single](#nodebpy.nodes.geometry.converter.GetBundleItem.single) | Create Get Bundle Item with operation ‘Single’. Socket expects a single value |
| [string](#nodebpy.nodes.geometry.converter.GetBundleItem.string) | Create Get Bundle Item with operation ‘String’. |
| [vector](#nodebpy.nodes.geometry.converter.GetBundleItem.vector) | Create Get Bundle Item with operation ‘Vector’. |

##### auto

``` python
auto(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used

##### boolean

``` python
boolean(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Boolean’.

##### bundle

``` python
bundle(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Bundle’.

##### closure

``` python
closure(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Closure’.

##### collection

``` python
collection(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Collection’.

##### color

``` python
color(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Color’.

##### dynamic

``` python
dynamic(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures

##### field

``` python
field(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Field’. Socket expects a field

##### float

``` python
float(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Float’.

##### font

``` python
font(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Font’.

##### geometry

``` python
geometry(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Geometry’.

##### grid

``` python
grid(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Grid’. Socket expects a grid

##### image

``` python
image(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Image’.

##### integer

``` python
integer(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Integer’.

##### list

``` python
list(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘List’. Socket expects a list

##### material

``` python
material(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Material’.

##### matrix

``` python
matrix(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Matrix’.

##### menu

``` python
menu(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Menu’.

##### object

``` python
object(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Object’.

##### rotation

``` python
rotation(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Rotation’.

##### single

``` python
single(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Single’. Socket expects a single value

##### string

``` python
string(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘String’.

##### vector

``` python
vector(bundle=None, path='', remove=False)
```

Create Get Bundle Item with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.bundle` | `BundleSocket`  | Bundle      |
| `i.path`   | `StringSocket`  | Path        |
| `i.remove` | `BooleanSocket` | Remove      |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.bundle` | `BundleSocket`  | Bundle      |
| `o.item`   | `FloatSocket`   | Item        |
| `o.exists` | `BooleanSocket` | Exists      |

### HashValue

``` python
HashValue(value=0, seed=0, *, data_type='INT')
```

Generate a randomized integer using the given input value as a seed

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| value | InputInteger | Value       | `0`     |
| seed  | InputInteger | Seed        | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.converter.HashValue.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.HashValue.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.HashValue.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.HashValue.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.HashValue.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.HashValue.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.HashValue.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.HashValue.type) |  |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.geometry.converter.HashValue.color) | Create Hash Value with operation ‘Color’. |
| [float](#nodebpy.nodes.geometry.converter.HashValue.float) | Create Hash Value with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.converter.HashValue.integer) | Create Hash Value with operation ‘Integer’. |
| [matrix](#nodebpy.nodes.geometry.converter.HashValue.matrix) | Create Hash Value with operation ‘Matrix’. |
| [rotation](#nodebpy.nodes.geometry.converter.HashValue.rotation) | Create Hash Value with operation ‘Rotation’. |
| [string](#nodebpy.nodes.geometry.converter.HashValue.string) | Create Hash Value with operation ‘String’. |
| [vector](#nodebpy.nodes.geometry.converter.HashValue.vector) | Create Hash Value with operation ‘Vector’. |

##### color

``` python
color(value=None, seed=0)
```

Create Hash Value with operation ‘Color’.

##### float

``` python
float(value=0.0, seed=0)
```

Create Hash Value with operation ‘Float’.

##### integer

``` python
integer(value=0, seed=0)
```

Create Hash Value with operation ‘Integer’.

##### matrix

``` python
matrix(value=None, seed=0)
```

Create Hash Value with operation ‘Matrix’.

##### rotation

``` python
rotation(value=None, seed=0)
```

Create Hash Value with operation ‘Rotation’.

##### string

``` python
string(value='', seed=0)
```

Create Hash Value with operation ‘String’.

##### vector

``` python
vector(value=None, seed=0)
```

Create Hash Value with operation ‘Vector’.

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.value` | `IntegerSocket` | Value       |
| `i.seed`  | `IntegerSocket` | Seed        |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.hash`  | `IntegerSocket` | Hash        |

### IndexOfNearest

``` python
IndexOfNearest(position=None, group_id=0)
```

Find the nearest element in a group. Similar to the “Sample Nearest” node

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| position | InputVector  | Position    | `None`  |
| group_id | InputInteger | Group ID    | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.IndexOfNearest.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.IndexOfNearest.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.IndexOfNearest.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.IndexOfNearest.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.IndexOfNearest.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.IndexOfNearest.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.IndexOfNearest.type) |  |

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.position` | `VectorSocket`  | Position    |
| `i.group_id` | `IntegerSocket` | Group ID    |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.index`        | `IntegerSocket` | Index        |
| `o.has_neighbor` | `BooleanSocket` | Has Neighbor |

### IntegerMath

``` python
IntegerMath(value=0, value_001=0, value_002=0, *, operation='ADD')
```

Perform various math operations on the given integer inputs

#### Parameters

| Name      | Type         | Description | Default |
|-----------|--------------|-------------|---------|
| value     | InputInteger | Value       | `0`     |
| value_001 | InputInteger | Value       | `0`     |
| value_002 | InputInteger | Value       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.IntegerMath.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.IntegerMath.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.IntegerMath.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.IntegerMath.o) |  |
| [`operation`](#nodebpy.nodes.geometry.converter.IntegerMath.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.IntegerMath.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.IntegerMath.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.IntegerMath.type) |  |

#### Methods

| Name | Description |
|----|----|
| [absolute](#nodebpy.nodes.geometry.converter.IntegerMath.absolute) | Create Integer Math with operation ‘Absolute’. Non-negative value of A, abs(A) |
| [add](#nodebpy.nodes.geometry.converter.IntegerMath.add) | Create Integer Math with operation ‘Add’. A + B |
| [divide](#nodebpy.nodes.geometry.converter.IntegerMath.divide) | Create Integer Math with operation ‘Divide’. A / B |
| [divide_ceiling](#nodebpy.nodes.geometry.converter.IntegerMath.divide_ceiling) | Create Integer Math with operation ‘Divide Ceiling’. Divide and ceil result, the smallest integer greater than or equal A |
| [divide_floor](#nodebpy.nodes.geometry.converter.IntegerMath.divide_floor) | Create Integer Math with operation ‘Divide Floor’. Divide and floor result, the largest integer smaller than or equal A |
| [divide_round](#nodebpy.nodes.geometry.converter.IntegerMath.divide_round) | Create Integer Math with operation ‘Divide Round’. Divide and round result toward zero |
| [floored_modulo](#nodebpy.nodes.geometry.converter.IntegerMath.floored_modulo) | Create Integer Math with operation ‘Floored Modulo’. Modulo that is periodic for both negative and positive operands |
| [greatest_common_divisor](#nodebpy.nodes.geometry.converter.IntegerMath.greatest_common_divisor) | Create Integer Math with operation ‘Greatest Common Divisor’. The largest positive integer that divides into each of the values A and B, e.g. GCD(8,12) = 4 |
| [least_common_multiple](#nodebpy.nodes.geometry.converter.IntegerMath.least_common_multiple) | Create Integer Math with operation ‘Least Common Multiple’. The smallest positive integer that is divisible by both A and B, e.g. LCM(6,10) = 30 |
| [maximum](#nodebpy.nodes.geometry.converter.IntegerMath.maximum) | Create Integer Math with operation ‘Maximum’. The maximum value from A and B, max(A,B) |
| [minimum](#nodebpy.nodes.geometry.converter.IntegerMath.minimum) | Create Integer Math with operation ‘Minimum’. The minimum value from A and B, min(A,B) |
| [modulo](#nodebpy.nodes.geometry.converter.IntegerMath.modulo) | Create Integer Math with operation ‘Modulo’. Modulo which is the remainder of A / B |
| [multiply](#nodebpy.nodes.geometry.converter.IntegerMath.multiply) | Create Integer Math with operation ‘Multiply’. A \* B |
| [multiply_add](#nodebpy.nodes.geometry.converter.IntegerMath.multiply_add) | Create Integer Math with operation ‘Multiply Add’. A \* B + C |
| [negate](#nodebpy.nodes.geometry.converter.IntegerMath.negate) | Create Integer Math with operation ‘Negate’. -A |
| [power](#nodebpy.nodes.geometry.converter.IntegerMath.power) | Create Integer Math with operation ‘Power’. A power B, pow(A,B) |
| [sign](#nodebpy.nodes.geometry.converter.IntegerMath.sign) | Create Integer Math with operation ‘Sign’. Return the sign of A, sign(A) |
| [subtract](#nodebpy.nodes.geometry.converter.IntegerMath.subtract) | Create Integer Math with operation ‘Subtract’. A - B |

##### absolute

``` python
absolute(value=0)
```

Create Integer Math with operation ‘Absolute’. Non-negative value of A, abs(A)

##### add

``` python
add(value=0, value_001=0)
```

Create Integer Math with operation ‘Add’. A + B

##### divide

``` python
divide(value=0, value_001=0)
```

Create Integer Math with operation ‘Divide’. A / B

##### divide_ceiling

``` python
divide_ceiling(value=0, value_001=0)
```

Create Integer Math with operation ‘Divide Ceiling’. Divide and ceil result, the smallest integer greater than or equal A

##### divide_floor

``` python
divide_floor(value=0, value_001=0)
```

Create Integer Math with operation ‘Divide Floor’. Divide and floor result, the largest integer smaller than or equal A

##### divide_round

``` python
divide_round(value=0, value_001=0)
```

Create Integer Math with operation ‘Divide Round’. Divide and round result toward zero

##### floored_modulo

``` python
floored_modulo(value=0, value_001=0)
```

Create Integer Math with operation ‘Floored Modulo’. Modulo that is periodic for both negative and positive operands

##### greatest_common_divisor

``` python
greatest_common_divisor(value=0, value_001=0)
```

Create Integer Math with operation ‘Greatest Common Divisor’. The largest positive integer that divides into each of the values A and B, e.g. GCD(8,12) = 4

##### least_common_multiple

``` python
least_common_multiple(value=0, value_001=0)
```

Create Integer Math with operation ‘Least Common Multiple’. The smallest positive integer that is divisible by both A and B, e.g. LCM(6,10) = 30

##### maximum

``` python
maximum(value=0, value_001=0)
```

Create Integer Math with operation ‘Maximum’. The maximum value from A and B, max(A,B)

##### minimum

``` python
minimum(value=0, value_001=0)
```

Create Integer Math with operation ‘Minimum’. The minimum value from A and B, min(A,B)

##### modulo

``` python
modulo(value=0, value_001=0)
```

Create Integer Math with operation ‘Modulo’. Modulo which is the remainder of A / B

##### multiply

``` python
multiply(value=0, value_001=0)
```

Create Integer Math with operation ‘Multiply’. A \* B

##### multiply_add

``` python
multiply_add(value=0, value_001=0, value_002=0)
```

Create Integer Math with operation ‘Multiply Add’. A \* B + C

##### negate

``` python
negate(value=0)
```

Create Integer Math with operation ‘Negate’. -A

##### power

``` python
power(value=0, value_001=0)
```

Create Integer Math with operation ‘Power’. A power B, pow(A,B)

##### sign

``` python
sign(value=0)
```

Create Integer Math with operation ‘Sign’. Return the sign of A, sign(A)

##### subtract

``` python
subtract(value=0, value_001=0)
```

Create Integer Math with operation ‘Subtract’. A - B

**Inputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `i.value`     | `IntegerSocket` | Value       |
| `i.value_001` | `IntegerSocket` | Value       |
| `i.value_002` | `IntegerSocket` | Value       |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.value` | `IntegerSocket` | Value       |

### InvertMatrix

``` python
InvertMatrix(matrix=None)
```

Compute the inverse of the given matrix, if one exists

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| matrix | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.InvertMatrix.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.InvertMatrix.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.InvertMatrix.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.InvertMatrix.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.InvertMatrix.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.InvertMatrix.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.InvertMatrix.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.matrix` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.matrix`     | `MatrixSocket`  | Matrix      |
| `o.invertible` | `BooleanSocket` | Invertible  |

### InvertRotation

``` python
InvertRotation(rotation=None)
```

Compute the inverse of the given rotation

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| rotation | InputRotation | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.InvertRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.InvertRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.InvertRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.InvertRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.InvertRotation.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.InvertRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.InvertRotation.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.rotation` | `RotationSocket` | Rotation    |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### JoinBundle

``` python
JoinBundle(bundle=None)
```

Join multiple bundles together

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| bundle | InputBundle | Bundle      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.JoinBundle.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.JoinBundle.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.JoinBundle.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.JoinBundle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.JoinBundle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.JoinBundle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.JoinBundle.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.bundle` | `BundleSocket` | Bundle      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.bundle` | `BundleSocket` | Bundle      |

### MapRange

``` python
MapRange(
    value=1.0,
    from_min=0.0,
    from_max=1.0,
    to_min=0.0,
    to_max=1.0,
    steps=4.0,
    vector=None,
    from_min_float3=None,
    from_max_float3=None,
    to_min_float3=None,
    to_max_float3=None,
    steps_float3=None,
    *,
    clamp=False,
    interpolation_type='LINEAR',
    data_type='FLOAT',
)
```

Remap a value from a range to a target range

#### Parameters

| Name            | Type        | Description | Default |
|-----------------|-------------|-------------|---------|
| value           | InputFloat  | Value       | `1.0`   |
| from_min        | InputFloat  | From Min    | `0.0`   |
| from_max        | InputFloat  | From Max    | `1.0`   |
| to_min          | InputFloat  | To Min      | `0.0`   |
| to_max          | InputFloat  | To Max      | `1.0`   |
| steps           | InputFloat  | Steps       | `4.0`   |
| vector          | InputVector | Vector      | `None`  |
| from_min_float3 | InputVector | From Min    | `None`  |
| from_max_float3 | InputVector | From Max    | `None`  |
| to_min_float3   | InputVector | To Min      | `None`  |
| to_max_float3   | InputVector | To Max      | `None`  |
| steps_float3    | InputVector | Steps       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`clamp`](#nodebpy.nodes.geometry.converter.MapRange.clamp) |  |
| [`data_type`](#nodebpy.nodes.geometry.converter.MapRange.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.MapRange.i) |  |
| [`interpolation_type`](#nodebpy.nodes.geometry.converter.MapRange.interpolation_type) |  |
| [`name`](#nodebpy.nodes.geometry.converter.MapRange.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.MapRange.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.MapRange.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.MapRange.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.MapRange.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.MapRange.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.converter.MapRange.float) | Create Map Range with operation ‘Float’. Floating-point value |
| [linear](#nodebpy.nodes.geometry.converter.MapRange.linear) | Create Map Range with operation ‘Linear’. Linear interpolation between From Min and From Max values |
| [smooth_step](#nodebpy.nodes.geometry.converter.MapRange.smooth_step) | Create Map Range with operation ‘Smooth Step’. Smooth Hermite edge interpolation between From Min and From Max values |
| [smoother_step](#nodebpy.nodes.geometry.converter.MapRange.smoother_step) | Create Map Range with operation ‘Smoother Step’. Smoother Hermite edge interpolation between From Min and From Max values |
| [stepped_linear](#nodebpy.nodes.geometry.converter.MapRange.stepped_linear) | Create Map Range with operation ‘Stepped Linear’. Stepped linear interpolation between From Min and From Max values |
| [vector](#nodebpy.nodes.geometry.converter.MapRange.vector) | Create Map Range with operation ‘Vector’. 3D vector with floating-point values |

##### float

``` python
float(value=1.0, from_min=0.0, from_max=1.0, to_min=0.0, to_max=1.0)
```

Create Map Range with operation ‘Float’. Floating-point value

##### linear

``` python
linear(value=1.0, from_min=0.0, from_max=1.0, to_min=0.0, to_max=1.0)
```

Create Map Range with operation ‘Linear’. Linear interpolation between From Min and From Max values

##### smooth_step

``` python
smooth_step(value=1.0, from_min=0.0, from_max=1.0, to_min=0.0, to_max=1.0)
```

Create Map Range with operation ‘Smooth Step’. Smooth Hermite edge interpolation between From Min and From Max values

##### smoother_step

``` python
smoother_step(value=1.0, from_min=0.0, from_max=1.0, to_min=0.0, to_max=1.0)
```

Create Map Range with operation ‘Smoother Step’. Smoother Hermite edge interpolation between From Min and From Max values

##### stepped_linear

``` python
stepped_linear(
    value=1.0,
    from_min=0.0,
    from_max=1.0,
    to_min=0.0,
    to_max=1.0,
    steps=4.0,
)
```

Create Map Range with operation ‘Stepped Linear’. Stepped linear interpolation between From Min and From Max values

##### vector

``` python
vector(vector=None, from_min3=None, from_max3=None, to_min3=None, to_max3=None)
```

Create Map Range with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute           | Type           | Description |
|---------------------|----------------|-------------|
| `i.value`           | `FloatSocket`  | Value       |
| `i.from_min`        | `FloatSocket`  | From Min    |
| `i.from_max`        | `FloatSocket`  | From Max    |
| `i.to_min`          | `FloatSocket`  | To Min      |
| `i.to_max`          | `FloatSocket`  | To Max      |
| `i.steps`           | `FloatSocket`  | Steps       |
| `i.vector`          | `VectorSocket` | Vector      |
| `i.from_min_float3` | `VectorSocket` | From Min    |
| `i.from_max_float3` | `VectorSocket` | From Max    |
| `i.to_min_float3`   | `VectorSocket` | To Min      |
| `i.to_max_float3`   | `VectorSocket` | To Max      |
| `i.steps_float3`    | `VectorSocket` | Steps       |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.result` | `FloatSocket`  | Result      |
| `o.vector` | `VectorSocket` | Vector      |

### MatchString

``` python
MatchString(string='', operation='Starts With', key='')
```

Check if a given string exists within another string

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| string | InputString | String | `''` |
| operation | InputMenu \| Literal\['Starts With', 'Ends With', 'Contains'\] | Operation | `'Starts With'` |
| key | InputString | Key | `''` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.MatchString.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.MatchString.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.MatchString.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.MatchString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.MatchString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.MatchString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.MatchString.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.string`    | `StringSocket` | String      |
| `i.operation` | `MenuSocket`   | Operation   |
| `i.key`       | `StringSocket` | Key         |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.result` | `BooleanSocket` | Result      |

### Math

``` python
Math(
    value=0.5,
    value_001=0.5,
    value_002=0.5,
    *,
    operation='ADD',
    use_clamp=False,
)
```

Perform math operations

#### Parameters

| Name      | Type       | Description | Default |
|-----------|------------|-------------|---------|
| value     | InputFloat | Value       | `0.5`   |
| value_001 | InputFloat | Value       | `0.5`   |
| value_002 | InputFloat | Value       | `0.5`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.Math.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.Math.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.Math.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.Math.o) |  |
| [`operation`](#nodebpy.nodes.geometry.converter.Math.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.Math.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.Math.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.Math.type) |  |
| [`use_clamp`](#nodebpy.nodes.geometry.converter.Math.use_clamp) |  |

#### Methods

| Name | Description |
|----|----|
| [absolute](#nodebpy.nodes.geometry.converter.Math.absolute) | Create Math with operation ‘Absolute’. Magnitude of A |
| [add](#nodebpy.nodes.geometry.converter.Math.add) | Create Math with operation ‘Add’. A + B |
| [arccosine](#nodebpy.nodes.geometry.converter.Math.arccosine) | Create Math with operation ‘Arccosine’. arccos(A) |
| [arcsine](#nodebpy.nodes.geometry.converter.Math.arcsine) | Create Math with operation ‘Arcsine’. arcsin(A) |
| [arctan2](#nodebpy.nodes.geometry.converter.Math.arctan2) | Create Math with operation ‘Arctan2’. The signed angle arctan(A / B) |
| [arctangent](#nodebpy.nodes.geometry.converter.Math.arctangent) | Create Math with operation ‘Arctangent’. arctan(A) |
| [ceil](#nodebpy.nodes.geometry.converter.Math.ceil) | Create Math with operation ‘Ceil’. The smallest integer greater than or equal A |
| [compare](#nodebpy.nodes.geometry.converter.Math.compare) | Create Math with operation ‘Compare’. 1 if (A == B) within tolerance C else 0 |
| [cosine](#nodebpy.nodes.geometry.converter.Math.cosine) | Create Math with operation ‘Cosine’. cos(A) |
| [divide](#nodebpy.nodes.geometry.converter.Math.divide) | Create Math with operation ‘Divide’. A / B |
| [exponent](#nodebpy.nodes.geometry.converter.Math.exponent) | Create Math with operation ‘Exponent’. exp(A) |
| [floor](#nodebpy.nodes.geometry.converter.Math.floor) | Create Math with operation ‘Floor’. The largest integer smaller than or equal A |
| [floored_modulo](#nodebpy.nodes.geometry.converter.Math.floored_modulo) | Create Math with operation ‘Floored Modulo’. The remainder of floored division |
| [fraction](#nodebpy.nodes.geometry.converter.Math.fraction) | Create Math with operation ‘Fraction’. The fraction part of A |
| [greater_than](#nodebpy.nodes.geometry.converter.Math.greater_than) | Create Math with operation ‘Greater Than’. 1 if A \> B else 0 |
| [hyperbolic_cosine](#nodebpy.nodes.geometry.converter.Math.hyperbolic_cosine) | Create Math with operation ‘Hyperbolic Cosine’. cosh(A) |
| [hyperbolic_sine](#nodebpy.nodes.geometry.converter.Math.hyperbolic_sine) | Create Math with operation ‘Hyperbolic Sine’. sinh(A) |
| [hyperbolic_tangent](#nodebpy.nodes.geometry.converter.Math.hyperbolic_tangent) | Create Math with operation ‘Hyperbolic Tangent’. tanh(A) |
| [inverse_square_root](#nodebpy.nodes.geometry.converter.Math.inverse_square_root) | Create Math with operation ‘Inverse Square Root’. 1 / Square root of A |
| [less_than](#nodebpy.nodes.geometry.converter.Math.less_than) | Create Math with operation ‘Less Than’. 1 if A \< B else 0 |
| [logarithm](#nodebpy.nodes.geometry.converter.Math.logarithm) | Create Math with operation ‘Logarithm’. Logarithm A base B |
| [maximum](#nodebpy.nodes.geometry.converter.Math.maximum) | Create Math with operation ‘Maximum’. The maximum from A and B |
| [minimum](#nodebpy.nodes.geometry.converter.Math.minimum) | Create Math with operation ‘Minimum’. The minimum from A and B |
| [multiply](#nodebpy.nodes.geometry.converter.Math.multiply) | Create Math with operation ‘Multiply’. A \* B |
| [multiply_add](#nodebpy.nodes.geometry.converter.Math.multiply_add) | Create Math with operation ‘Multiply Add’. A \* B + C |
| [ping_pong](#nodebpy.nodes.geometry.converter.Math.ping_pong) | Create Math with operation ‘Ping-Pong’. Wraps a value and reverses every other cycle (A,B) |
| [power](#nodebpy.nodes.geometry.converter.Math.power) | Create Math with operation ‘Power’. A power B |
| [round](#nodebpy.nodes.geometry.converter.Math.round) | Create Math with operation ‘Round’. Round A to the nearest integer. Round upward if the fraction part is 0.5 |
| [sign](#nodebpy.nodes.geometry.converter.Math.sign) | Create Math with operation ‘Sign’. Returns the sign of A |
| [sine](#nodebpy.nodes.geometry.converter.Math.sine) | Create Math with operation ‘Sine’. sin(A) |
| [smooth_maximum](#nodebpy.nodes.geometry.converter.Math.smooth_maximum) | Create Math with operation ‘Smooth Maximum’. The maximum from A and B with smoothing C |
| [smooth_minimum](#nodebpy.nodes.geometry.converter.Math.smooth_minimum) | Create Math with operation ‘Smooth Minimum’. The minimum from A and B with smoothing C |
| [snap](#nodebpy.nodes.geometry.converter.Math.snap) | Create Math with operation ‘Snap’. Snap to increment, snap(A,B) |
| [square_root](#nodebpy.nodes.geometry.converter.Math.square_root) | Create Math with operation ‘Square Root’. Square root of A |
| [subtract](#nodebpy.nodes.geometry.converter.Math.subtract) | Create Math with operation ‘Subtract’. A - B |
| [tangent](#nodebpy.nodes.geometry.converter.Math.tangent) | Create Math with operation ‘Tangent’. tan(A) |
| [to_degrees](#nodebpy.nodes.geometry.converter.Math.to_degrees) | Create Math with operation ‘To Degrees’. Convert from radians to degrees |
| [to_radians](#nodebpy.nodes.geometry.converter.Math.to_radians) | Create Math with operation ‘To Radians’. Convert from degrees to radians |
| [truncate](#nodebpy.nodes.geometry.converter.Math.truncate) | Create Math with operation ‘Truncate’. The integer part of A, removing fractional digits |
| [truncated_modulo](#nodebpy.nodes.geometry.converter.Math.truncated_modulo) | Create Math with operation ‘Truncated Modulo’. The remainder of truncated division using fmod(A,B) |
| [wrap](#nodebpy.nodes.geometry.converter.Math.wrap) | Create Math with operation ‘Wrap’. Wrap value to range, wrap(A,B) |

##### absolute

``` python
absolute(value=0.5)
```

Create Math with operation ‘Absolute’. Magnitude of A

##### add

``` python
add(value=0.5, value_001=0.5)
```

Create Math with operation ‘Add’. A + B

##### arccosine

``` python
arccosine(value=0.5)
```

Create Math with operation ‘Arccosine’. arccos(A)

##### arcsine

``` python
arcsine(value=0.5)
```

Create Math with operation ‘Arcsine’. arcsin(A)

##### arctan2

``` python
arctan2(value=0.5, value_001=0.5)
```

Create Math with operation ‘Arctan2’. The signed angle arctan(A / B)

##### arctangent

``` python
arctangent(value=0.5)
```

Create Math with operation ‘Arctangent’. arctan(A)

##### ceil

``` python
ceil(value=0.5)
```

Create Math with operation ‘Ceil’. The smallest integer greater than or equal A

##### compare

``` python
compare(value=0.5, value_001=0.5, value_002=0.5)
```

Create Math with operation ‘Compare’. 1 if (A == B) within tolerance C else 0

##### cosine

``` python
cosine(value=0.5)
```

Create Math with operation ‘Cosine’. cos(A)

##### divide

``` python
divide(value=0.5, value_001=0.5)
```

Create Math with operation ‘Divide’. A / B

##### exponent

``` python
exponent(value=0.5)
```

Create Math with operation ‘Exponent’. exp(A)

##### floor

``` python
floor(value=0.5)
```

Create Math with operation ‘Floor’. The largest integer smaller than or equal A

##### floored_modulo

``` python
floored_modulo(value=0.5, value_001=0.5)
```

Create Math with operation ‘Floored Modulo’. The remainder of floored division

##### fraction

``` python
fraction(value=0.5)
```

Create Math with operation ‘Fraction’. The fraction part of A

##### greater_than

``` python
greater_than(value=0.5, value_001=0.5)
```

Create Math with operation ‘Greater Than’. 1 if A \> B else 0

##### hyperbolic_cosine

``` python
hyperbolic_cosine(value=0.5)
```

Create Math with operation ‘Hyperbolic Cosine’. cosh(A)

##### hyperbolic_sine

``` python
hyperbolic_sine(value=0.5)
```

Create Math with operation ‘Hyperbolic Sine’. sinh(A)

##### hyperbolic_tangent

``` python
hyperbolic_tangent(value=0.5)
```

Create Math with operation ‘Hyperbolic Tangent’. tanh(A)

##### inverse_square_root

``` python
inverse_square_root(value=0.5)
```

Create Math with operation ‘Inverse Square Root’. 1 / Square root of A

##### less_than

``` python
less_than(value=0.5, value_001=0.5)
```

Create Math with operation ‘Less Than’. 1 if A \< B else 0

##### logarithm

``` python
logarithm(value=0.5, value_001=0.5)
```

Create Math with operation ‘Logarithm’. Logarithm A base B

##### maximum

``` python
maximum(value=0.5, value_001=0.5)
```

Create Math with operation ‘Maximum’. The maximum from A and B

##### minimum

``` python
minimum(value=0.5, value_001=0.5)
```

Create Math with operation ‘Minimum’. The minimum from A and B

##### multiply

``` python
multiply(value=0.5, value_001=0.5)
```

Create Math with operation ‘Multiply’. A \* B

##### multiply_add

``` python
multiply_add(value=0.5, value_001=0.5, value_002=0.5)
```

Create Math with operation ‘Multiply Add’. A \* B + C

##### ping_pong

``` python
ping_pong(value=0.5, value_001=0.5)
```

Create Math with operation ‘Ping-Pong’. Wraps a value and reverses every other cycle (A,B)

##### power

``` python
power(value=0.5, value_001=0.5)
```

Create Math with operation ‘Power’. A power B

##### round

``` python
round(value=0.5)
```

Create Math with operation ‘Round’. Round A to the nearest integer. Round upward if the fraction part is 0.5

##### sign

``` python
sign(value=0.5)
```

Create Math with operation ‘Sign’. Returns the sign of A

##### sine

``` python
sine(value=0.5)
```

Create Math with operation ‘Sine’. sin(A)

##### smooth_maximum

``` python
smooth_maximum(value=0.5, value_001=0.5, value_002=0.5)
```

Create Math with operation ‘Smooth Maximum’. The maximum from A and B with smoothing C

##### smooth_minimum

``` python
smooth_minimum(value=0.5, value_001=0.5, value_002=0.5)
```

Create Math with operation ‘Smooth Minimum’. The minimum from A and B with smoothing C

##### snap

``` python
snap(value=0.5, value_001=0.5)
```

Create Math with operation ‘Snap’. Snap to increment, snap(A,B)

##### square_root

``` python
square_root(value=0.5)
```

Create Math with operation ‘Square Root’. Square root of A

##### subtract

``` python
subtract(value=0.5, value_001=0.5)
```

Create Math with operation ‘Subtract’. A - B

##### tangent

``` python
tangent(value=0.5)
```

Create Math with operation ‘Tangent’. tan(A)

##### to_degrees

``` python
to_degrees(value=0.5)
```

Create Math with operation ‘To Degrees’. Convert from radians to degrees

##### to_radians

``` python
to_radians(value=0.5)
```

Create Math with operation ‘To Radians’. Convert from degrees to radians

##### truncate

``` python
truncate(value=0.5)
```

Create Math with operation ‘Truncate’. The integer part of A, removing fractional digits

##### truncated_modulo

``` python
truncated_modulo(value=0.5, value_001=0.5)
```

Create Math with operation ‘Truncated Modulo’. The remainder of truncated division using fmod(A,B)

##### wrap

``` python
wrap(value=0.5, value_001=0.5, value_002=0.5)
```

Create Math with operation ‘Wrap’. Wrap value to range, wrap(A,B)

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.value`     | `FloatSocket` | Value       |
| `i.value_001` | `FloatSocket` | Value       |
| `i.value_002` | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### MatrixDeterminant

``` python
MatrixDeterminant(matrix=None)
```

Compute the determinant of the given matrix

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| matrix | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.MatrixDeterminant.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.matrix` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `o.determinant` | `FloatSocket` | Determinant |

### MatrixSVD

``` python
MatrixSVD(matrix=None)
```

Compute the singular value decomposition of the 3x3 part of a matrix

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| matrix | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.MatrixSVD.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.MatrixSVD.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.MatrixSVD.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.MatrixSVD.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.MatrixSVD.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.MatrixSVD.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.MatrixSVD.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.matrix` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.u`     | `MatrixSocket` | U           |
| `o.s`     | `VectorSocket` | S           |
| `o.v`     | `MatrixSocket` | V           |

### Mix

``` python
Mix(
    factor_float=0.5,
    factor_vector=None,
    a_float=0.0,
    b_float=0.0,
    a_vector=None,
    b_vector=None,
    a_color=None,
    b_color=None,
    a_rotation=None,
    b_rotation=None,
    *,
    data_type='FLOAT',
    factor_mode='UNIFORM',
    blend_type='MIX',
    clamp_factor=False,
    clamp_result=False,
)
```

Mix values by a factor

#### Parameters

| Name          | Type          | Description | Default |
|---------------|---------------|-------------|---------|
| factor_float  | InputFloat    | Factor      | `0.5`   |
| factor_vector | InputVector   | Factor      | `None`  |
| a_float       | InputFloat    | A           | `0.0`   |
| b_float       | InputFloat    | B           | `0.0`   |
| a_vector      | InputVector   | A           | `None`  |
| b_vector      | InputVector   | B           | `None`  |
| a_color       | InputColor    | A           | `None`  |
| b_color       | InputColor    | B           | `None`  |
| a_rotation    | InputRotation | A           | `None`  |
| b_rotation    | InputRotation | B           | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`blend_type`](#nodebpy.nodes.geometry.converter.Mix.blend_type) |  |
| [`clamp_factor`](#nodebpy.nodes.geometry.converter.Mix.clamp_factor) |  |
| [`clamp_result`](#nodebpy.nodes.geometry.converter.Mix.clamp_result) |  |
| [`data_type`](#nodebpy.nodes.geometry.converter.Mix.data_type) |  |
| [`factor_mode`](#nodebpy.nodes.geometry.converter.Mix.factor_mode) |  |
| [`i`](#nodebpy.nodes.geometry.converter.Mix.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.Mix.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.Mix.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.Mix.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.Mix.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.Mix.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.Mix.type) |  |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.geometry.converter.Mix.color) | Create Mix with operation ‘Color’. |
| [float](#nodebpy.nodes.geometry.converter.Mix.float) | Create Mix with operation ‘Float’. |
| [rotation](#nodebpy.nodes.geometry.converter.Mix.rotation) | Create Mix with operation ‘Rotation’. |
| [vector](#nodebpy.nodes.geometry.converter.Mix.vector) | Create Mix with operation ‘Vector’. |

##### color

``` python
color(factor=0.5, a_color=None, b_color=None)
```

Create Mix with operation ‘Color’.

##### float

``` python
float(factor=0.5, a=0.0, b=0.0)
```

Create Mix with operation ‘Float’.

##### rotation

``` python
rotation(factor=0.5, a_rotation=None, b_rotation=None)
```

Create Mix with operation ‘Rotation’.

##### vector

``` python
vector(factor=0.5, a=None, b=None)
```

Create Mix with operation ‘Vector’.

**Inputs**

| Attribute         | Type             | Description |
|-------------------|------------------|-------------|
| `i.factor_float`  | `FloatSocket`    | Factor      |
| `i.factor_vector` | `VectorSocket`   | Factor      |
| `i.a_float`       | `FloatSocket`    | A           |
| `i.b_float`       | `FloatSocket`    | B           |
| `i.a_vector`      | `VectorSocket`   | A           |
| `i.b_vector`      | `VectorSocket`   | B           |
| `i.a_color`       | `ColorSocket`    | A           |
| `i.b_color`       | `ColorSocket`    | B           |
| `i.a_rotation`    | `RotationSocket` | A           |
| `i.b_rotation`    | `RotationSocket` | B           |

**Outputs**

| Attribute           | Type             | Description |
|---------------------|------------------|-------------|
| `o.result_float`    | `FloatSocket`    | Result      |
| `o.result_vector`   | `VectorSocket`   | Result      |
| `o.result_color`    | `ColorSocket`    | Result      |
| `o.result_rotation` | `RotationSocket` | Result      |

### MultiplyMatrices

``` python
MultiplyMatrices(matrix=None, matrix_001=None)
```

Perform a matrix multiplication on two input matrices

#### Parameters

| Name       | Type        | Description | Default |
|------------|-------------|-------------|---------|
| matrix     | InputMatrix | Matrix      | `None`  |
| matrix_001 | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.MultiplyMatrices.type) |  |

**Inputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `i.matrix`     | `MatrixSocket` | Matrix      |
| `i.matrix_001` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.matrix` | `MatrixSocket` | Matrix      |

### PackUVIslands

``` python
PackUVIslands(
    uv=None,
    selection=True,
    margin=0.001,
    rotate=True,
    method='Bounding Box',
    bottom_left=None,
    top_right=None,
)
```

Scale islands of a UV map and move them so they fill the UV space as much as possible

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| uv | InputVector | UV | `None` |
| selection | InputBoolean | Selection | `True` |
| margin | InputFloat | Margin | `0.001` |
| rotate | InputBoolean | Rotate | `True` |
| method | InputMenu \| Literal\['Bounding Box', 'Convex Hull', 'Exact Shape'\] | Method | `'Bounding Box'` |
| bottom_left | InputVector | Bottom Left | `None` |
| top_right | InputVector | Top Right | `None` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.PackUVIslands.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.PackUVIslands.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.PackUVIslands.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.PackUVIslands.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.PackUVIslands.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.PackUVIslands.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.PackUVIslands.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.uv`          | `VectorSocket`  | UV          |
| `i.selection`   | `BooleanSocket` | Selection   |
| `i.margin`      | `FloatSocket`   | Margin      |
| `i.rotate`      | `BooleanSocket` | Rotate      |
| `i.method`      | `MenuSocket`    | Method      |
| `i.bottom_left` | `VectorSocket`  | Bottom Left |
| `i.top_right`   | `VectorSocket`  | Top Right   |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### ProjectPoint

``` python
ProjectPoint(vector=None, transform=None)
```

Project a point using a matrix, using location, rotation, scale, and perspective divide

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| vector    | InputVector | Vector      | `None`  |
| transform | InputMatrix | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.ProjectPoint.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.ProjectPoint.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.ProjectPoint.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.ProjectPoint.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.ProjectPoint.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.ProjectPoint.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.ProjectPoint.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.vector`    | `VectorSocket` | Vector      |
| `i.transform` | `MatrixSocket` | Transform   |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### QuaternionToRotation

``` python
QuaternionToRotation(w=1.0, x=0.0, y=0.0, z=0.0)
```

Build a rotation from quaternion components

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| w    | InputFloat | W           | `1.0`   |
| x    | InputFloat | X           | `0.0`   |
| y    | InputFloat | Y           | `0.0`   |
| z    | InputFloat | Z           | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.QuaternionToRotation.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.w`     | `FloatSocket` | W           |
| `i.x`     | `FloatSocket` | X           |
| `i.y`     | `FloatSocket` | Y           |
| `i.z`     | `FloatSocket` | Z           |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### RandomValue

``` python
RandomValue(
    min=None,
    max=None,
    min_001=0.0,
    max_001=1.0,
    min_002=0,
    max_002=100,
    probability=0.5,
    id=0,
    seed=0,
    *,
    data_type='FLOAT',
)
```

Output a randomized value

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| min         | InputVector  | Min         | `None`  |
| max         | InputVector  | Max         | `None`  |
| min_001     | InputFloat   | Min         | `0.0`   |
| max_001     | InputFloat   | Max         | `1.0`   |
| min_002     | InputInteger | Min         | `0`     |
| max_002     | InputInteger | Max         | `100`   |
| probability | InputFloat   | Probability | `0.5`   |
| id          | InputInteger | ID          | `0`     |
| seed        | InputInteger | Seed        | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.converter.RandomValue.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.RandomValue.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RandomValue.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RandomValue.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RandomValue.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RandomValue.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RandomValue.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RandomValue.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.converter.RandomValue.boolean) | Create Random Value with operation ‘Boolean’. True or false |
| [float](#nodebpy.nodes.geometry.converter.RandomValue.float) | Create Random Value with operation ‘Float’. Floating-point value |
| [integer](#nodebpy.nodes.geometry.converter.RandomValue.integer) | Create Random Value with operation ‘Integer’. 32-bit integer |
| [vector](#nodebpy.nodes.geometry.converter.RandomValue.vector) | Create Random Value with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(probability=0.5, id=0, seed=0)
```

Create Random Value with operation ‘Boolean’. True or false

##### float

``` python
float(min=0.0, max=1.0, id=0, seed=0)
```

Create Random Value with operation ‘Float’. Floating-point value

##### integer

``` python
integer(min=0, max=100, id=0, seed=0)
```

Create Random Value with operation ‘Integer’. 32-bit integer

##### vector

``` python
vector(min=None, max=None, id=0, seed=0)
```

Create Random Value with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.min`         | `VectorSocket`  | Min         |
| `i.max`         | `VectorSocket`  | Max         |
| `i.min_001`     | `FloatSocket`   | Min         |
| `i.max_001`     | `FloatSocket`   | Max         |
| `i.min_002`     | `IntegerSocket` | Min         |
| `i.max_002`     | `IntegerSocket` | Max         |
| `i.probability` | `FloatSocket`   | Probability |
| `i.id`          | `IntegerSocket` | ID          |
| `i.seed`        | `IntegerSocket` | Seed        |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.value`     | `VectorSocket`  | Value       |
| `o.value_001` | `FloatSocket`   | Value       |
| `o.value_002` | `IntegerSocket` | Value       |
| `o.value_003` | `BooleanSocket` | Value       |

### ReplaceString

``` python
ReplaceString(string='', find='', replace='')
```

Replace a given string segment with another

#### Parameters

| Name    | Type        | Description | Default |
|---------|-------------|-------------|---------|
| string  | InputString | String      | `''`    |
| find    | InputString | Find        | `''`    |
| replace | InputString | Replace     | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.ReplaceString.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.ReplaceString.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.ReplaceString.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.ReplaceString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.ReplaceString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.ReplaceString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.ReplaceString.type) |  |

**Inputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `i.string`  | `StringSocket` | String      |
| `i.find`    | `StringSocket` | Find        |
| `i.replace` | `StringSocket` | Replace     |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.string` | `StringSocket` | String      |

### RotateEuler

``` python
RotateEuler(
    rotation=None,
    rotate_by=None,
    axis=None,
    angle=0.0,
    *,
    rotation_type='EULER',
    space='OBJECT',
)
```

Apply a secondary Euler rotation to a given Euler rotation

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| rotation  | InputVector | Rotation    | `None`  |
| rotate_by | InputVector | Rotate By   | `None`  |
| axis      | InputVector | Axis        | `None`  |
| angle     | InputFloat  | Angle       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotateEuler.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotateEuler.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotateEuler.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotateEuler.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotateEuler.outputs) |  |
| [`rotation_type`](#nodebpy.nodes.geometry.converter.RotateEuler.rotation_type) |  |
| [`space`](#nodebpy.nodes.geometry.converter.RotateEuler.space) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotateEuler.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotateEuler.type) |  |

#### Methods

| Name | Description |
|----|----|
| [axis_angle](#nodebpy.nodes.geometry.converter.RotateEuler.axis_angle) | Create Rotate Euler with operation ‘Axis Angle’. Rotate around an axis by an angle |
| [euler](#nodebpy.nodes.geometry.converter.RotateEuler.euler) | Create Rotate Euler with operation ‘Euler’. Rotate around the X, Y, and Z axes |

##### axis_angle

``` python
axis_angle(rotation=None, axis=None, angle=0.0)
```

Create Rotate Euler with operation ‘Axis Angle’. Rotate around an axis by an angle

##### euler

``` python
euler(rotation=None, rotate_by=None)
```

Create Rotate Euler with operation ‘Euler’. Rotate around the X, Y, and Z axes

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.rotation`  | `VectorSocket` | Rotation    |
| `i.rotate_by` | `VectorSocket` | Rotate By   |
| `i.axis`      | `VectorSocket` | Axis        |
| `i.angle`     | `FloatSocket`  | Angle       |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.rotation` | `VectorSocket` | Rotation    |

### RotateRotation

``` python
RotateRotation(rotation=None, rotate_by=None, *, rotation_space='GLOBAL')
```

Apply a secondary rotation to a given rotation value

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| rotation  | InputRotation | Rotation    | `None`  |
| rotate_by | InputRotation | Rotate By   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotateRotation.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotateRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotateRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotateRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotateRotation.outputs) |  |
| [`rotation_space`](#nodebpy.nodes.geometry.converter.RotateRotation.rotation_space) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotateRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotateRotation.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.rotation`  | `RotationSocket` | Rotation    |
| `i.rotate_by` | `RotationSocket` | Rotate By   |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### RotateVector

``` python
RotateVector(vector=None, rotation=None)
```

Apply a rotation to a given vector

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| vector   | InputVector   | Vector      | `None`  |
| rotation | InputRotation | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotateVector.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotateVector.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotateVector.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotateVector.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotateVector.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotateVector.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotateVector.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.vector`   | `VectorSocket`   | Vector      |
| `i.rotation` | `RotationSocket` | Rotation    |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### RotationToAxisAngle

``` python
RotationToAxisAngle(rotation=None)
```

Convert a rotation to axis angle components

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| rotation | InputRotation | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotationToAxisAngle.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.rotation` | `RotationSocket` | Rotation    |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.axis`  | `VectorSocket` | Axis        |
| `o.angle` | `FloatSocket`  | Angle       |

### RotationToEuler

``` python
RotationToEuler(rotation=None)
```

Convert a standard rotation value to an Euler rotation

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| rotation | InputRotation | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotationToEuler.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotationToEuler.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotationToEuler.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotationToEuler.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotationToEuler.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotationToEuler.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotationToEuler.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.rotation` | `RotationSocket` | Rotation    |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.euler` | `VectorSocket` | Euler       |

### RotationToQuaternion

``` python
RotationToQuaternion(rotation=None)
```

Retrieve the quaternion components representing a rotation

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| rotation | InputRotation | Rotation    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.RotationToQuaternion.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.rotation` | `RotationSocket` | Rotation    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.w`     | `FloatSocket` | W           |
| `o.x`     | `FloatSocket` | X           |
| `o.y`     | `FloatSocket` | Y           |
| `o.z`     | `FloatSocket` | Z           |

### SeparateBundle

``` python
SeparateBundle(bundle=None, *, define_signature=False)
```

Split a bundle into multiple sockets.

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| bundle | InputBundle | Bundle      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`define_signature`](#nodebpy.nodes.geometry.converter.SeparateBundle.define_signature) |  |
| [`i`](#nodebpy.nodes.geometry.converter.SeparateBundle.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SeparateBundle.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SeparateBundle.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SeparateBundle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SeparateBundle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SeparateBundle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SeparateBundle.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.bundle` | `BundleSocket` | Bundle      |

### SeparateColor

``` python
SeparateColor(color=None, *, mode='RGB')
```

Split a color into separate channels, based on a particular color model

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| color | InputColor | Color       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.SeparateColor.i) |  |
| [`mode`](#nodebpy.nodes.geometry.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SeparateColor.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SeparateColor.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SeparateColor.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SeparateColor.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SeparateColor.type) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.geometry.converter.SeparateColor.hsl) | Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.geometry.converter.SeparateColor.hsv) | Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [rgb](#nodebpy.nodes.geometry.converter.SeparateColor.rgb) | Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |

##### hsl

``` python
hsl(color=None)
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(color=None)
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

##### rgb

``` python
rgb(color=None)
```

Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.color` | `ColorSocket` | Color       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.red`   | `FloatSocket` | Red         |
| `o.green` | `FloatSocket` | Green       |
| `o.blue`  | `FloatSocket` | Blue        |
| `o.alpha` | `FloatSocket` | Alpha       |

### SeparateMatrix

``` python
SeparateMatrix(matrix=None)
```

Split a 4x4 matrix into its individual values

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| matrix | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.SeparateMatrix.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SeparateMatrix.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SeparateMatrix.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SeparateMatrix.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SeparateMatrix.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SeparateMatrix.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SeparateMatrix.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.matrix` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute          | Type          | Description    |
|--------------------|---------------|----------------|
| `o.column_1_row_1` | `FloatSocket` | Column 1 Row 1 |
| `o.column_1_row_2` | `FloatSocket` | Column 1 Row 2 |
| `o.column_1_row_3` | `FloatSocket` | Column 1 Row 3 |
| `o.column_1_row_4` | `FloatSocket` | Column 1 Row 4 |
| `o.column_2_row_1` | `FloatSocket` | Column 2 Row 1 |
| `o.column_2_row_2` | `FloatSocket` | Column 2 Row 2 |
| `o.column_2_row_3` | `FloatSocket` | Column 2 Row 3 |
| `o.column_2_row_4` | `FloatSocket` | Column 2 Row 4 |
| `o.column_3_row_1` | `FloatSocket` | Column 3 Row 1 |
| `o.column_3_row_2` | `FloatSocket` | Column 3 Row 2 |
| `o.column_3_row_3` | `FloatSocket` | Column 3 Row 3 |
| `o.column_3_row_4` | `FloatSocket` | Column 3 Row 4 |
| `o.column_4_row_1` | `FloatSocket` | Column 4 Row 1 |
| `o.column_4_row_2` | `FloatSocket` | Column 4 Row 2 |
| `o.column_4_row_3` | `FloatSocket` | Column 4 Row 3 |
| `o.column_4_row_4` | `FloatSocket` | Column 4 Row 4 |

### SeparateTransform

``` python
SeparateTransform(transform=None)
```

Split a transformation matrix into a translation vector, a rotation, and a scale vector

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| transform | InputMatrix | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.SeparateTransform.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SeparateTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SeparateTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SeparateTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SeparateTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SeparateTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SeparateTransform.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.transform` | `MatrixSocket` | Transform   |

**Outputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `o.translation` | `VectorSocket`   | Translation |
| `o.rotation`    | `RotationSocket` | Rotation    |
| `o.scale`       | `VectorSocket`   | Scale       |

### SeparateXYZ

``` python
SeparateXYZ(vector=None)
```

Split a vector into its X, Y, and Z components

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| vector | InputVector | Vector      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.SeparateXYZ.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SeparateXYZ.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SeparateXYZ.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SeparateXYZ.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SeparateXYZ.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SeparateXYZ.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SeparateXYZ.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.vector` | `VectorSocket` | Vector      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.x`     | `FloatSocket` | X           |
| `o.y`     | `FloatSocket` | Y           |
| `o.z`     | `FloatSocket` | Z           |

### SliceString

``` python
SliceString(string='', position=0, length=10)
```

Extract a string segment from a larger string

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| string   | InputString  | String      | `''`    |
| position | InputInteger | Position    | `0`     |
| length   | InputInteger | Length      | `10`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.SliceString.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.SliceString.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.SliceString.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.SliceString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.SliceString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.SliceString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.SliceString.type) |  |

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.string`   | `StringSocket`  | String      |
| `i.position` | `IntegerSocket` | Position    |
| `i.length`   | `IntegerSocket` | Length      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.string` | `StringSocket` | String      |

### StoreBundleItem

``` python
StoreBundleItem(
    bundle=None,
    path='',
    item=0.0,
    *,
    socket_type='FLOAT',
    structure_type='AUTO',
)
```

Store a bundle item by path and data type.

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| bundle | InputBundle | Bundle      | `None`  |
| path   | InputString | Path        | `''`    |
| item   | InputFloat  | Item        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.StoreBundleItem.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.StoreBundleItem.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.StoreBundleItem.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.StoreBundleItem.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.StoreBundleItem.outputs) |  |
| [`socket_type`](#nodebpy.nodes.geometry.converter.StoreBundleItem.socket_type) |  |
| [`structure_type`](#nodebpy.nodes.geometry.converter.StoreBundleItem.structure_type) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.StoreBundleItem.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.StoreBundleItem.type) |  |

#### Methods

| Name | Description |
|----|----|
| [auto](#nodebpy.nodes.geometry.converter.StoreBundleItem.auto) | Create Store Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used |
| [boolean](#nodebpy.nodes.geometry.converter.StoreBundleItem.boolean) | Create Store Bundle Item with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.geometry.converter.StoreBundleItem.bundle) | Create Store Bundle Item with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.geometry.converter.StoreBundleItem.closure) | Create Store Bundle Item with operation ‘Closure’. |
| [collection](#nodebpy.nodes.geometry.converter.StoreBundleItem.collection) | Create Store Bundle Item with operation ‘Collection’. |
| [color](#nodebpy.nodes.geometry.converter.StoreBundleItem.color) | Create Store Bundle Item with operation ‘Color’. |
| [dynamic](#nodebpy.nodes.geometry.converter.StoreBundleItem.dynamic) | Create Store Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures |
| [field](#nodebpy.nodes.geometry.converter.StoreBundleItem.field) | Create Store Bundle Item with operation ‘Field’. Socket expects a field |
| [float](#nodebpy.nodes.geometry.converter.StoreBundleItem.float) | Create Store Bundle Item with operation ‘Float’. |
| [font](#nodebpy.nodes.geometry.converter.StoreBundleItem.font) | Create Store Bundle Item with operation ‘Font’. |
| [geometry](#nodebpy.nodes.geometry.converter.StoreBundleItem.geometry) | Create Store Bundle Item with operation ‘Geometry’. |
| [grid](#nodebpy.nodes.geometry.converter.StoreBundleItem.grid) | Create Store Bundle Item with operation ‘Grid’. Socket expects a grid |
| [image](#nodebpy.nodes.geometry.converter.StoreBundleItem.image) | Create Store Bundle Item with operation ‘Image’. |
| [integer](#nodebpy.nodes.geometry.converter.StoreBundleItem.integer) | Create Store Bundle Item with operation ‘Integer’. |
| [list](#nodebpy.nodes.geometry.converter.StoreBundleItem.list) | Create Store Bundle Item with operation ‘List’. Socket expects a list |
| [material](#nodebpy.nodes.geometry.converter.StoreBundleItem.material) | Create Store Bundle Item with operation ‘Material’. |
| [matrix](#nodebpy.nodes.geometry.converter.StoreBundleItem.matrix) | Create Store Bundle Item with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.geometry.converter.StoreBundleItem.menu) | Create Store Bundle Item with operation ‘Menu’. |
| [object](#nodebpy.nodes.geometry.converter.StoreBundleItem.object) | Create Store Bundle Item with operation ‘Object’. |
| [rotation](#nodebpy.nodes.geometry.converter.StoreBundleItem.rotation) | Create Store Bundle Item with operation ‘Rotation’. |
| [single](#nodebpy.nodes.geometry.converter.StoreBundleItem.single) | Create Store Bundle Item with operation ‘Single’. Socket expects a single value |
| [string](#nodebpy.nodes.geometry.converter.StoreBundleItem.string) | Create Store Bundle Item with operation ‘String’. |
| [vector](#nodebpy.nodes.geometry.converter.StoreBundleItem.vector) | Create Store Bundle Item with operation ‘Vector’. |

##### auto

``` python
auto(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used

##### boolean

``` python
boolean(bundle=None, path='', item=False)
```

Create Store Bundle Item with operation ‘Boolean’.

##### bundle

``` python
bundle(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Bundle’.

##### closure

``` python
closure(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Closure’.

##### collection

``` python
collection(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Collection’.

##### color

``` python
color(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Color’.

##### dynamic

``` python
dynamic(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures

##### field

``` python
field(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Field’. Socket expects a field

##### float

``` python
float(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Float’.

##### font

``` python
font(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Font’.

##### geometry

``` python
geometry(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Geometry’.

##### grid

``` python
grid(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Grid’. Socket expects a grid

##### image

``` python
image(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Image’.

##### integer

``` python
integer(bundle=None, path='', item=0)
```

Create Store Bundle Item with operation ‘Integer’.

##### list

``` python
list(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘List’. Socket expects a list

##### material

``` python
material(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Material’.

##### matrix

``` python
matrix(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Matrix’.

##### menu

``` python
menu(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Menu’.

##### object

``` python
object(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Object’.

##### rotation

``` python
rotation(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Rotation’.

##### single

``` python
single(bundle=None, path='', item=0.0)
```

Create Store Bundle Item with operation ‘Single’. Socket expects a single value

##### string

``` python
string(bundle=None, path='', item='')
```

Create Store Bundle Item with operation ‘String’.

##### vector

``` python
vector(bundle=None, path='', item=None)
```

Create Store Bundle Item with operation ‘Vector’.

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.bundle` | `BundleSocket` | Bundle      |
| `i.path`   | `StringSocket` | Path        |
| `i.item`   | `FloatSocket`  | Item        |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.bundle` | `BundleSocket` | Bundle      |

### StringLength

``` python
StringLength(string='')
```

Output the number of characters in the given string

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| string | InputString | String      | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.StringLength.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.StringLength.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.StringLength.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.StringLength.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.StringLength.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.StringLength.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.StringLength.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.string` | `StringSocket` | String      |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.length` | `IntegerSocket` | Length      |

### StringToValue

``` python
StringToValue(string='', *, data_type='FLOAT')
```

Derive a numeric value from a given string representation

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| string | InputString | String      | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.converter.StringToValue.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.StringToValue.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.StringToValue.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.StringToValue.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.StringToValue.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.StringToValue.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.StringToValue.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.StringToValue.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.converter.StringToValue.float) | Create String to Value with operation ‘Float’. Floating-point value |
| [integer](#nodebpy.nodes.geometry.converter.StringToValue.integer) | Create String to Value with operation ‘Integer’. 32-bit integer |

##### float

``` python
float(string='')
```

Create String to Value with operation ‘Float’. Floating-point value

##### integer

``` python
integer(string='')
```

Create String to Value with operation ‘Integer’. 32-bit integer

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.string` | `StringSocket` | String      |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.value`  | `FloatSocket`   | Value       |
| `o.length` | `IntegerSocket` | Length      |

### TransformDirection

``` python
TransformDirection(direction=None, transform=None)
```

Apply a transformation matrix (excluding translation) to the given vector

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| direction | InputVector | Direction   | `None`  |
| transform | InputMatrix | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.TransformDirection.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.TransformDirection.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.TransformDirection.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.TransformDirection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.TransformDirection.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.TransformDirection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.TransformDirection.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.direction` | `VectorSocket` | Direction   |
| `i.transform` | `MatrixSocket` | Transform   |

**Outputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `o.direction` | `VectorSocket` | Direction   |

### TransformPoint

``` python
TransformPoint(vector=None, transform=None)
```

Apply a transformation matrix to the given vector

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| vector    | InputVector | Vector      | `None`  |
| transform | InputMatrix | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.TransformPoint.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.TransformPoint.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.TransformPoint.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.TransformPoint.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.TransformPoint.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.TransformPoint.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.TransformPoint.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.vector`    | `VectorSocket` | Vector      |
| `i.transform` | `MatrixSocket` | Transform   |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### TransposeMatrix

``` python
TransposeMatrix(matrix=None)
```

Flip a matrix over its diagonal, turning columns into rows and vice-versa

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| matrix | InputMatrix | Matrix      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.TransposeMatrix.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.TransposeMatrix.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.TransposeMatrix.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.TransposeMatrix.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.TransposeMatrix.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.TransposeMatrix.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.TransposeMatrix.type) |  |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.matrix` | `MatrixSocket` | Matrix      |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.matrix` | `MatrixSocket` | Matrix      |

### UVUnwrap

``` python
UVUnwrap(
    selection=True,
    seam=False,
    margin=0.001,
    fill_holes=True,
    method='Angle Based',
    iterations=10,
    no_flip=False,
)
```

Generate a UV map based on seam edges

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| selection | InputBoolean | Selection | `True` |
| seam | InputBoolean | Seam | `False` |
| margin | InputFloat | Margin | `0.001` |
| fill_holes | InputBoolean | Fill Holes | `True` |
| method | InputMenu \| Literal\['Angle Based', 'Conformal', 'Minimum Stretch'\] | Method | `'Angle Based'` |
| iterations | InputInteger | Iterations | `10` |
| no_flip | InputBoolean | No Flip | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.converter.UVUnwrap.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.UVUnwrap.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.UVUnwrap.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.UVUnwrap.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.UVUnwrap.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.UVUnwrap.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.UVUnwrap.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.selection`  | `BooleanSocket` | Selection   |
| `i.seam`       | `BooleanSocket` | Seam        |
| `i.margin`     | `FloatSocket`   | Margin      |
| `i.fill_holes` | `BooleanSocket` | Fill Holes  |
| `i.method`     | `MenuSocket`    | Method      |
| `i.iterations` | `IntegerSocket` | Iterations  |
| `i.no_flip`    | `BooleanSocket` | No Flip     |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### ValueToString

``` python
ValueToString(value=0.0, decimals=0, *, data_type='FLOAT')
```

Generate a string representation of the given input value

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| value    | InputFloat   | Value       | `0.0`   |
| decimals | InputInteger | Decimals    | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.converter.ValueToString.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.converter.ValueToString.i) |  |
| [`name`](#nodebpy.nodes.geometry.converter.ValueToString.name) |  |
| [`node`](#nodebpy.nodes.geometry.converter.ValueToString.node) |  |
| [`o`](#nodebpy.nodes.geometry.converter.ValueToString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.converter.ValueToString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.converter.ValueToString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.converter.ValueToString.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.converter.ValueToString.float) | Create Value to String with operation ‘Float’. Floating-point value |
| [integer](#nodebpy.nodes.geometry.converter.ValueToString.integer) | Create Value to String with operation ‘Integer’. 32-bit integer |

##### float

``` python
float(value=0.0, decimals=0)
```

Create Value to String with operation ‘Float’. Floating-point value

##### integer

``` python
integer(value=0)
```

Create Value to String with operation ‘Integer’. 32-bit integer

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.value`    | `FloatSocket`   | Value       |
| `i.decimals` | `IntegerSocket` | Decimals    |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.string` | `StringSocket` | String      |
