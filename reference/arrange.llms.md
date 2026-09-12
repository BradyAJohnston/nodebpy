# arrange

``` python
arrange(tree, method='sugiyama')
```

Arrange the nodes of a tree.

`method` selects the algorithm: `"sugiyama"` (or a :class:`SugiyamaOptions` instance for tuned settings), `"simple"` (or a :class:`SimpleOptions` instance), or None to leave the tree untouched.

The Sugiyama layout requires the optional `networkx` dependency; when it is missing, the simple arrangement is used instead (with a warning).
