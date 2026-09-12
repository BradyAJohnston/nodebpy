"""Tests for the unified arrange() API and its options."""

import itertools
from pathlib import Path

import bpy
import pytest

from nodebpy import SimpleOptions, SugiyamaOptions, TreeBuilder, arrange
from nodebpy import geometry as g
from nodebpy.builder import BundledLibrary
from nodebpy.builder.layout import calculate_socket_offset_y


def _build_chain(name: str, arrange_method=None) -> TreeBuilder:
    with TreeBuilder(name, arrange=arrange_method) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out
    return tree


def test_arrange_standalone_without_builder_context():
    """arrange() works on a plain node tree, outside any TreeBuilder context."""
    builder = _build_chain("StandaloneArrange")
    tree = builder.tree
    for node in tree.nodes:
        node.location = (0, 0)

    assert not TreeBuilder._tree_contexts
    arrange(tree)

    xs = {round(n.location.x) for n in tree.nodes}
    assert len(xs) > 1, "nodes should be spread horizontally"


def test_arrange_ignores_selection_state():
    """arrange() lays out the whole tree even when no node is selected —
    a library-loaded tree has no selection, and the addon-derived layout
    code used to silently arrange nothing (and drop every link whose
    consumer was unselected)."""
    builder = _build_chain("UnselectedArrange")
    tree = builder.tree
    for node in tree.nodes:
        node.select = False
        node.location = (0, 0)

    arrange(tree)

    xs = {round(n.location.x) for n in tree.nodes}
    assert len(xs) > 1, "unselected nodes should still be spread horizontally"


def test_hidden_sockets_do_not_add_height():
    """Sockets hidden by the editor's Hide Unused Sockets (hide=True and
    unlinked) don't occupy rows; hidden-but-linked sockets still do."""
    from nodebpy.builder.layout import calculate_node_dimensions

    builder = _build_chain("HiddenSockets")
    node = builder.tree.nodes["Set Position"]

    full = calculate_node_dimensions(node)[1]
    for socket in node.inputs:
        if not socket.is_linked:
            socket.hide = True
    reduced = calculate_node_dimensions(node)[1]
    assert reduced < full

    for socket in node.inputs:
        socket.hide = True  # linked sockets stay drawn regardless
    assert calculate_node_dimensions(node)[1] == reduced


def test_arrange_none_leaves_tree_untouched():
    builder = _build_chain("NoArrange")
    tree = builder.tree
    for node in tree.nodes:
        node.location = (12.0, 34.0)
    arrange(tree, None)
    assert all(tuple(n.location) == (12.0, 34.0) for n in tree.nodes)


def test_simple_options_spacing():
    """SimpleOptions.spacing controls the column gap of the simple layout."""
    narrow = _build_chain("SimpleNarrow", SimpleOptions(spacing=(10, 10)))
    wide = _build_chain("SimpleWide", SimpleOptions(spacing=(300, 10)))

    def column_pitch(tree):
        xs = sorted({n.location.x for n in tree.tree.nodes})
        return xs[1] - xs[0]

    assert column_pitch(wide) > column_pitch(narrow)


def test_sugiyama_options_margin():
    narrow = _build_chain("SugiyamaNarrow", SugiyamaOptions(margin=(50, 20)))
    wide = _build_chain("SugiyamaWide", SugiyamaOptions(margin=(400, 20)))

    def spread(tree):
        xs = [n.location.x for n in tree.tree.nodes]
        return max(xs) - min(xs)

    assert spread(wide) > spread(narrow)


def test_sugiyama_options_optimize_sizes():
    """optimize_sizes fits collapsed-node widths to their display name."""
    with TreeBuilder(
        "OptimizeSizes", arrange=SugiyamaOptions(optimize_sizes=True)
    ) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        a = g.Value()
        b = (a + 1.0) * 2.0
        _ = geo >> g.SetPosition(offset=g.CombineXYZ(x=b, y=b)) >> out
        for node in tree.tree.nodes:
            if node.bl_idname == "ShaderNodeMath":
                node.hide = True

    widths = {n.width for n in tree.tree.nodes if n.bl_idname == "ShaderNodeMath"}
    # ADD and MULTIPLY have different display names, so widths get fitted
    # individually (default width would be a single shared 140.0).
    assert 140.0 not in widths


def test_sugiyama_default_adds_no_reroutes():
    builder = _build_chain("NoReroutes", "sugiyama")
    assert not any(n.bl_idname == "NodeReroute" for n in builder.tree.nodes), (
        "default arrangement must not change the authored structure"
    )


