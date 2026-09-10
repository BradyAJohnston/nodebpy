# assets.dump_library

``` python
dump_library(
    blend_path,
    output_dir,
    *,
    names=None,
    nodebpy_pkg='nodebpy',
    snapshot_positions=False,
    keep_reroutes=False,
    materials=True,
    format=True,
    typed_api=False,
)
```

Dump every node-group asset in `blend_path` to Python source files.

Each asset becomes one `.py` module under `<output_dir>/<tree>/` (`geometry`/`shader`/`compositor`) with an `ASSET` marker and metadata footers. Every group class is defined exactly once: helper groups used by a single asset are embedded in that asset’s module, groups nested by several assets get their own module under `<tree>/_shared/`, and an asset nested inside other assets keeps its class in its own module — all referenced via relative imports (`__init__.py` package markers are written so the imports resolve). Materials referenced by the trees are code-generated into `materials/` modules, and other non-serialisable datablocks each module needs are recorded in its `DATABLOCK_DEPENDENCIES` footer. :func:`build_library` rebuilds the `.blend` from these files. A `blender_assets.cats.txt` next to the `.blend` is copied into `output_dir` so catalog assignments travel with the sources.

Each asset is appended into the current session for introspection and the appended groups are removed again afterwards. Run this in a session that doesn’t already hold node groups with the same names — appending renames on a clash, which would corrupt the dumped `_name` attributes; a clash raises instead. The CLI (`python -m nodebpy.assets dump`) runs in a fresh session by construction.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| blend_path | str \| Path | The `.blend` asset library to dump. | *required* |
| output_dir | str \| Path | Directory to write the per-asset modules into (created if needed). | *required* |
| names | set\[str\] \| None | Restrict the dump to these asset (node-group) names; defaults to all. A full dump first clears the managed subdirectories (`geometry`/`shader`/`compositor`/`materials`) so files from renamed or deleted assets don’t linger; a filtered dump leaves the other assets’ files in place. | `None` |
| nodebpy_pkg | str | Import anchor for nodebpy in the generated sources, as for :func:`nodebpy.export.to_python`. | `'nodebpy'` |
| snapshot_positions | bool | Preserve each node’s authored editor position so a rebuilt `.blend` opens with the same layout, instead of auto-arranging. Positions churn on every edit, so leave this off when minimal VCS diffs matter more than layout fidelity. | `False` |
| keep_reroutes | bool | Preserve reroute nodes instead of collapsing them into direct links. | `False` |
| materials | bool | Code-generate materials referenced by the dumped trees into `materials/` modules (the default). With `False` they are only recorded as `DATABLOCK_DEPENDENCIES`, to be resolved at build time like any other non-serialisable datablock. | `True` |
| format | bool | Run the generated sources through `ruff format` when available. | `True` |
| typed_api | bool | Merge the typed asset API into the dumped classes: each asset class gains a numpydoc docstring, `_Inputs`/`_Outputs` accessors and a typed `__init__`, subclasses `Asset*Group` and carries `_library = PackageLibrary(__file__, <relative path to blend_path>)` — so at runtime it *appends* the shipped `.blend` while its `_build_group` remains the source of truth that regenerates it (`build_library` builds from source via :func:`nodebpy.builder.build_from_source`). Shared helper modules get the typed API too (but stay `Custom*Group` — they are not assets), group calls in generated bodies use the typed parameter names, and each tree directory’s `__init__.py` re-exports its asset classes. Everything outside `_build_group` is regenerated on the next dump. | `False` |

## Returns

| Name | Type | Description |
|----|----|----|
|  | dict\[str, Path\] | Mapping of asset name to the file it was written to. |
