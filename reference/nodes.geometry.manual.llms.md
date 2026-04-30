# nodes.geometry.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [AccumulateField](#nodebpy.nodes.geometry.manual.AccumulateField) | Add the values of an evaluated field together and output the running total for each element |
| [AttributeStatistic](#nodebpy.nodes.geometry.manual.AttributeStatistic) | Calculate statistics about a data set from a field evaluated on a geometry |
| [Bake](#nodebpy.nodes.geometry.manual.Bake) | Cache the incoming data so that it can be used without recomputation |
| [CaptureAttribute](#nodebpy.nodes.geometry.manual.CaptureAttribute) | Store the result of a field on a geometry and output the data as a node socket. |
| [ColorRamp](#nodebpy.nodes.geometry.manual.ColorRamp) | Map values to colors with the use of a gradient |
| [Compare](#nodebpy.nodes.geometry.manual.Compare) | Perform a comparison operation on the two given inputs |
| [EvaluateAtIndex](#nodebpy.nodes.geometry.manual.EvaluateAtIndex) | Retrieve data of other elements in the context’s geometry |
| [EvaluateClosure](#nodebpy.nodes.geometry.manual.EvaluateClosure) | Execute a given closure |
| [EvaluateOnDomain](#nodebpy.nodes.geometry.manual.EvaluateOnDomain) | Retrieve values from a field on a different domain besides the domain from the context |
| [FieldAverage](#nodebpy.nodes.geometry.manual.FieldAverage) | Calculate the mean and median of a given field |
| [FieldMinAndMax](#nodebpy.nodes.geometry.manual.FieldMinAndMax) | Calculate the minimum and maximum of a given field |
| [FieldToGrid](#nodebpy.nodes.geometry.manual.FieldToGrid) | Create new grids by evaluating new values on an existing volume grid topology |
| [FieldVariance](#nodebpy.nodes.geometry.manual.FieldVariance) | Calculate the standard deviation and variance of a given field |
| [Float](#nodebpy.nodes.geometry.manual.Float) | Input numerical values to other nodes in the tree. A ‘type-hinted’ wrapper of the Value node. |
| [FloatCurve](#nodebpy.nodes.geometry.manual.FloatCurve) | Map an input float to a curve and outputs a float value |
| [FormatString](#nodebpy.nodes.geometry.manual.FormatString) | Insert values into a string using a Python and path template compatible formatting syntax |
| [Frame](#nodebpy.nodes.geometry.manual.Frame) |  |
| [GeometryToInstance](#nodebpy.nodes.geometry.manual.GeometryToInstance) | Convert each input geometry into an instance, which can be much faster |
| [HandleTypeSelection](#nodebpy.nodes.geometry.manual.HandleTypeSelection) | Provide a selection based on the handle types of Bézier control points |
| [IndexSwitch](#nodebpy.nodes.geometry.manual.IndexSwitch) | Node builder for the Index Switch node |
| [JoinGeometry](#nodebpy.nodes.geometry.manual.JoinGeometry) | Merge separately generated geometries into a single one |
| [JoinStrings](#nodebpy.nodes.geometry.manual.JoinStrings) | Combine any number of input strings |
| [MenuSwitch](#nodebpy.nodes.geometry.manual.MenuSwitch) | Node builder for the Menu Switch node |
| [MeshBoolean](#nodebpy.nodes.geometry.manual.MeshBoolean) | Cut, subtract, or join multiple mesh inputs |
| [SDFGridBoolean](#nodebpy.nodes.geometry.manual.SDFGridBoolean) | Cut, subtract, or join multiple SDF volume grid inputs |
| [SetHandleType](#nodebpy.nodes.geometry.manual.SetHandleType) | Set the handle type for the control points of a Bézier curve |
| [StoreNamedAttribute](#nodebpy.nodes.geometry.manual.StoreNamedAttribute) | Store the result of a field on a geometry as an attribute with the specified name |
| [Switch](#nodebpy.nodes.geometry.manual.Switch) | Switch between two inputs |
| [Value](#nodebpy.nodes.geometry.manual.Value) | Input numerical values to other nodes in the tree |

### AccumulateField

``` python
AccumulateField(value=1.0, group_index=0, *, data_type='FLOAT', domain='POINT')
```

Add the values of an evaluated field together and output the running total for each element

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.AccumulateField.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.AccumulateField.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.AccumulateField.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.AccumulateField.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.AccumulateField.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.AccumulateField.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.AccumulateField.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.AccumulateField.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.AccumulateField.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.AccumulateField.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.AccumulateField.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.AccumulateField.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.AccumulateField.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.AccumulateField.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.AccumulateField.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.AccumulateField.type) |  |

#### Classes

| Name | Description |
|----|----|
| [AccumulateFieldDomainFactory](#nodebpy.nodes.geometry.manual.AccumulateField.AccumulateFieldDomainFactory) |  |

##### AccumulateFieldDomainFactory

``` python
AccumulateFieldDomainFactory(domain)
```

###### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.manual.AccumulateField.AccumulateFieldDomainFactory.float) |  |
| [integer](#nodebpy.nodes.geometry.manual.AccumulateField.AccumulateFieldDomainFactory.integer) |  |
| [transform](#nodebpy.nodes.geometry.manual.AccumulateField.AccumulateFieldDomainFactory.transform) |  |
| [vector](#nodebpy.nodes.geometry.manual.AccumulateField.AccumulateFieldDomainFactory.vector) |  |

float

``` python
float(value=None, index=0)
```

integer

``` python
integer(value=None, index=0)
```

transform

``` python
transform(value=None, index=0)
```

vector

``` python
vector(value=None, index=0)
```

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
| [`name`](#nodebpy.nodes.geometry.manual.AttributeStatistic.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.AttributeStatistic.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.AttributeStatistic.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.AttributeStatistic.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.AttributeStatistic.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.AttributeStatistic.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.AttributeStatistic.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.AttributeStatistic.type) |  |

### Bake

``` python
Bake(*args, **kwargs)
```

Cache the incoming data so that it can be used without recomputation

TODO: properly handle Animation / Still bake opations and ability to bake to a file

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Bake.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.manual.Bake.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Bake.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Bake.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.Bake.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Bake.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Bake.type) |  |

### CaptureAttribute

``` python
CaptureAttribute(geometry=None, items={}, *, domain='POINT')
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
| [`name`](#nodebpy.nodes.geometry.manual.CaptureAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.CaptureAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.CaptureAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.CaptureAttribute.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.CaptureAttribute.point) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.CaptureAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.CaptureAttribute.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.manual.CaptureAttribute.capture) | Capture the value to store in the attribute |

##### capture

``` python
capture(value)
```

Capture the value to store in the attribute

Return the SocketLinker for the output socket

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
| [`name`](#nodebpy.nodes.geometry.manual.ColorRamp.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.ColorRamp.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.ColorRamp.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.ColorRamp.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.ColorRamp.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.ColorRamp.type) |  |

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
| [`name`](#nodebpy.nodes.geometry.manual.Compare.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Compare.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Compare.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.Compare.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Compare.outputs) |  |
| [`string`](#nodebpy.nodes.geometry.manual.Compare.string) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Compare.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Compare.type) |  |
| [`vector`](#nodebpy.nodes.geometry.manual.Compare.vector) |  |

#### Methods

| Name                                                    | Description |
|---------------------------------------------------------|-------------|
| [switch](#nodebpy.nodes.geometry.manual.Compare.switch) |             |

##### switch

``` python
switch(false, true)
```

### EvaluateAtIndex

``` python
EvaluateAtIndex(value=None, index=0, *, domain='POINT', data_type='FLOAT')
```

Retrieve data of other elements in the context’s geometry

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.type) |  |

### EvaluateClosure

``` python
EvaluateClosure(
    closure=None,
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
| [`name`](#nodebpy.nodes.geometry.manual.EvaluateClosure.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.EvaluateClosure.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.EvaluateClosure.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.EvaluateClosure.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.EvaluateClosure.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.EvaluateClosure.type) |  |

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

### EvaluateOnDomain

``` python
EvaluateOnDomain(value=None, *, domain='POINT', data_type='FLOAT')
```

Retrieve values from a field on a different domain besides the domain from the context

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.type) |  |

### FieldAverage

``` python
FieldAverage(value=None, group_index=0, *, data_type='FLOAT', domain='POINT')
```

Calculate the mean and median of a given field

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.FieldAverage.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.FieldAverage.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.FieldAverage.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.FieldAverage.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.FieldAverage.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.FieldAverage.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.FieldAverage.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.FieldAverage.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FieldAverage.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FieldAverage.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldAverage.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FieldAverage.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.FieldAverage.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.FieldAverage.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldAverage.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FieldAverage.type) |  |

### FieldMinAndMax

``` python
FieldMinAndMax(value=1.0, group_index=0, *, data_type='FLOAT', domain='POINT')
```

Calculate the minimum and maximum of a given field

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.type) |  |

### FieldToGrid

``` python
FieldToGrid(topology=None, items={}, *, data_type='FLOAT')
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
| [`name`](#nodebpy.nodes.geometry.manual.FieldToGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FieldToGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldToGrid.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.FieldToGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldToGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FieldToGrid.type) |  |

#### Methods

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [boolean](#nodebpy.nodes.geometry.manual.FieldToGrid.boolean) |             |
| [capture](#nodebpy.nodes.geometry.manual.FieldToGrid.capture) |             |
| [float](#nodebpy.nodes.geometry.manual.FieldToGrid.float)     |             |
| [integer](#nodebpy.nodes.geometry.manual.FieldToGrid.integer) |             |
| [vector](#nodebpy.nodes.geometry.manual.FieldToGrid.vector)   |             |

##### boolean

``` python
boolean(topology=None, items={})
```

##### capture

``` python
capture(items)
```

##### float

``` python
float(topology=None, items={})
```

##### integer

``` python
integer(topology=None, items={})
```

##### vector

``` python
vector(topology=None, items={})
```

### FieldVariance

``` python
FieldVariance(
    value=None,
    group_index=None,
    *,
    data_type='FLOAT',
    domain='POINT',
)
```

Calculate the standard deviation and variance of a given field

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.manual.FieldVariance.corner) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.FieldVariance.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.manual.FieldVariance.domain) |  |
| [`edge`](#nodebpy.nodes.geometry.manual.FieldVariance.edge) |  |
| [`face`](#nodebpy.nodes.geometry.manual.FieldVariance.face) |  |
| [`i`](#nodebpy.nodes.geometry.manual.FieldVariance.i) |  |
| [`instance`](#nodebpy.nodes.geometry.manual.FieldVariance.instance) |  |
| [`layer`](#nodebpy.nodes.geometry.manual.FieldVariance.layer) |  |
| [`name`](#nodebpy.nodes.geometry.manual.FieldVariance.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FieldVariance.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FieldVariance.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FieldVariance.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.FieldVariance.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.FieldVariance.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FieldVariance.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FieldVariance.type) |  |

### Float

``` python
Float(value=0.0)
```

Input numerical values to other nodes in the tree. A ‘type-hinted’ wrapper of the Value node.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Float.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.manual.Float.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Float.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Float.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Float.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Float.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Float.type) |  |
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
| [`name`](#nodebpy.nodes.geometry.manual.FloatCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FloatCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FloatCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FloatCurve.outputs) |  |
| [`points`](#nodebpy.nodes.geometry.manual.FloatCurve.points) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FloatCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FloatCurve.type) |  |

**Inputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `i.factor` | `FloatSocket` | Factor      |
| `i.value`  | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### FormatString

``` python
FormatString(format='', items={})
```

Insert values into a string using a Python and path template compatible formatting syntax

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.FormatString.i) |  |
| [`items`](#nodebpy.nodes.geometry.manual.FormatString.items) | Input sockets: |
| [`name`](#nodebpy.nodes.geometry.manual.FormatString.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.FormatString.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.FormatString.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.FormatString.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.FormatString.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.FormatString.type) |  |

### Frame

``` python
Frame(label=None, shrink=True, text=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Frame.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`label`](#nodebpy.nodes.geometry.manual.Frame.label) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Frame.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Frame.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Frame.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.Frame.outputs) |  |
| [`shrink`](#nodebpy.nodes.geometry.manual.Frame.shrink) |  |
| [`text`](#nodebpy.nodes.geometry.manual.Frame.text) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Frame.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Frame.type) |  |

### GeometryToInstance

``` python
GeometryToInstance(*args)
```

Convert each input geometry into an instance, which can be much faster than the Join Geometry node when the inputs are large

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.GeometryToInstance.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.GeometryToInstance.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.GeometryToInstance.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.GeometryToInstance.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.GeometryToInstance.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.GeometryToInstance.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.GeometryToInstance.type) |  |

**Inputs**

| Attribute | Type | Description |
|----|----|----|
| `geometry` | `GeometrySocket` | Multi-input socket; geometry that will be converted into an instance |

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `instances` | `GeometrySocket` | Single geometry output with each input linked geometry as a separate instance |

### HandleTypeSelection

``` python
HandleTypeSelection(handle_type='AUTO', left=True, right=True)
```

Provide a selection based on the handle types of Bézier control points

#### Attributes

| Name | Description |
|----|----|
| [`handle_type`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.handle_type) |  |
| [`i`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`left`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.left) |  |
| [`mode`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.mode) |  |
| [`name`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.outputs) |  |
| [`right`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.right) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.type) |  |

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
| [`name`](#nodebpy.nodes.geometry.manual.IndexSwitch.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.IndexSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.IndexSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.IndexSwitch.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.IndexSwitch.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.manual.IndexSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.IndexSwitch.bundle) |  |
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

##### boolean

``` python
boolean(index=0, items=())
```

##### bundle

``` python
bundle(index=0, items=())
```

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
| [`name`](#nodebpy.nodes.geometry.manual.JoinGeometry.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.JoinGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinGeometry.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.JoinGeometry.type) |  |

### JoinStrings

``` python
JoinStrings(strings=(), delimiter='')
```

Combine any number of input strings

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.JoinStrings.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.JoinStrings.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.JoinStrings.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinStrings.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinStrings.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinStrings.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.JoinStrings.type) |  |

### MenuSwitch

``` python
MenuSwitch(menu=None, items={}, *, data_type='FLOAT')
```

Node builder for the Menu Switch node

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.geometry.manual.MenuSwitch.i) |  |
| [`name`](#nodebpy.nodes.geometry.manual.MenuSwitch.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MenuSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.MenuSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MenuSwitch.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.MenuSwitch.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.manual.MenuSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.geometry.manual.MenuSwitch.bundle) |  |
| [closure](#nodebpy.nodes.geometry.manual.MenuSwitch.closure) |  |
| [collection](#nodebpy.nodes.geometry.manual.MenuSwitch.collection) |  |
| [color](#nodebpy.nodes.geometry.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.geometry.manual.MenuSwitch.float) |  |
| [geometry](#nodebpy.nodes.geometry.manual.MenuSwitch.geometry) |  |
| [image](#nodebpy.nodes.geometry.manual.MenuSwitch.image) |  |
| [integer](#nodebpy.nodes.geometry.manual.MenuSwitch.integer) |  |
| [material](#nodebpy.nodes.geometry.manual.MenuSwitch.material) |  |
| [matrix](#nodebpy.nodes.geometry.manual.MenuSwitch.matrix) |  |
| [menu](#nodebpy.nodes.geometry.manual.MenuSwitch.menu) |  |
| [object](#nodebpy.nodes.geometry.manual.MenuSwitch.object) |  |
| [rotation](#nodebpy.nodes.geometry.manual.MenuSwitch.rotation) |  |
| [string](#nodebpy.nodes.geometry.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.geometry.manual.MenuSwitch.vector) |  |

##### boolean

``` python
boolean(menu=None, items={})
```

##### bundle

``` python
bundle(menu=None, items={})
```

##### closure

``` python
closure(menu=None, items={})
```

##### collection

``` python
collection(menu=None, items={})
```

##### color

``` python
color(menu=None, items={})
```

##### float

``` python
float(menu=None, items={})
```

##### geometry

``` python
geometry(menu=None, items={})
```

##### image

``` python
image(menu=None, items={})
```

##### integer

``` python
integer(menu=None, items={})
```

##### material

``` python
material(menu=None, items={})
```

##### matrix

``` python
matrix(menu=None, items={})
```

##### menu

``` python
menu(menu=None, items={})
```

##### object

``` python
object(menu=None, items={})
```

##### rotation

``` python
rotation(menu=None, items={})
```

##### string

``` python
string(menu=None, items={})
```

##### vector

``` python
vector(menu=None, items={})
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
| [`name`](#nodebpy.nodes.geometry.manual.MeshBoolean.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.MeshBoolean.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MeshBoolean.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.MeshBoolean.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.MeshBoolean.outputs) |  |
| [`solver`](#nodebpy.nodes.geometry.manual.MeshBoolean.solver) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MeshBoolean.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.MeshBoolean.type) |  |

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
| [`name`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.o) |  |
| [`operation`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.operation) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.type) |  |

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

### SetHandleType

``` python
SetHandleType(
    curve=None,
    selection=True,
    *,
    left=False,
    right=False,
    handle_type='AUTO',
)
```

Set the handle type for the control points of a Bézier curve

#### Attributes

| Name | Description |
|----|----|
| [`handle_type`](#nodebpy.nodes.geometry.manual.SetHandleType.handle_type) |  |
| [`i`](#nodebpy.nodes.geometry.manual.SetHandleType.i) |  |
| [`left`](#nodebpy.nodes.geometry.manual.SetHandleType.left) |  |
| [`name`](#nodebpy.nodes.geometry.manual.SetHandleType.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.SetHandleType.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.SetHandleType.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.SetHandleType.outputs) |  |
| [`right`](#nodebpy.nodes.geometry.manual.SetHandleType.right) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.SetHandleType.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.SetHandleType.type) |  |

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
| [`name`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.outputs) |  |
| [`point`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.point) |  |
| [`spline`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.spline) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.StoreNamedAttribute.type) |  |

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

### Switch

``` python
Switch(switch=False, false=None, true=None, *, input_type='FLOAT')
```

Switch between two inputs

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| switch | InputBoolean | Switch      | `False` |
| false  | InputFloat   | False       | `None`  |
| true   | InputFloat   | True        | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Switch.i) |  |
| [`input_type`](#nodebpy.nodes.geometry.manual.Switch.input_type) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Switch.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Switch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Switch.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Switch.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Switch.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Switch.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.manual.Switch.boolean) | Create Switch with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.geometry.manual.Switch.bundle) | Create Switch with operation ‘Bundle’. |
| [closure](#nodebpy.nodes.geometry.manual.Switch.closure) | Create Switch with operation ‘Closure’. |
| [collection](#nodebpy.nodes.geometry.manual.Switch.collection) | Create Switch with operation ‘Collection’. |
| [color](#nodebpy.nodes.geometry.manual.Switch.color) | Create Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.geometry.manual.Switch.float) | Create Switch with operation ‘Float’. |
| [font](#nodebpy.nodes.geometry.manual.Switch.font) | Create Switch with operation ‘Font’. |
| [geometry](#nodebpy.nodes.geometry.manual.Switch.geometry) | Create Switch with operation ‘Geometry’. |
| [image](#nodebpy.nodes.geometry.manual.Switch.image) | Create Switch with operation ‘Image’. |
| [integer](#nodebpy.nodes.geometry.manual.Switch.integer) | Create Switch with operation ‘Integer’. |
| [material](#nodebpy.nodes.geometry.manual.Switch.material) | Create Switch with operation ‘Material’. |
| [matrix](#nodebpy.nodes.geometry.manual.Switch.matrix) | Create Switch with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.geometry.manual.Switch.menu) | Create Switch with operation ‘Menu’. |
| [object](#nodebpy.nodes.geometry.manual.Switch.object) | Create Switch with operation ‘Object’. |
| [rotation](#nodebpy.nodes.geometry.manual.Switch.rotation) | Create Switch with operation ‘Rotation’. |
| [string](#nodebpy.nodes.geometry.manual.Switch.string) | Create Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.geometry.manual.Switch.vector) | Create Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(switch=False, false=False, true=False)
```

Create Switch with operation ‘Boolean’.

##### bundle

``` python
bundle(switch=False, false=None, true=None)
```

Create Switch with operation ‘Bundle’.

##### closure

``` python
closure(switch=False, false=None, true=None)
```

Create Switch with operation ‘Closure’.

##### collection

``` python
collection(switch=False, false=None, true=None)
```

Create Switch with operation ‘Collection’.

##### color

``` python
color(switch=False, false=None, true=None)
```

Create Switch with operation ‘Color’.

##### float

``` python
float(switch=False, false=0.0, true=0.0)
```

Create Switch with operation ‘Float’.

##### font

``` python
font(switch=False, false=None, true=None)
```

Create Switch with operation ‘Font’.

##### geometry

``` python
geometry(switch=False, false=None, true=None)
```

Create Switch with operation ‘Geometry’.

##### image

``` python
image(switch=False, false=None, true=None)
```

Create Switch with operation ‘Image’.

##### integer

``` python
integer(switch=False, false=0, true=0)
```

Create Switch with operation ‘Integer’.

##### material

``` python
material(switch=False, false=None, true=None)
```

Create Switch with operation ‘Material’.

##### matrix

``` python
matrix(switch=False, false=None, true=None)
```

Create Switch with operation ‘Matrix’.

##### menu

``` python
menu(switch=False, false=None, true=None)
```

Create Switch with operation ‘Menu’.

##### object

``` python
object(switch=False, false=None, true=None)
```

Create Switch with operation ‘Object’.

##### rotation

``` python
rotation(switch=False, false=None, true=None)
```

Create Switch with operation ‘Rotation’.

##### string

``` python
string(switch=False, false='', true='')
```

Create Switch with operation ‘String’.

##### vector

``` python
vector(switch=False, false=None, true=None)
```

Create Switch with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.switch` | `BooleanSocket` | Switch      |
| `i.false`  | `FloatSocket`   | False       |
| `i.true`   | `FloatSocket`   | True        |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `FloatSocket` | Output      |

### Value

``` python
Value(value=0.0)
```

Input numerical values to other nodes in the tree

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Value.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.manual.Value.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Value.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Value.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Value.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Value.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Value.type) |  |
| [`value`](#nodebpy.nodes.geometry.manual.Value.value) | Input socket: Value |
