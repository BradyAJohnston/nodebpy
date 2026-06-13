# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate Python code from a Blender node tree using nodebpy.

The generator walks the tree in topological order and builds a small
expression IR for each node, then renders statements. Three behaviours make
the output read like hand-written nodebpy code:

* **Inlining** — a node whose output is consumed exactly once is embedded in
  its consumer's expression instead of being assigned to a variable.
* **Chain stitching** — runs of geometry/shader links through first sockets
  are rendered with the ``>>`` operator.
* **Operator lifting** — Math/VectorMath/IntegerMath/BooleanMath nodes whose
  operation has a Python operator equivalent are rendered as ``a + b`` style
  expressions, mirroring nodebpy's operator overloads.

Nodes that need bespoke treatment (zones, dynamic-socket nodes, …) can
register a custom emitter with :func:`register_emitter`.
"""

from __future__ import annotations

import ast
import heapq
import inspect
import keyword
import re
import textwrap
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, NamedTuple

from bpy.types import NodeTree

if TYPE_CHECKING:
    from ..builder.tree import TreeBuilder


class CodegenError(Exception):
    """Raised when a node tree cannot be faithfully expressed as code."""


# ---------------------------------------------------------------------------
# Expression IR
#
# Strings are only produced in render(); parenthesisation is decided from
# Python operator precedence, so emitters can compose expressions freely.
# ---------------------------------------------------------------------------

_ATOM_PREC = 100
_UNARY_PREC = 11

_BINOP_PREC: dict[str, int] = {
    "|": 5,
    "^": 6,
    "&": 7,
    ">>": 8,
    "+": 9,
    "-": 9,
    "*": 10,
    "/": 10,
    "//": 10,
    "%": 10,
    "@": 10,
    "**": 12,
}

_RIGHT_ASSOC = frozenset({"**"})


class Expr:
    """Base class for renderable expressions."""

    prec: int = _ATOM_PREC

    def render(self) -> str:
        raise NotImplementedError

    @staticmethod
    def _child(child: "Expr", parens: bool) -> str:
        text = child.render()
        return f"({text})" if parens else text


@dataclass
class Raw(Expr):
    """Verbatim source text (escape hatch for custom emitters)."""

    text: str

    def render(self) -> str:
        return self.text


@dataclass
class Lit(Expr):
    """A Python literal, formatted via :func:`_fmt`."""

    value: Any

    def render(self) -> str:
        return _fmt(self.value)


@dataclass
class Ref(Expr):
    """A variable reference."""

    name: str

    def render(self) -> str:
        return self.name


@dataclass
class Attr(Expr):
    """Attribute access; ``name`` may be dotted (e.g. ``"o.color"``)."""

    base: Expr
    name: str

    def render(self) -> str:
        return f"{self._child(self.base, self.base.prec < _ATOM_PREC)}.{self.name}"


@dataclass
class Call(Expr):
    """A call ``func(args, kwargs)``; ``func`` is rendered verbatim."""

    func: str
    args: list[Expr] = field(default_factory=list)
    kwargs: dict[str, Expr] = field(default_factory=dict)

    def render(self) -> str:
        parts = [a.render() for a in self.args]
        parts += [f"{k}={v.render()}" for k, v in self.kwargs.items()]
        return f"{self.func}({', '.join(parts)})"


@dataclass
class TupleExpr(Expr):
    """A tuple literal, used for multi-input sockets (e.g. JoinGeometry)."""

    items: list[Expr]

    def render(self) -> str:
        rendered = [item.render() for item in self.items]
        if len(rendered) == 1:
            return f"({rendered[0]},)"
        return f"({', '.join(rendered)})"


@dataclass
class DictExpr(Expr):
    """A dict literal with string keys, used for ``items=`` kwargs."""

    items: dict[str, Expr]

    def render(self) -> str:
        inner = ", ".join(f"{_fmt(k)}: {v.render()}" for k, v in self.items.items())
        return "{" + inner + "}"


@dataclass
class GroupCall(Expr):
    """``ClassName(**{"Socket Name": value, ...})`` for a generated group class.

    Socket names are passed through a dict because they need not be valid
    Python identifiers (``"Box Object"``); ``_establish_links`` matches them
    by socket name.
    """

    func: str
    items: dict[str, Expr]

    def render(self) -> str:
        if not self.items:
            return f"{self.func}()"
        inner = ", ".join(f"{_fmt(k)}: {v.render()}" for k, v in self.items.items())
        return f"{self.func}(**{{{inner}}})"


@dataclass
class MethodCall(Expr):
    """A method call on a receiver expression, e.g. ``value.point.at(i)``.

    ``method`` may be a dotted path (``"switch.float"``, ``"point.mean"``).
    """

    receiver: Expr
    method: str
    args: list[Expr] = field(default_factory=list)
    kwargs: dict[str, Expr] = field(default_factory=dict)

    def render(self) -> str:
        base = self._child(self.receiver, self.receiver.prec < _ATOM_PREC)
        parts = [a.render() for a in self.args]
        parts += [f"{k}={v.render()}" for k, v in self.kwargs.items()]
        return f"{base}.{self.method}({', '.join(parts)})"


@dataclass
class UnaryOp(Expr):
    """A prefix unary operator (``-x``, ``~x``)."""

    op: str
    operand: Expr

    prec: int = field(default=_UNARY_PREC, init=False)

    def render(self) -> str:
        return f"{self.op}{self._child(self.operand, self.operand.prec < self.prec)}"


_COMPARE_PREC = 4  # below every binary operator


@dataclass
class CompareOp(Expr):
    """A comparison expression (``a < b``).

    Comparison operands are always parenthesised — Python would chain
    ``a < b < c``, which is not what nested Compare nodes mean — and
    comparisons bind looser than every binary operator, so they get parens
    inside ``&``/``|``/``>>`` expressions automatically.
    """

    op: str
    lhs: Expr
    rhs: Expr

    prec: int = field(default=_COMPARE_PREC, init=False)

    def render(self) -> str:
        lhs = self._child(self.lhs, self.lhs.prec <= self.prec)
        rhs = self._child(self.rhs, self.rhs.prec <= self.prec)
        return f"{lhs} {self.op} {rhs}"


@dataclass
class BinOp(Expr):
    """A binary operator expression with precedence-aware rendering.

    Equal-precedence right operands are always parenthesised so the rendered
    code rebuilds the same node-graph grouping on round-trip.
    """

    op: str
    lhs: Expr
    rhs: Expr

    def __post_init__(self) -> None:
        self.prec = _BINOP_PREC[self.op]

    def render(self) -> str:
        right_assoc = self.op in _RIGHT_ASSOC
        lhs_parens = self.lhs.prec < self.prec or (
            self.lhs.prec == self.prec and right_assoc
        )
        rhs_parens = self.rhs.prec < self.prec or (
            self.rhs.prec == self.prec and not right_assoc
        )
        lhs = self._child(self.lhs, lhs_parens)
        rhs = self._child(self.rhs, rhs_parens)
        return f"{lhs} {self.op} {rhs}"


_MAX_LINE_WIDTH = 88


def _stmt_lines(
    expr: Expr,
    assign: str | None = None,
    indent: str = "    ",
    width: int = _MAX_LINE_WIDTH,
) -> list[str]:
    """Render a statement, wrapping a top-level ``>>`` chain in parentheses
    with one segment per line when the flat form exceeds ``width`` columns."""
    prefix = f"{assign} = " if assign else ""
    flat = f"{indent}{prefix}{expr.render()}"
    if len(flat) <= width or not (isinstance(expr, BinOp) and expr.op == ">>"):
        return [flat]
    segments: list[Expr] = []
    node: Expr = expr
    while isinstance(node, BinOp) and node.op == ">>":
        segments.append(node.rhs)
        node = node.lhs
    segments.append(node)
    segments.reverse()
    prec = _BINOP_PREC[">>"]
    inner = indent + "    "
    head = segments[0]
    lines = [f"{indent}{prefix}(", f"{inner}{Expr._child(head, head.prec < prec)}"]
    lines.extend(
        f"{inner}>> {Expr._child(seg, seg.prec <= prec)}" for seg in segments[1:]
    )
    lines.append(f"{indent})")
    return lines


# ---------------------------------------------------------------------------
# Value formatting
# ---------------------------------------------------------------------------


def _fmt_float(value: float) -> str:
    """Shortest literal that round-trips through float32.

    Blender stores socket values as float32, so reading them back through
    Python gives noisy float64 reprs (``0.10000000149011612``); the
    shortest decimal that uniquely identifies the float32 (``0.1``)
    rebuilds the identical socket value.
    """
    import math

    if not math.isfinite(value):
        return repr(value)
    try:
        import numpy as np
    except ImportError:  # pragma: no cover - Blender ships numpy
        return repr(value)
    f32 = np.float32(value)
    if float(f32) != value:
        return repr(value)  # genuine float64 — keep full precision
    return np.format_float_positional(f32, unique=True, trim="0")


def _fmt(value: Any) -> str:
    """Format a value as a Python literal using double-quoted strings."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _fmt_float(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    # Vectors / sequences
    try:
        items = list(value)
        return f"({', '.join(_fmt(v) for v in items)})"
    except TypeError:
        return repr(value)


def _eq(a: Any, b: Any) -> bool:
    """Compare two values for equality, handling vectors/sequences."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    try:
        if isinstance(a, str) and isinstance(b, str):
            return a == b
        if hasattr(a, "__len__") and hasattr(b, "__len__"):
            if len(a) != len(b):
                return False
            return all(_eq(x, y) for x, y in zip(a, b))
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return float(a) == float(b)
        return a == b
    except Exception:
        return False


def _is_zero(val: Any) -> bool:
    """Return True if val is a zero-like default."""
    if isinstance(val, bool):
        return not val
    if isinstance(val, (int, float)):
        return val == 0
    try:
        return all(_is_zero(v) for v in val)
    except TypeError:
        return False


# ---------------------------------------------------------------------------
# Node registry — bl_idname → (module_alias, node class)
# ---------------------------------------------------------------------------

_NODE_REGISTRY: dict[str, tuple[str, type]] | None = None

_ALIAS_MODULES = {"g": "geometry", "s": "shader", "c": "compositor"}

_TREE_CONSTRUCTORS = {
    "GeometryNodeTree": "TreeBuilder",
    "ShaderNodeTree": "TreeBuilder.shader",
    "CompositorNodeTree": "TreeBuilder.compositor",
}

_TREE_ALIAS = {
    "GeometryNodeTree": "g",
    "ShaderNodeTree": "s",
    "CompositorNodeTree": "c",
}

_SKIP_BL_IDNAMES = frozenset(
    {"NodeGroupInput", "NodeGroupOutput", "NodeReroute", "NodeFrame"}
)

_INTERFACE_TYPE_METHOD: dict[str, str] = {
    "NodeSocketFloat": "float",
    "NodeSocketInt": "integer",
    "NodeSocketBool": "boolean",
    "NodeSocketVector": "vector",
    "NodeSocketColor": "color",
    "NodeSocketRotation": "rotation",
    "NodeSocketMatrix": "matrix",
    "NodeSocketString": "string",
    "NodeSocketMenu": "menu",
    "NodeSocketObject": "object",
    "NodeSocketGeometry": "geometry",
    "NodeSocketCollection": "collection",
    "NodeSocketImage": "image",
    "NodeSocketMaterial": "material",
    "NodeSocketBundle": "bundle",
    "NodeSocketClosure": "closure",
    "NodeSocketShader": "shader",
}

_NO_DEFAULT_VALUE_TYPES = frozenset(
    {
        "NodeSocketGeometry",
        "NodeSocketObject",
        "NodeSocketCollection",
        "NodeSocketImage",
        "NodeSocketMaterial",
        "NodeSocketBundle",
        "NodeSocketClosure",
        "NodeSocketShader",
    }
)


def _all_subclasses(cls: type):
    for sub in cls.__subclasses__():
        yield sub
        yield from _all_subclasses(sub)


def _get_node_registry() -> dict[str, tuple[str, type]]:
    """Lazily build and return the bl_idname → (alias, class) registry."""
    global _NODE_REGISTRY
    if _NODE_REGISTRY is not None:
        return _NODE_REGISTRY
    _NODE_REGISTRY = {}
    from ..builder.node import BaseNode
    from ..nodes import compositor, geometry, shader

    domains = [
        ("g", geometry.__name__),
        ("s", shader.__name__),
        ("c", compositor.__name__),
    ]
    # Group bl_idnames are shared by every group/custom-group class, so a
    # single registry entry would be arbitrary (and emit the wrong class).
    ambiguous = {"GeometryNodeGroup", "ShaderNodeGroup", "CompositorNodeGroup"}
    for cls in _all_subclasses(BaseNode):
        bl_id = getattr(cls, "_bl_idname", None)
        if not bl_id or bl_id in ambiguous or bl_id in _NODE_REGISTRY:
            continue
        for alias, prefix in domains:
            if cls.__module__.startswith(prefix):
                _NODE_REGISTRY[bl_id] = (alias, cls)
                break
    return _NODE_REGISTRY


def _find_cls(bl_idname: str) -> tuple[str, type] | None:
    """Return (alias, class) for a bl_idname, or None."""
    return _get_node_registry().get(bl_idname)


# ---------------------------------------------------------------------------
# Blender socket defaults — probed on a scratch tree, never the user's tree
# ---------------------------------------------------------------------------

_BLENDER_SOCKET_DEFAULTS: dict[tuple[str, str], dict[str, object]] = {}


def _get_blender_socket_defaults(tree_idname: str, bl_idname: str) -> dict[str, object]:
    """Socket identifier → default value for a freshly created node of this type."""
    key = (tree_idname, bl_idname)
    if key in _BLENDER_SOCKET_DEFAULTS:
        return _BLENDER_SOCKET_DEFAULTS[key]
    defaults: dict[str, object] = {}
    try:
        import bpy

        probe_tree = bpy.data.node_groups.new("__nodebpy_codegen_probe__", tree_idname)
        try:
            node = probe_tree.nodes.new(bl_idname)
            for s in node.inputs:
                if not hasattr(s, "default_value"):
                    continue
                val = s.default_value
                try:
                    defaults[s.identifier] = tuple(val)
                except TypeError:
                    defaults[s.identifier] = val
        finally:
            bpy.data.node_groups.remove(probe_tree)
    except Exception:
        pass
    _BLENDER_SOCKET_DEFAULTS[key] = defaults
    return defaults


_IFACE_DEFAULTS: dict[tuple[str, str], dict[str, object]] = {}


def _get_interface_defaults(tree_idname: str, socket_type: str) -> dict[str, object]:
    """Property identifier → value for a freshly created interface socket."""
    key = (tree_idname, socket_type)
    if key in _IFACE_DEFAULTS:
        return _IFACE_DEFAULTS[key]
    defaults: dict[str, object] = {}
    try:
        import bpy

        probe_tree = bpy.data.node_groups.new("__nodebpy_codegen_probe__", tree_idname)
        try:
            socket = probe_tree.interface.new_socket(
                "probe", in_out="INPUT", socket_type=socket_type
            )
            for prop in socket.bl_rna.properties:
                if prop.is_readonly:
                    continue
                try:
                    value = getattr(socket, prop.identifier)
                except Exception:
                    continue
                if not isinstance(value, str):
                    try:
                        value = tuple(value)
                    except TypeError:
                        pass
                defaults[prop.identifier] = value
        finally:
            bpy.data.node_groups.remove(probe_tree)
    except Exception:
        pass
    _IFACE_DEFAULTS[key] = defaults
    return defaults


# ---------------------------------------------------------------------------
# Name utilities
# ---------------------------------------------------------------------------


def _normalize(name: str) -> str:
    from ..builder._utils import normalize_name

    return normalize_name(name)


def _make_var(label: str, counter: dict[str, int]) -> str:
    """Return a unique snake_case variable name for a node label."""
    base = re.sub(r"_+", "_", re.sub(r"\W", "_", _normalize(label))).strip("_")
    if not base or base[0].isdigit():
        base = f"n_{base}" if base else "node"
    if keyword.iskeyword(base):
        base = f"{base}_"
    if base not in counter:
        counter[base] = 0
        return base
    counter[base] += 1
    return f"{base}_{counter[base]}"


# ---------------------------------------------------------------------------
# Graph utilities
# ---------------------------------------------------------------------------


class _Link(NamedTuple):
    """A node-tree link with any reroute chain collapsed away."""

    from_node: Any
    from_socket: Any
    to_node: Any
    to_socket: Any
    sort_id: int = 0  # multi_input_sort_id; later-created links get higher ids


def _trace_reroute(node, socket, node_tree):
    """Follow a reroute chain backward to the real source node and socket."""
    visited = set()
    while node.bl_idname == "NodeReroute" and node.name not in visited:
        visited.add(node.name)
        upstream = [link for link in node_tree.links if link.to_node.name == node.name]
        if not upstream:
            break
        node = upstream[0].from_node
        socket = upstream[0].from_socket
    return node, socket


def _canonical_links(node_tree, links: list[_Link]) -> list[_Link]:
    """Sort links structurally so emission never depends on insertion order.

    bpy's links collection preserves creation order, which can differ
    between runs for structurally identical trees (the arrange pass inserts
    reroute links in set-iteration order). Sorting by node creation order
    and socket position makes ``to_python`` a pure function of the tree's
    structure.
    """
    node_idx = {n.name: i for i, n in enumerate(node_tree.nodes)}

    def socket_idx(sockets, socket) -> int:
        for i, s in enumerate(sockets):
            if s.identifier == socket.identifier:
                return i
        return -1

    return sorted(
        links,
        key=lambda link: (
            node_idx.get(link.to_node.name, -1),
            socket_idx(link.to_node.inputs, link.to_socket),
            -link.sort_id,  # multi-input: creation order, as emitted
            node_idx.get(link.from_node.name, -1),
            socket_idx(link.from_node.outputs, link.from_socket),
        ),
    )


def _effective_links(node_tree) -> list[_Link]:
    """All links with reroutes collapsed; reroute-internal segments dropped.

    Returned in canonical (structural) order — see :func:`_canonical_links`.
    """
    links: list[_Link] = []
    for link in node_tree.links:
        if link.to_node.bl_idname == "NodeReroute":
            continue
        from_node, from_socket = _trace_reroute(
            link.from_node, link.from_socket, node_tree
        )
        if from_node.bl_idname == "NodeReroute":
            continue  # dangling reroute with no real source
        links.append(
            _Link(
                from_node,
                from_socket,
                link.to_node,
                link.to_socket,
                getattr(link, "multi_input_sort_id", 0),
            )
        )
    return _canonical_links(node_tree, links)


def _ordering_edges(node_tree):
    """(from, to) node pairs that must hold in emission order: effective
    links (canonical order, reroutes collapsed) plus a synthetic edge from
    each zone input node to its paired output, so the zone wrapper is
    declared before the output side is emitted."""
    for link in _effective_links(node_tree):
        if link.from_node != link.to_node:
            yield link.from_node, link.to_node
    for node in node_tree.nodes:
        paired = getattr(node, "paired_output", None)
        if paired is not None:
            yield node, paired


def _topo_sort(node_tree) -> list:
    """Return nodes in topological order (dependencies first)."""
    try:
        import networkx as nx

        G: nx.DiGraph = nx.DiGraph()
        for node in node_tree.nodes:
            G.add_node(node)
        for from_node, to_node in _ordering_edges(node_tree):
            G.add_edge(from_node, to_node)
        return list(nx.topological_sort(G))
    except ImportError:
        pass

    from collections import deque

    nodes = list(node_tree.nodes)
    node_by_name = {n.name: n for n in nodes}
    in_deg: dict[str, int] = {n.name: 0 for n in nodes}
    adj: dict[str, list[str]] = {n.name: [] for n in nodes}
    for from_node, to_node in _ordering_edges(node_tree):
        fn, tn = from_node.name, to_node.name
        adj[fn].append(tn)
        in_deg[tn] += 1
    queue: deque = deque(n for n in nodes if in_deg[n.name] == 0)
    order = []
    while queue:
        n = queue.popleft()
        order.append(n)
        for m_name in adj[n.name]:
            in_deg[m_name] -= 1
            if in_deg[m_name] == 0:
                queue.append(node_by_name[m_name])
    return order


def _frame_key(node) -> str | None:
    """The frame a node's statement should be emitted under, or None."""
    parent = node.parent
    if parent is None or parent.bl_idname != "NodeFrame":
        return None
    if parent.parent is not None:
        return None  # nested frames are not expressible as with-blocks
    return parent.name


