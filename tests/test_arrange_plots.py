"""Visual snapshots of arrangement results.

Blender cannot render node editors headlessly, so these tests draw each
tree's layout with matplotlib (``nodebpy.export.to_plot``) before and after
arrangement. The images land in ``tests/plots/`` (gitignored, like the
saved ``.blend`` files) so layout quality can be inspected by eye without
opening Blender.
"""

from pathlib import Path

import bpy
import pytest

from nodebpy import SugiyamaOptions, TreeBuilder, arrange
from nodebpy import geometry as g
from nodebpy.export import to_node_plot, to_plot
from nodebpy.nodes.geometry.groups import (
    ClipFieldToBox,
    GeometryPrincipalComponents,
    PrincipalComponents,
    SliceToIndices,
)

PLOT_DIR = Path(__file__).parent / "plots"

# A drawn plot with axes and a title is well past this; an empty or broken
# figure is not.
_MIN_PLOT_BYTES = 5_000


def _reset_locations(tree) -> None:
    """Pile every node at the origin — the state a freshly authored
    (codegen or nodebpy-built) tree is in before arrangement."""
    for node in tree.nodes:
        node.location = (0, 0)


def _plot_stages(tree, name: str) -> None:
    """Plot the tree unarranged, then arranged with each algorithm."""
    _reset_locations(tree)
    written = [
        to_plot(tree, PLOT_DIR / f"{name}_0_before.png", title=f"{name} — before")
    ]

    arrange(tree, "sugiyama")
    written.append(
        to_plot(tree, PLOT_DIR / f"{name}_1_sugiyama.png", title=f"{name} — sugiyama")
    )

    _reset_locations(tree)
    arrange(tree, "simple")
    written.append(
        to_plot(tree, PLOT_DIR / f"{name}_2_simple.png", title=f"{name} — simple")
    )

    for path in written:
        assert path.exists()
        assert path.stat().st_size > _MIN_PLOT_BYTES


@pytest.mark.parametrize(
    "asset",
    [GeometryPrincipalComponents, PrincipalComponents, SliceToIndices, ClipFieldToBox],
    ids=lambda cls: cls.__name__,
)
def test_plot_asset_group_arrangements(asset):
    """Before/after plots for the shipped asset groups."""
    tree = asset.create_group()
    _plot_stages(tree, asset.__name__)


def test_plot_requires_matplotlib(monkeypatch, tmp_path):
    """Without matplotlib, to_plot raises the install hint instead of a bare
    ModuleNotFoundError."""
    import sys

    with TreeBuilder("NoMpl", arrange=None) as tree:
        tree.inputs.geometry() >> tree.outputs.geometry()

    monkeypatch.setitem(sys.modules, "matplotlib.figure", None)
    with pytest.raises(ImportError, match=r"nodebpy\[plot\]"):
        to_plot(tree.tree, tmp_path / "never.png")


def test_plot_skips_empty_frames(tmp_path):
    """A frame with no children has no extent to draw and is skipped."""
    with TreeBuilder("EmptyFrame", arrange=None) as tree:
        tree.inputs.geometry() >> tree.outputs.geometry()
        tree.tree.nodes.new("NodeFrame")

    path = to_plot(tree.tree, tmp_path / "empty_frame.png")
    assert path.stat().st_size > _MIN_PLOT_BYTES


def test_optimize_sizes_display_names():
    """optimize_sizes fits collapsed widths from each node's display name —
    label, math operation, referencing group tree, or image name."""
    image = bpy.data.images.new("SizeTex", 2, 2)
    with TreeBuilder("DisplayNames", arrange=None) as tree:
        geo = tree.inputs.geometry()
        labelled = g.SetPosition(geometry=geo)
        labelled.node.label = "A Rather Long Custom Label"
        math = g.Math.add(1.0, 2.0)
        tex = g.ImageTexture(image=image)
        group = g.Group()
        group.node.node_tree = bpy.data.node_groups.new(
            "Sized Group", "GeometryNodeTree"
        )
        labelled >> tree.outputs.geometry()
        for node in (labelled.node, math.node, tex.node, group.node):
            node.hide = True

    widths = {n.name: n.width for n in tree.tree.nodes}
    arrange(tree.tree, SugiyamaOptions(optimize_sizes=True, stack_collapsed=True))
    # The long label must have widened its collapsed node.
    assert tree.tree.nodes[labelled.node.name].width > widths[labelled.node.name]
    bpy.data.images.remove(image)


