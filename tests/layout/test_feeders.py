"""The step ``pull_feeders``: a node whose links all go to one node is
moved level with that node, as far as its column allows."""

from itertools import pairwise

from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.sugiyama import default_pipeline

from .data import MARGIN, plain_node, positions


def _tree() -> bNodeTree:
    """A frame holding a trunk of three nodes, a tall stack of sources into
    its first node and one feeder into its last. The sources push the
    trunk up, and a run packed downwards puts the feeder at the frame's
    bottom edge, well below the trunk."""
    tree = bNodeTree()
    frame = tree.add_node(bNode("frame", "NodeFrame"))
    nodes = {}
    for name in "abc":
        nodes[name] = plain_node(tree, name, inputs=2, outputs=1, parent=frame)
    for i in range(4):
        source = plain_node(
            tree, f"s{i}", inputs=0, outputs=1, height=120, parent=frame
        )
        tree.add_link(source.outputs[0], nodes["a"].inputs[0])
    tree.add_link(nodes["a"].outputs[0], nodes["b"].inputs[0])
    tree.add_link(nodes["b"].outputs[0], nodes["c"].inputs[0])
    feeder = plain_node(tree, "f", inputs=0, outputs=1, parent=frame)
    tree.add_link(feeder.outputs[0], nodes["c"].inputs[1])
    return tree


def test_feeder_moves_up_to_the_node_it_feeds():
    """The feeder cannot be level with ``c``: ``b`` is there in its column.
    It comes as close as ``b`` allows, where a run packed downwards left
    it at the bottom of the drawing."""
    tree = _tree()
    without = default_pipeline()
    without.remove("pull_feeders")
    before = positions(tree, direction="RIGHT_DOWN", pipeline=without)
    after = positions(tree, direction="RIGHT_DOWN")
    snug = after["b"][1] - 100 - MARGIN[1]
    assert before["f"][1] < snug - MARGIN[1]
    assert after["f"][1] == snug
    # Nothing else moved, other than with the centring of the whole.
    for name in before:
        if name != "f":
            assert before[name][1] - before["b"][1] == after[name][1] - after["b"][1]


def test_feeders_into_one_node_stack_without_overlapping():
    tree = bNodeTree()
    target = plain_node(tree, "t", inputs=3, outputs=0)
    for i in range(3):
        feeder = plain_node(tree, f"f{i}", inputs=0, outputs=1)
        tree.add_link(feeder.outputs[0], target.inputs[i])
    placed = positions(tree)
    tops = sorted((placed[f"f{i}"][1] for i in range(3)), reverse=True)
    for upper, lower in pairwise(tops):
        assert upper - lower >= 100 + MARGIN[1]
