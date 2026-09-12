"""Visual snapshots of arrangement results.

Blender cannot render node editors headlessly, so these tests draw each
tree's layout with matplotlib (``nodebpy.export.to_plot``) before and after
arrangement. The images land in ``tests/plots/`` (gitignored, like the
saved ``.blend`` files) so layout quality can be inspected by eye without
opening Blender.
"""

from pathlib import Path

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
