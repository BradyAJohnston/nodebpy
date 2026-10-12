# Verifying what you built

Building without errors is not building the right tree: `>>` picks sockets by type,
and an unlinked input silently uses its default. Pick the checks that fit the task.

## Contents
1. A quick report
2. Looking at the tree
3. Checking structure
4. Evaluating the geometry
5. Simulations
6. Checking numbers

## 1. A quick report

Attach the tree to an object, evaluate it, and print a few lines:

```python
import bpy


def report(tree, obj_name="Cube"):
    obj = bpy.data.objects[obj_name]
    mod = obj.modifiers.get("GN") or obj.modifiers.new("GN", "NODES")
    mod.node_group = tree.tree          # the bpy NodeTree, not the builder
    obj.update_tag()
    geo = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).evaluated_geometry()
    print(f"{tree.tree.name}: {len(tree)} nodes, {len(tree.tree.links)} links")
    print(geo)                          # vertex / face / point / instance counts
```

Missing geometry, zero instances or a count off by a factor usually point at a link
into the wrong socket.

## 2. Looking at the tree

- `print(tree.to_mermaid())` lists every link as text: the cheapest way to check that
  each link goes where you meant.
- `tree.to_plot("tree.png")` draws the tree as Blender's editor does (needs
  matplotlib). Look for inputs you meant to drive that still show a default value.
- `tree.to_plot("group.png", node=True)` draws the group as the single node users see,
  which shows its interface.

## 3. Checking structure

`len(tree)`, `len(tree.tree.links)`, `node.node.inputs["Offset"].is_linked`,
`tree.tree.interface.items_tree`, and for a switch its type
(`switch.input_type` / `switch.data_type`).

## 4. Evaluating the geometry

```python
ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
mesh = ev.to_mesh()                               # mesh data only
print(len(mesh.vertices), [a.name for a in mesh.attributes])
geo = ev.evaluated_geometry()                     # every component
pc = geo.instances_pointcloud()                   # one point per instance
```

- `geo.pointcloud.attributes`, `geo.mesh`, `geo.curves` hold the components.
- Unrealized instances: `pc.attributes["instance_transform"].data[i].value` is the
  instance's FLOAT4X4 transform (column 2 its local Z axis, column 3 its translation).
- Evaluated data belongs to the depsgraph and is freed on the next update
  (`ReferenceError: StructRNA of type ... has been removed`). Keep the objects you
  read in variables, copy values into plain lists straight away, and evaluate again
  after each `frame_set` or input change.

## 5. Simulations

A simulation zone only advances when frames are stepped in order:

```python
scene = bpy.context.scene
for frame in range(scene.frame_start, 25):
    scene.frame_set(frame)
geo = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).evaluated_geometry()
```

## 6. Checking numbers

A correct-looking graph can still compute the wrong thing, usually through where a
field is evaluated. When the tree computes something numeric (a displacement, a stored
attribute), compare the evaluated values against the same formula in plain Python.
