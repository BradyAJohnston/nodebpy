"""Regression tests for building node trees when networkx is unavailable.

When nodebpy is vendored into a Blender extension, the optional ``networkx``
dependency is frequently absent. The Sugiyama layout should then fall back to
the simple arrangement instead of crashing.

The subtle failure mode this guards against is order-dependent: the *first*
arrange attempt raises a clean ``ImportError`` (which is caught and falls back),
but a *second* attempt used to surface a raw ``KeyError`` from the namespace
package machinery, escaping the ``except ImportError`` guard. So we must build
more than one tree in the same process to exercise the real bug.
"""

import sys
import warnings

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g


@pytest.fixture
def no_networkx():
    """Simulate a vendored install where networkx cannot be imported.

    Setting ``sys.modules['networkx'] = None`` makes ``import networkx`` raise
    ``ImportError``. We also evict the cached ``nodebpy.lib.nodearrange``
    modules so the import is genuinely re-attempted (rebuilding the namespace
    package path), matching the user's fresh-process scenario.
    """
    blocked = "networkx"
    saved = {
        k: v
        for k, v in sys.modules.items()
        if k == blocked
        or k.startswith(blocked + ".")
        or k.startswith("nodebpy.lib.nodearrange")
    }
    for key in saved:
        del sys.modules[key]
    sys.modules[blocked] = None  # force ImportError on `import networkx`
    try:
        yield
    finally:
        del sys.modules[blocked]
        sys.modules.update(saved)


def _build(name: str) -> TreeBuilder:
    with TreeBuilder.geometry(name) as tree:  # default arrange="sugiyama"
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out
    return tree


def test_fallback_without_networkx(no_networkx):
    """Two sequential sugiyama builds must degrade gracefully without networkx."""
    # First tree: clean ImportError -> warns + falls back. This works today.
    with pytest.warns(UserWarning, match="networkx"):
        _build("FirstNoNX")

    # Second tree: this is where the stale namespace path used to raise
    # KeyError: 'nodebpy.lib.nodearrange', escaping `except ImportError`.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        second = _build("SecondNoNX")

    # The tree should still have been built and arranged (simple fallback).
    assert len(second.tree.nodes) > 0
