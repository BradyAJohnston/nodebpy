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
