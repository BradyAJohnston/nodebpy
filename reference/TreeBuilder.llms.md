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

| Name | Description |
|----|----|
| [`collapse`](#nodebpy.TreeBuilder.collapse) |  |
| [`fake_user`](#nodebpy.TreeBuilder.fake_user) |  |
| [`ignore_visibility`](#nodebpy.TreeBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.TreeBuilder.inputs) |  |
| [`node_positions`](#nodebpy.TreeBuilder.node_positions) | A `{node name: (x, y)}` snapshot of every node’s location. |
| [`nodes`](#nodebpy.TreeBuilder.nodes) |  |
| [`outputs`](#nodebpy.TreeBuilder.outputs) |  |
| [`tree`](#nodebpy.TreeBuilder.tree) |  |

## Methods

| Name | Description |
|----|----|
| [activate_tree](#nodebpy.TreeBuilder.activate_tree) | Make this tree the active tree for all new node creation. |
| [add](#nodebpy.TreeBuilder.add) |  |
| [arrange](#nodebpy.TreeBuilder.arrange) |  |
| [compositor](#nodebpy.TreeBuilder.compositor) | Create a compositor node tree. |
| [deactivate_tree](#nodebpy.TreeBuilder.deactivate_tree) | Whatever tree was previously active is set to be the active one (or None if no previously active tree). |
| [disable_arrange](#nodebpy.TreeBuilder.disable_arrange) | Disable the auto-layout that otherwise runs when this tree’s context |
| [geometry](#nodebpy.TreeBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.TreeBuilder.link) |  |
| [shader](#nodebpy.TreeBuilder.shader) | Create a shader node tree. |
| [to_mermaid](#nodebpy.TreeBuilder.to_mermaid) | Generate a Mermaid diagram that represents this tree. |
| [to_python](#nodebpy.TreeBuilder.to_python) | Generate Python source that recreates this tree using nodebpy. |

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

### disable_arrange

``` python
disable_arrange()
```

Disable the auto-layout that otherwise runs when this tree’s context exits, so explicitly assigned node locations are preserved.

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

### to_mermaid

``` python
to_mermaid(fenced=True)
```

Generate a Mermaid diagram that represents this tree.

This can be used for documentation or visualization purposes. The Mermaid syntax is supported by many tools, including GitHub and Jupyter notebooks.

#### Arguments

    fenced:
        Whether to wrap the output in a fenced code block with mermaid syntax highlighting.

#### Returns

| Name | Type | Description |
|----|----|----|
|  | A string containing the Mermaid diagram syntax representing this node tree. |  |

### to_python

``` python
to_python(
    min_chain_length=3,
    strict=True,
    max_inline_width=88,
    snapshot_positions=False,
    keep_reroutes=False,
    top_level='with',
    format=True,
)
```

Generate Python source that recreates this tree using nodebpy.

See :func:`nodebpy.codegen.to_python` for parameter details.
