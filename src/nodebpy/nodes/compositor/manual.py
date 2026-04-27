from typing import TYPE_CHECKING, Literal

from bpy.types import CompositorNodeImage

from ...builder import (
    ColorSocket,
    FloatSocket,
    NodeBuilder,
    SocketAccessor,
    TreeBuilder,
)
from ..geometry.manual import Float, Frame, _MenuSwitchBase

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


class MenuSwitch(_MenuSwitchBase):
    """Node builder for the Menu Switch node (Compositor tree)"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    string = _MenuSwitchBase._typed("STRING")
    menu = _MenuSwitchBase._typed("MENU")


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
