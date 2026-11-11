# nodes.compositor.converter

`converter`

## Classes

| Name | Description |
|----|----|
| [AlphaConvert](#nodebpy.nodes.compositor.converter.AlphaConvert) | Convert to and from premultiplied (associated) alpha |
| [CombineColor](#nodebpy.nodes.compositor.converter.CombineColor) | Combine an image from its composite color channels |
| [Compare](#nodebpy.nodes.compositor.converter.Compare) | Perform a comparison operation on the two given inputs |
| [ConvertToDisplay](#nodebpy.nodes.compositor.converter.ConvertToDisplay) | Convert from scene linear to display color space, with a view transform and look for tone mapping |
| [GetBundleItem](#nodebpy.nodes.compositor.converter.GetBundleItem) | Retrieve a bundle item by path. |
| [IDMask](#nodebpy.nodes.compositor.converter.IDMask) | Create a matte from an object or material index pass |
| [ImplicitConversion](#nodebpy.nodes.compositor.converter.ImplicitConversion) | Implicitly convert the input value to a fixed socket type |
| [Levels](#nodebpy.nodes.compositor.converter.Levels) | Compute average and standard deviation of pixel values |
| [RGBToBW](#nodebpy.nodes.compositor.converter.RGBToBW) | Convert RGB input into grayscale using luminance |
| [RelativeToPixel](#nodebpy.nodes.compositor.converter.RelativeToPixel) | Converts values that are relative to the image size to be in terms of pixels |
| [SeparateColor](#nodebpy.nodes.compositor.converter.SeparateColor) | Split an image into its composite color channels |
| [SetAlpha](#nodebpy.nodes.compositor.converter.SetAlpha) | Add an alpha channel to an image |
| [Split](#nodebpy.nodes.compositor.converter.Split) | Combine two images for side-by-side display. Typically used in combination with a Viewer node |
| [StoreBundleItem](#nodebpy.nodes.compositor.converter.StoreBundleItem) | Store a bundle item by path and data type. |
| [Switch](#nodebpy.nodes.compositor.converter.Switch) | Switch between two inputs |
| [SwitchView](#nodebpy.nodes.compositor.converter.SwitchView) | Combine the views (left and right) into a single stereo 3D output |

### AlphaConvert

``` python
AlphaConvert(image=None, type='To Premultiplied')
```

Convert to and from premultiplied (associated) alpha

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| type | InputMenu \| Literal\['To Premultiplied', 'To Straight'\] | Type | `'To Premultiplied'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.AlphaConvert.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.AlphaConvert.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.AlphaConvert.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.AlphaConvert.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.AlphaConvert.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.AlphaConvert.props) | Set the properties every node has and return the node, so it can |
| [to_premultiplied](#nodebpy.nodes.compositor.converter.AlphaConvert.to_premultiplied) | Create Alpha Convert node with type ‘To Premultiplied’. |
| [to_straight](#nodebpy.nodes.compositor.converter.AlphaConvert.to_straight) | Create Alpha Convert node with type ‘To Straight’. |

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

##### to_premultiplied

``` python
to_premultiplied(image=None)
```

Create Alpha Convert node with type ‘To Premultiplied’.

##### to_straight

``` python
to_straight(image=None)
```

Create Alpha Convert node with type ‘To Straight’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### CombineColor

``` python
CombineColor(
    red=0.0,
    green=0.0,
    blue=0.0,
    alpha=1.0,
    *,
    mode='RGB',
    ycc_mode='ITUBT709',
)
```

Combine an image from its composite color channels

#### Parameters

| Name  | Type       | Description | Default |
|-------|------------|-------------|---------|
| red   | InputFloat | Red         | `0.0`   |
| green | InputFloat | Green       | `0.0`   |
| blue  | InputFloat | Blue        | `0.0`   |
| alpha | InputFloat | Alpha       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.CombineColor.i) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.CombineColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.CombineColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.CombineColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.CombineColor.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.CombineColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`ycc_mode`](#nodebpy.nodes.compositor.converter.CombineColor.ycc_mode) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.compositor.converter.CombineColor.hsl) | Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.compositor.converter.CombineColor.hsv) | Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [props](#nodebpy.nodes.compositor.converter.CombineColor.props) | Set the properties every node has and return the node, so it can |
| [rgb](#nodebpy.nodes.compositor.converter.CombineColor.rgb) | Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |
| [ycbcr](#nodebpy.nodes.compositor.converter.CombineColor.ycbcr) | Create Combine Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing |
| [yuv](#nodebpy.nodes.compositor.converter.CombineColor.yuv) | Create Combine Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing |

##### hsl

``` python
hsl(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

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

##### rgb

``` python
rgb(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(red=0.0, green=0.0, blue=0.0, alpha=1.0, *, ycc_mode='ITUBT709')
```

Create Combine Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.red`   | `FloatSocket` | Red         |
| `i.green` | `FloatSocket` | Green       |
| `i.blue`  | `FloatSocket` | Blue        |
| `i.alpha` | `FloatSocket` | Alpha       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Compare

``` python
Compare(
    a=0.0,
    b=0.0,
    epsilon=None,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
    mode='ELEMENT',
)
```

Perform a comparison operation on the two given inputs

#### Parameters

| Name    | Type       | Description | Default |
|---------|------------|-------------|---------|
| a       | InputFloat | A           | `0.0`   |
| b       | InputFloat | B           | `0.0`   |
| epsilon | InputFloat | Epsilon     | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.Compare.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.Compare.i) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.Compare.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Compare.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Compare.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Compare.o) |  |
| [`operation`](#nodebpy.nodes.compositor.converter.Compare.operation) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Compare.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [average](#nodebpy.nodes.compositor.converter.Compare.average) | Create Compare with operation ‘Average’. Compare the average of the input vectors elements |
| [color](#nodebpy.nodes.compositor.converter.Compare.color) | Create Compare with operation ‘Color’. |
| [direction](#nodebpy.nodes.compositor.converter.Compare.direction) | Create Compare with operation ‘Direction’. Compare the direction of the input vectors |
| [dot_product](#nodebpy.nodes.compositor.converter.Compare.dot_product) | Create Compare with operation ‘Dot Product’. Compare the dot products of the input vectors |
| [element_wise](#nodebpy.nodes.compositor.converter.Compare.element_wise) | Create Compare with operation ‘Element-Wise’. Compare each element of the input vectors |
| [equal](#nodebpy.nodes.compositor.converter.Compare.equal) | Create Compare with operation ‘Equal’. True when both inputs are approximately equal |
| [float](#nodebpy.nodes.compositor.converter.Compare.float) | Create Compare with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.Compare.font) | Create Compare with operation ‘Font’. |
| [greater_than](#nodebpy.nodes.compositor.converter.Compare.greater_than) | Create Compare with operation ‘Greater Than’. True when the first input is greater than the second input |
| [greater_than_or_equal](#nodebpy.nodes.compositor.converter.Compare.greater_than_or_equal) | Create Compare with operation ‘Greater Than or Equal’. True when the first input is greater than the second input or equal |
| [integer](#nodebpy.nodes.compositor.converter.Compare.integer) | Create Compare with operation ‘Integer’. |
| [length](#nodebpy.nodes.compositor.converter.Compare.length) | Create Compare with operation ‘Length’. Compare the length of the input vectors |
| [less_than](#nodebpy.nodes.compositor.converter.Compare.less_than) | Create Compare with operation ‘Less Than’. True when the first input is smaller than second input |
| [less_than_or_equal](#nodebpy.nodes.compositor.converter.Compare.less_than_or_equal) | Create Compare with operation ‘Less Than or Equal’. True when the first input is smaller than the second input or equal |
| [not_equal](#nodebpy.nodes.compositor.converter.Compare.not_equal) | Create Compare with operation ‘Not Equal’. True when both inputs are not approximately equal |
| [object](#nodebpy.nodes.compositor.converter.Compare.object) | Create Compare with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.converter.Compare.props) | Set the properties every node has and return the node, so it can |
| [string](#nodebpy.nodes.compositor.converter.Compare.string) | Create Compare with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.Compare.vector) | Create Compare with operation ‘Vector’. |

##### average

``` python
average(
    a=0.0,
    b=0.0,
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
)
```

Create Compare with operation ‘Average’. Compare the average of the input vectors elements

##### color

``` python
color(
    a=(0.8, 0.8, 0.8, 1.0),
    b=(0.8, 0.8, 0.8, 1.0),
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    mode='ELEMENT',
)
```

Create Compare with operation ‘Color’.

##### direction

``` python
direction(
    a=0.0,
    b=0.0,
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
)
```

Create Compare with operation ‘Direction’. Compare the direction of the input vectors

##### dot_product

``` python
dot_product(
    a=0.0,
    b=0.0,
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
)
```

Create Compare with operation ‘Dot Product’. Compare the dot products of the input vectors

##### element_wise

``` python
element_wise(
    a=0.0,
    b=0.0,
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
)
```

Create Compare with operation ‘Element-Wise’. Compare each element of the input vectors

##### equal

``` python
equal(a=0.0, b=0.0, epsilon=0.001, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Equal’. True when both inputs are approximately equal

##### float

``` python
float(a=0.0, b=0.0, *, operation='GREATER_THAN', mode='ELEMENT')
```

Create Compare with operation ‘Float’.

##### font

``` python
font(a=None, b=None, *, operation='GREATER_THAN', mode='ELEMENT')
```

Create Compare with operation ‘Font’.

##### greater_than

``` python
greater_than(a=0.0, b=0.0, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Greater Than’. True when the first input is greater than the second input

##### greater_than_or_equal

``` python
greater_than_or_equal(a=0.0, b=0.0, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Greater Than or Equal’. True when the first input is greater than the second input or equal

##### integer

``` python
integer(a=0, b=0, *, operation='GREATER_THAN', mode='ELEMENT')
```

Create Compare with operation ‘Integer’.

##### length

``` python
length(
    a=0.0,
    b=0.0,
    epsilon=0.001,
    *,
    operation='GREATER_THAN',
    data_type='FLOAT',
)
```

Create Compare with operation ‘Length’. Compare the length of the input vectors

##### less_than

``` python
less_than(a=0.0, b=0.0, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Less Than’. True when the first input is smaller than second input

##### less_than_or_equal

``` python
less_than_or_equal(a=0.0, b=0.0, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Less Than or Equal’. True when the first input is smaller than the second input or equal

##### not_equal

``` python
not_equal(a=0.0, b=0.0, epsilon=0.001, *, data_type='FLOAT', mode='ELEMENT')
```

Create Compare with operation ‘Not Equal’. True when both inputs are not approximately equal

##### object

``` python
object(a=None, b=None, *, operation='GREATER_THAN', mode='ELEMENT')
```

Create Compare with operation ‘Object’.

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

##### string

``` python
string(a='', b='', *, operation='GREATER_THAN', mode='ELEMENT')
```

Create Compare with operation ‘String’.

##### vector

``` python
vector(
    a=(0.0, 0.0, 0.0),
    b=(0.0, 0.0, 0.0),
    *,
    operation='GREATER_THAN',
    mode='ELEMENT',
)
```

Create Compare with operation ‘Vector’.

**Inputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.a`       | `FloatSocket` | A           |
| `i.b`       | `FloatSocket` | B           |
| `i.epsilon` | `FloatSocket` | Epsilon     |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.result` | `BooleanSocket` | Result      |

### ConvertToDisplay

``` python
ConvertToDisplay(image=(1.0, 1.0, 1.0, 1.0), invert=False)
```

Convert from scene linear to display color space, with a view transform and look for tone mapping

#### Parameters

| Name   | Type         | Description | Default                |
|--------|--------------|-------------|------------------------|
| image  | InputColor   | Image       | `(1.0, 1.0, 1.0, 1.0)` |
| invert | InputBoolean | Invert      | `False`                |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ConvertToDisplay.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.ConvertToDisplay.props) | Set the properties every node has and return the node, so it can |

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

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.image`  | `ColorSocket`   | Image       |
| `i.invert` | `BooleanSocket` | Invert      |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### GetBundleItem

``` python
GetBundleItem(
    bundle=None,
    path='',
    remove=False,
    *,
    socket_type='FLOAT',
    structure_type='AUTO',
)
```

Retrieve a bundle item by path.

#### Parameters

| Name   | Type         | Description | Default |
|--------|--------------|-------------|---------|
| bundle | InputBundle  | Bundle      | `None`  |
| path   | InputString  | Path        | `''`    |
| remove | InputBoolean | Remove      | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.GetBundleItem.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.GetBundleItem.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.GetBundleItem.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.GetBundleItem.o) |  |
| [`socket_type`](#nodebpy.nodes.compositor.converter.GetBundleItem.socket_type) |  |
| [`structure_type`](#nodebpy.nodes.compositor.converter.GetBundleItem.structure_type) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.GetBundleItem.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [auto](#nodebpy.nodes.compositor.converter.GetBundleItem.auto) | Create Get Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used |
| [boolean](#nodebpy.nodes.compositor.converter.GetBundleItem.boolean) | Create Get Bundle Item with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.compositor.converter.GetBundleItem.bundle) | Create Get Bundle Item with operation ‘Bundle’. |
| [color](#nodebpy.nodes.compositor.converter.GetBundleItem.color) | Create Get Bundle Item with operation ‘Color’. |
| [dynamic](#nodebpy.nodes.compositor.converter.GetBundleItem.dynamic) | Create Get Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures |
| [field](#nodebpy.nodes.compositor.converter.GetBundleItem.field) | Create Get Bundle Item with operation ‘Field’. Socket expects a field |
| [float](#nodebpy.nodes.compositor.converter.GetBundleItem.float) | Create Get Bundle Item with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.GetBundleItem.font) | Create Get Bundle Item with operation ‘Font’. |
| [grid](#nodebpy.nodes.compositor.converter.GetBundleItem.grid) | Create Get Bundle Item with operation ‘Grid’. Socket expects a grid |
| [integer](#nodebpy.nodes.compositor.converter.GetBundleItem.integer) | Create Get Bundle Item with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.GetBundleItem.integer_vector) | Create Get Bundle Item with operation ‘Integer Vector’. |
| [list](#nodebpy.nodes.compositor.converter.GetBundleItem.list) | Create Get Bundle Item with operation ‘List’. Socket expects a list |
| [matrix](#nodebpy.nodes.compositor.converter.GetBundleItem.matrix) | Create Get Bundle Item with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.GetBundleItem.menu) | Create Get Bundle Item with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.GetBundleItem.object) | Create Get Bundle Item with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.converter.GetBundleItem.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.converter.GetBundleItem.rotation) | Create Get Bundle Item with operation ‘Rotation’. |
| [single](#nodebpy.nodes.compositor.converter.GetBundleItem.single) | Create Get Bundle Item with operation ‘Single’. Socket expects a single value |
| [string](#nodebpy.nodes.compositor.converter.GetBundleItem.string) | Create Get Bundle Item with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.GetBundleItem.vector) | Create Get Bundle Item with operation ‘Vector’. |

##### auto

``` python
auto(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used

##### boolean

``` python
boolean(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Boolean’.

##### bundle

``` python
bundle(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Bundle’.

##### color

``` python
color(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Color’.

##### dynamic

``` python
dynamic(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures

##### field

``` python
field(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘Field’. Socket expects a field

##### float

``` python
float(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Float’.

##### font

``` python
font(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Font’.

##### grid

``` python
grid(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘Grid’. Socket expects a grid

##### integer

``` python
integer(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Integer Vector’.

##### list

``` python
list(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘List’. Socket expects a list

##### matrix

``` python
matrix(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Matrix’.

##### menu

``` python
menu(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Menu’.

##### object

``` python
object(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Object’.

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

##### rotation

``` python
rotation(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Rotation’.

##### single

``` python
single(bundle=None, path='', remove=False, *, socket_type='FLOAT')
```

Create Get Bundle Item with operation ‘Single’. Socket expects a single value

##### string

``` python
string(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘String’.

##### vector

``` python
vector(bundle=None, path='', remove=False, *, structure_type='AUTO')
```

Create Get Bundle Item with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.bundle` | `BundleSocket`  | Bundle      |
| `i.path`   | `StringSocket`  | Path        |
| `i.remove` | `BooleanSocket` | Remove      |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.bundle` | `BundleSocket`  | Bundle      |
| `o.item`   | `FloatSocket`   | Item        |
| `o.exists` | `BooleanSocket` | Exists      |

### IDMask

``` python
IDMask(id_value=1.0, index=0, anti_alias=False)
```

Create a matte from an object or material index pass

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| id_value   | InputFloat   | ID value    | `1.0`   |
| index      | InputInteger | Index       | `0`     |
| anti_alias | InputBoolean | Anti-Alias  | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.IDMask.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.IDMask.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.IDMask.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.IDMask.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.IDMask.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.IDMask.props) | Set the properties every node has and return the node, so it can |

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

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.id_value`   | `FloatSocket`   | ID value    |
| `i.index`      | `IntegerSocket` | Index       |
| `i.anti_alias` | `BooleanSocket` | Anti-Alias  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.alpha` | `FloatSocket` | Alpha       |

### ImplicitConversion

``` python
ImplicitConversion(value=(0.0, 0.0, 0.0, 1.0), *, data_type='RGBA')
```

Implicitly convert the input value to a fixed socket type

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| value | InputColor | Value       | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.ImplicitConversion.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.ImplicitConversion.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.ImplicitConversion.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.ImplicitConversion.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.ImplicitConversion.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.ImplicitConversion.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.converter.ImplicitConversion.boolean) | Create Implicit Conversion with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.compositor.converter.ImplicitConversion.bundle) | Create Implicit Conversion with operation ‘Bundle’. |
| [color](#nodebpy.nodes.compositor.converter.ImplicitConversion.color) | Create Implicit Conversion with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.ImplicitConversion.float) | Create Implicit Conversion with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.ImplicitConversion.font) | Create Implicit Conversion with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.converter.ImplicitConversion.integer) | Create Implicit Conversion with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.ImplicitConversion.integer_vector) | Create Implicit Conversion with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.converter.ImplicitConversion.matrix) | Create Implicit Conversion with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.ImplicitConversion.menu) | Create Implicit Conversion with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.ImplicitConversion.object) | Create Implicit Conversion with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.converter.ImplicitConversion.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.converter.ImplicitConversion.rotation) | Create Implicit Conversion with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.converter.ImplicitConversion.string) | Create Implicit Conversion with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.ImplicitConversion.vector) | Create Implicit Conversion with operation ‘Vector’. |

##### boolean

``` python
boolean(value=False)
```

Create Implicit Conversion with operation ‘Boolean’.

##### bundle

``` python
bundle(value=None)
```

Create Implicit Conversion with operation ‘Bundle’.

##### color

``` python
color(value=(0.0, 0.0, 0.0, 1.0))
```

Create Implicit Conversion with operation ‘Color’.

##### float

``` python
float(value=0.0)
```

Create Implicit Conversion with operation ‘Float’.

##### font

``` python
font(value=None)
```

Create Implicit Conversion with operation ‘Font’.

##### integer

``` python
integer(value=0)
```

Create Implicit Conversion with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(value=(0, 0, 0))
```

Create Implicit Conversion with operation ‘Integer Vector’.

##### matrix

``` python
matrix(value=None)
```

Create Implicit Conversion with operation ‘Matrix’.

##### menu

``` python
menu(value=None)
```

Create Implicit Conversion with operation ‘Menu’.

##### object

``` python
object(value=None)
```

Create Implicit Conversion with operation ‘Object’.

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

##### rotation

``` python
rotation(value=(0.0, 0.0, 0.0))
```

Create Implicit Conversion with operation ‘Rotation’.

##### string

``` python
string(value='')
```

Create Implicit Conversion with operation ‘String’.

##### vector

``` python
vector(value=(0.0, 0.0, 0.0))
```

Create Implicit Conversion with operation ‘Vector’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.value` | `ColorSocket` | Value       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `ColorSocket` | Value       |

### Levels

``` python
Levels(image=(0.0, 0.0, 0.0, 1.0), channel='Combined')
```

Compute average and standard deviation of pixel values

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `(0.0, 0.0, 0.0, 1.0)` |
| channel | InputMenu \| Literal\['Combined', 'Red', 'Green', 'Blue', 'Luminance'\] | Channel | `'Combined'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Levels.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Levels.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Levels.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Levels.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Levels.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.Levels.props) | Set the properties every node has and return the node, so it can |

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

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `i.image`   | `ColorSocket` | Image       |
| `i.channel` | `MenuSocket`  | Channel     |

**Outputs**

| Attribute              | Type          | Description        |
|------------------------|---------------|--------------------|
| `o.mean`               | `FloatSocket` | Mean               |
| `o.standard_deviation` | `FloatSocket` | Standard Deviation |
| `o.minimum`            | `FloatSocket` | Minimum            |
| `o.maximum`            | `FloatSocket` | Maximum            |

### RGBToBW

``` python
RGBToBW(image=(0.8, 0.8, 0.8, 1.0))
```

Convert RGB input into grayscale using luminance

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| image | InputColor | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.RGBToBW.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RGBToBW.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RGBToBW.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RGBToBW.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RGBToBW.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.RGBToBW.props) | Set the properties every node has and return the node, so it can |

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

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.val`   | `FloatSocket` | Val         |

### RelativeToPixel

``` python
RelativeToPixel(
    vector_value=(0.0, 0.0),
    float_value=0.0,
    image=(0.8, 0.8, 0.8, 1.0),
    *,
    data_type='FLOAT',
    reference_dimension='X',
)
```

Converts values that are relative to the image size to be in terms of pixels

#### Parameters

| Name         | Type        | Description | Default                |
|--------------|-------------|-------------|------------------------|
| vector_value | InputVector | Value       | `(0.0, 0.0)`           |
| float_value  | InputFloat  | Value       | `0.0`                  |
| image        | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.compositor.converter.RelativeToPixel.data_type) |  |
| [`i`](#nodebpy.nodes.compositor.converter.RelativeToPixel.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.RelativeToPixel.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.RelativeToPixel.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.RelativeToPixel.o) |  |
| [`reference_dimension`](#nodebpy.nodes.compositor.converter.RelativeToPixel.reference_dimension) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.RelativeToPixel.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.compositor.converter.RelativeToPixel.float) | Create Relative To Pixel with operation ‘Float’. Float value |
| [props](#nodebpy.nodes.compositor.converter.RelativeToPixel.props) | Set the properties every node has and return the node, so it can |
| [vector](#nodebpy.nodes.compositor.converter.RelativeToPixel.vector) | Create Relative To Pixel with operation ‘Vector’. Vector value |

##### float

``` python
float(float_value=0.0, image=(0.8, 0.8, 0.8, 1.0), *, reference_dimension='X')
```

Create Relative To Pixel with operation ‘Float’. Float value

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

##### vector

``` python
vector(
    vector_value=(0.0, 0.0),
    image=(0.8, 0.8, 0.8, 1.0),
    *,
    reference_dimension='X',
)
```

Create Relative To Pixel with operation ‘Vector’. Vector value

**Inputs**

| Attribute        | Type           | Description |
|------------------|----------------|-------------|
| `i.vector_value` | `VectorSocket` | Value       |
| `i.float_value`  | `FloatSocket`  | Value       |
| `i.image`        | `ColorSocket`  | Image       |

**Outputs**

| Attribute        | Type           | Description |
|------------------|----------------|-------------|
| `o.float_value`  | `FloatSocket`  | Value       |
| `o.vector_value` | `VectorSocket` | Value       |

### SeparateColor

``` python
SeparateColor(image=(1.0, 1.0, 1.0, 1.0), *, mode='RGB', ycc_mode='ITUBT709')
```

Split an image into its composite color channels

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| image | InputColor | Image       | `(1.0, 1.0, 1.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SeparateColor.i) |  |
| [`mode`](#nodebpy.nodes.compositor.converter.SeparateColor.mode) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SeparateColor.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SeparateColor.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SeparateColor.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SeparateColor.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`ycc_mode`](#nodebpy.nodes.compositor.converter.SeparateColor.ycc_mode) |  |

#### Methods

| Name | Description |
|----|----|
| [hsl](#nodebpy.nodes.compositor.converter.SeparateColor.hsl) | Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing |
| [hsv](#nodebpy.nodes.compositor.converter.SeparateColor.hsv) | Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing |
| [props](#nodebpy.nodes.compositor.converter.SeparateColor.props) | Set the properties every node has and return the node, so it can |
| [rgb](#nodebpy.nodes.compositor.converter.SeparateColor.rgb) | Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing |
| [ycbcr](#nodebpy.nodes.compositor.converter.SeparateColor.ycbcr) | Create Separate Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing |
| [yuv](#nodebpy.nodes.compositor.converter.SeparateColor.yuv) | Create Separate Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing |

##### hsl

``` python
hsl(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘HSL’. Use HSL (Hue, Saturation, Lightness) color processing

##### hsv

``` python
hsv(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘HSV’. Use HSV (Hue, Saturation, Value) color processing

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

##### rgb

``` python
rgb(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘RGB’. Use RGB (Red, Green, Blue) color processing

##### ycbcr

``` python
ycbcr(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘YCbCr’. Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing

##### yuv

``` python
yuv(image=(1.0, 1.0, 1.0, 1.0), *, ycc_mode='ITUBT709')
```

Create Separate Color with operation ‘YUV’. Use YUV (Y - luma, U V - chroma) color processing

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.red`   | `FloatSocket` | Red         |
| `o.green` | `FloatSocket` | Green       |
| `o.blue`  | `FloatSocket` | Blue        |
| `o.alpha` | `FloatSocket` | Alpha       |

### SetAlpha

``` python
SetAlpha(image=None, alpha=1.0, type='Apply Mask')
```

Add an alpha channel to an image

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| image | InputColor | Image | `None` |
| alpha | InputFloat | Alpha | `1.0` |
| type | InputMenu \| Literal\['Apply Mask', 'Replace Alpha'\] | Type | `'Apply Mask'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SetAlpha.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SetAlpha.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SetAlpha.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SetAlpha.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SetAlpha.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [apply_mask](#nodebpy.nodes.compositor.converter.SetAlpha.apply_mask) | Create Set Alpha node with type ‘Apply Mask’. |
| [props](#nodebpy.nodes.compositor.converter.SetAlpha.props) | Set the properties every node has and return the node, so it can |
| [replace_alpha](#nodebpy.nodes.compositor.converter.SetAlpha.replace_alpha) | Create Set Alpha node with type ‘Replace Alpha’. |

##### apply_mask

``` python
apply_mask(image=None, alpha=1.0)
```

Create Set Alpha node with type ‘Apply Mask’.

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

##### replace_alpha

``` python
replace_alpha(image=None, alpha=1.0)
```

Create Set Alpha node with type ‘Replace Alpha’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.image` | `ColorSocket` | Image       |
| `i.alpha` | `FloatSocket` | Alpha       |
| `i.type`  | `MenuSocket`  | Type        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### Split

``` python
Split(
    position=(0.5, 0.5),
    rotation=math.pi / 4,
    image=(0.8, 0.8, 0.8, 1.0),
    image_001=(0.8, 0.8, 0.8, 1.0),
)
```

Combine two images for side-by-side display. Typically used in combination with a Viewer node

#### Parameters

| Name      | Type        | Description | Default                |
|-----------|-------------|-------------|------------------------|
| position  | InputVector | Position    | `(0.5, 0.5)`           |
| rotation  | InputFloat  | Rotation    | `math.pi / 4`          |
| image     | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |
| image_001 | InputColor  | Image       | `(0.8, 0.8, 0.8, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Split.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Split.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Split.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Split.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Split.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.Split.props) | Set the properties every node has and return the node, so it can |

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

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.position`  | `VectorSocket` | Position    |
| `i.rotation`  | `FloatSocket`  | Rotation    |
| `i.image`     | `ColorSocket`  | Image       |
| `i.image_001` | `ColorSocket`  | Image       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |

### StoreBundleItem

``` python
StoreBundleItem(
    bundle=None,
    path='',
    item=0.0,
    *,
    socket_type='FLOAT',
    structure_type='AUTO',
)
```

Store a bundle item by path and data type.

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| bundle | InputBundle | Bundle      | `None`  |
| path   | InputString | Path        | `''`    |
| item   | InputFloat  | Item        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.StoreBundleItem.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.StoreBundleItem.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.StoreBundleItem.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.StoreBundleItem.o) |  |
| [`socket_type`](#nodebpy.nodes.compositor.converter.StoreBundleItem.socket_type) |  |
| [`structure_type`](#nodebpy.nodes.compositor.converter.StoreBundleItem.structure_type) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.StoreBundleItem.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [auto](#nodebpy.nodes.compositor.converter.StoreBundleItem.auto) | Create Store Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used |
| [boolean](#nodebpy.nodes.compositor.converter.StoreBundleItem.boolean) | Create Store Bundle Item with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.compositor.converter.StoreBundleItem.bundle) | Create Store Bundle Item with operation ‘Bundle’. |
| [color](#nodebpy.nodes.compositor.converter.StoreBundleItem.color) | Create Store Bundle Item with operation ‘Color’. |
| [dynamic](#nodebpy.nodes.compositor.converter.StoreBundleItem.dynamic) | Create Store Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures |
| [field](#nodebpy.nodes.compositor.converter.StoreBundleItem.field) | Create Store Bundle Item with operation ‘Field’. Socket expects a field |
| [float](#nodebpy.nodes.compositor.converter.StoreBundleItem.float) | Create Store Bundle Item with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.StoreBundleItem.font) | Create Store Bundle Item with operation ‘Font’. |
| [grid](#nodebpy.nodes.compositor.converter.StoreBundleItem.grid) | Create Store Bundle Item with operation ‘Grid’. Socket expects a grid |
| [integer](#nodebpy.nodes.compositor.converter.StoreBundleItem.integer) | Create Store Bundle Item with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.StoreBundleItem.integer_vector) | Create Store Bundle Item with operation ‘Integer Vector’. |
| [list](#nodebpy.nodes.compositor.converter.StoreBundleItem.list) | Create Store Bundle Item with operation ‘List’. Socket expects a list |
| [matrix](#nodebpy.nodes.compositor.converter.StoreBundleItem.matrix) | Create Store Bundle Item with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.StoreBundleItem.menu) | Create Store Bundle Item with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.StoreBundleItem.object) | Create Store Bundle Item with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.converter.StoreBundleItem.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.converter.StoreBundleItem.rotation) | Create Store Bundle Item with operation ‘Rotation’. |
| [single](#nodebpy.nodes.compositor.converter.StoreBundleItem.single) | Create Store Bundle Item with operation ‘Single’. Socket expects a single value |
| [string](#nodebpy.nodes.compositor.converter.StoreBundleItem.string) | Create Store Bundle Item with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.StoreBundleItem.vector) | Create Store Bundle Item with operation ‘Vector’. |

##### auto

``` python
auto(bundle=None, path='', item=0.0, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘Auto’. Automatically detect a good structure type based on how the socket is used

##### boolean

``` python
boolean(bundle=None, path='', item=False, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Boolean’.

##### bundle

``` python
bundle(bundle=None, path='', item=None, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Bundle’.

##### color

``` python
color(bundle=None, path='', item=(0.8, 0.8, 0.8, 1.0), *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Color’.

##### dynamic

``` python
dynamic(bundle=None, path='', item=0.0, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘Dynamic’. Socket can work with different kinds of structures

##### field

``` python
field(bundle=None, path='', item=0.0, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘Field’. Socket expects a field

##### float

``` python
float(bundle=None, path='', item=0.0, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Float’.

##### font

``` python
font(bundle=None, path='', item=None, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Font’.

##### grid

``` python
grid(bundle=None, path='', item=None, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘Grid’. Socket expects a grid

##### integer

``` python
integer(bundle=None, path='', item=0, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(bundle=None, path='', item=(0, 0, 0), *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Integer Vector’.

##### list

``` python
list(bundle=None, path='', item=None, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘List’. Socket expects a list

##### matrix

``` python
matrix(bundle=None, path='', item=None, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Matrix’.

##### menu

``` python
menu(bundle=None, path='', item=None, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Menu’.

##### object

``` python
object(bundle=None, path='', item=None, *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Object’.

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

##### rotation

``` python
rotation(bundle=None, path='', item=(0.0, 0.0, 0.0), *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Rotation’.

##### single

``` python
single(bundle=None, path='', item=0.0, *, socket_type='FLOAT')
```

Create Store Bundle Item with operation ‘Single’. Socket expects a single value

##### string

``` python
string(bundle=None, path='', item='', *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘String’.

##### vector

``` python
vector(bundle=None, path='', item=(0.0, 0.0, 0.0), *, structure_type='AUTO')
```

Create Store Bundle Item with operation ‘Vector’.

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.bundle` | `BundleSocket` | Bundle      |
| `i.path`   | `StringSocket` | Path        |
| `i.item`   | `FloatSocket`  | Item        |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.bundle` | `BundleSocket` | Bundle      |

### Switch

``` python
Switch(switch=False, false=None, true=None, *, input_type=None)
```

Switch between two inputs

#### Parameters

| Name       | Type                 | Description | Default |
|------------|----------------------|-------------|---------|
| switch     | InputBoolean         | switch      | `False` |
| false      | InputAny             | false       | `None`  |
| true       | InputAny             | true        | `None`  |
| input_type | \_SwitchType \| None | input_type  | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.Switch.i) |  |
| [`input_type`](#nodebpy.nodes.compositor.converter.Switch.input_type) |  |
| [`name`](#nodebpy.nodes.compositor.converter.Switch.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.Switch.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.Switch.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.Switch.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.compositor.converter.Switch.boolean) | Create Switch with operation ‘Boolean’. |
| [bundle](#nodebpy.nodes.compositor.converter.Switch.bundle) | Create Switch with operation ‘Bundle’. |
| [color](#nodebpy.nodes.compositor.converter.Switch.color) | Create Switch with operation ‘Color’. |
| [float](#nodebpy.nodes.compositor.converter.Switch.float) | Create Switch with operation ‘Float’. |
| [font](#nodebpy.nodes.compositor.converter.Switch.font) | Create Switch with operation ‘Font’. |
| [integer](#nodebpy.nodes.compositor.converter.Switch.integer) | Create Switch with operation ‘Integer’. |
| [integer_vector](#nodebpy.nodes.compositor.converter.Switch.integer_vector) | Create Switch with operation ‘Integer Vector’. |
| [matrix](#nodebpy.nodes.compositor.converter.Switch.matrix) | Create Switch with operation ‘Matrix’. |
| [menu](#nodebpy.nodes.compositor.converter.Switch.menu) | Create Switch with operation ‘Menu’. |
| [object](#nodebpy.nodes.compositor.converter.Switch.object) | Create Switch with operation ‘Object’. |
| [props](#nodebpy.nodes.compositor.converter.Switch.props) | Set the properties every node has and return the node, so it can |
| [rotation](#nodebpy.nodes.compositor.converter.Switch.rotation) | Create Switch with operation ‘Rotation’. |
| [string](#nodebpy.nodes.compositor.converter.Switch.string) | Create Switch with operation ‘String’. |
| [vector](#nodebpy.nodes.compositor.converter.Switch.vector) | Create Switch with operation ‘Vector’. |

##### boolean

``` python
boolean(switch=False, false=False, true=False)
```

Create Switch with operation ‘Boolean’.

##### bundle

``` python
bundle(switch=False, false=None, true=None)
```

Create Switch with operation ‘Bundle’.

##### color

``` python
color(switch=False, false=(0.8, 0.8, 0.8, 1.0), true=(0.8, 0.8, 0.8, 1.0))
```

Create Switch with operation ‘Color’.

##### float

``` python
float(switch=False, false=0.0, true=0.0)
```

Create Switch with operation ‘Float’.

##### font

``` python
font(switch=False, false=None, true=None)
```

Create Switch with operation ‘Font’.

##### integer

``` python
integer(switch=False, false=0, true=0)
```

Create Switch with operation ‘Integer’.

##### integer_vector

``` python
integer_vector(switch=False, false=(0, 0, 0), true=(0, 0, 0))
```

Create Switch with operation ‘Integer Vector’.

##### matrix

``` python
matrix(switch=False, false=None, true=None)
```

Create Switch with operation ‘Matrix’.

##### menu

``` python
menu(switch=False, false=None, true=None)
```

Create Switch with operation ‘Menu’.

##### object

``` python
object(switch=False, false=None, true=None)
```

Create Switch with operation ‘Object’.

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

##### rotation

``` python
rotation(switch=False, false=(0.0, 0.0, 0.0), true=(0.0, 0.0, 0.0))
```

Create Switch with operation ‘Rotation’.

##### string

``` python
string(switch=False, false='', true='')
```

Create Switch with operation ‘String’.

##### vector

``` python
vector(switch=False, false=(0.0, 0.0, 0.0), true=(0.0, 0.0, 0.0))
```

Create Switch with operation ‘Vector’.

**Inputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `i.switch` | `BooleanSocket` | Switch      |
| `i.false`  | `ColorSocket`   | False       |
| `i.true`   | `ColorSocket`   | True        |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.output` | `ColorSocket` | Output      |

### SwitchView

``` python
SwitchView(left=(0.0, 0.0, 0.0, 1.0), right=(0.0, 0.0, 0.0, 1.0))
```

Combine the views (left and right) into a single stereo 3D output

#### Parameters

| Name  | Type       | Description | Default                |
|-------|------------|-------------|------------------------|
| left  | InputColor | left        | `(0.0, 0.0, 0.0, 1.0)` |
| right | InputColor | right       | `(0.0, 0.0, 0.0, 1.0)` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.compositor.converter.SwitchView.i) |  |
| [`name`](#nodebpy.nodes.compositor.converter.SwitchView.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.compositor.converter.SwitchView.node) |  |
| [`o`](#nodebpy.nodes.compositor.converter.SwitchView.o) |  |
| [`tree`](#nodebpy.nodes.compositor.converter.SwitchView.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.compositor.converter.SwitchView.props) | Set the properties every node has and return the node, so it can |

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
| `i.left`  | `ColorSocket` | left        |
| `i.right` | `ColorSocket` | right       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ColorSocket` | Image       |
