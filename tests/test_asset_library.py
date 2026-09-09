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

    code = written["Scale Up"].read_text(encoding="utf-8")
    # The asset's class and its nested dependency are both in the file.
    assert "class ScaleUp(CustomGeometryGroup):" in code
    assert "class Doubler(CustomGeometryGroup):" in code
    assert "ASSET = ScaleUp" in code
    # Metadata and non-default tree flags are dumped.
    assert CATALOG_ID in code
    assert '"tags": ("mesh", "transform")' in code
    assert '"is_modifier": True' in code
    # The shader asset carries no metadata or tree flags — no empty footers.
    shader_code = written["Flat Red"].read_text(encoding="utf-8")
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
    code = path.read_text(encoding="utf-8")
    assert "catalog_simple_name" not in code  # no longer dumped at all
    path.write_text(
        code + '\nASSET_METADATA["catalog_simple_name"] = "Tools"\n', encoding="utf-8"
    )

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
    shared_code = (out / "geometry" / "_shared" / "doubler.py").read_text(
        encoding="utf-8"
    )
    assert "class Doubler(CustomGeometryGroup):" in shared_code
    assert "ASSET" not in shared_code

    # The nested asset keeps its class in its own module and imports Doubler.
    inner_code = written["Inner Widget"].read_text(encoding="utf-8")
    assert "class InnerWidget(CustomGeometryGroup):" in inner_code
    assert "from ._shared.doubler import Doubler" in inner_code
    assert "class Doubler" not in inner_code
    assert "ASSET = InnerWidget" in inner_code

    # Outer A imports both the nested asset and the shared helper it also
    # uses directly; neither class is re-defined.
    a_code = written["Outer A"].read_text(encoding="utf-8")
    assert "from .inner_widget import InnerWidget" in a_code
    assert "from ._shared.doubler import Doubler" in a_code
    assert "class InnerWidget" not in a_code and "class Doubler" not in a_code

    # Outer B only references the nested asset, so it imports only that.
    b_code = written["Outer B"].read_text(encoding="utf-8")
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

    code = (out / "materials" / "test_glow.py").read_text(encoding="utf-8")
    assert "class TestGlow(CustomShaderGroup):" in code
    assert "MATERIAL = TestGlow" in code
    assert 'MATERIAL_NAME = "Test Glow"' in code
    assert '"metallic": 1.0' in code
    assert "ASSET" not in code  # a material module is not an asset module

    asset_code = written["Glowing Grid"].read_text(encoding="utf-8")
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
        assert (second / rel).read_text(encoding="utf-8") == (first / rel).read_text(
            encoding="utf-8"
        ), rel


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
        assert (second / rel).read_text(encoding="utf-8") == (first / rel).read_text(
            encoding="utf-8"
        ), rel


def test_digit_led_asset_name_roundtrips(tmp_path):
    """An asset whose name starts with a digit ("2 Index Angle") must not get
    a "_"-prefixed module — the build skips those as non-root (the _shared
    convention) and would silently drop the asset from the library."""
    path = tmp_path / "library.blend"
    with TreeBuilder("2 Sided") as tree:
        geo = tree.inputs.geometry("Geometry")
        geo >> tree.outputs.geometry("Geometry")
    tree.tree.asset_mark()
    bpy.data.libraries.write(str(path), {tree.tree}, fake_user=True)
    _clear_node_groups()

    src = tmp_path / "src"
    written = dump_library(path, src)
    assert written["2 Sided"] == src / "geometry" / "n2_sided.py"
    names = build_library(src, tmp_path / "rebuilt.blend")
    assert names == ["2 Sided"]


