# nodes.compositor.filter

`filter`

## Classes

| Name | Description |
|----|----|
| [AntiAliasing](#nodebpy.nodes.compositor.filter.AntiAliasing) | Smooth away jagged edges |
| [BilateralBlur](#nodebpy.nodes.compositor.filter.BilateralBlur) | Adaptively blur image, while retaining sharp edges |
| [Blur](#nodebpy.nodes.compositor.filter.Blur) | Blur an image, using several blur modes |
| [BokehBlur](#nodebpy.nodes.compositor.filter.BokehBlur) | Generate a bokeh type blur similar to Defocus. Unlike defocus an in-focus region is defined in the compositor |
| [Convolve](#nodebpy.nodes.compositor.filter.Convolve) | Convolves an image with a kernel |
| [Defocus](#nodebpy.nodes.compositor.filter.Defocus) | Apply depth of field in 2D, using a Z depth map or mask |
| [Denoise](#nodebpy.nodes.compositor.filter.Denoise) | Denoise renders from Cycles and other ray tracing renderers |
| [Despeckle](#nodebpy.nodes.compositor.filter.Despeckle) | Smooth areas of an image in which noise is noticeable, while leaving complex areas untouched |
| [Dilateerode](#nodebpy.nodes.compositor.filter.Dilateerode) | Expand and shrink masks |
| [DirectionalBlur](#nodebpy.nodes.compositor.filter.DirectionalBlur) | Blur an image along a direction |
| [Filter](#nodebpy.nodes.compositor.filter.Filter) | Apply common image enhancement filters |
| [Glare](#nodebpy.nodes.compositor.filter.Glare) | Add lens flares, fog and glows around bright parts of the image |
| [Inpaint](#nodebpy.nodes.compositor.filter.Inpaint) | Extend borders of an image into transparent or masked regions |
| [Kuwahara](#nodebpy.nodes.compositor.filter.Kuwahara) | Apply smoothing filter that preserves edges, for stylized and painterly effects |
| [Pixelate](#nodebpy.nodes.compositor.filter.Pixelate) | Reduce detail in an image by making individual pixels more prominent, for a blocky or mosaic-like appearance |
| [VectorBlur](#nodebpy.nodes.compositor.filter.VectorBlur) | Uses the vector speed render pass to blur the image pixels in 2D |

### AntiAliasing

``` python
AntiAliasing(
    image=None,
    threshold=0.2,
    contrast_limit=2.0,
    corner_rounding=0.25,
)
```

Smooth away jagged edges

#### Parameters

| Name            | Type       | Description     | Default |
|-----------------|------------|-----------------|---------|
| image           | InputColor | Image           | `None`  |
| threshold       | InputFloat | Threshold       | `0.2`   |
| contrast_limit  | InputFloat | Contrast Limit  | `2.0`   |
| corner_rounding | InputFloat | Corner Rounding | `0.25`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.AntiAliasing.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.AntiAliasing.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.AntiAliasing.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.AntiAliasing.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.AntiAliasing.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.AntiAliasing.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.AntiAliasing.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.AntiAliasing.type) |  |

**Inputs**

| Attribute           | Type          | Description     |
|---------------------|---------------|-----------------|
| `i.image`           | `ColorSocket` | Image           |
| `i.threshold`       | `FloatSocket` | Threshold       |
| `i.contrast_limit`  | `FloatSocket` | Contrast Limit  |
| `i.corner_rounding` | `FloatSocket` | Corner Rounding |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### BilateralBlur

``` python
BilateralBlur(image=None, determinator=None, size=0, threshold=0.1)
```

Adaptively blur image, while retaining sharp edges

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| image        | InputColor   | Image        | `None`  |
| determinator | InputColor   | Determinator | `None`  |
| size         | InputInteger | Size         | `0`     |
| threshold    | InputFloat   | Threshold    | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.BilateralBlur.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.BilateralBlur.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.BilateralBlur.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.BilateralBlur.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.BilateralBlur.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.BilateralBlur.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.BilateralBlur.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.BilateralBlur.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.image`        | `ColorSocket`   | Image        |
| `i.determinator` | `ColorSocket`   | Determinator |
| `i.size`         | `IntegerSocket` | Size         |
| `i.threshold`    | `FloatSocket`   | Threshold    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Blur

``` python
Blur(
    image=None,
    size=None,
    type='Gaussian',
    extend_bounds=False,
    separable=True,
)
```

Blur an image, using several blur modes

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| size | InputVector | Size | `None` |
| type | InputMenu \| Literal\['Flat', 'Tent', 'Quadratic', 'Cubic', 'Gaussian', 'Fast Gaussian', 'Catrom', 'Mitch'\] | Type | `'Gaussian'` |
| extend_bounds | InputBoolean | Extend Bounds | `False` |
| separable | InputBoolean | Separable | `True` |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.filter.Blur.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.filter.Blur.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.filter.Blur.name)       |             |
| [`node`](#nodebpy.nodes.compositor.filter.Blur.node)       |             |
| [`o`](#nodebpy.nodes.compositor.filter.Blur.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.filter.Blur.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.filter.Blur.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.filter.Blur.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [catrom](#nodebpy.nodes.compositor.filter.Blur.catrom) | Create Blur node with type ‘Catrom’. |
| [cubic](#nodebpy.nodes.compositor.filter.Blur.cubic) | Create Blur node with type ‘Cubic’. |
| [fast_gaussian](#nodebpy.nodes.compositor.filter.Blur.fast_gaussian) | Create Blur node with type ‘Fast Gaussian’. |
| [flat](#nodebpy.nodes.compositor.filter.Blur.flat) | Create Blur node with type ‘Flat’. |
| [gaussian](#nodebpy.nodes.compositor.filter.Blur.gaussian) | Create Blur node with type ‘Gaussian’. |
| [mitch](#nodebpy.nodes.compositor.filter.Blur.mitch) | Create Blur node with type ‘Mitch’. |
| [quadratic](#nodebpy.nodes.compositor.filter.Blur.quadratic) | Create Blur node with type ‘Quadratic’. |
| [tent](#nodebpy.nodes.compositor.filter.Blur.tent) | Create Blur node with type ‘Tent’. |

##### catrom

``` python
catrom(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Catrom’.

##### cubic

``` python
cubic(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Cubic’.

##### fast_gaussian

``` python
fast_gaussian(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Fast Gaussian’.

##### flat

``` python
flat(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Flat’.

##### gaussian

``` python
gaussian(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Gaussian’.

##### mitch

``` python
mitch(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Mitch’.

##### quadratic

``` python
quadratic(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Quadratic’.

##### tent

``` python
tent(image=None, size=None, extend_bounds=False, separable=True)
```

Create Blur node with type ‘Tent’.

**Inputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `i.image`         | `ColorSocket`   | Image         |
| `i.size`          | `VectorSocket`  | Size          |
| `i.type`          | `MenuSocket`    | Type          |
| `i.extend_bounds` | `BooleanSocket` | Extend Bounds |
| `i.separable`     | `BooleanSocket` | Separable     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### BokehBlur

``` python
BokehBlur(image=None, bokeh=None, size=0.0, mask=1.0, extend_bounds=False)
```

Generate a bokeh type blur similar to Defocus. Unlike defocus an in-focus region is defined in the compositor

#### Parameters

| Name          | Type         | Description   | Default |
|---------------|--------------|---------------|---------|
| image         | InputColor   | Image         | `None`  |
| bokeh         | InputColor   | Bokeh         | `None`  |
| size          | InputFloat   | Size          | `0.0`   |
| mask          | InputFloat   | Mask          | `1.0`   |
| extend_bounds | InputBoolean | Extend Bounds | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.BokehBlur.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.BokehBlur.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.BokehBlur.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.BokehBlur.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.BokehBlur.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.BokehBlur.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.BokehBlur.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.BokehBlur.type) |  |

**Inputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `i.image`         | `ColorSocket`   | Image         |
| `i.bokeh`         | `ColorSocket`   | Bokeh         |
| `i.size`          | `FloatSocket`   | Size          |
| `i.mask`          | `FloatSocket`   | Mask          |
| `i.extend_bounds` | `BooleanSocket` | Extend Bounds |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Convolve

``` python
Convolve(
    image=None,
    kernel_data_type='Float',
    float_kernel=0.0,
    color_kernel=None,
    normalize_kernel=True,
)
```

Convolves an image with a kernel

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| kernel_data_type | InputMenu \| Literal\['Float', 'Color'\] | Kernel Data Type | `'Float'` |
| float_kernel | InputFloat | Kernel | `0.0` |
| color_kernel | InputColor | Kernel | `None` |
| normalize_kernel | InputBoolean | Normalize Kernel | `True` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.Convolve.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Convolve.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Convolve.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Convolve.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Convolve.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Convolve.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Convolve.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Convolve.type) |  |

**Inputs**

| Attribute            | Type            | Description      |
|----------------------|-----------------|------------------|
| `i.image`            | `ColorSocket`   | Image            |
| `i.kernel_data_type` | `MenuSocket`    | Kernel Data Type |
| `i.float_kernel`     | `FloatSocket`   | Kernel           |
| `i.color_kernel`     | `ColorSocket`   | Kernel           |
| `i.normalize_kernel` | `BooleanSocket` | Normalize Kernel |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Defocus

``` python
Defocus(
    image=None,
    z=1.0,
    *,
    bokeh='CIRCLE',
    angle=0.0,
    f_stop=0.0,
    blur_max=0.0,
    use_zbuffer=False,
    z_scale=0.0,
)
```

Apply depth of field in 2D, using a Z depth map or mask

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| image | InputColor | Image       | `None`  |
| z     | InputFloat | Z           | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`angle`](#nodebpy.nodes.compositor.filter.Defocus.angle) |  |
| [`blur_max`](#nodebpy.nodes.compositor.filter.Defocus.blur_max) |  |
| [`bokeh`](#nodebpy.nodes.compositor.filter.Defocus.bokeh) |  |
| [`f_stop`](#nodebpy.nodes.compositor.filter.Defocus.f_stop) |  |
| [`i`](#nodebpy.nodes.compositor.filter.Defocus.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Defocus.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Defocus.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Defocus.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Defocus.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Defocus.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Defocus.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Defocus.type) |  |
| [`use_zbuffer`](#nodebpy.nodes.compositor.filter.Defocus.use_zbuffer) |  |
| [`z_scale`](#nodebpy.nodes.compositor.filter.Defocus.z_scale) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.z`     | `FloatSocket` | Z           |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Denoise

``` python
Denoise(
    image=None,
    albedo=None,
    normal=None,
    hdr=True,
    prefilter='Accurate',
    quality='Follow Scene',
)
```

Denoise renders from Cycles and other ray tracing renderers

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| albedo | InputColor | Albedo | `None` |
| normal | InputVector | Normal | `None` |
| hdr | InputBoolean | HDR | `True` |
| prefilter | InputMenu \| Literal\['None', 'Fast', 'Accurate'\] | Prefilter | `'Accurate'` |
| quality | InputMenu \| Literal\['Follow Scene', 'High', 'Balanced', 'Fast'\] | Quality | `'Follow Scene'` |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.filter.Denoise.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.filter.Denoise.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.filter.Denoise.name)       |             |
| [`node`](#nodebpy.nodes.compositor.filter.Denoise.node)       |             |
| [`o`](#nodebpy.nodes.compositor.filter.Denoise.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.filter.Denoise.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.filter.Denoise.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.filter.Denoise.type)       |             |

**Inputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `i.image`     | `ColorSocket`   | Image       |
| `i.albedo`    | `ColorSocket`   | Albedo      |
| `i.normal`    | `VectorSocket`  | Normal      |
| `i.hdr`       | `BooleanSocket` | HDR         |
| `i.prefilter` | `MenuSocket`    | Prefilter   |
| `i.quality`   | `MenuSocket`    | Quality     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Despeckle

``` python
Despeckle(image=None, fac=1.0, color_threshold=0.5, neighbor_threshold=0.5)
```

Smooth areas of an image in which noise is noticeable, while leaving complex areas untouched

#### Parameters

| Name               | Type       | Description        | Default |
|--------------------|------------|--------------------|---------|
| image              | InputColor | Image              | `None`  |
| fac                | InputFloat | Factor             | `1.0`   |
| color_threshold    | InputFloat | Color Threshold    | `0.5`   |
| neighbor_threshold | InputFloat | Neighbor Threshold | `0.5`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.Despeckle.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Despeckle.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Despeckle.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Despeckle.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Despeckle.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Despeckle.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Despeckle.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Despeckle.type) |  |

**Inputs**

| Attribute              | Type          | Description        |
|------------------------|---------------|--------------------|
| `i.image`              | `ColorSocket` | Image              |
| `i.fac`                | `FloatSocket` | Factor             |
| `i.color_threshold`    | `FloatSocket` | Color Threshold    |
| `i.neighbor_threshold` | `FloatSocket` | Neighbor Threshold |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Dilateerode

``` python
Dilateerode(mask=0.0, size=0, type='Steps', falloff_size=0.0, falloff='Smooth')
```

Expand and shrink masks

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| mask | InputFloat | Mask | `0.0` |
| size | InputInteger | Size | `0` |
| type | InputMenu \| Literal\['Steps', 'Threshold', 'Distance', 'Feather'\] | Type | `'Steps'` |
| falloff_size | InputFloat | Falloff Size | `0.0` |
| falloff | InputMenu \| Literal\['Smooth', 'Sphere', 'Root', 'Inverse Square', 'Sharp', 'Linear'\] | Falloff | `'Smooth'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.Dilateerode.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Dilateerode.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Dilateerode.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Dilateerode.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Dilateerode.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Dilateerode.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Dilateerode.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Dilateerode.type) |  |

#### Methods

| Name | Description |
|----|----|
| [distance](#nodebpy.nodes.compositor.filter.Dilateerode.distance) | Create Dilate/Erode node with type ‘Distance’. |
| [feather](#nodebpy.nodes.compositor.filter.Dilateerode.feather) | Create Dilate/Erode node with type ‘Feather’. |
| [steps](#nodebpy.nodes.compositor.filter.Dilateerode.steps) | Create Dilate/Erode node with type ‘Steps’. |
| [threshold](#nodebpy.nodes.compositor.filter.Dilateerode.threshold) | Create Dilate/Erode node with type ‘Threshold’. |

##### distance

``` python
distance(mask=0.0, size=0)
```

Create Dilate/Erode node with type ‘Distance’.

##### feather

``` python
feather(mask=0.0, size=0, falloff='Smooth')
```

Create Dilate/Erode node with type ‘Feather’.

##### steps

``` python
steps(mask=0.0, size=0)
```

Create Dilate/Erode node with type ‘Steps’.

##### threshold

``` python
threshold(mask=0.0, size=0, falloff_size=0.0)
```

Create Dilate/Erode node with type ‘Threshold’.

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.mask`         | `FloatSocket`   | Mask         |
| `i.size`         | `IntegerSocket` | Size         |
| `i.type`         | `MenuSocket`    | Type         |
| `i.falloff_size` | `FloatSocket`   | Falloff Size |
| `i.falloff`      | `MenuSocket`    | Falloff      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### DirectionalBlur

``` python
DirectionalBlur(
    image=None,
    samples=1,
    center=None,
    rotation=0.0,
    scale=1.0,
    translation_amount=0.0,
    translation_direction=0.0,
)
```

Blur an image along a direction

#### Parameters

| Name                  | Type         | Description | Default |
|-----------------------|--------------|-------------|---------|
| image                 | InputColor   | Image       | `None`  |
| samples               | InputInteger | Samples     | `1`     |
| center                | InputVector  | Center      | `None`  |
| rotation              | InputFloat   | Rotation    | `0.0`   |
| scale                 | InputFloat   | Scale       | `1.0`   |
| translation_amount    | InputFloat   | Amount      | `0.0`   |
| translation_direction | InputFloat   | Direction   | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.DirectionalBlur.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.DirectionalBlur.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.DirectionalBlur.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.DirectionalBlur.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.DirectionalBlur.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.DirectionalBlur.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.DirectionalBlur.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.DirectionalBlur.type) |  |

**Inputs**

| Attribute                 | Type            | Description |
|---------------------------|-----------------|-------------|
| `i.image`                 | `ColorSocket`   | Image       |
| `i.samples`               | `IntegerSocket` | Samples     |
| `i.center`                | `VectorSocket`  | Center      |
| `i.rotation`              | `FloatSocket`   | Rotation    |
| `i.scale`                 | `FloatSocket`   | Scale       |
| `i.translation_amount`    | `FloatSocket`   | Amount      |
| `i.translation_direction` | `FloatSocket`   | Direction   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Filter

``` python
Filter(image=None, fac=1.0, type='Soften')
```

Apply common image enhancement filters

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| fac | InputFloat | Factor | `1.0` |
| type | InputMenu \| Literal\['Soften', 'Box Sharpen', 'Diamond Sharpen', 'Laplace', 'Sobel', 'Prewitt', 'Kirsch', 'Shadow'\] | Type | `'Soften'` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.filter.Filter.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.filter.Filter.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.filter.Filter.name)       |             |
| [`node`](#nodebpy.nodes.compositor.filter.Filter.node)       |             |
| [`o`](#nodebpy.nodes.compositor.filter.Filter.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.filter.Filter.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.filter.Filter.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.filter.Filter.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [box_sharpen](#nodebpy.nodes.compositor.filter.Filter.box_sharpen) | Create Filter node with type ‘Box Sharpen’. |
| [diamond_sharpen](#nodebpy.nodes.compositor.filter.Filter.diamond_sharpen) | Create Filter node with type ‘Diamond Sharpen’. |
| [kirsch](#nodebpy.nodes.compositor.filter.Filter.kirsch) | Create Filter node with type ‘Kirsch’. |
| [laplace](#nodebpy.nodes.compositor.filter.Filter.laplace) | Create Filter node with type ‘Laplace’. |
| [prewitt](#nodebpy.nodes.compositor.filter.Filter.prewitt) | Create Filter node with type ‘Prewitt’. |
| [shadow](#nodebpy.nodes.compositor.filter.Filter.shadow) | Create Filter node with type ‘Shadow’. |
| [sobel](#nodebpy.nodes.compositor.filter.Filter.sobel) | Create Filter node with type ‘Sobel’. |
| [soften](#nodebpy.nodes.compositor.filter.Filter.soften) | Create Filter node with type ‘Soften’. |

##### box_sharpen

``` python
box_sharpen(image=None, fac=1.0)
```

Create Filter node with type ‘Box Sharpen’.

##### diamond_sharpen

``` python
diamond_sharpen(image=None, fac=1.0)
```

Create Filter node with type ‘Diamond Sharpen’.

##### kirsch

``` python
kirsch(image=None, fac=1.0)
```

Create Filter node with type ‘Kirsch’.

##### laplace

``` python
laplace(image=None, fac=1.0)
```

Create Filter node with type ‘Laplace’.

##### prewitt

``` python
prewitt(image=None, fac=1.0)
```

Create Filter node with type ‘Prewitt’.

##### shadow

``` python
shadow(image=None, fac=1.0)
```

Create Filter node with type ‘Shadow’.

##### sobel

``` python
sobel(image=None, fac=1.0)
```

Create Filter node with type ‘Sobel’.

##### soften

``` python
soften(image=None, fac=1.0)
```

Create Filter node with type ‘Soften’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.fac`   | `FloatSocket` | Factor      |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Glare

``` python
Glare(
    image=None,
    type='Streaks',
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    maximum_highlights=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    size=0.5,
    streaks=4,
    streaks_angle=0.0,
    iterations=3,
    fade=0.9,
    color_modulation=0.25,
    diagonal_star=True,
    sun_position=None,
    jitter=0.0,
    kernel_data_type='Float',
    float_kernel=0.0,
    color_kernel=None,
)
```

Add lens flares, fog and glows around bright parts of the image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['Bloom', 'Ghosts', 'Streaks', 'Fog Glow', 'Simple Star', 'Sun Beams', 'Kernel'\] | Type | `'Streaks'` |
| quality | InputMenu \| Literal\['High', 'Medium', 'Low'\] | Quality | `'Medium'` |
| highlights_threshold | InputFloat | Threshold | `1.0` |
| highlights_smoothness | InputFloat | Smoothness | `0.1` |
| clamp_highlights | InputBoolean | Clamp | `False` |
| maximum_highlights | InputFloat | Maximum | `10.0` |
| strength | InputFloat | Strength | `1.0` |
| saturation | InputFloat | Saturation | `1.0` |
| tint | InputColor | Tint | `None` |
| size | InputFloat | Size | `0.5` |
| streaks | InputInteger | Streaks | `4` |
| streaks_angle | InputFloat | Streaks Angle | `0.0` |
| iterations | InputInteger | Iterations | `3` |
| fade | InputFloat | Fade | `0.9` |
| color_modulation | InputFloat | Color Modulation | `0.25` |
| diagonal_star | InputBoolean | Diagonal | `True` |
| sun_position | InputVector | Sun Position | `None` |
| jitter | InputFloat | Jitter | `0.0` |
| kernel_data_type | InputMenu \| Literal\['Float', 'Color'\] | Kernel Data Type | `'Float'` |
| float_kernel | InputFloat | Kernel | `0.0` |
| color_kernel | InputColor | Kernel | `None` |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.filter.Glare.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.filter.Glare.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.filter.Glare.name)       |             |
| [`node`](#nodebpy.nodes.compositor.filter.Glare.node)       |             |
| [`o`](#nodebpy.nodes.compositor.filter.Glare.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.filter.Glare.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.filter.Glare.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.filter.Glare.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [bloom](#nodebpy.nodes.compositor.filter.Glare.bloom) | Create Glare node with type ‘Bloom’. |
| [fog_glow](#nodebpy.nodes.compositor.filter.Glare.fog_glow) | Create Glare node with type ‘Fog Glow’. |
| [ghosts](#nodebpy.nodes.compositor.filter.Glare.ghosts) | Create Glare node with type ‘Ghosts’. |
| [kernel](#nodebpy.nodes.compositor.filter.Glare.kernel) | Create Glare node with type ‘Kernel’. |
| [simple_star](#nodebpy.nodes.compositor.filter.Glare.simple_star) | Create Glare node with type ‘Simple Star’. |
| [streaks](#nodebpy.nodes.compositor.filter.Glare.streaks) | Create Glare node with type ‘Streaks’. |
| [sun_beams](#nodebpy.nodes.compositor.filter.Glare.sun_beams) | Create Glare node with type ‘Sun Beams’. |

##### bloom

``` python
bloom(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    size=0.5,
)
```

Create Glare node with type ‘Bloom’.

##### fog_glow

``` python
fog_glow(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    size=0.5,
)
```

Create Glare node with type ‘Fog Glow’.

##### ghosts

``` python
ghosts(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    iterations=3,
    color_modulation=0.25,
)
```

Create Glare node with type ‘Ghosts’.

##### kernel

``` python
kernel(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    kernel_data_type='Float',
    float_kernel=0.0,
)
```

Create Glare node with type ‘Kernel’.

##### simple_star

``` python
simple_star(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    iterations=3,
    fade=0.9,
    diagonal_star=True,
)
```

Create Glare node with type ‘Simple Star’.

##### streaks

``` python
streaks(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    streaks=4,
    streaks_angle=0.0,
    iterations=3,
    fade=0.9,
    color_modulation=0.25,
)
```

Create Glare node with type ‘Streaks’.

##### sun_beams

``` python
sun_beams(
    image=None,
    quality='Medium',
    highlights_threshold=1.0,
    highlights_smoothness=0.1,
    clamp_highlights=False,
    max=10.0,
    strength=1.0,
    saturation=1.0,
    tint=None,
    size=0.5,
    sun_position=None,
    jitter=0.0,
)
```

Create Glare node with type ‘Sun Beams’.

**Inputs**

| Attribute                 | Type            | Description      |
|---------------------------|-----------------|------------------|
| `i.image`                 | `ColorSocket`   | Image            |
| `i.type`                  | `MenuSocket`    | Type             |
| `i.quality`               | `MenuSocket`    | Quality          |
| `i.highlights_threshold`  | `FloatSocket`   | Threshold        |
| `i.highlights_smoothness` | `FloatSocket`   | Smoothness       |
| `i.clamp_highlights`      | `BooleanSocket` | Clamp            |
| `i.maximum_highlights`    | `FloatSocket`   | Maximum          |
| `i.strength`              | `FloatSocket`   | Strength         |
| `i.saturation`            | `FloatSocket`   | Saturation       |
| `i.tint`                  | `ColorSocket`   | Tint             |
| `i.size`                  | `FloatSocket`   | Size             |
| `i.streaks`               | `IntegerSocket` | Streaks          |
| `i.streaks_angle`         | `FloatSocket`   | Streaks Angle    |
| `i.iterations`            | `IntegerSocket` | Iterations       |
| `i.fade`                  | `FloatSocket`   | Fade             |
| `i.color_modulation`      | `FloatSocket`   | Color Modulation |
| `i.diagonal_star`         | `BooleanSocket` | Diagonal         |
| `i.sun_position`          | `VectorSocket`  | Sun Position     |
| `i.jitter`                | `FloatSocket`   | Jitter           |
| `i.kernel_data_type`      | `MenuSocket`    | Kernel Data Type |
| `i.float_kernel`          | `FloatSocket`   | Kernel           |
| `i.color_kernel`          | `ColorSocket`   | Kernel           |

**Outputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `o.image`      | `ColorSocket` | Image       |
| `o.glare`      | `ColorSocket` | Glare       |
| `o.highlights` | `ColorSocket` | Highlights  |

### Inpaint

``` python
Inpaint(image=None, size=0)
```

Extend borders of an image into transparent or masked regions

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| image | InputColor   | Image       | `None`  |
| size  | InputInteger | Size        | `0`     |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.filter.Inpaint.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.filter.Inpaint.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.filter.Inpaint.name)       |             |
| [`node`](#nodebpy.nodes.compositor.filter.Inpaint.node)       |             |
| [`o`](#nodebpy.nodes.compositor.filter.Inpaint.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.filter.Inpaint.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.filter.Inpaint.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.filter.Inpaint.type)       |             |

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.image` | `ColorSocket`   | Image       |
| `i.size`  | `IntegerSocket` | Size        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Kuwahara

``` python
Kuwahara(
    image=None,
    size=6.0,
    type='Anisotropic',
    uniformity=4,
    sharpness=1.0,
    eccentricity=1.0,
    high_precision=False,
)
```

Apply smoothing filter that preserves edges, for stylized and painterly effects

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| size | InputFloat | Size | `6.0` |
| type | InputMenu \| Literal\['Classic', 'Anisotropic'\] | Type | `'Anisotropic'` |
| uniformity | InputInteger | Uniformity | `4` |
| sharpness | InputFloat | Sharpness | `1.0` |
| eccentricity | InputFloat | Eccentricity | `1.0` |
| high_precision | InputBoolean | High Precision | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.Kuwahara.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Kuwahara.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Kuwahara.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Kuwahara.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Kuwahara.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Kuwahara.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Kuwahara.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Kuwahara.type) |  |

#### Methods

| Name | Description |
|----|----|
| [anisotropic](#nodebpy.nodes.compositor.filter.Kuwahara.anisotropic) | Create Kuwahara node with type ‘Anisotropic’. |
| [classic](#nodebpy.nodes.compositor.filter.Kuwahara.classic) | Create Kuwahara node with type ‘Classic’. |

##### anisotropic

``` python
anisotropic(image=None, size=6.0, uniformity=4, sharpness=1.0, eccentricity=1.0)
```

Create Kuwahara node with type ‘Anisotropic’.

##### classic

``` python
classic(image=None, size=6.0, high_precision=False)
```

Create Kuwahara node with type ‘Classic’.

**Inputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `i.image`          | `ColorSocket`   | Image          |
| `i.size`           | `FloatSocket`   | Size           |
| `i.type`           | `MenuSocket`    | Type           |
| `i.uniformity`     | `IntegerSocket` | Uniformity     |
| `i.sharpness`      | `FloatSocket`   | Sharpness      |
| `i.eccentricity`   | `FloatSocket`   | Eccentricity   |
| `i.high_precision` | `BooleanSocket` | High Precision |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Pixelate

``` python
Pixelate(color=None, size=1)
```

Reduce detail in an image by making individual pixels more prominent, for a blocky or mosaic-like appearance

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| color | InputColor   | Color       | `None`  |
| size  | InputInteger | Size        | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.Pixelate.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.Pixelate.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.Pixelate.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.Pixelate.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.Pixelate.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.Pixelate.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.Pixelate.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.Pixelate.type) |  |

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.color` | `ColorSocket`   | Color       |
| `i.size`  | `IntegerSocket` | Size        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### VectorBlur

``` python
VectorBlur(image=None, speed=None, z=0.0, samples=32, shutter=0.5)
```

Uses the vector speed render pass to blur the image pixels in 2D

#### Parameters

| Name    | Type         | Description | Default |
|---------|--------------|-------------|---------|
| image   | InputColor   | Image       | `None`  |
| speed   | InputVector  | Speed       | `None`  |
| z       | InputFloat   | Z           | `0.0`   |
| samples | InputInteger | Samples     | `32`    |
| shutter | InputFloat   | Shutter     | `0.5`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.filter.VectorBlur.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.filter.VectorBlur.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.filter.VectorBlur.name) |  |
| [`node`](#nodebpy.nodes.compositor.filter.VectorBlur.node) |  |
| [`o`](#nodebpy.nodes.compositor.filter.VectorBlur.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.filter.VectorBlur.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.filter.VectorBlur.tree) |  |
| [`type`](#nodebpy.nodes.compositor.filter.VectorBlur.type) |  |

**Inputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `i.image`   | `ColorSocket`   | Image       |
| `i.speed`   | `VectorSocket`  | Speed       |
| `i.z`       | `FloatSocket`   | Z           |
| `i.samples` | `IntegerSocket` | Samples     |
| `i.shutter` | `FloatSocket`   | Shutter     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
