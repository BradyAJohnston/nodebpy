"""Layout edits kept across a rebuild: ``TreeBuilder(keep_edits=True)``,
``default_keep_edits`` and ``live.run_source``."""

import textwrap

import bpy
import pytest

from nodebpy import default_keep_edits
from nodebpy import geometry as g
from nodebpy.layout import keep
from nodebpy.layout.node_size import dimensions, top_offset
from nodebpy.live import run_source


def _build(scale=5.0, extra=False, **kwargs):
    with g.tree("Kept", clear=True, **kwargs) as tree:
        geo = tree.inputs.geometry("Geometry")
        offset = g.NoiseTexture(scale=scale).o.factor * 0.2
        if extra:
            offset = offset + g.Index() * 0.01
        geo >> g.SetPosition(offset=offset) >> tree.outputs.geometry("Geometry")
    return tree.tree


def _where(tree, name):
    location = tree.nodes[name].location_absolute
    return (round(location.x, 1), round(location.y, 1))


def _edit(tree):
    noise = tree.nodes["Noise Texture"]
    noise.location_absolute = (-900.0, 300.0)
    noise.hide = True
    noise.width = 220.0
    noise.use_custom_color = True
    noise.color = (0.5, 0.1, 0.1)
    tree.nodes["Set Position"].label = "Move"
    tree.nodes["Set Position"].inputs["Selection"].hide = True


def _box(node):
    x, y = node.location_absolute
    width, height = dimensions(node)
    top = y - top_offset(node)
    return (x, top - height, x + width, top)


def _overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def test_edits_survive_a_rebuild():
    tree = _build()
    _edit(tree)

    rebuilt = _build(scale=7.0, keep_edits=True)

    assert rebuilt == tree
    noise = tree.nodes["Noise Texture"]
    assert noise.inputs["Scale"].default_value == 7.0
    assert _where(tree, "Noise Texture") == (-900.0, 300.0)
    assert noise.hide
    assert noise.width == 220.0
    assert noise.use_custom_color
    assert tuple(noise.color) == pytest.approx((0.5, 0.1, 0.1))
    assert tree.nodes["Set Position"].label == "Move"
    assert tree.nodes["Set Position"].inputs["Selection"].hide


def test_edits_are_lost_without_keep_edits():
    tree = _build()
    arranged = _where(tree, "Noise Texture")
    _edit(tree)

    _build(scale=7.0)

    assert _where(tree, "Noise Texture") == arranged
    assert not tree.nodes["Noise Texture"].hide
    assert tree.nodes["Set Position"].label == ""


def test_untouched_tree_is_arranged_afresh():
    _build()
    tree = _build(extra=True, keep_edits=True)
    fresh = {n.name: _where(tree, n.name) for n in tree.nodes}

    bpy.data.node_groups.remove(tree)
    _build()
    tree = _build(extra=True, keep_edits=True)

    assert {n.name: _where(tree, n.name) for n in tree.nodes} == fresh


def test_unmatched_nodes_clear_the_kept_ones():
    tree = _build()
    _edit(tree)

    _build(extra=True, keep_edits=True)

    assert _where(tree, "Noise Texture") == (-900.0, 300.0)
    nodes = [n for n in tree.nodes if n.bl_idname != "NodeFrame"]
    assert {"Index", "Math.001", "Math.002"} <= {n.name for n in nodes}
    for new in ("Index", "Math.001", "Math.002"):
        node = tree.nodes[new]
        for other in nodes:
            if other != node:
                assert not _overlaps(_box(node), _box(other)), (new, other.name)


def test_user_frame_is_made_again():
    tree = _build()
    frame = tree.nodes.new("NodeFrame")
    frame.label = "Mine"
    frame.shrink = False
    frame.location_absolute = (-1000.0, 500.0)
    frame.width, frame.height = 400.0, 400.0
    tree.nodes["Noise Texture"].parent = frame
    tree.nodes["Noise Texture"].location_absolute = (-950.0, 400.0)

    _build(scale=2.0, keep_edits=True)

    (frame,) = [n for n in tree.nodes if n.bl_idname == "NodeFrame"]
    assert frame.label == "Mine"
    assert tree.nodes["Noise Texture"].parent == frame
    assert _where(tree, "Noise Texture") == (-950.0, 400.0)
    assert _where(tree, frame.name) == (-1000.0, 500.0)
    assert (frame.width, frame.height) == (400.0, 400.0)


def test_default_keep_edits_scope():
    tree = _build()
    _edit(tree)
    with default_keep_edits():
        _build(scale=3.0)
    assert _where(tree, "Noise Texture") == (-900.0, 300.0)


def test_matching_sees_through_reroutes():
    tree = _build()
    noise = tree.nodes["Noise Texture"]
    link = noise.outputs["Factor"].links[0]
    target = link.to_socket
    reroute = tree.nodes.new("NodeReroute")
    tree.links.new(noise.outputs["Factor"], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], target)

    _, before = keep._keys(tree)
    tree.nodes.remove(reroute)
    tree.links.new(noise.outputs["Factor"], target)
    _, after = keep._keys(tree)

    math = tree.nodes["Math"]
    assert before[math][1] == after[math][1]


SOURCE = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup

    class Kept(CustomGeometryGroup):
        _name = "Kept Group"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            offset = g.NoiseTexture(scale={scale}).o.factor * 0.2
            geo >> g.SetPosition(offset=offset) >> tree.outputs.geometry("Geometry")
    """
)


def test_run_source_keeps_edits_of_a_group_class():
    tree = run_source(SOURCE.format(scale=5.0)).tree
    assert tree is not None
    _edit(tree)

    rebuilt = run_source(SOURCE.format(scale=6.0)).tree

    assert rebuilt is not None and rebuilt.name == "Kept Group"
    assert rebuilt.nodes["Noise Texture"].inputs["Scale"].default_value == 6.0
    assert _where(rebuilt, "Noise Texture") == (-900.0, 300.0)
    assert rebuilt.nodes["Set Position"].label == "Move"


def test_run_source_keep_edits_off():
    tree = run_source(SOURCE.format(scale=5.0)).tree
    assert tree is not None
    arranged = _where(tree, "Noise Texture")
    _edit(tree)

    rebuilt = run_source(SOURCE.format(scale=6.0), keep_edits=False).tree

    assert rebuilt is not None
    assert _where(rebuilt, "Noise Texture") == arranged
