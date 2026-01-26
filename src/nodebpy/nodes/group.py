
import bpy

from ..builder import NodeBuilder


class Group(NodeBuilder):
    """
    Group node
    """

    _bl_idname = "GeometryNodeGroup"
    node: bpy.types.GeometryNodeGroup

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)
