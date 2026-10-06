"""``sugiyama_layout`` on plain data: a ``dna.bNodeTree`` in, edits out."""

import ast
import random
from pathlib import Path

import pytest
from mathutils.geometry import intersect_line_line_2d

from nodebpy import layout
from nodebpy.layout.common import (
    REROUTE_MARGIN_Y_FAC,
    f32,
    group_by,
    segments_intersect,
)
from nodebpy.layout.config import LayoutState, SugiyamaOptions
from nodebpy.layout.dna import REROUTE_SIZE, bNode, bNodeTree, new_reroute
from nodebpy.layout.edits import (
    AddLink,
    AddReroute,
    MoveNode,
    RemoveNode,
    ResizeFrame,
)
from nodebpy.layout.model import Kind, Node, Socket
from nodebpy.layout.placement import separation
from nodebpy.layout.reroutes import link_is_clear
from nodebpy.layout.sugiyama import sugiyama_layout

from .data import MARGIN, options, plain_chain, plain_node
from .metrics import measure

_PACKAGE = Path(layout.__file__).parent
_BLENDER_SIDE = {"__init__", "api", "apply", "extract", "node_size"}


def _imports(module: Path) -> set[str]:
    """The top-level packages *module* imports, and the names it imports
    from this package."""
    imported = set()
    for node in ast.walk(ast.parse(module.read_text())):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
            imported.update(alias.name for alias in node.names)
    return imported


@pytest.mark.parametrize(
    "module", sorted(_PACKAGE.glob("*.py")), ids=lambda path: path.name
)
def test_layout_modules_do_not_import_blender(module):
    """No module imports ``networkx``, and only the Blender-side modules
    import ``bpy``, ``mathutils``, ``blf`` or each other."""
    imported = _imports(module)
    assert "networkx" not in imported
    if module.stem not in _BLENDER_SIDE:
        assert not imported & {"bpy", "mathutils", "blf", *_BLENDER_SIDE}


def test_chain_is_one_row():
    """A chain is laid out left to right in one row, a margin apart, centred
    where the nodes were, and the tree itself is not changed."""
    tree = bNodeTree()
    a, b, c = plain_chain(tree, "abc").values()

    result = sugiyama_layout(tree, options())

    assert all(isinstance(edit, MoveNode) for edit in result.edits)
    positions = result.positions()
    assert positions[b][0] - positions[a][0] == pytest.approx(140.0 + MARGIN[0])
    assert positions[c][0] - positions[b][0] == pytest.approx(140.0 + MARGIN[0])
    assert positions[a][1] == positions[b][1] == positions[c][1]
    assert positions[b][0] == pytest.approx(0.0)
    assert a.location == (0.0, 0.0)
    assert len(tree.links) == 2


def test_tree_without_nodes_to_place_needs_no_edits():
    assert sugiyama_layout(bNodeTree()).edits == []
    only_frame = bNodeTree()
    only_frame.add_node(bNode("Frame", "NodeFrame"))
    assert sugiyama_layout(only_frame).edits == []


def test_nodes_stay_in_their_frames():
    tree = bNodeTree()
    frame = tree.add_node(bNode("Frame", "NodeFrame", label="Stage"))
    a = plain_node(tree, "a")
    b = plain_node(tree, "b", parent=frame)
    c = plain_node(tree, "c", parent=frame)
    tree.add_link(a.outputs[0], b.inputs[0])
    tree.add_link(b.outputs[0], c.inputs[0])

    result = sugiyama_layout(tree)
    parents = {e.node: e.parent for e in result.edits if isinstance(e, MoveNode)}
    assert parents == {a: None, b: frame, c: frame}


def test_linked_socket_without_a_location_is_reported():
    tree = bNodeTree()
    a, b = plain_chain(tree, "ab").values()
    b.inputs[0].location = None

    with pytest.raises(ValueError, match=r"'b'.*input 0 has no location"):
        sugiyama_layout(tree, options())


