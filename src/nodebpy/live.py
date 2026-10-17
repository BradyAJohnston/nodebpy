"""Re-run nodebpy source safely inside a live Blender session.

A live editor (a Text block, a file on disk) re-executes its code on every
change. Three things make a naive ``exec`` unpleasant, and :func:`run_source`
handles all of them:

- ``Custom*Group.create_group()`` reuses an existing group of the same
  ``_name`` rather than rebuilding it, so re-running edited class code would
  silently hand back the previous build. Existing groups the code claims are
  renamed out of the way first (:func:`stash_groups`), then their users are
  remapped onto the rebuilt trees and the old ones removed
  (:meth:`GroupStash.replace`); on failure the old names are put back
  (:meth:`GroupStash.restore`).
- Rebuilding a tree's interface regenerates its socket identifiers, which is
  what Geometry Nodes modifiers key their input values on, so the values
  would be lost. :func:`preserve_modifier_inputs` snapshots them by socket
  name and reapplies them afterwards.
- Blender deletes the keyframes and drivers of the nodes a rebuild removes,
  and modifier animation addresses inputs by socket identifier.
  :class:`NodeAnimation` moves node animation onto the matching nodes of the
  rebuild and :func:`preserve_modifier_inputs` renames the modifier paths.
- A rebuilt tree is arranged afresh, which would undo the layout edits made
  to the old one (moved, resized, collapsed, framed or relabelled nodes).
  They are carried over to the matching nodes of the rebuild
  (:mod:`nodebpy.layout.keep`), for ``clear=True`` trees and group classes
  alike.
- The tree the run produced has to be found among whatever the code did:
  the ``tree`` variable of the ``with g.tree(...) as tree:`` form, the newest
  top-level group it created, or the last group class it defined.
"""

from __future__ import annotations

import ast
import re
import warnings
from collections.abc import Iterable, Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from typing import Any, cast

import bpy

from .builder import TreeBuilder, default_keep_edits
from .layout import keep

__all__ = [
    "GroupStash",
    "NodeAnimation",
    "RunResult",
    "copy_asset",
    "group_names_in_source",
    "preserve_modifier_inputs",
    "run_source",
    "stash_groups",
]


def group_names_in_source(code: str) -> set[str]:
    """Literal ``_name`` values assigned in class bodies of ``code``.

    Parsed with :mod:`ast`; both ``_name = "..."`` and ``_name: str = "..."``
    count. Returns an empty set on a :class:`SyntaxError` (``exec`` reports
    it).
    """
    try:
        module = ast.parse(code)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                targets, value = stmt.targets, stmt.value
            elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None:
                targets, value = [stmt.target], stmt.value
            else:
                continue
            if not (isinstance(value, ast.Constant) and isinstance(value.value, str)):
                continue
            if any(isinstance(t, ast.Name) and t.id == "_name" for t in targets):
                names.add(value.value)
    return names


@dataclass
class GroupStash:
    """Existing node groups renamed out of the way before a run.

    Maps each original name to the old tree, now named ``<name>.stale``.
    """

    stashed: dict[str, bpy.types.NodeTree] = field(default_factory=dict)

    def restore(self) -> None:
        """Failure path: remove any partial build under an original name and
        give the old trees their names back. Empties the stash, so calling
        it (or :meth:`replace`) again is a no-op."""
        for name, old in self.stashed.items():
            leftover = bpy.data.node_groups.get(name)
            if leftover is not None and leftover != old:
                bpy.data.node_groups.remove(leftover)
            old.name = name
        self.stashed.clear()

    def keep_edits(self) -> None:
        """Carry the layout edits made to each old tree over to the tree the
        run built under its name (see :mod:`nodebpy.layout.keep`)."""
        for name, old in self.stashed.items():
            new = bpy.data.node_groups.get(name)
            if new is None or new == old or new.bl_idname != old.bl_idname:
                continue
            edits = keep.record(old)
            if edits is not None:
                keep.restore(edits, new)

    def replace(self) -> None:
        """Success path: for each name, if the run created a new tree of the
        same type under it, point the old tree's users (group nodes,
        modifiers, pinned editors) at the new one, carry its asset status
        over (:func:`copy_asset`) and remove the old; otherwise the old tree
        keeps its original name. Empties the stash, so calling it (or
        :meth:`restore`) again is a no-op."""
        for name, old in self.stashed.items():
            new = bpy.data.node_groups.get(name)
            if new is not None and new != old and new.bl_idname == old.bl_idname:
                copy_asset(old, new)
                NodeAnimation(old).restore(new)
                old.user_remap(new)
                bpy.data.node_groups.remove(old)
            else:
                old.name = name
        self.stashed.clear()


