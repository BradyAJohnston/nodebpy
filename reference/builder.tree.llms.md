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
)
```

##### panel

``` python
panel(name, *, default_closed=False)
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
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=(0.0, 0.0, 0.0),
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
)
```

##### panel

``` python
panel(name, *, default_closed=False)
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
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=(0.0, 0.0, 0.0),
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
| [`ignore_visibility`](#nodebpy.builder.tree.MaterialBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.builder.tree.MaterialBuilder.inputs) |  |
| [`material`](#nodebpy.builder.tree.MaterialBuilder.material) |  |
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
| [geometry](#nodebpy.builder.tree.MaterialBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.builder.tree.MaterialBuilder.link) |  |
| [shader](#nodebpy.builder.tree.MaterialBuilder.shader) | Create a shader node tree. |

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
)
```

Create a compositor node tree.

##### deactivate_tree

``` python
deactivate_tree()
```

Whatever tree was previously active is set to be the active one (or None if no previously active tree).

##### geometry

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

##### link

``` python
link(socket1, socket2)
```

##### shader

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
)
```

##### panel

``` python
panel(name, *, default_closed=False)
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
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=(0.0, 0.0, 0.0),
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
)
```

### PanelContext

``` python
PanelContext(socket_context, name, *, default_closed=False)
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
)
```

##### panel

``` python
panel(name, *, default_closed=False)
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
)
```

##### vector

``` python
vector(
    name='Vector',
    default_value=(0.0, 0.0, 0.0),
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
)
```

Builder for creating Blender node trees with a clean Python API.

Supports geometry, shader, and compositor node trees.

#### Attributes

| Name | Description |
|----|----|
| [`collapse`](#nodebpy.builder.tree.TreeBuilder.collapse) |  |
| [`fake_user`](#nodebpy.builder.tree.TreeBuilder.fake_user) |  |
| [`ignore_visibility`](#nodebpy.builder.tree.TreeBuilder.ignore_visibility) |  |
| [`inputs`](#nodebpy.builder.tree.TreeBuilder.inputs) |  |
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
| [geometry](#nodebpy.builder.tree.TreeBuilder.geometry) | Create a geometry node tree. |
| [link](#nodebpy.builder.tree.TreeBuilder.link) |  |
| [shader](#nodebpy.builder.tree.TreeBuilder.shader) | Create a shader node tree. |

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
)
```

Create a compositor node tree.

##### deactivate_tree

``` python
deactivate_tree()
```

Whatever tree was previously active is set to be the active one (or None if no previously active tree).

##### geometry

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

##### link

``` python
link(socket1, socket2)
```

##### shader

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
