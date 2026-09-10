import bpy

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.nodes.geometry.groups import PrincipalComponents


def test_create_tree_and_save():
    with TreeBuilder("AnotherTree") as tree:
        count = tree.inputs.integer("Count")
        instances = tree.outputs.geometry("Instances")

        rotation = (
            g.RandomValue.vector(min=(-1, -1, -1), seed=2)
            >> g.AlignRotationToVector()
            >> g.RotateRotation(
                rotate_by=g.AxisAngleToRotation(angle=0.3),
                rotation_space="LOCAL",
            )
        )

        _ = (
            count
            >> g.Points(position=g.RandomValue.vector(min=(-1, -1, -1)))
            >> g.InstanceOnPoints(instance=g.Cube(), rotation=rotation)
            >> g.SetPosition(
                position=g.Position() * 2.0 + (0, 0.2, 0.3),
                offset=(0, 0, 0.1),
            )
            >> g.RealizeInstances()
            >> g.InstanceOnPoints(g.Cube(), instance=...)
            >> instances
        )


def test_panel_groups_input_sockets():
    """Test that sockets created inside a panel context are children of that panel."""
    with TreeBuilder("PanelInputTest") as tree:
        tree.inputs.geometry("Geometry")
        with tree.inputs.panel("Settings"):
            tree.inputs.integer("Count")
            tree.inputs.float("Scale")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 1
        assert panel_items[0].name == "Settings"

        count_item = next(i for i in items if getattr(i, "name", None) == "Count")
        scale_item = next(i for i in items if getattr(i, "name", None) == "Scale")
        assert count_item.parent == panel_items[0]
        assert scale_item.parent == panel_items[0]

        geo_item = next(i for i in items if getattr(i, "name", None) == "Geometry")
        assert geo_item.parent != panel_items[0]


def test_panel_groups_output_sockets():
    """Test that panels work on outputs too."""
    with TreeBuilder("PanelOutputTest") as tree:
        with tree.outputs.panel("Results"):
            tree.outputs.geometry("Geometry")
        tree.outputs.float("Extra")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 1
        assert panel_items[0].name == "Results"

        geo_item = next(i for i in items if getattr(i, "name", None) == "Geometry")
        extra_item = next(i for i in items if getattr(i, "name", None) == "Extra")
        assert geo_item.parent == panel_items[0]
        assert extra_item.parent != panel_items[0]


def test_multiple_panels():
    """Test creating multiple panels in the same inputs context."""
    with TreeBuilder("MultiPanelTest") as tree:
        with tree.inputs.panel("Transform"):
            tree.inputs.vector("Position")
        with tree.inputs.panel("Appearance"):
            tree.inputs.color("Color")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 2
        panel_names = {p.name for p in panel_items}
        assert panel_names == {"Transform", "Appearance"}

        pos_item = next(i for i in items if getattr(i, "name", None) == "Position")
        color_item = next(i for i in items if getattr(i, "name", None) == "Color")
        assert pos_item.parent.name == "Transform"
        assert color_item.parent.name == "Appearance"


def test_panel_default_closed():
    """Test that the default_closed option is applied to the panel."""
    with TreeBuilder("PanelClosedTest") as tree:
        with tree.inputs.panel("Advanced", default_closed=True):
            tree.inputs.float("Threshold")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        assert panel.default_closed is True


def test_panel_context_clears_after_exit():
    """Test that sockets after the panel block are not in the panel."""
    with TreeBuilder("PanelClearTest") as tree:
        with tree.inputs.panel("Group"):
            tree.inputs.integer("Inside")
        tree.inputs.integer("Outside")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        inside = next(i for i in items if getattr(i, "name", None) == "Inside")
        outside = next(i for i in items if getattr(i, "name", None) == "Outside")
        assert inside.parent == panel
        assert outside.parent != panel


def test_string_generators(snapshot):
    with g.tree():
        tree = TreeBuilder(PrincipalComponents().node_tree)

    assert snapshot == tree.to_python(format=False)
    assert snapshot == tree.to_mermaid()
    assert snapshot == tree.to_mermaid(fenced=False)


