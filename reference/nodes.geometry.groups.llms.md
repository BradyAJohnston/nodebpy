# nodes.geometry.groups

`groups`

## Classes

| Name | Description |
|----|----|
| [ClipFieldToBox](#nodebpy.nodes.geometry.groups.ClipFieldToBox) |  |
| [GeometryPrincipalComponents](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents) |  |
| [OffsetVector](#nodebpy.nodes.geometry.groups.OffsetVector) | Evaluate a given vector field at an offset to the current `Index`. |
| [OtherVertex](#nodebpy.nodes.geometry.groups.OtherVertex) | Given a vertex and an edge number from that vertex, returns the other |
| [PrincipalComponents](#nodebpy.nodes.geometry.groups.PrincipalComponents) | Compute PCA on a given vector field. |
| [SliceToIndices](#nodebpy.nodes.geometry.groups.SliceToIndices) | Converts a python slice to a list of indices. |

### ClipFieldToBox

``` python
ClipFieldToBox(box_object=None, invert=False)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.ClipFieldToBox.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

### GeometryPrincipalComponents

``` python
GeometryPrincipalComponents(geometry=None, position=None)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.GeometryPrincipalComponents.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

### OffsetVector

``` python
OffsetVector(index=None, vector=None, offset=0)
```

Evaluate a given vector field at an offset to the current `Index`.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.OffsetVector.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.OffsetVector.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.OffsetVector.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.OffsetVector.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.OffsetVector.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.OffsetVector.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.OffsetVector.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.OffsetVector.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

### OtherVertex

``` python
OtherVertex(vertex_index=None, edge_number=0)
```

Given a vertex and an edge number from that vertex, returns the other vertex of that edge.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.OtherVertex.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.OtherVertex.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.OtherVertex.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.OtherVertex.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.OtherVertex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.OtherVertex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.OtherVertex.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.OtherVertex.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

### PrincipalComponents

``` python
PrincipalComponents(position=None, group_id=None)
```

Compute PCA on a given vector field.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.PrincipalComponents.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.PrincipalComponents.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.PrincipalComponents.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.PrincipalComponents.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.PrincipalComponents.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.PrincipalComponents.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.PrincipalComponents.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.PrincipalComponents.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.

### SliceToIndices

``` python
SliceToIndices(start=0, stop=0, step=1)
```

Converts a python slice to a list of indices.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.SliceToIndices.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.SliceToIndices.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.geometry.groups.SliceToIndices.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.SliceToIndices.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.SliceToIndices.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.SliceToIndices.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.SliceToIndices.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [create_group](#nodebpy.nodes.geometry.groups.SliceToIndices.create_group) | Build this group’s node tree and return it, reusing an existing tree |

##### create_group

``` python
create_group()
```

Build this group’s node tree and return it, reusing an existing tree of the same name.

Unlike instantiating the class, this needs no active `TreeBuilder` context — it opens its own — so a group can be pre-built and reused directly (e.g. assigned to a node’s `node_tree`) instead of being created by constructing the class inside a tree.
