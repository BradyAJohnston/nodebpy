"""The layout on random trees and on trees built to break it: cycles, very
long chains, stacks feeding multi-inputs. Plain data, no Blender."""

import itertools
import random
import sys

import pytest

from nodebpy.layout import ordering
from nodebpy.layout.build import cycle_links
from nodebpy.layout.dna import bNodeTree, new_reroute
from nodebpy.layout.edits import MoveNode, RemoveNode
from nodebpy.layout.stacking import deterministic_hopcroft_karp_matching
from nodebpy.layout.sugiyama import sugiyama_layout

from .data import (
    collapsed_math,
    laid_out,
    node_overlaps,
    options,
    plain_chain,
    plain_node,
    positions,
    random_tree,
)

# ---------------------------------------------------------------------------
# Random trees
# ---------------------------------------------------------------------------

# Options far from the defaults, to reach more of the routing.
_OTHER = {"reroutes": "all", "direction": "LEFT_UP", "socket_alignment": "MODERATE"}


def _placed(result) -> list[tuple[str, tuple[float, float]]]:
    return [(e.node.name, e.top_left) for e in result.edits if isinstance(e, MoveNode)]


@pytest.mark.parametrize("seed", range(30))
@pytest.mark.parametrize(
    ("fields", "zones"),
    [
        ({}, 0),
        ({"reroutes": "all"}, 0),
        ({"reroutes": "blocked"}, 0),
        (_OTHER, 0),
        ({}, 3),
        (_OTHER, 3),
    ],
    ids=["default", "reroutes", "blocked", "other", "zones", "other-zones"],
)
def test_random_tree_is_placed_without_overlaps_the_same_every_time(
    seed, fields, zones
):
    """Every step leaves the graph as it promises, every node is placed or
    removed, no nodes overlap, and a second run gives the same positions.
    The zones are random pairs of nodes, which may overlap frames and each
    other as Blender's cannot."""
    tree = random_tree(seed, zones)

    result = sugiyama_layout(tree, options(**fields), verify=True)

    moved = {edit.node for edit in result.edits if isinstance(edit, MoveNode)}
    removed = {edit.node for edit in result.edits if isinstance(edit, RemoveNode)}
    for node in tree.nodes:
        assert node.is_frame() or node in moved or node in removed
    assert node_overlaps(result) == 0

    again = sugiyama_layout(random_tree(seed, zones), options(**fields))
    assert _placed(result) == _placed(again)


@pytest.mark.parametrize("seed", range(30))
def test_packing_parts_puts_no_more_frames_on_each_other(seed):
    """Laying the unlinked parts out apart leaves no more frames overlapping,
    or nodes on frames they are not in, than laying the tree out as one
    graph."""

    def frame_defects(**fields) -> int:
        metrics = laid_out(random_tree(seed), reroutes="all", **fields)
        return metrics.frame_overlaps + metrics.foreign_nodes_in_frames

    assert frame_defects() <= frame_defects(pack_components=False)


# ---------------------------------------------------------------------------
# Cycles
# ---------------------------------------------------------------------------


def _ring(size: int) -> bNodeTree:
    tree = bNodeTree()
    nodes = [plain_node(tree, f"n{i}") for i in range(size)]
    for i, node in enumerate(nodes):
        tree.add_link(node.outputs[0], nodes[(i + 1) % size].inputs[0])
    return tree


@pytest.mark.parametrize(
    ("size", "reroutes"), [(1, "none"), (2, "all"), (3, "none"), (6, "all")]
)
def test_cycle_is_laid_out_as_a_chain(size, reroutes):
    """A tree with a cycle is laid out without the link that closes it."""
    tree = _ring(size)

    assert [link.fromnode.name for link in cycle_links(tree)] == [f"n{size - 1}"]
    at = positions(tree, reroutes=reroutes)

    xs = [at[f"n{i}"][0] for i in range(size)]
    assert xs == sorted(xs) and len(set(xs)) == size


def test_only_the_closing_links_of_cycles_are_ignored():
    tree = bNodeTree()
    a, b, c, d = (plain_node(tree, name, inputs=2, outputs=2) for name in "abcd")
    forward = [
        tree.add_link(a.outputs[0], b.inputs[0]),
        tree.add_link(b.outputs[0], c.inputs[0]),
        tree.add_link(a.outputs[1], c.inputs[1]),
        tree.add_link(c.outputs[0], d.inputs[0]),
    ]
    back = {
        tree.add_link(c.outputs[1], a.inputs[0]),
        tree.add_link(d.outputs[0], b.inputs[1]),
    }

    assert cycle_links(tree) == back
    assert not cycle_links(tree) & set(forward)

    # Marked invalid, as Blender marks the link closing a cycle, they are
    # still the ones left out.
    for link in back:
        link.is_valid = False
    assert cycle_links(tree) == back

    # An invalid link that closes no cycle is kept: Blender also calls a
    # link between sockets that do not fit invalid, and still draws it.
    forward[2].is_valid = False
    assert cycle_links(tree) == back


