"""``muted(...)``: links that stay in the tree but pass nothing, and
``to_python`` writing them back."""

from pathlib import Path

import bpy
import pytest

from nodebpy import TreeBuilder, muted
from nodebpy import geometry as g
from nodebpy.builder import BundledLibrary
from nodebpy.builder._utils import socket_key
from nodebpy.export import to_python
from nodebpy.export.codegen import _effective_links


def _key(link) -> tuple[str, str, str, str]:
    return (
        link.from_node.name,
        socket_key(link.from_socket),
        link.to_node.name,
        socket_key(link.to_socket),
    )


def _muted(tree) -> list:
    return sorted(_key(link) for link in tree.links if link.is_muted)


def _round_trip(tree, **kwargs):
    code = to_python(tree, format=False, snapshot_positions=True, **kwargs)
    name = tree.name
    tree.name = f"__{name}_original"
    ns: dict = {}
    exec(code, ns)
    return code, bpy.data.node_groups[name]


def test_muted_mutes_the_link_from_its_source_wherever_it_is_passed():
    with TreeBuilder("MutedPaths", arrange=None) as tree:
        geo = tree.inputs.geometry("G")
        x = tree.inputs.float("X")
        moved = g.SetPosition(geometry=muted(geo), offset=g.CombineXYZ(z=x))
        joined = g.JoinGeometry([muted(moved), geo])
        offset = g.SetPosition(offset=(muted(x), 0, 0))
        muted(joined) >> offset >> tree.outputs.geometry("Out")
        capture = g.CaptureAttribute(geometry=geo)
        capture.items.new(muted(x), "X")

    assert _muted(tree.tree) == sorted(
        [
            ("Group Input", "G", "Set Position", "Geometry"),
            ("Set Position", "Geometry", "Join Geometry", "Geometry"),
            ("Group Input", "X", "Combine XYZ.001", "X"),
            ("Join Geometry", "Geometry", "Set Position.001", "Geometry"),
            ("Group Input", "X", "Capture Attribute", "X"),
        ]
    )
    # only the muted source's link: the other links stay live
    assert not any(
        link.is_muted
        for link in tree.tree.links
        if link.to_node.name == "Combine XYZ"
        or (
            link.to_node.name == "Join Geometry"
            and link.from_node.name == "Group Input"
        )
    )


def test_muted_value_sets_the_input_it_feeds():
    with TreeBuilder("MutedValue", arrange=None) as tree:
        x = tree.inputs.float("X")
        node = g.SetPosition(offset=muted(g.CombineXYZ(z=x), value=(0, 0, 1)))
        node >> tree.outputs.geometry("Out")
    assert tuple(node.node.inputs["Offset"].default_value) == (0, 0, 1)


def test_muted_takes_only_a_node_or_socket():
    with TreeBuilder("MutedBad", arrange=None):
        with pytest.raises(TypeError, match="node or socket"):
            muted(1.0)
        with pytest.raises(TypeError, match="node or socket"):
            muted((1.0, 2.0, 3.0))


def test_muting_waits_for_the_build_to_finish():
    """Muting at once would leave Mix's A unused (its factor reads 0), which
    the builder refuses to link into; the mute lands on exit instead."""
    with TreeBuilder("MutedLater", arrange=None) as tree:
        x = tree.inputs.float("X")
        mix = g.Mix.float(muted(x), 1.0, 2.0)
        assert not any(link.is_muted for link in tree.tree.links)
        mix >> tree.outputs.float("Out")
    assert [link.is_muted for link in tree.tree.links if link.to_node == mix.node] == [
        True
    ]


def test_to_python_writes_muted_links_and_rebuilds_them():
    with TreeBuilder("MutedRoundTrip", arrange=None) as tree:
        geo = tree.inputs.geometry("G")
        x = tree.inputs.float("X")
        moved = g.SetPosition(
            geometry=geo, offset=muted(g.CombineXYZ(z=x), value=(0, 0, 2))
        )
        compare = g.Compare.float.greater_than(muted(x), 0.5)
        joined = g.JoinGeometry([muted(moved), geo])
        g.DeleteGeometry(joined, selection=compare) >> tree.outputs.geometry("Out")
    want = _muted(tree.tree)

    code, rebuilt = _round_trip(tree.tree)
    assert "from nodebpy import geometry as g, TreeBuilder, muted" in code
    assert "value=(0.0, 0.0, 2.0)" in code
    assert _muted(rebuilt) == want
    offset = next(n for n in rebuilt.nodes if n.bl_idname == "GeometryNodeSetPosition")
    assert tuple(offset.inputs["Offset"].default_value) == (0, 0, 2)


