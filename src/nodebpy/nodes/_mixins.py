"""Hand-written mixins attached to auto-generated node classes.

These hold reusable behaviour that the code generator cannot derive on its own
(ergonomic flag accessors, items helpers, …). ``generate.py`` wires them onto
the generated classes via :class:`~generate.NodeCustomization`, so the bulky
boilerplate (sockets, docstrings, property accessors) stays generated while the
bespoke behaviour lives here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import bpy


class _HandleModeMixin:
    """Shared ``left``/``right``/``mode`` flags for the Bézier handle nodes
    (``SetHandleType`` / ``HandleTypeSelection``), whose ``mode`` is an
    ENUM_FLAG set drawn from ``{"LEFT", "RIGHT"}``. ``left``/``right`` are
    ergonomic per-side toggles; ``mode`` exposes the raw set."""

    if TYPE_CHECKING:
        node: (
            bpy.types.GeometryNodeCurveSetHandles
            | bpy.types.GeometryNodeCurveHandleTypeSelection
        )

    @property
    def left(self) -> bool:
        return "LEFT" in self.node.mode

    @left.setter
    def left(self, value: bool):
        self.node.mode = (
            (self.node.mode | {"LEFT"}) if value else (self.node.mode - {"LEFT"})
        )

    @property
    def right(self) -> bool:
        return "RIGHT" in self.node.mode

    @right.setter
    def right(self, value: bool):
        self.node.mode = (
            (self.node.mode | {"RIGHT"}) if value else (self.node.mode - {"RIGHT"})
        )

    @property
    def mode(self) -> set[Literal["LEFT", "RIGHT"]]:
        return self.node.mode

    @mode.setter
    def mode(self, value: set[Literal["LEFT", "RIGHT"]]):
        self.node.mode = value
