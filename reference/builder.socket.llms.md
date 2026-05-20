# builder.socket

`socket`

## Classes

| Name | Description |
|----|----|
| [AxisAngle](#nodebpy.builder.socket.AxisAngle) | Axis-angle components returned by `RotationSocket.to_axis_angle()`. |
| [BaseSocket](#nodebpy.builder.socket.BaseSocket) |  |
| [BooleanSocket](#nodebpy.builder.socket.BooleanSocket) | Runtime boolean socket wrapper. |
| [BundleSocket](#nodebpy.builder.socket.BundleSocket) | Runtime bundle socket wrapper. |
| [ClosureSocket](#nodebpy.builder.socket.ClosureSocket) | Runtime closure socket wrapper. |
| [CollectionSocket](#nodebpy.builder.socket.CollectionSocket) | Runtime collection socket wrapper. |
| [ColorSocket](#nodebpy.builder.socket.ColorSocket) | Runtime color socket wrapper. |
| [FindResult](#nodebpy.builder.socket.FindResult) | Result of `StringSocket.find()`. |
| [FloatSocket](#nodebpy.builder.socket.FloatSocket) | Runtime float socket wrapper. |
| [FontSocket](#nodebpy.builder.socket.FontSocket) | Runtime font socket wrapper. |
| [GeometrySocket](#nodebpy.builder.socket.GeometrySocket) | Runtime geometry socket wrapper. |
| [ImageSocket](#nodebpy.builder.socket.ImageSocket) | Runtime image socket wrapper. |
| [IntegerSocket](#nodebpy.builder.socket.IntegerSocket) | Runtime integer socket wrapper. |
| [MaterialSocket](#nodebpy.builder.socket.MaterialSocket) | Runtime material socket wrapper. |
| [MatrixSocket](#nodebpy.builder.socket.MatrixSocket) | Runtime matrix socket wrapper. |
| [MenuSocket](#nodebpy.builder.socket.MenuSocket) | Runtime menu socket wrapper. |
| [ObjectSocket](#nodebpy.builder.socket.ObjectSocket) | Runtime object socket wrapper. |
| [QuaternionComponents](#nodebpy.builder.socket.QuaternionComponents) | Quaternion components returned by `RotationSocket.to_quaternion()`. |
| [RotationSocket](#nodebpy.builder.socket.RotationSocket) | Runtime rotation socket wrapper. |
| [SVDResult](#nodebpy.builder.socket.SVDResult) | SVD components returned by `MatrixSocket.svd()`. |
| [ShaderSocket](#nodebpy.builder.socket.ShaderSocket) | Runtime shader socket wrapper. |
| [Socket](#nodebpy.builder.socket.Socket) | Wraps a single Blender NodeSocket, providing operator overloads and linking. |
| [StringSocket](#nodebpy.builder.socket.StringSocket) | Runtime string socket wrapper. |
| [VectorSocket](#nodebpy.builder.socket.VectorSocket) | Runtime vector socket wrapper. |

### AxisAngle

``` python
AxisAngle()
```

Axis-angle components returned by `RotationSocket.to_axis_angle()`.

#### Attributes

| Name                                               | Description |
|----------------------------------------------------|-------------|
| [`angle`](#nodebpy.builder.socket.AxisAngle.angle) |             |
| [`axis`](#nodebpy.builder.socket.AxisAngle.axis)   |             |

### BaseSocket

``` python
BaseSocket(socket)
```

#### Attributes

| Name                                                  | Description |
|-------------------------------------------------------|-------------|
| [`links`](#nodebpy.builder.socket.BaseSocket.links)   |             |
| [`name`](#nodebpy.builder.socket.BaseSocket.name)     |             |
| [`node`](#nodebpy.builder.socket.BaseSocket.node)     |             |
| [`socket`](#nodebpy.builder.socket.BaseSocket.socket) |             |
| [`tree`](#nodebpy.builder.socket.BaseSocket.tree)     |             |
| [`type`](#nodebpy.builder.socket.BaseSocket.type)     |             |

### BooleanSocket

``` python
BooleanSocket(socket)
```

Runtime boolean socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.BooleanSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.BooleanSocket.corner) |  |
| [`default_value`](#nodebpy.builder.socket.BooleanSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.BooleanSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.BooleanSocket.face) |  |
| [`i`](#nodebpy.builder.socket.BooleanSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.BooleanSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.BooleanSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.BooleanSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocket.node) |  |
| [`o`](#nodebpy.builder.socket.BooleanSocket.o) |  |
| [`point`](#nodebpy.builder.socket.BooleanSocket.point) |  |
| [`socket`](#nodebpy.builder.socket.BooleanSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.BooleanSocket.spline) |  |
| [`switch`](#nodebpy.builder.socket.BooleanSocket.switch) | Creat a Switch node with this boolean as the `switch` input. |
| [`tree`](#nodebpy.builder.socket.BooleanSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.BooleanSocket.type) |  |

### BundleSocket

``` python
BundleSocket(socket)
```

Runtime bundle socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.BundleSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.BundleSocket.i) |  |
| [`links`](#nodebpy.builder.socket.BundleSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BundleSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BundleSocket.node) |  |
| [`o`](#nodebpy.builder.socket.BundleSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.BundleSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.BundleSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.BundleSocket.type) |  |

### ClosureSocket

``` python
ClosureSocket(socket)
```

Runtime closure socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ClosureSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ClosureSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ClosureSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ClosureSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ClosureSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ClosureSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.ClosureSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ClosureSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ClosureSocket.type) |  |

### CollectionSocket

``` python
CollectionSocket(socket)
```

Runtime collection socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.CollectionSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.CollectionSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.CollectionSocket.i) |  |
| [`links`](#nodebpy.builder.socket.CollectionSocket.links) |  |
| [`name`](#nodebpy.builder.socket.CollectionSocket.name) |  |
| [`node`](#nodebpy.builder.socket.CollectionSocket.node) |  |
| [`o`](#nodebpy.builder.socket.CollectionSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.CollectionSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.CollectionSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.CollectionSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [instances](#nodebpy.builder.socket.CollectionSocket.instances) | Import objects from the collection as instances. |

##### instances

``` python
instances(
    transform_space='ORIGINAL',
    separate_children=False,
    reset_children=False,
)
```

Import objects from the collection as instances.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The transform space to use for the instances. | `'ORIGINAL'` |
| separate_children | bool | Whether to separate objects as their own instances. | `False` |
| reset_children | bool | Whether to reset children of the collection to world origin. | `False` |

###### Returns

| Name | Type | Description |
|----|----|----|
|  | GeometrySocket | The output ‘Instances’ `GeometrySocket`. Will be a single instance or multiple instances if `separate_children` is `True`. |

### ColorSocket

``` python
ColorSocket(socket)
```

Runtime color socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`a`](#nodebpy.builder.socket.ColorSocket.a) |  |
| [`b`](#nodebpy.builder.socket.ColorSocket.b) |  |
| [`builder_node`](#nodebpy.builder.socket.ColorSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.ColorSocket.default_value) |  |
| [`g`](#nodebpy.builder.socket.ColorSocket.g) |  |
| [`i`](#nodebpy.builder.socket.ColorSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ColorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ColorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ColorSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ColorSocket.o) |  |
| [`r`](#nodebpy.builder.socket.ColorSocket.r) |  |
| [`socket`](#nodebpy.builder.socket.ColorSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ColorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ColorSocket.type) |  |

### FindResult

``` python
FindResult()
```

Result of `StringSocket.find()`.

#### Attributes

| Name | Description |
|----|----|
| [`count`](#nodebpy.builder.socket.FindResult.count) |  |
| [`first_found`](#nodebpy.builder.socket.FindResult.first_found) |  |

### FloatSocket

``` python
FloatSocket(socket)
```

Runtime float socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FloatSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.FloatSocket.corner) |  |
| [`default_value`](#nodebpy.builder.socket.FloatSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.FloatSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.FloatSocket.face) |  |
| [`i`](#nodebpy.builder.socket.FloatSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.FloatSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.FloatSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.FloatSocket.links) |  |
| [`mix`](#nodebpy.builder.socket.FloatSocket.mix) | Create a `Mix` node using this socket as the factor. |
| [`name`](#nodebpy.builder.socket.FloatSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocket.node) |  |
| [`o`](#nodebpy.builder.socket.FloatSocket.o) |  |
| [`point`](#nodebpy.builder.socket.FloatSocket.point) |  |
| [`socket`](#nodebpy.builder.socket.FloatSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.FloatSocket.spline) |  |
| [`tree`](#nodebpy.builder.socket.FloatSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [ceil](#nodebpy.builder.socket.FloatSocket.ceil) | Round up to the nearest integer. |
| [clamp](#nodebpy.builder.socket.FloatSocket.clamp) | Clamp the value to *\[min, max\]*. Defaults to the unit interval `[0, 1]`. |
| [floor](#nodebpy.builder.socket.FloatSocket.floor) | Round down to the nearest integer. |
| [map_range](#nodebpy.builder.socket.FloatSocket.map_range) | Remap the values on the float socket using the MapRange node. |
| [modulo](#nodebpy.builder.socket.FloatSocket.modulo) | Floored modulo — remainder after dividing by *divisor*, always non-negative. |
| [negate](#nodebpy.builder.socket.FloatSocket.negate) | Negate the `FloatSocket` by multiplying the value by `-1`. |
| [power](#nodebpy.builder.socket.FloatSocket.power) | Raise this value to *exponent*. |
| [round](#nodebpy.builder.socket.FloatSocket.round) | Round to the nearest integer. |
| [sign](#nodebpy.builder.socket.FloatSocket.sign) | Return the sign of the FloatSocket, eithe `-1`, `0` or `1`. |
| [sqrt](#nodebpy.builder.socket.FloatSocket.sqrt) | Return the square root of this value. |
| [to_degrees](#nodebpy.builder.socket.FloatSocket.to_degrees) | Convert radians to degrees. |
| [to_integer](#nodebpy.builder.socket.FloatSocket.to_integer) | Convert the `FloatSocket` to an `IntegerSocket` by truncating the decimal part. |
| [to_radians](#nodebpy.builder.socket.FloatSocket.to_radians) | Convert degrees to radians. |
| [to_string](#nodebpy.builder.socket.FloatSocket.to_string) | Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places |
| [wrap](#nodebpy.builder.socket.FloatSocket.wrap) | Wrap the value into the *\[min, max\]* range, repeating cyclically. |

##### ceil

``` python
ceil()
```

Round up to the nearest integer.

##### clamp

``` python
clamp(min=0.0, max=1.0)
```

Clamp the value to *\[min, max\]*. Defaults to the unit interval `[0, 1]`.

##### floor

``` python
floor()
```

Round down to the nearest integer.

##### map_range

``` python
map_range(
    from_min=0.0,
    from_max=1.0,
    to_min=0.0,
    to_max=1.0,
    *,
    clamp=True,
    interpolation_type='LINEAR',
    steps=4.0,
)
```

Remap the values on the float socket using the MapRange node.

##### modulo

``` python
modulo(divisor)
```

Floored modulo — remainder after dividing by *divisor*, always non-negative.

##### negate

``` python
negate()
```

Negate the `FloatSocket` by multiplying the value by `-1`.

##### power

``` python
power(exponent)
```

Raise this value to *exponent*.

##### round

``` python
round()
```

Round to the nearest integer.

##### sign

``` python
sign()
```

Return the sign of the FloatSocket, eithe `-1`, `0` or `1`.

##### sqrt

``` python
sqrt()
```

Return the square root of this value.

##### to_degrees

``` python
to_degrees()
```

Convert radians to degrees.

##### to_integer

``` python
to_integer(rounding_mode='ROUND')
```

Convert the `FloatSocket` to an `IntegerSocket` by truncating the decimal part.

##### to_radians

``` python
to_radians()
```

Convert degrees to radians.

##### to_string

``` python
to_string(decimals=0)
```

Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places

##### wrap

``` python
wrap(min, max)
```

Wrap the value into the *\[min, max\]* range, repeating cyclically.

### FontSocket

``` python
FontSocket(socket)
```

Runtime font socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FontSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.FontSocket.i) |  |
| [`links`](#nodebpy.builder.socket.FontSocket.links) |  |
| [`name`](#nodebpy.builder.socket.FontSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FontSocket.node) |  |
| [`o`](#nodebpy.builder.socket.FontSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.FontSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.FontSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.FontSocket.type) |  |

### GeometrySocket

``` python
GeometrySocket(socket)
```

Runtime geometry socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.GeometrySocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.GeometrySocket.i) |  |
| [`links`](#nodebpy.builder.socket.GeometrySocket.links) |  |
| [`name`](#nodebpy.builder.socket.GeometrySocket.name) |  |
| [`node`](#nodebpy.builder.socket.GeometrySocket.node) |  |
| [`o`](#nodebpy.builder.socket.GeometrySocket.o) |  |
| [`socket`](#nodebpy.builder.socket.GeometrySocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.GeometrySocket.tree) |  |
| [`type`](#nodebpy.builder.socket.GeometrySocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [realize_instances](#nodebpy.builder.socket.GeometrySocket.realize_instances) |  |

##### realize_instances

``` python
realize_instances(selection=True, realize_all=False, depth=0)
```

### ImageSocket

``` python
ImageSocket(socket)
```

Runtime image socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ImageSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.ImageSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.ImageSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ImageSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ImageSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ImageSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ImageSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.ImageSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ImageSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ImageSocket.type) |  |

### IntegerSocket

``` python
IntegerSocket(socket)
```

Runtime integer socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.IntegerSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.IntegerSocket.corner) |  |
| [`default_value`](#nodebpy.builder.socket.IntegerSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.IntegerSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.IntegerSocket.face) |  |
| [`i`](#nodebpy.builder.socket.IntegerSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.IntegerSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.IntegerSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.IntegerSocket.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocket.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocket.node) |  |
| [`o`](#nodebpy.builder.socket.IntegerSocket.o) |  |
| [`point`](#nodebpy.builder.socket.IntegerSocket.point) |  |
| [`socket`](#nodebpy.builder.socket.IntegerSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.IntegerSocket.spline) |  |
| [`tree`](#nodebpy.builder.socket.IntegerSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [clamp](#nodebpy.builder.socket.IntegerSocket.clamp) | Clamp the value to *\[min, max\]*. |
| [modulo](#nodebpy.builder.socket.IntegerSocket.modulo) | Remainder after dividing by *divisor* (always non-negative). |
| [negate](#nodebpy.builder.socket.IntegerSocket.negate) |  |
| [sign](#nodebpy.builder.socket.IntegerSocket.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |
| [to_string](#nodebpy.builder.socket.IntegerSocket.to_string) | Convert the `IntegerSocket` to a `StringSocket`. |

##### clamp

``` python
clamp(min=0, max=1)
```

Clamp the value to *\[min, max\]*.

##### modulo

``` python
modulo(divisor)
```

Remainder after dividing by *divisor* (always non-negative).

##### negate

``` python
negate()
```

##### sign

``` python
sign()
```

Return the sign of the IntegerSocket, either `-1`, `0`, or `1`.

##### to_string

``` python
to_string()
```

Convert the `IntegerSocket` to a `StringSocket`.

### MaterialSocket

``` python
MaterialSocket(socket)
```

Runtime material socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MaterialSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.MaterialSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.MaterialSocket.i) |  |
| [`links`](#nodebpy.builder.socket.MaterialSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MaterialSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MaterialSocket.node) |  |
| [`o`](#nodebpy.builder.socket.MaterialSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.MaterialSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.MaterialSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MaterialSocket.type) |  |

### MatrixSocket

``` python
MatrixSocket(socket)
```

Runtime matrix socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MatrixSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.MatrixSocket.corner) |  |
| [`edge`](#nodebpy.builder.socket.MatrixSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.MatrixSocket.face) |  |
| [`i`](#nodebpy.builder.socket.MatrixSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.MatrixSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.MatrixSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.MatrixSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MatrixSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MatrixSocket.node) |  |
| [`o`](#nodebpy.builder.socket.MatrixSocket.o) |  |
| [`point`](#nodebpy.builder.socket.MatrixSocket.point) |  |
| [`rotation`](#nodebpy.builder.socket.MatrixSocket.rotation) |  |
| [`scale`](#nodebpy.builder.socket.MatrixSocket.scale) |  |
| [`socket`](#nodebpy.builder.socket.MatrixSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.MatrixSocket.spline) |  |
| [`translation`](#nodebpy.builder.socket.MatrixSocket.translation) |  |
| [`tree`](#nodebpy.builder.socket.MatrixSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MatrixSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [determinant](#nodebpy.builder.socket.MatrixSocket.determinant) | Compute the determinant of a matrix input and return as a `FloatSocket` |
| [invert](#nodebpy.builder.socket.MatrixSocket.invert) | Invert the `MatrixSocet` and return a `MatrixSocket` |
| [svd](#nodebpy.builder.socket.MatrixSocket.svd) | Decompose the matrix via SVD. Returns `(u, s, v)`. |
| [transform_direction](#nodebpy.builder.socket.MatrixSocket.transform_direction) | Apply this matrix to *direction*, ignoring translation. |
| [transpose](#nodebpy.builder.socket.MatrixSocket.transpose) | Transpose the `MatrixSocket` and return a `MatrixSocket` |

##### determinant

``` python
determinant()
```

Compute the determinant of a matrix input and return as a `FloatSocket`

##### invert

``` python
invert()
```

Invert the `MatrixSocet` and return a `MatrixSocket`

##### svd

``` python
svd()
```

Decompose the matrix via SVD. Returns `(u, s, v)`.

##### transform_direction

``` python
transform_direction(direction)
```

Apply this matrix to *direction*, ignoring translation.

Use this instead of `transform()` when transforming a direction vector (e.g. a normal) where translation must not affect the result.

##### transpose

``` python
transpose()
```

Transpose the `MatrixSocket` and return a `MatrixSocket`

### MenuSocket

``` python
MenuSocket(socket)
```

Runtime menu socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MenuSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.MenuSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.MenuSocket.i) |  |
| [`links`](#nodebpy.builder.socket.MenuSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MenuSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MenuSocket.node) |  |
| [`o`](#nodebpy.builder.socket.MenuSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.MenuSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.MenuSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MenuSocket.type) |  |

### ObjectSocket

``` python
ObjectSocket(socket)
```

Runtime object socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ObjectSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.ObjectSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.ObjectSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ObjectSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ObjectSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ObjectSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ObjectSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.ObjectSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ObjectSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ObjectSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [geometry](#nodebpy.builder.socket.ObjectSocket.geometry) | The object’s geometry, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [location](#nodebpy.builder.socket.ObjectSocket.location) | The object’s location, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [rotation](#nodebpy.builder.socket.ObjectSocket.rotation) | The object’s rotation, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [scale](#nodebpy.builder.socket.ObjectSocket.scale) | The object’s scale, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [transform](#nodebpy.builder.socket.ObjectSocket.transform) | The Object’s transform matrix, optionally in relative space. |

##### geometry

``` python
geometry(transform_space='ORIGINAL', as_instance=False)
```

The object’s geometry, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The space in which to return the geometry. | `'ORIGINAL'` |
| as_instance | InputBoolean | Whether to return the geometry as an instance. | `False` |

###### Returns

| Name | Type           | Description                             |
|------|----------------|-----------------------------------------|
|      | GeometrySocket | The output ‘Geometry’ `GeometrySocket`. |

##### location

``` python
location(transform_space='ORIGINAL')
```

The object’s location, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The space in which to return the location. | `'ORIGINAL'` |

###### Returns

| Name | Type         | Description                           |
|------|--------------|---------------------------------------|
|      | VectorSocket | The output ‘Location’ `VectorSocket`. |

##### rotation

``` python
rotation(transform_space='ORIGINAL')
```

The object’s rotation, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The space in which to return the rotation. | `'ORIGINAL'` |

###### Returns

| Name | Type           | Description                             |
|------|----------------|-----------------------------------------|
|      | RotationSocket | The output ‘Rotation’ `RotationSocket`. |

##### scale

``` python
scale(transform_space='ORIGINAL')
```

The object’s scale, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo).

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The space in which to return the scale. | `'ORIGINAL'` |

###### Returns

| Name | Type         | Description                        |
|------|--------------|------------------------------------|
|      | VectorSocket | The output ‘Scale’ `VectorSocket`. |

##### transform

``` python
transform(transform_space='ORIGINAL')
```

The Object’s transform matrix, optionally in relative space.

Adds [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo) to the node tree and returns.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| transform_space | Literal\['ORIGINAL', 'RELATIVE'\] | The space in which to return the transform matrix. | `'ORIGINAL'` |

###### Returns

| Name | Type         | Description                            |
|------|--------------|----------------------------------------|
|      | MatrixSocket | The output ‘Transform’ `MatrixSocket`. |

### QuaternionComponents

``` python
QuaternionComponents()
```

Quaternion components returned by `RotationSocket.to_quaternion()`.

#### Attributes

| Name                                                  | Description |
|-------------------------------------------------------|-------------|
| [`w`](#nodebpy.builder.socket.QuaternionComponents.w) |             |
| [`x`](#nodebpy.builder.socket.QuaternionComponents.x) |             |
| [`y`](#nodebpy.builder.socket.QuaternionComponents.y) |             |
| [`z`](#nodebpy.builder.socket.QuaternionComponents.z) |             |

### RotationSocket

``` python
RotationSocket(socket)
```

Runtime rotation socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.RotationSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.RotationSocket.corner) |  |
| [`default_value`](#nodebpy.builder.socket.RotationSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.RotationSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.RotationSocket.face) |  |
| [`i`](#nodebpy.builder.socket.RotationSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.RotationSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.RotationSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.RotationSocket.links) |  |
| [`name`](#nodebpy.builder.socket.RotationSocket.name) |  |
| [`node`](#nodebpy.builder.socket.RotationSocket.node) |  |
| [`o`](#nodebpy.builder.socket.RotationSocket.o) |  |
| [`point`](#nodebpy.builder.socket.RotationSocket.point) |  |
| [`socket`](#nodebpy.builder.socket.RotationSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.RotationSocket.spline) |  |
| [`tree`](#nodebpy.builder.socket.RotationSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.RotationSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [invert](#nodebpy.builder.socket.RotationSocket.invert) | Invert the rotation of the socket. |
| [rotate](#nodebpy.builder.socket.RotationSocket.rotate) | Rotate this rotation by the given rotation in the specified rotation space. |
| [to_axis_angle](#nodebpy.builder.socket.RotationSocket.to_axis_angle) | Decompose the rotation into axis-angle components `(axis, angle)`. |
| [to_euler](#nodebpy.builder.socket.RotationSocket.to_euler) | Convert the rotation to an XYZ euler rotation and return `VectorSocket`. |
| [to_quaternion](#nodebpy.builder.socket.RotationSocket.to_quaternion) | Decompose the rotation into quaternion components `(w, x, y, z)`. |

##### invert

``` python
invert()
```

Invert the rotation of the socket.

##### rotate

``` python
rotate(rotation, rotation_space='GLOBAL')
```

Rotate this rotation by the given rotation in the specified rotation space.

##### to_axis_angle

``` python
to_axis_angle()
```

Decompose the rotation into axis-angle components `(axis, angle)`.

##### to_euler

``` python
to_euler()
```

Convert the rotation to an XYZ euler rotation and return `VectorSocket`.

##### to_quaternion

``` python
to_quaternion()
```

Decompose the rotation into quaternion components `(w, x, y, z)`.

### SVDResult

``` python
SVDResult()
```

SVD components returned by `MatrixSocket.svd()`.

#### Attributes

| Name                                       | Description |
|--------------------------------------------|-------------|
| [`s`](#nodebpy.builder.socket.SVDResult.s) |             |
| [`u`](#nodebpy.builder.socket.SVDResult.u) |             |
| [`v`](#nodebpy.builder.socket.SVDResult.v) |             |

### ShaderSocket

``` python
ShaderSocket(socket)
```

Runtime shader socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ShaderSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ShaderSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ShaderSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ShaderSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ShaderSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ShaderSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.ShaderSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ShaderSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ShaderSocket.type) |  |

### Socket

``` python
Socket(socket)
```

Wraps a single Blender NodeSocket, providing operator overloads and linking.

Returned by `SocketAccessor.get()` / `node.inputs[...]` / `node.outputs[...]`. Type-specific subclasses (`VectorSocket`, `ColorSocket`, `IntegerSocket`) are selected automatically via the registry.

#### Properties:

tree : TreeBuilder The tree this socket belongs to. socket : NodeSocket The underlying Blender NodeSocket.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.Socket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.Socket.i) |  |
| [`links`](#nodebpy.builder.socket.Socket.links) |  |
| [`name`](#nodebpy.builder.socket.Socket.name) |  |
| [`node`](#nodebpy.builder.socket.Socket.node) |  |
| [`o`](#nodebpy.builder.socket.Socket.o) |  |
| [`socket`](#nodebpy.builder.socket.Socket.socket) |  |
| [`tree`](#nodebpy.builder.socket.Socket.tree) |  |
| [`type`](#nodebpy.builder.socket.Socket.type) |  |

### StringSocket

``` python
StringSocket(socket)
```

Runtime string socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.StringSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.StringSocket.default_value) |  |
| [`i`](#nodebpy.builder.socket.StringSocket.i) |  |
| [`links`](#nodebpy.builder.socket.StringSocket.links) |  |
| [`name`](#nodebpy.builder.socket.StringSocket.name) |  |
| [`node`](#nodebpy.builder.socket.StringSocket.node) |  |
| [`o`](#nodebpy.builder.socket.StringSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.StringSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.StringSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.StringSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [contains](#nodebpy.builder.socket.StringSocket.contains) | Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`. |
| [ends_with](#nodebpy.builder.socket.StringSocket.ends_with) | Create a MatchString\[Ends With\], return the result as a `BooleanSocket`. |
| [find](#nodebpy.builder.socket.StringSocket.find) | Find where in a string a pattern occurs. Returns `(first_found, count)`. |
| [format](#nodebpy.builder.socket.StringSocket.format) | Format a given string with the key-value items. |
| [join](#nodebpy.builder.socket.StringSocket.join) | Join the input strings with this as the separator. |
| [length](#nodebpy.builder.socket.StringSocket.length) | Compute the length of a string and return as `IntegerSocket`. |
| [replace](#nodebpy.builder.socket.StringSocket.replace) | Replace every match of the string with teh replacement string |
| [slice](#nodebpy.builder.socket.StringSocket.slice) | Slice a given string from a starting position for a given length. |
| [starts_with](#nodebpy.builder.socket.StringSocket.starts_with) | Create a MatchString\[Starts With\], return the result as a `BooleanSocket`. |

##### contains

``` python
contains(search)
```

Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`.

##### ends_with

``` python
ends_with(search)
```

Create a MatchString\[Ends With\], return the result as a `BooleanSocket`.

##### find

``` python
find(search)
```

Find where in a string a pattern occurs. Returns `(first_found, count)`.

##### format

``` python
format(items)
```

Format a given string with the key-value items.

##### join

``` python
join(strings)
```

Join the input strings with this as the separator.

##### length

``` python
length()
```

Compute the length of a string and return as `IntegerSocket`.

##### replace

``` python
replace(find, replace)
```

Replace every match of the string with teh replacement string

##### slice

``` python
slice(position=0, length=0)
```

Slice a given string from a starting position for a given length.

##### starts_with

``` python
starts_with(search)
```

Create a MatchString\[Starts With\], return the result as a `BooleanSocket`.

### VectorSocket

``` python
VectorSocket(socket)
```

Runtime vector socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.VectorSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.VectorSocket.corner) |  |
| [`default_value`](#nodebpy.builder.socket.VectorSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.VectorSocket.edge) |  |
| [`face`](#nodebpy.builder.socket.VectorSocket.face) |  |
| [`i`](#nodebpy.builder.socket.VectorSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.VectorSocket.instance) |  |
| [`layer`](#nodebpy.builder.socket.VectorSocket.layer) |  |
| [`links`](#nodebpy.builder.socket.VectorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocket.node) |  |
| [`o`](#nodebpy.builder.socket.VectorSocket.o) |  |
| [`point`](#nodebpy.builder.socket.VectorSocket.point) |  |
| [`socket`](#nodebpy.builder.socket.VectorSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.VectorSocket.spline) |  |
| [`tree`](#nodebpy.builder.socket.VectorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocket.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocket.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocket.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocket.z) |  |

#### Methods

| Name | Description |
|----|----|
| [cross](#nodebpy.builder.socket.VectorSocket.cross) | Cross product of this vector with *other*. Returns a vector perpendicular to both. |
| [distance](#nodebpy.builder.socket.VectorSocket.distance) | Euclidean distance between this vector and *other*. |
| [dot](#nodebpy.builder.socket.VectorSocket.dot) | Dot product with another vector. The other vector can be a Socket, a NodeSocket, or a 3-tuple of floats. |
| [length](#nodebpy.builder.socket.VectorSocket.length) |  |
| [map_range](#nodebpy.builder.socket.VectorSocket.map_range) | Convenience method to remap a vector socket using the `MapRange.vector()` node with this socket as input |
| [normalize](#nodebpy.builder.socket.VectorSocket.normalize) | Normalize this vector. Only valid for output sockets, as it creates a Normalize node linked from this socket. |
| [project](#nodebpy.builder.socket.VectorSocket.project) | Project this vector onto *other*. |
| [reflect](#nodebpy.builder.socket.VectorSocket.reflect) | Reflect this vector around *normal*. *normal* does not need to be normalised. |
| [rotate](#nodebpy.builder.socket.VectorSocket.rotate) | Rotate this vector by the given rotation. |
| [scale](#nodebpy.builder.socket.VectorSocket.scale) | Scale this vector by a scalar value and return VectorSocket |
| [transform](#nodebpy.builder.socket.VectorSocket.transform) | Transform this vector by the given matrix. |

##### cross

``` python
cross(other)
```

Cross product of this vector with *other*. Returns a vector perpendicular to both.

##### distance

``` python
distance(other)
```

Euclidean distance between this vector and *other*.

##### dot

``` python
dot(vector)
```

Dot product with another vector. The other vector can be a Socket, a NodeSocket, or a 3-tuple of floats.

A different VectorMath node is created each time.

##### length

``` python
length()
```

##### map_range

``` python
map_range(
    from_min=(0.0, 0.0, 0.0),
    from_max=(1.0, 1.0, 1.0),
    to_min=(0.0, 0.0, 0.0),
    to_max=(1.0, 1.0, 1.0),
    *,
    clamp=True,
    interpolation_type='LINEAR',
    steps=(4.0, 4.0, 4.0),
)
```

Convenience method to remap a vector socket using the `MapRange.vector()` node with this socket as input

##### normalize

``` python
normalize()
```

Normalize this vector. Only valid for output sockets, as it creates a Normalize node linked from this socket.

The same normalize node is re-used each time unless `new_node=True` where a new `VectorMath` node is created each time.

##### project

``` python
project(other)
```

Project this vector onto *other*.

##### reflect

``` python
reflect(normal)
```

Reflect this vector around *normal*. *normal* does not need to be normalised.

##### rotate

``` python
rotate(rotation)
```

Rotate this vector by the given rotation.

##### scale

``` python
scale(scale)
```

Scale this vector by a scalar value and return VectorSocket

##### transform

``` python
transform(matrix)
```

Transform this vector by the given matrix.
