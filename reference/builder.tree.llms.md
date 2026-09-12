# builder.tree

`tree`

## Classes

| Name | Description |
|----|----|
| [DirectionalContext](#nodebpy.builder.tree.DirectionalContext) | Base class for directional socket contexts |
| [InputInterfaceContext](#nodebpy.builder.tree.InputInterfaceContext) |  |
| [MaterialBuilder](#nodebpy.builder.tree.MaterialBuilder) |  |
| [OutputInterfaceContext](#nodebpy.builder.tree.OutputInterfaceContext) |  |
| [PanelContext](#nodebpy.builder.tree.PanelContext) | Context manager for grouping sockets into a panel. |
| [SocketContext](#nodebpy.builder.tree.SocketContext) |  |
| [TreeBuilder](#nodebpy.builder.tree.TreeBuilder) | Builder for creating Blender node trees with a clean Python API. |
| [TreePanelContext](#nodebpy.builder.tree.TreePanelContext) | Context manager for a panel holding both input *and* output sockets. |

### DirectionalContext

``` python
DirectionalContext(tree_builder)
```

Base class for directional socket contexts

#### Attributes

| Name | Description |
|----|----|
| [`builder`](#nodebpy.builder.tree.DirectionalContext.builder) |  |
| [`interface`](#nodebpy.builder.tree.DirectionalContext.interface) |  |
| [`tree`](#nodebpy.builder.tree.DirectionalContext.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.builder.tree.DirectionalContext.boolean) |  |
| [bundle](#nodebpy.builder.tree.DirectionalContext.bundle) |  |
| [closure](#nodebpy.builder.tree.DirectionalContext.closure) |  |
| [collection](#nodebpy.builder.tree.DirectionalContext.collection) |  |
| [color](#nodebpy.builder.tree.DirectionalContext.color) |  |
| [float](#nodebpy.builder.tree.DirectionalContext.float) |  |
| [font](#nodebpy.builder.tree.DirectionalContext.font) |  |
| [geometry](#nodebpy.builder.tree.DirectionalContext.geometry) |  |
| [image](#nodebpy.builder.tree.DirectionalContext.image) |  |
| [integer](#nodebpy.builder.tree.DirectionalContext.integer) |  |
| [material](#nodebpy.builder.tree.DirectionalContext.material) |  |
| [matrix](#nodebpy.builder.tree.DirectionalContext.matrix) |  |
| [menu](#nodebpy.builder.tree.DirectionalContext.menu) |  |
| [object](#nodebpy.builder.tree.DirectionalContext.object) |  |
| [panel](#nodebpy.builder.tree.DirectionalContext.panel) | Create a panel context for grouping sockets. |
| [rotation](#nodebpy.builder.tree.DirectionalContext.rotation) |  |
| [shader](#nodebpy.builder.tree.DirectionalContext.shader) |  |
| [sound](#nodebpy.builder.tree.DirectionalContext.sound) |  |
| [string](#nodebpy.builder.tree.DirectionalContext.string) |  |
| [vector](#nodebpy.builder.tree.DirectionalContext.vector) |  |

##### boolean

``` python
boolean(
    name='Boolean',
    default_value=False,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    layer_selection_field=False,
    attribute_domain='POINT',
    default_attribute=None,
    is_panel_toggle=False,
    force_non_field=False,
)
```

##### bundle

``` python
bundle(
    name='Bundle',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### closure

``` python
closure(
    name='Closure',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### collection

``` python
collection(
    name='Collection',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### color

``` python
color(
    name='Color',
    default_value=(1.0, 1.0, 1.0, 1.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### float

``` python
float(
    name='Value',
    default_value=0.0,
    description='',
    *,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
    default_input='VALUE',
)
```

##### font

``` python
font(
    name='Font',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### geometry

``` python
geometry(
    name='Geometry',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### image

``` python
image(
    name='Image',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### integer

``` python
integer(
    name='Integer',
    default_value=0,
    description='',
    *,
    min_value=-2147483648,
    max_value=2147483647,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### material

``` python
material(
    name='Material',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### matrix

``` python
matrix(
    name='Matrix',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### menu

``` python
menu(
    name='Menu',
    default_value=None,
    description='',
    *,
    expanded=False,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### object

``` python
object(
    name='Object',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
    default_input='VALUE',
)
```

##### panel

``` python
panel(name, *, description='', default_closed=False)
```

Create a panel context for grouping sockets.

##### rotation

``` python
rotation(
    name='Rotation',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### shader

``` python
shader(
    name='Shader',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### sound

``` python
sound(
    name='Sound',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### string

``` python
string(
    name='String',
    default_value='',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    subtype='NONE',
    structure_type='AUTO',
    force_non_field=False,
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=None,
    description='',
    *,
    dimensions=3,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    default_attribute=None,
    default_input='VALUE',
    attribute_domain='POINT',
    force_non_field=False,
)
```

### InputInterfaceContext

``` python
InputInterfaceContext(tree_builder)
```

#### Attributes

| Name | Description |
|----|----|
| [`builder`](#nodebpy.builder.tree.InputInterfaceContext.builder) |  |
| [`interface`](#nodebpy.builder.tree.InputInterfaceContext.interface) |  |
| [`tree`](#nodebpy.builder.tree.InputInterfaceContext.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.builder.tree.InputInterfaceContext.boolean) |  |
| [bundle](#nodebpy.builder.tree.InputInterfaceContext.bundle) |  |
| [closure](#nodebpy.builder.tree.InputInterfaceContext.closure) |  |
| [collection](#nodebpy.builder.tree.InputInterfaceContext.collection) |  |
| [color](#nodebpy.builder.tree.InputInterfaceContext.color) |  |
| [float](#nodebpy.builder.tree.InputInterfaceContext.float) |  |
| [font](#nodebpy.builder.tree.InputInterfaceContext.font) |  |
| [geometry](#nodebpy.builder.tree.InputInterfaceContext.geometry) |  |
| [image](#nodebpy.builder.tree.InputInterfaceContext.image) |  |
| [integer](#nodebpy.builder.tree.InputInterfaceContext.integer) |  |
| [material](#nodebpy.builder.tree.InputInterfaceContext.material) |  |
| [matrix](#nodebpy.builder.tree.InputInterfaceContext.matrix) |  |
| [menu](#nodebpy.builder.tree.InputInterfaceContext.menu) |  |
| [object](#nodebpy.builder.tree.InputInterfaceContext.object) |  |
| [panel](#nodebpy.builder.tree.InputInterfaceContext.panel) | Create a panel context for grouping sockets. |
| [rotation](#nodebpy.builder.tree.InputInterfaceContext.rotation) |  |
| [shader](#nodebpy.builder.tree.InputInterfaceContext.shader) |  |
| [sound](#nodebpy.builder.tree.InputInterfaceContext.sound) |  |
| [string](#nodebpy.builder.tree.InputInterfaceContext.string) |  |
| [vector](#nodebpy.builder.tree.InputInterfaceContext.vector) |  |

##### boolean

``` python
boolean(
    name='Boolean',
    default_value=False,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    layer_selection_field=False,
    attribute_domain='POINT',
    default_attribute=None,
    is_panel_toggle=False,
    force_non_field=False,
)
```

##### bundle

``` python
bundle(
    name='Bundle',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### closure

``` python
closure(
    name='Closure',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### collection

``` python
collection(
    name='Collection',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### color

``` python
color(
    name='Color',
    default_value=(1.0, 1.0, 1.0, 1.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### float

``` python
float(
    name='Value',
    default_value=0.0,
    description='',
    *,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
    default_input='VALUE',
)
```

##### font

``` python
font(
    name='Font',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### geometry

``` python
geometry(
    name='Geometry',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### image

``` python
image(
    name='Image',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### integer

``` python
integer(
    name='Integer',
    default_value=0,
    description='',
    *,
    min_value=-2147483648,
    max_value=2147483647,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### material

``` python
material(
    name='Material',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### matrix

``` python
matrix(
    name='Matrix',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### menu

``` python
menu(
    name='Menu',
    default_value=None,
    description='',
    *,
    expanded=False,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### object

``` python
object(
    name='Object',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
    default_input='VALUE',
)
```

##### panel

``` python
panel(name, *, description='', default_closed=False)
```

Create a panel context for grouping sockets.

##### rotation

``` python
rotation(
    name='Rotation',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### shader

``` python
shader(
    name='Shader',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### sound

``` python
sound(
    name='Sound',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### string

``` python
string(
    name='String',
    default_value='',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    subtype='NONE',
    structure_type='AUTO',
    force_non_field=False,
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=None,
    description='',
    *,
    dimensions=3,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    default_attribute=None,
    default_input='VALUE',
    attribute_domain='POINT',
    force_non_field=False,
)
```

### MaterialBuilder

``` python
MaterialBuilder(
    name='New Material',
    *,
    collapse=False,
    arrange='sugiyama',
    fake_user=False,
    ignore_visibility=False,
)
```

#### Attributes

| Name | Description |
|----|----|
| [`collapse`](#nodebpy.builder.tree.MaterialBuilder.collapse) |  |
| [`fake_user`](#nodebpy.builder.tree.MaterialBuilder.fake_user) |  |
| [`group_input_splits`](#nodebpy.builder.tree.MaterialBuilder.group_input_splits) | The extra Group Input instances beyond the primary one, each as |
| [`ignore_visibility`](#nodebpy.builder.tree.MaterialBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.builder.tree.MaterialBuilder.inputs) |  |
| [`layout_snapshot`](#nodebpy.builder.tree.MaterialBuilder.layout_snapshot) | A structural layout snapshot: for every node its type, `(x, y)` |
| [`material`](#nodebpy.builder.tree.MaterialBuilder.material) |  |
| [`node_positions`](#nodebpy.builder.tree.MaterialBuilder.node_positions) | A `{node name: (x, y)}` snapshot of every node’s location. |
| [`nodes`](#nodebpy.builder.tree.MaterialBuilder.nodes) |  |
| [`outputs`](#nodebpy.builder.tree.MaterialBuilder.outputs) |  |
| [`tree`](#nodebpy.builder.tree.MaterialBuilder.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [activate_tree](#nodebpy.builder.tree.MaterialBuilder.activate_tree) | Make this tree the active tree for all new node creation. |
| [add](#nodebpy.builder.tree.MaterialBuilder.add) |  |
| [arrange](#nodebpy.builder.tree.MaterialBuilder.arrange) |  |
| [compositor](#nodebpy.builder.tree.MaterialBuilder.compositor) | Create a compositor node tree. |
| [deactivate_tree](#nodebpy.builder.tree.MaterialBuilder.deactivate_tree) | Whatever tree was previously active is set to be the active one (or None if no previously active tree). |
| [disable_arrange](#nodebpy.builder.tree.MaterialBuilder.disable_arrange) | Disable the auto-layout that otherwise runs when this tree’s context |
| [geometry](#nodebpy.builder.tree.MaterialBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.builder.tree.MaterialBuilder.link) |  |
| [panel](#nodebpy.builder.tree.MaterialBuilder.panel) | A panel that can group input *and* output sockets together |
| [shader](#nodebpy.builder.tree.MaterialBuilder.shader) | Create a shader node tree. |
| [split_group_inputs](#nodebpy.builder.tree.MaterialBuilder.split_group_inputs) | Split the Group Input node into one instance per consumer node, |
| [to_mermaid](#nodebpy.builder.tree.MaterialBuilder.to_mermaid) | Generate a Mermaid diagram that represents this tree. |
| [to_python](#nodebpy.builder.tree.MaterialBuilder.to_python) | Generate Python source that recreates this tree using nodebpy. |

##### activate_tree

``` python
activate_tree()
```

Make this tree the active tree for all new node creation.

##### add

``` python
add(name)
```

##### arrange

``` python
arrange()
```

##### compositor

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

##### deactivate_tree

``` python
deactivate_tree()
```

Whatever tree was previously active is set to be the active one (or None if no previously active tree).

##### disable_arrange

``` python
disable_arrange()
```

Disable the auto-layout that otherwise runs when this tree’s context exits, so explicitly assigned node locations are preserved.

##### geometry

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

##### link

``` python
link(socket1, socket2)
```

##### panel

``` python
panel(name, *, description='', default_closed=False, reuse=True)
```

A panel that can group input *and* output sockets together (`tree.inputs.panel` / `tree.outputs.panel` group one direction). Reuses an existing same-named panel under the same parent, so a mixed panel can be declared in separate input and output passes; pass `reuse=False` to always create a fresh panel — Blender allows several same-named sibling panels, and rebuilding such an interface must not fold them into one. Passing an existing panel (or a previous `tree.panel(...)` context) instead of a name reopens exactly that panel — the unambiguous spelling generated code uses for the second direction pass over a same-named sibling.

##### shader

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

##### split_group_inputs

``` python
split_group_inputs()
```

Split the Group Input node into one instance per consumer node, with unused sockets hidden — regenerating the editor style that avoids a single input node trailing long noodles. Runs automatically on context exit (before auto-layout, so the instances are arranged next to their consumers) when the builder was created with `split_inputs=True`.

##### to_mermaid

``` python
to_mermaid(fenced=True)
```

Generate a Mermaid diagram that represents this tree.

This can be used for documentation or visualization purposes. The Mermaid syntax is supported by many tools, including GitHub and Jupyter notebooks.

###### Arguments

    fenced:
        Whether to wrap the output in a fenced code block with mermaid syntax highlighting.

###### Returns

| Name | Type | Description |
|----|----|----|
|  | A string containing the Mermaid diagram syntax representing this node tree. |  |

##### to_python

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

### OutputInterfaceContext

``` python
OutputInterfaceContext(tree_builder)
```

#### Attributes

| Name | Description |
|----|----|
| [`builder`](#nodebpy.builder.tree.OutputInterfaceContext.builder) |  |
| [`interface`](#nodebpy.builder.tree.OutputInterfaceContext.interface) |  |
| [`tree`](#nodebpy.builder.tree.OutputInterfaceContext.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.builder.tree.OutputInterfaceContext.boolean) |  |
| [bundle](#nodebpy.builder.tree.OutputInterfaceContext.bundle) |  |
| [closure](#nodebpy.builder.tree.OutputInterfaceContext.closure) |  |
| [collection](#nodebpy.builder.tree.OutputInterfaceContext.collection) |  |
| [color](#nodebpy.builder.tree.OutputInterfaceContext.color) |  |
| [float](#nodebpy.builder.tree.OutputInterfaceContext.float) |  |
| [font](#nodebpy.builder.tree.OutputInterfaceContext.font) |  |
| [geometry](#nodebpy.builder.tree.OutputInterfaceContext.geometry) |  |
| [image](#nodebpy.builder.tree.OutputInterfaceContext.image) |  |
| [integer](#nodebpy.builder.tree.OutputInterfaceContext.integer) |  |
| [material](#nodebpy.builder.tree.OutputInterfaceContext.material) |  |
| [matrix](#nodebpy.builder.tree.OutputInterfaceContext.matrix) |  |
| [menu](#nodebpy.builder.tree.OutputInterfaceContext.menu) |  |
| [object](#nodebpy.builder.tree.OutputInterfaceContext.object) |  |
| [panel](#nodebpy.builder.tree.OutputInterfaceContext.panel) | Create a panel context for grouping sockets. |
| [rotation](#nodebpy.builder.tree.OutputInterfaceContext.rotation) |  |
| [shader](#nodebpy.builder.tree.OutputInterfaceContext.shader) |  |
| [sound](#nodebpy.builder.tree.OutputInterfaceContext.sound) |  |
| [string](#nodebpy.builder.tree.OutputInterfaceContext.string) |  |
| [vector](#nodebpy.builder.tree.OutputInterfaceContext.vector) |  |

##### boolean

``` python
boolean(
    name='Boolean',
    default_value=False,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    layer_selection_field=False,
    attribute_domain='POINT',
    default_attribute=None,
    is_panel_toggle=False,
    force_non_field=False,
)
```

##### bundle

``` python
bundle(
    name='Bundle',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### closure

``` python
closure(
    name='Closure',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### collection

``` python
collection(
    name='Collection',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### color

``` python
color(
    name='Color',
    default_value=(1.0, 1.0, 1.0, 1.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### float

``` python
float(
    name='Value',
    default_value=0.0,
    description='',
    *,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
    default_input='VALUE',
)
```

##### font

``` python
font(
    name='Font',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### geometry

``` python
geometry(
    name='Geometry',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### image

``` python
image(
    name='Image',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### integer

``` python
integer(
    name='Integer',
    default_value=0,
    description='',
    *,
    min_value=-2147483648,
    max_value=2147483647,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### material

``` python
material(
    name='Material',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### matrix

``` python
matrix(
    name='Matrix',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### menu

``` python
menu(
    name='Menu',
    default_value=None,
    description='',
    *,
    expanded=False,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### object

``` python
object(
    name='Object',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
    default_input='VALUE',
)
```

##### panel

``` python
panel(name, *, description='', default_closed=False)
```

Create a panel context for grouping sockets.

##### rotation

``` python
rotation(
    name='Rotation',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### shader

``` python
shader(
    name='Shader',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### sound

``` python
sound(
    name='Sound',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### string

``` python
string(
    name='String',
    default_value='',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    subtype='NONE',
    structure_type='AUTO',
    force_non_field=False,
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=None,
    description='',
    *,
    dimensions=3,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    default_attribute=None,
    default_input='VALUE',
    attribute_domain='POINT',
    force_non_field=False,
)
```

### PanelContext

``` python
PanelContext(socket_context, name, *, description='', default_closed=False)
```

Context manager for grouping sockets into a panel.

### SocketContext

``` python
SocketContext(tree_builder)
```

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`builder`](#nodebpy.builder.tree.SocketContext.builder)     |             |
| [`interface`](#nodebpy.builder.tree.SocketContext.interface) |             |
| [`tree`](#nodebpy.builder.tree.SocketContext.tree)           |             |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.builder.tree.SocketContext.boolean) |  |
| [bundle](#nodebpy.builder.tree.SocketContext.bundle) |  |
| [closure](#nodebpy.builder.tree.SocketContext.closure) |  |
| [collection](#nodebpy.builder.tree.SocketContext.collection) |  |
| [color](#nodebpy.builder.tree.SocketContext.color) |  |
| [float](#nodebpy.builder.tree.SocketContext.float) |  |
| [font](#nodebpy.builder.tree.SocketContext.font) |  |
| [geometry](#nodebpy.builder.tree.SocketContext.geometry) |  |
| [image](#nodebpy.builder.tree.SocketContext.image) |  |
| [integer](#nodebpy.builder.tree.SocketContext.integer) |  |
| [material](#nodebpy.builder.tree.SocketContext.material) |  |
| [matrix](#nodebpy.builder.tree.SocketContext.matrix) |  |
| [menu](#nodebpy.builder.tree.SocketContext.menu) |  |
| [object](#nodebpy.builder.tree.SocketContext.object) |  |
| [panel](#nodebpy.builder.tree.SocketContext.panel) | Create a panel context for grouping sockets. |
| [rotation](#nodebpy.builder.tree.SocketContext.rotation) |  |
| [shader](#nodebpy.builder.tree.SocketContext.shader) |  |
| [sound](#nodebpy.builder.tree.SocketContext.sound) |  |
| [string](#nodebpy.builder.tree.SocketContext.string) |  |
| [vector](#nodebpy.builder.tree.SocketContext.vector) |  |

##### boolean

``` python
boolean(
    name='Boolean',
    default_value=False,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    layer_selection_field=False,
    attribute_domain='POINT',
    default_attribute=None,
    is_panel_toggle=False,
    force_non_field=False,
)
```

##### bundle

``` python
bundle(
    name='Bundle',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### closure

``` python
closure(
    name='Closure',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### collection

``` python
collection(
    name='Collection',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### color

``` python
color(
    name='Color',
    default_value=(1.0, 1.0, 1.0, 1.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### float

``` python
float(
    name='Value',
    default_value=0.0,
    description='',
    *,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
    default_input='VALUE',
)
```

##### font

``` python
font(
    name='Font',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### geometry

``` python
geometry(
    name='Geometry',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### image

``` python
image(
    name='Image',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### integer

``` python
integer(
    name='Integer',
    default_value=0,
    description='',
    *,
    min_value=-2147483648,
    max_value=2147483647,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    subtype='NONE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### material

``` python
material(
    name='Material',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### matrix

``` python
matrix(
    name='Matrix',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    default_input='VALUE',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### menu

``` python
menu(
    name='Menu',
    default_value=None,
    description='',
    *,
    expanded=False,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### object

``` python
object(
    name='Object',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
    default_input='VALUE',
)
```

##### panel

``` python
panel(name, *, description='', default_closed=False)
```

Create a panel context for grouping sockets.

##### rotation

``` python
rotation(
    name='Rotation',
    default_value=(0.0, 0.0, 0.0),
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    attribute_domain='POINT',
    default_attribute=None,
    force_non_field=False,
)
```

##### shader

``` python
shader(
    name='Shader',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    force_non_field=False,
)
```

##### sound

``` python
sound(
    name='Sound',
    default_value=None,
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
)
```

##### string

``` python
string(
    name='String',
    default_value='',
    description='',
    *,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    subtype='NONE',
    structure_type='AUTO',
    force_non_field=False,
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=None,
    description='',
    *,
    dimensions=3,
    min_value=None,
    max_value=None,
    optional_label=False,
    hide_value=False,
    hide_in_modifier=False,
    structure_type='AUTO',
    subtype='NONE',
    default_attribute=None,
    default_input='VALUE',
    attribute_domain='POINT',
    force_non_field=False,
)
```

### TreeBuilder

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

#### Attributes

| Name | Description |
|----|----|
| [`collapse`](#nodebpy.builder.tree.TreeBuilder.collapse) |  |
| [`fake_user`](#nodebpy.builder.tree.TreeBuilder.fake_user) |  |
| [`group_input_splits`](#nodebpy.builder.tree.TreeBuilder.group_input_splits) | The extra Group Input instances beyond the primary one, each as |
| [`ignore_visibility`](#nodebpy.builder.tree.TreeBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.builder.tree.TreeBuilder.inputs) |  |
| [`layout_snapshot`](#nodebpy.builder.tree.TreeBuilder.layout_snapshot) | A structural layout snapshot: for every node its type, `(x, y)` |
| [`node_positions`](#nodebpy.builder.tree.TreeBuilder.node_positions) | A `{node name: (x, y)}` snapshot of every node’s location. |
| [`nodes`](#nodebpy.builder.tree.TreeBuilder.nodes) |  |
| [`outputs`](#nodebpy.builder.tree.TreeBuilder.outputs) |  |
| [`tree`](#nodebpy.builder.tree.TreeBuilder.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [activate_tree](#nodebpy.builder.tree.TreeBuilder.activate_tree) | Make this tree the active tree for all new node creation. |
| [add](#nodebpy.builder.tree.TreeBuilder.add) |  |
| [arrange](#nodebpy.builder.tree.TreeBuilder.arrange) |  |
| [compositor](#nodebpy.builder.tree.TreeBuilder.compositor) | Create a compositor node tree. |
| [deactivate_tree](#nodebpy.builder.tree.TreeBuilder.deactivate_tree) | Whatever tree was previously active is set to be the active one (or None if no previously active tree). |
| [disable_arrange](#nodebpy.builder.tree.TreeBuilder.disable_arrange) | Disable the auto-layout that otherwise runs when this tree’s context |
| [geometry](#nodebpy.builder.tree.TreeBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.builder.tree.TreeBuilder.link) |  |
| [panel](#nodebpy.builder.tree.TreeBuilder.panel) | A panel that can group input *and* output sockets together |
| [shader](#nodebpy.builder.tree.TreeBuilder.shader) | Create a shader node tree. |
| [split_group_inputs](#nodebpy.builder.tree.TreeBuilder.split_group_inputs) | Split the Group Input node into one instance per consumer node, |
| [to_mermaid](#nodebpy.builder.tree.TreeBuilder.to_mermaid) | Generate a Mermaid diagram that represents this tree. |
| [to_python](#nodebpy.builder.tree.TreeBuilder.to_python) | Generate Python source that recreates this tree using nodebpy. |

##### activate_tree

``` python
activate_tree()
```

Make this tree the active tree for all new node creation.

##### add

``` python
add(name)
```

##### arrange

``` python
arrange()
```

##### compositor

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

##### deactivate_tree

``` python
deactivate_tree()
```

Whatever tree was previously active is set to be the active one (or None if no previously active tree).

##### disable_arrange

``` python
disable_arrange()
```

Disable the auto-layout that otherwise runs when this tree’s context exits, so explicitly assigned node locations are preserved.

##### geometry

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

##### link

``` python
link(socket1, socket2)
```

##### panel

``` python
panel(name, *, description='', default_closed=False, reuse=True)
```

A panel that can group input *and* output sockets together (`tree.inputs.panel` / `tree.outputs.panel` group one direction). Reuses an existing same-named panel under the same parent, so a mixed panel can be declared in separate input and output passes; pass `reuse=False` to always create a fresh panel — Blender allows several same-named sibling panels, and rebuilding such an interface must not fold them into one. Passing an existing panel (or a previous `tree.panel(...)` context) instead of a name reopens exactly that panel — the unambiguous spelling generated code uses for the second direction pass over a same-named sibling.

##### shader

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

##### split_group_inputs

``` python
split_group_inputs()
```

Split the Group Input node into one instance per consumer node, with unused sockets hidden — regenerating the editor style that avoids a single input node trailing long noodles. Runs automatically on context exit (before auto-layout, so the instances are arranged next to their consumers) when the builder was created with `split_inputs=True`.

##### to_mermaid

``` python
to_mermaid(fenced=True)
```

Generate a Mermaid diagram that represents this tree.

This can be used for documentation or visualization purposes. The Mermaid syntax is supported by many tools, including GitHub and Jupyter notebooks.

###### Arguments

    fenced:
        Whether to wrap the output in a fenced code block with mermaid syntax highlighting.

###### Returns

| Name | Type | Description |
|----|----|----|
|  | A string containing the Mermaid diagram syntax representing this node tree. |  |

##### to_python

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

### TreePanelContext

``` python
TreePanelContext(
    builder,
    name,
    *,
    description='',
    default_closed=False,
    reuse=True,
)
```

Context manager for a panel holding both input *and* output sockets.

Activates the panel on the builder’s `inputs` and `outputs` contexts at once, and reuses an existing top-level panel of the same name — so a mixed panel can be filled in two passes (inputs, then outputs) without duplicating it.

#### Attributes

| Name                                                    | Description |
|---------------------------------------------------------|-------------|
| [`panel`](#nodebpy.builder.tree.TreePanelContext.panel) |             |
