# Existing trees, group classes and asset libraries

## Contents
1. Rebuilding a tree in place
2. Starting from a tree's code (`to_python`)
3. Live re-runs in a Blender session
4. Group classes
5. Essentials and asset libraries

## 1. Rebuilding a tree in place

- `with g.tree("Name", clear=True) as tree:` reuses the datablock called "Name"
  (creating it if missing) and empties it, so modifiers and group nodes pointing at it
  stay attached. Without `clear=True` the same name makes `Name.001`, and the modifier
  still shows the old tree. `s.tree`, `s.material` and `c.tree` take `clear=` too; for
  a tree you hold, `TreeBuilder(existing_bpy_tree, clear=True)`.
- `clear=True` carries Geometry Nodes modifier input values, and their keyframes and
  drivers, over by socket name, so keep input names unchanged when editing a tree a
  user has tuned. Keyframes and drivers on node values move to the matching node of the
  rebuild; any it can't place stay on their old path and raise a warning. It also keeps
  the `is_modifier` / `is_tool` flags, but resets simulation caches.
- A rebuild of a tree someone changed by hand (nodes, links, values, the interface)
  since it was built keeps the changed tree as `"<name> (edited)"` and raises an
  `EditedTreeWarning`; compare the two and fold the user's changes into the code.
- `keep_edits=True` (with `clear=True`) keeps the layout a user gave the tree since it
  was last arranged: moved, resized, collapsed, coloured, relabelled and framed nodes
  stay as they were on the nodes that still match, and new nodes go beside their
  neighbours. A tree nobody touched is arranged afresh.
- Wire nodes with nodebpy, not `tree.links.new(...)`. Tweaking a property on an
  existing node through bpy is fine.

**Setting modifier inputs (Blender 5).** `mod["Socket_0"] = 1.0` raises
`TypeError: id properties not supported`; go through the socket identifier:

```python
ident = {i.name: i.identifier for i in tree.tree.interface.items_tree
         if i.item_type == "SOCKET" and i.in_out == "INPUT"}
getattr(mod.properties.inputs, ident["Count"]).value = 100
obj.update_tag()   # headless: otherwise the next evaluated_get() can be stale
```

## 2. Starting from a tree's code

Turn the existing tree into code and edit that, rather than reverse-engineering it:

```python
from nodebpy.export import to_python

print(to_python(bpy.data.node_groups["My Tree"], in_place=True))   # rebuilds that datablock
print(to_python(obj.modifiers["GeometryNodes"].node_group))
print(to_python(bpy.data.materials["Mat"].node_tree))
```

It works on hand-made trees too, and `tree.to_python()` on a builder. Options:

- `in_place=True`: the header uses `clear=True`, so the code rebuilds the same datablock.
- `top_level="class"`: emits a `CustomGeometryGroup` subclass (`Cls.create_group()`).
- `snapshot_positions=True`: keeps hand-made positions (`arrange=None` plus positions).
- `min_chain_length=3`, `format=True` (ruff, if installed).
- `strict=True` raises `CodegenError` for a node with no nodebpy class; `strict=False`
  emits a placeholder, or register one: `from nodebpy.export.codegen import register_emitter`.
  Blender's deprecated compositor Switch is rebuilt as `c.Switch.color(...)`.

Round-trip check after editing generated code:

```python
code = to_python(tree)
ns = {}
exec(code, ns)
assert len(ns["tree"]) == len(tree)
```

## 3. Live re-runs in a Blender session

Re-running a script in one Blender (text editor, MCP `execute_blender_code`) with a
plain `exec` reuses stale group classes and piles up `.001` trees.
`nodebpy.live.run_source` handles both:

```python
from nodebpy.live import run_source

result = run_source(code_string, filename="build_tree.py")
result.tree        # the tree the run produced (or None)
result.created     # node groups that did not exist before
```

It rebuilds the groups the code's classes claim, remaps their users, keeps modifier
input values by socket name and layout edits (as `keep_edits=True`; pass
`keep_edits=False` for a fresh layout), and on an exception restores the previous
state and re-raises. Top-level trees should still use `clear=True`.

## 4. Group classes

A sub-graph used in several places, or one a user should see as one node, belongs in a
group class; instantiating it adds a Group node, and its tree is built once.

```python
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry, InputInteger


class Jitter(CustomGeometryGroup):
    _name = "Jitter"                 # tree name and cache key; unique
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        geometry: InputGeometry = ...,   # `...` lets `>>` feed the geometry in
        amount: InputFloat = 0.2,
        seed: InputInteger = 0,
    ):
        super().__init__(geometry=geometry, amount=amount, seed=seed)

    def _build_group(self, tree):
        geometry = tree.inputs.geometry("Geometry")
        amount = tree.inputs.float("Amount", 0.2, min_value=0.0)
        seed = tree.inputs.integer("Seed")
        offset = g.RandomValue.vector(min=-1, seed=seed) * amount
        geometry >> g.SetPosition(offset=offset) >> tree.outputs.geometry("Geometry")


with g.tree("Jitter Demo", clear=True) as tree:
    g.IcoSphere(subdivisions=4) >> Jitter(amount=0.15) >> tree.outputs.geometry("Geometry")
```

- `super().__init__` keywords are the interface socket names, lowercase or as written
  (`**{"Count X": count_x}` for names with spaces). Outputs: `Jitter().o.geometry`.
- `CustomShaderGroup` and `CustomCompositorGroup` work the same way.
- Options: `_name` (required), `_color_tag`, `_warning_propagation`,
  `_tree_properties = {"description": "tooltip", "is_modifier": True}`.
  `Jitter.create_group()` builds the tree with no surrounding context; groups nest.
- `_build_group` runs once per `_name` per session: in a live session use `run_source`.
- Ready-made groups in `nodebpy.nodes.geometry.groups`: `SliceToIndices`,
  `OtherVertex`, `OffsetVector`, `PrincipalComponents`,
  `GeometryPrincipalComponents`, `ClipFieldToBox`.

## 5. Essentials and asset libraries

Blender's bundled Essentials groups (Array, Smooth by Angle, hair tools, ...) are
classes in `g`: `g.Cube() >> g.SmoothByAngle(angle=0.6) >> g.Array(count=4)`, appended
once and reused. `nodebpy lookup search` lists them as `GeometryNodeGroup`.

Creating an asset group reads its whole library; to take several from one library,
link them up front in one read:

```python
from nodebpy.builder import link_assets

link_assets(g.Array, g.SmoothByAngle)
```

For a project whose groups ship as a `.blend` asset library generated from Python (the
Molecular Nodes pattern), see the docs page "assets" and the `nodebpy` command:

```bash
nodebpy build <sources_dir> <out.blend>        # python -> .blend
nodebpy dump <in.blend> <sources_dir>          # .blend -> python
nodebpy dump --api-only <in.blend> <pkg_dir>   # typed classes only
nodebpy check                                  # CI: build, then dump reproduces the sources
nodebpy textconv <in.blend>                    # the dump as text, for git diff
```

Configuration lives in `[tool.nodebpy.assets]` in pyproject.toml. `#` comments in
`_build_group` don't survive `dump`; use socket `description=` strings instead.