def test_optimize_sizes_shader_image_name():
    """A collapsed shader image node's display name is its image's name;
    stacked collapsed nodes with parallel links stack without duplicating
    edges."""
    from nodebpy import shader as s

    image = bpy.data.images.new("ShaderSizeTex", 2, 2)
    with TreeBuilder.shader("ShaderSizes") as tree:
        tex = s.ImageTexture()
        tex.node.image = image
        # Two parallel links between the same pair of collapsed math nodes.
        first = s.Math.add(tex.o.alpha, 1.0)
        second = s.Math.add(first, first)
        second >> tree.outputs.float("Out")
        for node in (tex.node, first.node, second.node):
            node.hide = True
    arrange(tree.tree, SugiyamaOptions(optimize_sizes=True, stack_collapsed=True))
    xs = {round(n.location.x) for n in tree.tree.nodes}
    assert len(xs) > 1
    bpy.data.images.remove(image)


def test_plot_collapsed_and_framed_tree():
    """A tree exercising the visual features the plotter must show:
    collapsed (hidden) nodes, a frame, and fan-in/fan-out links."""
    with TreeBuilder("PlotShowcase", arrange=None) as tree:
        geo = tree.inputs.geometry()
        factor = tree.inputs.float("Factor", 1.0)
        out = tree.outputs.geometry()

        with g.Frame("Math"):
            a = (factor + 1.0) * 2.0
            b = (a - 0.5) / 3.0
        offset = g.CombineXYZ(x=a, y=b, z=factor)
        _ = geo >> g.SetPosition(offset=offset) >> g.RealizeInstances() >> out

        for node in tree.tree.nodes:
            if node.bl_idname == "ShaderNodeMath":
                node.hide = True

    _reset_locations(tree.tree)
    before = to_plot(
        tree.tree, PLOT_DIR / "PlotShowcase_0_before.png", title="PlotShowcase — before"
    )
    arrange(tree.tree, SugiyamaOptions(optimize_sizes=True))
    after = to_plot(
        tree.tree,
        PLOT_DIR / "PlotShowcase_1_sugiyama.png",
        title="PlotShowcase — sugiyama (optimize_sizes)",
    )

    for path in (before, after):
        assert path.exists()
        assert path.stat().st_size > _MIN_PLOT_BYTES


def test_node_plot_draws_group_node(tmp_path):
    """to_node_plot renders the tree as one group node — from the export
    function and the TreeBuilder method alike — and leaves no scratch tree
    behind. Every interface socket type that draws a value widget is
    exercised."""
    before = set(bpy.data.node_groups.keys())
    with TreeBuilder("NodePlot", arrange=None) as tree:
        geo = tree.inputs.geometry()
        tree.inputs.float("Factor", 0.5, min_value=0.0, max_value=1.0, subtype="FACTOR")
        tree.inputs.float("Angle", 1.0, subtype="ANGLE")
        tree.inputs.integer("Order", 6)
        tree.inputs.vector("Axis", (0.0, 0.0, 1.0))
        tree.inputs.string("Name", "sym_id")
        tree.inputs.boolean("Realize", True)
        tree.inputs.color("Tint", (0.8, 0.2, 0.1, 1.0))
        geo >> tree.outputs.geometry()

    path = to_node_plot(tree.tree, PLOT_DIR / "NodePlot_node.png")
    assert path.stat().st_size > _MIN_PLOT_BYTES
    wide = tree.to_node_plot(tmp_path / "wide.png", width=240)
    assert wide.stat().st_size > _MIN_PLOT_BYTES
    assert tree.to_plot(tmp_path / "tree.png", title="NodePlot").exists()
    assert set(bpy.data.node_groups.keys()) == before | {"NodePlot"}


def test_node_plot_rejects_unknown_tree_type(tmp_path):
    """A tree type without a known group-node counterpart is refused."""
    tree = bpy.data.node_groups.new("NoGroupNode", "TextureNodeTree")
    from nodebpy.export import plot as plot_module

    monkey = plot_module._GROUP_NODE_FOR_TREE.pop("TextureNodeTree")
    try:
        with pytest.raises(ValueError, match="Cannot draw a group node"):
            to_node_plot(tree, tmp_path / "never.png")
    finally:
        plot_module._GROUP_NODE_FOR_TREE["TextureNodeTree"] = monkey
        bpy.data.node_groups.remove(tree)


