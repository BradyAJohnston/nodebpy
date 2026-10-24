"""Tests for nodebpy.live — re-running source safely in a live session."""

import textwrap
import warnings

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.live import (
    EditedTreeWarning,
    GroupStash,
    RunResult,
    _fcurves,
    copy_asset,
    group_names_in_source,
    preserve_modifier_inputs,
    run_source,
    stash_groups,
    was_edited,
)


def _modifier(tree: bpy.types.NodeTree, name: str = "GN") -> bpy.types.NodesModifier:
    modifier = bpy.data.objects["Cube"].modifiers.new(name, "NODES")
    modifier.node_group = tree
    return modifier


def _input_value(modifier: bpy.types.NodesModifier, socket_name: str):
    assert modifier.node_group is not None
    item = next(
        i
        for i in modifier.node_group.interface.items_tree
        if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == socket_name
    )
    value = getattr(modifier.properties.inputs, item.identifier).value
    return tuple(value) if hasattr(value, "__len__") else value


def _set_input(modifier: bpy.types.NodesModifier, socket_name: str, value) -> None:
    assert modifier.node_group is not None
    item = next(
        i
        for i in modifier.node_group.interface.items_tree
        if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == socket_name
    )
    getattr(modifier.properties.inputs, item.identifier).value = value


# ---------------------------------------------------------------------------
# group_names_in_source
# ---------------------------------------------------------------------------


def test_group_names_in_source_reads_assign_and_annassign():
    code = textwrap.dedent(
        """
        class A(CustomGeometryGroup):
            _name = "Group A"

        class B(CustomGeometryGroup):
            _name: str = "Group B"
            _color_tag = "GEOMETRY"

        class NotAGroup:
            name = "no underscore"
            _name = other_variable

        _name = "module level, not a class body"
        """
    )
    assert group_names_in_source(code) == {"Group A", "Group B"}


def test_group_names_in_source_syntax_error_is_empty():
    assert group_names_in_source("class A(:\n    _name = 'x'") == set()


# ---------------------------------------------------------------------------
# stash_groups / GroupStash
# ---------------------------------------------------------------------------


class _Old(CustomGeometryGroup):
    _name = "Stash Me"

    def _build_group(self, tree):
        (
            tree.inputs.geometry("Geometry")
            >> g.SetPosition()
            >> tree.outputs.geometry("Geometry")
        )


def test_stash_and_restore_leaves_scene_unchanged():
    old = _Old.create_group()
    modifier = _modifier(old)
    names_before = {t.name for t in bpy.data.node_groups}

    stash = stash_groups(["Stash Me", "Never Existed"])
    assert set(stash.stashed) == {"Stash Me"}
    assert old.name == "Stash Me.stale"
    assert bpy.data.node_groups.get("Stash Me") is None

    # A partial build of the failed run under the original name.
    partial = bpy.data.node_groups.new("Stash Me", "GeometryNodeTree")
    assert partial.name == "Stash Me"
    stash.restore()

    assert old.name == "Stash Me"
    assert bpy.data.node_groups["Stash Me"] == old
    assert modifier.node_group == old
    assert {t.name for t in bpy.data.node_groups} == names_before
    assert not any(t.name.endswith(".stale") for t in bpy.data.node_groups)


def test_stash_and_replace_remaps_users_and_removes_old():
    old = _Old.create_group()
    modifier = _modifier(old)
    with g.tree("Parent") as parent:
        node = g.Group()
        node.node.node_tree = old
    group_node = parent.tree.nodes[node.node.name]

    stash = stash_groups(["Stash Me"])
    new = bpy.data.node_groups.new("Stash Me", "GeometryNodeTree")
    stash.replace()

    assert modifier.node_group == new
    assert group_node.node_tree == new
    assert bpy.data.node_groups.get("Stash Me.stale") is None
    assert bpy.data.node_groups["Stash Me"] == new


def test_stash_and_replace_keeps_old_when_nothing_replaced_it():
    old = _Old.create_group()
    stash = stash_groups(["Stash Me"])
    stash.replace()
    assert old.name == "Stash Me"
    assert bpy.data.node_groups["Stash Me"] == old


def test_stash_and_replace_ignores_new_tree_of_other_type():
    old = _Old.create_group()
    stash = stash_groups(["Stash Me"])
    other = bpy.data.node_groups.new("Stash Me", "ShaderNodeTree")
    stash.replace()
    assert bpy.data.node_groups.get("Stash Me.stale") is None
    assert other.name == "Stash Me"
    assert old.name == "Stash Me.001"


def test_group_stash_default_is_empty():
    assert GroupStash().stashed == {}


