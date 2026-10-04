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

from ..dna import bNodeSocket, bNodeTree

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


def socket_priorities(tree: bNodeTree) -> dict[bNodeSocket, int]:
    """The priority of every socket that has one (see the module notes)."""
    linked: dict[bNodeSocket, None] = {}
    for link in tree.links:
        if link.is_valid:
            linked[link.fromsock] = None
            linked[link.tosock] = None

    priorities: dict[bNodeSocket, int] = {}
    for node in tree.nodes:
        for side in (node.inputs, node.outputs):
            used = [socket for socket in side if socket in linked]
            if not used:
                continue
            flow = next((s for s in used if s.idname in FLOW_SOCKETS), None)
            if flow is not None:
                priorities[flow] = FLOW
            else:
                priorities[used[0]] = MAIN

    return priorities
