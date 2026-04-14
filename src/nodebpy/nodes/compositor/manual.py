from typing import Literal

from bpy.types import CompositorNodeFilter

from ...builder import ColorSocket, NodeBuilder, Socket, TreeBuilder
from ...types import InputColor, InputFloat, InputMenu
from ..geometry.manual import _MenuSwitchBase


def tree(
    name: str = "Compositor Nodes",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
    fake_user: bool = False,
) -> TreeBuilder:
    return TreeBuilder.compositor(
        name, collapse=collapse, arrange=arrange, fake_user=fake_user
    )


class MenuSwitch(_MenuSwitchBase):
    """Node builder for the Menu Switch node (Compositor tree)"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    string = _MenuSwitchBase._typed("STRING")
    menu = _MenuSwitchBase._typed("MENU")


class Filter(NodeBuilder):
    """
    Apply common image enhancement filters
    """

    _bl_idname = "CompositorNodeFilter"
    node: CompositorNodeFilter

    def __init__(
        self,
        image: InputColor = None,
        fac: InputFloat = 1.0,
        type: InputMenu
        | Literal[
            "Soften",
            "Box Sharpen",
            "Diamond Sharpen",
            "Laplace",
            "Sobel",
            "Prewitt",
            "Kirsch",
            "Shadow",
        ] = "Soften",
    ):
        super().__init__()
        key_args = {"Image": image, "Fac": fac, "Type": type}

        self._establish_links(**key_args)

    @classmethod
    def soften(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Soften")

    @classmethod
    def box_sharpen(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Box Sharpen")

    @classmethod
    def diamond_sharpen(
        cls, image: InputColor = None, fac: InputFloat = 1.0
    ) -> "Filter":
        return cls(image=image, fac=fac, type="Diamond Sharpen")

    @classmethod
    def laplace(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Laplace")

    @classmethod
    def sobel(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Sobel")

    @classmethod
    def prewitt(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Prewitt")

    @classmethod
    def kirsch(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Kirsch")

    @classmethod
    def shadow(cls, image: InputColor = None, fac: InputFloat = 1.0) -> "Filter":
        return cls(image=image, fac=fac, type="Shadow")

    @property
    def i_image(self) -> Socket:
        """Input socket: Image"""
        return self.inputs.get("Image")

    @property
    def i_fac(self) -> Socket:
        """Input socket: Factor"""
        return self.inputs.get("Fac")

    @property
    def i_type(self) -> Socket:
        """Input socket: Type"""
        return self.inputs.get("Type")

    @property
    def o_image(self) -> ColorSocket:
        """Output socket: Image"""
        return self.outputs.get("Image")
