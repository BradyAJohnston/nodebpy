# builder.BaseNode

``` python
BaseNode(node=None)
```

Base class for all node wrappers.

## Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.builder.BaseNode.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.builder.BaseNode.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.builder.BaseNode.node) |  |
| [`o`](#nodebpy.builder.BaseNode.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.builder.BaseNode.outputs) |  |
| [`tree`](#nodebpy.builder.BaseNode.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
