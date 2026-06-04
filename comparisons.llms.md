# Comapring the API

How does the API compare to other existing solutions?

## `geonodes`

### ‘Hello World’

The hello world example from `geonodes` readme: https://github.com/al1brn/geonodes

## `nodebpy`

``` python
from nodebpy import geometry as g

with g.tree("Hello World") as tree:
    height = tree.inputs.float("Height", 3.0)
    omega = tree.inputs.float("Omega", 2.0)

    with g.Frame("Computing the wave"):
        pos = g.Position().o.position
        distance = g.Math.square_root(pos.x**2 + pos.y**2)
        z = height * g.Math.sine(distance * omega) / distance

    with g.Frame("Point offset & smooth"):
        mesh = (
            g.Grid(20, 20, 200, 200)
            >> g.SetPosition(offset=g.CombineXYZ(z=z))
            >> g.SetShadeSmooth.face()
        )

    mesh >> tree.outputs.geometry("Mesh")
```

## `geonodes`

``` python
from geonodes import *

with GeoNodes("Hello World"):
    height = 3
    omega  = 2

    grid = Mesh.Grid(vertices_x=200, vertices_y=200, size_x=20, size_y=20)
    with Layout("Computing the wave"):
        pos = nd.position
        distance = gnmath.sqrt(pos.x**2 + pos.y**2)
        z = height*gnmath.sin(distance*omega)/distance

    with Layout("Point offset and smoothness"):
        grid.offset = (0, 0, z)
        grid.faces.smooth = True

    grid.out()
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Position"):::input-node
    N2("Separate XYZ"):::converter-node
    N3("Math<br/><small>(POWER)</small>"):::converter-node
    N4("Math<br/><small>(POWER)</small>"):::converter-node
    N5("Math<br/><small>(ADD)</small>"):::converter-node
    N6("Math<br/><small>(SQRT)</small>"):::converter-node
    N7("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N8("Frame"):::default-node
    N9("Frame"):::default-node
    N10("Math<br/><small>(SINE)</small>"):::converter-node
    N11("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N12("Math<br/><small>(DIVIDE)</small>"):::converter-node
    N13("Grid"):::geometry-node
    N14("Combine XYZ"):::converter-node
    N15("Set Position"):::geometry-node
    N16("Set Shade Smooth"):::geometry-node
    N17("Group Output"):::default-node
    N1 -->|"Position->Vector"| N2
    N2 -->|"X->Value"| N3
    N2 -->|"Y->Value"| N4
    N3 -->|"Value->Value"| N5
    N4 -->|"Value->Value"| N5
    N5 -->|"Value->Value"| N6
    N6 -->|"Value->Value"| N7
    N0 -->|"Omega->Value"| N7
    N7 -->|"Value->Value"| N10
    N10 -->|"Value->Value"| N11
    N11 -->|"Value->Value"| N12
    N12 -->|"Value->Z"| N14
    N14 -->|"Vector->Offset"| N15
    N13 -->|"Mesh->Geometry"| N15
    N15 -->|"Geometry->Mesh"| N16
    N16 -->|"Mesh->Mesh"| N17
    N0 -->|"Height->Value"| N11
    N6 -->|"Value->Value"| N12
```

## `geometry-script`

### README Demo

## `nodebpy`

``` python
from nodebpy import geometry as g

with g.tree("Repeat Grid") as tree:
    geometry = tree.inputs.geometry("Geometry")
    width = tree.inputs.integer("Width")
    height = tree.inputs.integer("Height")

    (
        g.Grid(width, height, vertices_x=width, vertices_y=height)
        >> g.MeshToPoints()
        >> g.InstanceOnPoints(instance=geometry)
        >> tree.outputs.geometry("Instances")
    )
```

## `geometry-script`

``` py
from geometry_script import *

@tree("Repeat Grid")
def repeat_grid(geometry: Geometry, width: Int, height: Int):
    g = grid(
        size_x=width, size_y=height,
        vertices_x=width, vertices_y=height
    ).mesh.mesh_to_points()
    return g.instance_on_points(instance=geometry)
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Grid"):::geometry-node
    N2("Mesh to Points"):::geometry-node
    N3("Instance on Points"):::geometry-node
    N4("Group Output"):::default-node
    N0 -->|"Width->Size X"| N1
    N0 -->|"Height->Size Y"| N1
    N0 -->|"Width->Vertices X"| N1
    N0 -->|"Height->Vertices Y"| N1
    N1 -->|"Mesh->Mesh"| N2
    N0 -->|"Geometry->Instance"| N3
    N2 -->|"Points->Points"| N3
    N3 -->|"Instances->Instances"| N4
```

