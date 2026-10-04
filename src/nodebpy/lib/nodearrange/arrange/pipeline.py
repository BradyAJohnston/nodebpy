# SPDX-License-Identifier: GPL-2.0-or-later
"""The layout as a list of named steps.

A layered layout is a sequence of passes over one graph. Four of them are
the *phases* that decide the layout, each with interchangeable strategies:

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
out as edits. (The split into phases and intermediate processors follows
the Eclipse Layout Kernel's layered algorithm.)

:func:`default_pipeline` builds the standard list. To experiment, take it
and :meth:`~Pipeline.replace` a step, :meth:`~Pipeline.insert_after` one, or
:func:`register` a new strategy for a phase and select it in the settings.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from ..config import LayoutState, Settings
from .common import Vec2
from .graph import Cluster, ClusterGraph, Node
from .tree import DiGraph, Tree

if TYPE_CHECKING:
    from .stacking import NodeStack

type Phase = Literal["rank", "order", "place", "route"]

PHASES: tuple[Phase, ...] = ("rank", "order", "place", "route")


@dataclass(slots=True)
class Layout:
    """The graph being laid out and everything the steps share."""

    CG: ClusterGraph
    old_center: Vec2
    """Centre of the nodes before the layout; the result is centred there."""
    node_stacks: list[NodeStack] = field(default_factory=list)
    """Stacks of collapsed nodes contracted into one node for the layout."""

    @property
    def G(self) -> Tree[Node]:
        return self.CG.G

    @property
    def T(self) -> DiGraph[Node | Cluster]:
        return self.CG.T

    @property
    def state(self) -> LayoutState:
        return self.CG.state

    @property
    def settings(self) -> Settings:
        return self.CG.state.settings


type StepFunction = Callable[[Layout], None]


def _always(settings: Settings) -> bool:
    return True


@dataclass(frozen=True, slots=True)
class Step:
    """One pass of the layout."""

    name: str
    run: StepFunction
    enabled: Callable[[Settings], bool] = _always
    """Whether the step runs under the given settings."""
    phase: Phase | None = None
    """The phase this step is the strategy of, if any."""


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
        old = self.steps[i]
        self.steps[i] = Step(old.name, run, old.enabled, old.phase)

    def insert_before(self, name: str, step: Step) -> None:
        self.steps.insert(self.index(name), step)

    def insert_after(self, name: str, step: Step) -> None:
        self.steps.insert(self.index(name) + 1, step)

    def remove(self, name: str) -> None:
        del self.steps[self.index(name)]

    def run(self, layout: Layout, observer: Observer | None = None) -> None:
        settings = layout.settings
        for step in self.steps:
            if not step.enabled(settings):
                continue
            start = time.perf_counter()
            step.run(layout)
            if observer is not None:
                observer(step, layout, time.perf_counter() - start)


# -------------------------------------------------------------------
# Strategies

_STRATEGIES: dict[Phase, dict[str, StepFunction]] = {phase: {} for phase in PHASES}


def register(phase: Phase, name: str) -> Callable[[StepFunction], StepFunction]:
    """Decorator: make a function available as the strategy *name* of
    *phase*. It is selected with the setting named after the phase's role
    (``Settings.ranking`` and so on)."""

    def decorator(run: StepFunction) -> StepFunction:
        _STRATEGIES[phase][name] = run
        return run

    return decorator


def strategies(phase: Phase) -> list[str]:
    """Names of the strategies registered for *phase*."""
    return list(_STRATEGIES[phase])


def strategy(phase: Phase, name: str) -> StepFunction:
    try:
        return _STRATEGIES[phase][name]
    except KeyError:
        raise ValueError(
            f"unknown {phase} strategy {name!r}; choose from {strategies(phase)}"
        ) from None
