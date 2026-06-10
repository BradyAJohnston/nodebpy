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

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, NamedTuple


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
class UnaryOp(Expr):
    """A prefix unary operator (``-x``, ``~x``)."""

    op: str
    operand: Expr

    prec: int = field(default=_UNARY_PREC, init=False)

    def render(self) -> str:
        return f"{self.op}{self._child(self.operand, self.operand.prec < self.prec)}"


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


# ---------------------------------------------------------------------------
# Value formatting
# ---------------------------------------------------------------------------


def _fmt(value: Any) -> str:
    """Format a value as a Python literal using double-quoted strings."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
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
    from .builder.node import BaseNode
    from .nodes import compositor, geometry, shader

    domains = [
        ("g", geometry.__name__),
        ("s", shader.__name__),
        ("c", compositor.__name__),
    ]
    for cls in _all_subclasses(BaseNode):
        bl_id = getattr(cls, "_bl_idname", None)
        if not bl_id or bl_id in _NODE_REGISTRY:
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


# ---------------------------------------------------------------------------
# Name utilities
# ---------------------------------------------------------------------------


def _normalize(name: str) -> str:
    from .builder._utils import normalize_name

    return normalize_name(name)


def _make_var(label: str, counter: dict[str, int]) -> str:
    """Return a unique snake_case variable name for a node label."""
    base = _normalize(label) or "node"
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


def _effective_links(node_tree) -> list[_Link]:
    """All links with reroutes collapsed; reroute-internal segments dropped."""
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
    return links


def _topo_sort(node_tree) -> list:
    """Return nodes in topological order (dependencies first)."""
    try:
        import networkx as nx

        G: nx.DiGraph = nx.DiGraph()
        for node in node_tree.nodes:
            G.add_node(node)
        for link in node_tree.links:
            if link.from_node != link.to_node:
                G.add_edge(link.from_node, link.to_node)
        return list(nx.topological_sort(G))
    except ImportError:
        pass

    from collections import deque

    nodes = list(node_tree.nodes)
    node_by_name = {n.name: n for n in nodes}
    in_deg: dict[str, int] = {n.name: 0 for n in nodes}
    adj: dict[str, list[str]] = {n.name: [] for n in nodes}
    for link in node_tree.links:
        fn, tn = link.from_node.name, link.to_node.name
        if fn != tn:
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


# ---------------------------------------------------------------------------
# Emission context
# ---------------------------------------------------------------------------


@dataclass
class EmitContext:
    """State shared across node emission; also the API for custom emitters."""

    node_tree: Any
    links: list[_Link]
    incoming: dict[str, list[_Link]]
    outgoing: dict[str, list[_Link]]
    var_map: dict[str, Expr] = field(default_factory=dict)
    counter: dict[str, int] = field(default_factory=dict)
    used_aliases: set[str] = field(default_factory=set)

    def input_link(self, node, identifier: str) -> _Link | None:
        """The effective link into ``node``'s socket ``identifier``, if any."""
        for link in self.incoming.get(node.name, ()):
            if link.to_socket.identifier == identifier:
                return link
        return None

    def upstream_expr(self, link: _Link) -> Expr:
        """Expression referencing the source side of ``link``."""
        from_node, from_socket = link.from_node, link.from_socket
        if from_node.bl_idname == "NodeGroupInput":
            expr = self.var_map.get(f"_iface_inputs_{from_socket.identifier}")
            if expr is None:
                raise CodegenError(
                    f"Group input socket '{from_socket.name}' has no interface "
                    "variable — was the interface emitted?"
                )
            return expr
        base = self.var_map.get(from_node.name)
        if base is None:
            raise CodegenError(
                f"Node '{from_node.name}' is referenced before any code was "
                "generated for it"
            )
        return _output_expr(base, from_node, from_socket)

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
        properties are appended. ``skip_input_id`` omits one input socket
        (used for the implicit ``>>`` chain input).
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
        kwargs: dict[str, Expr] = {}
        for name, entries in by_socket.items():
            if len(entries) == 1:
                kwargs[name] = entries[0][1]
            else:
                # Multiple links on one multi-input socket become a tuple in
                # creation order (descending sort_id) so the rebuilt tree
                # gets the same multi-input ordering.
                entries.sort(key=lambda e: e[0], reverse=True)
                kwargs[name] = TupleExpr([e[1] for e in entries])

        kwargs.update(self._literal_kwargs(node, cls, kwargs, skip_input_id))
        for name, value in _non_default_props(node, cls).items():
            if name not in kwargs:
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


