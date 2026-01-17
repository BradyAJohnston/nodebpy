from __future__ import annotations

from typing import Iterable

import bpy
from typing_extensions import Literal

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_STRING,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    _AttributeDomains,
    _GridDataTypes,
)


class DialGizmo(NodeBuilder):
    """Show a dial gizmo in the viewport for a value"""

    name = "GeometryNodeGizmoDial"
    node: bpy.types.GeometryNodeGizmoDial

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        position: LINKABLE | None = (0.0, 0.0, 0.0),
        up: LINKABLE | None = [0.0, 0.0, 1.0],
        screen_space: TYPE_INPUT_BOOLEAN = True,
        radius: TYPE_INPUT_VALUE = 1.0,
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Value": value,
            "Position": position,
            "Up": up,
            "Screen Space": screen_space,
            "Radius": radius,
        }
        key_args.update(kwargs)
        self.color_id = color_id
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_up(self) -> SocketLinker:
        """Input socket: Up"""
        return self._input("Up")

    @property
    def i_screen_space(self) -> SocketLinker:
        """Input socket: Screen Space"""
        return self._input("Screen Space")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def color_id(self) -> Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]:
        return self.node.color_id

    @color_id.setter
    def color_id(self, value: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]):
        self.node.color_id = value


class LinearGizmo(NodeBuilder):
    """Show a linear gizmo in the viewport for a value"""

    name = "GeometryNodeGizmoLinear"
    node: bpy.types.GeometryNodeGizmoLinear

    def __init__(
        self,
        value: TYPE_INPUT_VALUE = 0.0,
        position: LINKABLE | None = (0.0, 0.0, 0.0),
        direction: LINKABLE | None = [0.0, 0.0, 1.0],
        color_id: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"] = "PRIMARY",
        draw_style: Literal["ARROW", "CROSS", "BOX"] = "ARROW",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Direction": direction}
        key_args.update(kwargs)
        self.color_id = color_id
        self.draw_style = draw_style
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_direction(self) -> SocketLinker:
        """Input socket: Direction"""
        return self._input("Direction")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def color_id(self) -> Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]:
        return self.node.color_id

    @color_id.setter
    def color_id(self, value: Literal["PRIMARY", "SECONDARY", "X", "Y", "Z"]):
        self.node.color_id = value

    @property
    def draw_style(self) -> Literal["ARROW", "CROSS", "BOX"]:
        return self.node.draw_style

    @draw_style.setter
    def draw_style(self, value: Literal["ARROW", "CROSS", "BOX"]):
        self.node.draw_style = value


class TransformGizmo(NodeBuilder):
    """Show a transform gizmo in the viewport"""

    name = "GeometryNodeGizmoTransform"
    node: bpy.types.GeometryNodeGizmoTransform

    def __init__(
        self,
        value: LINKABLE | None = None,
        position: LINKABLE | None = (0.0, 0.0, 0.0),
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        use_translation_x: bool = False,
        use_translation_y: bool = False,
        use_translation_z: bool = False,
        use_rotation_x: bool = False,
        use_rotation_y: bool = False,
        use_rotation_z: bool = False,
        use_scale_x: bool = False,
        use_scale_y: bool = False,
        use_scale_z: bool = False,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Value": value, "Position": position, "Rotation": rotation}
        key_args.update(kwargs)
        self.use_translation_x = use_translation_x
        self.use_translation_y = use_translation_y
        self.use_translation_z = use_translation_z
        self.use_rotation_x = use_rotation_x
        self.use_rotation_y = use_rotation_y
        self.use_rotation_z = use_rotation_z
        self.use_scale_x = use_scale_x
        self.use_scale_y = use_scale_y
        self.use_scale_z = use_scale_z
        self._establish_links(**key_args)

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def use_translation_x(self) -> bool:
        return self.node.use_translation_x

    @use_translation_x.setter
    def use_translation_x(self, value: bool):
        self.node.use_translation_x = value

    @property
    def use_translation_y(self) -> bool:
        return self.node.use_translation_y

    @use_translation_y.setter
    def use_translation_y(self, value: bool):
        self.node.use_translation_y = value

    @property
    def use_translation_z(self) -> bool:
        return self.node.use_translation_z

    @use_translation_z.setter
    def use_translation_z(self, value: bool):
        self.node.use_translation_z = value

    @property
    def use_rotation_x(self) -> bool:
        return self.node.use_rotation_x

    @use_rotation_x.setter
    def use_rotation_x(self, value: bool):
        self.node.use_rotation_x = value

    @property
    def use_rotation_y(self) -> bool:
        return self.node.use_rotation_y

    @use_rotation_y.setter
    def use_rotation_y(self, value: bool):
        self.node.use_rotation_y = value

    @property
    def use_rotation_z(self) -> bool:
        return self.node.use_rotation_z

    @use_rotation_z.setter
    def use_rotation_z(self, value: bool):
        self.node.use_rotation_z = value

    @property
    def use_scale_x(self) -> bool:
        return self.node.use_scale_x

    @use_scale_x.setter
    def use_scale_x(self, value: bool):
        self.node.use_scale_x = value

    @property
    def use_scale_y(self) -> bool:
        return self.node.use_scale_y

    @use_scale_y.setter
    def use_scale_y(self, value: bool):
        self.node.use_scale_y = value

    @property
    def use_scale_z(self) -> bool:
        return self.node.use_scale_z

    @use_scale_z.setter
    def use_scale_z(self, value: bool):
        self.node.use_scale_z = value


class AdvectGrid(NodeBuilder):
    """Move grid values through a velocity field using numerical integration. Supports multiple integration schemes for different accuracy and performance trade-offs"""

    name = "GeometryNodeGridAdvect"
    node: bpy.types.GeometryNodeGridAdvect

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        velocity: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        time_step: LINKABLE | None = 1.0,
        integration_scheme: LINKABLE | None = "Runge-Kutta 3",
        limiter: LINKABLE | None = "Clamp",
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Grid": grid,
            "Velocity": velocity,
            "Time Step": time_step,
            "Integration Scheme": integration_scheme,
            "Limiter": limiter,
        }
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class GridCurl(NodeBuilder):
    """Calculate the magnitude and direction of circulation of a directional vector grid"""

    name = "GeometryNodeGridCurl"
    node: bpy.types.GeometryNodeGridCurl

    def __init__(self, grid: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0), **kwargs):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)

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

    def __init__(self, grid: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0), **kwargs):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)

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

    def __init__(self, grid: TYPE_INPUT_VALUE = 0.0, **kwargs):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)

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
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class GridLaplacian(NodeBuilder):
    """Compute the divergence of the gradient of the input grid"""

    name = "GeometryNodeGridLaplacian"
    node: bpy.types.GeometryNodeGridLaplacian

    def __init__(self, grid: TYPE_INPUT_VALUE = 0.0, **kwargs):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)

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
        grid: TYPE_INPUT_VALUE = 0.0,
        mode: LINKABLE | None = "Threshold",
        threshold: TYPE_INPUT_VALUE = 0.009999999776482582,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Mode": mode, "Threshold": threshold}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class VoxelizeGrid(NodeBuilder):
    """Remove sparseness from a volume grid by making the active tiles into voxels"""

    name = "GeometryNodeGridVoxelize"
    node: bpy.types.GeometryNodeGridVoxelize

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class Group(NodeBuilder):
    """Group node"""

    name = "GeometryNodeGroup"
    node: bpy.types.GeometryNodeGroup

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)


class ImageInfo(NodeBuilder):
    """Retrieve information about an image"""

    name = "GeometryNodeImageInfo"
    node: bpy.types.GeometryNodeImageInfo

    def __init__(
        self, image: LINKABLE | None = None, frame: TYPE_INPUT_INT = 0, **kwargs
    ):
        super().__init__()
        key_args = {"Image": image, "Frame": frame}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_frame(self) -> SocketLinker:
        """Input socket: Frame"""
        return self._input("Frame")

    @property
    def o_width(self) -> SocketLinker:
        """Output socket: Width"""
        return self._output("Width")

    @property
    def o_height(self) -> SocketLinker:
        """Output socket: Height"""
        return self._output("Height")

    @property
    def o_has_alpha(self) -> SocketLinker:
        """Output socket: Has Alpha"""
        return self._output("Has Alpha")

    @property
    def o_frame_count(self) -> SocketLinker:
        """Output socket: Frame Count"""
        return self._output("Frame Count")

    @property
    def o_fps(self) -> SocketLinker:
        """Output socket: FPS"""
        return self._output("FPS")


