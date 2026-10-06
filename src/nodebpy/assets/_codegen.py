"""Generate typed ``nodebpy`` API classes for node-group assets.

Given one or more asset ``.blend`` libraries, :func:`generate_asset_api` appends
each node group, introspects its interface, and writes a Python module of typed
:class:`~nodebpy.builder.AssetNodeGroup` subclasses — so an asset reads and
type-checks like any other node. The emitted classes append the asset at runtime
rather than rebuilding it.

This is a *shipped*, reusable tool: other projects call it on their own asset
libraries (via :class:`~nodebpy.builder.PackageLibrary`) to generate APIs for
their assets.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import bpy

from ..builder import AssetLibrary, BundledLibrary, PackageLibrary, asset_group_base
from ..builder._utils import typed_param_names
from ..export.codegen import GroupInterface, _fmt
from ..types import Default

# bl_socket_type substring → (Socket accessor class, Input* parameter type).
# Order matters: more specific keys (IntVector before Int) come first.
_SOCKET_TYPES: dict[str, tuple[str, str]] = {
    "NodeSocketFloat": ("FloatSocket", "InputFloat"),
    "NodeSocketIntVector": ("IntegerVectorSocket", "InputIntegerVector"),
    "NodeSocketInt": ("IntegerSocket", "InputInteger"),
    "NodeSocketBool": ("BooleanSocket", "InputBoolean"),
    "NodeSocketVector": ("VectorSocket", "InputVector"),
    "NodeSocketColor": ("ColorSocket", "InputColor"),
    "NodeSocketRotation": ("RotationSocket", "InputRotation"),
    "NodeSocketMatrix": ("MatrixSocket", "InputMatrix"),
    "NodeSocketString": ("StringSocket", "InputString"),
    "NodeSocketMenu": ("MenuSocket", "InputMenu"),
    "NodeSocketGeometry": ("GeometrySocket", "InputGeometry"),
    "NodeSocketObject": ("ObjectSocket", "InputObject"),
    "NodeSocketMaterial": ("MaterialSocket", "InputMaterial"),
    "NodeSocketImage": ("ImageSocket", "InputImage"),
    "NodeSocketCollection": ("CollectionSocket", "InputCollection"),
    "NodeSocketBundle": ("BundleSocket", "InputBundle"),
    "NodeSocketClosure": ("ClosureSocket", "InputClosure"),
    "NodeSocketShader": ("ShaderSocket", "InputShader"),
    "NodeSocketFont": ("FontSocket", "InputFont"),
    "NodeSocketSound": ("SoundSocket", "InputSound"),
    "NodeSocketVirtual": ("Socket", "InputLinkable"),
}


# Tree type → module name used when splitting generated output per tree type.
_TREE_MODULES: dict[str, str] = {
    "GeometryNodeTree": "geometry",
    "ShaderNodeTree": "shader",
    "CompositorNodeTree": "compositor",
}


def _socket_types(bl_socket_type: str) -> tuple[str, str]:
    for key, value in _SOCKET_TYPES.items():
        if key in bl_socket_type:
            return value
    return ("Socket", "InputLinkable")


def _class_name(name: str) -> str:
    """A valid, readable Python class name for an asset group display name."""
    cleaned = "".join(c if c.isalnum() or c.isspace() else " " for c in name)
    parts = cleaned.split()
    cleaned = "".join(p[:1].upper() + p[1:] for p in parts)
    if cleaned and cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned or "AssetGroup"


def _format_default(socket: bpy.types.NodeSocket) -> str:
    """Source for a socket's scalar default value, or ``None``.

    Only plain scalars are emitted as parameter defaults. Vector/colour/matrix
    defaults vary in arity (2D UVs, 3D vectors, 4-component colours) and don't
    always fit the parameter's ``Input*`` type, so they're left as ``None`` —
    the appended group keeps its own socket default regardless.
    """
    value = getattr(socket, "default_value", None)
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # The exact float32 round-trip formatter (which also folds pi/tau/e
        # constants): a lossy default here would *change* the socket value on
        # every instantiation, since the typed __init__ always passes it.
        return _fmt(value)
    if isinstance(value, str):
        return repr(value)
    return "None"


def _clean_doc(text: str) -> str:
    """Make ``text`` safe to drop inside a ``\"\"\"…\"\"\"`` docstring."""
    text = " ".join(text.split())
    text = text.replace('"""', "'''")
    return text.rstrip("\\").rstrip()


