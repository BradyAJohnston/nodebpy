"""Worlds and the scene compositor."""

import bpy

from nodebpy import compositor as c
from nodebpy import shader as s


def test_world_builds_and_rebuilds_in_place():
    with s.world("Test Studio", clear=True) as studio:
        s.Background(strength=1.0) >> s.WorldOutput()
    assert [n.bl_idname for n in studio.tree.nodes] == [
        "ShaderNodeBackground",
        "ShaderNodeOutputWorld",
    ]
    count = len(bpy.data.worlds)
    with s.world("Test Studio", clear=True) as again:
        s.Background(strength=2.0) >> s.WorldOutput()
    assert again.world == studio.world
    assert len(bpy.data.worlds) == count
    assert len(again.tree.nodes) == 2


def test_world_and_compositor_can_be_the_scenes():
    with s.world("Scene World", clear=True, scene=True) as world:
        s.Background() >> s.WorldOutput()
    with c.tree("Scene Glow", clear=True, scene=True) as glow:
        image = glow.inputs.color("Image")
        c.Blur(image) >> glow.outputs.color("Image")
    scene = bpy.context.scene
    assert scene.world == world.world
    assert scene.compositing_node_group == glow.tree


def test_trees_leave_the_scene_alone_by_default():
    scene = bpy.context.scene
    before = scene.world
    with s.world("Not The Scene's", clear=True):
        s.Background() >> s.WorldOutput()
    assert scene.world == before
