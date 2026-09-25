# live.stash_groups

``` python
stash_groups(names)
```

Rename each existing `bpy.data.node_groups[name]` to `"<name>.stale"` and return the :class:`GroupStash` that undoes or completes the move.

A group linked from a library (an appended asset) cannot be renamed and is left in place, so `create_group()` reuses it as usual.