def test_gap_between_dummy_nodes_is_a_fraction_of_the_margin():
    state = LayoutState(
        bNodeTree(), SugiyamaOptions(margin=(30.0, 40.0), snap_to_grid=False)
    )
    dummy_a, dummy_b = Node(type=Kind.DUMMY), Node(type=Kind.DUMMY)
    real = Node(bNode("Index", "GeometryNodeInputIndex"))

    def gap(u, w):
        return separation(u, u, w, state) - u.height

    assert gap(dummy_a, dummy_b) == pytest.approx(40.0 * REROUTE_MARGIN_Y_FAC)
    assert gap(real, dummy_a) == pytest.approx(40.0)
    assert gap(dummy_b, real) == pytest.approx(40.0)


# ---------------------------------------------------------------------------
# Reroutes
# ---------------------------------------------------------------------------


def _long_link() -> tuple[bNodeTree, list[bNode]]:
    """a -> b -> c -> d, and a link from a straight to d."""
    tree = bNodeTree()
    nodes = list(plain_chain(tree, "abcd", inputs=2).values())
    tree.add_link(nodes[0].outputs[0], nodes[3].inputs[1])
    return tree, nodes


def test_without_reroutes_a_long_link_only_moves_nodes():
    tree, _ = _long_link()
    result = sugiyama_layout(tree, options(reroutes="none"))
    assert {type(edit) for edit in result.edits} == {MoveNode}


def test_long_link_becomes_a_chain_of_reroutes():
    """With ``reroutes="all"`` the edits create the reroutes, then link
    them from the source to the target, and place them."""
    tree, nodes = _long_link()

    result = sugiyama_layout(tree, options(reroutes="all"))

    reroutes = [e.node for e in result.edits if isinstance(e, AddReroute)]
    assert reroutes
    assert all(node.is_reroute() and node.parent is None for node in reroutes)
    links = [e for e in result.edits if isinstance(e, AddLink)]
    assert links[0].fromsock is nodes[0].outputs[0]
    assert links[-1].tosock is nodes[3].inputs[1]
    assert {e.tosock.node for e in links[:-1]} == set(reroutes)
    assert set(reroutes) <= set(result.positions())
    created = result.edits.index(AddReroute(reroutes[0]))
    assert created < result.edits.index(links[0])


def _through_a_reroute(label: str = "") -> tuple[bNodeTree, bNode, bNode, bNode]:
    """a -> reroute -> b."""
    tree = bNodeTree()
    a, b = plain_node(tree, "a"), plain_node(tree, "b")
    reroute = tree.add_node(new_reroute())
    reroute.name, reroute.label = "Reroute", label
    tree.add_link(a.outputs[0], reroute.inputs[0])
    tree.add_link(reroute.outputs[0], b.inputs[0])
    return tree, a, reroute, b


def test_reroute_on_a_short_link_is_removed():
    tree, a, reroute, b = _through_a_reroute()

    result = sugiyama_layout(tree, options(reroutes="all"))

    assert RemoveNode(reroute) in result.edits
    assert AddLink(a.outputs[0], b.inputs[0]) in result.edits
    assert reroute not in result.positions()


def test_labelled_reroute_is_kept():
    tree, _, reroute, _ = _through_a_reroute(label="keep me")

    result = sugiyama_layout(tree, options(reroutes="all"))

    assert not any(isinstance(e, RemoveNode) for e in result.edits)
    assert reroute in result.positions()


def test_new_reroute_has_one_input_and_one_output():
    reroute = new_reroute()
    assert reroute.is_reroute() and not reroute.is_frame()
    assert (len(reroute.inputs), len(reroute.outputs)) == (1, 1)
    assert reroute.width == REROUTE_SIZE
    assert reroute.top - reroute.bottom == REROUTE_SIZE
    assert reroute.outputs[0].is_output and reroute.outputs[0].node is reroute
    assert "NodeReroute" in repr(reroute)


