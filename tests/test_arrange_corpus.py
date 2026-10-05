"""The layout against the stored corpus (``tests/arrange_corpus/``): trees
as plain data with the layout each must get. Nothing here needs Blender
except the test that compares the two ways of measuring a layout."""

import json

import pytest

from nodebpy.lib.nodearrange import arrange_node_tree
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.extract import extract
from nodebpy.lib.nodearrange.metrics import measure
from nodebpy.lib.nodearrange.serialize import (
    result_from_json,
    result_to_json,
    settings_from_json,
    settings_to_json,
    tree_from_json,
    tree_to_json,
)

from . import arrange_cases, arrange_corpus

CASES = dict(arrange_corpus.cases())
LAYOUTS = list(arrange_corpus.SETTINGS)


def _assert_close(actual, expected, path="result"):
    """Equal, but for floats, which may differ in their last digits."""
    if isinstance(expected, float) or isinstance(actual, float):
        assert actual == pytest.approx(expected, abs=1e-3), path
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), path
        for i, (a, e) in enumerate(zip(actual, expected)):
            _assert_close(a, e, f"{path}[{i}]")
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys(), path
        for key in expected:
            _assert_close(actual[key], expected[key], f"{path}.{key}")
    else:
        assert actual == expected, path


def test_corpus_is_there():
    assert len(CASES) >= 25
    assert all(set(case["layouts"]) == set(LAYOUTS) for case in CASES.values())


@pytest.mark.parametrize("layout", LAYOUTS)
@pytest.mark.parametrize("name", CASES)
def test_layout_matches_the_corpus(name, layout):
    """The layout of each stored tree is still the stored one. If the change
    is intended: ``python -m tests.arrange_corpus --update``."""
    case = CASES[name]
    tree = tree_from_json(case["tree"])
    settings = settings_from_json(case["layouts"][layout]["settings"])

    result = sugiyama_layout(tree, settings, tuple(case["margin"]))

    _assert_close(
        arrange_corpus._round(result_to_json(tree, result)),
        case["layouts"][layout]["result"],
    )


@pytest.mark.parametrize("name", CASES)
def test_json_round_trip(name):
    case = CASES[name]
    tree = tree_from_json(case["tree"])
    assert tree_to_json(tree) == case["tree"]
    # Survives being written out and read back.
    assert json.loads(json.dumps(case["tree"])) == case["tree"]

    for stored in case["layouts"].values():
        tree = tree_from_json(case["tree"])
        result = result_from_json(tree, stored["result"])
        assert result_to_json(tree, result) == stored["result"]
        settings = settings_from_json(stored["settings"])
        assert settings_to_json(settings) == stored["settings"]


def test_unknown_formats_are_refused():
    with pytest.raises(ValueError, match="unsupported tree format"):
        tree_from_json({"format": 99, "nodes": [], "links": []})
    tree = tree_from_json({"format": 1, "nodes": [], "links": []})
    with pytest.raises(ValueError, match="unsupported result format"):
        result_from_json(tree, {"format": 99, "edits": []})
    with pytest.raises(ValueError, match="unknown edit"):
        result_from_json(tree, {"format": 1, "edits": [["explode", 0]]})


@pytest.mark.parametrize("layout", LAYOUTS)
@pytest.mark.parametrize("name", CASES)
def test_stored_layout_is_sound(name, layout):
    """Applied to the plain tree, a stored layout overlaps no nodes."""
    tree, _, result = arrange_corpus.load(CASES[name], layout)
    links_before = sum(link.is_valid for link in tree.links)

    result.apply_to(tree)
    metrics = measure(tree)

    assert metrics.node_overlaps == 0
    if layout != "reroutes":
        # Without reroutes the layout only moves nodes (existing reroutes
        # without a label are still taken out).
        assert metrics.links <= links_before


@pytest.mark.parametrize("name", ["chain", "diamond", "framed_stages", "zones"])
def test_measuring_plain_data_agrees_with_measuring_blender(name):
    """``apply_to`` + ``measure`` on plain data gives what arranging the
    Blender tree and measuring that gives."""
    settings = arrange_corpus.SETTINGS["default"]
    ntree = arrange_cases.CASES[name]()
    arrange_cases.reset_locations(ntree)

    tree = extract(ntree)[0]
    sugiyama_layout(tree, settings, arrange_corpus.MARGIN).apply_to(tree)
    pure = measure(tree)

    arrange_node_tree(ntree, settings, arrange_corpus.MARGIN)
    blender = measure(ntree)

    assert pure.as_dict(ndigits=1) == blender.as_dict(ndigits=1)


def test_main_data_metrics():
    """A chain's trunk is level throughout, and a diamond's forks are
    symmetric."""
    for name in ("chain", "diamond"):
        tree, _, result = arrange_corpus.load(CASES[name], "default")
        result.apply_to(tree)
        metrics = measure(tree)
        assert metrics.flow_links > 0
        if name == "chain":
            assert metrics.level_flow_links == metrics.flow_links
        assert metrics.fork_imbalance == pytest.approx(0.0, abs=1.0)

    # Without the bias the diamond's forks are lopsided, and that costs.
    tree, _, result = arrange_corpus.load(CASES["diamond"], "plain")
    result.apply_to(tree)
    plain = measure(tree)
    assert plain.fork_imbalance > 100
    assert plain.cost() > metrics.cost()


def test_frame_that_does_not_shrink_round_trips():
    """A frame that does not fit itself to its members gets a
    ``resize_frame`` edit, which survives the JSON format and is a no-op on
    plain data (a frame's box is derived from its members there)."""
    data = CASES["framed_stages"]["tree"]
    tree = tree_from_json(data)
    frame = next(node for node in tree.nodes if node.is_frame())
    frame.shrink = False
    settings = arrange_corpus.SETTINGS["default"]

    result = sugiyama_layout(tree, settings, arrange_corpus.MARGIN)
    stored = result_to_json(tree, result)

    assert [edit for edit in stored["edits"] if edit[0] == "resize_frame"]
    again = result_from_json(tree, stored)
    assert result_to_json(tree, again) == stored
    assert tree_from_json(tree_to_json(tree)).nodes[tree.nodes.index(frame)].shrink is (
        False
    )
    again.apply_to(tree)
    assert measure(tree).node_overlaps == 0
