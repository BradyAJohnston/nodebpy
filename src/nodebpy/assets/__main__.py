"""Deprecated ``python -m nodebpy.assets`` entry point — use ``nodebpy``.

Forwards to the ``nodebpy`` command (:mod:`nodebpy.__main__`) with a
``FutureWarning``, and will be removed in nodebpy 530: subcommands pass
through unchanged (``python -m nodebpy.assets dump …`` → ``nodebpy dump …``)
and the flag-based codegen interface becomes ``nodebpy generate``
(``python -m nodebpy.assets -b lib.blend`` → ``nodebpy generate -b
lib.blend``). The :mod:`nodebpy.assets` module itself stays.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

# ``blender ... -P .../nodebpy/assets/__main__.py`` runs this file as a plain
# script (no package context): put the package root on sys.path so the
# absolute imports resolve — a no-op under ``python -m nodebpy.assets``.
if not __package__:  # pragma: no cover - only under blender -P
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def main() -> None:
    # Blender passes script arguments after a ``--`` separator: strip
    # everything up to and including it.
    argv = sys.argv[1:]
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]

    # The flag-based codegen interface took no positionals, so a leading
    # positional is always a subcommand.
    if not argv or argv[0].startswith("-"):
        argv = ["generate", *argv]
    warnings.warn(
        "'python -m nodebpy.assets' is deprecated and will be removed in "
        f"nodebpy 530; use 'nodebpy {argv[0]}' instead.",
        FutureWarning,
        stacklevel=2,
    )

    from nodebpy.__main__ import main as nodebpy_main

    nodebpy_main(argv)


if __name__ == "__main__":  # pragma: no cover
    main()
