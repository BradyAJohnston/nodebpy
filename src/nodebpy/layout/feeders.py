"""Feeders: nodes whose links out all go to one node of their own frame,
such as the samples summed by a chain of Add nodes.

The ranking puts a feeder as close to what feeds it as to what it feeds, so
the feeders of a long chain pile up in the first columns, far from the
nodes they feed. Three steps keep each one beside the node it feeds:
:func:`move_feeders_right` puts it in the column just before that node,
:func:`tuck_feeders` next to another node of that column feeding the same
node, and :func:`pull_up_feeders` against that node."""

from __future__ import annotations

from .model import is_real
from .pipeline import Layout
from .placement import separation


def move_feeders_right(layout: Layout) -> None:
    """Move each feeder to the column just before the node it feeds. The
    nodes are visited from the last column back, so a feeder of a feeder
    follows it."""
    G = layout.G
    for v in sorted(G, key=lambda v: v.rank, reverse=True):
        if not is_real(v) or v.is_reroute or len(G.successors(v)) != 1:
            continue
        (w,) = G.successors(v)
        if is_real(w) and w.cluster is v.cluster and v.rank < w.rank - 1:
            v.rank = w.rank - 1
            layout.moved_feeders.add(v)


def tuck_feeders(layout: Layout) -> None:
    """Put each moved feeder next to another node of its column that feeds
    the same node (its *anchor*), on the side of it the ordering chose, and
    behind the feeders already there. Nothing then passes between a feeder
    and its anchor."""
    G = layout.G
    moved = layout.moved_feeders
    for col in G.columns:
        order = list(col)
        for v in [v for v in col if v in moved]:
            (w,) = G.successors(v)
            if not is_real(w):
                continue
            anchor = next(
                (
                    u
                    for u in G.predecessors(w)
                    if u.col is col and u not in moved and u.cluster is v.cluster
                ),
                None,
            )
            if anchor is None:
                continue

            # The feeders of the same node already tucked beside the anchor.
            siblings = {u for u in G.predecessors(w) if u in moved}
            below = col.index(v) > col.index(anchor)
            order.remove(v)
            i = order.index(anchor)
            if below:
                i += 1
                while i < len(order) and order[i] in siblings:
                    i += 1
            else:
                while i > 0 and order[i - 1] in siblings:
                    i -= 1
            order.insert(i, v)
            layout.tucked_feeders[v] = (anchor, below)
        col[:] = order


def pull_up_feeders(layout: Layout) -> None:
    """Move each tucked feeder against its anchor, or the feeder between
    them, as close as the margin allows, however its own links would place
    it. Feeders below their anchor are pulled up, those above it down."""
    tucked = layout.tucked_feeders
    state = layout.state
    for col in layout.G.columns:
        for below in (True, False):
            indices = range(1, len(col)) if below else range(len(col) - 2, -1, -1)
            for i in indices:
                v = col[i]
                if v not in tucked or tucked[v][1] is not below:
                    continue
                anchor = tucked[v][0]
                u = col[i - 1] if below else col[i + 1]
                if u is not anchor and (u not in tucked or tucked[u][0] is not anchor):
                    continue
                if below:
                    v.y = u.y - separation(u, u, v, state)
                else:
                    v.y = u.y + separation(v, v, u, state)