# ---------------------------------------------------------------------------
# preserve_modifier_inputs
# ---------------------------------------------------------------------------


def test_preserve_modifier_inputs_round_trips_across_rebuild():
    with g.tree("Preserve") as tree:
        tree.inputs.geometry("Geometry") >> tree.outputs.geometry("Geometry")
        tree.inputs.float("Scale")
        tree.inputs.vector("Offset")
        tree.inputs.integer("Removed")
        tree.inputs.boolean("Retyped")
    modifier = _modifier(tree.tree)
    _set_input(modifier, "Scale", 2.5)
    _set_input(modifier, "Offset", (1.0, 2.0, 3.0))
    _set_input(modifier, "Removed", 7)
    _set_input(modifier, "Retyped", True)
    old_identifiers = {i.identifier for i in tree.tree.interface.items_tree}

    with preserve_modifier_inputs([tree.tree]):
        with TreeBuilder(tree.tree, clear=True) as rebuilt:
            rebuilt.inputs.geometry("Geometry") >> rebuilt.outputs.geometry("Geometry")
            rebuilt.inputs.vector("Offset")
            rebuilt.inputs.float("Scale")
            rebuilt.inputs.float("Retyped")
            rebuilt.inputs.float("Added")

    # The identifiers really were regenerated — the values had to be carried.
    assert {i.identifier for i in tree.tree.interface.items_tree}.isdisjoint(
        old_identifiers
    )
    assert _input_value(modifier, "Scale") == 2.5
    assert _input_value(modifier, "Offset") == (1.0, 2.0, 3.0)
    assert _input_value(modifier, "Retyped") == 0.0  # type changed: skipped
    assert _input_value(modifier, "Added") == 0.0
    assert "Removed" not in {i.name for i in tree.tree.interface.items_tree}


def test_preserve_modifier_inputs_ignores_other_trees():
    with g.tree("Other") as other:
        other.inputs.geometry("Geometry") >> other.outputs.geometry("Geometry")
        other.inputs.float("Scale")
    modifier = _modifier(other.tree)
    _set_input(modifier, "Scale", 4.0)
    with g.tree("Unrelated") as unrelated:
        pass
    with preserve_modifier_inputs([unrelated.tree]):
        # rebuild the interface by hand: clear=True would preserve the values
        other.tree.nodes.clear()
        other.tree.interface.clear()
        with TreeBuilder(other.tree) as rebuilt:
            rebuilt.inputs.geometry("Geometry") >> rebuilt.outputs.geometry("Geometry")
            rebuilt.inputs.float("Scale")
    assert _input_value(modifier, "Scale") == 0.0


# ---------------------------------------------------------------------------
# run_source
# ---------------------------------------------------------------------------

WITH_FORM = textwrap.dedent(
    """
    from nodebpy import geometry as g

    with g.tree("Live Tree", clear=True) as tree:
        tree.inputs.geometry("Geometry") >> g.SetPosition() >> tree.outputs.geometry(
            "Geometry"
        )
        tree.inputs.float("Scale")
    """
)

