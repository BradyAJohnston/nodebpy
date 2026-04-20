# nodes.compositor.vector

`vector`

## Classes

| Name | Description |
|----|----|
| [Normalize](#nodebpy.nodes.compositor.vector.Normalize) | Map values to 0 to 1 range, based on the minimum and maximum pixel values |

### Normalize

``` python
Normalize(value=1.0)
```

Map values to 0 to 1 range, based on the minimum and maximum pixel values

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| value | InputFloat | Value       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.vector.Normalize.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.vector.Normalize.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.vector.Normalize.name) |  |
| [`node`](#nodebpy.nodes.compositor.vector.Normalize.node) |  |
| [`o`](#nodebpy.nodes.compositor.vector.Normalize.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.vector.Normalize.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.vector.Normalize.tree) |  |
| [`type`](#nodebpy.nodes.compositor.vector.Normalize.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.value` | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |
