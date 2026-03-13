import bpy

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy import sockets as s


def test_create_tree_and_save():
    with TreeBuilder("AnotherTree") as tree:
        with tree.inputs:
            count = s.SocketInt("Count")
        with tree.outputs:
            instances = s.SocketGeometry("Instances")

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
        with tree.inputs:
            geo = s.SocketGeometry("Geometry")
            with tree.inputs.panel("Settings"):
                count = s.SocketInt("Count")
                scale = s.SocketFloat("Scale")

        items = list(tree.tree.interface.items_tree)
        panel_items = [
            item for item in items if isinstance(item, bpy.types.NodeTreeInterfacePanel)
        ]
        assert len(panel_items) == 1
        assert panel_items[0].name == "Settings"

        # Sockets inside the panel should have the panel as parent
        count_item = next(i for i in items if getattr(i, "name", None) == "Count")
        scale_item = next(i for i in items if getattr(i, "name", None) == "Scale")
        assert count_item.parent == panel_items[0]
        assert scale_item.parent == panel_items[0]

        # Socket outside the panel should have no panel parent
        geo_item = next(i for i in items if getattr(i, "name", None) == "Geometry")
        assert geo_item.parent != panel_items[0]


def test_panel_groups_output_sockets():
    """Test that panels work on outputs too."""
    with TreeBuilder("PanelOutputTest") as tree:
        with tree.outputs:
            with tree.outputs.panel("Results"):
                out_geo = s.SocketGeometry("Geometry")
            extra = s.SocketFloat("Extra")

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
        with tree.inputs:
            with tree.inputs.panel("Transform"):
                pos = s.SocketVector("Position")
            with tree.inputs.panel("Appearance"):
                color = s.SocketColor("Color")

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
        with tree.inputs:
            with tree.inputs.panel("Advanced", default_closed=True):
                s.SocketFloat("Threshold")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        assert panel.default_closed is True


def test_panel_context_clears_after_exit():
    """Test that sockets after the panel block are not in the panel."""
    with TreeBuilder("PanelClearTest") as tree:
        with tree.inputs:
            with tree.inputs.panel("Group"):
                s.SocketInt("Inside")
            s.SocketInt("Outside")

        items = list(tree.tree.interface.items_tree)
        panel = next(
            i for i in items if isinstance(i, bpy.types.NodeTreeInterfacePanel)
        )
        inside = next(i for i in items if getattr(i, "name", None) == "Inside")
        outside = next(i for i in items if getattr(i, "name", None) == "Outside")
        assert inside.parent == panel
        assert outside.parent != panel
