"""The Sugiyama layout must not need ``networkx``.

nodebpy is often vendored into a Blender extension, where ``networkx`` is
not available. The layout used to depend on it (falling back to the simple
arrangement with a warning when it was missing); it now runs on its own
graph structs, so blocking the import must change nothing.
"""

import sys
import warnings
from contextlib import contextmanager

from nodebpy import TreeBuilder
from nodebpy import geometry as g

_ARRANGE = "nodebpy.lib.nodearrange"


@contextmanager
def _networkx_blocked():
    """Make ``import networkx`` raise ``ImportError``, and evict the cached
    arrange modules so they are imported afresh while it is blocked."""
    blocked = "networkx"
    saved = {
        k: v
        for k, v in sys.modules.items()
        if k == blocked or k.startswith((blocked + ".", _ARRANGE))
    }
    for key in saved:
        del sys.modules[key]
    sys.modules[blocked] = None  # ty: ignore[invalid-assignment]
    try:
        yield
    finally:
        del sys.modules[blocked]
        for key in [k for k in sys.modules if k.startswith(_ARRANGE)]:
            del sys.modules[key]
        sys.modules.update(saved)


def _build(name: str) -> dict[str, tuple[float, float]]:
    with TreeBuilder.geometry(name) as tree:  # default arrange="sugiyama"
        geo = tree.inputs.geometry()
        out = tree.outputs.geometry()
        _ = geo >> g.SetPosition() >> g.RealizeInstances() >> out
    return {n.bl_idname: tuple(n.location) for n in tree.tree.nodes}


def test_sugiyama_does_not_need_networkx():
    """With networkx blocked the layout is the same Sugiyama layout, with no
    fallback warning — for a second tree in the same process too (the old
    fallback raised a stale-namespace ``KeyError`` there)."""
    reference = _build("Reference")
    # A chain of four nodes: four distinct columns.
    assert len({x for x, _ in reference.values()}) == 4

    with _networkx_blocked(), warnings.catch_warnings():
        warnings.simplefilter("error")
        first = _build("FirstNoNX")
        second = _build("SecondNoNX")

    assert first == reference
    assert second == reference
