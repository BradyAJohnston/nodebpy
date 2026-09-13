# default_split_inputs

``` python
default_split_inputs(split=True)
```

Scope in which every `TreeBuilder` left at its default `split_inputs` splits the Group Input node into one instance per consumer node (with unused sockets hidden) on context exit.

An explicit `split_inputs=True/False` is unaffected, and so are trees that disable auto-arrangement (as `snapshot_positions` dumps do) — their authored layout, including any authored Group Input splits, must survive untouched.