def test_to_python_mutes_a_link_through_a_collapsed_reroute():
    with TreeBuilder("MutedReroute", arrange=None) as tree:
        geo = tree.inputs.geometry("G")
        reroute = g.Reroute(geo)
        g.SetPosition(geometry=reroute) >> tree.outputs.geometry("Out")
    link = next(link for link in tree.tree.links if link.to_node == reroute.node)
    link.is_muted = True

    code, rebuilt = _round_trip(tree.tree)
    assert "muted(" in code
    assert _muted(rebuilt) == [("Group Input", "G", "Set Position", "Geometry")]


def test_parity_compares_muted_links():
    pytest.importorskip("tree_clipper")
    from nodebpy.export.parity import compare_libraries, serialize_library

    with TreeBuilder("MutedParity", arrange=None) as tree:
        x = tree.inputs.float("X")
        (x + 1.0) >> tree.outputs.float("Out")
    before = serialize_library([tree.tree])
    tree.tree.links[0].is_muted = True
    after = serialize_library([tree.tree])
    findings = compare_libraries(before, after)
    assert {(f.path, f.detail) for f in findings} == {
        ("count", "2 -> 1"),
        ("muted count", "0 -> 1"),
    }


# ---------------------------------------------------------------------------
# Bundled assets with their links muted: every kind of node and link the
# exporter writes, muted, must come back muted. Each tree covers a path that
# once lost its mute: Compare's operator form, Mix inputs left unused by a
# muted factor, menus behind muted links, bundles, capture items, reroutes
# into Mix, and nodes Enable Output gates.
# ---------------------------------------------------------------------------

_ASSETS = [
    ("geometry_nodes_essentials.blend", "Box Selection"),
    ("geometry_nodes_essentials.blend", "Project with Depth"),
    ("procedural_hair_node_assets.blend", "Redistribute Curve Points"),
    ("procedural_hair_node_assets.blend", "Attachment Info"),
    ("procedural_hair_node_assets.blend", "Generate Hair Curves"),
    ("compositing_nodes_essentials.blend", "Film Grain"),
    ("geometry_nodes_dynamics_assets.blend", "Hair Dynamics"),
    ("geometry_nodes_dynamics_assets.blend", "Custom Force"),
]


@pytest.mark.parametrize("keep_reroutes", [True, False], ids=["reroutes", "collapsed"])
@pytest.mark.parametrize("every", [1, 2], ids=["all", "half"])
@pytest.mark.parametrize(
    ("library", "name"), _ASSETS, ids=[n.replace(" ", "_") for _, n in _ASSETS]
)
def test_assets_with_muted_links_round_trip(library, name, every, keep_reroutes):
    path = Path(BundledLibrary(library).path())
    if not path.is_file():
        pytest.skip(f"{library} not installed")
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(path), link=False, assets_only=True
    ) as (_, dst):
        dst.node_groups = [name]
    tree = dst.node_groups[0]
    tree.name = f"Muted {name} {every} {keep_reroutes}"
    for index, link in enumerate(tree.links):
        if index % every == 0:
            link.is_muted = True
    links = tree.links if keep_reroutes else _effective_links(tree)
    want = sorted(_key(link) for link in links if link.is_muted)

    _, rebuilt = _round_trip(tree, keep_reroutes=keep_reroutes)
    links = rebuilt.links if keep_reroutes else _effective_links(rebuilt)
    got = sorted(_key(link) for link in links if link.is_muted)
    # Muting links at random leaves trees Blender can fail to evaluate (Custom
    # Force with every link muted trips an unreachable branch in
    # geometry_nodes_lazy_function.cc), and the test fixture evaluates every
    # tree before saving: remove them.
    bpy.data.node_groups.remove(tree)
    bpy.data.node_groups.remove(rebuilt)
    assert got == want
