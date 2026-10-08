"""Benchmarks for building node trees through the nodebpy builder API."""

from functools import reduce
from itertools import product
from operator import and_

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import shader as s


def build_readme_tree(arrange="sugiyama") -> TreeBuilder:
    with g.tree("ReadmeTree", collapse=True, is_modifier=True, arrange=arrange) as tree:
        rot = (
            g.RandomValue.vector(min=-1, seed=2)
            >> g.AlignRotationToVector()
            >> g.RotateRotation(rotate_by=g.AxisAngleToRotation(angle=0.3))
        )
        pos = g.Position() * 2.0 + (0, 0.2, 0.3)

        (
            tree.inputs.integer("Count", 10)
            >> g.Points(position=g.RandomValue.vector(min=-1))
            >> g.InstanceOnPoints(instance=g.Cube(), rotation=rot)
            >> g.SetPosition(position=pos, offset=(0, 0, 0.1))
            >> g.RealizeInstances()
            >> g.InstanceOnPoints(g.Cube(), instance=...)
            >> tree.outputs.geometry("Instances")
        )
    return tree


def build_decoder(n_bits: int, arrange=None) -> TreeBuilder:
    with g.tree(f"{n_bits}-Bit Decoder", arrange=arrange) as tree:
        bits = [tree.inputs.boolean(f"Bit {i}") for i in range(n_bits)]
        not_bits = [g.BooleanMath.l_not(b) for b in bits]
        for i, combo in enumerate(product((False, True), repeat=n_bits)):
            terms = [b if on else nb for b, nb, on in zip(bits, not_bits, combo)]
            reduce(and_, terms) >> tree.outputs.boolean(f"Out {i}")
    return tree


def build_math_expression(arrange=None) -> TreeBuilder:
    with g.tree("MathExpression", arrange=arrange) as tree:
        x = tree.inputs.float("X", 1.0)
        y = tree.inputs.float("Y", 2.0)
        pos = g.Position().o.position
        value = x
        for i in range(20):
            value = (value * y + i) / (x + 1.0) - pos.z
        v = g.Position() * value + (0, 0, 1)
        g.SetPosition(offset=v) >> tree.outputs.geometry("Geometry")
    return tree


def build_shader_tree(arrange=None) -> TreeBuilder:
    with TreeBuilder.shader("BenchShader", arrange=arrange) as tree:
        coord = s.TextureCoordinate()
        noise = s.NoiseTexture(vector=coord.o.object, scale=5.0)
        ramp = s.ColorRamp(fac=noise.o.fac)
        mix = s.MixShader(
            fac=noise.o.fac,
            shader=s.PrincipledBSDF(base_color=ramp.o.color),
            shader_001=s.Emission(),
        )
        mix >> tree.outputs.shader("Shader")
    return tree


@pytest.mark.benchmark
def test_build_readme_tree_no_arrange():
    build_readme_tree(arrange=None)


@pytest.mark.benchmark
def test_build_readme_tree_sugiyama():
    build_readme_tree(arrange="sugiyama")


@pytest.mark.benchmark
def test_build_decoder_4bit():
    build_decoder(4)


@pytest.mark.benchmark
def test_build_math_expression():
    build_math_expression()


@pytest.mark.benchmark
def test_build_shader_tree():
    build_shader_tree()
