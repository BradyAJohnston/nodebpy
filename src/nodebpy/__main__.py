"""The ``nodebpy`` command line.

``nodebpy <subcommand>`` (or ``python -m nodebpy <subcommand>``) round-trips
``.blend`` asset libraries through Python source — ``dump``, ``build``,
``ensure``, ``check``, ``plot`` — and renders them as text for ``git diff``
with ``textconv``; see :mod:`nodebpy.assets._library` and
:mod:`nodebpy.assets._textconv`.

Under a full Blender (no ``bpy`` module) run this file as a script, with the
arguments after Blender's ``--`` separator::

    blender -b --factory-startup -P <.../nodebpy/__main__.py> -- textconv <blend>
"""

from __future__ import annotations

import sys
from pathlib import Path

# ``blender ... -P .../nodebpy/__main__.py`` runs this file as a plain script
# (no package context): put the package root on sys.path so the absolute
# imports resolve — a no-op under ``python -m nodebpy``.
if not __package__:  # pragma: no cover - only under blender -P
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main() -> None:  # pragma: no cover - CLI wrapper
    # Blender passes script arguments after a ``--`` separator: strip
    # everything up to and including it, so the same subcommands work there.
    argv = sys.argv[1:]
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]

    from nodebpy.assets._library import main as library_main

    library_main(argv)


if __name__ == "__main__":  # pragma: no cover
    main()
