# nodes.compositor.manual

`manual`

## Attributes

| Name                                            | Description |
|-------------------------------------------------|-------------|
| [`tree`](#nodebpy.nodes.compositor.manual.tree) |             |

## Classes

| Name | Description |
|----|----|
| [IndexSwitch](#nodebpy.nodes.compositor.manual.IndexSwitch) | Node builder for the Index Switch node (Compositor tree). |
| [MenuSwitch](#nodebpy.nodes.compositor.manual.MenuSwitch) | Node builder for the Menu Switch node (Compositor tree) |

### IndexSwitch

``` python
IndexSwitch(index=0, items=(), data_type=None)
```

Node builder for the Index Switch node (Compositor tree).

The same node as in Geometry Nodes, with the same items API and type inference, but the compositor switches fewer types (and Integer Vector, which Geometry Nodes doesn’t). With nothing to infer from it is a Color switch, as Blender starts it in the compositor.

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.manual.IndexSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.compositor.manual.IndexSwitch.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`items`](#nodebpy.nodes.compositor.manual.IndexSwitch.items) | The switch’s items, one input socket each. |
| [`name`](#nodebpy.nodes.compositor.manual.IndexSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.manual.IndexSwitch.node) |  |
| [`o`](#nodebpy.nodes.compositor.manual.IndexSwitch.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.nodes.compositor.manual.IndexSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.manual.IndexSwitch.boolean) |  |
| [color](#nodebpy.nodes.compositor.manual.IndexSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.IndexSwitch.float) |  |
| [font](#nodebpy.nodes.compositor.manual.IndexSwitch.font) |  |
| [integer](#nodebpy.nodes.compositor.manual.IndexSwitch.integer) |  |
| [integer_vector](#nodebpy.nodes.compositor.manual.IndexSwitch.integer_vector) |  |
| [matrix](#nodebpy.nodes.compositor.manual.IndexSwitch.matrix) |  |
| [menu](#nodebpy.nodes.compositor.manual.IndexSwitch.menu) |  |
| [object](#nodebpy.nodes.compositor.manual.IndexSwitch.object) |  |
| [props](#nodebpy.nodes.compositor.manual.IndexSwitch.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.manual.IndexSwitch.rotation) |  |
| [string](#nodebpy.nodes.compositor.manual.IndexSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.IndexSwitch.vector) |  |

##### boolean

``` python
boolean(index=0, items=())
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

##### integer

``` python
integer(index=0, items=())
```

##### integer_vector

``` python
integer_vector(index=0, items=())
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

### MenuSwitch

``` python
MenuSwitch(menu=None, items=None, *, data_type=None)
```

Node builder for the Menu Switch node (Compositor tree)

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.compositor.manual.MenuSwitch.i) |  |
| [`items`](#nodebpy.nodes.compositor.manual.MenuSwitch.items) | The menu’s items, one input socket each. |
| [`name`](#nodebpy.nodes.compositor.manual.MenuSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.compositor.manual.MenuSwitch.o) |  |
| [`tree`](#nodebpy.nodes.compositor.manual.MenuSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.manual.MenuSwitch.boolean) |  |
| [color](#nodebpy.nodes.compositor.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.compositor.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.compositor.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [menu](#nodebpy.nodes.compositor.manual.MenuSwitch.menu) |  |
| [props](#nodebpy.nodes.compositor.manual.MenuSwitch.props) | Set the properties every node has and return the node, so it can |
| [string](#nodebpy.nodes.compositor.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.MenuSwitch.vector) |  |

##### boolean

``` python
boolean(menu=None, items=None)
```

##### color

``` python
color(menu=None, items=None)
```

##### float

``` python
float(menu=None, items=None)
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

##### menu

``` python
menu(menu=None, items=None)
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

##### string

``` python
string(menu=None, items=None)
```

##### vector

``` python
vector(menu=None, items=None)
```
