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


class _InnerWidget(CustomGeometryGroup):
    """A group that is an asset itself, is nested inside other assets, and
    itself nests the shared ``Doubler`` helper — the deepest sharing case."""

    _name = "Inner Widget"

    def _build_group(self, tree):
        geo = tree.inputs.geometry("Geometry")
        amount = tree.inputs.float("Amount")
        doubled = _Doubler(Value=amount).o.doubled
        offset = g.CombineXYZ(z=doubled)
        g.SetPosition(geometry=geo, offset=offset) >> tree.outputs.geometry("Geometry")


def _write_nested_library(path: Path) -> None:
    """Write a library where asset "Inner Widget" is nested inside assets
    "Outer A" and "Outer B", "Outer A" also uses the non-asset ``Doubler``
    directly, and ``Doubler`` is reachable from all three assets."""
    inner = _InnerWidget.create_group()
    inner.asset_mark()
    assert inner.asset_data is not None
    inner.asset_data.description = "Inner widget"

    with TreeBuilder("Outer A") as outer_a:
        geo = outer_a.inputs.geometry("Geometry")
        factor = outer_a.inputs.float("Factor")
        doubled = _Doubler(Value=factor).o.doubled
        widget = _InnerWidget(Geometry=geo, Amount=doubled)
        widget.o.geometry >> outer_a.outputs.geometry("Geometry")
    outer_a.tree.asset_mark()

    with TreeBuilder("Outer B") as outer_b:
        geo = outer_b.inputs.geometry("Geometry")
        widget = _InnerWidget(Geometry=geo, Amount=1.0)
        widget.o.geometry >> outer_b.outputs.geometry("Geometry")
    outer_b.tree.asset_mark()

    bpy.data.libraries.write(
        str(path), {inner, outer_a.tree, outer_b.tree}, fake_user=True
    )
    _clear_node_groups()


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


@pytest.fixture
def nested_library_blend(tmp_path):
    path = tmp_path / "nested_library.blend"
    _write_nested_library(path)
    return path


def _write_material_library(path: Path) -> None:
    """Write a library whose one geometry asset references a material (with a
    non-default property) and an image datablock. Leaves the session clean."""
    image = bpy.data.images.new("Grid Tex", 4, 4)
    material = bpy.data.materials.new("Test Glow")
    material.metallic = 1.0
    assert material.node_tree is not None
    material.node_tree.nodes.clear()
    with TreeBuilder(material.node_tree) as shader_tree:
        emission = s.Emission(color=(1.0, 0.5, 0.0, 1.0), strength=5.0)
        s.MaterialOutput(surface=emission)
    del shader_tree

    with TreeBuilder("Glowing Grid") as tree:
        geo = tree.inputs.geometry("Geometry")
        g.ImageTexture(image=image)  # dangling on purpose: an image dependency
        set_mat = g.SetMaterial(geometry=geo, material=material)
        set_mat >> tree.outputs.geometry("Geometry")
    tree.tree.asset_mark()

    bpy.data.libraries.write(str(path), {tree.tree}, fake_user=True)
    _clear_node_groups()
    bpy.data.materials.remove(material)
    bpy.data.images.remove(image)


@pytest.fixture
def material_library_blend(tmp_path):
    path = tmp_path / "material_library.blend"
    _write_material_library(path)
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


def test_build_ignores_stale_catalog_simple_name(library_blend, tmp_path):
    """``catalog_simple_name`` is read-only on AssetMetaData (derived from
    ``catalog_id``), so a dump that recorded it — as older nodebpy versions
    did — must still build rather than crash on the setattr."""
    src = tmp_path / "src"
    written = dump_library(library_blend, src)
    assert not bpy.data.node_groups
    path = written["Scale Up"]
    code = path.read_text()
    assert "catalog_simple_name" not in code  # no longer dumped at all
    path.write_text(code + '\nASSET_METADATA["catalog_simple_name"] = "Tools"\n')

    names = build_library(src, tmp_path / "rebuilt.blend")
    assert "Scale Up" in names
    assert bpy.data.node_groups["Scale Up"].asset_data.catalog_id == CATALOG_ID


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


def test_shared_and_nested_assets_split_into_modules(nested_library_blend, tmp_path):
    """Every group class is defined exactly once: a group shared by several
    assets gets its own ``_shared`` module, and an asset nested inside other
    assets keeps its class in its own module — dependents import both."""
    out = tmp_path / "src"
    written = dump_library(nested_library_blend, out)
    assert set(written) == {"Inner Widget", "Outer A", "Outer B"}

    # Doubler is reachable from all three assets → one module under _shared/,
    # with no ASSET marker (it is not an asset).
    shared_code = (out / "geometry" / "_shared" / "doubler.py").read_text()
    assert "class Doubler(CustomGeometryGroup):" in shared_code
    assert "ASSET" not in shared_code

    # The nested asset keeps its class in its own module and imports Doubler.
    inner_code = written["Inner Widget"].read_text()
    assert "class InnerWidget(CustomGeometryGroup):" in inner_code
    assert "from ._shared.doubler import Doubler" in inner_code
    assert "class Doubler" not in inner_code
    assert "ASSET = InnerWidget" in inner_code

    # Outer A imports both the nested asset and the shared helper it also
    # uses directly; neither class is re-defined.
    a_code = written["Outer A"].read_text()
    assert "from .inner_widget import InnerWidget" in a_code
    assert "from ._shared.doubler import Doubler" in a_code
    assert "class InnerWidget" not in a_code and "class Doubler" not in a_code

    # Outer B only references the nested asset, so it imports only that.
    b_code = written["Outer B"].read_text()
    assert "from .inner_widget import InnerWidget" in b_code
    assert "doubler" not in b_code

    # Package markers make the relative imports resolvable.
    assert (out / "__init__.py").is_file()
    assert (out / "geometry" / "__init__.py").is_file()
    assert (out / "geometry" / "_shared" / "__init__.py").is_file()


