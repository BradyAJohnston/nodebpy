from typing import TYPE_CHECKING, Generic, Literal

from bpy.types import ShaderNodeAttribute

from ...builder import (
    BooleanSocket,
    BundleSocket,
    ClosureSocket,
    ColorSocket,
    FloatSocket,
    IntegerSocket,
    MaterialBuilder,
    MenuSocket,
    NodeBuilder,
    ShaderSocket,
    TreeBuilder,
    VectorSocket,
)
from ...builder.accessor import SocketAccessor
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
from ..geometry.manual import _T, Float, _MenuSwitchBase

__all__ = [
    "MenuSwitch",
    "RepeatInput",
    "RepeatOutput",
    "RepeatZone",
    "Attribute",
    "Frame",
    "Float",
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


class MenuSwitch(_MenuSwitchBase[_T], Generic[_T]):
    """Node builder for the Menu Switch node (Shader tree)"""

    @classmethod
    def float(
        cls, *args: InputFloat, menu: InputMenu = None, **kwargs: InputFloat
    ) -> "MenuSwitch[FloatSocket]":
        return MenuSwitch(*args, menu=menu, data_type="FLOAT", **kwargs)

    @classmethod
    def integer(
        cls, *args: InputInteger, menu: InputMenu = None, **kwargs: InputInteger
    ) -> "MenuSwitch[IntegerSocket]":
        return MenuSwitch(*args, menu=menu, data_type="INT", **kwargs)

    @classmethod
    def boolean(
        cls, *args: InputBoolean, menu: InputMenu = None, **kwargs: InputBoolean
    ) -> "MenuSwitch[BooleanSocket]":
        return MenuSwitch(*args, menu=menu, data_type="BOOLEAN", **kwargs)

    @classmethod
    def vector(
        cls, *args: InputVector, menu: InputMenu = None, **kwargs: InputVector
    ) -> "MenuSwitch[VectorSocket]":
        return MenuSwitch(*args, menu=menu, data_type="VECTOR", **kwargs)

    @classmethod
    def color(
        cls, *args: InputColor, menu: InputMenu = None, **kwargs: InputColor
    ) -> "MenuSwitch[ColorSocket]":
        return MenuSwitch(*args, menu=menu, data_type="RGBA", **kwargs)

    @classmethod
    def menu(
        cls, *args: InputMenu, menu: InputMenu = None, **kwargs: InputMenu
    ) -> "MenuSwitch[MenuSocket]":
        return MenuSwitch(*args, menu=menu, data_type="MENU", **kwargs)

    @classmethod
    def closure(
        cls, *args: InputClosure, menu: InputMenu = None, **kwargs: InputClosure
    ) -> "MenuSwitch[ClosureSocket]":
        return MenuSwitch(*args, menu=menu, data_type="CLOSURE", **kwargs)

    @classmethod
    def bundle(
        cls, *args: InputBundle, menu: InputMenu = None, **kwargs: InputBundle
    ) -> "MenuSwitch[BundleSocket]":
        return MenuSwitch(*args, menu=menu, data_type="BUNDLE", **kwargs)

    @classmethod
    def shader(
        cls, *args: InputShader, menu: InputMenu = None, **kwargs: InputShader
    ) -> "MenuSwitch[ShaderSocket]":
        return MenuSwitch(*args, menu=menu, data_type="SHADER", **kwargs)


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
