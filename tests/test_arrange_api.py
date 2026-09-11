"""Tests for the unified arrange() API and its options."""

import bpy
import pytest

from nodebpy import SimpleOptions, SugiyamaOptions, TreeBuilder, arrange
from nodebpy import geometry as g
from nodebpy.builder.layout import calculate_socket_offset_y
from nodebpy.lib.nodearrange import config


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


def test_settings_restored_after_arrange():
    """Custom options must not leak into the global vendored settings."""
    defaults = config.Settings()
    _build_chain(
        "SettingsRestore",
        SugiyamaOptions(add_reroutes=True, optimize_sizes=True, iterations=3),
    )
    assert config.SETTINGS == defaults
    assert tuple(config.MARGIN) == (200.0, 20.0)
    assert config.ntree is None


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
