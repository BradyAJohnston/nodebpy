import bpy

from ..builder import NodeBuilder, SocketLinker
from .types import TYPE_INPUT_COLOR, TYPE_INPUT_VALUE


class RGBCurves(NodeBuilder):
    """Apply color corrections for each color channel"""

    # TODO: add support for custom curves along with FloatCurve

    name = "ShaderNodeRGBCurve"
    node: bpy.types.ShaderNodeRGBCurve

    def __init__(
        self,
        factor: TYPE_INPUT_VALUE = 1.0,
        color: TYPE_INPUT_COLOR = (1.0, 1.0, 1.0, 1.0),
        **kwargs,
    ):
        super().__init__()
        key_args = {"Factor": factor, "Color": color}
        key_args.update(kwargs)

        self._establish_links(**key_args)

    @property
    def i_factor(self) -> SocketLinker:
        """Input socket: Factor"""
        return self._input("Fac")

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")