def _frame_order(node_tree, ordered):
    """Reorder ``ordered`` so each emittable frame's members are contiguous.

    Frames become clusters in a cluster-level topological sort (each `with
    g.Frame():` block creates one frame, so members must emit together).
    A frame whose cluster sits on a cycle through outside nodes cannot be
    contiguous — it falls back to flat, frameless emission.

    Returns ``(order, frame_of, frame_nodes)``: the new node order, node
    name → frame key (or None), and frame key → bpy frame node.
    """
    frame_of = {n.name: _frame_key(n) for n in ordered}
    frame_nodes: dict[str, Any] = {}
    for n in ordered:
        key = frame_of[n.name]
        if key is not None:
            frame_nodes[key] = n.parent
    if not frame_nodes:
        return ordered, frame_of, frame_nodes

    in_order = {n.name for n in ordered}
    edges = [
        (a.name, b.name)
        for a, b in _ordering_edges(node_tree)
        if a.name in in_order and b.name in in_order
    ]
    while True:
        key_of = {n.name: frame_of[n.name] or f"__{n.name}" for n in ordered}
        clusters: dict[str, list] = {}
        order_keys: list[str] = []
        for n in ordered:
            key = key_of[n.name]
            if key not in clusters:
                clusters[key] = []
                order_keys.append(key)
            clusters[key].append(n)
        adj: dict[str, set[str]] = {k: set() for k in order_keys}
        in_deg = dict.fromkeys(order_keys, 0)
        for a, b in edges:
            ka, kb = key_of[a], key_of[b]
            if ka != kb and kb not in adj[ka]:
                adj[ka].add(kb)
                in_deg[kb] += 1

        # Kahn's algorithm preferring first-appearance order, so the
        # emission order stays close to the plain topological sort.
        pos = {k: i for i, k in enumerate(order_keys)}
        heap = [pos[k] for k in order_keys if in_deg[k] == 0]
        heapq.heapify(heap)
        result: list[str] = []
        while heap:
            k = order_keys[heapq.heappop(heap)]
            result.append(k)
            for m in adj[k]:
                in_deg[m] -= 1
                if in_deg[m] == 0:
                    heapq.heappush(heap, pos[m])
        if len(result) == len(order_keys):
            order = [n for k in result for n in clusters[k]]
            return order, frame_of, frame_nodes

        # Contract-induced cycle: flatten the first still-blocked frame
        # and retry (node graphs themselves are acyclic, so every cycle
        # runs through at least one frame cluster).
        stuck = next(
            (k for k in order_keys if in_deg[k] > 0 and k in frame_nodes), None
        )
        if stuck is None:  # pragma: no cover - defensive
            return ordered, dict.fromkeys(frame_of, None), {}
        del frame_nodes[stuck]
        for name, key in frame_of.items():
            if key == stuck:
                frame_of[name] = None


# ---------------------------------------------------------------------------
# Emission context
# ---------------------------------------------------------------------------


@dataclass
class _Val:
    """What a node's generated expression evaluates to.

    ``expr`` is the expression itself; ``is_socket`` distinguishes Socket
    values (interface refs, lifted operators, socket-method results) from
    node objects (constructor/factory calls). ``socket_id`` pins the
    expression to one specific output. ``outputs`` dissolves the node
    entirely into per-output expressions (e.g. SeparateXYZ → ``vec.x``).
    """

    expr: Expr | None
    is_socket: bool = False
    socket_id: str | None = None
    outputs: dict[str, Expr] | None = None

    def require_expr(self) -> Expr:
        if self.expr is None:  # pragma: no cover - dissolved vals bind earlier
            raise CodegenError(
                "Value was dissolved into per-output accessors and has no "
                "single expression"
            )
        return self.expr


@dataclass
class EmitContext:
    """State shared across node emission; also the API for custom emitters."""

    node_tree: Any
    links: list[_Link]
    incoming: dict[str, list[_Link]]
    outgoing: dict[str, list[_Link]]
    var_map: dict[str, _Val] = field(default_factory=dict)
    counter: dict[str, int] = field(default_factory=dict)
    used_aliases: set[str] = field(default_factory=set)
    pending_lines: list[str] = field(default_factory=list)
    zones: dict[str, "_ZoneState"] = field(default_factory=dict)
    collector: "_GroupCollector | None" = None

    def input_link(self, node, identifier: str) -> _Link | None:
        """The effective link into ``node``'s socket ``identifier``, if any."""
        for link in self.incoming.get(node.name, ()):
            if link.to_socket.identifier == identifier:
                return link
        return None

    def _resolve(self, link: _Link) -> _Val:
        from_node, from_socket = link.from_node, link.from_socket
        if from_node.bl_idname == "NodeGroupInput":
            val = self.var_map.get(f"_iface_inputs_{from_socket.identifier}")
            if val is None:
                raise CodegenError(
                    f"Group input socket '{from_socket.name}' has no interface "
                    "variable — was the interface emitted?"
                )
            return val
        val = self.var_map.get(from_node.name)
        if val is None:
            raise CodegenError(
                f"Node '{from_node.name}' is referenced before any code was "
                "generated for it"
            )
        return val

    def upstream_expr(self, link: _Link) -> Expr:
        """Expression referencing the source side of ``link``."""
        return _output_expr(self._resolve(link), link.from_node, link.from_socket)

    def socket_expr(self, link: _Link) -> Expr:
        """Like :meth:`upstream_expr` but guaranteed to evaluate to a Socket.

        Node-valued upstreams get an explicit ``.o.<name>`` accessor even for
        their first output, so socket methods can be called on the result.
        """
        return _output_expr(
            self._resolve(link), link.from_node, link.from_socket, force_socket=True
        )

    def promote_to_var(self, link: _Link, expr: Expr) -> Expr:
        """Bind an upstream socket expression to a variable and return its Ref.

        Used when an expression must be referenced more than once (e.g. the
        vector feeding ``vec.x`` / ``vec.y``). The assignment is queued on
        ``pending_lines`` and flushed before the consuming statement.
        """
        label = link.from_socket.name or link.from_node.bl_label or "value"
        var = _make_var(label, self.counter)
        self.pending_lines.append(f"    {var} = {expr.render()}")
        ref = Ref(var)
        if link.from_node.bl_idname != "NodeGroupInput":
            self.var_map[link.from_node.name] = _Val(
                ref, is_socket=True, socket_id=link.from_socket.identifier
            )
        return ref

    def input_expr(self, node, socket) -> Expr | None:
        """Expression for an input socket: upstream reference or literal default."""
        link = self.input_link(node, socket.identifier)
        if link is not None:
            return self.upstream_expr(link)
        if hasattr(socket, "default_value"):
            return Lit(socket.default_value)
        return None

    def constructor(self, node, skip_input_id: str | None = None) -> Call:
        """``alias.ClassName(...)`` call for a node.

        Linked inputs become kwargs referencing upstream expressions, unlinked
        non-default inputs become literal kwargs, and non-default keyword-only
        properties are appended. When a factory classmethod covers the node's
        non-default properties (``Math.square_root``, ``Compare.float.equal``,
        …) it is used instead of the plain constructor. ``skip_input_id``
        omits one input socket (used for the implicit ``>>`` chain input).
        """
        found = _find_cls(node.bl_idname)
        if found is None:
            raise CodegenError(
                f"No nodebpy class is registered for '{node.bl_idname}' "
                f"(node '{node.name}')"
            )
        alias, cls = found
        self.used_aliases.add(alias)

        by_socket: dict[str, list[tuple[int, Expr]]] = {}
        for link in self.incoming.get(node.name, ()):
            if skip_input_id and link.to_socket.identifier == skip_input_id:
                continue
            by_socket.setdefault(_normalize(link.to_socket.identifier), []).append(
                (link.sort_id, self.upstream_expr(link))
            )
        socket_kwargs: dict[str, Expr] = {}
        for name, entries in by_socket.items():
            if len(entries) == 1:
                socket_kwargs[name] = entries[0][1]
            else:
                # Multiple links on one multi-input socket become a tuple in
                # creation order (descending sort_id) so the rebuilt tree
                # gets the same multi-input ordering.
                entries.sort(key=lambda e: e[0], reverse=True)
                socket_kwargs[name] = TupleExpr([e[1] for e in entries])

        socket_kwargs.update(
            self._literal_kwargs(node, cls, socket_kwargs, skip_input_id)
        )
        prop_values = {
            name: value
            for name, value in _non_default_props(node, cls).items()
            if name not in socket_kwargs
        }

        factory_call = _factory_call(
            f"{alias}.{cls.__name__}",
            node,
            cls,
            prop_values,
            socket_kwargs,
            skip_input_id,
        )
        if factory_call is not None:
            return factory_call

        kwargs = dict(socket_kwargs)
        for name, value in prop_values.items():
            kwargs[name] = Lit(value)
        return Call(f"{alias}.{cls.__name__}", kwargs=kwargs)

    def _literal_kwargs(
        self, node, cls: type, existing: dict, skip_input_id: str | None
    ) -> dict[str, Expr]:
        """Literal kwargs for unlinked sockets whose value differs from the default."""
        try:
            sig = inspect.signature(cls.__init__)
        except (TypeError, ValueError):
            sig = None
        positional = (
            [
                (n, p)
                for n, p in sig.parameters.items()
                if n != "self" and p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ]
            if sig
            else []
        )

        result: dict[str, Expr] = {}
        blender_defaults: dict[str, object] | None = None
        for i, socket in enumerate(node.inputs):
            if socket.is_linked:
                continue
            if not socket.enabled:
                # Disabled by the active mode/data_type — the value is stale
                # and ignored by evaluation (length= on EVALUATED
                # CurveToPoints).
                continue
            if skip_input_id and socket.identifier == skip_input_id:
                continue
            if not hasattr(socket, "default_value"):
                continue
            kwarg_name = _normalize(socket.identifier)
            if kwarg_name in existing:
                continue
            try:
                val = socket.default_value
            except Exception:
                continue

            default: object = inspect.Parameter.empty
            if sig and kwarg_name in sig.parameters:
                default = sig.parameters[kwarg_name].default
            elif i < len(positional):
                default = positional[i][1].default

            if default is not inspect.Parameter.empty and default is not None:
                if _eq(val, default):
                    continue
            else:
                # Python default is None (optional socket param) — compare
                # against Blender's actual default for a fresh node.
                if blender_defaults is None:
                    blender_defaults = _get_blender_socket_defaults(
                        self.node_tree.bl_idname, node.bl_idname
                    )
                blender_default = blender_defaults.get(socket.identifier)
                if blender_default is not None:
                    if _eq(val, blender_default):
                        continue
                elif _is_zero(val):
                    continue
            result[kwarg_name] = Lit(val)
        return result


