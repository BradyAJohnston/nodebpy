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

| Name | Description |
|----|----|
| [`interface_socket`](#nodebpy.builder.socket.BaseSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.BaseSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BaseSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BaseSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.BaseSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.BaseSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.BaseSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.BaseSocket.type) |  |

### BooleanSocket

``` python
BooleanSocket(socket)
```

Runtime boolean socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.socket.BooleanSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.BooleanSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.BooleanSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.BooleanSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.BooleanSocket.socket_name) |  |
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
| [`interface_socket`](#nodebpy.builder.socket.BundleSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.BundleSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BundleSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BundleSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.BundleSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.BundleSocket.socket_name) |  |
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
| [`interface_socket`](#nodebpy.builder.socket.ClosureSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.ClosureSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ClosureSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ClosureSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.ClosureSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.ClosureSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.CollectionSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.CollectionSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.CollectionSocket.links) |  |
| [`name`](#nodebpy.builder.socket.CollectionSocket.name) |  |
| [`node`](#nodebpy.builder.socket.CollectionSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.CollectionSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.CollectionSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.ColorSocket.default_value) |  |
| [`g`](#nodebpy.builder.socket.ColorSocket.g) |  |
| [`interface_socket`](#nodebpy.builder.socket.ColorSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.ColorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ColorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ColorSocket.node) |  |
| [`r`](#nodebpy.builder.socket.ColorSocket.r) |  |
| [`socket`](#nodebpy.builder.socket.ColorSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.ColorSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.FloatSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.FloatSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.FloatSocket.links) |  |
| [`name`](#nodebpy.builder.socket.FloatSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.FloatSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.FloatSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.FloatSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocket.type) |  |

### FontSocket

``` python
FontSocket(socket)
```

Runtime font socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`interface_socket`](#nodebpy.builder.socket.FontSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.FontSocket.links) |  |
| [`name`](#nodebpy.builder.socket.FontSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FontSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.FontSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.FontSocket.socket_name) |  |
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
| [`interface_socket`](#nodebpy.builder.socket.GeometrySocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.GeometrySocket.links) |  |
| [`name`](#nodebpy.builder.socket.GeometrySocket.name) |  |
| [`node`](#nodebpy.builder.socket.GeometrySocket.node) |  |
| [`socket`](#nodebpy.builder.socket.GeometrySocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.GeometrySocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.ImageSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.ImageSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.ImageSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ImageSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ImageSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.ImageSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.ImageSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.IntegerSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.IntegerSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.IntegerSocket.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocket.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.IntegerSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.IntegerSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.IntegerSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocket.type) |  |

### MaterialSocket

``` python
MaterialSocket(socket)
```

Runtime material socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.socket.MaterialSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.MaterialSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.MaterialSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MaterialSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MaterialSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.MaterialSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.MaterialSocket.socket_name) |  |
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
| [`determinant`](#nodebpy.builder.socket.MatrixSocket.determinant) |  |
| [`interface_socket`](#nodebpy.builder.socket.MatrixSocket.interface_socket) |  |
| [`invert`](#nodebpy.builder.socket.MatrixSocket.invert) |  |
| [`links`](#nodebpy.builder.socket.MatrixSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MatrixSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MatrixSocket.node) |  |
| [`rotation`](#nodebpy.builder.socket.MatrixSocket.rotation) |  |
| [`scale`](#nodebpy.builder.socket.MatrixSocket.scale) |  |
| [`socket`](#nodebpy.builder.socket.MatrixSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.MatrixSocket.socket_name) |  |
| [`translation`](#nodebpy.builder.socket.MatrixSocket.translation) |  |
| [`transpose`](#nodebpy.builder.socket.MatrixSocket.transpose) |  |
| [`tree`](#nodebpy.builder.socket.MatrixSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MatrixSocket.type) |  |

### MenuSocket

``` python
MenuSocket(socket)
```

Runtime menu socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.socket.MenuSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.MenuSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.MenuSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MenuSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MenuSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.MenuSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.MenuSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.ObjectSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.ObjectSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.ObjectSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ObjectSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ObjectSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.ObjectSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.ObjectSocket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.RotationSocket.default_value) |  |
| [`euler`](#nodebpy.builder.socket.RotationSocket.euler) |  |
| [`interface_socket`](#nodebpy.builder.socket.RotationSocket.interface_socket) |  |
| [`invert`](#nodebpy.builder.socket.RotationSocket.invert) |  |
| [`links`](#nodebpy.builder.socket.RotationSocket.links) |  |
| [`name`](#nodebpy.builder.socket.RotationSocket.name) |  |
| [`node`](#nodebpy.builder.socket.RotationSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.RotationSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.RotationSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.RotationSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.RotationSocket.type) |  |
| [`w`](#nodebpy.builder.socket.RotationSocket.w) |  |
| [`x`](#nodebpy.builder.socket.RotationSocket.x) |  |
| [`y`](#nodebpy.builder.socket.RotationSocket.y) |  |
| [`z`](#nodebpy.builder.socket.RotationSocket.z) |  |

### ShaderSocket

``` python
ShaderSocket(socket)
```

Runtime shader socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`interface_socket`](#nodebpy.builder.socket.ShaderSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.ShaderSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ShaderSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ShaderSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.ShaderSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.ShaderSocket.socket_name) |  |
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
| [`interface_socket`](#nodebpy.builder.socket.Socket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.Socket.links) |  |
| [`name`](#nodebpy.builder.socket.Socket.name) |  |
| [`node`](#nodebpy.builder.socket.Socket.node) |  |
| [`socket`](#nodebpy.builder.socket.Socket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.Socket.socket_name) |  |
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
| [`default_value`](#nodebpy.builder.socket.StringSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.StringSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.StringSocket.links) |  |
| [`name`](#nodebpy.builder.socket.StringSocket.name) |  |
| [`node`](#nodebpy.builder.socket.StringSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.StringSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.StringSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.StringSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.StringSocket.type) |  |

### VectorSocket

``` python
VectorSocket(socket)
```

Runtime vector socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.socket.VectorSocket.default_value) |  |
| [`interface_socket`](#nodebpy.builder.socket.VectorSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.socket.VectorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocket.node) |  |
| [`socket`](#nodebpy.builder.socket.VectorSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.socket.VectorSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.socket.VectorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocket.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocket.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocket.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocket.z) |  |
