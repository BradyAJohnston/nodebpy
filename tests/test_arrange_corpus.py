"""The layout against the stored corpus (``tests/arrange_corpus/``): node
trees serialised with tree_clipper, with where every node must end up."""

import pytest

from nodebpy.layout import arrange_node_tree
from nodebpy.layout.config import Settings
from nodebpy.layout.edits import ResizeFrame
from nodebpy.layout.extract import extract
from nodebpy.layout.sugiyama import sugiyama_layout

from . import arrange_cases, arrange_corpus
from .arrange_metrics import measure

pytest.importorskip("tree_clipper")

CASES = dict(arrange_corpus.cases())
LAYOUTS = list(arrange_corpus.SETTINGS)


def _assert_close(actual, expected, path="layout"):
    """Equal, but for floats, which may differ in their last digits."""
    if isinstance(expected, float) or isinstance(actual, float):
        assert actual == pytest.approx(expected, abs=0.01), path
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), path
        for i, (a, e) in enumerate(zip(actual, expected)):
            _assert_close(a, e, f"{path}[{i}]")
    else:
        assert actual == expected, path


def test_corpus_is_there():
    """Every hand-built case is stored, each file under the settings it
    says it was laid out with."""
    assert set(arrange_cases.CASES) <= set(CASES)
    for name, case in CASES.items():
        expected = arrange_corpus.LAYOUTS_OF.get(name, arrange_corpus.SETTINGS)
        assert set(case["layouts"]) == set(expected)
        assert case["tree"].startswith("TreeClipper::")
        for layout, stored in case["layouts"].items():
            assert stored["settings"] == arrange_corpus.SETTINGS[layout]


@pytest.mark.parametrize("name", ["zones", "nested_frames", "annotated"])
def test_tree_survives_the_corpus_format(name):
    """A tree read back from its Tree Clipper string has the same nodes,
    frames and links."""
    tree = arrange_cases.CASES[name]()
    before = arrange_corpus.layout_of(tree)

    again = arrange_corpus.tree_from_payload(arrange_corpus.tree_to_payload(tree))

    assert arrange_corpus.layout_of(again) == before


@pytest.mark.parametrize("name", CASES)
def test_layout_matches_the_corpus(name):
    """Each stored tree still gets its stored layout under each of the
    settings, and none overlaps nodes. If the change is intended:
    ``python -m tests.arrange_corpus --update``."""
    case = CASES[name]

    for layout, tree in arrange_corpus.arranged(case["tree"], case["layouts"]):
        stored = case["layouts"][layout]
        actual = arrange_corpus.layout_of(tree)
        assert actual["links"] == stored["links"], layout
        _assert_close(actual["nodes"], stored["nodes"], layout)
        assert measure(tree).node_overlaps == 0, layout


@pytest.mark.parametrize("name", ["chain", "diamond", "framed_stages", "zones"])
def test_measuring_plain_data_agrees_with_measuring_blender(name):
    """``apply_to`` + ``measure`` on plain data gives what arranging the
    Blender tree and measuring that gives."""
    settings = Settings(**arrange_corpus.SETTINGS["default"])
    ntree = arrange_cases.CASES[name]()
    arrange_cases.reset_locations(ntree)

    tree = extract(ntree)[0]
    sugiyama_layout(tree, settings, arrange_corpus.MARGIN).apply_to(tree)
    pure = measure(tree)

    arrange_node_tree(ntree, settings, arrange_corpus.MARGIN)
    blender = measure(ntree)

    assert pure.as_dict(ndigits=1) == blender.as_dict(ndigits=1)


def test_applying_edits_to_plain_data_with_reroutes():
    """With reroutes, a result removes and adds nodes and links; applied to
    the plain tree it leaves a sound layout. A frame that does not fit
    itself to its members gets an edit of its own, which is a no-op on
    plain data (a frame's box is derived from its members there)."""
    ntree = arrange_cases.annotated()
    arrange_cases.reset_locations(ntree)
    tree = extract(ntree)[0]
    frame = next(node for node in tree.nodes if node.is_frame())
    frame.shrink = False
    reroutes_before = sum(node.is_reroute() for node in tree.nodes)

    settings = Settings(**arrange_corpus.SETTINGS["reroutes"])
    result = sugiyama_layout(tree, settings, arrange_corpus.MARGIN)
    result.apply_to(tree)

    assert any(isinstance(edit, ResizeFrame) for edit in result.edits)
    assert sum(node.is_reroute() for node in tree.nodes) != reroutes_before
    metrics = measure(tree)
    assert metrics.node_overlaps == 0
    assert metrics.links == sum(link.is_valid for link in tree.links)