class ImageTexture(NodeBuilder):
    """Sample values from an image texture"""

    name = "GeometryNodeImageTexture"
    node: bpy.types.GeometryNodeImageTexture

    def __init__(
        self,
        image: LINKABLE | None = None,
        vector: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        frame: TYPE_INPUT_INT = 0,
        interpolation: Literal["Linear", "Closest", "Cubic"] = "Linear",
        extension: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"] = "REPEAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Image": image, "Vector": vector, "Frame": frame}
        key_args.update(kwargs)
        self.interpolation = interpolation
        self.extension = extension
        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_frame(self) -> SocketLinker:
        """Input socket: Frame"""
        return self._input("Frame")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")

    @property
    def interpolation(self) -> Literal["Linear", "Closest", "Cubic"]:
        return self.node.interpolation

    @interpolation.setter
    def interpolation(self, value: Literal["Linear", "Closest", "Cubic"]):
        self.node.interpolation = value

    @property
    def extension(self) -> Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]:
        return self.node.extension

    @extension.setter
    def extension(self, value: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]):
        self.node.extension = value


class ImportCSV(NodeBuilder):
    """Import geometry from an CSV file"""

    name = "GeometryNodeImportCSV"
    node: bpy.types.GeometryNodeImportCSV

    def __init__(
        self,
        path: LINKABLE | None = "",
        delimiter: str | LINKABLE | None = ",",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Path": path, "Delimiter": delimiter}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def i_delimiter(self) -> SocketLinker:
        """Input socket: Delimiter"""
        return self._input("Delimiter")

    @property
    def o_point_cloud(self) -> SocketLinker:
        """Output socket: Point Cloud"""
        return self._output("Point Cloud")


class ImportOBJ(NodeBuilder):
    """Import geometry from an OBJ file"""

    name = "GeometryNodeImportOBJ"
    node: bpy.types.GeometryNodeImportOBJ

    def __init__(self, path: LINKABLE | None = "", **kwargs):
        super().__init__()
        key_args = {"Path": path}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class ImportPLY(NodeBuilder):
    """Import a point cloud from a PLY file"""

    name = "GeometryNodeImportPLY"
    node: bpy.types.GeometryNodeImportPLY

    def __init__(self, path: LINKABLE | None = "", **kwargs):
        super().__init__()
        key_args = {"Path": path}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class ImportSTL(NodeBuilder):
    """Import a mesh from an STL file"""

    name = "GeometryNodeImportSTL"
    node: bpy.types.GeometryNodeImportSTL

    def __init__(self, path: LINKABLE | None = "", **kwargs):
        super().__init__()
        key_args = {"Path": path}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class ImportText(NodeBuilder):
    """Import a string from a text file"""

    name = "GeometryNodeImportText"
    node: bpy.types.GeometryNodeImportText

    def __init__(self, path: LINKABLE | None = "", **kwargs):
        super().__init__()
        key_args = {"Path": path}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class ImportVDB(NodeBuilder):
    """Import volume data from a .vdb file"""

    name = "GeometryNodeImportVDB"
    node: bpy.types.GeometryNodeImportVDB

    def __init__(self, path: LINKABLE | None = "", **kwargs):
        super().__init__()
        key_args = {"Path": path}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_path(self) -> SocketLinker:
        """Input socket: Path"""
        return self._input("Path")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")


class IndexOfNearest(NodeBuilder):
    """Find the nearest element in a group. Similar to the "Sample Nearest" node"""

    name = "GeometryNodeIndexOfNearest"
    node: bpy.types.GeometryNodeIndexOfNearest

    def __init__(
        self,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        group_id: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Position": position, "Group ID": group_id}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_has_neighbor(self) -> SocketLinker:
        """Output socket: Has Neighbor"""
        return self._output("Has Neighbor")


class InstanceOnPoints(NodeBuilder):
    """Generate a reference to geometry at each of the input points, without duplicating its underlying data"""

    name = "GeometryNodeInstanceOnPoints"
    node: bpy.types.GeometryNodeInstanceOnPoints

    def __init__(
        self,
        points: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        instance: LINKABLE = None,
        pick_instance: TYPE_INPUT_BOOLEAN = False,
        instance_index: TYPE_INPUT_INT = 0,
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        scale: LINKABLE | None = [1.0, 1.0, 1.0],
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Points": points,
            "Selection": selection,
            "Instance": instance,
            "Pick Instance": pick_instance,
            "Instance Index": instance_index,
            "Rotation": rotation,
            "Scale": scale,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_instance(self) -> SocketLinker:
        """Input socket: Instance"""
        return self._input("Instance")

    @property
    def i_pick_instance(self) -> SocketLinker:
        """Input socket: Pick Instance"""
        return self._input("Pick Instance")

    @property
    def i_instance_index(self) -> SocketLinker:
        """Input socket: Instance Index"""
        return self._input("Instance Index")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class InstanceTransform(NodeBuilder):
    """Retrieve the full transformation of each instance in the geometry"""

    name = "GeometryNodeInstanceTransform"
    node: bpy.types.GeometryNodeInstanceTransform

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")


class InstancesToPoints(NodeBuilder):
    """Generate points at the origins of instances.
    Note: Nested instances are not affected by this node"""

    name = "GeometryNodeInstancesToPoints"
    node: bpy.types.GeometryNodeInstancesToPoints

    def __init__(
        self,
        instances: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        radius: LINKABLE | None = 0.05000000074505806,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Position": position,
            "Radius": radius,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")


class IsViewport(NodeBuilder):
    """Retrieve whether the nodes are being evaluated for the viewport rather than the final render"""

    name = "GeometryNodeIsViewport"
    node: bpy.types.GeometryNodeIsViewport

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_is_viewport(self) -> SocketLinker:
        """Output socket: Is Viewport"""
        return self._output("Is Viewport")


class List(NodeBuilder):
    """Create a list of values"""

    name = "GeometryNodeList"
    node: bpy.types.GeometryNodeList

    def __init__(
        self,
        count: TYPE_INPUT_INT = 1,
        value: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Count": count, "Value": value}
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_list(self) -> SocketLinker:
        """Output socket: List"""
        return self._output("List")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class GetListItem(NodeBuilder):
    """Retrieve a value from a list"""

    name = "GeometryNodeListGetItem"
    node: bpy.types.GeometryNodeListGetItem

    def __init__(
        self,
        list: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"List": list, "Index": index}
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_list(self) -> SocketLinker:
        """Input socket: List"""
        return self._input("List")

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class ListLength(NodeBuilder):
    """Count how many items are in a given list"""

    name = "GeometryNodeListLength"
    node: bpy.types.GeometryNodeListLength

    def __init__(
        self,
        list: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"List": list}
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_list(self) -> SocketLinker:
        """Input socket: List"""
        return self._input("List")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class MaterialSelection(NodeBuilder):
    """Provide a selection of faces that use the specified material"""

    name = "GeometryNodeMaterialSelection"
    node: bpy.types.GeometryNodeMaterialSelection

    def __init__(self, material: LINKABLE | None = None, **kwargs):
        super().__init__()
        key_args = {"Material": material}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_material(self) -> SocketLinker:
        """Input socket: Material"""
        return self._input("Material")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")


class MergeByDistance(NodeBuilder):
    """Merge vertices or points within a given distance"""

    name = "GeometryNodeMergeByDistance"
    node: bpy.types.GeometryNodeMergeByDistance

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: LINKABLE | None = "All",
        distance: LINKABLE | None = 0.0010000000474974513,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Mode": mode,
            "Distance": distance,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_distance(self) -> SocketLinker:
        """Input socket: Distance"""
        return self._input("Distance")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class MergeLayers(NodeBuilder):
    """Join groups of Grease Pencil layers into one"""

    name = "GeometryNodeMergeLayers"
    node: bpy.types.GeometryNodeMergeLayers

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        mode: Literal["MERGE_BY_NAME", "MERGE_BY_ID"] = "MERGE_BY_NAME",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grease Pencil": grease_pencil, "Selection": selection}
        key_args.update(kwargs)
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def mode(self) -> Literal["MERGE_BY_NAME", "MERGE_BY_ID"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["MERGE_BY_NAME", "MERGE_BY_ID"]):
        self.node.mode = value


class ObjectInfo(NodeBuilder):
    """Retrieve information from an object"""

    name = "GeometryNodeObjectInfo"
    node: bpy.types.GeometryNodeObjectInfo

    def __init__(
        self,
        object: LINKABLE | None = None,
        as_instance: TYPE_INPUT_BOOLEAN = False,
        transform_space: Literal["ORIGINAL", "RELATIVE"] = "ORIGINAL",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Object": object, "As Instance": as_instance}
        key_args.update(kwargs)
        self.transform_space = transform_space
        self._establish_links(**key_args)

    @property
    def i_object(self) -> SocketLinker:
        """Input socket: Object"""
        return self._input("Object")

    @property
    def i_as_instance(self) -> SocketLinker:
        """Input socket: As Instance"""
        return self._input("As Instance")

    @property
    def o_transform(self) -> SocketLinker:
        """Output socket: Transform"""
        return self._output("Transform")

    @property
    def o_location(self) -> SocketLinker:
        """Output socket: Location"""
        return self._output("Location")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")

    @property
    def o_scale(self) -> SocketLinker:
        """Output socket: Scale"""
        return self._output("Scale")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def transform_space(self) -> Literal["ORIGINAL", "RELATIVE"]:
        return self.node.transform_space

    @transform_space.setter
    def transform_space(self, value: Literal["ORIGINAL", "RELATIVE"]):
        self.node.transform_space = value


class OffsetCornerInFace(NodeBuilder):
    """Retrieve corners in the same face as another"""

    name = "GeometryNodeOffsetCornerInFace"
    node: bpy.types.GeometryNodeOffsetCornerInFace

    def __init__(
        self,
        corner_index: TYPE_INPUT_INT = 0,
        offset: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Corner Index": corner_index, "Offset": offset}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_corner_index(self) -> SocketLinker:
        """Output socket: Corner Index"""
        return self._output("Corner Index")


class Points(NodeBuilder):
    """Generate a point cloud with positions and radii defined by fields"""

    name = "GeometryNodePoints"
    node: bpy.types.GeometryNodePoints

    def __init__(
        self,
        count: TYPE_INPUT_INT = 1,
        position: LINKABLE | None = (0.0, 0.0, 0.0),
        radius: LINKABLE | None = 0.10000000149011612,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Count": count, "Position": position, "Radius": radius}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_count(self) -> SocketLinker:
        """Input socket: Count"""
        return self._input("Count")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Geometry")


class PointsToSDFGrid(NodeBuilder):
    """Create a signed distance volume grid from points"""

    name = "GeometryNodePointsToSDFGrid"
    node: bpy.types.GeometryNodePointsToSDFGrid

    def __init__(
        self,
        points: LINKABLE = None,
        radius: LINKABLE | None = 0.5,
        voxel_size: LINKABLE | None = 0.30000001192092896,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Points": points, "Radius": radius, "Voxel Size": voxel_size}
        key_args.update(kwargs)

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


class PointsToVertices(NodeBuilder):
    """Generate a mesh vertex for each point cloud point"""

    name = "GeometryNodePointsToVertices"
    node: bpy.types.GeometryNodePointsToVertices

    def __init__(
        self, points: LINKABLE = None, selection: TYPE_INPUT_BOOLEAN = True, **kwargs
    ):
        super().__init__()
        key_args = {"Points": points, "Selection": selection}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class PointsToVolume(NodeBuilder):
    """Generate a fog volume sphere around every point"""

    name = "GeometryNodePointsToVolume"
    node: bpy.types.GeometryNodePointsToVolume

    def __init__(
        self,
        points: LINKABLE = None,
        density: TYPE_INPUT_VALUE = 1.0,
        resolution_mode: LINKABLE | None = "Amount",
        voxel_size: LINKABLE | None = 0.30000001192092896,
        voxel_amount: TYPE_INPUT_VALUE = 64.0,
        radius: LINKABLE | None = 0.5,
        **kwargs,
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
        key_args.update(kwargs)

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


class GeometryProximity(NodeBuilder):
    """Compute the closest location on the target geometry"""

    name = "GeometryNodeProximity"
    node: bpy.types.GeometryNodeProximity

    def __init__(
        self,
        target: LINKABLE = None,
        group_id: TYPE_INPUT_INT = 0,
        source_position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        sample_group_id: TYPE_INPUT_INT = 0,
        target_element: Literal["POINTS", "EDGES", "FACES"] = "FACES",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Target": target,
            "Group ID": group_id,
            "Source Position": source_position,
            "Sample Group ID": sample_group_id,
        }
        key_args.update(kwargs)
        self.target_element = target_element
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Target")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Source Position")

    @property
    def i_sample_group_id(self) -> SocketLinker:
        """Input socket: Sample Group ID"""
        return self._input("Sample Group ID")

    @property
    def o_position(self) -> SocketLinker:
        """Output socket: Position"""
        return self._output("Position")

    @property
    def o_distance(self) -> SocketLinker:
        """Output socket: Distance"""
        return self._output("Distance")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def target_element(self) -> Literal["POINTS", "EDGES", "FACES"]:
        return self.node.target_element

    @target_element.setter
    def target_element(self, value: Literal["POINTS", "EDGES", "FACES"]):
        self.node.target_element = value


class Raycast(NodeBuilder):
    """Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point"""

    name = "GeometryNodeRaycast"
    node: bpy.types.GeometryNodeRaycast

    def __init__(
        self,
        target_geometry: LINKABLE = None,
        attribute: TYPE_INPUT_VALUE = 0.0,
        interpolation: LINKABLE | None = "Interpolated",
        source_position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        ray_direction: TYPE_INPUT_VECTOR = [0.0, 0.0, -1.0],
        ray_length: LINKABLE | None = 100.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Target Geometry": target_geometry,
            "Attribute": attribute,
            "Interpolation": interpolation,
            "Source Position": source_position,
            "Ray Direction": ray_direction,
            "Ray Length": ray_length,
        }
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_target_geometry(self) -> SocketLinker:
        """Input socket: Target Geometry"""
        return self._input("Target Geometry")

    @property
    def i_attribute(self) -> SocketLinker:
        """Input socket: Attribute"""
        return self._input("Attribute")

    @property
    def i_interpolation(self) -> SocketLinker:
        """Input socket: Interpolation"""
        return self._input("Interpolation")

    @property
    def i_source_position(self) -> SocketLinker:
        """Input socket: Source Position"""
        return self._input("Source Position")

    @property
    def i_ray_direction(self) -> SocketLinker:
        """Input socket: Ray Direction"""
        return self._input("Ray Direction")

    @property
    def i_ray_length(self) -> SocketLinker:
        """Input socket: Ray Length"""
        return self._input("Ray Length")

    @property
    def o_is_hit(self) -> SocketLinker:
        """Output socket: Is Hit"""
        return self._output("Is Hit")

    @property
    def o_hit_position(self) -> SocketLinker:
        """Output socket: Hit Position"""
        return self._output("Hit Position")

    @property
    def o_hit_normal(self) -> SocketLinker:
        """Output socket: Hit Normal"""
        return self._output("Hit Normal")

    @property
    def o_hit_distance(self) -> SocketLinker:
        """Output socket: Hit Distance"""
        return self._output("Hit Distance")

    @property
    def o_attribute(self) -> SocketLinker:
        """Output socket: Attribute"""
        return self._output("Attribute")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
        "STRING",
        "INT8",
        "INT16_2D",
        "INT32_2D",
        "FLOAT2",
        "BYTE_COLOR",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ],
    ):
        self.node.data_type = value


class RealizeInstances(NodeBuilder):
    """Convert instances into real geometry data"""

    name = "GeometryNodeRealizeInstances"
    node: bpy.types.GeometryNodeRealizeInstances

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        realize_all: TYPE_INPUT_BOOLEAN = True,
        depth: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Realize All": realize_all,
            "Depth": depth,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_realize_all(self) -> SocketLinker:
        """Input socket: Realize All"""
        return self._input("Realize All")

    @property
    def i_depth(self) -> SocketLinker:
        """Input socket: Depth"""
        return self._input("Depth")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class ReplaceMaterial(NodeBuilder):
    """Swap one material with another"""

    name = "GeometryNodeReplaceMaterial"
    node: bpy.types.GeometryNodeReplaceMaterial

    def __init__(
        self,
        geometry: LINKABLE = None,
        old: LINKABLE | None = None,
        new: LINKABLE | None = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Old": old, "New": new}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_old(self) -> SocketLinker:
        """Input socket: Old"""
        return self._input("Old")

    @property
    def i_new(self) -> SocketLinker:
        """Input socket: New"""
        return self._input("New")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class RotateInstances(NodeBuilder):
    """Rotate geometry instances in local or global space"""

    name = "GeometryNodeRotateInstances"
    node: bpy.types.GeometryNodeRotateInstances

    def __init__(
        self,
        instances: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        pivot_point: LINKABLE | None = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Rotation": rotation,
            "Pivot Point": pivot_point,
            "Local Space": local_space,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_pivot_point(self) -> SocketLinker:
        """Input socket: Pivot Point"""
        return self._input("Pivot Point")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SDFGridBoolean(NodeBuilder):
    """Cut, subtract, or join multiple SDF volume grid inputs"""

    name = "GeometryNodeSDFGridBoolean"
    node: bpy.types.GeometryNodeSDFGridBoolean

    def __init__(
        self,
        grid_1: TYPE_INPUT_VALUE = 0.0,
        grid_2: TYPE_INPUT_VALUE = 0.0,
        operation: Literal["INTERSECT", "UNION", "DIFFERENCE"] = "DIFFERENCE",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid 1": grid_1, "Grid 2": grid_2}
        key_args.update(kwargs)
        self.operation = operation
        self._establish_links(**key_args)

    @classmethod
    def intersect(
        cls,
        grid_1: TYPE_INPUT_VALUE = 0.0,
        grid_2: TYPE_INPUT_VALUE = 0.0,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Intersect'."""
        return cls(operation="INTERSECT", grid_1=grid_1, grid_2=grid_2)

    @classmethod
    def union(
        cls,
        grid_1: TYPE_INPUT_VALUE = 0.0,
        grid_2: TYPE_INPUT_VALUE = 0.0,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Union'."""
        return cls(operation="UNION", grid_1=grid_1, grid_2=grid_2)

    @classmethod
    def difference(
        cls,
        grid_1: TYPE_INPUT_VALUE = 0.0,
        grid_2: TYPE_INPUT_VALUE = 0.0,
    ) -> "SDFGridBoolean":
        """Create SDF Grid Boolean with operation 'Difference'."""
        return cls(operation="DIFFERENCE", grid_1=grid_1, grid_2=grid_2)

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

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}
        key_args.update(kwargs)

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

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}
        key_args.update(kwargs)

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
        grid: TYPE_INPUT_VALUE = 0.0,
        width: TYPE_INPUT_INT = 1,
        iterations: TYPE_INPUT_INT = 1,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Width": width, "Iterations": iterations}
        key_args.update(kwargs)

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
        grid: TYPE_INPUT_VALUE = 0.0,
        iterations: TYPE_INPUT_INT = 1,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Iterations": iterations}
        key_args.update(kwargs)

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
        grid: TYPE_INPUT_VALUE = 0.0,
        width: TYPE_INPUT_INT = 1,
        iterations: TYPE_INPUT_INT = 1,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Width": width, "Iterations": iterations}
        key_args.update(kwargs)

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

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        distance: LINKABLE | None = 0.10000000149011612,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Distance": distance}
        key_args.update(kwargs)

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
        grid: TYPE_INPUT_VALUE = 0.0,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        interpolation: LINKABLE | None = "Trilinear",
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Position": position, "Interpolation": interpolation}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class SampleGridIndex(NodeBuilder):
    """Retrieve volume grid values at specific voxels"""

    name = "GeometryNodeSampleGridIndex"
    node: bpy.types.GeometryNodeSampleGridIndex

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        x: TYPE_INPUT_INT = 0,
        y: TYPE_INPUT_INT = 0,
        z: TYPE_INPUT_INT = 0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "X": x, "Y": y, "Z": z}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class SampleIndex(NodeBuilder):
    """Retrieve values from specific geometry elements"""

    name = "GeometryNodeSampleIndex"
    node: bpy.types.GeometryNodeSampleIndex

    def __init__(
        self,
        geometry: LINKABLE = None,
        value: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ] = "FLOAT",
        domain: _AttributeDomains = "POINT",
        clamp: bool = False,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Value": value, "Index": index}
        key_args.update(kwargs)
        self.data_type = data_type
        self.domain = domain
        self.clamp = clamp
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_index(self) -> SocketLinker:
        """Input socket: Index"""
        return self._input("Index")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
        "STRING",
        "INT8",
        "INT16_2D",
        "INT32_2D",
        "FLOAT2",
        "BYTE_COLOR",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ],
    ):
        self.node.data_type = value

    @property
    def domain(
        self,
    ) -> _AttributeDomains:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: _AttributeDomains,
    ):
        self.node.domain = value

    @property
    def clamp(self) -> bool:
        return self.node.clamp

    @clamp.setter
    def clamp(self, value: bool):
        self.node.clamp = value


class SampleNearest(NodeBuilder):
    """Find the element of a geometry closest to a position. Similar to the "Index of Nearest" node"""

    name = "GeometryNodeSampleNearest"
    node: bpy.types.GeometryNodeSampleNearest

    def __init__(
        self,
        geometry: LINKABLE = None,
        sample_position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        domain: Literal["POINT", "EDGE", "FACE", "CORNER"] = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Sample Position": sample_position}
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Sample Position")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CORNER"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CORNER"]):
        self.node.domain = value


class SampleNearestSurface(NodeBuilder):
    """Calculate the interpolated value of a mesh attribute on the closest point of its surface"""

    name = "GeometryNodeSampleNearestSurface"
    node: bpy.types.GeometryNodeSampleNearestSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        value: TYPE_INPUT_VALUE = 0.0,
        group_id: TYPE_INPUT_INT = 0,
        sample_position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        sample_group_id: TYPE_INPUT_INT = 0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Value": value,
            "Group ID": group_id,
            "Sample Position": sample_position,
            "Sample Group ID": sample_group_id,
        }
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sample_position(self) -> SocketLinker:
        """Input socket: Sample Position"""
        return self._input("Sample Position")

    @property
    def i_sample_group_id(self) -> SocketLinker:
        """Input socket: Sample Group ID"""
        return self._input("Sample Group ID")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
        "STRING",
        "INT8",
        "INT16_2D",
        "INT32_2D",
        "FLOAT2",
        "BYTE_COLOR",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ],
    ):
        self.node.data_type = value


class SampleUVSurface(NodeBuilder):
    """Calculate the interpolated values of a mesh attribute at a UV coordinate"""

    name = "GeometryNodeSampleUVSurface"
    node: bpy.types.GeometryNodeSampleUVSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        value: TYPE_INPUT_VALUE = 0.0,
        source_uv_map: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        sample_uv: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Value": value,
            "Source UV Map": source_uv_map,
            "Sample UV": sample_uv,
        }
        key_args.update(kwargs)
        self.data_type = data_type
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def i_uv_map(self) -> SocketLinker:
        """Input socket: UV Map"""
        return self._input("Source UV Map")

    @property
    def i_sample_uv(self) -> SocketLinker:
        """Input socket: Sample UV"""
        return self._input("Sample UV")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def o_is_valid(self) -> SocketLinker:
        """Output socket: Is Valid"""
        return self._output("Is Valid")

    @property
    def data_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "FLOAT_VECTOR",
        "FLOAT_COLOR",
        "QUATERNION",
        "FLOAT4X4",
        "STRING",
        "INT8",
        "INT16_2D",
        "INT32_2D",
        "FLOAT2",
        "BYTE_COLOR",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "FLOAT_VECTOR",
            "FLOAT_COLOR",
            "QUATERNION",
            "FLOAT4X4",
            "STRING",
            "INT8",
            "INT16_2D",
            "INT32_2D",
            "FLOAT2",
            "BYTE_COLOR",
        ],
    ):
        self.node.data_type = value


class ScaleElements(NodeBuilder):
    """Scale groups of connected edges and faces"""

    name = "GeometryNodeScaleElements"
    node: bpy.types.GeometryNodeScaleElements

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: TYPE_INPUT_VALUE = 1.0,
        center: LINKABLE | None = (0.0, 0.0, 0.0),
        scale_mode: LINKABLE | None = "Uniform",
        axis: TYPE_INPUT_VECTOR = [1.0, 0.0, 0.0],
        domain: Literal["FACE", "EDGE"] = "FACE",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Scale": scale,
            "Center": center,
            "Scale Mode": scale_mode,
            "Axis": axis,
        }
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_center(self) -> SocketLinker:
        """Input socket: Center"""
        return self._input("Center")

    @property
    def i_scale_mode(self) -> SocketLinker:
        """Input socket: Scale Mode"""
        return self._input("Scale Mode")

    @property
    def i_axis(self) -> SocketLinker:
        """Input socket: Axis"""
        return self._input("Axis")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["FACE", "EDGE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["FACE", "EDGE"]):
        self.node.domain = value


class ScaleInstances(NodeBuilder):
    """Scale geometry instances in local or global space"""

    name = "GeometryNodeScaleInstances"
    node: bpy.types.GeometryNodeScaleInstances

    def __init__(
        self,
        instances: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        scale: LINKABLE | None = [1.0, 1.0, 1.0],
        center: LINKABLE | None = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Scale": scale,
            "Center": center,
            "Local Space": local_space,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_center(self) -> SocketLinker:
        """Input socket: Center"""
        return self._input("Center")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SelfObject(NodeBuilder):
    """Retrieve the object that contains the geometry nodes modifier currently being executed"""

    name = "GeometryNodeSelfObject"
    node: bpy.types.GeometryNodeSelfObject

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_self_object(self) -> SocketLinker:
        """Output socket: Self Object"""
        return self._output("Self Object")


class SeparateComponents(NodeBuilder):
    """Split a geometry into a separate output for each type of data in the geometry"""

    name = "GeometryNodeSeparateComponents"
    node: bpy.types.GeometryNodeSeparateComponents

    def __init__(self, geometry: LINKABLE = None, **kwargs):
        super().__init__()
        key_args = {"Geometry": geometry}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def o_point_cloud(self) -> SocketLinker:
        """Output socket: Point Cloud"""
        return self._output("Point Cloud")

    @property
    def o_volume(self) -> SocketLinker:
        """Output socket: Volume"""
        return self._output("Volume")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SeparateGeometry(NodeBuilder):
    """Split a geometry into two geometry outputs based on a selection"""

    name = "GeometryNodeSeparateGeometry"
    node: bpy.types.GeometryNodeSeparateGeometry

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")

    @property
    def o_inverted(self) -> SocketLinker:
        """Output socket: Inverted"""
        return self._output("Inverted")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]
    ):
        self.node.domain = value


