"""The layout as a list of named steps (``nodebpy.layout.pipeline``)."""

import pytest

from nodebpy.layout.config import SugiyamaOptions
from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.model import keep_frames_together
from nodebpy.layout.pipeline import (
    PHASES,
    Fact,
    InvariantError,
    Layout,
    PipelineError,
    Step,
)
from nodebpy.layout.ranking import compute_ranks, longest_path_ranks
from nodebpy.layout.sugiyama import default_pipeline, sugiyama_layout

from .data import MARGIN, options, plain_node, positions


def _fork() -> tuple[bNodeTree, dict[str, bNode]]:
    """a -> b -> c, and a -> s."""
    tree = bNodeTree()
    nodes = {name: plain_node(tree, name, socket="NodeSocketFloat") for name in "abcs"}
    for u, v in ("ab", "bc", "as"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree, nodes


def _framed() -> bNodeTree:
    """a -> b, c -> d, f -> e and f -> g, with b, d and g in a frame: by
    name, the unframed e sits between nodes of the frame."""
    tree = bNodeTree()
    frame = tree.add_node(bNode("frame", "NodeFrame", label="F"))
    nodes = {
        name: plain_node(tree, name, socket="NodeSocketFloat") for name in "abcdefg"
    }
    for name in "bdg":
        nodes[name].parent = frame
    for u, v in ("ab", "cd", "fe", "fg"):
        tree.add_link(nodes[u].outputs[0], nodes[v].inputs[0])
    return tree


def test_default_pipeline_has_the_four_phases_in_order():
    pipeline = default_pipeline()
    assert tuple(step.phase for step in pipeline if step.phase) == PHASES
    assert pipeline["rank"].phase == "rank"
    assert pipeline["merge_edges"].phase is None


@pytest.mark.parametrize(
    "fields",
    [
        {},
        {"reroutes": "blocked"},
        {"reroutes": "all"},
        {"stack_collapsed": False, "balance_heights": False, "straighten_trunk": False},
    ],
    ids=["default", "blocked", "all", "plain"],
)
def test_default_pipeline_passes_its_own_check(fields):
    default_pipeline().check(SugiyamaOptions(**fields))


def test_observer_is_called_after_a_step_with_the_layout():
    tree, _ = _fork()
    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        assert seconds >= 0
        if step.name == "rank":
            seen["ranks"] = sorted(v.rank for v in layout.G)
        if step.name == "add_columns":
            seen["columns"] = len(layout.G.columns)

    sugiyama_layout(tree, observer=observer)
    assert seen == {"ranks": [0, 1, 1, 2], "columns": 3}


# ---------------------------------------------------------------------------
# Editing a pipeline
# ---------------------------------------------------------------------------


def test_inserted_steps_run_in_their_place_unless_disabled():
    tree, _ = _fork()
    reference = positions(tree)

    log = []
    pipeline = default_pipeline()
    pipeline.insert_before("rank", Step("before_rank", lambda L: log.append("before")))
    pipeline.insert_after("rank", Step("after_rank", lambda L: log.append("after")))
    pipeline.insert_after(
        "after_rank",
        Step("never", lambda L: log.append("never"), enabled=lambda options: False),
    )

    start = pipeline.index("before_rank")
    assert pipeline.names()[start : start + 4] == [
        "before_rank",
        "rank",
        "after_rank",
        "never",
    ]
    assert positions(tree, pipeline=pipeline) == reference
    assert log == ["before", "after"]


def test_replaced_step_keeps_its_name_and_phase_and_runs_the_new_function():
    """With the placement replaced by one that piles each column from zero,
    the columns stay where they were and the two nodes sharing a column are
    a node's height and the margin apart."""
    tree, _ = _fork()
    reference = positions(tree)

    def place_from_zero(layout: Layout) -> None:
        for column in layout.G.columns:
            y = 0.0
            for v in column:
                v.y = y
                y -= v.height + layout.state.margin.y

    pipeline = default_pipeline()
    pipeline.replace("place", place_from_zero)
    assert pipeline["place"].phase == "place"

    piled = positions(tree, pipeline=pipeline)
    assert piled["a"][1] == piled["c"][1]
    assert {x for x, _ in piled.values()} == {x for x, _ in reference.values()}
    assert abs(piled["b"][1] - piled["s"][1]) == pytest.approx(100.0 + MARGIN[1])


def test_removed_step_is_gone_and_an_unknown_name_is_an_error():
    pipeline = default_pipeline()
    pipeline.remove("balance_heights")
    assert "balance_heights" not in pipeline.names()
    with pytest.raises(KeyError, match="no step named 'nope'"):
        pipeline.remove("nope")


# ---------------------------------------------------------------------------
# What steps require of each other
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("removed", "broken", "fact"),
    [
        ("rank", "move_feeders_right", "ranked"),
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
        sugiyama_layout(tree, SugiyamaOptions(reroutes="none"), pipeline=pipeline)


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
    sugiyama_layout(tree, SugiyamaOptions(), pipeline=late)
    assert seen == [3]

    # After the routing the columns are gone again.
    too_late = default_pipeline()
    too_late.insert_after("route", needs_columns)
    too_late.check(SugiyamaOptions(reroutes="none"))
    with pytest.raises(PipelineError, match="one took away"):
        too_late.check(SugiyamaOptions(reroutes="all"))


def test_replacing_a_phase():
    """Another algorithm for a phase goes in with ``replace``: ranking every
    node as far right as it can go puts the side branch of a fork beside
    the end of the chain instead of beside its middle."""
    tree, _ = _fork()
    simplex = positions(tree)

    pipeline = default_pipeline()
    pipeline.replace("rank", lambda L: compute_ranks(L.CG, longest_path_ranks))
    longest = positions(tree, pipeline=pipeline)

    assert simplex["s"][0] == simplex["b"][0]
    assert longest["s"][0] == longest["c"][0]


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
        sugiyama_layout(_framed(), options(), pipeline=pipeline, verify=True)

    # The same ordering, mended with the helper for exactly this.
    def order_by_name_in_frames(layout: Layout) -> None:
        order_by_name(layout)
        for col in layout.G.columns:
            keep_frames_together(col)

    pipeline.replace("order", order_by_name_in_frames)
    result = sugiyama_layout(_framed(), options(), pipeline=pipeline, verify=True)
    assert len(result.positions()) == 7


def _spoil_rank(layout: Layout) -> None:
    next(iter(layout.G)).rank += 10


def _spoil_column(layout: Layout) -> None:
    v = next(iter(layout.G))
    v.col = list(v.col)


def _spoil_y(layout: Layout) -> None:
    next(iter(layout.G)).y = None


@pytest.mark.parametrize(
    ("spoil", "after", "message"),
    [
        (_spoil_rank, "rank", "not ranked"),
        (_spoil_column, "add_columns", "not columns: .*col is not the column"),
        (_spoil_y, "place", "not y: .* has no y"),
    ],
    ids=["rank", "column", "y"],
)
def test_verify_names_the_step_that_spoiled_a_fact(spoil, after, message):
    pipeline = default_pipeline()
    pipeline.insert_after(after, Step("spoil", spoil))
    with pytest.raises(InvariantError, match=f"after step 'spoil' .*{message}"):
        sugiyama_layout(_framed(), options(), pipeline=pipeline, verify=True)
