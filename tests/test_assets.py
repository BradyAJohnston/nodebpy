"""Asset-backed node groups: the generated essentials APIs and the generator."""

import inspect
import os
from pathlib import Path

import pytest

from nodebpy import TreeBuilder
from nodebpy.assets import (
    BundledLibrary,
    PackageLibrary,
    _codegen,
    generate_asset_api,
    generate_asset_modules,
)
from nodebpy.assets.__main__ import generate_essentials
from nodebpy.builder import BaseNode, asset_group_base
from nodebpy.nodes import compositor as nc
from nodebpy.nodes import geometry as ng
from nodebpy.nodes import shader as ns

_ESSENTIALS = BundledLibrary("geometry_nodes_essentials.blend")
_HAVE_ESSENTIALS = os.path.exists(_ESSENTIALS.path())
_needs_essentials = pytest.mark.skipif(
    not _HAVE_ESSENTIALS, reason="bundled geometry essentials not installed"
)


def _asset_classes(module):
    """Generated asset classes exported from a tree's node module."""
    return [
        obj
        for name in dir(module)
        if inspect.isclass(obj := getattr(module, name))
        and issubclass(obj, BaseNode)
        and isinstance(getattr(obj, "_asset_name", None), str)
    ]


# -- Generated essentials: every asset class appends and exposes its interface --


@_needs_essentials
@pytest.mark.parametrize(
    "module,builder",
    [
        (ng, TreeBuilder.geometry),
        (ns, TreeBuilder.shader),
        (nc, TreeBuilder.compositor),
    ],
    ids=["geometry", "shader", "compositor"],
)
def test_every_generated_asset_instantiates(module, builder):
    classes = _asset_classes(module)
    assert classes, f"no asset classes generated in {module.__name__}"
    with builder("Assets"):
        for cls in classes:
            if not os.path.exists(cls._library.path()):
                continue  # that essentials library isn't installed
            node = cls()
            assert node.node.node_tree is not None, cls.__name__
            # The interface accessors resolve against the appended group.
            assert node.i is not None and node.o is not None


@_needs_essentials
def test_generated_asset_appends_and_links():
    with ng.tree("t"):
        node = ng.SmoothByAngle(mesh=ng.Cube(), angle=0.5)
        assert node.node.node_tree is not None
        assert node.node.node_tree.name == "Smooth by Angle"
        assert node.node.name == "Smooth by Angle"
        assert node.o.mesh is not None
        assert any(socket.is_linked for socket in node.node.inputs)


@_needs_essentials
def test_generated_asset_reuses_appended_group():
    """A second instance reuses the already-appended group (same tree object)."""
    with ng.tree("t"):
        first = ng.SmoothByAngle()
        second = ng.SmoothByAngle()
        assert first.node.node_tree is second.node.node_tree


@_needs_essentials
def test_generated_asset_chains():
    with ng.tree("t"):
        mesh = ng.SmoothByAngle(mesh=ng.Cube()).o.mesh
        arr = ng.Array(geometry=mesh, count=4)
        assert arr.o.geometry is not None


# -- Library resolution --------------------------------------------------------


def test_package_library_path_is_anchor_relative(tmp_path):
    # Resolved relative to the anchor's directory (use a real path so the
    # comparison is drive/platform-agnostic — .resolve() adds a drive on Windows).
    anchor = tmp_path / "sub" / "module.py"
    lib = PackageLibrary(str(anchor), "../data/assets.blend")
    assert lib.path() == str((tmp_path / "data" / "assets.blend").resolve())


def test_bundled_library_path_under_datafiles():
    path = BundledLibrary("x.blend").path()
    assert path.endswith(os.path.join("assets", "nodes", "x.blend"))


def test_asset_group_base_per_tree():
    assert asset_group_base("GeometryNodeTree").__name__ == "AssetGeometryGroup"
    assert asset_group_base("ShaderNodeTree").__name__ == "AssetShaderGroup"
    assert asset_group_base("CompositorNodeTree").__name__ == "AssetCompositorGroup"


# -- create_group error paths --------------------------------------------------


