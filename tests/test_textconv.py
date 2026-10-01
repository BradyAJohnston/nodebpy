# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for ``nodebpy textconv``: printing a ``.blend`` library as Python
source, including through Git LFS as a git diff driver."""

import os
import shutil
import subprocess
import sys

import pytest

from nodebpy.assets import dump_library
from nodebpy.assets._textconv import FILE_HEADER, is_lfs_pointer

from .test_asset_library import _write_library

TEXTCONV = [sys.executable, "-m", "nodebpy", "textconv"]

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
        check=True,
        env=ENV,
    )
    assert result.stdout.startswith("### ")
    assert "### geometry/scale_up.py\n" in result.stdout
    assert result.stdout == _expected(library_blend, tmp_path)


def test_is_lfs_pointer(library_blend, tmp_path):
    pointer = tmp_path / "pointer"
    pointer.write_text(
        "version https://git-lfs.github.com/spec/v1\noid sha256:00\nsize 1\n"
    )
    assert is_lfs_pointer(pointer)
    assert not is_lfs_pointer(library_blend)


@pytest.mark.skipif(
    shutil.which("git") is None
    or subprocess.run(
        ["git", "lfs", "version"], capture_output=True, check=False
    ).returncode,
    reason="needs git with git-lfs",
)
def test_textconv_git_lfs_diff_driver(library_blend, tmp_path):
    """Configured as a diff driver on an LFS-tracked .blend, git shows the
    library as Python source: textconv receives the LFS pointer and smudges
    it itself."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
            env=ENV,
        ).stdout

    git("init", "-q")
    git("lfs", "install", "--local")
    (repo / ".gitattributes").write_text(
        "*.blend filter=lfs diff=blend merge=lfs -text\n"
    )
    git("config", "diff.blend.textconv", " ".join(TEXTCONV))
    shutil.copy(library_blend, repo / "library.blend")
    git("add", ".")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "add")

    assert git("cat-file", "blob", "HEAD:library.blend").startswith("version ")
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
