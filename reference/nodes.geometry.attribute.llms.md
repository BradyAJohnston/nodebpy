# nodes.geometry.attribute

`attribute`

## Classes

| Name | Description |
|----|----|
| [BlurAttribute](#nodebpy.nodes.geometry.attribute.BlurAttribute) | Mix attribute values of neighboring elements |
| [DomainSize](#nodebpy.nodes.geometry.attribute.DomainSize) | Retrieve the number of elements in a geometry for each attribute domain |
| [GetAttributeNames](#nodebpy.nodes.geometry.attribute.GetAttributeNames) | Retrieves attribute names as a list of strings |
| [RemoveNamedAttribute](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute) | Delete an attribute with a specified name from a geometry. Typically used to optimize performance |

### BlurAttribute

``` python
BlurAttribute(value=None, iterations=1, weight=1.0, *, data_type='FLOAT')
```

Mix attribute values of neighboring elements

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| value      | InputFloat   | Value       | `None`  |
| iterations | InputInteger | Iterations  | `1`     |
| weight     | InputFloat   | Weight      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.attribute.BlurAttribute.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.attribute.BlurAttribute.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.BlurAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.attribute.BlurAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.BlurAttribute.o) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.BlurAttribute.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [color](#nodebpy.nodes.geometry.attribute.BlurAttribute.color) | Create Blur Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.attribute.BlurAttribute.float) | Create Blur Attribute with operation ‘Float’. Floating-point value |
| [integer](#nodebpy.nodes.geometry.attribute.BlurAttribute.integer) | Create Blur Attribute with operation ‘Integer’. 32-bit integer |
| [props](#nodebpy.nodes.geometry.attribute.BlurAttribute.props) | Set the properties every node has and return the node, so it can |
| [vector](#nodebpy.nodes.geometry.attribute.BlurAttribute.vector) | Create Blur Attribute with operation ‘Vector’. 3D vector with floating-point values |

##### color

``` python
color(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Float’. Floating-point value

##### integer

``` python
integer(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Integer’. 32-bit integer

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

##### vector

``` python
vector(value=None, iterations=1, weight=1.0)
```

Create Blur Attribute with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.value`      | `FloatSocket`   | Value       |
| `i.iterations` | `IntegerSocket` | Iterations  |
| `i.weight`     | `FloatSocket`   | Weight      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### DomainSize

``` python
DomainSize(geometry=None, *, component='MESH')
```

Retrieve the number of elements in a geometry for each attribute domain

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`component`](#nodebpy.nodes.geometry.attribute.DomainSize.component) |  |
| [`i`](#nodebpy.nodes.geometry.attribute.DomainSize.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.DomainSize.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.attribute.DomainSize.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.DomainSize.o) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.DomainSize.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.attribute.DomainSize.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |

**Outputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `o.point_count`       | `IntegerSocket` | Point Count       |
| `o.edge_count`        | `IntegerSocket` | Edge Count        |
| `o.face_count`        | `IntegerSocket` | Face Count        |
| `o.face_corner_count` | `IntegerSocket` | Face Corner Count |
| `o.spline_count`      | `IntegerSocket` | Spline Count      |
| `o.instance_count`    | `IntegerSocket` | Instance Count    |
| `o.layer_count`       | `IntegerSocket` | Layer Count       |

### GetAttributeNames

``` python
GetAttributeNames(
    geometry=None,
    filter_data_type=False,
    data_type='Float',
    filter_domain=False,
    domain='Point',
)
```

Retrieves attribute names as a list of strings

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| geometry | InputGeometry | Geometry | `None` |
| filter_data_type | InputBoolean | Filter Data Type | `False` |
| data_type | InputMenu \| Literal\['Float', 'Integer', 'Boolean', 'Vector', 'Color', 'Quaternion', '4x4 Matrix', 'String', '8-Bit Integer', '2D 16-Bit Integer Vector', '2D Integer Vector', '2D Vector', '4D Vector', 'Byte Color'\] | Data Type | `'Float'` |
| filter_domain | InputBoolean | Filter Domain | `False` |
| domain | InputMenu \| Literal\['Point', 'Edge', 'Face', 'Face Corner', 'Spline', 'Instance', 'Layer'\] | Domain | `'Point'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.attribute.GetAttributeNames.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.GetAttributeNames.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.attribute.GetAttributeNames.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.GetAttributeNames.o) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.GetAttributeNames.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.attribute.GetAttributeNames.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute            | Type             | Description      |
|----------------------|------------------|------------------|
| `i.geometry`         | `GeometrySocket` | Geometry         |
| `i.filter_data_type` | `BooleanSocket`  | Filter Data Type |
| `i.data_type`        | `MenuSocket`     | Data Type        |
| `i.filter_domain`    | `BooleanSocket`  | Filter Domain    |
| `i.domain`           | `MenuSocket`     | Domain           |

**Outputs**

| Attribute | Type               | Description |
|-----------|--------------------|-------------|
| `o.names` | `StringSocketList` | Names       |

### RemoveNamedAttribute

``` python
RemoveNamedAttribute(geometry=None, pattern_mode='Exact', name='')
```

Delete an attribute with a specified name from a geometry. Typically used to optimize performance

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| geometry | InputGeometry | Geometry | `None` |
| pattern_mode | InputMenu \| Literal\['Exact', 'Wildcard'\] | Pattern Mode | `'Exact'` |
| name | InputString | Name | `''` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.i) |  |
| [`name`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.o) |  |
| [`tree`](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.geometry.attribute.RemoveNamedAttribute.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.geometry`     | `GeometrySocket` | Geometry     |
| `i.pattern_mode` | `MenuSocket`     | Pattern Mode |
| `i.name`         | `StringSocket`   | Name         |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |
