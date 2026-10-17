"""Keep the edits a user made to a tree's layout across a rebuild.

A rebuilt tree is a new set of nodes. :func:`record` reads the layout of the
old ones before they go, and :func:`restore` matches them to the new ones and
carries the layout over once the new tree is arranged: location, width,
collapsed state, hidden sockets, colour, label and frame. A node that matches
nothing stays where the arrangement put it, moved by as much as its matched
neighbours were, and down out of the way of the others.

Nodes are matched by what they compute, as a hash of their type, settings,
unlinked values and inputs, the hashes of the nodes feeding them included,
then by looser keys for the nodes left over: without the values (a value
changed in the code), without the inputs (a node rewired), and so on.
Reroutes are seen through, so the reroutes an arrangement adds or removes
don't change the hash of the nodes downstream.

Every :func:`~.api.arrange` remembers the layout it produced (:func:`stamp`).
A tree whose layout is still that one has no edits to keep, and :func:`record`
returns None for it: a fresh arrangement suits a changed tree better than the
old one would.
"""

from __future__ import annotations

import hashlib
import statistics
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

import bpy
from bpy.types import Node, NodeFrame, NodeSocket, NodeTree

from .common import FRAME_PADDING, frame_label_room
from .node_size import dimensions, top_offset

__all__ = ["Edits", "record", "restore", "stamp"]

_ARRANGED: dict[int, str] = {}
"""The layout each arranged tree was left with, by ``session_uid``. Kept in
memory rather than on the tree, so it never reaches the saved file or an
export."""

_BASE_PROPERTIES = frozenset(bpy.types.Node.bl_rna.properties.keys())
_VALUE_TYPES = frozenset({"BOOLEAN", "INT", "FLOAT", "STRING", "ENUM"})
_GAP = 20.0
"""Space left above and below a node moved out of another's way."""


@dataclass
class _NodeLayout:
    keys: tuple[str | None, ...]
    location: tuple[float, float]
    width: float
    hide: bool
    show_options: bool
    label: str
    color: tuple[float, float, float] | None
    hidden_inputs: frozenset[str]
    hidden_outputs: frozenset[str]
    frame: int | None


@dataclass
class _FrameLayout:
    label: str
    color: tuple[float, float, float] | None
    shrink: bool
    label_size: int
    text: Any
    location: tuple[float, float]
    width: float
    height: float
    frame: int | None


@dataclass
class Edits:
    """The layout of a tree's nodes, read by :func:`record`."""

    nodes: list[_NodeLayout] = field(default_factory=list)
    frames: list[_FrameLayout] = field(default_factory=list)


def _round(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 5)
    if isinstance(value, bpy.types.ID):
        return value.name_full
    if isinstance(value, (str, bool, int)) or value is None:
        return value
    try:
        return tuple(_round(v) for v in value)
    except TypeError:
        return str(value)


def _xy(node: Node) -> tuple[float, float]:
    location = node.location_absolute
    return (location.x, location.y)


def _color(node: Node) -> tuple[float, float, float] | None:
    if not node.use_custom_color:
        return None
    color = node.color
    return (color[0], color[1], color[2])


def _frames(tree: NodeTree) -> list[NodeFrame]:
    return [node for node in tree.nodes if isinstance(node, NodeFrame)]


def _layout_digest(tree: NodeTree) -> str:
    rows = []
    for node in tree.nodes:
        rows.append(
            (
                node.name,
                _round(_xy(node)),
                _round(node.width),
                node.hide,
                node.parent.name if node.parent else None,
                node.label,
                _round(_color(node)),
                tuple(s.hide for s in node.inputs),
                tuple(s.hide for s in node.outputs),
            )
        )
    rows.sort(key=lambda row: row[0])
    return hashlib.sha1(repr(rows).encode()).hexdigest()


def stamp(tree: NodeTree) -> None:
    """Remember *tree*'s layout as the one an arrangement left it with."""
    _ARRANGED[tree.session_uid] = _layout_digest(tree)


