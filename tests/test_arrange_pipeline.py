"""The layout as a pipeline of named steps with swappable strategies
(``nodebpy.lib.nodearrange.arrange.pipeline``)."""

import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.lib.nodearrange.arrange import pipeline as pipeline_module
from nodebpy.lib.nodearrange.arrange.graph import keep_frames_together
from nodebpy.lib.nodearrange.arrange.pipeline import (
    CHECKS,
    PHASES,
    Fact,
    InvariantError,
    Layout,
    Pipeline,
    PipelineError,
    Step,
    register,
    strategies,
    strategy,
    unregister,
)
from nodebpy.lib.nodearrange.arrange.ranking import compute_ranks, longest_path_ranks
from nodebpy.lib.nodearrange.arrange.sugiyama import default_pipeline, sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree
from nodebpy.lib.nodearrange.metrics import measure

from . import arrange_cases


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


def test_default_pipeline_steps():
    pipeline = default_pipeline()
    assert pipeline.names() == [
        "prioritize_links",
        "save_multi_input_orders",
        "remove_reroutes",
        "contract_stacks",
        "rank",
        "pin_interface_nodes",
        "balance_heights",
        "merge_edges",
        "insert_dummy_nodes",
        "add_columns",
        "order",
        "add_frame_borders",
        "place",
        "dissolve_dummy_nodes",
        "align_reroutes",
        "remove_frame_borders",
        "space_columns",
        "route",
        "expand_stacks",
        "realize",
    ]
    # The four phases appear in order, each once.
    assert tuple(step.phase for step in pipeline if step.phase) == PHASES
    assert pipeline["rank"].phase == "rank"
    assert pipeline["merge_edges"].phase is None


def test_steps_follow_the_settings():
    """Steps for optional features only run when the feature is on."""
    tree, _ = _fork()

    def ran(settings: Settings) -> list[str]:
        names = []
        sugiyama_layout(
            tree, settings, observer=lambda step, *_: names.append(step.name)
        )
        return names

    everything = default_pipeline().names()
    with_reroutes = ran(Settings(add_reroutes=True))
    assert with_reroutes == [n for n in everything if n != "dissolve_dummy_nodes"]

    plain = ran(
        Settings(add_reroutes=False, stack_collapsed=False, balance_heights=False)
    )
    skipped = {
        "remove_reroutes",
        "route",
        "contract_stacks",
        "expand_stacks",
        "balance_heights",
    }
    assert plain == [n for n in everything if n not in skipped]


def test_observer_sees_the_layout_and_timings():
    tree, _ = _fork()
    seen = {}

    def observer(step: Step, layout: Layout, seconds: float) -> None:
        assert seconds >= 0
        if step.name == "rank":
            seen["ranks"] = sorted(v.rank for v in layout.G)
        if step.name == "add_columns":
            seen["columns"] = len(layout.G.columns)
            assert layout.T is layout.CG.T
            assert layout.settings is layout.state.settings

    sugiyama_layout(tree, Settings(), observer=observer)
    assert seen == {"ranks": [0, 1, 1, 2], "columns": 3}


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


def test_registered_strategies():
    assert strategies("rank") == ["network_simplex", "longest_path"]
    assert strategies("order") == ["layer_sweep"]
    assert strategies("place") == ["brandes_koepf"]
    assert strategies("route") == ["bend_points"]
    assert strategy("rank", "longest_path") is not strategy("rank", "network_simplex")
    tree, _ = _fork()
    with pytest.raises(
        ValueError, match="unknown rank strategy 'nope'.*network_simplex"
    ):
        sugiyama_layout(tree, Settings(ranking="nope"))


def test_a_pipeline_follows_the_settings_it_is_run_with():
    """A pipeline is not tied to the settings it was built under: each phase
    looks its strategy up when it runs."""
    tree, _ = _fork()
    pipeline = default_pipeline()

    simplex = _columns(tree, Settings(ranking="network_simplex"), pipeline=pipeline)
    longest = _columns(tree, Settings(ranking="longest_path"), pipeline=pipeline)

    assert simplex["s"] == simplex["b"]
    assert longest["s"] == longest["c"]


def test_ranking_strategies_differ():
    """Network simplex keeps a side branch next to its source; longest path
    pushes it to the last column."""
    tree, _ = _fork()
    simplex = _columns(tree, Settings(ranking="network_simplex"))
    assert simplex["a"] < simplex["b"] < simplex["c"]
    assert simplex["s"] == simplex["b"]

    longest = _columns(tree, Settings(ranking="longest_path"))
    assert longest["a"] < longest["b"] < longest["c"]
    assert longest["s"] == longest["c"]


def test_ranking_option_on_the_public_api():
    ntree = arrange_cases.framed_stages()
    arrange_cases.reset_locations(ntree)
    arrange(ntree, SugiyamaOptions(ranking="longest_path"))
    metrics = measure(ntree)
    assert metrics.node_overlaps == 0
    assert metrics.backward_links == 0
    assert metrics.frame_overlaps == 0


def test_register_a_strategy(monkeypatch):
    """A new strategy is a decorated function, selected by name."""
    monkeypatch.setitem(
        pipeline_module._STRATEGIES, "rank", dict(pipeline_module._STRATEGIES["rank"])
    )
    calls = []

    @register("rank", "test_longest")
    def rank_test(layout: Layout) -> None:
        calls.append(len(layout.G))
        compute_ranks(layout.CG, longest_path_ranks)

    assert "test_longest" in strategies("rank")
    tree, _ = _fork()
    columns = _columns(tree, Settings(ranking="test_longest"))
    assert calls == [4]
    assert columns["s"] == columns["c"]


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
    pipeline = default_pipeline(settings)
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

    pipeline = default_pipeline(settings)
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


