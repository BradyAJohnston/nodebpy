"""Snapping a layout to the node editor's grid (``layout.snapping``)."""

import bpy
import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.layout import sugiyama_layout
from nodebpy.layout.dna import bNodeTree
from nodebpy.layout.edits import MoveNode
from nodebpy.layout.snapping import GRID_SIZE, snap_to_grid

from . import cases
from .data import collapsed_math, node_overlaps, options, plain_chain, random_tree


def _off_grid(edits) -> list[str]:
    """Names of the placed nodes whose location is not on the grid."""
    names = []
    for edit in edits:
        if not isinstance(edit, MoveNode) or edit.node.is_reroute():
            continue
        node = edit.node
        x = edit.top_left[0] + node.location[0] - node.draw_bounds[0]
        y = edit.top_left[1] + node.location[1] - node.draw_bounds[3]
        if any(abs(v / GRID_SIZE - round(v / GRID_SIZE)) > 1e-4 for v in (x, y)):
            names.append(node.name)
    return names


def test_layout_is_off_the_grid_unless_asked():
    tree = bNodeTree()
    plain_chain(tree, "abc")
    assert _off_grid(sugiyama_layout(tree, options()).edits)
    assert not _off_grid(sugiyama_layout(tree, options(snap_to_grid=True)).edits)


def test_a_row_stays_a_row():
    tree = bNodeTree()
    plain_chain(tree, "abcd")
    result = sugiyama_layout(tree, options(snap_to_grid=True))
    tops = {y for _, y in result.positions().values()}
    lefts = sorted(x for x, _ in result.positions().values())
    assert len(tops) == 1
    assert len(set(lefts)) == 4


def test_nodes_keep_their_gap_rounded_down_to_the_grid():
    """Two nodes 100 tall, one above the other with a gap of 30: snapped, the
    gap is 20 or 40, never less."""
    tree = bNodeTree()
    nodes = plain_chain(tree, "ab")
    moves = [
        MoveNode(nodes["a"], (3.0, 9.0), None),
        MoveNode(nodes["b"], (3.0, 9.0 - 100.0 - 30.0), None),
    ]
    a, b = (edit.top_left for edit in snap_to_grid(moves))
    assert a == (0.0, 0.0)
    assert (a[1] - 100.0) - b[1] in (20.0, 40.0)

    # Rounding alone would leave these two 10 apart: the lower one steps down.
    moves = [
        MoveNode(nodes["a"], (0.0, -9.0), None),
        MoveNode(nodes["b"], (0.0, -9.0 - 100.0 - 21.0), None),
    ]
    a, b = (edit.top_left for edit in snap_to_grid(moves))
    assert a == (0.0, 0.0)
    assert b == (0.0, -120.0)


def test_collapsed_node_is_snapped_by_its_location():
    """A collapsed node's location is not the corner of its box; it is the
    location that lands on the grid."""
    tree = bNodeTree()
    node = collapsed_math(tree, "m")
    node.location = (0.0, -4.0)
    assert node.location[1] != node.draw_bounds[3]
    (edit,) = snap_to_grid([MoveNode(node, (7.0, 31.0), None)])
    assert not _off_grid([edit])


def test_nodes_are_snapped_beside_reroutes():
    tree = cases.CASES["long_links"]()
    cases.reset_locations(tree)
    arrange(tree, SugiyamaOptions(reroutes="all", snap_to_grid=True))
    reroutes = [n for n in tree.nodes if n.bl_idname == "NodeReroute"]
    others = [n for n in tree.nodes if n.bl_idname not in ("NodeReroute", "NodeFrame")]
    assert reroutes
    for node in others:
        x, y = node.location_absolute
        assert x % GRID_SIZE == pytest.approx(0, abs=0.01)
        assert y % GRID_SIZE == pytest.approx(0, abs=0.01)


@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("reroutes", ["none", "all"])
def test_snapped_random_tree_has_no_overlaps(seed, reroutes):
    result = sugiyama_layout(
        random_tree(seed), options(snap_to_grid=True, reroutes=reroutes), verify=True
    )
    assert node_overlaps(result) == 0
    assert not _off_grid(result.edits)


def test_snapping_in_blender_puts_locations_on_the_grid():
    tree = bpy.data.node_groups.new("Snapped", "GeometryNodeTree")
    a, b, c = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(3))
    frame = tree.nodes.new("NodeFrame")
    c.parent = frame
    for source, target in ((a, b), (b, c)):
        tree.links.new(source.outputs[0], target.inputs[0])

    arrange(tree, SugiyamaOptions(snap_to_grid=True))

    for node in (a, b, c):
        x, y = node.location_absolute
        assert x % GRID_SIZE == pytest.approx(0, abs=0.01)
        assert y % GRID_SIZE == pytest.approx(0, abs=0.01)
