from typing import Literal
import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import TYPE_INPUT_GEOMETRY, TYPE_INPUT_BOOLEAN


class SetHandleType(NodeBuilder):
    """Set the handle type for the control points of a Bézier curve"""

    name = "GeometryNodeCurveSetHandles"
    node: bpy.types.GeometryNodeCurveSetHandles

    def __init__(
        self,
        curve: TYPE_INPUT_GEOMETRY = None,
        selection: TYPE_INPUT_BOOLEAN = True,
        *,
        left: bool = False,
        right: bool = False,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
    ):
        super().__init__()
        key_args = {"Curve": curve, "Selection": selection}
        self.handle_type = handle_type
        self.left = left
        self.right = right
        self._establish_links(**key_args)

    @property
    def i_curve(self) -> SocketLinker:
        """Input socket: Curve"""
        return self._input("Curve")

    @property
    def i_selection(self) -> SocketLinker:
        """Input socket: Selection"""
        return self._input("Selection")

    @property
    def o_curve(self) -> SocketLinker:
        """Output socket: Curve"""
        return self._output("Curve")

    @property
    def handle_type(self) -> Literal["FREE", "AUTO", "VECTOR", "ALIGN"]:
        return self.node.handle_type

    @handle_type.setter
    def handle_type(self, value: Literal["FREE", "AUTO", "VECTOR", "ALIGN"]):
        self.node.handle_type = value

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        match value, self.right:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        match self.left, value:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()


class HandleTypeSelection(NodeBuilder):
    """Provide a selection based on the handle types of Bézier control points"""

    name = "GeometryNodeCurveHandleTypeSelection"
    node: bpy.types.GeometryNodeCurveHandleTypeSelection

    def __init__(
        self,
        handle_type: Literal["FREE", "AUTO", "VECTOR", "ALIGN"] = "AUTO",
        left: bool = True,
        right: bool = True,
    ):
        super().__init__()
        self.handle_type = handle_type
        self.left = left
        self.right = right

    @property
    def o_selection(self) -> SocketLinker:
        """Output socket: Selection"""
        return self._output("Selection")

    @property
    def handle_type(self) -> Literal["FREE", "AUTO", "VECTOR", "ALIGN"]:
        return self.node.handle_type

    @handle_type.setter
    def handle_type(self, value: Literal["FREE", "AUTO", "VECTOR", "ALIGN"]):
        self.node.handle_type = value

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        match value, self.right:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        match self.left, value:
            case True, True:
                self.node.mode = {"LEFT", "RIGHT"}
            case True, False:
                self.node.mode = {"LEFT"}
            case False, True:
                self.node.mode = {"RIGHT"}
            case False, False:
                self.node.mode = set()

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]):
        self.node.mode = value
