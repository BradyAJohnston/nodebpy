# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for the ``nodebpy`` command's ``dump --api-only`` and ``lookup``."""

import pytest

from nodebpy.__main__ import main

from .test_asset_library import _write_library


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


def test_api_only_dump_writes_a_module_per_asset(library_blend, tmp_path):
    """Each asset gets a module holding an appending class and no recipe,
    its library path relative to the module; the tree directories re-export
    the classes."""
    out = tmp_path / "pkg"
    main(["dump", "--api-only", str(library_blend), str(out)])
    code = (out / "geometry" / "scale_up.py").read_text(encoding="utf-8")
    assert "class ScaleUp(AssetGeometryGroup)" in code
    assert '"../../library.blend"' in code
    assert "_build_group" not in code
    assert "Parameters\n    ----------" in code
    assert "class FlatRed(" in (out / "shader" / "flat_red.py").read_text()
    assert "ScaleUp" in (out / "geometry" / "__init__.py").read_text()
    assert not (out / "materials").exists()


def test_api_only_dump_without_docstrings(library_blend, tmp_path):
    out = tmp_path / "pkg"
    main(["dump", "--api-only", "--no-docstrings", str(library_blend), str(out)])
    code = (out / "geometry" / "scale_up.py").read_text(encoding="utf-8")
    assert "Parameters" not in code


def test_api_only_dump_can_be_filtered_by_name(library_blend, tmp_path):
    out = tmp_path / "pkg"
    main(["dump", "--api-only", str(library_blend), str(out), "--names", "Scale Up"])
    assert (out / "geometry" / "scale_up.py").is_file()
    assert not (out / "shader").exists()


def test_lookup_search_show_and_socket(capsys):
    main(["lookup", "search", "named attribute", "--tree", "geometry"])
    out = capsys.readouterr().out
    assert "g.StoreNamedAttribute" in out and "GeometryNodeStoreNamedAttribute" in out

    main(["lookup", "show", "StoreNamedAttribute"])
    out = capsys.readouterr().out
    assert "constructor:" in out
    assert "geometry: " in out  # constructor parameters are listed with their types
    assert "StoreNamedAttribute.{" in out  # the domain/data-type factory variants
    assert "outputs: o.geometry" in out

    main(["lookup", "show", "Math"])
    assert "Math.add(" in capsys.readouterr().out
    main(["lookup", "show", "Bake"])  # a variadic constructor
    assert "**kwargs" in capsys.readouterr().out

    main(["lookup", "socket", "Vector"])
    out = capsys.readouterr().out
    assert out.startswith("VectorSocket") and ".normalize()" in out
    main(["lookup", "socket"])
    assert "socket types:" in capsys.readouterr().out


def test_lookup_misses_say_so(capsys):
    main(["lookup", "search", "zzzz-no-such-node"])
    assert "no node class matches" in capsys.readouterr().out
    main(["lookup", "show", "NoSuchNode"])
    assert "no class 'NoSuchNode'" in capsys.readouterr().out
    main(["lookup", "socket", "Nope"])
    assert "no socket type 'Nope'" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        main(["lookup", "show"])
