# SPDX-License-Identifier: GPL-3.0-or-later
"""Deep round-trip parity: dump → build must preserve everything on the
selected surfaces, verified via tree_clipper's full JSON serialization."""

import bpy
import pytest

pytest.importorskip("tree_clipper")

from nodebpy.assets import build_library, dump_library
from nodebpy.export.parity import (
    SURFACES,
    compare_libraries,
    format_report,
    serialize_library,
)

from .test_asset_library import (
    _clear_node_groups,
    _write_library,
    _write_material_library,
    _write_nested_library,
)


def _clear_session():
    """Remove everything a library load may have brought in — a leftover
    datablock would be silently reused (and renamed around) by the next
    append."""
    _clear_node_groups()
    bpy.data.batch_remove(list(bpy.data.materials) + list(bpy.data.images))


def _capture_blend(path):
    """Serialize a blend's assets in an otherwise clean session."""
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(path), link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = list(src.node_groups)
    capture = serialize_library(list(dst.node_groups))
    _clear_session()
    return capture


def _roundtrip_capture(tmp_path, writer, **dump_kwargs):
    """Write a fixture library, round-trip it through dump → build, and
    return (original capture, rebuilt capture)."""
    blend = tmp_path / "library.blend"
    writer(blend)
    original = _capture_blend(blend)

    src = tmp_path / "src"
    dump_library(blend, src, **dump_kwargs)
    rebuilt_blend = tmp_path / "rebuilt.blend"
    build_library(src, rebuilt_blend, resources=blend)
    _clear_session()
    return original, _capture_blend(rebuilt_blend)


@pytest.mark.parametrize(
    "writer",
    [_write_library, _write_nested_library, _write_material_library],
    ids=["basic", "nested", "materials"],
)
def test_functional_parity(writer, tmp_path):
    """With every cosmetic surface ignored, a round-trip must be a perfect
    functional match — any finding here is a real serialization gap."""
    original, rebuilt = _roundtrip_capture(tmp_path, writer)
    findings = compare_libraries(original, rebuilt, ignore=SURFACES)
    assert not findings, format_report(findings)


@pytest.mark.parametrize(
    "writer",
    [_write_library, _write_nested_library],
    ids=["basic", "nested"],
)
def test_full_parity_with_snapshot_positions(writer, tmp_path):
    """A snapshot-positions round-trip of a nodebpy-authored library reaches
    parity on *every* surface (nodebpy-assigned node names make the position
    snapshot lossless, and no reroutes or bespoke presentation exist)."""
    original, rebuilt = _roundtrip_capture(tmp_path, writer, snapshot_positions=True)
    findings = compare_libraries(original, rebuilt, ignore=frozenset())
    assert not findings, format_report(findings)


def test_unknown_surface_rejected():
    with pytest.raises(ValueError, match="positionz"):
        compare_libraries({}, {}, ignore={"positionz"})


# ---------------------------------------------------------------------------
# Direct comparison behaviour (no dump/build round-trip involved)
# ---------------------------------------------------------------------------

from nodebpy import TreeBuilder
from nodebpy import geometry as g


def _capture_variant(add_value, description, extra):
    """Serialize one small tree (plus optionally an extra tree), then clean."""
    with TreeBuilder("Alpha") as tree:
        fac = tree.inputs.float("Fac", description="in")
        g.Math.add(fac, add_value) >> tree.outputs.float("Out")
    tree.tree.description = description
    trees = [tree.tree]
    if extra:
        with TreeBuilder(extra) as other:
            other.inputs.float("X") >> other.outputs.float("Y")
        trees.append(other.tree)
    capture = serialize_library(trees)
    _clear_session()
    return capture


def test_compare_reports_each_difference_kind():
    a = _capture_variant(1.0, "one", "OnlyA")
    b = _capture_variant(2.0, "two", "OnlyB")

    findings = compare_libraries(a, b, ignore=SURFACES)
    kinds = {(f.context, f.path) for f in findings}
    assert ("tree", "presence") in kinds  # OnlyA / OnlyB
    assert ("tree", "description") in kinds  # "one" -> "two"
    # The 1.0 vs 2.0 operand shows as a node value-multiset difference.
    assert any(c == "node" and "ShaderNodeMath" in p for c, p in kinds)

    report = format_report(findings)
    assert "findings in" in report
    assert "[tree] description" in report


def test_interface_differences_reported():
    with TreeBuilder("Iface") as tree_a:
        tree_a.inputs.float("Fac", description="first")
        tree_a.inputs.float("Extra")
        tree_a.inputs.float("X") >> tree_a.outputs.float("Y")
    a = serialize_library([tree_a.tree])
    _clear_session()
    with TreeBuilder("Iface") as tree_b:
        tree_b.inputs.float("Fac", description="second")
        tree_b.inputs.float("X") >> tree_b.outputs.float("Y")
    b = serialize_library([tree_b.tree])
    _clear_session()

    kinds = {(f.context, f.path) for f in compare_libraries(a, b, ignore=SURFACES)}
    assert ("interface", "item count") in kinds

    # Same item count → per-item comparison kicks in.
    with TreeBuilder("Iface") as tree_c:
        tree_c.inputs.float("Fac", description="third")
        tree_c.inputs.float("X") >> tree_c.outputs.float("Y")
    c = serialize_library([tree_c.tree])
    _clear_session()
    kinds = {(f.context, f.path) for f in compare_libraries(b, c, ignore=SURFACES)}
    assert ("interface", "Fac.description") in kinds


