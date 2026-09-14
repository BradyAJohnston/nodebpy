from __future__ import annotations

import warnings
from collections import Counter, deque
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from dataclasses import replace as dataclass_replace
from typing import Any, Literal, cast

import bpy

from ._socket_order import SOCKET_ORDER

# Estimated row heights (in unscaled UI units) used to model node layout
# without a UI. Blender only computes real node/socket geometry when a node
# editor draws the tree, which never happens under the headless ``bpy``
# module. HEADER and SOCKET_ROW are calibrated against a UI-arranged tree
# whose reroutes the arranger had socket-aligned: reroute y minus node top
# measures the real socket offsets, giving header + (i + 0.5) * row fits of
# 24.5 / 21.75. The remaining rows scale to the same grid.
HEADER = 24.5
SOCKET_ROW = 21.75
HIDDEN_SOCKET = 14
HIDDEN_HEADER = 30
PROPERTY_ROW = 24
VECTOR_EXPANDED = 65.25  # three extra value rows


def _is_layoutable(node: bpy.types.Node) -> bool:
    """Check if a node should be included in column-based layout.

    Frame nodes are containers and reroute nodes are tiny routing helpers;
    neither should occupy a full column slot.
    """
    return node.bl_idname not in ("NodeFrame", "NodeReroute")


def build_dependency_graph(
    tree: bpy.types.NodeTree,
) -> tuple[dict[bpy.types.Node, set[bpy.types.Node]], Counter]:
    """Build a graph of node dependencies and count input connections.

    Only layoutable nodes (excluding frames and reroutes) are included.
    """
    layoutable = {n for n in tree.nodes if _is_layoutable(n)}
    dependency_graph: dict[bpy.types.Node, set[bpy.types.Node]] = {
        node: set() for node in layoutable
    }
    socket_input_connection_count: Counter = Counter()

    for link in tree.links:
        if link.from_node in layoutable and link.to_node in layoutable:
            dependency_graph[link.from_node].add(link.to_node)
        socket_input_connection_count[link.to_socket] += 1

    return dependency_graph, socket_input_connection_count


def topological_sort(
    dependency_graph: dict[bpy.types.Node, set[bpy.types.Node]],
) -> list[bpy.types.Node]:
    """Sort nodes in topological (dependency) order using Kahn's algorithm."""
    incoming = {node: 0 for node in dependency_graph}
    for dependents in dependency_graph.values():
        for target in dependents:
            incoming[target] += 1

    queue = deque(node for node, count in incoming.items() if count == 0)
    result: list[bpy.types.Node] = []

    while queue:
        current = queue.popleft()
        result.append(current)
        for dependent in dependency_graph[current]:
            incoming[dependent] -= 1
            if incoming[dependent] == 0:
                queue.append(dependent)

    return result


def organize_into_columns(
    nodes_in_order: list[bpy.types.Node],
    dependency_graph: dict[bpy.types.Node, set[bpy.types.Node]],
) -> list[list[bpy.types.Node]]:
    """Assign each node to a column based on its furthest dependent."""
    columns: list[list[bpy.types.Node]] = []
    column_of: dict[bpy.types.Node, int] = {}

    for node in reversed(nodes_in_order):
        col = (
            max(
                (column_of[dep] for dep in dependency_graph[node]),
                default=-1,
            )
            + 1
        )
        column_of[node] = col

        if col == len(columns):
            columns.append([node])
        else:
            columns[col].append(node)

    # reverse so flow goes left-to-right
    return list(reversed(columns))


# Node-specific RNA properties Blender never draws in the node body: UI
# bookkeeping for item lists and zones rather than settings.
_UNDRAWN_PROPERTIES = frozenset(
    {"is_active_output", "vector_dimensions", "inspection_index"}
)

# Rows a colour-picker widget (the Color input node) takes up.
_COLOR_PICKER_ROWS = 6


def _is_id_pointer(prop: Any) -> bool:
    """Whether a POINTER property references an ID datablock (drawn as a
    datablock selector) rather than an internal struct or another node."""
    fixed = getattr(prop, "fixed_type", None)
    if fixed is None:
        return False
    rna_type = getattr(bpy.types, fixed.bl_rna.identifier, None)
    return rna_type is not None and issubclass(rna_type, bpy.types.ID)


