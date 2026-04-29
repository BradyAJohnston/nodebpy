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
| [`name`](#nodebpy.builder.node.BaseNode.name) |  |
| [`node`](#nodebpy.builder.node.BaseNode.node) |  |
| [`o`](#nodebpy.builder.node.BaseNode.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.node.BaseNode.outputs) |  |
| [`tree`](#nodebpy.builder.node.BaseNode.tree) |  |
| [`type`](#nodebpy.builder.node.BaseNode.type) |  |

### CustomCompositorGroup

``` python
CustomCompositorGroup(**kwargs)
```

Node group in a Compositor node tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomCompositorGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomCompositorGroup.name) |  |
| [`node`](#nodebpy.builder.node.CustomCompositorGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomCompositorGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomCompositorGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.node.CustomCompositorGroup.outputs) |  |
| [`tree`](#nodebpy.builder.node.CustomCompositorGroup.tree) |  |
| [`type`](#nodebpy.builder.node.CustomCompositorGroup.type) |  |

### CustomGeometryGroup

``` python
CustomGeometryGroup(**kwargs)
```

Node group in a Geometry Nodes tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomGeometryGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomGeometryGroup.name) |  |
| [`node`](#nodebpy.builder.node.CustomGeometryGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomGeometryGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomGeometryGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.node.CustomGeometryGroup.outputs) |  |
| [`tree`](#nodebpy.builder.node.CustomGeometryGroup.tree) |  |
| [`type`](#nodebpy.builder.node.CustomGeometryGroup.type) |  |

### CustomShaderGroup

``` python
CustomShaderGroup(**kwargs)
```

Node group in a Shader (Material) node tree.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.node.CustomShaderGroup.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.node.CustomShaderGroup.name) |  |
| [`node`](#nodebpy.builder.node.CustomShaderGroup.node) |  |
| [`node_tree`](#nodebpy.builder.node.CustomShaderGroup.node_tree) |  |
| [`o`](#nodebpy.builder.node.CustomShaderGroup.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.node.CustomShaderGroup.outputs) |  |
| [`tree`](#nodebpy.builder.node.CustomShaderGroup.tree) |  |
| [`type`](#nodebpy.builder.node.CustomShaderGroup.type) |  |

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
| [`name`](#nodebpy.builder.node.NodeGroupBuilder.name) |  |
| [`node`](#nodebpy.builder.node.NodeGroupBuilder.node) |  |
| [`node_tree`](#nodebpy.builder.node.NodeGroupBuilder.node_tree) | The internal node tree for this group node. |
| [`o`](#nodebpy.builder.node.NodeGroupBuilder.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.node.NodeGroupBuilder.outputs) |  |
| [`tree`](#nodebpy.builder.node.NodeGroupBuilder.tree) |  |
| [`type`](#nodebpy.builder.node.NodeGroupBuilder.type) |  |
