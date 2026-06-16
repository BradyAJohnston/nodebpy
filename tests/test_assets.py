"""Asset-backed node groups: the generated essentials APIs and the generator."""

import inspect
import os
from pathlib import Path

import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.assets import BundledLibrary, PackageLibrary, generate_asset_api
from nodebpy.assets import _codegen
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
    with g.tree("t"):
        node = ng.SmoothByAngle(mesh=g.Cube(), angle=0.5)
        assert node.node.node_tree is not None
        assert node.node.node_tree.name == "Smooth by Angle"
        assert node.o.mesh is not None
        assert any(socket.is_linked for socket in node.node.inputs)


@_needs_essentials
def test_generated_asset_reuses_appended_group():
    """A second instance reuses the already-appended group (same tree object)."""
    with g.tree("t"):
        first = ng.SmoothByAngle()
        second = ng.SmoothByAngle()
        assert first.node.node_tree is second.node.node_tree


@_needs_essentials
def test_generated_asset_chains():
    with g.tree("t"):
        mesh = ng.SmoothByAngle(mesh=g.Cube()).o.mesh
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

    with g.tree("t"), pytest.raises(FileNotFoundError):
        Missing()


@_needs_essentials
def test_create_group_unknown_asset_name():
    class Unknown(asset_group_base("GeometryNodeTree")):
        _name = _asset_name = "No Such Group In Library"
        _library = _ESSENTIALS

    with g.tree("t"), pytest.raises(KeyError):
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
