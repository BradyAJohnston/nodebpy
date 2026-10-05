"""How tall a node is and where its sockets sit, worked out from the rows it
draws. Blender only measures nodes when a node editor draws them, which
never happens under the ``bpy`` module, so the layout estimates instead."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from dataclasses import replace as dataclass_replace
from typing import Any, Literal, cast

import bpy

from ..builder._socket_order import SOCKET_ORDER
from .dna import REROUTE_SIZE

# Estimated row heights (in unscaled UI units) used to model node layout
# without a UI. Blender only computes real node/socket geometry when a node
# editor draws the tree, which never happens under the headless ``bpy``
# module. HEADER and SOCKET_ROW are calibrated against a UI-arranged tree
# whose reroutes the arranger had socket-aligned: reroute y minus node top
# measures the real socket offsets, giving header + (i + 0.5) * row fits of
# 24.5 / 21.75. The remaining rows scale to the same grid.
HEADER = 24.5
SOCKET_ROW = 21.75
COLLAPSED_SOCKET = 10  # NODE_DY / 2
COLLAPSED_ENDS = 8  # 2 * BASIS_RAD
PROPERTY_ROW = 24
VECTOR_EXPANDED = 65.25  # three extra value rows


# Node-specific RNA properties Blender never draws in the node body: UI
# bookkeeping for item lists and zones rather than options.
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


def _socket_visible(socket: bpy.types.NodeSocket) -> bool:
    """Whether Blender draws this socket on an expanded node: enabled, and
    not hidden — a hidden socket reappears while it is linked (the editor's
    Hide Unused Sockets only hides unlinked ones)."""
    return socket.enabled and (not socket.hide or socket.is_linked)


def _is_expanded_vector(
    socket: bpy.types.NodeSocket,
    socket_input_connection_count: Counter[bpy.types.NodeSocket | None] | None,
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
    socket_input_connection_count: Counter[bpy.types.NodeSocket | None] | None = None,
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
    socket_input_connection_count: Counter[bpy.types.NodeSocket | None] | None,
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


def _collapsed_height(node: bpy.types.Node) -> float:
    """Height of a collapsed node: a row per visible socket on its fuller
    side, at least two (``node_update_collapsed`` in ``node_draw.cc``)."""
    inputs = sum(_socket_visible(s) for s in node.inputs)
    outputs = sum(_socket_visible(s) for s in node.outputs)
    return COLLAPSED_SOCKET * max(inputs, outputs, 2) + COLLAPSED_ENDS


def calculate_node_dimensions(
    node: bpy.types.Node,
    socket_input_connection_count: Counter[bpy.types.NodeSocket | None] | None = None,
    interface_scale: float = 1.0,
) -> tuple[float, float]:
    """Calculate the visual dimensions of a node.

    A collapsed node has a row per visible socket; otherwise the height is
    the header plus every row of :func:`node_rows`. When
    ``socket_input_connection_count`` is None, link
    state is read directly from ``socket.is_linked``.
    """
    if node.hide:
        return node.width, _collapsed_height(node) * interface_scale

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
        visible = [s for s in side if _socket_visible(s)]
        index = next((k for k, s in enumerate(visible) if s == socket), 0)
        middle = -_collapsed_height(node) / 2
        return middle + COLLAPSED_SOCKET * ((len(visible) - 1) / 2 - index)

    for row in node_rows(node):
        if socket in row.sockets:
            return row.anchor
    # Not drawn (hidden and unlinked, or in a closed panel): the header.
    return -HEADER / 2


def dimensions(node: bpy.types.Node) -> tuple[float, float]:
    """Width and height of the box *node* is drawn in: what Blender measured
    when a node editor last drew it, else the estimate."""
    if node.bl_idname == "NodeReroute":
        return (REROUTE_SIZE, REROUTE_SIZE)

    drawn = node.dimensions
    if drawn.x > 0 and drawn.y > 0:  # pragma: no cover - only drawn in a UI
        # Drawn sizes are in view space; locations are not.
        preferences = bpy.context.preferences
        assert preferences is not None
        scale = preferences.system.ui_scale
        return (drawn.x / scale, drawn.y / scale)
    return calculate_node_dimensions(node)


# A collapsed node is drawn around a point this far below its location.
_COLLAPSED_OFFSET = 10


def get_top(node: bpy.types.Node) -> float:
    """The y of the top edge of the box *node* is drawn in."""
    y = node.location_absolute.y
    if node.hide:
        return y - _COLLAPSED_OFFSET + dimensions(node)[1] / 2
    return y


def get_bottom(node: bpy.types.Node) -> float:
    """The y of the bottom edge of the box *node* is drawn in."""
    return get_top(node) - dimensions(node)[1]
