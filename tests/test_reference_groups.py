"""``to_python(groups="reference")``: groups a loaded class builds are called,
not written out again."""

import sys
import textwrap

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.builder import (
    AssetGeometryGroup,
    BundledLibrary,
    CustomGeometryGroup,
    PackageLibrary,
)
from nodebpy.export import _groups, to_python
from nodebpy.live import run_source
from nodebpy.nodes.geometry.groups import SliceToIndices


def _tree_body(code):
    return code.split("as tree:\n", 1)[1]


def _uses_array():
    with TreeBuilder("Live") as tree:
        geo = tree.inputs.geometry("Geometry")
        SliceToIndices(stop=5)
        geo >> g.Array(count=4) >> g.SetPosition() >> tree.outputs.geometry("Geometry")
    return tree


def test_builtin_groups_are_called():
    code = to_python(_uses_array(), groups="reference")

    assert "class " not in code
    assert "from nodebpy.nodes.geometry.groups import SliceToIndices" in code
    body = _tree_body(code)
    assert "g.Array(geometry=geometry, count=4)" in body
    assert "SliceToIndices(stop=5" in body

    exec(code, {})  # noqa: S102
    rebuilt = bpy.data.node_groups["Live.001"]
    assert rebuilt.nodes["Array"].node_tree == bpy.data.node_groups["Array"]
    assert bpy.data.node_groups["Array"].library is not None


def test_inline_is_the_default():
    code = to_python(_uses_array())
    assert "class Array(CustomGeometryGroup)" in code
    assert "class SliceToIndices(CustomGeometryGroup)" in code


def test_vendored_nodebpy_imports():
    code = to_python(_uses_array(), groups="reference", nodebpy_pkg="..vendor.nodebpy")
    assert "from ..vendor.nodebpy.nodes.geometry.groups import SliceToIndices" in code


def _appended(name, rename=None):
    path = BundledLibrary("geometry_nodes_essentials.blend").path()
    with bpy.data.libraries.load(path, link=False, assets_only=True) as (_, dst):
        dst.node_groups = [name]
    group = dst.node_groups[0]
    if rename:
        group.name = rename
    with TreeBuilder("Appended") as tree:
        node = g.Group()
        node.node.node_tree = group
    return tree


def test_asset_browser_copies_are_called():
    code = to_python(_appended("Array", rename="My Array"), groups="reference")
    assert "class " not in code
    assert "g.Array()" in _tree_body(code)


def test_local_tree_of_an_asset_name_is_called():
    tree = _appended("Array", rename="Appended Array")
    node = tree.tree.nodes["Group"]
    # A copy has no reference to the library.
    node.node_tree = node.node_tree.copy()
    bpy.data.node_groups.remove(bpy.data.node_groups["Appended Array"])
    node.node_tree.name = "Array"
    assert node.node_tree.library_weak_reference is None
    assert "g.Array()" in to_python(tree, groups="reference")


SCRIPT = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup

    class Offset(CustomGeometryGroup):
        _name = "Offset"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            amount = tree.inputs.float("Amount", 1.0)
            geo >> g.SetPosition(offset=(0, 0, amount)) >> tree.outputs.geometry("Geometry")

    with g.tree("Uses Offset", clear=True) as tree:
        geo = tree.inputs.geometry("Geometry")
        geo >> Offset(Amount=2.0) >> tree.outputs.geometry("Geometry")
    """
)


def test_script_classes_are_called_by_name():
    result = run_source(SCRIPT)
    assert result.tree is not None

    code = to_python(result.tree, groups="reference", in_place=True)

    assert "class Offset" not in code
    assert "import Offset" not in code
    assert "Offset(Geometry=geometry, Amount=2.0)" in code

    # The tree's code goes back into the script that defines the class.
    again = run_source(SCRIPT.split("with g.tree")[0] + code)
    assert again.tree is not None
    assert again.tree.nodes["Offset"].node_tree == bpy.data.node_groups["Offset"]


def test_edited_group_is_written_out():
    result = run_source(SCRIPT)
    assert result.tree is not None
    offset = bpy.data.node_groups["Offset"]
    offset.nodes["Set Position"].mute = True

    code = to_python(result.tree, groups="reference")

    assert "class Offset(CustomGeometryGroup)" in code


def test_script_class_name_taken_is_written_out():
    result = run_source(SCRIPT)
    assert result.tree is not None
    # A group written out first takes the name the script class would need.
    with TreeBuilder("Wrapper") as wrapper:
        with TreeBuilder("offset") as other:
            other.inputs.float("X") >> other.outputs.float("X")
        first = g.Group()
        first.node.node_tree = other.tree
        second = g.Group()
        second.node.node_tree = bpy.data.node_groups["Offset"]

    code = to_python(wrapper, groups="reference")

    assert code.count("class Offset") == 2


MODULE = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup


    class {cls}(CustomGeometryGroup):
        _name = "{name}"

        def __init__(self, amount: float = 1.0, geometry=None):
            super().__init__(Amount=amount, Geometry=geometry)

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            amount = tree.inputs.float("Amount", 1.0)
            geo >> g.SetPosition(offset=(0, 0, amount)) >> tree.outputs.geometry("Geometry")
    """
)


