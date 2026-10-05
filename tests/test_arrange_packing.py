"""Unconnected parts of a tree laid out apart (``arrange.packing``)."""

from itertools import pairwise

import pytest

from nodebpy.lib.nodearrange.arrange import packing
from nodebpy.lib.nodearrange.arrange.common import Vec2
from nodebpy.lib.nodearrange.arrange.edits import MoveNode
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree
from nodebpy.lib.nodearrange.zones import find_zones

from .arrange_data import MARGIN, node_overlaps, plain_node


def _chain(tree: bNodeTree, names: list[str], parent: bNode | None = None):
    nodes = [plain_node(tree, name, parent=parent) for name in names]
    for a, b in pairwise(nodes):
        tree.add_link(a.outputs[0], b.inputs[0])
    return nodes


def _names(parts) -> list[list[str]]:
    return [[node.name for node in part] for part in parts]


def _two_parts() -> bNodeTree:
    """A chain of four, a chain of two, and a framed node on its own."""
    tree = bNodeTree()
    _chain(tree, ["a1", "a2", "a3", "a4"])
    _chain(tree, ["b1", "b2"])
    note = tree.add_node(bNode("note", "NodeFrame", label="note"))
    plain_node(tree, "c1", parent=note)
    return tree


# ---------------------------------------------------------------------------
# The parts
# ---------------------------------------------------------------------------


def test_parts_are_what_links_join():
    assert _names(packing.components(_two_parts())) == [
        ["a1", "a2", "a3", "a4"],
        ["b1", "b2"],
        ["c1"],
    ]


def test_a_frame_makes_one_part_of_its_nodes():
    """Unlinked nodes in one frame, however deep, belong together; so do
    the nodes of a zone, linked or not."""
    tree = bNodeTree()
    outer = tree.add_node(bNode("outer", "NodeFrame"))
    inner = tree.add_node(bNode("inner", "NodeFrame", parent=outer))
    plain_node(tree, "x", parent=outer)
    plain_node(tree, "y", parent=inner)
    z, w = plain_node(tree, "z"), plain_node(tree, "w")
    assert _names(packing.components(tree)) == [["x", "y"], ["z"], ["w"]]

    tree.zones = find_zones(tree, [(z, w)])
    assert _names(packing.components(tree)) == [["x", "y"], ["z", "w"]]


def test_fixed_nodes_are_in_no_part():
    tree = bNodeTree()
    a, b, c = _chain(tree, ["a", "b", "c"])
    assert _names(packing.components(tree, frozenset({b}))) == [["a"], ["c"]]


def test_subtree_has_the_parts_frames_and_links():
    tree = _two_parts()
    part = packing.components(tree)[2]
    sub = packing.subtree(tree, part)
    assert [n.name for n in sub.nodes] == ["note", "c1"]
    assert sub.links == []
    first = packing.subtree(tree, packing.components(tree)[0])
    assert len(first.links) == 3 and len(first.nodes) == 4


# ---------------------------------------------------------------------------
# Packing
# ---------------------------------------------------------------------------


def test_pack_puts_the_rest_in_rows_under_the_first():
    boxes = [(0, 0, 500, 300), (0, 0, 200, 100), (0, 0, 200, 150), (0, 0, 200, 50)]
    offsets = packing.pack(boxes, Vec2(50, 60))
    placed = [
        (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)
        for b, (dx, dy) in zip(boxes, offsets)
    ]
    assert placed[0] == boxes[0]
    # Two fit beside each other under the first, tops level; the third
    # would stick out, and starts a new row under the taller of them.
    assert placed[1] == (0, -160, 200, -60)
    assert placed[2] == (250, -210, 450, -60)
    assert placed[3] == (0, -320, 200, -270)
    assert packing.pack([], Vec2(1, 1)) == []


def test_a_part_wider_than_the_first_gets_a_row_of_its_own():
    boxes = [(0, 0, 100, 100), (0, 0, 80, 10), (0, 0, 400, 10), (0, 0, 80, 10)]
    offsets = packing.pack(boxes, Vec2(10, 10))
    tops = [b[3] + dy for b, (_, dy) in zip(boxes, offsets)]
    lefts = [b[0] + dx for b, (dx, _) in zip(boxes, offsets)]
    assert lefts == [0, 0, 0, 0]
    assert tops[0] > tops[1] > tops[2] > tops[3]


def test_bounds_include_frames():
    tree = _two_parts()
    node = tree.nodes[-1]
    frame = node.parent
    box = packing.bounds([MoveNode(node, (0.0, 0.0), frame)])
    assert box is not None
    assert box[0] < 0 and box[2] > node.width and box[3] > 0
    assert packing.bounds([MoveNode(node, (0.0, 0.0), None)]) == (0, -100, 140, 0)
    assert packing.bounds([]) is None


# ---------------------------------------------------------------------------
# The layout
# ---------------------------------------------------------------------------


def _boxes(tree: bNodeTree, **settings) -> dict[str, tuple[float, ...]]:
    result = sugiyama_layout(tree, Settings(**settings), MARGIN, verify=True)
    assert node_overlaps(result) == 0
    boxes = {}
    for part in packing.components(tree):
        edits = [e for e in result.edits if isinstance(e, MoveNode) and e.node in part]
        box = packing.bounds(edits)
        assert box is not None
        boxes[part[0].name] = box
    return boxes


@pytest.mark.parametrize("add_reroutes", [False, True])
def test_parts_are_laid_out_apart(add_reroutes):
    boxes = _boxes(_two_parts(), reroutes="all" if add_reroutes else "none")
    main, second, note = boxes["a1"], boxes["b1"], boxes["c1"]
    # The largest on top, the others in a row beneath it.
    assert second[3] < main[1] and note[3] < main[1]
    assert second[0] == pytest.approx(main[0], abs=0.01)
    assert note[0] > second[2]
    assert note[3] == pytest.approx(second[3], abs=0.01)