def node_property_rows(node: bpy.types.Node) -> list[tuple[Any, int]]:
    """The node-specific RNA properties Blender draws in the node body, each
    with the number of :data:`PROPERTY_ROW` rows it takes.

    Properties inherited from the node's base classes (location, label, ...)
    are skipped, as are item collections, pointers to internal structs or
    other nodes (a zone's ``paired_output``) and known bookkeeping flags —
    none of which draw a widget. Vector-valued properties draw one number
    field per component; a colour property draws a picker.

    ``bl_rna`` exists on bpy classes via their metaclass, invisible to type
    checkers looking at plain ``type``.
    """
    inherited_ids = {
        prop.identifier
        for base in type(node).__bases__
        for prop in cast(Any, base).bl_rna.properties
    }
    rows: list[tuple[Any, int]] = []
    for prop in node.bl_rna.properties:
        if prop.identifier in inherited_ids or prop.identifier in _UNDRAWN_PROPERTIES:
            continue
        if prop.identifier.startswith("active_"):
            continue  # active item / index of an item list, edited in the sidebar
        if prop.type == "COLLECTION":
            continue
        if prop.type == "POINTER" and not _is_id_pointer(prop):
            continue
        count = 1
        array_length = int(getattr(prop, "array_length", 0) or 0)
        if prop.type in ("FLOAT", "INT") and array_length > 1:
            if getattr(prop, "subtype", "NONE") == "COLOR":
                count = _COLOR_PICKER_ROWS
            else:
                count = int(getattr(node, "vector_dimensions", array_length))
        rows.append((prop, count))
    return rows


def _node_property_count(node: bpy.types.Node) -> int:
    """Number of :data:`PROPERTY_ROW` rows the node's drawn properties take."""
    return sum(count for _, count in node_property_rows(node))


def _socket_visible(socket: bpy.types.NodeSocket) -> bool:
    """Whether Blender draws this socket on an expanded node: enabled, and
    not hidden — a hidden socket reappears while it is linked (the editor's
    Hide Unused Sockets only hides unlinked ones)."""
    return socket.enabled and (not socket.hide or socket.is_linked)


def _is_expanded_vector(
    socket: bpy.types.NodeSocket,
    socket_input_connection_count: Counter | None,
) -> bool:
    """Whether an input draws the expanded 3-component vector widget: an
    unlinked vector whose value is shown (``hide_value`` sockets, such as
    Set Position's *Position*, draw just their label)."""
    if socket.type != "VECTOR" or socket.hide_value:
        return False
    if socket_input_connection_count is None:
        return not socket.is_linked
    return socket_input_connection_count[socket] == 0


@dataclass(frozen=True)
class NodeRow:
    """One drawn row of an expanded node, as the headless row model sees it.

    ``top`` is the row's offset (<= 0) from the node's top edge and
    ``height`` its extent; ``anchor`` is where a socket marker sits. Socket
    rows carry their ``socket`` (plus an aligned output ``partner``);
    property rows the RNA ``prop``; panel rows the ``panel`` (an interface
    panel item for group nodes, the declared name for built-in nodes),
    whether it is ``open``, and — when closed — the linked
    ``collapsed_sockets`` Blender draws on the header instead.
    """

    kind: Literal["output", "property", "input", "panel"]
    top: float
    height: float
    socket: bpy.types.NodeSocket | None = None
    prop: Any = None
    panel: Any = None
    depth: int = 0
    open: bool = True
    collapsed_sockets: tuple[bpy.types.NodeSocket, ...] = ()
    #: An output drawn on the same row as this input (Blender's
    #: ``align_with_previous`` sockets: Set Position's Geometry in/out, a
    #: Menu Switch item's value input and "chosen" output, ...).
    partner: bpy.types.NodeSocket | None = None
    #: A boolean input drawn as a checkbox in this panel's header.
    toggle: bpy.types.NodeSocket | None = None

    @property
    def sockets(self) -> tuple[bpy.types.NodeSocket, ...]:
        """Every socket anchored on this row."""
        found = [s for s in (self.socket, self.partner, self.toggle) if s is not None]
        return (*found, *self.collapsed_sockets)

    @property
    def anchor(self) -> float:
        """Vertical offset (<= 0) of the row's socket marker / centre."""
        if self.kind == "property":
            return self.top - self.height / 2
        # Socket and panel rows anchor on their first SOCKET_ROW; an expanded
        # vector's three value rows hang below its label row.
        return self.top - SOCKET_ROW / 2


