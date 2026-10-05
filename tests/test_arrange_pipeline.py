"""The layout as a pipeline of named steps
(``nodebpy.lib.nodearrange.arrange.pipeline``), and the ordering phase."""

import pytest

from nodebpy.lib.nodearrange.arrange.graph import keep_frames_together
from nodebpy.lib.nodearrange.arrange.ordering import CROSSING_WEIGHTS, CrossingWeights
from nodebpy.lib.nodearrange.arrange.pipeline import (
    PHASES,
    Fact,
    InvariantError,
    Layout,
    PipelineError,
    Step,
)
from nodebpy.lib.nodearrange.arrange.ranking import compute_ranks, longest_path_ranks
from nodebpy.lib.nodearrange.arrange.sugiyama import default_pipeline, sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree


def _node(tree: bNodeTree, name: str) -> bNode:
    node = tree.add_node(
        bNode(
            name, "GeometryNodeSetPosition", width=140.0, draw_bounds=(0, -100, 140, 0)
        )
    )
    node.add_socket(True, location=(140.0, -30.0))
    node.add_socket(False, location=(0.0, -52.0))
    return node


def _fork() -> tuple[bNodeTree, dict[str, bNode]]:
    """a -> b -> c, and a -> s."""
    tree = bNodeTree()
    nodes = {name: _node(tree, name) for name in "abcs"}
    for u, v in ("ab", "bc", "as"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree, nodes


def _columns(tree: bNodeTree, settings: Settings, **kwargs) -> dict[str, float]:
    positions = sugiyama_layout(tree, settings, **kwargs).positions()
    return {node.name: x for node, (x, _) in positions.items()}


# ---------------------------------------------------------------------------
# The default pipeline
# ---------------------------------------------------------------------------


def test_default_pipeline_has_the_four_phases_in_order():
    pipeline = default_pipeline()
    assert tuple(step.phase for step in pipeline if step.phase) == PHASES
    assert pipeline["rank"].phase == "rank"
    assert pipeline["merge_edges"].phase is None


def test_observer_sees_the_layout_and_timings():
    tree, _ = _fork()
    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        assert seconds >= 0
        if step.name == "rank":
            seen["ranks"] = sorted(v.rank for v in layout.G)
        if step.name == "add_columns":
            seen["columns"] = len(layout.G.columns)

    sugiyama_layout(tree, Settings(), observer=observer)
    assert seen == {"ranks": [0, 1, 1, 2], "columns": 3}


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Editing a pipeline
# ---------------------------------------------------------------------------


def test_custom_pipeline_steps():
    """Steps can be replaced, inserted and removed; the layout runs the
    pipeline it is given."""
    tree, nodes = _fork()
    settings = Settings(balance_heights=False)
    reference = sugiyama_layout(tree, settings).positions()

    log = []
    pipeline = default_pipeline()
    pipeline.insert_before("rank", Step("before_rank", lambda L: log.append("before")))
    pipeline.insert_after("rank", Step("after_rank", lambda L: log.append("after")))
    pipeline.insert_after(
        "after_rank",
        Step("never", lambda L: log.append("never"), enabled=lambda s: False),
    )
    start = pipeline.index("before_rank")
    assert pipeline.names()[start : start + 4] == [
        "before_rank",
        "rank",
        "after_rank",
        "never",
    ]
    assert sugiyama_layout(tree, settings, pipeline=pipeline).positions() == reference
    assert log == ["before", "after"]

    # Replace the placement: stack each column from zero, no alignment.
    def place_stacked(layout: Layout) -> None:
        for column in layout.G.columns:
            y = 0.0
            for v in column:
                v.y = y
                y -= v.height + layout.state.margin.y

    pipeline = default_pipeline()
    pipeline.replace("place", place_stacked)
    assert pipeline["place"].phase == "place"
    stacked = sugiyama_layout(tree, settings, pipeline=pipeline).positions()
    assert stacked[nodes["a"]][1] == stacked[nodes["c"]][1]
    assert {x for x, _ in stacked.values()} == {x for x, _ in reference.values()}
    in_one_column = sorted(stacked[nodes[n]][1] for n in "bs")
    assert in_one_column[1] - in_one_column[0] == pytest.approx(100.0 + 20.0)

    pipeline.remove("balance_heights")
    assert "balance_heights" not in pipeline.names()
    with pytest.raises(KeyError, match="no step named 'nope'"):
        pipeline.index("nope")


# ---------------------------------------------------------------------------
# Contracts between steps
# ---------------------------------------------------------------------------


def _framed() -> bNodeTree:
    """Two parallel chains, a -> b and c -> d, with b and d in a frame and
    an unframed node e between them by name."""
    tree = bNodeTree()
    frame = tree.add_node(bNode("frame", "NodeFrame", label="F"))
    nodes = {name: _node(tree, name) for name in "abcdefg"}
    for name in "bdg":
        nodes[name].parent = frame
    for u, v in ("ab", "cd", "fe", "fg"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree


def test_default_pipeline_fits_together():
    for settings in (
        Settings(),
        Settings(reroutes="none"),
        Settings(stack_collapsed=False, balance_heights=False, straighten_trunk=False),
    ):
        default_pipeline().check(settings)


@pytest.mark.parametrize(
    ("removed", "broken", "fact"),
    [
        ("rank", "balance_heights", "ranked"),
        ("insert_dummy_nodes", "order", "proper"),
        ("add_columns", "order", "columns"),
        ("add_frame_borders", "place", "borders"),
        ("space_columns", "expand_stacks", "x"),
    ],
)
def test_pipeline_missing_a_step_is_refused(removed, broken, fact):
    """Taking out a step others depend on is reported before anything runs,
    naming the step that would have failed and what it lacks."""
    pipeline = default_pipeline()
    pipeline.remove(removed)
    tree, _ = _fork()

    with pytest.raises(PipelineError, match=rf"step '{broken}' requires .*{fact}"):
        sugiyama_layout(tree, Settings(reroutes="none"), pipeline=pipeline)


def test_step_with_requirements_must_come_late_enough():
    seen = []
    needs_columns = Step(
        "count_columns",
        lambda L: seen.append(len(L.G.columns)),
        requires=frozenset({Fact.COLUMNS}),
    )
    tree, _ = _fork()

    early = default_pipeline()
    early.insert_before("rank", needs_columns)
    with pytest.raises(PipelineError, match="'count_columns' requires .*columns"):
        early.check()

    late = default_pipeline()
    late.insert_after("add_columns", needs_columns)
    sugiyama_layout(tree, Settings(), pipeline=late)
    assert seen == [3]

    # After the routing the columns are gone again.
    too_late = default_pipeline()
    too_late.insert_after("route", needs_columns)
    too_late.check(Settings(reroutes="none"))
    with pytest.raises(PipelineError, match="one took away"):
        too_late.check(Settings(reroutes="all"))


def test_replacing_a_phase():
    """Another algorithm for a phase goes in with ``replace``: ranking every
    node as far right as it can go puts the side branch of a fork beside
    the end of the chain instead of beside its middle."""
    tree, _ = _fork()
    simplex = _columns(tree, Settings())

    pipeline = default_pipeline()
    pipeline.replace("rank", lambda L: compute_ranks(L.CG, longest_path_ranks))
    longest = _columns(tree, Settings(), pipeline=pipeline)

    assert simplex["s"] == simplex["b"]
    assert longest["s"] == longest["c"]


def test_verify_pins_a_broken_invariant_on_its_step():
    """An ordering that ignores frames is caught right after it runs, not
    as a crash or a bad drawing several steps later."""

    def order_by_name(layout: Layout) -> None:
        for col in layout.G.columns:
            col.sort(key=lambda v: v.node.name if v.node else "")

    pipeline = default_pipeline()
    pipeline.replace("order", order_by_name)
    with pytest.raises(
        InvariantError,
        match=r"after step 'order' the graph is not ordered: Node\('e', NODE\) "
        r"sits between nodes of the frame bNode\('frame', NodeFrame\)",
    ):
        sugiyama_layout(_framed(), Settings(), pipeline=pipeline, verify=True)

    # The same ordering, mended with the helper for exactly this.
    def order_by_name_in_frames(layout: Layout) -> None:
        order_by_name(layout)
        for col in layout.G.columns:
            keep_frames_together(col)

    pipeline.replace("order", order_by_name_in_frames)
    result = sugiyama_layout(_framed(), Settings(), pipeline=pipeline, verify=True)
    assert len(result.positions()) == 7


def test_verify_checks_every_fact_it_can():
    def spoil(what):
        def run(layout: Layout) -> None:
            v = next(iter(layout.G))
            if what == "rank":
                v.rank += 10
            elif what == "column":
                v.col = list(v.col)
            elif what == "y":
                v.y = None

        return run

    for what, after, message in (
        ("rank", "rank", "not ranked"),
        ("column", "add_columns", "not columns: .*col is not the column"),
        ("y", "place", "not y: .* has no y"),
    ):
        pipeline = default_pipeline()
        pipeline.insert_after(after, Step("spoil", spoil(what)))
        with pytest.raises(InvariantError, match=f"after step 'spoil' .*{message}"):
            sugiyama_layout(_framed(), Settings(), pipeline=pipeline, verify=True)


# ---------------------------------------------------------------------------
# Ordering
# ---------------------------------------------------------------------------


def _crossed() -> bNodeTree:
    """a and b in one column, c and d in the next, linked crosswise by
    name: a -> d and b -> c. Sorted by name, the two links cross."""
    tree = bNodeTree()
    nodes = {name: _node(tree, name) for name in "abcd"}
    for u, v in ("ad", "bc"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree


def _order_and_crossings(tree: bNodeTree, **settings) -> tuple[list[list[str]], int]:
    from nodebpy.lib.nodearrange.arrange.ordering import count_crossings

    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name in ("add_columns", "order"):
            columns = layout.G.columns
            seen[step.name] = (
                [[v.node.name if v.node else "" for v in col] for col in columns],
                count_crossings(layout.G, columns, CROSSING_WEIGHTS),
            )

    # (As one graph: the parts of these trees are not linked.)
    settings = {"pack_components": False, **settings}
    sugiyama_layout(tree, Settings(**settings), observer=observer, verify=True)
    assert seen["add_columns"][1] >= seen["order"][1]
    return seen["order"]


def test_ordering_uncrosses_links():
    order, crossings = _order_and_crossings(_crossed())
    assert crossings == 0
    assert [order[0].index("a") < order[0].index("b")] == [
        order[1].index("d") < order[1].index("c")
    ]


def test_count_crossings():
    from nodebpy.lib.nodearrange.arrange.ordering import count_crossings

    counts = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name == "add_columns":
            columns = layout.G.columns
            counts["by name"] = count_crossings(layout.G, columns)
            columns[1].reverse()
            counts["uncrossed"] = count_crossings(layout.G, columns)
            columns[1].reverse()

    sugiyama_layout(_crossed(), Settings(pack_components=False), observer=observer)
    assert counts == {"by name": 1, "uncrossed": 0}

    # Links fanning out of one socket never cross each other.
    tree = bNodeTree()
    nodes = {name: _node(tree, name) for name in "abc"}
    for target in "bc":
        tree.add_link(nodes["a"].outputs[0], nodes[target].inputs[0])
    assert _order_and_crossings(tree)[1] == 0


def _trade_off() -> bNodeTree:
    """p1 .. p4 in one column, each in a frame of its own so they keep
    their order, and x above y in the next. x takes a value from p1 and
    the geometry from p4; y takes values from p2 and p3. As they stand the
    geometry link crosses both of y's; with x and y swapped the link from
    p1 does instead."""
    tree = bNodeTree()
    nodes = {name: _node(tree, name) for name in ("p1", "p2", "p3", "p4", "x", "y")}
    for name in ("p1", "p2", "p3", "p4"):
        nodes[name].parent = tree.add_node(bNode(f"frame {name}", "NodeFrame"))
        nodes[name].outputs[0].idname = "NodeSocketFloat"
    nodes["p4"].outputs[0].idname = "NodeSocketGeometry"
    for name in ("x", "y"):
        nodes[name].add_socket(False, location=(0.0, -74.0))
    for source, target, index in (
        ("p1", "x", 0),
        ("p4", "x", 1),
        ("p2", "y", 0),
        ("p3", "y", 1),
    ):
        tree.add_link(nodes[source].outputs[0], nodes[target].inputs[index])
    return tree


def test_crossings_weighed_by_what_links_carry():
    """A value crossing the main data costs more than two values crossing,
    and swapping neighbours goes by the cost."""
    from nodebpy.lib.nodearrange.arrange.ordering import _transpose, count_crossings

    even = CrossingWeights(1.0, 1.0, 1.0)
    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        if step.name != "add_columns":
            return
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

    sugiyama_layout(
        _trade_off(),
        Settings(pack_components=False),
        observer=observer,
        verify=True,
    )
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


def test_shuffles_come_from_a_portable_generator():
    """The generator behind the shuffled starting orders is drand48's, so a
    port produces the same numbers: these are its first outputs."""
    from nodebpy.lib.nodearrange.arrange.ordering import _Lcg

    rng = _Lcg(0)
    state = 0x330E
    expected = []
    for _ in range(5):
        state = (state * 0x5DEECE66D + 0xB) % 2**48
        expected.append((state >> 17) % 1000)
    assert [rng.below(1000) for _ in range(5)] == expected
    # drand48 from seed 0: the first state is 0x2BBB62DC5101.
    assert expected[0] == (0x2BBB62DC5101 >> 17) % 1000

    items = list(range(10))
    _Lcg(0).shuffle(items)
    again = list(range(10))
    _Lcg(0).shuffle(again)
    assert items == again != list(range(10))
    assert sorted(items) == list(range(10))
