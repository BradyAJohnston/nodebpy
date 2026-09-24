# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for the asset pipeline CLI additions: ``[tool.nodebpy.assets]``
pyproject configuration, fingerprint stamping with ``ensure``, and the
``check`` roundtrip fixed-point verification."""

import shutil
from pathlib import Path

import pytest

from nodebpy.assets import dump_library
from nodebpy.assets._library import _parse_args
from nodebpy.assets._library import main as library_main
from nodebpy.assets._pipeline import (
    _INIT_CONTENT,
    compare_sources,
    fingerprint,
    is_stale,
    load_config,
    stamp_path,
)

from .test_asset_library import _clear_node_groups, _write_library


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


def _write_pyproject(directory: Path, body: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "pyproject.toml").write_text(body, encoding="utf-8")


CONFIG = """
[tool.nodebpy.assets]
source = "pkg/nodes"
blend = "pkg/assets/nodes.blend"
resources = "pkg/assets/resources.blend"
typed-api = true
add-reroutes = true
iterations = 100
"""


# ---------------------------------------------------------------------------
# [tool.nodebpy.assets] pyproject configuration
# ---------------------------------------------------------------------------


def test_load_config_walks_up(tmp_path):
    """The nearest pyproject above the start directory supplies the table,
    and the directory it was found in anchors the relative paths."""
    _write_pyproject(tmp_path, CONFIG)
    nested = tmp_path / "deeply" / "nested"
    nested.mkdir(parents=True)
    table, root = load_config(nested)
    assert root == tmp_path
    assert table["source"] == "pkg/nodes"
    assert table["typed-api"] is True

    # A nearer pyproject without the table still wins the walk — the nearest
    # project owns the configuration.
    _write_pyproject(nested, '[project]\nname = "inner"\nversion = "0"\n')
    table, root = load_config(nested)
    assert (table, root) == ({}, nested)


def test_config_fills_cli_args(tmp_path, monkeypatch):
    """Config supplies positionals and flags; paths resolve against the
    pyproject's directory; dests the subcommand's parser doesn't define
    resolve too (the stamp fingerprint hashes them)."""
    _write_pyproject(tmp_path, CONFIG)
    monkeypatch.chdir(tmp_path)

    args = _parse_args(["build"])
    assert args.source == tmp_path / "pkg/nodes"
    assert args.blend == tmp_path / "pkg/assets/nodes.blend"
    assert args.resources == tmp_path / "pkg/assets/resources.blend"
    assert args.add_reroutes is True
    assert args.iterations == 100
    assert args.typed_api is True  # a dump flag, resolved for build's stamp

    # dump maps the config's `source` onto its <output> positional.
    args = _parse_args(["dump"])
    assert args.blend == tmp_path / "pkg/assets/nodes.blend"
    assert args.output == tmp_path / "pkg/nodes"


def test_cli_overrides_config(tmp_path, monkeypatch):
    _write_pyproject(tmp_path, CONFIG)
    monkeypatch.chdir(tmp_path)
    args = _parse_args(["build", "elsewhere", "other.blend", "--iterations", "5"])
    assert args.source == Path("elsewhere")
    assert args.blend == Path("other.blend")
    assert args.iterations == 5
    # Flags the command line left alone still come from the config.
    assert args.add_reroutes is True


def test_missing_positional_names_argument_and_config_key(tmp_path, monkeypatch):
    _write_pyproject(tmp_path, '[project]\nname = "x"\nversion = "0"\n')
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as excinfo:
        _parse_args(["build"])
    message = str(excinfo.value)
    assert "<source>" in message and "'source'" in message
    assert "[tool.nodebpy.assets]" in message


def test_unknown_config_key_errors(tmp_path, monkeypatch):
    _write_pyproject(tmp_path, '[tool.nodebpy.assets]\nsourc = "typo"\n')
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit, match="sourc"):
        _parse_args(["build", "a", "b"])


# ---------------------------------------------------------------------------
# Fingerprint stamping and ensure
# ---------------------------------------------------------------------------


def test_fingerprint_stability_and_sensitivity(tmp_path):
    """A no-op keeps the fingerprint stable; a changed source file, changed
    resources bytes, or a changed option each change it."""
    src = tmp_path / "nodes"
    (src / "geometry").mkdir(parents=True)
    module = src / "geometry" / "thing.py"
    module.write_text("A = 1\n", encoding="utf-8")
    resources = tmp_path / "resources.blend"
    resources.write_bytes(b"stuff")
    options: dict[str, object] = {"add_reroutes": True, "iterations": 100}

    base = fingerprint(src, resources, options)
    assert fingerprint(src, resources, options) == base

    module.write_text("A = 2\n", encoding="utf-8")
    edited = fingerprint(src, resources, options)
    assert edited != base

    resources.write_bytes(b"other stuff")
    reresourced = fingerprint(src, resources, options)
    assert reresourced != edited

    assert fingerprint(src, resources, {**options, "iterations": 50}) != reresourced
    assert fingerprint(src, None, options) != reresourced

    # is_stale is a pure hash comparison against the stamp sidecar.
    blend = tmp_path / "nodes.blend"
    assert is_stale(blend, src, None, options)  # no .blend at all
    blend.write_bytes(b"blend")
    assert is_stale(blend, src, None, options)  # no stamp yet
    stamp_path(blend).write_text(fingerprint(src, None, options) + "\n")
    assert not is_stale(blend, src, None, options)
    module.write_text("A = 3\n", encoding="utf-8")
    assert is_stale(blend, src, None, options)


def test_ensure_builds_then_noops_then_rebuilds(library_blend, tmp_path, capsys):
    src = tmp_path / "src"
    dump_library(library_blend, src)
    blend = tmp_path / "out" / "nodes.blend"

    library_main(["ensure", str(src), str(blend)])
    assert "Built" in capsys.readouterr().out
    assert blend.is_file() and stamp_path(blend).is_file()

    library_main(["ensure", str(src), str(blend)])
    assert "up to date" in capsys.readouterr().out

    # Touching a source module invalidates the stamp; ensure rebuilds.
    module = src / "geometry" / "scale_up.py"
    module.write_text(
        module.read_text(encoding="utf-8") + "\n# touched\n", encoding="utf-8"
    )
    _clear_node_groups()  # ensure's rebuild needs the fresh-session guarantee
    library_main(["ensure", str(src), str(blend)])
    assert "Built" in capsys.readouterr().out


def test_cli_dump_refreshes_stamp(library_blend, tmp_path, capsys):
    """After a full CLI dump the .blend and sources match by construction, so
    the refreshed stamp makes a follow-up ensure a no-op — dump and ensure
    resolve the same option set for the fingerprint."""
    src = tmp_path / "src"
    library_main(["dump", str(library_blend), str(src)])
    assert stamp_path(library_blend).is_file()

    library_main(["ensure", str(src), str(library_blend)])
    assert "up to date" in capsys.readouterr().out


def test_cli_build_from_config(library_blend, tmp_path, monkeypatch, capsys):
    """`build` with no positionals takes everything from the pyproject table
    and stamps the built .blend."""
    src = tmp_path / "pkg" / "nodes"
    dump_library(library_blend, src)
    _write_pyproject(
        tmp_path,
        '[tool.nodebpy.assets]\nsource = "pkg/nodes"\nblend = "pkg/nodes.blend"\n',
    )
    monkeypatch.chdir(tmp_path)

    library_main(["build"])
    assert "Built" in capsys.readouterr().out
    assert (tmp_path / "pkg" / "nodes.blend").is_file()
    assert stamp_path(tmp_path / "pkg" / "nodes.blend").is_file()


# ---------------------------------------------------------------------------
# check: roundtrip fixed-point verification
# ---------------------------------------------------------------------------


def test_compare_sources_rules(tmp_path):
    """_-prefixed files at the source root and a hand-written top-level
    __init__.py are exempt; set differences and content differences are both
    failures."""
    src = tmp_path / "src"
    new = tmp_path / "new"
    (src / "geometry").mkdir(parents=True)
    (new / "geometry").mkdir(parents=True)
    (src / "geometry" / "a.py").write_text("same\n", encoding="utf-8")
    (new / "geometry" / "a.py").write_text("same\n", encoding="utf-8")
    (src / "_handlers.py").write_text("runtime module\n", encoding="utf-8")
    (src / "__init__.py").write_text("from . import geometry\n", encoding="utf-8")
    (new / "__init__.py").write_text(_INIT_CONTENT, encoding="utf-8")

    problems, modules = compare_sources(src, new)
    assert problems == [] and modules == 1

    # A generated top-level __init__.py is compared (and matches itself).
    (src / "__init__.py").write_text(_INIT_CONTENT, encoding="utf-8")
    problems, modules = compare_sources(src, new)
    assert problems == [] and modules == 2

    (new / "geometry" / "a.py").write_text("different\n", encoding="utf-8")
    (src / "geometry" / "b.py").write_text("only in sources\n", encoding="utf-8")
    (new / "geometry" / "_shared" / "c.py").parent.mkdir()
    (new / "geometry" / "_shared" / "c.py").write_text(
        "only in redump\n", encoding="utf-8"
    )
    problems, _ = compare_sources(src, new)
    assert problems == ["geometry/_shared/c.py", "geometry/b.py", "geometry/a.py"]


def test_check_passes_on_pristine_roundtrip(library_blend, tmp_path, capsys):
    """A freshly dumped source tree survives build->dump byte-for-byte: the
    check-dump into a temporary directory is anchored at the real source
    directory and .blend, so the typed-API PackageLibrary paths match too."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    blend = pkg / "nodes.blend"
    shutil.copyfile(library_blend, blend)
    src = pkg / "nodes"
    dump_library(blend, src, typed_api=True)

    library_main(["check", str(src), str(blend), "--typed-api"])
    assert "Roundtrip OK" in capsys.readouterr().out


