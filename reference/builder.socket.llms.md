# builder.socket

`socket`

## Classes

| Name | Description |
|----|----|
| [BaseSocket](#nodebpy.builder.socket.BaseSocket) |  |
| [BooleanSocket](#nodebpy.builder.socket.BooleanSocket) | Runtime boolean socket wrapper. |
| [BundleSocket](#nodebpy.builder.socket.BundleSocket) | Runtime bundle socket wrapper. |
| [ClosureSocket](#nodebpy.builder.socket.ClosureSocket) | Runtime closure socket wrapper. |
| [CollectionSocket](#nodebpy.builder.socket.CollectionSocket) | Runtime collection socket wrapper. |
| [ColorSocket](#nodebpy.builder.socket.ColorSocket) | Runtime color socket wrapper. |
| [FloatSocket](#nodebpy.builder.socket.FloatSocket) | Runtime float socket wrapper. |
| [FontSocket](#nodebpy.builder.socket.FontSocket) | Runtime font socket wrapper. |
| [GeometrySocket](#nodebpy.builder.socket.GeometrySocket) | Runtime geometry socket wrapper. |
| [ImageSocket](#nodebpy.builder.socket.ImageSocket) | Runtime image socket wrapper. |
| [IntegerSocket](#nodebpy.builder.socket.IntegerSocket) | Runtime integer socket wrapper. |
| [MaterialSocket](#nodebpy.builder.socket.MaterialSocket) | Runtime material socket wrapper. |
| [MatrixSocket](#nodebpy.builder.socket.MatrixSocket) | Runtime matrix socket wrapper. |
| [MenuSocket](#nodebpy.builder.socket.MenuSocket) | Runtime menu socket wrapper. |
| [ObjectSocket](#nodebpy.builder.socket.ObjectSocket) | Runtime object socket wrapper. |
| [RotationSocket](#nodebpy.builder.socket.RotationSocket) | Runtime rotation socket wrapper. |
| [ShaderSocket](#nodebpy.builder.socket.ShaderSocket) | Runtime shader socket wrapper. |
| [Socket](#nodebpy.builder.socket.Socket) | Wraps a single Blender NodeSocket, providing operator overloads and linking. |
| [StringSocket](#nodebpy.builder.socket.StringSocket) | Runtime string socket wrapper. |
| [VectorSocket](#nodebpy.builder.socket.VectorSocket) | Runtime vector socket wrapper. |

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
| [`default_value`](#nodebpy.builder.socket.BooleanSocket.default_value) |  |
| [`links`](#nodebpy.builder.socket.BooleanSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.BooleanSocket.socket) |  |
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
| [`links`](#nodebpy.builder.socket.BundleSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BundleSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BundleSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.ClosureSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ClosureSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ClosureSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.CollectionSocket.links) |  |
| [`name`](#nodebpy.builder.socket.CollectionSocket.name) |  |
| [`node`](#nodebpy.builder.socket.CollectionSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.CollectionSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.CollectionSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.CollectionSocket.type) |  |

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
| [`links`](#nodebpy.builder.socket.ColorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ColorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ColorSocket.node) |  |
| [`r`](#nodebpy.builder.socket.ColorSocket.r) |  |
| [`socket`](#nodebpy.builder.socket.ColorSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ColorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ColorSocket.type) |  |

### FloatSocket

``` python
FloatSocket(socket)
```

Runtime float socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FloatSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.FloatSocket.default_value) |  |
| [`links`](#nodebpy.builder.socket.FloatSocket.links) |  |
| [`name`](#nodebpy.builder.socket.FloatSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.FloatSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.FloatSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [negate](#nodebpy.builder.socket.FloatSocket.negate) | Negate the `FloatSocket` by multiplying the value by `-1`. |
| [sign](#nodebpy.builder.socket.FloatSocket.sign) | Return the sign of the FloatSocket, eithe `-1`, `0` or `1`. |
| [to_string](#nodebpy.builder.socket.FloatSocket.to_string) | Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places |

##### negate

``` python
negate()
```

Negate the `FloatSocket` by multiplying the value by `-1`.

##### sign

``` python
sign()
```

Return the sign of the FloatSocket, eithe `-1`, `0` or `1`.

##### to_string

``` python
to_string(decimals=0)
```

Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places

### FontSocket

``` python
FontSocket(socket)
```

Runtime font socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FontSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`links`](#nodebpy.builder.socket.FontSocket.links) |  |
| [`name`](#nodebpy.builder.socket.FontSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FontSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.GeometrySocket.links) |  |
| [`name`](#nodebpy.builder.socket.GeometrySocket.name) |  |
| [`node`](#nodebpy.builder.socket.GeometrySocket.node) |  |
| [`socket`](#nodebpy.builder.socket.GeometrySocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.GeometrySocket.tree) |  |
| [`type`](#nodebpy.builder.socket.GeometrySocket.type) |  |

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
| [`links`](#nodebpy.builder.socket.ImageSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ImageSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ImageSocket.node) |  |
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
| [`default_value`](#nodebpy.builder.socket.IntegerSocket.default_value) |  |
| [`links`](#nodebpy.builder.socket.IntegerSocket.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocket.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.IntegerSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.IntegerSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [negate](#nodebpy.builder.socket.IntegerSocket.negate) |  |
| [sign](#nodebpy.builder.socket.IntegerSocket.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |
| [to_string](#nodebpy.builder.socket.IntegerSocket.to_string) | Convert the `IntegerSocket` to a `StringSocket`. |

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
| [`links`](#nodebpy.builder.socket.MaterialSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MaterialSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MaterialSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.MatrixSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MatrixSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MatrixSocket.node) |  |
| [`rotation`](#nodebpy.builder.socket.MatrixSocket.rotation) |  |
| [`scale`](#nodebpy.builder.socket.MatrixSocket.scale) |  |
| [`socket`](#nodebpy.builder.socket.MatrixSocket.socket) |  |
| [`translation`](#nodebpy.builder.socket.MatrixSocket.translation) |  |
| [`tree`](#nodebpy.builder.socket.MatrixSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MatrixSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [determinant](#nodebpy.builder.socket.MatrixSocket.determinant) | Compute the determinant of a matrix input and return as a `FloatSocket` |
| [invert](#nodebpy.builder.socket.MatrixSocket.invert) | Invert the `MatrixSocet` and return a `MatrixSocket` |
| [svd](#nodebpy.builder.socket.MatrixSocket.svd) | Compute the ‘Single Value Decomposition’ and return output sockets of the MatrixSVD node, `tuple[u, s, v]` |
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

Compute the ‘Single Value Decomposition’ and return output sockets of the MatrixSVD node, `tuple[u, s, v]`

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
| [`links`](#nodebpy.builder.socket.MenuSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MenuSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MenuSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.ObjectSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ObjectSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ObjectSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.ObjectSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ObjectSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ObjectSocket.type) |  |

### RotationSocket

``` python
RotationSocket(socket)
```

Runtime rotation socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.RotationSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.RotationSocket.default_value) |  |
| [`links`](#nodebpy.builder.socket.RotationSocket.links) |  |
| [`name`](#nodebpy.builder.socket.RotationSocket.name) |  |
| [`node`](#nodebpy.builder.socket.RotationSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.RotationSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.RotationSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.RotationSocket.type) |  |
| [`w`](#nodebpy.builder.socket.RotationSocket.w) | Separate the rotation into a quaternion and return the `w` component |
| [`x`](#nodebpy.builder.socket.RotationSocket.x) | Separate the rotation into a quaternion and return the `x` component |
| [`y`](#nodebpy.builder.socket.RotationSocket.y) | Separate the rotation into a quaternion and return the `y` component |
| [`z`](#nodebpy.builder.socket.RotationSocket.z) | Separate the rotation into a quaternion and return the `z` component |

#### Methods

| Name | Description |
|----|----|
| [euler](#nodebpy.builder.socket.RotationSocket.euler) | Convert the rotation to an XYZ euler rotation and return `VectorSocket`. |
| [invert](#nodebpy.builder.socket.RotationSocket.invert) | Invert the rotation of the socket. |

##### euler

``` python
euler()
```

Convert the rotation to an XYZ euler rotation and return `VectorSocket`.

##### invert

``` python
invert()
```

Invert the rotation of the socket.

### ShaderSocket

``` python
ShaderSocket(socket)
```

Runtime shader socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ShaderSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`links`](#nodebpy.builder.socket.ShaderSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ShaderSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ShaderSocket.node) |  |
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
| [`links`](#nodebpy.builder.socket.Socket.links) |  |
| [`name`](#nodebpy.builder.socket.Socket.name) |  |
| [`node`](#nodebpy.builder.socket.Socket.node) |  |
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
| [`links`](#nodebpy.builder.socket.StringSocket.links) |  |
| [`name`](#nodebpy.builder.socket.StringSocket.name) |  |
| [`node`](#nodebpy.builder.socket.StringSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.StringSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.StringSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.StringSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [contains](#nodebpy.builder.socket.StringSocket.contains) | Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`. |
| [ends_with](#nodebpy.builder.socket.StringSocket.ends_with) | Create a MatchString\[Ends With\], return the result as a `BooleanSocket`. |
| [find](#nodebpy.builder.socket.StringSocket.find) | Find where in a string a pattern occurs. |
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

Find where in a string a pattern occurs.

Returns a tuple(IntegerSocket, IntegerSocket), corresponding to (index_of_first_match, count_of_matches).

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
| [`default_value`](#nodebpy.builder.socket.VectorSocket.default_value) |  |
| [`links`](#nodebpy.builder.socket.VectorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.VectorSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.VectorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocket.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocket.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocket.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocket.z) |  |

#### Methods

| Name | Description |
|----|----|
| [dot](#nodebpy.builder.socket.VectorSocket.dot) | Dot product with another vector. The other vector can be a Socket, a NodeSocket, or a 3-tuple of floats. |
| [length](#nodebpy.builder.socket.VectorSocket.length) |  |
| [normalize](#nodebpy.builder.socket.VectorSocket.normalize) | Normalize this vector. Only valid for output sockets, as it creates a Normalize node linked from this socket. |
| [scale](#nodebpy.builder.socket.VectorSocket.scale) | Scale this vector by a scalar value and return VectorSocket |

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

##### normalize

``` python
normalize()
```

Normalize this vector. Only valid for output sockets, as it creates a Normalize node linked from this socket.

The same normalize node is re-used each time unless `new_node=True` where a new `VectorMath` node is created each time.

##### scale

``` python
scale(scale)
```

Scale this vector by a scalar value and return VectorSocket