def test_create_group_missing_library():
    class Missing(asset_group_base("GeometryNodeTree")):
        _name = _asset_name = "Nope"
        _library = BundledLibrary("does_not_exist.blend")

    with ng.tree("t"), pytest.raises(FileNotFoundError):
        Missing()


@_needs_essentials
def test_create_group_unknown_asset_name():
    class Unknown(asset_group_base("GeometryNodeTree")):
        _name = _asset_name = "No Such Group In Library"
        _library = _ESSENTIALS

    with ng.tree("t"), pytest.raises(KeyError):
        Unknown()


# -- Generator -----------------------------------------------------------------


@_needs_essentials
def test_generate_full_library(tmp_path):
    """Generating a whole library exercises the socket-type, default and
    class-name code paths across its many groups."""
    out = tmp_path / "generated.py"
    names = generate_asset_api(_ESSENTIALS, out)
    assert len(names) > 1
    source = out.read_text()
    assert "BundledLibrary(" in source
    assert "__all__" in source


@_needs_essentials
def test_generate_with_package_library(tmp_path):
    # Point a PackageLibrary at the real essentials file so it can be introspected.
    essentials = Path(_ESSENTIALS.path())
    lib = PackageLibrary(str(essentials.parent / "_anchor.py"), essentials.name)
    out = tmp_path / "generated.py"
    generate_asset_api(lib, out, names={"Smooth by Angle"})
    source = out.read_text()
    assert "PackageLibrary(__file__, " in source


@_needs_essentials
def test_generate_modules_split_by_tree(tmp_path):
    """Mixed-tree-type libraries are split into one module per tree type, and
    tree types with no assets get no file."""
    libraries = [_ESSENTIALS]
    shader = BundledLibrary("shading_nodes_essentials.blend")
    if os.path.exists(shader.path()):
        libraries.append(shader)
    written = generate_asset_modules(libraries, tmp_path)
    assert written["geometry"]
    assert (tmp_path / "geometry.py").exists()
    assert "__all__" in (tmp_path / "geometry.py").read_text()
    if len(libraries) == 2:
        assert written["shader"]
        assert (tmp_path / "shader.py").exists()
    assert "compositor" not in written
    assert not (tmp_path / "compositor.py").exists()


def test_library_source_renders_path_as_plain_string():
    """A PackageLibrary built with a ``Path`` relative must render as a plain
    forward-slash string literal — never ``PosixPath('…')``, which the generated
    module doesn't import (and which isn't cross-platform)."""
    lib = PackageLibrary(__file__, Path("assets") / "data.blend")
    source = _codegen._library_source(lib)
    assert source == "PackageLibrary(__file__, 'assets/data.blend')"
    assert "PosixPath" not in source
    assert "WindowsPath" not in source


@_needs_essentials
def test_generate_with_vendored_nodebpy_pkg(tmp_path):
    """nodebpy_pkg rewrites the import anchor so a vendored copy can be reached
    with a relative path instead of the absolute ``nodebpy`` package."""
    out = tmp_path / "generated.py"
    generate_asset_api(
        _ESSENTIALS, out, names={"Smooth by Angle"}, nodebpy_pkg="..vendor.nodebpy"
    )
    source = out.read_text()
    assert "from ..vendor.nodebpy.builder import" in source
    assert "from nodebpy.builder import" not in source


@_needs_essentials
def test_generate_emits_numpy_docstrings(tmp_path):
    """Docstrings are on by default: a numpy-style class docstring plus the
    asset's own socket tooltips, so editors show docs beside the type hints."""
    out = tmp_path / "generated.py"
    generate_asset_api(_ESSENTIALS, out, names={"Smooth by Angle"})
    source = out.read_text()
    assert "Parameters\n    ----------" in source
    assert "Inputs\n    ------" in source
    assert "Outputs\n    -------" in source
    assert "mesh : InputGeometry" in source
    assert "i.angle : FloatSocket" in source
    assert "o.mesh : GeometrySocket" in source
    # The tooltip authored on the group interface, not just the socket name.
    assert "Maximum face angle for smooth edges" in source