class SetGeometryName(NodeBuilder):
    """Set the name of a geometry for easier debugging"""

    name = "GeometryNodeSetGeometryName"
    node: bpy.types.GeometryNodeSetGeometryName

    def __init__(
        self, geometry: LINKABLE = None, name: str | LINKABLE | None = "", **kwargs
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Name": name}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_name(self) -> SocketLinker:
        """Input socket: Name"""
        return self._input("Name")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetGreasePencilColor(NodeBuilder):
    """Set color and opacity attributes on Grease Pencil geometry"""

    name = "GeometryNodeSetGreasePencilColor"
    node: bpy.types.GeometryNodeSetGreasePencilColor

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        color: tuple[float, float, float, float] | LINKABLE | None = [
            1.0,
            1.0,
            1.0,
            1.0,
        ],
        opacity: TYPE_INPUT_VALUE = 1.0,
        mode: Literal["STROKE", "FILL"] = "STROKE",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Color": color,
            "Opacity": opacity,
        }
        key_args.update(kwargs)
        self.mode = mode
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def i_opacity(self) -> SocketLinker:
        """Input socket: Opacity"""
        return self._input("Opacity")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def mode(self) -> Literal["STROKE", "FILL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["STROKE", "FILL"]):
        self.node.mode = value


class SetGreasePencilDepth(NodeBuilder):
    """Set the Grease Pencil depth order to use"""

    name = "GeometryNodeSetGreasePencilDepth"
    node: bpy.types.GeometryNodeSetGreasePencilDepth

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        depth_order: Literal["2D", "3D"] = "2D",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grease Pencil": grease_pencil}
        key_args.update(kwargs)
        self.depth_order = depth_order
        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")

    @property
    def depth_order(self) -> Literal["2D", "3D"]:
        return self.node.depth_order

    @depth_order.setter
    def depth_order(self, value: Literal["2D", "3D"]):
        self.node.depth_order = value


class SetGreasePencilSoftness(NodeBuilder):
    """Set softness attribute on Grease Pencil geometry"""

    name = "GeometryNodeSetGreasePencilSoftness"
    node: bpy.types.GeometryNodeSetGreasePencilSoftness

    def __init__(
        self,
        grease_pencil: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        softness: TYPE_INPUT_VALUE = 0.0,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Grease Pencil": grease_pencil,
            "Selection": selection,
            "Softness": softness,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_grease_pencil(self) -> SocketLinker:
        """Input socket: Grease Pencil"""
        return self._input("Grease Pencil")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_softness(self) -> SocketLinker:
        """Input socket: Softness"""
        return self._input("Softness")

    @property
    def o_grease_pencil(self) -> SocketLinker:
        """Output socket: Grease Pencil"""
        return self._output("Grease Pencil")


class SetGridBackground(NodeBuilder):
    """Set the background value used for inactive voxels and tiles"""

    name = "GeometryNodeSetGridBackground"
    node: bpy.types.GeometryNodeSetGridBackground

    def __init__(
        self,
        grid: TYPE_INPUT_VALUE = 0.0,
        background: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Background": background}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
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
        data_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Grid": grid, "Transform": transform}
        key_args.update(kwargs)
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
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.data_type = value


class SetID(NodeBuilder):
    """Set the id attribute on the input geometry, mainly used internally for randomizing"""

    name = "GeometryNodeSetID"
    node: bpy.types.GeometryNodeSetID

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        id: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "ID": id}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_id(self) -> SocketLinker:
        """Input socket: ID"""
        return self._input("ID")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetInstanceTransform(NodeBuilder):
    """Set the transformation matrix of every instance"""

    name = "GeometryNodeSetInstanceTransform"
    node: bpy.types.GeometryNodeSetInstanceTransform

    def __init__(
        self,
        instances: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        transform: LINKABLE | None = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Transform": transform,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class SetMaterial(NodeBuilder):
    """Assign a material to geometry elements"""

    name = "GeometryNodeSetMaterial"
    node: bpy.types.GeometryNodeSetMaterial

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        material: LINKABLE | None = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Material": material}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_material(self) -> SocketLinker:
        """Input socket: Material"""
        return self._input("Material")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetMaterialIndex(NodeBuilder):
    """Set the material index for each selected geometry element"""

    name = "GeometryNodeSetMaterialIndex"
    node: bpy.types.GeometryNodeSetMaterialIndex

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        material_index: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Material Index": material_index,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_material_index(self) -> SocketLinker:
        """Input socket: Material Index"""
        return self._input("Material Index")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetPointRadius(NodeBuilder):
    """Set the display size of point cloud points"""

    name = "GeometryNodeSetPointRadius"
    node: bpy.types.GeometryNodeSetPointRadius

    def __init__(
        self,
        points: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        radius: LINKABLE | None = 0.05000000074505806,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Points": points, "Selection": selection, "Radius": radius}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_points(self) -> SocketLinker:
        """Input socket: Points"""
        return self._input("Points")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_radius(self) -> SocketLinker:
        """Input socket: Radius"""
        return self._input("Radius")

    @property
    def o_points(self) -> SocketLinker:
        """Output socket: Points"""
        return self._output("Points")


class SetPosition(NodeBuilder):
    """Set the location of each point"""

    name = "GeometryNodeSetPosition"
    node: bpy.types.GeometryNodeSetPosition

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        position: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        offset: LINKABLE | None = (0.0, 0.0, 0.0),
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Position": position,
            "Offset": offset,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_position(self) -> SocketLinker:
        """Input socket: Position"""
        return self._input("Position")

    @property
    def i_offset(self) -> SocketLinker:
        """Input socket: Offset"""
        return self._input("Offset")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class SetShadeSmooth(NodeBuilder):
    """Control the smoothness of mesh normals around each face by changing the "shade smooth" attribute"""

    name = "GeometryNodeSetShadeSmooth"
    node: bpy.types.GeometryNodeSetShadeSmooth

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        shade_smooth: TYPE_INPUT_BOOLEAN = True,
        domain: Literal["EDGE", "FACE"] = "FACE",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Shade Smooth": shade_smooth,
        }
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_shade_smooth(self) -> SocketLinker:
        """Input socket: Shade Smooth"""
        return self._input("Shade Smooth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["EDGE", "FACE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["EDGE", "FACE"]):
        self.node.domain = value


class SetSplineCyclic(NodeBuilder):
    """Control whether each spline loops back on itself by changing the "cyclic" attribute"""

    name = "GeometryNodeSetSplineCyclic"
    node: bpy.types.GeometryNodeSetSplineCyclic

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        cyclic: TYPE_INPUT_BOOLEAN = False,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Cyclic": cyclic}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_cyclic(self) -> SocketLinker:
        """Input socket: Cyclic"""
        return self._input("Cyclic")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Geometry")


class SetSplineResolution(NodeBuilder):
    """Control how many evaluated points should be generated on every curve segment"""

    name = "GeometryNodeSetSplineResolution"
    node: bpy.types.GeometryNodeSetSplineResolution

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        resolution: TYPE_INPUT_INT = 12,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Resolution": resolution,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_resolution(self) -> SocketLinker:
        """Input socket: Resolution"""
        return self._input("Resolution")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Geometry")


class SortElements(NodeBuilder):
    """Rearrange geometry elements, changing their indices"""

    name = "GeometryNodeSortElements"
    node: bpy.types.GeometryNodeSortElements

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        sort_weight: TYPE_INPUT_VALUE = 0.0,
        domain: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"] = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Selection": selection,
            "Group ID": group_id,
            "Sort Weight": sort_weight,
        }
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def i_sort_weight(self) -> SocketLinker:
        """Input socket: Sort Weight"""
        return self._input("Sort Weight")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE"]):
        self.node.domain = value


class SplineLength(NodeBuilder):
    """Retrieve the total length of each spline, as a distance or as a number of points"""

    name = "GeometryNodeSplineLength"
    node: bpy.types.GeometryNodeSplineLength

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def o_point_count(self) -> SocketLinker:
        """Output socket: Point Count"""
        return self._output("Point Count")


class SplineParameter(NodeBuilder):
    """Retrieve how far along each spline a control point is"""

    name = "GeometryNodeSplineParameter"
    node: bpy.types.GeometryNodeSplineParameter

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_factor(self) -> SocketLinker:
        """Output socket: Factor"""
        return self._output("Factor")

    @property
    def o_length(self) -> SocketLinker:
        """Output socket: Length"""
        return self._output("Length")

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")


class SplitEdges(NodeBuilder):
    """Duplicate mesh edges and break connections with the surrounding faces"""

    name = "GeometryNodeSplitEdges"
    node: bpy.types.GeometryNodeSplitEdges

    def __init__(
        self, mesh: LINKABLE = None, selection: TYPE_INPUT_BOOLEAN = True, **kwargs
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SplitToInstances(NodeBuilder):
    """Create separate geometries containing the elements from the same group"""

    name = "GeometryNodeSplitToInstances"
    node: bpy.types.GeometryNodeSplitToInstances

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        group_id: TYPE_INPUT_INT = 0,
        domain: Literal[
            "POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"
        ] = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection, "Group ID": group_id}
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_group_id(self) -> SocketLinker:
        """Input socket: Group ID"""
        return self._input("Group ID")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")

    @property
    def o_group_id(self) -> SocketLinker:
        """Output socket: Group ID"""
        return self._output("Group ID")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(
        self, value: Literal["POINT", "EDGE", "FACE", "CURVE", "INSTANCE", "LAYER"]
    ):
        self.node.domain = value


class StoreNamedGrid(NodeBuilder):
    """Store grid data in a volume geometry with the specified name"""

    name = "GeometryNodeStoreNamedGrid"
    node: bpy.types.GeometryNodeStoreNamedGrid

    def __init__(
        self,
        volume: LINKABLE = None,
        name: str | LINKABLE | None = "",
        grid: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "BOOLEAN",
            "FLOAT",
            "DOUBLE",
            "INT",
            "INT64",
            "MASK",
            "VECTOR_FLOAT",
            "VECTOR_DOUBLE",
            "VECTOR_INT",
            "POINTS",
            "UNKNOWN",
        ] = "FLOAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Volume": volume, "Name": name, "Grid": grid}
        key_args.update(kwargs)
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
    ) -> Literal[
        "BOOLEAN",
        "FLOAT",
        "DOUBLE",
        "INT",
        "INT64",
        "MASK",
        "VECTOR_FLOAT",
        "VECTOR_DOUBLE",
        "VECTOR_INT",
        "POINTS",
        "UNKNOWN",
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "BOOLEAN",
            "FLOAT",
            "DOUBLE",
            "INT",
            "INT64",
            "MASK",
            "VECTOR_FLOAT",
            "VECTOR_DOUBLE",
            "VECTOR_INT",
            "POINTS",
            "UNKNOWN",
        ],
    ):
        self.node.data_type = value


