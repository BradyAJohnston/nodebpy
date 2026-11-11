# nodes.shader.script

`script`

## Classes

| Name | Description |
|----|----|
| [Script](#nodebpy.nodes.shader.script.Script) | Generate an OSL shader from a file or text data-block. |

### Script

``` python
Script(
    script=None,
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
| [`mode`](#nodebpy.nodes.shader.script.Script.mode) |  |
| [`name`](#nodebpy.nodes.shader.script.Script.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.script.Script.node) |  |
| [`o`](#nodebpy.nodes.shader.script.Script.o) |  |
| [`script`](#nodebpy.nodes.shader.script.Script.script) |  |
| [`tree`](#nodebpy.nodes.shader.script.Script.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`use_auto_update`](#nodebpy.nodes.shader.script.Script.use_auto_update) |  |

#### Methods

| Name | Description |
|----|----|
| [external](#nodebpy.nodes.shader.script.Script.external) | Create Script with operation ‘External’. Use external .osl or .oso file |
| [internal](#nodebpy.nodes.shader.script.Script.internal) | Create Script with operation ‘Internal’. Use internal text data-block |
| [props](#nodebpy.nodes.shader.script.Script.props) | Set the properties every node has and return the node, so it can |

##### external

``` python
external(filepath='', use_auto_update=False, bytecode='', bytecode_hash='')
```

Create Script with operation ‘External’. Use external .osl or .oso file

##### internal

``` python
internal(script=None, bytecode='', bytecode_hash='')
```

Create Script with operation ‘Internal’. Use internal text data-block

##### props

``` python
props(
    label=None,
    color=None,
    width=None,
    height=None,
    hide=None,
    show_options=None,
    hide_inputs=(),
    hide_outputs=(),
    mute=None,
    warning_propagation=None,
    pin_gizmo=None,
    pin_gizmo_inputs=(),
)
```

Set the properties every node has and return the node, so it can go at the end of a chain::

    g.SetPosition(geometry=geo, offset=offset).props(
        label="Lift", color="#FFAA00", width=200
    )

Properties left as `None` are unchanged.

Args: label: The node’s header label. color: A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple; turns on `use_custom_color`. width: The node’s width. height: The node’s height; only frames use it. hide: Collapse the node. show_options: Show the node’s options (dropdowns and toggles). hide_inputs: Input sockets to hide, by name; `"Value#1"` names the second visible `Value`. hide_outputs: Output sockets to hide, by name. mute: Mute (bypass) the node. warning_propagation: Which of the node’s warnings show on the group node it sits in. pin_gizmo: Keep the node’s gizmo visible when it isn’t selected: a gizmo node’s, or a value node’s (Value, Vector, …). pin_gizmo_inputs: Inputs whose gizmos stay visible when the node isn’t selected, by name; for group nodes passing a gizmo through.
