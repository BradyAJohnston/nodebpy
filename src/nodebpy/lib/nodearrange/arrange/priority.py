# SPDX-License-Identifier: GPL-2.0-or-later
"""Which links matter most to the reader.

A node tree usually has a *trunk*: the line the main data flows along (the
geometry through a chain of geometry nodes, the shader into the output),
with side chains computing the values the trunk's nodes take. A good layout
keeps the trunk short and straight and hangs the side chains off it.

Each socket gets a priority, and a link the sum of its two sockets':

- 2 for a node's *flow* socket: the first linked input (and the first
  linked output) that carries the tree's main data (geometry, shader,
  bundle, closure);
- 1 for the first linked input (output) of a node with no linked flow
  socket on that side: its main operand;
- 0 for every other socket.

So a geometry-to-geometry link scores 4, a value entering a node's first
input 1 or 2, and a field wired into a geometry node's lesser input 0 or 1.
The ranking keeps heavier links short; the placement aligns a node with its
heaviest neighbour first. (:func:`.graph.link_priority` gives the priority
of a link of the layout graph.)
"""

from __future__ import annotations

from ..dna import bNodeLink, bNodeSocket, bNodeTree, bNodeTreeZone

FLOW_SOCKETS = frozenset(
    {
        "NodeSocketGeometry",
        "NodeSocketShader",
        "NodeSocketBundle",
        "NodeSocketClosure",
    }
)
"""Socket types carrying a tree's main data."""

FLOW = 2
MAIN = 1

ZONE = 4
"""Priority of the sockets along a zone's spine (see :func:`zone_spine`):
enough that a link of the spine outweighs any other."""

SPINE_MIN_PRIORITY = 2 * ZONE
"""The priority of a link of a zone's spine, and of no other."""

TRUNK_MIN_PRIORITY = 3
"""The placement aligns a node first with neighbours across a link of at
least this priority (a flow socket at one end and a flow or main socket at
the other), and only then with a median neighbour. Lower, and long links of
side chains start cutting through nodes."""


def _type_priority(idname: str) -> int:
    """How likely a socket of this type is a node's main one: Blender's
    ``get_main_socket_priority`` (``node_relationships.cc``), by idname."""
    kind = idname.removeprefix("NodeSocket")
    if kind.startswith(("Virtual", "Menu")) or not idname.startswith("NodeSocket"):
        return 1 if kind.startswith("Menu") else 0
    if kind.startswith("Bool"):
        return 2
    if kind.startswith("Int") and not kind.startswith("IntVector"):
        return 3
    if kind.startswith("Float"):
        return 4
    if kind.startswith("Vector"):
        return 5
    if kind.startswith("Color"):
        return 6
    return 7


def main_socket(sockets: list[bNodeSocket]) -> bNodeSocket | None:
    """The main socket among a node's inputs (or outputs), as Blender picks
    it for inserting a node on a link: the first one of the type that ranks
    highest."""
    best = None
    best_priority = -1
    for socket in sockets:
        priority = _type_priority(socket.idname)
        if priority > best_priority:
            best, best_priority = socket, priority
    return best


def socket_priorities(tree: bNodeTree, mode: str = "flow") -> dict[bNodeSocket, int]:
    """The priority of every socket that has one.

    *mode* ``"flow"`` is the scheme of the module notes. ``"main"`` instead
    gives priority 2 to each node's main linked input and main linked output
    (:func:`main_socket`), whatever its type, so chains of values get a
    trunk as well."""
    linked: dict[bNodeSocket, None] = {}
    for link in tree.links:
        linked[link.fromsock] = None
        linked[link.tosock] = None

    priorities: dict[bNodeSocket, int] = {}
    for node in tree.nodes:
        for side in (node.inputs, node.outputs):
            used = [socket for socket in side if socket in linked]
            if not used:
                continue
            if mode == "main":
                main = main_socket(used)
                assert main is not None
                priorities[main] = FLOW
                continue
            flow = next((s for s in used if s.idname in FLOW_SOCKETS), None)
            if flow is not None:
                priorities[flow] = FLOW
            else:
                priorities[used[0]] = MAIN

    return priorities


def zone_spine(
    zone: bNodeTreeZone, tree: bNodeTree, taken: set[bNodeLink] | None = None
) -> list[bNodeLink]:
    """The links along which *zone* is drawn as a row, from its
    input node to its output node: of the ways through the zone, the one
    that keeps to the spines of the zones inside it (*taken*), then has the
    most links carrying the main data, then is the longest. Empty when the
    input node does not lead to the output node."""
    inside = set(zone.nodes())
    out_links: dict[object, list[bNodeLink]] = {}
    for link in tree.links:
        if link.is_valid and link.fromnode in inside and link.tonode in inside:
            out_links.setdefault(link.fromnode, []).append(link)

    def score(link: bNodeLink) -> int:
        is_flow = (
            link.fromsock.idname in FLOW_SOCKETS and link.tosock.idname in FLOW_SOCKETS
        )
        on_spine = taken is not None and link in taken
        return 1 + 1_000 * is_flow + 1_000_000 * on_spine

    # The best way on from each node: (score, first link), or None when
    # the node does not lead to the output node. Depth first, on a stack.
    best: dict[object, tuple[int, bNodeLink | None] | None] = {
        zone.output_node: (0, None)
    }
    active = {zone.input_node}
    stack = [(zone.input_node, iter(out_links.get(zone.input_node, ())))]
    while stack:
        node, links = stack[-1]
        for link in links:
            target = link.tonode
            if target not in best and target not in active:
                active.add(target)
                stack.append((target, iter(out_links.get(target, ()))))
                break
        else:
            stack.pop()
            active.discard(node)
            choice = None
            for link in out_links.get(node, ()):
                onward = best.get(link.tonode)
                if onward is None:
                    continue
                total = score(link) + onward[0]
                if choice is None or total > choice[0]:
                    choice = (total, link)
            best[node] = choice

    spine = []
    step = best.get(zone.input_node)
    while step is not None and step[1] is not None:
        spine.append(step[1])
        step = best[step[1].tonode]
    return spine


def zone_priorities(tree: bNodeTree) -> dict[bNodeSocket, int]:
    """Priorities that make each zone's spine the heaviest links there are
    (nodebpy addition), so the placement draws a zone as a row: its input
    node, the nodes the data passes through, its output node."""
    priorities: dict[bNodeSocket, int] = {}
    taken: set[bNodeLink] = set()
    # Inner zones first, so the zone around them follows their spine.
    for zone in reversed(tree.zones):
        spine = zone_spine(zone, tree, taken)
        taken.update(spine)
        for link in spine:
            priorities[link.fromsock] = ZONE
            priorities[link.tosock] = ZONE
    return priorities
