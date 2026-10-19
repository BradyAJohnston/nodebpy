"""Evaluate socket values by running the tree as a modifier."""

import bpy
import databpy as db
import numpy as np

from nodebpy import geometry as g

_DATA_TYPES = {
    "VALUE": "FLOAT",
    "INT": "INT",
    "BOOLEAN": "BOOLEAN",
    "VECTOR": "FLOAT_VECTOR",
    "RGBA": "FLOAT_COLOR",
}


def evaluate(tree, **values) -> dict[str, np.ndarray]:
    """The evaluated value of each socket in *values*, keyed by name.

    Call inside the tree's ``with`` block: each value is stored as an
    attribute on a single-vertex mesh, which becomes the tree's output.
    """
    geometry = g.MeshLine(count=1).o.mesh
    for name, value in values.items():
        data_type = _DATA_TYPES[value.socket.type]
        geometry = g.StoreNamedAttribute(
            geometry, name=name, value=value, data_type=data_type
        ).o.geometry
    geometry >> tree.outputs.geometry("Geometry")

    obj = bpy.data.objects.new("Evaluate", bpy.data.meshes.new("Evaluate"))
    bpy.context.scene.collection.objects.link(obj)
    obj.modifiers.new("Evaluate", "NODES").node_group = tree.tree
    try:
        return {
            name: db.named_attribute(obj, name, evaluate=True)[0] for name in values
        }
    finally:
        bpy.data.objects.remove(obj)
