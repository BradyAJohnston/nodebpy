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


class Frame(NodeBuilder):
    """Collect related nodes together in a common area. Useful for organization when the re-usability of a node group is not required"""

    name = "NodeFrame"
    node: bpy.types.Node

    def __init__(
        self,
        shrink: bool = False,
        label_size: int = 0,
    ):
        super().__init__()
        key_args = kwargs
        self.shrink = shrink
        self.label_size = label_size
        self._establish_links(**key_args)

    @property
    def shrink(self) -> bool:
        return self.node.shrink

    @shrink.setter
    def shrink(self, value: bool):
        self.node.shrink = value

    @property
    def label_size(self) -> int:
        return self.node.label_size

    @label_size.setter
    def label_size(self, value: int):
        self.node.label_size = value


class Reroute(NodeBuilder):
    """A single-socket organization tool that supports one input and multiple outputs"""

    name = "NodeReroute"
    node: bpy.types.Node

    def __init__(
        self,
        input: TYPE_INPUT_COLOR = None,
        socket_idname: str = "",
    ):
        super().__init__()
        key_args = {"Input": input}
        self.socket_idname = socket_idname
        self._establish_links(**key_args)

    @property
    def i_input(self) -> SocketLinker:
        """Input socket: Input"""
        return self._input("Input")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def socket_idname(self) -> str:
        return self.node.socket_idname

    @socket_idname.setter
    def socket_idname(self, value: str):
        self.node.socket_idname = value
