"""Zones in the layout: which nodes are in a zone (``layout.zones``),
and the layout drawing a zone as a level row (``priority.zone_spine``)."""

import pytest

from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.priority import ZONE, zone_priorities, zone_spine
from nodebpy.layout.zones import find_zones

from .data import laid_out, plain_chain, plain_node


def _chain(tree: bNodeTree, names: str) -> dict[str, bNode]:
    return plain_chain(tree, names, inputs=2)


def _names(nodes) -> list[str]:
    return [node.name for node in nodes]


# ---------------------------------------------------------------------------
# Which nodes are in a zone
# ---------------------------------------------------------------------------


def test_zone_holds_what_is_between_its_input_and_output():
    """a -> [i -> b -> o] -> c, with f feeding b from outside and b also
    feeding d, which leads nowhere."""
    tree = bNodeTree()
    nodes = _chain(tree, "aiboc")
    f = plain_node(tree, "f")
    d = plain_node(tree, "d")
    tree.add_link(f.outputs[0], nodes["b"].inputs[1])
    tree.add_link(nodes["b"].outputs[0], d.inputs[0])

    (zone,) = find_zones(tree, [(nodes["i"], nodes["o"])])
    assert _names(zone.child_nodes) == ["b", "d"]
    assert _names(zone.nodes()) == ["i", "b", "d", "o"]
    assert zone.parent_zone is None and zone.child_zones == []


def test_nested_zones():
    """[i -> x -> [j -> y -> p] -> z -> o]: the inner zone's own nodes are
    the outer zone's only through it."""
    tree = bNodeTree()
    nodes = _chain(tree, "ixjypzo")
    zones = find_zones(tree, [(nodes["j"], nodes["p"]), (nodes["i"], nodes["o"])])

    outer, inner = zones
    assert (outer.input_node, inner.input_node) == (nodes["i"], nodes["j"])
    assert inner.parent_zone is outer and outer.child_zones == [inner]
    assert _names(inner.child_nodes) == ["y"]
    assert _names(outer.child_nodes) == ["x", "j", "p", "z"]
    assert sorted(_names(outer.nodes())) == sorted("ixjypzo")


def test_links_marked_invalid_do_not_put_a_node_in_a_zone():
    tree = bNodeTree()
    nodes = _chain(tree, "ibo")
    stray = plain_node(tree, "stray")
    tree.add_link(nodes["b"].outputs[0], stray.inputs[0]).is_valid = False
    (zone,) = find_zones(tree, [(nodes["i"], nodes["o"])])
    assert _names(zone.child_nodes) == ["b"]


# ---------------------------------------------------------------------------
# The spine
# ---------------------------------------------------------------------------


def _spine(zone, tree, taken=None) -> list[str]:
    return [f"{k.fromnode.name}{k.tonode.name}" for k in zone_spine(zone, tree, taken)]


def test_spine_follows_the_flow_links():
    """Two ways through the zone: i -> v -> w -> o carrying values, and
    i -> g -> o carrying geometry. The geometry is the spine, though the
    other way is longer."""
    tree = bNodeTree()
    nodes = {name: plain_node(tree, name, inputs=2, outputs=2) for name in "igo"}
    for name in "vw":
        nodes[name] = plain_node(tree, name, socket="NodeSocketFloat")
    for name in "io":
        nodes[name].outputs[1].idname = nodes[name].inputs[1].idname = "NodeSocketFloat"
    for a, b, out, into in (("i", "g", 0, 0), ("g", "o", 0, 0)):
        tree.add_link(nodes[a].outputs[out], nodes[b].inputs[into])
    tree.add_link(nodes["i"].outputs[1], nodes["v"].inputs[0])
    tree.add_link(nodes["v"].outputs[0], nodes["w"].inputs[0])
    tree.add_link(nodes["w"].outputs[0], nodes["o"].inputs[1])
    (zone,) = find_zones(tree, [(nodes["i"], nodes["o"])])
    assert _spine(zone, tree) == ["ig", "go"]

    # With nothing but values the longer way is taken.
    for node in nodes.values():
        for socket in (*node.inputs, *node.outputs):
            socket.idname = "NodeSocketFloat"
    assert _spine(zone, tree) == ["iv", "vw", "wo"]


