import bpy

from ...builder import (
    NodeBuilder,
    SocketLinker,
)
from ...types import (
    SOCKET_TYPES,
    TYPE_INPUT_ALL,
    TYPE_INPUT_MENU,
    _is_default_value,
)

__all__ = [
    "MenuSwitch",
]


def _typed_menu_switch(data_type: SOCKET_TYPES):
    @classmethod
    def method(
        cls,
        *args: TYPE_INPUT_ALL,
        menu: TYPE_INPUT_MENU = None,
        **kwargs: TYPE_INPUT_ALL,
    ) -> "MenuSwitch":
        """Create an MenuSwitch node with a pre-set data_type"""
        return cls(*args, menu=menu, data_type=data_type, **kwargs)

    return method


class MenuSwitch(NodeBuilder):
    """Node builder for the Menu Switch node"""

    _bl_idname = "GeometryNodeMenuSwitch"
    node: bpy.types.GeometryNodeMenuSwitch

    float = _typed_menu_switch("FLOAT")
    integer = _typed_menu_switch("INT")
    boolean = _typed_menu_switch("BOOLEAN")
    vector = _typed_menu_switch("VECTOR")
    color = _typed_menu_switch("RGBA")
    string = _typed_menu_switch("STRING")
    menu = _typed_menu_switch("MENU")

    def __init__(
        self,
        *args: TYPE_INPUT_ALL,
        menu: TYPE_INPUT_MENU = None,
        data_type: SOCKET_TYPES = "FLOAT",
        **kwargs: TYPE_INPUT_ALL,
    ):
        super().__init__()
        self.data_type = data_type
        self.node.enum_items.clear()
        key_args = {"Menu": menu}
        self._link_args(*args, **kwargs)
        self._establish_links(**key_args)

    def _link_args(self, *args: TYPE_INPUT_ALL, **kwargs: TYPE_INPUT_ALL):
        for arg in args:
            if _is_default_value(arg):
                socket = self._create_socket(f"Item_{len(self.node.enum_items)}")
                socket.default_value = arg
            else:
                source = self._source_socket(arg)
                self.tree.link(source, self.node.inputs["__extend__"])

        for key, value in kwargs.items():
            if _is_default_value(value):
                socket = self._create_socket(key)
                socket.default_value = value
            else:
                source = self._source_socket(value)  # type: ignore
                self._link(source, self.node.inputs["__extend__"])
                self.node.enum_items[-1].name = key

    def _create_socket(self, name: str) -> bpy.types.NodeSocket:
        item = self.node.enum_items.new(name)
        return self.node.inputs[item.name]

    @property
    def inputs(self) -> dict[str, SocketLinker]:
        """Input sockets"""
        return {
            item.name: SocketLinker(self.node.inputs[item.name])
            for item in self.node.enum_items
        }

    @property
    def outputs(self) -> dict[str, SocketLinker]:
        """Input sockets"""
        return {
            item.name: SocketLinker(self.node.outputs[item.name])
            for item in self.node.enum_items
        }

    @property
    def i_menu(self) -> SocketLinker:
        """Input socket: Menu"""
        return self._input("Menu")

    @property
    def o_output(self) -> SocketLinker:
        """Output socket: Output"""
        return self._output("Output")

    @property
    def data_type(self) -> SOCKET_TYPES:
        """Input socket: Data Type"""
        return self.node.data_type  # type: ignore

    @data_type.setter
    def data_type(self, value: SOCKET_TYPES):
        """Input socket: Data Type"""
        self.node.data_type = value
