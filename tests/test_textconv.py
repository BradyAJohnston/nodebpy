# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for ``nodebpy textconv``: printing a ``.blend`` library as Python
source, including through Git LFS as a git diff driver."""

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from nodebpy.assets import dump_library
from nodebpy.assets._library import _parse_args
from nodebpy.assets._textconv import FILE_HEADER, is_lfs_pointer, textconv

from .test_asset_library import _write_library

TEXTCONV = [sys.executable, "-m", "nodebpy", "textconv"]
# The same as a git config value: git runs it through sh, so quote the
# interpreter path and use forward slashes (Windows backslashes are escapes).
TEXTCONV_CONFIG = f'"{Path(sys.executable).as_posix()}" -m nodebpy textconv'

# Importing bpy setenv()s OCIO, which subprocesses inherit (directly, or via
# xdist workers' os.environ) — and a bpy that finds OCIO set logs "Using
# OCIO=..." to stdout on import, before textconv can redirect it. Run the
# children without it, as git would from a plain shell.
ENV = {k: v for k, v in os.environ.items() if k != "OCIO"}


@pytest.fixture
def library_blend(tmp_path):
    path = tmp_path / "library.blend"
    _write_library(path)
    return path


def _expected(library_blend, tmp_path) -> str:
    """The textconv output assembled by hand from a dump of the library."""
    output = tmp_path / "expected"
    dump_library(library_blend, output)
    return "".join(
        FILE_HEADER.format(f.relative_to(output).as_posix())
        + f.read_text(encoding="utf-8")
        for f in sorted(output.rglob("*.py"))
        if f.name != "__init__.py"
    )


def test_textconv_prints_dump(library_blend, tmp_path):
    """The CLI prints every dumped module under its path header, and nothing
    else — dump progress and Blender's own messages stay off stdout."""
    result = subprocess.run(
        [*TEXTCONV, str(library_blend)],
        capture_output=True,
        text=True,
        check=False,
        env=ENV,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("### ")
    assert "### geometry/scale_up.py\n" in result.stdout
    assert result.stdout == _expected(library_blend, tmp_path)


def test_textconv_in_process(library_blend, tmp_path):
    """``textconv()`` writes the same text to a given stream, and keeps the
    dump's own stdout output off it."""
    out = io.StringIO()
    textconv(library_blend, out)
    assert out.getvalue() == _expected(library_blend, tmp_path)


def test_parse_textconv_args(tmp_path, monkeypatch):
    """``textconv`` takes the .blend positional and ignores any
    [tool.nodebpy.assets] config."""
    (tmp_path / "pyproject.toml").write_text(
        '[tool.nodebpy.assets]\nsource = "src"\nblend = "lib.blend"\n'
    )
    monkeypatch.chdir(tmp_path)
    args = _parse_args(["textconv", "other.blend"])
    assert (args.command, args.blend) == ("textconv", Path("other.blend"))


def test_main_module_imports():
    """``python -m nodebpy`` resolves to an importable module with a
    ``main``."""
    import nodebpy.__main__

    assert callable(nodebpy.__main__.main)


def test_is_lfs_pointer(library_blend, tmp_path):
    pointer = tmp_path / "pointer"
    pointer.write_text(
        "version https://git-lfs.github.com/spec/v1\noid sha256:00\nsize 1\n"
    )
    assert is_lfs_pointer(pointer)
    assert not is_lfs_pointer(library_blend)


needs_git_lfs = pytest.mark.skipif(
    shutil.which("git") is None
    or subprocess.run(
        ["git", "lfs", "version"], capture_output=True, check=False
    ).returncode,
    reason="needs git with git-lfs",
)


@pytest.fixture
def lfs_repo(library_blend, tmp_path):
    """A git repo with ``library.blend`` committed to Git LFS and the textconv
    driver configured; yields the repo and a ``git`` runner."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
            env=ENV,
        )
        assert result.returncode == 0, result.stderr
        return result.stdout

    git("init", "-q")
    git("lfs", "install", "--local")
    (repo / ".gitattributes").write_text(
        "*.blend filter=lfs diff=blend merge=lfs -text\n"
    )
    git("config", "diff.blend.textconv", TEXTCONV_CONFIG)
    shutil.copy(library_blend, repo / "library.blend")
    git("add", ".")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "add")

    assert git("cat-file", "blob", "HEAD:library.blend").startswith("version ")
    return repo, git


@needs_git_lfs
def test_textconv_smudges_lfs_pointer(library_blend, lfs_repo, monkeypatch):
    """Handed an LFS pointer, ``textconv()`` smudges it to the real .blend
    through git-lfs before dumping."""
    repo, git = lfs_repo
    pointer = repo / "pointer"
    pointer.write_text(git("cat-file", "blob", "HEAD:library.blend"))
    monkeypatch.chdir(repo)
    from_pointer, from_blend = io.StringIO(), io.StringIO()
    textconv(pointer, from_pointer)
    textconv(library_blend, from_blend)
    assert from_pointer.getvalue().startswith("### geometry/scale_up.py\n")
    assert from_pointer.getvalue() == from_blend.getvalue()


@needs_git_lfs
def test_textconv_git_lfs_diff_driver(library_blend, lfs_repo):
    """Configured as a diff driver on an LFS-tracked .blend, git shows the
    library as Python source: textconv receives the LFS pointer and smudges
    it itself."""
    repo, git = lfs_repo
    shown = git("show", "--textconv", "HEAD:library.blend")
    # Compared against the CLI run from the same directory: the dump's ruff
    # pass picks up the nearest project's config, so output depends on cwd.
    direct = subprocess.run(
        [*TEXTCONV, str(library_blend)],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
        env=ENV,
    ).stdout
    assert shown.startswith("### geometry/scale_up.py\n")
    assert shown == direct
