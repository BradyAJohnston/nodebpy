# Math Operators

Nodes in `nodebpy` support Python’s arithmetic, comparison, and boolean operators. Instead of manually creating `Math`, `Compare`, or `BooleanMath` nodes and wiring them together, you can write expressions that read like regular Python code. The correct node type (`Math`, `IntegerMath`, `VectorMath`, `Compare`, `BooleanMath`, or `MultiplyMatrices`) is chosen automatically based on the socket types involved.

## Arithmetic Operators

The standard arithmetic operators `+`, `-`, `*`, `/` are joined by `**` (power), `%` (modulo), `//` (floor division), unary `-` (negate), and `abs()`.

``` python
with g.tree("ArithmeticDemo") as tree:
    out = tree.outputs.geometry()

    val = g.Value(2.0)
    scaled = val**2  # Math.power
    wrapped = scaled % 5.0  # Math.floored_modulo
    snapped = scaled // 3.0  # Math.divide -> Math.floor

    _ = (
        g.Points(100, position=g.RandomValue.vector(min=-1))
        >> g.SetPosition(offset=g.Position() * snapped)
        >> out
    )

tree
```

``` mermaid
graph LR
    N0("Value"):::input-node
    N1("Math<br/><small>(POWER)</small>"):::converter-node
    N2("Math<br/><small>(DIVIDE)</small>"):::converter-node
    N3("Math<br/><small>(FLOORED_MODULO)</small>"):::converter-node
    N4("Random Value<br/><small>(-1,-1,-1)</small>"):::converter-node
    N5("Position"):::input-node
    N6("Math<br/><small>(FLOOR)</small>"):::converter-node
    N7("Points"):::geometry-node
    N8("Vector Math<br/><small>(SCALE)</small>"):::vector-node
    N9("Set Position"):::geometry-node
    N10("Group Output"):::default-node
    N0 -->|"Value->Value"| N1
    N1 -->|"Value->Value"| N3
    N1 -->|"Value->Value"| N2
    N2 -->|"Value->Value"| N6
    N4 -->|"Value->Position"| N7
    N5 -->|"Position->Vector"| N8
    N6 -->|"Value->Scale"| N8
    N8 -->|"Vector->Offset"| N9
    N7 -->|"Points->Geometry"| N9
    N9 -->|"Geometry->Geometry"| N10
```

All operators automatically select the right node type. With integers you get `IntegerMath`, with vectors you get `VectorMath`, and scalars are broadcast when mixed with vectors:

``` python
with g.tree("TypeDispatch") as tree:
    out = tree.outputs.geometry()

    # Integer operations use IntegerMath nodes
    idx = g.Index()
    row = idx // 10  # IntegerMath.divide_floor
    col = idx % 10  # IntegerMath.modulo

    # Vector operations use VectorMath nodes
    pos = g.Position()
    offset = pos**2  # VectorMath.power (element-wise)
    wrapped = pos % (1, 1, 1)  # VectorMath.modulo

    _ = g.Grid(10, 10, 100, 100) >> g.SetPosition(offset=wrapped) >> out

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Grid"):::geometry-node
    N2("Vector Math<br/><small>(POWER)</small><br/><small>(2,2,2)</small>"):::vector-node
    N3("Vector Math<br/><small>(MODULO)</small>"):::vector-node
    N4("Set Position"):::geometry-node
    N5("Index"):::input-node
    N6("Integer Math<br/><small>(DIVIDE_FLOOR)</small>"):::converter-node
    N7("Integer Math<br/><small>(MODULO)</small>"):::converter-node
    N8("Group Output"):::default-node
    N5 -->|"Index->Value"| N6
    N5 -->|"Index->Value"| N7
    N0 -->|"Position->Vector"| N2
    N0 -->|"Position->Vector"| N3
    N3 -->|"Vector->Offset"| N4
    N1 -->|"Mesh->Geometry"| N4
    N4 -->|"Geometry->Geometry"| N8
```

### Negation and Absolute Value

The unary `-` and `abs()` operators work with all numeric types:

``` python
with g.tree("UnaryOps") as tree:
    _ = (
        g.Cube()
        >> g.SetPosition(offset=-abs(g.Position()))
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Vector Math<br/><small>(ABSOLUTE)</small>"):::vector-node
    N2("Cube"):::geometry-node
    N3("Vector Math<br/><small>(SCALE)</small><br/><small>×-1</small>"):::vector-node
    N4("Set Position"):::geometry-node
    N5("Group Output"):::default-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"Vector->Vector"| N3
    N3 -->|"Vector->Offset"| N4
    N2 -->|"Mesh->Geometry"| N4
    N4 -->|"Geometry->Geometry"| N5
```

