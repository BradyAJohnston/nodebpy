# assets.plot_library

``` python
plot_library(
    blend_path,
    output_dir,
    names=None,
    *,
    dpi=150,
    arrange=None,
    tree=True,
    node=True,
    open_panels=False,
)
```

Render node groups from `blend_path` to PNG images under `output_dir` — a headless, Blender-styled look at node graphs, e.g. for reviewing new nodes in pull requests (`python -m nodebpy.assets plot`).

`names` selects the groups to plot: exact names or :mod:`fnmatch` wildcard patterns (`"Style *"`), matched against *every* node group in the `.blend` (not just assets); `None` plots them all. A pattern matching nothing raises. Each group is rendered twice: its internals (`<name>.png`, :func:`nodebpy.export.to_plot`, drawn at the stored layout or re-arranged first when `arrange` options are given) and the single group node a user sees when adding it (`<name>_node.png`, `to_plot(node=True)`, with every interface panel expanded when `open_panels` is set); `tree=False` / `node=False` skip either. Both need the optional `matplotlib` dependency. Everything appended for plotting is removed from the session again afterwards.

## Returns

| Name | Type | Description |
|----|----|----|
|  | dict\[str, Path\] | Mapping of group name (suffixed with `" (node)"` for the group-node render) to the image it was written to. |
