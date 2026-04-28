# nodes.geometry.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [AccumulateField](#nodebpy.nodes.geometry.manual.AccumulateField) | Add the values of an evaluated field together and output the running total for each element |
| [AttributeStatistic](#nodebpy.nodes.geometry.manual.AttributeStatistic) | Calculate statistics about a data set from a field evaluated on a geometry |
| [Bake](#nodebpy.nodes.geometry.manual.Bake) | Cache the incoming data so that it can be used without recomputation |
| [CaptureAttribute](#nodebpy.nodes.geometry.manual.CaptureAttribute) | Store the result of a field on a geometry and output the data as a node socket. |
| [Compare](#nodebpy.nodes.geometry.manual.Compare) | Perform a comparison operation on the two given inputs |
| [EvaluateAtIndex](#nodebpy.nodes.geometry.manual.EvaluateAtIndex) | Retrieve data of other elements in the context’s geometry |
| [EvaluateClosure](#nodebpy.nodes.geometry.manual.EvaluateClosure) | Execute a given closure |
| [EvaluateOnDomain](#nodebpy.nodes.geometry.manual.EvaluateOnDomain) | Retrieve values from a field on a different domain besides the domain from the context |
| [FieldAverage](#nodebpy.nodes.geometry.manual.FieldAverage) | Calculate the mean and median of a given field |
| [FieldMinAndMax](#nodebpy.nodes.geometry.manual.FieldMinAndMax) | Calculate the minimum and maximum of a given field |
| [FieldToGrid](#nodebpy.nodes.geometry.manual.FieldToGrid) | Create new grids by evaluating new values on an existing volume grid topology |
| [FieldVariance](#nodebpy.nodes.geometry.manual.FieldVariance) | Calculate the standard deviation and variance of a given field |
| [Float](#nodebpy.nodes.geometry.manual.Float) | Input numerical values to other nodes in the tree. A ‘type-hinted’ wrapper of the Value node. |
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
| [Value](#nodebpy.nodes.geometry.manual.Value) | Input numerical values to other nodes in the tree |

### AccumulateField

``` python
AccumulateField(
    value=1.0,
    group_index=0,
    *,
    data_type='FLOAT',
    domain='POINT',
    **kwargs,
)
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
| [`inputs`](#nodebpy.nodes.geometry.manual.AccumulateField.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.AttributeStatistic.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.Bake.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Bake.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Bake.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Bake.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.manual.Bake.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Bake.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Bake.type) |  |

### CaptureAttribute

``` python
CaptureAttribute(*args, geometry=None, domain='POINT', **kwargs)
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
| [`inputs`](#nodebpy.nodes.geometry.manual.CaptureAttribute.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.Compare.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.EvaluateAtIndex.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.EvaluateClosure.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.EvaluateOnDomain.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.FieldAverage.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.FieldMinAndMax.inputs) |  |
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
FieldToGrid(*args, topology=None, data_type='FLOAT', **kwargs)
```

Create new grids by evaluating new values on an existing volume grid topology

New socket items for field evaluation are first created from \*args then \*\*kwargs to give specific names to the items.

Data types are inferred automatically from the closest compatible data type.

#### Inputs:

topology: InputLinkable The grid which contains the topology to evaluate the different fields on. data_type: \_GridDataTypes = “FLOAT” The data type of the grid to evaluate on. Possible values are “FLOAT”, “INT”, “VECTOR”, “BOOLEAN”. \*args: InputFloat \| InputVector \| InputInteger \| InputBoolean The fields to evaluate on the grid. \*\*kwargs: dict\[str, InputFloat \| InputVector \| InputInteger \| InputGeometry\] The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket.

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.manual.FieldToGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.manual.FieldToGrid.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.FieldToGrid.inputs) |  |
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
boolean(*args, topology=None, **kwargs)
```

##### capture

``` python
capture(*args, **kwargs)
```

##### float

``` python
float(*args, topology=None, **kwargs)
```

##### integer

``` python
integer(*args, topology=None, **kwargs)
```

##### vector

``` python
vector(*args, topology=None, **kwargs)
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
| [`inputs`](#nodebpy.nodes.geometry.manual.FieldVariance.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.Float.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Float.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Float.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Float.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Float.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Float.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Float.type) |  |
| [`value`](#nodebpy.nodes.geometry.manual.Float.value) | Input socket: Value |

### FormatString

``` python
FormatString(*args, format='', **kwargs)
```

Insert values into a string using a Python and path template compatible formatting syntax

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.FormatString.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.FormatString.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.Frame.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.GeometryToInstance.inputs) |  |
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
| [`inputs`](#nodebpy.nodes.geometry.manual.HandleTypeSelection.inputs) |  |
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
IndexSwitch(*args, index=0, data_type='FLOAT')
```

Node builder for the Index Switch node

#### Attributes

| Name | Description |
|----|----|
| [`boolean`](#nodebpy.nodes.geometry.manual.IndexSwitch.boolean) |  |
| [`bundle`](#nodebpy.nodes.geometry.manual.IndexSwitch.bundle) |  |
| [`closure`](#nodebpy.nodes.geometry.manual.IndexSwitch.closure) |  |
| [`collection`](#nodebpy.nodes.geometry.manual.IndexSwitch.collection) |  |
| [`color`](#nodebpy.nodes.geometry.manual.IndexSwitch.color) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.IndexSwitch.data_type) | Input socket: Data Type |
| [`float`](#nodebpy.nodes.geometry.manual.IndexSwitch.float) |  |
| [`geometry`](#nodebpy.nodes.geometry.manual.IndexSwitch.geometry) |  |
| [`i`](#nodebpy.nodes.geometry.manual.IndexSwitch.i) |  |
| [`image`](#nodebpy.nodes.geometry.manual.IndexSwitch.image) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.IndexSwitch.inputs) |  |
| [`integer`](#nodebpy.nodes.geometry.manual.IndexSwitch.integer) |  |
| [`material`](#nodebpy.nodes.geometry.manual.IndexSwitch.material) |  |
| [`matrix`](#nodebpy.nodes.geometry.manual.IndexSwitch.matrix) |  |
| [`menu`](#nodebpy.nodes.geometry.manual.IndexSwitch.menu) |  |
| [`name`](#nodebpy.nodes.geometry.manual.IndexSwitch.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.IndexSwitch.o) |  |
| [`object`](#nodebpy.nodes.geometry.manual.IndexSwitch.object) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.IndexSwitch.outputs) |  |
| [`rotation`](#nodebpy.nodes.geometry.manual.IndexSwitch.rotation) |  |
| [`string`](#nodebpy.nodes.geometry.manual.IndexSwitch.string) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.IndexSwitch.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.IndexSwitch.type) |  |
| [`vector`](#nodebpy.nodes.geometry.manual.IndexSwitch.vector) |  |

### JoinGeometry

``` python
JoinGeometry(*args)
```

Merge separately generated geometries into a single one

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.JoinGeometry.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.JoinGeometry.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.manual.JoinGeometry.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.JoinGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinGeometry.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.JoinGeometry.type) |  |

### JoinStrings

``` python
JoinStrings(*args, delimiter='')
```

Combine any number of input strings

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.JoinStrings.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.JoinStrings.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.manual.JoinStrings.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.JoinStrings.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.JoinStrings.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.JoinStrings.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.JoinStrings.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.JoinStrings.type) |  |

### MenuSwitch

``` python
MenuSwitch(*args, menu=None, data_type='FLOAT', **kwargs)
```

Node builder for the Menu Switch node

#### Attributes

| Name | Description |
|----|----|
| [`boolean`](#nodebpy.nodes.geometry.manual.MenuSwitch.boolean) |  |
| [`bundle`](#nodebpy.nodes.geometry.manual.MenuSwitch.bundle) |  |
| [`closure`](#nodebpy.nodes.geometry.manual.MenuSwitch.closure) |  |
| [`collection`](#nodebpy.nodes.geometry.manual.MenuSwitch.collection) |  |
| [`color`](#nodebpy.nodes.geometry.manual.MenuSwitch.color) |  |
| [`data_type`](#nodebpy.nodes.geometry.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`float`](#nodebpy.nodes.geometry.manual.MenuSwitch.float) |  |
| [`geometry`](#nodebpy.nodes.geometry.manual.MenuSwitch.geometry) |  |
| [`i`](#nodebpy.nodes.geometry.manual.MenuSwitch.i) |  |
| [`image`](#nodebpy.nodes.geometry.manual.MenuSwitch.image) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.MenuSwitch.inputs) |  |
| [`integer`](#nodebpy.nodes.geometry.manual.MenuSwitch.integer) |  |
| [`material`](#nodebpy.nodes.geometry.manual.MenuSwitch.material) |  |
| [`matrix`](#nodebpy.nodes.geometry.manual.MenuSwitch.matrix) |  |
| [`menu`](#nodebpy.nodes.geometry.manual.MenuSwitch.menu) |  |
| [`name`](#nodebpy.nodes.geometry.manual.MenuSwitch.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.MenuSwitch.o) |  |
| [`object`](#nodebpy.nodes.geometry.manual.MenuSwitch.object) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.MenuSwitch.outputs) |  |
| [`rotation`](#nodebpy.nodes.geometry.manual.MenuSwitch.rotation) |  |
| [`string`](#nodebpy.nodes.geometry.manual.MenuSwitch.string) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.MenuSwitch.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.MenuSwitch.type) |  |
| [`vector`](#nodebpy.nodes.geometry.manual.MenuSwitch.vector) |  |

### MeshBoolean

``` python
MeshBoolean(*args, operation='DIFFERENCE', solver='FLOAT', **kwargs)
```

Cut, subtract, or join multiple mesh inputs

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.MeshBoolean.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.manual.MeshBoolean.inputs) |  |
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
    *args,
    mesh_1=None,
    self_intersection=False,
    hole_tolerant=False,
    solver='FLOAT',
)
```

##### intersect

``` python
intersect(*args, self_intersection=False, hole_tolerant=False, solver='FLOAT')
```

##### union

``` python
union(*args, self_intersection=False, hole_tolerant=False, solver='FLOAT')
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
| [`inputs`](#nodebpy.nodes.geometry.manual.SDFGridBoolean.inputs) |  |
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
difference(*args, grid_1=None)
```

Create SDF Grid Boolean with operation ‘Difference’.

##### intersect

``` python
intersect(*args)
```

##### union

``` python
union(*args)
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
| [`inputs`](#nodebpy.nodes.geometry.manual.SetHandleType.inputs) |  |
| [`left`](#nodebpy.nodes.geometry.manual.SetHandleType.left) |  |
| [`name`](#nodebpy.nodes.geometry.manual.SetHandleType.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.SetHandleType.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.SetHandleType.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.SetHandleType.outputs) |  |
| [`right`](#nodebpy.nodes.geometry.manual.SetHandleType.right) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.SetHandleType.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.SetHandleType.type) |  |

### Value

``` python
Value(value=0.0)
```

Input numerical values to other nodes in the tree

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.manual.Value.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.manual.Value.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.manual.Value.name) |  |
| [`node`](#nodebpy.nodes.geometry.manual.Value.node) |  |
| [`o`](#nodebpy.nodes.geometry.manual.Value.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.manual.Value.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.manual.Value.tree) |  |
| [`type`](#nodebpy.nodes.geometry.manual.Value.type) |  |
| [`value`](#nodebpy.nodes.geometry.manual.Value.value) | Input socket: Value |
