# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for nodebpy.assets.dump_library / build_library — round-tripping a
.blend asset library through per-asset Python source files."""

from pathlib import Path

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.assets import build_library, dump_library
from nodebpy.assets._library import CATALOG_FILENAME
from nodebpy.builder import CustomGeometryGroup

from .test_codegen import _structure

CATALOG_ID = "12345678-1234-1234-1234-123456789abc"


class _Doubler(CustomGeometryGroup):
    """A nested (non-asset) helper group, to prove dependencies are dumped
    into the asset's file and rebuilt alongside it."""

    _name = "Doubler"

    def _build_group(self, tree):
        value = tree.inputs.float("Value")
        g.Math.multiply(value, 2.0) >> tree.outputs.float("Doubled")


def _clear_node_groups():
    for group in list(bpy.data.node_groups):
        bpy.data.node_groups.remove(group)


def _write_library(path: Path) -> None:
    """Write a two-asset library: a geometry asset (nesting ``Doubler``) with
    full metadata, and a shader asset. Leaves the session clean."""
    with TreeBuilder("Scale Up") as geo_tree:
        geo = geo_tree.inputs.geometry("Geometry")
        factor = geo_tree.inputs.float("Factor")
        doubled = _Doubler(Value=factor).o.doubled
        scale = g.CombineXYZ(x=doubled, y=doubled, z=doubled)
        g.TransformGeometry(geometry=geo, scale=scale) >> geo_tree.outputs.geometry(
            "Geometry"
        )

    tree = geo_tree.tree
    tree.asset_mark()
    assert tree.asset_data is not None
    tree.asset_data.description = "Scales geometry up by a doubled factor"
    tree.asset_data.author = "nodebpy tests"
    tree.asset_data.catalog_id = CATALOG_ID
    tree.asset_data.tags.new("mesh")
    tree.asset_data.tags.new("transform")
    tree.is_modifier = True

    with TreeBuilder.shader("Flat Red") as shader_tree:
        color = shader_tree.inputs.color("Color")
        s.Emission(color=color) >> shader_tree.outputs.shader("Shader")
    shader_tree.tree.asset_mark()

    bpy.data.libraries.write(
        str(path), {geo_tree.tree, shader_tree.tree}, fake_user=True
    )
    _clear_node_groups()


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


def test_dump_writes_one_module_per_asset(library_blend, tmp_path):
    out = tmp_path / "src"
    written = dump_library(library_blend, out)

    assert set(written) == {"Scale Up", "Flat Red"}
    assert written["Scale Up"] == out / "geometry" / "scale_up.py"
    assert written["Flat Red"] == out / "shader" / "flat_red.py"

    code = written["Scale Up"].read_text()
    # The asset's class and its nested dependency are both in the file.
    assert "class ScaleUp(CustomGeometryGroup):" in code
    assert "class Doubler(CustomGeometryGroup):" in code
    assert "ASSET = ScaleUp" in code
    # Metadata and non-default tree flags are dumped.
    assert CATALOG_ID in code
    assert '"tags": ("mesh", "transform")' in code
    assert '"is_modifier": True' in code
    # The shader asset carries no metadata or tree flags — no empty footers.
    shader_code = written["Flat Red"].read_text()
    assert "ASSET = FlatRed" in shader_code
    assert "ASSET_METADATA" not in shader_code
    assert "TREE_PROPERTIES" not in shader_code
    # Dumping cleans the appended groups back out of the session.
    assert not bpy.data.node_groups


def test_dump_names_filter(library_blend, tmp_path):
    written = dump_library(library_blend, tmp_path / "src", names={"Flat Red"})
    assert set(written) == {"Flat Red"}
    with pytest.raises(KeyError, match="No Such Asset"):
        dump_library(library_blend, tmp_path / "src", names={"No Such Asset"})


def test_dump_refuses_clashing_session_groups(library_blend, tmp_path):
    with TreeBuilder("Scale Up"):
        pass
    with pytest.raises(RuntimeError, match="fresh session"):
        dump_library(library_blend, tmp_path / "src")