CLASS_FORM = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup

    class LiveGroup(CustomGeometryGroup):
        _name = "Live Group"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            tree.inputs.float("Scale")
            {body}
            geo >> tree.outputs.geometry("Geometry")
    """
)


def test_run_source_with_form_returns_the_tree():
    result = run_source(WITH_FORM)
    assert isinstance(result, RunResult)
    assert result.tree is not None
    assert result.tree.name == "Live Tree"
    assert result.tree == result.namespace["tree"].tree
    assert result.created == [result.tree]
    assert result.namespace["__name__"] == "__nodebpy_live__"
    assert result.namespace["bpy"] is bpy

    # Running again rebuilds the same datablock: nothing new is created.
    again = run_source(WITH_FORM)
    assert again.tree == result.tree
    assert again.created == []


def test_run_source_with_form_preserves_modifier_inputs():
    first = run_source(WITH_FORM)
    assert first.tree is not None
    modifier = _modifier(first.tree)
    _set_input(modifier, "Scale", 3.0)
    run_source(WITH_FORM)
    assert modifier.node_group == first.tree
    assert _input_value(modifier, "Scale") == 3.0


def test_run_source_class_form_rebuilds_on_change():
    first = run_source(CLASS_FORM.format(body="pass"))
    assert first.tree is not None
    assert first.tree.name == "Live Group"
    assert first.tree.bl_idname == "GeometryNodeTree"
    first_count = len(first.tree.nodes)
    modifier = _modifier(first.tree)
    _set_input(modifier, "Scale", 1.5)
    with g.tree("Holder") as holder:
        node = g.Group()
        node.node.node_tree = first.tree
    group_node = holder.tree.nodes[node.node.name]

    second = run_source(CLASS_FORM.format(body="g.SetPosition(geo)\n        g.Cube()"))
    assert second.tree is not None
    assert second.tree.name == "Live Group"
    assert len(second.tree.nodes) == first_count + 2
    assert second.created == [second.tree]
    # Users moved to the rebuilt tree; the old one is gone.
    assert modifier.node_group == second.tree
    assert group_node.node_tree == second.tree
    assert _input_value(modifier, "Scale") == 1.5
    assert bpy.data.node_groups.get("Live Group.stale") is None
    assert [t.name for t in bpy.data.node_groups if t.name.startswith("Live")] == [
        "Live Group"
    ]


def test_run_source_class_form_keeps_asset_status():
    first = run_source(CLASS_FORM.format(body="pass")).tree
    assert first is not None
    first.asset_mark()
    asset = first.asset_data
    asset.description = "Moves things"
    asset.author = "Someone"
    asset.catalog_id = "12345678-1234-1234-1234-123456789abc"
    asset.tags.new("deform")
    preview = first.preview_ensure()
    preview.image_size = (2, 2)
    preview.image_pixels_float = [0.25] * 16

    second = run_source(CLASS_FORM.format(body="g.Cube()")).tree

    assert second is not None and second != first
    asset = second.asset_data
    assert asset is not None
    assert asset.description == "Moves things"
    assert asset.author == "Someone"
    assert asset.catalog_id == "12345678-1234-1234-1234-123456789abc"
    assert [tag.name for tag in asset.tags] == ["deform"]
    assert second.preview.is_image_custom
    assert tuple(second.preview.image_size) == (2, 2)
    # Previews are stored as 8-bit pixels.
    pixels = list(second.preview.image_pixels_float)
    assert pixels == pytest.approx([0.25] * 16, abs=1 / 255)


def test_copy_asset_leaves_a_marked_or_unmarked_target_alone():
    old = bpy.data.node_groups.new("Old", "GeometryNodeTree")
    new = bpy.data.node_groups.new("New", "GeometryNodeTree")
    copy_asset(old, new)
    assert new.asset_data is None

    old.asset_mark()
    old.asset_data.description = "old"
    new.asset_mark()
    new.asset_data.description = "built"
    copy_asset(old, new)
    assert new.asset_data.description == "built"


def test_run_source_class_form_with_explicit_create_group():
    code = CLASS_FORM.format(body="pass") + "\ntree = LiveGroup.create_group()\n"
    result = run_source(code)
    assert result.tree is not None
    assert result.tree == result.namespace["tree"]


def test_run_source_picks_top_level_of_nested_groups():
    code = textwrap.dedent(
        """
        from nodebpy import geometry as g
        from nodebpy.builder import CustomGeometryGroup

        class Inner(CustomGeometryGroup):
            _name = "Inner"

            def _build_group(self, tree):
                tree.inputs.geometry("Geometry") >> tree.outputs.geometry("Geometry")

        with g.tree("Outer") as outer:
            outer.inputs.geometry("Geometry") >> Inner() >> outer.outputs.geometry(
                "Geometry"
            )
        """
    )
    result = run_source(code)
    assert result.tree is not None
    assert result.tree.name == "Outer"
    assert sorted(t.name for t in result.created) == ["Inner", "Outer"]


def test_run_source_no_tree_returns_none():
    result = run_source("x = 1 + 1\n")
    assert result.tree is None
    assert result.created == []
    assert result.namespace["x"] == 2


def test_run_source_namespace_and_filename():
    result = run_source(
        "value = injected * 2\nname = __file__\n",
        filename="/tmp/live_script.py",
        namespace={"injected": 21},
    )
    assert result.namespace["value"] == 42
    assert result.namespace["name"] == "/tmp/live_script.py"


def test_run_source_reraises_original_exception_with_filename():
    class Boom(RuntimeError):
        pass

    with pytest.raises(Boom) as info:
        run_source(
            "x = 1\nraise Boom('bang')\n",
            filename="Text.001",
            namespace={"Boom": Boom},
        )
    assert str(info.value) == "bang"
    frames = info.traceback
    assert any(str(f.path) == "Text.001" and f.lineno + 1 == 2 for f in frames)


def test_run_source_failure_restores_stashed_group():
    first = run_source(CLASS_FORM.format(body="pass"))
    assert first.tree is not None
    modifier = _modifier(first.tree)
    names_before = {t.name for t in bpy.data.node_groups}

    failing = CLASS_FORM.format(body="raise ValueError('broken build')")
    failing += "\ntree = LiveGroup.create_group()\n"
    with pytest.raises(ValueError, match="broken build"):
        run_source(failing)

    assert bpy.data.node_groups["Live Group"] == first.tree
    assert modifier.node_group == first.tree
    assert {t.name for t in bpy.data.node_groups} == names_before


# ---------------------------------------------------------------------------
# Review follow-ups
# ---------------------------------------------------------------------------


def test_preserve_modifier_inputs_reapplies_when_body_raises():
    first = run_source(WITH_FORM)
    assert first.tree is not None
    modifier = _modifier(first.tree)
    _set_input(modifier, "Scale", 7.0)

    # The failing edit comes after the sockets are declared, as a half-typed
    # line at the end of the body would.
    failing = WITH_FORM + "    raise ValueError('half typed')\n"
    with pytest.raises(ValueError, match="half typed"):
        run_source(failing)
    assert modifier.node_group == first.tree
    assert _input_value(modifier, "Scale") == 7.0

    # And the value survives into the next successful run.
    run_source(WITH_FORM)
    assert _input_value(modifier, "Scale") == 7.0


def test_preserve_modifier_inputs_keeps_attribute_mode():
    first = run_source(WITH_FORM)
    assert first.tree is not None
    modifier = _modifier(first.tree)
    item = next(
        i
        for i in first.tree.interface.items_tree
        if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == "Scale"
    )
    wrapper = getattr(modifier.properties.inputs, item.identifier)
    wrapper.type = "ATTRIBUTE"
    wrapper.attribute_name = "my_attr"

    run_source(WITH_FORM)

    item = next(
        i
        for i in first.tree.interface.items_tree
        if i.item_type == "SOCKET" and i.in_out == "INPUT" and i.name == "Scale"
    )
    wrapper = getattr(modifier.properties.inputs, item.identifier)
    assert wrapper.type == "ATTRIBUTE"
    assert wrapper.attribute_name == "my_attr"


def test_stash_groups_skips_linked_asset_group():
    from nodebpy.nodes.geometry.assets import Array

    linked = Array.create_group()
    assert linked.library is not None

    stash = stash_groups(["Array"])
    assert stash.stashed == {}
    assert linked.name == "Array"
    # A class claiming that name reuses the linked group rather than failing.
    result = run_source(
        textwrap.dedent(
            """
            from nodebpy.nodes.geometry.assets import Array
            tree = Array.create_group()
            """
        )
    )
    assert result.tree == linked


TWO_CLASSES = textwrap.dedent(
    """
    from nodebpy.builder import CustomGeometryGroup

    class Unused(CustomGeometryGroup):
        _name = "Unused Group"

        def _build_group(self, tree):
            tree.inputs.geometry("Geometry") >> tree.outputs.geometry("Geometry")

    class Built(CustomGeometryGroup):
        _name = "Built Group"

        def _build_group(self, tree):
            tree.inputs.geometry("Geometry") >> tree.outputs.geometry("Geometry")

    {calls}
    """
)


def test_run_source_created_excludes_restored_stashed_group():
    run_source(TWO_CLASSES.format(calls="Unused.create_group()\nBuilt.create_group()"))
    unused = bpy.data.node_groups["Unused Group"]

    result = run_source(TWO_CLASSES.format(calls="Built.create_group()"))

    assert bpy.data.node_groups["Unused Group"] == unused
    assert [t.name for t in result.created] == ["Built Group"]


def test_run_source_ignores_tree_carried_over_in_namespace():
    first = run_source(WITH_FORM)
    assert first.tree is not None

    second = run_source(
        TWO_CLASSES.format(calls="Built.create_group()"), namespace=first.namespace
    )

    assert second.tree is not None
    assert second.tree.name == "Built Group"


def test_group_stash_replace_and_restore_are_idempotent():
    old = _Old.create_group()
    stash = stash_groups(["Stash Me"])
    new = bpy.data.node_groups.new("Stash Me", "GeometryNodeTree")
    stash.replace()
    assert stash.stashed == {}
    stash.replace()
    stash.restore()
    assert bpy.data.node_groups["Stash Me"] == new

    stash = stash_groups(["Stash Me"])
    stash.restore()
    assert stash.stashed == {}
    stash.restore()
    assert new.name == "Stash Me"
    del old


# ---------------------------------------------------------------------------
# animation across rebuilds
# ---------------------------------------------------------------------------


def _animated(first="multiply", **kwargs):
    with g.tree("Animated", clear=True, **kwargs) as tree:
        geo = tree.inputs.geometry("Geometry")
        tree.inputs.float("Extra")
        scale = tree.inputs.float("Scale", 1.0)
        if first != "multiply":
            scale = g.Math(scale, 3.0, operation=first.upper()).o.value
        value = g.Math.multiply(scale, 2.0)
        offset = g.CombineXYZ(z=value)
        geo >> g.SetPosition(offset=offset) >> tree.outputs.geometry("Geometry")
    return tree.tree


def _paths(owner):
    return sorted(curve.data_path for curve in _fcurves(owner))


def _multiply(tree):
    return next(
        n
        for n in tree.nodes
        if n.bl_idname == "ShaderNodeMath" and n.operation == "MULTIPLY"
    )


def test_rebuild_keeps_modifier_input_keyframes():
    tree = _animated()
    modifier = _modifier(tree)
    obj = modifier.id_data
    _set_input(modifier, "Scale", 1.0)
    item = next(i for i in tree.interface.items_tree if i.name == "Scale")
    path = getattr(modifier.properties.inputs, item.identifier).path_from_id("value")
    obj.keyframe_insert(path, frame=1)
    _set_input(modifier, "Scale", 4.0)
    obj.keyframe_insert(path, frame=10)

    _animated()

    item = next(i for i in tree.interface.items_tree if i.name == "Scale")
    (path,) = _paths(obj)
    assert path == f'modifiers["GN"].properties.inputs.{item.identifier}.value'
    assert obj.path_resolve(path) == 4.0


def test_rebuild_keeps_node_keyframes_and_drivers():
    tree = _animated()
    multiply = _multiply(tree)
    multiply.inputs[1].default_value = 2.0
    multiply.inputs[1].keyframe_insert("default_value", frame=1)
    multiply.inputs[1].default_value = 6.0
    multiply.inputs[1].keyframe_insert("default_value", frame=10)
    driver = multiply.inputs[0].driver_add("default_value")
    driver.driver.expression = "frame"

    # A node built before it takes its name.
    _animated(first="add")

    multiply = _multiply(tree)
    assert multiply.name != "Math"
    prefix = f'nodes["{multiply.name}"]'
    assert _paths(tree) == [
        f"{prefix}.inputs[0].default_value",
        f"{prefix}.inputs[1].default_value",
    ]
    (keyed,) = [c for c in _fcurves(tree) if c.data_path.endswith("[1].default_value")]
    assert keyed.evaluate(10) == pytest.approx(6.0)
    assert tree.animation_data.drivers[0].driver.expression == "frame"


def test_rebuild_warns_about_animation_it_cannot_place():
    tree = _animated(first="add")
    add = next(
        n
        for n in tree.nodes
        if n.bl_idname == "ShaderNodeMath" and n.operation == "ADD"
    )
    add.inputs[1].keyframe_insert("default_value", frame=1)
    path = f'nodes["{add.name}"].inputs[1].default_value'

    with pytest.warns(UserWarning, match="Kept the animation of 'Animated'"):
        _animated()

    assert _paths(tree) == [path]


ANIMATED_CLASS = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup

    class Animated(CustomGeometryGroup):
        _name = "Animated Group"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            {body}
            value = g.Math.multiply(1.0, 2.0)
            geo >> g.SetPosition(offset=g.CombineXYZ(z=value)) >> tree.outputs.geometry("Geometry")
    """
)


