# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate Python code from a Blender node tree using nodebpy."""

from __future__ import annotations

import inspect

# ---------------------------------------------------------------------------
# Node registry — bl_idname → (module_alias, class_name)
# ---------------------------------------------------------------------------

_NODE_REGISTRY: dict[str, tuple[str, str]] | None = None

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

_SKIP_BL_IDNAMES = frozenset({"NodeGroupInput", "NodeGroupOutput", "NodeReroute"})

# ---------------------------------------------------------------------------
# Phase 3: operator lifting
# ---------------------------------------------------------------------------

_OP_PREC: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "**": 3}


def _maybe_parens(
    expr: str, expr_op: str | None, ctx_op: str, is_rhs: bool = False
) -> str:
    """Wrap expr in parentheses only when strictly required by operator precedence.

    is_rhs: True when expr is the right-hand operand.  Right operands at equal
    precedence need parens for non-commutative operators (-, /, **).
    """
    if expr_op is None:
        return expr  # atomic — never needs parens
    ip = _OP_PREC.get(expr_op, 0)
    cp = _OP_PREC.get(ctx_op, 0)
    if cp > ip:
        return f"({expr})"
    if cp == ip:
        # Right side of non-commutative / right-associative ops
        if is_rhs and ctx_op in ("-", "/", "%"):
            return f"({expr})"
        # Left side of right-associative ** (a**b)**c → always needs parens)
        if not is_rhs and ctx_op == "**":
            return f"({expr})"
    return expr


_LIFTABLE_BINARY: dict[str, dict[str, str]] = {
    "ShaderNodeMath": {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "POWER": "**",
        "MODULO": "%",
    },
    "ShaderNodeVectorMath": {
        "ADD": "+",
        "SUBTRACT": "-",
        "MULTIPLY": "*",
        "DIVIDE": "/",
        "SCALE": "*",
    },
}


def _lift_op(node) -> str | None:
    """Return the Python binary operator for this node's operation, or None."""
    m = _LIFTABLE_BINARY.get(node.bl_idname)
    return m.get(getattr(node, "operation", "")) if m else None


def _lift_pair(node):
    """Return (lhs_socket, rhs_socket) for the two operand sockets, or None."""
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


def _operand_ref(socket, node, node_tree, var_map) -> str | None:
    """Expression for a socket: upstream var/expr reference or formatted literal."""
    if socket.is_linked:
        for link in node_tree.links:
            if (
                link.to_node.name == node.name
                and link.to_socket.identifier == socket.identifier
            ):
                return _upstream_ref(
                    link.from_node, link.from_socket, node_tree, var_map
                )
        return None
    if hasattr(socket, "default_value"):
        return _fmt(socket.default_value)
    return None


def _try_lift_node(node, node_tree, var_map) -> str | None:
    """Try to build a lifted operator expression for a liftable node.

    Only lifts when at least one input socket is linked (pure-literal nodes
    stay as function calls). Returns the expression string or None.
    """
    op = _lift_op(node)
    if op is None:
        return None
    pair = _lift_pair(node)
    if pair is None:
        return None
    lhs_s, rhs_s = pair
    if not (lhs_s.is_linked or rhs_s.is_linked):
        return None
    lhs = _operand_ref(lhs_s, node, node_tree, var_map)
    rhs = _operand_ref(rhs_s, node, node_tree, var_map)
    if lhs is None or rhs is None:
        return None
    return f"{lhs} {op} {rhs}"


_BLENDER_SOCKET_DEFAULTS: dict[str, dict[str, object]] = {}


def _get_blender_socket_defaults(node_tree, bl_idname: str) -> dict[str, object]:
    """Return a dict of socket identifier → default value for a fresh node of this type.

    Results are cached per bl_idname to avoid repeated temporary-node creation.
    """
    if bl_idname in _BLENDER_SOCKET_DEFAULTS:
        return _BLENDER_SOCKET_DEFAULTS[bl_idname]
    defaults: dict[str, object] = {}
    try:
        tmp = node_tree.nodes.new(bl_idname)
        for s in tmp.inputs:
            if hasattr(s, "default_value"):
                try:
                    val = s.default_value
                    try:
                        defaults[s.identifier] = tuple(val)
                    except TypeError:
                        defaults[s.identifier] = val
                except Exception:
                    pass
        node_tree.nodes.remove(tmp)
    except Exception:
        pass
    _BLENDER_SOCKET_DEFAULTS[bl_idname] = defaults
    return defaults