def _output_expr(base: Expr, from_node, from_socket) -> Expr:
    """Reference an output socket on ``base``: bare for the first output,
    ``.o.<name>`` otherwise."""
    if from_node.outputs and from_node.outputs[0].identifier == from_socket.identifier:
        return base
    return Attr(base, f"o.{_normalize(from_socket.name)}")


def _non_default_props(node, cls: type) -> dict[str, Any]:
    """Constructor property values that differ from their defaults.

    Covers keyword-only params and positional-or-keyword params that name a
    real bpy node property (e.g. ``Compare(operation=..., data_type=...)``);
    positional socket params never match ``bl_rna.properties``.
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
# Custom emitters
# ---------------------------------------------------------------------------

EmitterFn = Callable[[Any, EmitContext], "Expr | None"]

_EMITTERS: dict[str, EmitterFn] = {}


def register_emitter(bl_idname: str) -> Callable[[EmitterFn], EmitterFn]:
    """Register a custom code emitter for a node type.

    The decorated function is called as ``fn(node, ctx)`` and returns an
    :class:`Expr` for the node (or ``None`` to fall back to the default
    emission). ``ctx`` is an :class:`EmitContext`; useful helpers are
    ``ctx.input_expr(node, socket)``, ``ctx.upstream_expr(link)`` and
    ``ctx.constructor(node)``.

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


def _interface_items(node_tree, in_out: str):
    for item in node_tree.interface.items_tree:
        if hasattr(item, "socket_type") and item.in_out == in_out:
            yield item


