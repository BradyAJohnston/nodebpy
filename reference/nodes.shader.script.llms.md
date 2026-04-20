# nodes.shader.script

`script`

## Classes

| Name | Description |
|----|----|
| [Script](#nodebpy.nodes.shader.script.Script) | Generate an OSL shader from a file or text data-block. |

### Script

``` python
Script(
    filepath='',
    mode='INTERNAL',
    use_auto_update=False,
    bytecode='',
    bytecode_hash='',
)
```

    Generate an OSL shader from a file or text data-block.

Note: OSL shaders are not supported on all GPU backends

#### Attributes

| Name | Description |
|----|----|
| [`bytecode`](#nodebpy.nodes.shader.script.Script.bytecode) |  |
| [`bytecode_hash`](#nodebpy.nodes.shader.script.Script.bytecode_hash) |  |
| [`filepath`](#nodebpy.nodes.shader.script.Script.filepath) |  |
| [`i`](#nodebpy.nodes.shader.script.Script.i) |  |
| [`inputs`](#nodebpy.nodes.shader.script.Script.inputs) |  |
| [`mode`](#nodebpy.nodes.shader.script.Script.mode) |  |
| [`name`](#nodebpy.nodes.shader.script.Script.name) |  |
| [`node`](#nodebpy.nodes.shader.script.Script.node) |  |
| [`o`](#nodebpy.nodes.shader.script.Script.o) |  |
| [`outputs`](#nodebpy.nodes.shader.script.Script.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.script.Script.tree) |  |
| [`type`](#nodebpy.nodes.shader.script.Script.type) |  |
| [`use_auto_update`](#nodebpy.nodes.shader.script.Script.use_auto_update) |  |

#### Methods

| Name | Description |
|----|----|
| [external](#nodebpy.nodes.shader.script.Script.external) | Create Script with operation ‘External’. Use external .osl or .oso file |
| [internal](#nodebpy.nodes.shader.script.Script.internal) | Create Script with operation ‘Internal’. Use internal text data-block |

##### external

``` python
external()
```

Create Script with operation ‘External’. Use external .osl or .oso file

##### internal

``` python
internal()
```

Create Script with operation ‘Internal’. Use internal text data-block