def _is_root_panel(item: Any) -> bool:
    return item is None or getattr(item, "index", -1) < 0


def _interface_panels(node: bpy.types.Node) -> tuple[list[Any], dict[int, bool]] | None:
    """For a group node whose tree declares panels: the interface items in
    draw order and the node's per-panel collapsed state (keyed by the
    panel's persistent uid, falling back to ``default_closed``)."""
    if not node.bl_idname.endswith("NodeGroup"):
        return None
    tree = getattr(node, "node_tree", None)
    if tree is None:
        return None
    items = list(tree.interface.items_tree)
    if not any(item.item_type == "PANEL" for item in items):
        return None
    collapsed = {
        state.identifier: state.is_collapsed
        for state in getattr(node, "panel_states", ())
    }
    for item in items:
        if item.item_type == "PANEL":
            collapsed.setdefault(item.persistent_uid, item.default_closed)
    return items, collapsed


def node_rows(
    node: bpy.types.Node,
    socket_input_connection_count: Counter | None = None,
) -> list[NodeRow]:
    """The rows Blender draws below an expanded node's header, top to bottom.

    Conventionally drawn nodes list outputs first, then the node's drawn
    properties (:func:`node_property_rows`), then inputs; an unlinked, shown
    vector input is followed by its expanded three-value widget. Nodes that
    Blender draws from their declaration (``use_custom_socket_order``,
    recorded in :mod:`nodebpy.builder._socket_order`) follow that declared
    order instead: inputs and outputs interleaved, an aligned output sharing
    its input's row as its ``partner``, buttons where the declaration puts
    them, and panels. Group nodes whose interface declares panels draw them
    in interface order. Either way a panel is a header row with its sockets
    beneath it while open and — while closed — nothing but linked sockets
    gathered onto the header. When ``socket_input_connection_count`` is
    None, link state is read from ``socket.is_linked``.
    """
    rows: list[NodeRow] = []
    y = HEADER

    def add(kind: Any, height: float, **extra: Any) -> None:
        nonlocal y
        rows.append(NodeRow(kind, -y, height, **extra))
        y += height

    def add_input(socket: bpy.types.NodeSocket) -> None:
        height = SOCKET_ROW
        if _is_expanded_vector(socket, socket_input_connection_count):
            height += VECTOR_EXPANDED
        add("input", height, socket=socket)

    order = SOCKET_ORDER.get(node.bl_idname)
    if order is not None:
        return _rows_from_order(node, order, socket_input_connection_count)

    panels = _interface_panels(node)
    if panels is None:
        for socket in node.outputs:
            if _socket_visible(socket):
                add("output", SOCKET_ROW, socket=socket)
        for prop, count in node_property_rows(node):
            add("property", count * PROPERTY_ROW, prop=prop)
        for socket in node.inputs:
            if _socket_visible(socket):
                add_input(socket)
        return rows

    items, collapsed = panels
    by_key = {
        (socket.is_output, socket.identifier): socket
        for socket in (*node.inputs, *node.outputs)
    }
    # Top-level outputs sit above everything else, as on any node.
    for item in items:
        if (
            item.item_type == "SOCKET"
            and item.in_out == "OUTPUT"
            and _is_root_panel(item.parent)
        ):
            socket = by_key.get((True, item.identifier))
            if socket is not None and _socket_visible(socket):
                add("output", SOCKET_ROW, socket=socket)
    for prop, count in node_property_rows(node):
        add("property", count * PROPERTY_ROW, prop=prop)

    # Walk the remaining items in interface order. ``closed`` tracks the
    # innermost closed panel enclosing the current item, whose header row
    # collects the linked sockets Blender folds onto it.
    depth_of: dict[int, int] = {}
    closed_row: dict[int, int] = {}  # panel uid -> index of its header row
    for item in items:
        parent = item.parent
        parent_uid = None if _is_root_panel(parent) else parent.persistent_uid
        enclosing_closed = closed_row.get(parent_uid) if parent_uid else None
        if item.item_type == "PANEL":
            depth = 0 if parent_uid is None else depth_of[parent_uid] + 1
            depth_of[item.persistent_uid] = depth
            if enclosing_closed is not None:
                closed_row[item.persistent_uid] = enclosing_closed
                continue
            is_open = not collapsed.get(item.persistent_uid, item.default_closed)
            if not is_open:
                closed_row[item.persistent_uid] = len(rows)
            add("panel", SOCKET_ROW, panel=item, depth=depth, open=is_open)
            continue
        if item.in_out == "OUTPUT" and parent_uid is None:
            continue  # already placed at the top
        socket = by_key.get((item.in_out == "OUTPUT", item.identifier))
        if socket is None or not _socket_visible(socket):
            continue
        if enclosing_closed is not None:
            if socket.is_linked:
                header = rows[enclosing_closed]
                rows[enclosing_closed] = dataclass_replace(
                    header, collapsed_sockets=(*header.collapsed_sockets, socket)
                )
            continue
        if socket.is_output:
            add("output", SOCKET_ROW, socket=socket, depth=depth_of.get(parent_uid, 0))
        else:
            height = SOCKET_ROW
            if _is_expanded_vector(socket, socket_input_connection_count):
                height += VECTOR_EXPANDED
            add("input", height, socket=socket, depth=depth_of.get(parent_uid, 0))
    return rows


