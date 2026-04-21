# Node API Design

The design approach for interfacing with the nodes takes several aspects into consideration.

``` python
from nodebpy import geometry as g
```

## Sockets

### Inputs

Input sockets are exposed in two different ways, they are positional arguments in the class `__init__` signature and are available behind the `inputs / i` accessor on the nodes.

``` py
class SetPosition(NodeBuilder):
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

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
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

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
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

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
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

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
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

    classDef geometry-node fill:#e8f5f1,stroke:#3a7c49,stroke-width:2px
    classDef converter-node fill:#e6f1f7,stroke:#246283,stroke-width:2px
    classDef vector-node fill:#e9e9f5,stroke:#3C3C83,stroke-width:2px
    classDef texture-node fill:#fef3e6,stroke:#E66800,stroke-width:2px
    classDef shader-node fill:#fef0eb,stroke:#e67c52,stroke-width:2px
    classDef input-node fill:#f1f8ed,stroke:#7fb069,stroke-width:2px
    classDef output-node fill:#faf0ed,stroke:#c97659,stroke-width:2px
    classDef default-node fill:#f0f0f0,stroke:#5a5a5a,stroke-width:2px
```

## Enum Options

Many options aren’t available as sockets. These are exposed on the node class itself. The non-socket options are always keyword arguments, requiring them to be explicitly stated.

``` py
class EvaluateAtIndex(NodeBuilder):
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
>     <nodebpy.nodes.geometry.manual.Compare at 0x11d3e3b50>
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
