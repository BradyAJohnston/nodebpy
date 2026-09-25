# live.GroupStash

``` python
GroupStash(stashed=dict())
```

Existing node groups renamed out of the way before a run.

Maps each original name to the old tree, now named `<name>.stale`.

## Attributes

| Name                                          | Description |
|-----------------------------------------------|-------------|
| [`stashed`](#nodebpy.live.GroupStash.stashed) |             |

## Methods

| Name | Description |
|----|----|
| [replace](#nodebpy.live.GroupStash.replace) | Success path: for each name, if the run created a new tree of the |
| [restore](#nodebpy.live.GroupStash.restore) | Failure path: remove any partial build under an original name and |

### replace

``` python
replace()
```

Success path: for each name, if the run created a new tree of the same type under it, point the old tree’s users (group nodes, modifiers, pinned editors) at the new one and remove the old; otherwise the old tree keeps its original name. Empties the stash, so calling it (or :meth:`restore`) again is a no-op.

### restore

``` python
restore()
```

Failure path: remove any partial build under an original name and give the old trees their names back. Empties the stash, so calling it (or :meth:`replace`) again is a no-op.
