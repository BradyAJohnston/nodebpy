"""Layout metrics (``nodebpy.lib.nodearrange.metrics``).

First the measurements themselves, on trees placed by hand so every count is
known. Then what the Sugiyama layout must always deliver on the hand-built
cases of ``arrange_cases``, and a snapshot of its metrics on them and on the
asset groups: a change to the layout algorithm shows up there as a diff of
crossings, straight links, size and so on, to be judged and accepted with
``pytest --snapshot-update``.
"""

import bpy
import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.lib.nodearrange.metrics import CostWeights, LayoutMetrics, measure

from . import arrange_cases

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
    assert metrics.cost() == 0


def test_straight_link():
    """An output wired to the input at the same height is a straight link."""
    tree = _tree("Straight")
    a = _math(tree, 0, 0)
    b = _math(tree, 300, 0)
    link = tree.links.new(a.outputs[0], b.inputs[0])

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
    assert link.is_valid


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


def test_frames():
    """Frames overlap when their members interleave, and a node placed on a
    frame it does not belong to is foreign to it."""
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


def test_imbalance():
    """A node fed by two others is balanced when it sits level with the
    middle of the two."""
    tree = _tree("Balance")
    upper = _math(tree, 0, 200)
    lower = _math(tree, 0, -200)
    merge = _math(tree, 400, 0)
    tree.links.new(upper.outputs[0], merge.inputs[0])
    tree.links.new(lower.outputs[0], merge.inputs[1])
    assert measure(tree).imbalance == pytest.approx(0, abs=0.01)

    merge.location.y = 150
    assert measure(tree).imbalance == pytest.approx(150, abs=0.01)


def test_cost_weights():
    tree = _tree("Cost")
    a = _math(tree, 400, 0)
    b = _math(tree, 0, 0)
    tree.links.new(a.outputs[0], b.inputs[0])
    metrics = measure(tree)
    only_backward = CostWeights(
        backward_link=7,
        bent_link=0,
        link_length=0,
        link_span_y=0,
        area=0,
        link_through_node=0,
    )
    assert metrics.cost(only_backward) == 7
    assert metrics.cost() > 0
    assert set(metrics.as_dict()) == set(LayoutMetrics.field_names())
    assert metrics.as_dict(ndigits=None)["link_length"] == metrics.link_length
    assert "0 crossings" in metrics.summary()
    assert "1 backward" in metrics.summary()


# ---------------------------------------------------------------------------
# The Sugiyama layout, measured
# ---------------------------------------------------------------------------


def _arranged(name: str, options: SugiyamaOptions | None = None) -> LayoutMetrics:
    tree = {**arrange_cases.CASES, **arrange_cases.asset_groups()}[name]()
    arrange_cases.reset_locations(tree)
    arrange(tree, options or SugiyamaOptions())
    return measure(tree)


@pytest.mark.parametrize("name", list(arrange_cases.CASES))
def test_layout_is_sound(name):
    """Whatever the tree, an arranged layout has no overlapping nodes or
    frames and every link runs left to right."""
    metrics = _arranged(name)
    assert metrics.node_overlaps == 0
    assert metrics.backward_links == 0
    assert metrics.frame_overlaps == 0
    assert metrics.foreign_nodes_in_frames == 0
    assert metrics.crossings == 0  # none of the hand-built cases needs one


def test_chain_is_straight_with_full_socket_alignment():
    """With sockets fully aligned, a chain is laid out with every link
    straight."""
    metrics = _arranged("chain", SugiyamaOptions(socket_alignment="FULL"))
    assert metrics.straightness == 1


def test_framed_stages_run_left_to_right():
    """Three frames in sequence end up side by side: far wider than tall."""
    metrics = _arranged("framed_stages")
    assert metrics.aspect > 3


@pytest.mark.parametrize("name", [*arrange_cases.CASES, *arrange_cases.asset_groups()])
def test_layout_metrics_snapshot(name, snapshot):
    """The metrics of the default layout. A layout change shows up here;
    review the diff and accept it with ``pytest --snapshot-update``."""
    assert _arranged(name).as_dict() == snapshot
