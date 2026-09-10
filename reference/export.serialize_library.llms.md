# export.serialize_library

``` python
serialize_library(trees)
```

`tree_clipper` JSON data for each tree in `trees` (nested groups included), keyed by tree name. The trees must be in the current session: the capture is enriched from the live data with what the JSON alone can’t express — each socket’s `is_inactive` flag (codegen’s criterion for evaluation-inert links) and datablock references resolved to names instead of serialization-order ids.