@pytest.fixture
def package(tmp_path, monkeypatch):
    """A ``mygroups`` package on sys.path, with a ``Lift`` class in a
    submodule and another ``Lift`` in a second module."""
    root = tmp_path / "mygroups"
    root.mkdir()
    (root / "__init__.py").write_text("")
    (root / "lift.py").write_text(MODULE.format(cls="Lift", name="Lift"))
    (tmp_path / "otherlift.py").write_text(MODULE.format(cls="Lift", name="Lift 2"))
    monkeypatch.syspath_prepend(str(tmp_path))
    yield tmp_path
    for name in [n for n in sys.modules if n.startswith(("mygroups", "otherlift"))]:
        del sys.modules[name]


def _uses_lifts(*classes):
    with TreeBuilder("Lifted") as tree:
        geo = tree.inputs.geometry("Geometry")
        for cls in classes:
            geo = cls(amount=3.0, geometry=geo)
        geo >> tree.outputs.geometry("Geometry")
    return tree


def test_group_modules_are_imported_and_matched(package):
    import importlib

    lift = importlib.import_module("mygroups.lift").Lift
    tree = _uses_lifts(lift)
    for name in [n for n in sys.modules if n.startswith("mygroups")]:
        del sys.modules[name]

    code = to_python(tree, groups="reference", group_modules=["mygroups"])

    assert "from mygroups.lift import Lift" in code
    assert "Lift(geometry=geometry, amount=3.0)" in code


def test_imported_names_that_clash_are_aliased(package):
    import importlib

    first = importlib.import_module("mygroups.lift").Lift
    second = importlib.import_module("otherlift").Lift

    code = to_python(_uses_lifts(first, second), groups="reference", group_modules=[])

    assert "from mygroups.lift import Lift" in code
    assert "from otherlift import Lift as Lift2" in code
    assert "Lift2(geometry=Lift(geometry=geometry, amount=3.0)" in code


def test_configured_sources_are_imported(package, monkeypatch):
    (package / "pyproject.toml").write_text(
        '[tool.nodebpy.assets]\nsource = "mygroups"\n'
    )
    monkeypatch.chdir(package)
    import importlib

    tree = _uses_lifts(importlib.import_module("mygroups.lift").Lift)

    assert _groups.configured_modules() == ["mygroups"]
    assert "from mygroups.lift import Lift" in to_python(tree, groups="reference")


def test_configured_sources_off_sys_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert _groups.configured_modules() == []
    (tmp_path / "pyproject.toml").write_text(
        '[tool.nodebpy.assets]\nsource = "elsewhere/my-groups"\n'
    )
    assert _groups.configured_modules() == []


class _Required(CustomGeometryGroup):
    _name = "Required"

    def __init__(self, amount: float):
        super().__init__(Amount=amount)

    def _build_group(self, tree):
        tree.inputs.float("Amount") >> tree.outputs.float("Amount")


class _Untyped(CustomGeometryGroup):
    _name = "Untyped"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _build_group(self, tree):
        tree.inputs.float("Amount") >> tree.outputs.float("Amount")


class _Variant(CustomGeometryGroup):
    _name = "Variant"

    def _group_name(self):
        return "Variant"

    def _build_group(self, tree):
        tree.inputs.float("Amount") >> tree.outputs.float("Amount")


def test_call_forms():
    with TreeBuilder("Calls") as tree:
        _Required(2.0)
        _Untyped(Amount=2.0)
        _Variant(Amount=2.0)

    code = to_python(tree, groups="reference")

    # A required parameter codegen might not pass, and a tree named per
    # instance, are written out; ``**kwargs`` takes socket names.
    assert "class Required(CustomGeometryGroup)" in code
    assert "class Variant(CustomGeometryGroup)" in code
    assert "_Untyped(Amount=2.0)" in code


def test_package_library_assets(tmp_path):
    with TreeBuilder("Packaged Asset") as asset:
        asset.inputs.float("Amount") >> asset.outputs.float("Amount")
    asset.tree.asset_mark()
    blend = tmp_path / "assets.blend"
    bpy.data.libraries.write(str(blend), {asset.tree})
    bpy.data.node_groups.remove(asset.tree)

    class Packaged(AssetGeometryGroup):
        _asset_name = "Packaged Asset"
        _library = PackageLibrary(str(tmp_path / "anchor.py"), "assets.blend")

    try:
        with TreeBuilder("Uses Packaged") as tree:
            Packaged(Amount=1.5)
        linked = bpy.data.node_groups["Packaged Asset"]
        assert linked.library is not None

        code = to_python(tree, groups="reference")

        assert "Packaged(Amount=1.5)" in code
        assert "class Packaged" not in code
    finally:
        del Packaged
        import gc

        gc.collect()
