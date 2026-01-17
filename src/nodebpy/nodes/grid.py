import bpy
from typing_extensions import Literal

from nodebpy.builder import NodeBuilder, SocketLinker

from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
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
        grid: TYPE_INPUT_VALUE,
        spacing: TYPE_INPUT_VECTOR = (0.3, 0.3, 0.3),
        threshold: TYPE_INPUT_VALUE = 0.1,
    ) -> "DistributePointsInGrid":
        return cls(grid=grid, Spacing=spacing, Threshold=threshold, mode="DENSITY_GRID")

    @classmethod
    def random(
        cls,
        grid: TYPE_INPUT_VALUE,
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

    def __init__(
        self,
        *args: TYPE_INPUT_VALUE
        | TYPE_INPUT_VECTOR
        | TYPE_INPUT_INT
        | TYPE_INPUT_BOOLEAN,
        topology: LINKABLE = None,
        data_type: _GridDataTypes = "FLOAT",
        **kwargs: dict[
            str,
            TYPE_INPUT_VALUE | TYPE_INPUT_VECTOR | TYPE_INPUT_INT | TYPE_INPUT_BOOLEAN,
        ],
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
    def output_sockets(self) -> dict[str, SocketLinker]:
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.grid_items
        }

    @property
    def input_sockets(self) -> dict[str, SocketLinker]:
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
