"""The layout as a pure function: plain data in, edits out.

``sugiyama_layout`` takes a ``dna.bNodeTree`` (a plain-data copy of a Blender
tree) and returns the edits that realise the layout. ``extract`` builds that
copy from a Blender tree and ``apply`` carries the edits out. The middle
stage must never touch ``bpy`` — it is the part to be ported to C++.
"""

import ast
import random
from itertools import pairwise
from pathlib import Path

import bpy
import pytest
from mathutils.geometry import intersect_line_line_2d

from nodebpy.lib import nodearrange
from nodebpy.lib.nodearrange import arrange_node_tree
from nodebpy.lib.nodearrange.apply import apply
from nodebpy.lib.nodearrange.arrange.common import f32, group_by, segments_intersect
from nodebpy.lib.nodearrange.arrange.edits import (
    AddLink,
    AddReroute,
    LayoutResult,
    MoveNode,
    RemoveLink,
    RemoveNode,
    ResizeFrame,
    RestoreMultiInputOrder,
)
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import (
    REROUTE_SIZE,
    bNode,
    bNodeTree,
    new_reroute,
)
from nodebpy.lib.nodearrange.extract import extract

from . import arrange_cases

_PACKAGE = Path(nodearrange.__file__).parent


# ---------------------------------------------------------------------------
# The layout stage is pure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module",
    sorted(
        [
            *(_PACKAGE / "arrange").glob("*.py"),
            _PACKAGE / "dna.py",
            _PACKAGE / "config.py",
            _PACKAGE / "metrics.py",
        ]
    ),
    ids=lambda path: path.name,
)
def test_layout_modules_do_not_import_blender(module):
    """The layout, its input structs, its settings and the metrics import
    neither ``bpy`` nor ``mathutils``, nor the modules of
    this package that do."""
    blender_side = {"bpy", "mathutils", "blf", "utils", "extract", "apply", "structs"}
    imported = set()
    for node in ast.walk(ast.parse(module.read_text())):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
            imported.update(alias.name for alias in node.names)
    if module.name == "metrics.py":
        # `measure` reads a Blender tree into plain data when given one.
        imported.discard("extract")
    assert not imported & blender_side


def _node(
    tree: bNodeTree,
    name: str,
    *,
    inputs: int = 1,
    outputs: int = 1,
    height: float = 100.0,
    parent: bNode | None = None,
) -> bNode:
    """A 140-wide node at the origin, sockets 22 apart below a 30 header."""
    node = tree.add_node(
        bNode(
            name,
            "GeometryNodeSetPosition",
            width=140.0,
            draw_bounds=(0.0, -height, 140.0, 0.0),
            parent=parent,
        )
    )
    for k in range(outputs):
        node.add_socket(True, location=(140.0, -30.0 - 22.0 * k))
    for k in range(inputs):
        node.add_socket(False, location=(0.0, -30.0 - 22.0 * (outputs + k)))
    return node


def test_layout_of_a_hand_built_tree():
    """A tree built from plain data lays out without any Blender object: a
    chain becomes one row, left to right, a margin apart."""
    tree = bNodeTree()
    a, b, c = (_node(tree, name) for name in "abc")
    tree.add_link(a.outputs[0], b.inputs[0])
    tree.add_link(b.outputs[0], c.inputs[0])

    result = sugiyama_layout(tree, Settings(socket_alignment="NONE"), (50.0, 20.0))

    assert all(isinstance(edit, MoveNode) for edit in result.edits)
    positions = result.positions()
    assert positions[a][0] < positions[b][0] < positions[c][0]
    assert positions[b][0] - positions[a][0] == pytest.approx(140.0 + 50.0)
    assert positions[a][1] == positions[b][1] == positions[c][1]
    # Centred on where the nodes were.
    assert positions[b][0] == pytest.approx(0.0)
    # The input is untouched.
    assert a.location == (0.0, 0.0)
    assert len(tree.links) == 2


def test_empty_tree_needs_no_edits():
    assert sugiyama_layout(bNodeTree()).edits == []
    only_frame = bNodeTree()
    only_frame.add_node(bNode("Frame", "NodeFrame"))
    assert sugiyama_layout(only_frame).edits == []


