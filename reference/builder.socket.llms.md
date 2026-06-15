# builder.socket

`socket`

Typed Python wrappers around Blender node sockets.

These classes give each socket type (float, vector, color, …) a fluent, type-aware API and the operator overloads used when wiring node trees.

Organization (top to bottom): \* Type variables and result types \* Base wrappers: `BaseSocket` and `Socket` \* Grid sockets and domain-bound field evaluation \* Per-type behaviour mixins (`_VectorMixin`, `_FloatMixin`, …) \* Structural mixins (lists, default values, type conversions) \* Concrete socket classes — the registry targets returned by `_wrap_socket` \* Registry registration (bl_idname -\> socket class)

## Classes

| Name | Description |
|----|----|
| [BaseSocket](#nodebpy.builder.socket.BaseSocket) |  |
| [BooleanSocket](#nodebpy.builder.socket.BooleanSocket) | Runtime boolean socket wrapper. |
| [BooleanSocketGrid](#nodebpy.builder.socket.BooleanSocketGrid) | Runtime boolean grid socket wrapper. |
| [BooleanSocketList](#nodebpy.builder.socket.BooleanSocketList) | List of boolean sockets. |
| [BundleSocket](#nodebpy.builder.socket.BundleSocket) | Runtime bundle socket wrapper. |
| [BundleSocketList](#nodebpy.builder.socket.BundleSocketList) | List of bundle sockets. |
| [ClosureSocket](#nodebpy.builder.socket.ClosureSocket) | Runtime closure socket wrapper. |
| [ClosureSocketList](#nodebpy.builder.socket.ClosureSocketList) | List of closure sockets. |
| [CollectionSocket](#nodebpy.builder.socket.CollectionSocket) | Runtime collection socket wrapper. |
| [CollectionSocketList](#nodebpy.builder.socket.CollectionSocketList) | List of collection sockets. |
| [ColorSocket](#nodebpy.builder.socket.ColorSocket) | Runtime color socket wrapper. |
| [ColorSocketList](#nodebpy.builder.socket.ColorSocketList) | List of color sockets. |
| [FloatSocket](#nodebpy.builder.socket.FloatSocket) | Runtime float socket wrapper. |
| [FloatSocketGrid](#nodebpy.builder.socket.FloatSocketGrid) | Runtime float grid socket wrapper. |
| [FloatSocketList](#nodebpy.builder.socket.FloatSocketList) |  |
| [FontSocket](#nodebpy.builder.socket.FontSocket) | Runtime font socket wrapper. |
| [FontSocketList](#nodebpy.builder.socket.FontSocketList) | List of font sockets. |
| [GeometrySocket](#nodebpy.builder.socket.GeometrySocket) | Runtime geometry socket wrapper. |
| [GeometrySocketList](#nodebpy.builder.socket.GeometrySocketList) | List of geometry sockets. |
| [ImageSocket](#nodebpy.builder.socket.ImageSocket) | Runtime image socket wrapper. |
| [ImageSocketList](#nodebpy.builder.socket.ImageSocketList) | List of image sockets. |
| [IntegerSocket](#nodebpy.builder.socket.IntegerSocket) | Runtime integer socket wrapper. |
| [IntegerSocketGrid](#nodebpy.builder.socket.IntegerSocketGrid) | Runtime integer grid socket wrapper. |
| [IntegerSocketList](#nodebpy.builder.socket.IntegerSocketList) | List of integer sockets. |
| [IntegerVectorSocket](#nodebpy.builder.socket.IntegerVectorSocket) | Runtime integer vector socket wrapper. |
| [MaterialSocket](#nodebpy.builder.socket.MaterialSocket) | Runtime material socket wrapper. |
| [MaterialSocketList](#nodebpy.builder.socket.MaterialSocketList) | List of material sockets. |
| [MatrixSocket](#nodebpy.builder.socket.MatrixSocket) | Runtime matrix socket wrapper. |
| [MatrixSocketList](#nodebpy.builder.socket.MatrixSocketList) | List of matrix sockets. |
| [MenuSocket](#nodebpy.builder.socket.MenuSocket) | Runtime menu socket wrapper. |
| [MenuSocketList](#nodebpy.builder.socket.MenuSocketList) | List of menu sockets. |
| [ObjectSocket](#nodebpy.builder.socket.ObjectSocket) | Runtime object socket wrapper. |
| [ObjectSocketList](#nodebpy.builder.socket.ObjectSocketList) | List of object sockets. |
| [ResultAxisAngle](#nodebpy.builder.socket.ResultAxisAngle) | Axis-angle components returned by `RotationSocket.to_axis_angle()`. |
| [ResultMatrixSVD](#nodebpy.builder.socket.ResultMatrixSVD) | SVD components returned by `MatrixSocket.svd()`. |
| [ResultQuaternionComponents](#nodebpy.builder.socket.ResultQuaternionComponents) | Quaternion components returned by `RotationSocket.to_quaternion()`. |
| [ResultStringFind](#nodebpy.builder.socket.ResultStringFind) | Result of `StringSocket.find()`. |
| [RotationSocket](#nodebpy.builder.socket.RotationSocket) | Runtime rotation socket wrapper. |
| [RotationSocketList](#nodebpy.builder.socket.RotationSocketList) | List of rotation sockets. |
| [ShaderSocket](#nodebpy.builder.socket.ShaderSocket) | Runtime shader socket wrapper. |
| [ShaderSocketList](#nodebpy.builder.socket.ShaderSocketList) | List of shader sockets. |
| [Socket](#nodebpy.builder.socket.Socket) | Wraps a single Blender NodeSocket, providing operator overloads and linking. |
| [SoundSocket](#nodebpy.builder.socket.SoundSocket) | Runtime sound socket wrapper. |
| [SoundSocketList](#nodebpy.builder.socket.SoundSocketList) | List of sound sockets. |
| [StringSocket](#nodebpy.builder.socket.StringSocket) | Runtime string socket wrapper. |
| [StringSocketList](#nodebpy.builder.socket.StringSocketList) | List of string sockets. |
| [VectorSocket](#nodebpy.builder.socket.VectorSocket) | Runtime vector socket wrapper. |
| [VectorSocketGrid](#nodebpy.builder.socket.VectorSocketGrid) | Runtime vector grid socket wrapper. |
| [VectorSocketList](#nodebpy.builder.socket.VectorSocketList) |  |

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
| [`corner`](#nodebpy.builder.socket.BooleanSocket.corner) | BooleanSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`default_value`](#nodebpy.builder.socket.BooleanSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`edge`](#nodebpy.builder.socket.BooleanSocket.edge) | BooleanSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`face`](#nodebpy.builder.socket.BooleanSocket.face) | BooleanSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`i`](#nodebpy.builder.socket.BooleanSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.BooleanSocket.instance) | BooleanSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`layer`](#nodebpy.builder.socket.BooleanSocket.layer) | BooleanSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`links`](#nodebpy.builder.socket.BooleanSocket.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocket.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocket.node) |  |
| [`o`](#nodebpy.builder.socket.BooleanSocket.o) |  |
| [`point`](#nodebpy.builder.socket.BooleanSocket.point) | BooleanSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`socket`](#nodebpy.builder.socket.BooleanSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.BooleanSocket.spline) | BooleanSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`switch`](#nodebpy.builder.socket.BooleanSocket.switch) | Creat a Switch node with this boolean as the `switch` input. |
| [`tree`](#nodebpy.builder.socket.BooleanSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.BooleanSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.BooleanSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [to_list](#nodebpy.builder.socket.BooleanSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

### BooleanSocketGrid

``` python
BooleanSocketGrid(socket)
```

Runtime boolean grid socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`background_value`](#nodebpy.builder.socket.BooleanSocketGrid.background_value) |  |
| [`builder_node`](#nodebpy.builder.socket.BooleanSocketGrid.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.BooleanSocketGrid.i) |  |
| [`links`](#nodebpy.builder.socket.BooleanSocketGrid.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocketGrid.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocketGrid.node) |  |
| [`o`](#nodebpy.builder.socket.BooleanSocketGrid.o) |  |
| [`socket`](#nodebpy.builder.socket.BooleanSocketGrid.socket) |  |
| [`switch`](#nodebpy.builder.socket.BooleanSocketGrid.switch) | Creat a Switch node with this boolean as the `switch` input. |
| [`transform`](#nodebpy.builder.socket.BooleanSocketGrid.transform) |  |
| [`tree`](#nodebpy.builder.socket.BooleanSocketGrid.tree) |  |
| [`type`](#nodebpy.builder.socket.BooleanSocketGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [clip](#nodebpy.builder.socket.BooleanSocketGrid.clip) | Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value. |
| [dilate_erode](#nodebpy.builder.socket.BooleanSocketGrid.dilate_erode) | Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values. |
| [enable_output](#nodebpy.builder.socket.BooleanSocketGrid.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [field_to_grid](#nodebpy.builder.socket.BooleanSocketGrid.field_to_grid) | Create new grids by evaluating new values on an existing volume grid topology. |
| [prune](#nodebpy.builder.socket.BooleanSocketGrid.prune) | Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes. |
| [sample](#nodebpy.builder.socket.BooleanSocketGrid.sample) | Retrieve values from the specified volume grid. |
| [sample_index](#nodebpy.builder.socket.BooleanSocketGrid.sample_index) | Retrieve volume grid values at specific voxels. |
| [to_points](#nodebpy.builder.socket.BooleanSocketGrid.to_points) | Generate a point cloud from a volume grid’s active voxels. |
| [voxelize](#nodebpy.builder.socket.BooleanSocketGrid.voxelize) | Remove sparseness from a volume grid by making the active tiles into voxels. |

##### clip

``` python
clip(min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value.

##### dilate_erode

``` python
dilate_erode(steps=1, connectivity='Face', tiles='Preserve')
```

Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### field_to_grid

``` python
field_to_grid()
```

Create new grids by evaluating new values on an existing volume grid topology.

##### prune

``` python
prune(threshold=0.1, mode=None)
```

Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes.

##### sample

``` python
sample(position=None, interpolation='Trilinear')
```

Retrieve values from the specified volume grid.

##### sample_index

``` python
sample_index(x=0, y=0, z=0)
```

Retrieve volume grid values at specific voxels.

##### to_points

``` python
to_points()
```

Generate a point cloud from a volume grid’s active voxels.

##### voxelize

``` python
voxelize()
```

Remove sparseness from a volume grid by making the active tiles into voxels.

### BooleanSocketList

``` python
BooleanSocketList(socket)
```

List of boolean sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.BooleanSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.BooleanSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.BooleanSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.BooleanSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.BooleanSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.BooleanSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.BooleanSocketList.socket) |  |
| [`switch`](#nodebpy.builder.socket.BooleanSocketList.switch) | Creat a Switch node with this boolean as the `switch` input. |
| [`tree`](#nodebpy.builder.socket.BooleanSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.BooleanSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.BooleanSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.BooleanSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.BooleanSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.BooleanSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.BooleanSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.BooleanSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.BooleanSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.BundleSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### BundleSocketList

``` python
BundleSocketList(socket)
```

List of bundle sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.BundleSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.BundleSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.BundleSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.BundleSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.BundleSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.BundleSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.BundleSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.BundleSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.BundleSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.BundleSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.BundleSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.BundleSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.BundleSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.BundleSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.BundleSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.BundleSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ClosureSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### ClosureSocketList

``` python
ClosureSocketList(socket)
```

List of closure sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ClosureSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ClosureSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.ClosureSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.ClosureSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.ClosureSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.ClosureSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.ClosureSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.ClosureSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.ClosureSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ClosureSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.ClosureSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.ClosureSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.ClosureSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.ClosureSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.ClosureSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.ClosureSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### CollectionSocket

``` python
CollectionSocket(socket)
```

Runtime collection socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.CollectionSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.CollectionSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
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
| [enable_output](#nodebpy.builder.socket.CollectionSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [instances](#nodebpy.builder.socket.CollectionSocket.instances) | Import objects from the collection as instances. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

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

### CollectionSocketList

``` python
CollectionSocketList(socket)
```

List of collection sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.CollectionSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.CollectionSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.CollectionSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.CollectionSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.CollectionSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.CollectionSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.CollectionSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.CollectionSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.CollectionSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.CollectionSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.CollectionSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.CollectionSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.CollectionSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.CollectionSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.CollectionSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.CollectionSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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
| [`corner`](#nodebpy.builder.socket.ColorSocket.corner) | ColorSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`default_value`](#nodebpy.builder.socket.ColorSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.ColorSocket.edge) | ColorSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`face`](#nodebpy.builder.socket.ColorSocket.face) | ColorSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`g`](#nodebpy.builder.socket.ColorSocket.g) |  |
| [`i`](#nodebpy.builder.socket.ColorSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.ColorSocket.instance) | ColorSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`layer`](#nodebpy.builder.socket.ColorSocket.layer) | ColorSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`links`](#nodebpy.builder.socket.ColorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ColorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ColorSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ColorSocket.o) |  |
| [`point`](#nodebpy.builder.socket.ColorSocket.point) | BooleanSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`r`](#nodebpy.builder.socket.ColorSocket.r) |  |
| [`socket`](#nodebpy.builder.socket.ColorSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.ColorSocket.spline) | ColorSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`tree`](#nodebpy.builder.socket.ColorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ColorSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ColorSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [to_list](#nodebpy.builder.socket.ColorSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

### ColorSocketList

``` python
ColorSocketList(socket)
```

List of color sockets.

#### Attributes

| Name | Description |
|----|----|
| [`a`](#nodebpy.builder.socket.ColorSocketList.a) |  |
| [`b`](#nodebpy.builder.socket.ColorSocketList.b) |  |
| [`builder_node`](#nodebpy.builder.socket.ColorSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.ColorSocketList.corner) | ColorSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`default_value`](#nodebpy.builder.socket.ColorSocketList.default_value) |  |
| [`edge`](#nodebpy.builder.socket.ColorSocketList.edge) | ColorSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`face`](#nodebpy.builder.socket.ColorSocketList.face) | ColorSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`g`](#nodebpy.builder.socket.ColorSocketList.g) |  |
| [`i`](#nodebpy.builder.socket.ColorSocketList.i) |  |
| [`instance`](#nodebpy.builder.socket.ColorSocketList.instance) | ColorSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`layer`](#nodebpy.builder.socket.ColorSocketList.layer) | ColorSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`links`](#nodebpy.builder.socket.ColorSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.ColorSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.ColorSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.ColorSocketList.o) |  |
| [`point`](#nodebpy.builder.socket.ColorSocketList.point) | BooleanSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`r`](#nodebpy.builder.socket.ColorSocketList.r) |  |
| [`socket`](#nodebpy.builder.socket.ColorSocketList.socket) |  |
| [`spline`](#nodebpy.builder.socket.ColorSocketList.spline) | ColorSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`tree`](#nodebpy.builder.socket.ColorSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.ColorSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ColorSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.ColorSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.ColorSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.ColorSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.ColorSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.ColorSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.ColorSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [to_list](#nodebpy.builder.socket.ColorSocketList.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

### FloatSocket

``` python
FloatSocket(socket)
```

Runtime float socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FloatSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.FloatSocket.corner) | FloatSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`default_value`](#nodebpy.builder.socket.FloatSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`edge`](#nodebpy.builder.socket.FloatSocket.edge) | FloatSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`face`](#nodebpy.builder.socket.FloatSocket.face) | FloatSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`i`](#nodebpy.builder.socket.FloatSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.FloatSocket.instance) | FloatSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`layer`](#nodebpy.builder.socket.FloatSocket.layer) | FloatSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`links`](#nodebpy.builder.socket.FloatSocket.links) |  |
| [`mix`](#nodebpy.builder.socket.FloatSocket.mix) | Create a `Mix` node using this socket as the factor. |
| [`name`](#nodebpy.builder.socket.FloatSocket.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocket.node) |  |
| [`o`](#nodebpy.builder.socket.FloatSocket.o) |  |
| [`point`](#nodebpy.builder.socket.FloatSocket.point) | FloatSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`socket`](#nodebpy.builder.socket.FloatSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.FloatSocket.spline) | FloatSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`tree`](#nodebpy.builder.socket.FloatSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [ceil](#nodebpy.builder.socket.FloatSocket.ceil) | Round up to the nearest integer. |
| [clamp](#nodebpy.builder.socket.FloatSocket.clamp) | Clamp the value to *\[min, max\]*. Defaults to the unit interval `[0, 1]`. |
| [enable_output](#nodebpy.builder.socket.FloatSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
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
| [to_list](#nodebpy.builder.socket.FloatSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
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

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

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

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

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

### FloatSocketGrid

``` python
FloatSocketGrid(socket)
```

Runtime float grid socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`background_value`](#nodebpy.builder.socket.FloatSocketGrid.background_value) |  |
| [`builder_node`](#nodebpy.builder.socket.FloatSocketGrid.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.FloatSocketGrid.i) |  |
| [`links`](#nodebpy.builder.socket.FloatSocketGrid.links) |  |
| [`mix`](#nodebpy.builder.socket.FloatSocketGrid.mix) | Create a `Mix` node using this socket as the factor. |
| [`name`](#nodebpy.builder.socket.FloatSocketGrid.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocketGrid.node) |  |
| [`o`](#nodebpy.builder.socket.FloatSocketGrid.o) |  |
| [`socket`](#nodebpy.builder.socket.FloatSocketGrid.socket) |  |
| [`transform`](#nodebpy.builder.socket.FloatSocketGrid.transform) |  |
| [`tree`](#nodebpy.builder.socket.FloatSocketGrid.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocketGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [ceil](#nodebpy.builder.socket.FloatSocketGrid.ceil) | Round up to the nearest integer. |
| [clamp](#nodebpy.builder.socket.FloatSocketGrid.clamp) | Clamp the value to *\[min, max\]*. Defaults to the unit interval `[0, 1]`. |
| [clip](#nodebpy.builder.socket.FloatSocketGrid.clip) | Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value. |
| [dilate_erode](#nodebpy.builder.socket.FloatSocketGrid.dilate_erode) | Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values. |
| [enable_output](#nodebpy.builder.socket.FloatSocketGrid.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [field_to_grid](#nodebpy.builder.socket.FloatSocketGrid.field_to_grid) | Create new grids by evaluating new values on an existing volume grid topology. |
| [floor](#nodebpy.builder.socket.FloatSocketGrid.floor) | Round down to the nearest integer. |
| [gradient](#nodebpy.builder.socket.FloatSocketGrid.gradient) | Calculate the direction and magnitude of the change in values of a scalar grid. |
| [laplacian](#nodebpy.builder.socket.FloatSocketGrid.laplacian) | Compute the divergence of the gradient of the input grid. |
| [map_range](#nodebpy.builder.socket.FloatSocketGrid.map_range) | Remap the values on the float socket using the MapRange node. |
| [mean](#nodebpy.builder.socket.FloatSocketGrid.mean) | Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [median](#nodebpy.builder.socket.FloatSocketGrid.median) | Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [modulo](#nodebpy.builder.socket.FloatSocketGrid.modulo) | Floored modulo — remainder after dividing by *divisor*, always non-negative. |
| [negate](#nodebpy.builder.socket.FloatSocketGrid.negate) | Negate the `FloatSocket` by multiplying the value by `-1`. |
| [power](#nodebpy.builder.socket.FloatSocketGrid.power) | Raise this value to *exponent*. |
| [prune](#nodebpy.builder.socket.FloatSocketGrid.prune) | Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes. |
| [round](#nodebpy.builder.socket.FloatSocketGrid.round) | Round to the nearest integer. |
| [sample](#nodebpy.builder.socket.FloatSocketGrid.sample) | Retrieve values from the specified volume grid. |
| [sample_index](#nodebpy.builder.socket.FloatSocketGrid.sample_index) | Retrieve volume grid values at specific voxels. |
| [sdf_fillet](#nodebpy.builder.socket.FloatSocketGrid.sdf_fillet) | Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces. |
| [sdf_laplacian](#nodebpy.builder.socket.FloatSocketGrid.sdf_laplacian) | Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization. |
| [sdf_mean](#nodebpy.builder.socket.FloatSocketGrid.sdf_mean) | Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field. |
| [sdf_mean_curvature](#nodebpy.builder.socket.FloatSocketGrid.sdf_mean_curvature) | Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas. |
| [sdf_median](#nodebpy.builder.socket.FloatSocketGrid.sdf_median) | Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field. |
| [sdf_offset](#nodebpy.builder.socket.FloatSocketGrid.sdf_offset) | Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property. |
| [sign](#nodebpy.builder.socket.FloatSocketGrid.sign) | Return the sign of the FloatSocket, eithe `-1`, `0` or `1`. |
| [sqrt](#nodebpy.builder.socket.FloatSocketGrid.sqrt) | Return the square root of this value. |
| [to_degrees](#nodebpy.builder.socket.FloatSocketGrid.to_degrees) | Convert radians to degrees. |
| [to_mesh](#nodebpy.builder.socket.FloatSocketGrid.to_mesh) | Generate a mesh on the “surface” of a volume grid. |
| [to_points](#nodebpy.builder.socket.FloatSocketGrid.to_points) | Generate a point cloud from a volume grid’s active voxels. |
| [to_radians](#nodebpy.builder.socket.FloatSocketGrid.to_radians) | Convert degrees to radians. |
| [voxelize](#nodebpy.builder.socket.FloatSocketGrid.voxelize) | Remove sparseness from a volume grid by making the active tiles into voxels. |
| [wrap](#nodebpy.builder.socket.FloatSocketGrid.wrap) | Wrap the value into the *\[min, max\]* range, repeating cyclically. |

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

##### clip

``` python
clip(min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value.

##### dilate_erode

``` python
dilate_erode(steps=1, connectivity='Face', tiles='Preserve')
```

Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### field_to_grid

``` python
field_to_grid()
```

Create new grids by evaluating new values on an existing volume grid topology.

##### floor

``` python
floor()
```

Round down to the nearest integer.

##### gradient

``` python
gradient()
```

Calculate the direction and magnitude of the change in values of a scalar grid.

##### laplacian

``` python
laplacian()
```

Compute the divergence of the gradient of the input grid.

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

##### mean

``` python
mean(width=1, iterations=1)
```

Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

##### median

``` python
median(width=1, iterations=1)
```

Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

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

##### prune

``` python
prune(threshold=0.1, mode=None)
```

Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes.

##### round

``` python
round()
```

Round to the nearest integer.

##### sample

``` python
sample(position=None, interpolation='Trilinear')
```

Retrieve values from the specified volume grid.

##### sample_index

``` python
sample_index(x=0, y=0, z=0)
```

Retrieve volume grid values at specific voxels.

##### sdf_fillet

``` python
sdf_fillet(iterations=1)
```

Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces.

##### sdf_laplacian

``` python
sdf_laplacian(iterations=1)
```

Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization.

##### sdf_mean

``` python
sdf_mean(width=1, iterations=1)
```

Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field.

##### sdf_mean_curvature

``` python
sdf_mean_curvature(iterations=1)
```

Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas.

##### sdf_median

``` python
sdf_median(width=1, iterations=1)
```

Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field.

##### sdf_offset

``` python
sdf_offset(distance=0.1)
```

Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property.

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

##### to_mesh

``` python
to_mesh(threshold=0.1, adaptivity=0.0)
```

Generate a mesh on the “surface” of a volume grid.

##### to_points

``` python
to_points()
```

Generate a point cloud from a volume grid’s active voxels.

##### to_radians

``` python
to_radians()
```

Convert degrees to radians.

##### voxelize

``` python
voxelize()
```

Remove sparseness from a volume grid by making the active tiles into voxels.

##### wrap

``` python
wrap(min, max)
```

Wrap the value into the *\[min, max\]* range, repeating cyclically.

### FloatSocketList

``` python
FloatSocketList(socket)
```

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FloatSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.FloatSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.FloatSocketList.links) |  |
| [`mix`](#nodebpy.builder.socket.FloatSocketList.mix) | Create a `Mix` node using this socket as the factor. |
| [`name`](#nodebpy.builder.socket.FloatSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.FloatSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.FloatSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.FloatSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.FloatSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.FloatSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [ceil](#nodebpy.builder.socket.FloatSocketList.ceil) | Round up to the nearest integer. |
| [clamp](#nodebpy.builder.socket.FloatSocketList.clamp) | Clamp the value to *\[min, max\]*. Defaults to the unit interval `[0, 1]`. |
| [enable_output](#nodebpy.builder.socket.FloatSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.FloatSocketList.filter) | Filter the list based on the selection. |
| [floor](#nodebpy.builder.socket.FloatSocketList.floor) | Round down to the nearest integer. |
| [get](#nodebpy.builder.socket.FloatSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.FloatSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.FloatSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [map_range](#nodebpy.builder.socket.FloatSocketList.map_range) | Remap the values on the float socket using the MapRange node. |
| [modulo](#nodebpy.builder.socket.FloatSocketList.modulo) | Floored modulo — remainder after dividing by *divisor*, always non-negative. |
| [negate](#nodebpy.builder.socket.FloatSocketList.negate) | Negate the `FloatSocket` by multiplying the value by `-1`. |
| [power](#nodebpy.builder.socket.FloatSocketList.power) | Raise this value to *exponent*. |
| [reverse](#nodebpy.builder.socket.FloatSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [round](#nodebpy.builder.socket.FloatSocketList.round) | Round to the nearest integer. |
| [sign](#nodebpy.builder.socket.FloatSocketList.sign) | Return the sign of the FloatSocket, eithe `-1`, `0` or `1`. |
| [sort](#nodebpy.builder.socket.FloatSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [sqrt](#nodebpy.builder.socket.FloatSocketList.sqrt) | Return the square root of this value. |
| [to_degrees](#nodebpy.builder.socket.FloatSocketList.to_degrees) | Convert radians to degrees. |
| [to_integer](#nodebpy.builder.socket.FloatSocketList.to_integer) | Convert the `FloatSocket` to an `IntegerSocket` by truncating the decimal part. |
| [to_radians](#nodebpy.builder.socket.FloatSocketList.to_radians) | Convert degrees to radians. |
| [to_string](#nodebpy.builder.socket.FloatSocketList.to_string) | Convert the `FloatSocket` to a `StringSocket` wtih the given number of decimal places |
| [wrap](#nodebpy.builder.socket.FloatSocketList.wrap) | Wrap the value into the *\[min, max\]* range, repeating cyclically. |

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

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### floor

``` python
floor()
```

Round down to the nearest integer.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

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

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

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

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.FontSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### FontSocketList

``` python
FontSocketList(socket)
```

List of font sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.FontSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.FontSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.FontSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.FontSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.FontSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.FontSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.FontSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.FontSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.FontSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.FontSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.FontSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.FontSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.FontSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.FontSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.FontSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.FontSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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
| [enable_output](#nodebpy.builder.socket.GeometrySocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [realize_instances](#nodebpy.builder.socket.GeometrySocket.realize_instances) |  |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### realize_instances

``` python
realize_instances(selection=True, realize_all=False, depth=0)
```

### GeometrySocketList

``` python
GeometrySocketList(socket)
```

List of geometry sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.GeometrySocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.GeometrySocketList.i) |  |
| [`links`](#nodebpy.builder.socket.GeometrySocketList.links) |  |
| [`name`](#nodebpy.builder.socket.GeometrySocketList.name) |  |
| [`node`](#nodebpy.builder.socket.GeometrySocketList.node) |  |
| [`o`](#nodebpy.builder.socket.GeometrySocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.GeometrySocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.GeometrySocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.GeometrySocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.GeometrySocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.GeometrySocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.GeometrySocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.GeometrySocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.GeometrySocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [realize_instances](#nodebpy.builder.socket.GeometrySocketList.realize_instances) |  |
| [reverse](#nodebpy.builder.socket.GeometrySocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.GeometrySocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### realize_instances

``` python
realize_instances(selection=True, realize_all=False, depth=0)
```

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### ImageSocket

``` python
ImageSocket(socket)
```

Runtime image socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ImageSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.ImageSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`i`](#nodebpy.builder.socket.ImageSocket.i) |  |
| [`links`](#nodebpy.builder.socket.ImageSocket.links) |  |
| [`name`](#nodebpy.builder.socket.ImageSocket.name) |  |
| [`node`](#nodebpy.builder.socket.ImageSocket.node) |  |
| [`o`](#nodebpy.builder.socket.ImageSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.ImageSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.ImageSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.ImageSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ImageSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### ImageSocketList

``` python
ImageSocketList(socket)
```

List of image sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ImageSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ImageSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.ImageSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.ImageSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.ImageSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.ImageSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.ImageSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.ImageSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.ImageSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ImageSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.ImageSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.ImageSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.ImageSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.ImageSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.ImageSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.ImageSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### IntegerSocket

``` python
IntegerSocket(socket)
```

Runtime integer socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.IntegerSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.IntegerSocket.corner) | IntegerSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`default_value`](#nodebpy.builder.socket.IntegerSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`edge`](#nodebpy.builder.socket.IntegerSocket.edge) | IntegerSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`face`](#nodebpy.builder.socket.IntegerSocket.face) | IntegerSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`i`](#nodebpy.builder.socket.IntegerSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.IntegerSocket.instance) | IntegerSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`layer`](#nodebpy.builder.socket.IntegerSocket.layer) | IntegerSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`links`](#nodebpy.builder.socket.IntegerSocket.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocket.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocket.node) |  |
| [`o`](#nodebpy.builder.socket.IntegerSocket.o) |  |
| [`point`](#nodebpy.builder.socket.IntegerSocket.point) | IntegerSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`socket`](#nodebpy.builder.socket.IntegerSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.IntegerSocket.spline) | IntegerSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`. |
| [`tree`](#nodebpy.builder.socket.IntegerSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [abs](#nodebpy.builder.socket.IntegerSocket.abs) | Return the absolute value of the IntegerSocket. |
| [clamp](#nodebpy.builder.socket.IntegerSocket.clamp) | Clamp the value to *\[min, max\]*. |
| [enable_output](#nodebpy.builder.socket.IntegerSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [modulo](#nodebpy.builder.socket.IntegerSocket.modulo) | Remainder after dividing by *divisor* (always non-negative). |
| [negate](#nodebpy.builder.socket.IntegerSocket.negate) | Negate the IntegerSocket value. Positive becomes negative, negative becomes positive. |
| [sign](#nodebpy.builder.socket.IntegerSocket.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |
| [to_list](#nodebpy.builder.socket.IntegerSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
| [to_string](#nodebpy.builder.socket.IntegerSocket.to_string) | Convert the `IntegerSocket` to a `StringSocket`. |

##### abs

``` python
abs()
```

Return the absolute value of the IntegerSocket.

##### clamp

``` python
clamp(min=0, max=1)
```

Clamp the value to *\[min, max\]*.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### modulo

``` python
modulo(divisor)
```

Remainder after dividing by *divisor* (always non-negative).

##### negate

``` python
negate()
```

Negate the IntegerSocket value. Positive becomes negative, negative becomes positive.

##### sign

``` python
sign()
```

Return the sign of the IntegerSocket, either `-1`, `0`, or `1`.

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

##### to_string

``` python
to_string()
```

Convert the `IntegerSocket` to a `StringSocket`.

### IntegerSocketGrid

``` python
IntegerSocketGrid(socket)
```

Runtime integer grid socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`background_value`](#nodebpy.builder.socket.IntegerSocketGrid.background_value) |  |
| [`builder_node`](#nodebpy.builder.socket.IntegerSocketGrid.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.IntegerSocketGrid.i) |  |
| [`links`](#nodebpy.builder.socket.IntegerSocketGrid.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocketGrid.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocketGrid.node) |  |
| [`o`](#nodebpy.builder.socket.IntegerSocketGrid.o) |  |
| [`socket`](#nodebpy.builder.socket.IntegerSocketGrid.socket) |  |
| [`transform`](#nodebpy.builder.socket.IntegerSocketGrid.transform) |  |
| [`tree`](#nodebpy.builder.socket.IntegerSocketGrid.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocketGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [abs](#nodebpy.builder.socket.IntegerSocketGrid.abs) | Return the absolute value of the IntegerSocket. |
| [clamp](#nodebpy.builder.socket.IntegerSocketGrid.clamp) | Clamp the value to *\[min, max\]*. |
| [clip](#nodebpy.builder.socket.IntegerSocketGrid.clip) | Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value. |
| [dilate_erode](#nodebpy.builder.socket.IntegerSocketGrid.dilate_erode) | Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values. |
| [enable_output](#nodebpy.builder.socket.IntegerSocketGrid.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [field_to_grid](#nodebpy.builder.socket.IntegerSocketGrid.field_to_grid) | Create new grids by evaluating new values on an existing volume grid topology. |
| [mean](#nodebpy.builder.socket.IntegerSocketGrid.mean) | Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [median](#nodebpy.builder.socket.IntegerSocketGrid.median) | Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [modulo](#nodebpy.builder.socket.IntegerSocketGrid.modulo) | Remainder after dividing by *divisor* (always non-negative). |
| [negate](#nodebpy.builder.socket.IntegerSocketGrid.negate) | Negate the IntegerSocket value. Positive becomes negative, negative becomes positive. |
| [prune](#nodebpy.builder.socket.IntegerSocketGrid.prune) | Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes. |
| [sample](#nodebpy.builder.socket.IntegerSocketGrid.sample) | Retrieve values from the specified volume grid. |
| [sample_index](#nodebpy.builder.socket.IntegerSocketGrid.sample_index) | Retrieve volume grid values at specific voxels. |
| [sign](#nodebpy.builder.socket.IntegerSocketGrid.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |
| [to_points](#nodebpy.builder.socket.IntegerSocketGrid.to_points) | Generate a point cloud from a volume grid’s active voxels. |
| [voxelize](#nodebpy.builder.socket.IntegerSocketGrid.voxelize) | Remove sparseness from a volume grid by making the active tiles into voxels. |

##### abs

``` python
abs()
```

Return the absolute value of the IntegerSocket.

##### clamp

``` python
clamp(min=0, max=1)
```

Clamp the value to *\[min, max\]*.

##### clip

``` python
clip(min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value.

##### dilate_erode

``` python
dilate_erode(steps=1, connectivity='Face', tiles='Preserve')
```

Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### field_to_grid

``` python
field_to_grid()
```

Create new grids by evaluating new values on an existing volume grid topology.

##### mean

``` python
mean(width=1, iterations=1)
```

Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

##### median

``` python
median(width=1, iterations=1)
```

Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

##### modulo

``` python
modulo(divisor)
```

Remainder after dividing by *divisor* (always non-negative).

##### negate

``` python
negate()
```

Negate the IntegerSocket value. Positive becomes negative, negative becomes positive.

##### prune

``` python
prune(threshold=0.1, mode=None)
```

Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes.

##### sample

``` python
sample(position=None, interpolation='Trilinear')
```

Retrieve values from the specified volume grid.

##### sample_index

``` python
sample_index(x=0, y=0, z=0)
```

Retrieve volume grid values at specific voxels.

##### sign

``` python
sign()
```

Return the sign of the IntegerSocket, either `-1`, `0`, or `1`.

##### to_points

``` python
to_points()
```

Generate a point cloud from a volume grid’s active voxels.

##### voxelize

``` python
voxelize()
```

Remove sparseness from a volume grid by making the active tiles into voxels.

### IntegerSocketList

``` python
IntegerSocketList(socket)
```

List of integer sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.IntegerSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.IntegerSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.IntegerSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.IntegerSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.IntegerSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.IntegerSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [abs](#nodebpy.builder.socket.IntegerSocketList.abs) | Return the absolute value of the IntegerSocket. |
| [clamp](#nodebpy.builder.socket.IntegerSocketList.clamp) | Clamp the value to *\[min, max\]*. |
| [enable_output](#nodebpy.builder.socket.IntegerSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.IntegerSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.IntegerSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.IntegerSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.IntegerSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [modulo](#nodebpy.builder.socket.IntegerSocketList.modulo) | Remainder after dividing by *divisor* (always non-negative). |
| [negate](#nodebpy.builder.socket.IntegerSocketList.negate) | Negate the IntegerSocket value. Positive becomes negative, negative becomes positive. |
| [reverse](#nodebpy.builder.socket.IntegerSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sign](#nodebpy.builder.socket.IntegerSocketList.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |
| [sort](#nodebpy.builder.socket.IntegerSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [to_string](#nodebpy.builder.socket.IntegerSocketList.to_string) | Convert the `IntegerSocket` to a `StringSocket`. |

##### abs

``` python
abs()
```

Return the absolute value of the IntegerSocket.

##### clamp

``` python
clamp(min=0, max=1)
```

Clamp the value to *\[min, max\]*.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### modulo

``` python
modulo(divisor)
```

Remainder after dividing by *divisor* (always non-negative).

##### negate

``` python
negate()
```

Negate the IntegerSocket value. Positive becomes negative, negative becomes positive.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sign

``` python
sign()
```

Return the sign of the IntegerSocket, either `-1`, `0`, or `1`.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

##### to_string

``` python
to_string()
```

Convert the `IntegerSocket` to a `StringSocket`.

### IntegerVectorSocket

``` python
IntegerVectorSocket(socket)
```

Runtime integer vector socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.IntegerVectorSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.IntegerVectorSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`i`](#nodebpy.builder.socket.IntegerVectorSocket.i) |  |
| [`links`](#nodebpy.builder.socket.IntegerVectorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.IntegerVectorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.IntegerVectorSocket.node) |  |
| [`o`](#nodebpy.builder.socket.IntegerVectorSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.IntegerVectorSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.IntegerVectorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.IntegerVectorSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [abs](#nodebpy.builder.socket.IntegerVectorSocket.abs) | Return the absolute value of the IntegerSocket. |
| [clamp](#nodebpy.builder.socket.IntegerVectorSocket.clamp) | Clamp the value to *\[min, max\]*. |
| [enable_output](#nodebpy.builder.socket.IntegerVectorSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [modulo](#nodebpy.builder.socket.IntegerVectorSocket.modulo) | Remainder after dividing by *divisor* (always non-negative). |
| [negate](#nodebpy.builder.socket.IntegerVectorSocket.negate) | Negate the IntegerSocket value. Positive becomes negative, negative becomes positive. |
| [sign](#nodebpy.builder.socket.IntegerVectorSocket.sign) | Return the sign of the IntegerSocket, either `-1`, `0`, or `1`. |

##### abs

``` python
abs()
```

Return the absolute value of the IntegerSocket.

##### clamp

``` python
clamp(min=0, max=1)
```

Clamp the value to *\[min, max\]*.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### modulo

``` python
modulo(divisor)
```

Remainder after dividing by *divisor* (always non-negative).

##### negate

``` python
negate()
```

Negate the IntegerSocket value. Positive becomes negative, negative becomes positive.

##### sign

``` python
sign()
```

Return the sign of the IntegerSocket, either `-1`, `0`, or `1`.

### MaterialSocket

``` python
MaterialSocket(socket)
```

Runtime material socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MaterialSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.MaterialSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`i`](#nodebpy.builder.socket.MaterialSocket.i) |  |
| [`links`](#nodebpy.builder.socket.MaterialSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MaterialSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MaterialSocket.node) |  |
| [`o`](#nodebpy.builder.socket.MaterialSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.MaterialSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.MaterialSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MaterialSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.MaterialSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### MaterialSocketList

``` python
MaterialSocketList(socket)
```

List of material sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MaterialSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.MaterialSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.MaterialSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.MaterialSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.MaterialSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.MaterialSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.MaterialSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.MaterialSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.MaterialSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.MaterialSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.MaterialSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.MaterialSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.MaterialSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.MaterialSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.MaterialSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.MaterialSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### MatrixSocket

``` python
MatrixSocket(socket)
```

Runtime matrix socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MatrixSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.MatrixSocket.corner) | MatrixSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`edge`](#nodebpy.builder.socket.MatrixSocket.edge) | MatrixSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`face`](#nodebpy.builder.socket.MatrixSocket.face) | MatrixSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`i`](#nodebpy.builder.socket.MatrixSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.MatrixSocket.instance) | MatrixSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`layer`](#nodebpy.builder.socket.MatrixSocket.layer) | MatrixSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`links`](#nodebpy.builder.socket.MatrixSocket.links) |  |
| [`name`](#nodebpy.builder.socket.MatrixSocket.name) |  |
| [`node`](#nodebpy.builder.socket.MatrixSocket.node) |  |
| [`o`](#nodebpy.builder.socket.MatrixSocket.o) |  |
| [`point`](#nodebpy.builder.socket.MatrixSocket.point) | MatrixSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`rotation`](#nodebpy.builder.socket.MatrixSocket.rotation) | Get the rotation component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`scale`](#nodebpy.builder.socket.MatrixSocket.scale) | Get the scale component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`socket`](#nodebpy.builder.socket.MatrixSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.MatrixSocket.spline) | MatrixSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`. |
| [`translation`](#nodebpy.builder.socket.MatrixSocket.translation) | Get the translation component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`tree`](#nodebpy.builder.socket.MatrixSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.MatrixSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [determinant](#nodebpy.builder.socket.MatrixSocket.determinant) | Compute the determinant of a matrix input and return as a `FloatSocket`. |
| [enable_output](#nodebpy.builder.socket.MatrixSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [invert](#nodebpy.builder.socket.MatrixSocket.invert) | Invert the `MatrixSocet` and return a `MatrixSocket`. |
| [svd](#nodebpy.builder.socket.MatrixSocket.svd) | Decompose the matrix via SVD. Returns `(u, s, v)`. |
| [to_list](#nodebpy.builder.socket.MatrixSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
| [transform_direction](#nodebpy.builder.socket.MatrixSocket.transform_direction) | Apply this matrix to *direction*, ignoring translation. |
| [transpose](#nodebpy.builder.socket.MatrixSocket.transpose) | Transpose the `MatrixSocket` and return a `MatrixSocket`. |

##### determinant

``` python
determinant()
```

Compute the determinant of a matrix input and return as a `FloatSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### invert

``` python
invert()
```

Invert the `MatrixSocet` and return a `MatrixSocket`.

##### svd

``` python
svd()
```

Decompose the matrix via SVD. Returns `(u, s, v)`.

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

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

Transpose the `MatrixSocket` and return a `MatrixSocket`.

### MatrixSocketList

``` python
MatrixSocketList(socket)
```

List of matrix sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MatrixSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.MatrixSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.MatrixSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.MatrixSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.MatrixSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.MatrixSocketList.o) |  |
| [`rotation`](#nodebpy.builder.socket.MatrixSocketList.rotation) | Get the rotation component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`scale`](#nodebpy.builder.socket.MatrixSocketList.scale) | Get the scale component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`socket`](#nodebpy.builder.socket.MatrixSocketList.socket) |  |
| [`translation`](#nodebpy.builder.socket.MatrixSocketList.translation) | Get the translation component of the matrix, via \[`~nodebpy.nodes.geometry.converter.SeparateTransform`\]. |
| [`tree`](#nodebpy.builder.socket.MatrixSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.MatrixSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [determinant](#nodebpy.builder.socket.MatrixSocketList.determinant) | Compute the determinant of a matrix input and return as a `FloatSocket`. |
| [enable_output](#nodebpy.builder.socket.MatrixSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.MatrixSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.MatrixSocketList.get) | Get the item at the given index from the list. |
| [invert](#nodebpy.builder.socket.MatrixSocketList.invert) | Invert the `MatrixSocet` and return a `MatrixSocket`. |
| [list_length](#nodebpy.builder.socket.MatrixSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.MatrixSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.MatrixSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.MatrixSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [svd](#nodebpy.builder.socket.MatrixSocketList.svd) | Decompose the matrix via SVD. Returns `(u, s, v)`. |
| [transform_direction](#nodebpy.builder.socket.MatrixSocketList.transform_direction) | Apply this matrix to *direction*, ignoring translation. |
| [transpose](#nodebpy.builder.socket.MatrixSocketList.transpose) | Transpose the `MatrixSocket` and return a `MatrixSocket`. |

##### determinant

``` python
determinant()
```

Compute the determinant of a matrix input and return as a `FloatSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### invert

``` python
invert()
```

Invert the `MatrixSocet` and return a `MatrixSocket`.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

Transpose the `MatrixSocket` and return a `MatrixSocket`.

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.MenuSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [to_list](#nodebpy.builder.socket.MenuSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

### MenuSocketList

``` python
MenuSocketList(socket)
```

List of menu sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.MenuSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.MenuSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.MenuSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.MenuSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.MenuSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.MenuSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.MenuSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.MenuSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.MenuSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.MenuSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.MenuSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.MenuSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.MenuSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.MenuSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.MenuSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.MenuSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### ObjectSocket

``` python
ObjectSocket(socket)
```

Runtime object socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ObjectSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.ObjectSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
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
| [enable_output](#nodebpy.builder.socket.ObjectSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [geometry](#nodebpy.builder.socket.ObjectSocket.geometry) | The object’s geometry, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [location](#nodebpy.builder.socket.ObjectSocket.location) | The object’s location, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [rotation](#nodebpy.builder.socket.ObjectSocket.rotation) | The object’s rotation, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [scale](#nodebpy.builder.socket.ObjectSocket.scale) | The object’s scale, optionally in relative space, via [`ObjectInfo`](~nodebpy.nodes.geometry.ObjectInfo). |
| [transform](#nodebpy.builder.socket.ObjectSocket.transform) | The Object’s transform matrix, optionally in relative space. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

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

### ObjectSocketList

``` python
ObjectSocketList(socket)
```

List of object sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ObjectSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ObjectSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.ObjectSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.ObjectSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.ObjectSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.ObjectSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.ObjectSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.ObjectSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.ObjectSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ObjectSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.ObjectSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.ObjectSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.ObjectSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.ObjectSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.ObjectSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.ObjectSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### ResultAxisAngle

``` python
ResultAxisAngle()
```

Axis-angle components returned by `RotationSocket.to_axis_angle()`.

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`angle`](#nodebpy.builder.socket.ResultAxisAngle.angle) |             |
| [`axis`](#nodebpy.builder.socket.ResultAxisAngle.axis)   |             |

### ResultMatrixSVD

``` python
ResultMatrixSVD()
```

SVD components returned by `MatrixSocket.svd()`.

#### Attributes

| Name                                             | Description |
|--------------------------------------------------|-------------|
| [`s`](#nodebpy.builder.socket.ResultMatrixSVD.s) |             |
| [`u`](#nodebpy.builder.socket.ResultMatrixSVD.u) |             |
| [`v`](#nodebpy.builder.socket.ResultMatrixSVD.v) |             |

### ResultQuaternionComponents

``` python
ResultQuaternionComponents()
```

Quaternion components returned by `RotationSocket.to_quaternion()`.

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`w`](#nodebpy.builder.socket.ResultQuaternionComponents.w) |             |
| [`x`](#nodebpy.builder.socket.ResultQuaternionComponents.x) |             |
| [`y`](#nodebpy.builder.socket.ResultQuaternionComponents.y) |             |
| [`z`](#nodebpy.builder.socket.ResultQuaternionComponents.z) |             |

### ResultStringFind

``` python
ResultStringFind()
```

Result of `StringSocket.find()`.

#### Attributes

| Name | Description |
|----|----|
| [`count`](#nodebpy.builder.socket.ResultStringFind.count) |  |
| [`first_found`](#nodebpy.builder.socket.ResultStringFind.first_found) |  |

### RotationSocket

``` python
RotationSocket(socket)
```

Runtime rotation socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.RotationSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.RotationSocket.corner) | RotationSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`default_value`](#nodebpy.builder.socket.RotationSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
| [`edge`](#nodebpy.builder.socket.RotationSocket.edge) | RotationSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`face`](#nodebpy.builder.socket.RotationSocket.face) | RotationSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`i`](#nodebpy.builder.socket.RotationSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.RotationSocket.instance) | RotationSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`layer`](#nodebpy.builder.socket.RotationSocket.layer) | RotationSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`links`](#nodebpy.builder.socket.RotationSocket.links) |  |
| [`name`](#nodebpy.builder.socket.RotationSocket.name) |  |
| [`node`](#nodebpy.builder.socket.RotationSocket.node) |  |
| [`o`](#nodebpy.builder.socket.RotationSocket.o) |  |
| [`point`](#nodebpy.builder.socket.RotationSocket.point) | RotationSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`socket`](#nodebpy.builder.socket.RotationSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.RotationSocket.spline) | RotationSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`. |
| [`tree`](#nodebpy.builder.socket.RotationSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.RotationSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [align_to_vector](#nodebpy.builder.socket.RotationSocket.align_to_vector) | Align the specified axis of this rotation to the given vector. Uses `AlignRotationToVector` with this socket as the rotation input. |
| [enable_output](#nodebpy.builder.socket.RotationSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [invert](#nodebpy.builder.socket.RotationSocket.invert) | Invert the rotation of the socket. |
| [rotate](#nodebpy.builder.socket.RotationSocket.rotate) | Rotate this rotation by the given rotation in the specified rotation space. |
| [to_axis_angle](#nodebpy.builder.socket.RotationSocket.to_axis_angle) | Decompose the rotation into axis-angle components `(axis, angle)`. |
| [to_euler](#nodebpy.builder.socket.RotationSocket.to_euler) | Convert the rotation to an XYZ euler rotation and return `VectorSocket`. |
| [to_list](#nodebpy.builder.socket.RotationSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
| [to_quaternion](#nodebpy.builder.socket.RotationSocket.to_quaternion) | Decompose the rotation into quaternion components `(w, x, y, z)`. |

##### align_to_vector

``` python
align_to_vector(
    vector=(0.0, 0.0, 1.0),
    factor=1.0,
    *,
    axis='Z',
    pivot_axis='AUTO',
)
```

Align the specified axis of this rotation to the given vector. Uses `AlignRotationToVector` with this socket as the rotation input.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

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

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

##### to_quaternion

``` python
to_quaternion()
```

Decompose the rotation into quaternion components `(w, x, y, z)`.

### RotationSocketList

``` python
RotationSocketList(socket)
```

List of rotation sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.RotationSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.RotationSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.RotationSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.RotationSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.RotationSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.RotationSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.RotationSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.RotationSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.RotationSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [align_to_vector](#nodebpy.builder.socket.RotationSocketList.align_to_vector) | Align the specified axis of this rotation to the given vector. Uses `AlignRotationToVector` with this socket as the rotation input. |
| [enable_output](#nodebpy.builder.socket.RotationSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.RotationSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.RotationSocketList.get) | Get the item at the given index from the list. |
| [invert](#nodebpy.builder.socket.RotationSocketList.invert) | Invert the rotation of the socket. |
| [list_length](#nodebpy.builder.socket.RotationSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.RotationSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.RotationSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [rotate](#nodebpy.builder.socket.RotationSocketList.rotate) | Rotate this rotation by the given rotation in the specified rotation space. |
| [sort](#nodebpy.builder.socket.RotationSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [to_axis_angle](#nodebpy.builder.socket.RotationSocketList.to_axis_angle) | Decompose the rotation into axis-angle components `(axis, angle)`. |
| [to_euler](#nodebpy.builder.socket.RotationSocketList.to_euler) | Convert the rotation to an XYZ euler rotation and return `VectorSocket`. |
| [to_quaternion](#nodebpy.builder.socket.RotationSocketList.to_quaternion) | Decompose the rotation into quaternion components `(w, x, y, z)`. |

##### align_to_vector

``` python
align_to_vector(
    vector=(0.0, 0.0, 1.0),
    factor=1.0,
    *,
    axis='Z',
    pivot_axis='AUTO',
)
```

Align the specified axis of this rotation to the given vector. Uses `AlignRotationToVector` with this socket as the rotation input.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### invert

``` python
invert()
```

Invert the rotation of the socket.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### rotate

``` python
rotate(rotation, rotation_space='GLOBAL')
```

Rotate this rotation by the given rotation in the specified rotation space.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ShaderSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### ShaderSocketList

``` python
ShaderSocketList(socket)
```

List of shader sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.ShaderSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.ShaderSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.ShaderSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.ShaderSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.ShaderSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.ShaderSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.ShaderSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.ShaderSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.ShaderSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.ShaderSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.ShaderSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.ShaderSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.ShaderSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.ShaderSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.ShaderSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.ShaderSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

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

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.Socket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### SoundSocket

``` python
SoundSocket(socket)
```

Runtime sound socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.SoundSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.SoundSocket.i) |  |
| [`links`](#nodebpy.builder.socket.SoundSocket.links) |  |
| [`name`](#nodebpy.builder.socket.SoundSocket.name) |  |
| [`node`](#nodebpy.builder.socket.SoundSocket.node) |  |
| [`o`](#nodebpy.builder.socket.SoundSocket.o) |  |
| [`socket`](#nodebpy.builder.socket.SoundSocket.socket) |  |
| [`tree`](#nodebpy.builder.socket.SoundSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.SoundSocket.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.SoundSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

### SoundSocketList

``` python
SoundSocketList(socket)
```

List of sound sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.SoundSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.SoundSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.SoundSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.SoundSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.SoundSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.SoundSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.SoundSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.SoundSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.SoundSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [enable_output](#nodebpy.builder.socket.SoundSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.SoundSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.SoundSocketList.get) | Get the item at the given index from the list. |
| [list_length](#nodebpy.builder.socket.SoundSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.SoundSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [reverse](#nodebpy.builder.socket.SoundSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [sort](#nodebpy.builder.socket.SoundSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

### StringSocket

``` python
StringSocket(socket)
```

Runtime string socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.StringSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`default_value`](#nodebpy.builder.socket.StringSocket.default_value) | Get or set the default value of the socket. Only relevant for input sockets. |
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
| [enable_output](#nodebpy.builder.socket.StringSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [ends_with](#nodebpy.builder.socket.StringSocket.ends_with) | Create a MatchString\[Ends With\], return the result as a `BooleanSocket`. |
| [find](#nodebpy.builder.socket.StringSocket.find) | Find where in a string a pattern occurs. Returns `(first_found, count)`. |
| [format](#nodebpy.builder.socket.StringSocket.format) | Format a given string with the key-value items. |
| [join](#nodebpy.builder.socket.StringSocket.join) | Join the input strings with this as the separator. |
| [length](#nodebpy.builder.socket.StringSocket.length) | Compute the length of a string and return as `IntegerSocket`. |
| [lowercase](#nodebpy.builder.socket.StringSocket.lowercase) | Convert the string to lowercase and return as `StringSocket`. |
| [replace](#nodebpy.builder.socket.StringSocket.replace) | Replace every match of the string with the replacement string |
| [reverse](#nodebpy.builder.socket.StringSocket.reverse) | Reverse the string. |
| [slice](#nodebpy.builder.socket.StringSocket.slice) | Slice a given string from a starting position for a given length. |
| [split](#nodebpy.builder.socket.StringSocket.split) |  |
| [starts_with](#nodebpy.builder.socket.StringSocket.starts_with) | Create a MatchString\[Starts With\], return the result as a `BooleanSocket`. |
| [to_list](#nodebpy.builder.socket.StringSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
| [uppercase](#nodebpy.builder.socket.StringSocket.uppercase) | Convert the string to uppercase and return as `StringSocket`. |

##### contains

``` python
contains(search)
```

Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

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

##### lowercase

``` python
lowercase()
```

Convert the string to lowercase and return as `StringSocket`.

##### replace

``` python
replace(find, replace)
```

Replace every match of the string with the replacement string

##### reverse

``` python
reverse()
```

Reverse the string.

##### slice

``` python
slice(position=0, length=0)
```

Slice a given string from a starting position for a given length.

##### split

``` python
split(separator='')
```

##### starts_with

``` python
starts_with(search)
```

Create a MatchString\[Starts With\], return the result as a `BooleanSocket`.

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

##### uppercase

``` python
uppercase()
```

Convert the string to uppercase and return as `StringSocket`.

### StringSocketList

``` python
StringSocketList(socket)
```

List of string sockets.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.StringSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.StringSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.StringSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.StringSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.StringSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.StringSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.StringSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.StringSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.StringSocketList.type) |  |

#### Methods

| Name | Description |
|----|----|
| [contains](#nodebpy.builder.socket.StringSocketList.contains) | Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`. |
| [enable_output](#nodebpy.builder.socket.StringSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [ends_with](#nodebpy.builder.socket.StringSocketList.ends_with) | Create a MatchString\[Ends With\], return the result as a `BooleanSocket`. |
| [filter](#nodebpy.builder.socket.StringSocketList.filter) | Filter the list based on the selection. |
| [find](#nodebpy.builder.socket.StringSocketList.find) | Find where in a string a pattern occurs. Returns `(first_found, count)`. |
| [format](#nodebpy.builder.socket.StringSocketList.format) | Format a given string with the key-value items. |
| [get](#nodebpy.builder.socket.StringSocketList.get) | Get the item at the given index from the list. |
| [length](#nodebpy.builder.socket.StringSocketList.length) | Compute the length of a string and return as `IntegerSocket`. |
| [list_length](#nodebpy.builder.socket.StringSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.StringSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [lowercase](#nodebpy.builder.socket.StringSocketList.lowercase) | Convert the string to lowercase and return as `StringSocket`. |
| [replace](#nodebpy.builder.socket.StringSocketList.replace) | Replace every match of the string with the replacement string |
| [reverse](#nodebpy.builder.socket.StringSocketList.reverse) | Reverse the string. |
| [slice](#nodebpy.builder.socket.StringSocketList.slice) | Slice a given string from a starting position for a given length. |
| [sort](#nodebpy.builder.socket.StringSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [starts_with](#nodebpy.builder.socket.StringSocketList.starts_with) | Create a MatchString\[Starts With\], return the result as a `BooleanSocket`. |
| [uppercase](#nodebpy.builder.socket.StringSocketList.uppercase) | Convert the string to uppercase and return as `StringSocket`. |

##### contains

``` python
contains(search)
```

Create a MatchString[Contains](#nodebpy.builder.socket.StringSocket.contains), return the result as a `BooleanSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### ends_with

``` python
ends_with(search)
```

Create a MatchString\[Ends With\], return the result as a `BooleanSocket`.

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

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

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### length

``` python
length()
```

Compute the length of a string and return as `IntegerSocket`.

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### lowercase

``` python
lowercase()
```

Convert the string to lowercase and return as `StringSocket`.

##### replace

``` python
replace(find, replace)
```

Replace every match of the string with the replacement string

##### reverse

``` python
reverse()
```

Reverse the string.

##### slice

``` python
slice(position=0, length=0)
```

Slice a given string from a starting position for a given length.

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

##### starts_with

``` python
starts_with(search)
```

Create a MatchString\[Starts With\], return the result as a `BooleanSocket`.

##### uppercase

``` python
uppercase()
```

Convert the string to uppercase and return as `StringSocket`.

### VectorSocket

``` python
VectorSocket(socket)
```

Runtime vector socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.VectorSocket.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`corner`](#nodebpy.builder.socket.VectorSocket.corner) | VectorSocket `corner` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`default_value`](#nodebpy.builder.socket.VectorSocket.default_value) |  |
| [`edge`](#nodebpy.builder.socket.VectorSocket.edge) | VectorSocket `edge` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`face`](#nodebpy.builder.socket.VectorSocket.face) | VectorSocket `face` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`i`](#nodebpy.builder.socket.VectorSocket.i) |  |
| [`instance`](#nodebpy.builder.socket.VectorSocket.instance) | VectorSocket `instance` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`layer`](#nodebpy.builder.socket.VectorSocket.layer) | VectorSocket `layer` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`links`](#nodebpy.builder.socket.VectorSocket.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocket.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocket.node) |  |
| [`o`](#nodebpy.builder.socket.VectorSocket.o) |  |
| [`point`](#nodebpy.builder.socket.VectorSocket.point) | VectorSocket `point` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`socket`](#nodebpy.builder.socket.VectorSocket.socket) |  |
| [`spline`](#nodebpy.builder.socket.VectorSocket.spline) | VectorSocket `spline` domain-bound methods from `EvaluateAtIndex`, `EvaluateOnDomain`, `AccumulateField`, `FieldMinAndMax`, `FieldAverage`, `FieldVariance`. |
| [`tree`](#nodebpy.builder.socket.VectorSocket.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocket.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocket.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocket.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocket.z) |  |

#### Methods

| Name | Description |
|----|----|
| [align_rotation](#nodebpy.builder.socket.VectorSocket.align_rotation) | Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input. |
| [cross](#nodebpy.builder.socket.VectorSocket.cross) |  |
| [distance](#nodebpy.builder.socket.VectorSocket.distance) | Euclidean distance between this vector and *other*, as a `FloatSocket`. |
| [dot](#nodebpy.builder.socket.VectorSocket.dot) | Dot product with another vector and return the result as a `FloatSocket`. |
| [enable_output](#nodebpy.builder.socket.VectorSocket.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [length](#nodebpy.builder.socket.VectorSocket.length) | Get the length of this vector as a `FloatSocket` |
| [map_range](#nodebpy.builder.socket.VectorSocket.map_range) |  |
| [normalize](#nodebpy.builder.socket.VectorSocket.normalize) |  |
| [project](#nodebpy.builder.socket.VectorSocket.project) |  |
| [reflect](#nodebpy.builder.socket.VectorSocket.reflect) |  |
| [rotate](#nodebpy.builder.socket.VectorSocket.rotate) |  |
| [scale](#nodebpy.builder.socket.VectorSocket.scale) |  |
| [to_list](#nodebpy.builder.socket.VectorSocket.to_list) | Create a list of elements, evaluating this field `count` times based on the `Index` node. |
| [transform](#nodebpy.builder.socket.VectorSocket.transform) |  |

##### align_rotation

``` python
align_rotation(rotation=None, factor=1.0, *, axis='Z', pivot_axis='AUTO')
```

Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input.

##### cross

``` python
cross(other)
```

##### distance

``` python
distance(other=(0.0, 0.0, 0.0))
```

Euclidean distance between this vector and *other*, as a `FloatSocket`.

##### dot

``` python
dot(vector=(0.0, 0.0, 1.0))
```

Dot product with another vector and return the result as a `FloatSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### length

``` python
length()
```

Get the length of this vector as a `FloatSocket`

##### map_range

``` python
map_range(*args, **kwargs)
```

##### normalize

``` python
normalize()
```

##### project

``` python
project(other)
```

##### reflect

``` python
reflect(normal)
```

##### rotate

``` python
rotate(rotation)
```

##### scale

``` python
scale(scale)
```

##### to_list

``` python
to_list(count=10)
```

Create a list of elements, evaluating this field `count` times based on the `Index` node.

##### transform

``` python
transform(matrix)
```

### VectorSocketGrid

``` python
VectorSocketGrid(socket)
```

Runtime vector grid socket wrapper.

#### Attributes

| Name | Description |
|----|----|
| [`background_value`](#nodebpy.builder.socket.VectorSocketGrid.background_value) |  |
| [`builder_node`](#nodebpy.builder.socket.VectorSocketGrid.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.VectorSocketGrid.i) |  |
| [`links`](#nodebpy.builder.socket.VectorSocketGrid.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocketGrid.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocketGrid.node) |  |
| [`o`](#nodebpy.builder.socket.VectorSocketGrid.o) |  |
| [`socket`](#nodebpy.builder.socket.VectorSocketGrid.socket) |  |
| [`tree`](#nodebpy.builder.socket.VectorSocketGrid.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocketGrid.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocketGrid.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocketGrid.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocketGrid.z) |  |

#### Methods

| Name | Description |
|----|----|
| [align_rotation](#nodebpy.builder.socket.VectorSocketGrid.align_rotation) | Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input. |
| [clip](#nodebpy.builder.socket.VectorSocketGrid.clip) | Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value. |
| [cross](#nodebpy.builder.socket.VectorSocketGrid.cross) |  |
| [curl](#nodebpy.builder.socket.VectorSocketGrid.curl) | Calculate the magnitude and direction of circulation of a directional vector grid. |
| [dilate_erode](#nodebpy.builder.socket.VectorSocketGrid.dilate_erode) | Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values. |
| [distance](#nodebpy.builder.socket.VectorSocketGrid.distance) | Euclidean distance between this vector and *other*, as a `FloatSocket`. |
| [divergence](#nodebpy.builder.socket.VectorSocketGrid.divergence) | Calculate the flow into and out of each point of a directional vector grid. |
| [dot](#nodebpy.builder.socket.VectorSocketGrid.dot) | Dot product with another vector and return the result as a `FloatSocket`. |
| [enable_output](#nodebpy.builder.socket.VectorSocketGrid.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [field_to_grid](#nodebpy.builder.socket.VectorSocketGrid.field_to_grid) | Create new grids by evaluating new values on an existing volume grid topology. |
| [length](#nodebpy.builder.socket.VectorSocketGrid.length) | Get the length of this vector as a `FloatSocket` |
| [map_range](#nodebpy.builder.socket.VectorSocketGrid.map_range) |  |
| [mean](#nodebpy.builder.socket.VectorSocketGrid.mean) | Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [median](#nodebpy.builder.socket.VectorSocketGrid.median) | Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [normalize](#nodebpy.builder.socket.VectorSocketGrid.normalize) |  |
| [project](#nodebpy.builder.socket.VectorSocketGrid.project) |  |
| [prune](#nodebpy.builder.socket.VectorSocketGrid.prune) | Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes. |
| [reflect](#nodebpy.builder.socket.VectorSocketGrid.reflect) |  |
| [rotate](#nodebpy.builder.socket.VectorSocketGrid.rotate) |  |
| [sample](#nodebpy.builder.socket.VectorSocketGrid.sample) | Retrieve values from the specified volume grid. |
| [sample_index](#nodebpy.builder.socket.VectorSocketGrid.sample_index) | Retrieve volume grid values at specific voxels. |
| [scale](#nodebpy.builder.socket.VectorSocketGrid.scale) |  |
| [to_points](#nodebpy.builder.socket.VectorSocketGrid.to_points) | Generate a point cloud from a volume grid’s active voxels. |
| [transform](#nodebpy.builder.socket.VectorSocketGrid.transform) |  |
| [voxelize](#nodebpy.builder.socket.VectorSocketGrid.voxelize) | Remove sparseness from a volume grid by making the active tiles into voxels. |

##### align_rotation

``` python
align_rotation(rotation=None, factor=1.0, *, axis='Z', pivot_axis='AUTO')
```

Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input.

##### clip

``` python
clip(min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value.

##### cross

``` python
cross(other)
```

##### curl

``` python
curl()
```

Calculate the magnitude and direction of circulation of a directional vector grid.

##### dilate_erode

``` python
dilate_erode(steps=1, connectivity='Face', tiles='Preserve')
```

Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values.

##### distance

``` python
distance(other=(0.0, 0.0, 0.0))
```

Euclidean distance between this vector and *other*, as a `FloatSocket`.

##### divergence

``` python
divergence()
```

Calculate the flow into and out of each point of a directional vector grid.

##### dot

``` python
dot(vector=(0.0, 0.0, 1.0))
```

Dot product with another vector and return the result as a `FloatSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### field_to_grid

``` python
field_to_grid()
```

Create new grids by evaluating new values on an existing volume grid topology.

##### length

``` python
length()
```

Get the length of this vector as a `FloatSocket`

##### map_range

``` python
map_range(*args, **kwargs)
```

##### mean

``` python
mean(width=1, iterations=1)
```

Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

##### median

``` python
median(width=1, iterations=1)
```

Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

##### normalize

``` python
normalize()
```

##### project

``` python
project(other)
```

##### prune

``` python
prune(threshold=0.1, mode=None)
```

Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes.

##### reflect

``` python
reflect(normal)
```

##### rotate

``` python
rotate(rotation)
```

##### sample

``` python
sample(position=None, interpolation='Trilinear')
```

Retrieve values from the specified volume grid.

##### sample_index

``` python
sample_index(x=0, y=0, z=0)
```

Retrieve volume grid values at specific voxels.

##### scale

``` python
scale(scale)
```

##### to_points

``` python
to_points()
```

Generate a point cloud from a volume grid’s active voxels.

##### transform

``` python
transform(matrix)
```

##### voxelize

``` python
voxelize()
```

Remove sparseness from a volume grid by making the active tiles into voxels.

### VectorSocketList

``` python
VectorSocketList(socket)
```

#### Attributes

| Name | Description |
|----|----|
| [`builder_node`](#nodebpy.builder.socket.VectorSocketList.builder_node) | The builder node that owns this socket, if accessed via .o/.i. |
| [`i`](#nodebpy.builder.socket.VectorSocketList.i) |  |
| [`links`](#nodebpy.builder.socket.VectorSocketList.links) |  |
| [`name`](#nodebpy.builder.socket.VectorSocketList.name) |  |
| [`node`](#nodebpy.builder.socket.VectorSocketList.node) |  |
| [`o`](#nodebpy.builder.socket.VectorSocketList.o) |  |
| [`socket`](#nodebpy.builder.socket.VectorSocketList.socket) |  |
| [`tree`](#nodebpy.builder.socket.VectorSocketList.tree) |  |
| [`type`](#nodebpy.builder.socket.VectorSocketList.type) |  |
| [`x`](#nodebpy.builder.socket.VectorSocketList.x) |  |
| [`y`](#nodebpy.builder.socket.VectorSocketList.y) |  |
| [`z`](#nodebpy.builder.socket.VectorSocketList.z) |  |

#### Methods

| Name | Description |
|----|----|
| [align_rotation](#nodebpy.builder.socket.VectorSocketList.align_rotation) | Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input. |
| [cross](#nodebpy.builder.socket.VectorSocketList.cross) |  |
| [distance](#nodebpy.builder.socket.VectorSocketList.distance) | Euclidean distance between this vector and *other*, as a `FloatSocket`. |
| [dot](#nodebpy.builder.socket.VectorSocketList.dot) | Dot product with another vector and return the result as a `FloatSocket`. |
| [enable_output](#nodebpy.builder.socket.VectorSocketList.enable_output) | Enable or disable the the output of this node group that is connected to this socket. |
| [filter](#nodebpy.builder.socket.VectorSocketList.filter) | Filter the list based on the selection. |
| [get](#nodebpy.builder.socket.VectorSocketList.get) | Get the item at the given index from the list. |
| [length](#nodebpy.builder.socket.VectorSocketList.length) | Get the length of this vector as a `FloatSocket` |
| [list_length](#nodebpy.builder.socket.VectorSocketList.list_length) | Get the length of the list. |
| [list_slice](#nodebpy.builder.socket.VectorSocketList.list_slice) | Slice the list using start, stop, and step indices. Behaves like Python’s slice notation. |
| [map_range](#nodebpy.builder.socket.VectorSocketList.map_range) |  |
| [normalize](#nodebpy.builder.socket.VectorSocketList.normalize) |  |
| [project](#nodebpy.builder.socket.VectorSocketList.project) |  |
| [reflect](#nodebpy.builder.socket.VectorSocketList.reflect) |  |
| [reverse](#nodebpy.builder.socket.VectorSocketList.reverse) | Reverse the list. Currently uses a SortList node with negative Index to reverse the list. |
| [rotate](#nodebpy.builder.socket.VectorSocketList.rotate) |  |
| [scale](#nodebpy.builder.socket.VectorSocketList.scale) |  |
| [sort](#nodebpy.builder.socket.VectorSocketList.sort) | Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided. |
| [transform](#nodebpy.builder.socket.VectorSocketList.transform) |  |

##### align_rotation

``` python
align_rotation(rotation=None, factor=1.0, *, axis='Z', pivot_axis='AUTO')
```

Orient the given rotation along the current vector. Uses `AlignRotationToVector` with this socket as the vector input.

##### cross

``` python
cross(other)
```

##### distance

``` python
distance(other=(0.0, 0.0, 0.0))
```

Euclidean distance between this vector and *other*, as a `FloatSocket`.

##### dot

``` python
dot(vector=(0.0, 0.0, 1.0))
```

Dot product with another vector and return the result as a `FloatSocket`.

##### enable_output

``` python
enable_output(enable=True)
```

Enable or disable the the output of this node group that is connected to this socket.

If called on an output socket, the output of the EnableOutput node is returned. If called on an input socket, the input socket is returned.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| enable | InputBoolean | Whether to enable or disable the output, by default True. | `True` |

###### Returns

| Name | Type | Description                                                      |
|------|------|------------------------------------------------------------------|
|      | Self | The output socket or input socket, depending on the socket type. |

##### filter

``` python
filter(selection=True)
```

Filter the list based on the selection.

##### get

``` python
get(index)
```

Get the item at the given index from the list.

##### length

``` python
length()
```

Get the length of this vector as a `FloatSocket`

##### list_length

``` python
list_length()
```

Get the length of the list.

##### list_slice

``` python
list_slice(start=0, stop=None, step=1)
```

Slice the list using start, stop, and step indices. Behaves like Python’s slice notation.

##### map_range

``` python
map_range(*args, **kwargs)
```

##### normalize

``` python
normalize()
```

##### project

``` python
project(other)
```

##### reflect

``` python
reflect(normal)
```

##### reverse

``` python
reverse()
```

Reverse the list. Currently uses a SortList node with negative Index to reverse the list.

##### rotate

``` python
rotate(rotation)
```

##### scale

``` python
scale(scale)
```

##### sort

``` python
sort(sort_weight, group_id=None, selection=None)
```

Sort the list based on the weights. Optional `Group ID` and `Selection` can be provided.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| sort_weight | InputFloat \| InputFloatList | The weight to sort by. | *required* |
| group_id | InputInteger \| IntegerSocket | The group ID to sort within. Groups are sorted independently and groups returned in order of Group ID. | `None` |
| selection | InputBoolean \| BooleanSocketList | The selection to sort by. If False then an element is not included in the sort and remains in its original position. | `None` |

###### Returns

| Name | Type | Description      |
|------|------|------------------|
|      | Self | The sorted list. |

##### transform

``` python
transform(matrix)
```
