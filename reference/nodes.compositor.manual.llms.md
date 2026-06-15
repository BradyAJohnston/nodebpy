# nodes.compositor.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [MenuSwitch](#nodebpy.nodes.compositor.manual.MenuSwitch) | Node builder for the Menu Switch node (Compositor tree) |

### MenuSwitch

``` python
MenuSwitch(menu=None, items=None, *, data_type='FLOAT')
```

Node builder for the Menu Switch node (Compositor tree)

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.compositor.manual.MenuSwitch.i) |  |
| [`name`](#nodebpy.nodes.compositor.manual.MenuSwitch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.compositor.manual.MenuSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.manual.MenuSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.manual.MenuSwitch.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [add_item](#nodebpy.nodes.compositor.manual.MenuSwitch.add_item) | Add a single item and return its handle. |
| [add_items](#nodebpy.nodes.compositor.manual.MenuSwitch.add_items) | Add an item per mapping entry and return their handles by name. |
| [boolean](#nodebpy.nodes.compositor.manual.MenuSwitch.boolean) |  |
| [capture](#nodebpy.nodes.compositor.manual.MenuSwitch.capture) | Add an item linked from `value` and return its output socket. |
| [color](#nodebpy.nodes.compositor.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.compositor.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.compositor.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [menu](#nodebpy.nodes.compositor.manual.MenuSwitch.menu) |  |
| [string](#nodebpy.nodes.compositor.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.MenuSwitch.vector) |  |

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

##### boolean

``` python
boolean(menu=None, items={})
```

##### capture

``` python
capture(value, *, name=None)
```

Add an item linked from `value` and return its output socket.

The item is auto-named after the source socket unless `name` is given.

##### color

``` python
color(menu=None, items={})
```

##### float

``` python
float(menu=None, items={})
```

##### integer

``` python
integer(menu=None, items={})
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
menu(menu=None, items={})
```

##### string

``` python
string(menu=None, items={})
```

##### vector

``` python
vector(menu=None, items={})
```

## Functions

| Name                                          | Description |
|-----------------------------------------------|-------------|
| [tree](#nodebpy.nodes.compositor.manual.tree) |             |

### tree

``` python
tree(
    name='Compositor Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```