def test_spine_of_an_outer_zone_follows_the_inner_one():
    tree = bNodeTree()
    nodes = _chain(tree, "ixjypzo")
    # A second, longer way through the inner zone.
    for name in "st":
        nodes[name] = plain_node(tree, name)
    for a, b, into in (("j", "s", 0), ("s", "t", 0), ("t", "p", 1)):
        tree.add_link(nodes[a].outputs[0], nodes[b].inputs[into])
    outer, inner = find_zones(
        tree, [(nodes["j"], nodes["p"]), (nodes["i"], nodes["o"])]
    )
    inner_spine = zone_spine(inner, tree)
    assert _spine(inner, tree) == ["js", "st", "tp"]
    assert _spine(outer, tree, set(inner_spine)) == [
        "ix", "xj", "js", "st", "tp", "pz", "zo",
    ]  # fmt: skip
    tree.zones = [outer, inner]
    priorities = zone_priorities(tree)
    assert priorities[nodes["s"].inputs[0]] == ZONE
    assert nodes["y"].inputs[0] not in priorities


def test_zone_whose_input_does_not_reach_its_output_has_no_spine():
    tree = bNodeTree()
    a, b = plain_node(tree, "a"), plain_node(tree, "b")
    (zone,) = find_zones(tree, [(a, b)])
    assert zone_spine(zone, tree) == []
    assert zone_priorities(tree) == {}


# ---------------------------------------------------------------------------
# The layout
# ---------------------------------------------------------------------------


def _uneven_zone() -> tuple[bNodeTree, list[bNode]]:
    """a -> [i -> t -> o] -> b through nodes of very different sizes whose
    geometry sockets sit at different heights, and with a feeder of ``t``."""
    tree = bNodeTree()
    nodes = _chain(tree, "aitob")
    nodes["t"].draw_bounds = (0.0, -400.0, 140.0, 0.0)
    nodes["t"].inputs[0].location = (0.0, -300.0)
    nodes["i"].outputs[0].location = (140.0, -80.0)
    feeder = plain_node(tree, "feeder", socket="NodeSocketFloat")
    tree.add_link(feeder.outputs[0], nodes["t"].inputs[1])
    tree.zones = find_zones(tree, [(nodes["i"], nodes["o"])])
    return tree, [nodes[name] for name in "ito"]


@pytest.mark.parametrize(
    ("reroutes", "socket_alignment", "direction"),
    [
        ("none", "NONE", "BALANCED"),
        ("none", "MODERATE", "BALANCED"),
        ("none", "FULL", "BALANCED"),
        ("all", "FULL", "BALANCED"),
        ("none", "FULL", "LEFT_UP"),
        ("none", "FULL", "RIGHT_DOWN"),
    ],
)
def test_zone_is_a_level_row(reroutes, socket_alignment, direction):
    """The nodes from the zone's input node through to its output node
    have their tops at one height under every socket alignment."""
    tree, spine = _uneven_zone()
    metrics = laid_out(
        tree,
        reroutes=reroutes,
        socket_alignment=socket_alignment,
        direction=direction,
    )
    assert (metrics.zones, metrics.level_zones) == (1, 1)
    tops = [node.top for node in spine]
    assert tops == pytest.approx([tops[0]] * 3, abs=0.01)


def test_zone_is_aligned_by_sockets_when_the_trunk_is_not_straightened():
    tree, _ = _uneven_zone()
    metrics = laid_out(tree, straighten_trunk=False, socket_alignment="FULL")
    assert (metrics.zones, metrics.level_zones) == (1, 0)