def test_run_source_moves_group_animation_to_the_rebuild():
    first = run_source(ANIMATED_CLASS.format(body="pass")).tree
    assert first is not None
    multiply = _multiply(first)
    multiply.inputs[1].keyframe_insert("default_value", frame=1)
    multiply.inputs[0].driver_add("default_value").driver.expression = "frame"
    action = first.animation_data.action

    second = run_source(ANIMATED_CLASS.format(body="g.Cube()")).tree

    assert second is not None and second != first
    assert second.animation_data.action == action
    multiply = _multiply(second)
    prefix = f'nodes["{multiply.name}"]'
    assert _paths(second) == [
        f"{prefix}.inputs[0].default_value",
        f"{prefix}.inputs[1].default_value",
    ]


def test_rebuild_keeps_nla_strips_and_tree_drivers():
    tree = _animated()
    multiply = _multiply(tree)
    multiply.inputs[1].keyframe_insert("default_value", frame=1)
    animation = tree.animation_data
    track = animation.nla_tracks.new()
    track.strips.new("Pushed", 1, animation.action)
    animation.action = None
    # A driver on a property of the tree, which addresses no node.
    tree["amount"] = 1.0
    tree.driver_add('["amount"]').driver.expression = "2"

    _animated(first="add")

    multiply = _multiply(tree)
    assert _paths(tree) == sorted(
        ['["amount"]', f'nodes["{multiply.name}"].inputs[1].default_value']
    )


