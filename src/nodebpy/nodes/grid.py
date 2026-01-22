from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class AdvectGrid(NodeBuilder):
    """Move grid values through a velocity field using numerical integration. Supports multiple integration schemes for different accuracy and performance trade-offs"""

    _bl_idname = "GeometryNodeGridAdvect"
    node: bpy.types.GeometryNodeGridAdvect

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        velocity: TYPE_INPUT_VECTOR = None,
        time_step: TYPE_INPUT_VALUE = 1.0,
        integration_scheme: TYPE_INPUT_MENU = "Runge-Kutta 3",
        limiter: TYPE_INPUT_MENU = "Clamp",
        *,
        data_type: Literal["FLOAT", "INT", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {
            "Grid": grid,
            "Velocity": velocity,
            "Time Step": time_step,
            "Integration Scheme": integration_scheme,
            "Limiter": limiter,
        }
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        grid: TYPE_INPUT_VALUE = 0.0,
        velocity: TYPE_INPUT_VECTOR = None,
        time_step: TYPE_INPUT_VALUE = 1.0,
        integration_scheme: TYPE_INPUT_MENU = "Runge-Kutta 3",
        limiter: TYPE_INPUT_MENU = "Clamp",
    ) -> "AdvectGrid":
        """Create Advect Grid with operation 'Float'."""
        return cls(
            data_type="FLOAT",
            grid=grid,
            velocity=velocity,
            time_step=time_step,
            integration_scheme=integration_scheme,
            limiter=limiter,
        )

    @classmethod
    def integer(
        cls,
        grid: TYPE_INPUT_INT = 0,
        velocity: TYPE_INPUT_VECTOR = None,
        time_step: TYPE_INPUT_VALUE = 1.0,
        integration_scheme: TYPE_INPUT_MENU = "Runge-Kutta 3",
        limiter: TYPE_INPUT_MENU = "Clamp",
    ) -> "AdvectGrid":
        """Create Advect Grid with operation 'Integer'."""
        return cls(
            data_type="INT",
            grid=grid,
            velocity=velocity,
            time_step=time_step,
            integration_scheme=integration_scheme,
            limiter=limiter,
        )

    @classmethod
    def vector(
        cls,
        grid: TYPE_INPUT_VECTOR = None,
        velocity: TYPE_INPUT_VECTOR = None,
        time_step: TYPE_INPUT_VALUE = 1.0,
        integration_scheme: TYPE_INPUT_MENU = "Runge-Kutta 3",
        limiter: TYPE_INPUT_MENU = "Clamp",
    ) -> "AdvectGrid":
        """Create Advect Grid with operation 'Vector'."""
        return cls(
            data_type="VECTOR",
            grid=grid,
            velocity=velocity,
            time_step=time_step,
            integration_scheme=integration_scheme,
            limiter=limiter,
        )

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_velocity(self) -> SocketLinker:
        """Input socket: Velocity"""
        return self._input("Velocity")

    @property
    def i_time_step(self) -> SocketLinker:
        """Input socket: Time Step"""
        return self._input("Time Step")

    @property
    def i_integration_scheme(self) -> SocketLinker:
        """Input socket: Integration Scheme"""
        return self._input("Integration Scheme")

    @property
    def i_limiter(self) -> SocketLinker:
        """Input socket: Limiter"""
        return self._input("Limiter")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "VECTOR"]):
        self.node.data_type = value


class DistributePointsInGrid(NodeBuilder):
    """Generate points inside a volume grid"""

    _bl_idname = "GeometryNodeDistributePointsInGrid"
    node: bpy.types.GeometryNodeDistributePointsInGrid

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        density: TYPE_INPUT_VALUE = 1.0,
        seed: TYPE_INPUT_INT = 0,
        spacing: TYPE_INPUT_VECTOR = None,
        threshold: TYPE_INPUT_VALUE = 0.1,
        *,
        mode: Literal["DENSITY_RANDOM", "DENSITY_GRID"] = "DENSITY_RANDOM",
    ):
        super().__init__()
        key_args = {
            "Grid": grid,
            "Density": density,
            "Seed": seed,
            "Spacing": spacing,
            "Threshold": threshold,
        }
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_seed(self) -> SocketLinker:
        """Input socket: Seed"""
        return self._input("Seed")

    @property
    def i_spacing(self) -> SocketLinker:
        """Input socket: Spacing"""
        return self._input("Spacing")

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")

    @property
    def mode(self) -> Literal["DENSITY_RANDOM", "DENSITY_GRID"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["DENSITY_RANDOM", "DENSITY_GRID"]):
        self.node.mode = value


