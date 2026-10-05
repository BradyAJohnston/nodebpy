"""The public entry: :func:`arrange` and its options."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, fields
from typing import Literal

import bpy
from bpy.types import NodeTree

from .apply import apply
from .config import Settings
from .extract import extract, optimize_sizes
from .pipeline import Observer, Pipeline
from .simple import arrange_tree
from .sugiyama import sugiyama_layout


@dataclass(frozen=True)
class SimpleOptions:
    """Options for the simple column-based arrangement.

    Parameters
    ----------
    spacing : tuple[float, float]
        Horizontal gap between columns and vertical gap between nodes.
    """

    spacing: tuple[float, float] = (50, 25)


@dataclass(frozen=True)
class SugiyamaOptions:
    """Options for the Sugiyama (layered) arrangement.

    Parameters
    ----------
    margin : tuple[float, float]
        Horizontal and vertical space between nodes.
    direction : str
        Which way nodes lean where they could sit in several places along
        a column: ``"LEFT_UP"``, ``"LEFT_DOWN"``, ``"RIGHT_UP"``,
        ``"RIGHT_DOWN"``, or ``"BALANCED"`` for the middle of the four.
    socket_alignment : str
        Whether aligned nodes line up by their tops (``"NONE"``), by the
        sockets of the link between them so the link is straight
        (``"FULL"``), or by sockets only where the nodes differ much in
        height (``"MODERATE"``).
    reroutes : str
        Which links get reroute nodes. ``"none"``: the layout only moves
        nodes (the default: reroutes are real nodes, which would change
        the authored structure of generated trees). ``"blocked"``: links
        that would otherwise be drawn across a node, and the reroutes
        already in the tree are kept. ``"all"``: every link that passes
        over a column, and the tree's own reroutes are replaced.
    stack_collapsed : bool
        Stack chains of collapsed Math nodes vertically.
    optimize_sizes : bool
        Fit the widths of collapsed nodes to their display name.
    straighten_trunk : bool
        Keep the trunk straight. The trunk is the line the tree's main
        data runs along: the links between flow sockets (geometry, shader,
        bundle, closure). They are aligned before any other, so a chain of
        geometry nodes is one flat row with the side chains feeding it
        hung below, a fork that merges again is symmetric around its
        middle branch, and each zone (simulation, repeat, for-each,
        closure) is a row with its node tops level. Off, every link is
        treated alike and a node aligns with its median neighbour.
    pin_group_output : bool
        Put Group Output nodes (outside frames) in the last column.
    pin_group_input : bool
        Put Group Input nodes (outside frames) in the first column, rather
        than next to the nodes they feed.
    sequential_frames : bool
        Rank frames as stages: every node of a frame comes after every
        node of the frame (or intermediate node) feeding it, so frames
        line up left to right instead of stacking.
    balance_heights : bool
        Shorten the tallest columns by moving the chains that feed them one
        column left, while that brings the drawing closer to a screen's
        shape.
    pack_components : bool
        Lay out the parts of the tree that are not linked to each other
        apart: the largest first, the others (a second group of nodes, a
        frame holding a note) in rows beneath it. Off, the whole tree is
        laid out as one graph and unrelated parts share its columns.
    """

    # (The fields below `margin` are those of `config.Settings`, with the
    # same defaults.)
    margin: tuple[float, float] = (30.0, 30.0)
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "BALANCED"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "NONE"
    reroutes: Literal["none", "blocked", "all"] = "none"
    stack_collapsed: bool = True
    optimize_sizes: bool = False
    straighten_trunk: bool = True
    pin_group_output: bool = True
    pin_group_input: bool = False
    sequential_frames: bool = True
    balance_heights: bool = True
    pack_components: bool = True


type ArrangeMethod = (
    Literal["sugiyama", "simple"] | SugiyamaOptions | SimpleOptions | None
)

# What the plain "sugiyama" method resolves to (None = SugiyamaOptions()).
# Overridable per scope so a batch build can tune the arrangement of trees
# whose recipes leave TreeBuilder at its default — see
# :func:`default_sugiyama_options`.
_DEFAULT_SUGIYAMA: ContextVar[SugiyamaOptions | None] = ContextVar(
    "nodebpy_default_sugiyama", default=None
)


@contextmanager
def default_sugiyama_options(options: SugiyamaOptions) -> Iterator[None]:
    """Scope in which ``arrange(tree, "sugiyama")`` — and therefore every
    ``TreeBuilder`` left at its default arrangement — uses ``options``
    instead of ``SugiyamaOptions()``.

    Explicit ``SugiyamaOptions`` / ``SimpleOptions`` arguments and
    ``arrange=None`` (as emitted by ``snapshot_positions`` dumps) are
    unaffected.
    """
    token = _DEFAULT_SUGIYAMA.set(options)
    try:
        yield
    finally:
        _DEFAULT_SUGIYAMA.reset(token)


# What TreeBuilder's split_inputs=None resolves to. Overridable per scope so
# a batch build can split the Group Input of trees whose recipes leave
# TreeBuilder at its default — see :func:`default_split_inputs`.
_DEFAULT_SPLIT_INPUTS: ContextVar[bool] = ContextVar(
    "nodebpy_default_split_inputs", default=False
)


@contextmanager
def default_split_inputs(split: bool = True) -> Iterator[None]:
    """Scope in which every ``TreeBuilder`` left at its default
    ``split_inputs`` splits the Group Input node into one instance per
    consumer node (with unused sockets hidden) on context exit.

    An explicit ``split_inputs=True/False`` is unaffected, and so are trees
    that disable auto-arrangement (as ``snapshot_positions`` dumps do) —
    their authored layout, including any authored Group Input splits, must
    survive untouched.
    """
    token = _DEFAULT_SPLIT_INPUTS.set(split)
    try:
        yield
    finally:
        _DEFAULT_SPLIT_INPUTS.reset(token)


def _sugiyama_settings(options: SugiyamaOptions) -> Settings:
    """The layout's settings for *options*: every field but the margin."""
    return Settings(**{f.name: getattr(options, f.name) for f in fields(Settings)})


