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


def test_split_inputs_instances_named_after_sockets():
    """Split instances take the name (and header label) of the interface
    sockets they carry, so they read as their content when scanning the
    tree instead of an anonymous 'Group Input.001'."""
    with TreeBuilder("SplitNames", split_inputs=True) as tree:
        radius = tree.inputs.float("Radius")
        height = tree.inputs.float("Height")
        depth = tree.inputs.float("Depth")
        math = g.Math.add(radius, 1.0)
        combine = g.CombineXYZ(x=math, y=height, z=depth)
        combine.o.vector.length() >> tree.outputs.float("Out")

    # The first consumer (Math) keeps the primary node; CombineXYZ's
    # instance is named after both sockets it carries.
    instance = tree.tree.nodes["Height, Depth"]
    assert instance.bl_idname == "NodeGroupInput"
    assert instance.label == "Height, Depth"
    assert tree.tree.nodes["Group Input"].outputs["Radius"].is_linked


def test_split_inputs_instances_follow_consumer_frames():
    """A split instance is parented into its consumer's frame — an
    unparented instance would be pushed away from the consumer by the
    arranger's frame clustering."""
    with TreeBuilder("SplitFrames", split_inputs=True) as tree:
        a = tree.inputs.float("A")
        b = tree.inputs.float("B")
        math = g.Math.add(a, 1.0)
        with g.Frame("Inner"):
            combine = g.CombineXYZ(x=math, y=b)
        combine.o.vector.length() >> tree.outputs.float("Out")

    instance = tree.tree.nodes["B"]
    assert instance.parent is not None
    assert instance.parent == combine.node.parent
    # The frame-less first consumer keeps the frame-less primary node.
    assert tree.tree.nodes["Group Input"].parent is None


def test_default_split_inputs_scope():
    """Inside a default_split_inputs scope, builders left at their default
    split_inputs split on exit; an explicit False and arrangement-disabled
    trees (snapshot-positions dumps) are unaffected, and the default resets
    when the scope closes."""
    from nodebpy.builder import default_split_inputs

    def input_node_count(name: str, **kwargs) -> int:
        with TreeBuilder(name, **kwargs) as tree:
            a = tree.inputs.float("A")
            b = tree.inputs.float("B")
            math = g.Math.add(a, 1.0)
            g.CombineXYZ(x=math, y=b).o.vector.length() >> tree.outputs.float("Out")
        return sum(1 for n in tree.tree.nodes if n.bl_idname == "NodeGroupInput")

    with default_split_inputs():
        assert input_node_count("AmbientSplit") == 2
        assert input_node_count("AmbientSplitOff", split_inputs=False) == 1
        assert input_node_count("AmbientSplitNoArrange", arrange=None) == 1
    assert input_node_count("AmbientSplitOutside") == 1


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


def test_clear_rebuilds_existing_tree_in_place():
    with g.tree("Rebuild In Place") as tree:
        (
            tree.inputs.geometry("Geometry")
            >> g.SetPosition()
            >> tree.outputs.geometry("Geometry")
        )
    datablock = tree.tree
    modifier = bpy.data.objects["Cube"].modifiers.new("GN", "NODES")
    modifier.node_group = datablock

    with TreeBuilder(datablock, clear=True) as rebuilt:
        rebuilt.inputs.geometry("Geometry") >> rebuilt.outputs.geometry("Geometry")
        rebuilt.inputs.float("Scale")

    assert rebuilt.tree == datablock
    assert modifier.node_group == datablock
    assert {n.bl_idname for n in datablock.nodes} == {
        "NodeGroupInput",
        "NodeGroupOutput",
    }
    assert [item.name for item in datablock.interface.items_tree] == [
        "Geometry",
        "Geometry",
        "Scale",
    ]


def test_clear_reuses_group_by_name_and_type():
    with g.tree("Reuse By Name") as first:
        (
            first.inputs.geometry("Geometry")
            >> g.SetPosition()
            >> first.outputs.geometry("Geometry")
        )
    with g.tree("Reuse By Name", clear=True) as second:
        second.inputs.geometry("Geometry") >> second.outputs.geometry("Geometry")

    assert second.tree == first.tree
    assert bpy.data.node_groups.get("Reuse By Name.001") is None
    assert len(second.tree.nodes) == 2


def test_clear_with_other_tree_type_creates_new_tree():
    with TreeBuilder.shader("Type Collision") as shader_tree:
        shader_tree.inputs.float("Value") >> shader_tree.outputs.float("Value")
    node_count = len(shader_tree.tree.nodes)

    with g.tree("Type Collision", clear=True) as geo_tree:
        geo_tree.inputs.geometry("Geometry") >> geo_tree.outputs.geometry("Geometry")

    assert geo_tree.tree != shader_tree.tree
    assert geo_tree.tree.bl_idname == "GeometryNodeTree"
    assert geo_tree.tree.name == "Type Collision.001"
    assert len(shader_tree.tree.nodes) == node_count


def test_without_clear_a_name_creates_a_new_tree():
    with g.tree("Not Cleared") as first:
        pass
    with g.tree("Not Cleared") as second:
        pass
    assert second.tree != first.tree
    assert second.tree.name == "Not Cleared.001"