# ---------------------------------------------------------------------------
# changes made by hand
# ---------------------------------------------------------------------------


def test_rebuild_keeps_a_hand_edited_tree():
    tree = _animated()
    assert not was_edited(tree)
    _multiply(tree).inputs[1].default_value = 9.0
    assert was_edited(tree)

    with pytest.warns(EditedTreeWarning, match="'Animated' was changed by hand"):
        _animated()

    backup = bpy.data.node_groups["Animated (edited)"]
    assert backup.use_fake_user
    assert _multiply(backup).inputs[1].default_value == 9.0
    assert _multiply(tree).inputs[1].default_value == 2.0
    assert not was_edited(tree)


def test_layout_names_animation_and_reroutes_are_not_edits():
    tree = _animated()
    multiply = _multiply(tree)
    multiply.location = (500.0, 500.0)
    multiply.label = "Double"
    multiply.name = "Doubler"
    multiply.hide = True
    multiply.inputs[1].keyframe_insert("default_value", frame=1)
    multiply.inputs[1].default_value = 7.0  # animated, so it follows the frame
    link = multiply.outputs[0].links[0]
    target = link.to_socket
    reroute = tree.nodes.new("NodeReroute")
    tree.links.new(multiply.outputs[0], reroute.inputs[0])
    tree.links.new(reroute.outputs[0], target)
    assert not was_edited(tree)


