# nodes.compositor.matte

`matte`

## Classes

| Name | Description |
|----|----|
| [BoxMask](#nodebpy.nodes.compositor.matte.BoxMask) | Create rectangular mask suitable for use as a simple matte |
| [ChannelKey](#nodebpy.nodes.compositor.matte.ChannelKey) | Create matte based on differences in color channels |
| [ChromaKey](#nodebpy.nodes.compositor.matte.ChromaKey) | Create matte based on chroma values |
| [ColorKey](#nodebpy.nodes.compositor.matte.ColorKey) | Create matte using a given color, for green or blue screen footage |
| [ColorSpill](#nodebpy.nodes.compositor.matte.ColorSpill) | Remove colors from a blue or green screen, by reducing one RGB channel compared to the others |
| [DifferenceKey](#nodebpy.nodes.compositor.matte.DifferenceKey) | Produce a matte that isolates foreground content by comparing it with a reference background image |
| [DistanceKey](#nodebpy.nodes.compositor.matte.DistanceKey) | Create matte based on 3D distance between colors |
| [DoubleEdgeMask](#nodebpy.nodes.compositor.matte.DoubleEdgeMask) | Create a gradient between two masks |
| [EllipseMask](#nodebpy.nodes.compositor.matte.EllipseMask) | Create elliptical mask suitable for use as a simple matte or vignette mask |
| [Keying](#nodebpy.nodes.compositor.matte.Keying) | Perform both chroma keying (to remove the backdrop) and despill (to correct color cast from the backdrop) |
| [KeyingScreen](#nodebpy.nodes.compositor.matte.KeyingScreen) | Create plates for use as a color reference for keying nodes |
| [LuminanceKey](#nodebpy.nodes.compositor.matte.LuminanceKey) | Create a matte based on luminance (brightness) difference |

### BoxMask

``` python
BoxMask(
    operation='Add',
    mask=0.0,
    value=1.0,
    position=None,
    size=None,
    rotation=0.0,
)
```

Create rectangular mask suitable for use as a simple matte

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| operation | InputMenu \| Literal\['Add', 'Subtract', 'Multiply', 'Not'\] | Operation | `'Add'` |
| mask | InputFloat | Mask | `0.0` |
| value | InputFloat | Value | `1.0` |
| position | InputVector | Position | `None` |
| size | InputVector | Size | `None` |
| rotation | InputFloat | Rotation | `0.0` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.matte.BoxMask.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.matte.BoxMask.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.matte.BoxMask.name)       |             |
| [`node`](#nodebpy.nodes.compositor.matte.BoxMask.node)       |             |
| [`o`](#nodebpy.nodes.compositor.matte.BoxMask.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.matte.BoxMask.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.matte.BoxMask.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.matte.BoxMask.type)       |             |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.operation` | `MenuSocket`   | Operation   |
| `i.mask`      | `FloatSocket`  | Mask        |
| `i.value`     | `FloatSocket`  | Value       |
| `i.position`  | `VectorSocket` | Position    |
| `i.size`      | `VectorSocket` | Size        |
| `i.rotation`  | `FloatSocket`  | Rotation    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### ChannelKey

``` python
ChannelKey(
    image=None,
    minimum=0.0,
    maximum=1.0,
    color_space='RGB',
    rgb_key_channel='G',
    hsv_key_channel='H',
    yuv_key_channel='V',
    ycbcr_key_channel='Cr',
    limit_method='Max',
    rgb_limit_channel='R',
    hsv_limit_channel='S',
    yuv_limit_channel='U',
    ycbcr_limit_channel='Cb',
)
```

Create matte based on differences in color channels

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| minimum | InputFloat | Minimum | `0.0` |
| maximum | InputFloat | Maximum | `1.0` |
| color_space | InputMenu \| Literal\['RGB', 'HSV', 'YUV', 'YCbCr'\] | Color Space | `'RGB'` |
| rgb_key_channel | InputMenu \| Literal\['R', 'G', 'B'\] | RGB Key Channel | `'G'` |
| hsv_key_channel | InputMenu \| Literal\['H', 'S', 'V'\] | HSV Key Channel | `'H'` |
| yuv_key_channel | InputMenu \| Literal\['Y', 'U', 'V'\] | YUV Key Channel | `'V'` |
| ycbcr_key_channel | InputMenu \| Literal\['Y', 'Cb', 'Cr'\] | YCbCr Key Channel | `'Cr'` |
| limit_method | InputMenu \| Literal\['Single', 'Max'\] | Limit Method | `'Max'` |
| rgb_limit_channel | InputMenu \| Literal\['R', 'G', 'B'\] | RGB Limit Channel | `'R'` |
| hsv_limit_channel | InputMenu \| Literal\['H', 'S', 'V'\] | HSV Limit Channel | `'S'` |
| yuv_limit_channel | InputMenu \| Literal\['Y', 'U', 'V'\] | YUV Limit Channel | `'U'` |
| ycbcr_limit_channel | InputMenu \| Literal\['Y', 'Cb', 'Cr'\] | YCbCr Limit Channel | `'Cb'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.ChannelKey.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.ChannelKey.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.ChannelKey.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.ChannelKey.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.ChannelKey.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.ChannelKey.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.ChannelKey.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.ChannelKey.type) |  |

**Inputs**

| Attribute               | Type          | Description         |
|-------------------------|---------------|---------------------|
| `i.image`               | `ColorSocket` | Image               |
| `i.minimum`             | `FloatSocket` | Minimum             |
| `i.maximum`             | `FloatSocket` | Maximum             |
| `i.color_space`         | `MenuSocket`  | Color Space         |
| `i.rgb_key_channel`     | `MenuSocket`  | RGB Key Channel     |
| `i.hsv_key_channel`     | `MenuSocket`  | HSV Key Channel     |
| `i.yuv_key_channel`     | `MenuSocket`  | YUV Key Channel     |
| `i.ycbcr_key_channel`   | `MenuSocket`  | YCbCr Key Channel   |
| `i.limit_method`        | `MenuSocket`  | Limit Method        |
| `i.rgb_limit_channel`   | `MenuSocket`  | RGB Limit Channel   |
| `i.hsv_limit_channel`   | `MenuSocket`  | HSV Limit Channel   |
| `i.yuv_limit_channel`   | `MenuSocket`  | YUV Limit Channel   |
| `i.ycbcr_limit_channel` | `MenuSocket`  | YCbCr Limit Channel |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |

### ChromaKey

``` python
ChromaKey(
    image=None,
    key_color=None,
    minimum=0.1745,
    maximum=0.5236,
    falloff=1.0,
)
```

Create matte based on chroma values

#### Parameters

| Name      | Type       | Description | Default  |
|-----------|------------|-------------|----------|
| image     | InputColor | Image       | `None`   |
| key_color | InputColor | Key Color   | `None`   |
| minimum   | InputFloat | Minimum     | `0.1745` |
| maximum   | InputFloat | Maximum     | `0.5236` |
| falloff   | InputFloat | Falloff     | `1.0`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.ChromaKey.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.ChromaKey.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.ChromaKey.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.ChromaKey.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.ChromaKey.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.ChromaKey.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.ChromaKey.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.ChromaKey.type) |  |

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.image`     | `ColorSocket` | Image       |
| `i.key_color` | `ColorSocket` | Key Color   |
| `i.minimum`   | `FloatSocket` | Minimum     |
| `i.maximum`   | `FloatSocket` | Maximum     |
| `i.falloff`   | `FloatSocket` | Falloff     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |

### ColorKey

``` python
ColorKey(image=None, key_color=None, hue=0.01, saturation=0.1, value=0.1)
```

Create matte using a given color, for green or blue screen footage

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| image      | InputColor | Image       | `None`  |
| key_color  | InputColor | Key Color   | `None`  |
| hue        | InputFloat | Hue         | `0.01`  |
| saturation | InputFloat | Saturation  | `0.1`   |
| value      | InputFloat | Value       | `0.1`   |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.matte.ColorKey.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.matte.ColorKey.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.matte.ColorKey.name)       |             |
| [`node`](#nodebpy.nodes.compositor.matte.ColorKey.node)       |             |
| [`o`](#nodebpy.nodes.compositor.matte.ColorKey.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.matte.ColorKey.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.matte.ColorKey.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.matte.ColorKey.type)       |             |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.image`      | `ColorSocket` | Image       |
| `i.key_color`  | `ColorSocket` | Key Color   |
| `i.hue`        | `FloatSocket` | Hue         |
| `i.saturation` | `FloatSocket` | Saturation  |
| `i.value`      | `FloatSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |

### ColorSpill

``` python
ColorSpill(
    image=None,
    fac=1.0,
    spill_channel='G',
    limit_method='Single',
    limit_channel='R',
    limit_strength=1.0,
    use_spill_strength=False,
    spill_strength=None,
)
```

Remove colors from a blue or green screen, by reducing one RGB channel compared to the others

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| fac | InputFloat | Factor | `1.0` |
| spill_channel | InputMenu \| Literal\['R', 'G', 'B'\] | Spill Channel | `'G'` |
| limit_method | InputMenu \| Literal\['Single', 'Average'\] | Limit Method | `'Single'` |
| limit_channel | InputMenu \| Literal\['R', 'G', 'B'\] | Limit Channel | `'R'` |
| limit_strength | InputFloat | Limit Strength | `1.0` |
| use_spill_strength | InputBoolean | Use Spill Strength | `False` |
| spill_strength | InputColor | Strength | `None` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.ColorSpill.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.ColorSpill.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.ColorSpill.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.ColorSpill.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.ColorSpill.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.ColorSpill.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.ColorSpill.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.ColorSpill.type) |  |

**Inputs**

| Attribute              | Type            | Description        |
|------------------------|-----------------|--------------------|
| `i.image`              | `ColorSocket`   | Image              |
| `i.fac`                | `FloatSocket`   | Factor             |
| `i.spill_channel`      | `MenuSocket`    | Spill Channel      |
| `i.limit_method`       | `MenuSocket`    | Limit Method       |
| `i.limit_channel`      | `MenuSocket`    | Limit Channel      |
| `i.limit_strength`     | `FloatSocket`   | Limit Strength     |
| `i.use_spill_strength` | `BooleanSocket` | Use Spill Strength |
| `i.spill_strength`     | `ColorSocket`   | Strength           |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### DifferenceKey

``` python
DifferenceKey(image_1=None, image_2=None, tolerance=0.1, falloff=0.1)
```

Produce a matte that isolates foreground content by comparing it with a reference background image

#### Parameters

| Name      | Type       | Description | Default |
|-----------|------------|-------------|---------|
| image_1   | InputColor | Image 1     | `None`  |
| image_2   | InputColor | Image 2     | `None`  |
| tolerance | InputFloat | Tolerance   | `0.1`   |
| falloff   | InputFloat | Falloff     | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.DifferenceKey.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.DifferenceKey.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.DifferenceKey.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.DifferenceKey.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.DifferenceKey.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.DifferenceKey.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.DifferenceKey.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.DifferenceKey.type) |  |

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.image_1`   | `ColorSocket` | Image 1     |
| `i.image_2`   | `ColorSocket` | Image 2     |
| `i.tolerance` | `FloatSocket` | Tolerance   |
| `i.falloff`   | `FloatSocket` | Falloff     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |

### DistanceKey

``` python
DistanceKey(
    image=None,
    key_color=None,
    color_space='RGB',
    tolerance=0.1,
    falloff=0.1,
)
```

Create matte based on 3D distance between colors

#### Parameters

| Name        | Type                                 | Description | Default |
|-------------|--------------------------------------|-------------|---------|
| image       | InputColor                           | Image       | `None`  |
| key_color   | InputColor                           | Key Color   | `None`  |
| color_space | InputMenu \| Literal\['RGB', 'YCC'\] | Color Space | `'RGB'` |
| tolerance   | InputFloat                           | Tolerance   | `0.1`   |
| falloff     | InputFloat                           | Falloff     | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.DistanceKey.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.DistanceKey.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.DistanceKey.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.DistanceKey.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.DistanceKey.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.DistanceKey.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.DistanceKey.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.DistanceKey.type) |  |

**Inputs**

| Attribute       | Type          | Description |
|-----------------|---------------|-------------|
| `i.image`       | `ColorSocket` | Image       |
| `i.key_color`   | `ColorSocket` | Key Color   |
| `i.color_space` | `MenuSocket`  | Color Space |
| `i.tolerance`   | `FloatSocket` | Tolerance   |
| `i.falloff`     | `FloatSocket` | Falloff     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |

### DoubleEdgeMask

``` python
DoubleEdgeMask(
    outer_mask=0.8,
    inner_mask=0.8,
    image_edges=False,
    only_inside_outer=False,
)
```

Create a gradient between two masks

#### Parameters

| Name              | Type         | Description       | Default |
|-------------------|--------------|-------------------|---------|
| outer_mask        | InputFloat   | Outer Mask        | `0.8`   |
| inner_mask        | InputFloat   | Inner Mask        | `0.8`   |
| image_edges       | InputBoolean | Image Edges       | `False` |
| only_inside_outer | InputBoolean | Only Inside Outer | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.DoubleEdgeMask.type) |  |

**Inputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `i.outer_mask`        | `FloatSocket`   | Outer Mask        |
| `i.inner_mask`        | `FloatSocket`   | Inner Mask        |
| `i.image_edges`       | `BooleanSocket` | Image Edges       |
| `i.only_inside_outer` | `BooleanSocket` | Only Inside Outer |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### EllipseMask

``` python
EllipseMask(
    operation='Add',
    mask=0.0,
    value=1.0,
    position=None,
    size=None,
    rotation=0.0,
)
```

Create elliptical mask suitable for use as a simple matte or vignette mask

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| operation | InputMenu \| Literal\['Add', 'Subtract', 'Multiply', 'Not'\] | Operation | `'Add'` |
| mask | InputFloat | Mask | `0.0` |
| value | InputFloat | Value | `1.0` |
| position | InputVector | Position | `None` |
| size | InputVector | Size | `None` |
| rotation | InputFloat | Rotation | `0.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.EllipseMask.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.EllipseMask.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.EllipseMask.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.EllipseMask.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.EllipseMask.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.EllipseMask.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.EllipseMask.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.EllipseMask.type) |  |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.operation` | `MenuSocket`   | Operation   |
| `i.mask`      | `FloatSocket`  | Mask        |
| `i.value`     | `FloatSocket`  | Value       |
| `i.position`  | `VectorSocket` | Position    |
| `i.size`      | `VectorSocket` | Size        |
| `i.rotation`  | `FloatSocket`  | Rotation    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.mask`  | `FloatSocket` | Mask        |

### Keying

``` python
Keying(
    image=None,
    key_color=None,
    preprocess_blur_size=0,
    key_balance=0.5,
    black_level=0.0,
    white_level=1.0,
    edge_search_size=3,
    edge_tolerance=0.1,
    garbage_matte=0.0,
    core_matte=0.0,
    postprocess_blur_size=0,
    postprocess_dilate_size=0,
    postprocess_feather_size=0,
    feather_falloff='Smooth',
    despill_strength=1.0,
    despill_balance=0.5,
)
```

Perform both chroma keying (to remove the backdrop) and despill (to correct color cast from the backdrop)

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| key_color | InputColor | Key Color | `None` |
| preprocess_blur_size | InputInteger | Blur Size | `0` |
| key_balance | InputFloat | Balance | `0.5` |
| black_level | InputFloat | Black Level | `0.0` |
| white_level | InputFloat | White Level | `1.0` |
| edge_search_size | InputInteger | Size | `3` |
| edge_tolerance | InputFloat | Tolerance | `0.1` |
| garbage_matte | InputFloat | Garbage Matte | `0.0` |
| core_matte | InputFloat | Core Matte | `0.0` |
| postprocess_blur_size | InputInteger | Blur Size | `0` |
| postprocess_dilate_size | InputInteger | Dilate Size | `0` |
| postprocess_feather_size | InputInteger | Feather Size | `0` |
| feather_falloff | InputMenu \| Literal\['Smooth', 'Sphere', 'Root', 'Inverse Square', 'Sharp', 'Linear'\] | Feather Falloff | `'Smooth'` |
| despill_strength | InputFloat | Strength | `1.0` |
| despill_balance | InputFloat | Balance | `0.5` |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.compositor.matte.Keying.i)             |             |
| [`inputs`](#nodebpy.nodes.compositor.matte.Keying.inputs)   |             |
| [`name`](#nodebpy.nodes.compositor.matte.Keying.name)       |             |
| [`node`](#nodebpy.nodes.compositor.matte.Keying.node)       |             |
| [`o`](#nodebpy.nodes.compositor.matte.Keying.o)             |             |
| [`outputs`](#nodebpy.nodes.compositor.matte.Keying.outputs) |             |
| [`tree`](#nodebpy.nodes.compositor.matte.Keying.tree)       |             |
| [`type`](#nodebpy.nodes.compositor.matte.Keying.type)       |             |

**Inputs**

| Attribute                    | Type            | Description     |
|------------------------------|-----------------|-----------------|
| `i.image`                    | `ColorSocket`   | Image           |
| `i.key_color`                | `ColorSocket`   | Key Color       |
| `i.preprocess_blur_size`     | `IntegerSocket` | Blur Size       |
| `i.key_balance`              | `FloatSocket`   | Balance         |
| `i.black_level`              | `FloatSocket`   | Black Level     |
| `i.white_level`              | `FloatSocket`   | White Level     |
| `i.edge_search_size`         | `IntegerSocket` | Size            |
| `i.edge_tolerance`           | `FloatSocket`   | Tolerance       |
| `i.garbage_matte`            | `FloatSocket`   | Garbage Matte   |
| `i.core_matte`               | `FloatSocket`   | Core Matte      |
| `i.postprocess_blur_size`    | `IntegerSocket` | Blur Size       |
| `i.postprocess_dilate_size`  | `IntegerSocket` | Dilate Size     |
| `i.postprocess_feather_size` | `IntegerSocket` | Feather Size    |
| `i.feather_falloff`          | `MenuSocket`    | Feather Falloff |
| `i.despill_strength`         | `FloatSocket`   | Strength        |
| `i.despill_balance`          | `FloatSocket`   | Balance         |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |
| `o.edges` | `FloatSocket` | Edges       |

### KeyingScreen

``` python
KeyingScreen(smoothness=0.0, *, tracking_object='')
```

Create plates for use as a color reference for keying nodes

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| smoothness | InputFloat | Smoothness  | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.KeyingScreen.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.KeyingScreen.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.KeyingScreen.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.KeyingScreen.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.KeyingScreen.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.KeyingScreen.outputs) |  |
| [`tracking_object`](#nodebpy.nodes.compositor.matte.KeyingScreen.tracking_object) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.KeyingScreen.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.KeyingScreen.type) |  |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.smoothness` | `FloatSocket` | Smoothness  |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.screen` | `ColorSocket` | Screen      |

### LuminanceKey

``` python
LuminanceKey(image=None, minimum=0.0, maximum=1.0)
```

Create a matte based on luminance (brightness) difference

#### Parameters

| Name    | Type       | Description | Default |
|---------|------------|-------------|---------|
| image   | InputColor | Image       | `None`  |
| minimum | InputFloat | Minimum     | `0.0`   |
| maximum | InputFloat | Maximum     | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.matte.LuminanceKey.i) |  |
| [`inputs`](#nodebpy.nodes.compositor.matte.LuminanceKey.inputs) |  |
| [`name`](#nodebpy.nodes.compositor.matte.LuminanceKey.name) |  |
| [`node`](#nodebpy.nodes.compositor.matte.LuminanceKey.node) |  |
| [`o`](#nodebpy.nodes.compositor.matte.LuminanceKey.o) |  |
| [`outputs`](#nodebpy.nodes.compositor.matte.LuminanceKey.outputs) |  |
| [`tree`](#nodebpy.nodes.compositor.matte.LuminanceKey.tree) |  |
| [`type`](#nodebpy.nodes.compositor.matte.LuminanceKey.type) |  |

**Inputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.image`   | `ColorSocket` | Image       |
| `i.minimum` | `FloatSocket` | Minimum     |
| `i.maximum` | `FloatSocket` | Maximum     |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
| `o.matte` | `FloatSocket` | Matte       |
