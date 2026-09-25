# live.RunResult

``` python
RunResult(tree, created, namespace)
```

What :func:`run_source` produced.

## Attributes

| Name | Description |
|----|----|
| [`created`](#nodebpy.live.RunResult.created) | Every node group that exists after the run and did not before. |
| [`namespace`](#nodebpy.live.RunResult.namespace) | The globals the code ran in. |
| [`tree`](#nodebpy.live.RunResult.tree) | The tree the run produced, or `None` if it made no tree. |
