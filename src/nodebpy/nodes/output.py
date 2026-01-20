from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class Viewer(NodeBuilder):
    """Display the input data in the Spreadsheet Editor"""

    name = "GeometryNodeViewer"
    node: bpy.types.GeometryNodeViewer

    def __init__(
        self,
        extend: None = None,
        ui_shortcut: int = 0,
        domain: Literal[
            "AUTO", "POINT", "EDGE", "FACE", "CORNER", "CURVE", "INSTANCE", "LAYER"
        ] = "AUTO",
    ):
        super().__init__()
        key_args = {"__extend__": extend}
        self.ui_shortcut = ui_shortcut
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
