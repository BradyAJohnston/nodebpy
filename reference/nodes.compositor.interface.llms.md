# nodes.compositor.interface

`interface`

## Classes

| Name | Description |
|----|----|
| [EnableOutput](#nodebpy.nodes.compositor.interface.EnableOutput) | Either pass through the input value or output the fallback value |

### EnableOutput

``` python
EnableOutput(enable=False, value=None, *, data_type='FLOAT')
```

Either pass through the input value or output the fallback value

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| enable | InputBoolean | Enable      | `False` |
| value  | InputFloat   | Value       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.interface.EnableOutput.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.interface.EnableOutput.i) |  |
| [`name`](#nodebpy.nodes.compositor.interface.EnableOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.interface.EnableOutput.node) |  |
| [`o`](#nodebpy.nodes.compositor.interface.EnableOutput.o) |  |
| [`tree`](#nodebpy.nodes.compositor.interface.EnableOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.interface.EnableOutput.boolean) | Create Enable Output with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.compositor.interface.EnableOutput.bundle) | Create Enable Output with operation ‘Bundle’. |
| [color](#nodebpy.nodes.compositor.interface.EnableOutput.color) | Create Enable Output with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.interface.EnableOutput.float) | Create Enable Output with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.interface.EnableOutput.font) | Create Enable Output with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.interface.EnableOutput.integer) | Create Enable Output with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.interface.EnableOutput.integer_vector) | Create Enable Output with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.interface.EnableOutput.matrix) | Create Enable Output with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.interface.EnableOutput.menu) | Create Enable Output with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.interface.EnableOutput.object) | Create Enable Output with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.interface.EnableOutput.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.interface.EnableOutput.rotation) | Create Enable Output with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.interface.EnableOutput.string) | Create Enable Output with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.interface.EnableOutput.vector) | Create Enable Output with operation ‘Vector’. |

##### boolean

``` python
boolean(enable=False, value=None)
```

Create Enable Output with operation ‘Boolean’.

##### bundle

``` python
bundle(enable=False, value=None)
```

Create Enable Output with operation ‘Bundle’.

##### color

``` python
color(enable=False, value=None)
```

Create Enable Output with operation ‘Color’.

##### float

``` python
float(enable=False, value=None)
```

Create Enable Output with operation ‘Float’.

##### font

``` python
font(enable=False, value=None)
```

Create Enable Output with operation ‘Font’.

##### integer

``` python
integer(enable=False, value=None)
```

Create Enable Output with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(enable=False, value=None)
```

Create Enable Output with operation ‘Integer Vector’.

##### matrix

``` python
matrix(enable=False, value=None)
```

Create Enable Output with operation ‘Matrix’.

##### menu

``` python
menu(enable=False, value=None)
```

Create Enable Output with operation ‘Menu’.

##### object

``` python
object(enable=False, value=None)
```

Create Enable Output with operation ‘Object’.

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

##### rotation

``` python
rotation(enable=False, value=None)
```

Create Enable Output with operation ‘Rotation’.

##### string

``` python
string(enable=False, value=None)
```

Create Enable Output with operation ‘String’.

##### vector

``` python
vector(enable=False, value=None)
```

Create Enable Output with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.enable` | `BooleanSocket` | Enable      |
| `i.value`  | `FloatSocket`   | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |
