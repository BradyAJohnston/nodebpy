from typing import Literal

from bpy.types import ShaderNodeAttribute

from ...builder import (
    ColorSocket,
    FloatSocket,
    MaterialBuilder,
    NodeBuilder,
    TreeBuilder,
    VectorSocket,
)
from ..geometry import RepeatInput, RepeatOutput, RepeatZone
from ..geometry.manual import _MenuSwitchBase

__all__ = [
    "MenuSwitch",
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "Attribute",
    "tree",
    "material",
]


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
    name: str = "New Material",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
    fake_user: bool = False,
) -> MaterialBuilder:
    return MaterialBuilder(
        name, collapse=collapse, arrange=arrange, fake_user=fake_user
    )


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


class Attribute(NodeBuilder):
    """
    Retrieve attributes attached to objects or geometry
    """

    _bl_idname = "ShaderNodeAttribute"
    node: ShaderNodeAttribute

    def __init__(
        self,
        attribute_type: Literal[
            "GEOMETRY", "OBJECT", "INSTANCER", "VIEW_LAYER"
        ] = "GEOMETRY",
        attribute_name: str = "",
    ):
        super().__init__()
        key_args = {}
        self.attribute_type = attribute_type
        self.attribute_name = attribute_name
        self._establish_links(**key_args)

    @classmethod
    def geometry(cls, attribute_name: str = "") -> "Attribute":
        """Create Attribute with operation 'Geometry'."""
        return cls(attribute_type="GEOMETRY", attribute_name=attribute_name)

    @classmethod
    def object(cls, attribute_name: str = "") -> "Attribute":
        """Create Attribute with operation 'Object'."""
        return cls(attribute_type="OBJECT", attribute_name=attribute_name)

    @classmethod
    def instancer(cls, attribute_name: str = "") -> "Attribute":
        """Create Attribute with operation 'Instancer'."""
        return cls(attribute_type="INSTANCER", attribute_name=attribute_name)

    @classmethod
    def view_layer(cls, attribute_name: str = "") -> "Attribute":
        """Create Attribute with operation 'View Layer'."""
        return cls(attribute_type="VIEW_LAYER", attribute_name=attribute_name)

    @property
    def o_color(self) -> ColorSocket:
        """Output socket: Color"""
        return self.outputs._get("Color")

    @property
    def o_vector(self) -> VectorSocket:
        """Output socket: Vector"""
        return self.outputs._get("Vector")

    @property
    def o_fac(self) -> FloatSocket:
        """Output socket: Factor"""
        return self.outputs._get("Fac")

    @property
    def o_alpha(self) -> FloatSocket:
        """Output socket: Alpha"""
        return self.outputs._get("Alpha")

    @property
    def attribute_type(
        self,
    ) -> Literal["GEOMETRY", "OBJECT", "INSTANCER", "VIEW_LAYER"]:
        return self.node.attribute_type

    @attribute_type.setter
    def attribute_type(
        self, value: Literal["GEOMETRY", "OBJECT", "INSTANCER", "VIEW_LAYER"]
    ):
        self.node.attribute_type = value

    @property
    def attribute_name(self) -> str:
        return self.node.attribute_name

    @attribute_name.setter
    def attribute_name(self, value: str):
        self.node.attribute_name = value