class JoinStrings(NodeBuilder):
    """Combine any number of input strings"""

    name = "GeometryNodeStringJoin"
    node: bpy.types.GeometryNodeStringJoin

    def __init__(
        self,
        delimiter: str | LINKABLE | None = "",
        strings: str | LINKABLE | None = "",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Delimiter": delimiter, "Strings": strings}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_delimiter(self) -> SocketLinker:
        """Input socket: Delimiter"""
        return self._input("Delimiter")

    @property
    def i_strings(self) -> SocketLinker:
        """Input socket: Strings"""
        return self._input("Strings")

    @property
    def o_string(self) -> SocketLinker:
        """Output socket: String"""
        return self._output("String")


class SubdivisionSurface(NodeBuilder):
    """Divide mesh faces to form a smooth surface, using the Catmull-Clark subdivision method"""

    name = "GeometryNodeSubdivisionSurface"
    node: bpy.types.GeometryNodeSubdivisionSurface

    def __init__(
        self,
        mesh: LINKABLE = None,
        level: TYPE_INPUT_INT = 1,
        edge_crease: LINKABLE | None = 0.0,
        vertex_crease: LINKABLE | None = 0.0,
        limit_surface: TYPE_INPUT_BOOLEAN = True,
        uv_smooth: LINKABLE | None = "Keep Boundaries",
        boundary_smooth: LINKABLE | None = "All",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Level": level,
            "Edge Crease": edge_crease,
            "Vertex Crease": vertex_crease,
            "Limit Surface": limit_surface,
            "UV Smooth": uv_smooth,
            "Boundary Smooth": boundary_smooth,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_level(self) -> SocketLinker:
        """Input socket: Level"""
        return self._input("Level")

    @property
    def i_edge_crease(self) -> SocketLinker:
        """Input socket: Edge Crease"""
        return self._input("Edge Crease")

    @property
    def i_vertex_crease(self) -> SocketLinker:
        """Input socket: Vertex Crease"""
        return self._input("Vertex Crease")

    @property
    def i_limit_surface(self) -> SocketLinker:
        """Input socket: Limit Surface"""
        return self._input("Limit Surface")

    @property
    def i_uv_smooth(self) -> SocketLinker:
        """Input socket: UV Smooth"""
        return self._input("UV Smooth")

    @property
    def i_boundary_smooth(self) -> SocketLinker:
        """Input socket: Boundary Smooth"""
        return self._input("Boundary Smooth")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class Switch(NodeBuilder):
    """Switch between two inputs"""

    name = "GeometryNodeSwitch"
    node: bpy.types.GeometryNodeSwitch

    def __init__(
        self,
        switch: TYPE_INPUT_BOOLEAN = False,
        false: LINKABLE = None,
        true: LINKABLE = None,
        input_type: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ] = "GEOMETRY",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Switch": switch, "False": false, "True": true}
        key_args.update(kwargs)
        self.input_type = input_type
        self._establish_links(**key_args)

    @property
    def i_switch(self) -> SocketLinker:
        """Input socket: Switch"""
        return self._input("Switch")

    @property
    def i_false(self) -> SocketLinker:
        """Input socket: False"""
        return self._input("False")

    @property
    def i_true(self) -> SocketLinker:
        """Input socket: True"""
        return self._input("True")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def input_type(
        self,
    ) -> Literal[
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGBA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "MENU",
        "SHADER",
        "OBJECT",
        "IMAGE",
        "GEOMETRY",
        "COLLECTION",
        "TEXTURE",
        "MATERIAL",
        "BUNDLE",
        "CLOSURE",
    ]:
        return self.node.input_type

    @input_type.setter
    def input_type(
        self,
        value: Literal[
            "FLOAT",
            "INT",
            "BOOLEAN",
            "VECTOR",
            "RGBA",
            "ROTATION",
            "MATRIX",
            "STRING",
            "MENU",
            "SHADER",
            "OBJECT",
            "IMAGE",
            "GEOMETRY",
            "COLLECTION",
            "TEXTURE",
            "MATERIAL",
            "BUNDLE",
            "CLOSURE",
        ],
    ):
        self.node.input_type = value


class DCursor3(NodeBuilder):
    """The scene's 3D cursor location and rotation"""

    name = "GeometryNodeTool3DCursor"
    node: bpy.types.GeometryNodeTool3DCursor

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_location(self) -> SocketLinker:
        """Output socket: Location"""
        return self._output("Location")

    @property
    def o_rotation(self) -> SocketLinker:
        """Output socket: Rotation"""
        return self._output("Rotation")


class ActiveElement(NodeBuilder):
    """Active element indices of the edited geometry, for tool execution"""

    name = "GeometryNodeToolActiveElement"
    node: bpy.types.GeometryNodeToolActiveElement

    def __init__(
        self, domain: Literal["POINT", "EDGE", "FACE", "LAYER"] = "POINT", **kwargs
    ):
        super().__init__()
        key_args = kwargs
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def o_index(self) -> SocketLinker:
        """Output socket: Index"""
        return self._output("Index")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "LAYER"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "LAYER"]):
        self.node.domain = value