def test_layout_keeps_nodes_in_their_frames():
    tree = bNodeTree()
    frame = tree.add_node(bNode("Frame", "NodeFrame", label="Stage"))
    a = _node(tree, "a")
    b = _node(tree, "b", parent=frame)
    c = _node(tree, "c", parent=frame)
    tree.add_link(a.outputs[0], b.inputs[0])
    tree.add_link(b.outputs[0], c.inputs[0])

    result = sugiyama_layout(tree)
    parents = {e.node: e.parent for e in result.edits if isinstance(e, MoveNode)}
    assert parents == {a: None, b: frame, c: frame}


def test_long_link_gets_reroutes():
    """With reroutes on, a link skipping columns is replaced by a chain of
    reroutes: the edits create them, link them up, and place them."""
    tree = bNodeTree()
    nodes = [_node(tree, name, inputs=2) for name in "abcd"]
    for u, v in pairwise(nodes):
        tree.add_link(u.outputs[0], v.inputs[0])
    tree.add_link(nodes[0].outputs[0], nodes[3].inputs[1])

    plain = sugiyama_layout(tree, Settings(add_reroutes=False))
    assert {type(e) for e in plain.edits} == {MoveNode}

    result = sugiyama_layout(tree, Settings(add_reroutes=True))
    reroutes = [e.node for e in result.edits if isinstance(e, AddReroute)]
    assert reroutes
    assert all(node.is_reroute() and node.parent is None for node in reroutes)
    links = [e for e in result.edits if isinstance(e, AddLink)]
    # The chain: a -> reroute ... reroute -> d, input 1.
    assert links[0].fromsock is nodes[0].outputs[0]
    assert links[-1].tosock is nodes[3].inputs[1]
    assert {e.tosock.node for e in links[:-1]} == set(reroutes)
    assert set(reroutes) <= set(result.positions())
    # Edits come in an applicable order: a reroute exists before it is linked.
    created = result.edits.index(
        next(e for e in result.edits if isinstance(e, AddReroute))
    )
    assert created < result.edits.index(links[0])


def test_existing_reroute_is_replaced():
    """A reroute on a short link is dissolved: the edits remove it and link
    its ends directly."""
    tree = bNodeTree()
    a, b = _node(tree, "a"), _node(tree, "b")
    reroute = tree.add_node(new_reroute())
    reroute.name = "Reroute"
    tree.add_link(a.outputs[0], reroute.inputs[0])
    tree.add_link(reroute.outputs[0], b.inputs[0])

    result = sugiyama_layout(tree, Settings(add_reroutes=True))
    assert RemoveNode(reroute) in result.edits
    assert AddLink(a.outputs[0], b.inputs[0]) in result.edits
    assert reroute not in result.positions()

    labelled = bNodeTree()
    a, b = _node(labelled, "a"), _node(labelled, "b")
    kept = labelled.add_node(new_reroute())
    kept.label = "keep me"
    labelled.add_link(a.outputs[0], kept.inputs[0])
    labelled.add_link(kept.outputs[0], b.inputs[0])
    result = sugiyama_layout(labelled, Settings(add_reroutes=True))
    assert not any(isinstance(e, RemoveNode) for e in result.edits)
    assert kept in result.positions()


def test_new_reroute_shape():
    reroute = new_reroute()
    assert reroute.is_reroute() and not reroute.is_frame()
    assert (len(reroute.inputs), len(reroute.outputs)) == (1, 1)
    assert reroute.width == REROUTE_SIZE
    assert reroute.top - reroute.bottom == REROUTE_SIZE
    assert reroute.outputs[0].is_output and reroute.outputs[0].node is reroute
    assert "NodeReroute" in repr(reroute)


# ---------------------------------------------------------------------------
# extract and apply
# ---------------------------------------------------------------------------