### Primitive Shapes

## `nodebpy`

``` python
with g.tree("Primitive Shapes") as tree:
    (
        g.JoinGeometry([g.Cube(), g.UVSphere(), g.Cylinder()])
        >> tree.outputs.geometry("Result")
    )
```

## `geometry-script`

``` python
@tree("Primitive Shapes")
def primitive_shapes():
    yield cube()
    yield uv_sphere()
    yield cylinder().mesh
```

``` mermaid
graph LR
    N0("Cube"):::geometry-node
    N1("UV Sphere"):::geometry-node
    N2("Cylinder"):::geometry-node
    N3("Join Geometry"):::geometry-node
    N4("Group Output"):::default-node
    N2 -->|"Mesh->Geometry"| N3
    N1 -->|"Mesh->Geometry"| N3
    N0 -->|"Mesh->Geometry"| N3
    N3 -->|"Geometry->Result"| N4
```

### Voxelise

Example script found [here](https://carson-katri.github.io/geometry-script/tutorials/voxelize.html#final-script).

## `nodebpy`

``` python
with g.tree("Voxelise") as tree:
    geo = tree.inputs.geometry("Geometry")
    resolution = tree.inputs.float("Resolution", 0.2)

    (
        geo
        >> g.MeshToVolume(interior_band_width=resolution)
        >> g.DistributePointsInVolume(mode="Grid", spacing=resolution)
        >> g.InstanceOnPoints(instance=g.Cube(size=resolution))
        >> tree.outputs.geometry("Result")
    )
```

## `geometry-script`

``` python
from geometry_script import *

@tree("Voxelize")
def voxelize(geometry: Geometry, resolution: Float = 0.2):
    return geometry.mesh_to_volume(
        interior_band_width=resolution,
        fill_volume=False
    ).distribute_points_in_volume(
        mode=DistributePointsInVolume.Mode.DENSITY_GRID,
        spacing=resolution
    ).instance_on_points(
        instance=cube(size=resolution)
    )
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Mesh to Volume"):::geometry-node
    N2("Distribute Points in Volume"):::geometry-node
    N3("Cube"):::geometry-node
    N4("Instance on Points"):::geometry-node
    N5("Group Output"):::default-node
    N0 -->|"Resolution->Interior Band Width"| N1
    N0 -->|"Geometry->Mesh"| N1
    N1 -->|"Volume->Volume"| N2
    N3 -->|"Mesh->Instance"| N4
    N2 -->|"Points->Points"| N4
    N4 -->|"Instances->Result"| N5
    N0 -->|"Resolution->Spacing"| N2
    N0 -->|"Resolution->Size"| N3
```

### City Builder

Example script found [here](https://carson-katri.github.io/geometry-script/tutorials/city-builder.html#final-script).

## `nodebpy`

``` python
with g.tree("Voxelise") as tree:
    geo = tree.inputs.geometry("Geometry")
    seed = tree.inputs.integer("Seed")
    road_width = tree.inputs.float("Road Width", 0.25)
    size_x = tree.inputs.float("Size X", 5.0)
    size_y = tree.inputs.float("Size Y", 5.0)
    density = tree.inputs.float("Density", 10.0)
    building_size_min = tree.inputs.vector("Building Size Min", (0.1, 0.1, 0.2))
    building_size_max = tree.inputs.vector("Building Size Max", (0.3, 0.3, 1.0))

    curve_mesh = geo >> g.CurveToMesh(
        profile_curve=g.CurveLine(
            start=g.CombineXYZ(x=road_width * -0.5),
            end=g.CombineXYZ(x=road_width * 0.5),
        ),
    )

    building_points = g.Grid(size_x, size_y) >> g.DistributePointsOnFaces(
        density=density, seed=seed
    )

    road_points = geo >> g.CurveToPoints(mode="EVALUATED")
    building_points = g.DeleteGeometry.point(
        building_points,
        selection=g.GeometryProximity(
            target_element="POINTS",
            target=road_points,
            source_position=g.Position().o.position,
        ).o.distance
        < road_width,
    )

    buildings = building_points >> g.InstanceOnPoints(
        instance=g.Cube() >> g.TransformGeometry(translation=(0, 0, 0.5)),
        scale=g.RandomValue.vector(
            min=building_size_min, max=building_size_max, seed=seed
        ),
    )

    g.JoinGeometry((curve_mesh, buildings)) >> tree.outputs.geometry("Result")
```

## `geometry-script`

``` python
from geometry_script import *


@tree("City Builder")
def city_builder(
    geometry: Geometry,
    seed: Int,
    road_width: Float = 0.25,
    size_x: Float = 5,
    size_y: Float = 5,
    density: Float = 10,
    building_size_min: Vector = (0.1, 0.1, 0.2),
    building_size_max: Vector = (0.3, 0.3, 1),
):
    # Road mesh
    yield geometry.curve_to_mesh(
        profile_curve=curve_line(
            start=combine_xyz(x=road_width * -0.5), end=combine_xyz(x=road_width * 0.5)
        )
    )
    # Building points
    building_points = (
        grid(size_x=size_x, size_y=size_y)
        .distribute_points_on_faces(density=density, seed=seed)
        .points
    )
    road_points = geometry.curve_to_points(mode=CurveToPoints.Mode.EVALUATED).points
    # Delete points within the curve
    building_points = building_points.delete_geometry(
        domain=DeleteGeometry.Domain.POINT,
        selection=geometry_proximity(
            target_element=GeometryProximity.TargetElement.POINTS,
            target=road_points,
            source_position=position(),
        ).distance
        < road_width,
    )
    # Building instances
    yield building_points.instance_on_points(
        instance=cube().transform(translation=(0, 0, 0.5)),
        scale=random_value(
            data_type=RandomValue.DataType.FLOAT_VECTOR,
            min=building_size_min,
            max=building_size_max,
            seed=seed,
        ),
    )
```

``` mermaid
graph LR
    N0("Group Input"):::default-node
    N1("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N2("Math<br/><small>(MULTIPLY)</small>"):::converter-node
    N3("Curve to Points"):::geometry-node
    N4("Position"):::input-node
    N5("Grid"):::geometry-node
    N6("Random Value"):::converter-node
    N7("Combine XYZ"):::converter-node
    N8("Combine XYZ"):::converter-node
    N9("Geometry Proximity"):::geometry-node
    N10("Distribute Points on Faces"):::geometry-node
    N11("Curve Line<br/><small>(0,0,1)</small>"):::geometry-node
    N12("Compare<br/><small>(LESS_THAN)</small>"):::converter-node
    N13("Cube"):::geometry-node
    N14("Curve to Mesh"):::geometry-node
    N15("Delete Geometry"):::geometry-node
    N16("Transform Geometry<br/><small>(0,0,0.5)</small>"):::geometry-node
    N17("Instance on Points"):::geometry-node
    N18("Join Geometry"):::geometry-node
    N19("Group Output"):::default-node
    N0 -->|"Road Width->Value"| N1
    N1 -->|"Value->X"| N7
    N0 -->|"Road Width->Value"| N2
    N2 -->|"Value->X"| N8
    N7 -->|"Vector->Start"| N11
    N8 -->|"Vector->End"| N11
    N11 -->|"Curve->Profile Curve"| N14
    N0 -->|"Geometry->Curve"| N14
    N0 -->|"Size X->Size X"| N5
    N0 -->|"Size Y->Size Y"| N5
    N5 -->|"Mesh->Mesh"| N10
    N0 -->|"Geometry->Curve"| N3
    N3 -->|"Points->Geometry"| N9
    N4 -->|"Position->Sample Position"| N9
    N9 -->|"Distance->A"| N12
    N12 -->|"Result->Selection"| N15
    N13 -->|"Mesh->Geometry"| N16
    N0 -->|"Building Size Min->Min"| N6
    N0 -->|"Building Size Max->Max"| N6
    N0 -->|"Seed->Seed"| N6
    N16 -->|"Geometry->Instance"| N17
    N15 -->|"Geometry->Points"| N17
    N17 -->|"Instances->Geometry"| N18
    N18 -->|"Geometry->Result"| N19
    N0 -->|"Seed->Seed"| N10
    N0 -->|"Density->Density"| N10
    N0 -->|"Road Width->B"| N12
    N10 -->|"Points->Geometry"| N15
    N6 -->|"Value->Scale"| N17
    N14 -->|"Mesh->Geometry"| N18
```