def test_inert_links_do_not_count():
    """Stale links into inactive sockets (a Mix wired for every type, then
    set to RGBA) and reroute hops are invisible to the functional surface."""
    with TreeBuilder("Inert", ignore_visibility=True) as tree_a:
        col = tree_a.inputs.color("Color")
        fac = tree_a.inputs.float("Fac")
        mix = g.Mix(
            data_type="RGBA",
            factor_float=fac,
            a_color=col,
            b_color=col,
            a_float=fac,  # stale link into an inactive socket
            b_float=fac,
        )
        mix.o.result_color >> tree_a.outputs.color("Result")
    a = serialize_library([tree_a.tree])
    _clear_session()

    with TreeBuilder("Inert") as tree_b:
        col = tree_b.inputs.color("Color")
        fac = tree_b.inputs.float("Fac")
        mix = g.Mix(data_type="RGBA", factor_float=fac, a_color=col, b_color=col)
        mix.o.result_color >> tree_b.outputs.color("Result")
    b = serialize_library([tree_b.tree])
    _clear_session()

    findings = compare_libraries(a, b, ignore=SURFACES)
    assert not findings, format_report(findings)


def test_reroute_hops_do_not_count():
    with TreeBuilder("Hop", arrange=None) as tree_a:
        geo = tree_a.inputs.geometry("Geometry")
        out = tree_a.outputs.geometry("Out")
        sp = g.SetPosition(geometry=geo)
        reroute = tree_a.tree.nodes.new("NodeReroute")
        tree_a.tree.links.new(sp.node.outputs[0], reroute.inputs[0])
        tree_a.tree.links.new(reroute.outputs[0], out.socket)
    a = serialize_library([tree_a.tree])
    _clear_session()

    with TreeBuilder("Hop") as tree_b:
        geo = tree_b.inputs.geometry("Geometry")
        g.SetPosition(geometry=geo) >> tree_b.outputs.geometry("Out")
    b = serialize_library([tree_b.tree])
    _clear_session()

    findings = compare_libraries(a, b, ignore=SURFACES)
    assert not findings, format_report(findings)
    # Without the reroutes surface, the extra hop is a difference.
    assert compare_libraries(a, b, ignore=frozenset())


def test_material_tree_serializes():
    """An embedded material tree serializes via its owning material and is
    keyed by the material (embedded trees all share one name)."""
    material = bpy.data.materials.new("Cap Mat")
    assert material.node_tree is not None
    capture = serialize_library([material.node_tree])
    assert "material:Cap Mat" in capture
    bpy.data.materials.remove(material)


def test_cli_compares_two_blends(tmp_path, capsys):
    from nodebpy.export.parity import main

    blend_a = tmp_path / "a.blend"
    blend_b = tmp_path / "b.blend"
    _write_library(blend_a)
    _write_library(blend_b)

    assert main([str(blend_a), str(blend_b), "--ignore", "positions"]) == 0
    assert "no differences" in capsys.readouterr().out

    with TreeBuilder("Scale Up") as tree:  # same name, different content
        tree.inputs.float("Other") >> tree.outputs.float("Out")
    tree.tree.asset_mark()
    blend_c = tmp_path / "c.blend"
    bpy.data.libraries.write(str(blend_c), {tree.tree}, fake_user=True)
    _clear_session()

    assert main([str(blend_a), str(blend_c)]) == 1
    assert "findings" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Real-library round trips: every bundled essentials library and the
# MolecularNodes asset library must reach functional parity through
# dump → build. These are the example geometry, shader and compositor trees
# the rest of the suite already exercises.
# ---------------------------------------------------------------------------

from pathlib import Path

from nodebpy.builder import BundledLibrary

MN_FILE_PATH = (
    Path.cwd().parent / "MolecularNodes/molecularnodes/assets/node_data_file.blend"
)


def _clear_all_data():
    """Also drop objects/collections the startup file or a library load holds
    — a same-named leftover would make the dump's rename guard fire."""
    _clear_node_groups()
    bpy.data.batch_remove(
        list(bpy.data.materials)
        + list(bpy.data.images)
        + list(bpy.data.objects)
        + list(bpy.data.collections)
    )


def _capture_all(path):
    with bpy.data.libraries.load(  # ty: ignore[invalid-context-manager]
        str(path), link=False, assets_only=True
    ) as (src, dst):
        dst.node_groups = list(src.node_groups)
    capture = serialize_library(list(dst.node_groups))
    _clear_all_data()
    return capture


def _assert_library_roundtrip(blend, tmp_path):
    _clear_all_data()
    original = _capture_all(blend)
    src = tmp_path / "src"
    dump_library(blend, src, format=False)
    rebuilt = tmp_path / "rebuilt.blend"
    build_library(src, rebuilt, resources=blend)
    _clear_all_data()
    findings = compare_libraries(original, _capture_all(rebuilt), ignore=SURFACES)
    assert not findings, format_report(findings)


@pytest.mark.parametrize(
    "filename",
    [
        "geometry_nodes_essentials.blend",
        "shading_nodes_essentials.blend",
        "compositing_nodes_essentials.blend",
    ],
)
def test_functional_parity_bundled_essentials(filename, tmp_path):
    path = Path(BundledLibrary(filename).path())
    if not path.is_file():
        pytest.skip(f"bundled library {filename} not installed")
    _assert_library_roundtrip(path, tmp_path)


@pytest.mark.skipif(
    not MN_FILE_PATH.exists(),
    reason="MolecularNodes asset library not found",
)
def test_functional_parity_molecular_nodes(tmp_path):
    _assert_library_roundtrip(MN_FILE_PATH, tmp_path)
