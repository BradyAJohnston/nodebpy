# arrange

``` python
arrange(
    tree,
    method='sugiyama',
    *,
    selected_only=False,
    pipeline=None,
    observer=None,
    verify=False,
)
```

Arrange the nodes of *tree*.

*method* is a :class:`SugiyamaOptions`, `"sugiyama"` for the default options, `"simple"` for plain columns by dependency (:data:`~.config.SIMPLE_OPTIONS`), or None to leave the tree alone.

With *selected_only* the selected nodes are arranged among themselves around where they were, and moved clear of the others, which stay put. Otherwise selection is ignored.

*pipeline*, *observer* and *verify* are passed on to :func:`~.sugiyama.sugiyama_layout`.
