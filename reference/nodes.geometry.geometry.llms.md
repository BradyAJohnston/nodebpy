# nodes.geometry.geometry

`geometry`

## Classes

| Name | Description |
|----|----|
| [Arc](#nodebpy.nodes.geometry.geometry.Arc) | Generate a poly spline arc |
| [BezierSegment](#nodebpy.nodes.geometry.geometry.BezierSegment) | Generate a 2D Bézier spline from the given control points and handles |
| [BoundingBox](#nodebpy.nodes.geometry.geometry.BoundingBox) | Calculate the limits of a geometry’s positions and generate a box mesh with those dimensions |
| [Cone](#nodebpy.nodes.geometry.geometry.Cone) | Generate a cone mesh |
| [ConvexHull](#nodebpy.nodes.geometry.geometry.ConvexHull) | Create a mesh that encloses all points in the input geometry with the smallest number of points |
| [Cube](#nodebpy.nodes.geometry.geometry.Cube) | Generate a cuboid mesh with variable side lengths and subdivisions |
| [CurveCircle](#nodebpy.nodes.geometry.geometry.CurveCircle) | Generate a poly spline circle |
| [CurveLength](#nodebpy.nodes.geometry.geometry.CurveLength) | Retrieve the length of all splines added together |
| [CurveLine](#nodebpy.nodes.geometry.geometry.CurveLine) | Generate a poly spline line with two points |
| [CurveToMesh](#nodebpy.nodes.geometry.geometry.CurveToMesh) | Convert curves into a mesh, optionally with a custom profile shape defined by curves |
| [CurveToPoints](#nodebpy.nodes.geometry.geometry.CurveToPoints) | Generate a point cloud by sampling positions along curves |
| [CurvesToGreasePencil](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil) | Convert the curves in each top-level instance into Grease Pencil layer |
| [Cylinder](#nodebpy.nodes.geometry.geometry.Cylinder) | Generate a cylinder mesh |
| [DeformCurvesOnSurface](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface) | Translate and rotate curves based on changes between the object’s original and evaluated surface mesh |
| [DeleteGeometry](#nodebpy.nodes.geometry.geometry.DeleteGeometry) | Remove selected elements of a geometry |
| [DistributePointsOnFaces](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces) | Generate points spread out on the surface of a mesh |
| [DualMesh](#nodebpy.nodes.geometry.geometry.DualMesh) | Convert Faces into vertices and vertices into faces |
| [DuplicateElements](#nodebpy.nodes.geometry.geometry.DuplicateElements) | Generate an arbitrary number copies of each selected input element |
| [EdgePathsToCurves](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves) | Output curves following paths across mesh edges |
| [ExtrudeMesh](#nodebpy.nodes.geometry.geometry.ExtrudeMesh) | Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary |
| [FillCurve](#nodebpy.nodes.geometry.geometry.FillCurve) | Generate a mesh on the XY plane with faces on the inside of input curves |
| [FilletCurve](#nodebpy.nodes.geometry.geometry.FilletCurve) | Round corners by generating circular arcs on each control point |
| [FlipFaces](#nodebpy.nodes.geometry.geometry.FlipFaces) | Reverse the order of the vertices and edges of selected faces, flipping their normal direction |
| [GeometryProximity](#nodebpy.nodes.geometry.geometry.GeometryProximity) | Compute the closest location on the target geometry |
| [GreasePencilToCurves](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves) | Convert Grease Pencil layers into curve instances |
| [Grid](#nodebpy.nodes.geometry.geometry.Grid) | Generate a planar mesh on the XY plane |
| [IcoSphere](#nodebpy.nodes.geometry.geometry.IcoSphere) | Generate a spherical mesh that consists of equally sized triangles |
| [InstanceOnPoints](#nodebpy.nodes.geometry.geometry.InstanceOnPoints) | Generate a reference to geometry at each of the input points, without duplicating its underlying data |
| [InstancesToPoints](#nodebpy.nodes.geometry.geometry.InstancesToPoints) | Generate points at the origins of instances. |
| [InterpolateCurves](#nodebpy.nodes.geometry.geometry.InterpolateCurves) | Generate new curves on points by interpolating between existing curves |
| [MaterialSelection](#nodebpy.nodes.geometry.geometry.MaterialSelection) | Provide a selection of faces that use the specified material |
| [MergeByDistance](#nodebpy.nodes.geometry.geometry.MergeByDistance) | Merge vertices or points within a given distance |
| [MergeLayers](#nodebpy.nodes.geometry.geometry.MergeLayers) | Join groups of Grease Pencil layers into one |
| [MeshCircle](#nodebpy.nodes.geometry.geometry.MeshCircle) | Generate a circular ring of edges |
| [MeshLine](#nodebpy.nodes.geometry.geometry.MeshLine) | Generate vertices in a line and connect them with edges |
| [MeshToCurve](#nodebpy.nodes.geometry.geometry.MeshToCurve) | Generate a curve from a mesh |
| [MeshToPoints](#nodebpy.nodes.geometry.geometry.MeshToPoints) | Generate a point cloud from a mesh’s vertices |
| [Points](#nodebpy.nodes.geometry.geometry.Points) | Generate a point cloud with positions and radii defined by fields |
| [PointsToCurves](#nodebpy.nodes.geometry.geometry.PointsToCurves) | Split all points to curve by its group ID and reorder by weight |
| [PointsToVertices](#nodebpy.nodes.geometry.geometry.PointsToVertices) | Generate a mesh vertex for each point cloud point |
| [QuadraticBezier](#nodebpy.nodes.geometry.geometry.QuadraticBezier) | Generate a poly spline in a parabola shape with control points positions |
| [Quadrilateral](#nodebpy.nodes.geometry.geometry.Quadrilateral) | Generate a polygon with four points |
| [Raycast](#nodebpy.nodes.geometry.geometry.Raycast) | Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point |
| [RealizeInstances](#nodebpy.nodes.geometry.geometry.RealizeInstances) | Convert instances into real geometry data |
| [ReplaceMaterial](#nodebpy.nodes.geometry.geometry.ReplaceMaterial) | Swap one material with another |
| [ResampleCurve](#nodebpy.nodes.geometry.geometry.ResampleCurve) | Generate a poly spline for each input spline |
| [ReverseCurve](#nodebpy.nodes.geometry.geometry.ReverseCurve) | Change the direction of curves by swapping their start and end data |
| [RotateInstances](#nodebpy.nodes.geometry.geometry.RotateInstances) | Rotate geometry instances in local or global space |
| [SampleCurve](#nodebpy.nodes.geometry.geometry.SampleCurve) | Retrieve data from a point on a curve at a certain distance from its start |
| [SampleIndex](#nodebpy.nodes.geometry.geometry.SampleIndex) | Retrieve values from specific geometry elements |
| [SampleNearest](#nodebpy.nodes.geometry.geometry.SampleNearest) | Find the element of a geometry closest to a position. Similar to the “Index of Nearest” node |
| [SampleNearestSurface](#nodebpy.nodes.geometry.geometry.SampleNearestSurface) | Calculate the interpolated value of a mesh attribute on the closest point of its surface |
| [SampleUVSurface](#nodebpy.nodes.geometry.geometry.SampleUVSurface) | Calculate the interpolated values of a mesh attribute at a UV coordinate |
| [ScaleElements](#nodebpy.nodes.geometry.geometry.ScaleElements) | Scale groups of connected edges and faces |
| [ScaleInstances](#nodebpy.nodes.geometry.geometry.ScaleInstances) | Scale geometry instances in local or global space |
| [SeparateComponents](#nodebpy.nodes.geometry.geometry.SeparateComponents) | Split a geometry into a separate output for each type of data in the geometry |
| [SeparateGeometry](#nodebpy.nodes.geometry.geometry.SeparateGeometry) | Split a geometry into two geometry outputs based on a selection |
| [SetCurveNormal](#nodebpy.nodes.geometry.geometry.SetCurveNormal) | Set the evaluation mode for curve normals |
| [SetCurveRadius](#nodebpy.nodes.geometry.geometry.SetCurveRadius) | Set the radius of the curve at each control point |
| [SetCurveTilt](#nodebpy.nodes.geometry.geometry.SetCurveTilt) | Set the tilt angle at each curve control point |
| [SetFaceSet](#nodebpy.nodes.geometry.geometry.SetFaceSet) | Set sculpt face set values for faces |
| [SetGeometryName](#nodebpy.nodes.geometry.geometry.SetGeometryName) | Set the name of a geometry for easier debugging |
| [SetGreasePencilColor](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor) | Set color and opacity attributes on Grease Pencil geometry |
| [SetGreasePencilDepth](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth) | Set the Grease Pencil depth order to use |
| [SetGreasePencilSoftness](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness) | Set softness attribute on Grease Pencil geometry |
| [SetHandlePositions](#nodebpy.nodes.geometry.geometry.SetHandlePositions) | Set the positions for the handles of Bézier curves |
| [SetID](#nodebpy.nodes.geometry.geometry.SetID) | Set the id attribute on the input geometry, mainly used internally for randomizing |
| [SetInstanceTransform](#nodebpy.nodes.geometry.geometry.SetInstanceTransform) | Set the transformation matrix of every instance |
| [SetMaterial](#nodebpy.nodes.geometry.geometry.SetMaterial) | Assign a material to geometry elements |
| [SetMaterialIndex](#nodebpy.nodes.geometry.geometry.SetMaterialIndex) | Set the material index for each selected geometry element |
| [SetMeshNormal](#nodebpy.nodes.geometry.geometry.SetMeshNormal) | Store a normal vector for each mesh element |
| [SetPointRadius](#nodebpy.nodes.geometry.geometry.SetPointRadius) | Set the display size of point cloud points |
| [SetPosition](#nodebpy.nodes.geometry.geometry.SetPosition) | Set the location of each point |
| [SetSelection](#nodebpy.nodes.geometry.geometry.SetSelection) | Set selection of the edited geometry, for tool execution |
| [SetShadeSmooth](#nodebpy.nodes.geometry.geometry.SetShadeSmooth) | Control the smoothness of mesh normals around each face by changing the “shade smooth” attribute |
| [SetSplineCyclic](#nodebpy.nodes.geometry.geometry.SetSplineCyclic) | Control whether each spline loops back on itself by changing the “cyclic” attribute |
| [SetSplineResolution](#nodebpy.nodes.geometry.geometry.SetSplineResolution) | Control how many evaluated points should be generated on every curve segment |
| [SetSplineType](#nodebpy.nodes.geometry.geometry.SetSplineType) | Change the type of curves |
| [SortElements](#nodebpy.nodes.geometry.geometry.SortElements) | Rearrange geometry elements, changing their indices |
| [Spiral](#nodebpy.nodes.geometry.geometry.Spiral) | Generate a poly spline in a spiral shape |
| [SplitEdges](#nodebpy.nodes.geometry.geometry.SplitEdges) | Duplicate mesh edges and break connections with the surrounding faces |
| [SplitToInstances](#nodebpy.nodes.geometry.geometry.SplitToInstances) | Create separate geometries containing the elements from the same group |
| [Star](#nodebpy.nodes.geometry.geometry.Star) | Generate a poly spline in a star pattern by connecting alternating points of two circles |
| [StringToCurves](#nodebpy.nodes.geometry.geometry.StringToCurves) | Generate a paragraph of text with a specific font, using a curve instance to store each character |
| [SubdivideCurve](#nodebpy.nodes.geometry.geometry.SubdivideCurve) | Dividing each curve segment into a specified number of pieces |
| [SubdivideMesh](#nodebpy.nodes.geometry.geometry.SubdivideMesh) | Divide mesh faces into smaller ones without changing the shape or volume, using linear interpolation to place the new vertices |
| [SubdivisionSurface](#nodebpy.nodes.geometry.geometry.SubdivisionSurface) | Divide mesh faces to form a smooth surface, using the Catmull-Clark subdivision method |
| [TransformGeometry](#nodebpy.nodes.geometry.geometry.TransformGeometry) | Translate, rotate or scale the geometry |
| [TranslateInstances](#nodebpy.nodes.geometry.geometry.TranslateInstances) | Move top-level geometry instances in local or global space |
| [Triangulate](#nodebpy.nodes.geometry.geometry.Triangulate) | Convert all faces in a mesh to triangular faces |
| [TrimCurve](#nodebpy.nodes.geometry.geometry.TrimCurve) | Shorten curves by removing portions at the start or end |
| [UVSphere](#nodebpy.nodes.geometry.geometry.UVSphere) | Generate a spherical mesh with quads, except for triangles at the top and bottom |

### Arc

``` python
Arc(
    resolution=16,
    start=None,
    middle=None,
    end=None,
    radius=1.0,
    start_angle=0.0,
    sweep_angle=5.4978,
    offset_angle=0.0,
    connect_center=False,
    invert_arc=False,
    *,
    mode='RADIUS',
)
```

Generate a poly spline arc

#### Parameters

| Name           | Type         | Description    | Default  |
|----------------|--------------|----------------|----------|
| resolution     | InputInteger | Resolution     | `16`     |
| start          | InputVector  | Start          | `None`   |
| middle         | InputVector  | Middle         | `None`   |
| end            | InputVector  | End            | `None`   |
| radius         | InputFloat   | Radius         | `1.0`    |
| start_angle    | InputFloat   | Start Angle    | `0.0`    |
| sweep_angle    | InputFloat   | Sweep Angle    | `5.4978` |
| offset_angle   | InputFloat   | Offset Angle   | `0.0`    |
| connect_center | InputBoolean | Connect Center | `False`  |
| invert_arc     | InputBoolean | Invert Arc     | `False`  |

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Arc.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Arc.inputs)   |             |
| [`mode`](#nodebpy.nodes.geometry.geometry.Arc.mode)       |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Arc.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Arc.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Arc.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Arc.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Arc.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Arc.type)       |             |

#### Methods

| Name | Description |
|----|----|
| [points](#nodebpy.nodes.geometry.geometry.Arc.points) | Create Arc with operation ‘Points’. Define arc by 3 points on circle. Arc is calculated between start and end points |
| [radius](#nodebpy.nodes.geometry.geometry.Arc.radius) | Create Arc with operation ‘Radius’. Define radius with a float |

##### points

``` python
points(
    resolution=16,
    start=None,
    middle=None,
    end=None,
    offset_angle=0.0,
    connect_center=False,
    invert_arc=False,
)
```

Create Arc with operation ‘Points’. Define arc by 3 points on circle. Arc is calculated between start and end points

##### radius

``` python
radius(
    resolution=16,
    radius=1.0,
    start_angle=0.0,
    sweep_angle=5.4978,
    connect_center=False,
    invert_arc=False,
)
```

Create Arc with operation ‘Radius’. Define radius with a float

**Inputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `i.resolution`     | `IntegerSocket` | Resolution     |
| `i.start`          | `VectorSocket`  | Start          |
| `i.middle`         | `VectorSocket`  | Middle         |
| `i.end`            | `VectorSocket`  | End            |
| `i.radius`         | `FloatSocket`   | Radius         |
| `i.start_angle`    | `FloatSocket`   | Start Angle    |
| `i.sweep_angle`    | `FloatSocket`   | Sweep Angle    |
| `i.offset_angle`   | `FloatSocket`   | Offset Angle   |
| `i.connect_center` | `BooleanSocket` | Connect Center |
| `i.invert_arc`     | `BooleanSocket` | Invert Arc     |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curve`  | `GeometrySocket` | Curve       |
| `o.center` | `VectorSocket`   | Center      |
| `o.normal` | `VectorSocket`   | Normal      |
| `o.radius` | `FloatSocket`    | Radius      |

### BezierSegment

``` python
BezierSegment(
    resolution=16,
    start=None,
    start_handle=None,
    end_handle=None,
    end=None,
    *,
    mode='POSITION',
)
```

Generate a 2D Bézier spline from the given control points and handles

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| resolution   | InputInteger | Resolution   | `16`    |
| start        | InputVector  | Start        | `None`  |
| start_handle | InputVector  | Start Handle | `None`  |
| end_handle   | InputVector  | End Handle   | `None`  |
| end          | InputVector  | End          | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.BezierSegment.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.BezierSegment.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.BezierSegment.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.BezierSegment.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.BezierSegment.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.BezierSegment.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.BezierSegment.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.BezierSegment.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.BezierSegment.type) |  |

#### Methods

| Name | Description |
|----|----|
| [offset](#nodebpy.nodes.geometry.geometry.BezierSegment.offset) | Create Bézier Segment with operation ‘Offset’. The start and end handles are offsets from the spline’s control points |
| [position](#nodebpy.nodes.geometry.geometry.BezierSegment.position) | Create Bézier Segment with operation ‘Position’. The start and end handles are fixed positions |

##### offset

``` python
offset(resolution=16, start=None, start_handle=None, end_handle=None, end=None)
```

Create Bézier Segment with operation ‘Offset’. The start and end handles are offsets from the spline’s control points

##### position

``` python
position(
    resolution=16,
    start=None,
    start_handle=None,
    end_handle=None,
    end=None,
)
```

Create Bézier Segment with operation ‘Position’. The start and end handles are fixed positions

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.resolution`   | `IntegerSocket` | Resolution   |
| `i.start`        | `VectorSocket`  | Start        |
| `i.start_handle` | `VectorSocket`  | Start Handle |
| `i.end_handle`   | `VectorSocket`  | End Handle   |
| `i.end`          | `VectorSocket`  | End          |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### BoundingBox

``` python
BoundingBox(geometry=None, use_radius=True)
```

Calculate the limits of a geometry’s positions and generate a box mesh with those dimensions

#### Parameters

| Name       | Type          | Description | Default |
|------------|---------------|-------------|---------|
| geometry   | InputGeometry | Geometry    | `None`  |
| use_radius | InputBoolean  | Use Radius  | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.BoundingBox.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.BoundingBox.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.BoundingBox.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.BoundingBox.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.BoundingBox.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.BoundingBox.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.BoundingBox.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.BoundingBox.type) |  |

**Inputs**

| Attribute      | Type             | Description |
|----------------|------------------|-------------|
| `i.geometry`   | `GeometrySocket` | Geometry    |
| `i.use_radius` | `BooleanSocket`  | Use Radius  |

**Outputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `o.bounding_box` | `GeometrySocket` | Bounding Box |
| `o.min`          | `VectorSocket`   | Min          |
| `o.max`          | `VectorSocket`   | Max          |

### Cone

``` python
Cone(
    vertices=32,
    side_segments=1,
    fill_segments=1,
    radius_top=0.0,
    radius_bottom=1.0,
    depth=2.0,
    *,
    fill_type='NGON',
)
```

Generate a cone mesh

#### Parameters

| Name          | Type         | Description   | Default |
|---------------|--------------|---------------|---------|
| vertices      | InputInteger | Vertices      | `32`    |
| side_segments | InputInteger | Side Segments | `1`     |
| fill_segments | InputInteger | Fill Segments | `1`     |
| radius_top    | InputFloat   | Radius Top    | `0.0`   |
| radius_bottom | InputFloat   | Radius Bottom | `1.0`   |
| depth         | InputFloat   | Depth         | `2.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`fill_type`](#nodebpy.nodes.geometry.geometry.Cone.fill_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.Cone.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Cone.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.Cone.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.Cone.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.Cone.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Cone.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.Cone.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.Cone.type) |  |

#### Methods

| Name | Description |
|----|----|
| [n_gon](#nodebpy.nodes.geometry.geometry.Cone.n_gon) | Create Cone with operation ‘N-Gon’. |
| [none](#nodebpy.nodes.geometry.geometry.Cone.none) | Create Cone with operation ‘None’. |
| [triangles](#nodebpy.nodes.geometry.geometry.Cone.triangles) | Create Cone with operation ‘Triangles’. |

##### n_gon

``` python
n_gon(
    vertices=32,
    side_segments=1,
    fill_segments=1,
    radius_top=0.0,
    radius_bottom=1.0,
    depth=2.0,
)
```

Create Cone with operation ‘N-Gon’.

##### none

``` python
none(vertices=32, side_segments=1, radius_top=0.0, radius_bottom=1.0, depth=2.0)
```

Create Cone with operation ‘None’.

##### triangles

``` python
triangles(
    vertices=32,
    side_segments=1,
    fill_segments=1,
    radius_top=0.0,
    radius_bottom=1.0,
    depth=2.0,
)
```

Create Cone with operation ‘Triangles’.

**Inputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `i.vertices`      | `IntegerSocket` | Vertices      |
| `i.side_segments` | `IntegerSocket` | Side Segments |
| `i.fill_segments` | `IntegerSocket` | Fill Segments |
| `i.radius_top`    | `FloatSocket`   | Radius Top    |
| `i.radius_bottom` | `FloatSocket`   | Radius Bottom |
| `i.depth`         | `FloatSocket`   | Depth         |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.top`    | `BooleanSocket`  | Top         |
| `o.bottom` | `BooleanSocket`  | Bottom      |
| `o.side`   | `BooleanSocket`  | Side        |
| `o.uv_map` | `VectorSocket`   | UV Map      |

### ConvexHull

``` python
ConvexHull(geometry=None)
```

Create a mesh that encloses all points in the input geometry with the smallest number of points

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ConvexHull.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ConvexHull.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ConvexHull.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ConvexHull.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ConvexHull.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ConvexHull.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ConvexHull.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ConvexHull.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |

**Outputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `o.convex_hull` | `GeometrySocket` | Convex Hull |

### Cube

``` python
Cube(size=None, vertices_x=2, vertices_y=2, vertices_z=2)
```

Generate a cuboid mesh with variable side lengths and subdivisions

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| size       | InputVector  | Size        | `None`  |
| vertices_x | InputInteger | Vertices X  | `2`     |
| vertices_y | InputInteger | Vertices Y  | `2`     |
| vertices_z | InputInteger | Vertices Z  | `2`     |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Cube.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Cube.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Cube.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Cube.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Cube.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Cube.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Cube.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Cube.type)       |             |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.size`       | `VectorSocket`  | Size        |
| `i.vertices_x` | `IntegerSocket` | Vertices X  |
| `i.vertices_y` | `IntegerSocket` | Vertices Y  |
| `i.vertices_z` | `IntegerSocket` | Vertices Z  |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.uv_map` | `VectorSocket`   | UV Map      |

### CurveCircle

``` python
CurveCircle(
    resolution=32,
    point_1=None,
    point_2=None,
    point_3=None,
    radius=1.0,
    *,
    mode='RADIUS',
)
```

Generate a poly spline circle

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| resolution | InputInteger | Resolution  | `32`    |
| point_1    | InputVector  | Point 1     | `None`  |
| point_2    | InputVector  | Point 2     | `None`  |
| point_3    | InputVector  | Point 3     | `None`  |
| radius     | InputFloat   | Radius      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurveCircle.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurveCircle.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.CurveCircle.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurveCircle.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurveCircle.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurveCircle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurveCircle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurveCircle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurveCircle.type) |  |

#### Methods

| Name | Description |
|----|----|
| [points](#nodebpy.nodes.geometry.geometry.CurveCircle.points) | Create Curve Circle with operation ‘Points’. Define the radius and location with three points |
| [radius](#nodebpy.nodes.geometry.geometry.CurveCircle.radius) | Create Curve Circle with operation ‘Radius’. Define the radius with a float |

##### points

``` python
points(resolution=32, point_1=None, point_2=None, point_3=None)
```

Create Curve Circle with operation ‘Points’. Define the radius and location with three points

##### radius

``` python
radius(resolution=32, radius=1.0)
```

Create Curve Circle with operation ‘Radius’. Define the radius with a float

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.resolution` | `IntegerSocket` | Resolution  |
| `i.point_1`    | `VectorSocket`  | Point 1     |
| `i.point_2`    | `VectorSocket`  | Point 2     |
| `i.point_3`    | `VectorSocket`  | Point 3     |
| `i.radius`     | `FloatSocket`   | Radius      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curve`  | `GeometrySocket` | Curve       |
| `o.center` | `VectorSocket`   | Center      |

### CurveLength

``` python
CurveLength(curve=None)
```

Retrieve the length of all splines added together

#### Parameters

| Name  | Type          | Description | Default |
|-------|---------------|-------------|---------|
| curve | InputGeometry | Curve       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurveLength.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurveLength.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurveLength.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurveLength.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurveLength.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurveLength.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurveLength.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurveLength.type) |  |

**Inputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `i.curve` | `GeometrySocket` | Curve       |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.length` | `FloatSocket` | Length      |

### CurveLine

``` python
CurveLine(start=None, end=None, direction=None, length=1.0, *, mode='POINTS')
```

Generate a poly spline line with two points

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| start     | InputVector | Start       | `None`  |
| end       | InputVector | End         | `None`  |
| direction | InputVector | Direction   | `None`  |
| length    | InputFloat  | Length      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurveLine.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurveLine.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.CurveLine.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurveLine.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurveLine.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurveLine.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurveLine.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurveLine.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurveLine.type) |  |

#### Methods

| Name | Description |
|----|----|
| [direction](#nodebpy.nodes.geometry.geometry.CurveLine.direction) | Create Curve Line with operation ‘Direction’. Define a line with a start point, direction and length |
| [points](#nodebpy.nodes.geometry.geometry.CurveLine.points) | Create Curve Line with operation ‘Points’. Define the start and end points of the line |

##### direction

``` python
direction(start=None, direction=None, length=1.0)
```

Create Curve Line with operation ‘Direction’. Define a line with a start point, direction and length

##### points

``` python
points(start=None, end=None)
```

Create Curve Line with operation ‘Points’. Define the start and end points of the line

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.start`     | `VectorSocket` | Start       |
| `i.end`       | `VectorSocket` | End         |
| `i.direction` | `VectorSocket` | Direction   |
| `i.length`    | `FloatSocket`  | Length      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### CurveToMesh

``` python
CurveToMesh(curve=None, profile_curve=None, scale=1.0, fill_caps=False)
```

Convert curves into a mesh, optionally with a custom profile shape defined by curves

#### Parameters

| Name          | Type          | Description   | Default |
|---------------|---------------|---------------|---------|
| curve         | InputGeometry | Curve         | `None`  |
| profile_curve | InputGeometry | Profile Curve | `None`  |
| scale         | InputFloat    | Scale         | `1.0`   |
| fill_caps     | InputBoolean  | Fill Caps     | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurveToMesh.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurveToMesh.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurveToMesh.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurveToMesh.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurveToMesh.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurveToMesh.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurveToMesh.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurveToMesh.type) |  |

**Inputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `i.curve`         | `GeometrySocket` | Curve         |
| `i.profile_curve` | `GeometrySocket` | Profile Curve |
| `i.scale`         | `FloatSocket`    | Scale         |
| `i.fill_caps`     | `BooleanSocket`  | Fill Caps     |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### CurveToPoints

``` python
CurveToPoints(curve=None, count=10, length=0.1, *, mode='COUNT')
```

Generate a point cloud by sampling positions along curves

#### Parameters

| Name   | Type          | Description | Default |
|--------|---------------|-------------|---------|
| curve  | InputGeometry | Curve       | `None`  |
| count  | InputInteger  | Count       | `10`    |
| length | InputFloat    | Length      | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurveToPoints.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurveToPoints.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.CurveToPoints.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurveToPoints.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurveToPoints.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurveToPoints.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurveToPoints.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurveToPoints.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurveToPoints.type) |  |

#### Methods

| Name | Description |
|----|----|
| [count](#nodebpy.nodes.geometry.geometry.CurveToPoints.count) | Create Curve to Points with operation ‘Count’. Sample each spline by evenly distributing the specified number of points |
| [evaluated](#nodebpy.nodes.geometry.geometry.CurveToPoints.evaluated) | Create Curve to Points with operation ‘Evaluated’. Create points from the curve’s evaluated points, based on the resolution attribute for NURBS and Bézier splines |
| [length](#nodebpy.nodes.geometry.geometry.CurveToPoints.length) | Create Curve to Points with operation ‘Length’. Sample each spline by splitting it into segments with the specified length |

##### count

``` python
count(curve=None, count=10)
```

Create Curve to Points with operation ‘Count’. Sample each spline by evenly distributing the specified number of points

##### evaluated

``` python
evaluated(curve=None)
```

Create Curve to Points with operation ‘Evaluated’. Create points from the curve’s evaluated points, based on the resolution attribute for NURBS and Bézier splines

##### length

``` python
length(curve=None, length=0.1)
```

Create Curve to Points with operation ‘Length’. Sample each spline by splitting it into segments with the specified length

**Inputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `i.curve`  | `GeometrySocket` | Curve       |
| `i.count`  | `IntegerSocket`  | Count       |
| `i.length` | `FloatSocket`    | Length      |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.points`   | `GeometrySocket` | Points      |
| `o.tangent`  | `VectorSocket`   | Tangent     |
| `o.normal`   | `VectorSocket`   | Normal      |
| `o.rotation` | `RotationSocket` | Rotation    |

### CurvesToGreasePencil

``` python
CurvesToGreasePencil(curves=None, selection=True, instances_as_layers=True)
```

Convert the curves in each top-level instance into Grease Pencil layer

#### Parameters

| Name                | Type          | Description         | Default |
|---------------------|---------------|---------------------|---------|
| curves              | InputGeometry | Curves              | `None`  |
| selection           | InputBoolean  | Selection           | `True`  |
| instances_as_layers | InputBoolean  | Instances as Layers | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.CurvesToGreasePencil.type) |  |

**Inputs**

| Attribute               | Type             | Description         |
|-------------------------|------------------|---------------------|
| `i.curves`              | `GeometrySocket` | Curves              |
| `i.selection`           | `BooleanSocket`  | Selection           |
| `i.instances_as_layers` | `BooleanSocket`  | Instances as Layers |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |

### Cylinder

``` python
Cylinder(
    vertices=32,
    side_segments=1,
    fill_segments=1,
    radius=1.0,
    depth=2.0,
    *,
    fill_type='NGON',
)
```

Generate a cylinder mesh

#### Parameters

| Name          | Type         | Description   | Default |
|---------------|--------------|---------------|---------|
| vertices      | InputInteger | Vertices      | `32`    |
| side_segments | InputInteger | Side Segments | `1`     |
| fill_segments | InputInteger | Fill Segments | `1`     |
| radius        | InputFloat   | Radius        | `1.0`   |
| depth         | InputFloat   | Depth         | `2.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`fill_type`](#nodebpy.nodes.geometry.geometry.Cylinder.fill_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.Cylinder.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Cylinder.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.Cylinder.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.Cylinder.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.Cylinder.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Cylinder.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.Cylinder.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.Cylinder.type) |  |

#### Methods

| Name | Description |
|----|----|
| [n_gon](#nodebpy.nodes.geometry.geometry.Cylinder.n_gon) | Create Cylinder with operation ‘N-Gon’. |
| [none](#nodebpy.nodes.geometry.geometry.Cylinder.none) | Create Cylinder with operation ‘None’. |
| [triangles](#nodebpy.nodes.geometry.geometry.Cylinder.triangles) | Create Cylinder with operation ‘Triangles’. |

##### n_gon

``` python
n_gon(vertices=32, side_segments=1, fill_segments=1, radius=1.0, depth=2.0)
```

Create Cylinder with operation ‘N-Gon’.

##### none

``` python
none(vertices=32, side_segments=1, radius=1.0, depth=2.0)
```

Create Cylinder with operation ‘None’.

##### triangles

``` python
triangles(vertices=32, side_segments=1, fill_segments=1, radius=1.0, depth=2.0)
```

Create Cylinder with operation ‘Triangles’.

**Inputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `i.vertices`      | `IntegerSocket` | Vertices      |
| `i.side_segments` | `IntegerSocket` | Side Segments |
| `i.fill_segments` | `IntegerSocket` | Fill Segments |
| `i.radius`        | `FloatSocket`   | Radius        |
| `i.depth`         | `FloatSocket`   | Depth         |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.top`    | `BooleanSocket`  | Top         |
| `o.side`   | `BooleanSocket`  | Side        |
| `o.bottom` | `BooleanSocket`  | Bottom      |
| `o.uv_map` | `VectorSocket`   | UV Map      |

### DeformCurvesOnSurface

``` python
DeformCurvesOnSurface(curves=None)
```

Translate and rotate curves based on changes between the object’s original and evaluated surface mesh

#### Parameters

| Name   | Type          | Description | Default |
|--------|---------------|-------------|---------|
| curves | InputGeometry | Curves      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.DeformCurvesOnSurface.type) |  |

**Inputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `i.curves` | `GeometrySocket` | Curves      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curves` | `GeometrySocket` | Curves      |

### DeleteGeometry

``` python
DeleteGeometry(geometry=None, selection=True, *, mode='ALL', domain='POINT')
```

Remove selected elements of a geometry

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.DeleteGeometry.type) |  |

#### Methods

| Name | Description |
|----|----|
| [all](#nodebpy.nodes.geometry.geometry.DeleteGeometry.all) | Create Delete Geometry with operation ‘All’. |
| [edge](#nodebpy.nodes.geometry.geometry.DeleteGeometry.edge) | Create Delete Geometry with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.DeleteGeometry.face) | Create Delete Geometry with operation ‘Face’. Attribute on mesh faces |
| [instance](#nodebpy.nodes.geometry.geometry.DeleteGeometry.instance) | Create Delete Geometry with operation ‘Instance’. Attribute on instance |
| [layer](#nodebpy.nodes.geometry.geometry.DeleteGeometry.layer) | Create Delete Geometry with operation ‘Layer’. Attribute on Grease Pencil layer |
| [only_edges_faces](#nodebpy.nodes.geometry.geometry.DeleteGeometry.only_edges_faces) | Create Delete Geometry with operation ‘Only Edges & Faces’. |
| [only_faces](#nodebpy.nodes.geometry.geometry.DeleteGeometry.only_faces) | Create Delete Geometry with operation ‘Only Faces’. |
| [point](#nodebpy.nodes.geometry.geometry.DeleteGeometry.point) | Create Delete Geometry with operation ‘Point’. Attribute on point |
| [spline](#nodebpy.nodes.geometry.geometry.DeleteGeometry.spline) | Create Delete Geometry with operation ‘Spline’. Attribute on spline |

##### all

``` python
all(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘All’.

##### edge

``` python
edge(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Face’. Attribute on mesh faces

##### instance

``` python
instance(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Instance’. Attribute on instance

##### layer

``` python
layer(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Layer’. Attribute on Grease Pencil layer

##### only_edges_faces

``` python
only_edges_faces(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Only Edges & Faces’.

##### only_faces

``` python
only_faces(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Only Faces’.

##### point

``` python
point(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Point’. Attribute on point

##### spline

``` python
spline(geometry=None, selection=True)
```

Create Delete Geometry with operation ‘Spline’. Attribute on spline

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### DistributePointsOnFaces

``` python
DistributePointsOnFaces(
    mesh=None,
    selection=True,
    distance_min=0.0,
    density_max=10.0,
    density=10.0,
    density_factor=1.0,
    seed=0,
    *,
    distribute_method='RANDOM',
    use_legacy_normal=False,
)
```

Generate points spread out on the surface of a mesh

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| mesh           | InputGeometry | Mesh           | `None`  |
| selection      | InputBoolean  | Selection      | `True`  |
| distance_min   | InputFloat    | Distance Min   | `0.0`   |
| density_max    | InputFloat    | Density Max    | `10.0`  |
| density        | InputFloat    | Density        | `10.0`  |
| density_factor | InputFloat    | Density Factor | `1.0`   |
| seed           | InputInteger  | Seed           | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`distribute_method`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.distribute_method) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.type) |  |
| [`use_legacy_normal`](#nodebpy.nodes.geometry.geometry.DistributePointsOnFaces.use_legacy_normal) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.mesh`           | `GeometrySocket` | Mesh           |
| `i.selection`      | `BooleanSocket`  | Selection      |
| `i.distance_min`   | `FloatSocket`    | Distance Min   |
| `i.density_max`    | `FloatSocket`    | Density Max    |
| `i.density`        | `FloatSocket`    | Density        |
| `i.density_factor` | `FloatSocket`    | Density Factor |
| `i.seed`           | `IntegerSocket`  | Seed           |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.points`   | `GeometrySocket` | Points      |
| `o.normal`   | `VectorSocket`   | Normal      |
| `o.rotation` | `RotationSocket` | Rotation    |

### DualMesh

``` python
DualMesh(mesh=None, keep_boundaries=False)
```

Convert Faces into vertices and vertices into faces

#### Parameters

| Name            | Type          | Description     | Default |
|-----------------|---------------|-----------------|---------|
| mesh            | InputGeometry | Mesh            | `None`  |
| keep_boundaries | InputBoolean  | Keep Boundaries | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.DualMesh.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.DualMesh.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.DualMesh.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.DualMesh.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.DualMesh.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.DualMesh.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.DualMesh.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.DualMesh.type) |  |

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.mesh`            | `GeometrySocket` | Mesh            |
| `i.keep_boundaries` | `BooleanSocket`  | Keep Boundaries |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.dual_mesh` | `GeometrySocket` | Dual Mesh   |

### DuplicateElements

``` python
DuplicateElements(geometry=None, selection=True, amount=1, *, domain='POINT')
```

Generate an arbitrary number copies of each selected input element

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| amount    | InputInteger  | Amount      | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.DuplicateElements.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.DuplicateElements.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.DuplicateElements.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.DuplicateElements.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.DuplicateElements.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.DuplicateElements.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.DuplicateElements.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.DuplicateElements.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.DuplicateElements.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.DuplicateElements.edge) | Create Duplicate Elements with operation ‘Edge’. |
| [face](#nodebpy.nodes.geometry.geometry.DuplicateElements.face) | Create Duplicate Elements with operation ‘Face’. |
| [instance](#nodebpy.nodes.geometry.geometry.DuplicateElements.instance) | Create Duplicate Elements with operation ‘Instance’. |
| [layer](#nodebpy.nodes.geometry.geometry.DuplicateElements.layer) | Create Duplicate Elements with operation ‘Layer’. |
| [point](#nodebpy.nodes.geometry.geometry.DuplicateElements.point) | Create Duplicate Elements with operation ‘Point’. |
| [spline](#nodebpy.nodes.geometry.geometry.DuplicateElements.spline) | Create Duplicate Elements with operation ‘Spline’. |

##### edge

``` python
edge(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Edge’.

##### face

``` python
face(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Face’.

##### instance

``` python
instance(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Instance’.

##### layer

``` python
layer(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Layer’.

##### point

``` python
point(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Point’.

##### spline

``` python
spline(geometry=None, selection=True, amount=1)
```

Create Duplicate Elements with operation ‘Spline’.

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.amount`    | `IntegerSocket`  | Amount      |

**Outputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `o.geometry`        | `GeometrySocket` | Geometry        |
| `o.duplicate_index` | `IntegerSocket`  | Duplicate Index |

### EdgePathsToCurves

``` python
EdgePathsToCurves(mesh=None, start_vertices=True, next_vertex_index=-1)
```

Output curves following paths across mesh edges

#### Parameters

| Name              | Type          | Description       | Default |
|-------------------|---------------|-------------------|---------|
| mesh              | InputGeometry | Mesh              | `None`  |
| start_vertices    | InputBoolean  | Start Vertices    | `True`  |
| next_vertex_index | InputInteger  | Next Vertex Index | `-1`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.EdgePathsToCurves.type) |  |

**Inputs**

| Attribute             | Type             | Description       |
|-----------------------|------------------|-------------------|
| `i.mesh`              | `GeometrySocket` | Mesh              |
| `i.start_vertices`    | `BooleanSocket`  | Start Vertices    |
| `i.next_vertex_index` | `IntegerSocket`  | Next Vertex Index |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curves` | `GeometrySocket` | Curves      |

### ExtrudeMesh

``` python
ExtrudeMesh(
    mesh=None,
    selection=True,
    offset=None,
    offset_scale=1.0,
    individual=True,
    *,
    mode='FACES',
)
```

Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary

#### Parameters

| Name         | Type          | Description  | Default |
|--------------|---------------|--------------|---------|
| mesh         | InputGeometry | Mesh         | `None`  |
| selection    | InputBoolean  | Selection    | `True`  |
| offset       | InputVector   | Offset       | `None`  |
| offset_scale | InputFloat    | Offset Scale | `1.0`   |
| individual   | InputBoolean  | Individual   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edges](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.edges) | Create Extrude Mesh with operation ‘Edges’. |
| [faces](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.faces) | Create Extrude Mesh with operation ‘Faces’. |
| [vertices](#nodebpy.nodes.geometry.geometry.ExtrudeMesh.vertices) | Create Extrude Mesh with operation ‘Vertices’. |

##### edges

``` python
edges(mesh=None, selection=True, offset=None, offset_scale=1.0)
```

Create Extrude Mesh with operation ‘Edges’.

##### faces

``` python
faces(mesh=None, selection=True, offset=None, offset_scale=1.0, individual=True)
```

Create Extrude Mesh with operation ‘Faces’.

##### vertices

``` python
vertices(mesh=None, selection=True, offset=None, offset_scale=1.0)
```

Create Extrude Mesh with operation ‘Vertices’.

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.mesh`         | `GeometrySocket` | Mesh         |
| `i.selection`    | `BooleanSocket`  | Selection    |
| `i.offset`       | `VectorSocket`   | Offset       |
| `i.offset_scale` | `FloatSocket`    | Offset Scale |
| `i.individual`   | `BooleanSocket`  | Individual   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |
| `o.top`   | `BooleanSocket`  | Top         |
| `o.side`  | `BooleanSocket`  | Side        |

### FillCurve

``` python
FillCurve(curve=None, group_id=0, mode='Triangles')
```

Generate a mesh on the XY plane with faces on the inside of input curves

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| curve | InputGeometry | Curve | `None` |
| group_id | InputInteger | Group ID | `0` |
| mode | InputMenu \| Literal\['Triangles', 'N-gons'\] | Mode | `'Triangles'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.FillCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.FillCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.FillCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.FillCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.FillCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.FillCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.FillCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.FillCurve.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.curve`    | `GeometrySocket` | Curve       |
| `i.group_id` | `IntegerSocket`  | Group ID    |
| `i.mode`     | `MenuSocket`     | Mode        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### FilletCurve

``` python
FilletCurve(curve=None, radius=0.25, limit_radius=False, mode='Bézier', count=1)
```

Round corners by generating circular arcs on each control point

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| curve | InputGeometry | Curve | `None` |
| radius | InputFloat | Radius | `0.25` |
| limit_radius | InputBoolean | Limit Radius | `False` |
| mode | InputMenu \| Literal\['Bézier', 'Poly'\] | Mode | `'Bézier'` |
| count | InputInteger | Count | `1` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.FilletCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.FilletCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.FilletCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.FilletCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.FilletCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.FilletCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.FilletCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.FilletCurve.type) |  |

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.curve`        | `GeometrySocket` | Curve        |
| `i.radius`       | `FloatSocket`    | Radius       |
| `i.limit_radius` | `BooleanSocket`  | Limit Radius |
| `i.mode`         | `MenuSocket`     | Mode         |
| `i.count`        | `IntegerSocket`  | Count        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### FlipFaces

``` python
FlipFaces(mesh=None, selection=True)
```

Reverse the order of the vertices and edges of selected faces, flipping their normal direction

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| mesh      | InputGeometry | Mesh        | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.FlipFaces.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.FlipFaces.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.FlipFaces.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.FlipFaces.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.FlipFaces.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.FlipFaces.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.FlipFaces.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.FlipFaces.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.mesh`      | `GeometrySocket` | Mesh        |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### GeometryProximity

``` python
GeometryProximity(
    target=None,
    group_id=0,
    source_position=None,
    sample_group_id=0,
    *,
    target_element='FACES',
)
```

Compute the closest location on the target geometry

#### Parameters

| Name            | Type          | Description     | Default |
|-----------------|---------------|-----------------|---------|
| target          | InputGeometry | Geometry        | `None`  |
| group_id        | InputInteger  | Group ID        | `0`     |
| source_position | InputVector   | Sample Position | `None`  |
| sample_group_id | InputInteger  | Sample Group ID | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.GeometryProximity.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.GeometryProximity.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.GeometryProximity.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.GeometryProximity.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.GeometryProximity.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.GeometryProximity.outputs) |  |
| [`target_element`](#nodebpy.nodes.geometry.geometry.GeometryProximity.target_element) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.GeometryProximity.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.GeometryProximity.type) |  |

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.target`          | `GeometrySocket` | Geometry        |
| `i.group_id`        | `IntegerSocket`  | Group ID        |
| `i.source_position` | `VectorSocket`   | Sample Position |
| `i.sample_group_id` | `IntegerSocket`  | Sample Group ID |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.position` | `VectorSocket`  | Position    |
| `o.distance` | `FloatSocket`   | Distance    |
| `o.is_valid` | `BooleanSocket` | Is Valid    |

### GreasePencilToCurves

``` python
GreasePencilToCurves(
    grease_pencil=None,
    selection=True,
    layers_as_instances=True,
)
```

Convert Grease Pencil layers into curve instances

#### Parameters

| Name                | Type          | Description         | Default |
|---------------------|---------------|---------------------|---------|
| grease_pencil       | InputGeometry | Grease Pencil       | `None`  |
| selection           | InputBoolean  | Selection           | `True`  |
| layers_as_instances | InputBoolean  | Layers as Instances | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.GreasePencilToCurves.type) |  |

**Inputs**

| Attribute               | Type             | Description         |
|-------------------------|------------------|---------------------|
| `i.grease_pencil`       | `GeometrySocket` | Grease Pencil       |
| `i.selection`           | `BooleanSocket`  | Selection           |
| `i.layers_as_instances` | `BooleanSocket`  | Layers as Instances |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curves` | `GeometrySocket` | Curves      |

### Grid

``` python
Grid(size_x=1.0, size_y=1.0, vertices_x=3, vertices_y=3)
```

Generate a planar mesh on the XY plane

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| size_x     | InputFloat   | Size X      | `1.0`   |
| size_y     | InputFloat   | Size Y      | `1.0`   |
| vertices_x | InputInteger | Vertices X  | `3`     |
| vertices_y | InputInteger | Vertices Y  | `3`     |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Grid.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Grid.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Grid.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Grid.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Grid.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Grid.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Grid.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Grid.type)       |             |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.size_x`     | `FloatSocket`   | Size X      |
| `i.size_y`     | `FloatSocket`   | Size Y      |
| `i.vertices_x` | `IntegerSocket` | Vertices X  |
| `i.vertices_y` | `IntegerSocket` | Vertices Y  |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.uv_map` | `VectorSocket`   | UV Map      |

### IcoSphere

``` python
IcoSphere(radius=1.0, subdivisions=1)
```

Generate a spherical mesh that consists of equally sized triangles

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| radius       | InputFloat   | Radius       | `1.0`   |
| subdivisions | InputInteger | Subdivisions | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.IcoSphere.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.IcoSphere.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.IcoSphere.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.IcoSphere.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.IcoSphere.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.IcoSphere.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.IcoSphere.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.IcoSphere.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.radius`       | `FloatSocket`   | Radius       |
| `i.subdivisions` | `IntegerSocket` | Subdivisions |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.uv_map` | `VectorSocket`   | UV Map      |

### InstanceOnPoints

``` python
InstanceOnPoints(
    points=None,
    selection=True,
    instance=None,
    pick_instance=False,
    instance_index=0,
    rotation=None,
    scale=None,
)
```

Generate a reference to geometry at each of the input points, without duplicating its underlying data

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| points         | InputGeometry | Points         | `None`  |
| selection      | InputBoolean  | Selection      | `True`  |
| instance       | InputGeometry | Instance       | `None`  |
| pick_instance  | InputBoolean  | Pick Instance  | `False` |
| instance_index | InputInteger  | Instance Index | `0`     |
| rotation       | InputRotation | Rotation       | `None`  |
| scale          | InputVector   | Scale          | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.InstanceOnPoints.type) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.points`         | `GeometrySocket` | Points         |
| `i.selection`      | `BooleanSocket`  | Selection      |
| `i.instance`       | `GeometrySocket` | Instance       |
| `i.pick_instance`  | `BooleanSocket`  | Pick Instance  |
| `i.instance_index` | `IntegerSocket`  | Instance Index |
| `i.rotation`       | `RotationSocket` | Rotation       |
| `i.scale`          | `VectorSocket`   | Scale          |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### InstancesToPoints

``` python
InstancesToPoints(instances=None, selection=True, position=None, radius=0.05)
```

    Generate points at the origins of instances.

Note: Nested instances are not affected by this node

#### Parameters

    instances : InputGeometry
        Instances
    selection : InputBoolean
        Selection
    position : InputVector
        Position
    radius : InputFloat
        Radius

#### Inputs

    i.instances : GeometrySocket
        Instances
    i.selection : BooleanSocket
        Selection
    i.position : VectorSocket
        Position
    i.radius : FloatSocket
        Radius

#### Outputs

    o.points : GeometrySocket
        Points

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.InstancesToPoints.type) |  |

### InterpolateCurves

``` python
InterpolateCurves(
    guide_curves=None,
    guide_up=None,
    guide_group_id=0,
    points=None,
    point_up=None,
    point_group_id=0,
    max_neighbors=4,
)
```

Generate new curves on points by interpolating between existing curves

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| guide_curves   | InputGeometry | Guide Curves   | `None`  |
| guide_up       | InputVector   | Guide Up       | `None`  |
| guide_group_id | InputInteger  | Guide Group ID | `0`     |
| points         | InputGeometry | Points         | `None`  |
| point_up       | InputVector   | Point Up       | `None`  |
| point_group_id | InputInteger  | Point Group ID | `0`     |
| max_neighbors  | InputInteger  | Max Neighbors  | `4`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.InterpolateCurves.type) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.guide_curves`   | `GeometrySocket` | Guide Curves   |
| `i.guide_up`       | `VectorSocket`   | Guide Up       |
| `i.guide_group_id` | `IntegerSocket`  | Guide Group ID |
| `i.points`         | `GeometrySocket` | Points         |
| `i.point_up`       | `VectorSocket`   | Point Up       |
| `i.point_group_id` | `IntegerSocket`  | Point Group ID |
| `i.max_neighbors`  | `IntegerSocket`  | Max Neighbors  |

**Outputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `o.curves`         | `GeometrySocket` | Curves         |
| `o.closest_index`  | `IntegerSocket`  | Closest Index  |
| `o.closest_weight` | `FloatSocket`    | Closest Weight |

### MaterialSelection

``` python
MaterialSelection(material=None)
```

Provide a selection of faces that use the specified material

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| material | InputMaterial | Material    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.MaterialSelection.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MaterialSelection.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MaterialSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MaterialSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MaterialSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MaterialSelection.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MaterialSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MaterialSelection.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.material` | `MaterialSocket` | Material    |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.selection` | `BooleanSocket` | Selection   |

### MergeByDistance

``` python
MergeByDistance(geometry=None, selection=True, mode='All', distance=0.001)
```

Merge vertices or points within a given distance

#### Parameters

| Name      | Type                                       | Description | Default |
|-----------|--------------------------------------------|-------------|---------|
| geometry  | InputGeometry                              | Geometry    | `None`  |
| selection | InputBoolean                               | Selection   | `True`  |
| mode      | InputMenu \| Literal\['All', 'Connected'\] | Mode        | `'All'` |
| distance  | InputFloat                                 | Distance    | `0.001` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.MergeByDistance.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MergeByDistance.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MergeByDistance.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MergeByDistance.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MergeByDistance.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MergeByDistance.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MergeByDistance.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MergeByDistance.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.mode`      | `MenuSocket`     | Mode        |
| `i.distance`  | `FloatSocket`    | Distance    |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### MergeLayers

``` python
MergeLayers(
    grease_pencil=None,
    selection=True,
    group_id=0,
    *,
    mode='MERGE_BY_NAME',
)
```

Join groups of Grease Pencil layers into one

#### Parameters

| Name          | Type          | Description   | Default |
|---------------|---------------|---------------|---------|
| grease_pencil | InputGeometry | Grease Pencil | `None`  |
| selection     | InputBoolean  | Selection     | `True`  |
| group_id      | InputInteger  | Group ID      | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.MergeLayers.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MergeLayers.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.MergeLayers.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MergeLayers.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MergeLayers.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MergeLayers.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MergeLayers.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MergeLayers.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MergeLayers.type) |  |

#### Methods

| Name | Description |
|----|----|
| [by_group_id](#nodebpy.nodes.geometry.geometry.MergeLayers.by_group_id) | Create Merge Layers with operation ‘By Group ID’. Provide a custom group ID for each layer and all layers with the same ID will be merged into one |
| [by_name](#nodebpy.nodes.geometry.geometry.MergeLayers.by_name) | Create Merge Layers with operation ‘By Name’. Combine all layers which have the same name |

##### by_group_id

``` python
by_group_id(grease_pencil=None, selection=True, group_id=0)
```

Create Merge Layers with operation ‘By Group ID’. Provide a custom group ID for each layer and all layers with the same ID will be merged into one

##### by_name

``` python
by_name(grease_pencil=None, selection=True)
```

Create Merge Layers with operation ‘By Name’. Combine all layers which have the same name

**Inputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `i.grease_pencil` | `GeometrySocket` | Grease Pencil |
| `i.selection`     | `BooleanSocket`  | Selection     |
| `i.group_id`      | `IntegerSocket`  | Group ID      |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |

### MeshCircle

``` python
MeshCircle(vertices=32, radius=1.0, *, fill_type='NONE')
```

Generate a circular ring of edges

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| vertices | InputInteger | Vertices    | `32`    |
| radius   | InputFloat   | Radius      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`fill_type`](#nodebpy.nodes.geometry.geometry.MeshCircle.fill_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.MeshCircle.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MeshCircle.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MeshCircle.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MeshCircle.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MeshCircle.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MeshCircle.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MeshCircle.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MeshCircle.type) |  |

#### Methods

| Name | Description |
|----|----|
| [n_gon](#nodebpy.nodes.geometry.geometry.MeshCircle.n_gon) | Create Mesh Circle with operation ‘N-Gon’. |
| [none](#nodebpy.nodes.geometry.geometry.MeshCircle.none) | Create Mesh Circle with operation ‘None’. |
| [triangles](#nodebpy.nodes.geometry.geometry.MeshCircle.triangles) | Create Mesh Circle with operation ‘Triangles’. |

##### n_gon

``` python
n_gon(vertices=32, radius=1.0)
```

Create Mesh Circle with operation ‘N-Gon’.

##### none

``` python
none(vertices=32, radius=1.0)
```

Create Mesh Circle with operation ‘None’.

##### triangles

``` python
triangles(vertices=32, radius=1.0)
```

Create Mesh Circle with operation ‘Triangles’.

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.vertices` | `IntegerSocket` | Vertices    |
| `i.radius`   | `FloatSocket`   | Radius      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### MeshLine

``` python
MeshLine(
    count=10,
    resolution=1.0,
    start_location=None,
    offset=None,
    *,
    mode='OFFSET',
    count_mode='TOTAL',
)
```

Generate vertices in a line and connect them with edges

#### Parameters

| Name           | Type         | Description    | Default |
|----------------|--------------|----------------|---------|
| count          | InputInteger | Count          | `10`    |
| resolution     | InputFloat   | Resolution     | `1.0`   |
| start_location | InputVector  | Start Location | `None`  |
| offset         | InputVector  | Offset         | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`count_mode`](#nodebpy.nodes.geometry.geometry.MeshLine.count_mode) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.MeshLine.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MeshLine.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.MeshLine.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MeshLine.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MeshLine.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MeshLine.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MeshLine.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MeshLine.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MeshLine.type) |  |

#### Methods

| Name | Description |
|----|----|
| [end_points](#nodebpy.nodes.geometry.geometry.MeshLine.end_points) | Create Mesh Line with operation ‘End Points’. Specify the line’s start and end points |
| [offset](#nodebpy.nodes.geometry.geometry.MeshLine.offset) | Create Mesh Line with operation ‘Offset’. Specify the offset from one vertex to the next |

##### end_points

``` python
end_points(count=10, start_location=None, offset=None)
```

Create Mesh Line with operation ‘End Points’. Specify the line’s start and end points

##### offset

``` python
offset(count=10, start_location=None, offset=None)
```

Create Mesh Line with operation ‘Offset’. Specify the offset from one vertex to the next

**Inputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `i.count`          | `IntegerSocket` | Count          |
| `i.resolution`     | `FloatSocket`   | Resolution     |
| `i.start_location` | `VectorSocket`  | Start Location |
| `i.offset`         | `VectorSocket`  | Offset         |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### MeshToCurve

``` python
MeshToCurve(mesh=None, selection=True, *, mode='EDGES')
```

Generate a curve from a mesh

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| mesh      | InputGeometry | Mesh        | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.MeshToCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MeshToCurve.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.MeshToCurve.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MeshToCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MeshToCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MeshToCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MeshToCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MeshToCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MeshToCurve.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edges](#nodebpy.nodes.geometry.geometry.MeshToCurve.edges) | Create Mesh to Curve with operation ‘Edges’. Convert mesh edges to curve segments. Attributes are propagated to curve points. |
| [faces](#nodebpy.nodes.geometry.geometry.MeshToCurve.faces) | Create Mesh to Curve with operation ‘Faces’. Convert each mesh face to a cyclic curve. Face attributes are propagated to curves. |

##### edges

``` python
edges(mesh=None, selection=True)
```

Create Mesh to Curve with operation ‘Edges’. Convert mesh edges to curve segments. Attributes are propagated to curve points.

##### faces

``` python
faces(mesh=None, selection=True)
```

Create Mesh to Curve with operation ‘Faces’. Convert each mesh face to a cyclic curve. Face attributes are propagated to curves.

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.mesh`      | `GeometrySocket` | Mesh        |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### MeshToPoints

``` python
MeshToPoints(
    mesh=None,
    selection=True,
    position=None,
    radius=0.05,
    *,
    mode='VERTICES',
)
```

Generate a point cloud from a mesh’s vertices

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| mesh      | InputGeometry | Mesh        | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| position  | InputVector   | Position    | `None`  |
| radius    | InputFloat    | Radius      | `0.05`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.MeshToPoints.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.MeshToPoints.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.MeshToPoints.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.MeshToPoints.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.MeshToPoints.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.MeshToPoints.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.MeshToPoints.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.MeshToPoints.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.MeshToPoints.type) |  |

#### Methods

| Name | Description |
|----|----|
| [corners](#nodebpy.nodes.geometry.geometry.MeshToPoints.corners) | Create Mesh to Points with operation ‘Corners’. Create a point in the point cloud for each selected face corner |
| [edges](#nodebpy.nodes.geometry.geometry.MeshToPoints.edges) | Create Mesh to Points with operation ‘Edges’. Create a point in the point cloud for each selected edge |
| [faces](#nodebpy.nodes.geometry.geometry.MeshToPoints.faces) | Create Mesh to Points with operation ‘Faces’. Create a point in the point cloud for each selected face |
| [vertices](#nodebpy.nodes.geometry.geometry.MeshToPoints.vertices) | Create Mesh to Points with operation ‘Vertices’. Create a point in the point cloud for each selected vertex |

##### corners

``` python
corners(mesh=None, selection=True, position=None, radius=0.05)
```

Create Mesh to Points with operation ‘Corners’. Create a point in the point cloud for each selected face corner

##### edges

``` python
edges(mesh=None, selection=True, position=None, radius=0.05)
```

Create Mesh to Points with operation ‘Edges’. Create a point in the point cloud for each selected edge

##### faces

``` python
faces(mesh=None, selection=True, position=None, radius=0.05)
```

Create Mesh to Points with operation ‘Faces’. Create a point in the point cloud for each selected face

##### vertices

``` python
vertices(mesh=None, selection=True, position=None, radius=0.05)
```

Create Mesh to Points with operation ‘Vertices’. Create a point in the point cloud for each selected vertex

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.mesh`      | `GeometrySocket` | Mesh        |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.position`  | `VectorSocket`   | Position    |
| `i.radius`    | `FloatSocket`    | Radius      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.points` | `GeometrySocket` | Points      |

### Points

``` python
Points(count=1, position=None, radius=0.1)
```

Generate a point cloud with positions and radii defined by fields

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| count    | InputInteger | Count       | `1`     |
| position | InputVector  | Position    | `None`  |
| radius   | InputFloat   | Radius      | `0.1`   |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Points.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Points.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Points.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Points.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Points.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Points.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Points.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Points.type)       |             |

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.count`    | `IntegerSocket` | Count       |
| `i.position` | `VectorSocket`  | Position    |
| `i.radius`   | `FloatSocket`   | Radius      |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Points      |

### PointsToCurves

``` python
PointsToCurves(points=None, curve_group_id=0, weight=0.0)
```

Split all points to curve by its group ID and reorder by weight

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| points         | InputGeometry | Points         | `None`  |
| curve_group_id | InputInteger  | Curve Group ID | `0`     |
| weight         | InputFloat    | Weight         | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.PointsToCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.PointsToCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.PointsToCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.PointsToCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.PointsToCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.PointsToCurves.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.PointsToCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.PointsToCurves.type) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.points`         | `GeometrySocket` | Points         |
| `i.curve_group_id` | `IntegerSocket`  | Curve Group ID |
| `i.weight`         | `FloatSocket`    | Weight         |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.curves` | `GeometrySocket` | Curves      |

### PointsToVertices

``` python
PointsToVertices(points=None, selection=True)
```

Generate a mesh vertex for each point cloud point

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| points    | InputGeometry | Points      | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.PointsToVertices.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.PointsToVertices.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.PointsToVertices.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.PointsToVertices.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.PointsToVertices.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.PointsToVertices.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.PointsToVertices.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.PointsToVertices.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.points`    | `GeometrySocket` | Points      |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### QuadraticBezier

``` python
QuadraticBezier(resolution=16, start=None, middle=None, end=None)
```

Generate a poly spline in a parabola shape with control points positions

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| resolution | InputInteger | Resolution  | `16`    |
| start      | InputVector  | Start       | `None`  |
| middle     | InputVector  | Middle      | `None`  |
| end        | InputVector  | End         | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.QuadraticBezier.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.resolution` | `IntegerSocket` | Resolution  |
| `i.start`      | `VectorSocket`  | Start       |
| `i.middle`     | `VectorSocket`  | Middle      |
| `i.end`        | `VectorSocket`  | End         |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### Quadrilateral

``` python
Quadrilateral(
    width=2.0,
    height=2.0,
    bottom_width=4.0,
    top_width=2.0,
    offset=1.0,
    bottom_height=3.0,
    top_height=1.0,
    point_1=None,
    point_2=None,
    point_3=None,
    point_4=None,
    *,
    mode='RECTANGLE',
)
```

Generate a polygon with four points

#### Parameters

| Name          | Type        | Description   | Default |
|---------------|-------------|---------------|---------|
| width         | InputFloat  | Width         | `2.0`   |
| height        | InputFloat  | Height        | `2.0`   |
| bottom_width  | InputFloat  | Bottom Width  | `4.0`   |
| top_width     | InputFloat  | Top Width     | `2.0`   |
| offset        | InputFloat  | Offset        | `1.0`   |
| bottom_height | InputFloat  | Bottom Height | `3.0`   |
| top_height    | InputFloat  | Top Height    | `1.0`   |
| point_1       | InputVector | Point 1       | `None`  |
| point_2       | InputVector | Point 2       | `None`  |
| point_3       | InputVector | Point 3       | `None`  |
| point_4       | InputVector | Point 4       | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.Quadrilateral.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Quadrilateral.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.Quadrilateral.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.Quadrilateral.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.Quadrilateral.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.Quadrilateral.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Quadrilateral.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.Quadrilateral.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.Quadrilateral.type) |  |

#### Methods

| Name | Description |
|----|----|
| [kite](#nodebpy.nodes.geometry.geometry.Quadrilateral.kite) | Create Quadrilateral with operation ‘Kite’. Create a Kite / Dart |
| [parallelogram](#nodebpy.nodes.geometry.geometry.Quadrilateral.parallelogram) | Create Quadrilateral with operation ‘Parallelogram’. Create a parallelogram |
| [points](#nodebpy.nodes.geometry.geometry.Quadrilateral.points) | Create Quadrilateral with operation ‘Points’. Create a quadrilateral from four points |
| [rectangle](#nodebpy.nodes.geometry.geometry.Quadrilateral.rectangle) | Create Quadrilateral with operation ‘Rectangle’. Create a rectangle |
| [trapezoid](#nodebpy.nodes.geometry.geometry.Quadrilateral.trapezoid) | Create Quadrilateral with operation ‘Trapezoid’. Create a trapezoid |

##### kite

``` python
kite(width=2.0, bottom_height=3.0, top_height=1.0)
```

Create Quadrilateral with operation ‘Kite’. Create a Kite / Dart

##### parallelogram

``` python
parallelogram(width=2.0, height=2.0, offset=1.0)
```

Create Quadrilateral with operation ‘Parallelogram’. Create a parallelogram

##### points

``` python
points(point_1=None, point_2=None, point_3=None, point_4=None)
```

Create Quadrilateral with operation ‘Points’. Create a quadrilateral from four points

##### rectangle

``` python
rectangle(width=2.0, height=2.0)
```

Create Quadrilateral with operation ‘Rectangle’. Create a rectangle

##### trapezoid

``` python
trapezoid(height=2.0, bottom_width=4.0, top_width=2.0, offset=1.0)
```

Create Quadrilateral with operation ‘Trapezoid’. Create a trapezoid

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.width`         | `FloatSocket`  | Width         |
| `i.height`        | `FloatSocket`  | Height        |
| `i.bottom_width`  | `FloatSocket`  | Bottom Width  |
| `i.top_width`     | `FloatSocket`  | Top Width     |
| `i.offset`        | `FloatSocket`  | Offset        |
| `i.bottom_height` | `FloatSocket`  | Bottom Height |
| `i.top_height`    | `FloatSocket`  | Top Height    |
| `i.point_1`       | `VectorSocket` | Point 1       |
| `i.point_2`       | `VectorSocket` | Point 2       |
| `i.point_3`       | `VectorSocket` | Point 3       |
| `i.point_4`       | `VectorSocket` | Point 4       |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### Raycast

``` python
Raycast(
    target_geometry=None,
    attribute=0.0,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
    *,
    data_type='FLOAT',
)
```

Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| target_geometry | InputGeometry | Target Geometry | `None` |
| attribute | InputFloat | Attribute | `0.0` |
| interpolation | InputMenu \| Literal\['Interpolated', 'Nearest'\] | Interpolation | `'Interpolated'` |
| source_position | InputVector | Source Position | `None` |
| ray_direction | InputVector | Ray Direction | `None` |
| ray_length | InputFloat | Ray Length | `100.0` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.geometry.Raycast.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.Raycast.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Raycast.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.Raycast.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.Raycast.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.Raycast.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Raycast.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.Raycast.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.Raycast.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.Raycast.boolean) | Create Raycast with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.geometry.Raycast.color) | Create Raycast with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.geometry.Raycast.float) | Create Raycast with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.geometry.Raycast.input_4x4_matrix) | Create Raycast with operation ‘4x4 Matrix’. Floating point matrix |
| [integer](#nodebpy.nodes.geometry.geometry.Raycast.integer) | Create Raycast with operation ‘Integer’. 32-bit integer |
| [quaternion](#nodebpy.nodes.geometry.geometry.Raycast.quaternion) | Create Raycast with operation ‘Quaternion’. Floating point quaternion rotation |
| [vector](#nodebpy.nodes.geometry.geometry.Raycast.vector) | Create Raycast with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(
    target_geometry=None,
    attribute=False,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Boolean’. True or false

##### color

``` python
color(
    target_geometry=None,
    attribute=None,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(
    target_geometry=None,
    attribute=0.0,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(
    target_geometry=None,
    attribute=None,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘4x4 Matrix’. Floating point matrix

##### integer

``` python
integer(
    target_geometry=None,
    attribute=0,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Integer’. 32-bit integer

##### quaternion

``` python
quaternion(
    target_geometry=None,
    attribute=None,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Quaternion’. Floating point quaternion rotation

##### vector

``` python
vector(
    target_geometry=None,
    attribute=None,
    interpolation='Interpolated',
    source_position=None,
    ray_direction=None,
    ray_length=100.0,
)
```

Create Raycast with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.target_geometry` | `GeometrySocket` | Target Geometry |
| `i.attribute`       | `FloatSocket`    | Attribute       |
| `i.interpolation`   | `MenuSocket`     | Interpolation   |
| `i.source_position` | `VectorSocket`   | Source Position |
| `i.ray_direction`   | `VectorSocket`   | Ray Direction   |
| `i.ray_length`      | `FloatSocket`    | Ray Length      |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.is_hit`       | `BooleanSocket` | Is Hit       |
| `o.hit_position` | `VectorSocket`  | Hit Position |
| `o.hit_normal`   | `VectorSocket`  | Hit Normal   |
| `o.hit_distance` | `FloatSocket`   | Hit Distance |
| `o.attribute`    | `FloatSocket`   | Attribute    |

### RealizeInstances

``` python
RealizeInstances(geometry=None, selection=True, realize_all=True, depth=0)
```

Convert instances into real geometry data

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| geometry    | InputGeometry | Geometry    | `None`  |
| selection   | InputBoolean  | Selection   | `True`  |
| realize_all | InputBoolean  | Realize All | `True`  |
| depth       | InputInteger  | Depth       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.RealizeInstances.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.RealizeInstances.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.RealizeInstances.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.RealizeInstances.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.RealizeInstances.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.RealizeInstances.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.RealizeInstances.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.RealizeInstances.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.geometry`    | `GeometrySocket` | Geometry    |
| `i.selection`   | `BooleanSocket`  | Selection   |
| `i.realize_all` | `BooleanSocket`  | Realize All |
| `i.depth`       | `IntegerSocket`  | Depth       |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### ReplaceMaterial

``` python
ReplaceMaterial(geometry=None, old=None, new=None)
```

Swap one material with another

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |
| old      | InputMaterial | Old         | `None`  |
| new      | InputMaterial | New         | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ReplaceMaterial.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |
| `i.old`      | `MaterialSocket` | Old         |
| `i.new`      | `MaterialSocket` | New         |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### ResampleCurve

``` python
ResampleCurve(
    curve=None,
    selection=True,
    mode='Count',
    count=10,
    length=0.1,
    *,
    keep_last_segment=False,
)
```

Generate a poly spline for each input spline

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| curve | InputGeometry | Curve | `None` |
| selection | InputBoolean | Selection | `True` |
| mode | InputMenu \| Literal\['Evaluated', 'Count', 'Length'\] | Mode | `'Count'` |
| count | InputInteger | Count | `10` |
| length | InputFloat | Length | `0.1` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ResampleCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ResampleCurve.inputs) |  |
| [`keep_last_segment`](#nodebpy.nodes.geometry.geometry.ResampleCurve.keep_last_segment) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ResampleCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ResampleCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ResampleCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ResampleCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ResampleCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ResampleCurve.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.mode`      | `MenuSocket`     | Mode        |
| `i.count`     | `IntegerSocket`  | Count       |
| `i.length`    | `FloatSocket`    | Length      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### ReverseCurve

``` python
ReverseCurve(curve=None, selection=True)
```

Change the direction of curves by swapping their start and end data

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ReverseCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ReverseCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ReverseCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ReverseCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ReverseCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ReverseCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ReverseCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ReverseCurve.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### RotateInstances

``` python
RotateInstances(
    instances=None,
    selection=True,
    rotation=None,
    pivot_point=None,
    local_space=True,
)
```

Rotate geometry instances in local or global space

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| instances   | InputGeometry | Instances   | `None`  |
| selection   | InputBoolean  | Selection   | `True`  |
| rotation    | InputRotation | Rotation    | `None`  |
| pivot_point | InputVector   | Pivot Point | `None`  |
| local_space | InputBoolean  | Local Space | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.RotateInstances.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.RotateInstances.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.RotateInstances.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.RotateInstances.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.RotateInstances.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.RotateInstances.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.RotateInstances.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.RotateInstances.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.instances`   | `GeometrySocket` | Instances   |
| `i.selection`   | `BooleanSocket`  | Selection   |
| `i.rotation`    | `RotationSocket` | Rotation    |
| `i.pivot_point` | `VectorSocket`   | Pivot Point |
| `i.local_space` | `BooleanSocket`  | Local Space |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### SampleCurve

``` python
SampleCurve(
    curves=None,
    value=0.0,
    factor=0.0,
    length=0.0,
    curve_index=0,
    *,
    mode='FACTOR',
    use_all_curves=False,
    data_type='FLOAT',
)
```

Retrieve data from a point on a curve at a certain distance from its start

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| curves      | InputGeometry | Curves      | `None`  |
| value       | InputFloat    | Value       | `0.0`   |
| factor      | InputFloat    | Factor      | `0.0`   |
| length      | InputFloat    | Length      | `0.0`   |
| curve_index | InputInteger  | Curve Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.geometry.SampleCurve.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SampleCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SampleCurve.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.SampleCurve.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SampleCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SampleCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SampleCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SampleCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SampleCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SampleCurve.type) |  |
| [`use_all_curves`](#nodebpy.nodes.geometry.geometry.SampleCurve.use_all_curves) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.SampleCurve.boolean) | Create Sample Curve with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.geometry.SampleCurve.color) | Create Sample Curve with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [factor](#nodebpy.nodes.geometry.geometry.SampleCurve.factor) | Create Sample Curve with operation ‘Factor’. Find sample positions on the curve using a factor of its total length |
| [float](#nodebpy.nodes.geometry.geometry.SampleCurve.float) | Create Sample Curve with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.geometry.SampleCurve.input_4x4_matrix) | Create Sample Curve with operation ‘4x4 Matrix’. Floating point matrix |
| [integer](#nodebpy.nodes.geometry.geometry.SampleCurve.integer) | Create Sample Curve with operation ‘Integer’. 32-bit integer |
| [length](#nodebpy.nodes.geometry.geometry.SampleCurve.length) | Create Sample Curve with operation ‘Length’. Find sample positions on the curve using a distance from its beginning |
| [quaternion](#nodebpy.nodes.geometry.geometry.SampleCurve.quaternion) | Create Sample Curve with operation ‘Quaternion’. Floating point quaternion rotation |
| [vector](#nodebpy.nodes.geometry.geometry.SampleCurve.vector) | Create Sample Curve with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(curves=None, value=False, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Boolean’. True or false

##### color

``` python
color(curves=None, value=None, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Color’. RGBA color with 32-bit floating-point values

##### factor

``` python
factor(curves=None, value=0.0, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Factor’. Find sample positions on the curve using a factor of its total length

##### float

``` python
float(curves=None, value=0.0, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(curves=None, value=None, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘4x4 Matrix’. Floating point matrix

##### integer

``` python
integer(curves=None, value=0, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Integer’. 32-bit integer

##### length

``` python
length(curves=None, value=0.0, length=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Length’. Find sample positions on the curve using a distance from its beginning

##### quaternion

``` python
quaternion(curves=None, value=None, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Quaternion’. Floating point quaternion rotation

##### vector

``` python
vector(curves=None, value=None, factor=0.0, curve_index=0)
```

Create Sample Curve with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.curves`      | `GeometrySocket` | Curves      |
| `i.value`       | `FloatSocket`    | Value       |
| `i.factor`      | `FloatSocket`    | Factor      |
| `i.length`      | `FloatSocket`    | Length      |
| `i.curve_index` | `IntegerSocket`  | Curve Index |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.value`    | `FloatSocket`  | Value       |
| `o.position` | `VectorSocket` | Position    |
| `o.tangent`  | `VectorSocket` | Tangent     |
| `o.normal`   | `VectorSocket` | Normal      |

### SampleIndex

``` python
SampleIndex(
    geometry=None,
    value=0.0,
    index=0,
    *,
    data_type='FLOAT',
    domain='POINT',
    clamp=False,
)
```

Retrieve values from specific geometry elements

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |
| value    | InputFloat    | Value       | `0.0`   |
| index    | InputInteger  | Index       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`clamp`](#nodebpy.nodes.geometry.geometry.SampleIndex.clamp) |  |
| [`data_type`](#nodebpy.nodes.geometry.geometry.SampleIndex.data_type) |  |
| [`domain`](#nodebpy.nodes.geometry.geometry.SampleIndex.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SampleIndex.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SampleIndex.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SampleIndex.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SampleIndex.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SampleIndex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SampleIndex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SampleIndex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SampleIndex.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.SampleIndex.boolean) | Create Sample Index with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.geometry.SampleIndex.color) | Create Sample Index with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [edge](#nodebpy.nodes.geometry.geometry.SampleIndex.edge) | Create Sample Index with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SampleIndex.face) | Create Sample Index with operation ‘Face’. Attribute on mesh faces |
| [face_corner](#nodebpy.nodes.geometry.geometry.SampleIndex.face_corner) | Create Sample Index with operation ‘Face Corner’. Attribute on mesh face corner |
| [float](#nodebpy.nodes.geometry.geometry.SampleIndex.float) | Create Sample Index with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.geometry.SampleIndex.input_4x4_matrix) | Create Sample Index with operation ‘4x4 Matrix’. Floating point matrix |
| [instance](#nodebpy.nodes.geometry.geometry.SampleIndex.instance) | Create Sample Index with operation ‘Instance’. Attribute on instance |
| [integer](#nodebpy.nodes.geometry.geometry.SampleIndex.integer) | Create Sample Index with operation ‘Integer’. 32-bit integer |
| [layer](#nodebpy.nodes.geometry.geometry.SampleIndex.layer) | Create Sample Index with operation ‘Layer’. Attribute on Grease Pencil layer |
| [point](#nodebpy.nodes.geometry.geometry.SampleIndex.point) | Create Sample Index with operation ‘Point’. Attribute on point |
| [quaternion](#nodebpy.nodes.geometry.geometry.SampleIndex.quaternion) | Create Sample Index with operation ‘Quaternion’. Floating point quaternion rotation |
| [spline](#nodebpy.nodes.geometry.geometry.SampleIndex.spline) | Create Sample Index with operation ‘Spline’. Attribute on spline |
| [vector](#nodebpy.nodes.geometry.geometry.SampleIndex.vector) | Create Sample Index with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(geometry=None, value=False, index=0)
```

Create Sample Index with operation ‘Boolean’. True or false

##### color

``` python
color(geometry=None, value=None, index=0)
```

Create Sample Index with operation ‘Color’. RGBA color with 32-bit floating-point values

##### edge

``` python
edge(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Face’. Attribute on mesh faces

##### face_corner

``` python
face_corner(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Face Corner’. Attribute on mesh face corner

##### float

``` python
float(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(geometry=None, value=None, index=0)
```

Create Sample Index with operation ‘4x4 Matrix’. Floating point matrix

##### instance

``` python
instance(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Instance’. Attribute on instance

##### integer

``` python
integer(geometry=None, value=0, index=0)
```

Create Sample Index with operation ‘Integer’. 32-bit integer

##### layer

``` python
layer(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Layer’. Attribute on Grease Pencil layer

##### point

``` python
point(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Point’. Attribute on point

##### quaternion

``` python
quaternion(geometry=None, value=None, index=0)
```

Create Sample Index with operation ‘Quaternion’. Floating point quaternion rotation

##### spline

``` python
spline(geometry=None, value=0.0, index=0)
```

Create Sample Index with operation ‘Spline’. Attribute on spline

##### vector

``` python
vector(geometry=None, value=None, index=0)
```

Create Sample Index with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |
| `i.value`    | `FloatSocket`    | Value       |
| `i.index`    | `IntegerSocket`  | Index       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### SampleNearest

``` python
SampleNearest(geometry=None, sample_position=None, *, domain='POINT')
```

Find the element of a geometry closest to a position. Similar to the “Index of Nearest” node

#### Parameters

| Name            | Type          | Description     | Default |
|-----------------|---------------|-----------------|---------|
| geometry        | InputGeometry | Geometry        | `None`  |
| sample_position | InputVector   | Sample Position | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SampleNearest.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SampleNearest.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SampleNearest.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SampleNearest.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SampleNearest.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SampleNearest.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SampleNearest.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SampleNearest.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SampleNearest.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.SampleNearest.edge) | Create Sample Nearest with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SampleNearest.face) | Create Sample Nearest with operation ‘Face’. Attribute on mesh faces |
| [face_corner](#nodebpy.nodes.geometry.geometry.SampleNearest.face_corner) | Create Sample Nearest with operation ‘Face Corner’. Attribute on mesh face corner |
| [point](#nodebpy.nodes.geometry.geometry.SampleNearest.point) | Create Sample Nearest with operation ‘Point’. Attribute on point |

##### edge

``` python
edge(geometry=None, sample_position=None)
```

Create Sample Nearest with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, sample_position=None)
```

Create Sample Nearest with operation ‘Face’. Attribute on mesh faces

##### face_corner

``` python
face_corner(geometry=None, sample_position=None)
```

Create Sample Nearest with operation ‘Face Corner’. Attribute on mesh face corner

##### point

``` python
point(geometry=None, sample_position=None)
```

Create Sample Nearest with operation ‘Point’. Attribute on point

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.geometry`        | `GeometrySocket` | Geometry        |
| `i.sample_position` | `VectorSocket`   | Sample Position |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.index` | `IntegerSocket` | Index       |

### SampleNearestSurface

``` python
SampleNearestSurface(
    mesh=None,
    value=0.0,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
    *,
    data_type='FLOAT',
)
```

Calculate the interpolated value of a mesh attribute on the closest point of its surface

#### Parameters

| Name            | Type          | Description     | Default |
|-----------------|---------------|-----------------|---------|
| mesh            | InputGeometry | Mesh            | `None`  |
| value           | InputFloat    | Value           | `0.0`   |
| group_id        | InputInteger  | Group ID        | `0`     |
| sample_position | InputVector   | Sample Position | `None`  |
| sample_group_id | InputInteger  | Sample Group ID | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.boolean) | Create Sample Nearest Surface with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.color) | Create Sample Nearest Surface with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.float) | Create Sample Nearest Surface with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.input_4x4_matrix) | Create Sample Nearest Surface with operation ‘4x4 Matrix’. Floating point matrix |
| [integer](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.integer) | Create Sample Nearest Surface with operation ‘Integer’. 32-bit integer |
| [quaternion](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.quaternion) | Create Sample Nearest Surface with operation ‘Quaternion’. Floating point quaternion rotation |
| [vector](#nodebpy.nodes.geometry.geometry.SampleNearestSurface.vector) | Create Sample Nearest Surface with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(
    mesh=None,
    value=False,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
)
```

Create Sample Nearest Surface with operation ‘Boolean’. True or false

##### color

``` python
color(
    mesh=None,
    value=None,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
)
```

Create Sample Nearest Surface with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(mesh=None, value=0.0, group_id=0, sample_position=None, sample_group_id=0)
```

Create Sample Nearest Surface with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(
    mesh=None,
    value=None,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
)
```

Create Sample Nearest Surface with operation ‘4x4 Matrix’. Floating point matrix

##### integer

``` python
integer(mesh=None, value=0, group_id=0, sample_position=None, sample_group_id=0)
```

Create Sample Nearest Surface with operation ‘Integer’. 32-bit integer

##### quaternion

``` python
quaternion(
    mesh=None,
    value=None,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
)
```

Create Sample Nearest Surface with operation ‘Quaternion’. Floating point quaternion rotation

##### vector

``` python
vector(
    mesh=None,
    value=None,
    group_id=0,
    sample_position=None,
    sample_group_id=0,
)
```

Create Sample Nearest Surface with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.mesh`            | `GeometrySocket` | Mesh            |
| `i.value`           | `FloatSocket`    | Value           |
| `i.group_id`        | `IntegerSocket`  | Group ID        |
| `i.sample_position` | `VectorSocket`   | Sample Position |
| `i.sample_group_id` | `IntegerSocket`  | Sample Group ID |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.value`    | `FloatSocket`   | Value       |
| `o.is_valid` | `BooleanSocket` | Is Valid    |

### SampleUVSurface

``` python
SampleUVSurface(
    mesh=None,
    value=0.0,
    source_uv_map=None,
    sample_uv=None,
    *,
    data_type='FLOAT',
)
```

Calculate the interpolated values of a mesh attribute at a UV coordinate

#### Parameters

| Name          | Type          | Description | Default |
|---------------|---------------|-------------|---------|
| mesh          | InputGeometry | Mesh        | `None`  |
| value         | InputFloat    | Value       | `0.0`   |
| source_uv_map | InputVector   | UV Map      | `None`  |
| sample_uv     | InputVector   | Sample UV   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SampleUVSurface.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.SampleUVSurface.boolean) | Create Sample UV Surface with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.geometry.SampleUVSurface.color) | Create Sample UV Surface with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.geometry.SampleUVSurface.float) | Create Sample UV Surface with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.geometry.SampleUVSurface.input_4x4_matrix) | Create Sample UV Surface with operation ‘4x4 Matrix’. Floating point matrix |
| [integer](#nodebpy.nodes.geometry.geometry.SampleUVSurface.integer) | Create Sample UV Surface with operation ‘Integer’. 32-bit integer |
| [quaternion](#nodebpy.nodes.geometry.geometry.SampleUVSurface.quaternion) | Create Sample UV Surface with operation ‘Quaternion’. Floating point quaternion rotation |
| [vector](#nodebpy.nodes.geometry.geometry.SampleUVSurface.vector) | Create Sample UV Surface with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(mesh=None, value=False, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Boolean’. True or false

##### color

``` python
color(mesh=None, value=None, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(mesh=None, value=0.0, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(mesh=None, value=None, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘4x4 Matrix’. Floating point matrix

##### integer

``` python
integer(mesh=None, value=0, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Integer’. 32-bit integer

##### quaternion

``` python
quaternion(mesh=None, value=None, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Quaternion’. Floating point quaternion rotation

##### vector

``` python
vector(mesh=None, value=None, source_uv_map=None, sample_uv=None)
```

Create Sample UV Surface with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute         | Type             | Description |
|-------------------|------------------|-------------|
| `i.mesh`          | `GeometrySocket` | Mesh        |
| `i.value`         | `FloatSocket`    | Value       |
| `i.source_uv_map` | `VectorSocket`   | UV Map      |
| `i.sample_uv`     | `VectorSocket`   | Sample UV   |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.value`    | `FloatSocket`   | Value       |
| `o.is_valid` | `BooleanSocket` | Is Valid    |

### ScaleElements

``` python
ScaleElements(
    geometry=None,
    selection=True,
    scale=1.0,
    center=None,
    scale_mode='Uniform',
    axis=None,
    *,
    domain='FACE',
)
```

Scale groups of connected edges and faces

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| geometry | InputGeometry | Geometry | `None` |
| selection | InputBoolean | Selection | `True` |
| scale | InputFloat | Scale | `1.0` |
| center | InputVector | Center | `None` |
| scale_mode | InputMenu \| Literal\['Uniform', 'Single Axis'\] | Scale Mode | `'Uniform'` |
| axis | InputVector | Axis | `None` |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.ScaleElements.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.ScaleElements.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ScaleElements.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ScaleElements.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ScaleElements.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ScaleElements.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ScaleElements.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ScaleElements.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ScaleElements.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.ScaleElements.edge) | Create Scale Elements with operation ‘Edge’. Scale individual edges or neighboring edge islands |
| [face](#nodebpy.nodes.geometry.geometry.ScaleElements.face) | Create Scale Elements with operation ‘Face’. Scale individual faces or neighboring face islands |

##### edge

``` python
edge(
    geometry=None,
    selection=True,
    scale=1.0,
    center=None,
    scale_mode='Uniform',
)
```

Create Scale Elements with operation ‘Edge’. Scale individual edges or neighboring edge islands

##### face

``` python
face(
    geometry=None,
    selection=True,
    scale=1.0,
    center=None,
    scale_mode='Uniform',
)
```

Create Scale Elements with operation ‘Face’. Scale individual faces or neighboring face islands

**Inputs**

| Attribute      | Type             | Description |
|----------------|------------------|-------------|
| `i.geometry`   | `GeometrySocket` | Geometry    |
| `i.selection`  | `BooleanSocket`  | Selection   |
| `i.scale`      | `FloatSocket`    | Scale       |
| `i.center`     | `VectorSocket`   | Center      |
| `i.scale_mode` | `MenuSocket`     | Scale Mode  |
| `i.axis`       | `VectorSocket`   | Axis        |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### ScaleInstances

``` python
ScaleInstances(
    instances=None,
    selection=True,
    scale=None,
    center=None,
    local_space=True,
)
```

Scale geometry instances in local or global space

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| instances   | InputGeometry | Instances   | `None`  |
| selection   | InputBoolean  | Selection   | `True`  |
| scale       | InputVector   | Scale       | `None`  |
| center      | InputVector   | Center      | `None`  |
| local_space | InputBoolean  | Local Space | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.ScaleInstances.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.ScaleInstances.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.ScaleInstances.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.ScaleInstances.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.ScaleInstances.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.ScaleInstances.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.ScaleInstances.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.ScaleInstances.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.instances`   | `GeometrySocket` | Instances   |
| `i.selection`   | `BooleanSocket`  | Selection   |
| `i.scale`       | `VectorSocket`   | Scale       |
| `i.center`      | `VectorSocket`   | Center      |
| `i.local_space` | `BooleanSocket`  | Local Space |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### SeparateComponents

``` python
SeparateComponents(geometry=None)
```

Split a geometry into a separate output for each type of data in the geometry

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SeparateComponents.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SeparateComponents.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SeparateComponents.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SeparateComponents.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SeparateComponents.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SeparateComponents.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SeparateComponents.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SeparateComponents.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.mesh`          | `GeometrySocket` | Mesh          |
| `o.curve`         | `GeometrySocket` | Curve         |
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |
| `o.point_cloud`   | `GeometrySocket` | Point Cloud   |
| `o.volume`        | `GeometrySocket` | Volume        |
| `o.instances`     | `GeometrySocket` | Instances     |

### SeparateGeometry

``` python
SeparateGeometry(geometry=None, selection=True, *, domain='POINT')
```

Split a geometry into two geometry outputs based on a selection

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SeparateGeometry.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.SeparateGeometry.edge) | Create Separate Geometry with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SeparateGeometry.face) | Create Separate Geometry with operation ‘Face’. Attribute on mesh faces |
| [instance](#nodebpy.nodes.geometry.geometry.SeparateGeometry.instance) | Create Separate Geometry with operation ‘Instance’. Attribute on instance |
| [layer](#nodebpy.nodes.geometry.geometry.SeparateGeometry.layer) | Create Separate Geometry with operation ‘Layer’. Attribute on Grease Pencil layer |
| [point](#nodebpy.nodes.geometry.geometry.SeparateGeometry.point) | Create Separate Geometry with operation ‘Point’. Attribute on point |
| [spline](#nodebpy.nodes.geometry.geometry.SeparateGeometry.spline) | Create Separate Geometry with operation ‘Spline’. Attribute on spline |

##### edge

``` python
edge(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Face’. Attribute on mesh faces

##### instance

``` python
instance(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Instance’. Attribute on instance

##### layer

``` python
layer(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Layer’. Attribute on Grease Pencil layer

##### point

``` python
point(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Point’. Attribute on point

##### spline

``` python
spline(geometry=None, selection=True)
```

Create Separate Geometry with operation ‘Spline’. Attribute on spline

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.selection` | `GeometrySocket` | Selection   |
| `o.inverted`  | `GeometrySocket` | Inverted    |

### SetCurveNormal

``` python
SetCurveNormal(curve=None, selection=True, mode='Minimum Twist', normal=None)
```

Set the evaluation mode for curve normals

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| curve | InputGeometry | Curve | `None` |
| selection | InputBoolean | Selection | `True` |
| mode | InputMenu \| Literal\['Minimum Twist', 'Z Up', 'Free'\] | Mode | `'Minimum Twist'` |
| normal | InputVector | Normal | `None` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetCurveNormal.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.mode`      | `MenuSocket`     | Mode        |
| `i.normal`    | `VectorSocket`   | Normal      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SetCurveRadius

``` python
SetCurveRadius(curve=None, selection=True, radius=0.005)
```

Set the radius of the curve at each control point

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| radius    | InputFloat    | Radius      | `0.005` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetCurveRadius.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.radius`    | `FloatSocket`    | Radius      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SetCurveTilt

``` python
SetCurveTilt(curve=None, selection=True, tilt=0.0)
```

Set the tilt angle at each curve control point

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| tilt      | InputFloat    | Tilt        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetCurveTilt.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.tilt`      | `FloatSocket`    | Tilt        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SetFaceSet

``` python
SetFaceSet(mesh=None, selection=True, face_set=0)
```

Set sculpt face set values for faces

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| mesh      | InputGeometry | Mesh        | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| face_set  | InputInteger  | Face Set    | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetFaceSet.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetFaceSet.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetFaceSet.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetFaceSet.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetFaceSet.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetFaceSet.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetFaceSet.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetFaceSet.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.mesh`      | `GeometrySocket` | Mesh        |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.face_set`  | `IntegerSocket`  | Face Set    |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### SetGeometryName

``` python
SetGeometryName(geometry=None, name='')
```

Set the name of a geometry for easier debugging

#### Parameters

| Name     | Type          | Description | Default |
|----------|---------------|-------------|---------|
| geometry | InputGeometry | Geometry    | `None`  |
| name     | InputString   | Name        | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetGeometryName.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetGeometryName.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetGeometryName.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetGeometryName.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetGeometryName.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetGeometryName.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetGeometryName.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetGeometryName.type) |  |

**Inputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `i.geometry` | `GeometrySocket` | Geometry    |
| `i.name`     | `StringSocket`   | Name        |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetGreasePencilColor

``` python
SetGreasePencilColor(
    grease_pencil=None,
    selection=True,
    color=None,
    opacity=1.0,
    *,
    mode='STROKE',
)
```

Set color and opacity attributes on Grease Pencil geometry

#### Parameters

| Name          | Type          | Description   | Default |
|---------------|---------------|---------------|---------|
| grease_pencil | InputGeometry | Grease Pencil | `None`  |
| selection     | InputBoolean  | Selection     | `True`  |
| color         | InputColor    | Color         | `None`  |
| opacity       | InputFloat    | Opacity       | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.type) |  |

#### Methods

| Name | Description |
|----|----|
| [fill](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.fill) | Create Set Grease Pencil Color with operation ‘Fill’. Set the color and opacity for the stroke fills |
| [stroke](#nodebpy.nodes.geometry.geometry.SetGreasePencilColor.stroke) | Create Set Grease Pencil Color with operation ‘Stroke’. Set the color and opacity for the points of the stroke |

##### fill

``` python
fill(grease_pencil=None, selection=True, color=None, opacity=1.0)
```

Create Set Grease Pencil Color with operation ‘Fill’. Set the color and opacity for the stroke fills

##### stroke

``` python
stroke(grease_pencil=None, selection=True, color=None, opacity=1.0)
```

Create Set Grease Pencil Color with operation ‘Stroke’. Set the color and opacity for the points of the stroke

**Inputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `i.grease_pencil` | `GeometrySocket` | Grease Pencil |
| `i.selection`     | `BooleanSocket`  | Selection     |
| `i.color`         | `ColorSocket`    | Color         |
| `i.opacity`       | `FloatSocket`    | Opacity       |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |

### SetGreasePencilDepth

``` python
SetGreasePencilDepth(grease_pencil=None, *, depth_order='2D')
```

Set the Grease Pencil depth order to use

#### Parameters

| Name          | Type          | Description   | Default |
|---------------|---------------|---------------|---------|
| grease_pencil | InputGeometry | Grease Pencil | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`depth_order`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.depth_order) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetGreasePencilDepth.type) |  |

**Inputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `i.grease_pencil` | `GeometrySocket` | Grease Pencil |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |

### SetGreasePencilSoftness

``` python
SetGreasePencilSoftness(grease_pencil=None, selection=True, softness=0.0)
```

Set softness attribute on Grease Pencil geometry

#### Parameters

| Name          | Type          | Description   | Default |
|---------------|---------------|---------------|---------|
| grease_pencil | InputGeometry | Grease Pencil | `None`  |
| selection     | InputBoolean  | Selection     | `True`  |
| softness      | InputFloat    | Softness      | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetGreasePencilSoftness.type) |  |

**Inputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `i.grease_pencil` | `GeometrySocket` | Grease Pencil |
| `i.selection`     | `BooleanSocket`  | Selection     |
| `i.softness`      | `FloatSocket`    | Softness      |

**Outputs**

| Attribute         | Type             | Description   |
|-------------------|------------------|---------------|
| `o.grease_pencil` | `GeometrySocket` | Grease Pencil |

### SetHandlePositions

``` python
SetHandlePositions(
    curve=None,
    selection=True,
    position=None,
    offset=None,
    *,
    mode='LEFT',
)
```

Set the positions for the handles of Bézier curves

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| position  | InputVector   | Position    | `None`  |
| offset    | InputVector   | Offset      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetHandlePositions.type) |  |

#### Methods

| Name | Description |
|----|----|
| [left](#nodebpy.nodes.geometry.geometry.SetHandlePositions.left) | Create Set Handle Positions with operation ‘Left’. Use the left handles |
| [right](#nodebpy.nodes.geometry.geometry.SetHandlePositions.right) | Create Set Handle Positions with operation ‘Right’. Use the right handles |

##### left

``` python
left(curve=None, selection=True, position=None, offset=None)
```

Create Set Handle Positions with operation ‘Left’. Use the left handles

##### right

``` python
right(curve=None, selection=True, position=None, offset=None)
```

Create Set Handle Positions with operation ‘Right’. Use the right handles

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.position`  | `VectorSocket`   | Position    |
| `i.offset`    | `VectorSocket`   | Offset      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SetID

``` python
SetID(geometry=None, selection=True, id=0)
```

Set the id attribute on the input geometry, mainly used internally for randomizing

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| id        | InputInteger  | ID          | `0`     |

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.SetID.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetID.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.SetID.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.SetID.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.SetID.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetID.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetID.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.SetID.type)       |             |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.id`        | `IntegerSocket`  | ID          |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetInstanceTransform

``` python
SetInstanceTransform(instances=None, selection=True, transform=None)
```

Set the transformation matrix of every instance

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| instances | InputGeometry | Instances   | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| transform | InputMatrix   | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetInstanceTransform.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.instances` | `GeometrySocket` | Instances   |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.transform` | `MatrixSocket`   | Transform   |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### SetMaterial

``` python
SetMaterial(geometry=None, selection=True, material=None)
```

Assign a material to geometry elements

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| material  | InputMaterial | Material    | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetMaterial.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetMaterial.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetMaterial.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetMaterial.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetMaterial.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetMaterial.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetMaterial.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetMaterial.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.material`  | `MaterialSocket` | Material    |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetMaterialIndex

``` python
SetMaterialIndex(geometry=None, selection=True, material_index=0)
```

Set the material index for each selected geometry element

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| geometry       | InputGeometry | Geometry       | `None`  |
| selection      | InputBoolean  | Selection      | `True`  |
| material_index | InputInteger  | Material Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetMaterialIndex.type) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.geometry`       | `GeometrySocket` | Geometry       |
| `i.selection`      | `BooleanSocket`  | Selection      |
| `i.material_index` | `IntegerSocket`  | Material Index |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetMeshNormal

``` python
SetMeshNormal(
    mesh=None,
    remove_custom=True,
    edge_sharpness=False,
    face_sharpness=False,
    custom_normal=None,
    *,
    mode='SHARPNESS',
    domain='POINT',
)
```

Store a normal vector for each mesh element

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| mesh           | InputGeometry | Mesh           | `None`  |
| remove_custom  | InputBoolean  | Remove Custom  | `True`  |
| edge_sharpness | InputBoolean  | Edge Sharpness | `False` |
| face_sharpness | InputBoolean  | Face Sharpness | `False` |
| custom_normal  | InputVector   | Custom Normal  | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetMeshNormal.type) |  |

#### Methods

| Name | Description |
|----|----|
| [face](#nodebpy.nodes.geometry.geometry.SetMeshNormal.face) | Create Set Mesh Normal with operation ‘Face’. Attribute on mesh faces |
| [face_corner](#nodebpy.nodes.geometry.geometry.SetMeshNormal.face_corner) | Create Set Mesh Normal with operation ‘Face Corner’. Attribute on mesh face corner |
| [free](#nodebpy.nodes.geometry.geometry.SetMeshNormal.free) | Create Set Mesh Normal with operation ‘Free’. Store custom normals as simple vectors in the local space of the mesh. Values are not necessarily updated automatically later on as the mesh is deformed. |
| [point](#nodebpy.nodes.geometry.geometry.SetMeshNormal.point) | Create Set Mesh Normal with operation ‘Point’. Attribute on point |
| [sharpness](#nodebpy.nodes.geometry.geometry.SetMeshNormal.sharpness) | Create Set Mesh Normal with operation ‘Sharpness’. Store the sharpness of each face or edge. Similar to the “Shade Smooth” and “Shade Flat” operators. |
| [tangent_space](#nodebpy.nodes.geometry.geometry.SetMeshNormal.tangent_space) | Create Set Mesh Normal with operation ‘Tangent Space’. Store normals in a deformation dependent custom transformation space. This method is slower, but can be better when subsequent operations change the mesh without handling normals specifically. |

##### face

``` python
face(mesh=None, remove_custom=True, edge_sharpness=False, face_sharpness=False)
```

Create Set Mesh Normal with operation ‘Face’. Attribute on mesh faces

##### face_corner

``` python
face_corner(
    mesh=None,
    remove_custom=True,
    edge_sharpness=False,
    face_sharpness=False,
)
```

Create Set Mesh Normal with operation ‘Face Corner’. Attribute on mesh face corner

##### free

``` python
free(mesh=None, custom_normal=None)
```

Create Set Mesh Normal with operation ‘Free’. Store custom normals as simple vectors in the local space of the mesh. Values are not necessarily updated automatically later on as the mesh is deformed.

##### point

``` python
point(mesh=None, remove_custom=True, edge_sharpness=False, face_sharpness=False)
```

Create Set Mesh Normal with operation ‘Point’. Attribute on point

##### sharpness

``` python
sharpness(
    mesh=None,
    remove_custom=True,
    edge_sharpness=False,
    face_sharpness=False,
)
```

Create Set Mesh Normal with operation ‘Sharpness’. Store the sharpness of each face or edge. Similar to the “Shade Smooth” and “Shade Flat” operators.

##### tangent_space

``` python
tangent_space(mesh=None, custom_normal=None)
```

Create Set Mesh Normal with operation ‘Tangent Space’. Store normals in a deformation dependent custom transformation space. This method is slower, but can be better when subsequent operations change the mesh without handling normals specifically.

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.mesh`           | `GeometrySocket` | Mesh           |
| `i.remove_custom`  | `BooleanSocket`  | Remove Custom  |
| `i.edge_sharpness` | `BooleanSocket`  | Edge Sharpness |
| `i.face_sharpness` | `BooleanSocket`  | Face Sharpness |
| `i.custom_normal`  | `VectorSocket`   | Custom Normal  |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### SetPointRadius

``` python
SetPointRadius(points=None, selection=True, radius=0.05)
```

Set the display size of point cloud points

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| points    | InputGeometry | Points      | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| radius    | InputFloat    | Radius      | `0.05`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetPointRadius.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetPointRadius.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetPointRadius.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetPointRadius.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetPointRadius.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetPointRadius.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetPointRadius.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetPointRadius.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.points`    | `GeometrySocket` | Points      |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.radius`    | `FloatSocket`    | Radius      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.points` | `GeometrySocket` | Points      |

### SetPosition

``` python
SetPosition(geometry=None, selection=True, position=None, offset=None)
```

Set the location of each point

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| position  | InputVector   | Position    | `None`  |
| offset    | InputVector   | Offset      | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetPosition.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetPosition.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetPosition.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetPosition.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetPosition.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetPosition.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetPosition.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetPosition.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.position`  | `VectorSocket`   | Position    |
| `i.offset`    | `VectorSocket`   | Offset      |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetSelection

``` python
SetSelection(
    geometry=None,
    selection=True,
    *,
    domain='POINT',
    selection_type='BOOLEAN',
)
```

Set selection of the edited geometry, for tool execution

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SetSelection.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SetSelection.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetSelection.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetSelection.outputs) |  |
| [`selection_type`](#nodebpy.nodes.geometry.geometry.SetSelection.selection_type) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetSelection.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.geometry.SetSelection.boolean) | Create Set Selection with operation ‘Boolean’. Store true or false selection values in edit mode |
| [edge](#nodebpy.nodes.geometry.geometry.SetSelection.edge) | Create Set Selection with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SetSelection.face) | Create Set Selection with operation ‘Face’. Attribute on mesh faces |
| [float](#nodebpy.nodes.geometry.geometry.SetSelection.float) | Create Set Selection with operation ‘Float’. Store floating point selection values. For mesh geometry, stored inverted as the sculpt mode mask |
| [point](#nodebpy.nodes.geometry.geometry.SetSelection.point) | Create Set Selection with operation ‘Point’. Attribute on point |
| [spline](#nodebpy.nodes.geometry.geometry.SetSelection.spline) | Create Set Selection with operation ‘Spline’. Attribute on spline |

##### boolean

``` python
boolean(geometry=None, selection=True)
```

Create Set Selection with operation ‘Boolean’. Store true or false selection values in edit mode

##### edge

``` python
edge(geometry=None, selection=True)
```

Create Set Selection with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True)
```

Create Set Selection with operation ‘Face’. Attribute on mesh faces

##### float

``` python
float(geometry=None, selection=1.0)
```

Create Set Selection with operation ‘Float’. Store floating point selection values. For mesh geometry, stored inverted as the sculpt mode mask

##### point

``` python
point(geometry=None, selection=True)
```

Create Set Selection with operation ‘Point’. Attribute on point

##### spline

``` python
spline(geometry=None, selection=True)
```

Create Set Selection with operation ‘Spline’. Attribute on spline

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### SetShadeSmooth

``` python
SetShadeSmooth(
    geometry=None,
    selection=True,
    shade_smooth=True,
    *,
    domain='FACE',
)
```

Control the smoothness of mesh normals around each face by changing the “shade smooth” attribute

#### Parameters

| Name         | Type          | Description  | Default |
|--------------|---------------|--------------|---------|
| geometry     | InputGeometry | Mesh         | `None`  |
| selection    | InputBoolean  | Selection    | `True`  |
| shade_smooth | InputBoolean  | Shade Smooth | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.edge) | Create Set Shade Smooth with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SetShadeSmooth.face) | Create Set Shade Smooth with operation ‘Face’. Attribute on mesh faces |

##### edge

``` python
edge(geometry=None, selection=True, shade_smooth=True)
```

Create Set Shade Smooth with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True, shade_smooth=True)
```

Create Set Shade Smooth with operation ‘Face’. Attribute on mesh faces

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.geometry`     | `GeometrySocket` | Mesh         |
| `i.selection`    | `BooleanSocket`  | Selection    |
| `i.shade_smooth` | `BooleanSocket`  | Shade Smooth |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Mesh        |

### SetSplineCyclic

``` python
SetSplineCyclic(geometry=None, selection=True, cyclic=False)
```

Control whether each spline loops back on itself by changing the “cyclic” attribute

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| cyclic    | InputBoolean  | Cyclic      | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetSplineCyclic.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.cyclic`    | `BooleanSocket`  | Cyclic      |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Curve       |

### SetSplineResolution

``` python
SetSplineResolution(geometry=None, selection=True, resolution=12)
```

Control how many evaluated points should be generated on every curve segment

#### Parameters

| Name       | Type          | Description | Default |
|------------|---------------|-------------|---------|
| geometry   | InputGeometry | Curve       | `None`  |
| selection  | InputBoolean  | Selection   | `True`  |
| resolution | InputInteger  | Resolution  | `12`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetSplineResolution.type) |  |

**Inputs**

| Attribute      | Type             | Description |
|----------------|------------------|-------------|
| `i.geometry`   | `GeometrySocket` | Curve       |
| `i.selection`  | `BooleanSocket`  | Selection   |
| `i.resolution` | `IntegerSocket`  | Resolution  |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Curve       |

### SetSplineType

``` python
SetSplineType(curve=None, selection=True, *, spline_type='POLY')
```

Change the type of curves

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SetSplineType.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SetSplineType.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SetSplineType.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SetSplineType.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SetSplineType.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SetSplineType.outputs) |  |
| [`spline_type`](#nodebpy.nodes.geometry.geometry.SetSplineType.spline_type) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SetSplineType.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SetSplineType.type) |  |

#### Methods

| Name | Description |
|----|----|
| [bézier](#nodebpy.nodes.geometry.geometry.SetSplineType.bézier) | Create Set Spline Type with operation ‘Bézier’. |
| [catmull_rom](#nodebpy.nodes.geometry.geometry.SetSplineType.catmull_rom) | Create Set Spline Type with operation ‘Catmull Rom’. |
| [nurbs](#nodebpy.nodes.geometry.geometry.SetSplineType.nurbs) | Create Set Spline Type with operation ‘NURBS’. |
| [poly](#nodebpy.nodes.geometry.geometry.SetSplineType.poly) | Create Set Spline Type with operation ‘Poly’. |

##### bézier

``` python
bézier(curve=None, selection=True)
```

Create Set Spline Type with operation ‘Bézier’.

##### catmull_rom

``` python
catmull_rom(curve=None, selection=True)
```

Create Set Spline Type with operation ‘Catmull Rom’.

##### nurbs

``` python
nurbs(curve=None, selection=True)
```

Create Set Spline Type with operation ‘NURBS’.

##### poly

``` python
poly(curve=None, selection=True)
```

Create Set Spline Type with operation ‘Poly’.

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SortElements

``` python
SortElements(
    geometry=None,
    selection=True,
    group_id=0,
    sort_weight=0.0,
    *,
    domain='POINT',
)
```

Rearrange geometry elements, changing their indices

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| geometry    | InputGeometry | Geometry    | `None`  |
| selection   | InputBoolean  | Selection   | `True`  |
| group_id    | InputInteger  | Group ID    | `0`     |
| sort_weight | InputFloat    | Sort Weight | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SortElements.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SortElements.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SortElements.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SortElements.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SortElements.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SortElements.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SortElements.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SortElements.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SortElements.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.SortElements.edge) | Create Sort Elements with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SortElements.face) | Create Sort Elements with operation ‘Face’. Attribute on mesh faces |
| [instance](#nodebpy.nodes.geometry.geometry.SortElements.instance) | Create Sort Elements with operation ‘Instance’. Attribute on instance |
| [point](#nodebpy.nodes.geometry.geometry.SortElements.point) | Create Sort Elements with operation ‘Point’. Attribute on point |
| [spline](#nodebpy.nodes.geometry.geometry.SortElements.spline) | Create Sort Elements with operation ‘Spline’. Attribute on spline |

##### edge

``` python
edge(geometry=None, selection=True, group_id=0, sort_weight=0.0)
```

Create Sort Elements with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True, group_id=0, sort_weight=0.0)
```

Create Sort Elements with operation ‘Face’. Attribute on mesh faces

##### instance

``` python
instance(geometry=None, selection=True, group_id=0, sort_weight=0.0)
```

Create Sort Elements with operation ‘Instance’. Attribute on instance

##### point

``` python
point(geometry=None, selection=True, group_id=0, sort_weight=0.0)
```

Create Sort Elements with operation ‘Point’. Attribute on point

##### spline

``` python
spline(geometry=None, selection=True, group_id=0, sort_weight=0.0)
```

Create Sort Elements with operation ‘Spline’. Attribute on spline

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.geometry`    | `GeometrySocket` | Geometry    |
| `i.selection`   | `BooleanSocket`  | Selection   |
| `i.group_id`    | `IntegerSocket`  | Group ID    |
| `i.sort_weight` | `FloatSocket`    | Sort Weight |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### Spiral

``` python
Spiral(
    resolution=32,
    rotations=2.0,
    start_radius=1.0,
    end_radius=2.0,
    height=2.0,
    reverse=False,
)
```

Generate a poly spline in a spiral shape

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| resolution   | InputInteger | Resolution   | `32`    |
| rotations    | InputFloat   | Rotations    | `2.0`   |
| start_radius | InputFloat   | Start Radius | `1.0`   |
| end_radius   | InputFloat   | End Radius   | `2.0`   |
| height       | InputFloat   | Height       | `2.0`   |
| reverse      | InputBoolean | Reverse      | `False` |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Spiral.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Spiral.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Spiral.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Spiral.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Spiral.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Spiral.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Spiral.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Spiral.type)       |             |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.resolution`   | `IntegerSocket` | Resolution   |
| `i.rotations`    | `FloatSocket`   | Rotations    |
| `i.start_radius` | `FloatSocket`   | Start Radius |
| `i.end_radius`   | `FloatSocket`   | End Radius   |
| `i.height`       | `FloatSocket`   | Height       |
| `i.reverse`      | `BooleanSocket` | Reverse      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SplitEdges

``` python
SplitEdges(mesh=None, selection=True)
```

Duplicate mesh edges and break connections with the surrounding faces

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| mesh      | InputGeometry | Mesh        | `None`  |
| selection | InputBoolean  | Selection   | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SplitEdges.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SplitEdges.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SplitEdges.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SplitEdges.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SplitEdges.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SplitEdges.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SplitEdges.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SplitEdges.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.mesh`      | `GeometrySocket` | Mesh        |
| `i.selection` | `BooleanSocket`  | Selection   |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### SplitToInstances

``` python
SplitToInstances(geometry=None, selection=True, group_id=0, *, domain='POINT')
```

Create separate geometries containing the elements from the same group

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| geometry  | InputGeometry | Geometry    | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| group_id  | InputInteger  | Group ID    | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.geometry.SplitToInstances.domain) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.SplitToInstances.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SplitToInstances.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SplitToInstances.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SplitToInstances.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SplitToInstances.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SplitToInstances.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SplitToInstances.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SplitToInstances.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.geometry.SplitToInstances.edge) | Create Split to Instances with operation ‘Edge’. Attribute on mesh edge |
| [face](#nodebpy.nodes.geometry.geometry.SplitToInstances.face) | Create Split to Instances with operation ‘Face’. Attribute on mesh faces |
| [instance](#nodebpy.nodes.geometry.geometry.SplitToInstances.instance) | Create Split to Instances with operation ‘Instance’. Attribute on instance |
| [layer](#nodebpy.nodes.geometry.geometry.SplitToInstances.layer) | Create Split to Instances with operation ‘Layer’. Attribute on Grease Pencil layer |
| [point](#nodebpy.nodes.geometry.geometry.SplitToInstances.point) | Create Split to Instances with operation ‘Point’. Attribute on point |
| [spline](#nodebpy.nodes.geometry.geometry.SplitToInstances.spline) | Create Split to Instances with operation ‘Spline’. Attribute on spline |

##### edge

``` python
edge(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Edge’. Attribute on mesh edge

##### face

``` python
face(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Face’. Attribute on mesh faces

##### instance

``` python
instance(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Instance’. Attribute on instance

##### layer

``` python
layer(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Layer’. Attribute on Grease Pencil layer

##### point

``` python
point(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Point’. Attribute on point

##### spline

``` python
spline(geometry=None, selection=True, group_id=0)
```

Create Split to Instances with operation ‘Spline’. Attribute on spline

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.geometry`  | `GeometrySocket` | Geometry    |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.group_id`  | `IntegerSocket`  | Group ID    |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |
| `o.group_id`  | `IntegerSocket`  | Group ID    |

### Star

``` python
Star(points=8, inner_radius=1.0, outer_radius=2.0, twist=0.0)
```

Generate a poly spline in a star pattern by connecting alternating points of two circles

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| points       | InputInteger | Points       | `8`     |
| inner_radius | InputFloat   | Inner Radius | `1.0`   |
| outer_radius | InputFloat   | Outer Radius | `2.0`   |
| twist        | InputFloat   | Twist        | `0.0`   |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.geometry.Star.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Star.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.geometry.Star.name)       |             |
| [`node`](#nodebpy.nodes.geometry.geometry.Star.node)       |             |
| [`o`](#nodebpy.nodes.geometry.geometry.Star.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Star.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.geometry.Star.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.geometry.Star.type)       |             |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.points`       | `IntegerSocket` | Points       |
| `i.inner_radius` | `FloatSocket`   | Inner Radius |
| `i.outer_radius` | `FloatSocket`   | Outer Radius |
| `i.twist`        | `FloatSocket`   | Twist        |

**Outputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `o.curve`        | `GeometrySocket` | Curve        |
| `o.outer_points` | `BooleanSocket`  | Outer Points |

### StringToCurves

``` python
StringToCurves(
    string='',
    size=1.0,
    character_spacing=1.0,
    word_spacing=1.0,
    line_spacing=1.0,
    text_box_width=0.0,
    text_box_height=0.0,
    *,
    overflow='OVERFLOW',
    align_x='LEFT',
    align_y='TOP_BASELINE',
    pivot_mode='BOTTOM_LEFT',
)
```

Generate a paragraph of text with a specific font, using a curve instance to store each character

#### Parameters

| Name              | Type        | Description       | Default |
|-------------------|-------------|-------------------|---------|
| string            | InputString | String            | `''`    |
| size              | InputFloat  | Size              | `1.0`   |
| character_spacing | InputFloat  | Character Spacing | `1.0`   |
| word_spacing      | InputFloat  | Word Spacing      | `1.0`   |
| line_spacing      | InputFloat  | Line Spacing      | `1.0`   |
| text_box_width    | InputFloat  | Text Box Width    | `0.0`   |
| text_box_height   | InputFloat  | Text Box Height   | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`align_x`](#nodebpy.nodes.geometry.geometry.StringToCurves.align_x) |  |
| [`align_y`](#nodebpy.nodes.geometry.geometry.StringToCurves.align_y) |  |
| [`i`](#nodebpy.nodes.geometry.geometry.StringToCurves.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.StringToCurves.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.StringToCurves.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.StringToCurves.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.StringToCurves.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.StringToCurves.outputs) |  |
| [`overflow`](#nodebpy.nodes.geometry.geometry.StringToCurves.overflow) |  |
| [`pivot_mode`](#nodebpy.nodes.geometry.geometry.StringToCurves.pivot_mode) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.StringToCurves.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.StringToCurves.type) |  |

**Inputs**

| Attribute             | Type           | Description       |
|-----------------------|----------------|-------------------|
| `i.string`            | `StringSocket` | String            |
| `i.size`              | `FloatSocket`  | Size              |
| `i.character_spacing` | `FloatSocket`  | Character Spacing |
| `i.word_spacing`      | `FloatSocket`  | Word Spacing      |
| `i.line_spacing`      | `FloatSocket`  | Line Spacing      |
| `i.text_box_width`    | `FloatSocket`  | Text Box Width    |
| `i.text_box_height`   | `FloatSocket`  | Text Box Height   |

**Outputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `o.curve_instances` | `GeometrySocket` | Curve Instances |
| `o.remainder`       | `StringSocket`   | Remainder       |
| `o.line`            | `IntegerSocket`  | Line            |
| `o.pivot_point`     | `VectorSocket`   | Pivot Point     |

### SubdivideCurve

``` python
SubdivideCurve(curve=None, cuts=1)
```

Dividing each curve segment into a specified number of pieces

#### Parameters

| Name  | Type          | Description | Default |
|-------|---------------|-------------|---------|
| curve | InputGeometry | Curve       | `None`  |
| cuts  | InputInteger  | Cuts        | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SubdivideCurve.type) |  |

**Inputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `i.curve` | `GeometrySocket` | Curve       |
| `i.cuts`  | `IntegerSocket`  | Cuts        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### SubdivideMesh

``` python
SubdivideMesh(mesh=None, level=1)
```

Divide mesh faces into smaller ones without changing the shape or volume, using linear interpolation to place the new vertices

#### Parameters

| Name  | Type          | Description | Default |
|-------|---------------|-------------|---------|
| mesh  | InputGeometry | Mesh        | `None`  |
| level | InputInteger  | Level       | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SubdivideMesh.type) |  |

**Inputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `i.mesh`  | `GeometrySocket` | Mesh        |
| `i.level` | `IntegerSocket`  | Level       |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### SubdivisionSurface

``` python
SubdivisionSurface(
    mesh=None,
    level=1,
    edge_crease=0.0,
    vertex_crease=0.0,
    limit_surface=True,
    uv_smooth='Keep Boundaries',
    boundary_smooth='All',
)
```

Divide mesh faces to form a smooth surface, using the Catmull-Clark subdivision method

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| mesh | InputGeometry | Mesh | `None` |
| level | InputInteger | Level | `1` |
| edge_crease | InputFloat | Edge Crease | `0.0` |
| vertex_crease | InputFloat | Vertex Crease | `0.0` |
| limit_surface | InputBoolean | Limit Surface | `True` |
| uv_smooth | InputMenu \| Literal\['None', 'Keep Corners', 'Keep Corners, Junctions', 'Keep Corners, Junctions, Concave', 'Keep Boundaries', 'All'\] | UV Smooth | `'Keep Boundaries'` |
| boundary_smooth | InputMenu \| Literal\['Keep Corners', 'All'\] | Boundary Smooth | `'All'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.SubdivisionSurface.type) |  |

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.mesh`            | `GeometrySocket` | Mesh            |
| `i.level`           | `IntegerSocket`  | Level           |
| `i.edge_crease`     | `FloatSocket`    | Edge Crease     |
| `i.vertex_crease`   | `FloatSocket`    | Vertex Crease   |
| `i.limit_surface`   | `BooleanSocket`  | Limit Surface   |
| `i.uv_smooth`       | `MenuSocket`     | UV Smooth       |
| `i.boundary_smooth` | `MenuSocket`     | Boundary Smooth |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### TransformGeometry

``` python
TransformGeometry(
    geometry=None,
    mode='Components',
    translation=None,
    rotation=None,
    scale=None,
    transform=None,
)
```

Translate, rotate or scale the geometry

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| geometry | InputGeometry | Geometry | `None` |
| mode | InputMenu \| Literal\['Components', 'Matrix'\] | Mode | `'Components'` |
| translation | InputVector | Translation | `None` |
| rotation | InputRotation | Rotation | `None` |
| scale | InputVector | Scale | `None` |
| transform | InputMatrix | Transform | `None` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.TransformGeometry.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.TransformGeometry.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.TransformGeometry.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.TransformGeometry.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.TransformGeometry.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.TransformGeometry.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.TransformGeometry.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.TransformGeometry.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.geometry`    | `GeometrySocket` | Geometry    |
| `i.mode`        | `MenuSocket`     | Mode        |
| `i.translation` | `VectorSocket`   | Translation |
| `i.rotation`    | `RotationSocket` | Rotation    |
| `i.scale`       | `VectorSocket`   | Scale       |
| `i.transform`   | `MatrixSocket`   | Transform   |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.geometry` | `GeometrySocket` | Geometry    |

### TranslateInstances

``` python
TranslateInstances(
    instances=None,
    selection=True,
    translation=None,
    local_space=True,
)
```

Move top-level geometry instances in local or global space

#### Parameters

| Name        | Type          | Description | Default |
|-------------|---------------|-------------|---------|
| instances   | InputGeometry | Instances   | `None`  |
| selection   | InputBoolean  | Selection   | `True`  |
| translation | InputVector   | Translation | `None`  |
| local_space | InputBoolean  | Local Space | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.TranslateInstances.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.TranslateInstances.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.TranslateInstances.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.TranslateInstances.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.TranslateInstances.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.TranslateInstances.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.TranslateInstances.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.TranslateInstances.type) |  |

**Inputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `i.instances`   | `GeometrySocket` | Instances   |
| `i.selection`   | `BooleanSocket`  | Selection   |
| `i.translation` | `VectorSocket`   | Translation |
| `i.local_space` | `BooleanSocket`  | Local Space |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### Triangulate

``` python
Triangulate(
    mesh=None,
    selection=True,
    quad_method='Shortest Diagonal',
    n_gon_method='Beauty',
)
```

Convert all faces in a mesh to triangular faces

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| mesh | InputGeometry | Mesh | `None` |
| selection | InputBoolean | Selection | `True` |
| quad_method | InputMenu \| Literal\['Beauty', 'Fixed', 'Fixed Alternate', 'Shortest Diagonal', 'Longest Diagonal'\] | Quad Method | `'Shortest Diagonal'` |
| n_gon_method | InputMenu \| Literal\['Beauty', 'Clip'\] | N-gon Method | `'Beauty'` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.Triangulate.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.Triangulate.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.Triangulate.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.Triangulate.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.Triangulate.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.Triangulate.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.Triangulate.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.Triangulate.type) |  |

**Inputs**

| Attribute        | Type             | Description  |
|------------------|------------------|--------------|
| `i.mesh`         | `GeometrySocket` | Mesh         |
| `i.selection`    | `BooleanSocket`  | Selection    |
| `i.quad_method`  | `MenuSocket`     | Quad Method  |
| `i.n_gon_method` | `MenuSocket`     | N-gon Method |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### TrimCurve

``` python
TrimCurve(
    curve=None,
    selection=True,
    start=0.0,
    end=1.0,
    start_001=0.0,
    end_001=1.0,
    *,
    mode='FACTOR',
)
```

Shorten curves by removing portions at the start or end

#### Parameters

| Name      | Type          | Description | Default |
|-----------|---------------|-------------|---------|
| curve     | InputGeometry | Curve       | `None`  |
| selection | InputBoolean  | Selection   | `True`  |
| start     | InputFloat    | Start       | `0.0`   |
| end       | InputFloat    | End         | `1.0`   |
| start_001 | InputFloat    | Start       | `0.0`   |
| end_001   | InputFloat    | End         | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.TrimCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.TrimCurve.inputs) |  |
| [`mode`](#nodebpy.nodes.geometry.geometry.TrimCurve.mode) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.TrimCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.TrimCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.TrimCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.TrimCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.TrimCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.TrimCurve.type) |  |

#### Methods

| Name | Description |
|----|----|
| [factor](#nodebpy.nodes.geometry.geometry.TrimCurve.factor) | Create Trim Curve with operation ‘Factor’. Find the endpoint positions using a factor of each spline’s length |
| [length](#nodebpy.nodes.geometry.geometry.TrimCurve.length) | Create Trim Curve with operation ‘Length’. Find the endpoint positions using a length from the start of each spline |

##### factor

``` python
factor(curve=None, selection=True, start=0.0, end=1.0)
```

Create Trim Curve with operation ‘Factor’. Find the endpoint positions using a factor of each spline’s length

##### length

``` python
length(curve=None, selection=True, start_001=0.0, end_001=1.0)
```

Create Trim Curve with operation ‘Length’. Find the endpoint positions using a length from the start of each spline

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.curve`     | `GeometrySocket` | Curve       |
| `i.selection` | `BooleanSocket`  | Selection   |
| `i.start`     | `FloatSocket`    | Start       |
| `i.end`       | `FloatSocket`    | End         |
| `i.start_001` | `FloatSocket`    | Start       |
| `i.end_001`   | `FloatSocket`    | End         |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.curve` | `GeometrySocket` | Curve       |

### UVSphere

``` python
UVSphere(segments=32, rings=16, radius=1.0)
```

Generate a spherical mesh with quads, except for triangles at the top and bottom

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| segments | InputInteger | Segments    | `32`    |
| rings    | InputInteger | Rings       | `16`    |
| radius   | InputFloat   | Radius      | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.geometry.UVSphere.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.geometry.UVSphere.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.geometry.UVSphere.name) |  |
| [`node`](#nodebpy.nodes.geometry.geometry.UVSphere.node) |  |
| [`o`](#nodebpy.nodes.geometry.geometry.UVSphere.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.geometry.UVSphere.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.geometry.UVSphere.tree) |  |
| [`type`](#nodebpy.nodes.geometry.geometry.UVSphere.type) |  |

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.segments` | `IntegerSocket` | Segments    |
| `i.rings`    | `IntegerSocket` | Rings       |
| `i.radius`   | `FloatSocket`   | Radius      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.mesh`   | `GeometrySocket` | Mesh        |
| `o.uv_map` | `VectorSocket`   | UV Map      |