def _rows_from_order(
    node: bpy.types.Node,
    order: tuple[tuple, ...],
    socket_input_connection_count: Counter | None,
) -> list[NodeRow]:
    """Rows of a node drawn from its declaration (see ``_socket_order``)."""
    rows: list[NodeRow] = []
    y = HEADER
    inputs = list(node.inputs)
    outputs = list(node.outputs)
    by_key = {(s.is_output, s.identifier): s for s in (*inputs, *outputs)}
    literal_in = [e[1] for e in order if e[0] in ("in", "toggle")]
    literal_out = [e[1] for e in order if e[0] == "out"]
    placed: set[bpy.types.NodeSocket] = set()
    properties = node_property_rows(node)
    layout_drawn = False
    panel_states = list(getattr(node, "panel_states", ()))
    panel_index = 0
    # Stack of (depth, header row index or None when open) for enclosing panels.
    stack: list[tuple[int, int | None]] = []
    prev_socket_row: int | None = None  # index of the row an aligned entry may join
    last_panel_row: int | None = None  # header row of the most recently opened panel

    def add(kind: Any, height: float, **extra: Any) -> int:
        nonlocal y
        rows.append(NodeRow(kind, -y, height, **extra))
        y += height
        return len(rows) - 1

    def input_height(socket: bpy.types.NodeSocket) -> float:
        if _is_expanded_vector(socket, socket_input_connection_count):
            return SOCKET_ROW + VECTOR_EXPANDED
        return SOCKET_ROW

    def closed_header() -> int | None:
        return stack[-1][1] if stack else None

    def fold(socket: bpy.types.NodeSocket, header: int) -> None:
        if socket.is_linked:
            row = rows[header]
            rows[header] = dataclass_replace(
                row, collapsed_sockets=(*row.collapsed_sockets, socket)
            )

    def place(socket: bpy.types.NodeSocket, aligned: bool) -> None:
        nonlocal prev_socket_row
        placed.add(socket)
        if not _socket_visible(socket):
            return
        header = closed_header()
        if header is not None:
            fold(socket, header)
            return
        depth = len(stack)
        if aligned and prev_socket_row is not None:
            row = rows[prev_socket_row]
            if row.socket is not None and row.socket.is_output != socket.is_output:
                if socket.is_output and row.partner is None:
                    rows[prev_socket_row] = dataclass_replace(row, partner=socket)
                    return
                if not socket.is_output and row.kind == "output":
                    # An input aligned to the output before it: the row
                    # becomes the input's, keeping the output as partner.
                    rows[prev_socket_row] = dataclass_replace(
                        row,
                        kind="input",
                        socket=socket,
                        partner=row.socket,
                        height=input_height(socket),
                    )
                    _reflow(rows, prev_socket_row)
                    return
        if socket.is_output:
            prev_socket_row = add("output", SOCKET_ROW, socket=socket, depth=depth)
        else:
            prev_socket_row = add(
                "input", input_height(socket), socket=socket, depth=depth
            )

    def _reflow(rows: list[NodeRow], start: int) -> None:
        """Recompute row tops from *start* on, after a row was inserted or
        changed height."""
        nonlocal y
        top = -HEADER if start == 0 else rows[start - 1].top - rows[start - 1].height
        for k in range(start, len(rows)):
            rows[k] = dataclass_replace(rows[k], top=top)
            top -= rows[k].height
        y = -top

    def next_literal(side: list[str], sockets: list, after: int) -> int:
        """Index in *sockets* of the first table-listed socket at or after
        entry *after*: dynamic item blocks stop there."""
        for entry in order[after:]:
            if (
                entry[0] in ("in", "toggle")
                and side is literal_in
                or entry[0] == "out"
                and side is literal_out
            ):
                ident = entry[1]
            else:
                continue
            for k, s in enumerate(sockets):
                if s.identifier == ident:
                    return k
        return len(sockets)

    for index, entry in enumerate(order):
        kind = entry[0]
        if kind in ("in", "out"):
            socket = by_key.get((kind == "out", entry[1]))
            if socket is not None:
                place(socket, entry[2])
        elif kind == "toggle":
            socket = by_key.get((False, entry[1]))
            if socket is not None:
                placed.add(socket)
                header = closed_header()
                if last_panel_row is not None and header != last_panel_row:
                    # Drawn as a checkbox in the header of the panel just opened.
                    rows[last_panel_row] = dataclass_replace(
                        rows[last_panel_row], toggle=socket
                    )
                elif header is not None:
                    fold(socket, header)
            prev_socket_row = None
        elif kind == "items":
            _, has_in, has_out, aligned = entry
            stop_in = next_literal(literal_in, inputs, index + 1)
            stop_out = next_literal(literal_out, outputs, index + 1)
            block_in = [
                s
                for s in inputs[:stop_in]
                if s not in placed and s.identifier not in literal_in
            ]
            block_out = [
                s
                for s in outputs[:stop_out]
                if s not in placed and s.identifier not in literal_out
            ]
            if has_in:
                for socket in block_in:
                    place(socket, False)
                    if has_out:
                        match = next(
                            (o for o in block_out if o.identifier == socket.identifier),
                            None,
                        )
                        if match is not None:
                            place(match, aligned)
            if has_out:
                for socket in block_out:
                    if socket not in placed:
                        place(socket, False)
            prev_socket_row = None
        elif kind == "layout":
            if not layout_drawn and closed_header() is None:
                for prop, count in properties:
                    add("property", count * PROPERTY_ROW, prop=prop)
            layout_drawn = True
            prev_socket_row = None
        elif kind == "panel":
            _, name, default_closed = entry
            collapsed = default_closed
            if panel_index < len(panel_states):
                collapsed = panel_states[panel_index].is_collapsed
            panel_index += 1
            header = closed_header()
            if header is not None:
                # Inside a closed panel: no header of its own.
                stack.append((len(stack), header))
                last_panel_row = None
            else:
                row = add(
                    "panel",
                    SOCKET_ROW,
                    panel=name,
                    depth=len(stack),
                    open=not collapsed,
                )
                stack.append((len(stack), row if collapsed else None))
                last_panel_row = row
            prev_socket_row = None
        elif kind == "end":
            if stack:
                stack.pop()
            prev_socket_row = None

    # Buttons of a node whose declaration never placed them: after the
    # leading outputs, as conventional drawing does.
    if not layout_drawn and properties:
        insert_at = 0
        while insert_at < len(rows) and rows[insert_at].kind == "output":
            insert_at += 1
        for prop, count in properties:
            rows.insert(
                insert_at, NodeRow("property", 0.0, count * PROPERTY_ROW, prop=prop)
            )
            insert_at += 1
        _reflow(rows, 0)

    # Sockets the table does not know (a newer Blender): draw them last.
    for socket in (*outputs, *inputs):
        if socket not in placed:
            stack.clear()
            place(socket, False)
    return rows


