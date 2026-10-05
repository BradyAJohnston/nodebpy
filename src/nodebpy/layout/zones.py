# SPDX-License-Identifier: GPL-2.0-or-later
"""Which nodes are in which zone.

Blender works this out itself (``node_tree_zones.cc``) and keeps it on the
tree (``bNodeTree::zones()``), but does not show it to Python: there only
the pairing of a zone's input node with its output node can be read. So
for a tree read from Python the zones are found here, by Blender's rule: a
node is in a zone when it depends on the zone's input node and the zone's
output node does not come before it.
"""

from __future__ import annotations

from collections.abc import Iterable

from .dna import bNode, bNodeTree, bNodeTreeZone


def _downstream(start: bNode, out_nodes: dict[bNode, list[bNode]]) -> dict[bNode, None]:
    """*start* and every node that depends on it, in the order found."""
    found = {start: None}
    pending = [start]
    while pending:
        for node in out_nodes.get(pending.pop(), ()):
            if node not in found:
                found[node] = None
                pending.append(node)
    return found


def find_zones(
    tree: bNodeTree, pairs: Iterable[tuple[bNode, bNode]]
) -> list[bNodeTreeZone]:
    """The zones of *tree*, given the (input node, output node) of each,
    outer zones before the zones within them."""
    out_nodes: dict[bNode, list[bNode]] = {}
    for link in tree.links:
        if link.is_valid:
            out_nodes.setdefault(link.fromnode, []).append(link.tonode)

    order = {node: i for i, node in enumerate(tree.nodes)}
    inside: list[tuple[bNodeTreeZone, dict[bNode, None]]] = []
    for input_node, output_node in pairs:
        after_output = _downstream(output_node, out_nodes)
        members = {
            node: None
            for node in sorted(
                _downstream(input_node, out_nodes), key=order.__getitem__
            )
            if node is not input_node and node not in after_output
        }
        inside.append((bNodeTreeZone(input_node, output_node), members))

    # Outer zones first: a zone has more nodes inside than any zone in it.
    inside.sort(key=lambda item: -len(item[1]))
    for i, (zone, _) in enumerate(inside):
        # The innermost zone with this one's input node inside.
        for outer, members in reversed(inside[:i]):
            if zone.input_node in members and zone.output_node in members:
                zone.parent_zone = outer
                outer.child_zones.append(zone)
                break

    for zone, members in inside:
        nested: set[bNode] = set()
        for other, others in inside:
            if other is not zone and _is_within(other, zone):
                nested.update(others)
        zone.child_nodes = [node for node in members if node not in nested]

    return [zone for zone, _ in inside]


def _is_within(zone: bNodeTreeZone, outer: bNodeTreeZone) -> bool:
    parent = zone.parent_zone
    while parent is not None:
        if parent is outer:
            return True
        parent = parent.parent_zone
    return False
