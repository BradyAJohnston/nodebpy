# nodes.geometry.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [AttributeStatistic](#nodebpy.nodes.geometry.manual.AttributeStatistic) | Calculate statistics about a data set from a field evaluated on a geometry |
| [CaptureAttribute](#nodebpy.nodes.geometry.manual.CaptureAttribute) | Store the result of a field on a geometry and output the data as a node socket. |
| [ColorRamp](#nodebpy.nodes.geometry.manual.ColorRamp) | Map values to colors with the use of a gradient |
| [Compare](#nodebpy.nodes.geometry.manual.Compare) | Perform a comparison operation on the two given inputs |
| [EvaluateClosure](#nodebpy.nodes.geometry.manual.EvaluateClosure) | Execute a given closure |
| [FieldToGrid](#nodebpy.nodes.geometry.manual.FieldToGrid) | Create new grids by evaluating new values on an existing volume grid topology |
| [Float](#nodebpy.nodes.geometry.manual.Float) | Input numerical values to other nodes in the tree. A ‘type-hinted’ wrapper of the Value node. |
| [FloatCurve](#nodebpy.nodes.geometry.manual.FloatCurve) | Map an input float to a curve and outputs a float value |
| [Frame](#nodebpy.nodes.geometry.manual.Frame) |  |
| [GeometryToInstance](#nodebpy.nodes.geometry.manual.GeometryToInstance) | Convert each input geometry into an instance, which can be much faster |
| [IndexSwitch](#nodebpy.nodes.geometry.manual.IndexSwitch) | Node builder for the Index Switch node |
| [JoinGeometry](#nodebpy.nodes.geometry.manual.JoinGeometry) | Merge separately generated geometries into a single one |
| [JoinStrings](#nodebpy.nodes.geometry.manual.JoinStrings) | Combine any number of input strings |
| [MenuSwitch](#nodebpy.nodes.geometry.manual.MenuSwitch) | Node builder for the Menu Switch node |
| [MeshBoolean](#nodebpy.nodes.geometry.manual.MeshBoolean) | Cut, subtract, or join multiple mesh inputs |
| [SDFGridBoolean](#nodebpy.nodes.geometry.manual.SDFGridBoolean) | Cut, subtract, or join multiple SDF volume grid inputs |
| [StoreNamedAttribute](#nodebpy.nodes.geometry.manual.StoreNamedAttribute) | Store the result of a field on a geometry as an attribute with the specified name |
| [Value](#nodebpy.nodes.geometry.manual.Value) | Input numerical values to other nodes in the tree |

### AttributeStatistic

``` python
AttributeStatistic(
    geometry=None,
    selection=True,
    attribute=None,
    *,
    data_type='FLOAT',
    domain='POINT',
    **kwargs,
)
```

Calculate statistics about a data set from a field evaluated on a geometry

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.AttributeStatistic.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.AttributeStatistic.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.AttributeStatistic.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.AttributeStatistic.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.AttributeStatistic.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.AttributeStatistic.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.AttributeStatistic.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.AttributeStatistic.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.AttributeStatistic.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.AttributeStatistic.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.AttributeStatistic.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.AttributeStatistic.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.AttributeStatistic.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.AttributeStatistic.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.AttributeStatistic.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

### CaptureAttribute

``` python
CaptureAttribute(geometry=None, selection=True, items=None, *, domain='POINT')
```

Store the result of a field on a geometry and output the data as a node socket. Allows remembering or interpolating data as the geometry changes, such as positions before deformation

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.CaptureAttribute.corner) |  |
| [`curve`](#nodebpy.nodes.geometry.manual.CaptureAttribute.curve) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.CaptureAttribute.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.CaptureAttribute.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.CaptureAttribute.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.CaptureAttribute.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.CaptureAttribute.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.CaptureAttribute.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.CaptureAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.CaptureAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.CaptureAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.CaptureAttribute.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.CaptureAttribute.point) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.CaptureAttribute.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.CaptureAttribute.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.manual.CaptureAttribute.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.manual.CaptureAttribute.capture) | Add an item linked from `value` and return its output socket. |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Add a single item and return its handle.

`value` may be a linkable (linked to the item’s input) or a plain default value; otherwise `type` (a socket-type string such as `"FLOAT"`) declares the item unlinked.

##### add_items

``` python
add_items(items)
```

Add an item per mapping entry and return their handles by name.

Values may be linkables (linked to the new item’s input) or socket-type strings such as `"FLOAT"` (declare an unlinked item).

##### capture

``` python
capture(value, *, name=None)
```

Add an item linked from `value` and return its output socket.

The item is auto-named after the source socket unless `name` is given.

### ColorRamp

``` python
ColorRamp(
    fac=0.5,
    *,
    items=(),
    color_interpolation='EASE',
    hue_interpolation='NEAR',
    mode='RGB',
)
```

Map values to colors with the use of a gradient

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| fac | InputFloat | Factor: Which is used to sample the ColorRamp for the output color. | `0.5` |
| items | Iterable\[tuple\[float, tuple\[float, float, float float\]\]\] | Iterable of items which contain (position, color) which position being a 4-component float for values RGBA. Position is a value betwen `0..1`. | `()` |

#### Attributes

| Name | Description |
|----|----|
| [`color_interpolation`](#nodebpy.nodes.geometry.manual.ColorRamp.color_interpolation) |  |
| [`elements`](#nodebpy.nodes.geometry.manual.ColorRamp.elements) |  |
| [`hue_interpolation`](#nodebpy.nodes.geometry.manual.ColorRamp.hue_interpolation) |  |
| [`i`](#nodebpy.nodes.geometry.manual.ColorRamp.i) |  |
| [`mode`](#nodebpy.nodes.geometry.manual.ColorRamp.mode) |  |
| [`name`](#nodebpy.nodes.geometry.manual.ColorRamp.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.ColorRamp.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.ColorRamp.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.ColorRamp.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.ColorRamp.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute | Type | Description |
|----|----|----|
| `i.fac` | `FloatSocket` | Factor: The input value between `0..1` which maps to the final color value. |

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `o.color` | `ColorSocket` | Color: The mapped color value based in the input `fac`. |
| `o.alpha` | `FloatSocket` | Alpha: The mapped alpha of the color based on the input `fac`. |

### Compare

``` python
Compare(operation='GREATER_THAN', data_type='FLOAT', **kwargs)
```

Perform a comparison operation on the two given inputs

#### Attributes

| Name | Description |
|----|----|
| [`color`](#nodebpy.nodes.geometry.manual.Compare.color) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.Compare.data_type) |  |
| [`float`](#nodebpy.nodes.geometry.manual.Compare.float) |  |
| [`i`](#nodebpy.nodes.geometry.manual.Compare.i) |  |
| [`integer`](#nodebpy.nodes.geometry.manual.Compare.integer) |  |
| [`mode`](#nodebpy.nodes.geometry.manual.Compare.mode) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Compare.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Compare.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Compare.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.Compare.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Compare.outputs) |  |
| [`string`](#nodebpy.nodes.geometry.manual.Compare.string) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Compare.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`vector`](#nodebpy.nodes.geometry.manual.Compare.vector) |  |

### EvaluateClosure

``` python
EvaluateClosure(
    closure=None,
    input_items=None,
    output_items=None,
    *,
    active_input_index=0,
    active_output_index=0,
    define_signature=False,
)
```

Execute a given closure

#### Parameters

| Name    | Type         | Description | Default |
|---------|--------------|-------------|---------|
| closure | InputClosure | Closure     | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`active_input_index`](#nodebpy.nodes.geometry.manual.EvaluateClosure.active_input_index) |  |
| [`active_output_index`](#nodebpy.nodes.geometry.manual.EvaluateClosure.active_output_index) |  |
| [`define_signature`](#nodebpy.nodes.geometry.manual.EvaluateClosure.define_signature) |  |
| [`i`](#nodebpy.nodes.geometry.manual.EvaluateClosure.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.EvaluateClosure.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.EvaluateClosure.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.EvaluateClosure.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.EvaluateClosure.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.EvaluateClosure.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [sync_signature](#nodebpy.nodes.geometry.manual.EvaluateClosure.sync_signature) |  |

##### sync_signature

``` python
sync_signature(node)
```

**Inputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `i.closure` | `ClosureSocket` | Closure     |

### FieldToGrid

``` python
FieldToGrid(topology=None, items=None, *, data_type='FLOAT')
```

Create new grids by evaluating new values on an existing volume grid topology

Data types are inferred automatically from the closest compatible data type.

#### Inputs:

topology: InputLinkable The grid which contains the topology to evaluate the different fields on. items: dict\[str, InputAny\] The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket. data_type: \_GridDataTypes = “FLOAT” The data type of the grid to evaluate on. Possible values are “FLOAT”, “INT”, “VECTOR”, “BOOLEAN”.

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.manual.FieldToGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.manual.FieldToGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FieldToGrid.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.FieldToGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldToGrid.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.FieldToGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldToGrid.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.FieldToGrid.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.manual.FieldToGrid.add_items) | Add an item per mapping entry and return their handles by name. |
| [boolean](#nodebpy.nodes.geometry.manual.FieldToGrid.boolean) | Data type for the topology grid |
| [capture](#nodebpy.nodes.geometry.manual.FieldToGrid.capture) | Add an item linked from `value` and return its output socket. |
| [capture_boolean](#nodebpy.nodes.geometry.manual.FieldToGrid.capture_boolean) |  |
| [capture_float](#nodebpy.nodes.geometry.manual.FieldToGrid.capture_float) |  |
| [capture_integer](#nodebpy.nodes.geometry.manual.FieldToGrid.capture_integer) |  |
| [capture_vector](#nodebpy.nodes.geometry.manual.FieldToGrid.capture_vector) |  |
| [float](#nodebpy.nodes.geometry.manual.FieldToGrid.float) | Data type for the topology grid |
| [integer](#nodebpy.nodes.geometry.manual.FieldToGrid.integer) | Data type for the topology grid |
| [vector](#nodebpy.nodes.geometry.manual.FieldToGrid.vector) | Data type for the topology grid |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Add a single item and return its handle.

`value` may be a linkable (linked to the item’s input) or a plain default value; otherwise `type` (a socket-type string such as `"FLOAT"`) declares the item unlinked.

##### add_items

``` python
add_items(items)
```

Add an item per mapping entry and return their handles by name.

Values may be linkables (linked to the new item’s input) or socket-type strings such as `"FLOAT"` (declare an unlinked item).

##### boolean

``` python
boolean(topology=None, items=None)
```

Data type for the topology grid

##### capture

``` python
capture(value, *, name=None)
```

Add an item linked from `value` and return its output socket.

The item is auto-named after the source socket unless `name` is given.

##### capture_boolean

``` python
capture_boolean(field=None, name=None)
```

##### capture_float

``` python
capture_float(field=None, name=None)
```

##### capture_integer

``` python
capture_integer(field=None, name=None)
```

##### capture_vector

``` python
capture_vector(field=None, name=None)
```

##### float

``` python
float(topology=None, items=None)
```

Data type for the topology grid

##### integer

``` python
integer(topology=None, items=None)
```

Data type for the topology grid

##### vector

``` python
vector(topology=None, items=None)
```

Data type for the topology grid

### Float

``` python
Float(value=0.0)
```

Input numerical values to other nodes in the tree. A ‘type-hinted’ wrapper of the Value node.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Float.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.manual.Float.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Float.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Float.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Float.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Float.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`value`](#nodebpy.nodes.geometry.manual.Float.value) | Input socket: Value |

### FloatCurve

``` python
FloatCurve(factor=1.0, value=1.0, *, items=())
```

Map an input float to a curve and outputs a float value

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| factor | InputFloat | Factor | `1.0` |
| value | InputFloat | Value | `1.0` |
| items | Iterable\[tuple\[float, float\] \| tuple\[float, float, Literal\['AUTO', 'AUTO_CLAMPED', 'VECTOR'\]\]\] | An iterable which contains items `(x, y, Optional[handle_type])`. The position values are between `0..1` and map the input `value` to the output `value` from the resulting curve interpolation. | `()` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.FloatCurve.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FloatCurve.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.FloatCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FloatCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FloatCurve.outputs) |  |
| [`points`](#nodebpy.nodes.geometry.manual.FloatCurve.points) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FloatCurve.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `i.factor` | `FloatSocket` | Factor      |
| `i.value`  | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### Frame

``` python
Frame(label=None, shrink=True, text=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Frame.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`label`](#nodebpy.nodes.geometry.manual.Frame.label) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Frame.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Frame.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Frame.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.Frame.outputs) |  |
| [`shrink`](#nodebpy.nodes.geometry.manual.Frame.shrink) |  |
| [`text`](#nodebpy.nodes.geometry.manual.Frame.text) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Frame.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

### GeometryToInstance

``` python
GeometryToInstance(*args)
```

Convert each input geometry into an instance, which can be much faster than the Join Geometry node when the inputs are large

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.GeometryToInstance.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.GeometryToInstance.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.GeometryToInstance.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.GeometryToInstance.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.GeometryToInstance.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.GeometryToInstance.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute | Type | Description |
|----|----|----|
| `geometry` | `GeometrySocket` | Multi-input socket; geometry that will be converted into an instance |

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `instances` | `GeometrySocket` | Single geometry output with each input linked geometry as a separate instance |

### IndexSwitch

``` python
IndexSwitch(index=0, items=(), data_type='FLOAT')
```

Node builder for the Index Switch node

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.manual.IndexSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.geometry.manual.IndexSwitch.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.IndexSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.IndexSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.IndexSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.IndexSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.IndexSwitch.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.manual.IndexSwitch.add_items) | Add an item per mapping entry and return their handles by name. |
| [boolean](#nodebpy.nodes.geometry.manual.IndexSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.IndexSwitch.bundle) |  |
| [capture](#nodebpy.nodes.geometry.manual.IndexSwitch.capture) | Add an item linked from `value` and return its output socket. |
| [closure](#nodebpy.nodes.geometry.manual.IndexSwitch.closure) |  |
| [collection](#nodebpy.nodes.geometry.manual.IndexSwitch.collection) |  |
| [color](#nodebpy.nodes.geometry.manual.IndexSwitch.color) |  |
| [float](#nodebpy.nodes.geometry.manual.IndexSwitch.float) |  |
| [geometry](#nodebpy.nodes.geometry.manual.IndexSwitch.geometry) |  |
| [image](#nodebpy.nodes.geometry.manual.IndexSwitch.image) |  |
| [integer](#nodebpy.nodes.geometry.manual.IndexSwitch.integer) |  |
| [material](#nodebpy.nodes.geometry.manual.IndexSwitch.material) |  |
| [matrix](#nodebpy.nodes.geometry.manual.IndexSwitch.matrix) |  |
| [menu](#nodebpy.nodes.geometry.manual.IndexSwitch.menu) |  |
| [object](#nodebpy.nodes.geometry.manual.IndexSwitch.object) |  |
| [rotation](#nodebpy.nodes.geometry.manual.IndexSwitch.rotation) |  |
| [string](#nodebpy.nodes.geometry.manual.IndexSwitch.string) |  |
| [vector](#nodebpy.nodes.geometry.manual.IndexSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Add a single item and return its handle.

`value` may be a linkable (linked to the item’s input) or a plain default value; otherwise `type` (a socket-type string such as `"FLOAT"`) declares the item unlinked.

##### add_items

``` python
add_items(items)
```

Add an item per mapping entry and return their handles by name.

Values may be linkables (linked to the new item’s input) or socket-type strings such as `"FLOAT"` (declare an unlinked item).

##### boolean

``` python
boolean(index=0, items=())
```

##### bundle

``` python
bundle(index=0, items=())
```

##### capture

``` python
capture(value, *, name=None)
```

Add an item linked from `value` and return its output socket.

The item is auto-named after the source socket unless `name` is given.

##### closure

``` python
closure(index=0, items=())
```

##### collection

``` python
collection(index=0, items=())
```

##### color

``` python
color(index=0, items=())
```

##### float

``` python
float(index=0, items=())
```

##### geometry

``` python
geometry(index=0, items=())
```

##### image

``` python
image(index=0, items=())
```

##### integer

``` python
integer(index=0, items=())
```

##### material

``` python
material(index=0, items=())
```

##### matrix

``` python
matrix(index=0, items=())
```

##### menu

``` python
menu(index=0, items=())
```

##### object

``` python
object(index=0, items=())
```

##### rotation

``` python
rotation(index=0, items=())
```

##### string

``` python
string(index=0, items=())
```

##### vector

``` python
vector(index=0, items=())
```

### JoinGeometry

``` python
JoinGeometry(geometry=())
```

Merge separately generated geometries into a single one

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.JoinGeometry.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.JoinGeometry.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.JoinGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinGeometry.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

### JoinStrings

``` python
JoinStrings(strings=(), delimiter='')
```

Combine any number of input strings

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.JoinStrings.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.JoinStrings.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.JoinStrings.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinStrings.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinStrings.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinStrings.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

### MenuSwitch

``` python
MenuSwitch(menu=None, items=None, *, data_type='FLOAT')
```

Node builder for the Menu Switch node

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.geometry.manual.MenuSwitch.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.MenuSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MenuSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.MenuSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MenuSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.MenuSwitch.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.manual.MenuSwitch.add_items) | Add an item per mapping entry and return their handles by name. |
| [boolean](#nodebpy.nodes.geometry.manual.MenuSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.MenuSwitch.bundle) |  |
| [capture](#nodebpy.nodes.geometry.manual.MenuSwitch.capture) | Add an item linked from `value` and return its output socket. |
| [closure](#nodebpy.nodes.geometry.manual.MenuSwitch.closure) |  |
| [collection](#nodebpy.nodes.geometry.manual.MenuSwitch.collection) |  |
| [color](#nodebpy.nodes.geometry.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.geometry.manual.MenuSwitch.float) |  |
| [geometry](#nodebpy.nodes.geometry.manual.MenuSwitch.geometry) |  |
| [image](#nodebpy.nodes.geometry.manual.MenuSwitch.image) |  |
| [integer](#nodebpy.nodes.geometry.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.geometry.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [material](#nodebpy.nodes.geometry.manual.MenuSwitch.material) |  |
| [matrix](#nodebpy.nodes.geometry.manual.MenuSwitch.matrix) |  |
| [menu](#nodebpy.nodes.geometry.manual.MenuSwitch.menu) |  |
| [object](#nodebpy.nodes.geometry.manual.MenuSwitch.object) |  |
| [rotation](#nodebpy.nodes.geometry.manual.MenuSwitch.rotation) |  |
| [string](#nodebpy.nodes.geometry.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.geometry.manual.MenuSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Add a single item and return its handle.

`value` may be a linkable (linked to the item’s input) or a plain default value; otherwise `type` (a socket-type string such as `"FLOAT"`) declares the item unlinked.

##### add_items

``` python
add_items(items)
```

Add an item per mapping entry and return their handles by name.

Values may be linkables (linked to the new item’s input) or socket-type strings such as `"FLOAT"` (declare an unlinked item).

##### boolean

``` python
boolean(menu=None, items=None)
```

##### bundle

``` python
bundle(menu=None, items=None)
```

##### capture

``` python
capture(value, *, name=None)
```

Add an item linked from `value` and return its output socket.

The item is auto-named after the source socket unless `name` is given.

##### closure

``` python
closure(menu=None, items=None)
```

##### collection

``` python
collection(menu=None, items=None)
```

##### color

``` python
color(menu=None, items=None)
```

##### float

``` python
float(menu=None, items=None)
```

##### geometry

``` python
geometry(menu=None, items=None)
```

##### image

``` python
image(menu=None, items=None)
```

##### integer

``` python
integer(menu=None, items=None)
```

##### is_selected

``` python
is_selected(name)
```

Gets the boolean output socket that is True when the named menu item is selected.

Cannot be used with the “Output” name as this refers to the output socket itself.

###### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| name | str | The name of the menu item to get the selected socket for. | *required* |

###### Returns

| Name | Type | Description |
|----|----|----|
|  | BooleanSocket | The boolean output socket that is True when the named menu item is selected. |

##### material

``` python
material(menu=None, items=None)
```

##### matrix

``` python
matrix(menu=None, items=None)
```

##### menu

``` python
menu(menu=None, items=None)
```

##### object

``` python
object(menu=None, items=None)
```

##### rotation

``` python
rotation(menu=None, items=None)
```

##### string

``` python
string(menu=None, items=None)
```

##### vector

``` python
vector(menu=None, items=None)
```

### MeshBoolean

``` python
MeshBoolean(
    mesh_1=None,
    mesh_2=(),
    *,
    self_intersection=False,
    hole_tolerant=False,
    operation='DIFFERENCE',
    solver='FLOAT',
)
```

Cut, subtract, or join multiple mesh inputs

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.MeshBoolean.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.MeshBoolean.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.MeshBoolean.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MeshBoolean.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.MeshBoolean.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.MeshBoolean.outputs) |  |
| [`solver`](#nodebpy.nodes.geometry.manual.MeshBoolean.solver) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MeshBoolean.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [difference](#nodebpy.nodes.geometry.manual.MeshBoolean.difference) |  |
| [intersect](#nodebpy.nodes.geometry.manual.MeshBoolean.intersect) |  |
| [union](#nodebpy.nodes.geometry.manual.MeshBoolean.union) |  |

##### difference

``` python
difference(
    mesh_1=None,
    items=(),
    self_intersection=False,
    hole_tolerant=False,
    *,
    solver='FLOAT',
)
```

##### intersect

``` python
intersect(
    items=(),
    self_intersection=False,
    hole_tolerant=False,
    *,
    solver='FLOAT',
)
```

##### union

``` python
union(items=(), self_intersection=False, hole_tolerant=False, *, solver='FLOAT')
```

### SDFGridBoolean

``` python
SDFGridBoolean(operation='DIFFERENCE')
```

Cut, subtract, or join multiple SDF volume grid inputs

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [difference](#nodebpy.nodes.geometry.manual.SDFGridBoolean.difference) | Create SDF Grid Boolean with operation ‘Difference’. |
| [intersect](#nodebpy.nodes.geometry.manual.SDFGridBoolean.intersect) |  |
| [union](#nodebpy.nodes.geometry.manual.SDFGridBoolean.union) |  |

##### difference

``` python
difference(grid_1=None, grids=())
```

Create SDF Grid Boolean with operation ‘Difference’.

##### intersect

``` python
intersect(grids=())
```

##### union

``` python
union(grids=())
```

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
| [`corner`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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

### Value

``` python
Value(value=0.0)
```

Input numerical values to other nodes in the tree

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Value.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.manual.Value.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Value.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Value.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Value.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Value.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`value`](#nodebpy.nodes.geometry.manual.Value.value) | Input socket: Value |
