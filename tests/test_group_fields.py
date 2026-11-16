"""Groups declared with class fields (``nodebpy.builder.fields``)."""

import inspect
from typing import ClassVar

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import FloatSocket, GeometrySocket
from nodebpy.builder.fields import (
    BooleanInput,
    ColorInput,
    FloatInput,
    FloatOutput,
    GeometryGroup,
    GeometryInput,
    GeometryOutput,
    IntegerInput,
    Panel,
    ShaderGroup,
    ShaderOutput,
)
from nodebpy.export import to_python


class Jitter(GeometryGroup):
    """Randomly offset each point."""

    geometry: GeometryInput = GeometryInput(default=None)
    amount: FloatInput = FloatInput(default=0.2, min_value=0.0)
    seed: IntegerInput = IntegerInput(default=0)
    result: ClassVar[GeometryOutput] = GeometryOutput(name="Geometry")
    offset: ClassVar[FloatOutput] = FloatOutput(name="Max Offset")

    def build(self) -> None:
        offset = g.RandomValue.vector(min=-1, seed=self.seed) * self.amount
        _ = self.geometry >> g.SetPosition(offset=offset) >> self.result
        _ = g.Math.sine(self.amount) >> self.offset


class Scatter(GeometryGroup):
    _name = "Field Scatter"

    geometry: GeometryInput = GeometryInput(default=None)
    with Panel("Noise", default_closed=True):
        use_noise: BooleanInput = BooleanInput(default=True, panel_toggle=True)
        scale: FloatInput = FloatInput(default=1.0)
        with Panel("Detail"):
            seed: IntegerInput = IntegerInput(default=0)
        noise: ClassVar[FloatOutput] = FloatOutput()
    result: ClassVar[GeometryOutput] = GeometryOutput(name="Geometry")

    def build(self) -> None:
        n = g.RandomValue.float(seed=self.seed) * self.scale
        _ = g.Switch.float(self.use_noise, false=0.0, true=n) >> self.noise
        _ = self.geometry >> g.SetPosition(offset=g.CombineXYZ(z=n)) >> self.result


def _items(tree):
    """(depth, kind, name) for each interface item, in tree order."""
    rows = []
    for item in tree.interface.items_tree:
        depth, parent = 0, item.parent
        while parent is not None and parent.index != -1:
            depth, parent = depth + 1, parent.parent
        kind = "PANEL" if item.item_type == "PANEL" else item.in_out
        rows.append((depth, kind, item.name))
    return rows


def _interface(tree, in_out):
    return {
        item.name: item
        for item in tree.interface.items_tree
        if getattr(item, "in_out", None) == in_out
    }


def test_fields_become_the_interface():
    with g.tree():
        node = Jitter()
    tree = node.node.node_tree

    assert tree.name == "Jitter"
    inputs = _interface(tree, "INPUT")
    assert list(inputs) == ["Geometry", "Amount", "Seed"]
    assert inputs["Geometry"].socket_type == "NodeSocketGeometry"
    assert inputs["Amount"].default_value == pytest.approx(0.2)
    assert inputs["Amount"].min_value == pytest.approx(0.0)
    assert inputs["Seed"].socket_type == "NodeSocketInt"
    outputs = _interface(tree, "OUTPUT")
    assert list(outputs) == ["Geometry", "Max Offset"]
    assert tree.nodes["Group Output"].inputs["Geometry"].is_linked
    assert tree.nodes["Group Output"].inputs["Max Offset"].is_linked


def test_init_takes_inputs_by_position_and_keyword():
    with g.tree():
        a = Jitter(g.Cube(), 0.5)
        b = Jitter(amount=g.Value(0.3), seed=2)

    assert a.node.inputs["Geometry"].is_linked
    assert a.node.inputs["Amount"].default_value == pytest.approx(0.5)
    assert b.node.inputs["Amount"].is_linked
    assert b.node.inputs["Seed"].default_value == 2
    assert a.node.node_tree == b.node.node_tree
    assert len([t for t in bpy.data.node_groups if t.name.startswith("Jitter")]) == 1


def test_init_rejects_unknown_and_repeated_inputs():
    with g.tree():
        with pytest.raises(TypeError, match="unexpected input 'amont'"):
            Jitter(amont=1.0)
        with pytest.raises(TypeError, match="multiple values for input 'geometry'"):
            Jitter(g.Cube(), geometry=g.Cube())
        with pytest.raises(TypeError, match="takes 3 positional inputs"):
            Jitter(None, 1.0, 2, 3)


def test_init_signature_names_the_inputs():
    params = list(inspect.signature(Jitter.__init__).parameters)
    assert params == ["self", "geometry", "amount", "seed"]


