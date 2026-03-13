from ..geometry.manual import _MenuSwitchBase


class MenuSwitch(_MenuSwitchBase):
    """Node builder for the Menu Switch node (Compositor tree)"""

    float = _MenuSwitchBase._typed("FLOAT")
    integer = _MenuSwitchBase._typed("INT")
    boolean = _MenuSwitchBase._typed("BOOLEAN")
    vector = _MenuSwitchBase._typed("VECTOR")
    color = _MenuSwitchBase._typed("RGBA")
    string = _MenuSwitchBase._typed("STRING")
    menu = _MenuSwitchBase._typed("MENU")