def _socket_ref(socket: NodeSocket, sockets: Iterable[NodeSocket]) -> tuple:
    # Names rather than identifiers: rebuilding an interface gives its
    # sockets new identifiers.
    same = [s for s in sockets if s.name == socket.name]
    return (socket.name, same.index(socket))


def _settings(node: Node) -> tuple:
    values = []
    for prop in node.bl_rna.properties:
        name = prop.identifier
        if name in _BASE_PROPERTIES:
            continue
        if prop.type == "POINTER":
            target = getattr(node, name, None)
            if isinstance(target, bpy.types.ID):
                values.append((name, target.name_full))
        elif prop.type in _VALUE_TYPES:
            values.append((name, _round(getattr(node, name, None))))
    sockets = tuple(
        (s.name, s.bl_idname) for s in (*node.inputs, *node.outputs) if s.enabled
    )
    return (node.bl_idname, tuple(values), sockets)


def _values(node: Node) -> tuple:
    return tuple(
        (_socket_ref(s, node.inputs), _round(getattr(s, "default_value", None)))
        for s in node.inputs
        if s.enabled and not s.is_linked and hasattr(s, "default_value")
    )


def _hash(*parts: Any) -> str:
    return hashlib.sha1(repr(parts).encode()).hexdigest()


class _Graph:
    """The links of a tree with its reroutes seen through."""

    def __init__(self, tree: NodeTree):
        self.nodes = [node for node in tree.nodes if not isinstance(node, NodeFrame)]
        Links = list[tuple[NodeSocket, Node, NodeSocket]]
        self.sources: dict[Node, Links] = {}
        self.targets: dict[Node, Links] = {}
        self.neighbours: dict[Node, set[Node]] = {node: set() for node in self.nodes}
        for link in tree.links:
            if link.is_muted or link.from_node is None or link.to_node is None:
                continue
            self.neighbours[link.from_node].add(link.to_node)
            self.neighbours[link.to_node].add(link.from_node)
            if link.to_node.bl_idname == "NodeReroute":
                continue
            source = self._source(link.from_socket)
            if source is None:
                continue
            origin = source.node
            assert link.to_socket is not None and origin is not None
            self.sources.setdefault(link.to_node, []).append(
                (link.to_socket, origin, source)
            )
            self.targets.setdefault(origin, []).append(
                (source, link.to_node, link.to_socket)
            )
        self.reroute_sources = {
            node: self._source(node.outputs[0])
            for node in self.nodes
            if node.bl_idname == "NodeReroute"
        }

    @staticmethod
    def _source(socket: NodeSocket | None) -> NodeSocket | None:
        seen = set()
        while socket is not None:
            node = socket.node
            if node is None or node.bl_idname != "NodeReroute":
                break
            if node in seen:
                return None
            seen.add(node)
            links = node.inputs[0].links
            socket = links[0].from_socket if links else None
        return socket


def _keys(tree: NodeTree) -> tuple[_Graph, dict[Node, tuple[str | None, ...]]]:
    graph = _Graph(tree)
    settings = {node: _settings(node) for node in graph.nodes}
    values = {node: _values(node) for node in graph.nodes}

    def upstream(local: Callable[[Node], Any]) -> Callable[[Node], str]:
        memo: dict[Node, str] = {}

        def digest(node: Node) -> str:
            if node not in memo:
                memo[node] = ""  # a cycle (there should be none) ends here
                inputs = sorted(
                    (
                        _socket_ref(to_socket, node.inputs),
                        digest(source),
                        _socket_ref(from_socket, source.outputs),
                    )
                    for to_socket, source, from_socket in graph.sources.get(node, ())
                )
                memo[node] = _hash(local(node), inputs)
            return memo[node]

        return digest

    def downstream(digest: Callable[[Node], str], node: Node) -> str:
        return _hash(
            digest(node),
            sorted(
                (_socket_ref(s, node.outputs), digest(t), _socket_ref(ts, t.inputs))
                for s, t, ts in graph.targets.get(node, ())
            ),
        )

    full = upstream(lambda node: (settings[node], values[node]))
    shape = upstream(lambda node: settings[node])

    keys: dict[Node, tuple[str | None, ...]] = {}
    for node in graph.nodes:
        if node.bl_idname == "NodeReroute":
            source = graph.reroute_sources[node]
            origin_node = source.node if source is not None else None
            if source is None or origin_node is None:
                keys[node] = (None,) * 6
                continue
            ends = sorted(
                full(t) for t in graph.neighbours[node] if t.bl_idname != "NodeReroute"
            )
            origin = _socket_ref(source, origin_node.outputs)
            keys[node] = (
                _hash("reroute", full(origin_node), origin, ends),
                _hash("reroute", shape(origin_node), origin),
                None,
                None,
                None,
                None,
            )
            continue
        keys[node] = (
            downstream(full, node),
            full(node),
            downstream(shape, node),
            shape(node),
            _hash(settings[node], values[node]),
            _hash(settings[node]),
        )
    return graph, keys