def test_sugiyama_add_reroutes_option():
    """add_reroutes=True is available for users who want routed edges."""
    with TreeBuilder(
        "WithReroutes", arrange=SugiyamaOptions(add_reroutes=True)
    ) as tree:
        cube = g.Cube()
        sim = g.SimulationZone({"cube": cube})
        pos = sim.item("Position", g.Position())
        (pos.current + 0.1) >> pos.next
        offset = sim.delta_time * g.Vector((0, 0, 0.1)) * pos.current
        sim.input >> g.SetPosition(offset=offset) >> sim.output
        sim.output >> g.SetPosition(position=sim.output.o["Position"])

    assert any(n.bl_idname == "NodeReroute" for n in tree.tree.nodes)


def _build_reroutable(name: str) -> TreeBuilder:
    """A tree whose default arrangement spans enough ranks to route edges."""
    with TreeBuilder(name) as tree:
        cube = g.Cube()
        sim = g.SimulationZone({"cube": cube})
        pos = sim.item("Position", g.Position())
        (pos.current + 0.1) >> pos.next
        offset = sim.delta_time * g.Vector((0, 0, 0.1)) * pos.current
        sim.input >> g.SetPosition(offset=offset) >> sim.output
        sim.output >> g.SetPosition(position=sim.output.o["Position"])
    return tree


def test_default_sugiyama_options_scope():
    """default_sugiyama_options() changes what the plain "sugiyama" default
    resolves to (the hook behind the build CLI's --add-reroutes), without
    leaking past its scope or affecting explicit options."""
    from nodebpy import default_sugiyama_options

    with default_sugiyama_options(SugiyamaOptions(add_reroutes=True)):
        routed = _build_reroutable("ScopedReroutes")
        # An explicit method is not overridden.
        explicit = _build_chain("ScopedExplicit", SugiyamaOptions())
    after = _build_reroutable("ScopedRerouteAfter")

    assert any(n.bl_idname == "NodeReroute" for n in routed.tree.nodes)
    assert not any(n.bl_idname == "NodeReroute" for n in explicit.tree.nodes)
    assert not any(n.bl_idname == "NodeReroute" for n in after.tree.nodes)


def test_labelled_reroute_survives_add_reroutes():
    """add_reroutes dissolves authored reroutes before layout, but a
    labelled reroute carries meaning and must survive."""
    with TreeBuilder("LabelReroute", arrange=None) as tree:
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        sp = g.SetPosition(geometry=geo)
        reroute = tree.tree.nodes.new("NodeReroute")
        reroute.label = "keep me"
        tree.tree.links.new(sp.node.outputs[0], reroute.inputs[0])
        tree.tree.links.new(reroute.outputs[0], out.socket)

    arrange(tree.tree, SugiyamaOptions(add_reroutes=True))
    assert any(
        n.bl_idname == "NodeReroute" and n.label == "keep me" for n in tree.tree.nodes
    )


_ESSENTIALS = Path(BundledLibrary("geometry_nodes_essentials.blend").path())


@pytest.mark.skipif(
    not _ESSENTIALS.is_file(), reason="bundled geometry essentials not installed"
)
@pytest.mark.parametrize(
    ("tree_name", "options"),
    [
        # Authored reroutes + BALANCED direction + full socket alignment.
        (
            "Random Rotation",
            SugiyamaOptions(
                add_reroutes=True, direction="BALANCED", socket_alignment="FULL"
            ),
        ),
        # Frames + edge routing kept outside frames + moderate alignment.
        (
            "Project with Depth",
            SugiyamaOptions(
                add_reroutes=True,
                direction="RIGHT_DOWN",
                socket_alignment="MODERATE",
                keep_reroutes_outside_frames=True,
            ),
        ),
        # Frames + reroutes without routing (dummy nodes dissolve).
        (
            "Face Corner Angle",
            SugiyamaOptions(direction="LEFT_DOWN", socket_alignment="MODERATE"),
        ),
        # Heavy duplicate-type twins with authored reroutes: edge routing
        # around nodes (bend points).
        ("Randomize Transforms", SugiyamaOptions(add_reroutes=True)),
        # Frames + reroutes + split group inputs.
        ("Is UV Split", SugiyamaOptions(add_reroutes=True)),
    ],
    ids=[
        "balanced_full",
        "routed_outside_frames",
        "dissolved_left_down",
        "routed_twins",
        "routed_frames",
    ],
)
def test_arrange_essentials_option_matrix(tree_name, options):
    """The option combinations exercise the layout paths the defaults skip
    (BALANCED balancing, socket alignment, frame-aware edge routing,
    authored-reroute dissolution) on real, human-authored trees."""
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(_ESSENTIALS), link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = [tree_name]
    tree = dst.node_groups[0]
    assert tree is not None

    arrange(tree, options)

    real = [n for n in tree.nodes if n.bl_idname not in ("NodeFrame", "NodeReroute")]
    xs = {round(n.location.x) for n in real}
    assert len(xs) > 3, "nodes should be spread over several columns"
    for node in tree.nodes:
        for value in node.location:
            # Quantized to 2 decimals, modulo float32 storage error.
            assert abs(value - round(value, 2)) < 1e-4


