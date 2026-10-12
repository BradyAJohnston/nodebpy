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
| [add_item](#nodebpy.nodes.compositor.manual.IndexSwitch.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.compositor.manual.IndexSwitch.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.compositor.manual.IndexSwitch.boolean) |  |
| [capture](#nodebpy.nodes.compositor.manual.IndexSwitch.capture) | Deprecated: use `items.new(value, name).output`. |
| [color](#nodebpy.nodes.compositor.manual.IndexSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.IndexSwitch.float) |  |
| [font](#nodebpy.nodes.compositor.manual.IndexSwitch.font) |  |
| [integer](#nodebpy.nodes.compositor.manual.IndexSwitch.integer) |  |
| [integer_vector](#nodebpy.nodes.compositor.manual.IndexSwitch.integer_vector) |  |
| [matrix](#nodebpy.nodes.compositor.manual.IndexSwitch.matrix) |  |
| [menu](#nodebpy.nodes.compositor.manual.IndexSwitch.menu) |  |
| [object](#nodebpy.nodes.compositor.manual.IndexSwitch.object) |  |
| [rotation](#nodebpy.nodes.compositor.manual.IndexSwitch.rotation) |  |
| [string](#nodebpy.nodes.compositor.manual.IndexSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.IndexSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### boolean

``` python
boolean(index=0, items=())
```

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

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
| [add_item](#nodebpy.nodes.compositor.manual.MenuSwitch.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.compositor.manual.MenuSwitch.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.compositor.manual.MenuSwitch.boolean) |  |
| [capture](#nodebpy.nodes.compositor.manual.MenuSwitch.capture) | Deprecated: use `items.new(value, name).output`. |
| [color](#nodebpy.nodes.compositor.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.compositor.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.compositor.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [item](#nodebpy.nodes.compositor.manual.MenuSwitch.item) | Deprecated: use `items.new(value, name, description=)`. |
| [menu](#nodebpy.nodes.compositor.manual.MenuSwitch.menu) |  |
| [string](#nodebpy.nodes.compositor.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.MenuSwitch.vector) |  |

##### add_item

``` python
add_item(name, value=None, *, type=None)
```

Deprecated: use `items.new(value, name, type=)`.

##### add_items

``` python
add_items(items)
```

Deprecated: use `items.new(value, name)` per item.

##### boolean

``` python
boolean(menu=None, items=None)
```

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

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

##### item

``` python
item(name, value=None, *, description=None)
```

Deprecated: use `items.new(value, name, description=)`.

##### menu

``` python
menu(menu=None, items=None)
```

##### string

``` python
string(menu=None, items=None)
```

##### vector

``` python
vector(menu=None, items=None)
```
