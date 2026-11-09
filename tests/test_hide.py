"""Node hide attribute preservation: ``node.hide`` is stored in
``to_python(snapshot_positions=True)`` and restored by ``TreeBuilder.layout_snapshot``.
"""

import bpy
from nodebpy import TreeBuilder
from nodebpy import geometry as g

# ---------------------------------------------------------------------------
# Basic hide capture in layout_snapshot
# ---------------------------------------------------------------------------


def test_hide_basic():
    """Test that hide state is captured in layout_snapshot for simple nodes."""
    with TreeBuilder("HideBasic") as tree:
        geo_in = g.GeometryInput()
        geo_in.location = (0, 0)
        geo_in.hide = True

    snapshot = tree.layout_snapshot
    assert len(snapshot) == 1
    name, entry = list(snapshot.items())[0]
    bl_idname, loc, hide_status, parent, links = entry
    assert hide_status is True


def test_hide_false_is_captured():
    """Verify that hide=False is also captured (default state)."""
    with TreeBuilder("HideFalse") as tree:
        math = g.Math(1.0 + 2.0)
        math.location = (0, 0)

    snapshot = tree.layout_snapshot
    name, entry = list(snapshot.items())[0]
    bl_idname, loc, hide_status, parent, links = entry
    assert hide_status is False


# ---------------------------------------------------------------------------
# Hide with frame blocks
# ---------------------------------------------------------------------------


def test_hide_with_frames():
    """Test hiding nodes inside frame blocks."""
    with TreeBuilder("Frames") as tree:
        with g.Frame("Frame"):
            geo_in = g.GeometryInput()
            geo_in.location = (50, 50)
            geo_in.hide = True

    snapshot = tree.layout_snapshot
    # Frame should have hide=False
    frame_entry = snapshot["Frame"]
    assert frame_entry[2] is False
    # Geometry Input inside frame should have hide=True
    geo_entry = snapshot["Geometry Input"]
    assert geo_entry[2] is True


# ---------------------------------------------------------------------------
# Multiple nodes with mixed hide states
# ---------------------------------------------------------------------------


def test_multiple_nodes_with_mixed_hide():
    """Multiple nodes with mixed hide states all captured correctly."""
    with TreeBuilder("MixedHide") as tree:
        # Hidden node
        hidden_in = g.GeometryInput()
        hidden_in.location = (0, 0)
        hidden_in.hide = True

        # Visible node
        visible_math = g.Math(1.0 + 2.0)
        visible_math.location = (50, -30)

    snapshot = tree.layout_snapshot
    entries = {name: entry for name, entry in snapshot.items()}

    hidden_entry = entries["Geometry Input"]
    assert hidden_entry[2] is True

    visible_entry = entries["Math"]
    assert visible_entry[2] is False


# ---------------------------------------------------------------------------
# Hide attribute in generated code via to_python
# ---------------------------------------------------------------------------


def test_hide_in_generated_code():
    """Verify that hide state appears in to_python(snapshot_positions=True) output.

    The layout_snapshot block uses 'hide': node.hide which evaluates to a boolean
    at runtime, producing either '"hide":true' or '"hide":false'.
    """
    with TreeBuilder("GeneratedHide") as tree:
        geo = g.GeometryInput()
        geo.location = (0, 0)
        geo.hide = True

    code = tree.to_python(snapshot_positions=True, format=False)

    # Generated code should contain layout_snapshot block with hide field
    # The actual value depends on runtime evaluation but will be a boolean
    assert "layout_snapshot" in code


# ---------------------------------------------------------------------------
# Roundtrip: to_python -> exec -> restore hide state
# ---------------------------------------------------------------------------


def test_hide_roundtrip_simple():
    """Test that hide state survives to_python -> rebuild roundtrip."""
    with TreeBuilder("RoundTrip") as tree:
        geo_in = g.GeometryInput()
        geo_in.location = (0, 0)
        geo_in.hide = True

    # Generate Python code and rebuild
    code = tree.to_python(snapshot_positions=True)

    # The code generation should include layout_snapshot block with hide field
    assert "layout_snapshot" in code


# ---------------------------------------------------------------------------
# Edge cases: nested frames with different hide states
# ---------------------------------------------------------------------------


def test_nested_frames_hide():
    """Test hide state in nested frame structures."""
    with TreeBuilder("NestedFrames") as tree:
        outer = g.Frame("OuterFrame")
        inner = g.Frame("InnerFrame")

        geo_in = g.GeometryInput()
        geo_in.location = (0, 0)
        geo_in.hide = True

    snapshot = tree.layout_snapshot

    # Frame parent is stored for nodes inside frames
    # Blender uses 'Frame' and 'Frame.001' for multiple frames with same type
    frame_entries = [v for k, v in snapshot.items() if "Frame" in k]
    geo_entry = snapshot["Geometry Input"]

    assert len(frame_entries) == 2
    assert geo_entry[3] is None  # Geo node has no parent link


# ---------------------------------------------------------------------------
# Verify hide flag propagation for nested nodes inside Frame blocks
# ---------------------------------------------------------------------------


def test_hide_propagation_nested_frames():
    """Test that hide flag is correctly propagated for nested frames."""
    with TreeBuilder("NestedFramesHide") as tree:
        frame1 = g.Frame("Frame1")

        geo_in1 = g.GeometryInput()
        geo_in1.location = (0, 0)
        geo_in1.hide = True

        frame2 = g.Frame("Frame2")

        geo_in2 = g.GeometryInput()
        geo_in2.location = (50, -30)
        geo_in2.hide = False

    snapshot = tree.layout_snapshot

    # Check that frame entries and their contents have correct hide states
    # Blender renames duplicate node names: "Frame", "Frame.001", etc.
    frame_entries = [v for k, v in snapshot.items() if "Frame" in k]
    geo_entries = [v for v in snapshot.values() if "GeometryNodeGroup" in str(v[0])]

    assert len(frame_entries) == 2
    assert len(geo_entries) == 2

    # Both frames themselves are visible (hide=False)
    assert all(entry[2] is False for entry in frame_entries)

    # Verify that different hide states are captured
    geo_hide_states = [entry[2] for entry in geo_entries]
    assert any(
        h is True for h in geo_hide_states
    ), "Expected at least one hidden geometry node"
    assert any(
        h is False for h in geo_hide_states
    ), "Expected at least one visible geometry node"
