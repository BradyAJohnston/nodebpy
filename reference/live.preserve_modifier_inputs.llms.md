# live.preserve_modifier_inputs

``` python
preserve_modifier_inputs(trees)
```

Keep Geometry Nodes modifier input values across an interface rebuild.

Snapshots the input state of every Geometry Nodes modifier (on any object) whose `node_group` is one of `trees`, keyed by interface socket *name*: the value, and whether the input reads a named attribute instead (`type` and `attribute_name`). On exit — also when the body raised, so a failed in-place rebuild keeps the values of the sockets it did build — each entry whose socket name still exists on the modifier’s (possibly rebuilt, possibly remapped) tree is reapplied; sockets whose type changed are skipped, as is anything that fails to apply — the reapply step never raises.