def test_link_passing_under_a_wider_node_gets_a_bend_point():
    """s -> wide -> t in one row, and v, below ``wide`` in its column, also
    feeds t. The link from v rises under ``wide``, which reaches further
    right than v: it gets a reroute at the right edge of the column, level
    with v's output. The links along the row get none."""
    tree = bNodeTree()
    s = plain_node(tree, "s")
    wide = plain_node(tree, "wide", width=400.0)
    v = plain_node(tree, "v")
    t = plain_node(tree, "t", inputs=2)
    tree.add_link(s.outputs[0], wide.inputs[0])
    tree.add_link(wide.outputs[0], t.inputs[0])
    tree.add_link(v.outputs[0], t.inputs[1])

    result = sugiyama_layout(tree, options(reroutes="all"), verify=True)

    (reroute,) = (e.node for e in result.edits if isinstance(e, AddReroute))
    assert [e for e in result.edits if isinstance(e, AddLink)] == [
        AddLink(v.outputs[0], reroute.inputs[0]),
        AddLink(reroute.outputs[0], t.inputs[1]),
    ]
    positions = result.positions()
    assert positions[wide][1] == positions[t][1] > positions[v][1]
    assert positions[reroute][0] == pytest.approx(positions[wide][0] + 400.0)
    output_y = positions[v][1] + v.outputs[0].location[1]
    assert positions[reroute][1] == pytest.approx(output_y, abs=REROUTE_SIZE)


def test_link_is_clear_of_nodes_off_its_curve():
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
    # Within the clearance of the socket.
    assert not link_is_clear(start, end, [box(102.0, 50.0, width=20.0)])


def test_result_with_reroutes_applies_to_the_plain_tree():
    """Applied to the plain tree, a result that removes a reroute and adds
    others leaves every link between nodes of the tree and no nodes
    overlapping. The edit refitting a frame changes nothing there."""
    tree, nodes = _long_link()
    frame = tree.add_node(bNode("Frame", "NodeFrame", shrink=False))
    nodes[1].parent = frame
    old = tree.add_node(new_reroute())
    old.name = "old"
    tail = plain_node(tree, "tail")
    tree.add_link(nodes[3].outputs[0], old.inputs[0])
    tree.add_link(old.outputs[0], tail.inputs[0])

    result = sugiyama_layout(tree, options(reroutes="all"))
    result.apply_to(tree)

    added = [edit.node for edit in result.edits if isinstance(edit, AddReroute)]
    assert added and set(added) <= set(tree.nodes)
    assert old not in tree.nodes
    assert ResizeFrame(frame, (nodes[1],)) in result.edits
    assert all(
        link.fromnode in tree.nodes and link.tonode in tree.nodes for link in tree.links
    )
    assert any(link.fromnode is nodes[3] and link.tonode is tail for link in tree.links)
    assert measure(tree).node_overlaps == 0


# ---------------------------------------------------------------------------
# Helpers of the layout
# ---------------------------------------------------------------------------


def test_f32_rounds_to_single_precision():
    assert f32(0.5) == 0.5
    assert f32(0.1) != 0.1
    assert f32(0.1) == pytest.approx(0.1, abs=1e-8)
    assert f32(f32(0.1)) == f32(0.1)


def test_group_by_maps_each_group_to_its_key():
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
    """Same answers as ``mathutils.geometry.intersect_line_line_2d`` on
    random segments, many of them touching or collinear."""
    rng = random.Random(7)
    for _ in range(3000):
        segments = [
            (rng.randint(0, 6) * 20.0, rng.randint(0, 6) * 20.0) for _ in range(4)
        ]
        if rng.random() < 0.5:
            segments = [
                (x + rng.uniform(-1, 1), y + rng.uniform(-1, 1)) for x, y in segments
            ]
        expected = intersect_line_line_2d(*segments) is not None
        assert segments_intersect(*segments) is expected, segments