def test_packing_keeps_the_layout_centred_where_the_nodes_were():
    tree = _two_parts()
    for node in tree.nodes:
        node.location = (1000.0, -500.0)
    result = sugiyama_layout(tree, Settings(), MARGIN)
    corners = list(result.positions().values())
    assert sum(x for x, _ in corners) / len(corners) == pytest.approx(1000, abs=0.01)
    assert sum(y for _, y in corners) / len(corners) == pytest.approx(-500, abs=0.01)


def test_a_single_part_is_laid_out_as_before():
    tree = bNodeTree()
    _chain(tree, ["a", "b", "c"])
    packed = sugiyama_layout(tree, Settings(), MARGIN).positions()
    plain = sugiyama_layout(tree, Settings(pack_components=False), MARGIN).positions()
    assert packed == plain


def test_packing_can_be_turned_off():
    """As one graph the two chains share columns."""
    result = sugiyama_layout(_two_parts(), Settings(pack_components=False), MARGIN)
    left = {n.name: x for n, (x, _) in result.positions().items()}
    assert left["b2"] in {left[name] for name in ("a1", "a2", "a3", "a4")}


# ---------------------------------------------------------------------------
# Keeping a laid-out selection off the nodes that stay put
# ---------------------------------------------------------------------------


def _overlap(a, b, gap=0.0) -> bool:
    return (
        a[0] < b[2] + gap
        and b[0] < a[2] + gap
        and a[1] < b[3] + gap
        and b[1] < a[3] + gap
    )


def test_clear_of_takes_the_shortest_way_off():
    gap = Vec2(10, 10)
    box = [(0, 0, 100, 100)]
    assert packing.clear_of(box, [], gap) == (0, 0)
    assert packing.clear_of(box, [(500, 0, 600, 100)], gap) == (0, 0)
    # Overlapping at the bottom edge: up is nearest.
    assert packing.clear_of(box, [(0, -50, 100, 20)], gap) == (0, 30)
    # At the right edge: left.
    assert packing.clear_of(box, [(90, 0, 300, 100)], gap) == (-20, 0)
    # Past the first obstacle there is a second: the move clears both.
    dx, dy = packing.clear_of(box, [(0, -50, 100, 20), (0, 110, 100, 200)], gap)
    moved = [(0 + dx, 0 + dy, 100 + dx, 100 + dy)]
    assert not any(
        _overlap(moved[0], b, 9.99) for b in [(0, -50, 100, 20), (0, 110, 100, 200)]
    )


def _selection_on_an_obstacle(width: float = 140.0):
    """A chain of three selected nodes, and an unselected node right where
    the laid-out chain is centred."""
    tree = bNodeTree()
    chain = _chain(tree, ["a", "b", "c"])
    obstacle = plain_node(tree, "obstacle")
    obstacle.select = False
    obstacle.width = width
    obstacle.draw_bounds = (0.0, -100.0, width, 0.0)
    return tree, chain, obstacle


def _placed(result) -> list[tuple[float, float, float, float]]:
    return packing.node_rects(result.edits)


def _unmoved(tree: bNodeTree, obstacle: bNode):
    """The layout of the selection with nothing to keep off."""
    tree.nodes.remove(obstacle)
    try:
        return sugiyama_layout(tree, Settings(), MARGIN, selected_only=True)
    finally:
        tree.nodes.append(obstacle)


def test_selection_is_moved_off_unselected_nodes():
    tree, chain, obstacle = _selection_on_an_obstacle()
    on_top = _unmoved(tree, obstacle)
    assert any(_overlap(r, obstacle.draw_bounds) for r in _placed(on_top))

    result = sugiyama_layout(tree, Settings(), MARGIN, selected_only=True)
    assert obstacle not in result.positions()
    assert not any(
        _overlap(r, obstacle.draw_bounds, MARGIN[1] - 0.01) for r in _placed(result)
    )
    # Moved as one: the chain is still the row it was.
    before, after = on_top.positions(), result.positions()
    shifts = {
        (round(after[n][0] - before[n][0], 2), round(after[n][1] - before[n][1], 2))
        for n in chain
    }
    assert len(shifts) == 1 and shifts != {(0.0, 0.0)}


def test_selection_is_left_where_it_is_when_clear_is_too_far():
    """An unselected node far larger than the selection: getting off it
    would take the selection further than its own size."""
    tree, _, obstacle = _selection_on_an_obstacle()
    obstacle.draw_bounds = (-5000.0, -5000.0, 5000.0, 5000.0)
    obstacle.width = 10000.0
    moved_off = sugiyama_layout(
        tree, Settings(), MARGIN, selected_only=True
    ).positions()
    stayed = _unmoved(tree, obstacle).positions()
    assert moved_off == stayed


def test_unselected_reroutes_and_frames_are_no_obstacles():
    from nodebpy.lib.nodearrange.dna import new_reroute

    def corners(tree: bNodeTree) -> dict[str, tuple[float, float]]:
        result = sugiyama_layout(tree, Settings(), MARGIN, selected_only=True)
        return {node.name: corner for node, corner in result.positions().items()}

    alone, _, obstacle = _selection_on_an_obstacle()
    alone.nodes.remove(obstacle)

    tree, _, obstacle = _selection_on_an_obstacle()
    tree.nodes.remove(obstacle)
    reroute = tree.add_node(new_reroute())
    reroute.select = False
    frame = tree.add_node(bNode("frame", "NodeFrame"))
    frame.select = False

    assert corners(tree) == corners(alone)
