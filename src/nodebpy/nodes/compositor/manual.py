from typing import Literal

from ...builder import TreeBuilder
from ..geometry.manual import Frame, _MenuSwitchBase

__all__ = ["Frame", "MenuSwitch", "tree"]


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
