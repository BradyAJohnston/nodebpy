# SPDX-License-Identifier: GPL-2.0-or-later
"""The layout as a list of named steps.

A layered layout is a sequence of passes over one graph. Four of them are
the *phases* that decide the layout:

``rank``
    Assign every node a column.
``order``
    Order the nodes within each column, to reduce link crossings.
``place``
    Assign positions along the columns.
``route``
    Give links bend points around the nodes in their way.

The rest are smaller *steps* that prepare the graph for a phase or clean up
after one: replacing reroutes, stacking collapsed nodes, splitting long
links with dummy nodes, bordering frames, and finally writing the result
out as edits. The split into phases and steps between them follows the
Eclipse Layout Kernel's layered algorithm.

:func:`~.sugiyama.default_pipeline` builds the standard list. To
experiment, take it and :meth:`~Pipeline.replace` a step (a phase, to try
another algorithm for it), or :meth:`~Pipeline.insert_after` one.

Steps depend on each other through the state of the graph. Each
:class:`Step` names the facts (:class:`Fact`) it ``requires`` to hold, those
it ``provides`` and those it ``removes``. A pipeline whose steps do not fit
together is refused before it runs (:meth:`Pipeline.check`). With
``verify=True`` every fact is checked against the graph after every step
(:data:`CHECKS`), and a broken one is reported with the step that broke it.
"""

from __future__ import annotations

import itertools
import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import TYPE_CHECKING, Literal

from .common import Vec2
from .config import LayoutState, SugiyamaOptions
from .digraph import DiGraph, LayoutGraph
from .model import Cluster, ClusterGraph, Kind, Node

if TYPE_CHECKING:
    from .stacking import NodeStack

type Phase = Literal["rank", "order", "place", "route"]

PHASES: tuple[Phase, ...] = ("rank", "order", "place", "route")


class Fact(StrEnum):
    """Something true of the layout graph between two steps."""

    RANKED = "ranked"
    """Every node has a ``rank``, the index of its column, and every link
    runs to a later column."""
    PROPER = "proper"
    """Every link runs to the next column: long links are chains of dummy
    nodes."""
    COLUMNS = "columns"
    """``G.columns`` lists the nodes of each column, and every node's
    ``col`` is its column. A step that reorders a column must do so in
    place."""
    ORDERED = "ordered"
    """The order within each column is decided, and the nodes of each frame
    are next to each other in every column."""
    BORDERS = "borders"
    """Each frame has a border node above and below its nodes in every
    column, which keep room for its outline. They are thin nodes without a
    rank. A placement must treat them like any other node of a column."""
    Y = "y"
    """Every node has a ``y``, and no two nodes of a column overlap."""
    X = "x"
    """Every node has an ``x``, and the columns do not overlap."""


@dataclass(slots=True)
class Layout:
    """The graph being laid out and everything the steps share."""

    CG: ClusterGraph
    old_center: Vec2
    """Centre of the nodes before the layout; the result is centred there."""
    node_stacks: list[NodeStack] = field(default_factory=list)
    """Stacks of collapsed nodes contracted into one node for the layout."""

    @property
    def G(self) -> LayoutGraph[Node]:
        return self.CG.G

    @property
    def T(self) -> DiGraph[Node | Cluster]:
        return self.CG.T

    @property
    def state(self) -> LayoutState:
        return self.CG.state

    @property
    def options(self) -> SugiyamaOptions:
        return self.CG.state.options


type StepFunction = Callable[[Layout], None]


def _always(options: SugiyamaOptions) -> bool:
    return True


@dataclass(frozen=True, slots=True)
class Step:
    """One pass of the layout."""

    name: str
    run: StepFunction
    enabled: Callable[[SugiyamaOptions], bool] = _always
    """Whether the step runs under the given options."""
    phase: Phase | None = None
    """The phase this step is, if it is one of the four."""
    requires: frozenset[Fact] = frozenset()
    """What must hold when the step starts."""
    provides: frozenset[Fact] = frozenset()
    """What holds once it is done."""
    removes: frozenset[Fact] = frozenset()
    """What stops holding once it is done."""


class PipelineError(ValueError):
    """The steps of a pipeline do not fit together."""


class InvariantError(AssertionError):
    """A step left the graph in a state it (or an earlier step) promised it
    would not be in."""


type Observer = Callable[[Step, Layout, float], None]
"""Called after each step with the step, the layout and the seconds taken."""