## Comparison Operators

The `<`, `>`, `<=`, `>=` operators create `Compare` nodes that output boolean sockets. The correct data type (float, integer, or vector) is inferred from the left-hand operand.

``` python
with g.tree("CompareDemo") as tree:
    out = tree.outputs.geometry()

    pos = g.Position()
    z = pos.o.position.z

    above_ground = z > 0.0  # Compare.float.greater_than
    below_ceiling = z <= 5.0  # Compare.float.less_equal

    _ = (
        g.Cube(size=10)
        >> g.SetPosition(selection=above_ground, offset=(0, 0, 1))
        >> out
    )

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Separate XYZ"):::converter-node
    N2("Cube<br/><small>(1e+01,1e+01,1e+01)</small>"):::geometry-node
    N3("Compare<br/><small>(LESS_EQUAL)</small>"):::converter-node
    N4("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N5("Set Position<br/><small>+(0,0,1)</small>"):::geometry-node
    N6("Group Output"):::default-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"Z->A"| N4
    N1 -->|"Z->A"| N3
    N4 -->|"Result->Selection"| N5
    N2 -->|"Mesh->Geometry"| N5
    N5 -->|"Geometry->Geometry"| N6
```

## Comparison into a Switch

The result of a comparison is a `Compare` node, which can be used to directly chain into a `Switch` node when in a Geometry node tree. This saves us some time having to directly use `g.Switch.float(pos.z > v, ...)`

``` python
with g.tree("SwitchDemo") as tree:
    v = g.Value(5.0)
    pos = g.Position().o.position
    result = (pos.z > v).switch(g.RandomValue.float(), 5.0 ** g.Value(10.0))

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Separate XYZ"):::converter-node
    N2("Value"):::input-node
    N3("Value"):::input-node
    N4("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N5("Random Value"):::converter-node
    N6("Math<br/><small>(POWER)</small>"):::converter-node
    N7("Switch"):::converter-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"Z->A"| N4
    N2 -->|"Value->B"| N4
    N3 -->|"Value->Value"| N6
    N4 -->|"Result->Switch"| N7
    N5 -->|"Value->False"| N7
    N6 -->|"Value->True"| N7
```

## Boolean Operators

Python’s bitwise operators `&` (and), `|` (or), `^` (xor), and `~` (not) map to `BooleanMath` nodes. These are especially useful for combining comparison results into complex selections.

``` python
with g.tree("BooleanDemo") as tree:
    out = tree.outputs.geometry()

    z = g.SeparateXYZ(g.Position()).o.z

    # Combine conditions: select points in a vertical band
    selection = (z > -2.0) & (z < 2.0)

    _ = (
        g.Cube(size=6)
        >> g.MeshToPoints()
        >> g.SetPosition(selection=selection, offset=(1, 0, 0))
        >> out
    )

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Separate XYZ"):::converter-node
    N2("Cube<br/><small>(6,6,6)</small>"):::geometry-node
    N3("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N4("Compare<br/><small>(LESS_THAN)</small>"):::converter-node
    N5("Mesh to Points"):::geometry-node
    N6("Boolean Math<br/><small>(AND)</small>"):::converter-node
    N7("Set Position<br/><small>+(1,0,0)</small>"):::geometry-node
    N8("Group Output"):::default-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"Z->A"| N3
    N1 -->|"Z->A"| N4
    N3 -->|"Result->Boolean"| N6
    N4 -->|"Result->Boolean"| N6
    N2 -->|"Mesh->Mesh"| N5
    N6 -->|"Boolean->Selection"| N7
    N5 -->|"Points->Geometry"| N7
    N7 -->|"Geometry->Geometry"| N8
```

The `~` operator inverts a boolean:

``` python
with g.tree("InvertDemo") as tree:
    is_even = (g.Index() % 2) > 0
    is_odd = ~is_even

    _ = (
        g.MeshLine(count=20)
        >> g.MeshToPoints()
        >> g.SetPosition(selection=is_odd, offset=(0, 0, 0.5))
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Index"):::input-node
    N1("Integer Math<br/><small>(MODULO)</small>"):::converter-node
    N2("Mesh Line<br/><small>+(0,0,1)</small>"):::geometry-node
    N3("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N4("Mesh to Points"):::geometry-node
    N5("Boolean Math<br/><small>(NOT)</small>"):::converter-node
    N6("Set Position<br/><small>+(0,0,0.5)</small>"):::geometry-node
    N7("Group Output"):::default-node
    N0 -->|"Index->Value"| N1
    N1 -->|"Value->A"| N3
    N3 -->|"Result->Boolean"| N5
    N2 -->|"Mesh->Mesh"| N4
    N5 -->|"Boolean->Selection"| N6
    N4 -->|"Points->Geometry"| N6
    N6 -->|"Geometry->Geometry"| N7
```

## Matrix Multiplication

The `@` operator maps to `MultiplyMatrices`, composing two 4x4 transformation matrices. You can also multiply a matrix by a vector using `@` and a `TransformPoint` will automatically be added.

``` python
with g.tree("MatmulDemo") as tree:
    rotate = g.CombineTransform(rotation=(0, 45, 0))
    translate = g.CombineTransform(translation=(2, 0, 0))

    _ = g.Cube() >> g.SetPosition(position=rotate @ translate @ g.Position())

tree
```

``` mermaid
graph LR
    N0("Combine Transform<br/><small>(0,4e+01,0)</small>"):::converter-node
    N1("Combine Transform<br/><small>(2,0,0)</small>"):::converter-node
    N2("Position"):::input-node
    N3("Multiply Matrices"):::converter-node
    N4("Cube"):::geometry-node
    N5("Transform Point"):::converter-node
    N6("Set Position"):::geometry-node
    N0 -->|"Transform->Matrix"| N3
    N1 -->|"Transform->Matrix"| N3
    N2 -->|"Position->Vector"| N5
    N3 -->|"Matrix->Transform"| N5
    N5 -->|"Vector->Position"| N6
    N4 -->|"Mesh->Geometry"| N6
```

## Putting It All Together

Here are some examples of building small algorithms entirely with operators.

### Checkerboard Selection

Select alternating faces on a grid using integer modulo and comparisons:

``` python
with g.tree("Checkerboard") as tree:
    idx = g.Index()
    row = idx // 10
    col = idx % 10
    is_checker = ((row + col) % 2) > 0

    _ = (
        g.Grid(10, 10, 10, 10)
        >> g.SetPosition(selection=is_checker, offset=(0, 0, 0.5))
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Index"):::input-node
    N1("Integer Math<br/><small>(DIVIDE_FLOOR)</small>"):::converter-node
    N2("Integer Math<br/><small>(MODULO)</small>"):::converter-node
    N3("Integer Math<br/><small>(ADD)</small>"):::converter-node
    N4("Integer Math<br/><small>(MODULO)</small>"):::converter-node
    N5("Grid"):::geometry-node
    N6("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N7("Set Position<br/><small>+(0,0,0.5)</small>"):::geometry-node
    N8("Group Output"):::default-node
    N0 -->|"Index->Value"| N1
    N0 -->|"Index->Value"| N2
    N1 -->|"Value->Value"| N3
    N2 -->|"Value->Value"| N3
    N3 -->|"Value->Value"| N4
    N4 -->|"Value->A"| N6
    N6 -->|"Result->Selection"| N7
    N5 -->|"Mesh->Geometry"| N7
    N7 -->|"Geometry->Geometry"| N8
```

### Layered Selection

Divide space into layers using floor division, then select specific layers:

``` python
with g.tree("Layers") as tree:
    z = g.SeparateXYZ(g.Position()).o.z
    layer = g.SeparateXYZ(g.Position() // (1, 1, 1)).o.z

    selection = (layer > 0) & (layer < 3) & ~(layer > 1)

    _ = (
        g.Cube(size=5)
        >> g.MeshToPoints()
        >> g.SetPosition(selection=selection, offset=(1, 0, 0))
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Vector Math<br/><small>(DIVIDE)</small>"):::vector-node
    N2("Vector Math<br/><small>(FLOOR)</small>"):::vector-node
    N3("Separate XYZ"):::converter-node
    N4("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N5("Compare<br/><small>(LESS_THAN)</small>"):::converter-node
    N6("Compare<br/><small>(GREATER_THAN)</small>"):::converter-node
    N7("Cube<br/><small>(5,5,5)</small>"):::geometry-node
    N8("Boolean Math<br/><small>(AND)</small>"):::converter-node
    N9("Boolean Math<br/><small>(NOT)</small>"):::converter-node
    N10("Mesh to Points"):::geometry-node
    N11("Boolean Math<br/><small>(AND)</small>"):::converter-node
    N12("Position"):::input-node
    N13("Set Position<br/><small>+(1,0,0)</small>"):::geometry-node
    N14("Separate XYZ"):::converter-node
    N15("Group Output"):::default-node
    N12 -->|"Position->Vector"| N14
    N0 -->|"Position->Vector"| N1
    N1 -->|"Vector->Vector"| N2
    N2 -->|"Vector->Vector"| N3
    N3 -->|"Z->A"| N4
    N3 -->|"Z->A"| N5
    N4 -->|"Result->Boolean"| N8
    N5 -->|"Result->Boolean"| N8
    N3 -->|"Z->A"| N6
    N6 -->|"Result->Boolean"| N9
    N8 -->|"Boolean->Boolean"| N11
    N9 -->|"Boolean->Boolean"| N11
    N7 -->|"Mesh->Mesh"| N10
    N11 -->|"Boolean->Selection"| N13
    N10 -->|"Points->Geometry"| N13
    N13 -->|"Geometry->Geometry"| N15
```