class FaceSet(NodeBuilder):
    """Each face's sculpt face set value"""

    name = "GeometryNodeToolFaceSet"
    node: bpy.types.GeometryNodeToolFaceSet

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_face_set(self) -> SocketLinker:
        """Output socket: Face Set"""
        return self._output("Face Set")

    @property
    def o_exists(self) -> SocketLinker:
        """Output socket: Exists"""
        return self._output("Exists")


class MousePosition(NodeBuilder):
    """Retrieve the position of the mouse cursor"""

    name = "GeometryNodeToolMousePosition"
    node: bpy.types.GeometryNodeToolMousePosition

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_mouse_x(self) -> SocketLinker:
        """Output socket: Mouse X"""
        return self._output("Mouse X")

    @property
    def o_mouse_y(self) -> SocketLinker:
        """Output socket: Mouse Y"""
        return self._output("Mouse Y")

    @property
    def o_region_width(self) -> SocketLinker:
        """Output socket: Region Width"""
        return self._output("Region Width")

    @property
    def o_region_height(self) -> SocketLinker:
        """Output socket: Region Height"""
        return self._output("Region Height")


class Selection(NodeBuilder):
    """User selection of the edited geometry, for tool execution"""

    name = "GeometryNodeToolSelection"
    node: bpy.types.GeometryNodeToolSelection

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_boolean(self) -> SocketLinker:
        """Output socket: Boolean"""
        return self._output("Selection")

    @property
    def o_float(self) -> SocketLinker:
        """Output socket: Float"""
        return self._output("Float")


