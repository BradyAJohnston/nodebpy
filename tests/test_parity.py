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