def _all_subclasses(cls):
    for sub in cls.__subclasses__():
        yield sub
        yield from _all_subclasses(sub)


def _get_node_registry() -> dict[str, tuple[str, str]]:
    """Lazily build and return the bl_idname → (alias, class_name) registry."""
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
                _NODE_REGISTRY[bl_id] = (alias, cls.__name__)
                break
    return _NODE_REGISTRY


def _find_cls(bl_idname: str):
    """Return (alias, class) for a bl_idname, or None."""
    registry = _get_node_registry()
    entry = registry.get(bl_idname)
    if entry is None:
        return None
    alias, class_name = entry
    from .builder.node import BaseNode

    for cls in _all_subclasses(BaseNode):
        if cls.__name__ == class_name and getattr(cls, "_bl_idname", None) == bl_idname:
            return alias, cls
    return None


# ---------------------------------------------------------------------------
# Name utilities
# ---------------------------------------------------------------------------


def _normalize(name: str) -> str:
    from .builder._utils import normalize_name

    return normalize_name(name)


def _make_var(label: str, counter: dict[str, int]) -> str:
    """Return a unique snake_case variable name for a node label."""
    base = _normalize(label)
    if not base:
        base = "node"
    if base not in counter:
        counter[base] = 0
        return base
    counter[base] += 1
    return f"{base}_{counter[base]}"


# ---------------------------------------------------------------------------
# Value formatting
# ---------------------------------------------------------------------------


def _fmt(value) -> str:
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


def _eq(a, b) -> bool:
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


def _is_zero(val) -> bool:
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
# Graph utilities
# ---------------------------------------------------------------------------


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


def _trace_reroute(node, socket, node_tree):
    """Follow a reroute chain backward to the real source node and socket."""
    visited = set()
    while node.bl_idname == "NodeReroute" and node.name not in visited:
        visited.add(node.name)
        upstream = [l for l in node_tree.links if l.to_node.name == node.name]
        if not upstream:
            break
        node = upstream[0].from_node
        socket = upstream[0].from_socket
    return node, socket


# ---------------------------------------------------------------------------
# Phase 2: Chain detection
# ---------------------------------------------------------------------------


def _build_chain_data(node_tree):
    """Identify chain-eligible edges and which nodes can be emitted inline.

    A chain-eligible edge A→B requires:
    1. link.from_socket is A.outputs[0]
    2. link.to_socket is B.inputs[0]
    3. A.outputs[0] has exactly one outgoing link (no fan-out)

    An inline node has total outgoing link count == 1.

    Returns:
        chain_prev: node_name → (from_key, to_socket_identifier)
        chain_next: from_key → (to_key, to_socket_identifier)
        inline_nodes: set of node names with total outgoing count == 1
    """
    socket_out: dict[tuple[str, str], int] = {}
    node_out: dict[str, int] = {}

    for link in node_tree.links:
        sk = (link.from_node.name, link.from_socket.identifier)
        socket_out[sk] = socket_out.get(sk, 0) + 1
        node_out[link.from_node.name] = node_out.get(link.from_node.name, 0) + 1

    chain_prev: dict[str, tuple[str, str]] = {}
    chain_next: dict[str, tuple[str, str]] = {}

    for link in node_tree.links:
        fn, tn = link.from_node, link.to_node
        fs, ts = link.from_socket, link.to_socket

        if fn.bl_idname == "NodeReroute" or tn.bl_idname == "NodeReroute":
            continue

        # Condition 1: from_socket must be first output
        if fn.bl_idname == "NodeGroupInput":
            from_is_first = True
        elif fn.outputs and fs.identifier == fn.outputs[0].identifier:
            from_is_first = True
        else:
            from_is_first = False

        if not from_is_first:
            continue

        # Condition 2: to_socket must be first input
        if tn.bl_idname == "NodeGroupOutput":
            to_is_first = True
        elif tn.inputs and ts.identifier == tn.inputs[0].identifier:
            to_is_first = True
        else:
            to_is_first = False

        if not to_is_first:
            continue

        # Condition 3: from_socket has exactly one outgoing link
        if socket_out.get((fn.name, fs.identifier), 0) != 1:
            continue

        from_key = (
            f"_iface_inputs_{fs.identifier}"
            if fn.bl_idname == "NodeGroupInput"
            else fn.name
        )
        to_key = (
            f"_iface_outputs_{ts.identifier}"
            if tn.bl_idname == "NodeGroupOutput"
            else tn.name
        )

        chain_prev[to_key] = (from_key, ts.identifier)
        chain_next[from_key] = (to_key, ts.identifier)

    inline_nodes = {
        name
        for name, count in node_out.items()
        if count == 1 and name not in ("Group Input", "Group Output")
    }

    return chain_prev, chain_next, inline_nodes


