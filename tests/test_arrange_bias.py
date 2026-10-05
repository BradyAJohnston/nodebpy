"""Bias controls of the layout: keeping the trunk straight, laying forks out
symmetrically, pinning the group's interface nodes."""

import itertools

import bpy
import pytest

from nodebpy import SugiyamaOptions, arrange
from nodebpy.lib.nodearrange.arrange.graph import Kind, Node, Socket, link_priority
from nodebpy.lib.nodearrange.arrange.priority import (
    FLOW,
    MAIN,
    socket_priorities,
)
from nodebpy.lib.nodearrange.arrange.tree import Tree
from nodebpy.lib.nodearrange.dna import bNode, bNodeTree
from nodebpy.lib.nodearrange.extract import extract

from . import arrange_cases

GEOMETRY = "NodeSocketGeometry"
FLOAT = "NodeSocketFloat"

OFF = SugiyamaOptions(
    straighten_trunk=False, balance_min_column=0, pin_group_output=False
)


def _arranged(case, options: SugiyamaOptions | None = None):
    tree = case()
    arrange_cases.reset_locations(tree)
    arrange(tree, options or SugiyamaOptions())
    return tree


def _tops(nodes) -> list[float]:
    return [round(n.location.y, 1) for n in nodes]


def _by_type(tree, idname: str):
    return sorted(
        (n for n in tree.nodes if n.bl_idname == idname), key=lambda n: n.location.x
    )


# ---------------------------------------------------------------------------
# Link priorities
# ---------------------------------------------------------------------------


def _set_position(tree: bNodeTree, name: str) -> bNode:
    """Geometry, Selection and Offset in; Geometry out."""
    node = tree.add_node(bNode(name, "GeometryNodeSetPosition"))
    node.add_socket(False, idname=GEOMETRY)
    node.add_socket(False, idname="NodeSocketBool")
    node.add_socket(False, idname="NodeSocketVector")
    node.add_socket(True, idname=GEOMETRY)
    return node


def _math(tree: bNodeTree, name: str) -> bNode:
    node = tree.add_node(bNode(name, "ShaderNodeMath"))
    node.add_socket(False, idname=FLOAT)
    node.add_socket(False, idname=FLOAT)
    node.add_socket(True, idname=FLOAT)
    return node


def test_socket_priorities():
    """A node's first linked flow socket scores highest; without one, its
    first linked socket is its main one; unlinked sockets score nothing."""
    tree = bNodeTree()
    a, b = _set_position(tree, "a"), _set_position(tree, "b")
    x, y = _math(tree, "x"), _math(tree, "y")
    tree.add_link(a.outputs[0], b.inputs[0])  # geometry trunk
    tree.add_link(y.outputs[0], b.inputs[2])  # a value into Offset
    tree.add_link(x.outputs[0], y.inputs[1])  # into y's second input only
    tree.add_link(x.outputs[0], b.inputs[1])

    priorities = socket_priorities(tree)
    assert priorities == {
        a.outputs[0]: FLOW,
        b.inputs[0]: FLOW,
        x.outputs[0]: MAIN,
        y.inputs[1]: MAIN,  # y's first *linked* input
        y.outputs[0]: MAIN,
    }

    # A link Blender calls invalid is still a link, here as in the layout.
    tree.links[0].is_valid = False
    assert socket_priorities(tree) == priorities


def test_link_priority():
    tree = bNodeTree()
    a, b = _set_position(tree, "a"), _set_position(tree, "b")
    x = _math(tree, "x")
    tree.add_link(a.outputs[0], b.inputs[0])
    tree.add_link(x.outputs[0], b.inputs[2])
    priorities = socket_priorities(tree)

    G: Tree[Node] = Tree()
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


def test_extract_reads_socket_types():
    tree, _ = extract(arrange_cases.chain())
    cube = next(n for n in tree.nodes if n.idname == "GeometryNodeMeshCube")
    assert cube.outputs[0].idname == GEOMETRY
    assert not cube.is_group_input() and not cube.is_group_output()


# ---------------------------------------------------------------------------
# Straight trunk
# ---------------------------------------------------------------------------


