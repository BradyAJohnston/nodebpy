from typing import TYPE_CHECKING, Generic, Literal

from bpy.types import CompositorNodeCryptomatteV2, CompositorNodeImage

from ...builder import (
    BooleanSocket,
    ColorSocket,
    FloatSocket,
    IntegerSocket,
    MenuSocket,
    NodeBuilder,
    SocketAccessor,
    StringSocket,
    TreeBuilder,
    VectorSocket,
)
from ...types import (
    Image,
    InputBoolean,
    InputColor,
    InputFloat,
    InputInteger,
    InputMenu,
    InputString,
    InputVector,
)
from ..geometry.manual import _T, Float, Frame, _MenuSwitchBase

__all__ = ["Frame", "MenuSwitch", "tree", "Float"]


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


class MenuSwitch(_MenuSwitchBase[_T], Generic[_T]):
    """Node builder for the Menu Switch node (Compositor tree)"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    string = _MenuSwitchBase._typed("STRING")
    menu = _MenuSwitchBase._typed("MENU")

    if TYPE_CHECKING:

        @classmethod
        def float(
            cls, *args: InputFloat, menu: InputMenu = None, **kwargs: InputFloat
        ) -> "MenuSwitch[FloatSocket]": ...
        @classmethod
        def integer(
            cls, *args: InputInteger, menu: InputMenu = None, **kwargs: InputInteger
        ) -> "MenuSwitch[IntegerSocket]": ...
        @classmethod
        def boolean(
            cls, *args: InputBoolean, menu: InputMenu = None, **kwargs: InputBoolean
        ) -> "MenuSwitch[BooleanSocket]": ...
        @classmethod
        def vector(
            cls, *args: InputVector, menu: InputMenu = None, **kwargs: InputVector
        ) -> "MenuSwitch[VectorSocket]": ...
        @classmethod
        def color(
            cls, *args: InputColor, menu: InputMenu = None, **kwargs: InputColor
        ) -> "MenuSwitch[ColorSocket]": ...
        @classmethod
        def string(
            cls, *args: InputString, menu: InputMenu = None, **kwargs: InputString
        ) -> "MenuSwitch[StringSocket]": ...
        @classmethod
        def menu(
            cls, *args: InputMenu, menu: InputMenu = None, **kwargs: InputMenu
        ) -> "MenuSwitch[MenuSocket]": ...


class Image(NodeBuilder):
    """
    Input image or movie file

    Outputs
    -------
    o.image : ColorSocket
        Image
    o.alpha : FloatSocket
        Alpha
    """

    _bl_idname = "CompositorNodeImage"
    node: CompositorNodeImage

    class _Inputs(SocketAccessor):
        pass

    class _Outputs(SocketAccessor):
        image: ColorSocket
        """Image"""
        alpha: FloatSocket
        """Alpha"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        image: Image | None = None,
        frame_duration: int = 0,
        frame_start: int = 0,
        frame_offset: int = 0,
        use_cyclic: bool = False,
        use_auto_refresh: bool = False,
        layer: str | None = None,
        view: str | None = None,
    ):
        super().__init__()
        key_args = {}
        self.image = image
        self.frame_duration = frame_duration
        self.frame_start = frame_start
        self.frame_offset = frame_offset
        self.use_cyclic = use_cyclic
        self.use_auto_refresh = use_auto_refresh
        if layer:
            self.layer = layer
        if view:
            self.view = view
        self._establish_links(**key_args)

    @property
    def image(self) -> Image | None:
        return self.node.image

    @image.setter
    def image(self, value: Image | None):
        self.node.image = value

    @property
    def frame_duration(self) -> int:
        return self.node.frame_duration

    @frame_duration.setter
    def frame_duration(self, value: int):
        self.node.frame_duration = value

    @property
    def frame_start(self) -> int:
        return self.node.frame_start

    @frame_start.setter
    def frame_start(self, value: int):
        self.node.frame_start = value

    @property
    def frame_offset(self) -> int:
        return self.node.frame_offset

    @frame_offset.setter
    def frame_offset(self, value: int):
        self.node.frame_offset = value

    @property
    def use_cyclic(self) -> bool:
        return self.node.use_cyclic

    @use_cyclic.setter
    def use_cyclic(self, value: bool):
        self.node.use_cyclic = value

    @property
    def use_auto_refresh(self) -> bool:
        return self.node.use_auto_refresh

    @use_auto_refresh.setter
    def use_auto_refresh(self, value: bool):
        self.node.use_auto_refresh = value

    @property
    def layer(self) -> str:
        return self.node.layer

    @layer.setter
    def layer(self, value: str):
        self.node.layer = value

    @property
    def has_layers(self) -> bool:
        return self.node.has_layers

    @property
    def view(self) -> str:
        return self.node.view

    @view.setter
    def view(self, value: str):
        self.node.view = value

    @property
    def has_views(self) -> bool:
        return self.node.has_views


