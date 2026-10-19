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
| [add_item](#nodebpy.nodes.shader.manual.MenuSwitch.add_item) | Deprecated: use `items.new(value, name, type=)`. |
| [add_items](#nodebpy.nodes.shader.manual.MenuSwitch.add_items) | Deprecated: use `items.new(value, name)` per item. |
| [boolean](#nodebpy.nodes.shader.manual.MenuSwitch.boolean) |  |
| [bundle](#nodebpy.nodes.shader.manual.MenuSwitch.bundle) |  |
| [capture](#nodebpy.nodes.shader.manual.MenuSwitch.capture) | Deprecated: use `items.new(value, name).output`. |
| [closure](#nodebpy.nodes.shader.manual.MenuSwitch.closure) |  |
| [color](#nodebpy.nodes.shader.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.shader.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.shader.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.shader.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [item](#nodebpy.nodes.shader.manual.MenuSwitch.item) | Deprecated: use `items.new(value, name, description=)`. |
| [menu](#nodebpy.nodes.shader.manual.MenuSwitch.menu) |  |
| [shader](#nodebpy.nodes.shader.manual.MenuSwitch.shader) |  |
| [vector](#nodebpy.nodes.shader.manual.MenuSwitch.vector) |  |

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

##### bundle

``` python
bundle(menu=None, items=None)
```

##### capture

``` python
capture(value, *, name=None)
```

Deprecated: use `items.new(value, name).output`.

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

##### item

``` python
item(name, value=None, *, description=None)
```

Deprecated: use `items.new(value, name, description=)`.

##### menu

``` python
menu(menu=None, items=None)
```

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