@_needs_essentials
def test_generate_without_docstrings_stays_terse(tmp_path):
    out = tmp_path / "generated.py"
    generate_asset_api(_ESSENTIALS, out, names={"Smooth by Angle"}, docstrings=False)
    source = out.read_text()
    assert '"""Smooth by Angle"""' in source
    assert "Parameters" not in source
    assert "Maximum face angle for smooth edges" not in source
    # Accessor annotations still carry the socket's display name.
    assert '"""Mesh"""' in source


@_needs_essentials
def test_generated_docstrings_are_importable_and_readable(tmp_path):
    """The emitted module must import cleanly and expose the docstrings."""
    out = tmp_path / "generated_docs.py"
    generate_asset_api(_ESSENTIALS, out, names={"Smooth by Angle"})
    namespace: dict = {}
    exec(compile(out.read_text(), str(out), "exec"), namespace)
    doc = namespace["SmoothByAngle"].__doc__
    assert doc.lstrip().startswith("Smooth by Angle")
    assert "Maximum face angle for smooth edges" in doc


@_needs_essentials
def test_generate_types_menu_sockets_as_literals(tmp_path):
    """A menu socket's items are emitted as a ``Literal`` so editors can
    complete them."""
    out = tmp_path / "generated.py"
    generate_asset_api(_ESSENTIALS, out, names={"Array"})
    source = out.read_text()
    assert "from typing import TYPE_CHECKING, Literal" in source
    literal = 'InputMenu | Literal["Line", "Circle", "Curve", "Transform"]'
    assert f"shape: {literal} = 'Line'" in source
    # The narrowed type is documented alongside the parameter, too.
    assert f"shape : {literal}" in source


@_needs_essentials
def test_every_menu_socket_resolves_its_items(tmp_path):
    """Every menu input across the essentials resolves to its items."""
    classes = _codegen._introspect(_ESSENTIALS, None)
    menus = [s for c in classes for s in c.inputs if s.socket_class == "MenuSocket"]
    assert menus, "expected menu sockets in the geometry essentials"
    unresolved = [s.name for s in menus if not s.menu_items]
    assert not unresolved, f"menu items not found for {unresolved}"


@_needs_essentials
def test_menu_items_leave_the_socket_default_untouched():
    """Probing for the items assigns an impossible value; the rejected
    assignment must not disturb the socket's real default."""
    with ng.tree("t"):
        node = ng.Array()
        socket = next(s for s in node.node.inputs if s.type == "MENU")
        before = socket.default_value
        assert _codegen._menu_items(socket)
        assert socket.default_value == before


def test_menu_items_ignore_non_menu_sockets():
    class _NotAMenu:
        type = "GEOMETRY"
        default_value = ""

    assert _codegen._menu_items(_NotAMenu()) == ()


def test_clean_doc_escapes_docstring_terminator():
    assert _codegen._clean_doc('a """quoted""" tip') == "a '''quoted''' tip"
    assert _codegen._clean_doc("multi\nline\ttip") == "multi line tip"
    assert _codegen._clean_doc("trailing backslash \\") == "trailing backslash"


def test_generate_empty_library_writes_empty_all(tmp_path):
    out = tmp_path / "generated.py"
    names = generate_asset_api(_ESSENTIALS, out, names={"___no_such_group___"})
    assert names == []
    assert "__all__ = ()" in out.read_text()


def test_library_source_rejects_unknown_type():
    with pytest.raises(TypeError):
        _codegen._library_source(object())  # type: ignore[arg-type]


def test_class_name_helper():
    assert _codegen._class_name("Smooth by Angle") == "SmoothByAngle"
    assert _codegen._class_name("3D to Screen Space") == "_3DToScreenSpace"
    assert _codegen._class_name("") == "AssetGroup"


def test_socket_types_fallback():
    assert _codegen._socket_types("NodeSocketGeometry") == (
        "GeometrySocket",
        "InputGeometry",
    )
    assert _codegen._socket_types("NodeSocketSomethingNew") == (
        "Socket",
        "InputLinkable",
    )


# -- Essentials entry point ----------------------------------------------------


@_needs_essentials
def test_generate_essentials_writes_modules(tmp_path):
    written = generate_essentials(tmp_path)
    assert "geometry" in written and written["geometry"]
    assert (tmp_path / "geometry" / "assets.py").exists()
