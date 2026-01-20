from nodebpy.builder import NodeBuilder


import bpy


class Group(NodeBuilder):
    """Group node"""

    name = "GeometryNodeGroup"
    node: bpy.types.GeometryNodeGroup

    def __init__(self, node_tree: str | None = None, **kwargs):
        super().__init__()
        key_args = kwargs
        if node_tree:
            tree = bpy.data.node_groups[node_tree]
            assert isinstance(tree, bpy.types.GeometryNodeTree)
            self.node.node_tree = tree
            self._establish_links(**key_args)
