from typing import TYPE_CHECKING, Literal

from bpy.types import ShaderNodeAttribute, ShaderNodeTree

from ...builder import (
    BaseNode,
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
)
from ...builder.accessor import SocketAccessor
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
from ..geometry import Frame, RepeatInput, RepeatOutput, RepeatZone
from ..geometry.manual import Float, MenuItems, _MenuSwitchBase

__all__ = [
    "Attribute",
    "Float",
    "Frame",
    "MenuSwitch",
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "material",
    "tree",
]


def tree(
    name: str = "Shader Nodes",
    *,
    collapse: bool = False,
    arrange: Literal["sugiyama", "simple"] | None = "sugiyama",
    fake_user: bool = False,
) -> TreeBuilder[ShaderNodeTree]:
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


class Attribute(BaseNode):
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

    class _Outputs(SocketAccessor):
        color: ColorSocket
        """The attribute value as a color."""
        vector: VectorSocket
        """The attribute value as a vector."""
        fac: FloatSocket
        """The attribute value as a scalar factor."""
        alpha: FloatSocket
        """The attribute value as an alpha (scalar)."""

    if TYPE_CHECKING:

        @property
        def o(self) -> _Outputs: ...

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
