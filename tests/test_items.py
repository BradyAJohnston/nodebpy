"""The item collections shared by every items-driven node."""

import warnings

import pytest

from nodebpy.builder import (
    FloatSocket,
    FloatSocketGrid,
    GeometrySocket,
    VectorSocket,
    VectorSocketList,
)
from nodebpy.nodes import geometry as g


def test_collection_len_iter_and_index():
    with g.tree():
        cap = g.CaptureAttribute(g.Cube())
        pos = cap.items.vector(g.Position())
        cap.items.float(0.5, "Fac")
        cap.items.boolean()

        assert len(cap.items) == 3
        assert [item.name for item in cap.items] == ["Position", "Fac", "Boolean"]
        assert cap.items[0].name == pos.name
        assert cap.items[-1].socket_type == "BOOLEAN"
        assert cap.items["Fac"].input.socket.default_value == pytest.approx(0.5)
        assert isinstance(cap.items["Position"].output, VectorSocket)
        with pytest.raises(KeyError):
            cap.items["missing"]
        assert repr(cap.items).startswith("_FieldItems([Item('Position', ")


def test_name_inferred_from_source_or_type():
    with g.tree():
        cap = g.CaptureAttribute(g.Cube())
        assert cap.items.vector(g.Position()).name == "Position"
        assert cap.items.float(g.NoiseTexture().o.fac).name == "Factor"
        assert cap.items.float(g.NoiseTexture().o.fac, "Noise").name == "Noise"
        assert cap.items.float(1.0).name == "Value"
        assert cap.items.integer().name == "Integer"
        assert cap.items.new(2).name == "Integer.001"  # Blender suffixes duplicates
        assert cap.items.new(name="Any", type="FLOAT").socket_type == "FLOAT"
        with pytest.raises(TypeError):
            cap.items.new()
        with pytest.raises(TypeError):
            cap.items.new(object())


def test_constructor_takes_mapping_or_iterable():
    with g.tree():
        by_name = g.CaptureAttribute(
            g.Cube(), items={"P": g.Position(), "x": 1.0, "d": "FLOAT"}
        )
        assert [i.name for i in by_name.items] == ["P", "x", "d"]
        assert [i.socket_type for i in by_name.items] == [
            "FLOAT_VECTOR",
            "FLOAT",
            "FLOAT",
        ]
        by_source = g.CaptureAttribute(g.Cube(), items=[g.Position(), g.Index()])
        assert [i.name for i in by_source.items] == ["Position", "Index"]
        bake = g.Bake(g.Cube(), items=[g.Index()], val=0.5)
        assert [i.name for i in bake.items] == ["Mesh", "Index", "val"]


def test_rshift_into_input_continues_from_output():
    with g.tree() as tree:
        cap = g.CaptureAttribute(g.Cube())
        out = g.Position() >> cap.items.vector(name="P").input
        assert isinstance(out, VectorSocket)
        assert out.socket.is_output
        assert out.socket == cap.items["P"].output.socket
        g.SetPosition(cap.o.geometry, position=out) >> tree.outputs.geometry()

        zone = g.RepeatZone(5)
        geo = zone.items.geometry()
        current = g.Cube() >> geo.initial
        assert current.socket == geo.current.socket
        result = current >> g.SetShadeSmooth() >> geo.next
        assert result.socket == geo.result.socket
        assert isinstance(result, GeometrySocket)


def test_field_to_grid_and_list_pair_two_socket_classes():
    with g.tree():
        grid = g.FieldToGrid.float().items.float(0.5, "Density")
        assert isinstance(grid.input, FloatSocket)
        assert isinstance(grid.output, FloatSocketGrid)
        lst = g.FieldToList(4).items.vector(g.Position())
        assert isinstance(lst.input, VectorSocket)
        assert isinstance(lst.output, VectorSocketList)


def test_one_sided_items_have_one_role():
    with g.tree():
        cb = g.CombineBundle()
        a = cb.items.float(0.5, "a")
        assert isinstance(a.input, FloatSocket)
        with pytest.raises(AttributeError):
            _ = a.output
        sb = g.SeparateBundle(cb, items={"a": "FLOAT"})
        with pytest.raises(AttributeError):
            _ = sb.items["a"].input
        assert isinstance(sb.items["a"].output, FloatSocket)


def test_menu_and_index_switch_items():
    with g.tree():
        ms = g.MenuSwitch.float()
        first = ms.items.new(1.0, "A", description="first")
        ms.items.new(g.Value(), "B")
        ms.items.new(2.0)
        assert first.description == "first"
        assert first.output.socket.type == "BOOLEAN"
        assert [i.name for i in ms.items] == ["A", "B", "Item"]
        assert ms.node.inputs["Menu"].default_value == "A"
        ms2 = g.MenuSwitch.boolean(items={"on": True, "off": (False, "desc")})
        assert ms2.items["off"].description == "desc"

        sw = g.IndexSwitch.float(items=[0.5, g.Value(), None])
        sw.items.new(2.0)
        assert len(sw.items) == 4
        assert sw.items[0].input.socket.default_value == pytest.approx(0.5)
        assert len(sw.items[1].input.socket.links) == 1
        assert len(sw.items[2].input.socket.links) == 0


def test_deprecated_entry_points_still_work():
    with g.tree():
        cap = g.CaptureAttribute(g.Cube())
        zone = g.RepeatZone(2)
        fe = g.ForEachGeometryElementZone(g.Cube())
        ms = g.MenuSwitch.float()
        cz = g.ClosureZone()
        ftl = g.FieldToList(2)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            legacy = cap.items.float("Legacy", 0.25)
            assert legacy.name == "Legacy"
            assert legacy.input.socket.default_value == pytest.approx(0.25)
            assert cap.items.vector("Old").name == "Old"
            assert cap.add_item("x", 1.0).name == "x"
            assert cap.add_items({"y": "FLOAT"})["y"].socket_type == "FLOAT"
            assert cap.capture(g.Position()).socket.is_output
            assert zone.item("q", 1.0).name == "q"
            assert ms.item("C", 2.0).name == "C"
            assert ftl.float(1.0).socket.is_output
            assert cz.input_item("I").socket.is_output
            assert fe.inputs is not None and fe.main is not None
            assert fe.generated is not None
            assert fe.item("a", g.Index()).name == "a"
            assert fe.main_item("b", type="FLOAT").name == "b"
            assert fe.generated_item("c", type="FLOAT").name == "c"
        assert all(w.category is DeprecationWarning for w in caught)
        assert len(caught) == 15
