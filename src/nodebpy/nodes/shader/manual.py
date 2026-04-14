from typing import Literal

import bpy

from ...builder import TreeBuilder
from ..geometry import RepeatInput, RepeatOutput, RepeatZone
from ..geometry.manual import _MenuSwitchBase

__all__ = ["MenuSwitch", "RepeatInput", "RepeatOutput", "RepeatZone", "tree"]


def tree(
    name: str = "Shader Nodes",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
    fake_user: bool = False,
) -> TreeBuilder:
    return TreeBuilder.shader(
        name, collapse=collapse, arrange=arrange, fake_user=fake_user
    )


def material(
    name: str = "Material Nodes",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
    fake_user: bool = False,
) -> TreeBuilder:
    material = bpy.data.materials.new(name)
    tree = material.node_tree
    assert tree
    return TreeBuilder(tree, collapse=collapse, arrange=arrange, fake_user=fake_user)


class MenuSwitch(_MenuSwitchBase):
    """Node builder for the Menu Switch node (Shader tree)"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    menu = _MenuSwitchBase._typed("MENU")
    closure = _MenuSwitchBase._typed("CLOSURE")
    bundle = _MenuSwitchBase._typed("BUNDLE")
    shader = _MenuSwitchBase._typed("SHADER")
