# SPDX-License-Identifier: GPL-2.0-or-later
"""Link priorities.

A node tree usually has a *trunk*: the line the main data flows along, such
as the geometry through a chain of geometry nodes or the shader into the
output. Side chains compute the values the trunk's nodes take. The
placement keeps the trunk straight and hangs the side chains off it.

Each socket gets a priority, and a link the sum of its two sockets':

- 2 for a node's *flow* socket: the first linked input (and the first
  linked output) that carries the tree's main data (geometry, shader,
  bundle, closure).
- 1 for the first linked input (output) of a node with no linked flow
  socket on that side: its main operand.
- 0 for every other socket.

So a geometry-to-geometry link scores 4, a value entering a node's first
input 1 or 2, and a field wired into a geometry node's lesser input 0 or 1.
The placement aligns a node across its heaviest link first. Priorities do
not affect the ranking. :func:`.model.link_priority` gives the priority of
a link of the layout graph.
"""

from __future__ import annotations

from .dna import bNodeLink, bNodeSocket, bNodeTree, bNodeTreeZone

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


def is_flow_socket(socket: bNodeSocket) -> bool:
    """Whether *socket* is of a type that carries a tree's main data. A
    link is a flow link when the output it comes from is."""
    return socket.idname in FLOW_SOCKETS


ZONE = 4
"""Priority of the sockets along a zone's spine (see :func:`zone_spine`):
enough that a link of the spine outweighs any other."""

SPINE_MIN_PRIORITY = 2 * ZONE
"""The priority of a link of a zone's spine, and of no other."""

TRUNK_MIN_PRIORITY = 3
"""The placement aligns a node first with neighbours across a link of at
least this priority (a flow socket at one end and a flow or main socket at
the other), and only then with a median neighbour. With a lower value, long
links of side chains start cutting through nodes."""


def socket_priorities(tree: bNodeTree) -> dict[bNodeSocket, int]:
    """The priority of every socket that has one."""
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
            flow = next((s for s in used if is_flow_socket(s)), None)
            if flow is not None:
                priorities[flow] = FLOW
            else:
                priorities[used[0]] = MAIN

    return priorities


def zone_spine(
    zone: bNodeTreeZone, tree: bNodeTree, taken: set[bNodeLink] | None = None
) -> list[bNodeLink]:
    """The links along which *zone* is drawn as a row, from its input node
    to its output node. Of the ways through the zone, it is the one that
    keeps to the spines of the zones inside it (*taken*), then has the most
    flow links, then is the longest. Empty when the input node does not
    lead to the output node."""
    inside = set(zone.nodes())
    out_links: dict[object, list[bNodeLink]] = {}
    for link in tree.links:
        if link.is_valid and link.fromnode in inside and link.tonode in inside:
            out_links.setdefault(link.fromnode, []).append(link)

    def score(link: bNodeLink) -> int:
        is_flow = is_flow_socket(link.fromsock)
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
    """Priorities that make each zone's spine the heaviest links there are,
    so the placement draws a zone as a row: its input node, the nodes the
    data passes through, its output node."""
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