def test_extract_copies_what_the_layout_reads():
    ntree = arrange_cases.nested_frames()
    math = next(n for n in ntree.nodes if n.bl_idname == "ShaderNodeMath")
    math.location = (120.0, -40.0)
    tree, binding = extract(ntree)

    assert [n.name for n in tree.nodes] == [n.name for n in ntree.nodes]
    assert len(tree.links) == len(ntree.links)
    by_name = {n.name: n for n in tree.nodes}

    outer, inner = by_name["Frame"], by_name["Frame.001"]
    assert outer.is_frame() and outer.label == "Outer"
    assert inner.parent is outer and outer.parent is None
    assert outer.shrink

    data = by_name[math.name]
    assert binding.nodes[data] == math
    assert data.parent is outer
    assert data.idname == "ShaderNodeMath"
    assert not data.is_collapsed
    assert data.width == pytest.approx(140.0)
    assert data.location == pytest.approx((120.0, -40.0))
    assert data.top == pytest.approx(-40.0)
    assert data.top - data.bottom > 100
    assert (len(data.inputs), len(data.outputs)) == (
        len(math.inputs),
        len(math.outputs),
    )
    assert binding.socket(data.outputs[0]) == math.outputs[0]

    # Linked sockets know where their links attach; unlinked ones do not.
    output = data.outputs[0]
    assert output.location is not None
    assert output.location[0] == pytest.approx(120.0 + 140.0)
    assert data.bottom < output.location[1] < data.top
    assert all(s.location is None for s in data.inputs)

    link = tree.links[0]
    assert link.fromsock.node is link.fromnode
    assert link.tosock.node is link.tonode
    assert link.is_valid


def test_extract_marks_multi_inputs_and_collapsed_nodes():
    ntree = arrange_cases.diamond()
    next(n for n in ntree.nodes if n.bl_idname == "GeometryNodeMeshCube").hide = True
    tree, _ = extract(ntree)
    join = next(n for n in tree.nodes if n.idname == "GeometryNodeJoinGeometry")
    assert join.inputs[0].is_multi_input
    sort_ids = sorted(l.multi_input_sort_id for l in tree.links if l.tonode is join)
    assert sort_ids == [0, 1, 2]
    cube = next(n for n in tree.nodes if n.idname == "GeometryNodeMeshCube")
    assert cube.is_collapsed
    # A collapsed node is drawn around its location, not below it.
    assert cube.top > cube.location[1] > cube.bottom


def test_layout_failure_leaves_the_tree_untouched(monkeypatch):
    """The layout is computed in full before anything is applied, so an
    error in it cannot leave the Blender tree half arranged."""
    ntree = arrange_cases.long_links()
    reroute = ntree.nodes.new("NodeReroute")
    source = next(n for n in ntree.nodes if n.bl_idname == "ShaderNodeMath")
    target = next(n for n in ntree.nodes if n.bl_idname == "GeometryNodeSetPosition")
    ntree.links.new(source.outputs[0], reroute.inputs[0])
    ntree.links.new(reroute.outputs[0], target.inputs["Selection"])
    before = (
        [(n.name, tuple(n.location)) for n in ntree.nodes],
        len(ntree.links),
    )

    from nodebpy.lib.nodearrange.arrange import sugiyama

    def boom(*args, **kwargs):
        raise RuntimeError("late failure")

    monkeypatch.setattr(sugiyama, "realize_layout", boom)
    with pytest.raises(RuntimeError, match="late failure"):
        arrange_node_tree(ntree, Settings(add_reroutes=True))

    after = (
        [(n.name, tuple(n.location)) for n in ntree.nodes],
        len(ntree.links),
    )
    assert after == before


