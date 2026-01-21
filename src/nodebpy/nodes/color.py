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


class Gamma(NodeBuilder):
    """Apply a gamma correction"""

    name = "ShaderNodeGamma"
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

    name = "ShaderNodeRGBCurve"
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