def test_split_inputs_creates_instance_per_consumer():
    """``split_inputs=True`` regenerates the editor style: one Group Input
    instance per consumer node, unused sockets hidden, wiring unchanged."""
    with TreeBuilder("AutoSplit", split_inputs=True) as tree:
        a = tree.inputs.float("A")
        b = tree.inputs.float("B")
        out = tree.outputs.float("Out")
        math = g.Math.add(a, 1.0)
        combine = g.CombineXYZ(x=math, y=b)
        combine.o.vector.length() >> out

    instances = [n for n in tree.tree.nodes if n.bl_idname == "NodeGroupInput"]
    assert len(instances) == 2
    for node in instances:
        linked = {s.name for s in node.outputs if s.is_linked}
        hidden = {s.name for s in node.outputs if s.hide}
        assert len(linked) == 1  # one instance per consumer, one input each
        assert hidden == {"A", "B"} - linked
    # Wiring is unchanged: Math still takes A, CombineXYZ still takes B.
    assert math.node.inputs[0].links[0].from_socket.name == "A"
    assert combine.node.inputs["Y"].links[0].from_socket.name == "B"


def test_split_inputs_noop_with_single_consumer():
    """One consumer node means nothing to split — the primary stays alone
    (with its unused sockets hidden)."""
    with TreeBuilder("AutoSplitNoop", split_inputs=True) as tree:
        a = tree.inputs.float("A")
        tree.inputs.float("Spare")
        g.Math.add(a, 1.0) >> tree.outputs.float("Out")

    instances = [n for n in tree.tree.nodes if n.bl_idname == "NodeGroupInput"]
    assert len(instances) == 1
    assert instances[0].outputs["Spare"].hide


def test_group_input_splits_getter_reports_instances():
    with TreeBuilder("SplitGet", split_inputs=True) as tree:
        a = tree.inputs.float("A")
        b = tree.inputs.float("B")
        math = g.Math.add(a, 1.0)
        g.CombineXYZ(x=math, y=b).o.vector.length() >> tree.outputs.float("Out")

    splits = tree.group_input_splits
    assert len(splits) == 1
    (split,) = splits
    assert split["name"] != "Group Input"
    assert len(split["links"]) == 1


def test_group_input_splits_setter_skips_gracefully():
    """Entries naming consumers, sockets, or interface inputs the tree does
    not have (or that carry no matching existing link) leave the noodle on
    the primary node instead of mis-wiring anything."""
    with TreeBuilder("SplitSkip") as tree:
        a = tree.inputs.float("A")
        math = g.Math.add(a, 1.0)
        math >> tree.outputs.float("Out")
        tree.group_input_splits = [
            {"name": "GI.001", "links": [("A", "No Such Node", "Value")]},
            {"name": "GI.002", "links": [("A", "Math", "No Such Socket")]},
            # names a socket that exists but is not fed by a Group Input
            {"name": "GI.003", "links": [("A", "Math", "Value_001")]},
            # names an interface input that does not exist
            {"name": "GI.004", "links": [("Nope", "Math", "Value")]},
        ]

    primary = tree.tree.nodes["Group Input"]
    assert primary.outputs["A"].is_linked  # the noodle stayed put
    assert len([n for n in tree.tree.nodes if n.bl_idname == "NodeGroupInput"]) == 5


def test_split_group_inputs_without_primary_is_noop():
    with TreeBuilder("NoInputs", split_inputs=True) as tree:
        g.Value(1.0) >> tree.outputs.float("Out")
    assert not any(n.bl_idname == "NodeGroupInput" for n in tree.tree.nodes)


def test_nested_tree_panel_reuses_by_parent():
    """Re-entering the same nested tree.panel chain reuses the panels
    instead of duplicating them."""
    with TreeBuilder("NestedPanels") as tree:
        with tree.panel("Outer", description="o"):
            tree.inputs.float("A")
            with tree.panel("Inner"):
                tree.inputs.float("B")
        with tree.panel("Outer"):
            with tree.panel("Inner"):
                tree.outputs.float("C")
        tree.inputs.float("X") >> tree.outputs.float("Y")

    panels = [
        i
        for i in tree.tree.interface.items_tree
        if getattr(i, "item_type", "") == "PANEL"
    ]
    assert [p.name for p in panels] == ["Outer", "Inner"]
    outer, inner = panels
    assert inner.parent == outer
    sockets = {
        i.name: i
        for i in tree.tree.interface.items_tree
        if getattr(i, "item_type", "") == "SOCKET"
    }
    assert sockets["A"].parent == outer
    assert sockets["B"].parent == inner
    assert sockets["C"].parent == inner  # reused, not duplicated
