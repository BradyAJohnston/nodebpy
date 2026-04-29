# SPDX-License-Identifier: GPL-3.0-or-later
"""Snapshot tests for Mermaid diagram generation."""

from functools import reduce
from itertools import product
from operator import and_

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.diagram import to_mermaid
from nodebpy.nodes.geometry.groups import OffsetVector, OtherVertex


def test_diagram_simple_chain(snapshot):
    """Linear chain of geometry nodes."""
    with TreeBuilder("DiagramSimple") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        geo_in >> g.SetPosition() >> g.TransformGeometry() >> geo_out

    assert snapshot == to_mermaid(tree)


def test_diagram_join_geometry(snapshot):
    """Fan-in with JoinGeometry — tests multiple inputs to one node."""
    with TreeBuilder("DiagramJoin") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        g.JoinGeometry([geo_in, geo_in >> g.SubdivisionSurface()]) >> geo_out

    assert snapshot == to_mermaid(tree)


def test_diagram_math_operation(snapshot):
    """Math nodes carry an operation label in the diagram."""
    with TreeBuilder("DiagramMath") as tree:
        val = tree.inputs.float("Value", 1.0)
        result = tree.outputs.float("Result")
        (val * 2.0 + 1.0) >> result

    assert snapshot == to_mermaid(tree)


def test_diagram_shared_input(snapshot):
    """Single input feeding multiple branches — tests fan-out edge rendering."""
    with TreeBuilder("DiagramFanOut") as tree:
        geo_in = tree.inputs.geometry()
        scale = tree.inputs.float("Scale", 1.0)
        t1 = g.TransformGeometry(scale=scale)
        t2 = g.TransformGeometry(scale=scale)
        geo_in >> t1
        geo_in >> t2
        g.JoinGeometry([t1, t2]) >> tree.outputs.geometry()

    assert snapshot == to_mermaid(tree)


def test_diagram_custom_node_group(snapshot):
    with g.tree() as tree:
        items = [OtherVertex() for _ in range(10)]
        switch = g.IndexSwitch.integer(items=items)
        switch >> OffsetVector() >> tree.outputs.vector("Vector")

    assert snapshot == to_mermaid(tree)


def test_diagram_other_vertex(snapshot):
    with g.tree():
        other = OtherVertex()

    assert snapshot == to_mermaid(other.node.node_tree)


def test_diagram_node_label_params(snapshot):
    """Non-default seed, scalar scale, and offset values appear in node labels."""
    with TreeBuilder("DiagramLabelParams") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()

        distribute = g.DistributePointsOnFaces()
        distribute.node.inputs["Seed"].default_value = 7

        noise = g.NoiseTexture()
        noise.node.inputs["Scale"].default_value = 3.0

        set_pos = g.SetPosition()
        set_pos.node.inputs["Offset"].default_value = (1.0, 0.0, 0.5)
        geo_in >> set_pos >> geo_out

    assert snapshot == to_mermaid(tree)


def test_diagram_reroute_no_input(snapshot):
    """Reroute with no incoming link is skipped without error."""
    with TreeBuilder("DiagramRerouteNoInput") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        set_pos = g.SetPosition()
        geo_in >> set_pos >> geo_out

        nt = tree.tree
        reroute = nt.nodes.new("NodeReroute")
        nt.links.new(reroute.outputs[0], set_pos.node.inputs["Position"])

        # TreeBuilder.__exit__ prunes disconnected reroutes, so capture here
        result = to_mermaid(tree)

    assert snapshot == result


def test_diagram_reroute_dedup(snapshot):
    """Two reroute paths from the same source produce only one edge."""
    with TreeBuilder("DiagramRerouteDedup") as tree:
        geo_in = tree.inputs.geometry()
        geo_out = tree.outputs.geometry()
        set_pos = g.SetPosition()
        join = g.JoinGeometry()
        geo_in >> set_pos
        join >> geo_out

        nt = tree.tree
        r1 = nt.nodes.new("NodeReroute")
        r2 = nt.nodes.new("NodeReroute")
        nt.links.new(set_pos.node.outputs["Geometry"], r1.inputs[0])
        nt.links.new(set_pos.node.outputs["Geometry"], r2.inputs[0])
        nt.links.new(r1.outputs[0], join.node.inputs["Geometry"])
        nt.links.new(r2.outputs[0], join.node.inputs["Geometry"])

    assert snapshot == to_mermaid(tree)


def test_diagram_bit_decoder(snapshot):
    N_BITS = 4
    with g.tree("8-Bit Decoder", arrange="simple") as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(N_BITS)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]

        for i, combo in enumerate(product((False, True), repeat=N_BITS)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")

    assert snapshot == to_mermaid(tree)