def test_plot_zones_reroutes_and_widgets():
    """A tree exercising the remaining editor features the plotter draws:
    a simulation zone, a reroute, muted / invalid links, custom node colour,
    a frame label, value / vector / colour / string input nodes and every
    property widget kind."""
    with TreeBuilder("PlotZones", arrange=None) as tree:
        cube = g.Cube()
        sim = g.SimulationZone({"cube": cube})
        pos = sim.item("Position", g.Position())
        (pos.current + 0.1) >> pos.next
        vec = g.Vector((0.0, 0.0, 0.1))
        offset = sim.delta_time * vec * pos.current
        sim.input >> g.SetPosition(offset=offset) >> sim.output
        out = sim.output >> g.SetPosition(position=sim.output.o["Position"])
        with g.Frame("Constants"):
            g.Color(value=(0.2, 0.4, 0.8, 1.0))
            g.String(string="a comment")
            g.Value(1.5)
        store = g.StoreNamedAttribute(
            geometry=out, name="idx", value=g.Index(), data_type="INT"
        )
        store >> tree.outputs.geometry()
        reroute = tree.tree.nodes.new("NodeReroute")
        tree.tree.links.new(cube.node.outputs[0], reroute.inputs[0])
        cube.node.use_custom_color = True
        cube.node.color = (0.4, 0.2, 0.2)
        muted = tree.tree.links.new(vec.node.outputs[0], store.node.inputs["Name"])
        muted.is_muted = True

    arrange(tree.tree, "sugiyama")
    path = to_plot(tree.tree, PLOT_DIR / "PlotZones.png", title="PlotZones")
    assert path.stat().st_size > _MIN_PLOT_BYTES


def test_plot_matches_layout_row_model():
    """The plot and the arranger share one row model: a hide_value vector
    input takes a single row and undrawn RNA bookkeeping adds no property
    rows, so a Set Position node is header + 1 output + 4 inputs."""
    from nodebpy.builder.layout import (
        HEADER,
        SOCKET_ROW,
        calculate_node_dimensions,
        node_property_rows,
    )

    with TreeBuilder("RowModel", arrange=None) as tree:
        sp = g.SetPosition()
        sim = g.SimulationZone({"cube": g.Cube()})
        vec = g.Vector((1.0, 2.0, 3.0))
        out = tree.outputs.geometry()
        sim.output >> out

    _, height = calculate_node_dimensions(sp.node)
    # Offset is an unlinked, shown vector: one row plus the expanded widget.
    from nodebpy.builder.layout import VECTOR_EXPANDED

    assert height == pytest.approx(HEADER + 5 * SOCKET_ROW + VECTOR_EXPANDED)
    assert node_property_rows(sim.input.node) == []
    assert node_property_rows(sim.output.node) == []
    assert node_property_rows(tree.tree.nodes["Group Output"]) == []
    (vector_prop, rows), *rest = node_property_rows(vec.node)
    assert vector_prop.identifier == "vector" and rows == 3
    assert rest == []


def test_group_node_panels_in_row_model(tmp_path):
    """A group node draws its interface panels: a closed panel is one header
    row hiding its sockets (linked ones fold onto the header, which is
    where links anchor), an open panel adds a header row above its
    sockets, and to_node_plot(open_panels=True) expands them all."""
    from nodebpy.builder.layout import (
        HEADER,
        PROPERTY_ROW,
        SOCKET_ROW,
        calculate_node_dimensions,
        calculate_socket_offset_y,
        node_rows,
    )

    with TreeBuilder("Panelled", arrange=None) as inner:
        geo = inner.inputs.geometry()
        with inner.inputs.panel("Shape", default_closed=True):
            inner.inputs.float("Radius", 1.0)
            inner.inputs.float("Depth", 2.0)
        with inner.inputs.panel("Colour"):
            inner.inputs.boolean("Flat", False)
        geo >> inner.outputs.geometry()

    with TreeBuilder("Outer", arrange=None) as outer:
        group = g.Group()
        group.node.node_tree = inner.tree
        outer.inputs.float("Value", 0.5) >> group.node.inputs["Depth"]
        node = group.node

    kinds = [(r.kind, getattr(r.panel, "name", None), r.open) for r in node_rows(node)]
    assert kinds == [
        ("output", None, True),
        ("property", None, True),
        ("input", None, True),  # Geometry
        ("panel", "Shape", False),
        ("panel", "Colour", True),
        ("input", None, True),  # Flat
    ]
    # Closed panel: 1 row for the header, none for Radius / Depth.
    _, height = calculate_node_dimensions(node)
    assert height == pytest.approx(HEADER + 5 * SOCKET_ROW + PROPERTY_ROW)
    # The linked Depth folds onto the Shape header; unlinked Radius does not.
    shape_row = node_rows(node)[3]
    assert [s.name for s in shape_row.collapsed_sockets] == ["Depth"]
    assert calculate_socket_offset_y(node.inputs["Depth"]) == shape_row.anchor
    assert calculate_socket_offset_y(node.inputs["Radius"]) == pytest.approx(
        -HEADER / 2
    )

    for state in node.panel_states:
        state.is_collapsed = False
    assert [r.kind for r in node_rows(node)].count("input") == 4

    closed = to_node_plot(inner.tree, tmp_path / "closed.png")
    opened = to_node_plot(inner.tree, tmp_path / "open.png", open_panels=True)
    # More rows drawn => a taller image.
    from PIL import Image

    assert Image.open(opened).height > Image.open(closed).height
