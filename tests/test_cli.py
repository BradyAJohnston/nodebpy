"""Tests for the nodebpy CLI (``nodebpy export`` / ``nodebpy build``)."""

from pathlib import Path

import bpy

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.cli import _builders, _import_module, _merge_modules, main

STARTUP = Path(__file__).parent / "data/test_startup.blend"


def test_merge_modules_unions_imports():
    """Two single-class modules merge into one with deduped/unioned imports."""
    a = "from nodebpy import geometry as g\nfrom nodebpy.builder import CustomGeometryGroup\n\n\nclass A(CustomGeometryGroup):\n    _name = 'A'\n"
    b = "from nodebpy import geometry as g\nfrom nodebpy.builder import CustomShaderGroup\n\n\nclass B(CustomShaderGroup):\n    _name = 'B'\n"

    merged = _merge_modules([a, b])

    # `geometry as g` appears once; the two builder bases share one import line.
    assert merged.count("from nodebpy import geometry as g") == 1
    assert (
        "from nodebpy.builder import CustomGeometryGroup, CustomShaderGroup" in merged
    )
    assert "class A(CustomGeometryGroup):" in merged
    assert "class B(CustomShaderGroup):" in merged


def test_builders_discovery(tmp_path: Path):
    """`_builders` finds concrete NodeGroupBuilder subclasses defined in a module."""
    module_src = (
        "from nodebpy.builder import CustomGeometryGroup\n\n\n"
        "class Widget(CustomGeometryGroup):\n"
        "    _name = 'Widget'\n\n"
        "    def _build_group(self, tree):\n"
        "        tree.outputs.geometry('Geometry')\n"
    )
    py = tmp_path / "widget.py"
    py.write_text(module_src)

    builders = _builders(_import_module(py))

    assert [b.__name__ for b in builders] == ["Widget"]


def test_export_build_roundtrip(tmp_path: Path):
    """A node group survives .blend -> .py (export) -> .blend (build), asset-marked."""
    try:
        with TreeBuilder("RoundTrip") as tree:
            out = tree.outputs.geometry()
            _ = g.Cube() >> out
        tree.tree.use_fake_user = True  # keep the group through the save

        src = tmp_path / "src.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(src))

        py = tmp_path / "groups.py"
        main(["export", str(src), "-o", str(py)])
        assert "class RoundTrip(CustomGeometryGroup):" in py.read_text()

        out_blend = tmp_path / "library.blend"
        main(["build", str(py), "-o", str(out_blend)])

        bpy.ops.wm.open_mainfile(filepath=str(out_blend))
        group = bpy.data.node_groups.get("RoundTrip")
        assert group is not None
        assert group.asset_data is not None  # marked as a browsable asset
        assert group.use_fake_user
    finally:
        # The CLI replaced the active file; restore the test home file so the
        # autouse teardown finds its expected Cube/Material datablocks.
        bpy.ops.wm.read_homefile(filepath=str(STARTUP))


def test_build_no_asset(tmp_path: Path):
    """--no-asset saves the group without marking it as an asset."""
    try:
        py = tmp_path / "plain.py"
        py.write_text(
            "from nodebpy.builder import CustomGeometryGroup\n\n\n"
            "class Plain(CustomGeometryGroup):\n"
            "    _name = 'Plain'\n\n"
            "    def _build_group(self, tree):\n"
            "        tree.outputs.geometry('Geometry')\n"
        )
        out_blend = tmp_path / "plain.blend"
        main(["build", str(py), "-o", str(out_blend), "--no-asset"])

        bpy.ops.wm.open_mainfile(filepath=str(out_blend))
        group = bpy.data.node_groups.get("Plain")
        assert group is not None
        assert group.asset_data is None
    finally:
        bpy.ops.wm.read_homefile(filepath=str(STARTUP))
