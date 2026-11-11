from __future__ import annotations

import difflib
import keyword
import re
import unicodedata
import warnings
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, runtime_checkable

import bpy
from bpy.types import Node, NodeSocket

if TYPE_CHECKING:
    from ..types import SOCKET_TYPES


class SocketError(Exception):
    """Raised when a socket operation fails."""


class NodeUnavailableError(RuntimeError):
    """Raised for a node, or a node's input, that the running Blender lacks:
    the node classes are generated from a newer Blender than the one running."""


def _older_blender() -> bool:
    """Whether the running Blender is older than the node classes."""
    from ..nodes._blender import GENERATED_FOR

    return tuple(bpy.app.version[:2]) < GENERATED_FOR


def _needs_newer_blender(what: str) -> NodeUnavailableError:
    from ..nodes._blender import GENERATED_FOR

    return NodeUnavailableError(
        f"{what} is not in Blender {bpy.app.version_string}; this nodebpy is "
        f"generated from Blender {'.'.join(map(str, GENERATED_FOR))}."
    )


class OptionUnavailableError(NodeUnavailableError, TypeError):
    """Raised, on a Blender older than the node classes, for an enum option
    the running Blender lacks: a typo, or an option added since."""


class InvalidLinkWarning(UserWarning):
    """Emitted when a built tree holds links Blender can't evaluate."""


_ENUM_NOT_FOUND = re.compile(
    r'enum "(?P<value>[^"]*)" not found in \((?P<options>.*)\)'
)


def enum_value_error(error: TypeError, what: str) -> TypeError:
    """Blender's error for an unknown enum value, reworded to name ``what``
    and suggest the closest options (case aside: ``"add"`` suggests ``ADD``).
    Returns ``error`` itself when it is about something else."""
    match = _ENUM_NOT_FOUND.search(str(error))
    if match is None:
        return error
    value = match["value"]
    options = re.findall(r"'([^']*)'", match["options"])
    by_upper = {option.upper(): option for option in options}
    close = [
        by_upper[found]
        for found in difflib.get_close_matches(value.upper(), list(by_upper), n=3)
    ]
    if not options:
        # only a menu is ever empty: its items come from the Menu Switch it feeds
        return TypeError(
            f"{what} has no option {value!r}: it has no items yet. A menu input "
            "takes its items from the Menu Switch it is linked to; link it to one "
            f"with a {value!r} item."
        )
    hint = f" Did you mean {' or '.join(map(repr, close))}?" if close else ""
    message = f"{what} has no option {value!r}.{hint} Options: {', '.join(options)}."
    if _older_blender():
        from ..nodes._blender import GENERATED_FOR

        return OptionUnavailableError(
            f"{message} In Blender {bpy.app.version_string}, that is: it may be "
            f"new in Blender {'.'.join(map(str, GENERATED_FOR))}, which this "
            "nodebpy is generated from."
        )
    return TypeError(message)


# Type precedence for mixed-type operator dispatch (higher = dominant).
_TYPE_PRECEDENCE: dict[str, int] = {
    "INT": 0,
    "VALUE": 1,
    "FLOAT": 1,
    "VECTOR": 2,
}

GEO_NODE_NAMES = (
    f"GeometryNode{name}"
    for name in (
        "SetPosition",
        "TransformGeometry",
        "GroupInput",
        "GroupOutput",
        "MeshToPoints",
        "PointsToVertices",
    )
)


_NON_IDENTIFIER = re.compile(r"[^0-9a-z]+")


@cache
def normalize_name(name: str) -> str:
    """Convert 'Geometry' or 'My Socket' to a valid lower-case Python identifier
    ('geometry', 'my_socket'). Spaces, punctuation and other non-identifier
    characters (e.g. the '⟂'/'(' in 'BA⟂(BC)') collapse to underscores so the
    result is always usable as an attribute or parameter name. Accented
    letters fold to their ASCII base ('Bézier' → 'bezier') to match the
    generated method names."""
    text = "".join(
        c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c)
    ).lower()
    cleaned = _NON_IDENTIFIER.sub("_", text).strip("_")
    if cleaned and cleaned[0].isdigit():
        cleaned = "_" + cleaned
    if keyword.iskeyword(cleaned):
        cleaned += "_"
    return cleaned or "_"


def denormalize_name(attr_name: str) -> str:
    """Convert 'geometry' or 'my_socket' to 'Geometry' or 'My Socket'."""
    return attr_name.replace("_", " ").title()


def _socket_panels(sockets) -> dict[str, str]:
    """Socket identifier → name of the interface panel the group socket sits
    in (none at the top level). ``sockets`` are a group node's inputs or
    outputs; other socket-like objects have no panels."""
    node = getattr(sockets[0], "node", None) if sockets else None
    tree = getattr(node, "node_tree", None)
    if not isinstance(tree, bpy.types.NodeTree):
        return {}
    in_out = "OUTPUT" if sockets[0].is_output else "INPUT"
    return {
        item.identifier: item.parent.name
        for item in tree.interface.items_tree
        if item.item_type == "SOCKET" and item.in_out == in_out and item.parent
    }


