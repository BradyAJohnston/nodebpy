from ..geometry import RepeatInput, RepeatOutput, RepeatZone
from ..geometry.manual import _MenuSwitchBase

__all__ = ["MenuSwitch", "RepeatInput", "RepeatOutput", "RepeatZone"]


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
