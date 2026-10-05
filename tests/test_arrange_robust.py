"""The layout copes with whatever tree it is given: cycles, very long
chains, stacks feeding multi-inputs, random trees — and leaves no trace in
the process it runs in."""

import itertools
import random
import sys

import pytest

from nodebpy.lib.nodearrange.arrange import ordering
from nodebpy.lib.nodearrange.arrange.sugiyama import cycle_links, sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNodeTree

from .arrange_data import MARGIN, node_overlaps, plain_node, random_tree


def _positions(tree, **settings):
    result = sugiyama_layout(tree, Settings(**settings), MARGIN)
    return {node.name: xy for node, xy in result.positions().items()}


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
    ("size", "add_reroutes"), [(1, False), (2, True), (3, False), (6, True)]
)
def test_cycle_is_laid_out_as_a_chain(size, add_reroutes):
    """A tree with a cycle is laid out without the link that closes it."""
    tree = _ring(size)

    assert [link.fromnode.name for link in cycle_links(tree)] == [f"n{size - 1}"]
    positions = _positions(tree, reroutes="all" if add_reroutes else "none")

    xs = [positions[f"n{i}"][0] for i in range(size)]
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


def test_linked_socket_without_a_location_is_reported():
    tree = bNodeTree()
    a, b = plain_node(tree, "a"), plain_node(tree, "b")
    tree.add_link(a.outputs[0], b.inputs[0])
    b.inputs[0].location = None

    with pytest.raises(ValueError, match=r"'b'.*input 0 has no location"):
        sugiyama_layout(tree, Settings(), MARGIN)


# ---------------------------------------------------------------------------
# Size
# ---------------------------------------------------------------------------


def test_very_long_chain():
    """Nothing recurses once per node: a chain far longer than Python's
    recursion limit lays out as one row."""
    tree = bNodeTree()
    nodes = [plain_node(tree, f"n{i:04}") for i in range(1500)]
    for a, b in itertools.pairwise(nodes):
        tree.add_link(a.outputs[0], b.inputs[0])

    positions = _positions(tree, socket_alignment="NONE")

    assert len({y for _, y in positions.values()}) == 1
    assert len({x for x, _ in positions.values()}) == 1500


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
        result = sugiyama_layout(tree, Settings(balance_heights=False), MARGIN)
    finally:
        sys.setrecursionlimit(limit)

    assert node_overlaps(result) == 0


def test_long_stack_of_collapsed_math_nodes():
    tree = bNodeTree()
    nodes = [
        plain_node(
            tree,
            f"m{i:04}",
            idname="ShaderNodeMath",
            socket="NodeSocketFloat",
            collapsed=True,
            height=30.0,
            inputs=2,
        )
        for i in range(1200)
    ]
    for a, b in itertools.pairwise(nodes):
        tree.add_link(a.outputs[0], b.inputs[0])

    positions = _positions(tree)

    assert len({x for x, _ in positions.values()}) == 1


# ---------------------------------------------------------------------------
# Stacks and multi-inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("add_reroutes", [False, True])
def test_stack_feeding_a_multi_input(add_reroutes):
    """A stack takes over its nodes' sockets; the saved order of the links
    into a multi-input has to follow."""
    tree = bNodeTree()
    math = [
        plain_node(
            tree,
            name,
            idname="ShaderNodeMath",
            socket="NodeSocketFloat",
            collapsed=True,
            height=30.0,
            inputs=2,
        )
        for name in ("m0", "m1")
    ]
    join = plain_node(tree, "join", multi_input=True)
    other = plain_node(tree, "other", inputs=3)
    tree.add_link(math[0].outputs[0], math[1].inputs[0])
    # One output of the stack with two outside links, one into the multi-input.
    tree.add_link(math[0].outputs[0], other.inputs[0])
    tree.add_link(math[0].outputs[0], join.inputs[0], 0)
    tree.add_link(math[1].outputs[0], join.inputs[0], 1)

    positions = _positions(tree, reroutes="all" if add_reroutes else "none")

    assert positions["m0"][0] == positions["m1"][0] < positions["join"][0]


# ---------------------------------------------------------------------------
# No trace left behind
# ---------------------------------------------------------------------------


def test_layout_leaves_the_random_state_alone():
    tree = random_tree(5)
    random.seed(1234)
    expected = random.random()

    random.seed(1234)
    sugiyama_layout(tree, Settings(), MARGIN)

    assert random.random() == expected


def test_layout_keeps_no_graphs_alive():
    sugiyama_layout(random_tree(7), Settings(), MARGIN)

    for cached in (
        ordering.reflexive_transitive_closure,
        ordering.topologically_sorted_clusters,
        ordering.non_cluster_descendant,
    ):
        assert cached.cache_info().currsize == 0


def test_stack_feeding_a_multi_input_through_a_kept_reroute():
    """The same, when the link from the stack passes a reroute the layout
    keeps (it has a label)."""
    from nodebpy.lib.nodearrange.dna import new_reroute

    tree = bNodeTree()
    math = [
        plain_node(
            tree,
            name,
            idname="ShaderNodeMath",
            socket="NodeSocketFloat",
            collapsed=True,
            height=30.0,
            inputs=2,
        )
        for name in ("m0", "m1")
    ]
    join = plain_node(tree, "join", multi_input=True)
    other = plain_node(tree, "other")
    reroute = tree.add_node(new_reroute())
    reroute.name, reroute.label = "kept", "kept"
    tree.add_link(math[0].outputs[0], math[1].inputs[0])
    tree.add_link(math[0].outputs[0], other.inputs[0])
    tree.add_link(math[0].outputs[0], reroute.inputs[0])
    tree.add_link(reroute.outputs[0], join.inputs[0], 0)
    tree.add_link(math[1].outputs[0], join.inputs[0], 1)

    positions = _positions(tree)

    assert positions["m0"][0] < positions["kept"][0] < positions["join"][0]


def test_matching_reassigns_an_earlier_pair():
    """The matching behind the stacks finds the larger matching even when
    that means taking back a pair it made first."""
    from nodebpy.lib.nodearrange.arrange.stacking import (
        deterministic_hopcroft_karp_matching,
    )

    graph = {"a": ["x", "y"], "b": ["x"], "c": ["x"]}

    matching = deterministic_hopcroft_karp_matching(graph, "abc", "xy")

    assert matching == {"a": "y", "b": "x", "x": "b", "y": "a"}


@pytest.mark.parametrize("seed", [3, 7, 11, 19])
def test_ranking_keeps_its_cut_values_right(seed, monkeypatch):
    """The network simplex only updates the cut values an exchange changes.
    After every exchange they are what computing all of them afresh gives."""
    from nodebpy.lib.nodearrange.arrange import ranking

    from .arrange_data import random_tree

    exchange = ranking.exchange
    exchanges = []

    def checked(H, T, parents, leave, enter):
        parents = exchange(H, T, parents, leave, enter)
        kept = {link.ident: link.cut_value for link in T.all_links()}
        ranking.get_adj_edges_T.cache_clear()
        ranking.compute_cut_values(H, T)
        ranking.get_adj_edges_T.cache_clear()
        assert kept == {link.ident: link.cut_value for link in T.all_links()}
        exchanges.append(leave)
        return parents

    monkeypatch.setattr(ranking, "exchange", checked)
    sugiyama_layout(random_tree(seed), Settings(reroutes="all"), MARGIN, verify=True)
    assert exchanges
