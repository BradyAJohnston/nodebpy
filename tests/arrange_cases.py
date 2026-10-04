"""Node trees for judging layouts.

Small hand-built trees, each isolating one thing a layout should get right
(a chain should be a flat line, a branch-and-merge should be symmetric, …),
plus loaders for the larger real trees: nodebpy's asset groups and Blender's
bundled geometry-nodes essentials. Shared by the arrangement metric tests and
``tests/arrange_report.py``.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from itertools import pairwise
from pathlib import Path

import bpy
from bpy.types import Node, NodeTree

from nodebpy.builder import BundledLibrary

ESSENTIALS = Path(BundledLibrary("geometry_nodes_essentials.blend").path())


def _tree(name: str) -> NodeTree:
    return bpy.data.node_groups.new(name, "GeometryNodeTree")  # ty: ignore[invalid-argument-type]


def _math(tree: NodeTree, operation: str = "ADD") -> Node:
    node = tree.nodes.new("ShaderNodeMath")
    node.operation = operation  # ty: ignore[unresolved-attribute]
    return node


def _chain(tree: NodeTree, nodes: list[Node], to_input: int = 0) -> None:
    for a, b in pairwise(nodes):
        tree.links.new(a.outputs[0], b.inputs[to_input])


def chain() -> NodeTree:
    """A single line of nodes of different heights. Ideal: one flat row with
    every link straight."""
    tree = _tree("chain")
    nodes = [
        tree.nodes.new(idname)
        for idname in (
            "GeometryNodeMeshCube",
            "GeometryNodeSetPosition",
            "GeometryNodeTransform",
            "GeometryNodeSetShadeSmooth",
            "GeometryNodeJoinGeometry",
        )
    ]
    _chain(tree, nodes)
    return tree


def diamond() -> NodeTree:
    """One node feeding three branches that merge again. Ideal: the source
    and the merge sit level with the middle branch, the others symmetric
    above and below."""
    tree = _tree("diamond")
    source = tree.nodes.new("GeometryNodeMeshCube")
    join = tree.nodes.new("GeometryNodeJoinGeometry")
    tail = tree.nodes.new("GeometryNodeSetShadeSmooth")
    for _ in range(3):
        branch = tree.nodes.new("GeometryNodeSetPosition")
        tree.links.new(source.outputs[0], branch.inputs[0])
        tree.links.new(branch.outputs[0], join.inputs[0])
    tree.links.new(join.outputs[0], tail.inputs[0])
    return tree


def trunk_with_feeders() -> NodeTree:
    """A main line of geometry nodes, three of which take a value computed
    by a short side chain. Ideal: the trunk is a flat line and each side
    chain sits just below the node it feeds."""
    tree = _tree("trunk_with_feeders")
    trunk = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(5)]
    _chain(tree, trunk)
    for node in trunk[1:4]:
        first, second = _math(tree), _math(tree, "MULTIPLY")
        tree.links.new(first.outputs[0], second.inputs[0])
        tree.links.new(second.outputs[0], node.inputs["Offset"])
    return tree


def fan_in() -> NodeTree:
    """Eight values combined by one node. Ideal: a compact block of inputs
    rather than one very tall column."""
    tree = _tree("fan_in")
    join = tree.nodes.new("GeometryNodeJoinGeometry")
    for _ in range(8):
        source = tree.nodes.new("GeometryNodeMeshCube")
        move = tree.nodes.new("GeometryNodeSetPosition")
        tree.links.new(source.outputs[0], move.inputs[0])
        tree.links.new(move.outputs[0], join.inputs[0])
    return tree


def framed_stages() -> NodeTree:
    """Three frames processed one after the other, with a value node feeding
    the last two from outside. Ideal: the frames in a row, left to right,
    none overlapping."""
    tree = _tree("framed_stages")
    previous: Node = tree.nodes.new("GeometryNodeMeshCube")
    value = _math(tree)
    for stage in range(3):
        frame = tree.nodes.new("NodeFrame")
        frame.label = f"Stage {stage + 1}"
        nodes = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(3)]
        for node in nodes:
            node.parent = frame
        tree.links.new(previous.outputs[0], nodes[0].inputs[0])
        _chain(tree, nodes)
        if stage:
            tree.links.new(value.outputs[0], nodes[1].inputs["Offset"])
        previous = nodes[-1]
    return tree


def nested_frames() -> NodeTree:
    """A frame inside a frame, with links entering and leaving both."""
    tree = _tree("nested_frames")
    outer = tree.nodes.new("NodeFrame")
    outer.label = "Outer"
    inner = tree.nodes.new("NodeFrame")
    inner.label = "Inner"
    inner.parent = outer
    source = tree.nodes.new("GeometryNodeMeshCube")
    a, b, c, d = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(4))
    a.parent = outer
    b.parent = c.parent = inner
    _chain(tree, [source, a, b, c, d])
    value = _math(tree)
    value.parent = outer
    tree.links.new(value.outputs[0], c.inputs["Offset"])
    tree.links.new(value.outputs[0], d.inputs["Offset"])
    return tree


def long_links() -> NodeTree:
    """A value used at the start and at the end of a chain, so one link
    spans several columns. Ideal: the long link passes clear of the nodes
    in between."""
    tree = _tree("long_links")
    value = _math(tree)
    nodes = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(5)]
    _chain(tree, nodes)
    tree.links.new(value.outputs[0], nodes[0].inputs["Offset"])
    tree.links.new(value.outputs[0], nodes[4].inputs["Offset"])
    return tree


CASES: dict[str, Callable[[], NodeTree]] = {
    case.__name__: case
    for case in (
        chain,
        diamond,
        trunk_with_feeders,
        fan_in,
        framed_stages,
        nested_frames,
        long_links,
    )
}


def asset_groups() -> dict[str, Callable[[], NodeTree]]:
    """nodebpy's own asset groups, by class name."""
    from nodebpy.nodes.geometry import groups

    return {
        cls.__name__: cls.create_group
        for cls in (
            groups.ClipFieldToBox,
            groups.GeometryPrincipalComponents,
            groups.PrincipalComponents,
            groups.SliceToIndices,
        )
    }


def essentials(names: list[str] | None = None) -> Iterator[NodeTree]:
    """Fresh copies of the node groups in Blender's bundled geometry-nodes
    essentials (all of them, or *names*). Nothing if it is not installed."""
    if not ESSENTIALS.is_file():
        return
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(ESSENTIALS), link=False
    ) as (src, dst):
        dst.node_groups = [
            name for name in src.node_groups if names is None or name in names
        ]
    yield from dst.node_groups


def reset_locations(tree: NodeTree) -> None:
    """Pile every node at the origin, as in a freshly built tree."""
    for node in tree.nodes:
        node.location = (0, 0)
