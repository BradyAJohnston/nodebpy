# builder.node

`node`

## Classes

| Name | Description |
|----|----|
| [BaseNode](#nodebpy.builder.node.BaseNode) | Base class for all node wrappers. |
| [CustomCompositorGroup](#nodebpy.builder.node.CustomCompositorGroup) | Node group in a Compositor node tree. |
| [CustomGeometryGroup](#nodebpy.builder.node.CustomGeometryGroup) | Node group in a Geometry Nodes tree. |
| [CustomShaderGroup](#nodebpy.builder.node.CustomShaderGroup) | Node group in a Shader (Material) node tree. |
| [DynamicInputsMixin](#nodebpy.builder.node.DynamicInputsMixin) |  |
| [NodeGroupBuilder](#nodebpy.builder.node.NodeGroupBuilder) | Base class for custom node groups. |

### BaseNode

``` python
BaseNode(node=None)
```

Base class for all node wrappers.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.BaseNode.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.BaseNode.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.node.BaseNode.node) |  |
| [`o`](#nodebpy.builder.node.BaseNode.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.node.BaseNode.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.builder.node.BaseNode.props) | Set the properties every node has and return the node, so it can |

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

### CustomCompositorGroup

``` python
CustomCompositorGroup(**kwargs)
```

Node group in a Compositor node tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomCompositorGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomCompositorGroup.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.node.CustomCompositorGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomCompositorGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomCompositorGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.node.CustomCompositorGroup.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.builder.node.CustomCompositorGroup.create_group) | Build this group’s node tree and return it, reusing an existing tree |
| [props](#nodebpy.builder.node.CustomCompositorGroup.props) | Set the properties every node has and return the node, so it can |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

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

### CustomGeometryGroup

``` python
CustomGeometryGroup(**kwargs)
```

Node group in a Geometry Nodes tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomGeometryGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomGeometryGroup.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.node.CustomGeometryGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomGeometryGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomGeometryGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.node.CustomGeometryGroup.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.builder.node.CustomGeometryGroup.create_group) | Build this group’s node tree and return it, reusing an existing tree |
| [props](#nodebpy.builder.node.CustomGeometryGroup.props) | Set the properties every node has and return the node, so it can |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

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

### CustomShaderGroup

``` python
CustomShaderGroup(**kwargs)
```

Node group in a Shader (Material) node tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomShaderGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomShaderGroup.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.node.CustomShaderGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomShaderGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomShaderGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.node.CustomShaderGroup.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.builder.node.CustomShaderGroup.create_group) | Build this group’s node tree and return it, reusing an existing tree |
| [props](#nodebpy.builder.node.CustomShaderGroup.props) | Set the properties every node has and return the node, so it can |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

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

### DynamicInputsMixin

``` python
DynamicInputsMixin()
```

### NodeGroupBuilder

``` python
NodeGroupBuilder(**kwargs)
```

Base class for custom node groups.

Subclasses implement :meth:`_build_group` with the node-graph logic. Subclass one of the editor-specific variants: :class:`GeometryNodeGroup`, :class:`ShaderNodeGroup`, or :class:`CompositorNodeGroup`.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.NodeGroupBuilder.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.NodeGroupBuilder.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.node.NodeGroupBuilder.node) |  |
| [`node_tree`](#nodebpy.builder.node.NodeGroupBuilder.node_tree) | The internal node tree for this group node. |
| [`o`](#nodebpy.builder.node.NodeGroupBuilder.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`tree`](#nodebpy.builder.node.NodeGroupBuilder.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.builder.node.NodeGroupBuilder.create_group) | Build this group’s node tree and return it, reusing an existing tree |
| [props](#nodebpy.builder.node.NodeGroupBuilder.props) | Set the properties every node has and return the node, so it can |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

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
