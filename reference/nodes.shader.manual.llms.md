# nodes.shader.manual

`manual`

## Classes

| Name | Description |
|----|----|
| [Attribute](#nodebpy.nodes.shader.manual.Attribute) | Retrieve attributes attached to objects or geometry |
| [MenuSwitch](#nodebpy.nodes.shader.manual.MenuSwitch) | Node builder for the Menu Switch node (Shader tree) |

### Attribute

``` python
Attribute(attribute_type='GEOMETRY', attribute_name='')
```

Retrieve attributes attached to objects or geometry

#### Attributes

| Name | Description |
|----|----|
| [`attribute_name`](#nodebpy.nodes.shader.manual.Attribute.attribute_name) |  |
| [`attribute_type`](#nodebpy.nodes.shader.manual.Attribute.attribute_type) |  |
| [`i`](#nodebpy.nodes.shader.manual.Attribute.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.shader.manual.Attribute.name) |  |
| [`node`](#nodebpy.nodes.shader.manual.Attribute.node) |  |
| [`o`](#nodebpy.nodes.shader.manual.Attribute.o) |  |
| [`outputs`](#nodebpy.nodes.shader.manual.Attribute.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.manual.Attribute.tree) |  |
| [`type`](#nodebpy.nodes.shader.manual.Attribute.type) |  |

#### Methods

| Name | Description |
|----|----|
| [geometry](#nodebpy.nodes.shader.manual.Attribute.geometry) | Create Attribute with operation ‘Geometry’. |
| [instancer](#nodebpy.nodes.shader.manual.Attribute.instancer) | Create Attribute with operation ‘Instancer’. |
| [object](#nodebpy.nodes.shader.manual.Attribute.object) | Create Attribute with operation ‘Object’. |
| [view_layer](#nodebpy.nodes.shader.manual.Attribute.view_layer) | Create Attribute with operation ‘View Layer’. |

##### geometry

``` python
geometry(attribute_name='')
```

Create Attribute with operation ‘Geometry’.

##### instancer

``` python
instancer(attribute_name='')
```

Create Attribute with operation ‘Instancer’.

##### object

``` python
object(attribute_name='')
```

Create Attribute with operation ‘Object’.

##### view_layer

``` python
view_layer(attribute_name='')
```

Create Attribute with operation ‘View Layer’.

### MenuSwitch

``` python
MenuSwitch(menu=None, items={}, *, data_type='FLOAT')
```

Node builder for the Menu Switch node (Shader tree)

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.shader.manual.MenuSwitch.data_type) | Input socket: Data Type |
| [`i`](#nodebpy.nodes.shader.manual.MenuSwitch.i) |  |
| [`name`](#nodebpy.nodes.shader.manual.MenuSwitch.name) |  |
| [`node`](#nodebpy.nodes.shader.manual.MenuSwitch.node) |  |
| [`o`](#nodebpy.nodes.shader.manual.MenuSwitch.o) |  |
| [`outputs`](#nodebpy.nodes.shader.manual.MenuSwitch.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.manual.MenuSwitch.tree) |  |
| [`type`](#nodebpy.nodes.shader.manual.MenuSwitch.type) |  |

#### Methods

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [boolean](#nodebpy.nodes.shader.manual.MenuSwitch.boolean) |             |
| [bundle](#nodebpy.nodes.shader.manual.MenuSwitch.bundle)   |             |
| [closure](#nodebpy.nodes.shader.manual.MenuSwitch.closure) |             |
| [color](#nodebpy.nodes.shader.manual.MenuSwitch.color)     |             |
| [float](#nodebpy.nodes.shader.manual.MenuSwitch.float)     |             |
| [integer](#nodebpy.nodes.shader.manual.MenuSwitch.integer) |             |
| [menu](#nodebpy.nodes.shader.manual.MenuSwitch.menu)       |             |
| [shader](#nodebpy.nodes.shader.manual.MenuSwitch.shader)   |             |
| [vector](#nodebpy.nodes.shader.manual.MenuSwitch.vector)   |             |

##### boolean

``` python
boolean(menu=None, items={})
```

##### bundle

``` python
bundle(menu=None, items={})
```

##### closure

``` python
closure(menu=None, items={})
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

##### shader

``` python
shader(menu=None, items={})
```

##### vector

``` python
vector(menu=None, items={})
```

## Functions

| Name                                              | Description |
|---------------------------------------------------|-------------|
| [material](#nodebpy.nodes.shader.manual.material) |             |
| [tree](#nodebpy.nodes.shader.manual.tree)         |             |

### material

``` python
material(
    name='New Material',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```

### tree

``` python
tree(
    name='Shader Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```
