"""Structural layout snapshots: dump → rebuild must restore every node's
authored name and position even though a rebuild names duplicate-type nodes
in a different order.

``to_python(snapshot_positions=True)`` emits a ``tree.layout_snapshot``
block whose entries carry each node's type, location, frame parent and
links; ``TreeBuilder.layout_snapshot`` matches rebuilt nodes to entries by
structure (names only break ties). The plot tests draw real asset trees
before dumping and after rebuilding into ``tests/plots/`` so the fidelity
can also be checked by eye.
"""

from pathlib import Path

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.builder import BundledLibrary
from nodebpy.builder._utils import socket_key
from nodebpy.export import to_plot, to_python

PLOT_DIR = Path(__file__).parent / "plots"


def _abs_positions(tree):
    """{node name: absolute (x, y)} with frame parents walked."""
    out = {}
    for node in tree.nodes:
        x, y = node.location
        parent = node.parent
        while parent is not None:
            x += parent.location.x
            y += parent.location.y
            parent = parent.parent
        out[node.name] = (round(x, 2), round(y, 2))
    return out


def _link_keys(tree):
    return sorted(
        (
            link.from_node.name,
            socket_key(link.from_socket),
            link.to_node.name,
            socket_key(link.to_socket),
        )
        for link in tree.links
    )


# ---------------------------------------------------------------------------
# Matcher behaviour on hand-built trees
# ---------------------------------------------------------------------------


def test_snapshot_restores_swapped_duplicate_names():
    """Two same-type nodes whose authored suffixes disagree with rebuild
    creation order still land on their own authored spots — restoring by
    bare name would swap them."""
    with TreeBuilder("SwapSnap", arrange=None) as tree:
        x = tree.inputs.float("X")
        a = x + 1.0  # first Math created -> "Math"
        b = a * 2.0  # second -> "Math.001"
        b >> tree.outputs.float("Out")

    # Author the opposite naming: the add node carries ".001".
    add_node = tree.tree.nodes["Math"]
    mul_node = tree.tree.nodes["Math.001"]
    mul_node.name = "__tmp"
    add_node.name = "Math.001"
    mul_node.name = "Math"
    add_node.location = (100.0, -10.0)
    mul_node.location = (300.0, -30.0)

    code = to_python(tree, snapshot_positions=True, format=False)
    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    rebuilt = ns["tree"].tree

    # The add node (fed by Group Input) must be the one named "Math.001".
    renamed_add = rebuilt.nodes["Math.001"]
    assert renamed_add.operation == "ADD"
    assert tuple(renamed_add.location) == (100.0, -10.0)
    renamed_mul = rebuilt.nodes["Math"]
    assert renamed_mul.operation == "MULTIPLY"
    assert tuple(renamed_mul.location) == (300.0, -30.0)


def test_snapshot_restores_frame_membership():
    """A snapshot entry's parent puts the node back into its frame, and the
    location is applied parent-relative."""
    with TreeBuilder("FrameSnap", arrange=None) as tree:
        x = tree.inputs.float("X")
        with g.Frame("Inner"):
            a = x + 1.0
        a >> tree.outputs.float("Out")

    frame = next(n for n in tree.tree.nodes if n.bl_idname == "NodeFrame")
    frame.location = (500.0, 250.0)
    math = next(n for n in tree.tree.nodes if n.bl_idname == "ShaderNodeMath")
    math.location = (40.0, -20.0)

    code = to_python(tree, snapshot_positions=True, format=False)
    bpy.data.node_groups.remove(tree.tree)
    ns: dict = {}
    exec(code, ns)
    rebuilt = ns["tree"].tree

    math = next(n for n in rebuilt.nodes if n.bl_idname == "ShaderNodeMath")
    assert math.parent is not None and math.parent.bl_idname == "NodeFrame"
    assert tuple(math.location) == (40.0, -20.0)
    assert tuple(math.parent.location) == (500.0, 250.0)


def test_layout_snapshot_property_round_trip():
    """The getter's snapshot, applied to the same tree, is a no-op fixpoint."""
    with TreeBuilder("SnapProp", arrange=None) as tree:
        x = tree.inputs.float("X")
        (x + 1.0) * 2.0 >> tree.outputs.float("Out")
    for i, node in enumerate(tree.tree.nodes):
        node.location = (i * 90.0, i * -35.0)

    before = _abs_positions(tree.tree)
    tree.layout_snapshot = tree.layout_snapshot
    assert _abs_positions(tree.tree) == before


def test_snapshot_skips_missing_entries():
    """Entries with no structural counterpart (an edited tree) are skipped
    instead of stealing a same-type node."""
    with TreeBuilder("SparseSnap", arrange=None) as tree:
        x = tree.inputs.float("X")
        (x + 1.0) >> tree.outputs.float("Out")
    snapshot = tree.layout_snapshot
    snapshot["Ghost Node"] = ("GeometryNodeSetPosition", (9.0, 9.0), None, ())
    tree.layout_snapshot = snapshot  # must not raise
    assert "Ghost Node" not in tree.tree.nodes


# ---------------------------------------------------------------------------
# Real-asset round-trips, with before/after plots
# ---------------------------------------------------------------------------

_ESSENTIALS = Path(BundledLibrary("geometry_nodes_essentials.blend").path())

# Coverage: frames + split Group Inputs (Project with Depth), reroutes +
# heavy duplicate-type twins (Randomize Transforms), frames + reroutes
# (Face Corner Angle).
_TREES = ["Project with Depth", "Randomize Transforms", "Face Corner Angle"]


@pytest.mark.skipif(
    not _ESSENTIALS.is_file(), reason="bundled geometry essentials not installed"
)
@pytest.mark.parametrize("tree_name", _TREES, ids=lambda n: n.replace(" ", "_"))
def test_essentials_layout_round_trip(tree_name):
    """Dump a human-authored essentials tree with snapshot_positions and
    keep_reroutes, rebuild it, and require identical names, absolute
    positions and link topology — plotting both stages for eye inspection."""
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(_ESSENTIALS), link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = [tree_name]
    original = dst.node_groups[0]
    assert original is not None

    slug = tree_name.replace(" ", "_")
    to_plot(
        original,
        PLOT_DIR / f"{slug}_0_original.png",
        title=f"{tree_name} — original",
    )
    want_positions = _abs_positions(original)
    want_links = _link_keys(original)

    code = to_python(original, snapshot_positions=True, keep_reroutes=True)
    original.name = "__original"
    ns: dict = {}
    exec(code, ns)
    rebuilt = bpy.data.node_groups[tree_name]

    to_plot(
        rebuilt,
        PLOT_DIR / f"{slug}_1_rebuilt.png",
        title=f"{tree_name} — rebuilt",
    )
    assert _abs_positions(rebuilt) == want_positions
    assert _link_keys(rebuilt) == want_links
