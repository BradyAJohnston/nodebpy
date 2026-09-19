"""Tests for nodebpy.live — re-running source safely in a live session."""

import textwrap

import bpy
import pytest

from nodebpy import TreeBuilder
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.live import (
    GroupStash,
    RunResult,
    group_names_in_source,
    preserve_modifier_inputs,
    run_source,
    stash_groups,
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
        with TreeBuilder(other.tree, clear=True) as rebuilt:
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
