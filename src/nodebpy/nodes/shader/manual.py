from typing import Final

from ...builder import (
    ArrangeMethod,
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    ColorSocket,
    FloatSocket,
    IntegerSocket,
    MaterialBuilder,
    MenuSocket,
    ShaderSocket,
    TreeBuilder,
    VectorSocket,
    WorldBuilder,
)
from ...builder.socket import BaseSocket
from ...types import (
    InputBoolean,
    InputBundle,
    InputClosure,
    InputColor,
    InputFloat,
    InputInteger,
    InputMenu,
    InputShader,
    InputVector,
)
from ..geometry import ClosureZone, Frame, RepeatInput, RepeatOutput, RepeatZone
from ..geometry.manual import Float, MenuItems, _MenuSwitchBase

__all__ = [
    "ClosureZone",
    "Float",
    "Frame",
    "MenuSwitch",
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "material",
    "tree",
    "world",
]

tree: Final = TreeBuilder.shader


def material(
    name: str = "New Material",
    *,
    collapse: bool = False,
    arrange: ArrangeMethod = "sugiyama",
    fake_user: bool = False,
    clear: bool = False,
) -> MaterialBuilder:
    return MaterialBuilder(
        name, collapse=collapse, arrange=arrange, fake_user=fake_user, clear=clear
    )


def world(
    name: str = "World",
    *,
    collapse: bool = False,
    arrange: ArrangeMethod = "sugiyama",
    fake_user: bool = False,
    clear: bool = False,
    scene: bool = False,
) -> WorldBuilder:
    """Build a world's node tree; ``scene=True`` makes it the active scene's world.

    ``with s.world("Studio", clear=True, scene=True):`` then add a Background
    linked into a World Output, as in a material.
    """
    return WorldBuilder(
        name,
        collapse=collapse,
        arrange=arrange,
        fake_user=fake_user,
        clear=clear,
        scene=scene,
    )


class MenuSwitch[T: BaseSocket](_MenuSwitchBase[T]):
    """Node builder for the Menu Switch node (Shader tree)"""

    @classmethod
    def float(
        cls, menu: InputMenu = None, items: MenuItems[InputFloat] | None = None
    ) -> "MenuSwitch[FloatSocket]":
        return MenuSwitch(menu, items, data_type="FLOAT")

    @classmethod
    def integer(
        cls, menu: InputMenu = None, items: MenuItems[InputInteger] | None = None
    ) -> "MenuSwitch[IntegerSocket]":
        return MenuSwitch(menu, items, data_type="INT")

    @classmethod
    def boolean(
        cls, menu: InputMenu = None, items: MenuItems[InputBoolean] | None = None
    ) -> "MenuSwitch[BooleanSocket]":
        return MenuSwitch(menu, items, data_type="BOOLEAN")

    @classmethod
    def vector(
        cls, menu: InputMenu = None, items: MenuItems[InputVector] | None = None
    ) -> "MenuSwitch[VectorSocket]":
        return MenuSwitch(menu, items, data_type="VECTOR")

    @classmethod
    def color(
        cls, menu: InputMenu = None, items: MenuItems[InputColor] | None = None
    ) -> "MenuSwitch[ColorSocket]":
        return MenuSwitch(menu, items, data_type="RGBA")

    @classmethod
    def menu(
        cls, menu: InputMenu = None, items: MenuItems[InputMenu] | None = None
    ) -> "MenuSwitch[MenuSocket]":
        return MenuSwitch(menu, items, data_type="MENU")

    @classmethod
    def closure(
        cls, menu: InputMenu = None, items: MenuItems[InputClosure] | None = None
    ) -> "MenuSwitch[ClosureSocket]":
        return MenuSwitch(menu, items, data_type="CLOSURE")

    @classmethod
    def bundle(
        cls, menu: InputMenu = None, items: MenuItems[InputBundle] | None = None
    ) -> "MenuSwitch[BundleSocket]":
        return MenuSwitch(menu, items, data_type="BUNDLE")

    @classmethod
    def shader(
        cls, menu: InputMenu = None, items: MenuItems[InputShader] | None = None
    ) -> "MenuSwitch[ShaderSocket]":
        return MenuSwitch(menu, items, data_type="SHADER")
