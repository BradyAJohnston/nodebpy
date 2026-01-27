from typing import Literal

import bpy

from ..builder import NodeBuilder


class Viewer(NodeBuilder):
    """
    Display the input data in the Spreadsheet Editor
    """

    _bl_idname = "GeometryNodeViewer"
    node: bpy.types.GeometryNodeViewer

    def __init__(
        self,
        ui_shortcut: int = 0,
        domain: Literal[
            "AUTO", "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "AUTO",
    ):
        super().__init__()
        key_args = {}
        self.ui_shortcut = ui_shortcut
        self.domain = domain
        self._establish_links(**key_args)

    @classmethod
    def auto(cls) -> "Viewer":
        """Create Viewer with operation 'Auto'."""
        return cls(domain="AUTO")

    @classmethod
    def point(cls) -> "Viewer":
        """Create Viewer with operation 'Point'."""
        return cls(domain="POINT")

    @classmethod
    def edge(cls) -> "Viewer":
        """Create Viewer with operation 'Edge'."""
        return cls(domain="EDGE")

    @classmethod
    def face(cls) -> "Viewer":
        """Create Viewer with operation 'Face'."""
        return cls(domain="FACE")

    @classmethod
    def face_corner(cls) -> "Viewer":
        """Create Viewer with operation 'Face Corner'."""
        return cls(domain="CORNER")

    @classmethod
    def spline(cls) -> "Viewer":
        """Create Viewer with operation 'Spline'."""
        return cls(domain="CURVE")

    @classmethod
    def instance(cls) -> "Viewer":
        """Create Viewer with operation 'Instance'."""
        return cls(domain="INSTANCE")

    @classmethod
    def layer(cls) -> "Viewer":
        """Create Viewer with operation 'Layer'."""
        return cls(domain="LAYER")

    @property
    def ui_shortcut(self) -> int:
        return self.node.ui_shortcut

    @ui_shortcut.setter
    def ui_shortcut(self, value: int):
        self.node.ui_shortcut = value

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
