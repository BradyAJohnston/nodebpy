# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for the ``nodebpy`` command's ``generate`` subcommand and the
deprecated ``python -m nodebpy.assets`` entry point forwarding to it."""

import sys

import pytest

from nodebpy.__main__ import main

from .test_asset_library import _write_library


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


def test_generate_single_module(library_blend, tmp_path):
    """A .py output gets one module, its PackageLibrary path relative to it."""
    out = tmp_path / "pkg" / "assets.py"
    main(["generate", "-b", str(library_blend), "-o", str(out)])
    code = out.read_text(encoding="utf-8")
    assert "class ScaleUp(" in code
    assert '"../library.blend"' in code


def test_generate_tree_modules(library_blend, tmp_path):
    """A directory output gets one module per tree type."""
    out = tmp_path / "pkg"
    main(["generate", "-b", str(library_blend), "-o", str(out)])
    assert "class ScaleUp(" in (out / "geometry.py").read_text(encoding="utf-8")
    assert "class FlatRed(" in (out / "shader.py").read_text(encoding="utf-8")


def test_legacy_entry_forwards_subcommands(monkeypatch, library_blend, tmp_path):
    """``python -m nodebpy.assets dump …`` warns and runs ``nodebpy dump …``."""
    from nodebpy.assets.__main__ import main as legacy_main

    src = tmp_path / "src"
    monkeypatch.setattr(sys, "argv", ["prog", "dump", str(library_blend), str(src)])
    with pytest.warns(FutureWarning, match=r"removed in nodebpy 530.*'nodebpy dump'"):
        legacy_main()
    assert (src / "geometry" / "scale_up.py").is_file()


def test_legacy_entry_forwards_codegen_flags(monkeypatch, library_blend, tmp_path):
    """The flag-based ``python -m nodebpy.assets -b …`` warns and runs
    ``nodebpy generate -b …`` — also under Blender, after its ``--``."""
    from nodebpy.assets.__main__ import main as legacy_main

    out = tmp_path / "pkg"
    argv = [
        "blender",
        "-b",
        "-P",
        "x.py",
        "--",
        "-b",
        str(library_blend),
        "-o",
        str(out),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.warns(FutureWarning, match="'nodebpy generate'"):
        legacy_main()
    assert (out / "geometry.py").is_file()
