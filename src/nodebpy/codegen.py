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
import inspect
import textwrap
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


@dataclass(frozen=True)
class DissolveSpec:
    """A node replaced entirely by accessor attributes on its input.

    ``vec.x`` / ``mat.translation`` / ``col.r`` — every output maps to an
    attribute on the receiver expression; the node itself emits nothing.
    """

    receiver: str  # input identifier
    outputs: tuple[tuple[str, str], ...]  # (output identifier, attribute)
    require: tuple[tuple[str, Any], ...] = ()  # props that must equal these
    receiver_socket_type: str | None = None  # required from-socket type


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
    for identifier, param in spec.params:
        link = incoming.get(identifier)
        if link is not None:
            kwargs[param] = ctx.upstream_expr(link)
            continue
        socket = _input_socket_by_identifier(node, identifier)
        if socket is None or not hasattr(socket, "default_value"):
            continue
        if blender_defaults is None:
            blender_defaults = _get_blender_socket_defaults(
                ctx.node_tree.bl_idname, node.bl_idname
            )
        value = socket.default_value
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
    if (
        spec.receiver_socket_type is not None
        and links[0].from_socket.type != spec.receiver_socket_type
    ):
        return None
    found = _find_cls(node.bl_idname)
    if found is not None:
        uncovered = set(_non_default_props(node, found[1])) - {
            key for key, _ in spec.require
        }
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


def _interface_items(node_tree, in_out: str):
    for item in node_tree.interface.items_tree:
        if hasattr(item, "socket_type") and item.in_out == in_out:
            yield item


def _emit_interface(item, direction: str, ctx: EmitContext) -> str:
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

        # 1. Build the node's value:
        #    emitter → socket method → lift → factory/constructor.
        val: _Val | None = None
        emitter = _EMITTERS.get(node.bl_idname)
        if emitter is not None:
            emitted = emitter(node, ctx)
            if emitted is not None:
                val = _Val(emitted)
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
                if strict:
                    raise CodegenError(
                        f"Cannot generate code: {message}. Register an emitter "
                        "with register_emitter() or pass strict=False."
                    )
                var = _make_var(node.bl_label or "node", ctx.counter)
                ctx.var_map[name] = _Val(Ref(var))
                body.append(f"    {var} = None  # TODO: {message}")
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
            body.extend(ctx.pending_lines)
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

        if len(out_links) == 1 and not group_outs:
            ctx.var_map[name] = val  # single consumer → inline
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
            source = _output_expr(val, node, link.from_socket)
            body.append(f"    {BinOp('>>', source, out_ref.require_expr()).render()}")
            consumed_out_links.add(id(link))
            continue

        var = _make_var(node.bl_label or "node", ctx.counter)
        body.append(f"    {var} = {val.require_expr().render()}")
        ctx.var_map[name] = _Val(
            Ref(var), is_socket=val.is_socket, socket_id=val.socket_id
        )

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
        out_lines.append(f"    {BinOp('>>', source, out_ref.require_expr()).render()}")

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