def calculate_node_dimensions(
    node: bpy.types.Node,
    socket_input_connection_count: Counter | None = None,
    interface_scale: float = 1.0,
) -> tuple[float, float]:
    """Calculate the visual dimensions of a node.

    When a node is collapsed (``node.hide is True``) only linked sockets
    contribute to the height, and header / property / vector-expansion rows
    are omitted. Otherwise the height is the header plus every row of
    :func:`node_rows`. When ``socket_input_connection_count`` is None, link
    state is read directly from ``socket.is_linked``.
    """
    if node.hide:
        linked_inputs = sum(1 for s in node.inputs if s.enabled and s.is_linked)
        linked_outputs = sum(1 for s in node.outputs if s.enabled and s.is_linked)
        visible = max(linked_inputs, linked_outputs, 1)
        height = (HIDDEN_HEADER + visible * HIDDEN_SOCKET) * interface_scale
        return node.width, height

    rows = node_rows(node, socket_input_connection_count)
    height = (HEADER + sum(row.height for row in rows)) * interface_scale
    return node.width, height


def calculate_socket_offset_y(socket: bpy.types.NodeSocket) -> float:
    """Estimate a socket's vertical offset (<= 0) from the top of its node.

    Reads the row model of :func:`node_rows`: a socket sits on its own row's
    anchor, or on the header of the closed panel that hides it. Collapsed
    nodes spread their linked sockets evenly across the node's height.
    """
    node = socket.node
    assert node is not None

    if node.hide:
        side = node.outputs if socket.is_output else node.inputs
        visible = [s for s in side if s.enabled and s.is_linked]
        index = next((k for k, s in enumerate(visible) if s == socket), 0)
        height = calculate_node_dimensions(node)[1]
        return -height * (index + 0.5) / max(len(visible), 1)

    for row in node_rows(node):
        if socket in row.sockets:
            return row.anchor
    # Not drawn (hidden and unlinked, or in a closed panel): the header.
    return -HEADER / 2