class Cryptomatte(NodeBuilder):
    """
    Generate matte for individual objects and materials using Cryptomatte render passes

    Parameters
    ----------
    image : InputColor
        Image

    Inputs
    ------
    i.image : ColorSocket
        Image

    Outputs
    -------
    o.image : ColorSocket
        Image
    o.matte : FloatSocket
        Matte
    o.pick : ColorSocket
        Pick
    """

    _bl_idname = "CompositorNodeCryptomatteV2"
    node: CompositorNodeCryptomatteV2

    class _Inputs(SocketAccessor):
        image: ColorSocket
        """Image"""

    class _Outputs(SocketAccessor):
        image: ColorSocket
        """Image"""
        matte: FloatSocket
        """Matte"""
        pick: ColorSocket
        """Pick"""

    if TYPE_CHECKING:

        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__(
        self,
        image: InputColor = None,
        *,
        source: Literal["RENDER", "IMAGE"] = "RENDER",
        matte_id: str = "",
        layer_name: str | None = None,
        frame_duration: int = 0,
        frame_start: int = 0,
        frame_offset: int = 0,
        use_cyclic: bool = False,
        use_auto_refresh: bool = False,
        layer: str | None = None,
        view: str | None = None,
    ):
        super().__init__()
        key_args = {"Image": image}
        self.source = source
        self.matte_id = matte_id
        self.frame_duration = frame_duration
        self.frame_start = frame_start
        self.frame_offset = frame_offset
        self.use_cyclic = use_cyclic
        self.use_auto_refresh = use_auto_refresh
        if layer_name is not None:
            self.layer_name = layer_name
        if layer is not None:
            self.layer = layer
        if view is not None:
            self.view = view
        self._establish_links(**key_args)

    @property
    def source(self) -> Literal["RENDER", "IMAGE"]:
        return self.node.source

    @source.setter
    def source(self, value: Literal["RENDER", "IMAGE"]):
        self.node.source = value

    @property
    def matte_id(self) -> str:
        return self.node.matte_id

    @matte_id.setter
    def matte_id(self, value: str):
        self.node.matte_id = value

    @property
    def layer_name(self) -> str:
        return self.node.layer_name

    @layer_name.setter
    def layer_name(self, value: str):
        self.node.layer_name = value

    @property
    def frame_duration(self) -> int:
        return self.node.frame_duration

    @frame_duration.setter
    def frame_duration(self, value: int):
        self.node.frame_duration = value

    @property
    def frame_start(self) -> int:
        return self.node.frame_start

    @frame_start.setter
    def frame_start(self, value: int):
        self.node.frame_start = value

    @property
    def frame_offset(self) -> int:
        return self.node.frame_offset

    @frame_offset.setter
    def frame_offset(self, value: int):
        self.node.frame_offset = value

    @property
    def use_cyclic(self) -> bool:
        return self.node.use_cyclic

    @use_cyclic.setter
    def use_cyclic(self, value: bool):
        self.node.use_cyclic = value

    @property
    def use_auto_refresh(self) -> bool:
        return self.node.use_auto_refresh

    @use_auto_refresh.setter
    def use_auto_refresh(self, value: bool):
        self.node.use_auto_refresh = value

    @property
    def layer(self) -> str:
        return self.node.layer

    @layer.setter
    def layer(self, value: str):
        self.node.layer = value

    @property
    def has_layers(self) -> bool:
        return self.node.has_layers

    @property
    def view(self) -> str:
        return self.node.view

    @view.setter
    def view(self, value: str):
        self.node.view = value

    @property
    def has_views(self) -> bool:
        return self.node.has_views
