from nodebpy.builder import NodeBuilder, SocketLinker


import bpy
from .types import TYPE_INPUT_VALUE, TYPE_INPUT_VECTOR, TYPE_INPUT_INT


from typing_extensions import Literal


class DistributePointsInGrid(NodeBuilder):
    """Generate points inside a volume grid"""

    name = "GeometryNodeDistributePointsInGrid"
    node: bpy.types.GeometryNodeDistributePointsInGrid

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
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
