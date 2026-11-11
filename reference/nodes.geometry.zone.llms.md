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
| [`items`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseRepeatZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.BaseRepeatZone.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### BaseSimulationZone

``` python
BaseSimulationZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseSimulationZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.BaseSimulationZone.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### BaseZone

``` python
BaseZone(node=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZone.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZone.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZone.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZone.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZone.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZone.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.BaseZone.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### BaseZoneInput

``` python
BaseZoneInput(node=None)
```

Base class for zone input nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneInput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneInput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`output`](#nodebpy.nodes.geometry.zone.BaseZoneInput.output) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.BaseZoneInput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### BaseZoneOutput

``` python
BaseZoneOutput(node=None)
```

Base class for zone output nodes

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.BaseZoneOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.BaseZoneOutput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

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
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureInput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [link](#nodebpy.nodes.geometry.zone.ClosureInput.link) |  |
| [props](#nodebpy.nodes.geometry.zone.ClosureInput.props) | Set the properties every node has and return the node, so it can |

##### link

``` python
link(target)
```

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

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
| [`tree`](#nodebpy.nodes.geometry.zone.ClosureOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [link](#nodebpy.nodes.geometry.zone.ClosureOutput.link) |  |
| [props](#nodebpy.nodes.geometry.zone.ClosureOutput.props) | Set the properties every node has and return the node, so it can |
| [sync_signature](#nodebpy.nodes.geometry.zone.ClosureOutput.sync_signature) |  |

##### link

``` python
link(source)
```

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

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
| [`inputs`](#nodebpy.nodes.geometry.zone.ClosureZone.inputs) | The closure’s input items. |
| [`output`](#nodebpy.nodes.geometry.zone.ClosureZone.output) |  |
| [`outputs`](#nodebpy.nodes.geometry.zone.ClosureZone.outputs) | The closure’s output items. |

### ForEachGeometryElementInput

``` python
ForEachGeometryElementInput(geometry=None, selection=True)
```

For Each Geometry Element Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.i) |  |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.output) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.ForEachGeometryElementInput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### ForEachGeometryElementOutput

``` python
ForEachGeometryElementOutput(domain='POINT', **kwargs)
```

For Each Geometry Element Output node

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.domain) |  |
| [`i`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items) | The node’s items; subclasses return their typed collection. |
| [`items_generated`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.items_generated) |  |
| [`name`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.o) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.ForEachGeometryElementOutput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### ForEachGeometryElementZone

``` python
ForEachGeometryElementZone(geometry=None, selection=True, *, domain='POINT')
```

#### Attributes

| Name | Description |
|----|----|
| [`corner`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.corner) |  |
| [`curve`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.curve) |  |
| [`edge`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.edge) |  |
| [`element`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.element) | The current element as geometry, read inside the zone body. |
| [`face`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.face) |  |
| [`generated_items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.generated_items) | Generation items: values stored on the generated geometry. |
| [`index`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.index) |  |
| [`input`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.input) |  |
| [`instance`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.instance) |  |
| [`items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.items) | Per-element input items, read inside the body. |
| [`layer`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.layer) |  |
| [`main_items`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.main_items) | Main items: per-element results written back onto the geometry. |
| [`output`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.output) |  |
| [`point`](#nodebpy.nodes.geometry.zone.ForEachGeometryElementZone.point) |  |

### RepeatInput

``` python
RepeatInput(iterations=1)
```

Repeat Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatInput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatInput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.RepeatInput.output) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.RepeatInput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### RepeatOutput

``` python
RepeatOutput(node=None)
```

Repeat Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.RepeatOutput.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatOutput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.RepeatOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.RepeatOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.RepeatOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.RepeatOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.RepeatOutput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### RepeatZone

``` python
RepeatZone(iterations=1, items=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`input`](#nodebpy.nodes.geometry.zone.RepeatZone.input) |  |
| [`items`](#nodebpy.nodes.geometry.zone.RepeatZone.items) | The zone’s state items. |
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
| [`items`](#nodebpy.nodes.geometry.zone.SimulationInput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationInput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationInput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationInput.o) |  |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationInput.output) |  |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationInput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.SimulationInput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### SimulationOutput

``` python
SimulationOutput(node=None)
```

Simulation Output node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.zone.SimulationOutput.i) |  |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationOutput.items) | The node’s items; subclasses return their typed collection. |
| [`name`](#nodebpy.nodes.geometry.zone.SimulationOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.zone.SimulationOutput.node) |  |
| [`o`](#nodebpy.nodes.geometry.zone.SimulationOutput.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.geometry.zone.SimulationOutput.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.zone.SimulationOutput.props) | Set the properties every node has and return the node, so it can |

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.

### SimulationZone

``` python
SimulationZone(items=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`delta_time`](#nodebpy.nodes.geometry.zone.SimulationZone.delta_time) |  |
| [`input`](#nodebpy.nodes.geometry.zone.SimulationZone.input) |  |
| [`items`](#nodebpy.nodes.geometry.zone.SimulationZone.items) | The zone’s state items. |
| [`output`](#nodebpy.nodes.geometry.zone.SimulationZone.output) |  |

### ZoneItem

``` python
ZoneItem(items, item)
```

Handle for a simulation/repeat state item (four sockets per item).

`initial` and `next` are the link targets; `>> item.initial` continues the chain from `current` and `>> item.next` from `result`, so a zone body can be written as one chain::

    g.Cube() >> geo.initial >> g.SetShadeSmooth() >> geo.next >> out

The type parameter is the socket class every role returns; the typed methods on `zone.items` produce parameterised handles such as `ZoneItem[GeometrySocket]`.

#### Attributes

| Name | Description |
|----|----|
| [`current`](#nodebpy.nodes.geometry.zone.ZoneItem.current) | Input-node output socket — read the item inside the zone body. |
| [`initial`](#nodebpy.nodes.geometry.zone.ZoneItem.initial) | Input-node input socket — set the item’s starting value. |
| [`input`](#nodebpy.nodes.geometry.zone.ZoneItem.input) | The socket the item is fed through. |
| [`name`](#nodebpy.nodes.geometry.zone.ZoneItem.name) |  |
| [`next`](#nodebpy.nodes.geometry.zone.ZoneItem.next) | Output-node input socket — write the item’s per-iteration result. |
| [`output`](#nodebpy.nodes.geometry.zone.ZoneItem.output) | The socket the item is read from. |
| [`result`](#nodebpy.nodes.geometry.zone.ZoneItem.result) | Output-node output socket — read the item after the zone. |
| [`socket_type`](#nodebpy.nodes.geometry.zone.ZoneItem.socket_type) |  |
