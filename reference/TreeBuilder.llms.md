# TreeBuilder

``` python
TreeBuilder(
    tree='Geometry Nodes',
    *,
    tree_type='GeometryNodeTree',
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
    ignore_visibility=False,
)
```

Builder for creating Blender node trees with a clean Python API.

Supports geometry, shader, and compositor node trees.

## Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`collapse`](#nodebpy.TreeBuilder.collapse)                   |             |
| [`fake_user`](#nodebpy.TreeBuilder.fake_user)                 |             |
| [`ignore_visibility`](#nodebpy.TreeBuilder.ignore_visibility) |             |
| [`inputs`](#nodebpy.TreeBuilder.inputs)                       |             |
| [`nodes`](#nodebpy.TreeBuilder.nodes)                         |             |
| [`outputs`](#nodebpy.TreeBuilder.outputs)                     |             |
| [`tree`](#nodebpy.TreeBuilder.tree)                           |             |

## Methods

| Name | Description |
|----|----|
| [activate_tree](#nodebpy.TreeBuilder.activate_tree) | Make this tree the active tree for all new node creation. |
| [add](#nodebpy.TreeBuilder.add) |  |
| [arrange](#nodebpy.TreeBuilder.arrange) |  |
| [compositor](#nodebpy.TreeBuilder.compositor) | Create a compositor node tree. |
| [deactivate_tree](#nodebpy.TreeBuilder.deactivate_tree) | Whatever tree was previously active is set to be the active one (or None if no previously active tree). |
| [geometry](#nodebpy.TreeBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.TreeBuilder.link) |  |
| [shader](#nodebpy.TreeBuilder.shader) | Create a shader node tree. |

### activate_tree

``` python
activate_tree()
```

Make this tree the active tree for all new node creation.

### add

``` python
add(name)
```

### arrange

``` python
arrange()
```

### compositor

``` python
compositor(
    name='Compositor Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```

Create a compositor node tree.

### deactivate_tree

``` python
deactivate_tree()
```

Whatever tree was previously active is set to be the active one (or None if no previously active tree).

### geometry

``` python
geometry(
    name='Geometry Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```

Create a geometry node tree.

### link

``` python
link(socket1, socket2)
```

### shader

``` python
shader(
    name='Shader Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
)
```

Create a shader node tree.