def arrange_node_tree(
    ntree: NodeTree,
    settings: Settings | None = None,
    margin: tuple[float, float] | None = None,
    *,
    pipeline: Pipeline | None = None,
    observer: Observer | None = None,
    verify: bool = False,
    selected_only: bool = False,
) -> None:
    """Arrange the nodes of *ntree*.

    The whole tree is laid out unless *selected_only* is set: a tree built
    from Python has no selection. With *selected_only* the selected nodes
    are arranged among themselves around where they were; other nodes do
    not move, and links to them are left out of account.

    *pipeline*, *observer* and *verify* are passed on to the layout (see
    :func:`.sugiyama.sugiyama_layout`).
    """
    settings = settings or Settings()
    if settings.optimize_sizes:
        optimize_sizes(ntree.nodes)

    tree, binding = extract(ntree)
    result = sugiyama_layout(
        tree,
        settings,
        margin,
        pipeline=pipeline,
        observer=observer,
        verify=verify,
        selected_only=selected_only,
    )
    apply(ntree, binding, result)


def _arrange_sugiyama(
    tree: bpy.types.NodeTree, options: SugiyamaOptions, selected_only: bool = False
) -> None:
    arrange_node_tree(
        tree,
        _sugiyama_settings(options),
        margin=tuple(options.margin),
        selected_only=selected_only,
    )


def arrange(
    tree: bpy.types.NodeTree,
    method: ArrangeMethod = "sugiyama",
    *,
    selected_only: bool = False,
) -> None:
    """Arrange the nodes of a tree.

    ``method`` selects the algorithm: ``"sugiyama"`` (or a
    :class:`SugiyamaOptions` instance for tuned settings), ``"simple"`` (or a
    :class:`SimpleOptions` instance), or None to leave the tree untouched.

    With ``selected_only`` (Sugiyama only) just the selected nodes are
    arranged, among themselves and around where they were, and moved clear
    of the others, which stay put. By default the whole tree is arranged
    whatever is selected: a tree built from Python has no selection.
    """
    if method is None:
        return

    if isinstance(method, SimpleOptions):
        arrange_tree(tree, method.spacing)
    elif method == "simple":
        arrange_tree(tree)
    else:
        options = (
            method
            if isinstance(method, SugiyamaOptions)
            else _DEFAULT_SUGIYAMA.get() or SugiyamaOptions()
        )
        _arrange_sugiyama(tree, options, selected_only)

    # Quantize to the precision node positions are dumped with, so arranged
    # trees round-trip losslessly (and sub-0.01 UI units carry no meaning).
    for node in tree.nodes:
        location = node.location
        node.location = (round(location.x, 2), round(location.y, 2))
