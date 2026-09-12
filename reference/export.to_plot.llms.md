# export.to_plot

``` python
to_plot(tree, filepath, *, title=None, dpi=150)
```

Draw the tree’s current layout to an image file.

Nodes are rectangles at their real locations with the same estimated dimensions the arranger uses; links are curves between estimated socket positions, so what you see is what the layout algorithm saw.