@pytest.mark.parametrize(
    "edit",
    [
        lambda tree: setattr(_multiply(tree), "mute", True),
        lambda tree: setattr(_multiply(tree), "operation", "ADD"),
        lambda tree: tree.links.remove(_multiply(tree).outputs[0].links[0]),
        lambda tree: tree.nodes.new("GeometryNodeMeshCube"),
        lambda tree: tree.nodes.new("NodeGroupInput"),
        lambda tree: tree.interface.new_socket("Added", socket_type="NodeSocketFloat"),
    ],
    ids=["mute", "setting", "link", "node", "another-alike", "interface"],
)
def test_changes_that_are_edits(edit):
    tree = _animated()
    edit(tree)
    assert was_edited(tree)


def test_run_source_keeps_a_hand_edited_group():
    first = run_source(ANIMATED_CLASS.format(body="pass")).tree
    assert first is not None
    first.asset_mark()
    _multiply(first).inputs[0].default_value = 4.0

    with pytest.warns(EditedTreeWarning):
        second = run_source(ANIMATED_CLASS.format(body="pass")).tree

    backup = bpy.data.node_groups["Animated Group (edited)"]
    assert backup == first
    assert backup.asset_data is None and backup.users == 1  # the fake user
    assert second is not None and second.name == "Animated Group"
    assert _multiply(second).inputs[0].default_value == 1.0
    assert second.asset_data is not None
    # Not edited since this build: the next run replaces it quietly.
    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        run_source(ANIMATED_CLASS.format(body="pass"))


def test_second_hand_edited_rebuild_replaces_the_backup():
    tree = _animated()
    _multiply(tree).inputs[1].default_value = 9.0
    with pytest.warns(EditedTreeWarning):
        _animated()
    _multiply(tree).inputs[1].default_value = 5.0
    with pytest.warns(EditedTreeWarning):
        _animated()
    backups = [
        t for t in bpy.data.node_groups if t.name.startswith("Animated (edited)")
    ]
    assert [_multiply(t).inputs[1].default_value for t in backups] == [5.0]


def test_rebuilding_a_group_does_not_edit_its_users():
    def build():
        with g.tree("Inner", clear=True) as inner:
            inner.inputs.float("Value") >> inner.outputs.float("Value")
        with g.tree("Outer", clear=True) as outer:
            node = outer.tree.nodes.new("GeometryNodeGroup")
            node.node_tree = inner.tree
            outer.tree.links.new(g.Index().node.outputs[0], node.inputs["Value"])
            g.Points(10) >> outer.outputs.geometry("Geometry")
        return outer.tree

    outer = build()
    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        build()
    assert len(outer.links) == 2


def test_run_source_does_not_edit_users_of_a_group_class():
    code = ANIMATED_CLASS.format(body="pass") + textwrap.dedent(
        """
        with g.tree("Holder", clear=True) as holder:
            Animated() >> holder.outputs.geometry("Geometry")
        """
    )
    run_source(code)
    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        run_source(code)


