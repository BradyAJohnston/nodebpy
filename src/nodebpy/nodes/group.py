from typing import Literal

import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    LINKABLE,
    TYPE_INPUT_BOOLEAN,
    TYPE_INPUT_GEOMETRY,
    TYPE_INPUT_INT,
    TYPE_INPUT_MENU,
    TYPE_INPUT_STRING,
    TYPE_INPUT_ROTATION,
    TYPE_INPUT_COLOR,
    TYPE_INPUT_MATRIX,
    TYPE_INPUT_BUNDLE,
    TYPE_INPUT_CLOSURE,
    TYPE_INPUT_OBJECT,
    TYPE_INPUT_COLLECTION,
    TYPE_INPUT_IMAGE,
    TYPE_INPUT_MATERIAL,
    TYPE_INPUT_VALUE,
    TYPE_INPUT_VECTOR,
)


class Group(NodeBuilder):
    """Group node"""

    name = "GeometryNodeGroup"
    node: bpy.types.GeometryNodeGroup

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)