def _output_expr(
    val: _Val, from_node, from_socket, *, force_socket: bool = False
) -> Expr:
    """Reference an output socket of an emitted value.

    Node-valued expressions reference the first output bare (``noise``) and
    others via ``.o.<name>``; ``force_socket`` adds the accessor even for the
    first output. Socket-valued expressions are returned as-is, after
    checking they represent the requested output.
    """
    if val.outputs is not None:
        expr = val.outputs.get(from_socket.identifier)
        if expr is None:
            raise CodegenError(
                f"Output '{from_socket.name}' of node '{from_node.name}' has "
                "no generated expression"
            )
        return expr
    if val.expr is None:  # pragma: no cover - vals always carry one or the other
        raise CodegenError(f"Node '{from_node.name}' has no generated expression")
    if val.is_socket:
        if val.socket_id is not None and val.socket_id != from_socket.identifier:
            raise CodegenError(
                f"Expression for node '{from_node.name}' evaluates to output "
                f"'{val.socket_id}' but '{from_socket.identifier}' was requested"
            )
        return val.expr
    if (
        not force_socket
        and from_node.outputs
        and from_node.outputs[0].identifier == from_socket.identifier
    ):
        return val.expr
    # Duplicated output names (Mix's four "Result" sockets) are ambiguous on
    # the accessor — fall back to the identifier, which it resolves first.
    if sum(s.name == from_socket.name for s in from_node.outputs) > 1:
        return Attr(val.expr, f"o.{_normalize(from_socket.identifier)}")
    return Attr(val.expr, f"o.{_normalize(from_socket.name)}")


def _is_stable(expr: Expr) -> bool:
    """True when an expression can be rendered repeatedly without creating
    new nodes (a variable reference or attribute access rooted in one)."""
    if isinstance(expr, Ref):
        return True
    if isinstance(expr, Attr):
        return _is_stable(expr.base)
    return False


_BASE_NODE_PROPS: set[str] | None = None


def _base_node_props() -> set[str]:
    """Property names every bpy node has (color, label, mute, …) — these can
    collide with socket parameter names and are never constructor props."""
    global _BASE_NODE_PROPS
    if _BASE_NODE_PROPS is None:
        try:
            import bpy

            _BASE_NODE_PROPS = set(bpy.types.Node.bl_rna.properties.keys())
        except Exception:
            _BASE_NODE_PROPS = set()
    return _BASE_NODE_PROPS


def _non_default_props(node, cls: type) -> dict[str, Any]:
    """Constructor property values that differ from their defaults.

    Covers keyword-only params and positional-or-keyword params that name a
    node-specific bpy property (e.g. ``Compare(operation=..., data_type=...)``);
    positional socket params never match — they are either absent from
    ``bl_rna.properties`` or shadow a base-Node property like ``color``.
    """
    try:
        sig = inspect.signature(cls.__init__)
    except (TypeError, ValueError):
        return {}
    rna_props = getattr(getattr(node, "bl_rna", None), "properties", None)
    result: dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if rna_props is None or name not in rna_props:
                continue
            if name in _base_node_props():
                continue
        elif param.kind != inspect.Parameter.KEYWORD_ONLY:
            continue
        if param.default is inspect.Parameter.empty:
            continue
        try:
            current = getattr(node, name)
        except AttributeError:
            continue
        if current != param.default:
            result[name] = current
    return result


# ---------------------------------------------------------------------------
# Factory reverse-mapping
#
# nodebpy classes carry factory shortcuts whose bodies are simple
# ``return cls(operation="SQRT", value=value)`` calls — generated classmethods
# (``Math.square_root``), factory-instance methods
# (``StoreNamedAttribute.point.integer``), and nested-namespace staticmethods
# (``Compare.float.less_than``). Parsing those bodies at runtime yields a
# reverse table from node state to factory path, so generated code uses the
# same idiomatic spellings users write — with no separate table to keep in
# sync with generate.py. Factories whose bodies are not statically analysable
# (positional args, helper indirection, **kwargs) are simply skipped and the
# node falls back to the plain constructor.
# ---------------------------------------------------------------------------


class _Factory(NamedTuple):
    path: str  # dotted path on the class, e.g. "square_root" or "point.integer"
    props: dict[str, Any]  # constant constructor kwargs the factory sets
    socket_params: dict[str, str]  # normalized socket kwarg → factory param name
    param_defaults: dict[str, Any]  # factory param name → default (sig order)


_FACTORY_CACHE: dict[type, list[_Factory]] = {}


def _as_function(attr: Any):
    if isinstance(attr, (classmethod, staticmethod)):
        return attr.__func__
    if inspect.isfunction(attr):
        return attr
    return None


def _iter_factory_funcs(cls: type):
    """Yield (dotted_path, function, owner_instance) factory candidates.

    Walks the class's own methods plus one level of factory namespaces —
    either nested classes or class-level instances of module-local classes
    (whose methods may reference ``self._x`` constants).
    """
    for name, attr in vars(cls).items():
        if name.startswith("_"):
            continue
        func = _as_function(attr)
        if func is not None:
            yield name, func, None
            continue
        owner = None
        if inspect.isclass(attr) and attr.__module__ == cls.__module__:
            nested = attr
        elif (
            not callable(attr)
            and type(attr).__module__ == cls.__module__
            and inspect.isclass(type(attr))
        ):
            nested = type(attr)
            owner = attr
        else:
            continue
        for sub_name, sub_attr in vars(nested).items():
            if sub_name.startswith("_"):
                continue
            sub_func = _as_function(sub_attr)
            if sub_func is not None:
                yield f"{name}.{sub_name}", sub_func, owner


