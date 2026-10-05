"""How the layout treats what is the user's in a Blender tree: its links
and reroutes, its selection, and links Blender calls invalid."""

import itertools

import bpy
import pytest

from nodebpy.lib.nodearrange import arrange_node_tree
from nodebpy.lib.nodearrange.arrange.edits import MoveNode
from nodebpy.lib.nodearrange.arrange.sugiyama import sugiyama_layout
from nodebpy.lib.nodearrange.config import Settings
from nodebpy.lib.nodearrange.extract import extract
from nodebpy.lib.nodearrange.metrics import measure

from . import arrange_cases

MARGIN = (50.0, 20.0)


def _links(tree) -> list[tuple[int, int, int]]:
    """Every link by the identity of its sockets, with its sort id."""
    return sorted(
        (
            link.from_socket.as_pointer(),
            link.to_socket.as_pointer(),
            link.multi_input_sort_id,
        )
        for link in tree.links
    )


def _locations(tree) -> dict[str, tuple[float, float]]:
    return {node.name: tuple(node.location_absolute) for node in tree.nodes}


# ---------------------------------------------------------------------------
# Positions only
# ---------------------------------------------------------------------------


def _long_links_into_a_join():
    """A chain a -> b -> c -> d -> join, with a, b and c each also linked
    straight to the join's multi-input: long links, in a set order."""
    tree = bpy.data.node_groups.new("LongJoin", "GeometryNodeTree")
    nodes = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(4)]
    join = tree.nodes.new("GeometryNodeJoinGeometry")
    for a, b in itertools.pairwise(nodes):
        tree.links.new(a.outputs[0], b.inputs[0])
    for node in (nodes[3], nodes[0], nodes[2], nodes[1]):
        tree.links.new(node.outputs[0], join.inputs[0])
    return tree


@pytest.mark.parametrize("case", ["long_join", "annotated", "long_links", "fan_in"])
def test_without_reroutes_only_nodes_move(case):
    """With ``add_reroutes=False`` the layout is positions only: every edit
    is a move, and the tree keeps its links (the same sockets, in the same
    order) and its reroutes."""
    ntree = (
        _long_links_into_a_join()
        if case == "long_join"
        else arrange_cases.CASES[case]()
    )
    arrange_cases.reset_locations(ntree)
    names = sorted(node.name for node in ntree.nodes)
    links = _links(ntree)

    result = sugiyama_layout(
        extract(ntree)[0], Settings(add_reroutes=False), MARGIN, verify=True
    )
    assert {type(edit) for edit in result.edits} == {MoveNode}

    arrange_node_tree(ntree, Settings(add_reroutes=False), MARGIN)
    assert sorted(node.name for node in ntree.nodes) == names
    assert _links(ntree) == links
    assert len(set(_locations(ntree).values())) > 1


def test_dangling_reroutes_are_kept():
    """With reroutes on, the layout replaces the reroutes it finds between
    two nodes, but not ones that lead nowhere or come from nowhere."""
    tree = bpy.data.node_groups.new("Dangling", "GeometryNodeTree")
    a, b = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(2))
    between, loose_end, no_source = (tree.nodes.new("NodeReroute") for _ in range(3))
    between.name, loose_end.name, no_source.name = "between", "loose_end", "no_source"
    tree.links.new(a.outputs[0], between.inputs[0])
    tree.links.new(between.outputs[0], b.inputs[0])
    tree.links.new(a.outputs[0], loose_end.inputs[0])
    tree.links.new(no_source.outputs[0], b.inputs["Offset"])

    arrange_node_tree(tree, Settings(add_reroutes=True), MARGIN)

    names = {node.name for node in tree.nodes}
    assert "between" not in names
    assert {"loose_end", "no_source"} <= names
    assert tree.nodes["loose_end"].inputs[0].is_linked
    assert tree.nodes["no_source"].outputs[0].is_linked
    assert b.inputs[0].links[0].from_node == a


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------


