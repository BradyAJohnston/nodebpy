# builder.interface

`interface`

## Classes

| Name | Description |
|----|----|
| [InterfaceSocket](#nodebpy.builder.interface.InterfaceSocket) | Base class for all node group interface socket definitions. |
| [SocketBoolean](#nodebpy.builder.interface.SocketBoolean) | Boolean socket - true/false value. |
| [SocketBundle](#nodebpy.builder.interface.SocketBundle) | Bundle socket - holds multiple data types in one socket. |
| [SocketClosure](#nodebpy.builder.interface.SocketClosure) | Closure socket - holds shader closure data. |
| [SocketCollection](#nodebpy.builder.interface.SocketCollection) | Collection socket - Blender collection reference. |
| [SocketColor](#nodebpy.builder.interface.SocketColor) | Color socket — also provides .r, .g, .b, .a. |
| [SocketFloat](#nodebpy.builder.interface.SocketFloat) | Float socket |
| [SocketGeometry](#nodebpy.builder.interface.SocketGeometry) | Geometry socket - holds mesh, curve, point cloud, or volume data. |
| [SocketImage](#nodebpy.builder.interface.SocketImage) | Image socket - Blender image datablock reference. |
| [SocketInteger](#nodebpy.builder.interface.SocketInteger) | Integer socket |
| [SocketMaterial](#nodebpy.builder.interface.SocketMaterial) | Material socket - Blender material reference. |
| [SocketMatrix](#nodebpy.builder.interface.SocketMatrix) | Matrix socket - 4x4 transformation matrix. |
| [SocketMenu](#nodebpy.builder.interface.SocketMenu) | Menu socket - holds a selection from predefined items. |
| [SocketObject](#nodebpy.builder.interface.SocketObject) | Object socket - Blender object reference. |
| [SocketRotation](#nodebpy.builder.interface.SocketRotation) | Rotation socket - rotation value (Euler or Quaternion). |
| [SocketShader](#nodebpy.builder.interface.SocketShader) | Shader that is the final output for a material |
| [SocketString](#nodebpy.builder.interface.SocketString) |  |
| [SocketVector](#nodebpy.builder.interface.SocketVector) | Vector socket — also provides .x, .y, .z and vector math dispatch. |

### InterfaceSocket

``` python
InterfaceSocket(name, description='')
```

Base class for all node group interface socket definitions.

Extends `Socket` so that interface sockets behave like runtime sockets: they can be used directly in operator expressions, linked with `>>`, etc.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.InterfaceSocket.default_value) |  |
| [`description`](#nodebpy.builder.interface.InterfaceSocket.description) |  |
| [`inputs`](#nodebpy.builder.interface.InterfaceSocket.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.InterfaceSocket.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.InterfaceSocket.links) |  |
| [`name`](#nodebpy.builder.interface.InterfaceSocket.name) |  |
| [`node`](#nodebpy.builder.interface.InterfaceSocket.node) |  |
| [`outputs`](#nodebpy.builder.interface.InterfaceSocket.outputs) |  |
| [`socket`](#nodebpy.builder.interface.InterfaceSocket.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.InterfaceSocket.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.InterfaceSocket.tree) |  |
| [`type`](#nodebpy.builder.interface.InterfaceSocket.type) |  |

### SocketBoolean

``` python
SocketBoolean(
    name='Boolean',
    default_value=False,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    layer_selection_field=False,
    attribute_domain='POINT',
    default_attribute=None,
    is_panel_toggle=False,
)
```

Boolean socket - true/false value.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketBoolean.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketBoolean.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketBoolean.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketBoolean.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketBoolean.links) |  |
| [`name`](#nodebpy.builder.interface.SocketBoolean.name) |  |
| [`node`](#nodebpy.builder.interface.SocketBoolean.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketBoolean.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketBoolean.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketBoolean.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketBoolean.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketBoolean.type) |  |

### SocketBundle

``` python
SocketBundle(
    name='Bundle',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Bundle socket - holds multiple data types in one socket.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketBundle.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketBundle.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketBundle.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketBundle.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketBundle.links) |  |
| [`name`](#nodebpy.builder.interface.SocketBundle.name) |  |
| [`node`](#nodebpy.builder.interface.SocketBundle.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketBundle.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketBundle.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketBundle.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketBundle.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketBundle.type) |  |

### SocketClosure

``` python
SocketClosure(
    name='Closure',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Closure socket - holds shader closure data.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketClosure.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketClosure.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketClosure.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketClosure.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketClosure.links) |  |
| [`name`](#nodebpy.builder.interface.SocketClosure.name) |  |
| [`node`](#nodebpy.builder.interface.SocketClosure.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketClosure.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketClosure.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketClosure.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketClosure.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketClosure.type) |  |

### SocketCollection

``` python
SocketCollection(
    name='Collection',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Collection socket - Blender collection reference.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketCollection.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketCollection.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketCollection.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketCollection.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketCollection.links) |  |
| [`name`](#nodebpy.builder.interface.SocketCollection.name) |  |
| [`node`](#nodebpy.builder.interface.SocketCollection.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketCollection.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketCollection.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketCollection.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketCollection.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketCollection.type) |  |

### SocketColor

``` python
SocketColor(
    name='Color',
    default_value=(1.0, 1.0, 1.0, 1.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
)
```

Color socket — also provides .r, .g, .b, .a.

#### Attributes

| Name | Description |
|----|----|
| [`a`](#nodebpy.builder.interface.SocketColor.a) |  |
| [`b`](#nodebpy.builder.interface.SocketColor.b) |  |
| [`default_value`](#nodebpy.builder.interface.SocketColor.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketColor.description) |  |
| [`g`](#nodebpy.builder.interface.SocketColor.g) |  |
| [`inputs`](#nodebpy.builder.interface.SocketColor.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketColor.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketColor.links) |  |
| [`name`](#nodebpy.builder.interface.SocketColor.name) |  |
| [`node`](#nodebpy.builder.interface.SocketColor.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketColor.outputs) |  |
| [`r`](#nodebpy.builder.interface.SocketColor.r) |  |
| [`socket`](#nodebpy.builder.interface.SocketColor.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketColor.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketColor.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketColor.type) |  |

### SocketFloat

``` python
SocketFloat(
    name='Value',
    default_value=0.0,
    description='',
    *,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
)
```

Float socket

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketFloat.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketFloat.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketFloat.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketFloat.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketFloat.links) |  |
| [`name`](#nodebpy.builder.interface.SocketFloat.name) |  |
| [`node`](#nodebpy.builder.interface.SocketFloat.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketFloat.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketFloat.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketFloat.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketFloat.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketFloat.type) |  |

### SocketGeometry

``` python
SocketGeometry(
    name='Geometry',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Geometry socket - holds mesh, curve, point cloud, or volume data.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketGeometry.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketGeometry.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketGeometry.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketGeometry.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketGeometry.links) |  |
| [`name`](#nodebpy.builder.interface.SocketGeometry.name) |  |
| [`node`](#nodebpy.builder.interface.SocketGeometry.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketGeometry.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketGeometry.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketGeometry.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketGeometry.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketGeometry.type) |  |

### SocketImage

``` python
SocketImage(
    name='Image',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Image socket - Blender image datablock reference.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketImage.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketImage.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketImage.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketImage.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketImage.links) |  |
| [`name`](#nodebpy.builder.interface.SocketImage.name) |  |
| [`node`](#nodebpy.builder.interface.SocketImage.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketImage.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketImage.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketImage.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketImage.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketImage.type) |  |

### SocketInteger

``` python
SocketInteger(
    name='Integer',
    default_value=0,
    description='',
    *,
    min_value=-2147483648,
    max_value=2147483647,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
)
```

Integer socket

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketInteger.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketInteger.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketInteger.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketInteger.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketInteger.links) |  |
| [`name`](#nodebpy.builder.interface.SocketInteger.name) |  |
| [`node`](#nodebpy.builder.interface.SocketInteger.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketInteger.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketInteger.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketInteger.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketInteger.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketInteger.type) |  |

### SocketMaterial

``` python
SocketMaterial(
    name='Material',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Material socket - Blender material reference.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketMaterial.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketMaterial.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketMaterial.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketMaterial.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketMaterial.links) |  |
| [`name`](#nodebpy.builder.interface.SocketMaterial.name) |  |
| [`node`](#nodebpy.builder.interface.SocketMaterial.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketMaterial.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketMaterial.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketMaterial.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketMaterial.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketMaterial.type) |  |

### SocketMatrix

``` python
SocketMatrix(
    name='Matrix',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    attribute_domain='POINT',
    default_attribute=None,
)
```

Matrix socket - 4x4 transformation matrix.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketMatrix.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketMatrix.description) |  |
| [`determinant`](#nodebpy.builder.interface.SocketMatrix.determinant) |  |
| [`inputs`](#nodebpy.builder.interface.SocketMatrix.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketMatrix.interface_socket) |  |
| [`invert`](#nodebpy.builder.interface.SocketMatrix.invert) |  |
| [`links`](#nodebpy.builder.interface.SocketMatrix.links) |  |
| [`name`](#nodebpy.builder.interface.SocketMatrix.name) |  |
| [`node`](#nodebpy.builder.interface.SocketMatrix.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketMatrix.outputs) |  |
| [`rotation`](#nodebpy.builder.interface.SocketMatrix.rotation) |  |
| [`scale`](#nodebpy.builder.interface.SocketMatrix.scale) |  |
| [`socket`](#nodebpy.builder.interface.SocketMatrix.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketMatrix.socket_name) |  |
| [`translation`](#nodebpy.builder.interface.SocketMatrix.translation) |  |
| [`transpose`](#nodebpy.builder.interface.SocketMatrix.transpose) |  |
| [`tree`](#nodebpy.builder.interface.SocketMatrix.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketMatrix.type) |  |

### SocketMenu

``` python
SocketMenu(
    name='Menu',
    default_value=None,
    description='',
    *,
    expanded=False,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
)
```

Menu socket - holds a selection from predefined items.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketMenu.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketMenu.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketMenu.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketMenu.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketMenu.links) |  |
| [`name`](#nodebpy.builder.interface.SocketMenu.name) |  |
| [`node`](#nodebpy.builder.interface.SocketMenu.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketMenu.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketMenu.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketMenu.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketMenu.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketMenu.type) |  |

### SocketObject

``` python
SocketObject(
    name='Object',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Object socket - Blender object reference.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketObject.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketObject.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketObject.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketObject.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketObject.links) |  |
| [`name`](#nodebpy.builder.interface.SocketObject.name) |  |
| [`node`](#nodebpy.builder.interface.SocketObject.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketObject.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketObject.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketObject.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketObject.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketObject.type) |  |

### SocketRotation

``` python
SocketRotation(
    name='Rotation',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
)
```

Rotation socket - rotation value (Euler or Quaternion).

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketRotation.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketRotation.description) |  |
| [`euler`](#nodebpy.builder.interface.SocketRotation.euler) |  |
| [`inputs`](#nodebpy.builder.interface.SocketRotation.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketRotation.interface_socket) |  |
| [`invert`](#nodebpy.builder.interface.SocketRotation.invert) |  |
| [`links`](#nodebpy.builder.interface.SocketRotation.links) |  |
| [`name`](#nodebpy.builder.interface.SocketRotation.name) |  |
| [`node`](#nodebpy.builder.interface.SocketRotation.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketRotation.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketRotation.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketRotation.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketRotation.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketRotation.type) |  |
| [`w`](#nodebpy.builder.interface.SocketRotation.w) |  |
| [`x`](#nodebpy.builder.interface.SocketRotation.x) |  |
| [`y`](#nodebpy.builder.interface.SocketRotation.y) |  |
| [`z`](#nodebpy.builder.interface.SocketRotation.z) |  |

### SocketShader

``` python
SocketShader(
    name='Shader',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

Shader that is the final output for a material

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketShader.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketShader.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketShader.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketShader.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketShader.links) |  |
| [`name`](#nodebpy.builder.interface.SocketShader.name) |  |
| [`node`](#nodebpy.builder.interface.SocketShader.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketShader.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketShader.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketShader.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketShader.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketShader.type) |  |

### SocketString

``` python
SocketString(
    name='String',
    default_value='',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    subtype='NONE',
)
```

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketString.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketString.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketString.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketString.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketString.links) |  |
| [`name`](#nodebpy.builder.interface.SocketString.name) |  |
| [`node`](#nodebpy.builder.interface.SocketString.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketString.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketString.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketString.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketString.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketString.type) |  |

### SocketVector

``` python
SocketVector(
    name='Vector',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    dimensions=3,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    default_attribute=None,
    default_input='VALUE',
    attribute_domain='POINT',
)
```

Vector socket — also provides .x, .y, .z and vector math dispatch.

#### Attributes

| Name | Description |
|----|----|
| [`default_value`](#nodebpy.builder.interface.SocketVector.default_value) |  |
| [`description`](#nodebpy.builder.interface.SocketVector.description) |  |
| [`inputs`](#nodebpy.builder.interface.SocketVector.inputs) |  |
| [`interface_socket`](#nodebpy.builder.interface.SocketVector.interface_socket) |  |
| [`links`](#nodebpy.builder.interface.SocketVector.links) |  |
| [`name`](#nodebpy.builder.interface.SocketVector.name) |  |
| [`node`](#nodebpy.builder.interface.SocketVector.node) |  |
| [`outputs`](#nodebpy.builder.interface.SocketVector.outputs) |  |
| [`socket`](#nodebpy.builder.interface.SocketVector.socket) |  |
| [`socket_name`](#nodebpy.builder.interface.SocketVector.socket_name) |  |
| [`tree`](#nodebpy.builder.interface.SocketVector.tree) |  |
| [`type`](#nodebpy.builder.interface.SocketVector.type) |  |
| [`x`](#nodebpy.builder.interface.SocketVector.x) |  |
| [`y`](#nodebpy.builder.interface.SocketVector.y) |  |
| [`z`](#nodebpy.builder.interface.SocketVector.z) |  |
