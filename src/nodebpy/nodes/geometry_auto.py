from __future__ import annotations

from typing import Any

import bpy

from ..builder import NodeBuilder, SocketLinker


class Bake(NodeBuilder):
    """Cache the incoming data so that it can be used without recomputation"""

    name = "GeometryNodeBake"
    node: bpy.types.GeometryNodeBake
    _socket_data_types = (
        "FLOAT",
        "INT",
        "BOOLEAN",
        "VECTOR",
        "RGHA",
        "ROTATION",
        "MATRIX",
        "STRING",
        "GEOMETRY",
        "BUNDLE",
    )

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._establish_links(**self._add_inputs(*args, **kwargs))

    def _add_socket(self, name: str, type: str, default_value: Any | None = None):
        self.node.bake_items.new()

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