_ASSET_FIELDS = (
    "description",
    "author",
    "copyright",
    "license",
    "catalog_id",
    "use_preferred_import_method",
    "preferred_import_method",
)


def copy_asset(old: bpy.types.ID, new: bpy.types.ID) -> None:
    """Mark *new* as an asset as *old* is, with its metadata (description,
    author, copyright, license, catalog, tags, import method) and custom
    preview image. Does nothing if *old* is not an asset or *new* already
    is one, so a build that marks its own tree keeps its own metadata."""
    source = old.asset_data
    if source is None or new.asset_data is not None:
        return
    new.asset_mark()
    target = new.asset_data
    assert target is not None
    for name in _ASSET_FIELDS:
        with suppress(AttributeError, TypeError):  # absent in this Blender
            setattr(target, name, getattr(source, name))
    for tag in source.tags:
        target.tags.new(tag.name)
    preview = old.preview
    if preview is not None and preview.is_image_custom:
        copy = new.preview_ensure()
        assert copy is not None
        copy.image_size = preview.image_size
        copy.image_pixels_float = preview.image_pixels_float[:]


def stash_groups(names: Iterable[str]) -> GroupStash:
    """Rename each existing ``bpy.data.node_groups[name]`` to ``"<name>.stale"``
    and return the :class:`GroupStash` that undoes or completes the move.

    A group linked from a library (an appended asset) cannot be renamed and
    is left in place, so ``create_group()`` reuses it as usual.
    """
    stash = GroupStash()
    for name in names:
        if name in stash.stashed:
            continue
        existing = bpy.data.node_groups.get(name)
        if existing is not None and existing.library is None:
            existing.name = f"{name}.stale"
            stash.stashed[name] = existing
    return stash


def _copy_value(value: Any) -> Any:
    # Vector / colour values come back as bpy_prop_array views into the
    # modifier's storage, which the rebuild replaces; keep a plain tuple.
    if hasattr(value, "__len__") and not isinstance(value, (str, bytes, bpy.types.ID)):
        return tuple(value)
    return value


def _input_sockets(
    tree: bpy.types.NodeTree,
) -> dict[str, bpy.types.NodeTreeInterfaceSocket]:
    """Interface input sockets by name (first wins on duplicate names)."""
    sockets: dict[str, bpy.types.NodeTreeInterfaceSocket] = {}
    assert tree.interface is not None
    for item in tree.interface.items_tree:
        if item.item_type != "SOCKET":
            continue
        assert isinstance(item, bpy.types.NodeTreeInterfaceSocket)
        if item.in_out == "INPUT" and item.name not in sockets:
            sockets[item.name] = item
    return sockets


def _modifier_inputs(modifier: bpy.types.NodesModifier) -> Any:
    """``modifier.properties.inputs``: one RNA property per interface input,
    named by socket identifier, each wrapping the stored ``value`` (Blender
    5.x; the type stubs predate it)."""
    properties = cast("Any", modifier.properties)
    return properties.inputs


def _nodes_modifiers(pointers: set[int]) -> Iterator[bpy.types.NodesModifier]:
    for obj in bpy.data.objects:
        for modifier in obj.modifiers:
            if not isinstance(modifier, bpy.types.NodesModifier):
                continue
            group = modifier.node_group
            if group is not None and group.as_pointer() in pointers:
                yield modifier


# Per-input state a modifier stores besides ``value``: whether the input
# reads a named attribute instead (``type`` is ``VALUE`` or ``ATTRIBUTE``)
# and which one.
_INPUT_ATTRS = ("value", "type", "attribute_name")


@dataclass
class _InputState:
    socket_type: str
    identifier: str
    attrs: dict[str, Any]


