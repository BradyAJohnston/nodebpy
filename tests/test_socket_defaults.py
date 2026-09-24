# SPDX-License-Identifier: GPL-3.0-or-later
"""Generated constructor defaults must be Blender's own socket defaults.

The generator spells a float32 default as the shortest literal that rebuilds it
(``0.1``) or as a ``math.*`` expression (``7 * math.pi / 4``); anything looser
(``5.4978``) both changes the built node and makes ``to_python`` treat every
untouched node as edited.
"""

import inspect

import bpy
import numpy as np
import pytest

from nodebpy import compositor as c
from nodebpy import geometry as g
from nodebpy import shader as s
from nodebpy.builder import BaseNode
from nodebpy.export.codegen import _normalize, to_python


def _node_classes(module):
    return sorted(
        (
            cls
            for cls in vars(module).values()
            if isinstance(cls, type)
            and issubclass(cls, BaseNode)
            and getattr(cls, "_bl_idname", None)
        ),
        key=lambda cls: cls.__name__,
    )


def _as_f32(value):
    try:
        return tuple(np.float32(v) for v in value)
    except TypeError:
        return np.float32(value)


@pytest.mark.parametrize(
    ("module", "tree_type"),
    [
        (g, "GeometryNodeTree"),
        (s, "ShaderNodeTree"),
        (c, "CompositorNodeTree"),
    ],
    ids=["geometry", "shader", "compositor"],
)
def test_generated_defaults_match_fresh_node(module, tree_type):
    tree = bpy.data.node_groups.new("defaults", tree_type)
    mismatches = []
    for cls in _node_classes(module):
        try:
            node = tree.nodes.new(cls._bl_idname)
        except RuntimeError:
            continue  # not available in this tree type
        params = inspect.signature(cls.__init__).parameters
        for socket in node.inputs:
            default = params.get(_normalize(socket.identifier))
            fresh = getattr(socket, "default_value", None)
            if default is None or default.default is None or fresh is None:
                continue
            if isinstance(fresh, (bool, int, str)) or isinstance(default.default, str):
                continue
            if _as_f32(default.default) != _as_f32(fresh):
                mismatches.append(
                    (cls.__name__, socket.identifier, default.default, fresh)
                )
    assert not mismatches


def test_fresh_nodes_export_without_default_kwargs():
    with g.tree("Fresh Defaults") as tree:
        g.Arc()  # sweep angle is 7π/4, a float32 no 4-decimal literal reproduces
        g.MeshToPoints()  # radius 0.05 reads back as 0.05000000074505806
        g.SetPosition()  # vector default
        g.Arc(sweep_angle=3.0)
    lines = [ln.strip() for ln in to_python(tree.tree).splitlines() if "g." in ln]
    assert "_arc = g.Arc()" in lines
    assert "_arc_1 = g.Arc(sweep_angle=3.0)" in lines
    assert "_mesh_to_points = g.MeshToPoints()" in lines
    assert "_set_position = g.SetPosition()" in lines
