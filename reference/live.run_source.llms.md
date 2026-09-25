# live.run_source

``` python
run_source(code, *, filename='<nodebpy>', namespace=None)
```

Execute nodebpy source for a live re-run.

Existing groups the code’s classes claim by `_name` are stashed so `create_group()` builds fresh, Geometry Nodes modifier input values on every pre-existing tree are preserved across the rebuild, and the stashed trees’ users are remapped onto the new builds afterwards. On any exception the stash is restored and the exception re-raised unchanged; `filename` is what its traceback names. Nothing is printed or captured.

## Parameters

| Name | Type | Description | Default |
|----|----|----|----|
| code | str | The source to run. | *required* |
| filename | str | Filename for the compiled code, so tracebacks point at the caller’s Text block or file. | `'<nodebpy>'` |
| namespace | dict\[str, Any\] \| None | Extra globals merged over the defaults (`__name__`, `__file__` and `bpy`). A `tree` it carries over from an earlier run’s :attr:`RunResult.namespace` is not mistaken for this run’s tree. | `None` |

## Notes

A run that fails partway through a `with g.tree(..., clear=True)` body leaves that tree half built (the class form is atomic: the old build is restored). Groups the failed run created under other names are left behind as well.