def record(tree: NodeTree) -> Edits | None:
    """Read the layout of *tree*'s nodes, to :func:`restore` onto its
    rebuild; None when the layout is still the one *tree* was last
    arranged with, so there are no edits to keep."""
    if _ARRANGED.get(tree.session_uid) == _layout_digest(tree):
        return None
    edits = Edits()
    frames = _frames(tree)
    index: dict[Node | None, int] = {frame: i for i, frame in enumerate(frames)}
    for frame in frames:
        edits.frames.append(
            _FrameLayout(
                label=frame.label,
                color=_color(frame),
                shrink=frame.shrink,
                label_size=frame.label_size,
                text=frame.text,
                location=_xy(frame),
                width=frame.width,
                height=frame.height,
                frame=index.get(frame.parent),
            )
        )
    _, keys = _keys(tree)
    for node, node_keys in keys.items():
        edits.nodes.append(
            _NodeLayout(
                keys=node_keys,
                location=_xy(node),
                width=node.width,
                hide=node.hide,
                show_options=node.show_options,
                label=node.label,
                color=_color(node),
                hidden_inputs=frozenset(
                    s.identifier for s in node.inputs if s.hide and s.enabled
                ),
                hidden_outputs=frozenset(
                    s.identifier for s in node.outputs if s.hide and s.enabled
                ),
                frame=index.get(node.parent),
            )
        )
    return edits


def _match(
    old: list[_NodeLayout], new: dict[Node, tuple[str | None, ...]]
) -> dict[Node, _NodeLayout]:
    matched: dict[Node, _NodeLayout] = {}
    taken: set[int] = set()
    for level in range(6):
        buckets: dict[str, list[int]] = {}
        for i, layout in enumerate(old):
            key = layout.keys[level]
            if i not in taken and key is not None:
                buckets.setdefault(key, []).append(i)
        for node, keys in new.items():
            key = keys[level]
            if node in matched or key is None or not buckets.get(key):
                continue
            i = buckets[key].pop(0)
            taken.add(i)
            matched[node] = old[i]
    return matched


def _box(node: Node, location: tuple[float, float]) -> tuple[float, ...]:
    width, height = dimensions(node)
    top = location[1] - top_offset(node)
    return (location[0], top - height, location[0] + width, top)


def _overlap(a: tuple[float, ...], b: tuple[float, ...]) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] + _GAP and b[1] < a[3] + _GAP


def _fit_frame(frame: NodeFrame, children: list[tuple[float, ...]]) -> None:
    label = frame_label_room(frame.label, frame.label_size)
    left = min(b[0] for b in children) - FRAME_PADDING
    bottom = min(b[1] for b in children) - FRAME_PADDING
    right = max(b[2] for b in children) + FRAME_PADDING
    top = max(b[3] for b in children) + FRAME_PADDING + label
    frame.location_absolute = (left, top)
    frame.width = right - left
    frame.height = top - bottom


