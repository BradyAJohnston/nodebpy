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
        g.JoinGeometry(geo_in, geo_in >> g.SubdivisionSurface()) >> geo_out

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
        g.JoinGeometry(t1, t2) >> tree.outputs.geometry()

    assert snapshot == to_mermaid(tree)


def test_diagram_custom_node_group(snapshot):
    with g.tree() as tree:
        items = [OtherVertex() for _ in range(10)]
        switch = g.IndexSwitch.integer(*items)
        switch >> OffsetVector() >> tree.outputs.vector("Vector")

    assert snapshot == to_mermaid(tree)


def test_diagram_other_vertex(snapshot):
    with g.tree() as tree:
        other = OtherVertex()

    assert snapshot == to_mermaid(other.node.node_tree)


def test_diagram_bit_decoder(snapshot):
    N_BITS = 4
    with g.tree("8-Bit Decoder", arrange="simple") as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(N_BITS)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]

        for i, combo in enumerate(product((False, True), repeat=N_BITS)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")

    assert snapshot == to_mermaid(tree)