def test_build_refuses_dirty_session(library_blend, tmp_path):
    src = tmp_path / "src"
    dump_library(library_blend, src)
    with TreeBuilder("Stale"):
        pass
    with pytest.raises(RuntimeError, match="fresh session"):
        build_library(src, tmp_path / "rebuilt.blend")


def test_build_requires_sources(tmp_path):
    with pytest.raises(FileNotFoundError):
        build_library(tmp_path, tmp_path / "rebuilt.blend")


def test_roundtrip_blend_to_python_to_blend(library_blend, tmp_path):
    src = tmp_path / "src"
    dump_library(library_blend, src)
    assert not bpy.data.node_groups

    rebuilt_path = tmp_path / "rebuilt" / "library.blend"
    names = build_library(src, rebuilt_path)
    assert rebuilt_path.is_file()
    assert set(names) == {"Scale Up", "Flat Red"}
    # The built trees are in-session, marked as assets, with metadata applied.
    scale_up = bpy.data.node_groups["Scale Up"]
    assert scale_up.asset_data is not None
    assert scale_up.asset_data.catalog_id == CATALOG_ID
    assert scale_up.asset_data.description == "Scales geometry up by a doubled factor"
    assert {t.name for t in scale_up.asset_data.tags} == {"mesh", "transform"}
    assert scale_up.is_modifier
    # The nested dependency was rebuilt once, not per reference.
    assert "Doubler" in bpy.data.node_groups

    # Structural signature of the originals, for comparison after reload.
    _clear_node_groups()
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(library_blend), link=False, assets_only=True
    ) as (src_lib, dst):
        original_names = set(src_lib.node_groups)
        dst.node_groups = list(src_lib.node_groups)
    originals = {t.name: _structure(t) for t in dst.node_groups}
    _clear_node_groups()

    # The rebuilt .blend exposes the same assets with the same structure and
    # metadata.
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(rebuilt_path), link=False, assets_only=True
    ) as (src_lib, dst):
        assert set(src_lib.node_groups) == original_names
        dst.node_groups = list(src_lib.node_groups)
    for rebuilt in dst.node_groups:
        assert _structure(rebuilt) == originals[rebuilt.name], rebuilt.name
    rebuilt_scale_up = next(t for t in dst.node_groups if t.name == "Scale Up")
    assert rebuilt_scale_up.asset_data is not None
    assert rebuilt_scale_up.asset_data.catalog_id == CATALOG_ID
    assert rebuilt_scale_up.is_modifier


def test_dump_is_stable_across_a_roundtrip(library_blend, tmp_path):
    """dump → build → dump again produces identical sources, so a no-op edit
    in Blender leaves no VCS diff."""
    first = tmp_path / "first"
    dump_library(library_blend, first)
    rebuilt = tmp_path / "rebuilt.blend"
    build_library(first, rebuilt)
    _clear_node_groups()

    second = tmp_path / "second"
    dump_library(rebuilt, second)
    first_files = sorted(p.relative_to(first) for p in first.rglob("*.py"))
    second_files = sorted(p.relative_to(second) for p in second.rglob("*.py"))
    assert first_files == second_files
    for rel in first_files:
        assert (second / rel).read_text() == (first / rel).read_text(), rel


def test_catalog_file_travels_both_ways(library_blend, tmp_path):
    catalog = "VERSION 1\n\n" + CATALOG_ID + ":Tools:Tools\n"
    (library_blend.parent / CATALOG_FILENAME).write_text(catalog)

    src = tmp_path / "src"
    dump_library(library_blend, src)
    assert (src / CATALOG_FILENAME).read_text() == catalog

    rebuilt_path = tmp_path / "rebuilt" / "library.blend"
    build_library(src, rebuilt_path)
    assert (rebuilt_path.parent / CATALOG_FILENAME).read_text() == catalog
