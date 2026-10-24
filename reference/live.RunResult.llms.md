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

## Methods

| Name | Description |
|----|----|
| [to_python](#nodebpy.live.RunResult.to_python) | The code for :attr:`tree` as it is now, to put back into the |

### to_python

``` python
to_python(**options)
```

The code for :attr:`tree` as it is now, to put back into the script that built it, edits made in Blender since included.

This is :func:`nodebpy.export.to_python` with defaults for that:

- `groups="reference"`: groups a class builds (the script’s own, Blender’s bundled assets, nodebpy’s, your modules’) are called, not written out, and a class is called by the name the script binds it to, without an import (`namespace=` :attr:`namespace`). A group changed by hand since it was built is written out under the name of the script’s class for it, to replace that class.
- A tree one of the script’s classes builds comes back as that class (`top_level="class"`); any other as a `with` block that rebuilds the tree in place (`in_place=True`).

*options* are passed on to :func:`~nodebpy.export.to_python` and override these.

#### Raises

| Name | Type       | Description               |
|------|------------|---------------------------|
|      | ValueError | The run produced no tree. |
