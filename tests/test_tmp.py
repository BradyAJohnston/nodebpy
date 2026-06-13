import os
from collections import Counter
import bpy
from nodebpy import TreeBuilder
from nodebpy.export.codegen import to_python
from tests.test_codegen import _structure


def diff(name):
    df = bpy.utils.system_resource("DATAFILES")
    with bpy.data.libraries.load(os.path.join(df, "assets/nodes/geometry_nodes_essentials.blend"), assets_only=True) as (s, d):
        d.node_groups = [name]
    ng = bpy.data.node_groups[name]
    try:
        ns = {}; exec(to_python(TreeBuilder.geometry(ng)), ns)
    except Exception as e:
        print(f"{name}: {type(e).__name__}: {str(e)[:55]}"); return
    a, b = _structure(ng), _structure(ns["tree"].tree)
    ok = a == b
    print(f"{name}: {'PASS' if ok else 'MISMATCH'}")
    if not ok:
        ca, cb = Counter(map(tuple, a[1])), Counter(map(tuple, b[1]))
        for x in list((ca-cb).elements())[:3]: print("  ORIG:", x)
        for x in list((cb-ca).elements())[:3]: print("  REBUILT:", x)


def test_diff():
    diff("Array")
    diff("Scatter on Surface")