def test_catalog_file_travels_both_ways(library_blend, tmp_path):
    catalog = "VERSION 1\n\n" + CATALOG_ID + ":Tools:Tools\n"
    (library_blend.parent / CATALOG_FILENAME).write_text(catalog, encoding="utf-8")

    src = tmp_path / "src"
    dump_library(library_blend, src)
    assert (src / CATALOG_FILENAME).read_text(encoding="utf-8") == catalog

    rebuilt_path = tmp_path / "rebuilt" / "library.blend"
    build_library(src, rebuilt_path)
    assert (rebuilt_path.parent / CATALOG_FILENAME).read_text(
        encoding="utf-8"
    ) == catalog


# ---------------------------------------------------------------------------
# Error paths, collisions, and legacy-format compatibility
# ---------------------------------------------------------------------------


def test_dump_missing_blend_errors(tmp_path):
    with pytest.raises(FileNotFoundError, match="Asset library not found"):
        dump_library(tmp_path / "nope.blend", tmp_path / "src")


def test_dump_refuses_renamed_dependencies(nested_library_blend, tmp_path):
    """A pre-existing group matching a *dependency* name (not an asset name)
    slips past the upfront clash check but renames on append — caught by the
    post-append guard."""
    with TreeBuilder("Doubler"):
        pass
    with pytest.raises(RuntimeError, match="renamed dependency groups"):
        dump_library(nested_library_blend, tmp_path / "src")


def test_dump_skips_unsupported_tree_types(tmp_path, capsys):
    tex = bpy.data.node_groups.new("Tex Asset", "TextureNodeTree")
    tex.asset_mark()
    path = tmp_path / "library.blend"
    bpy.data.libraries.write(str(path), {tex}, fake_user=True)
    _clear_node_groups()

    written = dump_library(path, tmp_path / "src")
    assert written == {}
    assert "unsupported tree type" in capsys.readouterr().out


def test_dump_material_tree_name_collision_errors(tmp_path):
    """A *dumped* node group named like an embedded material tree would be
    clobbered by the per-emission class-name override — refused with
    guidance."""

    class _Weird(CustomGeometryGroup):
        _name = "Shader Nodetree"

        def _build_group(self, tree):
            tree.inputs.float("V") >> tree.outputs.float("V")

    material = bpy.data.materials.new("Collide Mat")
    with TreeBuilder("Collider Asset") as tree:
        geo = tree.inputs.geometry("Geometry")
        _Weird(V=1.0)
        set_mat = g.SetMaterial(geometry=geo, material=material)
        set_mat >> tree.outputs.geometry("Geometry")
    tree.tree.asset_mark()
    path = tmp_path / "library.blend"
    bpy.data.libraries.write(str(path), {tree.tree}, fake_user=True)
    _clear_node_groups()
    bpy.data.materials.remove(material)

    with pytest.raises(RuntimeError, match="embedded tree"):
        dump_library(path, tmp_path / "src")


def test_resolve_dependencies_errors():
    from nodebpy.assets._library import _resolve_dependencies

    with pytest.raises(FileNotFoundError, match="Resources library not found"):
        _resolve_dependencies({"images": {"X"}}, Path("/nope.blend"), "error")
    with pytest.raises(RuntimeError, match="Cannot placeholder"):
        _resolve_dependencies({"fonts": {"SomeFont"}}, None, "drop")