# ---------------------------------------------------------------------------
# Size
# ---------------------------------------------------------------------------


def test_very_long_chain():
    """Nothing recurses once per node: a chain far longer than Python's
    recursion limit lays out as one row."""
    tree = bNodeTree()
    plain_chain(tree, [f"n{i:04}" for i in range(1500)])

    at = positions(tree, socket_alignment="NONE")

    assert len({y for _, y in at.values()}) == 1
    assert len({x for x, _ in at.values()}) == 1500


def test_very_tall_column():
    """Placing a column does not recurse once per node either: a column
    taller than the recursion limit (lowered here, to keep the test quick)
    lays out without overlaps."""
    tree = bNodeTree()
    join = plain_node(tree, "join", multi_input=True)
    for i in range(400):
        source = plain_node(tree, f"s{i:04}", height=40.0)
        tree.add_link(source.outputs[0], join.inputs[0], i)

    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(300)
    try:
        result = sugiyama_layout(tree, options(balance_heights=False))
    finally:
        sys.setrecursionlimit(limit)

    assert node_overlaps(result) == 0


# ---------------------------------------------------------------------------
# Stacks of collapsed Math nodes
# ---------------------------------------------------------------------------


def test_long_chain_of_collapsed_math_nodes_is_one_stack():
    tree = bNodeTree()
    nodes = [collapsed_math(tree, f"m{i:04}") for i in range(1200)]
    for a, b in itertools.pairwise(nodes):
        tree.add_link(a.outputs[0], b.inputs[0])

    at = positions(tree)

    assert len({x for x, _ in at.values()}) == 1
    assert len({y for _, y in at.values()}) == 1200


@pytest.mark.parametrize("reroutes", ["none", "all"])
def test_stack_feeding_a_multi_input_is_placed_before_it(reroutes):
    """m0 -> m1 is a stack. m0 also feeds ``other`` and the multi-input of
    ``join``, which m1 feeds too."""
    tree = bNodeTree()
    m0, m1 = collapsed_math(tree, "m0"), collapsed_math(tree, "m1")
    join = plain_node(tree, "join", multi_input=True)
    other = plain_node(tree, "other", inputs=3)
    tree.add_link(m0.outputs[0], m1.inputs[0])
    tree.add_link(m0.outputs[0], other.inputs[0])
    tree.add_link(m0.outputs[0], join.inputs[0], 0)
    tree.add_link(m1.outputs[0], join.inputs[0], 1)

    at = positions(tree, reroutes=reroutes)

    assert at["m0"][0] == at["m1"][0] < at["join"][0]


def test_stack_feeding_a_multi_input_through_a_labelled_reroute():
    """As above, with the link from m0 to ``join`` passing a reroute the
    layout keeps."""
    tree = bNodeTree()
    m0, m1 = collapsed_math(tree, "m0"), collapsed_math(tree, "m1")
    join = plain_node(tree, "join", multi_input=True)
    other = plain_node(tree, "other")
    reroute = tree.add_node(new_reroute())
    reroute.name, reroute.label = "kept", "kept"
    tree.add_link(m0.outputs[0], m1.inputs[0])
    tree.add_link(m0.outputs[0], other.inputs[0])
    tree.add_link(m0.outputs[0], reroute.inputs[0])
    tree.add_link(reroute.outputs[0], join.inputs[0], 0)
    tree.add_link(m1.outputs[0], join.inputs[0], 1)

    at = positions(tree)

    assert at["m0"][0] < at["kept"][0] < at["join"][0]


def test_matching_reassigns_an_earlier_pair():
    """The matching behind the stacks finds the larger matching even when
    that means taking back a pair it made first."""
    graph = {"a": ["x", "y"], "b": ["x"], "c": ["x"]}

    matching = deterministic_hopcroft_karp_matching(graph, "abc", "xy")

    assert matching == {"a": "y", "b": "x", "x": "b", "y": "a"}


# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------


def test_layout_does_not_touch_the_random_module():
    tree = random_tree(5)
    random.seed(1234)
    expected = random.random()

    random.seed(1234)
    sugiyama_layout(tree, options())

    assert random.random() == expected


def test_layout_empties_its_caches():
    sugiyama_layout(random_tree(7), options())

    for cached in (
        ordering.reflexive_transitive_closure,
        ordering.topologically_sorted_clusters,
        ordering.non_cluster_descendant,
    ):
        assert cached.cache_info().currsize == 0
