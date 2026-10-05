"""The layout against the stored corpus (``tests/layout/corpus/``): node
trees serialised with tree_clipper, with where every node must end up."""

import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.layout.extract import extract
from nodebpy.layout.sugiyama import sugiyama_layout

from . import cases, corpus
from .metrics import measure

pytest.importorskip("tree_clipper")

CASES = dict(corpus.cases())


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


def test_every_case_is_stored_under_the_current_options():
    assert set(cases.CASES) <= set(CASES)
    for name, case in CASES.items():
        expected = corpus.LAYOUTS_OF.get(name, corpus.SETTINGS)
        assert set(case["layouts"]) == set(expected)
        assert case["tree"].startswith("TreeClipper::")
        for layout, stored in case["layouts"].items():
            assert stored["settings"] == corpus.SETTINGS[layout]


@pytest.mark.parametrize("name", ["zones", "nested_frames", "annotated"])
def test_tree_survives_the_corpus_format(name):
    """A tree read back from its Tree Clipper string has the same nodes,
    frames and links."""
    tree = cases.CASES[name]()
    before = corpus.layout_of(tree)

    again = corpus.tree_from_payload(corpus.tree_to_payload(tree))

    assert corpus.layout_of(again) == before


@pytest.mark.parametrize("name", CASES)
def test_layout_matches_the_corpus(name):
    """Each stored tree still gets its stored layout under each set of
    options, and none overlaps nodes. If the change is intended:
    ``python -m tests.layout.corpus --update``."""
    case = CASES[name]

    for layout, tree in corpus.arranged(case["tree"], case["layouts"]):
        stored = case["layouts"][layout]
        actual = corpus.layout_of(tree)
        assert actual["links"] == stored["links"], layout
        _assert_close(actual["nodes"], stored["nodes"], layout)
        assert measure(tree).node_overlaps == 0, layout


@pytest.mark.parametrize("name", ["framed_stages", "zones"])
def test_measuring_plain_data_agrees_with_measuring_blender(name):
    """``apply_to`` and ``measure`` on plain data give what arranging the
    Blender tree and measuring that gives."""
    options = SugiyamaOptions(margin=corpus.MARGIN)
    ntree = cases.CASES[name]()
    cases.reset_locations(ntree)

    tree = extract(ntree)[0]
    sugiyama_layout(tree, options).apply_to(tree)
    plain = measure(tree)

    arrange(ntree, options)
    blender = measure(ntree)

    assert plain.as_dict() == blender.as_dict()
