# nodes.geometry.grid

`grid`

## Classes

| Name | Description |
|----|----|
| [AdvectGrid](#nodebpy.nodes.geometry.grid.AdvectGrid) | Move grid values through a velocity field using numerical integration. Supports multiple integration schemes for different accuracy and performance trade-offs |
| [ClipGrid](#nodebpy.nodes.geometry.grid.ClipGrid) | Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value. |
| [CubeGridTopology](#nodebpy.nodes.geometry.grid.CubeGridTopology) | Create a boolean grid topology with the given dimensions, for use with the Field to Grid node |
| [DistributePointsInGrid](#nodebpy.nodes.geometry.grid.DistributePointsInGrid) | Generate points inside a volume grid |
| [DistributePointsInVolume](#nodebpy.nodes.geometry.grid.DistributePointsInVolume) | Generate points inside a volume |
| [GetNamedGrid](#nodebpy.nodes.geometry.grid.GetNamedGrid) | Get volume grid from a volume geometry with the specified name |
| [GridCurl](#nodebpy.nodes.geometry.grid.GridCurl) | Calculate the magnitude and direction of circulation of a directional vector grid |
| [GridDilateErode](#nodebpy.nodes.geometry.grid.GridDilateErode) | Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values. |
| [GridDivergence](#nodebpy.nodes.geometry.grid.GridDivergence) | Calculate the flow into and out of each point of a directional vector grid |
| [GridGradient](#nodebpy.nodes.geometry.grid.GridGradient) | Calculate the direction and magnitude of the change in values of a scalar grid |
| [GridInfo](#nodebpy.nodes.geometry.grid.GridInfo) | Retrieve information about a volume grid |
| [GridLaplacian](#nodebpy.nodes.geometry.grid.GridLaplacian) | Compute the divergence of the gradient of the input grid |
| [GridMean](#nodebpy.nodes.geometry.grid.GridMean) | Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [GridMedian](#nodebpy.nodes.geometry.grid.GridMedian) | Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value. |
| [GridToMesh](#nodebpy.nodes.geometry.grid.GridToMesh) | Generate a mesh on the “surface” of a volume grid |
| [GridToPoints](#nodebpy.nodes.geometry.grid.GridToPoints) | Generate a point cloud from a volume grid’s active voxels |
| [MeshToDensityGrid](#nodebpy.nodes.geometry.grid.MeshToDensityGrid) | Create a filled volume grid from a mesh |
| [MeshToSDFGrid](#nodebpy.nodes.geometry.grid.MeshToSDFGrid) | Create a signed distance volume grid from a mesh |
| [MeshToVolume](#nodebpy.nodes.geometry.grid.MeshToVolume) | Create a fog volume with the shape of the input mesh’s surface |
| [PointsToSDFGrid](#nodebpy.nodes.geometry.grid.PointsToSDFGrid) | Create a signed distance volume grid from points |
| [PointsToVolume](#nodebpy.nodes.geometry.grid.PointsToVolume) | Generate a fog volume sphere around every point |
| [PruneGrid](#nodebpy.nodes.geometry.grid.PruneGrid) | Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes |
| [SDFGridFillet](#nodebpy.nodes.geometry.grid.SDFGridFillet) | Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces |
| [SDFGridLaplacian](#nodebpy.nodes.geometry.grid.SDFGridLaplacian) | Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization |
| [SDFGridMean](#nodebpy.nodes.geometry.grid.SDFGridMean) | Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field |
| [SDFGridMeanCurvature](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature) | Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas |
| [SDFGridMedian](#nodebpy.nodes.geometry.grid.SDFGridMedian) | Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field |
| [SDFGridOffset](#nodebpy.nodes.geometry.grid.SDFGridOffset) | Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property |
| [SampleGrid](#nodebpy.nodes.geometry.grid.SampleGrid) | Retrieve values from the specified volume grid |
| [SampleGridIndex](#nodebpy.nodes.geometry.grid.SampleGridIndex) | Retrieve volume grid values at specific voxels |
| [SetGridBackground](#nodebpy.nodes.geometry.grid.SetGridBackground) | Set the background value used for inactive voxels and tiles |
| [SetGridTransform](#nodebpy.nodes.geometry.grid.SetGridTransform) | Set the transform for the grid from index space into object space. |
| [StoreNamedGrid](#nodebpy.nodes.geometry.grid.StoreNamedGrid) | Store grid data in a volume geometry with the specified name |
| [VolumeCube](#nodebpy.nodes.geometry.grid.VolumeCube) | Generate a dense volume with a field that controls the density at each grid voxel based on its position |
| [VolumeToMesh](#nodebpy.nodes.geometry.grid.VolumeToMesh) | Generate a mesh on the “surface” of a volume |
| [VoxelizeGrid](#nodebpy.nodes.geometry.grid.VoxelizeGrid) | Remove sparseness from a volume grid by making the active tiles into voxels |

### AdvectGrid

``` python
AdvectGrid(
    grid=0.0,
    velocity=None,
    time_step=1.0,
    integration_scheme='Runge-Kutta 3',
    limiter='Clamp',
    *,
    data_type='FLOAT',
)
```

Move grid values through a velocity field using numerical integration. Supports multiple integration schemes for different accuracy and performance trade-offs

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| grid | InputFloat | Grid | `0.0` |
| velocity | InputVector | Velocity | `None` |
| time_step | InputFloat | Time Step | `1.0` |
| integration_scheme | InputMenu \| Literal\['Semi-Lagrangian', 'Midpoint', 'Runge-Kutta 3', 'Runge-Kutta 4', 'MacCormack', 'BFECC'\] | Integration Scheme | `'Runge-Kutta 3'` |
| limiter | InputMenu \| Literal\['None', 'Clamp', 'Revert'\] | Limiter | `'Clamp'` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.AdvectGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.AdvectGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.AdvectGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.AdvectGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.AdvectGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.AdvectGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.AdvectGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.AdvectGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.grid.AdvectGrid.float) | Create Advect Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.AdvectGrid.integer) | Create Advect Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.AdvectGrid.vector) | Create Advect Grid with operation ‘Vector’. |

##### float

``` python
float(
    grid=0.0,
    velocity=None,
    time_step=1.0,
    integration_scheme='Runge-Kutta 3',
    limiter='Clamp',
)
```

Create Advect Grid with operation ‘Float’.

##### integer

``` python
integer(
    grid=0,
    velocity=None,
    time_step=1.0,
    integration_scheme='Runge-Kutta 3',
    limiter='Clamp',
)
```

Create Advect Grid with operation ‘Integer’.

##### vector

``` python
vector(
    grid=None,
    velocity=None,
    time_step=1.0,
    integration_scheme='Runge-Kutta 3',
    limiter='Clamp',
)
```

Create Advect Grid with operation ‘Vector’.

**Inputs**

| Attribute              | Type           | Description        |
|------------------------|----------------|--------------------|
| `i.grid`               | `FloatSocket`  | Grid               |
| `i.velocity`           | `VectorSocket` | Velocity           |
| `i.time_step`          | `FloatSocket`  | Time Step          |
| `i.integration_scheme` | `MenuSocket`   | Integration Scheme |
| `i.limiter`            | `MenuSocket`   | Limiter            |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### ClipGrid

``` python
ClipGrid(
    grid=0.0,
    min_x=0,
    min_y=0,
    min_z=0,
    max_x=32,
    max_y=32,
    max_z=32,
    *,
    data_type='FLOAT',
)
```

Deactivate grid voxels outside minimum and maximum coordinates, setting them to the background value.

#### Parameters

| Name  | Type         | Description | Default |
|-------|--------------|-------------|---------|
| grid  | InputFloat   | Grid        | `0.0`   |
| min_x | InputInteger | Min X       | `0`     |
| min_y | InputInteger | Min Y       | `0`     |
| min_z | InputInteger | Min Z       | `0`     |
| max_x | InputInteger | Max X       | `32`    |
| max_y | InputInteger | Max Y       | `32`    |
| max_z | InputInteger | Max Z       | `32`    |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.ClipGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.ClipGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.ClipGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.ClipGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.ClipGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.ClipGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.ClipGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.ClipGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.ClipGrid.boolean) | Create Clip Grid with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.ClipGrid.float) | Create Clip Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.ClipGrid.integer) | Create Clip Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.ClipGrid.vector) | Create Clip Grid with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Create Clip Grid with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Create Clip Grid with operation ‘Float’.

##### integer

``` python
integer(grid=0, min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Create Clip Grid with operation ‘Integer’.

##### vector

``` python
vector(grid=None, min_x=0, min_y=0, min_z=0, max_x=32, max_y=32, max_z=32)
```

Create Clip Grid with operation ‘Vector’.

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.grid`  | `FloatSocket`   | Grid        |
| `i.min_x` | `IntegerSocket` | Min X       |
| `i.min_y` | `IntegerSocket` | Min Y       |
| `i.min_z` | `IntegerSocket` | Min Z       |
| `i.max_x` | `IntegerSocket` | Max X       |
| `i.max_y` | `IntegerSocket` | Max Y       |
| `i.max_z` | `IntegerSocket` | Max Z       |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### CubeGridTopology

``` python
CubeGridTopology(
    bounds_min=None,
    bounds_max=None,
    resolution_x=32,
    resolution_y=32,
    resolution_z=32,
    min_x=0,
    min_y=0,
    min_z=0,
)
```

Create a boolean grid topology with the given dimensions, for use with the Field to Grid node

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| bounds_min   | InputVector  | Bounds Min   | `None`  |
| bounds_max   | InputVector  | Bounds Max   | `None`  |
| resolution_x | InputInteger | Resolution X | `32`    |
| resolution_y | InputInteger | Resolution Y | `32`    |
| resolution_z | InputInteger | Resolution Z | `32`    |
| min_x        | InputInteger | Min X        | `0`     |
| min_y        | InputInteger | Min Y        | `0`     |
| min_z        | InputInteger | Min Z        | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.CubeGridTopology.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.CubeGridTopology.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.CubeGridTopology.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.CubeGridTopology.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.CubeGridTopology.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.CubeGridTopology.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.CubeGridTopology.type) |  |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.bounds_min`   | `VectorSocket`  | Bounds Min   |
| `i.bounds_max`   | `VectorSocket`  | Bounds Max   |
| `i.resolution_x` | `IntegerSocket` | Resolution X |
| `i.resolution_y` | `IntegerSocket` | Resolution Y |
| `i.resolution_z` | `IntegerSocket` | Resolution Z |
| `i.min_x`        | `IntegerSocket` | Min X        |
| `i.min_y`        | `IntegerSocket` | Min Y        |
| `i.min_z`        | `IntegerSocket` | Min Z        |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.topology` | `BooleanSocket` | Topology    |

### DistributePointsInGrid

``` python
DistributePointsInGrid(
    grid=0.0,
    density=1.0,
    seed=0,
    spacing=None,
    threshold=0.1,
    *,
    mode='DENSITY_RANDOM',
)
```

Generate points inside a volume grid

#### Parameters

| Name      | Type         | Description | Default |
|-----------|--------------|-------------|---------|
| grid      | InputFloat   | Grid        | `0.0`   |
| density   | InputFloat   | Density     | `1.0`   |
| seed      | InputInteger | Seed        | `0`     |
| spacing   | InputVector  | Spacing     | `None`  |
| threshold | InputFloat   | Threshold   | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.i) |  |
| [`mode`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.mode) |  |
| [`name`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [grid](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.grid) | Create Distribute Points in Grid with operation ‘Grid’. Distribute the points in a grid pattern inside of the volume |
| [random](#nodebpy.nodes.geometry.grid.DistributePointsInGrid.random) | Create Distribute Points in Grid with operation ‘Random’. Distribute points randomly inside of the volume |

##### grid

``` python
grid(grid=0.0, spacing=None, threshold=0.1)
```

Create Distribute Points in Grid with operation ‘Grid’. Distribute the points in a grid pattern inside of the volume

##### random

``` python
random(grid=0.0, density=1.0, seed=0)
```

Create Distribute Points in Grid with operation ‘Random’. Distribute points randomly inside of the volume

**Inputs**

| Attribute     | Type            | Description |
|---------------|-----------------|-------------|
| `i.grid`      | `FloatSocket`   | Grid        |
| `i.density`   | `FloatSocket`   | Density     |
| `i.seed`      | `IntegerSocket` | Seed        |
| `i.spacing`   | `VectorSocket`  | Spacing     |
| `i.threshold` | `FloatSocket`   | Threshold   |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.points` | `GeometrySocket` | Points      |

### DistributePointsInVolume

``` python
DistributePointsInVolume(
    volume=None,
    mode='Random',
    density=1.0,
    seed=0,
    spacing=None,
    threshold=0.1,
)
```

Generate points inside a volume

#### Parameters

| Name      | Type                                     | Description | Default    |
|-----------|------------------------------------------|-------------|------------|
| volume    | InputGeometry                            | Volume      | `None`     |
| mode      | InputMenu \| Literal\['Random', 'Grid'\] | Mode        | `'Random'` |
| density   | InputFloat                               | Density     | `1.0`      |
| seed      | InputInteger                             | Seed        | `0`        |
| spacing   | InputVector                              | Spacing     | `None`     |
| threshold | InputFloat                               | Threshold   | `0.1`      |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.DistributePointsInVolume.type) |  |

**Inputs**

| Attribute     | Type             | Description |
|---------------|------------------|-------------|
| `i.volume`    | `GeometrySocket` | Volume      |
| `i.mode`      | `MenuSocket`     | Mode        |
| `i.density`   | `FloatSocket`    | Density     |
| `i.seed`      | `IntegerSocket`  | Seed        |
| `i.spacing`   | `VectorSocket`   | Spacing     |
| `i.threshold` | `FloatSocket`    | Threshold   |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.points` | `GeometrySocket` | Points      |

### GetNamedGrid

``` python
GetNamedGrid(volume=None, name='', remove=True, *, data_type='FLOAT')
```

Get volume grid from a volume geometry with the specified name

#### Parameters

| Name   | Type          | Description | Default |
|--------|---------------|-------------|---------|
| volume | InputGeometry | Volume      | `None`  |
| name   | InputString   | Name        | `''`    |
| remove | InputBoolean  | Remove      | `True`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GetNamedGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GetNamedGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GetNamedGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GetNamedGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GetNamedGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GetNamedGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GetNamedGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GetNamedGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.GetNamedGrid.boolean) | Create Get Named Grid with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.GetNamedGrid.float) | Create Get Named Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GetNamedGrid.integer) | Create Get Named Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GetNamedGrid.vector) | Create Get Named Grid with operation ‘Vector’. |

##### boolean

``` python
boolean(volume=None, name='', remove=True)
```

Create Get Named Grid with operation ‘Boolean’.

##### float

``` python
float(volume=None, name='', remove=True)
```

Create Get Named Grid with operation ‘Float’.

##### integer

``` python
integer(volume=None, name='', remove=True)
```

Create Get Named Grid with operation ‘Integer’.

##### vector

``` python
vector(volume=None, name='', remove=True)
```

Create Get Named Grid with operation ‘Vector’.

**Inputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `i.volume` | `GeometrySocket` | Volume      |
| `i.name`   | `StringSocket`   | Name        |
| `i.remove` | `BooleanSocket`  | Remove      |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |
| `o.grid`   | `FloatSocket`    | Grid        |

### GridCurl

``` python
GridCurl(grid=None)
```

Calculate the magnitude and direction of circulation of a directional vector grid

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| grid | InputVector | Grid        | `None`  |

#### Attributes

| Name                                                       | Description |
|------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.grid.GridCurl.i)             |             |
| [`name`](#nodebpy.nodes.geometry.grid.GridCurl.name)       |             |
| [`node`](#nodebpy.nodes.geometry.grid.GridCurl.node)       |             |
| [`o`](#nodebpy.nodes.geometry.grid.GridCurl.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridCurl.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.grid.GridCurl.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.grid.GridCurl.type)       |             |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.grid`  | `VectorSocket` | Grid        |

**Outputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `o.curl`  | `VectorSocket` | Curl        |

### GridDilateErode

``` python
GridDilateErode(
    grid=0.0,
    connectivity='Face',
    tiles='Preserve',
    steps=1,
    *,
    data_type='FLOAT',
)
```

Dilate or erode the active regions of a grid. This changes which voxels are active but does not change their values.

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| grid | InputFloat | Grid | `0.0` |
| connectivity | InputMenu \| Literal\['Face', 'Edge', 'Vertex'\] | Connectivity | `'Face'` |
| tiles | InputMenu \| Literal\['Ignore', 'Expand', 'Preserve'\] | Tiles | `'Preserve'` |
| steps | InputInteger | Steps | `1` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GridDilateErode.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GridDilateErode.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridDilateErode.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridDilateErode.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridDilateErode.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridDilateErode.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridDilateErode.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridDilateErode.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.GridDilateErode.boolean) | Create Grid Dilate & Erode with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.GridDilateErode.float) | Create Grid Dilate & Erode with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GridDilateErode.integer) | Create Grid Dilate & Erode with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GridDilateErode.vector) | Create Grid Dilate & Erode with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, connectivity='Face', tiles='Preserve', steps=1)
```

Create Grid Dilate & Erode with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, connectivity='Face', tiles='Preserve', steps=1)
```

Create Grid Dilate & Erode with operation ‘Float’.

##### integer

``` python
integer(grid=0, connectivity='Face', tiles='Preserve', steps=1)
```

Create Grid Dilate & Erode with operation ‘Integer’.

##### vector

``` python
vector(grid=None, connectivity='Face', tiles='Preserve', steps=1)
```

Create Grid Dilate & Erode with operation ‘Vector’.

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.grid`         | `FloatSocket`   | Grid         |
| `i.connectivity` | `MenuSocket`    | Connectivity |
| `i.tiles`        | `MenuSocket`    | Tiles        |
| `i.steps`        | `IntegerSocket` | Steps        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### GridDivergence

``` python
GridDivergence(grid=None)
```

Calculate the flow into and out of each point of a directional vector grid

#### Parameters

| Name | Type        | Description | Default |
|------|-------------|-------------|---------|
| grid | InputVector | Grid        | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.GridDivergence.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridDivergence.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridDivergence.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridDivergence.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridDivergence.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridDivergence.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridDivergence.type) |  |

**Inputs**

| Attribute | Type           | Description |
|-----------|----------------|-------------|
| `i.grid`  | `VectorSocket` | Grid        |

**Outputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `o.divergence` | `FloatSocket` | Divergence  |

### GridGradient

``` python
GridGradient(grid=0.0)
```

Calculate the direction and magnitude of the change in values of a scalar grid

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| grid | InputFloat | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.GridGradient.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridGradient.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridGradient.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridGradient.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridGradient.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridGradient.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridGradient.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.grid`  | `FloatSocket` | Grid        |

**Outputs**

| Attribute    | Type           | Description |
|--------------|----------------|-------------|
| `o.gradient` | `VectorSocket` | Gradient    |

### GridInfo

``` python
GridInfo(grid=0.0, *, data_type='FLOAT')
```

Retrieve information about a volume grid

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| grid | InputFloat | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GridInfo.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GridInfo.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridInfo.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridInfo.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridInfo.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridInfo.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridInfo.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridInfo.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.GridInfo.boolean) | Create Grid Info with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.GridInfo.float) | Create Grid Info with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GridInfo.integer) | Create Grid Info with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GridInfo.vector) | Create Grid Info with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False)
```

Create Grid Info with operation ‘Boolean’.

##### float

``` python
float(grid=0.0)
```

Create Grid Info with operation ‘Float’.

##### integer

``` python
integer(grid=0)
```

Create Grid Info with operation ‘Integer’.

##### vector

``` python
vector(grid=None)
```

Create Grid Info with operation ‘Vector’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.grid`  | `FloatSocket` | Grid        |

**Outputs**

| Attribute            | Type           | Description      |
|----------------------|----------------|------------------|
| `o.transform`        | `MatrixSocket` | Transform        |
| `o.background_value` | `FloatSocket`  | Background Value |

### GridLaplacian

``` python
GridLaplacian(grid=0.0)
```

Compute the divergence of the gradient of the input grid

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| grid | InputFloat | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.GridLaplacian.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridLaplacian.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridLaplacian.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridLaplacian.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridLaplacian.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridLaplacian.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridLaplacian.type) |  |

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.grid`  | `FloatSocket` | Grid        |

**Outputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `o.laplacian` | `FloatSocket` | Laplacian   |

### GridMean

``` python
GridMean(grid=0.0, width=1, iterations=1, *, data_type='FLOAT')
```

Apply mean (box) filter smoothing to a voxel. The mean value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| width      | InputInteger | Width       | `1`     |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GridMean.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GridMean.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridMean.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridMean.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridMean.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridMean.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridMean.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridMean.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.grid.GridMean.float) | Create Grid Mean with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GridMean.integer) | Create Grid Mean with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GridMean.vector) | Create Grid Mean with operation ‘Vector’. |

##### float

``` python
float(grid=0.0, width=1, iterations=1)
```

Create Grid Mean with operation ‘Float’.

##### integer

``` python
integer(grid=0, width=1, iterations=1)
```

Create Grid Mean with operation ‘Integer’.

##### vector

``` python
vector(grid=None, width=1, iterations=1)
```

Create Grid Mean with operation ‘Vector’.

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.width`      | `IntegerSocket` | Width       |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### GridMedian

``` python
GridMedian(grid=0.0, width=1, iterations=1, *, data_type='FLOAT')
```

Apply median (box) filter smoothing to a voxel. The median value from surrounding voxels in a box-shape defined by the radius replaces the voxel value.

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| width      | InputInteger | Width       | `1`     |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GridMedian.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GridMedian.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridMedian.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridMedian.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridMedian.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridMedian.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridMedian.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridMedian.type) |  |

#### Methods

| Name | Description |
|----|----|
| [float](#nodebpy.nodes.geometry.grid.GridMedian.float) | Create Grid Median with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GridMedian.integer) | Create Grid Median with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GridMedian.vector) | Create Grid Median with operation ‘Vector’. |

##### float

``` python
float(grid=0.0, width=1, iterations=1)
```

Create Grid Median with operation ‘Float’.

##### integer

``` python
integer(grid=0, width=1, iterations=1)
```

Create Grid Median with operation ‘Integer’.

##### vector

``` python
vector(grid=None, width=1, iterations=1)
```

Create Grid Median with operation ‘Vector’.

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.width`      | `IntegerSocket` | Width       |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### GridToMesh

``` python
GridToMesh(grid=0.0, threshold=0.1, adaptivity=0.0)
```

Generate a mesh on the “surface” of a volume grid

#### Parameters

| Name       | Type       | Description | Default |
|------------|------------|-------------|---------|
| grid       | InputFloat | Grid        | `0.0`   |
| threshold  | InputFloat | Threshold   | `0.1`   |
| adaptivity | InputFloat | Adaptivity  | `0.0`   |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.grid.GridToMesh.i)             |             |
| [`name`](#nodebpy.nodes.geometry.grid.GridToMesh.name)       |             |
| [`node`](#nodebpy.nodes.geometry.grid.GridToMesh.node)       |             |
| [`o`](#nodebpy.nodes.geometry.grid.GridToMesh.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridToMesh.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.grid.GridToMesh.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.grid.GridToMesh.type)       |             |

**Inputs**

| Attribute      | Type          | Description |
|----------------|---------------|-------------|
| `i.grid`       | `FloatSocket` | Grid        |
| `i.threshold`  | `FloatSocket` | Threshold   |
| `i.adaptivity` | `FloatSocket` | Adaptivity  |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### GridToPoints

``` python
GridToPoints(grid=0.0, *, data_type='FLOAT')
```

Generate a point cloud from a volume grid’s active voxels

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| grid | InputFloat | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.GridToPoints.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.GridToPoints.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.GridToPoints.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.GridToPoints.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.GridToPoints.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.GridToPoints.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.GridToPoints.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.GridToPoints.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.GridToPoints.boolean) | Create Grid to Points with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.GridToPoints.float) | Create Grid to Points with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.GridToPoints.integer) | Create Grid to Points with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.GridToPoints.vector) | Create Grid to Points with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False)
```

Create Grid to Points with operation ‘Boolean’.

##### float

``` python
float(grid=0.0)
```

Create Grid to Points with operation ‘Float’.

##### integer

``` python
integer(grid=0)
```

Create Grid to Points with operation ‘Integer’.

##### vector

``` python
vector(grid=None)
```

Create Grid to Points with operation ‘Vector’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.grid`  | `FloatSocket` | Grid        |

**Outputs**

| Attribute   | Type             | Description |
|-------------|------------------|-------------|
| `o.points`  | `GeometrySocket` | Points      |
| `o.value`   | `FloatSocket`    | Value       |
| `o.x`       | `IntegerSocket`  | X           |
| `o.y`       | `IntegerSocket`  | Y           |
| `o.z`       | `IntegerSocket`  | Z           |
| `o.is_tile` | `BooleanSocket`  | Is Tile     |
| `o.extent`  | `IntegerSocket`  | Extent      |

### MeshToDensityGrid

``` python
MeshToDensityGrid(mesh=None, density=1.0, voxel_size=0.3, gradient_width=0.2)
```

Create a filled volume grid from a mesh

#### Parameters

| Name           | Type          | Description    | Default |
|----------------|---------------|----------------|---------|
| mesh           | InputGeometry | Mesh           | `None`  |
| density        | InputFloat    | Density        | `1.0`   |
| voxel_size     | InputFloat    | Voxel Size     | `0.3`   |
| gradient_width | InputFloat    | Gradient Width | `0.2`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.MeshToDensityGrid.type) |  |

**Inputs**

| Attribute          | Type             | Description    |
|--------------------|------------------|----------------|
| `i.mesh`           | `GeometrySocket` | Mesh           |
| `i.density`        | `FloatSocket`    | Density        |
| `i.voxel_size`     | `FloatSocket`    | Voxel Size     |
| `i.gradient_width` | `FloatSocket`    | Gradient Width |

**Outputs**

| Attribute        | Type          | Description  |
|------------------|---------------|--------------|
| `o.density_grid` | `FloatSocket` | Density Grid |

### MeshToSDFGrid

``` python
MeshToSDFGrid(mesh=None, voxel_size=0.3, band_width=3)
```

Create a signed distance volume grid from a mesh

#### Parameters

| Name       | Type          | Description | Default |
|------------|---------------|-------------|---------|
| mesh       | InputGeometry | Mesh        | `None`  |
| voxel_size | InputFloat    | Voxel Size  | `0.3`   |
| band_width | InputInteger  | Band Width  | `3`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.MeshToSDFGrid.type) |  |

**Inputs**

| Attribute      | Type             | Description |
|----------------|------------------|-------------|
| `i.mesh`       | `GeometrySocket` | Mesh        |
| `i.voxel_size` | `FloatSocket`    | Voxel Size  |
| `i.band_width` | `IntegerSocket`  | Band Width  |

**Outputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `o.sdf_grid` | `FloatSocket` | SDF Grid    |

### MeshToVolume

``` python
MeshToVolume(
    mesh=None,
    density=1.0,
    resolution_mode='Amount',
    voxel_size=0.3,
    voxel_amount=64.0,
    interior_band_width=0.2,
)
```

Create a fog volume with the shape of the input mesh’s surface

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| mesh | InputGeometry | Mesh | `None` |
| density | InputFloat | Density | `1.0` |
| resolution_mode | InputMenu \| Literal\['Amount', 'Size'\] | Resolution Mode | `'Amount'` |
| voxel_size | InputFloat | Voxel Size | `0.3` |
| voxel_amount | InputFloat | Voxel Amount | `64.0` |
| interior_band_width | InputFloat | Interior Band Width | `0.2` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.MeshToVolume.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.MeshToVolume.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.MeshToVolume.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.MeshToVolume.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.MeshToVolume.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.MeshToVolume.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.MeshToVolume.type) |  |

**Inputs**

| Attribute               | Type             | Description         |
|-------------------------|------------------|---------------------|
| `i.mesh`                | `GeometrySocket` | Mesh                |
| `i.density`             | `FloatSocket`    | Density             |
| `i.resolution_mode`     | `MenuSocket`     | Resolution Mode     |
| `i.voxel_size`          | `FloatSocket`    | Voxel Size          |
| `i.voxel_amount`        | `FloatSocket`    | Voxel Amount        |
| `i.interior_band_width` | `FloatSocket`    | Interior Band Width |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |

### PointsToSDFGrid

``` python
PointsToSDFGrid(points=None, radius=0.5, voxel_size=0.3)
```

Create a signed distance volume grid from points

#### Parameters

| Name       | Type          | Description | Default |
|------------|---------------|-------------|---------|
| points     | InputGeometry | Points      | `None`  |
| radius     | InputFloat    | Radius      | `0.5`   |
| voxel_size | InputFloat    | Voxel Size  | `0.3`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.PointsToSDFGrid.type) |  |

**Inputs**

| Attribute      | Type             | Description |
|----------------|------------------|-------------|
| `i.points`     | `GeometrySocket` | Points      |
| `i.radius`     | `FloatSocket`    | Radius      |
| `i.voxel_size` | `FloatSocket`    | Voxel Size  |

**Outputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `o.sdf_grid` | `FloatSocket` | SDF Grid    |

### PointsToVolume

``` python
PointsToVolume(
    points=None,
    density=1.0,
    resolution_mode='Amount',
    voxel_size=0.3,
    voxel_amount=64.0,
    radius=0.5,
)
```

Generate a fog volume sphere around every point

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| points | InputGeometry | Points | `None` |
| density | InputFloat | Density | `1.0` |
| resolution_mode | InputMenu \| Literal\['Amount', 'Size'\] | Resolution Mode | `'Amount'` |
| voxel_size | InputFloat | Voxel Size | `0.3` |
| voxel_amount | InputFloat | Voxel Amount | `64.0` |
| radius | InputFloat | Radius | `0.5` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.PointsToVolume.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.PointsToVolume.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.PointsToVolume.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.PointsToVolume.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.PointsToVolume.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.PointsToVolume.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.PointsToVolume.type) |  |

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.points`          | `GeometrySocket` | Points          |
| `i.density`         | `FloatSocket`    | Density         |
| `i.resolution_mode` | `MenuSocket`     | Resolution Mode |
| `i.voxel_size`      | `FloatSocket`    | Voxel Size      |
| `i.voxel_amount`    | `FloatSocket`    | Voxel Amount    |
| `i.radius`          | `FloatSocket`    | Radius          |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |

### PruneGrid

``` python
PruneGrid(grid=0.0, mode='Threshold', threshold=0.01, *, data_type='FLOAT')
```

Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| grid | InputFloat | Grid | `0.0` |
| mode | InputMenu \| Literal\['Inactive', 'Threshold', 'SDF'\] | Mode | `'Threshold'` |
| threshold | InputFloat | Threshold | `0.01` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.PruneGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.PruneGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.PruneGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.PruneGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.PruneGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.PruneGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.PruneGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.PruneGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.PruneGrid.boolean) | Create Prune Grid with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.PruneGrid.float) | Create Prune Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.PruneGrid.integer) | Create Prune Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.PruneGrid.vector) | Create Prune Grid with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, mode='Threshold')
```

Create Prune Grid with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, mode='Threshold', threshold=0.01)
```

Create Prune Grid with operation ‘Float’.

##### integer

``` python
integer(grid=0, mode='Threshold', threshold=0)
```

Create Prune Grid with operation ‘Integer’.

##### vector

``` python
vector(grid=None, mode='Threshold', threshold=None)
```

Create Prune Grid with operation ‘Vector’.

**Inputs**

| Attribute     | Type          | Description |
|---------------|---------------|-------------|
| `i.grid`      | `FloatSocket` | Grid        |
| `i.mode`      | `MenuSocket`  | Mode        |
| `i.threshold` | `FloatSocket` | Threshold   |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridFillet

``` python
SDFGridFillet(grid=0.0, iterations=1)
```

Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridFillet.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridFillet.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridFillet.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridFillet.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridFillet.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridFillet.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridFillet.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridLaplacian

``` python
SDFGridLaplacian(grid=0.0, iterations=1)
```

Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridLaplacian.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridMean

``` python
SDFGridMean(grid=0.0, width=1, iterations=1)
```

Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| width      | InputInteger | Width       | `1`     |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name                                                          | Description |
|---------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridMean.i)             |             |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridMean.name)       |             |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridMean.node)       |             |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridMean.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridMean.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridMean.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridMean.type)       |             |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.width`      | `IntegerSocket` | Width       |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridMeanCurvature

``` python
SDFGridMeanCurvature(grid=0.0, iterations=1)
```

Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridMeanCurvature.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridMedian

``` python
SDFGridMedian(grid=0.0, width=1, iterations=1)
```

Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field

#### Parameters

| Name       | Type         | Description | Default |
|------------|--------------|-------------|---------|
| grid       | InputFloat   | Grid        | `0.0`   |
| width      | InputInteger | Width       | `1`     |
| iterations | InputInteger | Iterations  | `1`     |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridMedian.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridMedian.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridMedian.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridMedian.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridMedian.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridMedian.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridMedian.type) |  |

**Inputs**

| Attribute      | Type            | Description |
|----------------|-----------------|-------------|
| `i.grid`       | `FloatSocket`   | Grid        |
| `i.width`      | `IntegerSocket` | Width       |
| `i.iterations` | `IntegerSocket` | Iterations  |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SDFGridOffset

``` python
SDFGridOffset(grid=0.0, distance=0.1)
```

Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property

#### Parameters

| Name     | Type       | Description | Default |
|----------|------------|-------------|---------|
| grid     | InputFloat | Grid        | `0.0`   |
| distance | InputFloat | Distance    | `0.1`   |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.SDFGridOffset.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SDFGridOffset.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SDFGridOffset.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SDFGridOffset.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SDFGridOffset.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SDFGridOffset.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SDFGridOffset.type) |  |

**Inputs**

| Attribute    | Type          | Description |
|--------------|---------------|-------------|
| `i.grid`     | `FloatSocket` | Grid        |
| `i.distance` | `FloatSocket` | Distance    |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SampleGrid

``` python
SampleGrid(
    grid=0.0,
    position=None,
    interpolation='Trilinear',
    *,
    data_type='FLOAT',
)
```

Retrieve values from the specified volume grid

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| grid | InputFloat | Grid | `0.0` |
| position | InputVector | Position | `None` |
| interpolation | InputMenu \| Literal\['Nearest Neighbor', 'Trilinear', 'Triquadratic'\] | Interpolation | `'Trilinear'` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.SampleGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.SampleGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SampleGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SampleGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SampleGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SampleGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SampleGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SampleGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.SampleGrid.boolean) | Create Sample Grid with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.SampleGrid.float) | Create Sample Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.SampleGrid.integer) | Create Sample Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.SampleGrid.vector) | Create Sample Grid with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, position=None, interpolation='Trilinear')
```

Create Sample Grid with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, position=None, interpolation='Trilinear')
```

Create Sample Grid with operation ‘Float’.

##### integer

``` python
integer(grid=0, position=None, interpolation='Trilinear')
```

Create Sample Grid with operation ‘Integer’.

##### vector

``` python
vector(grid=None, position=None, interpolation='Trilinear')
```

Create Sample Grid with operation ‘Vector’.

**Inputs**

| Attribute         | Type           | Description   |
|-------------------|----------------|---------------|
| `i.grid`          | `FloatSocket`  | Grid          |
| `i.position`      | `VectorSocket` | Position      |
| `i.interpolation` | `MenuSocket`   | Interpolation |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### SampleGridIndex

``` python
SampleGridIndex(grid=0.0, x=0, y=0, z=0, *, data_type='FLOAT')
```

Retrieve volume grid values at specific voxels

#### Parameters

| Name | Type         | Description | Default |
|------|--------------|-------------|---------|
| grid | InputFloat   | Grid        | `0.0`   |
| x    | InputInteger | X           | `0`     |
| y    | InputInteger | Y           | `0`     |
| z    | InputInteger | Z           | `0`     |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.SampleGridIndex.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.SampleGridIndex.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SampleGridIndex.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SampleGridIndex.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SampleGridIndex.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SampleGridIndex.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SampleGridIndex.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SampleGridIndex.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.SampleGridIndex.boolean) | Create Sample Grid Index with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.SampleGridIndex.float) | Create Sample Grid Index with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.SampleGridIndex.integer) | Create Sample Grid Index with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.SampleGridIndex.vector) | Create Sample Grid Index with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, x=0, y=0, z=0)
```

Create Sample Grid Index with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, x=0, y=0, z=0)
```

Create Sample Grid Index with operation ‘Float’.

##### integer

``` python
integer(grid=0, x=0, y=0, z=0)
```

Create Sample Grid Index with operation ‘Integer’.

##### vector

``` python
vector(grid=None, x=0, y=0, z=0)
```

Create Sample Grid Index with operation ‘Vector’.

**Inputs**

| Attribute | Type            | Description |
|-----------|-----------------|-------------|
| `i.grid`  | `FloatSocket`   | Grid        |
| `i.x`     | `IntegerSocket` | X           |
| `i.y`     | `IntegerSocket` | Y           |
| `i.z`     | `IntegerSocket` | Z           |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.value` | `FloatSocket` | Value       |

### SetGridBackground

``` python
SetGridBackground(
    grid=0.0,
    background=0.0,
    update_inactive=False,
    *,
    data_type='FLOAT',
)
```

Set the background value used for inactive voxels and tiles

#### Parameters

| Name            | Type         | Description     | Default |
|-----------------|--------------|-----------------|---------|
| grid            | InputFloat   | Grid            | `0.0`   |
| background      | InputFloat   | Background      | `0.0`   |
| update_inactive | InputBoolean | Update Inactive | `False` |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.SetGridBackground.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.SetGridBackground.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SetGridBackground.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SetGridBackground.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SetGridBackground.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SetGridBackground.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SetGridBackground.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SetGridBackground.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.SetGridBackground.boolean) | Create Set Grid Background with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.SetGridBackground.float) | Create Set Grid Background with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.SetGridBackground.integer) | Create Set Grid Background with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.SetGridBackground.vector) | Create Set Grid Background with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, background=False, update_inactive=False)
```

Create Set Grid Background with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, background=0.0, update_inactive=False)
```