@dataclass(slots=True)
class Pipeline:
    """An ordered list of steps."""

    steps: list[Step] = field(default_factory=list)

    def __iter__(self) -> Iterator[Step]:
        return iter(self.steps)

    def names(self) -> list[str]:
        return [step.name for step in self.steps]

    def index(self, name: str) -> int:
        for i, step in enumerate(self.steps):
            if step.name == name:
                return i
        raise KeyError(f"no step named {name!r}; steps are {self.names()}")

    def __getitem__(self, name: str) -> Step:
        return self.steps[self.index(name)]

    def replace(self, name: str, run: StepFunction) -> None:
        """Keep the step called *name* but have it run *run* instead."""
        i = self.index(name)
        self.steps[i] = replace(self.steps[i], run=run)

    def insert_before(self, name: str, step: Step) -> None:
        self.steps.insert(self.index(name), step)

    def insert_after(self, name: str, step: Step) -> None:
        self.steps.insert(self.index(name) + 1, step)

    def remove(self, name: str) -> None:
        del self.steps[self.index(name)]

    def check(self, options: SugiyamaOptions | None = None) -> None:
        """Raise :class:`PipelineError` unless every step that runs under
        *options* finds what it requires provided by the steps before."""
        options = options or SugiyamaOptions()
        facts: set[Fact] = set()
        for step in self.steps:
            if not step.enabled(options):
                continue
            missing = step.requires - facts
            if missing:
                raise PipelineError(
                    f"step {step.name!r} requires the graph to be "
                    f"{_listed(missing)}, which no step before it provides "
                    f"(or one took away). Steps: {self.names()}"
                )
            facts -= step.removes
            facts |= step.provides

    def run(
        self,
        layout: Layout,
        observer: Observer | None = None,
        *,
        verify: bool = False,
    ) -> None:
        """Run the steps on *layout*. With *verify*, check after every step
        that the graph is what the steps so far say it is."""
        options = layout.options
        self.check(options)
        facts: set[Fact] = set()
        for step in self.steps:
            if not step.enabled(options):
                continue
            start = time.perf_counter()
            step.run(layout)
            if observer is not None:
                observer(step, layout, time.perf_counter() - start)
            facts -= step.removes
            facts |= step.provides
            if verify:
                for fact in sorted(facts):
                    try:
                        CHECKS.get(fact, _no_check)(layout)
                    except AssertionError as error:
                        raise InvariantError(
                            f"after step {step.name!r} the graph is not "
                            f"{fact.value}: {error}"
                        ) from error


def _listed(facts: Iterable[Fact]) -> str:
    return " and ".join(sorted(fact.value for fact in facts))


def _no_check(layout: Layout) -> None:
    pass


# What each fact means, as a check of the graph.


def _is_border(v: Node) -> bool:
    return v.type == Kind.VERTICAL_BORDER


def _check_ranked(layout: Layout) -> None:
    for v in layout.G:
        assert _is_border(v) or isinstance(v.rank, int), f"{v!r} has no rank"
    for link in layout.G.all_links():
        u, v = link.fromnode, link.tonode
        if _is_border(u) or _is_border(v):
            continue
        assert u.rank < v.rank, f"link {u!r} -> {v!r} runs from {u.rank} to {v.rank}"


def _check_proper(layout: Layout) -> None:
    for link in layout.G.all_links():
        u, v = link.fromnode, link.tonode
        if _is_border(u) or _is_border(v):
            continue
        assert v.rank - u.rank == 1, (
            f"link {u!r} -> {v!r} spans {v.rank - u.rank} columns"
        )


def _check_columns(layout: Layout) -> None:
    G = layout.G
    columns = getattr(G, "columns", None)
    assert columns is not None, "the graph has no columns"
    seen: set[Node] = set()
    for col in columns:
        for v in col:
            assert v in G, f"{v!r} is in a column but not in the graph"
            assert v not in seen, f"{v!r} is in two columns"
            assert v.col is col, f"{v!r}.col is not the column it is in"
            seen.add(v)
    missing = [v for v in G if v not in seen]
    assert not missing, f"{missing[0]!r} is in no column"


def _frames_of(v: Node) -> list[Cluster]:
    frames = []
    c = v.cluster
    while c is not None:
        frames.append(c)
        c = c.cluster
    return frames


def _check_ordered(layout: Layout) -> None:
    for col in layout.G.columns:
        last_seen: dict[Cluster, int] = {}
        for i, v in enumerate(col):
            if _is_border(v):
                continue
            for c in _frames_of(v):
                if c in last_seen:
                    between = [
                        w
                        for w in col[last_seen[c] + 1 : i]
                        if not _is_border(w) and c not in _frames_of(w)
                    ]
                    assert not between, (
                        f"{between[0]!r} sits between nodes of the frame "
                        f"{c.node!r} in a column"
                    )
                last_seen[c] = i


def _check_y(layout: Layout) -> None:
    G = layout.G
    for v in G:
        assert v.y is not None, f"{v!r} has no y"  # type: ignore[redundant-expr]
    for col in getattr(G, "columns", ()):
        placed = [v for v in col if v in G]
        for above, below in itertools.pairwise(placed):
            assert above.y - above.height >= below.y - 0.01, (
                f"{above!r} (y {above.y:g}, height {above.height:g}) overlaps "
                f"{below!r} (y {below.y:g}) below it in its column"
            )


def _check_x(layout: Layout) -> None:
    G = layout.G
    for v in G:
        assert v.x is not None, f"{v!r} has no x"  # type: ignore[redundant-expr]
    right = None
    for col in getattr(G, "columns", ()):
        placed = [v for v in col if v in G]
        if not placed:
            continue
        left = min(placed, key=lambda v: v.x)
        assert right is None or right.x + right.width <= left.x + 0.01, (
            f"{left!r} (x {left.x:g}) starts before {right!r} of the column "
            f"before ends (x {right.x + right.width:g})"
        )
        right = max(placed, key=lambda v: v.x + v.width)


CHECKS: dict[Fact, Callable[[Layout], None]] = {
    Fact.RANKED: _check_ranked,
    Fact.PROPER: _check_proper,
    Fact.COLUMNS: _check_columns,
    Fact.ORDERED: _check_ordered,
    Fact.Y: _check_y,
    Fact.X: _check_x,
}
"""How to check each fact against a layout: a function that raises
``AssertionError`` when it does not hold. Facts without an entry are taken
on trust."""