def test_build_rejects_malformed_modules(library_blend, tmp_path):
    src = tmp_path / "src"
    dump_library(library_blend, src)

    rogue = src / "geometry" / "rogue.py"
    rogue.write_text("x = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="neither ASSET nor MATERIAL"):
        build_library(src, tmp_path / "rebuilt.blend")
    rogue.write_text("ASSET = 42\n", encoding="utf-8")
    with pytest.raises(TypeError, match="not a node-group class"):
        build_library(src, tmp_path / "rebuilt.blend")
    rogue.write_text("MATERIAL = 42\nMATERIAL_NAME = 'X'\n", encoding="utf-8")
    with pytest.raises(TypeError, match="MATERIAL is not a node-group class"):
        build_library(src, tmp_path / "rebuilt.blend")


def test_build_applies_legacy_tree_properties_footer(library_blend, tmp_path):
    """Older dumps carried tree flags in a TREE_PROPERTIES footer; build
    still applies them."""
    src = tmp_path / "src"
    written = dump_library(library_blend, src)
    path = written["Flat Red"]
    path.write_text(
        path.read_text(encoding="utf-8")
        + '\nTREE_PROPERTIES = {"description": "legacy"}\n',
        encoding="utf-8",
    )

    build_library(src, tmp_path / "rebuilt.blend")
    assert bpy.data.node_groups["Flat Red"].description == "legacy"


def test_build_skips_unknown_material_property(
    material_library_blend, tmp_path, capsys
):
    src = tmp_path / "src"
    dump_library(material_library_blend, src)
    mat_module = src / "materials" / "test_glow.py"
    mat_module.write_text(
        mat_module.read_text(encoding="utf-8")
        + '\nMATERIAL_PROPERTIES = {"not_a_real_property": 1}\n',
        encoding="utf-8",
    )
    names = build_library(src, tmp_path / "rebuilt.blend", on_missing="drop")
    assert "Glowing Grid" in names
    assert "skipping read-only material property" in capsys.readouterr().out


def test_colliding_names_get_suffixes(tmp_path):
    """Assets whose names normalize identically get distinct class names and
    module stems, and still round-trip."""
    for name in ("Twin!", "Twin?"):
        with TreeBuilder(name) as tree:
            tree.inputs.float("A") >> tree.outputs.float("B")
        tree.tree.asset_mark()
    trees = {t for t in bpy.data.node_groups}
    path = tmp_path / "library.blend"
    bpy.data.libraries.write(str(path), trees, fake_user=True)
    _clear_node_groups()

    src = tmp_path / "src"
    written = dump_library(path, src)
    assert {p.name for p in written.values()} == {"twin.py", "twin_2.py"}
    code = "".join(p.read_text(encoding="utf-8") for p in written.values())
    assert "class Twin(" in code and "class Twin2(" in code

    names = build_library(src, tmp_path / "rebuilt.blend")
    assert set(names) == {"Twin!", "Twin?"}


def test_cli_dump_and_build_dispatch(monkeypatch, library_blend, tmp_path, capsys):
    """``python -m nodebpy.assets dump/build`` dispatches to the library CLI."""
    import sys as _sys

    from nodebpy.assets.__main__ import main

    src = tmp_path / "src"
    monkeypatch.setattr(_sys, "argv", ["prog", "dump", str(library_blend), str(src)])
    main()
    assert "Dumped 2 assets" in capsys.readouterr().out

    rebuilt = tmp_path / "rebuilt.blend"
    monkeypatch.setattr(_sys, "argv", ["prog", "build", str(src), str(rebuilt)])
    main()
    assert "Built" in capsys.readouterr().out
    assert rebuilt.is_file()


# ---------------------------------------------------------------------------
# typed_api: merged classes (typed interface + _build_group source of truth)
# ---------------------------------------------------------------------------


def test_typed_param_names_collisions_and_reserved():
    from types import SimpleNamespace as NS

    from nodebpy.builder._utils import typed_param_names

    sockets = [
        NS(name="Scale", identifier="Socket_1"),
        NS(name="Scale", identifier="Socket_2"),
        NS(name="Self", identifier="Socket_3"),
        NS(name="Geometry", identifier="Socket_4"),
        NS(name="__extend__", identifier="__extend__"),
    ]
    params = typed_param_names(sockets)
    # Colliding names fall back to identifiers; reserved names get a suffix;
    # __extend__ virtual sockets are skipped entirely.
    assert params == {
        "Socket_1": "socket_1",
        "Socket_2": "socket_2",
        "Socket_3": "self_2",
        "Socket_4": "geometry",
    }


def test_typed_api_dump_merges_interface(nested_library_blend, tmp_path):
    """typed_api merges the asset API into the dumped class: Asset*Group base
    with _library, numpydoc docstring, accessors, typed __init__ keyed by
    socket name, typed call sites, and __init__.py re-exports; shared helper
    modules get the typed API but stay Custom*Group."""
    import os

    out = tmp_path / "src"
    dump_library(nested_library_blend, out, typed_api=True)

    outer_a = (out / "geometry" / "outer_a.py").read_text(encoding="utf-8")
    assert "class OuterA(AssetGeometryGroup):" in outer_a
    assert '_asset_name = "Outer A"' in outer_a
    relpath = Path(os.path.relpath(nested_library_blend, out / "geometry")).as_posix()
    assert f'_library = PackageLibrary(__file__, "{relpath}")' in outer_a
    assert "Parameters" in outer_a and "Outputs" in outer_a
    assert "class _Inputs(SocketAccessor):" in outer_a
    assert 'super().__init__(**{"Geometry": geometry, "Factor": factor})' in outer_a
    assert "def _build_group(self, tree):" in outer_a
    # Group calls inside _build_group use the typed parameter names.
    assert "InnerWidget(geometry=geometry, amount=Doubler(value=factor))" in outer_a
    assert "ASSET = OuterA" in outer_a

    # Shared helpers are typed but stay Custom*Group — they are not assets.
    doubler = (out / "geometry" / "_shared" / "doubler.py").read_text(encoding="utf-8")
    assert "class Doubler(CustomGeometryGroup):" in doubler
    assert "_library =" not in doubler
    assert "class _Inputs(SocketAccessor):" in doubler

    init = (out / "geometry" / "__init__.py").read_text(encoding="utf-8")
    assert "from .outer_a import OuterA" in init
    assert "from .inner_widget import InnerWidget" in init
    assert '"OuterB",' in init


def test_typed_api_roundtrip_stable_and_builds_from_source(
    nested_library_blend, tmp_path
):
    """dump(typed) → build → dump(typed) is byte-stable when the .blend sits
    at the same relative location, and the build constructs every tree from
    _build_group source rather than appending."""
    import shutil as _shutil

    pkg1 = tmp_path / "pkg1"
    pkg1.mkdir()
    blend1 = pkg1 / "assets.blend"
    _shutil.copyfile(nested_library_blend, blend1)
    first = pkg1 / "nodes"
    dump_library(blend1, first, typed_api=True)

    pkg2 = tmp_path / "pkg2"
    pkg2.mkdir()
    blend2 = pkg2 / "assets.blend"
    names = build_library(first, blend2)
    assert set(names) == {"Inner Widget", "Outer A", "Outer B"}
    # Built locally from source, not appended from the library.
    assert all(bpy.data.node_groups[n].library is None for n in names)
    _clear_node_groups()

    second = pkg2 / "nodes"
    dump_library(blend2, second, typed_api=True)
    first_files = sorted(p.relative_to(first) for p in first.rglob("*.py"))
    second_files = sorted(p.relative_to(second) for p in second.rglob("*.py"))
    assert first_files == second_files
    for rel in first_files:
        assert (second / rel).read_text(encoding="utf-8") == (first / rel).read_text(
            encoding="utf-8"
        ), rel


def test_typed_api_create_group_appends_then_falls_back(nested_library_blend, tmp_path):
    """At runtime a merged class appends its group from the .blend; under
    build_from_source() — or when the .blend is missing — it builds from its
    _build_group recipe instead."""
    from nodebpy.assets._library import _import_source_modules, _source_files
    from nodebpy.builder import build_from_source

    out = tmp_path / "src"
    dump_library(nested_library_blend, out, typed_api=True)
    files = _source_files(out)
    modules = _import_source_modules(out, files)
    outer_b = next(m.ASSET for m in modules if m.ASSET._name == "Outer B")

    appended = outer_b.create_group()
    assert appended.library is not None  # linked from the .blend
    _clear_node_groups()

    with build_from_source():
        built = outer_b.create_group()
    assert built.library is None
    _clear_node_groups()

    outer_b._library.relative = "does_not_exist.blend"
    fallback = outer_b.create_group()
    assert fallback.library is None
    _clear_node_groups()


def test_typed_api_instantiates_with_typed_kwargs(nested_library_blend, tmp_path):
    """The typed __init__ links inputs by socket name on the appended tree."""
    from nodebpy.assets._library import _import_source_modules, _source_files

    out = tmp_path / "src"
    dump_library(nested_library_blend, out, typed_api=True)
    modules = _import_source_modules(out, _source_files(out))
    outer_a = next(m.ASSET for m in modules if m.ASSET._name == "Outer A")

    with TreeBuilder("Host") as host:
        call = outer_a(geometry=host.inputs.geometry("Geo"), factor=2.0)
        call.o.geometry >> host.outputs.geometry("Out")
    node = host.tree.nodes["Outer A"]
    assert node.inputs["Factor"].default_value == 2.0
    assert node.inputs["Geometry"].is_linked
    _clear_node_groups()


def test_typed_api_duplicate_socket_names(tmp_path):
    """Duplicate interface names ride the _named_links mechanism in the typed
    __init__ and still build from source."""
    with TreeBuilder("Dup") as tb:
        a = tb.inputs.float("Value")
        b = tb.inputs.float("Value", 3.0)
        g.Math.add(a, b) >> tb.outputs.float("Sum")
    tb.tree.asset_mark()
    blend = tmp_path / "dup.blend"
    bpy.data.libraries.write(str(blend), {tb.tree}, fake_user=True)
    _clear_node_groups()

    out = tmp_path / "src"
    dump_library(blend, out, typed_api=True)
    module = (out / "geometry" / "dup.py").read_text(encoding="utf-8")
    assert "_named_links=[" in module

    rebuilt = tmp_path / "rebuilt.blend"
    build_library(out, rebuilt)
    tree = bpy.data.node_groups["Dup"]
    values = [
        item.default_value
        for item in tree.interface.items_tree
        if item.item_type == "SOCKET" and item.in_out == "INPUT"
    ]
    assert values == [0.0, 3.0]
    _clear_node_groups()


def test_typed_api_material_library_builds(material_library_blend, tmp_path):
    """Material modules coexist with typed asset modules and still build."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    src = pkg / "nodes"
    dump_library(material_library_blend, src, typed_api=True)
    rebuilt = pkg / "assets.blend"
    names = build_library(src, rebuilt, resources=material_library_blend)
    assert names == ["Glowing Grid"]
    assert bpy.data.node_groups["Glowing Grid"].library is None
    _clear_node_groups()
    for coll in ("materials", "images"):
        data = getattr(bpy.data, coll)
        for db in list(data):
            data.remove(db)


def test_typed_api_keeps_handwritten_dir_init(library_blend, tmp_path):
    """A hand-written tree-dir __init__.py is never overwritten."""
    out = tmp_path / "src"
    (out / "geometry").mkdir(parents=True)
    custom = "# my hand-rolled exports\n"
    (out / "geometry" / "__init__.py").write_text(custom, encoding="utf-8")
    dump_library(library_blend, out, typed_api=True)
    assert (out / "geometry" / "__init__.py").read_text(encoding="utf-8") == custom
    # The untouched shader dir still gets generated exports.
    shader_init = (out / "shader" / "__init__.py").read_text(encoding="utf-8")
    assert "from .flat_red import FlatRed" in shader_init


def test_cli_dump_typed_api(monkeypatch, library_blend, tmp_path, capsys):
    """--typed-api reaches dump_library through the CLI."""
    import sys as _sys

    from nodebpy.assets.__main__ import main

    src = tmp_path / "src"
    monkeypatch.setattr(
        _sys, "argv", ["prog", "dump", str(library_blend), str(src), "--typed-api"]
    )
    main()
    assert "Dumped 2 assets" in capsys.readouterr().out
    code = (src / "geometry" / "scale_up.py").read_text(encoding="utf-8")
    assert "class ScaleUp(AssetGeometryGroup):" in code


def _write_compositor_library(path: Path) -> None:
    """Write a library with one compositor asset. Leaves the session clean."""
    from nodebpy import compositor as c

    with TreeBuilder.compositor("Grade Boost") as tb:
        img = tb.inputs.color("Image")
        fac = tb.inputs.float("Boost", 0.5, description="How much to boost")
        blur = c.Blur(image=img)
        c.Mix(factor_float=fac, a_color=img, b_color=blur, data_type="RGBA") >> (
            tb.outputs.color("Image")
        )
    tb.tree.asset_mark()
    assert tb.tree.asset_data is not None
    tb.tree.asset_data.description = "Boosts an image"
    bpy.data.libraries.write(str(path), {tb.tree}, fake_user=True)
    _clear_node_groups()


def test_compositor_roundtrip_plain_and_typed(tmp_path):
    """Compositor assets round-trip in both dump modes: plain
    Custom*Group sources rebuild the .blend, and typed_api merges an
    appending AssetCompositorGroup with the _build_group recipe."""
    from nodebpy.assets._library import _import_source_modules, _source_files

    pkg1 = tmp_path / "pkg1"
    pkg1.mkdir()
    blend = pkg1 / "assets.blend"
    _write_compositor_library(blend)

    # Plain dump → build.
    plain = tmp_path / "plain"
    dump_library(blend, plain)
    code = (plain / "compositor" / "grade_boost.py").read_text(encoding="utf-8")
    assert "class GradeBoost(CustomCompositorGroup):" in code
    rebuilt_plain = tmp_path / "plain.blend"
    assert build_library(plain, rebuilt_plain) == ["Grade Boost"]
    _clear_node_groups()

    # Typed dump: merged class, appends at runtime, builds from source.
    first = pkg1 / "nodes"
    dump_library(blend, first, typed_api=True)
    typed = (first / "compositor" / "grade_boost.py").read_text(encoding="utf-8")
    assert "class GradeBoost(AssetCompositorGroup):" in typed
    assert '_library = PackageLibrary(__file__, "../../assets.blend")' in typed
    assert 'super().__init__(**{"Image": image, "Boost": boost})' in typed
    assert "def _build_group(self, tree):" in typed
    init = (first / "compositor" / "__init__.py").read_text(encoding="utf-8")
    assert "from .grade_boost import GradeBoost" in init

    pkg2 = tmp_path / "pkg2"
    pkg2.mkdir()
    blend2 = pkg2 / "assets.blend"
    assert build_library(first, blend2) == ["Grade Boost"]
    assert bpy.data.node_groups["Grade Boost"].library is None
    _clear_node_groups()

    # Byte-stable across the round trip (same relative blend location).
    second = pkg2 / "nodes"
    dump_library(blend2, second, typed_api=True)
    for rel in sorted(p.relative_to(first) for p in first.rglob("*.py")):
        assert (second / rel).read_text(encoding="utf-8") == (first / rel).read_text(
            encoding="utf-8"
        ), rel

    # Runtime: typed instantiation appends the group into a compositor tree.
    modules = _import_source_modules(first, _source_files(first))
    grade_boost = next(m.ASSET for m in modules if m.ASSET._name == "Grade Boost")
    with TreeBuilder.compositor("Host") as host:
        call = grade_boost(image=host.inputs.color("In"), boost=0.8)
        call.o.image >> host.outputs.color("Out")
    assert bpy.data.node_groups["Grade Boost"].library is not None
    node = host.tree.nodes["Grade Boost"]
    assert round(node.inputs["Boost"].default_value, 3) == 0.8
    _clear_node_groups()
