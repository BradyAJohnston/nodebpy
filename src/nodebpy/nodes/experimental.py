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


class GetListItem(NodeBuilder):
    """Retrieve a value from a list"""

    name = "GeometryNodeListGetItem"
    node: bpy.types.GeometryNodeListGetItem

    def __init__(
        self,
        list: TYPE_INPUT_VALUE = 0.0,
        index: TYPE_INPUT_INT = 0,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"List": list, "Index": index}
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
        "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ],
    ):
        self.node.data_type = value


class List(NodeBuilder):
    """Create a list of values"""

    name = "GeometryNodeList"
    node: bpy.types.GeometryNodeList

    def __init__(
        self,
        count: TYPE_INPUT_INT = 1,
        value: TYPE_INPUT_VALUE = 0.0,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Count": count, "Value": value}
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
        "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
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
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"List": list}
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
        "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
    ]:
        return self.node.data_type

    @data_type.setter
    def data_type(
        self,
        value: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ],
    ):
        self.node.data_type = value