class DistributePointsInVolume(NodeBuilder):
    """Generate points inside a volume"""

    _bl_idname = "GeometryNodeDistributePointsInVolume"
    node: bpy.types.GeometryNodeDistributePointsInVolume

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        mode: TYPE_INPUT_MENU = "Random",
        density: TYPE_INPUT_VALUE = 1.0,
        seed: TYPE_INPUT_INT = 0,
        spacing: TYPE_INPUT_VECTOR = None,
        threshold: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {
            "Volume": volume,
            "Mode": mode,
            "Density": density,
            "Seed": seed,
            "Spacing": spacing,
            "Threshold": threshold,
        }

        self._establish_links(**key_args)

    @property
    def i_volume(self) -> SocketLinker:
        """Input socket: Volume"""
        return self._input("Volume")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_seed(self) -> SocketLinker:
        """Input socket: Seed"""
        return self._input("Seed")

    @property
    def i_spacing(self) -> SocketLinker:
        """Input socket: Spacing"""
        return self._input("Spacing")

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")


class GetNamedGrid(NodeBuilder):
    """Get volume grid from a volume geometry with the specified name"""

    _bl_idname = "GeometryNodeGetNamedGrid"
    node: bpy.types.GeometryNodeGetNamedGrid

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Volume": volume, "Name": name, "Remove": remove}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
    ) -> "GetNamedGrid":
        """Create Get Named Grid with operation 'Float'."""
        return cls(data_type="FLOAT", volume=volume, name=name, remove=remove)

    @classmethod
    def integer(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
    ) -> "GetNamedGrid":
        """Create Get Named Grid with operation 'Integer'."""
        return cls(data_type="INT", volume=volume, name=name, remove=remove)

    @classmethod
    def boolean(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
    ) -> "GetNamedGrid":
        """Create Get Named Grid with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", volume=volume, name=name, remove=remove)

    @classmethod
    def vector(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
    ) -> "GetNamedGrid":
        """Create Get Named Grid with operation 'Vector'."""
        return cls(data_type="VECTOR", volume=volume, name=name, remove=remove)

    @property
    def i_volume(self) -> SocketLinker:
        """Input socket: Volume"""
        return self._input("Volume")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def i_remove(self) -> SocketLinker:
        """Input socket: Remove"""
        return self._input("Remove")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class GridCurl(NodeBuilder):
    """Calculate the magnitude and direction of circulation of a directional vector grid"""

    _bl_idname = "GeometryNodeGridCurl"
    node: bpy.types.GeometryNodeGridCurl

    def __init__(self, grid: TYPE_INPUT_VECTOR = None):
        super().__init__()
        key_args = {"Grid": grid}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_curl(self) -> SocketLinker:
        """Output socket: Curl"""
        return self._output("Curl")


class GridDivergence(NodeBuilder):
    """Calculate the flow into and out of each point of a directional vector grid"""

    _bl_idname = "GeometryNodeGridDivergence"
    node: bpy.types.GeometryNodeGridDivergence

    def __init__(self, grid: TYPE_INPUT_VECTOR = None):
        super().__init__()
        key_args = {"Grid": grid}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_divergence(self) -> SocketLinker:
        """Output socket: Divergence"""
        return self._output("Divergence")


class GridGradient(NodeBuilder):
    """Calculate the direction and magnitude of the change in values of a scalar grid"""

    _bl_idname = "GeometryNodeGridGradient"
    node: bpy.types.GeometryNodeGridGradient

    def __init__(self, grid: TYPE_INPUT_VALUE = 0.0):
        super().__init__()
        key_args = {"Grid": grid}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_gradient(self) -> SocketLinker:
        """Output socket: Gradient"""
        return self._output("Gradient")


class GridInfo(NodeBuilder):
    """Retrieve information about a volume grid"""

    _bl_idname = "GeometryNodeGridInfo"
    node: bpy.types.GeometryNodeGridInfo

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, grid: TYPE_INPUT_VALUE = 0.0) -> "GridInfo":
        """Create Grid Info with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid)

    @classmethod
    def integer(cls, grid: TYPE_INPUT_INT = 0) -> "GridInfo":
        """Create Grid Info with operation 'Integer'."""
        return cls(data_type="INT", grid=grid)

    @classmethod
    def boolean(cls, grid: TYPE_INPUT_BOOLEAN = False) -> "GridInfo":
        """Create Grid Info with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid)

    @classmethod
    def vector(cls, grid: TYPE_INPUT_VECTOR = None) -> "GridInfo":
        """Create Grid Info with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def o_background_value(self) -> SocketLinker:
        """Output socket: Background Value"""
        return self._output("Background Value")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class GridLaplacian(NodeBuilder):
    """Compute the divergence of the gradient of the input grid"""

    _bl_idname = "GeometryNodeGridLaplacian"
    node: bpy.types.GeometryNodeGridLaplacian

    def __init__(self, grid: TYPE_INPUT_VALUE = 0.0):
        super().__init__()
        key_args = {"Grid": grid}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_laplacian(self) -> SocketLinker:
        """Output socket: Laplacian"""
        return self._output("Laplacian")


