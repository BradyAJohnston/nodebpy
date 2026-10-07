"""Reading a Blender tree into plain data (``extract``) and carrying a
layout out on it (``apply``): frames, reroutes, links Blender calls
invalid, and the selection."""

import itertools

import bpy
import pytest

from nodebpy import TreeBuilder, arrange
from nodebpy import geometry as g
from nodebpy.layout import sugiyama
from nodebpy.layout.apply import apply
from nodebpy.layout.dna import new_reroute
from nodebpy.layout.edits import (
    AddLink,
    AddReroute,
    LayoutResult,
    MoveNode,
    RemoveLink,
    RemoveNode,
    ResizeFrame,
    RestoreMultiInputOrder,
)
from nodebpy.layout.extract import extract
from nodebpy.layout.node_size import get_bottom
from nodebpy.layout.sugiyama import sugiyama_layout

from . import cases
from .data import options
from .metrics import measure


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


def _reroutes(tree) -> list[str]:
    return sorted(n.name for n in tree.nodes if n.bl_idname == "NodeReroute")


# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------


def test_extract_copies_nodes_frames_sockets_and_links():
    ntree = cases.nested_frames()
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
    ntree = cases.diamond()
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


def test_extract_reads_socket_types():
    tree, _ = extract(cases.chain())
    cube = next(n for n in tree.nodes if n.idname == "GeometryNodeMeshCube")
    assert cube.outputs[0].idname == "NodeSocketGeometry"
    assert not cube.is_group_input() and not cube.is_group_output()


def test_extract_reads_the_selection():
    ntree = cases.chain()
    for node in ntree.nodes:
        node.select = False
    ntree.nodes[0].select = True

    tree, _ = extract(ntree)

    assert [node.select for node in tree.nodes] == [True, False, False, False, False]


def test_zones_are_read_from_blender():
    """Python only sees which output node a zone's input node is paired
    with; the nodes inside are worked out when the tree is read."""
    tree = cases.zones()
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

    arrange(tree)
    metrics = measure(tree)
    assert (metrics.zones, metrics.level_zones) == (2, 2)


def test_link_into_a_closed_panel_puts_its_source_before_its_target():
    """A socket in a closed panel is not drawn; a link into it is extracted
    all the same."""
    with TreeBuilder("PanelInner", arrange=None) as inner:
        geo = inner.inputs.geometry()
        with inner.inputs.panel("Tuning", default_closed=True):
            factor = inner.inputs.float("Factor", 1.0)
        g.SetPosition(geometry=geo, offset=g.CombineXYZ(x=factor)) >> (
            inner.outputs.geometry()
        )

    with TreeBuilder("PanelOuter", arrange=None) as outer:
        group = g.Group()
        group.node.node_tree = inner.tree
        outer.inputs.geometry() >> group.i["Geometry"]
        producer = g.Math.add(g.Value(1.0), 2.0)
        producer >> group.i["Factor"]
        group.o["Geometry"] >> outer.outputs.geometry()

    arrange(outer.tree)
    assert producer.node.location.x + producer.node.width < group.node.location.x


def test_invalid_link_still_orders_its_nodes():
    """The annotated case links a reroute carrying a field to an input that
    takes none. Blender marks the link invalid and still draws it; the
    layout keeps its target to the right of its source."""
    tree = cases.annotated()
    cases.reset_locations(tree)
    invalid = [link for link in tree.links if not link.is_valid]
    assert len(invalid) == 1
    source, target = invalid[0].from_node, invalid[0].to_node

    arrange(tree, options(reroutes="none"))

    assert source.location_absolute.x < target.location_absolute.x


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------


def test_apply_carries_out_each_kind_of_edit():
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

    # The new reroute takes the name of the one removed.
    names = {n.name for n in ntree.nodes}
    assert "Reroute" in names and len(names) == 5
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


