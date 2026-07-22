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
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import bpy

from ..builder import AssetLibrary, BundledLibrary, asset_group_base
from ..builder._utils import normalize_name

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
        return str(round(value, 6))
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

    @property
    def doc(self) -> str:
        """Documentation line for this socket — its tooltip, else its name."""
        return _clean_doc(self.description or self.name)

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
) -> list[_Socket]:
    """Introspect ``sockets`` into records.

    ``menus`` resolves menu sockets to their items — only worth doing for the
    group's *inputs*, whose parameters are typed from them.
    """
    descriptions = descriptions or {}
    raw = [
        s
        for s in sockets
        if s.identifier != "__extend__" and not getattr(s, "is_inactive", False)
    ]
    # The accessor resolves attribute names by identifier first, then name, so a
    # group socket's readable name works as the attr/param when it's unambiguous;
    # fall back to the opaque-but-unique identifier only on a name collision.
    name_counts = Counter(normalize_name(s.name) for s in raw)
    out: list[_Socket] = []
    for s in raw:
        socket_class, input_type = _socket_types(type(s).__name__)
        menu_items = _menu_items(s) if menus else ()
        norm_name = normalize_name(s.name)
        attr = (
            norm_name if name_counts[norm_name] == 1 else normalize_name(s.identifier)
        )
        out.append(
            _Socket(
                name=s.name,
                identifier=s.identifier,
                socket_class=socket_class,
                input_type=input_type,
                default=_format_default(s),
                attr=attr,
                description=descriptions.get(s.identifier, ""),
                menu_items=menu_items,
            )
        )
    return out


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

        host = bpy.data.node_groups.new("_introspect_host", group.bl_idname)
        try:
            node_type = {
                "GeometryNodeTree": "GeometryNodeGroup",
                "ShaderNodeTree": "ShaderNodeGroup",
                "CompositorNodeTree": "CompositorNodeGroup",
            }[group.bl_idname]
            node = host.nodes.new(node_type)
            node.node_tree = group  # ty: ignore[unresolved-attribute]
            # Tooltips live on the tree *interface* items, not on the node's
            # sockets — collect them by identifier so the generated docstrings
            # can use the asset author's own wording.
            descriptions = {
                item.identifier: item.description or ""
                for item in group.interface.items_tree
                if item.item_type == "SOCKET"
            }
            classes.append(
                _AssetClass(
                    class_name=_class_name(name),
                    asset_name=name,
                    description=(group.description or name).strip(),
                    library_source=library_source,
                    tree_idname=group.bl_idname,
                    inputs=_collect(node.inputs, descriptions, menus=True),
                    outputs=_collect(node.outputs, descriptions),
                )
            )
        finally:
            bpy.data.node_groups.remove(host)
    return classes


def _library_source(library: AssetLibrary) -> str:
    """Source expression that reconstructs ``library`` in the generated module."""
    if isinstance(library, BundledLibrary):
        return f"BundledLibrary({library.filename!r})"
    from ..builder import PackageLibrary

    if isinstance(library, PackageLibrary):
        # Emit a plain forward-slash string literal (never ``PosixPath(...)``),
        # so the generated module imports cleanly and stays cross-platform even
        # when ``relative`` was passed as a ``Path``.
        relative = Path(library.relative).as_posix()
        return f"PackageLibrary(__file__, {relative!r})"
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
            lines += [f"{s.attr} : {s.param_type}", f"    {s.doc}"]
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


def _render_class(cls: _AssetClass, docstrings: bool = False) -> str:
    base = asset_group_base(cls.tree_idname).__name__
    docstring = (
        _class_docstring(cls) if docstrings else f'"""{_clean_doc(cls.description)}"""'
    )
    inputs_cls = _accessor(cls.inputs, "_Inputs", docstrings)
    outputs_cls = _accessor(cls.outputs, "_Outputs", docstrings)

    params = [f"{s.attr}: {s.param_type} = {s.default}" for s in cls.inputs]
    signature = (
        "(\n        self,\n        " + ",\n        ".join(params) + ",\n    )"
        if params
        else "(self)"
    )
    key_args = ", ".join(f'"{s.identifier}": {s.attr}' for s in cls.inputs)

    return f"""class {cls.class_name}({base}):
    {docstring}

    _name = {cls.asset_name!r}
    _asset_name = {cls.asset_name!r}
    _library = {cls.library_source}

{inputs_cls}

{outputs_cls}

    if TYPE_CHECKING:
        @property
        def i(self) -> _Inputs: ...
        @property
        def o(self) -> _Outputs: ...

    def __init__{signature}:
        super().__init__(**{{{key_args}}})
"""