def test_pipeline_iterates_its_steps():
    steps = [Step("one", lambda L: None), Step("two", lambda L: None)]
    assert list(Pipeline(steps)) == steps


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
        Settings(add_reroutes=False),
        Settings(stack_collapsed=False, balance_heights=False, link_priority="none"),
    ):
        default_pipeline().check(settings)

    steps = {step.name: step for step in default_pipeline()}
    assert steps["rank"].provides == {Fact.RANKED}
    assert steps["order"].requires == {Fact.PROPER, Fact.COLUMNS}
    assert steps["order"].provides == {Fact.ORDERED}
    assert steps["place"].provides == {Fact.Y}
    assert Fact.BORDERS in steps["remove_frame_borders"].removes


@pytest.mark.parametrize(
    ("removed", "broken", "fact"),
    [
        ("rank", "pin_interface_nodes", "ranked"),
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
        sugiyama_layout(tree, Settings(add_reroutes=False), pipeline=pipeline)


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
    too_late.check(Settings(add_reroutes=False))
    with pytest.raises(PipelineError, match="one took away"):
        too_late.check(Settings(add_reroutes=True))


def test_verify_pins_a_broken_invariant_on_its_step(monkeypatch):
    """An ordering that ignores frames is caught right after it runs, not
    as a crash or a bad drawing several steps later."""
    monkeypatch.setitem(
        pipeline_module._STRATEGIES,
        "order",
        dict(pipeline_module._STRATEGIES["order"]),
    )

    @register("order", "by_name")
    def order_by_name(layout: Layout) -> None:
        for col in layout.G.columns:
            col.sort(key=lambda v: v.node.name if v.node else "")

    settings = Settings(ordering="by_name", add_reroutes=False)
    with pytest.raises(
        InvariantError,
        match=r"after step 'order' the graph is not ordered: Node\('e', NODE\) "
        r"sits between nodes of the frame bNode\('frame', NodeFrame\)",
    ):
        sugiyama_layout(_framed(), settings, verify=True)

    # The same strategy, mended with the helper for exactly this.
    @register("order", "by_name", replace=True)
    def order_by_name_in_frames(layout: Layout) -> None:
        for col in layout.G.columns:
            col.sort(key=lambda v: v.node.name if v.node else "")
            keep_frames_together(col)

    result = sugiyama_layout(_framed(), settings, verify=True)
    assert len(result.positions()) == 7


def test_verify_checks_every_fact_it_can():
    assert set(CHECKS) == {
        Fact.RANKED,
        Fact.PROPER,
        Fact.COLUMNS,
        Fact.ORDERED,
        Fact.Y,
        Fact.X,
    }

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


def test_keep_frames_together():
    tree = _framed()
    observed = {}

    def scramble(layout: Layout) -> None:
        col = max(layout.G.columns, key=len)
        col.sort(key=lambda v: v.node.name)
        observed["before"] = [v.node.name for v in col]
        keep_frames_together(col)
        observed["after"] = [v.node.name for v in col]

    pipeline = default_pipeline()
    pipeline.insert_after("add_columns", Step("scramble", scramble))
    sugiyama_layout(tree, Settings(add_reroutes=False), pipeline=pipeline)

    assert observed["before"] == ["b", "d", "e", "g"]
    assert observed["after"] == ["b", "d", "g", "e"]


def test_strategy_names_are_not_taken_silently(monkeypatch):
    monkeypatch.setitem(
        pipeline_module._STRATEGIES, "rank", dict(pipeline_module._STRATEGIES["rank"])
    )
    builtin = strategy("rank", "longest_path")

    with pytest.raises(ValueError, match="already is a rank strategy"):
        register("rank", "longest_path")(lambda layout: None)
    assert strategy("rank", "longest_path") is builtin

    register("rank", "mine")(builtin)
    assert "mine" in strategies("rank")
    unregister("rank", "mine")
    assert "mine" not in strategies("rank")


def test_steps_can_share_data_of_their_own():
    tree, _ = _fork()
    seen = []
    pipeline = default_pipeline()
    pipeline.insert_after(
        "rank",
        Step("count", lambda L: L.extra.__setitem__("ranks", {v.rank for v in L.G})),
    )
    pipeline.insert_after(
        "add_columns", Step("read", lambda L: seen.append(L.extra["ranks"]))
    )

    sugiyama_layout(tree, Settings(), pipeline=pipeline)

    assert seen == [{0, 1, 2}]


def test_strategy_options_on_the_public_api(monkeypatch):
    """Every phase's strategy can be chosen through ``SugiyamaOptions``,
    including one registered from outside."""
    monkeypatch.setitem(
        pipeline_module._STRATEGIES,
        "place",
        dict(pipeline_module._STRATEGIES["place"]),
    )
    calls = []

    @register("place", "logged")
    def place_logged(layout: Layout) -> None:
        calls.append(len(layout.G))
        strategy("place", "brandes_koepf")(layout)

    ntree = arrange_cases.diamond()
    arrange_cases.reset_locations(ntree)
    arrange(ntree, SugiyamaOptions(placement="logged"))

    assert len(calls) == 1
    assert measure(ntree).node_overlaps == 0