def _quote(text: str) -> str:
    """``text`` as a double-quoted Python string literal."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _menu_items(socket) -> tuple[str, ...]:
    """The items a menu socket accepts, in order.

    A menu socket's items come from the Menu Switch node that defines them and
    aren't readable from the socket's RNA enum, but assigning an impossible
    value makes Blender list them in the ``TypeError`` — the same trick as
    ``gen.introspect._collect_socket_menu_items`` (duplicated rather than
    imported, since ``gen`` is a build tool and isn't shipped with the package).
    """
    if getattr(socket, "type", "") != "MENU" or not socket.default_value:
        return ()
    try:
        socket.default_value = "X" * 100
    except TypeError as error:
        _, _, listed = str(error).partition("not found in ")
        items = (item.strip("()'\" ") for item in listed.split(", "))
        return tuple(item for item in items if item)
    # A menu that accepted the impossible value tells us nothing about its items.
    return ()


@dataclass
class _Socket:
    name: str
    identifier: str
    socket_class: str  # e.g. "GeometrySocket"
    input_type: str  # e.g. "InputGeometry"
    default: str  # source for the default value
    attr: str  # normalized accessor/param name
    description: str = ""  # interface tooltip, if the asset author set one
    menu_items: tuple[str, ...] = ()  # menu sockets only: the selectable items
    fallback: str = ""  # what an unconnected input reads, for the docstring
    modifier_attribute: str = ""  # attribute a modifier input defaults to reading

    @property
    def doc(self) -> str:
        """Documentation line for this socket — its tooltip, else its name."""
        return _clean_doc(self.description or self.name)

    @property
    def param_doc(self) -> str:
        """The parameter's documentation line: the tooltip plus, for an input
        with a fallback, what it reads when nothing is connected, and for one
        with a default attribute, what a modifier input reads by default."""
        doc = self.doc
        if self.fallback:
            doc = f"{doc.rstrip('.')}. When unconnected: {self.fallback}"
        if self.modifier_attribute:
            doc = (
                f"{doc.rstrip('.')}. As a modifier input, reads the "
                f'"{self.modifier_attribute}" attribute by default.'
            )
        return doc

    @property
    def param_type(self) -> str:
        """Type hint for the ``__init__`` parameter.

        A menu socket is narrowed to its own items so editors offer them for
        completion, while still accepting a linked ``MenuSocket``.
        """
        if not self.menu_items:
            return self.input_type
        # Double-quoted to match the formatted source (ruff reformats the code
        # but not the docstring copy of the same annotation).
        literals = ", ".join(_quote(item) for item in self.menu_items)
        return f"{self.input_type} | Literal[{literals}]"


@dataclass
class _AssetClass:
    class_name: str
    asset_name: str
    description: str
    library_source: str
    tree_idname: str
    inputs: list[_Socket]
    outputs: list[_Socket]


def _collect(
    sockets,
    descriptions: dict[str, str] | None = None,
    menus: bool = False,
    fallbacks: dict[str, Default] | None = None,
    modifier_attributes: dict[str, str] | None = None,
) -> list[_Socket]:
    """Introspect ``sockets`` into records.

    ``menus`` resolves menu sockets to their items — only worth doing for the
    group's *inputs*, whose parameters are typed from them. ``fallbacks`` maps
    an input's identifier to what it reads when unconnected (the interface's
    ``default_input`` field); such a parameter defaults to the matching
    ``Default`` member instead of a stored value. ``modifier_attributes``
    maps an input to its default attribute name, which only a Geometry Nodes
    modifier uses, so it is documented but does not change the default.
    """
    descriptions = descriptions or {}
    fallbacks = fallbacks or {}
    modifier_attributes = modifier_attributes or {}
    # Keep inactive sockets: socket-usage inference deactivates inputs that the
    # current node options (e.g. a menu selection) leave unused, but a caller
    # may set those options differently, so the API must expose every input.
    raw = [s for s in sockets if s.identifier != "__extend__"]
    # Accessor and parameter names follow the one mapping the generated call
    # sites use too.
    attrs = typed_param_names(raw)
    out: list[_Socket] = []
    for s in raw:
        socket_class, input_type = _socket_types(type(s).__name__)
        menu_items = _menu_items(s) if menus else ()
        attr = attrs[s.identifier]
        fallback = fallbacks.get(s.identifier)
        out.append(
            _Socket(
                name=s.name,
                identifier=s.identifier,
                socket_class=socket_class,
                input_type=input_type,
                default=repr(fallback) if fallback else _format_default(s),
                attr=attr,
                description=descriptions.get(s.identifier, ""),
                menu_items=menu_items,
                fallback=fallback.description if fallback else "",
                modifier_attribute=modifier_attributes.get(s.identifier, ""),
            )
        )
    return out


def _interface_fallbacks(group) -> dict[str, Default]:
    """What each group input reads when unconnected, by socket identifier.

    An interface input with a ``default_input`` other than ``VALUE`` reads an
    implicit field or context value instead of its stored default, whether
    the group is a modifier or a node in another tree. Other inputs are left
    out.
    """
    fallbacks: dict[str, Default] = {}
    for item in group.interface.items_tree:
        if item.item_type != "SOCKET" or item.in_out != "INPUT":
            continue
        default_input = getattr(item, "default_input", "VALUE")
        if default_input != "VALUE":
            fallbacks[item.identifier] = Default(default_input)
    return fallbacks


def _interface_modifier_attributes(group) -> dict[str, str]:
    """Each group input's default attribute name, by socket identifier.

    Blender only applies it when the group is a Geometry Nodes modifier (the
    input starts in attribute mode reading that name); as a node inside
    another tree the input still uses its stored value.
    """
    return {
        item.identifier: item.default_attribute_name
        for item in group.interface.items_tree
        if item.item_type == "SOCKET"
        and item.in_out == "INPUT"
        and getattr(item, "default_attribute_name", "")
    }


def _introspect_group(group, name: str, library_source: str) -> _AssetClass:
    """Introspect the node group ``group`` (a ``bpy.types.NodeTree``) into an
    :class:`_AssetClass` record by instantiating it on a throwaway host node.

    ``group`` is deliberately unannotated: the stubs type interface items and
    ``node_groups.new`` too narrowly for the runtime attributes used here.
    """
    host = bpy.data.node_groups.new("_introspect_host", group.bl_idname)
    assert host is not None
    try:
        node_type = {
            "GeometryNodeTree": "GeometryNodeGroup",
            "ShaderNodeTree": "ShaderNodeGroup",
            "CompositorNodeTree": "CompositorNodeGroup",
        }[group.bl_idname]
        node = host.nodes.new(node_type)
        assert node is not None
        node = cast(
            "bpy.types.GeometryNodeGroup | bpy.types.ShaderNodeGroup | bpy.types.CompositorNodeGroup",
            node,
        )
        node.node_tree = group
        # Tooltips live on the tree *interface* items, not on the node's
        # sockets — collect them by identifier so the generated docstrings
        # can use the asset author's own wording.
        descriptions = {
            item.identifier: item.description or ""
            for item in group.interface.items_tree
            if item.item_type == "SOCKET"
        }
        return _AssetClass(
            class_name=_class_name(name),
            asset_name=name,
            description=(group.description or name).strip(),
            library_source=library_source,
            tree_idname=group.bl_idname,
            inputs=_collect(
                node.inputs,
                descriptions,
                menus=True,
                fallbacks=_interface_fallbacks(group),
                modifier_attributes=_interface_modifier_attributes(group),
            ),
            outputs=_collect(node.outputs, descriptions),
        )
    finally:
        bpy.data.node_groups.remove(host)


def _introspect(library: AssetLibrary, names: set[str] | None) -> list[_AssetClass]:
    """Append each requested group from the library and introspect its
    interface into :class:`_AssetClass` records."""
    path = library.path()
    library_source = _library_source(library)

    with bpy.data.libraries.load(path, link=False, assets_only=True) as (src, _):  # ty: ignore[invalid-context-manager]
        available = list(src.node_groups)
    wanted = [n for n in available if names is None or n in names]

    classes: list[_AssetClass] = []
    for name in wanted:
        # Always append from *this* library — never reuse a same-named group by
        # global lookup, since names collide across tree types (a geometry and a
        # compositor "Combine Spherical" both exist) and we'd introspect the
        # wrong one. Blender renames the appended copy on a clash; that's fine,
        # we only read its interface (the emitted _asset_name uses the original).
        with bpy.data.libraries.load(path, link=False, assets_only=True) as (  # ty: ignore[invalid-context-manager]
            src,
            dst,
        ):
            dst.node_groups = [name]
        group = dst.node_groups[0]
        classes.append(_introspect_group(group, name, library_source))
    return classes


def _library_source(library: AssetLibrary) -> str:
    """Source expression that reconstructs ``library`` in the generated module."""
    if isinstance(library, BundledLibrary):
        return f"BundledLibrary({_fmt(library.filename)})"

    if isinstance(library, PackageLibrary):
        # Emit a plain forward-slash string literal (never ``PosixPath(...)``),
        # so the generated module imports cleanly and stays cross-platform even
        # when ``relative`` was passed as a ``Path``.
        relative = Path(library.relative).as_posix()
        return f"PackageLibrary(__file__, {_fmt(relative)})"
    raise TypeError(f"Cannot serialise asset library: {library!r}")


def _accessor(sockets: list[_Socket], kind: str, docstrings: bool) -> str:
    if not sockets:
        return f"    class {kind}(SocketAccessor):\n        pass"
    lines = [f"    class {kind}(SocketAccessor):"]
    for s in sockets:
        lines.append(f"        {s.attr}: {s.socket_class}")
        doc = s.doc if docstrings else _clean_doc(s.name)
        if doc and doc != s.attr:
            lines.append(f'        """{doc}"""')
    return "\n".join(lines)


def _class_docstring(cls: _AssetClass) -> str:
    """A numpy-style docstring for ``cls``, matching the built-in node classes."""
    lines = [_clean_doc(cls.description), ""]
    if cls.inputs:
        lines += ["Parameters", "----------"]
        for s in cls.inputs:
            lines += [f"{s.attr} : {s.param_type}", f"    {s.param_doc}"]
        lines.append("")
        lines += ["Inputs", "------"]
        for s in cls.inputs:
            lines += [f"i.{s.attr} : {s.socket_class}", f"    {s.doc}"]
        lines.append("")
    if cls.outputs:
        lines += ["Outputs", "-------"]
        for s in cls.outputs:
            lines += [f"o.{s.attr} : {s.socket_class}", f"    {s.doc}"]
    # Indent to the class body, leaving blank separator lines truly blank so the
    # module needs no formatter pass to be clean.
    body = "\n".join(f"    {line}" if line else "" for line in lines).strip("\n")
    return f'"""\n{body}\n    """'


def _render_interface(
    cls: _AssetClass, *, docstrings: bool = True, nodebpy_pkg: str = "nodebpy"
) -> tuple[GroupInterface, list[str]]:
    """The typed-interface parts of the class for *cls*, and the import lines
    they need.

    The parts are the docstring, the ``_asset_name`` and ``_library``
    attributes, the ``_Inputs`` and ``_Outputs`` accessors and the typed
    ``__init__``. With a ``library_source`` the class is an appending
    ``Asset*Group``; without one (a shared helper group, which is not an
    asset) only the typed API is added and the ``Custom*Group`` base stays.

    The ``__init__`` keys its super call by socket *name*, with a
    ``_named_links`` fallback for duplicate names, rather than by identifier:
    identifiers are authoring-history artifacts that a tree rebuilt from
    ``_build_group`` reassigns, while names round-trip.
    """
    docstring = (
        _class_docstring(cls) if docstrings else f'"""{_clean_doc(cls.description)}"""'
    )

    params = [f"{s.attr}: {s.param_type} = {s.default}" for s in cls.inputs]
    signature = (
        "(\n        self,\n        " + ",\n        ".join(params) + ",\n    )"
        if params
        else "(self)"
    )
    name_counts = Counter(s.name for s in cls.inputs)
    keyed = [
        f"{_quote(s.name)}: {s.attr}" for s in cls.inputs if name_counts[s.name] == 1
    ]
    pairs = [
        f"({_quote(s.name)}, {s.attr})" for s in cls.inputs if name_counts[s.name] > 1
    ]
    args = []
    if keyed:
        args.append("**{" + ", ".join(keyed) + "}")
    if pairs:
        args.append("_named_links=[" + ", ".join(pairs) + "]")
    init_return = " -> None" if signature == "(self)" else ""
    init = f"    def __init__{signature}{init_return}:\n        super().__init__({', '.join(args)})"

    type_checking = (
        "    if TYPE_CHECKING:\n"
        "        @property\n"
        "        def i(self) -> _Inputs: ...\n"
        "        @property\n"
        "        def o(self) -> _Outputs: ..."
    )
    body = "\n\n".join(
        [
            _accessor(cls.inputs, "_Inputs", docstrings),
            _accessor(cls.outputs, "_Outputs", docstrings),
            type_checking,
            init,
        ]
    )

    base: str | None = None
    attr_lines: list[str] = []
    if cls.library_source:
        base = asset_group_base(cls.tree_idname).__name__
        attr_lines = [
            f"_asset_name = {_fmt(cls.asset_name)}",
            f"_library = {cls.library_source}",
        ]

    typing_names = ["TYPE_CHECKING"]
    if any(s.menu_items for s in cls.inputs):
        typing_names.append("Literal")
    builder_names = {
        "SocketAccessor",
        *(s.socket_class for s in cls.inputs + cls.outputs),
    }
    if cls.library_source:
        builder_names.add(cls.library_source.partition("(")[0])
    import_lines = [
        f"from typing import {', '.join(typing_names)}",
        f"from {nodebpy_pkg}.builder import {', '.join(sorted(builder_names))}",
    ]
    if any("math." in s.default for s in cls.inputs):
        import_lines.insert(0, "import math")
    input_types = sorted({s.input_type for s in cls.inputs})
    if any(s.default.startswith("Default.") for s in cls.inputs):
        input_types.insert(0, "Default")  # sorts before the Input* names
    if input_types:
        import_lines.append(f"from {nodebpy_pkg}.types import {', '.join(input_types)}")

    return (
        GroupInterface(
            docstring=f"    {docstring}", body=body, base=base, attr_lines=attr_lines
        ),
        import_lines,
    )


def interface_parts(
    group,
    *,
    library_source: str | None,
    nodebpy_pkg: str = "nodebpy",
) -> tuple[GroupInterface, list[str]]:
    """The typed-interface parts (:func:`_render_interface`) of the merged
    dump class for ``group``, a live ``bpy.types.NodeTree``. They are spliced
    by :func:`nodebpy.export.to_python` into the class it emits around
    ``_build_group``, so one class both documents the group and carries the
    recipe that regenerates it."""
    cls = _introspect_group(group, group.name, library_source or "")
    return _render_interface(cls, nodebpy_pkg=nodebpy_pkg)


def render_asset_class(
    cls: _AssetClass, *, docstrings: bool = True, nodebpy_pkg: str = "nodebpy"
) -> tuple[str, list[str]]:
    """The source of a class that only appends its asset: the typed
    interface around the attributes the appending base needs, with no
    recipe. Returns the class and the import lines it needs."""
    parts, import_lines = _render_interface(
        cls, docstrings=docstrings, nodebpy_pkg=nodebpy_pkg
    )
    import_lines.append(f"from {nodebpy_pkg}.builder import {parts.base}")
    attrs = "\n".join(
        f"    {line}" for line in (f"_name = {_fmt(cls.asset_name)}", *parts.attr_lines)
    )
    source = (
        f"class {cls.class_name}({parts.base}):\n"
        f"{parts.docstring}\n\n{attrs}\n\n{parts.body}\n"
    )
    return source, import_lines


def merge_imports(lines: Iterable[str]) -> list[str]:
    """One import line per module, with every name the given lines import
    from it."""
    plain: list[str] = []
    names: dict[str, set[str]] = {}
    for line in lines:
        if line.startswith("from "):
            module, _, imported = line[5:].partition(" import ")
            names.setdefault(module, set()).update(
                n.strip() for n in imported.split(",")
            )
        elif line not in plain:
            plain.append(line)
    # Constants before classes, as ruff's import sorting wants them.
    return plain + [
        f"from {module} import {', '.join(sorted(ns, key=lambda n: (not n.isupper(), n)))}"
        for module, ns in names.items()
    ]


def _render_module(
    classes: list[_AssetClass], nodebpy_pkg: str = "nodebpy", docstrings: bool = True
) -> str:
    """A module of appending asset classes, sorted by name."""
    rendered = [
        render_asset_class(c, docstrings=docstrings, nodebpy_pkg=nodebpy_pkg)
        for c in sorted(classes, key=lambda c: c.class_name)
    ]
    imports = merge_imports(line for _, lines in rendered for line in lines)
    header = [
        "# Generated by nodebpy.assets.generate_asset_api; do not edit.",
        *imports,
    ]
    body = "\n\n".join(source for source, _ in rendered)
    all_names = ",\n    ".join(
        f'"{c.class_name}"' for c in sorted(classes, key=lambda c: c.class_name)
    )
    footer = (
        f"\n\n__all__ = (\n    {all_names},\n)\n" if classes else "\n__all__ = ()\n"
    )
    return "\n".join(header) + "\n\n\n" + body + footer


def generate_asset_api(
    libraries: AssetLibrary | Sequence[AssetLibrary],
    output_path: str | Path,
    *,
    names: set[str] | None = None,
    nodebpy_pkg: str = "nodebpy",
    docstrings: bool = True,
) -> list[str]:
    """Generate typed asset classes for ``libraries`` into one module.

    Parameters
    ----------
    libraries:
        One or more :class:`~nodebpy.builder.AssetLibrary` instances
        (:class:`~nodebpy.builder.BundledLibrary` for Blender's bundled assets,
        :class:`~nodebpy.builder.PackageLibrary` for a ``.blend`` shipped inside
        your own package).
    output_path:
        The ``.py`` file to write.
    names:
        Restrict generation to these asset (node-group) names; defaults to all.
    nodebpy_pkg:
        Import anchor for nodebpy in the generated module. Defaults to the
        absolute ``"nodebpy"``. When nodebpy is vendored inside another package,
        pass the path that reaches it *relative to the generated module's
        package*, such as ``"..vendor.nodebpy"``.
    docstrings:
        Emit numpy-style class docstrings (description, ``Parameters``,
        ``Inputs``, ``Outputs``) from the asset's own socket tooltips, so
        editors show documentation alongside the type hints. Pass ``False``
        for a terser module.

    Returns
    -------
    list[str]
        The generated class names.
    """
    classes = _introspect_all(libraries, names)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        _render_module(classes, nodebpy_pkg=nodebpy_pkg, docstrings=docstrings),
        encoding="utf-8",
    )
    return [c.class_name for c in classes]


def generate_asset_modules(
    libraries: AssetLibrary | Sequence[AssetLibrary],
    output_dir: str | Path,
    *,
    names: set[str] | None = None,
    nodebpy_pkg: str = "nodebpy",
    docstrings: bool = True,
) -> dict[str, list[str]]:
    """Generate typed asset classes for ``libraries``, one module per tree
    type inside ``output_dir``: ``geometry.py``, ``shader.py`` and/or
    ``compositor.py``, for the tree types that have assets. Asset names
    repeat across editors (a geometry and a compositor "Combine Spherical"
    both exist), so splitting keeps the class names from shadowing each
    other. Parameters are as for :func:`generate_asset_api`. Returns the
    class names written per module."""
    classes = _introspect_all(libraries, names)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, list[str]] = {}
    for tree_idname, module in _TREE_MODULES.items():
        tree_classes = [c for c in classes if c.tree_idname == tree_idname]
        if not tree_classes:
            continue
        (output_dir / f"{module}.py").write_text(
            _render_module(
                tree_classes, nodebpy_pkg=nodebpy_pkg, docstrings=docstrings
            ),
            encoding="utf-8",
        )
        written[module] = [c.class_name for c in tree_classes]
    return written


def _introspect_all(
    libraries: AssetLibrary | Sequence[AssetLibrary], names: set[str] | None
) -> list[_AssetClass]:
    if isinstance(libraries, AssetLibrary):
        libraries = [libraries]
    return [cls for library in libraries for cls in _introspect(library, names)]