def _render_module(
    classes: list[_AssetClass],
    nodebpy_pkg: str = "nodebpy",
    docstrings: bool = False,
) -> str:
    socket_classes = sorted(
        {s.socket_class for c in classes for s in c.inputs + c.outputs}
    )
    input_types = sorted({s.input_type for c in classes for s in c.inputs})
    bases = sorted({asset_group_base(c.tree_idname).__name__ for c in classes})
    libraries = sorted(
        {
            "BundledLibrary"
            if c.library_source.startswith("BundledLibrary")
            else "PackageLibrary"
            for c in classes
        }
    )

    builder_imports = sorted(
        set(bases) | set(libraries) | {"SocketAccessor"} | set(socket_classes)
    )

    typing_imports = ["TYPE_CHECKING"]
    if any(s.menu_items for c in classes for s in c.inputs):
        typing_imports.append("Literal")

    lines = [
        "# Auto-generated by nodebpy.assets.generate_asset_api — do not edit manually.",
        f"from typing import {', '.join(typing_imports)}",
        "",
        f"from {nodebpy_pkg}.builder import (\n    {',\n    '.join(builder_imports)},\n)",
        f"from {nodebpy_pkg}.types import (\n    {',\n    '.join(input_types)},\n)"
        if input_types
        else "",
    ]
    header = "\n".join(line for line in lines if line) + "\n\n\n"
    ordered = sorted(classes, key=lambda c: c.class_name)
    body = "\n\n".join(_render_class(c, docstrings) for c in ordered)
    all_names = ",\n    ".join(f'"{c.class_name}"' for c in ordered)
    footer = (
        f"\n\n__all__ = (\n    {all_names},\n)\n" if ordered else "\n__all__ = ()\n"
    )
    return header + body + footer


def generate_asset_api(
    libraries: AssetLibrary | Sequence[AssetLibrary],
    output_path: str | Path,
    *,
    names: set[str] | None = None,
    nodebpy_pkg: str = "nodebpy",
    docstrings: bool = True,
) -> list[str]:
    """Generate typed asset classes for ``libraries`` into ``output_path``.

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
        package* — e.g. ``"..vendor.nodebpy"`` — so the emitted imports stay
        relative to the install/vendor location.
    docstrings:
        Emit numpy-style class docstrings (description, ``Parameters``,
        ``Inputs``, ``Outputs``) using the asset's own socket tooltips, so
        editors show documentation alongside the type hints. Defaults to
        ``True``; pass ``False`` for a terser module.

    Returns the list of generated class names.
    """
    if isinstance(libraries, AssetLibrary):
        libraries = [libraries]

    classes: list[_AssetClass] = []
    for library in libraries:
        classes.extend(_introspect(library, names))

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
) -> dict[str, list[str]]:
    """Generate typed asset classes for ``libraries``, split into one module per
    tree type inside ``output_dir``.

    Writes ``geometry.py``, ``shader.py`` and/or ``compositor.py`` — one module
    for each tree type that has assets in the libraries (no file for the
    others). Asset names repeat across editors (a geometry *and* a compositor
    "Combine Spherical" both exist), so splitting keeps the generated class
    names collision-free where a single :func:`generate_asset_api` module would
    silently shadow one with the other.

    Parameters are as for :func:`generate_asset_api`, except ``output_dir`` is
    the directory to write the modules into (created if needed).

    Returns a mapping of module name (``"geometry"`` / ``"shader"`` /
    ``"compositor"``) to the class names written to it.
    """
    if isinstance(libraries, AssetLibrary):
        libraries = [libraries]

    classes: list[_AssetClass] = []
    for library in libraries:
        classes.extend(_introspect(library, names))

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, list[str]] = {}
    for tree_idname, module in _TREE_MODULES.items():
        tree_classes = [c for c in classes if c.tree_idname == tree_idname]
        if not tree_classes:
            continue
        (output_dir / f"{module}.py").write_text(
            _render_module(tree_classes, nodebpy_pkg=nodebpy_pkg), encoding="utf-8"
        )
        written[module] = [c.class_name for c in tree_classes]
    return written
