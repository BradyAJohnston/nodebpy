# nodes.compositor.input

`input`

## Classes

| Name | Description |
|----|----|
| [Color](#nodebpy.nodes.compositor.input.Color) | A color picker |
| [Mask](#nodebpy.nodes.compositor.input.Mask) | Input mask from a mask data-block, created in the image editor |
| [MovieClip](#nodebpy.nodes.compositor.input.MovieClip) | Input image or movie from a movie clip data-block, typically used for motion tracking |
| [Normal](#nodebpy.nodes.compositor.input.Normal) | Input normalized normal values to other nodes in the tree |
| [RenderLayers](#nodebpy.nodes.compositor.input.RenderLayers) | Input render passes from a scene render |
| [SceneTime](#nodebpy.nodes.compositor.input.SceneTime) | Input the current scene time in seconds or frames |
| [TimeCurve](#nodebpy.nodes.compositor.input.TimeCurve) | Generate a factor value (from 0.0 to 1.0) between scene start and end time, using a curve mapping |
| [TrackPosition](#nodebpy.nodes.compositor.input.TrackPosition) | Provide information about motion tracking points, such as x and y values |

### Color

``` python
Color()
```

A color picker

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.input.Color.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.input.Color.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.input.Color.name)       |             |
| [`node`](#nodebpy.nodes.compositor.input.Color.node)       |             |
| [`o`](#nodebpy.nodes.compositor.input.Color.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.input.Color.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.input.Color.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.input.Color.type)       |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### Mask

``` python
Mask(
    size_source='Scene Size',
    size_x=256,
    size_y=256,
    feather=True,
    motion_blur=False,
    motion_blur_samples=16,
    motion_blur_shutter=0.5,
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
| motion_blur_samples | InputInteger | Samples | `16` |
| motion_blur_shutter | InputFloat | Shutter | `0.5` |

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.input.Mask.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.input.Mask.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.input.Mask.name)       |             |
| [`node`](#nodebpy.nodes.compositor.input.Mask.node)       |             |
| [`o`](#nodebpy.nodes.compositor.input.Mask.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.input.Mask.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.input.Mask.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.input.Mask.type)       |             |

**Inputs**

| Attribute               | Type            | Description |
|-------------------------|-----------------|-------------|
| `i.size_source`         | `MenuSocket`    | Size Source |
| `i.size_x`              | `IntegerSocket` | Size X      |
| `i.size_y`              | `IntegerSocket` | Size Y      |
| `i.feather`             | `BooleanSocket` | Feather     |
| `i.motion_blur`         | `BooleanSocket` | Motion Blur |
| `i.motion_blur_samples` | `IntegerSocket` | Samples     |
| `i.motion_blur_shutter` | `FloatSocket`   | Shutter     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### MovieClip

``` python
MovieClip()
```

Input image or movie from a movie clip data-block, typically used for motion tracking

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.MovieClip.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.input.MovieClip.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.input.MovieClip.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.MovieClip.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.MovieClip.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.MovieClip.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.MovieClip.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.MovieClip.type) |  |

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

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.input.Normal.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.input.Normal.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.input.Normal.name)       |             |
| [`node`](#nodebpy.nodes.compositor.input.Normal.node)       |             |
| [`o`](#nodebpy.nodes.compositor.input.Normal.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.input.Normal.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.input.Normal.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.input.Normal.type)       |             |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.normal` | `VectorSocket` | Normal      |

### RenderLayers

``` python
RenderLayers(layer='ViewLayer')
```

Input render passes from a scene render

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.RenderLayers.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.input.RenderLayers.inputs) |  |
| [`layer`](#nodebpy.nodes.compositor.input.RenderLayers.layer) |  |
| [`name`](#nodebpy.nodes.compositor.input.RenderLayers.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.RenderLayers.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.RenderLayers.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.RenderLayers.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.RenderLayers.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.RenderLayers.type) |  |

**Outputs**

| Attribute                 | Type           | Description           |
|---------------------------|----------------|-----------------------|
| `o.image`                 | `ColorSocket`  | Image                 |
| `o.alpha`                 | `FloatSocket`  | Alpha                 |
| `o.depth`                 | `FloatSocket`  | Depth                 |
| `o.normal`                | `VectorSocket` | Normal                |
| `o.uv`                    | `VectorSocket` | UV                    |
| `o.vector`                | `VectorSocket` | Vector                |
| `o.position`              | `VectorSocket` | Position              |
| `o.deprecated`            | `ColorSocket`  | Deprecated            |
| `o.deprecated_001`        | `ColorSocket`  | Deprecated            |
| `o.shadow`                | `ColorSocket`  | Shadow                |
| `o.ambient_occlusion`     | `ColorSocket`  | Ambient Occlusion     |
| `o.deprecated_002`        | `ColorSocket`  | Deprecated            |
| `o.deprecated_003`        | `ColorSocket`  | Deprecated            |
| `o.deprecated_004`        | `ColorSocket`  | Deprecated            |
| `o.object_index`          | `FloatSocket`  | Object Index          |
| `o.material_index`        | `FloatSocket`  | Material Index        |
| `o.mist`                  | `FloatSocket`  | Mist                  |
| `o.emission`              | `ColorSocket`  | Emission              |
| `o.environment`           | `ColorSocket`  | Environment           |
| `o.diffuse_direct`        | `ColorSocket`  | Diffuse Direct        |
| `o.diffuse_indirect`      | `ColorSocket`  | Diffuse Indirect      |
| `o.diffuse_color`         | `ColorSocket`  | Diffuse Color         |
| `o.glossy_direct`         | `ColorSocket`  | Glossy Direct         |
| `o.glossy_indirect`       | `ColorSocket`  | Glossy Indirect       |
| `o.glossy_color`          | `ColorSocket`  | Glossy Color          |
| `o.transmission_direct`   | `ColorSocket`  | Transmission Direct   |
| `o.transmission_indirect` | `ColorSocket`  | Transmission Indirect |
| `o.transmission_color`    | `ColorSocket`  | Transmission Color    |
| `o.subsurface_direct`     | `ColorSocket`  | Subsurface Direct     |
| `o.subsurface_indirect`   | `ColorSocket`  | Subsurface Indirect   |
| `o.subsurface_color`      | `ColorSocket`  | Subsurface Color      |

### SceneTime

``` python
SceneTime()
```

Input the current scene time in seconds or frames

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.SceneTime.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.input.SceneTime.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.input.SceneTime.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.SceneTime.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.SceneTime.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.SceneTime.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.SceneTime.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.SceneTime.type) |  |

**Outputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `o.seconds` | `FloatSocket` | Seconds     |
| `o.frame`   | `FloatSocket` | Frame       |

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
| [`inputs`](#nodebpy.nodes.compositor.input.TimeCurve.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.input.TimeCurve.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.TimeCurve.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.TimeCurve.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.TimeCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.TimeCurve.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.TimeCurve.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.start_frame` | `IntegerSocket` | Start Frame |
| `i.end_frame`   | `IntegerSocket` | End Frame   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.fac`   | `FloatSocket` | Factor      |

### TrackPosition

``` python
TrackPosition(mode='Absolute', frame=0, *, tracking_object='', track_name='')
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
| [`i`](#nodebpy.nodes.compositor.input.TrackPosition.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.input.TrackPosition.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.input.TrackPosition.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.TrackPosition.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.TrackPosition.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.TrackPosition.outputs) |  |
| [`track_name`](#nodebpy.nodes.compositor.input.TrackPosition.track_name) |  |
| [`tracking_object`](#nodebpy.nodes.compositor.input.TrackPosition.tracking_object) |  |
| [`tree`](#nodebpy.nodes.compositor.input.TrackPosition.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.TrackPosition.type) |  |

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
