"""Zones in the layout: which nodes are in a zone (``nodearrange.zones``),
and the layout keeping a zone's nodes together with no other among them
(``sugiyama.cluster_zones``)."""

from itertools import pairwise

import pytest

from nodebpy.lib.nodearrange.arrange.edits import MoveNode, RemoveNode
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
# The layout
# ---------------------------------------------------------------------------


def _zone_with_feeder() -> bNodeTree:
    """[i -> tall -> o], and a feeder of ``tall`` from outside the zone,
    which has a feeder of its own and so sits in the column of ``i``: under
    ``i``, beside ``tall``, in the box around the zone."""
    tree = bNodeTree()
    nodes = _chain(tree, "ito")
    tall = nodes["t"]
    tall.draw_bounds = (0.0, -400.0, 140.0, 0.0)
    source = plain_node(tree, "source", socket="NodeSocketFloat")
    feeder = plain_node(tree, "feeder", socket="NodeSocketFloat")
    tree.add_link(source.outputs[0], feeder.inputs[0])
    tree.add_link(feeder.outputs[0], tall.inputs[1])
    tree.zones = find_zones(tree, [(nodes["i"], nodes["o"])])
    return tree


def _foreign_nodes(tree: bNodeTree, **settings) -> int:
    result = sugiyama_layout(tree, Settings(**settings), MARGIN, verify=True)
    assert node_overlaps(result) == 0
    result.apply_to(tree)
    return measure(tree).foreign_nodes_in_zones


@pytest.mark.parametrize("add_reroutes", [False, True])
def test_other_nodes_are_kept_out_of_a_zone(add_reroutes):
    assert _foreign_nodes(_zone_with_feeder(), add_reroutes=add_reroutes) == 0


def test_zones_can_be_left_alone():
    """Without the grouping the feeder sits in the zone's box (which is
    what the metric is for)."""
    assert _foreign_nodes(_zone_with_feeder(), group_zones=False) == 1


def _clusters(tree: bNodeTree) -> dict[str, list[str]]:
    """For each node, what its clusters stand for, innermost first."""
    seen = {}

    def observer(step, layout, seconds):
        if step.name != "rank":
            return
        for v in layout.G:
            if v.node is None:
                continue
            around = []
            c = v.cluster
            while c is not None and not c.is_root:
                around.append(c.node.name if c.node is not None else "zone")
                c = c.cluster
            seen[v.node.name] = around

    result = sugiyama_layout(tree, Settings(), MARGIN, observer=observer, verify=True)
    assert node_overlaps(result) == 0
    return seen


def test_zone_inside_a_frame_and_frame_inside_a_zone():
    tree = bNodeTree()
    outer = tree.add_node(bNode("outer", "NodeFrame"))
    inner = tree.add_node(bNode("inner", "NodeFrame"))
    nodes = _chain(tree, "aixyob")
    for name in "aixyo":
        nodes[name].parent = outer
    for name in "xy":
        nodes[name].parent = inner
    inner.parent = outer
    tree.zones = find_zones(tree, [(nodes["i"], nodes["o"])])

    assert _clusters(tree) == {
        "a": ["outer"],
        "i": ["zone", "outer"],
        "x": ["inner", "zone", "outer"],
        "y": ["inner", "zone", "outer"],
        "o": ["zone", "outer"],
        "b": [],
    }
    # The nodes go back into their frames, not into anything of the zone's.
    result = sugiyama_layout(tree, Settings(), MARGIN)
    parents = {e.node.name: e.parent for e in result.edits if isinstance(e, MoveNode)}
    assert parents["i"] is outer and parents["x"] is inner and parents["b"] is None


def test_zone_that_only_overlaps_a_frame_is_not_grouped():
    """A frame around the zone's input node and a node before the zone can
    be nested neither in the zone nor around it."""
    tree = bNodeTree()
    frame = tree.add_node(bNode("frame", "NodeFrame"))
    nodes = _chain(tree, "aixob")
    nodes["a"].parent = nodes["i"].parent = frame
    tree.zones = find_zones(tree, [(nodes["i"], nodes["o"])])
    assert all("zone" not in around for around in _clusters(tree).values())


def test_zone_that_is_all_of_its_frame_adds_nothing():
    tree = bNodeTree()
    frame = tree.add_node(bNode("frame", "NodeFrame"))
    nodes = _chain(tree, "aixob")
    for name in "ixo":
        nodes[name].parent = frame
    tree.zones = find_zones(tree, [(nodes["i"], nodes["o"])])
    assert _clusters(tree)["x"] == ["frame"]


def test_nested_zones_are_nested_clusters():
    tree = bNodeTree()
    nodes = _chain(tree, "aixjypzob")
    tree.zones = find_zones(tree, [(nodes["j"], nodes["p"]), (nodes["i"], nodes["o"])])
    clusters = _clusters(tree)
    assert clusters["y"] == ["zone", "zone"]
    assert clusters["x"] == ["zone"]
    assert clusters["a"] == []


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