def test_roundtrip_nested_library(nested_library_blend, tmp_path):
    src = tmp_path / "src"
    dump_library(nested_library_blend, src)
    assert not bpy.data.node_groups

    rebuilt_path = tmp_path / "rebuilt.blend"
    names = build_library(src, rebuilt_path)
    assert set(names) == {"Inner Widget", "Outer A", "Outer B"}
    # The shared helper and nested asset were each built exactly once.
    assert "Doubler" in bpy.data.node_groups
    assert bpy.data.node_groups["Inner Widget"].asset_data is not None

    # Structural signatures survive the trip.
    _clear_node_groups()
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(nested_library_blend), link=False, assets_only=True
    ) as (src_lib, dst):
        dst.node_groups = list(src_lib.node_groups)
    originals = {t.name: _structure(t) for t in dst.node_groups}
    _clear_node_groups()

    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(rebuilt_path), link=False, assets_only=True
    ) as (src_lib, dst):
        assert set(src_lib.node_groups) == set(originals)
        dst.node_groups = list(src_lib.node_groups)
    for rebuilt in dst.node_groups:
        assert _structure(rebuilt) == originals[rebuilt.name], rebuilt.name


def test_dump_generates_material_modules(material_library_blend, tmp_path):
    """A referenced material becomes a materials/ module: its shader tree as
    a class recipe, MATERIAL/MATERIAL_NAME markers, non-default material
    properties, and datablock dependencies recorded on the root modules."""
    out = tmp_path / "src"
    written = dump_library(material_library_blend, out)

    code = (out / "materials" / "test_glow.py").read_text()
    assert "class TestGlow(CustomShaderGroup):" in code
    assert "MATERIAL = TestGlow" in code
    assert 'MATERIAL_NAME = "Test Glow"' in code
    assert '"metallic": 1.0' in code
    assert "ASSET" not in code  # a material module is not an asset module

    asset_code = written["Glowing Grid"].read_text()
    assert 'bpy.data.materials["Test Glow"]' in asset_code
    assert '"materials": ("Test Glow",)' in asset_code
    assert '"images": ("Grid Tex",)' in asset_code
    # The dump cleans every appended datablock back out of the session.
    assert not bpy.data.node_groups
    assert "Test Glow" not in bpy.data.materials
    assert "Grid Tex" not in bpy.data.images


def test_roundtrip_material_library(material_library_blend, tmp_path):
    """Materials rebuild from their modules; the remaining image dependency
    is sourced by name from a resources .blend (here: the original library)."""
    src = tmp_path / "src"
    dump_library(material_library_blend, src)

    rebuilt_path = tmp_path / "rebuilt.blend"
    names = build_library(src, rebuilt_path, resources=material_library_blend)
    assert names == ["Glowing Grid"]

    material = bpy.data.materials["Test Glow"]
    assert material.metallic == 1.0
    assert material.node_tree is not None
    assert any(n.bl_idname == "ShaderNodeEmission" for n in material.node_tree.nodes)
    # The asset's Set Material default points at the rebuilt material.
    set_mat = next(
        n
        for n in bpy.data.node_groups["Glowing Grid"].nodes
        if n.bl_idname == "GeometryNodeSetMaterial"
    )
    assert set_mat.inputs["Material"].default_value is material
    # The image came from the resources blend and ships in the library.
    assert "Grid Tex" in bpy.data.images
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(rebuilt_path), link=False
    ) as (src_lib, _):
        assert "Test Glow" in src_lib.materials
        assert "Grid Tex" in src_lib.images


def test_build_missing_datablocks_error(material_library_blend, tmp_path):
    """Without resources, the missing image is a hard, listed error — the
    material never counts as missing because its own module provides it."""
    src = tmp_path / "src"
    dump_library(material_library_blend, src)
    with pytest.raises(RuntimeError, match="Grid Tex"):
        build_library(src, tmp_path / "rebuilt.blend")


def test_build_drop_missing_datablocks(material_library_blend, tmp_path):
    """on_missing='drop' builds via temporary placeholders and deletes them
    before the write, leaving the referencing socket default empty."""
    src = tmp_path / "src"
    dump_library(material_library_blend, src)
    names = build_library(src, tmp_path / "rebuilt.blend", on_missing="drop")
    assert names == ["Glowing Grid"]
    assert "Grid Tex" not in bpy.data.images  # placeholder was cleaned up
    tex = next(
        n
        for n in bpy.data.node_groups["Glowing Grid"].nodes
        if n.bl_idname == "GeometryNodeImageTexture"
    )
    assert tex.inputs["Image"].default_value is None


def test_build_in_presence_of_datablocks(material_library_blend, tmp_path):
    """Datablocks already in the session satisfy dependencies directly, and a
    same-named existing material is reused instead of rebuilt."""
    src = tmp_path / "src"
    dump_library(material_library_blend, src)
    image = bpy.data.images.new("Grid Tex", 2, 2)
    material = bpy.data.materials.new("Test Glow")
    names = build_library(src, tmp_path / "rebuilt.blend")
    assert names == ["Glowing Grid"]
    assert bpy.data.materials["Test Glow"] is material  # reused, not rebuilt
    assert bpy.data.images["Grid Tex"] is image


def test_nested_dump_is_stable_across_a_roundtrip(nested_library_blend, tmp_path):
    """The module split (own file / _shared / embedded) is deterministic, so a
    no-op round-trip of the nested library leaves no VCS diff."""
    first = tmp_path / "first"
    dump_library(nested_library_blend, first)
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
