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
    split_inputs=False,
)
```

Builder for creating Blender node trees with a clean Python API.

Supports geometry, shader, and compositor node trees.

## Attributes

| Name | Description |
|----|----|
| [`collapse`](#nodebpy.TreeBuilder.collapse) |  |
| [`fake_user`](#nodebpy.TreeBuilder.fake_user) |  |
| [`group_input_splits`](#nodebpy.TreeBuilder.group_input_splits) | The extra Group Input instances beyond the primary one, each as |
| [`ignore_visibility`](#nodebpy.TreeBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.TreeBuilder.inputs) |  |
| [`layout_snapshot`](#nodebpy.TreeBuilder.layout_snapshot) | A structural layout snapshot: for every node its type, `(x, y)` |
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
| [panel](#nodebpy.TreeBuilder.panel) | A panel that can group input *and* output sockets together |
| [shader](#nodebpy.TreeBuilder.shader) | Create a shader node tree. |
| [split_group_inputs](#nodebpy.TreeBuilder.split_group_inputs) | Split the Group Input node into one instance per consumer node, |
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
    split_inputs=False,
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
    split_inputs=False,
)
```

Create a geometry node tree.

### link

``` python
link(socket1, socket2)
```

### panel

``` python
panel(name, *, description='', default_closed=False, reuse=True)
```

A panel that can group input *and* output sockets together (`tree.inputs.panel` / `tree.outputs.panel` group one direction). Reuses an existing same-named panel under the same parent, so a mixed panel can be declared in separate input and output passes; pass `reuse=False` to always create a fresh panel — Blender allows several same-named sibling panels, and rebuilding such an interface must not fold them into one. Passing an existing panel (or a previous `tree.panel(...)` context) instead of a name reopens exactly that panel — the unambiguous spelling generated code uses for the second direction pass over a same-named sibling.

### shader

``` python
shader(
    name='Shader Nodes',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
    split_inputs=False,
)
```

Create a shader node tree.

### split_group_inputs

``` python
split_group_inputs()
```

Split the Group Input node into one instance per consumer node, with unused sockets hidden — regenerating the editor style that avoids a single input node trailing long noodles. Runs automatically on context exit (before auto-layout, so the instances are arranged next to their consumers) when the builder was created with `split_inputs=True`.

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
    nodebpy_pkg='nodebpy',
)
```

Generate Python source that recreates this tree using nodebpy.

See :func:`nodebpy.codegen.to_python` for parameter details.
