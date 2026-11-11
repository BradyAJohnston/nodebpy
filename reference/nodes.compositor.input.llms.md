# nodes.compositor.input

`input`

## Classes

| Name | Description |
|----|----|
| [BlankImage](#nodebpy.nodes.compositor.input.BlankImage) | Returns an image with the given size and constant color |
| [BokehImage](#nodebpy.nodes.compositor.input.BokehImage) | Generate image with bokeh shape for use with the Bokeh Blur filter node |
| [Color](#nodebpy.nodes.compositor.input.Color) | A color picker |
| [ImageCoordinates](#nodebpy.nodes.compositor.input.ImageCoordinates) | Returns the coordinates of the pixels of an image |
| [ImageInfo](#nodebpy.nodes.compositor.input.ImageInfo) | Returns information about an image |
| [Mask](#nodebpy.nodes.compositor.input.Mask) | Input mask from a mask data-block, created in the image editor |
| [MovieClip](#nodebpy.nodes.compositor.input.MovieClip) | Input image or movie from a movie clip data-block, typically used for motion tracking |
| [Normal](#nodebpy.nodes.compositor.input.Normal) | Input normalized normal values to other nodes in the tree |
| [RenderLayers](#nodebpy.nodes.compositor.input.RenderLayers) | Input render passes from a scene render |
| [SceneTime](#nodebpy.nodes.compositor.input.SceneTime) | Input the current scene time in seconds or frames |
| [SequencerStripInfo](#nodebpy.nodes.compositor.input.SequencerStripInfo) | Returns information about the active strip of the modifier |
| [StringToImage](#nodebpy.nodes.compositor.input.StringToImage) | Generates an image containing the given paragraph of text |
| [TimeCurve](#nodebpy.nodes.compositor.input.TimeCurve) | Generate a factor value (from 0.0 to 1.0) between scene start and end time, using a curve mapping |
| [TrackPosition](#nodebpy.nodes.compositor.input.TrackPosition) | Provide information about motion tracking points, such as x and y values |

### BlankImage

``` python
BlankImage(color=(0.0, 0.0, 0.0, 1.0), size=(1920, 1080))
```

Returns an image with the given size and constant color

#### Parameters

| Name  | Type               | Description | Default                |
|-------|--------------------|-------------|------------------------|
| color | InputColor         | Color       | `(0.0, 0.0, 0.0, 1.0)` |
| size  | InputIntegerVector | Size        | `(1920, 1080)`         |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.BlankImage.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.BlankImage.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.BlankImage.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.BlankImage.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.BlankImage.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.BlankImage.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.color` | `ColorSocket`   | Color       |
| `i.size`  | `IntegerSocket` | Size        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### BokehImage

``` python
BokehImage(
    flaps=5,
    angle=0.0,
    roundness=0.0,
    catadioptric_size=0.0,
    color_shift=0.0,
)
```

Generate image with bokeh shape for use with the Bokeh Blur filter node

#### Parameters

| Name              | Type         | Description       | Default |
|-------------------|--------------|-------------------|---------|
| flaps             | InputInteger | Flaps             | `5`     |
| angle             | InputFloat   | Angle             | `0.0`   |
| roundness         | InputFloat   | Roundness         | `0.0`   |
| catadioptric_size | InputFloat   | Catadioptric Size | `0.0`   |
| color_shift       | InputFloat   | Color Shift       | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.BokehImage.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.BokehImage.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.BokehImage.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.BokehImage.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.BokehImage.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.BokehImage.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `i.flaps`             | `IntegerSocket` | Flaps             |
| `i.angle`             | `FloatSocket`   | Angle             |
| `i.roundness`         | `FloatSocket`   | Roundness         |
| `i.catadioptric_size` | `FloatSocket`   | Catadioptric Size |
| `i.color_shift`       | `FloatSocket`   | Color Shift       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Color

``` python
Color()
```

A color picker

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.Color.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.Color.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.Color.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.Color.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.Color.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.Color.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### ImageCoordinates

``` python
ImageCoordinates(image=None)
```

Returns the coordinates of the pixels of an image

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.ImageCoordinates.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.ImageCoordinates.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.ImageCoordinates.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.ImageCoordinates.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.ImageCoordinates.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.ImageCoordinates.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.uniform`    | `VectorSocket`  | Uniform     |
| `o.normalized` | `VectorSocket`  | Normalized  |
| `o.pixel`      | `IntegerSocket` | Pixel       |

### ImageInfo

``` python
ImageInfo(image=None)
```

Returns information about an image

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.ImageInfo.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.ImageInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.ImageInfo.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.ImageInfo.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.ImageInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.ImageInfo.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.dimensions` | `IntegerSocket` | Dimensions  |
| `o.resolution` | `IntegerSocket` | Resolution  |
| `o.location`   | `VectorSocket`  | Location    |
| `o.rotation`   | `FloatSocket`   | Rotation    |
| `o.scale`      | `VectorSocket`  | Scale       |

### Mask

``` python
Mask(
    size_source='Scene Size',
    size_x=256,
    size_y=256,
    feather=True,
    motion_blur=False,
    samples=16,
    shutter=0.5,
    *,
    mask=None,
)
```

Input mask from a mask data-block, created in the image editor

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| size_source | InputMenu \| Literal\['Scene Size', 'Fixed', 'Fixed/Scene'\] | Size Source | `'Scene Size'` |
| size_x | InputInteger | Size X | `256` |
| size_y | InputInteger | Size Y | `256` |
| feather | InputBoolean | Feather | `True` |
| motion_blur | InputBoolean | Motion Blur | `False` |
| samples | InputInteger | Samples. Renamed from `Motion Blur Samples`; `i.motion_blur_samples` still resolves to it. | `16` |
| shutter | InputFloat | Shutter. Renamed from `Motion Blur Shutter`; `i.motion_blur_shutter` still resolves to it. | `0.5` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.Mask.i) |  |
| [`mask`](#nodebpy.nodes.compositor.input.Mask.mask) |  |
| [`name`](#nodebpy.nodes.compositor.input.Mask.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.Mask.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.Mask.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.Mask.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.Mask.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type | Description |
|----|----|----|
| `i.size_source` | `MenuSocket` | Size Source |
| `i.size_x` | `IntegerSocket` | Size X |
| `i.size_y` | `IntegerSocket` | Size Y |
| `i.feather` | `BooleanSocket` | Feather |
| `i.motion_blur` | `BooleanSocket` | Motion Blur |
| `i.samples` | `IntegerSocket` | Samples. Renamed from `Motion Blur Samples`; `i.motion_blur_samples` still resolves to it. |
| `i.shutter` | `FloatSocket` | Shutter. Renamed from `Motion Blur Shutter`; `i.motion_blur_shutter` still resolves to it. |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### MovieClip

``` python
MovieClip(clip=None)
```

Input image or movie from a movie clip data-block, typically used for motion tracking

#### Attributes

| Name | Description |
|----|----|
| [`clip`](#nodebpy.nodes.compositor.input.MovieClip.clip) |  |
| [`i`](#nodebpy.nodes.compositor.input.MovieClip.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.MovieClip.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.MovieClip.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.MovieClip.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.MovieClip.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.MovieClip.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `o.image`    | `ColorSocket` | Image       |
| `o.alpha`    | `FloatSocket` | Alpha       |
| `o.offset_x` | `FloatSocket` | Offset X    |
| `o.offset_y` | `FloatSocket` | Offset Y    |
| `o.scale`    | `FloatSocket` | Scale       |
| `o.angle`    | `FloatSocket` | Angle       |

### Normal

``` python
Normal()
```

Input normalized normal values to other nodes in the tree

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.Normal.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.Normal.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.Normal.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.Normal.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.Normal.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.Normal.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.normal` | `VectorSocket` | Normal      |

### RenderLayers

``` python
RenderLayers(scene=None, layer='ViewLayer')
```

Input render passes from a scene render

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.RenderLayers.i) |  |
| [`layer`](#nodebpy.nodes.compositor.input.RenderLayers.layer) |  |
| [`name`](#nodebpy.nodes.compositor.input.RenderLayers.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.RenderLayers.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.RenderLayers.o) |  |
| [`scene`](#nodebpy.nodes.compositor.input.RenderLayers.scene) |  |
| [`tree`](#nodebpy.nodes.compositor.input.RenderLayers.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.RenderLayers.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.alpha` | `FloatSocket` | Alpha       |

### SceneTime

``` python
SceneTime()
```

Input the current scene time in seconds or frames

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.SceneTime.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.SceneTime.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.SceneTime.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.SceneTime.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.SceneTime.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.SceneTime.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `o.seconds` | `FloatSocket` | Seconds     |
| `o.frame`   | `FloatSocket` | Frame       |

### SequencerStripInfo

``` python
SequencerStripInfo()
```

Returns information about the active strip of the modifier

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.SequencerStripInfo.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.SequencerStripInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.SequencerStripInfo.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.SequencerStripInfo.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.SequencerStripInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.SequencerStripInfo.props) | Set the properties every node has and return the node, so it can |

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

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.start_frame` | `IntegerSocket` | Start Frame |
| `o.end_frame`   | `IntegerSocket` | End Frame   |
| `o.location`    | `VectorSocket`  | Location    |
| `o.rotation`    | `FloatSocket`   | Rotation    |
| `o.scale`       | `VectorSocket`  | Scale       |

### StringToImage

``` python
StringToImage(
    string='',
    font=None,
    size=128.0,
    horizontal_alignment='Center',
    vertical_alignment='Middle',
    wrap=True,
    width=1920,
)
```

Generates an image containing the given paragraph of text

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| string | InputString | String | `''` |
| font | InputFont | Font | `None` |
| size | InputFloat | Size | `128.0` |
| horizontal_alignment | InputMenu \| Literal\['Left', 'Center', 'Right'\] | Horizontal Alignment | `'Center'` |
| vertical_alignment | InputMenu \| Literal\['Top', 'Top Baseline', 'Middle', 'Bottom Baseline', 'Bottom'\] | Vertical Alignment | `'Middle'` |
| wrap | InputBoolean | Wrap | `True` |
| width | InputInteger | Width. Renamed from `Wrap Width`; `i.wrap_width` still resolves to it. | `1920` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.StringToImage.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.StringToImage.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.StringToImage.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.StringToImage.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.StringToImage.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.StringToImage.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type | Description |
|----|----|----|
| `i.string` | `StringSocket` | String |
| `i.font` | `FontSocket` | Font |
| `i.size` | `FloatSocket` | Size |
| `i.horizontal_alignment` | `MenuSocket` | Horizontal Alignment |
| `i.vertical_alignment` | `MenuSocket` | Vertical Alignment |
| `i.wrap` | `BooleanSocket` | Wrap |
| `i.width` | `IntegerSocket` | Width. Renamed from `Wrap Width`; `i.wrap_width` still resolves to it. |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `FloatSocket` | Image       |

### TimeCurve

``` python
TimeCurve(start_frame=1, end_frame=250)
```

Generate a factor value (from 0.0 to 1.0) between scene start and end time, using a curve mapping

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| start_frame | InputInteger | Start Frame | `1`     |
| end_frame   | InputInteger | End Frame   | `250`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.TimeCurve.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.TimeCurve.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.TimeCurve.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.TimeCurve.o) |  |
| [`tree`](#nodebpy.nodes.compositor.input.TimeCurve.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.TimeCurve.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.start_frame` | `IntegerSocket` | Start Frame |
| `i.end_frame`   | `IntegerSocket` | End Frame   |

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `o.factor` | `FloatSocket` | Factor. Renamed from `Fac`; `o.fac` still resolves to it. |

### TrackPosition

``` python
TrackPosition(
    mode='Absolute',
    frame=0,
    *,
    clip=None,
    tracking_object='',
    track_name='',
)
```

Provide information about motion tracking points, such as x and y values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| mode | InputMenu \| Literal\['Absolute', 'Relative Start', 'Relative Frame', 'Absolute Frame'\] | Mode | `'Absolute'` |
| frame | InputInteger | Frame | `0` |

#### Attributes

| Name | Description |
|----|----|
| [`clip`](#nodebpy.nodes.compositor.input.TrackPosition.clip) |  |
| [`i`](#nodebpy.nodes.compositor.input.TrackPosition.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.TrackPosition.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.input.TrackPosition.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.TrackPosition.o) |  |
| [`track_name`](#nodebpy.nodes.compositor.input.TrackPosition.track_name) |  |
| [`tracking_object`](#nodebpy.nodes.compositor.input.TrackPosition.tracking_object) |  |
| [`tree`](#nodebpy.nodes.compositor.input.TrackPosition.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.input.TrackPosition.props) | Set the properties every node has and return the node, so it can |

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

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.mode`  | `MenuSocket`    | Mode        |
| `i.frame` | `IntegerSocket` | Frame       |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.x`     | `FloatSocket`  | X           |
| `o.y`     | `FloatSocket`  | Y           |
| `o.speed` | `VectorSocket` | Speed       |
