import bpy

from ..builder import NodeBuilder, SocketLinker
from ..types import (
    TYPE_INPUT_COLOR,
    TYPE_INPUT_VALUE,
)


class Gamma(NodeBuilder):
    """Apply a gamma correction"""

    _bl_idname = "ShaderNodeGamma"
    node: bpy.types.ShaderNodeGamma

    def __init__(
        self,
        color: TYPE_INPUT_COLOR = None,
        gamma: TYPE_INPUT_VALUE = 1.0,
    ):
        super().__init__()
        key_args = {"Color": color, "Gamma": gamma}

        self._establish_links(**key_args)

    @property
    def i_color(self) -> SocketLinker:
        """Input socket: Color"""
        return self._input("Color")

    @property
    def i_gamma(self) -> SocketLinker:
        """Input socket: Gamma"""
        return self._input("Gamma")

    @property
    def o_color(self) -> SocketLinker:
        """Output socket: Color"""
        return self._output("Color")


class RgbCurves(NodeBuilder):
    """Apply color corrections for each color channel"""

    _bl_idname = "ShaderNodeRGBCurve"
    node: bpy.types.ShaderNodeRGBCurve

    def __init__(
        self,
        fac: TYPE_INPUT_VALUE = 1.0,
        color: TYPE_INPUT_COLOR = None,
    ):
        super().__init__()
        key_args = {"Fac": fac, "Color": color}

        self._establish_links(**key_args)

    @property
    def i_fac(self) -> SocketLinker:
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