def test_trunk_is_a_flat_row():
    """The geometry nodes of the trunk are level; the side chains feeding
    them hang below."""
    tree = _arranged(arrange_cases.trunk_with_feeders)
    trunk = _by_type(tree, "GeometryNodeSetPosition")
    assert len(set(_tops(trunk))) == 1
    for math in _by_type(tree, "ShaderNodeMath"):
        assert math.location.y < trunk[0].location.y

    # Without the bias the side chains pull the trunk into a staircase.
    plain = _arranged(arrange_cases.trunk_with_feeders, OFF)
    assert len(set(_tops(_by_type(plain, "GeometryNodeSetPosition")))) > 1


def test_trunk_stays_straight_through_frames():
    tree = _arranged(arrange_cases.framed_stages)
    trunk = _by_type(tree, "GeometryNodeSetPosition")
    assert len(trunk) == 9
    assert len({round(n.location_absolute.y, 1) for n in trunk}) == 1


def test_trunk_with_reroutes():
    """The trunk stays level when long links are routed through reroutes."""
    tree = _arranged(arrange_cases.long_links, SugiyamaOptions(add_reroutes=True))
    assert len(set(_tops(_by_type(tree, "GeometryNodeSetPosition")))) == 1


# ---------------------------------------------------------------------------
# Symmetric forks
# ---------------------------------------------------------------------------


def test_fork_and_merge_is_symmetric():
    """A fork into three branches that merge again: the fork, the middle
    branch and the merge are level, the other branches the same distance
    above and below, all three in one column."""
    tree = _arranged(arrange_cases.diamond)
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


def test_balance_min_column():
    """Height balancing leaves a column of a few parallel branches whole,
    unless told it may split it."""
    whole = _arranged(arrange_cases.diamond, SugiyamaOptions(straighten_trunk=False))
    assert len({n.location.x for n in _by_type(whole, "GeometryNodeSetPosition")}) == 1

    split = _arranged(
        arrange_cases.diamond,
        SugiyamaOptions(straighten_trunk=False, balance_min_column=0),
    )
    assert len({n.location.x for n in _by_type(split, "GeometryNodeSetPosition")}) == 2


# ---------------------------------------------------------------------------
# Pinned interface nodes
# ---------------------------------------------------------------------------


def _with_interface():
    """Group Input -> a -> Group Output, and a -> b -> c with nothing after:
    the output is not at the end of the longest chain, and a second Group
    Input feeds the last node."""
    tree = bpy.data.node_groups.new("Interface", "GeometryNodeTree")
    tree.interface.new_socket("Geometry", in_out="INPUT", socket_type=GEOMETRY)
    tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type=GEOMETRY)
    group_in = tree.nodes.new("NodeGroupInput")
    late_in = tree.nodes.new("NodeGroupInput")
    group_out = tree.nodes.new("NodeGroupOutput")
    a, b, c = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(3))
    join = tree.nodes.new("GeometryNodeJoinGeometry")
    tree.links.new(group_in.outputs[0], a.inputs[0])
    tree.links.new(a.outputs[0], group_out.inputs[0])
    tree.links.new(a.outputs[0], b.inputs[0])
    tree.links.new(b.outputs[0], c.inputs[0])
    tree.links.new(c.outputs[0], join.inputs[0])
    tree.links.new(late_in.outputs[0], join.inputs[0])
    return tree


def test_pin_group_output():
    tree = _arranged(_with_interface)
    last = max(n.location.x for n in tree.nodes)
    assert tree.nodes["Group Output"].location.x == last

    free = _arranged(_with_interface, SugiyamaOptions(pin_group_output=False))
    assert free.nodes["Group Output"].location.x < max(n.location.x for n in free.nodes)


def test_pin_group_input():
    """Off by default: a Group Input sits next to what it feeds."""
    tree = _arranged(_with_interface)
    first = min(n.location.x for n in tree.nodes)
    assert tree.nodes["Group Input"].location.x == first
    assert tree.nodes["Group Input.001"].location.x > first

    pinned = _arranged(_with_interface, SugiyamaOptions(pin_group_input=True))
    first = min(n.location.x for n in pinned.nodes)
    assert pinned.nodes["Group Input"].location.x == first
    assert pinned.nodes["Group Input.001"].location.x == first


def test_pinning_leaves_framed_interface_nodes_alone():
    tree = _with_interface()
    frame = tree.nodes.new("NodeFrame")
    tree.nodes["Group Output"].parent = frame
    arrange(tree, SugiyamaOptions())
    assert tree.nodes["Group Output"].location_absolute.x < max(
        n.location_absolute.x for n in tree.nodes if n.bl_idname != "NodeFrame"
    )