def test_fields_read_as_the_nodes_sockets():
    with g.tree() as tree:
        node = Jitter()
        assert isinstance(node.geometry, GeometrySocket)
        assert isinstance(node.offset, FloatSocket)
        assert node.offset.socket.is_output
        assert not node.amount.socket.is_output

        _ = g.Cube() >> node.geometry
        node.amount = 0.7
        node.seed = g.Value(3.0)
        _ = node.offset * 2.0 >> tree.outputs.float("Out")

    assert node.node.inputs["Geometry"].is_linked
    assert node.node.inputs["Amount"].default_value == pytest.approx(0.7)
    assert node.node.inputs["Seed"].is_linked
    assert node.node.outputs["Max Offset"].is_linked


def test_chains_from_the_first_output():
    with g.tree() as tree:
        _ = g.Cube() >> Jitter() >> g.RealizeInstances() >> tree.outputs.geometry()

    jitter = next(n for n in tree.nodes if n.bl_idname == "GeometryNodeGroup")
    assert jitter.inputs["Geometry"].is_linked
    assert jitter.outputs["Geometry"].is_linked


def test_panels():
    with g.tree():
        node = Scatter(scale=2.0, seed=3, use_noise=False)
    tree = node.node.node_tree

    assert _items(tree) == [
        (0, "OUTPUT", "Geometry"),
        (0, "INPUT", "Geometry"),
        (0, "PANEL", "Noise"),
        (1, "INPUT", "Noise"),
        (1, "OUTPUT", "Noise"),
        (1, "INPUT", "Scale"),
        (1, "PANEL", "Detail"),
        (2, "INPUT", "Seed"),
    ]
    panels = {i.name: i for i in tree.interface.items_tree if i.item_type == "PANEL"}
    assert panels["Noise"].default_closed
    assert not panels["Detail"].default_closed
    toggle = _interface(tree, "INPUT")["Noise"]
    assert toggle.is_panel_toggle
    assert node.node.inputs["Seed"].default_value == 3
    assert node.use_noise.socket.default_value is False


def test_same_named_panels_stay_apart():
    class Twice(GeometryGroup):
        with Panel("Settings"):
            a: FloatInput = FloatInput(default=1.0)
        with Panel("Settings"):
            b: FloatInput = FloatInput(default=2.0)

        def build(self) -> None:
            pass

    with g.tree():
        node = Twice()
    panels = [
        i for i in node.node.node_tree.interface.items_tree if i.item_type == "PANEL"
    ]
    assert [p.name for p in panels] == ["Settings", "Settings"]


def test_name_from_class_name():
    class RadialArray(GeometryGroup):
        count: IntegerInput = IntegerInput(default=6)

        def build(self) -> None:
            pass

    assert RadialArray._name == "Radial Array"


def test_create_group_without_a_tree():
    tree = Jitter.create_group()
    assert tree.name == "Jitter"
    assert list(_interface(tree, "INPUT")) == ["Geometry", "Amount", "Seed"]


def test_subclass_adds_fields():
    class MoreJitter(Jitter):
        scale: FloatInput = FloatInput(default=2.0)

    assert [f._attr for f in MoreJitter._inputs] == [
        "geometry",
        "amount",
        "seed",
        "scale",
    ]
    assert MoreJitter._name == "More Jitter"


def test_shader_group():
    class Tint(ShaderGroup):
        color: ColorInput = ColorInput(default=(1.0, 0.2, 0.2, 1.0))
        strength: FloatInput = FloatInput(default=1.0)
        shader: ClassVar[ShaderOutput] = ShaderOutput(name="Emission")

        def build(self) -> None:
            _ = s.Emission(color=self.color, strength=self.strength) >> self.shader

    with s.tree():
        node = Tint(strength=3.0)
    assert node.node.inputs["Strength"].default_value == pytest.approx(3.0)
    assert list(_interface(node.node.node_tree, "OUTPUT")) == ["Emission"]


def test_reserved_names_are_rejected():
    with pytest.raises(TypeError, match="'node' is part of the group node's API"):

        class Bad(GeometryGroup):
            node: FloatInput = FloatInput(default=1.0)


def test_duplicate_socket_names_are_rejected():
    with pytest.raises(TypeError, match=r"several inputs named \['Value'\]"):

        class Bad(GeometryGroup):
            a: FloatInput = FloatInput(default=1.0, name="Value")
            b: FloatInput = FloatInput(default=2.0, name="Value")


def test_panel_toggle_needs_a_panel():
    with pytest.raises(TypeError, match="must be declared inside"):

        class Bad(GeometryGroup):
            on: BooleanInput = BooleanInput(default=True, panel_toggle=True)


def test_inputs_cannot_be_assigned_while_building():
    class Assigns(GeometryGroup):
        value: FloatInput = FloatInput(default=1.0)

        def build(self) -> None:
            self.value = 2.0

    with g.tree(), pytest.raises(AttributeError, match="inside build"):
        Assigns()


def test_to_python_calls_the_class():
    with TreeBuilder("Uses Jitter") as tree:
        geo = tree.inputs.geometry("Geometry")
        _ = geo >> Jitter(amount=0.5, seed=4) >> tree.outputs.geometry("Geometry")

    code = to_python(tree, groups="reference")
    assert "class Jitter" not in code
    assert "Jitter(" in code
