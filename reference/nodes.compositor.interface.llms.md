# nodes.compositor.interface

`interface`

## Classes

| Name | Description |
|----|----|
| [EnableOutput](#nodebpy.nodes.compositor.interface.EnableOutput) | Either pass through the input value or output the fallback value |

### EnableOutput

``` python
EnableOutput(enable=False, value=0.0, *, data_type='FLOAT')
```

Either pass through the input value or output the fallback value

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| enable | InputBoolean | Enable      | `False` |
| value  | InputFloat   | Value       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.interface.EnableOutput.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.interface.EnableOutput.i) |  |
| [`name`](#nodebpy.nodes.compositor.interface.EnableOutput.name) |  |
| [`node`](#nodebpy.nodes.compositor.interface.EnableOutput.node) |  |
| [`o`](#nodebpy.nodes.compositor.interface.EnableOutput.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.interface.EnableOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.interface.EnableOutput.tree) |  |
| [`type`](#nodebpy.nodes.compositor.interface.EnableOutput.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.interface.EnableOutput.boolean) | Create Enable Output with operation ‘Boolean’. |
| [color](#nodebpy.nodes.compositor.interface.EnableOutput.color) | Create Enable Output with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.interface.EnableOutput.float) | Create Enable Output with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.interface.EnableOutput.font) | Create Enable Output with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.interface.EnableOutput.integer) | Create Enable Output with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.interface.EnableOutput.integer_vector) | Create Enable Output with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.interface.EnableOutput.matrix) | Create Enable Output with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.interface.EnableOutput.menu) | Create Enable Output with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.interface.EnableOutput.object) | Create Enable Output with operation ‘Object’. |
| [rotation](#nodebpy.nodes.compositor.interface.EnableOutput.rotation) | Create Enable Output with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.interface.EnableOutput.string) | Create Enable Output with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.interface.EnableOutput.vector) | Create Enable Output with operation ‘Vector’. |

##### boolean

``` python
boolean(enable=False, value=False)
```

Create Enable Output with operation ‘Boolean’.

##### color

``` python
color(enable=False, value=None)
```

Create Enable Output with operation ‘Color’.

##### float

``` python
float(enable=False, value=0.0)
```

Create Enable Output with operation ‘Float’.

##### font

``` python
font(enable=False, value=None)
```

Create Enable Output with operation ‘Font’.

##### integer

``` python
integer(enable=False, value=0)
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

##### rotation

``` python
rotation(enable=False, value=None)
```

Create Enable Output with operation ‘Rotation’.

##### string

``` python
string(enable=False, value='')
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
