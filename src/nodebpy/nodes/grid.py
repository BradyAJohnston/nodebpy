import bpy
from typing_extensions import Literal

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_GRID,
    TYPE_INPUT_INT,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    _AdvectGridIntegration,
    _GridDataTypes,
)


class DistributePointsInGrid(NodeBuilder):
    """Generate points inside a volume grid"""

    name = "GeometryNodeDistributePointsInGrid"
    node: bpy.types.GeometryNodeDistributePointsInGrid

    def __init__(
        self,
        grid: LINKABLE = None,
        mode: Literal["DENSITY_RANDOM", "DENSITY_GRID"] = "DENSITY_RANDOM",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Grid": grid,
        }
        self.mode = mode
        key_args.update(kwargs)
        self._establish_links(**key_args)

    @classmethod
    def grid(
        cls,
        grid: LINKABLE,
        spacing: TYPE_INPUT_VECTOR = (0.3, 0.3, 0.3),
        threshold: TYPE_INPUT_VALUE = 0.1,
    ) -> "DistributePointsInGrid":
        return cls(grid=grid, Spacing=spacing, Threshold=threshold, mode="DENSITY_GRID")

    @classmethod
    def random(
        cls,
        grid: LINKABLE,
        density: TYPE_INPUT_VALUE = 1.0,
        seed: TYPE_INPUT_INT = 0,
    ) -> "DistributePointsInGrid":
        return cls(grid=grid, Density=density, Seed=seed, mode="DENSITY_RANDOM")

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

    name = "GeometryNodeDistributePointsInVolume"
    node: bpy.types.GeometryNodeDistributePointsInVolume

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        mode: Literal["Random", "Grid"] = "Random",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Volume": volume,
            "Mode": mode,
        }
        key_args.update(kwargs)
        self._establish_links(**key_args)

    @classmethod
    def grid(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        density: TYPE_INPUT_VALUE = 1.0,
        seed: TYPE_INPUT_INT = 0,
    ):
        return cls(volume=volume, Density=density, Seed=seed, mode="Grid")

    @classmethod
    def random(
        cls,
        volume: TYPE_INPUT_GEOMETRY = None,
        spacing: TYPE_INPUT_VECTOR = (0.3, 0.3, 0.3),
        threshold: TYPE_INPUT_VALUE = 0.1,
    ):
        return cls(volume=volume, Space=spacing, Threshold=threshold, mode="Random")

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


class FieldToGrid(NodeBuilder):
    """Create new grids by evaluating new values on an existing volume grid topology

    New socket items for field evaluation are first created from *args then **kwargs to give specific names to the items.

    Data types are inferred automatically from the closest compatible data type.

    Inputs:
    -------
    topology: LINKABLE
        The grid which contains the topology to evaluate the different fields on.
    data_type: _GridDataTypes = "FLOAT"
        The data type of the grid to evaluate on. Possible values are "FLOAT", "INT", "VECTOR", "BOOLEAN".
    *args: TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT | TYPE_INPUT_BOOLEAN
        The fields to evaluate on the grid.
    **kwargs: dict[str, TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT | TYPE_INPUT_GEOMETRY]
        The key-value pairs of the fields to evaluate on the grid. Keys will be used as the name of the socket.

    """

    name = "GeometryNodeFieldToGrid"
    node: bpy.types.GeometryNodeFieldToGrid
    _socket_data_types = ("FLOAT", "VALUE", "INT", "VECTOR", "BOOLEAN")
    _default_input_id = "Topology"

    def __init__(
        self,
        *args: TYPE_INPUT_GRID,
        topology: TYPE_INPUT_GRID = None,
        data_type: _GridDataTypes = "FLOAT",
        **kwargs: TYPE_INPUT_GRID,
    ):
        super().__init__()
        self.data_type = data_type
        key_args = {
            "Topology": topology,
        }
        key_args.update(self._add_inputs(*args, **kwargs))  # type: ignore
        self._establish_links(**key_args)

    def _add_socket(  # type: ignore
        self,
        name: str,
        type: _GridDataTypes = "FLOAT",
        default_value: float | int | str | None = None,
    ):
        item = self.node.grid_items.new(socket_type=type, name=name)
        if default_value is not None:
            try:
                self.node.inputs[item.name].default_value = default_value  # type: ignore
            except TypeError as e:
                raise ValueError(
                    f"Invalid default value for {type}: {default_value}"
                ) from e
        return self.node.inputs[item.name]

    def capture(self, *args, **kwargs) -> list[SocketLinker]:
        outputs = {
            name: self.node.outputs[name] for name in self._add_inputs(*args, **kwargs)
        }

        return [SocketLinker(x) for x in outputs.values()]

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.grid_items
        }

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.grid_items
        }

    @property
    def i_topology(self) -> SocketLinker:
        """Input socket: Topology"""
        return self._input("Topology")

    @property
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class GetNamedGrid(NodeBuilder):
    """Get volume grid from a volume geometry with the specified name"""

    name = "GeometryNodeGetNamedGrid"
    node: bpy.types.GeometryNodeGetNamedGrid
    _default_input_id = "Volume"

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        remove: TYPE_INPUT_BOOLEAN = True,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Volume": volume, "Name": name, "Remove": remove}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class AdvectGrid(NodeBuilder):
    """Move grid values through a velocity field using numerical integration. Supports multiple integration schemes for different accuracy and performance trade-offs"""

    name = "GeometryNodeGridAdvect"
    node: bpy.types.GeometryNodeGridAdvect
    _socket_data_types = ["FLOAT", "VALUE", "INT", "VECTOR"]

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
        velocity: TYPE_INPUT_VECTOR = None,
        time_step: TYPE_INPUT_VALUE = 1.0,
        *,
        integration_scheme: _AdvectGridIntegration = "Runge-Kutta 3",
        limiter: Literal["None", "Clamp", "Revert"] = "Clamp",
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
    def data_type(
        self,
    ) -> Literal["FLOAT", "INT", "VECTOR"]:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: Literal["FLOAT", "INT", "VECTOR"],
    ):
        self.node.data_type = value


