# assets.generate_asset_modules

``` python
generate_asset_modules(
    libraries,
    output_dir,
    *,
    names=None,
    nodebpy_pkg='nodebpy',
    docstrings=True,
)
```

Generate typed asset classes for `libraries`, one module per tree type inside `output_dir`: `geometry.py`, `shader.py` and/or `compositor.py`, for the tree types that have assets. Asset names repeat across editors (a geometry and a compositor “Combine Spherical” both exist), so splitting keeps the class names from shadowing each other. Parameters are as for :func:`generate_asset_api`. Returns the class names written per module.