class SetFaceSet(NodeBuilder):
    """Set sculpt face set values for faces"""

    name = "GeometryNodeToolSetFaceSet"
    node: bpy.types.GeometryNodeToolSetFaceSet

    def __init__(
        self,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        face_set: TYPE_INPUT_INT = 0,
        **kwargs,
    ):
        super().__init__()
        key_args = {"Mesh": mesh, "Selection": selection, "Face Set": face_set}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_face_set(self) -> SocketLinker:
        """Input socket: Face Set"""
        return self._input("Face Set")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class SetSelection(NodeBuilder):
    """Set selection of the edited geometry, for tool execution"""

    name = "GeometryNodeToolSetSelection"
    node: bpy.types.GeometryNodeToolSetSelection

    def __init__(
        self,
        geometry: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        domain: Literal["POINT", "EDGE", "FACE", "CURVE"] = "POINT",
        selection_type: Literal["BOOLEAN", "FLOAT"] = "BOOLEAN",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry, "Selection": selection}
        key_args.update(kwargs)
        self.domain = domain
        self.selection_type = selection_type
        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

    @property
    def domain(self) -> Literal["POINT", "EDGE", "FACE", "CURVE"]:
        return self.node.domain

    @domain.setter
    def domain(self, value: Literal["POINT", "EDGE", "FACE", "CURVE"]):
        self.node.domain = value

    @property
    def selection_type(self) -> Literal["BOOLEAN", "FLOAT"]:
        return self.node.selection_type

    @selection_type.setter
    def selection_type(self, value: Literal["BOOLEAN", "FLOAT"]):
        self.node.selection_type = value