class GridCurl(NodeBuilder):
    """Calculate the magnitude and direction of circulation of a directional vector grid"""

    name = "GeometryNodeGridCurl"
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

    name = "GeometryNodeGridDivergence"
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

    name = "GeometryNodeGridGradient"
    node: bpy.types.GeometryNodeGridGradient

    def __init__(self, grid: TYPE_INPUT_VALUE = None):
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

    name = "GeometryNodeGridInfo"
    node: bpy.types.GeometryNodeGridInfo

    def __init__(
        self, grid: TYPE_INPUT_GRID = None, data_type: _GridDataTypes = "FLOAT"
    ):
        super().__init__()
        key_args = {"Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class GridLaplacian(NodeBuilder):
    """Compute the divergence of the gradient of the input grid"""

    name = "GeometryNodeGridLaplacian"
    node: bpy.types.GeometryNodeGridLaplacian

    def __init__(self, grid: TYPE_INPUT_VALUE = None):
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


class PruneGrid(NodeBuilder):
    """Make the storage of a volume grid more efficient by collapsing data into tiles or inner nodes"""

    name = "GeometryNodeGridPrune"
    node: bpy.types.GeometryNodeGridPrune

    def __init__(
        self,
        grid: TYPE_INPUT_GRID = None,
        *,
        mode: Literal["Inactive", "Threshold", "SDF"] = "Threshold",
        threshold: TYPE_INPUT_VALUE = 0.01,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Mode": mode, "Threshold": threshold}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class VoxelizeGrid(NodeBuilder):
    """Remove sparseness from a volume grid by making the active tiles into voxels"""

    name = "GeometryNodeGridVoxelize"
    node: bpy.types.GeometryNodeGridVoxelize

    def __init__(
        self, grid: TYPE_INPUT_GRID = None, data_type: _GridDataTypes = "FLOAT"
    ):
        super().__init__()
        key_args = {"Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_grid(self) -> SocketLinker:
        """Input socket: Grid"""
        return self._input("Grid")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class VolumeCube(NodeBuilder):
    """Generate a dense volume with a field that controls the density at each grid voxel based on its position"""

    name = "GeometryNodeVolumeCube"
    node: bpy.types.GeometryNodeVolumeCube

    def __init__(
        self,
        density: TYPE_INPUT_VALUE = 1.0,
        background: TYPE_INPUT_VALUE = 0.0,
        min: TYPE_INPUT_VECTOR = (-1.0, -1.0, -1.0),
        max: TYPE_INPUT_VECTOR = (1.0, 1.0, 1.0),
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


class SDFGridBoolean(NodeBuilder):
    """Cut, subtract, or join multiple SDF volume grid inputs"""

    name = "GeometryNodeSDFGridBoolean"
    node: bpy.types.GeometryNodeSDFGridBoolean

    def __init__(
        self, *, operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE"
    ):
        super().__init__()
        self.operation = operation

    @classmethod
    def intersect(
        cls,
        *args: LINKABLE,
    ) -> "SDFGridBoolean":
        node = cls(operation="INTERSECT")
        for arg in args:
            if arg is None:
                continue
            node.link_from(arg, "Grid 2")
        return node

    @classmethod
    def union(
        cls,
        *args: LINKABLE,
    ) -> "SDFGridBoolean":
        node = cls(operation="UNION")
        for arg in args:
            if arg is None:
                continue
            node.link_from(arg, "Grid 2")
        return node

    @classmethod
    def difference(
        cls,
        *args: LINKABLE,
        grid_1: LINKABLE,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Difference'."""
        node = cls(operation="DIFFERENCE")
        node.link_from(grid_1, "Grid 1")
        for arg in args:
            if arg is None:
                continue
            node.link_from(arg, "Grid 2")
        return node

    @property
    def i_grid_1(self) -> SocketLinker:
        """Input socket: Grid 1"""
        return self._input("Grid 1")

    @property
    def i_grid_2(self) -> SocketLinker:
        """Input socket: Grid 2"""
        return self._input("Grid 2")

    @property
    def o_grid(self) -> SocketLinker:
        """Output socket: Grid"""
        return self._output("Grid")

    @property
    def operation(self) -> Literal["INTERSECT", "UNION", "DIFFERENCE"]:
        return self.node.operation

    @operation.setter
    def operation(self, value: Literal["INTERSECT", "UNION", "DIFFERENCE"]):
        self.node.operation = value


class SDFGridFillet(NodeBuilder):
    """Round off concave internal corners in a signed distance field. Only affects areas with negative principal curvature, creating smoother transitions between surfaces"""

    name = "GeometryNodeSDFGridFillet"
    node: bpy.types.GeometryNodeSDFGridFillet

    def __init__(self, grid: TYPE_INPUT_VALUE = None, iterations: TYPE_INPUT_INT = 1):
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

    name = "GeometryNodeSDFGridLaplacian"
    node: bpy.types.GeometryNodeSDFGridLaplacian

    def __init__(self, grid: TYPE_INPUT_VALUE = None, iterations: TYPE_INPUT_INT = 1):
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

    name = "GeometryNodeSDFGridMean"
    node: bpy.types.GeometryNodeSDFGridMean

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
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

    name = "GeometryNodeSDFGridMeanCurvature"
    node: bpy.types.GeometryNodeSDFGridMeanCurvature

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
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

    name = "GeometryNodeSDFGridMedian"
    node: bpy.types.GeometryNodeSDFGridMedian

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
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

    name = "GeometryNodeSDFGridOffset"
    node: bpy.types.GeometryNodeSDFGridOffset

    def __init__(self, grid: TYPE_INPUT_VALUE = 0.0, distance: TYPE_INPUT_VALUE = 0.1):
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

    name = "GeometryNodeSampleGrid"
    node: bpy.types.GeometryNodeSampleGrid

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
        position: TYPE_INPUT_VECTOR = None,
        interpolation: Literal["Trilinear", "Triquadratic", "Nearest Neighbor"]
        | bpy.types.NodeSocketMenu = "Trilinear",
        *,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Position": position, "Interpolation": interpolation}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class SampleGridIndex(NodeBuilder):
    """Retrieve volume grid values at specific voxels"""

    name = "GeometryNodeSampleGridIndex"
    node: bpy.types.GeometryNodeSampleGridIndex

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = None,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
        *,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "X": x, "Y": y, "Z": z}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class SetGridBackground(NodeBuilder):
    """Set the background value used for inactive voxels and tiles"""

    name = "GeometryNodeSetGridBackground"
    node: bpy.types.GeometryNodeSetGridBackground

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        background: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Background": background}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class SetGridTransform(NodeBuilder):
    """Set the transform for the grid from index space into object space."""

    name = "GeometryNodeSetGridTransform"
    node: bpy.types.GeometryNodeSetGridTransform

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        transform: LINKABLE | None = None,
        *,
        data_type: _GridDataTypes = "FLOAT",
    ):
        super().__init__()
        key_args = {"Grid": grid, "Transform": transform}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> _GridDataTypes:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: _GridDataTypes,
    ):
        self.node.data_type = value


class StoreNamedGrid(NodeBuilder):
    """Store grid data in a volume geometry with the specified name"""

    name = "GeometryNodeStoreNamedGrid"
    node: bpy.types.GeometryNodeStoreNamedGrid

    def __init__(
        self,
        volume: TYPE_INPUT_GEOMETRY = None,
        name: TYPE_INPUT_STRING = "",
        grid: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal["FLOAT", "VECTOR_FLOAT", "INT", "BOOLEAN"] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Volume": volume, "Name": name, "Grid": grid}
        self.data_type = data_type
        self._establish_links(**key_args)

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
    def data_type(
        self,
    ) -> Literal["FLOAT", "VECTOR_FLOAT", "INT", "BOOLEAN"]:
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(
        self,
        value: Literal["FLOAT", "VECTOR_FLOAT", "INT", "BOOLEAN"],
    ):
        self.node.data_type = value
