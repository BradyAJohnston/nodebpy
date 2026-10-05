"""Layout metrics (``tests/layout/metrics.py``): the measurements, on trees
placed by hand so that every count is known, then what the layout delivers
on the hand-built trees of ``cases``.
"""

import bpy
import pytest

from nodebpy import SugiyamaOptions
from nodebpy.layout.dna import bNodeTree
from nodebpy.layout.extract import extract
from nodebpy.layout.zones import find_zones

from . import cases
from .data import plain_node
from .metrics import LayoutMetrics, frame_rects, measure
from .report import CostWeights, cost

_SOCKET_ROW = 22.0  # rough height of one socket row


def _tree(name: str):
    return bpy.data.node_groups.new(name, "GeometryNodeTree")


def _math(tree, x: float, y: float):
    node = tree.nodes.new("ShaderNodeMath")
    node.location = (x, y)
    return node


# ---------------------------------------------------------------------------
# The measurements
# ---------------------------------------------------------------------------


def test_empty_tree():
    metrics = measure(_tree("Empty"))
    assert metrics.nodes == 0
    assert metrics.links == 0
    assert metrics.area == 0
    assert metrics.aspect == 0
    assert metrics.straightness == 1
    assert cost(metrics) == 0


def test_straight_link():
    """An output wired to the input at the same height is a straight link."""
    tree = _tree("Straight")
    a = _math(tree, 0, 0)
    b = _math(tree, 300, 0)
    tree.links.new(a.outputs[0], b.inputs[0])

    bent = measure(tree)
    assert bent.links == 1
    assert bent.straight_links == 0  # the output row is above the input row
    assert bent.link_span_y > _SOCKET_ROW

    # Lower the consumer until its input is level with the output.
    b.location.y += bent.link_span_y
    straight = measure(tree)
    assert straight.straight_links == 1
    assert straight.straightness == 1
    assert straight.link_span_y == pytest.approx(0, abs=0.01)
    assert straight.backward_links == 0


def test_crossing_links():
    """Two producers wired to the opposite consumers cross once; wired
    straight across they do not."""
    tree = _tree("Crossing")
    top_left = _math(tree, 0, 0)
    bottom_left = _math(tree, 0, -400)
    top_right = _math(tree, 400, 0)
    bottom_right = _math(tree, 400, -400)

    tree.links.new(top_left.outputs[0], top_right.inputs[0])
    tree.links.new(bottom_left.outputs[0], bottom_right.inputs[0])
    assert measure(tree).crossings == 0

    tree.links.clear()
    tree.links.new(top_left.outputs[0], bottom_right.inputs[0])
    tree.links.new(bottom_left.outputs[0], top_right.inputs[0])
    assert measure(tree).crossings == 1


def test_crossings_by_what_links_carry():
    """A crossing counts as mixed when one of the links is a flow link, and
    as a flow crossing when both are."""

    def crossed(first: str, second: str):
        tree = _tree("Kinds")
        ends = []
        for kind, (y_from, y_to) in ((first, (0, -400)), (second, (-400, 0))):
            if kind == "geometry":
                a = tree.nodes.new("GeometryNodeSetPosition")
                b = tree.nodes.new("GeometryNodeSetPosition")
            else:
                a, b = _math(tree, 0, 0), _math(tree, 0, 0)
            a.location, b.location = (0, y_from), (400, y_to)
            ends.append((a, b))
        for a, b in ends:
            tree.links.new(a.outputs[0], b.inputs[0])
        metrics = measure(tree)
        return metrics.crossings, metrics.flow_crossings, metrics.mixed_crossings

    assert crossed("value", "value") == (1, 0, 0)
    assert crossed("geometry", "value") == (1, 0, 1)
    assert crossed("geometry", "geometry") == (1, 1, 0)


def test_trunk_and_zone_metrics():
    """Counted on plain data placed by hand: a -> b -> c carrying geometry,
    with b forking to d as well, and b .. c a zone."""

    def place(node, x, y):
        dx, dy = x - node.draw_bounds[0], y - node.draw_bounds[3]
        node.location = (x, y)
        node.draw_bounds = (x, y - 100.0, x + 140.0, y)
        for socket in (*node.inputs, *node.outputs):
            socket.location = (socket.location[0] + dx, socket.location[1] + dy)

    tree = bNodeTree()
    a, b, c, d = (plain_node(tree, name) for name in "abcd")
    for source, target in ((a, b), (b, c), (b, d)):
        tree.add_link(source.outputs[0], target.inputs[0])
    tree.zones = find_zones(tree, [(b, c)])
    for node, (x, y) in ((a, (0, 0)), (b, (200, 0)), (c, (400, 0)), (d, (400, -300))):
        place(node, x, y)

    metrics = measure(tree)
    assert metrics.flow_links == 3
    assert metrics.level_flow_links == 2  # a -> b and b -> c: tops level
    assert (metrics.zones, metrics.level_zones) == (1, 1)
    # b's output is 172 above the middle of the two inputs it fans out to
    # (150 between the nodes, and an input sits 22 below an output).
    assert metrics.fork_imbalance == pytest.approx(172)

    place(c, 400, 300)
    place(d, 400, -300)
    metrics = measure(tree)
    assert metrics.fork_imbalance == pytest.approx(22)
    assert metrics.level_zones == 0
    assert metrics.level_flow_links == 1


def test_links_from_one_socket_do_not_cross():
    tree = _tree("FanOut")
    source = _math(tree, 0, 0)
    for y in (200, 0, -200):
        tree.links.new(source.outputs[0], _math(tree, 400, y).inputs[0])
    assert measure(tree).crossings == 0


