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
| [Frame](#nodebpy.nodes.geometry.manual.Frame) | Frame for visually grouping nodes in the editor. |
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
| [`items`](#nodebpy.nodes.geometry.manual.CaptureAttribute.items) | The captured items: `input` is the field, `output` the |
| [`layer`](#nodebpy.nodes.geometry.manual.CaptureAttribute.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.CaptureAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.CaptureAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.CaptureAttribute.o) |  |
| [`point`](#nodebpy.nodes.geometry.manual.CaptureAttribute.point) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.CaptureAttribute.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.CaptureAttribute.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.geometry.manual.CaptureAttribute.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [capture](#nodebpy.nodes.geometry.manual.CaptureAttribute.capture) | Deprecated: use `items.new(value, name).output`. |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

### ColorRamp

``` python
ColorRamp(
    fac=0.5,
    *,
    items=_COLOR_RAMP_DEFAULT_ITEMS,
    color_interpolation='LINEAR',
    hue_interpolation='NEAR',
    mode='RGB',
)
```

Map values to colors with the use of a gradient

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| fac | InputFloat | Factor: Which is used to sample the ColorRamp for the output color. | `0.5` |
| items | Iterable\[tuple\[float, tuple\[float, float, float float\]\] \| tuple\[float, float, float, float, float\]\] | Iterable of items which contain (position, color) which position being a 4-component float for values RGBA. Position is a value betwen `0..1`. Items can also be flat `(position, r, g, b, a)`, so an `(N, 5)` numpy array works. Defaults to black at 0.0 and white at 1.0. At least one item is required. | `_COLOR_RAMP_DEFAULT_ITEMS` |

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
| [`collection`](#nodebpy.nodes.geometry.manual.Compare.collection) |  |
| [`color`](#nodebpy.nodes.geometry.manual.Compare.color) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.Compare.data_type) |  |
| [`float`](#nodebpy.nodes.geometry.manual.Compare.float) |  |
| [`font`](#nodebpy.nodes.geometry.manual.Compare.font) |  |
| [`i`](#nodebpy.nodes.geometry.manual.Compare.i) |  |
| [`image`](#nodebpy.nodes.geometry.manual.Compare.image) |  |
| [`integer`](#nodebpy.nodes.geometry.manual.Compare.integer) |  |
| [`material`](#nodebpy.nodes.geometry.manual.Compare.material) |  |
| [`mode`](#nodebpy.nodes.geometry.manual.Compare.mode) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Compare.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Compare.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Compare.o) |  |
| [`object`](#nodebpy.nodes.geometry.manual.Compare.object) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.Compare.operation) |  |
| [`sound`](#nodebpy.nodes.geometry.manual.Compare.sound) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.EvaluateClosure.inputs) | The values fed into the closure. |
| [`items`](#nodebpy.nodes.geometry.manual.EvaluateClosure.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.manual.EvaluateClosure.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.EvaluateClosure.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.EvaluateClosure.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.EvaluateClosure.outputs) | The results read from the closure. |
| [`tree`](#nodebpy.nodes.geometry.manual.EvaluateClosure.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.EvaluateClosure.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.geometry.manual.EvaluateClosure.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [capture](#nodebpy.nodes.geometry.manual.EvaluateClosure.capture) | Deprecated: use `items.new(value, name).output`. |
| [sync_signature](#nodebpy.nodes.geometry.manual.EvaluateClosure.sync_signature) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

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
| [`items`](#nodebpy.nodes.geometry.manual.FieldToGrid.items) | The evaluated items: `input` is the field, `output` the grid. |
| [`name`](#nodebpy.nodes.geometry.manual.FieldToGrid.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.FieldToGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldToGrid.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldToGrid.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.FieldToGrid.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.geometry.manual.FieldToGrid.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.geometry.manual.FieldToGrid.boolean) | Data type for the topology grid |
| [capture](#nodebpy.nodes.geometry.manual.FieldToGrid.capture) | Deprecated: use `items.new(value, name).output`. |
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

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### boolean

``` python
boolean(topology=None, items=None)
```

Data type for the topology grid

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

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
| [`tree`](#nodebpy.nodes.geometry.manual.Float.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`value`](#nodebpy.nodes.geometry.manual.Float.value) | Input socket: Value |

### FloatCurve

``` python
FloatCurve(factor=1.0, value=1.0, *, items=_FLOAT_CURVE_DEFAULT_ITEMS)
```

Map an input float to a curve and outputs a float value

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| factor | InputFloat | Factor | `1.0` |
| value | InputFloat | Value | `1.0` |
| items | Iterable\[tuple\[float, float\] \| tuple\[float, float, Literal\['AUTO', 'AUTO_CLAMPED', 'VECTOR'\]\]\] | An iterable which contains items `(x, y, Optional[handle_type])`. The position values are between `0..1` and map the input `value` to the output `value` from the resulting curve interpolation. Defaults to a straight line from `(0, 0)` to `(1, 1)`. At least two items are required. | `_FLOAT_CURVE_DEFAULT_ITEMS` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.FloatCurve.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FloatCurve.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.FloatCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FloatCurve.o) |  |
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

Frame for visually grouping nodes in the editor.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Frame.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`label`](#nodebpy.nodes.geometry.manual.Frame.label) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Frame.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.Frame.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Frame.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
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
| [`items`](#nodebpy.nodes.geometry.manual.IndexSwitch.items) | The switch’s items, one input socket each. |
| [`name`](#nodebpy.nodes.geometry.manual.IndexSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.IndexSwitch.o) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.IndexSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.IndexSwitch.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.geometry.manual.IndexSwitch.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.geometry.manual.IndexSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.IndexSwitch.bundle) |  |
| [capture](#nodebpy.nodes.geometry.manual.IndexSwitch.capture) | Deprecated: use `items.new(value, name).output`. |
| [closure](#nodebpy.nodes.geometry.manual.IndexSwitch.closure) |  |
| [collection](#nodebpy.nodes.geometry.manual.IndexSwitch.collection) |  |
| [color](#nodebpy.nodes.geometry.manual.IndexSwitch.color) |  |
| [float](#nodebpy.nodes.geometry.manual.IndexSwitch.float) |  |
| [font](#nodebpy.nodes.geometry.manual.IndexSwitch.font) |  |
| [geometry](#nodebpy.nodes.geometry.manual.IndexSwitch.geometry) |  |
| [image](#nodebpy.nodes.geometry.manual.IndexSwitch.image) |  |
| [integer](#nodebpy.nodes.geometry.manual.IndexSwitch.integer) |  |
| [material](#nodebpy.nodes.geometry.manual.IndexSwitch.material) |  |
| [matrix](#nodebpy.nodes.geometry.manual.IndexSwitch.matrix) |  |
| [menu](#nodebpy.nodes.geometry.manual.IndexSwitch.menu) |  |
| [object](#nodebpy.nodes.geometry.manual.IndexSwitch.object) |  |
| [rotation](#nodebpy.nodes.geometry.manual.IndexSwitch.rotation) |  |
| [sound](#nodebpy.nodes.geometry.manual.IndexSwitch.sound) |  |
| [string](#nodebpy.nodes.geometry.manual.IndexSwitch.string) |  |
| [vector](#nodebpy.nodes.geometry.manual.IndexSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

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

Deprecated: use `items.new(value, name).output`.

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

##### font

``` python
font(index=0, items=())
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

##### sound

``` python
sound(index=0, items=())
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
| [`items`](#nodebpy.nodes.geometry.manual.MenuSwitch.items) | The menu’s items, one input socket each. |
| [`name`](#nodebpy.nodes.geometry.manual.MenuSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MenuSwitch.o) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MenuSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.manual.MenuSwitch.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.geometry.manual.MenuSwitch.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.geometry.manual.MenuSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.MenuSwitch.bundle) |  |
| [capture](#nodebpy.nodes.geometry.manual.MenuSwitch.capture) | Deprecated: use `items.new(value, name).output`. |
| [closure](#nodebpy.nodes.geometry.manual.MenuSwitch.closure) |  |
| [collection](#nodebpy.nodes.geometry.manual.MenuSwitch.collection) |  |
| [color](#nodebpy.nodes.geometry.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.geometry.manual.MenuSwitch.float) |  |
| [font](#nodebpy.nodes.geometry.manual.MenuSwitch.font) |  |
| [geometry](#nodebpy.nodes.geometry.manual.MenuSwitch.geometry) |  |
| [image](#nodebpy.nodes.geometry.manual.MenuSwitch.image) |  |
| [integer](#nodebpy.nodes.geometry.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.geometry.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [item](#nodebpy.nodes.geometry.manual.MenuSwitch.item) | Deprecated: use `items.new(value, name, description=)`. |
| [material](#nodebpy.nodes.geometry.manual.MenuSwitch.material) |  |
| [matrix](#nodebpy.nodes.geometry.manual.MenuSwitch.matrix) |  |
| [menu](#nodebpy.nodes.geometry.manual.MenuSwitch.menu) |  |
| [object](#nodebpy.nodes.geometry.manual.MenuSwitch.object) |  |
| [rotation](#nodebpy.nodes.geometry.manual.MenuSwitch.rotation) |  |
| [sound](#nodebpy.nodes.geometry.manual.MenuSwitch.sound) |  |
| [string](#nodebpy.nodes.geometry.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.geometry.manual.MenuSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

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

Deprecated: use `items.new(value, name).output`.

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

##### font

``` python
font(menu=None, items=None)
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

##### item

``` python
item(name, value=None, *, description=None)
```

Deprecated: use `items.new(value, name, description=)`.

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

##### sound

``` python
sound(menu=None, items=None)
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
SDFGridBoolean(grid_1=None, grid_2=(), *, operation='DIFFERENCE')
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
| [`tree`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [difference](#nodebpy.nodes.geometry.manual.SDFGridBoolean.difference) | Create SDF Grid Boolean with operation ‘Difference’. |
| [intersect](#nodebpy.nodes.geometry.manual.SDFGridBoolean.intersect) | Create SDF Grid Boolean with operation ‘Intersect’. |
| [union](#nodebpy.nodes.geometry.manual.SDFGridBoolean.union) | Create SDF Grid Boolean with operation ‘Union’. |

##### difference

``` python
difference(grid_1=None, grids=())
```

Create SDF Grid Boolean with operation ‘Difference’.

##### intersect

``` python
intersect(grids=())
```

Create SDF Grid Boolean with operation ‘Intersect’.

##### union

``` python
union(grids=())
```

Create SDF Grid Boolean with operation ‘Union’.

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
| [`tree`](#nodebpy.nodes.geometry.manual.Value.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`value`](#nodebpy.nodes.geometry.manual.Value.value) | Input socket: Value |
