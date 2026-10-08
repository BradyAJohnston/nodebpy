"""Benchmarks for the automatic node layout (``arrange``)."""

import pytest

from nodebpy import arrange

from .test_bench_builder import build_decoder, build_math_expression, build_readme_tree


@pytest.mark.parametrize("method", ["sugiyama", "simple"])
def test_arrange_readme_tree(benchmark, method):
    tree = build_readme_tree(arrange=None)
    benchmark(arrange, tree.tree, method)


@pytest.mark.parametrize("method", ["sugiyama", "simple"])
def test_arrange_decoder_4bit(benchmark, method):
    tree = build_decoder(4)
    benchmark(arrange, tree.tree, method)


def test_arrange_math_expression(benchmark):
    tree = build_math_expression()
    benchmark(arrange, tree.tree, "sugiyama")