def test_failed_run_does_not_edit_users_of_a_group_class():
    code = ANIMATED_CLASS.format(body="pass") + textwrap.dedent(
        """
        with g.tree("Holder", clear=True) as holder:
            Animated() >> holder.outputs.geometry("Geometry")
        """
    )
    run_source(code)
    with pytest.raises(ZeroDivisionError):
        run_source(ANIMATED_CLASS.format(body="1 / 0") + "\nAnimated.create_group()")
    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        run_source(code)


# ---------------------------------------------------------------------------
# GroupLinks: group nodes keep their links when their group is rebuilt
# ---------------------------------------------------------------------------


def _inner(extra=False, amount=1.0, drop_out=False):
    with g.tree("Inner", clear=True) as inner:
        geo = inner.inputs.geometry("Geometry")
        if extra:
            inner.inputs.float("Extra")
        value = inner.inputs.float("Amount", amount)
        inner.inputs.float("Amount", 0.5)
        geo >> g.SetPosition(offset=(0, 0, value)) >> inner.outputs.geometry("Geometry")
        if not drop_out:
            (value * 2) >> inner.outputs.float("Out")
    return inner.tree


def _links(tree):
    """Each link by node names and socket names, a repeated socket name
    numbered by its place among those of that name."""

    def ref(socket):
        sockets = socket.node.outputs if socket.is_output else socket.node.inputs
        same = [s.identifier for s in sockets if s.name == socket.name]
        return (socket.node.name, socket.name, same.index(socket.identifier))

    return sorted((ref(link.from_socket), ref(link.to_socket)) for link in tree.links)


def _outer():
    group = bpy.data.node_groups["Inner"]
    with TreeBuilder("Outer", arrange=None) as outer:
        geo = outer.inputs.geometry("Geometry")
        first = g.Group()
        first.node.node_tree = group
        second = g.Group()
        second.node.node_tree = group
        links = outer.tree.links
        links.new(geo.socket, first.node.inputs["Geometry"])
        first.node.inputs[1].default_value = 3.0
        # The second "Amount", and a link between two nodes of the group.
        links.new(g.Index().node.outputs[0], first.node.inputs[2])
        links.new(first.node.outputs["Geometry"], second.node.inputs["Geometry"])
        links.new(first.node.outputs["Out"], second.node.inputs[1])
        join = g.JoinGeometry()
        links.new(second.node.outputs["Geometry"], join.node.inputs[0])
        links.new(first.node.outputs["Geometry"], join.node.inputs[0])
        join >> outer.outputs.geometry("Geometry")
    return outer.tree


def test_clear_rebuild_keeps_the_links_of_its_group_nodes():
    _inner()
    outer = _outer()
    before = _links(outer)

    _inner(extra=True, amount=2.0)

    assert _links(outer) == before
    first, second = outer.nodes["Group"], outer.nodes["Group.001"]
    assert first.inputs["Amount"].default_value == 3.0  # set on the node
    assert second.inputs["Extra"].default_value == 0.0
    # Untouched values follow the rebuilt interface's defaults.
    assert first.inputs[3].default_value == 0.5
    assert not was_edited(outer)


def test_sockets_the_rebuild_drops_lose_their_links():
    _inner()
    outer = _outer()

    _inner(drop_out=True)

    assert "Out" not in [link.from_socket.name for link in outer.links]
    assert outer.nodes["Group.001"].inputs["Amount"].default_value == 1.0


def test_run_source_keeps_the_links_of_a_group_class():
    code = textwrap.dedent(
        """
        from nodebpy import geometry as g
        from nodebpy.builder import CustomGeometryGroup

        class Inner(CustomGeometryGroup):
            _name = "Inner"

            def _build_group(self, tree):
                geo = tree.inputs.geometry("Geometry")
                {extra}
                value = tree.inputs.float("Amount", 1.0)
                tree.inputs.float("Amount", 0.5)
                geo >> g.SetPosition(offset=(0, 0, value)) >> tree.outputs.geometry("Geometry")
                (value * 2) >> tree.outputs.float("Out")
        """
    )
    run_source(code.format(extra="pass"))
    outer = _outer()
    before = _links(outer)

    run_source(code.format(extra='tree.inputs.float("Extra")'))

    assert outer.nodes["Group"].node_tree == bpy.data.node_groups["Inner"]
    assert _links(outer) == before
    assert outer.nodes["Group"].inputs["Amount"].default_value == 3.0


