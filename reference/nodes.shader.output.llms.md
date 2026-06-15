# nodes.shader.output

`output`

## Classes

| Name | Description |
|----|----|
| [AovOutput](#nodebpy.nodes.shader.output.AovOutput) | Arbitrary Output Variables. |
| [LightOutput](#nodebpy.nodes.shader.output.LightOutput) | Output light information to a light object |
| [LineStyleOutput](#nodebpy.nodes.shader.output.LineStyleOutput) | Control the mixing of texture information into the base color of line styles |
| [MaterialOutput](#nodebpy.nodes.shader.output.MaterialOutput) | Output surface material information for use in rendering |
| [WorldOutput](#nodebpy.nodes.shader.output.WorldOutput) | Output light color information to the scene’s World |

### AovOutput

``` python
AovOutput(color=None, value=0.0, *, aov_name='')
```

    Arbitrary Output Variables.

Provide custom render passes for arbitrary shader node outputs

#### Parameters

    color : InputColor
        Color
    value : InputFloat
        Value

#### Inputs

    i.color : ColorSocket
        Color
    i.value : FloatSocket
        Value

#### Attributes

| Name | Description |
|----|----|
| [`aov_name`](#nodebpy.nodes.shader.output.AovOutput.aov_name) |  |
| [`i`](#nodebpy.nodes.shader.output.AovOutput.i) |  |
| [`name`](#nodebpy.nodes.shader.output.AovOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.output.AovOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.output.AovOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.output.AovOutput.outputs) |  |
| [`tree`](#nodebpy.nodes.shader.output.AovOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

### LightOutput

``` python
LightOutput(surface=None, *, is_active_output=False, target='ALL')
```

Output light information to a light object

#### Parameters

| Name    | Type        | Description | Default |
|---------|-------------|-------------|---------|
| surface | InputShader | Surface     | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.output.LightOutput.i) |  |
| [`is_active_output`](#nodebpy.nodes.shader.output.LightOutput.is_active_output) |  |
| [`name`](#nodebpy.nodes.shader.output.LightOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.output.LightOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.output.LightOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.output.LightOutput.outputs) |  |
| [`target`](#nodebpy.nodes.shader.output.LightOutput.target) |  |
| [`tree`](#nodebpy.nodes.shader.output.LightOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `i.surface` | `ShaderSocket` | Surface     |

### LineStyleOutput

``` python
LineStyleOutput(
    color=None,
    color_fac=1.0,
    alpha=1.0,
    alpha_fac=1.0,
    *,
    is_active_output=False,
    target='ALL',
    blend_type='MIX',
    use_alpha=False,
    use_clamp=False,
)
```

Control the mixing of texture information into the base color of line styles

#### Parameters

| Name      | Type       | Description | Default |
|-----------|------------|-------------|---------|
| color     | InputColor | Color       | `None`  |
| color_fac | InputFloat | Color Fac   | `1.0`   |
| alpha     | InputFloat | Alpha       | `1.0`   |
| alpha_fac | InputFloat | Alpha Fac   | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`blend_type`](#nodebpy.nodes.shader.output.LineStyleOutput.blend_type) |  |
| [`i`](#nodebpy.nodes.shader.output.LineStyleOutput.i) |  |
| [`is_active_output`](#nodebpy.nodes.shader.output.LineStyleOutput.is_active_output) |  |
| [`name`](#nodebpy.nodes.shader.output.LineStyleOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.output.LineStyleOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.output.LineStyleOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.output.LineStyleOutput.outputs) |  |
| [`target`](#nodebpy.nodes.shader.output.LineStyleOutput.target) |  |
| [`tree`](#nodebpy.nodes.shader.output.LineStyleOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |
| [`use_alpha`](#nodebpy.nodes.shader.output.LineStyleOutput.use_alpha) |  |
| [`use_clamp`](#nodebpy.nodes.shader.output.LineStyleOutput.use_clamp) |  |

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.color`     | `ColorSocket` | Color       |
| `i.color_fac` | `FloatSocket` | Color Fac   |
| `i.alpha`     | `FloatSocket` | Alpha       |
| `i.alpha_fac` | `FloatSocket` | Alpha Fac   |

### MaterialOutput

``` python
MaterialOutput(
    surface=None,
    volume=None,
    displacement=None,
    thickness=0.0,
    *,
    is_active_output=False,
    target='ALL',
)
```

Output surface material information for use in rendering

#### Parameters

| Name         | Type        | Description  | Default |
|--------------|-------------|--------------|---------|
| surface      | InputShader | Surface      | `None`  |
| volume       | InputShader | Volume       | `None`  |
| displacement | InputVector | Displacement | `None`  |
| thickness    | InputFloat  | Thickness    | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.output.MaterialOutput.i) |  |
| [`is_active_output`](#nodebpy.nodes.shader.output.MaterialOutput.is_active_output) |  |
| [`name`](#nodebpy.nodes.shader.output.MaterialOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.output.MaterialOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.output.MaterialOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.output.MaterialOutput.outputs) |  |
| [`target`](#nodebpy.nodes.shader.output.MaterialOutput.target) |  |
| [`tree`](#nodebpy.nodes.shader.output.MaterialOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute        | Type           | Description  |
|------------------|----------------|--------------|
| `i.surface`      | `ShaderSocket` | Surface      |
| `i.volume`       | `ShaderSocket` | Volume       |
| `i.displacement` | `VectorSocket` | Displacement |
| `i.thickness`    | `FloatSocket`  | Thickness    |

### WorldOutput

``` python
WorldOutput(surface=None, volume=None, *, is_active_output=False, target='ALL')
```

Output light color information to the scene’s World

#### Parameters

| Name    | Type        | Description | Default |
|---------|-------------|-------------|---------|
| surface | InputShader | Surface     | `None`  |
| volume  | InputShader | Volume      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.shader.output.WorldOutput.i) |  |
| [`is_active_output`](#nodebpy.nodes.shader.output.WorldOutput.is_active_output) |  |
| [`name`](#nodebpy.nodes.shader.output.WorldOutput.name) | The name of the node being wrapped by this instance. |
| [`node`](#nodebpy.nodes.shader.output.WorldOutput.node) |  |
| [`o`](#nodebpy.nodes.shader.output.WorldOutput.o) |  |
| [`outputs`](#nodebpy.nodes.shader.output.WorldOutput.outputs) |  |
| [`target`](#nodebpy.nodes.shader.output.WorldOutput.target) |  |
| [`tree`](#nodebpy.nodes.shader.output.WorldOutput.tree) | The `TreeBuilder` instance this node belongs to and is being built within. |

**Inputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `i.surface` | `ShaderSocket` | Surface     |
| `i.volume`  | `ShaderSocket` | Volume      |
