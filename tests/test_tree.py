import bpy

from nodebpy import TreeBuilder
from nodebpy import geometry as g


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


from nodebpy import TreeBuilder
from nodebpy import geometry as g

with TreeBuilder("Outline") as tree:
    geo_in = tree.inputs.geometry()
    geo_out = tree.outputs.geometry()

    outline_near = tree.inputs.float("Outline Near", 0.005)
    outline_far = tree.inputs.float("Outline Far", 0.02)
    near_dist = tree.inputs.float("Near Distance", 1.0)
    far_dist = tree.inputs.float("Far Distance", 20.0)

    # ── Camera data ────────────────────────────────────────────────────────────
    cam_obj = g.ActiveCamera().o.active_camera
    cam_loc = g.ObjectInfo(cam_obj).o.location
    cam_info = g.CameraInfo(cam_obj)

    # column_2_row_2 = P[1][1] = cot(fov/2) — equivalent of unity_CameraProjection[1].y
    fov_factor = g.SeparateMatrix(cam_info.o.projection_matrix).o.column_2_row_2

    # ── Per-vertex distance from camera ────────────────────────────────────────
    dist = g.VectorMath.length(g.Position() - cam_loc).o.value

    # ── Smoothstep rolloff → outline size ──────────────────────────────────────
    # MapRange SMOOTHSTEP replaces smoothstep() + lerp() in one node
    outline_size = g.MapRange.smooth_step(
        value=dist,
        from_min=near_dist,
        from_max=far_dist,
        to_min=outline_near,
        to_max=outline_far,
    )

    # ── Perspective compensation ────────────────────────────────────────────────
    # HLSL extrudes in clip-space (screen units); GN extrudes in world-space.
    # To match: world_offset = screen_size × dist / P[1][1]
    world_offset = outline_size * dist / fov_factor

    # ── Extrude geometry along surface normal ──────────────────────────────────
    g.SetPosition(geo_in, offset=g.Normal().o.normal * world_offset) >> geo_out