class GridToMesh(NodeBuilder):
    """Generate a mesh on the "surface" of a volume grid"""

    _bl_idname = "GeometryNodeGridToMesh"
    node: bpy.types.GeometryNodeGridToMesh

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        threshold: TYPE_INPUT_VALUE = 0.1,
        adaptivity: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Threshold": threshold, "Adaptivity": adaptivity}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def i_adaptivity(self) -> SocketLinker:
        """Input socket: Adaptivity"""
        return self._input("Adaptivity")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class MeshToDensityGrid(NodeBuilder):
    """Create a filled volume grid from a mesh"""

    _bl_idname = "GeometryNodeMeshToDensityGrid"
    node: bpy.types.GeometryNodeMeshToDensityGrid

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        density: TYPE_INPUT_VALUE = 1.0,
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        gradient_width: TYPE_INPUT_VALUE = 0.2,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Density": density,
            "Voxel Size": voxel_size,
            "Gradient Width": gradient_width,
        }

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_gradient_width(self) -> SocketLinker:
        """Input socket: Gradient Width"""
        return self._input("Gradient Width")

    @property
    def o_density_grid(self) -> SocketLinker:
        """Output socket: Density Grid"""
        return self._output("Density Grid")


class MeshToSDFGrid(NodeBuilder):
    """Create a signed distance volume grid from a mesh"""

    _bl_idname = "GeometryNodeMeshToSDFGrid"
    node: bpy.types.GeometryNodeMeshToSDFGrid

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        band_width: TYPE_INPUT_INT = 3,
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Voxel Size": voxel_size, "Band Width": band_width}

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_band_width(self) -> SocketLinker:
        """Input socket: Band Width"""
        return self._input("Band Width")

    @property
    def o_sdf_grid(self) -> SocketLinker:
        """Output socket: SDF Grid"""
        return self._output("SDF Grid")


class MeshToVolume(NodeBuilder):
    """Create a fog volume with the shape of the input mesh's surface"""

    _bl_idname = "GeometryNodeMeshToVolume"
    node: bpy.types.GeometryNodeMeshToVolume

    def __init__(
        self,
        mesh: TYPE_INPUT_GEOMETRY = None,
        density: TYPE_INPUT_VALUE = 1.0,
        resolution_mode: TYPE_INPUT_MENU = "Amount",
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        voxel_amount: TYPE_INPUT_VALUE = 64.0,
        interior_band_width: TYPE_INPUT_VALUE = 0.2,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Density": density,
            "Resolution Mode": resolution_mode,
            "Voxel Size": voxel_size,
            "Voxel Amount": voxel_amount,
            "Interior Band Width": interior_band_width,
        }

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_resolution_mode(self) -> SocketLinker:
        """Input socket: Resolution Mode"""
        return self._input("Resolution Mode")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_voxel_amount(self) -> SocketLinker:
        """Input socket: Voxel Amount"""
        return self._input("Voxel Amount")

    @property
    def i_interior_band_width(self) -> SocketLinker:
        """Input socket: Interior Band Width"""
        return self._input("Interior Band Width")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class PointsToSDFGrid(NodeBuilder):
    """Create a signed distance volume grid from points"""

    _bl_idname = "GeometryNodePointsToSDFGrid"
    node: bpy.types.GeometryNodePointsToSDFGrid

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        radius: TYPE_INPUT_VALUE = 0.5,
        voxel_size: TYPE_INPUT_VALUE = 0.3,
    ):
        super().__init__()
        key_args = {"Points": points, "Radius": radius, "Voxel Size": voxel_size}

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def o_sdf_grid(self) -> SocketLinker:
        """Output socket: SDF Grid"""
        return self._output("SDF Grid")