@contextmanager
def preserve_modifier_inputs(trees: Iterable[bpy.types.NodeTree]) -> Iterator[None]:
    """Keep Geometry Nodes modifier input values across an interface rebuild.

    Snapshots the input state of every Geometry Nodes modifier (on any
    object) whose ``node_group`` is one of ``trees``, keyed by interface
    socket *name*: the value, and whether the input reads a named attribute
    instead (``type`` and ``attribute_name``). On exit — also when the body
    raised, so a failed in-place rebuild keeps the values of the sockets it
    did build — each entry whose socket name still exists on the modifier's
    (possibly rebuilt, possibly remapped) tree is reapplied; sockets whose
    type changed are skipped, as is anything that fails to apply — the
    reapply step never raises.

    Keyframes and drivers on those inputs are kept too: they address an
    input by its socket identifier, which a rebuild changes, so their paths
    are rewritten to the new identifier of the socket with the same name
    and type.
    """
    pointers = {tree.as_pointer() for tree in trees}
    snapshot: list[tuple[bpy.types.NodesModifier, dict[str, _InputState]]] = []
    for modifier in _nodes_modifiers(pointers):
        assert modifier.node_group is not None
        inputs = _modifier_inputs(modifier)
        values: dict[str, _InputState] = {}
        for name, socket in _input_sockets(modifier.node_group).items():
            wrapper = getattr(inputs, socket.identifier, None)
            if wrapper is None or not hasattr(wrapper, "value"):
                continue  # a geometry socket, or one with no stored value
            attrs = {
                attr: _copy_value(getattr(wrapper, attr))
                for attr in _INPUT_ATTRS
                if hasattr(wrapper, attr)
            }
            values[name] = _InputState(socket.socket_type, socket.identifier, attrs)
        snapshot.append((modifier, values))

    try:
        yield
    finally:
        for modifier, values in snapshot:
            # A modifier the run removed, a tree it freed, ...: never raise.
            with suppress(Exception):
                _reapply_inputs(modifier, values)


def _reapply_inputs(
    modifier: bpy.types.NodesModifier, values: dict[str, _InputState]
) -> None:
    group = modifier.node_group
    if group is None:
        return
    inputs = _modifier_inputs(modifier)
    sockets = _input_sockets(group)
    renamed: dict[str, str] = {}
    for name, state in values.items():
        socket = sockets.get(name)
        if socket is None or socket.socket_type != state.socket_type:
            continue
        if socket.identifier != state.identifier:
            renamed[state.identifier] = socket.identifier
        wrapper = getattr(inputs, socket.identifier, None)
        if wrapper is None or not hasattr(wrapper, "value"):
            continue
        for attr, value in state.attrs.items():
            with suppress(Exception):  # best effort, per attribute
                setattr(wrapper, attr, value)
    if renamed:
        _rename_input_paths(modifier, renamed)


def _fcurves(owner: bpy.types.ID) -> list[bpy.types.FCurve]:
    """The F-curves animating *owner*: those of its action and NLA strips
    (the channels of the slot each one uses) and its drivers."""
    animation = getattr(owner, "animation_data", None)
    if animation is None:
        return []
    actions = [(animation.action, animation.action_slot)]
    for track in animation.nla_tracks:
        actions.extend((strip.action, strip.action_slot) for strip in track.strips)
    curves: list[bpy.types.FCurve] = []
    for action, slot in actions:
        if action is None:
            continue
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    if slot is None or bag.slot_handle == slot.handle:
                        curves.extend(bag.fcurves)
    curves.extend(animation.drivers)
    return curves


def _rename_input_paths(
    modifier: bpy.types.NodesModifier, renamed: dict[str, str]
) -> None:
    """Point the animation of *modifier*'s inputs at their new identifiers
    (``modifiers["GN"].properties.inputs.Socket_1.value``, or the older
    ``modifiers["GN"]["Socket_1"]``), all at once so swapped identifiers
    don't collide."""
    prefix = re.escape(f'modifiers["{bpy.utils.escape_identifier(modifier.name)}"]')
    old = "|".join(re.escape(i) for i in sorted(renamed, key=len, reverse=True))
    pattern = re.compile(rf'^({prefix}(?:\.properties\.inputs\.|\["))({old})(?![0-9])')
    owner = modifier.id_data
    assert isinstance(owner, bpy.types.ID)
    for curve in _fcurves(owner):
        path = pattern.sub(lambda m: m[1] + renamed[m[2]], curve.data_path)
        if path != curve.data_path:
            curve.data_path = path


