# Asset Node Groups

Blender ships node-group *assets* (the bundled “essentials” libraries), and many add-ons distribute their own. `nodebpy` can generate typed Python classes for these assets so they read, link and type-check **exactly like any built-in node** — the only difference is that instantiating one *appends* the asset’s node group from its `.blend` at runtime (and points a Group node at it) instead of building the tree from scratch.

This is the asset counterpart to [Custom Node Groups](custom-node-groups.llms.md): a custom group *builds* its tree in `_build_group`; an asset group *appends* a pre-authored one.

## Using the bundled essentials

The classes for Blender’s bundled essentials libraries are generated into `nodebpy.nodes.{geometry,shader,compositor}` and exported alongside the built-in nodes, so you reach them straight off the editor module:

``` python
from nodebpy import geometry as g

with g.tree("Assets") as tree:
    (
        g.Cube()
        >> g.SmoothByAngle(angle=0.6)
        >> g.Array(count=4)
        >> tree.outputs.geometry()
    )

tree
```

Each asset is a normal node: typed inputs/outputs (`g.SmoothByAngle().o.mesh` is a `GeometrySocket`), `>>` chaining, IDE autocomplete, and the usual operators. The underlying node group is appended once and reused on subsequent uses.

## Generating an API for your own assets

`generate_asset_api` introspects a `.blend` asset library and writes a module of typed classes. Point it at your library and a destination `.py` file:

``` python
from nodebpy.assets import generate_asset_api, PackageLibrary

generate_asset_api(
    PackageLibrary(__file__, "data/my_assets.blend"),
    "my_addon/nodes/assets.py",
)
```

`PackageLibrary(anchor, relative)` locates a `.blend` shipped inside your own package (resolved relative to `anchor`, usually `__file__`); use `BundledLibrary("…")` for a library that ships with Blender. You can pass a list of libraries to merge several into one module, and `names={...}` to restrict generation to specific node groups.

If your libraries mix tree types, use `generate_asset_modules` instead — it takes a directory and writes one module per tree type (`geometry.py`, `shader.py`, `compositor.py`), skipping tree types with no assets:

``` python
from nodebpy.assets import generate_asset_modules, PackageLibrary

generate_asset_modules(
    PackageLibrary(__file__, "data/my_assets.blend"),
    "my_addon/nodes/",
)
```

Because asset names repeat across editors, splitting also keeps the generated class names collision-free where a single mixed module would silently shadow one tree type’s class with another’s.

### Docstrings and menu types

By default the generated classes carry numpy-style docstrings built from the asset’s own interface — the group description, then `Parameters`, `Inputs` and `Outputs` sections using each socket’s tooltip — so editors show documentation next to the type hints. Menu sockets are narrowed to the items they actually offer:

``` python
def __init__(
    self,
    geometry: InputGeometry = None,
    shape: InputMenu | Literal["Line", "Circle", "Curve", "Transform"] = "Line",
    ...
```

Pass `docstrings=False` (or `--no-docstrings` on the command line) for a terser module without the class docstrings.

The generated module imports from `nodebpy` and looks like any other node module, so import and use it directly:

``` python
from my_addon.nodes import assets as a

with a.tree("Demo") as tree:
    _ = a.MyAsset(value=2.0) >> tree.outputs.geometry()
```

Re-run `generate_asset_api` whenever the `.blend` changes — the classes are regenerated from the assets’ current interfaces.

## How resolution works

Generated classes carry the library reference, not a hard-coded path, and the group is located on demand:

| Library | Resolves to |
|:---|:---|
| `BundledLibrary("geometry_nodes_essentials.blend")` | Blender’s system datafiles (`…/datafiles/assets/nodes/…`) |
| `PackageLibrary(__file__, "data/my_assets.blend")` | a path relative to the generated module’s file |

Because asset names can collide across editors (a geometry **and** a compositor “Combine Spherical” both exist), an appended group is reused only when its tree type matches; otherwise the correct one is appended fresh.

## Dumping a library to Python source (and back)

`dump_library` and `build_library` round-trip a whole `.blend` asset library through per-asset Python modules, so the `.py` files — not the binary `.blend` — can be the version-controlled source of truth:

``` python
# | eval: false
from nodebpy.assets import build_library, dump_library

dump_library("my_assets.blend", "my_assets_src/")   # one .py per asset
build_library("my_assets_src/", "my_assets.blend")  # rebuild the .blend
```

or from the command line (each runs in a fresh Blender session):

``` bash
python -m nodebpy.assets dump my_assets.blend my_assets_src/
python -m nodebpy.assets build my_assets_src/ my_assets.blend
```

Node groups can also be rendered to PNG images headlessly — for reviewing layouts or posting graphs in pull requests — selected by exact name or wildcard (`plot_library` in Python):

``` bash
python -m nodebpy.assets plot my_assets.blend plots/ "Style *"
```

By default each tree is drawn at its stored layout; pass `--arrange` (plus any of the arrangement flags shared with `build`, e.g. `--add-reroutes`) to re-arrange before plotting.

Each asset becomes one module holding its group as a class; helper groups used by a single asset are embedded, groups shared between assets get their own module under `_shared/`, and referenced materials are code-generated under `materials/`. Asset metadata (catalog, description, tags), tree-level flags and non-serialisable datablock references (`DATABLOCK_DEPENDENCIES`) travel in module footers, and a `blender_assets.cats.txt` next to the `.blend` is copied along so catalog assignments survive. Pass `snapshot_positions=True` to keep authored node layouts (including split Group Input instances), and `--typed-api` / `typed_api=True` to merge the typed asset API from above into the dumped classes. On the build side the automatic layout is tunable: `--add-reroutes` / `add_reroutes=True` arranges the rebuilt trees with reroute nodes routing long links around nodes (the node-arrange addon’s behaviour), and `--spacing`, `--iterations` (crossing reduction), `--direction`, `--socket-alignment` and the other `SugiyamaOptions` fields (`arrange=SugiyamaOptions(...)` in Python) override the defaults; sources dumped with `snapshot_positions` keep their authored layout regardless.

Round-trip fidelity is checked with `nodebpy.export.compare_libraries` / `serialize_library` (or `python -m nodebpy.export.parity a.blend b.blend`), which deep-compare two libraries with cosmetic surfaces (positions, reroutes, …) excludable — Blender’s bundled essentials libraries and MolecularNodes round-trip to zero functional findings.

## Notes

- The generator is a normal runtime tool — call `generate_asset_api` in a build step, a test, or once by hand; commit the generated module like the rest of your source.
- Inputs with non-scalar defaults (vectors, colours) take `None` in the generated signature; the appended group keeps its own socket defaults.
- `nodebpy`’s own bundled-essentials modules are regenerated by `python -m nodebpy.assets` (wired into `make generate`).
