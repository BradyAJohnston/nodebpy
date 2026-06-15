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
| [RepeatZone](#nodebpy.nodes.geometry.zone.RepeatZone) |  |
| [SimulationInput](#nodebpy.nodes.geometry.zone.SimulationInput) | Simulation Input node |
| [SimulationOutput](#nodebpy.nodes.geometry.zone.SimulationOutput) | Simulation Output node |
| [SimulationZone](#nodebpy.nodes.geometry.zone.SimulationZone) |  |
| [ZoneItem](#nodebpy.nodes.geometry.zone.ZoneItem) | Handle for a simulation/repeat state item (four sockets per item). |

### BaseRepeatZone

``` python
BaseRepeatZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.BaseRepeatZone.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.BaseRepeatZone.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.BaseRepeatZone.capture) | Add an item linked from `value` and return its output socket. |

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

### BaseSimulationZone

``` python
BaseSimulationZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.BaseSimulationZone.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.BaseSimulationZone.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.BaseSimulationZone.capture) | Add an item linked from `value` and return its output socket. |

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

### BaseZone

``` python
BaseZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZone.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.BaseZone.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.BaseZone.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.BaseZone.capture) | Add an item linked from `value` and return its output socket. |

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

### BaseZoneInput

``` python
BaseZoneInput(node=None)
```

Base class for zone input nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneInput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneInput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`output`](#nodebpy.nodes.geometry.zone.BaseZoneInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZoneInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.BaseZoneInput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.BaseZoneInput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.BaseZoneInput.capture) | Add an item linked from `value` and return its output socket. |

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

### BaseZoneOutput

``` python
BaseZoneOutput(node=None)
```

Base class for zone output nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.BaseZoneOutput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.BaseZoneOutput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.BaseZoneOutput.capture) | Add an item linked from `value` and return its output socket. |

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

### ClosureInput

``` python
ClosureInput()
```

Closure Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.ClosureInput.i) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ClosureInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ClosureInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ClosureInput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ClosureInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureInput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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
| [`name`](#nodebpy.nodes.geometry.zone.ClosureOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ClosureOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ClosureOutput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ClosureOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

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

| Name | Description |
|----|----|
| [`closure`](#nodebpy.nodes.geometry.zone.ClosureZone.closure) | The closure produced by the zone. |
| [`input`](#nodebpy.nodes.geometry.zone.ClosureZone.input) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ClosureZone.output) |  |

#### Methods

| Name | Description |
|----|----|
| [input_item](#nodebpy.nodes.geometry.zone.ClosureZone.input_item) | Declare a closure input and return the socket to read in the body. |
| [output_item](#nodebpy.nodes.geometry.zone.ClosureZone.output_item) | Declare a closure output and return the target to feed with `>>`. |

##### input_item

``` python
input_item(name, type='GEOMETRY')
```

Declare a closure input and return the socket to read in the body.

`type` is a socket-type string (`"GEOMETRY"`, `"MATRIX"`, `"VECTOR"`, …); the item collection lives on the output node and drives the matching output socket on the input node.

##### output_item

``` python
output_item(name, type='GEOMETRY')
```

Declare a closure output and return the target to feed with `>>`.

### ForEachGeometryElementInput

``` python
ForEachGeometryElementInput(geometry=None, selection=True)
```

For Each Geometry Element Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.i) |  |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.capture) | Add an item linked from `value` and return its output socket. |

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
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items) | The bpy item collection driving this zone’s sockets. |
| [`items_generated`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items_generated) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_generated_item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.add_generated_item) | Add a generation item and return its handle. |
| [add_item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.capture) | Add an item linked from `value` and return its output socket. |
| [capture_generated](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.capture_generated) | Capture `value` as a generated-geometry item evaluated on the |

##### add_generated_item

``` python
add_generated_item(name, value=None, *, type=None, domain='POINT')
```

Add a generation item and return its handle.

`value` may be a linkable (linked to the item’s input) or a plain default value; otherwise `type` declares the item unlinked.

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

##### capture_generated

``` python
capture_generated(value, *, name=None, domain='POINT')
```

Capture `value` as a generated-geometry item evaluated on the given `domain`, and return its output socket.

### ForEachGeometryElementZone

``` python
ForEachGeometryElementZone(geometry=None, selection=True, *, domain='POINT')
```

#### Attributes

| Name | Description |
|----|----|
| [`generation`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.generation) | Handle for the default generation item (the generated geometry). |
| [`index`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.index) |  |
| [`input`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.input) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.output) |  |

#### Methods

| Name | Description |
|----|----|
| [generated_item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.generated_item) | Declare a generation item — a value stored on the generated |
| [item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.item) | Declare an input item — a per-element field made available |
| [main_item](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.main_item) | Declare a main item — a per-element result written back onto |

##### generated_item

``` python
generated_item(name, value=None, *, type=None, domain='POINT')
```

Declare a generation item — a value stored on the generated geometry with the given `domain`.

##### item

``` python
item(name, value=None, *, type=None)
```

Declare an input item — a per-element field made available inside the zone.

##### main_item

``` python
main_item(name, value=None, *, type=None)
```

Declare a main item — a per-element result written back onto the input geometry.

### RepeatInput

``` python
RepeatInput(iterations=1)
```

Repeat Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatInput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.RepeatInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.RepeatInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.RepeatInput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.RepeatInput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.RepeatInput.capture) | Add an item linked from `value` and return its output socket. |

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

### RepeatOutput

``` python
RepeatOutput(node=None)
```

Repeat Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatOutput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.RepeatOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.RepeatOutput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.RepeatOutput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.RepeatOutput.capture) | Add an item linked from `value` and return its output socket. |

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

### RepeatZone

``` python
RepeatZone(iterations=1, items=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`input`](#nodebpy.nodes.geometry.zone.RepeatZone.input) |  |
| [`iteration`](#nodebpy.nodes.geometry.zone.RepeatZone.iteration) | The current iteration index. |
| [`output`](#nodebpy.nodes.geometry.zone.RepeatZone.output) |  |

#### Methods

| Name | Description |
|----|----|
| [item](#nodebpy.nodes.geometry.zone.RepeatZone.item) | Declare a state item and return its handle. |

##### item

``` python
item(name, initial=None, *, type=None)
```

Declare a state item and return its handle.

`initial` may be a linkable (linked as the item’s starting value), a plain default value, or a socket-type string such as `"FLOAT"` (declares the item without linking).

### SimulationInput

``` python
SimulationInput(node=None)
```

Simulation Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.SimulationInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationInput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationInput.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.SimulationInput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.SimulationInput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.SimulationInput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.SimulationInput.capture) | Add an item linked from `value` and return its output socket. |

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

### SimulationOutput

``` python
SimulationOutput(node=None)
```

Simulation Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.SimulationOutput.i) |  |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationOutput.items) | The bpy item collection driving this zone’s sockets. |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.zone.SimulationOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.geometry.zone.SimulationOutput.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.geometry.zone.SimulationOutput.add_items) | Add an item per mapping entry and return their handles by name. |
| [capture](#nodebpy.nodes.geometry.zone.SimulationOutput.capture) | Add an item linked from `value` and return its output socket. |

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

### SimulationZone

``` python
SimulationZone(items=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`delta_time`](#nodebpy.nodes.geometry.zone.SimulationZone.delta_time) |  |
| [`input`](#nodebpy.nodes.geometry.zone.SimulationZone.input) |  |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationZone.output) |  |

#### Methods

| Name | Description |
|----|----|
| [item](#nodebpy.nodes.geometry.zone.SimulationZone.item) | Declare a state item and return its handle. |

##### item

``` python
item(name, initial=None, *, type=None)
```

Declare a state item and return its handle.

`initial` may be a linkable (linked as the item’s starting value), a plain default value, or a socket-type string such as `"FLOAT"` (declares the item without linking).

### ZoneItem

``` python
ZoneItem(input_node, output_node, item)
```

Handle for a simulation/repeat state item (four sockets per item).

#### Attributes

| Name | Description |
|----|----|
| [`current`](#nodebpy.nodes.geometry.zone.ZoneItem.current) | Input-node output socket — read the item inside the zone body. |
| [`initial`](#nodebpy.nodes.geometry.zone.ZoneItem.initial) | Input-node input socket — set the item’s starting value. |
| [`input`](#nodebpy.nodes.geometry.zone.ZoneItem.input) | The node’s input socket for this item. |
| [`name`](#nodebpy.nodes.geometry.zone.ZoneItem.name) |  |
| [`next`](#nodebpy.nodes.geometry.zone.ZoneItem.next) | Output-node input socket — write the item’s per-iteration result. |
| [`output`](#nodebpy.nodes.geometry.zone.ZoneItem.output) | The node’s output socket for this item. |
| [`result`](#nodebpy.nodes.geometry.zone.ZoneItem.result) | Output-node output socket — read the item after the zone. |
| [`socket_type`](#nodebpy.nodes.geometry.zone.ZoneItem.socket_type) |  |