def _find_chains(
    chain_prev: dict,
    chain_next: dict,
    inline_nodes: set,
    min_chain_length: int,
) -> list[list[str]]:
    """Find maximal chains where all interior regular nodes are inline-eligible.

    A chain is a sequence of keys [start, n1, ..., nk, (iface_out?)] where:
    - start is an iface-input key or regular node name with no chain predecessor
    - All interior regular nodes (n1...n_{k-1}) are in inline_nodes
    - Length >= min_chain_length
    """
    visited: set[str] = set()
    chains: list[list[str]] = []

    for start_key in list(chain_next.keys()):
        if start_key in visited:
            continue
        # Chain heads: not a regular-node that itself has a chain predecessor
        if not start_key.startswith("_iface_inputs_") and start_key in chain_prev:
            continue

        # Follow chain_next to build the maximal chain
        chain = [start_key]
        current = start_key
        while current in chain_next:
            next_key, _ = chain_next[current]
            if next_key in visited:
                break
            chain.append(next_key)
            visited.add(next_key)
            if next_key.startswith("_iface_outputs_"):
                break
            current = next_key

        visited.add(start_key)

        if len(chain) < min_chain_length:
            continue

        # Check that all interior regular nodes are inline-eligible
        regular_nodes = [k for k in chain if not k.startswith("_iface_")]
        if start_key.startswith("_iface_inputs_"):
            interior = regular_nodes[:-1]  # All except tail are interior
        else:
            interior = regular_nodes[
                1:-1
            ]  # Skip head; all except head and tail are interior

        if all(n in inline_nodes for n in interior):
            chains.append(chain)

    return chains


# ---------------------------------------------------------------------------
# Interface codegen
# ---------------------------------------------------------------------------


def _interface_items(node_tree):
    """Yield interface items that are sockets (not panels)."""
    for item in node_tree.interface.items_tree:
        if hasattr(item, "socket_type"):
            yield item


def _emit_interface(item, direction: str, var_map: dict, counter: dict) -> str:
    """Generate a single tree.inputs.*() or tree.outputs.*() assignment line."""
    method = _INTERFACE_TYPE_METHOD.get(item.socket_type, "geometry")
    var_name = _make_var(_normalize(item.name), counter)
    var_map[f"_iface_{direction}_{item.identifier}"] = var_name

    args: list[str] = [_fmt(item.name)]

    if direction == "inputs" and item.socket_type not in _NO_DEFAULT_VALUE_TYPES:
        try:
            dv = item.default_value
            args.append(_fmt(dv))
        except Exception:
            pass

    return f"    {var_name} = tree.{direction}.{method}({', '.join(args)})"


# ---------------------------------------------------------------------------
# Node codegen helpers
# ---------------------------------------------------------------------------