_NODE_PATH = re.compile(r'^nodes\["((?:[^"\\]|\\.)*)"\](.*)$', re.DOTALL)


@dataclass
class _NodeCurve:
    curve: bpy.types.FCurve
    node: str
    rest: str
    original: str
    driver: bool


class NodeAnimation:
    """Keyframes and drivers on a tree's nodes, kept through a rebuild.

    Blender deletes the animation of the nodes a rebuild removes, and a
    rebuild into a new tree starts with none. Made before the rebuild, this
    moves those curves out of the way (to a path that names no node); after
    it, :meth:`restore` points each at the node of the rebuilt tree that
    matches its old node (see :func:`nodebpy.layout.keep.match_nodes`),
    moving the action and drivers over first when the rebuild is a new
    tree. A curve whose node matches nothing, or whose property the new
    node lacks, gets its old path back and is named in a warning.
    """

    tree: bpy.types.NodeTree
    """The tree the animation was read from."""
    keys: dict[str, keep.Keys]
    """The match keys of that tree's nodes, by name."""

    def __init__(self, tree: bpy.types.NodeTree):
        self.tree = tree
        self.curves: list[_NodeCurve] = []
        drivers = set()
        if tree.animation_data is not None:
            drivers = {curve.as_pointer() for curve in tree.animation_data.drivers}
        for curve in _fcurves(tree):
            match = _NODE_PATH.match(curve.data_path)
            if match is None:
                continue
            name = match[1].replace('\\"', '"').replace("\\\\", "\\")
            self.curves.append(
                _NodeCurve(
                    curve,
                    name,
                    match[2],
                    curve.data_path,
                    curve.as_pointer() in drivers,
                )
            )
        self.keys = keep.node_keys(tree) if self.curves else {}
        for i, item in enumerate(self.curves):
            item.curve.data_path = f"nodebpy_kept[{i}]{item.rest}"

    def restore(self, tree: bpy.types.NodeTree | None = None) -> None:
        """Point the curves at the matching nodes of *tree*, the rebuild
        (default: the tree they were read from, rebuilt in place)."""
        if not self.curves:
            return
        tree = self.tree if tree is None else tree
        if tree != self.tree:
            self._move_to(tree)
        matched = keep.match_nodes(self.keys, tree)
        lost = []
        for item in self.curves:
            node = matched.get(item.node)
            path = None
            if node is not None:
                name = bpy.utils.escape_identifier(node.name)
                path = f'nodes["{name}"]{item.rest}'
                try:
                    tree.path_resolve(path)
                except ValueError:  # pragma: no cover - matched nodes share sockets
                    path = None
            if path is None:
                path = item.original
                lost.append(item.original)
            item.curve.data_path = path
        self.curves = []
        if lost:
            warnings.warn(
                f"Kept the animation of '{tree.name}' on the old paths, which "
                "no node of the rebuilt tree has: " + ", ".join(lost),
                stacklevel=2,
            )

    def _move_to(self, tree: bpy.types.NodeTree) -> None:
        source = self.tree.animation_data
        assert source is not None
        target = tree.animation_data_create()
        assert target is not None
        if target.action is None and source.action is not None:
            target.action = source.action
            target.action_slot = source.action_slot
        for item in self.curves:
            if item.driver:
                copy = target.drivers.from_existing(src_driver=item.curve)
                assert copy is not None
                item.curve = copy


@dataclass
class RunResult:
    """What :func:`run_source` produced."""

    tree: bpy.types.NodeTree | None
    """The tree the run produced, or ``None`` if it made no tree."""
    created: list[bpy.types.NodeTree]
    """Every node group that exists after the run and did not before."""
    namespace: dict[str, Any]
    """The globals the code ran in."""