def test_layout_failure_leaves_the_tree_untouched(monkeypatch):
    """The layout is computed in full before anything is applied: an error
    in its last step leaves every node and link as it was."""
    ntree = cases.long_links()
    reroute = ntree.nodes.new("NodeReroute")
    source = next(n for n in ntree.nodes if n.bl_idname == "ShaderNodeMath")
    target = next(n for n in ntree.nodes if n.bl_idname == "GeometryNodeSetPosition")
    ntree.links.new(source.outputs[0], reroute.inputs[0])
    ntree.links.new(reroute.outputs[0], target.inputs["Selection"])
    before = (_locations(ntree), _links(ntree))

    def boom(*args, **kwargs):
        raise RuntimeError("late failure")

    monkeypatch.setattr(sugiyama, "realize_layout", boom)
    with pytest.raises(RuntimeError, match="late failure"):
        arrange(ntree, options(reroutes="all"))

    assert (_locations(ntree), _links(ntree)) == before


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
    """With ``reroutes="none"`` every edit is a move, and the tree keeps
    its reroutes and its links: the same sockets, in the same order."""
    ntree = _long_links_into_a_join() if case == "long_join" else cases.CASES[case]()
    cases.reset_locations(ntree)
    names = sorted(node.name for node in ntree.nodes)
    links = _links(ntree)

    result = sugiyama_layout(extract(ntree)[0], options(reroutes="none"), verify=True)
    assert {type(edit) for edit in result.edits} == {MoveNode}

    arrange(ntree, options(reroutes="none"))
    assert sorted(node.name for node in ntree.nodes) == names
    assert _links(ntree) == links
    assert len(set(_locations(ntree).values())) > 1


@pytest.mark.parametrize("nested", [False, True], ids=["nodes", "frame"])
def test_frame_that_does_not_shrink_is_fitted_around_its_nodes(nested):
    """A frame with Shrink off is sized around the nodes in it, or in the
    frame it holds, where the layout put them, and Shrink stays off."""
    tree = cases.framed_stages()
    cases.reset_locations(tree)
    frame = next(n for n in tree.nodes if n.bl_idname == "NodeFrame")
    members = [n for n in tree.nodes if n.parent == frame]
    if nested:
        inner, frame = frame, tree.nodes.new("NodeFrame")
        inner.parent = frame
    frame.shrink = False
    frame.width = frame.height = 10.0

    arrange(tree, options())

    assert frame.shrink is False
    left, top = frame.location_absolute
    assert left < min(n.location_absolute.x for n in members)
    assert left + frame.width > max(n.location_absolute.x + n.width for n in members)
    assert top > max(n.location_absolute.y for n in members)
    assert top - frame.height < min(get_bottom(n) for n in members)
    assert all(n.parent.parent == frame for n in members) == nested


# ---------------------------------------------------------------------------
# Reroutes
# ---------------------------------------------------------------------------


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

    arrange(tree, options(reroutes="all"))

    names = {node.name for node in tree.nodes}
    assert "between" not in names
    assert {"loose_end", "no_source"} <= names
    assert tree.nodes["loose_end"].inputs[0].is_linked
    assert tree.nodes["no_source"].outputs[0].is_linked
    assert b.inputs[0].links[0].from_node == a


def test_source_feeding_a_multi_input_directly_and_through_reroutes_keeps_both():
    """Set Position feeds the join directly and through a chain of reroutes
    alone in a frame. Linking the source straight to the join in place of
    the chain would merge the two links."""
    with TreeBuilder("RerouteCluster", arrange=None) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        sp = g.SetPosition(geometry=geo)
        chain = [tree.tree.nodes.new("NodeReroute") for _ in range(3)]
        frame = tree.tree.nodes.new("NodeFrame")
        tree.tree.links.new(sp.node.outputs[0], chain[0].inputs[0])
        for a, b in itertools.pairwise(chain):
            tree.tree.links.new(a.outputs[0], b.inputs[0])
            a.parent = frame
            b.parent = frame
        join = g.JoinGeometry(geometry=[sp])
        tree.tree.links.new(chain[-1].outputs[0], join.node.inputs[0])
        join >> out

    arrange(tree.tree, options(reroutes="all"))

    into_join = [link for link in tree.tree.links if link.to_node == join.node]
    assert len(into_join) == 2
    assert all(link.from_node.bl_idname == "NodeReroute" for link in into_join)


@pytest.mark.parametrize("case", ["long_links", "framed_stages", "shader_material"])
def test_blocked_links_are_routed_around_nodes(case):
    """Each of these trees has a link drawn across a node when laid out
    without reroutes. ``reroutes="blocked"`` leaves none, with no more
    reroutes than ``reroutes="all"`` adds."""
    unrouted = measure(cases.arranged(case, options(reroutes="none")))
    blocked = measure(cases.arranged(case, options(reroutes="blocked")))
    every = measure(cases.arranged(case, options(reroutes="all")))

    assert unrouted.links_through_nodes > 0
    assert blocked.links_through_nodes == 0
    assert blocked.node_overlaps == 0
    assert unrouted.reroutes < blocked.reroutes <= every.reroutes


