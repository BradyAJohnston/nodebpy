# assets.generate_asset_api

``` python
generate_asset_api(libraries, output_path, *, names=None, nodebpy_pkg='nodebpy')
```

Generate typed asset classes for `libraries` into `output_path`.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| libraries | AssetLibrary \| Sequence\[AssetLibrary\] | One or more :class:`~nodebpy.builder.AssetLibrary` instances (:class:`~nodebpy.builder.BundledLibrary` for Blender’s bundled assets, :class:`~nodebpy.builder.PackageLibrary` for a `.blend` shipped inside your own package). | *required* |
| output_path | str \| Path | The `.py` file to write. | *required* |
| names | set\[str\] \| None | Restrict generation to these asset (node-group) names; defaults to all. | `None` |
| nodebpy_pkg | str | Import anchor for nodebpy in the generated module. Defaults to the absolute `"nodebpy"`. When nodebpy is vendored inside another package, pass the path that reaches it *relative to the generated module’s package* — e.g. `"..vendor.nodebpy"` — so the emitted imports stay relative to the install/vendor location. | `'nodebpy'` |
| Returns |  |  | *required* |
