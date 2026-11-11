# nodes.shader.manual

`manual`

## Attributes

| Name                                        | Description |
|---------------------------------------------|-------------|
| [`tree`](#nodebpy.nodes.shader.manual.tree) |             |

## Classes

| Name | Description |
|----|----|
| [MenuSwitch](#nodebpy.nodes.shader.manual.MenuSwitch) | Node builder for the Menu Switch node (Shader tree) |

### MenuSwitch

``` python
MenuSwitch(menu=None, items=None, *, data_type=None)
```

Node builder for the Menu Switch node (Shader tree)

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.shader.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.shader.manual.MenuSwitch.i) |  |
| [`items`](#nodebpy.nodes.shader.manual.MenuSwitch.items) | The menu’s items, one input socket each. |
| [`name`](#nodebpy.nodes.shader.manual.MenuSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.shader.manual.MenuSwitch.o) |  |
| [`tree`](#nodebpy.nodes.shader.manual.MenuSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.shader.manual.MenuSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.shader.manual.MenuSwitch.bundle) |  |
| [closure](#nodebpy.nodes.shader.manual.MenuSwitch.closure) |  |
| [color](#nodebpy.nodes.shader.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.shader.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.shader.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.shader.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [menu](#nodebpy.nodes.shader.manual.MenuSwitch.menu) |  |
| [props](#nodebpy.nodes.shader.manual.MenuSwitch.props) | Set the properties every node has and return the node, so it can |
| [shader](#nodebpy.nodes.shader.manual.MenuSwitch.shader) |  |
| [vector](#nodebpy.nodes.shader.manual.MenuSwitch.vector) |  |

##### boolean

``` python
boolean(menu=None, items=None)
```

##### bundle

``` python
bundle(menu=None, items=None)
```

##### closure

``` python
closure(menu=None, items=None)
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

##### shader

``` python
shader(menu=None, items=None)
```

##### vector

``` python
vector(menu=None, items=None)
```

## Functions

| Name | Description |
|----|----|
| [material](#nodebpy.nodes.shader.manual.material) |  |
| [world](#nodebpy.nodes.shader.manual.world) | Build a world’s node tree; `scene=True` makes it the active scene’s world. |

### material

``` python
material(
    name='New Material',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
    clear=False,
    keep_edits=None,
)
```

### world

``` python
world(
    name='World',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
    clear=False,
    keep_edits=None,
    scene=False,
)
```

Build a world’s node tree; `scene=True` makes it the active scene’s world.

`with s.world("Studio", clear=True, scene=True):` then add a Background linked into a World Output, as in a material.