def _socket_index(socket: bpy.types.NodeSocket) -> int:
    """Return the index of a socket among its node's visible sockets."""
    assert socket.node is not None
    collection = socket.node.inputs if not socket.is_output else socket.node.outputs
    idx = 0
    for s in collection:
        if s == socket:
            return idx
        if _socket_visible(s):
            idx += 1
    return idx  # pragma: no cover - socket not in its own node's collection


def _reduce_crossings(
    columns: list[list[bpy.types.Node]],
    tree: bpy.types.NodeTree,
    passes: int = 4,
) -> None:
    """Reorder nodes within columns to reduce edge crossings.

    Uses the barycenter heuristic with socket-level precision: for each node
    compute its weight from the position of the sockets it connects to in the
    adjacent column, then sort by that weight.  This correctly distinguishes
    nodes that connect to different sockets on the same target.

    Alternating forward and backward sweeps iteratively improve the ordering.
    """
    if len(columns) < 2:
        return

    layoutable = {n for col in columns for n in col}
    col_of = {n: ci for ci, col in enumerate(columns) for n in col}

    # Pre-compute per-node link weights towards each adjacent column direction.
    # For a forward sweep (fixing col i, sorting col i+1), a node in col i+1
    # cares about its connections INTO col i.  The weight of each connection is
    # the position of the *node* in the fixed column plus a fractional offset
    # derived from the socket index, so that multiple links to the same node
    # produce distinct, correctly ordered weights.
    #
    # We store raw (neighbour_node, socket_fraction) pairs per node per
    # direction and resolve them during each sweep once column order is known.

    # link records: for each layoutable node, collect tuples of
    #   (neighbour_node, socket_fraction)
    # keyed by which side the neighbour is on (left or right).
    left_links: dict[bpy.types.Node, list[tuple[bpy.types.Node, float]]] = {
        n: [] for n in layoutable
    }
    right_links: dict[bpy.types.Node, list[tuple[bpy.types.Node, float]]] = {
        n: [] for n in layoutable
    }

    for link in tree.links:
        src, dst = link.from_node, link.to_node
        if src not in layoutable or dst not in layoutable:
            continue
        src_col, dst_col = col_of[src], col_of[dst]
        if src_col >= dst_col:  # pragma: no cover - Blender forbids link cycles
            continue  # only consider forward edges

        # Weight based on socket position on the neighbour node.
        # For a node in the right column looking left: the relevant socket is
        # on the source node (output side).
        # For a node in the left column looking right: the relevant socket is
        # on the target node (input side).
        out_count = max(1, sum(1 for s in src.outputs if s.enabled))
        in_count = max(1, sum(1 for s in dst.inputs if s.enabled))
        assert link.from_socket is not None and link.to_socket is not None
        src_frac = _socket_index(link.from_socket) / out_count
        dst_frac = _socket_index(link.to_socket) / in_count

        # dst looks left towards src: weight by src's output socket position
        left_links[dst].append((src, src_frac))
        # src looks right towards dst: weight by dst's input socket position
        right_links[src].append((dst, dst_frac))

    for iteration in range(passes):
        if iteration % 2 == 0:
            # forward sweep: fix column i, sort column i+1
            col_range = range(1, len(columns))
        else:
            # backward sweep: fix column i, sort column i-1
            col_range = range(len(columns) - 2, -1, -1)

        for ci in col_range:
            if iteration % 2 == 0:
                fixed_col = columns[ci - 1]
                links_map = left_links
            else:
                fixed_col = columns[ci + 1]
                links_map = right_links

            pos_in_fixed = {node: idx for idx, node in enumerate(fixed_col)}
            original_pos = {node: float(idx) for idx, node in enumerate(columns[ci])}

            barycenters: dict[bpy.types.Node, float] = {}
            for node in columns[ci]:
                weights = [
                    pos_in_fixed[nb] + frac
                    for nb, frac in links_map[node]
                    if nb in pos_in_fixed
                ]
                if weights:
                    barycenters[node] = sum(weights) / len(weights)
                else:
                    barycenters[node] = original_pos[node]

            columns[ci].sort(key=lambda n: barycenters[n])


