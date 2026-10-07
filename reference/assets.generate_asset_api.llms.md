# assets.generate_asset_api

``` python
generate_asset_api(
    libraries,
    output_path,
    *,
    names=None,
    nodebpy_pkg='nodebpy',
    docstrings=True,
)
```

Generate typed asset classes for `libraries` into one module.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| libraries | AssetLibrary \| Sequence\[AssetLibrary\] | One or more :class:`~nodebpy.builder.AssetLibrary` instances (:class:`~nodebpy.builder.BundledLibrary` for Blender’s bundled assets, :class:`~nodebpy.builder.PackageLibrary` for a `.blend` shipped inside your own package). | *required* |
| output_path | str \| Path | The `.py` file to write. | *required* |
| names | set\[str\] \| None | Restrict generation to these asset (node-group) names; defaults to all. | `None` |
| nodebpy_pkg | str | Import anchor for nodebpy in the generated module. Defaults to the absolute `"nodebpy"`. When nodebpy is vendored inside another package, pass the path that reaches it *relative to the generated module’s package*, such as `"..vendor.nodebpy"`. | `'nodebpy'` |
| docstrings | bool | Emit numpy-style class docstrings (description, `Parameters`, `Inputs`, `Outputs`) from the asset’s own socket tooltips, so editors show documentation alongside the type hints. Pass `False` for a terser module. | `True` |

## Returns

| Name | Type        | Description                |
|------|-------------|----------------------------|
|      | list\[str\] | The generated class names. |