def _parse_factory_func(
    func, owner: Any, cls: type
) -> tuple[dict[str, Any], dict[str, str]] | None:
    """Extract (constant props, socket-param mapping) from a factory body.

    Only bodies of the form ``return cls(key="CONST", socket=param, ...)``
    qualify; anything else returns None.
    """
    try:
        source = textwrap.dedent(inspect.getsource(func))
        fn = ast.parse(source).body[0]
    except (OSError, TypeError, SyntaxError, IndexError):
        return None
    if not isinstance(fn, ast.FunctionDef):
        return None
    returns = [s for s in ast.walk(fn) if isinstance(s, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.Call):
        return None
    call = returns[0].value
    if not (isinstance(call.func, ast.Name) and call.func.id in ("cls", cls.__name__)):
        return None
    if call.args:
        return None

    props: dict[str, Any] = {}
    socket_params: dict[str, str] = {}
    for kw in call.keywords:
        if kw.arg is None:
            return None  # **kwargs forwarding
        value = kw.value
        if isinstance(value, ast.Constant):
            props[kw.arg] = value.value
        elif isinstance(value, ast.Name):
            socket_params[_normalize(kw.arg)] = value.id
        elif (
            isinstance(value, ast.Attribute)
            and isinstance(value.value, ast.Name)
            and value.value.id == "self"
            and owner is not None
            and hasattr(owner, value.attr)
        ):
            # e.g. domain=self._domain on a parameterised factory instance
            props[kw.arg] = getattr(owner, value.attr)
        else:
            return None
    if not props:
        return None
    return props, socket_params


def _factory_param_defaults(func) -> dict[str, Any] | None:
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return None
    defaults: dict[str, Any] = {}
    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            return None
        defaults[name] = param.default
    return defaults


def _class_factories(cls: type) -> list[_Factory]:
    """All statically-analysable factory shortcuts on a node class, cached."""
    cached = _FACTORY_CACHE.get(cls)
    if cached is not None:
        return cached
    factories: list[_Factory] = []
    for path, func, owner in _iter_factory_funcs(cls):
        parsed = _parse_factory_func(func, owner, cls)
        if parsed is None:
            continue
        defaults = _factory_param_defaults(func)
        if defaults is None:
            continue
        props, socket_params = parsed
        factories.append(_Factory(path, props, socket_params, defaults))
    _FACTORY_CACHE[cls] = factories
    return factories


def _input_socket_by_kwarg(node, kwarg_name: str):
    normalized = _normalize(kwarg_name)
    for socket in node.inputs:
        if _normalize(socket.identifier) == normalized:
            return socket
    return None


def _factory_state_matches(node, props: dict[str, Any]) -> bool:
    """True if every constant the factory sets equals the node's current state."""
    rna_props = getattr(getattr(node, "bl_rna", None), "properties", None)
    for key, value in props.items():
        if rna_props is not None and key in rna_props:
            if getattr(node, key) != value:
                return False
            continue
        # Not an rna property — may be a constant on an input socket (menu
        # "type" sockets). Verify against the socket's default value.
        socket = _input_socket_by_kwarg(node, key)
        if (
            socket is None
            or socket.is_linked
            or not hasattr(socket, "default_value")
            or not _eq(socket.default_value, value)
        ):
            return False
    return True


def _factory_call(
    func_prefix: str,
    node,
    cls: type,
    prop_values: dict[str, Any],
    socket_kwargs: dict[str, Expr],
    skip_input_id: str | None,
) -> Call | None:
    """A factory-classmethod Call for the node, or None to use the constructor.

    A factory is used only when it is fully faithful: it must cover every
    non-default property, every socket kwarg must map to one of its
    parameters, and unlinked sockets whose factory-parameter default differs
    from the node's value get explicit literal kwargs.
    """
    skip_key = _normalize(skip_input_id) if skip_input_id else None
    best: tuple[_Factory, dict[str, Expr]] | None = None

    for factory in _class_factories(cls):
        if not _factory_state_matches(node, factory.props):
            continue
        covered = {_normalize(key) for key in factory.props}
        if set(prop_values) - set(factory.props):
            continue  # leftover props can't be passed to the factory
        if not (set(prop_values) or covered & set(socket_kwargs)):
            continue  # nothing gained over the plain constructor

        call_kwargs: dict[str, Expr] = {}
        for key, expr in socket_kwargs.items():
            if key in covered:
                continue  # constant already baked into the factory
            param = factory.socket_params.get(key)
            if param is None:
                break  # socket not exposed by this factory's signature
            call_kwargs[param] = expr
        else:
            # Unlinked sockets where the factory default differs from the
            # node's actual value need explicit kwargs (e.g. epsilon).
            faithful = True
            for key, param in factory.socket_params.items():
                if param in call_kwargs or key == skip_key:
                    continue
                default = factory.param_defaults.get(param, inspect.Parameter.empty)
                if default is inspect.Parameter.empty or default is None:
                    continue  # None means "leave the socket untouched"
                socket = _input_socket_by_kwarg(node, key)
                if socket is None:
                    faithful = False
                    break
                if socket.is_linked or not hasattr(socket, "default_value"):
                    continue
                if not _eq(socket.default_value, default):
                    call_kwargs[param] = Lit(socket.default_value)
            if faithful and (best is None or len(factory.props) > len(best[0].props)):
                ordered = {
                    param: call_kwargs[param]
                    for param in factory.param_defaults
                    if param in call_kwargs
                }
                best = (factory, ordered)

    if best is None:
        return None
    factory, call_kwargs = best
    # Leading consecutive parameters render positionally (g.Math.sine(x)),
    # matching how factory shortcuts are written by hand.
    args: list[Expr] = []
    for param in factory.param_defaults:
        if param not in call_kwargs:
            break
        args.append(call_kwargs.pop(param))
    return Call(f"{func_prefix}.{factory.path}", args=args, kwargs=call_kwargs)


# ---------------------------------------------------------------------------
# Socket-method reverse-mapping
#
# Many nodes are idiomatically written as methods on the socket feeding their
# primary input: ``value.map_range(...)``, ``cond.switch.float(a, b)``,
# ``field.point.at(i)``, ``vec.x``. Each spec names the receiver input, the
# method path (templated on node properties like domain/data_type), the
# output the method returns, and the parameter mapping. A spec applies only
# when it is fully faithful: receiver linked with a matching socket type, all
# other linked inputs covered by parameters, all outgoing links from the
# returned output, and no uncovered non-default properties. This assumes the
# tree is self-consistent (a node's data_type matches its linked input — true
# for everything Blender lets you build).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SocketMethodSpec:
    receiver: str  # input identifier whose source becomes the receiver
    method: str  # template, e.g. "map_range", "{domain}.at", "switch.{input_type}"
    output: str | None = None  # output identifier the method returns (None = first)
    params: tuple[tuple[str, str], ...] = ()  # (input identifier, param name)
    require: tuple[tuple[str, Any], ...] = ()  # props that must equal these values
    consumed_props: tuple[str, ...] = ()  # props encoded in the method path/receiver
    prop_kwargs: tuple[tuple[str, Any], ...] = ()  # prop → default; kwarg if differs
    receiver_socket_type: str | None = None  # required from-socket type;
    # "{data_type}" resolves via _DATA_TYPE_SOCKET so the method re-derives
    # the same data_type from the receiver socket on round-trip.
    require_sockets: tuple[tuple[str, str], ...] = ()  # unlinked input sockets
    # (typically menus) that must hold these values — baked into the method.
    always_args: int = 0  # leading params the method signature requires —
    # emitted even when unlinked at the default value (skipping them would
    # render a call with missing positional arguments).


@dataclass(frozen=True)
class DissolveSpec:
    """A node replaced entirely by accessor attributes on its input.

    ``vec.x`` / ``mat.translation`` / ``col.r`` — every output maps to an
    attribute on the receiver expression; the node itself emits nothing.
    """

    receiver: str  # input identifier
    outputs: tuple[tuple[str, str], ...]  # (output identifier, attribute)
    require: tuple[tuple[str, Any], ...] = ()  # props that must equal these
    consumed_props: tuple[str, ...] = ()  # props the accessor re-derives
    receiver_socket_type: str | None = None  # required from-socket type;
    # "{data_type}" resolves via _DATA_TYPE_SOCKET like SocketMethodSpec.
    receiver_structure: str | None = None  # required inferred_structure_type
    # of the from-socket (grids expose the accessors, plain fields don't)


@dataclass(frozen=True)
class TupleMethodSpec:
    """A node authored as a socket method returning a NamedTuple of sockets.

    ``s.find(x)`` → ``(first_found, count)``, ``mat.svd()`` → ``(u, s, v)``.
    Every output maps to a NamedTuple attribute on the call result; when more
    than one link consumes the node, the call is bound to a variable first so
    re-rendering it cannot create duplicate nodes.
    """

    receiver: str  # input identifier whose source becomes the receiver
    method: str
    outputs: tuple[tuple[str, str], ...]  # (output identifier, tuple attr)
    params: tuple[tuple[str, str], ...] = ()  # required params — always
    # rendered positionally, linked or not
    receiver_socket_type: str | None = None
    require_sockets: tuple[tuple[str, str], ...] = ()  # as SocketMethodSpec


_DOMAIN_ATTR = {
    "POINT": "point",
    "EDGE": "edge",
    "FACE": "face",
    "CORNER": "corner",
    "CURVE": "spline",
    "INSTANCE": "instance",
    "LAYER": "layer",
}

_SWITCH_METHOD = {
    "FLOAT": "float",
    "INT": "integer",
    "BOOLEAN": "boolean",
    "VECTOR": "vector",
    "RGBA": "color",
    "ROTATION": "rotation",
    "MATRIX": "matrix",
    "STRING": "string",
    "MENU": "menu",
    "OBJECT": "object",
    "IMAGE": "image",
    "GEOMETRY": "geometry",
    "COLLECTION": "collection",
    "MATERIAL": "material",
    "BUNDLE": "bundle",
    "CLOSURE": "closure",
    "FONT": "font",
    "SOUND": "sound",
}

_DATA_TYPE_SOCKET = {
    "FLOAT": "VALUE",
    "INT": "INT",
    "FLOAT_VECTOR": "VECTOR",
    "BOOLEAN": "BOOLEAN",
    "FLOAT_COLOR": "RGBA",
    "QUATERNION": "ROTATION",
    "FLOAT4X4": "MATRIX",
    "TRANSFORM": "MATRIX",
    "VECTOR": "VECTOR",  # GridInfo-style enums spell vectors "VECTOR"
}

_FIELD_PROPS = ("domain", "data_type")
_FIELD_STAT_PARAMS = (("Group Index", "group_index"),)
_MAP_RANGE_PROP_KWARGS = (("clamp", True), ("interpolation_type", "LINEAR"))


def _field_spec(method: str, output: str, *params) -> SocketMethodSpec:
    return SocketMethodSpec(
        receiver="Value",
        method=method,
        output=output,
        params=tuple(params),
        consumed_props=_FIELD_PROPS,
        receiver_socket_type="{data_type}",
    )


def _vector_op_spec(
    operation: str, method: str, output: str, *params
) -> SocketMethodSpec:
    return SocketMethodSpec(
        receiver="Vector",
        method=method,
        output=output,
        params=tuple(params),
        require=(("operation", operation),),
        consumed_props=("operation",),
        receiver_socket_type="VECTOR",
    )


def _string_spec(
    method: str, output: str, *params, case: str | None = None
) -> SocketMethodSpec:
    return SocketMethodSpec(
        receiver="String",
        method=method,
        output=output,
        params=tuple(params),
        require_sockets=(("Case", case),) if case else (),
        receiver_socket_type="STRING",
    )


def _match_string_spec(method: str, operation: str) -> SocketMethodSpec:
    return SocketMethodSpec(
        receiver="String",
        method=method,
        output="Result",
        params=(("Key", "search"),),
        require_sockets=(("Operation", operation),),
        receiver_socket_type="STRING",
    )


def _matrix_spec(method: str, output: str) -> SocketMethodSpec:
    return SocketMethodSpec(
        receiver="Matrix",
        method=method,
        output=output,
        receiver_socket_type="MATRIX",
    )


def _mix_spec(data_type: str, attr: str, suffix: str) -> SocketMethodSpec:
    """``factor.mix.float(a, b)`` — the receiver is always the uniform float
    factor; non-uniform vector mixes have ``Factor_Vector`` linked instead
    and fall through to the constructor."""
    return SocketMethodSpec(
        receiver="Factor_Float",
        method=f"mix.{attr}",
        output=f"Result_{suffix}",
        params=((f"A_{suffix}", "a"), (f"B_{suffix}", "b")),
        require=(("data_type", data_type),),
        consumed_props=("data_type",),
        receiver_socket_type="VALUE",
        always_args=2,
    )


_SOCKET_METHODS: dict[str, list[SocketMethodSpec]] = {
    "GeometryNodeSwitch": [
        SocketMethodSpec(
            receiver="Switch",
            method="switch.{input_type}",
            output="Output",
            params=(("False", "false"), ("True", "true")),
            consumed_props=("input_type",),
            receiver_socket_type="BOOLEAN",
        ),
    ],
    "ShaderNodeMapRange": [
        SocketMethodSpec(
            receiver="Value",
            method="map_range",
            output="Result",
            params=(
                ("From Min", "from_min"),
                ("From Max", "from_max"),
                ("To Min", "to_min"),
                ("To Max", "to_max"),
                ("Steps", "steps"),
            ),
            require=(("data_type", "FLOAT"),),
            consumed_props=("data_type",),
            prop_kwargs=_MAP_RANGE_PROP_KWARGS,
            receiver_socket_type="VALUE",
        ),
        SocketMethodSpec(
            receiver="Vector",
            method="map_range",
            output="Vector",
            params=(
                ("From_Min_FLOAT3", "from_min"),
                ("From_Max_FLOAT3", "from_max"),
                ("To_Min_FLOAT3", "to_min"),
                ("To_Max_FLOAT3", "to_max"),
                ("Steps_FLOAT3", "steps"),
            ),
            require=(("data_type", "FLOAT_VECTOR"),),
            consumed_props=("data_type",),
            prop_kwargs=_MAP_RANGE_PROP_KWARGS,
            receiver_socket_type="VECTOR",
        ),
    ],
    "GeometryNodeFieldAtIndex": [
        _field_spec("{domain}.at", "Value", ("Index", "index")),
    ],
    "GeometryNodeFieldOnDomain": [
        _field_spec("{domain}.evaluate", "Value"),
    ],
    "GeometryNodeAccumulateField": [
        _field_spec("{domain}.leading", "Leading", *_FIELD_STAT_PARAMS),
        _field_spec("{domain}.trailing", "Trailing", *_FIELD_STAT_PARAMS),
        _field_spec("{domain}.total", "Total", *_FIELD_STAT_PARAMS),
    ],
    "GeometryNodeFieldAverage": [
        _field_spec("{domain}.mean", "Mean", *_FIELD_STAT_PARAMS),
        _field_spec("{domain}.median", "Median", *_FIELD_STAT_PARAMS),
    ],
    "GeometryNodeFieldMinAndMax": [
        _field_spec("{domain}.min", "Min", *_FIELD_STAT_PARAMS),
        _field_spec("{domain}.max", "Max", *_FIELD_STAT_PARAMS),
    ],
    "GeometryNodeFieldVariance": [
        _field_spec("{domain}.std_dev", "Standard Deviation", *_FIELD_STAT_PARAMS),
        _field_spec("{domain}.variance", "Variance", *_FIELD_STAT_PARAMS),
    ],
    "ShaderNodeVectorMath": [
        _vector_op_spec("DOT_PRODUCT", "dot", "Value", ("Vector_001", "vector")),
        _vector_op_spec("LENGTH", "length", "Value"),
        _vector_op_spec("NORMALIZE", "normalize", "Vector"),
        _vector_op_spec("CROSS_PRODUCT", "cross", "Vector", ("Vector_001", "other")),
        _vector_op_spec("DISTANCE", "distance", "Value", ("Vector_001", "other")),
        _vector_op_spec("PROJECT", "project", "Vector", ("Vector_001", "other")),
        _vector_op_spec("REFLECT", "reflect", "Vector", ("Vector_001", "normal")),
    ],
    "FunctionNodeRotateVector": [
        SocketMethodSpec(
            receiver="Vector",
            method="rotate",
            output="Vector",
            params=(("Rotation", "rotation"),),
            receiver_socket_type="VECTOR",
        ),
    ],
    "FunctionNodeTransformPoint": [
        SocketMethodSpec(
            receiver="Vector",
            method="transform",
            output="Vector",
            params=(("Transform", "matrix"),),
            receiver_socket_type="VECTOR",
        ),
    ],
    "ShaderNodeClamp": [
        SocketMethodSpec(
            receiver="Value",
            method="clamp",
            output="Result",
            params=(("Min", "min"), ("Max", "max")),
            require=(("clamp_type", "MINMAX"),),
            consumed_props=("clamp_type",),
            receiver_socket_type="VALUE",
        ),
    ],
    "FunctionNodeSliceString": [
        _string_spec("slice", "String", ("Position", "position"), ("Length", "length")),
    ],
    "FunctionNodeReplaceString": [
        _string_spec("replace", "String", ("Find", "find"), ("Replace", "replace")),
    ],
    "FunctionNodeReverseString": [
        _string_spec("reverse", "String"),
    ],
    "FunctionNodeStringLength": [
        _string_spec("length", "Length"),
    ],
    "FunctionNodeMatchString": [
        _match_string_spec("starts_with", "Starts With"),
        _match_string_spec("ends_with", "Ends With"),
        _match_string_spec("contains", "Contains"),
    ],
    "FunctionNodeSetStringCase": [
        _string_spec("uppercase", "String", case="Uppercase"),
        _string_spec("lowercase", "String", case="Lowercase"),
    ],
    "FunctionNodeInvertMatrix": [
        _matrix_spec("invert", "Matrix"),
    ],
    "FunctionNodeTransposeMatrix": [
        _matrix_spec("transpose", "Matrix"),
    ],
    "FunctionNodeMatrixDeterminant": [
        _matrix_spec("determinant", "Determinant"),
    ],
    "FunctionNodeTransformDirection": [
        SocketMethodSpec(
            receiver="Transform",
            method="transform_direction",
            output="Direction",
            params=(("Direction", "direction"),),
            receiver_socket_type="MATRIX",
        ),
    ],
    "FunctionNodeInvertRotation": [
        SocketMethodSpec(
            receiver="Rotation",
            method="invert",
            output="Rotation",
            receiver_socket_type="ROTATION",
        ),
    ],
    "FunctionNodeRotateRotation": [
        SocketMethodSpec(
            receiver="Rotation",
            method="rotate",
            output="Rotation",
            params=(("Rotate By", "rotation"),),
            prop_kwargs=(("rotation_space", "GLOBAL"),),
            receiver_socket_type="ROTATION",
        ),
    ],
    "FunctionNodeRotationToEuler": [
        SocketMethodSpec(
            receiver="Rotation",
            method="to_euler",
            output="Euler",
            receiver_socket_type="ROTATION",
        ),
    ],
    "ShaderNodeMix": [
        _mix_spec("FLOAT", "float", "Float"),
        _mix_spec("VECTOR", "vector", "Vector"),
        _mix_spec("RGBA", "color", "Color"),
        _mix_spec("ROTATION", "rotation", "Rotation"),
    ],
}

_DISSOLVE_SPECS: dict[str, DissolveSpec] = {
    "ShaderNodeSeparateXYZ": DissolveSpec(
        receiver="Vector",
        outputs=(("X", "x"), ("Y", "y"), ("Z", "z")),
        receiver_socket_type="VECTOR",
    ),
    "FunctionNodeSeparateTransform": DissolveSpec(
        receiver="Transform",
        outputs=(
            ("Translation", "translation"),
            ("Rotation", "rotation"),
            ("Scale", "scale"),
        ),
        receiver_socket_type="MATRIX",
    ),
    "FunctionNodeSeparateColor": DissolveSpec(
        receiver="Color",
        outputs=(("Red", "r"), ("Green", "g"), ("Blue", "b"), ("Alpha", "a")),
        require=(("mode", "RGB"),),
        receiver_socket_type="RGBA",
    ),
    # Repeated accessor renders are safe: GridSocketMixin._info reuses one
    # GridInfo node per grid socket.
    "GeometryNodeGridInfo": DissolveSpec(
        receiver="Grid",
        outputs=(("Transform", "transform"), ("Background Value", "background_value")),
        consumed_props=("data_type",),
        receiver_socket_type="{data_type}",
        receiver_structure="GRID",
    ),
}

_TUPLE_METHODS: dict[str, TupleMethodSpec] = {
    "FunctionNodeFindInString": TupleMethodSpec(
        receiver="String",
        method="find",
        outputs=(("First Found", "first_found"), ("Count", "count")),
        params=(("Search", "search"),),
        receiver_socket_type="STRING",
        require_sockets=(("Mode", "From Start"),),
    ),
    "FunctionNodeMatrixSVD": TupleMethodSpec(
        receiver="Matrix",
        method="svd",
        outputs=(("U", "u"), ("S", "s"), ("V", "v")),
        receiver_socket_type="MATRIX",
    ),
    "FunctionNodeRotationToQuaternion": TupleMethodSpec(
        receiver="Rotation",
        method="to_quaternion",
        outputs=(("W", "w"), ("X", "x"), ("Y", "y"), ("Z", "z")),
        receiver_socket_type="ROTATION",
    ),
    "FunctionNodeRotationToAxisAngle": TupleMethodSpec(
        receiver="Rotation",
        method="to_axis_angle",
        outputs=(("Axis", "axis"), ("Angle", "angle")),
        receiver_socket_type="ROTATION",
    ),
}


def _format_method(spec: SocketMethodSpec, node) -> str | None:
    method = spec.method
    if "{domain}" in method:
        attr = _DOMAIN_ATTR.get(getattr(node, "domain", ""))
        if attr is None:
            return None
        method = method.replace("{domain}", attr)
    if "{input_type}" in method:
        attr = _SWITCH_METHOD.get(getattr(node, "input_type", ""))
        if attr is None:
            return None
        method = method.replace("{input_type}", attr)
    return method


def _input_socket_by_identifier(node, identifier: str):
    for socket in node.inputs:
        if socket.identifier == identifier:
            return socket
    return None


def _match_socket_method(
    ctx: EmitContext, node
) -> tuple[SocketMethodSpec, str, str] | None:
    """Structural check: (spec, method path, output identifier) or None."""
    specs = _SOCKET_METHODS.get(node.bl_idname)
    if not specs:
        return None
    found = _find_cls(node.bl_idname)
    if found is None:
        return None
    incoming = {
        link.to_socket.identifier: link for link in ctx.incoming.get(node.name, ())
    }
    for spec in specs:
        if any(getattr(node, key, None) != value for key, value in spec.require):
            continue
        receiver_link = incoming.get(spec.receiver)
        if receiver_link is None:
            continue
        expected_type = spec.receiver_socket_type
        if expected_type == "{data_type}":
            expected_type = _DATA_TYPE_SOCKET.get(getattr(node, "data_type", ""))
            if expected_type is None:
                continue
        if (
            expected_type is not None
            and receiver_link.from_socket.type != expected_type
        ):
            continue
        if not all(
            (socket := _input_socket_by_identifier(node, identifier)) is not None
            and not socket.is_linked
            and hasattr(socket, "default_value")
            and _eq(socket.default_value, value)
            for identifier, value in spec.require_sockets
        ):
            continue
        method = _format_method(spec, node)
        if method is None:
            continue
        out_id = spec.output or (node.outputs[0].identifier if node.outputs else "")
        if any(
            link.from_socket.identifier != out_id
            for link in ctx.outgoing.get(node.name, ())
        ):
            continue
        param_ids = {pid for pid, _ in spec.params}
        if set(incoming) - {spec.receiver} - param_ids:
            continue
        _, cls = found
        uncovered = (
            set(_non_default_props(node, cls))
            - set(spec.consumed_props)
            - {key for key, _ in spec.require}
            - {key for key, _ in spec.prop_kwargs}
        )
        if uncovered:
            continue
        return spec, method, out_id
    return None


def _socket_method_val(ctx: EmitContext, node) -> _Val | None:
    """Emit a node as a method call on its receiver socket, if possible."""
    dissolve = _DISSOLVE_SPECS.get(node.bl_idname)
    if dissolve is not None:
        return _dissolve_val(ctx, node, dissolve)
    tuple_spec = _TUPLE_METHODS.get(node.bl_idname)
    if tuple_spec is not None:
        return _tuple_method_val(ctx, node, tuple_spec)
    matched = _match_socket_method(ctx, node)
    if matched is None:
        return None
    spec, method, out_id = matched
    incoming = {
        link.to_socket.identifier: link for link in ctx.incoming.get(node.name, ())
    }
    receiver = ctx.socket_expr(incoming[spec.receiver])

    kwargs: dict[str, Expr] = {}
    blender_defaults: dict[str, object] | None = None
    for index, (identifier, param) in enumerate(spec.params):
        link = incoming.get(identifier)
        if link is not None:
            kwargs[param] = ctx.upstream_expr(link)
            continue
        socket = _input_socket_by_identifier(node, identifier)
        if socket is None or not hasattr(socket, "default_value"):
            continue
        value = socket.default_value
        if index >= spec.always_args:
            if blender_defaults is None:
                blender_defaults = _get_blender_socket_defaults(
                    ctx.node_tree.bl_idname, node.bl_idname
                )
            default = blender_defaults.get(identifier)
            if default is not None:
                if _eq(value, default):
                    continue
            elif _is_zero(value):
                continue
        kwargs[param] = Lit(value)

    for prop, default in spec.prop_kwargs:
        current = getattr(node, prop)
        if current != default:
            kwargs[prop] = Lit(current)

    # Leading consecutive parameters render positionally.
    args: list[Expr] = []
    for _, param in spec.params:
        if param not in kwargs:
            break
        args.append(kwargs.pop(param))

    return _Val(
        MethodCall(receiver, method, args=args, kwargs=kwargs),
        is_socket=True,
        socket_id=out_id,
    )


def _dissolve_val(ctx: EmitContext, node, spec: DissolveSpec) -> _Val | None:
    """Dissolve a separator node into accessor attributes on its input
    (``vec.x``, ``mat.translation``, ``col.r``).

    Repeated accessor renders are safe: the library's
    ``_find_or_create_linked`` reuses one separator node per source socket.
    The receiver must be a variable (or be promoted to one) when it would
    render more than once, so no upstream nodes get duplicated.
    """
    if any(getattr(node, key, None) != value for key, value in spec.require):
        return None
    links = ctx.incoming.get(node.name, ())
    if len(links) != 1 or links[0].to_socket.identifier != spec.receiver:
        return None
    expected_type = spec.receiver_socket_type
    if expected_type == "{data_type}":
        expected_type = _DATA_TYPE_SOCKET.get(getattr(node, "data_type", ""))
        if expected_type is None:
            return None
    if expected_type is not None and links[0].from_socket.type != expected_type:
        return None
    if (
        spec.receiver_structure is not None
        and getattr(links[0].from_socket, "inferred_structure_type", None)
        != spec.receiver_structure
    ):
        return None
    found = _find_cls(node.bl_idname)
    if found is not None:
        uncovered = (
            set(_non_default_props(node, found[1]))
            - {key for key, _ in spec.require}
            - set(spec.consumed_props)
        )
        if uncovered:
            return None
    out_links = ctx.outgoing.get(node.name, ())
    receiver = ctx.socket_expr(links[0])
    if len(out_links) > 1 and not _is_stable(receiver):
        receiver = ctx.promote_to_var(links[0], receiver)
    return _Val(
        None,
        outputs={ident: Attr(receiver, attr) for ident, attr in spec.outputs},
    )


def _tuple_method_val(ctx: EmitContext, node, spec: TupleMethodSpec) -> _Val | None:
    """Dissolve a node into NamedTuple attributes on a socket-method call
    (``s.find(x).count``, ``mat.svd().u``)."""
    incoming = {
        link.to_socket.identifier: link for link in ctx.incoming.get(node.name, ())
    }
    receiver_link = incoming.get(spec.receiver)
    if receiver_link is None:
        return None
    if (
        spec.receiver_socket_type is not None
        and receiver_link.from_socket.type != spec.receiver_socket_type
    ):
        return None
    if not all(
        (socket := _input_socket_by_identifier(node, identifier)) is not None
        and not socket.is_linked
        and hasattr(socket, "default_value")
        and _eq(socket.default_value, value)
        for identifier, value in spec.require_sockets
    ):
        return None
    param_ids = {pid for pid, _ in spec.params}
    if set(incoming) - {spec.receiver} - param_ids:
        return None
    found = _find_cls(node.bl_idname)
    if found is None or _non_default_props(node, found[1]):
        return None
    out_links = ctx.outgoing.get(node.name, ())
    if not out_links:
        return None  # unused node — the constructor keeps it visible

    args: list[Expr] = []
    for identifier, _param in spec.params:
        link = incoming.get(identifier)
        if link is not None:
            args.append(ctx.upstream_expr(link))
            continue
        socket = _input_socket_by_identifier(node, identifier)
        if socket is None or not hasattr(socket, "default_value"):
            return None
        args.append(Lit(socket.default_value))

    base: Expr = MethodCall(ctx.socket_expr(receiver_link), spec.method, args)
    if len(out_links) > 1:
        # Bind the NamedTuple once — re-rendering the call would create a
        # new node per consumer.
        var = _make_var(node.bl_label or "result", ctx.counter)
        ctx.pending_lines.append(f"    {var} = {base.render()}")
        base = Ref(var)
    return _Val(
        None,
        outputs={ident: Attr(base, attr) for ident, attr in spec.outputs},
    )


# ---------------------------------------------------------------------------
# Custom emitters
# ---------------------------------------------------------------------------

EmitterFn = Callable[[Any, EmitContext], "Expr | _Val | None"]

_EMITTERS: dict[str, EmitterFn] = {}


def register_emitter(bl_idname: str) -> Callable[[EmitterFn], EmitterFn]:
    """Register a custom code emitter for a node type.

    The decorated function is called as ``fn(node, ctx)`` and returns an
    :class:`Expr` for the node (or ``None`` to fall back to the default
    emission). ``ctx`` is an :class:`EmitContext`; useful helpers are
    ``ctx.input_expr(node, socket)``, ``ctx.upstream_expr(link)`` and
    ``ctx.constructor(node)``. Emitters may also return a :class:`_Val`
    with per-output expressions (and queue statements on
    ``ctx.pending_lines``) to dissolve a node entirely, as the zone
    emitters do.

    Example::

        @register_emitter("GeometryNodeSetShadeSmooth")
        def _emit_shade_smooth(node, ctx):
            if node.domain == "FACE":
                return Call("g.SetShadeSmooth.face")
            return None
    """

    def decorator(fn: EmitterFn) -> EmitterFn:
        _EMITTERS[bl_idname] = fn
        return fn

    return decorator


# ---------------------------------------------------------------------------
# Operator lifting
#
# These tables mirror nodebpy's OperatorMixin exactly: an emitted operator
# expression must rebuild the same node and operation on round-trip.
# ---------------------------------------------------------------------------

_LIFT_BINARY: dict[str, dict[str, str]] = {
    "ShaderNodeMath": {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "POWER": "**",
        # float % dispatches to FLOORED_MODULO (Python semantics); plain
        # MODULO has no operator equivalent and stays a call.
        "FLOORED_MODULO": "%",
    },
    "ShaderNodeVectorMath": {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "MODULO": "%",
        "SCALE": "*",
    },
    "FunctionNodeIntegerMath": {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "POWER": "**",
        "MODULO": "%",
        "DIVIDE_FLOOR": "//",
    },
    "FunctionNodeBooleanMath": {
        "AND": "&",
        "OR": "|",
        "XOR": "^",
    },
}

_LIFT_UNARY: dict[str, dict[str, str]] = {
    "FunctionNodeBooleanMath": {"NOT": "~"},
    "FunctionNodeIntegerMath": {"NEGATE": "-"},
}

_LIFT_UNARY_CALL: dict[str, dict[str, str]] = {
    "ShaderNodeMath": {"ABSOLUTE": "abs"},
    "ShaderNodeVectorMath": {"ABSOLUTE": "abs"},
    "FunctionNodeIntegerMath": {"ABSOLUTE": "abs"},
}


def _lift_pair(node) -> tuple[Any, Any] | None:
    """The two operand sockets for a liftable binary node, or None."""
    if (
        node.bl_idname == "ShaderNodeVectorMath"
        and getattr(node, "operation", "") == "SCALE"
    ):
        if len(node.inputs) > 3:
            return node.inputs[0], node.inputs[3]
        return None
    if len(node.inputs) >= 2:
        return node.inputs[0], node.inputs[1]
    return None


class _LiftPlan(NamedTuple):
    kind: str  # "binary" | "unary" | "unary_call"
    op: str
    sockets: tuple


def _lift_plan(node, linked_ids: set[str]) -> _LiftPlan | None:
    """Structural check: can this node be lifted to an operator expression?

    Requires at least one linked operand and that *all* incoming links target
    operand sockets — otherwise links would be silently dropped on round-trip.
    """
    operation = getattr(node, "operation", "")

    binary = _LIFT_BINARY.get(node.bl_idname, {})
    if operation in binary:
        pair = _lift_pair(node)
        if pair is not None:
            lhs_s, rhs_s = pair
            pair_ids = {lhs_s.identifier, rhs_s.identifier}
            if linked_ids and linked_ids <= pair_ids:
                if all(
                    s.identifier in linked_ids or hasattr(s, "default_value")
                    for s in pair
                ):
                    return _LiftPlan("binary", binary[operation], pair)

    inputs = list(node.inputs)
    if inputs:
        first_id = inputs[0].identifier
        unary = _LIFT_UNARY.get(node.bl_idname, {})
        if operation in unary and linked_ids == {first_id}:
            return _LiftPlan("unary", unary[operation], (inputs[0],))
        unary_call = _LIFT_UNARY_CALL.get(node.bl_idname, {})
        if operation in unary_call and linked_ids == {first_id}:
            return _LiftPlan("unary_call", unary_call[operation], (inputs[0],))
    return None


def _lift_expr(ctx: EmitContext, node, plan: _LiftPlan) -> Expr:
    """Materialise a lift plan into an expression."""
    operands: list[Expr] = []
    for socket in plan.sockets:
        operand = ctx.input_expr(node, socket)
        if operand is None:  # pragma: no cover - guarded by _lift_plan
            raise CodegenError(f"Cannot resolve operands for '{node.name}'")
        operands.append(operand)
    if plan.kind == "binary":
        return BinOp(plan.op, operands[0], operands[1])
    if plan.kind == "unary":
        return UnaryOp(plan.op, operands[0])
    return Call(plan.op, args=[operands[0]])


def _linked_ids(ctx: EmitContext, node) -> set[str]:
    return {link.to_socket.identifier for link in ctx.incoming.get(node.name, ())}


# ---------------------------------------------------------------------------
# Chain analysis (>> stitching)
# ---------------------------------------------------------------------------

_CHAIN_SOCKET_TYPES = frozenset({"GEOMETRY", "SHADER"})


def _chainable_links(ctx: EmitContext) -> dict[str, _Link]:
    """Consumer node name → its single chainable incoming link.

    A link is chainable when it joins a first output to a first input, the
    source socket has no fan-out, and the data flowing is a "pipeline" type
    (geometry/shader). Such links render as ``a >> b``.
    """
    socket_out: dict[tuple[str, str], int] = {}
    socket_in: dict[tuple[str, str], int] = {}
    for link in ctx.links:
        out_key = (link.from_node.name, link.from_socket.identifier)
        in_key = (link.to_node.name, link.to_socket.identifier)
        socket_out[out_key] = socket_out.get(out_key, 0) + 1
        socket_in[in_key] = socket_in.get(in_key, 0) + 1

    result: dict[str, _Link] = {}
    for link in ctx.links:
        from_node, to_node = link.from_node, link.to_node
        if to_node.bl_idname in _SKIP_BL_IDNAMES:
            continue
        if to_node.bl_idname in _EMITTERS:
            continue  # custom emitters manage their own inputs
        if link.from_socket.type not in _CHAIN_SOCKET_TYPES:
            continue
        if from_node.bl_idname != "NodeGroupInput":
            if not (
                from_node.outputs
                and from_node.outputs[0].identifier == link.from_socket.identifier
            ):
                continue
        if not (
            to_node.inputs and to_node.inputs[0].identifier == link.to_socket.identifier
        ):
            continue
        if socket_out[(from_node.name, link.from_socket.identifier)] != 1:
            continue
        # Multi-input sockets with several links must stay as a tuple kwarg.
        if socket_in[(to_node.name, link.to_socket.identifier)] != 1:
            continue
        result[to_node.name] = link
    return result


def _gate_short_chains(
    ctx: EmitContext,
    chain_in: dict[str, _Link],
    ordered: list,
    min_chain_length: int,
) -> set[str]:
    """Suppress ``>>`` syntax for runs shorter than the threshold.

    Run length counts a leading interface input and a trailing interface
    output as items, matching how the chain reads in the generated code.
    Returns the gated node names — they keep ordinary kwarg inlining but
    render no ``>>`` — and removes their entries from ``chain_in``.
    """
    node_by_name = {n.name: n for n in ordered}
    next_map: dict[str, str] = {}
    head_from_iface: set[str] = set()
    for to_name, link in chain_in.items():
        if link.from_node.bl_idname == "NodeGroupInput":
            head_from_iface.add(to_name)
        else:
            next_map[link.from_node.name] = to_name
    chained_consumers = set(next_map.values())

    forced: set[str] = set()
    for node in ordered:
        name = node.name
        if name in chained_consumers:
            continue  # not a run head
        if node.bl_idname in _EMITTERS:
            continue
        if _lift_plan(node, _linked_ids(ctx, node)) is not None:
            continue  # lifted expressions always inline freely
        if node.bl_idname in _SOCKET_METHODS and _match_socket_method(ctx, node):
            continue  # socket-method expressions inline freely too

        run = [name]
        current = name
        while (
            len(ctx.outgoing.get(current, ())) == 1
            and (nxt := next_map.get(current))
            and nxt not in run
        ):
            run.append(nxt)
            current = nxt

        tail_outs = ctx.outgoing.get(run[-1], ())
        tail_to_iface = (
            len(tail_outs) == 1 and tail_outs[0].to_node.bl_idname == "NodeGroupOutput"
        )
        length = (
            len(run)
            + (1 if run[0] in head_from_iface else 0)
            + (1 if tail_to_iface else 0)
        )
        # Only gate runs that would actually render with >> syntax.
        has_chain_syntax = len(run) > 1 or run[0] in head_from_iface or tail_to_iface
        if has_chain_syntax and length < min_chain_length:
            forced.update(n for n in run if node_by_name[n].bl_idname not in _EMITTERS)

    for name in forced:
        chain_in.pop(name, None)
    return forced


# ---------------------------------------------------------------------------
# Interface codegen
# ---------------------------------------------------------------------------


# Builder parameter name → bpy interface property name, where they differ.
_IFACE_PARAM_ATTR = {
    "expanded": "menu_expanded",
    "default_attribute": "default_attribute_name",
}


def _interface_kwargs(item, method: str) -> dict[str, Any]:
    """Keyword args whose interface values differ from a fresh socket.

    The builder method's keyword-only parameters define what is expressible;
    each is compared against a probed fresh interface socket (covering
    parameters like ``min_value`` whose Python default ``None`` means
    "leave Blender's default alone").
    """
    from ..builder.tree import SocketContext

    fn = getattr(SocketContext, method, None)
    if fn is None:
        return {}
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return {}
    defaults = _get_interface_defaults(item.id_data.bl_idname, item.socket_type)
    kwargs: dict[str, Any] = {}
    for pname, param in sig.parameters.items():
        if param.kind != inspect.Parameter.KEYWORD_ONLY:
            continue
        attr = _IFACE_PARAM_ATTR.get(pname, pname)
        try:
            current = getattr(item, attr)
        except AttributeError:
            continue
        if not isinstance(current, str):
            try:
                current = tuple(current)
            except TypeError:
                pass
        if attr in defaults:
            if _eq(current, defaults[attr]):
                continue
        elif param.default is None or _eq(current, param.default):
            continue
        kwargs[pname] = current
    return kwargs


def _emit_interface(
    item, direction: str, ctx: EmitContext, indent: str = "    "
) -> str:
    """One ``var = tree.inputs.*()`` / ``tree.outputs.*()`` line."""
    method = _INTERFACE_TYPE_METHOD.get(item.socket_type, "geometry")
    var_name = _make_var(item.name, ctx.counter)
    ctx.var_map[f"_iface_{direction}_{item.identifier}"] = _Val(
        Ref(var_name), is_socket=True
    )

    args: list[str] = [_fmt(item.name)]
    if direction == "inputs" and item.socket_type not in _NO_DEFAULT_VALUE_TYPES:
        try:
            args.append(_fmt(item.default_value))
        except (AttributeError, TypeError):
            pass
    description = getattr(item, "description", "")
    if description:
        args.append(f"description={_fmt(description)}")
    args.extend(
        f"{pname}={_fmt(value)}"
        for pname, value in _interface_kwargs(item, method).items()
    )
    return f"{indent}{var_name} = tree.{direction}.{method}({', '.join(args)})"


def _panel_emittable(panel, in_out: str) -> bool:
    """A panel the builder can author: top-level, sockets all one direction."""
    if panel is None or panel.index == -1:
        return False
    if panel.parent is None or panel.parent.index != -1:
        return False  # nested panels are not expressible
    children = [
        c for c in panel.interface_items if getattr(c, "item_type", "") == "SOCKET"
    ]
    return bool(children) and all(c.in_out == in_out for c in children)


def _emit_interface_lines(node_tree, ctx: EmitContext) -> list[str]:
    """Interface lines in items_tree order, grouped into panel with-blocks."""
    lines: list[str] = []
    for direction, in_out in (("inputs", "INPUT"), ("outputs", "OUTPUT")):
        open_panel_index: int | None = None
        for item in node_tree.interface.items_tree:
            if getattr(item, "item_type", "") != "SOCKET" or item.in_out != in_out:
                continue
            panel = item.parent
            if not _panel_emittable(panel, in_out):
                open_panel_index = None
                lines.append(_emit_interface(item, direction, ctx))
                continue
            if open_panel_index != panel.index:
                open_panel_index = panel.index
                panel_args = [_fmt(panel.name)]
                if panel.default_closed:
                    panel_args.append("default_closed=True")
                lines.append(
                    f"    with tree.{direction}.panel({', '.join(panel_args)}):"
                )
            lines.append(_emit_interface(item, direction, ctx, indent=" " * 8))
    return lines


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def to_python(
    tree: NodeTree | "TreeBuilder",
    min_chain_length: int = 3,
    strict: bool = True,
    max_inline_width: int | None = 88,
) -> str:
    """Generate Python code that recreates the given node tree using nodebpy.

    Parameters
    ----------
        tree: ``TreeBuilder`` | ``bpy.types.NodeTree``.

        min_chain_length: int
            Minimum number of items (including interface endpoints) for a linear
            pipeline to be expressed with ``>>`` syntax; shorter runs are emitted
            as flat assignments.
        strict: bool
            If True (default), raise :class:`CodegenError` for nodes that
            have no nodebpy class and no registered emitter. If False, emit a
            ``var = None  # TODO`` placeholder instead.
        max_inline_width: int | None
            Longest rendered expression (in characters) that may inline into its consumer's
            statement; longer values bind to a variable first, so deep graphs split into
            steps instead of collapsing into one huge statement. ``>>`` chain continuations
            are exempt — a pipeline stays one statement; statements longer than 88 columns
            wrap in parentheses with one ``>>`` segment per line.
            ``None`` disables the budget.

    Returns
    -------
    str
        Python source code as a string.
    """
    node_tree: NodeTree = tree.tree if hasattr(tree, "tree") else tree  # ty: ignore[invalid-assignment]

    collector = _GroupCollector(
        min_chain_length=min_chain_length,
        strict=strict,
        max_inline_width=max_inline_width,
    )
    emission = _emit_tree(node_tree, collector)

    # 5. Assemble the module: imports, any nested group classes, then the tree,
    #    each top-level block separated by two blank lines (PEP 8).
    used_aliases = emission.used_aliases | collector.used_aliases
    import_parts = [
        f"{_ALIAS_MODULES[alias]} as {alias}"
        for alias in ("g", "s", "c")
        if alias in used_aliases
    ]
    lines = ["from nodebpy import " + ", ".join(import_parts + ["TreeBuilder"])]
    if collector.bases_used:
        lines.append(
            "from nodebpy.builder import " + ", ".join(sorted(collector.bases_used))
        )
    # Group classes are top-level defs: two blank lines around each (PEP 8).
    for class_def in collector.class_defs:
        lines.extend(["", "", class_def])
    lines.append("")  # one blank line before the tree block
    if collector.class_defs:
        lines.append("")  # ...two, when a class def precedes it

    constructor = _TREE_CONSTRUCTORS.get(node_tree.bl_idname, "TreeBuilder")
    lines.append(f"with {constructor}({_fmt(node_tree.name)}) as tree:")
    lines.extend(_assemble_tree_body(emission))
    return "\n".join(lines)


def _assemble_tree_body(emission: "_TreeEmission") -> list[str]:
    """The indented lines inside a ``with ... as tree:`` block (or, re-indented,
    a ``_build_group`` method)."""
    iface_lines, body, out_lines = (
        emission.iface_lines,
        emission.body_lines,
        emission.out_lines,
    )
    lines = list(iface_lines)
    if iface_lines and (body or out_lines):
        lines.append("")
    lines.extend(body)
    if out_lines:
        if body:
            lines.append("")
        lines.extend(out_lines)
    if not (iface_lines or body or out_lines):
        lines.append("    pass")
    return lines


@dataclass
class _TreeEmission:
    """The interface, body, and output lines of a single tree (without the
    surrounding ``with``/class wrapper). Lines carry their in-block 4-space
    indent."""

    iface_lines: list[str]
    body_lines: list[str]
    out_lines: list[str]
    used_aliases: set[str]


# bl_idname of a group node → the CustomGroup base it round-trips to.
_GROUP_BASES = {
    "GeometryNodeGroup": "CustomGeometryGroup",
    "ShaderNodeGroup": "CustomShaderGroup",
    "CompositorNodeGroup": "CustomCompositorGroup",
}


@dataclass
class _GroupCollector:
    """Tracks nested-group class emission across one ``to_python`` call.

    Each distinct inner node tree becomes one ``CustomGroup`` subclass,
    rendered into :attr:`class_defs` in dependency order (a group is appended
    only after the groups it nests, since ``register`` recurses first)."""

    min_chain_length: int
    strict: bool
    max_inline_width: int | None
    class_defs: list[str] = field(default_factory=list)
    names_by_tree: dict[str, str] = field(default_factory=dict)
    used_names: set[str] = field(default_factory=set)
    bases_used: set[str] = field(default_factory=set)
    used_aliases: set[str] = field(default_factory=set)

    def register(self, node_tree) -> str:
        """Ensure a class exists for ``node_tree`` and return its name."""
        existing = self.names_by_tree.get(node_tree.name)
        if existing is not None:
            return existing
        class_name = self._unique_name(node_tree.name)
        # Reserve before recursing so a self-referential group resolves.
        self.names_by_tree[node_tree.name] = class_name
        emission = _emit_tree(node_tree, self)
        self.used_aliases |= emission.used_aliases
        base = _GROUP_BASES.get(node_tree.bl_idname, "CustomGeometryGroup")
        self.bases_used.add(base)
        self.class_defs.append(
            _render_group_class(class_name, node_tree, base, emission)
        )
        return class_name

    def _unique_name(self, tree_name: str) -> str:
        base = _class_name(tree_name)
        name, n = base, 1
        while name in self.used_names:
            n += 1
            name = f"{base}{n}"
        self.used_names.add(name)
        return name


def _class_name(name: str) -> str:
    """A valid, PascalCase Python class name derived from a tree name."""
    cleaned = "".join(p[:1].upper() + p[1:] for p in re.split(r"\W+", name) if p)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"Group{cleaned}"
    if keyword.iskeyword(cleaned):
        cleaned += "_"
    return cleaned


def _render_group_class(
    class_name: str, node_tree, base: str, emission: "_TreeEmission"
) -> str:
    """A ``class X(CustomGroup): _name = ...; def _build_group(self, tree): ...``
    block, with the tree body re-indented one level deeper."""
    header = [f"class {class_name}({base}):", f"    _name = {_fmt(node_tree.name)}"]
    color = getattr(node_tree, "color_tag", "NONE")
    if color and color != "NONE":
        header.append(f"    _color_tag = {_fmt(color)}")
    header.extend(["", "    def _build_group(self, tree):"])
    body = [("    " + line) if line else "" for line in _assemble_tree_body(emission)]
    return "\n".join(header + body)


def _emit_tree(node_tree, collector: "_GroupCollector") -> "_TreeEmission":
    """Generate the interface/body/output lines for one tree. Nested group
    nodes register their classes on ``collector`` as a side effect."""
    links = _effective_links(node_tree)
    incoming: dict[str, list[_Link]] = {}
    outgoing: dict[str, list[_Link]] = {}
    for link in links:
        incoming.setdefault(link.to_node.name, []).append(link)
        outgoing.setdefault(link.from_node.name, []).append(link)

    ctx = EmitContext(node_tree, links, incoming, outgoing, collector=collector)
    ordered = [n for n in _topo_sort(node_tree) if n.bl_idname not in _SKIP_BL_IDNAMES]
    ordered, frame_of, frame_nodes = _frame_order(node_tree, ordered)

    iface_lines = _emit_interface_lines(node_tree, ctx)

    chain_in = _chainable_links(ctx)
    gated_nodes = _gate_short_chains(ctx, chain_in, ordered, collector.min_chain_length)

    # Body lines tagged with the emitting node's frame; with-blocks and
    # indentation are applied after the loop (frame members are contiguous
    # thanks to _frame_order).
    tagged_body: list[tuple[str | None, str]] = []
    consumed_out_links: set[int] = set()  # id() of tail-inlined _Link tuples

    for node in ordered:
        name = node.name
        frame = frame_of.get(name)

        # 1. Build the node's value:
        #    emitter → socket method → lift → factory/constructor.
        val: _Val | None = None
        emitter = _EMITTERS.get(node.bl_idname)
        if emitter is not None:
            emitted = emitter(node, ctx)
            if emitted is not None:
                val = emitted if isinstance(emitted, _Val) else _Val(emitted)
        if val is None:
            val = _socket_method_val(ctx, node)
        if val is None:
            plan = _lift_plan(node, _linked_ids(ctx, node))
            if plan is not None:
                val = _Val(
                    _lift_expr(ctx, node, plan),
                    is_socket=True,
                    socket_id=node.outputs[0].identifier if node.outputs else None,
                )
        if val is None:
            if _find_cls(node.bl_idname) is None:
                message = f"unsupported node '{name}' ({node.bl_idname})"
                if collector.strict:
                    raise CodegenError(
                        f"Cannot generate code: {message}. Register an emitter "
                        "with register_emitter() or pass strict=False."
                    )
                var = _make_var(node.bl_label or "node", ctx.counter)
                ctx.var_map[name] = _Val(Ref(var))
                tagged_body.append((frame, f"    {var} = None  # TODO: {message}"))
                continue
            chain_link = chain_in.get(name)
            call = ctx.constructor(
                node,
                skip_input_id=chain_link.to_socket.identifier if chain_link else None,
            )
            expr: Expr = (
                BinOp(">>", ctx.upstream_expr(chain_link), call) if chain_link else call
            )
            val = _Val(expr)

        # Flush any variable promotions queued while building the value.
        if ctx.pending_lines:
            tagged_body.extend((frame, line) for line in ctx.pending_lines)
            ctx.pending_lines.clear()

        # 2. Bind it: inline into the consumer, finish a >> chain, or assign.
        if val.outputs is not None:
            # Fully dissolved node (e.g. SeparateXYZ) — consumers reference
            # the per-output expressions directly; nothing to emit here.
            ctx.var_map[name] = val
            continue

        out_links = ctx.outgoing.get(name, ())
        group_outs = [
            link for link in out_links if link.to_node.bl_idname == "NodeGroupOutput"
        ]

        if (
            len(out_links) == 1
            and not group_outs
            # Inlining would create this node at the consumer's statement —
            # only allowed when both sit in the same frame.
            and frame == frame_of.get(out_links[0].to_node.name)
            # Budget: long expressions bind to a variable instead of growing
            # the consumer's statement; chain continuations stay inline.
            and (
                collector.max_inline_width is None
                or chain_in.get(out_links[0].to_node.name) is out_links[0]
                or len(val.require_expr().render()) <= collector.max_inline_width
            )
        ):
            ctx.var_map[name] = val  # single consumer → inline
            continue

        # Gated nodes render no >> syntax; everything else with a single link
        # to a group output finishes its chain right here.
        if len(out_links) == 1 and group_outs and name not in gated_nodes:
            link = group_outs[0]
            out_ref = ctx.var_map.get(f"_iface_outputs_{link.to_socket.identifier}")
            if out_ref is None:
                raise CodegenError(
                    f"Group output socket '{link.to_socket.name}' has no "
                    "interface variable"
                )
            source = _output_expr(val, node, link.from_socket)
            chain = BinOp(">>", source, out_ref.require_expr())
            width = _MAX_LINE_WIDTH - (4 if frame is not None else 0)
            tagged_body.extend(
                (frame, line) for line in _stmt_lines(chain, width=width)
            )
            consumed_out_links.add(id(link))
            continue

        var = _make_var(node.bl_label or "node", ctx.counter)
        width = _MAX_LINE_WIDTH - (4 if frame is not None else 0)
        tagged_body.extend(
            (frame, line)
            for line in _stmt_lines(val.require_expr(), assign=var, width=width)
        )
        ctx.var_map[name] = _Val(
            Ref(var), is_socket=val.is_socket, socket_id=val.socket_id
        )

    # 3. Wrap frame members in with-blocks.
    frame_alias = _TREE_ALIAS.get(node_tree.bl_idname, "g")
    body: list[str] = []
    open_frame: str | None = None
    for frame, line in tagged_body:
        if frame != open_frame:
            open_frame = frame
            if frame is not None:
                ctx.used_aliases.add(frame_alias)
                frame_node = frame_nodes[frame]
                label = _fmt(frame_node.label) if frame_node.label else ""
                body.append(f"    with {frame_alias}.Frame({label}):")
        body.append(f"    {line}" if frame is not None else line)

    # 4. Remaining group-output connections.
    out_lines: list[str] = []
    for link in links:
        if link.to_node.bl_idname != "NodeGroupOutput":
            continue
        if id(link) in consumed_out_links:
            continue
        out_ref = ctx.var_map.get(f"_iface_outputs_{link.to_socket.identifier}")
        if out_ref is None:
            raise CodegenError(
                f"Group output socket '{link.to_socket.name}' has no interface variable"
            )
        source = ctx.upstream_expr(link)
        out_lines.extend(_stmt_lines(BinOp(">>", source, out_ref.require_expr())))

    return _TreeEmission(iface_lines, body, out_lines, ctx.used_aliases)


# ---------------------------------------------------------------------------
# Built-in emitters
# ---------------------------------------------------------------------------


_COMPARE_LIFT = {
    "LESS_THAN": "<",
    "GREATER_THAN": ">",
    "LESS_EQUAL": "<=",
    "GREATER_EQUAL": ">=",
    "EQUAL": "==",
    "NOT_EQUAL": "!=",
}

# data_type the comparison overloads dispatch to, by lhs socket type
_COMPARE_DISPATCH = {"VALUE": "FLOAT", "INT": "INT", "VECTOR": "VECTOR"}

# epsilon the ==/!= overloads set (float32 of 1e-4)
_OPERATOR_EPSILON = 9.999999747378752e-05


def _lift_compare(node, ctx: EmitContext) -> _Val | None:
    """Lift a Compare node to a Python comparison when its state matches
    exactly what the operator overloads produce on round-trip."""
    op = _COMPARE_LIFT.get(node.operation)
    if op is None or node.mode != "ELEMENT":
        return None
    linked = _linked_ids(ctx, node)
    if "A" not in linked or not linked <= {"A", "B"}:
        return None
    a_link = ctx.input_link(node, "A")
    assert a_link is not None
    if _COMPARE_DISPATCH.get(a_link.from_socket.type) != node.data_type:
        return None
    if node.operation in ("EQUAL", "NOT_EQUAL"):
        epsilon = _input_socket_by_identifier(node, "Epsilon")
        if epsilon is None or not _eq(epsilon.default_value, _OPERATOR_EPSILON):
            return None
    b_link = ctx.input_link(node, "B")
    if b_link is not None:
        rhs: Expr = ctx.upstream_expr(b_link)
    else:
        b_socket = _input_socket_by_identifier(node, "B")
        if b_socket is None:
            return None
        rhs = Lit(b_socket.default_value)
    return _Val(
        CompareOp(op, ctx.upstream_expr(a_link), rhs),
        is_socket=True,
        socket_id=node.outputs[0].identifier,
    )


@register_emitter("FunctionNodeCompare")
def _emit_compare(node, ctx: EmitContext) -> Expr | _Val | None:
    """Lift to a Python comparison when possible; otherwise emit the
    constructor — Compare's ``mode`` is consumed via ``**kwargs`` (required
    for VECTOR), so it never appears in the signature and is added
    explicitly."""
    lifted = _lift_compare(node, ctx)
    if lifted is not None:
        return lifted
    call = ctx.constructor(node)
    if node.data_type == "VECTOR":
        call.kwargs["mode"] = Lit(node.mode)
    return call


@register_emitter("FunctionNodeFormatString")
def _emit_format_string(node, ctx: EmitContext) -> Expr | _Val | None:
    """FormatString renders as ``fmt.format({...})`` when the format string
    is linked, else ``g.FormatString("...", items={...})``. Item names may
    not be valid Python kwargs, so items always go through a dict."""
    items: dict[str, Expr] = {}
    for socket in node.inputs:
        if socket.identifier == "Format" or socket.identifier.startswith("__extend__"):
            continue
        link = ctx.input_link(node, socket.identifier)
        items[socket.name] = (
            ctx.upstream_expr(link) if link is not None else Lit(socket.default_value)
        )
    format_link = ctx.input_link(node, "Format")
    if format_link is not None:
        return _Val(
            MethodCall(ctx.socket_expr(format_link), "format", [DictExpr(items)]),
            is_socket=True,
            socket_id=node.outputs[0].identifier,
        )
    format_socket = _input_socket_by_identifier(node, "Format")
    args: list[Expr] = [
        Lit(format_socket.default_value if format_socket is not None else "")
    ]
    kwargs: dict[str, Expr] = {"items": DictExpr(items)} if items else {}
    ctx.used_aliases.add("g")
    return Call("g.FormatString", args, kwargs)


@register_emitter("GeometryNodeStringJoin")
def _emit_join_strings(node, ctx: EmitContext) -> Expr | _Val | None:
    """JoinStrings renders as ``delimiter.join((...))`` when the delimiter
    is linked, else ``g.JoinStrings((...), delimiter=...)``. The strings
    multi-input becomes a tuple in creation order."""
    entries = [
        (link.sort_id, ctx.upstream_expr(link))
        for link in ctx.incoming.get(node.name, ())
        if link.to_socket.identifier == "Strings"
    ]
    entries.sort(key=lambda e: e[0], reverse=True)
    strings = TupleExpr([e[1] for e in entries])
    delimiter_link = ctx.input_link(node, "Delimiter")
    if delimiter_link is not None:
        return _Val(
            MethodCall(ctx.socket_expr(delimiter_link), "join", [strings]),
            is_socket=True,
            socket_id=node.outputs[0].identifier,
        )
    ctx.used_aliases.add("g")
    kwargs: dict[str, Expr] = {}
    delimiter = _input_socket_by_identifier(node, "Delimiter")
    if delimiter is not None and delimiter.default_value:
        kwargs["delimiter"] = Lit(delimiter.default_value)
    return Call("g.JoinStrings", [strings], kwargs)


# data_type → MenuSwitch/IndexSwitch factory classmethod name.
_SWITCH_FACTORY_NAMES = {
    "FLOAT": "float",
    "INT": "integer",
    "BOOLEAN": "boolean",
    "VECTOR": "vector",
    "RGBA": "color",
    "ROTATION": "rotation",
    "MATRIX": "matrix",
    "STRING": "string",
    "MENU": "menu",
    "OBJECT": "object",
    "GEOMETRY": "geometry",
    "COLLECTION": "collection",
    "IMAGE": "image",
    "MATERIAL": "material",
    "BUNDLE": "bundle",
    "CLOSURE": "closure",
}


def _switch_item_exprs(node, ctx: EmitContext, skip_id: str) -> list[tuple[str, Expr]]:
    """(socket name, value expression) per item input, in collection order.

    Unlinked items render their default value, or ``None`` for socket types
    without one (the constructors declare such items but leave them unlinked).
    """
    out: list[tuple[str, Expr]] = []
    for socket in node.inputs:
        if socket.identifier == skip_id or socket.identifier.startswith("__extend__"):
            continue
        link = ctx.input_link(node, socket.identifier)
        if link is not None:
            expr: Expr = ctx.upstream_expr(link)
        elif hasattr(socket, "default_value"):
            expr = Lit(socket.default_value)
        else:
            expr = Lit(None)
        out.append((socket.name, expr))
    return out


@register_emitter("GeometryNodeMenuSwitch")
def _emit_menu_switch(node, ctx: EmitContext) -> Expr | _Val | None:
    """MenuSwitch emits the factory dict form
    ``g.MenuSwitch.geometry(menu, {"Name": value, ...})`` — the plain
    constructor's per-socket kwargs cannot recreate the enum item names."""
    factory = _SWITCH_FACTORY_NAMES.get(node.data_type)
    if factory is None:
        return None
    ctx.used_aliases.add("g")
    items = DictExpr(dict(_switch_item_exprs(node, ctx, "Menu")))
    menu_link = ctx.input_link(node, "Menu")
    if menu_link is not None:
        return Call(f"g.MenuSwitch.{factory}", [ctx.upstream_expr(menu_link), items])
    # The constructor defaults the menu selection to the first item; only a
    # different selection needs an explicit argument.
    menu_socket = _input_socket_by_identifier(node, "Menu")
    first_name = node.enum_items[0].name if node.enum_items else ""
    if menu_socket is not None and menu_socket.default_value != first_name:
        return Call(f"g.MenuSwitch.{factory}", [Lit(menu_socket.default_value), items])
    return Call(f"g.MenuSwitch.{factory}", kwargs={"items": items})


@register_emitter("GeometryNodeIndexSwitch")
def _emit_index_switch(node, ctx: EmitContext) -> Expr | _Val | None:
    """IndexSwitch emits the factory tuple form
    ``g.IndexSwitch.float(index, (a, b, ...))`` so the item count
    round-trips (the constructor clears and recreates the items)."""
    factory = _SWITCH_FACTORY_NAMES.get(node.data_type)
    if factory is None:
        return None
    ctx.used_aliases.add("g")
    items = TupleExpr([expr for _, expr in _switch_item_exprs(node, ctx, "Index")])
    index_link = ctx.input_link(node, "Index")
    if index_link is not None:
        return Call(f"g.IndexSwitch.{factory}", [ctx.upstream_expr(index_link), items])
    index_socket = _input_socket_by_identifier(node, "Index")
    if index_socket is not None and index_socket.default_value:
        return Call(
            f"g.IndexSwitch.{factory}", [Lit(index_socket.default_value), items]
        )
    return Call(f"g.IndexSwitch.{factory}", kwargs={"items": items})


# ---------------------------------------------------------------------------
# Variable-items node emitter (CaptureAttribute / FieldToGrid / …)
#
# These take an ``items={name: field}`` dict; the plain constructor path emits
# each item input as its own kwarg (``field_0=``), which the constructor does
# not accept. A small spec names the fixed (non-item) inputs and the factory
# method selected by the node's type/domain property; item sockets are the
# trailing input/output sockets (one per collection item).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ItemsNodeSpec:
    collection: str  # bpy items collection attribute
    factory_prop: str  # node property choosing the factory method
    factory_map: dict[str, str]  # property value → factory method name
    fixed: tuple[tuple[str, str], ...]  # (input identifier, factory param) pairs


_ITEMS_NODE_SPECS = {
    "GeometryNodeFieldToGrid": _ItemsNodeSpec(
        collection="grid_items",
        factory_prop="data_type",
        factory_map={
            "FLOAT": "float",
            "INT": "integer",
            "VECTOR": "vector",
            "BOOLEAN": "boolean",
        },
        fixed=(("Topology", "topology"),),
    ),
    "GeometryNodeCaptureAttribute": _ItemsNodeSpec(
        collection="capture_items",
        factory_prop="domain",
        factory_map={
            "POINT": "point",
            "EDGE": "edge",
            "FACE": "face",
            "CORNER": "corner",
            "CURVE": "curve",
            "INSTANCE": "instance",
            "LAYER": "layer",
        },
        fixed=(("Geometry", "geometry"),),
    ),
}


def _emit_items_node(node, ctx: EmitContext) -> Expr | _Val | None:
    """A variable-items node as ``Factory(fixed=..., items={name: field})``.

    Bails (falls through) when an input the factory cannot express — e.g. a
    linked CaptureAttribute ``Selection`` — is in use, since no faithful call
    exists."""
    spec = _ITEMS_NODE_SPECS.get(node.bl_idname)
    found = _find_cls(node.bl_idname)
    if spec is None or found is None:
        return None
    alias, cls = found

    n_items = len(getattr(node, spec.collection))
    in_sockets = [s for s in node.inputs if not s.identifier.startswith("__extend__")]
    split = len(in_sockets) - n_items
    fixed_inputs, item_inputs = in_sockets[:split], in_sockets[split:]
    fixed_ids = {ident for ident, _ in spec.fixed}

    # Any fixed input the spec doesn't name can't be authored — only tolerate
    # it when unlinked (a stray default we can safely drop).
    for socket in fixed_inputs:
        if socket.identifier not in fixed_ids and ctx.input_link(
            node, socket.identifier
        ):
            return None

    items: dict[str, Expr] = {}
    for socket, item in zip(item_inputs, getattr(node, spec.collection)):
        link = ctx.input_link(node, socket.identifier)
        if link is not None:
            items[socket.name] = ctx.upstream_expr(link)
        elif hasattr(socket, "default_value"):
            items[socket.name] = Lit(socket.default_value)
        else:
            items[socket.name] = Lit(
                getattr(item, "socket_type", None) or getattr(item, "data_type", "")
            )

    kwargs: dict[str, Expr] = {}
    for ident, param in spec.fixed:
        link = ctx.input_link(node, ident)
        if link is not None:
            kwargs[param] = ctx.upstream_expr(link)
    kwargs["items"] = DictExpr(items)

    ctx.used_aliases.add(alias)
    method = spec.factory_map.get(getattr(node, spec.factory_prop))
    if method is not None:
        return Call(f"{alias}.{cls.__name__}.{method}", kwargs=kwargs)
    kwargs[spec.factory_prop] = Lit(getattr(node, spec.factory_prop))
    return Call(f"{alias}.{cls.__name__}", kwargs=kwargs)


for _items_bl_idname in _ITEMS_NODE_SPECS:
    register_emitter(_items_bl_idname)(_emit_items_node)


# ---------------------------------------------------------------------------
# Node group emitter (recursive)
# ---------------------------------------------------------------------------

_UNSET = object()


def _group_input_defaults(node_tree) -> dict[str, Any]:
    """Interface input socket identifier → default value, for deciding which
    unlinked group inputs differ from the group's own defaults."""
    defaults: dict[str, Any] = {}
    for item in node_tree.interface.items_tree:
        if getattr(item, "item_type", "") != "SOCKET" or item.in_out != "INPUT":
            continue
        if not hasattr(item, "default_value"):
            continue
        value = item.default_value
        try:
            value = tuple(value)
        except TypeError:
            pass
        defaults[item.identifier] = value
    return defaults


def _emit_group_node(node, ctx: EmitContext) -> Expr | _Val | None:
    """A group node becomes ``GeneratedClass(**{"Socket": value, ...})``; the
    inner tree is emitted as a ``CustomGroup`` subclass on the collector.

    Only linked inputs and unlinked inputs whose value differs from the
    group's own interface default are passed — the rest come from the
    rebuilt interface."""
    inner = node.node_tree
    if inner is None or ctx.collector is None:
        return None  # unknown group → fall through to the unsupported path
    class_name = ctx.collector.register(inner)
    iface_defaults = _group_input_defaults(inner)

    items: dict[str, Expr] = {}
    for socket in node.inputs:
        if socket.identifier.startswith("__extend__"):
            continue
        link = ctx.input_link(node, socket.identifier)
        if link is not None:
            items[socket.name] = ctx.upstream_expr(link)
            continue
        if not hasattr(socket, "default_value"):
            continue
        current = socket.default_value
        try:
            current = tuple(current)
        except TypeError:
            pass
        iface_default = iface_defaults.get(socket.identifier, _UNSET)
        if iface_default is _UNSET or not _eq(current, iface_default):
            items[socket.name] = Lit(socket.default_value)
    return GroupCall(class_name, items)


for _group_bl_idname in _GROUP_BASES:
    register_emitter(_group_bl_idname)(_emit_group_node)


# ---------------------------------------------------------------------------
# Zone emitters
#
# Paired zone nodes (Simulation/Repeat/ForEachGeometryElement) cannot be
# expressed as two independent constructors: the wrapper owns the pairing
# and the shared item collections. The input-node emitter declares the zone
# wrapper plus one ``zone.item(...)`` handle line per item and dissolves the
# input node into per-output handle expressions (``h.current``); the
# output-node emitter renders its incoming links as ``expr >> h.next``
# statements at its own topological position and dissolves into
# ``h.result`` expressions. _topo_sort() adds a synthetic input→output
# edge so the input node is always visited first. Item handle lines are
# emitted in original creation order (the numeric suffix of the socket
# identifier) so the rebuilt zone assigns identical socket identifiers.
# ---------------------------------------------------------------------------


@dataclass
class _ZoneState:
    """Per-zone emission state handed from the input to the output emitter."""

    targets: dict[str, Expr]  # output-node input identifier → ``>>`` target
    outputs: dict[str, Expr]  # output-node output identifier → expression


def _prefixed_sockets(node, prefix: str, *, output: bool = False) -> list:
    sockets = node.outputs if output else node.inputs
    return [s for s in sockets if s.identifier.startswith(prefix)]


def _ident_num(identifier: str) -> int:
    """The numeric suffix of an item socket identifier (``Item_3`` → 3)."""
    try:
        return int(identifier.rsplit("_", 1)[1])
    except (IndexError, ValueError):
        return -1


def _item_socket_type(item) -> str:
    return getattr(item, "socket_type", None) or item.data_type


def _significant_default(socket) -> Any | None:
    """The socket's default value if it is worth emitting, else None."""
    if not hasattr(socket, "default_value"):
        return None
    try:
        value = socket.default_value
    except Exception:
        return None
    if isinstance(value, str):
        return value or None
    if value is None or _is_zero(value):
        return None
    try:
        return tuple(value)
    except TypeError:
        return value


def _needs_type_kwarg(
    types: tuple[str, ...],
    type_map: dict[str, str],
    item_type: str,
    link: _Link | None,
    default: Any,
) -> bool:
    """True when item-type inference from the link source or default value
    would not reproduce ``item_type``, so ``type=`` must be emitted."""
    if link is not None:
        from ..types import SOCKET_COMPATIBILITY

        for t in SOCKET_COMPATIBILITY.get(link.from_socket.type, ()):
            if t in types:
                return type_map.get(t, t) != item_type
        return True
    if default is not None:
        from ..builder.items import _infer_value_type

        return _infer_value_type(default) != item_type
    return True


def _zone_value_expr(ctx: EmitContext, link: _Link) -> Expr:
    """Upstream expression for an item value; pinned to the exact output
    socket when the source node has several, so the rebuilt link cannot
    drift to a different best-compatible output."""
    real_outputs = [s for s in link.from_node.outputs if s.enabled]
    if len(real_outputs) > 1:
        return ctx.socket_expr(link)
    return ctx.upstream_expr(link)


def _zone_required(node) -> Any:
    paired = getattr(node, "paired_output", None)
    if paired is None:
        raise CodegenError(
            f"zone input node '{node.name}' has no paired output — the tree "
            "cannot be expressed with a zone wrapper"
        )
    return paired


class _ZoneItemPlan(NamedTuple):
    """One ``zone.<method>(...)`` declaration line plus its socket roles."""

    sort_key: int
    method: str  # "item" / "main_item" / "generated_item"
    item: Any
    types: tuple[str, ...]
    type_map: dict[str, str]
    value_link: _Link | None  # link supplying the declaration's value=
    default_socket: Any | None  # socket probed for a literal default
    extra_kwargs: dict[str, Expr]
    current_id: str | None  # input-node output identifier (read in body)
    next_id: str | None  # output-node input identifier (>> target)
    result_id: str | None  # output-node output identifier (read after)
    roles: tuple[str, str, str]  # expr attr names for the three sockets


def _emit_zone_items(
    ctx: EmitContext,
    zone_ref: Ref,
    node,
    out_node,
    plans: list[_ZoneItemPlan],
) -> tuple[dict[str, Expr], dict[str, Expr], dict[str, Expr]]:
    """Emit handle declaration lines and build the three socket-role maps."""
    consumed_current = {
        link.from_socket.identifier for link in ctx.outgoing.get(node.name, ())
    }
    linked_next = {
        link.to_socket.identifier for link in ctx.incoming.get(out_node.name, ())
    }
    consumed_result = {
        link.from_socket.identifier for link in ctx.outgoing.get(out_node.name, ())
    }

    current_map: dict[str, Expr] = {}
    targets: dict[str, Expr] = {}
    outputs: dict[str, Expr] = {}
    for plan in sorted(plans, key=lambda p: p.sort_key):
        item_type = _item_socket_type(plan.item)
        args: list[Expr] = [Lit(plan.item.name)]
        kwargs: dict[str, Expr] = {}
        default = None
        if plan.value_link is not None:
            args.append(_zone_value_expr(ctx, plan.value_link))
        elif plan.default_socket is not None:
            default = _significant_default(plan.default_socket)
            if default is not None:
                args.append(Lit(default))
        if _needs_type_kwarg(
            plan.types, plan.type_map, item_type, plan.value_link, default
        ):
            kwargs["type"] = Lit(item_type)
        kwargs.update(plan.extra_kwargs)
        call = Call(f"{zone_ref.name}.{plan.method}", args, kwargs)

        needed = (
            plan.current_id in consumed_current
            or plan.next_id in linked_next
            or plan.result_id in consumed_result
        )
        if needed:
            handle = Ref(_make_var(plan.item.name, ctx.counter))
            ctx.pending_lines.append(f"    {handle.name} = {call.render()}")
            current_attr, next_attr, result_attr = plan.roles
            if plan.current_id is not None:
                current_map[plan.current_id] = Attr(handle, current_attr)
            if plan.next_id is not None:
                targets[plan.next_id] = Attr(handle, next_attr)
            if plan.result_id is not None:
                outputs[plan.result_id] = Attr(handle, result_attr)
        else:
            ctx.pending_lines.append(f"    {call.render()}")
    return current_map, targets, outputs


def _emit_state_zone_input(
    node,
    ctx: EmitContext,
    *,
    ctor: str,
    label: str,
    items_attr: str,
    zone_cls_attrs: tuple[tuple[str, ...], dict[str, str]],
    special_outputs: dict[str, str],
    ctor_args: list[Expr],
    extra_targets: dict[str, str],
) -> _Val:
    """Shared input-node emitter for simulation/repeat zones."""
    out_node = _zone_required(node)
    ctx.used_aliases.add("g")
    zone_ref = Ref(_make_var(label, ctx.counter))
    ctx.pending_lines.append(f"    {zone_ref.name} = {Call(ctor, ctor_args).render()}")

    types, type_map = zone_cls_attrs
    items = list(getattr(out_node, items_attr))
    in_inputs = _prefixed_sockets(node, "Item_")
    in_outputs = _prefixed_sockets(node, "Item_", output=True)
    out_inputs = _prefixed_sockets(out_node, "Item_")
    out_outputs = _prefixed_sockets(out_node, "Item_", output=True)

    plans = [
        _ZoneItemPlan(
            sort_key=_ident_num(in_inputs[i].identifier),
            method="item",
            item=item,
            types=types,
            type_map=type_map,
            value_link=ctx.input_link(node, in_inputs[i].identifier),
            default_socket=in_inputs[i],
            extra_kwargs={},
            current_id=in_outputs[i].identifier,
            next_id=out_inputs[i].identifier,
            result_id=out_outputs[i].identifier,
            roles=("current", "next", "result"),
        )
        for i, item in enumerate(items)
    ]
    current_map, targets, outputs = _emit_zone_items(
        ctx, zone_ref, node, out_node, plans
    )
    for identifier, attr in special_outputs.items():
        current_map[identifier] = Attr(zone_ref, attr)
    for identifier, attr in extra_targets.items():
        targets[identifier] = Attr(zone_ref, attr)

    ctx.zones[out_node.name] = _ZoneState(targets, outputs)
    return _Val(None, outputs=current_map)


@register_emitter("GeometryNodeSimulationInput")
def _emit_simulation_input(node, ctx: EmitContext) -> _Val:
    from ..nodes.geometry.zone import BaseSimulationZone

    return _emit_state_zone_input(
        node,
        ctx,
        ctor="g.SimulationZone",
        label="simulation_zone",
        items_attr="state_items",
        zone_cls_attrs=(
            BaseSimulationZone._socket_data_types,
            BaseSimulationZone._type_map,
        ),
        special_outputs={"Delta Time": "delta_time"},
        ctor_args=[],
        extra_targets={"Skip": "output.i.skip"},
    )


@register_emitter("GeometryNodeRepeatInput")
def _emit_repeat_input(node, ctx: EmitContext) -> _Val:
    from ..nodes.geometry.zone import BaseRepeatZone

    ctor_args: list[Expr] = []
    link = ctx.input_link(node, "Iterations")
    if link is not None:
        ctor_args.append(_zone_value_expr(ctx, link))
    else:
        iterations = node.inputs["Iterations"].default_value
        if iterations != 1:
            ctor_args.append(Lit(iterations))
    return _emit_state_zone_input(
        node,
        ctx,
        ctor="g.RepeatZone",
        label="repeat_zone",
        items_attr="repeat_items",
        zone_cls_attrs=(
            BaseRepeatZone._socket_data_types,
            BaseRepeatZone._type_map,
        ),
        special_outputs={"Iteration": "iteration"},
        ctor_args=ctor_args,
        extra_targets={},
    )


@register_emitter("GeometryNodeForeachGeometryElementInput")
def _emit_foreach_input(node, ctx: EmitContext) -> _Val:
    from ..nodes.geometry.zone import (
        ForEachGeometryElementInput,
        ForEachGeometryElementOutput,
    )

    out_node = _zone_required(node)
    ctx.used_aliases.add("g")

    kwargs: dict[str, Expr] = {}
    geometry_link = ctx.input_link(node, "Geometry")
    if geometry_link is not None:
        kwargs["geometry"] = _zone_value_expr(ctx, geometry_link)
    selection_link = ctx.input_link(node, "Selection")
    if selection_link is not None:
        kwargs["selection"] = _zone_value_expr(ctx, selection_link)
    elif node.inputs["Selection"].default_value is not True:
        kwargs["selection"] = Lit(node.inputs["Selection"].default_value)
    if out_node.domain != "POINT":
        kwargs["domain"] = Lit(out_node.domain)
    zone_ref = Ref(_make_var("for_each", ctx.counter))
    ctx.pending_lines.append(
        f"    {zone_ref.name} = "
        f"{Call('g.ForEachGeometryElementZone', kwargs=kwargs).render()}"
    )

    generation_items = list(out_node.generation_items)
    if (
        not generation_items
        or generation_items[0].socket_type != "GEOMETRY"
        or generation_items[0].name != "Geometry"
    ):
        raise CodegenError(
            f"foreach zone '{node.name}': the first generation item is not "
            "the default Geometry item, which the zone wrapper cannot rebuild"
        )

    in_types = ForEachGeometryElementInput._socket_data_types
    in_type_map = ForEachGeometryElementInput._type_map
    main_types = ForEachGeometryElementOutput._socket_data_types
    gen_types = ForEachGeometryElementOutput._generation_data_types
    out_type_map = ForEachGeometryElementOutput._type_map

    plans: list[_ZoneItemPlan] = []
    in_inputs = _prefixed_sockets(node, "Input_")
    in_outputs = _prefixed_sockets(node, "Input_", output=True)
    for i, item in enumerate(out_node.input_items):
        plans.append(
            _ZoneItemPlan(
                sort_key=_ident_num(in_inputs[i].identifier),
                method="item",
                item=item,
                types=in_types,
                type_map=in_type_map,
                value_link=ctx.input_link(node, in_inputs[i].identifier),
                default_socket=in_inputs[i],
                extra_kwargs={},
                current_id=in_outputs[i].identifier,
                next_id=None,
                result_id=None,
                roles=("output", "", ""),
            )
        )
    main_inputs = _prefixed_sockets(out_node, "Main_")
    main_outputs = _prefixed_sockets(out_node, "Main_", output=True)
    for i, item in enumerate(out_node.main_items):
        plans.append(
            _ZoneItemPlan(
                sort_key=_ident_num(main_inputs[i].identifier),
                method="main_item",
                item=item,
                types=main_types,
                type_map=out_type_map,
                value_link=None,
                default_socket=main_inputs[i],
                extra_kwargs={},
                current_id=None,
                next_id=main_inputs[i].identifier,
                result_id=main_outputs[i].identifier,
                roles=("", "input", "output"),
            )
        )
    gen_inputs = _prefixed_sockets(out_node, "Generation_")
    gen_outputs = _prefixed_sockets(out_node, "Generation_", output=True)
    for i, item in enumerate(generation_items):
        if i == 0:
            continue  # the wrapper creates the default Geometry item itself
        extra: dict[str, Expr] = {}
        if item.domain != "POINT":
            extra["domain"] = Lit(item.domain)
        plans.append(
            _ZoneItemPlan(
                sort_key=_ident_num(gen_inputs[i].identifier),
                method="generated_item",
                item=item,
                types=gen_types,
                type_map=out_type_map,
                value_link=None,
                default_socket=gen_inputs[i],
                extra_kwargs=extra,
                current_id=None,
                next_id=gen_inputs[i].identifier,
                result_id=gen_outputs[i].identifier,
                roles=("", "input", "output"),
            )
        )

    current_map, targets, outputs = _emit_zone_items(
        ctx, zone_ref, node, out_node, plans
    )
    current_map["Index"] = Attr(zone_ref, "index")
    current_map["Element"] = Attr(zone_ref, "input.o.element")
    targets[gen_inputs[0].identifier] = Attr(zone_ref, "generation.input")
    outputs[gen_outputs[0].identifier] = Attr(zone_ref, "generation.output")
    outputs["Geometry"] = Attr(zone_ref, "output")

    ctx.zones[out_node.name] = _ZoneState(targets, outputs)
    return _Val(None, outputs=current_map)


@register_emitter("GeometryNodeSimulationOutput")
@register_emitter("GeometryNodeRepeatOutput")
@register_emitter("GeometryNodeForeachGeometryElementOutput")
def _emit_zone_output(node, ctx: EmitContext) -> _Val:
    """Render incoming links as ``expr >> target`` statements and dissolve
    the output node into the result expressions prepared by the input
    emitter."""
    state = ctx.zones.pop(node.name, None)
    if state is None:
        raise CodegenError(
            f"zone output node '{node.name}' was emitted before its paired "
            "input node — is the zone paired?"
        )
    order = {s.identifier: i for i, s in enumerate(node.inputs)}
    links = sorted(
        ctx.incoming.get(node.name, ()),
        key=lambda link: order.get(link.to_socket.identifier, 0),
    )
    for link in links:
        target = state.targets.get(link.to_socket.identifier)
        if target is None:
            raise CodegenError(
                f"zone output node '{node.name}' has a link into "
                f"'{link.to_socket.name}' with no emit target"
            )
        statement = BinOp(">>", ctx.upstream_expr(link), target)
        ctx.pending_lines.extend(_stmt_lines(statement))
    return _Val(None, outputs=state.outputs)
