"""Drawing node trees with matplotlib (``nodebpy.export.to_plot``).

Blender cannot render node editors headlessly, so some of these tests draw
trees before and after ``arrange()`` into ``tests/plots/`` (gitignored, like
the saved ``.blend`` files), where the layouts can be looked at.
"""

from pathlib import Path

import bpy
import pytest

from nodebpy import SugiyamaOptions, TreeBuilder, arrange
from nodebpy import geometry as g
from nodebpy.export import to_plot
from nodebpy.nodes.geometry.groups import (
    ClipFieldToBox,
    GeometryPrincipalComponents,
    PrincipalComponents,
    SliceToIndices,
)

from .layout.cases import reset_locations
from .layout.metrics import measure

PLOT_DIR = Path(__file__).parent / "plots"

# A drawn plot with axes and a title is well past this; an empty or broken
# figure is not.
_MIN_PLOT_BYTES = 5_000


def _plot_stages(tree, name: str) -> None:
    """Plot the tree unarranged, then arranged with each method, titled
    with its layout metrics."""
    reset_locations(tree)
    written = [
        to_plot(tree, PLOT_DIR / f"{name}_0_before.png", title=f"{name} — before")
    ]

    arrange(tree, "sugiyama")
    written.append(
        to_plot(
            tree,
            PLOT_DIR / f"{name}_1_sugiyama.png",
            title=f"{name} — sugiyama — {measure(tree).summary()}",
        )
    )

    reset_locations(tree)
    arrange(tree, "simple")
    written.append(
        to_plot(
            tree,
            PLOT_DIR / f"{name}_2_simple.png",
            title=f"{name} — simple — {measure(tree).summary()}",
        )
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

    reset_locations(tree.tree)
    before = to_plot(
        tree.tree, PLOT_DIR / "PlotShowcase_0_before.png", title="PlotShowcase — before"
    )
    arrange(tree.tree, SugiyamaOptions(fit_collapsed_widths=True))
    after = to_plot(
        tree.tree,
        PLOT_DIR / "PlotShowcase_1_sugiyama.png",
        title="PlotShowcase — sugiyama (fit_collapsed_widths)",
    )

    for path in (before, after):
        assert path.exists()
        assert path.stat().st_size > _MIN_PLOT_BYTES


def test_node_plot_draws_group_node(tmp_path):
    """to_plot(node=True) renders the tree as one group node — from the
    export function and the TreeBuilder method alike — and leaves no
    scratch tree behind. Every interface socket type that draws a value
    widget is exercised, and axes=True adds a ticked frame."""
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

    path = to_plot(tree.tree, PLOT_DIR / "NodePlot_node.png", node=True)
    assert path.stat().st_size > _MIN_PLOT_BYTES
    wide = tree.to_plot(tmp_path / "wide.png", node=True, width=240)
    assert wide.stat().st_size > _MIN_PLOT_BYTES
    plain = tree.to_plot(tmp_path / "tree.png", title="NodePlot")
    framed = tree.to_plot(PLOT_DIR / "NodePlot_axes.png", title="NodePlot", axes=True)
    assert set(bpy.data.node_groups.keys()) == before | {"NodePlot"}

    from PIL import Image

    # The axes margin grows the image without rescaling the drawing.
    assert Image.open(framed).width > Image.open(plain).width
    assert Image.open(framed).height > Image.open(plain).height


def test_node_plot_rejects_unknown_tree_type(tmp_path):
    """A tree type without a known group-node counterpart is refused."""
    tree = bpy.data.node_groups.new("NoGroupNode", "TextureNodeTree")
    from nodebpy.export import plot as plot_module

    monkey = plot_module._GROUP_NODE_FOR_TREE.pop("TextureNodeTree")
    try:
        with pytest.raises(ValueError, match="Cannot draw a group node"):
            to_plot(tree, tmp_path / "never.png", node=True)
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


def test_node_plot_with_open_panels_is_taller(tmp_path):
    with TreeBuilder("Panelled", arrange=None) as tree:
        geo = tree.inputs.geometry()
        with tree.inputs.panel("Shape", default_closed=True):
            tree.inputs.float("Radius", 1.0)
            tree.inputs.float("Depth", 2.0)
        geo >> tree.outputs.geometry()

    closed = to_plot(tree.tree, tmp_path / "closed.png", node=True)
    opened = to_plot(tree.tree, tmp_path / "open.png", node=True, open_panels=True)

    from PIL import Image

    assert Image.open(opened).height > Image.open(closed).height


def test_zone_members_and_hull():
    """A zone holds its input and output nodes and whatever is fed from the
    input; a node feeding into the zone from outside is not a member. The
    zone outline is the rounded convex hull of the members."""
    from nodebpy.export.plot import _convex_hull, _rounded_offset, _zone_members

    with TreeBuilder("ZoneMembers", arrange=None) as tree:
        sim = g.SimulationZone({"mesh": g.Cube()})
        outside = g.Vector((0.0, 0.0, 0.1))  # fed from nothing inside
        inside = sim.input >> g.SetPosition(offset=outside)
        inside >> sim.output
        sim.output >> tree.outputs.geometry()

    members = _zone_members(tree.tree, sim.input.node, sim.output.node)
    assert {sim.input.node, sim.output.node, inside.node} <= members
    assert outside.node not in members
    assert tree.tree.nodes["Group Output"] not in members

    hull = _convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 0)])
    assert set(hull) == {(0, 0), (2, 0), (2, 2), (0, 2)}
    outline = _rounded_offset(hull, 1.0)
    xs = [x for x, _ in outline]
    ys = [y for _, y in outline]
    assert min(xs) == pytest.approx(-1.0) and max(xs) == pytest.approx(3.0)
    assert min(ys) == pytest.approx(-1.0) and max(ys) == pytest.approx(3.0)
