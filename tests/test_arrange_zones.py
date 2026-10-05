"""Zones in the layout: which nodes are in a zone (``nodearrange.zones``),
and the layout drawing a zone as a level row (``priority.zone_spine``)."""

from itertools import pairwise

import pytest

from nodebpy.lib.nodearrange.arrange.edits import MoveNode, RemoveNode
from nodebpy.lib.nodearrange.arrange.priority import ZONE, zone_priorities, zone_spine
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree
from nodebpy.lib.nodearrange.metrics import measure
from nodebpy.lib.nodearrange.zones import find_zones

from .arrange_fuzz import node_overlaps, plain_node, random_tree

MARGIN = (50.0, 20.0)


def _chain(tree: bNodeTree, names: str, **kwargs) -> dict[str, bNode]:
    nodes = {name: plain_node(tree, name, inputs=2, **kwargs) for name in names}
    for a, b in pairwise(names):
        tree.add_link(nodes[a].outputs[0], nodes[b].inputs[0])
    return nodes


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


def test_spine_follows_the_main_data():
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


def _measured(tree: bNodeTree, **settings):
    result = sugiyama_layout(tree, Settings(**settings), MARGIN, verify=True)
    assert node_overlaps(result) == 0
    result.apply_to(tree)
    return measure(tree)


@pytest.mark.parametrize("add_reroutes", [False, True])
@pytest.mark.parametrize("socket_alignment", ["NONE", "MODERATE", "FULL"])
@pytest.mark.parametrize("direction", ["BALANCED", "LEFT_UP", "RIGHT_DOWN"])
def test_zone_is_a_level_row(add_reroutes, socket_alignment, direction):
    """The nodes from the zone's input node through to its output node
    have their tops at one height, whatever the alignment asked for
    elsewhere."""
    tree, spine = _uneven_zone()
    metrics = _measured(
        tree,
        add_reroutes=add_reroutes,
        socket_alignment=socket_alignment,
        direction=direction,
    )
    assert (metrics.zones, metrics.level_zones) == (1, 1)
    tops = [node.top for node in spine]
    assert tops == pytest.approx([tops[0]] * 3, abs=0.01)


def test_zones_can_be_left_alone():
    """Without it the nodes are aligned by their sockets when that is
    asked for (which is what the metric is for)."""
    tree, _ = _uneven_zone()
    metrics = _measured(tree, straighten_zones=False, socket_alignment="FULL")
    assert (metrics.zones, metrics.level_zones) == (1, 0)


def test_zones_are_straightened_without_link_priorities():
    tree, _ = _uneven_zone()
    metrics = _measured(tree, link_priority="none", socket_alignment="FULL")
    assert metrics.level_zones == 1


@pytest.mark.parametrize("seed", range(40))
@pytest.mark.parametrize("add_reroutes", [False, True])
def test_random_tree_with_zones(seed, add_reroutes):
    """Zones thrown at random trees, overlapping frames and each other any
    which way: every step still leaves the graph as it promises and no
    nodes overlap."""
    settings = Settings(add_reroutes=add_reroutes)
    tree = random_tree(seed, zones=3)
    result = sugiyama_layout(tree, settings, MARGIN, verify=True)

    moved = {edit.node for edit in result.edits if isinstance(edit, MoveNode)}
    removed = {edit.node for edit in result.edits if isinstance(edit, RemoveNode)}
    for node in tree.nodes:
        assert node.is_frame() or node in moved or node in removed
    assert node_overlaps(result) == 0
    # Frames and reroutes are still the tree's own afterwards.
    result.apply_to(tree)
    measure(tree)