Create Set Grid Background with operation ‘Float’.

##### integer

``` python
integer(grid=0, background=0, update_inactive=False)
```

Create Set Grid Background with operation ‘Integer’.

##### vector

``` python
vector(grid=None, background=None, update_inactive=False)
```

Create Set Grid Background with operation ‘Vector’.

**Inputs**

| Attribute           | Type            | Description     |
|---------------------|-----------------|-----------------|
| `i.grid`            | `FloatSocket`   | Grid            |
| `i.background`      | `FloatSocket`   | Background      |
| `i.update_inactive` | `BooleanSocket` | Update Inactive |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |

### SetGridTransform

``` python
SetGridTransform(grid=0.0, transform=None, *, data_type='FLOAT')
```

Set the transform for the grid from index space into object space.

#### Parameters

| Name      | Type        | Description | Default |
|-----------|-------------|-------------|---------|
| grid      | InputFloat  | Grid        | `0.0`   |
| transform | InputMatrix | Transform   | `None`  |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.SetGridTransform.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.SetGridTransform.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.SetGridTransform.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.SetGridTransform.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.SetGridTransform.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.SetGridTransform.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.SetGridTransform.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.SetGridTransform.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.SetGridTransform.boolean) | Create Set Grid Transform with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.SetGridTransform.float) | Create Set Grid Transform with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.SetGridTransform.integer) | Create Set Grid Transform with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.SetGridTransform.vector) | Create Set Grid Transform with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False, transform=None)
```

Create Set Grid Transform with operation ‘Boolean’.

##### float

``` python
float(grid=0.0, transform=None)
```

Create Set Grid Transform with operation ‘Float’.

##### integer

``` python
integer(grid=0, transform=None)
```

Create Set Grid Transform with operation ‘Integer’.

##### vector

``` python
vector(grid=None, transform=None)
```

Create Set Grid Transform with operation ‘Vector’.

**Inputs**

| Attribute     | Type           | Description |
|---------------|----------------|-------------|
| `i.grid`      | `FloatSocket`  | Grid        |
| `i.transform` | `MatrixSocket` | Transform   |

**Outputs**

| Attribute    | Type            | Description |
|--------------|-----------------|-------------|
| `o.is_valid` | `BooleanSocket` | Is Valid    |
| `o.grid`     | `FloatSocket`   | Grid        |

### StoreNamedGrid

``` python
StoreNamedGrid(volume=None, name='', grid=0.0, *, data_type='FLOAT')
```

Store grid data in a volume geometry with the specified name

#### Parameters

| Name   | Type          | Description | Default |
|--------|---------------|-------------|---------|
| volume | InputGeometry | Volume      | `None`  |
| name   | InputString   | Name        | `''`    |
| grid   | InputFloat    | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.StoreNamedGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.StoreNamedGrid.boolean) | Create Store Named Grid with operation ‘Boolean’. Boolean |
| [float](#nodebpy.nodes.geometry.grid.StoreNamedGrid.float) | Create Store Named Grid with operation ‘Float’. Single precision float |
| [integer](#nodebpy.nodes.geometry.grid.StoreNamedGrid.integer) | Create Store Named Grid with operation ‘Integer’. 32-bit integer |
| [vector](#nodebpy.nodes.geometry.grid.StoreNamedGrid.vector) | Create Store Named Grid with operation ‘Vector’. 3D float vector |

##### boolean

``` python
boolean(volume=None, name='', grid=False)
```

Create Store Named Grid with operation ‘Boolean’. Boolean

##### float

``` python
float(volume=None, name='', grid=0.0)
```

Create Store Named Grid with operation ‘Float’. Single precision float

##### integer

``` python
integer(volume=None, name='', grid=0)
```

Create Store Named Grid with operation ‘Integer’. 32-bit integer

##### vector

``` python
vector(volume=None, name='', grid=None)
```

Create Store Named Grid with operation ‘Vector’. 3D float vector

**Inputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `i.volume` | `GeometrySocket` | Volume      |
| `i.name`   | `StringSocket`   | Name        |
| `i.grid`   | `FloatSocket`    | Grid        |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |

### VolumeCube

``` python
VolumeCube(
    density=1.0,
    background=0.0,
    min=None,
    max=None,
    resolution_x=32,
    resolution_y=32,
    resolution_z=32,
)
```

Generate a dense volume with a field that controls the density at each grid voxel based on its position

#### Parameters

| Name         | Type         | Description  | Default |
|--------------|--------------|--------------|---------|
| density      | InputFloat   | Density      | `1.0`   |
| background   | InputFloat   | Background   | `0.0`   |
| min          | InputVector  | Min          | `None`  |
| max          | InputVector  | Max          | `None`  |
| resolution_x | InputInteger | Resolution X | `32`    |
| resolution_y | InputInteger | Resolution Y | `32`    |
| resolution_z | InputInteger | Resolution Z | `32`    |

#### Attributes

| Name                                                         | Description |
|--------------------------------------------------------------|-------------|
| [`i`](#nodebpy.nodes.geometry.grid.VolumeCube.i)             |             |
| [`name`](#nodebpy.nodes.geometry.grid.VolumeCube.name)       |             |
| [`node`](#nodebpy.nodes.geometry.grid.VolumeCube.node)       |             |
| [`o`](#nodebpy.nodes.geometry.grid.VolumeCube.o)             |             |
| [`outputs`](#nodebpy.nodes.geometry.grid.VolumeCube.outputs) |             |
| [`tree`](#nodebpy.nodes.geometry.grid.VolumeCube.tree)       |             |
| [`type`](#nodebpy.nodes.geometry.grid.VolumeCube.type)       |             |

**Inputs**

| Attribute        | Type            | Description  |
|------------------|-----------------|--------------|
| `i.density`      | `FloatSocket`   | Density      |
| `i.background`   | `FloatSocket`   | Background   |
| `i.min`          | `VectorSocket`  | Min          |
| `i.max`          | `VectorSocket`  | Max          |
| `i.resolution_x` | `IntegerSocket` | Resolution X |
| `i.resolution_y` | `IntegerSocket` | Resolution Y |
| `i.resolution_z` | `IntegerSocket` | Resolution Z |

**Outputs**

| Attribute  | Type             | Description |
|------------|------------------|-------------|
| `o.volume` | `GeometrySocket` | Volume      |

### VolumeToMesh

``` python
VolumeToMesh(
    volume=None,
    resolution_mode='Grid',
    voxel_size=0.3,
    voxel_amount=64.0,
    threshold=0.1,
    adaptivity=0.0,
)
```

Generate a mesh on the “surface” of a volume

#### Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| volume | InputGeometry | Volume | `None` |
| resolution_mode | InputMenu \| Literal\['Grid', 'Amount', 'Size'\] | Resolution Mode | `'Grid'` |
| voxel_size | InputFloat | Voxel Size | `0.3` |
| voxel_amount | InputFloat | Voxel Amount | `64.0` |
| threshold | InputFloat | Threshold | `0.1` |
| adaptivity | InputFloat | Adaptivity | `0.0` |

#### Attributes

| Name | Description |
|----|----|
| [`i`](#nodebpy.nodes.geometry.grid.VolumeToMesh.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.VolumeToMesh.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.VolumeToMesh.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.VolumeToMesh.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.VolumeToMesh.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.VolumeToMesh.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.VolumeToMesh.type) |  |

**Inputs**

| Attribute           | Type             | Description     |
|---------------------|------------------|-----------------|
| `i.volume`          | `GeometrySocket` | Volume          |
| `i.resolution_mode` | `MenuSocket`     | Resolution Mode |
| `i.voxel_size`      | `FloatSocket`    | Voxel Size      |
| `i.voxel_amount`    | `FloatSocket`    | Voxel Amount    |
| `i.threshold`       | `FloatSocket`    | Threshold       |
| `i.adaptivity`      | `FloatSocket`    | Adaptivity      |

**Outputs**

| Attribute | Type             | Description |
|-----------|------------------|-------------|
| `o.mesh`  | `GeometrySocket` | Mesh        |

### VoxelizeGrid

``` python
VoxelizeGrid(grid=0.0, *, data_type='FLOAT')
```

Remove sparseness from a volume grid by making the active tiles into voxels

#### Parameters

| Name | Type       | Description | Default |
|------|------------|-------------|---------|
| grid | InputFloat | Grid        | `0.0`   |

#### Attributes

| Name | Description |
|----|----|
| [`data_type`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.data_type) |  |
| [`i`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.i) |  |
| [`name`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.name) |  |
| [`node`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.node) |  |
| [`o`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.o) |  |
| [`outputs`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.outputs) |  |
| [`tree`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.tree) |  |
| [`type`](#nodebpy.nodes.geometry.grid.VoxelizeGrid.type) |  |

#### Methods

| Name | Description |
|----|----|
| [boolean](#nodebpy.nodes.geometry.grid.VoxelizeGrid.boolean) | Create Voxelize Grid with operation ‘Boolean’. |
| [float](#nodebpy.nodes.geometry.grid.VoxelizeGrid.float) | Create Voxelize Grid with operation ‘Float’. |
| [integer](#nodebpy.nodes.geometry.grid.VoxelizeGrid.integer) | Create Voxelize Grid with operation ‘Integer’. |
| [vector](#nodebpy.nodes.geometry.grid.VoxelizeGrid.vector) | Create Voxelize Grid with operation ‘Vector’. |

##### boolean

``` python
boolean(grid=False)
```

Create Voxelize Grid with operation ‘Boolean’.

##### float

``` python
float(grid=0.0)
```

Create Voxelize Grid with operation ‘Float’.

##### integer

``` python
integer(grid=0)
```

Create Voxelize Grid with operation ‘Integer’.

##### vector

``` python
vector(grid=None)
```

Create Voxelize Grid with operation ‘Vector’.

**Inputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `i.grid`  | `FloatSocket` | Grid        |

**Outputs**

| Attribute | Type          | Description |
|-----------|---------------|-------------|
| `o.grid`  | `FloatSocket` | Grid        |