class PointsToVolume(NodeBuilder):
    """Generate a fog volume sphere around every point"""

    _bl_idname = "GeometryNodePointsToVolume"
    node: bpy.types.GeometryNodePointsToVolume

    def __init__(
        self,
        points: TYPE_INPUT_GEOMETRY = None,
        density: TYPE_INPUT_VALUE = 1.0,
        resolution_mode: TYPE_INPUT_MENU = "Amount",
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        voxel_amount: TYPE_INPUT_VALUE = 64.0,
        radius: TYPE_INPUT_VALUE = 0.5,
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Density": density,
            "Resolution Mode": resolution_mode,
            "Voxel Size": voxel_size,
            "Voxel Amount": voxel_amount,
            "Radius": radius,
        }

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_resolution_mode(self) -> SocketLinker:
        """Input socket: Resolution Mode"""
        return self._input("Resolution Mode")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_voxel_amount(self) -> SocketLinker:
        """Input socket: Voxel Amount"""
        return self._input("Voxel Amount")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class PruneGrid(NodeBuilder):
    """Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes"""

    _bl_idname = "GeometryNodeGridPrune"
    node: bpy.types.GeometryNodeGridPrune

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        mode: TYPE_INPUT_MENU = "Threshold",
        threshold: TYPE_INPUT_VALUE = 0.01,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Mode": mode, "Threshold": threshold}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        grid: TYPE_INPUT_VALUE = 0.0,
        mode: TYPE_INPUT_MENU = "Threshold",
        threshold: TYPE_INPUT_VALUE = 0.01,
    ) -> "PruneGrid":
        """Create Prune Grid with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid, mode=mode, threshold=threshold)

    @classmethod
    def integer(
        cls,
        grid: TYPE_INPUT_INT = 0,
        mode: TYPE_INPUT_MENU = "Threshold",
        threshold: TYPE_INPUT_INT = 0,
    ) -> "PruneGrid":
        """Create Prune Grid with operation 'Integer'."""
        return cls(data_type="INT", grid=grid, mode=mode, threshold=threshold)

    @classmethod
    def boolean(
        cls, grid: TYPE_INPUT_BOOLEAN = False, mode: TYPE_INPUT_MENU = "Threshold"
    ) -> "PruneGrid":
        """Create Prune Grid with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid, mode=mode)

    @classmethod
    def vector(
        cls,
        grid: TYPE_INPUT_VECTOR = None,
        mode: TYPE_INPUT_MENU = "Threshold",
        threshold: TYPE_INPUT_VECTOR = None,
    ) -> "PruneGrid":
        """Create Prune Grid with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid, mode=mode, threshold=threshold)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class SDFGridFillet(NodeBuilder):
    """Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces"""

    _bl_idname = "GeometryNodeSDFGridFillet"
    node: bpy.types.GeometryNodeSDFGridFillet

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SDFGridLaplacian(NodeBuilder):
    """Apply Laplacian flow smoothing to a signed distance field. Computationally efficient alternative to mean curvature flow, ideal when combined with SDF normalization"""

    _bl_idname = "GeometryNodeSDFGridLaplacian"
    node: bpy.types.GeometryNodeSDFGridLaplacian

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SDFGridMean(NodeBuilder):
    """Apply mean (box) filter smoothing to a signed distance field. Fast separable averaging filter for general smoothing of the distance field"""

    _bl_idname = "GeometryNodeSDFGridMean"
    node: bpy.types.GeometryNodeSDFGridMean

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        width: TYPE_INPUT_INT = 1,
        iterations: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Width": width, "Iterations": iterations}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_width(self) -> SocketLinker:
        """Input socket: Width"""
        return self._input("Width")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SDFGridMeanCurvature(NodeBuilder):
    """Apply mean curvature flow smoothing to a signed distance field. Evolves the surface based on its mean curvature, naturally smoothing high-curvature regions more than flat areas"""

    _bl_idname = "GeometryNodeSDFGridMeanCurvature"
    node: bpy.types.GeometryNodeSDFGridMeanCurvature

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SDFGridMedian(NodeBuilder):
    """Apply median filter to a signed distance field. Reduces noise while preserving sharp features and edges in the distance field"""

    _bl_idname = "GeometryNodeSDFGridMedian"
    node: bpy.types.GeometryNodeSDFGridMedian

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        width: TYPE_INPUT_INT = 1,
        iterations: TYPE_INPUT_INT = 1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Width": width, "Iterations": iterations}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_width(self) -> SocketLinker:
        """Input socket: Width"""
        return self._input("Width")

    @property
    def i_iterations(self) -> SocketLinker:
        """Input socket: Iterations"""
        return self._input("Iterations")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SDFGridOffset(NodeBuilder):
    """Offset a signed distance field surface by a world-space distance. Dilates (positive) or erodes (negative) while maintaining the signed distance property"""

    _bl_idname = "GeometryNodeSDFGridOffset"
    node: bpy.types.GeometryNodeSDFGridOffset

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        distance: TYPE_INPUT_VALUE = 0.1,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Distance": distance}

        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_distance(self) -> SocketLinker:
        """Input socket: Distance"""
        return self._input("Distance")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")


class SampleGrid(NodeBuilder):
    """Retrieve values from the specified volume grid"""

    _bl_idname = "GeometryNodeSampleGrid"
    node: bpy.types.GeometryNodeSampleGrid

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Trilinear",
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Position": position, "Interpolation": interpolation}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        grid: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Trilinear",
    ) -> "SampleGrid":
        """Create Sample Grid with operation 'Float'."""
        return cls(
            data_type="FLOAT", grid=grid, position=position, interpolation=interpolation
        )

    @classmethod
    def integer(
        cls,
        grid: TYPE_INPUT_INT = 0,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Trilinear",
    ) -> "SampleGrid":
        """Create Sample Grid with operation 'Integer'."""
        return cls(
            data_type="INT", grid=grid, position=position, interpolation=interpolation
        )

    @classmethod
    def boolean(
        cls,
        grid: TYPE_INPUT_BOOLEAN = False,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Trilinear",
    ) -> "SampleGrid":
        """Create Sample Grid with operation 'Boolean'."""
        return cls(
            data_type="BOOLEAN",
            grid=grid,
            position=position,
            interpolation=interpolation,
        )

    @classmethod
    def vector(
        cls,
        grid: TYPE_INPUT_VECTOR = None,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: TYPE_INPUT_MENU = "Trilinear",
    ) -> "SampleGrid":
        """Create Sample Grid with operation 'Vector'."""
        return cls(
            data_type="VECTOR",
            grid=grid,
            position=position,
            interpolation=interpolation,
        )

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_interpolation(self) -> SocketLinker:
        """Input socket: Interpolation"""
        return self._input("Interpolation")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class SampleGridIndex(NodeBuilder):
    """Retrieve volume grid values at specific voxels"""

    _bl_idname = "GeometryNodeSampleGridIndex"
    node: bpy.types.GeometryNodeSampleGridIndex

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "X": x, "Y": y, "Z": z}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls,
        grid: TYPE_INPUT_VALUE = 0.0,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
    ) -> "SampleGridIndex":
        """Create Sample Grid Index with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid, x=x, y=y, z=z)

    @classmethod
    def integer(
        cls,
        grid: TYPE_INPUT_INT = 0,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
    ) -> "SampleGridIndex":
        """Create Sample Grid Index with operation 'Integer'."""
        return cls(data_type="INT", grid=grid, x=x, y=y, z=z)

    @classmethod
    def boolean(
        cls,
        grid: TYPE_INPUT_BOOLEAN = False,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
    ) -> "SampleGridIndex":
        """Create Sample Grid Index with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid, x=x, y=y, z=z)

    @classmethod
    def vector(
        cls,
        grid: TYPE_INPUT_VECTOR = None,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
    ) -> "SampleGridIndex":
        """Create Sample Grid Index with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid, x=x, y=y, z=z)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_x(self) -> SocketLinker:
        """Input socket: X"""
        return self._input("X")

    @property
    def i_y(self) -> SocketLinker:
        """Input socket: Y"""
        return self._input("Y")

    @property
    def i_z(self) -> SocketLinker:
        """Input socket: Z"""
        return self._input("Z")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class SetGridBackground(NodeBuilder):
    """Set the background value used for inactive voxels and tiles"""

    _bl_idname = "GeometryNodeSetGridBackground"
    node: bpy.types.GeometryNodeSetGridBackground

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        background: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Background": background}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, grid: TYPE_INPUT_VALUE = 0.0, background: TYPE_INPUT_VALUE = 0.0
    ) -> "SetGridBackground":
        """Create Set Grid Background with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid, background=background)

    @classmethod
    def integer(
        cls, grid: TYPE_INPUT_INT = 0, background: TYPE_INPUT_INT = 0
    ) -> "SetGridBackground":
        """Create Set Grid Background with operation 'Integer'."""
        return cls(data_type="INT", grid=grid, background=background)

    @classmethod
    def boolean(
        cls, grid: TYPE_INPUT_BOOLEAN = False, background: TYPE_INPUT_BOOLEAN = False
    ) -> "SetGridBackground":
        """Create Set Grid Background with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid, background=background)

    @classmethod
    def vector(
        cls, grid: TYPE_INPUT_VECTOR = None, background: TYPE_INPUT_VECTOR = None
    ) -> "SetGridBackground":
        """Create Set Grid Background with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid, background=background)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_background(self) -> SocketLinker:
        """Input socket: Background"""
        return self._input("Background")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class SetGridTransform(NodeBuilder):
    """Set the transform for the grid from index space into object space."""

    _bl_idname = "GeometryNodeSetGridTransform"
    node: bpy.types.GeometryNodeSetGridTransform

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        transform: TYPE_INPUT_MATRIX = None,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Transform": transform}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, grid: TYPE_INPUT_VALUE = 0.0, transform: TYPE_INPUT_MATRIX = None
    ) -> "SetGridTransform":
        """Create Set Grid Transform with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid, transform=transform)

    @classmethod
    def integer(
        cls, grid: TYPE_INPUT_INT = 0, transform: TYPE_INPUT_MATRIX = None
    ) -> "SetGridTransform":
        """Create Set Grid Transform with operation 'Integer'."""
        return cls(data_type="INT", grid=grid, transform=transform)

    @classmethod
    def boolean(
        cls, grid: TYPE_INPUT_BOOLEAN = False, transform: TYPE_INPUT_MATRIX = None
    ) -> "SetGridTransform":
        """Create Set Grid Transform with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid, transform=transform)

    @classmethod
    def vector(
        cls, grid: TYPE_INPUT_VECTOR = None, transform: TYPE_INPUT_MATRIX = None
    ) -> "SetGridTransform":
        """Create Set Grid Transform with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid, transform=transform)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value


