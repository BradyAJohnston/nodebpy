# SPDX-License-Identifier: GPL-2.0-or-later
"""The node tree as the layout sees it.

A plain-data copy of the parts of a Blender node tree the layout reads,
named after the structs they come from (``DNA_node_types.h``,
``BKE_node_runtime.hh``): :class:`bNodeTree`, :class:`bNode`,
:class:`bNodeSocket`, :class:`bNodeLink`. Nothing here needs ``bpy``: the
layout takes a :class:`bNodeTree` and returns edits to make to it, so it can
be driven from Python data in tests, and later reimplemented in C++ reading
the real structs.

All coordinates are in the tree's own space (Blender's unscaled UI units),
x to the right and y up, and absolute: a node's location is not relative to
its frame.
"""

from __future__ import annotations

from dataclasses import dataclass, field

REROUTE_SIZE = 8.0
"""Width and height the layout gives a reroute."""


@dataclass(eq=False, slots=True)
class bNodeSocket:
    """A socket of a node (``bNodeSocket``)."""

    node: bNode
    """The node the socket is on (``owner_node()``)."""
    index: int
    """Position among the node's inputs, or among its outputs (``index()``)."""
    is_output: bool
    is_multi_input: bool = False
    location: tuple[float, float] | None = None
    """Where links attach (``runtime->location``). Only known for sockets
    that have a link."""
    idname: str = ""
    """The socket's type, e.g. ``NodeSocketGeometry``."""


@dataclass(eq=False, slots=True)
class bNode:
    """A node (``bNode``), a frame or a reroute included."""

    name: str = ""
    idname: str = ""
    label: str = ""
    location: tuple[float, float] = (0.0, 0.0)
    """``location``: for most nodes the top-left corner, for a collapsed
    node a point on its left edge, for a reroute its centre."""
    width: float = 0.0
    draw_bounds: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    """The box the node is drawn in, ``(xmin, ymin, xmax, ymax)``
    (``runtime->draw_bounds``). Blender only knows it once a node editor
    has drawn the tree; otherwise it has to be estimated."""
    parent: bNode | None = None
    """The frame the node is in."""
    is_collapsed: bool = False
    """Drawn as a header only (``NODE_COLLAPSED``, Python's ``hide``)."""
    select: bool = True
    """Whether the layout is to arrange the node (``NODE_SELECT``, when an
    operator arranges the selection). Nodes that are not selected stay
    where they are and links to them are left out of account."""
    inputs: list[bNodeSocket] = field(default_factory=list)
    outputs: list[bNodeSocket] = field(default_factory=list)

    # Frames only (``NodeFrame``).
    label_size: int = 20
    shrink: bool = True
    """The frame fits itself around its members (``NODE_FRAME_SHRINK``)."""

    def is_frame(self) -> bool:
        return self.idname == "NodeFrame"

    def is_reroute(self) -> bool:
        return self.idname == "NodeReroute"

    def is_group_input(self) -> bool:
        return self.idname == "NodeGroupInput"

    def is_group_output(self) -> bool:
        return self.idname == "NodeGroupOutput"

    @property
    def top(self) -> float:
        return self.draw_bounds[3]

    @property
    def bottom(self) -> float:
        return self.draw_bounds[1]

    def add_socket(
        self,
        is_output: bool,
        *,
        is_multi_input: bool = False,
        location: tuple[float, float] | None = None,
        idname: str = "",
    ) -> bNodeSocket:
        sockets = self.outputs if is_output else self.inputs
        socket = bNodeSocket(
            self, len(sockets), is_output, is_multi_input, location, idname
        )
        sockets.append(socket)
        return socket

    def __repr__(self) -> str:
        return f"bNode({self.name!r}, {self.idname})"


@dataclass(eq=False, slots=True)
class bNodeLink:
    """A link between two sockets (``bNodeLink``)."""

    fromnode: bNode
    fromsock: bNodeSocket
    tonode: bNode
    tosock: bNodeSocket
    multi_input_sort_id: int = 0
    """Position among the links into a multi-input socket."""
    is_valid: bool = True
    """``NODE_LINK_VALID``. Blender clears it for a link that closes a
    cycle, but also for one between sockets that do not fit, which is still
    drawn; so the layout goes by every link and breaks cycles itself."""


@dataclass(eq=False, slots=True)
class bNodeTreeZone:
    """A zone (``bNodeTreeZone``): a simulation, a repeat, a for-each
    element, a closure."""

    input_node: bNode
    output_node: bNode
    parent_zone: bNodeTreeZone | None = None
    """The zone this one is directly in."""
    child_zones: list[bNodeTreeZone] = field(default_factory=list)
    """The zones directly in this one."""
    child_nodes: list[bNode] = field(default_factory=list)
    """The nodes directly in the zone: not its own input and output node,
    nor the nodes inside a zone within it, but that zone's input and output
    node."""

    def nodes(self) -> list[bNode]:
        """Every node the zone is drawn around: its input and output node
        and all that is inside, zones within it included."""
        nodes = [self.input_node, *self.child_nodes]
        for zone in self.child_zones:
            nodes += zone.nodes()
        nodes.append(self.output_node)
        return list(dict.fromkeys(nodes))


@dataclass(eq=False, slots=True)
class bNodeTree:
    """Nodes and links (``bNodeTree``)."""

    nodes: list[bNode] = field(default_factory=list)
    links: list[bNodeLink] = field(default_factory=list)
    zones: list[bNodeTreeZone] = field(default_factory=list)
    """``zones()``, outer zones before the zones within them. (From Python
    Blender does not tell which nodes are in a zone; :mod:`.zones` works it
    out.)"""

    def add_node(self, node: bNode) -> bNode:
        self.nodes.append(node)
        return node

    def add_link(
        self, fromsock: bNodeSocket, tosock: bNodeSocket, multi_input_sort_id: int = 0
    ) -> bNodeLink:
        link = bNodeLink(
            fromsock.node, fromsock, tosock.node, tosock, multi_input_sort_id
        )
        self.links.append(link)
        return link


def new_reroute(parent: bNode | None = None) -> bNode:
    """A reroute node at the origin, as Blender would create it."""
    node = bNode(
        idname="NodeReroute",
        parent=parent,
        width=REROUTE_SIZE,
        draw_bounds=(0.0, -REROUTE_SIZE, REROUTE_SIZE, 0.0),
    )
    node.add_socket(False)
    node.add_socket(True)
    return node
