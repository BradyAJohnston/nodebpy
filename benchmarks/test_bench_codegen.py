"""Benchmarks for exporting node trees back to nodebpy Python source."""

import pytest

from nodebpy.export.codegen import to_python

from .test_bench_builder import (
    build_decoder,
    build_math_expression,
    build_readme_tree,
    build_shader_tree,
)

BUILDERS = {
    "readme": build_readme_tree,
    "decoder_4bit": lambda: build_decoder(4),
    "math_expression": build_math_expression,
    "shader": build_shader_tree,
}


@pytest.mark.parametrize("name", list(BUILDERS))
def test_to_python(benchmark, name):
    tree = BUILDERS[name]()
    code = benchmark(to_python, tree, format=False)
    assert "nodebpy" in code


def test_to_python_roundtrip(benchmark):
    code = to_python(build_readme_tree(), format=False)

    def run():
        exec(code, {})  # noqa: S102

    benchmark(run)