class TransformGeometry(NodeBuilder):
    """Translate, rotate or scale the geometry"""

    name = "GeometryNodeTransform"
    node: bpy.types.GeometryNodeTransform

    def __init__(
        self,
        geometry: LINKABLE = None,
        mode: LINKABLE | None = "Components",
        translation: LINKABLE | None = (0.0, 0.0, 0.0),
        rotation: TYPE_INPUT_ROTATION = (0.0, 0.0, 0.0),
        scale: LINKABLE | None = [1.0, 1.0, 1.0],
        transform: LINKABLE | None = None,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Geometry": geometry,
            "Mode": mode,
            "Translation": translation,
            "Rotation": rotation,
            "Scale": scale,
            "Transform": transform,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def i_mode(self) -> SocketLinker:
        """Input socket: Mode"""
        return self._input("Mode")

    @property
    def i_translation(self) -> SocketLinker:
        """Input socket: Translation"""
        return self._input("Translation")

    @property
    def i_rotation(self) -> SocketLinker:
        """Input socket: Rotation"""
        return self._input("Rotation")

    @property
    def i_scale(self) -> SocketLinker:
        """Input socket: Scale"""
        return self._input("Scale")

    @property
    def i_transform(self) -> SocketLinker:
        """Input socket: Transform"""
        return self._input("Transform")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")


class TranslateInstances(NodeBuilder):
    """Move top-level geometry instances in local or global space"""

    name = "GeometryNodeTranslateInstances"
    node: bpy.types.GeometryNodeTranslateInstances

    def __init__(
        self,
        instances: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        translation: LINKABLE | None = (0.0, 0.0, 0.0),
        local_space: TYPE_INPUT_BOOLEAN = True,
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Instances": instances,
            "Selection": selection,
            "Translation": translation,
            "Local Space": local_space,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_instances(self) -> SocketLinker:
        """Input socket: Instances"""
        return self._input("Instances")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_translation(self) -> SocketLinker:
        """Input socket: Translation"""
        return self._input("Translation")

    @property
    def i_local_space(self) -> SocketLinker:
        """Input socket: Local Space"""
        return self._input("Local Space")

    @property
    def o_instances(self) -> SocketLinker:
        """Output socket: Instances"""
        return self._output("Instances")


class Triangulate(NodeBuilder):
    """Convert all faces in a mesh to triangular faces"""

    name = "GeometryNodeTriangulate"
    node: bpy.types.GeometryNodeTriangulate

    def __init__(
        self,
        mesh: LINKABLE = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        quad_method: LINKABLE | None = "Shortest Diagonal",
        n_gon_method: LINKABLE | None = "Beauty",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Mesh": mesh,
            "Selection": selection,
            "Quad Method": quad_method,
            "N-gon Method": n_gon_method,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_mesh(self) -> SocketLinker:
        """Input socket: Mesh"""
        return self._input("Mesh")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_quad_method(self) -> SocketLinker:
        """Input socket: Quad Method"""
        return self._input("Quad Method")

    @property
    def i_n_gon_method(self) -> SocketLinker:
        """Input socket: N-gon Method"""
        return self._input("N-gon Method")

    @property
    def o_mesh(self) -> SocketLinker:
        """Output socket: Mesh"""
        return self._output("Mesh")


class PackUVIslands(NodeBuilder):
    """Scale islands of a UV map and move them so they fill the UV space as much as possible"""

    name = "GeometryNodeUVPackIslands"
    node: bpy.types.GeometryNodeUVPackIslands

    def __init__(
        self,
        uv: TYPE_INPUT_VECTOR = (0.0, 0.0, 0.0),
        selection: TYPE_INPUT_BOOLEAN = True,
        margin: TYPE_INPUT_VALUE = 0.0010000000474974513,
        rotate: TYPE_INPUT_BOOLEAN = True,
        method: LINKABLE | None = "Bounding Box",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "UV": uv,
            "Selection": selection,
            "Margin": margin,
            "Rotate": rotate,
            "Method": method,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_uv(self) -> SocketLinker:
        """Input socket: UV"""
        return self._input("UV")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_margin(self) -> SocketLinker:
        """Input socket: Margin"""
        return self._input("Margin")

    @property
    def i_rotate(self) -> SocketLinker:
        """Input socket: Rotate"""
        return self._input("Rotate")

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def o_uv(self) -> SocketLinker:
        """Output socket: UV"""
        return self._output("UV")


class UVTangent(NodeBuilder):
    """Generate tangent directions based on a UV map"""

    name = "GeometryNodeUVTangent"
    node: bpy.types.GeometryNodeUVTangent

    def __init__(
        self,
        method: LINKABLE | None = "Exact",
        uv: LINKABLE | None = [0.0, 0.0],
        **kwargs,
    ):
        super().__init__()
        key_args = {"Method": method, "UV": uv}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def i_uv(self) -> SocketLinker:
        """Input socket: UV"""
        return self._input("UV")

    @property
    def o_tangent(self) -> SocketLinker:
        """Output socket: Tangent"""
        return self._output("Tangent")


class UVUnwrap(NodeBuilder):
    """Generate a UV map based on seam edges"""

    name = "GeometryNodeUVUnwrap"
    node: bpy.types.GeometryNodeUVUnwrap

    def __init__(
        self,
        selection: TYPE_INPUT_BOOLEAN = True,
        seam: TYPE_INPUT_BOOLEAN = False,
        margin: TYPE_INPUT_VALUE = 0.0010000000474974513,
        fill_holes: TYPE_INPUT_BOOLEAN = True,
        method: LINKABLE | None = "Angle Based",
        **kwargs,
    ):
        super().__init__()
        key_args = {
            "Selection": selection,
            "Seam": seam,
            "Margin": margin,
            "Fill Holes": fill_holes,
            "Method": method,
        }
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def i_seam(self) -> SocketLinker:
        """Input socket: Seam"""
        return self._input("Seam")

    @property
    def i_margin(self) -> SocketLinker:
        """Input socket: Margin"""
        return self._input("Margin")

    @property
    def i_fill_holes(self) -> SocketLinker:
        """Input socket: Fill Holes"""
        return self._input("Fill Holes")

    @property
    def i_method(self) -> SocketLinker:
        """Input socket: Method"""
        return self._input("Method")

    @property
    def o_uv(self) -> SocketLinker:
        """Output socket: UV"""
        return self._output("UV")


class VertexOfCorner(NodeBuilder):
    """Retrieve the vertex each face corner is attached to"""

    name = "GeometryNodeVertexOfCorner"
    node: bpy.types.GeometryNodeVertexOfCorner

    def __init__(self, corner_index: TYPE_INPUT_INT = 0, **kwargs):
        super().__init__()
        key_args = {"Corner Index": corner_index}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_corner_index(self) -> SocketLinker:
        """Input socket: Corner Index"""
        return self._input("Corner Index")

    @property
    def o_vertex_index(self) -> SocketLinker:
        """Output socket: Vertex Index"""
        return self._output("Vertex Index")


class Viewer(NodeBuilder):
    """Display the input data in the Spreadsheet Editor"""

    name = "GeometryNodeViewer"
    node: bpy.types.GeometryNodeViewer

    def __init__(
        self,
        extend: LINKABLE | None = None,
        ui_shortcut: int = 0,
        active_index: int = 0,
        domain: Literal[
            "AUTO", "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "AUTO",
        **kwargs,
    ):
        super().__init__()
        key_args = {"__extend__": extend}
        key_args.update(kwargs)
        self.ui_shortcut = ui_shortcut
        self.active_index = active_index
        self.domain = domain
        self._establish_links(**key_args)

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def ui_shortcut(self) -> int:
        return self.node.ui_shortcut

    @ui_shortcut.setter
    def ui_shortcut(self, value: int):
        self.node.ui_shortcut = value

    @property
    def active_index(self) -> int:
        return self.node.active_index

    @active_index.setter
    def active_index(self, value: int):
        self.node.active_index = value

    @property
    def domain(
        self,
    ) -> Literal[
        "AUTO", "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
    ]:
        return self.node.domain

    @domain.setter
    def domain(
        self,
        value: Literal[
            "AUTO", "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ],
    ):
        self.node.domain = value


class ViewportTransform(NodeBuilder):
    """Retrieve the view direction and location of the 3D viewport"""

    name = "GeometryNodeViewportTransform"
    node: bpy.types.GeometryNodeViewportTransform

    def __init__(self, **kwargs):
        super().__init__()
        key_args = kwargs

        self._establish_links(**key_args)

    @property
    def o_projection(self) -> SocketLinker:
        """Output socket: Projection"""
        return self._output("Projection")

    @property
    def o_view(self) -> SocketLinker:
        """Output socket: View"""
        return self._output("View")

    @property
    def o_is_orthographic(self) -> SocketLinker:
        """Output socket: Is Orthographic"""
        return self._output("Is Orthographic")


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


class Warning(NodeBuilder):
    """Create custom warnings in node groups"""

    name = "GeometryNodeWarning"
    node: bpy.types.GeometryNodeWarning

    def __init__(
        self,
        show: TYPE_INPUT_BOOLEAN = True,
        message: str | LINKABLE | None = "",
        warning_type: Literal["ERROR", "WARNING", "INFO"] = "ERROR",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Show": show, "Message": message}
        key_args.update(kwargs)
        self.warning_type = warning_type
        self._establish_links(**key_args)

    @property
    def i_show(self) -> SocketLinker:
        """Input socket: Show"""
        return self._input("Show")

    @property
    def i_message(self) -> SocketLinker:
        """Input socket: Message"""
        return self._input("Message")

    @property
    def o_show(self) -> SocketLinker:
        """Output socket: Show"""
        return self._output("Show")

    @property
    def warning_type(self) -> Literal["ERROR", "WARNING", "INFO"]:
        return self.node.warning_type

    @warning_type.setter
    def warning_type(self, value: Literal["ERROR", "WARNING", "INFO"]):
        self.node.warning_type = value


class Bake(NodeBuilder):
    """Cache the incoming data so that it can be used without recomputation"""

    name = "GeometryNodeBake"
    node: bpy.types.GeometryNodeBake

    def __init__(self, extend: LINKABLE | None = None, active_index: int = 0, **kwargs):
        super().__init__()
        key_args = {"__extend__": extend}
        key_args.update(kwargs)
        self.active_index = active_index
        self._establish_links(**key_args)

    @property
    def i_input_socket(self) -> SocketLinker:
        """Input socket:"""
        return self._input("__extend__")

    @property
    def o_input_socket(self) -> SocketLinker:
        """Output socket:"""
        return self._output("__extend__")

    @property
    def active_index(self) -> int:
        return self.node.active_index

    @active_index.setter
    def active_index(self, value: int):
        self.node.active_index = value