def position_nodes_in_columns(
    columns: list[list[bpy.types.Node]],
    connection_counts: Counter,
    spacing: tuple[float, float] = (50, 25),
) -> None:
    """Position nodes column-by-column with the given spacing.

    Consecutive collapsed nodes are stacked tightly (with minimal gap) to
    keep related math/converter chains visually grouped together.
    """
    COLLAPSED_GAP = 4

    x = 0.0
    for column in columns:
        col_width = 0.0
        y = 0.0
        prev_hidden = False

        for node in column:
            node.update()

            width, height = calculate_node_dimensions(node, connection_counts, 1.0)

            col_width = max(col_width, width)

            node.location = (x, y)

            # use tight spacing between consecutive collapsed nodes
            if node.hide and prev_hidden:
                y -= height + COLLAPSED_GAP
            else:
                y -= height + spacing[1]

            prev_hidden = node.hide

        x += col_width + spacing[0]


def position_reroutes(tree: bpy.types.NodeTree) -> None:
    """Place reroute nodes midway between their source and target."""
    for node in tree.nodes:
        if node.bl_idname != "NodeReroute":
            continue

        sources: list[bpy.types.Node] = []
        targets: list[bpy.types.Node] = []
        for link in tree.links:
            if link.to_node == node:
                assert link.from_node is not None
                sources.append(link.from_node)
            if link.from_node == node:
                assert link.to_node is not None
                targets.append(link.to_node)

        neighbours = sources + targets
        if not neighbours:
            continue

        avg_x = sum(n.location.x for n in neighbours) / len(neighbours)
        avg_y = sum(n.location.y for n in neighbours) / len(neighbours)
        node.location = (avg_x, avg_y)