def test_backward_link():
    tree = _tree("Backward")
    a = _math(tree, 400, 0)
    b = _math(tree, 0, 0)
    tree.links.new(a.outputs[0], b.inputs[0])
    assert measure(tree).backward_links == 1


def test_node_overlap():
    tree = _tree("Overlap")
    _math(tree, 0, 0)
    _math(tree, 50, -50)
    _math(tree, 1000, 0)
    assert measure(tree).node_overlaps == 1


def test_link_through_node():
    """A link between two nodes passes over a third placed between them."""
    tree = _tree("Through")
    a = _math(tree, 0, 0)
    b = _math(tree, 600, 0)
    tree.links.new(a.outputs[0], b.inputs[0])
    assert measure(tree).links_through_nodes == 0

    _math(tree, 300, 0)
    assert measure(tree).links_through_nodes == 1


def test_frame_overlaps_and_foreign_nodes_in_frames():
    """Frames overlap when their padded boxes do, and a node placed on a
    frame it is not in is foreign to it."""
    tree = _tree("Frames")
    frames = []
    for x in (0, 1000):
        frame = tree.nodes.new("NodeFrame")
        node = tree.nodes.new("ShaderNodeMath")
        node.parent = frame
        node.location = (x, 0)
        frames.append((frame, node))
    assert measure(tree).frame_overlaps == 0
    assert measure(tree).foreign_nodes_in_frames == 0

    # A loose node dropped onto the first frame.
    loose = _math(tree, 20, -20)
    metrics = measure(tree)
    assert metrics.foreign_nodes_in_frames == 1
    assert metrics.node_overlaps == 1
    tree.nodes.remove(loose)

    # Slide the second frame's node next to the first's: the frames' padded
    # boxes overlap though the nodes themselves do not.
    frames[1][1].location = (160, 0)
    metrics = measure(tree)
    assert metrics.frame_overlaps == 1
    assert metrics.node_overlaps == 0

    # A frame nested in another does not overlap it.
    frames[1][0].parent = frames[0][0]
    assert measure(tree).frame_overlaps == 0

    # An empty frame is not drawn, so it cannot overlap anything.
    tree.nodes.new("NodeFrame")
    assert measure(tree).frame_overlaps == 0


def test_reroutes_are_points():
    tree = _tree("Reroutes")
    a = _math(tree, 0, 0)
    reroute = tree.nodes.new("NodeReroute")
    reroute.location = (300, -100)
    b = _math(tree, 600, 0)
    tree.links.new(a.outputs[0], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], b.inputs[0])
    metrics = measure(tree)
    assert metrics.nodes == 3
    assert metrics.reroutes == 1
    assert metrics.links == 2
    assert metrics.links_through_nodes == 0
    # The two links meet at the reroute; that is not a crossing, even when
    # the second doubles back over the first.
    assert metrics.crossings == 0
    reroute.location = (800, -100)
    doubled_back = measure(tree)
    assert doubled_back.crossings == 0
    assert doubled_back.backward_links == 1


def test_cost_weighs_each_defect():
    tree = _tree("Cost")
    a = _math(tree, 400, 0)
    b = _math(tree, 0, 0)
    tree.links.new(a.outputs[0], b.inputs[0])
    metrics = measure(tree)

    nothing = dict.fromkeys(CostWeights.__slots__, 0.0)
    assert cost(metrics, CostWeights(**nothing)) == 0
    assert cost(metrics, CostWeights(**{**nothing, "backward_link": 7.0})) == 7
    assert cost(metrics, CostWeights(**{**nothing, "area": 2.0})) == pytest.approx(
        2 * metrics.width * metrics.height
    )


def test_summary_and_dict_report_the_counts():
    tree = _tree("Summary")
    a = _math(tree, 400, 0)
    b = _math(tree, 0, 0)
    tree.links.new(a.outputs[0], b.inputs[0])
    metrics = measure(tree)

    assert list(metrics.as_dict()) == LayoutMetrics.field_names()
    assert metrics.as_dict()["link_length"] == round(metrics.link_length, 1)
    assert "0 crossings" in metrics.summary()
    assert "1 backward" in metrics.summary()
    assert metrics.headline()["crossings"] == 0


# ---------------------------------------------------------------------------
# The layout, measured
# ---------------------------------------------------------------------------


# Cases the layout does not get right yet. Strict: fixing one fails the test
# until it is taken off this list.
KNOWN_DEFECTS = {
    "shader_material": "one avoidable crossing",
}


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(
            name,
            marks=pytest.mark.xfail(reason=KNOWN_DEFECTS[name], strict=True),
        )
        if name in KNOWN_DEFECTS
        else name
        for name in cases.CASES
    ],
)
def test_layout_has_no_overlaps_backward_links_or_crossings(name):
    """None of the hand-built cases needs a crossing."""
    metrics = measure(cases.arranged(name))
    assert metrics.node_overlaps == 0
    assert metrics.backward_links == 0
    assert metrics.frame_overlaps == 0
    assert metrics.foreign_nodes_in_frames == 0
    assert metrics.crossings == 0


def test_chain_is_straight_with_full_socket_alignment():
    """Off the grid: a node cannot be on a grid row and have its sockets
    level with its neighbour's at once."""
    options = SugiyamaOptions(socket_alignment="FULL", snap_to_grid=False)
    assert measure(cases.arranged("chain", options)).straightness == 1


def test_framed_stages_are_side_by_side_in_order():
    tree = extract(cases.arranged("framed_stages"))[0]
    rects = {frame.label: rect for frame, rect in frame_rects(tree).items()}
    first, second, third = (rects[f"Stage {i}"] for i in (1, 2, 3))
    # Frames may touch; 0.01 allows for single precision.
    assert first[2] <= second[0] + 0.01 and second[2] <= third[0] + 0.01
