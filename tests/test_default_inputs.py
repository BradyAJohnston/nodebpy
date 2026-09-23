"""``Default``: the fallback an unconnected input reads instead of a value.

Blender lets a group input (and some built-in inputs, such as Set Position's
*Position*) read an implicit field, a named attribute or a context value when
nothing is linked. ``Default`` members spell that fallback in generated
signatures, are accepted by the node constructors and the ``tree.inputs.*``
factories, and never touch the socket.
"""

import importlib.util
import inspect
import os

import pytest

from nodebpy import Default, TreeBuilder
from nodebpy import geometry as g
from nodebpy.assets import BundledLibrary, _codegen, generate_asset_api
from nodebpy.export.codegen import to_python
from nodebpy.types import DefaultAttribute

_ESSENTIALS = BundledLibrary("geometry_nodes_essentials.blend")
_needs_essentials = pytest.mark.skipif(
    not os.path.exists(_ESSENTIALS.path()),
    reason="bundled geometry essentials not installed",
)


def test_members_mirror_blender_identifiers():
    assert Default("POSITION") is Default.POSITION
    assert Default.POSITION.value == "POSITION"
    assert repr(Default.POSITION) == "Default.POSITION"
    assert str(Default.ID_OR_INDEX) == "Default.ID_OR_INDEX"
    assert Default.POSITION.description == "the position field"


def test_attribute_fallback():
    uv = Default.attribute("UVMap")
    assert isinstance(uv, DefaultAttribute)
    assert uv == DefaultAttribute("UVMap")
    assert repr(uv) == "Default.attribute('UVMap')"
    assert uv.description == 'the "UVMap" attribute'


def test_constructor_leaves_the_socket_untouched():
    with g.tree("Default Inputs") as tree:
        node = g.SetPosition(
            g.Cube(),
            position=Default.POSITION,
            offset=Default.attribute("offset"),
            selection=Default.INDEX,
        )
    linked = {
        link.to_socket.name for link in tree.tree.links if link.to_node == node.node
    }
    assert linked == {"Geometry"}
    assert tuple(node.node.inputs["Position"].default_value) == (0.0, 0.0, 0.0)
    assert node.node.inputs["Selection"].default_value is True


def test_hidden_value_inputs_default_to_none():
    """A built-in input whose value Blender hides (and, for Position, ignores in
    favour of the position field) advertises no value in its signature."""
    params = inspect.signature(g.SetPosition.__init__).parameters
    assert params["position"].default is None
    assert params["selection"].default is None
    assert params["offset"].default == (0.0, 0.0, 0.0)


def test_tree_factories_accept_default():
    with TreeBuilder.geometry("Fallbacks") as tree:
        tree.inputs.vector("Position", default_input=Default.POSITION)
        tree.inputs.integer("ID", default_input="ID_OR_INDEX")
        tree.inputs.vector(
            "UV Map", hide_value=True, default_attribute=Default.attribute("UVMap")
        )
        tree.inputs.object("Object", default_input=Default.SELF_OBJECT)
        tree.outputs.vector("Rest", default_attribute=Default.attribute("rest"))
        tree.outputs.geometry()
    items = {item.name: item for item in tree.tree.interface.items_tree}
    assert items["Position"].default_input == "POSITION"
    assert items["ID"].default_input == "ID_OR_INDEX"
    assert items["UV Map"].default_attribute_name == "UVMap"
    assert items["Object"].default_input == "SELF_OBJECT"
    assert items["Rest"].default_attribute_name == "rest"


def _fallback_group():
    with TreeBuilder.geometry("Fallback Group") as tree:
        geometry = tree.inputs.geometry()
        tree.inputs.vector("Position", default_input=Default.POSITION)
        tree.inputs.integer(
            "ID", 3, description="Per-point seed", default_input="ID_OR_INDEX"
        )
        tree.inputs.vector(
            "UV Map", hide_value=True, default_attribute=Default.attribute("UVMap")
        )
        tree.inputs.float("Scale", 2.0)
        geometry >> tree.outputs.geometry()
    return tree.tree


def test_asset_codegen_spells_fallbacks_as_default():
    parts, imports = _codegen.interface_parts(_fallback_group(), library_source=None)
    assert "position: InputVector = Default.POSITION" in parts.body
    assert "id: InputInteger = Default.ID_OR_INDEX" in parts.body
    assert "uv_map: InputVector = Default.attribute('UVMap')" in parts.body
    assert "scale: InputFloat = 2.0" in parts.body
    # The docstring says what the input reads when nothing is connected.
    assert (
        "Per-point seed. When unconnected, reads the ID field, or the index when there is no ID."
        in parts.docstring
    )
    assert "Position. When unconnected, reads the position field." in parts.docstring
    assert 'UV Map. When unconnected, reads the "UVMap" attribute.' in parts.docstring
    assert any(
        line.startswith("from nodebpy.types import ") and "Default" in line
        for line in imports
    )


def test_asset_codegen_without_fallbacks_does_not_import_default():
    with TreeBuilder.geometry("Plain Group") as tree:
        tree.inputs.float("Scale", 2.0)
        tree.outputs.float("Out")
    _, imports = _codegen.interface_parts(tree.tree, library_source=None)
    assert not any("Default" in line for line in imports)


@_needs_essentials
def test_generated_essentials_use_default(tmp_path):
    out = tmp_path / "generated.py"
    generate_asset_api(_ESSENTIALS, out, names={"Random Rotation"})
    source = out.read_text()
    assert "id: InputInteger = Default.ID_OR_INDEX" in source
    assert "Default," in source.split("from nodebpy.types import")[1].split(")")[0]
    spec = importlib.util.spec_from_file_location("generated_default", out)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with g.tree("Essentials Default") as tree:
        node = module.RandomRotation()
        assert not [l for l in tree.tree.links if l.to_node == node.node]


@_needs_essentials
def test_fresh_asset_node_exports_without_default_kwargs():
    """A ``Default`` parameter default is "nothing to export": the fresh
    node's stored socket value never becomes a keyword argument."""
    with g.tree("Fresh Asset") as tree:
        g.RandomRotation()
    lines = [ln.strip() for ln in to_python(tree.tree).splitlines()]
    assert "_random_rotation = RandomRotation()" in lines
