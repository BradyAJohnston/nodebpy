"""The order phase (``nodebpy.layout.ordering``): crossings counted and
reduced."""

from itertools import combinations

import pytest

from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.ordering import (
    CROSSING_WEIGHTS,
    CrossingWeights,
    Lcg,
    _transpose,
    count_crossings,
)
from nodebpy.layout.pipeline import Layout, Step
from nodebpy.layout.sugiyama import sugiyama_layout

from .data import options, plain_node, positions, random_tree


def _value_nodes(tree: bNodeTree, names, **node_options) -> dict[str, bNode]:
    return {
        name: plain_node(tree, name, socket="NodeSocketFloat", **node_options)
        for name in names
    }


def _crossed() -> bNodeTree:
    """a and b in one column, c and d in the next, linked a -> d and
    b -> c. Sorted by name, the two links cross."""
    tree = bNodeTree()
    nodes = _value_nodes(tree, "abcd")
    for u, v in ("ad", "bc"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree


def _observed(tree: bNodeTree, step_name: str, observe) -> None:
    """Lay *tree* out as one graph, so that the step runs once, and call
    *observe* with the layout after the step called *step_name*."""

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name == step_name:
            observe(layout)

    sugiyama_layout(
        tree, options(pack_components=False), observer=observer, verify=True
    )


def _names(columns) -> list[list[str]]:
    return [[v.node.name if v.node else "" for v in col] for col in columns]


def test_ordering_uncrosses_links():
    seen = {}

    def observe(layout: Layout) -> None:
        columns = layout.G.columns
        seen["order"] = _names(columns)
        seen["crossings"] = count_crossings(layout.G, columns, CROSSING_WEIGHTS)

    _observed(_crossed(), "order", observe)

    first, second = seen["order"]
    assert seen["crossings"] == 0
    assert (first.index("a") < first.index("b")) == (
        second.index("d") < second.index("c")
    )


def test_count_crossings_counts_a_crossed_pair_once():
    counts = {}

    def observe(layout: Layout) -> None:
        columns = layout.G.columns
        assert _names(columns) == [["a", "b"], ["c", "d"]]
        counts["by name"] = count_crossings(layout.G, columns)
        columns[1].reverse()
        counts["uncrossed"] = count_crossings(layout.G, columns)
        columns[1].reverse()

    _observed(_crossed(), "add_columns", observe)
    assert counts == {"by name": 1, "uncrossed": 0}


def test_links_from_one_socket_do_not_cross():
    tree = bNodeTree()
    nodes = _value_nodes(tree, "abc", inputs=2)
    # Into the targets' sockets in the opposite order to the targets'.
    tree.add_link(nodes["a"].outputs[0], nodes["b"].inputs[1])
    tree.add_link(nodes["a"].outputs[0], nodes["c"].inputs[0])
    counts = []

    def observe(layout: Layout) -> None:
        columns = layout.G.columns
        counts.append(count_crossings(layout.G, columns))
        columns[1].reverse()
        counts.append(count_crossings(layout.G, columns))
        columns[1].reverse()

    _observed(tree, "add_columns", observe)
    assert counts == [0, 0]


def _crossing_pairs(layout: Layout) -> int:
    """Pairs of links into one column whose ends are in opposite orders at
    the two columns, going by node position and then socket index."""
    G, columns = layout.G, layout.G.columns
    column_of = {v: i for i, col in enumerate(columns) for v in col}
    position = {v: i for col in columns for i, v in enumerate(col)}
    ends: dict[int, list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    for link in G.all_links():
        ends.setdefault(column_of[link.tonode], []).append(
            (
                (position[link.fromnode], link.fromsock.idx),
                (position[link.tonode], link.tosock.idx),
            )
        )
    return sum(
        (a[0] < b[0] and a[1] > b[1]) or (a[0] > b[0] and a[1] < b[1])
        for links in ends.values()
        for a, b in combinations(links, 2)
    )


@pytest.mark.parametrize("seed", [1, 6, 9, 16, 23, 26])
def test_count_crossings_agrees_with_counting_pairs(seed):
    """Before the ordering, where these trees have crossings, and after."""
    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name in ("add_columns", "order"):
            fast = count_crossings(layout.G, layout.G.columns)
            seen[step.name] = (fast, _crossing_pairs(layout))

    tree = random_tree(seed)
    sugiyama_layout(tree, options(pack_components=False), observer=observer)

    before, after = seen["add_columns"], seen["order"]
    assert before[0] == before[1] > 0
    assert after[0] == after[1]


def _trade_off() -> bNodeTree:
    """p1 .. p4 in one column, each in a frame of its own so they keep
    their order, and x above y in the next. x takes a value from p1 and
    the geometry from p4; y takes values from p2 and p3. As they stand the
    flow link crosses both of y's; with x and y swapped the link from p1
    does instead."""
    tree = bNodeTree()
    nodes = _value_nodes(tree, ("p1", "p2", "p3", "p4"))
    nodes |= _value_nodes(tree, "xy", inputs=2)
    for name in ("p1", "p2", "p3", "p4"):
        nodes[name].parent = tree.add_node(bNode(f"frame {name}", "NodeFrame"))
    nodes["p4"].outputs[0].idname = "NodeSocketGeometry"
    for source, target, index in (
        ("p1", "x", 0),
        ("p4", "x", 1),
        ("p2", "y", 0),
        ("p3", "y", 1),
    ):
        tree.add_link(nodes[source].outputs[0], nodes[target].inputs[index])
    return tree


def test_transpose_prefers_value_crossings_over_flow_crossings():
    """Two crossings of a flow link with value links cost more than two
    crossings among value links, and the swap of neighbours goes by the
    cost: it is made under the default weights and not under even ones."""
    even = CrossingWeights(1.0, 1.0, 1.0)
    seen = {}

    def observe(layout: Layout) -> None:
        G, columns = layout.G, layout.G.columns
        assert [v.node.name for v in columns[1]] == ["x", "y"]
        seen["count"] = count_crossings(G, columns)
        seen["even"] = count_crossings(G, columns, even)
        seen["weighted"] = count_crossings(G, columns, CrossingWeights())
        seen["flow only"] = count_crossings(G, columns, CrossingWeights(1.0, 0.0, 0.0))
        seen["even swaps"] = _transpose(G, columns, even)
        seen["weighted swaps"] = _transpose(G, columns, CrossingWeights())
        seen["order"] = [v.node.name for v in columns[1]]
        seen["after"] = count_crossings(G, columns, CrossingWeights())

    _observed(_trade_off(), "add_columns", observe)
    assert seen == {
        "count": 2,
        "even": 2,
        "weighted": 2 * CrossingWeights().flow_value,
        "flow only": 0,
        "even swaps": False,
        "weighted swaps": True,
        "order": ["y", "x"],
        "after": 2,
    }


# ---------------------------------------------------------------------------
# Shuffled starting orders
# ---------------------------------------------------------------------------


def test_shuffles_come_from_a_portable_generator():
    """``Lcg`` is the generator of ``drand48``: from seed 0 its first state
    is 0x2BBB62DC5101, and these are its first outputs."""
    rng = Lcg(0)
    assert [rng.below(1000) for _ in range(5)] == [414, 240, 554, 841, 840]
    assert (0x2BBB62DC5101 >> 17) % 1000 == 414

    items = list(range(10))
    Lcg(0).shuffle(items)
    assert items == [9, 5, 6, 1, 3, 7, 0, 8, 2, 4]


@pytest.mark.parametrize("seed", [0, 1, 12345])
def test_same_seed_gives_the_same_layout(seed):
    assert positions(random_tree(16), seed=seed) == positions(
        random_tree(16), seed=seed
    )


def test_another_seed_can_give_another_order():
    """Random tree 16 is small enough for shuffled starts and has an order
    only some of them find."""
    assert positions(random_tree(16), seed=0) != positions(random_tree(16), seed=1)