def restore(edits: Edits, tree: NodeTree) -> None:
    """Carry the layout in *edits* over to the matching nodes of *tree*, a
    rebuild of the tree it was read from, after *tree* was arranged."""
    graph, keys = _keys(tree)
    matched = _match(edits.nodes, keys)
    if not matched:
        return

    arranged = {node: _xy(node) for node in graph.nodes}

    # Frames: the rebuild's own frames take the place of old ones with the
    # same label; the others are made again around their matched nodes.
    used = {layout.frame for layout in matched.values() if layout.frame is not None}
    pending = list(used)
    while pending:
        outer = edits.frames[pending.pop()].frame
        if outer is not None and outer not in used:
            used.add(outer)
            pending.append(outer)
    built = _frames(tree)
    frames: dict[int, NodeFrame] = {}
    for i, layout in enumerate(edits.frames):
        if i not in used:
            continue
        same = next((f for f in built if f.label == layout.label), None)
        if same is not None:
            built.remove(same)
            frames[i] = same
            continue
        frame = tree.nodes.new("NodeFrame")
        assert isinstance(frame, NodeFrame)
        frame.label = layout.label
        frame.shrink = layout.shrink
        frame.label_size = layout.label_size
        frame.text = layout.text
        frames[i] = frame
    for i, frame in frames.items():
        layout = edits.frames[i]
        if layout.color is not None:
            frame.use_custom_color = True
            frame.color = layout.color
        frame.parent = None if layout.frame is None else frames[layout.frame]

    deltas: dict[Node, tuple[float, float]] = {}
    for node, layout in matched.items():
        if layout.frame is not None:
            node.parent = frames[layout.frame]
        node.width = layout.width
        node.hide = layout.hide
        node.show_options = layout.show_options
        if not node.label:
            node.label = layout.label
        if layout.color is not None and not node.use_custom_color:
            node.use_custom_color = True
            node.color = layout.color
        for socket in node.inputs:
            if socket.enabled and socket.identifier in layout.hidden_inputs:
                socket.hide = True
        for socket in node.outputs:
            if socket.enabled and socket.identifier in layout.hidden_outputs:
                socket.hide = True
        node.location_absolute = layout.location
        x, y = arranged[node]
        deltas[node] = (layout.location[0] - x, layout.location[1] - y)

    # The nodes that matched nothing keep their place relative to their
    # neighbours, and move down until they clear every other node.
    boxes = [_box(node, _xy(node)) for node in matched]
    for node in graph.nodes:
        if node in matched:
            continue
        near = [deltas[n] for n in graph.neighbours[node] if n in deltas]
        pool = near or list(deltas.values())
        dx = statistics.median(d[0] for d in pool)
        dy = statistics.median(d[1] for d in pool)
        x, y = arranged[node][0] + dx, arranged[node][1] + dy
        box = _box(node, (x, y))
        for _ in range(len(boxes) + 1):
            hit = next((b for b in boxes if _overlap(box, b)), None)
            if hit is None:
                break
            y -= box[3] - hit[1] + _GAP
            box = _box(node, (x, y))
        node.location_absolute = (x, y)
        boxes.append(box)

    # Frames last, inner ones first: an old frame whose nodes all kept their
    # place keeps its box; any other frame is fitted around its nodes.
    kept = {frame: i for i, frame in frames.items()}

    def depth(node: Node) -> int:
        return 0 if node.parent is None else 1 + depth(node.parent)

    for frame in sorted(_frames(tree), key=depth, reverse=True):
        children = [n for n in tree.nodes if n.parent == frame]
        if not children:
            continue
        # Blender fits a Shrink frame to its nodes itself, but only when a
        # node editor draws it.
        if frame in kept and not frame.shrink and all(n in matched for n in children):
            layout = edits.frames[kept[frame]]
            frame.location_absolute = layout.location
            frame.width = layout.width
            frame.height = layout.height
        else:
            _fit_frame(frame, [_frame_or_node_box(n) for n in children])


def _frame_or_node_box(node: Node) -> tuple[float, ...]:
    x, y = _xy(node)
    if isinstance(node, NodeFrame):
        return (x, y - node.height, x + node.width, y)
    return _box(node, (x, y))
