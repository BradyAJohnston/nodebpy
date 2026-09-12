# assets.plot_library

``` python
plot_library(blend_path, output_dir, names=None, *, dpi=150, arrange=None)
```

Render node groups from `blend_path` to PNG images under `output_dir` — a headless look at node graphs, e.g. for posting in pull requests (`python -m nodebpy.assets plot`).

`names` selects the groups to plot: exact names or :mod:`fnmatch` wildcard patterns (`"Style *"`), matched against *every* node group in the `.blend` (not just assets); `None` plots them all. A pattern matching nothing raises. Each tree is drawn with :func:`nodebpy.export.to_plot` (which needs the optional `matplotlib` dependency) at its stored layout, or re-arranged first when `arrange` options are given. Everything appended for plotting is removed from the session again afterwards.

## Returns

| Name | Type | Description |
|----|----|----|
|  | dict\[str, Path\] | Mapping of group name to the image it was written to. |