def _get_props(node, cls) -> dict:
    """Return keyword-only property values that differ from constructor defaults."""
    try:
        sig = inspect.signature(cls.__init__)
    except Exception:
        return {}
    result: dict = {}
    for name, param in sig.parameters.items():
        if name == "self" or param.kind != inspect.Parameter.KEYWORD_ONLY:
            continue
        if param.default is inspect.Parameter.empty:
            continue
        try:
            current = getattr(node, name)
            if current != param.default:
                result[name] = current
        except AttributeError:
            pass
    return result


def _strip_outer_parens(s: str) -> str:
    """Remove one layer of surrounding parentheses if they span the whole string."""
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth = 0
    for i, c in enumerate(s):
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if depth == 0 and i < len(s) - 1:
            return s  # parens close before end — they don't wrap the whole expression
    return s[1:-1]


def _upstream_ref(from_node, from_socket, node_tree, var_map: dict) -> str | None:
    """Return Python expression referencing an upstream output socket."""
    from_node, from_socket = _trace_reroute(from_node, from_socket, node_tree)

    if from_node.bl_idname == "NodeGroupInput":
        return var_map.get(f"_iface_inputs_{from_socket.identifier}")

    var = var_map.get(from_node.name)
    if not var:
        return None

    if from_node.outputs and from_node.outputs[0].identifier == from_socket.identifier:
        return var
    return f"{var}.o.{_normalize(from_socket.name)}"


def _node_kwargs(
    node, node_tree, var_map, skip_input_id: str | None = None
) -> list[str]:
    """Build the constructor kwarg strings for a node.

    skip_input_id: socket identifier to omit (the chain-link input).
    """
    result = _find_cls(node.bl_idname)
    if result is None:
        return []
    _, cls = result

    kwargs: dict[str, str] = {}
    for link in node_tree.links:
        if link.to_node.name != node.name:
            continue
        if skip_input_id and link.to_socket.identifier == skip_input_id:
            continue
        ref = _upstream_ref(link.from_node, link.from_socket, node_tree, var_map)
        if ref is None:
            continue
        kwarg_name = _normalize(link.to_socket.identifier)
        # Keyword argument values don't need outer parens — Python's parser
        # handles operator precedence inside `key=expr` unambiguously.
        kwargs[kwarg_name] = _strip_outer_parens(ref)

    try:
        sig = inspect.signature(cls.__init__)
    except Exception:
        sig = None

    positional_params: list[tuple[str, inspect.Parameter]] = []
    if sig:
        positional_params = [
            (n, p)
            for n, p in sig.parameters.items()
            if n != "self" and p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]

    blender_defaults: dict[str, object] | None = None

    for i, socket in enumerate(node.inputs):
        if socket.is_linked:
            continue
        if skip_input_id and socket.identifier == skip_input_id:
            continue
        if not hasattr(socket, "default_value"):
            continue
        kwarg_name = _normalize(socket.identifier)
        if kwarg_name in kwargs:
            continue
        try:
            val = socket.default_value
            default: object = inspect.Parameter.empty
            if sig and kwarg_name in sig.parameters:
                default = sig.parameters[kwarg_name].default
            elif i < len(positional_params):
                default = positional_params[i][1].default

            if default is not inspect.Parameter.empty and default is not None:
                if _eq(val, default):
                    continue
            else:
                # Python default is None (optional socket param) — compare against
                # Blender's actual socket default for a freshly-created node.
                if blender_defaults is None:
                    blender_defaults = _get_blender_socket_defaults(
                        node_tree, node.bl_idname
                    )
                blender_default = blender_defaults.get(socket.identifier)
                if blender_default is not None:
                    if _eq(val, blender_default):
                        continue
                else:
                    if _is_zero(val):
                        continue
            kwargs[kwarg_name] = _fmt(val)
        except Exception:
            pass

    props = _get_props(node, cls)
    parts = [f"{k}={v}" for k, v in kwargs.items()]
    parts += [f"{k}={_fmt(v)}" for k, v in props.items()]
    return parts