def typed_param_names(sockets) -> dict[str, str]:
    """Socket identifier → ``__init__`` parameter name for a typed group class.

    The one place this mapping is defined: both the generated class's typed
    ``__init__`` (``nodebpy.assets``) and the call sites codegen emits for it
    (``nodebpy.export``) must agree, and they both derive it from the same
    live tree during a dump, and a group's ``i.<name>`` / ``o.<name>`` resolve
    through it. A socket's parameter is its normalized name. When several
    sockets normalize to the same name, one inside an interface panel
    is prefixed with the panel's name (Clump Hair Curves' two ``Seed`` inputs
    are ``seed`` and ``guide_map_seed``); those still colliding fall back to
    their normalized identifier. Residual collisions (or reserved names like
    ``self``) get a numeric suffix.

    ``sockets`` is any iterable of objects with ``name``/``identifier``
    (interface items or group-node sockets); ``__extend__`` virtual sockets
    are skipped.
    """
    real = [s for s in sockets if not s.identifier.startswith("__extend__")]
    from collections import Counter

    counts = Counter(normalize_name(s.name) for s in real)
    panels = _socket_panels(real)
    candidates = {}
    for s in real:
        name = normalize_name(s.name)
        if counts[name] > 1 and panels.get(s.identifier):
            name = normalize_name(f"{panels[s.identifier]} {s.name}")
        candidates[s.identifier] = name
    candidate_counts = Counter(candidates.values())
    reserved = {"self", "_named_links"}
    params: dict[str, str] = {}
    used: set[str] = set()
    for s in real:
        base = candidates[s.identifier]
        if candidate_counts[base] > 1:
            base = normalize_name(s.identifier)
        name, n = base, 1
        while name in used or name in reserved:
            n += 1
            name = f"{base}_{n}"
        used.add(name)
        params[s.identifier] = name
    return params


def socket_key(socket: NodeSocket) -> str:
    """A rebuild-stable key for a socket on its node: the socket name, plus
    ``#<n>`` for repeats (a Math node has two ``Value`` inputs).

    Socket *identifiers* are not stable across a dump → build round-trip:
    interface sockets and dynamic items (Index Switch, Capture Attribute, ...)
    get counter-based identifiers (``Socket_7``, ``Item_2``) that depend on
    the tree's full editing history, which a rebuild does not replay. Names
    and their in-node order are recreated exactly, so they are the currency
    layout snapshots and split records use."""
    node = socket.node
    assert node is not None
    collection = node.outputs if socket.is_output else node.inputs
    repeat = 0
    for other in collection:
        if other.identifier == socket.identifier:
            break
        if other.name == socket.name:
            repeat += 1
    return f"{socket.name}#{repeat}" if repeat else socket.name


type WarningPropagation = Literal["ALL", "ERRORS_AND_WARNINGS", "ERRORS", "NONE"]


def visible_socket_key(socket: NodeSocket) -> str:
    """The key :meth:`BaseNode.props` takes in ``hide_inputs`` /
    ``hide_outputs``: the socket name, plus ``#<n>`` for repeats among the
    node's *enabled* sockets on that side, so ``"Value#1"`` is a Math node's
    second visible ``Value`` input."""
    node = socket.node
    assert node is not None
    collection = node.outputs if socket.is_output else node.inputs
    repeat = 0
    for other in collection:
        if other.identifier == socket.identifier:
            break
        if other.enabled and other.name == socket.name:
            repeat += 1
    return f"{socket.name}#{repeat}" if repeat else socket.name


def _resolve_visible_socket(sockets, key: str, side: str, node: Node) -> NodeSocket:
    name, _, repeat = key.partition("#")
    index = int(repeat) if repeat.isdigit() else 0
    matches = [s for s in sockets if s.enabled and s.name == name]
    if index < len(matches):
        return matches[index]
    names = [visible_socket_key(s) for s in sockets if s.enabled]
    raise ValueError(
        f"{node.bl_idname} has no {side} socket {key!r}; its {side}s are {names}"
    )


def _parse_color(color: str | tuple[float, float, float]) -> tuple[float, float, float]:
    if isinstance(color, str):
        digits = color.removeprefix("#")
        if len(digits) != 6 or any(c not in "0123456789abcdefABCDEF" for c in digits):
            raise ValueError(f"Expected a hex colour like '#FFAA00', got {color!r}")
        r, g, b = (int(digits[i : i + 2], 16) / 255 for i in (0, 2, 4))
        return (r, g, b)
    if len(color) != 3:
        raise ValueError(f"Expected an (r, g, b) colour, got {color!r}")
    return (float(color[0]), float(color[1]), float(color[2]))