def test_clear_long_links_get_no_reroutes():
    """The long links of the zones case pass clear of every node:
    ``"blocked"`` adds nothing where ``"all"`` adds reroutes."""
    unrouted = measure(cases.arranged("zones", options()))
    blocked = cases.arranged("zones", options(reroutes="blocked"))
    every = cases.arranged("zones", options(reroutes="all"))

    assert unrouted.links_through_nodes == 0
    assert _reroutes(blocked) == []
    assert _reroutes(every) != []


def test_blocked_mode_keeps_the_trees_own_reroutes():
    before = _reroutes(cases.annotated())
    assert len(before) == 2

    tree = cases.arranged("annotated", options(reroutes="blocked"))
    assert set(before) <= set(_reroutes(tree))
    # Still wired as they were: the first feeds the labelled second.
    first, second = (tree.nodes[name] for name in before)
    if second.label != "offset":
        first, second = second, first
    assert second.inputs[0].links[0].from_node == first


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------


def _two_chains():
    """Two chains of three, the end of the first linked to the start of
    the second, scattered."""
    tree = bpy.data.node_groups.new("TwoChains", "GeometryNodeTree")
    first = [tree.nodes.new("GeometryNodeSetPosition") for _ in range(3)]
    second = [tree.nodes.new("GeometryNodeTransform") for _ in range(3)]
    for chain in (first, second):
        for a, b in itertools.pairwise(chain):
            tree.links.new(a.outputs[0], b.inputs[0])
    tree.links.new(first[2].outputs[0], second[0].inputs[0])
    for i, node in enumerate(tree.nodes):
        node.location = (37.0 * i, -200.0 * i)
    return tree, first, second


def test_selected_only_moves_the_selection():
    """The selected chain becomes a row centred where it was; the other
    nodes stay."""
    tree, first, second = _two_chains()
    for node in tree.nodes:
        node.select = node in second
    before = _locations(tree)

    arrange(tree, options(reroutes="none"), selected_only=True)

    after = _locations(tree)
    for node in first:
        assert after[node.name] == before[node.name]
    xs = [after[node.name][0] for node in second]
    assert xs == sorted(xs) and len(set(xs)) == 3
    assert len({after[node.name][1] for node in second}) == 1
    centre = sum(before[node.name][0] for node in second) / 3
    assert sum(xs) / 3 == pytest.approx(centre, abs=0.01)


def test_selected_only_with_nothing_selected_does_nothing():
    tree, *_ = _two_chains()
    for node in tree.nodes:
        node.select = False
    before = _locations(tree)

    arrange(tree, options(), selected_only=True)

    assert _locations(tree) == before


def test_unselected_nodes_are_arranged_unless_selected_only():
    tree, first, _ = _two_chains()
    for node in tree.nodes:
        node.select = False

    arrange(tree, options(reroutes="none"))

    assert len({node.location.y for node in first}) == 1


def test_selected_reroute_at_the_edge_of_the_selection_is_kept():
    """A selected reroute fed by an unselected node is not replaced."""
    tree = bpy.data.node_groups.new("EdgeReroute", "GeometryNodeTree")
    a, b = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(2))
    reroute = tree.nodes.new("NodeReroute")
    tree.links.new(a.outputs[0], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], b.inputs[0])
    a.select = False
    links = _links(tree)

    arrange(tree, options(reroutes="all"), selected_only=True)

    assert reroute.name in tree.nodes
    assert _links(tree) == links


@pytest.mark.parametrize("unselected", ["source", "consumer"])
def test_reroute_that_also_links_outside_the_selection_is_kept(unselected):
    """a -> reroute -> b and reroute -> c. With a or c unselected the
    reroute is not replaced: that node would lose its link."""
    tree = bpy.data.node_groups.new("SharedReroute", "GeometryNodeTree")
    a, b, c = (tree.nodes.new("GeometryNodeSetPosition") for _ in range(3))
    reroute = tree.nodes.new("NodeReroute")
    tree.links.new(a.outputs[0], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], b.inputs[0])
    tree.links.new(reroute.outputs[0], c.inputs[0])
    {"source": a, "consumer": c}[unselected].select = False
    links = _links(tree)

    arrange(tree, options(reroutes="all"), selected_only=True)

    assert reroute.name in tree.nodes
    assert _links(tree) == links