def _emit_interface(item, direction: str, ctx: EmitContext) -> str:
    """One ``var = tree.inputs.*()`` / ``tree.outputs.*()`` line."""
    method = _INTERFACE_TYPE_METHOD.get(item.socket_type, "geometry")
    var_name = _make_var(item.name, ctx.counter)
    ctx.var_map[f"_iface_{direction}_{item.identifier}"] = Ref(var_name)

    args: list[str] = [_fmt(item.name)]
    if direction == "inputs" and item.socket_type not in _NO_DEFAULT_VALUE_TYPES:
        try:
            args.append(_fmt(item.default_value))
        except (AttributeError, TypeError):
            pass
    return f"    {var_name} = tree.{direction}.{method}({', '.join(args)})"


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def to_python(tree, min_chain_length: int = 3, strict: bool = True) -> str:
    """Generate Python code that recreates the given node tree using nodebpy.

    Args:
        tree: A ``TreeBuilder`` instance or ``bpy.types.NodeTree``.
        min_chain_length: Minimum number of items (including interface
            endpoints) for a linear pipeline to be expressed with ``>>``
            syntax; shorter runs are emitted as flat assignments.
        strict: If True (default), raise :class:`CodegenError` for nodes that
            have no nodebpy class and no registered emitter. If False, emit a
            ``var = None  # TODO`` placeholder instead.

    Returns:
        Python source code as a string.
    """
    node_tree = tree.tree if hasattr(tree, "tree") else tree

    links = _effective_links(node_tree)
    incoming: dict[str, list[_Link]] = {}
    outgoing: dict[str, list[_Link]] = {}
    for link in links:
        incoming.setdefault(link.to_node.name, []).append(link)
        outgoing.setdefault(link.from_node.name, []).append(link)

    ctx = EmitContext(node_tree, links, incoming, outgoing)
    ordered = [n for n in _topo_sort(node_tree) if n.bl_idname not in _SKIP_BL_IDNAMES]

    iface_lines = [
        _emit_interface(item, direction, ctx)
        for direction, in_out in (("inputs", "INPUT"), ("outputs", "OUTPUT"))
        for item in _interface_items(node_tree, in_out)
    ]

    chain_in = _chainable_links(ctx)
    gated_nodes = _gate_short_chains(ctx, chain_in, ordered, min_chain_length)

    body: list[str] = []
    consumed_out_links: set[int] = set()  # id() of tail-inlined _Link tuples

    for node in ordered:
        name = node.name

        # 1. Build the node's expression: emitter → lift → constructor.
        expr: Expr | None = None
        emitter = _EMITTERS.get(node.bl_idname)
        if emitter is not None:
            expr = emitter(node, ctx)
        if expr is None:
            plan = _lift_plan(node, _linked_ids(ctx, node))
            if plan is not None:
                expr = _lift_expr(ctx, node, plan)
        if expr is None:
            if _find_cls(node.bl_idname) is None:
                message = f"unsupported node '{name}' ({node.bl_idname})"
                if strict:
                    raise CodegenError(
                        f"Cannot generate code: {message}. Register an emitter "
                        "with register_emitter() or pass strict=False."
                    )
                var = _make_var(node.bl_label or "node", ctx.counter)
                ctx.var_map[name] = Ref(var)
                body.append(f"    {var} = None  # TODO: {message}")
                continue
            chain_link = chain_in.get(name)
            call = ctx.constructor(
                node,
                skip_input_id=chain_link.to_socket.identifier if chain_link else None,
            )
            expr = (
                BinOp(">>", ctx.upstream_expr(chain_link), call) if chain_link else call
            )

        # 2. Bind it: inline into the consumer, finish a >> chain, or assign.
        out_links = ctx.outgoing.get(name, ())
        group_outs = [
            link for link in out_links if link.to_node.bl_idname == "NodeGroupOutput"
        ]

        if len(out_links) == 1 and not group_outs:
            ctx.var_map[name] = expr  # single consumer → inline
            continue

        # Gated nodes render no >> syntax; everything else with a single link
        # to a group output finishes its chain right here.
        if len(out_links) == 1 and name not in gated_nodes:
            link = group_outs[0]
            out_ref = ctx.var_map.get(f"_iface_outputs_{link.to_socket.identifier}")
            if out_ref is None:
                raise CodegenError(
                    f"Group output socket '{link.to_socket.name}' has no "
                    "interface variable"
                )
            source = _output_expr(expr, node, link.from_socket)
            body.append(f"    {BinOp('>>', source, out_ref).render()}")
            consumed_out_links.add(id(link))
            continue

        var = _make_var(node.bl_label or "node", ctx.counter)
        body.append(f"    {var} = {expr.render()}")
        ctx.var_map[name] = Ref(var)

    # 3. Remaining group-output connections.
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
        out_lines.append(f"    {BinOp('>>', source, out_ref).render()}")

    # 4. Assemble.
    import_parts = [
        f"{_ALIAS_MODULES[alias]} as {alias}"
        for alias in ("g", "s", "c")
        if alias in ctx.used_aliases
    ]
    import_line = "from nodebpy import " + ", ".join(import_parts + ["TreeBuilder"])

    lines = [import_line, "", f'with TreeBuilder("{node_tree.name}") as tree:']
    lines.extend(iface_lines)
    if iface_lines and (body or out_lines):
        lines.append("")
    lines.extend(body)
    if out_lines:
        if body:
            lines.append("")
        lines.extend(out_lines)
    if not (iface_lines or body or out_lines):
        lines.append("    pass")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Built-in emitters
# ---------------------------------------------------------------------------


@register_emitter("FunctionNodeCompare")
def _emit_compare(node, ctx: EmitContext) -> Expr | None:
    """Compare's ``mode`` is consumed via ``**kwargs`` (required for VECTOR),
    so it never appears in the constructor signature — add it explicitly."""
    call = ctx.constructor(node)
    if node.data_type == "VECTOR":
        call.kwargs["mode"] = Lit(node.mode)
    return call