def test_apply_edits():
    """Each kind of edit, applied to a Blender tree."""
    ntree = bpy.data.node_groups.new("ApplyEdits", "GeometryNodeTree")
    frame = ntree.nodes.new("NodeFrame")
    frame.shrink = False
    a = ntree.nodes.new("GeometryNodeMeshCube")
    b = ntree.nodes.new("GeometryNodeMeshCube")
    join = ntree.nodes.new("GeometryNodeJoinGeometry")
    old = ntree.nodes.new("NodeReroute")
    ntree.links.new(a.outputs[0], join.inputs[0])
    ntree.links.new(b.outputs[0], join.inputs[0])
    ntree.links.new(a.outputs[0], old.inputs[0])

    tree, binding = extract(ntree)
    data = {n.name: n for n in tree.nodes}
    d_a, d_b, d_join, d_frame = (data[n.name] for n in (a, b, join, frame))
    reroute = new_reroute(parent=d_frame)
    multi = d_join.inputs[0]

    apply(
        ntree,
        binding,
        LayoutResult(
            [
                RemoveNode(data[old.name]),
                RemoveLink(d_a.outputs[0], multi),
                AddReroute(reroute),
                AddLink(d_a.outputs[0], reroute.inputs[0]),
                AddLink(reroute.outputs[0], multi),
                RestoreMultiInputOrder(
                    multi,
                    (reroute.outputs[0], d_b.outputs[0]),
                    ((d_b.outputs[0], 0), (reroute.outputs[0], 1)),
                ),
                MoveNode(d_a, (10.0, 20.0), None),
                MoveNode(d_b, (300.0, -40.0), d_frame),
                MoveNode(reroute, (150.0, 0.0), d_frame),
                ResizeFrame(d_frame, (d_b, reroute)),
            ]
        ),
    )

    names = {n.name for n in ntree.nodes}
    assert "Reroute" in names and len(names) == 5  # the old one is replaced
    new = ntree.nodes["Reroute"]
    assert new.parent == frame and b.parent == frame and a.parent is None
    assert tuple(a.location) == (10.0, 20.0)
    assert tuple(b.location_absolute) == (300.0, -40.0)
    assert tuple(new.location_absolute) == (150.0, 0.0)
    links = {(l.from_node.name, l.to_node.name): l for l in ntree.links}
    assert set(links) == {
        ("Cube", "Reroute"),
        ("Reroute", "Join Geometry"),
        ("Cube.001", "Join Geometry"),
    }
    assert (
        links["Cube.001", "Join Geometry"].multi_input_sort_id
        < links["Reroute", "Join Geometry"].multi_input_sort_id
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def test_f32_rounds_to_single_precision():
    assert f32(0.5) == 0.5
    assert f32(0.1) != 0.1
    assert f32(0.1) == pytest.approx(0.1, abs=1e-8)
    assert f32(f32(0.1)) == f32(0.1)


def test_group_by():
    groups = group_by(["bb", "a", "cc", "d"], key=len)
    assert groups == {("bb", "cc"): 2, ("a", "d"): 1}
    assert list(group_by(["bb", "a"], key=len, sort=True)) == [("a",), ("bb",)]


@pytest.mark.parametrize(
    ("segments", "expected"),
    [
        (((0, 0), (2, 2), (0, 2), (2, 0)), True),  # an X
        (((0, 0), (1, 0), (0, 1), (1, 1)), False),  # parallel
        (((0, 0), (1, 1), (2, 2), (3, 1)), False),  # would meet beyond the end
        (((0, 0), (2, 0), (2, 0), (2, 2)), True),  # touching at an end
        (((0, 0), (1, 0), (1, 0), (2, 0)), True),  # collinear, one common point
        (((0, 0), (2, 0), (1, 0), (3, 0)), False),  # collinear, overlapping
        (((0, 0), (1, 0), (2, 0), (3, 0)), False),  # collinear, apart
        (((1, 1), (1, 1), (1, 1), (1, 1)), True),  # the same point
        (((1, 1), (1, 1), (2, 2), (2, 2)), False),  # two different points
        (((1, 0), (1, 0), (0, 0), (2, 0)), True),  # a point inside a segment
        (((0, 0), (0, 0), (0, 0), (2, 0)), True),  # a point on a segment's end
    ],
)
def test_segments_intersect(segments, expected):
    assert segments_intersect(*segments) is expected
    assert (intersect_line_line_2d(*segments) is not None) is expected


def test_segments_intersect_matches_blender():
    """Same answers as ``mathutils.geometry.intersect_line_line_2d``, which
    the layout used before it stopped depending on Blender."""
    rng = random.Random(7)
    for _ in range(3000):
        # A coarse grid makes touching and collinear cases common.
        segments = [
            (rng.randint(0, 6) * 20.0, rng.randint(0, 6) * 20.0) for _ in range(4)
        ]
        if rng.random() < 0.5:
            segments = [
                (x + rng.uniform(-1, 1), y + rng.uniform(-1, 1)) for x, y in segments
            ]
        expected = intersect_line_line_2d(*segments) is not None
        assert segments_intersect(*segments) is expected, segments
