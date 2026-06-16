"""Asset-backed node groups: the generated essentials APIs and the generator."""

import os

import pytest

from nodebpy import geometry as g
from nodebpy.assets import BundledLibrary, generate_asset_api

_ESSENTIALS = BundledLibrary("geometry_nodes_essentials.blend")
_HAVE_ESSENTIALS = os.path.exists(_ESSENTIALS.path())
_needs_essentials = pytest.mark.skipif(
    not _HAVE_ESSENTIALS, reason="bundled geometry essentials not installed"
)


@_needs_essentials
def test_generated_asset_appends_and_links():
    from nodebpy.nodes import geometry as ga

    with g.tree("t"):
        node = ga.SmoothByAngle(mesh=g.Cube(), angle=0.5)
        # The asset's node group is appended and wired to a Group node.
        assert node.node.node_tree is not None
        assert node.node.node_tree.name == "Smooth by Angle"
        # Typed interface access works like any other node.
        assert node.o.mesh is not None
        # The Mesh input was linked from the Cube.
        assert any(socket.is_linked for socket in node.node.inputs)


@_needs_essentials
def test_generated_asset_chains():
    from nodebpy.nodes import geometry as ga

    with g.tree("t"):
        mesh = ga.SmoothByAngle(mesh=g.Cube()).o.mesh
        arr = ga.Array(geometry=mesh, count=4)
        assert arr.o.geometry is not None


@_needs_essentials
def test_generate_asset_api_roundtrip(tmp_path):
    out = tmp_path / "generated.py"
    names = generate_asset_api(_ESSENTIALS, out, names={"Smooth by Angle"})
    assert names == ["SmoothByAngle"]
    source = out.read_text()
    assert "class SmoothByAngle(AssetGeometryGroup):" in source
    assert "Smooth by Angle" in source
