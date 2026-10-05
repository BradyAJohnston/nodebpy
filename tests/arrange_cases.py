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


def shader_material() -> NodeTree:
    """A shader tree: a texture chain into a BSDF, mixed with a second
    shader. The shader links are the trunk; the texture chain feeds it."""
    tree = bpy.data.node_groups.new("shader_material", "ShaderNodeTree")  # ty: ignore[invalid-argument-type]
    new = tree.nodes.new
    coords, mapping, noise = (
        new("ShaderNodeTexCoord"),
        new("ShaderNodeMapping"),
        new("ShaderNodeTexNoise"),
    )
    ramp, bump = new("ShaderNodeValToRGB"), new("ShaderNodeBump")
    principled, emission = new("ShaderNodeBsdfPrincipled"), new("ShaderNodeEmission")
    mix, fresnel = new("ShaderNodeMixShader"), new("ShaderNodeFresnel")
    tree.links.new(coords.outputs["Object"], mapping.inputs["Vector"])
    tree.links.new(mapping.outputs[0], noise.inputs["Vector"])
    tree.links.new(noise.outputs[0], ramp.inputs[0])
    tree.links.new(noise.outputs[0], bump.inputs["Height"])
    tree.links.new(ramp.outputs[0], principled.inputs["Base Color"])
    tree.links.new(bump.outputs[0], principled.inputs["Normal"])
    tree.links.new(ramp.outputs[0], emission.inputs["Color"])
    tree.links.new(fresnel.outputs[0], mix.inputs[0])
    tree.links.new(principled.outputs[0], mix.inputs[1])
    tree.links.new(emission.outputs[0], mix.inputs[2])
    return tree


def compositor_chain() -> NodeTree:
    """A compositor tree: no geometry or shader sockets at all, so the main
    line is the colour chain."""
    tree = bpy.data.node_groups.new("compositor_chain", "CompositorNodeTree")  # ty: ignore[invalid-argument-type]
    new = tree.nodes.new
    blur, glare, over = (
        new("CompositorNodeBlur"),
        new("CompositorNodeGlare"),
        new("CompositorNodeAlphaOver"),
    )
    balance, lens = new("CompositorNodeColorBalance"), new("CompositorNodeLensdist")
    tree.links.new(blur.outputs[0], glare.inputs[0])
    tree.links.new(glare.outputs[0], over.inputs[1])
    tree.links.new(balance.outputs[0], over.inputs[2])
    tree.links.new(over.outputs[0], lens.inputs[0])
    return tree


def zones() -> NodeTree:
    """A simulation zone and a repeat zone in one chain, each with nodes
    inside and a value fed in from outside. Ideal: each zone's nodes sit
    between its input and output node, with nothing else among them."""
    tree = _tree("zones")
    new = tree.nodes.new
    cube = new("GeometryNodeMeshCube")
    sim_in, sim_out = (
        new("GeometryNodeSimulationInput"),
        new("GeometryNodeSimulationOutput"),
    )
    sim_in.pair_with_output(sim_out)  # ty: ignore[unresolved-attribute]
    rep_in, rep_out = new("GeometryNodeRepeatInput"), new("GeometryNodeRepeatOutput")
    rep_in.pair_with_output(rep_out)  # ty: ignore[unresolved-attribute]
    move, noise, scale = (
        new("GeometryNodeSetPosition"),
        new("ShaderNodeTexNoise"),
        _math(tree, "MULTIPLY"),
    )
    subdivide, smooth = (
        new("GeometryNodeSubdivideMesh"),
        new("GeometryNodeSetShadeSmooth"),
    )
    outside, join = new("GeometryNodeTransform"), new("GeometryNodeJoinGeometry")
    rep_out.repeat_items.new("GEOMETRY", "Geometry")  # ty: ignore[unresolved-attribute]

    def geometry(sockets):
        return next(s for s in sockets if s.type == "GEOMETRY")

    line = [cube, sim_in, move, sim_out, rep_in, subdivide, smooth, rep_out, join]
    for a, b in pairwise(line):
        tree.links.new(geometry(a.outputs), geometry(b.inputs))
    tree.links.new(noise.outputs[0], scale.inputs[0])
    tree.links.new(scale.outputs[0], move.inputs["Offset"])
    # A branch that leaves before the zones and joins after them.
    tree.links.new(cube.outputs[0], outside.inputs[0])
    tree.links.new(outside.outputs[0], join.inputs[0])
    return tree


def annotated() -> NodeTree:
    """What a hand-made tree looks like: a labelled frame around part of the
    chain, reroutes the user placed (one labelled), a frame that only holds
    a note, and a second, unconnected group of nodes."""
    tree = _tree("annotated")
    new = tree.nodes.new
    cube, move, transform, join = (
        new("GeometryNodeMeshCube"),
        new("GeometryNodeSetPosition"),
        new("GeometryNodeTransform"),
        new("GeometryNodeJoinGeometry"),
    )
    _chain(tree, [cube, move, transform, join])
    stage = new("NodeFrame")
    stage.label = "Deform"
    move.parent = transform.parent = stage

    position, offset = new("GeometryNodeInputPosition"), new("ShaderNodeVectorMath")
    first, second = new("NodeReroute"), new("NodeReroute")
    second.label = "offset"
    tree.links.new(position.outputs[0], offset.inputs[0])
    tree.links.new(offset.outputs[0], first.inputs[0])
    tree.links.new(first.outputs[0], second.inputs[0])
    tree.links.new(second.outputs[0], move.inputs["Offset"])
    tree.links.new(first.outputs[0], transform.inputs["Translation"])
    # The original cube also goes straight to the join, past the frame.
    tree.links.new(cube.outputs[0], join.inputs[0])

    note = new("NodeFrame")
    note.label = "TODO: expose the offset"
    value = new("ShaderNodeValue")
    value.parent = note

    # Unconnected to the rest.
    grid, wire = new("GeometryNodeMeshGrid"), new("GeometryNodeMeshToCurve")
    tree.links.new(grid.outputs[0], wire.inputs[0])
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
        shader_material,
        compositor_chain,
        zones,
        annotated,
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
