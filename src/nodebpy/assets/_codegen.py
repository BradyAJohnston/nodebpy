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


@dataclass
class _Socket:
    name: str
    identifier: str
    socket_class: str  # e.g. "GeometrySocket"
    input_type: str  # e.g. "InputGeometry"
    default: str  # source for the default value
    attr: str  # normalized accessor/param name


@dataclass
class _AssetClass:
    class_name: str
    asset_name: str
    description: str
    library_source: str
    tree_idname: str
    inputs: list[_Socket]
    outputs: list[_Socket]


def _collect(sockets) -> list[_Socket]:
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
            classes.append(
                _AssetClass(
                    class_name=_class_name(name),
                    asset_name=name,
                    description=(group.description or name).strip(),
                    library_source=library_source,
                    tree_idname=group.bl_idname,
                    inputs=_collect(node.inputs),
                    outputs=_collect(node.outputs),
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


def _accessor(sockets: list[_Socket], kind: str) -> str:
    if not sockets:
        return f"    class {kind}(SocketAccessor):\n        pass"
    lines = [f"    class {kind}(SocketAccessor):"]
    for s in sockets:
        lines.append(f"        {s.attr}: {s.socket_class}")
        doc = s.name
        if doc and doc != s.attr:
            lines.append(f'        """{doc}"""')
    return "\n".join(lines)


def _render_class(cls: _AssetClass) -> str:
    base = asset_group_base(cls.tree_idname).__name__
    inputs_cls = _accessor(cls.inputs, "_Inputs")
    outputs_cls = _accessor(cls.outputs, "_Outputs")

    params = [f"{s.attr}: {s.input_type} = {s.default}" for s in cls.inputs]
    signature = (
        "(\n        self,\n        " + ",\n        ".join(params) + ",\n    )"
        if params
        else "(self)"
    )
    key_args = ", ".join(f'"{s.identifier}": {s.attr}' for s in cls.inputs)

    return f'''class {cls.class_name}({base}):
    """{cls.description}"""

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
'''


def _render_module(classes: list[_AssetClass], nodebpy_pkg: str = "nodebpy") -> str:
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

    lines = [
        "# Auto-generated by nodebpy.assets.generate_asset_api — do not edit manually.",
        "from typing import TYPE_CHECKING",
        "",
        f"from {nodebpy_pkg}.builder import (\n    {',\n    '.join(builder_imports)},\n)",
        f"from {nodebpy_pkg}.types import (\n    {',\n    '.join(input_types)},\n)"
        if input_types
        else "",
    ]
    header = "\n".join(line for line in lines if line) + "\n\n\n"
    ordered = sorted(classes, key=lambda c: c.class_name)
    body = "\n\n".join(_render_class(c) for c in ordered)
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
        _render_module(classes, nodebpy_pkg=nodebpy_pkg), encoding="utf-8"
    )
    return [c.class_name for c in classes]