def apply_node_props(
    node: Node,
    *,
    label: str | None = None,
    color: str | tuple[float, float, float] | None = None,
    width: float | None = None,
    height: float | None = None,
    hide: bool | None = None,
    show_options: bool | None = None,
    hide_inputs: Iterable[str] = (),
    hide_outputs: Iterable[str] = (),
    mute: bool | None = None,
    warning_propagation: WarningPropagation | None = None,
    pin_gizmo: bool | None = None,
    pin_gizmo_inputs: Iterable[str] = (),
) -> None:
    """Set the properties every node has; ``None`` leaves one unchanged."""
    if label is not None:
        node.label = label
    if color is not None:
        node.use_custom_color = True
        node.color = _parse_color(color)
    if width is not None:
        node.width = width
    if height is not None:
        node.height = height
    if hide is not None:
        node.hide = hide
    if show_options is not None:
        node.show_options = show_options
    for key in hide_inputs:
        _resolve_visible_socket(node.inputs, key, "input", node).hide = True
    for key in hide_outputs:
        _resolve_visible_socket(node.outputs, key, "output", node).hide = True
    if mute is not None:
        node.mute = mute
    if warning_propagation is not None:
        node.warning_propagation = warning_propagation
    if pin_gizmo is not None:
        gizmo_socket(node).pin_gizmo = pin_gizmo
    for key in pin_gizmo_inputs:
        _resolve_visible_socket(node.inputs, key, "input", node).pin_gizmo = True


def gizmo_socket(node: Node) -> NodeSocket:
    """The socket whose ``pin_gizmo`` Blender reads for the node's own gizmo:
    a gizmo node's first input, or a value node's (Value, Vector, ...)
    output."""
    if node.bl_idname.startswith("GeometryNodeGizmo"):
        return node.inputs[0]
    if not node.outputs:
        raise ValueError(f"{node.bl_idname} has no gizmo to pin")
    return node.outputs[0]


def resolve_socket_key(sockets, key: str) -> NodeSocket | None:
    """Find the socket a :func:`socket_key` (or, for records written before
    keys existed, a raw identifier) refers to, or None."""
    name, _, repeat = key.partition("#")
    index = int(repeat) if repeat.isdigit() else 0
    seen = 0
    for socket in sockets:
        if socket.name == name:
            if seen == index:
                return socket
            seen += 1
    return next((s for s in sockets if s.identifier == key), None)


def _allow_innactive_sockets(node: bpy.types.Node) -> bool:
    """Returns True if we should allow inactive sockets to be linked for this node type"""
    return node.bl_idname in (
        "GeometryNodeIndexSwitch",
        "GeometryNodeMenuSwitch",
        "ShaderNodeMixShader",
        # "ShaderNodeMix",
        "GeometryNodeSwitch",
        # Group inputs that are only used behind an internal switch poll as
        # inactive until the group is evaluated — including the input we are
        # about to link, which would itself activate the socket.
        "GeometryNodeGroup",
        "ShaderNodeGroup",
        "CompositorNodeGroup",
    )


def _resolve_promotion(
    self_socket: NodeSocket, other: Any, reverse: bool
) -> tuple[NodeSocket, Any, bool]:
    """Determine the dominant socket for operator dispatch.

    When both operands have a socket type, the higher-precedence type wins.
    If `other` is dominant, the operands are swapped and `reverse` is flipped.

    Returns (dominant_socket, effective_other, effective_reverse).
    """
    other_type = _output_socket_type(other)
    self_prec = _TYPE_PRECEDENCE.get(self_socket.type, 1)
    other_prec = _TYPE_PRECEDENCE.get(other_type, -1) if other_type is not None else -1

    if other_prec > self_prec:
        # Other side is dominant — swap so the linker wraps the vector/higher socket
        if isinstance(other, NodeSocket):
            other_socket = other
        else:
            other_socket = other._default_output_socket
        return other_socket, self_socket, not reverse

    return self_socket, other, reverse


@runtime_checkable
class _NodeLike(Protocol):
    """Protocol for objects that wrap a Blender node and expose an ``o`` output accessor."""

    @property
    def o(self) -> Any: ...  # SocketAccessor at runtime; Any avoids a circular import


@runtime_checkable
class _SocketLike(Protocol):
    """Protocol for objects that wrap a single Blender NodeSocket and expose ``.socket``."""

    socket: NodeSocket


def _output_socket_type(value: Any) -> SOCKET_TYPES | None:
    """The Blender socket ``type`` of *value*'s default output socket.

    Resolves a raw ``NodeSocket`` or any socket/node wrapper to the type string
    Blender uses (e.g. ``"VECTOR"``, ``"VALUE"``). Returns ``None`` for plain
    Python values (ints, floats, tuples) that carry no socket type.
    """
    if isinstance(value, NodeSocket):
        return value.type  # type: ignore[return-value]
    if isinstance(value, (_SocketLike, _NodeLike)):
        return value._default_output_socket.type  # type: ignore[return-value]
    return None


_PACKAGE_DIR = str(Path(__file__).resolve().parents[1])


def _deprecated(old: str, new: str, *, removed_in: int) -> None:
    """Warn that ``old`` is deprecated in favour of ``new`` and is removed in
    nodebpy ``removed_in`` (the Blender line, e.g. ``540``). The warning
    points at the first frame outside nodebpy: the user's code."""
    warnings.warn(
        f"{old} is deprecated and will be removed in nodebpy {removed_in}; use {new}",
        DeprecationWarning,
        skip_file_prefixes=(_PACKAGE_DIR,),
    )
