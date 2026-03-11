from typing import Literal

import bpy

from ...builder import NodeBuilder, SocketLinker
from ...types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_VALUE,
)


class EnableOutput(NodeBuilder):
    """
    Either pass through the input value or output the fallback value
    """

    _bl_idname = "NodeEnableOutput"
    node: bpy.types.Node

    def __init__(
        self,
        enable: TYPE_INPUT_BOOLEAN = False,
        value: TYPE_INPUT_VALUE = 0.0,
        *,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Enable": enable, "Value": value}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Float'."""
        return cls(data_type="FLOAT", enable=enable)

    @classmethod
    def integer(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Integer'."""
        return cls(data_type="INT", enable=enable)

    @classmethod
    def boolean(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", enable=enable)

    @classmethod
    def vector(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Vector'."""
        return cls(data_type="VECTOR", enable=enable)

    @classmethod
    def color(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Color'."""
        return cls(data_type="RGBA", enable=enable)

    @classmethod
    def string(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'String'."""
        return cls(data_type="STRING", enable=enable)

    @classmethod
    def menu(cls, enable: TYPE_INPUT_BOOLEAN = False) -> "EnableOutput":
        """Create Enable Output with operation 'Menu'."""
        return cls(data_type="MENU", enable=enable)

    @property
    def i_enable(self) -> SocketLinker:
        """Input socket: Enable"""
        return self._input("Enable")

    @property
    def i_value(self) -> SocketLinker:
        """Input socket: Value"""
        return self._input("Value")

    @property
    def o_value(self) -> SocketLinker:
        """Output socket: Value"""
        return self._output("Value")

    @property
    def data_type(
        self,
    ) -> Literal["FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal["FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "STRING", "MENU"],
    ):
        self.node.data_type = value


class GroupInput(NodeBuilder):
    """
    Expose connected data from inside a node group as inputs to its interface
    """

    _bl_idname = "NodeGroupInput"
    node: bpy.types.Node

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)


class GroupOutput(NodeBuilder):
    """
    Output data from inside of a node group
    """

    _bl_idname = "NodeGroupOutput"
    node: bpy.types.Node

    def __init__(self, is_active_output: bool = False):
        super().__init__()
        key_args = {}
        self.is_active_output = is_active_output
        self._establish_links(**key_args)

    @property
    def is_active_output(self) -> bool:
        return self.node.is_active_output

    @is_active_output.setter
    def is_active_output(self, value: bool):
        self.node.is_active_output = value
