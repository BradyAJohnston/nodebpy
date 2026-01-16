"""
Some of the nodes need to be manually specified because they are a bit tricky to generate automatically.
"""

from __future__ import annotations

from typing import Iterable, Literal

import bpy

from ..builder import (
    NodeBuilder,
    SocketLinker,
    source_socket,
)
from . import types
from .types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_INT,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
    _AttributeDomains,
    _MixColorBlendTypes,
)


_AttributeDataTypes = Literal[
    "FLOAT", "INT", "BOOLEAN", "VECTOR", "RGBA", "ROTATION", "MATRIX"
]


class CaptureAttribute(NodeBuilder):
    """Store the result of a field on a geometry and output the data as a node socket. Allows remembering or interpolating data as the geometry changes, such as positions before deformation"""

    name = "GeometryNodeCaptureAttribute"
    node: bpy.types.GeometryNodeCaptureAttribute

    def __init__(
        self,
        geometry: LINKABLE = None,
        domain: _AttributeDomains = "POINT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Geometry": geometry}
        key_args.update(kwargs)
        self.domain = domain
        self._establish_links(**key_args)

    def capture(
        self,
        value: LINKABLE,
        name: str | None = None,
        data_type: _AttributeDataTypes | None = None,
    ):
        """Capture the value to store in the attribute"""
        source = source_socket(value)
        if name is None:
            name = source.name
        if data_type is None:
            data_type = source.type  # type: ignore

        item = self._add_item(name, data_type)  # type: ignore
        self._establish_links(**{item.name: value})
        return SocketLinker(self.node.outputs[item.name])

    def _add_item(
        self, name: str, data_type: _AttributeDataTypes = "FLOAT"
    ) -> bpy.types.NodeGeometryCaptureAttributeItem:
        """Add a new output socket to capture additional attributes"""
        return self._items.new(data_type, name)

    @property
    def _items(self) -> bpy.types.NodeGeometryCaptureAttributeItems:
        return self.node.capture_items

    @property
    def i_geometry(self) -> SocketLinker:
        """Input socket: Geometry"""
        return self._input("Geometry")

    @property
    def o_geometry(self) -> SocketLinker:
        """Output socket: Geometry"""
        return self._output("Geometry")

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
