# nodes.geometry.input

`input`

## Classes

| Name | Description |
|----|----|
| [ActiveCamera](#nodebpy.nodes.geometry.input.ActiveCamera) | Retrieve the scene’s active camera |
| [ActiveElement](#nodebpy.nodes.geometry.input.ActiveElement) | Active element indices of the edited geometry, for tool execution |
| [Boolean](#nodebpy.nodes.geometry.input.Boolean) | Provide a True/False value that can be connected to other nodes in the tree |
| [CameraInfo](#nodebpy.nodes.geometry.input.CameraInfo) | Retrieve information from a camera object |
| [CollectionInfo](#nodebpy.nodes.geometry.input.CollectionInfo) | Retrieve geometry instances from a collection |
| [Color](#nodebpy.nodes.geometry.input.Color) | Output a color value chosen with the color picker widget |
| [CornersOfEdge](#nodebpy.nodes.geometry.input.CornersOfEdge) | Retrieve face corners connected to edges |
| [CornersOfFace](#nodebpy.nodes.geometry.input.CornersOfFace) | Retrieve corners that make up a face |
| [CornersOfVertex](#nodebpy.nodes.geometry.input.CornersOfVertex) | Retrieve face corners connected to vertices |
| [Cursor3D](#nodebpy.nodes.geometry.input.Cursor3D) | The scene’s 3D cursor location and rotation |
| [CurveHandlePositions](#nodebpy.nodes.geometry.input.CurveHandlePositions) | Retrieve the position of each Bézier control point’s handles |
| [CurveOfPoint](#nodebpy.nodes.geometry.input.CurveOfPoint) | Retrieve the curve a control point is part of |
| [CurveTangent](#nodebpy.nodes.geometry.input.CurveTangent) | Retrieve the direction of curves at each control point |
| [CurveTilt](#nodebpy.nodes.geometry.input.CurveTilt) | Retrieve the angle at each control point used to twist the curve’s normal around its tangent |
| [EdgeAngle](#nodebpy.nodes.geometry.input.EdgeAngle) | The angle between the normals of connected manifold faces |
| [EdgeNeighbors](#nodebpy.nodes.geometry.input.EdgeNeighbors) | Retrieve the number of faces that use each edge as one of their sides |
| [EdgePathsToSelection](#nodebpy.nodes.geometry.input.EdgePathsToSelection) | Output a selection of edges by following paths across mesh edges |
| [EdgeVertices](#nodebpy.nodes.geometry.input.EdgeVertices) | Retrieve topology information relating to each edge of a mesh |
| [EdgesOfCorner](#nodebpy.nodes.geometry.input.EdgesOfCorner) | Retrieve the edges on both sides of a face corner |
| [EdgesOfVertex](#nodebpy.nodes.geometry.input.EdgesOfVertex) | Retrieve the edges connected to each vertex |
| [EdgesToFaceGroups](#nodebpy.nodes.geometry.input.EdgesToFaceGroups) | Group faces into regions surrounded by the selected boundary edges |
| [EndpointSelection](#nodebpy.nodes.geometry.input.EndpointSelection) | Provide a selection for an arbitrary number of endpoints in each spline |
| [FaceArea](#nodebpy.nodes.geometry.input.FaceArea) | Calculate the surface area of a mesh’s faces |
| [FaceGroupBoundaries](#nodebpy.nodes.geometry.input.FaceGroupBoundaries) | Find edges on the boundaries between groups of faces with the same ID value |
| [FaceNeighbors](#nodebpy.nodes.geometry.input.FaceNeighbors) | Retrieve topology information relating to each face of a mesh |
| [FaceOfCorner](#nodebpy.nodes.geometry.input.FaceOfCorner) | Retrieve the face each face corner is part of |
| [FaceSet](#nodebpy.nodes.geometry.input.FaceSet) | Each face’s sculpt face set value |
| [ID](#nodebpy.nodes.geometry.input.ID) | Retrieve a stable random identifier value from the “id” attribute on the point domain, or the index if the attribute does not exist |
| [Image](#nodebpy.nodes.geometry.input.Image) | Input an image data-block |
| [ImageInfo](#nodebpy.nodes.geometry.input.ImageInfo) | Retrieve information about an image |
| [ImportCSV](#nodebpy.nodes.geometry.input.ImportCSV) | Import geometry from an CSV file |
| [ImportOBJ](#nodebpy.nodes.geometry.input.ImportOBJ) | Import geometry from an OBJ file |
| [ImportPLY](#nodebpy.nodes.geometry.input.ImportPLY) | Import a point cloud from a PLY file |
| [ImportSTL](#nodebpy.nodes.geometry.input.ImportSTL) | Import a mesh from an STL file |
| [ImportText](#nodebpy.nodes.geometry.input.ImportText) | Import a string from a text file |
| [ImportVDB](#nodebpy.nodes.geometry.input.ImportVDB) | Import volume data from a .vdb file |
| [Index](#nodebpy.nodes.geometry.input.Index) | Retrieve an integer value indicating the position of each element in the list, starting at zero |
| [InstanceBounds](#nodebpy.nodes.geometry.input.InstanceBounds) | Calculate position bounds of each instance’s geometry set |
| [InstanceRotation](#nodebpy.nodes.geometry.input.InstanceRotation) | Retrieve the rotation of each instance in the geometry |
| [InstanceScale](#nodebpy.nodes.geometry.input.InstanceScale) | Retrieve the scale of each instance in the geometry |
| [InstanceTransform](#nodebpy.nodes.geometry.input.InstanceTransform) | Retrieve the full transformation of each instance in the geometry |
| [Integer](#nodebpy.nodes.geometry.input.Integer) | Provide an integer value that can be connected to other nodes in the tree |
| [IsEdgeSmooth](#nodebpy.nodes.geometry.input.IsEdgeSmooth) | Retrieve whether each edge is marked for smooth or split normals |
| [IsFacePlanar](#nodebpy.nodes.geometry.input.IsFacePlanar) | Retrieve whether all triangles in a face are on the same plane, i.e. whether they have the same normal |
| [IsFaceSmooth](#nodebpy.nodes.geometry.input.IsFaceSmooth) | Retrieve whether each face is marked for smooth or sharp normals |
| [IsSplineCyclic](#nodebpy.nodes.geometry.input.IsSplineCyclic) | Retrieve whether each spline endpoint connects to the beginning |
| [IsViewport](#nodebpy.nodes.geometry.input.IsViewport) | Retrieve whether the nodes are being evaluated for the viewport rather than the final render |
| [MaterialIndex](#nodebpy.nodes.geometry.input.MaterialIndex) | Retrieve the index of the material used for each element in the geometry’s list of materials |
| [MeshIsland](#nodebpy.nodes.geometry.input.MeshIsland) | Retrieve information about separate connected regions in a mesh |
| [MousePosition](#nodebpy.nodes.geometry.input.MousePosition) | Retrieve the position of the mouse cursor |
| [NamedAttribute](#nodebpy.nodes.geometry.input.NamedAttribute) | Retrieve the data of a specified attribute |
| [NamedLayerSelection](#nodebpy.nodes.geometry.input.NamedLayerSelection) | Output a selection of a Grease Pencil layer |
| [Normal](#nodebpy.nodes.geometry.input.Normal) | Retrieve a unit length vector indicating the direction pointing away from the geometry at each element |
| [ObjectInfo](#nodebpy.nodes.geometry.input.ObjectInfo) | Retrieve information from an object |
| [OffsetCornerInFace](#nodebpy.nodes.geometry.input.OffsetCornerInFace) | Retrieve corners in the same face as another |
| [OffsetPointInCurve](#nodebpy.nodes.geometry.input.OffsetPointInCurve) | Offset a control point index within its curve |
| [PointsOfCurve](#nodebpy.nodes.geometry.input.PointsOfCurve) | Retrieve a point index within a curve |
| [Position](#nodebpy.nodes.geometry.input.Position) | Retrieve a vector indicating the location of each element |
| [Radius](#nodebpy.nodes.geometry.input.Radius) | Retrieve the radius at each point on curve or point cloud geometry |
| [Rotation](#nodebpy.nodes.geometry.input.Rotation) | Provide a rotation value that can be connected to other nodes in the tree |
| [SceneTime](#nodebpy.nodes.geometry.input.SceneTime) | Retrieve the current time in the scene’s animation in units of seconds or frames |
| [Selection](#nodebpy.nodes.geometry.input.Selection) | User selection of the edited geometry, for tool execution |
| [SelfObject](#nodebpy.nodes.geometry.input.SelfObject) | Retrieve the object that contains the geometry nodes modifier currently being executed |
| [ShortestEdgePaths](#nodebpy.nodes.geometry.input.ShortestEdgePaths) | Find the shortest paths along mesh edges to selected end vertices, with customizable cost per edge |
| [SpecialCharacters](#nodebpy.nodes.geometry.input.SpecialCharacters) | Output string characters that cannot be typed directly with the keyboard |
| [SplineLength](#nodebpy.nodes.geometry.input.SplineLength) | Retrieve the total length of each spline, as a distance or as a number of points |
| [SplineParameter](#nodebpy.nodes.geometry.input.SplineParameter) | Retrieve how far along each spline a control point is |
| [SplineResolution](#nodebpy.nodes.geometry.input.SplineResolution) | Retrieve the number of evaluated points that will be generated for every control point on curves |
| [String](#nodebpy.nodes.geometry.input.String) | Provide a string value that can be connected to other nodes in the tree |
| [UVTangent](#nodebpy.nodes.geometry.input.UVTangent) | Generate tangent directions based on a UV map |
| [Vector](#nodebpy.nodes.geometry.input.Vector) | Provide a vector value that can be connected to other nodes in the tree |
| [VertexNeighbors](#nodebpy.nodes.geometry.input.VertexNeighbors) | Retrieve topology information relating to each vertex of a mesh |
| [VertexOfCorner](#nodebpy.nodes.geometry.input.VertexOfCorner) | Retrieve the vertex each face corner is attached to |
| [ViewportTransform](#nodebpy.nodes.geometry.input.ViewportTransform) | Retrieve the view direction and location of the 3D viewport |
| [VoxelIndex](#nodebpy.nodes.geometry.input.VoxelIndex) | Retrieve the integer coordinates of the voxel that the field is evaluated on |

### ActiveCamera

``` python
ActiveCamera()
```

Retrieve the scene’s active camera

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.ActiveCamera.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.ActiveCamera.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.ActiveCamera.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.ActiveCamera.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.ActiveCamera.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.ActiveCamera.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.ActiveCamera.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.ActiveCamera.type) |  |

**Outputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `o.active_camera` | `ObjectSocket` | Active Camera |

### ActiveElement

``` python
ActiveElement(domain='POINT')
```

Active element indices of the edited geometry, for tool execution

#### Attributes

| Name | Description |
|----|----|
| [`domain`](#nodebpy.nodes.geometry.input.ActiveElement.domain) |  |
| [`i`](#nodebpy.nodes.geometry.input.ActiveElement.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.ActiveElement.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.ActiveElement.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.ActiveElement.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.ActiveElement.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.ActiveElement.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.ActiveElement.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.ActiveElement.type) |  |

#### Methods

| Name | Description |
|----|----|
| [edge](#nodebpy.nodes.geometry.input.ActiveElement.edge) | Create Active Element with operation ‘Edge’. |
| [face](#nodebpy.nodes.geometry.input.ActiveElement.face) | Create Active Element with operation ‘Face’. |
| [layer](#nodebpy.nodes.geometry.input.ActiveElement.layer) | Create Active Element with operation ‘Layer’. |
| [point](#nodebpy.nodes.geometry.input.ActiveElement.point) | Create Active Element with operation ‘Point’. |

##### edge

``` python
edge()
```

Create Active Element with operation ‘Edge’.

##### face

``` python
face()
```

Create Active Element with operation ‘Face’.

##### layer

``` python
layer()
```

Create Active Element with operation ‘Layer’.

##### point

``` python
point()
```

Create Active Element with operation ‘Point’.

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.index`  | `IntegerSocket` | Index       |
| `o.exists` | `BooleanSocket` | Exists      |

### Boolean

``` python
Boolean(boolean=False)
```

Provide a True/False value that can be connected to other nodes in the tree

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`boolean`](#nodebpy.nodes.geometry.input.Boolean.boolean) |             |
| [`i`](#nodebpy.nodes.geometry.input.Boolean.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Boolean.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Boolean.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Boolean.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Boolean.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Boolean.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Boolean.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Boolean.type)       |             |

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.boolean` | `BooleanSocket` | Boolean     |

### CameraInfo

``` python
CameraInfo(camera=None)
```

Retrieve information from a camera object

#### Parameters

| Name   | Type        | Description | Default |
|--------|-------------|-------------|---------|
| camera | InputObject | Camera      | `None`  |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.CameraInfo.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.CameraInfo.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.CameraInfo.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.CameraInfo.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.CameraInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.CameraInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.CameraInfo.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.CameraInfo.type)       |             |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.camera` | `ObjectSocket` | Camera      |

**Outputs**

| Attribute              | Type            | Description        |
|------------------------|-----------------|--------------------|
| `o.projection_matrix`  | `MatrixSocket`  | Projection Matrix  |
| `o.focal_length`       | `FloatSocket`   | Focal Length       |
| `o.sensor`             | `VectorSocket`  | Sensor             |
| `o.shift`              | `VectorSocket`  | Shift              |
| `o.clip_start`         | `FloatSocket`   | Clip Start         |
| `o.clip_end`           | `FloatSocket`   | Clip End           |
| `o.focus_distance`     | `FloatSocket`   | Focus Distance     |
| `o.is_orthographic`    | `BooleanSocket` | Is Orthographic    |
| `o.orthographic_scale` | `FloatSocket`   | Orthographic Scale |

### CollectionInfo

``` python
CollectionInfo(
    collection=None,
    separate_children=False,
    reset_children=False,
    *,
    transform_space='ORIGINAL',
)
```

Retrieve geometry instances from a collection

#### Parameters

| Name              | Type            | Description       | Default |
|-------------------|-----------------|-------------------|---------|
| collection        | InputCollection | Collection        | `None`  |
| separate_children | InputBoolean    | Separate Children | `False` |
| reset_children    | InputBoolean    | Reset Children    | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CollectionInfo.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CollectionInfo.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CollectionInfo.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CollectionInfo.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CollectionInfo.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CollectionInfo.outputs) |  |
| [`transform_space`](#nodebpy.nodes.geometry.input.CollectionInfo.transform_space) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CollectionInfo.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CollectionInfo.type) |  |

**Inputs**

| Attribute             | Type               | Description       |
|-----------------------|--------------------|-------------------|
| `i.collection`        | `CollectionSocket` | Collection        |
| `i.separate_children` | `BooleanSocket`    | Separate Children |
| `i.reset_children`    | `BooleanSocket`    | Reset Children    |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### Color

``` python
Color(value=(0.735, 0.735, 0.735, 1.0))
```

Output a color value chosen with the color picker widget

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Color.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Color.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Color.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Color.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Color.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Color.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Color.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Color.type)       |             |
| [`value`](#nodebpy.nodes.geometry.input.Color.value)     |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.color` | `ColorSocket` | Color       |

### CornersOfEdge

``` python
CornersOfEdge(edge_index=0, weights=0.0, sort_index=0)
```

Retrieve face corners connected to edges

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| edge_index | InputInteger | Edge Index  | `0`     |
| weights    | InputFloat   | Weights     | `0.0`   |
| sort_index | InputInteger | Sort Index  | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CornersOfEdge.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CornersOfEdge.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CornersOfEdge.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CornersOfEdge.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CornersOfEdge.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CornersOfEdge.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CornersOfEdge.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CornersOfEdge.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.edge_index` | `IntegerSocket` | Edge Index  |
| `i.weights`    | `FloatSocket`   | Weights     |
| `i.sort_index` | `IntegerSocket` | Sort Index  |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.corner_index` | `IntegerSocket` | Corner Index |
| `o.total`        | `IntegerSocket` | Total        |

### CornersOfFace

``` python
CornersOfFace(face_index=0, weights=0.0, sort_index=0)
```

Retrieve corners that make up a face

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| face_index | InputInteger | Face Index  | `0`     |
| weights    | InputFloat   | Weights     | `0.0`   |
| sort_index | InputInteger | Sort Index  | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CornersOfFace.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CornersOfFace.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CornersOfFace.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CornersOfFace.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CornersOfFace.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CornersOfFace.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CornersOfFace.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CornersOfFace.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.face_index` | `IntegerSocket` | Face Index  |
| `i.weights`    | `FloatSocket`   | Weights     |
| `i.sort_index` | `IntegerSocket` | Sort Index  |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.corner_index` | `IntegerSocket` | Corner Index |
| `o.total`        | `IntegerSocket` | Total        |

### CornersOfVertex

``` python
CornersOfVertex(vertex_index=0, weights=0.0, sort_index=0)
```

Retrieve face corners connected to vertices

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| vertex_index | InputInteger | Vertex Index | `0`     |
| weights      | InputFloat   | Weights      | `0.0`   |
| sort_index   | InputInteger | Sort Index   | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CornersOfVertex.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CornersOfVertex.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CornersOfVertex.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CornersOfVertex.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CornersOfVertex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CornersOfVertex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CornersOfVertex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CornersOfVertex.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.vertex_index` | `IntegerSocket` | Vertex Index |
| `i.weights`      | `FloatSocket`   | Weights      |
| `i.sort_index`   | `IntegerSocket` | Sort Index   |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.corner_index` | `IntegerSocket` | Corner Index |
| `o.total`        | `IntegerSocket` | Total        |

### Cursor3D

``` python
Cursor3D()
```

The scene’s 3D cursor location and rotation

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Cursor3D.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Cursor3D.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Cursor3D.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Cursor3D.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Cursor3D.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Cursor3D.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Cursor3D.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Cursor3D.type)       |             |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.location` | `VectorSocket`   | Location    |
| `o.rotation` | `RotationSocket` | Rotation    |

### CurveHandlePositions

``` python
CurveHandlePositions(relative=False)
```

Retrieve the position of each Bézier control point’s handles

#### Parameters

| Name     | Type         | Description | Default |
|----------|--------------|-------------|---------|
| relative | InputBoolean | Relative    | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CurveHandlePositions.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CurveHandlePositions.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CurveHandlePositions.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CurveHandlePositions.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CurveHandlePositions.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CurveHandlePositions.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CurveHandlePositions.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CurveHandlePositions.type) |  |

**Inputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `i.relative` | `BooleanSocket` | Relative    |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.left`  | `VectorSocket` | Left        |
| `o.right` | `VectorSocket` | Right       |

### CurveOfPoint

``` python
CurveOfPoint(point_index=0)
```

Retrieve the curve a control point is part of

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| point_index | InputInteger | Point Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CurveOfPoint.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CurveOfPoint.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CurveOfPoint.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CurveOfPoint.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CurveOfPoint.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CurveOfPoint.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CurveOfPoint.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CurveOfPoint.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.point_index` | `IntegerSocket` | Point Index |

**Outputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `o.curve_index`    | `IntegerSocket` | Curve Index    |
| `o.index_in_curve` | `IntegerSocket` | Index in Curve |

### CurveTangent

``` python
CurveTangent()
```

Retrieve the direction of curves at each control point

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.CurveTangent.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.CurveTangent.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.CurveTangent.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.CurveTangent.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.CurveTangent.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.CurveTangent.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.CurveTangent.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.CurveTangent.type) |  |

**Outputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `o.tangent` | `VectorSocket` | Tangent     |

### CurveTilt

``` python
CurveTilt()
```

Retrieve the angle at each control point used to twist the curve’s normal around its tangent

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.CurveTilt.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.CurveTilt.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.CurveTilt.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.CurveTilt.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.CurveTilt.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.CurveTilt.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.CurveTilt.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.CurveTilt.type)       |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.tilt`  | `FloatSocket` | Tilt        |

### EdgeAngle

``` python
EdgeAngle()
```

The angle between the normals of connected manifold faces

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.EdgeAngle.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgeAngle.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.EdgeAngle.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.EdgeAngle.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.EdgeAngle.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgeAngle.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.EdgeAngle.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.EdgeAngle.type)       |             |

**Outputs**

| Attribute          | Type          | Description    |
|--------------------|---------------|----------------|
| `o.unsigned_angle` | `FloatSocket` | Unsigned Angle |
| `o.signed_angle`   | `FloatSocket` | Signed Angle   |

### EdgeNeighbors

``` python
EdgeNeighbors()
```

Retrieve the number of faces that use each edge as one of their sides

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgeNeighbors.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgeNeighbors.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgeNeighbors.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgeNeighbors.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgeNeighbors.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgeNeighbors.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgeNeighbors.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgeNeighbors.type) |  |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.face_count` | `IntegerSocket` | Face Count  |

### EdgePathsToSelection

``` python
EdgePathsToSelection(start_vertices=True, next_vertex_index=-1)
```

Output a selection of edges by following paths across mesh edges

#### Parameters

| Name              | Type         | Description       | Default |
|-------------------|--------------|-------------------|---------|
| start_vertices    | InputBoolean | Start Vertices    | `True`  |
| next_vertex_index | InputInteger | Next Vertex Index | `-1`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgePathsToSelection.type) |  |

**Inputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `i.start_vertices`    | `BooleanSocket` | Start Vertices    |
| `i.next_vertex_index` | `IntegerSocket` | Next Vertex Index |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.selection` | `BooleanSocket` | Selection   |

### EdgeVertices

``` python
EdgeVertices()
```

Retrieve topology information relating to each edge of a mesh

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgeVertices.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgeVertices.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgeVertices.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgeVertices.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgeVertices.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgeVertices.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgeVertices.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgeVertices.type) |  |

**Outputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `o.vertex_index_1` | `IntegerSocket` | Vertex Index 1 |
| `o.vertex_index_2` | `IntegerSocket` | Vertex Index 2 |
| `o.position_1`     | `VectorSocket`  | Position 1     |
| `o.position_2`     | `VectorSocket`  | Position 2     |

### EdgesOfCorner

``` python
EdgesOfCorner(corner_index=0)
```

Retrieve the edges on both sides of a face corner

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| corner_index | InputInteger | Corner Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgesOfCorner.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgesOfCorner.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgesOfCorner.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgesOfCorner.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgesOfCorner.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgesOfCorner.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgesOfCorner.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgesOfCorner.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.corner_index` | `IntegerSocket` | Corner Index |

**Outputs**

| Attribute               | Type            | Description         |
|-------------------------|-----------------|---------------------|
| `o.next_edge_index`     | `IntegerSocket` | Next Edge Index     |
| `o.previous_edge_index` | `IntegerSocket` | Previous Edge Index |

### EdgesOfVertex

``` python
EdgesOfVertex(vertex_index=0, weights=0.0, sort_index=0)
```

Retrieve the edges connected to each vertex

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| vertex_index | InputInteger | Vertex Index | `0`     |
| weights      | InputFloat   | Weights      | `0.0`   |
| sort_index   | InputInteger | Sort Index   | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgesOfVertex.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgesOfVertex.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgesOfVertex.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgesOfVertex.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgesOfVertex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgesOfVertex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgesOfVertex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgesOfVertex.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.vertex_index` | `IntegerSocket` | Vertex Index |
| `i.weights`      | `FloatSocket`   | Weights      |
| `i.sort_index`   | `IntegerSocket` | Sort Index   |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.edge_index` | `IntegerSocket` | Edge Index  |
| `o.total`      | `IntegerSocket` | Total       |

### EdgesToFaceGroups

``` python
EdgesToFaceGroups(boundary_edges=True)
```

Group faces into regions surrounded by the selected boundary edges

#### Parameters

| Name           | Type         | Description    | Default |
|----------------|--------------|----------------|---------|
| boundary_edges | InputBoolean | Boundary Edges | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EdgesToFaceGroups.type) |  |

**Inputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `i.boundary_edges` | `BooleanSocket` | Boundary Edges |

**Outputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `o.face_group_id` | `IntegerSocket` | Face Group ID |

### EndpointSelection

``` python
EndpointSelection(start_size=1, end_size=1)
```

Provide a selection for an arbitrary number of endpoints in each spline

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| start_size | InputInteger | Start Size  | `1`     |
| end_size   | InputInteger | End Size    | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.EndpointSelection.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.EndpointSelection.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.EndpointSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.EndpointSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.EndpointSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.EndpointSelection.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.EndpointSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.EndpointSelection.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.start_size` | `IntegerSocket` | Start Size  |
| `i.end_size`   | `IntegerSocket` | End Size    |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.selection` | `BooleanSocket` | Selection   |

### FaceArea

``` python
FaceArea()
```

Calculate the surface area of a mesh’s faces

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.FaceArea.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.FaceArea.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.FaceArea.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.FaceArea.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.FaceArea.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.FaceArea.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.FaceArea.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.FaceArea.type)       |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.area`  | `FloatSocket` | Area        |

### FaceGroupBoundaries

``` python
FaceGroupBoundaries(face_set=0)
```

Find edges on the boundaries between groups of faces with the same ID value

#### Parameters

| Name     | Type         | Description   | Default |
|----------|--------------|---------------|---------|
| face_set | InputInteger | Face Group ID | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.FaceGroupBoundaries.type) |  |

**Inputs**

| Attribute    | Type            | Description   |
|--------------|-----------------|---------------|
| `i.face_set` | `IntegerSocket` | Face Group ID |

**Outputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `o.boundary_edges` | `BooleanSocket` | Boundary Edges |

### FaceNeighbors

``` python
FaceNeighbors()
```

Retrieve topology information relating to each face of a mesh

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.FaceNeighbors.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.FaceNeighbors.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.FaceNeighbors.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.FaceNeighbors.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.FaceNeighbors.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.FaceNeighbors.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.FaceNeighbors.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.FaceNeighbors.type) |  |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.vertex_count` | `IntegerSocket` | Vertex Count |
| `o.face_count`   | `IntegerSocket` | Face Count   |

### FaceOfCorner

``` python
FaceOfCorner(corner_index=0)
```

Retrieve the face each face corner is part of

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| corner_index | InputInteger | Corner Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.FaceOfCorner.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.FaceOfCorner.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.FaceOfCorner.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.FaceOfCorner.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.FaceOfCorner.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.FaceOfCorner.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.FaceOfCorner.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.FaceOfCorner.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.corner_index` | `IntegerSocket` | Corner Index |

**Outputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `o.face_index`    | `IntegerSocket` | Face Index    |
| `o.index_in_face` | `IntegerSocket` | Index in Face |

### FaceSet

``` python
FaceSet()
```

Each face’s sculpt face set value

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.FaceSet.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.FaceSet.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.FaceSet.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.FaceSet.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.FaceSet.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.FaceSet.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.FaceSet.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.FaceSet.type)       |             |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.face_set` | `IntegerSocket` | Face Set    |
| `o.exists`   | `BooleanSocket` | Exists      |

### ID

``` python
ID()
```

Retrieve a stable random identifier value from the “id” attribute on the point domain, or the index if the attribute does not exist

#### Attributes

| Name                                                  | Description |
|-------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ID.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ID.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ID.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ID.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ID.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ID.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ID.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ID.type)       |             |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.id`    | `IntegerSocket` | ID          |

### Image

``` python
Image()
```

Input an image data-block

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Image.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Image.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Image.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Image.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Image.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Image.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Image.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Image.type)       |             |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.image` | `ImageSocket` | Image       |

### ImageInfo

``` python
ImageInfo(image=None, frame=0)
```

Retrieve information about an image

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| image | InputImage   | Image       | `None`  |
| frame | InputInteger | Frame       | `0`     |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImageInfo.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImageInfo.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImageInfo.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImageInfo.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImageInfo.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImageInfo.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImageInfo.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImageInfo.type)       |             |

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.image` | `ImageSocket`   | Image       |
| `i.frame` | `IntegerSocket` | Frame       |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.width`       | `IntegerSocket` | Width       |
| `o.height`      | `IntegerSocket` | Height      |
| `o.has_alpha`   | `BooleanSocket` | Has Alpha   |
| `o.frame_count` | `IntegerSocket` | Frame Count |
| `o.fps`         | `FloatSocket`   | FPS         |

### ImportCSV

``` python
ImportCSV(path='', delimiter=',')
```

Import geometry from an CSV file

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| path      | InputString | Path        | `''`    |
| delimiter | InputString | Delimiter   | `','`   |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportCSV.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportCSV.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportCSV.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportCSV.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportCSV.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportCSV.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportCSV.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportCSV.type)       |             |

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.path`      | `StringSocket` | Path        |
| `i.delimiter` | `StringSocket` | Delimiter   |

**Outputs**

| Attribute       | Type             | Description |
|-----------------|------------------|-------------|
| `o.point_cloud` | `GeometrySocket` | Point Cloud |

### ImportOBJ

``` python
ImportOBJ(path='')
```

Import geometry from an OBJ file

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| path | InputString | Path        | `''`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportOBJ.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportOBJ.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportOBJ.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportOBJ.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportOBJ.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportOBJ.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportOBJ.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportOBJ.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.path`  | `StringSocket` | Path        |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.instances` | `GeometrySocket` | Instances   |

### ImportPLY

``` python
ImportPLY(path='')
```

Import a point cloud from a PLY file

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| path | InputString | Path        | `''`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportPLY.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportPLY.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportPLY.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportPLY.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportPLY.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportPLY.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportPLY.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportPLY.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.path`  | `StringSocket` | Path        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### ImportSTL

``` python
ImportSTL(path='')
```

Import a mesh from an STL file

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| path | InputString | Path        | `''`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportSTL.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportSTL.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportSTL.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportSTL.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportSTL.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportSTL.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportSTL.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportSTL.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.path`  | `StringSocket` | Path        |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### ImportText

``` python
ImportText(path='')
```

Import a string from a text file

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| path | InputString | Path        | `''`    |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportText.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportText.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportText.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportText.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportText.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportText.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportText.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportText.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.path`  | `StringSocket` | Path        |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.string` | `StringSocket` | String      |

### ImportVDB

``` python
ImportVDB(path='')
```

Import volume data from a .vdb file

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| path | InputString | Path        | `''`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.ImportVDB.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.ImportVDB.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.ImportVDB.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.ImportVDB.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.ImportVDB.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.ImportVDB.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.ImportVDB.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.ImportVDB.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.path`  | `StringSocket` | Path        |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |

### Index

``` python
Index()
```

Retrieve an integer value indicating the position of each element in the list, starting at zero

#### Attributes

| Name                                                     | Description |
|----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Index.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Index.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Index.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Index.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Index.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Index.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Index.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Index.type)       |             |

**Outputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `o.index` | `IntegerSocket` | Index       |

### InstanceBounds

``` python
InstanceBounds(use_radius=True)
```

Calculate position bounds of each instance’s geometry set

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| use_radius | InputBoolean | Use Radius  | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.InstanceBounds.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.InstanceBounds.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.InstanceBounds.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.InstanceBounds.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.InstanceBounds.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.InstanceBounds.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.InstanceBounds.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.InstanceBounds.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.use_radius` | `BooleanSocket` | Use Radius  |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.min`   | `VectorSocket` | Min         |
| `o.max`   | `VectorSocket` | Max         |

### InstanceRotation

``` python
InstanceRotation()
```

Retrieve the rotation of each instance in the geometry

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.InstanceRotation.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.InstanceRotation.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.InstanceRotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.InstanceRotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.InstanceRotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.InstanceRotation.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.InstanceRotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.InstanceRotation.type) |  |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### InstanceScale

``` python
InstanceScale()
```

Retrieve the scale of each instance in the geometry

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.InstanceScale.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.InstanceScale.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.InstanceScale.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.InstanceScale.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.InstanceScale.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.InstanceScale.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.InstanceScale.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.InstanceScale.type) |  |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.scale` | `VectorSocket` | Scale       |

### InstanceTransform

``` python
InstanceTransform()
```

Retrieve the full transformation of each instance in the geometry

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.InstanceTransform.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.InstanceTransform.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.InstanceTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.InstanceTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.InstanceTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.InstanceTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.InstanceTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.InstanceTransform.type) |  |

**Outputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `o.transform` | `MatrixSocket` | Transform   |

### Integer

``` python
Integer(integer=1)
```

Provide an integer value that can be connected to other nodes in the tree

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Integer.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Integer.inputs)   |             |
| [`integer`](#nodebpy.nodes.geometry.input.Integer.integer) |             |
| [`name`](#nodebpy.nodes.geometry.input.Integer.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Integer.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Integer.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Integer.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Integer.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Integer.type)       |             |

**Outputs**

| Attribute   | Type            | Description |
|-------------|-----------------|-------------|
| `o.integer` | `IntegerSocket` | Integer     |

### IsEdgeSmooth

``` python
IsEdgeSmooth()
```

Retrieve whether each edge is marked for smooth or split normals

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.IsEdgeSmooth.type) |  |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.smooth` | `BooleanSocket` | Smooth      |

### IsFacePlanar

``` python
IsFacePlanar(threshold=0.01)
```

Retrieve whether all triangles in a face are on the same plane, i.e. whether they have the same normal

#### Parameters

| Name      | Type       | Description | Default |
|-----------|------------|-------------|---------|
| threshold | InputFloat | Threshold   | `0.01`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.IsFacePlanar.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.IsFacePlanar.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.IsFacePlanar.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.IsFacePlanar.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.IsFacePlanar.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.IsFacePlanar.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.IsFacePlanar.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.IsFacePlanar.type) |  |

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.threshold` | `FloatSocket` | Threshold   |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.planar` | `BooleanSocket` | Planar      |

### IsFaceSmooth

``` python
IsFaceSmooth()
```

Retrieve whether each face is marked for smooth or sharp normals

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.IsFaceSmooth.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.IsFaceSmooth.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.IsFaceSmooth.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.IsFaceSmooth.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.IsFaceSmooth.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.IsFaceSmooth.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.IsFaceSmooth.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.IsFaceSmooth.type) |  |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.smooth` | `BooleanSocket` | Smooth      |

### IsSplineCyclic

``` python
IsSplineCyclic()
```

Retrieve whether each spline endpoint connects to the beginning

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.IsSplineCyclic.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.IsSplineCyclic.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.IsSplineCyclic.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.IsSplineCyclic.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.IsSplineCyclic.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.IsSplineCyclic.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.IsSplineCyclic.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.IsSplineCyclic.type) |  |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.cyclic` | `BooleanSocket` | Cyclic      |

### IsViewport

``` python
IsViewport()
```

Retrieve whether the nodes are being evaluated for the viewport rather than the final render

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.IsViewport.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.IsViewport.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.IsViewport.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.IsViewport.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.IsViewport.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.IsViewport.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.IsViewport.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.IsViewport.type)       |             |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.is_viewport` | `BooleanSocket` | Is Viewport |

### MaterialIndex

``` python
MaterialIndex()
```

Retrieve the index of the material used for each element in the geometry’s list of materials

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.MaterialIndex.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.MaterialIndex.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.MaterialIndex.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.MaterialIndex.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.MaterialIndex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.MaterialIndex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.MaterialIndex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.MaterialIndex.type) |  |

**Outputs**

| Attribute          | Type            | Description    |
|--------------------|-----------------|----------------|
| `o.material_index` | `IntegerSocket` | Material Index |

### MeshIsland

``` python
MeshIsland()
```

Retrieve information about separate connected regions in a mesh

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.MeshIsland.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.MeshIsland.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.MeshIsland.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.MeshIsland.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.MeshIsland.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.MeshIsland.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.MeshIsland.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.MeshIsland.type)       |             |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.island_index` | `IntegerSocket` | Island Index |
| `o.island_count` | `IntegerSocket` | Island Count |

### MousePosition

``` python
MousePosition()
```

Retrieve the position of the mouse cursor

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.MousePosition.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.MousePosition.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.MousePosition.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.MousePosition.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.MousePosition.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.MousePosition.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.MousePosition.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.MousePosition.type) |  |

**Outputs**

| Attribute         | Type            | Description   |
|-------------------|-----------------|---------------|
| `o.mouse_x`       | `IntegerSocket` | Mouse X       |
| `o.mouse_y`       | `IntegerSocket` | Mouse Y       |
| `o.region_width`  | `IntegerSocket` | Region Width  |
| `o.region_height` | `IntegerSocket` | Region Height |

### NamedAttribute

``` python
NamedAttribute(name='', *, data_type='FLOAT')
```

Retrieve the data of a specified attribute

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| name | InputString | Name        | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.input.NamedAttribute.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.input.NamedAttribute.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.NamedAttribute.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.NamedAttribute.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.NamedAttribute.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.NamedAttribute.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.NamedAttribute.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.NamedAttribute.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.NamedAttribute.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.input.NamedAttribute.boolean) | Create Named Attribute with operation ‘Boolean’. True or false |
| [color](#nodebpy.nodes.geometry.input.NamedAttribute.color) | Create Named Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values |
| [float](#nodebpy.nodes.geometry.input.NamedAttribute.float) | Create Named Attribute with operation ‘Float’. Floating-point value |
| [input_4x4_matrix](#nodebpy.nodes.geometry.input.NamedAttribute.input_4x4_matrix) | Create Named Attribute with operation ‘4x4 Matrix’. Floating point matrix |
| [integer](#nodebpy.nodes.geometry.input.NamedAttribute.integer) | Create Named Attribute with operation ‘Integer’. 32-bit integer |
| [quaternion](#nodebpy.nodes.geometry.input.NamedAttribute.quaternion) | Create Named Attribute with operation ‘Quaternion’. Floating point quaternion rotation |
| [vector](#nodebpy.nodes.geometry.input.NamedAttribute.vector) | Create Named Attribute with operation ‘Vector’. 3D vector with floating-point values |

##### boolean

``` python
boolean(name='')
```

Create Named Attribute with operation ‘Boolean’. True or false

##### color

``` python
color(name='')
```

Create Named Attribute with operation ‘Color’. RGBA color with 32-bit floating-point values

##### float

``` python
float(name='')
```

Create Named Attribute with operation ‘Float’. Floating-point value

##### input_4x4_matrix

``` python
input_4x4_matrix(name='')
```

Create Named Attribute with operation ‘4x4 Matrix’. Floating point matrix

##### integer

``` python
integer(name='')
```

Create Named Attribute with operation ‘Integer’. 32-bit integer

##### quaternion

``` python
quaternion(name='')
```

Create Named Attribute with operation ‘Quaternion’. Floating point quaternion rotation

##### vector

``` python
vector(name='')
```

Create Named Attribute with operation ‘Vector’. 3D vector with floating-point values

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.name`  | `StringSocket` | Name        |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.attribute` | `FloatSocket`   | Attribute   |
| `o.exists`    | `BooleanSocket` | Exists      |

### NamedLayerSelection

``` python
NamedLayerSelection(name='')
```

Output a selection of a Grease Pencil layer

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| name | InputString | Name        | `''`    |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.NamedLayerSelection.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.NamedLayerSelection.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.NamedLayerSelection.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.NamedLayerSelection.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.NamedLayerSelection.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.NamedLayerSelection.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.NamedLayerSelection.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.NamedLayerSelection.type) |  |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.name`  | `StringSocket` | Name        |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.selection` | `BooleanSocket` | Selection   |

### Normal

``` python
Normal(legacy_corner_normals=False)
```

Retrieve a unit length vector indicating the direction pointing away from the geometry at each element

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.Normal.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.Normal.inputs) |  |
| [`legacy_corner_normals`](#nodebpy.nodes.geometry.input.Normal.legacy_corner_normals) |  |
| [`name`](#nodebpy.nodes.geometry.input.Normal.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.Normal.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.Normal.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.Normal.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.Normal.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.Normal.type) |  |

**Outputs**

| Attribute       | Type           | Description |
|-----------------|----------------|-------------|
| `o.normal`      | `VectorSocket` | Normal      |
| `o.true_normal` | `VectorSocket` | True Normal |

### ObjectInfo

``` python
ObjectInfo(object=None, as_instance=False, *, transform_space='ORIGINAL')
```

Retrieve information from an object

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| object      | InputObject  | Object      | `None`  |
| as_instance | InputBoolean | As Instance | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.ObjectInfo.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.ObjectInfo.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.ObjectInfo.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.ObjectInfo.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.ObjectInfo.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.ObjectInfo.outputs) |  |
| [`transform_space`](#nodebpy.nodes.geometry.input.ObjectInfo.transform_space) |  |
| [`tree`](#nodebpy.nodes.geometry.input.ObjectInfo.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.ObjectInfo.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.object`      | `ObjectSocket`  | Object      |
| `i.as_instance` | `BooleanSocket` | As Instance |

**Outputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `o.transform` | `MatrixSocket`   | Transform   |
| `o.location`  | `VectorSocket`   | Location    |
| `o.rotation`  | `RotationSocket` | Rotation    |
| `o.scale`     | `VectorSocket`   | Scale       |
| `o.geometry`  | `GeometrySocket` | Geometry    |

### OffsetCornerInFace

``` python
OffsetCornerInFace(corner_index=0, offset=0)
```

Retrieve corners in the same face as another

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| corner_index | InputInteger | Corner Index | `0`     |
| offset       | InputInteger | Offset       | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.OffsetCornerInFace.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.corner_index` | `IntegerSocket` | Corner Index |
| `i.offset`       | `IntegerSocket` | Offset       |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.corner_index` | `IntegerSocket` | Corner Index |

### OffsetPointInCurve

``` python
OffsetPointInCurve(point_index=0, offset=0)
```

Offset a control point index within its curve

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| point_index | InputInteger | Point Index | `0`     |
| offset      | InputInteger | Offset      | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.OffsetPointInCurve.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.point_index` | `IntegerSocket` | Point Index |
| `i.offset`      | `IntegerSocket` | Offset      |

**Outputs**

| Attribute           | Type            | Description     |
|---------------------|-----------------|-----------------|
| `o.is_valid_offset` | `BooleanSocket` | Is Valid Offset |
| `o.point_index`     | `IntegerSocket` | Point Index     |

### PointsOfCurve

``` python
PointsOfCurve(curve_index=0, weights=0.0, sort_index=0)
```

Retrieve a point index within a curve

#### Parameters

| Name        | Type         | Description | Default |
|-------------|--------------|-------------|---------|
| curve_index | InputInteger | Curve Index | `0`     |
| weights     | InputFloat   | Weights     | `0.0`   |
| sort_index  | InputInteger | Sort Index  | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.PointsOfCurve.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.PointsOfCurve.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.PointsOfCurve.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.PointsOfCurve.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.PointsOfCurve.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.PointsOfCurve.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.PointsOfCurve.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.PointsOfCurve.type) |  |

**Inputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `i.curve_index` | `IntegerSocket` | Curve Index |
| `i.weights`     | `FloatSocket`   | Weights     |
| `i.sort_index`  | `IntegerSocket` | Sort Index  |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.point_index` | `IntegerSocket` | Point Index |
| `o.total`       | `IntegerSocket` | Total       |

### Position

``` python
Position()
```

Retrieve a vector indicating the location of each element

#### Attributes

| Name                                                        | Description |
|-------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Position.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Position.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Position.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Position.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Position.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Position.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Position.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Position.type)       |             |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.position` | `VectorSocket` | Position    |

### Radius

``` python
Radius()
```

Retrieve the radius at each point on curve or point cloud geometry

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Radius.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Radius.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Radius.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Radius.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Radius.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Radius.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Radius.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Radius.type)       |             |

**Outputs**

| Attribute  | Type          | Description |
|------------|---------------|-------------|
| `o.radius` | `FloatSocket` | Radius      |

### Rotation

``` python
Rotation(rotation_euler=(0.0, 0.0, 0.0))
```

Provide a rotation value that can be connected to other nodes in the tree

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.Rotation.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.Rotation.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.Rotation.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.Rotation.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.Rotation.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.Rotation.outputs) |  |
| [`rotation_euler`](#nodebpy.nodes.geometry.input.Rotation.rotation_euler) |  |
| [`tree`](#nodebpy.nodes.geometry.input.Rotation.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.Rotation.type) |  |

**Outputs**

| Attribute    | Type             | Description |
|--------------|------------------|-------------|
| `o.rotation` | `RotationSocket` | Rotation    |

### SceneTime

``` python
SceneTime()
```

Retrieve the current time in the scene’s animation in units of seconds or frames

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.SceneTime.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.SceneTime.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.SceneTime.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.SceneTime.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.SceneTime.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.SceneTime.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.SceneTime.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.SceneTime.type)       |             |

**Outputs**

| Attribute   | Type          | Description |
|-------------|---------------|-------------|
| `o.seconds` | `FloatSocket` | Seconds     |
| `o.frame`   | `FloatSocket` | Frame       |

### Selection

``` python
Selection()
```

User selection of the edited geometry, for tool execution

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Selection.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Selection.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Selection.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Selection.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Selection.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Selection.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Selection.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Selection.type)       |             |

**Outputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `o.selection` | `BooleanSocket` | Boolean     |
| `o.float`     | `FloatSocket`   | Float       |

### SelfObject

``` python
SelfObject()
```

Retrieve the object that contains the geometry nodes modifier currently being executed

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.SelfObject.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.SelfObject.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.SelfObject.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.SelfObject.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.SelfObject.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.SelfObject.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.SelfObject.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.SelfObject.type)       |             |

**Outputs**

| Attribute       | Type           | Description |
|-----------------|----------------|-------------|
| `o.self_object` | `ObjectSocket` | Self Object |

### ShortestEdgePaths

``` python
ShortestEdgePaths(end_vertex=False, edge_cost=1.0)
```

Find the shortest paths along mesh edges to selected end vertices, with customizable cost per edge

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| end_vertex | InputBoolean | End Vertex  | `False` |
| edge_cost  | InputFloat   | Edge Cost   | `1.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.ShortestEdgePaths.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.end_vertex` | `BooleanSocket` | End Vertex  |
| `i.edge_cost`  | `FloatSocket`   | Edge Cost   |

**Outputs**

| Attribute             | Type            | Description       |
|-----------------------|-----------------|-------------------|
| `o.next_vertex_index` | `IntegerSocket` | Next Vertex Index |
| `o.total_cost`        | `FloatSocket`   | Total Cost        |

### SpecialCharacters

``` python
SpecialCharacters()
```

Output string characters that cannot be typed directly with the keyboard

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.SpecialCharacters.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.SpecialCharacters.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.SpecialCharacters.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.SpecialCharacters.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.SpecialCharacters.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.SpecialCharacters.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.SpecialCharacters.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.SpecialCharacters.type) |  |

**Outputs**

| Attribute      | Type           | Description |
|----------------|----------------|-------------|
| `o.line_break` | `StringSocket` | Line Break  |
| `o.tab`        | `StringSocket` | Tab         |

### SplineLength

``` python
SplineLength()
```

Retrieve the total length of each spline, as a distance or as a number of points

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.SplineLength.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.SplineLength.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.SplineLength.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.SplineLength.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.SplineLength.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.SplineLength.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.SplineLength.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.SplineLength.type) |  |

**Outputs**

| Attribute       | Type            | Description |
|-----------------|-----------------|-------------|
| `o.length`      | `FloatSocket`   | Length      |
| `o.point_count` | `IntegerSocket` | Point Count |

### SplineParameter

``` python
SplineParameter()
```

Retrieve how far along each spline a control point is

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.SplineParameter.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.SplineParameter.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.SplineParameter.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.SplineParameter.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.SplineParameter.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.SplineParameter.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.SplineParameter.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.SplineParameter.type) |  |

**Outputs**

| Attribute  | Type            | Description |
|------------|-----------------|-------------|
| `o.factor` | `FloatSocket`   | Factor      |
| `o.length` | `FloatSocket`   | Length      |
| `o.index`  | `IntegerSocket` | Index       |

### SplineResolution

``` python
SplineResolution()
```

Retrieve the number of evaluated points that will be generated for every control point on curves

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.SplineResolution.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.SplineResolution.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.SplineResolution.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.SplineResolution.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.SplineResolution.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.SplineResolution.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.SplineResolution.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.SplineResolution.type) |  |

**Outputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `o.resolution` | `IntegerSocket` | Resolution  |

### String

``` python
String(string='')
```

Provide a string value that can be connected to other nodes in the tree

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.String.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.String.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.String.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.String.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.String.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.String.outputs) |             |
| [`string`](#nodebpy.nodes.geometry.input.String.string)   |             |
| [`tree`](#nodebpy.nodes.geometry.input.String.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.String.type)       |             |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.string` | `StringSocket` | String      |

### UVTangent

``` python
UVTangent(method='Exact', uv=None)
```

Generate tangent directions based on a UV map

#### Parameters

| Name   | Type                                    | Description | Default   |
|--------|-----------------------------------------|-------------|-----------|
| method | InputMenu \| Literal\['Exact', 'Fast'\] | Method      | `'Exact'` |
| uv     | InputVector                             | UV          | `None`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.UVTangent.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.UVTangent.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.UVTangent.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.UVTangent.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.UVTangent.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.UVTangent.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.UVTangent.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.UVTangent.type)       |             |

**Inputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `i.method` | `MenuSocket`   | Method      |
| `i.uv`     | `VectorSocket` | UV          |

**Outputs**

| Attribute   | Type           | Description |
|-------------|----------------|-------------|
| `o.tangent` | `VectorSocket` | Tangent     |

### Vector

``` python
Vector(vector=(0.0, 0.0, 0.0))
```

Provide a vector value that can be connected to other nodes in the tree

#### Attributes

| Name                                                      | Description |
|-----------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.Vector.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.Vector.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.Vector.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.Vector.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.Vector.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.Vector.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.Vector.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.Vector.type)       |             |
| [`vector`](#nodebpy.nodes.geometry.input.Vector.vector)   |             |

**Outputs**

| Attribute  | Type           | Description |
|------------|----------------|-------------|
| `o.vector` | `VectorSocket` | Vector      |

### VertexNeighbors

``` python
VertexNeighbors()
```

Retrieve topology information relating to each vertex of a mesh

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.VertexNeighbors.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.VertexNeighbors.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.VertexNeighbors.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.VertexNeighbors.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.VertexNeighbors.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.VertexNeighbors.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.VertexNeighbors.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.VertexNeighbors.type) |  |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.vertex_count` | `IntegerSocket` | Vertex Count |
| `o.face_count`   | `IntegerSocket` | Face Count   |

### VertexOfCorner

``` python
VertexOfCorner(corner_index=0)
```

Retrieve the vertex each face corner is attached to

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| corner_index | InputInteger | Corner Index | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.VertexOfCorner.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.VertexOfCorner.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.VertexOfCorner.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.VertexOfCorner.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.VertexOfCorner.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.VertexOfCorner.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.VertexOfCorner.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.VertexOfCorner.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.corner_index` | `IntegerSocket` | Corner Index |

**Outputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `o.vertex_index` | `IntegerSocket` | Vertex Index |

### ViewportTransform

``` python
ViewportTransform()
```

Retrieve the view direction and location of the 3D viewport

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.input.ViewportTransform.i) |  |
| [`inputs`](#nodebpy.nodes.geometry.input.ViewportTransform.inputs) |  |
| [`name`](#nodebpy.nodes.geometry.input.ViewportTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.input.ViewportTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.input.ViewportTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.input.ViewportTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.input.ViewportTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.input.ViewportTransform.type) |  |

**Outputs**

| Attribute           | Type            | Description     |
|---------------------|-----------------|-----------------|
| `o.projection`      | `MatrixSocket`  | Projection      |
| `o.view`            | `MatrixSocket`  | View            |
| `o.is_orthographic` | `BooleanSocket` | Is Orthographic |

### VoxelIndex

``` python
VoxelIndex()
```

Retrieve the integer coordinates of the voxel that the field is evaluated on

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.input.VoxelIndex.i)             |             |
| [`inputs`](#nodebpy.nodes.geometry.input.VoxelIndex.inputs)   |             |
| [`name`](#nodebpy.nodes.geometry.input.VoxelIndex.name)       |             |
| [`node`](#nodebpy.nodes.geometry.input.VoxelIndex.node)       |             |
| [`o`](#nodebpy.nodes.geometry.input.VoxelIndex.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.input.VoxelIndex.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.input.VoxelIndex.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.input.VoxelIndex.type)       |             |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.x`        | `IntegerSocket` | X           |
| `o.y`        | `IntegerSocket` | Y           |
| `o.z`        | `IntegerSocket` | Z           |
| `o.is_tile`  | `BooleanSocket` | Is Tile     |
| `o.extent_x` | `IntegerSocket` | Extent X    |
| `o.extent_y` | `IntegerSocket` | Extent Y    |
| `o.extent_z` | `IntegerSocket` | Extent Z    |
