
import bpy

from ...builder import NodeBuilder


class Group(NodeBuilder):
    """
    Group node
    """

    _bl_idname = "CompositorNodeGroup"
    node: bpy.types.CompositorNodeGroup

    def __init__(self):
        super().__init__()
        key_args = {}

        self._establish_links(**key_args)
