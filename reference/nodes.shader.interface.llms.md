# nodes.shader.interface

`interface`

## Classes

| Name | Description |
|----|----|
| [ClosureInput](#nodebpy.nodes.shader.interface.ClosureInput) | Closure Input node |
| [ClosureOutput](#nodebpy.nodes.shader.interface.ClosureOutput) | Closure Output node |

### ClosureInput

``` python
ClosureInput()
```

Closure Input node

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.interface.ClosureInput.i) |  |
| [`inputs`](#nodebpy.nodes.shader.interface.ClosureInput.inputs) |  |
| [`name`](#nodebpy.nodes.shader.interface.ClosureInput.name) |  |
| [`node`](#nodebpy.nodes.shader.interface.ClosureInput.node) |  |
| [`o`](#nodebpy.nodes.shader.interface.ClosureInput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.interface.ClosureInput.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.interface.ClosureInput.tree) |  |
| [`type`](#nodebpy.nodes.shader.interface.ClosureInput.type) |  |

### ClosureOutput

``` python
ClosureOutput(
    active_input_index=0,
    active_output_index=0,
    define_signature=False,
)
```

Closure Output node

#### Attributes

| Name | Description |
|----|----|
| [`active_input_index`](#nodebpy.nodes.shader.interface.ClosureOutput.active_input_index) |  |
| [`active_output_index`](#nodebpy.nodes.shader.interface.ClosureOutput.active_output_index) |  |
| [`define_signature`](#nodebpy.nodes.shader.interface.ClosureOutput.define_signature) |  |
| [`i`](#nodebpy.nodes.shader.interface.ClosureOutput.i) |  |
| [`inputs`](#nodebpy.nodes.shader.interface.ClosureOutput.inputs) |  |
| [`name`](#nodebpy.nodes.shader.interface.ClosureOutput.name) |  |
| [`node`](#nodebpy.nodes.shader.interface.ClosureOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.interface.ClosureOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.interface.ClosureOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.interface.ClosureOutput.tree) |  |
| [`type`](#nodebpy.nodes.shader.interface.ClosureOutput.type) |  |

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.closure` | `ClosureSocket` | Closure     |
