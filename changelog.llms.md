# Changelog

## Unreleased

### Enhancements

- Support adding of closure nodes (`EvaluateClosure` and the `ClosureInput` / `ClosureOutput` nodes). Convenience `ClosureZone` class is added similar to the repeat, simulation and for-each-element zones. ([`#60`](https://github.com/BradyAJohnston/nodebpy/pull/60))
- Iteration output for the `RepeatZone` has change `.i` -\> `.iteration` to not confuse with input / output socket access ([`#60`](https://github.com/BradyAJohnston/nodebpy/pull/60))
- Add a `Float()` class which just wraps the `Value()` class / node but is better for hinting towards it’s type and more discoverage (`[#58](https://github.com/BradyAJohnston/nodebpy/pull/58)`)

### Bug Fixes

- Properly expose mode, domain and data_type as methods and method factories for `SampleIndex` and `SampleCurve`. ([`#61`](https://github.com/BradyAJohnston/nodebpy/pull/61))
- Math on a `ColorSocket` now uses the `VectorMath` instead of `Math` preserving the RGB channels as XYZ. ([`#56`](https://github.com/BradyAJohnston/nodebpy/pull/56))

## v0.12.0 - 2026-04-25

### Enhancements

- Support custom node groups for each node tree via `CustomGeometryGroup`, `CustomShaderGroup`, `CustomCompositorGroup` ([`#53`](https://github.com/BradyAJohnston/nodebpy/pull/53))

## v0.11.1 - 2026-04-24

### Bug Fixes

- Fix type inference for the `>>` operator in chains, properly propagating the correct node’s return type.

## v0.11.0 — 2026-04-24

### Enhancements

- Refactor the mermaid diagram generation. Change `screenshot.py` -\> `diagram.py` and added test coverage.
- **Socket iteration and indexing** — `VectorSocket`, `ColorSocket`, and `MatrixSocket` now support `__getitem__`, `__iter__`, and `__len__` on both output and input sockets. ([\#48](https://github.com/BradyAJohnston/nodebpy/pull/48)) Output sockets decompose via `SeparateXYZ`/`SeparateColor`/`SeparateMatrix` (node reuse on repeated access); input sockets auto-wire a `CombineXYZ`/`CombineColor`/`CombineMatrix` and return the component input socket.

``` python
for i, axis in enumerate(g.Position().o.position):
    math = axis * float(i)

# Pipe a value into the Y component of a position input
g.Value(5.0) >> g.SetPosition().i.position[1]

mat = g.InstanceTransform().o.transform
vec = g.CombineXYZ(*mat[:3])
```

- **`RotationSocket`/`MatrixSocket` helpers** — Added `.invert` and `.transpose` properties on `MatrixSocket`, `.invert` on `RotationSocket`, following the same node-reuse pattern as `.x`/`.y`/`.z`.
- **`SocketAccessor` overloads** — `__getitem__` and `_get` are overloaded so slices return `list[Socket]` and str/int keys return `Socket`, eliminating the `Socket | list[Socket]` union that was blocking `enumerate` and unpacking.
- **Blender 5.1 compatibility** — Generator updated for Blender 5.1: `FontSocket` type, `Frame` node moved to `manually_defined`, `SVD` class name normalisation, and classmethod param deduplication fix (`min_x`/`min_y`/`min_z` no longer collapsed to `min`). ([\#50](https://github.com/BradyAJohnston/nodebpy/pull/50))
- **Precise operator return types** — Arithmetic operators on `FloatSocket` → `Math`, `VectorSocket` → `VectorMath`, `IntegerSocket` → `IntegerMath`. Comparison operators (`<`, `>`, `<=`, `>=`, `==`, `!=`) → `Compare`. The `>>` operator is typed via `TypeVar` so the right-hand operand’s exact type is preserved through chains.
- **Generic factory nodes** — `AccumulateField`, `EvaluateAtIndex`, `FieldAverage`, `FieldMinAndMax`, `EvaluateOnDomain`, `FieldVariance`, and `Compare` are now `Generic[_T]`. Their `_Inputs`/`_Outputs` inner classes carry the type parameter so e.g. `.point.vector(...)` returns `FieldAverage[VectorSocket]` and `.o.mean` resolves to `VectorSocket`.

### Bug Fixes

- Fix doc building and will only deploy on tagged releases. ([\#49](https://github.com/BradyAJohnston/nodebpy/pull/49))
- **Domain factory pattern** — All `_domain_factory` / local-class patterns replaced with proper `_DomainFactory` inner classes (including `CaptureAttribute`) so the type checker can resolve their return types.
- **`SocketAccessor` identifier lookup fix** — Added a normalised-identifier pass (`normalize_name(id)`) so attribute access like `.i.value_001` correctly resolves Blender identifiers such as `Value_001` that cannot be round-tripped through `denormalize_name`.

## v0.10.2 - 2026-04-21

### Enhancements

- Added changelog to the documentation to better track and explain changes in the project.
- Support `len(tree.inputs)` and `len(tree.outputs)` to get the number of inputs and outputs in the tree. ([\#43](https://github.com/BradyAJohnston/nodebpy/pull/43))
- Added the GPLv3 license to the project.

## v0.10.1 — 2026-04-20

### Bug fixes

- Fixed `CaptureAttribute.capture()` not correctly linking the captured input socket. ([\#41](https://github.com/BradyAJohnston/nodebpy/pull/41))

## v0.10.0 — 2026-04-19

The biggest release yet. The headline change is a new typed socket accessor API — `node.i.x` / `node.o.x` — that replaces the old `node.o_position`-style properties and brings full IDE auto-complete and type narrowing to socket access.

### Enhancements

#### `node.i` / `node.o` socket accessors ([\#39](https://github.com/BradyAJohnston/nodebpy/pull/39))

Sockets are now accessed through `.i` (inputs) and `.o` (outputs) accessor objects. Attribute names are the normalised socket identifier, so spaces become underscores and the first letter is lowercased.

``` python
node.o.position >> node.i.offset   # pipe position into offset
node.o.position.y * 0.2            # operate on the y component
```

In node definitions, `_Inputs` / `_Outputs` inner classes declare the available sockets and their types so IDEs can provide auto-complete:

``` python
class SetPosition(NodeBuilder):
    class _Inputs(SocketAccessor):
        geometry: GeometrySocket
        position: VectorSocket
        offset:   VectorSocket

    class _Outputs(SocketAccessor):
        geometry: GeometrySocket
```

#### `NodeGroupBuilder` — custom node groups as Python classes ([\#31](https://github.com/BradyAJohnston/nodebpy/pull/31))

Define reusable node groups as plain Python classes. The group tree is built once and cached; subsequent uses insert a `Group` node pointing at that tree.

``` python
class Jitter(NodeGroupBuilder):
    _name = "Jitter"
    _color_tag = "geometry"

    def __init__(self, geometry=None, amount=0.2, seed=0):
        super().__init__(Geometry=geometry, Amount=amount, Seed=seed)

    @classmethod
    def _build_group(cls, tree):
        geom   = tree.inputs.geometry("Geometry")
        amount = tree.inputs.float("Amount", 0.2)
        seed   = tree.inputs.integer("Seed", 0)

        offset = g.RandomValue.vector(min=-1, seed=seed) * amount
        _ = g.SetPosition(geom, offset=offset) >> tree.outputs.geometry()

# Composes identically with built-in nodes
g.IcoSphere(subdivisions=4) >> Jitter(amount=0.15) >> out
```

#### `g.tree()` module-level helper ([\#36](https://github.com/BradyAJohnston/nodebpy/pull/36))

Eliminates the need to import `TreeBuilder` directly when working with a single editor type.

``` python
# Before
from nodebpy import TreeBuilder
with TreeBuilder.geometry("My Group") as tree: ...

# After
from nodebpy import geometry as g
with g.tree("My Group") as tree: ...
```

#### Simplified interface socket definition ([\#37](https://github.com/BradyAJohnston/nodebpy/pull/37))

Interface sockets can now be defined directly on the tree object without a context manager:

``` python
with g.tree() as tree:
    geo = tree.inputs.geometry("Points")
    g.SetPosition(geo)
```

The previous context-manager form still works.

### Other changes

- Auto-detection of nodes requiring data-type class methods (e.g. `.float()`, `.vector()`) is now more robust. ([\#38](https://github.com/BradyAJohnston/nodebpy/pull/38))
- `builder.py` was split into a `builder/` package for maintainability; `VectorSocketLinker` was renamed to `VectorSocket`. ([\#35](https://github.com/BradyAJohnston/nodebpy/pull/35))
- Internal type aliases cleaned up — `InputFloat` replaces `TYPE_INPUT_VALUE` etc. ([\#34](https://github.com/BradyAJohnston/nodebpy/pull/34))

------------------------------------------------------------------------

## v0.9.1 — 2026-03-27

### Enhancements

#### `==` / `!=` comparison operators ([\#28](https://github.com/BradyAJohnston/nodebpy/pull/28))

`NodeBuilder` objects now support Python equality operators, returning a `Compare` node. Chain `.switch()` to immediately branch on the result:

``` python
# Creates a Compare node then routes into a Switch
(g.Value(5.0) > 2.0).switch(false=g.Cube(), true=g.IcoSphere())
```

#### Data-type-specific socket linkers ([\#29](https://github.com/BradyAJohnston/nodebpy/pull/29))

`VectorSocket`, `ColorSocket`, `FloatSocket`, and `IntegerSocket` carry type-specific operations (e.g. `.x`, `.y`, `.z` on vectors) so arithmetic stays typed all the way through a chain.

### Other changes

- Documentation styling improvements. ([\#27](https://github.com/BradyAJohnston/nodebpy/pull/27))

------------------------------------------------------------------------

## v0.8.0 — 2026-03-16

### Enhancements

#### `networkx` is now an optional dependency ([\#24](https://github.com/BradyAJohnston/nodebpy/pull/24))

`nodebpy` now has no hard dependencies outside of `bpy`, making it easier to vendor into add-ons. A built-in simple arranger is used when `networkx` is absent; the Sugiyama layout remains the default when it is installed.

------------------------------------------------------------------------

## v0.7.2 — 2026-03-15

### Enhancements

#### `matrix @ vector` creates a `TransformPoint` node ([\#22](https://github.com/BradyAJohnston/nodebpy/pull/22))

``` python
matrix @ g.Position()  # → TransformPoint node
```

### Bug fixes

- Fixed `...` (ellipsis) handling in `>>` chains — type-aware output selection now works correctly when skipping intermediate nodes. ([\#23](https://github.com/BradyAJohnston/nodebpy/pull/23))

------------------------------------------------------------------------

## v0.7.1 — 2026-03-14

### Enhancements

#### `Color >> Shader` linking ([\#21](https://github.com/BradyAJohnston/nodebpy/pull/21))

Piping a color socket into a shader input is now handled automatically, matching the way Blender promotes color connections in the node editor.

------------------------------------------------------------------------

## v0.7.0 — 2026-03-13

### Enhancements

#### Panels for tree interfaces ([\#20](https://github.com/BradyAJohnston/nodebpy/pull/20))

Group interface sockets can be organised into named panels:

``` python
with tree.inputs.panel("Settings"):
    s.SocketFloat("Amount", 0.2)
    s.SocketInt("Seed", 0)
```

Integer math is now handled correctly in Shader and Compositor editors (mapped to float math, as Blender does not expose integer math there).

------------------------------------------------------------------------

## v0.6.0 — 2026-03-13

### Bug fixes

- Fixed `MenuSwitch` node creation and socket wiring. ([\#18](https://github.com/BradyAJohnston/nodebpy/pull/18))

### Other changes

- Mermaid diagram generation improvements: math node operators are now shown, and socket connections use `->` instead of `>>`. ([\#19](https://github.com/BradyAJohnston/nodebpy/pull/19))

------------------------------------------------------------------------

## v0.5.0 — 2026-03-13

### Enhancements

#### Compositor and Material (Shader) node editors ([\#12](https://github.com/BradyAJohnston/nodebpy/pull/12))

`nodebpy` now supports building Compositor and Shader/Material node trees in addition to Geometry Nodes.

#### Remaining Python math operators ([\#15](https://github.com/BradyAJohnston/nodebpy/pull/15), [\#16](https://github.com/BradyAJohnston/nodebpy/pull/16))

`**` (power), `%` (modulo), `//` (floor divide), `abs()`, and unary `-` are all wired up. Operator order for vector math was also corrected.

#### Literal type hints for menu sockets ([\#17](https://github.com/BradyAJohnston/nodebpy/pull/17))

Enum choices on menu sockets are exposed as `Literal` type hints, giving IDE auto-complete on string arguments like `data_type="FLOAT"`.
