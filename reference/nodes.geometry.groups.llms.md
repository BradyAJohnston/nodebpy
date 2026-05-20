# nodes.geometry.groups

`groups`

## Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`GROUP_NAME`](#nodebpy.nodes.geometry.groups.GROUP_NAME) |             |

## Classes

| Name | Description |
|----|----|
| [ClipFieldToBox](#nodebpy.nodes.geometry.groups.ClipFieldToBox) |  |
| [OffsetVector](#nodebpy.nodes.geometry.groups.OffsetVector) | Evaluate a given vector field at an offset to the current `Index`. |
| [OtherVertex](#nodebpy.nodes.geometry.groups.OtherVertex) | Given a vertex and an edge number from that vertex, returns the other |
| [PrincipalComponents](#nodebpy.nodes.geometry.groups.PrincipalComponents) | Compute PCA on a given vector field. |

### ClipFieldToBox

``` python
ClipFieldToBox(box_object=None, invert=False)
```

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.i) | Input socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`name`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.name) |  |
| [`node`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.o) | Output socket accessor. Subclasses narrow the return type via TYPE_CHECKING. |
| [`outputs`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.tree) |  |
| [`type`](#nodebpy.nodes.geometry.groups.ClipFieldToBox.type) |  |

### OffsetVector

``` python
OffsetVector(index=None, vector=None, offset=0)
```

Evaluate a given vector field at an offset to the current `Index`.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.OffsetVector.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.OffsetVector.name) |  |
| [`node`](#nodebpy.nodes.geometry.groups.OffsetVector.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.OffsetVector.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.OffsetVector.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.OffsetVector.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.OffsetVector.tree) |  |
| [`type`](#nodebpy.nodes.geometry.groups.OffsetVector.type) |  |

### OtherVertex

``` python
OtherVertex(vertex_index=None, edge_number=0)
```

Given a vertex and an edge number from that vertex, returns the other vertex of that edge.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.OtherVertex.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.OtherVertex.name) |  |
| [`node`](#nodebpy.nodes.geometry.groups.OtherVertex.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.OtherVertex.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.OtherVertex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.OtherVertex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.OtherVertex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.groups.OtherVertex.type) |  |

### PrincipalComponents

``` python
PrincipalComponents(position=None, group_id=None)
```

Compute PCA on a given vector field.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.groups.PrincipalComponents.i) |  |
| [`name`](#nodebpy.nodes.geometry.groups.PrincipalComponents.name) |  |
| [`node`](#nodebpy.nodes.geometry.groups.PrincipalComponents.node) |  |
| [`node_tree`](#nodebpy.nodes.geometry.groups.PrincipalComponents.node_tree) |  |
| [`o`](#nodebpy.nodes.geometry.groups.PrincipalComponents.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.groups.PrincipalComponents.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.groups.PrincipalComponents.tree) |  |
| [`type`](#nodebpy.nodes.geometry.groups.PrincipalComponents.type) |  |
