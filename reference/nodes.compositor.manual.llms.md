# nodes.compositor.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [MenuSwitch](#nodebpy.nodes.compositor.manual.MenuSwitch) | Node builder for the Menu Switch node (Compositor tree) |

### MenuSwitch

``` python
MenuSwitch(menu=None, items={}, *, data_type='FLOAT')
```

Node builder for the Menu Switch node (Compositor tree)

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.compositor.manual.MenuSwitch.i) |  |
| [`name`](#nodebpy.nodes.compositor.manual.MenuSwitch.name) |  |
| [`node`](#nodebpy.nodes.compositor.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.compositor.manual.MenuSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.manual.MenuSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.manual.MenuSwitch.tree) |  |
| [`type`](#nodebpy.nodes.compositor.manual.MenuSwitch.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.manual.MenuSwitch.boolean) |  |
| [color](#nodebpy.nodes.compositor.manual.MenuSwitch.color) |  |
| [float](#nodebpy.nodes.compositor.manual.MenuSwitch.float) |  |
| [integer](#nodebpy.nodes.compositor.manual.MenuSwitch.integer) |  |
| [is_selected](#nodebpy.nodes.compositor.manual.MenuSwitch.is_selected) | Gets the boolean output socket that is True when the named menu item is selected. |
| [menu](#nodebpy.nodes.compositor.manual.MenuSwitch.menu) |  |
| [string](#nodebpy.nodes.compositor.manual.MenuSwitch.string) |  |
| [vector](#nodebpy.nodes.compositor.manual.MenuSwitch.vector) |  |

##### boolean

``` python
boolean(menu=None, items={})
```

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
