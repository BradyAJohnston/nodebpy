# nodes.compositor.distort

`distort`

## Classes

| Name | Description |
|----|----|
| [CornerPin](#nodebpy.nodes.compositor.distort.CornerPin) | Plane warp transformation using explicit corner values |
| [Crop](#nodebpy.nodes.compositor.distort.Crop) | Crops image to a smaller region, either making the cropped area transparent or resizing the image |
| [Displace](#nodebpy.nodes.compositor.distort.Displace) | Displace pixel position using an offset vector |
| [Flip](#nodebpy.nodes.compositor.distort.Flip) | Flip an image along a defined axis |
| [LensDistortion](#nodebpy.nodes.compositor.distort.LensDistortion) | Simulate distortion and dispersion from camera lenses |
| [MapUV](#nodebpy.nodes.compositor.distort.MapUV) | Map a texture using UV coordinates, to apply a texture to objects in compositing |
| [MovieDistortion](#nodebpy.nodes.compositor.distort.MovieDistortion) | Remove lens distortion from footage, using motion tracking camera lens settings |
| [PlaneTrackDeform](#nodebpy.nodes.compositor.distort.PlaneTrackDeform) | Replace flat planes in footage by another image, detected by plane tracks from motion tracking |
| [Rotate](#nodebpy.nodes.compositor.distort.Rotate) | Rotate image by specified angle |
| [Scale](#nodebpy.nodes.compositor.distort.Scale) | Change the size of the image |
| [Stabilize2D](#nodebpy.nodes.compositor.distort.Stabilize2D) | Stabilize footage using 2D stabilization motion tracking settings |
| [Transform](#nodebpy.nodes.compositor.distort.Transform) | Scale, translate and rotate an image |
| [Translate](#nodebpy.nodes.compositor.distort.Translate) | Offset an image |

### CornerPin

``` python
CornerPin(
    image=None,
    upper_left=None,
    upper_right=None,
    lower_left=None,
    lower_right=None,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Plane warp transformation using explicit corner values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| upper_left | InputVector | Upper Left | `None` |
| upper_right | InputVector | Upper Right | `None` |
| lower_left | InputVector | Lower Left | `None` |
| lower_right | InputVector | Lower Right | `None` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.CornerPin.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.CornerPin.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.CornerPin.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.CornerPin.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.CornerPin.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.CornerPin.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.CornerPin.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.CornerPin.type) |  |

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.image`         | `ColorSocket`  | Image         |
| `i.upper_left`    | `VectorSocket` | Upper Left    |
| `i.upper_right`   | `VectorSocket` | Upper Right   |
| `i.lower_left`    | `VectorSocket` | Lower Left    |
| `i.lower_right`   | `VectorSocket` | Lower Right   |
| `i.interpolation` | `MenuSocket`   | Interpolation |
| `i.extension_x`   | `MenuSocket`   | Extension X   |
| `i.extension_y`   | `MenuSocket`   | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.plane` | `FloatSocket` | Plane       |

### Crop

``` python
Crop(image=None, x=0, y=0, width=1920, height=1080, alpha_crop=False)
```

Crops image to a smaller region, either making the cropped area transparent or resizing the image

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| image      | InputColor   | Image       | `None`  |
| x          | InputInteger | X           | `0`     |
| y          | InputInteger | Y           | `0`     |
| width      | InputInteger | Width       | `1920`  |
| height     | InputInteger | Height      | `1080`  |
| alpha_crop | InputBoolean | Alpha Crop  | `False` |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.distort.Crop.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.distort.Crop.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.distort.Crop.name)       |             |
| [`node`](#nodebpy.nodes.compositor.distort.Crop.node)       |             |
| [`o`](#nodebpy.nodes.compositor.distort.Crop.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.distort.Crop.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.distort.Crop.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.distort.Crop.type)       |             |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.image`      | `ColorSocket`   | Image       |
| `i.x`          | `IntegerSocket` | X           |
| `i.y`          | `IntegerSocket` | Y           |
| `i.width`      | `IntegerSocket` | Width       |
| `i.height`     | `IntegerSocket` | Height      |
| `i.alpha_crop` | `BooleanSocket` | Alpha Crop  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Displace

``` python
Displace(
    image=None,
    displacement=None,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Displace pixel position using an offset vector

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| displacement | InputVector | Displacement | `None` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.Displace.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.Displace.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.Displace.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.Displace.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.Displace.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.Displace.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.Displace.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.Displace.type) |  |

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.image`         | `ColorSocket`  | Image         |
| `i.displacement`  | `VectorSocket` | Displacement  |
| `i.interpolation` | `MenuSocket`   | Interpolation |
| `i.extension_x`   | `MenuSocket`   | Extension X   |
| `i.extension_y`   | `MenuSocket`   | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Flip

``` python
Flip(image=None, flip_x=False, flip_y=False)
```

Flip an image along a defined axis

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| image  | InputColor   | Image       | `None`  |
| flip_x | InputBoolean | Flip X      | `False` |
| flip_y | InputBoolean | Flip Y      | `False` |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.distort.Flip.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.distort.Flip.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.distort.Flip.name)       |             |
| [`node`](#nodebpy.nodes.compositor.distort.Flip.node)       |             |
| [`o`](#nodebpy.nodes.compositor.distort.Flip.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.distort.Flip.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.distort.Flip.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.distort.Flip.type)       |             |

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.image`  | `ColorSocket`   | Image       |
| `i.flip_x` | `BooleanSocket` | Flip X      |
| `i.flip_y` | `BooleanSocket` | Flip Y      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### LensDistortion

``` python
LensDistortion(
    image=None,
    type='Radial',
    distortion=0.0,
    dispersion=0.0,
    jitter=False,
    fit=False,
)
```

Simulate distortion and dispersion from camera lenses

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['Radial', 'Horizontal'\] | Type | `'Radial'` |
| distortion | InputFloat | Distortion | `0.0` |
| dispersion | InputFloat | Dispersion | `0.0` |
| jitter | InputBoolean | Jitter | `False` |
| fit | InputBoolean | Fit | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.LensDistortion.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.LensDistortion.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.LensDistortion.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.LensDistortion.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.LensDistortion.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.LensDistortion.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.LensDistortion.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.LensDistortion.type) |  |

#### Methods

| Name | Description |
|----|----|
| [horizontal](#nodebpy.nodes.compositor.distort.LensDistortion.horizontal) | Create Lens Distortion node with type ‘Horizontal’. |
| [radial](#nodebpy.nodes.compositor.distort.LensDistortion.radial) | Create Lens Distortion node with type ‘Radial’. |

##### horizontal

``` python
horizontal(image=None, dispersion=0.0)
```

Create Lens Distortion node with type ‘Horizontal’.

##### radial

``` python
radial(image=None, distortion=0.0, dispersion=0.0, jitter=False, fit=False)
```

Create Lens Distortion node with type ‘Radial’.

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.image`      | `ColorSocket`   | Image       |
| `i.type`       | `MenuSocket`    | Type        |
| `i.distortion` | `FloatSocket`   | Distortion  |
| `i.dispersion` | `FloatSocket`   | Dispersion  |
| `i.jitter`     | `BooleanSocket` | Jitter      |
| `i.fit`        | `BooleanSocket` | Fit         |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### MapUV

``` python
MapUV(
    image=None,
    uv=None,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Map a texture using UV coordinates, to apply a texture to objects in compositing

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| uv | InputVector | UV | `None` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.distort.MapUV.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.distort.MapUV.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.distort.MapUV.name)       |             |
| [`node`](#nodebpy.nodes.compositor.distort.MapUV.node)       |             |
| [`o`](#nodebpy.nodes.compositor.distort.MapUV.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.distort.MapUV.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.distort.MapUV.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.distort.MapUV.type)       |             |

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.image`         | `ColorSocket`  | Image         |
| `i.uv`            | `VectorSocket` | UV            |
| `i.interpolation` | `MenuSocket`   | Interpolation |
| `i.extension_x`   | `MenuSocket`   | Extension X   |
| `i.extension_y`   | `MenuSocket`   | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### MovieDistortion

``` python
MovieDistortion(image=None, type='Undistort')
```

Remove lens distortion from footage, using motion tracking camera lens settings

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['Undistort', 'Distort'\] | Type | `'Undistort'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.MovieDistortion.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.MovieDistortion.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.MovieDistortion.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.MovieDistortion.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.MovieDistortion.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.MovieDistortion.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.MovieDistortion.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.MovieDistortion.type) |  |

#### Methods

| Name | Description |
|----|----|
| [distort](#nodebpy.nodes.compositor.distort.MovieDistortion.distort) | Create Movie Distortion node with type ‘Distort’. |
| [undistort](#nodebpy.nodes.compositor.distort.MovieDistortion.undistort) | Create Movie Distortion node with type ‘Undistort’. |

##### distort

``` python
distort(image=None)
```

Create Movie Distortion node with type ‘Distort’.

##### undistort

``` python
undistort(image=None)
```

Create Movie Distortion node with type ‘Undistort’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### PlaneTrackDeform

``` python
PlaneTrackDeform(
    image=None,
    motion_blur=False,
    motion_blur_samples=16,
    motion_blur_shutter=0.5,
    *,
    tracking_object='',
    plane_track_name='',
)
```

Replace flat planes in footage by another image, detected by plane tracks from motion tracking

#### Parameters

| Name                | Type         | Description | Default |
|---------------------|--------------|-------------|---------|
| image               | InputColor   | Image       | `None`  |
| motion_blur         | InputBoolean | Motion Blur | `False` |
| motion_blur_samples | InputInteger | Samples     | `16`    |
| motion_blur_shutter | InputFloat   | Shutter     | `0.5`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.outputs) |  |
| [`plane_track_name`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.plane_track_name) |  |
| [`tracking_object`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.tracking_object) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.PlaneTrackDeform.type) |  |

**Inputs**

| Attribute               | Type            | Description |
|-------------------------|-----------------|-------------|
| `i.image`               | `ColorSocket`   | Image       |
| `i.motion_blur`         | `BooleanSocket` | Motion Blur |
| `i.motion_blur_samples` | `IntegerSocket` | Samples     |
| `i.motion_blur_shutter` | `FloatSocket`   | Shutter     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.plane` | `FloatSocket` | Plane       |

### Rotate

``` python
Rotate(
    image=None,
    angle=0.0,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Rotate image by specified angle

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| angle | InputFloat | Angle | `0.0` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.distort.Rotate.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.distort.Rotate.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.distort.Rotate.name)       |             |
| [`node`](#nodebpy.nodes.compositor.distort.Rotate.node)       |             |
| [`o`](#nodebpy.nodes.compositor.distort.Rotate.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.distort.Rotate.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.distort.Rotate.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.distort.Rotate.type)       |             |

**Inputs**

| Attribute         | Type          | Description   |
|-------------------|---------------|---------------|
| `i.image`         | `ColorSocket` | Image         |
| `i.angle`         | `FloatSocket` | Angle         |
| `i.interpolation` | `MenuSocket`  | Interpolation |
| `i.extension_x`   | `MenuSocket`  | Extension X   |
| `i.extension_y`   | `MenuSocket`  | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Scale

``` python
Scale(
    image=None,
    type='Relative',
    x=1.0,
    y=1.0,
    frame_type='Stretch',
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Change the size of the image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['Relative', 'Absolute', 'Scene Size', 'Render Size'\] | Type | `'Relative'` |
| x | InputFloat | X | `1.0` |
| y | InputFloat | Y | `1.0` |
| frame_type | InputMenu \| Literal\['Stretch', 'Fit', 'Crop'\] | Frame Type | `'Stretch'` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.distort.Scale.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.distort.Scale.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.distort.Scale.name)       |             |
| [`node`](#nodebpy.nodes.compositor.distort.Scale.node)       |             |
| [`o`](#nodebpy.nodes.compositor.distort.Scale.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.distort.Scale.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.distort.Scale.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.distort.Scale.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [absolute](#nodebpy.nodes.compositor.distort.Scale.absolute) | Create Scale node with type ‘Absolute’. |
| [relative](#nodebpy.nodes.compositor.distort.Scale.relative) | Create Scale node with type ‘Relative’. |
| [render_size](#nodebpy.nodes.compositor.distort.Scale.render_size) | Create Scale node with type ‘Render Size’. |
| [scene_size](#nodebpy.nodes.compositor.distort.Scale.scene_size) | Create Scale node with type ‘Scene Size’. |

##### absolute

``` python
absolute(
    image=None,
    x=1.0,
    y=1.0,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Create Scale node with type ‘Absolute’.

##### relative

``` python
relative(
    image=None,
    x=1.0,
    y=1.0,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Create Scale node with type ‘Relative’.

##### render_size

``` python
render_size(
    image=None,
    frame_type='Stretch',
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Create Scale node with type ‘Render Size’.

##### scene_size

``` python
scene_size(
    image=None,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Create Scale node with type ‘Scene Size’.

**Inputs**

| Attribute         | Type          | Description   |
|-------------------|---------------|---------------|
| `i.image`         | `ColorSocket` | Image         |
| `i.type`          | `MenuSocket`  | Type          |
| `i.x`             | `FloatSocket` | X             |
| `i.y`             | `FloatSocket` | Y             |
| `i.frame_type`    | `MenuSocket`  | Frame Type    |
| `i.interpolation` | `MenuSocket`  | Interpolation |
| `i.extension_x`   | `MenuSocket`  | Extension X   |
| `i.extension_y`   | `MenuSocket`  | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Stabilize2D

``` python
Stabilize2D(
    image=None,
    invert=False,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Stabilize footage using 2D stabilization motion tracking settings

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| invert | InputBoolean | Invert | `False` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.Stabilize2D.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.Stabilize2D.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.Stabilize2D.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.Stabilize2D.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.Stabilize2D.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.Stabilize2D.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.Stabilize2D.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.Stabilize2D.type) |  |

**Inputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `i.image`         | `ColorSocket`   | Image         |
| `i.invert`        | `BooleanSocket` | Invert        |
| `i.interpolation` | `MenuSocket`    | Interpolation |
| `i.extension_x`   | `MenuSocket`    | Extension X   |
| `i.extension_y`   | `MenuSocket`    | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Transform

``` python
Transform(
    image=None,
    x=0.0,
    y=0.0,
    angle=0.0,
    scale=1.0,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Scale, translate and rotate an image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| x | InputFloat | X | `0.0` |
| y | InputFloat | Y | `0.0` |
| angle | InputFloat | Angle | `0.0` |
| scale | InputFloat | Scale | `1.0` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.Transform.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.Transform.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.Transform.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.Transform.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.Transform.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.Transform.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.Transform.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.Transform.type) |  |

**Inputs**

| Attribute         | Type          | Description   |
|-------------------|---------------|---------------|
| `i.image`         | `ColorSocket` | Image         |
| `i.x`             | `FloatSocket` | X             |
| `i.y`             | `FloatSocket` | Y             |
| `i.angle`         | `FloatSocket` | Angle         |
| `i.scale`         | `FloatSocket` | Scale         |
| `i.interpolation` | `MenuSocket`  | Interpolation |
| `i.extension_x`   | `MenuSocket`  | Extension X   |
| `i.extension_y`   | `MenuSocket`  | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Translate

``` python
Translate(
    image=None,
    x=0.0,
    y=0.0,
    interpolation='Bilinear',
    extension_x='Clip',
    extension_y='Clip',
)
```

Offset an image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| x | InputFloat | X | `0.0` |
| y | InputFloat | Y | `0.0` |
| interpolation | InputMenu \| Literal\['Nearest', 'Bilinear', 'Bicubic', 'Anisotropic'\] | Interpolation | `'Bilinear'` |
| extension_x | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension X | `'Clip'` |
| extension_y | InputMenu \| Literal\['Clip', 'Extend', 'Repeat'\] | Extension Y | `'Clip'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.distort.Translate.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.distort.Translate.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.distort.Translate.name) |  |
| [`node`](#nodebpy.nodes.compositor.distort.Translate.node) |  |
| [`o`](#nodebpy.nodes.compositor.distort.Translate.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.distort.Translate.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.distort.Translate.tree) |  |
| [`type`](#nodebpy.nodes.compositor.distort.Translate.type) |  |

**Inputs**

| Attribute         | Type          | Description   |
|-------------------|---------------|---------------|
| `i.image`         | `ColorSocket` | Image         |
| `i.x`             | `FloatSocket` | X             |
| `i.y`             | `FloatSocket` | Y             |
| `i.interpolation` | `MenuSocket`  | Interpolation |
| `i.extension_x`   | `MenuSocket`  | Extension X   |
| `i.extension_y`   | `MenuSocket`  | Extension Y   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
