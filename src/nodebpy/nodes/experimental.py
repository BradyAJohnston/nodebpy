from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_MATRIX,
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
        *,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"List": list, "Index": index}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(
        cls, list: TYPE_INPUT_VALUE = 0.0, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Float'."""
        return cls(data_type="FLOAT", list=list, index=index)

    @classmethod
    def integer(
        cls, list: TYPE_INPUT_INT = 0, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Integer'."""
        return cls(data_type="INT", list=list, index=index)

    @classmethod
    def boolean(
        cls, list: TYPE_INPUT_BOOLEAN = False, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", list=list, index=index)

    @classmethod
    def vector(
        cls, list: TYPE_INPUT_VECTOR = None, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Vector'."""
        return cls(data_type="VECTOR", list=list, index=index)

    @classmethod
    def color(
        cls, list: TYPE_INPUT_COLOR = None, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Color'."""
        return cls(data_type="RGBA", list=list, index=index)

    @classmethod
    def rotation(
        cls, list: TYPE_INPUT_ROTATION = None, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Rotation'."""
        return cls(data_type="ROTATION", list=list, index=index)

    @classmethod
    def matrix(
        cls, list: TYPE_INPUT_MATRIX = None, index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Matrix'."""
        return cls(data_type="MATRIX", list=list, index=index)

    @classmethod
    def menu(
        cls, list: TYPE_INPUT_MENU = "", index: TYPE_INPUT_INT = 0
    ) -> "GetListItem":
        """Create Get List Item with operation 'Menu'."""
        return cls(data_type="MENU", list=list, index=index)

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
        *,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"Count": count, "Value": value}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_VALUE = 0.0) -> "List":
        """Create List with operation 'Float'."""
        return cls(data_type="FLOAT", count=count, value=value)

    @classmethod
    def integer(cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_INT = 0) -> "List":
        """Create List with operation 'Integer'."""
        return cls(data_type="INT", count=count, value=value)

    @classmethod
    def boolean(
        cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_BOOLEAN = False
    ) -> "List":
        """Create List with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", count=count, value=value)

    @classmethod
    def vector(
        cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_VECTOR = None
    ) -> "List":
        """Create List with operation 'Vector'."""
        return cls(data_type="VECTOR", count=count, value=value)

    @classmethod
    def color(cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_COLOR = None) -> "List":
        """Create List with operation 'Color'."""
        return cls(data_type="RGBA", count=count, value=value)

    @classmethod
    def rotation(
        cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_ROTATION = None
    ) -> "List":
        """Create List with operation 'Rotation'."""
        return cls(data_type="ROTATION", count=count, value=value)

    @classmethod
    def matrix(
        cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_MATRIX = None
    ) -> "List":
        """Create List with operation 'Matrix'."""
        return cls(data_type="MATRIX", count=count, value=value)

    @classmethod
    def menu(cls, count: TYPE_INPUT_INT = 1, value: TYPE_INPUT_MENU = "") -> "List":
        """Create List with operation 'Menu'."""
        return cls(data_type="MENU", count=count, value=value)

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
        *,
        data_type: Literal[
            "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX", "MENU"
        ] = "FLOAT",
    ):
        super().__init__()
        key_args = {"List": list}
        self.data_type = data_type
        self._establish_links(**key_args)

    @classmethod
    def float(cls, list: TYPE_INPUT_VALUE = 0.0) -> "ListLength":
        """Create List Length with operation 'Float'."""
        return cls(data_type="FLOAT", list=list)

    @classmethod
    def integer(cls, list: TYPE_INPUT_INT = 0) -> "ListLength":
        """Create List Length with operation 'Integer'."""
        return cls(data_type="INT", list=list)

    @classmethod
    def boolean(cls, list: TYPE_INPUT_BOOLEAN = False) -> "ListLength":
        """Create List Length with operation 'Boolean'."""
        return cls(data_type="BOOLEAN", list=list)

    @classmethod
    def vector(cls, list: TYPE_INPUT_VECTOR = None) -> "ListLength":
        """Create List Length with operation 'Vector'."""
        return cls(data_type="VECTOR", list=list)

    @classmethod
    def color(cls, list: TYPE_INPUT_COLOR = None) -> "ListLength":
        """Create List Length with operation 'Color'."""
        return cls(data_type="RGBA", list=list)

    @classmethod
    def rotation(cls, list: TYPE_INPUT_ROTATION = None) -> "ListLength":
        """Create List Length with operation 'Rotation'."""
        return cls(data_type="ROTATION", list=list)

    @classmethod
    def matrix(cls, list: TYPE_INPUT_MATRIX = None) -> "ListLength":
        """Create List Length with operation 'Matrix'."""
        return cls(data_type="MATRIX", list=list)

    @classmethod
    def menu(cls, list: TYPE_INPUT_MENU = "") -> "ListLength":
        """Create List Length with operation 'Menu'."""
        return cls(data_type="MENU", list=list)

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