def _two_chains():
    tree = bpy.data.node_groups.new("TwoChains", "GeometryNodeTree")
    first = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(3)]
    second = [tree.nodes.new("GeometryNodeTransform") for _ in range(3)]
    for chain in (first, second):
        for a, b in itertools.pairwise(chain):
            tree.links.new(a.outputs[0], b.inputs[0])
    # The chains are joined, across what will be the selection's edge.
    tree.links.new(first[2].outputs[0], second[0].inputs[0])
    for i, node in enumerate(tree.nodes):
        node.location = (37.0 * i, -200.0 * i)
    return tree, first, second


def test_selected_only_moves_the_selection():
    tree, first, second = _two_chains()
    for node in tree.nodes:
        node.select = node in second
    before = _locations(tree)

    arrange_node_tree(tree, Settings(add_reroutes=False), MARGIN, selected_only=True)

    after = _locations(tree)
    for node in first:
        assert after[node.name] == before[node.name]
    xs = [after[node.name][0] for node in second]
    assert xs == sorted(xs) and len(set(xs)) == 3
    # In a row, centred on where the selection was.
    assert len({after[node.name][1] for node in second}) == 1
    centre = sum(before[node.name][0] for node in second) / 3
    assert sum(xs) / 3 == pytest.approx(centre, abs=1.0)


def test_selected_only_with_nothing_selected_does_nothing():
    tree, *_ = _two_chains()
    for node in tree.nodes:
        node.select = False
    before = _locations(tree)

    arrange_node_tree(tree, Settings(), MARGIN, selected_only=True)

    assert _locations(tree) == before


def test_selection_is_ignored_unless_asked_for():
    tree, *_ = _two_chains()
    for node in tree.nodes:
        node.select = False
    before = _locations(tree)

    arrange_node_tree(tree, Settings(add_reroutes=False), MARGIN)

    assert _locations(tree) != before
    plain, _ = extract(tree)
    assert all(node.select for node in plain.nodes)
    chosen, _ = extract(tree, selected_only=True)
    assert not any(node.select for node in chosen.nodes)


def test_selected_reroutes_at_the_edge_of_the_selection_are_kept():
    """A selected reroute whose other end is not selected looks dangling
    from inside the selection, and is left in place."""
    tree = bpy.data.node_groups.new("EdgeReroute", "GeometryNodeTree")
    a, b = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(2))
    reroute = tree.nodes.new("NodeReroute")
    tree.links.new(a.outputs[0], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], b.inputs[0])
    a.select = False
    links = _links(tree)

    arrange_node_tree(tree, Settings(add_reroutes=True), MARGIN, selected_only=True)

    assert reroute.name in tree.nodes
    assert _links(tree) == links


# ---------------------------------------------------------------------------
# Links Blender calls invalid
# ---------------------------------------------------------------------------


def test_invalid_link_still_orders_its_nodes():
    """The annotated case links a reroute carrying a field to an input that
    takes none. Blender marks the link invalid and still draws it; the
    layout keeps its target to the right of its source."""
    tree = arrange_cases.annotated()
    arrange_cases.reset_locations(tree)
    invalid = [link for link in tree.links if not link.is_valid]
    assert len(invalid) == 1
    source, target = invalid[0].from_node, invalid[0].to_node

    arrange_node_tree(tree, Settings(add_reroutes=False), MARGIN)

    assert source.location_absolute.x < target.location_absolute.x


# ---------------------------------------------------------------------------
# Reroutes only where a link is blocked
# ---------------------------------------------------------------------------


def _reroutes(tree) -> list[str]:
    return sorted(n.name for n in tree.nodes if n.bl_idname == "NodeReroute")


def _arranged(case, **settings):
    from nodebpy.lib.nodearrange.metrics import measure

    tree = arrange_cases.CASES[case]()
    arrange_cases.reset_locations(tree)
    arrange_node_tree(
        tree, Settings(direction="BALANCED", **settings), MARGIN, verify=True
    )
    return tree, measure(tree)


