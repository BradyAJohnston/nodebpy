# Reusable groups, nodes-to-code, live re-runs and assets

## Contents
1. Custom node group classes
2. Turning existing trees into code (`to_python`)
3. Live re-runs in a Blender session (`nodebpy.live`)
4. Bundled essentials and asset libraries

## 1. Custom node group classes

A sub-graph used in more than one place, or one a user should see as a single node,
belongs in a group class. Instantiating the class inside a tree adds a Group node;
the group's own tree is built the first time it is needed.

```python
from nodebpy import geometry as g
from nodebpy.builder import CustomGeometryGroup
from nodebpy.types import InputFloat, InputGeometry, InputInteger


class Jitter(CustomGeometryGroup):
    _name = "Jitter"                 # tree name and cache key; must be unique
    _color_tag = "GEOMETRY"

    def __init__(
        self,
        geometry: InputGeometry = ...,   # `...` lets `>>` feed the geometry in
        amount: InputFloat = 0.2,
        seed: InputInteger = 0,
    ):
        super().__init__(**{"Geometry": geometry, "Amount": amount, "Seed": seed})

    def _build_group(self, tree):
        geometry = tree.inputs.geometry("Geometry")
        amount = tree.inputs.float("Amount", 0.2, min_value=0.0)
        seed = tree.inputs.integer("Seed")
        offset = g.RandomValue.vector(min=-1, seed=seed) * amount
        geometry >> g.SetPosition(offset=offset) >> tree.outputs.geometry("Geometry")


with g.tree("Jitter Demo", clear=True) as tree:
    g.IcoSphere(subdivisions=4) >> Jitter(amount=0.15) >> tree.outputs.geometry("Geometry")
```

- `super().__init__(**{...})` keys are the group's interface socket *names*. The
  `__init__` override is optional; without it, pass socket names as keywords directly
  (`Jitter(Amount=0.15)`, lowercase also resolves).
- Output sockets of the group node are reached like any node: `Jitter().o.geometry`.
- Also available: `CustomShaderGroup`, `CustomCompositorGroup` (from `nodebpy.builder`).
- Class options: `_name` (required), `_color_tag`, `_warning_propagation`,
  `_tree_properties = {"description": "tooltip"}`.
- `Jitter.create_group()` builds (or returns) the bpy tree without a surrounding context.
- Groups can nest: use one group class inside another's `_build_group`.
- **Caching**: `_build_group` runs once per `_name` per Blender session. If you change the
  class and run again in the same session, the old tree is reused. In a fresh headless
  process this never matters; in a live session use `nodebpy.live.run_source` (section 3)
  or delete `bpy.data.node_groups[_name]` first.
- Reusing a `_name` for a different tree type raises
  `TypeError ... already exists as GeometryNodeTree ... Use a unique _name`.
- Built-in helper groups live in `nodebpy.nodes.geometry.groups`: `SliceToIndices`,
  `OtherVertex`, `OffsetVector`, `PrincipalComponents`, `GeometryPrincipalComponents`,
  `ClipFieldToBox`. Check there before writing a common utility yourself.

## 2. Turning existing trees into code

```python
import bpy
from nodebpy.export import to_python

print(to_python(bpy.data.node_groups["My Tree"]))                  # new tree each run
print(to_python(bpy.data.node_groups["My Tree"], in_place=True))   # rebuilds that datablock
print(to_python(obj.modifiers["GeometryNodes"].node_group))
print(to_python(bpy.data.materials["Mat"].node_tree))
```

Works on any tree, including ones wired by hand in the GUI; also `tree.to_python()` on
a builder. Options:

- `in_place=True`: header becomes `TreeBuilder("Name", clear=True)`, so running the
  code rebuilds the same datablock and keeps modifiers attached. Use this when the goal
  is to edit an existing tree.
- `top_level="class"`: emits a `CustomGeometryGroup` subclass; build with `Cls.create_group()`.
- `snapshot_positions=True`: keeps the hand-made node positions (`arrange=None` + a
  position block) instead of re-arranging.
- `min_chain_length=3`: how long a linear run must be before it is written as a `>>`
  chain; `format=True` runs ruff on the output if installed.
- `strict=True` raises `CodegenError` on a node without a nodebpy class (legacy nodes
  from old files). `strict=False` emits a placeholder; or register an emitter:
  `from nodebpy.export.codegen import register_emitter`.

Round-trip check (useful after editing generated code):

```python
code = to_python(tree)
ns = {}
exec(code, ns)
rebuilt = ns["tree"]            # a TreeBuilder
assert len(rebuilt) == len(tree)
```

Generated code is a good way to learn idioms: build something in the GUI (or have the
user do it), dump it, and read how nodebpy expresses it.

## 3. Live re-runs in a Blender session

When an agent or user iterates on the same script inside one running Blender (text
editor, MCP `execute_blender_code`), two things go wrong with a plain `exec`: group
classes reuse their stale cached trees, and trees built without `clear=True` pile up as
`.001`, `.002`. `nodebpy.live.run_source` handles both:

```python
from nodebpy.live import run_source

result = run_source(code_string, filename="build_tree.py")
result.tree        # the bpy NodeTree the run produced (or None)
result.created     # bpy node groups that did not exist before this run
result.namespace   # the globals the code ran in
```

It stashes group trees claimed by class `_name`s in the code, rebuilds them, remaps
every user (modifiers, group nodes) onto the rebuilt trees, and keeps modifier input
values by socket name. On an exception it restores the previous state and re-raises.
Top-level trees in the code should still use `clear=True` (or `in_place=True` output).

Lower-level pieces, if you need them: `stash_groups`, `preserve_modifier_inputs`,
`group_names_in_source`.

## 4. Bundled essentials and asset libraries

Blender's bundled "Essentials" node groups (Array, Smooth by Angle, hair tools, ...) are
ordinary classes in `g`: `g.Cube() >> g.SmoothByAngle(angle=0.6) >> g.Array(count=4)`.
Each is appended once from Blender's bundled library and reused. Their `lookup.py`
bl_idname is `GeometryNodeGroup`.

For a project whose node groups ship as a `.blend` asset library generated from Python
(the Molecular Nodes pattern), see the nodebpy docs page "assets" and the CLI:

```bash
uv run -m nodebpy.assets build <sources_dir> <out.blend>   # python -> .blend
uv run -m nodebpy.assets dump <in.blend> <sources_dir>     # .blend -> python
uv run -m nodebpy.assets check                             # CI: build then dump reproduces sources
```

Configuration lives in `[tool.nodebpy.assets]` in pyproject.toml. Python `#` comments
inside `_build_group` do not survive `dump`; put explanations in socket `description=`
strings or the group's `_tree_properties`.