def test_links_to_removed_nodes_are_left_out():
    from nodebpy.live import GroupLinks

    group = _inner()
    outer = _outer()
    links = GroupLinks(group)
    outer.nodes.remove(outer.nodes["Index"])
    outer.nodes.remove(outer.nodes["Join Geometry"])

    links.restore()

    assert len(outer.links) == 3


# ---------------------------------------------------------------------------
# RunResult.to_python
# ---------------------------------------------------------------------------

LIVE_SCRIPT = textwrap.dedent(
    """
    from nodebpy import geometry as g
    from nodebpy.builder import CustomGeometryGroup

    class Offset(CustomGeometryGroup):
        _name = "Offset"

        def _build_group(self, tree):
            geo = tree.inputs.geometry("Geometry")
            amount = tree.inputs.float("Amount", 1.0)
            geo >> g.SetPosition(offset=(0, 0, amount)) >> tree.outputs.geometry("Geometry")

    {body}
    """
)
WITH_BODY = """
with g.tree("Live", clear=True) as tree:
    geo = tree.inputs.geometry("Geometry")
    geo >> g.Array(count=4) >> Offset(Amount=2.0) >> tree.outputs.geometry("Geometry")
"""


def test_run_result_to_python_writes_the_edited_tree_only():
    result = run_source(LIVE_SCRIPT.format(body=WITH_BODY))
    assert result.tree is not None
    result.tree.nodes.new("GeometryNodeSubdivisionSurface")

    code = result.to_python()

    assert "class " not in code
    assert 'with TreeBuilder("Live", clear=True) as tree:' in code
    assert "Offset(Geometry=g.Array(geometry=geometry, count=4), Amount=2.0)" in code
    assert "g.SubdivisionSurface()" in code

    # Back into the script, in place of the with block.
    again = run_source(LIVE_SCRIPT.format(body=code))
    assert again.tree == result.tree
    assert "Subdivision Surface" in again.tree.nodes


def test_run_result_to_python_writes_a_class_back_as_the_class():
    result = run_source(LIVE_SCRIPT.format(body=""))
    assert result.tree is not None and result.tree.name == "Offset"

    code = result.to_python()

    assert "class Offset(CustomGeometryGroup):" in code
    assert "with TreeBuilder" not in code
    assert result.to_python(top_level="with").startswith("from nodebpy import")


def test_run_result_to_python_without_a_tree():
    with pytest.raises(ValueError, match="no tree"):
        run_source("x = 1").to_python()


def _backups():
    return [t.name for t in bpy.data.node_groups if t.name.endswith("(edited)")]


def test_rerunning_the_written_out_code_keeps_no_backup():
    result = run_source(LIVE_SCRIPT.format(body=WITH_BODY))
    assert result.tree is not None
    result.tree.nodes.new("GeometryNodeSubdivisionSurface")
    code = LIVE_SCRIPT.format(body=result.to_python())

    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        again = run_source(code)
    assert _backups() == []
    assert [t.name for t in again.created] == ["Offset"]  # the class, rebuilt

    # A hand edit the code doesn't have is still kept.
    result.tree.nodes.new("GeometryNodeMeshToPoints")
    with pytest.warns(EditedTreeWarning):
        run_source(code)
    assert _backups() == ["Live (edited)"]


def test_written_out_class_reruns_without_a_backup():
    result = run_source(LIVE_SCRIPT.format(body=""))
    assert result.tree is not None
    result.tree.nodes["Set Position"].mute = True
    code = result.to_python()

    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        run_source(code)
    assert _backups() == []


def test_written_out_code_rebuilds_without_a_backup_outside_run_source():
    with g.tree("Plain", clear=True) as tree:
        g.Points(3) >> tree.outputs.geometry("Geometry")
    tree.tree.nodes["Points"].inputs["Count"].default_value = 9
    code = tree.to_python(in_place=True)

    with warnings.catch_warnings():
        warnings.simplefilter("error", EditedTreeWarning)
        exec(code, {})  # noqa: S102
    assert _backups() == []
    assert tree.tree.nodes["Points"].inputs["Count"].default_value == 9


def test_failed_run_keeps_the_edited_tree():
    result = run_source(LIVE_SCRIPT.format(body=WITH_BODY))
    assert result.tree is not None
    result.tree.nodes.new("GeometryNodeSubdivisionSurface")
    failing = WITH_BODY.replace(
        'geo = tree.inputs.geometry("Geometry")',
        'geo = tree.inputs.geometry("Geometry")\n    1 / 0',
    )

    with pytest.warns(EditedTreeWarning), pytest.raises(ZeroDivisionError):
        run_source(LIVE_SCRIPT.format(body=failing))
    assert _backups() == ["Live (edited)"]