# ---------------------------------------------------------------------------
# Layer constraints on plain data
# ---------------------------------------------------------------------------


def _plain(tree: bNodeTree, name: str, idname="GeometryNodeSetPosition") -> bNode:
    node = tree.add_node(
        bNode(name, idname, width=140.0, draw_bounds=(0.0, -100.0, 140.0, 0.0))
    )
    node.add_socket(True, location=(140.0, -30.0), idname=GEOMETRY)
    node.add_socket(False, location=(0.0, -52.0), idname=GEOMETRY)
    return node


def _columns(tree: bNodeTree, settings=None) -> dict[str, float]:
    from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout

    result = sugiyama_layout(tree, settings, (50.0, 20.0), verify=True)
    return {node.name: x for node, (x, _) in result.positions().items()}


def _output_among_short_chains() -> bNodeTree:
    """A three-node chain into a Group Output, a longer chain beside it,
    and eight unrelated pairs that make two columns tall."""
    tree = bNodeTree()
    a, b, c = (_plain(tree, name) for name in "abc")
    out = _plain(tree, "out", "NodeGroupOutput")
    for u, v in ((a, b), (b, c), (c, out)):
        tree.add_link(u.outputs[0], v.inputs[0])
    long = [_plain(tree, f"long{i}") for i in range(6)]
    for u, v in itertools.pairwise(long):
        tree.add_link(u.outputs[0], v.inputs[0])
    for i in range(8):
        u, v = _plain(tree, f"u{i}"), _plain(tree, f"v{i}")
        tree.add_link(u.outputs[0], v.inputs[0])
    return tree


def test_pinned_output_survives_height_balancing():
    """The balancing moves nodes left along with what feeds them; a pinned
    Group Output still ends up in the last column."""
    columns = _columns(_output_among_short_chains())
    assert columns["out"] == max(columns.values())


def test_any_node_can_be_held_to_the_first_or_last_column():
    tree = _output_among_short_chains()
    nodes = {node.name: node for node in tree.nodes}
    free = _columns(tree)
    assert free["a"] > min(free.values())
    assert free["u4"] > min(free.values())
    assert free["long0"] < max(free.values())

    nodes["v0"].layer = "last"
    nodes["long0"].layer = "last"  # has nodes after it: stays
    nodes["a"].layer = "first"
    nodes["u4"].layer = "first"
    # Not possible for a node with something after it: left where it is.
    nodes["b"].layer = "last"
    held = _columns(tree)

    assert held["v0"] == max(held.values())
    assert held["long0"] < held["long1"]
    assert held["a"] == held["u4"] == min(held.values())
    assert held["a"] < held["b"] < held["c"] < held["out"]


# ---------------------------------------------------------------------------
# Which links make the trunk
# ---------------------------------------------------------------------------


def test_main_sockets_give_a_chain_of_values_a_trunk():
    """With flow sockets only geometry-like links are straightened, so a
    chain of Math nodes is a staircase; with main sockets it is a row."""
    tree = _arranged(arrange_cases.value_chain)
    assert len(set(_tops(_by_type(tree, "ShaderNodeMath")))) > 1

    tree = _arranged(arrange_cases.value_chain, SugiyamaOptions(trunk_sockets="main"))
    assert len(set(_tops(_by_type(tree, "ShaderNodeMath")))) == 1


def test_main_socket_is_the_one_blender_picks():
    from nodebpy.lib.nodearrange.arrange.priority import main_socket

    node = bNode("n", "GeometryNodeSetPosition")
    kinds = ("Menu", "Bool", "Int", "FloatFactor", "Vector", "Color", "Geometry")
    sockets = [node.add_socket(False, idname=f"NodeSocket{kind}") for kind in kinds]
    for count in range(1, len(sockets) + 1):
        # Each type outranks all the ones before it.
        assert main_socket(sockets[:count]) is sockets[count - 1]
    # Among equals the first wins; odd sockets rank last.
    twice = [node.add_socket(False, idname="NodeSocketFloat") for _ in range(2)]
    assert main_socket(twice) is twice[0]
    virtual = node.add_socket(False, idname="NodeSocketVirtual")
    custom = node.add_socket(False, idname="MyCustomSocket")
    assert main_socket([virtual, custom, sockets[0]]) is sockets[0]
    assert main_socket([]) is None