def test_reroute_only_frame_and_repeated_multi_input():
    """A frame holding nothing but a reroute chain keeps its chain (as
    dummies) rather than dissolving it, and a reroute feeding the same
    multi-input twice is left alone — dissolving would collapse the
    duplicate links into one."""
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
        # The same reroute output into the same multi-input, twice.
        tree.tree.links.new(chain[-1].outputs[0], join.node.inputs[0])
        tree.tree.links.new(chain[-1].outputs[0], join.node.inputs[0])
        join >> out

    arrange(tree.tree, SugiyamaOptions(add_reroutes=True))
    multi_links = [link for link in tree.tree.links if link.to_node == join.node]
    assert len(multi_links) >= 2, "duplicate multi-input links must survive"


def test_simple_arrangement_edge_cases():
    """The simple arrangement handles an empty tree and a cyclic (zone)
    tree whose backward edges the crossing reducer must skip."""
    empty = bpy.data.node_groups.new("SimpleEmpty", "GeometryNodeTree")
    arrange(empty, "simple")
    assert len(empty.nodes) == 0

    # Nodes but nothing layoutable: only a frame.
    frame_only = bpy.data.node_groups.new("SimpleFrameOnly", "GeometryNodeTree")
    frame_only.nodes.new("NodeFrame")
    arrange(frame_only, "simple")

    cyclic = _build_reroutable("SimpleCyclic")
    arrange(cyclic.tree, SimpleOptions(spacing=(60, 30)))
    xs = {round(n.location.x) for n in cyclic.tree.nodes}
    assert len(xs) > 1


def test_options_do_not_leak_between_runs():
    """Each layout run gets fresh state: a run with custom options must not
    influence a later run with defaults."""
    reference = _build_chain("LeakReference", "sugiyama")
    _build_chain(
        "LeakCustom",
        SugiyamaOptions(add_reroutes=True, optimize_sizes=True, iterations=3),
    )
    repeat = _build_chain("LeakRepeat", "sugiyama")

    def locations(tree):
        return {n.name: tuple(n.location) for n in tree.tree.nodes}

    assert locations(repeat) == locations(reference)


def test_locations_are_quantized():
    """Arranged locations round-trip through the 2-decimal dump precision."""
    builder = _build_chain("Quantized", "sugiyama")
    for node in builder.tree.nodes:
        for value in node.location:
            assert value == round(value, 2)


class TestSocketOffsets:
    def test_outputs_above_inputs(self):
        tree = bpy.data.node_groups.new("Offsets", "GeometryNodeTree")
        node = tree.nodes.new("GeometryNodeSetPosition")

        output_offsets = [
            calculate_socket_offset_y(s) for s in node.outputs if s.enabled
        ]
        input_offsets = [calculate_socket_offset_y(s) for s in node.inputs if s.enabled]

        assert all(offset < 0 for offset in output_offsets + input_offsets)
        assert max(input_offsets) < min(output_offsets)

    def test_inputs_ordered_top_to_bottom(self):
        tree = bpy.data.node_groups.new("OffsetsOrder", "GeometryNodeTree")
        node = tree.nodes.new("GeometryNodeSetPosition")

        offsets = [calculate_socket_offset_y(s) for s in node.inputs if s.enabled]
        assert offsets == sorted(offsets, reverse=True)

    def test_offsets_within_estimated_height(self):
        from nodebpy.builder.layout import calculate_node_dimensions

        tree = bpy.data.node_groups.new("OffsetsHeight", "GeometryNodeTree")
        node = tree.nodes.new("GeometryNodeSetPosition")
        height = calculate_node_dimensions(node)[1]

        for socket in [*node.inputs, *node.outputs]:
            if not socket.enabled:
                continue
            assert -height <= calculate_socket_offset_y(socket) < 0

    def test_hidden_node_offsets(self):
        from nodebpy.builder.layout import calculate_node_dimensions

        with TreeBuilder("HiddenOffsets", arrange=None) as tree:
            a = g.Value()
            _ = a + 1.0

        math_node = next(n for n in tree.tree.nodes if n.bl_idname == "ShaderNodeMath")
        math_node.hide = True
        height = calculate_node_dimensions(math_node)[1]

        linked = [s for s in math_node.inputs if s.enabled and s.is_linked]
        assert linked
        for socket in linked:
            assert -height <= calculate_socket_offset_y(socket) < 0


def test_fallback_warns_and_arranges(monkeypatch):
    """A non-networkx ImportError propagates instead of falling back."""
    import nodebpy.builder.layout as arrange_module

    def boom(tree, options):
        raise ImportError("something else entirely")

    monkeypatch.setattr(arrange_module, "_arrange_sugiyama", boom)
    builder = _build_chain("FallbackRaise")
    with pytest.raises(ImportError, match="something else"):
        arrange(builder.tree, "sugiyama")