def _node_call_str(node, node_tree, var_map, skip_input_id: str | None = None) -> str:
    """Return just 'alias.ClassName(kwargs)' — no variable assignment."""
    result = _find_cls(node.bl_idname)
    if result is None:
        return f"# Unknown node: {node.bl_idname}"
    alias, cls = result
    parts = _node_kwargs(node, node_tree, var_map, skip_input_id=skip_input_id)
    return f"{alias}.{cls.__name__}({', '.join(parts)})"


def _emit_node(node, var_map: dict, counter: dict, node_tree) -> list[str]:
    """Generate a standalone variable assignment for a node (Phase 1 style)."""
    registry = _get_node_registry()

    if node.bl_idname not in registry:
        var = _make_var(node.bl_label or "node", counter)
        var_map[node.name] = var
        return [f"    # Unknown node: {node.bl_idname}"]

    result = _find_cls(node.bl_idname)
    if result is None:
        var = _make_var(node.bl_label or "node", counter)
        var_map[node.name] = var
        return [f"    # Unknown node class: {node.bl_idname}"]

    var = _make_var(node.bl_label, counter)
    var_map[node.name] = var
    call = _node_call_str(node, node_tree, var_map)
    return [f"    {var} = {call}"]


# ---------------------------------------------------------------------------
# Phase 2: chain expression emission
# ---------------------------------------------------------------------------


