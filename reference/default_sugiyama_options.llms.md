# default_sugiyama_options

``` python
default_sugiyama_options(options)
```

Scope in which `arrange(tree, "sugiyama")` — and therefore every `TreeBuilder` left at its default arrangement — uses `options` instead of `SugiyamaOptions()`.

Explicit `SugiyamaOptions` / `SimpleOptions` arguments and `arrange=None` (as emitted by `snapshot_positions` dumps) are unaffected.