def test_check_fails_and_names_the_edited_module(library_blend, tmp_path, capsys):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    blend = pkg / "nodes.blend"
    shutil.copyfile(library_blend, blend)
    src = pkg / "nodes"
    dump_library(blend, src, typed_api=True)

    module = src / "geometry" / "scale_up.py"
    module.write_text(
        module.read_text(encoding="utf-8") + "\nX = 1  # hand edit\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit):
        library_main(["check", str(src), str(blend), "--typed-api"])
    out = capsys.readouterr().out
    assert "do not survive" in out
    assert "geometry/scale_up.py" in out
    assert "build && python -m nodebpy.assets dump" in out


# ---------------------------------------------------------------------------
# Blender-style invocation of the CLI entry
# ---------------------------------------------------------------------------


def test_blender_style_argv_separator(monkeypatch, library_blend, tmp_path, capsys):
    """Under a full Blender the CLI runs as ``blender -b --factory-startup
    -P .../__main__.py -- <args>``: everything up to the ``--`` separator is
    Blender's own argv and is stripped."""
    import sys as _sys

    from nodebpy.assets.__main__ import main

    src = tmp_path / "src"
    monkeypatch.setattr(
        _sys,
        "argv",
        ["blender", "-b", "-P", "x.py", "--", "dump", str(library_blend), str(src)],
    )
    main()
    assert "Dumped 2 assets" in capsys.readouterr().out
