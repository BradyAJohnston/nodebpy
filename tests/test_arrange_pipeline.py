"""The layout as a pipeline of named steps with swappable strategies
(``nodebpy.lib.nodearrange.arrange.pipeline``)."""

import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.lib.nodearrange.arrange import pipeline as pipeline_module
from nodebpy.lib.nodearrange.arrange.pipeline import (
    PHASES,
    Layout,
    Pipeline,
    Step,
    register,
    strategies,
    strategy,
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
        "save_multi_input_orders",
        "remove_reroutes",
        "contract_stacks",
        "rank",
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
    assert default_pipeline()["rank"].run is strategy("rank", "network_simplex")
    assert default_pipeline(Settings(ranking="longest_path"))["rank"].run is strategy(
        "rank", "longest_path"
    )
    with pytest.raises(
        ValueError, match="unknown rank strategy 'nope'.*network_simplex"
    ):
        default_pipeline(Settings(ranking="nope"))


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
    assert pipeline.names()[3:7] == ["before_rank", "rank", "after_rank", "never"]
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
