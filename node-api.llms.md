# Node API Design

The design approach for interfacing with the nodes takes several aspects into consideration.

``` python
from nodebpy import geometry as g
```

## Sockets

### Inputs

Input sockets are exposed in two different ways, they are positional arguments in the class `__init__` signature and are available behind the `inputs / i` accessor on the nodes.

``` py
class SetPosition(BaseNode):
    def __init__(
        self,
        geometry: InputGeometry = None,
        selection: InputBoolean = None,
        position: InputVector = None,
        offset: InputVector = (0.0, 0.0, 0.0),
    ):
```

We can either pass in nodes / sockets / values into the constructor, or link them after construction.

The `g.Cube()` is used as a positional argument to `geometry`, while we explicitly state the offset with a keyword argument. On the second line we scale `Position()` by `0.5` and then link that to the `position` input of `SetPosition`.

``` python
with g.tree() as tree:
    sp = g.SetPosition(g.Cube(), offset=g.RandomValue() * 0.1)
    _ = (g.Position() * 0.5) >> sp.i.position

tree
```

A vector, rotation or color input can also take a tuple that mixes plain values and sockets. The parts known only when the tree runs can’t go into the socket’s default, so they are combined with a `Combine XYZ` (or `Combine Color`) node that is linked in instead:

``` python
with g.tree() as tree:
    height = tree.inputs.float("Height", 2.0)
    g.Cube(size=(1, 1, height)) >> tree.outputs.geometry("Geometry")

tree
```

### Default Inputs

Some inputs read something other than their stored value when nothing is connected. Blender hides the value of such sockets in the editor: Set Position’s *Position* reads the position field, its *Selection* means every element, and many group assets declare a *Default Input* (an implicit field or context value) for an input. A constructor parameter whose value Blender hides defaults to `None`, which leaves the socket alone.

For generated asset classes the fallback is spelled out with `Default`, so it shows in the signature and the reference:

``` py
class RandomRotation(AssetGeometryGroup):
    def __init__(
        self,
        id: InputInteger = Default.ID_OR_INDEX,
        ...
```

The members mirror Blender’s default-input identifiers (`Default.POSITION`, `Default.NORMAL`, `Default.INDEX`, `Default.ID_OR_INDEX`, `Default.INSTANCE_TRANSFORM`, `Default.HANDLE_LEFT`, `Default.HANDLE_RIGHT`, `Default.SCENE_FRAME`, `Default.UNIFORM_IMAGE_COORDINATES`, `Default.SELF_OBJECT`). Passing a member to any constructor is the same as passing `None`: nothing is set or linked, the socket keeps its own fallback.

``` python
from nodebpy import Default

with g.tree() as tree:
    _ = g.SetPosition(g.Cube(), position=Default.POSITION) >> tree.outputs.geometry()

tree
```

### Outputs

Selection of outputs is done automatically to best match the data types of the inputs. You can be specific with the output though, with outputs available behind the `outputs` / `o` accessor.

``` python
with g.tree() as tree:
    time = g.SceneTime()

    _ = (
        g.Cube()
        >> g.SetPosition(offset=g.RandomValue(min=-1) * time.o.seconds)
        >> tree.outputs.geometry()
    )

tree
```

### Slicing Inputs and Outputs

You can use slicing to access individual or multiple components of input and output sockets.

``` python
with g.tree() as tree:
    sep = g.SeparateXYZ(g.Position())
    comb = g.CombineXYZ(*sep.o)
    comb2 = g.CombineXYZ()

    sep.o[1] >> comb2.i[2]

tree
```

We can replicate part of a PCA analysis, getting the mean difference of the position field, scaling and combining into a matrix.

``` python
with g.tree() as tree:
    pos = g.Position()
    diff = g.FieldAverage.point.vector(pos).o.mean - pos
    matrix = g.CombineMatrix()

    for i, axis1 in enumerate(diff):
        sep = g.FieldAverage.point.vector(diff * axis1)
        for j, axis2 in enumerate(sep.o.mean):
            axis2 >> matrix.i[int(i * 4 + j)]

tree
```

#### Vector Outputs

Some output attributes have convenience methods for simpler chaining. Vector outputs can access the `x/y/z/` components quickly, which internally adds the `SeparateXYZ` required. The same SeparateXYZ node is re-used across different outputs.

``` python
with g.tree() as tree:
    pos = g.Position().o.position

    _ = g.SetPosition(g.Cube(), position=pos.x, offset=pos.y)

tree
```

#### Which socket owns a method

A socket method lives on the value that continues down the chain, so the result has the same role as the receiver: `vec.transform(matrix)` and `vec.transform_direction(matrix)` apply a matrix to a vector (as a point, so translation applies, or as a direction, so it does not), `rot.rotate(other)` rotates a rotation, and `mat.invert()` keeps the matrix. Getters that produce another type read as nouns: `mat.translation`, `obj.matrix()`, `obj.location()`.

The two selector factories are the deliberate exceptions. `fac.mix.float(a, b)` and `condition.switch.geometry(false, true)` sit on the factor or boolean that drives a Mix or Switch node, and return the mixed or chosen value:

``` python
with g.tree() as tree:
    fac = g.NoiseTexture().o.factor
    mixed = fac.mix.vector((0, 0, 0), (1, 1, 1))
    picked = (fac > 0.5).switch.geometry(g.Cube(), g.IcoSphere())

tree
```

#### Other Accessors

Similar methods also exist for `SocketColor`, `SocketMatrix`

##### Matrix

Matrix sockets have access to the `translation`, `rotation` and `scale` from the transform.

``` python
with g.tree() as tree:
    mat = g.CombineMatrix().o.matrix
    mat.translation * 0.5
    mat.rotation >> g.RotateRotation()
    mat.scale + 0.5

tree
```

##### Color

Color sockets have `r` `g` `b` `a` properties.

``` python
with g.tree() as tree:
    col = g.CombineColor().o.color
    col.r + 10
    col.g + 0.5
    col.b * 0.3
    col.a - 0.3
tree
```

Arithmetic between two colors uses a Mix node and keeps the left color’s alpha. With a scalar or a vector the color acts as a vector, so a texture’s color can still drive a vector or rotation input.

``` python
with g.tree() as tree:
    col = g.CombineColor().o.color
    tinted = col * (1.0, 0.8, 0.6, 1.0)  # Mix (Multiply), a color
    offset = g.NoiseTexture().o.color * 0.2  # Vector Math (Scale), a vector
tree
```

##### Bundle

Bundle sockets store and read items by path. A read names the type it expects, and joining with `|` keeps the later bundle’s item when a path is in both.

``` python
with g.tree() as tree:
    settings = g.CombineBundle().o.bundle.store("radius", 0.5).store("count", 8)
    overrides = g.CombineBundle().o.bundle.store("radius", 1.0)
    merged = settings | overrides
    g.MeshCircle(merged.get.integer("count"), merged.get.float("radius"))
tree
```

##### Python builtins

`round()`, `math.floor()`, `math.ceil()` and `math.trunc()` on a float socket return an integer socket through Float To Integer, as they return an `int` in Python; the `.round()`/`.floor()` methods keep a float. Float To Integer rounds halves away from zero, where Python’s `round()` rounds them to even.

``` python
import math

with g.tree() as tree:
    count = math.ceil(g.Value(2.5).o.value * 3)
    g.MeshLine(count=count)
tree
```

## Enum Options

Many options aren’t available as sockets. These are exposed on the node class itself. The non-socket options are always keyword arguments, requiring them to be explicitly stated.

``` py
class EvaluateAtIndex(BaseNode):
    def __init__(
        self,
        value: InputFloat
        | InputInteger
        | InputBoolean
        | InputVector
        | InputRotation
        | InputMatrix = None,
        index: InputInteger = 0,
        *,
        domain: _AttributeDomains = "POINT",
        data_type: _EvaluateAtIndexDataTypes = "FLOAT",
    ):
```

They are set during the class construction, but can also be set and changed afterwards. A value the node doesn’t have raises a `TypeError` that lists its options and suggests the closest, so `g.Math(operation="SUBSTRACT")` asks “Did you mean ‘SUBTRACT’?”. Menu sockets such as Resample Curve’s `mode` do the same.

``` python
with g.tree() as tree:
    eai = g.EvaluateAtIndex(data_type="FLOAT_VECTOR")
    eai.data_type = "QUATERNION"
    eai.domain = "FACE"
```

## Node Properties

Every node has properties that aren’t sockets or options: its label, colour, width, whether it is collapsed or muted, and so on. `.props()` sets them while writing the tree, and returns the node it is called on, so it goes at the end of a chain. Called on a socket, it sets the properties of the node the socket belongs to and returns the socket.

``` python
with g.tree() as tree:
    geo = tree.inputs.geometry("Geometry")
    offset = (g.Position().o.position.x * 0.1).props(label="Ripple", hide=True)
    lifted = g.SetPosition(geometry=geo, offset=g.CombineXYZ(z=offset)).props(
        color="#FFAA00",
        width=200,
        hide_inputs=["Selection"],
        warning_propagation="ERRORS",
    )
    lifted >> tree.outputs.geometry("Geometry")

lifted.node.label, lifted.node.width, lifted.node.inputs["Selection"].hide
```

    ('', 200.0, True)

| Argument | Sets |
|----|----|
| `label` | The header label. |
| `color` | A custom header colour, as a hex string (`"#FFAA00"`) or an `(r, g, b)` tuple. |
| `width`, `height` | The node’s size; only frames use `height`. |
| `hide` | Collapse the node. |
| `show_options` | Show the node’s dropdowns and toggles. |
| `hide_inputs`, `hide_outputs` | Sockets to hide, by name; `"Value#1"` is the second visible `Value`. Blender won’t hide a linked socket. |
| `mute` | Mute (bypass) the node. |
| `warning_propagation` | Which of the node’s warnings show on the group node it sits in. |
| `pin_gizmo` | Keep a value node’s or gizmo node’s gizmo visible when the node isn’t selected. |
| `pin_gizmo_inputs` | The same for inputs passing a gizmo through, on group nodes. |

Properties left as `None` are unchanged.