class StoreNamedGrid(NodeBuilder):
    """Store grid data in a volume geometry with the specified name"""

    _bl_idname = "GeometryNodeStoreNamedGrid"
    node: bpy.types.GeometryNodeStoreNamedGrid

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal["BOOLEAN", "FLOAT", "INT", "VECTOR_FLOAT"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Volume": volume, "Name": name, "Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def boolean(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_BOOLEAN = False,
    ) -> "StoreNamedGrid":
        """Create Store Named Grid with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", volume=volume, name=name, grid=grid)

    @classmethod
    def float(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_VALUE = 0.0,
    ) -> "StoreNamedGrid":
        """Create Store Named Grid with operation 'Float'."""
        return cls(data_type="FLOAT", volume=volume, name=name, grid=grid)

    @classmethod
    def integer(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_INT = 0,
    ) -> "StoreNamedGrid":
        """Create Store Named Grid with operation 'Integer'."""
        return cls(data_type="INT", volume=volume, name=name, grid=grid)

    @classmethod
    def vector(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_VECTOR = None,
    ) -> "StoreNamedGrid":
        """Create Store Named Grid with operation 'Vector'."""
        return cls(data_type="VECTOR_FLOAT", volume=volume, name=name, grid=grid)

    @property
    def i_volume(self) -> SocketLinker:
        """Input socket: Volume"""
        return self._input("Volume")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")

    @property
    def data_type(self) -> Literal["BOOLEAN", "FLOAT", "INT", "VECTOR_FLOAT"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["BOOLEAN", "FLOAT", "INT", "VECTOR_FLOAT"]):
        self.node.data_type = value


class VolumeCube(NodeBuilder):
    """Generate a dense volume with a field that controls the density at each grid voxel based on its position"""

    _bl_idname = "GeometryNodeVolumeCube"
    node: bpy.types.GeometryNodeVolumeCube

    def __init__(
        self,
        density: TYPE_INPUT_VALUE = 1.0,
        background: TYPE_INPUT_VALUE = 0.0,
        min: TYPE_INPUT_VECTOR = None,
        max: TYPE_INPUT_VECTOR = None,
        resolution_x: TYPE_INPUT_INT = 32,
        resolution_y: TYPE_INPUT_INT = 32,
        resolution_z: TYPE_INPUT_INT = 32,
    ):
        super().__init__()
        key_args = {
            "Density": density,
            "Background": background,
            "Min": min,
            "Max": max,
            "Resolution X": resolution_x,
            "Resolution Y": resolution_y,
            "Resolution Z": resolution_z,
        }

        self._establish_links(**key_args)

    @property
    def i_density(self) -> SocketLinker:
        """Input socket: Density"""
        return self._input("Density")

    @property
    def i_background(self) -> SocketLinker:
        """Input socket: Background"""
        return self._input("Background")

    @property
    def i_min(self) -> SocketLinker:
        """Input socket: Min"""
        return self._input("Min")

    @property
    def i_max(self) -> SocketLinker:
        """Input socket: Max"""
        return self._input("Max")

    @property
    def i_resolution_x(self) -> SocketLinker:
        """Input socket: Resolution X"""
        return self._input("Resolution X")

    @property
    def i_resolution_y(self) -> SocketLinker:
        """Input socket: Resolution Y"""
        return self._input("Resolution Y")

    @property
    def i_resolution_z(self) -> SocketLinker:
        """Input socket: Resolution Z"""
        return self._input("Resolution Z")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class VolumeToMesh(NodeBuilder):
    """Generate a mesh on the "surface" of a volume"""

    _bl_idname = "GeometryNodeVolumeToMesh"
    node: bpy.types.GeometryNodeVolumeToMesh

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        resolution_mode: TYPE_INPUT_MENU = "Grid",
        voxel_size: TYPE_INPUT_VALUE = 0.3,
        voxel_amount: TYPE_INPUT_VALUE = 64.0,
        threshold: TYPE_INPUT_VALUE = 0.1,
        adaptivity: TYPE_INPUT_VALUE = 0.0,
    ):
        super().__init__()
        key_args = {
            "Volume": volume,
            "Resolution Mode": resolution_mode,
            "Voxel Size": voxel_size,
            "Voxel Amount": voxel_amount,
            "Threshold": threshold,
            "Adaptivity": adaptivity,
        }

        self._establish_links(**key_args)

    @property
    def i_volume(self) -> SocketLinker:
        """Input socket: Volume"""
        return self._input("Volume")

    @property
    def i_resolution_mode(self) -> SocketLinker:
        """Input socket: Resolution Mode"""
        return self._input("Resolution Mode")

    @property
    def i_voxel_size(self) -> SocketLinker:
        """Input socket: Voxel Size"""
        return self._input("Voxel Size")

    @property
    def i_voxel_amount(self) -> SocketLinker:
        """Input socket: Voxel Amount"""
        return self._input("Voxel Amount")

    @property
    def i_threshold(self) -> SocketLinker:
        """Input socket: Threshold"""
        return self._input("Threshold")

    @property
    def i_adaptivity(self) -> SocketLinker:
        """Input socket: Adaptivity"""
        return self._input("Adaptivity")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class VoxelizeGrid(NodeBuilder):
    """Remove sparseness from a volume grid by making the active tiles into voxels"""

    _bl_idname = "GeometryNodeGridVoxelize"
    node: bpy.types.GeometryNodeGridVoxelize

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, grid: TYPE_INPUT_VALUE = 0.0) -> "VoxelizeGrid":
        """Create Voxelize Grid with operation 'Float'."""
        return cls(data_type="FLOAT", grid=grid)

    @classmethod
    def integer(cls, grid: TYPE_INPUT_INT = 0) -> "VoxelizeGrid":
        """Create Voxelize Grid with operation 'Integer'."""
        return cls(data_type="INT", grid=grid)

    @classmethod
    def boolean(cls, grid: TYPE_INPUT_BOOLEAN = False) -> "VoxelizeGrid":
        """Create Voxelize Grid with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", grid=grid)

    @classmethod
    def vector(cls, grid: TYPE_INPUT_VECTOR = None) -> "VoxelizeGrid":
        """Create Voxelize Grid with operation 'Vector'."""
        return cls(data_type="VECTOR", grid=grid)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(self) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]:
        return self.node.data_type

    @data_type.setter
    def data_type(self, value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR"]):
        self.node.data_type = value