@pytest.mark.parametrize("case", ["long_links", "fan_in", "framed_stages"])
def test_blocked_links_are_routed_around_nodes(case):
    """``reroute_links="blocked"`` leaves no link drawn across a node, as
    routing every long link does, without adding more reroutes than that."""
    _, unrouted = _arranged(case, add_reroutes=False)
    _, blocked = _arranged(case, add_reroutes=True, reroute_links="blocked")
    _, long = _arranged(case, add_reroutes=True, reroute_links="long")

    assert blocked.links_through_nodes == 0
    assert blocked.node_overlaps == 0
    assert blocked.reroutes <= long.reroutes
    if unrouted.links_through_nodes:
        assert blocked.reroutes > unrouted.reroutes


def test_clear_long_links_get_no_reroutes():
    """In this tree the long links pass clear of every node, so nothing is
    added, where routing every long link adds reroutes."""
    tree, blocked = _arranged(
        "trunk_with_feeders", add_reroutes=True, reroute_links="blocked"
    )
    _, unrouted = _arranged("trunk_with_feeders", add_reroutes=False)

    assert blocked.links_through_nodes == unrouted.links_through_nodes == 0
    assert _reroutes(tree) == []


def test_blocked_mode_keeps_the_trees_own_reroutes():
    before = _reroutes(arrange_cases.annotated())
    assert len(before) == 2

    tree, _ = _arranged("annotated", add_reroutes=True, reroute_links="blocked")
    assert set(before) <= set(_reroutes(tree))
    # Still wired as they were: the first feeds the labelled second.
    first, second = (tree.nodes[name] for name in before)
    if second.label != "offset":
        first, second = second, first
    assert second.inputs[0].links[0].from_node == first


def test_reroute_links_option_on_the_public_api():
    from nodebpy import SugiyamaOptions, arrange
    from nodebpy.lib.nodearrange.metrics import measure

    tree = arrange_cases.long_links()
    arrange_cases.reset_locations(tree)
    arrange(tree, SugiyamaOptions(add_reroutes=True, reroute_links="blocked"))
    assert measure(tree).links_through_nodes == 0


def test_link_is_clear():
    from nodebpy.lib.nodearrange.arrange.graph import Kind, Node, Socket
    from nodebpy.lib.nodearrange.arrange.sugiyama import link_is_clear

    def box(x: float, top: float, width: float = 100.0, height: float = 100.0):
        v = Node(type=Kind.DUMMY)
        v.x, v.y, v.width, v.height = x, top, width, height
        return v

    source, target = box(0.0, 0.0), box(600.0, 0.0)
    start, end = Socket(source, 0, True), Socket(target, 0, False)

    assert link_is_clear(start, end, [source, target])
    # A node on the way, one well off it, and one beyond the far end.
    assert not link_is_clear(start, end, [box(300.0, 50.0)])
    assert link_is_clear(start, end, [box(300.0, 300.0), box(300.0, -200.0)])
    assert link_is_clear(start, end, [box(900.0, 50.0)])
    # A link that only dips where the curve bends still hits what is there.
    low = box(600.0, -400.0)
    dipping = Socket(low, 0, False)
    assert not link_is_clear(start, dipping, [box(250.0, -150.0)])
    assert link_is_clear(start, dipping, [box(250.0, 300.0)])
    # Too close to count as clear: within the clearance of the socket.
    assert not link_is_clear(start, end, [box(102.0, 50.0, width=20.0)])


def test_zones_are_read_from_blender():
    """Python only sees which output node a zone's input node is paired
    with; the nodes inside are worked out when the tree is read."""
    tree = arrange_cases.zones()
    data, _ = extract(tree)
    zones = {zone.input_node.idname: zone for zone in data.zones}
    assert sorted(zones) == ["GeometryNodeRepeatInput", "GeometryNodeSimulationInput"]
    simulation = zones["GeometryNodeSimulationInput"]
    assert simulation.output_node.idname == "GeometryNodeSimulationOutput"
    assert [n.idname for n in simulation.child_nodes] == ["GeometryNodeSetPosition"]
    assert [n.idname for n in zones["GeometryNodeRepeatInput"].child_nodes] == [
        "GeometryNodeSubdivideMesh",
        "GeometryNodeSetShadeSmooth",
    ]

    arrange_node_tree(tree, Settings())
    metrics = measure(tree)
    assert (metrics.zones, metrics.level_zones) == (2, 2)
