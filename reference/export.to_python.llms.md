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
    group_class_names=None,
    external_groups=None,
    typed_groups=None,
    root_interface=None,
)
```

Generate Python code that recreates the given node tree using nodebpy.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| tree | NodeTree \| TreeBuilder | The node tree to export. | *required* |
| min_chain_length | int | Minimum number of items (including interface endpoints) for a linear pipeline to be expressed with `>>` syntax; shorter runs are emitted as flat assignments. | `3` |
| strict | bool | If True (default), raise :class:`CodegenError` for nodes that have no nodebpy class and no registered emitter. If False, emit a `var = None # TODO` placeholder instead. | `True` |
| max_inline_width | int \| None | Longest rendered expression (in characters) that may inline into its consumer’s statement; longer values bind to a variable first, so deep graphs split into steps instead of collapsing into one huge statement. `>>` chain continuations are exempt — a pipeline stays one statement; statements longer than 88 columns wrap in parentheses with one `>>` segment per line. `None` disables the budget. | `88` |
| snapshot_positions | bool | If True, build the tree with `arrange=None` (no auto-layout) and append a block that restores each node’s authored `location` by name. Nodes a rebuild doesn’t recreate (reroutes — unless `keep_reroutes`) or names a rebuild assigns differently (duplicate-type nodes created in another order) are skipped via `tree.tree.nodes.get(name)`. | `False` |
| keep_reroutes | bool | If True, preserve reroute nodes as `g.Reroute(...)` pass-throughs instead of collapsing each reroute chain into a direct link. Useful with `snapshot_positions` to reproduce the original wire routing. | `False` |
| top_level | Literal\['with', 'class'\] | How the top-level tree is rendered. `"with"` (default) emits a `with TreeBuilder(...) as tree:` block. `"class"` emits the top-level tree as a `Custom*Group` subclass too — so every node group, including the one being exported, becomes a class. Build any of them with `ClassName.create_group()`; useful for archiving a set of node groups as plain, reusable Python. | `'with'` |
| format | bool | If True (default) and the optional `ruff` package is installed, the generated source is run through `ruff format` for tidier output. A no-op when `ruff` is unavailable. | `True` |
| nodebpy_pkg | str | Import anchor for nodebpy in the generated source. Defaults to the absolute `"nodebpy"`. When nodebpy is vendored inside another package, pass the path that reaches it *relative to the generated module’s package* — e.g. `"..vendor.nodebpy"` — so the emitted imports stay relative to the install/vendor location. | `'nodebpy'` |
| group_class_names | Mapping\[str, str\] \| None | Class name to use for a given tree name, overriding the derived PascalCase name — for callers that split groups across several generated modules and need the names to agree between them. | `None` |
| external_groups | Collection\[str\] \| None | Tree names whose classes are defined in another module: they are referenced by their `group_class_names` entry (which must exist) but no class definition is emitted for them. The caller is responsible for making the name resolvable (e.g. an import). | `None` |
| typed_groups | Collection\[str\] \| None | Tree names whose classes carry a typed `__init__` (merged dump classes) — group calls to them are emitted with the normalized parameter names from `typed_param_names` instead of socket-name keyword keys. | `None` |
| root_interface | GroupInterface \| None | Typed-interface parts (docstring, class attributes, accessors and `__init__`) spliced into the top-level tree’s class in `class` mode, ahead of `_build_group`. | `None` |

## Returns

| Name | Type | Description                     |
|------|------|---------------------------------|
|      | str  | Python source code as a string. |
