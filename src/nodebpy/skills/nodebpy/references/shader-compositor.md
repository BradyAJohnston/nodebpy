# Shaders, materials, worlds and the compositor

```python
from nodebpy import shader as s
from nodebpy import compositor as c
```

Each tree type has its own module, with the nodes that tree accepts. Some names exist
in several modules behind different nodes; import each module where it is used.

## Contents
1. Materials
2. Shader node groups
3. Worlds
4. Compositor groups
5. Shader specifics
6. Compositor specifics

## 1. Materials

```python
with s.material("Rust", clear=True) as mat:        # starts empty; re-runs rebuild in place
    noise = s.NoiseTexture(scale=8.0).o.fac
    rust = s.Mix.color(noise, (0.3, 0.1, 0.05, 1.0), (0.6, 0.25, 0.1, 1.0))
    s.PrincipledBSDF(base_color=rust, roughness=noise.map_range(0, 1, 0.4, 0.9)) >> s.MaterialOutput()

obj.data.materials.append(mat.material)           # mat.material is the bpy.types.Material
```

In a geometry tree, `g.SetMaterial(material=mat.material)` assigns it to generated
geometry, which has no material of its own otherwise. Without `clear=True` a second
run makes `Rust.001`.

## 2. Shader node groups

```python
with s.tree("Stripes", clear=True) as tree:
    a = tree.inputs.color("Color A")
    b = tree.inputs.color("Color B")
    wave = s.WaveTexture(scale=tree.inputs.float("Scale", 6.0)).o.fac
    wave.mix.color(a, b) >> tree.outputs.color("Color")
```

Materials and worlds have no interface of their own; put anything a user should adjust
into a shader group. Shader trees also have `s.RepeatZone` and `s.ClosureZone`
([zones-and-items.md](zones-and-items.md)).

## 3. Worlds

There is no world builder; wrap the world's own node tree:

```python
from nodebpy.builder import TreeBuilder

world = bpy.data.worlds.new("Studio")
with TreeBuilder(world.node_tree, clear=True):
    s.Background(color=(0.05, 0.06, 0.08, 1.0), strength=1.0) >> s.WorldOutput()
bpy.context.scene.world = world
```

## 4. Compositor groups

```python
with c.tree("Soft Glow", clear=True) as tree:
    image = tree.inputs.color("Image")
    glow = c.Blur(image, size=(20, 20))
    c.Mix.color(0.3, image, glow, blend_type="SCREEN") >> tree.outputs.color("Image")

bpy.context.scene.compositing_node_group = tree.tree   # the scene's compositor
```

Frames work as in geometry trees (`with c.Frame("Label"):`).

## 5. Shader specifics

- Shader trees have no Compare node: `a > b` builds Math GREATER_THAN, giving 1.0 / 0.0.
- `Mix` variants take `(factor, a, b)`. Pass `a` explicitly: `x >> s.Mix.color(...)`
  links into Factor, the first compatible input.
- A shader output can't feed a color input (`SocketError`).
- Shader colors carry no alpha through links: a color tuple of sockets takes
  (red, green, blue), and a linked alpha raises.
- Read geometry-node attributes with `s.Attribute(attribute_type="INSTANCER",
  attribute_name="col")` when they were stored on instances before Instance on Points,
  `"GEOMETRY"` otherwise.
- `s.Raycast().items.float("height")` samples the `height` attribute where the ray
  hits: the item's input is the attribute name and its `.output` the value read (named
  after the attribute unless a name is given). A color item also has an
  `"<name> Alpha"` output on the node. Attribute sampling is Cycles-only.
- `s.MenuSwitch.shader(menu, {...})` switches shaders.

## 6. Compositor specifics

- `c.Switch` is the typed Switch (Blender 5.2 deprecates the old Color-only one) and
  `c.IndexSwitch(index, [...])` the same Index Switch as in Geometry Nodes, both
  inferring their type from their values; with nothing to infer from, an Index Switch
  is a Color switch. The compositor switches FLOAT, INT, BOOLEAN, VECTOR, RGBA,
  ROTATION, MATRIX, STRING, MENU, OBJECT, FONT and INT_VECTOR
  (`c.IndexSwitch.integer_vector(...)`).
- `c.FileOutput(directory="//renders/").items.color(image, "Beauty")` adds an input
  to write (Float, Vector or Color).
- Noise, White Noise and Voronoi Texture start 2D in the compositor, 3D elsewhere.
