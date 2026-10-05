"""The public entry: :func:`arrange`."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Literal

from bpy.types import NodeTree

from .apply import apply
from .config import SIMPLE_OPTIONS, SugiyamaOptions
from .extract import extract, optimize_sizes
from .pipeline import Observer, Pipeline
from .sugiyama import sugiyama_layout

type ArrangeMethod = Literal["sugiyama", "simple"] | SugiyamaOptions | None

# What "sugiyama" stands for; see `default_sugiyama_options`.
_DEFAULT_SUGIYAMA: ContextVar[SugiyamaOptions | None] = ContextVar(
    "nodebpy_default_sugiyama", default=None
)


@contextmanager
def default_sugiyama_options(options: SugiyamaOptions) -> Iterator[None]:
    """Scope in which ``arrange(tree, "sugiyama")``, and so every
    ``TreeBuilder`` left at its default arrangement, uses *options*.

    Explicit options and ``arrange=None`` are unaffected.
    """
    token = _DEFAULT_SUGIYAMA.set(options)
    try:
        yield
    finally:
        _DEFAULT_SUGIYAMA.reset(token)


def arrange(
    tree: NodeTree,
    method: ArrangeMethod = "sugiyama",
    *,
    selected_only: bool = False,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
    verify: bool = False,
) -> None:
    """Arrange the nodes of *tree*.

    *method* is a :class:`SugiyamaOptions`, ``"sugiyama"`` for the default
    options, ``"simple"`` for plain columns by dependency
    (:data:`~.config.SIMPLE_OPTIONS`), or None to leave the tree alone.

    With *selected_only* the selected nodes are arranged among themselves
    around where they were, and moved clear of the others, which stay put.
    Otherwise selection is ignored.

    *pipeline*, *observer* and *verify* are passed on to
    :func:`~.sugiyama.sugiyama_layout`.
    """
    if method is None:
        return
    if method == "simple":
        options = SIMPLE_OPTIONS
    elif isinstance(method, SugiyamaOptions):
        options = method
    else:
        options = _DEFAULT_SUGIYAMA.get() or SugiyamaOptions()

    if options.optimize_sizes:
        optimize_sizes(tree.nodes)

    data, binding = extract(tree)
    result = sugiyama_layout(
        data,
        options,
        pipeline=pipeline,
        observer=observer,
        verify=verify,
        selected_only=selected_only,
    )
    apply(tree, binding, result)

    # Positions are dumped to two decimals; keep to that so an arranged tree
    # survives a round trip unchanged.
    for node in tree.nodes:
        location = node.location
        node.location = (round(location.x, 2), round(location.y, 2))
