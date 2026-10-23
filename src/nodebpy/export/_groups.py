"""Group classes that exist in Python already, for
``to_python(groups="reference")``.

A tree can use a group that a loaded class builds or links: one of Blender's
bundled assets (``g.Array``), one of nodebpy's own groups, a class from a
generated asset module or one the live script defines. Codegen can then call
that class instead of writing the group out again.

A tree belongs to a class when:

- an asset class linked it: the tree is linked from the class's library under
  the asset's name;
- it was appended from that library (the asset browser's default), which
  leaves a weak reference to the file and the asset's name;
- it is a local tree with the name the class gives its tree, which is the tree
  the class reuses when it runs. A tree changed by hand since nodebpy built
  it in this session is not matched, so the edits are written out.
"""

from __future__ import annotations

import importlib
import inspect
import os
import pkgutil
import sys
from collections.abc import Collection, Iterable, Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import bpy

from ..builder._utils import typed_param_names
from ..builder.asset import BundledLibrary, _AssetGroupMixin
from ..builder.node import NodeGroupBuilder

# Modules a script's own classes live in: run_source runs code as
# __nodebpy_live__, Blender runs scripts and Text blocks as __main__.
SCRIPT_MODULES = frozenset({"__main__", "__nodebpy_live__"})

# Modules holding nodebpy's own group classes, which nothing else imports.
_BUILTIN_MODULES = ("nodebpy.nodes.geometry.groups",)


@dataclass(frozen=True)
class Reference:
    """How codegen calls the class that builds a group node's tree."""

    cls: type[NodeGroupBuilder]
    params: dict[str, str] | None
    """Socket identifier → ``__init__`` parameter for a typed class, or
    ``None`` to pass inputs by socket name."""


def import_modules(names: Iterable[str]) -> None:
    """Import each module, and every submodule of a package, so the group
    classes they define can be found."""
    for name in names:
        module = importlib.import_module(name)
        if hasattr(module, "__path__"):
            for info in pkgutil.walk_packages(module.__path__, f"{name}."):
                importlib.import_module(info.name)


def configured_modules(start: str | Path | None = None) -> list[str]:
    """The package holding the dumped sources that ``[tool.nodebpy.assets]``
    names in the nearest ``pyproject.toml``, if it can be imported from a
    ``sys.path`` entry."""
    from ..assets._pipeline import load_config

    table, root = load_config(start)
    source = table.get("source")
    if not source or root is None:
        return []
    path = (root / source).resolve()
    names = []
    for entry in sys.path:
        try:
            parts = path.relative_to(Path(entry or ".").resolve()).parts
        except ValueError:
            continue
        if parts and all(part.isidentifier() for part in parts):
            names.append(".".join(parts))
    return [min(names, key=len)] if names else []


def _subclasses[T](cls: type[T]) -> Iterator[type[T]]:
    for sub in cls.__subclasses__():
        yield sub
        yield from _subclasses(sub)


def _group_classes() -> list[type[NodeGroupBuilder]]:
    import_modules(_BUILTIN_MODULES)
    return [
        cls
        for cls in dict.fromkeys(_subclasses(NodeGroupBuilder))
        if not inspect.isabstract(cls)
        and (getattr(cls, "_asset_name", None) or getattr(cls, "_name", None))
    ]


def _path(path: str) -> str:
    return os.path.normcase(os.path.realpath(bpy.path.abspath(path)))


def _from_library(cls: type[_AssetGroupMixin], path: str) -> bool:
    library = cls._library
    if isinstance(library, BundledLibrary):
        # Blender installs differ, the bundled file names don't.
        return os.path.basename(bpy.path.abspath(path)) == library.filename
    return _path(path) == _path(library.path())


def _builds(cls: type[NodeGroupBuilder], tree: bpy.types.NodeTree) -> bool:
    if cls._tree_idname != tree.bl_idname:
        return False
    if issubclass(cls, _AssetGroupMixin):
        name = cls._asset_name
        if tree.library is not None:
            return tree.name == name and _from_library(cls, tree.library.filepath)
        weak = tree.library_weak_reference
        if weak is not None:
            return weak.id_name[2:] == name and _from_library(cls, weak.filepath)
        return tree.name == name
    # A class choosing its tree's name per instance can't be matched by name.
    return (
        tree.library is None
        and cls._group_name is NodeGroupBuilder._group_name
        and tree.name == getattr(cls, "_name", None)
    )


def namespace_classes(
    namespace: Mapping[str, Any],
) -> dict[type[NodeGroupBuilder], str]:
    """The group classes bound in *namespace* (a script's globals), each with
    the name it is bound to there; a public name over a private one."""
    names: dict[type[NodeGroupBuilder], str] = {}
    for name, value in namespace.items():
        if not (isinstance(value, type) and issubclass(value, NodeGroupBuilder)):
            continue
        if value not in names or names[value].startswith("_"):
            names[value] = name
    return names


def tree_name(cls: type[NodeGroupBuilder]) -> str | None:
    """The name of the tree *cls* builds or links, if it doesn't choose one
    per instance."""
    if issubclass(cls, _AssetGroupMixin):
        return cls._asset_name
    if cls._group_name is not NodeGroupBuilder._group_name:
        return None
    return getattr(cls, "_name", None)


def find_class(
    tree: bpy.types.NodeTree, prefer: Collection[type] = ()
) -> type[NodeGroupBuilder] | None:
    """The loaded class that builds or links *tree*: one in *prefer* if any
    does, else the latest defined (a live script defines its classes again
    on every run, so older copies linger)."""
    from ..live import was_edited

    if tree.library is None and was_edited(tree):
        return None
    found = [cls for cls in _group_classes() if _builds(cls, tree)]
    preferred = [cls for cls in found if cls in prefer]
    return (preferred or found)[-1] if found else None


def reference(node: bpy.types.Node, prefer: Collection[type] = ()) -> Reference | None:
    """How to call the class that builds *node*'s group, or ``None`` when no
    loaded class does or its ``__init__`` can't take the node's inputs."""
    tree = getattr(node, "node_tree", None)
    cls = find_class(tree, prefer) if tree is not None else None
    if cls is None:
        return None
    if cls.__init__ is NodeGroupBuilder.__init__:
        return Reference(cls, None)
    parameters = list(inspect.signature(cls.__init__).parameters.values())[1:]
    named = {
        p.name: p
        for p in parameters
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    }
    if not named and any(p.kind is p.VAR_KEYWORD for p in parameters):
        # ``__init__(self, **kwargs)`` passes socket names through.
        return Reference(cls, None)
    params = typed_param_names(node.inputs)
    if not set(params.values()) <= named.keys() or any(
        p.default is p.empty for p in named.values()
    ):
        return None
    return Reference(cls, params)