### Frames

`g.Frame` takes the frame’s own settings (`label`, `shrink`, `text` and `label_size`); its colour and size go through `.props()`. Used as a `with` block it holds the nodes made inside; made on its own it is an empty frame, for notes:

``` python
with g.tree() as tree:
    with g.Frame("Lift", label_size=28).props(color="#336699"):
        lifted = g.SetPosition(offset=(0, 0, 1))
    g.Frame("Notes", shrink=False).props(width=300, height=150)
```

## Muted Links

A muted link stays in the tree but passes nothing, so the input it feeds uses its own value. Wrap the node or socket passed as an input in `muted()` to mute its link; `value=` sets the value the input uses meanwhile. It works wherever a node or socket is passed: as an argument, in a list for a multi-input socket, with `>>` and when declaring items.

``` python
from nodebpy import muted

with g.tree() as tree:
    geo = tree.inputs.geometry("Geometry")
    lifted = g.SetPosition(geometry=geo, offset=muted(g.Position(), value=(0, 0, 1)))
    g.JoinGeometry([lifted, muted(geo)]) >> tree.outputs.geometry("Geometry")

[(link.from_node.name, link.to_node.name) for link in tree.tree.links if link.is_muted]
```

    [('Position', 'Set Position'), ('Group Input', 'Join Geometry')]

`muted()` takes only a node or socket, and can’t be an operand: write `g.Math.add(muted(a), b)` rather than `muted(a) + b`. The links are muted when the tree’s `with` block exits, as muting them straight away would change which inputs Blender counts as used while the rest of the tree is being built.

## Class Methods

For nodes that have `mode`, `domain`, `data_type` and `operation` as potential enum values, convenience class methods are provided.

> The order that these methods will appear are: `mode` \> `domain` \> `data_type` \> `operation`, but should only ever be 1 or 2 deep.
>
> ``` py
> g.EvaluateAtIndex.face.vector()   # .domain.data_type
> g.Compare.float.less_than()       # .data_type.operation
> ```

Because sockets are the only positional arguments for the node constructors, enum values like `data_type` have to be specified as keyword arguments to the constructor. All enum options are type-hinted with `Literal[]` so IDE auto-complete and type hinting will work, but the convenience class methods enable a cleaner way of writing the nodes. For the example below both methods do work, but the second is cleaner to write and flows better with what the node is doing; ‘On the edge domain, evaluate a float attribute’.

``` python
with g.tree():
    # domain and data_type require kwargs
    eod1 = g.EvaluateOnDomain(domain="EDGE", data_type="FLOAT")

    # better IDE type-hinting and auto-complete
    eod2 = g.EvaluateOnDomain.edge.float()

assert eod1.data_type == eod2.data_type
assert eod1.domain == eod2.domain
```

### Switches pick their type

`Switch`, `IndexSwitch` and `MenuSwitch` work out their type from the values they are given when you don’t name one, so a node passed in is linked through its output of that type: the meshes below, rather than the UV Maps. Plain Python values decide only when nothing is linked (`g.Switch(cond, 1, 2)` is an integer switch), and values of different types raise an error naming each one. The class methods, or `input_type=` / `data_type=`, still set the type explicitly.

``` python
with g.tree():
    use_sphere = g.Boolean(True)
    switch = g.Switch(use_sphere, g.Cube(), g.UVSphere())

assert switch.input_type == "GEOMETRY"
```

A similar approach is taken for the `Compare` node, with the first being data type and then secondarily the comparison operation.

If the items being compared are nodes or sockets, regular boolean comparison with operators will also work. All 3 different approaches have the same result.

``` py
a = g.Integer(0)
b = g.Integer(2)

g.Compare(A=a, B=b, data_type="INT", operation="EQUAL")

g.Compare.integer.equal(a, b)

a == b
```

> **WARNING:**
>
> ### Comparing Node Objects
>
> In this instance `comp` will be the output of a `g.Compare` node, set with `operation="GREATER_THAN"` and `data_type="FLOAT"` (the Scene Time `frame` output is a float, which takes precedence over the integer).
>
> As this is a node within the node graph, the inputs have the potential to change during node tree evaluation meaning the result of the comparison could change. During playback on an animation the output will be `Cube` at frames \<=50 and `Cone` when above that value.
>
> ``` python
> with g.tree():
>     a = g.SceneTime().o.frame
>     b = g.Integer(50)
>
>     comp = a > b
>     geo = g.Switch.geometry(comp, g.Cube(), g.Cone())
>
> comp
> ```
>
>     <nodebpy.builder.socket.BooleanSocket at 0x133d1c050>
>
> ### Comparing Python Objects
>
> If the comparison was of just regular python values, then the result at runtime will just be boolean `True` and *not* a `Compare` node. This means the value *won’t* change during node tree evaluation, and will only be evaluated a single time in node tree construction.
>
> The result below will *always* output a `Cone` geometry because the input will always be `True`.
>
> ``` python
> with g.tree():
>     a = 0
>     b = 0
>
>     comp = a == b
>     geo = g.Switch.geometry(comp, g.Cube(), g.Cone())
>
> comp
> ```
>
>     True