def arrange_tree(
    tree: bpy.types.NodeTree,
    spacing: tuple[float, float] = (50, 25),
) -> None:
    """Arrange nodes in a node tree based on their dependencies.

    Organises layoutable nodes into columns from left to right and positions
    reroute nodes between their neighbours.  Frame nodes are left untouched.
    """
    if not tree.nodes:
        return

    dependency_graph, connection_counts = build_dependency_graph(tree)

    if not dependency_graph:
        return

    nodes_in_order = topological_sort(dependency_graph)
    columns = organize_into_columns(nodes_in_order, dependency_graph)
    _reduce_crossings(columns, tree)
    position_nodes_in_columns(columns, connection_counts, spacing)
    position_reroutes(tree)


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
        Which directions nodes may be moved in during layout.
    socket_alignment : str
        How aggressively links are straightened by aligning the sockets
        they connect.
    add_reroutes : bool
        Insert reroute nodes to route long edges around nodes. Off by
        default: added reroutes are real nodes, which would change the
        authored structure of generated trees (node counts, round-trips,
        diagrams).
    keep_reroutes_outside_frames : bool
        Do not place added reroutes inside frames.
    stack_collapsed : bool
        Stack consecutive collapsed nodes tightly.
    stack_margin_y_fac : float
        Fraction of the vertical margin used between stacked collapsed
        nodes.
    optimize_sizes : bool
        Fit the widths of collapsed nodes to their display name.
    iterations : int
        Number of crossing-minimization iterations.
    """

    # Defaults calibrated against hand-approved node-arrange addon output
    # ("30" x/y spacing, no socket alignment, top-right node alignment).
    margin: tuple[float, float] = (30.0, 30.0)
    direction: Literal["LEFT_DOWN", "RIGHT_DOWN", "BALANCED", "LEFT_UP", "RIGHT_UP"] = (
        "RIGHT_UP"
    )
    socket_alignment: Literal["NONE", "MODERATE", "FULL"] = "NONE"
    add_reroutes: bool = False
    keep_reroutes_outside_frames: bool = False
    stack_collapsed: bool = True
    stack_margin_y_fac: float = 0.5
    optimize_sizes: bool = False
    iterations: int = 50


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


def _arrange_sugiyama(tree: bpy.types.NodeTree, options: SugiyamaOptions) -> None:
    from mathutils import Vector

    from ..lib.nodearrange.arrange import sugiyama
    from ..lib.nodearrange.config import Settings

    settings = Settings(
        iterations=options.iterations,
        direction=options.direction,
        socket_alignment=options.socket_alignment,
        add_reroutes=options.add_reroutes,
        keep_reroutes_outside_frames=options.keep_reroutes_outside_frames,
        stack_collapsed=options.stack_collapsed,
        optimize_sizes=options.optimize_sizes,
        stack_margin_y_fac=options.stack_margin_y_fac,
    )
    sugiyama.sugiyama_layout(tree, settings=settings, margin=Vector(options.margin))


def arrange(
    tree: bpy.types.NodeTree,
    method: ArrangeMethod = "sugiyama",
) -> None:
    """Arrange the nodes of a tree.

    ``method`` selects the algorithm: ``"sugiyama"`` (or a
    :class:`SugiyamaOptions` instance for tuned settings), ``"simple"`` (or a
    :class:`SimpleOptions` instance), or None to leave the tree untouched.

    The Sugiyama layout requires the optional ``networkx`` dependency; when
    it is missing, the simple arrangement is used instead (with a warning).
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
        try:
            _arrange_sugiyama(tree, options)
        except ImportError as e:
            if "networkx" not in str(e):
                raise
            warnings.warn(
                "networkx is not installed, falling back to simple arrangement. "
                "Install networkx for the Sugiyama layout: pip install nodebpy[networkx]",
                stacklevel=2,
            )
            arrange_tree(tree)

    # Quantize to the precision node positions are dumped with, so arranged
    # trees round-trip losslessly (and sub-0.01 UI units carry no meaning).
    for node in tree.nodes:
        location = node.location
        node.location = (round(location.x, 2), round(location.y, 2))
