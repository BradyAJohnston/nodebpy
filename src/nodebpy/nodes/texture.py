from nodebpy.builder import NodeBuilder, SocketLinker


import bpy
from typing import Literal
from .types import TYPE_INPUT_IMAGE, TYPE_INPUT_VECTOR, TYPE_INPUT_INT


class ImageTexture(NodeBuilder):
    """Sample values from an image texture"""

    name = "GeometryNodeImageTexture"
    node: bpy.types.GeometryNodeImageTexture

    def __init__(
        self,
        image: TYPE_INPUT_IMAGE = None,
        vector: TYPE_INPUT_VECTOR = None,
        frame: TYPE_INPUT_INT = 0,
        interpolation: Literal["Linear", "Closest", "Cubic"] = "Linear",
        extension: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"] = "REPEAT",
        **kwargs,
    ):
        super().__init__()
        key_args = {"Image": image, "Vector": vector, "Frame": frame}
        key_args.update(kwargs)
        self.interpolation = interpolation
        self.extension = extension
        self._establish_links(**key_args)

    @property
    def i_image(self) -> SocketLinker:
        """Input socket: Image"""
        return self._input("Image")

    @property
    def i_vector(self) -> SocketLinker:
        """Input socket: Vector"""
        return self._input("Vector")

    @property
    def i_frame(self) -> SocketLinker:
        """Input socket: Frame"""
        return self._input("Frame")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")

    @property
    def o_alpha(self) -> SocketLinker:
        """Output socket: Alpha"""
        return self._output("Alpha")

    @property
    def interpolation(self) -> Literal["Linear", "Closest", "Cubic"]:
        return self.node.interpolation

    @interpolation.setter
    def interpolation(self, value: Literal["Linear", "Closest", "Cubic"]):
        self.node.interpolation = value

    @property
    def extension(self) -> Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]:
        return self.node.extension

    @extension.setter
    def extension(self, value: Literal["REPEAT", "EXTEND", "CLIP", "MIRROR"]):
        self.node.extension = value
