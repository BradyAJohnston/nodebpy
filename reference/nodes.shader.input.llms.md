# nodes.shader.input

`input`

## Classes

| Name | Description |
|----|----|
| [AmbientOcclusion](#nodebpy.nodes.shader.input.AmbientOcclusion) | Compute how much the hemisphere above the shading point is occluded, for example to add weathering effects to corners. |
| [Attribute](#nodebpy.nodes.shader.input.Attribute) | Retrieve attributes attached to objects or geometry |
| [Bevel](#nodebpy.nodes.shader.input.Bevel) | Generates normals with round corners. |
| [CameraData](#nodebpy.nodes.shader.input.CameraData) | Retrieve information about the camera and how it relates to the current shading point’s position |
| [Color](#nodebpy.nodes.shader.input.Color) | A color picker |
| [ColorAttribute](#nodebpy.nodes.shader.input.ColorAttribute) | Retrieve a color attribute, or the default fallback if none is specified |
| [CurvesInfo](#nodebpy.nodes.shader.input.CurvesInfo) | Retrieve hair curve information |
| [Fresnel](#nodebpy.nodes.shader.input.Fresnel) | Produce a blending factor depending on the angle between the surface normal and the view direction using Fresnel equations. |
| [Geometry](#nodebpy.nodes.shader.input.Geometry) | Retrieve geometric information about the current shading point |
| [LayerWeight](#nodebpy.nodes.shader.input.LayerWeight) | Produce a blending factor depending on the angle between the surface normal and the view direction. |
| [LightEvaluation](#nodebpy.nodes.shader.input.LightEvaluation) | Light Evaluation |
| [LightInfo](#nodebpy.nodes.shader.input.LightInfo) | Exposes physical properties of the light being evaluated and computes basic information relative to the evaluation position |
| [LightPath](#nodebpy.nodes.shader.input.LightPath) | Retrieve the type of incoming ray for which the shader is being executed. |
| [ObjectInfo](#nodebpy.nodes.shader.input.ObjectInfo) | Retrieve information about the object instance |
| [ParticleInfo](#nodebpy.nodes.shader.input.ParticleInfo) | Retrieve the data of the particle that spawned the object instance, for example to give variation to multiple instances of an object |
| [PointInfo](#nodebpy.nodes.shader.input.PointInfo) | Retrieve information about points in a point cloud |
| [Raycast](#nodebpy.nodes.shader.input.Raycast) | Cast rays and retrieve information from the hit point |
| [ShadowRaycast](#nodebpy.nodes.shader.input.ShadowRaycast) | Shadow Raycast |
| [Tangent](#nodebpy.nodes.shader.input.Tangent) | Generate a tangent direction for the Anisotropic BSDF |
| [TextureCoordinate](#nodebpy.nodes.shader.input.TextureCoordinate) | Retrieve multiple types of texture coordinates. |
| [UVAlongStroke](#nodebpy.nodes.shader.input.UVAlongStroke) | UV coordinates that map a texture along the stroke length |
| [UVMap](#nodebpy.nodes.shader.input.UVMap) | Retrieve a UV map from the geometry, or the default fallback if none is specified |
| [Wireframe](#nodebpy.nodes.shader.input.Wireframe) | Retrieve the edges of an object as it appears to Cycles. |

### AmbientOcclusion

``` python
AmbientOcclusion(
    color=(1.0, 1.0, 1.0, 1.0),
    distance=1.0,
    normal=None,
    *,
    samples=16,
    inside=False,
    only_local=False,
)
```

    Compute how much the hemisphere above the shading point is occluded, for example to add weathering effects to corners.

Note: For Cycles, this may slow down renders significantly

#### Parameters

    color : InputColor
        Color
    distance : InputFloat
        Distance
    normal : InputVector
        Normal

#### Inputs

    i.color : ColorSocket
        Color
    i.distance : FloatSocket
        Distance
    i.normal : VectorSocket
        Normal

#### Outputs

    o.color : ColorSocket
        Color
    o.ao : FloatSocket
        AO

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.AmbientOcclusion.i) |  |
| [`inside`](#nodebpy.nodes.shader.input.AmbientOcclusion.inside) |  |
| [`name`](#nodebpy.nodes.shader.input.AmbientOcclusion.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.AmbientOcclusion.node) |  |
| [`o`](#nodebpy.nodes.shader.input.AmbientOcclusion.o) |  |
| [`only_local`](#nodebpy.nodes.shader.input.AmbientOcclusion.only_local) |  |
| [`samples`](#nodebpy.nodes.shader.input.AmbientOcclusion.samples) |  |
| [`tree`](#nodebpy.nodes.shader.input.AmbientOcclusion.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.AmbientOcclusion.props) | Set the properties every node has and return the node, so it can |

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

### Attribute

``` python
Attribute(attribute_type='GEOMETRY', attribute_name='')
```

Retrieve attributes attached to objects or geometry

#### Attributes

| Name | Description |
|----|----|
| [`attribute_name`](#nodebpy.nodes.shader.input.Attribute.attribute_name) |  |
| [`attribute_type`](#nodebpy.nodes.shader.input.Attribute.attribute_type) |  |
| [`i`](#nodebpy.nodes.shader.input.Attribute.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Attribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Attribute.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Attribute.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Attribute.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [geometry](#nodebpy.nodes.shader.input.Attribute.geometry) | Create Attribute with operation ‘Geometry’. |
| [instancer](#nodebpy.nodes.shader.input.Attribute.instancer) | Create Attribute with operation ‘Instancer’. |
| [light](#nodebpy.nodes.shader.input.Attribute.light) | Create Attribute with operation ‘Light’. |
| [object](#nodebpy.nodes.shader.input.Attribute.object) | Create Attribute with operation ‘Object’. |
| [props](#nodebpy.nodes.shader.input.Attribute.props) | Set the properties every node has and return the node, so it can |
| [view_layer](#nodebpy.nodes.shader.input.Attribute.view_layer) | Create Attribute with operation ‘View Layer’. |

##### geometry

``` python
geometry(attribute_name='')
```

Create Attribute with operation ‘Geometry’.

##### instancer

``` python
instancer(attribute_name='')
```

Create Attribute with operation ‘Instancer’.

##### light

``` python
light(attribute_name='')
```

Create Attribute with operation ‘Light’.

##### object

``` python
object(attribute_name='')
```

Create Attribute with operation ‘Object’.

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

##### view_layer

``` python
view_layer(attribute_name='')
```

Create Attribute with operation ‘View Layer’.

**Outputs**

| Attribute | Type | Description |
|----|----|----|
| `o.color` | `ColorSocket` | Color |
| `o.vector` | `VectorSocket` | Vector |
| `o.factor` | `FloatSocket` | Factor. Renamed from `Fac`; `o.fac` still resolves to it. |
| `o.alpha` | `FloatSocket` | Alpha |

### Bevel

``` python
Bevel(radius=0.05, normal=None, *, samples=4)
```

    Generates normals with round corners.

Note: only supported in Cycles, and may slow down renders

#### Parameters

    radius : InputFloat
        Radius
    normal : InputVector
        Normal

#### Inputs

    i.radius : FloatSocket
        Radius
    i.normal : VectorSocket
        Normal

#### Outputs

    o.normal : VectorSocket
        Normal

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Bevel.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Bevel.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Bevel.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Bevel.o) |  |
| [`samples`](#nodebpy.nodes.shader.input.Bevel.samples) |  |
| [`tree`](#nodebpy.nodes.shader.input.Bevel.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Bevel.props) | Set the properties every node has and return the node, so it can |

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

### CameraData

``` python
CameraData()
```

Retrieve information about the camera and how it relates to the current shading point’s position

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.CameraData.i) |  |
| [`name`](#nodebpy.nodes.shader.input.CameraData.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.CameraData.node) |  |
| [`o`](#nodebpy.nodes.shader.input.CameraData.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.CameraData.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.CameraData.props) | Set the properties every node has and return the node, so it can |

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

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `o.view_vector`   | `VectorSocket` | View Vector   |
| `o.view_z_depth`  | `FloatSocket`  | View Z Depth  |
| `o.view_distance` | `FloatSocket`  | View Distance |

### Color

``` python
Color()
```

A color picker

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Color.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Color.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Color.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Color.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Color.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Color.props) | Set the properties every node has and return the node, so it can |

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

### ColorAttribute

``` python
ColorAttribute(layer_name='')
```

Retrieve a color attribute, or the default fallback if none is specified

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.ColorAttribute.i) |  |
| [`layer_name`](#nodebpy.nodes.shader.input.ColorAttribute.layer_name) |  |
| [`name`](#nodebpy.nodes.shader.input.ColorAttribute.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.ColorAttribute.node) |  |
| [`o`](#nodebpy.nodes.shader.input.ColorAttribute.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.ColorAttribute.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.ColorAttribute.props) | Set the properties every node has and return the node, so it can |

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
| `o.alpha` | `FloatSocket` | Alpha       |

### CurvesInfo

``` python
CurvesInfo()
```

Retrieve hair curve information

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.CurvesInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.input.CurvesInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.CurvesInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.input.CurvesInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.CurvesInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.CurvesInfo.props) | Set the properties every node has and return the node, so it can |

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

| Attribute          | Type           | Description    |
|--------------------|----------------|----------------|
| `o.is_strand`      | `FloatSocket`  | Is Strand      |
| `o.intercept`      | `FloatSocket`  | Intercept      |
| `o.length`         | `FloatSocket`  | Length         |
| `o.thickness`      | `FloatSocket`  | Thickness      |
| `o.tangent_normal` | `VectorSocket` | Tangent Normal |
| `o.random`         | `FloatSocket`  | Random         |

### Fresnel

``` python
Fresnel(ior=1.5, normal=None)
```

    Produce a blending factor depending on the angle between the surface normal and the view direction using Fresnel equations.

Typically used for mixing reflections at grazing angles

#### Parameters

    ior : InputFloat
        IOR
    normal : InputVector
        Normal

#### Inputs

    i.ior : FloatSocket
        IOR
    i.normal : VectorSocket
        Normal

#### Outputs

    o.factor : FloatSocket
        Factor. Renamed from ``Fac``; ``o.fac`` still resolves to it.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Fresnel.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Fresnel.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Fresnel.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Fresnel.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Fresnel.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Fresnel.props) | Set the properties every node has and return the node, so it can |

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

### Geometry

``` python
Geometry()
```

Retrieve geometric information about the current shading point

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Geometry.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Geometry.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Geometry.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Geometry.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Geometry.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Geometry.props) | Set the properties every node has and return the node, so it can |

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

| Attribute             | Type           | Description       |
|-----------------------|----------------|-------------------|
| `o.position`          | `VectorSocket` | Position          |
| `o.normal`            | `VectorSocket` | Normal            |
| `o.tangent`           | `VectorSocket` | Tangent           |
| `o.true_normal`       | `VectorSocket` | True Normal       |
| `o.incoming`          | `VectorSocket` | Incoming          |
| `o.parametric`        | `VectorSocket` | Parametric        |
| `o.backfacing`        | `FloatSocket`  | Backfacing        |
| `o.pointiness`        | `FloatSocket`  | Pointiness        |
| `o.random_per_island` | `FloatSocket`  | Random Per Island |

### LayerWeight

``` python
LayerWeight(blend=0.5, normal=None)
```

    Produce a blending factor depending on the angle between the surface normal and the view direction.

Typically used for layering shaders with the Mix Shader node

#### Parameters

    blend : InputFloat
        Blend
    normal : InputVector
        Normal

#### Inputs

    i.blend : FloatSocket
        Blend
    i.normal : VectorSocket
        Normal

#### Outputs

    o.fresnel : FloatSocket
        Fresnel
    o.facing : FloatSocket
        Facing

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.LayerWeight.i) |  |
| [`name`](#nodebpy.nodes.shader.input.LayerWeight.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.LayerWeight.node) |  |
| [`o`](#nodebpy.nodes.shader.input.LayerWeight.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.LayerWeight.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.LayerWeight.props) | Set the properties every node has and return the node, so it can |

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

### LightEvaluation

``` python
LightEvaluation(position=None, normal=None, roughness=0.5, *, mode='DIFFUSE')
```

Light Evaluation

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| position  | InputVector | Position    | `None`  |
| normal    | InputVector | Normal      | `None`  |
| roughness | InputFloat  | Roughness   | `0.5`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.LightEvaluation.i) |  |
| [`mode`](#nodebpy.nodes.shader.input.LightEvaluation.mode) |  |
| [`name`](#nodebpy.nodes.shader.input.LightEvaluation.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.LightEvaluation.node) |  |
| [`o`](#nodebpy.nodes.shader.input.LightEvaluation.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.LightEvaluation.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [diffuse](#nodebpy.nodes.shader.input.LightEvaluation.diffuse) | Create Light Evaluation with operation ‘Diffuse’. |
| [glossy](#nodebpy.nodes.shader.input.LightEvaluation.glossy) | Create Light Evaluation with operation ‘Glossy’. |
| [props](#nodebpy.nodes.shader.input.LightEvaluation.props) | Set the properties every node has and return the node, so it can |

##### diffuse

``` python
diffuse(position=None, normal=None)
```

Create Light Evaluation with operation ‘Diffuse’.

##### glossy

``` python
glossy(position=None, normal=None, roughness=0.5)
```

Create Light Evaluation with operation ‘Glossy’.

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
| `i.normal`    | `VectorSocket` | Normal      |
| `i.roughness` | `FloatSocket`  | Roughness   |

**Outputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `o.factor`    | `FloatSocket`  | Factor      |
| `o.mask`      | `FloatSocket`  | Mask        |
| `o.direction` | `VectorSocket` | Direction   |
| `o.distance`  | `FloatSocket`  | Distance    |

### LightInfo

``` python
LightInfo()
```

Exposes physical properties of the light being evaluated and computes basic information relative to the evaluation position

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.LightInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.input.LightInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.LightInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.input.LightInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.LightInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.LightInfo.props) | Set the properties every node has and return the node, so it can |

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

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.color`    | `ColorSocket`  | Color       |
| `o.power`    | `FloatSocket`  | Power       |
| `o.position` | `VectorSocket` | Position    |

### LightPath

``` python
LightPath()
```

    Retrieve the type of incoming ray for which the shader is being executed.

Typically used for non-physically-based tricks

#### Outputs

    o.is_camera_ray : FloatSocket
        Is Camera Ray
    o.is_shadow_ray : FloatSocket
        Is Shadow Ray
    o.is_diffuse_ray : FloatSocket
        Is Diffuse Ray
    o.is_glossy_ray : FloatSocket
        Is Glossy Ray
    o.is_singular_ray : FloatSocket
        Is Singular Ray
    o.is_reflection_ray : FloatSocket
        Is Reflection Ray
    o.is_transmission_ray : FloatSocket
        Is Transmission Ray
    o.is_volume_scatter_ray : FloatSocket
        Is Volume Scatter Ray
    o.ray_length : FloatSocket
        Ray Length
    o.ray_depth : FloatSocket
        Ray Depth
    o.diffuse_depth : FloatSocket
        Diffuse Depth
    o.glossy_depth : FloatSocket
        Glossy Depth
    o.transparent_depth : FloatSocket
        Transparent Depth
    o.transmission_depth : FloatSocket
        Transmission Depth
    o.portal_depth : FloatSocket
        Portal Depth

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.LightPath.i) |  |
| [`name`](#nodebpy.nodes.shader.input.LightPath.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.LightPath.node) |  |
| [`o`](#nodebpy.nodes.shader.input.LightPath.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.LightPath.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.LightPath.props) | Set the properties every node has and return the node, so it can |

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

### ObjectInfo

``` python
ObjectInfo()
```

Retrieve information about the object instance

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.ObjectInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.input.ObjectInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.ObjectInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.input.ObjectInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.ObjectInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.ObjectInfo.props) | Set the properties every node has and return the node, so it can |

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

| Attribute          | Type           | Description    |
|--------------------|----------------|----------------|
| `o.location`       | `VectorSocket` | Location       |
| `o.color`          | `ColorSocket`  | Color          |
| `o.alpha`          | `FloatSocket`  | Alpha          |
| `o.object_index`   | `FloatSocket`  | Object Index   |
| `o.material_index` | `FloatSocket`  | Material Index |
| `o.random`         | `FloatSocket`  | Random         |

### ParticleInfo

``` python
ParticleInfo()
```

Retrieve the data of the particle that spawned the object instance, for example to give variation to multiple instances of an object

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.ParticleInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.input.ParticleInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.ParticleInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.input.ParticleInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.ParticleInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.ParticleInfo.props) | Set the properties every node has and return the node, so it can |

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

| Attribute            | Type           | Description      |
|----------------------|----------------|------------------|
| `o.index`            | `FloatSocket`  | Index            |
| `o.random`           | `FloatSocket`  | Random           |
| `o.age`              | `FloatSocket`  | Age              |
| `o.lifetime`         | `FloatSocket`  | Lifetime         |
| `o.location`         | `VectorSocket` | Location         |
| `o.size`             | `FloatSocket`  | Size             |
| `o.velocity`         | `VectorSocket` | Velocity         |
| `o.angular_velocity` | `VectorSocket` | Angular Velocity |

### PointInfo

``` python
PointInfo()
```

Retrieve information about points in a point cloud

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.PointInfo.i) |  |
| [`name`](#nodebpy.nodes.shader.input.PointInfo.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.PointInfo.node) |  |
| [`o`](#nodebpy.nodes.shader.input.PointInfo.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.PointInfo.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.PointInfo.props) | Set the properties every node has and return the node, so it can |

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

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.position` | `VectorSocket` | Position    |
| `o.radius`   | `FloatSocket`  | Radius      |
| `o.random`   | `FloatSocket`  | Random      |

### Raycast

``` python
Raycast(position=None, direction=None, length=1.0, *, only_local=False)
```

Cast rays and retrieve information from the hit point

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| position  | InputVector | Position    | `None`  |
| direction | InputVector | Direction   | `None`  |
| length    | InputFloat  | Length      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Raycast.i) |  |
| [`items`](#nodebpy.nodes.shader.input.Raycast.items) | The attributes to sample at the hit point. |
| [`name`](#nodebpy.nodes.shader.input.Raycast.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Raycast.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Raycast.o) |  |
| [`only_local`](#nodebpy.nodes.shader.input.Raycast.only_local) |  |
| [`tree`](#nodebpy.nodes.shader.input.Raycast.tree) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Raycast.props) | Set the properties every node has and return the node, so it can |

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
| `i.direction` | `VectorSocket` | Direction   |
| `i.length`    | `FloatSocket`  | Length      |

**Outputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `o.is_hit`       | `FloatSocket`  | Is Hit       |
| `o.self_hit`     | `FloatSocket`  | Self Hit     |
| `o.hit_distance` | `FloatSocket`  | Hit Distance |
| `o.hit_position` | `VectorSocket` | Hit Position |
| `o.hit_normal`   | `VectorSocket` | Hit Normal   |

### ShadowRaycast

``` python
ShadowRaycast(position=None, softness=1.0)
```

Shadow Raycast

#### Parameters

| Name     | Type        | Description | Default |
|----------|-------------|-------------|---------|
| position | InputVector | Position    | `None`  |
| softness | InputFloat  | Softness    | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.ShadowRaycast.i) |  |
| [`name`](#nodebpy.nodes.shader.input.ShadowRaycast.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.ShadowRaycast.node) |  |
| [`o`](#nodebpy.nodes.shader.input.ShadowRaycast.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.ShadowRaycast.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.ShadowRaycast.props) | Set the properties every node has and return the node, so it can |

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

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `i.position` | `VectorSocket` | Position    |
| `i.softness` | `FloatSocket`  | Softness    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### Tangent

``` python
Tangent(direction_type='RADIAL', axis='Z', uv_map='')
```

Generate a tangent direction for the Anisotropic BSDF

#### Attributes

| Name | Description |
|----|----|
| [`axis`](#nodebpy.nodes.shader.input.Tangent.axis) |  |
| [`direction_type`](#nodebpy.nodes.shader.input.Tangent.direction_type) |  |
| [`i`](#nodebpy.nodes.shader.input.Tangent.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Tangent.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Tangent.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Tangent.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Tangent.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`uv_map`](#nodebpy.nodes.shader.input.Tangent.uv_map) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Tangent.props) | Set the properties every node has and return the node, so it can |

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

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `o.tangent` | `VectorSocket` | Tangent     |

### TextureCoordinate

``` python
TextureCoordinate(object=None, from_instancer=False)
```

    Retrieve multiple types of texture coordinates.

Typically used as inputs for texture nodes

#### Outputs

    o.generated : VectorSocket
        Generated
    o.normal : VectorSocket
        Normal
    o.uv : VectorSocket
        UV
    o.object : VectorSocket
        Object
    o.camera : VectorSocket
        Camera
    o.window : VectorSocket
        Window
    o.reflection : VectorSocket
        Reflection

#### Attributes

| Name | Description |
|----|----|
| [`from_instancer`](#nodebpy.nodes.shader.input.TextureCoordinate.from_instancer) |  |
| [`i`](#nodebpy.nodes.shader.input.TextureCoordinate.i) |  |
| [`name`](#nodebpy.nodes.shader.input.TextureCoordinate.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.TextureCoordinate.node) |  |
| [`o`](#nodebpy.nodes.shader.input.TextureCoordinate.o) |  |
| [`object`](#nodebpy.nodes.shader.input.TextureCoordinate.object) |  |
| [`tree`](#nodebpy.nodes.shader.input.TextureCoordinate.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.TextureCoordinate.props) | Set the properties every node has and return the node, so it can |

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

### UVAlongStroke

``` python
UVAlongStroke(use_tips=False)
```

UV coordinates that map a texture along the stroke length

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.UVAlongStroke.i) |  |
| [`name`](#nodebpy.nodes.shader.input.UVAlongStroke.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.UVAlongStroke.node) |  |
| [`o`](#nodebpy.nodes.shader.input.UVAlongStroke.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.UVAlongStroke.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`use_tips`](#nodebpy.nodes.shader.input.UVAlongStroke.use_tips) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.UVAlongStroke.props) | Set the properties every node has and return the node, so it can |

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

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### UVMap

``` python
UVMap(from_instancer=False, uv_map='')
```

Retrieve a UV map from the geometry, or the default fallback if none is specified

#### Attributes

| Name | Description |
|----|----|
| [`from_instancer`](#nodebpy.nodes.shader.input.UVMap.from_instancer) |  |
| [`i`](#nodebpy.nodes.shader.input.UVMap.i) |  |
| [`name`](#nodebpy.nodes.shader.input.UVMap.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.UVMap.node) |  |
| [`o`](#nodebpy.nodes.shader.input.UVMap.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.UVMap.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`uv_map`](#nodebpy.nodes.shader.input.UVMap.uv_map) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.UVMap.props) | Set the properties every node has and return the node, so it can |

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

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.uv`    | `VectorSocket` | UV          |

### Wireframe

``` python
Wireframe(size=0.01, *, use_pixel_size=False)
```

    Retrieve the edges of an object as it appears to Cycles.

Note: as meshes are triangulated before being processed by Cycles, topology will always appear triangulated

#### Parameters

    size : InputFloat
        Size

#### Inputs

    i.size : FloatSocket
        Size

#### Outputs

    o.factor : FloatSocket
        Factor. Renamed from ``Fac``; ``o.fac`` still resolves to it.

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.input.Wireframe.i) |  |
| [`name`](#nodebpy.nodes.shader.input.Wireframe.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.input.Wireframe.node) |  |
| [`o`](#nodebpy.nodes.shader.input.Wireframe.o) |  |
| [`tree`](#nodebpy.nodes.shader.input.Wireframe.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`use_pixel_size`](#nodebpy.nodes.shader.input.Wireframe.use_pixel_size) |  |

#### Methods

| Name | Description |
|----|----|
| [props](#nodebpy.nodes.shader.input.Wireframe.props) | Set the properties every node has and return the node, so it can |

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
