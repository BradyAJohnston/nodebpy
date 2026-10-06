"""Plain-data node trees for testing the layout without Blender.

``plain_node`` adds one node to a ``dna.bNodeTree``, ``plain_chain`` a chain
of them. ``random_tree(seed)`` builds a tree with frames (some nested),
reroutes, collapsed Math nodes, multi-input sockets and links that only run
forwards. ``positions`` and ``laid_out`` run the layout; ``node_overlaps``
counts the nodes a layout draws over each other.
"""

from __future__ import annotations

import random
from collections.abc import Iterable
from itertools import pairwise

from nodebpy.layout.config import SugiyamaOptions
from nodebpy.layout.dna import bNode, bNodeTree, new_reroute
from nodebpy.layout.edits import LayoutResult
from nodebpy.layout.pipeline import Pipeline
from nodebpy.layout.sugiyama import sugiyama_layout
from nodebpy.layout.zones import find_zones

from .metrics import LayoutMetrics, measure

MARGIN = (50.0, 20.0)
"""Room between nodes the plain-data tests lay out with: ``(x, y)``."""


def options(**fields) -> SugiyamaOptions:
    """Options for the plain-data tests: the test margin, and no snapping to
    the grid, so positions can be asserted exactly. ``test_snapping.py``
    turns it on."""
    return SugiyamaOptions(**{"margin": MARGIN, "snap_to_grid": False, **fields})


def plain_node(
    tree: bNodeTree,
    name: str,
    *,
    inputs: int = 1,
    outputs: int = 1,
    height: float = 100.0,
    width: float = 140.0,
    parent: bNode | None = None,
    idname: str = "GeometryNodeSetPosition",
    socket: str = "NodeSocketGeometry",
    multi_input: bool = False,
    collapsed: bool = False,
) -> bNode:
    """A node at the origin, sockets 22 apart below a 30 header."""
    node = tree.add_node(
        bNode(
            name,
            idname,
            width=width,
            draw_bounds=(0.0, -height, width, 0.0),
            parent=parent,
            is_collapsed=collapsed,
        )
    )
    for k in range(outputs):
        node.add_socket(True, location=(width, -30.0 - 22.0 * k), idname=socket)
    for k in range(inputs):
        node.add_socket(
            False,
            location=(0.0, -30.0 - 22.0 * (outputs + k)),
            idname=socket,
            is_multi_input=multi_input,
        )
    return node


def collapsed_math(tree: bNodeTree, name: str, parent: bNode | None = None) -> bNode:
    """A collapsed Math node: two value inputs, one value output."""
    return plain_node(
        tree,
        name,
        idname="ShaderNodeMath",
        socket="NodeSocketFloat",
        collapsed=True,
        height=30.0,
        inputs=2,
        parent=parent,
    )


def plain_chain(
    tree: bNodeTree, names: Iterable[str], **node_options
) -> dict[str, bNode]:
    """Nodes called *names*, each linked from its first output to the first
    input of the next. *node_options* are passed to :func:`plain_node`."""
    nodes = {name: plain_node(tree, name, **node_options) for name in names}
    for a, b in pairwise(nodes.values()):
        tree.add_link(a.outputs[0], b.inputs[0])
    return nodes


def positions(
    tree: bNodeTree,
    *,
    pipeline: Pipeline | None = None,
    selected_only: bool = False,
    **fields,
) -> dict[str, tuple[float, float]]:
    """Where the layout puts the top-left corner of each node, by name."""
    result = sugiyama_layout(
        tree, options(**fields), pipeline=pipeline, selected_only=selected_only
    )
    return {node.name: corner for node, corner in result.positions().items()}


def laid_out(tree: bNodeTree, **fields) -> LayoutMetrics:
    """Lay *tree* out in place, checking every step and that no nodes
    overlap, and measure the result."""
    result = sugiyama_layout(tree, options(**fields), verify=True)
    assert node_overlaps(result) == 0
    result.apply_to(tree)
    return measure(tree)


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
            node = collapsed_math(tree, f"m{i:02}", parent)
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
