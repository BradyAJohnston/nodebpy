"""The trunk: which links are flow links (``priority``), and the layout
keeping the trunk a straight row with forks symmetric around it."""

import pytest

from nodebpy import SugiyamaOptions
from nodebpy.layout.digraph import LayoutGraph
from nodebpy.layout.dna import bNode, bNodeTree
from nodebpy.layout.model import Kind, Node, Socket, link_priority
from nodebpy.layout.priority import FLOW, MAIN, socket_priorities

from . import cases
from .data import plain_node

FLOAT = "NodeSocketFloat"


def _tops(nodes) -> list[float]:
    return [round(n.location_absolute.y, 1) for n in nodes]


def _by_type(tree, idname: str):
    return sorted(
        (n for n in tree.nodes if n.bl_idname == idname), key=lambda n: n.location.x
    )


# ---------------------------------------------------------------------------
# Link priorities
# ---------------------------------------------------------------------------


def _set_position(tree: bNodeTree, name: str) -> bNode:
    """Geometry, Selection and Offset in; Geometry out."""
    node = plain_node(tree, name, inputs=3)
    node.inputs[1].idname = "NodeSocketBool"
    node.inputs[2].idname = "NodeSocketVector"
    return node


def _math(tree: bNodeTree, name: str) -> bNode:
    return plain_node(tree, name, idname="ShaderNodeMath", socket=FLOAT, inputs=2)


def test_first_linked_flow_socket_has_the_highest_priority():
    """Without a flow socket a node's first linked socket is its main one,
    and unlinked sockets have no priority."""
    tree = bNodeTree()
    a, b = _set_position(tree, "a"), _set_position(tree, "b")
    x, y = _math(tree, "x"), _math(tree, "y")
    tree.add_link(a.outputs[0], b.inputs[0])  # the trunk
    tree.add_link(y.outputs[0], b.inputs[2])  # a value into Offset
    tree.add_link(x.outputs[0], y.inputs[1])  # into y's second input only
    tree.add_link(x.outputs[0], b.inputs[1])

    priorities = socket_priorities(tree)
    assert priorities == {
        a.outputs[0]: FLOW,
        b.inputs[0]: FLOW,
        x.outputs[0]: MAIN,
        y.inputs[1]: MAIN,
        y.outputs[0]: MAIN,
    }

    # A link Blender calls invalid counts like any other.
    tree.links[0].is_valid = False
    assert socket_priorities(tree) == priorities


def test_link_priority_adds_up_the_priorities_of_its_sockets():
    tree = bNodeTree()
    a, b = _set_position(tree, "a"), _set_position(tree, "b")
    x = _math(tree, "x")
    tree.add_link(a.outputs[0], b.inputs[0])
    tree.add_link(x.outputs[0], b.inputs[2])
    priorities = socket_priorities(tree)

    G: LayoutGraph[Node] = LayoutGraph()
    u, v, w = Node(a), Node(b), Node(x)
    trunk = G.add_link(u, v, Socket(u, 0, True), Socket(v, 0, False))
    side = G.add_link(w, v, Socket(w, 0, True), Socket(v, 2, False))
    constraint = G.add_link(u, w)
    assert link_priority(trunk, priorities) == 2 * FLOW
    assert link_priority(side, priorities) == MAIN
    assert link_priority(constraint, priorities) == 0
    assert link_priority(trunk, {}) == 0

    # A piece of a long link has the priority of the whole link.
    dummy = Node(type=Kind.DUMMY)
    dummy.priority = 4
    piece = G.add_link(dummy, v, Socket(dummy, 0, True), Socket(v, 2, False))
    assert link_priority(piece, priorities) == 4


# ---------------------------------------------------------------------------
# Straight trunk
# ---------------------------------------------------------------------------


def test_trunk_is_one_row_with_its_feeders_below():
    tree = cases.arranged("trunk_with_feeders")
    trunk = _by_type(tree, "GeometryNodeSetPosition")
    assert len(set(_tops(trunk))) == 1
    for math in _by_type(tree, "ShaderNodeMath"):
        assert math.location.y < trunk[0].location.y


def test_trunk_is_a_staircase_when_not_straightened():
    tree = cases.arranged(
        "trunk_with_feeders",
        SugiyamaOptions(straighten_trunk=False, pin_group_output=False),
    )
    assert len(set(_tops(_by_type(tree, "GeometryNodeSetPosition")))) > 1


def test_trunk_stays_straight_through_frames():
    tree = cases.arranged("framed_stages")
    trunk = _by_type(tree, "GeometryNodeSetPosition")
    assert len(trunk) == 9
    assert len(set(_tops(trunk))) == 1


def test_trunk_stays_straight_when_long_links_get_reroutes():
    tree = cases.arranged("long_links", SugiyamaOptions(reroutes="all"))
    assert len(set(_tops(_by_type(tree, "GeometryNodeSetPosition")))) == 1


def test_fork_that_merges_again_is_symmetric():
    """A fork into three branches that merge again: the fork, the middle
    branch and the merge are level, the other branches the same distance
    above and below, all three in one column."""
    tree = cases.arranged("diamond")
    (cube,) = _by_type(tree, "GeometryNodeMeshCube")
    (join,) = _by_type(tree, "GeometryNodeJoinGeometry")
    (tail,) = _by_type(tree, "GeometryNodeSetShadeSmooth")
    branches = sorted(
        _by_type(tree, "GeometryNodeSetPosition"), key=lambda n: -n.location.y
    )
    assert len({n.location.x for n in branches}) == 1

    upper, middle, lower = branches
    assert _tops([cube, join, tail]) == _tops([middle]) * 3
    assert upper.location.y - middle.location.y == pytest.approx(
        middle.location.y - lower.location.y
    )
