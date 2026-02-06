# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from bpy.types import Node as BlenderNode
from bpy.types import NodeSocket
from mathutils import Vector

if TYPE_CHECKING:
    from .arrange.graph import Socket

selected: list[BlenderNode] = []
linked_sockets: defaultdict[NodeSocket, set[NodeSocket]] = defaultdict(set)
multi_input_sort_ids: defaultdict[Socket, list[tuple[Socket, int]]] = defaultdict(list)


@dataclass
class Settings:
    spacing: float = 30.0
    arrange_mode = "NODES"
    iterations: int = 50
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "LEFT_UP"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "FULL"
    add_reroutes: bool = True
    keep_reroutes_outside_frames: bool = False
    stack_collapsed: bool = True
    recenter_mode = "NODES"
    origin: Literal["CENTER", "ACTIVE_OUTPUT", "ACTIVE_NODE"] = "CENTER"
    stack_margin_y_fac: float = 0.5


SETTINGS = Settings()
MARGIN: Vector = Vector((200, 20.0))


def reset() -> None:
    selected.clear()
    linked_sockets.clear()
    multi_input_sort_ids.clear()