def _is_group_class(value: Any, module_name: str | None) -> bool:
    return (
        isinstance(value, type)
        and getattr(value, "__module__", None) == module_name
        and callable(getattr(value, "create_group", None))
        and bool(getattr(value, "_name", None))
        and bool(getattr(value, "_tree_idname", None))
    )


def _produced_tree(
    namespace: dict[str, Any], before: set[int], prior: Any
) -> bpy.types.NodeTree | None:
    """The tree a run produced: the ``tree`` variable's, else the newest
    top-level group created, else the last group class defined (built now).

    ``before`` holds the ``session_uid`` of every group that existed before
    the run; ``prior`` is whatever ``tree`` was bound to before it (a value
    the caller's namespace carried over from an earlier run), which does not
    count as produced by this one."""
    bound = namespace.get("tree")
    if bound is not prior:
        if isinstance(bound, TreeBuilder):
            return bound.tree
        if isinstance(bound, bpy.types.NodeTree):
            return bound

    new_groups = [g for g in bpy.data.node_groups if g.session_uid not in before]
    if new_groups:
        nested = {
            sub.as_pointer()
            for group in new_groups
            for node in group.nodes
            if (sub := getattr(node, "node_tree", None)) is not None
        }
        top_level = [g for g in new_groups if g.as_pointer() not in nested]
        # bpy.data.node_groups is sorted by name; session_uid counts up with
        # creation, so it picks the group the code made last.
        return max(top_level or new_groups, key=lambda g: g.session_uid)

    module_name = namespace.get("__name__")
    for value in reversed(list(namespace.values())):
        if _is_group_class(value, module_name):
            tree = value.create_group()
            if isinstance(tree, bpy.types.NodeTree):
                return tree
    return None


def run_source(
    code: str,
    *,
    filename: str = "<nodebpy>",
    namespace: dict[str, Any] | None = None,
    keep_edits: bool = True,
) -> RunResult:
    """Execute nodebpy source for a live re-run.

    Existing groups the code's classes claim by ``_name`` are stashed so
    ``create_group()`` builds fresh, Geometry Nodes modifier input values on
    every pre-existing tree are preserved across the rebuild, and the
    stashed trees' users are remapped onto the new builds afterwards. On any
    exception the stash is restored and the exception re-raised unchanged;
    ``filename`` is what its traceback names. Nothing is printed or captured.

    Parameters
    ----------
    code
        The source to run.
    filename
        Filename for the compiled code, so tracebacks point at the caller's
        Text block or file.
    namespace
        Extra globals merged over the defaults (``__name__``, ``__file__``
        and ``bpy``). A ``tree`` it carries over from an earlier run's
        :attr:`RunResult.namespace` is not mistaken for this run's tree.
    keep_edits
        Carry the layout edits made to each rebuilt tree since it was last
        arranged over to its rebuild (see :mod:`nodebpy.layout.keep`).

    Notes
    -----
    A run that fails partway through a ``with g.tree(..., clear=True)`` body
    leaves that tree half built (the class form is atomic: the old build is
    restored). Groups the failed run created under other names are left
    behind as well.
    """
    stash = stash_groups(group_names_in_source(code))
    before = {group.session_uid for group in bpy.data.node_groups}
    globals_: dict[str, Any] = {
        "__name__": "__nodebpy_live__",
        "__file__": filename,
        "bpy": bpy,
    }
    if namespace:
        globals_.update(namespace)
    prior = globals_.get("tree")

    existing = list(bpy.data.node_groups)
    with preserve_modifier_inputs(existing), default_keep_edits(keep_edits):
        try:
            exec(compile(code, filename, "exec"), globals_)  # noqa: S102
            # Resolved before the stash is replaced: building a defined-only
            # class must not find the old tree back under its name.
            tree = _produced_tree(globals_, before, prior)
            if keep_edits:
                stash.keep_edits()
        except BaseException:
            stash.restore()
            raise
        # Inside the preserve context: remapping a modifier onto the rebuilt
        # tree resets its inputs just like an in-place rebuild does.
        stash.replace()

    created = [g for g in bpy.data.node_groups if g.session_uid not in before]
    return RunResult(tree=tree, created=created, namespace=globals_)
