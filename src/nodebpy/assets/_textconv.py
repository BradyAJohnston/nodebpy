"""Render a ``.blend`` asset library as text, for ``git diff``.

``nodebpy textconv <file>`` dumps a library (see
:func:`~nodebpy.assets.dump_library`) and prints every module to stdout, each
headed by its path, so git can line-diff binary ``.blend`` files as Python
source. Wire it up as a git ``textconv`` diff driver::

    # .gitattributes
    *.blend diff=blend

    git config diff.blend.textconv "nodebpy textconv"
    git config diff.blend.cachetextconv true

Git hands a textconv driver the blob as stored in the repository; for files
tracked with Git LFS that is the pointer, which is smudged through
``git lfs smudge`` to the real ``.blend`` first.
"""

from __future__ import annotations

import contextlib
import ctypes
import os
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import TextIO

LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/"
FILE_HEADER = "### {}\n"


def is_lfs_pointer(path: str | Path) -> bool:
    """Whether ``path`` holds a Git LFS pointer rather than file content."""
    with open(path, "rb") as f:
        return f.read(len(LFS_POINTER_PREFIX)) == LFS_POINTER_PREFIX


@contextlib.contextmanager
def _stdout_to_stderr() -> Iterator[None]:
    """Send everything written to file descriptor 1 — Python's ``print`` and
    Blender's own C-level messages alike — to stderr, keeping stdout clean
    for the textconv output. C stdio buffers are flushed before fd 1 is
    restored, so Blender's buffered messages land on stderr too."""
    libc = ctypes.CDLL(None)
    sys.stdout.flush()
    saved = os.dup(1)
    os.dup2(2, 1)
    try:
        yield
    finally:
        sys.stdout.flush()
        libc.fflush(None)
        os.dup2(saved, 1)
        os.close(saved)


def textconv(path: str | Path, out: TextIO | None = None) -> None:
    """Dump the asset library at ``path`` and write its modules to ``out``
    (default stdout) in sorted path order, each preceded by a ``### <path>``
    header (``__init__.py`` package markers are left out). A Git LFS pointer is smudged to the real ``.blend`` first."""
    from nodebpy.assets._library import dump_library

    out = out or sys.stdout
    with tempfile.TemporaryDirectory(prefix="nodebpy-textconv-") as tmp:
        blend = Path(path)
        if is_lfs_pointer(blend):
            blend = Path(tmp) / "smudged.blend"
            with open(path, "rb") as src, open(blend, "wb") as dst:
                subprocess.run(
                    ["git", "lfs", "smudge", str(path)],
                    stdin=src,
                    stdout=dst,
                    check=True,
                )
        output = Path(tmp) / "dump"
        with _stdout_to_stderr():
            dump_library(blend, output)
        # Skip the ``__init__.py`` package markers: boilerplate in a diff.
        for file in sorted(output.rglob("*.py")):
            if file.name == "__init__.py":
                continue
            out.write(FILE_HEADER.format(file.relative_to(output).as_posix()))
            out.write(file.read_text(encoding="utf-8"))
