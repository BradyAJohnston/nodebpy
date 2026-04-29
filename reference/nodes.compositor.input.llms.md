# nodes.compositor.input

`input`

## Classes

| Name | Description |
|----|----|
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
| [TimeCurve](#nodebpy.nodes.compositor.input.TimeCurve) | Generate a factor value (from 0.0 to 1.0) between scene start and end time, using a curve mapping |
| [TrackPosition](#nodebpy.nodes.compositor.input.TrackPosition) | Provide information about motion tracking points, such as x and y values |

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
| [`name`](#nodebpy.nodes.compositor.input.BokehImage.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.BokehImage.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.BokehImage.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.BokehImage.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.BokehImage.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.BokehImage.type) |  |

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

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.input.Color.i)             |             |
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
| [`name`](#nodebpy.nodes.compositor.input.ImageCoordinates.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.ImageCoordinates.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.ImageCoordinates.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.ImageCoordinates.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.ImageCoordinates.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.ImageCoordinates.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `o.uniform`    | `VectorSocket` | Uniform     |
| `o.normalized` | `VectorSocket` | Normalized  |
| `o.pixel`      | `VectorSocket` | Pixel       |

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
| [`name`](#nodebpy.nodes.compositor.input.ImageInfo.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.ImageInfo.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.ImageInfo.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.ImageInfo.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.ImageInfo.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.ImageInfo.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `o.dimensions` | `VectorSocket` | Dimensions  |
| `o.resolution` | `VectorSocket` | Resolution  |
| `o.location`   | `VectorSocket` | Location    |
| `o.rotation`   | `FloatSocket`  | Rotation    |
| `o.scale`      | `VectorSocket` | Scale       |

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
| [`layer`](#nodebpy.nodes.compositor.input.RenderLayers.layer) |  |
| [`name`](#nodebpy.nodes.compositor.input.RenderLayers.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.RenderLayers.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.RenderLayers.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.RenderLayers.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.RenderLayers.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.RenderLayers.type) |  |

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

### SequencerStripInfo

``` python
SequencerStripInfo()
```

Returns information about the active strip of the modifier

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.input.SequencerStripInfo.i) |  |
| [`name`](#nodebpy.nodes.compositor.input.SequencerStripInfo.name) |  |
| [`node`](#nodebpy.nodes.compositor.input.SequencerStripInfo.node) |  |
| [`o`](#nodebpy.nodes.compositor.input.SequencerStripInfo.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.input.SequencerStripInfo.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.input.SequencerStripInfo.tree) |  |
| [`type`](#nodebpy.nodes.compositor.input.SequencerStripInfo.type) |  |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.start_frame` | `IntegerSocket` | Start Frame |
| `o.end_frame`   | `IntegerSocket` | End Frame   |
| `o.location`    | `VectorSocket`  | Location    |
| `o.rotation`    | `FloatSocket`   | Rotation    |
| `o.scale`       | `VectorSocket`  | Scale       |

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
