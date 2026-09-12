# assets.build_library

``` python
build_library(
    source_dir,
    blend_path,
    *,
    compress=True,
    allow_existing=False,
    resources=None,
    on_missing='error',
    add_reroutes=False,
    arrange=None,
)
```

Rebuild a `.blend` asset library from sources written by :func:`dump_library`.

Imports every root module under `source_dir` (recursively; `_shared` group modules are pulled in by the root modules’ own imports), rebuilds each `MATERIAL` module’s material, builds each `ASSET` class via `create_group()`, re-marks the tree as an asset, applies the dumped `ASSET_METADATA`/`TREE_PROPERTIES`/`MATERIAL_PROPERTIES`, and writes those trees and materials (plus their dependencies) to `blend_path` with `bpy.data.libraries.write`. A `blender_assets.cats.txt` in `source_dir` is copied next to the `.blend`.

Datablocks the sources reference but cannot serialise (images, objects, …, recorded in each module’s `DATABLOCK_DEPENDENCIES`) resolve in order: already present in the session (build “in the presence” of the data — e.g. after opening a working file), appended by name from the `resources` `.blend`, or — with `on_missing="drop"` — replaced by temporary placeholders deleted again before the write, leaving those socket defaults empty. The default `on_missing="error"` raises upfront, listing everything missing.

`arrange` tunes how the built trees are laid out: a :class:`~nodebpy.SugiyamaOptions` with any of its settings (spacing, crossing-reduction iterations, direction, socket alignment, …) is scoped over the build via :func:`nodebpy.builder.default_sugiyama_options`. `add_reroutes=True` additionally inserts reroute nodes to route long links around nodes (the node-arrange addon’s behaviour); it composes with `arrange`. Either only affects modules that leave the arrangement at its default — sources dumped with `snapshot_positions` disable arrangement and keep their authored layout.

The built trees stay in the current session afterwards. Because `create_group()` reuses an existing tree of the same name (that is what deduplicates groups shared between asset files), the session must not already hold node groups when the build starts — a stale same-named group would silently end up in the `.blend`. This raises if any exist, unless `allow_existing` is passed. The CLI (`python -m nodebpy.assets build`) runs in a fresh session by construction.

## Returns

| Name | Type | Description |
|----|----|----|
|  | list\[str\] | The names of the asset node groups written to the `.blend`. |