def _emit_chain(
    chain: list[str],
    tail_node,
    var_map: dict,
    counter: dict,
    node_tree,
    inline_nodes: set,
    chain_prev: dict,
) -> list[str]:
    """Emit a chain expression, assigning a variable to the tail if needed.

    chain: sequence of keys [start_key, ..., (iface_out_key?)]
    tail_node: the bpy node for the last regular node in the chain
    """
    nodes_by_name = {n.name: n for n in node_tree.nodes}
    start_key = chain[0]

    start_ref = var_map.get(start_key, "# missing")
    parts: list[str] = [start_ref]

    regular_nodes = [k for k in chain if not k.startswith("_iface_")]
    if start_key.startswith("_iface_inputs_"):
        chain_members = regular_nodes
    else:
        chain_members = regular_nodes[1:]

    for node_name in chain_members:
        node = nodes_by_name.get(node_name)
        if node is None:
            parts.append(f"# missing_node:{node_name}")
            continue
        prev_entry = chain_prev.get(node_name)
        skip_input_id = prev_entry[1] if prev_entry else None

        op = _lift_op(node)
        if op is not None:
            pair = _lift_pair(node)
            if pair is not None:
                lhs_s, rhs_s = pair
                if skip_input_id == lhs_s.identifier:
                    rhs = _operand_ref(rhs_s, node, node_tree, var_map)
                    if rhs is not None:
                        lhs = parts.pop()
                        parts.append(f"({lhs} {op} {rhs})")
                        continue
                elif skip_input_id == rhs_s.identifier:
                    lhs_ref = _operand_ref(lhs_s, node, node_tree, var_map)
                    if lhs_ref is not None:
                        accumulated = parts.pop()
                        parts.append(f"({lhs_ref} {op} {accumulated})")
                        continue

        call = _node_call_str(node, node_tree, var_map, skip_input_id=skip_input_id)
        parts.append(call)

    last_key = chain[-1]
    if last_key.startswith("_iface_outputs_"):
        iface_ref = var_map.get(last_key, "# missing_iface_output")
        parts.append(iface_ref)

    expr = " >> ".join(parts)

    tail_needs_var = tail_node.name not in inline_nodes
    if tail_needs_var:
        var = _make_var(tail_node.bl_label, counter)
        var_map[tail_node.name] = var
        return [f"    {var} = {expr}"]
    else:
        return [f"    {expr}"]


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def to_python(tree, min_chain_length: int = 3) -> str:
    """Generate Python code that recreates the given node tree using nodebpy.

    Args:
        tree: A ``TreeBuilder`` instance or ``bpy.types.NodeTree``.
        min_chain_length: Minimum number of items (including interface endpoints)
            for a linear pipeline to be expressed with ``>>`` syntax.

    Returns:
        Python source code as a string.
    """
    node_tree = tree.tree if hasattr(tree, "tree") else tree

    ordered = _topo_sort(node_tree)
    var_map: dict[str, str] = {}
    counter: dict[str, int] = {}

    # Build chain data
    chain_prev, chain_next, inline_nodes = _build_chain_data(node_tree)
    chains = _find_chains(chain_prev, chain_next, inline_nodes, min_chain_length)

    # Determine inline chain members and where to emit chain expressions
    inline_chain_members: set[str] = set()
    chain_tails: dict[str, list[str]] = {}  # tail_node_name → chain sequence

    for chain in chains:
        regular_nodes = [k for k in chain if not k.startswith("_iface_")]
        if not regular_nodes:
            continue
        start_key = chain[0]
        tail = regular_nodes[-1]

        if start_key.startswith("_iface_inputs_"):
            interior = regular_nodes[:-1]
        else:
            interior = regular_nodes[1:-1]

        # Only include chains whose interior nodes are all inline-eligible
        if not all(n in inline_nodes for n in interior):
            continue

        for n in interior:
            inline_chain_members.add(n)
        chain_tails[tail] = chain

    # Build output
    lines = ["from nodebpy import geometry as g, TreeBuilder", ""]
    lines.append(f'with TreeBuilder("{node_tree.name}") as tree:')

    input_items = [i for i in _interface_items(node_tree) if i.in_out == "INPUT"]
    output_items = [i for i in _interface_items(node_tree) if i.in_out == "OUTPUT"]

    for item in input_items:
        lines.append(_emit_interface(item, "inputs", var_map, counter))
    for item in output_items:
        lines.append(_emit_interface(item, "outputs", var_map, counter))
    if input_items or output_items:
        lines.append("")

    # Track output connections that are already expressed inside a chain
    handled_output_links: set[tuple[str, str]] = set()

    for node in ordered:
        if node.bl_idname in _SKIP_BL_IDNAMES:
            continue

        if node.name in inline_chain_members:
            # Emitted inline — skip standalone code; no var_map entry needed
            continue

        if node.name in chain_tails:
            chain_lines = _emit_chain(
                chain_tails[node.name],
                node,
                var_map,
                counter,
                node_tree,
                inline_nodes,
                chain_prev,
            )
            lines.extend(chain_lines)

            # Mark interface output links that are part of this chain as handled
            last_key = chain_tails[node.name][-1]
            if last_key.startswith("_iface_outputs_"):
                for link in node_tree.links:
                    if (
                        link.from_node.name == node.name
                        and link.to_node.bl_idname == "NodeGroupOutput"
                        and f"_iface_outputs_{link.to_socket.identifier}" == last_key
                    ):
                        handled_output_links.add((node.name, link.to_socket.identifier))
            continue

        # Phase 3: operator lifting for non-chain nodes
        lift_expr = _try_lift_node(node, node_tree, var_map)
        if lift_expr is not None:
            if node.name in inline_nodes:
                # Used exactly once — inline the expression (with parens) as a ref
                var_map[node.name] = f"({lift_expr})"
            else:
                # Fan-out — assign to a named variable
                var = _make_var(node.bl_label, counter)
                var_map[node.name] = var
                lines.append(f"    {var} = {lift_expr}")
            continue

        lines.extend(_emit_node(node, var_map, counter, node_tree))

    # Emit remaining output connections (not handled by chains)
    out_lines: list[str] = []
    for link in node_tree.links:
        if link.to_node.bl_idname != "NodeGroupOutput":
            continue
        if (link.from_node.name, link.to_socket.identifier) in handled_output_links:
            continue
        ref = _upstream_ref(link.from_node, link.from_socket, node_tree, var_map)
        if ref is None:
            continue
        out_key = f"_iface_outputs_{link.to_socket.identifier}"
        out_var = var_map.get(out_key)
        if out_var:
            out_lines.append(f"    {ref} >> {out_var}")

    if out_lines:
        lines.append("")
        lines.extend(out_lines)

    return "\n".join(lines)
