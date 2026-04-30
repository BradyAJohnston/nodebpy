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
        selection: InputBoolean = True,
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

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Random Value"):::converter-node
    N2("Cube"):::geometry-node
    N3("Vector Math<br/><small>(SCALE)</small><br/><small>×0.5</small>"):::vector-node
    N4("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N5("Set Position"):::geometry-node
    N1 -->|"Value->Value"| N4
    N2 -->|"Mesh->Geometry"| N5
    N4 -->|"Value->Offset"| N5
    N0 -->|"Position->Vector"| N3
    N3 -->|"Vector->Position"| N5
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

``` mermaid
graph LR
    N0("Random Value<br/><small>(-1,-1,-1)</small>"):::converter-node
    N1("Scene Time"):::input-node
    N2("Cube"):::geometry-node
    N3("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N4("Set Position"):::geometry-node
    N5("Group Output"):::default-node
    N0 -->|"Value->Value"| N3
    N1 -->|"Seconds->Value"| N3
    N3 -->|"Value->Offset"| N4
    N2 -->|"Mesh->Geometry"| N4
    N4 -->|"Geometry->Geometry"| N5
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

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Separate XYZ"):::converter-node
    N2("Combine XYZ"):::converter-node
    N3("Combine XYZ"):::converter-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"X->X"| N3
    N1 -->|"Y->Y"| N3
    N1 -->|"Z->Z"| N3
    N1 -->|"Y->Z"| N2
```

We can replicate part of a PCA analysis, getting the mean difference of the position field, scaling and combining into a matrix.

``` python
with g.tree() as tree:
    pos = g.Position()
    diff = g.FieldAverage.point.vector(pos).o.mean - pos
    matrix = g.CombineMatrix()

    for i, axis1 in enumerate(diff.o.vector):
        sep = g.FieldAverage.point.vector(diff * axis1)
        for j, axis2 in enumerate(sep.o.mean):
            axis2 >> matrix.i[int(i * 4 + j)]

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Field Average"):::converter-node
    N2("Vector Math<br/><small>(SUBTRACT)</small>"):::vector-node
    N3("Separate XYZ"):::converter-node
    N4("Vector Math<br/><small>(SCALE)</small>"):::vector-node
    N5("Vector Math<br/><small>(SCALE)</small>"):::vector-node
    N6("Vector Math<br/><small>(SCALE)</small>"):::vector-node
    N7("Field Average"):::converter-node
    N8("Field Average"):::converter-node
    N9("Field Average"):::converter-node
    N10("Separate XYZ"):::converter-node
    N11("Separate XYZ"):::converter-node
    N12("Separate XYZ"):::converter-node
    N13("Combine Matrix"):::converter-node
    N0 -->|"Position->Value"| N1
    N1 -->|"Mean->Vector"| N2
    N0 -->|"Position->Vector"| N2
    N2 -->|"Vector->Vector"| N3
    N3 -->|"X->Scale"| N4
    N4 -->|"Vector->Value"| N7
    N7 -->|"Mean->Vector"| N10
    N10 -->|"X->Column 1 Row 1"| N13
    N10 -->|"Y->Column 1 Row 2"| N13
    N10 -->|"Z->Column 1 Row 3"| N13
    N3 -->|"Y->Scale"| N5
    N5 -->|"Vector->Value"| N8
    N8 -->|"Mean->Vector"| N11
    N11 -->|"X->Column 2 Row 1"| N13
    N11 -->|"Y->Column 2 Row 2"| N13
    N11 -->|"Z->Column 2 Row 3"| N13
    N3 -->|"Z->Scale"| N6
    N6 -->|"Vector->Value"| N9
    N9 -->|"Mean->Vector"| N12
    N12 -->|"X->Column 3 Row 1"| N13
    N12 -->|"Y->Column 3 Row 2"| N13
    N12 -->|"Z->Column 3 Row 3"| N13
    N2 -->|"Vector->Vector"| N6
    N2 -->|"Vector->Vector"| N5
    N2 -->|"Vector->Vector"| N4
```

#### Vector Outputs

Some output attributes have convenience methods for simpler chaining. Vector outputs can access the `x/y/z/` components quickly, which internally adds the `SeparateXYZ` required. The same SeparateXYZ node is re-used across different outputs.

``` python
with g.tree() as tree:
    pos = g.Position().o.position

    _ = g.SetPosition(g.Cube(), position=pos.x, offset=pos.y)

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Cube"):::geometry-node
    N2("Separate XYZ"):::converter-node
    N3("Set Position"):::geometry-node
    N0 -->|"Position->Vector"| N2
    N1 -->|"Mesh->Geometry"| N3
    N2 -->|"X->Position"| N3
    N2 -->|"Y->Offset"| N3
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

``` mermaid
graph LR
    N0("Combine Matrix"):::converter-node
    N1("Separate Transform"):::converter-node
    N2("Vector Math<br/><small>(SCALE)</small><br/><small>×0.5</small>"):::vector-node
    N3("Rotate Rotation"):::converter-node
    N4("Vector Math<br/><small>(ADD)</small><br/><small>(0.5,0.5,0.5)</small>"):::vector-node
    N0 -->|"Matrix->Transform"| N1
    N1 -->|"Translation->Vector"| N2
    N1 -->|"Rotation->Rotation"| N3
    N1 -->|"Scale->Vector"| N4
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

``` mermaid
graph LR
    N0("Combine Color"):::converter-node
    N1("Separate Color"):::converter-node
    N2("Math<br/><small>(ADD)</small>"):::converter-node
    N3("Math<br/><small>(ADD)</small>"):::converter-node
    N4("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N5("Math<br/><small>(SUBTRACT)</small>"):::converter-node
    N0 -->|"Color->Color"| N1
    N1 -->|"Red->Value"| N2
    N1 -->|"Green->Value"| N3
    N1 -->|"Blue->Value"| N4
    N1 -->|"Alpha->Value"| N5
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

They are set during the class construction, but can also be set and changed afterwards.

``` python
with g.tree() as tree:
    eai = g.EvaluateAtIndex(data_type="FLOAT_VECTOR")
    eai.data_type = "QUATERNION"
    eai.domain = "FACE"
```

## Class Methods

For nodes that have `mode`, `domain`, `data_type` and `operation` as potential enum values, convenience class methods are provided.

> The order that these methods will appear are: `mode` \> `domain` \> `data_type` \> `operation`, but should only ever be 1 or 2 deep.
>
> ``` py
> g.EvaluateAtIndex.face.vector()   # .domain.data_type
> g.Compare.float.less_than()       # .data_type.operation
> ```

Because sockets are the only positional for the node constructors, enum values like `data_typa` have to be specified with as key word arguments to the constructor. All enum options are type-hinted with `Literal[]` so IDE auto-complete and type hinting will work, but the convenience class methods enable a cleaner way of writing the nodes. For the example below both methods do work, but the second is cleaner to write and flows better with what the node is doing; ‘On the edge domain, evaluate a float attribute’.

``` python
with g.tree():
    # domain and data_type require kwargs
    eod1 = g.EvaluateOnDomain(domain="EDGE", data_type="FLOAT")

    # better IDE type-hinting and auto-complete
    eod2 = g.EvaluateOnDomain.edge.float()

assert eod1.data_type == eod2.data_type
assert eod1.domain == eod2.domain
```

A similar approach is taken for the `Compare` node, with the first being data type and then secondarily the comparison operation.

If the items being compared are nodes or sockets, regular boolean comparison with operators will also work. All 3 different approaches have the same result.

``` py
a = g.Integer(0)
b = g.Integer(2)

g.Compare(A_INT = a, A_INT = b, data_type = "INT", operation="EQUAL")

g.Compare.integer.equal(a, b)

a == b
```

> **WARNING:**
>
> ### Comparing Node Objects
>
> In this instance `comp` will be a `g.Compare` node, set with the `operation="GREATER_THAN"` and `data_type="INT"`.
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
>     <nodebpy.nodes.geometry.manual.Compare at 0x12f625e80>
>
> ### Comparing Python Objects
>
> If the comparison was of just regular python values, then the result at runtime will just be boolean `True` and *not* a `Compare` node. This means the value *won’t* change during node tree evaluation, and will only be evaluated a single time in node tree construction.
>
> The result below will *always* output a `Cone` geoemtry because the input will always be `True`.
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
