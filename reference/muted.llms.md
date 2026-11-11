# muted

``` python
muted(source, value=None)
```

Link `source` into an input through a muted link.

A muted link stays in the tree but passes nothing, so the input uses its own value: `value`, or the socket’s default when `value` is `None`. It works wherever a node or socket is passed as an input::

    g.JoinGeometry([muted(set_position), geo])
    g.SetPosition(geometry=geo, offset=muted(offset, value=(0, 0, 1)))
    muted(geo) >> g.SetPosition() >> tree.outputs.geometry("Geometry")

`source` must be a node or socket: the muted link is the one from it.
