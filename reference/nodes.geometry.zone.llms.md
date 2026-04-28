# nodes.geometry.zone

`zone`

## Classes

| Name | Description |
|----|----|
| [BaseRepeatZone](#nodebpy.nodes.geometry.zone.BaseRepeatZone) |  |
| [BaseSimulationZone](#nodebpy.nodes.geometry.zone.BaseSimulationZone) |  |
| [BaseZone](#nodebpy.nodes.geometry.zone.BaseZone) |  |
| [BaseZoneInput](#nodebpy.nodes.geometry.zone.BaseZoneInput) | Base class for zone input nodes |
| [BaseZoneOutput](#nodebpy.nodes.geometry.zone.BaseZoneOutput) | Base class for zone output nodes |
| [ClosureInput](#nodebpy.nodes.geometry.zone.ClosureInput) | Closure Input node |
| [ClosureOutput](#nodebpy.nodes.geometry.zone.ClosureOutput) | Closure Output node |
| [ClosureZone](#nodebpy.nodes.geometry.zone.ClosureZone) |  |
| [ForEachGeometryElementInput](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput) | For Each Geometry Element Input node |
| [ForEachGeometryElementOutput](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput) | For Each Geometry Element Output node |
| [ForEachGeometryElementZone](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone) |  |
| [RepeatInput](#nodebpy.nodes.geometry.zone.RepeatInput) | Repeat Input node |
| [RepeatOutput](#nodebpy.nodes.geometry.zone.RepeatOutput) | Repeat Output node |
| [RepeatZone](#nodebpy.nodes.geometry.zone.RepeatZone) | Wrapper that supports both direct unpacking and iteration |
| [SimulationInput](#nodebpy.nodes.geometry.zone.SimulationInput) | Simulation Input node |
| [SimulationOutput](#nodebpy.nodes.geometry.zone.SimulationOutput) | Simulation Output node |
| [SimulationZone](#nodebpy.nodes.geometry.zone.SimulationZone) |  |

### BaseRepeatZone

``` python
BaseRepeatZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.BaseRepeatZone.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### BaseSimulationZone

``` python
BaseSimulationZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.BaseSimulationZone.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### BaseZone

``` python
BaseZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.BaseZone.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZone.items) | Return the items collection |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZone.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZone.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.BaseZone.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.BaseZone.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### BaseZoneInput

``` python
BaseZoneInput(node=None)
```

Base class for zone input nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.BaseZoneInput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneInput.items) | Return the items collection |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneInput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneInput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`output`](#nodebpy.nodes.geometry.zone.BaseZoneInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZoneInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneInput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.BaseZoneInput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.BaseZoneInput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### BaseZoneOutput

``` python
BaseZoneOutput(node=None)
```

Base class for zone output nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.items) | Return the items collection |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.BaseZoneOutput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### ClosureInput

``` python
ClosureInput()
```

Closure Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.ClosureInput.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.zone.ClosureInput.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ClosureInput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.ClosureInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ClosureInput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ClosureInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureInput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.ClosureInput.type) |  |

#### Methods

| Name                                                   | Description |
|--------------------------------------------------------|-------------|
| [link](#nodebpy.nodes.geometry.zone.ClosureInput.link) |             |

##### link

``` python
link(target)
```

### ClosureOutput

``` python
ClosureOutput(define_signature=False)
```

Closure Output node

#### Attributes

| Name | Description |
|----|----|
| [`define_signature`](#nodebpy.nodes.geometry.zone.ClosureOutput.define_signature) |  |
| [`i`](#nodebpy.nodes.geometry.zone.ClosureOutput.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.zone.ClosureOutput.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ClosureOutput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.ClosureOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ClosureOutput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ClosureOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureOutput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.ClosureOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [link](#nodebpy.nodes.geometry.zone.ClosureOutput.link) |  |
| [sync_signature](#nodebpy.nodes.geometry.zone.ClosureOutput.sync_signature) |  |

##### link

``` python
link(source)
```

##### sync_signature

``` python
sync_signature(node)
```

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.closure` | `ClosureSocket` | Closure     |

### ClosureZone

``` python
ClosureZone()
```

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`input`](#nodebpy.nodes.geometry.zone.ClosureZone.input)   |             |
| [`output`](#nodebpy.nodes.geometry.zone.ClosureZone.output) |             |

### ForEachGeometryElementInput

``` python
ForEachGeometryElementInput(geometry=None, selection=True)
```

For Each Geometry Element Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### ForEachGeometryElementOutput

``` python
ForEachGeometryElementOutput(domain='POINT', **kwargs)
```

For Each Geometry Element Output node

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.domain) |  |
| [`i`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items) |  |
| [`items_generated`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items_generated) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.capture) | Capture something as an input to the simulation |
| [capture_generated](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.capture_generated) |  |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

##### capture_generated

``` python
capture_generated(value)
```

### ForEachGeometryElementZone

``` python
ForEachGeometryElementZone(geometry=None, selection=True, *, domain='POINT')
```

#### Attributes

| Name | Description |
|----|----|
| [`index`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.index) |  |
| [`input`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.input) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.output) |  |

### RepeatInput

``` python
RepeatInput(iterations=1)
```

Repeat Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.RepeatInput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatInput.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatInput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.RepeatInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.RepeatInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatInput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.RepeatInput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.RepeatInput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### RepeatOutput

``` python
RepeatOutput(node=None)
```

Repeat Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.RepeatOutput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatOutput.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatOutput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.RepeatOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatOutput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.RepeatOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.RepeatOutput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### RepeatZone

``` python
RepeatZone(iterations=1, *args, **kwargs)
```

Wrapper that supports both direct unpacking and iteration

#### Attributes

| Name | Description |
|----|----|
| [`input`](#nodebpy.nodes.geometry.zone.RepeatZone.input) |  |
| [`iteration`](#nodebpy.nodes.geometry.zone.RepeatZone.iteration) | The current iteration index. |
| [`output`](#nodebpy.nodes.geometry.zone.RepeatZone.output) |  |

### SimulationInput

``` python
SimulationInput(node=None)
```

Simulation Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.SimulationInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`inputs`](#nodebpy.nodes.geometry.zone.SimulationInput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationInput.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationInput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.SimulationInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationInput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.SimulationInput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.SimulationInput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### SimulationOutput

``` python
SimulationOutput(node=None)
```

Simulation Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.SimulationOutput.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.zone.SimulationOutput.inputs) |  |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationOutput.items) |  |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationOutput.name) |  |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.SimulationOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationOutput.tree) |  |
| [`type`](#nodebpy.nodes.geometry.zone.SimulationOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [capture](#nodebpy.nodes.geometry.zone.SimulationOutput.capture) | Capture something as an input to the simulation |

##### capture

``` python
capture(value, domain='POINT')
```

Capture something as an input to the simulation

### SimulationZone

``` python
SimulationZone(*args, **kwargs)
```

#### Attributes

| Name | Description |
|----|----|
| [`delta_time`](#nodebpy.nodes.geometry.zone.SimulationZone.delta_time) |  |
| [`input`](#nodebpy.nodes.geometry.zone.SimulationZone.input) |  |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationZone.output) |  |
