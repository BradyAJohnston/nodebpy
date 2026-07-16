# assets.generate_asset_modules

``` python
generate_asset_modules(
    libraries,
    output_dir,
    *,
    names=None,
    nodebpy_pkg='nodebpy',
)
```

Generate typed asset classes for `libraries`, split into one module per tree type inside `output_dir`.

Writes `geometry.py`, `shader.py` and/or `compositor.py` — one module for each tree type that has assets in the libraries (no file for the others). Asset names repeat across editors (a geometry *and* a compositor “Combine Spherical” both exist), so splitting keeps the generated class names collision-free where a single :func:`generate_asset_api` module would silently shadow one with the other.

Parameters are as for :func:`generate_asset_api`, except `output_dir` is the directory to write the modules into (created if needed).

Returns a mapping of module name (`"geometry"` / `"shader"` / `"compositor"`) to the class names written to it.
