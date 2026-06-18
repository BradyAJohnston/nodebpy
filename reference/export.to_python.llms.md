# export.to_python

``` python
to_python(
    tree,
    min_chain_length=3,
    strict=True,
    max_inline_width=88,
    snapshot_positions=False,
    keep_reroutes=False,
    top_level='with',
    format=True,
    nodebpy_pkg='nodebpy',
)
```

Generate Python code that recreates the given node tree using nodebpy.

## Returns

| Name | Type | Description                     |
|------|------|---------------------------------|
|      | str  | Python source code as a string. |
