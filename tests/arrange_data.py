"""Plain-data node trees for testing the layout without Blender.

``plain_node`` adds one node to a ``dna.bNodeTree``. ``random_tree(seed)`` builds a ``dna.bNodeTree`` with frames (some nested),
reroutes, collapsed Math nodes, multi-input sockets and links that only run
forwards. ``node_overlaps`` checks a layout for nodes drawn over each other.
"""

from __future__ import annotations

import random

from nodebpy.lib.nodearrange.arrange.edits import LayoutResult
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree, new_reroute
from nodebpy.lib.nodearrange.zones import find_zones

MARGIN = (50.0, 20.0)
"""Room between nodes the pure-layout tests arrange with: ``(x, y)``."""


def plain_node(
    tree: bNodeTree,
    name: str,
    *,
    inputs: int = 1,
    outputs: int = 1,
    height: float = 100.0,
    parent: bNode | None = None,
    idname: str = "GeometryNodeSetPosition",
    socket: str = "NodeSocketGeometry",
    multi_input: bool = False,
    collapsed: bool = False,
) -> bNode:
    """A 140-wide node at the origin, sockets 22 apart below a 30 header."""
    node = tree.add_node(
        bNode(
            name,
            idname,
            width=140.0,
            draw_bounds=(0.0, -height, 140.0, 0.0),
            parent=parent,
            is_collapsed=collapsed,
        )
    )
    for k in range(outputs):
        node.add_socket(True, location=(140.0, -30.0 - 22.0 * k), idname=socket)
    for k in range(inputs):
        node.add_socket(
            False,
            location=(0.0, -30.0 - 22.0 * (outputs + k)),
            idname=socket,
            is_multi_input=multi_input,
        )
    return node


def random_tree(seed: int, zones: int = 0) -> bNodeTree:
    """A random tree. With *zones*, up to that many pairs of its nodes are
    made the input and output node of a zone; such zones may overlap each
    other and the frames in ways Blender's cannot."""
    tree = _random_tree(seed)
    if zones:
        rng = random.Random(seed + 1000)
        nodes = [n for n in tree.nodes if not n.is_frame() and not n.is_reroute()]
        pairs = []
        for _ in range(zones):
            link = rng.choice(tree.links) if tree.links else None
            if link is None:
                break
            start, end = link.fromnode, link.tonode
            for _ in range(rng.randint(0, 3)):
                onward = [k for k in tree.links if k.fromnode is end]
                if not onward:
                    break
                end = rng.choice(onward).tonode
            taken = {n for pair in pairs for n in pair}
            if start in nodes and end in nodes and not {start, end} & taken:
                pairs.append((start, end))
        tree.zones = find_zones(tree, pairs)
    return tree


def _random_tree(seed: int) -> bNodeTree:
    rng = random.Random(seed)
    tree = bNodeTree()
    count = rng.randint(2, 28)

    frames: list[bNode] = []
    for i in range(rng.choice([0, 0, 1, 2, 4])):
        parent = rng.choice([None, *frames]) if frames and rng.random() < 0.4 else None
        frames.append(
            tree.add_node(
                bNode(f"F{i}", "NodeFrame", label=rng.choice(["", "x"]), parent=parent)
            )
        )

    nodes: list[bNode] = []
    for i in range(count):
        kind = rng.random()
        parent = rng.choice([None, *frames]) if frames else None
        if kind < 0.1:
            node = tree.add_node(new_reroute(parent))
            node.name = f"r{i:02}"
            if rng.random() < 0.2:
                node.label = "keep"
        elif kind < 0.25:
            node = plain_node(
                tree,
                f"m{i:02}",
                idname="ShaderNodeMath",
                socket="NodeSocketFloat",
                collapsed=True,
                height=30.0,
                inputs=2,
                parent=parent,
            )
        elif kind < 0.3:
            node = plain_node(tree, f"j{i:02}", multi_input=True, parent=parent)
        else:
            n_in, n_out = rng.randint(1, 4), rng.randint(1, 3)
            node = plain_node(
                tree,
                f"n{i:02}",
                inputs=n_in,
                outputs=n_out,
                height=30.0 + 22.0 * (n_in + n_out) + 10.0,
                parent=parent,
                socket=rng.choice(["NodeSocketGeometry", "NodeSocketFloat"]),
            )
        nodes.append(node)

    used: set[object] = set()
    for _ in range(rng.randint(count // 2, 2 * count)):
        i, j = sorted(rng.sample(range(count), 2))
        output = rng.choice(nodes[i].outputs)
        target = rng.choice(nodes[j].inputs)
        if (target in used and not target.is_multi_input) or (output, target) in used:
            continue
        used.update((target, (output, target)))
        tree.add_link(
            output, target, sum(1 for link in tree.links if link.tosock is target)
        )

    return tree


def node_overlaps(result: LayoutResult) -> int:
    """How many pairs of (non-reroute) nodes the layout draws overlapping."""
    rects = []
    for node, (x, y) in result.positions().items():
        if not node.is_reroute():
            rects.append((x, y - (node.top - node.bottom), x + node.width, y))

    count = 0
    for i, a in enumerate(rects):
        for b in rects[i + 1 :]:
            if (
                a[0] < b[2] - 1
                and b[0] < a[2] - 1
                and a[1] < b[3] - 1
                and b[1] < a[3] - 1
            ):
                count += 1
    return count
