from typing import Literal

import bpy

from ...builder import NodeBuilder


class Script(NodeBuilder):
    """
    Generate an OSL shader from a file or text data-block.
    Note: OSL shaders are not supported on all GPU backends
    """

    _bl_idname = "ShaderNodeScript"
    node: bpy.types.ShaderNodeScript

    def __init__(
        self,
        filepath: str = "",
        mode: Literal["INTERNAL", "EXTERNAL"] = "INTERNAL",
        use_auto_update: bool = False,
        bytecode: str = "",
        bytecode_hash: str = "",
    ):
        super().__init__()
        key_args = {}
        self.filepath = filepath
        self.mode = mode
        self.use_auto_update = use_auto_update
        self.bytecode = bytecode
        self.bytecode_hash = bytecode_hash
        self._establish_links(**key_args)

    @property
    def filepath(self) -> str:
        return self.node.filepath

    @filepath.setter
    def filepath(self, value: str):
        self.node.filepath = value

    @property
    def mode(self) -> Literal["INTERNAL", "EXTERNAL"]:
        return self.node.mode

    @mode.setter
    def mode(self, value: Literal["INTERNAL", "EXTERNAL"]):
        self.node.mode = value

    @property
    def use_auto_update(self) -> bool:
        return self.node.use_auto_update

    @use_auto_update.setter
    def use_auto_update(self, value: bool):
        self.node.use_auto_update = value

    @property
    def bytecode(self) -> str:
        return self.node.bytecode

    @bytecode.setter
    def bytecode(self, value: str):
        self.node.bytecode = value

    @property
    def bytecode_hash(self) -> str:
        return self.node.bytecode_hash

    @bytecode_hash.setter
    def bytecode_hash(self, value: str):
        self.node.bytecode_hash = value