### Spiral Point Distribution

Use power and modulo to create a spiral-like displacement pattern:

``` python
with g.tree("Spiral") as tree:
    pos = g.Position().o.position
    angle = pos.x * 3.14
    radius = abs(pos.y) ** 0.5

    spiral_offset = g.CombineXYZ(
        x=g.Math.cosine(angle) * radius,
        y=g.Math.sine(angle) * radius,
        z=pos.z,
    )

    _ = (
        g.Points(500, position=g.RandomValue.vector(min=-1))
        >> g.SetPosition(position=spiral_offset)
        >> tree.outputs.geometry()
    )

tree
```

``` mermaid
graph LR
    N0("Position"):::input-node
    N1("Separate XYZ"):::converter-node
    N2("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N3("Math<br/><small>(ABSOLUTE)</small>"):::converter-node
    N4("Math<br/><small>(COSINE)</small>"):::converter-node
    N5("Math<br/><small>(SINE)</small>"):::converter-node
    N6("Math<br/><small>(POWER)</small>"):::converter-node
    N7("Random Value<br/><small>(-1,-1,-1)</small>"):::converter-node
    N8("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N9("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N10("Points"):::geometry-node
    N11("Combine XYZ"):::converter-node
    N12("Set Position"):::geometry-node
    N13("Group Output"):::default-node
    N0 -->|"Position->Vector"| N1
    N1 -->|"X->Value"| N2
    N1 -->|"Y->Value"| N3
    N3 -->|"Value->Value"| N6
    N2 -->|"Value->Value"| N4
    N4 -->|"Value->Value"| N8
    N6 -->|"Value->Value"| N8
    N2 -->|"Value->Value"| N5
    N5 -->|"Value->Value"| N9
    N6 -->|"Value->Value"| N9
    N8 -->|"Value->X"| N11
    N9 -->|"Value->Y"| N11
    N7 -->|"Value->Position"| N10
    N11 -->|"Vector->Position"| N12
    N10 -->|"Points->Geometry"| N12
    N12 -->|"Geometry->Geometry"| N13
    N1 -->|"Z->Z"| N11
```

## Operator Reference

| Operator | Python | Node |
|:---|:---|:---|
| Add | `a + b` | Math / VectorMath / IntegerMath |
| Subtract | `a - b` | Math / VectorMath / IntegerMath |
| Multiply | `a * b` | Math / VectorMath / IntegerMath |
| Divide | `a / b` | Math / VectorMath / IntegerMath |
| Power | `a ** b` | Math / VectorMath / IntegerMath |
| Modulo | `a % b` | Math / VectorMath / IntegerMath |
| Floor Divide | `a // b` | IntegerMath (int) or Divide+Floor (float/vector) |
| Negate | `-a` | IntegerMath.negate / Math.multiply(a, -1) / VectorMath.scale(a, -1) |
| Absolute | `abs(a)` | Math / VectorMath / IntegerMath `.absolute` |
| Less Than | `a < b` | Compare |
| Greater Than | `a > b` | Compare |
| Less Equal | `a <= b` | Compare |
| Greater Equal | `a >= b` | Compare |
| And | `a & b` | BooleanMath |
| Or | `a \| b` | BooleanMath |
| Xor | `a ^ b` | BooleanMath |
| Not | `~a` | BooleanMath |
| Matrix Multiply | `a @ b` | MultiplyMatrices |
| Chain | `a >> b` | Links output to input |
